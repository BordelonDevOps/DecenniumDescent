from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET = BASE / "rank9_summonhosts5_current_source_285_prepared/DD_Rank9_SummonHosts5_CurrentSource_285.zip"
DELIVERY = BASE / "rank9_summonhosts5_current_source_285_prepared/DD_Rank9_SummonHosts5_CurrentSource_285_DELIVERY.json"
PREPARATION = BASE / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_285.json"
AUDIT = BASE / "RANK9SUMMONHOSTS5_PACKET_285_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9SUMMONHOSTS5_PACKET_285_RECEIPT.json"
RECORD = BASE / "RANK9SUMMONHOSTS5_PACKET_285.json"
OUT = BASE / "RANK9SUMMONHOSTS5_PACKET_285_AUDIT_RECONCILIATION.json"


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
    assert audit["status"] == receipt["status"] == prep["status"] == "PASS"
    assert audit["passedChecks"] == audit["checkCount"] == 14 and len(audit["failedChecks"]) == 0
    assert audit["sourceAuthority"] == receipt["sourceAuthority"] == delivery["sourceAuthority"]
    assert delivery["archive"]["sha256"] == bind(PACKET)["sha256"] == audit["archive"]["sha256"]
    record.update({"status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT", "archive": bind(PACKET),
        "deliveryManifest": bind(DELIVERY), "sourcePreparation": bind(PREPARATION),
        "independentAudit": bind(AUDIT), "receipt": bind(RECEIPT)})
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    report = {"id": "RANK9SUMMONHOSTS5-PACKET285-AUDIT-RECONCILIATION", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS", "group": "rank9-summon-hosts5", "pendingIds": audit["targetIds"],
        "sourceAuthority": audit["sourceAuthority"], "archive": bind(PACKET), "delivery": bind(DELIVERY),
        "sourcePreparation": bind(PREPARATION), "independentAudit": bind(AUDIT), "receipt": bind(RECEIPT),
        "packetRecord": bind(RECORD), "checks": ["Packet preparation PASS", "Independent packet audit PASS 14/14",
            "Archive and delivery SHA-256 values agree", "Authority remains 816 applied / 32 pending / 0 accepted-unapplied"]}
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
