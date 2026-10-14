# One-shot builder for T6–10 encounter operational toolkit JSON.
# Run: python scripts/_build_t6_10_encounter_toolkit.py
# Mirrors scripts/_build_t1_5_encounter_toolkit.py for floors 51–100.
# Does NOT rewrite bestiary combat stats.

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
        "id": "t6-10-encounter-toolkit",
        "title": "Tier 6–10 Encounter Operational Toolkit",
        "stamped": "2026-07-31",
        "status": "director-ops draft — EV/threat budgets; not an XP economy; T6–10 floors remain draft-mapped in floor-encounters",
        "sources": [
            "docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx (Ch 15 EV, Ch 16 eight-actor, Ch 29 workflow, Part IX Ch 63–68 T6–10 ops, Old God Interstice Ch 65)",
            "src/data/floor-encounters.json (T6–10 draft zones, havens, POIs, live Guardian bosses)",
            "docs/mechanics/BESTIARY_LORE_PASS_2026-07-30.md + src/bestiary_data_full.json (Guardian CR/Type only — combat blocks may still be draft)",
            "docs/mechanics/XP_ADVANCEMENT_CANON.md (awards BLOCKED)",
            "docs/manuals/Instruments_of_the_Weave.md (T6–10 d8 pressure tables)",
            "docs/mechanics/T1_5_ENCOUNTERS_2026-07-31.md (pattern predecessor)",
        ],
        "canonLocks": {
            "openingHours": 2400,
            "hornPoNRHours": 1200,
            "expeditionMax": 12,
            "umbrinNotDrow": True,
            "noSwtor": True,
            "gateGuardianLiveNamesOnly": True,
            "oldGodIntersticeNotGateGuardian": True,
            "civilizationLineEndsAtTier6": True,
        },
        "xpStance": (
            "XP award rules remain BLOCKED (thresholds exist; CR→XP / encounter XP budgets "
            "are not canon). This toolkit uses bible EV / incoming-pressure bands and the "
            "eight-actor rule only. Milestone / narrative advancement assumed. Do not invent "
            "a second XP economy."
        ),
    },
    "tierFloorMap": [
        {
            "tier": 6,
            "floors": [51, 60],
            "floorsLabel": "51–60",
            "zone": "Crossroads of the Shattered Thread",
            "guardian": "Lumen of the Shattered Thread",
            "gate": "Lumen Gate (end Floor 60)",
            "difficulty": "Adept",
            "mapped": False,
            "note": "Last depth where stable small civilizations remain normal (bible Ch 31 / Ch 63).",
        },
        {
            "tier": 7,
            "floors": [61, 70],
            "floorsLabel": "61–70",
            "zone": "Pactbound Arena",
            "guardian": "Xarog, the Pactbound Furnace",
            "gate": "Furnace Gate (end Floor 70)",
            "difficulty": "Veteran",
            "mapped": False,
            "note": "Old God Interstice sits after Xarog / before Eirfax — not a Gate Guardian.",
        },
        {
            "tier": 8,
            "floors": [71, 80],
            "floorsLabel": "71–80",
            "zone": "Duskshard Pools",
            "guardian": "Eirfax, the Dusk Crowned",
            "gate": "Crown Gate (end Floor 80)",
            "difficulty": "Elite",
            "mapped": False,
        },
        {
            "tier": 9,
            "floors": [81, 90],
            "floorsLabel": "81–90",
            "zone": "Veiled Iron Spiral",
            "guardian": "Threxus, the Iron Spiral",
            "gate": "Spiral Gate (end Floor 90)",
            "difficulty": "Mythic",
            "mapped": False,
        },
        {
            "tier": 10,
            "floors": [91, 100],
            "floorsLabel": "91–100",
            "zone": "Silencebound Void",
            "guardian": "The Marquis of Silence",
            "gate": "Marquis Gate (end Floor 100)",
            "difficulty": "Legendary",
            "mapped": False,
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
            "Interstice": "Prefer identity/memory/route pressure over raw damage; ≤8 detailed if any combat forms",
        },
        "tierThreatNotes": [
            {
                "tier": 6,
                "defaultBand": "Hard",
                "notes": (
                    "Route / witness / anchor politics are primary tax. Civilization rivalry can "
                    "substitute for HP fights. Seal = Hard→Severe with path-choice Recognition."
                ),
            },
            {
                "tier": 7,
                "defaultBand": "Hard→Severe",
                "notes": (
                    "Every fight carries a term. Winning combat while losing the stated claim is "
                    "valid. Seal leaves ≥1 binding term for Tier 8. Interstice after Gate is not XP."
                ),
            },
            {
                "tier": 8,
                "defaultBand": "Severe",
                "notes": (
                    "Delayed identity / reflection leverage. Settlements are exceptional. Seal "
                    "tests which version of the Expedition deserves continuity."
                ),
            },
            {
                "tier": 9,
                "defaultBand": "Severe",
                "notes": (
                    "False progress + compression. Circular strategies strengthen Threxus. Use "
                    "transformation anchors, not distance marks."
                ),
            },
            {
                "tier": 10,
                "defaultBand": "Severe→Catastrophic",
                "notes": (
                    "Anti-resonance + stillness offer. Marquis may be defeated, replaced, persuaded, "
                    "bound, or transformed — not a pure HP wall. Silent Ones: never name aloud."
                ),
            },
        ],
    },
    "gateGuardiansT6to10": [
        {
            "tier": 6,
            "name": "Lumen of the Shattered Thread",
            "type": "Elemental",
            "size": "Large",
            "challengeRating": "22",
            "xpField": 41000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award until XP_ADVANCEMENT_CANON resolves",
            "alignment": "Chaotic Neutral",
            "zoneFound": "Crossroads of the Shattered Thread",
            "sealFloor": 60,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 7,
            "name": "Xarog, the Pactbound Furnace",
            "type": "Fiend",
            "size": "Huge",
            "challengeRating": "24",
            "xpField": 62000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Lawful Evil",
            "zoneFound": "Pactbound Arena",
            "sealFloor": 70,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 8,
            "name": "Eirfax, the Dusk Crowned",
            "type": "Fey",
            "size": "Medium",
            "challengeRating": "26",
            "xpField": 90000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Neutral Evil",
            "zoneFound": "Duskshard Pools",
            "sealFloor": 80,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 9,
            "name": "Threxus, the Iron Spiral",
            "type": "Construct",
            "size": "Gargantuan",
            "challengeRating": "28",
            "xpField": 120000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Lawful Neutral",
            "zoneFound": "Veiled Iron Spiral",
            "sealFloor": 90,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
        {
            "tier": 10,
            "name": "The Marquis of Silence",
            "type": "Fiend",
            "size": "Huge",
            "challengeRating": "30",
            "xpField": 155000,
            "xpFieldNote": "Bestiary xp field present; NOT a canon award",
            "alignment": "Chaotic Evil",
            "zoneFound": "Silencebound Void",
            "sealFloor": 100,
            "tags": "Gate Guardian",
            "combatDraft": True,
        },
    ],
    "oldGodInterstice": {
        "placement": "Between Tier 7 (after Furnace Gate / Xarog) and Tier 8 (before Duskshard Pools / Eirfax)",
        "isGateGuardian": False,
        "bibleChapter": "Director bible Ch 65 — Operating the Old God Interstice",
        "pressure": "Identity, memory, and route pressure over raw damage",
        "note": (
            "Not an eleventh tier, not a Gate Guardian, not ordinary floor content. "
            "Do not put Old God on the live Guardian roster. Live roster only: Lumen, Xarog, "
            "Eirfax, Threxus, Marquis (plus T1–5)."
        ),
    },
    "bestiaryCaveat": (
        "Trash/zone fauna in bestiary_data_full.json often has sandbox Type/CR/zoneFound "
        "mismatches. Rosters prefer lore-scrubbed names that exist post BESTIARY_LORE_PASS "
        "and state intendedCrBand for EV planning. When excel CR is absurd, use bible Ch 17 "
        "reskin from a same-band template. Never use SWTOR names. Prefer Umbrin over any "
        "residual Drow labels. Do not rewrite bestiary combat stats from this toolkit."
    ),
    "inventoryExisting": {
        "floorEncountersJson": {
            "path": "src/data/floor-encounters.json",
            "has": "T6–10 draft zones (mapped:false), havens, POIs, live Guardian bosses; T1–5 mapped",
        },
        "directorOpsT6to10": {
            "path": "Director bible Part IX Ch 63–68 (+ Ch 65 Interstice)",
            "has": "Tier purposes, core pressures, revelation ceilings, gate prep, sample floor seeds",
        },
        "t1to5Toolkit": {
            "path": "src/data/t1-5-encounter-toolkit.json",
            "has": "Shipped pattern this file mirrors",
        },
        "instrumentsPressure": {
            "path": "docs/manuals/Instruments_of_the_Weave.md Part X",
            "has": "d8 compressed pressure tables T6–10",
        },
        "monstersLibrary": {
            "path": "src/components/MonstersLibrary.tsx + src/bestiary_data_full.json",
            "has": "Gate Guardians T6–10 tagged with lore-pass CR; trash combat often draft/sandbox",
        },
    },
}

