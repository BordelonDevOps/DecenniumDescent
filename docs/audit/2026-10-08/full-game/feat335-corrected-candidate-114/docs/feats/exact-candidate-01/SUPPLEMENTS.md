# Complete finite feat supplements

Derived complete-text assembly 106; exact parent review and integration pending.

These separately identified supplements do not add original registry identities or activate deferred payloads.

## SUP-01

```json
{
  "profile": "AC12+floor(current ownerPB/2); dynamic maximumHP5+current total owner level; all ordinary saves use current ownerPB alone; other ability checks use template ability modifiers, no PB unless a real source grants it. Template INT3 is a feat-profile value, not proof that a real source beast meets the INT<7 admission gate.",
  "nativeBody": "Preserve actual original source profile, body identity, current health ratio, size, breathing, conditions, disease, hunger, custody and age. Templates replace only their stated combat/ability/speed values for this bond. Any actual anatomy incapacity/sensory blocker remains. No template creates a supernatural sense, trait, hand or extra body.",
  "actions": "One command and offensive allowance across owner companions/devices per numbered round. Commanded body has one attached phase after whole owner regular turn, move plus chosen legal attack or standard Dash/Disengage/Help/Dodge; Dash adds one currentSpeed to its phase cap, Disengage suppresses opportunities for that phase, Help follows actual5ft/physically possible aid and expires at the next original companion-start marker. No independent BA/Reaction/turn/death save; no extra-turn phase. Uncommanded only defensive movement/Dodge.",
  "conversion": "Admission requires a real living animal with positiveHP and positive maximumHP and an actual eligible willing/tamed receipt. Initial and release conversion preserves health ratio using max(1,floor(newMax*oldHP/oldMax)), not a heal/damage event. At0 the feat animal is dead, never eligible for conversion. Save the prior source profile rather than deriving a new one on release.",
  "recovery": "No resummon, free rest healing, unprinted Hit Dice or new original animal from a saved profile. External legal healing/resurrection retains its actual costs and rules; resurrection returns the same body unbonded, and new bonding still requires the post-death completedLR plus full procedure. Capacity change never repairs injury, replenishes resources or creates death/HP-loss triggers."
}
```

## SUP-02

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

## SUP-03

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

## SUP-04

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

## SUP-05

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

## SUP-06

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

## SUP-07

