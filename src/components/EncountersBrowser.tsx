"use client";

import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { AlertTriangle, MapPin, Shield, Search, Swords, X } from "lucide-react";
import encounters from "@/data/floor-encounters.json";
import encounterToolkitT15 from "@/data/t1-5-encounter-toolkit.json";
import encounterToolkitT610 from "@/data/t6-10-encounter-toolkit.json";
import { pushEncounterHandoff } from "@/lib/session-handoff";

type Haven = { name: string; description: string };
type DraftRegion = { name: string; note: string; draft?: boolean };
type DraftHazard = { name: string; description: string; draft?: boolean };
type GateBossSeed = {
  name: string;
  encounterTitle: string;
  description: string;
  draft?: boolean;
};
type EncounterVibe = {
  summary: string;
  tags?: string[];
  draft?: boolean;
};
type Tier = {
  tier: number;
  name: string;
  floors: string;
  description: string;
  draftNote?: string;
  draft?: boolean;
  boss: string;
  difficulty?: string;
  mapped?: boolean;
  regionNames?: DraftRegion[];
  hazards?: DraftHazard[];
  gateBossSeed?: GateBossSeed;
  encounterVibe?: EncounterVibe;
  safeHavens: Haven[];
  pointsOfInterest: Haven[];
};

const tiers = encounters.tiers as Tier[];

function tierMatchesQuery(t: Tier, q: string): boolean {
  const hay = [
    t.name,
    t.floors,
    t.description,
    t.boss,
    t.difficulty ?? "",
    t.draftNote ?? "",
    t.gateBossSeed?.encounterTitle ?? "",
    t.gateBossSeed?.description ?? "",
    t.encounterVibe?.summary ?? "",
    ...(t.encounterVibe?.tags ?? []),
    ...(t.regionNames?.flatMap((r) => [r.name, r.note]) ?? []),
    ...(t.hazards?.flatMap((h) => [h.name, h.description]) ?? []),
    ...t.safeHavens.flatMap((h) => [h.name, h.description]),
    ...t.pointsOfInterest.flatMap((p) => [p.name, p.description]),
  ]
    .join(" ")
    .toLowerCase();
  return hay.includes(q);
}

type ToolkitActor = {
  displayName: string;
  count: number;
  role: string;
  bestiaryName?: string;
  bestiaryCr?: string;
  intendedCrBand?: string;
  sandboxCr?: boolean;
  note?: string;
};
type ToolkitRoster = {
  id: string;
  title: string;
  job: string;
  targetPressureBand: string;
  detailedActors: ToolkitActor[];
  notes?: string;
};
type ToolkitCard = {
  id: string;
  floors: string;
  title: string;
  job: string;
  targetBand: string;
  site?: string;
  summary?: string;
  detailedActorBudget?: string;
  rosterRef?: string;
  hazard?: string;
};
type ToolkitTier = {
  tier: number;
  zone: string;
  corePressures?: string[];
  sampleRosters: ToolkitRoster[];
  encounterCards: ToolkitCard[];
};

type ToolkitGuardian = {
  tier: number;
  name: string;
  type: string;
  challengeRating: string;
  size: string;
  alignment: string;
};

type ToolkitRoot = {
  tiers: ToolkitTier[];
  budgetGuidance: { method: string; eightActorRule: { maxDetailedInitiativeActors: number } };
  meta: { xpStance: string };
  gateGuardiansT1to5?: ToolkitGuardian[];
  gateGuardiansT6to10?: ToolkitGuardian[];
};

type EncountersBrowserProps = {
  onLoadSession?: () => void;
};

