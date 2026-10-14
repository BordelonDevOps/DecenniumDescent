"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { AlertTriangle, Plus, Trash2, RotateCcw, Timer, Sparkles, Heart, Swords, ArrowDownUp, ChevronDown, ChevronRight, RefreshCw } from "lucide-react";
import encounters from "@/data/floor-encounters.json";
import monstersData from "@/bestiary_data_full.json";
import { loadSavedCharacters, upsertCharacter, characterDisplayName } from "@/lib/character-storage";
import ReputationPanel from "@/components/ReputationPanel";
import { getOathById } from "@/data/paladin-oaths";
import {
  DRUID_CIRCLES,
  ARCH_ATTUNEMENT_MAX,
  hasArchFormAttunement,
  hasPrimalRecovery,
  isFreeArchAttunementSwap,
  primalRecoveryRpGain,
  shapeshiftFormsForDruid,
  shapeshiftUsesAtLevel,
  wildShapeCrCap,
  wildShapeDurationMinutes,
} from "@/data/druid-shapeshifting";
import { getSpellDisplayName, searchSpellsByName } from "@/data/spell-utils";
import { SPELL_SCHOOLS } from "@/data/spells";
import { getMysteryById } from "@/data/oracle-mysteries";
import { getCurseById } from "@/data/oracle-curses";
import {
  takeEncounterHandoff,
  takeFoeHandoff,
  takeItemHandoff,
  takeSpellHandoff,
  type EncounterHandoff,
  type FoeHandoff,
  type ItemHandoff,
  type SpellHandoff,
} from "@/lib/session-handoff";
import {
  applyLongRest,
  applyShortRest,
  COMMON_CONDITIONS,
  compareInitiativeOrder,
  defaultRevelationCharges,
  dexModifierFromAbilities,
  gateBossStubHp,
  hasCondition,
  isOracleClass,
  isWeaveCaster,
  resolvePcHp,
  sumWeaveCasterCurrentRp,
  sumWeaveCasterMaxRp,
  toggleCondition,
} from "@/lib/session-utils";
import {
  BURNOUT_EFFECT_STUB,
  formatMaxRpTooltip,
  fullRestore,
  isBurnoutRisk,
  overcastBurnoutHintAfterCast,
  OVERCAST_OPTIONS,
  overcastRpCost,
  PLAYER_ALIGNMENTS,
  resolveMaxRp,
  retuneAmount,
  schoolAffinityMods,
  spellCost,
  spellCostRepModifier,
  totalCastCost,
} from "@/data/resonance-economy";
import {
  draftXpForCr,
  formatDraftXpAwardLine,
  formatXp,
  parseCrFromNotes,
  splitPartyXp,
} from "@/lib/xp-economy";

type Combatant = {
  id: string;
  name: string;
  initiative: number;
  hp: number;
  maxHp: number;
  resonance: number;
  level: number;
  revelationCharges: number;
  revelationChargesMax: number;
  characterClass: string;
  sacredOath: string;
  druidCircle: string;
  oracleMystery: string;
  oracleCurse: string;
  alignment: string;
  reputation: Record<string, number>;
  overcastIds: string[];
  burnoutRisk: boolean;
  /** Spell tier (1–9) for overcast base RP cost via spellCost(); 0 = unset. */
  castSpellTier: number;
  /** Spell school for affinity/opposition modifiers on base cost. */
  castSpellSchool: string;
  /** Optional spell key from lookup (display only). */
  castSpellKey: string;
  /** Druid wild-shape tracker (VQ-22 stub). */
  wildShapeUses: number;
  wildShapeUsesMax: number;
  activeFormId: string;
  /** Minutes remaining in current Wild Shape form (0 = not transformed). */
  wildShapeMinutesLeft: number;
  /** Primal Recovery (L13 draft) — once per short rest. */
  primalRecoveryUsed: boolean;
  /** L15+ attuned arch form ids (max 2). */
  attunedArchFormIds: string[];
  /** Free attuned arch swap used this encounter (L15 draft). */
  archAttunementSwapUsed: boolean;
  /** Post-cast Burnout / concentration hint (Mage L17 draft stub). */
  burnoutCastHint: string;
  /** Shaman totems placed for the current scene; effect resolution remains table-facing. */
  activeTotemIds: string[];
  notes: string;
  conditions: string;
  isEnemy: boolean;
  dexMod: number;
  /** Bestiary CR when known — used by draft XP award stub only. */
  challengeRating?: string;
  /** Draft XP already logged for this defeated foe (Session stub). */
  draftXpAwarded?: boolean;
  /** Session-only draft XP tally for participating allies (not written to character save). */
  draftXpSession?: number;
  /** Optional multiclass — RESONANCE_CANON.md §7; used by resolveMaxRp when present. */
  secondaryClass?: string;
  secondaryLevel?: number;
  classLevels?: Record<string, number>;
};

type MonsterRow = {
  name?: string;
  hitPoints?: number;
  challengeRating?: string;
  zoneFound?: string;
};

type SavedChar = ReturnType<typeof loadSavedCharacters>[number];

const STORAGE_KEY = "dd_session_tracker";
const HORN_AT = 1200; // Opening PoNR at hour 1200 / day 50 (Opening = 2400 h)
type CombatantFilter = "all" | "allies" | "foes";
const CROWDED_COMBATANTS = 7;
const CROWDED_FOES = 4;

/** Compact ethos labels for Session row picker. */
const ALIGNMENT_ABBREV: Record<string, string> = {
  "Lawful Good": "LG",
  "Neutral Good": "NG",
  "Chaotic Good": "CG",
  "Lawful Neutral": "LN",
  "True Neutral": "N",
  "Chaotic Neutral": "CN",
  "Lawful Evil": "LE",
  "Neutral Evil": "NE",
  "Chaotic Evil": "CE",
};

function uid() {
  return Math.random().toString(36).slice(2, 9);
}

function parseHp(m: MonsterRow): number {
  const hp = Number(m.hitPoints);
  if (Number.isFinite(hp) && hp > 0) return hp;
  const cr = parseFloat(String(m.challengeRating || "1")) || 1;
  return Math.max(10, Math.round(cr * 12));
}

function savedCharacterLabel(c: SavedChar): string {
  const identity = [c.race, c.class].filter(Boolean).join(" · ");
  return `${characterDisplayName(c)}${identity ? ` — ${identity}` : ""} · L${c.level || 1}`;
}


function rollInitiative(dexMod = 0) {
  return 1 + Math.floor(Math.random() * 20) + dexMod;
}

function castingModFromChar(char?: SavedChar | null): number {
  if (!char?.class) return 0;
  const abilityByClass: Record<string, string> = {
    Wizard: "Intelligence",
    Mage: "Intelligence",
    Cleric: "Wisdom",
    Druid: "Wisdom",
    Bard: "Charisma",
    Paladin: "Charisma",
    Ranger: "Wisdom",
    Shaman: "Wisdom",
    Mirrorsage: "Intelligence",
    "Crimson Agent": "Charisma",
    Monk: "Wisdom",
    Thief: "Charisma",
    Tinker: "Intelligence",
    Dragoon: "Charisma",
  };
  const abilityName = abilityByClass[char.class];
  if (!abilityName) return 0;
  const ability = char.abilities?.find((a: { name: string }) => a.name === abilityName);
  if (typeof ability?.modifier === "number") return ability.modifier;
  if (typeof ability?.score === "number") return Math.floor((ability.score - 10) / 2);
  return 0;
}

function combatantRpContext(
  c: Pick<Combatant, "characterClass" | "level" | "reputation" | "secondaryClass" | "secondaryLevel" | "classLevels">
) {
  return {
    secondaryClass: c.secondaryClass,
    secondaryLevel: c.secondaryLevel,
    classLevels: c.classLevels,
  };
}

function resolveCombatantMaxRp(c: Combatant) {
  return resolveMaxRp(c.characterClass, c.level, c.reputation, combatantRpContext(c));
}

function isDruidClass(className?: string) {
  return className === "Druid";
}

function isShamanClass(className?: string) {
  return className === "Shaman";
}

function maxActiveTotems(level: number) {
  if (level >= 13) return 2; // L13 draft: Second active totem slot.
  return level >= 6 ? 1 : 0; // L6 canon: Totem Pulse on placement.
}

const SHAMAN_TOTEM_OPTIONS = [
  { id: "spirit", label: "Spirit Totem" },
  { id: "echo", label: "Echo Totem" },
  { id: "divining", label: "Divining Totem" },
  { id: "blight", label: "Blight Totem" },
] as const;

function defaultWildShapeUses(level: number) {
  const max = shapeshiftUsesAtLevel(level);
  return { wildShapeUses: max, wildShapeUsesMax: max };
}

function overcastAffinityFlags(c: Combatant) {
  return schoolAffinityMods(c.alignment, c.castSpellSchool);
}

function overcastBaseCost(c: Combatant) {
  if (!c.castSpellTier) return 0;
  const { affinity, opposition } = overcastAffinityFlags(c);
  return spellCost(c.castSpellTier, {
    affinity,
    opposition,
    reputationModifier: spellCostRepModifier(c.characterClass, c.reputation),
  });
}

