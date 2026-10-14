"use client";

import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dice5, Sparkles, Map, Users, Coins, Home, Swords, Copy, X } from "lucide-react";
import encounters from "@/data/floor-encounters.json";
import craftingRecipes from "@/data/crafting-recipes.json";
import { builderRaces } from "@/data/builder-races";
import { pushEncounterHandoff } from "@/lib/session-handoff";

function roll(sides: number) {
  return 1 + Math.floor(Math.random() * sides);
}

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

const nameBits = {
  prefixes: ["Ash", "Bloom", "Canticle", "Dusk", "Echo", "Forge", "Gloam", "Hearth", "Iron", "Lumen", "Murk", "Nexus", "Oath", "Obsidian", "Pyre", "Quiet", "Rune", "Shadow", "Shard", "Thorn", "Veil", "Warden"],
  middles: ["born", "bound", "caller", "deep", "fall", "heart", "keep", "light", "mere", "shade", "song", "spire", "stone", "thread", "wake", "weave"],
  suffixes: ["ael", "an", "ar", "eth", "ia", "ion", "is", "or", "us", "yn"],
};

const umbrinLoreTags = ["Murk exile", "Obsidian Burn (draft)", "Umbra faith", "strange alliances"];

const umbrinNameHints = ["Murk", "Gloam", "Obsidian", "Shadow", "Veil", "Night", "deep"];

function isUmbrinFlavoredName(n: string): boolean {
  const lower = n.toLowerCase();
  return umbrinNameHints.some((h) => lower.includes(h.toLowerCase()));
}

const hooks = [
  "A haven's lanterns dim as something older than the Automatons listens.",
  "A merchant sells a key that only works if you already regret using it.",
  "Your party's Resonance spikes — the Weave is remembering your names.",
  "A rival expedition offers alliance… until the next Gate Warden.",
  "A map appears that shows floors that should not exist this Cycle.",
  "Someone in the party hears the First Song under the ambient noise.",
  "A salvage crate ticks. Inside: a still-warm Automaton heart.",
  "The horn is still days away — but something answers it early.",
];

type Tier = {
  tier: number;
  name: string;
  boss: string;
  floors: string;
  mapped?: boolean;
  safeHavens: { name: string; description: string }[];
  pointsOfInterest: { name: string; description: string }[];
};

type GeneratorsPanelProps = {
  onLoadSession?: () => void;
};

