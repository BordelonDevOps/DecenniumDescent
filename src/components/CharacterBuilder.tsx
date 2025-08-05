"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import {
  Dice1,
  Dice2,
  Dice3,
  Dice4,
  Dice5,
  Dice6,
  RotateCcw,
  Shuffle,
  Eye,
  EyeOff,
  Plus,
  Copy,
  Save,
  Download,
  Info,
  Lock,
  Settings
} from "lucide-react";

const races = [
  {
    name: "Amphibian",
    info: "Amphibians are aquatic humanoids with a deep connection to water and wetlands. They are natural swimmers and can breathe both air and water, making them excellent scouts and explorers of aquatic environments.",
    abilityScoreIncrease: "Constitution +2, Wisdom +1",
    size: "Medium",
    speed: "30 feet, Swim 30 feet",
    traits: ["Amphibious", "Natural Swimmer", "Poison Resistance", "Swamp Camouflage"],
    languages: ["Common", "Aquan"],
    subraces: ["River Amphibian", "Poison Amphibian", "Jungle Amphibian"]
  },
  {
    name: "Drow",
    info: "Drow are dark elves who dwell in the subterranean expanse of the Murk. They are skilled in stealth and shadow magic, often misunderstood by surface dwellers who fear their dark heritage.",
    abilityScoreIncrease: "Dexterity +2, Charisma +1",
    size: "Medium",
    speed: "30 feet",
    traits: ["Superior Darkvision", "Sunlight Sensitivity", "Drow Magic", "Drow Weapon Training"],
    languages: ["Common", "Elvish", "Undercommon"],
    subraces: ["Noble Drow", "Shadow Blades", "Cavern Mystics"]
  },
  {
    name: "Drakari",
    info: "Drakari are draconic humanoids with scales and draconic heritage. They possess the pride and power of dragons, with different variants corresponding to different types of draconic ancestry.",
    abilityScoreIncrease: "Strength +2, Charisma +1",
    size: "Medium",
    speed: "30 feet",
    traits: ["Draconic Ancestry", "Breath Weapon", "Damage Resistance", "Draconic Pride"],
    languages: ["Common", "Draconic"],
    subraces: ["Flame Drakari", "Frost Drakari", "Storm Drakari", "Stone Drakari", "Gale Drakari", "Wave Drakari"]
  },
  {
    name: "Dwarf",
    info: "Dwarves are stout, hardy folk with strong connections to mountains and forges. Their craftsmanship is legendary, as is their resilience and determination in the face of adversity.",
    abilityScoreIncrease: "Constitution +2",
    size: "Medium",
    speed: "25 feet",
    traits: ["Darkvision", "Dwarven Resilience", "Dwarven Combat Training", "Stonecunning"],
    languages: ["Common", "Dwarvish"],
    subraces: ["Mountain Dwarf", "Forge Dwarf", "Deep Dwarf"]
  },
  {
    name: "Elf",
    info: "Elves are graceful, long-lived beings with keen senses and natural magical affinity. Their connection to the natural and magical worlds grants them unique perspectives and abilities.",
    abilityScoreIncrease: "Dexterity +2",
    size: "Medium",
    speed: "30 feet",
    traits: ["Darkvision", "Keen Senses", "Fey Ancestry", "Trance"],
    languages: ["Common", "Elvish"],
    subraces: ["High Elf", "Wood Elf", "Twilight Elf"]
  },
  {
    name: "Feykin",
    info: "Feykin are humanoids touched by fey magic, with an otherworldly grace and connection to nature's wilder aspects. They embody the whimsical and unpredictable nature of the fey realm.",
    abilityScoreIncrease: "Dexterity +2, Charisma +1",
    size: "Medium",
    speed: "30 feet",
    traits: ["Fey Ancestry", "Natural Magic", "Fey Step", "Seasonal Affinity"],
    languages: ["Common", "Sylvan"],
    subraces: ["Summer Fey", "Winter Fey", "Twilight Fey"]
  },
  {
    name: "Gnome",
    info: "Gnomes are small folk with an insatiable curiosity about the world. They delight in life, enjoying every moment of invention, exploration, investigation, creation, and play.",
    abilityScoreIncrease: "Intelligence +2",
    size: "Small",
    speed: "25 feet",
    traits: ["Darkvision", "Gnome Cunning", "Natural Illusionist"],
    languages: ["Common", "Gnomish"],
    subraces: ["Tinker Gnome", "Arcanist Gnome", "Prankster Gnome"]
  },
  {
    name: "Goblin",
    info: "Goblins are small, resourceful creatures with a knack for survival and improvisation. Often underestimated, they possess surprising talents and adaptability in harsh environments.",
    abilityScoreIncrease: "Dexterity +2, Constitution +1",
    size: "Small",
    speed: "30 feet",
    traits: ["Darkvision", "Nimble Escape", "Fury of the Small"],
    languages: ["Common", "Goblin"],
    subraces: ["Boom Goblin", "Scrap Goblin", "Shadow Goblin"]
  },
  {
    name: "Human",
    info: "Humans are the most adaptable and ambitious people among the common races. They have widely varying tastes, morals, and customs in the many different lands where they have settled.",
    abilityScoreIncrease: "All ability scores +1 OR One ability score +2 and gain a feat",
    size: "Medium",
    speed: "30 feet",
    traits: ["Extra Language", "Extra Skill", "Versatility"],
    languages: ["Common"],
    subraces: ["Imperial Human", "Nomadic Human", "Scholarly Human"]
  },
  {
    name: "Mycelian",
    info: "Mycelians are fungal humanoids with a collective consciousness and deep connection to decay and renewal. They commune through spores and understand the cycle of life and death.",
    abilityScoreIncrease: "Constitution +2, Wisdom +1",
    size: "Medium",
    speed: "30 feet",
    traits: ["Fungal Body", "Spore Communication", "Decay Resistance", "Regeneration"],
    languages: ["Common", "Mycelian"],
    subraces: ["Spore Mycelian", "Decay Mycelian", "Symbiotic Mycelian"]
  },
  {
    name: "Ogre",
    info: "Ogres are large, powerful humanoids known for their immense strength and size. Despite their fearsome appearance, many ogres are capable of great wisdom and surprising gentleness.",
    abilityScoreIncrease: "Strength +2, Constitution +1",
    size: "Large",
    speed: "30 feet",
    traits: ["Powerful Build", "Natural Armor", "Intimidating Presence"],
    languages: ["Common", "Giant"],
    subraces: ["Mountain Ogre", "War Ogre", "Marsh Ogre"]
  },
  {
    name: "Orc",
    info: "Orcs are fierce warriors with a strong tribal culture. They value strength, honor, and loyalty to their clan above all else, and are known for their prowess in battle.",
    abilityScoreIncrease: "Strength +2, Constitution +1",
    size: "Medium",
    speed: "30 feet",
    traits: ["Darkvision", "Aggressive", "Powerful Build", "Relentless Endurance"],
    languages: ["Common", "Orc"],
    subraces: ["War Orc", "Shaman Orc", "Hunter Orc"]
  },
  {
    name: "Troll",
    info: "Trolls are large, regenerating humanoids with incredible resilience. They possess remarkable healing abilities and are known for their tenacity and survival instincts.",
    abilityScoreIncrease: "Constitution +2, Strength +1",
    size: "Large",
    speed: "30 feet",
    traits: ["Regeneration", "Powerful Build", "Natural Armor", "Keen Smell"],
    languages: ["Common", "Giant"],
    subraces: ["Swamp Troll", "Stone Troll", "Blood Troll"]
  },
  {
    name: "Undead",
    info: "Undead are beings who have transcended death through various means. They retain their consciousness and memories while gaining resistance to many mortal concerns.",
    abilityScoreIncrease: "Constitution +2, Intelligence +1",
    size: "Medium",
    speed: "30 feet",
    traits: ["Undead Nature", "Damage Resistance", "Deathless", "Dark Vision"],
    languages: ["Common"],
    subraces: ["Lichborn", "Revenant", "Wraith"]
  }
];

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
  const applyRacialBonuses = (abilities: typeof defaultAbilities, race: any) => {
    if (!race || !race.abilityScoreIncrease) return abilities;
    
    const bonuses = race.abilityScoreIncrease.split(', ');
    const updatedAbilities = [...abilities];
    
    bonuses.forEach((bonus: string) => {
      const [abilityName, modifier] = bonus.split(' ');
      const abilityIndex = updatedAbilities.findIndex(a => a.name === abilityName);
      if (abilityIndex !== -1) {
        const bonusValue = parseInt(modifier.replace('+', ''));
        updatedAbilities[abilityIndex] = {
          ...updatedAbilities[abilityIndex],
          score: updatedAbilities[abilityIndex].score + bonusValue
        };
      }
    });
    
    return updateAbilityModifiers(updatedAbilities);
  };

  const feats = [
    {
      name: "Berserker",
      description: "You can enter a battle rage.",
      prerequisite: "Constitution 15+",
      effect: "Once per long rest, you can rage for 1 minute, gaining +2 damage on melee attacks and resistance to physical damage.",
      type: "Combat"
    },
    {
      name: "Bladedancer",
      description: "You move with deadly grace in combat.",
      prerequisite: "Dexterity 15+",
      effect: "When you hit with a finesse weapon, you can move 5 feet without provoking opportunity attacks.",
      type: "Combat"
    },
    {
      name: "Bowyer",
      description: "You are skilled at crafting and using bows.",
      prerequisite: "Proficiency with longbow or shortbow",
      effect: "You can craft masterwork bows and arrows. Your ranged attacks with bows deal +1 damage.",
      type: "Combat"
    },
    {
      name: "Arcane Focus",
      description: "You can focus magical energy more effectively.",
      prerequisite: "Spellcasting ability",
      effect: "You can use your spellcasting focus to cast spells without material components worth less than 100 gp.",
      type: "Magic"
    },
    {
      name: "Battle Mage",
      description: "You blend magic and martial combat.",
      prerequisite: "Spellcasting ability, proficiency with martial weapons",
      effect: "You can cast spells with somatic components while holding weapons and shields.",
      type: "Magic"
    },
    {
      name: "Cantrip Mastery",
      description: "Your cantrips become more powerful.",
      prerequisite: "Ability to cast cantrips",
      effect: "Choose one cantrip you know. It deals maximum damage when you roll a natural 20 on the attack roll or the target rolls a natural 1 on their saving throw.",
      type: "Magic"
    },
    {
      name: "Acrobatics Expert",
      description: "You are exceptionally agile and nimble.",
      prerequisite: "Dexterity 13+",
      effect: "You gain proficiency in Acrobatics, or expertise if already proficient. You can move through hostile creatures' spaces.",
      type: "Skill"
    },
    {
      name: "Animal Whisperer",
      description: "You have a natural affinity with animals.",
      prerequisite: "Wisdom 13+",
      effect: "You gain proficiency in Animal Handling, or expertise if already proficient. You can communicate simple concepts with beasts.",
      type: "Skill"
    },
    // General Feats
    {
      name: "Acrobatic",
      description: "You are exceptionally agile.",
      prerequisite: "Dexterity 13+",
      effect: "You gain proficiency in Acrobatics and can use Dexterity instead of Strength for Athletics checks involving jumping.",
      type: "General"
    },
    {
      name: "Animal Companion",
      description: "You have formed a bond with an animal.",
      prerequisite: "Animal Handling proficiency",
      effect: "You gain an animal companion that follows your commands and fights alongside you.",
      type: "General"
    },
    {
      name: "Artisan",
      description: "You are skilled in crafting.",
      prerequisite: "Intelligence 13+",
      effect: "Choose one type of artisan's tools. You gain proficiency and can create masterwork items.",
      type: "General"
    },
    {
      name: "Blind Fight",
      description: "You can fight without relying on sight.",
      prerequisite: "Wisdom 13+",
      effect: "You don't suffer disadvantage on attack rolls due to being blinded, and you can pinpoint the location of creatures within 30 feet.",
      type: "General"
    },
    {
      name: "Burglar",
      description: "You are skilled at breaking and entering.",
      prerequisite: "Dexterity 13+",
      effect: "You gain proficiency with thieves' tools and can pick locks and disable traps more effectively.",
      type: "General"
    },
    {
      name: "Cartographer",
      description: "You excel at navigation and mapmaking.",
      prerequisite: "Intelligence 13+",
      effect: "You can create accurate maps and never get lost. You have advantage on Survival checks for navigation.",
      type: "General"
    },
    {
      name: "Charismatic",
      description: "Your personality is magnetic.",
      prerequisite: "Charisma 13+",
      effect: "You gain proficiency in Persuasion and Deception. If already proficient, you add double your proficiency bonus.",
      type: "General"
    },
    {
      name: "Commanding Presence",
      description: "You naturally command respect.",
      prerequisite: "Charisma 15+",
      effect: "You can use your Charisma modifier instead of Strength for Intimidation checks, and you have advantage on Persuasion checks against creatures of lower level.",
      type: "General"
    },
    {
      name: "Deceiver",
      description: "You are a master of deception.",
      prerequisite: "Charisma 13+",
      effect: "You gain proficiency in Deception and can lie convincingly even under magical compulsion.",
      type: "General"
    },
    {
      name: "Endurance",
      description: "You can push your body beyond normal limits.",
      prerequisite: "Constitution 13+",
      effect: "You can go twice as long without food, water, or sleep, and you have advantage on Constitution saves against exhaustion.",
      type: "General"
    },
    {
      name: "Entertainer",
      description: "You can captivate audiences.",
      prerequisite: "Charisma 13+",
      effect: "You gain proficiency in Performance and can earn money and gather information through performances.",
      type: "General"
    },
    {
      name: "Intimidating",
      description: "Your presence strikes fear into others.",
      prerequisite: "Charisma 13+ or Strength 15+",
      effect: "You gain proficiency in Intimidation and can demoralize enemies in combat, causing them to have disadvantage on their next attack.",
      type: "General"
    },
    {
      name: "Leadership",
      description: "You inspire others to follow you.",
      prerequisite: "Charisma 15+, level 6+",
      effect: "You can recruit followers and hirelings more easily, and they are more loyal to you.",
      type: "General"
    },
    {
      name: "Negotiator",
      description: "You excel at making deals.",
      prerequisite: "Charisma 13+",
      effect: "You can negotiate better prices for goods and services, and you have advantage on Persuasion checks during negotiations.",
      type: "General"
    }
  ];

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
    archClasses: ["Spiritwalker"]
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
    name: "Oracle",
    info: "Divine magic user with prophetic abilities. Oracles receive visions and divine guidance to aid their allies.",
    hitDie: "d8",
    primaryAbility: "Charisma",
    savingThrows: ["Constitution", "Charisma"],
    spellcasting: "Full Caster",
    archClasses: ["Bishop"]
  },
  {
    name: "Paladin",
    info: "Holy warrior with divine magic. Paladins are champions of justice who smite evil and protect the innocent.",
    hitDie: "d10",
    primaryAbility: "Strength or Charisma",
    savingThrows: ["Wisdom", "Charisma"],
    spellcasting: "Half Caster",
    archClasses: ["Dragon Lancer"]
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
    archClasses: ["Battlemaster", "Juggernaut"]
  },
  {
    name: "Wizard",
    info: "Scholarly arcane spellcaster who studies magic through rigorous academic pursuit. Wizards are the ultimate masters of arcane lore.",
    hitDie: "d6",
    primaryAbility: "Intelligence",
    savingThrows: ["Intelligence", "Wisdom"],
    spellcasting: "Full Caster",
    archClasses: ["Arcanist", "Master"]
  }
];

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