tiers = []

# ----- Tier 6 -----
tiers.append(
    {
        "tier": 6,
        "zone": "Crossroads of the Shattered Thread",
        "floors": "51–60",
        "guardian": "Lumen of the Shattered Thread",
        "corePressures": [
            "Route instability / Path Recall",
            "Causal disagreement between truthful accounts",
            "Political navigation of floor civilizations (last normal depth)",
            "Separation into neighboring non-identical nodes",
            "Weave-Snap / Lantern Doubt",
        ],
        "opsChapter": {
            "status": "Director bible Ch 63 operational guidance (not room-by-room keys)",
            "sampleSeed": "The City of Two Afternoons — dual treaty histories on same streets",
            "gatePrep": (
                "Lumen tests choosing one path without denying paths not taken; "
                "outcome-echoes / shared-crossing recognition"
            ),
        },
        "faunaRoles": [
            "thread-wraith echoes",
            "civic enforcers / route auditors",
            "weave-static scavengers",
            "rival cartographers",
        ],
        "sampleRosters": [
            roster(
                "t6-crossroads-tax",
                "Shattered Crossroads Stir (F51)",
                "Teaching",
                "Hard",
                [
                    actor(
                        "Thread Wraith",
                        2,
                        "skirmisher/controller",
                        "Allip",
                        "5",
                        "8–10",
                        True,
                        "Display as Weave-echo; excel CR often sandbox — scale to deep-tier band",
                    ),
                    actor(
                        "Lantern Doubt Will-o'",
                        2,
                        "skirmisher",
                        "Will-o-wisp",
                        "7",
                        "5–7",
                        True,
                        "False-path lure; Ch 17 reskin if CR absurd",
                    ),
                ],
                abstract=["Path Recall clock: looking back → route rewrite in 1–2 rounds"],
                levers={
                    "player": "Declare anchor statement (who/from where/carrying what) to stabilize fight space",
                    "director": "One wraith phases out if party accepts a rival map condition",
                    "exit": "Threadbare Camp approach corridor (F53 rumor)",
                },
                notes="Teach that maps need anchors. Keep ≤4 detailed for Combat team of 4.",
            ),
            roster(
                "t6-civic-extraction",
                "Academic Faction Extraction (F55 Lumen's Cross)",
                "Choosing",
                "Hard→Severe",
                [
                    actor(
                        "Void Broker negotiator",
                        1,
                        "controller",
                        "Void Broker",
                        "6",
                        "10–12",
                        True,
                    ),
                    actor(
                        "Umbrin Shadowblade escort",
                        2,
                        "skirmisher",
                        "Umbrin Shadowblade",
                        "7",
                        "8–10",
                        note="Umbrin demonym — never Drow",
                    ),
                    actor(
                        "Shield Guardian parcel-guard",
                        1,
                        "brute",
                        "Shield Guardian",
                        "6",
                        "10–12",
                        True,
                    ),
                ],
                abstract=[
                    "Off-map: Research seat translates rival civilization's map conditions",
                    "Morale: escorts withdraw if broker gets the thread sample",
                ],
                levers={
                    "player": "Sell sample / steal / forge shared crossing rights",
                    "director": "Two civilizations remember different winners unless witnesses agree",
                    "exit": "Quiet Deep Thread-Well rumor route (unmapped — costly)",
                },
                notes="Political win can skip combat. ≤8 detailed.",
            ),
            roster(
                "t6-lumen-seal",
                "Lumen Gate — Lumen of the Shattered Thread (F60)",
                "Climactic",
                "Hard→Severe",
                [
                    actor(
                        "Lumen of the Shattered Thread",
                        1,
                        "seal/guardian",
                        "Lumen of the Shattered Thread",
                        "22",
                        "22",
                    ),
                    actor(
                        "Outcome-Echo (arena feature)",
                        2,
                        "hazard-actor",
                        note="Count toward eight-actor only if they act each round; else terrain/Recognition lever",
                    ),
                ],
                abstract=[
                    "Recognition: choose one path without denying others",
                    "Civilization witness clock — need ≥1 culture to recognize shared crossing",
                ],
                levers={
                    "player": "Sacrifice a possible future / bind shared crossing",
                    "director": "Do not silent-fudge; echoes punish contradictory denial",
                    "exit": "Yield to Threadbare Camp if seal condition unmet — civilization line still open",
                },
                notes="Elemental / Large / CR 22 / CN — Gate Guardian. Past Lumen Gate, stable civilization ends.",
            ),
        ],
        "encounterCards": [
            card(
                id="t6-f51-crossroads",
                floors="51",
                title="Shattered Crossroads",
                job="Teaching",
                targetBand="Hard",
                site="Shattered Crossroads",
                summary="Footprints fade; half-real pathways. First deep route-discipline fight.",
                detailedActorBudget="3–5",
                rosterRef="t6-crossroads-tax",
                hazard="Path Recall",
            ),
            card(
                id="t6-f52-thread-fork",
                floors="52",
                title="Thread-Fork Galleries",
                job="Taxing",
                targetBand="Hard",
                site="Thread-Fork Galleries",
                summary="Corridors split/rejoin; party may occupy neighboring nodes.",
                detailedActorBudget="3–6",
                hazard="Separation — Support/Research seats off-map",
            ),
            card(
                id="t6-f53-haven",
                floors="53",
                title="Threadbare Camp Politics",
                job="Choosing",
                targetBand="Standard (social)→Hard",
                site="Threadbare Camp",
                summary="Last-tier haven rumor; crossing rights vs hospitality.",
                detailedActorBudget="0–4",
            ),
            card(
                id="t6-f55-lumens-cross",
                floors="55",
                title="Lumen's Cross Junction",
                job="Choosing",
                targetBand="Hard→Severe",
                site="Lumen's Cross",
                summary="All paths seem to arrive at once; academic extraction / rival cartographers.",
                detailedActorBudget="4–6",
                rosterRef="t6-civic-extraction",
            ),
            card(
                id="t6-f56-two-afternoons",
                floors="56",
                title="City of Two Afternoons",
                job="Revealing",
                targetBand="Hard",
                site="Ch 63 sample seed",
                summary="Dual treaty histories; witnesses affect both versions.",
                detailedActorBudget="2–5",
                hazard="Causal disagreement as EV (non-HP) tax",
            ),
            card(
                id="t6-f58-weave-snap",
                floors="58",
                title="Weave-Snap Shear",
                job="Taxing",
                targetBand="Severe",
                site="Deep Thread-Fork",
                summary="Brief planar shear; disorientation before seal approach.",
                detailedActorBudget="3–5",
                hazard="Weave-Snap",
            ),
            card(
                id="t6-f60-seal",
                floors="60",
                title="Lumen Gate + Lumen",
                job="Climactic",
                targetBand="Hard→Severe",
                site="Lumen Gate",
                rosterRef="t6-lumen-seal",
                detailedActorBudget="1–3",
            ),
        ],
    }
)

