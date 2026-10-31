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
ARCHIVE = OUT / "DD_Rank9_DefenseForm8_SourceSupplement_236.zip"
DELIVERY = OUT / "DD_Rank9_DefenseForm8_SourceSupplement_236_DELIVERY.json"
REPORT = BASE / "RANK9_DEFENSEFORM8_SUPPLEMENT236_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_DEFENSEFORM8_SUPPLEMENT236_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
checks = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def matches(raw: bytes, binding: dict) -> bool:
    got = digest(raw)
    return all(got.get(k) == binding.get(k) for k in ("bytes", "sha256")) and (binding.get("crc32") is None or got["crc32"] == binding["crc32"])


def check(name: str, passed: bool, detail=None):
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
archive_raw = ARCHIVE.read_bytes()
delivery_raw = DELIVERY.read_bytes()
check("supplement archive and delivery bind exact bytes and current authority", delivery.get("id") == "RANK9-DEFENSEFORM8-SOURCESUPPLEMENT236-DELIVERY" and delivery.get("authority") == AUTHORITY and matches(archive_raw, delivery.get("archive", {})) and delivery.get("archive", {}).get("fileName") == ARCHIVE.name, digest(archive_raw))
index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
index = json.loads(index_path.read_text(encoding="utf-8-sig"))
catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
entries = {row["id"]: row for row in index["entries"]}
spells = {row["id"]: row for row in catalog["spells"]}
check("current index distinguishes accepted standalone Volcanic Cage/Deep Crust Spike from pending Time Stop", index.get("authoredCounts") == {"reviewed": 811, "pending": 37} and all(entries[s].get("authoredStatus") == "reviewed-authored-operational-playtest" for s in ("volcanic-cage", "deep-crust-spike")) and entries["time-stop"].get("authoredStatus") == "pending-authored-procedure", {s: entries[s].get("authoredStatus") for s in ("volcanic-cage", "deep-crust-spike", "time-stop")})
check("catalog still leaves all three operational pointers null and preserves their source statuses", all(spells[s].get("operational") is None for s in ("volcanic-cage", "deep-crust-spike", "time-stop")) and all(spells[s].get("status") == "blocked-pending-operational-review" for s in ("volcanic-cage", "deep-crust-spike", "time-stop")), {s: {"status": spells[s].get("status"), "operational": spells[s].get("operational")} for s in ("volcanic-cage", "deep-crust-spike", "time-stop")})

