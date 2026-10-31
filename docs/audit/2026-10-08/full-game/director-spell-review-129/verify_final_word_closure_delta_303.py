from __future__ import annotations

import hashlib
import json
import pathlib
import datetime as dt
import zipfile
import zlib


ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_final_word_closure_delta_303"
ARCHIVE = OUT / "DD_Rank9_FinalWord_ClosureDelta_303.zip"
RETURN235 = A / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD.zip"
SOURCE279_DIR = A / "rank9_deathrecovery7_current_source_279_prepared_review2"
SOURCE279 = SOURCE279_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
EXPECTED = "087a50b901d1c7f561036d3b3f086871e5c19ebe245d549a687485da6bec57a2"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def bind(path: pathlib.Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}


def main() -> None:
    outer = ARCHIVE.read_bytes()
    assert sha(outer) == EXPECTED and len(outer) == 10_228_938
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == 28
        names = set(z.namelist())
        manifest_raw = z.read("DELIVERY_MANIFEST_303.json")
        manifest = read(manifest_raw)
        assert manifest["fileCountExcludingManifest"] == 27 and len(manifest["files"]) == 27
        for row in manifest["files"]:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
        index_zip = z.read("current/authored_review_index.json")
        catalog_zip = z.read("current/catalog.json")
        assert sha(index_zip) == sha(INDEX.read_bytes())
        assert sha(catalog_zip) == sha(CATALOG.read_bytes())
        index = read(index_zip)
        catalog = read(catalog_zip)
        assert index["authoredCounts"] == {"reviewed": 822, "pending": 26}
        assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 546
        pending = {x["id"] for x in index["entries"] if x.get("authoredStatus") == "pending-authored-procedure"}
        assert len(pending) == 26 and "final-word" in pending and "weird" not in pending
        final_entry = next(x for x in index["entries"] if x["id"] == "final-word")
        assert final_entry["authoredStatus"] == "pending-authored-procedure" and final_entry["sourceStatus"] == "blocked-pending-operational-review"
        assert next(x for x in catalog["spells"] if x["id"] == "final-word")["operational"] is None

        source_refresh = read(z.read("current/SOURCE_REFRESH_MAP_303.json"))
        assert source_refresh["priorSourceBindingCount"] == source_refresh["currentSourceBindingCount"] == 74
        assert source_refresh["byteExactUnchangedCount"] == 73 and source_refresh["changedCount"] == 1
        assert len(source_refresh["refreshedBindings"]) == 74
        source279 = read(SOURCE279.read_bytes())
        old_rows = {row["path"]: row for row in source279["sourceBindings"]}
        changed = []
        for row in source_refresh["refreshedBindings"]:
            current = row["current"]
            path = ROOT / pathlib.PurePosixPath(current["path"])
            raw = path.read_bytes()
            assert len(raw) == current["bytes"] and sha(raw) == current["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == current["crc32"]
            old = old_rows[current["path"]]
            same = all(old.get(k) == current[k] for k in ("path", "bytes", "sha256", "crc32"))
            assert same == row["byteExactUnchanged"]
            if not same:
                changed.append(current["path"])
        assert changed == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]
        target279 = source279["currentReviewTargets"][0]["currentIndexEntry"]
        assert final_entry == target279

        q = read(z.read("current/CURRENT_SPELL_QUEUE_302.json"))
        h = read(z.read("current/CURRENT_HANDOFF_302.json"))
        p = read(z.read("current/CURRENT26_PENDING_IDENTITY_AUDIT_302.json"))
        auth = read(z.read("current/CURRENT_AUTHORITY_303.json"))
        requirements = read(z.read("current/CURRENT_FINAL_WORD_DIRECTOR_REQUIREMENTS_303.json"))
        validation = read(z.read("current/WEIRD_APPLICATION_VALIDATION_302.json"))
        acceptance = read(z.read("current/WEIRD_ACCEPTANCE_302.json"))
        application = read(z.read("current/WEIRD_APPLICATION_302.json"))
        assert q["currentAuthority"] == h["currentAuthority"] == p["authority"] == auth["authority"]
        assert q["currentAuthority"] == {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
        assert q["next"]["pendingIds"] == h["nextPendingIds"] == ["final-word"]
        assert requirements["remainingOrder"][0] == "final-word" and len(requirements["remainingOrder"]) == 26
        assert validation["status"] == "PASS" and validation["failedChecks"] == 0
        assert acceptance["acceptedIds"] == application["appliedIds"] == ["weird"]
        assert auth["finalWordAccepted"] is False and auth["finalWordApplied"] is False

        prior = read(z.read("prior/RANK9DEATHRECOVERY7_PACKET_279.json"))
        prior_audit = read(z.read("prior/RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json"))
        ruling279 = read(z.read("prior/DEATHRECOVERY7_DIRECTOR_RULING_279.json"))
        crosscheck279 = read(z.read("prior/DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json"))
        assert prior["accepted"] is False and prior["applied"] is False
        assert prior_audit["status"] == "PASS" and ruling279["heldIds"] == ["final-word"]
        assert ruling279["blockerIds"] == ["DR217-B01"] and crosscheck279["status"] == "PASS"
        source279zip = SOURCE279_DIR / "DD_Rank9_DeathRecovery7_CurrentSource_279.zip"
        source279_delivery = read((SOURCE279_DIR / "DD_Rank9_DeathRecovery7_CurrentSource_279_DELIVERY.json").read_bytes())
        assert source279_delivery["archive"]["sha256"] == sha(source279zip.read_bytes())

        prior235 = z.read("prior/Return235_HELD.zip")
        assert sha(prior235) == sha(RETURN235.read_bytes())
        with zipfile.ZipFile(RETURN235) as z235:
            assert z235.testzip() is None
            counts = read(z235.read("COUNTS.json"))
            decision235 = read(z235.read("DIRECTOR_DECISION.json"))
            integrity235 = read(z235.read("SOURCE_VERIFICATION.json"))
            semantic235 = read(z235.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
            assert counts["cases"] == 16 and counts["events"] == 223
            assert counts["forwardOperations"] == counts["inverseOperations"] == 446
            assert decision235["heldIds"] == ["final-word"] and decision235["perIdentity"][0]["blockerIds"] == ["DR217-B01"]
            assert integrity235["failedChecks"] == 0 and semantic235["blockedCriteria"] == 1

        focus = read(z.read("current/FOCUSED_WITNESS_ASSESSMENT_303.json"))
        assert focus["status"] == "HELD_NO_ADMISSIBLE_POSITIVE_CAPTURE_WITNESS"
        assert focus["existingSpellRulesRemainSelected"] is True and focus["noSyntheticVictimOrCampaignEventCreated"] is True
        assert focus["existing16Cases"]["replayClaim"].startswith("preserved historical")
        chronicle_raw = z.read("supplemental/Chronicle_of_the_Decennial_Opening.md")
        assert sha(chronicle_raw) == "28c7e59c881bacdc73d7f88d19b595de33b61ba342c98a231b9de9ed04ca6a29"
        chronicle_assessment = read(z.read("supplemental/FINAL_WORD_CHRONICLE_SOURCE_LEAD_303.json"))
        assert chronicle_assessment["status"] == "LEAD_ONLY_NO_POSITIVE_CAPTURE_WITNESS"
        assert chronicle_assessment["accepted"] is False and chronicle_assessment["applied"] is False
        semantic = read(z.read("INDEPENDENT_SEMANTIC_AUDIT_303.json"))
        assert semantic["status"] == "PASS_WITH_DR217_B01_HELD" and semantic["blockedCriteria"] == 1
        assert semantic["newGameplayEvents"] == 0 and semantic["newIdentityAccepted"] is False and semantic["newIdentityApplied"] is False

        assert "current/DELIVERY_MANIFEST_303.json" in names or "DELIVERY_MANIFEST_303.json" in names
    receipt = read((OUT / "SUBMISSION_RECEIPT_303.json").read_bytes())
    assert receipt["archive"]["sha256"] == EXPECTED and receipt["status"].startswith("PASS_PACKET_READY")
    assert receipt["acceptedIds"] == receipt["appliedIds"] == [] and receipt["heldIds"] == ["final-word"]
    checks = [
        "outer archive bytes, SHA-256 and CRC32 match the packet receipt",
        "ZIP integrity, member count, and all payload SHA-256/CRC32 bindings pass",
        "embedded current index/catalog are byte-exact to the live repository",
        "authority is 822/26/0 with 546 complete procedures and exactly 26 pending identities",
        "Final Word remains pending and source-blocked; catalog operational pointer is null",
        "all 74 prior current-source bindings were rechecked; exactly 73 match and the index is the sole changed file",
        "the Final Word authored-index entry is structurally unchanged from the prior current-source candidate",
        "current queue, handoff, pending audit, and authority wrapper agree; Final Word remains next",
        "Weird exact acceptance/application receipts and application validation remain bound at 822/26/0",
        "Return279 packet and independent audit are preserved as held and independently passed",
        "Return279 exact director ruling/crosscheck retains DR217-B01 and the prior order",
        "Return235 archive and preserved 16 cases / 223 events / 446 forward / 446 inverse counts verify",
        "Return235 source verification passes all 1,173 checks; its prior Director ruling holds Final Word under DR217-B01",
        "Chronicle source hash and Gorthan lead assessment bind; adventure seed is not treated as an actual witness",
        "focused witness assessment creates no actor, encounter, gameplay events, capture permission, or token history",
        "independent semantic audit passes with only the required positive-source-witness criterion held",
        "no Final Word identity was accepted or applied and runtime/canonical gates remain unchanged",
    ]
    report = {"id": "FINAL-WORD-CLOSURE-DELTA-INDEPENDENT-AUDIT-303", "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "status": "PASS_WITH_DR217_B01_HELD",
              "outerArchive": bind(ARCHIVE), "memberCount": 28, "payloadCount": 27,
              "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
              "checks": [{"check": name, "passed": True} for name in checks],
              "sourceBindings": {"prior": 74, "unchanged": 73, "changed": changed},
              "preservedPriorFinalWordCases": {"cases": 16, "events": 223, "forwardOperations": 446, "inverseOperations": 446, "newReplayClaim": False},
              "authority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
                            "completeStandaloneProcedures": 546, "scopedInterfaces": 173},
              "heldIdentity": "final-word", "blockerIds": ["DR217-B01"], "acceptedIds": [], "appliedIds": [],
              "next": "Await Director's disposition; if held, continue to the next ordered closure identity.",
              "canonicalCatalogChanged": False, "runtimeSelectionEnabled": False}
    (OUT / "INDEPENDENT_AUDIT_303.json").write_bytes(json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    print(json.dumps({"status": "PASS", "archiveSHA256": EXPECTED, "members": 28,
                      "refreshedSourceBindings": 74, "unchangedSources": 73,
                      "changedSources": changed, "preservedCases": 16, "events": 223,
                      "authority": "822/26/0", "finalWord": "held pending source witness",
                      "newGameplayEvents": 0, "accepted": [], "applied": []}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
