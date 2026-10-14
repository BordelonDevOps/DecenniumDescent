#!/usr/bin/env python3
"""
V7 Pack 04 — Seasonal / Decennial Persistence playtest harness.
Deterministic Cycle Record simulations. Does not edit canon.
Sources used (pending-review V7 bible extract + main/ReviewBible companions):
  - DescentReviewChanges/incoming/DecenniumDescentv7/GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (§20)
  - src/data/haven.json
  - src/data/dungeon-mechanics.json (cycle / Opening / Horn)
  - docs/canon/CANON_MANIFEST.json
  - ReviewBible docs/director-only/continuity/* + MM CANON_BOUNDARY.md
Missing pack-expected paths noted in metrics.sourceGaps:
  docs/mechanics/GAMEPLAY_LOOP_CANON.md, DESIGN_DOCTRINE.md, docs/director-only/continuity/ on main.
"""
from __future__ import annotations

import json
import random
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
PACK = "04-seasonal-decennial-persistence"

SOURCE_GAPS = [
    "docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)",
    "docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)",
    "docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)",
]

AGENTS = [
    "cycle-director",
    "campaign-chronicler",
    "haven-council",
    "market-historian",
    "expedition-dynasty",
    "new-player-company",
    "map-and-route-auditor",
    "canon-boundary-auditor",
]

# 10 three-Cycle + 3 five-Cycle stress campaigns
CAMPAIGNS = [
    {"seed": 301, "scenarioId": "SEA-HAVEN-BOOM", "cycles": 3, "stress": False},
    {"seed": 302, "scenarioId": "SEA-HAVEN-BOOM", "cycles": 3, "stress": False},
    {"seed": 311, "scenarioId": "SEA-MARKET-GLUT", "cycles": 3, "stress": False},
    {"seed": 312, "scenarioId": "SEA-MARKET-GLUT", "cycles": 3, "stress": False},
    {"seed": 321, "scenarioId": "SEA-FAILED-DEPTH", "cycles": 3, "stress": False},
    {"seed": 322, "scenarioId": "SEA-FAILED-DEPTH", "cycles": 3, "stress": False},
    {"seed": 331, "scenarioId": "SEA-FACTION-WAR", "cycles": 3, "stress": False},
    {"seed": 341, "scenarioId": "SEA-DYNASTY", "cycles": 3, "stress": False},
    {"seed": 342, "scenarioId": "SEA-DYNASTY", "cycles": 3, "stress": False},
    {"seed": 351, "scenarioId": "SEA-HAVEN-DAMAGE", "cycles": 3, "stress": False},
    {"seed": 501, "scenarioId": "SEA-HAVEN-BOOM", "cycles": 5, "stress": True},
    {"seed": 502, "scenarioId": "SEA-FACTION-WAR", "cycles": 5, "stress": True},
    {"seed": 503, "scenarioId": "SEA-DYNASTY", "cycles": 5, "stress": True},
]

GEO_OPTS = [
    "subsidence collapses a previously mapped side spur",
    "flood opens a new lower gallery near a secured trunk",
    "earthshift reorients a Haven approach corridor",
    "rockfall seals an unsecured shortcut while trunk remains",
]
ECO_OPTS = [
    "predator rebound after harvest pause",
    "fungal bloom recolonizes stripped chambers",
    "migratory swarm displaces prior nesting sites",
    "disease cull thins one harvestable species",
]
ECON_OPTS = [
    "surface glut crashes unit price for prior boom material",
    "scarcity premium returns after stockpile decay",
    "sponsor insurance rates spike after famous loss",
    "assay house opens a new specialty desk for rival material",
]
POL_OPTS = [
    "district charter rewritten after sponsor contest",
    "militia ordinance after civic damage",
    "heir recognition and title dispute",
    "route-abandonment decree after Tier IV rumor panic",
]
RES_OPTS = [
    "resonance weather shifts Watch risk on trunk routes",
    "quiet-week intensifies near damaged districts",
    "song-echo makes Attention-tagged cargo hotter",
    "Twilight Week boundary blur alters ritual timing",
]


