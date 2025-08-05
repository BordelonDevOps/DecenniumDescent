// Decennium Descent Game Data
// This file contains all the game data including races, classes, spells, monsters, etc.

// Race Data with detailed descriptions and bonuses
const RACES = {
    amphibian: {
        name: "Amphibian",
        description: "Amphibians are aquatic humanoids with a deep connection to water and moisture. They possess unique adaptations that allow them to thrive both on land and in water.",
        image: "https://i.imgur.com/amphibian-race.jpg",
        abilityScoreIncrease: { constitution: 2 },
        statCaps: { strength: 16, dexterity: 20, constitution: 16, intelligence: 16, wisdom: 18, charisma: 14 },
        size: "Medium",
        speed: 30,
        swimSpeed: 30,
        languages: ["Common", "Aquan"],
        traits: [
            "Amphibious: Can breathe air and water",
            "Moisture Dependency: Must immerse in water for 1 hour every 24 hours",
            "Natural Camouflage: Proficiency in Stealth",
            "Water Sense: Detect water sources within 1 mile"
        ],
        subraces: {
            river: {
                name: "River Amphibian",
                description: "Amphibians adapted to freshwater environments with water manipulation abilities.",
                abilityScoreIncrease: { wisdom: 1 },
                spells: ["shape water", "create or destroy water", "water walk"]
            },
            poison: {
                name: "Poison Amphibian",
                description: "Amphibians with toxic secretions and resistance to poisons.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Poison Resistance", "Toxic Skin"]
            },
            jungle: {
                name: "Jungle Amphibian",
                description: "Amphibians adapted to tropical rainforest environments.",
                abilityScoreIncrease: { dexterity: 1 },
                traits: ["Climbing Speed 30 feet", "Camouflage Expertise"]
            }
        }
    },
    drakari: {
        name: "Drakari",
        description: "Draconic humanoids with elemental affinities and natural magical abilities. They possess both the wisdom of dragons and the adaptability of humanoids.",
        image: "https://i.imgur.com/drakari-race.jpg",
        abilityScoreIncrease: { strength: 2 },
        statCaps: { strength: 20, dexterity: 16, constitution: 18, intelligence: 16, wisdom: 16, charisma: 14 },
        size: "Medium",
        speed: 30,
        languages: ["Common", "Draconic"],
        traits: [
            "Draconic Heritage: Resistance to one damage type",
            "Breath Weapon: Elemental breath attack",
            "Natural Armor: 13 + Dex modifier AC when unarmored",
            "Draconic Senses: Advantage on Perception checks"
        ],
        subraces: {
            flame: {
                name: "Flame Drakari",
                description: "Fire-aligned drakari with flame breath and heat resistance. Descended from red dragons.",
                abilityScoreIncrease: { charisma: 1 },
                damageResistance: "fire",
                breathWeapon: "fire"
            },
            frost: {
                name: "Frost Drakari",
                description: "Ice-aligned drakari with frost breath and cold resistance. Descended from white dragons.",
                abilityScoreIncrease: { constitution: 1 },
                damageResistance: "cold",
                breathWeapon: "cold"
            },
            storm: {
                name: "Storm Drakari",
                description: "Lightning-aligned drakari with storm breath and electrical resistance. Descended from blue dragons.",
                abilityScoreIncrease: { intelligence: 1 },
                damageResistance: "lightning",
                breathWeapon: "lightning"
            },
            stone: {
                name: "Stone Drakari",
                description: "Earth-aligned drakari with acid breath and enhanced durability. Descended from black dragons.",
                abilityScoreIncrease: { constitution: 1 },
                damageResistance: "acid",
                breathWeapon: "acid"
            },
            gale: {
                name: "Gale Drakari",
                description: "Wind-aligned drakari with poison breath and aerial grace. Descended from green dragons.",
                abilityScoreIncrease: { dexterity: 1 },
                damageResistance: "poison",
                breathWeapon: "poison"
            },
            wave: {
                name: "Wave Drakari",
                description: "Water-aligned drakari with lightning breath and aquatic abilities. Descended from bronze dragons.",
                abilityScoreIncrease: { wisdom: 1 },
                damageResistance: "lightning",
                breathWeapon: "lightning"
            }
        }
    },
    drow: {
        name: "Drow",
        description: "Subterranean elves with a complex society and innate magical abilities. Their long history in the Murk has shaped their physiology and culture.",
        image: "https://i.imgur.com/drow-race.jpg",
        abilityScoreIncrease: { dexterity: 2 },
        statCaps: { strength: 14, dexterity: 20, constitution: 14, intelligence: 18, wisdom: 16, charisma: 20 },
        size: "Medium",
        speed: 30,
        languages: ["Common", "Elvish", "Undercommon"],
        traits: [
            "Superior Darkvision: See in darkness within 120 feet",
            "Sunlight Sensitivity: Disadvantage on attacks and Perception in sunlight",
            "Drow Magic: Dancing lights cantrip, faerie fire (3rd level), darkness (5th level)",
            "Keen Senses: Proficiency in Perception",
            "Trance: 4 hours of meditation instead of sleep"
        ],
        subraces: {
            noble: {
                name: "Noble Drow",
                description: "Aristocratic drow with stronger magic and command presence.",
                abilityScoreIncrease: { charisma: 1 },
                traits: ["Enhanced Drow Magic", "Command Presence", "Noble Training"]
            },
            shadowblade: {
                name: "Shadow Blade",
                description: "Drow trained in stealth, assassination, and poison.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Shadow Step", "Poison Expert", "Assassin's Training"]
            },
            mystic: {
                name: "Cavern Mystic",
                description: "Drow with spiritual connection to the Murk and earth.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Earth Communion", "Stone Sense", "Murkish Lore"]
            }
        }
    },
    dwarf: {
        name: "Dwarf",
        description: "Stout and resilient, dwarves are renowned for their craftsmanship, martial prowess, and connection to stone and metal.",
        image: "https://i.imgur.com/dwarf-race.jpg",
        abilityScoreIncrease: { constitution: 2 },
        statCaps: { strength: 18, dexterity: 14, constitution: 20, intelligence: 16, wisdom: 18, charisma: 14 },
        size: "Medium",
        speed: 25,
        languages: ["Common", "Dwarvish"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Dwarven Resilience: Advantage against poison, resistance to poison damage",
            "Dwarven Combat Training: Proficiency with battleaxe, handaxe, light hammer, warhammer",
            "Tool Proficiency: Proficiency with artisan's tools",
            "Stonecunning: Double proficiency bonus on History checks related to stonework"
        ],
        subraces: {
            mountain: {
                name: "Mountain Dwarf",
                description: "Strong dwarves adapted to high altitudes and mountain warfare.",
                abilityScoreIncrease: { strength: 2 },
                traits: ["Armor Training", "Mountain Born", "Mountaineer"]
            },
            forge: {
                name: "Forge Dwarf",
                description: "Master craftsmen with enhanced smithing abilities and fire resistance.",
                abilityScoreIncrease: { intelligence: 1 },
                traits: ["Artisan's Expertise", "Fire Resistance", "Master Craftsman"]
            },
            deep: {
                name: "Deep Dwarf",
                description: "Dwarves adapted to the deepest underground realms.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Superior Darkvision", "Murk Knowledge", "Deep Resilience"]
            }
        }
    },
    dwarf: {
        name: "Dwarf",
        description: "Stout and resilient, dwarves are renowned for their craftsmanship, martial prowess, and connection to stone and metal.",
        abilityScoreIncrease: { constitution: 2 },
        size: "Medium",
        speed: 25,
        languages: ["Common", "Dwarvish"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Dwarven Resilience: Advantage against poison, resistance to poison damage",
            "Dwarven Combat Training: Proficiency with battleaxe, handaxe, light hammer, warhammer",
            "Tool Proficiency: Proficiency with artisan's tools",
            "Stonecunning: Double proficiency bonus on History checks related to stonework"
        ],
        subraces: {
            mountain: {
                name: "Mountain Dwarf",
                description: "Strong dwarves adapted to high altitudes and mountain warfare.",
                abilityScoreIncrease: { strength: 2 },
                traits: ["Armor Training", "Mountain Born", "Mountaineer"]
            },
            forge: {
                name: "Forge Dwarf",
                description: "Master craftsmen with enhanced smithing abilities and fire resistance.",
                abilityScoreIncrease: { intelligence: 1 },
                traits: ["Artisan's Expertise", "Fire Resistance", "Master Craftsman"]
            },
            deep: {
                name: "Deep Dwarf",
                description: "Dwarves adapted to the deepest underground realms.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Superior Darkvision", "Murk Knowledge", "Deep Resilience"]
            }
        }
    },
    elf: {
        name: "Elf",
        description: "Graceful and long-lived, elves possess an innate connection to magic and nature. Their keen senses and agile forms make them natural scouts and spellcasters.",
        image: "https://i.imgur.com/elf-race.jpg",
        abilityScoreIncrease: { dexterity: 2 },
        statCaps: { strength: 14, dexterity: 20, constitution: 14, intelligence: 18, wisdom: 18, charisma: 16 },
        size: "Medium",
        speed: 30,
        languages: ["Common", "Elvish"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Keen Senses: Proficiency in Perception",
            "Fey Ancestry: Advantage against charm, immunity to magical sleep",
            "Trance: 4 hours of meditation instead of 8 hours sleep"
        ],
        subraces: {
            high: {
                name: "High Elf",
                description: "Intellectually gifted elves with strong magical traditions.",
                abilityScoreIncrease: { intelligence: 1 },
                cantrip: true,
                weaponProficiency: ["longsword", "shortbow", "longbow"]
            },
            wood: {
                name: "Wood Elf",
                description: "Forest-dwelling elves with exceptional archery skills.",
                abilityScoreIncrease: { wisdom: 1 },
                weaponProficiency: ["longsword", "shortbow", "longbow"],
                traits: ["Mask of the Wild", "Fleet of Foot"]
            },
            twilight: {
                name: "Twilight Elf",
                description: "Elves who dwell in the liminal spaces between day and night, possessing abilities that bridge light and shadow.",
                abilityScoreIncrease: { charisma: 1 },
                traits: ["Twilight Magic", "Enhanced Darkvision", "Dusk Walker"]
            }
        }
    },
    feykin: {
        name: "Feykin",
        description: "Beings touched by fey magic with changeable appearances and whimsical nature. They embody the chaotic beauty and mystery of the feywild.",
        image: "https://i.imgur.com/feykin-race.jpg",
        abilityScoreIncrease: { charisma: 2 },
        statCaps: { strength: 12, dexterity: 20, constitution: 12, intelligence: 18, wisdom: 16, charisma: 20 },
        size: "Medium",
        speed: 30,
        languages: ["Common", "Sylvan"],
        traits: [
            "Fey Ancestry: Advantage against charm effects",
            "Changeable Form: Minor shape-shifting abilities",
            "Fey Magic: Innate spellcasting",
            "Whimsical Nature: Unpredictable magical effects"
        ],
        subraces: {
            seelie: {
                name: "Seelie Feykin",
                description: "Feykin aligned with the bright and benevolent aspects of the fey.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Healing Light", "Nature's Blessing", "Seelie Magic"]
            },
            unseelie: {
                name: "Unseelie Feykin",
                description: "Feykin touched by the darker, more mischievous fey powers.",
                abilityScoreIncrease: { dexterity: 1 },
                traits: ["Shadow Step", "Mischief Magic", "Unseelie Curse"]
            },
            wild: {
                name: "Wild Feykin",
                description: "Feykin embodying the untamed, primal aspects of nature.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Wild Shape", "Beast Speech", "Primal Magic"]
            }
        }
    },
    gnome: {
        name: "Gnome",
        description: "Small but clever, gnomes are natural tinkerers and magic users. Their curiosity and ingenuity make them excellent inventors and scholars.",
        image: "https://i.imgur.com/gnome-race.jpg",
        abilityScoreIncrease: { intelligence: 2 },
        statCaps: { strength: 12, dexterity: 18, constitution: 14, intelligence: 20, wisdom: 16, charisma: 18 },
        size: "Small",
        speed: 25,
        languages: ["Common", "Gnomish"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Gnome Cunning: Advantage on mental saving throws",
            "Tinker: Proficiency with artisan's tools",
            "Small Size: Can move through larger creatures' spaces"
        ],
        subraces: {
            forest: {
                name: "Forest Gnome",
                description: "Nature-loving gnomes with animal communication abilities.",
                abilityScoreIncrease: { dexterity: 1 },
                traits: ["Natural Illusionist", "Speak with Small Beasts", "Forest Camouflage"]
            },
            rock: {
                name: "Rock Gnome",
                description: "Inventive gnomes with exceptional crafting and mechanical skills.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Artificer's Lore", "Tinker", "Clockwork Toy"]
            },
            deep: {
                name: "Deep Gnome",
                description: "Underground gnomes with enhanced stealth and stone magic.",
                abilityScoreIncrease: { dexterity: 1 },
                traits: ["Superior Darkvision", "Stone Camouflage", "Underground Navigation"]
            }
        }
    },
    goblin: {
        name: "Goblin",
        description: "Small, cunning humanoids known for their resourcefulness and survival instincts. Despite their size, they are fierce and determined.",
        image: "https://i.imgur.com/goblin-race.jpg",
        abilityScoreIncrease: { dexterity: 2 },
        statCaps: { strength: 14, dexterity: 20, constitution: 12, intelligence: 16, wisdom: 14, charisma: 18 },
        size: "Small",
        speed: 30,
        languages: ["Common", "Goblin"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Fury of the Small: Extra damage against larger creatures",
            "Nimble Escape: Disengage or Hide as bonus action",
            "Survival Instinct: Proficiency in Survival"
        ],
        subraces: {
            forest: {
                name: "Forest Goblin",
                description: "Goblins adapted to woodland environments with climbing abilities.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Climbing Speed", "Forest Stealth", "Beast Empathy"]
            },
            mountain: {
                name: "Mountain Goblin",
                description: "Hardy goblins from mountainous regions with enhanced endurance.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Mountain Born", "Cold Resistance", "Sure-Footed"]
            },
            urban: {
                name: "Urban Goblin",
                description: "City-dwelling goblins with enhanced social and thievery skills.",
                abilityScoreIncrease: { charisma: 1 },
                traits: ["Street Smart", "Pickpocket", "Urban Camouflage"]
            }
        }
    },
    human: {
        name: "Human",
        description: "Versatile and ambitious, humans are the most adaptable race. Their drive and determination allow them to excel in any profession.",
        image: "https://i.imgur.com/human-race.jpg",
        abilityScoreIncrease: { intelligence: 1 },
        statCaps: { strength: 18, dexterity: 18, constitution: 18, intelligence: 18, wisdom: 18, charisma: 18 },
        size: "Medium",
        speed: 30,
        languages: ["Common"],
        traits: [
            "Versatile: +1 to all ability scores",
            "Extra Skill: Choose one additional skill proficiency",
            "Ambitious: Advantage on one ability check per long rest",
            "Adaptable: Learn one cantrip from any spell list"
        ],
        subraces: {
            nomadic: {
                name: "Nomadic Human",
                description: "Wandering humans with survival skills and wayfinding abilities.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Survival Instinct", "Wayfinder", "Hardy Traveler"]
            },
            scholarly: {
                name: "Scholarly Human",
                description: "Humans from academic traditions with enhanced learning abilities.",
                abilityScoreIncrease: { intelligence: 1 },
                traits: ["Knowledge Seeker", "Quick Learner", "Lore Master"]
            },
            noble: {
                name: "Noble Human",
                description: "Aristocratic humans with leadership and social skills.",
                abilityScoreIncrease: { charisma: 1 },
                traits: ["Noble Bearing", "Command Presence", "Wealthy"]
            }
        }
    },
    mycelian: {
        name: "Mycelian",
        description: "Fungal beings with unique physiologies and perspectives. Their connection to decomposition and renewal gives them unusual abilities related to life and death.",
        image: "https://i.imgur.com/mycelian-race.jpg",
        abilityScoreIncrease: { wisdom: 2 },
        statCaps: { strength: 14, dexterity: 14, constitution: 20, intelligence: 16, wisdom: 20, charisma: 12 },
        size: "Medium",
        speed: 30,
        languages: ["Common", "Undercommon"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Fungal Nature: Resistance to poison, don't need to breathe",
            "Spore Cloud: Blind enemies in 10-foot radius",
            "Mycological Insight: Advantage on Nature checks for fungi and decay"
        ],
        subraces: {
            spore: {
                name: "Spore Mycelian",
                description: "Mycelians with advanced spore production and bioluminescence.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Bioluminescent Spores", "Hallucinogenic Cloud", "Spore Preservation"]
            },
            decay: {
                name: "Decay Mycelian",
                description: "Mycelians specialized in breaking down organic matter.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Decomposition Touch", "Consume Decay", "Decay Sense"]
            },
            symbiotic: {
                name: "Symbiotic Mycelian",
                description: "Mycelians able to form beneficial bonds with other living beings.",
                abilityScoreIncrease: { charisma: 1 },
                traits: ["Healing Spores", "Enhanced Regeneration", "Vitality Transfer"]
            }
        }
    },
    ogre: {
        name: "Ogre",
        description: "Large, powerful humanoids with immense strength and surprising cunning. Despite their fearsome reputation, many ogres are capable of great loyalty and wisdom.",
        image: "https://i.imgur.com/ogre-race.jpg",
        abilityScoreIncrease: { strength: 2, constitution: 1 },
        statCaps: { strength: 26, dexterity: 12, constitution: 20, intelligence: 12, wisdom: 10, charisma: 10 },
        size: "Large",
        speed: 30,
        languages: ["Common", "Giant"],
        traits: [
            "Powerful Build: Count as one size larger for carrying capacity",
            "Natural Armor: 12 + Con modifier AC when unarmored",
            "Intimidating Presence: Proficiency in Intimidation",
            "Thick Skin: Resistance to bludgeoning damage"
        ],
        subraces: {
            hill: {
                name: "Hill Ogre",
                description: "Ogres from rolling hills with enhanced endurance and wisdom.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Hill Wisdom", "Endurance", "Natural Healer"]
            },
            frost: {
                name: "Frost Ogre",
                description: "Cold-adapted ogres with ice magic and cold resistance.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Cold Resistance", "Ice Magic", "Frozen Breath"]
            },
            stone: {
                name: "Stone Ogre",
                description: "Ogres with rocky skin and earth-based abilities.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Stone Skin", "Earth Tremor", "Rock Throw"]
            }
        }
    },
    orc: {
        name: "Orc",
        description: "Fierce warriors with a strong tribal culture and connection to primal forces. Their strength and determination make them formidable allies or enemies.",
        image: "https://i.imgur.com/orc-race.jpg",
        abilityScoreIncrease: { strength: 2 },
        statCaps: { strength: 20, dexterity: 16, constitution: 18, intelligence: 12, wisdom: 14, charisma: 12 },
        size: "Medium",
        speed: 30,
        languages: ["Common", "Orc"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Aggressive: Move up to speed as bonus action toward enemy",
            "Powerful Build: Count as one size larger for carrying",
            "Relentless Endurance: Drop to 1 HP instead of 0 once per long rest"
        ],
        subraces: {
            mountain: {
                name: "Mountain Orc",
                description: "Hardy orcs from mountainous regions with enhanced climbing abilities.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Mountain Born", "Climbing Speed", "Cold Resistance"]
            },
            plains: {
                name: "Plains Orc",
                description: "Swift orcs from grasslands with mounted combat expertise.",
                abilityScoreIncrease: { dexterity: 1 },
                traits: ["Mounted Warrior", "Fleet of Foot", "Beast Bond"]
            },
            blood: {
                name: "Blood Orc",
                description: "Fierce orcs with berserker rage and enhanced combat abilities.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Blood Rage", "Savage Attacks", "Battle Frenzy"]
            }
        }
    },
    troll: {
        name: "Troll",
        description: "Large, regenerating humanoids with incredible resilience and adaptability. Their ability to recover from almost any wound makes them nearly unstoppable.",
        image: "https://i.imgur.com/troll-race.jpg",
        abilityScoreIncrease: { constitution: 2, strength: 1 },
        statCaps: { strength: 22, dexterity: 14, constitution: 20, intelligence: 10, wisdom: 14, charisma: 10 },
        size: "Large",
        speed: 30,
        languages: ["Common", "Giant"],
        traits: [
            "Regeneration: Regain hit points at start of turn",
            "Powerful Build: Count as one size larger for carrying",
            "Natural Weapons: Claws deal 1d6 + Str slashing damage",
            "Thick Hide: Natural armor bonus"
        ],
        subraces: {
            forest: {
                name: "Forest Troll",
                description: "Trolls adapted to woodland environments with plant-like regeneration.",
                abilityScoreIncrease: { wisdom: 1 },
                traits: ["Plant Regeneration", "Bark Skin", "Root Network"]
            },
            ice: {
                name: "Ice Troll",
                description: "Cold-adapted trolls with ice-based abilities and cold immunity.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Cold Immunity", "Ice Regeneration", "Frozen Touch"]
            },
            blood: {
                name: "Blood Troll",
                description: "Trolls with enhanced regeneration powered by blood magic.",
                abilityScoreIncrease: { constitution: 1 },
                traits: ["Enhanced Regeneration", "Blood Magic", "Vitality Transfer"]
            }
        }
    },
    undead: {
        name: "Undead",
        description: "Beings who have transcended death through magic, willpower, or cosmic intervention. They retain their personalities and memories from life.",
        image: "https://i.imgur.com/undead-race.jpg",
        abilityScoreIncrease: { constitution: 2, intelligence: 1 },
        statCaps: { strength: 16, dexterity: 16, constitution: null, intelligence: 18, wisdom: 18, charisma: 16 },
        necroticFortitude: true,
        size: "Medium",
        speed: 30,
        languages: ["Common"],
        traits: [
            "Darkvision: See in dim light within 60 feet",
            "Undead Nature: Don't need to breathe, eat, or sleep",
            "Necrotic Resistance: Resistance to necrotic damage",
            "Deathless Fortitude: Save to drop to 1 HP instead of 0"
        ],
        subraces: {
            lichborn: {
                name: "Lichborn",
                description: "Undead who achieved undeath through arcane study and ritual.",
                abilityScoreIncrease: { intelligence: 1 },
                traits: ["Arcane Knowledge", "Soul Drain", "Arcane Recovery"]
            },
            revenant: {
                name: "Revenant",
                description: "Undead who returned from death to fulfill an unfinished purpose.",
                abilityScoreIncrease: { strength: 1 },
                traits: ["Relentless Nature", "Vengeful Tracker", "Unfinished Business"]
            },
            wraith: {
                name: "Wraith",
                description: "Undead existing between corporeal and incorporeal states.",
                abilityScoreIncrease: { dexterity: 1 },
                traits: ["Incorporeal Movement", "Shadow Stealth", "Chilling Touch"]
            }
        }
    }
};

