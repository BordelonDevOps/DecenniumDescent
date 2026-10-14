"use client";

import { Badge } from "@/components/ui/badge";
import { getClassCeilingCaps } from "@/data/class-ceiling-caps";

export default function ClassCeilingCapsCallout({
  className,
  compact = false,
}: {
  className: string | null | undefined;
  compact?: boolean;
}) {
  const profile = getClassCeilingCaps(className);
  if (!profile) return null;

  return (
    <div
      className={`border border-amber-600/40 rounded bg-amber-950/20 text-xs ${
        compact ? "p-2" : "p-3"
      } print:border-gray-400 print:bg-transparent`}
    >
      <div className="flex flex-wrap items-center gap-2 mb-1">
        <span className="text-amber-300 font-medium print:text-black">Ceiling caps (GM fiat)</span>
        <Badge
          variant="outline"
          className="text-[9px] px-1 py-0 border-amber-500/40 text-amber-300/80 print:border-gray-400 print:text-gray-700"
        >
          GM fiat
        </Badge>
      </div>
      <p className="text-amber-100/70 print:text-gray-700 mb-2">
        Informational only — not auto-enforced. {profile.summary}
      </p>
      <ul className={`space-y-1 text-amber-50/80 print:text-gray-800 ${compact ? "text-[11px]" : ""}`}>
        {profile.caps.map((row) => (
          <li key={row.category}>
            <strong className="text-amber-200/90 print:text-black">{row.category}:</strong> {row.cap}
            {row.note ? (
              <span className="text-amber-200/50 print:text-gray-600"> — {row.note}</span>
            ) : null}
          </li>
        ))}
      </ul>
      {!compact && profile.playtestLedger.length > 0 && (
        <p className="mt-2 text-[10px] text-amber-200/50 italic print:text-gray-600">
          Playtest ledger: {profile.playtestLedger.join(" · ")}
        </p>
      )}
      <p className="mt-1 text-[10px] text-amber-200/40 print:text-gray-500">
        See docs/mechanics/CLASS_CEILING_CAPS.md — Worker 3
      </p>
    </div>
  );
}
