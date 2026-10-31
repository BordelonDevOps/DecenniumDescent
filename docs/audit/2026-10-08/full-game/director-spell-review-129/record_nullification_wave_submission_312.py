from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_wardcontrol6_source_packet_312_prepared"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
MESSAGE = (
    "Packet 312 is attached and independently audited PASS (11 checks, 0 failures). Adjudicate only Nullification Wave / WC188-B01 at 822 applied / 26 pending / 0 accepted-unapplied. Reality Anchor / WC188-B02 is separate and remains next; do not include it in this decision. The packet refreshes all 91 Ward/Control source bindings, preserves old hashes and the exact Return281 Wave procedure/blocker/qualifications/source-pair/actor files and 18 Wave cases, and binds the Glove of Null Ink sources plus the accepted Eternal Forge envelope and draft W2 supplement/audit as leads only. Please determine from the bound sources whether either component supports the required source-authorized continuing permanent property and complete terminal/remainder contract. Do not infer that finite inscription expiry or Forge-root termination proves removability. If the exact eligible component, legal acquired actor/custodian, and paid Wave witness are not fully supported, retain WC188-B01 with the narrowest remaining evidence; do not invent history or change conditional records. Return the sealed decision ZIP and exact DELIVERY.json, then confirm acceptedIds, appliedIds, heldIds, authority, next order, and remaining count."
)


def file_binding(path: pathlib.Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    packet = OUT / "DD_Rank9_WardControl6_CurrentSource_312.zip"
    delivery = OUT / "DD_Rank9_WardControl6_CurrentSource_312_DELIVERY.json"
    audit_path = A / "NULLIFICATION_WAVE_PACKET_312_INDEPENDENT_AUDIT.json"
    req_path = A / "NULLIFICATION_WAVE_DIRECTOR_REQUIREMENTS_312.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8-sig"))
    delivered = json.loads(delivery.read_text(encoding="utf-8-sig"))
    assert audit["status"] == "PASS" and audit["failedChecks"] == 0
    assert hashlib.sha256(packet.read_bytes()).hexdigest() == delivered["archive"]["sha256"]
    attached = {"packet": file_binding(packet), "delivery": file_binding(delivery),
                "independentAudit": file_binding(audit_path), "directorRequirements": file_binding(req_path)}
    receipt = {
        "id": "NULLIFICATION-WAVE-PACKET312-SUBMISSION-RECEIPT",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "SUBMITTED_WAITING_FOR_DIRECTOR_DECISION",
        "destination": {"service": "ChatGPT", "chatTitle": "Calibration review part 6", "url": CHAT},
        "scopeIds": ["nullification-wave"], "blockerIds": ["WC188-B01"],
        "separateNext": {"identity": "reality-anchor", "blockerId": "WC188-B02", "jointPacket": False},
        "authority": delivered["authority"], "attachments": attached,
        "packetArchive": delivered["archive"],
        "independentAudit": {"status": audit["status"], "checkCount": audit["checkCount"], "failedChecks": audit["failedChecks"]},
        "message": MESSAGE,
        "submissionEvidence": "The Director chat displayed all four attachment names and the sent message, then showed Working.",
        "acceptedIds": [], "appliedIds": [], "canonicalFilesChanged": False,
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
    }
    receipt_path = A / "NULLIFICATION_WAVE_PACKET_312_SUBMISSION_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    queue = json.loads((A / "CURRENT_SPELL_QUEUE_312.json").read_text(encoding="utf-8-sig"))
    queue["id"] = "SPELL-REVIEW-QUEUE-313"
    queue["recordedAtUtc"] = receipt["recordedAtUtc"]
    queue["supersedesQueue"] = file_binding(A / "CURRENT_SPELL_QUEUE_312.json")
    queue["status"] = "NULLIFICATION_WAVE_PACKET_312_SUBMITTED_WAITING_FOR_DIRECTOR"
    queue["currentPacket"] = attached["packet"]
    queue["currentPacketDelivery"] = attached["delivery"]
    queue["currentPacketAudit"] = attached["independentAudit"]
    queue["currentSubmission"] = file_binding(receipt_path)
    queue["currentPreparation"] = queue.get("currentPreparation")
    queue["directorConnectionStatus"] = "Packet312 submitted; checking Director response for adjudication."
    queue_path = A / "CURRENT_SPELL_QUEUE_313.json"
    queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    handoff = {
        "id": "CURRENT-HANDOFF-313", "recordedAtUtc": receipt["recordedAtUtc"],
        "supersedes": file_binding(A / "CURRENT_HANDOFF_312.json"),
        "status": "NULLIFICATION_WAVE_PACKET_312_SUBMITTED_WAITING_FOR_DIRECTOR",
        "authority": delivered["authority"], "scopeIds": ["nullification-wave"], "blockerIds": ["WC188-B01"],
        "queue": queue_path.relative_to(ROOT).as_posix(), "queueBinding": file_binding(queue_path),
        "currentPacket": attached["packet"], "currentDelivery": attached["delivery"],
        "currentIndependentAudit": attached["independentAudit"], "currentSubmissionReceipt": file_binding(receipt_path),
        "acceptedIds": [], "appliedIds": [], "heldIdsIfUnresolved": ["nullification-wave"],
        "nextPendingGroup": queue["next"], "currentBlocker": {"identity": "nullification-wave", "blockerIds": ["WC188-B01"]},
        "nextStep": "Continue monitoring GPT. Independently audit Return312 and apply only exact accepted IDs; otherwise record the narrow hold and follow its next order.",
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False, "applicationPerformed": False, "githubChanges": False,
    }
    handoff_path = A / "CURRENT_HANDOFF_313.json"
    handoff_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    snapshot = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_313.md"
    snapshot.write_text(
        "# Current spell review snapshot 313\n\n"
        "Authority remains **822 reviewed/applied / 26 pending / 0 accepted-unapplied**, with **546 complete standalone procedures / 173 scoped interfaces**. Packet312 was independently audited PASS and submitted for **Nullification Wave / WC188-B01 only**. **Reality Anchor / WC188-B02 remains separate and next.**\n\n"
        "The packet refreshes 91 Ward/Control source bindings, preserves the prior hashes and exact Return281 Wave procedure, obligations, qualifications, source-pair table, actor profiles, and 18 Wave case files, and binds the Glove of Null Ink and Eternal Forge W2 leads without treating either as established closure evidence.\n\n"
        "The Director is reviewing Packet312. No acceptance, application, or canonical mutation has occurred. There are **26 closure tasks remaining and zero first-review tasks**.\n",
        encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": file_binding(receipt_path),
                      "queue": file_binding(queue_path), "handoff": file_binding(handoff_path)}, indent=2))


if __name__ == "__main__":
    main()
