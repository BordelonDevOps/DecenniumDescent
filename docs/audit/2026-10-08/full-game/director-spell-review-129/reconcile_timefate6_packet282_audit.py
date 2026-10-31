from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def bind(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


packet_path = BASE / "rank9_timefate6_current_source_282_prepared/DD_Rank9_TimeFate6_CurrentSource_282.zip"
delivery_path = packet_path.with_name("DD_Rank9_TimeFate6_CurrentSource_282_DELIVERY.json")
prep_path = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_282.json"
audit_path = BASE / "RANK9_TIMEFATE6_PACKET282_INDEPENDENT_AUDIT.json"
receipt_path = BASE / "RANK9_TIMEFATE6_PACKET282_RECEIPT.json"
record_path = BASE / "RANK9_TIMEFATE6_PACKET_282.json"
q_path = BASE / "CURRENT_SPELL_QUEUE_282.json"
h_path = BASE / "CURRENT_HANDOFF_282.json"
p_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_282.json"
audit, receipt, prep, delivery, record = (read(p) for p in (audit_path, receipt_path, prep_path, delivery_path, record_path))
q, h, pending = read(q_path), read(h_path), read(p_path)
authority = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
ids = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
assert audit["status"] == receipt["status"] == "PASS" and audit["checkCount"] == 12 and audit["failedChecks"] == 0
assert prep["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT" and prep["checksPassed"] == 10 and prep["checksFailed"] == 0
assert delivery["status"] == record["status"] == "PREPARED_UNSENT"
assert delivery["sourceAuthority"] == q["currentAuthority"] == h["currentAuthority"] == pending["authority"] == authority
assert delivery["pendingIds"] == q["nextPendingIds"] == ids and q["nextGroup"] == h["nextGroup"] == "rank9-time-fate6"

packet_binding, delivery_binding = bind(packet_path), bind(delivery_path)
prep_binding, audit_binding, receipt_binding, record_binding = bind(prep_path), bind(audit_path), bind(receipt_path), bind(record_path)
next_row = {"group": "rank9-time-fate6", "pendingIds": ids, "pendingCount": 4,
            "status": "PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
            "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": packet_binding,
            "deliveryManifest": delivery_binding, "packetRecord": record_binding,
            "preparation": prep_binding, "independentAudit": audit_binding, "receipt": receipt_binding}
for row in q.get("currentPendingGroups", []):
    if row.get("group") == "rank9-time-fate6":
        row.update({k: v for k, v in next_row.items() if k != "group"})
q.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_TIMEFATE6_PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "packetStatus": "RANK9_TIMEFATE6_PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "currentPreparation": prep_binding, "currentPacket": packet_binding,
          "currentDeliveryManifest": delivery_binding, "currentPacketDelivery": delivery_binding,
          "currentPacketRecord": record_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding, "next": next_row,
          "nextPreparedRequest": {"group": "rank9-time-fate6", "pendingIds": ids,
                                   "status": "PREPARED_UNSENT", "request": bind(BASE / "rank9_timefate6_current_source_282_prepared/REQUEST_282.txt")},
          "nextSuggestedGroups": [next_row]})

pending.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                "status": "TIMEFATE6_PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                "preparedNextGroup": {"group": "rank9-time-fate6", "pendingIds": ids, "pendingCount": 4,
                                      "status": "PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                                      "preparation": prep_binding, "independentAudit": audit_binding,
                                      "receipt": receipt_binding, "freshPacketRequiredForCurrentAuthority": False}})
write(p_path, pending)
pending_binding = bind(p_path)
q["pendingIdentityAudit"] = q["currentPendingAudit"] = pending_binding
write(q_path, q)
queue_binding = bind(q_path)
h.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_TIMEFATE6_PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "queue": queue_binding, "queueBinding": queue_binding, "currentQueueBinding": queue_binding,
          "pendingIdentityAudit": pending_binding, "currentPreparation": prep_binding,
          "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
          "currentPacketRecord": record_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding,
          "nextStep": {"group": "rank9-time-fate6", "pendingIds": ids, "pendingCount": 4,
                       "status": "PACKET282_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32"},
          "nextStepText": "Send independently audited Packet282 and matching current 816/32 queue, handoff and pending audit to the GPT Director; keep polling and ping as needed; audit any sealed ruling and apply only exact acceptances."})
write(h_path, h)

(BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_282.md").write_text(
    "# Current ordinary spell-review checkpoint 282\n\n"
    "Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces. Return281 held nullification-wave (WC188-B01) and reality-anchor (WC188-B02) after a 17/17 independent audit; no acceptance or application occurred.\n\n"
    "**Packet282 is prepared and independently audited PASS (12/12)** for only Time/Fate6: time-stop (TF192-B01), fate-rewrite (TF192-B04), collapse-timeline (TF192-B05) and eternal-prophecy (TF192-B02). All 140 current source bindings were refreshed, and Return221 plus Return281/Packet281 evidence are preserved. The Director has not reviewed Packet282 yet.\n\n"
    "See [handoff](CURRENT_HANDOFF_282.json), [queue](CURRENT_SPELL_QUEUE_282.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_282.json), [preparation](RANK9_TIMEFATE6_SOURCE_PREPARATION_282.json), [packet audit](RANK9_TIMEFATE6_PACKET282_INDEPENDENT_AUDIT.json), and [receipt](RANK9_TIMEFATE6_PACKET282_RECEIPT.json).\n",
    encoding="utf-8")
start = ROOT / "START_HERE.md"
old = start.read_text(encoding="utf-8-sig")
first, _, rest = old.partition("\n\n")
if "Current ordinary spell-review handoff [282]" in first:
    start.write_text("**Current ordinary spell-review handoff [282](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_282.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. Packet282 is independently audited PASS (12/12) for Time/Fate6. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_timefate6_current_source_282_prepared/DD_Rank9_TimeFate6_CurrentSource_282.zip) and [audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_PACKET282_INDEPENDENT_AUDIT.json).\n\n" + rest,
                          encoding="utf-8", newline="\n")
print(json.dumps({"authority": authority, "group": "rank9-time-fate6", "pendingIds": ids,
                  "packet": packet_binding, "delivery": delivery_binding, "audit": audit_binding,
                  "receipt": receipt_binding, "queue": bind(q_path), "handoff": bind(h_path),
                  "pendingAudit": bind(p_path)}, indent=2))
