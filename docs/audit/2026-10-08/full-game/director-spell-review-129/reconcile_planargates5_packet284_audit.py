from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_planargates5_current_source_284_prepared"
ARCHIVE = OUT / "DD_Rank9_PlanarGates5_CurrentSource_284.zip"
DELIVERY = OUT / "DD_Rank9_PlanarGates5_CurrentSource_284_DELIVERY.json"
PREPARATION = BASE / "RANK9PLANARGATES5_SOURCE_PREPARATION_284.json"
AUDIT = BASE / "RANK9PLANARGATES5_PACKET_284_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9PLANARGATES5_PACKET_284_RECEIPT.json"
RECORD = BASE / "RANK9PLANARGATES5_PACKET_284.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_284.json"
HANDOFF = BASE / "CURRENT_HANDOFF_284.json"
PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_284.json"
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_284.md"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
IDS = ["banishment-gate", "conjure-demiplane-fortress"]
GROUP = "rank9-planar-gates5"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    audit, receipt, prep, delivery, record = (read(p) for p in (AUDIT, RECEIPT, PREPARATION, DELIVERY, RECORD))
    queue, handoff, pending = (read(p) for p in (QUEUE, HANDOFF, PENDING))
    assert audit["status"] == receipt["status"] == prep["status"] == "PASS"
    assert audit["checksPassed"] == 14 and audit["checksFailed"] == 0 and receipt["checksFailed"] == 0
    assert audit["authority"] == receipt["authority"] == prep["sourceAuthority"] == delivery["sourceAuthority"] == AUTH
    assert audit["pendingIds"] == receipt["pendingIds"] == delivery["pendingIds"] == IDS
    assert pending["pendingCount"] == 32 and all(x in pending["pendingIds"] for x in IDS)
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTH
    assert ARCHIVE.exists() and delivery["archive"]["sha256"] == binding(ARCHIVE)["sha256"]

    archive_binding, delivery_binding = binding(ARCHIVE), binding(DELIVERY)
    prep_binding, audit_binding, receipt_binding = binding(PREPARATION), binding(AUDIT), binding(RECEIPT)
    record.update({"status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT", "archive": archive_binding,
                   "deliveryManifest": delivery_binding, "sourcePreparation": prep_binding,
                   "independentAudit": audit_binding, "receipt": receipt_binding})
    write(RECORD, record)
    record_binding = binding(RECORD)
    request = {"group": GROUP, "pendingIds": IDS, "pendingCount": 2,
               "status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
               "freshPacketRequiredForCurrentAuthority": True, "packet": archive_binding,
               "deliveryManifest": delivery_binding, "packetRecord": record_binding,
               "sourcePreparation": prep_binding, "independentAudit": audit_binding, "receipt": receipt_binding}

    for row in queue.get("currentPendingGroups", []):
        if row.get("group") == GROUP:
            row.update({"status": "PACKET284_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                        "freshPacketRequiredForCurrentAuthority": True, "pendingIds": IDS, "pendingCount": 2,
                        "packet": archive_binding, "deliveryManifest": delivery_binding,
                        "packetRecord": record_binding, "sourcePreparation": prep_binding,
                        "independentAudit": audit_binding, "receipt": receipt_binding})
        elif row.get("group") == "rank9-knowledge-revelation5":
            row["freshPacketRequiredForCurrentAuthority"] = True
    queue.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                  "status": "RANK9_PLANARGATES5_PACKET284_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                  "packetStatus": "RANK9_PLANARGATES5_PACKET284_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32",
                  "currentPreparation": prep_binding, "currentPacket": archive_binding,
                  "currentDeliveryManifest": delivery_binding, "currentPacketDelivery": delivery_binding,
                  "currentPacketRecord": record_binding, "currentIndependentAudit": audit_binding,
                  "currentReceipt": receipt_binding, "next": request, "nextPreparedRequest": request,
                  "nextGroup": GROUP, "nextPendingIds": IDS, "nextSuggestedGroups": [request],
                  "pendingIdentityAudit": binding(PENDING), "currentPendingAudit": binding(PENDING)})
    write(QUEUE, queue)
    queue_binding = binding(QUEUE)

    handoff.update({"recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                    "status": "RANK9_KNOWLEDGEREVELATION5_RETURN283_AUDITED_NEXT_PLANARGATES5_PACKET284_AUDITED_816_32",
                    "currentAuthority": AUTH, "currentQueueBinding": queue_binding,
                    "queue": queue_binding, "queueBinding": queue_binding,
                    "pendingIdentityAudit": binding(PENDING), "currentPreparation": prep_binding,
                    "currentPacket": archive_binding, "currentPacketDelivery": delivery_binding,
                    "currentPacketRecord": record_binding, "currentIndependentAudit": audit_binding,
                    "currentReceipt": receipt_binding,
                    "nextStep": {"group": GROUP, "pendingIds": IDS, "pendingCount": 2,
                                 "status": "PACKET284_PREPARED_INDEPENDENTLY_AUDITED_UNSENT_816_32"},
                    "nextStepText": "Upload the independently audited Packet284 for only banishment-gate and conjure-demiplane-fortress. Check GPT Director frequently, audit its sealed return, and apply only exact accepted identities.",
                    "resumePriority": "Send Packet284 to GPT Director; continue only with the two exact Planar Gates identities, preserve Return200 closed spells and all current holds, and audit/apply exact accepted spells.",
                    "currentReturnAudit": audit_binding, "currentReceipt": receipt_binding})
    write(HANDOFF, handoff)
    snapshot = ("# Current ordinary spell-review snapshot 284\n\n"
                "Return283 is independently audited PASS (14/14); `faction-omniscience-supreme` remains held under KR198-B01. "
                "Authority is **816 applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.\n\n"
                "Packet284 passed independent audit (14/14) for only `banishment-gate` and `conjure-demiplane-fortress`, "
                "with 175 refreshed source bindings and all 250 archive members verified. The three Planar spells accepted and applied in Return200 remain closed.\n\n"
                "See [handoff](CURRENT_HANDOFF_284.json), [queue](CURRENT_SPELL_QUEUE_284.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_284.json), "
                "[packet](rank9_planargates5_current_source_284_prepared/DD_Rank9_PlanarGates5_CurrentSource_284.zip), and "
                "[independent audit](RANK9PLANARGATES5_PACKET_284_INDEPENDENT_AUDIT.json).\n")
    SNAPSHOT.write_text(snapshot, encoding="utf-8", newline="\n")

    start = ROOT / "START_HERE.md"
    old = start.read_text(encoding="utf-8-sig")
    _, _, rest = old.partition("\n\n")
    new_first = ("**Current ordinary spell-review handoff [284](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_284.json):** "
                 "authority is 816 applied / 32 pending / 0 accepted-unapplied. Packet284 is independently audited PASS (14/14) for "
                 "banishment-gate and conjure-demiplane-fortress. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_planargates5_current_source_284_prepared/DD_Rank9_PlanarGates5_CurrentSource_284.zip) "
                 "and [audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PLANARGATES5_PACKET_284_INDEPENDENT_AUDIT.json).")
    start.write_text(new_first + "\n\n" + rest, encoding="utf-8", newline="\n")

    report = {"id": "RANK9PLANARGATES5-PACKET284-AUDIT-RECONCILIATION", "status": "PASS",
              "authority": AUTH, "group": GROUP, "pendingIds": IDS, "packet": archive_binding,
              "delivery": delivery_binding, "independentAudit": audit_binding, "receipt": receipt_binding,
              "packetRecord": record_binding, "queue": binding(QUEUE), "handoff": binding(HANDOFF),
              "pendingIdentityAudit": binding(PENDING), "snapshot": binding(SNAPSHOT)}
    write(BASE / "RANK9PLANARGATES5_PACKET_284_AUDIT_RECONCILIATION.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
