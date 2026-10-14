# Complete finite feat supplements

Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.

All entries here are NEW bounded supplements. Their source directions are settled; the assembled candidate still awaits exact review. They do not add original registry IDs or promote comparison class/spell cards.

## SUP-01 — General Combat

```json
{
  "profile": "AC12+floor(current ownerPB/2); dynamic maximumHP5+current total owner level; all ordinary saves use current ownerPB alone; other ability checks use template ability modifiers, no PB unless a real source grants it. Template INT3 is a feat-profile value, not proof that a real source beast meets the INT<7 admission gate.",
  "nativeBody": "Preserve actual original source profile, body identity, current health ratio, size, breathing, conditions, disease, hunger, custody and age. Templates replace only their stated combat/ability/speed values for this bond. Any actual anatomy incapacity/sensory blocker remains. No template creates a supernatural sense, trait, hand or extra body.",
  "actions": "One command and offensive allowance across owner companions/devices per numbered round. Commanded body has one attached phase after whole owner regular turn, move plus chosen legal attack or standard Dash/Disengage/Help/Dodge; Dash adds one currentSpeed to its phase cap, Disengage suppresses opportunities for that phase, Help follows actual5ft/physically possible aid and expires at the next original companion-start marker. No independent BA/Reaction/turn/death save; no extra-turn phase. Uncommanded only defensive movement/Dodge.",
  "conversion": "Admission requires a real living animal with positiveHP and positive maximumHP and an actual eligible willing/tamed receipt. Initial and release conversion preserves health ratio using max(1,floor(newMax*oldHP/oldMax)), not a heal/damage event. At0 the feat animal is dead, never eligible for conversion. Save the prior source profile rather than deriving a new one on release.",
  "recovery": "No resummon, free rest healing, unprinted Hit Dice or new original animal from a saved profile. External legal healing/resurrection retains its actual costs and rules; resurrection returns the same body unbonded, and new bonding still requires the post-death completedLR plus full procedure. Capacity change never repairs injury, replenishes resources or creates death/HP-loss triggers."
}
```

## SUP-02 — General Combat

```json
[
  {
    "id": "feat-animal.ground",
    "name": "Ground companion",
    "eligibleBody": "An actual positive-HP living Small or Medium terrestrial Beast with ordinary biting anatomy; preserve its actual size. Dog/fox-like examples are illustrative, not free supplied animals.",
    "abilities": {
      "STR": 12,
      "DEX": 12,
      "CON": 12,
      "INT": 3,
      "WIS": 12,
      "CHA": 6
    },
    "movement": {
      "walkFeet": 30
    },
    "attack": "One melee bite, reach5ft, attack=ownerPB+owner actualWIS modifier, damage1d6piercing; no addedWIS damage and no automatic level scaling.",
    "sense": "Choose its actually sourced keen hearing OR smell, if present, for advantage on that sense's actual Perception checks. No new keen sense if absent.",
    "limits": "No Pack Tactics, knockdown, grapple, multiattack, burrow or extraordinary source powers. Carrying uses this actual body/STR and ordinary Load/pounds limits, real harness/hands. A mount must separately meet real riding eligibility."
  },
  {
    "id": "feat-animal.flyer",
    "name": "Flying companion",
    "eligibleBody": "An actual positive-HP living Tiny winged Beast that already possesses natural flight and a pecking/biting attack. No Hover.",
    "abilities": {
      "STR": 3,
      "DEX": 14,
      "CON": 10,
      "INT": 3,
      "WIS": 14,
      "CHA": 6
    },
    "movement": {
      "walkFeet": 10,
      "flyFeet": 30
    },
    "attack": "One melee peck/bite, reach5ft, attack=ownerPB+owner actualWIS modifier, damage1d4piercing; no addedWIS damage and no level scaling.",
    "sense": "Retain actual sourced keen sight, if present, as advantage on that sense's Perception checks; no automatic darkvision/blindsight.",
    "limits": "No free Flyby, invisibility, aerial carrying exception, Hover, multiattack or ability to carry a Medium ally. Ordinary falling, weather, carrying and support apply."
  },
  {
    "id": "feat-animal.swimmer",
    "name": "Swimming companion",
    "eligibleBody": "An actual positive-HP living Small Beast with native swimming and biting anatomy. Keep its real breathing requirements; a fish gains no lungs and an air breather gains no gills.",
    "abilities": {
      "STR": 10,
      "DEX": 12,
      "CON": 12,
      "INT": 3,
      "WIS": 12,
      "CHA": 6
    },
    "movement": {
      "walkFeet": 5,
      "swimFeet": 30
    },
    "attack": "One melee bite, reach5ft, attack=ownerPB+owner actualWIS modifier, damage1d6piercing; no addedWIS damage and no level scaling.",
    "sense": "Retain one actually sourced keen hearing OR smell, if present, for that sense's Perception advantage only.",
    "limits": "The5ft ground movement is crawling/flopping for a body without legs, paying ordinary crawl cost and suffocation/exposure; no new hands, amphibiousness, Water Breathing, multiattack or sonar."
  }
]
```

## SUP-03 — General Combat

```json
[
  {
    "id": "feat-maneuver.measured-strike",
    "name": "Measured Strike",
    "activation": "Within one actual weapon attack, before its attack roll",
    "cost": "One superiorityd6",
    "procedure": "Roll the spentd6 and add it to that one attack roll. Choose before seeing the d20/outcome; natural1 still misses and no extra critical range is created. It adds no damage and supplies no attack, target permission or extra Action."
  },
  {
    "id": "feat-maneuver.driving-shove",
    "name": "Driving Shove",
    "activation": "Replace one Attack Action attack with ordinary Shove",
    "cost": "One superiorityd6 plus the replaced attack",
    "procedure": "Before both opposed rolls, spend/roll thed6 and add it to yourSTR Athletics total for that one ordinary Shove. Target choosesAthletics/Acrobatics; tie preserves state. Actual reach/one-size-larger cap applies; success still pushes5ft away OR Prone, never both solely from this maneuver. It adds no damage."
  },
  {
    "id": "feat-maneuver.disarming-feint",
    "name": "Disarming Feint",
    "activation": "Replace one Attack Action attack with ordinary opposed Disarm",
    "cost": "One superiorityd6 plus replaced attack",
    "procedure": "Choose a reachable actually held droppable item and an ordinary legal Athletics or weapon-check Disarm. Before rolls, spend/roll thed6 and add it to your one opposed total; defender usesAthletics/Acrobatics, tie preserves state. Success uses the existing adjacent/own-space drop placement, not automatic custody. No damage, severed bond or proficiency grant. The save-based Disarm feat and Whip Control are separate procedures and do not acquire this bonus."
  },
  {
    "id": "feat-maneuver.guarding-deflection",
    "name": "Guarding Deflection",
    "activation": "Reaction when one direct damage event would damage you",
    "cost": "One superiorityd6 and the actual Reaction",
    "procedure": "After passive defenses but before tempHP, spend/roll1d6 to reduce that whole resolved event by its face, minimum0. Allocate across stable native component order. Attached conditions remain. No re-mitigation of transfer packets that forbid recipient mitigation, HP sacrifice, state assignment or direct death. It neither changes a hit to a miss nor qualifies as Riposte's successful Parry."
  },
  {
    "id": "feat-maneuver.measured-advance",
    "name": "Measured Advance",
    "activation": "Bonus Action on your own regular turn",
    "cost": "One superiorityd6 and the actual BA",
    "procedure": "Spend/roll1d6, gaining a separate movement-cost budget of5×face feet resolved immediately. Use one already available movement mode with nonzeroSpeed, pay normal terrain/crawl/squeeze costs, respect legal endpoints and provoke ordinary opportunity attacks. No teleport, new movement mode, free Disengage, replenished ordinary movement or banked distance. Interrupted unspent distance is lost."
  },
  {
    "id": "feat-maneuver.rallying-signal",
    "name": "Rallying Signal",
    "activation": "Action under the ordinary Rally procedure",
    "cost": "One superiorityd6 and the actual Action",
    "procedure": "Choose one actual ally within30ft able to perceive the rally and one active source-qualifiedFrightened record. Before rolling the ordinaryCHA task check at its sourceDC (otherwise10), spend/roll thed6 and add its face to the total. Apply actual task degrees/natural shift; success ends only that selected record. NoHP/tempHP, loyalty, extra save, new ally turn or automatic cure of other fear records."
  }
]
```

## SUP-04 — General Combat

