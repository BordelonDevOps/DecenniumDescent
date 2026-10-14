# One-shot: build playtest-consumable canon from GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt
import json
import pathlib

base = pathlib.Path(__file__).resolve().parent.parent
extract = (base / "GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt").read_text(encoding="utf-8")
ws = pathlib.Path(__file__).resolve().parent

m_dd_start = extract.find("Decennium Descent Design Doctrine")
m_canon_start = extract.find("Decennium Descent Gameplay Loop — Canon Rules")
if m_dd_start < 0 or m_canon_start < 0:
    raise SystemExit("Could not locate Design Doctrine / Canon Rules markers in extract")

dd_body = extract[m_dd_start:m_canon_start].strip()
canon_body = extract[m_canon_start:].strip()

design_md = f"""# Decennium Descent Design Doctrine

> Playtest-consumable extract from Gameplay Loop Bible v1.0 (August 2026).
> Source: `Decennium_Descent_Gameplay_Loop_Bible_v1.docx` / `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt`
> Staging only — not promoted to ReviewBible/main. Effective: 2026-08-05.

{dd_body}
"""
(ws / "docs" / "mechanics" / "DESIGN_DOCTRINE.md").write_text(design_md, encoding="utf-8")
print("Wrote DESIGN_DOCTRINE.md", len(design_md))

canon_md = f"""# Decennium Descent Gameplay Loop — Canon Rules

> Playtest-consumable extract from Gameplay Loop Bible v1.0 (August 2026).
> Source: `Decennium_Descent_Gameplay_Loop_Bible_v1.docx` / `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt`
> Staging only — not promoted to ReviewBible/main.
> Status: Canonical gameplay procedure · Version: 1.0 · Effective: 2026-08-05
> Authority pointer: `CANON_MANIFEST.json` (pending V7 domain registration on promote)

{canon_body}
"""
(ws / "docs" / "mechanics" / "GAMEPLAY_LOOP_CANON.md").write_text(canon_md, encoding="utf-8")
print("Wrote GAMEPLAY_LOOP_CANON.md", len(canon_md))

