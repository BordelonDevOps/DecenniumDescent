#!/usr/bin/env python3
"""Independently verify sealed Wish Return343 and close the first-review order."""
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
PREP = A / "rank9_wish_review_343_prepared"
PREP_ZIP = PREP / "DD_Rank9_Wish_Review343.zip"
PREP_DELIVERY = PREP / "DD_Rank9_Wish_Review343_DELIVERY.json"
DOWNLOADS = Path.home() / "Downloads"
IN_ZIP = DOWNLOADS / "DD_Wish_Director_Return343_HELD.zip"
IN_DELIVERY = DOWNLOADS / "DD_Wish_Director_Return343_HELD_DELIVERY.json"
RECEIVED = A / "rank9_wish_return343_received"
PAYLOAD = RECEIVED / "payload"
ARCHIVE = RECEIVED / IN_ZIP.name
DELIVERY = RECEIVED / IN_DELIVERY.name
AUDIT = A / "WISH_RETURN343_INDEPENDENT_AUDIT.json"
RECEIPT = A / "WISH_RETURN343_RECEIPT.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_343.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_343.json"
HANDOFF = A / "CURRENT_HANDOFF_343.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_343.md"
HISTORICAL_ARCHIVE = A / "rank9_miraclereality2_current_source_289_prepared" / "DD_Rank9_MiracleReality2_CurrentSource_289.zip"
AUTHORITY = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
SPELL = "wish"
BLOCKER = "MR233-B02"
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
                A / "CURRENT_SPELL_QUEUE_342.json", A / "CURRENT25_PENDING_IDENTITY_AUDIT_342.json",
                A / "CURRENT_HANDOFF_342.json", PREP / "PREPARATION_AUDIT_343.json")
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    if any(p.exists() for p in (AUDIT, RECEIPT, QUEUE, PENDING, HANDOFF, SNAPSHOT)):
        raise RuntimeError("Refusing to overwrite an existing Return343 receipt or queue file.")
    RECEIVED.mkdir(parents=True, exist_ok=True)
    for source, dest in ((IN_ZIP, ARCHIVE), (IN_DELIVERY, DELIVERY)):
        if dest.exists() and dest.read_bytes() != source.read_bytes():
            raise RuntimeError(f"Existing received file differs from downloaded Director artifact: {dest}")
        if not dest.exists():
            shutil.copyfile(source, dest)

    archive_bytes = ARCHIVE.read_bytes()
    delivery = load(DELIVERY)
    expected_archive = delivery.get("archive", {})
    check("delivery-return343-identity", delivery.get("id") == "WISH-DIRECTOR-RETURN343-HELD-DELIVERY" and delivery.get("reviewId") == "Return343", "Return343 delivery identity.")
    check("archive-name-size-sha-crc", expected_archive.get("fileName") == ARCHIVE.name and (expected_archive.get("bytes"), expected_archive.get("sha256"), expected_archive.get("crc32")) == (len(archive_bytes), sha(archive_bytes), crc(archive_bytes)), json.dumps(expected_archive))
    check("single-target-wish-hold", delivery.get("targetIds") == [SPELL] and delivery.get("heldIds") == [SPELL] and delivery.get("blockerIds") == [BLOCKER] and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [], "Only Wish / MR233-B02 is held.")
    check("no-application-or-canonical-mutation", delivery.get("applicationAuthorized") is False and delivery.get("canonicalMutation") is False and delivery.get("releaseApproved") in (None, False), "Return343 does not authorize application, release, or canonical mutation.")
    check("authority-unchanged", delivery.get("authority") == AUTHORITY, repr(delivery.get("authority")))
    check("first-review-order-exhausted", delivery.get("nextPendingIdentity") is None and delivery.get("nextBlockerIds") is None and delivery.get("closureTasksRemaining") == 25 and delivery.get("firstReviewTasksRemaining") == 0, "No first-review target remains; all 25 closure tasks remain.")
    seals = delivery.get("sealChecks", [])
    check("director-seal-rows", len(seals) == 95 and all(row.get("passed") is True for row in seals), f"Director reports {len(seals)} seal rows.")
    check("director-seal-counts", delivery.get("sealCheckCount") == 95 and delivery.get("sealPassed") == 95 and delivery.get("sealFailed") == 0, "95/95 reported seal checks.")
    counts = delivery.get("counts", {})
    check("source-data-check-counts", counts.get("sourceDataChecks") == counts.get("sourceDataPassed") == 464 and counts.get("sourceDataFailed") == 0, "464/464 reported source/data checks.")
    check("no-replay-or-fabricated-events", counts.get("freshCaseReplays") == counts.get("freshEvents") == counts.get("freshForwardOperations") == counts.get("freshInverseOperations") == counts.get("freshActorClockChecks") == 0, "No prior cases or gameplay events were replayed or fabricated.")

    prior_queue = load(A / "CURRENT_SPELL_QUEUE_342.json")
    prior_pending = load(A / "CURRENT25_PENDING_IDENTITY_AUDIT_342.json")
    prior_handoff = load(A / "CURRENT_HANDOFF_342.json")
    with ZipFile(ARCHIVE) as z, ZipFile(PREP_ZIP) as submitted, ZipFile(HISTORICAL_ARCHIVE) as hist:
        names = z.namelist()
        name_set = set(names)
        external_rows = delivery.get("members", [])
        external_map = {row.get("path"): row for row in external_rows}
        check("zip-integrity-and-safe-names", z.testzip() is None and len(names) == len(name_set) == 44 and all(safe_name(n) for n in names), f"archiveMembers={len(names)}")
        check("delivery-exact-member-roster", len(external_rows) == len(external_map) == 44 and delivery.get("archiveMemberCount") == 44 and delivery.get("payloadMemberCount") == 43 and delivery.get("exactAllowlist") == names == list(external_map), "Exact external 44-member roster/order.")
        ext_ok = True
        for row in external_rows:
            data = z.read(row["path"])
            ext_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("external-member-bindings", ext_ok, "Every delivery size/SHA/CRC matches its exact archive member.")
        root_manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        root_payload = [n for n in names if n != "MEMBER_MANIFEST.json"]
        root_rows = root_manifest.get("members", [])
        root_ok = root_manifest.get("id") == "WISH-RETURN343-MEMBER-MANIFEST" and root_manifest.get("payloadMemberCount") == 43 and root_manifest.get("exactPayloadAllowlist") == root_payload and len(root_rows) == 43
        for row in root_rows:
            if row.get("path") not in name_set or row.get("path") == "MEMBER_MANIFEST.json":
                root_ok = False
                continue
            data = z.read(row["path"])
            root_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("root-manifest", root_ok, "Root manifest binds all 43 payload members.")

        decision = json.loads(z.read("DIRECTOR_DECISION.json"))
        hold = json.loads(z.read("HOLD_REGISTER.json"))
        qstatus = json.loads(z.read("QUEUE_STATUS.json"))
        coverage = json.loads(z.read("CASE_COVERAGE.json"))
        source_rec = json.loads(z.read("SOURCE_RECONCILIATION.json"))
        semantic = json.loads(z.read("SEMANTIC_RECONCILIATION.json"))
        validation = json.loads(z.read("VALIDATION.json"))
        check("sealed-director-decision", decision.get("id") == "WISH-DIRECTOR-RETURN343" and decision.get("reviewId") == "Return343" and decision.get("decision") == "HOLD" and decision.get("targetIds") == [SPELL] and decision.get("heldIds") == [SPELL] and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("applicationAuthorized") is False and decision.get("canonicalMutation") is False, "One target held; no application or canonical mutation.")
        identity_rows = decision.get("perIdentity", [])
        check("wish-blocker-and-open-contracts", len(identity_rows) == 1 and identity_rows[0].get("id") == SPELL and identity_rows[0].get("blockerIds") == [BLOCKER] and identity_rows[0].get("openContractAndWitnessIds") == ["MR343-W01", "MR343-W02", "MR343-W03"], "Three one-target Wish contracts remain open.")
        contracts = hold.get("openContractsAndWitnessNeeds", [])
        check("hold-contract-records", hold.get("spellId") == SPELL and hold.get("blockerId") == BLOCKER and hold.get("status") == "OPEN" and [r.get("id") for r in contracts] == ["MR343-W01", "MR343-W02", "MR343-W03"] and [r.get("status") for r in contracts] == ["OPEN", "OPEN", "MISSING_PAID_INTEGRATED_WITNESSES"], "Substantive outcomes, composite lifecycle/settlement, and paid four-route witnesses remain open.")
        check("semantic-gate-hold", semantic.get("completePositiveSpell") is False and semantic.get("acceptanceGate") == "FAIL_MISSING_CENTRAL_CONTRACTS_AND_PAID_WITNESSES" and semantic.get("blockerIds") == [BLOCKER], "No semantic acceptance despite integrity PASS.")
        check("coverage-no-replay", coverage.get("spellId") == SPELL and coverage.get("priorCasesReplayed") is False and coverage.get("freshCaseReplays") == coverage.get("freshEvents") == coverage.get("freshForwardOperations") == coverage.get("freshInverseOperations") == coverage.get("freshActorClockChecks") == 0, "No prior case replay or invented gameplay witness.")
        qpending, ppending = qstatus.get("pendingIds", []), prior_pending.get("pendingIds", [])
        check("queue-pending-and-order-preserved", qstatus.get("authority") == AUTHORITY and qstatus.get("pendingCount") == 25 and len(qpending) == len(ppending) == 25 and set(qpending) == set(ppending) and qstatus.get("heldIds") == [SPELL] and qstatus.get("currentReview") == SPELL and qstatus.get("nextPendingIdentity") is None and qstatus.get("nextPendingGroup") is None and qstatus.get("closureTasksRemaining") == 25 and qstatus.get("firstReviewTasksRemaining") == 0 and qstatus.get("unreviewedPendingIds") == [] and qstatus.get("canonicalQueueEdited") is False, "All 25 pending identities are retained; zero first-review identities and no next review are reported.")
        check("preserved-holds-and-priority-order", qstatus.get("separatelyRetainedHolds") == sorted(set(prior_queue.get("separatelyRetainedHolds", [])) | set(prior_queue.get("currentReturnHeldIds", []))) and qstatus.get("continuingPriorityOrderPreserved") == prior_queue.get("continuingPriorityOrder") and "Return336-342" in decision.get("preserved", "") and "AFP211-E01" in decision.get("preserved", "") and "MR233-E01 CLOSED" in decision.get("preserved", ""), "Return336-342, prior holds, and both closed findings are preserved.")
        vchecks = validation.get("checks", [])
        check("reported-source-validation", validation.get("status") == "PASS_SOURCE_AND_DATA_INTEGRITY_ONLY" and len(vchecks) == 464 and all(r.get("passed") is True for r in vchecks) and validation.get("semanticAcceptanceGate") == "NOT_PASSED_MR233_B02", "Director reports 464/464 source/data checks; semantic gate remains held.")

        # Check every historical byte and every present-day file; do not rely on the Director's 141-row limitation.
        delta = json.loads(z.read("evidence/packet/input/09_RETURN289_TO_CURRENT_SOURCE_DELTA.json"))
        rows = delta.get("sourceBindings", [])
        hist_ref = delta.get("priorSourceSnapshot", {}).get("archive", {})
        hist_bytes = HISTORICAL_ARCHIVE.read_bytes()
        hist_ok = hist_ref.get("bytes") == len(hist_bytes) and hist_ref.get("sha256") == sha(hist_bytes) and hist_ref.get("crc32") == crc(hist_bytes) and hist.testzip() is None
        live_ok = hist_ok and len(rows) == 153
        actual_changed = []
        hist_names = set(hist.namelist())
        for row in rows:
            old_member = row.get("previousReturn289PacketMember", "")
            live_path = ROOT / PurePosixPath(row.get("path", ""))
            if old_member not in hist_names or not live_path.is_file():
                live_ok = False
                continue
            old, live = hist.read(old_member), live_path.read_bytes()
            old_match = (len(old), sha(old)) == (row.get("previousBytes"), row.get("previousSha256"))
            live_match = (len(live), sha(live)) == (row.get("currentBytes"), row.get("currentSha256"))
            changed = (len(old), sha(old)) != (len(live), sha(live))
            live_ok &= old_match and live_match and row.get("unchangedSinceReturn289") is (not changed)
            if changed:
                actual_changed.append(row.get("path"))
        expected_path = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
        check("historical-archive-binding", hist_ok and hist_ref.get("path") == (A / "rank9_miraclereality2_current_source_289_prepared" / "DD_Rank9_MiracleReality2_CurrentSource_289.zip").relative_to(ROOT).as_posix() and source_rec.get("historicalSourceArchiveBinding") == hist_ref, "Exact Return289 historical source archive binding and ZIP integrity.")
        check("all-153-historical-and-live-source-rows", live_ok, f"Independently verified all {len(rows)} old-byte rows and actual current workspace files.")
        check("exact-source-change-set", actual_changed == [expected_path] and delta.get("currentChangedPaths") == actual_changed and source_rec.get("changedPaths") == actual_changed and delta.get("targetSpecificFilesChanged") is False, json.dumps(actual_changed))

        bindings = source_rec.get("currentSourceBindings", [])
        check("current-14-source-roster", len(bindings) == 14 and source_rec.get("currentEmbeddedSourceCount") == 14, "Fourteen current Wish source files are embedded.")
        bindings_ok = True
        for row in bindings:
            live_path = ROOT / PurePosixPath(row["path"])
            member = "evidence/packet/" + row["packetMember"]
            if not live_path.is_file() or member not in name_set:
                bindings_ok = False
                continue
            live = live_path.read_bytes()
            payload = z.read(member)
            bindings_ok &= live == payload and (len(live), sha(live), crc(live)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("all-14-current-source-bindings", bindings_ok, "All 14 current Wish sources match workspace bytes and archive members.")
        extra = source_rec.get("additionalCurrentComparatorBindings", [])
        extra_ok = len(extra) == 2
        for row in extra:
            live_path = ROOT / PurePosixPath(row["path"])
            member = "evidence/packet/" + row["packetMember"]
            if not live_path.is_file() or member not in name_set:
                extra_ok = False
                continue
            live, payload = live_path.read_bytes(), z.read(member)
            extra_ok &= (len(live), sha(live), crc(live)) == (row.get("bytes"), row.get("sha256"), row.get("crc32")) == (len(payload), sha(payload), crc(payload))
        check("two-extra-comparator-bindings", extra_ok, "Both extra current comparators match workspace and archive.")

        submitted, submitted_delivery = decision.get("inputPacket", {}), decision.get("inputDelivery", {})
        packet_bytes, delivery_bytes = PREP_ZIP.read_bytes(), PREP_DELIVERY.read_bytes()
        sent_ok = submitted.get("fileName") == PREP_ZIP.name and (submitted.get("bytes"), submitted.get("sha256"), submitted.get("crc32")) == (len(packet_bytes), sha(packet_bytes), crc(packet_bytes))
        sent_ok &= submitted_delivery.get("fileName") == PREP_DELIVERY.name and (submitted_delivery.get("bytes"), submitted_delivery.get("sha256"), submitted_delivery.get("crc32")) == (len(delivery_bytes), sha(delivery_bytes), crc(delivery_bytes)) and z.read("evidence/Review343_DELIVERY.json") == delivery_bytes
        check("exact-review343-submission-binding", sent_ok, "Return343 binds the exact submitted Review343 ZIP and delivery manifest.")

        nested = json.loads(z.read("evidence/packet/MEMBER_MANIFEST.json"))
        nested_rows = nested.get("members", [])
        nested_names = [n[len("evidence/packet/"):] for n in names if n.startswith("evidence/packet/") and n != "evidence/packet/MEMBER_MANIFEST.json"]
        nested_ok = nested.get("id") == "WISH-REVIEW343-PACKET-MANIFEST" and nested.get("payloadMemberCount") == len(nested_names) == 28 and {r.get("path") for r in nested_rows} == set(nested_names) and len(nested_rows) == 28
        for row in nested_rows:
            member = "evidence/packet/" + row.get("path", "")
            if member not in name_set:
                nested_ok = False
                continue
            data = z.read(member)
            nested_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("nested-review343-packet-manifest", nested_ok, "Nested packet manifest binds all 28 files exactly.")

    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return343 independent verification failed: " + json.dumps([row for row in checks if not row["passed"]]))

    with ZipFile(ARCHIVE) as z:
        for name in sorted(n for n in z.namelist() if n != "MEMBER_MANIFEST.json"):
            dst = PAYLOAD.joinpath(*PurePosixPath(name).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(z.read(name))
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path, hold_path = PAYLOAD / "DIRECTOR_DECISION.json", PAYLOAD / "HOLD_REGISTER.json"
    open_contracts = ["MR343-W01", "MR343-W02", "MR343-W03"]
    audit = {
        "id": "WISH-RETURN343-INDEPENDENT-AUDIT", "recordedAtUtc": timestamp,
        "status": "PASS_RETURN343_SEALED_HOLD_MR233_B02", "archive": archive_ref,
        "delivery": delivery_ref, "archiveMemberCount": 44, "checks": checks,
        "checkCount": len(checks), "passed": sum(c["passed"] for c in checks),
        "failed": sum(not c["passed"] for c in checks),
        "historicalSourceRowsIndependentlyVerifiedAgainstWorkspace": 153,
        "decision": "HOLD", "acceptedIds": [], "appliedIds": [], "heldIds": [SPELL],
        "applicationAuthorizedIds": [], "authority": AUTHORITY,
        "openContractIds": open_contracts, "nextIdentity": None, "nextBlockerIds": [],
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    save(AUDIT, audit)
    receipt = {
        "id": "WISH-RETURN343-RECEIPT", "recordedAtUtc": timestamp,
        "decision": "HOLD", "blockerIds": [BLOCKER], "archive": archive_ref,
        "delivery": delivery_ref, "directorDecision": bind(decision_path),
        "holdRegister": bind(hold_path), "independentAudit": bind(AUDIT),
        "acceptedIds": [], "appliedIds": [], "heldIds": [SPELL],
        "applicationAuthorizedIds": [], "openContractIds": open_contracts,
        "authority": AUTHORITY, "nextIdentity": None, "nextBlockerIds": [],
        "nextGroup": None, "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    save(RECEIPT, receipt)

    audit_ref, receipt_ref, decision_ref = bind(AUDIT), bind(RECEIPT), bind(decision_path)
    retained = sorted(set(prior_queue.get("separatelyRetainedHolds", [])) | set(prior_queue.get("currentReturnHeldIds", [])) | {SPELL})
    blockers = dict(prior_queue.get("currentReturnBlockers", {}))
    blockers[SPELL] = [BLOCKER]
    queue = dict(prior_queue)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-343", "recordedAtUtc": timestamp,
        "supersedesQueue": bind(A / "CURRENT_SPELL_QUEUE_342.json"),
        "currentAuthority": AUTHORITY, "pendingCount": 25, "acceptedUnapplied": 0,
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "nextGroup": None, "next": None, "nextPendingIds": [], "nextPendingCount": 0,
        "heldThisStep": [SPELL], "separatelyRetainedHolds": retained,
        "pendingIdentityAudit": PENDING.relative_to(ROOT).as_posix(),
        "currentHandoff": HANDOFF.relative_to(ROOT).as_posix(), "currentPacket": None,
        "currentPacketStatus": "RETURN343_WISH_HELD_FIRST_REVIEW_ORDER_EXHAUSTED_25_CLOSURE_TASKS_REMAIN",
        "activeReview": None, "currentReview": SPELL,
        "currentReturn": receipt_ref, "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref, "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref, "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": [SPELL],
        "currentReturnBlockers": blockers,
        "currentDirectorInstruction": "Return343 holds Wish / MR233-B02. MR343-W01 multiple substantive outcome contracts and W02 composite ordering/partial settlement/aftermath/resource lifecycle remain open; W03 legally acquired paid encounters across all four native class routes and meaningful adverse branches remains missing. First-review order is exhausted: 0 first-review identities and 25 closure tasks remain. The Director names no next priority. Its queue-status nextAction requires selecting a changed closure delta containing missing rules/facts and witnesses; do not automatically re-run unchanged holds. No application authorized. Return336-343 holds and AFP211-E01/MR233-E01 CLOSED remain unchanged.",
        "directorConnectionStatus": "Return343 independently verified. Wish remains held; supplied first-review order exhausted, 25 closure tasks remain, and Director next priority is null.",
        "applicationPerformed": False, "canonicalFilesChanged": False, "githubChanges": False,
    })
    save(QUEUE, queue)
    pending = dict(prior_pending)
    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-343",
        "recordedAtUtc": timestamp, "status": "PASS_CURRENT_823_25_RETURN343_WISH_HOLD_FIRST_REVIEW_ORDER_EXHAUSTED",
        "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_342.json", "authority": AUTHORITY,
        "pendingCount": 25, "acceptedIds": [], "appliedIds": [], "heldThisStep": [SPELL],
        "separatelyHeldIds": retained, "nextGroup": None, "nextIdentity": None,
        "nextBlockerIds": [], "nextPendingIds": [], "nextPendingCount": 0,
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "nextStep": "No first-review identity remains in the supplied order. Select a changed Director-prioritized closure delta with the missing source rules/facts and actual witnesses; do not re-run unchanged holds.",
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
        "id": "CURRENT-HANDOFF-343", "recordedAtUtc": timestamp,
        "supersedes": "CURRENT_HANDOFF_342.json", "status": "RETURN343_VERIFIED_WISH_HELD_FIRST_REVIEW_ORDER_EXHAUSTED_823_25_0",
        "authority": AUTHORITY, "queue": QUEUE.relative_to(ROOT).as_posix(),
        "queueBinding": bind(QUEUE), "pendingIdentityAudit": PENDING.name,
        "pendingIdentityAuditBinding": bind(PENDING), "currentDirectorReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref, "currentReturnAudit": audit_ref,
        "currentReturnArchive": archive_ref, "currentReturnDelivery": delivery_ref,
        "heldThisStep": [SPELL], "separatelyRetainedHolds": retained,
        "acceptedIds": [], "appliedIds": [], "applicationPerformed": False, "canonicalFilesChanged": False,
        "currentBlocker": None, "nextPendingGroup": None,
        "lastReviewedBlocker": {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP},
        "nextStep": "Select a changed closure delta for a Director-prioritized pending spell, with missing rules/facts and actual paid-use evidence; do not automatically repeat unchanged holds.",
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "Return343 sealed Wish HOLD. No first-review target remains in supplied order; 25 closure tasks remain; next Director priority is null.",
    })
    save(HANDOFF, handoff)
    SNAPSHOT.write_text(
        "# Spell review status — queue 343\n\n"
        f"Return343 independently verified {len(checks)}/{len(checks)} checks and holds Wish / MR233-B02. "
        "Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "Wish still needs multiple substantive outcome contracts, a composite ordering/settlement/aftermath and lifecycle contract, and legally acquired paid encounters covering all four native class routes with meaningful adverse branches. Return336-343 holds and AFP211-E01/MR233-E01 CLOSED remain unchanged; no application is authorized.\n\n"
        "The supplied first-review order is exhausted: **0 first-review identities remain; 25 closure tasks remain; next Director priority is null**. Select a changed closure delta with the missing rules/facts and witnesses; do not rerun unchanged holds.\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"status": "PASS", "checks": len(checks), "passed": sum(c["passed"] for c in checks), "failed": sum(not c["passed"] for c in checks), "archiveMembers": 44, "historicalSourceRowsIndependentlyVerified": 153, "held": SPELL, "authority": AUTHORITY, "firstReviewRemaining": 0, "closureTasksRemaining": 25, "next": None, "receipt": str(RECEIPT)}, indent=2))


if __name__ == "__main__":
    main()
