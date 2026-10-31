from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
PACKET = AUDIT / "rank9_conjure_demiplane_fortress_current_source_328_prepared"
ARCHIVE = PACKET / "DD_Rank9_ConjureDemiplaneFortress_CurrentSource_328.zip"
DELIVERY = PACKET / "DD_Rank9_ConjureDemiplaneFortress_CurrentSource_328_DELIVERY.json"
INDEPENDENT_AUDIT = AUDIT / "FORTRESS_PACKET_328_INDEPENDENT_AUDIT.json"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def readj(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: pathlib.Path):
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def main() -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    delivery = readj(DELIVERY)
    audit = readj(INDEPENDENT_AUDIT)
    assert delivery["status"] == "PREPARED_READBACK_PASS"
    assert delivery["scopeIds"] == ["conjure-demiplane-fortress"]
    assert audit["status"] == "PASS" and audit["failedChecks"] == 0
    receipt = {
        "id": "FORTRESS-PACKET-328-SUBMISSION-RECEIPT",
        "recordedAtUtc": now,
        "destination": "ChatGPT Director conversation: Calibration review part 6",
        "conversationUrl": URL,
        "status": "SENT_DIRECTOR_RESPONSE_PENDING",
        "submissionMethod": "User-authorized browser upload and message",
        "scopeIds": ["conjure-demiplane-fortress"],
        "blockerIds": ["PG200-B06"],
        "archive": bind(ARCHIVE),
        "delivery": bind(DELIVERY),
        "independentAudit": bind(INDEPENDENT_AUDIT),
        "authority": delivery["currentAuthority"],
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
    }
    receipt_path = AUDIT / "FORTRESS_PACKET_328_SUBMISSION_RECEIPT.json"
    receipt_path.write_bytes(pretty(receipt))

    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_328.json"
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_328.json"
    handoff_path = AUDIT / "CURRENT_HANDOFF_328.json"
    queue = readj(queue_path)
    queue.update({
        "recordedAtUtc": now,
        "activeReview": {"spellId": "conjure-demiplane-fortress", "blockerIds": ["PG200-B06"], "packet": bind(ARCHIVE), "status": "PACKET328_SUBMITTED_DIRECTOR_RESPONSE_PENDING"},
        "currentPacketStatus": "PACKET328_FORTRESS_SUBMITTED_DIRECTOR_RESPONSE_PENDING",
        "currentSubmission": bind(receipt_path),
        "currentPreparation": {"archive": bind(ARCHIVE), "delivery": bind(DELIVERY), "audit": bind(INDEPENDENT_AUDIT)},
        "directorConnectionStatus": "Packet328 uploaded and sent for Conjure Demiplane Fortress / PG200-B06-only review; awaiting sealed Director disposition.",
        "githubChanges": False,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    })
    queue_path.write_bytes(pretty(queue))
    pending = readj(pending_path)
    pending.update({
        "recordedAtUtc": now,
        "status": "PACKET328_FORTRESS_SUBMITTED_AWAITING_DIRECTOR",
        "currentQueueBinding": bind(queue_path),
        "currentSubmission": bind(receipt_path),
        "currentPreparation": {"archive": bind(ARCHIVE), "delivery": bind(DELIVERY), "audit": bind(INDEPENDENT_AUDIT)},
        "nextStep": "Await and independently audit Director's sealed Conjure Demiplane Fortress / PG200-B06-only disposition. Apply only exact identities expressly accepted and authorized in the sealed return.",
        "canonicalFilesChanged": False,
    })
    pending_path.write_bytes(pretty(pending))
    handoff = readj(handoff_path)
    handoff.update({
        "recordedAtUtc": now,
        "status": "PACKET328_FORTRESS_SUBMITTED_AWAITING_DIRECTOR",
        "queueBinding": bind(queue_path),
        "pendingIdentityAuditBinding": bind(pending_path),
        "currentPacketStatus": "PACKET328_FORTRESS_SUBMITTED_DIRECTOR_RESPONSE_PENDING",
        "currentPreparation": {"archive": bind(ARCHIVE), "delivery": bind(DELIVERY), "audit": bind(INDEPENDENT_AUDIT)},
        "currentSubmission": bind(receipt_path),
        "directorConnectionStatus": "Packet328 uploaded and sent to Director; await sealed Fortress-only disposition before moving to the next identity.",
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    })
    handoff_path.write_bytes(pretty(handoff))
    (AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_328.md").write_text(
        "# Current spell-review snapshot — Packet328 submitted\n\n"
        f"Recorded: {now}\n\n"
        "Authority remains **823 applied / 25 pending / 0 accepted-unapplied**, with **547 complete procedures / 173 scoped interfaces**. Return327 is independently verified; Banishment Gate remains held at PG200-B03/B04. Packet328 now asks Director to review only Conjure Demiplane Fortress / PG200-B06.\n\n"
        "Packet328 includes the sealed Return200 and Return284 blocker context, 14 preserved Fortress cases, current native procedure/catalog/index, current Wizard Arch Dispel source, and the bounded AC5 source comparison. The packet passed its independent readback audit before upload. Await the sealed Director decision; no canonical edits or application have occurred.\n",
        encoding="utf-8",
    )
    print(json.dumps({"receipt": str(receipt_path), "archiveSha256": receipt["archive"]["sha256"], "status": receipt["status"], "next": "conjure-demiplane-fortress"}, indent=2))


if __name__ == "__main__":
    main()
