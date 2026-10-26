from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

import jsonpatch


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_deathrecovery7_return184_received"
ARCHIVE = RECEIVED / "DD_Rank9_DeathRecovery7_Director_Return184.zip"
DELIVERY = RECEIVED / "DD_Rank9_DeathRecovery7_Director_Return184_DELIVERY.json"
REPORT = AUDIT / "RANK9_DEATHRECOVERY7_RETURN184_INDEPENDENT_AUDIT.json"
COMMIT = "25273775f16cf9877c758b3b923f672e60d6a44b"
GROUP = [
    "doom",
    "soul-harvest",
    "final-word",
    "eternal-pact",
    "power-word-kill",
    "thread-severance",
    "wail-of-the-banshee",
]
ACCEPTED = ["soul-harvest", "power-word-kill", "thread-severance", "wail-of-the-banshee"]
UNACCEPTED = ["doom", "final-word", "eternal-pact"]
BLOCKERS = {"doom": "DR184-B03", "final-word": "DR184-B01", "eternal-pact": "DR184-B02"}

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


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{COMMIT}:{path}"], cwd=ROOT)


def git_blob_id(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{COMMIT}:{path}"], cwd=ROOT, text=True).strip()


def local_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8"))


def check(label: str, passed: bool, detail=None) -> None:
    row = {"check": label, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    if not passed:
        failures.append(label)


def json_pointer(value, pointer: str):
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer {pointer!r}")
    current = value
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def replay_case(case: dict) -> tuple[int, int, int]:
    state = copy.deepcopy(case["initialState"])
    assert sha(canonical(state)) == case["initialSHA256"]
    forward_ops = inverse_ops = 0
    for ordinal, event in enumerate(case["events"], 1):
        before = copy.deepcopy(state)
        assert event["id"] == f'{case["id"]}:{ordinal}'
        assert event["before"] == before
        assert sha(canonical(before)) == event["beforeSHA256"]
        after = jsonpatch.JsonPatch(event["operations"]).apply(copy.deepcopy(before), in_place=False)
        assert after == event["after"]
        assert sha(canonical(after)) == event["afterSHA256"]
        restored = jsonpatch.JsonPatch(event["inverseOperations"]).apply(copy.deepcopy(after), in_place=False)
        assert restored == before
        forward_ops += len(event["operations"])
        inverse_ops += len(event["inverseOperations"])
        state = after
    assert state == case["finalState"]
    assert sha(canonical(state)) == case["finalSHA256"]
    for assertion in case.get("assertions", []):
        assert set(assertion) == {"equals", "path"}, assertion
        assert json_pointer(state, assertion["path"]) == assertion["equals"], assertion
    return len(case["events"]), forward_ops, inverse_ops


def verify() -> dict:
    delivery = local_json(DELIVERY)
    expected_zip_bytes = delivery["archive"]["bytes"]
    expected_zip_sha = delivery["archive"]["sha256"]
    actual_bytes = ARCHIVE.stat().st_size
    actual_sha = sha_file(ARCHIVE)
    check("Return184 archive matches delivery byte count and SHA-256", actual_bytes == expected_zip_bytes and actual_sha == expected_zip_sha, {"bytes": actual_bytes, "sha256": actual_sha})

    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        check("ZIP CRC scan succeeds and member names are unique", archive.testzip() is None and len(names) == len(set(names)), {"members": len(names)})
        unsafe = [n for n in names if n.startswith(("/", "\\")) or ".." in Path(n.replace("\\", "/")).parts or any(p.startswith(".") for p in n.replace("\\", "/").split("/")) or any(x in n.lower() for x in (".tmp", ".temp", "~$"))]
        check("ZIP members contain no traversal, hidden, or temporary paths", not unsafe, unsafe[:20])

        internal = member_json(archive, "MEMBER_MANIFEST.json")
        bindings = delivery["allMemberBindings"]
        by_path = {row["path"]: row for row in bindings}
        check("Delivery manifest binds every unique archive member exactly once", len(by_path) == len(bindings) == len(names) and set(by_path) == set(names), {"archiveMembers": len(names), "bindings": len(bindings)})
        failures_by_member = []
        for path, binding in by_path.items():
            info = archive.getinfo(path)
            digest = hashlib.sha256()
            size = 0
            crc = 0
            with archive.open(path) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(block)
                    digest.update(block)
                    crc = zlib.crc32(block, crc)
            observed = {"bytes": size, "sha256": digest.hexdigest(), "crc32": f"{crc & 0xffffffff:08x}"}
            required = {"bytes": binding["bytes"], "sha256": binding["sha256"], "crc32": binding["crc32"].lower()}
            if observed != required or info.file_size != binding["bytes"] or info.CRC != crc & 0xffffffff:
                failures_by_member.append({"path": path, "observed": observed, "expected": required})
        check("Every archive member matches delivered size, SHA-256, and CRC32", not failures_by_member, failures_by_member[:5])

        internal_members = {row["path"]: row for row in internal["members"]}
        external_members = {path: row for path, row in by_path.items() if path != "MEMBER_MANIFEST.json"}
        check("Internal manifest is an exact self-excluding 189-member binding", internal.get("memberCountExcludingSelf") == 189 and len(internal_members) == 189 and set(internal_members) == set(external_members), {"internal": len(internal_members), "external": len(external_members)})
        internal_mismatch = []
        for path, row in internal_members.items():
            ext = external_members.get(path, {})
            if any(row.get(k) != ext.get(k) for k in ("bytes", "sha256", "crc32")):
                internal_mismatch.append(path)
        check("Internal member hashes, sizes and CRCs match the external delivery manifest", not internal_mismatch, internal_mismatch[:10])
        check("Internal manifest SHA-256 matches the delivery manifest", sha(archive.read("MEMBER_MANIFEST.json")) == delivery["memberManifestSHA256"])

        counts = delivery["counts"]
        check("Director package checks report full pass", delivery["packageChecks"]["status"] == "PASS" and all(delivery["packageChecks"].get(k) is True for k in ("allCRC32", "allLocalMemberRoundTrips", "allMemberSizesAndSHA256", "exactAllowlist", "originalSourceCandidateArchiveByteExact")) and delivery["packageChecks"].get("hiddenOrTempMembers") == 0)
        check("Delivery manifest is explicit that nothing was applied and canonical files were not edited", delivery["applied"] is False and delivery["applicationClaimed"] is False and delivery["canonicalFilesEdited"] is False)
        check("Director delivery and local source are bound to the current reviewed commit", delivery["sourceCommit"] == COMMIT and member_json(archive, "CURRENT_CONTEXT_184.json")["commit"] == COMMIT)

        source_bindings = member_json(archive, "SOURCE_BINDINGS.json")
        check("Bound source record identifies the exact current commit", source_bindings["commit"] == COMMIT)
        current_file_failures = []
        for binding in source_bindings["currentFiles"]:
            path = binding["path"]
            raw = archive.read(path)
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"]:
                current_file_failures.append({"path": path, "error": "snapshot hash mismatch"})
                continue
            if binding.get("gitBlobSHA1"):
                prefix = "evidence/current/"
                if not path.startswith(prefix):
                    current_file_failures.append({"path": path, "error": "git-bound source is not under evidence/current"})
                    continue
                git_path = path[len(prefix):]
                actual = git_blob(git_path)
                if len(actual) != binding["bytes"] or sha(actual) != binding["sha256"] or git_blob_id(git_path) != binding["gitBlobSHA1"]:
                    current_file_failures.append({"path": path, "error": "current Git source mismatch"})
        check("All 50 evidence snapshots match their byte/hash bindings and all Git-bound sources match the exact commit", not current_file_failures, current_file_failures[:10])

        git_fetch_failures = []
        fetch_bindings = source_bindings["freshGitFetchBindings"]
        for binding in fetch_bindings:
            path = binding["path"]
            try:
                actual = git_blob(path)
                snapshot_path = "evidence/current/" + path
                if path.endswith("/rank9_death_recovery_7_source_conference_01.json"):
                    snapshot_path = "SOURCE_CONFERENCE_CANDIDATE_01.json"
                elif path.endswith("/DD_Rank9_Death_Recovery_7_Source_Conference_01.zip"):
                    snapshot_path = "SOURCE_CONFERENCE_ARCHIVE_01.zip"
                if snapshot_path not in names:
                    snapshot_path = path
                snapshot = archive.read(snapshot_path)
            except Exception as exc:
                git_fetch_failures.append({"path": path, "error": str(exc)})
                continue
            if len(actual) != binding["bytes"] or sha(actual) != binding["sha256"] or git_blob_id(path) != binding["gitBlobSHA1"] or snapshot != actual:
                git_fetch_failures.append({"path": path, "error": "fresh Git fetch not byte-identical to snapshot/binding"})
        check("All fresh Git source fetch bindings reproduce from the pinned commit", not git_fetch_failures, git_fetch_failures[:10])

        source_archive_raw = archive.read("SOURCE_CONFERENCE_ARCHIVE_01.zip")
        source_candidate_raw = archive.read("SOURCE_CONFERENCE_CANDIDATE_01.json")
        source_archive_path = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Death_Recovery_7_Source_Conference_01.zip"
        source_candidate_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_death_recovery_7_source_conference_01.json"
        local_source_archive = git_blob(source_archive_path.relative_to(ROOT).as_posix())
        local_source_candidate = git_blob(source_candidate_path.relative_to(ROOT).as_posix())
        check("Source conference ZIP and candidate are byte-exact copies of current Git source", source_archive_raw == local_source_archive and source_candidate_raw == local_source_candidate and sha(source_archive_raw) == "1869e49888e9ebfea76c1d660ab2cb7dc4ace2f6f64c471d8487c93480b167d8" and sha(source_candidate_raw) == "e6ea3fd27360b1af713aec7b798e1bc51fe454791a9749ef895db244b1986a1f")
        source_archive_members = source_bindings["sourceArchiveMembersVerified"]
        archive_source_failures = []
        import io
        with zipfile.ZipFile(io.BytesIO(source_archive_raw)) as source_archive:
            for binding in source_archive_members:
                try:
                    raw = source_archive.read(binding["archiveMember"])
                except Exception as exc:
                    archive_source_failures.append({"path": binding["archiveMember"], "error": str(exc)})
                    continue
                if not binding.get("pass") or len(raw) != binding["bytes"] or sha(raw) != binding["sha256"]:
                    archive_source_failures.append({"path": binding["archiveMember"], "error": "source archive binding mismatch"})
        check("All 74 original source-conference member bindings verify", len(source_archive_members) == 74 and not archive_source_failures, archive_source_failures[:10])

        candidate = member_json(archive, "SOURCE_CONFERENCE_CANDIDATE_01.json")
        candidate_ids = [row["spellId"] for row in candidate["records"]]
        check("The fresh source conference covers exactly the seven queued identities", candidate_ids == GROUP)

        decision = member_json(archive, "DIRECTOR_DECISION.json")
        procedure_doc = member_json(archive, "PROCEDURES.json")
        decision_rows = decision["decisions"]
        decision_map = {row["id"]: row for row in decision_rows}
        package_accepted = [row["id"] for row in decision_rows if row["accepted"]]
        package_unaccepted = [row["id"] for row in decision_rows if not row["accepted"]]
        check("Director decided the exact seven queued identities and accepted exactly four", set(decision_map) == set(GROUP) and set(package_accepted) == set(ACCEPTED) and set(package_unaccepted) == set(UNACCEPTED) and decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == UNACCEPTED)
        check("No director decision claims application or canonical mutation", decision["applied"] is False and decision["canonicalFilesEdited"] is False and all(not row["applied"] for row in decision_rows))
        check("No accepted identity carries a blocker; the three held identities have their exact blocker IDs", all(not decision_map[s]["blockerIds"] for s in ACCEPTED) and all(decision_map[s]["blockerIds"] == [BLOCKERS[s]] for s in UNACCEPTED))
        procedure_map = {row["id"]: row for row in procedure_doc["spells"]}
        check("Procedure dossier identities and per-identity decisions agree", set(procedure_map) == set(GROUP) and all(procedure_map[s]["accepted"] is True and procedure_map[s]["applied"] is False for s in ACCEPTED) and all(procedure_map[s]["accepted"] is False and procedure_map[s]["applied"] is False for s in UNACCEPTED))

        for source, local in ((delivery["perIdentityDecisions"], decision_rows),):
            compact = [{k: row[k] for k in ("id", "accepted", "applied", "blockerIds")} for row in local]
            check("Delivery and embedded director decision agree exactly per identity", source == compact)

        sem = member_json(archive, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        check("Independent semantic check has no semantic failures and preserves exactly three required-evidence holds", sem["applied"] is False and sem["scopedSemanticFailures"] == 0 and sem["exactAcceptedIds"] == ACCEPTED and len(sem["blockers"]) == 3 and {b["id"] for b in sem["blockers"]} == set(BLOCKERS.values()) and all(not b["accepted"] and not b["applied"] for b in sem["blockers"]))

        data_integrity = member_json(archive, "DATA_INTEGRITY_CHECK.json")
        case_index = member_json(archive, "CASE_INDEX.json")["cases"]
        coverage = member_json(archive, "COVERAGE.json")
        case_results = {row["id"]: row for row in data_integrity["caseResults"]}
        check("All 103 case entries report passed data-integrity checks", len(case_results) == len(case_index) == 103 and all(row["passed"] for row in case_results.values()) and data_integrity["failureCount"] == 0 and data_integrity["passedChecks"] == data_integrity["checks"] == 39088)
        check("Coverage inventory preserves every original question and future obligation", len(coverage["questions"]) == 22 and len(coverage["originalFutureObligations"]) == 9 and coverage["allOriginalQuestionsSelected"] is True)

        accepted_case_ids = set()
        for sid in ACCEPTED:
            row = decision_map[sid]
            proc = procedure_map[sid]
            ids = row["caseIds"]
            check(f"{sid}: complete source-bound procedure has no held cases", bool(proc["procedure"]) and ids and all(not case_index[[c["id"] for c in case_index].index(cid)]["holdIds"] for cid in ids))
            accepted_case_ids.update(ids)
        check("Accepted cases are unique and all belong to the exact four accepted identities", len(accepted_case_ids) == sum(len(decision_map[s]["caseIds"]) for s in ACCEPTED))

        total_cases = total_events = total_reversible_ops = 0
        accepted_events = accepted_forward_ops = accepted_inverse_ops = 0
        case_failures = []
        accepted_case_count = 0
        for index_row in case_index:
            path = index_row["member"]
            try:
                case = member_json(archive, path)
                raw = archive.read(path)
                events = len(case["events"])
                if case["id"] != index_row["id"] or case["spellId"] != index_row["spellId"] or case["status"] != index_row["status"] or events != index_row["events"] or sha(raw) != index_row["memberSHA256"]:
                    raise AssertionError("case-index/member mismatch")
                if case["status"] != "COMPLETE_CONDITIONAL_AUTHORED_TRACE" and case["status"] != "HELD_REQUIRED_SOURCE_FACT":
                    raise AssertionError(f"unexpected case status {case['status']}")
                total_cases += 1
                total_events += events
                total_reversible_ops += sum(len(e["operations"]) + len(e["inverseOperations"]) for e in case["events"])
                if case["id"] in accepted_case_ids:
                    if case["spellId"] not in ACCEPTED or case["holdIds"] or case["status"] != "COMPLETE_CONDITIONAL_AUTHORED_TRACE":
                        raise AssertionError("accepted case has hold or wrong status")
                    n, fwd, inv = replay_case(case)
                    accepted_case_count += 1
                    accepted_events += n
                    accepted_forward_ops += fwd
                    accepted_inverse_ops += inv
            except Exception as exc:
                case_failures.append({"case": index_row.get("id"), "error": f"{type(exc).__name__}: {exc}"})
        check("All case files match their index identities, statuses, events and member hashes", not case_failures, case_failures[:10])
        check("All accepted cases independently replay forward and inverse with full state hashes and assertions", not case_failures and accepted_case_count == len(accepted_case_ids) == 58 and accepted_events == 1031 and accepted_forward_ops + accepted_inverse_ops > 0, {"cases": accepted_case_count, "events": accepted_events, "forwardOperations": accepted_forward_ops, "inverseOperations": accepted_inverse_ops})
        check("Case and reversible-operation counts match the delivered package", total_cases == 103 and total_events == 2074 and total_reversible_ops == counts["eventOperations"] == 8296, {"cases": total_cases, "events": total_events, "reversibleEventOperations": total_reversible_ops})
        check("Accepted trace count and delivered total reversible operations reconcile", accepted_case_count == 58 and total_reversible_ops + counts["proposalOperations"] == counts["totalReversibleOperations"] == 8324)

    # Verify the source authority and queue against the actual committed records.
    handoff_path = AUDIT / "CURRENT_HANDOFF_182.json"
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_182.json"
    pending_path = AUDIT / "CURRENT89_PENDING_IDENTITY_AUDIT_182.json"
    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    handoff = local_json(handoff_path)
    queue = local_json(queue_path)
    pending = local_json(pending_path)
    index = local_json(index_path)
    catalog = local_json(catalog_path)
    actual_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    by_group = {row["group"]: row for row in queue["currentPendingGroups"]}
    check("Current handoff, queue and pending audit agree on 759/89/0", handoff["currentAuthority"] == queue["currentAuthority"] == {"reviewedApplied": 759, "pending": 89, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 483, "scopedInterfaces": 173} and pending["pendingCount"] == 89 and len(actual_pending) == 89 and set(pending["pendingIds"]) == actual_pending)
    check("DeathRecovery7 is exactly the next seven pending IDs in the current queue", by_group["rank9-death-recovery7"]["pendingIds"] == GROUP and set(GROUP) <= actual_pending)
    check("The previous three Psychic Fear identities remain pending and are not in this packet", {"psychic-scream", "mass-phantom-killer", "weird"} <= actual_pending and not ({"psychic-scream", "mass-phantom-killer", "weird"} & set(GROUP)))
    counts_before = index["authoredCounts"]
    check("Canonical authored index and catalog are still bound to the exact source commit", counts_before == {"reviewed": 759, "pending": 89} and index["sourceCatalogSha256"] == sha(git_blob("DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json")))
    catalog_ids = {row["id"] for row in catalog.get("spells", [])}
    check("All seven in-scope identities remain in the current catalog", set(GROUP) <= catalog_ids)
    rows = {row["id"]: row for row in index["entries"]}
    check("All seven decisions target pending authored statuses with unchanged native/source status", all(rows[s]["authoredStatus"] == "pending-authored-procedure" and rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in GROUP))

    authority = delivery["sourceAuthority"]
    check("Director return retains the actual pre-application authority", authority == {"acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 483, "pending": 89, "reviewedApplied": 759, "scopedInterfaces": 173})
    check("Static acceptance is not runtime/source/balance/release approval", len(delivery["qualifications"]) >= 6 and delivery["libraryArtifactVerification"]["status"] == "PASS")

    report = {
        "id": "RANK9-DEATHRECOVERY7-RETURN184-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "accepted": True if not failures else False,
        "applied": False,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "unacceptedBlockers": BLOCKERS,
        "sourceAuthority": authority,
        "sourceCommit": COMMIT,
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": actual_bytes, "sha256": actual_sha, "members": len(names)},
        "independentReplay": {"acceptedCases": accepted_case_count, "acceptedEvents": accepted_events, "forwardOperations": accepted_forward_ops, "inverseOperations": accepted_inverse_ops, "failures": case_failures},
        "checksPassed": sum(c["passed"] for c in checks),
        "checksFailed": sum(not c["passed"] for c in checks),
        "failures": failures,
        "checks": checks,
        "qualifications": delivery["qualifications"],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = verify()
    print(json.dumps({k: result[k] for k in ("status", "acceptedIds", "unacceptedIds", "sourceAuthority", "archive", "independentReplay", "checksPassed", "checksFailed", "failures")}, ensure_ascii=False, indent=2))
