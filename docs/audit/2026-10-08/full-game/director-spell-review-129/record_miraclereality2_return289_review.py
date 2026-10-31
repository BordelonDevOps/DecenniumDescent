#!/usr/bin/env python3
"""Record the audited Return289 and advance the ordinary-spell handoff."""
from __future__ import annotations

import hashlib
import json
import pathlib
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
AUDIT = BASE / "RANK9MIRACLEREALITY2_RETURN289_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9MIRACLEREALITY2_RETURN289_RECEIPT.json"
ARCHIVE = BASE / "rank9_miraclereality2_return289_received/DD_Rank9_MiracleReality2_Director_Return289_HELD.zip"
DELIVERY = BASE / "rank9_miraclereality2_return289_received/DD_Rank9_MiracleReality2_Director_Return289_HELD_DELIVERY.json"
QUEUE_OLD = BASE / "CURRENT_SPELL_QUEUE_289.json"
HANDOFF_OLD = BASE / "CURRENT_HANDOFF_289.json"
PENDING_OLD = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_289.json"
SUBMISSION = BASE / "RANK9MIRACLEREALITY2_PACKET_289_SUBMISSION.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path: pathlib.Path):
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}",
    }


def save(path: pathlib.Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


audit = load(AUDIT)
receipt = load(RECEIPT)
queue = load(QUEUE_OLD)
handoff = load(HANDOFF_OLD)
pending = load(PENDING_OLD)
submission = load(SUBMISSION)
if audit.get("status") != "PASS" or audit.get("checkCount") != 27 or audit.get("failedChecks") != 0:
    raise SystemExit("Return289 audit is not PASS 27/27")
if audit.get("authority", {}).get("reviewedApplied") != 816 or audit.get("authority", {}).get("pending") != 32:
    raise SystemExit("Return289 authority does not match 816/32")
if audit.get("heldIds") != ["divine-intervention-greater", "wish"] or audit.get("acceptedIds") or audit.get("appliedIds"):
    raise SystemExit("Return289 decision scope does not match the expected held pair")

now = datetime.now(timezone.utc).isoformat()
archive_record = sha(ARCHIVE)
delivery_record = sha(DELIVERY)
audit_record = sha(AUDIT)
receipt_record = sha(RECEIPT)
decision = {
    "return": 289,
    "decisionId": "RANK9-MIRACLE-REALITY2-DIRECTOR-RETURN289",
    "acceptedIds": [],
    "appliedIds": [],
    "heldIds": ["divine-intervention-greater", "wish"],
    "blockerIds": {"divine-intervention-greater": ["MR233-B01"], "wish": ["MR233-B02"]},
    "authority": {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173},
    "archive": archive_record,
    "deliveryManifest": delivery_record,
    "independentAudit": audit_record,
    "receipt": receipt_record,
}
priority = {
    "group": "rank9-memory-denial6",
    "pendingIds": ["mind-collapse"],
    "blockerIds": ["MD196-B01"],
    "queueBucket": "qualification-holds",
    "status": "WAIT_FOR_NEW_QUALIFYING_SOURCE_OR_ACQUISITION_EVIDENCE",
    "purpose": "Closure priority only; all 32 pending identities have completed first review. Do not repeat a held review without new source/acquisition evidence.",
    "directorReturn": 289,
}

# Snapshot 290 advances the status while retaining Return289 and all prior history.
queue["id"] = "SPELL-REVIEW-QUEUE-290"
queue["recordedAtUtc"] = now
queue["supersedesQueue"] = "SPELL-REVIEW-QUEUE-289"
queue["nextSuggestedGroups"] = [{"group": priority["group"], "pendingIds": priority["pendingIds"], "pendingCount": 1, "kind": "closure-priority", "requiresNewEvidence": True, "blockerIds": priority["blockerIds"]}]
queue["nextGroup"] = priority["group"]
queue["nextPendingIds"] = priority["pendingIds"]
queue["nextPendingCount"] = 1
queue["next"] = priority
queue["closureStatus"] = "ALL_32_PENDING_IDENTITIES_HAVE_COMPLETED_FIRST_REVIEW; 0 ACCEPTED; 0 ACCEPTED-UNAPPLIED; NEW EVIDENCE REQUIRED FOR CLOSURE"
queue["nextPreparedRequest"] = {**priority, "packetPrepared": False, "reason": "Director requires new qualifying source/acquisition evidence before repeating a held review."}
queue["latestReturn289"] = decision
queue["status"] = "RETURN289_INDEPENDENT_AUDIT_PASS_NO_ACCEPTANCE_816_32_0"
queue["packetStatus"] = queue["status"]
queue["firstReviewTasksRemaining"] = 0
queue["unreviewedPendingIds"] = []
queue["githubChanges"] = False
QUEUE_NEW = BASE / "CURRENT_SPELL_QUEUE_290.json"

pending["id"] = "CURRENT32-PENDING-IDENTITY-AUDIT-290"
pending["recordedAtUtc"] = now
pending["status"] = "RETURN289_AUDITED_PASS_NO_ACCEPTANCE_816_32_0"
pending["allCurrentPendingIdentitiesReviewed"] = True
pending["unreviewedPendingIds"] = []
pending["remainingPendingCount"] = 32
pending["latestReviewedBatch"] = decision
pending["latestHeldDecision"] = decision
pending["closureStatus"] = queue["closureStatus"]
pending["closurePriority"] = priority
pending["nextGroup"] = priority["group"]
pending["nextPendingIds"] = priority["pendingIds"]
pending["nextPendingCount"] = 1
pending["preparedNextGroup"] = {**priority, "status": priority["status"], "packetPrepared": False}
pending["currentReturn289"] = decision
pending["return289IndependentAudit"] = audit_record
pending["return289Receipt"] = receipt_record
PENDING_NEW = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_290.json"

submission["status"] = "RETURN289_INDEPENDENT_AUDIT_PASS_NO_ACCEPTANCE_816_32_0"
submission["sent"] = True
submission["acceptedIds"] = []
submission["appliedIds"] = []
submission["heldIds"] = decision["heldIds"]
submission["return289"] = decision
submission["directorProgress"] = (submission.get("directorProgress") or []) + [
    {"atUtc": now, "note": "Return289 sealed: 533 package checks and 3,344 source/data/replay checks pass; 26 questions and eight future requirements recorded. Both identities held; Director names mind-collapse/MD196-B01 as the next closure priority, conditional on new source/acquisition evidence."}
]
submission["remainingWork"] = queue["closureStatus"]
submission["nextClosurePriority"] = priority
save(SUBMISSION, submission)

pending["currentSubmission"] = {"path": SUBMISSION.relative_to(ROOT).as_posix(), **sha(SUBMISSION)}
save(PENDING_NEW, pending)
queue["pendingIdentityAudit"] = {"path": PENDING_NEW.relative_to(ROOT).as_posix(), **sha(PENDING_NEW)}
queue["currentPendingAudit"] = queue["pendingIdentityAudit"]
save(QUEUE_NEW, queue)

handoff["id"] = "CURRENT-ORDINARY-SPELL-REVIEW-HANDOFF-290"
handoff["recordedAtUtc"] = now
handoff["supersedes"] = "CURRENT_HANDOFF_289.json"
handoff["status"] = "RETURN289_AUDITED_PASS_NO_ACCEPTANCE_816_32; ALL_FIRST_REVIEW_TASKS_COMPLETE"
handoff["authority"] = decision["authority"]
handoff["currentAuthority"] = decision["authority"]
handoff["nextStep"] = "Obtain new qualifying source/acquisition evidence for mind-collapse / MD196-B01 before any closure re-review; then return to Director. All 32 pending identities have completed first review."
handoff["nextStepText"] = handoff["nextStep"]
handoff["nextGroup"] = priority["group"]
handoff["nextPendingIds"] = priority["pendingIds"]
handoff["nextPendingCount"] = 1
handoff["nextPendingGroup"] = priority
handoff["currentBlocker"] = {"identity": "mind-collapse", "blockerId": "MD196-B01", "missing": "authorized genuine inserted-full-turn feature, actual legal acquisition, and complete actor/grantor history while preserving the existing three regular ENDs, 6.205 admission, 7.900/13.900/19.900 ENDs, concentration/Ready, recharge/Reaction; event :11 at 6.300 is not a turn"}
handoff["firstReviewTasksRemaining"] = 0
handoff["allPendingIdentitiesReviewed"] = True
handoff["closurePriority"] = priority
handoff["directorConnectionStatus"] = "Return289 sealed and independently audited; Director states all first-review tasks are complete and closure requires new evidence."
handoff["currentReturn289"] = decision
handoff["currentReturnArchive"] = archive_record
handoff["currentReturnDelivery"] = delivery_record
handoff["currentReturnAudit"] = audit_record
handoff["currentReturnReceipt"] = receipt_record
handoff["currentReturnBinding"] = {"archive": archive_record, "delivery": delivery_record, "independentAudit": audit_record, "receipt": receipt_record}
handoff["currentSubmission"] = {"path": SUBMISSION.relative_to(ROOT).as_posix(), **sha(SUBMISSION)}
handoff["currentPacket"] = submission.get("archive")
handoff["currentPacketDelivery"] = submission.get("deliveryManifest")
handoff["currentPacketAudit"] = submission.get("independentAudit")
handoff["currentPacketAuditReceipt"] = submission.get("auditReceipt")
handoff["packetStatus"] = submission.get("status")
handoff["currentDirectorPosition"] = {
    "stage": "Return289 sealed and independently audited PASS 27/27; Director says the first-review sweep is complete.",
    "acceptedIds": [],
    "appliedIds": [],
    "heldIds": decision["heldIds"],
    "blockers": decision["blockerIds"],
    "nextPendingGroup": {"group": priority["group"], "pendingIds": priority["pendingIds"], "blockerIds": priority["blockerIds"], "conditionalOnNewEvidence": True},
}
handoff["directorProgress"] = (handoff.get("directorProgress") or []) + [
    {"atUtc": now, "note": "Return289 independently audited PASS 27/27. Held divine-intervention-greater/Wish under MR233-B01/B02. Director closure priority is mind-collapse/MD196-B01, conditional on new source/acquisition evidence; no first-review tasks remain."}
]
handoff["queue"] = {"path": QUEUE_NEW.relative_to(ROOT).as_posix(), **sha(QUEUE_NEW)}
handoff["queueBinding"] = handoff["queue"]
handoff["currentQueueBinding"] = handoff["queue"]
handoff["pendingIdentityAudit"] = {"path": PENDING_NEW.relative_to(ROOT).as_posix(), **sha(PENDING_NEW)}
handoff["githubChanges"] = False
handoff["canonicalRuntimeApplicationPerformed"] = False
HANDOFF_NEW = BASE / "CURRENT_HANDOFF_290.json"
save(HANDOFF_NEW, handoff)

snapshot = f"""# Current Ordinary Spell Review Snapshot 290

Authority: **816 reviewed/applied / 32 pending / 0 accepted-unapplied**; 540 complete standalone procedures and 173 scoped interfaces.

Return289 for **divine-intervention-greater** and **wish** is sealed and independently audited PASS (27/27). Both remain held under MR233-B01 and MR233-B02. Its ZIP has 132 members, 2,521,417 bytes, CRC32 `f2ceb843`, SHA-256 `bb8123ad2bf4cd4b1616c892c90b7b6a62f93bf88ebe7dbda653f273b7cf791c`; all 533 package checks and 3,344 source/data/replay checks pass. No acceptance, application, canonical changes, or runtime execution occurred.

The Director confirms **zero first-review tasks remain** across the 32 pending identities. Closure work requires new source/acquisition evidence. The next priority is **mind-collapse / MD196-B01**: an authorized feature that genuinely inserts a full turn, its legal acquisition, and complete actor/grantor history, while preserving the three regular ENDs at 7.900/13.900/19.900, the 6.205 admission, concentration/Ready, recharge/Reaction, and the 6.300 event boundary. Do not treat an extra Action or event :11 as an inserted turn.

Next artifacts: [handoff 290](CURRENT_HANDOFF_290.json), [queue 290](CURRENT_SPELL_QUEUE_290.json), [pending audit 290](CURRENT32_PENDING_IDENTITY_AUDIT_290.json), [Return289 audit](RANK9MIRACLEREALITY2_RETURN289_INDEPENDENT_AUDIT.json). The full current-review overlay is preserved in the same folder. No feat cohort or completed 16-spell cohort was reopened.
"""
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_290.md"
SNAPSHOT.write_text(snapshot, encoding="utf-8")

start = ROOT / "START_HERE.md"
start_text = start.read_text(encoding="utf-8-sig")
first_end = start_text.find("\n\n")
first = "**Current ordinary spell-review handoff [290](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_290.json):** Return289 independently audited PASS 27/27 and holds divine-intervention-greater / wish under MR233-B01/B02 at 816/32/0. GPT confirms all first reviews are complete; closure requires new source/acquisition evidence, with mind-collapse / MD196-B01 first. See [snapshot](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_290.md)."
if first_end < 0:
    raise SystemExit("START_HERE has no first paragraph boundary")
start.write_text(first + start_text[first_end:], encoding="utf-8")

print(json.dumps({"status": "RECORDED", "queue": QUEUE_NEW.relative_to(ROOT).as_posix(), "handoff": HANDOFF_NEW.relative_to(ROOT).as_posix(), "pendingAudit": PENDING_NEW.relative_to(ROOT).as_posix(), "snapshot": SNAPSHOT.relative_to(ROOT).as_posix(), "authority": decision["authority"], "next": priority}, ensure_ascii=False, indent=2))
