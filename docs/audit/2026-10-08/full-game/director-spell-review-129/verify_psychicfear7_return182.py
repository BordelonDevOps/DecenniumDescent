from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import jsonpatch

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECV = AUDIT / "rank9_psychicfear7_return182_received"
RETURN = RECV / "DD_Rank9_PsychicFear7_Director_Return182.zip"
AUDIT_OUT = AUDIT / "RANK9_PSYCHICFEAR7_RETURN182_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_02_180.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Psychic_Fear_7_Source_Conference_02_180.zip"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_179.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_179.json"
PENDING = AUDIT / "CURRENT93_PENDING_IDENTITY_AUDIT_179.json"
ALL_IDS = [
    "phantom-armageddon",
    "phantom-cataclysm",
    "psychic-scream",
    "frightful-sovereignty",
    "mass-phantom-killer",
    "weird",
    "reality-break",
]
ACCEPTED_IDS = ["phantom-armageddon", "phantom-cataclysm", "frightful-sovereignty", "reality-break"]
BLOCKED_IDS = ["psychic-scream", "mass-phantom-killer", "weird"]
BEFORE = {
    "reviewedApplied": 755,
    "pending": 93,
    "acceptedUnapplied": 0,
    "completeReviewedStandaloneProcedures": 479,
    "scopedInterfaces": 173,
}
RETURN_BYTES = 86_442_040
RETURN_SHA256 = "f36d4b42dcc1803c27e57af96b71e31b016a141ce95ebaf307c946091273bb56"
checks: list[dict] = []
failures: list[str] = []


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8"))


