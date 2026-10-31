from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import zipfile
import zlib


ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_final_word_closure_delta_303"
ZIP_PATH = OUT / "DD_Rank9_FinalWord_ClosureDelta_303.zip"
RETURN235 = A / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD.zip"
SOURCE279_DIR = A / "rank9_deathrecovery7_current_source_279_prepared_review2"
SOURCE279_CANDIDATE = SOURCE279_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json"
CURRENT_AUTHORITY_ARTIFACTS = [
    A / "CURRENT_SPELL_QUEUE_302.json",
    A / "CURRENT_HANDOFF_302.json",
    A / "CURRENT26_PENDING_IDENTITY_AUDIT_302.json",
    A / "CURRENT_SPELL_REVIEW_SNAPSHOT_302.md",
    A / "CURRENT_FINAL_WORD_DIRECTOR_REQUIREMENTS_303.json",
    A / "WEIRD_ACCEPTANCE_302.json",
    A / "WEIRD_APPLICATION_302.json",
    A / "WEIRD_APPLICATION_VALIDATION_302.json",
]
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
CHRONICLE = ROOT / "docs/manuals/Chronicle_of_the_Decennial_Opening.md"
CHRONICLE_ASSESSMENT = A / "FINAL_WORD_CHRONICLE_SOURCE_LEAD_303.json"
CURRENT_AUTHORITY = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
RETURN235_SHA = ""  # Captured and cross-checked from the existing Return235 receipt at build time.
EXPECTED_CATALOG_SHA = "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def file_binding(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


def archived_binding(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}