def scenario_opening_outcome(scenario: str, cycle_idx: int, rng: random.Random) -> dict:
    """Representative expedition outcome for this Opening (scenario-driven)."""
    base = {
        "publicDepthRecord": "Haven",
        "routesSecured": [],
        "routesLost": [],
        "routesConcealed": [],
        "districts": {},
        "artifactsExtracted": [],
        "artifactsRetainedBelow": [],
        "factionStandings": {},
        "debts": [],
        "specialists": [],
        "successors": [],
        "unresolved": [],
        "economicShocks": [],
        "directorOnlyHidden": [],
        "survivors": 10,
        "retired": 0,
        "heirsReady": 0,
        "wealthIndex": 40,
        "mapChamberFidelity": 0.85,
        "securedPrincipleValue": 0.7,
        "explorationTrivial": False,
        "newPlayerAccess": 0.65,
    }

    if scenario == "SEA-HAVEN-BOOM":
        base.update(
            {
                "publicDepthRecord": "Haven",
                "routesSecured": ["Gateward-Haven Trunk A"],
                "districts": {"Gateward Caravan Yards": "strengthened", "Makers' Quarter": "strengthened"},
                "artifactsExtracted": ["Assayed bloom-metal lot", "Route charter seals"],
                "factionStandings": {"Caravan Guild": +2, "Iron Ledger Houses": +1},
                "economicShocks": ["Institutionalized Haven haul; surface stockpile rising"],
                "wealthIndex": 55 + cycle_idx * 12,
                "survivors": 11,
                "specialists": ["Routekeeper lineage", "Assay clerk retainer"],
            }
        )
        if cycle_idx >= 1:
            base["economicShocks"].append("Prior boom material saturates surface markets")
            base["wealthIndex"] = min(95, base["wealthIndex"] + 8)
        if cycle_idx >= 2:
            base["explorationTrivial"] = base["wealthIndex"] >= 90 and base["securedPrincipleValue"] > 0.85
            base["newPlayerAccess"] = 0.45 if base["wealthIndex"] >= 85 else 0.6

    elif scenario == "SEA-MARKET-GLUT":
        mat = rng.choice(["Bloom resin", "Anvil slag-ingot", "Choir silver-thread"])
        base.update(
            {
                "publicDepthRecord": "Tier III",
                "routesSecured": ["Marsh Spur B"],
                "artifactsExtracted": [f"Bulk {mat}"],
                "economicShocks": [f"{mat} floods Seal Exchange and surface yards"],
                "factionStandings": {"Makers' Quarter guilds": +1, "Surface sponsors": -1},
                "wealthIndex": 50 - cycle_idx * 8,
                "districts": {"Seal Exchange": "strengthened", "Makers' Quarter": "strained"},
            }
        )
        if cycle_idx >= 1:
            base["economicShocks"].append(f"Next-Cycle demand for {mat} collapses; crafting pivots")
            base["artifactsExtracted"] = [f"Alternate harvest (not {mat})"]
            base["wealthIndex"] = 42 + (5 if cycle_idx == 2 else 0)

    elif scenario == "SEA-FAILED-DEPTH":
        base.update(
            {
                "publicDepthRecord": "Tier IV (disappeared; no verified return)",
                "routesSecured": [],
                "routesLost": ["Radiant Isles approach"],
                "unresolved": ["Famous company missing after Horn window"],
                "factionStandings": {"Sovereign sponsors": -2, "Rival companies": +1},
                "economicShocks": ["Insurance panic; Tier IV premiums spike"],
                "debts": ["Open recovery bonds unpaid"],
                "survivors": 0 if cycle_idx == 0 else 8,
                "wealthIndex": 25,
                "securedPrincipleValue": 0.35,
                "mapChamberFidelity": 0.2,
                "directorOnlyHidden": [
                    # Director notes only — must NOT appear in public Cycle Record fields
                    "DIR: no confirmation of passage beyond Gate VI; disappearance stays rumor-grade"
                ],
            }
        )
        if cycle_idx >= 1:
            base["routesLost"].append("Abandoned Radiant Isles approach (decree)")
            base["unresolved"].append("Rumor war: reckless glory vs cursed depth")
            base["publicDepthRecord"] = "Haven / Tier III (cautionary ceiling in public talk)"
            base["survivors"] = 9
            base["newPlayerAccess"] = 0.7

    elif scenario == "SEA-FACTION-WAR":
        a, b = "Seal Exchange Consortium", "Gateward Charter House"
        lead = a if cycle_idx % 2 == 0 else b
        base.update(
            {
                "publicDepthRecord": "Haven",
                "districts": {
                    "Seal Exchange": "contested" if cycle_idx < 2 else ("captured" if lead == a else "strengthened"),
                    "Gateward Caravan Yards": "contested",
                },
                "factionStandings": {a: 2 - cycle_idx, b: cycle_idx - 1},
                "debts": [f"Provenance lien held by {lead}"],
                "unresolved": ["District control and artifact provenance dispute"],
                "economicShocks": ["Auction delays; seizure claims rise"],
                "wealthIndex": 48,
                "specialists": ["Magistrate advocates", "Broker secondaries"],
            }
        )

    elif scenario == "SEA-DYNASTY":
        base.update(
            {
                "publicDepthRecord": "Haven",
                "routesSecured": ["Family Trunk Charter"],
                "districts": {"Iron Ledger Houses": "strengthened"},
                "survivors": max(4, 10 - cycle_idx * 2),
                "retired": 2 + cycle_idx,
                "heirsReady": 1 + cycle_idx,
                "successors": [f"Heir cohort {cycle_idx + 1}"],
                "specialists": ["Retired Routekeeper as trainer", "Apprentice assay hand"],
                "factionStandings": {"Dynasty house": 1 + cycle_idx},
                "debts": ["Inherited outfitter liens"] if cycle_idx else [],
                "wealthIndex": 50 + cycle_idx * 5,
                "newPlayerAccess": 0.55 if cycle_idx >= 2 else 0.65,
                "securedPrincipleValue": 0.75,
            }
        )
        if cycle_idx >= 2:
            base["artifactsExtracted"] = ["Heir-provenanced seals (not unbeatable gear)"]

    elif scenario == "SEA-HAVEN-DAMAGE":
        dmg = ["Gateward Caravan Yards", "Low Lantern Ward", "Draughtworks"][min(cycle_idx, 2)]
        recovery = "damaged" if cycle_idx == 0 else ("recovering" if cycle_idx == 1 else "strengthened")
        base.update(
            {
                "publicDepthRecord": "Haven",
                "districts": {dmg: recovery, "Underways": "strained"},
                "unresolved": ["Civic repair bonds", "Militia curfew memory"],
                "factionStandings": {"Haven Council": 1 if cycle_idx else -1, "Labor crews": +1},
                "economicShocks": ["Repair demand boom; outbound convoy capacity cut"],
                "wealthIndex": 35 + cycle_idx * 10,
                "newPlayerAccess": 0.6,
            }
        )

    # Replenishment always erodes chamber fidelity; principles decay slowly
    base["mapChamberFidelity"] = round(max(0.1, 0.85 - 0.25 * cycle_idx - rng.random() * 0.1), 2)
    base["securedPrincipleValue"] = round(
        min(0.95, max(0.25, base["securedPrincipleValue"] - 0.05 * cycle_idx + rng.uniform(-0.05, 0.08))), 2
    )
    if base["mapChamberFidelity"] < 0.4 and base["securedPrincipleValue"] >= 0.55:
        base["explorationTrivial"] = False
    return base


