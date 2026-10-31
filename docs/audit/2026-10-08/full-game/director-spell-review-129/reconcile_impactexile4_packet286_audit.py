from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET = BASE / "rank9_impactexile4_current_source_286_prepared/DD_Rank9_ImpactExile4_CurrentSource_286.zip"
DELIVERY = BASE / "rank9_impactexile4_current_source_286_prepared/DD_Rank9_ImpactExile4_CurrentSource_286_DELIVERY.json"
PREPARATION = BASE / "RANK9IMPACTEXILE4_SOURCE_PREPARATION_286.json"
AUDIT = BASE / "RANK9IMPACTEXILE4_PACKET_286_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9IMPACTEXILE4_PACKET_286_RECEIPT.json"
RECORD = BASE / "RANK9IMPACTEXILE4_PACKET_286.json"
OUT = BASE / "RANK9IMPACTEXILE4_PACKET_286_AUDIT_RECONCILIATION.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_286.json"
HANDOFF = BASE / "CURRENT_HANDOFF_286.json"
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_286.md"


def bind(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8-sig"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8-sig"))
    prep = json.loads(PREPARATION.read_text(encoding="utf-8-sig"))
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    record = json.loads(RECORD.read_text(encoding="utf-8-sig"))
    auth = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
    assert audit["status"] == receipt["status"] == prep["status"] == "PASS"
    assert audit["passedChecks"] == audit["checkCount"] == 16 and not audit["failedChecks"]
    assert audit["authority"] == receipt["authority"] == delivery["sourceAuthority"] == auth
    assert delivery["archive"]["sha256"] == bind(PACKET)["sha256"] == audit["archive"]["sha256"]
    record.update({"status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT", "archive": bind(PACKET),
        "deliveryManifest": bind(DELIVERY), "sourcePreparation": bind(PREPARATION),
        "independentAudit": bind(AUDIT), "receipt": bind(RECEIPT)})
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    report = {"id": "RANK9IMPACTEXILE4-PACKET286-AUDIT-RECONCILIATION",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS",
        "group": "rank9-impact-exile4", "pendingIds": audit["targetIds"], "sourceAuthority": auth,
        "archive": bind(PACKET), "delivery": bind(DELIVERY), "sourcePreparation": bind(PREPARATION),
        "independentAudit": bind(AUDIT), "receipt": bind(RECEIPT), "packetRecord": bind(RECORD),
        "checks": ["Packet preparation PASS", "Independent packet audit PASS 16/16",
            "Archive and delivery SHA-256 values agree", "Authority remains 816 applied / 32 pending / 0 accepted-unapplied"]}
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    queue = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
    queue.update({"status": "RETURN285_AUDITED_HELD_NEXT_IMPACTEXILE4_PACKET286_INDEPENDENTLY_AUDITED_UNSENT_816_32",
        "packetStatus": "RANK9_IMPACT_EXILE4_PACKET_286_INDEPENDENTLY_AUDITED_UNSENT_816_32",
        "currentIndependentAudit": bind(AUDIT), "currentReceipt": bind(RECEIPT),
        "currentAuditReconciliation": bind(OUT)})
    queue["next"]["status"] = "CURRENT_SOURCE_PACKET_286_INDEPENDENTLY_AUDITED_UNSENT"
    queue["nextPreparedRequest"]["status"] = "CURRENT_SOURCE_PACKET_286_INDEPENDENTLY_AUDITED_UNSENT"
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8-sig"))
    handoff.update({"status": "RETURN285_AUDITED_HELD_NEXT_IMPACTEXILE4_PACKET286_INDEPENDENTLY_AUDITED_UNSENT_816_32",
        "currentIndependentAudit": bind(AUDIT), "currentReceipt": bind(RECEIPT),
        "currentAuditReconciliation": bind(OUT)})
    handoff["nextStep"]["status"] = "CURRENT_SOURCE_PACKET_286_INDEPENDENTLY_AUDITED_UNSENT_AT_AUTHORITY_816_32_0"
    handoff["nextPreparedRequest"]["status"] = "CURRENT_SOURCE_PACKET_286_INDEPENDENTLY_AUDITED_UNSENT"
    handoff["queue"] = bind(QUEUE)
    handoff["currentQueueBinding"] = handoff["queue"]
    HANDOFF.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    SNAPSHOT.write_text("# Current ordinary spell-review checkpoint 286\n\nReturn285 was independently audited and held exactly the three Summon Hosts5 identities. "
        "The fresh Impact/Exile4 packet for reverse-gravity-field passed its independent audit (16/16). "
        "Authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied** (540 complete standalone procedures; 173 scoped interfaces).\n",
        encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
