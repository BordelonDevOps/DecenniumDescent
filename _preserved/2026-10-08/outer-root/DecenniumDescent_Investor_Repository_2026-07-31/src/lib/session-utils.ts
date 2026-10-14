import { estimateMaxHpFromHitDie } from "@/data/class-hit-dice";
import { ORACLE_REVELATION_CHARGES } from "@/data/oracle-curses";
import { defaultMaxRp, longRestRecovery, shortRestRecovery } from "@/data/resonance-economy";
import { isSpellcasterClass } from "@/data/spell-utils";

/** Common conditions referenced in class features — quick-add only, not exhaustive rules. */
export const COMMON_CONDITIONS = [
  "Prone",
  "Blessed",
  "Poisoned",
  "Stunned",
  "Feared",
  "Blinded",
  "Restrained",
  "Invisible",
  "Dazed",
  "Slowed",
] as const;

/** Director default: L1 = 3 RC, +1 every odd level, cap 7 (matches oracle-mysteries progression). */
export function maxRevelationCharges(level = 1): number {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  return Math.min(
    ORACLE_REVELATION_CHARGES.maximum,
    ORACLE_REVELATION_CHARGES.initial + Math.floor((lvl - 1) / 2)
  );
}

/** Oracle uses Revelation Charges — not Weave Resonance Points. */
export function isOracleClass(className?: string): boolean {
  return className === "Oracle";
}

/** Weave casters spend RP; Oracle excluded (Revelation Charges track). */
export function isWeaveCaster(className?: string): boolean {
  return isSpellcasterClass(className || "");
}

export function defaultRevelationCharges(level = 1) {
  const max = maxRevelationCharges(level);
  return { current: max, max };
}

/**
 * Fallback max HP when character save lacks hp/maxHp.
 * Rulebook formula via `class-hit-dice.js` (Ch3 Classes Table HD + avg-per-level + CON).
 */
export function estimatePcMaxHp(level: number, conMod: number, className?: string): number {
  return estimateMaxHpFromHitDie(level, conMod, className || "");
}

type AbilityRow = { name: string; modifier?: number; score?: number };

type HpCharacter = {
  hp?: number;
  maxHp?: number;
  level?: number;
  class?: string;
  abilities?: AbilityRow[];
};

/** Prefer stored hp/maxHp from character save; fall back to estimatePcMaxHp. */
export function resolvePcHp(char: HpCharacter): { hp: number; maxHp: number; fromSave: boolean } {
  const storedMax = Number(char.maxHp);
  const storedHp = Number(char.hp);
  if (Number.isFinite(storedMax) && storedMax > 0) {
    return {
      maxHp: storedMax,
      hp: Number.isFinite(storedHp) && storedHp >= 0 ? storedHp : storedMax,
      fromSave: true,
    };
  }
  const con = char.abilities?.find((a) => a.name === "Constitution");
  const conMod =
    typeof con?.modifier === "number"
      ? con.modifier
      : typeof con?.score === "number"
        ? Math.floor((con.score - 10) / 2)
        : 0;
  const maxHp = estimatePcMaxHp(char.level || 1, conMod, char.class);
  return { hp: maxHp, maxHp, fromSave: false };
}

export function conModifierFromAbilities(abilities?: AbilityRow[]): number {
  const con = abilities?.find((a) => a.name === "Constitution");
  if (typeof con?.modifier === "number") return con.modifier;
  if (typeof con?.score === "number") return Math.floor((con.score - 10) / 2);
  return 0;
}

export function dexModifierFromAbilities(abilities?: AbilityRow[]): number {
  const dex = abilities?.find((a) => a.name === "Dexterity");
  if (typeof dex?.modifier === "number") return dex.modifier;
  if (typeof dex?.score === "number") return Math.floor((dex.score - 10) / 2);
  return 0;
}