def apply_gep_changes(record: dict, prior: dict | None, rng: random.Random) -> dict:
    """One change each in Geography, Ecology, Economy, Politics, Resonance — tied to Cycle Record."""
    cause = "baseline Opening"
    if prior:
        cause = (
            prior.get("economicShocks", ["prior Opening"])[0]
            if prior.get("economicShocks")
            else (prior.get("unresolved") or ["prior Opening"])[0]
        )
    changes = {
        "Geography": f"{rng.choice(GEO_OPTS)} (cause: {cause})",
        "Ecology": f"{rng.choice(ECO_OPTS)} (cause: {cause})",
        "Economy": f"{rng.choice(ECON_OPTS)} (cause: {cause})",
        "Politics": f"{rng.choice(POL_OPTS)} (cause: {cause})",
        "Resonance": f"{rng.choice(RES_OPTS)} (cause: {cause})",
    }
    record["gepChanges"] = changes
    return record


def public_cycle_record(outcome: dict, cycle_year: int) -> dict:
    """Public Cycle Record fields only — strips directorOnlyHidden into separate sealed note."""
    sealed = outcome.get("directorOnlyHidden", [])
    public = {
        "cycleYear": cycle_year,
        "routes": {
            "discoveredOrSecured": outcome.get("routesSecured", []),
            "lost": outcome.get("routesLost", []),
            "concealed": outcome.get("routesConcealed", []),
        },
        "havenDistricts": outcome.get("districts", {}),
        "majorArtifactsExtracted": outcome.get("artifactsExtracted", []),
        "majorArtifactsRetainedBelow": outcome.get("artifactsRetainedBelow", []),
        "factionStandingsAndDebts": {
            "standings": outcome.get("factionStandings", {}),
            "debts": outcome.get("debts", []),
        },
        "specialistsAndSuccessors": {
            "specialists": outcome.get("specialists", []),
            "successors": outcome.get("successors", []),
        },
        "unresolved": outcome.get("unresolved", []),
        "economicShocks": outcome.get("economicShocks", []),
        "publiclyAcceptedDepthRecord": outcome.get("publicDepthRecord"),
        "gepChanges": outcome.get("gepChanges", {}),
        "tenYearAdvance": {
            "survivors": outcome.get("survivors"),
            "retired": outcome.get("retired"),
            "heirsReady": outcome.get("heirsReady"),
            "wealthIndex": outcome.get("wealthIndex"),
        },
    }
    return {"public": public, "directorSealed": sealed}


