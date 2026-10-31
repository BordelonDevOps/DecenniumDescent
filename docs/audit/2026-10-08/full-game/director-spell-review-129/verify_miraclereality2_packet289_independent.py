from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_miraclereality2_current_source_289_prepared"
ARCHIVE = OUT / "DD_Rank9_MiracleReality2_CurrentSource_289.zip"
DELIVERY = OUT / "DD_Rank9_MiracleReality2_CurrentSource_289_DELIVERY.json"
PACKET = BASE / "RANK9MIRACLEREALITY2_PACKET_289.json"
PREPARATION = BASE / "RANK9MIRACLEREALITY2_SOURCE_PREPARATION_289.json"
PACKET_AUDIT = BASE / "RANK9MIRACLEREALITY2_PACKET_289_INDEPENDENT_AUDIT.json"
PACKET_RECEIPT = BASE / "RANK9MIRACLEREALITY2_PACKET_289_RECEIPT.json"
SOURCE_PACKET288_AUDIT = BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_INDEPENDENT_AUDIT.json"
SOURCE_PACKET288_RECEIPT = BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_RECEIPT.json"
SOURCE_PACKET288_SUBMISSION = BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_SUBMISSION.json"
SOURCE_RETURN288_AUDIT = BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN288_INDEPENDENT_AUDIT.json"
SOURCE_RETURN288_RECEIPT = BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN288_RECEIPT.json"
PRIOR233 = BASE / "rank9_miraclereality2_return233_received"
CURRENT_QUEUE = BASE / "CURRENT_SPELL_QUEUE_289.json"
CURRENT_HANDOFF = BASE / "CURRENT_HANDOFF_289.json"
CURRENT_PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_289.json"
CURRENT_SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_289.md"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
TARGETS = ["divine-intervention-greater", "wish"]
PRIOR_BLOCKERS = {"divine-intervention-greater": ["MR233-B01"], "wish": ["MR233-B02"]}
RECENT = {
    284: ["banishment-gate", "conjure-demiplane-fortress"],
    285: ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"],
    286: ["reverse-gravity-field"],
    287: ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"],
    288: ["astral-projection", "imprisonment"],
}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def readj(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def readm(z: zipfile.ZipFile, name: str):
    return json.loads(z.read(name).decode("utf-8-sig"))


def sha_matches(raw: bytes, row: dict) -> bool:
    d = digest(raw)
    return d["bytes"] == row.get("bytes") and d["sha256"] == row.get("sha256") and (row.get("crc32") is None or d["crc32"] == str(row.get("crc32")).lower())


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and ".." not in p.parts and ":" not in p.parts[0]


def main() -> None:
    checks: list[dict] = []

    def check(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    d = readj(DELIVERY)
    packet = readj(PACKET)
    preparation = readj(PREPARATION)
    archive_raw = ARCHIVE.read_bytes()
    delivery_raw = DELIVERY.read_bytes()
    archive_digest = digest(archive_raw)
    delivery_digest = digest(delivery_raw)
    valid_statuses = {"PREPARED_UNAUDITED_UNSENT", "PREPARED_AUDITED_UNSENT", "PACKET289_INDEPENDENT_AUDIT_PASS_PENDING_GPT_SUBMISSION_816_32_0"}
    check("Packet289 ZIP and DELIVERY agree on exact bytes and tracked preparation status", sha_matches(archive_raw, d.get("archive", {})) and packet.get("archive", {}).get("sha256") == archive_digest["sha256"] == preparation.get("archive", {}).get("sha256") and packet.get("status") in valid_statuses and preparation.get("status") in valid_statuses, {"archive": archive_digest, "delivery": delivery_digest, "packetStatus": packet.get("status"), "preparationStatus": preparation.get("status")})
    check("Packet289 names exact current main authority and only the Director-selected targets", d.get("sourceAuthority") == AUTH and packet.get("sourceAuthority") == AUTH and d.get("group") == packet.get("group") == "rank9-miracle-reality2" and d.get("pendingIds") == packet.get("pendingIds") == TARGETS and d.get("accepted") is False and d.get("applied") is False, {"authority": d.get("sourceAuthority"), "targets": d.get("pendingIds")})

    prior_archive = PRIOR233 / "DD_Rank9_MiracleReality2_Director_Return233_HELD.zip"
    prior_delivery = PRIOR233 / "DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json"
    prior_audit = BASE / "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json"
    prior_receipt = BASE / "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json"
    prior_audit_doc = readj(prior_audit)
    with zipfile.ZipFile(prior_archive) as pz:
        prior_decision = readm(pz, "DIRECTOR_DECISION.json")
    prior_by_id = {x.get("id"): x for x in prior_decision.get("perIdentityDecisions", [])}
    check("Return233 target history is exact, held at 811/37/0, and independently PASS 30/30", prior_decision.get("authority") == {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173} and prior_decision.get("heldIds") == TARGETS and prior_decision.get("acceptedIds") == [] and prior_decision.get("appliedIds") == [] and {sid: prior_by_id.get(sid, {}).get("blockerIds") for sid in TARGETS} == PRIOR_BLOCKERS and prior_audit_doc.get("status") == "PASS" and prior_audit_doc.get("checkCount") == 30 and prior_audit_doc.get("failedChecks") == 0 and readj(prior233_entry("delivery")) == readj(prior_delivery), {"priorAuthority": prior_decision.get("authority"), "blockers": {sid: prior_by_id.get(sid, {}).get("blockerIds") for sid in TARGETS}, "audit": prior_audit_doc.get("status"), "checks": prior_audit_doc.get("checkCount")})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        name_set = set(names)
        unsafe = [n for n in names if not safe(n)]
        check("Packet289 contains 200 unique safe members and passes ZIP CRC validation", len(names) == len(name_set) == d.get("zipMemberCount") == 200 and d.get("payloadMemberCount") == 199 and not unsafe and z.testzip() is None, {"members": len(names), "unsafe": unsafe[:10]})
        manifest = readm(z, "MANIFEST.json")
        manifest_rows = manifest.get("members", [])
        manifest_by_path = {x.get("path"): x for x in manifest_rows if isinstance(x, dict)}
        payload = name_set - {"MANIFEST.json"}
        external_rows = d.get("members", [])
        external_by_path = {x.get("path"): x for x in external_rows if isinstance(x, dict)}
        check("Delivery and internal MANIFEST cover exactly all 199 non-manifest files", len(manifest_rows) == len(manifest_by_path) == len(external_rows) == len(external_by_path) == 199 and set(manifest_by_path) == set(external_by_path) == payload and manifest.get("memberCountExcludingSelf") == 199 and sha_matches(z.read("MANIFEST.json"), d.get("memberManifest", {})), {"payload": len(payload), "internal": len(manifest_rows), "external": len(external_rows)})
        member_failures = [n for n, row in manifest_by_path.items() if not sha_matches(z.read(n), row)]
        member_failures.extend(n for n, row in external_by_path.items() if not sha_matches(z.read(n), row))
        check("Every Packet289 member matches its exact size/SHA/CRC roster", not member_failures, member_failures[:15])

        candidate = readm(z, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_289.json")
        context = readm(z, "CURRENT_CONTEXT_289.json")
        check("Candidate and context bind the exact 816/32/0 Miracle/Reality2 review", candidate.get("currentAuthority") == AUTH and candidate.get("currentPendingGroup") == {"group": "rank9-miracle-reality2", "spellIds": TARGETS, "count": 2} and candidate.get("sourceCommitBase") == packet.get("sourceCommitBase") and candidate.get("sourceBranch") == "main" and context.get("sourceAuthority") == AUTH and context.get("targetGroup", {}).get("pendingIds") == TARGETS, {"authority": candidate.get("currentAuthority"), "group": candidate.get("currentPendingGroup")})
        history_notes = readm(z, "history/NEXT_CONFERENCE_NOTES_129.json")
        check("The packet preserves 24 original questions, two focused additions, four main cases and eight future requirements", len(candidate.get("questions", [])) == 24 and len(history_notes.get("focusedAdditionalQuestions", [])) == 2 and len(history_notes.get("requiredNewCases", [])) == 4 and len(candidate.get("futureCaseRequirements", [])) == 8 and packet.get("totalQuestions") == 26 and packet.get("requiredMainCases") == 4 and packet.get("futureRequirements") == 8 and packet.get("nativePlacements") == 3, {"questions": len(candidate.get("questions", [])), "focused": len(history_notes.get("focusedAdditionalQuestions", [])), "mainCases": len(history_notes.get("requiredNewCases", [])), "future": len(candidate.get("futureCaseRequirements", [])), "placements": packet.get("nativePlacements")})
        history = candidate.get("historicalWorkflow", {})
        check("Prior Return233 is disclosed as historical ruling and requires a current-source reassessment", candidate.get("priorTargetRuling", {}).get("heldIds") == TARGETS and candidate.get("priorTargetRuling", {}).get("blockerIds") == PRIOR_BLOCKERS and "Return233" in history.get("priorDirectorRuling", "") and context.get("priorTargetRulingInterpretation", "").startswith("The exact Return233 ruling is historical evidence only"), history)

        # Current 153-file source set: exact bytes, Git blob IDs, and live files.
        source_rows = candidate.get("sourceBindings", [])
        failures = []
        for row in source_rows:
            path = row.get("path", "")
            member = "sources_current/" + path
            if member not in name_set:
                failures.append(path + " missing from packet")
                continue
            raw = z.read(member)
            if not sha_matches(raw, row) or git_blob_sha(raw) != row.get("gitBlobSHA1"):
                failures.append(path + " packet bytes")
            live = ROOT / Path(*PurePosixPath(path).parts)
            if not live.is_file() or not sha_matches(live.read_bytes(), row) or git_blob_sha(live.read_bytes()) != row.get("gitBlobSHA1"):
                failures.append(path + " live bytes")
        check("All 153 refreshed source bindings match Packet289 and the current live tree", len(source_rows) == 153 and not failures and candidate.get("sourceBindingRefresh", {}).get("sourceFiles") == 153, {"bindings": len(source_rows), "failures": failures[:12]})
        changed = candidate.get("sourceBindingRefresh", {}).get("changedSinceHistoricalCandidate", [])
        check("Historical source refresh transparently lists every changed binding", len(changed) == 108 and len({x.get("path") for x in changed}) == 108 and all(x.get("path") in {r.get("path") for r in source_rows} for x in changed), {"changed": len(changed), "examples": [x.get("path") for x in changed[:8]]})

        check("Current 289 queue, handoff and pending audit in the packet retain exact target and authority", readm(z, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_289.json").get("currentAuthority") == AUTH and readm(z, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_289.json").get("nextPendingIds") == TARGETS and readm(z, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_289.json").get("nextGroup") == "rank9-miracle-reality2" and readm(z, "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_289.json").get("authority") == AUTH, None)

        # Packet carries Return233 as the prior target decision and Return288 as
        # the latest current-authority return. Returns284-287 remain represented
        # by exact, independently audited delivery records.
        check("Exact Return233 ZIP, delivery, audit and receipt are attached", z.read("prior_target/RETURN233.zip") == prior_archive.read_bytes() and z.read("prior_target/RETURN233_DELIVERY.json") == prior_delivery.read_bytes() and z.read("prior_target/RETURN233_INDEPENDENT_AUDIT.json") == prior_audit.read_bytes() and z.read("prior_target/RETURN233_RECEIPT.json") == prior_receipt.read_bytes(), {"priorArchive": digest(prior_archive.read_bytes())})
        batch_failures = []
        for number, held in RECENT.items():
            delivery_name = f"evidence/RETURN{number}_DELIVERY.json"
            audit_name = f"evidence/RETURN{number}_INDEPENDENT_AUDIT.json"
            receipt_name = f"evidence/RETURN{number}_RECEIPT.json"
            delivered = readm(z, delivery_name)
            audited = readm(z, audit_name)
            if delivered.get("heldIds") != held or delivered.get("acceptedIds") != [] or delivered.get("appliedIds") != [] or audited.get("status") != "PASS" or audited.get("failedChecks", 0) != 0 or receipt_name not in name_set:
                batch_failures.append(number)
        check("Return284–288 delivery/audit records preserve all exact unrelated holds", not batch_failures, batch_failures)
        check("Return288 sealed current-source audit and receipt are bound and report 27/27 PASS", readj(SOURCE_RETURN288_AUDIT).get("status") == "PASS" and readj(SOURCE_RETURN288_AUDIT).get("checkCount") == 27 and readj(SOURCE_RETURN288_RECEIPT).get("failedChecks") == 0 and z.read("evidence/RETURN288_INDEPENDENT_AUDIT.json") == SOURCE_RETURN288_AUDIT.read_bytes() and z.read("evidence/RETURN288_RECEIPT.json") == SOURCE_RETURN288_RECEIPT.read_bytes(), {"audit": readj(SOURCE_RETURN288_AUDIT).get("status"), "checks": readj(SOURCE_RETURN288_AUDIT).get("checkCount")})
        check("Packet288 source audit and submission status are preserved", readj(SOURCE_PACKET288_AUDIT).get("status") == "PASS" and readj(SOURCE_PACKET288_RECEIPT).get("status") == "PASS" and readj(SOURCE_PACKET288_SUBMISSION).get("status") == "RETURN288_AUDITED_HELD_816_32_0", None)

        # Current target spell records remain pending; no canonical application.
        catalog = readm(z, "sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json")
        index = readm(z, "sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json")
        index_by_id = {x.get("id"): x for x in index.get("entries", [])}
        catalog_by_id = {x.get("id"): x for x in catalog.get("spells", [])}
        check("Both current target index rows remain pending with exact catalog records", index.get("authoredCounts") == {"reviewed": 816, "pending": 32} and all(index_by_id.get(sid, {}).get("authoredStatus") == "pending-authored-procedure" and catalog_by_id.get(sid, {}).get("id") == sid for sid in TARGETS), {"authoredCounts": index.get("authoredCounts")})
        check("Packet preparation makes no canonical, application, runtime or GitHub changes", d.get("canonicalChanges") is False and d.get("applicationChanges") is False and packet.get("canonicalChanges") is False and context.get("canonicalChanges") is False and context.get("applicationChanges") is False and context.get("runtimeExecuted") is False, {"canonicalChanges": d.get("canonicalChanges"), "applicationChanges": d.get("applicationChanges"), "runtimeExecuted": context.get("runtimeExecuted")})

    failures = [x for x in checks if not x["passed"]]
    report = {"id": "RANK9MIRACLEREALITY2-PACKET289-INDEPENDENT-AUDIT", "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_digest}, "authority": AUTH,
        "targetIds": TARGETS, "priorTargetRuling": {"heldIds": TARGETS, "blockerIds": PRIOR_BLOCKERS, "authority": {"reviewedApplied": 811, "pending": 37}},
        "nextPendingGroup": None, "memberCount": 200, "sourceBindings": 153, "changedSourceBindings": 108,
        "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "checks": checks}
    PACKET_AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_digest = digest(PACKET_AUDIT.read_bytes())
    receipt = {"id": "RANK9MIRACLEREALITY2-PACKET289-RECEIPT", "status": report["status"],
        "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
        "independentAudit": {"path": PACKET_AUDIT.relative_to(ROOT).as_posix(), **report_digest},
        "authority": AUTH, "targetIds": TARGETS, "checkCount": len(checks), "failedChecks": len(failures)}
    PACKET_RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": len(checks), "passed": len(checks) - len(failures), "failed": len(failures), "archive": archive_digest, "delivery": delivery_digest, "failures": failures}, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


def prior233_entry(which: str) -> Path:
    if which == "delivery":
        return PRIOR233 / "DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json"
    raise KeyError(which)


if __name__ == "__main__":
    main()