```json
{
  "copyProfileContract": {
    "capture": "Capture only one directly witnessed resolved component that actually expresses one profile below. Record canonical source/event, actual original spell rank or pre-encounter monster effective rank, native magnitude before external bonuses/defenses, selected type/profile and qualifying own casting route. For monster abilities without a spell rank, use max(1, min(9, ceil(actualCR/2))); missing CR needs a rating assigned before the encounter, never a favorable after-the-fact guess. No unique/legendary/boss feature without an independently reviewed exception; no copying copies, class engines, actions, resources, permanent changes, resurrection, creation, items or protected information. An unsupported role is ineligible, not a blank Director permission.",
    "rankAndPayment": "For original rank 0, q=0; otherwise q=max(1, floor(originalRank/2)). The chosen actual owned spellcasting route must independently support learning q; merely owning a pool or feat prerequisite does not. Use that route’s real ability for attack/DC and spell components V/S, normal rank price 0/2/3/5/7/10/13/17/21/26 plus actual adjustments. It grants a temporary feat-copy route only, never the original full spell. Spellcasting time is oneAction. For a direct Action release, pay/cast/history/interrupt once at commitment, with copy-provenance flags disabling copy/resource/class-proc chains. For a legal Ready, that one casting/payment/history/counter transaction occurs at preparation; its later Reaction release is not a second cast. Apply COPY-READY-ALLOWANCE-02: the applicable allowances are spent at the direct commitment or Ready preparation only. The same paid Ready release, in any otherwise legal round, spends its real Reaction but no new feat or Mirrorsage allowance. An explicit source such as Mirrorsage retains its own actual profile/rank/payment instead of being silently converted. FINAL FS-08: these releases are paid feat-copy casts with actual RP/components/history, not ordinary knowledge grants. Boon uses one feat-copy-boon family; its repeated copies do not add, while genuinely distinct eligible ordinary feat bonuses use FS-03.",
    "numericBound": "For numeric damage/heal/ward select one witnessed native component/type and record its rolled or fixed magnitude B before external bonuses, saves, defenses and recipient caps. If that magnitude was hidden, the Director records it privately; no free identification is given. At feat-copy release roll (q+1)d6, then bound the native numeric result to min(roll, floor(B/2)). No copied critical multiplier, external damage/heal modifier, converted excess or extra recipients. Actual recipient defenses and healing limits still apply. A zero ceiling cannot produce a numeric benefit. This is an explicit NEW meaning of half potency, not an assertion about original undefined wording.",
    "lifecycle": "At most one new paid feat-copy commitment per owner per numbered round across Eldritch Echo, Mimicry and adapted copies: either a direct cast or Ready preparation. An actually applicable Mirrorsage owner also spends its existing shared allowance at that commitment. Completion of the same paid Ready hold spends neither allowance again, even in a later round with either current allowance already spent; an unowned Mirrorsage engine is not granted. Strike/Burst/Mend/Step are immediate. Ward/Hindrance/Boon use their stated maximum two-interval duration; source-specific shorter hold deadlines still govern. Only one pending feat-copy record across Eldritch Echo/Mimicry; before a new capture choose whether to replace the old, losing its paid capture/use without refund. Adaptation may retain permission but creates no second new-commitment allowance. No copied effect grants extra Action/BA/Reaction, persistent body, loot, learning or concentration capacity.\n\nCOPY-READY-ALLOWANCE-02 — owner-directed preparation-round-only successor for the seven FS-08/SUP-07 feat-copy profiles used through Arcane Adaptation, Eldritch Echo and Mimicry. This supersedes COPY-READY-ALLOWANCE-01's both-touched-round policy only. All earlier archives and receipts retain their exact historical wording. This selection changes no profile payload, acquisition predicate, ordinary Ready rule, ordinary class casting cadence or unrelated Mirrorsage class Echo procedure.\n\nPREPARATION. The shared feat-copy cap counts new paid feat-copy casting commitments: a direct cast commits in its current numbered round; a Readied feat copy commits in its preparation numbered round. Require and atomically spend that round's owner feat-copy allowance. If the owner actually has the separately acquired Mirrorsage shared-release engine to which the exact source binds this feat copy, also require and spend that same preparation round's actual shared class allowance. A qualifying ability route alone never creates that engine. Validate the actual setup prerequisites first. At legal preparation commitment, pay the Action, current quote and other actual costs, consume the applicable permission/use once, provide components, record the independent feat-copy family/Dissonance/Refrain once, and establish the one Ready concentration burden before its single preparation counter window. No partial class/feat/resource debit is allowed. Countering, abandonment, replacement, expiry or concentration loss after commitment never refunds those preparation spends, recreates a capture, restores displaced concentration or reopens that round's allowance. Failed precommit validation spends nothing and cannot delete an existing valid hold.\n\nHELD RECORD. Bind one unique preparation ID and actual owner to its fixed captured source/profile/q/mode, preparation-bound choices, paid transaction, consumed permission receipt, preparation round and actual ledger identities. Preserve its original Ready deadline and every independently applicable earlier source/capture/use deadline. Consuming the capture permission at preparation is not itself loss of this paid hold's authorization, but the hold cannot extend the original permission window. No future round's allowance is reserved. The hold remains subject to ordinary concentration, body/source availability and valid replacement rules. Paid preparation alone creates no payload. Earlier prose calling the limit one-copy-release per round is controlled here: it limits new direct casts and Ready preparations, not a later completion of this same paid hold.\n\nRELEASE. After an actual perceivable trigger has completed and before every governing deadline, validate the actual hold and its preparation receipts, the available lawful Reaction, continuing concentration and the release predicates at the points required by their actual sources. Select legal current targets/ordered recipients/area/destination at release under the fixed preparation profile and mode; do not freeze a setup-time ghost target or rewrite preparation-bound choices from hidden results. Neither same-round nor later-round release checks, reserves or spends a new feat-copy allowance or a new Mirrorsage shared-release allowance. The preparation receipts remain spent in their original round. An otherwise lawful delayed release therefore remains eligible even when the release round's feat allowance, an actually owned class shared allowance, or both have already been spent by another lawful use. This exemption belongs only to completion of that specific paid feat-copy hold; it does not waive any new direct cast's or unrelated class Echo's own allowances.\n\nA declined trigger or an invalid precommit release, including no actual Reaction, invalid target/geometry, missing source predicate or uncompleted/unperceived trigger, spends no Reaction, makes no new debit and grants no hidden diagnostic. Keep the existing hold only while its actual concentration and original deadlines permit; another genuine trigger occurrence may be considered. An already-spent release-round copy allowance alone is NOT a failed-release reason. At an exact governing expiry, expiry wins. Lost concentration, actual abandonment, successful replacement or another real ending terminates the hold without a refund; a failed release cannot restore a hold that ended.\n\nOn a valid release commitment, atomically consume this hold once and spend the real Reaction before resolving its one payload. No second RP/material payment, capture-use consumption, casting-family/Refrain update, cast hook or Counterspell window occurs. Subsequent prevention or a failed attack/save outcome does not refund the Reaction or preparation; actual source-specific hidden-eligibility checks retain their own paid timing. Duplicate callbacks/retry IDs cannot create a second payload or debit. Immediate Strike/Burst/Mend/Step end the held concentration after resolution. Ward/Hindrance/Boon continue the same one burden under their actual effect clock and earlier limits, never a second concentration slot.\n\nOTHER USES AND PERSISTENCE. Another copy in the release round still needs its own genuinely available Action/source permission, current legal resources/credentials, its own new-commitment allowances and all ordinary concentration/cadence predicates. No Action, Reaction refresh, capture or second concentration slot is granted. A concentration-breaking new cast can end the old hold even though its allowance is irrelevant to the old release. Releasing a prior hold first leaves a genuinely free current-round allowance available for a separate lawful new commitment; a lawful prior current-round use does not by itself block the old hold's release. Actual competing-use opportunities before the owner's next regular START are illustrative prerequisites unless supplied by a real source; the old Ready cannot be carried past that START merely to obtain the ordinary Action. Save/load, extra turns, changing routes/profiles or round labels must preserve owner/hold identity, original expiry, actual consumed receipts, completed release identity and chronological/per-round ledgers. Release never rewrites a later cast's history. This rule is a proposed authoring successor, not implementation of scheduling, live perception, source-qualified recipient effects, canonical persistence or the game engine.",
    "castFamilyKeyContract": "NEW feat-copy chronological identity. Every paid feat-copy cast records `castFamilyKey = feat-copy::<canonicalSourceEffectId>`. `canonicalSourceEffectId` is the stable identity of the actually witnessed underlying spell/effect from which the bounded profile was captured; for a source-qualified monster ability use that ability's stable source identity. Changing the capture event, owner, Eldritch Echo/Mimicry/Arcane Adaptation permission, bounded profile, selected damage/type component, q, or qualifying casting-ability route does not create a new family. Copies sharing that key use the ordinary chronological Refrain history together. An ordinary cast of the underlying spell uses its ordinary spell family and does not share the feat-copy family; Mirrorsage Echo Release likewise keeps its own class family. A missing stable underlying source identity is ineligible for release rather than being assigned a favorable new key. This key grants no ordinary spell knowledge or access.",
    "concentrationRules": "NEW feat-copy concentration tags. Strike: no. Burst: no. Mend: no. Ward: yes. Hindrance: yes. Boon: yes. Step: no; its movement/teleport resolves instantaneously. A concentration-required copy establishes the releaser's one concentration burden during casting commitment under the ordinary sequence, ending an incompatible existing concentration before the counter window. If that cast is later countered, prior concentration remains ended and no copied lasting effect remains. Loss of concentration ends the Ward/Hindrance/Boon copied effect immediately; their printed earlier deadlines still cap duration. Immediate profiles establish no new concentration burden. Ready is separate: preparation already occupies concentration. On release, an immediate profile resolves and that Ready concentration ends with the released spell; a concentration-required Ward/Hindrance/Boon continues on that same one concentration burden, never a second slot. No witnessed original concentration tag is inherited or used to change these seven profile tags.",
    "strainEngineRef": "FS-09/CRS-03",
    "strainEngineRules": "COPY-ROUTE STRAIN SCOPE. A paid feat-copy cast under FS-08 is an independent feat-casting route for strain purposes. Use FS-09 exactly: base Dissonance 0 for q/rank 0, 1 for ranks 1-5, and 2 for ranks 6-9; apply ordinary same-family Refrain using CRS-01; and use `Limit = max(4, 2*PB + casting modifier)` for that copy route, including its existing surcharge/block thresholds. The owned route chosen to qualify the copy supplies only the permitted casting ability, rank ceiling and other expressly required source credentials; it does not import that class engine's protected Dissonance reduction, routing, vent, prepared-matrix treatment or proc chain into the feat-copy cast. In particular a Wizard-qualified copy is not a prepared matrix, a Shaman-qualified copy is not an ordinary Shaman spell for the totem vent, and a Mirrorsage-qualified copy is not class Echo Release. The ordinary `max(4, 2 + PB + max(0, modifier))` Limit in SPELL_INTEGRATION_RULES remains controlling for ordinary class spells within its existing scope and is not globally changed here. If the only qualifying route is the feat-only Eldritch Blast grant, it supplies CHA and only its actual rank-0 ceiling; it does not change the copy engine or Limit, create a Warlock/class engine, or qualify a ranked q>0 copy.",
    "readyAllowanceDecision": {
      "id": "COPY-READY-ALLOWANCE-02",
      "classification": "Owner-directed preparation-round-only successor; no whole-feat or runtime acceptance",
      "operativeWording": "COPY-READY-ALLOWANCE-02 — owner-directed preparation-round-only successor for the seven FS-08/SUP-07 feat-copy profiles used through Arcane Adaptation, Eldritch Echo and Mimicry. This supersedes COPY-READY-ALLOWANCE-01's both-touched-round policy only. All earlier archives and receipts retain their exact historical wording. This selection changes no profile payload, acquisition predicate, ordinary Ready rule, ordinary class casting cadence or unrelated Mirrorsage class Echo procedure.\n\nPREPARATION. The shared feat-copy cap counts new paid feat-copy casting commitments: a direct cast commits in its current numbered round; a Readied feat copy commits in its preparation numbered round. Require and atomically spend that round's owner feat-copy allowance. If the owner actually has the separately acquired Mirrorsage shared-release engine to which the exact source binds this feat copy, also require and spend that same preparation round's actual shared class allowance. A qualifying ability route alone never creates that engine. Validate the actual setup prerequisites first. At legal preparation commitment, pay the Action, current quote and other actual costs, consume the applicable permission/use once, provide components, record the independent feat-copy family/Dissonance/Refrain once, and establish the one Ready concentration burden before its single preparation counter window. No partial class/feat/resource debit is allowed. Countering, abandonment, replacement, expiry or concentration loss after commitment never refunds those preparation spends, recreates a capture, restores displaced concentration or reopens that round's allowance. Failed precommit validation spends nothing and cannot delete an existing valid hold.\n\nHELD RECORD. Bind one unique preparation ID and actual owner to its fixed captured source/profile/q/mode, preparation-bound choices, paid transaction, consumed permission receipt, preparation round and actual ledger identities. Preserve its original Ready deadline and every independently applicable earlier source/capture/use deadline. Consuming the capture permission at preparation is not itself loss of this paid hold's authorization, but the hold cannot extend the original permission window. No future round's allowance is reserved. The hold remains subject to ordinary concentration, body/source availability and valid replacement rules. Paid preparation alone creates no payload. Earlier prose calling the limit one-copy-release per round is controlled here: it limits new direct casts and Ready preparations, not a later completion of this same paid hold.\n\nRELEASE. After an actual perceivable trigger has completed and before every governing deadline, validate the actual hold and its preparation receipts, the available lawful Reaction, continuing concentration and the release predicates at the points required by their actual sources. Select legal current targets/ordered recipients/area/destination at release under the fixed preparation profile and mode; do not freeze a setup-time ghost target or rewrite preparation-bound choices from hidden results. Neither same-round nor later-round release checks, reserves or spends a new feat-copy allowance or a new Mirrorsage shared-release allowance. The preparation receipts remain spent in their original round. An otherwise lawful delayed release therefore remains eligible even when the release round's feat allowance, an actually owned class shared allowance, or both have already been spent by another lawful use. This exemption belongs only to completion of that specific paid feat-copy hold; it does not waive any new direct cast's or unrelated class Echo's own allowances.\n\nA declined trigger or an invalid precommit release, including no actual Reaction, invalid target/geometry, missing source predicate or uncompleted/unperceived trigger, spends no Reaction, makes no new debit and grants no hidden diagnostic. Keep the existing hold only while its actual concentration and original deadlines permit; another genuine trigger occurrence may be considered. An already-spent release-round copy allowance alone is NOT a failed-release reason. At an exact governing expiry, expiry wins. Lost concentration, actual abandonment, successful replacement or another real ending terminates the hold without a refund; a failed release cannot restore a hold that ended.\n\nOn a valid release commitment, atomically consume this hold once and spend the real Reaction before resolving its one payload. No second RP/material payment, capture-use consumption, casting-family/Refrain update, cast hook or Counterspell window occurs. Subsequent prevention or a failed attack/save outcome does not refund the Reaction or preparation; actual source-specific hidden-eligibility checks retain their own paid timing. Duplicate callbacks/retry IDs cannot create a second payload or debit. Immediate Strike/Burst/Mend/Step end the held concentration after resolution. Ward/Hindrance/Boon continue the same one burden under their actual effect clock and earlier limits, never a second concentration slot.\n\nOTHER USES AND PERSISTENCE. Another copy in the release round still needs its own genuinely available Action/source permission, current legal resources/credentials, its own new-commitment allowances and all ordinary concentration/cadence predicates. No Action, Reaction refresh, capture or second concentration slot is granted. A concentration-breaking new cast can end the old hold even though its allowance is irrelevant to the old release. Releasing a prior hold first leaves a genuinely free current-round allowance available for a separate lawful new commitment; a lawful prior current-round use does not by itself block the old hold's release. Actual competing-use opportunities before the owner's next regular START are illustrative prerequisites unless supplied by a real source; the old Ready cannot be carried past that START merely to obtain the ordinary Action. Save/load, extra turns, changing routes/profiles or round labels must preserve owner/hold identity, original expiry, actual consumed receipts, completed release identity and chronological/per-round ledgers. Release never rewrites a later cast's history. This rule is a proposed authoring successor, not implementation of scheduling, live perception, source-qualified recipient effects, canonical persistence or the game engine.",
      "preparationRoundAllowance": "spent atomically at legal paid preparation; actually owned applicable Mirrorsage allowance only",
      "sameRoundRelease": "validate this hold preparation receipts; spend the real Reaction only, no new copy allowance",
      "laterRoundRelease": "no current-round feat or Mirrorsage allowance check or spend; actual Reaction and all other ordinary/source predicates still required",
      "newCastAtRelease": false,
      "newCounterWindowAtRelease": false,
      "runtimeImplementedByThisRecord": false,
      "supersedes": "COPY-READY-ALLOWANCE-01 both-touched-round accounting only; unchanged earlier archives/receipts remain historical"
    },
    "profiles": [
      {
        "id": "strike",
        "role": "Direct single-target damage",
        "activation": "Action",
        "range": "60 ft, one perceived creature with line of effect",
        "resolution": "Actual own casting ability+PB spell attack; on hit bounded numeric damage of one observed native type. No added critical dice. No original riders. Instant.",
        "concentrationRequired": false
      },
      {
        "id": "burst",
        "role": "Area damage",
        "activation": "Action",
        "range": "Point within 30 ft;10 ft radius, at most 3 originally declared perceived creatures in area with line of effect",
        "resolution": "DEX save vs own DC for bounded numeric observed-type damage, half on success; one shared roll. No original riders. Instant.",
        "concentrationRequired": false
      },
      {
        "id": "mend",
        "role": "Actual normal HP healing",
        "activation": "Action",
        "range": "30 ft one perceived willing living creature with line of effect",
        "resolution": "Restore bounded numeric HP under actual prohibitions/maximum/Critical caps. No reviving, healing dice add-ons, Wound cure, heal-copy/resource trigger or excess conversion. Instant.",
        "concentrationRequired": false
      },
      {
        "id": "ward",
        "role": "Temporary HP",
        "activation": "Action",
        "range": "30 ft one perceived willing living creature with line of effect",
        "resolution": "Offer bounded numerictemp HP into the actual single grant ledger, ending at the source’s second future regular start. Rejected offer wastes the copy. No linked riders.",
        "concentrationRequired": true
      },
      {
        "id": "hindrance",
        "role": "Actual slow or action/reaction control",
        "activation": "Action",
        "range": "30 ft one perceived creature with line of effect",
        "resolution": "WIS save vs own DC or Speed−10 ft and no new Reactions until its next future regular end, never later than the source’s second future regular start. Strongest slow arbitration; no wholeAction/turn denial, repeated save or original hard-control rider.",
        "concentrationRequired": true
      },
      {
        "id": "boon",
        "role": "A source actually granting a positive attack, save or AC modifier",
        "activation": "Action",
        "range": "30 ft one perceived willing creature with line of effect",
        "resolution": "Choose one statistic actually benefited by the witnessed source: +1 AC OR+1 to one next actual attack roll OR+1 to one next actual save, through source’s next future regular end. Strongest feat-copy-boon-family arbitration; no new roll or cloned concentration.",
        "concentrationRequired": true
      },
      {
        "id": "step",
        "role": "Actual short personal movement/teleport",
        "activation": "Action",
        "range": "Self to visible unoccupied fitting space within min(15 ft, floor(observed distance/2))",
        "resolution": "If original component was teleport, teleport with actual line of effect and ordinary teleport restrictions; otherwise move that distance over an actual legal path paying terrain and provoking normally. No passenger, planar travel, new locomotion mode or movement into an unseen space. Instant.",
        "concentrationRequired": false
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
    "dc": "At acquisition select one actual possessed spellcasting route; use DC 8+current PB+that route’s current ability modifier. No phantom Wisdom/Spellcraft statistic. Actual source-specific component/target defenses still apply. FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-01 — KEEP acquisition-only provider selection. A valid paid Conjure Flora acquisition permanently binds its actual qualifying personal casting route and the ability operand supplied by that route. Later loss, expiry, retraining-away or temporary unavailability of that casting grant does not by itself remove Conjure Flora, reselect its provider, prohibit an otherwise legal Flora creation/command/Bloom Burst, terminate an existing seedling or disable an already armed entry trap. Current prepared repertoire, renewable casting charges and RP are not new ongoing Flora prerequisites. This does not qualify a NEW feat acquisition through a grant that is actually gone; ACQ-03 still governs that separate snapshot. Flora is a magical nonspell feat, not a cast through the provider: a spell-only prohibition applies only to its actual scope, Silence still blocks an audible command, and an effect actually suppressing this feat, a plant, its magic or the required action applies under that effect's own rule. NEW explicit lost-provider representation: retain the original provider/ability binding and compute Flora DC as 8 + the owner's current lawful PB + the current modifier of that bound ability; no alternative route, Wisdom default, reconstructed casting entitlement or favorable old ability score is substituted. A missing or invalid original acquisition/provider record is not cured by this rule. Completed results are not recalculated, and existing body HP/save snapshots, deadlines, spent uses and ownership are not reset.",
    "cadence": "Action creates; one creation use per beneficial SR/LR under FS-06; current capacity is one plant, or two at total character level 10. FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-02–03 — NEW second-creation window completion. Each legally completed first creation records one original use ID, its first-plant ID and that plant's original minute deadline, with at most one additional creation unspent. This is a bounded open-use record even when the owner is below total level 10; it is not another rest use or an immediately usable creation at that level. Admit a second creation only while that same first plant remains present and unended, before its original deadline, with the additional creation unspent, current total character level at least 10, actual free plant capacity, and every ordinary Action, ground, range, line-of-effect and use predicate satisfied. The level-10 condition is live at the additional Action, not snapshotted at first creation. Genuine advancement during that open window can make the existing unspent permission usable, but creates no body, charge, healing or new window. Destruction, uprooting, Bloom Burst consumption, expiry or another actual ending of the first plant permanently closes any unused additional-creation permission immediately; its old future deadline does not keep that permission alive. Suppression without an actual ending is not by itself an ending. A legal additional creation consumes that one permission and costs its own Action, but no second rest use; its own minute begins at its own creation. Once the second plant exists, ending the first does not shorten the second's independent deadline. No ended plant, spent permission, missed deadline, level change, recovery, new ID or subsequent body can reopen the old use. A later beneficial rest restores only the ordinary creation allowance under FS-06; a later first creation starts a genuinely new use. Any hostile command, trap or Burst uses the owner's one shared offensive-companion allowance per numbered round. Ordinary command uses the shared Bonus Action and its actual within-60-ft perceptible channel at commitment, with one attached phase after that owner regular turn; use FLQ-04's split-command completion in commandChoice. No independent plant turn or additional allowance is created.",
    "endpoints": "Poisoned/Restrained records also end if the generating plant ends; no concentration is required. Reapplying same profile follows ordinary nonstacking rules. Burst consumes one body before resolving a 10 ft-radius area, all creaturesDEXsave,2d6 selectedtype half on success. Chosenmode/type doesnotchange aftercreation. No destroyed body can command or trap during the resolving event. FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-04 — NEW explicit owner/instance continuity. These particular one-minute, nonconcentration Flora bodies do not end merely because their owner is incapacitated or dies; retain the same owner, mode, actual body state, original deadline and no-resource restrictions. No recipient, ally, host, companion or replacement actor inherits control. A received pending command may resolve only at its already attached original phase under the split-command rule, even if the owner's live initiative slot is removed; preserve that one scheduled phase, not a new recurring independent turn. An already armed Trapcasting plant may perform its specified first-eligible-entry exception without a new owner Action/Reaction or remote command channel, even while its owner cannot act or is dead, but it still needs the actual qualifying entry, operative plant/trap, target legality and unspent same-owner numbered-round allowance. Incapacity/death neither refreshes that allowance nor rearms or moves the trap. Preserve the owner's last lawful PB/selected-ability state when its live actor view ends, applying any subsequently due source-defined changes; death is not a zero ability score, a new provider or a freeze of expiring modifiers. Use that continuing lawful record for later Flora DCs; a missing authoritative operand is an invalid/unestablished input, not permission to invent one. Lawful recovery continues the same history without replaying missed phases or refilling anything. Ending a generating plant still ends its own Poisoned/Restrained records immediately. A legally committed Bloom Burst binds its existing DC/type/area event, consumes its body before its one payload, and does not fail merely because that required consumption has occurred; it grants no other action to the ended body. Other independently applicable cancellation, suppression, condition, duration and target rules retain their own actual scope. No Animal Companion release/death rule or standard-companion movement/Dodge/attack is imported into these fixed Flora profiles.",
    "commandChoice": "Every seedling may use the printed Lash command. Its selected creation mode additionally determines its Spore or Entangle option and its Trapcasting result/burst type; selecting Lash leaves that basic profile. A coordinated command chooses only one permitted outcome from one actual participating plant. Other plants extend the legal Lash origin as printed but never multiply damage, control areas or offense allowances. FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-04 — NEW split command/phase completion. On the owner's regular turn, first establish a legal shared Bonus Action, an available owner/numbered-round offensive-companion allowance, and actual receipt of the required within-60-ft audible or visible command by each nominated participating plant. At that legal commitment spend the Bonus Action and that one shared offensive allowance once; record the owner, original regular-turn/round identity, participating plant IDs, one chosen mode and target or area, its permitted origin or nominated Lash origins, and the immediately following attached phase. This is a paid pending command, not a Readied action, independent plant turn or extra allowance. It need not be the owner's last voluntary decision that turn. Resolve it once in the attached phase after that same regular turn's actual end processing, using the preserved schedule; an extra turn neither advances nor duplicates that phase. Recheck the surviving unended, unsuppressed, otherwise capable participating plant and the mode's actual target/area, range, perception and line-of-effect requirements. For Lash, an independently legal surviving nominated origin may support the same selected target; losing the selected Spore/Entangle origin does not authorize another origin or mode. For an area, resolve its actual occupants at that phase. If the chosen outcome is no longer legal, close the pending command with no effect, no refund, no new target and no carry to a later phase. After actual receipt, later owner incapacity, Silence, loss of owner-to-plant sight/range/channel, or owner death alone does not retract that command: no continuous concentration/channel/consciousness requirement is added. These states can prevent a NEW command or personal creation/Bloom Burst. An effect expressly cancelling the pending command or disabling/ending its plant still controls. Once committed, no other companion or armed trap can spend the same owner-round allowance, and the phase does not spend it a second time.",
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

## SUP-08

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

## SUP-09

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
    "proposedBorrowedProcedure": "KEEP this SUP-09 row's exact source ranger.base.nature-s-whisper, minimum borrower total level 1 and actualSourceClass Ranger. Use only the separately paid Versatile Mastery ability branch, its one-minute preparation within 5 feet, current conscious willing party donor within 30 feet who actually perceives and understands the signal, and its one-use/beneficial-rest and same-card recharge histories. The donor must actually hold the chosen unsuppressed, nonborrowed class grant. No Ranger level, repertoire, skill proficiency, pool or engine is copied. Pay the borrower's own legal Action and 1 actual personal RP plus its feat use at activation commitment; a valid generic Ready substitutes the setup Action and release Reaction as specified below. The donor pays nothing.\n\nThe following complete native operating procedure also controls this one borrowed activation; 'you' means the borrower. The native Ranger acquisition schedule is not imposed as a second acquisition gate on this expressly permitted borrowed route. This replaces only this row's former unresolved 'minorWeave/sharedcasting restrictions' wording, not the other eleven SUP-09 procedures:\n\nGain advantage on one Perception/Survival check to find tracks, hidden natural creatures or signs of passage. It reveals evidence on success, not automatically creatures through total cover, incorporeal beings or thoughts.\n\nNEW NWQ-01 classification: this exact card is a magical nonspell class technique, not an ordinary spell, class spell, cantrip, Echo release or Matrix cast. Preserve spellRank:null and the historical originalText; no rank, school, spell component block, repertoire, spellcasting credential or class engine is inferred from its name, its historical minor-spell wording or its 1 RP cost.\n\nNEW NWQ-02 activation: no verbal, somatic, focus, material, command-word or audible channel is required by the technique itself. You must be conscious, capable of the required Action, legitimately entitled to this exact activation, ready on its own recharge ledger, and able to perceive and have line of effect to the selected actual natural terrain within 15 feet. Silence, occupied hands or lack of a casting focus alone do not prohibit it. Actual suppression or a prohibition whose operative scope covers this magical technique still applies. The later investigation keeps its own senses, hands, tools, access and task requirements. A permitted borrowed activation separately requires Versatile Mastery's actual donor preparation, consent and perceived/understood signal; the technique supplies no communication channel.\n\nKEEP shared technique strain: pay 1 actual RP from your own existing lawful personal pool, not a donor pool or newly granted pool. No ordinary spell-rank price, spell strain surcharge, automatic spell Dissonance, Refrain update, remembered-spell-name change, Fracture ranked-cast prohibition or rank-based trauma is applied by this activation. It does not clear, advance, consume or vent an ordinary spell-cadence record. Do not invent a casting ability or recompute a strain Limit for it. A later Perception or Survival check uses your own current applicable task ability and actual proficiency or replacing Expertise, ordinarily Wisdom, not a donor modifier or automatic borrowed skill proficiency. There is no activation attack or saving-throw DC. Its legal commitment is a magical-ability-use event: it prevents idle-turn Dissonance recovery on the actor's regular turn containing that commitment, including when the paid activation is interrupted. An illegal uncommitted declaration is not such an event. Merely retaining the rider or applying it to a later ordinary task is not another activation. Extra turns and off-turn releases create no additional recovery tick and cannot rewrite a completed tick. Actual separately acquired hooks operate only on their exact triggers; this is not a Bard Performance or an ordinary Ranger spell cast, and it grants no donor Track Target, Hit Chain, stabilization, Crescendo or Echo engine.\n\nNEW NWQ-04 commitment and area: before payment, declare this source, actor and one fixed investigation area consisting only of the actual natural terrain within 15 feet of the actor's commitment position that is then perceivable and has line of effect. Record that area and position; the area does not follow the actor and no moving aura or remote sensor is created. Actual hidden clues need not already be known or present to make an otherwise lawful investigation site eligible. Commit the legal Action and 1 RP together, set the actor's same-card Recharge counter to 3, and, for borrowing, spend the single Versatile Mastery use at that same commitment. Record donor provenance without spending any donor resource. A rejected precommit declaration spends none of these costs. Resolve the activation within that same action after only genuinely applicable source-defined interruptions; there is no automatic Counterspell window, opposed cast roll or concentration test. Ordinary Counterspell and rank-limited spell dispels do not acquire this nonspell target. A separately sourced interrupt or suppression must actually cover it; ordinary damage alone does not add a concentration requirement. If the actor cannot finish the activation or its fixed terrain is no longer legally in range, perceivable and reachable by line of effect at resolution, the paid activation fails without a new area or refund. Borrowing's donor condition is tested at actual activation commitment, not imposed as a new continuing tether after receipt of the signal.\n\nNEW NWQ-04 rider and check: a surviving activation gives this actor one unused rider from actual resolution until resolution time plus 60 elapsed seconds; the exact deadline is not renewed by travel, turns, initiative changes, donor departure or the borrowed permission ending. No concentration is required. At most one unused Nature's Whisper rider belongs to that actor across native and borrowed uses; a new successful resolution replaces an older unused rider, not stacks or banks checks. A failed or interrupted new activation does not itself replace an older otherwise valid rider. Before any dice or outcome are supplied, voluntarily bind the rider to one separately lawful and paid Perception or Survival check about tracks, hidden natural creatures or signs of passage in the original fixed area. The relevant terrain/evidence must still be natural, within 15 feet of the actor and accessible to the task's actual senses and line of effect; no total-cover, thoughts, incorporeal-detection or automatic-revelation exception is supplied. Consume the rider at that check's outcome commitment before rolling or determining its result, even if other advantage already exists, disadvantage cancels it, the legal check fails, or a genuine interruption then prevents its result. An invalid check declaration does not consume the rider or grant a free roll. A paid longer task whose check reaches adjudication at or after the deadline receives no rider. Use ordinary task resolution and advantage cancellation; no passive-score adjustment, extra degree effect, free check, new retry or second bonus is granted. Reveal only real evidence supported by the actual successful task and observer rules; unknown data is not proof of absence. Failure does not reveal otherwise hidden facts. Expired, consumed or ended riders cannot be reclaimed by repeating a request.\n\nKEEP generic nonspell Ready: this Action-time technique may be readied through the current Ready procedure. Ready setup spends its Action and records one perceivable trigger; it does not activate Nature's Whisper, pay its RP/feat use, start its Recharge, start its minute, update spell history or create held-spell concentration. On a legal release before Ready expires, spend the required permitted Reaction and perform the actual activation commitment instead of another Action; recheck its own entitlement, recharge, personal RP, terrain and, for borrowing, the prepared donor/signal conditions at that release. An invalid or declined trigger spends no release resource and may await another valid trigger within the same Ready window. Unreleased, replaced or expired Ready loses its setup Action but not an unspent Nature/feat cost. A legally released then interrupted activation retains all committed costs and Recharge. Native and borrowed copies use the actor's same source-ID recharge history; borrowing does not refresh it or the donor's history. Recharge 3 ticks once at each subsequent owner regular-turn start, or once per six elapsed seconds outside initiative without double counting; extra Actions and extra turns do not tick it. A recharge becoming ready grants no new borrowed feat use."
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
