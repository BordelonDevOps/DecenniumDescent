from __future__ import annotations

import hashlib
import io
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import jsonpatch


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_agencycontrol9_return190_received"
ARCHIVE = RECEIVED / "DD_Rank9_AgencyControl9_Director_Return190.zip"
DELIVERY = RECEIVED / "DD_Rank9_AgencyControl9_Director_Return190_DELIVERY.json"
INPUT_PACKET = AUDIT / "rank9_agencycontrol9_return189_prepared/DD_Rank9_AgencyControl9_CurrentSource_189.zip"
INPUT_DELIVERY = AUDIT / "rank9_agencycontrol9_return189_prepared/DD_Rank9_AgencyControl9_CurrentSource_189_DELIVERY.json"
REPORT = AUDIT / "RANK9_AGENCYCONTROL9_RETURN190_INDEPENDENT_AUDIT.json"
SOURCE_COMMIT = "0d09d2b2b409d179207763dd4023961c6a1be491"
PUBLISH_COMMIT = "039e9730b790773a74e606de789d85c4e7833a9d"
GROUP = [
    "absolute-domination",
    "command-reality",
    "dominate-legion",
    "erase-soul",
    "overwhelming-presence",
    "perfect-mesmerize",
    "prophecy-fulfilled",
    "puppetmaster-s-realm",
    "rewrite-loyalty",
]
ACCEPTED = [
    "command-reality",
    "dominate-legion",
    "erase-soul",
    "overwhelming-presence",
    "perfect-mesmerize",
    "prophecy-fulfilled",
    "rewrite-loyalty",
]
UNACCEPTED = ["absolute-domination", "puppetmaster-s-realm"]
BLOCKERS = {"absolute-domination": ["AG190-B01"], "puppetmaster-s-realm": ["AG190-B02"]}
NEXT_IDS = [
    "time-stop",
    "time-fracture",
    "foresight-perfect",
    "fate-rewrite",
    "collapse-timeline",
    "eternal-prophecy",
]
AUTHORITY = {
    "reviewedApplied": 770,
    "pending": 78,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 494,
    "scopedInterfaces": 173,
}

checks: list[dict] = []
failures: list[str] = []


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def member_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8-sig"))


