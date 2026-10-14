"use client";

import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  activeReputationEntries,
  factionsForEditor,
  tierFromScore,
  tierLabel,
} from "@/data/reputation";

type ReputationScores = Record<string, number>;

type ReputationPanelProps = {
  scores: ReputationScores;
  onChange: (next: ReputationScores) => void;
  /** Compact: only non-zero factions; full: all factions grouped */
  mode?: "compact" | "full";
  readOnly?: boolean;
  className?: string;
};

function tierBadgeClass(tierId: string) {
  switch (tierId) {
    case "proscribed":
    case "hunted":
    case "hostile":
      return "bg-red-950 text-red-200 border-red-700/50";
    case "distrusted":
    case "unwelcome":
      return "bg-orange-950 text-orange-200 border-orange-700/50";
    case "recognized":
    case "favored":
    case "trusted":
      return "bg-emerald-950 text-emerald-200 border-emerald-700/50";
    case "champion":
    case "authority":
      return "bg-amber-900 text-amber-100 border-amber-600/50";
    default:
      return "bg-slate-800 text-slate-200 border-slate-600/50";
  }
}

export default function ReputationPanel({
  scores,
  onChange,
  mode = "full",
  readOnly = false,
  className = "",
}: ReputationPanelProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");

  const entries =
    mode === "compact"
      ? activeReputationEntries(scores)
      : factionsForEditor().map((faction) => ({
          factionId: faction.id,
          faction,
          score: scores[faction.id] ?? 0,
          tier: tierFromScore(scores[faction.id] ?? 0),
        }));

  const visible =
    mode === "compact"
      ? entries
      : entries.filter((e) => e.score !== 0 || !readOnly);

  const categories = useMemo(() => {
    const cats = new Set<string>();
    for (const e of entries) {
      if (e.faction?.category) cats.add(e.faction.category);
    }
    return [...cats].sort();
  }, [entries]);

  const filtered = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return visible.filter(({ faction }) => {
      if (!faction) return false;
      if (categoryFilter !== "All" && faction.category !== categoryFilter) return false;
      if (!q) return true;
      const haystack = [faction.name, faction.category, faction.description ?? ""]
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [visible, searchQuery, categoryFilter]);

  const hasActiveFilters = searchQuery.trim() !== "" || categoryFilter !== "All";

  const clearFilters = () => {
    setSearchQuery("");
    setCategoryFilter("All");
  };

  if (readOnly && visible.length === 0) {
    return (
      <p className={`text-xs text-amber-100/50 ${className}`}>
        No faction standing recorded — Neutral with all groups (0).
      </p>
    );
  }

  if (!readOnly && visible.length === 0) {
    return (
      <p className={`text-xs text-amber-100/50 ${className}`}>
        No faction standing yet — pick a background in Character Builder, or use the full editor there.
      </p>
    );
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {mode === "full" && visible.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 pb-1">
          <Input
            type="search"
            placeholder="Search factions…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-7 flex-1 min-w-[8rem] text-xs bg-black/30 border-amber-700/40 text-amber-100 placeholder:text-amber-200/35"
            aria-label="Search factions"
          />
          <Select value={categoryFilter} onValueChange={setCategoryFilter}>
            <SelectTrigger className="h-7 w-[9.5rem] text-xs bg-black/30 border-amber-700/40 text-amber-100">
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="All">All categories</SelectItem>
              {categories.map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {cat}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {hasActiveFilters && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="h-7 px-2 text-[10px] text-amber-200/70 hover:text-amber-100"
              onClick={clearFilters}
            >
              Clear
            </Button>
          )}
        </div>
      )}
      {hasActiveFilters && filtered.length === 0 && (
        <p className="text-xs text-amber-100/50">No factions match your filters.</p>
      )}
      {filtered.map(({ factionId, faction, score, tier }) => {
        if (!faction) return null;
        return (
          <div
            key={factionId}
            className="flex flex-wrap items-center gap-2 justify-between border border-amber-800/30 rounded px-2 py-1.5 bg-black/20"
          >
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="text-xs font-medium text-amber-100">{faction.name}</span>
                {faction.draft && (
                  <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 border-amber-600/40 text-amber-300/70">
                    draft
                  </Badge>
                )}
                {faction.resonanceTrack && (
                  <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 border-purple-600/40 text-purple-200/80">
                    RP track
                  </Badge>
                )}
              </div>
              {mode === "full" && faction.description && (
                <p className="text-[10px] text-amber-100/45 mt-0.5 line-clamp-1">{faction.description}</p>
              )}
            </div>
            <div className="flex items-center gap-1.5 shrink-0">
              {!readOnly && (
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  className="h-7 w-7 p-0 border-amber-700/40"
                  onClick={() =>
                    onChange({
                      ...scores,
                      [factionId]: Math.max(-5, score - 1),
                    })
                  }
                  aria-label={`Decrease ${faction.name} reputation`}
                >
                  −
                </Button>
              )}
              <Badge className={`text-[10px] min-w-[4.5rem] justify-center ${tierBadgeClass(tier.id)}`}>
                {tier.label}
                {!readOnly && <span className="ml-1 opacity-60">({score})</span>}
              </Badge>
              {!readOnly && (
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  className="h-7 w-7 p-0 border-amber-700/40"
                  onClick={() =>
                    onChange({
                      ...scores,
                      [factionId]: Math.min(5, score + 1),
                    })
                  }
                  aria-label={`Increase ${faction.name} reputation`}
                >
                  +
                </Button>
              )}
            </div>
          </div>
        );
      })}
      {!readOnly && mode === "full" && (
        <p className="text-[10px] text-amber-200/45 pt-1">
          Scores −5…+5 map to Proscribed → Authority. Standing changes access, trust, training opportunities, and story consequences; it never changes the intrinsic physics of Resonance or spell cost.
          {" "}
          <span className="text-amber-200/35">
            Umbrin: no fixed race lock — civic/mainstream bias is narrative; Murk expediency may yield strange alliances (Underworld, Planar Trading Guilds, Corruption Scholars, Anti-Cult Alliances).
          </span>
        </p>
      )}
      {readOnly && mode === "compact" && filtered.length > 0 && (
        <p className="text-[10px] text-amber-200/45">
          {filtered.map((e) => `${e.faction!.name}: ${tierLabel(e.score)}`).join(" · ")}
        </p>
      )}
    </div>
  );
}
