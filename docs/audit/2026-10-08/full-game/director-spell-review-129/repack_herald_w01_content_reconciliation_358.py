from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import shutil
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SOURCE = A / "rank9_summon_herald_w01_content_reconciliation_358"
OUT = A / "rank9_summon_herald_w01_content_reconciliation_358_repack01"
ARCHIVE = OUT / "DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01.zip"
DELIVERY = OUT / "DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01_DELIVERY.json"
PAYLOAD = OUT / "payload"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def crc(b: bytes) -> str:
    return f"{zlib.crc32(b) & 0xffffffff:08x}"


def main() -> None:
    if OUT.exists():
        raise SystemExit(f"Refusing to overwrite Repack01 output: {OUT}")
    PAYLOAD.mkdir(parents=True)
    rows = []
    for source in sorted(SOURCE.iterdir(), key=lambda p: p.name):
        if not source.is_file() or source.name in {
            "MEMBER_MANIFEST.json",
            "DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358.zip",
        }:
            continue
        dest = PAYLOAD / source.name
        shutil.copyfile(source, dest)
        b = dest.read_bytes()
        rows.append({"path": source.name, "bytes": len(b), "sha256": sha(b), "crc32": crc(b)})
    assert len(rows) == 10
    manifest = {"id": "SH202-W01-RECONCILIATION-358-REPACK01-MANIFEST", "selfExcluded": True,
                "memberCountExcludingSelf": len(rows), "members": rows}
    (PAYLOAD / "MEMBER_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(PAYLOAD.iterdir(), key=lambda p: p.name):
            if path.is_file():
                zf.write(path, path.name)
    with zipfile.ZipFile(ARCHIVE) as zf:
        assert zf.testzip() is None
        names = zf.namelist()
        assert "MEMBER_MANIFEST.json" in names and len(names) == len(rows) + 1
        for row in rows:
            b = zf.read(row["path"])
            assert len(b) == row["bytes"] and sha(b) == row["sha256"] and crc(b) == row["crc32"]
    archive_raw = ARCHIVE.read_bytes()
    delivery = {
        "id": "SH202-W01-RECONCILIATION-358-REPACK01-DELIVERY",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "SOURCE_BOUND_W01_PACKET_REPACKAGED_SELF_MEMBER_REMOVED_NOT_APPROVED",
        "supersedesArchive": "../rank9_summon_herald_w01_content_reconciliation_358/DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358.zip",
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw), "memberCount": len(rows) + 1},
        "payloadManifest": {"path": "payload/MEMBER_MANIFEST.json", "memberCountExcludingSelf": len(rows), "selfArchiveExcluded": True},
        "w01Approved": False,
    }
    DELIVERY.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "archive": delivery["archive"], "payloads": len(rows), "w01Approved": False}, indent=2))


if __name__ == "__main__":
    main()