export default function GeneratorsPanel({ onLoadSession }: GeneratorsPanelProps) {
  const [dice, setDice] = useState("d20");
  const [diceResult, setDiceResult] = useState<number | null>(null);
  const [name, setName] = useState("");
  const [hook, setHook] = useState("");
  const [poi, setPoi] = useState("");
  const [haven, setHaven] = useState("");
  const [loot, setLoot] = useState("");
  const [pack, setPack] = useState("");
  const [peopleSpark, setPeopleSpark] = useState("");
  const [peopleLoreTags, setPeopleLoreTags] = useState<string[]>([]);
  const [lastSpark, setLastSpark] = useState("");
  const [nameLoreHint, setNameLoreHint] = useState(false);
  const [count, setCount] = useState(4);
  const [tierPick, setTierPick] = useState(1);
  const [copyStatus, setCopyStatus] = useState<"copied" | "failed" | null>(null);
  const [handoffStatus, setHandoffStatus] = useState<"ready" | "failed" | null>(null);

  const sides = Number(dice.replace("d", "")) || 20;
  const tiers = encounters.tiers as Tier[];

  const mappedPois = useMemo(
    () =>
      tiers.flatMap((t) =>
        t.pointsOfInterest.map((p) => ({ ...p, tier: t.tier, tierName: t.name }))
      ),
    [tiers]
  );

  const mappedHavens = useMemo(
    () =>
      tiers.flatMap((t) =>
        t.safeHavens.map((h) => ({ ...h, tier: t.tier, tierName: t.name }))
      ),
    [tiers]
  );

  const recipes = craftingRecipes as { name: string; skill: string; rarity: string }[];

  const genName = () => {
    const generated = `${pick(nameBits.prefixes)}${pick(nameBits.middles)}${pick(nameBits.suffixes)}`;
    setName(generated);
    setNameLoreHint(isUmbrinFlavoredName(generated));
  };

  const clearSparks = () => {
    setHook("");
    setPoi("");
    setHaven("");
    setPeopleSpark("");
    setPeopleLoreTags([]);
    setLoot("");
    setLastSpark("");
    setCopyStatus(null);
  };

  const copyLastSpark = async () => {
    try {
      await navigator.clipboard.writeText(lastSpark);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
  };

  const genHook = () => {
    const next = pick(hooks);
    setHook(next);
    setLastSpark(next);
  };

  const genPoi = () => {
    const pool = mappedPois.filter((p) => p.tier === tierPick);
    const use = pool.length ? pool : mappedPois;
    if (!use.length) {
      setPoi("No POI data.");
      setLastSpark("No POI data.");
      return;
    }
    const p = pick(use);
    const next = `T${p.tier} ${p.tierName} — ${p.name}: ${p.description}`;
    setPoi(next);
    setLastSpark(next);
  };

  const genHaven = () => {
    const pool = mappedHavens.filter((h) => h.tier === tierPick);
    const use = pool.length ? pool : mappedHavens;
    if (!use.length) {
      setHaven("No haven data for that band.");
      setLastSpark("No haven data for that band.");
      return;
    }
    const h = pick(use);
    const next = `T${h.tier} ${h.tierName} — ${h.name}: ${h.description}`;
    setHaven(next);
    setLastSpark(next);
  };

  const genLoot = () => {
    const r = pick(recipes);
    const gold = roll(20) * tierPick * 5;
    const next = `${r.name} (${r.skill}, ${r.rarity || "Common"}) · salvage value ~${gold} gp · Tier ${tierPick} find`;
    setLoot(next);
    setLastSpark(next);
  };

  const genPeople = () => {
    const racePool = builderRaces.filter((r) => r.name);
    if (!racePool.length) {
      setPeopleSpark("No people data.");
      setLastSpark("No people data.");
      return;
    }
    const race = pick(racePool);
    const lineage = race.subraces?.length ? pick(race.subraces) : "";
    const isUmbrin = race.name === "Umbrin";
    setPeopleLoreTags(isUmbrin ? umbrinLoreTags : []);
    const next = lineage
      ? `${race.name} (${lineage}) — ${race.info.slice(0, 120)}${race.info.length > 120 ? "…" : ""}`
      : `${race.name} — ${race.info.slice(0, 140)}${race.info.length > 140 ? "…" : ""}`;
    setPeopleSpark(next);
    setLastSpark(next);
  };

  const genParty = () => {
    const roles = ["Striker", "Warden", "Herald", "Infiltrator", "Support", "Artisan"];
    const picks = Array.from({ length: Math.max(1, Math.min(8, count)) }, () => pick(roles));
    setHook(`Party seed (${picks.length}): ${picks.join(" · ")}`);
  };

  const genEncounterPack = () => {
    const t = tiers.find((x) => x.tier === tierPick) || tiers[0];
    const poiLine = t.pointsOfInterest.length ? pick(t.pointsOfInterest).name : "Uncharted chamber";
    const havenLine = t.safeHavens.length ? pick(t.safeHavens).name : "No confirmed haven";
    const pressure = pick([
      "time pressure (horn clock)",
      "rival party",
      "environmental hazard",
      "Resonance spike",
      "broken Automaton patrol",
    ]);
    setPack(
      [
        `Tier ${t.tier}: ${t.name} (Floors ${t.floors})`,
        `Site: ${poiLine}`,
        `Fallback haven: ${havenLine}`,
        `Gate shadow: ${t.boss}`,
        `Twist: ${pressure}`,
        `Hook: ${pick(hooks)}`,
      ].join("\n")
    );
    setHandoffStatus(null);
  };

  const loadPackInSession = () => {
    if (!pack) return;
    const t = tiers.find((x) => x.tier === tierPick) || tiers[0];
    try {
      pushEncounterHandoff({
        tier: t.tier,
        tierName: t.name,
        boss: t.boss,
        floors: t.floors,
        brief: pack,
        source: "generators",
      });
      setHandoffStatus("ready");
      onLoadSession?.();
    } catch {
      setHandoffStatus("failed");
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-amber-400">Generators</h1>
        <p className="text-amber-100/70 text-sm max-w-xl mx-auto">
          Table tools for Aethel — dice, names, havens, loot sparks, and full encounter packs.
        </p>
      </div>

      <div className="flex flex-wrap gap-2 justify-center">
        {tiers.map((t) => (
          <Button
            key={t.tier}
            size="sm"
            variant={tierPick === t.tier ? "default" : "outline"}
            className={tierPick === t.tier ? "bg-amber-600" : ""}
            onClick={() => {
              setTierPick(t.tier);
              setPack("");
              setHandoffStatus(null);
            }}
          >
            T{t.tier}
          </Button>
        ))}
      </div>

      {lastSpark && (
        <div className="flex flex-wrap gap-2 justify-center">
          <Button
            size="sm"
            variant="outline"
            onClick={() => void copyLastSpark()}
          >
            <Copy className="w-3 h-3 mr-1" /> Copy last spark
          </Button>
          <Button size="sm" variant="ghost" className="text-amber-100/60" onClick={clearSparks}>
            <X className="w-3 h-3 mr-1" /> Clear sparks
          </Button>
        </div>
      )}
      {copyStatus && (
        <p className={`text-center text-xs ${copyStatus === "copied" ? "text-emerald-200/80" : "text-red-200/80"}`} role="status">
          {copyStatus === "copied"
            ? "Last spark copied."
            : "Could not copy this spark. Select the text to copy it manually."}
        </p>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        <Card className="bg-slate-900/70 border-amber-600/30">
          <CardHeader>
            <CardTitle className="text-amber-300 flex items-center gap-2">
              <Dice5 className="w-4 h-4" /> Dice
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              {["d4", "d6", "d8", "d10", "d12", "d20", "d100"].map((d) => (
                <Button key={d} size="sm" variant={dice === d ? "default" : "outline"} onClick={() => setDice(d)}>
                  {d}
                </Button>
              ))}
            </div>
            <Button className="bg-amber-600 hover:bg-amber-500" onClick={() => setDiceResult(roll(sides))}>
              Roll {dice}
            </Button>
            {diceResult != null && <div className="text-4xl font-bold text-amber-200">{diceResult}</div>}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-amber-600/30">
          <CardHeader>
            <CardTitle className="text-amber-300 flex items-center gap-2">
              <Sparkles className="w-4 h-4" /> Names
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button onClick={genName} variant="outline">
              Generate Aethel-flavored name
            </Button>
            {name && <Badge className="text-base px-3 py-1 bg-amber-700/70">{name}</Badge>}
            {nameLoreHint && (
              <div className="flex flex-wrap gap-1">
                {umbrinLoreTags.map((tag) => (
                  <Badge key={tag} className="text-[10px] bg-violet-900/70 text-violet-100 font-normal">
                    {tag}
                  </Badge>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-amber-600/30">
          <CardHeader>
            <CardTitle className="text-amber-300 flex items-center gap-2">
              <Map className="w-4 h-4" /> Site sparks
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Button onClick={genHook} variant="outline">
                Story hook
              </Button>
              <Button onClick={genPoi} variant="outline">
                Random POI
              </Button>
              <Button onClick={genHaven} variant="outline">
                <Home className="w-3 h-3 mr-1" /> Haven
              </Button>
              <Button onClick={genPeople} variant="outline">
                <Users className="w-3 h-3 mr-1" /> People spark
              </Button>
            </div>
            {(hook || poi || haven || peopleSpark) && (
              <div className="space-y-2 text-sm text-amber-50/80 leading-relaxed">
                {hook && <p>{hook}</p>}
                {poi && <p className="text-sky-200/90">{poi}</p>}
                {haven && <p className="text-emerald-200/90">{haven}</p>}
                {peopleSpark && <p className="text-violet-200/90">{peopleSpark}</p>}
                {peopleLoreTags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {peopleLoreTags.map((tag) => (
                      <Badge key={tag} className="text-[10px] bg-violet-900/70 text-violet-100 font-normal">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-amber-600/30">
          <CardHeader>
            <CardTitle className="text-amber-300 flex items-center gap-2">
              <Coins className="w-4 h-4" /> Loot spark
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button onClick={genLoot} variant="outline">
              Crafted find from workbook
            </Button>
            {loot && <p className="text-sm text-amber-50/80">{loot}</p>}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/70 border-amber-600/30 md:col-span-2">
          <CardHeader>
            <CardTitle className="text-amber-300 flex items-center gap-2">
              <Swords className="w-4 h-4" /> Encounter pack
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap items-center gap-2">
              <Button onClick={genEncounterPack} className="bg-amber-600 hover:bg-amber-500">
                Build pack for Tier {tierPick}
              </Button>
              <Button onClick={loadPackInSession} variant="outline" disabled={!pack}>
                <Swords className="w-3 h-3 mr-1" /> Load in Session
              </Button>
              <div className="flex items-center gap-2">
                <span className="text-sm text-amber-100/70">Party size</span>
                <Input
                  type="number"
                  min={1}
                  max={8}
                  value={count}
                  onChange={(e) => setCount(Number(e.target.value) || 1)}
                  className="w-20 bg-slate-950 border-amber-600/30 text-white"
                />
                <Button onClick={genParty} variant="outline">
                  <Users className="w-3 h-3 mr-1" /> Roles
                </Button>
              </div>
            </div>
            {pack && (
              <pre className="text-sm text-amber-50/85 whitespace-pre-wrap bg-black/40 border border-amber-700/30 rounded p-3">
                {pack}
              </pre>
            )}
            {!pack && (
              <p className="text-xs text-amber-100/60">
                Build a pack first, then send that displayed source-backed output to Session.
              </p>
            )}
            {handoffStatus && (
              <p className={`text-xs ${handoffStatus === "ready" ? "text-emerald-200/80" : "text-red-200/80"}`} role="status">
                {handoffStatus === "ready"
                  ? "Pack queued for Session."
                  : "Could not queue this pack. Build it again and retry."}
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
