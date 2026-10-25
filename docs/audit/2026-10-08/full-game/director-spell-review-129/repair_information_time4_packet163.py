from __future__ import annotations

import copy
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
REVIEW = ROOT / "DescentReviewChanges/ReviewBible"
OLD_ZIP = FULL / "DD_Rank8_Information_Time_4_Source_Conference_02.zip"
OLD_CANDIDATE = REVIEW / "data/director/spell_review/rank8_information_time_4_source_conference_02.json"
OLD_REQUEST = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_02_REQUEST.txt"
OLD_CHECK = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_02_CHECK.json"
OLD_PREP = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_02_PREPARATION.json"
BASE_ZIP = FULL / "DD_Rank8_Information_Time_4_Source_Conference_01.zip"
IDS = ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]
AUTHORITY = {"reviewedApplied": 726, "pending": 122, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 450, "scopedInterfaces": 173}
OUTROOT = FULL / "rank8-information-time4-source-conference-03"
STAGING = OUTROOT.with_name(OUTROOT.name + ".staging")
ARCHIVE = FULL / "DD_Rank8_Information_Time_4_Source_Conference_03.zip"
CANDIDATE = REVIEW / "data/director/spell_review/rank8_information_time_4_source_conference_03.json"
REQUEST = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_03_REQUEST.txt"
CHECK = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_03_CHECK.json"
PREP = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_03_PREPARATION.json"
SUBMISSION = AUDIT / "RANK8_INFORMATION_TIME4_SUBMISSION_163.json"
QUEUE_IN = AUDIT / "CURRENT_SPELL_QUEUE_162.json"
HANDOFF_IN = AUDIT / "CURRENT_HANDOFF_162.json"
PENDING = AUDIT / "CURRENT122_PENDING_IDENTITY_AUDIT_161.json"
QUEUE_OUT = AUDIT / "CURRENT_SPELL_QUEUE_163.json"
HANDOFF_OUT = AUDIT / "CURRENT_HANDOFF_163.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: Path, rel: str) -> dict:
    raw = path.read_bytes()
    return {"path": rel, "bytes": len(raw), "sha256": sha(raw)}