def canonical_hash(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha_bytes(raw)


def git_blob(path: Path) -> bytes:
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{rel}"], cwd=ROOT)


def check(label: str, passed: bool, detail=None) -> None:
    checks.append({"check": label, "passed": bool(passed), "detail": detail})
    if not passed:
        failures.append(label)


def replay_case(case: dict) -> tuple[int, int, list[str]]:
    problems: list[str] = []
    state = case["initialState"]
    events = case["events"]
    operations = 0
    if events and canonical_hash(state) != events[0]["beforeSHA256"]:
        problems.append(f"{case['id']}:initial-hash")
    for event in events:
        operations += len(event["forward"]) + len(event["inverse"])
        if state != event["before"] or canonical_hash(state) != event["beforeSHA256"]:
            problems.append(f"{case['id']}:{event['id']}:before")
            break
        try:
            advanced = jsonpatch.JsonPatch(event["forward"]).apply(state, in_place=False)
            if advanced != event["after"] or canonical_hash(advanced) != event["afterSHA256"]:
                problems.append(f"{case['id']}:{event['id']}:forward")
                break
            restored = jsonpatch.JsonPatch(event["inverse"]).apply(advanced, in_place=False)
            if restored != state:
                problems.append(f"{case['id']}:{event['id']}:inverse")
                break
            state = advanced
        except Exception as exc:
            problems.append(f"{case['id']}:{event['id']}:replay:{type(exc).__name__}")
            break
    if not problems and state != case["finalState"]:
        problems.append(f"{case['id']}:final-state")
    return len(events), operations, problems


def main() -> int:
    archive_size = RETURN.stat().st_size
    archive_hash = sha_file(RETURN)
    check(
        "Return182 ZIP matches the director's delivered byte count and SHA-256",
        archive_size == RETURN_BYTES and archive_hash == RETURN_SHA256,
        {"bytes": archive_size, "sha256": archive_hash},
    )

    with zipfile.ZipFile(RETURN, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        safe_names = [
            name
            for name in names
            if not name.startswith(("/", "\\"))
            and "\\" not in name
            and ".." not in PurePosixPath(name).parts
            and not any(part.startswith(".") for part in PurePosixPath(name).parts)
            and "__MACOSX" not in PurePosixPath(name).parts
            and "tmp" not in PurePosixPath(name).name.lower()
        ]
        check("ZIP CRC scan succeeds and member names are unique", archive.testzip() is None and len(names) == len(set(names)))
        check("ZIP contains exactly 175 safe, non-hidden, non-temporary members", len(names) == 175 and len(safe_names) == 175, {"members": len(names), "unsafe": sorted(set(names) - set(safe_names))[:10]})

        member_manifest = member_json(archive, "MEMBER_MANIFEST.json")
        expected = {row["path"]: row for row in member_manifest["members"]}
        check("Internal member manifest is the exact 174-member self-excluding allowlist", member_manifest["memberCountExcludingSelf"] == len(expected) == 174 and member_manifest["selfExcluded"].startswith("MEMBER_MANIFEST.json;") and member_manifest["hiddenOrTemporaryMembersPermitted"] is False and set(expected) == set(names) - {"MEMBER_MANIFEST.json"})
        member_mismatches: list[str] = []
        for name, row in expected.items():
            info = archive.getinfo(name)
            digest = hashlib.sha256()
            crc = 0
            total = 0
            with archive.open(name, "r") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
                    crc = zlib.crc32(block, crc)
                    total += len(block)
            if (
                total != row["bytes"]
                or total != info.file_size
                or digest.hexdigest() != row["sha256"]
                or f"{crc & 0xffffffff:08x}" != row["crc32"].lower()
                or info.CRC != (crc & 0xffffffff)
            ):
                member_mismatches.append(name)
        check("All 174 non-self members match manifest byte counts, SHA-256 and CRC32", not member_mismatches, member_mismatches[:20])

        decision = member_json(archive, "DIRECTOR_DECISION.json")
        semantic = member_json(archive, "SEMANTIC_FAILURE_CHECK.json")
        model_source = member_json(archive, "MODEL.json")
        procedures = member_json(archive, "PROCEDURES.json")
        proposals = member_json(archive, "PROCEDURE_PROPOSALS.json")
        counts = member_json(archive, "COUNTS.json")
        data_validation = member_json(archive, "DATA_VALIDATION.json")
        source_verification = member_json(archive, "SOURCE_VERIFICATION.json")
        metadata_validation = member_json(archive, "METADATA_VALIDATION.json")
        case_index = member_json(archive, "CASE_INDEX.json")
        authority_doc = member_json(archive, "CURRENT_AUTHORITY.json")
        book_candidate = archive.read("SOURCE_CONFERENCE_CANDIDATE.json")
        book_archive = archive.read("SOURCE_CONFERENCE_ARCHIVE.zip")

        identity_decisions = {row["id"]: row for row in decision["perIdentity"]}
        check("Director's partial decision accepts exactly four named identities and applies none", decision["accepted"] is False and decision["batchAccepted"] is False and decision["applied"] is False and decision["appliedIds"] == [] and decision["acceptedIds"] == ACCEPTED_IDS and decision["unacceptedIds"] == BLOCKED_IDS and decision["scopeIds"] == ALL_IDS and set(identity_decisions) == set(ALL_IDS) and all(identity_decisions[sid]["accepted"] is True and identity_decisions[sid]["applied"] is False and identity_decisions[sid]["blockerIds"] == [] for sid in ACCEPTED_IDS) and all(identity_decisions[sid]["accepted"] is False and identity_decisions[sid]["applied"] is False and identity_decisions[sid]["blockerIds"] for sid in BLOCKED_IDS), {"acceptedIds": decision["acceptedIds"], "unacceptedIds": decision["unacceptedIds"], "blockers": [row["id"] for row in decision["blockers"]]})
        semantic_held = {row["name"]: row["result"] for row in semantic["checks"] if row["result"] != "PASS"}
        check("Semantic failure check agrees with the four-ID partial acceptance and two explicit blocker groups", semantic["overall"] == "PARTIAL_PASS_WITH_REQUIRED_SOURCE_BLOCKERS" and semantic["acceptedIds"] == ACCEPTED_IDS and semantic["unacceptedIds"] == BLOCKED_IDS and {row["id"] for row in semantic["blockers"]} == {"PF182-B01", "PF182-B02"} and semantic_held == {"Death Ward, Null and head consequence": "PARTIAL_HELD", "Genuine full extra turn": "HELD"}, {"checks": len(semantic["checks"]), "held": semantic_held})
        check("All seven procedure and proposal rows remain unapplied proposals; the decision overlay is separate", [row["spellId"] for row in procedures] == ALL_IDS and len(proposals) == 7 and all(row["accepted"] is False and row["applied"] is False for row in procedures) and {row["spellId"] for row in proposals} == set(ALL_IDS) and model_source["acceptanceOverlay"] == "DIRECTOR_DECISION.json" and model_source["acceptedIds"] == ACCEPTED_IDS and model_source["applied"] is False)
        check("Data validation reports 48,108 checks, 3,851 events, 15,404 operations and no failures", data_validation["pass"] is True and data_validation["totalChecks"] == 48_108 and data_validation["failures"] == [] and data_validation["counts"]["events"] == 3_851 and data_validation["counts"]["eventOperations"] == 15_404 and sum(data_validation["checkCounts"].values()) == 48_108 and counts["dataIntegrityAndScopedChecks"] == 48_108 and counts["failedDataChecks"] == 0 and counts["events"] == 3_851 and counts["eventOperations"] == 15_404 and counts["totalReversibleOperations"] == 15_432)
        check("Source and metadata validations pass every recorded source/metadata check", source_verification["passed"] is True and len(source_verification["checks"]) == 307 and all(row.get("pass") is True for row in source_verification["checks"]) and metadata_validation["pass"] is True and len(metadata_validation["checks"]) == 600 and all(row.get("pass") is True for row in metadata_validation["checks"]))
        check("The return binds the exact current 94-source conference candidate and ZIP", len(book_candidate) == source_verification["sourceCandidateBytes"] == 713_807 and sha_bytes(book_candidate) == source_verification["sourceCandidateSHA256"] == "02a2c41116ff6a29c33db0c783de4923e1fc38b87177085936a2283ca751e3ac" and len(book_archive) > 0 and sha_bytes(book_archive) == source_verification["sourceArchiveSHA256"] == "0ccb5030479401ec7af176d32b0ec657b1fa63209e29fa7f61e56dc39d901565" and book_candidate == SOURCE_CANDIDATE.read_bytes() and book_archive == SOURCE_ARCHIVE.read_bytes())
        check("Original question, focused-question, hold and case counts match the final return", counts["procedures"] == 7 and counts["questions"] == 25 and counts["originalQuestions"] == 23 and counts["focusedQuestions"] == 2 and counts["cases"] == 100 and counts["mainCases"] == 14 and counts["branches"] == 86 and counts["heldCases"] == 4 and counts["totalIndexedHoldRecords"] == 122 and counts["proposalOperations"] == 28)
        check("Return authority is frozen at 755/93/0", authority_doc["authority"] == {"appliedReviewed": 755, "pending": 93, "acceptedUnapplied": 0, "standaloneProcedures": 479, "scopedInterfaces": 173} and decision["authorityUnchanged"]["appliedReviewed"] == 755 and decision["authorityUnchanged"]["pending"] == 93 and decision["authorityUnchanged"]["acceptedUnapplied"] == 0)

        catalog = json.loads(git_blob(CATALOG).decode("utf-8"))
        index_bytes = INDEX.read_bytes()
        index = json.loads(index_bytes.decode("utf-8-sig"))
        catalog_working = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
        catalog_git = git_blob(CATALOG)
        catalog_rows = {row["id"]: row for row in catalog["spells"]}
        current_entries = {row["id"]: row for row in index["entries"]}
        live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
        pending = read_json(PENDING)
        queue = read_json(QUEUE)
        handoff = read_json(HANDOFF)
        current_bindings = authority_doc["packetAuthorityUnchanged"]
        check("Live index/catalog/queue/handoff remain byte-bound to the return's 755/93 checkpoint", sha_bytes(index_bytes) == current_bindings["index"]["sha256"] and len(index_bytes) == current_bindings["index"]["bytes"] and sha_bytes(catalog_git) == current_bindings["catalog"]["sha256"] and len(catalog_git) == current_bindings["catalog"]["bytes"] and catalog_working == catalog and index["authoredCounts"] == {"reviewed": 755, "pending": 93} and set(ALL_IDS) <= live_pending and pending["pendingCount"] == 93 and queue["currentAuthority"]["reviewedApplied"] == handoff["currentAuthority"]["reviewedApplied"] == 755 and queue["currentAuthority"]["pending"] == handoff["currentAuthority"]["pending"] == 93)
        check("Each of the four accepted source cards is unchanged and was pending in the bound index", all(current_entries[sid]["authoredStatus"] == "pending-authored-procedure" and current_entries[sid]["sourceStatus"] == "blocked-pending-operational-review" and next(row for row in procedures if row["spellId"] == sid)["nativeCardAndAccessUnchanged"] == catalog_rows[sid] for sid in ACCEPTED_IDS))

        # Recompute each accepted procedure proposal's before/after hashes and JSON Patch.
        proposals_by_id = {row["spellId"]: row for row in proposals}
        proposal_failures = []
        for sid, row in proposals_by_id.items():
            if canonical_hash(row["before"]) != row["beforeSHA256"] or canonical_hash(row["after"]) != row["afterSHA256"]:
                proposal_failures.append(f"{sid}:hash")
                continue
            try:
                applied = jsonpatch.JsonPatch(row["forward"]).apply(row["before"], in_place=False)
                restored = jsonpatch.JsonPatch(row["inverse"]).apply(row["after"], in_place=False)
                if applied != row["after"] or restored != row["before"]:
                    proposal_failures.append(f"{sid}:forward-inverse")
            except Exception as exc:
                proposal_failures.append(f"{sid}:{type(exc).__name__}")
        check("All seven noncanonical proposal operations replay and invert exactly", not proposal_failures, proposal_failures)

        # Independently replay every case attached to an accepted identity. The three held
        # identities are excluded from application but remain bound and checked by the
        # director's full data-validation report and the archive-member hashes above.
        accepted_index_rows = [row for row in case_index if row["spellId"] in ACCEPTED_IDS]
        replay_failures: list[str] = []
        replay_events = 0
        replay_operations = 0
        case_paths: set[str] = set()
        for row in accepted_index_rows:
            name = row["path"]
            if name in case_paths:
                replay_failures.append(f"duplicate:{name}")
                continue
            case_paths.add(name)
            case = member_json(archive, name)
            if case["spellId"] not in ACCEPTED_IDS or case.get("runtimeExecuted") is True:
                replay_failures.append(f"scope-or-runtime:{case['id']}")
            event_count, op_count, problems = replay_case(case)
            if event_count != row["events"]:
                replay_failures.append(f"event-count:{case['id']}")
            replay_events += event_count
            replay_operations += op_count
            replay_failures.extend(problems[:10])
        check("Accepted-identity case records independently replay all forward/inverse state hashes", len(accepted_index_rows) == len(case_paths) and replay_events > 0 and not replay_failures, {"cases": len(case_paths), "events": replay_events, "operations": replay_operations, "failures": replay_failures[:30]})

    audit_result = {
        "id": "RANK9-PSYCHICFEAR7-RETURN182-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "accepted": not failures,
        "applied": False,
        "acceptedIds": ACCEPTED_IDS if not failures else [],
        "unacceptedIds": BLOCKED_IDS,
        "authority": BEFORE,
        "archive": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_hash, "memberCount": len(names)},
        "counts": {"cases": 100, "events": 3_851, "eventOperations": 15_404, "proposalOperations": 28, "reversibleOperations": 15_432, "dataChecks": 48_108, "sourceChecks": 307, "metadataChecks": 600, "packageChecks": 765, "savedArtifactChecks": 534},
        "independentAcceptedCaseReplay": {"cases": len(case_paths), "events": replay_events, "forwardAndInverseOperations": replay_operations, "failures": replay_failures},
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": len(failures),
        "blockers": failures,
        "checks": checks,
        "limits": "Exact partial static authored acceptance only for the four named identities. The other three identities remain blocked and unapplied; no runtime, human-play, balance, cosmology, domain-closure, or release approval is claimed.",
    }
    AUDIT_OUT.write_text(json.dumps(audit_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": audit_result["status"], "checksPassed": audit_result["checksPassed"], "checksFailed": audit_result["checksFailed"], "acceptedIds": audit_result["acceptedIds"], "caseReplay": audit_result["independentAcceptedCaseReplay"], "auditPath": AUDIT_OUT.relative_to(ROOT).as_posix()}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
