from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP = "rank9-knowledge-revelation5"
IDS = ["faction-omniscience-supreme"]
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
PACKET = BASE / "rank9_knowledgerevelation5_current_source_283_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_283.zip"
DELIVERY = PACKET.with_name("DD_Rank9_KnowledgeRevelation5_CurrentSource_283_DELIVERY.json")
PREP = BASE / "RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_283.json"
AUDIT = BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_283_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_KNOWLEDGEREVELATION5_PACKET_283_RECEIPT.json"
RECORD = BASE / "RANK9KNOWLEDGEREVELATION5_PACKET_283.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_283.json"
HANDOFF = BASE / "CURRENT_HANDOFF_283.json"
PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_283.json"


def bind(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


audit, receipt, prep, delivery, record = (read(p) for p in (AUDIT, RECEIPT, PREP, DELIVERY, RECORD))
queue, handoff, pending = (read(p) for p in (QUEUE, HANDOFF, PENDING))
assert audit["status"] == receipt["status"] == "PASS" and audit["checksFailed"] == 0
assert audit["authority"] == receipt["authority"] == prep["sourceAuthority"] == delivery["sourceAuthority"] == AUTH
assert audit["heldIds"] == receipt["pendingIds"] == delivery["pendingIds"] == IDS
assert audit["acceptedIds"] == []
assert queue["currentAuthority"] == handoff["currentAuthority"] == pending["authority"] == AUTH
assert queue["nextGroup"] == handoff["nextGroup"] == GROUP and pending["pendingCount"] == 32

packet_binding, delivery_binding = bind(PACKET), bind(DELIVERY)
prep_binding, audit_binding, receipt_binding = bind(PREP), bind(AUDIT), bind(RECEIPT)
record.update({"status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT", "independentAudit": audit_binding,
               "receipt": receipt_binding, "sourcePreparation": prep_binding})
write(RECORD, record)
record_binding = bind(RECORD)
request = {"group": GROUP, "pendingIds": IDS, "pendingCount": 1,
           "status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT",
           "freshPacketRequiredForCurrentAuthority": False, "packet": packet_binding,
           "deliveryManifest": delivery_binding, "packetRecord": record_binding,
           "sourcePreparation": prep_binding, "independentAudit": audit_binding, "receipt": receipt_binding}

for row in queue.get("currentPendingGroups", []):
    if row.get("group") == GROUP:
        row.update({"status": "PACKET283_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                    "freshPacketRequiredForCurrentAuthority": False, "packet": packet_binding,
                    "deliveryManifest": delivery_binding, "packetRecord": record_binding,
                    "sourcePreparation": prep_binding, "independentAudit": audit_binding, "receipt": receipt_binding})
queue.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
              "status": "RANK9_KNOWLEDGE_REVELATION5_PACKET283_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
              "packetStatus": "RANK9_KNOWLEDGE_REVELATION5_PACKET283_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
              "currentPreparation": prep_binding, "currentPacket": packet_binding,
              "currentDeliveryManifest": delivery_binding, "currentPacketDelivery": delivery_binding,
              "currentPacketRecord": record_binding, "currentIndependentAudit": audit_binding,
              "currentReceipt": receipt_binding, "next": request, "nextPreparedRequest": request,
              "nextGroup": GROUP, "nextPendingIds": IDS, "nextSuggestedGroups": [request]})
write(QUEUE, queue)

pending.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                "status": "KNOWLEDGE_REVELATION5_PACKET283_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "pendingCount": 1,
                                      "status": "PACKET283_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                                      "preparation": prep_binding, "independentAudit": audit_binding,
                                      "receipt": receipt_binding, "freshPacketRequiredForCurrentAuthority": False}})
write(PENDING, pending)
pending_binding = bind(PENDING)
queue["pendingIdentityAudit"] = queue["currentPendingAudit"] = pending_binding
write(QUEUE, queue)
queue_binding = bind(QUEUE)

handoff.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                "status": "RANK9_TIMEFATE6_RETURN282_AUDITED_NEXT_KNOWLEDGE_REVELATION5_PACKET283_AUDITED_816_32",
                "currentAuthority": AUTH, "currentQueueBinding": queue_binding,
                "queue": queue_binding, "queueBinding": queue_binding,
                "pendingIdentityAudit": pending_binding, "currentPreparation": prep_binding,
                "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
                "currentPacketRecord": record_binding, "currentIndependentAudit": audit_binding,
                "currentReceipt": receipt_binding,
                "nextStep": {"group": GROUP, "pendingIds": IDS, "pendingCount": 1,
                             "status": "PACKET283_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32"},
                "nextStepText": "Send independently audited Packet283 and its matching delivery manifest, queue, handoff, and pending audit to the GPT Director. Keep checking the Director, audit the sealed return, and apply only exact acceptances.",
                "resumePriority": "Upload Packet283 plus its delivery manifest and Return198 witness supplement; review only faction-omniscience-supreme; preserve current holds and 816/32 authority."})
write(HANDOFF, handoff)

snapshot = ("# Current ordinary spell-review checkpoint 283\n\n"
            "Return282 passed independent audit (79/79) with all four Time/Fate6 spells held and unapplied. "
            "Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.\n\n"
            "Packet283 passed independent audit (9/9) for only `faction-omniscience-supreme` under KR198-B01. It contains 126 refreshed source bindings, all eight preserved target cases, the Return198 witness supplement, and current Return279–282 hold context. No canonical spell changes or applications occurred.\n\n"
            "See [handoff](CURRENT_HANDOFF_283.json), [queue](CURRENT_SPELL_QUEUE_283.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_283.json), [packet](rank9_knowledgerevelation5_current_source_283_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_283.zip), and [independent audit](RANK9KNOWLEDGEREVELATION5_PACKET_283_INDEPENDENT_AUDIT.json).\n")
(BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_283.md").write_text(snapshot, encoding="utf-8", newline="\n")

start = ROOT / "START_HERE.md"
old = start.read_text(encoding="utf-8-sig")
first, _, rest = old.partition("\n\n")
new_first = ("**Current ordinary spell-review handoff [283](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_283.json):** "
             "authority is 816 applied / 32 pending / 0 accepted-unapplied. Packet283 is independently audited PASS (9/9) for faction-omniscience-supreme. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_knowledgerevelation5_current_source_283_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_283.zip) and [audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9KNOWLEDGEREVELATION5_PACKET_283_INDEPENDENT_AUDIT.json).")
start.write_text(new_first + "\n\n" + rest, encoding="utf-8", newline="\n")
print(json.dumps({"status": audit["status"], "checks": audit["checksPassed"], "authority": AUTH,
                  "group": GROUP, "packet": packet_binding, "queue": queue_binding,
                  "handoff": bind(HANDOFF), "pendingAudit": pending_binding}, indent=2))
