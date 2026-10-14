"use client";

import { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, BookOpen, Heart, Eye, Swords, X } from "lucide-react";
import monstersData from "../bestiary_data_full.json";
import { pushFoeHandoff } from "@/lib/session-handoff";

// Tier Zone Mapping
const TIER_ZONES: Record<number, { name: string; boss: string; description: string }> = {
  1: {
    name: "Yieldheart Caverns",
    boss: "Vaskor, the Stone Maw",
    description: "The best documented portion of the Descent. Routes change between Openings, but professional maps, patrol reports, and harvest ledgers make Tier I understood danger rather than mystery."
  },
  2: {
    name: "Bloomdeep Marsh",
    boss: "The Bloom That Hungers",
    description: "The marsh and the routes approaching the Haven support the dungeon's largest professional economy. Surviving this depth with profitable cargo establishes an expedition as a serious company."
  },
  3: {
    name: "Anvil of Brogi",
    boss: "Ashthirst the Hollow",
    description: "Beyond the Haven economy, expeditions require military logistics, replacement equipment, specialists, and reliable extraction plans. Tier III service marks an elite professional career."
  },
  4: {
    name: "Isles of Eternal Radiance",
    boss: "Gor Vekk, Architect of Ends",
    description: "The dark frontier. Reports remain usable, but repeated symbols, shared dreams, altered records, and impossible anatomies begin appearing without an accepted explanation."
  },
  5: {
    name: "Sanctum of Echoing Choirs",
    boss: "Choralith, Voice Below",
    description: "Legendary territory reconstructed from rare returns, damaged journals, sealed guild records, and artifacts whose provenance is often disputed."
  },
  6: {
    name: "Crossroads of the Shattered Thread",
    boss: "Lumen — Sixth Gate Disaster Record",
    description: "The limit of recognized history. The most famous expedition reached this Gate Guardian and failed. Public records preserve fragments, not a complete ecology, stat block, or proven victory method."
  }
};

// CRITICAL DUNGEON RULE: At 1200 hours (day 50 of the 2400h Opening), a giant horn
// sounds throughout the dungeon — point of no return. Soft quit at Floor 50 Canticle
// is separate. Retreat or risk 10 years trapped. Only Tiers 1-5 fully mapped.

interface RawMonster {
  name: string;
  size: string;
  type: string;
  challengeRating: string;
  xp: number;
  alignment: string;
  zoneFound: string;
  armorClass?: number;
  hitPoints?: number;
  speed?: string;
  abilities?: {
    strength: number;
    dexterity: number;
    constitution: number;
    intelligence: number;
    wisdom: number;
    charisma: number;
  };
  skills?: string;
  senses?: string;
  languages?: string;
  description: string;
  tags?: string | string[];
  loot?: Record<string, { drop?: string | null; rate?: string | null; value?: string | null }>;
  ingestSource?: string;
  publicationClassification?: string;
  knowledgeStatus?: string;
  primarySource?: string;
  reliability?: string;
  confirmedRange?: string;
  rumoredRange?: string;
  encounterRole?: string;
  experiencedSigns?: string;
  knowledge?: Array<{ result: string; information: string }>;
  traits?: Array<{ name: string; text: string }>;
  actions?: Array<{ name: string; text: string }>;
  tactics?: string;
  howToDefeat?: string;
  habitat?: string;
  harvest?: string;
  variants?: string;
}

type Monster = Omit<RawMonster, "tags"> & { tags: string[] };

function statOrDash(value?: number | null): string {
  return value != null && Number.isFinite(value) ? String(value) : "—";
}

function normalizeTags(tags?: string | string[]): string[] {
  if (Array.isArray(tags)) return tags.filter(Boolean);
  if (typeof tags === "string" && tags.trim() && tags.toLowerCase() !== "nan") return [tags];
  return [];
}

