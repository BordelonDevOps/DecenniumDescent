from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
ARCHIVE = FULL / "DD_Rank8_Information_Time_4_Source_Conference_03.zip"
OLD_ARCHIVE = FULL / "DD_Rank8_Information_Time_4_Source_Conference_02.zip"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_information_time_4_source_conference_03.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
IDS = ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]
AUTH = {"reviewedApplied": 726, "pending": 122, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 450, "scopedInterfaces": 173}
REPORT = AUDIT / "RANK8_INFORMATION_TIME4_PACKET163_VERIFICATION.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify() -> dict:
    checks, failed = [], []

    def ck(label: str, ok: bool):
        checks.append({"check": label, "passed": bool(ok)})
        if not ok:
            failed.append(label)

    new_raw, old_raw = ARCHIVE.read_bytes(), OLD_ARCHIVE.read_bytes()
    with zipfile.ZipFile(ARCHIVE) as newz, zipfile.ZipFile(OLD_ARCHIVE) as oldz:
        ck("Packet03 is a 68-member unique CRC-valid ZIP", len(newz.namelist()) == 68 and len(set(newz.namelist())) == 68 and newz.testzip() is None)
        names = set(newz.namelist())
        manifest = json.loads(newz.read("MANIFEST.json"))
        candidate = json.loads(newz.read("CURRENT_AUTHORITY_UPDATE.json"))
        request = newz.read("DIRECTOR_REQUEST.txt").decode("utf-8")
        correction = json.loads(newz.read("PROVENANCE_CORRECTION.json"))
        ck("Packet03 manifest matches actual members and requested IDs", manifest["memberCount"] == 68 and manifest["requestedIds"] == IDS and {x["path"] for x in manifest["members"]} == names - {"MANIFEST.json"})
        member_hashes = all(len(newz.read(x["path"])) == x["bytes"] and sha(newz.read(x["path"])) == x["sha256"] for x in manifest["members"])
        ck("Every Packet03 manifest path, size, and hash verifies", member_hashes)
        ck("Packet03 request and corrected candidate target only four identities", candidate["requestedIds"] == IDS and [x["spellId"] for x in candidate["records"]] == IDS and all(name in request for name in ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]))
        ck("Packet03 binds exact fresh authority files", candidate["currentAuthority"] == AUTH and newz.read("CURRENT_AUTHORITY/authored_review_index.json") == INDEX.read_bytes() and newz.read("CURRENT_AUTHORITY/catalog.json") == CATALOG.read_bytes())
        ck("The pending four are still pending in exact live index", all(next(row for row in json.loads(INDEX.read_text(encoding="utf-8-sig"))["entries"] if row["id"] == sid)["authoredStatus"] == "pending-authored-procedure" for sid in IDS))
        prev = candidate["previousConference"]
        base_raw = newz.read("BASE_PACKET/DD_Rank8_Information_Time_4_Source_Conference_01.zip")
        ck("Previous packet archive reference resolves to exact embedded historical ZIP", prev["archive"]["path"] == "BASE_PACKET/DD_Rank8_Information_Time_4_Source_Conference_01.zip" and len(base_raw) == prev["archive"]["bytes"] and sha(base_raw) == prev["archive"]["sha256"])
        archived_ok = True
        with zipfile.ZipFile(__import__("io").BytesIO(base_raw)) as basez:
            for row in prev["archiveMemberBindings"]:
                member = row["path"].removeprefix("BASE_PACKET/")
                raw = basez.read(member)
                archived_ok = archived_ok and len(raw) == row["bytes"] and sha(raw) == row["sha256"] and newz.read(row["path"]) == raw
            ck("Conference01 authority in embedded candidate matches stated historical 525/323", json.loads(basez.read("CANDIDATE.json"))["countsUnchanged"] == prev["authorityAtPreparation"] == {"reviewed": 525, "pending": 323})
        ck("Every previous-conference path resolves to exact nested archive member", archived_ok and prev["bindingRule"].startswith("Each archiveMemberBindings path resolves"))
        ck("No packet02 stale sidecar paths or hashes remain in corrected history", all(key not in prev for key in ["candidate", "check", "preparation", "request", "manifest"]) and len(prev["archiveMemberBindings"]) == 4)
        ck("Correction note binds and supersedes exact packet02 archive", correction["supersededArchive"]["bytes"] == len(old_raw) and correction["supersededArchive"]["sha256"] == sha(old_raw) and candidate["supersedesPacket"]["archive"] == correction["supersededArchive"])
        unchanged_names = names & set(oldz.namelist()) - {"CURRENT_AUTHORITY_UPDATE.json", "DIRECTOR_REQUEST.txt", "MANIFEST.json"}
        exact_preserved = all(newz.read(name) == oldz.read(name) for name in unchanged_names)
        ck("All prior packet source and authority members are preserved byte-exactly", exact_preserved and len(unchanged_names) == 64)
        ck("Current-source authority remains static-only and excluded cohorts are explicit", candidate["excludedAlreadyAppliedIds"] == ["absolute-silence", "control-weather", "earthquake"] and candidate["excludedClosedCohorts"] == ["feat335", "completed spell batches"])

    result = {"id": "RANK8-INFORMATION-TIME4-PACKET163-VERIFICATION", "status": "PASS" if not failed else "FAIL", "checksPassed": len(checks)-len(failed), "checksFailed": len(failed), "failedChecks": failed, "checks": checks, "authority": AUTH, "requestedIds": IDS, "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(new_raw), "sha256": sha(new_raw)}}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    report = verify()
    print(json.dumps({k: report[k] for k in ["id", "status", "checksPassed", "checksFailed", "failedChecks", "archive"]}, indent=2))
    sys.exit(0 if report["status"] == "PASS" else 1)