// Classes data
const CLASSES = {
    bard: {
        name: "Bard",
        description: "Masters of song and story, bards weave magic through music and words. Their versatility and social skills make them valuable in any situation.",
        hitDie: 8,
        primaryAbility: ["Charisma"],
        savingThrows: ["Dexterity", "Charisma"],
        skillChoices: 3,
        skillList: ["Any"],
        armorProficiency: ["Light armor"],
        weaponProficiency: ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
        spellcasting: {
            ability: "Charisma",
            ritual: true,
            known: true
        },
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Rapier or longsword", "Dagger"],
            tools: ["Entertainer's pack", "Musical instrument"]
        },
        features: {
            1: ["Spellcasting", "Bardic Inspiration"],
            2: ["Jack of All Trades", "Song of Rest"],
            3: ["Bard College", "Expertise"],
            4: ["Ability Score Improvement"]
        },
        colleges: {
            lore: "Enhanced knowledge and magical secrets",
            valor: "Combat training and inspiring leadership",
            glamour: "Fey magic and enchanting presence"
        }
    },
    cleric: {
        name: "Cleric",
        description: "Divine spellcasters who serve deities and channel their power. Clerics can heal allies, smite enemies, and provide spiritual guidance to their companions.",
        hitDie: 8,
        primaryAbility: ["Wisdom"],
        savingThrows: ["Wisdom", "Charisma"],
        skillChoices: 2,
        skillList: ["History", "Insight", "Medicine", "Persuasion", "Religion"],
        armorProficiency: ["Light armor", "Medium armor", "Shields"],
        weaponProficiency: ["Simple weapons"],
        spellcasting: {
            ability: "Wisdom",
            ritual: true,
            prepared: true
        },
        startingEquipment: {
            armor: "Scale mail or leather armor",
            weapons: ["Mace or warhammer", "Shield"],
            tools: ["Priest's pack"]
        },
        features: {
            1: ["Spellcasting", "Divine Domain"],
            2: ["Channel Divinity", "Divine Domain feature"],
            3: ["Destroy Undead"],
            4: ["Ability Score Improvement"]
        },
        domains: {
            life: "Enhanced healing and protective abilities",
            light: "Radiant damage and illumination powers",
            war: "Combat prowess and weapon mastery",
            tempest: "Control over storms and lightning"
        }
    },
    crimsonAgent: {
        name: "Crimson Agent",
        description: "Shadowy operatives who blend stealth with blood magic. They mark their targets and strike with deadly precision from the shadows.",
        hitDie: 8,
        primaryAbility: ["Dexterity"],
        savingThrows: ["Dexterity", "Charisma"],
        skillChoices: 4,
        skillList: ["Acrobatics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Sleight of Hand", "Stealth"],
        armorProficiency: ["Light armor"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        spellcasting: {
            ability: "Charisma",
            level: 3,
            known: true
        },
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Rapier", "Two daggers", "Shortbow and quiver"],
            tools: ["Burglar's pack", "Thieves' tools"]
        },
        features: {
            1: ["Blood Mark", "Sneak Attack"],
            2: ["Crimson Arts"],
            3: ["Blood Magic", "Crimson Archetype"],
            4: ["Ability Score Improvement"]
        },
        archetypes: {
            assassin: "Enhanced stealth and deadly strikes",
            infiltrator: "Social manipulation and disguise",
            hunter: "Tracking and pursuit specialization"
        }
    },
    dragoon: {
        name: "Dragoon",
        description: "Elite warriors who combine aerial mobility with devastating spear techniques. They leap great distances to strike enemies from above.",
        hitDie: 10,
        primaryAbility: ["Strength", "Dexterity"],
        savingThrows: ["Strength", "Dexterity"],
        skillChoices: 2,
        skillList: ["Acrobatics", "Athletics", "History", "Intimidation", "Perception", "Survival"],
        armorProficiency: ["Light armor", "Medium armor", "Heavy armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        startingEquipment: {
            armor: "Scale mail",
            weapons: ["Spear or pike", "Javelin (4)"],
            tools: ["Dungeoneer's pack"]
        },
        features: {
            1: ["Jump Attack", "Spear Mastery"],
            2: ["Aerial Maneuvers"],
            3: ["Dragoon Order"],
            4: ["Ability Score Improvement"]
        },
        orders: {
            sky: "Enhanced jumping and aerial combat",
            storm: "Lightning-based attacks and speed",
            earth: "Defensive techniques and area control"
        }
    },
    druid: {
        name: "Druid",
        description: "Nature-focused spellcasters who can shapeshift and command the forces of the natural world. They serve as guardians of the wilderness and its creatures.",
        hitDie: 8,
        primaryAbility: ["Wisdom"],
        savingThrows: ["Intelligence", "Wisdom"],
        skillChoices: 2,
        skillList: ["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"],
        armorProficiency: ["Light armor", "Medium armor", "Shields (non-metal)"],
        weaponProficiency: ["Clubs", "Daggers", "Darts", "Javelins", "Maces", "Quarterstaffs", "Scimitars", "Sickles", "Slings", "Spears"],
        toolProficiency: ["Herbalism kit"],
        spellcasting: {
            ability: "Wisdom",
            ritual: true,
            prepared: true
        },
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Scimitar or simple weapon", "Shield"],
            tools: ["Explorer's pack", "Herbalism kit"]
        },
        features: {
            1: ["Druidcraft", "Spellcasting"],
            2: ["Wild Shape", "Druid Circle"],
            3: ["Circle feature"],
            4: ["Ability Score Improvement"]
        },
        circles: {
            land: "Enhanced spellcasting and terrain-based abilities",
            moon: "Improved wild shape and combat forms",
            stars: "Cosmic magic and stellar guidance",
            fang: "Primal hunters who embrace the savage aspects of nature",
            grove: "Guardians of sacred groves and ancient wisdom",
            tempest: "Masters of storms and elemental fury",
            decay: "Shepherds of death and renewal in nature's cycle",
            tides: "Coastal druids who command the power of the seas"
        }
    },
    mage: {
        name: "Mage",
        description: "Scholars of the arcane arts, mages wield reality-bending magic through study and practice. Their spells can devastate enemies or aid allies in countless ways.",
        hitDie: 6,
        primaryAbility: ["Intelligence"],
        savingThrows: ["Intelligence", "Wisdom"],
        skillChoices: 2,
        skillList: ["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"],
        armorProficiency: ["None"],
        weaponProficiency: ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        spellcasting: {
            ability: "Intelligence",
            ritual: true,
            spellbook: true
        },
        startingEquipment: {
            weapons: ["Quarterstaff or dagger"],
            tools: ["Scholar's pack", "Spellbook"]
        },
        features: {
            1: ["Spellcasting", "Arcane Recovery"],
            2: ["Arcane Tradition"],
            3: ["Cantrip Formulas"],
            4: ["Ability Score Improvement"]
        },
        traditions: {
            evocation: "Specializes in destructive and protective magic",
            divination: "Focuses on information gathering and foresight",
            enchantment: "Masters of charm and mind control",
            necromancy: "Manipulates life, death, and undeath"
        }
    },

    cleric: {
        name: "Cleric",
        description: "Divine spellcasters who serve deities and channel their power. Clerics can heal allies, smite enemies, and provide spiritual guidance to their companions.",
        hitDie: 8,
        primaryAbility: ["Wisdom"],
        savingThrows: ["Wisdom", "Charisma"],
        skillChoices: 2,
        skillList: ["History", "Insight", "Medicine", "Persuasion", "Religion"],
        armorProficiency: ["Light armor", "Medium armor", "Shields"],
        weaponProficiency: ["Simple weapons"],
        spellcasting: {
            ability: "Wisdom",
            ritual: true,
            prepared: true
        },
        startingEquipment: {
            armor: "Scale mail or leather armor",
            weapons: ["Mace or warhammer", "Shield"],
            tools: ["Priest's pack"]
        },
        features: {
            1: ["Spellcasting", "Divine Domain"],
            2: ["Channel Divinity", "Divine Domain feature"],
            3: ["Destroy Undead"],
            4: ["Ability Score Improvement"]
        },
        domains: {
            life: "Enhanced healing and protective abilities",
            light: "Radiant damage and illumination powers",
            war: "Combat prowess and weapon mastery",
            tempest: "Control over storms and lightning"
        }
    },
    ranger: {
        name: "Ranger",
        description: "Guardians of the wilderness, rangers combine martial skill with nature magic. Their tracking abilities and favored enemies make them excellent scouts and hunters.",
        hitDie: 10,
        primaryAbility: ["Dexterity", "Wisdom"],
        savingThrows: ["Strength", "Dexterity"],
        skillChoices: 3,
        skillList: ["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
        armorProficiency: ["Light armor", "Medium armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        spellcasting: {
            ability: "Wisdom",
            level: 2
        },
        startingEquipment: {
            armor: "Scale mail or leather armor",
            weapons: ["Two shortswords or two simple weapons", "Longbow and quiver"],
            tools: ["Dungeoneer's pack"]
        },
        features: {
            1: ["Favored Enemy", "Natural Explorer"],
            2: ["Fighting Style", "Spellcasting"],
            3: ["Ranger Archetype", "Primeval Awareness"],
            4: ["Ability Score Improvement"]
        },
        archetypes: {
            hunter: "Specialized in tracking and eliminating specific prey",
            beastMaster: "Forms a bond with an animal companion",
            gloomStalker: "Excels in dark environments and ambush tactics"
        }
    },
    paladin: {
        name: "Paladin",
        description: "Holy warriors bound by sacred oaths, paladins combine martial prowess with divine magic. Their dedication to justice makes them powerful allies and feared enemies.",
        hitDie: 10,
        primaryAbility: ["Strength", "Charisma"],
        savingThrows: ["Wisdom", "Charisma"],
        skillChoices: 2,
        skillList: ["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"],
        armorProficiency: ["All armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        spellcasting: {
            ability: "Charisma",
            level: 2
        },
        startingEquipment: {
            armor: "Chain mail",
            weapons: ["Martial weapon", "Shield"],
            tools: ["Priest's pack"]
        },
        features: {
            1: ["Divine Sense", "Lay on Hands"],
            2: ["Fighting Style", "Spellcasting", "Divine Smite"],
            3: ["Divine Health", "Sacred Oath"],
            4: ["Ability Score Improvement"]
        },
        oaths: {
            mercy: "Protection, healing, and preservation of life",
            vengeance: "Fury, execution, and relentless pursuit of enemies",
            dominion: "Authority, law, and divine rulership",
            flame: "Purification, zeal, and cleansing fire",
            ancients: "Nature, memory, and primordial power",
            silence: "Humility, anti-pride, and quiet strength",
            chain: "Martyrdom, warding, and protective bonds",
            grief: "Sorrow, funerary power, and memorialization",
            chainsBroken: "Liberty, rebellion, and freedom",
            martyrKing: "Kingship, burden, and noble sacrifice"
        },
        oathbreakers: {
            cruelty: "Corrupted Mercy - spreads suffering and drains life",
            malice: "Corrupted Vengeance - seeks destruction for its own sake",
            tyranny: "Corrupted Dominion - enslaves minds and crushes free will",
            inferno: "Corrupted Flame - burns the pure and blocks healing",
            witheringGrove: "Corrupted Ancients - spreads blight and decay",
            silentHeretic: "Corrupted Silence - silences truth and spreads lies",
            shackledLord: "Corrupted Chain - enslaves the innocent",
            gravetongue: "Corrupted Grief - spreads despair and prevents rest",
            unboundFlame: "Corrupted Chains Broken - burns freedom itself",
            usurpersCrown: "Corrupted Martyr King - steals power from others"
        }
    },
    monk: {
        name: "Monk",
        description: "Martial artists who harness inner energy to perform supernatural feats of combat and mobility. They channel ki to enhance their abilities.",
        hitDie: 8,
        primaryAbility: ["Dexterity"],
        savingThrows: ["Strength", "Dexterity"],
        skillChoices: 2,
        skillList: ["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"],
        armorProficiency: ["None"],
        weaponProficiency: ["Simple weapons", "Shortswords"],
        toolProficiency: ["One type of artisan's tools or musical instrument"],
        startingEquipment: {
            armor: "None (Unarmored Defense)",
            weapons: ["Shortsword or simple weapon", "Dungeoneer's pack"],
            tools: ["10 darts"]
        },
        features: {
            1: ["Unarmored Defense", "Martial Arts"],
            2: ["Ki", "Unarmored Movement"],
            3: ["Monastic Tradition", "Deflect Missiles"],
            4: ["Ability Score Improvement"]
        },
        traditions: {
            openHand: "Enhanced unarmed combat and ki manipulation",
            shadow: "Stealth abilities and shadow magic",
            fourElements: "Elemental ki techniques and spellcasting"
        }
    },
    crimsonAgent: {
        name: "Crimson Agent",
        description: "Shadowy operatives who blend stealth with blood magic. They mark their targets and strike with deadly precision from the shadows.",
        hitDie: 8,
        primaryAbility: ["Dexterity"],
        savingThrows: ["Dexterity", "Charisma"],
        skillChoices: 4,
        skillList: ["Acrobatics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Sleight of Hand", "Stealth"],
        armorProficiency: ["Light armor"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        spellcasting: {
            ability: "Charisma",
            level: 3,
            known: true
        },
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Rapier", "Two daggers", "Shortbow and quiver"],
            tools: ["Burglar's pack", "Thieves' tools"]
        },
        features: {
            1: ["Blood Mark", "Sneak Attack"],
            2: ["Crimson Arts"],
            3: ["Blood Magic", "Crimson Archetype"],
            4: ["Ability Score Improvement"]
        },
        archetypes: {
            assassin: "Enhanced stealth and deadly strikes",
            infiltrator: "Social manipulation and disguise",
            hunter: "Tracking and pursuit specialization"
        }
    },
    dragoon: {
        name: "Dragoon",
        description: "Elite warriors who combine aerial mobility with devastating spear techniques. They leap great distances to strike enemies from above.",
        hitDie: 10,
        primaryAbility: ["Strength", "Dexterity"],
        savingThrows: ["Strength", "Dexterity"],
        skillChoices: 2,
        skillList: ["Acrobatics", "Athletics", "History", "Intimidation", "Perception", "Survival"],
        armorProficiency: ["Light armor", "Medium armor", "Heavy armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        startingEquipment: {
            armor: "Scale mail",
            weapons: ["Spear or pike", "Javelin (4)"],
            tools: ["Dungeoneer's pack"]
        },
        features: {
            1: ["Jump Attack", "Spear Mastery"],
            2: ["Aerial Maneuvers"],
            3: ["Dragoon Order"],
            4: ["Ability Score Improvement"]
        },
        orders: {
            sky: "Enhanced jumping and aerial combat",
            storm: "Lightning-based attacks and speed",
            earth: "Defensive techniques and area control"
        }
    },
    mirrorsage: {
        name: "Mirrorsage",
        description: "Adaptive spellcasters who learn magic by observing and mimicking other creatures. They build their spell repertoire through encounters.",
        hitDie: 6,
        primaryAbility: ["Intelligence"],
        savingThrows: ["Intelligence", "Wisdom"],
        skillChoices: 3,
        skillList: ["Arcana", "History", "Insight", "Investigation", "Nature", "Perception"],
        armorProficiency: ["None"],
        weaponProficiency: ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        spellcasting: {
            ability: "Intelligence",
            adaptive: true,
            mimicry: true
        },
        startingEquipment: {
            weapons: ["Quarterstaff", "Dagger"],
            tools: ["Scholar's pack", "Crystal focus"]
        },
        features: {
            1: ["Spell Mimicry", "Arcane Echo"],
            2: ["Adaptive Casting"],
            3: ["Mirror Tradition"],
            4: ["Ability Score Improvement"]
        },
        traditions: {
            reflection: "Perfect mimicry and spell copying",
            refraction: "Spell modification and enhancement",
            absorption: "Spell stealing and energy manipulation"
        }
    },
    oracle: {
        name: "Oracle",
        description: "Divine spellcasters who receive visions and prophecies from the gods. Their magic is spontaneous and tied to their mysterious curse.",
        hitDie: 8,
        primaryAbility: ["Charisma"],
        savingThrows: ["Constitution", "Charisma"],
        skillChoices: 4,
        skillList: ["History", "Insight", "Medicine", "Persuasion", "Religion", "Spellcraft"],
        armorProficiency: ["Light armor", "Medium armor", "Shields"],
        weaponProficiency: ["Simple weapons"],
        spellcasting: {
            ability: "Charisma",
            known: true,
            spontaneous: true
        },
        startingEquipment: {
            armor: "Scale mail or leather armor",
            weapons: ["Simple weapon", "Shield"],
            tools: ["Priest's pack"]
        },
        features: {
            1: ["Spellcasting", "Oracle's Curse", "Mystery"],
            2: ["Oracle's Burden"],
            3: ["Mystery feature"],
            4: ["Ability Score Improvement"]
        },
        mysteries: {
            battle: "Combat prowess and tactical abilities",
            heavens: "Cosmic knowledge and stellar magic",
            life: "Healing and protective powers",
            nature: "Connection to the natural world"
        }
    },
    shaman: {
        name: "Shaman",
        description: "Spiritual guides who commune with spirits and channel elemental forces. They serve as bridges between the material and spirit worlds.",
        hitDie: 8,
        primaryAbility: ["Wisdom"],
        savingThrows: ["Constitution", "Wisdom"],
        skillChoices: 4,
        skillList: ["Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"],
        armorProficiency: ["Light armor", "Medium armor", "Shields"],
        weaponProficiency: ["Simple weapons"],
        spellcasting: {
            ability: "Wisdom",
            ritual: true,
            known: true
        },
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Simple weapon", "Shield"],
            tools: ["Explorer's pack", "Herbalism kit"]
        },
        features: {
            1: ["Spellcasting", "Spirit Guide"],
            2: ["Shamanic Trance"],
            3: ["Spirit Bond"],
            4: ["Ability Score Improvement"]
        },
        spirits: {
            ancestor: "Wisdom and guidance from the past",
            nature: "Connection to natural spirits",
            elemental: "Control over elemental forces",
            beast: "Bond with animal spirits"
        }
    },
    soldier: {
        name: "Soldier",
        description: "Disciplined warriors trained in formation fighting and military tactics. They excel in coordinated combat and battlefield leadership.",
        hitDie: 10,
        primaryAbility: ["Strength", "Constitution"],
        savingThrows: ["Strength", "Constitution"],
        skillChoices: 2,
        skillList: ["Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"],
        armorProficiency: ["All armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        toolProficiency: ["One type of gaming set", "Vehicles (land)"],
        startingEquipment: {
            armor: "Chain mail",
            weapons: ["Martial weapon", "Shield"],
            tools: ["Dungeoneer's pack"]
        },
        features: {
            1: ["Fighting Style", "Military Training"],
            2: ["Formation Fighting"],
            3: ["Military Archetype"],
            4: ["Ability Score Improvement"]
        },
        archetypes: {
            officer: "Leadership and tactical coordination",
            veteran: "Combat experience and battlefield awareness",
            specialist: "Expertise in specific military roles"
        }
    },
    thief: {
        name: "Thief",
        description: "Masters of stealth and larceny who excel at infiltration and acquiring what others would keep hidden. They are skilled in avoiding detection and bypassing security.",
        hitDie: 8,
        primaryAbility: ["Dexterity"],
        savingThrows: ["Dexterity", "Intelligence"],
        skillChoices: 4,
        skillList: ["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"],
        armorProficiency: ["Light armor"],
        weaponProficiency: ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
        toolProficiency: ["Thieves' tools"],
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Rapier or shortsword", "Shortbow and quiver"],
            tools: ["Burglar's pack", "Thieves' tools"]
        },
        features: {
            1: ["Expertise", "Sneak Attack", "Thieves' Cant"],
            2: ["Cunning Action"],
            3: ["Roguish Archetype"],
            4: ["Ability Score Improvement"]
        },
        archetypes: {
            burglar: "Enhanced climbing, jumping, and lock picking",
            assassin: "Deadly surprise attacks and poison use",
            spy: "Infiltration and information gathering"
        }
    },
    tinker: {
        name: "Tinker",
        description: "Ingenious inventors who create mechanical devices and gadgets. They combine technical knowledge with magical theory to craft unique solutions.",
        hitDie: 8,
        primaryAbility: ["Intelligence"],
        savingThrows: ["Constitution", "Intelligence"],
        skillChoices: 4,
        skillList: ["Arcana", "History", "Investigation", "Medicine", "Nature", "Perception"],
        armorProficiency: ["Light armor", "Medium armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Light crossbows", "Heavy crossbows"],
        toolProficiency: ["Tinker's tools", "One type of artisan's tools"],
        startingEquipment: {
            armor: "Leather armor",
            weapons: ["Light crossbow and bolts", "Simple weapon"],
            tools: ["Dungeoneer's pack", "Tinker's tools"]
        },
        features: {
            1: ["Magical Tinkering", "Infuse Item"],
            2: ["Tool Expertise"],
            3: ["Artificer Specialist"],
            4: ["Ability Score Improvement"]
        },
        specializations: {
            alchemist: "Potions and chemical reactions",
            artillerist: "Magical cannons and explosive devices",
            armorer: "Magical armor and defensive systems"
        }
    },
    warrior: {
        name: "Warrior",
        description: "Versatile combatants who adapt to any fighting style. They are skilled with weapons and armor, making them formidable opponents in any battle.",
        hitDie: 10,
        primaryAbility: ["Strength", "Dexterity"],
        savingThrows: ["Strength", "Constitution"],
        skillChoices: 2,
        skillList: ["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"],
        armorProficiency: ["All armor", "Shields"],
        weaponProficiency: ["Simple weapons", "Martial weapons"],
        startingEquipment: {
            armor: "Chain mail",
            weapons: ["Martial weapon", "Shield or second weapon"],
            tools: ["Dungeoneer's pack"]
        },
        features: {
            1: ["Fighting Style", "Second Wind"],
            2: ["Action Surge"],
            3: ["Martial Archetype"],
            4: ["Ability Score Improvement"]
        },
        archetypes: {
            champion: "Enhanced critical strikes and athletic prowess",
            battlemaster: "Tactical maneuvers and combat superiority",
            weaponmaster: "Specialization in specific weapon types"
        }
    },
    wizard: {
        name: "Wizard",
        description: "Scholarly spellcasters who master magic through study and preparation. They have access to the broadest selection of spells through their spellbooks.",
        hitDie: 6,
        primaryAbility: ["Intelligence"],
        savingThrows: ["Intelligence", "Wisdom"],
        skillChoices: 2,
        skillList: ["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"],
        armorProficiency: ["None"],
        weaponProficiency: ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
        spellcasting: {
            ability: "Intelligence",
            ritual: true,
            spellbook: true,
            prepared: true
        },
        startingEquipment: {
            weapons: ["Quarterstaff or dagger"],
            tools: ["Scholar's pack", "Spellbook"]
        },
        features: {
            1: ["Spellcasting", "Arcane Recovery"],
            2: ["Arcane Tradition"],
            3: ["Cantrip Formulas"],
            4: ["Ability Score Improvement"]
        },
        traditions: {
            abjuration: "Protective and banishing magic",
            conjuration: "Summoning and teleportation spells",
            divination: "Information gathering and foresight",
            enchantment: "Charm and mind control magic",
            evocation: "Destructive and energy-based spells",
            illusion: "Deception and misdirection magic",
            necromancy: "Death and undeath manipulation",
            transmutation: "Transformation and alteration spells"
        }
    }

};