export default function CharacterBuilder() {
  const [selectedRace, setSelectedRace] = useState<string>("");
  const [selectedSubrace, setSelectedSubrace] = useState<string>("");
  const [selectedClass, setSelectedClass] = useState<string>("");
  const [selectedBackground, setSelectedBackground] = useState<string>("");
  const [selectedFeats, setSelectedFeats] = useState<string[]>([]);
  const [featFilter, setFeatFilter] = useState<string>("All");
  const [currentLevel, setCurrentLevel] = useState<number>(1);
  const [currentXP, setCurrentXP] = useState<number>(0);
  const [selectedAlignment, setSelectedAlignment] = useState<string>("");
  const [abilityGenerationMethod, setAbilityGenerationMethod] = useState<string>("preset");
  const [abilities, setAbilities] = useState(defaultAbilities);
  const [pointBuyRemaining, setPointBuyRemaining] = useState<number>(pointBuyPoints);
  const [standardArrayAssignments, setStandardArrayAssignments] = useState<number[]>([15, 14, 13, 12, 10, 8]);

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
  }, [selectedRace, abilityGenerationMethod, standardArrayAssignments]);

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Title and Action Buttons */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-4xl font-bold text-white">Character Builder</h1>
        <div className="flex gap-2">
          <Button className="amber-button">
            <Dice1 className="w-4 h-4 mr-2" />
            RANDOM
          </Button>
          <Button className="amber-button">
            <Plus className="w-4 h-4 mr-2" />
            NEW
          </Button>
          <Button className="amber-button">
            <Copy className="w-4 h-4 mr-2" />
            CLONE
          </Button>
          <Button className="amber-button">
            <Save className="w-4 h-4 mr-2" />
            SAVE NEW CHARACTER
          </Button>
          <Button className="amber-button">
            <Download className="w-4 h-4 mr-2" />
            EXPORT
          </Button>
        </div>
      </div>

      {/* Support Banner */}
      <div className="bg-amber-600/20 border border-amber-600 rounded-lg p-4 mb-6 text-center">
        <div className="text-white">Please consider a gift of $1 to support this site.</div>
        <div className="text-sm text-gray-300">Your support of $1 will provide the server with one lunch because no server should go hungry.</div>
        <Button className="mt-2 bg-amber-600 hover:bg-amber-700 text-white">
          Become a Patron today
        </Button>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-12 gap-6">
        {/* Left Panel - Race Selection and Options */}
        <div className="col-span-4">
          <Card className="glass-card">
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle className="text-white">Options</CardTitle>
                <Badge variant="destructive" className="text-xs">AL Illegal</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="race" className="w-full">
                <TabsList className="grid w-full grid-cols-4 bg-muted">
                  <TabsTrigger value="race">Race</TabsTrigger>
                  <TabsTrigger value="class">Class</TabsTrigger>
                  <TabsTrigger value="feats">Feats</TabsTrigger>
                  <TabsTrigger value="background">Background</TabsTrigger>
                </TabsList>

                <TabsContent value="race" className="space-y-4">
                  <div className="text-white">
                    <h3 className="font-semibold mb-2">Race</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      The options here are the ones allowed by the SRD. Don't see a race or subrace here that you want to use?
                    </p>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm">Race</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400">show info</span>
                        <Lock className="w-4 h-4 text-gray-400" />
                        <Settings className="w-4 h-4 text-gray-400" />
                      </div>
                    </div>

                    <select
                      className="w-full bg-input border border-border rounded px-3 py-2 text-white"
                      value={selectedRace}
                      onChange={(e) => {
                        setSelectedRace(e.target.value);
                        setSelectedSubrace(""); // Reset subrace when race changes
                      }}
                    >
                      <option value="">select 1</option>
                      {races.map((race) => (
                        <option key={race.name} value={race.name}>
                          {race.name}
                        </option>
                      ))}
                    </select>

                    <div className="text-xs text-red-400 mt-2">1 remaining</div>

                    <div className="flex gap-2 mb-4">
                      {selectedRace && (
                        <div className="w-full">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm">Subrace</span>
                            <div className="flex items-center gap-2">
                              <span className="text-xs text-gray-400">show info</span>
                              <Lock className="w-4 h-4 text-gray-400" />
                              <Settings className="w-4 h-4 text-gray-400" />
                            </div>
                          </div>
                          <select
                            className="w-full bg-input border border-border rounded px-3 py-2 text-white"
                            value={selectedSubrace}
                            onChange={(e) => setSelectedSubrace(e.target.value)}
                          >
                            <option value="">select 1</option>
                            {races.find(race => race.name === selectedRace)?.subraces?.map((subrace) => (
                              <option key={subrace} value={subrace}>
                                {subrace}
                              </option>
                            ))}
                          </select>
                          <div className="text-xs text-red-400 mt-2">1 remaining</div>
                        </div>
                      )}
                    </div>

                    <div className="mt-4 space-y-3">
                      {races.map((race) => (
                        <div key={race.name} className="border border-gray-600 rounded-lg p-3 bg-gray-800/50">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-white">{race.name}</span>
                            <span className="text-xs text-gray-400">Size: {race.size}</span>
                          </div>
                          <p className="text-xs text-gray-300 mb-2">{race.info}</p>
                          <div className="space-y-1 text-xs">
                            <div><span className="text-blue-400">Ability Scores:</span> <span className="text-gray-300">{race.abilityScoreIncrease}</span></div>
                            <div><span className="text-green-400">Speed:</span> <span className="text-gray-300">{race.speed}</span></div>
                            <div><span className="text-purple-400">Traits:</span> <span className="text-gray-300">{race.traits.join(", ")}</span></div>
                            <div><span className="text-yellow-400">Languages:</span> <span className="text-gray-300">{race.languages.join(", ")}</span></div>
                            {race.subraces && (
                              <div><span className="text-orange-400">Subraces:</span> <span className="text-gray-300">{race.subraces.join(", ")}</span></div>
                            )}
                            {race.variants && (
                              <div><span className="text-orange-400">Variants:</span> <span className="text-gray-300">{race.variants.join(", ")}</span></div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    <Button className="w-full mt-4 bg-green-600 hover:bg-green-700">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Race
                    </Button>
                  </div>
                </TabsContent>

                <TabsContent value="class" className="space-y-4">
                  <div className="text-white">
                    <h3 className="font-semibold mb-2">Class</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      Choose your character's class to determine their abilities and role.
                    </p>
                    
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm">Class</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400">show info</span>
                        <Lock className="w-4 h-4 text-gray-400" />
                        <Settings className="w-4 h-4 text-gray-400" />
                      </div>
                    </div>

                    <select
                      className="w-full bg-input border border-border rounded px-3 py-2 text-white"
                      value={selectedClass}
                      onChange={(e) => setSelectedClass(e.target.value)}
                    >
                      <option value="">select 1</option>
                      {classes.map((cls) => (
                        <option key={cls.name} value={cls.name}>
                          {cls.name}
                        </option>
                      ))}
                    </select>

                    <div className="text-xs text-red-400 mt-2">1 remaining</div>

                    <div className="mt-4 space-y-3">
                      {classes.map((cls) => (
                        <div key={cls.name} className="border border-gray-600 rounded-lg p-3 bg-gray-800/50">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-white">{cls.name}</span>
                            <span className="text-xs text-gray-400">Hit Die: {cls.hitDie}</span>
                          </div>
                          <p className="text-xs text-gray-300 mb-2">{cls.info}</p>
                          <div className="space-y-1 text-xs">
                            <div><span className="text-blue-400">Primary Ability:</span> <span className="text-gray-300">{cls.primaryAbility}</span></div>
                            <div><span className="text-green-400">Saving Throws:</span> <span className="text-gray-300">{cls.savingThrows.join(", ")}</span></div>
                            <div><span className="text-purple-400">Spellcasting:</span> <span className="text-gray-300">{cls.spellcasting}</span></div>
                            {cls.archClasses && cls.archClasses.length > 0 && (
                              <div><span className="text-orange-400">Arch Classes:</span> <span className="text-gray-300">{cls.archClasses.join(", ")}</span></div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    <Button className="w-full mt-4 bg-green-600 hover:bg-green-700">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Class
                    </Button>
                  </div>
                </TabsContent>

                <TabsContent value="feats" className="space-y-4">
                  <div className="text-white">
                    <h3 className="font-semibold mb-2">Feats</h3>
                    <p className="text-sm text-gray-400 mb-4">
                      Choose feats to enhance your character's abilities.
                    </p>
                    
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm">Filter by Type</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400">show info</span>
                        <Lock className="w-4 h-4 text-gray-400" />
                        <Settings className="w-4 h-4 text-gray-400" />
                      </div>
                    </div>

                    <select
                       className="w-full bg-input border border-border rounded px-3 py-2 text-white mb-4"
                       value={featFilter}
                       onChange={(e) => setFeatFilter(e.target.value)}
                     >
                       <option value="All">All Types</option>
                       <option value="Combat">Combat</option>
                       <option value="Magic">Magic</option>
                       <option value="Skill">Skill</option>
                       <option value="General">General</option>
                     </select>

                    <div className="mt-4 space-y-3 max-h-64 overflow-y-auto">
                      {feats
                        .filter(feat => featFilter === "All" || feat.type === featFilter)
                        .map((feat) => (
                        <div key={feat.name} className="border border-gray-600 rounded-lg p-3 bg-gray-800/50">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-white">{feat.name}</span>
                            <Badge variant="outline" className="text-xs">{feat.type}</Badge>
                          </div>
                          <p className="text-xs text-gray-300 mb-2">{feat.description}</p>
                          <div className="space-y-1 text-xs">
                            <div><span className="text-blue-400">Prerequisite:</span> <span className="text-gray-300">{feat.prerequisite}</span></div>
                            <div><span className="text-green-400">Effect:</span> <span className="text-gray-300">{feat.effect}</span></div>
                          </div>
                          <Button 
                            size="sm" 
                            className="mt-2 w-full bg-blue-600 hover:bg-blue-700"
                            onClick={() => {
                              if (!selectedFeats.includes(feat.name)) {
                                setSelectedFeats([...selectedFeats, feat.name]);
                              }
                            }}
                            disabled={selectedFeats.includes(feat.name)}
                          >
                            {selectedFeats.includes(feat.name) ? "Selected" : "Select Feat"}
                          </Button>
                        </div>
                      ))}
                    </div>

                    {selectedFeats.length > 0 && (
                      <div className="mt-4 p-3 bg-green-900/20 border border-green-600 rounded-lg">
                        <h4 className="text-sm font-semibold text-green-400 mb-2">Selected Feats:</h4>
                        <div className="space-y-1">
                          {selectedFeats.map((featName) => (
                            <div key={featName} className="flex items-center justify-between">
                              <span className="text-xs text-white">{featName}</span>
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

                    <Button className="w-full mt-4 bg-green-600 hover:bg-green-700">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Selected Feats
                    </Button>
                  </div>
                </TabsContent>

                <TabsContent value="background" className="space-y-4">
                  {(() => {
                    const backgrounds = [
                      {
                        name: "Aethel City Guard Veteran",
                        description: "You served in the City Guard of Aethel, dealing with everything from back-alley brawls to organized crime.",
                        skillProficiencies: ["Athletics", "Insight"],
                        toolProficiencies: ["Gaming Set", "Vehicles (Land)"],
                        feature: "Watchman's Eye",
                        featureDescription: "You gain advantage on Wisdom (Perception) checks to spot trouble within city limits and on checks to navigate Aethel.",
                        alignmentTendency: "Often Lawful",
                        startingReputation: "Neutral with Aethel authorities, Liked among common folk"
                      },
                      {
                        name: "Rift Scarred Survivor",
                        description: "You were present during a Rift event and survived, but the experience left indelible marks.",
                        skillProficiencies: ["Survival", "Arcana"],
                        toolProficiencies: [],
                        languages: ["One Exotic language (Abyssal, Celestial, Primordial, or Deep Speech)"],
                        feature: "Planar Sense",
                        featureDescription: "You have advantage on saving throws against being frightened or charmed by aberrations, celestials, elementals, fey, or fiends.",
                        alignmentTendency: "Often Chaotic",
                        startingReputation: "Neutral with planar scholars, Disliked by mundane authorities"
                      },
                      {
                        name: "Disgraced Noble Scion",
                        description: "You hail from a noble family but scandal, betrayal, or your own actions led to your disgrace.",
                        skillProficiencies: ["History", "Persuasion"],
                        toolProficiencies: ["Gaming Set"],
                        languages: ["One of your choice"],
                        feature: "Lingering Influence",
                        featureDescription: "Once per week, you can leverage past connections to gain an audience with minor officials or secure temporary lodging.",
                        alignmentTendency: "Varies greatly",
                        startingReputation: "Disliked by established nobility, Neutral with underground groups"
                      },
                      {
                        name: "Branded Exile",
                        description: "You carry something you were never meant to have: a relic, secret, stolen spell, or divine fragment.",
                        skillProficiencies: ["Stealth", "Arcana"],
                        toolProficiencies: ["Thieves' Tools"],
                        languages: ["One obscure or factional language"],
                        feature: "Echo of the Stolen",
                        featureDescription: "Once per long rest, you may replicate a 1st-level spell you've seen cast within the last hour.",
                        alignmentTendency: "Often Chaotic",
                        startingReputation: "Liked by resistance movements, Hated by the faction you stole from"
                      },
                      {
                        name: "Expedition Cartographer",
                        description: "You've made your living mapping the unknown territories of Aethel, accompanying merchants and adventuring parties.",
                        skillProficiencies: ["Survival", "Investigation"],
                        toolProficiencies: ["Cartographer's Tools", "Navigator's Tools"],
                        feature: "Trailblazer",
                        featureDescription: "You have excellent memory for maps and geography. You can identify safe routes, hazards, and prime camping locations.",
                        alignmentTendency: "Often Neutral",
                        startingReputation: "Liked by merchant guilds and explorers' societies, Neutral with indigenous tribes"
                      },
                      {
                        name: "Arcane Academy Dropout",
                        description: "You studied at a prestigious arcane academy but left before graduation due to expulsion, restrictive policies, or disturbing discoveries.",
                        skillProficiencies: ["Arcana", "History"],
                        toolProficiencies: [],
                        languages: ["Two of your choice"],
                        feature: "Theoretical Knowledge",
                        featureDescription: "You have advantage on Intelligence (Arcana) checks to identify magical effects, traditions, or items.",
                        alignmentTendency: "Often Chaotic",
                        startingReputation: "Disliked by formal arcane institutions, Neutral with independent mages"
                      },
                      {
                        name: "Cult Escapee",
                        description: "You were once part of a secretive cult but broke free. You live with memories of what you witnessed and fear of reclamation.",
                        skillProficiencies: ["Religion", "Deception"],
                        toolProficiencies: ["Disguise Kit"],
                        languages: ["One exotic language (Abyssal, Infernal, or Deep Speech)"],
                        feature: "Hidden Knowledge",
                        featureDescription: "You know the signs and practices of various cults and can identify their symbols and rituals.",
                        alignmentTendency: "Often Good (seeking redemption)",
                        startingReputation: "Feared by cult members, Neutral with religious authorities"
                      }
                    ];

                    const [backgroundFilter, setBackgroundFilter] = useState<string>("");

                    const filteredBackgrounds = backgrounds.filter(background => 
                      backgroundFilter === "" || background.name.toLowerCase().includes(backgroundFilter.toLowerCase())
                    );

                    const handleBackgroundSelect = (background: any) => {
                      setSelectedBackground(background.name);
                    };

                    return (
                      <div className="space-y-6">
                        <div className="flex items-center space-x-4">
                          <Input
                            placeholder="Search backgrounds..."
                            value={backgroundFilter}
                            onChange={(e) => setBackgroundFilter(e.target.value)}
                            className="flex-1"
                          />
                        </div>

                        <div className="grid gap-4">
                          {filteredBackgrounds.map((background) => (
                            <Card key={background.name} className={`p-4 cursor-pointer transition-colors ${
                              selectedBackground === background.name ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:bg-gray-50'
                            }`} onClick={() => handleBackgroundSelect(background)}>
                              <div className="space-y-3">
                                <div className="flex items-center justify-between">
                                  <h3 className="text-lg font-semibold">{background.name}</h3>
                                  {selectedBackground === background.name && (
                                    <Badge variant="default">Selected</Badge>
                                  )}
                                </div>
                                
                                <p className="text-sm text-gray-600">{background.description}</p>
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                                  <div>
                                    <span className="font-medium">Skill Proficiencies:</span>
                                    <p className="text-gray-600">{background.skillProficiencies.join(", ")}</p>
                                  </div>
                                  
                                  {background.toolProficiencies.length > 0 && (
                                    <div>
                                      <span className="font-medium">Tool Proficiencies:</span>
                                      <p className="text-gray-600">{background.toolProficiencies.join(", ")}</p>
                                    </div>
                                  )}
                                  
                                  {background.languages && (
                                    <div>
                                      <span className="font-medium">Languages:</span>
                                      <p className="text-gray-600">{background.languages.join(", ")}</p>
                                    </div>
                                  )}
                                  
                                  <div>
                                    <span className="font-medium">Feature:</span>
                                    <p className="text-gray-600">{background.feature}</p>
                                  </div>
                                </div>
                                
                                <div className="text-sm">
                                  <span className="font-medium">Feature Description:</span>
                                  <p className="text-gray-600">{background.featureDescription}</p>
                                </div>
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                                  <div>
                                    <span className="font-medium">Alignment Tendency:</span>
                                    <p className="text-gray-600">{background.alignmentTendency}</p>
                                  </div>
                                  
                                  <div>
                                    <span className="font-medium">Starting Reputation:</span>
                                    <p className="text-gray-600">{background.startingReputation}</p>
                                  </div>
                                </div>
                              </div>
                            </Card>
                          ))}
                        </div>

                        {selectedBackground && (
                          <Card className="p-4 bg-green-50 border-green-200">
                            <h3 className="text-lg font-semibold text-green-800 mb-2">Selected Background</h3>
                            <p className="text-green-700">{selectedBackground}</p>
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

        {/* Middle Panel - Character Info */}
        <div className="col-span-4">
          <Card className="bg-card mb-4">
            <CardHeader>
              <CardTitle className="text-white text-center">
                {selectedClass || "Select a Class"}
                <span className="block text-sm text-gray-400">(1)</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="alignment" className="w-full">
                <TabsList className="grid w-full grid-cols-5 bg-muted text-xs">
                  <TabsTrigger value="alignment">alignment</TabsTrigger>
                  <TabsTrigger value="combat">combat</TabsTrigger>
                  <TabsTrigger value="proficiencies">proficiencies</TabsTrigger>
                  <TabsTrigger value="spells">spells</TabsTrigger>
                  <TabsTrigger value="features">features</TabsTrigger>
                </TabsList>
                
                <TabsContent value="alignment" className="mt-4">
                  <div className="space-y-4">
                    <h3 className="text-white font-semibold text-center">Select Alignment</h3>
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
                              ? "bg-blue-600 text-white" 
                              : "text-white border-white hover:bg-white hover:text-black"
                          }`}
                          onClick={() => setSelectedAlignment(alignment)}
                        >
                          {alignment}
                        </Button>
                      ))}
                    </div>
                    {selectedAlignment && (
                      <div className="text-center text-white text-sm mt-2">
                        Selected: <span className="font-semibold">{selectedAlignment}</span>
                      </div>
                    )}
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-white text-center">Experience Points</CardTitle>
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
                      const xpThresholds = [0, 500, 1500, 3000, 5500, 9000, 13500, 19000, 25500, 33000, 42000, 53000, 66000, 82000, 101000, 124000, 151000, 182000, 217000, 256000];
                      setCurrentXP(xpThresholds[newLevel - 1] || 0);
                    }
                  }}
                  disabled={currentLevel <= 1}
                  className="text-white border-white hover:bg-white hover:text-black"
                >
                  -1
                </Button>
                <div className="text-center">
                  <div className="text-white font-semibold">Level {currentLevel}</div>
                  <Input 
                    type="number" 
                    value={currentXP} 
                    onChange={(e) => setCurrentXP(parseInt(e.target.value) || 0)}
                    className="w-32 text-center mt-1" 
                    placeholder="Current XP" 
                  />
                </div>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => {
                    if (currentLevel < 20) {
                      const newLevel = currentLevel + 1;
                      setCurrentLevel(newLevel);
                      const xpThresholds = [0, 500, 1500, 3000, 5500, 9000, 13500, 19000, 25500, 33000, 42000, 53000, 66000, 82000, 101000, 124000, 151000, 182000, 217000, 256000];
                      setCurrentXP(xpThresholds[newLevel - 1] || 0);
                    }
                  }}
                  disabled={currentLevel >= 20}
                  className="text-white border-white hover:bg-white hover:text-black"
                >
                  +1
                </Button>
              </div>
              <div className="max-h-48 overflow-y-auto">
                <div className="text-xs text-gray-300 space-y-1">
                  <div className="flex justify-between"><span>Level 1:</span><span>0 XP</span></div>
                  <div className="flex justify-between"><span>Level 2:</span><span>500 XP</span></div>
                  <div className="flex justify-between"><span>Level 3:</span><span>1,500 XP</span></div>
                  <div className="flex justify-between"><span>Level 4:</span><span>3,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 5:</span><span>5,500 XP</span></div>
                  <div className="flex justify-between"><span>Level 6:</span><span>9,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 7:</span><span>13,500 XP</span></div>
                  <div className="flex justify-between"><span>Level 8:</span><span>19,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 9:</span><span>25,500 XP</span></div>
                  <div className="flex justify-between"><span>Level 10:</span><span>33,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 11:</span><span>42,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 12:</span><span>53,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 13:</span><span>66,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 14:</span><span>82,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 15:</span><span>101,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 16:</span><span>124,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 17:</span><span>151,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 18:</span><span>182,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 19:</span><span>217,000 XP</span></div>
                  <div className="flex justify-between"><span>Level 20:</span><span>256,000 XP</span></div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Panel - Ability Scores and Skills */}
        <div className="col-span-4">
          {/* Ability Scores */}
          <Card className="bg-card mb-4">
            <CardHeader>
              <CardTitle className="text-white text-center">Ability Scores</CardTitle>
            </CardHeader>
            <CardContent>
              {/* Ability Generation Method Selection */}
              <div className="mb-4">
                <div className="text-white text-sm mb-2">Generation Method:</div>
                <div className="grid grid-cols-3 gap-2">
                  {abilityGenerationMethods.map((method) => (
                    <Button
                      key={method.id}
                      variant={abilityGenerationMethod === method.id ? "default" : "outline"}
                      size="sm"
                      onClick={() => handleGenerationMethodChange(method.id)}
                      className={abilityGenerationMethod === method.id 
                        ? "bg-blue-600 text-white" 
                        : "text-white border-white hover:bg-white hover:text-black"}
                    >
                      {method.name}
                    </Button>
                  ))}
                </div>
              </div>

              {/* Point Buy Interface */}
              {abilityGenerationMethod === 'buyin' && (
                <div className="mb-4 p-3 border border-gray-600 rounded">
                  <div className="text-white text-sm mb-2">Points Remaining: {pointBuyRemaining}</div>
                  <div className="grid grid-cols-1 gap-2">
                    {abilities.map((ability, index) => (
                      <div key={ability.name} className="flex items-center justify-between">
                        <span className="text-white text-sm">{ability.name}:</span>
                        <div className="flex items-center gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handlePointBuyChange(index, -1)}
                            disabled={ability.score <= 8}
                            className="w-8 h-8 p-0 text-white border-white hover:bg-white hover:text-black"
                          >
                            -
                          </Button>
                          <span className="text-white w-8 text-center">{ability.score}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handlePointBuyChange(index, 1)}
                            disabled={ability.score >= 15 || pointBuyRemaining <= 0}
                            className="w-8 h-8 p-0 text-white border-white hover:bg-white hover:text-black"
                          >
                            +
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Standard Array Interface */}
              {abilityGenerationMethod === 'preset' && (
                <div className="mb-4 p-3 border border-gray-600 rounded">
                  <div className="text-white text-sm mb-2">Assign Standard Array Values:</div>
                  <div className="text-xs text-gray-400 mb-2">Available: {standardArray.join(', ')}</div>
                  <div className="grid grid-cols-1 gap-2">
                    {abilities.map((ability, index) => (
                      <div key={ability.name} className="flex items-center justify-between">
                        <span className="text-white text-sm">{ability.name}:</span>
                        <select
                          value={standardArrayAssignments[index] || ''}
                          onChange={(e) => handleStandardArrayChange(index, parseInt(e.target.value))}
                          className="bg-gray-700 text-white border border-gray-600 rounded px-2 py-1 text-sm"
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
                    <div className="text-white text-sm mb-1">{ability.name}</div>
                    <div className="ability-score text-white mb-1">{ability.score}</div>
                    <div className="ability-modifier">{ability.modifier}</div>
                    <div className="text-xs text-gray-400 mt-1">mod</div>
                  </div>
                ))}
              </div>

              <div className="mt-6 text-center">
                <div className="text-white font-semibold">Proficiency Bonus</div>
                <div className="text-2xl font-bold text-white">+2</div>
              </div>
            </CardContent>
          </Card>

          {/* Character Stats */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <Card className="glass-card">
              <CardContent className="p-4 text-center">
                <div className="text-white font-semibold">Armor Class</div>
                <div className="text-2xl font-bold text-white">13</div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardContent className="p-4 text-center">
                <div className="text-white font-semibold">Max Hit Points</div>
                <div className="text-xl text-white">
                  <Input type="number" defaultValue="13" className="w-16 inline mr-1" />
                  / 13
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardContent className="p-4 text-center">
                <div className="text-white font-semibold">Speed</div>
                <div className="text-2xl font-bold text-white">0 ft.</div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardContent className="p-4 text-center">
                <div className="text-white font-semibold">Passive Perception</div>
                <div className="text-2xl font-bold text-white">10</div>
              </CardContent>
            </Card>
          </div>

          {/* Saving Throws */}
          <Card className="bg-card mb-4">
            <CardHeader>
              <CardTitle className="text-white">Saving Throws</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-2">
                {abilities.map((ability) => (
                  <div key={ability.name} className="text-center">
                    <div className="text-white text-sm mb-1">{ability.name}</div>
                    <div className="skill-modifier">{ability.modifier}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Additional Stats */}
          <div className="grid grid-cols-1 gap-4 mb-4">
            <Card className="glass-card">
              <CardContent className="p-4 text-center">
                <div className="text-white font-semibold">Darkvision</div>
                <div className="text-2xl font-bold text-white">0 ft.</div>
              </CardContent>
            </Card>
          </div>

          {/* Skills */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-white">Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {skills.map((skill) => (
                  <div key={skill.name} className="flex items-center justify-between">
                    <span className="text-white text-sm">{skill.name}</span>
                    <span className="skill-modifier">{skill.modifier}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Notes Section */}
      <Card className="bg-card mt-6">
        <CardHeader>
          <CardTitle className="text-white">Notes</CardTitle>
        </CardHeader>
        <CardContent>
          <textarea
            className="w-full h-32 bg-input border border-border rounded p-3 text-white resize-none"
            placeholder="Add your character notes here..."
          />
          <div className="text-right mt-2">
            <span className="text-xs text-gray-400 cursor-pointer">show selections ▼</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
