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
            "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8-sig"))


def write(name: str, value) -> None:
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


audit_path = BASE / "RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json"
receipt_path = BASE / "RANK9_WARDCONTROL6_PACKET281_RECEIPT.json"
prep_path = BASE / "RANK9_WARDCONTROL6_SOURCE_PREPARATION_281.json"
packet_path = BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip"
delivery_path = packet_path.with_name("DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json")
q_path = BASE / "CURRENT_SPELL_QUEUE_281.json"
h_path = BASE / "CURRENT_HANDOFF_281.json"
audit, receipt, prep, q, h = (read(p.name) for p in (audit_path, receipt_path, prep_path, q_path, h_path))
assert audit["status"] == receipt["status"] == "PASS" and audit["failedChecks"] == 0
assert audit["checkCount"] == audit["passedChecks"] == 17
assert prep["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT" and prep["checksFailed"] == 0
authority = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
targets = ["nullification-wave", "reality-anchor"]
assert q["currentAuthority"] == h["currentAuthority"] == authority
assert q["nextGroup"] == h["nextGroup"] == "rank9-ward-control6"
assert q["nextPendingIds"] == h["nextPendingIds"] == targets

audit_binding = bind(audit_path)
receipt_binding = bind(receipt_path)
prep_binding = bind(prep_path)
packet_binding = bind(packet_path)
delivery_binding = bind(delivery_path)
next_row = {"group": "rank9-ward-control6", "pendingIds": targets, "pendingCount": 2,
            "status": "PACKET281_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
            "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": packet_binding,
            "deliveryManifest": delivery_binding, "preparation": prep_binding,
            "independentAudit": audit_binding, "receipt": receipt_binding}
for group in q.get("currentPendingGroups", []):
    if group.get("group") == "rank9-ward-control6":
        group.update({k: v for k, v in next_row.items() if k != "group"})
q.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_WARDCONTROL6_PACKET281_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "packetStatus": "RANK9_WARDCONTROL6_PACKET281_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "currentPreparation": prep_binding, "currentPacket": packet_binding,
          "currentDeliveryManifest": delivery_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding, "next": next_row, "nextPreparedRequest": next_row,
          "nextSuggestedGroups": [next_row]})
write(q_path.name, q)
q_binding = bind(q_path)
h.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_WARDCONTROL6_PACKET281_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "queue": q_binding, "queueBinding": q_binding, "currentQueueBinding": q_binding,
          "currentPreparation": prep_binding, "currentPacket": packet_binding,
          "currentPacketDelivery": delivery_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding,
          "nextStep": "Send the independently audited Packet281 and matching current 816/32 queue, handoff and pending audit to the GPT Director; keep polling and ping as needed; independently audit any sealed decision and apply only exact accepted identities.",
          "resumePriority": "Packet281 is independently audited PASS (17/17) for exactly nullification-wave and reality-anchor. GPT is the director; monitor, ping as needed, and apply only an exact independently audited acceptance."})
write(h_path.name, h)

snapshot = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_281.md"
snapshot.write_text(
    "# Current ordinary spell-review checkpoint 281\n\n"
    "Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.\n\n"
    "Return280 held Defense/Form8: elemental-shell (DF218-B01/B02), timeless-form (DF218-B03), and invulnerable-sphere (DF218-B04). Its corrected archive and delivery pass a 15-check independent audit; 46 preserved cases replayed, with no acceptance or application.\n\n"
    "**Packet281 is prepared and independently audited PASS (17/17)** for exactly Ward/Control6: nullification-wave (WC188-B01) and reality-anchor (WC188-B02), using 91 refreshed source bindings. It has not yet been sent to the Director.\n\n"
    "See [handoff](CURRENT_HANDOFF_281.json), [queue](CURRENT_SPELL_QUEUE_281.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_281.json), [preparation](RANK9_WARDCONTROL6_SOURCE_PREPARATION_281.json), [packet audit](RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json), and [receipt](RANK9_WARDCONTROL6_PACKET281_RECEIPT.json).\n",
    encoding="utf-8")

start = ROOT / "START_HERE.md"
old = start.read_text(encoding="utf-8-sig")
first, sep, rest = old.partition("\n\n")
if "Current ordinary spell-review handoff [281]" in first:
    start.write_text(
        "**Current ordinary spell-review handoff [281](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_281.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. Packet281 is independently audited PASS (17/17) for Ward/Control6. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip) and [audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json).\n\n"
        + rest, encoding="utf-8", newline="\n")

print(json.dumps({"authority": authority, "packet": packet_binding,
                  "delivery": delivery_binding, "independentAudit": audit_binding,
                  "receipt": receipt_binding, "queue": bind(q_path), "handoff": bind(h_path)}, indent=2))
