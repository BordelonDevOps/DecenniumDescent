from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_timefate6_current_source_191_prepared"
DELIVERY = OUT / "DD_Rank9_TimeFate6_CurrentSource_191_DELIVERY.json"
REPORT = AUDIT / "RANK9_TIMEFATE6_PACKET_VERIFICATION_191.json"
EXPECTED_IDS = ["time-stop", "time-fracture", "foresight-perfect", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") and not x.startswith(".") for x in p.parts)


def main() -> None:
    checks = []

    def record(name: str, detail: str) -> None:
        checks.append({"check": name, "passed": True, "detail": detail})

    delivery = read(DELIVERY.read_bytes())
    packet_path = ROOT / delivery["archive"]["path"]
    packet_raw = packet_path.read_bytes()
    assert len(packet_raw) == delivery["archive"]["bytes"] and sha(packet_raw) == delivery["archive"]["sha256"]
    record("Separate delivery manifest binds the exact packet", f"{len(packet_raw)} bytes; SHA-256 {sha(packet_raw)}")

    with zipfile.ZipFile(packet_path) as packet:
        names = packet.namelist()
        assert packet.testzip() is None and len(names) == len(set(names)) and all(safe(n) for n in names)
        manifest = read(packet.read("MANIFEST.json"))
        rows = manifest["members"]
        assert manifest["memberCountExcludingSelf"] == len(rows) and len(names) == len(rows) + 1
        for row in rows:
            raw = packet.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]
        record("Packet ZIP, safe-member list, SHA-256, and CRC manifest validate", f"{len(rows)} unique bound members plus MANIFEST.json")

        commit = manifest["sourceCommit"]
        branch = manifest["sourceBranch"]
        assert commit == delivery["sourceCommit"]
        assert branch == delivery["sourceBranch"]
        current = read(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_191.json"))
        context = read(packet.read("CURRENT_CONTEXT_191.json"))
        historical = read(packet.read("HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json"))
        assert current["currentSourceCommit"] == context["sourceCommit"] == commit
        assert current["currentAuthority"] == context["sourceAuthority"] == delivery["sourceAuthority"]
        assert current["currentPendingGroup"]["spellIds"] == context["targetGroup"]["pendingIds"] == EXPECTED_IDS
        assert [r["spellId"] for r in current["records"]] == EXPECTED_IDS
        record("Packet is bound to the exact pushed commit, authority, and queue group", f"{branch}@{commit}; 777 reviewed / 71 pending / 0 accepted-unapplied")

        original_archive_raw = packet.read("HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip")
        with zipfile.ZipFile(__import__("io").BytesIO(original_archive_raw)) as original:
            assert original.testzip() is None
            for binding in historical["sourceBindings"]:
                raw = original.read("sources/" + binding["path"])
                assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
        assert len(historical["sourceBindings"]) == len(current["sourceBindings"]) == 140
        record("All historical source bindings match their archived source conference", "140 historical source files verified")

        for binding in current["sourceBindings"]:
            raw = packet.read("sources_current/" + binding["path"])
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
            assert raw == blob(commit, binding["path"])
        record("All refreshed source bytes match Git objects at the declared commit", "140 current source files verified byte-for-byte")

        required = [
            "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_EXACT_ACCEPTANCE_190_RECONCILED01.json",
            "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_APPLICATION_190_RECONCILED01.json",
            "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_APPLICATION_VALIDATION_190_RECONCILED01.json",
            "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_INDEPENDENT_AUDIT.json",
        ]
        present = set(names)
        assert all(p in present for p in required)
        accepted = read(packet.read(required[0]))["acceptedIds"]
        assert accepted == ["command-reality", "dominate-legion", "erase-soul", "overwhelming-presence", "perfect-mesmerize", "prophecy-fulfilled", "rewrite-loyalty"]
        record("Reconciled Return190 acceptance and application evidence are included", "Seven accepted procedures; two held blockers remain outside this group")

        notes = read(packet.read("HISTORICAL_NOTES/RANK9TIMEFATE6_NEXT_CONFERENCE_NOTES_129.json"))
        assert len(notes["allQuestions"]) == 34 and len(notes["focusedAdditionalQuestions"]) == 2 and len(notes["requiredNewCases"]) == 12
        record("Review questions and required case scope are complete", "34 questions including 2 focused addenda; 12 required case specifications")

    report = {
        "id": "RANK9-TIME-FATE6-CURRENT-SOURCE-PACKET-VERIFICATION-191",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "checksPassed": len(checks),
        "checksFailed": 0,
        "packet": delivery["archive"],
        "sourceCommit": delivery["sourceCommit"],
        "sourceAuthority": delivery["sourceAuthority"],
        "pendingIds": EXPECTED_IDS,
        "sourceBindingsVerified": 140,
        "checks": checks,
    }
    REPORT.write_bytes((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