```json
{
  "Bard": {
    "featCastingAbility": "CHA",
    "rank0Choices": 47,
    "rank1Choices": 46,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "daze",
        "name": "Daze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "calm-whispers",
        "name": "Calm Whispers",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-flicker",
        "name": "Mental Flicker",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "false-comfort",
        "name": "False Comfort",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimmering-eyes",
        "name": "Glimmering Eyes",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "disrupt-memory",
        "name": "Disrupt Memory",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "enthralling-tune",
        "name": "Enthralling Tune",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-tap",
        "name": "Mental Tap",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "friends",
        "name": "Friends",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "lullaby",
        "name": "Lullaby",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "soothe-animal",
        "name": "Soothe Animal",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-sympathy",
        "name": "Faction Sympathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "alignment-empathy",
        "name": "Alignment Empathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-whisper",
        "name": "Resonance Whisper",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-suggestion",
        "name": "Minor Suggestion",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "beguiling-gaze",
        "name": "Beguiling Gaze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "mesmerize",
        "name": "Mesmerize",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "pacify",
        "name": "Pacify",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "sleep",
        "name": "Sleep",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "confusing-flash",
        "name": "Confusing Flash",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaken-will",
        "name": "Weaken Will",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "distract",
        "name": "Distract",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "voice-of-peace",
        "name": "Voice of Peace",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "command",
        "name": "Command",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "hideous-laughter",
        "name": "Hideous Laughter",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "heroism",
        "name": "Heroism",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-charm",
        "name": "Faction Charm",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-suggestion",
        "name": "Alignment Suggestion",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-influence",
        "name": "Resonance Influence",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "enthrall",
        "name": "Enthrall",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "ghost-sound",
        "name": "Ghost Sound",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-image",
        "name": "Minor Image",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "flickerstep",
        "name": "Flickerstep",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "silent-echo",
        "name": "Silent Echo",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirage-spark",
        "name": "Mirage Spark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "illusive-flash",
        "name": "Illusive Flash",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-puppet",
        "name": "Shadow Puppet",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blurred-visage",
        "name": "Blurred Visage",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "disguise-self-minor",
        "name": "Disguise Self (Minor)",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "distort-voice",
        "name": "Distort Voice",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-footsteps",
        "name": "Phantom Footsteps",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-mark",
        "name": "Shadow Mark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blur-vision",
        "name": "Blur Vision",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirror-image",
        "name": "Mirror Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "silent-image",
        "name": "Silent Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "color-spray",
        "name": "Color Spray",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-blade",
        "name": "Illusory Blade",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "veil-of-mist",
        "name": "Veil of Mist",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "phantom-grasp",
        "name": "Phantom Grasp",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "mask-voice",
        "name": "Mask Voice",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-footsteps",
        "name": "False Footsteps",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "disguise-self",
        "name": "Disguise Self",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-script",
        "name": "Illusory Script",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "distort-value",
        "name": "Distort Value",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "uncontrollable-laughter",
        "name": "Uncontrollable Laughter",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-terrain",
        "name": "Illusory Terrain",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Bard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Cleric": {
    "featCastingAbility": "WIS",
    "rank0Choices": 63,
    "rank1Choices": 59,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "foresight-flicker",
        "name": "Foresight Flicker",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "guiding-spark",
        "name": "Guiding Spark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "omen-whisper",
        "name": "Omen Whisper",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-emotion",
        "name": "Detect Emotion",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-glimpse",
        "name": "Aura Glimpse",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "far-echo",
        "name": "Far Echo",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "predict-movement",
        "name": "Predict Movement",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "soul-mark",
        "name": "Soul Mark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-alignment",
        "name": "Sense Alignment",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimpse-future",
        "name": "Glimpse Future",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-faction",
        "name": "Detect Faction",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-sight",
        "name": "Resonance Sight",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-weather",
        "name": "Detect Weather",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-corruption",
        "name": "Sense Corruption",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "true-sight-lesser",
        "name": "True Sight (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "warning-ward",
        "name": "Warning Ward",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "scribe-destiny",
        "name": "Scribe Destiny",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "mark-omen",
        "name": "Mark Omen",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "clairaudience-lesser",
        "name": "Clairaudience (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "fate-coin",
        "name": "Fate Coin",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-secret-doors",
        "name": "Detect Secret Doors",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-insight",
        "name": "Faction Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-sense",
        "name": "Alignment Sense",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-map",
        "name": "Resonance Map",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "locate-object",
        "name": "Locate Object",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "read-memories",
        "name": "Read Memories",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-insight",
        "name": "Corruption Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "grave-spark",
        "name": "Grave Spark",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "rotting-touch",
        "name": "Rotting Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "finger-of-the-dead",
        "name": "Finger of the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "corpse-light",
        "name": "Corpse Light",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-of-the-crypt",
        "name": "Chill of the Crypt",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "whispers-from-beyond",
        "name": "Whispers from Beyond",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-claw",
        "name": "Spectral Claw",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "gravewind-flicker",
        "name": "Gravewind Flicker",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "toll-the-dead",
        "name": "Toll the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "death-whisper",
        "name": "Death Whisper",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "bone-shard",
        "name": "Bone Shard",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "wither-plant",
        "name": "Wither Plant",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-undead",
        "name": "Sense Undead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "blood-trickle",
        "name": "Blood Trickle",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "decay",
        "name": "Decay",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "lifedraw",
        "name": "Lifedraw",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-lesser-skeleton",
        "name": "Summon Lesser Skeleton",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "dread-whisper",
        "name": "Dread Whisper",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "putrefy",
        "name": "Putrefy",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "pact-of-bone",
        "name": "Pact of Bone",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "soul-tap",
        "name": "Soul Tap",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "eyes-of-the-grave",
        "name": "Eyes of the Grave",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "ray-of-sickness",
        "name": "Ray of Sickness",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "inflict-wounds",
        "name": "Inflict Wounds",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "corpse-puppet",
        "name": "Corpse Puppet",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "bone-armor",
        "name": "Bone Armor",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "speak-with-dead-lesser",
        "name": "Speak with Dead (Lesser)",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Cleric",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Crimson Agent": {
    "featCastingAbility": "INT",
    "rank0Choices": 62,
    "rank1Choices": 61,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "daze",
        "name": "Daze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "calm-whispers",
        "name": "Calm Whispers",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-flicker",
        "name": "Mental Flicker",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "false-comfort",
        "name": "False Comfort",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimmering-eyes",
        "name": "Glimmering Eyes",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "disrupt-memory",
        "name": "Disrupt Memory",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "enthralling-tune",
        "name": "Enthralling Tune",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-tap",
        "name": "Mental Tap",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "friends",
        "name": "Friends",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "lullaby",
        "name": "Lullaby",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "soothe-animal",
        "name": "Soothe Animal",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-sympathy",
        "name": "Faction Sympathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "alignment-empathy",
        "name": "Alignment Empathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-whisper",
        "name": "Resonance Whisper",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-suggestion",
        "name": "Minor Suggestion",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "beguiling-gaze",
        "name": "Beguiling Gaze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "mesmerize",
        "name": "Mesmerize",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "pacify",
        "name": "Pacify",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "sleep",
        "name": "Sleep",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "confusing-flash",
        "name": "Confusing Flash",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaken-will",
        "name": "Weaken Will",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "distract",
        "name": "Distract",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "voice-of-peace",
        "name": "Voice of Peace",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "command",
        "name": "Command",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "hideous-laughter",
        "name": "Hideous Laughter",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "heroism",
        "name": "Heroism",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-charm",
        "name": "Faction Charm",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-suggestion",
        "name": "Alignment Suggestion",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-influence",
        "name": "Resonance Influence",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "enthrall",
        "name": "Enthrall",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-ray",
        "name": "Arcane Ray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sparkbolt",
        "name": "Sparkbolt",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "freezing-touch",
        "name": "Freezing Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flame-lash",
        "name": "Flame Lash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "soundburst",
        "name": "Soundburst",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-combustion",
        "name": "Minor Combustion",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "force-needle",
        "name": "Force Needle",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-echo",
        "name": "Arcane Echo",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shocking-grasp",
        "name": "Shocking Grasp",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "ray-of-frost",
        "name": "Ray of Frost",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "acid-splash",
        "name": "Acid Splash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sacred-flame",
        "name": "Sacred Flame",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thunderclap",
        "name": "Thunderclap",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "poison-spray",
        "name": "Poison Spray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fireburst",
        "name": "Fireburst",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "frost-arrow",
        "name": "Frost Arrow",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chain-jolt",
        "name": "Chain Jolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "force-spike",
        "name": "Force Spike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-missile-storm",
        "name": "Magic Missile Storm",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunder-clap",
        "name": "Thunder Clap",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-shield-shatter",
        "name": "Arcane Shield Shatter",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ignition-bolt",
        "name": "Ignition Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-hands",
        "name": "Burning Hands",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "earth-tremor",
        "name": "Earth Tremor",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "hellish-rebuke",
        "name": "Hellish Rebuke",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ice-knife",
        "name": "Ice Knife",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunderwave",
        "name": "Thunderwave",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "witch-bolt",
        "name": "Witch Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "zephyr-strike",
        "name": "Zephyr Strike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ghost-sound",
        "name": "Ghost Sound",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-image",
        "name": "Minor Image",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "flickerstep",
        "name": "Flickerstep",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "silent-echo",
        "name": "Silent Echo",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirage-spark",
        "name": "Mirage Spark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "illusive-flash",
        "name": "Illusive Flash",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-puppet",
        "name": "Shadow Puppet",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blurred-visage",
        "name": "Blurred Visage",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "disguise-self-minor",
        "name": "Disguise Self (Minor)",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "distort-voice",
        "name": "Distort Voice",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-footsteps",
        "name": "Phantom Footsteps",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-mark",
        "name": "Shadow Mark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blur-vision",
        "name": "Blur Vision",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirror-image",
        "name": "Mirror Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "silent-image",
        "name": "Silent Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "color-spray",
        "name": "Color Spray",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-blade",
        "name": "Illusory Blade",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "veil-of-mist",
        "name": "Veil of Mist",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "phantom-grasp",
        "name": "Phantom Grasp",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "mask-voice",
        "name": "Mask Voice",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-footsteps",
        "name": "False Footsteps",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "disguise-self",
        "name": "Disguise Self",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-script",
        "name": "Illusory Script",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "distort-value",
        "name": "Distort Value",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "uncontrollable-laughter",
        "name": "Uncontrollable Laughter",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-terrain",
        "name": "Illusory Terrain",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "grave-spark",
        "name": "Grave Spark",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "rotting-touch",
        "name": "Rotting Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "finger-of-the-dead",
        "name": "Finger of the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "corpse-light",
        "name": "Corpse Light",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-of-the-crypt",
        "name": "Chill of the Crypt",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "whispers-from-beyond",
        "name": "Whispers from Beyond",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-claw",
        "name": "Spectral Claw",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "gravewind-flicker",
        "name": "Gravewind Flicker",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "toll-the-dead",
        "name": "Toll the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "death-whisper",
        "name": "Death Whisper",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "bone-shard",
        "name": "Bone Shard",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "wither-plant",
        "name": "Wither Plant",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-undead",
        "name": "Sense Undead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "blood-trickle",
        "name": "Blood Trickle",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "decay",
        "name": "Decay",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "lifedraw",
        "name": "Lifedraw",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-lesser-skeleton",
        "name": "Summon Lesser Skeleton",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "dread-whisper",
        "name": "Dread Whisper",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "putrefy",
        "name": "Putrefy",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "pact-of-bone",
        "name": "Pact of Bone",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "soul-tap",
        "name": "Soul Tap",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "eyes-of-the-grave",
        "name": "Eyes of the Grave",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "ray-of-sickness",
        "name": "Ray of Sickness",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "inflict-wounds",
        "name": "Inflict Wounds",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "corpse-puppet",
        "name": "Corpse Puppet",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "bone-armor",
        "name": "Bone Armor",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "speak-with-dead-lesser",
        "name": "Speak with Dead (Lesser)",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Crimson Agent",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Dragoon": {
    "featCastingAbility": "STR",
    "rank0Choices": 48,
    "rank1Choices": 48,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-ray",
        "name": "Arcane Ray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sparkbolt",
        "name": "Sparkbolt",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "freezing-touch",
        "name": "Freezing Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flame-lash",
        "name": "Flame Lash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "soundburst",
        "name": "Soundburst",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-combustion",
        "name": "Minor Combustion",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "force-needle",
        "name": "Force Needle",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-echo",
        "name": "Arcane Echo",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shocking-grasp",
        "name": "Shocking Grasp",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "ray-of-frost",
        "name": "Ray of Frost",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "acid-splash",
        "name": "Acid Splash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sacred-flame",
        "name": "Sacred Flame",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thunderclap",
        "name": "Thunderclap",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "poison-spray",
        "name": "Poison Spray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fireburst",
        "name": "Fireburst",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "frost-arrow",
        "name": "Frost Arrow",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chain-jolt",
        "name": "Chain Jolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "force-spike",
        "name": "Force Spike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-missile-storm",
        "name": "Magic Missile Storm",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunder-clap",
        "name": "Thunder Clap",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-shield-shatter",
        "name": "Arcane Shield Shatter",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ignition-bolt",
        "name": "Ignition Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-hands",
        "name": "Burning Hands",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "earth-tremor",
        "name": "Earth Tremor",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "hellish-rebuke",
        "name": "Hellish Rebuke",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ice-knife",
        "name": "Ice Knife",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunderwave",
        "name": "Thunderwave",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "witch-bolt",
        "name": "Witch Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "zephyr-strike",
        "name": "Zephyr Strike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Dragoon",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Druid": {
    "featCastingAbility": "WIS",
    "rank0Choices": 64,
    "rank1Choices": 64,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "grave-spark",
        "name": "Grave Spark",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "rotting-touch",
        "name": "Rotting Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "finger-of-the-dead",
        "name": "Finger of the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "corpse-light",
        "name": "Corpse Light",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-of-the-crypt",
        "name": "Chill of the Crypt",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "whispers-from-beyond",
        "name": "Whispers from Beyond",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-claw",
        "name": "Spectral Claw",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "gravewind-flicker",
        "name": "Gravewind Flicker",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "toll-the-dead",
        "name": "Toll the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "death-whisper",
        "name": "Death Whisper",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "bone-shard",
        "name": "Bone Shard",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "wither-plant",
        "name": "Wither Plant",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-undead",
        "name": "Sense Undead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "blood-trickle",
        "name": "Blood Trickle",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "decay",
        "name": "Decay",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "lifedraw",
        "name": "Lifedraw",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-lesser-skeleton",
        "name": "Summon Lesser Skeleton",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "dread-whisper",
        "name": "Dread Whisper",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "putrefy",
        "name": "Putrefy",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "pact-of-bone",
        "name": "Pact of Bone",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "soul-tap",
        "name": "Soul Tap",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "eyes-of-the-grave",
        "name": "Eyes of the Grave",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "ray-of-sickness",
        "name": "Ray of Sickness",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "inflict-wounds",
        "name": "Inflict Wounds",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "corpse-puppet",
        "name": "Corpse Puppet",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "bone-armor",
        "name": "Bone Armor",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "speak-with-dead-lesser",
        "name": "Speak with Dead (Lesser)",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Druid",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Mage": {
    "featCastingAbility": "INT",
    "rank0Choices": 80,
    "rank1Choices": 79,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-ray",
        "name": "Arcane Ray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sparkbolt",
        "name": "Sparkbolt",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "freezing-touch",
        "name": "Freezing Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flame-lash",
        "name": "Flame Lash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "soundburst",
        "name": "Soundburst",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-combustion",
        "name": "Minor Combustion",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "force-needle",
        "name": "Force Needle",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-echo",
        "name": "Arcane Echo",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shocking-grasp",
        "name": "Shocking Grasp",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "ray-of-frost",
        "name": "Ray of Frost",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "acid-splash",
        "name": "Acid Splash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sacred-flame",
        "name": "Sacred Flame",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thunderclap",
        "name": "Thunderclap",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "poison-spray",
        "name": "Poison Spray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fireburst",
        "name": "Fireburst",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "frost-arrow",
        "name": "Frost Arrow",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chain-jolt",
        "name": "Chain Jolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "force-spike",
        "name": "Force Spike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-missile-storm",
        "name": "Magic Missile Storm",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunder-clap",
        "name": "Thunder Clap",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-shield-shatter",
        "name": "Arcane Shield Shatter",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ignition-bolt",
        "name": "Ignition Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-hands",
        "name": "Burning Hands",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "earth-tremor",
        "name": "Earth Tremor",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "hellish-rebuke",
        "name": "Hellish Rebuke",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ice-knife",
        "name": "Ice Knife",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunderwave",
        "name": "Thunderwave",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "witch-bolt",
        "name": "Witch Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "zephyr-strike",
        "name": "Zephyr Strike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Monk": {
    "featCastingAbility": "DEX",
    "rank0Choices": 48,
    "rank1Choices": 48,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "ghost-sound",
        "name": "Ghost Sound",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-image",
        "name": "Minor Image",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "flickerstep",
        "name": "Flickerstep",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "silent-echo",
        "name": "Silent Echo",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirage-spark",
        "name": "Mirage Spark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "illusive-flash",
        "name": "Illusive Flash",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-puppet",
        "name": "Shadow Puppet",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blurred-visage",
        "name": "Blurred Visage",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "disguise-self-minor",
        "name": "Disguise Self (Minor)",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "distort-voice",
        "name": "Distort Voice",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-footsteps",
        "name": "Phantom Footsteps",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-mark",
        "name": "Shadow Mark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blur-vision",
        "name": "Blur Vision",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirror-image",
        "name": "Mirror Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "silent-image",
        "name": "Silent Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "color-spray",
        "name": "Color Spray",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-blade",
        "name": "Illusory Blade",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "veil-of-mist",
        "name": "Veil of Mist",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "phantom-grasp",
        "name": "Phantom Grasp",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "mask-voice",
        "name": "Mask Voice",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-footsteps",
        "name": "False Footsteps",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "disguise-self",
        "name": "Disguise Self",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-script",
        "name": "Illusory Script",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "distort-value",
        "name": "Distort Value",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "uncontrollable-laughter",
        "name": "Uncontrollable Laughter",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-terrain",
        "name": "Illusory Terrain",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Monk",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Mirrorsage": {
    "featCastingAbility": "INT",
    "rank0Choices": 63,
    "rank1Choices": 59,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "foresight-flicker",
        "name": "Foresight Flicker",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "guiding-spark",
        "name": "Guiding Spark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "omen-whisper",
        "name": "Omen Whisper",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-emotion",
        "name": "Detect Emotion",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-glimpse",
        "name": "Aura Glimpse",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "far-echo",
        "name": "Far Echo",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "predict-movement",
        "name": "Predict Movement",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "soul-mark",
        "name": "Soul Mark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-alignment",
        "name": "Sense Alignment",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimpse-future",
        "name": "Glimpse Future",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-faction",
        "name": "Detect Faction",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-sight",
        "name": "Resonance Sight",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-weather",
        "name": "Detect Weather",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-corruption",
        "name": "Sense Corruption",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "true-sight-lesser",
        "name": "True Sight (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "warning-ward",
        "name": "Warning Ward",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "scribe-destiny",
        "name": "Scribe Destiny",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "mark-omen",
        "name": "Mark Omen",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "clairaudience-lesser",
        "name": "Clairaudience (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "fate-coin",
        "name": "Fate Coin",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-secret-doors",
        "name": "Detect Secret Doors",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-insight",
        "name": "Faction Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-sense",
        "name": "Alignment Sense",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-map",
        "name": "Resonance Map",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "locate-object",
        "name": "Locate Object",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "read-memories",
        "name": "Read Memories",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-insight",
        "name": "Corruption Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "daze",
        "name": "Daze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "calm-whispers",
        "name": "Calm Whispers",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-flicker",
        "name": "Mental Flicker",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "false-comfort",
        "name": "False Comfort",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimmering-eyes",
        "name": "Glimmering Eyes",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "disrupt-memory",
        "name": "Disrupt Memory",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "enthralling-tune",
        "name": "Enthralling Tune",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-tap",
        "name": "Mental Tap",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "friends",
        "name": "Friends",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "lullaby",
        "name": "Lullaby",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "soothe-animal",
        "name": "Soothe Animal",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-sympathy",
        "name": "Faction Sympathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "alignment-empathy",
        "name": "Alignment Empathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-whisper",
        "name": "Resonance Whisper",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-suggestion",
        "name": "Minor Suggestion",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "beguiling-gaze",
        "name": "Beguiling Gaze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "mesmerize",
        "name": "Mesmerize",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "pacify",
        "name": "Pacify",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "sleep",
        "name": "Sleep",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "confusing-flash",
        "name": "Confusing Flash",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaken-will",
        "name": "Weaken Will",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "distract",
        "name": "Distract",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "voice-of-peace",
        "name": "Voice of Peace",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "command",
        "name": "Command",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "hideous-laughter",
        "name": "Hideous Laughter",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "heroism",
        "name": "Heroism",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-charm",
        "name": "Faction Charm",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-suggestion",
        "name": "Alignment Suggestion",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-influence",
        "name": "Resonance Influence",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "enthrall",
        "name": "Enthrall",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "ghost-sound",
        "name": "Ghost Sound",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-image",
        "name": "Minor Image",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "flickerstep",
        "name": "Flickerstep",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "silent-echo",
        "name": "Silent Echo",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirage-spark",
        "name": "Mirage Spark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "illusive-flash",
        "name": "Illusive Flash",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-puppet",
        "name": "Shadow Puppet",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blurred-visage",
        "name": "Blurred Visage",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "disguise-self-minor",
        "name": "Disguise Self (Minor)",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "distort-voice",
        "name": "Distort Voice",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-footsteps",
        "name": "Phantom Footsteps",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-mark",
        "name": "Shadow Mark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blur-vision",
        "name": "Blur Vision",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirror-image",
        "name": "Mirror Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "silent-image",
        "name": "Silent Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "color-spray",
        "name": "Color Spray",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-blade",
        "name": "Illusory Blade",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "veil-of-mist",
        "name": "Veil of Mist",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "phantom-grasp",
        "name": "Phantom Grasp",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "mask-voice",
        "name": "Mask Voice",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-footsteps",
        "name": "False Footsteps",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "disguise-self",
        "name": "Disguise Self",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-script",
        "name": "Illusory Script",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "distort-value",
        "name": "Distort Value",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "uncontrollable-laughter",
        "name": "Uncontrollable Laughter",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-terrain",
        "name": "Illusory Terrain",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mirrorsage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Paladin": {
    "featCastingAbility": "CHA",
    "rank0Choices": 64,
    "rank1Choices": 59,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "foresight-flicker",
        "name": "Foresight Flicker",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "guiding-spark",
        "name": "Guiding Spark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "omen-whisper",
        "name": "Omen Whisper",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-emotion",
        "name": "Detect Emotion",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-glimpse",
        "name": "Aura Glimpse",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "far-echo",
        "name": "Far Echo",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "predict-movement",
        "name": "Predict Movement",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "soul-mark",
        "name": "Soul Mark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-alignment",
        "name": "Sense Alignment",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimpse-future",
        "name": "Glimpse Future",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-faction",
        "name": "Detect Faction",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-sight",
        "name": "Resonance Sight",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-weather",
        "name": "Detect Weather",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-corruption",
        "name": "Sense Corruption",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "true-sight-lesser",
        "name": "True Sight (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "warning-ward",
        "name": "Warning Ward",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "scribe-destiny",
        "name": "Scribe Destiny",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "mark-omen",
        "name": "Mark Omen",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "clairaudience-lesser",
        "name": "Clairaudience (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "fate-coin",
        "name": "Fate Coin",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-secret-doors",
        "name": "Detect Secret Doors",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-insight",
        "name": "Faction Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-sense",
        "name": "Alignment Sense",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-map",
        "name": "Resonance Map",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "locate-object",
        "name": "Locate Object",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "read-memories",
        "name": "Read Memories",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-insight",
        "name": "Corruption Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "daze",
        "name": "Daze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "calm-whispers",
        "name": "Calm Whispers",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-flicker",
        "name": "Mental Flicker",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "false-comfort",
        "name": "False Comfort",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimmering-eyes",
        "name": "Glimmering Eyes",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "disrupt-memory",
        "name": "Disrupt Memory",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "enthralling-tune",
        "name": "Enthralling Tune",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-tap",
        "name": "Mental Tap",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "friends",
        "name": "Friends",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "lullaby",
        "name": "Lullaby",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "soothe-animal",
        "name": "Soothe Animal",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-sympathy",
        "name": "Faction Sympathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "alignment-empathy",
        "name": "Alignment Empathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-whisper",
        "name": "Resonance Whisper",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-suggestion",
        "name": "Minor Suggestion",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "beguiling-gaze",
        "name": "Beguiling Gaze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "mesmerize",
        "name": "Mesmerize",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "pacify",
        "name": "Pacify",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "sleep",
        "name": "Sleep",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "confusing-flash",
        "name": "Confusing Flash",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaken-will",
        "name": "Weaken Will",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "distract",
        "name": "Distract",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "voice-of-peace",
        "name": "Voice of Peace",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "command",
        "name": "Command",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "hideous-laughter",
        "name": "Hideous Laughter",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "heroism",
        "name": "Heroism",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-charm",
        "name": "Faction Charm",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-suggestion",
        "name": "Alignment Suggestion",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-influence",
        "name": "Resonance Influence",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "enthrall",
        "name": "Enthrall",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Paladin",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Ranger": {
    "featCastingAbility": "WIS",
    "rank0Choices": 48,
    "rank1Choices": 48,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "foresight-flicker",
        "name": "Foresight Flicker",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "guiding-spark",
        "name": "Guiding Spark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "omen-whisper",
        "name": "Omen Whisper",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-emotion",
        "name": "Detect Emotion",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-glimpse",
        "name": "Aura Glimpse",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "far-echo",
        "name": "Far Echo",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "predict-movement",
        "name": "Predict Movement",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "soul-mark",
        "name": "Soul Mark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-alignment",
        "name": "Sense Alignment",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimpse-future",
        "name": "Glimpse Future",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-faction",
        "name": "Detect Faction",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-sight",
        "name": "Resonance Sight",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-weather",
        "name": "Detect Weather",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-corruption",
        "name": "Sense Corruption",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "true-sight-lesser",
        "name": "True Sight (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "warning-ward",
        "name": "Warning Ward",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "scribe-destiny",
        "name": "Scribe Destiny",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "mark-omen",
        "name": "Mark Omen",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "clairaudience-lesser",
        "name": "Clairaudience (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "fate-coin",
        "name": "Fate Coin",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-secret-doors",
        "name": "Detect Secret Doors",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-insight",
        "name": "Faction Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-sense",
        "name": "Alignment Sense",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-map",
        "name": "Resonance Map",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "locate-object",
        "name": "Locate Object",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "read-memories",
        "name": "Read Memories",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-insight",
        "name": "Corruption Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Ranger",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Shaman": {
    "featCastingAbility": "WIS",
    "rank0Choices": 64,
    "rank1Choices": 64,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "foresight-flicker",
        "name": "Foresight Flicker",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "guiding-spark",
        "name": "Guiding Spark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "omen-whisper",
        "name": "Omen Whisper",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-emotion",
        "name": "Detect Emotion",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-glimpse",
        "name": "Aura Glimpse",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "far-echo",
        "name": "Far Echo",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "predict-movement",
        "name": "Predict Movement",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "soul-mark",
        "name": "Soul Mark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-alignment",
        "name": "Sense Alignment",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimpse-future",
        "name": "Glimpse Future",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-faction",
        "name": "Detect Faction",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-sight",
        "name": "Resonance Sight",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-weather",
        "name": "Detect Weather",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-corruption",
        "name": "Sense Corruption",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "true-sight-lesser",
        "name": "True Sight (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "warning-ward",
        "name": "Warning Ward",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "scribe-destiny",
        "name": "Scribe Destiny",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "mark-omen",
        "name": "Mark Omen",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "clairaudience-lesser",
        "name": "Clairaudience (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "fate-coin",
        "name": "Fate Coin",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-secret-doors",
        "name": "Detect Secret Doors",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-insight",
        "name": "Faction Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-sense",
        "name": "Alignment Sense",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-map",
        "name": "Resonance Map",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "locate-object",
        "name": "Locate Object",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "read-memories",
        "name": "Read Memories",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-insight",
        "name": "Corruption Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "grave-spark",
        "name": "Grave Spark",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "rotting-touch",
        "name": "Rotting Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "finger-of-the-dead",
        "name": "Finger of the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "corpse-light",
        "name": "Corpse Light",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-of-the-crypt",
        "name": "Chill of the Crypt",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "whispers-from-beyond",
        "name": "Whispers from Beyond",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-claw",
        "name": "Spectral Claw",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "gravewind-flicker",
        "name": "Gravewind Flicker",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "toll-the-dead",
        "name": "Toll the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "death-whisper",
        "name": "Death Whisper",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "bone-shard",
        "name": "Bone Shard",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "wither-plant",
        "name": "Wither Plant",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-undead",
        "name": "Sense Undead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "blood-trickle",
        "name": "Blood Trickle",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "decay",
        "name": "Decay",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "lifedraw",
        "name": "Lifedraw",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-lesser-skeleton",
        "name": "Summon Lesser Skeleton",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "dread-whisper",
        "name": "Dread Whisper",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "putrefy",
        "name": "Putrefy",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "pact-of-bone",
        "name": "Pact of Bone",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "soul-tap",
        "name": "Soul Tap",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "eyes-of-the-grave",
        "name": "Eyes of the Grave",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "ray-of-sickness",
        "name": "Ray of Sickness",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "inflict-wounds",
        "name": "Inflict Wounds",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "corpse-puppet",
        "name": "Corpse Puppet",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "bone-armor",
        "name": "Bone Armor",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "speak-with-dead-lesser",
        "name": "Speak with Dead (Lesser)",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Shaman",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Thief": {
    "featCastingAbility": "DEX",
    "rank0Choices": 64,
    "rank1Choices": 62,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "daze",
        "name": "Daze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "calm-whispers",
        "name": "Calm Whispers",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-flicker",
        "name": "Mental Flicker",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "false-comfort",
        "name": "False Comfort",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimmering-eyes",
        "name": "Glimmering Eyes",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "disrupt-memory",
        "name": "Disrupt Memory",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "enthralling-tune",
        "name": "Enthralling Tune",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-tap",
        "name": "Mental Tap",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "friends",
        "name": "Friends",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "lullaby",
        "name": "Lullaby",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "soothe-animal",
        "name": "Soothe Animal",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-sympathy",
        "name": "Faction Sympathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "alignment-empathy",
        "name": "Alignment Empathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-whisper",
        "name": "Resonance Whisper",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-suggestion",
        "name": "Minor Suggestion",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "beguiling-gaze",
        "name": "Beguiling Gaze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "mesmerize",
        "name": "Mesmerize",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "pacify",
        "name": "Pacify",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "sleep",
        "name": "Sleep",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "confusing-flash",
        "name": "Confusing Flash",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaken-will",
        "name": "Weaken Will",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "distract",
        "name": "Distract",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "voice-of-peace",
        "name": "Voice of Peace",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "command",
        "name": "Command",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "hideous-laughter",
        "name": "Hideous Laughter",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "heroism",
        "name": "Heroism",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-charm",
        "name": "Faction Charm",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-suggestion",
        "name": "Alignment Suggestion",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-influence",
        "name": "Resonance Influence",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "enthrall",
        "name": "Enthrall",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "ghost-sound",
        "name": "Ghost Sound",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-image",
        "name": "Minor Image",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "flickerstep",
        "name": "Flickerstep",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "silent-echo",
        "name": "Silent Echo",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirage-spark",
        "name": "Mirage Spark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "illusive-flash",
        "name": "Illusive Flash",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-puppet",
        "name": "Shadow Puppet",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blurred-visage",
        "name": "Blurred Visage",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "disguise-self-minor",
        "name": "Disguise Self (Minor)",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "distort-voice",
        "name": "Distort Voice",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-footsteps",
        "name": "Phantom Footsteps",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-mark",
        "name": "Shadow Mark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blur-vision",
        "name": "Blur Vision",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirror-image",
        "name": "Mirror Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "silent-image",
        "name": "Silent Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "color-spray",
        "name": "Color Spray",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-blade",
        "name": "Illusory Blade",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "veil-of-mist",
        "name": "Veil of Mist",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "phantom-grasp",
        "name": "Phantom Grasp",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "mask-voice",
        "name": "Mask Voice",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-footsteps",
        "name": "False Footsteps",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "disguise-self",
        "name": "Disguise Self",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-script",
        "name": "Illusory Script",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "distort-value",
        "name": "Distort Value",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "uncontrollable-laughter",
        "name": "Uncontrollable Laughter",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-terrain",
        "name": "Illusory Terrain",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "grave-spark",
        "name": "Grave Spark",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "rotting-touch",
        "name": "Rotting Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "finger-of-the-dead",
        "name": "Finger of the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "corpse-light",
        "name": "Corpse Light",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-of-the-crypt",
        "name": "Chill of the Crypt",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "whispers-from-beyond",
        "name": "Whispers from Beyond",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-claw",
        "name": "Spectral Claw",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "gravewind-flicker",
        "name": "Gravewind Flicker",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "toll-the-dead",
        "name": "Toll the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "death-whisper",
        "name": "Death Whisper",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "bone-shard",
        "name": "Bone Shard",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "wither-plant",
        "name": "Wither Plant",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-undead",
        "name": "Sense Undead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "blood-trickle",
        "name": "Blood Trickle",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "decay",
        "name": "Decay",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "lifedraw",
        "name": "Lifedraw",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-lesser-skeleton",
        "name": "Summon Lesser Skeleton",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "dread-whisper",
        "name": "Dread Whisper",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "putrefy",
        "name": "Putrefy",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "pact-of-bone",
        "name": "Pact of Bone",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "soul-tap",
        "name": "Soul Tap",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "eyes-of-the-grave",
        "name": "Eyes of the Grave",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "ray-of-sickness",
        "name": "Ray of Sickness",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "inflict-wounds",
        "name": "Inflict Wounds",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "corpse-puppet",
        "name": "Corpse Puppet",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "bone-armor",
        "name": "Bone Armor",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "speak-with-dead-lesser",
        "name": "Speak with Dead (Lesser)",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Thief",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 3,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Tinker": {
    "featCastingAbility": "INT",
    "rank0Choices": 64,
    "rank1Choices": 63,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Tinker",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 2,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Wizard": {
    "featCastingAbility": "INT",
    "rank0Choices": 140,
    "rank1Choices": 135,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dispel-minor",
        "name": "Dispel Minor",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repelling-pulse",
        "name": "Repelling Pulse",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-magic",
        "name": "Sense Magic",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-gesture",
        "name": "Warding Gesture",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "barrier-flicker",
        "name": "Barrier Flicker",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "nullify-element",
        "name": "Nullify Element",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "seal-minor-wound",
        "name": "Seal Minor Wound",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-sight",
        "name": "Aura Sight",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "fortify-object",
        "name": "Fortify Object",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-shield",
        "name": "Resonance Shield",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-corruption",
        "name": "Detect Corruption",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "harmonic-protection",
        "name": "Harmonic Protection",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "purify-drop",
        "name": "Purify Drop",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "repel-vermin",
        "name": "Repel Vermin",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "warding-mark",
        "name": "Warding Mark",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "protective-sphere",
        "name": "Protective Sphere",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm-ward",
        "name": "Alarm Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "dispel-resonance",
        "name": "Dispel Resonance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-resistance",
        "name": "Elemental Resistance",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "sanctuary",
        "name": "Sanctuary",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "binding-circle",
        "name": "Binding Circle",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "armor-of-faith",
        "name": "Armor of Faith",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "purify-food-and-drink",
        "name": "Purify Food and Drink",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-poison",
        "name": "Detect Poison",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "repulsion-field",
        "name": "Repulsion Field",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "warding-bond",
        "name": "Warding Bond",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-shield",
        "name": "Alignment Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-ward",
        "name": "Corruption Ward",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-lock",
        "name": "Resonance Lock",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-seal",
        "name": "Faction Seal",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-spark",
        "name": "Flare Spark",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "dust-gust",
        "name": "Dust Gust",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "crackle-jolt",
        "name": "Crackle Jolt",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "lodestone-pull",
        "name": "Lodestone Pull",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-elemental-ward",
        "name": "Minor Elemental Ward",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-flame",
        "name": "Flicker Flame",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-skin-sliver",
        "name": "Stone Skin Sliver",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-kindle",
        "name": "Resonance Kindle",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "conjure-water",
        "name": "Conjure Water",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "pebble-swarm",
        "name": "Pebble Swarm",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-tool",
        "name": "Summon Tool",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "elemental-touch",
        "name": "Elemental Touch",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "mist-veil",
        "name": "Mist Veil",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-key",
        "name": "Phantom Key",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-mote",
        "name": "Resonance Mote",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-emblem",
        "name": "Faction Emblem",
        "rank": 0,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "summon-fire-pet",
        "name": "Summon Fire Pet",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "shockwave",
        "name": "Shockwave",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "earthen-grip",
        "name": "Earthen Grip",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-mod-rod",
        "name": "Summon Mod Rod",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-minor-weapon",
        "name": "Summon Minor Weapon",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "heat-metal-conjured",
        "name": "Heat Metal (Conjured)",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "conjure-rope",
        "name": "Conjure Rope",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-familiar",
        "name": "Summon Familiar",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "mist-step",
        "name": "Mist Step",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-bridge",
        "name": "Resonance Bridge",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-messenger",
        "name": "Faction Messenger",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-essence",
        "name": "Alignment Essence",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-sensor",
        "name": "Corruption Sensor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "foresight-flicker",
        "name": "Foresight Flicker",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "guiding-spark",
        "name": "Guiding Spark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "omen-whisper",
        "name": "Omen Whisper",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-emotion",
        "name": "Detect Emotion",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "aura-glimpse",
        "name": "Aura Glimpse",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "far-echo",
        "name": "Far Echo",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "predict-movement",
        "name": "Predict Movement",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "soul-mark",
        "name": "Soul Mark",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-alignment",
        "name": "Sense Alignment",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimpse-future",
        "name": "Glimpse Future",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-faction",
        "name": "Detect Faction",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-sight",
        "name": "Resonance Sight",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "detect-weather",
        "name": "Detect Weather",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-corruption",
        "name": "Sense Corruption",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "identify",
        "name": "Identify",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-magic",
        "name": "Detect Magic",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "true-sight-lesser",
        "name": "True Sight (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "warning-ward",
        "name": "Warning Ward",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "scribe-destiny",
        "name": "Scribe Destiny",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "mark-omen",
        "name": "Mark Omen",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "clairaudience-lesser",
        "name": "Clairaudience (Lesser)",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "fate-coin",
        "name": "Fate Coin",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "comprehend-languages",
        "name": "Comprehend Languages",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "detect-secret-doors",
        "name": "Detect Secret Doors",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-insight",
        "name": "Faction Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-sense",
        "name": "Alignment Sense",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-map",
        "name": "Resonance Map",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "locate-object",
        "name": "Locate Object",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "read-memories",
        "name": "Read Memories",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "corruption-insight",
        "name": "Corruption Insight",
        "rank": 1,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 2
        }
      },
      {
        "id": "daze",
        "name": "Daze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "calm-whispers",
        "name": "Calm Whispers",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-flicker",
        "name": "Mental Flicker",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "false-comfort",
        "name": "False Comfort",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "glimmering-eyes",
        "name": "Glimmering Eyes",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "disrupt-memory",
        "name": "Disrupt Memory",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "enthralling-tune",
        "name": "Enthralling Tune",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "mental-tap",
        "name": "Mental Tap",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "friends",
        "name": "Friends",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "lullaby",
        "name": "Lullaby",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "soothe-animal",
        "name": "Soothe Animal",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "faction-sympathy",
        "name": "Faction Sympathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "alignment-empathy",
        "name": "Alignment Empathy",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "resonance-whisper",
        "name": "Resonance Whisper",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-suggestion",
        "name": "Minor Suggestion",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "beguiling-gaze",
        "name": "Beguiling Gaze",
        "rank": 0,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 0
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "mesmerize",
        "name": "Mesmerize",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "pacify",
        "name": "Pacify",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "sleep",
        "name": "Sleep",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "confusing-flash",
        "name": "Confusing Flash",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaken-will",
        "name": "Weaken Will",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "distract",
        "name": "Distract",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "voice-of-peace",
        "name": "Voice of Peace",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "command",
        "name": "Command",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "hideous-laughter",
        "name": "Hideous Laughter",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "heroism",
        "name": "Heroism",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "faction-charm",
        "name": "Faction Charm",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "alignment-suggestion",
        "name": "Alignment Suggestion",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-influence",
        "name": "Resonance Influence",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "bane",
        "name": "Bane",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "enthrall",
        "name": "Enthrall",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-ray",
        "name": "Arcane Ray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sparkbolt",
        "name": "Sparkbolt",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "freezing-touch",
        "name": "Freezing Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flame-lash",
        "name": "Flame Lash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "soundburst",
        "name": "Soundburst",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-combustion",
        "name": "Minor Combustion",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "force-needle",
        "name": "Force Needle",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-echo",
        "name": "Arcane Echo",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shocking-grasp",
        "name": "Shocking Grasp",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "ray-of-frost",
        "name": "Ray of Frost",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "dancing-lights",
        "name": "Dancing Lights",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "acid-splash",
        "name": "Acid Splash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "sacred-flame",
        "name": "Sacred Flame",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thunderclap",
        "name": "Thunderclap",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "poison-spray",
        "name": "Poison Spray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fireburst",
        "name": "Fireburst",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "frost-arrow",
        "name": "Frost Arrow",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chain-jolt",
        "name": "Chain Jolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "force-spike",
        "name": "Force Spike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-missile-storm",
        "name": "Magic Missile Storm",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunder-clap",
        "name": "Thunder Clap",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-shield-shatter",
        "name": "Arcane Shield Shatter",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ignition-bolt",
        "name": "Ignition Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-hands",
        "name": "Burning Hands",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "chromatic-orb",
        "name": "Chromatic Orb",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "earth-tremor",
        "name": "Earth Tremor",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "hellish-rebuke",
        "name": "Hellish Rebuke",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ice-knife",
        "name": "Ice Knife",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "thunderwave",
        "name": "Thunderwave",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "witch-bolt",
        "name": "Witch Bolt",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "zephyr-strike",
        "name": "Zephyr Strike",
        "rank": 1,
        "school": "Evocation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 2
        }
      },
      {
        "id": "ghost-sound",
        "name": "Ghost Sound",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-image",
        "name": "Minor Image",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "flickerstep",
        "name": "Flickerstep",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "silent-echo",
        "name": "Silent Echo",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirage-spark",
        "name": "Mirage Spark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "illusive-flash",
        "name": "Illusive Flash",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-puppet",
        "name": "Shadow Puppet",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blurred-visage",
        "name": "Blurred Visage",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "disguise-self-minor",
        "name": "Disguise Self (Minor)",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "distort-voice",
        "name": "Distort Voice",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "phantom-footsteps",
        "name": "Phantom Footsteps",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "shadow-mark",
        "name": "Shadow Mark",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "blur-vision",
        "name": "Blur Vision",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "mirror-image",
        "name": "Mirror Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "silent-image",
        "name": "Silent Image",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "color-spray",
        "name": "Color Spray",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-blade",
        "name": "Illusory Blade",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "veil-of-mist",
        "name": "Veil of Mist",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "phantom-grasp",
        "name": "Phantom Grasp",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "mask-voice",
        "name": "Mask Voice",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-footsteps",
        "name": "False Footsteps",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "disguise-self",
        "name": "Disguise Self",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-script",
        "name": "Illusory Script",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "distort-value",
        "name": "Distort Value",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "uncontrollable-laughter",
        "name": "Uncontrollable Laughter",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "illusory-terrain",
        "name": "Illusory Terrain",
        "rank": 1,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 2
        }
      },
      {
        "id": "grave-spark",
        "name": "Grave Spark",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "rotting-touch",
        "name": "Rotting Touch",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "finger-of-the-dead",
        "name": "Finger of the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "corpse-light",
        "name": "Corpse Light",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "chill-of-the-crypt",
        "name": "Chill of the Crypt",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "whispers-from-beyond",
        "name": "Whispers from Beyond",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-claw",
        "name": "Spectral Claw",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "gravewind-flicker",
        "name": "Gravewind Flicker",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "toll-the-dead",
        "name": "Toll the Dead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "spare-the-dying",
        "name": "Spare the Dying",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "death-whisper",
        "name": "Death Whisper",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "bone-shard",
        "name": "Bone Shard",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "wither-plant",
        "name": "Wither Plant",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "sense-undead",
        "name": "Sense Undead",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "blood-trickle",
        "name": "Blood Trickle",
        "rank": 0,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 0
        }
      },
      {
        "id": "decay",
        "name": "Decay",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "lifedraw",
        "name": "Lifedraw",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "summon-lesser-skeleton",
        "name": "Summon Lesser Skeleton",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "dread-whisper",
        "name": "Dread Whisper",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "putrefy",
        "name": "Putrefy",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "pact-of-bone",
        "name": "Pact of Bone",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "soul-tap",
        "name": "Soul Tap",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "eyes-of-the-grave",
        "name": "Eyes of the Grave",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "ray-of-sickness",
        "name": "Ray of Sickness",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "inflict-wounds",
        "name": "Inflict Wounds",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "corpse-puppet",
        "name": "Corpse Puppet",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "bone-armor",
        "name": "Bone Armor",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "speak-with-dead-lesser",
        "name": "Speak with Dead (Lesser)",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "magehand",
        "name": "Magehand",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shimmerstep",
        "name": "Shimmerstep",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "stone-touch",
        "name": "Stone Touch",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-matter",
        "name": "Mold Matter",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-enhancement",
        "name": "Minor Enhancement",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "fleeting-flight",
        "name": "Fleeting Flight",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "snap-freeze",
        "name": "Snap Freeze",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "flicker-skin",
        "name": "Flicker Skin",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mending",
        "name": "Mending",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "druidcraft",
        "name": "Druidcraft",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "primal-savagery",
        "name": "Primal Savagery",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shape-water",
        "name": "Shape Water",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "mold-earth",
        "name": "Mold Earth",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "control-flames",
        "name": "Control Flames",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "gust",
        "name": "Gust",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "thaumaturgy",
        "name": "Thaumaturgy",
        "rank": 0,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 0
        }
      },
      {
        "id": "featherstep",
        "name": "Featherstep",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "stoneflesh",
        "name": "Stoneflesh",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "weaponbend",
        "name": "Weaponbend",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "spider-climb",
        "name": "Spider Climb",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "feral-might",
        "name": "Feral Might",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "steel-skin",
        "name": "Steel Skin",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "magnetic-grip",
        "name": "Magnetic Grip",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "unravel-threads",
        "name": "Unravel Threads",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "expeditious-retreat",
        "name": "Expeditious Retreat",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "jump",
        "name": "Jump",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "longstrider",
        "name": "Longstrider",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "absorb-elements",
        "name": "Absorb Elements",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "catapult",
        "name": "Catapult",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "enlarge-reduce",
        "name": "Enlarge/Reduce",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "grease",
        "name": "Grease",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "alter-fluid",
        "name": "Alter Fluid",
        "rank": 1,
        "school": "Transmutation",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Transmutation",
          "baseRpCost": 2
        }
      },
      {
        "id": "mage-light",
        "name": "Mage Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-tether",
        "name": "Arcane Tether",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "glyph-trace",
        "name": "Glyph Trace",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "momentary-pause",
        "name": "Momentary Pause",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spectral-quill",
        "name": "Spectral Quill",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cantrip-echo",
        "name": "Cantrip Echo",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "guidance",
        "name": "Guidance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "light",
        "name": "Light",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "message",
        "name": "Message",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "resistance",
        "name": "Resistance",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "true-strike",
        "name": "True Strike",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-mark",
        "name": "Arcane Mark",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "spellshift",
        "name": "Spellshift",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "ritual-anchor",
        "name": "Ritual Anchor",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "resonance-tether",
        "name": "Resonance Tether",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "delay-spell",
        "name": "Delay Spell",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "flare-sigil",
        "name": "Flare Sigil",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "quick-cast",
        "name": "Quick Cast",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "alarm",
        "name": "Alarm",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Sorcerer": {
    "featCastingAbility": "CHA",
    "rank0Choices": 6,
    "rank1Choices": 6,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "sparkbolt",
        "name": "Sparkbolt",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "ray-of-frost",
        "name": "Ray of Frost",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "shocking-grasp",
        "name": "Shocking Grasp",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "acid-splash",
        "name": "Acid Splash",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "prestidigitation",
        "name": "Prestidigitation",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-ward",
        "name": "Arcane Ward",
        "rank": 0,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 0
        }
      },
      {
        "id": "shield",
        "name": "Shield",
        "rank": 1,
        "school": "Abjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Abjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "elemental-bolt",
        "name": "Elemental Bolt",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "burning-sands",
        "name": "Burning Sands",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "flame-armor",
        "name": "Flame Armor",
        "rank": 1,
        "school": "Conjuration",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Conjuration",
          "baseRpCost": 2
        }
      },
      {
        "id": "feather-fall",
        "name": "Feather Fall",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "magic-thread",
        "name": "Magic Thread",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  },
  "Warlock": {
    "featCastingAbility": "CHA",
    "rank0Choices": 6,
    "rank1Choices": 6,
    "selection": "Permanently choose two distinct rank0 spells and one rank1 spell at acquisition. Current unreviewed payloads remain unavailable pending their own exact approval.",
    "ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax": true,
    "choices": [
      {
        "id": "chill-touch",
        "name": "Chill Touch",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "minor-illusion",
        "name": "Minor Illusion",
        "rank": 0,
        "school": "Illusion",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Illusion",
          "baseRpCost": 0
        }
      },
      {
        "id": "arcane-ray",
        "name": "Arcane Ray",
        "rank": 0,
        "school": "Evocation",
        "sourceClass": "Mage",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Evocation",
          "baseRpCost": 0
        }
      },
      {
        "id": "read-surface-thoughts",
        "name": "Read Surface Thoughts",
        "rank": 0,
        "school": "Divination",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      {
        "id": "magical-ping",
        "name": "Magical Ping",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "mage-hand",
        "name": "Mage Hand",
        "rank": 0,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 0
        }
      },
      {
        "id": "cause-fear",
        "name": "Cause Fear",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "false-life",
        "name": "False Life",
        "rank": 1,
        "school": "Necromancy",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Necromancy",
          "baseRpCost": 2
        }
      },
      {
        "id": "charm-person",
        "name": "Charm Person",
        "rank": 1,
        "school": "Enchantment",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Enchantment",
          "baseRpCost": 2
        }
      },
      {
        "id": "find-familiar",
        "name": "Find Familiar",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "unseen-servant",
        "name": "Unseen Servant",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      },
      {
        "id": "arcane-lock",
        "name": "Arcane Lock",
        "rank": 1,
        "school": "Universal",
        "sourceClass": "Wizard",
        "fullOriginalClassAccessRow": {
          "rank": 1,
          "minimumClassLevel": 1,
          "school": "Universal",
          "baseRpCost": 2
        }
      }
    ]
  }
}
```

