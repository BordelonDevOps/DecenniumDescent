"use client";

import { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, BookOpen, Heart, Eye } from "lucide-react";
import monstersData from "../bestiary_data_full.json";

// Tier Zone Mapping
const TIER_ZONES = {
  1: {
    name: "Yieldheart Caverns",
    boss: "Vaskor, the Stone Maw",
    description: "The winding, crystalline gateway into the dungeon's depths. Calcified stalactites drip with luminescent mineral veins, casting fractured rainbows across slippery floors. Floors 1-3 are kept under the watchful eyes of patrolling Automaton sentinels—ancient constructs bound to ensure that only prepared adventurers press onward."
  },
  2: {
    name: "Bloomdeep Marsh",
    boss: "The Bloom That Hungers",
    description: "A self-contained, waterlogged realm of glowing fungus, tangled reeds, and mist-shrouded pools. This bioluminescent swamp spans floors 11-20, where everything from the air you breathe to the ground you tread is part of this living ecosystem. Only those who learn to move with the marsh's rhythms survive."
  },
  3: {
    name: "Anvil of Brogi",
    boss: "Ashthirst the Hollow",
    description: "Brogi's primordial forge: a roaring realm of molten rivers, echoing hammer-strikes, and towering pillars of smelted obsidian. Floors 21-30 vibrate with the cadence of Brogi's eternal hammer on an impossibly vast anvil. The air shimmers with heat and sulfur, and molten droplets spatter like living coals."
  },
  4: {
    name: "Isles of Eternal Radiance",
    boss: "Gor Vekk, Architect of Ends",
    description: "A self-contained archipelago perpetually bathed in dawn's first light. Floating islets of sun-kissed stone drift atop a sea of glowing mist, connected by translucent crystal bridges. Floors 31-40 are where sunstone shards cast prismatic flares, and every breeze carries the echo of distant bell-tones."
  },
  5: {
    name: "Sanctum of Echoing Choirs",
    boss: "Choralith, Voice Below",
    description: "A vast, vaulted cathedral of living sound where every whisper swells into a sweeping symphony. Floors 41-50 immerse you in overwhelming acoustics where time slips away and mounting dread convinces most to turn back. This is where the overwhelming majority of expeditions end."
  },
  6: {
    name: "Crossroads of the Shattered Thread",
    boss: "Lumen of the Shattered Thread",
    description: "A planar nexus where reality's worn weave fractures—and Lumen looms at its heart, weaving fate's loose ends. Beyond Tier 5, only 5 more tiers remain unmapped in the dungeon's deepest reaches."
  },
  7: {
    name: "Pactbound Arena",
    boss: "Xarog, the Pactbound Furnace",
    description: "A circular pit ringed with smoldering braziers, where Xarog's chained forge fuels ten unending trial-matches."
  },
  8: {
    name: "Duskshard Pools",
    boss: "Eirfax, the Dusk Crowned",
    description: "Sunken basins of twilight-tinted crystal through which Eirfax glides, her crown's glow reflected in every shard."
  },
  9: {
    name: "Veiled Iron Spiral",
    boss: "Threxus, the Iron Spiral",
    description: "Twisting girders of black steel form a hidden labyrinth where this spiraling golem enforces its iron will."
  },
  10: {
    name: "Silencebound Void",
    boss: "The Marquis of Silence",
    description: "A boundless nothingness—once conquered by a mortal, now the Marquis's eternal prison and vigil. The deepest mapped tier before the unknown depths."
  }
};

// CRITICAL DUNGEON RULE: At 120 hours, a giant horn sounds throughout the dungeon.
// This marks the point of no return - adventurers must begin their ascent or risk
// being trapped in the depths for 10 years. Only Tiers 1-5 have been fully mapped.

interface Monster {
  name: string;
  size: string;
  type: string;
  challengeRating: string;
  xp: number;
  alignment: string;
  zoneFound: string;
  armorClass: number;
  hitPoints: number;
  speed: string;
  abilities: {
    strength: number;
    dexterity: number;
    constitution: number;
    intelligence: number;
    wisdom: number;
    charisma: number;
  };
  skills: string;
  senses: string;
  languages: string;
  description: string;
  tags: string[];
  loot?: {
    tier1?: { drop: string; rate: string; value: string };
    tier2?: { drop: string; rate: string; value: string };
    tier3?: { drop: string; rate: string; value: string };
  };
}

