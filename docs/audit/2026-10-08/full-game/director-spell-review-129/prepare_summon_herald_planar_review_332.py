#!/usr/bin/env python3
"""Prepare a narrowly scoped current-source review packet for SH202-B02."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path


A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_summon_herald_planar_review_332_prepared"
ZIP_PATH = OUT / "DD_Rank9_SummonHeraldOfThePlanes_Review332.zip"
DELIVERY_PATH = OUT / "DD_Rank9_SummonHeraldOfThePlanes_Review332_DELIVERY.json"
CATALOG_PATH = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX_PATH = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
RETURN285_PATH = A / "rank9_summonhosts5_return285_received/DD_Rank9_SummonHosts5_Director_Return285_HELD.zip"
RETURN331_DIR = A / "rank9_summon_elemental_avatar_return331_received/payload"
QUEUE331 = A / "CURRENT_SPELL_QUEUE_331.json"
PENDING331 = A / "CURRENT25_PENDING_IDENTITY_AUDIT_331.json"
HANDOFF331 = A / "CURRENT_HANDOFF_331.json"
SPELL_ID = "summon-herald-of-the-planes"
BLOCKER = "SH202-B02"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc32(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind_file(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def find_id(node, wanted):
    if isinstance(node, dict):
        if node.get("id") == wanted:
            return node
        for value in node.values():
            found = find_id(value, wanted)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_id(value, wanted)
            if found is not None:
                return found
    return None


def main() -> None:
    if OUT.exists() and any(OUT.iterdir()):
        raise RuntimeError(f"Refusing to overwrite a non-empty packet directory: {OUT}")
    OUT.mkdir(parents=True, exist_ok=True)
    files_dir = OUT / "packet"
    files_dir.mkdir()

    queue = load_json(QUEUE331)
    pending = load_json(PENDING331)
    handoff = load_json(HANDOFF331)
    catalog = load_json(CATALOG_PATH)
    index = load_json(INDEX_PATH)
    spell = find_id(catalog, SPELL_ID)
    index_row = find_id(index, SPELL_ID)
    if spell is None or index_row is None:
        raise RuntimeError("Current catalog/index binding does not contain the target spell.")
    if queue.get("next") != SPELL_ID or queue.get("currentAuthority", {}).get("pending") != 25:
        raise RuntimeError("Queue331 does not designate the current target or authority.")

    with zipfile.ZipFile(RETURN285_PATH) as prior:
        old_decision = json.loads(prior.read("DIRECTOR_DECISION.json"))
        old_row = next(item for item in old_decision["decisions"] if item.get("id") == SPELL_ID)
        source_bindings = json.loads(prior.read("SOURCE_BINDINGS.json"))
        selected_rows = [
            row for row in source_bindings.get("rows", [])
            if "lumen-of-the-shattered-thread" in row.get("path", "").lower()
            or row.get("path", "").endswith("spell_playtests/catalog.json")
        ]
        embedded = {
            "priorArchive": {"path": RETURN285_PATH.relative_to(ROOT).as_posix(), "bytes": RETURN285_PATH.stat().st_size, "sha256": sha256(RETURN285_PATH.read_bytes()), "crc32": crc32(RETURN285_PATH.read_bytes())},
            "priorAuthority": old_decision.get("authority"),
            "scopeRow": old_row,
            "selectedSourceBindings": selected_rows,
        }
        payload = {
            "00_CURRENT_AUTHORITY_331.json": {
                "authority": queue["currentAuthority"],
                "queue": bind_file(QUEUE331),
                "pendingAudit": bind_file(PENDING331),
                "handoff": bind_file(HANDOFF331),
                "activeReview": queue.get("activeReview"),
                "heldAvatarCorrectionOpen": ["SH331-C01", "SH331-C02", "SH331-C03"],
            },
            "01_CURRENT_CATALOG_SPELL.json": spell,
            "02_CURRENT_AUTHORED_REVIEW_INDEX_ROW.json": index_row,
            "03_RETURN331_AVATAR_HOLD.json": load_json(RETURN331_DIR / "DIRECTOR_DECISION.json"),
            "04_RETURN285_HERALD_DECISION_AND_BINDINGS.json": embedded,
            "05_RETURN285_HERALD_PROCEDURE.json": json.loads(prior.read("procedures/summon-herald-of-the-planes.json")),
            "06_RETURN285_HERALD_CASE_A.json": json.loads(prior.read("cases/RANK9SUMMONHOSTS5129-SUMMON-HERALD-OF-THE-PLANES-A.json")),
            "07_RETURN285_HERALD_CASE_B.json": json.loads(prior.read("cases/RANK9SUMMONHOSTS5129-SUMMON-HERALD-OF-THE-PLANES-B.json")),
        }
        lumen = prior.read("evidence/lumen-of-the-shattered-thread.md")

    for filename, value in payload.items():
        (files_dir / filename).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (files_dir / "08_RETURN285_LUMEN_SOURCE.md").write_bytes(lumen)

    request = """# Director review request — Summon Herald of the Planes / SH202-B02

This packet covers one identity only. Current authority is queue331: 823 reviewed/applied, 25 pending, 0 accepted-unapplied. Return331 expressly designates Summon Herald of the Planes / SH202-B02 as the next priority and separately leaves the Avatar correction findings SH331-C01–C03 open.

Please reuse Return285’s exact Herald procedure, cases A/B, source bindings and its selected Lumen evidence. Reconcile them with the current catalog spell row and current review-index row. Do not use Return285’s historical 816/32 authority as current.