## SUP-05 — Magic Core

```json
{
  "newSpellFocus": {
    "id": "proposal_spell_focus",
    "name": "Spell Focus",
    "sourceRegistryEntry": false,
    "prerequisite": "Actual personal spellcasting ability",
    "effect": "Choose one actual school through which you can cast an acquired spell. Your personally cast spells through that school gain+1to their actual saving-throw DC. Record the school permanently. No bonus to spell attacks, nonspell techniques, fixed independent itemDCs or saves you make. Not repeatable. The source spell’s actual DC snapshot controls later saves. Greater Spell Focus’s separately acquired+1can add within this same chosen scope.",
    "castingPrerequisitePolicyRef": "FEAT327-ACQ-03"
  },
  "newLegacyInitiateCurricula": {
    "Sorcerer": {
      "ability": "CHA",
      "notice": "NEW feat-only curriculum; no Sorcerer class or Mage alias is created.",
      "cantrips": [
        [
          "sparkbolt",
          "Mage"
        ],
        [
          "ray-of-frost",
          "Mage"
        ],
        [
          "shocking-grasp",
          "Mage"
        ],
        [
          "acid-splash",
          "Mage"
        ],
        [
          "prestidigitation",
          "Mage"
        ],
        [
          "arcane-ward",
          "Mage"
        ]
      ],
      "rank1": [
        [
          "shield",
          "Mage"
        ],
        [
          "elemental-bolt",
          "Mage"
        ],
        [
          "burning-sands",
          "Mage"
        ],
        [
          "flame-armor",
          "Mage"
        ],
        [
          "feather-fall",
          "Mage"
        ],
        [
          "magic-thread",
          "Mage"
        ]
      ]
    },
    "Warlock": {
      "ability": "CHA",
      "notice": "NEW feat-only curriculum; no Warlock class, patron doctrine or Wizard alias is created.",
      "cantrips": [
        [
          "chill-touch",
          "Mage"
        ],
        [
          "minor-illusion",
          "Wizard"
        ],
        [
          "arcane-ray",
          "Mage"
        ],
        [
          "read-surface-thoughts",
          "Wizard"
        ],
        [
          "magical-ping",
          "Wizard"
        ],
        [
          "mage-hand",
          "Wizard"
        ]
      ],
      "rank1": [
        [
          "cause-fear",
          "Wizard"
        ],
        [
          "false-life",
          "Wizard"
        ],
        [
          "charm-person",
          "Wizard"
        ],
        [
          "find-familiar",
          "Wizard"
        ],
        [
          "unseen-servant",
          "Wizard"
        ],
        [
          "arcane-lock",
          "Wizard"
        ]
      ]
    }
  },
  "newRitualTagOverlay": {
    "ids": [
      "detect-magic",
      "identify",
      "comprehend-languages",
      "alarm",
      "unseen-servant",
      "find-familiar",
      "illusory-script"
    ],
    "placement": "Exact existing Wizard rank1school/mode for each named identity"
  },
  "newDetectThoughts": {
    "id": "proposal_feat_detect_thoughts",
    "rank": 2,
    "school": "Divination",
    "completeProcedureInFeat": "telepathic",
    "ordinaryClassAccess": {},
    "explicitComparisonOnly": "read-surface-thoughts is distinct, retained and not renamed"
  }
}
```

