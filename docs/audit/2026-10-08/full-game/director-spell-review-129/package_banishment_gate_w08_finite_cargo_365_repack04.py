from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "banishment_gate_witness365_w08_finite_cargo04_build02"
PACKET = OUT / "packet"
ARCHIVE_NAME = "DD_Rank9_BanishmentGate_W08_FiniteCargo_365_TESTONLY_REPACK04.zip"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    archive_path = OUT / ARCHIVE_NAME
    delivery_path = OUT / "ARCHIVE_DELIVERY_365_W08_REPACK04.json"
    manifest_path = PACKET / "ARCHIVE_MANIFEST.json"
    if not PACKET.is_dir():
        raise SystemExit(f"Missing W08 packet directory: {PACKET}")
    if archive_path.exists() or manifest_path.exists():
        raise SystemExit("Refusing to overwrite an existing W08 archive or manifest")

    paths = sorted(p for p in PACKET.rglob("*") if p.is_file() and p != manifest_path)
    records = []
    for path in paths:
        data = path.read_bytes()
        records.append({
            "path": path.relative_to(PACKET).as_posix(),
            "bytes": len(data),
            "sha256": sha(data),
            "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}",
        })
    manifest = {
        "id": "PG327-W08-ARCHIVE-MANIFEST-365-REPACK04",
        "createdAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "manifestMember": "ARCHIVE_MANIFEST.json",
        "memberCount": len(records),
        "members": records,
        "allPathsUnique": len({r["path"] for r in records}) == len(records),
        "archiveContainsOnlyListedPayloadsPlusManifest": True,
    }
    write_json(manifest_path, manifest)

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        all_paths = sorted(p for p in PACKET.rglob("*") if p.is_file())
        for path in all_paths:
            rel = path.relative_to(PACKET).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    archive_data = archive_path.read_bytes()
    manifest_data = manifest_path.read_bytes()
    delivery = {
        "id": "PG327-W08-ARCHIVE-DELIVERY-365-REPACK04",
        "createdAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "TEST_ONLY_W08_REPACK04_PACKET_SUBMITTED_FOR_FRESH_DIRECTOR_REVIEW",
        "witnessId": "W08",
        "scopeId": "banishment-gate",
        "archive": {
            "name": ARCHIVE_NAME,
            "bytes": len(archive_data),
            "sha256": sha(archive_data),
            "archiveMembers": len(records) + 1,
            "manifestPayloadMembers": len(records),
        },
        "manifest": {"path": "ARCHIVE_MANIFEST.json", "bytes": len(manifest_data), "sha256": sha(manifest_data)},
        "directorSequence": ["W08", "W05"],
        "preservedWitnesses": ["W01 SEALED_TEST_ONLY", "W02", "W04", "W06", "W07"],
        "remainingWitnessesAfterThisSubmission": ["W08", "W05", "W03"],
        "identityDecision": "HOLD",
        "blockerIds": ["PG200-B03", "PG200-B04"],
        "acceptedIds": [],
        "appliedIds": [],
        "applicationAuthorized": False,
        "queueAuthority": {"applied": 828, "pending": 20, "acceptedUnapplied": 0,
                            "completeStandaloneProcedures": 552, "scopedInterfaces": 173,
                            "firstReviews": 0, "closureTasks": 20},
        "evidenceClass": "conditional TEST_ONLY authored static witness; no campaign event or runtime execution asserted",
    }
    write_json(delivery_path, delivery)
    print(json.dumps({"archive": str(archive_path), "bytes": len(archive_data), "sha256": sha(archive_data),
                      "members": len(records) + 1, "delivery": str(delivery_path)}, indent=2))


if __name__ == "__main__":
    main()
