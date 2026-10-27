from __future__ import annotations

import hashlib
import io
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RECEIVED = HERE / "rank9_impactexile4_return205_received"
ARCHIVE = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return205.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return205_DELIVERY.json"
OUT = HERE / "RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json"
EXPECTED_ZIP_SHA = "9914504bde2c4ac555a38400797aee7739a91b4e4780f95bdd86416a66f4403d"
SOURCE_COMMIT = "3bce65038b561b10aa572d7bb42c99bc98e770dc"
SUBMISSION_COMMIT = "2de1e419799c5dc2b5e5c423f5abe130605f3c4c"
BRANCH = "codex/ordinary-spell-review-complete"
GROUP_IDS = ["eternal-anvil", "reverse-gravity-field", "transmute-flesh-to-energy", "planar-collapse"]
ACCEPTED = ["eternal-anvil", "transmute-flesh-to-energy", "planar-collapse"]
HELD = ["reverse-gravity-field"]
BLOCKER = "IE204-B02"
checks: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "passed": bool(ok), **({"detail": detail} if detail else {})})


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_member(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
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


def canonical_state_sha(state: dict) -> str:
    raw = json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha(raw)


def git_tree(commit: str, paths: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for start in range(0, len(paths), 35):
        batch = paths[start:start + 35]
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


def main() -> None:
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8"))
    archive_bytes = ARCHIVE.stat().st_size
    archive_sha = file_sha(ARCHIVE)
    delivery_sha = file_sha(DELIVERY)
    check("outer ZIP size and SHA-256 match delivery and announced digest",
          archive_bytes == delivery["bytes"] and archive_sha == delivery["sha256"] == EXPECTED_ZIP_SHA)
    check("delivery identifies exact three accepted-unapplied IDs and one held identity",
          delivery["accepted"] is True and delivery["applied"] is False and
          delivery["acceptedIds"] == ACCEPTED and delivery["heldIds"] == HELD and
          delivery["blockingIds"] == [BLOCKER] and delivery["canonicalFilesChanged"] is False)
    authority = {"reviewedApplied": 795, "pending": 53, "acceptedUnapplied": 0,
                 "completeStandaloneProcedures": 519, "scopedInterfaces": 173}
    check("review authority is the unchanged 795/53/0 baseline", delivery["authorityAtReview"] == authority)
    check("review scope contains three passing procedures and one current identity blocker",
          delivery["counts"]["acceptedIds"] == delivery["counts"]["completePassingProcedures"] == 3 and
          delivery["counts"]["currentIdentityBlockers"] == 1 and
          delivery["counts"]["mainCases"] == delivery["counts"]["requiredMainCases"] == 8 and
          delivery["counts"]["branches"] == 35 and delivery["counts"]["cases"] == 43 and
          delivery["counts"]["events"] == 1670 and delivery["counts"]["forwardOperations"] == 3340 and
          delivery["counts"]["inverseOperations"] == 3340 and delivery["counts"]["eventOperations"] == 6680)
    check("director package did not claim downstream approvals or program execution",
          all(value is False for key, value in delivery["qualifications"].items() if key != "scope"))

    with zipfile.ZipFile(ARCHIVE, "r") as outer:
        infos = outer.infolist()
        names = [item.filename for item in infos]
        declared = {item["path"]: item for item in delivery["members"]}
        check("archive entries are unique and match the 98-member delivery allowlist",
              len(names) == len(set(names)) == delivery["archiveMemberCount"] and set(names) == set(declared))
        check("archive member paths contain no traversal",
              all(not name.startswith(("/", "\\")) and ".." not in Path(name).parts for name in names))
        check("outer ZIP CRC test passes", outer.testzip() is None)
        for name in names:
            size, digest, crc = digest_member(outer, name)
            expected = declared[name]
            check(f"member size/SHA/CRC: {name}",
                  size == expected["bytes"] and digest == expected["sha256"] and crc == expected["crc32"])

        embedded = member_json(outer, "MANIFEST.json")
        embedded_rows = {row["path"]: row for row in embedded["members"]}
        check("embedded manifest matches delivery member records",
              embedded["memberCountExcludingSelf"] == len(names) - 1 and
              set(embedded_rows) == set(declared) - {"MANIFEST.json"} and
              all(embedded_rows[name] == declared[name] for name in embedded_rows))

        decision = member_json(outer, "DIRECTOR_DECISION.json")
        procedures = member_json(outer, "PROCEDURES.json")
        validation = member_json(outer, "VALIDATION.json")
        semantics = member_json(outer, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        data_check = member_json(outer, "DATA_INTEGRITY_CHECK.json")
        case_index = member_json(outer, "CASE_INDEX.json")
        outstanding = member_json(outer, "OUTSTANDING_CASE_OBLIGATIONS.json")
        resolved = member_json(outer, "RESOLVED_PREVIOUS_BLOCKERS.json")
        source_verification = member_json(outer, "SOURCE_VERIFICATION_205.json")
        source_delivery = member_json(outer, "SOURCE_DELIVERY_203.json")
        source_proof = member_json(outer, "source_proofs/GIT_SOURCE_PROOF.json")
        supplemental_proof = member_json(outer, "source_proofs/SUPPLEMENTAL_GIT_PROOF.json")

        check("director decision accepts only the same three IDs, leaves them unapplied, and retains one hold",
              decision["id"] == "RANK9-IMPACTEXILE4-DIRECTOR-RETURN205" and
              decision["accepted"] is True and decision["applied"] is False and
              decision["acceptedIds"] == ACCEPTED and decision["heldIds"] == HELD and
              decision["authorityAtReview"] == authority and
              {row["id"] for row in decision["perIdentity"]} == set(GROUP_IDS) and
              all(row["applied"] is False for row in decision["perIdentity"]))
        rows = {row["id"]: row for row in decision["perIdentity"]}
        check("each accepted identity is individually accepted and Reverse Gravity Field is not",
              all(rows[sid]["accepted"] is True for sid in ACCEPTED) and
              rows["reverse-gravity-field"]["accepted"] is False)
        check("only IE204-B02 remains unresolved for the held identity",
              [item["id"] for item in decision["currentBlockers"]] == [BLOCKER] and
              decision["currentBlockers"][0]["spellIds"] == HELD and
              outstanding["heldIds"] == HELD and
              [item["id"] for item in outstanding["blockers"]] == [BLOCKER])
        check("three prior blockers are resolved and none is represented as a new global rule",
              {item["originalBlockerUnchanged"]["id"] for item in resolved} ==
              {"IE204-B01", "IE204-B03", "IE204-B04"} and
              all(item["resolvedInReturn"] == 205 for item in resolved))
        check("semantic gate passes exactly the three director-accepted identities",
              semantics["status"] == "PARTIAL_PASS" and
              semantics["acceptedEligibleIds"] == ACCEPTED and semantics["heldIds"] == HELD and
              len(semantics["checks"]) == 20 and
              sum(row["pass"] is True for row in semantics["checks"]) == 19 and
              [row["spellId"] for row in semantics["checks"] if row["pass"] is False] == HELD)
        check("data-integrity results cover all 43 cases and report no failures",
              data_check["status"] == "PASS" and data_check["checkCount"] == 37417 and
              data_check["failed"] == 0 and len(data_check["caseResults"]) == 43 and
              all(row["passed"] is True for row in data_check["caseResults"]))
        check("validation agrees with independent acceptance and leaves runtime disabled",
              validation["acceptedIds"] == ACCEPTED and validation["heldIds"] == HELD and
              validation["applied"] is False and validation["dataStatus"] == "PASS" and
              validation["semanticStatus"] == "PARTIAL_PASS" and
              validation["sourceStatus"] == "PASS" and validation["runtimeTestsExecuted"] is False and
              validation["sourceOrHistoricalProgramsExecuted"] is False)
        check("case index exactly covers 8 main cases plus 35 branches and 1,670 events",
              len(case_index) == 43 and sum(row["events"] for row in case_index) == 1670 and
              sum(row["kind"] == "main" for row in case_index) == 8 and
              sum(row["kind"] == "branch" for row in case_index) == 35)

        case_by_id = {row["id"]: row for row in case_index}
        case_ids_seen: set[str] = set()
        events_seen = forward_seen = inverse_seen = 0
        for case_row in case_index:
            case_id = case_row["id"]
            member = "cases/" + case_id.replace("/", "__") + ".json"
            case_doc = member_json(outer, member)
            case_ids_seen.add(case_id)
            events_seen += len(case_doc["events"])
            check(f"case identity, scope and event count: {case_id}",
                  case_doc["id"] == case_id and case_doc["spellId"] == case_row["spellId"] and
                  case_doc["kind"] == case_row["kind"] and len(case_doc["events"]) == case_row["events"])
            current = case_doc["initialState"]
            check(f"initial state hash: {case_id}",
                  canonical_state_sha(current) == case_doc["events"][0]["beforeSHA256"])
            for position, event in enumerate(case_doc["events"], 1):
                before, after = event["before"], event["after"]
                before_hash, after_hash = canonical_state_sha(before), canonical_state_sha(after)
                forward = event["forward"]
                inverse = event["inverse"]
                ok = (before == current and before_hash == event["beforeSHA256"] and
                      after_hash == event["afterSHA256"] and len(forward) == len(inverse) == 2 and
                      forward[0] == {"op": "test", "path": "", "value": before} and
                      forward[1] == {"op": "replace", "path": "", "value": after} and
                      inverse[0] == {"op": "test", "path": "", "value": after} and
                      inverse[1] == {"op": "replace", "path": "", "value": before})
                check(f"forward/inverse operation and snapshot chain: {case_id}:{position}", ok)
                current = after
            check(f"final state hash and last snapshot: {case_id}",
                  current == case_doc["finalState"] and
                  canonical_state_sha(current) == case_doc["expectedFinalSHA256"] and
                  case_doc["expectedFinalSHA256"] == data_check["caseResults"][
                      next(i for i, row in enumerate(data_check["caseResults"]) if row["id"] == case_id)
                  ]["finalSHA256"])
            forward_seen += sum(len(event["forward"]) for event in case_doc["events"])
            inverse_seen += sum(len(event["inverse"]) for event in case_doc["events"])
        check("all 1,670 event snapshots and exact forward/inverse operations independently reconcile",
              events_seen == 1670 and forward_seen == inverse_seen == 3340 and
              len(case_ids_seen) == 43 and case_ids_seen == set(case_by_id))

        spell_records = {row["id"]: row for row in procedures["spells"]}
        check("procedure envelope contains exactly the three accepted identities, unapplied",
              procedures["acceptedIds"] == ACCEPTED and procedures["heldIds"] == HELD and
              procedures["applied"] is False and set(spell_records) == set(ACCEPTED))
        for sid in ACCEPTED:
            record = spell_records[sid]
            check(f"complete accepted procedure and source/access record: {sid}",
                  record["accepted"] is True and record["applied"] is False and
                  bool(record["procedure"]) and bool(record["rules"]) and
                  record["completeSourceAndAccess"]["id"] == sid and
                  record["completeSourceAndAccess"]["status"] == "blocked-pending-operational-review" and
                  all(value is False for key, value in record["qualifications"].items() if key != "scope"))
            listed = set(record["caseIds"])
            indexed = {row["id"] for row in case_index if row["spellId"] == sid}
            check(f"accepted procedure case references resolve exactly: {sid}", listed == indexed)

        check("source verification summary passes 164 checks at the current pushed review head",
              source_verification["status"] == "PASS" and source_verification["checkCount"] == 164 and
              source_verification["sourceCommit"] == SOURCE_COMMIT and
              source_verification["latestReviewCommit"] == SUBMISSION_COMMIT and
              source_verification["unchanged149SourceBindings"] == 149 and
              all(row["pass"] is True for row in source_verification["checks"]))
        check("prepared packet 203 identity, source commit, authority and bytes are preserved",
              source_delivery["sourceCommit"] == SOURCE_COMMIT and
              source_delivery["sourceBranch"] == BRANCH and
              source_delivery["sourceAuthority"]["pending"] == 53 and
              source_delivery["archive"]["sha256"] == delivery["sourceArchiveSHA256"] and
              source_delivery["archive"]["bytes"] == outer.getinfo("SOURCE_PACKET_203.zip").file_size and
              sha(outer.read("SOURCE_DELIVERY_203.json")) == delivery["sourceDeliverySHA256"])

        source_packet_bytes = outer.read("SOURCE_PACKET_203.zip")
        with zipfile.ZipFile(io.BytesIO(source_packet_bytes), "r") as packet:
            check("nested source packet CRC test passes", packet.testzip() is None)
            candidate = member_json(packet, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_203.json")
            bindings = candidate["sourceBindings"]
            packet_paths = {name[len("sources_current/"):] for name in packet.namelist()
                            if name.startswith("sources_current/")}
            check("149 current source bindings exactly cover sources_current packet members",
                  len(bindings) == 149 and {row["path"] for row in bindings} == packet_paths and
                  candidate["currentSourceCommit"] == SOURCE_COMMIT and candidate["currentBranch"] == BRANCH and
                  candidate["currentPendingGroup"]["spellIds"] == GROUP_IDS)
            for binding in bindings:
                raw = packet.read("sources_current/" + binding["path"])
                check(f"current source packet binding: {binding['path']}",
                      len(raw) == binding["bytes"] and sha(raw) == binding["sha256"])

        proof_rows = source_proof["verified"]
        check("Git source proof has 177 source-commit paths and no errors",
              source_proof["commit"]["sha"] == SOURCE_COMMIT and len(proof_rows) == 177 and
              source_proof["errors"] == [])
        proof_tree = git_tree(SOURCE_COMMIT, [row["path"] for row in proof_rows])
        check("all source-proof paths resolve in source commit", len(proof_tree) == 177)
        proof_oids = []
        for row in proof_rows:
            oid = proof_tree.get(row["path"])
            check(f"Git tree object matches source proof: {row['path']}",
                  oid == row["gitBlobSHA1"] == row["treeBlob"]["sha"] and
                  row["treeBlob"]["size"] == row["bytes"])
            if oid:
                proof_oids.append(oid)
        proof_blobs = git_blobs(proof_oids)
        for row, raw in zip(proof_rows, proof_blobs):
            check(f"source commit blob bytes match SHA-256 proof: {row['path']}",
                  len(raw) == row["bytes"] and sha(raw) == row["sha256"])

        supplemental = supplemental_proof["blobs"]
        check("nine supplemental source blobs are bound to the reviewed source commit",
              supplemental_proof["commit"] == SOURCE_COMMIT and len(supplemental) == 9)
        for item in supplemental:
            raw = outer.read("supplemental_sources/" + item["path"])
            git_oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            check(f"supplemental source object matches Git proof: {item['path']}",
                  len(raw) == item["size"] and git_oid == item["sha"])

        handoff = member_json(outer, "NEXT_QUEUE_HANDOFF.json")
        next_group = handoff["nextGroup"]
        check("director handoff queues the next five exact pending IDs at a fresh current authority",
              handoff["currentAuthorityUnchanged"] == authority and
              handoff["Return205AcceptedUnappliedIds"] == ACCEPTED and
              next_group["group"] == "rank9-illusion-reality5" and
              next_group["pendingCount"] == 5 and
              next_group["pendingIds"] == ["supreme-illusion", "mirrored-world", "ethereal-disjunction",
                                           "illusory-reality", "soul-reflection"] and
              next_group["freshPacketRequiredForCurrentAuthority"] is True)

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          text=True, capture_output=True).stdout.strip()
    remote = subprocess.run(["git", "ls-remote", "origin", f"refs/heads/{BRANCH}"],
                            cwd=ROOT, check=True, text=True, capture_output=True).stdout.split()
    remote_head = remote[0] if remote else None
    check("review source packet was prepared from the exact pushed current branch head",
          head == SUBMISSION_COMMIT and remote_head == SUBMISSION_COMMIT,
          f"local={head}; remote={remote_head}")

    failed = [item for item in checks if not item["passed"]]
    report = {
        "id": "RANK9-IMPACTEXILE4-RETURN205-INDEPENDENT-AUDIT",
        "status": "PASS" if not failed else "FAIL",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": SOURCE_COMMIT,
        "submissionCommit": SUBMISSION_COMMIT,
        "branch": BRANCH,
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_bytes, "sha256": archive_sha},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size,
                     "sha256": delivery_sha},
        "authorityAtReview": authority,
        "acceptedIds": ACCEPTED,
        "heldIds": HELD,
        "blocker": {"id": BLOCKER, "spellId": HELD[0],
                    "missing": "sourced crate impact/breakage and rated tether/anchor evidence"},
        "counts": delivery["counts"],
        "outerMembersChecked": len(delivery["members"]),
        "caseFilesChecked": len(case_index),
        "caseEventsChecked": events_seen,
        "sourceProofPathsChecked": len(proof_rows),
        "sourceBindingsChecked": len(bindings),
        "supplementalBindingsChecked": len(supplemental),
        "checksPassed": len(checks) - len(failed),
        "checksFailed": len(failed),
        "checks": checks,
        "decision": "Independent package, source and reversible-case integrity passed. Apply only the three exact accepted static authored procedures. Keep Reverse Gravity Field pending under IE204-B02; runtime and downstream approvals remain disabled.",
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "outerMembers": len(delivery["members"]),
                      "caseEvents": events_seen, "sourceProofPaths": len(proof_rows),
                      "archiveSha256": archive_sha, "remoteHead": remote_head,
                      "audit": OUT.relative_to(ROOT).as_posix()}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
