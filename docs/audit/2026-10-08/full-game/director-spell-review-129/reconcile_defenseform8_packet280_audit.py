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


audit_path = BASE / "RANK9_DEFENSEFORM8_PACKET280_INDEPENDENT_AUDIT.json"
receipt_path = BASE / "RANK9_DEFENSEFORM8_PACKET280_RECEIPT.json"
prep_path = BASE / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_280.json"
packet_path = BASE / "RANK9_DEFENSEFORM8_PACKET_280.json"
q_path = BASE / "CURRENT_SPELL_QUEUE_280.json"
h_path = BASE / "CURRENT_HANDOFF_280.json"
audit, receipt, prep, packet = (read(p.name) for p in (audit_path, receipt_path, prep_path, packet_path))
assert audit["status"] == receipt["status"] == "PASS" and audit["failedChecks"] == 0
assert prep["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_816_32_0"
assert packet["status"] == "PREPARED_UNSENT"
assert packet["pendingIds"] == ["elemental-shell", "timeless-form", "invulnerable-sphere"]
q, h = read(q_path.name), read(h_path.name)
authority = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
assert q["currentAuthority"] == h["currentAuthority"] == authority
assert q["nextGroup"] == "rank9-defense-form8"
assert q["nextPendingIds"] == ["elemental-shell", "timeless-form", "invulnerable-sphere"]

audit_binding = bind(audit_path)
receipt_binding = bind(receipt_path)
prep_binding = bind(prep_path)
packet_binding = prep["packet"]
delivery_binding = prep["deliveryManifest"]
for group in q.get("currentPendingGroups", []):
    if group.get("group") == "rank9-defense-form8":
        group.update({"status": "PACKET280_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                      "preparedPacket": packet_binding, "deliveryManifest": delivery_binding,
                      "preparation": prep_binding, "independentAudit": audit_binding,
                      "receipt": receipt_binding})
next_row = {"group": "rank9-defense-form8", "pendingIds": q["nextPendingIds"], "pendingCount": 3,
            "status": "PACKET280_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
            "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": packet_binding,
            "deliveryManifest": delivery_binding, "preparation": prep_binding,
            "independentAudit": audit_binding, "receipt": receipt_binding}
q.update({"id": "SPELL-REVIEW-QUEUE-280", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_DEFENSEFORM8_PACKET280_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "packetStatus": "RANK9_DEFENSEFORM8_PACKET280_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "currentPreparation": prep_binding, "currentPacket": packet_binding,
          "currentDeliveryManifest": delivery_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding, "next": next_row, "nextPreparedRequest": next_row,
          "nextSuggestedGroups": [next_row]})
write(q_path.name, q)
q_binding = bind(q_path)
h.update({"id": "CURRENT-HANDOFF-280", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_DEFENSEFORM8_PACKET280_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
          "queue": q_binding, "queueBinding": q_binding, "currentQueueBinding": q_binding,
          "currentPreparation": prep_binding, "currentPacket": packet_binding,
          "currentPacketDelivery": delivery_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding,
          "nextStep": "Send the independently audited Packet280 and matching current 816/32 queue, handoff and pending audit to the GPT Director; keep polling and ping if needed; independently audit any sealed decision and apply only exact accepted identities.",
          "resumePriority": "Packet280 is independently audited PASS (21/21) for exactly elemental-shell, timeless-form and invulnerable-sphere. GPT is the director; monitor, ping as needed, and apply only an exact independently audited acceptance."})
write(h_path.name, h)

snapshot = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_280.md"
snapshot.write_text(
    "# Current ordinary spell-review checkpoint 280\n\n"
    "Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.\n\n"
    "The Director held final-word under DR217-B01. The 16 preserved cases replayed, but the current evidence still lacks an eligible-victim/capture witness. The text-only ruling passed its local crosscheck; no sealed Return279 archive or delivery manifest was created.\n\n"
    "**Packet280 is ready and independently audited PASS (21/21).** It covers only Defense/Form8: elemental-shell (DF218-B01/B02), timeless-form (DF218-B03), and invulnerable-sphere (DF218-B04). It refreshes all 87 current source bindings and preserves 46 prior target cases. The Director has not reviewed Packet280 yet.\n\n"
    "See [handoff](CURRENT_HANDOFF_280.json), [queue](CURRENT_SPELL_QUEUE_280.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_280.json), [preparation](RANK9_DEFENSEFORM8_SOURCE_PREPARATION_280.json), and [independent audit](RANK9_DEFENSEFORM8_PACKET280_INDEPENDENT_AUDIT.json).\n",
    encoding="utf-8")

start = ROOT / "START_HERE.md"
old = start.read_text(encoding="utf-8-sig")
first, sep, rest = old.partition("\n\n")
if "Current ordinary spell-review handoff [280]" in first:
    start.write_text(
        "**Current ordinary spell-review handoff [280](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_280.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. Packet280 is independently audited PASS (21/21) for Defense/Form8. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_PACKET_280.json) and [audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_PACKET280_INDEPENDENT_AUDIT.json).\n\n"
        + rest, encoding="utf-8", newline="\n")

print(json.dumps({"authority": authority, "packet": packet_binding,
                  "independentAudit": audit_binding, "receipt": receipt_binding,
                  "queue": bind(q_path), "handoff": bind(h_path)}, indent=2))
