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

    featured = [
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
        ("Expedition player chapter — first seven directions drafted", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART01_PLAYER.md"),
        ("Expedition Director chapter — first seven directions drafted", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART01_DIRECTOR.md"),
        ("Routes, extraction and retreat — player chapter draft", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART02_PLAYER.md"),
        ("Routes, extraction and retreat — Director chapter draft", "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PART02_DIRECTOR.md"),
    ]
    featured = [{**ref(p), "label": label} for label, p in featured]
    pending = [
        ("Completed 58-question GPT source verdict", "ex58-final-gpt-verdict/EX58_AUTHORING_VERDICT.md"),
        ("All transport profiles and procedures", "ex58-final-gpt-verdict/EX58_TRANSPORT_CATALOGUE.md"),
        ("Complete expedition worked sequences", "ex58-final-gpt-verdict/EX58_WORKED_SEQUENCES.md"),
        ("Verified final download and local reproduction", "EX58_FINAL_RECEIPT_LOCAL.json"),
        ("Final GPT response", "EX58_FINAL_TERMINAL_RESPONSE.json"),
        ("Exact candidate acceptance contract", "ex58-final-gpt-verdict/EX58_CONTRACTS_AND_EXACT_REVIEW.md"),
        ("First expedition chapter module checks", "EX58_CANDIDATE_PART01_CHECK.json"),
        ("Route, extraction and retreat module checks", "EX58_CANDIDATE_PART02_CHECK.json"),
        ("Five source offices correction fulfilled", "EX58_EDIT_01_FULFILLMENT.json"),
        ("Earlier owner-requested continuation", "EXPEDITION_V3_OWNER_RECOVERY_CONTINUATION.json"),
        ("GPT correction: archive intact, unpublished drafts missing", "GPT_EXPEDITION_V3_MISSING_DRAFT_CORRECTION.md"),
        ("Earlier recovery response — not a delivered verdict", "GPT_EXPEDITION_V3_RECOVERY_ACCESS_LIMITATION.md"),
        ("Preserved access-failure response", "GPT_EXPEDITION_V3_ACCESS_FAILURE.md"),
        ("Original 58-question GPT submission", "EXPEDITION_INTEGRATED_V3_SUBMISSION.json"),
        ("Complete expedition review scope", "EXPEDITION_INTEGRATED_CONFERENCE_SCOPE.md"),
        ("Teaching review fulfilled", "TEACHING_TEX_EXACT_FULFILLMENT.json"),
        ("Internal wording addendum fulfilled", "TEACHING_TEX_ADDENDUM_FULFILLMENT.json"),
        ("Social and faction source questions", "SOCIAL_FACTION_SOURCE_AUDIT.md"),
        ("Social proposal awaiting discussion", "SOCIAL_FACTION_OPERATING_PROPOSAL.md"),
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
    receipt = {"generatedAtUtc": data["generatedAtUtc"], "artifact": OUT.relative_to(G).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "ledgerSha256": data["ledgerSha256"], "areas": len(result), "existingDistinctLinks": len(links), "missingLinks": missing, "currentInputFilesUnchangedDuringBuild": len(current_inputs), "frozenArchivePayloadsVerified": len(frozen), "frozenExpeditionCurrentPayloadsVerified": len(expedition_frozen)-1, "currentDescendantsDifferentFromHistoricalSubmission": changed_since_submission, "purpose": "Offline owner navigation snapshot; no rule, approval, ledger, source, archive or save changes", "notebookReview": "TEX and addendum fulfilled; final EX58 source verdict delivered by assistant f9effea2-510e-4529-a141-a3c1932008f3; 17 payloads hash-verified and 2316 source/reference checks reproduced locally with0 failures; all304 original payloads intact; earlier unpublished drafts reconstructed, not recovered; first18 source directions authored in player/Director modules with34 cases; part1 has374 and part2 has428 preservation/parity/arithmetic checks passing;40 directions remain for complete exact candidate assembly; EX58-EDIT-01 office correction fulfilled with40 checks and exact descendant hashes; one complete feat index separates8 reviewed full feats from327 pending, including325 complete unadopted procedures and2 deferred grant outlines with660 authored cases;0 source-question-only entries;1 NEW Spell Focus supplement outside the335-source registry; higher-spell index distinguishes30 unadopted proposed procedures with60 authored examples,358 remaining mechanical questions and47 literal post-push receipts; ordinary catalog unchanged at412 reviewed/436 pending; whole-game work open"}
    (A / "REVIEW_MAP_BUILD.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