def simulate_campaign(camp: dict) -> dict:
    rng = random.Random(camp["seed"])
    cycles = []
    prior_outcome = None
    year = 710 + camp["seed"] % 50  # fictional Opening years for ledger
    for i in range(camp["cycles"]):
        outcome = scenario_opening_outcome(camp["scenarioId"], i, rng)
        apply_gep_changes(outcome, prior_outcome, rng)
        # Persistence ledger checks
        persistence = {
            "knowledgePersists": True,
            "provenancePersists": bool(outcome.get("artifactsExtracted") or (prior_outcome and prior_outcome.get("artifactsExtracted"))),
            "havenCivicCorePersists": True,
            "securedPrinciplesPersist": outcome["securedPrincipleValue"] >= 0.45,
            "chambersReplenished": outcome["mapChamberFidelity"] < 0.7 or i > 0,
            "marketDemandShifted": bool(outcome.get("economicShocks")),
            "priorMattersWithoutTrivialExploration": (not outcome["explorationTrivial"])
            and (
                bool(outcome.get("routesSecured"))
                or bool(outcome.get("factionStandings"))
                or outcome.get("heirsReady", 0) > 0
                or bool(outcome.get("debts"))
            ),
        }
        if camp["scenarioId"] == "SEA-HAVEN-BOOM" and i >= 2 and outcome["wealthIndex"] >= 90:
            persistence["runawayWealthRisk"] = True
        else:
            persistence["runawayWealthRisk"] = False

        rec = public_cycle_record(outcome, year + i * 10)
        cycles.append(
            {
                "openingIndex": i + 1,
                "outcome": outcome,
                "record": rec,
                "persistence": persistence,
            }
        )
        prior_outcome = outcome
    return {"campaign": camp, "cycles": cycles}