## SUP-06 — Magic Core

```json
[
  {
    "id": "detect-magic",
    "name": "Detect Magic",
    "rank": 1,
    "school": "Divination",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    }
  },
  {
    "id": "identify",
    "name": "Identify",
    "rank": 1,
    "school": "Divination",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    }
  },
  {
    "id": "comprehend-languages",
    "name": "Comprehend Languages",
    "rank": 1,
    "school": "Divination",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    }
  },
  {
    "id": "alarm",
    "name": "Alarm",
    "rank": 1,
    "school": "Universal",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Universal",
      "baseRpCost": 2
    }
  },
  {
    "id": "unseen-servant",
    "name": "Unseen Servant",
    "rank": 1,
    "school": "Universal",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Universal",
      "baseRpCost": 2
    }
  },
  {
    "id": "find-familiar",
    "name": "Find Familiar",
    "rank": 1,
    "school": "Universal",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Universal",
      "baseRpCost": 2
    }
  },
  {
    "id": "illusory-script",
    "name": "Illusory Script",
    "rank": 1,
    "school": "Illusion",
    "sourceClass": "Wizard",
    "fullOriginalClassAccessRow": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Illusion",
      "baseRpCost": 2
    }
  }
]
```

## SUP-07 — Magic Extended

```json
{
  "copyProfileContract": {
    "capture": "Capture only one directly witnessed resolved component that actually expresses one profile below. Record canonical source/event, actual original spell rank or pre-encounter monster effective rank, native magnitude before external bonuses/defenses, selected type/profile and qualifying own casting route. For monster abilities without a spell rank, use max(1, min(9, ceil(actualCR/2))); missing CR needs a rating assigned before the encounter, never a favorable after-the-fact guess. No unique/legendary/boss feature without an independently reviewed exception; no copying copies, class engines, actions, resources, permanent changes, resurrection, creation, items or protected information. An unsupported role is ineligible, not a blank Director permission.",
    "rankAndPayment": "For original rank 0, q=0; otherwise q=max(1, floor(originalRank/2)). The chosen actual owned spellcasting route must independently support learning q; merely owning a pool or feat prerequisite does not. Use that route’s real ability for attack/DC and spell components V/S, normal rank price 0/2/3/5/7/10/13/17/21/26 plus actual adjustments. It grants a temporary feat-copy route only, never the original full spell. Spellcasting time is oneAction. At release pay/cast/history/interrupt once, with copy-provenance flags disabling copy/resource/class-proc chains. An explicit source such as Mirrorsage retains its own actual profile/rank/payment instead of being silently converted. FINAL FS-08: these releases are paid feat-copy casts with actual RP/components/history, not ordinary knowledge grants. Boon uses one feat-copy-boon family; its repeated copies do not add, while genuinely distinct eligible ordinary feat bonuses use FS-03.",
    "numericBound": "For numeric damage/heal/ward select one witnessed native component/type and record its rolled or fixed magnitude B before external bonuses, saves, defenses and recipient caps. If that magnitude was hidden, the Director records it privately; no free identification is given. At feat-copy release roll (q+1)d6, then bound the native numeric result to min(roll, floor(B/2)). No copied critical multiplier, external damage/heal modifier, converted excess or extra recipients. Actual recipient defenses and healing limits still apply. A zero ceiling cannot produce a numeric benefit. This is an explicit NEW meaning of half potency, not an assertion about original undefined wording.",
    "lifecycle": "At most one feat-copy release per owner per numbered round across Eldritch Echo, Mimicry and adapted copies. A Mirrorsage owner also spends its existing shared release allowance; an unowned Mirrorsage engine is not granted. Strike/Burst/Mend are immediate. Ward/Hindrance/Boon/Step use their stated maximum two-interval duration; source-specific shorter hold deadlines still govern. Only one pending feat-copy record across Eldritch Echo/Mimicry; before a new capture choose whether to replace the old, losing its paid capture/use without refund. Adaptation may retain permission but creates no second release allowance. No copied effect grants extra Action/BA/Reaction, persistent body, loot, learning or concentration capacity.",
    "profiles": [
      {
        "id": "strike",
        "role": "Direct single-target damage",
        "activation": "Action",
        "range": "60 ft, one perceived creature with line of effect",
        "resolution": "Actual own casting ability+PB spell attack; on hit bounded numeric damage of one observed native type. No added critical dice. No original riders. Instant."
      },
      {
        "id": "burst",
        "role": "Area damage",
        "activation": "Action",
        "range": "Point within 30 ft;10 ft radius, at most 3 originally declared perceived creatures in area with line of effect",
        "resolution": "DEX save vs own DC for bounded numeric observed-type damage, half on success; one shared roll. No original riders. Instant."
      },
      {
        "id": "mend",
        "role": "Actual normal HP healing",
        "activation": "Action",
        "range": "30 ft one perceived willing living creature with line of effect",
        "resolution": "Restore bounded numeric HP under actual prohibitions/maximum/Critical caps. No reviving, healing dice add-ons, Wound cure, heal-copy/resource trigger or excess conversion. Instant."
      },
      {
        "id": "ward",
        "role": "Temporary HP",
        "activation": "Action",
        "range": "30 ft one perceived willing living creature with line of effect",
        "resolution": "Offer bounded numerictemp HP into the actual single grant ledger, ending at the source’s second future regular start. Rejected offer wastes the copy. No linked riders."
      },
      {
        "id": "hindrance",
        "role": "Actual slow or action/reaction control",
        "activation": "Action",
        "range": "30 ft one perceived creature with line of effect",
        "resolution": "WIS save vs own DC or Speed−10 ft and no new Reactions until its next future regular end, never later than the source’s second future regular start. Strongest slow arbitration; no wholeAction/turn denial, repeated save or original hard-control rider."
      },
      {
        "id": "boon",
        "role": "A source actually granting a positive attack, save or AC modifier",
        "activation": "Action",
        "range": "30 ft one perceived willing creature with line of effect",
        "resolution": "Choose one statistic actually benefited by the witnessed source: +1 AC OR+1 to one next actual attack roll OR+1 to one next actual save, through source’s next future regular end. Strongest feat-copy-boon-family arbitration; no new roll or cloned concentration."
      },
      {
        "id": "step",
        "role": "Actual short personal movement/teleport",
        "activation": "Action",
        "range": "Self to visible unoccupied fitting space within min(15 ft, floor(observed distance/2))",
        "resolution": "If original component was teleport, teleport with actual line of effect and ordinary teleport restrictions; otherwise move that distance over an actual legal path paying terrain and provoking normally. No passenger, planar travel, new locomotion mode or movement into an unseen space. Instant."
      }
    ]
  },
  "eldritchBlast": {
    "id": "feat-supplement.eldritch-blast",
    "name": "Eldritch Blast",
    "rank": 0,
    "castingAbility": "CHA; both feat grants share this one source ability/identity, not two selectable histories.",
    "castingTime": "Action",
    "components": [
      "V",
      "S"
    ],
    "rangeFeet": 60,
    "effect": "Make one spell attack for 1d10 force. Explicit total-character-level scaling supplies 2 beams at 5,3 at 11,4 at 17; declare each target before its attack, each must be perceived within 60 ft/line of effect. Different legal recipients allowed; each beam is a separate hit/damage event. Ordinary critical doubles that beam’s die only. No CHA damage modifier, pushing or automatic extra effect. Normal cantrip RP 0, actual independent costs, Dissonance/Refrain and interruption apply once for the cast, not once per beam. No generic ordinary catalog access or Warlock class is inferred.",
    "grant": "Forbidden Pact or Eldritch Echo supplies one actual cantrip spellcasting route. Duplicate grant creates no duplicate spell, price waiver, resource pool, known-spell count or separate Refrain."
  },
  "pactSigils": [
    {
      "id": "shadowstep",
      "effect": "Once SR/LR use BA to teleport up to 15 ft from actualdim/dark occupiedspace to a visible fitting unoccupieddim/dark destination withlineofeffect. Whole footprints qualify. This use is a separate exact sigil source, not free Dark Affinity acquisition; ordinary teleport prohibitions remain."
    },
    {
      "id": "hex",
      "effect": "Once SR/LR use BA to mark one perceived hostile within 30 ft/lineofeffect until your next future regular start. Your next personal direct weapon hit against it before expiry adds 1d4 necrotic, then ends the mark; critical doubles the die. No curse classification, drop reward, ongoing damage or Curse Channeling grant."
    },
    {
      "id": "energyResistance",
      "effect": "At acquisition choose one permanent damage resistance: acid, cold, fire, lightning or thunder. It never stacks with another resistance to the same type. No immunity, absorption, charge generation or creature/plane affiliation."
    }
  ],
  "floraBody": {
    "size": "Tiny, occupies a supported 5 ft square as a low plant; does not block traversal or grant cover; zeroSpeed and no voluntary movement. Can be carried only as an ordinary object-body interaction; lifting/uprooting ends it immediately without harvest.",
    "statistics": "Plant creature; no assumed language, mind immunity or world-origin claim. AC 12, HP 5+owner PB snapshotted at creation; saves +owner PB, other checks +0. No damage/condition immunities or special senses unless an actual source grants them. It perceives commands within 60 ft through ordinary sight/hearing; Silence matters for spoken commands. It has no independent initiative, Action, Bonus Action or Reaction, and no attack outside the commanded profiles or the final expressly bounded Trapcasting exception. Zero HP permanently destroys it instead of creating a dying body. No corpse, reward, harvest, resource/soul collection, loot or Supply credit. Ordinary legal damage and healing may affect the actual creature but cannot recreate a destroyed plant, refill its creation entitlement or extend its deadline.",
    "dc": "At acquisition select one actual possessed spellcasting route; use DC 8+current PB+that route’s current ability modifier. No phantom Wisdom/Spellcraft statistic. Actual source-specific component/target defenses still apply.",
    "cadence": "Action creates;1/SR or LR, capacity 1 or 2 at 10. NEW level 10 completion: after the first creation, one additionalAction before that first seedling expires may create the second without a second rest use. This one extra creation entitlement is bound to that original committed use and is consumed once; if missed/lost it is not banked. Each plant has its own original minute deadline. No replacement/revival can restore the entitlement. Any command, trap orBurst with a hostile result uses the owner’s one shared offensive-companion allowance per numbered round; one selected mode outcome for the coordinated group. Ordinary command: owner shared Bonus Action, actual perceptible60ft channel, attached phase after owner regular turn. One action outcome and one offensive allowance per owner/numbered round; Trapcasting spends that same allowance at its exact entry/burst event. No independent turn is added.",
    "endpoints": "Poisoned/Restrained records also end if the generating plant ends; no concentration is required. Reapplying same profile follows ordinary nonstacking rules. Burst consumes one body before resolving a 10 ft-radius area, all creaturesDEXsave,2d6 selectedtype half on success. Chosenmode/type doesnotchange aftercreation. No destroyed body can command or trap during the resolving event.",
    "commandChoice": "Every seedling may use the printed Lash command. Its selected creation mode additionally determines its Spore or Entangle option and its Trapcasting result/burst type; selecting Lash leaves that basic profile. A coordinated command chooses only one permitted outcome from one actual participating plant. Other plants extend the legal Lash origin as printed but never multiply damage, control areas or offense allowances.",
    "modes": [
      {
        "id": "lash",
        "command": "One creature within 10 ft of any commandedplant makesDEXsave;1d6 piercing, half on success. One shared attack outcome, not a die perplant.",
        "trap": "Entering creatureDEXsave;failure 1d6 piercing, success 0.",
        "burstType": "piercing"
      },
      {
        "id": "spore",
        "command": "One creature within 10 ft of any commandedplant makesCONsave orPoisoned until its next future regular end. No damage; actual poison/Poisoned immunities apply.",
        "trap": "Entering creatureDEXsave;failurePoisoned until its next future regular end, successnone.",
        "burstType": "poison"
      },
      {
        "id": "entangle",
        "command": "Choose one 10 ft square within 10 ft of a commandedplant, withsupportedground/lineofeffect. Each creature in it makesSTRsave orRestrained until its next future regular end. On its turn an affected creature may spendAction for STR(Athletics) or DEX(Acrobatics) vsflora DC to end its ownrecord. No damaginggrowth or freewall.",
        "trap": "Entering creatureDEXsave;failureRestrained until its next future regular end with sameActionescape, successnone.",
        "burstType": "piercing"
      }
    ]
  },
  "minorBuffTransfer": {
    "guidance": "One 1d4 actual task/ability check of next spell.",
    "resistance": "One 1d4 actual concentration save maintaining next spell.",
    "true-strike": "Advantage on first actual spell attack of next spell.",
    "finalClarification": "The three selected current payloads are non-concentration. Holding adds no concentration; preserve original deadline, payment and one held identity. Use the full final Spellweave procedure."
  },
  "timeTagOverlay": {
    "spellIds": [
      "slow",
      "haste",
      "future-echo"
    ],
    "condition": "Only an actual failed save can trigger Temporal Flux; existing save-less payloads gain no save."
  },
  "naturePredicate": {
    "castingClassRoutes": [
      "Druid",
      "Ranger",
      "Shaman"
    ],
    "exclusions": "Copied/borrowed profile aliases; actual independent route access/rank/school still required."
  }
}
```