// Background Data
const BACKGROUNDS = {
    "aethel-city-guard-veteran": {
        name: "Aethel City Guard Veteran",
        description: "You served in the City Guard of Aethel, dealing with everything from back-alley brawls to organized crime. You understand the chain of command, the city's layout, and the pulse of its streets.",
        skillProficiencies: ["Athletics", "Insight"],
        toolProficiencies: ["Gaming set", "Vehicles (land)"],
        equipment: ["Piece of old uniform", "Map of Aethel's districts", "Common clothes", "Manacles", "Belt pouch with 10 gp"],
        feature: "Watchman's Eye: Advantage on Wisdom (Perception) checks to spot trouble within city limits and on checks to navigate Aethel."
    },
    "battlefield-medic": {
        name: "Battlefield Medic",
        description: "You are a former combat field doctor trained in emergency healing, having saved countless lives under the most dire circumstances.",
        skillProficiencies: ["Medicine", "Survival"],
        toolProficiencies: ["Herbalism kit", "Healer's kit"],
        equipment: ["Healer's kit", "Bloodstained medical tools", "Field surgeon's apron", "Common clothes", "Belt pouch with 15 gp"],
        feature: "Combat Medic: You can stabilize dying creatures without expending uses of a healer's kit, and your medical treatment grants +1 hp when healing."
    },
    "celestial-emissary": {
        name: "Celestial Emissary",
        description: "You are an inspired messenger or seer of higher divine orders, touched by celestial beings and granted visions of divine purpose.",
        skillProficiencies: ["Religion", "Insight"],
        languages: 1,
        equipment: ["Celestial holy symbol", "Divine vision journal", "Fine robes", "Blessed water", "Belt pouch with 15 gp"],
        feature: "Divine Guidance: Once per day, you can seek guidance from celestial forces, gaining advantage on one Wisdom-based check."
    },
    "disgraced-noble-scion": {
        name: "Disgraced Noble Scion",
        description: "You hail from a noble family but scandal, betrayal, or your own actions led to your disgrace. Now you must navigate the world without the safety net of your birthright.",
        skillProficiencies: ["History", "Persuasion"],
        toolProficiencies: ["Gaming set"],
        languages: 1,
        equipment: ["Fine clothes (slightly worn)", "Signet ring with tarnished family crest", "Letter detailing your disgrace", "Purse with 25 gp"],
        feature: "Lingering Influence: Once per week, leverage past connections to gain audience with minor officials or secure temporary lodging."
    },
    "expedition-cartographer": {
        name: "Expedition Cartographer",
        description: "You are a skilled mapmaker and explorer, tied to organized discovery expeditions. Your maps have guided countless adventurers through uncharted territories.",
        skillProficiencies: ["Survival", "Investigation"],
        toolProficiencies: ["Cartographer's tools", "Navigator's tools"],
        equipment: ["Cartographer's tools", "Detailed regional map", "Compass", "Explorer's pack", "Belt pouch with 20 gp"],
        feature: "Master Navigator: You can create accurate maps of areas you've explored and never become lost in wilderness you've previously mapped."
    },
    "guild-artisan-dropout": {
        name: "Guild Artisan Dropout",
        description: "You were once an apprentice in one of Aethel's powerful artisan guilds, but the rigid structure or internal politics didn't suit you. You left seeking freedom.",
        skillProficiencies: ["Insight", "Persuasion"],
        toolProficiencies: ["Artisan's tools"],
        languages: 1,
        equipment: ["Set of artisan's tools", "Sample of your best work", "Letter of resignation from guild", "Traveler's clothes", "Belt pouch with 15 gp"],
        feature: "Trade Secret: You can identify quality craftsmanship and navigate guild bureaucracy, though your departure means strained relations."
    },
    "marked-fugitive": {
        name: "Marked Fugitive",
        description: "You carry something you were never meant to have: a relic, secret, stolen spell, or divine fragment. You're branded, cursed, or watched by factions that believe your existence is a violation.",
        skillProficiencies: ["Stealth", "Arcana"],
        toolProficiencies: ["Thieves' tools"],
        languages: 1,
        equipment: ["Broken manacle", "False identity papers", "Hidden mark or scar", "Common clothes", "10 gp in mixed coin"],
        feature: "Echo of the Stolen: Once per long rest, replicate a 1st-level spell you've seen cast within the last hour."
    },
    "planar-merchant": {
        name: "Planar Merchant",
        description: "You are a trader in extraplanar goods and knowledge, dealing in both legal and illicit items from other planes of existence.",
        skillProficiencies: ["Persuasion", "Arcana"],
        toolProficiencies: ["Gaming set"],
        languages: 1,
        equipment: ["Planar trade goods sample", "Merchant's scales", "Fine clothes", "Signet ring", "Belt pouch with 25 gp"],
        feature: "Planar Contacts: You have connections with traders and beings from other planes, allowing access to rare extraplanar goods."
    },
    "rift-scarred-survivor": {
        name: "Rift-Scarred Survivor",
        description: "You were present during a Rift event and survived, but the experience left indelible marks. You may have been pulled into another plane or witnessed horrors beyond comprehension.",
        skillProficiencies: ["Survival", "Arcana"],
        languages: 1,
        equipment: ["Strange trinket from the other side", "Tattered map of unknown place", "Traveler's clothes", "Amulet to ward off bad luck", "5 gp"],
        feature: "Planar Sense: Advantage on saving throws against being frightened or charmed by aberrations, celestials, elementals, fey, or fiends."
    },
    "seeker-of-lost-pantheon": {
        name: "Seeker of the Lost Pantheon",
        description: "You are driven by a quest to uncover the truths behind Aethel's Lost Pantheon - deities worshiped in ages past but now largely forgotten or suppressed.",
        skillProficiencies: ["Religion", "History"],
        toolProficiencies: ["Calligrapher's supplies"],
        languages: 2,
        equipment: ["Rubbing from ancient tablet", "Book of fragmented myths", "Holy symbol of forgotten deity", "Common clothes", "Incense", "10 gp"],
        feature: "Whispers of the Past: Advantage on Intelligence checks to decipher ancient ruins, symbols, or texts related to Aethel's history."
    },
    "wilderness-herbalist": {
        name: "Wilderness Herbalist",
        description: "You lived on the fringes of civilization, learning the secrets of plants, fungi, and natural remedies. Your knowledge of nature's pharmacy is extensive.",
        skillProficiencies: ["Nature", "Medicine"],
        toolProficiencies: ["Herbalism kit"],
        languages: 1,
        equipment: ["Herbalism kit", "Collection of rare seeds", "Leather-bound plant journal", "Traveler's clothes", "Belt pouch with 10 gp"],
        feature: "Natural Remedies: You can identify beneficial and harmful plants, and create basic healing poultices from natural materials."
    }
};