with zipfile.ZipFile(ARCHIVE) as z:
    names = z.namelist()
    name_set = set(names)
    check("ZIP is CRC-valid, unique and contains exactly the external allowlist", z.testzip() is None and len(names) == len(name_set) == delivery.get("memberCount") and set(delivery.get("exactAllowlist", [])) == name_set, {"members": len(names), "memberCount": delivery.get("memberCount")})
    external = {row["path"]: row for row in delivery.get("members", [])}
    errors = [name for name in names if name not in external or not matches(z.read(name), external[name])]
    check("all supplement members match external byte/SHA/CRC bindings", not errors, errors[:10])
    manifest_raw = z.read("MEMBER_MANIFEST.json")
    manifest = json.loads(manifest_raw)
    internal = {row["path"]: row for row in manifest.get("members", [])}
    check("internal self-excluding member manifest covers every payload and matches its external record", set(internal) == name_set - {"MEMBER_MANIFEST.json"} and matches(manifest_raw, delivery.get("memberManifest", {})), len(internal))
    errors = [name for name, binding in internal.items() if not matches(z.read(name), binding)]
    check("all supplement payloads match internal manifest", not errors, errors[:10])
    source_files = [name for name in names if name.startswith("current/")]
    worktree_errors = []
    for name in source_files:
        local = ROOT / PurePosixPath(name.removeprefix("current/"))
        if not local.exists() or local.read_bytes() != z.read(name):
            worktree_errors.append(name)
    check("all 15 copied sources equal their current worktree bytes", len(source_files) == 15 and not worktree_errors, {"sourceCount": len(source_files), "errors": worktree_errors})

    volcanic = entries["volcanic-cage"]
    volcanic_candidate = ROOT / volcanic["completeEnvelopeBinding"]["path"]
    volcanic_receipt = ROOT / volcanic["authoredAcceptanceReceipt"]["path"]
    check("Volcanic Cage current procedure and receipt match their exact authored-index bindings", matches(volcanic_candidate.read_bytes(), volcanic["completeEnvelopeBinding"]) and matches(z.read("current/" + volcanic["completeEnvelopeBinding"]["path"]), volcanic["completeEnvelopeBinding"]) and matches(volcanic_receipt.read_bytes(), volcanic["authoredAcceptanceReceipt"]), {"candidate": digest(volcanic_candidate.read_bytes()), "receipt": digest(volcanic_receipt.read_bytes())})

    deep = entries["deep-crust-spike"]
    deep_candidate = ROOT / deep["completeEnvelopeBinding"]["path"]
    deep_receipt = ROOT / deep["authoredAcceptanceReceipt"]["path"]
    candidate_current = digest(deep_candidate.read_bytes())
    receipt_current = digest(deep_receipt.read_bytes())
    candidate_normalized = deep_candidate.read_bytes().replace(b"\r\n", b"\n")
    receipt_normalized = deep_receipt.read_bytes().replace(b"\r\n", b"\n")
    candidate_git = subprocess.run(["git", "show", f"HEAD:{deep['completeEnvelopeBinding']['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
    receipt_git = subprocess.run(["git", "show", f"HEAD:{deep['authoredAcceptanceReceipt']['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
    supplement_scope = json.loads(z.read("SUPPLEMENT_SCOPE.json"))
    rec = supplement_scope["bindingReconciliation"]["deep-crust-spike"]
    candidate_normalized_digest = digest(candidate_normalized)
    receipt_normalized_digest = digest(receipt_normalized)
    normalized_paths = {"candidate": "index-bound/" + deep["completeEnvelopeBinding"]["path"], "receipt": "index-bound/" + deep["authoredAcceptanceReceipt"]["path"]}
    reconciliation_ok = rec.get("indexBindingStatus") == "verified-after-line-ending-normalization" and candidate_normalized == candidate_git == z.read(normalized_paths["candidate"]) and receipt_normalized == receipt_git == z.read(normalized_paths["receipt"]) and matches(candidate_normalized, deep["completeEnvelopeBinding"]) and matches(receipt_normalized, deep["authoredAcceptanceReceipt"]) and rec.get("normalizedCandidate") == {"path": normalized_paths["candidate"], "bytes": candidate_normalized_digest["bytes"], "sha256": candidate_normalized_digest["sha256"]} and rec.get("normalizedReceipt") == {"path": normalized_paths["receipt"], "bytes": receipt_normalized_digest["bytes"], "sha256": receipt_normalized_digest["sha256"]} and "CRLF" in rec.get("disposition", "")
    check("Deep Crust Spike LF normalization matches the exact indexed candidate and receipt Git blobs", reconciliation_ok, {"currentCandidate": candidate_current, "normalizedCandidate": candidate_normalized_digest, "indexedCandidate": deep["completeEnvelopeBinding"], "currentReceipt": receipt_current, "normalizedReceipt": receipt_normalized_digest, "indexedReceipt": deep["authoredAcceptanceReceipt"]})

failures = [x for x in checks if not x["passed"]]
report = {"id": "RANK9DEFENSEFORM8-SUPPLEMENT236-INDEPENDENT-AUDIT", "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **digest(archive_raw)}, "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(delivery_raw)}, "authority": AUTHORITY, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "checks": checks}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9DEFENSEFORM8-SUPPLEMENT236-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"], "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "failures": failures, "archiveSha256": digest(archive_raw)["sha256"]}, ensure_ascii=False, indent=2))
