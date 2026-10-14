"use client";

import React, { useState, useEffect, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Dice1,
  Plus,
  Copy,
  Save,
  Download,
  Search,
  BookOpen,
  Zap
} from "lucide-react";
import { SPELLS, SPELL_SCHOOLS, SPELL_LEVELS, searchSpells } from "@/data/spells";
import {
  filterSpellsForClass,
  getSpellKey,
  getSpellDisplayName,
  isSpellAvailableToClass,
  isSpellcasterClass,
  normalizeSpellKeys,
} from "@/data/spell-utils";
import { BACKGROUNDS, getBackgroundByName } from "@/data/backgrounds";
import {
  applyBackgroundReputation,
  reputationSummary,
} from "@/data/reputation";
import { computeSpellCost, multiclassRpBreakdown, resolveMaxRp } from "@/data/resonance-economy";
import ReputationPanel from "@/components/ReputationPanel";
import featsData from "@/data/feats";
import { builderRaces } from "@/data/builder-races";
import racialVariants from "@/data/racial-variants.json";
import prestigePaths, { prestigeForBaseClass } from "@/data/prestige";
import CharacterAppearance from "@/components/CharacterAppearance";
import classDetails, { classPathBlocks } from "@/data/class-details";
import { CANON_CLASSES } from "@/data/canon-classes";
import { SACRED_OATHS, getOathById, PALADIN_AURA_SCALING } from "@/data/paladin-oaths";
import {
  DRUID_CIRCLES,
  BASE_DRUID_FORMS,
  ARCH_DRUID_FORMS,
  SHAPESHIFT_RULES,
  getHeroFormsForCircle,
  hasDraftHeroFormsForCircle,
  druidPathBlocksForCircle,
  formsAvailableAtLevel,
} from "@/data/druid-shapeshifting";
import { ORACLE_MYSTERIES, getMysteryById, ORACLE_HERO_PROGRESSION } from "@/data/oracle-mysteries";
import {
  ORACLE_CURSES,
  getCurseById,
  ORACLE_REVELATION_CHARGES,
  ORACLE_CURSE_BOON_LEVELS,
} from "@/data/oracle-curses";
import CharacterSheet from "@/components/CharacterSheet";
import ClassPathDisplay from "@/components/ClassPathDisplay";
import LevelFeatureList from "@/components/LevelFeatureList";
import ClassCeilingCapsCallout from "@/components/ClassCeilingCapsCallout";
import ChargenWarnings from "@/components/ChargenWarnings";
import PrestigeRequirements from "@/components/PrestigeRequirements";
import {
  loadSavedCharacters,
  upsertCharacter,
  deleteCharacter,
  characterDisplayName,
  normalizeCharacter,
} from "@/lib/character-storage";
import {
  CANON_XP_THRESHOLDS,
  formatXp,
  xpThresholdForLevel,
  xpToNextLevel,
} from "@/lib/xp-economy";

const PINNED_RACE = "Umbrin";
const races = builderRaces;
const sortedRaces = (() => {
  const pinned = builderRaces.find((r) => r.name === PINNED_RACE);
  const rest = builderRaces.filter((r) => r.name !== PINNED_RACE);
  return pinned ? [pinned, ...rest] : builderRaces;
})();

type RacialVariant = {
  subrace: string;
  parentRace: string;
  ability: string;
  racialFeat: { name: string; effect: string };
};

const racialVariantList = racialVariants as RacialVariant[];

function subraceVariant(subrace: string): RacialVariant | undefined {
  return racialVariantList.find((v) => v.subrace === subrace);
}

const defaultAbilities = [
    { name: "Strength", score: 10, modifier: 0 },
    { name: "Dexterity", score: 10, modifier: 0 },
    { name: "Constitution", score: 10, modifier: 0 },
    { name: "Intelligence", score: 10, modifier: 0 },
    { name: "Wisdom", score: 10, modifier: 0 },
    { name: "Charisma", score: 10, modifier: 0 },
  ];

  const abilityGenerationMethods = [
    { id: "random", name: "Random Roll", description: "Roll 4d6, drop lowest for each ability" },
    { id: "buyin", name: "Point Buy", description: "Purchase ability scores with 27 points" },
    { id: "preset", name: "Standard Array", description: "Use preset values: 15, 14, 13, 12, 10, 8" }
  ];

  const standardArray = [15, 14, 13, 12, 10, 8];
  const pointBuyBase = 8;
  const pointBuyMax = 15;
  const pointBuyPoints = 27;

  // Utility function to calculate ability modifier from score
  const calculateModifier = (score: number): number => {
    return Math.floor((score - 10) / 2);
  };

  // Function to roll 4d6 drop lowest
  const rollAbilityScore = (): number => {
    const rolls = Array.from({ length: 4 }, () => Math.floor(Math.random() * 6) + 1);
    rolls.sort((a, b) => b - a);
    return rolls.slice(0, 3).reduce((sum, roll) => sum + roll, 0);
  };

  // Function to generate random ability scores
  const generateRandomAbilities = () => {
    return defaultAbilities.map(ability => ({
      ...ability,
      score: rollAbilityScore(),
      modifier: 0 // Will be calculated after
    }));
  };

  // Function to apply standard array
  const applyStandardArray = (assignments: number[]) => {
    return defaultAbilities.map((ability, index) => ({
      ...ability,
      score: assignments[index] || 10,
      modifier: 0 // Will be calculated after
    }));
  };

  // Function to update ability modifiers
  const updateAbilityModifiers = (abilities: typeof defaultAbilities) => {
    return abilities.map(ability => ({
      ...ability,
      modifier: calculateModifier(ability.score)
    }));
  };

  // Point buy cost calculation
  const getPointBuyCost = (score: number): number => {
    if (score <= 13) return score - 8;
    if (score === 14) return 7;
    if (score === 15) return 9;
    return 0;
  };

  // Calculate total point buy cost
  const calculatePointBuyCost = (abilities: typeof defaultAbilities): number => {
    return abilities.reduce((total, ability) => total + getPointBuyCost(ability.score), 0);
  };

  // Apply racial bonuses to abilities
  const applyRacialBonuses = (abilities: typeof defaultAbilities, race: (typeof races)[number] | null | undefined) => {
    if (!race || !race.abilityScoreIncrease) return abilities;

    const asi = race.abilityScoreIncrease;
    const updatedAbilities = abilities.map((a) => ({ ...a }));

    // Human (and similar): all scores +1
    if (/All ability scores \+1/i.test(asi)) {
      return updateAbilityModifiers(
        updatedAbilities.map((a) => ({ ...a, score: a.score + 1 }))
      );
    }

    // Skip ambiguous OR choices — leave scores unchanged until player picks
    if (/\bOR\b/i.test(asi)) {
      return updateAbilityModifiers(updatedAbilities);
    }

    for (const part of asi.split(/,/)) {
      const m = part.trim().match(/([A-Za-z]+)\s*\+(\d+)/);
      if (!m) continue;
      const abilityIndex = updatedAbilities.findIndex((a) => a.name === m[1]);
      if (abilityIndex === -1) continue;
      updatedAbilities[abilityIndex] = {
        ...updatedAbilities[abilityIndex],
        score: updatedAbilities[abilityIndex].score + Number(m[2]),
      };
    }

    return updateAbilityModifiers(updatedAbilities);
  };

const feats = featsData;

/** Rulebook Classes Table — 17 canon base classes; must match `CANON_CLASSES` exactly. */
const classes = [
  {
    name: "Bard",
    info: "Musical magic user with Crescendo mechanics. Bards weave magic through words and music, inspiring allies and confounding enemies.",
    hitDie: "d8",
    primaryAbility: "Charisma",
    savingThrows: ["Dexterity", "Charisma"],
    spellcasting: "Full Caster",
    archClasses: ["Virtuoso"]
  },
  {
    name: "Cleric",
    info: "Divine spellcaster who channels the power of their deity. Clerics serve as healers, protectors, and spiritual guides.",
    hitDie: "d8",
    primaryAbility: "Wisdom",
    savingThrows: ["Wisdom", "Charisma"],
    spellcasting: "Full Caster",
    archClasses: ["Bishop"]
  },
  {
    name: "Crimson Agent",
    info: "Specialized agent with limited spellcasting. Masters of infiltration, espionage, and targeted elimination.",
    hitDie: "d8",
    primaryAbility: "Dexterity",
    savingThrows: ["Dexterity", "Intelligence"],
    spellcasting: "Third Caster",
    archClasses: ["Hemomancer"]
  },
  {
    name: "Druid",
    info: "Nature magic user with shapeshifting system. Druids are guardians of the natural world and masters of primal magic.",
    hitDie: "d8",
    primaryAbility: "Wisdom",
    savingThrows: ["Intelligence", "Wisdom"],
    spellcasting: "Full Caster",
    archClasses: ["Circle of the Land", "Circle of the Moon", "Circle of the Storm"]
  },
  {
    name: "Dragoon",
    info: "Elite polearm fighter who harnesses momentum and gravity for devastating leap attacks.",
    hitDie: "d10",
    primaryAbility: "Strength & Dexterity",
    savingThrows: ["Strength", "Dexterity"],
    spellcasting: "Non-Caster",
    archClasses: ["Dragon Lancer"]
  },
  {
    name: "Mage",
    info: "Arcane spellcaster who studies the fundamental forces of magic. Mages are versatile wielders of arcane power.",
    hitDie: "d6",
    primaryAbility: "Intelligence",
    savingThrows: ["Intelligence", "Wisdom"],
    spellcasting: "Full Caster",
    archClasses: ["Arcanist"]
  },
  {
    name: "Mirrorsage",
    info: "Specialized arcane caster who manipulates reflection and illusion magic with unique mirror-based abilities.",
    hitDie: "d6",
    primaryAbility: "Intelligence",
    savingThrows: ["Intelligence", "Charisma"],
    spellcasting: "Full Caster",
    archClasses: ["Reflectionist"]
  },
  {
    name: "Monk",
    info: "Martial artist who channels ki through stances and unarmed mastery.",
    hitDie: "d8",
    primaryAbility: "Dexterity & Wisdom",
    savingThrows: ["Strength", "Dexterity"],
    spellcasting: "Non-Caster",
    archClasses: ["Master"]
  },
  {
    name: "Oracle",
    info: "Living conduit of divine mystery — cursed and blessed in equal measure. Oracles channel Revelations through Revelation Charges, not Weave spell slots.",
    hitDie: "d8",
    primaryAbility: "Charisma",
    savingThrows: ["Constitution", "Charisma"],
    spellcasting: "Revelation Caster (charges)",
    archClasses: ["Mystery (choose at L1)"]
  },
  {
    name: "Paladin",
    info: "Holy warrior with divine magic. Paladins are champions of justice who smite evil and protect the innocent.",
    hitDie: "d10",
    primaryAbility: "Strength or Charisma",
    savingThrows: ["Wisdom", "Charisma"],
    spellcasting: "Half Caster",
    archClasses: ["Sacred Oath (L3)"]
  },
  {
    name: "Ranger",
    info: "Nature warrior with limited spellcasting. Rangers are skilled hunters and guardians of the wilderness.",
    hitDie: "d10",
    primaryAbility: "Dexterity or Strength",
    savingThrows: ["Strength", "Dexterity"],
    spellcasting: "Half Caster",
    archClasses: ["Pathfinder"]
  },
  {
    name: "Shaman",
    info: "Spiritual magic user who communes with spirits and ancestors. Shamans bridge the gap between the living and spirit worlds.",
    hitDie: "d8",
    primaryAbility: "Wisdom",
    savingThrows: ["Constitution", "Wisdom"],
    spellcasting: "Full Caster",
    archClasses: ["Spiritwalker"]
  },
  {
    name: "Soldier",
    info: "Military combatant trained in warfare and tactics. Soldiers are disciplined fighters who excel in organized combat.",
    hitDie: "d10",
    primaryAbility: "Strength or Dexterity",
    savingThrows: ["Strength", "Constitution"],
    spellcasting: "Non-Caster",
    archClasses: ["Commander"]
  },
  {
    name: "Thief",
    info: "Rogue with potential spellcasting features. Thieves are masters of stealth, deception, and acquiring what others possess.",
    hitDie: "d8",
    primaryAbility: "Dexterity",
    savingThrows: ["Dexterity", "Intelligence"],
    spellcasting: "Third Caster (Optional)",
    archClasses: ["Rake"]
  },
  {
    name: "Tinker",
    info: "Inventor and gadgeteer who creates mechanical devices and infuses them with magic. Tinkers blend technology with arcane knowledge.",
    hitDie: "d8",
    primaryAbility: "Intelligence",
    savingThrows: ["Constitution", "Intelligence"],
    spellcasting: "Half Caster",
    archClasses: ["Mechanist"]
  },
  {
    name: "Warrior",
    info: "Combat specialist focused on martial prowess. Warriors are masters of weapons and armor, excelling in direct confrontation.",
    hitDie: "d10",
    primaryAbility: "Strength or Dexterity",
    savingThrows: ["Strength", "Constitution"],
    spellcasting: "Non-Caster",
    archClasses: ["Juggernaut"]
  },
  {
    name: "Wizard",
    info: "Scholarly arcane spellcaster who studies magic through rigorous academic pursuit. Wizards are the ultimate masters of arcane lore.",
    hitDie: "d6",
    primaryAbility: "Intelligence",
    savingThrows: ["Intelligence", "Wisdom"],
    spellcasting: "Full Caster",
    archClasses: ["Arcanist"]
  }
];

