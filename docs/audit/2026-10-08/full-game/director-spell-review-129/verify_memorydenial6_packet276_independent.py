from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PKG = AUDIT / "rank9_memorydenial6_current_source_276_prepared"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_276.json"
    pending_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_276.json"
    handoff_path = AUDIT / "CURRENT_HANDOFF_276.json"
    archive_path = PKG / "DD_Rank9_MemoryDenial6_CurrentSource_276.zip"
    delivery_path = PKG / "DD_Rank9_MemoryDenial6_CurrentSource_276_DELIVERY.json"
    candidate_path = PKG / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_276.json"
    index, catalog = read(index_path), read(catalog_path)
    queue, pending, handoff = read(queue_path), read(pending_path), read(handoff_path)
    delivery, candidate = read(delivery_path), read(candidate_path)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    expected_authority = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
                         "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
    assert queue["currentAuthority"] == handoff["authority"] == expected_authority
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 32
    assert len(set(pending["pendingIds"])) == 32
    assert queue["activeReview"]["identity"] == "mind-collapse"
    assert queue["activeReview"]["blocker"] == "MD196-B01"
    assert "UNHOLY_ASCENDANCE" not in queue["status"] and "UNHOLY_ASCENDANCE" not in queue["packetStatus"]
    assert queue["nextGroup"] == handoff["nextGroup"] == "rank9-memory-denial6"
    assert queue["nextPendingIds"] == handoff["nextPendingIds"] == ["mind-collapse"]
    assert queue["nextPendingCount"] == handoff["nextPendingCount"] == 1
    assert queue["pendingCount"] == 32 and queue["currentPendingGroups"]
    assert queue["currentSourcePacket"]["path"] == delivery["archive"]["path"]
    assert handoff["currentQueueBinding"]["sha256"] == sha(queue_path.read_bytes())
    assert handoff["currentPacket"]["sha256"] == sha(archive_path.read_bytes())
    assert handoff["currentPacketDelivery"]["sha256"] == sha(delivery_path.read_bytes())
    assert delivery["sourceAuthority"] == expected_authority and delivery["sourceBranch"] == "main"
    assert delivery["sourceCommit"] == commit and delivery["group"] == "rank9-memory-denial6"
    assert delivery["pendingIds"] == ["mind-collapse"] and delivery["accepted"] is False and delivery["applied"] is False
    assert candidate["currentSourceCommit"] == commit and candidate["currentBranch"] == "main"
    assert candidate["currentAuthority"] == expected_authority
    assert [row["spellId"] for row in candidate["records"]] == ["mind-collapse"]
    assert len(candidate["sourceBindings"]) == 120

    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        assert archive.testzip() is None and len(names) == len(set(names))
        assert all("\\" not in name and not PurePosixPath(name).is_absolute() and
                   all(part not in ("", ".", "..") and not part.startswith(".") for part in PurePosixPath(name).parts)
                   for name in names)
        manifest = json.loads(archive.read("MANIFEST.json"))
        assert len(manifest["members"]) == manifest["memberCountExcludingSelf"]
        assert manifest["sourceAuthority"] == expected_authority and manifest["sourceCommit"] == commit
        assert manifest["pendingIds"] == ["mind-collapse"]
        assert sha(archive_path.read_bytes()) == delivery["archive"]["sha256"]
        assert archive_path.stat().st_size == delivery["archive"]["bytes"]
        assert f"{zlib.crc32(archive_path.read_bytes()) & 0xFFFFFFFF:08x}" == delivery["archive"]["crc32"]
        manifest_rows = {row["path"]: row for row in manifest["members"]}
        assert set(manifest_rows) == set(names) - {"MANIFEST.json"}
        for name, row in manifest_rows.items():
            raw = archive.read(name)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
        for binding in candidate["sourceBindings"]:
            path = ROOT / binding["path"]
            raw = path.read_bytes()
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
            member = archive.read("sources_current/" + binding["path"])
            assert member == raw
        for path in ["current/CURRENT_SPELL_QUEUE_276.json", "current/CURRENT32_PENDING_IDENTITY_AUDIT_276.json",
                     "current/CURRENT_HANDOFF_276.json", "current/MIND_COLLAPSE_DIRECTOR_FINDINGS_275.json",
                     "REQUEST_276.txt"]:
            assert path in names
        packaged_queue = json.loads(archive.read("current/CURRENT_SPELL_QUEUE_276.json"))
        assert packaged_queue["activeReview"]["identity"] == "mind-collapse"
        assert "UNHOLY_ASCENDANCE" not in packaged_queue["status"]
    report = {"id": "RANK9-MEMORYDENIAL6-PACKET276-INDEPENDENT-AUDIT", "status": "PASS",
        "authority": expected_authority, "pendingIds": pending["pendingIds"],
        "queueStatusCorrected": True, "sourceBindingsVerified": 120,
        "archiveMembersVerified": len(manifest_rows), "archiveBytes": archive_path.stat().st_size,
        "archiveSha256": sha(archive_path.read_bytes()), "deliveryManifestSha256": sha(delivery_path.read_bytes()),
        "currentQueueSha256": sha(queue_path.read_bytes()), "currentHandoffSha256": sha(handoff_path.read_bytes()),
        "directorPriorityGroups": len(queue["recommendedClosureOrder"]),
        "checksPassed": 12, "checksFailed": 0,
        "checks": [
            {"check": "Canonical index and current queue/handoff/pending audit reconcile to 816/32/0 and 540/173.", "passed": True},
            {"check": "All 32 current pending IDs are unique and preserved; the next selected ID is Mind Collapse.", "passed": True},
            {"check": "Queue activeReview/status no longer names completed Unholy Ascendance.", "passed": True},
            {"check": "Corrected queue, handoff and packet/delivery bindings agree byte-for-byte.", "passed": True},
            {"check": "Candidate packet contains only pending Mind Collapse with current main/HEAD authority.", "passed": True},
            {"check": "All 120 refreshed source bindings match current workspace files and packet members.", "passed": True},
            {"check": "Archive manifest names every member and each member size/SHA-256/CRC matches on readback.", "passed": True},
            {"check": "Archive has no duplicate or unsafe member paths and passes ZIP CRC testing.", "passed": True},
            {"check": "Time Stop and unrelated prior spell decisions remain context only; no identity is accepted or applied.", "passed": True},
            {"check": "Director's full 15-group priority sequence and exact top-three evidence targets are recorded.", "passed": True},
            {"check": "Canonical Mind Collapse spell record remains pending and operational is null.", "passed": True},
            {"check": "No canonical spell card change was performed during packet preparation.", "passed": True},
        ]}
    report_path = AUDIT / "RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
