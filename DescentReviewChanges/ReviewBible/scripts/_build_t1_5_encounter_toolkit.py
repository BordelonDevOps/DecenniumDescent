# One-shot builder for T1–5 encounter operational toolkit JSON.
# Run: python scripts/_build_t1_5_encounter_toolkit.py

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]


def card(**kwargs):
    return kwargs


def roster(id, title, job, band, detailed_actors, abstract=None, levers=None, notes=""):
    return {
        "id": id,
        "title": title,
        "job": job,
        "targetPressureBand": band,
        "detailedActors": detailed_actors,
        "abstractSupport": abstract or [],
        "levers": levers
        or {"player": "", "director": "", "exit": ""},
        "notes": notes,
    }


def actor(
    name,
    count,
    role,
    bestiary_name=None,
    cr=None,
    intended_cr_band=None,
    sandbox_cr=False,
    note="",
):
    a = {"displayName": name, "count": count, "role": role}
    if bestiary_name:
        a["bestiaryName"] = bestiary_name
    if cr is not None:
        a["bestiaryCr"] = cr
    if intended_cr_band:
        a["intendedCrBand"] = intended_cr_band
    if sandbox_cr:
        a["sandboxCr"] = True
    if note:
        a["note"] = note
    return a


toolkit = {
    "meta": {
        "id": "t1-5-encounter-toolkit",
        "title": "Tier 1–5 Encounter Operational Toolkit",
        "stamped": "2026-07-31",
        "status": "director-ops draft — EV/threat budgets; not an XP economy",
        "sources": [
            "docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx (Ch 15 EV, Ch 16 eight-actor, Ch 29 workflow, Part VII Ashen Bell, Part IX T1–5 ops)",
            "src/data/floor-encounters.json (zones, havens, POIs, mapped T1–5)",
            "docs/mechanics/BESTIARY_LORE_PASS_2026-07-30.md + src/bestiary_data_full.json (Guardian CR/Type)",
            "docs/mechanics/XP_ADVANCEMENT_CANON.md (awards BLOCKED)",
            "docs/manuals/Instruments_of_the_Weave.md (tier pressure tables)",
        ],
        "canonLocks": {
            "openingHours": 2400,
            "hornPoNRHours": 1200,
            "expeditionMax": 12,
            "umbrinNotDrow": True,
            "noSwtor": True,
            "gateGuardianLiveNamesOnly": True,
        },
        "xpStance": (
            "XP award rules remain BLOCKED (thresholds exist; CR→XP / encounter XP budgets "
            "are not canon). This toolkit uses bible EV / incoming-pressure bands and the "
            "eight-actor rule only. Do not invent a second XP economy."
        ),
    },
    "tierFloorMap": [
        {
            "tier": 1,
            "floors": [1, 10],
            "floorsLabel": "1–10",
            "zone": "Yieldheart Caverns",
            "guardian": "Vaskor, the Stone Maw",
            "gate": "Vaskor's Seal / Floor 10 (Warded Gate at Floor 3 ends automaton patrol, not the seal)",
            "difficulty": "Novice",
            "mapped": True,
        },
        {
            "tier": 2,
            "floors": [11, 20],
            "floorsLabel": "11–20",
            "zone": "Bloomdeep Marsh",
            "guardian": "The Bloom That Hungers",
            "gate": "Sporemist Gate (end Floor 20)",
            "difficulty": "Apprentice",
            "mapped": True,
        },
        {
            "tier": 3,
            "floors": [21, 30],
            "floorsLabel": "21–30",
            "zone": "Anvil of Brogi",
            "guardian": "Ashthirst the Hollow",
            "gate": "Lavaflow Gate (end Floor 30)",
            "difficulty": "Journeyman",
            "mapped": True,
        },
        {
            "tier": 4,
            "floors": [31, 40],
            "floorsLabel": "31–40",
            "zone": "Isles of Eternal Radiance",
            "guardian": "Gor Vekk, Architect of Ends",
            "gate": "Radiance Gate (end Floor 40)",
            "difficulty": "Expert",
            "mapped": True,
        },
        {
            "tier": 5,
            "floors": [41, 50],
            "floorsLabel": "41–50",
            "zone": "Sanctum of Echoing Choirs",
            "guardian": "Choralith, Voice Below",
            "gate": "Canticle Gate (end Floor 50); Bar of Last Refuge = soft cultural quit ≠ Horn",
            "difficulty": "Master",
            "mapped": True,
        },
    ],
    "budgetGuidance": {
        "method": "Combat as Expected Value (Director bible Ch 15)",
        "formulas": {
            "roundsToResolve": "foeTotalHP ÷ partyDamagePerRound",
            "incomingPressure": "(foeDamagePerRound × numberOfFoes) × roundsToResolve",
            "hitAssumption": (
                "Assume ~2/3 of foe attacks/saves land unless accuracy or defenses say "
                "otherwise (Ch 29)"
            ),
        },
        "pressureBands": [
            {
                "band": "Routine",
                "incomingPressurePctOfPartyHP": "<20%",
                "directorReading": "Use only if it teaches, reveals, or spends a meaningful non-HP resource",
            },
            {
                "band": "Standard",
                "incomingPressurePctOfPartyHP": "20–40%",
                "directorReading": "Win with visible cost if engaged honestly",
            },
            {
                "band": "Hard",
                "incomingPressurePctOfPartyHP": "40–65%",
                "directorReading": "Poor opening / failed objective can drop characters; retreat must remain possible",
            },
            {
                "band": "Severe",
                "incomingPressurePctOfPartyHP": "65–90%",
                "directorReading": "Telegraph clearly; terrain, prep, or objective leverage required",
            },
            {
                "band": "Catastrophic",
                "incomingPressurePctOfPartyHP": ">90%",
                "directorReading": "Only if party knowingly chose risk, has exits, or fight is not meant to be won by damage alone",
            },
        ],
        "rolePressure": (
            "Add one pressure step if two or more apply without a known counter: reliable "
            "stun/paralysis, forced movement into severe hazards, flight vs melee-heavy party, "
            "invisibility without detection, meaningful foe healing, protected independent "
            "objective. Remove one step for surprise, strong chokepoint, researched "
            "vulnerability, or participating allies."
        ),
        "eightActorRule": {
            "maxDetailedInitiativeActors": 8,
            "abstractWith": ["reinforcementClocks", "moraleTracks", "offMapObjectives"],
            "waves": (
                "Prepare total opposition; reveal only perceptible actors first. Later waves "
                "need a visible trigger. Never add waves solely because the first group died quickly."
            ),
        },
        "expeditionSeatNote": (
            "Full Expedition max 12 (RAW). Detailed combat usually runs the Combat team (~4) "
            "plus a few allies/foes under the eight-actor cap; other seats resolve via clocks/checks."
        ),
        "suggestedDetailedActorCountsByJob": {
            "Teaching": "2–4 detailed foes (+ hazard as non-actor)",
            "Taxing": "3–6 detailed foes or 1 brute + 2–3 skirmishers",
            "Revealing": "1–3 foes; prioritize behavior/terrain over HP",
            "Choosing": "2–5 foes or split fronts via off-map objective",
            "ClimacticSeal": "Guardian + 0–2 arena features as detailed actors; extra pressure via plates/phases/waves under eight-actor",
            "HavenSiege": "≤8 detailed; reinforce with clocks/morale",
        },
        "tierThreatNotes": [
            {
                "tier": 1,
                "defaultBand": "Teaching→Standard",
                "notes": "First fights teach weight/echo/claim. Hard reserved for ignored hazards or split parties. Seal = Hard→Severe with Recognition leverage.",
            },
            {
                "tier": 2,
                "defaultBand": "Standard",
                "notes": "Contamination and living routes raise non-HP tax. Hard when masks fail or Heartroot contested.",
            },
            {
                "tier": 3,
                "defaultBand": "Standard→Hard",
                "notes": "Industrial timing can add a free pressure step if players ignore stated cycles.",
            },
            {
                "tier": 4,
                "defaultBand": "Hard",
                "notes": "Exposure + reflection; shade/sun-shields are consumable Resource budget.",
            },
            {
                "tier": 5,
                "defaultBand": "Hard→Severe",
                "notes": "Accumulated wear + sound discipline. Catastrophic only for knowingly pressing Canticle without exits.",
            },
        ],
    },
    "gateGuardiansT1to5": [
        {
            "tier": 1,
            "name": "Vaskor, the Stone Maw",
            "type": "Elemental",
            "size": "Huge",
            "challengeRating": "8",
            "xpField": 3900,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award until XP_ADVANCEMENT_CANON resolves",
            "alignment": "Neutral",
            "zoneFound": "Yieldheart Caverns",
            "sealFloor": 10,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 2,
            "name": "The Bloom That Hungers",
            "type": "Plant",
            "size": "Huge",
            "challengeRating": "11",
            "xpField": 7200,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Chaotic Evil",
            "zoneFound": "Bloomdeep Marsh",
            "sealFloor": 20,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 3,
            "name": "Ashthirst the Hollow",
            "type": "Elemental",
            "size": "Huge",
            "challengeRating": "14",
            "xpField": 11500,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Neutral Evil",
            "zoneFound": "Anvil of Brogi",
            "sealFloor": 30,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 4,
            "name": "Gor Vekk, Architect of Ends",
            "type": "Aberration",
            "size": "Large",
            "challengeRating": "17",
            "xpField": 18000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Lawful Evil",
            "zoneFound": "Isles of Eternal Radiance",
            "sealFloor": 40,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 5,
            "name": "Choralith, Voice Below",
            "type": "Aberration",
            "size": "Large",
            "challengeRating": "20",
            "xpField": 25000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Neutral",
            "zoneFound": "Sanctum of Echoing Choirs",
            "sealFloor": 50,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
    ],
    "bestiaryCaveat": (
        "Trash/zone fauna in bestiary_data_full.json often has sandbox Type/CR/zoneFound "
        "mismatches. Rosters prefer lore-scrubbed names that exist post BESTIARY_LORE_PASS "
        "and state intendedCrBand for EV planning. When excel CR is absurd, use bible Ch 17 "
        "reskin from a same-band template. Never use SWTOR names. Prefer Umbrin over any "
        "residual Drow labels."
    ),
    "inventoryExisting": {
        "floorEncountersJson": {
            "path": "src/data/floor-encounters.json",
            "has": "T1–5 mapped zones, havens, POIs, bosses; T6–10 draft stubs; hornRule 1200/2400",
        },
        "ashenBell": {
            "path": "docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx Part VII",
            "has": "Full Tier 1 Opening through Vaskor + compact F4–9 keys",
        },
        "generators": {
            "path": "src/components/GeneratorsPanel.tsx",
            "has": "Dice, names, hooks, POI/haven/loot sparks from floor-encounters; thin full encounter gen",
        },
        "monstersLibrary": {
            "path": "src/components/MonstersLibrary.tsx + src/bestiary_data_full.json",
            "has": "~785 creatures; Gate Guardians tagged; many trash combat shells draft",
        },
        "instrumentsPressure": {
            "path": "docs/manuals/Instruments_of_the_Weave.md Part X",
            "has": "d12 tier pressure tables T1–5+",
        },
        "encountersBrowser": {
            "path": "src/components/EncountersBrowser.tsx",
            "had": "Haven/POI/boss browser only — no EV budgets or rosters before this toolkit",
        },
    },
}

tiers = []

# ----- Tier 1 -----
tiers.append(
    {
        "tier": 1,
        "zone": "Yieldheart Caverns",
        "floors": "1–10",
        "guardian": "Vaskor, the Stone Maw",
        "corePressures": [
            "Weight / burden / claim",
            "Echo / Noise",
            "Diminishing automaton supervision (F1–3 only)",
            "Route investment vs race depth",
        ],
        "ashenBell": {
            "status": "Ready-to-run in Director bible Part VII",
            "arc": "Opening hour 0 → Floors 1–10 → Vaskor's Seal",
            "compactKeys": [
                {
                    "floors": "1–3",
                    "summary": "Crystalfront / Hearth of Yieldheart / Warded Gate — teach patrol edge, salvage claim, echo discipline",
                },
                {
                    "floor": 4,
                    "name": "The Weight Garden",
                    "summary": "Pressure-grown crystal; rescue Pell Orra; pressure seeds",
                },
                {
                    "floor": 5,
                    "name": "The Calcified Road",
                    "summary": "Stillness calcifies; parallel Combat/Research/Support",
                },
                {
                    "floor": 6,
                    "name": "Stonewake Refuge",
                    "summary": "First durable haven; cistern burrow quest; ownership law",
                },
                {
                    "floor": 7,
                    "name": "The Split Choir",
                    "summary": "Interfering tones; resonator = Vaskor Recognition phrase piece",
                },
                {
                    "floor": 8,
                    "name": "The Maw's Tribute",
                    "summary": "Mass-gated jaws; surrender gear as bait",
                },
                {
                    "floor": 9,
                    "name": "The Surveyor's Descent",
                    "summary": "Declared weight ledges; seal approach",
                },
                {
                    "floor": 10,
                    "name": "Vaskor's Seal",
                    "summary": "Recognition questions before initiative; burden plates",
                },
            ],
        },
        "faunaRoles": [
            "crystal feeders",
            "vibration burrowers",
            "Pact automata (procedure enforcers)",
            "scavengers who retreat when denied food",
        ],
        "sampleRosters": [
            roster(
                "t1-patrol-tax",
                "Automaton Procedure Check (F1–3)",
                "Teaching",
                "Routine→Standard",
                [
                    actor(
                        "Pact Automaton Sentinel",
                        2,
                        "brute/controller",
                        "Deep Scion",
                        "4",
                        "2–4",
                        note="No Automaton row in bestiary — reskin Deep Scion per Ch 17",
                    ),
                    actor(
                        "Crystal Shardling",
                        2,
                        "skirmisher",
                        "Ochre Jelly",
                        "1/4",
                        "1/4–1",
                        note="Reskin as mineral feeder swarmlets",
                    ),
                ],
                abstract=["Noise clock: shout → +1 reinforcement Automaton in 2 rounds"],
                levers={
                    "player": "Show registered claim / follow posted procedure to skip fight",
                    "director": "One Automaton stands down if party complies",
                    "exit": "Mapped side passage back to Crystalfront",
                },
                notes="Demonstrate that not every foe fights to the death.",
            ),
            roster(
                "t1-echo-gallery",
                "Echoing Gallery Stir (F2)",
                "Taxing",
                "Standard",
                [
                    actor("Cave Bear", 1, "brute", "Cave Bear", "2", "2"),
                    actor("Spiral Worm", 2, "skirmisher", "Spiral Worm", "2", "2"),
                    actor(
                        "Umbrin Arachnid scout",
                        1,
                        "skirmisher",
                        "Umbrin Arachnid",
                        "1",
                        "1",
                        note="Umbrin demonym — never Drow",
                    ),
                ],
                abstract=["Morale: scavengers flee if bear drops and party holds light"],
                levers={
                    "player": "Whisper / split noise; use echo to locate before engage",
                    "director": "Delayed burrower wave if Noise ≥ threshold",
                    "exit": "Retreat toward Hearth of Yieldheart (F3)",
                },
                notes="Keep ≤8 detailed. Prefer 4 foes for Combat team of 4.",
            ),
            roster(
                "t1-stonewake-burrow",
                "Crystal Burrow (F6 haven quest)",
                "Choosing",
                "Standard→Hard",
                [
                    actor(
                        "Hookbeast matriarch",
                        1,
                        "brute",
                        "Hookbeast",
                        "0",
                        "3–4",
                        True,
                        "Excel CR 0 is sandbox garbage — scale to CR 3–4 template",
                    ),
                    actor(
                        "Crystal Shardling",
                        3,
                        "skirmisher",
                        "Ochre Jelly",
                        "1/4",
                        "1/4–1",
                    ),
                    actor("Spiral Worm", 1, "controller", "Spiral Worm", "2", "2"),
                ],
                abstract=["Reinforcement clock 3 rounds if cistern cracked"],
                levers={
                    "player": "Pressure seeds redirect burrow; or negotiate faction claim",
                    "director": "Haven remembers method (fight / redirect / cede)",
                    "exit": "Collapse tunnel behind party — costs route later",
                },
                notes="Ashen Bell key encounter — aftermath matters more than kill XP.",
            ),
            roster(
                "t1-vaskor-seal",
                "Vaskor's Seal (F10)",
                "Climactic",
                "Hard→Severe",
                [
                    actor(
                        "Vaskor, the Stone Maw",
                        1,
                        "seal/guardian",
                        "Vaskor, the Stone Maw",
                        "8",
                        "8",
                    ),
                    actor(
                        "Burden Plate (arena feature)",
                        2,
                        "hazard-actor",
                        note="Count toward eight-actor only if they act each round; else treat as terrain lever",
                    ),
                ],
                abstract=[
                    "Recognition phase before initiative",
                    "Dust-mark claim phase at first major threshold",
                ],
                levers={
                    "player": "Honest Recognition answers; redistribute carried weight",
                    "director": "Contradictions activate abandoned items; do not silent-fudge HP",
                    "exit": "Yield/sleep outcome possible if seal condition unmet",
                },
                notes="Guardian is seal of burden/passage. Seed burdens on F1–9.",
            ),
        ],
        "encounterCards": [
            card(
                id="t1-f1-spire",
                floors="1",
                title="Spire of Whispers",
                job="Revealing",
                targetBand="Routine",
                site="Spire of Whispers",
                summary="Humming stalagmite; murmurs as rumor delivery. Optional 1–2 scavengers if party chips ore.",
                detailedActorBudget="0–2",
                hazard="Attention from harvesting Luminous Veins nearby",
            ),
            card(
                id="t1-f2-echo",
                floors="2",
                title="Echoing Gallery Discipline",
                job="Teaching",
                targetBand="Standard",
                site="Echoing Gallery",
                summary="Noise summons dormant guardians or frays party coordination.",
                detailedActorBudget="3–5",
                rosterRef="t1-echo-gallery",
            ),
            card(
                id="t1-f3-warded",
                floors="3",
                title="Warded Gate Puzzle",
                job="Choosing",
                targetBand="Hard if failed",
                site="Warded Gate",
                summary="Glyph puzzle; failure = arcane backlash + possible Automaton response. Beyond = no patrol net.",
                detailedActorBudget="0–3",
                hazard="Backlash as EV spike, not mandatory TPK",
            ),
            card(
                id="t1-f4-weight",
                floors="4",
                title="Weight Garden",
                job="Choosing",
                targetBand="Standard",
                site="Ashen Bell F4",
                summary="Rescue vs redistribute weight; formation movement hazard.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t1-f5-calcified",
                floors="5",
                title="Calcified Road",
                job="Taxing",
                targetBand="Standard",
                site="Ashen Bell F5",
                summary="Movement prevents calcification; Research needs escort.",
                detailedActorBudget="2–4",
                hazard="Stillness clock as pressure",
            ),
            card(
                id="t1-f6-haven",
                floors="6",
                title="Stonewake Cistern Burrow",
                job="Choosing",
                targetBand="Standard→Hard",
                site="Stonewake Refuge",
                summary="Fight, redirect, or faction claim.",
                detailedActorBudget="4–6",
                rosterRef="t1-stonewake-burrow",
            ),
            card(
                id="t1-f7-split",
                floors="7",
                title="Split Choir Resonator",
                job="Revealing",
                targetBand="Standard",
                site="Ashen Bell F7",
                summary="Tone tunnels; repair resonator for Recognition phrase.",
                detailedActorBudget="1–3",
                hazard="Deafening / whispered command routes",
            ),
            card(
                id="t1-f8-tribute",
                floors="8",
                title="Maw's Tribute",
                job="Choosing",
                targetBand="Hard if greedy",
                site="Ashen Bell F8",
                summary="Leave gear or clever mass solutions; bait chambers.",
                detailedActorBudget="2–5",
            ),
            card(
                id="t1-f9-surveyor",
                floors="9",
                title="Surveyor's Descent",
                job="Taxing",
                targetBand="Standard",
                site="Ashen Bell F9",
                summary="Declared weight ledges; rival clocks.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t1-f10-seal",
                floors="10",
                title="Vaskor's Seal",
                job="Climactic",
                targetBand="Hard→Severe",
                site="Gate",
                summary="Recognition → burden combat → claim phase.",
                detailedActorBudget="1–3",
                rosterRef="t1-vaskor-seal",
            ),
        ],
    }
)

# ----- Tier 2 -----
tiers.append(
    {
        "tier": 2,
        "zone": "Bloomdeep Marsh",
        "floors": "11–20",
        "guardian": "The Bloom That Hungers",
        "corePressures": [
            "Moisture / contamination",
            "Visibility (mist/spores)",
            "Living routes",
            "Mutual dependence on floor cultures",
        ],
        "gatePrep": "Foreshadow Bloom as predator + regulator. Heartroot Blossoms acquisition method changes seal aftermath.",
        "faunaRoles": [
            "spore clouds",
            "root-graspers",
            "amphibian enclaves",
            "Mycelian networks",
            "hunger scavengers",
        ],
        "sampleRosters": [
            roster(
                "t2-reed-ambush",
                "Reedcaller Ambush (F11)",
                "Taxing",
                "Standard",
                [
                    actor("Giant Toad", 1, "brute", "Giant Toad", "6", "5–6"),
                    actor(
                        "Sporefolk Sprout",
                        4,
                        "swarm skirmisher",
                        "Sporefolk Sprout",
                        "1/2",
                        "1/2–1",
                    ),
                    actor("Banderhobb", 1, "controller", "Banderhobb", "3", "3"),
                ],
                abstract=["Morale: sprouts break if toad flees into mire"],
                levers={
                    "player": "Reedcaller signal discipline; burn vs redirect spores",
                    "director": "Mist hides retreat for either side",
                    "exit": "Rootlight Sanctuary bearing if earned",
                },
                notes="Stay at 6 detailed actors.",
            ),
            roster(
                "t2-reliquary",
                "Overgrown Reliquary Roots (F14–15)",
                "Revealing",
                "Standard→Hard",
                [
                    actor(
                        "Violet Fungus",
                        2,
                        "controller",
                        "Violet Fungus",
                        "6",
                        "4–6",
                        note="Type field in Excel may be wrong — treat as Plant hazard-foe",
                    ),
                    actor(
                        "Sporefolk Adult",
                        1,
                        "brute",
                        "Sporefolk Adult",
                        "14",
                        "6–8",
                        True,
                        "CR 14 may be high for mid-T2 — reskin down to CR 6–8 unless party is stacked",
                    ),
                    actor(
                        "Sporefolk Sprout",
                        3,
                        "skirmisher",
                        "Sporefolk Sprout",
                        "1/2",
                        "1/2",
                    ),
                ],
                levers={
                    "player": "Identify which growth is medicine vs predator",
                    "director": "Burning clears cloud but awakens roots",
                    "exit": "Negotiate Mycelian quarantine passage",
                },
                notes="Job is reveal ecology management — not clear-cut kill.",
            ),
            roster(
                "t2-bloom-seal",
                "Bloom That Hungers (F20)",
                "Climactic",
                "Hard→Severe",
                [
                    actor(
                        "The Bloom That Hungers",
                        1,
                        "seal/guardian",
                        "The Bloom That Hungers",
                        "11",
                        "11",
                    ),
                    actor(
                        "Heartroot Tendril",
                        2,
                        "skirmisher",
                        "Violet Fungus",
                        "6",
                        "4–6",
                        note="Arena tendrils — reskin",
                    ),
                ],
                abstract=["Spore weather as reinforcement clock if blossoms impure"],
                levers={
                    "player": "Blossom provenance changes confrontation",
                    "director": "Phase shifts predator↔regulator question",
                    "exit": "Partial cleanse opens gate with cost",
                },
                notes="Plant / Huge / CR 11 / CE — Gate Guardian.",
            ),
        ],
        "encounterCards": [
            card(
                id="t2-f11-reed",
                floors="11",
                title="Reedcaller's Circle",
                job="Teaching",
                targetBand="Standard",
                site="Reedcaller's Circle",
                summary="Whisper signals echo; unwanted ears.",
                rosterRef="t2-reed-ambush",
                detailedActorBudget="4–6",
            ),
            card(
                id="t2-f12-spore",
                floors="12",
                title="Spore-Veil Falls",
                job="Taxing",
                targetBand="Standard",
                site="Spore-Veil Falls",
                summary="Timed dash between spore spurts; mask saturation.",
                detailedActorBudget="0–3",
                hazard="Spore EV as environment",
            ),
            card(
                id="t2-f12-13-mire",
                floors="12–13",
                title="Phantom Mire",
                job="Pursuit",
                targetBand="Hard",
                site="Phantom Mire",
                summary="Shallow pool swallow; lights guide Bloom.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t2-f13-haven",
                floors="13",
                title="Rootlight Quarantine Scene",
                job="Choosing",
                targetBand="Routine→Standard",
                site="Rootlight Sanctuary",
                summary="Social survival stakes around burn/water law.",
                detailedActorBudget="0–2",
            ),
            card(
                id="t2-f14-15-reliquary",
                floors="14–15",
                title="Overgrown Reliquary",
                job="Revealing",
                targetBand="Standard→Hard",
                site="Overgrown Reliquary",
                rosterRef="t2-reliquary",
                detailedActorBudget="4–6",
            ),
            card(
                id="t2-f18-lurk",
                floors="18",
                title="Lurkwell Approach",
                job="Taxing",
                targetBand="Standard",
                site="Lurkwell Refuge",
                summary="Islet rest; lichen dimming as warning.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t2-f20-seal",
                floors="20",
                title="Sporemist Gate + Bloom",
                job="Climactic",
                targetBand="Hard→Severe",
                site="Sporemist Gate",
                rosterRef="t2-bloom-seal",
                detailedActorBudget="1–3",
            ),
        ],
    }
)

# ----- Tier 3 -----
tiers.append(
    {
        "tier": 3,
        "zone": "Anvil of Brogi",
        "floors": "21–30",
        "guardian": "Ashthirst the Hollow",
        "corePressures": [
            "Heat budget",
            "Timing cycles",
            "Equipment stress",
            "Production claims",
        ],
        "gatePrep": "Key forged in Quenching Pool bears material provenance consequences.",
        "faunaRoles": [
            "forge spirits",
            "empty armor bodies",
            "slag beasts",
            "heat mephits",
            "contractors",
        ],
        "sampleRosters": [
            roster(
                "t3-hammerfall",
                "Hammerfall Timing Fight (F21)",
                "Teaching",
                "Standard→Hard",
                [
                    actor("Magma Mephit", 3, "skirmisher", "Magma Mephit", "2", "2"),
                    actor("Steam Mephit", 2, "controller", "Steam Mephit", "2", "2"),
                    actor(
                        "Earth Elemental Myrmidon",
                        1,
                        "brute",
                        "Earth Elemental Myrmidon",
                        "6",
                        "6",
                    ),
                ],
                abstract=["Hammer cycle: falls every 3 rounds — terrain EV, not a 9th actor"],
                levers={
                    "player": "Act on stated cycle; brace or bait under hammer",
                    "director": "Skip a hammer beat if party earned timing mastery",
                    "exit": "Cooling alcove toward Emberrest",
                },
                notes="State the cycle before asking for action.",
            ),
            roster(
                "t3-rivetworks",
                "Rivetworks Patrol (F26)",
                "Taxing",
                "Hard",
                [
                    actor(
                        "Iron Cobra",
                        2,
                        "skirmisher",
                        "Iron Cobra",
                        "7",
                        "5–7",
                        note="Type may be sandbox — treat as Construct serpent",
                    ),
                    actor(
                        "Fire Elemental Myrmidon",
                        1,
                        "brute",
                        "Fire Elemental Myrmidon",
                        "8",
                        "8",
                    ),
                    actor(
                        "Hellfire Engine",
                        1,
                        "controller",
                        "Hellfire Engine",
                        "7",
                        "7",
                    ),
                ],
                levers={
                    "player": "Redirect pour / stop line",
                    "director": "Unfinished Legion production reacts to nearby conflict",
                    "exit": "Gearspark Forge haven (F27)",
                },
                notes="Max 4 detailed + hazard cycles.",
            ),
            roster(
                "t3-ashthirst",
                "Ashthirst the Hollow (F30)",
                "Climactic",
                "Severe",
                [
                    actor(
                        "Ashthirst the Hollow",
                        1,
                        "seal/guardian",
                        "Ashthirst the Hollow",
                        "14",
                        "14",
                    )
                ],
                abstract=["Quench-key quality as phase lever"],
                levers={
                    "player": "Honest materials in key forge",
                    "director": "Hollow tests creation vs spent heat",
                    "exit": "Partial quench opens with lasting forge debt",
                },
                notes="Elemental / Huge / CR 14 / NE — Gate Guardian.",
            ),
        ],
        "encounterCards": [
            card(
                id="t3-f21-hammer",
                floors="21",
                title="Hammerfall Hall",
                job="Teaching",
                targetBand="Standard→Hard",
                site="Hammerfall Hall",
                rosterRef="t3-hammerfall",
                detailedActorBudget="4–6",
            ),
            card(
                id="t3-f22-river",
                floors="22",
                title="Molten River Crossing",
                job="Taxing",
                targetBand="Hard",
                site="Molten River Crossing",
                summary="Heat budget + timed causeway.",
                detailedActorBudget="2–4",
                hazard="White-hot current",
            ),
            card(
                id="t3-f23-ember",
                floors="23",
                title="Emberrest Pause",
                job="Choosing",
                targetBand="Routine",
                site="Emberrest Alcove",
                summary="Cooling / repair; social forge politics.",
                detailedActorBudget="0–2",
            ),
            card(
                id="t3-f24-anvil",
                floors="24",
                title="Chained Anvil Chamber",
                job="Pursuit",
                targetBand="Hard",
                site="Chained Anvil Chamber",
                summary="Slow-arc crush; timing objective.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t3-f26-rivet",
                floors="26",
                title="Rivetworks Maze",
                job="Taxing",
                targetBand="Hard",
                site="Rivetworks Maze",
                rosterRef="t3-rivetworks",
                detailedActorBudget="4",
            ),
            card(
                id="t3-f27-gearspark",
                floors="27",
                title="Gearspark Claim Dispute",
                job="Choosing",
                targetBand="Standard",
                site="Gearspark Forge",
                summary="Tools, formulas, ownership.",
                detailedActorBudget="2–5",
            ),
            card(
                id="t3-f30-seal",
                floors="30",
                title="Lavaflow Gate + Ashthirst",
                job="Climactic",
                targetBand="Severe",
                site="Lavaflow Gate",
                rosterRef="t3-ashthirst",
                detailedActorBudget="1",
            ),
        ],
    }
)

# ----- Tier 4 -----
tiers.append(
    {
        "tier": 4,
        "zone": "Isles of Eternal Radiance",
        "floors": "31–40",
        "guardian": "Gor Vekk, Architect of Ends",
        "corePressures": [
            "Exposure",
            "Reflection / doubles",
            "Distance / moving bridges",
            "Publicity of actions",
        ],
        "gatePrep": "Three sun-shards = beginnings / continuations / endings; charging method shapes Guardian stance.",
        "faunaRoles": [
            "light-forged constructs",
            "mirror doubles",
            "shade markets",
            "radiant flora guardians",
        ],
        "sampleRosters": [
            roster(
                "t4-bridge",
                "Shifting Bridge Skirmish (F31)",
                "Taxing",
                "Hard",
                [
                    actor(
                        "Lumen Drifter",
                        2,
                        "skirmisher",
                        "Lumen Drifter",
                        "6",
                        "6",
                        note="Lore-scrub rename (ex-Flumph)",
                    ),
                    actor(
                        "Slithering Tracker",
                        1,
                        "controller",
                        "Slithering Tracker",
                        "9",
                        "7–9",
                    ),
                    actor(
                        "Swarm of Bats (light-maddened)",
                        1,
                        "swarm",
                        "Swarm of Bats",
                        "9",
                        "6–8",
                        True,
                        "CR may be high — reskin to CR 3–4 swarm if needed",
                    ),
                ],
                abstract=["Bridge angle shift every 2 rounds as terrain clock"],
                levers={
                    "player": "Spend shade vial for safe crossing",
                    "director": "Double appears if mirror surface disturbed",
                    "exit": "Sunward Terrace if route invested",
                },
                notes="Avoid radiant immunity on every foe.",
            ),
            roster(
                "t4-mirror",
                "Mirror Reef Doubles (F34)",
                "Choosing",
                "Hard",
                [
                    actor(
                        "Party Double (reskin)",
                        2,
                        "mirror threat",
                        "Allip",
                        "5",
                        "5–7",
                        note="Reskin Allip as radiant echo-double",
                    ),
                    actor("Cloaker", 1, "controller", "Cloaker", "10", "8–10"),
                    actor("Lumen Drifter", 1, "skirmisher", "Lumen Drifter", "6", "6"),
                ],
                levers={
                    "player": "Break line of sight / rename identity marks",
                    "director": "Doubles prioritize exposed names",
                    "exit": "Dawn's Refuge under shade contract",
                },
                notes="Reflection complicates identity — job is Choosing.",
            ),
            roster(
                "t4-gorvekk",
                "Gor Vekk, Architect of Ends (F40)",
                "Climactic",
                "Severe",
                [
                    actor(
                        "Gor Vekk, Architect of Ends",
                        1,
                        "seal/guardian",
                        "Gor Vekk, Architect of Ends",
                        "17",
                        "17",
                    )
                ],
                abstract=[
                    "Projection fight may use reduced HP — full CR 17 is seal budget (bestiary note)"
                ],
                levers={
                    "player": "Shard charging choices alter Architect stance",
                    "director": "Perfect conclusion cost — complete / preserve / erase",
                    "exit": "Unfinished ending leaves Gate ajar with story debt",
                },
                notes="Aberration / Large / CR 17 / LE — Gate Guardian.",
            ),
        ],
        "encounterCards": [
            card(
                id="t4-f31-prism",
                floors="31",
                title="Prismatic Archipelago",
                job="Taxing",
                targetBand="Hard",
                site="Prismatic Archipelago",
                rosterRef="t4-bridge",
                detailedActorBudget="4",
            ),
            card(
                id="t4-f32-gardens",
                floors="32",
                title="Radiant Bloom Gardens",
                job="Choosing",
                targetBand="Standard→Hard",
                site="Radiant Bloom Gardens",
                summary="Harvest tonic vs patrol; Resource vs Combat.",
                detailedActorBudget="3–5",
            ),
            card(
                id="t4-f33-sunward",
                floors="33",
                title="Sunward Terrace Politics",
                job="Revealing",
                targetBand="Routine→Standard",
                site="Sunward Terrace",
                detailedActorBudget="0–3",
            ),
            card(
                id="t4-f34-mirror",
                floors="34",
                title="Mirror Reef",
                job="Choosing",
                targetBand="Hard",
                site="Mirror Reef",
                rosterRef="t4-mirror",
                detailedActorBudget="4",
            ),
            card(
                id="t4-f36-obelisk",
                floors="36",
                title="Sunforged Obelisk",
                job="Revealing",
                targetBand="Standard",
                site="Sunforged Obelisk",
                summary="Glyph rings; emergency gear grotto.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t4-f37-dawn",
                floors="37",
                title="Dawn's Refuge",
                job="Taxing",
                targetBand="Standard",
                site="Dawn's Refuge",
                summary="Heat-fatigue cleanse before Gate.",
                detailedActorBudget="1–3",
            ),
            card(
                id="t4-f40-seal",
                floors="40",
                title="Radiance Gate + Gor Vekk",
                job="Climactic",
                targetBand="Severe",
                site="Radiance Gate",
                rosterRef="t4-gorvekk",
                detailedActorBudget="1",
            ),
        ],
    }
)

# ----- Tier 5 -----
tiers.append(
    {
        "tier": 5,
        "zone": "Sanctum of Echoing Choirs",
        "floors": "41–50",
        "guardian": "Choralith, Voice Below",
        "corePressures": [
            "Sound discipline",
            "Composure / passivity",
            "Accumulated wear",
            "Witnessed memory",
        ],
        "gatePrep": (
            "Four-note Canticle necessary but insufficient — teams hold distinct "
            "notes/silences while Guardian harmonizes toward obedience."
        ),
        "barOfLastRefuge": "Cultural soft quit — professionalism, not cowardice. Distinct from Horn PoNR (1200h).",
        "faunaRoles": [
            "tone-wardens",
            "echo archives",
            "composure predators",
            "silence brokers",
        ],
        "sampleRosters": [
            roster(
                "t5-pillars",
                "Whispering Pillars Test (F41)",
                "Teaching",
                "Hard",
                [
                    actor(
                        "Dust Mephit (echo dust)",
                        2,
                        "skirmisher",
                        "Dust Mephit",
                        "5",
                        "5",
                    ),
                    actor(
                        "Smoke Mephit (choir smoke)",
                        1,
                        "controller",
                        "Smoke Mephit",
                        "9",
                        "7–9",
                    ),
                    actor(
                        "Voidmind Archivist",
                        1,
                        "controller",
                        "Voidmind Archivist",
                        "1/2",
                        "6–8",
                        True,
                        "Excel CR 1/2 is sandbox — scale to CR 6–8 tone-warden",
                    ),
                    actor("Banderhobb", 1, "brute", "Banderhobb", "3", "3–5"),
                ],
                abstract=[
                    "Sound discipline track: failed whispers promote +1 detailed echo"
                ],
                levers={
                    "player": "Map acoustics with thrown stones / cantrips",
                    "director": "Calm passivity as trap — Soft quit pressure",
                    "exit": "Bar of Last Refuge (F43)",
                },
                notes="Do not require real singing talent.",
            ),
            roster(
                "t5-reliquary",
                "Resonant Reliquary Chorus (F44)",
                "Revealing",
                "Hard→Severe",
                [
                    actor(
                        "Gibbering Mouther (dissonant choir)",
                        1,
                        "controller",
                        "Gibbering Mouther",
                        "12",
                        "10–12",
                        note="Type field may be wrong — treat as Aberration sound-horror",
                    ),
                    actor("Voidmind", 1, "controller", "Voidmind", "11", "11"),
                    actor(
                        "Smoke Mephit",
                        2,
                        "skirmisher",
                        "Smoke Mephit",
                        "9",
                        "6–8",
                        True,
                    ),
                ],
                levers={
                    "player": "Open one ossuary only; preserve vs weaponize echo",
                    "director": "Chorus calms or fractures — player choice",
                    "exit": "Cantor's Archive (F47)",
                },
                notes="Keep ≤4–5 detailed under eight-actor with party.",
            ),
            roster(
                "t5-choralith",
                "Choralith, Voice Below (F50)",
                "Climactic",
                "Severe→Catastrophic",
                [
                    actor(
                        "Choralith, Voice Below",
                        1,
                        "seal/guardian",
                        "Choralith, Voice Below",
                        "20",
                        "20",
                    )
                ],
                abstract=[
                    "Four-note team objectives as off-map / parallel seat checks"
                ],
                levers={
                    "player": "Shared signal without erasing individual voices",
                    "director": "Harmonize-toward-obedience phase — not HP wall only",
                    "exit": "Bar retreat remains honorable until Gate commit",
                },
                notes="Aberration / Large / CR 20 / N — Gate Guardian. Soft quit ≠ Horn.",
            ),
        ],
        "encounterCards": [
            card(
                id="t5-f41-pillars",
                floors="41",
                title="Whispering Pillars",
                job="Teaching",
                targetBand="Hard",
                site="Whispering Pillars",
                rosterRef="t5-pillars",
                detailedActorBudget="4–5",
            ),
            card(
                id="t5-f42-aeolian",
                floors="42",
                title="Aeolian Mirror Pools",
                job="Choosing",
                targetBand="Hard",
                site="Aeolian Mirror Pools",
                summary="Rippling arias twist reality.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t5-f43-bar",
                floors="43",
                title="Bar of Last Refuge",
                job="Choosing",
                targetBand="Routine (social)",
                site="Bar of Last Refuge",
                summary="Memorial walls, brokers, respectable withdrawal.",
                detailedActorBudget="0–2",
            ),
            card(
                id="t5-f44-reliquary",
                floors="44",
                title="Resonant Reliquary",
                job="Revealing",
                targetBand="Hard→Severe",
                site="Resonant Reliquary",
                rosterRef="t5-reliquary",
                detailedActorBudget="4",
            ),
            card(
                id="t5-f46-acappella",
                floors="46",
                title="A Cappella Alcove",
                job="Taxing",
                targetBand="Hard",
                site="A Cappella Alcove",
                summary="Devices silent; voice/stillness triggers statues.",
                detailedActorBudget="3–5",
            ),
            card(
                id="t5-f47-cantor",
                floors="47",
                title="Cantor's Archive",
                job="Revealing",
                targetBand="Standard",
                site="Cantor's Archive",
                summary="Tone-stones vs dissonance.",
                detailedActorBudget="1–3",
            ),
            card(
                id="t5-f50-seal",
                floors="50",
                title="Canticle Gate + Choralith",
                job="Climactic",
                targetBand="Severe→Catastrophic",
                site="Canticle Gate",
                rosterRef="t5-choralith",
                detailedActorBudget="1",
            ),
        ],
    }
)

toolkit["tiers"] = tiers

text = json.dumps(toolkit, indent=2, ensure_ascii=False) + "\n"
(out1 := root / "src" / "data" / "t1-5-encounter-toolkit.json").write_text(
    text, encoding="utf-8"
)
(out2 := root / "scripts" / "t1-5-encounter-toolkit.json").write_text(
    text, encoding="utf-8"
)
print("wrote", out1)
print("wrote", out2)
print(
    "cards",
    sum(len(t["encounterCards"]) for t in tiers),
    "rosters",
    sum(len(t["sampleRosters"]) for t in tiers),
)
