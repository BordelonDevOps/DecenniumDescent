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
RECV = AUDIT / "rank9_stormcontrol6_return177_received"
RETURN = RECV / "DD_Rank9_StormControl6_Director_Return177.zip"
DELIVERY = RECV / "DD_Rank9_StormControl6_Director_Return177_DELIVERY.json"
AUDIT_OUT = AUDIT / "RANK9_STORMCONTROL6_RETURN177_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_storm_control_6_source_conference_02_175.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Storm_Control_6_Source_Conference_02_175.zip"
IDS = [
    "cosmic-implosion",
    "frozen-eternity",
    "hellstorm",
    "storm-of-vengeance",
    "thunder-wrath",
    "storm-cage",
]
BEFORE = {"reviewedApplied": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173}
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


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8"))


def canonical_hash(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha_bytes(raw)


def check(label: str, passed: bool, detail=None) -> None:
    row = {"check": label, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    if not passed:
        failures.append(label)


def replay_case(case: dict) -> tuple[int, int, list[str]]:
    problems: list[str] = []
    events = case["events"]
    operations = sum(len(event["forward"]) + len(event["inverse"]) for event in events)
    state = case["initialState"]
    if events and canonical_hash(state) != events[0]["beforeSHA256"]:
        problems.append(f"{case['id']}:initial-hash")
    for event in events:
        if state != event["beforeState"] or canonical_hash(state) != event["beforeSHA256"]:
            problems.append(f"{case['id']}:{event['id']}:before")
            break
        try:
            advanced = jsonpatch.JsonPatch(event["forward"]).apply(state, in_place=False)
            if advanced != event["afterState"] or canonical_hash(advanced) != event["afterSHA256"]:
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
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8"))
    archive_bytes = RETURN.stat().st_size
    archive_hash = sha_file(RETURN)
    check(
        "The saved ZIP matches the delivered filename, byte count, and SHA-256",
        RETURN.name == delivery["archive"]["fileName"]
        and archive_bytes == delivery["archive"]["bytes"] == 105824642
        and archive_hash == delivery["archive"]["sha256"] == "ae787f7f830262075483f7de1a6391da2d7bdb4a144cb611d9f53d7bf8750674",
        {"bytes": archive_bytes, "sha256": archive_hash},
    )
    check("Delivery says exactly six accepted IDs, unapplied, against 749/99/0", delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS and delivery["sourceAuthority"] == {"appliedReviewed": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173})
    check("Delivery member manifest is a 140-member exact allowlist", delivery["memberCount"] == len(delivery["members"]) == 140 and len({row["path"] for row in delivery["members"]}) == 140)

    streamed_members = 0
    hash_mismatches: list[str] = []
    unsafe_names: list[str] = []
    with zipfile.ZipFile(RETURN, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        expected_members = {row["path"]: row for row in delivery["members"]}
        check("ZIP member names are unique and exactly match the external allowlist", len(infos) == 140 and len(set(names)) == 140 and set(names) == set(expected_members))
        for name in names:
            path = PurePosixPath(name)
            if name.startswith(("/", "\\")) or "\\" in name or ".." in path.parts or "__MACOSX" in path.parts or any(part.startswith(".") for part in path.parts) or "tmp" in path.name.lower():
                unsafe_names.append(name)
        check("ZIP has no hidden, temporary, or traversal member paths", not unsafe_names, unsafe_names[:20])
        info_by_name = {item.filename: item for item in infos}
        for name, expected in expected_members.items():
            digest = hashlib.sha256()
            crc = 0
            total = 0
            with archive.open(name, "r") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
                    crc = zlib.crc32(block, crc)
                    total += len(block)
            info = info_by_name.get(name)
            if (info is None or total != expected["bytes"] or total != info.file_size
                    or digest.hexdigest() != expected["sha256"]
                    or f"{crc & 0xffffffff:08x}" != expected["crc32"].lower()
                    or info.CRC != (crc & 0xffffffff)):
                hash_mismatches.append(name)
            streamed_members += 1
        check("All 140 archive members independently match size, SHA-256, and ZIP CRC32", streamed_members == 140 and not hash_mismatches, hash_mismatches[:20])

        decision = member_json(archive, "DIRECTOR_DECISION.json")
        semantic = member_json(archive, "SEMANTIC_FAILURE_CHECK.json")
        model = member_json(archive, "MODEL.json")
        procedures_wrapper = member_json(archive, "PROCEDURES.json")
        procedures = procedures_wrapper["procedures"]
        case_index = member_json(archive, "CASE_INDEX.json")
        dispositions = member_json(archive, "CASE_DISPOSITIONS.json")
        data_validation = member_json(archive, "DATA_VALIDATION.json")
        source_verification = member_json(archive, "SOURCE_VERIFICATION.json")
        accepted_comparisons = member_json(archive, "ACCEPTED_COMPARISON_VERIFICATION.json")
        auxiliary = member_json(archive, "AUXILIARY_SOURCE_VERIFICATION.json")
        final_metadata = member_json(archive, "FINAL_METADATA_VALIDATION.json")
        profile = member_json(archive, "PROFILE_REPAIR_EVIDENCE.json")
        clock = member_json(archive, "REGULAR_CLOCK_FAILURE_CHECK.json")
        qualified_extra_turn = member_json(archive, "QUALIFIED_EXTRA_TURN_OBLIGATION.json")
        holds = member_json(archive, "HOLD_REGISTER.json")
        member_manifest = member_json(archive, "MEMBER_MANIFEST.json")

        check("Director and semantic decisions agree: accepted, unapplied, exact IDs, no blockers", decision["accepted"] is True and decision["applied"] is False and decision["acceptedIds"] == IDS and decision["reviewedIds"] == IDS and decision["blockers"] == [] and semantic["passed"] is True and semantic["acceptedIds"] == IDS and semantic["applied"] is False and semantic["blockers"] == [])
        check("Three Return176 findings are explicitly qualified/resolved without overstating evidence", {row["id"]: row["blocking"] for row in decision["priorFindingDispositions"]} == {"ST176-B01": False, "ST176-B02": False, "ST176-B03": False} and qualified_extra_turn["positiveProofClaim"] is False and qualified_extra_turn["blockingForStaticSpellAuthorship"] is False and clock["unresolvedOverdueActorRecords"] == 0)
        check("Model authority and six procedure records stay unapplied with exact IDs", model["accepted"] is True and model["applied"] is False and {key: model["authority"][key] for key in BEFORE} == BEFORE and [row["spellId"] for row in procedures] == IDS and all(row["accepted"] is True and row["applied"] is False for row in procedures))
        check("Source, comparison, auxiliary, and metadata verification reports pass", source_verification["passed"] is True and source_verification["checkCount"] == 311 and source_verification["failures"] == [] and all(row.get("passed") is True for row in source_verification["checks"]) and accepted_comparisons["passed"] is True and accepted_comparisons["checkCount"] == 106 and all(row["authorityHashMatch"] is True and row["snapshotMatchesCurrent"] is True for row in accepted_comparisons["interfaces"]) and all(row["wholeSourceMatch"] is True and row["cardObjectMatch"] is True for row in accepted_comparisons["counterparts"]) and auxiliary["checkCount"] == 10 and all(row.get("passed") is True for row in auxiliary["checks"]) and final_metadata["passed"] is True and final_metadata["checkCount"] == 225 and final_metadata["failures"] == [])
        expected_counts = {"procedures": 6, "questions": 27, "originalQuestions": 25, "focusedAdditionalQuestions": 2, "mainCases": 12, "branches": 49, "caseRecords": 61, "events": 2592, "eventOperations": 10368, "proposalOperations": 24, "conditionalOutcomeBranches": 7, "unobservedInputDecisionPoints": 1, "originalCaseRecordsPreserved": 54, "sourcePreconditionHoldRecords": 6, "originalFutureObligations": 10, "localHolds": 8, "inheritedScopedHoldRecords": 87, "totalScopedHoldRecords": 95, "dataAndScopedSemanticChecks": 57066, "failedChecks": 0, "acceptanceBlockers": 0, "repairedPriorClockCases": 43, "repairedPriorClockActorRecords": 213, "retainedOriginalSourceChecks": 311, "retainedAcceptedComparisonChecks": 106, "retainedAuxiliarySourceChecks": 10}
        check("Decision/delivery counts match the exact six-procedure, 61-case repair", delivery["counts"] == decision["counts"] == expected_counts)
        check("All GPT data validations report 57,066 passes and zero failures", data_validation["passed"] is True and data_validation["passedCount"] == 57066 and data_validation["failedCount"] == 0 and data_validation["failures"] == [] and data_validation["checks"] == 57066 and len(data_validation["caseReports"]) == 61 and all(row.get("failures") == 0 for row in data_validation["caseReports"]))
        check("B02 replacement profile is source-qualified Monk3 Whirlwind Stance", profile["passed"] is True and len(profile["checks"]) == 33 and all(row["passed"] is True for row in profile["checks"]) and any(row["level"] == 3 and row["cardId"] == "monk.arch.whirlwind-stance" for row in profile["replacementProfile"]["acquisitions"]))
        check("B03 repairs all 43 listed prior cases/213 actors and keeps seven dice outcomes conditional", clock["passed"] is True and clock["originalAffectedCases"] == 43 and clock["originalAffectedActorRecords"] == 213 and clock["reviewedCaseRecords"] == 61 and clock["unresolvedOverdueActorRecords"] == 0 and len(clock["repairedOriginalFindings"]) == 43 and sum(len(row["actors"]) for row in clock["repairedOriginalFindings"]) == 213 and all(row["repaired"] is True for row in clock["repairedOriginalFindings"]) and "7 full conditional continuations" in clock["conditionalInput"])
        check("All 95 scoped hold records remain separated into 8 local and 87 inherited", holds["counts"] == {"local": 8, "inheritedScopedRecords": 87, "totalScopedRecords": 95} and len(holds["localHolds"]) == 8 and len(holds["inheritedExactScopeRecords"]) == 87)
        check("Internal exact allowlist binds all 140 package members", member_manifest["memberCount"] == 140 and set(member_manifest["exactAllowlist"]) == set(names) and member_manifest["hiddenTemporaryMembers"] == 0)
        check("Case index and dispositions preserve 12 main/49 branch case records", len(case_index["orderedCaseIds"]) == 61 and len(set(case_index["orderedCaseIds"])) == 61 and len(dispositions["cases"]) == 61 and {row["id"] for row in dispositions["cases"]} == set(case_index["orderedCaseIds"]))

        case_paths = [name for name in names if name.startswith("cases/") and name.endswith(".json")]
        replayed_case_ids: set[str] = set()
        event_total = 0
        operation_total = 0
        replay_failures: list[str] = []
        case_kind_counts = {"main": 0, "branch": 0}
        case_hold_count = 0
        for name in case_paths:
            case = member_json(archive, name)
            if case["id"] in replayed_case_ids:
                replay_failures.append(f"duplicate-case:{case['id']}")
                continue
            replayed_case_ids.add(case["id"])
            case_kind_counts[case["kind"]] += 1
            case_hold_count += bool(case.get("holds"))
            if case.get("runtimeExecuted") is not False:
                replay_failures.append(f"runtime-executed:{case['id']}")
            events, operations, problems = replay_case(case)
            event_total += events
            operation_total += operations
            replay_failures.extend(problems[:10])
            calendars = case.get("actorCalendars", {})
            for actor_id, calendar in calendars.items():
                period = calendar["periodSeconds"]
                offset = calendar["endOffsetSeconds"]
                starts = calendar["starts"]
                ends = calendar["ends"]
                if (starts and abs(starts[0] - calendar["firstPendingStart"]) > 1e-9) or any(abs((starts[i] - starts[i - 1]) - period) > 1e-9 for i in range(1, len(starts))):
                    replay_failures.append(f"calendar-start-spacing:{case['id']}:{actor_id}")
                initial_start = calendar["initialLastStart"]
                aligned = len(ends) <= len(starts) and all(abs(ends[i] - (starts[i] + offset)) <= 1e-9 for i in range(len(ends)))
                leading_initial = (initial_start is not None and len(ends) <= len(starts) + 1 and bool(ends)
                                   and abs(ends[0] - (initial_start + offset)) <= 1e-9
                                   and all(abs(ends[i] - (starts[i - 1] + offset)) <= 1e-9 for i in range(1, len(ends))))
                if not (aligned or leading_initial):
                    replay_failures.append(f"calendar-end-offset:{case['id']}:{actor_id}")
        check("All 61 standalone case files independently replay every forward/inverse event and state hash", len(case_paths) == len(replayed_case_ids) == 61 and replayed_case_ids == set(case_index["orderedCaseIds"]) and event_total == 2592 and operation_total == 10368 and not replay_failures, {"caseFiles": len(case_paths), "events": event_total, "operations": operation_total, "failures": replay_failures[:30]})
        check("Case type totals are 12 main and 49 branches; all scheduled actor calendars are regular", case_kind_counts == {"main": 12, "branch": 49} and not [item for item in replay_failures if item.startswith("calendar-")])

    # Compare the director's source snapshot with the current, unchanged canonical source files.
    index = read(INDEX)
    catalog = read(CATALOG)
    entries = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    pending = sorted(row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure")
    git_index = subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{INDEX.relative_to(ROOT).as_posix()}"], cwd=ROOT)
    git_catalog = subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{CATALOG.relative_to(ROOT).as_posix()}"], cwd=ROOT)
    model_authority = model["authority"]
    check("Current canonical Git blobs match the return's bound 749/99 authority", sha_bytes(git_index) == model_authority["index"]["sha256"] == "d7157bb971283767404868ca6e3c662feb38b3d5e5c2a73fcd3980486ca65bdb" and len(git_index) == model_authority["index"]["bytes"] and sha_bytes(git_catalog) == model_authority["catalog"]["sha256"] == "f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8" and len(git_catalog) == model_authority["catalog"]["bytes"])
    check("Live pending set still contains exactly 99 identities and all six remain pending", index["authoredCounts"] == {"reviewed": 749, "pending": 99} and len(pending) == 99 and set(IDS) <= set(pending) and all(entries[sid]["authoredStatus"] == "pending-authored-procedure" and entries[sid]["sourceStatus"] == "blocked-pending-operational-review" for sid in IDS))
    procedures = {row["spellId"]: row for row in procedures}
    check("All six accepted rows preserve native catalog cards and unchanged class-access/source fields", all(procedures[sid]["nativeCardUnchanged"] == catalog_rows[sid] for sid in IDS))
    source_member = None
    with zipfile.ZipFile(RETURN, "r") as archive:
        source_member = archive.read("SOURCE_CONFERENCE_CANDIDATE.json")
        packet_member = archive.read("SOURCE_CONFERENCE_ARCHIVE.zip")
    check("Return embeds the exact source conference candidate and archive already in the repository", source_member == SOURCE_CANDIDATE.read_bytes() and packet_member == SOURCE_ARCHIVE.read_bytes())
    check("Current pre-application queue is still at 749/99 and identifies the six accepted rows", read(AUDIT / "CURRENT_HANDOFF_178.json")["currentAuthority"] == BEFORE and read(AUDIT / "CURRENT_SPELL_QUEUE_178.json")["currentAuthority"] == BEFORE)
    check("Independent verification itself performs no canonical application", index["authoredCounts"] == {"reviewed": 749, "pending": 99} and delivery["applied"] is False)

    result = {
        "id": "RANK9-STORMCONTROL6-RETURN177-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "accepted": not failures and delivery["accepted"] is True,
        "applied": False,
        "acceptedIds": IDS if not failures else [],
        "blockers": failures,
        "authority": BEFORE,
        "archive": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": archive_bytes, "sha256": archive_hash, "memberCount": streamed_members},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_bytes), "sha256": sha_bytes(delivery_bytes)},
        "counts": delivery["counts"],
        "independentCaseReplay": {"cases": 61, "events": event_total, "forwardAndInverseOperations": operation_total, "failures": replay_failures},
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": len(failures),
        "checks": checks,
        "limits": "Static authored spell review only. Extra-turn source and unobserved dice remain qualified/held; no runtime, campaign, human-play, balance, cosmology, domain-closure, or release approval is granted.",
    }
    AUDIT_OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"audit": AUDIT_OUT.relative_to(ROOT).as_posix(), "status": result["status"], "checksPassed": result["checksPassed"], "checksFailed": result["checksFailed"], "eventsReplayed": event_total, "acceptedIds": result["acceptedIds"], "blockers": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
