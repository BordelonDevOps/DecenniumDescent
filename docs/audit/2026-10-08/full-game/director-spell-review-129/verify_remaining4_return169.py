from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
RECV = AUDIT / "remaining4_return169_received"
PAYLOAD = RECV / "payload"
RETURN = RECV / "DD_Rank8_Remaining4_Director_Return169.zip"
DELIVERY = RECV / "DD_Rank8_Remaining4_Director_Return169_DELIVERY.json"
LOCAL_PACKET = FULL / "DD_Rank8_Remaining_4_Source_Conference_02.zip"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_remaining_4_source_conference_02.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_169.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_169.json"
IDS = ["prismatic-wall", "faction-convergence", "divine-intervention-lesser", "reality-patch"]
AUTHORITY = {"reviewedApplied": 735, "pending": 113, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 459, "scopedInterfaces": 173}
checks: list[dict] = []
failures: list[str] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check(label: str, ok: bool, detail=None) -> None:
    checks.append({"check": label, "passed": bool(ok), **({"detail": detail} if detail is not None else {})})
    if not ok:
        failures.append(label)


def canonical_hash(value) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def main() -> int:
    delivered = read(DELIVERY)
    zip_bytes = RETURN.read_bytes()
    manifest_bytes = (PAYLOAD / "MEMBER_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    with zipfile.ZipFile(RETURN) as archive:
        infos = archive.infolist()
        names = [entry.filename for entry in infos]
        corrupt = archive.testzip()
        members = {name: archive.read(name) for name in names}

    check("Downloaded return ZIP matches GPT delivery size and SHA-256", len(zip_bytes) == delivered["archive"]["bytes"] == 29362298 and sha(zip_bytes) == delivered["archive"]["sha256"] == "081aa49e33c7df0965428db6a63bbcbf656f226e3f496976a68750fb90330b0e")
    check("GPT decision and delivery agree on accepted=true, applied=false, and the exact four IDs", delivered["accepted"] is True and delivered["applied"] is False and delivered["acceptedIds"] == IDS)
    check("ZIP CRC passes and the archive has exactly 85 unique members", corrupt is None and len(names) == 85 and len(set(names)) == 85 and delivered["archive"]["members"] == 85)
    unsafe = [name for name in names if name.startswith(("/", "\\")) or ".." in PurePosixPath(name).parts or "\\" in name]
    check("Archive members contain no absolute paths, traversal, or duplicate entries", not unsafe, unsafe[:5])
    allowlist = set(manifest["allowlistIncludingThisManifest"])
    expected_members = {item["path"]: item for item in manifest["members"]}
    check("Member manifest allowlist exactly matches ZIP names", allowlist == set(names) and len(manifest["members"]) == 84 and manifest["memberCountIncludingThisManifest"] == 85)
    member_mismatches = []
    for name, item in expected_members.items():
        data = members.get(name)
        info = next((entry for entry in infos if entry.filename == name), None)
        if data is None or info is None or len(data) != item["bytes"] or sha(data) != item["sha256"] or f"{info.CRC:08x}" != item["crc32"]:
            member_mismatches.append(name)
    check("All 84 payload member byte lengths, SHA-256 values, and CRC32 values match manifest", not member_mismatches, member_mismatches[:10])
    check("Delivery JSON saved from GPT matches the downloaded local copy", sha(DELIVERY.read_bytes()) == "f368bf22d7f392f7a9d011571f19f8f593b76e144150a9a3fbf38898aec21dbc")

    decision = json.loads(members["DIRECTOR_ACCEPTANCE.json"])
    counts = json.loads(members["COUNTS.json"])
    check("Archive decision independently confirms only the exact four IDs and no blockers", decision["accepted"] is True and decision["applied"] is False and decision["acceptedIds"] == IDS and decision["unacceptedIds"] == [] and decision["blockingFindings"] == [])
    check("Pre-decision authority is exactly 735/113/0 and 459 complete standalone procedures", decision["authoritySnapshotBeforeDecision"] == {"reviewedApplied": 735, "pending": 113, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 459})
    check("Expected authority after a separate four-ID application is 739/109 and 463 procedures", decision["expectedCountsOnlyAfterSeparateApplication"] == {"reviewedApplied": 739, "pending": 109, "completeReviewedStandaloneProcedures": 463})
    expected_counts = {"procedures": 4, "sourceQuestions": 22, "selectedDispositions": 22, "originalFutureCaseObligations": 6, "mainCases": 9, "branches": 38, "totalCases": 47, "events": 539, "reversibleEventOperations": 2156, "proposalOperations": 16, "holds": 29, "newQualificationHolds": 12, "inheritedGodsSourceHolds": 17, "wholeCaseHeldBranches": 4, "sourceArchiveMembers": 124, "currentSourceBindings": 113, "exactAcceptedInterfaceComparisons": 31, "exactCompleteSpellComparisons": 14, "sourceVerificationChecks": 223, "runtimeTests": 0, "humanPlaytests": 0, "independentFinalDataChecks": 16261, "independentFinalDataFailures": 0}
    check("Published counts exactly match the decision counts", counts == expected_counts and decision["counts"] == expected_counts)

    source = json.loads(members["SOURCE_VERIFICATION.json"])
    check("All 223 director source-verification checks pass", len(source["checks"]) == 223 and source["checksPassed"] == 223 and all(row.get("pass") is True for row in source["checks"]))
    check("Return binds the exact Conference02 archive submitted to GPT", source["archive"] == {"bytes": 26416138, "sha256": "42de110748cc76cb52f790c6cd719f5d8db7676cde6d6cd900f0e926610fbf90", "memberCount": 124, "CRC": "pass"} and members["source/DD_Rank8_Remaining_4_Source_Conference_02.zip"] == LOCAL_PACKET.read_bytes())
    source_candidate = json.loads(members["source/CANDIDATE.json"])
    local_candidate_bytes = CANDIDATE.read_bytes()
    check("Embedded source candidate is byte-identical to the submitted public candidate", members["source/CANDIDATE.json"] == local_candidate_bytes)
    check("All 113 current source bindings still match live repository bytes", len(source["currentBindings"]) == 113 and all((ROOT / binding["path"]).is_file() and (ROOT / binding["path"]).stat().st_size == binding["bytes"] and sha((ROOT / binding["path"]).read_bytes()) == binding["sha256"] for binding in source["currentBindings"]))
    check("Live index and catalog bindings equal the 735/113 submitted baseline", len(INDEX.read_bytes()) == source["authority"]["index"]["bytes"] and sha(INDEX.read_bytes()) == source["authority"]["index"]["sha256"] and len(CATALOG.read_bytes()) == source["authority"]["catalog"]["bytes"] and sha(CATALOG.read_bytes()) == source["authority"]["catalog"]["sha256"])
    embedded_packet = zipfile.ZipFile(LOCAL_PACKET)
    packet_manifest = json.loads(embedded_packet.read("MANIFEST.json"))
    embedded_candidate = json.loads(embedded_packet.read("CANDIDATE.json"))
    original_questions = embedded_candidate["questions"]
    qdata = json.loads(members["QUESTION_DISPOSITIONS.json"])
    qrows = qdata["questions"]
    check("All 22 exact source questions are preserved and individually selected", len(original_questions) == len(qrows) == 22 and [q["id"] for q in original_questions] == [q["id"] for q in qrows] and all(q["originalUnchanged"] == original_questions[i] and isinstance(q.get("selectedOptionIndex"), int) and q.get("status") == "authored-qualified" for i, q in enumerate(qrows)))
    check("No source verification check reports a non-pass and superseded 525/323 history is not adopted", source["historicalAuthoritySuperseded"] == [525, 323] and source["laterEditsAccepted"] is False and source["sourceProgramsExecuted"] is False)

    procedures = json.loads(members["PROCEDURES.json"])
    procedure_rows = procedures["procedures"]
    check("All four complete procedure records are present in exact accepted-ID order", [p["id"] for p in procedure_rows] == IDS and len(procedure_rows) == 4)
    index = read(INDEX)
    catalog = read(CATALOG)
    live_rows = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    native_ok = True
    for procedure in procedure_rows:
        sid = procedure["id"]
        native = procedure["nativeSource"]
        current = source_candidate["records"][IDS.index(sid)]["completeCurrentCatalogSourceAndAccess"]
        native_ok &= live_rows[sid]["authoredStatus"] == "pending-authored-procedure"
        native_ok &= current == catalog_rows[sid]
        native_ok &= native == catalog_rows[sid]
        native_ok &= procedure.get("implementationStatus") == "authored review only; not applied"
    check("Four procedure native catalog/class-access rows exactly preserve the live source and remain pending", native_ok)

    casebook = json.loads(members["CASEBOOK.json"])
    case_rows = casebook["cases"]
    events = [event for case in case_rows for event in case["events"]]
    event_operations = sum(len(event["forward"]) + len(event["inverse"]) for event in events)
    check("Casebook has 47 uniquely identified cases, 539 events, and 2,156 reversible operations", len(case_rows) == len({c["id"] for c in case_rows}) == 47 and len(events) == 539 and event_operations == 2156 and sum(c["eventCount"] for c in case_rows) == 539 and sum(c["eventOperationCount"] for c in case_rows) == 2156)
    cases_failures = []
    try:
        import jsonpatch

        for case in case_rows:
            state = case["initialState"]
            if canonical_hash(state) != case["initialSHA256"]:
                cases_failures.append(f"{case['id']}:initial-hash")
                continue
            for event in case["events"]:
                if state != event["before"] or canonical_hash(state) != event["beforeSHA256"]:
                    cases_failures.append(f"{case['id']}:{event['id']}:before")
                    break
                advanced = jsonpatch.JsonPatch(event["forward"]).apply(state, in_place=False)
                if advanced != event["after"] or canonical_hash(advanced) != event["afterSHA256"]:
                    cases_failures.append(f"{case['id']}:{event['id']}:forward")
                    break
                restored = jsonpatch.JsonPatch(event["inverse"]).apply(advanced, in_place=False)
                if restored != state:
                    cases_failures.append(f"{case['id']}:{event['id']}:inverse")
                    break
                state = advanced
            if case["id"] in [item.split(":")[0] for item in cases_failures]:
                continue
            if state != case["finalState"] or canonical_hash(state) != case["finalSHA256"]:
                cases_failures.append(f"{case['id']}:final")
    except Exception as exc:
        cases_failures.append(f"replay-error:{type(exc).__name__}:{exc}")
    check("Independent forward replay, inverse replay, continuity, and final hashes pass for every case", not cases_failures, cases_failures[:10])

    hold_register = json.loads(members["HOLD_REGISTER.json"])
    hold_ids = [hold["id"] for hold in hold_register["holds"]]
    held_cases = decision["heldCaseIds"]
    check("All 29 holds remain retained and exact accepted hold IDs match the register", len(hold_ids) == 29 and len(set(hold_ids)) == 29 and set(hold_ids) == set(decision["retainedHoldIds"]) and all(hold["status"] in {"retained", "retained-original"} for hold in hold_register["holds"]))
    check("Four whole-case held branches stay explicitly held", held_cases == ["RR169-PW-A/stun-immune", "RR169-PW-H/transport", "RR169-DI-H/unsupported-payload", "RR169-RP-H/unknown-profile"] and all(next(c for c in case_rows if c["id"] == case_id)["status"] == "held-whole" for case_id in held_cases))
    semantic = json.loads(members["SEMANTIC_FAILURE_CHECK.json"])
    validation = json.loads(members["VALIDATION.json"])
    check("Final independent data check has 16,261 passes and zero failures", semantic["finalIndependentDataResult"] == {"passed": 16261, "failed": 0, "file": "VALIDATION.json"} and validation["passed"] == 16261 and validation["failed"] == 0 and validation["runtimeExecuted"] is False and validation["sourceOrHistoricalProgramsExecuted"] is False)
    check("Semantic review has no unresolved blockers and explicitly keeps all five qualifications unapproved", semantic["unresolvedBlockingFindings"] == [] and all(term in semantic["qualifications"].lower() for term in ["no runtime", "human-play", "balance", "cosmology", "release"]))
    check("Return preserves the 29 holds, four held cases and all five qualification boundaries", decision["counts"]["holds"] == 29 and decision["counts"]["wholeCaseHeldBranches"] == 4 and all(decision["qualifications"][k] is False for k in ["runtimeApproved", "humanPlayApproved", "balanceApproved", "cosmologyApproved", "releaseApproved"]))

    queue = read(QUEUE)
    handoff = read(HANDOFF)
    check("Current queue and handoff still bind the submitted 735/113 baseline and exact four-ID decision scope", queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY and queue["currentPendingGroups"][0]["pendingIds"] == IDS and handoff["directorSubmission"]["reviewIds"] == IDS)
    submission_path = ROOT / read(AUDIT / "REMAINING4_GPT_SUBMISSION_169.json")["receiptPath"] if "receiptPath" in read(AUDIT / "REMAINING4_GPT_SUBMISSION_169.json") else AUDIT / "REMAINING4_GPT_SUBMISSION_169.json"
    check("No canonical file changed after packet submission and the handoff binds the receipt", handoff["currentIndexBinding"]["sha256"] == sha(INDEX.read_bytes()) and handoff["currentCatalogBinding"]["sha256"] == sha(CATALOG.read_bytes()) and handoff["currentSubmissionBinding"]["bytes"] == submission_path.stat().st_size and handoff["currentSubmissionBinding"]["sha256"] == sha(submission_path.read_bytes()))

    result = {
        "id": "REMAINING4-RETURN-INDEPENDENT-AUDIT-169",
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks),
        "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures),
        "failedChecks": failures,
        "checks": checks,
        "accepted": True,
        "applied": False,
        "acceptedIds": IDS,
        "authorityBeforeApplication": AUTHORITY,
        "directorReturn": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": len(zip_bytes), "sha256": sha(zip_bytes)},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())},
        "sourceBindingsChecked": len(source["currentBindings"]),
        "eventCount": len(events),
        "reversibleEventOperations": event_operations,
    }
    output = AUDIT / "REMAINING4_RETURN169_INDEPENDENT_AUDIT.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ["id", "status", "checkCount", "checksPassed", "checksFailed", "failedChecks", "acceptedIds", "sourceBindingsChecked", "eventCount", "reversibleEventOperations"]}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