## SUP-08 — Heritage Mutation

```json
[
  {
    "die": 1,
    "id": "heritage-gadget.shaded-lamp",
    "name": "Shaded lamp",
    "procedure": "Action light or extinguish the integral enclosed wick. While lit it gives bright light10ft and dim light another10ft for the remaining gadget lifetime. No fuel inventory, attack, ignition of other objects, magical darkness penetration or restored illumination item is created."
  },
  {
    "die": 2,
    "id": "heritage-gadget.line-bell",
    "name": "Line bell",
    "procedure": "Action fix the gadget and its attached5ft non-load-bearing thread across one reachable ground passage. An actual body crossing and physically touching the taut thread rings an ordinary bell audible30ft, then the thread releases and the device becomes inert. It neither detects incorporeal/noncontact passage nor reveals identity/location beyond its physical site, restrains, trips or causes damage. A visible thread can be noticed by ordinary senses; it has no automatic hidden DC."
  },
  {
    "die": 3,
    "id": "heritage-gadget.light-clamp",
    "name": "Light clamp",
    "procedure": "Action attach/remove the clamp to a reachable mundane edge no more than2inches thick. It can hold one unattended or willingly presented object of at most5lb against that edge, falling normally on expiry/destruction. It cannot restrain a creature, secure a door against forced entry, support a climber, substitute for restraints or improve a check. No free hand is created."
  },
  {
    "die": 4,
    "id": "heritage-gadget.hand-fan",
    "name": "Hand fan",
    "procedure": "Action crank while held to move ordinary air through a5ft cone until the start of your next regular turn; sustained use needs anotherAction. It can cool a touched/hands-reach surface for comfort and stir loose paper/dust, without mechanical damage, creature movement, suffocation relief, weather/hazard immunity or removal of a rules-defined gas/cloud. It can visibly show ordinary airflow but identifies no substance."
  }
]
```