// Spell Data (sample spells)
const SPELLS = {
    // Cantrips
    "acid-splash": {
        name: "Acid Splash",
        level: 0,
        school: "Conjuration",
        castingTime: "1 action",
        range: "60 feet",
        components: "V, S",
        duration: "Instantaneous",
        description: "You hurl a bubble of acid. Choose one or two creatures within range. A creature must succeed on a Dexterity saving throw or take 1d6 acid damage.",
        classes: ["mage", "warlock"]
    },
    "fire-bolt": {
        name: "Fire Bolt",
        level: 0,
        school: "Evocation",
        castingTime: "1 action",
        range: "120 feet",
        components: "V, S",
        duration: "Instantaneous",
        description: "You hurl a mote of fire at a creature or object within range. Make a ranged spell attack. On a hit, the target takes 1d10 fire damage.",
        classes: ["mage"]
    },
    "mage-hand": {
        name: "Mage Hand",
        level: 0,
        school: "Transmutation",
        castingTime: "1 action",
        range: "30 feet",
        components: "V, S",
        duration: "1 minute",
        description: "A spectral, floating hand appears at a point you choose within range. The hand can manipulate objects, open doors, or retrieve items.",
        classes: ["mage", "bard", "warlock"]
    },
    // 1st Level Spells
    "magic-missile": {
        name: "Magic Missile",
        level: 1,
        school: "Evocation",
        castingTime: "1 action",
        range: "120 feet",
        components: "V, S",
        duration: "Instantaneous",
        description: "You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage.",
        classes: ["mage"]
    },
    "cure-wounds": {
        name: "Cure Wounds",
        level: 1,
        school: "Evocation",
        castingTime: "1 action",
        range: "Touch",
        components: "V, S",
        duration: "Instantaneous",
        description: "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier.",
        classes: ["cleric", "bard", "paladin", "ranger"]
    },
    "shield": {
        name: "Shield",
        level: 1,
        school: "Abjuration",
        castingTime: "1 reaction",
        range: "Self",
        components: "V, S",
        duration: "1 round",
        description: "An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC.",
        classes: ["mage"]
    }
};

