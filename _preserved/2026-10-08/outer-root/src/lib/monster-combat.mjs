/**
 * Normalizes the optional Bestiary combat payload without inventing a fallback.
 * See docs/mechanics/MONSTER_COMBAT_SCHEMA.md.
 */

/** @typedef {{ minimumRoll: number, dieSides: number }} RechargeSpec */

/**
 * Probability a recharge action is available at the start of a turn.
 * @param {RechargeSpec} recharge
 */
export function rechargeAvailabilityProbability(recharge) {
  const { minimumRoll, dieSides } = recharge;
  if (!Number.isFinite(minimumRoll) || !Number.isFinite(dieSides) || dieSides < 1) {
    return 0;
  }
  const successOutcomes = Math.max(0, dieSides - minimumRoll + 1);
  return Math.min(1, successOutcomes / dieSides);
}

export function resolveMonsterCombat(monster) {
  if (!monster || typeof monster !== "object") {
    return { combat: null, reason: "Monster record is missing." };
  }

  const combat = monster.combat;
  if (!combat || typeof combat !== "object") {
    return { combat: null, reason: "No structured combat payload is authored for this monster." };
  }
  if (combat.schemaVersion !== 1) {
    return { combat: null, reason: `Unsupported combat schema version: ${combat.schemaVersion ?? "missing"}.` };
  }
  if (!Array.isArray(combat.attacks) || combat.attacks.length === 0) {
    return { combat: null, reason: "Structured combat has no attacks." };
  }
  if (!combat.defenses || !Array.isArray(combat.defenses.resistances)
    || !Array.isArray(combat.defenses.immunities)
    || !Array.isArray(combat.defenses.conditionImmunities)) {
    return { combat: null, reason: "Structured combat defenses are incomplete." };
  }

  const defaultAction = combat.attacks.find((attack) => attack.id === combat.defaultActionId);
  if (!defaultAction) {
    return { combat: null, reason: "Structured combat defaultActionId does not identify an attack." };
  }
  if (defaultAction.kind !== "attack" || defaultAction.usage !== "atWill"
    || !Number.isFinite(defaultAction.attackBonus)
    || !Array.isArray(defaultAction.damage) || defaultAction.damage.length === 0) {
    return { combat: null, reason: "Structured combat default action cannot model sustained attack DPR." };
  }
  if (defaultAction.damage.some((damage) => !Number.isFinite(damage.average))) {
    return { combat: null, reason: "Structured combat default action has invalid damage averages." };
  }

  return { combat, reason: null };
}

export function sustainedAttackDpr(combat, targetAc, hitChance) {
  const action = combat.attacks.find((attack) => attack.id === combat.defaultActionId);
  const averageDamage = action.damage.reduce((total, damage) => total + damage.average, 0);
  return (action.count ?? 1) * averageDamage * hitChance(action.attackBonus, targetAc);
}

/**
 * Expected per-round DPR from recharge actions (draft cadence model).
 *
 * Assumptions (documented in MONSTER_COMBAT_SCHEMA.md):
 * - Recharge is available on round 1, then re-rolls each turn; steady-state availability
 *   equals rechargeAvailabilityProbability (e.g. 5-6 on d6 → 1/3).
 * - Save actions: flat save-fail rate (default 55%); success halves damage.
 * - Area scope is treated as single-target full expected damage (conservative for party).
 *
 * @param {object} combat
 * @param {number} targetAc
 * @param {(bonus: number, ac: number) => number} hitChance
 * @param {{ saveFailRate?: number }} [options]
 */
export function expectedRechargeDpr(combat, targetAc, hitChance, options = {}) {
  const saveFailRate = options.saveFailRate ?? 0.55;
  const rechargeAttacks = combat.attacks.filter(
    (attack) => attack.usage === "recharge" && attack.recharge,
  );

  return rechargeAttacks.reduce((total, attack) => {
    const availability = rechargeAvailabilityProbability(attack.recharge);
    const averageDamage = attack.damage.reduce((sum, damage) => sum + damage.average, 0);
    if (attack.kind === "attack") {
      if (!Number.isFinite(attack.attackBonus)) return total;
      return total + availability * averageDamage * hitChance(attack.attackBonus, targetAc);
    }
    if (attack.kind === "save" && attack.save) {
      const expectedSaveDamage = averageDamage * (saveFailRate + (1 - saveFailRate) * 0.5);
      return total + availability * expectedSaveDamage;
    }
    return total;
  }, 0);
}

/**
 * At-will plus optional recharge expected DPR.
 * @param {object} combat
 * @param {number} targetAc
 * @param {(bonus: number, ac: number) => number} hitChance
 * @param {{ includeRecharge?: boolean, saveFailRate?: number }} [options]
 */
export function totalExpectedMonsterDpr(combat, targetAc, hitChance, options = {}) {
  const atWill = sustainedAttackDpr(combat, targetAc, hitChance);
  if (options.includeRecharge === false) return atWill;
  return atWill + expectedRechargeDpr(combat, targetAc, hitChance, options);
}

export function listRechargeAttacks(combat) {
  return combat.attacks.filter((attack) => attack.usage === "recharge");
}
