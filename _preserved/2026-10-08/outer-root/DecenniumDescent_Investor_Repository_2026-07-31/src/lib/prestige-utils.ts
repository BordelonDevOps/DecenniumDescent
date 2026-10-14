function trimOrEmpty(value: string | undefined | null): string {
  return typeof value === "string" ? value.trim() : "";
}

/** Strip empty hallmark slots and trim prose lines. */
export function cleanHallmarks(hallmarks: string[] | undefined | null): string[] {
  return (hallmarks || []).map((h) => trimOrEmpty(h)).filter(Boolean);
}

/** Split lorebook requirement strings into labeled lines (drops empty segments from leading `-`). */
export function parsePrestigeRequirementLines(requirements: string | undefined | null): string[] {
  const raw = trimOrEmpty(requirements);
  if (!raw) return [];
  return raw
    .split(/\s*-\s*/)
    .map((s) => s.trim())
    .filter(Boolean);
}

/** Parse feat names from prestige-lorebook `requirements` strings. */
export function extractPrestigeFeats(requirements: string | undefined | null): string[] {
  const segments = parsePrestigeRequirementLines(requirements);
  const featSeg = segments.find((s) => /^Feats:/i.test(s));
  if (!featSeg) return [];
  return featSeg
    .replace(/^Feats:\s*/i, "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

/** @returns feat names from requirements that are not in `selectedFeats` */
export function missingPrestigeFeats(
  requirements: string | undefined | null,
  selectedFeats: string[] | undefined | null
): string[] {
  const taken = new Set(selectedFeats || []);
  return extractPrestigeFeats(requirements).filter((f) => !taken.has(f));
}