// Equipment Data
const EQUIPMENT = {
    weapons: {
        dagger: { name: "Dagger", damage: "1d4", damageType: "piercing", properties: ["finesse", "light", "thrown"], cost: "2 gp", weight: "1 lb" },
        shortsword: { name: "Shortsword", damage: "1d6", damageType: "piercing", properties: ["finesse", "light"], cost: "10 gp", weight: "2 lb" },
        longsword: { name: "Longsword", damage: "1d8", damageType: "slashing", properties: ["versatile (1d10)"], cost: "15 gp", weight: "3 lb" },
        greataxe: { name: "Greataxe", damage: "1d12", damageType: "slashing", properties: ["heavy", "two-handed"], cost: "30 gp", weight: "7 lb" },
        longbow: { name: "Longbow", damage: "1d8", damageType: "piercing", properties: ["ammunition", "heavy", "range (150/600)", "two-handed"], cost: "50 gp", weight: "2 lb" }
    },
    armor: {
        leather: { name: "Leather Armor", ac: "11 + Dex modifier", type: "light", cost: "10 gp", weight: "10 lb" },
        chainmail: { name: "Chain Mail", ac: "16", type: "heavy", cost: "75 gp", weight: "55 lb", strength: 13 },
        plate: { name: "Plate Armor", ac: "18", type: "heavy", cost: "1,500 gp", weight: "65 lb", strength: 15 }
    }
};

// Utility Functions
function rollDice(sides, count = 1, modifier = 0) {
    let total = modifier;
    let rolls = [];
    
    for (let i = 0; i < count; i++) {
        const roll = Math.floor(Math.random() * sides) + 1;
        rolls.push(roll);
        total += roll;
    }
    
    return { total, rolls, modifier };
}

function rollAbilityScore() {
    // Roll 4d6, drop lowest
    const rolls = [];
    for (let i = 0; i < 4; i++) {
        rolls.push(Math.floor(Math.random() * 6) + 1);
    }
    rolls.sort((a, b) => b - a);
    return rolls.slice(0, 3).reduce((sum, roll) => sum + roll, 0);
}

function getAbilityModifier(score) {
    return Math.floor((score - 10) / 2);
}

function formatModifier(modifier) {
    return modifier >= 0 ? `+${modifier}` : `${modifier}`;
}