export default function MonstersLibrary() {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedType, setSelectedType] = useState<string>("All");
  const [selectedCR, setSelectedCR] = useState<string>("All");
  const [selectedSize, setSelectedSize] = useState<string>("All");
  const [selectedZone, setSelectedZone] = useState<string>("All");
  const [selectedTierZone, setSelectedTierZone] = useState<string>("All");
  const [selectedView, setSelectedView] = useState<string>("cards");
  const [selectedMonster, setSelectedMonster] = useState<Monster | null>(null);
  const [favoriteMonsters, setFavoriteMonsters] = useState<string[]>([]);

  const monsters: Monster[] = (monstersData as unknown as Monster[]).map(monster => ({
    ...monster,
    tags: Array.isArray(monster.tags) ? monster.tags : [monster.tags].filter(Boolean)
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

  // Helper function to get tier zone for a monster based on CR
  const getTierZoneForMonster = (monster: Monster) => {
    const cr = parseFloat(monster.challengeRating.replace(/[^0-9.]/g, '')) || 0;
    if (cr <= 2) return TIER_ZONES[1];
    if (cr <= 4) return TIER_ZONES[2];
    if (cr <= 6) return TIER_ZONES[3];
    if (cr <= 8) return TIER_ZONES[4];
    if (cr <= 10) return TIER_ZONES[5];
    if (cr <= 12) return TIER_ZONES[6];
    if (cr <= 14) return TIER_ZONES[7];
    if (cr <= 16) return TIER_ZONES[8];
    if (cr <= 18) return TIER_ZONES[9];
    return TIER_ZONES[10];
  };

  // Filter monsters based on search and filters
  const filteredMonsters = useMemo(() => {
    return monsters.filter(monster => {
      const matchesSearch = monster.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          monster.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          monster.description.toLowerCase().includes(searchQuery.toLowerCase());
      
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
          <p className="text-gray-400">Explore the creatures of Decennium's Descent</p>
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
                placeholder="Search monsters by name, type, or description..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-black/30 border-gray-600 text-white placeholder:text-gray-400"
              />
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
            <div className="flex justify-between items-center text-sm text-gray-400">
              <span>{filteredMonsters.length} monsters found</span>
              <span>{favoriteMonsters.length} favorites</span>
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
                          AC {monster.armorClass} • HP {monster.hitPoints}
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
                    
                    <div className="grid grid-cols-3 gap-2 text-xs text-gray-400 mb-2">
                      <div>STR {monster.abilities.strength}</div>
                      <div>DEX {monster.abilities.dexterity}</div>
                      <div>CON {monster.abilities.constitution}</div>
                    </div>
                    
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
                      <span className="text-white ml-2">{selectedMonster.armorClass}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Hit Points:</span>
                      <span className="text-white ml-2">{selectedMonster.hitPoints}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Speed:</span>
                      <span className="text-white ml-2">{selectedMonster.speed}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Tags:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {selectedMonster.tags.map((tag, index) => (
                          <Badge key={index} variant="outline" className="text-xs">{tag}</Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Abilities */}
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

                  {/* Additional Info */}
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-gray-400">Skills:</span>
                      <span className="text-white ml-2">{selectedMonster.skills}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Senses:</span>
                      <span className="text-white ml-2">{selectedMonster.senses}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Languages:</span>
                      <span className="text-white ml-2">{selectedMonster.languages}</span>
                    </div>
                  </div>

                  {/* Description */}
                  <div>
                    <h4 className="text-white font-semibold mb-2">Description</h4>
                    <p className="text-gray-300 text-sm">{selectedMonster.description}</p>
                  </div>

                  {/* Tier Zone Information */}
                  <div>
                    <h4 className="text-white font-semibold mb-2">Tier Zone: {getTierZoneForMonster(selectedMonster).name}</h4>
                    <div className="bg-amber-900/20 border border-amber-600/30 rounded p-3 space-y-2">
                      <div className="text-amber-400 font-medium">Boss: {getTierZoneForMonster(selectedMonster).boss}</div>
                      <p className="text-gray-300 text-sm">{getTierZoneForMonster(selectedMonster).description}</p>
                      {parseFloat(selectedMonster.challengeRating.replace(/[^0-9.]/g, '')) <= 10 && (
                        <div className="mt-3 p-3 bg-red-900/20 border border-red-600/30 rounded">
                          <p className="text-sm text-red-300">
                            <span className="font-semibold">⚠️ Dungeon Warning:</span> At 120 hours, a giant horn sounds marking the point of no return. 
                            Adventurers must begin their ascent or risk being trapped for 10 years. Only Tiers 1-5 have been fully mapped.
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
                        {selectedMonster.loot.tier1 && (
                          <div className="flex justify-between items-center bg-black/20 rounded p-2">
                            <div>
                              <div className="text-white font-medium">Tier 1 Loot</div>
                              <div className="text-gray-400 text-xs">Common drops</div>
                            </div>
                            <div className="text-right">
                              <div className="text-white font-medium">{selectedMonster.loot.tier1.rate && selectedMonster.loot.tier1.rate !== 'nan' ? Math.round(parseFloat(selectedMonster.loot.tier1.rate) * 100) : 0}%</div>
                              <div className="text-yellow-400 text-xs">{selectedMonster.loot.tier1.value && selectedMonster.loot.tier1.value !== 'nan' ? selectedMonster.loot.tier1.value : '0'} gold</div>
                            </div>
                          </div>
                        )}
                        {selectedMonster.loot.tier2 && (
                          <div className="flex justify-between items-center bg-black/20 rounded p-2">
                            <div>
                              <div className="text-white font-medium">Tier 2 Loot</div>
                              <div className="text-gray-400 text-xs">Uncommon drops</div>
                            </div>
                            <div className="text-right">
                              <div className="text-white font-medium">{selectedMonster.loot.tier2.rate && selectedMonster.loot.tier2.rate !== 'nan' ? Math.round(parseFloat(selectedMonster.loot.tier2.rate) * 100) : 0}%</div>
                              <div className="text-yellow-400 text-xs">{selectedMonster.loot.tier2.value && selectedMonster.loot.tier2.value !== 'nan' ? selectedMonster.loot.tier2.value : '0'} gold</div>
                            </div>
                          </div>
                        )}
                        {selectedMonster.loot.tier3 && (
                          <div className="flex justify-between items-center bg-black/20 rounded p-2">
                            <div>
                              <div className="text-white font-medium">Tier 3 Loot</div>
                              <div className="text-gray-400 text-xs">Rare drops</div>
                            </div>
                            <div className="text-right">
                              <div className="text-white font-medium">{selectedMonster.loot.tier3.rate && selectedMonster.loot.tier3.rate !== 'nan' ? Math.round(parseFloat(selectedMonster.loot.tier3.rate) * 100) : 0}%</div>
                              <div className="text-yellow-400 text-xs">{selectedMonster.loot.tier3.value && selectedMonster.loot.tier3.value !== 'nan' ? selectedMonster.loot.tier3.value : '0'} gold</div>
                            </div>
                          </div>
                        )}
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