"use client";

import { Badge } from "@/components/ui/badge";

type ArchPath = {
  name: string;
  levels: string;
  passives?: string[];
  actives?: string[];
};

type HeroPath = {
  name: string;
  alignment?: string;
  tagline?: string;
  draft?: boolean;
  passives?: string[];
  actives?: string[];
  finale?: string;
};

function SkillList({ title, items }: { title: string; items?: string[] }) {
  if (!items?.length) return null;
  return (
    <div className="mt-2">
      <div className="text-amber-400/90 text-[11px] font-medium uppercase tracking-wide">{title}</div>
      <ul className="list-disc pl-4 mt-1 space-y-0.5 text-xs text-amber-50/75">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default function ClassPathDisplay({
  archPaths,
  heroPaths,
  compact = false,
  showEmptyHeroPaths = false,
}: {
  archPaths?: ArchPath[];
  heroPaths?: HeroPath[];
  compact?: boolean;
  showEmptyHeroPaths?: boolean;
  className?: string;
}) {
  if (!archPaths?.length && !heroPaths?.length && !showEmptyHeroPaths) return null;

  const card = compact
    ? "border border-amber-700/30 rounded p-2 bg-black/20"
    : "border border-amber-700/40 rounded p-3 bg-black/30";

  return (
    <div className="space-y-3">
      {archPaths?.map((arch) => (
        <div key={arch.name} className={card}>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-amber-300 font-semibold text-xs">Arch: {arch.name}</span>
            <Badge variant="outline" className="text-[10px] border-amber-600/40 text-amber-200/70">
              L{arch.levels}
            </Badge>
          </div>
          <SkillList title="Passives" items={arch.passives} />
          <SkillList title="Actives" items={arch.actives} />
        </div>
      ))}
      {heroPaths?.map((hero) => (
        <div key={hero.name} className={card}>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-purple-300 font-semibold text-xs">{hero.name}</span>
            {hero.draft && (
              <Badge variant="outline" className="text-[10px] border-sky-600/40 text-sky-200/80">
                Draft
              </Badge>
            )}
            {hero.alignment && (
              <Badge variant="outline" className="text-[10px] border-purple-600/40 text-purple-200/70">
                {hero.alignment}
              </Badge>
            )}
          </div>
          {hero.tagline && <p className="text-[11px] text-amber-100/60 mt-1 italic">{hero.tagline}</p>}
          <SkillList title="Passives" items={hero.passives} />
          <SkillList title="Actives" items={hero.actives} />
          {hero.finale && (
            <p className="text-[11px] text-amber-200/70 mt-2">
              <span className="text-amber-400">Final theorem:</span> {hero.finale}
            </p>
          )}
        </div>
      ))}
      {showEmptyHeroPaths && !heroPaths?.length && (
        <div className={card}>
          <p className="text-[11px] text-amber-100/60">
            No hero-path entries are recorded in the current reference for this class.
          </p>
        </div>
      )}
    </div>
  );
}
