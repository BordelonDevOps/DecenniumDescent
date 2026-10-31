from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_projectionconfinement2_return288_received"
ARCHIVE = RECEIVED / "DD_Rank9_ProjectionConfinement2_Director_Return288_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_ProjectionConfinement2_Director_Return288_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_projectionconfinement2_current_source_288_prepared"
SOURCE_PACKET = SOURCE_DIR / "DD_Rank9_ProjectionConfinement2_CurrentSource_288.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_ProjectionConfinement2_CurrentSource_288_DELIVERY.json"
PACKET_AUDIT = BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_INDEPENDENT_AUDIT.json"
PACKET_RECEIPT = BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_RECEIPT.json"
PACKET_SUBMISSION = BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_SUBMISSION.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_288.json"
REPORT = BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN288_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN288_RECEIPT.json"

AUTH = {
    "reviewedApplied": 816,
    "pending": 32,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 540,
    "scopedInterfaces": 173,
}
TARGETS = ["astral-projection", "imprisonment"]
BLOCKERS = {"astral-projection": ["PC232-B01"], "imprisonment": ["PC232-B02"]}
NEXT = {"group": "rank9-miracle-reality2", "pendingIds": ["divine-intervention-greater", "wish"]}
EXPECTED_ARCHIVE = {
    "bytes": 2248706,
    "sha256": "5bae4c955f92b73a1544922ac0a6188076411a2dce10db26be6cc41d64378f98",
    "crc32": "ba30c2f0",
}
EXPECTED_DELIVERY = {
    "bytes": 89110,
    "sha256": "d02ce6bcbf1f3a2bf55f207db374cf6242e31f1d7fa8e257730665f359b6b284",
    "crc32": "225a6d92",
}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def sha_matches(raw: bytes, row: dict) -> bool:
    actual = digest(raw)
    return all(actual.get(k) == row.get(k) for k in ("bytes", "sha256")) and (
        row.get("crc32") is None or actual["crc32"].lower() == str(row["crc32"]).lower()
    )