## SUP-09 — Heritage Mutation

```json
[
  {
    "sourceId": "soldier.base.covering-fire",
    "name": "Covering Fire",
    "actualSourceClass": "Soldier",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "Action; own actual ranged weapon/ammunition and normal attack/damage. On hit one−2 next attack against an ally other than you, until your next regular start. One attack only; no Soldier engine."
  },
  {
    "sourceId": "soldier.base.tactical-reposition",
    "name": "Tactical Reposition",
    "actualSourceClass": "Soldier",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "BA; move half current usableSpeed as a separate movement-cost budget, normal terrain/route/endpoint restrictions, no opportunity attacks; no teleport or escape from actual restraints."
  },
  {
    "sourceId": "warrior.base.brutal-strike",
    "name": "Brutal Strike",
    "actualSourceClass": "Warrior",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "Action; one own actual meleeweapon attack, hit adds1d6 native weapon type (NEW fixedS1 for borrowing, doubled on critical). TargetCONsaveDC8+yourPB+actualattackability; fail Staggered−1attacks and−5Speed through next future target regular end. No mutation/BT grant."
  },
  {
    "sourceId": "ranger.base.quick-shot",
    "name": "Quick Shot",
    "actualSourceClass": "Ranger",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "BA; one own legal bowattack using normal attack ability/proficiency, weapon die only without any ability damage modifier. Spend one borrowed entitlement, never donor use. No ExtraAttack, QuickShot loop or HitChain generation from borrowing."
  },
  {
    "sourceId": "ranger.base.twin-strike",
    "name": "Twin Strike",
    "actualSourceClass": "Ranger",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "Action; two actually wieldedLightmeleeweapons, one attack with each against one/two legaltargets. Add actual ability damage only to first successful hit. Two are the wholeAction; no ordinaryExtraAttack or borrowedHitChain."
  },
  {
    "sourceId": "ranger.base.nature-s-whisper",
    "name": "Nature's Whisper",
    "actualSourceClass": "Ranger",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "Action and1actualpersonalRP; for1minute gain advantage on one actualPerception/Survival check to find tracks/hidden natural creatures/signs of passage in natural terrain within15ft. Success reveals real evidence only. No free check, location through totalcover or borrowedclassengine; apply actual minorWeave/sharedcasting restrictions of the source."
  },
  {
    "sourceId": "ranger.base.skirmisher-s-step",
    "name": "Skirmisher's Step",
    "actualSourceClass": "Ranger",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "BA; half current usableSpeed as separate movement-cost budget, no opportunity attacks, ordinary terrain/legalroute/endpoint and actual restraint restrictions; ordinary movement is not refunded."
  },
  {
    "sourceId": "thief.base.cunning-movement",
    "name": "Cunning Movement",
    "actualSourceClass": "Thief",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "BA; half current usableSpeed separate movement-cost budget, no opportunity attacks, may cross hostile occupiedspace but never end there; ordinary terrain/cost, no impassable route or escape from restraints."
  },
  {
    "sourceId": "thief.base.disable-device",
    "name": "Disable Device",
    "actualSourceClass": "Thief",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "Action with actual usablethieves tools; one accessible nonmagical mechanism in reach,DEX+ownPB vsactualdisarmDC, otherwise15ordinary/20complex. Apply taskdegrees/naturalshifts; success disarms one mechanism, numericfailuremargin5triggersit as source. No magicdispel or blanket toolproficiency."
  },
  {
    "sourceId": "thief.base.feint",
    "name": "Feint",
    "actualSourceClass": "Thief",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "BA; one perceivedenemy within10ft able to perceiveyou,chooseCHAorDEX+ownPB vsitsactualpassiveInsight. Ordinarytaskresolution; successadvantage on yournextweaponattackagainst it thisactualturn, no automaticcritical/mindcontrol."
  },
  {
    "sourceId": "thief.base.shadow-step",
    "name": "Shadow Step",
    "actualSourceClass": "Thief",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "BA; begin in actualcover/concealment,movehalfcurrentSpeed with ordinarycost/route, then one actualHidecheck only ifdestinationqualifies. No deliberatefootfallnoise fromthismove; ordinaryOA stillapply. No teleport, invisibility or removal of other tracking evidence."
  },
  {
    "sourceId": "monk.base.flurry-of-blows",
    "name": "Flurry of Blows",
    "actualSourceClass": "Monk",
    "minimumBorrowerTotalLevel": 1,
    "proposedBorrowedProcedure": "Action; exactlytwo separate actualunarmedstrikes with your ownbody/normalunarmedprofile againstone/twolegalcreatures. No borrowedmartialdie,unarmedproficiency,Ki,Tiger/FlowingFormorMonkengine. Actuallyowned independentfeatures may operate within their owncaps; this permission itself generates no resource or recursiveattack."
  }
]
```