def check(label: str, passed: bool, detail=None) -> None:
    row = {"check": label, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    if not passed:
        failures.append(label)


def replay(case: dict) -> tuple[int, int, int]:
    state = case["initialState"]
    if sha(canonical(state)) != case["initialSHA256"]:
        raise AssertionError("initial full-state hash mismatch")
    prior_time = state.get("timestampDS", -1)
    forward_ops = inverse_ops = 0
    seen = set()
    for event in case["events"]:
        if event["id"] in seen:
            raise AssertionError(f"duplicate local event id {event['id']}")
        seen.add(event["id"])
        before, after = event["before"], event["after"]
        if state != before:
            raise AssertionError(f"event {event['id']} does not continue the prior state")
        if sha(canonical(before)) != event["beforeSHA256"] or sha(canonical(after)) != event["afterSHA256"]:
            raise AssertionError(f"event {event['id']} before/after hash mismatch")
        if after.get("timestampDS", -1) < prior_time:
            raise AssertionError(f"event {event['id']} moves the decisecond clock backward")
        calculated = jsonpatch.JsonPatch(event["forward"]).apply(before, in_place=False)
        if calculated != after:
            raise AssertionError(f"event {event['id']} forward patch mismatch")
        restored = jsonpatch.JsonPatch(event["inverse"]).apply(after, in_place=False)
        if restored != before:
            raise AssertionError(f"event {event['id']} inverse patch mismatch")
        forward_ops += len(event["forward"])
        inverse_ops += len(event["inverse"])
        state = after
        prior_time = after.get("timestampDS", prior_time)
    if state != case["finalState"] or sha(canonical(state)) != case["finalSHA256"]:
        raise AssertionError("final full-state mismatch")
    return len(case["events"]), forward_ops, inverse_ops


def verify() -> dict:
    delivery_raw = DELIVERY.read_bytes()
    delivery = json.loads(delivery_raw.decode("utf-8-sig"))
    archive_size, archive_sha = ARCHIVE.stat().st_size, sha_file(ARCHIVE)
    archive_crc = f"{zlib.crc32(ARCHIVE.read_bytes()) & 0xffffffff:08x}"
    declared_archive = delivery["archive"]
    check(
        "Return190 ZIP matches delivered byte length, SHA-256, and CRC32",
        (archive_size, archive_sha, archive_crc)
        == (declared_archive["bytes"], declared_archive["sha256"], declared_archive["CRC32"].lower())
        == (79_729_568, "821a1bd4896d39e6b325be7a1380e4513c25b30fcbcacbe516bb1c19338c5ae7", "9b69c2a7"),
        {"bytes": archive_size, "sha256": archive_sha, "crc32": archive_crc},
    )
    check(
        "Delivery manifest names the exact return archive and binds the current authority",
        declared_archive["fileName"] == ARCHIVE.name
        and delivery["allMemberHashesAndCRCsMatch"] is True
        and delivery["canonicalAuthorityUnchanged"] == AUTHORITY,
    )
    git_objects = True
    for commit in (SOURCE_COMMIT, PUBLISH_COMMIT):
        try:
            subprocess.check_call(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            git_objects = False
    check("Exact source-anchor and publishing commits exist in the local repository", git_objects)

    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        external_rows = delivery["completeMemberAllowlist"]
        external_map = {row["path"]: row for row in external_rows}
        internal = member_json(archive, "MEMBER_MANIFEST.json")
        internal_rows = internal["members"]
        internal_map = {row["path"]: row for row in internal_rows}
        check(
            "ZIP CRC scan, unique names, and complete member allowlist pass",
            archive.testzip() is None
            and len(names) == len(set(names)) == len(external_rows) == len(external_map) == 242
            and set(external_map) == set(names),
            {"members": len(names), "allowlisted": len(external_rows)},
        )
        unsafe = [
            n for n in names
            if n.startswith(("/", "\\"))
            or ".." in PurePosixPath(n.replace("\\", "/")).parts
            or any(part.startswith(".") for part in n.replace("\\", "/").split("/"))
            or any(token in n.lower() for token in (".tmp", ".temp", "~$"))
        ]
        check("No traversal, hidden, or temporary archive members", not unsafe, unsafe[:20])
        check(
            "Internal member manifest is complete and self-excluding",
            internal["memberCountExcludingThisManifest"] == len(internal_rows) == 241
            and internal["memberCountExcludingThisManifest"] + 1 == len(names)
            and set(internal_map) == set(names) - {"MEMBER_MANIFEST.json"},
        )
        member_errors, internal_errors = [], []
        for name in names:
            digest = hashlib.sha256()
            size = crc = 0
            with archive.open(name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(block)
                    digest.update(block)
                    crc = zlib.crc32(block, crc)
            crc_hex = f"{crc & 0xffffffff:08x}"
            info = archive.getinfo(name)
            row = external_map.get(name, {})
            triple = (size, digest.hexdigest(), crc_hex)
            external_triple = (row.get("bytes"), row.get("sha256"), str(row.get("CRC32", "")).lower())
            if triple != external_triple or info.CRC != (crc & 0xffffffff):
                member_errors.append(name)
            if name != "MEMBER_MANIFEST.json":
                irow = internal_map.get(name, {})
                if triple != (irow.get("bytes"), irow.get("sha256"), str(irow.get("CRC32", "")).lower()):
                    internal_errors.append(name)
        check("All ZIP members independently match SHA-256, length, and CRC32", not member_errors, member_errors[:20])
        check("All payload members match the internal manifest", not internal_errors, internal_errors[:20])

        packet_raw = archive.read("evidence/input/DD_Rank9_AgencyControl9_CurrentSource_189.zip")
        packet_delivery_raw = archive.read("evidence/input/DD_Rank9_AgencyControl9_CurrentSource_189_DELIVERY.json")
        local_packet_delivery_raw = INPUT_DELIVERY.read_bytes()
        source_verification = member_json(archive, "SOURCE_VERIFICATION.json")
        input_zip_decl = source_verification["inputZIP"]
        input_manifest_decl = source_verification["inputDelivery"]
        check(
            "Embedded Return189 input packet and delivery exactly match the published local inputs",
            packet_raw == INPUT_PACKET.read_bytes()
            and packet_delivery_raw == local_packet_delivery_raw
            and len(packet_raw) == input_zip_decl["bytes"]
            and sha(packet_raw) == input_zip_decl["sha256"]
            and len(packet_delivery_raw) == input_manifest_decl["bytes"]
            and sha(packet_delivery_raw) == input_manifest_decl["sha256"],
        )
        with zipfile.ZipFile(io.BytesIO(packet_raw)) as packet:
            packet_names = [n for n in packet.namelist() if n != "MANIFEST.json" and not n.endswith("/")]
            packet_manifest = json.loads(packet.read("MANIFEST.json").decode("utf-8-sig"))
            packet_map = {row["path"]: row for row in packet_manifest["members"]}
            packet_errors = []
            for name in packet_names:
                raw = packet.read(name)
                row = packet_map.get(name, {})
                if (len(raw), sha(raw), f"{zlib.crc32(raw) & 0xffffffff:08x}") != (
                    row.get("bytes"), row.get("sha256"), str(row.get("crc32", "")).lower()
                ):
                    packet_errors.append(name)
            packet_meta = member_json(archive, "evidence/packet189/MANIFEST.json")
            check(
                "Embedded Return189 packet members and manifest bind exactly",
                len(packet_names) == 117
                and len(packet_map) == 117
                and set(packet_names) == set(packet_map)
                and not packet_errors
                and packet_meta["sourceCommit"] == SOURCE_COMMIT
                and packet_meta["sourceAuthority"] == AUTHORITY
                and packet_meta["group"] == "rank9-agency-control9"
                and packet_meta["pendingIds"] == GROUP,
                packet_errors[:20],
            )

        candidate = member_json(archive, "evidence/packet189/CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json")
        candidate_current = candidate.get("currentAuthority")
        source_errors = []
        for binding in candidate.get("sourceBindings", []):
            path = binding["path"]
            raw = archive.read("evidence/packet189/sources_current/" + path)
            expected = git_blob(SOURCE_COMMIT, path)
            if (len(raw), sha(raw), git_blob_id(SOURCE_COMMIT, path)) != (
                binding["bytes"], binding["sha256"], binding["gitBlobSHA1"]
            ) or raw != expected:
                source_errors.append(path)
        check(
            "All 96 refreshed source bindings reproduce exact source-commit Git blobs",
            candidate["currentSourceCommit"] == SOURCE_COMMIT
            and candidate_current == AUTHORITY
            and candidate["currentPendingGroup"]["group"] == "rank9-agency-control9"
            and candidate["currentPendingGroup"]["spellIds"] == GROUP
            and len(candidate.get("sourceBindings", [])) == 96
            and not source_errors,
            source_errors[:20],
        )
        current_names = [n for n in names if n.startswith("evidence/packet189/current/")]
        current_errors = []
        for name in current_names:
            path = name[len("evidence/packet189/current/"):]
            try:
                if archive.read(name) != git_blob(SOURCE_COMMIT, path):
                    current_errors.append(path)
            except subprocess.CalledProcessError:
                current_errors.append(path)
        check("All current-context snapshot files reproduce exact source-commit Git bytes", bool(current_names) and not current_errors, current_errors[:20])

        supplement = member_json(archive, "SOURCE_VERIFICATION.json")["supplementBindings"]
        supplement_errors = []
        for binding in supplement:
            path, commit = binding["path"], binding["sourceCommit"]
            raw = archive.read("evidence/supplement/" + path)
            if (len(raw), sha(raw), git_blob_id(commit, path)) != (
                binding["bytes"], binding["sha256"], binding["gitBlobSHA1"]
            ) or raw != git_blob(commit, path):
                supplement_errors.append(path)
        check("All supplemental evidence bindings reproduce their exact Git source blobs", bool(supplement) and not supplement_errors, supplement_errors[:20])

        evidence = member_json(archive, "EVIDENCE_MANIFEST.json")
        evidence_map = {row["path"]: row for row in evidence["members"]}
        evidence_errors = []
        for name, row in evidence_map.items():
            if name not in names:
                evidence_errors.append(name)
                continue
            raw = archive.read(name)
            triple = (len(raw), sha(raw), f"{zlib.crc32(raw) & 0xffffffff:08x}")
            if triple != (row["bytes"], row["sha256"], row["CRC32"].lower()):
                evidence_errors.append(name)
        check(
            "All source-evidence manifest members bind and source/publishing commits remain distinct",
            len(evidence_map) == 138
            and not evidence_errors
            and evidence["sourceAnchor"] == SOURCE_COMMIT
            and evidence["publishingCommit"] == "039e9730"
            and evidence["executionOfSuppliedSources"] is False
            and source_verification["sourceCommit"] == SOURCE_COMMIT
            and source_verification["publishingCommit"] == "039e9730"
            and source_verification["sourceProgramsExecuted"] is False,
            evidence_errors[:20],
        )

        decision = member_json(archive, "DIRECTOR_DECISION.json")
        delivery_decisions = {row["id"]: row for row in delivery["decisions"]["perIdentity"]}
        decision_rows = {row["id"]: row for row in decision["perIdentity"]}
        procedures_doc = member_json(archive, "PROCEDURES.json")
        procedures = {row["id"]: row for row in procedures_doc["procedures"]}
        check(
            "Director, delivery, and procedure records agree on the exact nine-ID partial decision",
            set(decision_rows) == set(delivery_decisions) == set(procedures) == set(GROUP)
            and decision["acceptedIds"] == delivery["decisions"]["acceptedIds"] == ACCEPTED
            and decision["unacceptedIds"] == delivery["decisions"]["unacceptedIds"] == UNACCEPTED
            and procedures_doc["exactIds"] == GROUP
            and decision["applied"] is False
            and decision["canonicalFilesEdited"] is False
            and decision["allRequestedIdentitiesAccepted"] is False,
        )
        identity_errors = []
        for sid in GROUP:
            accepted = sid in ACCEPTED
            blockers = BLOCKERS.get(sid, [])
            for source, row in (("director", decision_rows[sid]), ("delivery", delivery_decisions[sid]), ("procedure", procedures[sid])):
                if row.get("applied") is not False:
                    identity_errors.append({"spellId": sid, "record": source, "accepted/applied": [row.get("accepted"), row.get("applied")]})
                if source != "procedure" and row.get("blockerIds", []) != blockers:
                    identity_errors.append({"spellId": sid, "record": source, "blockerIds": row.get("blockerIds")})
                if source == "procedure":
                    blocker_ids = {blocker for ids in BLOCKERS.values() for blocker in ids}
                    if (not set(blockers) <= set(row.get("holdIds", []))) or (accepted and blocker_ids & set(row.get("holdIds", []))) or not isinstance(row.get("nativeCardUnchanged"), dict):
                        identity_errors.append({"spellId": sid, "record": source, "scope/blockers": True})
        check("Exactly seven accepted identities and two narrow unaccepted blockers are consistent", not identity_errors, identity_errors)
        hold_register = member_json(archive, "HOLD_REGISTER.json")
        blockers = {row["id"]: row for row in hold_register["holds"] if row.get("id") in {"AG190-B01", "AG190-B02"}}
        blocker_errors = []
        for sid, blocker_id in (("absolute-domination", "AG190-B01"), ("puppetmaster-s-realm", "AG190-B02")):
            drow = blockers.get(blocker_id)
            if not drow or drow.get("blockingForIds") != [sid] or drow.get("status") != "OPEN":
                blocker_errors.append(blocker_id)
        check("Two director blockers remain narrowly scoped and open", not blocker_errors, blocker_errors)
        check(
            "Inherited Ward/Control6 blockers are carried forward without reopening old cohorts",
            member_json(archive, "NEXT_QUEUE_GROUP.json")["carriedForwardBlocked"] == ["nullification-wave", "reality-anchor"]
            and decision["retainedInheritedBlockers"] == ["WC188-B01", "WC188-B02"]
            and hold_register["carryForward"] == ["WC188-B01", "WC188-B02"]
            and decision["canonicalAuthorityUnchanged"] == AUTHORITY,
        )
        check(
            "Authority and canonical-scope claims remain unchanged and unapplied",
            decision["canonicalAuthorityUnchanged"] == AUTHORITY
            and procedures_doc["authorityUnchanged"] == AUTHORITY
            and delivery["canonicalAuthorityUnchanged"] == AUTHORITY
            and decision["runtimeSelectionEnabled"] is False,
        )

        counts = member_json(archive, "COUNTS.json")
        dic = member_json(archive, "DATA_INTEGRITY_CHECK.json")
        validation = member_json(archive, "VALIDATION.json")
        semantic = member_json(archive, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        semantic_assertions = member_json(archive, "SEMANTIC_ASSERTIONS.json")
        expected_counts = {
            "acceptedIds": 7, "branches": 54, "cases": 72, "currentCaseHeldRecords": 4,
            "dataIntegrityChecks": dic["checkCount"], "eventOperations": 7676, "events": 1919,
            "explicitSemanticAssertions": 57, "holdRegisterEntries": 28, "inheritedRegistersPreserved": True,
            "mainCases": 18, "procedures": 9, "proposalOperations": 36, "questions": 34,
            "semanticChecks": 17, "semanticChecksBlocked": 2, "semanticChecksPassed": 15, "unacceptedIds": 2,
        }
        stale_decision_counts = decision["counts"] != counts
        check(
            "Director counts and validation summaries use the final data-check total",
            counts == expected_counts
            and delivery["counts"] == counts
            and decision["counts"] == counts
            and decision["validation"].get("dataChecks") == dic["checkCount"]
            and validation["exactCounts"] == counts
            and validation["dataCheckCount"] == dic["checkCount"]
            and dic["status"] == "PASS"
            and dic["checkCount"] == sum(dic["byCategory"].values())
            and not dic["failures"]
            and semantic["integrityCheckCount"] == dic["checkCount"]
            and not semantic["integrityFailures"]
            and all(row.get("passed") is True for row in semantic_assertions),
            {"COUNTS.dataIntegrityChecks": counts.get("dataIntegrityChecks"), "DIRECTOR_DECISION.counts.dataIntegrityChecks": decision["counts"].get("dataIntegrityChecks"), "DATA_INTEGRITY_CHECK.checkCount": dic["checkCount"], "decisionCountsDiffer": stale_decision_counts},
        )
        check("No runtime, source execution, playtest, balance, cosmology, closure, or release approval is claimed", all(x is False for x in (decision["applied"], decision["canonicalFilesEdited"], decision["runtimeSelectionEnabled"], source_verification["sourceProgramsExecuted"])))

        casebook = member_json(archive, "CASEBOOK.json")
        cases = casebook["cases"]
        case_ids = {case["id"] for case in cases}
        case_files = [name for name in names if name.startswith("cases/") and name.endswith(".json")]
        case_mirror_errors = []
        for case in cases:
            expected_name = "cases/" + case["id"].replace("/", "__") + ".json"
            if expected_name not in names or member_json(archive, expected_name) != case:
                case_mirror_errors.append(case["id"])
        check(
            "All 72 standalone case files mirror the casebook and stay within the nine-ID scope",
            len(cases) == len(case_ids) == len(case_files) == 72
            and all(case["spellId"] in GROUP for case in cases)
            and not case_mirror_errors,
            case_mirror_errors[:20],
        )
        event_ids = set()
        event_total = forward_total = inverse_total = replayed = 0
        replay_errors = []
        for case in cases:
            try:
                for event in case["events"]:
                    if event["id"] in event_ids:
                        raise AssertionError(f"duplicate global event id {event['id']}")
                    event_ids.add(event["id"])
                events, forward_ops, inverse_ops = replay(case)
                replayed += 1
                event_total += events
                forward_total += forward_ops
                inverse_total += inverse_ops
            except Exception as exc:
                replay_errors.append({"caseId": case["id"], "error": f"{type(exc).__name__}: {exc}"})
        check(
            "All cases independently pass full-state forward/inverse and monotone-time replay",
            replayed == 72 and event_total == len(event_ids) == 1919
            and forward_total + inverse_total == 7676
            and not replay_errors,
            {"cases": replayed, "events": event_total, "forwardOperations": forward_total, "inverseOperations": inverse_total, "errors": replay_errors[:10]},
        )
        case_summary = {row["caseId"]: row for row in dic["caseSummary"]}
        summary_errors = []
        for case in cases:
            row = case_summary.get(case["id"], {})
            if row.get("events") != len(case["events"]) or row.get("fullStateReplayed") is not True:
                summary_errors.append(case["id"])
        check("Data-integrity case summary mirrors all replayed cases", len(case_summary) == 72 and not summary_errors, summary_errors[:20])

        question_doc = member_json(archive, "QUESTION_DISPOSITIONS.json")
        question_ids = {row["id"] for row in question_doc["questions"]}
        procedure_question_ids = {row["id"] for proc in procedures.values() for row in proc["questionDispositions"]}
        check(
            "All 34 retained question dispositions map to exactly the reviewed procedures",
            len(question_ids) == 34 and question_ids == procedure_question_ids,
        )

        proposal_rows = member_json(archive, "PROPOSAL_OPERATIONS.json")
        proposal_errors = []
        proposal_operation_count = 0
        for row in proposal_rows:
            try:
                before = row["forward"][0]["value"]
                if sha(canonical(before)) != row["beforeSHA256"]:
                    raise AssertionError("before hash mismatch")
                after = jsonpatch.JsonPatch(row["forward"]).apply(before, in_place=False)
                if sha(canonical(after)) != row["afterSHA256"]:
                    raise AssertionError("after hash mismatch")
                if jsonpatch.JsonPatch(row["inverse"]).apply(after, in_place=False) != before:
                    raise AssertionError("inverse patch mismatch")
                proposal_operation_count += len(row["forward"]) + len(row["inverse"])
            except Exception as exc:
                proposal_errors.append(f"{type(exc).__name__}: {exc}")
        check(
            "All nine proposal records remain unapplied and independently invertible",
            len(proposal_rows) == 9 and proposal_operation_count == 36 and not proposal_errors,
            proposal_errors[:10],
        )
        next_queue = member_json(archive, "NEXT_QUEUE_GROUP.json")
        next_group = next_queue["exactCurrentQueueGroupUnchanged"]
        check(
            "Next queue group is exactly Time/Fate6 at the unchanged 770/78 authority",
            next_queue["applicationPerformed"] is False
            and next_queue["authorityUnchanged"] == AUTHORITY
            and next_group["group"] == "rank9-time-fate6"
            and next_group["pendingIds"] == NEXT_IDS
            and next_group["pendingCount"] == 6
            and next_group["freshPacketRequiredForCurrentAuthority"] is True,
        )

    report = {
        "id": "RANK9-AGENCYCONTROL9-RETURN190-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks),
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": sum(not row["passed"] for row in checks),
        "failures": failures,
        "checks": checks,
        "sourceAnchorCommit": SOURCE_COMMIT,
        "publishingCommit": PUBLISH_COMMIT,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "CRC32": archive_crc, "memberCount": 242},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_raw), "sha256": sha(delivery_raw)},
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "applied": False,
        "blockers": BLOCKERS,
        "canonicalAuthorityStill": AUTHORITY,
        "replay": {"cases": replayed, "events": event_total, "forwardOperations": forward_total, "inverseOperations": inverse_total, "allExactReplaysPass": not replay_errors},
        "nextQueueGroup": {"group": "rank9-time-fate6", "pendingIds": NEXT_IDS, "pendingCount": len(NEXT_IDS)},
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = verify()
    print(json.dumps({key: result[key] for key in ("status", "checkCount", "checksPassed", "checksFailed", "failures", "acceptedIds", "unacceptedIds", "returnArchive", "deliveryManifest", "replay", "nextQueueGroup")}, ensure_ascii=False, indent=2))