export default function MonstersLibrary({ onLoadSession }: { onLoadSession?: () => void }) {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedType, setSelectedType] = useState<string>("All");
  const [selectedCR, setSelectedCR] = useState<string>("All");
  const [selectedSize, setSelectedSize] = useState<string>("All");
  const [selectedZone, setSelectedZone] = useState<string>("All");
  const [selectedTierZone, setSelectedTierZone] = useState<string>("All");
  const [selectedView, setSelectedView] = useState<string>("cards");
  const [selectedMonster, setSelectedMonster] = useState<Monster | null>(null);
  const [favoriteMonsters, setFavoriteMonsters] = useState<string[]>([]);

  const monsters: Monster[] = (monstersData as unknown as RawMonster[]).map(monster => ({
    ...monster,
    tags: normalizeTags(monster.tags),
  }));

  // Get unique values for filters
  const uniqueTypes = useMemo(() => {
    const types = new Set(monsters.map(monster => monster.type));
    return Array.from(types).sort();
  }, [monsters]);

  const uniqueCRs = useMemo(() => {
    const crs = new Set(monsters.map(monster => monster.challengeRating));
    return Array.from(crs).sort((a, b) => {
      const aNum = parseFloat(a.replace(/[^0-9.]/g, ''));
      const bNum = parseFloat(b.replace(/[^0-9.]/g, ''));
      return aNum - bNum;
    });
  }, [monsters]);

  const uniqueSizes = useMemo(() => {
    const sizes = new Set(monsters.map(monster => monster.size));
    return Array.from(sizes).sort();
  }, [monsters]);

  const uniqueZones = useMemo(() => {
    const zones = new Set(monsters.map(monster => monster.zoneFound));
    return Array.from(zones).sort();
  }, [monsters]);

  // Prefer the canonical dossier's declared tier. CR is only a fallback for legacy rows.
  const getTierNumberForMonster = (monster: Monster) => {
    const declared = `${monster.zoneFound} ${monster.confirmedRange ?? ""}`.match(/\bT(?:ier\s*)?([1-6])\b/i);
    if (declared) return Number(declared[1]);
    const cr = parseFloat(monster.challengeRating.replace(/[^0-9.]/g, "")) || 0;
    if (cr <= 2) return 1;
    if (cr <= 4) return 2;
    if (cr <= 6) return 3;
    if (cr <= 8) return 4;
    if (cr <= 10) return 5;
    return 6;
  };

  const getTierZoneForMonster = (monster: Monster) =>
    TIER_ZONES[getTierNumberForMonster(monster)] ?? TIER_ZONES[6];

  const hasActiveFilters =
    searchQuery.trim() !== "" ||
    selectedType !== "All" ||
    selectedCR !== "All" ||
    selectedSize !== "All" ||
    selectedZone !== "All" ||
    selectedTierZone !== "All";

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedType("All");
    setSelectedCR("All");
    setSelectedSize("All");
    setSelectedZone("All");
    setSelectedTierZone("All");
  };

  // Filter monsters based on search and filters
  const filteredMonsters = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    const crQuery = q.replace(/^cr\s*/, "");

    return monsters.filter(monster => {
      const tagText = (monster.tags || []).join(" ").toLowerCase();
      const cr = monster.challengeRating.toLowerCase();
      const matchesSearch =
        !q ||
        monster.name.toLowerCase().includes(q) ||
        monster.type.toLowerCase().includes(q) ||
        monster.description.toLowerCase().includes(q) ||
        monster.zoneFound.toLowerCase().includes(q) ||
        cr.includes(q) ||
        cr.includes(crQuery) ||
        tagText.includes(q);
      
      const matchesType = selectedType === "All" || monster.type === selectedType;
      const matchesCR = selectedCR === "All" || monster.challengeRating === selectedCR;
      const matchesSize = selectedSize === "All" || monster.size === selectedSize;
      const matchesZone = selectedZone === "All" || monster.zoneFound === selectedZone;
      
      const tierZone = getTierZoneForMonster(monster);
      const matchesTierZone = selectedTierZone === "All" || tierZone.name === selectedTierZone;
      
      return matchesSearch && matchesType && matchesCR && matchesSize && matchesZone && matchesTierZone;
    });
  }, [monsters, searchQuery, selectedType, selectedCR, selectedSize, selectedZone, selectedTierZone]);

  const toggleFavorite = (monsterName: string) => {
    setFavoriteMonsters(prev => 
      prev.includes(monsterName) 
        ? prev.filter(name => name !== monsterName)
        : [...prev, monsterName]
    );
  };

  const addMonsterToSession = (monster: Monster) => {
    pushFoeHandoff({
      name: monster.name,
      hitPoints: monster.hitPoints,
      challengeRating: monster.challengeRating,
      zoneFound: monster.zoneFound,
    });
    onLoadSession?.();
  };

  const getAbilityModifier = (score: number) => {
    return Math.floor((score - 10) / 2);
  };

  const formatModifier = (modifier: number) => {
    return modifier >= 0 ? `+${modifier}` : `${modifier}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Bestiary</h1>
          <p className="text-gray-400">Field dossiers from the confirmed and licensed records of the Known Descent</p>
        </div>

        {/* Search and Filters */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Search className="w-5 h-5" />
              Search & Filter
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Search name, type, CR (e.g. cr 5), tags, zone…"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-9 bg-black/30 border-gray-600 text-white placeholder:text-gray-400"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery("")}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  aria-label="Clear search"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Filters */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              <div>
                <label className="text-sm text-gray-400 mb-1 block">Type</label>
                <Select value={selectedType} onValueChange={setSelectedType}>
                  <SelectTrigger 
                    className="w-full bg-black/30 border border-gray-600 rounded-md px-3 py-2 text-white"
                  >
                    <SelectValue placeholder="All Types" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="All">All Types</SelectItem>
                    {uniqueTypes.map(type => (
                      <SelectItem key={type} value={type}>{type}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm text-gray-400 mb-1 block">Challenge Rating</label>
                <Select value={selectedCR} onValueChange={setSelectedCR}>
                  <SelectTrigger 
                    className="w-full bg-black/30 border border-gray-600 rounded-md px-3 py-2 text-white"
                  >
                    <SelectValue placeholder="All CRs" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="All">All CRs</SelectItem>
                    {uniqueCRs.map(cr => (
                      <SelectItem key={cr} value={cr}>CR {cr}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm text-gray-400 mb-1 block">Size</label>
                <Select value={selectedSize} onValueChange={setSelectedSize}>
                  <SelectTrigger 
                    className="w-full bg-black/30 border border-gray-600 rounded-md px-3 py-2 text-white"
                  >
                    <SelectValue placeholder="All Sizes" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="All">All Sizes</SelectItem>
                    {uniqueSizes.map(size => (
                      <SelectItem key={size} value={size}>{size}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm text-gray-400 mb-1 block">Zone</label>
                <Select value={selectedZone} onValueChange={setSelectedZone}>
                  <SelectTrigger 
                    className="w-full bg-black/30 border border-gray-600 rounded-md px-3 py-2 text-white"
                  >
                    <SelectValue placeholder="All Zones" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="All">All Zones</SelectItem>
                    {uniqueZones.map(zone => (
                      <SelectItem key={zone} value={zone}>{zone}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm text-gray-400 mb-1 block">Tier Zone</label>
                <Select value={selectedTierZone} onValueChange={setSelectedTierZone}>
                  <SelectTrigger 
                    className="w-full bg-black/30 border border-gray-600 rounded-md px-3 py-2 text-white"
                  >
                    <SelectValue placeholder="All Tier Zones" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="All">All Tier Zones</SelectItem>
                    {Object.values(TIER_ZONES).map(tierZone => (
                      <SelectItem key={tierZone.name} value={tierZone.name}>{tierZone.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* View Toggle */}
            <div>
              <label className="text-sm text-gray-400 mb-1 block">View</label>
              <Select value={selectedView} onValueChange={setSelectedView}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cards">Cards</SelectItem>
                  <SelectItem value="list">List</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Results Summary */}
            <div className="flex flex-wrap justify-between items-center gap-2 text-sm text-gray-400">
              <span>
                {filteredMonsters.length} monsters found
                {hasActiveFilters && " (filtered)"}
              </span>
              <div className="flex items-center gap-3">
                {hasActiveFilters && (
                  <Button type="button" variant="ghost" size="sm" onClick={clearFilters} className="h-7 text-xs text-gray-300">
                    Clear all filters
                  </Button>
                )}
                <span>{favoriteMonsters.length} favorites</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Monster List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Monster Cards */}
          <div className="space-y-4 order-2 lg:order-1">
            {filteredMonsters.length === 0 ? (
              <Card className="glass-card">
                <CardContent className="p-8 text-center">
                  <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">No Monsters Found</h3>
                  <p className="text-gray-400">Try adjusting your search criteria or filters.</p>
                  {hasActiveFilters && (
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={clearFilters}
                      className="mt-4"
                    >
                      Clear all filters
                    </Button>
                  )}
                </CardContent>
              </Card>
            ) : (
              filteredMonsters.map((monster) => (
                <Card 
                  key={monster.name} 
                  className={`glass-card hover:bg-white/5 transition-colors cursor-pointer ${
                    selectedMonster?.name === monster.name ? 'border-blue-500/50 bg-blue-500/10' : ''
                  }`}
                  onClick={() => setSelectedMonster(monster)}
                >
                  <CardContent className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="text-lg font-semibold text-white">{monster.name}</h3>
                        <div className="flex gap-1 mt-1 flex-wrap">
                          <Badge variant="outline" className="text-xs">{monster.size}</Badge>
                          <Badge variant="outline" className="text-xs">{monster.type}</Badge>
                          <Badge variant="outline" className="text-xs">CR {monster.challengeRating}</Badge>
                          {monster.xp > 0 && (
                            <Badge variant="outline" className="text-xs text-yellow-400">
                              {monster.xp} XP
                            </Badge>
                          )}
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          {monster.armorClass != null || monster.hitPoints != null
                            ? `AC ${statOrDash(monster.armorClass)} • HP ${statOrDash(monster.hitPoints)}`
                            : "Combat stats not in spreadsheet source"}
                        </div>
                        <div className="text-xs mt-1">
                          <div className="text-gray-400">Zone: {monster.zoneFound}</div>
                          <div className="text-amber-400">Tier: {getTierZoneForMonster(monster).name}</div>
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(monster.name);
                          }}
                          className={favoriteMonsters.includes(monster.name) ? "text-red-400" : "text-gray-400"}
                        >
                          <Heart className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                    
                    {monster.abilities && (
                      <div className="grid grid-cols-3 gap-2 text-xs text-gray-400 mb-2">
                        <div>STR {monster.abilities.strength}</div>
                        <div>DEX {monster.abilities.dexterity}</div>
                        <div>CON {monster.abilities.constitution}</div>
                      </div>
                    )}
                    
                    <p className="text-sm text-gray-300 line-clamp-2">{monster.description}</p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          {/* Monster Details */}
          <div className="order-1 lg:order-2">
            {selectedMonster ? (
              <Card className="glass-card sticky top-4">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-white text-xl">{selectedMonster.name}</CardTitle>
                      <p className="text-gray-400">{selectedMonster.size} {selectedMonster.type}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-gray-400 hover:text-white"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => toggleFavorite(selectedMonster.name)}
                        className={favoriteMonsters.includes(selectedMonster.name) ? "text-red-400" : "text-gray-400"}
                      >
                        <Heart className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Basic Stats */}
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-400">Size:</span>
                      <span className="text-white ml-2">{selectedMonster.size}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Type:</span>
                      <span className="text-white ml-2">{selectedMonster.type}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Challenge Rating:</span>
                      <span className="text-white ml-2">{selectedMonster.challengeRating}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Experience Points:</span>
                      <span className="text-yellow-400 ml-2">{selectedMonster.xp}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Alignment:</span>
                      <span className="text-white ml-2">{selectedMonster.alignment}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Zone Found:</span>
                      <span className="text-white ml-2">{selectedMonster.zoneFound}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Tier Zone:</span>
                      <span className="text-amber-400 ml-2">{getTierZoneForMonster(selectedMonster).name}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Armor Class:</span>
                      <span className="text-white ml-2">{statOrDash(selectedMonster.armorClass)}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Hit Points:</span>
                      <span className="text-white ml-2">{statOrDash(selectedMonster.hitPoints)}</span>
                    </div>
                    {selectedMonster.speed && (
                      <div>
                        <span className="text-gray-400">Speed:</span>
                        <span className="text-white ml-2">{selectedMonster.speed}</span>
                      </div>
                    )}
                    {selectedMonster.tags && selectedMonster.tags.length > 0 && (
                      <div>
                        <span className="text-gray-400">Tags:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {selectedMonster.tags.map((tag, index) => (
                            <Badge key={index} variant="outline" className="text-xs">{tag}</Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {selectedMonster.abilities && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">Ability Scores</h4>
                      <div className="grid grid-cols-6 gap-2 text-center text-sm">
                        {Object.entries(selectedMonster.abilities).map(([ability, score]) => (
                          <div key={ability} className="bg-black/20 rounded p-2">
                            <div className="text-gray-400 uppercase">{ability.slice(0, 3)}</div>
                            <div className="text-white font-bold">{score}</div>
                            <div className="text-gray-400">{formatModifier(getAbilityModifier(score as number))}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {(selectedMonster.skills || selectedMonster.senses || selectedMonster.languages) && (
                    <div className="space-y-2 text-sm">
                      {selectedMonster.skills && (
                        <div>
                          <span className="text-gray-400">Skills:</span>
                          <span className="text-white ml-2">{selectedMonster.skills}</span>
                        </div>
                      )}
                      {selectedMonster.senses && (
                        <div>
                          <span className="text-gray-400">Senses:</span>
                          <span className="text-white ml-2">{selectedMonster.senses}</span>
                        </div>
                      )}
                      {selectedMonster.languages && (
                        <div>
                          <span className="text-gray-400">Languages:</span>
                          <span className="text-white ml-2">{selectedMonster.languages}</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Description */}
                  <div>
                    <h4 className="text-white font-semibold mb-2">What It Is</h4>
                    <p className="text-gray-300 text-sm">{selectedMonster.description}</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div className="bg-black/20 rounded p-3">
                      <div className="text-gray-400">Knowledge status</div>
                      <div className="text-white">{selectedMonster.knowledgeStatus || "Unclassified"}</div>
                    </div>
                    <div className="bg-black/20 rounded p-3">
                      <div className="text-gray-400">Reliability</div>
                      <div className="text-white">{selectedMonster.reliability || "Unverified"}</div>
                    </div>
                    <div className="bg-black/20 rounded p-3 md:col-span-2">
                      <div className="text-gray-400">Primary source</div>
                      <div className="text-white">{selectedMonster.primarySource || "No surviving source named"}</div>
                    </div>
                  </div>

                  {selectedMonster.experiencedSigns && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">What Experienced Expeditions Notice</h4>
                      <p className="text-gray-300 text-sm">{selectedMonster.experiencedSigns}</p>
                    </div>
                  )}

                  {selectedMonster.knowledge && selectedMonster.knowledge.length > 0 && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">Creature Knowledge</h4>
                      <div className="space-y-2">
                        {selectedMonster.knowledge.map((row) => (
                          <div key={row.result} className="bg-black/20 rounded p-2 text-sm">
                            <span className="font-semibold text-amber-300">{row.result}: </span>
                            <span className="text-gray-300">{row.information}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {selectedMonster.traits && selectedMonster.traits.length > 0 && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">Traits</h4>
                      <div className="space-y-2">
                        {selectedMonster.traits.map((trait) => (
                          <p key={trait.name} className="text-sm text-gray-300"><span className="font-semibold text-white">{trait.name}.</span> {trait.text}</p>
                        ))}
                      </div>
                    </div>
                  )}

                  {selectedMonster.actions && selectedMonster.actions.length > 0 && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">Actions</h4>
                      <div className="space-y-2">
                        {selectedMonster.actions.map((action) => (
                          <p key={action.name} className="text-sm text-gray-300"><span className="font-semibold text-white">{action.name}.</span> {action.text}</p>
                        ))}
                      </div>
                    </div>
                  )}

                  {selectedMonster.tactics && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">How It Fights</h4>
                      <p className="text-gray-300 text-sm">{selectedMonster.tactics}</p>
                    </div>
                  )}

                  {selectedMonster.howToDefeat && (
                    <div className="bg-emerald-950/30 border border-emerald-600/30 rounded p-3">
                      <h4 className="text-emerald-300 font-semibold mb-2">How to Defeat It</h4>
                      <p className="text-gray-200 text-sm">{selectedMonster.howToDefeat}</p>
                    </div>
                  )}

                  {selectedMonster.habitat && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">Habitat, Goals, and Lair</h4>
                      <p className="text-gray-300 text-sm">{selectedMonster.habitat}</p>
                    </div>
                  )}

                  <div className="space-y-2">
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-red-600/50 text-red-200 hover:bg-red-900/40"
                      onClick={() => addMonsterToSession(selectedMonster)}
                    >
                      <Swords className="w-3 h-3 mr-1" />
                      Add foe in Session
                    </Button>
                    <p className="text-xs text-gray-400">
                      Sends name, CR, zone, and HP when present (otherwise Session estimates HP from CR).
                    </p>
                  </div>

                  {/* Tier Zone Information */}
                  <div>
                    <h4 className="text-white font-semibold mb-2">Tier Zone: {getTierZoneForMonster(selectedMonster).name}</h4>
                    <div className="bg-amber-900/20 border border-amber-600/30 rounded p-3 space-y-2">
                      <div className="text-amber-400 font-medium">Boss: {getTierZoneForMonster(selectedMonster).boss}</div>
                      <p className="text-gray-300 text-sm">{getTierZoneForMonster(selectedMonster).description}</p>
                      {getTierNumberForMonster(selectedMonster) <= 6 && (
                        <div className="mt-3 p-3 bg-red-900/20 border border-red-600/30 rounded">
                          <p className="text-sm text-red-300">
                            <span className="font-semibold">⚠️ Dungeon Warning:</span> At 1200 hours (day 50), a giant horn sounds marking the point of no return.
                            Adventurers must begin their ascent or risk being trapped for 10 years. Soft quit at Floor 50 Canticle ≠ Horn. Only Tiers I–V have reliable field records; the Sixth Gate remains a failed historical boundary.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Loot Information */}
                  {selectedMonster.loot && (
                    <div>
                      <h4 className="text-white font-semibold mb-2">Loot Table</h4>
                      <div className="space-y-2">
                        {Object.entries(selectedMonster.loot).map(([tierKey, tierLoot]) => {
                          if (!tierLoot?.drop) return null;
                          const tierLabel = (tierLoot as { tier?: string }).tier ?? tierKey.replace("drop", "");
                          return (
                            <div key={tierKey} className="flex justify-between items-center bg-black/20 rounded p-2">
                              <div>
                                <div className="text-white font-medium">Tier {tierLabel} — {tierLoot.drop}</div>
                                <div className="text-gray-400 text-xs">Harvest component</div>
                              </div>
                              <div className="text-right">
                                <div className="text-white font-medium">{tierLoot.rate || "Director-set"}</div>
                                <div className="text-yellow-400 text-xs">{tierLoot.value || "Director-set"}</div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="glass-card">
                <CardContent className="p-8 text-center">
                  <Eye className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">Select a Monster</h3>
                  <p className="text-gray-400">Click on a monster card to view detailed information.</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};