# ----- Tier 7 -----
tiers.append(
    {
        "tier": 7,
        "zone": "Pactbound Arena",
        "floors": "61–70",
        "guardian": "Xarog, the Pactbound Furnace",
        "corePressures": [
            "Oath accumulation (leverage / fuel / restriction)",
            "Audience / witnessed terms",
            "Escalating stakes after victories",
            "Identity as office (titles > personal names)",
            "Pact Rewrite / Blood-Tally / Arena Echo",
        ],
        "opsChapter": {
            "status": "Director bible Ch 64 operational guidance",
            "sampleSeed": "The Empty Grandstand — applause of erased Expeditions",
            "gatePrep": (
                "Xarog burns false/impossible/contradictory obligations; passage leaves "
                "≥1 binding term that matters in Tier 8"
            ),
            "intersticeAfter": "Ch 65 Old God Interstice — not a Gate Guardian",
        },
        "faunaRoles": [
            "arena challengers under stated terms",
            "pact-devil observers",
            "oath-echo remnants",
            "furnace auditors",
        ],
        "sampleRosters": [
            roster(
                "t7-coliseum-open",
                "Pactbound Coliseum Opening Bout (F61)",
                "Teaching",
                "Hard",
                [
                    actor(
                        "Pact Devil (White Court) adjudicator",
                        1,
                        "controller",
                        "Pact Devil (White Court)",
                        "7",
                        "12–14",
                        True,
                        "Witness / term enforcer — not necessarily a damage race",
                    ),
                    actor(
                        "Barbed Devil challenger",
                        2,
                        "brute",
                        "Barbed Devil",
                        "10",
                        "12–14",
                        True,
                    ),
                ],
                abstract=["Crowd favor clock as morale/rep swing (Instruments d8)"],
                levers={
                    "player": "Win the stated contest objective, not just HP",
                    "director": "Write the term before initiative; both sides may exploit wording",
                    "exit": "Refuse challenge publicly — costs favor, keeps oath clean",
                },
                notes="Contest + term. Keep ≤4 detailed.",
            ),
            roster(
                "t7-empty-grandstand",
                "Empty Grandstand Claim (F65–67)",
                "Choosing",
                "Severe",
                [
                    actor(
                        "Arena Echo (erased Expedition)",
                        3,
                        "skirmisher",
                        "Fracture-Kin Shadow Demon",
                        "11",
                        "12–15",
                        True,
                        "Scrubbed Fracture-Kin name; applause transfers unfinished claim",
                    ),
                    actor(
                        "Chain Devil binder",
                        1,
                        "controller",
                        "Chain Devil",
                        "10",
                        "14–16",
                        True,
                    ),
                ],
                abstract=["Accepting acclaim = power + inherited unfinished Pact claim"],
                levers={
                    "player": "Accept / refuse / renegotiate whose claim you inherit",
                    "director": "Power without term clarity becomes Xarog fuel later",
                    "exit": "Oathbreaker's Nook (F64) if fight abandoned mid-term",
                },
                notes="Ch 64 sample seed pressure. ≤8 detailed.",
            ),
            roster(
                "t7-xarog-seal",
                "Furnace Gate — Xarog, the Pactbound Furnace (F70)",
                "Climactic",
                "Severe",
                [
                    actor(
                        "Xarog, the Pactbound Furnace",
                        1,
                        "seal/guardian",
                        "Xarog, the Pactbound Furnace",
                        "24",
                        "24",
                    ),
                    actor(
                        "Oath Plate (arena feature)",
                        1,
                        "hazard-actor",
                        note="Burns contradictory obligations; treat as terrain unless acting each round",
                    ),
                ],
                abstract=[
                    "Inventory of party promises as off-map track",
                    "One binding term must survive into Tier 8",
                ],
                levers={
                    "player": "Choose which promises become permanent",
                    "director": "False/impossible oaths feed the Furnace — do not invent silent XP",
                    "exit": "Yield with unfinished claim — Arena remembers wording",
                },
                notes="Fiend / Huge / CR 24 / LE — Gate Guardian. Interstice may follow; not automatic.",
            ),
            roster(
                "t7-interstice-room",
                "Old God Interstice — Room With One History (post-F70)",
                "Interstice",
                "Severe (identity/memory; not HP)",
                [
                    actor(
                        "History Collapse (arena feature)",
                        1,
                        "hazard-actor",
                        note="Not a Gate Guardian. Prefer seat checks over monster stats.",
                    ),
                    actor(
                        "Difference Warden echo",
                        2,
                        "controller",
                        "Voidmind",
                        "11",
                        "14–16",
                        True,
                        "Optional combat form if table needs initiative — scrubbed aberration",
                    ),
                ],
                abstract=[
                    "Three layers: perceptible / operational / interpretive",
                    "Record what certainty each PC lost and what difference they refuse to surrender",
                ],
                levers={
                    "player": "Preserve contradictory truths; carry one another's memories",
                    "director": "Keep ≥2 plausible readings of the Old God alive",
                    "exit": "Crossing creates campaign language for Tier 8 — not a seal unlock alone",
                },
                notes="Ch 65. NOT on Guardian roster. No silent cosmology dump.",
            ),
        ],
        "encounterCards": [
            card(
                id="t7-f61-coliseum",
                floors="61",
                title="Pactbound Coliseum",
                job="Teaching",
                targetBand="Hard",
                site="Pactbound Coliseum",
                summary="Contest + term on day one. Audience validates wording.",
                detailedActorBudget="3–4",
                rosterRef="t7-coliseum-open",
            ),
            card(
                id="t7-f63-oath-post",
                floors="63",
                title="Oath-Post Ring",
                job="Revealing",
                targetBand="Hard",
                site="Oath-Post Ring",
                summary="Verbal bargains bind before blood; write terms down.",
                detailedActorBudget="1–3",
                hazard="Pact Rewrite",
            ),
            card(
                id="t7-f64-haven",
                floors="64",
                title="Oathbreaker's Nook",
                job="Choosing",
                targetBand="Routine (social)→Hard",
                site="Oathbreaker's Nook",
                summary="Broken pact-runes briefly repel rewrites; speak carefully.",
                detailedActorBudget="0–3",
            ),
            card(
                id="t7-f66-grandstand",
                floors="66",
                title="Empty Grandstand",
                job="Choosing",
                targetBand="Severe",
                site="Ch 64 sample seed",
                rosterRef="t7-empty-grandstand",
                detailedActorBudget="4–5",
            ),
            card(
                id="t7-f68-furnace-tier",
                floors="68",
                title="Furnace Tier Heat Audit",
                job="Taxing",
                targetBand="Hard→Severe",
                site="Furnace Tier",
                summary="Heat pools; auditor challenges unfinished claims.",
                detailedActorBudget="3–6",
                hazard="Blood-Tally rumor — presentation, confirm at table",
            ),
            card(
                id="t7-f70-seal",
                floors="70",
                title="Furnace Gate + Xarog",
                job="Climactic",
                targetBand="Severe",
                site="Furnace Gate",
                rosterRef="t7-xarog-seal",
                detailedActorBudget="1–2",
            ),
            card(
                id="t7-interstice",
                floors="70→71",
                title="Old God Interstice",
                job="Interstice",
                targetBand="Severe (non-HP)",
                site="Ch 65",
                summary="Campaign-scale threshold; not Tier 7.5; not a Gate Guardian.",
                detailedActorBudget="0–3",
                rosterRef="t7-interstice-room",
                hazard="Identity / memory / route pressure",
            ),
        ],
    }
)