export default function EncountersBrowser({ onLoadSession }: EncountersBrowserProps) {
  const [selectedTier, setSelectedTier] = useState(1);
  const [query, setQuery] = useState("");

  const tier = tiers.find((t) => t.tier === selectedTier) ?? tiers[0];
  const toolkitRoot = (
    selectedTier <= 5 ? encounterToolkitT15 : encounterToolkitT610
  ) as ToolkitRoot;
  const toolkitTier = toolkitRoot.tiers.find((t) => t.tier === selectedTier);
  const toolkitGuardians =
    toolkitRoot.gateGuardiansT1to5 ?? toolkitRoot.gateGuardiansT6to10 ?? [];
  const toolkitGuardian = toolkitGuardians.find((g) => g.tier === selectedTier);
  const toolkitBudget = toolkitRoot.budgetGuidance;
  const toolkitXpStance = toolkitRoot.meta.xpStance;

  const q = query.trim().toLowerCase();
  const hasActiveFilters = q.length > 0;

  const clearFilters = () => setQuery("");

  const matchingTiers = useMemo(() => {
    if (!q) return [];
    return tiers.filter((t) => tierMatchesQuery(t, q));
  }, [q]);

  const filtered = useMemo(() => {
    if (!q) return tier;
    const match = (h: Haven) =>
      h.name.toLowerCase().includes(q) || h.description.toLowerCase().includes(q);
    const tierMetaMatch =
      tier.name.toLowerCase().includes(q) ||
      tier.boss.toLowerCase().includes(q) ||
      tier.description.toLowerCase().includes(q) ||
      tier.floors.toLowerCase().includes(q);
    return {
      ...tier,
      safeHavens: tierMetaMatch ? tier.safeHavens : tier.safeHavens.filter(match),
      pointsOfInterest: tierMetaMatch ? tier.pointsOfInterest : tier.pointsOfInterest.filter(match),
    };
  }, [tier, q]);

  const loadInSession = ({
    site,
    haven,
  }: {
    site?: Haven;
    haven?: Haven;
  } = {}) => {
    const poi = site ?? tier.pointsOfInterest[0];
    const fallbackHaven = haven ?? tier.safeHavens[0];
    const brief = [
      `Tier ${tier.tier}: ${tier.name} (Floors ${tier.floors})`,
      poi ? `Site: ${poi.name}` : "Site: Uncharted / no POI data",
      fallbackHaven
        ? `Fallback haven: ${fallbackHaven.name}`
        : "Fallback haven: None confirmed",
      `Gate boss: ${tier.boss}`,
      tier.gateBossSeed?.encounterTitle
        ? `Gate seed: ${tier.gateBossSeed.encounterTitle}`
        : "",
      tier.encounterVibe?.summary ? `Vibe: ${tier.encounterVibe.summary}` : "",
      tier.mapped ? "" : "[DRAFT tier — seeds only; not mapped canon]",
    ]
      .filter(Boolean)
      .join("\n");
    pushEncounterHandoff({
      tier: tier.tier,
      tierName: tier.name,
      boss: tier.boss,
      floors: tier.floors,
      brief,
      source: "encounters",
    });
    onLoadSession?.();
  };

  return (
    <div className="p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-amber-400">Floor Encounters</h1>
        <p className="text-amber-100/70 max-w-2xl mx-auto text-sm">
          Safe havens, points of interest, and gate bosses across the Decennium&apos;s ten tiers.
        </p>
      </div>

      <Card className="bg-red-950/40 border-red-500/40">
        <CardContent className="py-4 flex gap-3 items-start">
          <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5 shrink-0" />
          <p className="text-sm text-red-100/90">{encounters.hornRule}</p>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-2">
        {tiers.map((t) => (
          <Button
            key={t.tier}
            size="sm"
            variant={selectedTier === t.tier ? "default" : "outline"}
            onClick={() => setSelectedTier(t.tier)}
            className={selectedTier === t.tier ? "bg-amber-600 hover:bg-amber-500" : ""}
          >
            T{t.tier}
            {!t.mapped && <span className="ml-1 opacity-60">*</span>}
          </Button>
        ))}
      </div>

      <div className="space-y-2 max-w-md">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-amber-200/50" />
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search tier, boss, havens & POIs…"
            className="pl-9 pr-9 bg-slate-900/60 border-amber-600/30 text-white"
          />
          {query && (
            <button
              type="button"
              onClick={clearFilters}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-amber-200/50 hover:text-amber-100"
              aria-label="Clear search"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
        {hasActiveFilters && (
          <div className="flex flex-wrap gap-1.5 items-center">
            <span className="text-xs text-amber-200/60">
              {matchingTiers.length} tier{matchingTiers.length === 1 ? "" : "s"} match
            </span>
            {matchingTiers.length > 0 && (
              <>
                <span className="text-xs text-amber-200/60">·</span>
                {matchingTiers.map((t) => (
                  <Button
                    key={t.tier}
                    size="sm"
                    variant={selectedTier === t.tier ? "default" : "outline"}
                    onClick={() => setSelectedTier(t.tier)}
                    className={`h-7 text-xs ${selectedTier === t.tier ? "bg-amber-600 hover:bg-amber-500" : ""}`}
                  >
                    T{t.tier}: {t.name}
                  </Button>
                ))}
              </>
            )}
            <Button
              type="button"
              size="sm"
              variant="ghost"
              onClick={clearFilters}
              className="h-7 text-xs text-amber-200/80 hover:text-amber-100"
            >
              Clear filters
            </Button>
          </div>
        )}
      </div>

      {hasActiveFilters && matchingTiers.length === 0 && (
        <Card className="bg-slate-900/70 border-amber-600/30">
          <CardContent className="py-6 text-center space-y-3">
            <p className="text-sm text-amber-100/70">
              No encounter tiers match &ldquo;{query.trim()}&rdquo;.
            </p>
            <Button type="button" size="sm" variant="outline" onClick={clearFilters}>
              Clear filters
            </Button>
          </CardContent>
        </Card>
      )}

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <CardTitle className="text-amber-300">
              Tier {tier.tier}: {tier.name}
            </CardTitle>
            <div className="flex gap-2">
              <Badge variant="outline" className="border-amber-500/50 text-amber-200">
                Floors {tier.floors}
              </Badge>
              {tier.difficulty && (
                <Badge className="bg-amber-700/80">{tier.difficulty}</Badge>
              )}
              {!tier.mapped && (
                <Badge variant="destructive">Unmapped depths</Badge>
              )}
              {tier.draftNote && (
                <Badge variant="outline" className="border-amber-500/50 text-amber-200">
                  Draft extract
                </Badge>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {tier.draftNote && (
            <p className="rounded border border-amber-600/30 bg-amber-950/20 p-2 text-xs leading-relaxed text-amber-100/70">
              {tier.draftNote}
            </p>
          )}
          <p className="text-sm text-amber-50/80 leading-relaxed">{tier.description}</p>
          <div className="flex items-center gap-2 text-amber-200">
            <Shield className="w-4 h-4" />
            <span className="text-sm font-medium">Gate boss: {tier.boss}</span>
          </div>
          {!tier.mapped && tier.gateBossSeed && (
            <div className="rounded border border-red-700/30 bg-red-950/20 p-2 text-xs space-y-1">
              <div className="text-red-300 font-medium">
                Gate seed: {tier.gateBossSeed.encounterTitle}
                <Badge variant="outline" className="ml-2 text-[9px] border-amber-500/40 text-amber-300/80">
                  Draft
                </Badge>
              </div>
              <p className="text-amber-50/70">{tier.gateBossSeed.description}</p>
            </div>
          )}
          {!tier.mapped && tier.encounterVibe && (
            <div className="rounded border border-sky-700/30 bg-sky-950/20 p-2 text-xs space-y-1">
              <div className="text-sky-300 font-medium">
                Encounter vibe
                <Badge variant="outline" className="ml-2 text-[9px] border-amber-500/40 text-amber-300/80">
                  Draft
                </Badge>
              </div>
              <p className="text-amber-50/70">{tier.encounterVibe.summary}</p>
            </div>
          )}
          <Button
            size="sm"
            className="bg-amber-600 hover:bg-amber-500"
            onClick={() => loadInSession()}
            aria-describedby="encounter-handoff-summary"
          >
            <Swords className="w-3 h-3 mr-1" />
            Load tier brief in Session
          </Button>
          <p id="encounter-handoff-summary" className="text-xs text-amber-100/60">
            Sends this tier&apos;s default site and fallback haven to Session. Choose a listed
            site or haven below to send that specific source entry instead.
          </p>
        </CardContent>
      </Card>

      {toolkitTier && (
        <Card className="bg-slate-900/70 border-amber-500/40">
          <CardHeader>
            <CardTitle className="text-amber-300 text-lg flex items-center gap-2">
              <Swords className="w-4 h-4" />
              T{tier.tier} Operational Toolkit
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <p className="text-xs text-amber-100/70 leading-relaxed">{toolkitXpStance}</p>
            <div className="flex flex-wrap gap-2 text-xs">
              <Badge variant="outline" className="border-amber-500/50 text-amber-200">
                {toolkitBudget.method}
              </Badge>
              <Badge variant="outline" className="border-amber-500/50 text-amber-200">
                ≤{toolkitBudget.eightActorRule.maxDetailedInitiativeActors} detailed actors
              </Badge>
              {toolkitGuardian && (
                <Badge className="bg-amber-800/80">
                  {toolkitGuardian.name}: {toolkitGuardian.type} CR {toolkitGuardian.challengeRating}
                </Badge>
              )}
            </div>
            {toolkitTier.corePressures && toolkitTier.corePressures.length > 0 && (
              <div>
                <div className="text-amber-200 font-medium mb-1">Core pressures</div>
                <ul className="list-disc list-inside text-xs text-amber-50/70 space-y-0.5">
                  {toolkitTier.corePressures.map((p) => (
                    <li key={p}>{p}</li>
                  ))}
                </ul>
              </div>
            )}
            <div>
              <div className="text-amber-200 font-medium mb-2">
                Encounter cards ({toolkitTier.encounterCards.length})
              </div>
              <div className="grid md:grid-cols-2 gap-2">
                {toolkitTier.encounterCards.map((c) => (
                  <div
                    key={c.id}
                    className="border border-amber-700/30 rounded-md p-2 text-xs space-y-1"
                  >
                    <div className="font-medium text-amber-100">
                      F{c.floors}: {c.title}
                    </div>
                    <div className="text-amber-200/80">
                      {c.job} · {c.targetBand}
                      {c.detailedActorBudget ? ` · actors ${c.detailedActorBudget}` : ""}
                    </div>
                    {c.summary && (
                      <p className="text-amber-50/70 leading-relaxed">{c.summary}</p>
                    )}
                    {c.rosterRef && (
                      <p className="text-amber-300/70">Roster: {c.rosterRef}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-amber-200 font-medium mb-2">
                Sample rosters ({toolkitTier.sampleRosters.length})
              </div>
              <div className="space-y-2">
                {toolkitTier.sampleRosters.map((r) => (
                  <div
                    key={r.id}
                    className="border border-amber-700/30 rounded-md p-2 text-xs space-y-1"
                  >
                    <div className="font-medium text-amber-100">{r.title}</div>
                    <div className="text-amber-200/80">
                      {r.job} · EV {r.targetPressureBand}
                    </div>
                    <ul className="text-amber-50/70 space-y-0.5">
                      {r.detailedActors.map((a, i) => (
                        <li key={`${r.id}-${i}`}>
                          {a.count}× {a.displayName} ({a.role}
                          {a.intendedCrBand ? `; CR band ${a.intendedCrBand}` : ""}
                          {a.bestiaryName ? `; bestiary: ${a.bestiaryName}` : ""}
                          {a.sandboxCr ? "; sandbox CR" : ""})
                        </li>
                      ))}
                    </ul>
                    {r.notes && <p className="text-amber-100/60 italic">{r.notes}</p>}
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {!tier.mapped && ((tier.regionNames?.length ?? 0) > 0 || (tier.hazards?.length ?? 0) > 0) && (
        <div className="grid md:grid-cols-2 gap-4">
          {(tier.regionNames?.length ?? 0) > 0 && (
            <Card className="bg-slate-900/70 border-violet-600/30">
              <CardHeader>
                <CardTitle className="text-violet-300 text-lg flex items-center gap-2">
                  Draft Regions ({tier.regionNames!.length})
                  <Badge variant="outline" className="text-[9px] border-amber-500/40 text-amber-300/80">
                    Draft
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {tier.regionNames!.map((r) => (
                  <div key={r.name} className="border border-violet-700/30 rounded-md p-3">
                    <div className="font-medium text-violet-200 mb-1">{r.name}</div>
                    <p className="text-xs text-amber-50/70 leading-relaxed">{r.note}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
          {(tier.hazards?.length ?? 0) > 0 && (
            <Card className="bg-slate-900/70 border-orange-600/30">
              <CardHeader>
                <CardTitle className="text-orange-300 text-lg flex items-center gap-2">
                  Draft Hazards ({tier.hazards!.length})
                  <Badge variant="outline" className="text-[9px] border-amber-500/40 text-amber-300/80">
                    Draft
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {tier.hazards!.map((h) => (
                  <div key={h.name} className="border border-orange-700/30 rounded-md p-3">
                    <div className="font-medium text-orange-200 mb-1">{h.name}</div>
                    <p className="text-xs text-amber-50/70 leading-relaxed">{h.description}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        <Card className="bg-slate-900/70 border-emerald-600/30">
          <CardHeader>
            <CardTitle className="text-emerald-300 text-lg flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Safe Havens ({filtered.safeHavens.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {filtered.safeHavens.length === 0 ? (
              <div className="space-y-2">
                <p className="text-sm text-amber-100/50 italic">
                  {tier.mapped
                    ? "No matching havens."
                    : "No confirmed havens past the Canticle Gate. Survivors disagree on what still stands."}
                </p>
                {hasActiveFilters && (
                  <Button type="button" size="sm" variant="ghost" onClick={clearFilters} className="h-7 px-0 text-xs text-amber-200/80 hover:text-amber-100">
                    Clear filters
                  </Button>
                )}
              </div>
            ) : (
              filtered.safeHavens.map((h) => (
                <div key={h.name} className="border border-emerald-700/30 rounded-md p-3">
                  <div className="font-medium text-emerald-200 mb-1">{h.name}</div>
                  <p className="text-xs text-amber-50/70 leading-relaxed">{h.description}</p>
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    onClick={() => loadInSession({ haven: h })}
                    className="mt-2 h-7 px-0 text-xs text-emerald-200/80 hover:text-emerald-100"
                  >
                    <Swords className="w-3 h-3 mr-1" />
                    Use as fallback haven in Session
                  </Button>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-sky-600/30">
          <CardHeader>
            <CardTitle className="text-sky-300 text-lg flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Points of Interest ({filtered.pointsOfInterest.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {filtered.pointsOfInterest.length === 0 ? (
              <div className="space-y-2">
                <p className="text-sm text-amber-100/50 italic">
                  {tier.mapped ? "No matching points of interest." : "Uncharted. Bring your own map — and a way back."}
                </p>
                {hasActiveFilters && (
                  <Button type="button" size="sm" variant="ghost" onClick={clearFilters} className="h-7 px-0 text-xs text-amber-200/80 hover:text-amber-100">
                    Clear filters
                  </Button>
                )}
              </div>
            ) : (
              filtered.pointsOfInterest.map((p) => (
                <div key={p.name} className="border border-sky-700/30 rounded-md p-3">
                  <div className="font-medium text-sky-200 mb-1">{p.name}</div>
                  <p className="text-xs text-amber-50/70 leading-relaxed">{p.description}</p>
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    onClick={() => loadInSession({ site: p })}
                    className="mt-2 h-7 px-0 text-xs text-sky-200/80 hover:text-sky-100"
                  >
                    <Swords className="w-3 h-3 mr-1" />
                    Use as site in Session
                  </Button>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
