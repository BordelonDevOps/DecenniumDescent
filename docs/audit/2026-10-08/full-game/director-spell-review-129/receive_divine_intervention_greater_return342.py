#!/usr/bin/env python3
"""Independently verify sealed Divine Intervention Greater Return342 and advance queue."""
from __future__ import annotations

import hashlib
import json
import shutil
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
PREP = A / "rank9_divine_intervention_greater_review_342_prepared"
PREP_ZIP = PREP / "DD_Rank9_DivineInterventionGreater_Review342.zip"
PREP_DELIVERY = PREP / "DD_Rank9_DivineInterventionGreater_Review342_DELIVERY.json"
DOWNLOADS = Path.home() / "Downloads"
IN_ZIP = DOWNLOADS / "DD_DivineInterventionGreater_Director_Return342_HELD.zip"
IN_DELIVERY = DOWNLOADS / "DD_DivineInterventionGreater_Director_Return342_HELD_DELIVERY.json"
RECEIVED = A / "rank9_divine_intervention_greater_return342_received"
PAYLOAD = RECEIVED / "payload"
ARCHIVE = RECEIVED / IN_ZIP.name
DELIVERY = RECEIVED / IN_DELIVERY.name
AUDIT = A / "DIVINE_INTERVENTION_GREATER_RETURN342_INDEPENDENT_AUDIT.json"
RECEIPT = A / "DIVINE_INTERVENTION_GREATER_RETURN342_RECEIPT.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_342.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_342.json"
HANDOFF = A / "CURRENT_HANDOFF_342.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_342.md"
HISTORICAL_ARCHIVE = A / "rank9_miraclereality2_current_source_289_prepared" / "DD_Rank9_MiracleReality2_CurrentSource_289.zip"
AUTHORITY = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
SPELL = "divine-intervention-greater"
BLOCKER = "MR233-B01"
NEXT = "wish"
NEXT_BLOCKER = "MR233-B02"
GROUP = "rank9-miracle-reality2"
checks: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def safe_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and ":" not in name


def check(ident: str, passed: bool, detail: str) -> None:
    checks.append({"id": ident, "passed": bool(passed), "detail": detail})