loop = {
    "meta": {
        "id": "Decennium_Descent_Gameplay_Loop_v1",
        "title": "Decennium Descent Gameplay Loop",
        "version": "1.0",
        "effective": "2026-08-05",
        "sourceDoc": "Decennium_Descent_Gameplay_Loop_Bible_v1.docx",
        "authority": "CANON_MANIFEST.json",
        "status": "playtest-staging",
        "notes": (
            "Machine-readable companion to GAMEPLAY_LOOP_CANON.md for V7 playtest packs. "
            "Not promoted to main."
        ),
    },
    "designDoctrine": {
        "governingRule": (
            "Decennium Descent should have 5e's readability and speed, Pathfinder 2e's "
            "tactical clarity and balance discipline, and its own expedition, extraction, "
            "Haven, and seasonal systems."
        ),
        "priorityOrder": [
            (
                "Preserve Decennium Descent's identity: expedition organization, extraction "
                "risk, the Haven economy, the decennial Opening, and seasonal consequences."
            ),
            "Preserve tactical clarity and mathematical balance.",
            (
                "Simplify wording, timing, and table procedure wherever simplification does "
                "not damage the first two priorities."
            ),
        ],
        "vocabulary": {
            "Action": "The character's primary act on a combat turn.",
            "Bonus Action": "A fast ability used only when a rule grants it.",
            "Reaction": "One response between the start of one turn and the start of the next.",
            "Movement": "Travel up to Speed during a combat turn.",
            "Expedition Watch": "One eight-hour block of the Opening.",
            "Activity": "A team assignment resolved during an Expedition Watch.",
            "Pressure": "The current likelihood of a dungeon complication.",
            "Load": "Physical carrying burden.",
            "Extraction Class": "The handling danger and attention created by cargo.",
            "Haven Phase": (
                "Appraisal, claims, sale, recovery, research, and preparation between delves."
            ),
            "Cycle Record": "The persistent consequences carried into the next Opening.",
        },
    },
    "completeLoop": [
        "Choose an objective",
        "Finance the descent",
        "Build the Expedition",
        "Load the convoy",
        "Enter the dungeon",
        "Resolve Watches",
        "Resolve encounters",
        "Manage attrition",
        "Choose cargo",
        "Extract",
        "Resolve the Haven",
        "Advance and prepare",
        "Close the Opening",
    ],
    "modes": {
        "encounter": {
            "unit": "round (~6 seconds)",
            "perTurn": [
                "Movement up to Speed",
                "One Action",
                "One Bonus Action if granted",
                "One free object interaction",
                "One Reaction before next turn",
            ],
            "additionalActionCap": 1,
        },
        "expedition": {
            "watchHours": 8,
            "watchesPerDay": ["Morning", "Afternoon", "Evening"],
            "assignment": "Every member must be assigned one activity per Watch or Rest",
        },
        "haven": {
            "havenTurn": "normally one day",
            "uses": [
                "recovery",
                "crafting",
                "research",
                "business",
                "training",
                "politics",
                "preparation",
            ],
        },
    },
    "coreResolution": {
        "roll": "d20 + ability modifier + proficiency (when trained) + circumstance modifiers",
        "standardDCs": {
            "routineUnderPressure": 10,
            "tierI": 12,
            "tierII": 13,
            "tierIII": 15,
            "tierIV": 16,
            "tierV": 18,
            "tierVI": 19,
        },
        "dcModifiers": {"hard": 3, "severe": 6, "favorable": -3},
        "degrees": {
            "criticalSuccess": "total >= DC + 10",
            "success": "total >= DC",
            "failure": "total < DC",
            "criticalFailure": "total <= DC - 10",
        },
        "nat20": "improve one degree",
        "nat1": "worsen one degree",
        "assistance": {"perAssistant": 1, "maxAssistants": 3, "maxBonus": 3},
    },
    "expedition": {
        "maxCharacters": 12,
        "teams": {
            "Combat": {
                "normalSize": "4-6",
                "purpose": "Fight, breach, escort, and hold routes",
            },
            "Reconnaissance": {
                "normalSize": "1-3",
                "purpose": "Scout, map, trail, conceal, and warn",
            },
            "Research": {
                "normalSize": "1-3",
                "purpose": "Identify, translate, analyze, and reconstruct",
            },
            "Resource": {
                "normalSize": "2-4",
                "purpose": "Harvest, forage, mine, preserve, and craft",
            },
            "Support": {
                "normalSize": "1-3",
                "purpose": "Camp, heal, repair, transport, and administer",
            },
        },
        "offices": [
            "Expedition Leader",
            "Quartermaster",
            "Routekeeper",
            "Surgeon",
            "Claimant of Record",
        ],
        "openingHours": 2400,
        "hornHour": 1200,
        "activeWatchesPerDay": 2,
        "restWatchRequired": True,
        "strainWithoutRest": 1,
    },
    "rest": {
        "shortRest": {
            "durationHours": 1,
            "maxBetweenLongRests": 2,
            "rpRecover": "one-quarter maximum RP rounded down, minimum 1",
            "oracleRevelationCharge": 1,
        },
        "longRest": {
            "duration": "one full Watch",
            "maxPer24h": 1,
            "removesStrain": 1,
            "woundsRequireTreatment": True,
        },
    },
    "route": {
        "ratings": ["Length", "Risk", "Mapping", "Capacity"],
        "progressPerActiveWatch": {
            "SecuredOrMapped": 2,
            "Sketched": 1,
            "UnknownOrObstructed": 0,
        },
        "mappingStates": ["Unknown", "Sketched", "Mapped", "Secured"],
        "overCapacity": {"progressPenalty": 1, "pressureIncrease": 1},
    },
    "pressure": {
        "range": [0, 6],
        "states": {
            "0": "Secured; no routine complication roll",
            "1": "Watched",
            "2": "Unstable",
            "3": "Hostile",
            "4": "Hunted",
            "5": "Overrun",
            "6": "Immediate crisis",
        },
        "complicationRoll": "1d6 <= Pressure at end of active Watch",
        "maxReductionsPerWatch": 2,
        "pressure6": "Severe complication automatically; do not roll",
    },
    "teamActivities": {
        "Combat": ["Advance", "Breach", "Escort", "Patrol"],
        "Reconnaissance": ["Scout Ahead", "Map Route", "Counter-Ambush", "Conceal Trail"],
        "Research": ["Identify", "Translate", "Analyze Threat", "Experiment"],
        "Resource": ["Harvest", "Forage", "Mine or Salvage", "Preserve"],
        "Support": ["Establish Camp", "Treat", "Repair", "Transport"],
    },
    "supply": {
        "unitDefinition": "One Supply Unit sustains one Medium character for one day",
        "smallConsumes": 1,
        "largeConsumes": 2,
        "unpaidDaily": "every unsupported character gains 1 Strain",
    },
    "strain": {
        "0": "No penalty",
        "1": "-1 initiative and expedition checks",
        "2": "Speed -10 ft.; -1 attacks and saves",
        "3": "Disadvantage on expedition checks; cannot Dash twice consecutively",
        "4": "Maximum HP reduced by 25%",
        "5": "Incapacitated except for slow travel and Rest",
        "6": "Death or permanent collapse, as appropriate to the cause",
    },
    "integrity": {
        "range": [0, 3],
        "3": "Sound",
        "2": "Worn; no penalty",
        "1": "Damaged; checks using it suffer -2",
        "0": "Broken; unusable until repaired",
        "repairSuccess": 1,
        "repairCriticalSuccess": 2,
    },
    "load": {
        "unitApproxPounds": 10,
        "carryLimit": "Strength score",
        "sizeMods": {"Small": -2, "Medium": 0, "Large": "double"},
        "burdenedAtHalf": True,
        "burdenedEffects": [
            "Speed -10 ft.",
            "disadvantage on climb/swim/move silently",
        ],
    },
    "extractionClass": {
        "0": "Ordinary trade goods",
        "1": "Common monster parts or durable salvage",
        "2": "Uncommon, fragile, or regulated cargo",
        "3": "Rare artifact, volatile substance, or living captive",
        "4": "Very rare strategic cargo or dangerous curse",
        "5": "Epic cargo likely to attract sovereign or faction intervention",
        "6": "Legendary documented-limit cargo requiring a dedicated operation",
        "tags": [
            "Fragile",
            "Volatile",
            "Cursed",
            "Living",
            "Contraband",
            "Perishable",
            "Attention",
        ],
    },
    "casualtyLoad": {"Medium": 6, "Small": 3, "Large": 12},
    "camps": {
        "Exposed bivouac": {
            "establishment": "No activity",
            "storage": 0,
            "notes": "Rest possible; Pressure +1; no Wound recovery",
        },
        "Temporary Camp": {"establishment": "1 Support Success", "storage": 20},
        "Fortified Outpost": {
            "establishment": "3 accumulated Support Successes and materials",
            "storage": 60,
        },
        "Research Station": {
            "establishment": "Fortified Outpost plus 2 Research Successes",
            "storage": 60,
        },
        "Forward Base": {
            "establishment": (
                "8 total accumulated successes, supply line, and faction approval"
            ),
            "storage": 150,
        },
    },
    "encounterBudgetsFourCharacter": {
        "Routine": 50,
        "Standard": 90,
        "Hard": 130,
        "Severe": 180,
        "Catastrophic": 240,
    },
    "threatPointsRelativeLevel": {
        "-4orLower": 5,
        "-3": 10,
        "-2": 15,
        "-1": 25,
        "0": 40,
        "+1": 60,
        "+2": 90,
        "+3": 135,
        "+4orHigher": 200,
    },
    "partySizeBudgetScale": 0.20,
    "retreat": {
        "declareAt": "start of round",
        "escapeSuccessesNeeded": 3,
        "pursuitSuccessesFail": 3,
        "onSuccess": "Expedition Mode with Pressure +1",
    },
    "wounds": {
        "triggers": [
            "Dropped to 0 HP by a critical hit",
            "Suffered two death-save failures before stabilization",
            "Revived after death or magical soul separation",
            "Suffered a Severe hazard or injury result that specifies a Wound",
        ],
        "perWound": "-1 Constitution saves; Hit Dice healing -1 per die (min 1)",
        "atThree": "Critical: Speed halved; Strain cannot be removed until a Wound treated",
        "treatment": "medical kit + 1 Supply + 8 hours + Medicine vs tier DC",
    },
    "actionEconomyLimits": [
        "No more than one additional full Action per round",
        "Only one Reaction before next turn",
        "Only one Stance unless feature permits two",
        "No more than two independent combat-capable summons; extras use swarm/unit block",
        "Cooldown resets cannot reset the same ability more than once per round",
        (
            "Cannot lose more than one full turn to the same control source without "
            "new save or escalation"
        ),
    ],
    "extraction": {
        "pressureIncrease": "floor(highest Extraction Class / 2), max +3",
        "testTiming": "every major route transition and after every Severe complication",
    },
    "havenOrder": [
        "Quarantine and inspection",
        "Provenance filing",
        "Appraisal",
        "Claims and liens",
        "Disposition",
        "Settlement",
        "Recovery",
        "Standing",
        "Advancement",
        "Next descent",
    ],
    "saleMultipliers": {
        "provenance": {
            "undocumented": 0.5,
            "disputed": 0.75,
            "documented": 1.0,
            "Gate-Sealed": 1.25,
        },
        "demand": {"glutted": 0.75, "normal": 1.0, "sought": 1.25, "strategic": 1.5},
        "condition": {
            "damaged": 0.5,
            "worn": 0.75,
            "sound": 1.0,
            "exceptional": 1.25,
        },
        "urgency": {"forced sale": 0.75, "normal": 1.0, "patient auction": 1.1},
    },
    "sponsorShares": {
        "Self-funded": 0.0,
        "Local guild": 0.20,
        "Merchant or bank": 0.30,
        "Noble or temple": 0.35,
        "Sovereign or great institution": 0.45,
    },
    "reputation": {"min": -5, "max": 5, "maxChangePerScene": 2},
    "xpAwardsPercentOfLevelGap": {
        "Routine": 0.05,
        "Standard": 0.10,
        "Hard": 0.15,
        "Severe": 0.25,
        "GateGuardian": 0.40,
        "ProfitableExtraction": 0.10,
        "FirstVerifiedBreakthrough": "0.05-0.15",
        "sceneCap": 0.60,
    },
    "cycle": {
        "persist": [
            "Character and institutional knowledge",
            "Provenance records and artifacts already extracted",
            "Haven civic core and major permanent institutions unless destroyed",
            "Faction relationships, debts, bloodlines, titles, and property",
            "Secured route principles (not every chamber/node)",
            "Consequences of Gate victories and major failures",
        ],
        "replenish": [
            "Creature populations",
            "Resource nodes and ordinary treasure",
            "Unsecured routes, chambers, hazards, and local settlements",
            "Market demand and scarcity",
            "Faction leadership and expedition competition",
            "The exact expression of the dungeon's tests",
        ],
        "openingChangeCategories": [
            "Geography",
            "Ecology",
            "Economy",
            "Politics",
            "Resonance",
        ],
    },
    "quickReference": {
        "watchOrder": [
            "Confirm assignments",
            "Consume one-third of daily Supply",
            "Resolve team activities",
            "Add route Progress",
            "Apply Pressure changes",
            "Roll the Pressure d6",
            "Resolve complications",
            "Update cargo, Strain, Wounds, and Integrity",
            "Advance eight hours",
        ],
        "havenTurnOrder": [
            "Choose one downtime activity per character",
            "Resolve required checks and costs",
            "Advance one day",
            "Update recovery, crafting, research, business, and faction clocks",
            "Resolve one Haven event when appropriate",
        ],
    },
}

text = json.dumps(loop, indent=2, ensure_ascii=False) + "\n"
(ws / "data" / "public" / "Decennium_Descent_Gameplay_Loop_v1.json").write_text(
    text, encoding="utf-8"
)
(ws / "src" / "data" / "gameplay-loop.json").write_text(text, encoding="utf-8")
print("Wrote gameplay-loop JSON twin paths", len(text))