# ----- Tier 8 -----
tiers.append(
    {
        "tier": 8,
        "zone": "Duskshard Pools",
        "floors": "71–80",
        "guardian": "Eirfax, the Dusk Crowned",
        "corePressures": [
            "Delayed consequence via reflections",
            "Identity drift across surfaces",
            "Cooling light / dusk residue",
            "Uncertain succession (which self continues)",
            "Dusk Inversion / Shard-Sink / Prayer Rust",
        ],
        "opsChapter": {
            "status": "Director bible Ch 66 operational guidance",
            "sampleSeed": "The Camp That Returned First — exhausted future selves",
            "gatePrep": (
                "Eirfax tests which version of the Expedition deserves continuity; "
                "choose identity without erasing alternatives"
            ),
        },
        "faunaRoles": [
            "reflection doubles",
            "dusk-crown cult remnants",
            "pool claimers",
            "grief-bound stalkers",
        ],
        "sampleRosters": [
            roster(
                "t8-basins-open",
                "Duskshard Basins Crossing (F71)",
                "Teaching",
                "Hard→Severe",
                [
                    actor(
                        "Slithering Tracker (pool claim)",
                        2,
                        "skirmisher",
                        "Slithering Tracker",
                        "9",
                        "10–12",
                        True,
                    ),
                    actor(
                        "Reflection double (lagged intention)",
                        2,
                        "skirmisher",
                        "Allip",
                        "5",
                        "10–12",
                        True,
                        "Establish what the surface reflects before it lies",
                    ),
                ],
                abstract=["Dusk Inversion clock mid-fight"],
                levers={
                    "player": "Learn which pool shows intention vs last action vs rejected choice",
                    "director": "Arbitrary deceptive mirrors are banned — teach rules first",
                    "exit": "Twilight Shelf (F74) if inversion unresolved",
                },
                notes="Keep ≤4 detailed. Reflections lag — delayed EV.",
            ),
            roster(
                "t8-camp-returned",
                "Camp That Returned First (F75–77)",
                "Choosing",
                "Severe",
                [
                    actor(
                        "Exhausted future self (PC double)",
                        2,
                        "brute/controller",
                        "Deathlock",
                        "12",
                        "14–16",
                        True,
                        "Use as shell for future-PC — scrubbed undead template; sandbox CR",
                    ),
                    actor(
                        "Yeth Hound grief-bind",
                        2,
                        "skirmisher",
                        "Yeth Hound",
                        "10",
                        "11–13",
                        True,
                    ),
                ],
                abstract=[
                    "Helping them may create the future they warn against",
                    "One carries a relic the party has not yet found — off-map Research check",
                ],
                levers={
                    "player": "Aid / quarantine / harvest relic / refuse recognition",
                    "director": "Equipment can be real; do not auto-kill doubles for XP",
                    "exit": "Crown-Shard Shelf dry ledge",
                },
                notes="Ch 66 sample seed. ≤8 detailed.",
            ),
            roster(
                "t8-eirfax-seal",
                "Crown Gate — Eirfax, the Dusk Crowned (F80)",
                "Climactic",
                "Severe→Catastrophic",
                [
                    actor(
                        "Eirfax, the Dusk Crowned",
                        1,
                        "seal/guardian",
                        "Eirfax, the Dusk Crowned",
                        "26",
                        "26",
                    ),
                    actor(
                        "Crown Reflection (arena feature)",
                        1,
                        "hazard-actor",
                        note="Offers to remove regret / duplicate success / abandon Interstice burden",
                    ),
                ],
                abstract=["Continuity vote across seats — not damage alone"],
                levers={
                    "player": "Choose which version continues without erasing alternatives",
                    "director": "Crown silhouette clearer in water than air — stage accordingly",
                    "exit": "Refuse crown bargain — costs continuity leverage later",
                },
                notes="Fey / Medium / CR 26 / NE — Gate Guardian.",
            ),
        ],
        "encounterCards": [
            card(
                id="t8-f71-basins",
                floors="71",
                title="Duskshard Basins",
                job="Teaching",
                targetBand="Hard→Severe",
                site="Duskshard Basins",
                rosterRef="t8-basins-open",
                detailedActorBudget="3–5",
                hazard="Shard-Sink",
            ),
            card(
                id="t8-f72-obsidian",
                floors="72",
                title="Obsidian Mirror Bank",
                job="Revealing",
                targetBand="Hard",
                site="Obsidian Mirror Bank",
                summary="Survivor poetry ties to Veyr-Obsid rites — unmapped link; reflections linger.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t8-f74-haven",
                floors="74",
                title="Twilight Shelf",
                job="Choosing",
                targetBand="Routine (rest)→Hard",
                site="Twilight Shelf",
                summary="Exceptional dry ledge; light/hush trade slowly.",
                detailedActorBudget="0–3",
            ),
            card(
                id="t8-f76-camp",
                floors="76",
                title="Camp That Returned First",
                job="Choosing",
                targetBand="Severe",
                site="Ch 66 sample seed",
                rosterRef="t8-camp-returned",
                detailedActorBudget="4–5",
            ),
            card(
                id="t8-f78-crown-cult",
                floors="78",
                title="Crown Cult Procession",
                job="Taxing",
                targetBand="Severe",
                site="Twilight Verge",
                summary="Instruments d8 omen pressure; liturgical hush.",
                detailedActorBudget="3–6",
                hazard="Prayer Rust (presentation)",
            ),
            card(
                id="t8-f79-inversion",
                floors="79",
                title="Dusk Inversion Approach",
                job="Taxing",
                targetBand="Severe",
                site="Deep basin approach",
                summary="Light/shadow swap; seal silhouette clearer below.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t8-f80-seal",
                floors="80",
                title="Crown Gate + Eirfax",
                job="Climactic",
                targetBand="Severe→Catastrophic",
                site="Crown Gate",
                rosterRef="t8-eirfax-seal",
                detailedActorBudget="1–2",
            ),
        ],
    }
)

