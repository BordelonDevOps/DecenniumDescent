'use client';

import React, { useMemo, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import {
  Castle,
  Shield,
  ArrowUp,
  ArrowDown,
  RotateCcw,
  AlertTriangle,
  Coins,
  Hammer,
  Heart,
  MapPin,
  Search,
  X,
} from 'lucide-react';
import { Input } from './ui/input';
import { Button } from './ui/button';
import encounters from '@/data/floor-encounters.json';
import dungeonMechanics from '@/data/dungeon-mechanics.json';
import haven from '@/data/haven.json';
import { DirectorCosmologyNotes, PlayerCosmologyNotes, QualifiedCycleTimeline } from './CosmologyReadingNotes';

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
type TierData = {
  tier: number;
  name: string;
  floors: string;
  description: string;
  boss: string;
  difficulty?: string;
  mapped?: boolean;
  draft?: boolean;
  draftNote?: string;
  regionNames?: DraftRegion[];
  hazards?: DraftHazard[];
  gateBossSeed?: GateBossSeed;
  encounterVibe?: EncounterVibe;
  safeHavens: Haven[];
  pointsOfInterest: Haven[];
};

type TierVictoryConsequence = {
  tier: number;
  zone: string;
  boss: string;
  consequence: string;
};

type EntryClassesView = {
  draft: boolean;
  eligible: string[];
  policy: string | null;
};

type VictoryConsequencesView = {
  draft: boolean;
  summary: string;
  byTier: TierVictoryConsequence[];
};

function DraftBadge() {
  return (
    <span
      className="inline-flex items-center rounded-md border font-semibold ml-2 text-[9px] px-1 py-0 border-amber-500/40 text-amber-300/80 align-middle"
    >
      Draft
    </span>
  );
}

/** Accept legacy string[] or { draft, eligible[], policy }. */
function normalizeEntryClasses(raw: unknown): EntryClassesView {
  if (Array.isArray(raw)) {
    return {
      draft: false,
      eligible: raw.filter((c): c is string => typeof c === 'string'),
      policy: null,
    };
  }
  if (raw && typeof raw === 'object') {
    const o = raw as Record<string, unknown>;
    return {
      draft: Boolean(o.draft),
      eligible: Array.isArray(o.eligible)
        ? o.eligible.filter((c): c is string => typeof c === 'string')
        : [],
      policy: typeof o.policy === 'string' ? o.policy : null,
    };
  }
  return { draft: false, eligible: [], policy: null };
}

/** Accept legacy string or { draft, summary, byTier[] }. */
function normalizeVictoryConsequences(raw: unknown): VictoryConsequencesView {
  if (typeof raw === 'string') {
    return { draft: false, summary: raw, byTier: [] };
  }
  if (raw && typeof raw === 'object') {
    const o = raw as Record<string, unknown>;
    const byTier = Array.isArray(o.byTier)
      ? o.byTier
          .filter((v): v is Record<string, unknown> => Boolean(v) && typeof v === 'object')
          .map((v) => ({
            tier: typeof v.tier === 'number' ? v.tier : 0,
            zone: typeof v.zone === 'string' ? v.zone : '',
            boss: typeof v.boss === 'string' ? v.boss : '',
            consequence: typeof v.consequence === 'string' ? v.consequence : '',
          }))
          .filter((v) => v.tier > 0)
      : [];
    return {
      draft: Boolean(o.draft),
      summary: typeof o.summary === 'string' ? o.summary : '',
      byTier,
    };
  }
  return { draft: false, summary: '', byTier: [] };
}

function tierSearchHaystack(tier: TierData): string {
  const parts = [
    tier.name,
    tier.boss,
    tier.floors,
    tier.description,
    tier.draftNote ?? '',
    tier.difficulty ?? '',
    tier.gateBossSeed?.encounterTitle ?? '',
    tier.gateBossSeed?.description ?? '',
    tier.encounterVibe?.summary ?? '',
    ...(tier.encounterVibe?.tags ?? []),
    ...(tier.regionNames?.flatMap((r) => [r.name, r.note]) ?? []),
    ...(tier.hazards?.flatMap((h) => [h.name, h.description]) ?? []),
    ...tier.safeHavens.flatMap((h) => [h.name, h.description]),
    ...tier.pointsOfInterest.flatMap((p) => [p.name, p.description]),
  ];
  return parts.join(' ').toLowerCase();
}

const DungeonGuide: React.FC = () => {
  const dungeonTiers = encounters.tiers as TierData[];
  const [selectedTier, setSelectedTier] = useState<number>(1);
  const [activeTab, setActiveTab] = useState<'overview' | 'tiers' | 'mechanics'>('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [mappedOnly, setMappedOnly] = useState(false);

  const query = searchQuery.trim().toLowerCase();
  const hasActiveFilters = query.length > 0 || mappedOnly;

  const filteredTiers = useMemo(() => {
    return dungeonTiers.filter((tier) => {
      if (mappedOnly && !tier.mapped) return false;
      if (!query) return true;
      return tierSearchHaystack(tier).includes(query);
    });
  }, [dungeonTiers, query, mappedOnly]);

  const filteredGateBosses = useMemo(() => {
    if (!query) return dungeonMechanics.gateBosses;
    return dungeonMechanics.gateBosses.filter((b) =>
      `${b.name} ${b.zone} ${b.floors} tier ${b.tier}`.toLowerCase().includes(query)
    );
  }, [query]);

  const filteredVictoryByTier = useMemo(() => {
    const all = normalizeVictoryConsequences(dungeonMechanics.cycle.victoryConsequences).byTier;
    if (!query) return all;
    return all.filter((v) =>
      `${v.zone} ${v.boss} ${v.consequence} tier ${v.tier}`.toLowerCase().includes(query)
    );
  }, [query]);

  const current = useMemo(() => {
    const inFilter = filteredTiers.find((t) => t.tier === selectedTier);
    if (inFilter) return inFilter;
    return filteredTiers[0] ?? dungeonTiers.find((t) => t.tier === selectedTier) ?? dungeonTiers[0];
  }, [dungeonTiers, filteredTiers, selectedTier]);

  const clearFilters = () => {
    setSearchQuery('');
    setMappedOnly(false);
  };

  const entryClasses = useMemo(
    () => normalizeEntryClasses(dungeonMechanics.cycle.entryClasses),
    []
  );
  const victoryConsequences = useMemo(
    () => normalizeVictoryConsequences(dungeonMechanics.cycle.victoryConsequences),
    []
  );

  return (
    <div className="space-y-6 p-6">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-amber-400">Dungeon Guide</h2>
        <p className="text-amber-200/80 max-w-2xl mx-auto">
          The Decennium reshapes each Cycle when the Shardspire activates — but the 10-year rotation,
          1200-hour horn, and expedition structure remain.
        </p>
      </div>

      <Card className="bg-red-950/40 border-red-500/40">
        <CardContent className="py-4 flex gap-3 items-start">
          <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5 shrink-0" />
          <p className="text-sm text-red-100/90">{dungeonMechanics.hornRule}</p>
        </CardContent>
      </Card>

      <Card className="bg-slate-800/50 border-amber-600/30">
        <CardContent className="py-4 space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-amber-400/60 w-4 h-4" />
            <Input
              type="text"
              placeholder="Search tiers, bosses, havens, POIs, gate bosses…"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-9 bg-slate-950/60 border-amber-600/30 text-amber-50 placeholder:text-amber-200/40"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-amber-200/50 hover:text-amber-100"
                aria-label="Clear search"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <button
              type="button"
              onClick={() => setMappedOnly((v) => !v)}
              className={`px-2 py-1 rounded border ${
                mappedOnly
                  ? 'bg-amber-600 border-amber-400 text-white'
                  : 'bg-slate-900 border-amber-600/30 text-amber-100/80'
              }`}
            >
              Mapped tiers only
            </button>
            {hasActiveFilters && (
              <>
                <span className="text-amber-200/60">
                  {filteredTiers.length} tier{filteredTiers.length === 1 ? '' : 's'} match
                </span>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                  className="h-7 text-xs text-amber-200/80 hover:text-amber-100"
                >
                  Clear filters
                </Button>
              </>
            )}
          </div>
        </CardContent>
      </Card>

      <Tabs value={activeTab} onValueChange={(value: string) => setActiveTab(value as typeof activeTab)}>
        <TabsList className="grid w-full grid-cols-3 bg-amber-600/20 border border-amber-600/30">
          <TabsTrigger value="overview" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <MapPin className="w-4 h-4 mr-2" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="tiers" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <Castle className="w-4 h-4 mr-2" />
            Tier Details
          </TabsTrigger>
          <TabsTrigger value="mechanics" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
            <Shield className="w-4 h-4 mr-2" />
            Mechanics
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <Card className="bg-emerald-950/30 border-emerald-500/40">
            <CardHeader>
              <CardTitle className="text-emerald-300 flex items-center gap-2">
                <Castle className="w-5 h-5" />
                {haven.name} — {haven.depth}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-emerald-50/80">{haven.careerMeaning}</p>
              <div className="grid md:grid-cols-2 gap-3">
                {haven.districts.map((district) => (
                  <div key={district.name} className="rounded border border-emerald-700/30 bg-slate-950/30 p-3">
                    <div className="font-semibold text-emerald-200">{district.name}</div>
                    <p className="text-xs text-emerald-50/70 mt-1">{district.function}</p>
                  </div>
                ))}
              </div>
              <div>
                <div className="font-semibold text-emerald-200 mb-2">Expedition standing</div>
                <div className="flex flex-wrap gap-2">
                  {haven.expeditionStanding.map((row) => (
                    <Badge key={row.depth} variant="outline" className="border-emerald-600/40 text-emerald-100">
                      {row.depth}: {row.meaning}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400 flex items-center gap-2">
                <Castle className="w-5 h-5" />
                The Decennium
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-amber-300">Core Principles</h3>
                  <ul className="space-y-2 text-amber-100/80">
                    <li className="flex items-start gap-2">
                      <RotateCcw className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Dungeon reshapes every 10-year Cycle</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ArrowDown className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Gate bosses bar deeper tiers until defeated</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <ArrowUp className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Free movement within conquered tiers</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <AlertTriangle className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Tiers 1–5 mapped; 6–10 are survivor rumor</span>
                    </li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-amber-300">Safe Haven System</h3>
                  <ul className="space-y-2 text-amber-100/80">
                    <li className="flex items-start gap-2">
                      <Heart className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Rest, repair, and steel nerves between floors</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <Coins className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Trading grows scarce with depth</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <Hammer className="w-4 h-4 mt-1 text-amber-400" />
                      <span>Salvage and craft from dungeon materials</span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3">
            {filteredTiers.length === 0 ? (
              <Card className="bg-slate-800/50 border-amber-600/30 col-span-full">
                <CardContent className="py-8 text-center space-y-3">
                  <p className="text-sm text-amber-100/70">No tier overviews match the current filters.</p>
                  <Button type="button" variant="outline" size="sm" onClick={clearFilters}>
                    Clear filters
                  </Button>
                </CardContent>
              </Card>
            ) : (
              filteredTiers.map((tier) => (
              <Card
                key={tier.tier}
                className={`cursor-pointer border transition-colors ${
                  selectedTier === tier.tier
                    ? 'bg-amber-900/40 border-amber-400'
                    : 'bg-slate-800/50 border-amber-600/20 hover:border-amber-500/50'
                }`}
                onClick={() => {
                  setSelectedTier(tier.tier);
                  setActiveTab('tiers');
                }}
              >
                <CardContent className="p-3 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="text-amber-300 font-semibold">Tier {tier.tier}</span>
                    {!tier.mapped && (
                      <Badge variant="outline" className="text-[10px] border-red-400/50 text-red-300">
                        {tier.draftNote ? 'Draft extract' : 'Unmapped'}
                      </Badge>
                    )}
                  </div>
                  <div className="text-sm text-white font-medium leading-snug">{tier.name}</div>
                  <div className="text-xs text-amber-100/60">Floors {tier.floors}</div>
                  <div className="text-xs text-amber-200/80 truncate">{tier.boss}</div>
                </CardContent>
              </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="tiers" className="space-y-4">
          {filteredTiers.length === 0 ? (
            <Card className="bg-slate-800/50 border-amber-600/30">
              <CardContent className="py-8 text-center space-y-3">
                <p className="text-sm text-amber-100/70">No tier details match the current filters.</p>
                <Button type="button" variant="outline" size="sm" onClick={clearFilters}>
                  Clear filters
                </Button>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="flex flex-wrap gap-2">
                {filteredTiers.map((t) => (
                  <button
                    key={t.tier}
                    type="button"
                    onClick={() => setSelectedTier(t.tier)}
                    className={`px-3 py-1 rounded text-sm border ${
                      selectedTier === t.tier
                        ? 'bg-amber-600 border-amber-400 text-white'
                        : 'bg-slate-800 border-amber-600/30 text-amber-100'
                    }`}
                  >
                    T{t.tier}
                  </button>
                ))}
              </div>

              <Card className="bg-slate-800/50 border-amber-600/30">
                <CardHeader>
                  <CardTitle className="text-amber-400">
                    Tier {current.tier}: {current.name}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline" className="border-amber-500/40 text-amber-200">
                      Floors {current.floors}
                    </Badge>
                    {current.difficulty && <Badge className="bg-amber-700/80">{current.difficulty}</Badge>}
                    {!current.mapped && (
                      <Badge variant="outline" className="text-[10px] border-red-400/50 text-red-300">
                        {current.draftNote ? 'Draft extract' : 'Unmapped rumor'}
                      </Badge>
                    )}
                    <Badge className="bg-slate-700">Boss: {current.boss}</Badge>
                  </div>
                  {!current.mapped && (
                    <p className="text-[10px] text-amber-200/50 italic">
                      Survivor-rumor content — POI/haven stubs from tier prose only. Gate boss HP in Session uses tier formula until bestiary wired.
                    </p>
                  )}
                  {!current.mapped && current.draftNote && (
                    <div className="flex gap-2 rounded border border-amber-500/30 bg-amber-950/20 p-3 text-xs text-amber-100/70">
                      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-300" />
                      <div>
                        <span className="font-medium text-amber-200">Draft extract.</span> {current.draftNote}
                      </div>
                    </div>
                  )}
                  <p className="text-sm text-amber-50/80 leading-relaxed">{current.description}</p>

                  {!current.mapped && current.regionNames && current.regionNames.length > 0 && (
                    <div>
                      <h4 className="text-violet-300 font-semibold mb-2 flex items-center gap-2">
                        Draft Regions
                        <DraftBadge />
                      </h4>
                      <ul className="space-y-2">
                        {current.regionNames.map((r) => (
                          <li key={r.name} className="text-sm border border-violet-700/30 rounded p-2">
                            <div className="text-violet-200 font-medium">{r.name}</div>
                            <div className="text-xs text-amber-50/70 mt-1">{r.note}</div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {!current.mapped && current.hazards && current.hazards.length > 0 && (
                    <div>
                      <h4 className="text-orange-300 font-semibold mb-2 flex items-center gap-2">
                        Draft Hazards
                        <DraftBadge />
                      </h4>
                      <ul className="space-y-2">
                        {current.hazards.map((h) => (
                          <li key={h.name} className="text-sm border border-orange-700/30 rounded p-2">
                            <div className="text-orange-200 font-medium">{h.name}</div>
                            <div className="text-xs text-amber-50/70 mt-1">{h.description}</div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {!current.mapped && current.gateBossSeed && (
                    <div className="rounded border border-red-700/30 bg-red-950/20 p-3 space-y-1">
                      <h4 className="text-red-300 font-semibold text-sm flex items-center gap-2">
                        Gate Boss Seed
                        <DraftBadge />
                      </h4>
                      <div className="text-sm text-red-100/90 font-medium">
                        {current.gateBossSeed.name}
                        <span className="text-amber-200/70 font-normal">
                          {' '}
                          — {current.gateBossSeed.encounterTitle}
                        </span>
                      </div>
                      <p className="text-xs text-amber-50/70">{current.gateBossSeed.description}</p>
                    </div>
                  )}

                  {!current.mapped && current.encounterVibe && (
                    <div className="rounded border border-sky-700/30 bg-sky-950/20 p-3 space-y-2">
                      <h4 className="text-sky-300 font-semibold text-sm flex items-center gap-2">
                        Encounter Vibe
                        <DraftBadge />
                      </h4>
                      <p className="text-xs text-amber-50/80">{current.encounterVibe.summary}</p>
                      {current.encounterVibe.tags && current.encounterVibe.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {current.encounterVibe.tags.map((tag) => (
                            <Badge
                              key={tag}
                              variant="outline"
                              className="text-[10px] border-sky-500/40 text-sky-200/80"
                            >
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-emerald-300 font-semibold mb-2">Safe Havens</h4>
                      {current.safeHavens.length === 0 ? (
                        <p className="text-sm text-amber-100/50 italic">None confirmed for this tier.</p>
                      ) : (
                        <ul className="space-y-2">
                          {current.safeHavens.map((h) => (
                            <li key={h.name} className="text-sm border border-emerald-700/30 rounded p-2">
                              <div className="text-emerald-200 font-medium">{h.name}</div>
                              <div className="text-xs text-amber-50/70 mt-1">{h.description}</div>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                    <div>
                      <h4 className="text-sky-300 font-semibold mb-2">Points of Interest</h4>
                      {current.pointsOfInterest.length === 0 ? (
                        <p className="text-sm text-amber-100/50 italic">None confirmed for this tier.</p>
                      ) : (
                        <ul className="space-y-2">
                          {current.pointsOfInterest.map((p) => (
                            <li key={p.name} className="text-sm border border-sky-700/30 rounded p-2">
                              <div className="text-sky-200 font-medium">{p.name}</div>
                              <div className="text-xs text-amber-50/70 mt-1">{p.description}</div>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        <TabsContent value="mechanics" className="space-y-4">
          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400">The Cycle &amp; Shardspire</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-amber-50/80">
              <p>{dungeonMechanics.cycle.rotation}</p>
              <p>{dungeonMechanics.cycle.calendar}</p>
              {victoryConsequences.summary && (
                <p>
                  <strong className="text-amber-300">Victory:</strong> {victoryConsequences.summary}
                  {victoryConsequences.draft && <DraftBadge />}
                </p>
              )}
              <div>
                <strong className="text-amber-300">Classes of Entry</strong>
                {entryClasses.draft && <DraftBadge />}
                {entryClasses.policy && (
                  <p className="text-xs text-amber-100/60 mt-1">{entryClasses.policy}</p>
                )}
                {entryClasses.eligible.length > 0 ? (
                  <ul className="list-disc pl-5 mt-1 space-y-1 columns-2">
                    {entryClasses.eligible.map((c) => (
                      <li key={c}>{c}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-amber-100/50 italic mt-1">No entry classes listed.</p>
                )}
              </div>
              {victoryConsequences.byTier.length > 0 && (
                <div>
                  <strong className="text-amber-300">Victory Consequences by Tier</strong>
                  {victoryConsequences.draft && <DraftBadge />}
                  {(query ? filteredVictoryByTier : victoryConsequences.byTier).length === 0 ? (
                    <div className="mt-2 rounded border border-amber-700/20 p-3 text-xs text-amber-100/60">
                      <p>No victory consequences match the current search.</p>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={clearFilters}
                        className="mt-1 h-7 px-2 text-xs text-amber-200/80 hover:text-amber-100"
                      >
                        Clear filters
                      </Button>
                    </div>
                  ) : (
                    <ul className="space-y-2 mt-1">
                      {(query ? filteredVictoryByTier : victoryConsequences.byTier).map((v) => (
                        <li key={v.tier} className="text-xs border border-amber-700/20 rounded p-2">
                          <span className="text-amber-300 font-medium">
                            T{v.tier} — {v.zone} ({v.boss}):
                          </span>{' '}
                          {v.consequence}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400">Expedition ({dungeonMechanics.expedition.maxSize} max)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-amber-50/80">
              <p>{dungeonMechanics.expedition.summary}</p>
              <div className="grid sm:grid-cols-2 gap-2">
                {dungeonMechanics.expedition.teams.map((t) => (
                  <div key={t.name} className="border border-amber-700/30 rounded p-2">
                    <div className="text-amber-300 font-medium">{t.name} <span className="text-amber-100/50">({t.size})</span></div>
                    <div className="text-xs text-amber-100/70">{t.function}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400">Gate Bosses (lorebook reference)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-amber-50/80">
              {filteredGateBosses.length === 0 ? (
                <p className="text-xs text-amber-100/50 italic">No gate bosses match the current search.</p>
              ) : (
                filteredGateBosses.map((b) => (
                  <p key={b.tier}>
                    <strong>T{b.tier}:</strong> {b.name} — {b.zone} (floors {b.floors})
                    {'draft' in b && b.draft && (
                      <>
                        {' '}
                        <DraftBadge />
                        {'encounterTitle' in b && b.encounterTitle && (
                          <span className="text-amber-100/70"> · {String(b.encounterTitle)}</span>
                        )}
                      </>
                    )}
                  </p>
                ))
              )}
              <p className="text-xs text-amber-200/60 pt-2">
                Tier 1–5 floor bosses in the Tier Details tab come from Floor Encounters.docx; tiers 6–10 carry draft extract seeds (regions, hazards, encounter vibe) — not mapped canon.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-amber-600/30">
            <CardHeader>
              <CardTitle className="text-amber-400">Myth & Timeline</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-amber-50/80">
              <PlayerCosmologyNotes />
              <QualifiedCycleTimeline />
              <details className="border-t border-amber-600/30 pt-3">
                <summary className="cursor-pointer text-amber-300 focus-visible:outline focus-visible:outline-2">
                  Director / source reference — original myth and timeline
                </summary>
                <div className="space-y-4 pt-4">
                  <DirectorCosmologyNotes />
                  <ul className="list-disc pl-5 space-y-1">
                    {dungeonMechanics.cycle.mythHistory.map((m) => (
                      <li key={m.slice(0, 48)}>{m}</li>
                    ))}
                  </ul>
                  <ul className="list-disc pl-5 space-y-1 text-amber-100/70">
                    {dungeonMechanics.timeline.map((t) => (
                      <li key={t}>{t}</li>
                    ))}
                  </ul>
                </div>
              </details>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DungeonGuide;
