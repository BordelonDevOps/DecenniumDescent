from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_planargates5_current_source_199_prepared"
ARCHIVE = OUT / "DD_Rank9_PlanarGates5_CurrentSource_199.zip"
DELIVERY = OUT / "DD_Rank9_PlanarGates5_CurrentSource_199_DELIVERY.json"
REPORT = AUDIT / "RANK9PLANARGATES5_PACKET199_INDEPENDENT_VERIFICATION.json"
IDS = ["gate", "absolute-gate", "banishment-gate", "planar-sanctuary", "conjure-demiplane-fortress"]
AUTHORITY = {"reviewedApplied": 790, "pending": 58, "acceptedUnapplied": 0, "completeStandaloneProcedures": 514, "scopedInterfaces": 173}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def main() -> None:
    delivery = read(DELIVERY)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    remote_rows = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=ROOT, text=True).split()
    archive_hash = hashlib.sha256()
    archive_bytes = 0
    with ARCHIVE.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            archive_hash.update(chunk)
            archive_bytes += len(chunk)
    checks = []
    checks.append({"check": "Packet source commit is the pushed branch head", "passed": bool(remote_rows) and delivery["sourceCommit"] == head == remote_rows[0] and delivery["sourceBranch"] == branch, "detail": {"source": delivery["sourceCommit"], "head": head, "remote": remote_rows[0] if remote_rows else None}})
    checks.append({"check": "Archive byte length and SHA match delivery", "passed": archive_bytes == delivery["archive"]["bytes"] and archive_hash.hexdigest() == delivery["archive"]["sha256"], "detail": {"bytes": archive_bytes, "sha256": archive_hash.hexdigest()}})
    checks.append({"check": "Delivery names the exact next group at 790/58 authority", "passed": delivery["status"] == "PREPARED_UNSENT" and delivery["sourceAuthority"] == AUTHORITY and delivery["pendingIds"] == IDS and delivery["accepted"] is False and delivery["applied"] is False, "detail": {"group": delivery["group"], "pendingIds": delivery["pendingIds"]}})
    with zipfile.ZipFile(ARCHIVE) as packet:
        names = packet.namelist()
        manifest = json.loads(packet.read("MANIFEST.json"))
        rows = {row["path"]: row for row in manifest["members"]}
        all_ok = packet.testzip() is None and len(names) == len(set(names)) == manifest["memberCountExcludingSelf"] + 1 and set(names) == set(rows) | {"MANIFEST.json"} and all(safe(name) for name in names)
        failed = []
        for name, row in rows.items():
            h, crc, size = hashlib.sha256(), 0, 0
            with packet.open(name) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(chunk)
                    crc = zlib.crc32(chunk, crc)
                    size += len(chunk)
            if size != row["bytes"] or h.hexdigest() != row["sha256"] or f"{crc & 0xffffffff:08x}" != row["crc32"]:
                failed.append(name)
        checks.append({"check": "ZIP members are safe, unique, CRC-valid, and fully match size/SHA/CRC manifest", "passed": all_ok and not failed, "detail": {"members": len(names), "manifestRows": len(rows), "failed": failed[:10]}})
        candidate = json.loads(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"))
        notes = json.loads(packet.read("HISTORICAL_NOTES/RANK9PLANARGATES5_NEXT_CONFERENCE_NOTES_129.json"))
        packet_request = packet.read("REQUEST_199.txt").decode("utf-8")
        checks.append({"check": "All questions, main cases, future obligations, and exact target identities are preserved", "passed": [row["spellId"] for row in candidate["records"]] == IDS and len(notes["completeOriginalQuestionsUnchanged"]) == 30 and len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["allQuestions"]) == 32 and len(notes["requiredNewCases"]) == 10 and len(notes["originalFutureCaseRequirementsUnchanged"]) == 9 and all(sid in packet_request for sid in IDS), "detail": {"questions": len(notes["allQuestions"]), "mainCases": len(notes["requiredNewCases"]), "future": len(notes["originalFutureCaseRequirementsUnchanged"])}})
        source_failures = []
        for binding in candidate["sourceBindings"]:
            name = "sources_current/" + binding["path"]
            try:
                raw = packet.read(name)
                expected_blob = blob(delivery["sourceCommit"], binding["path"])
                git_blob_sha = subprocess.check_output(["git", "rev-parse", f"{delivery['sourceCommit']}:{binding['path']}"], cwd=ROOT, text=True).strip()
                if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"] or len(expected_blob) != binding["bytes"] or sha(expected_blob) != binding["sha256"] or git_blob_sha != binding["gitBlobSHA1"]:
                    source_failures.append(binding["path"])
            except Exception:
                source_failures.append(binding["path"])
        checks.append({"check": "All 132 refreshed source bindings match embedded members and Git blobs", "passed": len(candidate["sourceBindings"]) == 132 and not source_failures and candidate["currentSourceCommit"] == delivery["sourceCommit"], "detail": {"checked": len(candidate["sourceBindings"]), "failures": source_failures[:10]}})
        old_candidate = packet.read("HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json")
        old_archive = packet.read("HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip")
        checks.append({"check": "Historical candidate and archive match exact queued bindings", "passed": len(old_candidate) == delivery["historicalCandidate"]["bytes"] and sha(old_candidate) == delivery["historicalCandidate"]["sha256"] and len(old_archive) == delivery["historicalSourceArchive"]["bytes"] and sha(old_archive) == delivery["historicalSourceArchive"]["sha256"], "detail": {"candidateBytes": len(old_candidate), "archiveBytes": len(old_archive)}})
        queue = json.loads(packet.read("current/" + "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_198.json"))
        pending = json.loads(packet.read("current/" + "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT58_PENDING_IDENTITY_AUDIT_198.json"))
        index = json.loads(packet.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
        catalog = json.loads(packet.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
        pending_now = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
        target = next(group for group in queue["currentPendingGroups"] if group["group"] == delivery["group"])
        checks.append({"check": "Current queue, pending audit, source index, and catalog agree at 790/58", "passed": queue["currentAuthority"] == AUTHORITY and pending["pendingCount"] == 58 and set(pending["pendingIds"]) == pending_now and target["pendingIds"] == IDS and target["pendingCount"] == 5 and index["authoredCounts"] == {"reviewed": 790, "pending": 58} and all(sid in {row["id"] for row in catalog["spells"]} for sid in IDS), "detail": {"pending": len(pending_now), "targetIds": target["pendingIds"]}})
        context_text = packet.read("CURRENT_CONTEXT_199.json").decode("utf-8")
        memory_model = json.loads(packet.read("current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json"))
        transport_model = json.loads(packet.read("current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/MODEL.json"))
        checks.append({"check": "Current KR198 and accepted Transport6 context are preserved with named hold", "passed": "KR198-B01" in context_text and "MD196" in context_text and memory_model["acceptedIds"] == ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"] and memory_model["unacceptedIds"] == ["faction-omniscience-supreme"] and memory_model["runtimeSelectionEnabled"] is False and "transport-6" in transport_model.get("id", "").lower(), "detail": {"knowledgeAccepted": memory_model["acceptedIds"], "knowledgeHeld": memory_model["unacceptedIds"], "transportModel": transport_model.get("id")}})
    failed_checks = [row for row in checks if not row["passed"]]
    report = {"id": "RANK9-PLANAR-GATES5-PACKET199-INDEPENDENT-VERIFICATION", "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failed_checks else "FAIL", "checksPassed": len(checks) - len(failed_checks), "checksFailed": len(failed_checks), "checks": checks, "sourceCommit": delivery["sourceCommit"], "sourceBranch": delivery["sourceBranch"], "sourceAuthority": delivery["sourceAuthority"], "packet": delivery["archive"], "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())}, "accepted": False, "applied": False}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"], "failures": failed_checks}, indent=2))
    if failed_checks:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