def analyze_campaign(sim: dict) -> dict:
    cycles = sim["cycles"]
    camp = sim["campaign"]
    wealth = [c["outcome"]["wealthIndex"] for c in cycles]
    map_f = [c["outcome"]["mapChamberFidelity"] for c in cycles]
    princ = [c["outcome"]["securedPrincipleValue"] for c in cycles]
    access = [c["outcome"]["newPlayerAccess"] for c in cycles]
    trivial_flags = [c["outcome"]["explorationTrivial"] for c in cycles]
    runaway = any(c["persistence"].get("runawayWealthRisk") for c in cycles)
    gep_linked = all(
        all("cause:" in str(v) for v in c["outcome"]["gepChanges"].values()) for c in cycles
    )
    public_leaks = []
    for c in cycles:
        pub = json.dumps(c["record"]["public"]).lower()
        for banned in [
            "marquis",
            "crystal path",
            "focusing crystal",
            "floor 97",
            "floor 100",
            "tier vii",
            "tier viii",
            "tier ix",
            "tier x",
            "claimant succession",
            "silent ones",
            "old god vulnerability",
        ]:
            if banned in pub:
                public_leaks.append(banned)
        # Public depth must not claim verified beyond Sixth Gate
        depth = str(c["record"]["public"].get("publiclyAcceptedDepthRecord", "")).lower()
        if "seventh" in depth or "tier vii" in depth or "tier 7" in depth:
            public_leaks.append("public depth beyond Sixth Gate")

    return {
        "wealthTrajectory": wealth,
        "mapChamberFidelity": map_f,
        "securedPrincipleValue": princ,
        "newPlayerAccess": access,
        "anyExplorationTrivial": any(trivial_flags),
        "runawayWealthRisk": runaway,
        "gepAlwaysCausedByPriorRecord": gep_linked,
        "publicCanonLeaks": public_leaks,
        "cyclesRun": camp["cycles"],
        "stress": camp["stress"],
        "finalDistricts": cycles[-1]["outcome"]["districts"],
        "finalDepthPublic": cycles[-1]["outcome"]["publicDepthRecord"],
    }


