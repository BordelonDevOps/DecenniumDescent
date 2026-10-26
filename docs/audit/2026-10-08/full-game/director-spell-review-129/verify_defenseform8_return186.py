from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import jsonpatch


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_defenseform8_return186_received"
ARCHIVE = RECEIVED / "DD_Rank9_DefenseForm8_Director_Return186.zip"
DELIVERY = RECEIVED / "DD_Rank9_DefenseForm8_Director_Return186_DELIVERY.json"
INPUT_PACKET = AUDIT / "rank9_defenseform8_return185_prepared/DD_Rank9_DefenseForm8_CurrentSource_185.zip"
REPORT = AUDIT / "RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json"
SOURCE_COMMIT = "a88d9cd4177cab3d4f6dbaa2fef55876699b626c"
PUBLISH_COMMIT = "3b97f1e7"
GROUP = ["absolute-immunity", "astral-shell", "divine-shield", "eternal-protection", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]
ACCEPTED = ["astral-shell", "divine-shield", "eternal-protection"]
UNACCEPTED = ["absolute-immunity", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]
BLOCKERS = {
    "absolute-immunity": ["DF186-H-TRACKS"],
    "elemental-shell": ["DF186-H-NULL", "DF186-H-ENV", "DF186-H-COMPANION"],
    "body-to-void": ["DF186-H-OCCUPIED"],
    "timeless-form": ["DF186-H-AGING", "DF186-H-TIMESTOP"],
    "invulnerable-sphere": ["DF186-H-PLANAR", "DF186-H-CONTROL"],
}
QUALIFICATIONS = ["DF186-QH-SOURCE-ACCESS", "DF186-QH-CONTENT-PHYSICAL", "DF186-QH-RUNTIME", "DF186-QH-HUMAN-PLAY", "DF186-QH-BALANCE", "DF186-QH-COSMOLOGY", "DF186-QH-DOMAIN-CLOSURE", "DF186-QH-RELEASE", "DF186-QH-INHERITED"]
PRIOR_HELD = ["psychic-scream", "mass-phantom-killer", "weird", "doom", "final-word", "eternal-pact"]
NEXT_IDS = ["greater-spell-turning", "nullification-wave", "eternal-ward", "ultimate-ward", "reality-anchor", "prismatic-sphere"]

checks: list[dict] = []
failures: list[str] = []


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def local_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member_json(archive: zipfile.ZipFile, name: str):
    with archive.open(name) as stream:
        return json.load(stream)