# ----- Tier 9 -----
tiers.append(
    {
        "tier": 9,
        "zone": "Veiled Iron Spiral",
        "floors": "81–90",
        "guardian": "Threxus, the Iron Spiral",
        "corePressures": [
            "False progress (descend / circle / return unclear)",
            "Compression of time, space, supply, history",
            "Concealment of routes / scale / pursuers",
            "Endurance of purpose when milestones vanish",
            "Coil Tighten / Rail-Vanish / Shadow Trade",
        ],
        "opsChapter": {
            "status": "Director bible Ch 67 operational guidance",
            "sampleSeed": "The Siege on Every Turn — same attackers at different prep moments",
            "gatePrep": (
                "Threxus tests defining progress without distance; circular strategy strengthens Guardian"
            ),
            "nameCollision": (
                "Do not confuse zone/Guardian with Turning Spiral patron theology — live name is Threxus"
            ),
        },
        "faunaRoles": [
            "iron hunters on repeated routes",
            "compressed swarms",
            "timeline-split pursuers",
            "rivet-tunnel constructs",
        ],
        "sampleRosters": [
            roster(
                "t9-helix-open",
                "Veiled Helix First Coil (F81)",
                "Teaching",
                "Severe",
                [
                    actor(
                        "Helmed Horror rail-hunter",
                        2,
                        "brute",
                        "Helmed Horror",
                        "11",
                        "14–16",
                        True,
                        "Attacks only on repeated routes if party circles",
                    ),
                    actor(
                        "Iron Cobra rivet-scout",
                        2,
                        "skirmisher",
                        "Iron Cobra",
                        "7",
                        "10–12",
                        True,
                    ),
                ],
                abstract=["Rail-Vanish: path behind disappears — map transformation, not turns"],
                levers={
                    "player": "Leave material/wound/oath anchors that survive compression",
                    "director": "Identical corridors differ by what they change in carried objects",
                    "exit": "Iron Rest landing (F84) if coil recognized as repeat",
                },
                notes="Keep ≤4 detailed. Circular kite strengthens later Threxus.",
            ),
            roster(
                "t9-siege-every-turn",
                "Siege on Every Turn (F85–87)",
                "HavenSiege",
                "Severe",
                [
                    actor(
                        "Siege force (early prep)",
                        2,
                        "skirmisher",
                        "Shield Guardian",
                        "6",
                        "14–16",
                        True,
                    ),
                    actor(
                        "Siege force (mid prep)",
                        2,
                        "brute",
                        "Hellfire Engine",
                        "7",
                        "16–18",
                        True,
                        "Same force, later moment — sandbox CR; Ch 17 scale",
                    ),
                    actor(
                        "Haven speaker (ally)",
                        1,
                        "ally",
                        note="Remembers only most recent version — off-map unless acting",
                    ),
                ],
                abstract=[
                    "Defending one turn changes the next",
                    "Evidence-that-survives-compression as victory condition",
                ],
                levers={
                    "player": "Create records the compression cannot erase",
                    "director": "Do not add waves only because first group died quickly",
                    "exit": "Murkish Rivet-Tunnels — costly, may skip a coil",
                },
                notes="Ch 67 sample seed. ≤8 detailed including optional ally.",
            ),
            roster(
                "t9-threxus-seal",
                "Spiral Gate — Threxus, the Iron Spiral (F90)",
                "Climactic",
                "Severe→Catastrophic",
                [
                    actor(
                        "Threxus, the Iron Spiral",
                        1,
                        "seal/guardian",
                        "Threxus, the Iron Spiral",
                        "28",
                        "28",
                    ),
                    actor(
                        "Compression Coil (arena feature)",
                        1,
                        "hazard-actor",
                        note="Strengthens if party only circles; demonstrate irrepeatable change",
                    ),
                ],
                abstract=[
                    "Prove changes caused, people preserved, truths carried, choices that cannot repeat"
                ],
                levers={
                    "player": "Define progress without distance marks",
                    "director": "Purely circular strategies empower Threxus",
                    "exit": "Iron Rest — temporary only; Gate demands demonstration",
                },
                notes="Construct / Gargantuan / CR 28 / LN — Gate Guardian.",
            ),
        ],
        "encounterCards": [
            card(
                id="t9-f81-helix",
                floors="81",
                title="Veiled Helix",
                job="Teaching",
                targetBand="Severe",
                site="Veiled Helix",
                rosterRef="t9-helix-open",
                detailedActorBudget="3–5",
                hazard="Coil Tighten",
            ),
            card(
                id="t9-f82-veil-coil",
                floors="82",
                title="Veiled Coil Shadow Trade",
                job="Taxing",
                targetBand="Severe",
                site="Veiled Coil",
                summary="Iron rail and dark swap beyond lantern reach.",
                detailedActorBudget="3–6",
                hazard="Shadow Trade",
            ),
            card(
                id="t9-f84-haven",
                floors="84",
                title="Iron Rest",
                job="Choosing",
                targetBand="Routine (rest)→Hard",
                site="Iron Rest",
                summary="Narrow landing; Weave tightening eases briefly.",
                detailedActorBudget="0–3",
            ),
            card(
                id="t9-f86-siege",
                floors="86",
                title="Siege on Every Turn",
                job="HavenSiege",
                targetBand="Severe",
                site="Ch 67 sample seed",
                rosterRef="t9-siege-every-turn",
                detailedActorBudget="4–6",
            ),
            card(
                id="t9-f88-rivet",
                floors="88",
                title="Murkish Rivet-Tunnels",
                job="Revealing",
                targetBand="Hard→Severe",
                site="Murkish Rivet-Tunnels",
                summary="Side passages; The Murk iron-guild slang ≠ Umbrin faction lore.",
                detailedActorBudget="2–5",
            ),
            card(
                id="t9-f89-echo",
                floors="89",
                title="Threxus Echo Approach",
                job="Taxing",
                targetBand="Severe",
                site="Spiral approach",
                summary="Instruments d8 Threxus echo; false progress peaks.",
                detailedActorBudget="2–4",
            ),
            card(
                id="t9-f90-seal",
                floors="90",
                title="Spiral Gate + Threxus",
                job="Climactic",
                targetBand="Severe→Catastrophic",
                site="Spiral Gate",
                rosterRef="t9-threxus-seal",
                detailedActorBudget="1–2",
            ),
        ],
    }
)