function normalizeCombatant(raw: Partial<Combatant>): Combatant {
  const characterClass = raw.characterClass || "";
  const level = Number(raw.level) || 1;
  const oracle = isOracleClass(characterClass);
  const rcDefaults = oracle ? defaultRevelationCharges(level) : { current: 0, max: 0 };
  const reputation =
    raw.reputation && typeof raw.reputation === "object" && !Array.isArray(raw.reputation)
      ? raw.reputation
      : {};
  const overcastIds = Array.isArray(raw.overcastIds) ? raw.overcastIds.filter(Boolean) : [];
  const castSpellTier = Math.max(0, Math.min(9, Math.round(Number(raw.castSpellTier) || 0)));
  const castSpellSchool = typeof raw.castSpellSchool === "string" ? raw.castSpellSchool : "";
  const castSpellKey = typeof raw.castSpellKey === "string" ? raw.castSpellKey : "";
  const wildDefaults = isDruidClass(characterClass) ? defaultWildShapeUses(level) : { wildShapeUses: 0, wildShapeUsesMax: 0 };
  const wildShapeUsesMax = isDruidClass(characterClass)
    ? Math.max(0, Number(raw.wildShapeUsesMax ?? wildDefaults.wildShapeUsesMax) || wildDefaults.wildShapeUsesMax)
    : 0;
  const wildShapeUses = isDruidClass(characterClass)
    ? Math.max(0, Math.min(wildShapeUsesMax, Number(raw.wildShapeUses ?? wildDefaults.wildShapeUses) || wildDefaults.wildShapeUses))
    : 0;
  return {
    id: raw.id || uid(),
    name: raw.name || "Combatant",
    initiative: Number(raw.initiative) || 0,
    hp: Number(raw.hp) || 0,
    maxHp: Number(raw.maxHp) || Number(raw.hp) || 0,
    resonance: Number(raw.resonance) || 0,
    level,
    revelationCharges: oracle
      ? Number(raw.revelationCharges ?? rcDefaults.current) || rcDefaults.current
      : 0,
    revelationChargesMax: oracle
      ? Number(raw.revelationChargesMax ?? rcDefaults.max) || rcDefaults.max
      : 0,
    characterClass,
    sacredOath: raw.sacredOath || "",
    druidCircle: raw.druidCircle || "",
    oracleMystery: raw.oracleMystery || "",
    oracleCurse: raw.oracleCurse || "",
    alignment: raw.alignment || "",
    reputation,
    overcastIds,
    burnoutRisk: Boolean(raw.burnoutRisk),
    castSpellTier,
    castSpellSchool,
    castSpellKey,
    wildShapeUses,
    wildShapeUsesMax,
    activeFormId: raw.activeFormId || "",
    wildShapeMinutesLeft: Math.max(0, Number(raw.wildShapeMinutesLeft) || 0),
    primalRecoveryUsed: Boolean(raw.primalRecoveryUsed),
    attunedArchFormIds: Array.isArray(raw.attunedArchFormIds)
      ? raw.attunedArchFormIds.filter(Boolean).slice(0, ARCH_ATTUNEMENT_MAX)
      : [],
    archAttunementSwapUsed: Boolean(raw.archAttunementSwapUsed),
    burnoutCastHint: typeof raw.burnoutCastHint === "string" ? raw.burnoutCastHint : "",
    activeTotemIds: isShamanClass(characterClass)
      ? Array.isArray(raw.activeTotemIds)
        ? raw.activeTotemIds.filter((id): id is string => typeof id === "string").slice(0, maxActiveTotems(level))
        : []
      : [],
    notes: raw.notes || "",
    conditions: raw.conditions ?? "",
    isEnemy: Boolean(raw.isEnemy),
    dexMod: Number(raw.dexMod) || 0,
    secondaryClass: raw.secondaryClass || undefined,
    secondaryLevel: raw.secondaryLevel != null ? Number(raw.secondaryLevel) : undefined,
    classLevels:
      raw.classLevels && typeof raw.classLevels === "object" && !Array.isArray(raw.classLevels)
        ? raw.classLevels
        : undefined,
    challengeRating: typeof raw.challengeRating === "string" ? raw.challengeRating : undefined,
    draftXpAwarded: Boolean(raw.draftXpAwarded),
    draftXpSession: Math.max(0, Number(raw.draftXpSession) || 0),
  };
}

function bumpRevelationCharges(c: Combatant, delta: number): Combatant {
  const max = c.revelationChargesMax || defaultRevelationCharges(c.level).max;
  const next = Math.max(0, Math.min(max, c.revelationCharges + delta));
  return { ...c, revelationCharges: next, revelationChargesMax: max };
}

function subclassBadges(c: Combatant): { key: string; label: string; className: string }[] {
  const out: { key: string; label: string; className: string }[] = [];
  if (c.secondaryClass) {
    out.push({
      key: "multiclass",
      label: `${c.characterClass || "—"} L${c.level} + ${c.secondaryClass} L${c.secondaryLevel ?? 1}`,
      className: "bg-sky-800/80 text-sky-100",
    });
  }
  if (c.sacredOath) {
    out.push({
      key: "oath",
      label: `Oath: ${getOathById(c.sacredOath)?.name ?? c.sacredOath}`,
      className: "bg-amber-800/80 text-amber-100",
    });
  }
  if (c.druidCircle) {
    out.push({
      key: "circle",
      label: `Circle: ${DRUID_CIRCLES.find((circle) => circle.id === c.druidCircle)?.label ?? c.druidCircle}`,
      className: "bg-emerald-800/80 text-emerald-100",
    });
  }
  if (c.oracleMystery) {
    out.push({
      key: "mystery",
      label: `Mystery: ${getMysteryById(c.oracleMystery)?.name ?? c.oracleMystery}`,
      className: "bg-violet-800/80 text-violet-100",
    });
  }
  if (c.oracleCurse) {
    out.push({
      key: "curse",
      label: `Curse: ${getCurseById(c.oracleCurse)?.name ?? c.oracleCurse}`,
      className: "bg-fuchsia-900/80 text-fuchsia-100",
    });
  }
  return out;
}

function adjustHp(c: Combatant, delta: number): Combatant {
  const hp = Math.max(0, Math.min(c.maxHp, c.hp + delta));
  return { ...c, hp };
}

type SessionTrackerProps = {
  handoffTick?: number;
};

