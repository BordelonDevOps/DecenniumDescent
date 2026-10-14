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
        assert digest(G / rel) == expected["sha256"], rel
    assert digest(LEDGER) == fulfillment["coverage"]["sha256"]
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
        assert digest(G / rel) == expected["sha256"], rel
        current_inputs[rel] = expected["sha256"]
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
    assert digest(LEDGER) == ex58_addendum["baseLedger"]["sha256"]
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
        "counts": {"aspects": len(result), "closed": sum(a["closure"] == "closed" for a in result), "spellsReviewed": ledger["activeLowRankSpellReview"]["ordinaryOperational"], "spellsPending": ledger["activeLowRankSpellReview"]["ordinaryPending"]},
    }
    assert not missing, "Unresolved ledger paths: " + repr(sorted(set(missing)))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = TEMPLATE.read_text(encoding="utf-8")
    assert template.count("__REVIEW_DATA__") == 1
    OUT.write_text(template.replace("__REVIEW_DATA__", payload), encoding="utf-8", newline="\n")
    for rel, expected_hash in current_inputs.items():
        assert digest(G / rel) == expected_hash, rel
    receipt = {"generatedAtUtc": data["generatedAtUtc"], "artifact": OUT.relative_to(G).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "ledgerSha256": data["ledgerSha256"], "areas": len(result), "existingDistinctLinks": len(links), "missingLinks": missing, "currentInputFilesUnchangedDuringBuild": len(current_inputs), "frozenArchivePayloadsVerified": len(frozen), "frozenExpeditionCurrentPayloadsVerified": len(expedition_frozen)-1, "currentDescendantsDifferentFromHistoricalSubmission": changed_since_submission, "purpose": "Offline owner navigation snapshot; no rule, approval, ledger, source, archive or save changes", "notebookReview": "EX58-EXACT-2026-10-11 delivered by e1b66405-efca-40d8-9986-31fe30323dff. All58 directions retained; EX58-X01 resource correction applied to8 candidate files with all419 submitted originals preserved. Corrected reference:1584 passing reviewer checks and435 strict checks; complete public projection, exact descendant bytes and reversible label-only proof verified. Current books carry reviewed authored scope;17 domain scope addenda recorded without closing broader domains. FLOW-C01/C02 accepted. All304 V3 originals unchanged. TEACHING TEX/addendum, LAX/NWX/LRX and687 internal/433 public recipes carried forward. Higher-spell index has180 unadopted procedures/360 examples,208 remaining mechanical questions and47 post-push receipts. TU6 adds13 Transmutation/Universal procedures and26 examples,21 current counterparts (11 reviewed/10 pending),10 earlier drafts and all17 class envelopes. Its675 source-preservation/rendering checks pass, including39 plain arithmetic checks;17 explicit issues await joint review. Reviewed Gaseous Form/Glyph descendants are correctly distinguished from stale catalog snapshots. Local checks do not establish runtime correctness, balance or joint approval. DI6 adds5 Divination procedures and10 examples,13 current counterparts,6 prior drafts and all17 class envelopes while preserving1 literal post-push receipt. Its577 source-preservation/rendering checks pass, including22 plain arithmetic checks;13 explicit issues await joint review. Class suppression and prediction require actual GPT agreement; no semantic approval or application runtime testing is claimed. AC6 adds11 Abjuration/Conjuration procedures and22 examples,16 whole current counterparts,8 prior drafts and8 class envelopes while preserving3 literal post-push receipts. Its636 source-preservation/rendering checks pass, including31 plain arithmetic checks;16 explicit issues await joint review. These are authored proposals, with no semantic approval or application runtime testing claimed. IN6 adds13 Illusion/Necromancy procedures and26 examples,15 full current counterparts,8 earlier drafts,7 class envelopes and4 explicitly new creature profiles. Its646 preservation/rendering/source checks pass, including29 arithmetic checks;17 explicit issues await joint review. The profiles remain unrated, sources remain intact, and no semantic approval or application runtime tests are claimed. EN6 adds7 Enchantment procedures and14 examples,15 full current counterparts,7 earlier drafts and7 class envelopes, preserving Soul Cage as a literal post-push receipt. Its581 preservation/rendering/source checks pass, including19 arithmetic checks;13 explicit issues await joint review. These checks are not semantic approval or application runtime tests. EV6 adds8 Evocation procedures and16 examples,15 full current counterparts,6 earlier drafts and7 class envelopes. Its587 preservation/rendering/source checks pass, including23 arithmetic checks;12 explicit issues await joint review. No independent semantic approval or application runtime testing is claimed. DU5 adds11 Divination/Universal procedures and22 examples,24 full current counterparts,7 earlier drafts and9 class envelopes, while preserving4 literal post-push receipts. Its634 preservation/rendering/source checks pass, including18 arithmetic checks;13 explicit issues await joint review. These are authored checks, with no independent semantic approval or application runtime testing. AC5 adds11 Abjuration/Conjuration procedures and22 examples,28 full current counterparts,4 earlier drafts,1 current-cohort counterpart and8 class envelopes, while preserving5literal post-push receipts. Its646 preservation/rendering/reference checks pass, including20 arithmetic and7 bounded accounting-model checks;14explicit issues remain for joint review. NT5 adds16 Necromancy/Transmutation procedures and32 examples,22 full current counterparts,5 earlier draft counterparts and8 class envelopes;684 preservation/rendering/reference checks pass, including27 arithmetic and6 bounded accounting-model checks. Seventeen new joint issues remain for actual GPT review. EI5 adds14 Enchantment/Illusion procedures and28 examples,21 full current counterparts,6 earlier drafts,1 current-cohort counterpart and6 class envelopes;652 preservation/rendering/reference checks pass, including24 arithmetic and4 accounting-model checks. No full spell runtime or human balance test is claimed. EV5 adds8 complete procedures and16 examples,17 whole current counterparts,7 earlier proposed counterparts and6 class envelopes;548 preservation/rendering/reference checks pass. These remain unadopted and await their dedicated spell review. All327 pending feat proposals (325 full drafts and2 deferred grant outlines,660 examples) are now submitted to GPT in request bf9d8dbb-22e3-4c31-a046-74608129acb9 with707 full payloads and15 explicit EX58/cross-cohort issues. Packaging passed5940 preservation/structural checks and707 archive payload checks. The original access-limitation report6cea42e9-4628-41a0-8619-6257ec16f577 is preserved. Continuation a64ef367-c9d6-400f-8ba6-4a76dd7f8080 subsequently completed with actual source verdict b50ec7da-7a7c-4975-82bb-b99d10a24134. Its969891-byte archive matches the declared SHA; all28 payloads and all3884 read-only source/manuscript/reference checks were independently verified locally. GPT supplies275 retained procedures,50 exact replacements,2 null deferred wrappers,67 field operations,26 corrected examples among660 positions,28 extra authored cases,16 shared rules and15 FEX resolutions. This completes source-authoring directions only. The complete exact feat text is now assembled in separate internal/public envelopes and nine reader plus nine source-audit chapters:325 full procedures,two null wrappers,all335 originals/eight reviewed unchanged,660 original cases and28 extra authored cases,16 shared rules,91 convention dispositions,15 FEX resolutions and all finite supplements. All1838 curriculum placements and7 ritual placements bind their exact reviewed payloads;282 reviewed spell references and2 literal deferred receipts are preserved. Assembly9061 and independent projection/source6826 checks pass. A first finite reference pass now represents all28 extra FA expectations with explicit executed subsets and unexecuted premise limits:362 checks pass, including204 bounded state/predicate checks,7 arithmetic,102 unchanged input bindings,28 full procedure equalities,18 source-data,2 source-adjudication and1 coverage check. These do not execute all660 original examples or close FXC-04–10. The remaining finite acceptance evidence, full package and actual exact review remain outstanding. No feat or comparison promotion occurs. The71 higher-spell proposals were included only as unadopted comparisons. Ordinary spells remain412 reviewed/436 pending. Whole-game review, remaining catalogs, runtime/human testing, push and cosmology remain open."}
    (A / "REVIEW_MAP_BUILD.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