if (process.env.NODE_ENV !== "production") {
  const pickerNames = classes.map((c) => c.name).sort();
  const canon = [...CANON_CLASSES].sort();
  const drift =
    pickerNames.length !== canon.length || pickerNames.some((n, i) => n !== canon[i]);
  if (drift) {
    console.warn("CharacterBuilder class picker drift from CANON_CLASSES", {
      pickerNames,
      canon,
    });
  }
}

const skills = [
  { name: "Acrobatics", modifier: "+2" },
  { name: "Animal Handling", modifier: "+0" },
  { name: "Arcana", modifier: "+1" },
  { name: "Athletics", modifier: "+2" },
  { name: "Deception", modifier: "-1" },
  { name: "History", modifier: "+1" },
  { name: "Insight", modifier: "+0" },
  { name: "Intimidation", modifier: "-1" },
  { name: "Investigation", modifier: "+1" },
  { name: "Medicine", modifier: "+0" },
  { name: "Nature", modifier: "+1" },
  { name: "Perception", modifier: "+0" },
  { name: "Performance", modifier: "-1" },
  { name: "Persuasion", modifier: "-1" },
  { name: "Religion", modifier: "+1" },
  { name: "Sleight of Hand", modifier: "+2" },
  { name: "Stealth", modifier: "+2" },
  { name: "Survival", modifier: "+0" }
];

type CharacterBuilderProps = {
  /** Opens COSMOLOGY tab — Umbrin key terms + Obsidian Burn draft canon */
  onOpenLore?: () => void;
};