# ----- Tier 10 -----
tiers.append(
    {
        "tier": 10,
        "zone": "Silencebound Void",
        "floors": "91–100",
        "guardian": "The Marquis of Silence",
        "corePressures": [
            "Sound Theft / anti-resonance",
            "Void Lean toward unseen center",
            "Unasked questions louder than voices",
            "Attractive stillness offer (end of loss/contradiction)",
            "Preserve difference without romanticizing endless suffering",
        ],
        "opsChapter": {
            "status": "Director bible Ch 68 operational guidance",
            "sampleSeed": "Marquis confrontation — defeat / replace / persuade / bind / transform",
            "gatePrep": (
                "Marquis understands exhaustion; offer of genuine rest. Victory reframes Opening/"
                "Heartcell relationship — not a treasure chest ending."
            ),
            "silentOnes": "Never name Silent Ones aloud — Director note only (Instruments d8)",
        },
        "faunaRoles": [
            "hush-threshold sentinels",
            "anti-resonance wraiths",
            "memory-thieves",
            "void-lean brutes",
        ],
        "sampleRosters": [
            roster(
                "t10-hush-threshold",
                "Hush Threshold Crossing (F91)",
                "Teaching",
                "Severe",
                [
                    actor(
                        "Sound-Theft Wraith",
                        2,
                        "controller",
                        "Bodak",
                        "9",
                        "14–16",
                        True,
                        "Verbal spell risk; last reply never arrives",
                    ),
                    actor(
                        "Void Lean brute",
                        2,
                        "brute",
                        "Nightwalker",
                        "12",
                        "16–18",
                        True,
                        "Excel CR/type often sandbox — scale; gravity toward unseen center",
                    ),
                ],
                abstract=["Communication fail waves as seat checks, not only HP"],
                levers={
                    "player": "Nonverbal coordination; prepared signals from earlier tiers",
                    "director": "Thin sound gradually — teach before total hush",
                    "exit": "Last Whisper (F93) while echo still survives",
                },
                notes="Keep ≤4 detailed. Silence is the tax.",
            ),
            roster(
                "t10-last-choir",
                "Last Choir Echo Defense (F94–96)",
                "Taxing",
                "Severe",
                [
                    actor(
                        "Anti-Resonance Zone (feature)",
                        1,
                        "hazard-actor",
                        note="Treat as terrain unless it acts; Resonance cost spike",
                    ),
                    actor(
                        "Voidmind echo-eater",
                        2,
                        "controller",
                        "Voidmind",
                        "11",
                        "15–17",
                        True,
                    ),
                    actor(
                        "Fracture-Kin Shadow Demon hush-blade",
                        2,
                        "skirmisher",
                        "Fracture-Kin Shadow Demon",
                        "11",
                        "14–16",
                        True,
                        "Lore-scrubbed Fracture-Kin name — not SWTOR",
                    ),
                ],
                abstract=["Memory loss clock — lose map detail on failed Support"],
                levers={
                    "player": "Spend earlier-tier anchors (oaths, songs, path-claims) as fuel",
                    "director": "Do not monologue full Matrix; reveal through operation",
                    "exit": "Quiet Deep Antechamber rumor — unfinished on purpose",
                },
                notes="≤8 detailed. Preserve difference as objective.",
            ),
            roster(
                "t10-marquis-seal",
                "Marquis Gate — The Marquis of Silence (F100)",
                "Climactic",
                "Catastrophic (chosen risk / exits / non-damage win allowed)",
                [
                    actor(
                        "The Marquis of Silence",
                        1,
                        "seal/guardian",
                        "The Marquis of Silence",
                        "30",
                        "30",
                    ),
                    actor(
                        "Stillness Offer (arena feature)",
                        1,
                        "hazard-actor",
                        note="Genuine rest offer — attractive, not cartoon evil. Count only if acting.",
                    ),
                ],
                abstract=[
                    "Victory modes: defeat / replace / persuade / bind / transform",
                    "Personal consequences for each PC from earlier Interstice answers",
                ],
                levers={
                    "player": "Preserve difference without endless suffering romance",
                    "director": "Floor 100 must force an answer — not loot silence",
                    "exit": "Honorable campaign end before F100 remains valid if table chose it openly",
                },
                notes="Fiend / Huge / CR 30 / CE — Gate Guardian. xpField metadata only.",
            ),
        ],
        "encounterCards": [
            card(
                id="t10-f91-hush",
                floors="91",
                title="Hush Threshold",
                job="Teaching",
                targetBand="Severe",
                site="Hush Threshold",
                rosterRef="t10-hush-threshold",
                detailedActorBudget="3–5",
                hazard="Sound Theft",
            ),
            card(
                id="t10-f93-haven",
                floors="93",
                title="Last Whisper",
                job="Choosing",
                targetBand="Routine (social)→Hard",
                site="Last Whisper",
                summary="Final place any echo survives; whispered names linger one breath.",
                detailedActorBudget="0–3",
            ),
            card(
                id="t10-f94-choir",
                floors="94",
                title="Last Choir Echo",
                job="Taxing",
                targetBand="Severe",
                site="Last Choir Echo",
                rosterRef="t10-last-choir",
                detailedActorBudget="4–6",
            ),
            card(
                id="t10-f96-void-lean",
                floors="96",
                title="Void Lean Deep",
                job="Taxing",
                targetBand="Severe→Catastrophic",
                site="Silencebound deep",
                summary="Gravity toward unseen center; stillness unfinished.",
                detailedActorBudget="2–5",
                hazard="Void Lean",
            ),
            card(
                id="t10-f98-unasked",
                floors="98",
                title="Unasked Question Gallery",
                job="Revealing",
                targetBand="Hard→Severe",
                site="Quiet Deep Antechamber approach",
                summary="Unspoken thoughts louder than voices — dread as EV, confirm mechanics at table.",
                detailedActorBudget="1–3",
                hazard="Unasked Question",
            ),
            card(
                id="t10-f99-gate-hum",
                floors="99",
                title="Marquis Gate Hum",
                job="Revealing",
                targetBand="Severe",
                site="Approach to Marquis Gate",
                summary="Instruments d8 omen; absolute still can free one gate-clock tick.",
                detailedActorBudget="1–3",
            ),
            card(
                id="t10-f100-seal",
                floors="100",
                title="Marquis Gate + The Marquis of Silence",
                job="Climactic",
                targetBand="Catastrophic",
                site="Marquis Gate",
                rosterRef="t10-marquis-seal",
                detailedActorBudget="1–2",
            ),
        ],
    }
)

toolkit["tiers"] = tiers

text = json.dumps(toolkit, indent=2, ensure_ascii=False) + "\n"
(out1 := root / "src" / "data" / "t6-10-encounter-toolkit.json").write_text(
    text, encoding="utf-8"
)
(out2 := root / "scripts" / "t6-10-encounter-toolkit.json").write_text(
    text, encoding="utf-8"
)
n_cards = sum(len(t["encounterCards"]) for t in tiers)
n_rosters = sum(len(t["sampleRosters"]) for t in tiers)
print("wrote", out1)
print("wrote", out2)
print("cards", n_cards, "rosters", n_rosters)
for t in tiers:
    print(
        f"  T{t['tier']}: cards={len(t['encounterCards'])} rosters={len(t['sampleRosters'])} guardian={t['guardian']}"
    )
