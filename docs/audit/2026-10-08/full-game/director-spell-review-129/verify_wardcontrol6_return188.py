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
RECEIVED = AUDIT / "rank9_wardcontrol6_return188_received"
ARCHIVE = RECEIVED / "DD_Rank9_WardControl6_Director_Return188.zip"
DELIVERY = RECEIVED / "DD_Rank9_WardControl6_Director_Return188_DELIVERY.json"
INPUT_PACKET = AUDIT / "rank9_wardcontrol6_return187_prepared/DD_Rank9_WardControl6_CurrentSource_187.zip"
INPUT_DELIVERY = AUDIT / "rank9_wardcontrol6_return187_prepared/DD_Rank9_WardControl6_CurrentSource_187_DELIVERY.json"
REPORT = AUDIT / "RANK9_WARDCONTROL6_RETURN188_INDEPENDENT_AUDIT.json"
SOURCE_COMMIT = "9624930ad8ac3a06c7e4bda1b84c8a730ae69bd3"
PUBLISH_COMMIT = "1774828baf0f8610437030613d34112f4307efba"
GROUP = [
    "greater-spell-turning",
    "nullification-wave",
    "eternal-ward",
    "ultimate-ward",
    "reality-anchor",
    "prismatic-sphere",
]
ACCEPTED = ["greater-spell-turning", "eternal-ward", "ultimate-ward", "prismatic-sphere"]
UNACCEPTED = ["nullification-wave", "reality-anchor"]
BLOCKERS = {
    "nullification-wave": ["WC188-B01"],
    "reality-anchor": ["WC188-B02"],
}
NEXT_IDS = [
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

checks: list[dict] = []
failures: list[str] = []


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


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
    prior_time = state.get("tDS", -1)
    forward_ops = inverse_ops = 0
    seen_ids = set()
    for event in case["events"]:
        if event["id"] in seen_ids:
            raise AssertionError(f"duplicate event id {event['id']}")
        seen_ids.add(event["id"])
        before = event["before"]
        after = event["after"]
        if state != before or sha(canonical(before)) != event["beforeSHA256"] or sha(canonical(after)) != event["afterSHA256"]:
            raise AssertionError(f"event {event.get('id')} before/after state hash mismatch")
        event_time = event["timeDS"]
        if event_time < prior_time:
            raise AssertionError(f"event {event.get('id')} moves the clock backward")
        calculated = jsonpatch.JsonPatch(event["forward"]).apply(before, in_place=False)
        if calculated != after:
            raise AssertionError(f"event {event.get('id')} forward patch mismatch")
        restored = jsonpatch.JsonPatch(event["inverse"]).apply(after, in_place=False)
        if restored != before:
            raise AssertionError(f"event {event.get('id')} inverse patch mismatch")
        forward_ops += len(event["forward"])
        inverse_ops += len(event["inverse"])
        state = after
        prior_time = event_time
    if state != case["finalState"] or sha(canonical(state)) != case["finalSHA256"]:
        raise AssertionError("final state mismatch")
    return len(case["events"]), forward_ops, inverse_ops


def verify() -> dict:
    delivery_raw = DELIVERY.read_bytes()
    delivery = json.loads(delivery_raw.decode("utf-8-sig"))
    archive_size = ARCHIVE.stat().st_size
    archive_sha = sha_file(ARCHIVE)
    delivery_sha = sha(delivery_raw)
    check(
        "Downloaded Return188 ZIP matches the director delivery size and SHA-256",
        archive_size == delivery["bytes"] == 141_721_055
        and archive_sha == delivery["sha256"] == "93e609e4a11b428cbb99de7da42dded65879274ebdc50c7a8696b137c576c190",
        {"bytes": archive_size, "sha256": archive_sha},
    )
    check(
        "Downloaded delivery JSON is present and independently hashed",
        delivery_sha == "af6a86f32579eb66958ce8ddc3b27977e543bffc6a2c01e9a4c24c73d0f0907a"
        and delivery["filename"] == ARCHIVE.name
        and delivery["memberCount"] == 229,
        {"bytes": len(delivery_raw), "sha256": delivery_sha},
    )
    check(
        "Return188 binds the exact current-source and publishing commits",
        delivery["sourcePacket"]["sha256"] == "16ee2936c8be8b20a5ba700de7955880e229b95a468607575c907edaba7139eb"
        and delivery["sourcePacket"]["deliverySHA256"] == "c801a031e8988d2b49d08b9d04e0ce77473b2f9c64ea7f68b2ecb89eb6b74757",
    )

    git_objects_exist = True
    for commit in (SOURCE_COMMIT, PUBLISH_COMMIT):
        try:
            subprocess.check_call(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            git_objects_exist = False
    check("Exact source-anchor and publishing commits exist locally", git_objects_exist)

    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        check("Return188 ZIP CRC scan passes and member names are unique", archive.testzip() is None and len(names) == len(set(names)) == 229, {"members": len(names)})
        unsafe = [
            name for name in names
            if name.startswith(("/", "\\"))
            or ".." in PurePosixPath(name.replace("\\", "/")).parts
            or any(part.startswith(".") for part in name.replace("\\", "/").split("/"))
            or any(token in name.lower() for token in (".tmp", ".temp", "~$"))
        ]
        check("Return188 has no traversal, hidden, or temporary members", not unsafe, unsafe[:20])

        external_rows = delivery["completeArchiveMemberBindings"]
        external_map = {row["path"]: row for row in external_rows}
        internal = member_json(archive, "MEMBER_MANIFEST.json")
        internal_rows = internal["members"]
        internal_map = {row["path"]: row for row in internal_rows}
        check(
            "Internal manifest is exact and self-excluding",
            internal["totalArchiveMemberCount"] == len(names) == 229
            and internal["memberCountExcludingSelf"] == len(internal_rows) == 228
            and set(internal_map) == set(names) - {"MEMBER_MANIFEST.json"},
        )
        check(
            "Delivery manifest binds the full ZIP and every unique member",
            len(external_rows) == len(external_map) == len(names) == delivery["memberCount"]
            and set(external_map) == set(names)
            and delivery["memberManifest"] == next(row for row in external_rows if row["path"] == "MEMBER_MANIFEST.json"),
        )
        member_errors = []
        internal_errors = []
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
            if (size, digest.hexdigest(), crc_hex) != (
                row.get("bytes"), row.get("sha256"), str(row.get("crc32", "")).lower()
            ) or info.CRC != (crc & 0xffffffff):
                member_errors.append(name)
            if name != "MEMBER_MANIFEST.json":
                irow = internal_map.get(name, {})
                if (size, digest.hexdigest(), crc_hex) != (
                    irow.get("bytes"), irow.get("sha256"), str(irow.get("crc32", "")).lower()
                ):
                    internal_errors.append(name)
        check("All 229 members match independent size/SHA-256/CRC checks and the delivery bindings", not member_errors, member_errors[:20])
        check("All 228 payload members match the internal manifest", not internal_errors, internal_errors[:20])

        input_packet_raw = archive.read("inputs/DD_Rank9_WardControl6_CurrentSource_187.zip")
        input_delivery_raw = archive.read("inputs/DD_Rank9_WardControl6_CurrentSource_187_DELIVERY.json")
        check(
            "Embedded input packet and manifest match the locally prepared 187 packet byte-for-byte",
            len(input_packet_raw) == INPUT_PACKET.stat().st_size
            and input_packet_raw == INPUT_PACKET.read_bytes()
            and sha(input_packet_raw) == delivery["sourcePacket"]["sha256"]
            and input_delivery_raw == INPUT_DELIVERY.read_bytes()
            and sha(input_delivery_raw) == delivery["sourcePacket"]["deliverySHA256"],
        )

        with zipfile.ZipFile(io.BytesIO(input_packet_raw)) as packet:
            packet_names = [name for name in packet.namelist() if not name.endswith("/")]
            packet_manifest = json.loads(packet.read("MANIFEST.json").decode("utf-8-sig"))
            reconstructed_errors = []
            for name in packet_names:
                outer_name = "packet187/" + name
                if outer_name not in names or archive.read(outer_name) != packet.read(name):
                    reconstructed_errors.append(name)
            check(
                "All original current-source packet members are preserved exactly under packet187/",
                len(packet_names) == 113 and not reconstructed_errors and packet_manifest["sourceCommit"] == SOURCE_COMMIT,
                reconstructed_errors[:20],
            )

        candidate = member_json(archive, "packet187/CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json")
        check(
            "Current-source candidate binds the exact source anchor and queue state",
            candidate["currentSourceCommit"] == SOURCE_COMMIT
            and candidate["currentAuthority"] == {
                "reviewedApplied": 766,
                "pending": 82,
                "acceptedUnapplied": 0,
                "completeStandaloneProcedures": 490,
                "scopedInterfaces": 173,
            }
            and candidate["currentPendingGroup"]["group"] == "rank9-ward-control6"
            and candidate["currentPendingGroup"]["spellIds"] == GROUP,
        )
        source_errors = []
        for binding in candidate["sourceBindings"]:
            path = binding["path"]
            raw = archive.read("packet187/sources_current/" + path)
            expected = git_blob(SOURCE_COMMIT, path)
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"] or raw != expected or git_blob_id(SOURCE_COMMIT, path) != binding["gitBlobSHA1"]:
                source_errors.append(path)
        check("All 91 refreshed source bindings reproduce exact Git bytes and blob IDs", len(candidate["sourceBindings"]) == 91 and not source_errors, source_errors[:20])

        current_errors = []
        current_names = [name for name in names if name.startswith("packet187/current/")]
        for name in current_names:
            path = name[len("packet187/current/"):]
            try:
                expected = git_blob(SOURCE_COMMIT, path)
            except subprocess.CalledProcessError:
                current_errors.append(path)
                continue
            if archive.read(name) != expected:
                current_errors.append(path)
        check("All 15 current context snapshots reproduce exact Git bytes", len(current_names) == 15 and not current_errors, current_errors[:20])

        source_check = member_json(archive, "SOURCE_CHECK.json")
        supplement_errors = []
        for binding in source_check["supplementBindings"]:
            path = binding["path"]
            member = "supplement/" + path
            raw = archive.read(member)
            expected = git_blob(binding["sourceCommit"], path)
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"] or raw != expected or git_blob_id(binding["sourceCommit"], path) != binding["gitBlob"]:
                supplement_errors.append(path)
        check(
            "All supplemental source records reproduce their exact Git blobs",
            len(source_check["supplementBindings"]) == 23 and not supplement_errors,
            supplement_errors[:20],
        )

        evidence = member_json(archive, "EVIDENCE_MANIFEST.json")
        evidence_errors = []
        evidence_map = {row["path"]: row for row in evidence["sourceEvidenceMembers"]}
        if len(evidence_map) != len(evidence["sourceEvidenceMembers"]) != 136:
            evidence_errors.append("duplicate or unexpected evidence member count")
        for name, row in evidence_map.items():
            if name not in names:
                evidence_errors.append(name)
                continue
            raw = archive.read(name)
            crc = f"{zlib.crc32(raw) & 0xffffffff:08x}"
            if (len(raw), sha(raw), crc) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                evidence_errors.append(name)
        check("All source-evidence manifest entries bind exact archive members", len(evidence_map) == evidence["count"] == 136 and not evidence_errors, evidence_errors[:20])
        check(
            "Source and publishing labels remain separate and canonical files are unchanged",
            evidence["sourceCommit"] == SOURCE_COMMIT
            and evidence["publishingCommit"] == PUBLISH_COMMIT
            and evidence["canonicalMutation"] is False
            and source_check["sourceAnchorCommit"] == SOURCE_COMMIT
            and source_check["publishingCommit"] == PUBLISH_COMMIT
            and source_check["canonicalFilesChanged"] is False,
        )

        decision = member_json(archive, "DIRECTOR_DECISION.json")
        semantic = member_json(archive, "SEMANTIC_FAILURE_CHECK.json")
        procedures_doc = member_json(archive, "PROCEDURES.json")
        delivery_decisions = {row["id"]: row for row in delivery["perIdentityDecisions"]}
        decision_rows = {row["spellId"]: row for row in decision["decisions"]}
        procedure_rows = {row["id"]: row for row in procedures_doc["procedures"]}
        check(
            "Director, delivery, and semantic check agree on the six per-identity rulings",
            set(decision_rows) == set(delivery_decisions) == set(procedure_rows) == set(GROUP)
            and decision["accepted"] is False
            and decision["acceptedIds"] == ACCEPTED
            and decision["unacceptedIds"] == UNACCEPTED
            and decision["applied"] is False
            and decision["canonicalFilesChanged"] is False
            and semantic["acceptedIds"] == ACCEPTED
            and semantic["unacceptedIds"] == UNACCEPTED
            and semantic["applied"] is False
            and semantic["assertionFailures"] == 0,
        )
        identity_errors = []
        for sid in GROUP:
            drow = decision_rows[sid]
            vrow = delivery_decisions[sid]
            prow = procedure_rows[sid]
            expected_accepted = sid in ACCEPTED
            expected_blockers = BLOCKERS.get(sid, [])
            if (drow["accepted"], drow["applied"], drow["blockerIds"]) != (expected_accepted, False, expected_blockers):
                identity_errors.append({"spellId": sid, "where": "decision"})
            if (vrow["accepted"], vrow["applied"], vrow["blockerIds"]) != (expected_accepted, False, expected_blockers):
                identity_errors.append({"spellId": sid, "where": "delivery"})
            if (prow["accepted"], prow["applied"], prow["blockerIds"]) != (expected_accepted, False, expected_blockers):
                identity_errors.append({"spellId": sid, "where": "procedure"})
            if not prow["nativeCardUnchanged"] or prow["runtimeSelectionEnabled"] is not False or not prow["currentIndexEntryUnchanged"]:
                identity_errors.append({"spellId": sid, "where": "scope/native"})
        check("Exact four acceptances/two narrow holds and static-only/native-card scope agree", not identity_errors, identity_errors)

        blocker_rows = {row["id"]: row for row in decision["blockers"]}
        check(
            "Both retained blockers are exact and narrowly scoped",
            set(blocker_rows) == {"WC188-B01", "WC188-B02"}
            and blocker_rows["WC188-B01"]["spellIds"] == ["nullification-wave"]
            and blocker_rows["WC188-B02"]["spellIds"] == ["reality-anchor"]
            and all(row["status"] == "BLOCKING_SOURCE_EVIDENCE_GAP" and row["notClaimed"] for row in blocker_rows.values()),
        )
        check(
            "Canonical authority remains 766/82/0 with 490 procedures and 173 interfaces",
            delivery["canonicalAuthorityUnchanged"] == {
                "reviewedApplied": 766, "pending": 82, "acceptedUnapplied": 0,
                "standaloneProcedures": 490, "scopedInterfaces": 173,
            }
            and decision["authorityBeforeAndStillCanonical"] == delivery["canonicalAuthorityUnchanged"],
        )

        data_check = member_json(archive, "DATA_INTEGRITY_CHECK.json")
        doc_check = member_json(archive, "FINAL_DOCUMENT_CHECK.json")
        counts = member_json(archive, "CASE_COUNTS.json")
        check(
            "Director reports zero failures in semantic, data, and final document checks",
            semantic["checkCount"] == 248
            and all(row["passed"] for row in semantic["checks"])
            and data_check["totalChecks"] == 167_085
            and data_check["failureCount"] == 0
            and not data_check["failures"]
            and doc_check["checkCount"] == 925
            and doc_check["failureCount"] == 0
            and not doc_check["failures"],
        )
        check(
            "Reported case/event/operation counts match the required six-spell scope",
            counts == {
                "branchCases": 48, "cases": 60, "events": 5_182, "focusedQuestions": 2,
                "forwardOperations": 10_364, "heldNoPositiveCases": 6, "inverseOperations": 10_364,
                "mainCases": 12, "originalQuestions": 24, "procedures": 6, "questions": 26,
            },
        )

        casebook = member_json(archive, "CASEBOOK.json")
        cases = casebook["cases"]
        case_map = {row["id"]: row for row in cases}
        index_rows = {row["id"]: row for row in data_check["caseIndex"]}
        case_errors = []
        event_ids = set()
        event_total = forward_total = inverse_total = replayed_cases = 0
        replay_errors = []
        for case in cases:
            cid = case["id"]
            index = index_rows.get(cid)
            if not index or index["spellId"] != case["spellId"] or index["status"] != case["status"] or index["events"] != len(case["events"]):
                case_errors.append({"caseId": cid, "where": "index mirror"})
            if case["spellId"] not in GROUP or case["status"] not in {"AUTHORED_STATIC_TRACE", "HELD_NO_POSITIVE_CLAIM"}:
                case_errors.append({"caseId": cid, "where": "scope/status"})
            for event in case["events"]:
                if event["id"] in event_ids:
                    case_errors.append({"caseId": cid, "eventId": event["id"], "where": "duplicate global event"})
                event_ids.add(event["id"])
            try:
                events, forward_ops, inverse_ops = replay(case)
                event_total += events
                forward_total += forward_ops
                inverse_total += inverse_ops
                replayed_cases += 1
            except Exception as exc:
                replay_errors.append({"caseId": cid, "error": f"{type(exc).__name__}: {exc}"})
        check(
            "All 60 casebook rows mirror the case index and stay within the six requested identities",
            len(cases) == len(case_map) == len(index_rows) == 60 and not case_errors,
            case_errors[:20],
        )
        check(
            "All 5,182 event states pass independent forward/inverse and monotone-clock replay",
            not replay_errors and len(event_ids) == event_total == 5_182
            and replayed_cases == 60
            and forward_total == inverse_total == 10_364,
            {"cases": replayed_cases, "events": event_total, "forwardOperations": forward_total,
             "inverseOperations": inverse_total, "errors": replay_errors[:10]},
        )

        accepted_case_errors = []
        for sid in ACCEPTED:
            drow = decision_rows[sid]
            for cid in drow["caseIds"]:
                case = case_map.get(cid)
                idx = index_rows.get(cid)
                if not case or case["spellId"] != sid or not idx:
                    accepted_case_errors.append({"spellId": sid, "caseId": cid})
                elif set(case["holdIds"]) & {"WC188-B01", "WC188-B02"} or set(idx["holdIds"]) & {"WC188-B01", "WC188-B02"}:
                    accepted_case_errors.append({"spellId": sid, "caseId": cid, "where": "identity blocker leaked into an accepted case"})
        check("Every accepted case is present, source-scoped, replayed, and has no blocking hold", not accepted_case_errors, accepted_case_errors[:20])

        proposal = member_json(archive, "PROPOSAL_OPERATIONS.json")
        proposal_state = proposal["initialState"]
        proposal_operation_errors = []
        proposal_ops = inverse_ops = 0
        for row in proposal["operations"]:
            before = proposal_state
            after = jsonpatch.JsonPatch(row["forward"]).apply(before, in_place=False)
            restored = jsonpatch.JsonPatch(row["inverse"]).apply(after, in_place=False)
            if restored != before:
                proposal_operation_errors.append(row["id"])
            proposal_state = after
            proposal_ops += len(row["forward"])
            inverse_ops += len(row["inverse"])
        check(
            "Noncanonical proposal operations have exact inverse patches and remain unapplied",
            proposal["applied"] is False
            and proposal["operationCount"] == proposal_ops + inverse_ops == 24
            and proposal_ops == inverse_ops
            and len(proposal["operations"]) == 6
            and not proposal_operation_errors,
            proposal_operation_errors,
        )

        next_group = member_json(archive, "NEXT_QUEUE_GROUP.json")
        check(
            "Next queue group is exactly the current nine-identity Agency/Control cohort",
            next_group["group"] == "rank9-agency-control9"
            and next_group["pendingCount"] == 9
            and next_group["pendingIds"] == NEXT_IDS
            and next_group["freshPacketRequiredForCurrentAuthority"] is True,
        )
        check(
            "Runtime, human-play, balance, cosmology, closure, and release approval remain explicitly out of scope",
            delivery["qualifications"]
            and delivery["canonicalAuthorityUnchanged"]["acceptedUnapplied"] == 0
            and casebook["runtimeExecuted"] is False
            and casebook["historicalProgramsExecuted"] is False
            and data_check["runtimeExecuted"] is False
            and data_check["historicalProgramsExecuted"] is False,
        )

    report = {
        "id": "RANK9-WARDCONTROL6-RETURN188-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks),
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": sum(not row["passed"] for row in checks),
        "failures": failures,
        "checks": checks,
        "sourceAnchorCommit": SOURCE_COMMIT,
        "publishingCommit": PUBLISH_COMMIT,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "memberCount": 229},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_raw), "sha256": delivery_sha},
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "applied": False,
        "blockers": BLOCKERS,
        "canonicalAuthorityStill": {"reviewedApplied": 766, "pending": 82, "acceptedUnapplied": 0, "completeStandaloneProcedures": 490, "scopedInterfaces": 173},
        "replay": {"cases": replayed_cases, "events": event_total, "forwardOperations": forward_total, "inverseOperations": inverse_total, "allExactReplaysPass": not replay_errors},
        "nextQueueGroup": {"group": "rank9-agency-control9", "pendingIds": NEXT_IDS, "pendingCount": 9},
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = verify()
    print(json.dumps({key: result[key] for key in ("status", "checkCount", "checksPassed", "checksFailed", "failures", "acceptedIds", "unacceptedIds", "returnArchive", "deliveryManifest", "replay", "nextQueueGroup")}, ensure_ascii=False, indent=2))
