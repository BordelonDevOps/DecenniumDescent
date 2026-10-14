/** Helpers for class level features (canon strings or draft objects). */

/** @typedef {{ text: string; draft?: boolean; source?: string }} LevelFeature */

const DRAFT_SOURCE = "Draft — pending author review";

/** @param {string | LevelFeature} feature */
export function featureText(feature) {
  if (typeof feature === "string") return feature;
  return feature?.text ?? "";
}

/** @param {string | LevelFeature} feature */
export function isDraftFeature(feature) {
  if (typeof feature === "string") return false;
  return Boolean(feature?.draft);
}

/** @param {string | LevelFeature} feature */
export function featureSource(feature) {
  if (typeof feature === "string") return null;
  if (feature?.draft) return feature.source || DRAFT_SOURCE;
  return feature.source ?? null;
}

/** @param {string} text */
export function draftFeature(text) {
  return { text, draft: true, source: DRAFT_SOURCE };
}

/** @param {Record<number, (string | LevelFeature)[] | undefined> | undefined} levels */
export function normalizeLevelFeatures(levels) {
  if (!levels) return [];
  return Object.keys(levels)
    .map(Number)
    .sort((a, b) => a - b)
    .map((level) => ({
      level,
      features: (levels[level] || []).map((f) =>
        typeof f === "string" ? { text: f, draft: false } : { ...f, draft: Boolean(f.draft) }
      ),
    }));
}

export { DRAFT_SOURCE };