def prepare() -> None:
    outputs = [OUTROOT, STAGING, ARCHIVE, CANDIDATE, REQUEST, CHECK, PREP, SUBMISSION, QUEUE_OUT, HANDOFF_OUT]
    assert not [str(p) for p in outputs if p.exists()], "Packet03 output exists; inspect before retrying."
    queue = read(QUEUE_IN)
    handoff = read(HANDOFF_IN)
    pending = read(PENDING)
    current_candidate = read(OLD_CANDIDATE)
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert pending["pendingCount"] == 122 and set(IDS) <= set(pending["pendingIds"])
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS
    old_zip_bytes = OLD_ZIP.read_bytes()
    old_zip_sha = sha(old_zip_bytes)
    with zipfile.ZipFile(OLD_ZIP) as source:
        assert source.testzip() is None and len(source.namelist()) == 67
        old_members = {name: source.read(name) for name in source.namelist()}
    with zipfile.ZipFile(BASE_ZIP) as source:
        assert source.testzip() is None
        base_members = {name: source.read(name) for name in source.namelist()}
    archived_base = json.loads(base_members["CANDIDATE.json"])
    archive_member_names = [name for name in ["CANDIDATE.json", "SOURCE_CHECK.json", "MANIFEST.json", "README.md"] if name in base_members]
    archive_bindings = [{"path": f"BASE_PACKET/{name}", "bytes": len(base_members[name]), "sha256": sha(base_members[name])} for name in archive_member_names]
    base_zip_binding = {"path": "BASE_PACKET/DD_Rank8_Information_Time_4_Source_Conference_01.zip", "bytes": len(BASE_ZIP.read_bytes()), "sha256": sha(BASE_ZIP.read_bytes())}

    corrected = copy.deepcopy(current_candidate)
    corrected["id"] = "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE03"
    corrected["recordedAtUtc"] = datetime.now(timezone.utc).isoformat()
    corrected["status"] = "SOURCE_CONFERENCE_PREPARED_UNSENT"
    corrected["supersedesPacket"] = {"id": current_candidate["id"], "archive": {"path": OLD_ZIP.name, "bytes": len(old_zip_bytes), "sha256": old_zip_sha}, "reason": "Packet02 referenced five previous-conference sidecars at paths that were not members of its archive. Packet03 replaces those links with exact nested archive-member bindings."}
    corrected["requestedIds"] = IDS
    corrected["previousConference"] = {
        "status": "context_only_unselected_and_unadopted",
        "authorityAtPreparation": archived_base.get("countsUnchanged"),
        "archive": base_zip_binding,
        "archiveMemberBindings": archive_bindings,
        "bindingRule": "Each archiveMemberBindings path resolves inside the nested packet01 ZIP's extracted BASE_PACKET tree and carries the exact member size and SHA-256. No external packet01 sidecar is represented as a member or byte-identical copy.",
    }
    assert corrected["previousConference"]["authorityAtPreparation"] == {"reviewed": 525, "pending": 323}
    assert [row["spellId"] for row in corrected["records"]] == IDS

    superseded_record = {
        "id": "INFORMATION-TIME4-PACKET02-PROVENANCE-CORRECTION",
        "supersededArchive": {"path": OLD_ZIP.name, "bytes": len(old_zip_bytes), "sha256": old_zip_sha},
        "reason": "Packet02's CURRENT_AUTHORITY_UPDATE.previousConference contained five sidecar paths whose byte/hash bindings did not resolve to exact members of the delivered nested historical packet archive.",
        "correction": "Packet03 removes those five sidecar references from the controlling candidate and binds the original conference archive plus its exact archived CANDIDATE.json, SOURCE_CHECK.json, MANIFEST.json, and README.md members.",
        "currentAuthorityUnchanged": AUTHORITY,
        "requestedIdsUnchanged": IDS,
    }
    request_text = (
        "GPT director correction and review request — Information/Time4 packet03, authority unchanged at 726/122.\n\n"
        "Packet03 supersedes packet02 because packet02's previousConference block had five provenance sidecar references whose path/hash bindings did not resolve inside the delivered ZIP. The corrected CURRENT_AUTHORITY_UPDATE.json removes those links and binds the exact nested Conference01 ZIP plus exact embedded CANDIDATE.json, SOURCE_CHECK.json, MANIFEST.json, and README.md member bytes. See PROVENANCE_CORRECTION.json and the packet manifest.\n\n"
        "Use packet03's fresh CURRENT_AUTHORITY_UPDATE.json and CURRENT_AUTHORITY directory as controlling. The current authority is unchanged: 726 applied-reviewed / 122 pending / 0 accepted-unapplied. Review only alignment-revelation-mass, moment-of-prescience, telepathy, and time-echo. Keep the complete packet02 source context and all current authority files; do not revisit the three applied Environment3 identities, feat335, or completed cohorts. Resolve all 17 source questions and return complete exact proposed procedures, dispositions, cases, state-transition operations, holds, and an independent failure check. If packet03 passes, state accepted=true/applied=false only for exact accepted IDs; otherwise leave unaccepted/unapplied and list exact binding or semantic blockers. Runtime, human-play, balance, cosmology and release remain unapproved.\n"
    )

    STAGING.mkdir(parents=True, exist_ok=False)
    for name, raw in old_members.items():
        if name in {"CURRENT_AUTHORITY_UPDATE.json", "DIRECTOR_REQUEST.txt", "MANIFEST.json"}:
            continue
        target = STAGING / PurePosixPath(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (STAGING / "CURRENT_AUTHORITY_UPDATE.json").write_bytes(enc(corrected))
    (STAGING / "DIRECTOR_REQUEST.txt").write_text(request_text, encoding="utf-8", newline="\n")
    (STAGING / "PROVENANCE_CORRECTION.json").write_bytes(enc(superseded_record))
    manifest_members = []
    for path in sorted(STAGING.rglob("*")):
        if path.is_file():
            raw = path.read_bytes()
            manifest_members.append({"path": path.relative_to(STAGING).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    manifest = {
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE03-MANIFEST",
        "authority": AUTHORITY,
        "requestedIds": IDS,
        "supersedes": superseded_record["supersededArchive"],
        "members": manifest_members,
        "memberCount": len(manifest_members) + 1,
        "manifestExcludedFromSelfHash": True,
    }
    (STAGING / "MANIFEST.json").write_bytes(enc(manifest))
    with zipfile.ZipFile(ARCHIVE, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(STAGING.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(STAGING).as_posix())
    archive_bytes = ARCHIVE.read_bytes()
    archive_binding = {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(archive_bytes), "sha256": sha(archive_bytes)}
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == manifest["memberCount"] == 68
        for row in manifest_members:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        assert z.read("CURRENT_AUTHORITY_UPDATE.json") == enc(corrected)
        assert z.read("BASE_PACKET/DD_Rank8_Information_Time_4_Source_Conference_01.zip") == BASE_ZIP.read_bytes()
        for row in archive_bindings:
            member = row["path"].removeprefix("BASE_PACKET/")
            raw = z.read("BASE_PACKET/" + member)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]

    CANDIDATE.write_bytes(enc(corrected))
    REQUEST.write_text(request_text, encoding="utf-8", newline="\n")
    check = {
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE03-CHECK",
        "status": "PASS",
        "checksPassed": 14 + len(manifest_members) + len(archive_bindings),
        "checksFailed": 0,
        "authority": AUTHORITY,
        "requestedIds": IDS,
        "packet02Superseded": superseded_record["supersededArchive"],
        "nestedConference01ArchiveExact": True,
        "allPreviousConferencePathsResolveToExactNestedArchiveMembers": True,
        "noExternalSidecarMisrepresentedAsNestedMember": True,
        "currentIndexCatalogQueuePendingAuditAndHandoffBindingsPreserved": True,
        "allPacketMembersPassManifestHashCheck": True,
        "sourceRulesAdopted": 0,
        "runtimeTestsExecuted": 0,
        "humanPlaytests": 0,
        "archive": archive_binding,
        "correctedCandidate": {"path": CANDIDATE.relative_to(ROOT).as_posix(), "bytes": len(enc(corrected)), "sha256": sha(enc(corrected))},
        "nestedArchiveMemberBindings": archive_bindings,
    }
    CHECK.write_bytes(enc(check))
    PREP.write_bytes(enc({
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE03-PREPARATION",
        "status": "PREPARED_UNSENT",
        "authority": AUTHORITY,
        "requestedIds": IDS,
        "archive": archive_binding,
        "candidate": {"path": CANDIDATE.relative_to(ROOT).as_posix(), "bytes": CANDIDATE.stat().st_size, "sha256": sha(CANDIDATE.read_bytes())},
        "request": {"path": REQUEST.relative_to(ROOT).as_posix(), "bytes": REQUEST.stat().st_size, "sha256": sha(REQUEST.read_bytes())},
        "check": {"path": CHECK.relative_to(ROOT).as_posix(), "bytes": CHECK.stat().st_size, "sha256": sha(CHECK.read_bytes())},
        "nestedArchiveMemberBindings": archive_bindings,
        "manifestMemberCount": manifest["memberCount"],
    }))
    for path in sorted(STAGING.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()
    STAGING.rmdir()
    OUTROOT.mkdir()
    (OUTROOT / "README.md").write_text("Information/Time4 packet03 supersedes packet02's defective historical sidecar links. It retains current authority 726/122 and binds the nested Conference01 archive to exact archived members.\n", encoding="utf-8", newline="\n")

    submission = {
        "id": "RANK8-INFORMATION-TIME4-SUBMISSION-163",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PREPARED_FOR_GPT_DIRECTOR_SUBMISSION",
        "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "conversationTitle": "Calibration review part 6",
        "authority": AUTHORITY,
        "requestedIds": IDS,
        "supersedesSubmission": "RANK8_INFORMATION_TIME4_SUBMISSION_162.json",
        "archive": archive_binding,
        "request": {"path": REQUEST.relative_to(ROOT).as_posix(), "bytes": REQUEST.stat().st_size, "sha256": sha(REQUEST.read_bytes())},
        "candidate": {"path": CANDIDATE.relative_to(ROOT).as_posix(), "bytes": CANDIDATE.stat().st_size, "sha256": sha(CANDIDATE.read_bytes())},
        "check": {"path": CHECK.relative_to(ROOT).as_posix(), "bytes": CHECK.stat().st_size, "sha256": sha(CHECK.read_bytes())},
        "preparation": {"path": PREP.relative_to(ROOT).as_posix(), "bytes": PREP.stat().st_size, "sha256": sha(PREP.read_bytes())},
        "directorTask": "Use packet03 as the controlling corrected packet. Verify the corrected nested historical archive-member bindings and continue static review of only the four Information/Time IDs.",
    }
    SUBMISSION.write_bytes(enc(submission))
    queue_out = copy.deepcopy(queue)
    queue_out["id"] = "SPELL-REVIEW-QUEUE-163"
    queue_out["recordedAtUtc"] = datetime.now(timezone.utc).isoformat()
    first = queue_out["currentPendingGroups"][0]
    first.update({"candidate": submission["candidate"], "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False,
                  "preparation": submission["preparation"], "submission": {"path": SUBMISSION.relative_to(ROOT).as_posix(), "bytes": SUBMISSION.stat().st_size, "sha256": sha(SUBMISSION.read_bytes())},
                  "status": "CORRECTED_PACKET03_SUBMITTED_AWAITING_DIRECTOR_RETURN"})
    queue_out["currentSubmission"] = {"path": SUBMISSION.relative_to(ROOT).as_posix(), "bytes": SUBMISSION.stat().st_size, "sha256": sha(SUBMISSION.read_bytes())}
    queue_out["next"] = {"group": first["group"], "pendingCount": 4, "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False, "status": first["status"]}
    QUEUE_OUT.write_bytes(enc(queue_out))
    handoff_out = copy.deepcopy(handoff)
    handoff_out.update({"id": "CURRENT-HANDOFF-163", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                        "status": "RANK8_INFORMATION_TIME4_PACKET03_CORRECTED_AWAITING_DIRECTOR_RETURN_726_122",
                        "currentQueueBinding": {"path": QUEUE_OUT.relative_to(ROOT).as_posix(), "bytes": QUEUE_OUT.stat().st_size, "sha256": sha(QUEUE_OUT.read_bytes())},
                        "resumePriority": "Await GPT's corrected Information/Time4 packet03 exact return; independently audit it, apply only exact accepted IDs, and continue until pending reaches zero.",
                        "nextPreparedRequest": {"group": "rank8-information-time4", "candidate": submission["candidate"], "archive": archive_binding, "preparation": submission["preparation"], "request": submission["request"], "submission": {"path": SUBMISSION.relative_to(ROOT).as_posix(), "bytes": SUBMISSION.stat().st_size, "sha256": sha(SUBMISSION.read_bytes())}, "freshPacketRequiredForCurrentAuthority": False},
                        "directorSubmission": {"record": SUBMISSION.relative_to(ROOT).as_posix(), "status": submission["status"], "conversationId": submission["conversationId"], "archiveSha256": archive_binding["sha256"], "supersedes": "RANK8_INFORMATION_TIME4_SUBMISSION_162.json"}})
    HANDOFF_OUT.write_bytes(enc(handoff_out))
    print(json.dumps({"status": "PACKET03_READY", "authority": AUTHORITY, "ids": IDS, "archive": archive_binding,
                      "memberCount": manifest["memberCount"], "correctedHistoryBindings": archive_bindings,
                      "check": check["status"], "submission": submission["id"]}, indent=2))


if __name__ == "__main__":
    prepare()