/** Party pool default = sum of living Weave casters' max RP (Director v1). */
export function sumWeaveCasterMaxRp(
  combatants: { isEnemy: boolean; hp: number; characterClass: string; level: number }[]
): number {
  return combatants
    .filter((c) => !c.isEnemy && c.hp > 0 && isWeaveCaster(c.characterClass))
    .reduce((sum, c) => sum + defaultMaxRp(c.characterClass, c.level).maxRp, 0);
}

/** Display-only: sum of living Weave casters' current RP. Per-character RP remains v1 canon. */
export function sumWeaveCasterCurrentRp(
  combatants: { isEnemy: boolean; hp: number; characterClass: string; resonance: number }[]
): number {
  return combatants
    .filter((c) => !c.isEnemy && c.hp > 0 && isWeaveCaster(c.characterClass))
    .reduce((sum, c) => sum + (Number(c.resonance) || 0), 0);
}

/** Gate boss placeholder HP until bestiary stats are wired — tier-scaled stub. */
export function gateBossStubHp(tier: number): number {
  return 40 + Math.max(1, tier) * 25;
}

/** Initiative tie-break: higher initiative → higher Dex → player add-order → name. */
export function compareInitiativeOrder(
  a: { id: string; name: string; initiative: number; isEnemy: boolean; dexMod?: number },
  b: { id: string; name: string; initiative: number; isEnemy: boolean; dexMod?: number },
  addOrder: Map<string, number>
): number {
  if (b.initiative !== a.initiative) return b.initiative - a.initiative;
  const dexDiff = (b.dexMod ?? 0) - (a.dexMod ?? 0);
  if (dexDiff !== 0) return dexDiff;
  if (!a.isEnemy && !b.isEnemy) {
    return (addOrder.get(a.id) ?? 0) - (addOrder.get(b.id) ?? 0);
  }
  if (a.isEnemy !== b.isEnemy) return a.isEnemy ? 1 : -1;
  return a.name.localeCompare(b.name);
}

type RestCombatant = {
  isEnemy: boolean;
  characterClass: string;
  level: number;
  resonance: number;
  revelationCharges: number;
  revelationChargesMax: number;
};

/** Short rest: retune ¼ max RP (Weave) + RC +1 to max (Oracle). */
export function applyShortRest(c: RestCombatant): Partial<RestCombatant> {
  if (c.isEnemy) return {};
  if (isOracleClass(c.characterClass)) {
    const max = c.revelationChargesMax || maxRevelationCharges(c.level);
    return { revelationCharges: Math.min(max, c.revelationCharges + 1), revelationChargesMax: max };
  }
  if (!isWeaveCaster(c.characterClass)) return {};
  const { maxRp } = defaultMaxRp(c.characterClass, c.level);
  const gain = shortRestRecovery(maxRp);
  return { resonance: Math.min(maxRp, c.resonance + gain) };
}

/** Long rest: full RP (Weave) and full RC (Oracle). */
export function applyLongRest(c: RestCombatant): Partial<RestCombatant> {
  if (c.isEnemy) return {};
  if (isOracleClass(c.characterClass)) {
    const max = maxRevelationCharges(c.level);
    return { revelationCharges: max, revelationChargesMax: max };
  }
  if (!isWeaveCaster(c.characterClass)) return {};
  const { maxRp } = defaultMaxRp(c.characterClass, c.level);
  return { resonance: longRestRecovery(maxRp) };
}

export function parseConditions(raw: string): string[] {
  return raw
    .split(/[,;]+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

export function formatConditions(list: string[]): string {
  return list.join(", ");
}

export function toggleCondition(raw: string, condition: string): string {
  const list = parseConditions(raw);
  const idx = list.findIndex((c) => c.toLowerCase() === condition.toLowerCase());
  if (idx >= 0) list.splice(idx, 1);
  else list.push(condition);
  return formatConditions(list);
}

export function hasCondition(raw: string, condition: string): boolean {
  return parseConditions(raw).some((c) => c.toLowerCase() === condition.toLowerCase());
}
