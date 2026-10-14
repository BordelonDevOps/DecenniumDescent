"use client";

import { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, BookOpen, Star, Plus, Check, Send } from "lucide-react";
import { SPELLS, SPELL_SCHOOLS, SPELL_LEVELS } from "@/data/spells";
import { pushSpellHandoff } from "@/lib/session-handoff";
import {
  CLASS_SPELL_ALIASES,
  filterSpellsForClass,
  getSpellKey,
  getSpellLevelForClass,
  getSpellLearnLevelForClass,
  getSpellSchoolForClass,
  isRevelationCaster,
  isSpellAvailableToClass,
} from "@/data/spell-utils";

interface Spell {
  name: string;
  level: number;
  school: string;
  schools?: string[];
  placements?: { school: string; level: number; summary: string }[];
  classLevels?: Record<string, number>;
  classRanks?: Record<string, number>;
  classLearnLevels?: Record<string, number>;
  classSchools?: Record<string, string>;
  castingTime: string;
  range: string;
  components: string;
  duration: string;
  description: string;
  classes: string[];
}

export default function SpellsLibrary({ onLoadSession }: { onLoadSession?: () => void }) {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedSchool, setSelectedSchool] = useState<string>("All");
  const [selectedLevel, setSelectedLevel] = useState<string>("All");
  const [selectedClass, setSelectedClass] = useState<string>("All");
  const [learnedSpells, setLearnedSpells] = useState<string[]>([]);
  const [favoriteSpells, setFavoriteSpells] = useState<string[]>([]);
  const [activeView, setActiveView] = useState<string>("all");

  // Filter spells based on current filters
  const filteredSpells = useMemo(() => {
    let spells = Object.values(SPELLS) as Spell[];

    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      spells = spells.filter(
        (spell) =>
          spell.name.toLowerCase().includes(q) ||
          spell.description.toLowerCase().includes(q)
      );
    }

    if (selectedClass !== "All") {
      spells = filterSpellsForClass(spells, selectedClass, {
        schoolFilter: selectedSchool,
        levelFilter: selectedLevel,
      });
    } else {
      if (selectedSchool !== "All") {
        spells = spells.filter((spell) =>
          (spell.placements || []).some((placement) => placement.school === selectedSchool)
        );
      }
      if (selectedLevel !== "All") {
        const level = parseInt(selectedLevel, 10);
        spells = spells.filter((spell) =>
          (spell.placements || []).some((placement) => placement.level === level)
        );
      }
      spells = spells.sort((a, b) =>
        a.level !== b.level ? a.level - b.level : a.name.localeCompare(b.name)
      );
    }

    if (activeView === "learned") {
      spells = spells.filter((spell) => learnedSpells.includes(getSpellKey(spell)));
    } else if (activeView === "favorites") {
      spells = spells.filter((spell) => favoriteSpells.includes(getSpellKey(spell)));
    }

    return spells;
  }, [searchQuery, selectedSchool, selectedLevel, selectedClass, activeView, learnedSpells, favoriteSpells]);

  // Group spells by school
  const spellsBySchool = useMemo(() => {
    const grouped: { [key: string]: Spell[] } = {};
    filteredSpells.forEach(spell => {
      const school = selectedClass !== "All"
        ? (getSpellSchoolForClass(spell, selectedClass) || spell.school)
        : spell.school;
      if (!grouped[school]) {
        grouped[school] = [];
      }
      grouped[school].push(spell);
    });
    return grouped;
  }, [filteredSpells, selectedClass]);

  const hasActiveFilters =
    searchQuery.trim() !== "" ||
    selectedSchool !== "All" ||
    selectedLevel !== "All" ||
    selectedClass !== "All";
  const canClearResults = hasActiveFilters || activeView !== "all";

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedSchool("All");
    setSelectedLevel("All");
    setSelectedClass("All");
  };

  const clearResultView = () => {
    clearFilters();
    setActiveView("all");
  };

  const toggleLearnedSpell = (spell: Spell) => {
    const key = getSpellKey(spell);
    setLearnedSpells((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
    );
  };

  const toggleFavoriteSpell = (spell: Spell) => {
    const key = getSpellKey(spell);
    setFavoriteSpells((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
    );
  };

  const previewSpellInSession = (spell: Spell) => {
    const level = selectedClass !== "All" ? (getSpellLevelForClass(spell, selectedClass) ?? spell.level) : spell.level;
    const school = selectedClass !== "All" ? (getSpellSchoolForClass(spell, selectedClass) ?? spell.school) : spell.school;
    pushSpellHandoff({
      name: spell.name,
      level,
      school,
      castingTime: spell.castingTime,
      range: spell.range,
      duration: spell.duration,
    });
    onLoadSession?.();
  };

  const getSchoolColor = (school: string) => {
    const colors: { [key: string]: string } = {
      "Abjuration": "bg-blue-600",
      "Conjuration": "bg-purple-600",
      "Divination": "bg-yellow-600",
      "Enchantment": "bg-pink-600",
      "Evocation": "bg-red-600",
      "Illusion": "bg-indigo-600",
      "Necromancy": "bg-gray-600",
      "Transmutation": "bg-green-600",
      "Universal": "bg-orange-600"
    };
    return colors[school] || "bg-gray-600";
  };

  const getLevelSuffix = (level: number) => {
    if (level === 0) return "Cantrip";
    return `Rank ${level}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold text-white">Spell Library</h1>
        <p className="text-gray-400">Browse the Weave by Resonance Rank, school, and class-specific acquisition level</p>
      </div>

      {/* Search and Filters */}
      <Card className="glass-card">
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Search spells..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-black/30 border-gray-600 text-white placeholder:text-gray-400"
              />
            </div>

            {/* School Filter */}
            <Select value={selectedSchool} onValueChange={setSelectedSchool}>
              <SelectTrigger className="bg-black/30 border-gray-600 text-white">
                <SelectValue placeholder="School" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All">All Schools</SelectItem>
                {SPELL_SCHOOLS.map(school => (
                  <SelectItem key={school} value={school}>{school}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Level Filter */}
            <Select value={selectedLevel} onValueChange={setSelectedLevel}>
              <SelectTrigger className="bg-black/30 border-gray-600 text-white">
                <SelectValue placeholder="Resonance Rank" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All">All Resonance Ranks</SelectItem>
                {SPELL_LEVELS.map(level => (
                  <SelectItem key={level} value={level.toString()}>
                    {level === 0 ? "Cantrips" : `Rank ${level}`}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Class Filter */}
            <Select value={selectedClass} onValueChange={setSelectedClass}>
              <SelectTrigger className="bg-black/30 border-gray-600 text-white">
                <SelectValue placeholder="Class" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All">All Classes</SelectItem>
                {Object.keys(CLASS_SPELL_ALIASES).map((className) => (
                  <SelectItem key={className} value={className}>
                    {className === "Oracle" ? "Oracle (Revelations)" : className}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* View Toggle */}
            <Tabs value={activeView} onValueChange={setActiveView} className="w-full">
              <TabsList className="grid w-full grid-cols-3 bg-black/30">
                <TabsTrigger value="all" className="text-xs">All</TabsTrigger>
                <TabsTrigger value="learned" className="text-xs">Learned</TabsTrigger>
                <TabsTrigger value="favorites" className="text-xs">Favorites</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          {isRevelationCaster(selectedClass) && (
            <div className="mt-4 rounded-md border border-violet-600/40 bg-violet-950/30 px-4 py-3 text-sm text-violet-200">
              <strong className="text-violet-100">Revelation Caster — not Weave.</strong>{" "}
              Oracles channel Mystery Revelations via Revelation Charges (see Character Builder → Paths).
              They do not receive a general Weave spellbook, so the class filter intentionally returns no spells.
            </div>
          )}

          {/* Stats */}
          <div className="flex flex-wrap justify-between items-center gap-2 mt-4 text-sm text-gray-400">
            <span>
              {filteredSpells.length} spell{filteredSpells.length !== 1 ? "s" : ""} found
              {hasActiveFilters ? " (filtered)" : ""}
              {isRevelationCaster(selectedClass) ? " (reference)" : ""}
            </span>
            <div className="flex items-center gap-3">
              {canClearResults && (
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={clearResultView}
                  className="h-7 text-xs text-gray-300"
                >
                  Clear all filters
                </Button>
              )}
              <span>{learnedSpells.length} learned</span>
              <span>{favoriteSpells.length} favorites</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Spells by School */}
      <div className="space-y-6">
        {Object.keys(spellsBySchool).length === 0 ? (
          <Card className="glass-card">
            <CardContent className="p-8 text-center">
              <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No Spells Found</h3>
              <p className="text-gray-400">Try adjusting your search criteria or filters.</p>
              {canClearResults && (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={clearResultView}
                  className="mt-4"
                >
                  Clear all filters
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          Object.entries(spellsBySchool).map(([school, spells]) => (
            <Card key={school} className="glass-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <div className={`w-4 h-4 rounded ${getSchoolColor(school)}`}></div>
                  <span className="text-white">{school}</span>
                  <Badge variant="secondary" className="ml-auto">
                    {spells.length} spell{spells.length !== 1 ? 's' : ''}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {spells.map((spell) => {
                    const spellKey = getSpellKey(spell);
                    const isLearned = learnedSpells.includes(spellKey);
                    const isFavorite = favoriteSpells.includes(spellKey);
                    const classOk = selectedClass === "All" || isSpellAvailableToClass(spell, selectedClass);
                    const displayLevel = selectedClass !== "All" && classOk
                      ? (getSpellLevelForClass(spell, selectedClass) ?? spell.level)
                      : spell.level;
                    const displaySchool = selectedClass !== "All" && classOk
                      ? (getSpellSchoolForClass(spell, selectedClass) ?? spell.school)
                      : spell.school;
                    const learnLevel = selectedClass !== "All" && classOk
                      ? getSpellLearnLevelForClass(spell, selectedClass)
                      : null;
                    return (
                    <Card key={spellKey} className={`bg-black/20 border-gray-700 hover:border-gray-500 transition-colors ${!classOk ? "opacity-60" : ""}`}>
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between">
                          <div>
                            <CardTitle className="text-lg text-white">{spell.name}</CardTitle>
                            <p className="text-sm text-gray-400">{getLevelSuffix(displayLevel)} · {displaySchool}{Number.isInteger(learnLevel) ? ` · Learn L${learnLevel}` : ""}</p>
                          </div>
                          <div className="flex gap-1">
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => toggleFavoriteSpell(spell)}
                              className={`p-1 h-8 w-8 ${isFavorite ? 'text-yellow-400' : 'text-gray-400'}`}
                            >
                              <Star className="w-4 h-4" fill={isFavorite ? 'currentColor' : 'none'} />
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => toggleLearnedSpell(spell)}
                              className={`p-1 h-8 w-8 ${isLearned ? 'text-green-400' : 'text-gray-400'}`}
                            >
                              {isLearned ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                            </Button>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-2 text-sm">
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div><span className="text-blue-400">Casting Time:</span> {spell.castingTime}</div>
                            <div><span className="text-green-400">Range:</span> {spell.range}</div>
                            <div><span className="text-purple-400">Components:</span> {spell.components}</div>
                            <div><span className="text-yellow-400">Duration:</span> {spell.duration}</div>
                          </div>
                          <div className="text-gray-300 text-xs leading-relaxed">
                            {spell.description.length > 150 
                              ? `${spell.description.substring(0, 150)}...` 
                              : spell.description
                            }
                          </div>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {spell.classes.map(cls => (
                              <Badge key={cls} variant="outline" className="text-xs">
                                {cls.charAt(0).toUpperCase() + cls.slice(1)}
                              </Badge>
                            ))}
                          </div>
                          <div className="pt-1">
                            <Button
                              size="sm"
                              variant="outline"
                              className="h-7 border-indigo-600/50 text-indigo-200 hover:bg-indigo-900/40"
                              onClick={() => previewSpellInSession(spell)}
                            >
                              <Send className="w-3 h-3 mr-1" />
                              Preview in Session
                            </Button>
                            <p className="mt-1 text-[10px] leading-snug text-gray-400">
                              Sends spell reference to Session only; choose a caster and spend RP there if appropriate.
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
      </div>
    </div>
  );
}