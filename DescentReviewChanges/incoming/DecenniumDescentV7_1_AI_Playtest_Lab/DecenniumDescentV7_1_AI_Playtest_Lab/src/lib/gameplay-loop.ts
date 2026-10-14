export type Degree = "critical-success" | "success" | "failure" | "critical-failure";
export type SizeCategory = "Small" | "Medium" | "Large";
export type MappingState = "Unknown" | "Sketched" | "Mapped" | "Secured";

const DEGREE_ORDER: Degree[] = [
  "critical-failure",
  "failure",
  "success",
  "critical-success",
];

export function degreeOfSuccess(total: number, dc: number, naturalRoll?: number): Degree {
  let result: Degree;
  if (total >= dc + 10) result = "critical-success";
  else if (total >= dc) result = "success";
  else if (total <= dc - 10) result = "critical-failure";
  else result = "failure";

  const current = DEGREE_ORDER.indexOf(result);
  if (naturalRoll === 20) return DEGREE_ORDER[Math.min(DEGREE_ORDER.length - 1, current + 1)];
  if (naturalRoll === 1) return DEGREE_ORDER[Math.max(0, current - 1)];
  return result;
}

export function carryLimit(strengthScore: number, size: SizeCategory = "Medium"): number {
  const strength = Math.max(1, Math.floor(Number(strengthScore) || 1));
  if (size === "Small") return Math.max(1, strength - 2);
  if (size === "Large") return strength * 2;
  return strength;
}

export function isBurdened(load: number, limit: number): boolean {
  return Math.max(0, load) > Math.max(0, limit) / 2;
}

export function casualtyLoad(size: SizeCategory = "Medium"): number {
  if (size === "Small") return 3;
  if (size === "Large") return 12;
  return 6;
}

export function routeProgressForWatch(mapping: MappingState, overCapacity = false): number {
  const base = mapping === "Secured" || mapping === "Mapped" ? 2 : mapping === "Sketched" ? 1 : 0;
  return Math.max(0, base - (overCapacity ? 1 : 0));
}

export function pressureTriggersComplication(pressure: number, d6Roll: number): boolean {
  const p = Math.max(0, Math.min(6, Math.floor(pressure)));
  if (p === 0) return false;
  if (p === 6) return true;
  return Math.max(1, Math.min(6, Math.floor(d6Roll))) <= p;
}

export function complicationSeverity(pressure: number, d6Roll: number): "none" | "minor" | "standard" | "severe" {
  if (!pressureTriggersComplication(pressure, d6Roll)) return "none";
  if (pressure >= 6 || d6Roll === 1) return "severe";
  if (d6Roll === pressure) return "minor";
  return "standard";
}

export function dailySupplyRequirement(mediumOrSmall: number, large: number): number {
  return Math.max(0, Math.floor(mediumOrSmall)) + Math.max(0, Math.floor(large)) * 2;
}

export function extractionPressureIncrease(highestExtractionClass: number): number {
  return Math.min(3, Math.floor(Math.max(0, highestExtractionClass) / 2));
}

export function extractionDc(options: {
  tierDc: number;
  burdened?: boolean;
  unsecuredDangerousLots?: number;
  pursued?: boolean;
  securedRoute?: boolean;
}): number {
  const dangerous = Math.min(3, Math.max(0, Math.floor(options.unsecuredDangerousLots ?? 0)));
  return Math.max(
    5,
    Math.floor(options.tierDc)
      + (options.burdened ? 1 : 0)
      + dangerous
      + (options.pursued ? 2 : 0)
      - (options.securedRoute ? 2 : 0),
  );
}

export function saleValue(options: {
  baseValue: number;
  provenance: number;
  demand: number;
  condition: number;
  urgency: number;
}): number {
  const value = Math.max(0, options.baseValue)
    * Math.max(0, options.provenance)
    * Math.max(0, options.demand)
    * Math.max(0, options.condition)
    * Math.max(0, options.urgency);
  return Math.round(value);
}

export function netAfterSponsor(grossAfterTax: number, sponsorShare: number): number {
  const share = Math.max(0, Math.min(1, sponsorShare));
  return Math.max(0, Math.round(Math.max(0, grossAfterTax) * (1 - share)));
}

export function xpAwardFromGap(levelGap: number, percent: number): number {
  const raw = Math.max(0, levelGap) * Math.max(0, Math.min(0.6, percent));
  return Math.max(0, Math.round(raw / 10) * 10);
}

export function adjustedEncounterBudget(baseBudget: number, partySize: number): number {
  const difference = Math.floor(partySize) - 4;
  return Math.max(1, Math.round(baseBudget * Math.pow(1.2, difference)));
}

export function relativeThreatPoints(relativeLevel: number): number {
  if (relativeLevel <= -4) return 5;
  if (relativeLevel === -3) return 10;
  if (relativeLevel === -2) return 15;
  if (relativeLevel === -1) return 25;
  if (relativeLevel === 0) return 40;
  if (relativeLevel === 1) return 60;
  if (relativeLevel === 2) return 90;
  if (relativeLevel === 3) return 135;
  return 200;
}

export function forageSupply(sustenance: number, degree: Degree): number {
  const value = Math.max(0, Math.min(4, Math.floor(sustenance)));
  if (degree === "critical-success") return value + Math.ceil(value / 2);
  if (degree === "success") return value;
  return 0;
}

export function extractionTestDue(options: {
  mapping: MappingState;
  progress: number;
  length: number;
  lastTestProgress?: number;
  atExit?: boolean;
  severeComplication?: boolean;
  routeTransition?: boolean;
}): boolean {
  if (options.severeComplication) return true;
  if (options.atExit) return true;
  const progress = Math.max(0, Math.floor(options.progress));
  const last = Math.max(-1, Math.floor(options.lastTestProgress ?? -1));
  if (progress === last) return false;
  if (options.mapping === "Secured") return Boolean(options.routeTransition);
  if (options.mapping === "Mapped") return options.length >= 6 && progress >= Math.ceil(options.length / 2) && last < Math.ceil(options.length / 2);
  if (options.mapping === "Sketched") return progress > 0 && progress % 3 === 0;
  return progress > 0 && progress % 2 === 0;
}

export function havenTaxRate(category: "routine" | "licensed" | "artifact" | "strategic" | "amnesty"): number {
  return ({ routine: 0.03, licensed: 0.05, artifact: 0.06, strategic: 0.08, amnesty: 0.12 })[category];
}

export function underwaysComplication(heat: number, d6Roll: number): boolean {
  const score = Math.max(0, Math.min(6, Math.floor(heat)));
  return score > 0 && Math.max(1, Math.min(6, Math.floor(d6Roll))) <= score;
}

export function reputationLabel(score: number): string {
  const s = Math.max(-5, Math.min(5, Math.round(score)));
  const labels: Record<number, string> = {
    [-5]: "Proscribed",
    [-4]: "Hunted",
    [-3]: "Hostile",
    [-2]: "Distrusted",
    [-1]: "Unwelcome",
    0: "Neutral",
    1: "Recognized",
    2: "Favored",
    3: "Trusted",
    4: "Champion",
    5: "Authority",
  };
  return labels[s];
}