def main() -> None:
    required = (IN_ZIP, IN_DELIVERY, PREP_ZIP, PREP_DELIVERY, HISTORICAL_ARCHIVE,
                A / "CURRENT_SPELL_QUEUE_341.json", A / "CURRENT25_PENDING_IDENTITY_AUDIT_341.json",
                A / "CURRENT_HANDOFF_341.json")
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    if any(p.exists() for p in (AUDIT, RECEIPT, QUEUE, PENDING, HANDOFF, SNAPSHOT)):
        raise RuntimeError("Refusing to overwrite an existing Return342 receipt or queue file.")
    RECEIVED.mkdir(parents=True, exist_ok=True)
    for source, dest in ((IN_ZIP, ARCHIVE), (IN_DELIVERY, DELIVERY)):
        if dest.exists() and dest.read_bytes() != source.read_bytes():
            raise RuntimeError(f"Existing received file differs from the downloaded Director artifact: {dest}")
        if not dest.exists():
            shutil.copyfile(source, dest)
    archive_bytes = ARCHIVE.read_bytes()
    delivery = load(DELIVERY)
    archive_binding = delivery.get("archive", {})
    check("delivery-return-identity", delivery.get("id") == "DIVINE-INTERVENTION-GREATER-DIRECTOR-RETURN342-HELD-DELIVERY" and delivery.get("reviewId") == "Return342", "Return342 delivery identity.")
    check("archive-name-size-sha-crc", archive_binding.get("fileName") == ARCHIVE.name and (archive_binding.get("bytes"), archive_binding.get("sha256"), archive_binding.get("crc32")) == (len(archive_bytes), sha(archive_bytes), crc(archive_bytes)), json.dumps(archive_binding))
    check("single-target-hold", delivery.get("targetIds") == [SPELL] and delivery.get("heldIds") == [SPELL] and delivery.get("blockerIds") == [BLOCKER] and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [], "Only Divine Intervention Greater / MR233-B01 is held.")
    check("no-application-or-canonical-mutation", delivery.get("applicationAuthorized") is False and delivery.get("canonicalMutation") is False and delivery.get("releaseApproved") in (None, False), "Return342 does not authorize application, release, or canonical mutation.")
    check("authority-unchanged", delivery.get("authority") == AUTHORITY, repr(delivery.get("authority")))
    check("next-priority-wish", delivery.get("nextPendingIdentity") == NEXT and delivery.get("nextBlockerIds") == [NEXT_BLOCKER] and delivery.get("nextPendingGroup") == GROUP, "Wish / MR233-B02 is the next review target.")
    seals = delivery.get("sealChecks", [])
    check("director-seal-check-rows", len(seals) == 93 and all(row.get("passed") is True for row in seals), f"Director claims {len(seals)} seal rows.")
    check("director-seal-counts", delivery.get("sealCheckCount") == 93 and delivery.get("sealPassed") == 93 and delivery.get("sealFailed") == 0, "93/93 reported seal checks.")
    counts = delivery.get("counts", {})
    check("director-source-data-counts", counts.get("sourceDataChecks") == counts.get("sourceDataPassed") == 449 and counts.get("sourceDataFailed") == 0, "449/449 reported source/data checks.")
    check("no-replays-or-fabricated-events", counts.get("freshCaseReplays") == counts.get("freshEvents") == counts.get("freshForwardOperations") == counts.get("freshInverseOperations") == counts.get("freshActorClockChecks") == 0, "No cases or gameplay events were replayed or fabricated.")

    prior_queue = load(A / "CURRENT_SPELL_QUEUE_341.json")
    prior_pending = load(A / "CURRENT25_PENDING_IDENTITY_AUDIT_341.json")
    prior_handoff = load(A / "CURRENT_HANDOFF_341.json")
    with ZipFile(ARCHIVE) as z, ZipFile(PREP_ZIP) as submitted, ZipFile(HISTORICAL_ARCHIVE) as hist:
        names = z.namelist()
        name_set = set(names)
        external_rows = delivery.get("members", [])
        external_map = {row.get("path"): row for row in external_rows}
        check("zip-integrity-and-safe-names", z.testzip() is None and len(names) == len(name_set) == 43 and all(safe_name(n) for n in names), f"archiveMembers={len(names)}")
        check("delivery-member-roster", len(external_rows) == len(external_map) == 43 and delivery.get("archiveMemberCount") == 43 and delivery.get("payloadMemberCount") == 42 and delivery.get("exactAllowlist") == names == list(external_map), "Exact external 43-member roster/order.")
        ext_ok = True
        for row in external_rows:
            data = z.read(row["path"])
            ext_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("external-member-bindings", ext_ok, "Every DELIVERY member size/SHA/CRC matches the exact ZIP member.")
        root_manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        payload_names = [n for n in names if n != "MEMBER_MANIFEST.json"]
        root_rows = root_manifest.get("members", [])
        root_ok = root_manifest.get("id") == "DIVINE-INTERVENTION-GREATER-RETURN342-MEMBER-MANIFEST" and root_manifest.get("payloadMemberCount") == 42 and root_manifest.get("exactPayloadAllowlist") == payload_names and len(root_rows) == 42
        for row in root_rows:
            if row.get("path") not in name_set or row.get("path") == "MEMBER_MANIFEST.json":
                root_ok = False
                continue
            data = z.read(row["path"])
            root_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("root-manifest", root_ok, "Root manifest binds the exact 42 payload members.")

        decision = json.loads(z.read("DIRECTOR_DECISION.json"))
        hold = json.loads(z.read("HOLD_REGISTER.json"))
        queue_status = json.loads(z.read("QUEUE_STATUS.json"))
        coverage = json.loads(z.read("CASE_COVERAGE.json"))
        source_rec = json.loads(z.read("SOURCE_RECONCILIATION.json"))
        sem = json.loads(z.read("SEMANTIC_RECONCILIATION.json"))
        validation = json.loads(z.read("VALIDATION.json"))
        check("sealed-director-decision", decision.get("id") == "DIVINE-INTERVENTION-GREATER-DIRECTOR-RETURN342" and decision.get("decision") == "HOLD" and decision.get("targetIds") == [SPELL] and decision.get("heldIds") == [SPELL] and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("applicationAuthorized") is False and decision.get("canonicalMutation") is False, "One identity held; no application or canonical mutation.")
        identity_decisions = decision.get("perIdentity", [])
        check("identity-blocker-and-contracts", len(identity_decisions) == 1 and identity_decisions[0].get("id") == SPELL and identity_decisions[0].get("blockerIds") == [BLOCKER] and identity_decisions[0].get("openContractAndWitnessIds") == ["MR342-W01", "MR342-W02", "MR342-W03"], "Three open one-target contracts.")
        contracts = hold.get("openContractsAndWitnessNeeds", [])
        check("hold-register-contracts", hold.get("spellId") == SPELL and hold.get("blockerId") == BLOCKER and hold.get("status") == "OPEN" and [x.get("id") for x in contracts] == ["MR342-W01", "MR342-W02", "MR342-W03"] and [x.get("status") for x in contracts] == ["OPEN", "OPEN", "MISSING_PAID_INTEGRATED_WITNESSES"], "Useful question, substantive task, and paid Cleric/Wizard encounter requirements remain open.")
        check("semantic-gate-remains-hold", sem.get("completePositiveSpell") is False and sem.get("acceptanceGate") == "FAIL_MISSING_CENTRAL_CONTRACTS_AND_PAID_WITNESSES" and sem.get("blockerIds") == [BLOCKER], "Integrity does not establish acceptance.")
        check("case-coverage-no-replay", coverage.get("spellId") == SPELL and coverage.get("priorCasesReplayed") is False and coverage.get("freshCaseReplays") == 0 and coverage.get("freshEvents") == 0 and coverage.get("freshForwardOperations") == 0 and coverage.get("freshInverseOperations") == 0 and coverage.get("freshActorClockChecks") == 0, "No prior case replay or invented gameplay witness.")
        qpending = queue_status.get("pendingIds", [])
        ppending = prior_pending.get("pendingIds", [])
        check("queue-pending-unchanged-and-wish-next", queue_status.get("authority") == AUTHORITY and queue_status.get("pendingCount") == 25 and len(qpending) == len(ppending) == 25 and set(qpending) == set(ppending) and queue_status.get("heldIds") == [SPELL] and queue_status.get("nextPendingIdentity") == NEXT and queue_status.get("nextBlockerIds") == [NEXT_BLOCKER] and queue_status.get("nextPendingGroup") == GROUP and queue_status.get("wishNotAdjudicated") is True and queue_status.get("canonicalQueueEdited") is False, "All 25 pending identities are preserved; Wish alone is next and not adjudicated here.")
        preserved_claim = decision.get("preserved", "")
        check("prior-holds-preserved", "Return336-341" in preserved_claim and "AFP211-E01" in preserved_claim and "MR233-E01 CLOSED" in preserved_claim and "Wish MR233-B02 is context only, not adjudicated" in preserved_claim and queue_status.get("separatelyRetainedHolds") == prior_queue.get("separatelyRetainedHolds") and queue_status.get("continuingPriorityOrderPreserved") == prior_queue.get("continuingPriorityOrder"), "Return336-341, all unrelated holds, and the prior queue order are preserved; Wish not re-adjudicated.")
        vchecks = validation.get("checks", [])
        check("source-validation-record", validation.get("status") == "PASS_SOURCE_AND_DATA_INTEGRITY_ONLY" and len(vchecks) == 449 and all(row.get("passed") is True for row in vchecks) and validation.get("semanticAcceptanceGate") == "NOT_PASSED_MR233_B01", "Director's 449 source/data checks pass; semantic acceptance gate fails.")

        # Verify all 153 historical-to-current source rows against both actual archives and this checkout.
        delta = json.loads(z.read("evidence/packet/input/09_RETURN289_TO_CURRENT_SOURCE_DELTA.json"))
        rows = delta.get("sourceBindings", [])
        historical_archive_ref = delta.get("priorSourceSnapshot", {}).get("archive", {})
        historical_bytes = HISTORICAL_ARCHIVE.read_bytes()
        hist_ok = historical_archive_ref.get("bytes") == len(historical_bytes) and historical_archive_ref.get("sha256") == sha(historical_bytes) and historical_archive_ref.get("crc32") == crc(historical_bytes) and hist.testzip() is None
        current_ok = hist_ok and len(rows) == 153
        actual_changed = []
        hist_members = set(hist.namelist())
        for row in rows:
            hist_member = row.get("previousReturn289PacketMember", "")
            path = ROOT / PurePosixPath(row.get("path", ""))
            if hist_member not in hist_members or not path.is_file():
                current_ok = False
                continue
            prev = hist.read(hist_member)
            live = path.read_bytes()
            prev_match = (len(prev), sha(prev)) == (row.get("previousBytes"), row.get("previousSha256"))
            live_match = (len(live), sha(live)) == (row.get("currentBytes"), row.get("currentSha256"))
            changed = (len(prev), sha(prev)) != (len(live), sha(live))
            flag_match = row.get("unchangedSinceReturn289") is (not changed)
            current_ok &= prev_match and live_match and flag_match
            if changed:
                actual_changed.append(row.get("path"))
        reported_changed = delta.get("currentChangedPaths", [])
        check("historical-archive-binding-and-integrity", hist_ok and historical_archive_ref.get("path") == (A / "rank9_miraclereality2_current_source_289_prepared" / "DD_Rank9_MiracleReality2_CurrentSource_289.zip").relative_to(ROOT).as_posix(), "Exact Return289 source archive hash and ZIP integrity.")
        check("all-153-historical-and-live-source-bindings", current_ok, f"Independently checked {len(rows)} old archive members against actual workspace files.")
        check("exact-source-delta-paths", actual_changed == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"] and reported_changed == actual_changed and delta.get("targetSpecificFilesChanged") is False, json.dumps(actual_changed))
        current_bindings = source_rec.get("currentSourceBindings", [])
        check("current-full-source-roster", len(current_bindings) == 12 and source_rec.get("currentEmbeddedSourceCount") == 12 and source_rec.get("currentEmbeddedRowsIndependentlyByteVerified") == 12, "Twelve current source bindings embedded.")
        cur_ok = True
        for row in current_bindings:
            live_path = ROOT / PurePosixPath(row["path"])
            member = "evidence/packet/" + row["packetMember"]
            if not live_path.is_file() or member not in name_set:
                cur_ok = False
                continue
            live = live_path.read_bytes()
            payload = z.read(member)
            cur_ok &= live == payload and (len(live), sha(live), crc(live)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("all-12-live-current-source-bindings", cur_ok, "Current embedded source bytes match workspace and Return342 evidence members.")
        comp = json.loads(z.read("evidence/packet/input/10_CURRENT_SOURCE_BINDINGS_342.json"))
        extra = source_rec.get("additionalCurrentComparatorBindings", [])
        extras_ok = len(extra) == 2 and len(comp.get("fullCurrentSources", [])) == 12
        for row in extra:
            live_path = ROOT / PurePosixPath(row["path"])
            member = "evidence/packet/" + row["packetMember"]
            if not live_path.is_file() or member not in name_set:
                extras_ok = False
                continue
            live = live_path.read_bytes()
            extras_ok &= (len(live), sha(live), crc(live)) == (row.get("bytes"), row.get("sha256"), row.get("crc32")) == (len(z.read(member)), sha(z.read(member)), crc(z.read(member)))
        check("two-extra-current-comparator-bindings", extras_ok, "Both separately declared comparator sources match the workspace and archive.")
        submitted = decision.get("inputPacket", {})
        submitted_del = decision.get("inputDelivery", {})
        prep_zip_bytes, prep_del_bytes = PREP_ZIP.read_bytes(), PREP_DELIVERY.read_bytes()
        submitted_ok = submitted.get("fileName") == PREP_ZIP.name and (submitted.get("bytes"), submitted.get("sha256"), submitted.get("crc32")) == (len(prep_zip_bytes), sha(prep_zip_bytes), crc(prep_zip_bytes))
        submitted_ok &= submitted_del.get("fileName") == PREP_DELIVERY.name and (submitted_del.get("bytes"), submitted_del.get("sha256"), submitted_del.get("crc32")) == (len(prep_del_bytes), sha(prep_del_bytes), crc(prep_del_bytes)) and z.read("evidence/Review342_DELIVERY.json") == prep_del_bytes
        check("exact-submitted-review342-bindings", submitted_ok, "Return binds the exact submitted Review342 ZIP and delivery manifest.")
        packet_manifest = json.loads(z.read("evidence/packet/MEMBER_MANIFEST.json"))
        packet_rows = packet_manifest.get("members", [])
        packet_names = [n[len("evidence/packet/"):] for n in names if n.startswith("evidence/packet/") and n != "evidence/packet/MEMBER_MANIFEST.json"]
        packet_ok = {row.get("path") for row in packet_rows} == set(packet_names) and len(packet_rows) == packet_manifest.get("payloadMemberCount") == len(packet_names)
        for row in packet_rows:
            member = "evidence/packet/" + row.get("path", "")
            if member not in name_set:
                packet_ok = False
                continue
            data = z.read(member)
            packet_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("nested-review342-packet-manifest", packet_ok, f"Nested manifest binds all {len(packet_names)} exact packet files.")

    if any(not item["passed"] for item in checks):
        raise RuntimeError("Return342 independent verification failed: " + json.dumps([item for item in checks if not item["passed"]]))

    with ZipFile(ARCHIVE) as z:
        for name in sorted(n for n in z.namelist() if n != "MEMBER_MANIFEST.json"):
            dst = PAYLOAD.joinpath(*PurePosixPath(name).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(z.read(name))

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path, hold_path = PAYLOAD / "DIRECTOR_DECISION.json", PAYLOAD / "HOLD_REGISTER.json"
    open_contracts = ["MR342-W01", "MR342-W02", "MR342-W03"]
    audit = {
        "id": "DIVINE-INTERVENTION-GREATER-RETURN342-INDEPENDENT-AUDIT",
        "recordedAtUtc": timestamp,
        "status": "PASS_RETURN342_SEALED_HOLD_MR233_B01",
        "archive": archive_ref,
        "delivery": delivery_ref,
        "archiveMemberCount": 43,
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(item["passed"] for item in checks),
        "failed": sum(not item["passed"] for item in checks),
        "historicalSourceRowsIndependentlyVerifiedAgainstWorkspace": 153,
        "decision": "HOLD",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationAuthorizedIds": [],
        "authority": AUTHORITY,
        "openContractIds": open_contracts,
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(AUDIT, audit)
    receipt = {
        "id": "DIVINE-INTERVENTION-GREATER-RETURN342-RECEIPT",
        "recordedAtUtc": timestamp,
        "decision": "HOLD",
        "blockerIds": [BLOCKER],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "holdRegister": bind(hold_path),
        "independentAudit": bind(AUDIT),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationAuthorizedIds": [],
        "openContractIds": open_contracts,
        "authority": AUTHORITY,
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "nextGroup": GROUP,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(RECEIPT, receipt)
    audit_ref, receipt_ref, decision_ref = bind(AUDIT), bind(RECEIPT), bind(decision_path)
    retained = sorted(set(prior_queue.get("separatelyRetainedHolds", [])) | set(prior_queue.get("currentReturnHeldIds", [])) | {SPELL})
    blockers = dict(prior_queue.get("currentReturnBlockers", {}))
    blockers[SPELL] = [BLOCKER]
    queue = dict(prior_queue)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-342", "recordedAtUtc": timestamp,
        "supersedesQueue": bind(A / "CURRENT_SPELL_QUEUE_341.json"),
        "currentAuthority": AUTHORITY, "pendingCount": 25, "acceptedUnapplied": 0,
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "nextGroup": GROUP, "next": NEXT, "nextPendingIds": [NEXT], "nextPendingCount": 1,
        "heldThisStep": [SPELL], "separatelyRetainedHolds": retained,
        "pendingIdentityAudit": PENDING.relative_to(ROOT).as_posix(),
        "currentHandoff": HANDOFF.relative_to(ROOT).as_posix(), "currentPacket": None,
        "currentPacketStatus": "RETURN342_DIVINE_INTERVENTION_GREATER_HELD_WISH_MR233_B02_NEXT",
        "activeReview": {"spellId": NEXT, "blockerIds": [NEXT_BLOCKER], "packet": None, "status": "DIRECTOR_RETURN342_NEXT_PRIORITY"},
        "currentReturn": receipt_ref, "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref, "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref, "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": [SPELL],
        "currentReturnBlockers": blockers,
        "currentDirectorInstruction": "Return342 holds Divine Intervention Greater / MR233-B01. MR342-W01 useful single-question outcome and W02 substantive task contract remain open; W03 actual acquired paid Cleric/Wizard encounter witnesses remain missing. Director authorship permission is not evidence of complete content or witness facts. No application is authorized. Return336-341 holds and AFP211-E01 CLOSED remain unchanged. Next Director priority: Wish / MR233-B02.",
        "directorConnectionStatus": "Return342 independently verified. Divine Intervention Greater remains held; next is Wish / MR233-B02.",
        "applicationPerformed": False, "canonicalFilesChanged": False, "githubChanges": False,
    })
    save(QUEUE, queue)
    pending = dict(prior_pending)
    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-342",
        "recordedAtUtc": timestamp,
        "status": "PASS_CURRENT_823_25_RETURN342_DIVINE_INTERVENTION_GREATER_HOLD_WISH_NEXT",
        "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_341.json",
        "authority": AUTHORITY, "pendingCount": 25, "acceptedIds": [], "appliedIds": [],
        "heldThisStep": [SPELL], "separatelyHeldIds": retained,
        "nextGroup": GROUP, "nextIdentity": NEXT, "nextBlockerIds": [NEXT_BLOCKER],
        "nextPendingIds": [NEXT], "nextPendingCount": 1,
        "nextStep": "Review Wish / MR233-B02 against exact current source bindings. Preserve Return336-342 holds and AFP211-E01 CLOSED; apply only an exact sealed acceptance.",
        "sourceQueue": QUEUE.relative_to(ROOT).as_posix(), "currentQueueBinding": bind(QUEUE),
        "currentHandoff": HANDOFF.relative_to(ROOT).as_posix(),
        "currentReturn": receipt_ref, "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref, "currentReturnReceipt": receipt_ref,
        "noPendingTargetSilentlyAccepted": True, "allCurrentPendingIdentitiesReviewed": True,
        "unreviewedPendingIds": [], "canonicalFilesChanged": False, "applicationPerformed": False,
    })
    save(PENDING, pending)
    handoff = dict(prior_handoff)
    handoff.update({
        "id": "CURRENT-HANDOFF-342", "recordedAtUtc": timestamp,
        "supersedes": "CURRENT_HANDOFF_341.json",
        "status": "RETURN342_VERIFIED_DIVINE_INTERVENTION_GREATER_HELD_WISH_NEXT_823_25_0",
        "authority": AUTHORITY, "queue": QUEUE.relative_to(ROOT).as_posix(),
        "queueBinding": bind(QUEUE), "pendingIdentityAudit": PENDING.name,
        "pendingIdentityAuditBinding": bind(PENDING), "currentDirectorReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref, "currentReturnAudit": audit_ref,
        "currentReturnArchive": archive_ref, "currentReturnDelivery": delivery_ref,
        "heldThisStep": [SPELL], "separatelyRetainedHolds": retained,
        "acceptedIds": [], "appliedIds": [], "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": NEXT, "blockerId": NEXT_BLOCKER, "group": GROUP},
        "nextPendingGroup": {"group": GROUP, "pendingIds": [NEXT], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Wish / MR233-B02 using exact current source bindings; preserve Return336-342 holds and AFP211-E01 CLOSED; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return342 sealed Divine Intervention Greater HOLD; the Director designates Wish / MR233-B02 next.",
    })
    save(HANDOFF, handoff)
    SNAPSHOT.write_text(
        "# Spell review status — queue 342\n\n"
        f"Return342 independently verified {len(checks)}/{len(checks)} checks and holds Divine Intervention Greater / MR233-B01. "
        "Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "The open contracts are a complete useful question outcome, a concrete substantive task outcome, and acquired paid Cleric/Wizard encounters demonstrating those routes. Return336-342 holds and AFP211-E01 CLOSED remain unchanged; no application is authorized.\n\n"
        "Next Director-prioritized identity: **Wish / MR233-B02**.\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"status": "PASS", "checks": len(checks), "passed": sum(x["passed"] for x in checks), "failed": sum(not x["passed"] for x in checks), "archiveMembers": 43, "historicalSourceRowsIndependentlyVerified": 153, "held": SPELL, "authority": AUTHORITY, "next": NEXT, "receipt": str(RECEIPT)}, indent=2))


if __name__ == "__main__":
    main()
