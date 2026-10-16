"""Build a read-only, offline navigation snapshot without changing game sources."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote, unquote, urlsplit
import hashlib
import json
import zipfile

G = Path(__file__).resolve().parents[3]
R = G / "DescentReviewChanges/ReviewBible"
A = G / "docs/audit/2026-10-08/full-game"
LEDGER = R / "data/playtest/game_development_coverage.json"
TEMPLATE = Path(__file__).with_name("review_map_template.html")
OUT = G / "REVIEW_MAP.html"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def group(number):
    if number in [0, 1, 4, 5, 6, 7, 8, 9, 10]:
        return "Game and characters"
    if 11 <= number <= 14:
        return "Magic and feats"
    if number in [2, 3] or 15 <= number <= 24:
        return "Checks and combat"
    if number <= 32:
        return "Equipment and crafting"
    if number <= 38:
        return "Creatures and encounters"
    if number <= 46:
        return "Expeditions and society"
    if number <= 52:
        return "World and cosmology"
    if number <= 57:
        return "Director procedures"
    if number <= 62:
        return "Teaching and reference"
    return "Software and delivery"


def verify_current_binding(rel, expected_sha):
    current_sha = digest(G / rel)
    if current_sha == expected_sha:
        return
    correction = read(A / "FEAT327_ACQ_02_DERIVED_OPERATIONS.json")
    entries = {entry["after"]["path"]: entry for entry in correction["changes"]}
    coverage_deltas = [read(A / name) for name in [
        "FEAT_EXACT_01_WARRIOR_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_TRAINING_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_OWNED_FEAT_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_INITIATE_REVIEW_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_LINEAGE_COVERAGE_DELTA.json",
        "FEAT327_ACQ_03_SOURCE_COVERAGE_DELTA.json",
        "FEAT327_ACQ_03_FULFILLMENT_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_COMPOSITE_CASTING_COVERAGE_DELTA.json",
        "FEAT327_ACQ_04_SOURCE_AND_CHAINS_COVERAGE_DELTA.json",
        "FEAT327_ACQ_04_FULFILLMENT_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_PRODIGY_AND_ACQ05_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_CHOICES_AND_ACQ05_SOURCE_COVERAGE_DELTA.json",
        "FEAT327_ACQ_05_FULFILLMENT_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_FIXED_MENUS_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_CASTING_SELECTIONS_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_COVERAGE_DELTA.json",
        "FEAT335_ACQUISITION_AUDIT_01_SUBMISSION_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_MANEUVERS_USE_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_GADGET_USE_COVERAGE_DELTA.json",
        "FEAT_EXACT_01_FLORA_ACQUISITION_COVERAGE_DELTA.json",
    ]]
    acq03 = read(A / "FEAT327_ACQ_03_DERIVED_OPERATIONS.json")
    acq04 = read(A / "FEAT327_ACQ_04_DERIVED_OPERATIONS.json")
    acq05 = read(A / "FEAT327_ACQ_05_DERIVED_OPERATIONS.json")
    chain = list(entries.values()) + acq03["changes"] + acq04["changes"] + acq05["changes"] + coverage_deltas + read(A / "DI7_AND_FEAT335_AUDIT_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_ACQUISITION_AUDIT_01_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_FAA_FOLLOWTHROUGH_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_FAA04_NUMERIC_BINDING_ADAPTATION.json")["changes"] + read(A / "FEAT335_FAA03_PROFILE_BRIDGE_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_FAA_CORRECTIONS_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_SHARED_STATES_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_CURSE_CAPACITY_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_DEFERRED_STATES_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_FIXED_SNAPSHOTS_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_CONDITIONAL_PRESERVATION_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_ALLOWANCE_ASSEMBLY_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_FULL_REVIEW_PREFLIGHT_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_CADENCE_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_CADENCE_AND_FLORA_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_BORROWED_STUNTS_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_BORROWED_TRANSACTIONS_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_FLORA_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_FLORA_FULFILLMENT_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_BORROWED_SKILL_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_VERDANT_AND_NATURE_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_FLORA_PHYSICAL_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_COPY_SOURCES_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_NATURE_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_COPY_CAPTURE_NATURE_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_JOINT_SUBMISSION_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_NATURE_TRANSACTIONS_PROGRESS_DELTA.json")["changes"] + read(A / "NATURE_FULFILLMENT_DI7_VERDICT_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_AP_AS_01_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_CANDIDATE_ASSEMBLY_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_CAST_TRANSACTIONS_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_ACQ19_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_FATE_ACQ19_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_SHIELD_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_SHIELD_LATE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_SHIELD_LATE_ACQUISITION_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_VISION_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_GEOMETRY_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_FACTION_GEOMETRY_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_MASS_GEOMETRY_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_CLOCK_SUPREME_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_SUPREME_SHAMAN_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_SHAMAN_EXECUTION_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_FINITE_INVENTORY_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_BOUNDARY_COPY_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_EXACT_SUBMISSION_PROGRESS_DELTA.json")["changes"] + read(A / "FEAT335_COPY_RELEASE_QUESTIONS_PROGRESS_DELTA.json")["changes"] + read(A / "PACKAGING_OWNER_NAVIGATION_PROGRESS_DELTA.json")["changes"] + read(A / "DI7_EXACT_ACCEPTANCE_RECORDING_OPERATIONS.json")["changes"] + read(A / "DI7_ACCEPTANCE_RESUME_NAVIGATION_DELTA.json")["changes"] + read(A / "FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json")["changes"] + read(A / "COPY_SOURCE_COSMOLOGY_NAVIGATION_DELTA.json")["changes"] + read(A / "CREATION_ORIGIN_COMPLETION_NAVIGATION_DELTA.json")["changes"] + read(A / "GODS_FOLLOWUP_01_NAVIGATION_DELTA.json")["changes"] + read(A / "GODS_PANTHEONS_COMPLETION_01_NAVIGATION_DELTA.json")["changes"] + read(A / "OWNER_RECONCILIATION_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"] + read(A / "OWNER_ADOPTION_WEBSITE_SOURCE_01_NAVIGATION_DELTA.json")["changes"] + read(A / "HEARTCELL_OWNER_UPDATE_02_NAVIGATION_DELTA.json")["changes"] + read(A / "Q6_PLANES_SOULS_READING_01_NAVIGATION_DELTA.json")["changes"] + read(A / "SOULS_HUNT_DRAFT_01_NAVIGATION_DELTA.json")["changes"] + read(A / "EQUATION_LIBRARY_INVENTORY_01_NAVIGATION_DELTA.json")["changes"] + read(A / "EQUATION_RESEARCH_INTERFACE_01_NAVIGATION_DELTA.json")["changes"] + read(A / "PART3_CHRONOLOGY_01_NAVIGATION_DELTA.json")["changes"] + read(A / "PLANES_SOULS_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]
    visited = set()
    while expected_sha != current_sha:
        assert expected_sha not in visited, ("Cyclic binding history", rel)
        visited.add(expected_sha)
        matches = [entry for entry in chain if entry["after"]["path"] == rel
                   and entry["before"]["sha256"] == expected_sha]
        assert len(matches) == 1, ("Unrecorded or ambiguous current-file change", rel)
        entry = matches[0]
        assert digest(G / entry["before"]["preservedCopy"]) == expected_sha, rel
        expected_sha = entry["after"]["sha256"]


def main():
    ledger = read(LEDGER)
    frozen = read(A / "TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json")["manifest"]
    current_inputs = {}
    changed_since_submission = []
    # The frozen archive remains evidence of the submitted revision. TEX now
    # authorizes specific current descendants; never rewrite old expectations.
    with zipfile.ZipFile(A / "DD_Teaching_Navigation_9_Exact_Review_v1.zip") as archive:
        for rel, expected in frozen.items():
            assert hashlib.sha256(archive.read(rel)).hexdigest() == expected["sha256"], rel
    fulfillment = read(A / "TEACHING_TEX_EXACT_FULFILLMENT.json")
    addendum = read(A / "TEACHING_TEX_ADDENDUM_FULFILLMENT.json")
    for rel, expected in {**fulfillment["finalArtifacts"], **fulfillment["correctedCurrentCraftArtifacts"], **addendum["finalArtifacts"]}.items():
        verify_current_binding(rel, expected["sha256"])
    verify_current_binding(LEDGER.relative_to(G).as_posix(), fulfillment["coverage"]["sha256"])
    for rel, expected in frozen.items():
        p = G / rel
        if rel == "README_TEACHING_EXACT_V1.md":
            assert not p.exists(), "Expected archive-only README"
            continue
        assert p.is_file(), rel
        current_inputs[rel] = digest(p)
        if current_inputs[rel] != expected["sha256"]:
            changed_since_submission.append(rel)
    assert len(current_inputs) == 217
    expedition = read(A / "EXPEDITION_INTEGRATED_V3_SUBMISSION.json")
    expedition_frozen = read(A / "EXPEDITION_INTEGRATED_V3_PREPARATION.json")["manifest"]
    assert expedition["savedUserMessageId"] == "999dd180-8e31-48be-ad59-58f8f65e1a1c"
    assert digest(G / expedition["archive"]["path"]) == expedition["archive"]["sha256"]
    for rel, expected in expedition_frozen.items():
        if rel == "README_EXPEDITION_INTEGRATED_V3.md":
            continue
        verify_current_binding(rel, expected["sha256"])
        current_inputs[rel] = digest(G / rel)
    areas = ledger["aspects"]
    assert len(areas) == 75 and len({x["id"] for x in areas}) == 75
    missing, links = [], set()

    def ref(rel):
        parts = urlsplit(rel)
        assert not parts.scheme and not parts.netloc, rel
        path = (G / unquote(parts.path)).resolve()
        assert path.is_relative_to(G.resolve()), rel
        exists = path.is_file() or path.is_dir()
        (links if exists else set()).add(rel)
        if not exists:
            missing.append(rel)
        return {"path": rel, "label": path.name + ("/" if path.is_dir() else ""), "url": quote(parts.path, safe="/") + ("/" if path.is_dir() else "") + ("#" + quote(parts.fragment) if parts.fragment else ""), "exists": exists}

    result = []
    fields = ["draftEvidence", "sourceEvidence", "reviewEvidence", "validationEvidence", "humanEvidence"]
    for area in areas:
        entry = {k: area.get(k, [] if k in ["completedScopes", "openIssues"] else "") for k in ["id", "number", "domain", "requiredCoverage", "acceptanceGate", "status", "closure", "completionClass", "completedScopes", "openIssues"]}
        entry["group"] = group(area["number"])
        entry["references"] = {key: [ref(p) for p in area.get(key, [])] for key in fields}
        result.append(entry)

    ex58_addendum = read(A / "EX58_COVERAGE_ADDENDUM.json")
    verify_current_binding(LEDGER.relative_to(G).as_posix(), ex58_addendum["baseLedger"]["sha256"])
    for key in ["fulfillment", "labels"]:
        binding = ex58_addendum[key]
        assert digest(G / binding["path"]) == binding["sha256"]
        current_inputs[binding["path"]] = binding["sha256"]
    ex58_status_path = R / "docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json"
    ex58_status = read(ex58_status_path)
    assert ex58_status["exactCandidateAuthoredApproval"] is True
    for rel, binding in ex58_status["currentArtifactBindings"].items():
        assert digest(G / rel) == binding["sha256"]
        current_inputs[rel] = binding["sha256"]
    current_inputs[ex58_status_path.relative_to(G).as_posix()] = digest(ex58_status_path)
    current_inputs["docs/audit/2026-10-08/full-game/EX58_COVERAGE_ADDENDUM.json"] = digest(A / "EX58_COVERAGE_ADDENDUM.json")
    for entry in result:
        if entry["id"] in ex58_addendum["scopes"]:
            entry["completedScopes"] = list(entry["completedScopes"]) + [ex58_addendum["scopes"][entry["id"]]]
            entry["status"] = "EX58 authored interfaces reviewed; broader domain open"
            entry["openIssues"] = ["EX58 exact-candidate work is fulfilled. Older EX58 source-preparation/review-queue notes below are retained history, superseded within the named reviewed scope. Other domain work remains open."] + list(entry["openIssues"])
            entry["references"]["reviewEvidence"].append(ref("docs/audit/2026-10-08/full-game/ex58-exact-gpt-verdict/EX58_EXACT_VERDICT.md"))
            entry["references"]["validationEvidence"].append(ref("docs/audit/2026-10-08/full-game/EX58_X01_FULFILLMENT.json"))
    feat_dispatch = read(A / "FEAT_AUTHORED_V3_SUBMISSION.json")
    assert feat_dispatch["sent"] is True and feat_dispatch["requestId"] == "bf9d8dbb-22e3-4c31-a046-74608129acb9"
    for binding in [feat_dispatch["archive"], *feat_dispatch["currentNavigationArtifacts"]]:
        assert digest(G / binding["path"]) == binding["sha256"]
        current_inputs[binding["path"]] = binding["sha256"]
    current_inputs["docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_SUBMISSION.json"] = digest(A / "FEAT_AUTHORED_V3_SUBMISSION.json")
    featured = [
        ("DI7 Shaman casting-interface clarification", "DescentReviewChanges/ReviewBible/docs/spells/candidates/DI7_SHAMAN_CASTING_INTERFACE.md"),
        ("Seven Divination candidates \u2014public complete cards, unapproved", "DescentReviewChanges/ReviewBible/data/public/spell_candidates/divination_rank7_exact_01.json"),
        ("Seven Divination candidates \u2014internal full source envelope", "DescentReviewChanges/ReviewBible/data/director/spell_candidates/divination_rank7_exact_01.json"),
        ("Seven Divination candidates \u2014readable manuscript", "DescentReviewChanges/ReviewBible/docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md"),
        ("Seven rank-seven Divination drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/DIVINATION_RANK7.md"),
        ("Complete feat candidate — 325 procedures plus two deferred wrappers", "DescentReviewChanges/ReviewBible/docs/feats/exact-candidate-01/README.md"),
        ("GPT feat source verdict — exact candidate pending", "docs/audit/2026-10-08/full-game/feat327-source-verdict/FEAT327_FINAL_SOURCE_VERDICT.md"),
        ("13 new rank-six Transmutation and Universal drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/TRANSMUTATION_UNIVERSAL_RANK6.md"),
        ("5 new rank-six Divination drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/DIVINATION_RANK6.md"),
        ("11 new rank-six Abjuration/Conjuration drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ABJURATION_CONJURATION_RANK6.md"),
        ("13 new rank-six Illusion/Necromancy drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ILLUSION_NECROMANCY_RANK6.md"),
        ("7 new rank-six Enchantment drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ENCHANTMENT_RANK6.md"),
        ("8 new rank-six Evocation drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/EVOCATION_RANK6.md"),
        ("11 new rank-five Divination and Universal drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/DIVINATION_UNIVERSAL_RANK5.md"),
        ("11 new rank-five Abjuration and Conjuration drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ABJURATION_CONJURATION_RANK5.md"),
        ("16 new rank-five Necromancy and Transmutation drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/NECROMANCY_TRANSMUTATION_RANK5.md"),
        ("14 new rank-five Enchantment and Illusion drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ENCHANTMENT_ILLUSION_RANK5.md"),
        ("327 pending feats — complete procedures submitted to GPT", "docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_REVIEW_GUIDE.md"),
        ("Feat conference submission and preserved sources", "docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_SUBMISSION.json"),
        ("Reviewed expedition player book", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md"),
        ("Reviewed expedition Director book", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md"),
        ("Expedition review status and current hashes", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json"),
        ("28 expedition boundary walkthroughs", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_BOUNDARY_WALKTHROUGHS.md"),
        ("24 complete social walkthroughs", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/SOCIAL_SCENARIO_WALKTHROUGHS.md"),
        ("Start here", "START_HERE.md"),
        ("First Bard character", "DescentReviewChanges/ReviewBible/docs/playtest/FIRST_BARD_WALKTHROUGH.md"),
        ("All 17 class families", "DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md"),
        ("Paladin Oaths and Oathbreakers", "DescentReviewChanges/ReviewBible/docs/mechanics/PALADIN_OATHS_AND_OATHBREAKERS.md"),
        ("Reviewed spell index", "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"),
        ("Reviewed recipe index", "DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md"),
        ("Reviewed character sheet", "DescentReviewChanges/ReviewBible/output/pdf/Decennium_Descent_Character_Sheet_Playtest.pdf"),
        ("Source authority", "docs/canon/CANON_MANIFEST.json"),
        ("Full review history", "docs/audit/2026-10-08/full-game/GPT_REVIEW_CONTINUATION_HANDOFF.md"),
        ("All feats — reviewed work, proposed procedures and remaining questions", "DescentReviewChanges/ReviewBible/docs/feats/FEAT_OPERATING_PROPOSAL_INDEX.md"),
        ("Higher spells — proposed procedures and remaining source questions", "DescentReviewChanges/ReviewBible/docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md"),
        ("Expedition player chapter — first seven directions (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART01_PLAYER.md"),
        ("Expedition Director chapter — first seven directions (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART01_DIRECTOR.md"),
        ("Routes, extraction and retreat — player chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART02_PLAYER.md"),
        ("Routes, extraction and retreat — Director chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART02_DIRECTOR.md"),
        ("Haven, settlement and advancement — player chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART03_PLAYER.md"),
        ("Haven, settlement and advancement — Director chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART03_DIRECTOR.md"),
        ("Social scenes and faction activity — player chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART04_PLAYER.md"),
        ("Social scenes and faction activity — Director chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART04_DIRECTOR.md"),
        ("Mounts, vehicles and transport — player chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART05_PLAYER.md"),
        ("Mounts, vehicles and transport — Director chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART05_DIRECTOR.md"),
        ("Reputation and background standing — player chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART06_PLAYER.md"),
        ("Reputation preservation and institutions — Director chapter source (reviewed in complete book)", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART06_DIRECTOR.md"),
        ("A complete expedition — integrated worked candidate", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_INTEGRATED_WALKTHROUGH.md"),
        ("Integrated expedition — complete synthetic records", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_INTEGRATED_RECORDS.md"),
        ("Complete transport catalogue — candidate profiles", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/TRANSPORT_CATALOGUE_CANDIDATE.md"),
        ("Current source verdict with the confirmed assay correction", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EX58_SOURCE_VERDICT_CORRECTED.md"),
        ("Current source contracts with the confirmed five offices", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md"),
    ]
    featured = [{**ref(p), "label": label} for label, p in featured]
    pending = [
        ('Souls/Research — 21 issues and 34 situations submitted in Part 3', 'COSMOLOGY_SOULS_RESEARCH_01_SUBMISSION_RECEIPT.json'),
        ('Planes — corrected scoped successor verified and applied', 'COSMOLOGY_PLANES_01_APPLICATION_CHECK.json'),
        ('Planes — resumed in owner-created Part 3; submission receipt', 'CALIBRATION_REVIEW_PART_3_SUBMISSION_RECEIPT_01.json'),
        ('Chronology and research sites — 173 source locations; joint review pending', 'COSMOLOGY_CHRONOLOGY_RESEARCH_SITES_DRAFT_01_CHECK.json'),
        ('Equation Research — procedure/worksheet and 14 situations; joint review pending', 'COSMOLOGY_EQUATION_RESEARCH_INTERFACE_DRAFT_01_CHECK.json'),
        ('Equation libraries — 22 records and 125 source locations; joint review pending', 'COSMOLOGY_EQUATION_LIBRARY_SOURCE_INVENTORY_01_CHECK.json'),
        ('Souls/Hunt — draft citations verified; joint review pending', 'COSMOLOGY_SOULS_DEATH_HUNT_DRAFT_01_CITATION_CHECK.json'),
        ('Soul Mirror — current authored status correction', 'COSMOLOGY_SOULS_DEATH_AUTHORED_STATUS_CORRECTION_01.json'),
        ('Taint/Research — original enforcement and actual cure sources', 'COSMOLOGY_TAINT_RESEARCH_SOURCE_READING_04.json'),
        ('Q6 — verified return and current Director application', 'COSMOLOGY_Q6_LATER_LOCK_01_APPLICATION_CHECK.json'),
        ('Planes — historical Part 2 length-limit receipt', 'COSMOLOGY_PLANES_01_LENGTH_LIMIT_RECEIPT.json'),
        ('Continuation — preserved original Part 3 handoff', 'CALIBRATION_REVIEW_PART_3_HANDOFF_01.txt'),
        ('Souls and death — bounded source reading, no new mechanics', 'COSMOLOGY_SOULS_DEATH_SOURCE_READING_01_CHECK.json'),
        ('Heartcell owner update — original sources, ages, taint and Hunt', 'HEARTCELL_OWNER_UPDATE_02_RECEIVED_DECISION.json'),
        ('Q6 — historical terminal capture; archive now verified', 'COSMOLOGY_Q6_LATER_LOCK_01_TERMINAL_THREAD_CAPTURE.json'),
        ('Planes — 76 source claims, provisional inventory', 'COSMOLOGY_PLANES_SOURCE_INVENTORY_DRAFT_01_CHECK.json'),
        ('Owner cosmology corrections — reviewed and applied', 'COSMOLOGY_OWNER_RECONCILIATION_01_ADOPTION_CHECK.json'),
        ('Saved cosmology website — source audit and backup verification', 'COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json'),
        ('Q6 later lock — focused review submitted once', 'COSMOLOGY_Q6_LATER_LOCK_01_SUBMISSION.json'),
        ('Planes preparation — Director context and frozen Blink receipts', 'COSMOLOGY_PLANES_DIRECTOR_AND_RECEIPT_READING_01.json'),
        ('Planes preparation — six reviewed counterpart cards', 'COSMOLOGY_PLANES_REVIEWED_COUNTERPART_READING_01.json'),
        ('Owner corrections — source reconciliation sent once', 'COSMOLOGY_OWNER_RECONCILIATION_01_SUBMISSION.json'),
        ('Owner source priority — exact message; human clarification pending', 'COSMOLOGY_OWNER_SOURCE_PRIORITY_2026_10_15_CAPTURE.json'),
        ('Source search — encoding recovery; nine errors resolved', 'COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json'),
        ('Source search — twelve archive indexes', 'COSMOLOGY_OWNER_RECONCILIATION_01_ARCHIVE_INDEX_CHECK.json'),
        ('Planes preparation — twelve transit cards and two unadopted procedures', 'COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json'),
        ('Current Director Interstice — exact counterpart/source check', 'COSMOLOGY_DIRECTOR_INTERSTICE_SOURCE_CHECK_01.json'),
        ('Gods/pantheons — original returned evidence, superseded by corrected successor', 'COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json'),
        ('Gods/pantheons — exact citation check', 'COSMOLOGY_GODS_PANTHEONS_01_CITATION_CHECK.json'),
        ('Gods/pantheons — corrected companion verified; seventeen dependencies', 'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_APPLICATION_CHECK.json'),
        ('Planes — preliminary source and spell concordance', 'COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json'),
        ('Matrix — original formula source gaps checked', 'COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json'),
        ("Current player publication — eight patch anchors verified", "COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json"),
        ("Cosmology authority verdict — six findings, bounded scope", "COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json"),
        ("Creation/origins — nine comparisons reviewed, eleven open dependencies", "COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json"),
        ("DI7 exact authored acceptance — seven recorded", "DI7_EXACT_ACCEPTANCE_RECEIPT.json"),
        ("Copy-release source rulings — applied; behavior pending", "FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json"),
        ("Pact sigils — 140 checks, 45 conditional histories", "FEAT335_PACT_SIGILS_CHECK.json"),
        ("Player/Director packaging inventory — release gate open", "PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json"),
        ("Prepared copy-release source questions \u2014 not sent", "FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json"),
        ("Complete copy-release source question archive", "DD_Feat335_Copy_Release_Source_01.zip"),
        ("Three exact source questions and scope", "feat335-copy-release-source-01-input/REQUEST.txt"),
        ("Actual complete DI7 exact submission \u2014GPT response pending", "DI7_EXACT_REVIEW_01_SUBMISSION.json"),
        ("Complete213-payload exact review archive", "DD_DI7_Exact_Review_01.zip"),
        ("Fate mode gate \u201443 checks,12 paid histories and11 scoped source proofs", "DI7_FATE_MODE_ADMISSION_CHECK.json"),
        ("Exact-review request and evidence qualifications", "di7-exact-review-01-input/REQUEST.txt"),
        ("Exact submission visible proof", "DI7_EXACT_REVIEW_01_SENT.png"),
        ("Exact fractional cone and copied alignment source —82 checks in24 histories", "DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json"),
        ("Copied alignment source lookup —preserved previous evaluator and inverse", "DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json"),
        ("DI7 all93-case evidence inventory —explicit remaining gaps", "DI7_FINITE_93_EVIDENCE_INVENTORY.json"),
        ("Paid alignment transactions —136 checks in32 histories", "DI7_ALIGNMENT_TRANSACTIONS_CHECK.json"),
        ("Shaman paid casting interface —62 checks in26 histories; all9 source expectations", "DI7_SHAMAN_TRANSACTIONS_CHECK.json"),
        ("Supreme historical payload \u201474 checks in31 conditional histories, all8 temporal cases", "DI7_SUPREME_TRANSACTIONS_CHECK.json"),
        ("GPT Shaman vent checkpoint \u2014terminal existing-source clarification", "DI7_SHAMAN_VENT_RECEIVED.json"),
        ("Shaman shared interface \u2014preserved original files and inverse proof", "DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json"),
        ("Exact Shaman interface text received from GPT", "DI7_SHAMAN_VENT_CLARIFICATION.txt"),
        ("Suggestion original virtual clock and paid Fate child \u201458 checks in22 histories", "DI7_ALIGNMENT_CLOCK_CHECK.json"),
        ("GPT Supreme historical scope ruling \u2014terminal source addendum", "DI7_SUPREME_TIME_SCOPE_RECEIVED.json"),
        ("Supreme time-scope insertion \u2014exact source text", "DI7_SUPREME_TIME_SCOPE_INSERTION.txt"),
        ("Supreme time-scope originals and inverse proof", "DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json"),
        ("Faction current evidence \u201481 checks in36 conditional histories", "DI7_FACTION_TRANSACTIONS_V2_CHECK.json"),
        ("GPT Faction targeting correction \u2014terminal received", "DI7_FACTION_REFERENCE_RECEIVED.json"),
        ("Faction correction preserved originals and exact inverse proof", "DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json"),
        ("Geometry19 source expectations executed \u201485 checks in41 histories", "DI7_AREA_GEOMETRY_CHECK.json"),
        ("Mass Revelation four-category payload \u201473 checks in29 histories", "DI7_MASS_TRANSACTIONS_CHECK.json"),
        ("Supreme original temporal-scope question \u2014terminal addendum received and applied", "DI7_SUPREME_TIME_SCOPE_QUESTION.txt"),
        ("Faction Omniscience \u201463 checks in28 conditional histories", "DI7_FACTION_TRANSACTIONS_CHECK.json"),
        ("GPT geometry ruling \u2014terminal scoped source addendum", "DI7_GEOMETRY_3D_RECEIVED.json"),
        ("Geometry exact edits \u2014originals preserved and inverse verified", "DI7_GEOMETRY_DERIVED_OPERATIONS.json"),
        ("Faction original wording question \u2014terminal correction received; see ruling", "DI7_FACTION_REFERENCE_QUESTION.txt"),
        ("Vision Quest current lifecycle and private answers \u201497 checks in44 conditional histories", "DI7_VISION_TRANSACTIONS_V2_CHECK.json"),
        ("Vision communication refinement \u2014preserved helper and inverse proof", "DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json"),
        ("Vision initial bounded evidence \u201484 checks in41 histories; see current97/44", "DI7_VISION_TRANSACTIONS_CHECK.json"),
        ("Shield timing source ruling received \u2014family-wide first-admission closure", "DI7_SHIELD_LATE_ADMISSION_RECEIVED.json"),
        ("Shield exact operative amendments \u2014preservation and inverse proof", "DI7_SHIELD_LATE_DERIVED_OPERATIONS.json"),
        ("Current Shield evaluator \u201495 checks in36 conditional histories", "DI7_SHIELD_LATE_TRANSACTIONS_CHECK.json"),
        ("All-seven acquisition matrix \u2014385 checks in77 conditional histories", "DI7_ALL_SEVEN_ACQUISITION_CHECK.json"),
        ("Shield timing ruling \u2014visible completed GPT response", "DI7_SHIELD_LATE_ADMISSION_RECEIVED.png"),
        ("Premonition Shield paid wards and conditional occurrences \u201468 checks in27 histories", "DI7_SHIELD_TRANSACTIONS_CHECK.json"),
        ("Original Shield timing question \u2014see received applied amendment", "DI7_SHIELD_LATE_ADMISSION_SUBMISSION.json"),
        ("Complete Shield source timing question", "DI7_SHIELD_LATE_ADMISSION_QUESTION.txt"),
        ("Shield timing question submitted \u2014visible proof", "DI7_SHIELD_LATE_ADMISSION_SENT.png"),
        ("Fate Echo paid composites and Ready \u201468 checks in34 conditional histories", "DI7_FATE_TRANSACTIONS_CHECK.json"),
        ("DI7-ACQ19 received KEEP ruling \u2014rank eligibility is not acquisition", "DI7_ACQ19_RECEIVED.json"),
        ("DI7-ACQ19 exact expectation change \u2014preserved original and inverse proof", "DI7_ACQ19_DERIVED_OPERATIONS.json"),
        ("DI7-ACQ19 completed GPT response \u2014visible proof", "DI7_ACQ19_RECEIVED.png"),
        ("DI7 actual conditional cast commitments and nested counters \u2014185 checks", "DI7_CAST_TRANSACTIONS_CHECK.json"),
        ("DI7-ACQ19 original question \u2014see received KEEP clarification", "DI7_ACQ19_SUBMISSION.json"),
        ("DI7-ACQ19 complete source packet", "DD_DI7_ACQ19_Clarification.zip"),
        ("DI7-ACQ19 visible dispatch proof", "DI7_ACQ19_SENT.png"),
        ("DI7 complete candidate assembly \u2014182 preservation and parity checks", "DI7_EXACT_01_ASSEMBLY_CHECK.json"),
        ("DI7 alignment component \u201464 behavior assertions in26 conditional histories", "DI7_ALIGNMENT_COMPONENT_CHECK.json"),
        ("DI7 current readiness \u2014full casting and finite follow-through remain", "DI7_EXACT_01_CURRENT_READINESS.json"),
        ("AP-AS-01 applied counterpart changes \u2014preserved originals and exact inverse", "DI7_AP_AS_01_DERIVED_OPERATIONS.json"),
        ("AP-AS-01 controlling active readers", "DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json"),
        ("Nature finite47-variant fulfillment and exact evidence matrix", "FEAT335_NATURE_FINITE_FULFILLMENT.json"),
        ("Nature ordinary cast and actual Fate Coin integration \u201477 checks", "FEAT335_NATURE_SPELL_INTEGRATION_CHECK.json"),
        ("Nature finite fulfillment \u2014scope and wider limits", "FEAT335_NATURE_FINITE_FULFILLMENT_SCOPE.json"),
        ("DI7 source-authoring verdict \u2014received26 payloads", "DI7_JOINT_REVIEW_01_RECEIVED.json"),
        ("DI7 checks \u2014484 plus150 reproduced", "DI7_JOINT_REVIEW_01_REPRODUCED.json"),
        ("DI7 complete source directions", "di7-joint-review-01-verdict/DI7_COMPLETE_OPERATING_DIRECTIONS.md"),
        ("DI7 later exact-review requirements", "di7-joint-review-01-verdict/DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json"),
        ("DI7 received verdict \u2014visible proof", "DI7_JOINT_REVIEW_01_RECEIVED.png"),
        ("Nature transactions \u2014185 checks,75 conditional histories", "FEAT335_NATURE_TRANSACTIONS_CHECK.json"),
        ("Nature earlier scope \u2014two gaps subsequently closed in finite fulfillment", "FEAT335_NATURE_TRANSACTIONS_SCOPE.json"),
        ("DI7 historical browser timeout \u2014subsequently recovered", "DI7_BROWSER_OBSERVATION_AFTER_NATURE_TRANSACTIONS.json"),
        ("DI7 original dispatch \u2014sent once; see received verdict", "DI7_JOINT_REVIEW_01_SUBMISSION.json"),
        ("DI7 complete source package \u201458 payloads", "DI7_JOINT_REVIEW_01_PREPARATION.json"),
        ("DI7 dispatch and unchanged-rule checks", "DI7_JOINT_REVIEW_01_DISPATCH_CHECK.json"),
        ("DI7 visible GPT submission", "DI7_JOINT_REVIEW_01_SENT.png"),
        ("Paid copy capture \u2014189 checks,31 histories", "FEAT335_COPY_CAPTURE_CHECK.json"),
        ("Copy capture \u2014scope and pending paid release", "FEAT335_COPY_CAPTURE_SCOPE.json"),
        ("Nature source propagation \u2014137 preservation checks", "FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json"),
        ("Nature controlling addendum and exact descendants", "FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json"),
        ("Nature reviewer checks \u2014124 reproduced", "FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json"),
        ("Nature16 authored expectation groups \u2014see later47-variant fulfillment", "feat335-nature-source-check-01-verdict/FINITE_NATURE_EXPECTATIONS.json"),
        ("Seven feat-copy source components \u2014248 checks,35 scenarios", "FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json"),
        ("Copy-source scope \u2014capture and release still pending", "FEAT335_COPY_SOURCE_COMPONENTS_SCOPE.json"),
        ("Flora physical interfaces \u2014148 checks,34 histories", "FEAT335_FLORA_PHYSICAL_INTERFACES_CHECK.json"),
        ("Flora task/terrain/inspection \u2014 scope and remaining integrations", "FEAT335_FLORA_PHYSICAL_INTERFACES_SCOPE.json"),
        ("Verdant message and simple plant communication \u201492 checks,19 histories", "FEAT335_VERDANT_MESSAGE_CHECK.json"),
        ("Verdant message \u2014 conditional scope and remaining work", "FEAT335_VERDANT_MESSAGE_SCOPE.json"),
        ("Nature Whisper source questions \u2014 actual GPT submission", "FEAT335_NATURE_SOURCE_CHECK_01_SUBMISSION.json"),
        ("Nature Whisper \u2014 full source packet preparation", "FEAT335_NATURE_SOURCE_CHECK_01_PREPARATION.json"),
        ("Borrowed class skill transactions \u2014362 checks,38 histories", "FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json"),
        ("Borrowed class skills \u2014 finite scope and remaining integration", "FEAT335_BORROWED_SKILL_TRANSACTIONS_SCOPE.json"),
        ("Flora \u2014 actual GPT ruling and finite fulfillment", "FEAT335_FLORA_SOURCE_CHECK_01_FINITE_FULFILLMENT.json"),
        ("Flora \u2014189 checks across all18 acceptance groups", "FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_V2_CHECK.json"),
        ("Flora \u2014 historical qualifications and remaining scope", "FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_SCOPE.json"),
        ("Flora \u2014738 guarded source propagation checks", "FEAT335_FLORA_SOURCE_PROPAGATION_CHECK.json"),
        ("Feats \u2014 current acquisition register after Flora fulfillment", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA_FULFILLMENT.json"),
        ("Flora \u2014 received complete source addendum", "feat335-flora-source-check-01-verdict/FEAT335_FLORA_SOURCE_CHECK_01_ADDENDUM.md"),
        ("Borrowed ability transactions \u2014239 checks, declared costs and later riders", "FEAT335_BORROWED_TRANSACTIONS_CHECK.json"),
        ("Borrowed transactions \u2014 remaining integration limits", "FEAT335_BORROWED_TRANSACTIONS_SCOPE.json"),
        ("Borrowed class abilities \u2014158 checks across12 cards and skill alternative", "FEAT335_BORROWED_STUNTS_USE_CHECK.json"),
        ("Borrowed-ability scope limits \u2014 retain remaining integration gates", "FEAT335_BORROWED_STUNTS_SCOPE_QUALIFICATION.json"),
        ("Current acquisition register \u2014 cadence addendum fulfilled", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CADENCE.json"),
        ("Cadence fulfillment \u2014 2290 current checks and381 reproduced", "FEAT335_CADENCE_FULFILLMENT_CHECK.json"),
        ("Flora use \u2014114 bounded checks, read qualification before relying on growth case", "FEAT335_FLORA_USE_CHECK.json"),
        ("Flora scope qualification \u2014 four concrete source questions", "FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json"),
        ("Flora source review \u2014 sent once to actual GPT", "FEAT335_FLORA_SOURCE_CHECK_01_SUBMISSION.json"),
        ("Full feat exact-review preflight \u2014 remaining finite use and case work", "FEAT335_FULL_EXACT_REVIEW_PREFLIGHT.json"),
        ("Current reading files \u20145382 checks, all688 authored positions preserved", "FEAT335_CURRENT_READING_FILES_V2_CHECK.json"),
        ("Focused cadence review \u2014 actual GPT submission receipt", "FEAT335_CADENCE_CHECK_01_SUBMISSION.json"),
        ("Current335 acquisition audit follow-through \u2014 all finite groups assembled", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_COMPLETE.json"),
        ("All335 complete acquisition source and evidence assembly", "FEAT335_COMPLETE_ACQUISITION_ASSEMBLY.json"),
        ("177 allowance descriptors \u2014111 plain plus66 specific", "FEAT335_ALLOWANCE_DESCRIPTORS.json"),
        ("Allowance and final335 assembly check \u20144307 checks", "FEAT335_ALLOWANCE_ASSEMBLY_CHECK.json"),
        ("Current335 follow-through \u2014 only finite allowance assembly remains", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CONDITIONAL_PRESERVATION.json"),
        ("Conditional and null preservation \u2014587 checks", "FEAT335_CONDITIONAL_PRESERVATION_CHECK.json"),
        ("Current335 acquisition follow-through after fixed snapshots", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FIXED_SNAPSHOTS.json"),
        ("Twenty-one exact fixed choice and training descriptors", "FEAT335_FIXED_SOURCE_SNAPSHOT_DESCRIPTORS.json"),
        ("Paid fixed-snapshot and recipient evidence \u2014555 checks", "FEAT335_FIXED_SOURCE_SNAPSHOT_CHECK.json"),
        ("Current335-row acquisition follow-through after deferred states", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_DEFERRED_STATES.json"),
        ("Twenty exact delayed or empty starting-state descriptors", "FEAT335_DEFERRED_ACQUISITION_DESCRIPTORS.json"),
        ("Paid starting-state and capacity verification \u2014301 checks", "FEAT335_DEFERRED_ACQUISITION_STATE_CHECK.json"),
        ("Preserved Curse Channeling current-level helper correction", "FEAT335_CURSE_CAPACITY_DERIVED_OPERATIONS.json"),
        ("Current335-row follow-through after shared-state assembly", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_SHARED_STATES.json"),
        ("Both shared acquisition orders \u2014203 checks", "FEAT335_SHARED_ACQUISITION_STATE_CHECK.json"),
        ("AA13 exact retained paid resource-state evidence", "FEAT335_AA13_EXISTING_EVIDENCE_BINDING_CHECK.json"),
        ("Current335-row acquisition follow-through and remaining scopes", "FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH.json"),
        ("Current correction bindings and preservation checks", "FEAT335_FAA_CORRECTIONS_CURRENT_BINDING_CHECK.json"),
        ("Corrected actual casting-provider histories", "FEAT335_FAA01_FAA02_PROVIDER_CHECK.json"),
        ("Actual unarmed and Troll Claws profile histories", "FEAT335_FAA03_UNARMED_PROFILE_CHECK.json"),
        ("Immutable historical snapshot comparison verification", "FEAT335_FAA04_IMMUTABLE_EVIDENCE_CHECK.json"),
        ("Fresh897-check acquisition history report", "FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_FAA04_CHECK.json"),
        ("Fresh11851-check numeric prerequisite report", "FEAT_EXACT_01_NUMERIC_PREREQUISITE_AFTER_FAA04_V2_CHECK.json"),
        ("Completed335-row acquisition audit \u2014 actual GPT verdict", "feat335-acquisition-audit-01-verdict/FEAT335_ACQUISITION_AUDIT_VERDICT.md"),
        ("335 individual acquisition and initial-state obligations", "feat335-acquisition-audit-01-verdict/ACQUISITION_ROWS.md"),
        ("Four findings and guarded corrections", "feat335-acquisition-audit-01-verdict/GUARDED_CORRECTIONS.json"),
        ("Finite acquisition evidence remaining", "feat335-acquisition-audit-01-verdict/FINITE_REMAINING_WORK.json"),
        ("Independent local reproduction of the scoped audit", "FEAT335_ACQUISITION_AUDIT_01_LOCAL_REPRODUCTION.json"),
        ("Divination rank7 source/rendering check", "DIVINATION_RANK7_OPERATING_PROPOSAL_CHECK.json"),
        ("Owner stop condition:50 percent weekly usage", "OWNER_USAGE_STOP_50_PERCENT_2026-10-13.json"),
        ("Feat prerequisites — all335 exact source contracts", "FEAT_EXACT_01_ACQUISITION_CONTRACTS.md"),
        ("Feat acquisition history — current reference checks", "FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json"),
        ("Feat numeric prerequisites — 209 source-qualified projections", "FEAT_EXACT_01_NUMERIC_PREREQUISITE_NOTES.md"),
        ("Feat numeric prerequisites — independent printed-string checks", "FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json"),
        ("Warrior feats — twelve acquisition examples", "FEAT_EXACT_01_WARRIOR_ACQUISITION_NOTES.md"),
        ("Warrior feats — full source-bound acquisition fixtures", "FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json"),
        ("Warrior feats — acquisition and activation checks", "FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json"),
        ("Feat training prerequisites — 48 source-qualified examples", "FEAT_EXACT_01_TRAINING_PREREQUISITE_NOTES.md"),
        ("Feat training prerequisites — complete source fixtures", "FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json"),
        ("Feat training prerequisites — 184 checked cases", "FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json"),
        ("Feat ownership — ten prerequisite chains", "FEAT_EXACT_01_OWNED_FEAT_CHAIN_NOTES.md"),
        ("Feat ownership — 32 paid histories and checks", "FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json"),
        ("Training and ownership — actual focused GPT dispatch", "FEAT327_FXC05_TRAINING_OWNERSHIP_SUBMISSION.json"),
        ("Training and ownership — focused review request", "FEAT327_FXC05_TRAINING_OWNERSHIP_REQUEST.txt"),
        ("Training and ownership — received GPT review receipt", "FEAT327_FXC05_TRAINING_OWNERSHIP_REVIEW_RECEIPT.json"),
        ("Training and ownership — complete GPT verdict", "feat327-fxc05-training-ownership-review/FEAT327_FXC05_REVIEW_VERDICT.md"),
        ("Magic Initiate — all sixteen curricula selection notes", "FEAT_EXACT_01_INITIATE_ACQUISITION_NOTES.md"),
        ("Magic Initiate — 39 paid selection histories", "FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json"),
        ("Casting prerequisites — actual ACQ-03 dispatch", "FEAT327_ACQ_03_SUBMISSION.json"),
        ("Casting prerequisites — exact ACQ-03 question", "FEAT327_ACQ_03_CASTING_PREREQUISITE_QUESTION.txt"),
        ("Casting prerequisites — actual GPT addendum", "FEAT327_ACQ_03_GPT_ADDENDUM.md"),
        ("Casting prerequisites — eight preserved source changes", "FEAT327_ACQ_03_DERIVED_OPERATIONS.json"),
        ("Casting prerequisites — independent source verification", "FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json"),
        ("Casting prerequisites — finite acceptance notes", "FEAT327_ACQ_03_CASTING_CREDENTIAL_NOTES.md"),
        ("Casting prerequisites — all recorded snapshot evidence", "FEAT327_ACQ_03_CASTING_CREDENTIAL_CHECK.json"),
        ("Casting prerequisites — finite fulfillment", "FEAT327_ACQ_03_FINITE_FULFILLMENT.json"),
        ("Combined feat prerequisites — source-qualified cases", "FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_CHECK.json"),
        ("Combined feat prerequisites — scope and remaining work", "FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_NOTES.md"),
        ("Owner CRPG and expedition direction", "OWNER_CRPG_DIRECTION_VISIBLE_CAPTURE_2026-10-13.json"),
        ("Tinker Adept — actual trade progression", "FEAT_EXACT_01_TINKERING_PROGRESSION_NOTES.md"),
        ("Tinker Adept — recorded conditional history", "FEAT_EXACT_01_TINKERING_PROGRESSION_CHECK.json"),
        ("Remaining paid feat chains — scope", "FEAT_EXACT_01_REMAINING_OWNED_CHAINS_NOTES.md"),
        ("Remaining paid feat chains — source-qualified histories", "FEAT_EXACT_01_REMAINING_OWNED_CHAINS_CHECK.json"),
        ("External credentials — actual GPT reply", "FEAT327_ACQ_04_GPT_RESPONSE.json"),
        ("External credentials — controlling evidence policy", "FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json"),
        ("External credentials — preservation and source changes", "FEAT327_ACQ_04_DERIVED_OPERATIONS.json"),
        ("External credentials — independent source check", "FEAT327_ACQ_04_INDEPENDENT_DESCENDANT_CHECK.json"),
        ("External credentials — sixteen authored acceptance expectations", "feat327-acq04-source/ACQ04_ACCEPTANCE_CASES.json"),
        ("External credentials — finite fulfillment", "FEAT327_ACQ_04_FINITE_FULFILLMENT.json"),
        ("External credentials — recorded acceptance cases", "FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_CHECK.json"),
        ("External credentials — scope and limits", "FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_NOTES.md"),
        ("Animal Companion — acquisition histories", "FEAT_EXACT_01_COMPANION_ACQUISITION_CHECK.json"),
        ("Animal Companion — scope and remaining use work", "FEAT_EXACT_01_COMPANION_ACQUISITION_NOTES.md"),
        ("All335 feats — partial prerequisite evidence index", "FEAT_EXACT_01_PARTIAL_PREREQUISITE_COVERAGE_INDEX.json"),
        ("Prodigy — ordered choice evidence", "FEAT_EXACT_01_PRODIGY_CHOICES_CHECK.json"),
        ("Prodigy — scope and limits", "FEAT_EXACT_01_PRODIGY_CHOICES_NOTES.md"),
        ("Trade-training selections — evidence", "FEAT_EXACT_01_TRADE_SELECTIONS_CHECK.json"),
        ("Trade-training selections — scope", "FEAT_EXACT_01_TRADE_SELECTIONS_NOTES.md"),
        ("Eight half-feats — ability and training choices", "FEAT_EXACT_01_HALF_FEAT_CHOICES_CHECK.json"),
        ("Eight half-feats — scope", "FEAT_EXACT_01_HALF_FEAT_CHOICES_NOTES.md"),
        ("Martial, metamagic and elemental menus — evidence", "FEAT_EXACT_01_FIXED_MENUS_CHECK.json"),
        ("Martial, metamagic and elemental menus — scope", "FEAT_EXACT_01_FIXED_MENUS_NOTES.md"),
        ("Skill, tool and language choices — evidence", "FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_CHECK.json"),
        ("Skill, tool and language choices — scope", "FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_NOTES.md"),
        ("Casting selections — eleven-feat evidence", "FEAT_EXACT_01_CASTING_SELECTIONS_CHECK.json"),
        ("Casting selections — scope and spell placement limits", "FEAT_EXACT_01_CASTING_SELECTIONS_NOTES.md"),
        ("Weapon Focus/Mastery — profile evidence", "FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_CHECK.json"),
        ("Weapon profile choices — source and conditional limits", "FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_NOTES.md"),
        ("Complete feat acquisition audit — submitted request", "feat335-acquisition-audit-01-input/REQUEST.txt"),
        ("Complete feat acquisition audit — scope and evidence index", "feat335-acquisition-audit-01-input/START_HERE.json"),
        ("Complete feat acquisition audit — literal 335-row source index", "feat335-acquisition-audit-01-input/ALL335_SOURCE_INDEX.json"),
        ("Complete feat acquisition audit — exact submitted archive", "DD_FEAT335_Acquisition_Audit_01.zip"),
        ("Complete feat acquisition audit — actual submission receipt", "FEAT335_ACQUISITION_AUDIT_01_SUBMISSION.json"),
        ("Six maneuvers — paid acquisition and use evidence", "FEAT_EXACT_01_MANEUVERS_USE_CHECK.json"),
        ("Six maneuvers — encounter scope and remaining integration", "FEAT_EXACT_01_MANEUVERS_USE_NOTES.md"),
        ("Four heritage gadgets — construction and use evidence", "FEAT_EXACT_01_GADGET_USE_CHECK.json"),
        ("Four heritage gadgets — source and physical-scope limits", "FEAT_EXACT_01_GADGET_USE_NOTES.md"),
        ("Conjure Flora — mandatory provider and current-level capacity evidence", "FEAT_EXACT_01_FLORA_ACQUISITION_CHECK.json"),
        ("Conjure Flora — earlier model omission and correction scope", "FEAT_EXACT_01_FLORA_ACQUISITION_NOTES.md"),
        ("Companion lifecycle — actual GPT reply", "FEAT327_ACQ_05_GPT_RESPONSE.json"),
        ("Companion lifecycle — controlling addendum", "feat327-acq05-source/FEAT327_ACQ05_CONTROLLING_ADDENDUM.md"),
        ("Companion lifecycle — preserved exact source changes", "FEAT327_ACQ_05_DERIVED_OPERATIONS.json"),
        ("Companion lifecycle — independent preservation checks", "FEAT327_ACQ_05_INDEPENDENT_DESCENDANT_CHECK.json"),
        ("Companion lifecycle — twenty authored acceptance expectations", "feat327-acq05-source/ACQ05_ACCEPTANCE_EXPECTATIONS.json"),
        ("Companion lifecycle — finite fulfillment", "FEAT327_ACQ_05_FINITE_FULFILLMENT.json"),
        ("Companion lifecycle — executed conditional traces", "FEAT327_ACQ_05_LIFECYCLE_CHECK.json"),
        ("Companion lifecycle — scope and limits", "FEAT327_ACQ_05_LIFECYCLE_NOTES.md"),
        ("Local validator corrections — retained draft evidence", "FEAT_EXACT_01_CHOICES_AND_ACQ05_VALIDATOR_CORRECTIONS.json"),
        ("Animal Companion — actual ACQ05 submission", "FEAT327_ACQ_05_SUBMISSION.json"),
        ("Animal Companion — submitted lifecycle question", "FEAT327_ACQ_05_COMPANION_TIMING_QUESTION.txt"),
        ("Remaining credentials — source preparation", "FEAT_EXACT_01_REMAINING_CREDENTIAL_SOURCE_PLAN.json"),
        ("Lineage prerequisites — all current variants", "FEAT_EXACT_01_LINEAGE_PREREQUISITE_NOTES.md"),
        ("Lineage prerequisites — 585 variant/feat pairs", "FEAT_EXACT_01_LINEAGE_PREREQUISITE_CHECK.json"),
        ("Warrior tier limits — actual GPT ACQ-02 addendum", "feat327-acq02-source/FEAT327_ACQ_02_ADDENDUM.md"),
        ("Warrior tier limits — exact applied operations", "FEAT327_ACQ_02_DERIVED_OPERATIONS.json"),
        ("Warrior tier limits — independent fulfillment", "FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json"),
        ("GPT weapon-prerequisite addendum — exact ruling", "FEAT327_ACQ_01_GPT_ADDENDUM.md"),
        ("Weapon-prerequisite addendum — fulfilled derived correction", "FEAT327_ACQ_01_DERIVED_FULFILLMENT.json"),
        ("Weapon-prerequisite correction — independent whole-file checks", "FEAT327_ACQ_01_INDEPENDENT_CHECK.json"),
        ("Feat acceptance boundaries — scope and remaining work", "FEAT_EXACT_01_BOUNDARY_REFERENCE_NOTES.md"),
        ("Feat acceptance boundaries — reproducible reference checks", "FEAT_EXACT_01_BOUNDARY_REFERENCE_CHECK.json"),
        ("Feat candidate assembly — originals and full text", "FEAT_EXACT_CANDIDATE_01_BUILD.json"),
        ("Feat candidate — independent public and source checks", "FEAT_EXACT_CANDIDATE_01_STRUCTURE_CHECK.json"),
        ("Feat source verdict — local archive verification", "FEAT327_SOURCE_VERDICT_DOWNLOAD_CHECK.json"),
        ("Feat source verdict — independently rerun source checks", "FEAT327_SOURCE_VERDICT_LOCAL_REPRODUCTION.json"),
        ("Rank-six Transmutation and Universal proposals — preservation and source checks", "TRANSMUTATION_UNIVERSAL_RANK6_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-six Divination proposals — preservation and source checks", "DIVINATION_RANK6_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-six Abjuration/Conjuration proposals — preservation and source checks", "ABJURATION_CONJURATION_RANK6_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-six Illusion/Necromancy proposals — preservation and source checks", "ILLUSION_NECROMANCY_RANK6_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-six Enchantment proposals — preservation and source checks", "ENCHANTMENT_RANK6_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-six Evocation proposals — preservation and source checks", "EVOCATION_RANK6_OPERATING_PROPOSAL_CHECK.json"),
        ("Feat review access-limitation report — no verdict", "GPT_FEAT_V3_TERMINAL_ACCESS_LIMITATION.md"),
        ("Requested continuation of the existing full feat review", "CODEX_FEAT_V3_RECOVERY_CONTINUATION_REQUEST.txt"),
        ("Rank-five Divination and Universal proposals — preservation and source checks", "DIVINATION_UNIVERSAL_RANK5_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-five Evocation proposals — preservation and reference checks", "EVOCATION_RANK5_OPERATING_PROPOSAL_CHECK.json"),
        ("Completed exact expedition verdict", "ex58-exact-gpt-verdict/EX58_EXACT_VERDICT.md"),
        ("EX58-X01 fulfilled with preserved originals", "EX58_X01_FULFILLMENT.json"),
        ("Reversible reviewed-label proof", "EX58_REVIEW_LABEL_NORMALIZATION.json"),
        ("Current reviewed-scope coverage addendum", "EX58_COVERAGE_ADDENDUM.json"),
        ("Rank-four Illusion and Necromancy proposals — preservation and reference checks", "ILLUSION_NECROMANCY_RANK4_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-four Transmutation and Universal proposals — preservation and reference checks", "TRANSMUTATION_UNIVERSAL_RANK4_OPERATING_PROPOSAL_CHECK.json"),
        ("Rank-four Evocation proposals — preservation and reference checks", "EVOCATION_RANK4_OPERATING_PROPOSAL_CHECK.json"),
        ("Complete exact candidate submitted to GPT", "EX58_EXACT_CANDIDATE_SUBMISSION.json"),
        ("Whole candidate preservation and rendering checks", "EX58_EXACT_CANDIDATE_CHECK.json"),
        ("Exact review handoff and reading order", "EX58_EXACT_REVIEW_HANDOFF.md"),
        ("Cross-domain boundary record checks", "EX58_BOUNDARY_CANDIDATE_CHECK.json"),
        ("Social scenario record checks", "EX58_SOCIAL_SCENARIO_CANDIDATE_CHECK.json"),
        ("Completed 58-question GPT source verdict", "ex58-final-gpt-verdict/EX58_AUTHORING_VERDICT.md"),
        ("All transport profiles and procedures", "ex58-final-gpt-verdict/EX58_TRANSPORT_CATALOGUE.md"),
        ("Complete expedition worked sequences", "ex58-final-gpt-verdict/EX58_WORKED_SEQUENCES.md"),
        ("Verified final download and local reproduction", "EX58_FINAL_RECEIPT_LOCAL.json"),
        ("Final GPT response", "EX58_FINAL_TERMINAL_RESPONSE.json"),
        ("Exact candidate acceptance contract", "ex58-final-gpt-verdict/EX58_CONTRACTS_AND_EXACT_REVIEW.md"),
        ("First expedition chapter module checks", "EX58_CANDIDATE_PART01_CHECK.json"),
        ("Route, extraction and retreat module checks", "EX58_CANDIDATE_PART02_CHECK.json"),
        ("Haven, settlement and advancement module checks", "EX58_CANDIDATE_PART03_CHECK.json"),
        ("Social scenes and faction module checks", "EX58_CANDIDATE_PART04_CHECK.json"),
        ("Mounts, vehicles and transport module checks", "EX58_CANDIDATE_PART05_CHECK.json"),
        ("Reputation and background standing module checks", "EX58_CANDIDATE_PART06_CHECK.json"),
        ("Integrated expedition record and arithmetic checks", "EX58_INTEGRATED_FLOW_CANDIDATE_CHECK.json"),
        ("Complete transport catalogue preservation checks", "EX58_TRANSPORT_CATALOGUE_CANDIDATE_CHECK.json"),
        ("Five source offices correction fulfilled", "EX58_EDIT_01_FULFILLMENT.json"),
        ("Coin assay and fee allocation correction fulfilled", "EX58_EDIT_02_FULFILLMENT.json"),
        ("Earlier owner-requested continuation", "EXPEDITION_V3_OWNER_RECOVERY_CONTINUATION.json"),
        ("GPT correction: archive intact, unpublished drafts missing", "GPT_EXPEDITION_V3_MISSING_DRAFT_CORRECTION.md"),
        ("Earlier recovery response — not a delivered verdict", "GPT_EXPEDITION_V3_RECOVERY_ACCESS_LIMITATION.md"),
        ("Preserved access-failure response", "GPT_EXPEDITION_V3_ACCESS_FAILURE.md"),
        ("Original 58-question GPT submission", "EXPEDITION_INTEGRATED_V3_SUBMISSION.json"),
        ("Complete expedition review scope", "EXPEDITION_INTEGRATED_CONFERENCE_SCOPE.md"),
        ("Teaching review fulfilled", "TEACHING_TEX_EXACT_FULFILLMENT.json"),
        ("Internal wording addendum fulfilled", "TEACHING_TEX_ADDENDUM_FULFILLMENT.json"),
        ("Social and faction source questions", "SOCIAL_FACTION_SOURCE_AUDIT.md"),
        ("Historical social proposal — superseded by reviewed EX58 candidate", "SOCIAL_FACTION_OPERATING_PROPOSAL.md"),
        ("Reputation preservation findings", "REPUTATION_PRESERVATION_SOURCE_ADDENDUM.md"),
        ("Transport source questions", "TRANSPORT_SOURCE_AUDIT.md"),
        ("Joint flow and GitHub delivery", "FINAL_FLOW_AND_GITHUB_DELIVERY.md"),
    ]
    pending = [{**ref("docs/audit/2026-10-08/full-game/" + p), "label": label} for label, p in pending]
    data = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "ledgerSha256": digest(LEDGER),
        "areas": result,
        "featured": featured,
        "pending": pending,
        "ledger": ref(LEDGER.relative_to(G).as_posix()),
        "counts": {"aspects": len(result), "closed": sum(a["closure"] == "closed" for a in result), "spellsReviewed": ledger["activeOrdinarySpellReview"]["ordinaryOperational"], "spellsPending": ledger["activeOrdinarySpellReview"]["ordinaryPending"]},
    }
    assert not missing, "Unresolved ledger paths: " + repr(sorted(set(missing)))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = TEMPLATE.read_text(encoding="utf-8")
    assert template.count("__REVIEW_DATA__") == 1
    OUT.write_text(template.replace("__REVIEW_DATA__", payload), encoding="utf-8", newline="\n")
    for rel, expected_hash in current_inputs.items():
        assert digest(G / rel) == expected_hash, rel
    receipt = {"generatedAtUtc": data["generatedAtUtc"], "artifact": OUT.relative_to(G).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "ledgerSha256": data["ledgerSha256"], "areas": len(result), "existingDistinctLinks": len(links), "missingLinks": missing, "currentInputFilesUnchangedDuringBuild": len(current_inputs), "frozenArchivePayloadsVerified": len(frozen), "frozenExpeditionCurrentPayloadsVerified": len(expedition_frozen)-1, "currentDescendantsDifferentFromHistoricalSubmission": changed_since_submission, "purpose": "Offline owner navigation snapshot; no rule, approval, ledger, source, archive or save changes", "notebookReview": 'Planes review completed with corrected evidence: 11 bounded decisions, 76 retained source claims, 64 frozen source hashes and 18 actual travel-card bindings; 468 local checks passed. Two return archives preserved. The Director successor keeps original realms, mortal cosmography and saved website presentations distinct, preserves current effects and 12 pending higher travel spells, and adopts no new operating rules. COSMOLOGY-SOULS-RESEARCH-01 submitted once in owner-created Part 3 with 79 sources, 21 issues and 34 authored situations. GPT was responding at submission. It requests concrete proposed research, qualification, taint, Hunt and rare-intervention procedures; no numerical model or spell approval is adopted by submission. Current campaign epoch, chronology and epilogue adoption remain open. Ordinary spells419reviewed429pending. Latest verified GitHub18c6e3a; later work local.'}
    (A / "REVIEW_MAP_BUILD.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
