from __future__ import annotations

import copy
import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def enc(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    prep = read(BASE / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_236.json")
    audit = read(BASE / "RANK9_DEFENSEFORM8_PACKET236_INDEPENDENT_AUDIT.json")
    receipt = read(BASE / "RANK9_DEFENSEFORM8_PACKET236_RECEIPT.json")
    assert prep["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37_0"
    assert audit["status"] == receipt["status"] == "PASS" and audit["failedChecks"] == receipt["failedChecks"] == 0
    archive = BASE / "rank9_defenseform8_current_source_236_prepared/DD_Rank9_DefenseForm8_CurrentSource_236.zip"
    delivery = BASE / "rank9_defenseform8_current_source_236_prepared/DD_Rank9_DefenseForm8_CurrentSource_236_DELIVERY.json"
    assert info(archive)["sha256"] == prep["packet"]["sha256"] and info(delivery)["sha256"] == prep["deliveryManifest"]["sha256"]
    packet, delivery_info = info(archive), info(delivery)
    audit_info, receipt_info = info(BASE / "RANK9_DEFENSEFORM8_PACKET236_INDEPENDENT_AUDIT.json"), info(BASE / "RANK9_DEFENSEFORM8_PACKET236_RECEIPT.json")
    submission = {
        "id": "RANK9DEFENSEFORM8-PACKET236-SUBMISSION",
        "recordedAtUtc": now,
        "status": "PACKET236_SUBMITTED_GPT_PENDING_811_37_0",
        "group": "rank9-defense-form8",
        "targetIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
        "authority": prep["sourceAuthority"],
        "archive": packet,
        "deliveryManifest": delivery_info,
        "independentAudit": audit_info,
        "auditReceipt": receipt_info,
        "auditStatus": "PASS",
        "auditChecks": audit["checkCount"],
        "auditFailures": 0,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [],
        "destination": "Calibration review part 6",
        "browserVerified": True,
        "submittedAtUtc": now,
        "githubChanges": False,
    }
    submission_path = BASE / "RANK9_DEFENSEFORM8_PACKET_236_SUBMISSION.json"
    submission_path.write_text(enc(submission), encoding="utf-8")

    p_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_236.json"
    p = read(p_path)
    p["status"] = "PACKET236_SUBMITTED_GPT_PENDING_811_37_0"
    p["preparedNextGroup"].update({"status": p["status"], "packet": packet, "deliveryManifest": delivery_info, "independentAudit": audit_info, "auditReceipt": receipt_info, "submittedAtUtc": now})
    p["lastSubmittedPacket"] = {"group": submission["group"], "targetIds": submission["targetIds"], "archive": packet, "deliveryManifest": delivery_info, "independentAudit": audit_info, "receipt": receipt_info, "acceptedIds": [], "appliedIds": []}
    p_path.write_text(enc(p), encoding="utf-8")

    q_path = BASE / "CURRENT_SPELL_QUEUE_236.json"
    q = read(q_path)
    q["recordedAtUtc"] = now
    q["status"] = q["packetStatus"] = submission["status"]
    q["pendingIdentityAudit"] = info(p_path)
    q["currentPacket"] = packet
    q["currentDeliveryManifest"] = delivery_info
    q["currentPacketDelivery"] = delivery_info
    q["currentPacketAudit"] = audit_info
    q["currentPacketAuditReceipt"] = receipt_info
    q["currentPacketAuditStatus"] = "PASS"
    q["currentPacketAuditChecks"] = audit["checkCount"]
    q["currentPacketAuditFailures"] = 0
    q["sourcePreparation"] = info(BASE / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_236.json")
    q["currentSubmission"] = info(submission_path)
    q["submittedAtUtc"] = now
    q["githubChanges"] = False
    row = next(x for x in q["currentPendingGroups"] if x["group"] == submission["group"])
    row["status"] = submission["status"]
    row["freshPacketRequiredForCurrentAuthority"] = True
    q_path.write_text(enc(q), encoding="utf-8")

    h_path = BASE / "CURRENT_HANDOFF_236.json"
    h = read(h_path)
    h["recordedAtUtc"] = now
    h["status"] = submission["status"]
    h["pendingIdentityAudit"] = info(p_path)
    h["queue"] = info(q_path)
    h["currentQueueBinding"] = info(q_path)
    h["currentPacket"] = packet
    h["currentPacketDelivery"] = delivery_info
    h["currentPacketAudit"] = audit_info
    h["currentPacketAuditReceipt"] = receipt_info
    h["packetAuditStatus"] = "PASS"
    h["packetAuditChecks"] = audit["checkCount"]
    h["packetAuditFailures"] = 0
    h["sourcePreparation"] = info(BASE / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_236.json")
    h["currentSubmission"] = info(submission_path)
    h["submittedAtUtc"] = now
    h["nextStep"] = "GPT director is reviewing Packet236. Keep monitoring Calibration review part 6 and ping if it stalls; independently audit the sealed return before applying exact accepted identities."
    h["resumePriority"] = "Packet236 for elemental-shell, timeless-form and invulnerable-sphere is submitted and independently passed 16 checks. Monitor the browser and ping as needed; audit the sealed decision before any exact application."
    h_path.write_text(enc(h), encoding="utf-8")
    print(json.dumps({"status": submission["status"], "submission": info(submission_path), "queue": info(q_path), "handoff": info(h_path), "pendingAudit": info(p_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