def check(label: str, passed: bool, detail=None) -> None:
    row = {"check": label, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    if not passed:
        failures.append(label)


def pointer(value, path: str):
    current = value
    for part in path.removeprefix("/").split("/"):
        if not part:
            continue
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def replay(case: dict) -> tuple[int, int, int]:
    state = case["initialState"]
    if sha(canonical(state)) != case["initialSHA256"]:
        raise AssertionError("initial state hash mismatch")
    fwd_ops = inv_ops = 0
    for event in case["events"]:
        before = event["beforeState"]
        after = event["afterState"]
        if state != before or sha(canonical(before)) != event["beforeSHA256"] or sha(canonical(after)) != event["afterSHA256"]:
            raise AssertionError(f"event {event.get('id')} before/after state mismatch")
        calculated = jsonpatch.JsonPatch(event["forward"]).apply(before, in_place=False)
        if calculated != after:
            raise AssertionError(f"event {event.get('id')} forward patch mismatch")
        restored = jsonpatch.JsonPatch(event["inverse"]).apply(after, in_place=False)
        if restored != before:
            raise AssertionError(f"event {event.get('id')} inverse patch mismatch")
        fwd_ops += len(event["forward"])
        inv_ops += len(event["inverse"])
        state = after
    if state != case["finalState"] or sha(canonical(state)) != case["finalSHA256"]:
        raise AssertionError("final state mismatch")
    return len(case["events"]), fwd_ops, inv_ops


def verify() -> dict:
    delivery = local_json(DELIVERY)
    archive_size = ARCHIVE.stat().st_size
    archive_sha = sha_file(ARCHIVE)
    check("Saved Return186 ZIP size and SHA-256 equal the delivery record", archive_size == delivery["archive"]["bytes"] == 29_814_865 and archive_sha == delivery["archive"]["sha256"] == "d9894a0b250bb750f10beaf9f16a8e21a22c7486e838817ea3746d0a7b17d151", {"bytes": archive_size, "sha256": archive_sha})
    check("Delivery record binds the exact source and publishing commits", delivery["currentSourceCommit"] == SOURCE_COMMIT and delivery["publishingCommit"] == PUBLISH_COMMIT)
    check("Delivery baseline is 763/85/0 with 487 complete procedures and 173 scoped interfaces", delivery["baselineAuthority"] == {"reviewedApplied": 763, "pending": 85, "acceptedUnapplied": 0, "completeStandaloneProcedures": 487, "scopedInterfaces": 173})
    check("Delivery record authorizes exactly three unapplied IDs and holds the other five", delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED and delivery["applied"] is False and delivery["appliedIds"] == [] and delivery["canonicalFilesEdited"] is False and delivery["applicationPerformed"] is False)

    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        check("Return186 ZIP passes CRC scan and has unique member names", archive.testzip() is None and len(names) == len(set(names)) == delivery["archive"]["memberCount"] == 255, {"members": len(names)})
        unsafe = [name for name in names if name.startswith(("/", "\\")) or ".." in PurePosixPath(name.replace("\\", "/")).parts or any(part.startswith(".") for part in name.replace("\\", "/").split("/")) or any(token in name.lower() for token in (".tmp", ".temp", "~$"))]
        check("Return186 contains no traversal, hidden, or temporary members", not unsafe, unsafe[:20])

        internal = member_json(archive, "MEMBER_MANIFEST.json")
        internal_rows = internal["members"]
        internal_map = {row["path"]: row for row in internal_rows}
        delivery_rows = delivery["members"]
        delivery_map = {row["path"]: row for row in delivery_rows}
        check("Internal member manifest is exact and self-excluding", internal["payloadMemberCount"] == 254 and internal["manifestSelfExcluded"] == "MEMBER_MANIFEST.json is bound by the separate delivery record, together with every payload member. No recursive self-hash is claimed." and len(internal_map) == 254 and set(internal_map) == set(names) - {"MEMBER_MANIFEST.json"})
        check("Delivery manifest binds every archive member exactly once", len(delivery_map) == len(delivery_rows) == len(names) and set(delivery_map) == set(names))
        member_errors = []
        internal_errors = []
        for name in names:
            digest = hashlib.sha256()
            size = crc = 0
            with archive.open(name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(block)
                    digest.update(block)
                    crc = zlib.crc32(block, crc)
            crc_hex = f"{crc & 0xffffffff:08x}"
            row = delivery_map.get(name, {})
            if (size, digest.hexdigest(), crc_hex) != (row.get("bytes"), row.get("sha256"), str(row.get("crc32", "")).lower()) or archive.getinfo(name).CRC != crc & 0xffffffff:
                member_errors.append(name)
            if name != "MEMBER_MANIFEST.json":
                irow = internal_map.get(name, {})
                if (size, digest.hexdigest(), crc_hex) != (irow.get("bytes"), irow.get("sha256"), str(irow.get("crc32", "")).lower()):
                    internal_errors.append(name)
        check("All 255 archive members independently match delivered byte, SHA-256, and CRC bindings", not member_errors, member_errors[:10])
        check("All 254 payload members independently match the internal manifest", not internal_errors, internal_errors[:10])

        decision = member_json(archive, "DIRECTOR_DECISION_186.json")
        semantic = member_json(archive, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        procedures_doc = member_json(archive, "PROCEDURES.json")
        procedure_files = {sid: member_json(archive, f"procedures/{sid}.json") for sid in GROUP}
        case_index_doc = member_json(archive, "CASE_INDEX.json")
        case_index = case_index_doc["cases"]
        case_index_map = {row["id"]: row for row in case_index}
        decision_map = {row["spellId"]: row for row in decision["perIdentityDecisions"]}
        delivery_decisions = {row["spellId"]: row for row in delivery["perIdentityDecisions"]}
        check("Director decision, delivery, and independent semantic check agree on all eight identity dispositions", set(decision_map) == set(GROUP) and set(delivery_decisions) == set(GROUP) and semantic["acceptedIds"] == ACCEPTED and semantic["unacceptedIds"] == UNACCEPTED and semantic["appliedIds"] == [] and decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == UNACCEPTED and decision["appliedIds"] == [] and all(decision_map[s]["accepted"] is True and decision_map[s]["applied"] is False for s in ACCEPTED) and all(decision_map[s]["accepted"] is False and decision_map[s]["applied"] is False for s in UNACCEPTED))
        identity_errors = []
        for sid in GROUP:
            drow = decision_map[sid]
            vrow = delivery_decisions[sid]
            pfile = procedure_files[sid]
            if (vrow["accepted"], vrow["applied"], vrow["procedureSHA256"], vrow["blockerHoldIds"], vrow["caseIds"]) != (drow["accepted"], drow["applied"], drow["procedureSHA256"], drow["blockerHoldIds"], drow["caseIds"]):
                identity_errors.append({"spellId": sid, "error": "delivery/decision mismatch"})
            if pfile["spellId"] != sid or pfile["accepted"] != drow["accepted"] or pfile["applied"] is not False or sha(archive.read(drow["procedurePath"])) != drow["procedureSHA256"]:
                identity_errors.append({"spellId": sid, "error": "procedure file or SHA mismatch"})
            if sid in ACCEPTED and (pfile["holds"] or drow["blockerHoldIds"]):
                identity_errors.append({"spellId": sid, "error": "accepted identity has blocking hold"})
            if sid in UNACCEPTED and drow["blockerHoldIds"] != BLOCKERS[sid]:
                identity_errors.append({"spellId": sid, "error": "exact blocker IDs differ"})
            for case_id in drow["caseIds"]:
                cindex = case_index_map.get(case_id)
                if not cindex or cindex["spellId"] != sid:
                    identity_errors.append({"spellId": sid, "caseId": case_id, "error": "case reference absent or wrong spell"})
                elif sid in ACCEPTED and (cindex["holds"] or cindex["coverageHoldIds"] or cindex["status"] != "DEMONSTRATED_STATIC_FIXTURE"):
                    identity_errors.append({"spellId": sid, "caseId": case_id, "error": "accepted case is held or not demonstrated"})
        check("Per-identity procedure hashes, blocker lists, and complete accepted case bindings agree", not identity_errors, identity_errors[:12])
        proc_rows = {row["spellId"]: row for row in procedures_doc["spells"]}
        check("Standalone procedure dossier covers exactly eight IDs and marks all three acceptances unapplied", set(proc_rows) == set(GROUP) and all(proc_rows[s]["accepted"] is (s in ACCEPTED) and proc_rows[s]["applied"] is False for s in GROUP))
        check("Every accepted procedure preserves the native unmodified catalog card and class access", all(proc_rows[s]["nativeCardAndAccessUnchanged"] == next(row for row in json.loads(git_blob(SOURCE_COMMIT, "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))["spells"] if row["id"] == s) for s in ACCEPTED))

        hold_register = member_json(archive, "HOLD_REGISTER.json")
        blocking = [row for row in hold_register["holds"] if row["kind"] == "BLOCKER" and row["blocksAcceptance"]]
        hold_map = {row["id"]: row for row in hold_register["holds"]}
        check("Nine exact unresolved blockers cover the five held identities; nine separate qualification/inherited holds remain", hold_register["count"] == 18 and hold_register["blockingCount"] == len(blocking) == 9 and hold_register["qualificationAndInheritedCount"] == 9 and {row["id"] for row in blocking} == {h for hs in BLOCKERS.values() for h in hs} and hold_register["priorHeldIdentitiesUnchanged"] == PRIOR_HELD)
        check("Every held spell blocker is unresolved and does not invent positive evidence", all(hold_map[h]["state"] == "RETAINED_UNRESOLVED" and hold_map[h]["noInventedPositivePremise"] is True for hs in BLOCKERS.values() for h in hs))
        check("All nine source/runtime/play/balance/cosmology/closure/release qualification holds remain", all(all(h in decision_map[s]["qualificationHoldIds"] for h in QUALIFICATIONS) for s in GROUP))

        data_check = member_json(archive, "DATA_INTEGRITY_AND_SCOPED_SEMANTIC_CHECK.json")
        doc_check = member_json(archive, "DOCUMENT_AND_COVERAGE_CHECK.json")
        summary = member_json(archive, "VALIDATION_SUMMARY.json")
        check("Director data and semantic checks report zero failures", data_check["checks"] == data_check["passed"] == 74_628 and data_check["failed"] == 0 and not data_check["failures"] and len(data_check["caseResults"]) == 107 and all(row["checks"] > 0 for row in data_check["caseResults"]))
        check("Director document and coverage checks report zero failures", doc_check["checks"] == doc_check["passed"] == 739 and doc_check["failed"] == 0 and all(row["passed"] for row in doc_check["results"]))
        check("Summary records the requested 107-case scope, 2,310 events, 9,240 forward/inverse operations and next ward-control group", summary["counts"]["caseCount"] == 107 and summary["counts"]["eventCount"] == 2310 and summary["counts"]["eventOperationCount"] == 9240 and summary["inverseResult"] == {"events": 2310, "forwardOperations": 4620, "inverseOperations": 4620, "allExactReplaysPass": True} and summary["nextQueueGroup"]["groupUnchanged"]["group"] == "rank9-ward-control6" and summary["nextQueueGroup"]["groupUnchanged"]["pendingIds"] == NEXT_IDS)

        casebook = member_json(archive, "CASEBOOK.json")
        cases = casebook["cases"]
        case_map = {row["id"]: row for row in cases}
        all_events = sum(len(row["events"]) for row in cases)
        all_ops = sum(len(event["forward"]) + len(event["inverse"]) for row in cases for event in row["events"])
        case_errors = []
        for row in case_index:
            case = case_map.get(row["id"])
            if not case or case["spellId"] != row["spellId"] or case["status"] != row["status"] or len(case["events"]) != row["eventCount"]:
                case_errors.append(row["id"])
        accepted_case_ids = [cid for sid in ACCEPTED for cid in decision_map[sid]["caseIds"]]
        replay_cases = replay_events = forward_ops = inverse_ops = 0
        replay_errors = []
        for cid in accepted_case_ids:
            try:
                events, fwd, inv = replay(case_map[cid])
                replay_cases += 1
                replay_events += events
                forward_ops += fwd
                inverse_ops += inv
            except Exception as exc:
                replay_errors.append({"caseId": cid, "error": f"{type(exc).__name__}: {exc}"})
        check("All 107 case-index rows match the casebook identities, statuses, and event counts", not case_errors and len(cases) == len(case_index) == 107 and all_events == 2310 and all_ops == 9240, case_errors[:10])
        check("All 38 accepted cases independently pass forward and inverse state-hash replays", not replay_errors and replay_cases == len(set(accepted_case_ids)) == 38 and replay_events == 814 and forward_ops == inverse_ops and forward_ops + inverse_ops > 0, {"cases": replay_cases, "events": replay_events, "forwardOperations": forward_ops, "inverseOperations": inverse_ops, "errors": replay_errors[:5]})

        source_check = member_json(archive, "SOURCE_INTEGRITY_CHECK.json")
        source_scope = member_json(archive, "SOURCE_SCOPE_RECHECK.json")
        candidate = member_json(archive, "INPUT_PACKET/CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json")
        input_manifest = member_json(archive, "INPUT_PACKET/MANIFEST.json")
        packet_member_errors = []
        packet_rows = {row["path"]: row for row in input_manifest["members"]}
        packet_errors = []
        for name, row in packet_rows.items():
            member_name = "INPUT_PACKET/" + name
            if member_name not in names:
                packet_errors.append(name)
                continue
            info = archive.getinfo(member_name)
            if (info.file_size, f"{info.CRC:08x}") != (row["bytes"], row["crc32"].lower()):
                packet_errors.append(name)
                continue
            digest = hashlib.sha256()
            with archive.open(member_name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            if digest.hexdigest() != row["sha256"]:
                packet_errors.append(name)
        check("Embedded current-source packet has 101 self-excluding hash/CRC-verified payload members", input_manifest["sourceCommit"] == SOURCE_COMMIT and input_manifest["memberCountExcludingSelf"] == 101 and len(packet_rows) == 101 and not packet_errors, packet_errors[:10])
        embedded_packet = archive.read("INPUT_PACKET_ARCHIVE.zip")
        check("Embedded source packet ZIP is byte-exact to the committed input packet", len(embedded_packet) == INPUT_PACKET.stat().st_size and sha(embedded_packet) == sha_file(INPUT_PACKET) and embedded_packet == INPUT_PACKET.read_bytes())
        candidate_bindings = candidate["sourceBindings"]
        current_source_errors = []
        for binding in candidate_bindings:
            path = binding["path"]
            snap_path = "INPUT_PACKET/sources_current/" + path
            raw = archive.read(snap_path)
            expected = git_blob(SOURCE_COMMIT, path)
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"] or raw != expected or git_blob_id(SOURCE_COMMIT, path) != binding["gitBlobSHA1"]:
                current_source_errors.append(path)
        check("All 87 current source snapshots reproduce exact Git bytes and blob IDs at the source anchor", len(candidate_bindings) == 87 and candidate["currentSourceCommit"] == SOURCE_COMMIT and not current_source_errors, current_source_errors[:10])
        current_member_errors = []
        for row in input_manifest["members"]:
            if row["path"].startswith("current/"):
                path = row["path"][len("current/"):]
                if archive.read("INPUT_PACKET/" + row["path"]) != git_blob(SOURCE_COMMIT, path):
                    current_member_errors.append(path)
        check("All nine current context snapshots are exact Git blobs at the source anchor", not current_member_errors, current_member_errors[:10])
        supplemental = member_json(archive, "SUPPLEMENTAL_SOURCE_BINDINGS.json")
        supplemental_errors = []
        for binding in supplemental:
            ref = binding["ref"]
            path = binding["path"]
            raw = archive.read("SUPPLEMENTAL_CURRENT/" + path)
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"] or raw != git_blob(ref, path) or git_blob_id(ref, path) != binding["gitBlobSHA1"]:
                supplemental_errors.append(path)
        check("All 12 supplemental records reproduce their pinned Git blobs", len(supplemental) == 12 and not supplemental_errors, supplemental_errors[:10])
        check("Director source integrity check contains 188 successful bindings and no errors", len(source_check["checks"]) == 188 and all(any(row.get(key) is True for key in ("bytesSHA256CRC", "bytesSHA256GitBlob")) for row in source_check["checks"]) and source_check["errors"] == [])
        check("Source scope recheck anchors the current 763/85 packet at the correct source and publishing commits", source_scope["currentSourceCommit"] == SOURCE_COMMIT and source_scope["publishingCommit"] == PUBLISH_COMMIT and source_scope["authority"]["reviewedApplied"] == 763 and source_scope["authority"]["pending"] == 85)

        line_endings = member_json(archive, "SOURCE_LINE_ENDING_RECONCILIATION.json")
        catalog_path = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
        catalog_blob = git_blob(SOURCE_COMMIT, catalog_path)
        current_working = (ROOT / catalog_path).read_bytes()
        check("Catalog LF/CRLF reconciliation is an exact line-ending transform with no content substitution", line_endings["exactExpectedWorkingCopyMatched"] is True and line_endings["gitBlob"] == {"bytes": len(catalog_blob), "sha256": sha(catalog_blob)} and line_endings["handoffRecordedWorkingCopy"] == {"bytes": len(current_working), "sha256": sha(current_working)} and current_working == catalog_blob.replace(b"\n", b"\r\n"))

        compare = member_json(archive, "GITHUB_COMMIT_COMPARE.json")
        changed_paths = subprocess.check_output(["git", "diff", "--name-only", SOURCE_COMMIT, PUBLISH_COMMIT], cwd=ROOT, text=True).splitlines()
        check("Publishing commit adds only the seven review-packet/handoff files and no canonical source changes", compare["base"] == SOURCE_COMMIT and compare["head"] == PUBLISH_COMMIT and compare["status"] == "ahead" and compare["ahead_by"] == 1 and compare["behind_by"] == 0 and sorted(changed_paths) == sorted(["START_HERE.md", "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_185.json", "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_185.json", "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_PACKET_185.json", "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_SOURCE_PREPARATION_185.json", "docs/audit/2026-10-08/full-game/director-spell-review-129/prepare_defenseform8_return185.py", "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_defenseform8_return185_prepared/DD_Rank9_DefenseForm8_CurrentSource_185.zip"]))

        qualification = delivery["qualifications"]
        check("Static-only boundary and all source/access/runtime/play/balance/cosmology/closure/release gates remain unapproved", qualification["staticAuthoredReviewOnly"] is True and all(qualification[k] is False for k in ("runtimeExecuted", "suppliedOrHistoricalProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyApproved", "domainClosed", "releaseApproved", "canonicalFilesEdited", "applicationPerformed")))
        next_group = delivery["nextQueueGroup"]["groupUnchanged"]
        check("After this exact application, next group remains six Rank9 Ward/Control identities and needs a fresh packet", next_group["group"] == "rank9-ward-control6" and next_group["pendingIds"] == NEXT_IDS and next_group["pendingCount"] == 6 and next_group["freshPacketRequiredForCurrentAuthority"] is True)

    result = {
        "id": "RANK9-DEFENSEFORM8-RETURN186-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": sum(not row["passed"] for row in checks),
        "checks": checks,
        "failures": failures,
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha, "memberCount": delivery["archive"]["memberCount"]},
        "sourceAnchorCommit": SOURCE_COMMIT,
        "publishingCommit": PUBLISH_COMMIT,
        "baselineAuthority": delivery["baselineAuthority"],
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "appliedIds": [],
        "caseReplay": {"acceptedCases": replay_cases, "events": replay_events, "forwardOperations": forward_ops, "inverseOperations": inverse_ops},
        "blockerHoldIds": BLOCKERS,
        "priorHeldIdentitiesUnchanged": PRIOR_HELD,
        "nextQueueGroup": {"group": "rank9-ward-control6", "pendingIds": NEXT_IDS, "pendingCount": 6},
        "canonicalFilesEdited": False,
        "applicationPerformed": False,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = verify()
    print(json.dumps({k: output[k] for k in ("status", "checksPassed", "checksFailed", "acceptedIds", "unacceptedIds", "caseReplay", "failures", "archive", "nextQueueGroup")}, ensure_ascii=False, indent=2))
    if output["status"] != "PASS":
        raise SystemExit(1)
