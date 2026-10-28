from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RECEIVED = HERE / "rank9_illusionreality5_return207_received"
ARCHIVE = RECEIVED / "DD_Rank9_IllusionReality5_Director_Return207.zip"
DELIVERY = RECEIVED / "DD_Rank9_IllusionReality5_Director_Return207_DELIVERY.json"
OUT = HERE / "RANK9ILLUSIONREALITY5_RETURN207_INDEPENDENT_AUDIT.json"
BRANCH = "codex/ordinary-spell-review-complete"
ACCEPTED = ["supreme-illusion", "mirrored-world", "ethereal-disjunction", "illusory-reality"]
HELD = ["soul-reflection"]
GROUP_IDS = ACCEPTED + HELD
AUTHORITY = {"reviewedApplied": 798, "pending": 50, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 522, "scopedInterfaces": 173}
checks: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "passed": bool(ok), **({"detail": detail} if detail else {})})


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha(raw)


def member_digest(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    digest = hashlib.sha256()
    crc = 0
    size = 0
    with archive.open(name) as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return size, digest.hexdigest(), f"{crc & 0xffffffff:08x}"


def member_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8"))


def git_tree(commit: str, paths: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for start in range(0, len(paths), 40):
        batch = paths[start:start + 40]
        result = subprocess.run(
            ["git", "ls-tree", "-r", "-z", "--full-tree", commit, "--", *batch],
            cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for record in result.stdout.split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            _mode, kind, oid = header.decode("ascii").split(" ")
            if kind == "blob":
                found[raw_path.decode("utf-8")] = oid
    return found


def git_blobs(oids: list[str]) -> list[bytes]:
    if not oids:
        return []
    result = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT, check=True,
        input=("".join(oid + "\n" for oid in oids)).encode("ascii"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    data = result.stdout
    offset = 0
    blobs: list[bytes] = []
    for expected in oids:
        end = data.index(b"\n", offset)
        header = data[offset:end].decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise AssertionError(f"Unexpected git cat-file header: {header}")
        size = int(header[2])
        start = end + 1
        blob = data[start:start + size]
        if len(blob) != size or data[start + size:start + size + 1] != b"\n":
            raise AssertionError("Truncated git cat-file response")
        blobs.append(blob)
        offset = start + size + 1
    if offset != len(data):
        raise AssertionError("Unexpected trailing git cat-file bytes")
    return blobs


def verify_trace(doc: dict, expected_events: int) -> tuple[bool, int, int, str]:
    events = doc["events"]
    if len(events) != expected_events:
        return False, 0, 0, f"events={len(events)} expected={expected_events}"
    current = doc["initialState"]
    if canonical_sha(current) != doc["initialSHA256"]:
        return False, 0, 0, "initial state hash mismatch"
    forward_count = inverse_count = 0
    for position, event in enumerate(events, 1):
        before, after = event["before"], event["after"]
        fwd, inv = event["forward"], event["inverse"]
        ok = (
            before == current
            and canonical_sha(before) == event["beforeSHA256"]
            and canonical_sha(after) == event["afterSHA256"]
            and len(fwd) == len(inv) == 2
            and fwd[0] == {"op": "test", "path": "", "value": before}
            and fwd[1] == {"op": "replace", "path": "", "value": after}
            and inv[0] == {"op": "test", "path": "", "value": after}
            and inv[1] == {"op": "replace", "path": "", "value": before}
        )
        if not ok:
            return False, forward_count, inverse_count, f"event chain/operation mismatch at {position}"
        current = after
        forward_count += len(fwd)
        inverse_count += len(inv)
    ok = current == doc["finalState"] and canonical_sha(current) == doc["finalSHA256"]
    return ok, forward_count, inverse_count, "" if ok else "final state mismatch"


def main() -> None:
    delivery_raw = DELIVERY.read_bytes()
    delivery = json.loads(delivery_raw.decode("utf-8"))
    archive_size = ARCHIVE.stat().st_size
    archive_sha = sha(ARCHIVE.read_bytes())
    check("outer archive matches exact adjacent delivery receipt",
          archive_size == delivery["bytes"] and archive_sha == delivery["sha256"] and
          ARCHIVE.name == delivery["filename"] and delivery["id"] == "RANK9-ILLUSIONREALITY5-RETURN207-DELIVERY")
    check("delivery receipt is not applied and lists exactly four acceptances plus one hold",
          delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == HELD and
          delivery["applied"] is False and delivery["appliedIds"] == [] and
          delivery["baselineAuthority"] == AUTHORITY)
    check("delivery per-identity outcomes match the named set",
          {r["id"] for r in delivery["perIdentity"]} == set(GROUP_IDS) and
          all(r["accepted"] is True and r["applied"] is False for r in delivery["perIdentity"]
              if r["id"] in ACCEPTED) and
          all(r["accepted"] is False and r["applied"] is False and r["blockerIds"] == ["IR207-B02"]
              for r in delivery["perIdentity"] if r["id"] in HELD))

    with zipfile.ZipFile(ARCHIVE, "r") as outer:
        names = [info.filename for info in outer.infolist()]
        declared = {row["path"]: row for row in delivery["members"]}
        safe_paths = all(
            name and not name.startswith(("/", "\\")) and "\\" not in name
            and ".." not in PurePosixPath(name).parts for name in names
        )
        check("ZIP members are unique, safe and equal the 102-member delivery allowlist",
              len(names) == len(set(names)) == delivery["memberCount"] == 102 and
              set(names) == set(declared) and safe_paths)
        check("outer archive CRC test passes", outer.testzip() is None)
        for name in names:
            size, digest, crc = member_digest(outer, name)
            row = declared[name]
            check(f"outer member exact byte/SHA/CRC binding: {name}",
                  size == row["bytes"] and digest == row["sha256"] and crc == row["crc32"])

        manifest = member_json(outer, "MEMBER_MANIFEST.json")
        manifest_rows = {row["path"]: row for row in manifest["members"]}
        delivery_without_self = {p: r for p, r in declared.items() if p != "MEMBER_MANIFEST.json"}
        check("embedded allowlist binds all non-self members and delivery binds manifest self-member",
              manifest["memberCountIncludingThisManifest"] == 102 and
              manifest["listedPayloadCount"] == 101 and
              manifest_rows == delivery_without_self and
              manifest["selfBinding"].startswith("This exact member is SHA-256/size/CRC-bound"))

        decision = member_json(outer, "DIRECTOR_DECISION.json")
        procedures_envelope = member_json(outer, "PROCEDURES.json")["procedures"]
        semantics = member_json(outer, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        data_check = member_json(outer, "DATA_INTEGRITY_CHECK.json")
        consistency = member_json(outer, "INTERNAL_CONSISTENCY_CHECK.json")
        case_index_doc = member_json(outer, "CASE_INDEX.json")["cases"]
        case_dispositions = member_json(outer, "CASE_DISPOSITIONS.json")["dispositions"]
        counts = member_json(outer, "COUNTS.json")
        check("director decision matches authority and exact acceptance scope",
              decision["id"] == "RANK9-ILLUSIONREALITY5-DIRECTOR-RETURN207" and
              decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == HELD and
              decision["applied"] is False and decision["appliedIds"] == [] and
              decision["baselineAuthority"] == AUTHORITY and decision["canonicalFilesEdited"] is False)
        check("all delivery package checks and 139 consistency checks pass",
              delivery["packageStatus"] == "PASS" and delivery["packageChecks"] == 310 and
              len(delivery["packageCheckResults"]) == 310 and
              all(row["pass"] is True for row in delivery["packageCheckResults"]) and
              consistency["status"] == "PASS" and consistency["checkCount"] == 139 and
              all(row["pass"] is True for row in consistency["checks"]))
        check("all 504 declared source-preservation checks pass",
              member_json(outer, "SOURCE_VERIFICATION.json")["status"] == "PASS" and
              member_json(outer, "SOURCE_VERIFICATION.json")["checkCount"] == 504 and
              all(row["pass"] is True for row in member_json(outer, "SOURCE_VERIFICATION.json")["checks"]))
        check("semantic gate passes only four identities and keeps Soul Reflection held",
              semantics["status"] == "PARTIAL_PASS_WITH_ONE_NAMED_COVERAGE_BLOCKER" and
              semantics["acceptedIdsIfIntegrityPasses"] == ACCEPTED and semantics["heldIds"] == HELD and
              semantics["mechanicalFailureCount"] == 0 and semantics["checkCount"] == 195 and
              len(semantics["checks"]) == 195 and all(row["pass"] is True for row in semantics["checks"]) and
              [row["id"] for row in semantics["blockingFindings"]] == ["IR207-B02"])
        blocker = semantics["blockingFindings"][0]
        check("IR207-B02 is confined to unsupported Soul Reflection lifecycle branches",
              blocker["spellIds"] == HELD and blocker["questionIds"] ==
              ["RIR5-Q26", "RIR5-Q28", "RIR5-Q29", "RIR5-Q30", "ILLUSION129-ADD02"] and
              all(token in blocker["finding"] for token in ("changed-form reversion", "target0/death", "cargo")))
        check("director makes no runtime or downstream approval claim",
              decision["sourceProgramsExecuted"] is False and
              decision["qualifications"] == delivery["qualifications"] and
              any("No game execution or runtime behavior verified" in row
                  for row in decision["qualifications"]) and
              any("No human playtest completed or approved" in row
                  for row in decision["qualifications"]))
        check("director and sidecar counts agree", counts == delivery["counts"] == decision["counts"])

        case_by_id = {row["id"]: row for row in case_index_doc}
        check("case index covers 10 required main cases plus 46 branches and the declared 56 cases",
              len(case_index_doc) == len(case_by_id) == 56 and
              sum(row["kind"] == "main" for row in case_index_doc) == 10 and
              sum(row["kind"] == "branch" for row in case_index_doc) == 46 and
              sum(row["events"] for row in case_index_doc) == 2005)
        case_disp_by_id = {row["id"]: row for row in case_dispositions}
        check("case dispositions cover precisely the indexed cases and keep them static-only",
              set(case_disp_by_id) == set(case_by_id) and
              all(row["dataReplay"] == "PASS" and row["blockerIds"] == [] for row in case_dispositions
                  if row["spellId"] in ACCEPTED))
        events_seen = fwd_seen = inv_seen = 0
        case_hashes_ok = True
        trace_chains_ok = True
        for row in case_index_doc:
            case_id = row["id"]
            member = row["file"]
            raw = outer.read(member)
            case = json.loads(raw.decode("utf-8"))
            exact = (
                len(raw) == row["bytes"] and sha(raw) == row["sha256"] and
                case["id"] == case_id and case["spellId"] == row["spellId"] and
                case["kind"] == row["kind"] and case["mainCaseId"] == row["mainCaseId"] and
                case["finalSHA256"] == row["finalSHA256"] and len(case["events"]) == row["events"]
            )
            case_hashes_ok &= exact
            trace_ok, fwd, inv, _why = verify_trace(case, row["events"])
            trace_chains_ok &= trace_ok
            events_seen += len(case["events"])
            fwd_seen += fwd
            inv_seen += inv
            actor_binding_ok = case["actorProfileBinding"] == {
                "file": "ACTOR_PROFILES.json",
                "sha256": declared["ACTOR_PROFILES.json"]["sha256"],
            }
            check(f"case and actor-profile bindings: {case_id}", exact and actor_binding_ok)
        check("all 2,005 combat events independently replay as reversible full-state snapshots",
              case_hashes_ok and trace_chains_ok and events_seen == 2005 and
              fwd_seen == inv_seen == 4010 and data_check["combatEvents"] == events_seen and
              data_check["status"] == "PASS" and data_check["failures"] == [])

        spell_records = {row["id"]: row for row in procedures_envelope}
        decision_rows = {row["id"]: row for row in decision["perIdentity"]}
        check("five procedure mirrors are exact, with four accepted and one held",
              set(spell_records) == set(GROUP_IDS) and
              all(spell_records[sid]["accepted"] is True and spell_records[sid]["applied"] is False
                  for sid in ACCEPTED) and
              spell_records[HELD[0]]["accepted"] is False and spell_records[HELD[0]]["applied"] is False)
        accepted_case_ids: dict[str, list[str]] = {}
        for sid in GROUP_IDS:
            embedded = spell_records[sid]
            procedure_name = f"procedures/{sid}.json"
            procedure = member_json(outer, procedure_name)
            accepted = sid in ACCEPTED
            row = decision_rows[sid]
            cases_for_spell = [r["id"] for r in case_index_doc if r["spellId"] == sid]
            accepted_case_ids[sid] = cases_for_spell
            check(f"procedure mirror, director row and exact per-identity source bind: {sid}",
                  embedded == procedure and row["accepted"] is accepted and row["applied"] is False and
                  set(embedded["caseIds"]) == set(cases_for_spell) and
                  declared[procedure_name]["sha256"] == delivery["perIdentity"][GROUP_IDS.index(sid)]["procedureSHA256"])
        check("accepted procedure case coverage is 46; held Soul Reflection cases are excluded from application",
              sum(len(accepted_case_ids[sid]) for sid in ACCEPTED) == 46 and
              len(accepted_case_ids[HELD[0]]) == 10 and
              set().union(*(set(accepted_case_ids[sid]) for sid in ACCEPTED)) ==
              {r["id"] for r in case_index_doc if r["spellId"] in ACCEPTED})

        proposal = member_json(outer, "PROPOSAL_OPERATIONS.json")["operations"]
        proposal_ok = True
        for op in proposal:
            before, after = op["before"], op["after"]
            proposal_ok &= (
                canonical_sha(before) == op["beforeSHA256"] and canonical_sha(after) == op["afterSHA256"]
                and len(op["forward"]) == len(op["inverse"]) == 2
                and op["forward"] == [{"op": "test", "path": "", "value": before},
                                      {"op": "replace", "path": "", "value": after}]
                and op["inverse"] == [{"op": "test", "path": "", "value": after},
                                      {"op": "replace", "path": "", "value": before}]
                and after["proposal"]["applied"] is False
                and after["proposal"]["currentIndexEntryUnchanged"]["authoredStatus"] == "pending-authored-procedure"
            )
        check("five proposal envelopes have exact reversible data-only operations", len(proposal) == 5 and proposal_ok)

        acquisition = member_json(outer, "NULL_ACQUISITION_EVIDENCE.json")
        acq_ok, acq_fwd, acq_inv, _why = verify_trace(acquisition, 2)
        check("two-event Null-acquisition evidence independently replays with exact source binding",
              acq_ok and acq_fwd == acq_inv == 4 and
              acquisition["sourceBinding"]["path"] in {r["path"] for r in
                  json.loads(zipfile.ZipFile(__import__("io").BytesIO(
                      outer.read("source_packet/DD_Rank9_IllusionReality5_CurrentSource_206.zip"))
                  ).read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_206.json"))["sourceBindings"]})

        # Verify the nested, fresh source packet and its 157 Git-bound files.
        import io
        source_packet_raw = outer.read("source_packet/DD_Rank9_IllusionReality5_CurrentSource_206.zip")
        source_delivery_raw = outer.read("source_packet/DD_Rank9_IllusionReality5_CurrentSource_206_DELIVERY.json")
        source_delivery = json.loads(source_delivery_raw.decode("utf-8"))
        source_packet = zipfile.ZipFile(io.BytesIO(source_packet_raw))
        candidate = member_json(source_packet, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_206.json")
        source_verification = member_json(outer, "SOURCE_VERIFICATION.json")
        source_commit = source_verification["sourceCommit"]
        packet_commit = source_verification["packetCommit"]
        bindings = candidate["sourceBindings"]
        source_names = {n[len("sources_current/"):] for n in source_packet.namelist()
                        if n.startswith("sources_current/")}
        check("nested Return206 source packet matches exact prior archive and delivery bindings",
              source_delivery["archive"]["bytes"] == len(source_packet_raw) and
              source_delivery["archive"]["sha256"] == sha(source_packet_raw) and
              source_delivery["sourceCommit"] == source_commit == "0136ce2b33b57278a3d7aa4e58c07b68fcc45bfe" and
              source_delivery["sourceBranch"] == BRANCH and
              source_delivery["sourceAuthority"] == AUTHORITY and
              source_delivery["accepted"] is False and source_delivery["applied"] is False)
        check("157 refreshed source bindings cover all nested current-source files exactly",
              len(bindings) == 157 and {r["path"] for r in bindings} == source_names and
              candidate["currentSourceCommit"] == source_commit and candidate["currentBranch"] == BRANCH and
              candidate["currentAuthority"] == AUTHORITY and
              candidate["currentPendingGroup"]["spellIds"] == GROUP_IDS)
        source_rows_ok = True
        for row in bindings:
            raw = source_packet.read("sources_current/" + row["path"])
            source_rows_ok &= len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        tree = git_tree(source_commit, [r["path"] for r in bindings])
        source_rows_ok &= len(tree) == len(bindings)
        source_oids = [tree.get(r["path"], "") for r in bindings]
        if all(source_oids):
            source_blobs = git_blobs(source_oids)
            for row, oid, raw in zip(bindings, source_oids, source_blobs):
                source_rows_ok &= (
                    oid == row["gitBlobSHA1"] and len(raw) == row["bytes"] and sha(raw) == row["sha256"]
                )
        else:
            source_rows_ok = False
        check("all 157 refreshed source files match source commit Git blobs byte-for-byte", source_rows_ok)

        supplemental = member_json(outer, "evidence/SUPPLEMENTAL_BINDINGS.json")
        supplemental_ok = True
        supplemental_paths = []
        for row in supplemental:
            raw = outer.read("evidence/supplemental_current/" + row["path"])
            supplemental_ok &= len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            supplemental_paths.append(row["path"])
        supplemental_tree = git_tree(source_commit, supplemental_paths)
        supplemental_oids = [supplemental_tree.get(path, "") for path in supplemental_paths]
        if all(supplemental_oids):
            supplemental_blobs = git_blobs(supplemental_oids)
            for row, oid, raw in zip(supplemental, supplemental_oids, supplemental_blobs):
                supplemental_ok &= oid == row["gitBlobSHA1"] and len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        else:
            supplemental_ok = False
        check("seven supplemental source documents match their exact source commit blobs", len(supplemental) == 7 and supplemental_ok)

        next_handoff = member_json(outer, "NEXT_HANDOFF.json")
        next_group = next_handoff["nextQueueGroupUnchanged"]
        check("next fresh queue group is exactly Elemental Convergence/Fusion", next_group["group"] == "rank9-elemental-pets2" and
              next_group["pendingIds"] == ["elemental-convergence", "elemental-fusion"] and
              next_group["pendingCount"] == 2 and next_group["freshPacketRequiredForCurrentAuthority"] is True)

    # Reconcile the review against the exact pushed Return206 baseline.
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    remote_rows = subprocess.check_output(["git", "ls-remote", "origin", f"refs/heads/{BRANCH}"],
                                          cwd=ROOT, text=True).split()
    remote = remote_rows[0] if remote_rows else None
    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    index_raw = index_path.read_bytes()
    index = json.loads(index_raw.decode("utf-8-sig"))
    pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    pending_audit_path = HERE / "CURRENT50_PENDING_IDENTITY_AUDIT_206.json"
    pending_audit = json.loads(pending_audit_path.read_text(encoding="utf-8-sig"))
    check("current branch, pushed Return206 head and 798/50 index authority match",
          head == remote == "85cec3cfaca3f3e6df852ac3ff706f06872bb967" and branch == BRANCH and
          index["authoredCounts"] == {"reviewed": 798, "pending": 50} and
          index["representationCounts"]["completeReviewedStandaloneProcedures"] == 522 and
          pending_audit["currentAuthority"] == AUTHORITY and pending_audit["pendingCount"] == 50 and
          pending == set(pending_audit["pendingIds"]) and set(GROUP_IDS) <= pending and
          sha(index_raw) == candidate["sourceBindings"][1]["sha256"])

    failed = [row for row in checks if not row["passed"]]
    report = {
        "id": "RANK9-ILLUSIONREALITY5-RETURN207-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "FAIL",
        "sourceCommit": source_commit,
        "submissionCommit": packet_commit,
        "branch": BRANCH,
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size, "sha256": archive_sha},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_raw), "sha256": sha(delivery_raw)},
        "authorityAtReview": AUTHORITY,
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "blocker": {"id": "IR207-B02", "spellId": HELD[0], "finding": blocker["finding"]},
        "counts": counts,
        "archiveMembersChecked": delivery["memberCount"],
        "caseFilesChecked": len(case_index_doc),
        "combatEventsReplayed": events_seen,
        "sourceBindingsChecked": len(bindings),
        "supplementalBindingsChecked": len(supplemental),
        "checksPassed": len(checks) - len(failed),
        "checksFailed": len(failed),
        "checks": checks,
        "decision": "Independent archive, source-commit, procedure and reversible-trace checks passed. Apply only the four exact accepted static procedures. Keep Soul Reflection pending under IR207-B02; runtime and downstream approvals remain disabled.",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "members": delivery["memberCount"],
                      "combatEventsReplayed": events_seen, "sourceBindings": len(bindings),
                      "archiveSha256": archive_sha, "report": OUT.relative_to(ROOT).as_posix()}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
