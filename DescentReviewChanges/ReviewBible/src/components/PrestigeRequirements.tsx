"use client";

import { Badge } from "@/components/ui/badge";
import {
  extractPrestigeFeats,
  missingPrestigeFeats,
  parsePrestigeRequirementLines,
} from "@/lib/prestige-utils";

type PrestigePath = {
  name: string;
  requirements?: string;
  unlock?: string;
  entrance?: string;
  baseClass?: string;
};

export default function PrestigeRequirements({
  prestige,
  selectedFeats = [],
  compact = false,
}: {
  prestige: PrestigePath;
  selectedFeats?: string[];
  compact?: boolean;
}) {
  const reqLines = parsePrestigeRequirementLines(prestige.requirements);
  const reqFeats = extractPrestigeFeats(prestige.requirements);
  const missing = missingPrestigeFeats(prestige.requirements, selectedFeats);
  const unlockText = (prestige.unlock || prestige.entrance || "").trim();

  return (
    <div className={`space-y-1 ${compact ? "text-[11px]" : "text-xs"} text-amber-50/80 print:text-gray-800`}>
      {reqLines.length > 0 && (
        <div>
          <span className="text-amber-400 font-medium">Requirements:</span>
          <ul className="list-disc pl-4 mt-1 text-amber-100/75 space-y-0.5">
            {reqLines.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </div>
      )}
      {reqFeats.length > 0 && (
        <div>
          <span className="text-amber-400 font-medium">Feat prerequisites:</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {reqFeats.map((feat) => {
              const has = selectedFeats.includes(feat);
              return (
                <Badge
                  key={feat}
                  variant="outline"
                  className={`text-[10px] ${
                    has
                      ? "border-green-600/50 text-green-300/90"
                      : "border-red-600/50 text-red-300/90"
                  }`}
                >
                  {has ? "✓" : "○"} {feat}
                </Badge>
              );
            })}
          </div>
          {missing.length > 0 && (
            <p className="text-red-300/80 mt-1 print:text-gray-700">
              Missing on sheet: {missing.join(", ")}
            </p>
          )}
        </div>
      )}
      {unlockText && (
        <div>
          <span className="text-amber-400 font-medium">Unlock:</span>{" "}
          {unlockText}
        </div>
      )}
    </div>
  );
}