def readj(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def readm(archive: zipfile.ZipFile, member: str):
    return json.loads(archive.read(member).decode("utf-8-sig"))


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and ".." not in p.parts and ":" not in p.parts[0]


def ids(items) -> list[str]:
    return [x.get("id") for x in items if isinstance(x, dict) and x.get("id")]


def main() -> None:
    checks: list[dict] = []

    def check(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    delivery_raw = DELIVERY.read_bytes()
    archive_raw = ARCHIVE.read_bytes()
    d = json.loads(delivery_raw.decode("utf-8-sig"))
    archive_digest = digest(archive_raw)
    delivery_digest = digest(delivery_raw)
    check("Return288 archive matches the exact Director-reported size, SHA-256 and CRC32", archive_digest == EXPECTED_ARCHIVE and sha_matches(archive_raw, d.get("archive", {})), archive_digest)
    check("Return288 DELIVERY matches its downloaded size, SHA-256 and CRC32", delivery_digest == EXPECTED_DELIVERY, delivery_digest)
    check("Delivery names the received archive and reports the sealed 120-member package", Path(d.get("archive", {}).get("path", "")).name == ARCHIVE.name and d.get("zipMemberCount") == 120 and d.get("payloadMemberCount") == 119, {"archive": d.get("archive"), "members": d.get("zipMemberCount"), "payloads": d.get("payloadMemberCount")})
    check("Outer delivery preserves current authority and no acceptance or application", d.get("authority") == AUTH and d.get("acceptedIds") == [] and d.get("appliedIds") == [] and d.get("heldIds") == TARGETS and d.get("canonicalChanges") is False and d.get("runtimeExecuted") is False, {"authority": d.get("authority"), "acceptedIds": d.get("acceptedIds"), "appliedIds": d.get("appliedIds"), "heldIds": d.get("heldIds")})

    prior232_path = BASE / "rank9_projectionconfinement2_return232_received/DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip"
    prior232_delivery_path = BASE / "rank9_projectionconfinement2_return232_received/DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json"
    correction_dir = BASE / "rank9_projectionconfinement2_packet288_history_correction"
    correction_zip = correction_dir / "DD_Rank9_ProjectionConfinement2_Packet288_HistoryCorrection.zip"
    external_paths = {
        "DD_Rank9_ProjectionConfinement2_CurrentSource_288.zip": SOURCE_PACKET,
        "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip": prior232_path,
        "DD_Rank9_ProjectionConfinement2_Packet288_HistoryCorrection.zip": correction_zip,
    }
    external_failures = []
    for row in d.get("externalArchives", []):
        path = external_paths.get(row.get("filename"))
        if path is None or not path.is_file() or not sha_matches(path.read_bytes(), row):
            external_failures.append(row.get("filename"))
    check("Three external evidence archives match their exact sealed byte bindings", len(d.get("externalArchives", [])) == 3 and not external_failures, external_failures)

    packet_record = readj(BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288.json")
    packet_audit = readj(PACKET_AUDIT)
    packet_receipt = readj(PACKET_RECEIPT)
    packet_submission = readj(PACKET_SUBMISSION)
    source_delivery = readj(SOURCE_DELIVERY)
    source_raw = SOURCE_PACKET.read_bytes()
    check("Packet288 submitted source is independently audited and bound byte-exactly", packet_audit.get("status") == "PASS" and packet_audit.get("checkCount") == 15 and packet_receipt.get("status") == "PASS" and packet_record.get("archive", {}).get("sha256") == d.get("sourcePacketSHA256") == digest(source_raw)["sha256"] == source_delivery.get("archive", {}).get("sha256") and packet_submission.get("status") == "PACKET288_SUBMITTED_GPT_PENDING_816_32_0" and packet_submission.get("targetIds") == TARGETS, {"packetAudit": packet_audit.get("status"), "checks": packet_audit.get("checkCount"), "sourceSha256": digest(source_raw)["sha256"], "submission": packet_submission.get("status")})

    with zipfile.ZipFile(ARCHIVE) as z, zipfile.ZipFile(SOURCE_PACKET) as source:
        names = z.namelist()
        name_set = set(names)
        bad_paths = [n for n in names if not safe_member(n)]
        check("Return288 archive has 120 unique safe paths and passes ZIP CRC validation", len(names) == len(name_set) == 120 and not bad_paths and z.testzip() is None, {"members": len(names), "unsafe": bad_paths[:10]})

        external_rows = d.get("members", [])
        external_by_path = {x.get("path"): x for x in external_rows if isinstance(x, dict)}
        internal_manifest_raw = z.read("MEMBER_MANIFEST.json")
        internal_manifest = json.loads(internal_manifest_raw.decode("utf-8-sig"))
        internal_rows = internal_manifest.get("members", [])
        internal_by_path = {x.get("path"): x for x in internal_rows if isinstance(x, dict)}
        payload_names = name_set - {"MEMBER_MANIFEST.json"}
        check("Delivery allowlist and embedded manifest cover the exact ZIP member set", len(external_by_path) == len(external_rows) == 120 and set(external_by_path) == name_set and len(internal_by_path) == len(internal_rows) == 119 and set(internal_by_path) == payload_names and sha_matches(internal_manifest_raw, d.get("memberManifest", {})), {"external": len(external_by_path), "internal": len(internal_by_path)})
        bad_external = [n for n, row in external_by_path.items() if not sha_matches(z.read(n), row)]
        bad_internal = [n for n, row in internal_by_path.items() if not sha_matches(z.read(n), row)]
        check("Every ZIP member matches the external and internal size/SHA/CRC manifests", not bad_external and not bad_internal, {"externalFailures": bad_external[:10], "internalFailures": bad_internal[:10]})

        decision = readm(z, "DIRECTOR_DECISION.json")
        authority = readm(z, "CURRENT_AUTHORITY.json")
        counts = readm(z, "COUNTS.json")
        hold = readm(z, "HOLD_REGISTER.json")
        procedure_rows = readm(z, "PROCEDURES.json")
        decisions = decision.get("perIdentityDecisions", [])
        decision_by_id = {x.get("id"): x for x in decisions}
        check("Sealed Director ruling holds exactly both submitted identities under PC232-B01/B02", set(decision_by_id) == set(TARGETS) and all(decision_by_id[s].get("decision") == "HOLD" and decision_by_id[s].get("held") is True and decision_by_id[s].get("accepted") is False and decision_by_id[s].get("applied") is False and decision_by_id[s].get("blockerIds") == BLOCKERS[s] for s in TARGETS) and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("heldIds") == TARGETS, {s: decision_by_id.get(s, {}).get("blockerIds") for s in TARGETS})
        check("Decision, current-authority payload and delivery all match 816/32/0 with no side effects", decision.get("authority") == AUTH and decision.get("authorityAfter") == AUTH and authority.get("authority") == AUTH and authority.get("acceptedIds") == [] and authority.get("appliedIds") == [] and authority.get("heldIds") == TARGETS and authority.get("canonicalChanges") is False and decision.get("canonicalChanges") is False and decision.get("githubChanges") is False and decision.get("runtimeExecuted") is False and decision.get("sourceProgramsExecuted") is False, {"authority": authority.get("authority"), "canonicalChanges": decision.get("canonicalChanges"), "githubChanges": decision.get("githubChanges"), "runtimeExecuted": decision.get("runtimeExecuted")})
        blockers = hold.get("targetBlockers", [])
        blocker_by_id = {x.get("id"): x for x in blockers}
        check("Open blocker register and procedure mirror preserve PC232-B01/B02 as incomplete", set(blocker_by_id) == {"PC232-B01", "PC232-B02"} and all(blocker_by_id[b].get("spellId") == s and blocker_by_id[b].get("status") == "OPEN" and blocker_by_id[b].get("decision") == "held" and blocker_by_id[b].get("accepted") is False and blocker_by_id[b].get("applied") is False for s, ids_ in BLOCKERS.items() for b in ids_) and {x.get("id") for x in procedure_rows} == set(TARGETS) and all(x.get("held") is True and x.get("completeOperationalProcedure") is False and x.get("blockerIds") == BLOCKERS[x["id"]] for x in procedure_rows), {"blockers": sorted(blocker_by_id), "procedures": len(procedure_rows)})
        expected_qualifications = [f"PC232-Q{i:02d}" for i in range(1, 8)]
        check("Both held identities retain the seven qualified scope limitations", all(decision_by_id[s].get("qualificationIds") == expected_qualifications for s in TARGETS) and len(readm(z, "QUALIFICATIONS.json")) == 7, expected_qualifications)

        original_questions = readm(z, "ORIGINAL_QUESTIONS.json")
        focused = readm(z, "FOCUSED_ADDITIONS.json")
        qdisp = readm(z, "QUESTION_DISPOSITIONS.json")
        qids = set(ids(original_questions)) | set(ids(focused))
        qdids = ids(qdisp)
        check("All 24 original questions and two focused additions have one disposition each", len(original_questions) == 24 and len(focused) == 2 and len(qdisp) == 26 and len(set(qdids)) == 26 and set(qdids) == qids and counts.get("questionDispositions") == 26, {"original": len(original_questions), "focused": len(focused), "dispositions": len(qdisp)})

        main_cases = readm(z, "MAIN_CASE_DISPOSITIONS.json")
        obligations = readm(z, "ORIGINAL_MAIN_CASE_OBLIGATIONS.json")
        check("All four required main cases remain held without complete spell or actor-clock witnesses", len(main_cases) == len(obligations) == 4 and {x.get("id") for x in main_cases} == set(ids(obligations)) and all(x.get("status") == "HELD-NOT-DEMONSTRATED" and x.get("accepted") is False and x.get("applied") is False and x.get("completeSpellWitness") is False and x.get("actorClockComplete") is False for x in main_cases) and counts.get("heldMainCases") == 4 and counts.get("completeMainCases") == 0, {"cases": len(main_cases), "held": counts.get("heldMainCases"), "complete": counts.get("completeMainCases")})
        future = readm(z, "FUTURE_CASE_DISPOSITIONS.json")
        future_statuses = [x.get("status") for x in future]
        check("All eight future requirements are dispositioned with no positive completion witness", len(future) == 8 and sum(x == "HELD-NOT-DEMONSTRATED" for x in future_statuses) == 7 and sum(x == "EVIDENCE_BOUNDARY_OBSERVED" for x in future_statuses) == 1 and all(x.get("completePositiveWitness") is False for x in future) and counts.get("futureRequirements") == 8 and counts.get("completePositiveFutureWitnesses") == 0, {"future": len(future), "statuses": future_statuses})

        replay = readm(z, "REPLAY_RESULTS.json")
        replay_cases = replay.get("cases", [])
        check("Eight preserved audit traces pass with 8 events and 16 forward/inverse operations", len(replay_cases) == 8 and all(x.get("passed") is True and x.get("completeSpellWitness") is False and x.get("completeActorClockWitness") is not True for x in replay_cases) and sum(x.get("events", 0) for x in replay_cases) == replay.get("auditEvents") == 8 and replay.get("gameplayEvents") == 0 and sum(x.get("forwardOperations", 0) for x in replay_cases) == replay.get("forwardOperations") == 16 and sum(x.get("inverseOperations", 0) for x in replay_cases) == replay.get("inverseOperations") == 16 and replay.get("fullReverseTraversals") == 8 and counts.get("preservedAuditComponentCases") == 8, {k: replay.get(k) for k in ["auditEvents", "gameplayEvents", "forwardOperations", "inverseOperations", "fullReverseTraversals"]})
        clock = readm(z, "CLOCK_CHECK.json")
        check("Clock check explicitly leaves complete actor-clock witnesses absent", clock.get("status") == "NOT_DEMONSTRATED_FOR_MAIN_CASES" and clock.get("completeActorClockCases") == 0 and counts.get("completeActorClockCases") == 0 and counts.get("gameplayEvents") == 0, clock)

        # Bind all 135 current files to the audited Packet288 and the live tree.
        source_bindings = readm(z, "SOURCE_BINDINGS.json")
        binding_rows = source_bindings.get("currentSourceFiles", [])
        source_names = set(source.namelist())
        candidate = readm(source, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_288.json")
        candidate_rows = candidate.get("sourceBindings", [])
        source_failures = []
        for row in binding_rows:
            path = row.get("path", "")
            member = "sources_current/" + path
            if member not in source_names:
                source_failures.append(path + " missing from Packet288")
                continue
            raw = source.read(member)
            if not sha_matches(raw, row) or (row.get("gitBlobSHA1") and git_blob_sha(raw) != row.get("gitBlobSHA1")):
                source_failures.append(path + " packet bytes")
            live = ROOT / Path(*PurePosixPath(path).parts)
            if not live.is_file() or not sha_matches(live.read_bytes(), row):
                source_failures.append(path + " live bytes")
        candidate_by_path = {x.get("path"): x for x in candidate_rows if isinstance(x, dict)}
        if len(candidate_by_path) != len(candidate_rows) or set(candidate_by_path) != {x.get("path") for x in binding_rows}:
            source_failures.append("candidate source binding path set")
        else:
            for row in binding_rows:
                c = candidate_by_path[row["path"]]
                if any(c.get(k) != row.get(k) for k in ("path", "bytes", "sha256", "gitBlobSHA1")):
                    source_failures.append(row["path"] + " candidate binding")
        check("All 135 current source bindings match Packet288, Git blob IDs and the live tree", len(binding_rows) == 135 and not source_failures and source_bindings.get("programsExecuted") is False and source_bindings.get("currentAuthority") == AUTH, {"bindings": len(binding_rows), "failures": source_failures[:12]})
        comparison = readm(z, "SOURCE_COMPARISON_232_TO_288.json")
        changed_paths = [x.get("path") for x in comparison.get("rows", []) if x.get("rawByteIdentical") is False]
        check("Source delta from Return232 is exactly 134 unchanged files plus the authored review index", comparison.get("unchanged") == 134 and len(comparison.get("rows", [])) == 135 and changed_paths == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"] and counts.get("currentSourceBindings") == 135, {"unchanged": comparison.get("unchanged"), "changed": changed_paths})

        # Validate the prior ruling, its correction supplement and preserved evidence.
        workflow = readm(z, "WORKFLOW_RECONCILIATION.json")
        history_check = readm(z, "validation/HISTORY_CORRECTION_CHECK.json")
        correction_audit = readj(BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET288_HISTORY_CORRECTION_INDEPENDENT_AUDIT.json")
        correction_receipt = readj(BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET288_HISTORY_CORRECTION_RECEIPT.json")
        correction_local = readj(correction_dir / "HISTORY_CORRECTION.json")
        correction_delivery_local = readj(correction_dir / "DD_Rank9_ProjectionConfinement2_Packet288_HistoryCorrection_DELIVERY.json")
        check("History correction is resolved, independently audited, and changes no current source or decision authority", workflow.get("id") == "PC288-E01" and workflow.get("status") == "RESOLVED_IN_RETURN_CONTEXT" and workflow.get("historicalCountsSuperseded") is True and workflow.get("sourceFilesEdited") is False and workflow.get("blocksSourceReview") is False and history_check.get("status") == "PASS" and history_check.get("checkCount") == 48 and all(x.get("passed") is True for x in history_check.get("checks", [])) and correction_audit.get("status") == "PASS" and correction_audit.get("checkCount") == 8 and correction_receipt.get("status") == "PASS" and readm(z, "history_correction/HISTORY_CORRECTION.json") == correction_local and readm(z, "history_correction/DD_Rank9_ProjectionConfinement2_Packet288_HistoryCorrection_DELIVERY.json") == correction_delivery_local, {"workflow": workflow.get("status"), "historyChecks": history_check.get("checkCount"), "correctionAudit": correction_audit.get("status"), "correctionAuditChecks": correction_audit.get("checkCount")})
        prior_delivery = readj(prior232_delivery_path)
        prior_audit = readj(BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json")
        with zipfile.ZipFile(prior232_path) as prior:
            prior_decision = json.loads(prior.read("DIRECTOR_DECISION.json").decode("utf-8-sig"))
        prior_blockers = {x.get("id"): x.get("blockerIds") for x in prior_decision.get("perIdentityDecisions", [])}
        check("Return232 exact prior HOLD and its independent PASS audit are preserved", prior_delivery.get("heldIds") == TARGETS and prior_decision.get("acceptedIds") == [] and prior_decision.get("appliedIds") == [] and prior_blockers == BLOCKERS and prior_audit.get("status") == "PASS" and prior_audit.get("checkCount") == 35 and readm(z, "history_correction/evidence/RETURN232_DELIVERY.json") == prior_delivery and readm(z, "history_correction/evidence/RETURN232_INDEPENDENT_AUDIT.json") == prior_audit, {"priorAudit": prior_audit.get("status"), "checks": prior_audit.get("checkCount"), "blockers": prior_blockers})
        with zipfile.ZipFile(prior232_path) as prior:
            preservation = readm(z, "PRESERVATION_MANIFEST.json")
            preserve_failures = []
            for row in preservation.get("members", []):
                member = row.get("priorMember")
                if member not in prior.namelist() or not sha_matches(prior.read(member), row):
                    preserve_failures.append(member)
            check("Every Return232 member named by the preservation manifest remains byte-exact", len(preservation.get("members", [])) >= 8 and not preserve_failures and sha_matches(prior232_path.read_bytes(), workflow.get("priorArchive", {})), {"preserved": len(preservation.get("members", [])), "failures": preserve_failures[:10]})

        # Return284-287 are carried unchanged and remain outside this review's scope.
        expected_prior = {
            "RETURN284_DELIVERY.json": {"banishment-gate", "conjure-demiplane-fortress"},
            "RETURN285_DELIVERY.json": {"summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"},
            "RETURN286_DELIVERY.json": {"reverse-gravity-field"},
            "RETURN287_DELIVERY.json": {"alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"},
        }
        inherited_failures = []
        for filename, held in expected_prior.items():
            row = readm(z, "inherited/" + filename)
            packet_row = readm(source, "evidence/" + filename)
            if row != packet_row or set(row.get("heldIds", [])) != held or row.get("acceptedIds") != [] or row.get("appliedIds") != []:
                inherited_failures.append(filename)
        unrelated = set(hold.get("unrelatedHoldsPreserved", []))
        required_unrelated = {"PG200-B03", "PG200-B04", "PG200-B06", "SH202-B01", "SH202-B02", "SH202-B03", "IE204-B02", "AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"}
        check("Return284-287 holds match Packet288 history and remain unchanged outside scope", not inherited_failures and unrelated == required_unrelated and hold.get("closedOutsideScope") == ["AFP211-E01"], {"failures": inherited_failures, "unrelatedHolds": sorted(unrelated), "closed": hold.get("closedOutsideScope")})

        # Return288 must name the exact next pending row in the current queue.
        next_group = readm(z, "NEXT_PENDING_GROUP.json")
        embedded_queue = readm(z, "context/CURRENT_SPELL_QUEUE_288.json")
        queue_rows = embedded_queue.get("currentPendingGroups", [])
        queue_next = next((x for x in queue_rows if x.get("group") == NEXT["group"]), None)
        check("Next group is exactly the still-pending Miracle/Reality pair", next_group.get("group") == NEXT["group"] and next_group.get("pendingIds") == NEXT["pendingIds"] and next_group.get("reviewStarted") is False and queue_next is not None and queue_next.get("pendingIds") == NEXT["pendingIds"] and queue_next.get("pendingCount") == 2 and next_group == d.get("nextPendingGroup") and embedded_queue.get("currentAuthority") == AUTH, next_group)

        package_checks = d.get("packageChecks", [])
        data_checks = readm(z, "validation/CHECKS.json")
        artifact_checks = readm(z, "validation/ARTIFACT_CHECKS.json")
        semantic_checks = readm(z, "validation/SCOPED_SEMANTIC_CHECKS.json")
        check("Package, source replay, artifact, focused semantics and history checks all pass", len(package_checks) == d.get("packageCheckCount") == 487 and all(x.get("passed") is True for x in package_checks) and len(data_checks) == 2177 and all(x.get("passed") is True for x in data_checks) and len(artifact_checks) == d.get("artifactCheckCount") == 30 and all(x.get("passed") is True for x in artifact_checks) and len(semantic_checks) == 55 and all(x.get("passed") is True for x in semantic_checks) and counts.get("sourceDataReplayChecks") == 2177 and counts.get("additionalScopedSemanticChecks") == 55 and counts.get("combinedSourceDataSemanticChecks") == 2232 and d.get("historyCorrectionCheckCount") == 48, {"packageChecks": len(package_checks), "sourceChecks": len(data_checks), "artifactChecks": len(artifact_checks), "semanticChecks": len(semantic_checks), "historyCorrectionChecks": d.get("historyCorrectionCheckCount")})
        check("No spell, canonical file, runtime, source program or GitHub change is reported", decision.get("accepted") is False and decision.get("applied") is False and decision.get("canonicalChanges") is False and decision.get("githubChanges") is False and decision.get("runtimeExecuted") is False and decision.get("sourceProgramsExecuted") is False and source_bindings.get("programsExecuted") is False and authority.get("canonicalChanges") is False, {"accepted": decision.get("accepted"), "applied": decision.get("applied"), "canonicalChanges": decision.get("canonicalChanges"), "runtimeExecuted": decision.get("runtimeExecuted")})

    failures = [x for x in checks if not x["passed"]]
    report = {
        "id": "RANK9PROJECTIONCONFINEMENT2-RETURN288-INDEPENDENT-AUDIT",
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_digest},
        "authority": AUTH,
        "targetIds": TARGETS,
        "acceptedIds": d.get("acceptedIds"),
        "appliedIds": d.get("appliedIds"),
        "heldIds": d.get("heldIds"),
        "blockers": BLOCKERS,
        "nextPendingGroup": d.get("nextPendingGroup"),
        "memberCount": d.get("zipMemberCount"),
        "checkCount": len(checks),
        "passedChecks": len(checks) - len(failures),
        "failedChecks": len(failures),
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_digest = digest(REPORT.read_bytes())
    receipt = {
        "id": "RANK9PROJECTIONCONFINEMENT2-RETURN288-RECEIPT",
        "auditStatus": report["status"],
        "archive": report["archive"],
        "deliveryManifest": report["deliveryManifest"],
        "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **report_digest},
        "authority": AUTH,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockerIds": BLOCKERS,
        "nextPendingGroup": {"group": NEXT["group"], "pendingIds": NEXT["pendingIds"]},
        "checkCount": len(checks),
        "failedChecks": len(failures),
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "archiveSha256": archive_digest["sha256"], "deliverySha256": delivery_digest["sha256"], "failures": failures}, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
