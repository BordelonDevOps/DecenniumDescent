from __future__ import annotations

import copy
import hashlib
import json
import zlib
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "environment3_return159_received"
ARCHIVE = RECEIVED / "DD_Rank8_Environment3_Director_Return159.zip"
DELIVERY = RECEIVED / "DD_Rank8_Environment3_Director_Return159_DELIVERY.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank8_Environment_3_Source_Conference_02.zip"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_environment_3_source_conference_02.json"
SOURCE_REQUEST = ROOT / "docs/audit/2026-10-08/full-game/RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_REQUEST.txt"
SOURCE_NOTES = ROOT / "docs/audit/2026-10-08/full-game/rank8-environment3-source-conference-02/CONFERENCE_NOTES.json"
SOURCE_MANIFEST = ROOT / "docs/audit/2026-10-08/full-game/rank8-environment3-source-conference-02/MANIFEST.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_REPORT = AUDIT / "RANK8_ENVIRONMENT3_SOURCE_CONFERENCE02_INDEPENDENT_VERIFICATION_159.json"
REPORT = AUDIT / "ENVIRONMENT3_RETURN159_INDEPENDENT_VERIFICATION.json"

IDS = ["absolute-silence", "control-weather", "earthquake"]
AUTHORITY = {
    "reviewedApplied": 723,
    "pending": 125,
    "acceptedUnapplied": 0,
    "completeReviewedStandaloneProcedures": 447,
}
COUNTS = {
    "procedures": 3,
    "conferenceQuestionDispositions": 15,
    "originalIdentityQuestionDispositions": 3,
    "futureObligationDispositions": 5,
    "requiredMainCases": 6,
    "distinctBranches": 29,
    "totalCases": 35,
    "wholeHeldBranches": 18,
    "events": 105,
    "eventOperations": 420,
    "proposalOperations": 12,
    "holdCategories": 15,
    "sourceBoundFiles": 71,
    "sourceArchiveMembers": 83,
}
MAIN_CASE_IDS = [
    "RANK8ENVIRONMENT3129-ABSOLUTE-SILENCE-A",
    "RANK8ENVIRONMENT3129-ABSOLUTE-SILENCE-B",
    "RANK8ENVIRONMENT3129-CONTROL-WEATHER-A",
    "RANK8ENVIRONMENT3129-CONTROL-WEATHER-B",
    "RANK8ENVIRONMENT3129-EARTHQUAKE-A",
    "RANK8ENVIRONMENT3129-EARTHQUAKE-B",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def apply_root_operations(state, operations):
    result = copy.deepcopy(state)
    for operation in operations:
        assert operation["path"] == "", f"unexpected nested operation path: {operation['path']}"
        if operation["op"] == "test":
            assert result == operation["value"], "root state test failed"
        elif operation["op"] == "replace":
            result = copy.deepcopy(operation["value"])
        else:
            raise AssertionError(f"unsupported operation: {operation['op']}")
    return result


def verify() -> dict:
    checks: list[dict] = []
    failures: list[str] = []

    def ck(label: str, value: bool) -> None:
        passed = bool(value)
        checks.append({"check": label, "passed": passed})
        if not passed:
            failures.append(label)

    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8-sig"))
    archive_sha = sha(archive_bytes)
    delivery_sha = sha(delivery_bytes)

    ck("Downloaded ZIP exact byte count and SHA-256 match delivery", len(archive_bytes) == delivery["archive"]["bytes"] == 14_025_213 and archive_sha == delivery["archive"]["sha256"] == "a62241bc136dc7b4af88312357930d201055c2a9eb3dae17d76dabdf9c7c1d92")
    ck("Delivery names the downloaded archive exactly", delivery["archive"]["fileName"] == ARCHIVE.name)
    ck("Director accepted but did not apply exactly three requested identities", delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == IDS and delivery["newAcceptedUnappliedIds"] == IDS)
    ck("Delivery binds the exact unchanged authority", delivery["inputAuthorityUnchanged"] == AUTHORITY)
    ck("Delivery does not claim canonical, runtime, play, balance, cosmology or release mutation", delivery["canonicalFilesEditedOrApplied"] is False and all(delivery["qualifications"].get(k) is False for k in ("runtimeApproval", "humanPlayApproval", "balanceApproval", "cosmologyApproval", "releaseApproval", "domainClosure", "sourceOrHistoricalProgramsExecuted", "closedCohortsReopened")))
    ck("Downloaded delivery has distinct stable content and hash", len(delivery_bytes) == 2719 and delivery_sha == sha(DELIVERY.read_bytes()))
    ck("Delivery is bound to the exact expected package counts", delivery["counts"] == COUNTS)

    source_report = read_json(SOURCE_REPORT)
    ck("Fresh source packet independent verifier passed", source_report["status"] == "PASS" and source_report["failures"] == 0 and source_report["verifiedCurrentSources"] == 71 and source_report["verifiedArchiveMembers"] == 83)

    index_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    index = json.loads(index_bytes.decode("utf-8-sig"))
    catalog = read_json(CATALOG)
    index_rows = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    ck("Live authored index remains exactly 723/125 with 447 complete procedures", index["authoredCounts"] == {"reviewed": 723, "pending": 125} and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 447)
    pending_ids = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    ck("All and only the three requested IDs are still pending in current index", len(pending_ids) == 125 and set(IDS) <= pending_ids)

    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        raw_members = {name: archive.read(name) for name in names}
        ck("Return ZIP has 65 unique members and passes CRC test", len(names) == len(set(names)) == 65 and archive.testzip() is None)
        safe = all(name and not PurePosixPath(name).is_absolute() and ".." not in PurePosixPath(name).parts and "\\" not in name and not any(part.startswith(".") for part in PurePosixPath(name).parts) for name in names)
        ck("Return ZIP members have safe exact paths", safe)

        member_manifest_bytes = raw_members["MEMBER_MANIFEST.json"]
        member_manifest = json.loads(member_manifest_bytes.decode("utf-8-sig"))
        external_binding = delivery["memberManifest"]
        ck("Outer delivery binds the inner member manifest by size, SHA and CRC", external_binding["path"] == "MEMBER_MANIFEST.json" and len(member_manifest_bytes) == external_binding["bytes"] == 17_602 and sha(member_manifest_bytes) == external_binding["sha256"] == "34d57e8f04d2fc7c238d073102e8a4659216ca4817c37672c0a2cae3ad18e724" and f"{zlib.crc32(member_manifest_bytes) & 0xffffffff:08x}" == external_binding["crc32"].lower() == "d9419866")
        manifest_rows = {row["path"]: row for row in member_manifest["members"]}
        ck("Inner manifest is an exact allowlist with no hidden or temporary members", member_manifest["archiveMemberCount"] == 65 and member_manifest["payloadHashedMemberCount"] == len(manifest_rows) == 64 and set(member_manifest["exactAllowlist"]) == set(names) and set(manifest_rows) == set(names) - {"MEMBER_MANIFEST.json"} and member_manifest["hiddenOrTempMembersAllowed"] is False)
        for name, row in manifest_rows.items():
            raw = raw_members[name]
            ck("Member binding " + name, len(raw) == row["bytes"] and sha(raw) == row["sha256"] and f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"].lower())

        model = json.loads(raw_members["MODEL.json"])
        decision = json.loads(raw_members["DIRECTOR_DECISION.json"])
        counts = json.loads(raw_members["COUNTS.json"])
        coverage = json.loads(raw_members["COVERAGE.json"])
        casebook = json.loads(raw_members["CASEBOOK.json"])
        questions = json.loads(raw_members["QUESTION_DISPOSITIONS.json"])
        original_questions = json.loads(raw_members["ORIGINAL_QUESTION_DISPOSITIONS.json"])
        future = json.loads(raw_members["FUTURE_OBLIGATION_DISPOSITIONS.json"])
        original = json.loads(raw_members["ORIGINAL_SOURCE_RECORDS.json"])
        holds = json.loads(raw_members["HOLDS.json"])
        proposal_ops = json.loads(raw_members["PROPOSAL_OPERATIONS.json"])
        independent = json.loads(raw_members["INDEPENDENT_FAILURE_CHECK.json"])
        validation = json.loads(raw_members["VALIDATION.json"])
        source_verification = json.loads(raw_members["evidence/SOURCE_VERIFICATION.json"])
        candidate = json.loads(raw_members["source/CANDIDATE.json"])

        ck("Model and decision agree on static-only acceptance and exact IDs", model["id"] == "Environment3-Director-Return159" and bool(decision["id"]) and model["accepted"] is True and model["applied"] is False and model["canonicalMutation"] is False and decision["accepted"] is True and decision["applied"] is False and decision["acceptedIds"] == IDS and decision["newAcceptedUnappliedIds"] == IDS and decision["canonicalFilesEdited"] is False and decision["blockingFindings"] == [])
        ck("Decision preserves current authority and complete-procedure count", decision["inputAuthorityUnchanged"] == AUTHORITY)
        ck("Decision, delivery, counts and validation agree", counts == COUNTS and decision["counts"] == COUNTS and delivery["counts"] == COUNTS and validation["inputAuthority"] == AUTHORITY)
        ck("Independent failure check passes with no remaining blockers", independent["passed"] is True and independent["remainingBlockers"] == [] and independent["noRuntimeOrHistoricalExecution"] is True)
        ck("Package validation passes without blockers", validation["passed"] is True and validation["blockingFindings"] == [] and validation["checks"] == 10_892 and sum(validation["checksByCategory"].values()) == 10_892)
        ck("All qualification limits are false", all(model["qualifications"].get(k) is False for k in ("runtimeApproval", "humanPlayApproval", "balanceApproval", "cosmologyApproval", "releaseApproval", "domainClosure", "sourceOrHistoricalProgramsExecuted", "closedCohortsReopened")))

        ck("Exactly three procedure records and six required cases are present", list(model["spells"]) == IDS and [row["id"] for row in coverage["requiredCases"]] == MAIN_CASE_IDS and [row["id"] for row in coverage["requiredCases"]] == MAIN_CASE_IDS)
        case_rows = casebook["cases"]
        case_by_id = {case["id"]: case for case in case_rows}
        ck("Casebook covers exactly 35 distinct cases with no actual-campaign successes", len(case_rows) == len(case_by_id) == COUNTS["totalCases"] and all(case["actualCampaignSuccess"] is False for case in case_rows))
        ck("Six main cases and 29 branches match the return counts", sum(case["kind"] == "required-main" for case in case_rows) == 6 and sum(case["kind"] == "distinct-branch" for case in case_rows) == 29)
        per_case_names = {name.removeprefix("cases/").removesuffix(".json") for name in names if name.startswith("cases/") and name.endswith(".json")}
        ck("Every case is separately serialized with no extra case files", per_case_names == set(case_by_id))

        for sid in IDS:
            procedure = model["spells"][sid]
            native = procedure["completeNativeSourceAndAccess"]
            candidate_row = next(row for row in candidate["records"] if row["spellId"] == sid)
            ck("Exact current native catalog/access binding " + sid, native == catalog_rows[sid] == candidate_row["completeCurrentCatalogSourceAndAccess"] and candidate_row["currentIndexEntry"] == index_rows[sid])
            ck("Procedure is a new static proposal with pending source status " + sid, procedure["id"] == sid and procedure["authorship"] == "NEW spell-local director proposal" and native["status"] == "blocked-pending-operational-review" and native["operational"] is None and index_rows[sid]["authoredStatus"] == "pending-authored-procedure")
            ck("Procedure references only known cases and exact retained holds " + sid, set(procedure["caseIds"]) <= set(case_by_id) and set(procedure["holdIds"]) == {row["id"] for row in holds})
            ck("Procedure mirror equals archived procedure file " + sid, json.loads(raw_members[f"procedures/{sid}.json"]) == procedure)

        candidate_questions = {row["id"]: row for row in candidate["questions"]}
        ck("All 15 unique questions are resolved exactly once", len(questions) == len(candidate_questions) == 15 and {row["id"] for row in questions} == set(candidate_questions))
        for row in questions:
            source_q = candidate_questions[row["id"]]
            original_q = {k: v for k, v in source_q.items() if k != "decisionSelected"} | {"decisionSelected": False}
            if row["id"] in {"ENV129-ADD01", "ENV129-ADD02"}:
                selection_ok = row["selectedOptionIndex"] is None and row["selectedSourceOption"] == "Focused request explicitly resolved below"
            else:
                idx = row["selectedOptionIndex"]
                selection_ok = isinstance(idx, int) and 0 <= idx < len(source_q["options"]) and row["selectedSourceOption"] == source_q["options"][idx]
            ck("Question source/options unchanged and selection is properly sourced " + row["id"], row["originalQuestionUnchanged"] == original_q and row["decisionSelected"] is True and selection_ok and row["selectionIsSourceFact"] is False)
        ck("Three original identity questions and five future obligations are preserved", len(original["originalIdentityQuestions"]) == len(original_questions) == 3 and len(original["requiredCasesUnchanged"]) == len(json.loads(raw_members["CASE_DISPOSITIONS.json"])) == 6 and len(original["futureObligationsUnchanged"]) == len(future) == 5)
        identity_rows = {row["spellId"]: row for row in candidate["records"]}
        for row in original_questions:
            sid = row["procedureId"]
            ck("Original identity question source preserved " + sid, row["originalQuestionUnchanged"] == identity_rows[sid]["completeOriginalSourceQuestionUnchanged"] and row["procedureId"] == sid)
        for ordinal, row in enumerate(future, start=1):
            ck("Future obligation preserved " + str(ordinal), row["ordinal"] == ordinal and row["originalObligationUnchanged"] == original["futureObligationsUnchanged"][ordinal - 1])

        case_dispositions = json.loads(raw_members["CASE_DISPOSITIONS.json"])
        ck("Six required case dispositions preserve source requirements", [row["id"] for row in case_dispositions] == MAIN_CASE_IDS and [row["originalRequirementUnchanged"] for row in case_dispositions] == original["requiredCasesUnchanged"])
        hold_ids = {row["id"] for row in holds}
        ck("All 15 hold categories remain retained and uniquely indexed", len(holds) == 15 and len(hold_ids) == 15 and len({row["category"] for row in holds}) == 15 and all(row["retained"] is True for row in holds) and decision["retainedHoldIds"] == sorted(hold_ids))
        whole_held = {case["id"] for case in case_rows if case["status"] == "held-dependent-case"}
        ck("All 18 conditional branches remain held", len(whole_held) == 18 and set(decision["wholeHeldBranchIds"]) == whole_held)
        ck("Coverage records the complete scope and six required cases", coverage["procedures"] == IDS and len(coverage["questionToCases"]) == 15 and len(coverage["futureObligations"]) == 5 and len(coverage["originalQuestions"]) == 3 and {row["id"] for row in coverage["allCases"]} == set(case_by_id))

        total_events = 0
        total_event_operations = 0
        for case_id, case in case_by_id.items():
            ck("Case is bounded by explicit hold records " + case_id, set(case.get("qualificationHolds", [])) <= hold_ids and set(case.get("wholeCaseHolds", [])) <= hold_ids)
            previous = case["initial"]
            prior_at = None
            for event in case["events"]:
                total_events += 1
                total_event_operations += len(event["forward"]) + len(event["inverse"])
                before_hash = sha(canonical(event["before"]))
                after_hash = sha(canonical(event["after"]))
                try:
                    forward = apply_root_operations(event["before"], event["forward"])
                    inverse = apply_root_operations(event["after"], event["inverse"])
                    op_ok = forward == event["after"] and inverse == event["before"]
                except Exception:
                    op_ok = False
                ck("Event state continuity and canonical hashes " + event["id"], event["before"] == previous and before_hash == event["beforeSHA256"] and after_hash == event["afterSHA256"])
                ck("Event full-state forward and inverse operations " + event["id"], len(event["forward"]) == 2 and len(event["inverse"]) == 2 and op_ok)
                if prior_at is not None:
                    ck("Event clock does not run backwards " + event["id"], event["at"] >= prior_at)
                prior_at = event["at"]
                previous = event["after"]
            ck("Case final state matches its last event " + case_id, previous == case["final"])
            for assertion_index, assertion in enumerate(case["assertions"]):
                path = assertion.get("path")
                if path:
                    value = case["final"]
                    try:
                        for part in path:
                            value = value[part] if isinstance(value, dict) else value[int(part)]
                        assertion_ok = value == assertion.get("expected")
                    except Exception:
                        assertion_ok = False
                    ck(f"Case assertion {case_id}#{assertion_index + 1}", assertion_ok)
            case_file = json.loads(raw_members[f"cases/{case_id}.json"])
            ck("Standalone case file mirrors the casebook " + case_id, case_file == case)
        ck("Full case/event/operation totals agree with declared counts", total_events == COUNTS["events"] and total_event_operations == COUNTS["eventOperations"])

        for proposal in proposal_ops:
            try:
                forward = apply_root_operations(proposal["before"], proposal["forward"])
                inverse = apply_root_operations(proposal["after"], proposal["inverse"])
                op_ok = forward == proposal["after"] and inverse == proposal["before"]
            except Exception:
                op_ok = False
            ck("Proposal full-state forward/inverse operation " + proposal["id"], len(proposal["forward"]) == 2 and len(proposal["inverse"]) == 2 and op_ok and proposal["scope"] == "isolated proposal data only, not a canonical patch")
        ck("Proposal operation totals agree with declared counts", len(proposal_ops) == 3 and sum(len(row["forward"]) + len(row["inverse"]) for row in proposal_ops) == COUNTS["proposalOperations"])

        source_archive_bytes = SOURCE_ARCHIVE.read_bytes()
        source_candidate_bytes = SOURCE_CANDIDATE.read_bytes()
        ck("Return carries exact source-conference archive and candidate", raw_members["source/DD_Rank8_Environment_3_Source_Conference_02.zip"] == source_archive_bytes and raw_members["source/CANDIDATE.json"] == source_candidate_bytes)
        ck("Return carries exact source request, conference notes and source manifest", raw_members["source/REQUEST.txt"] == SOURCE_REQUEST.read_bytes() and raw_members["source/CONFERENCE_NOTES.json"] == SOURCE_NOTES.read_bytes() and raw_members["source/SOURCE_MANIFEST.json"] == SOURCE_MANIFEST.read_bytes())
        ck("Embedded source archive exact hash/size/member count match", len(source_archive_bytes) == source_verification["archiveBytes"] == 10_585_509 and sha(source_archive_bytes) == source_verification["archiveSHA256"] == "4d81358a29f0d6dc0e123883dd02044c794e84b02d6cc1f87e5e8942605d56e1" and source_verification["archiveMembers"] == 83 and source_verification["crcVerified"] is True)
        ck("Return records current 723/125 source authority with no historical adoption", {k: source_verification["currentAuthority"][k] for k in AUTHORITY} == AUTHORITY and source_verification["historicalCountsAdopted"] is False and source_verification["suppliedProgramsExecuted"] is False)
        source_files = source_verification["currentSourceFiles"]
        ck("71 frozen current source file bindings are listed", len(source_files) == COUNTS["sourceBoundFiles"] and all(row["verified"] is True for row in source_files))
        with ZipFile(SOURCE_ARCHIVE) as source_zip:
            ck("Source packet nested ZIP has unique members and passes CRC", len(source_zip.namelist()) == len(set(source_zip.namelist())) == 83 and source_zip.testzip() is None)
            for row in source_files:
                path = ROOT / PurePosixPath(row["path"])
                try:
                    raw = path.read_bytes()
                    frozen = source_zip.read("sources/" + row["path"])
                    ok = len(raw) == row["bytes"] and sha(raw) == row["sha256"] and frozen == raw
                except Exception:
                    ok = False
                ck("Current and frozen source binding " + row["path"], ok)
        for label in ("index", "catalog", "currentQueue", "pendingIdentityAudit", "priorHandoff"):
            binding = source_verification["currentAuthority"][label]
            path = ROOT / PurePosixPath(binding["path"])
            try:
                raw = path.read_bytes()
                ok = len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
            except Exception:
                ok = False
            ck("Current authority binding " + label, ok)

        exact_interfaces = json.loads(raw_members["evidence/EXACT_ACCEPTED_INTERFACES.json"])
        ck("Exact accepted-interface comparison evidence is present and scoped", len(exact_interfaces["interfacesUnchanged"]) == 35 and len(exact_interfaces["counterpartsUnchanged"]) == 9 and len(exact_interfaces["recentAppliedPerception5Unchanged"]) == 1 and len(exact_interfaces["historicalPendingNowReviewedUnchanged"]) == 3 and len(exact_interfaces["provisionalExpeditionComparisonsUnchanged"]) == 4 and "no closed" in exact_interfaces["scope"].lower())
        counter_scope = json.loads(raw_members["evidence/COUNTERPART_SCOPE_CHECK.json"])
        ck("Comparison checks did not execute historical programs or grant broad authority", counter_scope["historicalProgramsExecuted"] is False)

    report = {
        "id": "ENVIRONMENT3-RETURN159-INDEPENDENT-VERIFICATION",
        "status": "PASS" if not failures else "FAIL",
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(archive_bytes), "sha256": archive_sha},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_bytes), "sha256": delivery_sha},
        "authority": AUTHORITY,
        "acceptedIds": IDS,
        "checkCount": len(checks),
        "failures": len(failures),
        "failedChecks": failures,
        "checks": checks,
        "scope": "Independent integrity, source/authority binding, exact identity, hold, case/state transition, and proposal inverse verification. Static authored review only; no runtime or source program execution.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = verify()
    print(json.dumps({k: result[k] for k in ("status", "checkCount", "failures", "failedChecks", "archive", "delivery", "acceptedIds", "authority")}, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)