// Feat System
const FEATS = {
    // General Feats
    abilityScoreImprovement: {
        name: "Ability Score Improvement",
        description: "Increase one ability score by 2, or increase two ability scores by 1 each. You can't increase an ability score above 20 using this feat.",
        prerequisite: "None",
        effect: "Choose +2 to one ability score or +1 to two ability scores",
        type: "general"
    },
    alert: {
        name: "Alert",
        description: "Always on the lookout for danger, you gain the following benefits:",
        prerequisite: "None",
        effect: "+5 bonus to initiative, can't be surprised while conscious, creatures don't gain advantage on attack rolls from being hidden",
        type: "general"
    },
    athlete: {
        name: "Athlete",
        description: "You have undergone extensive physical training to gain the following benefits:",
        prerequisite: "None",
        effect: "Increase Strength or Dexterity by 1, climbing doesn't cost extra movement, running long jump distance increases by feet equal to Strength modifier",
        type: "general"
    },
    durable: {
        name: "Durable",
        description: "Hardy and resilient, you gain the following benefits:",
        prerequisite: "None",
        effect: "Increase Constitution by 1, when you roll a Hit Die to regain hit points, minimum amount regained equals twice your Constitution modifier",
        type: "general"
    },
    lucky: {
        name: "Lucky",
        description: "You have inexplicable luck that seems to kick in at just the right moment.",
        prerequisite: "None",
        effect: "You have 3 luck points. Whenever you make an attack roll, ability check, or saving throw, you can spend one luck point to roll an additional d20",
        type: "general"
    },
    magicInitiate: {
        name: "Magic Initiate",
        description: "Choose a class: bard, cleric, druid, sorcerer, warlock, or wizard. You learn magic from that class.",
        prerequisite: "None",
        effect: "Learn two cantrips and one 1st-level spell from chosen class. You can cast the spell once per long rest",
        type: "general"
    },
    martialAdept: {
        name: "Martial Adept",
        description: "You have martial training that allows you to perform special combat maneuvers.",
        prerequisite: "None",
        effect: "Learn two maneuvers from the Battle Master archetype, gain one superiority die (d6)",
        type: "general"
    },
    observant: {
        name: "Observant",
        description: "Quick to notice details of your environment, you gain the following benefits:",
        prerequisite: "None",
        effect: "Increase Intelligence or Wisdom by 1, +5 bonus to passive Perception and passive Investigation",
        type: "general"
    },
    resilient: {
        name: "Resilient",
        description: "Choose one ability score. You gain the following benefits:",
        prerequisite: "None",
        effect: "Increase the chosen ability score by 1, gain proficiency in saving throws using the chosen ability",
        type: "general"
    },
    skilled: {
        name: "Skilled",
        description: "You gain proficiency in any combination of three skills or tools of your choice.",
        prerequisite: "None",
        effect: "Gain proficiency in three skills or tools",
        type: "general"
    },
    powerAttack: {
        name: "Power Attack",
        description: "You can sacrifice accuracy for devastating damage.",
        prerequisite: "Strength 13+",
        effect: "Take -2 to attack rolls for +4 damage on melee attacks",
        type: "general"
    },
    combatCasting: {
        name: "Combat Casting",
        description: "You have learned to cast spells in the heat of battle.",
        prerequisite: "Spellcasting ability",
        effect: "Advantage on Constitution saving throws to maintain concentration, can cast spells as opportunity attacks",
        type: "general"
    },
    weaponFocus: {
        name: "Weapon Focus",
        description: "You have specialized training with a particular weapon type.",
        prerequisite: "Proficiency with chosen weapon",
        effect: "+1 to attack rolls with chosen weapon type",
        type: "general"
    },
    combatReflexes: {
        name: "Combat Reflexes",
        description: "Your quick reflexes allow you to react swiftly in combat.",
        prerequisite: "Dexterity 13+",
        effect: "+1 opportunity attack per round, +2 to initiative rolls",
        type: "general"
    },
    riposte: {
        name: "Riposte",
        description: "You can quickly counterattack after successfully defending.",
        prerequisite: "Dexterity 15+, Melee Proficiency",
        effect: "Free attack after successful dodge or parry",
        type: "general"
    },
    grappler: {
        name: "Grappler",
        description: "You have developed the skills necessary to hold your own in close-quarters grappling.",
        prerequisite: "Strength 14+",
        effect: "+4 to grapple rolls, enemies have -4 to escape grapples",
        type: "general"
    },
    feint: {
        name: "Feint",
        description: "You can mislead opponents with deceptive movements.",
        prerequisite: "Dexterity 14+, Charisma 13+",
        effect: "Enemy loses AC bonus vs your next attack",
        type: "general"
    },
    defensiveStance: {
        name: "Defensive Stance",
        description: "You can adopt a defensive posture that greatly improves your protection.",
        prerequisite: "Level 6",
        effect: "+15% AC bonus, cannot move during the turn this is used",
        type: "general"
    },
    
    // Vital Mutation Feats (from rulebook)
    bioStabilizer: {
        name: "Bio-Stabilizer",
        description: "Your mutations have stabilized, providing enhanced regeneration.",
        prerequisite: "Bloodthick Node mutation",
        effect: "+1 regeneration while under the effect of 2+ mutations",
        type: "vital_mutation"
    },
    juggernautCore: {
        name: "Juggernaut's Core",
        description: "Your ossified core provides protection against precision attacks.",
        prerequisite: "Ossified Core mutation",
        effect: "If you are immune to critical hits, gain resistance to sneak attack damage",
        type: "vital_mutation"
    },
    livingFortress: {
        name: "Living Fortress",
        description: "Multiple vital mutations make you nearly impregnable.",
        prerequisite: "3 Vital Mutations active",
        effect: "Gain immunity to flanking",
        type: "vital_mutation"
    },
    evolutionUnderFire: {
        name: "Evolution Under Fire",
        description: "Severe damage triggers rapid adaptation.",
        prerequisite: "Any Apex Mutation",
        effect: "When you take >15 damage from a single hit, reduce cooldowns by 1 round",
        type: "vital_mutation"
    },
    
    // Combat Mutation Feats (from rulebook) - Warrior Class Only
    killChainAdaptation: {
        name: "Kill-Chain Adaptation",
        description: "Successful kills enhance your combat capabilities.",
        prerequisite: "2 Combat Mutations",
        effect: "After a melee kill, gain +10 ft movement and +1 to hit",
        type: "combat_mutation",
        classRestriction: ["warrior"]
    },
    backlashEngine: {
        name: "Backlash Engine",
        description: "Taking damage while mutated builds up energy.",
        prerequisite: "Adrenal Backlash Core mutation",
        effect: "Each time you're hit while mutated, gain +1 BT",
        type: "combat_mutation",
        classRestriction: ["warrior"]
    },
    evisceratorProtocol: {
        name: "Eviscerator Protocol",
        description: "Your enhanced attacks apply debilitating effects.",
        prerequisite: "Echo Knuckles + Talons mutations",
        effect: "Free offhand hits now apply Bleed or Weakened (player choice)",
        type: "combat_mutation",
        classRestriction: ["warrior"]
    },
    hypermutationSpike: {
        name: "Hypermutation Spike",
        description: "Extend your apex transformation beyond normal limits.",
        prerequisite: "Butcherform Chassis (Apex) mutation",
        effect: "Once per long rest, extend Butcherform to 5 rounds and become immune to stun/slow during duration",
        type: "combat_mutation",
        classRestriction: ["warrior"]
    },
    
    // Magic Feats
    arcaneResonance: {
        name: "Arcane Resonance",
        description: "Your magical abilities resonate with ambient magical energy.",
        prerequisite: "Spellcasting ability, Level 3",
        effect: "Regain one spell slot of 1st level or lower on a natural 20 attack roll",
        type: "magic"
    },
    spellPenetration: {
        name: "Spell Penetration",
        description: "Your spells are particularly effective against magical defenses.",
        prerequisite: "Spellcasting ability, Level 5",
        effect: "+2 bonus to spell attack rolls against targets with spell resistance",
        type: "magic"
    },
    metamagicAdept: {
        name: "Metamagic Adept",
        description: "You have learned to modify your spells in subtle ways.",
        prerequisite: "Spellcasting ability, Level 4",
        effect: "Learn 2 metamagic options, gain 2 sorcery points",
        type: "magic"
    },
    elementalAffinity: {
        name: "Elemental Affinity",
        description: "You have a natural connection to elemental forces.",
        prerequisite: "Spellcasting ability",
        effect: "Choose an element: +1 damage per die for spells of that element",
        type: "magic"
    },
    spellEchoChamer: {
        name: "Spell Echo Chamber",
        description: "Your spells can affect a wider area through magical resonance.",
        prerequisite: "Level 10, Spellcasting ability",
        effect: "Once per long rest, your next area spell affects the area twice",
        type: "magic"
    },
    
    // Aberrant Mutation Feats (from rulebook)
    distortedDominance: {
        name: "Distorted Dominance",
        description: "Your aberrant nature overwhelms enemy actions.",
        prerequisite: "Any Aberrant Mutation",
        effect: "Enemies who fail saves vs your effects also lose 1 action",
        type: "aberrant_mutation"
    },
    terrorEngine: {
        name: "Terror Engine",
        description: "Fear effects provide defensive benefits.",
        prerequisite: "Carrion Signal Gland mutation",
        effect: "If 2+ enemies are Shaken or Disoriented, gain +2 DR",
        type: "aberrant_mutation"
    },
    bornToHorrify: {
        name: "Born to Horrify",
        description: "Your apex mutations grant enhanced resilience.",
        prerequisite: "Any Apex Mutation",
        effect: "While your Apex mutation is active, you may reroll 1 save per turn",
        type: "aberrant_mutation"
    },
    synapticRot: {
        name: "Synaptic Rot",
        description: "Mental attacks disrupt enemy spellcasting.",
        prerequisite: "Wailing Eye or Viral Core mutation",
        effect: "If an enemy fails a WIS or INT save near you, they cannot cast spells next round",
        type: "aberrant_mutation"
    },
    
    // Additional General Feats (expanding to 330 total)
    acrobat: {
        name: "Acrobat",
        description: "You become more nimble and agile.",
        prerequisite: "Dexterity 13 or higher",
        effect: "You gain proficiency in the Acrobatics skill. If you are already proficient, you add double your proficiency bonus to Acrobatics checks.",
        type: "general"
    },
    actor: {
        name: "Actor",
        description: "Skilled at mimicry and dramatics.",
        prerequisite: "Charisma 13 or higher",
        effect: "You have advantage on Charisma (Deception) and Charisma (Performance) checks when trying to pass yourself off as a different person.",
        type: "general"
    },
    alertness: {
        name: "Alertness",
        description: "You have finely tuned senses.",
        prerequisite: "None",
        effect: "+2 bonus to Perception checks and initiative rolls.",
        type: "general"
    },
    ambidexterity: {
        name: "Ambidexterity",
        description: "You can use both hands with equal skill.",
        prerequisite: "Dexterity 15 or higher",
        effect: "You can fight with two weapons without penalty to either hand.",
        type: "general"
    },
    animalAffinity: {
        name: "Animal Affinity",
        description: "You have a way with animals.",
        prerequisite: "Wisdom 13 or higher",
        effect: "You gain proficiency in Animal Handling. If already proficient, you add double your proficiency bonus.",
        type: "general"
    },
    armorProficiency: {
        name: "Armor Proficiency",
        description: "You are skilled with a type of armor.",
        prerequisite: "None",
        effect: "You gain proficiency with light, medium, or heavy armor (choose one).",
        type: "general"
    },
    athleticProdigy: {
        name: "Athletic Prodigy",
        description: "Your physical prowess is exceptional.",
        prerequisite: "Strength or Dexterity 15 or higher",
        effect: "You gain proficiency in Athletics and Acrobatics. If already proficient, you add double your proficiency bonus.",
        type: "general"
    },
    battleReady: {
        name: "Battle Ready",
        description: "You are always prepared for combat.",
        prerequisite: "Constitution 13 or higher",
        effect: "You can don or doff armor in half the normal time and have advantage on initiative rolls.",
        type: "general"
    },
    blindFighting: {
        name: "Blind Fighting",
        description: "You can fight effectively without sight.",
        prerequisite: "Wisdom 13 or higher",
        effect: "You have blindsight with a range of 10 feet. You can effectively see anything within this range that isn't behind total cover.",
        type: "general"
    },
    brawler: {
        name: "Brawler",
        description: "You excel at unarmed combat.",
        prerequisite: "Strength 13 or higher",
        effect: "Your unarmed strikes deal 1d4 + Strength modifier bludgeoning damage and you can grapple as a bonus action.",
        type: "general"
    },
    charger: {
        name: "Charger",
        description: "You can make devastating charge attacks.",
        prerequisite: "Strength 13 or higher",
        effect: "When you use the Dash action, you can make one melee weapon attack or shove as a bonus action.",
        type: "general"
    },
    chef: {
        name: "Chef",
        description: "You are an accomplished cook.",
        prerequisite: "None",
        effect: "You can cook special food during a long rest that provides temporary hit points to your party.",
        type: "general"
    },
    climber: {
        name: "Climber",
        description: "You are an expert at scaling walls and cliffs.",
        prerequisite: "Strength 13 or higher",
        effect: "You gain a climbing speed equal to your walking speed and advantage on Athletics checks made to climb.",
        type: "general"
    },
    coordinator: {
        name: "Coordinator",
        description: "You excel at directing others in combat.",
        prerequisite: "Charisma 13 or higher",
        effect: "As a bonus action, you can grant an ally within 30 feet advantage on their next attack roll.",
        type: "general"
    },
    craftsman: {
        name: "Craftsman",
        description: "You are skilled in creating items.",
        prerequisite: "Intelligence 13 or higher",
        effect: "You gain proficiency with artisan's tools and can craft items in half the normal time.",
        type: "general"
    },
    crossbowExpert: {
        name: "Crossbow Expert",
        description: "You have mastered crossbow combat.",
        prerequisite: "Dexterity 13 or higher",
        effect: "You ignore the loading property of crossbows and can attack with a hand crossbow as a bonus action.",
        type: "general"
    },
    crusher: {
        name: "Crusher",
        description: "You are adept at dealing bludgeoning damage.",
        prerequisite: "Strength 13 or higher",
        effect: "When you hit with a bludgeoning weapon, you can move the target 5 feet and critical hits cause the target to have disadvantage on attack rolls.",
        type: "general"
    },
    defender: {
        name: "Defender",
        description: "You excel at protecting others.",
        prerequisite: "Constitution 13 or higher",
        effect: "When an ally within 5 feet is attacked, you can use your reaction to impose disadvantage on the attack roll.",
        type: "general"
    },
    diplomat: {
        name: "Diplomat",
        description: "You are skilled in negotiation and persuasion.",
        prerequisite: "Charisma 13 or higher",
        effect: "You gain proficiency in Persuasion and Insight. If already proficient, you add double your proficiency bonus.",
        type: "general"
    },
    dungeonDelver: {
        name: "Dungeon Delver",
        description: "You are experienced in underground exploration.",
        prerequisite: "Wisdom 13 or higher",
        effect: "You have advantage on Perception and Investigation checks to detect secret doors and traps.",
        type: "general"
    },
    elementalAdept: {
        name: "Elemental Adept",
        description: "You have mastery over elemental magic.",
        prerequisite: "Ability to cast at least one spell",
        effect: "Choose an element. Spells you cast ignore resistance to that damage type and treat 1s as 2s on damage dice.",
        type: "magic"
    },
    elvenAccuracy: {
        name: "Elven Accuracy",
        description: "Your elven heritage grants supernatural accuracy.",
        prerequisite: "Elf or half-elf",
        effect: "When you have advantage on an attack roll using Dexterity, Intelligence, Wisdom, or Charisma, you can reroll one of the dice.",
        type: "general"
    },
    fencer: {
        name: "Fencer",
        description: "You are skilled with finesse weapons.",
        prerequisite: "Dexterity 13 or higher",
        effect: "When wielding a finesse weapon, you gain +1 AC and can make opportunity attacks when enemies enter your reach.",
        type: "general"
    },
    feyTouched: {
        name: "Fey Touched",
        description: "Your exposure to the Feywild has changed you.",
        prerequisite: "None",
        effect: "You learn misty step and one 1st-level divination or enchantment spell. You can cast each once per long rest.",
        type: "magic"
    },
    fighter: {
        name: "Fighter",
        description: "You have trained extensively in combat.",
        prerequisite: "Strength or Dexterity 13 or higher",
        effect: "You gain proficiency with all simple and martial weapons and can use a bonus action to make an additional attack.",
        type: "general"
    },
    greatWeaponMaster: {
        name: "Great Weapon Master",
        description: "You have mastered two-handed weapons.",
        prerequisite: "Strength 13 or higher",
        effect: "When you score a critical hit or reduce a creature to 0 hit points, you can make another attack as a bonus action.",
        type: "general"
    },
    healer: {
        name: "Healer",
        description: "You are skilled in medicine and healing.",
        prerequisite: "Wisdom 13 or higher",
        effect: "You can use a healer's kit to restore hit points and stabilize dying creatures more effectively.",
        type: "general"
    },
    heavily_armored: {
        name: "Heavily Armored",
        description: "You have trained to master heavy armor.",
        prerequisite: "Proficiency with medium armor",
        effect: "You gain proficiency with heavy armor and increase your Strength score by 1.",
        type: "general"
    },
    inspiring_leader: {
        name: "Inspiring Leader",
        description: "You can inspire others through stirring words.",
        prerequisite: "Charisma 13 or higher",
        effect: "You can spend 10 minutes inspiring your companions, giving them temporary hit points.",
        type: "general"
    },
    keen_mind: {
        name: "Keen Mind",
        description: "You have a mind that can track time, direction, and detail.",
        prerequisite: "Intelligence 13 or higher",
        effect: "You always know which way is north, the number of hours left before sunrise or sunset, and can recall anything you have seen or heard within the past month.",
        type: "general"
    },
    lightly_armored: {
        name: "Lightly Armored",
        description: "You have trained to master light armor.",
        prerequisite: "None",
        effect: "You gain proficiency with light armor and shields, and increase your Strength or Dexterity score by 1.",
        type: "general"
    },
    linguist: {
        name: "Linguist",
        description: "You have studied languages and codes.",
        prerequisite: "Intelligence 13 or higher",
        effect: "You learn three languages and can create written ciphers that require an Intelligence check to decipher.",
        type: "general"
    },
    mage_slayer: {
        name: "Mage Slayer",
        description: "You have practiced techniques for fighting spellcasters.",
        prerequisite: "None",
        effect: "When a creature within 5 feet casts a spell, you can use your reaction to make a melee weapon attack against that creature.",
        type: "general"
    },
    magic_initiate_bard: {
        name: "Magic Initiate (Bard)",
        description: "You have learned some bard magic.",
        prerequisite: "None",
        effect: "You learn two cantrips and one 1st-level spell from the bard spell list. You can cast the spell once per long rest.",
        type: "magic"
    },
    magic_initiate_cleric: {
        name: "Magic Initiate (Cleric)",
        description: "You have learned some cleric magic.",
        prerequisite: "None",
        effect: "You learn two cantrips and one 1st-level spell from the cleric spell list. You can cast the spell once per long rest.",
        type: "magic"
    },
    magic_initiate_druid: {
        name: "Magic Initiate (Druid)",
        description: "You have learned some druid magic.",
        prerequisite: "None",
        effect: "You learn two cantrips and one 1st-level spell from the druid spell list. You can cast the spell once per long rest.",
        type: "magic"
    },
    magic_initiate_sorcerer: {
        name: "Magic Initiate (Sorcerer)",
        description: "You have learned some sorcerer magic.",
        prerequisite: "None",
        effect: "You learn two cantrips and one 1st-level spell from the sorcerer spell list. You can cast the spell once per long rest.",
        type: "magic"
    },
    magic_initiate_warlock: {
        name: "Magic Initiate (Warlock)",
        description: "You have learned some warlock magic.",
        prerequisite: "None",
        effect: "You learn two cantrips and one 1st-level spell from the warlock spell list. You can cast the spell once per long rest.",
        type: "magic"
    },
    magic_initiate_wizard: {
        name: "Magic Initiate (Wizard)",
        description: "You have learned some wizard magic.",
        prerequisite: "None",
        effect: "You learn two cantrips and one 1st-level spell from the wizard spell list. You can cast the spell once per long rest.",
        type: "magic"
    },
    martial_adept_advanced: {
        name: "Martial Adept (Advanced)",
        description: "You have advanced martial training.",
        prerequisite: "Martial Adept feat",
        effect: "You learn two additional maneuvers and gain one more superiority die.",
        type: "general"
    },
    medium_armor_master: {
        name: "Medium Armor Master",
        description: "You have mastered medium armor.",
        prerequisite: "Proficiency with medium armor",
        effect: "Wearing medium armor doesn't impose disadvantage on Dexterity (Stealth) checks and you can add 3 to AC instead of 2 if you have a Dexterity of 16 or higher.",
        type: "general"
    },
    mobile: {
        name: "Mobile",
        description: "You are exceptionally speedy and agile.",
        prerequisite: "None",
        effect: "Your speed increases by 10 feet and you don't provoke opportunity attacks from creatures you've attacked this turn.",
        type: "general"
    },
    moderately_armored: {
        name: "Moderately Armored",
        description: "You have trained to master medium armor.",
        prerequisite: "Proficiency with light armor",
        effect: "You gain proficiency with medium armor and shields, and increase your Strength or Dexterity score by 1.",
        type: "general"
    },
    mounted_combatant: {
        name: "Mounted Combatant",
        description: "You are a dangerous foe to face while mounted.",
        prerequisite: "None",
        effect: "You have advantage on melee attack rolls against unmounted creatures smaller than your mount.",
        type: "general"
    },
    naturalist: {
        name: "Naturalist",
        description: "You have extensive knowledge of nature.",
        prerequisite: "Wisdom 13 or higher",
        effect: "You gain proficiency in Nature and Survival. If already proficient, you add double your proficiency bonus.",
        type: "general"
    },
    orcish_fury: {
        name: "Orcish Fury",
        description: "Your orcish blood burns with fury.",
        prerequisite: "Half-orc or orc",
        effect: "When you hit with an attack using a simple or martial weapon, you can roll one of the weapon's damage dice one additional time.",
        type: "general"
    },
    piercer: {
        name: "Piercer",
        description: "You are adept at dealing piercing damage.",
        prerequisite: "Dexterity 13 or higher",
        effect: "When you hit with a piercing weapon, you can reroll one damage die and critical hits add an extra damage die.",
        type: "general"
    },
    polearm_master: {
        name: "Polearm Master",
        description: "You have mastered polearms and similar weapons.",
        prerequisite: "Strength 13 or higher",
        effect: "When you wield a glaive, halberd, pike, or quarterstaff, you can make opportunity attacks when creatures enter your reach.",
        type: "general"
    },
    prodigy: {
        name: "Prodigy",
        description: "You have exceptional talent in multiple areas.",
        prerequisite: "Half-elf, half-orc, or human",
        effect: "You gain one skill proficiency, one tool proficiency, fluency in one language, and expertise in one skill.",
        type: "general"
    },
    ritual_caster: {
        name: "Ritual Caster",
        description: "You have learned to cast spells as rituals.",
        prerequisite: "Intelligence or Wisdom 13 or higher",
        effect: "You can cast spells with the ritual tag without expending spell slots, but it takes 10 minutes longer.",
        type: "magic"
    },
    savage_attacker: {
        name: "Savage Attacker",
        description: "You fight with primal ferocity.",
        prerequisite: "None",
        effect: "Once per turn when you roll damage for a melee weapon attack, you can reroll the damage dice and use either total.",
        type: "general"
    },
    sentinel: {
        name: "Sentinel",
        description: "You excel at locking down enemies.",
        prerequisite: "None",
        effect: "When you hit a creature with an opportunity attack, the creature's speed becomes 0 for the rest of the turn.",
        type: "general"
    },
    shadow_touched: {
        name: "Shadow Touched",
        description: "Your exposure to the Shadowfell has changed you.",
        prerequisite: "None",
        effect: "You learn invisibility and one 1st-level necromancy or illusion spell. You can cast each once per long rest.",
        type: "magic"
    },
    sharpshooter: {
        name: "Sharpshooter",
        description: "You have mastered ranged weapons.",
        prerequisite: "Dexterity 13 or higher",
        effect: "Your ranged weapon attacks ignore half and three-quarters cover and don't have disadvantage at long range.",
        type: "general"
    },
    shield_master: {
        name: "Shield Master",
        description: "You use shields not just for protection but also for offense.",
        prerequisite: "None",
        effect: "You can use a bonus action to shove a creature within 5 feet of you with your shield.",
        type: "general"
    },
    skill_expert: {
        name: "Skill Expert",
        description: "You have honed your proficiency with particular skills.",
        prerequisite: "None",
        effect: "You gain proficiency in one skill and expertise in one skill you're proficient with.",
        type: "general"
    },
    skulker: {
        name: "Skulker",
        description: "You excel at hiding and moving unseen.",
        prerequisite: "Dexterity 13 or higher",
        effect: "You can hide when lightly obscured and missing with a ranged weapon attack doesn't reveal your position.",
        type: "general"
    },
    slasher: {
        name: "Slasher",
        description: "You are adept at dealing slashing damage.",
        prerequisite: "Strength or Dexterity 13 or higher",
        effect: "When you hit with a slashing weapon, you can reduce the target's speed by 10 feet and critical hits cause disadvantage on attack rolls.",
        type: "general"
    },
    spell_sniper: {
        name: "Spell Sniper",
        description: "You have learned techniques to enhance your spells.",
        prerequisite: "Ability to cast at least one spell",
        effect: "When you cast a spell that requires a ranged attack roll, the spell's range is doubled.",
        type: "magic"
    },
    tavern_brawler: {
        name: "Tavern Brawler",
        description: "You excel at fighting with improvised weapons.",
        prerequisite: "None",
        effect: "You are proficient with improvised weapons and unarmed strikes, and can grapple as a bonus action after hitting with an unarmed strike.",
        type: "general"
    },
    telekinetic: {
        name: "Telekinetic",
        description: "You have learned to move things with your mind.",
        prerequisite: "None",
        effect: "You learn the mage hand cantrip and can cast it without verbal or somatic components. You can use it to shove creatures.",
        type: "magic"
    },
    telepathic: {
        name: "Telepathic",
        description: "You can reach out to others with your mind.",
        prerequisite: "None",
        effect: "You can communicate telepathically with creatures and cast detect thoughts once per long rest.",
        type: "magic"
    },
    tough: {
        name: "Tough",
        description: "Your hit point maximum increases.",
        prerequisite: "None",
        effect: "Your hit point maximum increases by an amount equal to twice your level when you gain this feat.",
        type: "general"
    },
    war_caster: {
        name: "War Caster",
        description: "You have practiced casting spells in the midst of combat.",
        prerequisite: "Ability to cast at least one spell",
        effect: "You have advantage on Constitution saving throws to maintain concentration on spells.",
        type: "magic"
    },
    weapon_master: {
        name: "Weapon Master",
        description: "You have practiced extensively with a variety of weapons.",
        prerequisite: "None",
        effect: "You gain proficiency with four weapons of your choice and increase your Strength or Dexterity score by 1.",
        type: "general"
    },
    
    // Combat Feats (51-100)
    berserker: {
        name: "Berserker",
        description: "You can enter a battle rage.",
        prerequisite: "Constitution 15+",
        effect: "Once per long rest, you can rage for 1 minute, gaining +2 damage on melee attacks and resistance to physical damage.",
        type: "general"
    },
    bladedancer: {
        name: "Bladedancer",
        description: "You move with deadly grace in combat.",
        prerequisite: "Dexterity 15+",
        effect: "When you hit with a finesse weapon, you can move 5 feet without provoking opportunity attacks.",
        type: "general"
    },
    bowyer: {
        name: "Bowyer",
        description: "You are skilled at crafting and using bows.",
        prerequisite: "Proficiency with longbow or shortbow",
        effect: "You can craft masterwork bows and arrows. Your ranged attacks with bows deal +1 damage.",
        type: "general"
    },
    bruiser: {
        name: "Bruiser",
        description: "You excel at intimidating and overpowering foes.",
        prerequisite: "Strength 15+",
        effect: "You gain proficiency in Intimidation and can use Strength instead of Charisma for Intimidation checks.",
        type: "general"
    },
    cavalry: {
        name: "Cavalry",
        description: "You are trained in mounted warfare.",
        prerequisite: "Animal Handling proficiency",
        effect: "You have advantage on attacks against unmounted creatures while mounted, and your mount gains +10 feet movement speed.",
        type: "general"
    },
    cleave: {
        name: "Cleave",
        description: "Your attacks can strike multiple foes.",
        prerequisite: "Strength 13+",
        effect: "When you reduce a creature to 0 hit points with a melee attack, you can make another attack against a different creature within reach.",
        type: "general"
    },
    combatExpertise: {
        name: "Combat Expertise",
        description: "You can trade accuracy for defense.",
        prerequisite: "Intelligence 13+",
        effect: "You can take a -1 penalty to attack rolls to gain +1 AC until your next turn.",
        type: "general"
    },
    deadlyAim: {
        name: "Deadly Aim",
        description: "You can trade accuracy for damage with ranged weapons.",
        prerequisite: "Dexterity 13+",
        effect: "You can take a -1 penalty to ranged attack rolls to deal +2 damage.",
        type: "general"
    },
    disarm: {
        name: "Disarm",
        description: "You can disarm opponents in combat.",
        prerequisite: "Dexterity 13+",
        effect: "You can attempt to disarm an opponent as an attack. The target makes a Strength or Dexterity save (DC 8 + proficiency + ability modifier).",
        type: "general"
    },
    dualWielder: {
        name: "Dual Wielder",
        description: "You master fighting with two weapons.",
        prerequisite: "Dexterity 13+",
        effect: "You can use two-weapon fighting with non-light weapons and gain +1 AC while wielding two weapons.",
        type: "general"
    },
    
    // Magic Feats (101-150)
    arcaneFocus: {
        name: "Arcane Focus",
        description: "You can focus magical energy more effectively.",
        prerequisite: "Spellcasting ability",
        effect: "You can use your spellcasting focus to cast spells without material components worth less than 100 gp.",
        type: "magic"
    },
    battleMage: {
        name: "Battle Mage",
        description: "You blend magic and martial combat.",
        prerequisite: "Spellcasting ability, proficiency with martial weapons",
        effect: "You can cast spells with somatic components while holding weapons and shields.",
        type: "magic"
    },
    cantrip_mastery: {
        name: "Cantrip Mastery",
        description: "Your cantrips become more powerful.",
        prerequisite: "Ability to cast cantrips",
        effect: "Choose one cantrip you know. It deals maximum damage when you roll a natural 20 on the attack roll or the target rolls a natural 1 on their saving throw.",
        type: "magic"
    },
    dispel_mastery: {
        name: "Dispel Mastery",
        description: "You excel at dispelling magic.",
        prerequisite: "Ability to cast dispel magic",
        effect: "When you cast dispel magic, you can target one additional magical effect.",
        type: "magic"
    },
    elemental_mastery: {
        name: "Elemental Mastery",
        description: "You have mastered elemental magic.",
        prerequisite: "Ability to cast 3rd level spells",
        effect: "Choose an element. You can change the damage type of your spells to that element.",
        type: "magic"
    },
    enchantment_focus: {
        name: "Enchantment Focus",
        description: "Your enchantment spells are more effective.",
        prerequisite: "Ability to cast enchantment spells",
        effect: "Creatures have disadvantage on saving throws against your enchantment spells.",
        type: "magic"
    },
    evocation_focus: {
        name: "Evocation Focus",
        description: "Your evocation spells deal more damage.",
        prerequisite: "Ability to cast evocation spells",
        effect: "Your evocation spells deal +1 damage per die rolled.",
        type: "magic"
    },
    familiar_bond: {
        name: "Familiar Bond",
        description: "Your bond with your familiar is stronger.",
        prerequisite: "Ability to cast find familiar",
        effect: "Your familiar gains hit points equal to your level and can attack using your spell attack bonus.",
        type: "magic"
    },
    greater_spell_focus: {
        name: "Greater Spell Focus",
        description: "Your spells are harder to resist.",
        prerequisite: "Spell Focus feat",
        effect: "The DC for your spells increases by an additional +1.",
        type: "magic"
    },
    heighten_spell: {
        name: "Heighten Spell",
        description: "You can cast spells at higher levels.",
        prerequisite: "Ability to cast 3rd level spells",
        effect: "You can expend a spell slot one level higher to increase the spell's DC by +1.",
        type: "magic"
    },
    
    // Skill Feats (151-200)
    acrobatic: {
        name: "Acrobatic",
        description: "You are exceptionally agile.",
        prerequisite: "Dexterity 13+",
        effect: "You gain proficiency in Acrobatics and can use Dexterity instead of Strength for Athletics checks involving jumping.",
        type: "general"
    },
    alertness_improved: {
        name: "Improved Alertness",
        description: "Your senses are incredibly sharp.",
        prerequisite: "Alertness feat",
        effect: "You gain blindsense 10 feet and cannot be surprised while conscious.",
        type: "general"
    },
    animal_companion: {
        name: "Animal Companion",
        description: "You have formed a bond with an animal.",
        prerequisite: "Animal Handling proficiency",
        effect: "You gain an animal companion that follows your commands and fights alongside you.",
        type: "general"
    },
    appraise: {
        name: "Appraise",
        description: "You can accurately determine the value of items.",
        prerequisite: "Intelligence 13+",
        effect: "You can determine the exact value and properties of any item with a successful Investigation check.",
        type: "general"
    },
    artisan: {
        name: "Artisan",
        description: "You are skilled in crafting.",
        prerequisite: "Intelligence 13+",
        effect: "Choose one type of artisan's tools. You gain proficiency and can create masterwork items.",
        type: "general"
    },
    athlete_improved: {
        name: "Improved Athlete",
        description: "Your athletic abilities are exceptional.",
        prerequisite: "Athlete feat",
        effect: "Your climbing and swimming speeds equal your walking speed, and you can long jump your full Strength score.",
        type: "general"
    },
    blind_fight: {
        name: "Blind Fight",
        description: "You can fight without relying on sight.",
        prerequisite: "Wisdom 13+",
        effect: "You don't suffer disadvantage on attack rolls due to being blinded, and you can pinpoint the location of creatures within 30 feet.",
        type: "general"
    },
    burglar: {
        name: "Burglar",
        description: "You are skilled at breaking and entering.",
        prerequisite: "Dexterity 13+",
        effect: "You gain proficiency with thieves' tools and can pick locks and disable traps more effectively.",
        type: "general"
    },
    cartographer: {
        name: "Cartographer",
        description: "You excel at navigation and mapmaking.",
        prerequisite: "Intelligence 13+",
        effect: "You can create accurate maps and never get lost. You have advantage on Survival checks for navigation.",
        type: "general"
    },
    climber_improved: {
        name: "Improved Climber",
        description: "You are an exceptional climber.",
        prerequisite: "Climber feat",
        effect: "You can climb on ceilings and overhangs, and you don't fall when you fail a climbing check by 4 or less.",
        type: "general"
    },
    
    // Social Feats (201-250)
    charismatic: {
        name: "Charismatic",
        description: "Your personality is magnetic.",
        prerequisite: "Charisma 13+",
        effect: "You gain proficiency in Persuasion and Deception. If already proficient, you add double your proficiency bonus.",
        type: "general"
    },
    commanding_presence: {
        name: "Commanding Presence",
        description: "You naturally command respect.",
        prerequisite: "Charisma 15+",
        effect: "You can use your Charisma modifier instead of Strength for Intimidation checks, and you have advantage on Persuasion checks against creatures of lower level.",
        type: "general"
    },
    courtly_manners: {
        name: "Courtly Manners",
        description: "You are well-versed in noble etiquette.",
        prerequisite: "Charisma 13+",
        effect: "You have advantage on Charisma checks when interacting with nobles and can gain audience with important figures more easily.",
        type: "general"
    },
    deceiver: {
        name: "Deceiver",
        description: "You are a master of deception.",
        prerequisite: "Charisma 13+",
        effect: "You gain proficiency in Deception and can lie convincingly even under magical compulsion.",
        type: "general"
    },
    entertainer: {
        name: "Entertainer",
        description: "You can captivate audiences.",
        prerequisite: "Charisma 13+",
        effect: "You gain proficiency in Performance and can earn money and gather information through performances.",
        type: "general"
    },
    fast_talker: {
        name: "Fast Talker",
        description: "You can talk your way out of trouble.",
        prerequisite: "Charisma 15+",
        effect: "You can attempt to distract or confuse enemies with rapid speech, potentially causing them to lose their action.",
        type: "general"
    },
    gossip: {
        name: "Gossip",
        description: "You excel at gathering information.",
        prerequisite: "Charisma 13+",
        effect: "You can gather information about local events, people, and rumors twice as fast as normal.",
        type: "general"
    },
    intimidating: {
        name: "Intimidating",
        description: "Your presence strikes fear into others.",
        prerequisite: "Charisma 13+ or Strength 15+",
        effect: "You gain proficiency in Intimidation and can demoralize enemies in combat, causing them to have disadvantage on their next attack.",
        type: "general"
    },
    leadership: {
        name: "Leadership",
        description: "You inspire others to follow you.",
        prerequisite: "Charisma 15+, level 6+",
        effect: "You can recruit followers and hirelings more easily, and they are more loyal to you.",
        type: "general"
    },
    negotiator: {
        name: "Negotiator",
        description: "You excel at making deals.",
        prerequisite: "Charisma 13+",
        effect: "You can negotiate better prices for goods and services, and you have advantage on Persuasion checks during negotiations.",
        type: "general"
    },
    
    // Survival Feats (251-300)
    endurance: {
        name: "Endurance",
        description: "You can push your body beyond normal limits.",
        prerequisite: "Constitution 13+",
        effect: "You can go twice as long without food, water, or sleep, and you have advantage on Constitution saves against exhaustion.",
        type: "general"
    },
    forager: {
        name: "Forager",
        description: "You can find food and water in the wild.",
        prerequisite: "Wisdom 13+",
        effect: "You can find enough food and water for yourself and up to 6 other people each day in any terrain except deserts or arctic regions.",
        type: "general"
    },
    hardy: {
        name: "Hardy",
        description: "You are resistant to environmental hazards.",
        prerequisite: "Constitution 15+",
        effect: "You have resistance to cold and heat damage, and you have advantage on saves against disease and poison.",
        type: "general"
    },
    hunter: {
        name: "Hunter",
        description: "You are skilled at tracking and hunting prey.",
        prerequisite: "Wisdom 13+",
        effect: "You gain proficiency in Survival and can track creatures across any terrain. You deal +2 damage to beasts and monstrosities.",
        type: "general"
    },
    iron_will: {
        name: "Iron Will",
        description: "Your willpower is unbreakable.",
        prerequisite: "Wisdom 15+",
        effect: "You have advantage on Wisdom saving throws and are immune to being charmed or frightened.",
        type: "general"
    },
    pathfinder: {
        name: "Pathfinder",
        description: "You can navigate any terrain.",
        prerequisite: "Wisdom 13+",
        effect: "You and your party can move at normal speed while tracking, and difficult terrain doesn't slow your group's travel.",
        type: "general"
    },
    ranger_training: {
        name: "Ranger Training",
        description: "You have learned wilderness survival techniques.",
        prerequisite: "Wisdom 13+",
        effect: "You gain proficiency in Survival and Nature, and you can hide even when only lightly obscured by natural phenomena.",
        type: "general"
    },
    scavenger: {
        name: "Scavenger",
        description: "You can find useful items in unlikely places.",
        prerequisite: "Intelligence 13+",
        effect: "You can find basic equipment and supplies in ruins, dungeons, and other locations where others have been.",
        type: "general"
    },
    survivalist: {
        name: "Survivalist",
        description: "You excel at surviving in harsh conditions.",
        prerequisite: "Constitution 13+, Wisdom 13+",
        effect: "You can survive in any environment and can help others do the same. You need only half the normal amount of food and water.",
        type: "general"
    },
    tracker: {
        name: "Tracker",
        description: "You can follow tracks across any terrain.",
        prerequisite: "Wisdom 15+",
        effect: "You can track creatures across any surface, including water and air. You can determine the age, size, and condition of tracks.",
        type: "general"
    },
    
    // Exotic Feats (301-330)
    aberrant_mind: {
        name: "Aberrant Mind",
        description: "Your mind has been touched by alien intelligence.",
        prerequisite: "Intelligence 15+",
        effect: "You can communicate telepathically with aberrations and have resistance to psychic damage.",
        type: "aberrant_mutation"
    },
    astral_projection: {
        name: "Astral Projection",
        description: "You can project your consciousness to other planes.",
        prerequisite: "Wisdom 17+, level 15+",
        effect: "Once per long rest, you can cast astral projection without expending a spell slot.",
        type: "magic"
    },
    divine_favor: {
        name: "Divine Favor",
        description: "You have earned the favor of a deity.",
        prerequisite: "Charisma 15+, worship a deity",
        effect: "Once per long rest, you can call upon divine aid to automatically succeed on one saving throw or ability check.",
        type: "magic"
    },
    dragon_blood: {
        name: "Dragon Blood",
        description: "Draconic blood flows through your veins.",
        prerequisite: "Dragonborn or sorcerer with draconic bloodline",
        effect: "You gain resistance to your draconic ancestry's damage type and can speak, read, and write Draconic.",
        type: "general"
    },
    elemental_body: {
        name: "Elemental Body",
        description: "Your body has been infused with elemental energy.",
        prerequisite: "Constitution 15+, exposure to elemental plane",
        effect: "Choose an element. You gain resistance to that damage type and your unarmed strikes deal that damage type.",
        type: "general"
    },
    fey_ancestry: {
        name: "Fey Ancestry",
        description: "You have fey blood in your lineage.",
        prerequisite: "Charisma 13+",
        effect: "You have advantage on saving throws against being charmed, and magic can't put you to sleep.",
        type: "general"
    },
    giant_strength: {
        name: "Giant Strength",
        description: "You possess the strength of giants.",
        prerequisite: "Strength 17+",
        effect: "Your carrying capacity doubles, and you can wield weapons one size larger than normal without penalty.",
        type: "general"
    },
    immortal_vigor: {
        name: "Immortal Vigor",
        description: "You age more slowly than normal.",
        prerequisite: "Constitution 17+, level 10+",
        effect: "You age at half the normal rate and have advantage on death saving throws.",
        type: "general"
    },
    planar_binding: {
        name: "Planar Binding",
        description: "You can bind extraplanar creatures to your service.",
        prerequisite: "Charisma 15+, ability to cast 5th level spells",
        effect: "You can cast planar binding once per long rest without expending a spell slot.",
        type: "magic"
    },
    void_touched: {
        name: "Void Touched",
        description: "You have been exposed to the void between planes.",
        prerequisite: "Wisdom 15+",
        effect: "You have resistance to necrotic damage and can see normally in magical darkness.",
        type: "general"
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        RACES,
        CLASSES,
        BACKGROUNDS,
        SPELLS,
        EQUIPMENT,
        FEATS,
        rollDice,
        rollAbilityScore,
        getAbilityModifier,
        formatModifier
    };
}