export default function SessionTracker({ handoffTick = 0 }: SessionTrackerProps) {
  const [hours, setHours] = useState(0);
  const [tier, setTier] = useState(1);
  const [combatants, setCombatants] = useState<Combatant[]>([]);
  const [turn, setTurn] = useState(0);
  const [round, setRound] = useState(1);
  const [name, setName] = useState("");
  const [partyResonance, setPartyResonance] = useState(6);
  const [monsterQuery, setMonsterQuery] = useState("");
  const [savedChars, setSavedChars] = useState<ReturnType<typeof loadSavedCharacters>>([]);
  const [savedCharsRefreshNote, setSavedCharsRefreshNote] = useState("");
  const [encounterHandoff, setEncounterHandoff] = useState<EncounterHandoff | null>(null);
  const [foeHandoff, setFoeHandoff] = useState<FoeHandoff | null>(null);
  const [itemHandoff, setItemHandoff] = useState<ItemHandoff | null>(null);
  const [spellHandoff, setSpellHandoff] = useState<SpellHandoff | null>(null);
  const [handoffDismissalNote, setHandoffDismissalNote] = useState("");
  const [sceneNotes, setSceneNotes] = useState("");
  const [lastRestSummary, setLastRestSummary] = useState("");
  const [repEditCharId, setRepEditCharId] = useState<string>("");
  const [combatantFilter, setCombatantFilter] = useState<CombatantFilter>("all");
  const [foesExpanded, setFoesExpanded] = useState(false);
  const [spellLookup, setSpellLookup] = useState<{ combatantId: string; query: string } | null>(null);
  const addOrderRef = useRef(new Map<string, number>());
  const addOrderSeq = useRef(0);
  const lastEncounterHandoffAt = useRef(0);
  const lastFoeHandoffAt = useRef(0);
  const lastItemHandoffAt = useRef(0);
  const lastSpellHandoffAt = useRef(0);

  const tiers = encounters.tiers as { tier: number; name: string; boss: string }[];
  const currentTier = tiers.find((t) => t.tier === tier) || tiers[0];
  const hoursLeft = Math.max(0, HORN_AT - hours);
  const hornBlown = hours >= HORN_AT;
  const hornProgress = Math.min(100, (hours / HORN_AT) * 100);
  const monsters = monstersData as MonsterRow[];

  const monsterHits = useMemo(() => {
    const q = monsterQuery.trim().toLowerCase();
    if (q.length < 2) return [];
    return monsters.filter((m) => m.name && m.name.toLowerCase().includes(q)).slice(0, 8);
  }, [monsterQuery, monsters]);

  const applyPendingHandoffs = () => {
    let notesOverride: string | undefined;
    const pending = takeEncounterHandoff(lastEncounterHandoffAt.current);
    if (pending) {
      lastEncounterHandoffAt.current = pending.createdAt;
      setEncounterHandoff(pending);
      setHandoffDismissalNote("");
      setTier(pending.tier);
      notesOverride = pending.brief;
    }

    const foePending = takeFoeHandoff(lastFoeHandoffAt.current);
    if (foePending) {
      lastFoeHandoffAt.current = foePending.createdAt;
      setFoeHandoff(foePending);
      setHandoffDismissalNote("");
      addMonster(foePending);
    }

    const itemPending = takeItemHandoff(lastItemHandoffAt.current);
    if (itemPending) {
      lastItemHandoffAt.current = itemPending.createdAt;
      setItemHandoff(itemPending);
      setHandoffDismissalNote("");
    }

    const spellPending = takeSpellHandoff(lastSpellHandoffAt.current);
    if (spellPending) {
      lastSpellHandoffAt.current = spellPending.createdAt;
      setSpellHandoff(spellPending);
      setHandoffDismissalNote("");
    }

    if (notesOverride !== undefined) {
      setSceneNotes(notesOverride);
    }
    return notesOverride;
  };

  useEffect(() => {
    setSavedChars(loadSavedCharacters());
    let notes = "";
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const data = JSON.parse(raw);
        if (data.hours != null) setHours(data.hours);
        if (data.tier != null) setTier(data.tier);
        if (data.combatants) {
          setCombatants(data.combatants.map((c: Partial<Combatant>) => normalizeCombatant(c)));
        }
        if (data.partyResonance != null) setPartyResonance(data.partyResonance);
        if (data.turn != null) setTurn(data.turn);
        if (data.round != null) setRound(data.round);
        if (typeof data.sceneNotes === "string") notes = data.sceneNotes;
      }
    } catch {
      /* ignore */
    }
    const handoffNotes = applyPendingHandoffs();
    if (handoffNotes === undefined) setSceneNotes(notes);
  }, []);

  useEffect(() => {
    if (handoffTick < 1) return;
    applyPendingHandoffs();
  }, [handoffTick]);

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ hours, tier, combatants, partyResonance, turn, round, sceneNotes })
    );
  }, [hours, tier, combatants, partyResonance, turn, round, sceneNotes]);

  const weaveMaxRp = useMemo(() => sumWeaveCasterMaxRp(combatants), [combatants]);
  const weaveCurrentRp = useMemo(() => sumWeaveCasterCurrentRp(combatants), [combatants]);

  const ordered = useMemo(
    () =>
      [...combatants].sort((a, b) =>
        compareInitiativeOrder(a, b, addOrderRef.current)
      ),
    [combatants]
  );
  const orderedAllies = useMemo(() => ordered.filter((c) => !c.isEnemy), [ordered]);
  const orderedFoes = useMemo(() => ordered.filter((c) => c.isEnemy), [ordered]);
  const crowdedTable = combatants.length >= CROWDED_COMBATANTS;
  const crowdedFoes = orderedFoes.length >= CROWDED_FOES;
  const visibleCombatants = useMemo(() => {
    if (combatantFilter === "allies") return orderedAllies;
    if (combatantFilter === "foes") return orderedFoes;
    if (crowdedFoes && !foesExpanded) return orderedAllies;
    return ordered;
  }, [combatantFilter, crowdedFoes, foesExpanded, ordered, orderedAllies, orderedFoes]);
  const active = ordered.length ? ordered[turn % ordered.length] : null;
  const activeHiddenByFilter = Boolean(
    active && !visibleCombatants.some((c) => c.id === active.id)
  );
  const repEditChar = savedChars.find((c) => c.id === repEditCharId) || null;

  const revealActiveCombatant = () => {
    if (!active) return;
    setCombatantFilter(active.isEnemy ? "foes" : "allies");
    if (active.isEnemy) setFoesExpanded(true);
  };

  const activeHandoffCount = [encounterHandoff, foeHandoff, itemHandoff, spellHandoff].filter(Boolean).length;

  const dismissAllHandoffNotices = () => {
    const count = activeHandoffCount;
    setEncounterHandoff(null);
    setFoeHandoff(null);
    setItemHandoff(null);
    setSpellHandoff(null);
    setHandoffDismissalNote(
      `${count} arrival ${count === 1 ? "notice" : "notices"} dismissed. Scene notes, combatants, tier, horn time, turn, round, and resources are unchanged.`
    );
  };

  const setCharacterReputation = (charId: string, next: Record<string, number>) => {
    const char = savedChars.find((c) => c.id === charId);
    if (!char) return;
    const saved = upsertCharacter({ ...char, reputation: next });
    setSavedChars(loadSavedCharacters());
    setRepEditCharId(saved.id);
  };

  const registerAddOrder = (id: string) => {
    addOrderRef.current.set(id, addOrderSeq.current++);
  };

  const addCombatant = (isEnemy: boolean) => {
    const label =
      name.trim() ||
      (isEnemy
        ? `Foe ${combatants.filter((c) => c.isEnemy).length + 1}`
        : `Ally ${combatants.filter((c) => !c.isEnemy).length + 1}`);
    const maxHp = isEnemy ? 20 + tier * 8 : 30 + tier * 5;
    const id = uid();
    registerAddOrder(id);
    setCombatants((prev) => [
      ...prev,
      normalizeCombatant({
        id,
        name: label,
        initiative: rollInitiative(),
        hp: maxHp,
        maxHp,
        resonance: isEnemy ? 0 : 3,
        level: 1,
        revelationCharges: 0,
        revelationChargesMax: 0,
        characterClass: "",
        sacredOath: "",
        druidCircle: "",
        oracleMystery: "",
        oracleCurse: "",
        alignment: "",
        reputation: {},
        overcastIds: [],
        burnoutRisk: false,
        notes: "",
        conditions: "",
        isEnemy,
        dexMod: 0,
      }),
    ]);
    setName("");
  };

  const addMonster = (m: MonsterRow) => {
    const hp = parseHp(m);
    const id = uid();
    registerAddOrder(id);
    setCombatants((prev) => [
      ...prev,
      normalizeCombatant({
        id,
        name: m.name || "Monster",
        initiative: rollInitiative(),
        hp,
        maxHp: hp,
        resonance: 0,
        level: 1,
        revelationCharges: 0,
        revelationChargesMax: 0,
        characterClass: "",
        sacredOath: "",
        druidCircle: "",
        oracleMystery: "",
        oracleCurse: "",
        notes: `CR ${m.challengeRating || "?"} · ${m.zoneFound || "Unknown zone"}`,
        conditions: "",
        isEnemy: true,
        dexMod: 0,
        challengeRating: m.challengeRating ? String(m.challengeRating) : undefined,
      }),
    ]);
    setMonsterQuery("");
  };

  const addSavedCharacter = (c: SavedChar) => {
    const level = c.level || 1;
    const { hp, maxHp, fromSave } = resolvePcHp(c);
    const dexMod = dexModifierFromAbilities(c.abilities);
    const init = rollInitiative(dexMod);
    const oracle = isOracleClass(c.class);
    const rc = oracle ? defaultRevelationCharges(level) : { current: 0, max: 0 };
    const rpMax = isWeaveCaster(c.class) ? resolveMaxRp(c.class, level, c.reputation, c).maxRp : 0;
    const baseNotes = [
      [c.race, c.class, c.secondaryClass ? `+ ${c.secondaryClass} L${(c as { secondaryLevel?: number }).secondaryLevel ?? 1}` : ""]
        .filter(Boolean)
        .join(" "),
      `L${level}${fromSave ? "" : " · HP stub"}`,
    ]
      .filter(Boolean)
      .join(" ")
      .trim();
    const id = uid();
    registerAddOrder(id);
    setCombatants((prev) => {
      const next = [
        ...prev,
        normalizeCombatant({
          id,
          name: characterDisplayName(c),
          initiative: init,
          hp,
          maxHp,
          resonance: oracle ? 0 : (c.resonancePoints ?? rpMax),
          level,
          revelationCharges: rc.current,
          revelationChargesMax: rc.max,
          characterClass: c.class || "",
          secondaryClass: (c as { secondaryClass?: string }).secondaryClass,
          secondaryLevel: (c as { secondaryLevel?: number }).secondaryLevel,
          classLevels: (c as { classLevels?: Record<string, number> }).classLevels,
          sacredOath: c.sacredOath || "",
          druidCircle: c.druidCircle || "",
          oracleMystery: c.oracleMystery || "",
          oracleCurse: c.oracleCurse || "",
          alignment: c.alignment || "",
          reputation: c.reputation || {},
          overcastIds: [],
          burnoutRisk: false,
          notes: baseNotes,
          conditions: "",
          isEnemy: false,
          dexMod,
        }),
      ];
      setPartyResonance(sumWeaveCasterMaxRp(next));
      return next;
    });
  };

  const update = (id: string, patch: Partial<Combatant>) => {
    setCombatants((prev) => prev.map((c) => (c.id === id ? { ...c, ...patch } : c)));
  };

  const bumpHp = (id: string, delta: number) => {
    setCombatants((prev) => prev.map((c) => (c.id === id ? adjustHp(c, delta) : c)));
  };

  const bumpRc = (id: string, delta: number) => {
    setCombatants((prev) => prev.map((c) => (c.id === id ? bumpRevelationCharges(c, delta) : c)));
  };

  const toggleCombatantCondition = (id: string, condition: string) => {
    setCombatants((prev) =>
      prev.map((c) =>
        c.id === id ? { ...c, conditions: toggleCondition(c.conditions, condition) } : c
      )
    );
  };

  const retuneCombatant = (id: string, savedChar?: SavedChar | null) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || isOracleClass(c.characterClass)) return c;
        const rpMax = resolveCombatantMaxRp(c);
        const castingMod = savedChar ? castingModFromChar(savedChar) : 0;
        const gain = retuneAmount(rpMax.maxRp, castingMod, c.reputation);
        const next = Math.min(rpMax.maxRp, c.resonance + gain);
        return {
          ...c,
          resonance: next,
          burnoutRisk: isBurnoutRisk(next, rpMax.maxRp),
        };
      })
    );
  };

  const fullRestoreCombatant = (id: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || isOracleClass(c.characterClass)) return c;
        const rpMax = resolveCombatantMaxRp(c);
        const next = fullRestore(rpMax.maxRp);
        return {
          ...c,
          resonance: next,
          burnoutRisk: false,
          burnoutCastHint: "",
          overcastIds: [],
          castSpellTier: 0,
          castSpellSchool: "",
          castSpellKey: "",
        };
      })
    );
  };

  const toggleOvercast = (id: string, overcastId: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id) return c;
        const has = c.overcastIds.includes(overcastId);
        const overcastIds = has
          ? c.overcastIds.filter((oid) => oid !== overcastId)
          : [...c.overcastIds, overcastId];
        return { ...c, overcastIds };
      })
    );
  };

  const applyOvercastSpend = (id: string, baseCost?: number) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy) return c;
        const rpMax = resolveCombatantMaxRp(c);
        const base = baseCost ?? overcastBaseCost(c);
        const spend = totalCastCost(base, c.overcastIds);
        const castTier = c.castSpellTier;
        const next = Math.max(0, c.resonance - spend);
        const hint = overcastBurnoutHintAfterCast(
          next,
          rpMax.maxRp,
          castTier,
          c.level,
          c.characterClass
        );
        return {
          ...c,
          resonance: next,
          burnoutRisk: isBurnoutRisk(next, rpMax.maxRp),
          burnoutCastHint: hint?.summary ?? "",
          overcastIds: [],
          castSpellTier: 0,
          castSpellSchool: "",
          castSpellKey: "",
        };
      })
    );
  };

  const spendWildShape = (id: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || !isDruidClass(c.characterClass)) return c;
        if (c.wildShapeUses <= 0 || !c.activeFormId) return c;
        return {
          ...c,
          wildShapeUses: c.wildShapeUses - 1,
          wildShapeMinutesLeft: wildShapeDurationMinutes(),
        };
      })
    );
  };

  const selectWildShapeForm = (id: string, formId: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || !isDruidClass(c.characterClass)) return c;
        const clearing = !formId || c.activeFormId === formId;
        if (clearing) {
          return { ...c, activeFormId: "", wildShapeMinutesLeft: 0 };
        }
        const fromForm = c.activeFormId;
        const freeSwap =
          hasArchFormAttunement(c.level) &&
          !c.archAttunementSwapUsed &&
          c.wildShapeMinutesLeft > 0 &&
          isFreeArchAttunementSwap(fromForm, formId, c.attunedArchFormIds);
        return {
          ...c,
          activeFormId: formId,
          archAttunementSwapUsed: freeSwap ? true : c.archAttunementSwapUsed,
          wildShapeMinutesLeft: c.wildShapeMinutesLeft > 0 ? c.wildShapeMinutesLeft : 0,
        };
      })
    );
  };

  const toggleArchFormAttunement = (id: string, formId: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || !isDruidClass(c.characterClass)) return c;
        if (!hasArchFormAttunement(c.level)) return c;
        const attuned = [...c.attunedArchFormIds];
        const idx = attuned.indexOf(formId);
        if (idx >= 0) {
          attuned.splice(idx, 1);
        } else if (attuned.length < ARCH_ATTUNEMENT_MAX) {
          attuned.push(formId);
        }
        return { ...c, attunedArchFormIds: attuned };
      })
    );
  };

  const revertWildShape = (id: string) => {
    update(id, { activeFormId: "", wildShapeMinutesLeft: 0 });
  };

  const toggleTotem = (id: string, totemId: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || !isShamanClass(c.characterClass)) return c;
        const active = [...c.activeTotemIds];
        const index = active.indexOf(totemId);
        if (index >= 0) {
          active.splice(index, 1);
        } else if (active.length < maxActiveTotems(c.level)) {
          active.push(totemId);
        }
        return { ...c, activeTotemIds: active };
      })
    );
  };

  const recallTotems = (id: string) => update(id, { activeTotemIds: [] });

  const tickWildShapeMinutes = (id: string, delta: number) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || !isDruidClass(c.characterClass)) return c;
        const next = Math.max(0, c.wildShapeMinutesLeft + delta);
        return {
          ...c,
          wildShapeMinutesLeft: next,
          activeFormId: next > 0 ? c.activeFormId : "",
        };
      })
    );
  };

  const applyPrimalRecovery = (id: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id || c.isEnemy || !isDruidClass(c.characterClass)) return c;
        if (!hasPrimalRecovery(c.level) || c.primalRecoveryUsed || c.wildShapeUses <= 0) return c;
        const rpMax = resolveCombatantMaxRp(c);
        const gain = primalRecoveryRpGain(c.level);
        const next = Math.min(rpMax.maxRp, c.resonance + gain);
        return {
          ...c,
          wildShapeUses: c.wildShapeUses - 1,
          resonance: next,
          burnoutRisk: isBurnoutRisk(next, rpMax.maxRp),
          primalRecoveryUsed: true,
        };
      })
    );
  };

  const restoreWildShapeUses = (c: Combatant): Combatant => {
    if (!isDruidClass(c.characterClass)) return c;
    const max = shapeshiftUsesAtLevel(c.level);
    return {
      ...c,
      wildShapeUses: max,
      wildShapeUsesMax: max,
      activeFormId: "",
      wildShapeMinutesLeft: 0,
      primalRecoveryUsed: false,
      archAttunementSwapUsed: false,
    };
  };

  const setCombatantResonance = (id: string, value: number) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id) return c;
        const rpMax = resolveCombatantMaxRp(c);
        const next = Math.max(0, value);
        return { ...c, resonance: next, burnoutRisk: isBurnoutRisk(next, rpMax.maxRp) };
      })
    );
  };

  const remove = (id: string) => setCombatants((prev) => prev.filter((c) => c.id !== id));

  /** Draft XP stub — logs to Scene notes and per-ally session tally; does not write character saves. */
  const awardDraftXpForFoe = (foeId: string) => {
    const foe = combatants.find((c) => c.id === foeId);
    if (!foe?.isEnemy || foe.draftXpAwarded) return;
    const cr = foe.challengeRating ?? parseCrFromNotes(foe.notes);
    const participants = combatants.filter((c) => !c.isEnemy && c.hp > 0);
    const totalXp = draftXpForCr(cr);
    const split = splitPartyXp(totalXp, participants.length);
    const line = formatDraftXpAwardLine({
      foeName: foe.name,
      cr,
      participantCount: participants.length,
    });
    setSceneNotes((prev) => (prev.trim() ? `${prev.trim()}\n${line}` : line));
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id === foeId) return { ...c, draftXpAwarded: true };
        if (!c.isEnemy && c.hp > 0 && split.perMember > 0) {
          return { ...c, draftXpSession: (c.draftXpSession || 0) + split.perMember };
        }
        return c;
      })
    );
  };

  const clearFoes = () => {
    const allyCount = combatants.filter((c) => !c.isEnemy).length;
    setCombatants((prev) => prev.filter((c) => !c.isEnemy));
    setTurn((t) => (allyCount ? t % allyCount : 0));
    setFoesExpanded(false);
    if (combatantFilter === "foes") setCombatantFilter("all");
  };

  const nextTurn = () => {
    if (!ordered.length) return;
    const next = turn + 1;
    if (next % ordered.length === 0) setRound((r) => r + 1);
    setTurn(next);
  };

  const sortInitiative = () => {
    setCombatants((prev) =>
      [...prev].sort((a, b) => compareInitiativeOrder(a, b, addOrderRef.current))
    );
    setTurn(0);
  };

  const rollAllInitiative = () => {
    setCombatants((prev) =>
      [...prev]
        .map((c) => ({ ...c, initiative: rollInitiative(c.dexMod ?? 0) }))
        .sort((a, b) => compareInitiativeOrder(a, b, addOrderRef.current))
    );
    setTurn(0);
    setRound(1);
  };

  const runShortRest = () => {
    const allyCount = combatants.filter((c) => !c.isEnemy).length;
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.isEnemy) return c;
        if (isOracleClass(c.characterClass)) {
          return { ...c, ...applyShortRest(c), burnoutCastHint: "" };
        }
        let next = { ...c, burnoutCastHint: "" };
        if (isDruidClass(c.characterClass)) {
          next = { ...next, primalRecoveryUsed: false, archAttunementSwapUsed: false };
        }
        if (isWeaveCaster(c.characterClass)) {
          const rpMax = resolveCombatantMaxRp(next);
          const gain = retuneAmount(rpMax.maxRp, 0, next.reputation);
          const res = Math.min(rpMax.maxRp, next.resonance + gain);
          next = { ...next, resonance: res, burnoutRisk: isBurnoutRisk(res, rpMax.maxRp) };
        }
        return next;
      })
    );
    setLastRestSummary(
      `Short rest applied to ${allyCount} ${allyCount === 1 ? "ally" : "allies"}. Oracle RC and Weave RP recover by their existing tracks; Druid Primal Recovery and free arch swap reset.`
    );
  };

  const runLongRest = () => {
    const allyCount = combatants.filter((c) => !c.isEnemy).length;
    setHours((h) => h + 8);
    setCombatants((prev) => {
      const next = prev.map((c) => {
        if (c.isEnemy) return c;
        if (isOracleClass(c.characterClass)) {
          return { ...c, ...applyLongRest(c), burnoutCastHint: "" };
        }
        let next = { ...c, burnoutCastHint: "" };
        if (isDruidClass(c.characterClass)) next = restoreWildShapeUses(next);
        if (isShamanClass(c.characterClass)) next = { ...next, activeTotemIds: [] };
        if (isWeaveCaster(c.characterClass)) {
          const rpMax = resolveCombatantMaxRp(next);
          next = {
            ...next,
            resonance: fullRestore(rpMax.maxRp),
            burnoutRisk: false,
            overcastIds: [],
            castSpellTier: 0,
            castSpellSchool: "",
            castSpellKey: "",
          };
        }
        return next;
      });
      setPartyResonance(sumWeaveCasterMaxRp(next) || partyResonance);
      return next;
    });
    setLastRestSummary(
      `Long rest applied to ${allyCount} ${allyCount === 1 ? "ally" : "allies"}. The horn advanced 8h; Oracle RC, Weave RP, Druid uses, and Shaman totems reset.`
    );
  };

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-6xl mx-auto">
      <div className="text-center space-y-2">
        <h1 className="text-2xl md:text-3xl font-bold text-amber-400">Expedition Session</h1>
        <p className="text-amber-100/70 text-sm max-w-2xl mx-auto">
          Horn clock, party Resonance (Weave), Revelation Charges (Oracle), and initiative — pull saved characters and bestiary foes onto the table.
        </p>
        <p className="text-[11px] text-amber-200/55 max-w-2xl mx-auto leading-snug">
          Opening campaigns use <span className="text-amber-100/80 font-medium">milestone advancement</span> (official).
          Session CR→XP is <span className="text-amber-100/80 font-medium">optional / non-canon</span>.
          Burnout effects and class ceiling caps are <span className="text-amber-100/80 font-medium">GM fiat</span> until final tables ship.
          Non-core RP pools marked <span className="text-amber-100/80 font-medium">*</span> are draft estimates.
        </p>
      </div>

      <Card
        className={`${hornBlown ? "bg-red-950/70 border-red-400 shadow-lg shadow-red-900/40 animate-pulse" : "bg-red-950/30 border-red-500/40"}`}
      >
        <CardContent className="py-4 space-y-3">
          <div className="flex flex-wrap gap-4 items-start justify-between">
            <div className="flex gap-3 items-start min-w-0 flex-1">
              <AlertTriangle className={`w-5 h-5 mt-0.5 shrink-0 ${hornBlown ? "text-red-200" : "text-red-400"}`} />
              <div className="min-w-0">
                <div className={`text-sm font-medium ${hornBlown ? "text-red-50" : "text-red-100"}`}>
                  {hornBlown
                    ? "HORN HAS SOUNDED — begin ascent or risk 10 years below"
                    : encounters.hornRule}
                </div>
                <div className="text-xs text-red-200/70 mt-1 flex items-center gap-2 flex-wrap">
                  <Timer className="w-3 h-3 shrink-0" />
                  <span>{hoursLeft}h until horn (day 50 PoNR)</span>
                  <span>·</span>
                  <span>elapsed {hours} / {HORN_AT}h · Opening 2400h</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <Button size="sm" variant="outline" onClick={() => setHours((h) => Math.max(0, h - 1))}>−1h</Button>
              <Input
                type="number"
                className="w-20 bg-black/40 border-red-500/40 text-white"
                value={hours}
                onChange={(e) => setHours(Math.max(0, Number(e.target.value) || 0))}
              />
              <Button size="sm" variant="outline" onClick={() => setHours((h) => h + 1)}>+1h</Button>
              <Button size="sm" variant="outline" onClick={() => setHours((h) => h + 8)}>Advance +8h</Button>
            </div>
          </div>
          <div className="space-y-1">
            <div className="flex justify-between text-[10px] text-red-200/60 uppercase tracking-wide">
              <span>Horn countdown</span>
              <span>{Math.round(hornProgress)}%</span>
            </div>
            <Progress value={hornProgress} className="h-2 bg-red-950" />
          </div>
        </CardContent>
      </Card>

      {activeHandoffCount > 1 && (
        <div className="flex flex-wrap items-center justify-between gap-2 rounded-md border border-slate-700/70 bg-slate-900/70 px-3 py-2">
          <p className="text-xs text-slate-200/75">
            {activeHandoffCount} arrival notices are open. Dismissing them does not change scene notes, combatants, or resources.
          </p>
          <Button
            size="sm"
            variant="ghost"
            className="text-slate-200 hover:text-white"
            onClick={dismissAllHandoffNotices}
          >
            Dismiss all notices
          </Button>
        </div>
      )}
      {handoffDismissalNote && (
        <p className="text-xs text-slate-200/75" role="status">
          {handoffDismissalNote}
        </p>
      )}

      {encounterHandoff && (
        <Card className="bg-amber-950/40 border-amber-500/50">
          <CardContent className="py-3 space-y-2">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div className="text-sm text-amber-100">
                <span className="font-medium text-amber-300">Scene loaded</span>
                {" "}from {encounterHandoff.source} — Tier {encounterHandoff.tier}: {encounterHandoff.tierName}
              </div>
              <Button size="sm" variant="ghost" onClick={() => setEncounterHandoff(null)}>
                Dismiss
              </Button>
            </div>
            <pre className="text-xs text-amber-50/85 whitespace-pre-wrap">{encounterHandoff.brief}</pre>
          </CardContent>
        </Card>
      )}

      {foeHandoff && (
        <Card className="bg-red-950/40 border-red-500/50">
          <CardContent className="py-3">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div className="text-sm text-red-100 space-y-1">
                <p>
                  <span className="font-medium text-red-300">Foe added from Bestiary</span>
                  {" "}— {foeHandoff.name} (HP {parseHp(foeHandoff)})
                </p>
                <p className="text-xs text-red-100/75">
                  Added as one editable foe; adjust initiative, HP, and conditions in Combatants before the scene.
                </p>
              </div>
              <Button size="sm" variant="ghost" onClick={() => setFoeHandoff(null)}>
                Dismiss
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {itemHandoff && (
        <Card className="bg-teal-950/40 border-teal-500/50">
          <CardContent className="py-3 space-y-2">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div className="text-sm text-teal-100 space-y-1">
                <p>
                  <span className="font-medium text-teal-300">Item preview from Items</span>
                  {" "}— {itemHandoff.name} · {itemHandoff.rarity} · T{itemHandoff.tier}
                </p>
                <p className="text-xs text-teal-100/75">
                  {itemHandoff.category} · {itemHandoff.source.replace("items-", "")}. Reference only: the GM resolves
                  acquisition, use, crafting, and any inventory change. Add relevant details to Scene notes manually.
                </p>
              </div>
              <Button size="sm" variant="ghost" onClick={() => setItemHandoff(null)}>
                Dismiss
              </Button>
            </div>
            <p className="text-xs text-teal-50/85">{itemHandoff.description}</p>
          </CardContent>
        </Card>
      )}

      {spellHandoff && (
        <Card className="bg-indigo-950/40 border-indigo-500/50">
          <CardContent className="py-3">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div className="text-sm text-indigo-100 space-y-1">
                <p>
                  <span className="font-medium text-indigo-300">Cast preview from Spells</span>
                  {" "}— {spellHandoff.name} · {spellHandoff.school} · T{spellHandoff.level}
                </p>
                <p className="text-xs text-indigo-100/75">
                  {spellHandoff.castingTime} · {spellHandoff.range} · {spellHandoff.duration}. Select a caster and use
                  that row&apos;s spell lookup / Overcast controls if applicable; this preview does not spend RP or resolve a cast.
                </p>
              </div>
              <Button size="sm" variant="ghost" onClick={() => setSpellHandoff(null)}>
                Dismiss
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <Card className="bg-slate-900/70 border-sky-600/30">
        <CardHeader className="pb-2">
          <CardTitle className="text-sky-300 text-base">Scene notes</CardTitle>
        </CardHeader>
        <CardContent>
          <textarea
            value={sceneNotes}
            onChange={(e) => setSceneNotes(e.target.value)}
            placeholder="Encounter brief, loot, fiction beats…"
            className="w-full min-h-[88px] rounded-md bg-slate-950 border border-sky-700/40 text-white text-sm p-3"
          />
        </CardContent>
      </Card>

      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        <Card className="bg-slate-900/70 border-amber-600/30">
          <CardHeader className="pb-2"><CardTitle className="text-amber-300 text-base">Current Tier</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-1">
              {tiers.map((t) => (
                <Button key={t.tier} size="sm" variant={tier === t.tier ? "default" : "outline"}
                  className={tier === t.tier ? "bg-amber-600" : ""} onClick={() => setTier(t.tier)}>T{t.tier}</Button>
              ))}
            </div>
            <div className="text-sm text-amber-50/80">
              <div className="font-medium text-amber-200">{currentTier.name}</div>
              <div className="text-xs mt-1">Gate: {currentTier.boss}</div>
              <div className="text-[10px] text-amber-200/50 mt-1">
                Stub HP: {gateBossStubHp(tier)} (tier formula — pull bestiary when ready)
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-purple-600/40">
          <CardHeader className="pb-2">
            <CardTitle className="text-purple-300 text-base flex items-center gap-2"><Sparkles className="w-4 h-4" /> Party Resonance</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-4xl font-bold text-purple-200">{partyResonance}</div>
            <p className="text-[10px] text-purple-200/55 leading-snug">
              Director default: pool cap = sum of living Weave casters&apos; max RP ({weaveMaxRp}).
              Per-character RP is v1 canon — living casters hold {weaveCurrentRp} RP total.
            </p>
            <div className="flex gap-2 flex-wrap">
              <Button size="sm" variant="outline" onClick={() => setPartyResonance((r) => Math.max(0, r - 1))}>Spend 1 RP</Button>
              <Button size="sm" variant="outline" onClick={() => setPartyResonance((r) => Math.min(24, r + 1))}>Gain 1 RP</Button>
              <Button size="sm" variant="outline" onClick={() => setPartyResonance(weaveMaxRp)} disabled={!weaveMaxRp}>
                Sync to max ({weaveMaxRp})
              </Button>
            </div>
            <div className="flex gap-2 flex-wrap pt-1 border-t border-purple-700/30">
              <Button size="sm" variant="outline" onClick={runShortRest}>Short rest</Button>
              <Button size="sm" variant="outline" onClick={runLongRest}>Long rest (+8h)</Button>
            </div>
            {lastRestSummary && (
              <p className="text-[10px] text-emerald-200/75 leading-snug" role="status">
                {lastRestSummary}
              </p>
            )}
            <p className="text-[10px] text-purple-200/45">
              Retune (short): ¼ max RP · Full (long): restore Resonance · Oracle RC +1 / full · +8h horn.
            </p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-amber-600/30 sm:col-span-2 md:col-span-1">
          <CardHeader className="pb-2"><CardTitle className="text-amber-300 text-base">Round / Turn</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm text-amber-50/80">
              Round <span className="text-white font-bold">{round}</span>
              {active && (
                <span> · Active: <span className={active.isEnemy ? "text-red-300" : "text-emerald-300"}>{active.name}</span></span>
              )}
            </div>
            <div className="flex gap-2 flex-wrap">
              <Button size="sm" className="bg-amber-600 hover:bg-amber-500" onClick={nextTurn} disabled={!ordered.length}>Next turn</Button>
              <Button size="sm" variant="outline" onClick={sortInitiative} disabled={!ordered.length}
                title="Reorder combatants by initiative (ties: Dex, then add-order)">
                <ArrowDownUp className="w-3 h-3 mr-1" /> Sort initiative
              </Button>
              <Button size="sm" variant="outline" onClick={rollAllInitiative} disabled={!ordered.length}
                title="Roll d20 + Dex for all combatants, sort, reset to round 1">
                Roll all
              </Button>
              <Button size="sm" variant="outline" onClick={() => { setTurn(0); setRound(1); }}>
                <RotateCcw className="w-3 h-3 mr-1" /> Reset
              </Button>
            </div>
            <p className="text-[10px] text-amber-200/45 leading-snug">
              Initiative ties: higher Dex, then player add-order (allies before foes). Sort after manual Init edits; Roll all at combat start.
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <Card className="bg-slate-900/70 border-emerald-600/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-emerald-300 text-base flex flex-wrap items-center justify-between gap-2">
              <span>Add saved character</span>
              <Badge variant="outline" className="text-[10px] border-emerald-600/40 text-emerald-200/80">
                {savedChars.length} available
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-[10px] text-emerald-100/60 leading-snug">
              Session reads characters saved in this browser. After <span className="text-emerald-200">SAVE</span> in Characters, return here and refresh;
              adding a hero copies it into this encounter, so later character edits stay in Characters.
            </p>
            {savedChars.length === 0 ? (
              <p className="text-xs text-amber-100/50">
                No saved characters found. Go to <span className="text-amber-200">CHARACTERS</span> and
                <span className="text-amber-200"> SAVE</span> a build, then return here and refresh this list.
                Session has no separate JSON-import action.
              </p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {savedChars.map((c) => (
                  <Button
                    key={c.id}
                    size="sm"
                    variant="outline"
                    title={`Add ${savedCharacterLabel(c)} to this encounter`}
                    onClick={() => addSavedCharacter(c)}
                  >
                    <Plus className="w-3 h-3 mr-1" />{characterDisplayName(c)} <span className="text-emerald-200/60">· {c.class || "Adventurer"} L{c.level || 1}</span>
                  </Button>
                ))}
              </div>
            )}
            <div className="flex flex-wrap items-center gap-2">
              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  const refreshed = loadSavedCharacters();
                  setSavedChars(refreshed);
                  setSavedCharsRefreshNote(
                    refreshed.length
                      ? `Saved list refreshed — ${refreshed.length} character${refreshed.length === 1 ? "" : "s"} available.`
                      : "Saved list refreshed — no characters found yet."
                  );
                }}
              >
                <RefreshCw className="w-3 h-3 mr-1" />Refresh saved list
              </Button>
              {savedCharsRefreshNote && (
                <span className="text-[10px] text-emerald-200/70" role="status">{savedCharsRefreshNote}</span>
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-teal-600/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-teal-300 text-base">Reputation (play adjust)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {savedChars.length === 0 ? (
              <p className="text-xs text-amber-100/50">Save a character with faction standing first.</p>
            ) : (
              <>
                <div className="flex flex-wrap gap-2">
                  {savedChars.map((c) => (
                    <Button
                      key={c.id}
                      size="sm"
                      variant={repEditCharId === c.id ? "default" : "outline"}
                      className={repEditCharId === c.id ? "bg-teal-700 hover:bg-teal-600" : ""}
                      onClick={() => setRepEditCharId(c.id || "")}
                    >
                      {characterDisplayName(c)}
                    </Button>
                  ))}
                </div>
                {repEditChar ? (
                  <ReputationPanel
                    scores={repEditChar.reputation || {}}
                    onChange={(next) => setCharacterReputation(repEditChar.id || "", next)}
                    mode="compact"
                  />
                ) : (
                  <p className="text-xs text-amber-100/50">Pick a hero to adjust faction standing (+/−).</p>
                )}
                <p className="text-[10px] text-teal-200/45">
                  Changes save to the character in localStorage. Resonance max RP and spell costs update from Arcane Guilds and class tracks.
                </p>
              </>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-red-600/30">
          <CardHeader className="pb-2"><CardTitle className="text-red-300 text-base">Add from bestiary</CardTitle></CardHeader>
          <CardContent className="space-y-2">
            <Input value={monsterQuery} onChange={(e) => setMonsterQuery(e.target.value)}
              placeholder="Search monsters…" className="bg-slate-950 border-red-700/40 text-white" />
            <div className="flex flex-wrap gap-2">
              {monsterHits.map((m) => (
                <Button key={m.name} size="sm" variant="outline" onClick={() => addMonster(m)}>
                  {m.name} (HP {parseHp(m)})
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2 pb-2">
          <CardTitle className="text-amber-300">
            Combatants
            {ordered.length > 0 && visibleCombatants.length !== ordered.length && (
              <span className="ml-2 text-xs font-normal text-amber-200/60">
                {visibleCombatants.length} of {ordered.length} shown
              </span>
            )}
          </CardTitle>
          {crowdedTable && (
            <div className="flex gap-1">
              {(["all", "allies", "foes"] as const).map((filter) => (
                <Button
                  key={filter}
                  size="sm"
                  variant={combatantFilter === filter ? "default" : "outline"}
                  className={combatantFilter === filter ? "bg-amber-700 h-7 text-xs" : "h-7 text-xs"}
                  onClick={() => {
                    setCombatantFilter(filter);
                    if (filter === "foes") setFoesExpanded(true);
                  }}
                >
                  {filter === "all" ? "All" : filter === "allies" ? "Allies" : "Foes"}
                </Button>
              ))}
            </div>
          )}
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name (optional)"
              className="max-w-xs bg-slate-950 border-amber-600/30 text-white" />
            <Button onClick={() => addCombatant(false)} className="bg-emerald-700 hover:bg-emerald-600">
              <Plus className="w-4 h-4 mr-1" /> Ally
            </Button>
            <Button onClick={() => addCombatant(true)} className="bg-red-800 hover:bg-red-700">
              <Plus className="w-4 h-4 mr-1" /> Enemy
            </Button>
            <Button
              variant="outline"
              onClick={clearFoes}
              disabled={!orderedFoes.length}
              title="Remove all foes from the table; allies stay"
              className="border-red-700/50 text-red-200/90 hover:bg-red-950/40"
            >
              <Trash2 className="w-4 h-4 mr-1" /> Clear foes
            </Button>
            <Button variant="outline" onClick={() => {
              const bossHp = gateBossStubHp(tier);
              const id = uid();
              registerAddOrder(id);
              setCombatants((prev) => [...prev, normalizeCombatant({
                id,
                name: currentTier.boss,
                initiative: rollInitiative(2),
                hp: bossHp,
                maxHp: bossHp,
                resonance: 0,
                revelationCharges: 0,
                revelationChargesMax: 0,
                characterClass: "",
                sacredOath: "",
                druidCircle: "",
                oracleMystery: "",
                oracleCurse: "",
                alignment: "",
                reputation: {},
                overcastIds: [],
                burnoutRisk: false,
                notes: `Gate Warden · T${tier} stub HP (${bossHp}) — bestiary when ready`,
                conditions: "",
                isEnemy: true,
                dexMod: 2,
              })]);
            }} aria-label={`Add gate boss ${currentTier.boss} with ${gateBossStubHp(tier)} stub HP`}>
              Add Gate Boss: {currentTier.boss} ({gateBossStubHp(tier)} HP)
            </Button>
          </div>

          {ordered.length === 0 ? (
            <div className="rounded-md border border-dashed border-amber-700/40 bg-black/15 px-3 py-3 text-sm text-amber-100/65">
              <p className="font-medium text-amber-100/80">No combatants on the table yet.</p>
              <p className="mt-1 text-xs leading-snug">
                Add a saved character above, search the Bestiary, or use the Ally / Enemy controls. Scene notes, tier, horn time,
                and arrival notices stay in place while you build the table.
              </p>
            </div>
          ) : (
            <div className="space-y-3 overflow-x-auto">
              {activeHiddenByFilter && active && (
                <div className="flex flex-wrap items-center gap-2 px-1">
                  <p className="text-xs text-amber-300/70 italic">
                    Active turn: <span className="text-amber-200">{active.name}</span> — hidden by filter.
                  </p>
                  <Button
                    size="sm"
                    variant="outline"
                    className="h-6 border-amber-600/50 px-2 text-[10px] text-amber-200"
                    onClick={revealActiveCombatant}
                  >
                    Show active turn
                  </Button>
                </div>
              )}
              {visibleCombatants.length === 0 && (
                <div className="flex flex-wrap items-center gap-2 rounded-md border border-dashed border-slate-700/70 bg-black/15 px-3 py-2">
                  <p className="text-xs text-slate-200/75">
                    No combatants match this view. The table and its current turn stay unchanged.
                  </p>
                  <Button
                    size="sm"
                    variant="outline"
                    className="h-6 border-slate-600 px-2 text-[10px] text-slate-200"
                    onClick={() => {
                      setCombatantFilter("all");
                      setFoesExpanded(true);
                    }}
                  >
                    Show all combatants
                  </Button>
                </div>
              )}
              <div className="hidden md:grid md:grid-cols-12 gap-2 text-[10px] uppercase text-amber-200/50 px-2">
                <div className="col-span-3">Name</div>
                <div className="col-span-1">Init</div>
                <div className="col-span-2">HP</div>
                <div className="col-span-1" title="RP for Weave casters; RC for Oracle">Pool</div>
                <div className="col-span-2">Conditions</div>
                <div className="col-span-2">Notes</div>
                <div className="col-span-1 text-right">Actions</div>
              </div>
              {visibleCombatants.map((c) => {
                const isActive = active?.id === c.id;
                const badges = subclassBadges(c);
                const isDown = !c.isEnemy && c.hp <= 0;
                const oracle = isOracleClass(c.characterClass);
                return (
                  <div key={c.id} className={`border rounded p-2 space-y-2 ${
                    isActive ? "border-amber-400 bg-amber-950/40" : isDown ? "border-red-800/60 bg-red-950/20" : "border-slate-700 bg-black/30"
                  }`}>
                    <div className="grid md:grid-cols-12 gap-2 items-center">
                      <div className="md:col-span-3 flex items-center gap-2 min-w-0">
                        <Badge className={c.isEnemy ? "bg-red-700 shrink-0" : "bg-emerald-700 shrink-0"}>{c.isEnemy ? "Foe" : "Ally"}</Badge>
                        {isDown && <Badge className="bg-red-900 shrink-0">Down</Badge>}
                        <Input value={c.name} onChange={(e) => update(c.id, { name: e.target.value })}
                          className="bg-transparent border-slate-600 text-white h-8 min-w-0" />
                      </div>
                      <div className="md:col-span-1 flex items-center gap-1 text-xs text-amber-100/70">
                        <Input type="number" value={c.initiative}
                          onChange={(e) => update(c.id, { initiative: Number(e.target.value) || 0 })}
                          className="w-full h-8 bg-slate-950 border-slate-600 text-white" />
                      </div>
                      <div className="md:col-span-2 flex items-center gap-1 flex-wrap">
                        <Input type="number" value={c.hp}
                          onChange={(e) => update(c.id, { hp: Number(e.target.value) || 0 })}
                          className="w-14 h-8 bg-slate-950 border-slate-600 text-white" />
                        <span className="text-amber-100/50">/</span>
                        <Input type="number" value={c.maxHp}
                          onChange={(e) => update(c.id, { maxHp: Number(e.target.value) || 0 })}
                          className="w-14 h-8 bg-slate-950 border-slate-600 text-white" />
                        <div className="flex gap-0.5">
                          <Button size="sm" variant="ghost" className="h-7 px-1.5 text-red-400" title="−5 HP" onClick={() => bumpHp(c.id, -5)}>
                            <Swords className="w-3 h-3" />5
                          </Button>
                          <Button size="sm" variant="ghost" className="h-7 px-1.5 text-red-300" onClick={() => bumpHp(c.id, -1)}>−1</Button>
                          <Button size="sm" variant="ghost" className="h-7 px-1.5 text-emerald-300" onClick={() => bumpHp(c.id, 1)}>+1</Button>
                          <Button size="sm" variant="ghost" className="h-7 px-1.5 text-emerald-400" title="+5 HP" onClick={() => bumpHp(c.id, 5)}>
                            <Heart className="w-3 h-3" />5
                          </Button>
                        </div>
                      </div>
                      <div className="md:col-span-1">
                        {oracle && !c.isEnemy ? (
                          <div className="flex items-center gap-0.5 flex-wrap">
                            <span className="text-[10px] text-violet-300 font-medium shrink-0">RC</span>
                            <Input type="number" value={c.revelationCharges}
                              onChange={(e) => update(c.id, { revelationCharges: Number(e.target.value) || 0 })}
                              className="w-10 h-8 bg-slate-950 border-violet-700/50 text-white px-1" />
                            <span className="text-amber-100/40 text-xs">/</span>
                            <Input type="number" value={c.revelationChargesMax}
                              onChange={(e) => update(c.id, { revelationChargesMax: Number(e.target.value) || 0 })}
                              className="w-10 h-8 bg-slate-950 border-violet-700/50 text-white px-1" />
                            <Button size="sm" variant="ghost" className="h-7 px-1 text-violet-300" title="Spend 1 Revelation Charge"
                              onClick={() => bumpRc(c.id, -1)}>−</Button>
                            <Button size="sm" variant="ghost" className="h-7 px-1 text-violet-200" title="Regain 1 (Prophecy Trigger / rest)"
                              onClick={() => bumpRc(c.id, 1)}>+</Button>
                          </div>
                        ) : c.isEnemy ? (
                          <span className="text-slate-500 text-xs">—</span>
                        ) : (
                          <div className="space-y-1">
                            <div className="flex items-center gap-0.5 flex-wrap">
                              <span className="text-[10px] text-purple-300 font-medium shrink-0">RP</span>
                              <Input type="number" value={c.resonance}
                                onChange={(e) => setCombatantResonance(c.id, Number(e.target.value) || 0)}
                                className="w-14 h-8 bg-slate-950 border-slate-600 text-white" />
                              {c.characterClass && (() => {
                                const rpMax = resolveCombatantMaxRp(c);
                                if (rpMax.maxRp <= 0) return null;
                                return (
                                  <button
                                    type="button"
                                    title={formatMaxRpTooltip(
                                      rpMax,
                                      c.secondaryClass
                                        ? `${c.characterClass} L${c.level} + ${c.secondaryClass} L${c.secondaryLevel ?? 1}`
                                        : `${c.characterClass} L${c.level}`
                                    )}
                                    onClick={() => fullRestoreCombatant(c.id)}
                                    className="text-[10px] text-purple-300/70 hover:text-purple-200 underline decoration-dotted shrink-0"
                                  >
                                    /{rpMax.maxRp}{rpMax.draft ? "*" : ""}
                                  </button>
                                );
                              })()}
                              {c.burnoutRisk && (
                                <Badge
                                  className="text-[9px] bg-orange-900/80 text-orange-100 shrink-0"
                                  title={BURNOUT_EFFECT_STUB.summary}
                                >
                                  {BURNOUT_EFFECT_STUB.label}
                                </Badge>
                              )}
                            </div>
                            {c.burnoutRisk && (
                              <p className="text-[9px] text-orange-200/70 leading-snug">
                                <span className="font-medium">GM fiat:</span> {BURNOUT_EFFECT_STUB.disadvantageNote}; {BURNOUT_EFFECT_STUB.actionPenalty}. Not auto-enforced — Director announces.
                              </p>
                            )}
                            {c.burnoutCastHint && (
                              <p className="text-[9px] text-amber-200/80 leading-snug">
                                <span className="font-medium">Overcast check:</span> {c.burnoutCastHint}
                              </p>
                            )}
                            {c.characterClass && resolveCombatantMaxRp(c).maxRp > 0 && (
                              <div className="flex flex-wrap gap-0.5">
                                <Button size="sm" variant="ghost" className="h-6 px-1 text-[10px] text-sky-300"
                                  title="Short rest retune (~¼ pool + casting mod + Nature bonus)"
                                  onClick={() => {
                                    const saved = savedChars.find((s) => s.name === c.name || characterDisplayName(s) === c.name);
                                    retuneCombatant(c.id, saved);
                                  }}>
                                  Retune
                                </Button>
                                <Button size="sm" variant="ghost" className="h-6 px-1 text-[10px] text-indigo-300"
                                  title="Long rest full harmony"
                                  onClick={() => fullRestoreCombatant(c.id)}>
                                  Full
                                </Button>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                      <div className="md:col-span-2 space-y-1">
                        <Input value={c.conditions} placeholder="Prone, Blessed…"
                          onChange={(e) => update(c.id, { conditions: e.target.value })}
                          className="h-8 bg-slate-950 border-slate-600 text-white text-xs" />
                        <div className="flex flex-wrap gap-1">
                          {COMMON_CONDITIONS.map((cond) => (
                            <button
                              key={cond}
                              type="button"
                              onClick={() => toggleCombatantCondition(c.id, cond)}
                              className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors ${
                                hasCondition(c.conditions, cond)
                                  ? "bg-amber-700/60 border-amber-500 text-amber-50"
                                  : "border-slate-600 text-amber-100/50 hover:border-amber-600/50"
                              }`}
                            >
                              {cond}
                            </button>
                          ))}
                        </div>
                      </div>
                      <div className="md:col-span-2">
                        <Input value={c.notes} placeholder="Notes"
                          onChange={(e) => update(c.id, { notes: e.target.value })}
                          className="h-8 bg-slate-950 border-slate-600 text-white text-xs" />
                      </div>
                      <div className="md:col-span-1 flex justify-end gap-1 items-center">
                        {isActive && <Badge className="bg-amber-600 hidden md:inline-flex">Active</Badge>}
                        <Button size="sm" variant="ghost" onClick={() => remove(c.id)}>
                          <Trash2 className="w-4 h-4 text-red-400" />
                        </Button>
                      </div>
                    </div>
                    {badges.length > 0 && (
                      <div className="flex flex-wrap gap-1 pl-1">
                        {badges.map((b) => (
                          <Badge key={b.key} className={`text-[10px] font-normal ${b.className}`}>{b.label}</Badge>
                        ))}
                      </div>
                    )}
                    {c.isEnemy && c.hp <= 0 && (
                      <div className="pl-1 flex flex-wrap items-center gap-2 border-t border-slate-700/50 pt-2">
                        {c.draftXpAwarded ? (
                          <Badge variant="outline" className="text-[10px] border-amber-500/40 text-amber-200/80">
                            Optional XP logged (non-canon)
                          </Badge>
                        ) : (
                          <>
                            <Button
                              size="sm"
                              variant="outline"
                              className="h-7 text-[10px] border-amber-600/50 text-amber-100"
                              title="Optional non-canon CR→XP helper — Opening campaigns use milestones. Does not update saved characters."
                              onClick={() => awardDraftXpForFoe(c.id)}
                            >
                              Optional XP (non-canon)
                            </Button>
                            <span className="text-[10px] text-amber-200/60">
                              CR {c.challengeRating ?? parseCrFromNotes(c.notes) ?? "?"} → {formatXp(draftXpForCr(c.challengeRating ?? parseCrFromNotes(c.notes)))} total — not Opening law
                            </span>
                          </>
                        )}
                      </div>
                    )}
                    {!c.isEnemy && (c.draftXpSession ?? 0) > 0 && (
                      <p className="pl-1 text-[10px] text-amber-200/70">
                        <span className="font-medium">Optional session XP (non-canon):</span> {formatXp(c.draftXpSession)} — Opening uses milestones; tally only, no save write-back
                      </p>
                    )}
                    {!c.isEnemy && (
                      <div className="pl-1 space-y-1">
                        <div className="flex flex-wrap items-center gap-1">
                          <span className="text-[10px] text-amber-200/50 shrink-0 uppercase tracking-wide">Ethos</span>
                          {PLAYER_ALIGNMENTS.map((alignment) => {
                            const axis = alignment.split(/\s+/).pop() || alignment;
                            const selected = c.alignment === alignment;
                            return (
                              <button
                                key={alignment}
                                type="button"
                                title={`${alignment} — ${axis} axis for spell affinity`}
                                onClick={() => update(c.id, { alignment: selected ? "" : alignment })}
                                className={`text-[9px] px-1 py-0.5 rounded border transition-colors ${
                                  selected
                                    ? "bg-amber-800/70 border-amber-400 text-amber-50"
                                    : "border-slate-600 text-amber-200/50 hover:border-amber-600/50"
                                }`}
                              >
                                {ALIGNMENT_ABBREV[alignment] ?? alignment.slice(0, 2)}
                              </button>
                            );
                          })}
                        </div>
                        {c.alignment && (
                          <p className="text-[10px] text-amber-200/60">
                            {c.alignment}
                            {c.castSpellSchool && (() => {
                              const { affinity, opposition } = schoolAffinityMods(c.alignment, c.castSpellSchool);
                              if (!affinity && !opposition) return null;
                              return (
                                <>
                                  {" · "}
                                  {c.castSpellSchool}:{" "}
                                  {affinity && <span className="text-emerald-300">−1 RP</span>}
                                  {affinity && opposition && " / "}
                                  {opposition && <span className="text-orange-300">+1 RP</span>}
                                </>
                              );
                            })()}
                          </p>
                        )}
                      </div>
                    )}
                    {!c.isEnemy && !oracle && c.characterClass && resolveCombatantMaxRp(c).maxRp > 0 && (
                      <div className="pl-1 space-y-1 border-t border-slate-700/50 pt-2">
                        <div className="text-[10px] text-purple-200/60 uppercase tracking-wide">Overcast</div>
                        <div className="flex flex-wrap items-center gap-1">
                          <Input
                            value={spellLookup?.combatantId === c.id ? spellLookup.query : (c.castSpellKey ? getSpellDisplayName(c.castSpellKey) : "")}
                            onChange={(e) => setSpellLookup({ combatantId: c.id, query: e.target.value })}
                            onFocus={() => setSpellLookup({ combatantId: c.id, query: spellLookup?.combatantId === c.id ? spellLookup.query : "" })}
                            placeholder="Spell lookup…"
                            className="h-7 max-w-[140px] bg-slate-950 border-slate-600 text-white text-[10px]"
                          />
                          {spellLookup?.combatantId === c.id && spellLookup.query.trim().length >= 2 && (
                            <div className="flex flex-wrap gap-1">
                              {searchSpellsByName(spellLookup.query, c.characterClass).map((hit) => (
                                <button
                                  key={hit.key}
                                  type="button"
                                  title={`${hit.school} · T${hit.level || "0"}`}
                                  onClick={() => {
                                    update(c.id, {
                                      castSpellKey: hit.key,
                                      castSpellTier: hit.level || 0,
                                      castSpellSchool: hit.school,
                                    });
                                    setSpellLookup(null);
                                  }}
                                  className="text-[10px] px-1.5 py-0.5 rounded border border-indigo-600/50 text-indigo-100 hover:bg-indigo-900/40"
                                >
                                  {hit.name} (T{hit.level})
                                </button>
                              ))}
                            </div>
                          )}
                        </div>
                        <div className="flex flex-wrap items-center gap-1">
                          <span className="text-[10px] text-purple-200/50 shrink-0">School</span>
                          {SPELL_SCHOOLS.map((school) => {
                            const { affinity, opposition } = schoolAffinityMods(c.alignment, school);
                            return (
                              <button
                                key={school}
                                type="button"
                                title={`${school}${affinity ? " · affinity −1" : opposition ? " · opposition +1" : ""}`}
                                onClick={() => update(c.id, {
                                  castSpellSchool: c.castSpellSchool === school ? "" : school,
                                  castSpellKey: c.castSpellSchool === school ? c.castSpellKey : "",
                                })}
                                className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors ${
                                  c.castSpellSchool === school
                                    ? "bg-indigo-800/70 border-indigo-400 text-indigo-50"
                                    : "border-slate-600 text-purple-200/60 hover:border-indigo-500/50"
                                }`}
                              >
                                {school.slice(0, 4)}
                                {affinity && " −1"}
                                {opposition && " +1"}
                              </button>
                            );
                          })}
                        </div>
                        {c.castSpellSchool && c.alignment && (() => {
                          const { affinity, opposition } = overcastAffinityFlags(c);
                          if (!affinity && !opposition) return null;
                          return (
                            <p className="text-[10px] text-purple-200/70">
                              {c.alignment} · {c.castSpellSchool}:{" "}
                              {affinity && <span className="text-emerald-300">Affinity −1 RP</span>}
                              {affinity && opposition && " · "}
                              {opposition && <span className="text-orange-300">Opposition +1 RP</span>}
                            </p>
                          );
                        })()}
                        <div className="flex flex-wrap items-center gap-1">
                          <span className="text-[10px] text-purple-200/50 shrink-0">Spell tier</span>
                          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((tier) => {
                            const { affinity, opposition } = overcastAffinityFlags(c);
                            const preview = spellCost(tier, {
                              affinity,
                              opposition,
                              reputationModifier: spellCostRepModifier(c.characterClass, c.reputation),
                            });
                            return (
                              <button
                                key={tier}
                                type="button"
                                title={`Base RP: ${preview}${c.castSpellSchool ? ` (${c.castSpellSchool})` : ""}`}
                                onClick={() => update(c.id, { castSpellTier: c.castSpellTier === tier ? 0 : tier })}
                                className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors ${
                                  c.castSpellTier === tier
                                    ? "bg-indigo-800/70 border-indigo-400 text-indigo-50"
                                    : "border-slate-600 text-purple-200/60 hover:border-indigo-500/50"
                                }`}
                              >
                                T{tier}
                              </button>
                            );
                          })}
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {OVERCAST_OPTIONS.map((opt) => (
                            <button
                              key={opt.id}
                              type="button"
                              title={`${opt.effect} (+${opt.rpCost} RP)`}
                              onClick={() => toggleOvercast(c.id, opt.id)}
                              className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors ${
                                c.overcastIds.includes(opt.id)
                                  ? "bg-purple-800/70 border-purple-400 text-purple-50"
                                  : "border-slate-600 text-purple-200/60 hover:border-purple-500/50"
                              }`}
                            >
                              {opt.label} +{opt.rpCost}
                            </button>
                          ))}
                        </div>
                        {(c.castSpellTier > 0 || c.overcastIds.length > 0) && (
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-[10px] text-purple-200/70">
                              {c.castSpellTier > 0 && (
                                <>Base: {overcastBaseCost(c)} RP · </>
                              )}
                              {c.overcastIds.length > 0 && <>Surcharge: +{overcastRpCost(c.overcastIds)} RP · </>}
                              Total: {totalCastCost(overcastBaseCost(c), c.overcastIds)} RP
                            </span>
                            <Button size="sm" variant="outline" className="h-6 text-[10px] border-purple-600/50 text-purple-200"
                              onClick={() => applyOvercastSpend(c.id)}
                              title="Deduct base spell cost + overcast surcharge from RP">
                              Apply cast spend
                            </Button>
                            <Button size="sm" variant="ghost" className="h-6 text-[10px] text-slate-400"
                              onClick={() => update(c.id, { overcastIds: [], castSpellTier: 0, castSpellSchool: "", castSpellKey: "", burnoutCastHint: "" })}>
                              Clear
                            </Button>
                          </div>
                        )}
                      </div>
                    )}
                    {!c.isEnemy && isDruidClass(c.characterClass) && (
                      <div className="pl-1 space-y-1 border-t border-emerald-800/40 pt-2">
                        <div className="flex flex-wrap items-center gap-2">
                          <div className="text-[10px] text-emerald-200/60 uppercase tracking-wide">Wild Shape</div>
                          <Badge variant="outline" className="text-[9px] border-emerald-600/40 text-emerald-200/80">
                            CR ≤ {wildShapeCrCap(c.level)}
                          </Badge>
                          {hasArchFormAttunement(c.level) && (
                            <Badge
                              variant="outline"
                              className="text-[9px] border-teal-600/50 text-teal-200/90"
                              title="L15 draft — attune 2 arch forms (Shift+click); swap between attuned forms free once/encounter"
                            >
                              Arch attuned {c.attunedArchFormIds.length}/{ARCH_ATTUNEMENT_MAX}
                              {c.archAttunementSwapUsed ? " · swap used" : ""}
                            </Badge>
                          )}
                          <span className="text-[10px] text-emerald-200/70">
                            Uses {c.wildShapeUses}/{c.wildShapeUsesMax}
                          </span>
                          {c.wildShapeMinutesLeft > 0 && (
                            <Badge className="text-[9px] bg-emerald-900/80 text-emerald-100">
                              {c.wildShapeMinutesLeft} min left
                            </Badge>
                          )}
                          <Button size="sm" variant="outline" className="h-6 text-[10px] border-emerald-600/50 text-emerald-200"
                            disabled={c.wildShapeUses <= 0 || !c.activeFormId}
                            onClick={() => spendWildShape(c.id)}
                            title="Spend one Wild Shape use (pick form first; starts 10 min timer)">
                            Spend use
                          </Button>
                          {c.activeFormId && (
                            <>
                              <Button size="sm" variant="ghost" className="h-6 text-[10px] text-emerald-300/80"
                                disabled={c.wildShapeMinutesLeft <= 0}
                                onClick={() => tickWildShapeMinutes(c.id, -1)}
                                title="Tick down 1 minute (table time)">
                                −1 min
                              </Button>
                              <Button size="sm" variant="ghost" className="h-6 text-[10px] text-slate-400"
                                onClick={() => revertWildShape(c.id)}
                                title="Revert form (bonus action at table)">
                                Revert
                              </Button>
                            </>
                          )}
                          {hasPrimalRecovery(c.level) && (
                            <Button size="sm" variant="outline" className="h-6 text-[10px] border-teal-600/50 text-teal-200"
                              disabled={c.primalRecoveryUsed || c.wildShapeUses <= 0}
                              onClick={() => applyPrimalRecovery(c.id)}
                              title={`Primal Recovery (L13 draft): spend 1 Wild Shape use → regain ${primalRecoveryRpGain(c.level)} RP; once per short rest`}>
                              Primal Recovery +{primalRecoveryRpGain(c.level)} RP
                            </Button>
                          )}
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {shapeshiftFormsForDruid(c.level, c.druidCircle).map((form) => {
                            const attuned =
                              form.tier === "arch" &&
                              hasArchFormAttunement(c.level) &&
                              c.attunedArchFormIds.includes(form.id);
                            return (
                              <button
                                key={form.id}
                                type="button"
                                title={
                                  form.tier === "arch" && hasArchFormAttunement(c.level)
                                    ? `${form.tier} form · Shift+click to attune (${c.attunedArchFormIds.length}/${ARCH_ATTUNEMENT_MAX})`
                                    : `${form.tier} form`
                                }
                                onClick={(e) => {
                                  if (
                                    e.shiftKey &&
                                    form.tier === "arch" &&
                                    hasArchFormAttunement(c.level)
                                  ) {
                                    toggleArchFormAttunement(c.id, form.id);
                                    return;
                                  }
                                  selectWildShapeForm(c.id, c.activeFormId === form.id ? "" : form.id);
                                }}
                                className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors ${
                                  c.activeFormId === form.id
                                    ? "bg-emerald-800/70 border-emerald-400 text-emerald-50"
                                    : attuned
                                      ? "bg-teal-900/50 border-teal-500/60 text-teal-100"
                                      : "border-slate-600 text-emerald-200/60 hover:border-emerald-500/50"
                                }`}
                              >
                                {attuned && "★ "}
                                {form.name}
                                {form.draft && " · Draft"}
                              </button>
                            );
                          })}
                        </div>
                        {c.activeFormId ? (
                          <p className="text-[10px] text-emerald-200/60 italic">
                            Active: {(() => {
                              const activeForm = shapeshiftFormsForDruid(c.level, c.druidCircle).find(
                                (form) => form.id === c.activeFormId
                              );
                              return `${activeForm?.name ?? c.activeFormId}${activeForm?.draft ? " (draft)" : ""}`;
                            })()}
                            {" · "}{wildShapeDurationMinutes()} min/form
                            {c.wildShapeMinutesLeft > 0 ? ` · ${c.wildShapeMinutesLeft} min remaining` : " · pick form + Spend use to start timer"}
                            {" · "}revert as bonus action
                            {hasPrimalRecovery(c.level) && (
                              <span className="text-teal-200/70">
                                {" · "}Primal Recovery {c.primalRecoveryUsed ? "used this rest" : "ready"}
                              </span>
                            )}
                            {hasArchFormAttunement(c.level) && c.attunedArchFormIds.length > 0 && (
                              <span className="text-teal-200/70">
                                {" · "}Attuned: {c.attunedArchFormIds.join(", ")}
                                {c.archAttunementSwapUsed ? " · free swap spent" : " · free swap ready"}
                              </span>
                            )}
                          </p>
                        ) : hasArchFormAttunement(c.level) && c.attunedArchFormIds.length > 0 ? (
                          <p className="text-[10px] text-teal-200/60 italic">
                            Attuned arch: {c.attunedArchFormIds.join(", ")} · Shift+click arch forms to attune
                            {c.archAttunementSwapUsed ? " · free swap spent" : " · free swap ready"}
                          </p>
                        ) : null}
                      </div>
                    )}
                    {!c.isEnemy && isShamanClass(c.characterClass) && maxActiveTotems(c.level) > 0 && (
                      <div className="pl-1 space-y-1 border-t border-cyan-800/40 pt-2">
                        <div className="flex flex-wrap items-center gap-2">
                          <div className="text-[10px] text-cyan-200/60 uppercase tracking-wide">Totems</div>
                          <Badge
                            variant="outline"
                            className="text-[9px] border-cyan-600/40 text-cyan-200/80"
                            title="Draft table tracker — resolve each totem's effect with the Shaman path and GM."
                          >
                            Placed {c.activeTotemIds.length}/{maxActiveTotems(c.level)}
                          </Badge>
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-6 text-[10px] text-cyan-300/80"
                            disabled={!c.activeTotemIds.length}
                            onClick={() => recallTotems(c.id)}
                            title="Clear placed totems from the session tracker"
                          >
                            Recall all
                          </Button>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {SHAMAN_TOTEM_OPTIONS.map((totem) => {
                            const active = c.activeTotemIds.includes(totem.id);
                            const full = !active && c.activeTotemIds.length >= maxActiveTotems(c.level);
                            return (
                              <button
                                key={totem.id}
                                type="button"
                                disabled={full}
                                onClick={() => toggleTotem(c.id, totem.id)}
                                title={
                                  active
                                    ? `Recall ${totem.label}`
                                    : `Place ${totem.label}; its Totem Pulse resolves at the table`
                                }
                                className={`text-[10px] px-1.5 py-0.5 rounded border transition-colors disabled:opacity-40 ${
                                  active
                                    ? "bg-cyan-800/70 border-cyan-400 text-cyan-50"
                                    : "border-slate-600 text-cyan-200/60 hover:border-cyan-500/50"
                                }`}
                              >
                                {active && "● "}{totem.label}
                              </button>
                            );
                          })}
                        </div>
                        <p className="text-[10px] text-cyan-200/55 leading-snug">
                          {c.level >= 13 ? "L13 draft: second active slot. " : ""}
                          Placement triggers Totem Pulse; this stub records presence only, so path effects stay GM-resolved.
                        </p>
                      </div>
                    )}
                    {isActive && <Badge className="bg-amber-600 md:hidden w-fit">Active turn</Badge>}
                  </div>
                );
              })}
              {crowdedFoes && combatantFilter === "all" && (
                <button
                  type="button"
                  onClick={() => setFoesExpanded((open) => !open)}
                  className="w-full flex items-center gap-2 rounded border border-red-800/50 bg-red-950/20 px-3 py-2 text-left text-sm text-red-200/90 hover:bg-red-950/35 transition-colors"
                >
                  {foesExpanded ? (
                    <ChevronDown className="w-4 h-4 shrink-0" />
                  ) : (
                    <ChevronRight className="w-4 h-4 shrink-0" />
                  )}
                  <span>
                    {foesExpanded ? "Collapse" : "Show"} foes ({orderedFoes.length})
                  </span>
                </button>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
