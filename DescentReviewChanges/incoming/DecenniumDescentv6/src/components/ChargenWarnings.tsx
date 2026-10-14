"use client";

import { AlertTriangle } from "lucide-react";
import { getChargenWarnings, type ChargenSnapshot } from "@/lib/chargen-validation";

export default function ChargenWarnings({
  character,
  compact = false,
}: {
  character: ChargenSnapshot;
  compact?: boolean;
}) {
  const warnings = getChargenWarnings(character);
  if (!warnings.length) return null;

  const required = warnings.filter((w) => w.severity === "required");
  const advisory = warnings.filter((w) => w.severity === "advisory");

  return (
    <div
      className={`rounded-lg border print:border-gray-400 ${
        required.length
          ? "border-red-600/50 bg-red-950/30"
          : "border-amber-600/40 bg-amber-950/25"
      } ${compact ? "p-2" : "p-3"}`}
    >
      <div className="flex items-center gap-2 mb-1.5">
        <AlertTriangle
          className={`w-4 h-4 shrink-0 ${required.length ? "text-red-400" : "text-amber-400"}`}
        />
        <span className={`text-xs font-semibold ${required.length ? "text-red-300" : "text-amber-300"}`}>
          {required.length ? "Required picks missing" : "Chargen notes"}
        </span>
      </div>
      <ul className={`space-y-0.5 ${compact ? "text-[11px]" : "text-xs"} text-amber-50/85 print:text-gray-800`}>
        {required.map((w) => (
          <li key={w.id} className="text-red-200/90 print:text-gray-900">
            {w.message}
          </li>
        ))}
        {advisory.map((w) => (
          <li key={w.id} className="text-amber-100/75 print:text-gray-700">
            {w.message}
          </li>
        ))}
      </ul>
    </div>
  );
}