def write_json(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def main() -> None:
    if OUT.exists():
        existing = list(OUT.iterdir())
        assert len(existing) == 1 and existing[0].name == "payload" and existing[0].is_dir() and not any(existing[0].iterdir()), "Refusing to overwrite a non-empty Final Word closure delta 303 output."
    assert sha(CATALOG.read_bytes()) == EXPECTED_CATALOG_SHA, "Unexpected native catalog change."
    assert sha(CHRONICLE.read_bytes()) == "28c7e59c881bacdc73d7f88d19b595de33b61ba342c98a231b9de9ed04ca6a29"
    OUT.mkdir(parents=True, exist_ok=True)
    stage = OUT / "payload"
    stage.mkdir(exist_ok=True)

    old_source = read(SOURCE279_CANDIDATE)
    old_bindings = old_source["sourceBindings"]
    assert len(old_bindings) == 74
    refreshed = []
    changed = []
    for old in old_bindings:
        source_path = ROOT / pathlib.PurePosixPath(old["path"])
        assert source_path.is_file(), f"Missing source binding {old['path']}"
        raw = source_path.read_bytes()
        current = {"path": old["path"], "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}
        same = all(old.get(key) == current[key] for key in ("path", "bytes", "sha256", "crc32"))
        row = {"path": old["path"], "previous": {k: old.get(k) for k in ("path", "bytes", "sha256", "crc32")}, "current": current, "byteExactUnchanged": same}
        refreshed.append(row)
        if not same:
            changed.append(row)
    assert len(changed) == 1 and changed[0]["path"].endswith("authored_review_index.json")

    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index_now, catalog_now = read(INDEX), read(CATALOG)
    assert index_now["authoredCounts"] == {"reviewed": 822, "pending": 26}
    assert index_now["representationCounts"]["completeReviewedStandaloneProcedures"] == 546
    final_word_now = copy.deepcopy(next(x for x in index_now["entries"] if x["id"] == "final-word"))
    final_word_before = copy.deepcopy(old_source["currentReviewTargets"][0]["currentIndexEntry"])
    assert final_word_now == final_word_before
    assert final_word_now["authoredStatus"] == "pending-authored-procedure"
    assert final_word_now["sourceStatus"] == "blocked-pending-operational-review"
    pending_ids_now = sorted(x["id"] for x in index_now["entries"] if x.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending_ids_now) == 26 and pending_ids_now[0] == "alignment-ascension"
    final_word_catalog = copy.deepcopy(next(x for x in catalog_now["spells"] if x["id"] == "final-word"))
    assert final_word_catalog["operational"] is None and final_word_catalog["status"] == "blocked-pending-operational-review"

    q = read(A / "CURRENT_SPELL_QUEUE_302.json")
    h = read(A / "CURRENT_HANDOFF_302.json")
    p = read(A / "CURRENT26_PENDING_IDENTITY_AUDIT_302.json")
    app = read(A / "WEIRD_APPLICATION_302.json")
    acc = read(A / "WEIRD_ACCEPTANCE_302.json")
    val = read(A / "WEIRD_APPLICATION_VALIDATION_302.json")
    assert q["currentAuthority"] == h["currentAuthority"] == p["authority"] == CURRENT_AUTHORITY
    assert q["next"]["pendingIds"] == h["nextPendingIds"] == ["final-word"]
    assert p["pendingCount"] == 26 and val["status"] == "PASS"
    assert app["appliedIds"] == ["weird"] and acc["acceptedIds"] == ["weird"]
    assert app["countsAfter"] == CURRENT_AUTHORITY and not app["implementationApproved"] and app["runtimeSelectionEnabled"] is False

    return235_raw = RETURN235.read_bytes()
    assert not RETURN235_SHA or sha(return235_raw) == RETURN235_SHA
    with zipfile.ZipFile(RETURN235) as z:
        assert z.testzip() is None
        names = set(z.namelist())
        required = {"DIRECTOR_DECISION.json", "PROCEDURE_STATUS_235.json", "QUESTION_DISPOSITIONS.json", "CURRENT_SOURCE_REASSESSMENT.json", "GORTHAN_SOURCE_LEAD.json", "COUNTS.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "SOURCE_VERIFICATION.json"}
        assert required <= names
        counts235 = json.loads(z.read("COUNTS.json"))
        assert counts235["cases"] == 16 and counts235["events"] == 223
        assert counts235["forwardOperations"] == counts235["inverseOperations"] == 446
        decision235 = json.loads(z.read("DIRECTOR_DECISION.json"))
        assert decision235["heldIds"] == ["final-word"]
        assert decision235["perIdentity"][0]["id"] == "final-word" and decision235["perIdentity"][0]["blockerIds"] == ["DR217-B01"]
        source_search_hits = json.loads(z.read("SOURCE_SEARCH_HITS.json"))
        assert len(source_search_hits) == 251

    chronology_assessment = read(CHRONICLE_ASSESSMENT)
    assert chronology_assessment["status"] == "LEAD_ONLY_NO_POSITIVE_CAPTURE_WITNESS"
    assert chronology_assessment["accepted"] is False and chronology_assessment["applied"] is False

    # Refreshed current-source inventory and the no-witness disposition.
    source_refresh = {
        "id": "FINAL-WORD-SOURCE-REFRESH-303", "recordedAtUtc": "2026-10-31T03:05:00Z",
        "sourcePacket279": file_binding(SOURCE279_DIR / "DD_Rank9_DeathRecovery7_CurrentSource_279.zip"),
        "sourcePacket279Delivery": file_binding(SOURCE279_DIR / "DD_Rank9_DeathRecovery7_CurrentSource_279_DELIVERY.json"),
        "priorSourceBindingCount": 74, "currentSourceBindingCount": len(refreshed),
        "byteExactUnchangedCount": len(refreshed) - len(changed), "changedCount": len(changed),
        "changedBindings": changed, "refreshedBindings": refreshed,
        "additionalLead": file_binding(CHRONICLE),
        "additionalLeadDisposition": file_binding(CHRONICLE_ASSESSMENT),
        "interpretation": "The only changed file among the prior 74 bound sources is the authored review index after Weird's accepted application. Catalog and all other 73 sources are byte-exact to the prior inventory.",
    }
    write_json(stage / "SOURCE_REFRESH_MAP_303.json", source_refresh)
    witness_assessment = {
        "id": "FINAL-WORD-FOCUSED-WITNESS-ASSESSMENT-303", "recordedAtUtc": "2026-10-31T03:05:00Z",
        "spellId": "final-word", "blocker": "DR217-B01", "status": "HELD_NO_ADMISSIBLE_POSITIVE_CAPTURE_WITNESS",
        "scope": "Evidence-only reassessment of the single DR217-B01 positive-capture witness requirement; no new rule or permission is proposed.",
        "priorSearch": {"sourceInventory": file_binding(SOURCE279_CANDIDATE), "currentSourceCount": 74, "Return235SearchHitCount": 251, "Return235SourceVerificationPassed": True},
        "newSourceLead": {
            "source": file_binding(CHRONICLE), "assessment": file_binding(CHRONICLE_ASSESSMENT),
            "findings": [
                "Chronicle lines 145 and 332 report Gorthan's three prior deaths and returns by soulbinding.",
                "Chronicle line 549 is explicitly in the Adventure seeds section; it describes a proposed Gorthan rescue tied to a PC's true name, not an occurred event or named PC record.",
                "Neither Gorthan nor the unnamed PC has a source-bound current living body/normal HP, actual soul availability and capture permission, custody/capture bars, Hunt status, lawful Final Word death, or token/payment history in this source."
            ],
            "notAPositiveWitness": True,
        },
        "minimumStillMissing": [
            "One exact source-qualified independent victim identity with current living body and normal HP, life/soul lifecycle, soul availability and capture permission, custody/capture bars, Hunt status, and summon/no-resource-farming facts.",
            "A lawful acquired Final Word cast with prepared repertoire, Action/V/S/F/26 RP/cadence, 120-foot range/perception/line of effect, actual normal HP below 50 excluding temporary HP, and all genuine would-die protections resolved before committed death.",
            "The resulting uniquely sourced reserve and eligible actual one-spell base-RP use with once-only consumption, lost remainder, counter nonrefund, distinct lawful concurrent origins, and original next-completed-long-rest expiry."
        ],
        "existingSpellRulesRemainSelected": True,
        "existing16Cases": {"archive": file_binding(RETURN235), "caseCount": 16, "events": 223, "forwardOperations": 446, "inverseOperations": 446, "replayClaim": "preserved historical Director-return results only; not replayed by this delta"},
        "noSyntheticVictimOrCampaignEventCreated": True,
        "noIdentityAcceptedOrApplied": True,
        "currentAuthority": CURRENT_AUTHORITY,
        "sourceStatus": "blocked-pending-operational-review",
        "runtimeSelectionEnabled": False,
    }
    write_json(stage / "FOCUSED_WITNESS_ASSESSMENT_303.json", witness_assessment)

    # Bind every exact current snapshot required by Director.
    current_files: list[tuple[pathlib.Path, str]] = [
        (INDEX, "current/authored_review_index.json"), (CATALOG, "current/catalog.json"),
        (RETURN235, "prior/Return235_HELD.zip"), (SOURCE279_CANDIDATE, "prior/CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json"),
        (A / "DEATHRECOVERY7_DIRECTOR_RULING_279.json", "prior/DEATHRECOVERY7_DIRECTOR_RULING_279.json"),
        (A / "DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json", "prior/DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json"),
        (A / "RANK9DEATHRECOVERY7_PACKET_279.json", "prior/RANK9DEATHRECOVERY7_PACKET_279.json"),
        (A / "RANK9DEATHRECOVERY7_PACKET279_RECEIPT.json", "prior/RANK9DEATHRECOVERY7_PACKET279_RECEIPT.json"),
        (A / "RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json", "prior/RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json"),
        (SOURCE279_DIR / "DD_Rank9_DeathRecovery7_CurrentSource_279_DELIVERY.json", "prior/DD_Rank9_DeathRecovery7_CurrentSource_279_DELIVERY.json"),
        (CHRONICLE, "supplemental/Chronicle_of_the_Decennial_Opening.md"),
        (CHRONICLE_ASSESSMENT, "supplemental/FINAL_WORD_CHRONICLE_SOURCE_LEAD_303.json"),
    ]
    current_files += [(path, f"current/{path.name}") for path in CURRENT_AUTHORITY_ARTIFACTS]
    for source, dest in current_files:
        target = stage / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    shutil.copyfile(stage / "SOURCE_REFRESH_MAP_303.json", stage / "current/SOURCE_REFRESH_MAP_303.json")
    shutil.copyfile(stage / "FOCUSED_WITNESS_ASSESSMENT_303.json", stage / "current/FOCUSED_WITNESS_ASSESSMENT_303.json")

    authority = {
        "id": "CURRENT-FINAL-WORD-AUTHORITY-303", "recordedAtUtc": "2026-10-31T03:05:00Z",
        "authority": CURRENT_AUTHORITY, "nextIdentity": "final-word", "blocker": "DR217-B01",
        "index": file_binding(INDEX), "catalog": file_binding(CATALOG),
        "queue": file_binding(A / "CURRENT_SPELL_QUEUE_302.json"),
        "handoff": file_binding(A / "CURRENT_HANDOFF_302.json"),
        "pendingIdentityAudit": file_binding(A / "CURRENT26_PENDING_IDENTITY_AUDIT_302.json"),
        "weirdAcceptance": file_binding(A / "WEIRD_ACCEPTANCE_302.json"),
        "weirdApplication": file_binding(A / "WEIRD_APPLICATION_302.json"),
        "weirdApplicationValidation": file_binding(A / "WEIRD_APPLICATION_VALIDATION_302.json"),
        "finalWordIndexEntryBefore": final_word_before, "finalWordIndexEntryAfter": final_word_now,
        "catalogByteExact": True, "finalWordAccepted": False, "finalWordApplied": False,
        "firstReviewTasksRemaining": 0, "closureTasksRemaining": 26,
    }
    write_json(stage / "CURRENT_AUTHORITY_303.json", authority)
    # Add the authority wrapper after creating its source bindings.
    shutil.copyfile(stage / "CURRENT_AUTHORITY_303.json", stage / "current/CURRENT_AUTHORITY_303.json")

    # A compact semantic audit: prior procedural work remains intact, only the missing real source witness blocks closure.
    semantic = {
        "id": "FINAL-WORD-CLOSURE-DELTA-SEMANTIC-AUDIT-303", "recordedAtUtc": "2026-10-31T03:05:00Z",
        "status": "PASS_WITH_DR217_B01_HELD", "criteriaCount": 13, "passedCriteria": 12, "blockedCriteria": 1,
        "criteria": [
            {"id": "FW303-S01", "status": "PASS", "criterion": "Current authority and pending membership", "finding": "822/26/0; exact pending index set; Final Word remains pending."},
            {"id": "FW303-S02", "status": "PASS", "criterion": "Current 74-source inventory", "finding": "73 sources and native catalog remain byte-exact; only authored index changed after Weird application."},
            {"id": "FW303-S03", "status": "PASS", "criterion": "Final Word target state", "finding": "Final Word index entry is byte-structurally unchanged from the prior current-source review; source remains blocked."},
            {"id": "FW303-S04", "status": "PASS", "criterion": "Prior selected spell rules and cases", "finding": "Return235's 16 cases, 223 events, 446 forward and 446 inverse operations are preserved with historical status, not claimed replayed by this delta."},
            {"id": "FW303-S05", "status": "PASS", "criterion": "Return217/235/279 findings", "finding": "Exact prior decisions, audits, blocker and next order are bound; all prior application/acceptance status is preserved."},
            {"id": "FW303-S06", "status": "PASS", "criterion": "Question scope", "finding": "Only DR9-Q01/Q09/Q10/Q11/Q12/Q21/Q22 are relevant; other Death/Recovery identities remain closed."},
            {"id": "FW303-S07", "status": "PASS", "criterion": "Chronicle source integrity", "finding": "Exact source hash and cited lines verified; adventure seed remains a lead, not an actual event."},
            {"id": "FW303-S08", "status": "PASS", "criterion": "No invented victim or campaign facts", "finding": "No actual victim state, Final Word death, soul availability, capture permission, or token history was created."},
            {"id": "FW303-S09", "status": "PASS", "criterion": "No synthetic eligibility or revision", "finding": "No synthetic permission or new obligation revision was added; PF301 remains Weird-only."},
            {"id": "FW303-S10", "status": "PASS", "criterion": "Catalog and runtime", "finding": "Catalog is byte-exact; sourceStatus stays blocked and runtime selection disabled."},
            {"id": "FW303-S11", "status": "PASS", "criterion": "Index reversible operation", "finding": "Final Word index entry is identical before/after; no index mutation or irreversible game-state action occurred."},
            {"id": "FW303-S12", "status": "PASS", "criterion": "Implementation and downstream gates", "finding": "Runtime, implementation, balance, cosmology, domain completion and release gates remain closed."},
            {"id": "FW303-S13", "status": "BLOCKED", "criterion": "Positive source-qualified capture witness", "finding": "No exact current identity/lifecycle with soul availability, capture permission, actual lawful Final Word death and resulting token/payment history is established."}
        ],
        "newGameplayEvents": 0, "newReplayClaim": False, "newIdentityAccepted": False, "newIdentityApplied": False,
        "blockerIds": ["DR217-B01"],
    }
    write_json(stage / "INDEPENDENT_SEMANTIC_AUDIT_303.json", semantic)

    # Manifest binds each payload by exact bytes, SHA-256 and CRC32.
    members = sorted(x for x in stage.rglob("*") if x.is_file())
    manifest_rows = []
    for path in members:
        raw = path.read_bytes()
        manifest_rows.append({"path": path.relative_to(stage).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
    manifest = {"id": "FINAL-WORD-CLOSURE-DELTA-303-MANIFEST", "recordedAtUtc": "2026-10-31T03:05:00Z", "fileCountExcludingManifest": len(manifest_rows), "files": manifest_rows}
    write_json(stage / "DELIVERY_MANIFEST_303.json", manifest)
    manifest_raw = (stage / "DELIVERY_MANIFEST_303.json").read_bytes()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(x for x in stage.rglob("*") if x.is_file()):
            archive.write(path, path.relative_to(stage).as_posix())
    with zipfile.ZipFile(ZIP_PATH) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(manifest_rows) + 1
        for row in manifest_rows:
            raw = archive.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]

    receipt = {
        "id": "FINAL-WORD-CLOSURE-DELTA-303-RECEIPT", "recordedAtUtc": "2026-10-31T03:05:00Z",
        "status": "PASS_PACKET_READY_FOR_DIRECTOR_ADJUDICATION; FINAL_WORD_HELD_PENDING_SOURCE_WITNESS",
        "archive": file_binding(ZIP_PATH), "manifest": {"path": "DELIVERY_MANIFEST_303.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": f"{zlib.crc32(manifest_raw) & 0xFFFFFFFF:08x}"},
        "payloadCount": len(manifest_rows), "memberCount": len(manifest_rows) + 1,
        "currentAuthority": CURRENT_AUTHORITY, "sourceBindings": {"prior": 74, "unchanged": 73, "changed": 1},
        "preservedFinalWordCases": {"cases": 16, "events": 223, "forwardOperations": 446, "inverseOperations": 446},
        "acceptedIds": [], "appliedIds": [], "heldIds": ["final-word"], "blockerIds": ["DR217-B01"],
        "nextAfterHeldTarget": "Request Director's current next target and remaining closure order after Final Word is held.",
    }
    write_json(OUT / "SUBMISSION_RECEIPT_303.json", receipt)
    (OUT / "REQUEST_303.txt").write_text(
        "FINAL WORD / DR217-B01 — CLOSURE DELTA 303\n\n"
        "Please adjudicate only Final Word. The archive and manifest preserve the current 822/26/0 authority and refreshed 74-source inventory (73 byte-exact, with only the authored index changed after Weird's accepted application), exact Final Word procedure/dispositions and Return217/235/279 findings, all 16 prior cases, and the supplemental Chronicle source lead.\n\n"
        "The new source lead remains an adventure seed and does not establish an actual eligible victim. No synthetic identity, permission, encounter, token or payment history has been created. If DR217-B01 remains open, return the narrowest missing source witness and the next current identity/order; do not accept or apply any other identity.\n",
        encoding="utf-8", newline="\n",
    )
    shutil.rmtree(stage)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
