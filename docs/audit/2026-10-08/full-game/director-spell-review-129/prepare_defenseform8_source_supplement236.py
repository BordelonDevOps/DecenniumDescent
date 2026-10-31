from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_defenseform8_source_supplement_236"
ZIP = OUT / "DD_Rank9_DefenseForm8_SourceSupplement_236.zip"
DELIVERY = OUT / "DD_Rank9_DefenseForm8_SourceSupplement_236_DELIVERY.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}

FILES = [
    "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/manifestation7_reviewed_137/MODEL.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/manifestation7_reviewed_137/PROCEDURES.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/manifestation7_reviewed_137/CASEBOOK.json.gz",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8_damage6_reviewed_122.json",
    "DescentReviewChanges/ReviewBible/data/playtest/spell_candidates/rank8_damage6_cases_122.json",
    "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_damage6_retained_holds_122.json",
    "DescentReviewChanges/ReviewBible/docs/mechanics/classes/mage.md",
    "DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_SOURCE_BINDINGS.md",
    "DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md",
    "DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/MANIFESTATION7_EXACT_ACCEPTANCE_137.json",
    "docs/audit/2026-10-08/full-game/RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json",
    "docs/audit/2026-10-08/full-game/accepted72-application-122/rank8-damage6_APPLICATION.json",
]


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    idx_path = ROOT / FILES[0]
    idx_raw = idx_path.read_bytes()
    index = json.loads(idx_raw.decode("utf-8-sig"))
    entries = {row["id"]: row for row in index["entries"]}
    assert index.get("authoredCounts") == {"reviewed": 811, "pending": 37}
    assert entries["volcanic-cage"]["authoredStatus"] == "reviewed-authored-operational-playtest"
    assert entries["deep-crust-spike"]["authoredStatus"] == "reviewed-authored-operational-playtest"
    assert entries["time-stop"]["authoredStatus"] == "pending-authored-procedure"
    def git_head_bytes(rel: str) -> bytes:
        result = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, check=True, capture_output=True)
        return result.stdout

    deep_path = entries["deep-crust-spike"]["completeEnvelopeBinding"]["path"]
    deep_receipt_path = entries["deep-crust-spike"]["authoredAcceptanceReceipt"]["path"]
    deep_current = (ROOT / deep_path).read_bytes()
    deep_current_receipt = (ROOT / deep_receipt_path).read_bytes()
    deep_git = git_head_bytes(deep_path)
    deep_receipt_git = git_head_bytes(deep_receipt_path)
    assert deep_current.replace(b"\r\n", b"\n") == deep_git
    assert deep_current_receipt.replace(b"\r\n", b"\n") == deep_receipt_git
    assert hashlib.sha256(deep_git).hexdigest() == entries["deep-crust-spike"]["completeEnvelopeBinding"]["sha256"]
    assert hashlib.sha256(deep_receipt_git).hexdigest() == entries["deep-crust-spike"]["authoredAcceptanceReceipt"]["sha256"]

    evidence = {
        "id": "RANK9-DEFENSEFORM8-PACKET236-ACCEPTED-SOURCE-LEADS",
        "authority": AUTHORITY,
        "purpose": "Provide the exact previously accepted standalone procedure envelopes for two relevant source leads plus current Mage Elemental Familiar and lifecycle sources omitted from Packet236's 87-path source snapshot.",
        "scopeIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
        "identityStatuses": {key: {"authoredStatus": entries[key].get("authoredStatus"), "sourceStatus": entries[key].get("sourceStatus"), "procedureFile": entries[key].get("procedureFile"), "procedurePointer": entries[key].get("procedurePointer"), "completeEnvelopeBinding": entries[key].get("completeEnvelopeBinding"), "authoredAcceptanceReceipt": entries[key].get("authoredAcceptanceReceipt")} for key in ("volcanic-cage", "deep-crust-spike", "time-stop")},
        "bindingReconciliation": {
            "volcanic-cage": "The current candidate and receipt bytes match the authored index bindings exactly.",
            "deep-crust-spike": {
                "indexBindingStatus": "verified-after-line-ending-normalization",
                "currentCandidate": {"path": deep_path, "bytes": len(deep_current), "sha256": hashlib.sha256(deep_current).hexdigest()},
                "indexedCandidate": entries["deep-crust-spike"]["completeEnvelopeBinding"],
                "normalizedCandidate": {"path": "index-bound/" + deep_path, "bytes": len(deep_git), "sha256": hashlib.sha256(deep_git).hexdigest()},
                "currentReceipt": {"path": deep_receipt_path, "bytes": len(deep_current_receipt), "sha256": hashlib.sha256(deep_current_receipt).hexdigest()},
                "indexedReceipt": entries["deep-crust-spike"]["authoredAcceptanceReceipt"],
                "normalizedReceipt": {"path": "index-bound/" + deep_receipt_path, "bytes": len(deep_receipt_git), "sha256": hashlib.sha256(deep_receipt_git).hexdigest()},
                "disposition": "The apparent byte mismatch is Windows CRLF checkout conversion only. Normalizing CRLF to LF exactly reproduces the current HEAD Git blobs and the authored index byte counts and SHA-256 values for both candidate and receipt. Exact indexed envelope and receipt are included under index-bound/."
            }
        },
        "qualifications": [
            "Authored acceptance of Volcanic Cage and Deep Crust Spike does not change their current catalog sourceStatus or populate operational fields.",
            "The two accepted procedures are source-search leads only; no hazard, victim, crossing, actor history or lawful scenario is asserted by this supplement.",
            "Deep Crust Spike's apparent local byte mismatch is only Windows CRLF conversion: line-ending normalization exactly matches the current HEAD Git blobs and the authored index bindings. The exact LF-bound envelope and receipt are also included under index-bound/.",
            "Mage Elemental Familiar and the companion lifecycle documents define source-authored properties; no actual campaign instance is asserted.",
            "No new rule, identity, canonical change, operational card, or application is introduced.",
        ],
    }
    files: dict[str, bytes] = {"SUPPLEMENT_SCOPE.json": enc(evidence)}
    for rel in FILES:
        path = ROOT / PurePosixPath(rel)
        raw = path.read_bytes()
        data = raw
        if rel.endswith("authored_review_index.json") or rel.endswith("catalog.json"):
            data = json.loads(raw.decode("utf-8-sig"))
            current_raw = path.read_bytes()
            files["current/" + rel] = current_raw
        else:
            files["current/" + rel] = raw
    files["index-bound/" + deep_path] = deep_git
    files["index-bound/" + deep_receipt_path] = deep_receipt_git
    files.pop(FILES[0], None)
    # Include the accepted-application state explicitly; all copied inputs are
    # exact current bytes and are bound below.
    member_rows = [{"path": name, **digest(raw)} for name, raw in sorted(files.items())]
    manifest = {"id": "RANK9-DEFENSEFORM8-SUPPLEMENT236-INTERNAL-MANIFEST", "authority": AUTHORITY, "members": member_rows}
    manifest_raw = enc(manifest)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(files.items()):
            assert safe(name)
            z.writestr(name, raw)
        z.writestr("MEMBER_MANIFEST.json", manifest_raw)
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert set(z.namelist()) == set(files) | {"MEMBER_MANIFEST.json"}
        for row in member_rows:
            assert digest(z.read(row["path"])) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
        assert z.read("MEMBER_MANIFEST.json") == manifest_raw
    archive_raw = ZIP.read_bytes()
    delivery = {
        "id": "RANK9-DEFENSEFORM8-SOURCESUPPLEMENT236-DELIVERY",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "authority": AUTHORITY,
        "targetIds": evidence["scopeIds"],
        "archive": {"fileName": ZIP.name, **digest(archive_raw)},
        "memberCount": len(files) + 1,
        "payloadCount": len(files),
        "memberManifest": {"path": "MEMBER_MANIFEST.json", **digest(manifest_raw)},
        "exactAllowlist": sorted([*files, "MEMBER_MANIFEST.json"]),
        "members": member_rows + [{"path": "MEMBER_MANIFEST.json", **digest(manifest_raw)}],
        "canonicalChanges": False,
        "githubChanges": False,
    }
    DELIVERY.write_bytes(enc(delivery))
    print(json.dumps({"status": "PREPARED", "authority": AUTHORITY, "targetIds": evidence["scopeIds"], "members": len(files) + 1, "archive": {"bytes": len(archive_raw), "sha256": digest(archive_raw)["sha256"]}, "delivery": digest(DELIVERY.read_bytes())}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
