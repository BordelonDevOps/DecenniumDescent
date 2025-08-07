"use client";

import { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, BookOpen, Star, Plus, Check } from "lucide-react";
import { SPELLS, SPELL_SCHOOLS, SPELL_LEVELS } from "@/data/spells";

// Class-spell school mapping data
const CLASS_SPELL_SCHOOL_MAPPING: { [key: string]: string[] } = {
  'Bard': ['Enchantment', 'Illusion', 'Universal'],
  'Cleric': ['Abjuration', 'Divination', 'Necromancy', 'Universal'],
  'Druid': ['Abjuration', 'Conjuration', 'Necromancy', 'Transmutation'],
  'mage': ['Abjuration', 'Conjuration', 'Evocation', 'Transmutation', 'Universal'],
  'Paladin': ['Abjuration', 'Divination', 'Enchantment', 'Universal'],
  'Ranger': ['Conjuration', 'Divination', 'Transmutation'],
  'Wizard': ['Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation', 'Universal']
};

interface Spell {
  name: string;
  level: number;
  school: string;
  castingTime: string;
  range: string;
  components: string;
  duration: string;
  description: string;
  classes: string[];
}

export default function SpellsLibrary() {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedSchool, setSelectedSchool] = useState<string>("All");
  const [selectedLevel, setSelectedLevel] = useState<string>("All");
  const [selectedClass, setSelectedClass] = useState<string>("All");
  const [learnedSpells, setLearnedSpells] = useState<string[]>([]);
  const [favoriteSpells, setFavoriteSpells] = useState<string[]>([]);
  const [activeView, setActiveView] = useState<string>("all");

  // Get all unique classes from spells
  const allClasses = useMemo(() => {
    const classes = new Set<string>();
    Object.values(SPELLS).forEach((spell: Spell) => {
      spell.classes.forEach(cls => classes.add(cls));
    });
    return Array.from(classes).sort();
  }, []);

  // Filter spells based on current filters
  const filteredSpells = useMemo(() => {
    let spells = Object.values(SPELLS) as Spell[];

    // Apply search filter
    if (searchQuery) {
      spells = spells.filter(spell => 
        spell.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        spell.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Apply school filter
    if (selectedSchool !== "All") {
      spells = spells.filter(spell => spell.school === selectedSchool);
    }

    // Apply level filter
    if (selectedLevel !== "All") {
      spells = spells.filter(spell => spell.level === parseInt(selectedLevel));
    }

    // Apply class filter with school mapping
    if (selectedClass !== "All") {
      const accessibleSchools = CLASS_SPELL_SCHOOL_MAPPING[selectedClass] || [];
      spells = spells.filter(spell => {
        // Check if spell is available to the class AND if the class can access the spell's school
        return spell.classes.includes(selectedClass) && accessibleSchools.includes(spell.school);
      });
    }

    // Apply view filter
    if (activeView === "learned") {
      spells = spells.filter(spell => learnedSpells.includes(spell.name));
    } else if (activeView === "favorites") {
      spells = spells.filter(spell => favoriteSpells.includes(spell.name));
    }

    return spells.sort((a, b) => {
      if (a.level !== b.level) return a.level - b.level;
      return a.name.localeCompare(b.name);
    });
  }, [searchQuery, selectedSchool, selectedLevel, selectedClass, activeView, learnedSpells, favoriteSpells]);

  // Group spells by school
  const spellsBySchool = useMemo(() => {
    const grouped: { [key: string]: Spell[] } = {};
    filteredSpells.forEach(spell => {
      if (!grouped[spell.school]) {
        grouped[spell.school] = [];
      }
      grouped[spell.school].push(spell);
    });
    return grouped;
  }, [filteredSpells]);

  const toggleLearnedSpell = (spellName: string) => {
    setLearnedSpells(prev => 
      prev.includes(spellName) 
        ? prev.filter(name => name !== spellName)
        : [...prev, spellName]
    );
  };

  const toggleFavoriteSpell = (spellName: string) => {
    setFavoriteSpells(prev => 
      prev.includes(spellName) 
        ? prev.filter(name => name !== spellName)
        : [...prev, spellName]
    );
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
    if (level === 1) return "1st Level";
    if (level === 2) return "2nd Level";
    if (level === 3) return "3rd Level";
    return `${level}th Level`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold text-white">Spell Library</h1>
        <p className="text-gray-400">Discover and learn spells from the Decennium Descent magical compendium</p>
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
                <SelectValue placeholder="Level" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All">All Levels</SelectItem>
                {SPELL_LEVELS.map(level => (
                  <SelectItem key={level} value={level.toString()}>
                    {level === 0 ? "Cantrips" : `Level ${level}`}
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
                {Object.keys(CLASS_SPELL_SCHOOL_MAPPING).map(className => (
                  <SelectItem key={className} value={className}>{className}</SelectItem>
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

          {/* Stats */}
          <div className="flex justify-between items-center mt-4 text-sm text-gray-400">
            <span>{filteredSpells.length} spells found</span>
            <div className="flex gap-4">
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
                  {spells.map((spell) => (
                    <Card key={spell.name} className="bg-black/20 border-gray-700 hover:border-gray-500 transition-colors">
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between">
                          <div>
                            <CardTitle className="text-lg text-white">{spell.name}</CardTitle>
                            <p className="text-sm text-gray-400">{getLevelSuffix(spell.level)} {spell.school}</p>
                          </div>
                          <div className="flex gap-1">
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => toggleFavoriteSpell(spell.name)}
                              className={`p-1 h-8 w-8 ${favoriteSpells.includes(spell.name) ? 'text-yellow-400' : 'text-gray-400'}`}
                            >
                              <Star className="w-4 h-4" fill={favoriteSpells.includes(spell.name) ? 'currentColor' : 'none'} />
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => toggleLearnedSpell(spell.name)}
                              className={`p-1 h-8 w-8 ${learnedSpells.includes(spell.name) ? 'text-green-400' : 'text-gray-400'}`}
                            >
                              {learnedSpells.includes(spell.name) ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
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
                        </div>
                      </CardContent>
                    </Card>
                  ))}
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