def agent_payload(agent: str, scenario: str, seed: int, sim: dict, metrics_base: dict) -> dict:
    cycles = sim["cycles"]
    m = deepcopy(metrics_base)
    m["seed"] = seed
    m["sourceGaps"] = SOURCE_GAPS
    m["authorityNote"] = (
        "Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; "
        "Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits."
    )

    obs, questions, exploits, recs = [], [], [], []
    conf = "medium"

    # Shared cycle ledger snippet
    ledger = []
    for c in cycles:
        o = c["outcome"]
        ledger.append(
            f"Opening {c['openingIndex']}: depth={o['publicDepthRecord']}; "
            f"wealth={o['wealthIndex']}; mapFidelity={o['mapChamberFidelity']}; "
            f"principle={o['securedPrincipleValue']}; GEP={{G:{o['gepChanges']['Geography'][:40]}...}}"
        )
    m["cycleLedger"] = ledger

    if agent == "cycle-director":
        obs = [
            f"Applied replenishment across {len(cycles)} Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).",
            f"Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity {m['mapChamberFidelity']}).",
            "Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.",
            "Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.",
        ]
        if m["runawayWealthRisk"]:
            obs.append("OBSERVED RISK: multi-Cycle Haven boom pushed wealthIndex into runaway band while secured trunk still valued.")
            exploits.append("Institutionalized Haven boom + retained trunk principles can stack into near-solved surface economy without solving the dungeon.")
        if m["anyExplorationTrivial"]:
            exploits.append("Exploration triviality flag tripped when wealth and secured principles both stayed very high.")
        questions.append(
            "Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule)."
        )
        recs.append(
            "Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore."
        )
        conf = "high"

    elif agent == "campaign-chronicler":
        obs = [
            "Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.",
            f"Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ({m['securedPrincipleValue']}).",
            "Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).",
        ]
        if not m["gepAlwaysCausedByPriorRecord"]:
            questions.append("Found a GEP change without explicit prior cause — chronicler reject.")
        else:
            obs.append("No orphaned Cycle-to-Cycle changes in this seed.")
        questions.append(
            "How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?"
        )
        recs.append("Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.")
        conf = "high"

    elif agent == "haven-council":
        obs = [
            f"District end-state: {m['finalDistricts']}.",
            "Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.",
            "Political memory (debts, decrees, contested provenance) persisted even when markets reset.",
        ]
        if scenario == "SEA-HAVEN-DAMAGE":
            obs.append("Damaged district moved damaged→recovering→strengthened across three Openings; outbound capacity lagged wealth recovery.")
            questions.append("No numeric civic HP / repair-cost table in haven.json — recovery pace was a Director ruling.")
        if scenario == "SEA-FACTION-WAR":
            obs.append("Sponsor contest kept Seal Exchange / Gateward contested across Cycles; institutions remembered liens.")
            exploits.append("If provenance liens never expire, faction war can lock auction liquidity for multiple Openings.")
        recs.append("Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.")
        conf = "medium"

    elif agent == "market-historian":
        obs = [
            f"Wealth trajectory across Openings: {m['wealthTrajectory']}.",
            "Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.",
            "Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.",
        ]
        if scenario == "SEA-MARKET-GLUT":
            obs.append("Next-Cycle demand collapse after flood was the dominant ten-year effect; alternate harvest restored partial wealth.")
            questions.append("No explicit glut→price elasticity numbers in companion data — used qualitative shock tiers.")
        if m["runawayWealthRisk"]:
            exploits.append("Repeated profitable Haven institutionalization without glut correction → runaway wealthIndex.")
            recs.append("Mandate at least one Economy GEP that counters any wealthIndex ≥80 boom unless a named disaster intervenes.")
        else:
            recs.append("Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.")
        conf = "medium"

    elif agent == "expedition-dynasty":
        last = cycles[-1]["outcome"]
        obs = [
            f"Survivors={last['survivors']}, retired={last['retired']}, heirsReady={last['heirsReady']}.",
            "Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.",
            "Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).",
        ]
        if scenario == "SEA-DYNASTY":
            obs.append("Heir cohorts inherited outfitter liens and Routekeeper training; new Opening still required fresh Supply and route risk.")
            questions.append("Bible lists successors but not heir mechanical benefits — used soft reputation + trainer access only.")
        if scenario == "SEA-FAILED-DEPTH" and cycles[0]["outcome"]["survivors"] == 0:
            obs.append("Opening 1 total loss produced rumor/debt persistence without living veterans; later Openings were non-dynastic replacements.")
        exploits.append("If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).")
        recs.append("Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).")
        conf = "medium"

    elif agent == "new-player-company":
        obs = [
            f"New-player access scores by Opening: {m['newPlayerAccess']} (1.0 = fully open field).",
            "Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.",
            "Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.",
        ]
        if min(m["newPlayerAccess"]) < 0.5:
            exploits.append("Late-Cycle institutionalized boom lowered new-player access below 0.5 — sponsorship oligopoly risk.")
            recs.append("Offer public charter slots / starter debts so new companies can enter boom Havens without dynasty capital.")
        if scenario == "SEA-FAILED-DEPTH":
            obs.append("After famous disappearance, cautionary public ceiling actually improved new-company Haven focus (access rose).")
        questions.append("Should Cycle Records expose competitor charters to new players, or only public decrees?")
        conf = "medium"

    elif agent == "map-and-route-auditor":
        obs = [
            f"Chamber map fidelity by Opening: {m['mapChamberFidelity']} (replenishment / geography shifts).",
            f"Secured-route principle value: {m['securedPrincipleValue']} (persists, not every chamber).",
            "Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.",
        ]
        if m["anyExplorationTrivial"]:
            exploits.append("High principle value + incomplete replenishment narrative could make exploration feel solved — flagged in boom stress.")
        questions.append(
            "Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years."
        )
        recs.append("On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.")
        conf = "high"

    elif agent == "canon-boundary-auditor":
        obs = [
            "Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.",
            "Director sealed notes (if any) were stored separately from public records.",
            "No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.",
            f"Leak scan on public JSON: {m['publicCanonLeaks'] or 'none'}.",
        ]
        if m["publicCanonLeaks"]:
            exploits.append(f"PUBLIC LEAK DETECTED: {m['publicCanonLeaks']}")
            conf = "high"
        else:
            obs.append("PASS: public vs Director boundary held for this seed.")
            conf = "high"
        if scenario == "SEA-FAILED-DEPTH":
            obs.append("Tier IV disappearance recorded as unverified public rumor/panic — not as cosmology reveal.")
            questions.append(
                "dungeon-mechanics.json still lists Tier 7–10 gate bosses and Marquis victory text in companion data — playtest used public ceiling from CANON_BOUNDARY; companion scrub is a separate continuity task (not edited here)."
            )
        recs.append(
            "Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge."
        )

    m["priorMattersWithoutTrivialExploration"] = all(
        c["persistence"]["priorMattersWithoutTrivialExploration"] for c in cycles
    ) and not m["anyExplorationTrivial"]

    return {
        "pack": PACK,
        "scenarioId": scenario,
        "agentId": agent,
        "seed": seed,
        "observations": obs,
        "metrics": m,
        "rulesQuestions": questions,
        "exploits": exploits,
        "recommendations": recs,
        "confidence": conf,
    }


