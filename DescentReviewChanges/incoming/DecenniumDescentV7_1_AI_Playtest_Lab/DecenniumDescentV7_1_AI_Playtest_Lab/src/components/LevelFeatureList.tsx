"use client";

import { Badge } from "@/components/ui/badge";
import { featureSource, featureText, isDraftFeature, normalizeLevelFeatures } from "@/data/class-level-utils";

export default function LevelFeatureList({
  levels,
  compact = false,
}: {
  levels?: Record<number, (string | { text: string; draft?: boolean; source?: string })[]>;
  compact?: boolean;
}) {
  const rows = normalizeLevelFeatures(levels);
  if (!rows.length) return <p className="text-xs text-amber-50/50">—</p>;

  const draftCount = rows.reduce(
    (n, r) => n + r.features.filter((f) => f.draft).length,
    0
  );
  const hasDraft = draftCount > 0;

  return (
    <div className="space-y-1">
      {hasDraft && (
        <p className="text-[10px] text-amber-200/50 italic mb-2 print:text-gray-700 print:break-inside-avoid">
          {draftCount} draft milestone{draftCount === 1 ? "" : "s"} pending author review — marked with{" "}
          <Badge
            variant="outline"
            className="text-[9px] px-1 py-0 border-amber-500/40 text-amber-300/80 align-middle print:border-gray-400 print:text-gray-700 print:bg-transparent"
          >
            Draft
          </Badge>
          .
        </p>
      )}
      {rows.map(({ level, features }) => (
        <div key={level} className={compact ? "text-xs print:text-gray-800" : "text-xs text-amber-50/80 print:text-gray-800"}>
          <span className="text-amber-400 font-medium print:text-black">L{level}: </span>
          {features.map((f, i) => (
            <span key={`${level}-${i}`}>
              {i > 0 ? ", " : ""}
              {featureText(f)}
              {isDraftFeature(f) && (
                <Badge
                  variant="outline"
                  className="ml-1 text-[9px] px-1 py-0 border-amber-500/40 text-amber-300/80 align-middle print:border-gray-400 print:text-gray-700 print:bg-transparent"
                  title={featureSource(f) || undefined}
                >
                  Draft
                </Badge>
              )}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
}