export default function CharacterBuilder({ onOpenLore }: CharacterBuilderProps = {}) {
  const [selectedRace, setSelectedRace] = useState<string>("");
  const [selectedSubrace, setSelectedSubrace] = useState<string>("");
  const [raceQuery, setRaceQuery] = useState<string>("");
  const [selectedClass, setSelectedClass] = useState<string>("");
  const [selectedArchClass, setSelectedArchClass] = useState<string>("");
  const [resonancePoints, setResonancePoints] = useState<number>(3);
  const [appearance, setAppearance] = useState({
    body: "Athletic",
    skin: "#c4a484",
    hair: "#1a1a1a",
    eyes: "#1565c0",
    accent: "#d97706",
    gearTint: "#334155",
  });
  const [selectedBackground, setSelectedBackground] = useState<string>("");
  const [reputationScores, setReputationScores] = useState<Record<string, number>>({});
  const [characterName, setCharacterName] = useState<string>("");
  const [characterId, setCharacterId] = useState<string>("");
  const [characterNotes, setCharacterNotes] = useState<string>("");
  const [builderView, setBuilderView] = useState<"build" | "sheet">("build");
  const [savedCharacters, setSavedCharacters] = useState<ReturnType<typeof loadSavedCharacters>>([]);
  const [selectedFeats, setSelectedFeats] = useState<string[]>([]);
  const [featFilter, setFeatFilter] = useState<string>("All");
  const [featQuery, setFeatQuery] = useState<string>("");
  const [currentLevel, setCurrentLevel] = useState<number>(1);
  const [currentXP, setCurrentXP] = useState<number>(0);
  const [selectedAlignment, setSelectedAlignment] = useState<string>("");
  const [abilityGenerationMethod, setAbilityGenerationMethod] = useState<string>("preset");
  const [abilities, setAbilities] = useState(defaultAbilities);
  const [pointBuyRemaining, setPointBuyRemaining] = useState<number>(pointBuyPoints);
  const [standardArrayAssignments, setStandardArrayAssignments] = useState<number[]>([15, 14, 13, 12, 10, 8]);
  
  // Spell management state
  const [spellSearchQuery, setSpellSearchQuery] = useState<string>("");
  const [selectedSpellSchool, setSelectedSpellSchool] = useState<string>("All");
  const [selectedSpellLevel, setSelectedSpellLevel] = useState<string>("All");
  const [knownSpells, setKnownSpells] = useState<string[]>([]);
  const [preparedSpells, setPreparedSpells] = useState<string[]>([]);
  const [backgroundFilter, setBackgroundFilter] = useState<string>("");
  const [spellClassOnly, setSpellClassOnly] = useState<boolean>(true);
  const [selectedSacredOath, setSelectedSacredOath] = useState<string>("");
  const [selectedDruidCircle, setSelectedDruidCircle] = useState<string>("");
  const [selectedOracleMystery, setSelectedOracleMystery] = useState<string>("");
  const [selectedOracleCurse, setSelectedOracleCurse] = useState<string>("");
  const [secondaryClass, setSecondaryClass] = useState<string>("");
  const [secondaryLevel, setSecondaryLevel] = useState<number>(1);

  const visibleRaces = useMemo(() => {
    const q = raceQuery.trim().toLowerCase();
    if (!q) return sortedRaces;
    return sortedRaces.filter(
      (race) =>
        race.name.toLowerCase().includes(q) ||
        race.subraces?.some((s) => s.toLowerCase().includes(q)) ||
        race.traits?.some((t) => t.toLowerCase().includes(q)) ||
        race.languages?.some((l) => l.toLowerCase().includes(q))
    );
  }, [raceQuery]);

  const visibleFeats = useMemo(() => {
    const query = featQuery.trim().toLowerCase();
    return feats.filter(
      (feat) =>
        !feat.deprecated &&
        feat.id !== "skill_feats1_master_tracker" &&
        (featFilter === "All" || feat.type === featFilter) &&
        (!query || feat.name.toLowerCase().includes(query))
    );
  }, [featFilter, featQuery]);

  // Resonance canon (RESONANCE_CANON.md) — max RP from class/level/reputation; does not
  // clamp/overwrite the player-editable resonancePoints counter.
  const resonanceMax = resolveMaxRp(
    selectedClass,
    currentLevel,
    reputationScores,
    secondaryClass ? { secondaryClass, secondaryLevel } : undefined
  );

  const previewSpellCost = (spell: { level: number; school: string }) =>
    computeSpellCost(spell, {
      className: selectedClass,
      alignment: selectedAlignment,
      reputation: reputationScores,
    });

  const getFilteredSpells = () => {
    let filteredSpells = Object.values(SPELLS);

    if (spellSearchQuery.trim()) {
      filteredSpells = searchSpells(spellSearchQuery);
    }

    if (spellClassOnly && selectedClass && isSpellcasterClass(selectedClass)) {
      filteredSpells = filterSpellsForClass(filteredSpells, selectedClass, {
        schoolFilter: selectedSpellSchool,
        levelFilter: selectedSpellLevel,
      });
    } else {
      if (selectedSpellSchool !== "All") {
        filteredSpells = filteredSpells.filter((spell) => spell.school === selectedSpellSchool);
      }
      if (selectedSpellLevel !== "All") {
        const level = selectedSpellLevel === "Cantrips" ? 0 : parseInt(selectedSpellLevel, 10);
        filteredSpells = filteredSpells.filter((spell) => spell.level === level);
      }
      filteredSpells = filteredSpells.sort((a, b) =>
        a.level !== b.level ? a.level - b.level : a.name.localeCompare(b.name)
      );
    }

    return filteredSpells;
  };

  const toggleKnownSpell = (spellKey: string) => {
    setKnownSpells(prev => 
      prev.includes(spellKey) 
        ? prev.filter(key => key !== spellKey)
        : [...prev, spellKey]
    );
  };

  const togglePreparedSpell = (spellKey: string) => {
    if (!knownSpells.includes(spellKey)) return;
    setPreparedSpells(prev => 
      prev.includes(spellKey) 
        ? prev.filter(key => key !== spellKey)
        : [...prev, spellKey]
    );
  };

  // Handle ability generation method changes
  const handleGenerationMethodChange = (method: string) => {
    setAbilityGenerationMethod(method);
    
    switch (method) {
      case "random":
        const randomAbilities = generateRandomAbilities();
        const updatedRandomAbilities = updateAbilityModifiers(randomAbilities);
        setAbilities(updatedRandomAbilities);
        break;
      case "preset":
        const presetAbilities = applyStandardArray(standardArrayAssignments);
        const updatedPresetAbilities = updateAbilityModifiers(presetAbilities);
        setAbilities(updatedPresetAbilities);
        break;
      case "buyin":
        const buyinAbilities = defaultAbilities.map(ability => ({ ...ability, score: 8 }));
        const updatedBuyinAbilities = updateAbilityModifiers(buyinAbilities);
        setAbilities(updatedBuyinAbilities);
        setPointBuyRemaining(pointBuyPoints);
        break;
    }
  };

  // Handle point buy score changes
  const handlePointBuyChange = (abilityIndex: number, newScore: number) => {
    if (newScore < pointBuyBase || newScore > pointBuyMax) return;
    
    const newAbilities = [...abilities];
    const oldCost = getPointBuyCost(newAbilities[abilityIndex].score);
    const newCost = getPointBuyCost(newScore);
    const costDifference = newCost - oldCost;
    
    if (pointBuyRemaining - costDifference >= 0) {
      newAbilities[abilityIndex] = { ...newAbilities[abilityIndex], score: newScore };
      const updatedAbilities = updateAbilityModifiers(newAbilities);
      setAbilities(updatedAbilities);
      setPointBuyRemaining(pointBuyRemaining - costDifference);
    }
  };

  // Handle standard array assignment changes
  const handleStandardArrayChange = (abilityIndex: number, value: number) => {
    const newAssignments = [...standardArrayAssignments];
    const oldValue = newAssignments[abilityIndex];
    
    // Find where the new value is currently assigned and swap
    const swapIndex = newAssignments.findIndex(v => v === value);
    if (swapIndex !== -1) {
      newAssignments[swapIndex] = oldValue;
    }
    newAssignments[abilityIndex] = value;
    
    setStandardArrayAssignments(newAssignments);
    const newAbilities = applyStandardArray(newAssignments);
    const updatedAbilities = updateAbilityModifiers(newAbilities);
    setAbilities(updatedAbilities);
  };

  useEffect(() => {
    setSavedCharacters(loadSavedCharacters());
  }, []);

  // Apply racial bonuses when race changes
  useEffect(() => {
    if (selectedRace) {
      const race = races.find(r => r.name === selectedRace);
      if (race) {
        const baseAbilities = abilityGenerationMethod === "preset" 
          ? applyStandardArray(standardArrayAssignments)
          : abilities;
        const racialAbilities = applyRacialBonuses(baseAbilities, race);
        setAbilities(racialAbilities);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- omit `abilities`: only re-run on race/method/array, not every manual score edit (avoids stacking racial ASI).
  }, [selectedRace, abilityGenerationMethod, standardArrayAssignments]);


  const buildCharacterPayload = () => ({
    id: characterId || undefined,
    name: characterName.trim() || (selectedRace ? `${selectedRace} ${selectedClass || "Adventurer"}` : "Unnamed Adventurer"),
    race: selectedRace,
    subrace: selectedSubrace,
    class: selectedClass,
    archClass: selectedArchClass,
    resonancePoints,
    appearance,
    background: selectedBackground,
    feats: selectedFeats,
    level: currentLevel,
    xp: currentXP,
    alignment: selectedAlignment,
    abilities: abilities.map((a) => ({ name: a.name, score: a.score, modifier: a.modifier })),
    knownSpells: normalizeSpellKeys(knownSpells),
    preparedSpells: normalizeSpellKeys(preparedSpells),
    sacredOath: selectedSacredOath,
    druidCircle: selectedDruidCircle,
    oracleMystery: selectedOracleMystery,
    oracleCurse: selectedOracleCurse,
    notes: characterNotes,
    reputation: reputationScores,
    secondaryClass: secondaryClass || "",
    secondaryLevel: secondaryClass
      ? Math.max(1, Math.min(20, secondaryLevel))
      : undefined,
    exportedAt: new Date().toISOString(),
  });

  const exportCharacter = () => {
    const payload = buildCharacterPayload();
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${payload.name.replace(/\s+/g, "_").toLowerCase() || "character"}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const saveCharacter = () => {
    const saved = upsertCharacter(buildCharacterPayload());
    setCharacterId(saved.id);
    setCharacterName(saved.name || "");
    setSavedCharacters(loadSavedCharacters());
    setBuilderView("sheet");
  };

  const loadCharacter = (c: ReturnType<typeof loadSavedCharacters>[number]) => {
    const norm = normalizeCharacter(c);
    if (!norm) return;
    setCharacterId(norm.id || "");
    setCharacterName(norm.name || "");
    setSelectedRace(norm.race || "");
    setSelectedSubrace(norm.subrace || "");
    setSelectedClass(norm.class || "");
    setSelectedArchClass(norm.archClass || "");
    setResonancePoints(norm.resonancePoints ?? 3);
    setSelectedBackground(norm.background || "");
    setSelectedFeats(norm.feats || []);
    setCurrentLevel(norm.level || 1);
    setCurrentXP(norm.xp || 0);
    setSelectedAlignment(norm.alignment || "");
    if (norm.abilities?.length) {
      setAbilities(
        norm.abilities.map((a: { name: string; score: number; modifier: number }) => ({
          ...a,
          modifier: Number(a.modifier),
        }))
      );
    }
    setKnownSpells(norm.knownSpells || []);
    setPreparedSpells(norm.preparedSpells || []);
    setCharacterNotes(norm.notes || "");
    setSelectedSacredOath(norm.sacredOath || "");
    setSelectedDruidCircle(norm.druidCircle || "");
    setSelectedOracleMystery(norm.oracleMystery || "");
    setSelectedOracleCurse(norm.oracleCurse || "");
    setSecondaryClass(norm.secondaryClass || "");
    setSecondaryLevel(norm.secondaryLevel ?? 1);
    setReputationScores(norm.reputation || {});
    setBuilderView("build");
  };

  const removeSaved = (id: string) => {
    setSavedCharacters(deleteCharacter(id));
    if (characterId === id) setCharacterId("");
  };

  const resetCharacter = () => {
    setCharacterId("");
    setCharacterName("");
    setCharacterNotes("");
    setSelectedRace("");
    setSelectedSubrace("");
    setSelectedClass("");
    setSelectedArchClass("");
    setResonancePoints(3);
    setSelectedBackground("");
    setSelectedFeats([]);
    setCurrentLevel(1);
    setCurrentXP(0);
    setSelectedAlignment("");
    setAbilities(defaultAbilities);
    setKnownSpells([]);
    setPreparedSpells([]);
    setSelectedSacredOath("");
    setSelectedDruidCircle("");
    setSelectedOracleMystery("");
    setSelectedOracleCurse("");
    setSecondaryClass("");
    setSecondaryLevel(1);
    setReputationScores({});
    setBuilderView("build");
  };

  const randomCharacter = () => {
    const race = races[Math.floor(Math.random() * races.length)];
    const cls = classes[Math.floor(Math.random() * classes.length)];
    setSelectedRace(race.name);
    setSelectedSubrace(race.subraces?.[0] || "");
    setSelectedClass(cls.name);
    const featPool = feats;
    const pick = featPool[Math.floor(Math.random() * featPool.length)];
    setSelectedFeats(pick ? [pick.name] : []);
  };

  const selectedRaceData = races.find((r) => r.name === selectedRace);
  const selectedClassData = classes.find((c) => c.name === selectedClass);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4 md:p-6">
      <div className="flex flex-col gap-4 mb-6 max-w-[1600px] mx-auto">
        <div className="flex flex-wrap justify-between items-start gap-3">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-amber-400">Character Builder</h1>
            <p className="text-amber-100/70 text-sm mt-1">Forge an Aethel hero — save, then run them in Session.</p>
          </div>
          <div className="flex gap-2 flex-wrap">
            <Button variant={builderView === "build" ? "default" : "outline"} className={builderView === "build" ? "bg-amber-600" : ""} onClick={() => setBuilderView("build")}>Build</Button>
            <Button variant={builderView === "sheet" ? "default" : "outline"} className={builderView === "sheet" ? "bg-amber-600" : ""} onClick={() => setBuilderView("sheet")}>Sheet</Button>
            <Button className="amber-button" onClick={randomCharacter}><Dice1 className="w-4 h-4 mr-2" />RANDOM</Button>
            <Button className="amber-button" onClick={resetCharacter}><Plus className="w-4 h-4 mr-2" />NEW</Button>
            <Button className="amber-button" onClick={() => { navigator.clipboard.writeText(JSON.stringify(buildCharacterPayload(), null, 2)); }}><Copy className="w-4 h-4 mr-2" />COPY JSON</Button>
            <Button className="amber-button" onClick={saveCharacter}><Save className="w-4 h-4 mr-2" />SAVE</Button>
            <Button className="amber-button" onClick={exportCharacter}><Download className="w-4 h-4 mr-2" />EXPORT</Button>
          </div>
        </div>
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-amber-200/70">Character name</label>
            <Input className="bg-black/40 border-amber-700/40 text-amber-50 placeholder:text-amber-200/40" value={characterName} onChange={(e) => setCharacterName(e.target.value)} placeholder="Name your hero" />
          </div>
          <div className="min-w-[220px]">
            <label className="text-xs text-amber-200/70">Load saved</label>
            <select
              className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50"
              value=""
              onChange={(e) => {
                const c = savedCharacters.find((x) => x.id === e.target.value);
                if (c) loadCharacter(c);
              }}
            >
              <option value="">Select a saved character…</option>
              {savedCharacters.map((c) => (
                <option key={c.id} value={c.id}>{characterDisplayName(c)} (L{c.level || 1})</option>
              ))}
            </select>
          </div>
        </div>
        {savedCharacters.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {savedCharacters.slice(0, 8).map((c) => (
              <div key={c.id} className="flex items-center gap-1 bg-black/40 border border-amber-700/30 rounded px-2 py-1 text-xs text-amber-100">
                <button type="button" className="hover:text-amber-300" onClick={() => loadCharacter(c)}>{characterDisplayName(c)}</button>
                <button type="button" className="text-red-400 ml-1" onClick={() => removeSaved(c.id!)}>×</button>
              </div>
            ))}
          </div>
        )}
        <ChargenWarnings character={buildCharacterPayload()} />
      </div>

      {builderView === "sheet" ? (
        <CharacterSheet character={buildCharacterPayload()} onExport={exportCharacter} />
      ) : (
      <>
      <div className="grid grid-cols-12 gap-4 md:gap-6 max-w-[1600px] mx-auto">
        <div className="col-span-12 lg:col-span-4">
          <Card className="bg-slate-900/70 border-amber-600/30">
            <CardHeader className="pb-2">
              <div className="flex justify-between items-center">
                <CardTitle className="text-amber-300">Origin</CardTitle>
                <Badge className="bg-amber-700/80 text-amber-50 text-xs border-amber-500/40">Aethel</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="race" className="w-full">
                <TabsList className="grid w-full grid-cols-4 bg-black/40 border border-amber-700/40 p-1 h-auto">
                  <TabsTrigger value="race" className="text-xs data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">People</TabsTrigger>
                  <TabsTrigger value="class" className="text-xs data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Class</TabsTrigger>
                  <TabsTrigger value="feats" className="text-xs data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Feats</TabsTrigger>
                  <TabsTrigger value="background" className="text-xs data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Past</TabsTrigger>
                </TabsList>

                <TabsContent value="race" className="space-y-4 mt-3">
                  <div>
                    <p className="text-sm text-amber-100/60 mb-3">
                      Peoples of Aethel — Umbrin pinned first; Amphibian through Undead.
                    </p>
                    <label className="text-xs text-amber-200/70 mb-1 block">Search people</label>
                    <div className="relative mb-3">
                      <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-amber-200/50" />
                      <Input
                        value={raceQuery}
                        onChange={(e) => setRaceQuery(e.target.value)}
                        placeholder="Filter by name, lineage, trait…"
                        className="pl-9 bg-black/40 border-amber-700/40 text-amber-50"
                      />
                    </div>
                    <label className="text-xs text-amber-200/70 mb-1 block">People</label>
                    <select
                      className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50"
                      value={selectedRace}
                      onChange={(e) => {
                        setSelectedRace(e.target.value);
                        setSelectedSubrace("");
                      }}
                    >
                      <option value="">Choose a people…</option>
                      {visibleRaces.map((race) => (
                        <option key={race.name} value={race.name}>
                          {race.name}
                        </option>
                      ))}
                    </select>
                    {selectedRace === PINNED_RACE && (
                      <p className="text-xs text-violet-200/80 mt-2 leading-snug">
                        <span className="text-violet-300/90">Obsidian Burn</span>{" "}
                        — Calan&apos;thir and the
                        First Choir banished Umbrin forebears; flesh cooled to obsidian sheen.{" "}
                        {onOpenLore ? (
                          <button
                            type="button"
                            onClick={onOpenLore}
                            className="text-violet-300 underline underline-offset-2 hover:text-violet-100"
                          >
                            Lore
                          </button>
                        ) : null}
                      </p>
                    )}
                    {raceQuery && visibleRaces.length === 0 && (
                      <p className="text-xs text-amber-100/50 mt-1 italic">No peoples match that filter.</p>
                    )}

                    {selectedRace && (
                      <div className="mt-3">
                        <label className="text-xs text-amber-200/70 mb-1 block">Lineage</label>
                        <select
                          className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50"
                          value={selectedSubrace}
                          onChange={(e) => setSelectedSubrace(e.target.value)}
                        >
                          <option value="">Choose lineage…</option>
                          {selectedRaceData?.subraces?.map((subrace) => (
                            <option key={subrace} value={subrace}>
                              {subrace}
                            </option>
                          ))}
                        </select>
                        {selectedSubrace && subraceVariant(selectedSubrace) && (
                          <div className="mt-3 border border-amber-700/40 rounded p-3 space-y-1 text-xs bg-black/30">
                            <div className="text-amber-300 font-semibold">{selectedSubrace}</div>
                            <div className="text-amber-100/80">
                              <span className="text-amber-400">Variant:</span>{" "}
                              {subraceVariant(selectedSubrace)?.ability}
                            </div>
                            <div className="text-amber-100/80">
                              <span className="text-amber-400">Racial feat:</span>{" "}
                              {subraceVariant(selectedSubrace)?.racialFeat.name} —{" "}
                              {subraceVariant(selectedSubrace)?.racialFeat.effect}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {selectedRaceData && (
                      <div className="mt-4 border border-amber-700/40 rounded-lg p-3 bg-black/30">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-semibold text-amber-200">{selectedRaceData.name}</span>
                          <span className="text-xs text-amber-200/60">Size: {selectedRaceData.size}</span>
                        </div>
                        <p className="text-xs text-amber-100/70 mb-2">{selectedRaceData.info}</p>
                        <div className="space-y-1 text-xs text-amber-100/80">
                          <div><span className="text-amber-400">Ability:</span> {selectedRaceData.abilityScoreIncrease}</div>
                          <div><span className="text-amber-400">Speed:</span> {selectedRaceData.speed}</div>
                          <div><span className="text-amber-400">Traits:</span> {selectedRaceData.traits.join(", ")}</div>
                          <div><span className="text-amber-400">Languages:</span> {selectedRaceData.languages.join(", ")}</div>
                          {selectedRaceData.subraces && (
                            <div><span className="text-amber-400">Lineages:</span> {selectedRaceData.subraces.join(", ")}</div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="class" className="space-y-4 mt-3">
                  <div>
                    <p className="text-sm text-amber-100/60 mb-3">
                      Path and role — base class plus optional arch path.
                    </p>
                    <label className="text-xs text-amber-200/70 mb-1 block">Class</label>
                    <select
                      className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50"
                      value={selectedClass}
                      onChange={(e) => setSelectedClass(e.target.value)}
                    >
                      <option value="">Choose a class…</option>
                      {classes.map((cls) => (
                        <option key={cls.name} value={cls.name}>
                          {cls.name}
                        </option>
                      ))}
                    </select>

                    {selectedClass && (
                      <div className="mt-3">
                        <label className="text-xs text-amber-200/70 mb-1 block">Arch path</label>
                        <select
                          className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50"
                          value={selectedArchClass}
                          onChange={(e) => setSelectedArchClass(e.target.value)}
                        >
                          <option value="">None yet (unlock in play)</option>
                          {prestigeForBaseClass(selectedClass).map((p) => (
                            <option key={p.name} value={p.name}>{p.name}</option>
                          ))}
                        </select>
                        {selectedArchClass && (
                          <p className="mt-1 text-[11px] text-amber-100/60">
                            This records your intended path. Review its requirements and draft markers on the{" "}
                            <span className="text-amber-200">Paths</span> tab; selection does not grant its
                            prerequisites or features.
                          </p>
                        )}
                      </div>
                    )}

                    {selectedClass && (
                      <div className="mt-3 space-y-2 border border-amber-700/30 rounded-lg p-3 bg-black/20">
                        <p className="text-[11px] text-amber-200/60">
                          Optional multiclass — affects Weave max RP per{" "}
                          <span className="text-amber-300">Resonance canon §7</span> (highest pool + 25% secondary).
                          Oracle, Soldier, and Warrior do not add a Weave pool.
                        </p>
                        <div className="grid grid-cols-2 gap-2">
                          <div>
                            <label className="text-xs text-amber-200/70 mb-1 block">Secondary class</label>
                            <select
                              className="w-full bg-black/40 border border-amber-700/40 rounded px-2 py-2 text-amber-50 text-sm"
                              value={secondaryClass}
                              onChange={(e) => setSecondaryClass(e.target.value)}
                            >
                              <option value="">None (single-class)</option>
                              {classes
                                .filter((cls) => cls.name !== selectedClass)
                                .map((cls) => (
                                  <option key={cls.name} value={cls.name}>
                                    {cls.name}
                                  </option>
                                ))}
                            </select>
                          </div>
                          <div>
                            <label className="text-xs text-amber-200/70 mb-1 block">Secondary level</label>
                            <select
                              className="w-full bg-black/40 border border-amber-700/40 rounded px-2 py-2 text-amber-50 text-sm"
                              value={secondaryLevel}
                              disabled={!secondaryClass}
                              onChange={(e) => setSecondaryLevel(Number(e.target.value))}
                            >
                              {Array.from({ length: 20 }, (_, i) => i + 1).map((lvl) => (
                                <option key={lvl} value={lvl}>
                                  L{lvl}
                                </option>
                              ))}
                            </select>
                          </div>
                        </div>
                        {secondaryClass && (() => {
                          const breakdown = multiclassRpBreakdown(resonanceMax);
                          if (!breakdown) {
                            return (
                              <div className="rounded border border-amber-700/30 bg-black/20 p-2 text-[11px] text-amber-100/70">
                                <span className="font-medium text-amber-200">
                                  {secondaryClass} L{secondaryLevel}
                                </span>{" "}
                                is recorded as a secondary class. It does not add a second Weave pool here, so the
                                current RP maximum uses the eligible class pool only.
                              </div>
                            );
                          }
                          return (
                            <div className="rounded border border-purple-700/40 bg-purple-950/25 p-2 text-[11px] text-amber-100/75 space-y-0.5">
                              <div className="flex items-center gap-1.5">
                                <span className="text-purple-300 font-medium">Multiclass RP merge</span>
                                <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 border-purple-500/50 text-purple-200">
                                  Canon
                                </Badge>
                              </div>
                              {breakdown.lines.map((line) => (
                                <div key={line}>{line}</div>
                              ))}
                            </div>
                          );
                        })()}
                      </div>
                    )}

                    {selectedClassData && (
                      <div className="mt-4 border border-amber-700/40 rounded-lg p-3 bg-black/30 space-y-3">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-semibold text-amber-200">{selectedClassData.name}</span>
                          <span className="text-xs text-amber-200/60">Hit Die: {selectedClassData.hitDie}</span>
                        </div>
                        <p className="text-xs text-amber-100/70 mb-2">{selectedClassData.info}</p>
                        <div className="space-y-1 text-xs text-amber-100/80">
                          <div><span className="text-amber-400">Primary:</span> {selectedClassData.primaryAbility}</div>
                          <div><span className="text-amber-400">Saves:</span> {selectedClassData.savingThrows.join(", ")}</div>
                          <div><span className="text-amber-400">Weave:</span> {selectedClassData.spellcasting}</div>
                          {selectedClassData.archClasses.length > 0 && (
                            <div><span className="text-amber-400">Arch paths:</span> {selectedClassData.archClasses.join(", ")}</div>
                          )}
                        </div>
                        <ClassCeilingCapsCallout className={selectedClass} compact />
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="feats" className="space-y-4 mt-3">
                  <div>
                    <p className="text-sm text-amber-100/60 mb-3">
                      Enhance your hero with optional feats.
                    </p>
                    <label className="text-xs text-amber-200/70 mb-1 block">Filter by type</label>
                    <select
                      className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50 mb-4"
                      value={featFilter}
                      onChange={(e) => setFeatFilter(e.target.value)}
                    >
                      <option value="All">All types</option>
                      {[...new Set(feats.filter((f) => !f.deprecated).map((f) => f.type))].sort().map((t) => (
                        <option key={t} value={t}>{t}</option>
                      ))}
                    </select>
                    <label className="text-xs text-amber-200/70 mb-1 block">Search feats</label>
                    <Input
                      value={featQuery}
                      onChange={(e) => setFeatQuery(e.target.value)}
                      placeholder="Filter by feat name…"
                      className="bg-black/40 border-amber-700/40 text-amber-50 mb-4"
                    />

                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {visibleFeats.map((feat) => (
                        <div key={feat.name} className="border border-amber-700/40 rounded-lg p-3 bg-black/30">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-amber-200">{feat.name}</span>
                            <div className="flex items-center gap-1">
                              {feat.draft && (
                                <Badge variant="outline" className="text-[10px] border-amber-500/40 text-amber-300/80">
                                  Draft
                                </Badge>
                              )}
                              <Badge variant="outline" className="text-xs border-amber-600/50 text-amber-200/80">{feat.type}</Badge>
                            </div>
                          </div>
                          <p className="text-xs text-amber-100/70 mb-2">{feat.description}</p>
                          <div className="space-y-1 text-xs text-amber-100/80">
                            <div><span className="text-amber-400">Prerequisite:</span> {feat.prerequisite}</div>
                            <div><span className="text-amber-400">Effect:</span> {feat.effect}</div>
                          </div>
                          <Button
                            size="sm"
                            className="mt-2 w-full bg-amber-700 hover:bg-amber-600 text-amber-50"
                            onClick={() => {
                              if (!selectedFeats.includes(feat.name)) {
                                setSelectedFeats([...selectedFeats, feat.name]);
                              }
                            }}
                            disabled={selectedFeats.includes(feat.name)}
                          >
                            {selectedFeats.includes(feat.name) ? "Selected" : "Take feat"}
                          </Button>
                        </div>
                      ))}
                      {visibleFeats.length === 0 && (
                        <p className="rounded-lg border border-amber-700/30 bg-black/20 p-3 text-xs text-amber-100/60">
                          No feats match the current filter. Change the type or search to browse available feat cards.
                        </p>
                      )}
                    </div>

                    {selectedFeats.length > 0 && (
                      <div className="mt-4 p-3 bg-amber-950/40 border border-amber-600/40 rounded-lg">
                        <h4 className="text-sm font-semibold text-amber-300 mb-2">Chosen feats</h4>
                        <div className="space-y-1">
                          {selectedFeats.map((featName) => (
                            <div key={featName} className="flex items-center justify-between">
                              <span className="text-xs text-amber-100 flex items-center gap-1.5">
                                {featName}
                                {feats.find((feat) => feat.name === featName)?.draft && (
                                  <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 border-amber-500/40 text-amber-300/80">
                                    Draft
                                  </Badge>
                                )}
                              </span>
                              <Button
                                size="sm"
                                variant="destructive"
                                className="h-6 px-2 text-xs"
                                onClick={() => setSelectedFeats(selectedFeats.filter(f => f !== featName))}
                              >
                                Remove
                              </Button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="background" className="space-y-4 mt-3">
                  {(() => {
                    const filteredBackgrounds = BACKGROUNDS.filter(
                      (background) =>
                        backgroundFilter === "" ||
                        background.name.toLowerCase().includes(backgroundFilter.toLowerCase())
                    );
                    const selectedBg = getBackgroundByName(selectedBackground);

                    return (
                      <div className="space-y-6">
                        <Input
                          placeholder="Search backgrounds…"
                          value={backgroundFilter}
                          onChange={(e) => setBackgroundFilter(e.target.value)}
                          className="bg-black/40 border-amber-700/40 text-amber-50 placeholder:text-amber-200/40"
                        />

                        <div className="grid gap-3 max-h-[520px] overflow-y-auto pr-1">
                          {filteredBackgrounds.map((background) => (
                            <Card
                              key={background.name}
                              className={`p-4 cursor-pointer transition-colors border-amber-700/40 ${
                                selectedBackground === background.name
                                  ? "ring-2 ring-amber-500 bg-amber-950/40"
                                  : "bg-black/30 hover:bg-black/50"
                              }`}
                              onClick={() => {
                                setSelectedBackground(background.name);
                                setReputationScores((prev) =>
                                  applyBackgroundReputation(prev, background.name)
                                );
                              }}
                            >
                              <div className="space-y-3">
                                <div className="flex items-center justify-between">
                                  <h3 className="text-base font-semibold text-amber-200">{background.name}</h3>
                                  {selectedBackground === background.name && (
                                    <Badge className="bg-amber-600">Selected</Badge>
                                  )}
                                </div>
                                <p className="text-sm text-amber-100/70">{background.description}</p>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-amber-100/70">
                                  <div>
                                    <span className="font-medium text-amber-200">Skills:</span>{" "}
                                    {background.skillProficiencies.join(", ")}
                                  </div>
                                  {background.toolProficiencies.length > 0 && (
                                    <div>
                                      <span className="font-medium text-amber-200">Tools:</span>{" "}
                                      {background.toolProficiencies.join(", ")}
                                    </div>
                                  )}
                                  {background.languages && (
                                    <div>
                                      <span className="font-medium text-amber-200">Languages:</span>{" "}
                                      {background.languages.join(", ")}
                                    </div>
                                  )}
                                  <div>
                                    <span className="font-medium text-amber-200">{background.feature}:</span>{" "}
                                    {background.featureDescription}
                                  </div>
                                </div>
                              </div>
                            </Card>
                          ))}
                        </div>

                        {selectedBg && (
                          <Card className="p-4 bg-amber-950/40 border-amber-600/50 space-y-4">
                            <div>
                              <h3 className="text-base font-semibold text-amber-300 mb-2">Selected: {selectedBg.name}</h3>
                              <p className="text-sm text-amber-100/80">{selectedBg.featureDescription}</p>
                              <p className="text-xs text-amber-200/60 mt-2">
                                Rulebook starting reputation: {selectedBg.startingReputation}
                              </p>
                            </div>
                            <div>
                              <h4 className="text-sm font-medium text-amber-300 mb-2">Faction standing</h4>
                              <p className="text-[10px] text-amber-200/50 mb-2">
                                Adjust scores for playtest prep. Changing background re-applies its starting values.
                              </p>
                              <ReputationPanel
                                scores={reputationScores}
                                onChange={setReputationScores}
                                mode="full"
                              />
                              {Object.keys(reputationScores).length > 0 && (
                                <p className="text-[10px] text-amber-200/45 mt-2">{reputationSummary(reputationScores)}</p>
                              )}
                            </div>
                          </Card>
                        )}
                      </div>
                    );
                  })()}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        <div className="col-span-12 lg:col-span-4">
          <Card className="bg-slate-900/70 border-amber-600/30 mb-4">
            <CardHeader className="pb-2">
              <CardTitle className="text-amber-300 text-center">
                {characterName.trim() || selectedClass || "New Hero"}
              </CardTitle>
              {(selectedRace || selectedClass) && (
                <p className="text-center text-xs text-amber-200/60 mt-1">
                  {[
                    selectedRace && `${selectedRace}${selectedSubrace ? ` · ${selectedSubrace}` : ""}`,
                    selectedClass,
                    `Level ${currentLevel}`,
                  ].filter(Boolean).join(" · ")}
                </p>
              )}
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="alignment" className="w-full">
                <TabsList className="flex w-full flex-wrap h-auto gap-1 bg-black/40 border border-amber-700/40 p-1">
                  <TabsTrigger value="alignment" className="text-xs flex-1 min-w-[64px] data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Ethos</TabsTrigger>
                  <TabsTrigger value="combat" className="text-xs flex-1 min-w-[64px] data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Combat</TabsTrigger>
                  <TabsTrigger value="proficiencies" className="text-xs flex-1 min-w-[64px] data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Gear</TabsTrigger>
                  <TabsTrigger value="spells" className="text-xs flex-1 min-w-[64px] data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Weave</TabsTrigger>
                  <TabsTrigger value="features" className="text-xs flex-1 min-w-[64px] data-[state=active]:bg-amber-600 data-[state=active]:text-amber-50 text-amber-200/70">Paths</TabsTrigger>
                </TabsList>
                
                <TabsContent value="alignment" className="mt-4">
                  <div className="space-y-4">
                    <h3 className="text-amber-300 font-semibold text-center text-sm">Ethos & alignment</h3>
                    <div className="grid grid-cols-3 gap-2">
                      {[
                        "Lawful Good", "Neutral Good", "Chaotic Good",
                        "Lawful Neutral", "True Neutral", "Chaotic Neutral",
                        "Lawful Evil", "Neutral Evil", "Chaotic Evil"
                      ].map((alignment) => (
                        <Button
                          key={alignment}
                          variant={selectedAlignment === alignment ? "default" : "outline"}
                          className={`text-xs p-2 h-auto ${
                            selectedAlignment === alignment
                              ? "bg-amber-600 text-amber-50 border-amber-500"
                              : "text-amber-100/80 border-amber-700/50 hover:bg-amber-950/50 hover:text-amber-50"
                          }`}
                          onClick={() => setSelectedAlignment(alignment)}
                        >
                          {alignment}
                        </Button>
                      ))}
                    </div>
                    {selectedAlignment && (
                      <div className="text-center text-amber-100/80 text-sm mt-2">
                        Chosen: <span className="font-semibold text-amber-200">{selectedAlignment}</span>
                      </div>
                    )}
                    {!selectedAlignment && (
                      <p className="text-center text-amber-200/60 text-xs mt-2">
                        No ethos recorded. Choose one to include it when you save this hero and in the existing
                        spell-cost preview.
                      </p>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="combat" className="space-y-4 mt-4">
                  <div className="space-y-3">
                    <h3 className="text-amber-300 font-semibold text-center text-sm">Combat</h3>
                    {!selectedClass ? (
                      <p className="text-center text-amber-200/50 text-sm">Choose a class to see combat notes.</p>
                    ) : (
                      <div className="space-y-3 text-sm">
                        <div className="border border-amber-700/40 rounded p-3 bg-black/30">
                          <div className="text-amber-300 font-medium mb-2">{selectedClass}</div>
                          <ul className="list-disc pl-4 space-y-1 text-amber-50/80 text-xs">
                            {(classDetails[selectedClass as keyof typeof classDetails]?.combat || ["No combat notes yet."]).map((line) => (
                              <li key={line}>{line}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div className="border border-amber-700/40 rounded p-2 bg-black/20">
                            <div className="text-amber-400 mb-1">Hit Die</div>
                            <div className="text-amber-100">{selectedClassData?.hitDie}</div>
                          </div>
                          <div className="border border-amber-700/40 rounded p-2 bg-black/20">
                            <div className="text-amber-400 mb-1">Saves</div>
                            <div className="text-amber-100">{selectedClassData?.savingThrows.join(", ")}</div>
                          </div>
                          <div className="border border-amber-700/40 rounded p-2 col-span-2 bg-black/20">
                            <div className="text-amber-400 mb-1">Primary Ability</div>
                            <div className="text-amber-100">{selectedClassData?.primaryAbility}</div>
                          </div>
                        </div>
                        <div className="border border-purple-700/40 rounded p-3 text-xs bg-purple-950/20">
                          <div className="text-purple-300 font-medium mb-1">Resonance in combat</div>
                          <p className="text-amber-50/70">
                            Current RP: <span className="text-amber-200 font-semibold">{resonancePoints}</span>. Spend to push smites, crescendos, or Weave echoes.
                          </p>
                        </div>
                        <ClassCeilingCapsCallout className={selectedClass} compact />
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="proficiencies" className="space-y-4 mt-4">
                  <div className="space-y-3">
                    <h3 className="text-amber-300 font-semibold text-center text-sm">Proficiencies</h3>
                    {!selectedClass ? (
                      <p className="text-center text-amber-200/50 text-sm">Choose a class to load proficiencies.</p>
                    ) : (
                      <div className="space-y-2 text-xs text-amber-50/80">
                        {(["armor", "weapons", "tools", "skills"] as const).map((key) => {
                          const detail = classDetails[selectedClass as keyof typeof classDetails];
                          const list = detail?.[key] || [];
                          return (
                            <div key={key} className="border border-amber-700/40 rounded p-3 bg-black/30">
                              <div className="text-amber-400 font-medium capitalize mb-1">{key}</div>
                              <div className="text-amber-100/80">{list.length ? list.join(" · ") : "—"}</div>
                            </div>
                          );
                        })}
                        {selectedRaceData && (
                          <div className="border border-amber-700/40 rounded p-3 bg-black/30">
                            <div className="text-amber-400 font-medium mb-1">Racial traits</div>
                            <div className="text-amber-100/80">{selectedRaceData.traits.join(" · ")}</div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="features" className="space-y-4 mt-4">
                  <div className="space-y-4">
                    <h3 className="text-amber-300 font-semibold text-center text-sm">Class & arch paths</h3>
                    {!selectedClass ? (
                      <div className="text-center text-amber-200/50 text-sm">Choose a class to see features and arch paths.</div>
                    ) : (
                      <div className="space-y-3 text-sm text-amber-50/80">
                        <div className="border border-amber-700/40 rounded p-3 bg-black/30">
                          <div className="text-amber-300 font-semibold mb-1">{selectedClass}</div>
                          <p className="text-xs text-amber-100/70">{selectedClassData?.info}</p>
                          <div className="mt-2 text-xs text-amber-200/60">
                            Hit Die: {selectedClassData?.hitDie} · Weave: {selectedClassData?.spellcasting}
                          </div>
                          <div className="mt-3">
                            <LevelFeatureList
                              compact
                              levels={
                                classDetails[selectedClass as keyof typeof classDetails]?.levels as Record<
                                  number,
                                  (string | { text: string; draft?: boolean; source?: string })[]
                                >
                              }
                            />
                          </div>
                          <ClassCeilingCapsCallout className={selectedClass} />
                          <ClassPathDisplay
                            compact
                            archPaths={
                              selectedClass === "Druid" && selectedDruidCircle
                                ? druidPathBlocksForCircle(
                                    selectedDruidCircle,
                                    classPathBlocks(selectedClass).archPaths,
                                    classPathBlocks(selectedClass).heroPaths
                                  ).archPaths
                                : classPathBlocks(selectedClass).archPaths
                            }
                            heroPaths={
                              selectedClass === "Druid" && selectedDruidCircle
                                ? druidPathBlocksForCircle(
                                    selectedDruidCircle,
                                    classPathBlocks(selectedClass).archPaths,
                                    classPathBlocks(selectedClass).heroPaths
                                  ).heroPaths
                                : classPathBlocks(selectedClass).heroPaths
                            }
                            showEmptyHeroPaths
                          />
                          {selectedClass === "Druid" && !selectedDruidCircle && (
                            <p className="text-[11px] text-amber-200/50 mt-2">
                              Choose a Druid Circle below to filter arch path and hero forms for your circle.
                            </p>
                          )}
                        </div>
                        {selectedClass === "Paladin" && (
                          <div className="border border-amber-700/40 rounded p-3 bg-black/30 space-y-2">
                            <div className="text-amber-200 font-medium text-xs">
                              Sacred Oath (L3)
                              {currentLevel >= 3 && !selectedSacredOath && (
                                <span className="text-red-400 ml-1">— required</span>
                              )}
                            </div>
                            <select
                              className={`w-full bg-black/40 border rounded px-3 py-2 text-amber-50 text-xs ${
                                currentLevel >= 3 && !selectedSacredOath
                                  ? "border-red-600/60"
                                  : "border-amber-700/40"
                              }`}
                              value={selectedSacredOath}
                              onChange={(e) => setSelectedSacredOath(e.target.value)}
                            >
                              <option value="">Choose an oath…</option>
                              {SACRED_OATHS.map((o) => (
                                <option key={o.id} value={o.id}>{o.name}</option>
                              ))}
                            </select>
                            {!selectedSacredOath && (
                              <p className="text-[11px] text-amber-200/60">
                                No Sacred Oath recorded. Choose one at L3; until then, this saved hero has no oath
                                selection.
                              </p>
                            )}
                            {selectedSacredOath && (() => {
                              const oath = getOathById(selectedSacredOath);
                              if (!oath) return null;
                              return (
                                <div className="space-y-1 text-xs text-amber-50/80">
                                  {oath.draft && (
                                    <Badge variant="outline" className="text-[10px] border-amber-500/50 text-amber-300">
                                      Draft — pending author review
                                    </Badge>
                                  )}
                                  <p className="text-amber-100/70">{oath.theme}</p>
                                  <div><span className="text-amber-400">Smite:</span> {oath.smiteType}</div>
                                  <div><span className="text-amber-400">Aura:</span> {oath.auraEffect}</div>
                                  <div><span className="text-amber-400">Signature (L11):</span> {oath.signaturePower}</div>
                                  <div className="mt-2">
                                    <span className="text-amber-400">Conduct:</span>
                                    <ul className="list-disc pl-4 mt-1">
                                      {oath.conductClause.map((c) => <li key={c}>{c}</li>)}
                                    </ul>
                                  </div>
                                  <div className="mt-2">
                                    <span className="text-amber-400">Revelation spells:</span>
                                    <ul className="list-disc pl-4 mt-1">
                                      {oath.revelationSpells.map((s) => (
                                        <li key={s.level}>L{s.level}: {s.spell}</li>
                                      ))}
                                    </ul>
                                  </div>
                                  <div className="mt-2 text-[11px] text-red-300/80">
                                    <span className="text-red-400">Oathbreaker → {oath.oathbreaker.name}:</span>{" "}
                                    {oath.oathbreaker.blasphemousWord}
                                  </div>
                                </div>
                              );
                            })()}
                            <div className="mt-2 pt-2 border-t border-amber-800/40">
                              <div className="text-amber-400 text-[11px] font-medium mb-1">Aura scaling (all oaths)</div>
                              <ul className="text-[11px] text-amber-100/60 space-y-0.5">
                                {PALADIN_AURA_SCALING.map((a) => (
                                  <li key={a.level}>L{a.level}: {a.radius} — {a.note}</li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        )}
                        {selectedClass === "Druid" && (
                          <div className="border border-green-700/40 rounded p-3 bg-green-950/20 space-y-3">
                            <div className="text-green-300 font-medium text-xs">
                              Druid Circle & Shapeshifting (L2)
                              {currentLevel >= 2 && !selectedDruidCircle && (
                                <span className="text-red-400 ml-1">— required</span>
                              )}
                            </div>
                            <select
                              className={`w-full bg-black/40 border rounded px-3 py-2 text-amber-50 text-xs ${
                                currentLevel >= 2 && !selectedDruidCircle
                                  ? "border-red-600/60"
                                  : "border-green-700/40"
                              }`}
                              value={selectedDruidCircle}
                              onChange={(e) => setSelectedDruidCircle(e.target.value)}
                            >
                              <option value="">Choose a circle…</option>
                              {DRUID_CIRCLES.map((c) => (
                                <option key={c.id} value={c.id}>
                                  {c.label}{hasDraftHeroFormsForCircle(c.id) ? " (draft)" : ""}
                                </option>
                              ))}
                            </select>
                            {selectedDruidCircle && hasDraftHeroFormsForCircle(selectedDruidCircle) && (
                              <Badge variant="outline" className="text-[10px] border-amber-500/50 text-amber-300">
                                Draft — hero forms pending author review
                              </Badge>
                            )}
                            <div className="text-[11px] text-amber-100/60">
                              {SHAPESHIFT_RULES.activation} · {SHAPESHIFT_RULES.duration}
                            </div>
                            <div>
                              <div className="text-amber-400 text-[11px] font-medium mb-1">
                                Base forms (L{currentLevel >= 11 ? "1–10 + arch" : "1–10"})
                              </div>
                              <div className="space-y-2 max-h-40 overflow-y-auto">
                                {formsAvailableAtLevel(currentLevel).map((form: { id: string; name: string; role: string; traits: string[] }) => (
                                  <div key={form.id} className="border border-green-800/30 rounded p-2 text-[11px]">
                                    <div className="text-green-200 font-medium">{form.name} <span className="text-amber-200/50">({form.role})</span></div>
                                    <ul className="list-disc pl-4 text-amber-100/70 mt-1">
                                      {form.traits.map((t: string) => <li key={t}>{t}</li>)}
                                    </ul>
                                  </div>
                                ))}
                              </div>
                            </div>
                            {selectedDruidCircle && currentLevel >= 10 && (() => {
                              const hero = getHeroFormsForCircle(selectedDruidCircle);
                              if (!hero) return null;
                              return (
                                <div>
                                  <div className="text-purple-300 text-[11px] font-medium mb-1 flex flex-wrap items-center gap-1.5">
                                    <span>Hero forms — {hero.circle} (L10+)</span>
                                    {hasDraftHeroFormsForCircle(selectedDruidCircle) && (
                                      <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 border-amber-500/50 text-amber-300">
                                        Draft
                                      </Badge>
                                    )}
                                  </div>
                                  <div className="space-y-2">
                                    {hero.forms.map((form: { id: string; name: string; traits: string[]; draft?: boolean }) => (
                                      <div key={form.id} className="border border-purple-800/30 rounded p-2 text-[11px]">
                                        <div className="text-purple-200 font-medium flex flex-wrap items-center gap-1.5">
                                          <span>{form.name}</span>
                                          {form.draft && (
                                            <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 border-amber-500/50 text-amber-300">
                                              Draft
                                            </Badge>
                                          )}
                                        </div>
                                        <ul className="list-disc pl-4 text-amber-100/70 mt-1">
                                          {form.traits.map((t: string) => <li key={t}>{t}</li>)}
                                        </ul>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              );
                            })()}
                            {currentLevel < 10 && selectedDruidCircle && (
                              <p className="text-[11px] text-amber-200/50">Hero circle forms unlock at level 10.</p>
                            )}
                          </div>
                        )}
                        {selectedClass === "Oracle" && (
                          <div className="border border-violet-700/40 rounded p-3 bg-violet-950/20 space-y-3">
                            <div className="text-[11px] text-amber-100/60 border border-violet-800/30 rounded p-2 bg-black/20">
                              <span className="text-violet-300 font-medium">Revelation Charges:</span>{" "}
                              {ORACLE_REVELATION_CHARGES.initial} at L1, max {ORACLE_REVELATION_CHARGES.maximum}.{" "}
                              {ORACLE_REVELATION_CHARGES.note}
                            </div>
                            <div>
                              <div className="text-violet-300 font-medium text-xs">
                                Oracle Mystery (L1)
                                {!selectedOracleMystery && (
                                  <span className="text-red-400 ml-1">— required</span>
                                )}
                              </div>
                              <select
                                className={`w-full bg-black/40 border rounded px-3 py-2 text-amber-50 text-xs mt-1 ${
                                  !selectedOracleMystery ? "border-red-600/60" : "border-violet-700/40"
                                }`}
                                value={selectedOracleMystery}
                                onChange={(e) => setSelectedOracleMystery(e.target.value)}
                              >
                                <option value="">Choose a mystery…</option>
                                {ORACLE_MYSTERIES.map((m) => (
                                  <option key={m.id} value={m.id}>
                                    {m.name}{m.draft ? " (draft)" : ""}
                                  </option>
                                ))}
                              </select>
                            {!selectedOracleMystery && (
                              <p className="text-[11px] text-amber-200/60 mt-2">
                                No Oracle Mystery recorded. Choose one at L1; until then, this saved hero has no
                                mystery selection.
                              </p>
                            )}
                            </div>
                            <div>
                              <div className="text-violet-300 font-medium text-xs">
                                Oracle&apos;s Curse (L1)
                                {!selectedOracleCurse && (
                                  <span className="text-red-400 ml-1">— required</span>
                                )}
                              </div>
                              <select
                                className={`w-full bg-black/40 border rounded px-3 py-2 text-amber-50 text-xs mt-1 ${
                                  !selectedOracleCurse ? "border-red-600/60" : "border-violet-700/40"
                                }`}
                                value={selectedOracleCurse}
                                onChange={(e) => setSelectedOracleCurse(e.target.value)}
                              >
                                <option value="">Choose a curse…</option>
                                {ORACLE_CURSES.map((c) => (
                                  <option key={c.id} value={c.id}>
                                    {c.name}{c.draft ? " (draft)" : ""}
                                  </option>
                                ))}
                              </select>
                            {!selectedOracleCurse && (
                              <p className="text-[11px] text-amber-200/60 mt-2">
                                No Oracle&apos;s Curse recorded. Choose one at L1; until then, this saved hero has no
                                curse selection.
                              </p>
                            )}
                            </div>
                            {selectedOracleMystery && (() => {
                              const mystery = getMysteryById(selectedOracleMystery);
                              if (!mystery) return null;
                              const show = (minLevel: number) => currentLevel >= minLevel;
                              return (
                                <div className="space-y-2 text-xs text-amber-50/80">
                                  {mystery.draft && (
                                    <Badge variant="outline" className="text-[10px] border-violet-500/50 text-violet-300">
                                      Draft — Aethel lore, pending author review
                                    </Badge>
                                  )}
                                  <p className="text-amber-100/70">{mystery.theme}</p>
                                  {mystery.patron && <div><span className="text-violet-400">Patron:</span> {mystery.patron}</div>}
                                  {mystery.prophecyTrigger && (
                                    <div><span className="text-violet-400">Prophecy trigger:</span> {mystery.prophecyTrigger}</div>
                                  )}
                                  {mystery.combatRole && (
                                    <div><span className="text-violet-400">Combat:</span> {mystery.combatRole}</div>
                                  )}
                                  {mystery.level1 && show(1) && (
                                    <div className="border border-violet-800/30 rounded p-2">
                                      <div className="text-violet-300 font-medium">L1 — {mystery.level1.name}</div>
                                      <p className="mt-1 text-amber-100/70">{mystery.level1.description}</p>
                                    </div>
                                  )}
                                  {currentLevel < 3 && mystery.level1 && (
                                    <p className="text-[11px] text-amber-200/50">Tier I revelations unlock at level 3.</p>
                                  )}
                                  {mystery.tierI && show(3) && (
                                    <div>
                                      <div className="text-violet-400 font-medium mb-1">Tier I (L3) — choose 1</div>
                                      <div className="space-y-1">
                                        {mystery.tierI.map((r) => (
                                          <div key={r.name} className="border border-violet-800/20 rounded p-2">
                                            <div className="text-violet-200 font-medium">
                                              {r.name}
                                              {r.charges != null ? ` (${r.charges} charge${r.charges === 1 ? "" : "s"})` : ""}
                                            </div>
                                            <p className="text-amber-100/70 mt-0.5">{r.description}</p>
                                          </div>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                  {mystery.tierII && show(6) && (
                                    <div>
                                      <div className="text-violet-400 font-medium mb-1">Tier II (L6) — choose 1</div>
                                      <div className="space-y-1">
                                        {mystery.tierII.map((r) => (
                                          <div key={r.name} className="border border-violet-800/20 rounded p-2">
                                            <div className="text-violet-200 font-medium">
                                              {r.name}
                                              {r.charges != null ? ` (${r.charges} charge${r.charges === 1 ? "" : "s"})` : ""}
                                            </div>
                                            <p className="text-amber-100/70 mt-0.5">{r.description}</p>
                                          </div>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                  {mystery.tierIII && show(9) && (
                                    <div className="border border-violet-800/30 rounded p-2">
                                      <div className="text-violet-300 font-medium">
                                        Tier III (L9) — {mystery.tierIII.name}
                                        {mystery.tierIII.charges != null ? ` (${mystery.tierIII.charges} charges)` : ""}
                                      </div>
                                      <p className="mt-1 text-amber-100/70">{mystery.tierIII.description}</p>
                                    </div>
                                  )}
                                  {mystery.mysticInsight && show(12) && (
                                    <div className="border border-violet-800/30 rounded p-2">
                                      <div className="text-violet-300 font-medium">L12 Mystic Insight — {mystery.mysticInsight.name}</div>
                                      <p className="mt-1 text-amber-100/70">{mystery.mysticInsight.description}</p>
                                    </div>
                                  )}
                                  {mystery.revelationMastery && show(15) && (
                                    <div>
                                      <div className="text-violet-400 font-medium mb-1">L15 Revelation Mastery</div>
                                      <ul className="list-disc pl-4 text-amber-100/70">
                                        {mystery.revelationMastery.map((opt) => <li key={opt}>{opt}</li>)}
                                      </ul>
                                    </div>
                                  )}
                                  {mystery.propheticSurge && show(18) && (
                                    <div className="border border-violet-800/30 rounded p-2">
                                      <div className="text-violet-300 font-medium">L18 Prophetic Surge — {mystery.propheticSurge.name}</div>
                                      <p className="mt-1 text-amber-100/70">{mystery.propheticSurge.description}</p>
                                    </div>
                                  )}
                                  {mystery.finalRevelation && show(20) && (
                                    <div className="border border-violet-700/40 rounded p-2 bg-violet-950/30">
                                      <div className="text-violet-200 font-medium">L20 Final Revelation — {mystery.finalRevelation.name}</div>
                                      <p className="mt-1 text-amber-100/70">{mystery.finalRevelation.description}</p>
                                    </div>
                                  )}
                                </div>
                              );
                            })()}
                            {selectedOracleCurse && (() => {
                              const curse = getCurseById(selectedOracleCurse);
                              if (!curse) return null;
                              const show = (minLevel: number) => currentLevel >= minLevel;
                              return (
                                <div className="space-y-2 text-xs text-amber-50/80 border-t border-violet-800/40 pt-2">
                                  <div className="text-violet-300 font-medium">Curse — {curse.name}</div>
                                  {curse.draft && (
                                    <Badge variant="outline" className="text-[10px] border-violet-500/50 text-violet-300">
                                      Draft — Aethel lore, pending author review
                                    </Badge>
                                  )}
                                  <p className="text-amber-100/70">{curse.blurb}</p>
                                  {curse.limitations && show(1) && (
                                    <div>
                                      <div className="text-violet-400 font-medium mb-1">Limitations</div>
                                      <ul className="list-disc pl-4 text-amber-100/70">
                                        {curse.limitations.map((lim) => <li key={lim}>{lim}</li>)}
                                      </ul>
                                    </div>
                                  )}
                                  {ORACLE_CURSE_BOON_LEVELS.map((lvl) => {
                                    const boons = curse.boons.filter((b) => b.level === lvl);
                                    if (!boons.length || !show(lvl)) return null;
                                    return (
                                      <div key={lvl}>
                                        <div className="text-violet-400 font-medium mb-1">Curse Boon (L{lvl})</div>
                                        {boons.map((b) => (
                                          <div key={b.level} className="border border-violet-800/20 rounded p-2">
                                            <p className="text-amber-100/70">{b.description}</p>
                                          </div>
                                        ))}
                                      </div>
                                    );
                                  })}
                                  {currentLevel < 3 && (
                                    <p className="text-[11px] text-amber-200/50">Curse Boon I unlocks at level 3.</p>
                                  )}
                                </div>
                              );
                            })()}
                            <div className="mt-2 pt-2 border-t border-violet-800/40">
                              <div className="text-violet-400 text-[11px] font-medium mb-1">Shared L10+ progression</div>
                              <ul className="text-[11px] text-amber-100/60 space-y-0.5">
                                {ORACLE_HERO_PROGRESSION.milestones.map((m) => (
                                  <li key={m.level} className={currentLevel >= m.level ? "" : "opacity-50"}>
                                    L{m.level}: {m.feature}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        )}
                        <div>
                          <div className="text-amber-200 font-medium mb-2 text-xs">Arch / prestige path</div>
                          <select
                            className="w-full bg-black/40 border border-amber-700/40 rounded px-3 py-2 text-amber-50 mb-2"
                            value={selectedArchClass}
                            onChange={(e) => setSelectedArchClass(e.target.value)}
                          >
                            <option value="">None yet (unlock in play)</option>
                            {prestigeForBaseClass(selectedClass).map((p) => (
                              <option key={p.name} value={p.name}>{p.name}</option>
                            ))}
                          </select>
                          {selectedArchClass && prestigePaths.filter((p) => p.name === selectedArchClass).map((p) => (
                            <div key={p.name} className="border border-amber-700/40 rounded p-3 space-y-1 text-xs bg-black/30">
                              <div className="text-amber-300 font-semibold">{p.name}</div>
                              <p className="text-amber-100/70">{p.summary}</p>
                              <div><span className="text-amber-400">Base class:</span> {p.baseClass}</div>
                              <PrestigeRequirements prestige={p} selectedFeats={selectedFeats} compact />
                              {p.hallmarks.length > 0 && (
                                <div>
                                  <span className="text-amber-400">Hallmarks:</span>
                                  <ul className="list-disc pl-4 mt-1 text-amber-100/75 space-y-0.5">
                                    {p.hallmarks.map((h, index) => (
                                      <li key={h}>
                                        {p.draftHallmarkIndices.includes(index) && (
                                          <Badge variant="outline" className="mr-1 border-amber-500/50 px-1 py-0 text-[9px] text-amber-300">
                                            draft
                                          </Badge>
                                        )}
                                        {h}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {p.capstone && (
                                <div>
                                  <span className="text-amber-400">Capstone:</span>{" "}
                                  {p.draftCapstone && (
                                    <Badge variant="outline" className="mr-1 border-amber-500/50 px-1 py-0 text-[9px] text-amber-300">
                                      draft
                                    </Badge>
                                  )}
                                  {p.capstone}
                                </div>
                              )}
                              {p.combatRole && (
                                <div><span className="text-amber-400">Role:</span> {p.combatRole}</div>
                              )}
                            </div>
                          ))}
                        </div>
                        <div className="border border-purple-700/40 rounded p-3 bg-purple-950/20">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-purple-300 font-medium text-xs">Resonance Points</span>
                            <span className="text-amber-200 font-bold">{resonancePoints}</span>
                          </div>
                          <input
                            type="range"
                            min={0}
                            max={Math.max(12, resonanceMax.maxRp)}
                            value={resonancePoints}
                            onChange={(e) => setResonancePoints(Number(e.target.value))}
                            className="w-full accent-amber-500"
                          />
                          <p className="text-[11px] text-amber-200/50 mt-1">
                            Spend RP to push the Weave at the table. Resonance max for{" "}
                            {secondaryClass
                              ? `${selectedClass} L${currentLevel} + ${secondaryClass} L${secondaryLevel}`
                              : `${selectedClass} L${currentLevel}`}
                            :{" "}
                            <span className="text-amber-200 font-semibold">{resonanceMax.maxRp}</span>
                            {resonanceMax.draft && <span className="text-amber-400/70"> (draft)</span>}
                            {secondaryClass && resonanceMax.multiclass && (
                              <span className="block text-[10px] text-purple-200/60 mt-0.5">
                                Merge: {resonanceMax.multiclass.primaryPool} + {resonanceMax.multiclass.secondaryBonus}
                                {(resonanceMax.multiclass.repModifier ?? 0) !== 0
                                  ? ` + rep ${resonanceMax.multiclass.repModifier! >= 0 ? "+" : ""}${resonanceMax.multiclass.repModifier}`
                                  : ""}
                              </span>
                            )}
                            {" "}
                            <button
                              type="button"
                              onClick={() => setResonancePoints(resonanceMax.maxRp)}
                              className="underline decoration-dotted hover:text-amber-200"
                            >
                              sync to max
                            </button>
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="spells" className="space-y-4 mt-4">
                  <div className="space-y-4">
                    {!selectedClass ? (
                      <p className="text-sm text-amber-200/70 text-center py-2">Choose a class to filter Weave spells.</p>
                    ) : selectedClass === "Oracle" ? (
                      <p className="text-sm text-violet-200/70 text-center py-2">
                        Oracles use <strong className="text-violet-300">Revelation Charges</strong> and Mystery Revelations — not Weave Resonance Points. Configure Mystery and Oracle&apos;s Curse on the <strong className="text-violet-300">Paths</strong> tab (both required at L1).
                      </p>
                    ) : !isSpellcasterClass(selectedClass) ? (
                      <p className="text-sm text-amber-200/50 text-center py-2">{selectedClass} is not a primary weaver — browse all spells below.</p>
                    ) : (
                      <p className="text-xs text-amber-200/60 text-center">
                        Spells for <strong className="text-amber-300">{selectedClass}</strong>
                        {spellClassOnly ? " (class list)" : " (full Weave)"}
                      </p>
                    )}

                    <div className="flex flex-wrap gap-2 justify-center">
                      <Button
                        size="sm"
                        variant={spellClassOnly ? "default" : "outline"}
                        className={spellClassOnly ? "bg-amber-600" : "text-amber-100 border-amber-700/50"}
                        onClick={() => setSpellClassOnly(true)}
                        disabled={!selectedClass || !isSpellcasterClass(selectedClass)}
                      >
                        Class list
                      </Button>
                      <Button
                        size="sm"
                        variant={!spellClassOnly ? "default" : "outline"}
                        className={!spellClassOnly ? "bg-amber-600" : "text-amber-100 border-amber-700/50"}
                        onClick={() => setSpellClassOnly(false)}
                      >
                        Full Weave
                      </Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-amber-400/60 h-4 w-4" />
                        <Input
                          placeholder="Search spells…"
                          value={spellSearchQuery}
                          onChange={(e) => setSpellSearchQuery(e.target.value)}
                          className="pl-10 bg-black/40 border-amber-700/40 text-amber-50 placeholder:text-amber-200/40"
                        />
                      </div>
                      <Select value={selectedSpellSchool} onValueChange={setSelectedSpellSchool}>
                        <SelectTrigger className="bg-black/40 border-amber-700/40 text-amber-50">
                          <SelectValue placeholder="School" />
                        </SelectTrigger>
                        <SelectContent className="bg-slate-900 border-amber-700/40">
                          <SelectItem value="All" className="text-amber-50">All schools</SelectItem>
                          {SPELL_SCHOOLS.map(school => (
                            <SelectItem key={school} value={school} className="text-amber-50">
                              {school}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <Select value={selectedSpellLevel} onValueChange={setSelectedSpellLevel}>
                        <SelectTrigger className="bg-black/40 border-amber-700/40 text-amber-50">
                          <SelectValue placeholder="Level" />
                        </SelectTrigger>
                        <SelectContent className="bg-slate-900 border-amber-700/40">
                          <SelectItem value="All" className="text-amber-50">All levels</SelectItem>
                          <SelectItem value="Cantrips" className="text-amber-50">Cantrips (0)</SelectItem>
                          {SPELL_LEVELS.slice(1).map(level => (
                            <SelectItem key={level} value={level.toString()} className="text-amber-50">
                              Level {level}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-black/30 border border-amber-700/30 p-3 rounded-lg text-center">
                        <BookOpen className="h-5 w-5 text-amber-400 mx-auto mb-1" />
                        <div className="text-sm text-amber-200/60">Known</div>
                        <div className="text-lg font-bold text-amber-100">{knownSpells.length}</div>
                      </div>
                      <div className="bg-black/30 border border-amber-700/30 p-3 rounded-lg text-center">
                        <Zap className="h-5 w-5 text-amber-400 mx-auto mb-1" />
                        <div className="text-sm text-amber-200/60">Prepared</div>
                        <div className="text-lg font-bold text-amber-100">{preparedSpells.length}</div>
                      </div>
                      <div className="bg-black/30 border border-amber-700/30 p-3 rounded-lg text-center">
                        <div className="text-sm text-amber-200/60">Filtered</div>
                        <div className="text-lg font-bold text-amber-100">{getFilteredSpells().length}</div>
                      </div>
                      <div className="bg-black/30 border border-amber-700/30 p-3 rounded-lg text-center">
                        <div className="text-sm text-amber-200/60">Total</div>
                        <div className="text-lg font-bold text-amber-100">{Object.keys(SPELLS).length}</div>
                      </div>
                    </div>

                    <div className="max-h-96 overflow-y-auto space-y-2">
                      {getFilteredSpells().map((spell) => {
                        const spellKey = getSpellKey(spell);
                        const isKnown = knownSpells.includes(spellKey);
                        const isPrepared = preparedSpells.includes(spellKey);
                        const onClassList = selectedClass ? isSpellAvailableToClass(spell, selectedClass) : true;

                        return (
                          <div key={spellKey} className={`bg-black/30 p-4 rounded-lg border ${onClassList ? "border-amber-700/40" : "border-amber-900/30 opacity-70"}`}>
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2 flex-wrap">
                                  <h3 className="font-semibold text-amber-200">{getSpellDisplayName(spell)}</h3>
                                  <span className="text-xs px-2 py-1 bg-amber-800/60 text-amber-100 rounded">
                                    {spell.level === 0 ? "Cantrip" : `Level ${spell.level}`}
                                  </span>
                                  <span className="text-xs px-2 py-1 bg-purple-900/50 text-purple-200 rounded">
                                    {spell.school}
                                  </span>
                                  {selectedClass && isSpellcasterClass(selectedClass) && (
                                    <span className="text-xs px-2 py-1 bg-amber-900/60 text-amber-100 rounded" title="Resonance cost (school affinity + reputation applied)">
                                      {previewSpellCost(spell) === 0 ? "0 RP" : `${previewSpellCost(spell)} RP`}
                                    </span>
                                  )}
                                </div>
                                <div className="text-sm text-amber-100/70 space-y-1">
                                  <div><strong className="text-amber-300">Casting:</strong> {spell.castingTime}</div>
                                  <div><strong className="text-amber-300">Range:</strong> {spell.range}</div>
                                  <div><strong className="text-amber-300">Components:</strong> {spell.components}</div>
                                  <div><strong className="text-amber-300">Duration:</strong> {spell.duration}</div>
                                  <div><strong className="text-amber-300">Classes:</strong> {spell.classes.join(", ")}</div>
                                </div>
                                <p className="text-sm text-amber-200/50 mt-2">{spell.description}</p>
                              </div>
                              <div className="flex flex-col gap-2 ml-4">
                                <Button
                                  size="sm"
                                  variant={isKnown ? "default" : "outline"}
                                  onClick={() => toggleKnownSpell(spellKey)}
                                  className={isKnown ? "bg-amber-700 hover:bg-amber-600" : "border-amber-600 text-amber-400 hover:bg-amber-700 hover:text-amber-50"}
                                >
                                  {isKnown ? "Known" : "Learn"}
                                </Button>
                                {isKnown && (
                                  <Button
                                    size="sm"
                                    variant={isPrepared ? "default" : "outline"}
                                    onClick={() => togglePreparedSpell(spellKey)}
                                    className={isPrepared ? "bg-purple-700 hover:bg-purple-600" : "border-purple-600 text-purple-400 hover:bg-purple-700 hover:text-purple-50"}
                                  >
                                    {isPrepared ? "Prepared" : "Prepare"}
                                  </Button>
                                )}
                              </div>
                            </div>
                          </div>
                        );
                      })}
                      {getFilteredSpells().length === 0 && (
                        <div className="text-center text-amber-200/50 py-8">
                          No spells match your filters.
                        </div>
                      )}
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/70 border-amber-600/30">
            <CardHeader className="pb-2">
              <div className="flex flex-wrap items-center justify-center gap-2">
                <CardTitle className="text-amber-300 text-center text-base">Advancement</CardTitle>
                <Badge variant="outline" className="text-[9px] px-1.5 py-0 border-emerald-500/50 text-emerald-200">
                  Canon thresholds
                </Badge>
              </div>
              <p className="text-[11px] text-amber-200/55 text-center mt-2 leading-snug">
                Confirmed rulebook L1–L20 cumulative XP. Draft CR→XP awards are{" "}
                <span className="text-amber-200/80">Session-only</span> — log there, then apply totals here manually.
              </p>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center gap-2 mb-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    if (currentLevel > 1) {
                      const newLevel = currentLevel - 1;
                      setCurrentLevel(newLevel);
                      setCurrentXP(xpThresholdForLevel(newLevel));
                    }
                  }}
                  disabled={currentLevel <= 1}
                  className="text-amber-100 border-amber-700/50 hover:bg-amber-950/50"
                >
                  −1
                </Button>
                <div className="text-center">
                  <div className="text-amber-200 font-semibold">Level {currentLevel}</div>
                  <Input
                    type="number"
                    value={currentXP}
                    onChange={(e) => setCurrentXP(parseInt(e.target.value) || 0)}
                    className="w-32 text-center mt-1 bg-black/40 border-amber-700/40 text-amber-50"
                    placeholder="XP"
                  />
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    if (currentLevel < 20) {
                      const newLevel = currentLevel + 1;
                      setCurrentLevel(newLevel);
                      setCurrentXP(xpThresholdForLevel(newLevel));
                    }
                  }}
                  disabled={currentLevel >= 20}
                  className="text-amber-100 border-amber-700/50 hover:bg-amber-950/50"
                >
                  +1
                </Button>
              </div>
              {currentLevel < 20 && (
                <p className="text-center text-[11px] text-amber-200/70 mb-3">
                  To reach L{currentLevel + 1}:{" "}
                  <span className="text-amber-100 font-medium">
                    {formatXp(xpToNextLevel(currentLevel, currentXP))} XP remaining
                  </span>
                  {" "}(threshold {formatXp(CANON_XP_THRESHOLDS[currentLevel + 1] ?? 0)})
                </p>
              )}
              <div className="max-h-48 overflow-y-auto">
                <div className="text-xs text-amber-200/60 space-y-1">
                  {CANON_XP_THRESHOLDS.slice(1).map((threshold, index) => {
                    const level = index + 1;
                    const isCurrent = level === currentLevel;
                    return (
                      <div
                        key={level}
                        className={`flex justify-between rounded px-1 ${
                          isCurrent ? "bg-amber-900/40 text-amber-100 font-medium" : ""
                        }`}
                      >
                        <span>
                          Level {level}
                          {isCurrent ? " (current)" : ""}:
                        </span>
                        <span>{formatXp(threshold ?? 0)} XP</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="col-span-12 lg:col-span-4">
          <Card className="bg-slate-900/70 border-amber-600/30 mb-4">
            <CardHeader className="pb-2">
              <CardTitle className="text-amber-300 text-center text-base">Look</CardTitle>
            </CardHeader>
            <CardContent>
              <CharacterAppearance raceName={selectedRace} value={appearance} onChange={setAppearance} />
            </CardContent>
          </Card>
          <Card className="bg-slate-900/70 border-amber-600/30 mb-4">
            <CardHeader className="pb-2">
              <CardTitle className="text-amber-300 text-center">Abilities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <div className="text-amber-200/70 text-sm mb-2">Generation</div>
                <div className="grid grid-cols-3 gap-2">
                  {abilityGenerationMethods.map((method) => (
                    <Button
                      key={method.id}
                      variant={abilityGenerationMethod === method.id ? "default" : "outline"}
                      size="sm"
                      onClick={() => handleGenerationMethodChange(method.id)}
                      className={abilityGenerationMethod === method.id
                        ? "bg-amber-600 text-amber-50"
                        : "text-amber-100/80 border-amber-700/50 hover:bg-amber-950/50"}
                    >
                      {method.name}
                    </Button>
                  ))}
                </div>
              </div>

              {abilityGenerationMethod === "buyin" && (
                <div className="mb-4 p-3 border border-amber-700/40 rounded bg-black/20">
                  <div className="text-amber-200 text-sm mb-2">Points left: {pointBuyRemaining}</div>
                  <div className="grid grid-cols-1 gap-2">
                    {abilities.map((ability, index) => (
                      <div key={ability.name} className="flex items-center justify-between">
                        <span className="text-amber-100 text-sm">{ability.name}:</span>
                        <div className="flex items-center gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handlePointBuyChange(index, ability.score - 1)}
                            disabled={ability.score <= 8}
                            className="w-8 h-8 p-0 text-amber-100 border-amber-700/50 hover:bg-amber-950/50"
                          >
                            −
                          </Button>
                          <span className="text-amber-100 w-8 text-center">{ability.score}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handlePointBuyChange(index, ability.score + 1)}
                            disabled={ability.score >= 15 || pointBuyRemaining <= 0}
                            className="w-8 h-8 p-0 text-amber-100 border-amber-700/50 hover:bg-amber-950/50"
                          >
                            +
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {abilityGenerationMethod === "preset" && (
                <div className="mb-4 p-3 border border-amber-700/40 rounded bg-black/20">
                  <div className="text-amber-200 text-sm mb-2">Standard array</div>
                  <div className="text-xs text-amber-200/50 mb-2">Values: {standardArray.join(", ")}</div>
                  <div className="grid grid-cols-1 gap-2">
                    {abilities.map((ability, index) => (
                      <div key={ability.name} className="flex items-center justify-between">
                        <span className="text-amber-100 text-sm">{ability.name}:</span>
                        <select
                          value={standardArrayAssignments[index] || ""}
                          onChange={(e) => handleStandardArrayChange(index, parseInt(e.target.value))}
                          className="bg-black/40 text-amber-50 border border-amber-700/40 rounded px-2 py-1 text-sm"
                        >
                          <option value="">Select...</option>
                          {standardArray.map((value) => (
                            <option 
                              key={value} 
                              value={value}
                              disabled={standardArrayAssignments.includes(value) && standardArrayAssignments[index] !== value}
                            >
                              {value}
                            </option>
                          ))}
                        </select>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-3 gap-4">
                {abilities.map((ability) => (
                  <div key={ability.name} className="text-center">
                    <div className="text-amber-200/70 text-sm mb-1">{ability.name.slice(0, 3).toUpperCase()}</div>
                    <div className="ability-score text-amber-100 mb-1">{ability.score}</div>
                    <div className="ability-modifier">{ability.modifier >= 0 ? `+${ability.modifier}` : ability.modifier}</div>
                  </div>
                ))}
              </div>

              <div className="mt-6 text-center">
                <div className="text-amber-200/70 font-semibold text-sm">Proficiency</div>
                <div className="text-2xl font-bold text-amber-200">+2</div>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-2 gap-3 mb-4">
            <Card className="bg-slate-900/70 border-amber-600/30">
              <CardContent className="p-4 text-center">
                <div className="text-amber-200/70 font-semibold text-sm">Armor Class</div>
                <div className="text-2xl font-bold text-amber-100">13</div>
              </CardContent>
            </Card>

            <Card className="bg-slate-900/70 border-amber-600/30">
              <CardContent className="p-4 text-center">
                <div className="text-amber-200/70 font-semibold text-sm">Hit Points</div>
                <div className="text-xl text-amber-100">
                  <Input type="number" defaultValue="13" className="w-16 inline mr-1 bg-black/40 border-amber-700/40 text-amber-50" />
                  / 13
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-900/70 border-amber-600/30">
              <CardContent className="p-4 text-center">
                <div className="text-amber-200/70 font-semibold text-sm">Speed</div>
                <div className="text-2xl font-bold text-amber-100">{selectedRaceData?.speed?.replace(/\s*ft\.?/i, "") || "30"} ft.</div>
              </CardContent>
            </Card>

            <Card className="bg-slate-900/70 border-amber-600/30">
              <CardContent className="p-4 text-center">
                <div className="text-amber-200/70 font-semibold text-sm">Passive Perception</div>
                <div className="text-2xl font-bold text-amber-100">10</div>
              </CardContent>
            </Card>
          </div>

          <Card className="bg-slate-900/70 border-amber-600/30 mb-4">
            <CardHeader className="pb-2">
              <CardTitle className="text-amber-300 text-sm">Saving Throws</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-2">
                {abilities.map((ability) => (
                  <div key={ability.name} className="text-center">
                    <div className="text-amber-200/70 text-sm mb-1">{ability.name.slice(0, 3).toUpperCase()}</div>
                    <div className="skill-modifier">{ability.modifier >= 0 ? `+${ability.modifier}` : ability.modifier}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/70 border-amber-600/30 mb-4">
            <CardContent className="p-4 text-center">
              <div className="text-amber-200/70 font-semibold text-sm">Darkvision</div>
              <div className="text-2xl font-bold text-amber-100">0 ft.</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/70 border-amber-600/30">
            <CardHeader className="pb-2">
              <CardTitle className="text-amber-300 text-sm">Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {skills.map((skill) => (
                  <div key={skill.name} className="flex items-center justify-between">
                    <span className="text-amber-100/80 text-sm">{skill.name}</span>
                    <span className="skill-modifier">{skill.modifier}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Card className="bg-slate-900/70 border-amber-600/30 mt-6 max-w-[1600px] mx-auto">
        <CardHeader className="pb-2">
          <CardTitle className="text-amber-300">Notes</CardTitle>
        </CardHeader>
        <CardContent>
          <textarea
            className="w-full h-32 bg-black/40 border border-amber-700/40 rounded p-3 text-amber-50 resize-none placeholder:text-amber-200/40"
            value={characterNotes} onChange={(e) => setCharacterNotes(e.target.value)} placeholder="Session notes, bonds, quirks…"
          />
          <div className="text-right mt-2">
            <span className="text-xs text-amber-200/50">Tip: SAVE, then add this hero from the Session tab.</span>
          </div>
        </CardContent>
      </Card>
      </>
      )}
    </div>
  );
}