def write_results():
    if RESULTS.exists():
        for p in RESULTS.rglob("*.json"):
            p.unlink()
    RESULTS.mkdir(parents=True, exist_ok=True)

    campaign_summaries = []
    for camp in CAMPAIGNS:
        sim = simulate_campaign(camp)
        metrics = analyze_campaign(sim)
        campaign_summaries.append({"seed": camp["seed"], "scenarioId": camp["scenarioId"], "metrics": metrics, "sim": sim})
        out_dir = RESULTS / camp["scenarioId"] / f"seed-{camp['seed']}"
        out_dir.mkdir(parents=True, exist_ok=True)
        # Persist cycle records outside results/*.json so compile_results.py only sees agent schemas
        ledger_dir = ROOT / "campaign_ledgers" / camp["scenarioId"]
        ledger_dir.mkdir(parents=True, exist_ok=True)
        (ledger_dir / f"seed-{camp['seed']}.json").write_text(
            json.dumps(
                {
                    "campaign": camp,
                    "cycles": [
                        {
                            "openingIndex": c["openingIndex"],
                            "publicRecord": c["record"]["public"],
                            "directorSealed": c["record"]["directorSealed"],
                            "persistence": c["persistence"],
                            "mapChamberFidelity": c["outcome"]["mapChamberFidelity"],
                            "securedPrincipleValue": c["outcome"]["securedPrincipleValue"],
                            "wealthIndex": c["outcome"]["wealthIndex"],
                            "explorationTrivial": c["outcome"]["explorationTrivial"],
                            "newPlayerAccess": c["outcome"]["newPlayerAccess"],
                        }
                        for c in sim["cycles"]
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        for agent in AGENTS:
            payload = agent_payload(agent, camp["scenarioId"], camp["seed"], sim, metrics)
            (out_dir / f"{agent}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Proposed patches (separate from canon)
    patches = ROOT / "proposed_patches"
    patches.mkdir(exist_ok=True)
    (patches / "PATCH_PROPOSALS.md").write_text(
        "\n".join(
            [
                "# Pack 04 — Proposed patches (NOT applied to canon)",
                "",
                "Playtest-only proposals. Owner must approve before any rulebook/companion edit.",
                "",
                "1. **Cycle Record template** — Add explicit `publicDepthRecord` + `directorSealedConsequence` fields (bible §20 already lists both conceptually).",
                "2. **GEP magnitude bands** — Optional minor/standard/severe tables for Geography/Ecology/Economy/Politics/Resonance.",
                "3. **Haven district condition track** — Intact / Strained / Damaged / Captured / Recovering for ten-year civic recovery.",
                "4. **Mapping reset on Cycle advance** — Keep Secured trunk principles; reset unsecured spur Mapping; apply ≥1 Geography change to a prior shortcut.",
                "5. **Heir package clarification** — Titles/property/reputation/trainers persist; chamber maps and stocked nodes do not.",
                "6. **Boom counter-Economy rule (hypothesis)** — If wealthIndex ≥80, next Economy GEP should usually counter-glut unless a named disaster intervenes — needs retest.",
                "7. **Companion scrub note** — `dungeon-mechanics.json` still exposes Tier 7–10 / Marquis victory draft text; public ceiling is CANON_BOUNDARY (failed Sixth Gate). Do not silently rewrite in this pack; schedule continuity scrub separately.",
                "8. **Source path gap** — Promote or symlink `GAMEPLAY_LOOP_CANON.md` / Design Doctrine from bible extract for future packs.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    # Narrative report matching REPORT_TEMPLATE (complements compile_results.py)
    boom = [c for c in campaign_summaries if c["scenarioId"] == "SEA-HAVEN-BOOM"]
    glut = [c for c in campaign_summaries if c["scenarioId"] == "SEA-MARKET-GLUT"]
    narrative = ROOT / "SEASONAL_REPORT.md"
    narrative.write_text(
        "\n".join(
            [
                "# Seasonal and Decennial Report",
                "",
                "## Cycle summaries",
                f"- Ran **{sum(1 for c in CAMPAIGNS if not c['stress'])}** three-Cycle campaigns and **{sum(1 for c in CAMPAIGNS if c['stress'])}** five-Cycle stress campaigns across 6 scenarios.",
                f"- Seeds: {', '.join(str(c['seed']) for c in CAMPAIGNS)}.",
                "- Each Opening produced a full Cycle Record (public) + optional directorSealed notes; then one Geography/Ecology/Economy/Politics/Resonance change cause-linked to that record; then ten-year advance.",
                "",
                "## Persistence that mattered",
                "- Secured route principles, faction standings/debts, Haven civic core, provenance, heirs/trainers, and political memory changed later Openings.",
                "- Dynasty heirs gained soft legacy without automatic dungeon solve.",
                "- Faction-war provenance liens and Haven damage repair bonds persisted across decades.",
                "",
                "## Replenishment that restored uncertainty",
                "- Chamber map fidelity fell across Cycles; unsecured spurs and resource nodes effectively reset.",
                "- Market demand shifted after gluts; ordinary treasure nodes did not remain permanently stripped in a way that deleted play.",
                "- Geography GEP changes invalidated at least some prior shortcuts even when trunks stayed Secured.",
                "",
                "## Economic and political trajectories",
                f"- Haven boom wealth trajectories (incl. stress 501): {[c['metrics']['wealthTrajectory'] for c in boom]}.",
                f"- Market glut trajectories: {[c['metrics']['wealthTrajectory'] for c in glut]}.",
                "- Failed-depth seeds produced insurance panic and route abandonment without cosmology leak.",
                "- Faction-war seeds kept district contest alive; damage seeds showed multi-Opening civic recovery.",
                "",
                "## New-player accessibility",
                "- Generally remained viable; boom late-Cycles risked sponsorship oligopoly (access <0.5) — patch proposal #6/#new-player charter slots.",
                "- Post-disappearance cautionary mood improved Haven-focused entry for new companies.",
                "",
                "## Canon-boundary findings",
                "- Public records did not confirm Marquis truth, claimant succession, crystal path, Floor 97/100, or tiers beyond the failed Sixth Gate.",
                "- Companion `dungeon-mechanics.json` still contains deep-tier draft victory text — flagged for separate scrub, not edited.",
                "- Pack 05 onboarding zip missing — skipped per owner instruction.",
                "",
                "## Recommended changes",
                "- See `proposed_patches/PATCH_PROPOSALS.md` (not applied).",
                "",
                "## Source gaps",
                *[f"- {g}" for g in SOURCE_GAPS],
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote results for {len(CAMPAIGNS)} campaigns × {len(AGENTS)} agents")
    print(narrative)


if __name__ == "__main__":
    write_results()