Decide whether the current source and existing conditional evidence permit a precise spell-local operational contract and executed positive/negative transition witnesses for this identity. The historical blocker requires an eligible unique CR15+ Celestial/Elemental/Outsider with complete operational profile; present availability, willingness, location, resources, custody and knowledge permissions; lawful arrival and blocked-return settlement; and useful aid, concurrent-call exclusion and ending. For Lumen specifically, prior findings name Thread Lance/Bind reach, Thread Shatter area, and the Seal/arena/phase/return contract. Its attached dossier is a historical failure record; it does not by itself establish current location, presence, willingness, custody or permissions.

Do not invent campaign facts, generic heralds, consent, or new cosmology. If conditional fixtures are sufficient for the authored-procedure review, specify exact conditional premises, operations, observed before/after outcomes, reverse operations and unchanged state paths, clearly separating that result from actual campaign authorization. Otherwise seal an exact one-identity HOLD naming only the minimum unproved facts, the best already-source-bound witness (if any), and the next priority after SH202-B02. State exact accepted/applied/held IDs and application authorization, counts, provenance, and provide a matching sealed ZIP plus delivery JSON.

Do not repeat the full Summon Hosts replay or alter canonical data. Do not close the separate Avatar corrections.
"""
    (OUT / "REQUEST_332.md").write_text(request, encoding="utf-8")

    entries = []
    for path in sorted(files_dir.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            entries.append({"path": path.relative_to(files_dir).as_posix(), "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)})
    manifest = {"id": "SUMMON-HERALD-PLANAR-REVIEW-332-MANIFEST", "payloadMemberCount": len(entries), "members": entries}
    (files_dir / "MEMBER_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(OUT / "REQUEST_332.md", "REQUEST_332.md")
        for path in sorted(files_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(files_dir).as_posix())
    zip_bytes = ZIP_PATH.read_bytes()
    with zipfile.ZipFile(ZIP_PATH) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Archive CRC failure: {bad}")
        exact_names = set(archive.namelist())
        if len(exact_names) != len(archive.namelist()) or "REQUEST_332.md" not in exact_names:
            raise RuntimeError("Archive members are duplicate or missing the request.")

    current_catalog = bind_file(CATALOG_PATH)
    current_index = bind_file(INDEX_PATH)
    delivery = {
        "id": "SUMMON-HERALD-PLANAR-REVIEW-332-DELIVERY",
        "archive": {"fileName": ZIP_PATH.name, "bytes": len(zip_bytes), "sha256": sha256(zip_bytes), "crc32": crc32(zip_bytes)},
        "archiveMemberCount": len(exact_names),
        "payloadMemberCount": len(entries),
        "currentAuthority": queue["currentAuthority"],
        "currentQueue": bind_file(QUEUE331),
        "currentPendingAudit": bind_file(PENDING331),
        "currentCatalogBinding": current_catalog,
        "currentIndexBinding": current_index,
        "targetId": SPELL_ID,
        "blockerId": BLOCKER,
        "priorReturn285AuthorityHistoricalOnly": embedded["priorAuthority"],
        "noCanonicalMutation": True,
        "contents": entries,
    }
    DELIVERY_PATH.write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    checks = {
        "target_present_in_current_catalog": spell.get("id") == SPELL_ID and spell.get("status") == "blocked-pending-operational-review",
        "target_present_in_current_index": index_row.get("id") == SPELL_ID and index_row.get("authoredStatus") == "pending-authored-procedure",
        "queue331_designates_target": queue.get("next") == SPELL_ID and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER],
        "authority_is_current_823_25_0": queue.get("currentAuthority") == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
        "return285_has_one_exact_held_row": old_row.get("blockerIds") == [BLOCKER] and old_row.get("held") is True,
        "herald_procedure_and_cases_included": len([x for x in payload if "HERALD_CASE" in x]) == 2 and "05_RETURN285_HERALD_PROCEDURE.json" in payload,
        "lumen_source_is_explicitly_historical": b"Historical Failure Record" in lumen,
        "avatar_findings_preserved": payload["03_RETURN331_AVATAR_HOLD.json"].get("heldIds") == ["summon-elemental-avatar"],
        "archive_crc_passes": True,
        "no_canonical_mutation": delivery["noCanonicalMutation"] is True,
    }
    if not all(checks.values()):
        raise RuntimeError("Packet audit failed: " + json.dumps(checks, ensure_ascii=False))
    audit = {
        "id": "SUMMON-HERALD-PLANAR-REVIEW-332-PREPARATION-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS_PACKET_PREPARED_NOT_SENT",
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(checks.values()),
        "failed": sum(not value for value in checks.values()),
        "archive": delivery["archive"],
        "delivery": {"path": DELIVERY_PATH.relative_to(ROOT).as_posix(), "bytes": DELIVERY_PATH.stat().st_size, "sha256": sha256(DELIVERY_PATH.read_bytes()), "crc32": crc32(DELIVERY_PATH.read_bytes())},
        "authority": queue["currentAuthority"],
        "scope": [SPELL_ID],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    (OUT / "PREPARATION_AUDIT_332.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"archive": str(ZIP_PATH), "bytes": len(zip_bytes), "sha256": sha256(zip_bytes), "delivery": str(DELIVERY_PATH), "checks": len(checks), "passed": sum(checks.values()), "failed": sum(not value for value in checks.values())}, indent=2))


if __name__ == "__main__":
    main()
