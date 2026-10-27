from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path

import orjson

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_knowledgerevelation5_return198_received"
ARCHIVE = RECEIVED / "DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
DELIVERY = RECEIVED / "DD_Rank9_KnowledgeRevelation5_Director_Return198_DELIVERY.json"
SOURCE_PACKET = AUDIT / "rank9_knowledgerevelation5_current_source_197_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_197.zip"
SOURCE_DELIVERY = AUDIT / "rank9_knowledgerevelation5_current_source_197_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_197_DELIVERY.json"
SOURCE_COMMIT = "1880dc5cea9faf3aa764300162751973c2bee7dd"
REPORT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN198_INDEPENDENT_AUDIT.json"
ACCEPTED = ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"]
HELD = ["faction-omniscience-supreme"]
GROUP = ACCEPTED + HELD
BASELINE = {
    "reviewedApplied": 786,
    "pending": 62,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 510,
    "scopedInterfaces": 173,
}
EXPECTED_COUNTS = {
    "procedures": 5,
    "acceptedProcedures": 4,
    "unacceptedProcedures": 1,
    "originalQuestions": 26,
    "focusedAddenda": 2,
    "answeredDispositions": 28,
    "requiredMainCases": 10,
    "mainCases": 10,
    "branches": 67,
    "cases": 77,
    "passingStaticCases": 69,
    "heldCases": 8,
    "events": 1693,
    "forwardEventOperations": 3386,
    "inverseEventOperations": 3386,
    "eventOperations": 6772,
    "proposalOperations": 20,
    "futureObligations": 9,
    "refreshedSourceBindings": 126,
    "additionalCurrentSourceBindings": 10,
    "boundInputArchiveMembers": 157,
    "newHoldRecords": 7,
    "inheritedHoldRecords": 141,
    "totalHoldRecords": 148,
    "distinctHoldIds": 148,
    "newAcceptanceBlockers": 1,
    "carriedNamedBlockerIds": 10,
    "sourceVerificationChecks": 1142,
    "profileSourceChecks": 270,
    "supplementalSourceChecks": 20,
    "dataIntegrityChecks": 74752,
    "semanticChecks": 47,
    "finalBindingChecks": 96,
    "stateHashFields": 3540,
    "totalPrePackagingChecks": 76327,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_state_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha(raw)


def check(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{SOURCE_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def stream_sha(member) -> tuple[int, str, int]:
    h = hashlib.sha256()
    crc = 0
    size = 0
    for chunk in iter(lambda: member.read(1024 * 1024), b""):
        size += len(chunk)
        h.update(chunk)
        crc = zlib.crc32(chunk, crc)
    return size, h.hexdigest(), crc & 0xFFFFFFFF


def iter_case_objects(stream):
    """Stream one case at a time from the large compact CASEBOOK JSON array."""
    chunk_size = 1024 * 1024
    marker = b'"cases":['
    chunk = stream.read(chunk_size)
    marker_at = chunk.find(marker)
    if marker_at < 0:
        raise ValueError("CASEBOOK cases array marker not found in first chunk")
    data_chunks = [chunk[marker_at + len(marker):]]
    current = bytearray()
    depth = 0
    in_string = False
    escaped = False
    started = False
    while True:
        if data_chunks:
            data = data_chunks.pop(0)
        else:
            data = stream.read(chunk_size)
            if not data:
                if started or depth:
                    raise ValueError("CASEBOOK ended inside a case object")
                return
        for byte in data:
            if not started:
                if byte in b" \r\n\t,":
                    continue
                if byte == ord("]"):
                    return
                if byte != ord("{"):
                    raise ValueError(f"Expected a case object, got byte {byte}")
                started = True
                depth = 1
                in_string = False
                escaped = False
                current.clear()
                current.append(byte)
                continue
            current.append(byte)
            if in_string:
                if escaped:
                    escaped = False
                elif byte == ord("\\"):
                    escaped = True
                elif byte == ord('"'):
                    in_string = False
                continue
            if byte == ord('"'):
                in_string = True
            elif byte in (ord("{"), ord("[")):
                depth += 1
            elif byte in (ord("}"), ord("]")):
                depth -= 1
                if depth == 0:
                    yield orjson.loads(current)
                    current.clear()
                    started = False


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    source_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))

    archive_bytes = ARCHIVE.stat().st_size
    archive_sha = file_sha(ARCHIVE)
    delivery_sha = file_sha(DELIVERY)
    check(checks, "Return ZIP matches delivery bytes and SHA-256",
          archive_bytes == delivery["archive"]["bytes"] == 113662026
          and archive_sha == delivery["archive"]["sha256"] == "2da202eaab4542d7b3bef90e03e75b5276f8396b8a8e3e535a1245d20d87afca",
          {"bytes": archive_bytes, "sha256": archive_sha})
    check(checks, "Delivery preserves exact source packet and baseline authority",
          delivery["sourcePacketSHA256"] == source_delivery["archive"]["sha256"] == file_sha(SOURCE_PACKET)
          and delivery["sourceDeliverySHA256"] == file_sha(SOURCE_DELIVERY)
          and delivery["authorityBaselineUnchanged"] == BASELINE,
          {"sourcePacketSHA256": delivery["sourcePacketSHA256"], "sourceDeliverySHA256": delivery["sourceDeliverySHA256"],
           "authorityBaselineUnchanged": delivery["authorityBaselineUnchanged"]})
    check(checks, "Director and delivery show exact four acceptances, one hold, and no application",
          delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == HELD
          and delivery["applied"] is False and delivery["canonicalFilesChanged"] is False
          and delivery["counts"] == EXPECTED_COUNTS,
          {"acceptedIds": delivery["acceptedIds"], "unacceptedIds": delivery["unacceptedIds"],
           "counts": delivery["counts"]})

    with zipfile.ZipFile(ARCHIVE) as z:
        infos = {info.filename: info for info in z.infolist()}
        names = list(infos)
        outer_rows = {row["path"]: row for row in delivery["allOuterMembersIncludingManifest"]}
        check(checks, "ZIP has 128 unique safe members and exact outer allowlist",
              len(names) == len(set(names)) == 128 and set(names) == set(outer_rows)
              and all(not n.startswith(("/", "\\")) and ".." not in Path(n).parts for n in names),
              {"members": len(names), "outerManifestMembers": len(outer_rows)})

        member_failures = []
        total_member_bytes = 0
        for name, info in infos.items():
            size, digest, crc = stream_sha(z.open(info, "r"))
            total_member_bytes += size
            row = outer_rows[name]
            if (size != row["bytes"] or digest != row["sha256"]
                    or f"{crc:08x}" != str(row["crc32"]).lower()
                    or info.compress_size != row["compressedBytes"]
                    or info.CRC != crc):
                member_failures.append({"path": name, "size": size, "sha256": digest, "crc32": f"{crc:08x}"})
        check(checks, "All 128 streamed ZIP members match byte, SHA-256, CRC, and compressed-size bindings",
              not member_failures and total_member_bytes == sum(x["bytes"] for x in outer_rows.values()),
              {"checked": len(infos), "uncompressedBytes": total_member_bytes, "failures": member_failures[:10]})
        check(checks, "ZIP central directory and CRC test pass", z.testzip() is None,
              {"centralDirectoryEntries": len(infos)})

        member_manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        internal_rows = {row["path"]: row for row in member_manifest["members"]}
        check(checks, "Internal member manifest lists exactly all members except itself",
              member_manifest["listedMemberCount"] == 127 and member_manifest["totalArchiveMemberCount"] == 128
              and member_manifest["excludesOnlySelf"] == "MEMBER_MANIFEST.json"
              and set(internal_rows) == set(names) - {"MEMBER_MANIFEST.json"}
              and delivery["memberManifest"]["sha256"] == outer_rows["MEMBER_MANIFEST.json"]["sha256"]
              and all(internal_rows[k]["sha256"] == outer_rows[k]["sha256"]
                      and internal_rows[k]["bytes"] == outer_rows[k]["bytes"] for k in internal_rows),
              {"internalListed": len(internal_rows), "archiveMembers": len(names)})

        # Source packet roundtrip is compared directly against the exact local packet of record.
        embedded_packet = z.open("source_packet/DD_Rank9_KnowledgeRevelation5_CurrentSource_197.zip", "r")
        embedded_packet_size, embedded_packet_sha, _ = stream_sha(embedded_packet)
        embedded_delivery = z.read("source_packet/DD_Rank9_KnowledgeRevelation5_CurrentSource_197_DELIVERY.json")
        check(checks, "Return embeds the byte-exact submitted source ZIP and delivery JSON",
              embedded_packet_size == SOURCE_PACKET.stat().st_size == 103797987
              and embedded_packet_sha == file_sha(SOURCE_PACKET)
              and embedded_delivery == SOURCE_DELIVERY.read_bytes(),
              {"embeddedPacketBytes": embedded_packet_size, "embeddedPacketSHA256": embedded_packet_sha,
               "embeddedDeliveryBytes": len(embedded_delivery)})

        remote = json.loads(z.read("REMOTE_SOURCE_BINDINGS.json"))
        source_verification = json.loads(z.read("SOURCE_VERIFICATION.json"))
        check(checks, "Bound source commit, tree traversal, and 1,142 declared checks are complete",
              remote["sourceCommit"] == source_verification["sourceCommit"] == SOURCE_COMMIT
              and remote["publicationCommit"] == "77625c617db8d177a09d27a372173dc910119caf"
              and source_delivery["sourceCommit"] == SOURCE_COMMIT
              and remote["treeCount"] == 41 and len(remote["entries"]) == 148 and not remote["missing"]
              and source_verification["allPass"] is True
              and source_verification["checkCount"] == len(source_verification["checks"]) == 1142
              and all(row.get("passed") is True for row in source_verification["checks"]),
              {"sourceCommit": remote["sourceCommit"], "publicationCommit": remote["publicationCommit"],
               "gitBindings": len(remote["entries"]), "sourceChecks": len(source_verification["checks"])})
        git_failures = []
        for binding in remote["entries"]:
            raw = git_blob(binding["path"])
            blob_sha1 = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if len(raw) != binding["size"] or blob_sha1 != binding["sha"]:
                git_failures.append(binding["path"])
        check(checks, "All 148 refreshed source-tree entries independently match Git blobs",
              not git_failures, {"checked": len(remote["entries"]), "failures": git_failures[:20]})

        extra_bindings = json.loads(z.read("ADDITIONAL_SOURCE_BINDINGS.json"))["bindings"]
        additional_failures = []
        for binding in extra_bindings:
            raw = git_blob(binding["path"])
            blob_sha1 = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            name = "additional_sources/" + binding["path"]
            member_raw = z.read(name)
            if (len(raw) != binding["bytes"] or sha(raw) != binding["sha256"]
                    or blob_sha1 != binding["gitBlobSHA1"] or member_raw != raw
                    or binding["sourceCommit"] != SOURCE_COMMIT):
                additional_failures.append(binding["path"])
        check(checks, "All ten additional current-source copies match exact Git blobs and package members",
              len(extra_bindings) == 10 and not additional_failures,
              {"checked": len(extra_bindings), "failures": additional_failures})

        director = json.loads(z.read("DIRECTOR_DECISION.json"))
        model = json.loads(z.read("MODEL.json"))
        validation = json.loads(z.read("VALIDATION.json"))
        semantic = json.loads(z.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        blockers = {x["id"]: x for x in director["blockers"]}
        decisions = {x["id"]: x for x in director["perIdentity"]}
        model_spells = {x["id"]: x for x in model["spells"]}
        check(checks, "Director, model, validation, and delivery agree on per-identity decisions",
              director["acceptedIds"] == model["acceptedIds"] == validation["semanticPassForAcceptedIds"] == ACCEPTED
              and director["unacceptedIds"] == model["unacceptedIds"] == validation["unacceptedIds"] == HELD
              and director["applied"] is False and model["applied"] is False
              and validation["canonicalApplied"] is False and validation["wholeBatchAccepted"] is False
              and set(decisions) == set(model_spells) == set(GROUP)
              and all(decisions[s]["accepted"] is True and decisions[s]["applied"] is False
                      and not decisions[s].get("blockerIds") and model_spells[s]["accepted"] is True
                      and model_spells[s]["applied"] is False for s in ACCEPTED)
              and decisions[HELD[0]]["accepted"] is False and decisions[HELD[0]]["applied"] is False
              and decisions[HELD[0]]["blockerIds"] == ["KR198-B01"]
              and model_spells[HELD[0]]["accepted"] is False and model_spells[HELD[0]]["applied"] is False,
              {"acceptedIds": director["acceptedIds"], "heldIds": director["unacceptedIds"]})
        blocker = blockers.get("KR198-B01", {})
        check(checks, "KR198-B01 narrowly blocks only faction omniscience for missing canonical history/forecast evidence",
              set(blocker.get("spellIds", [])) == set(HELD) and blocker.get("blocking") is True
              and "complete past/present/distant-branch ledger" in blocker.get("missing", "")
              and "forecast" in blocker.get("missing", "").lower()
              and semantic["wholeBatchPass"] is False and semantic["allImplementedChecksPass"] is True
              and semantic["acceptedIds"] == ACCEPTED and semantic["unacceptedIds"] == HELD
              and semantic["sourceBindingPass"] is True and semantic["dataIntegrityPass"] is True
              and len(semantic["checks"]) == 47 and all(x.get("passed") is True for x in semantic["checks"]),
              {"blocker": blocker, "semanticChecks": len(semantic["checks"]), "wholeBatchPass": semantic["wholeBatchPass"]})

        carried = json.loads(z.read("CARRIED_HOLDS_196.json"))
        carried_named = director["carriedNamedBlockersUnchanged"]
        expected_named = {
            "AG190": ["AG190-B01", "AG190-B02"],
            "TF192": ["TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"],
            "CC194": ["CC194-B01", "CC194-B04"],
            "MD196": ["MD196-B01", "MD196-B02"],
        }
        carried_ids = {blocker_id for rows in carried_named.values() for blocker_id in rows["blockers"]}
        check(checks, "All ten inherited named blockers and prior accepted Memory/Denial context remain unchanged",
              {k: v["blockers"] for k, v in carried_named.items()} == expected_named
              and len(carried_ids) == delivery["counts"]["carriedNamedBlockerIds"] == 10
              and carried["recordCount"] == 141 and carried["inherited194Records"] == 56
              and director["priorAcceptedContextUnchanged"]["acceptedIds"] == [
                  "mass-willbreaker", "mind-prison-mass", "mind-wipe", "unmake-spell"]
              and director["priorAcceptedContextUnchanged"]["unacceptedIds"] == ["mind-collapse", "unravel-identity"],
              {"carriedNamedBlockers": {k: v["blockers"] for k, v in carried_named.items()},
               "recordCount": carried["recordCount"], "inherited194Records": carried["inherited194Records"]})

        counts = json.loads(z.read("COUNTS.json"))
        questions = json.loads(z.read("QUESTION_DISPOSITIONS.json"))
        future = json.loads(z.read("FUTURE_OBLIGATION_DISPOSITIONS.json"))
        dispositions = json.loads(z.read("CASE_DISPOSITIONS.json"))
        check(checks, "Question, future-obligation, case-disposition, and count totals match the required cohort",
              counts == EXPECTED_COUNTS and validation["exactCounts"] == EXPECTED_COUNTS
              and len(questions) == 28 and len(future) == 9 and len(dispositions) == 10
              and all(x.get("originalObligationUnchanged") for x in dispositions),
              {"questions": len(questions), "futureObligations": len(future), "mainDispositions": len(dispositions)})
        check(checks, "Package, saved-artifact, final-binding, and prepackage integrity gates all report pass",
              delivery["packagingIntegrity"]["allPass"] is True
              and all(x.get("passed") is True for x in delivery["packagingIntegrity"]["checks"])
              and delivery["savedArtifactVerification"]["status"] == "EXACT_SAVED_ARTIFACT_ROUNDTRIP_PASS"
              and delivery["savedArtifactVerification"]["verified"] is True
              and delivery["savedArtifactVerification"]["byteEquality"] is True
              and delivery["savedArtifactVerification"]["memberAllowlistAndCRCsAndHashes"] is True
              and delivery["savedArtifactVerification"]["checkCount"] == 390
              and all(x.get("passed") is True for x in delivery["savedArtifactVerification"]["checks"])
              and delivery["postAssemblyDataChecks"]["allPass"] is True
              and delivery["validationChecksBeforeSavedArtifactReadback"] == 77246
              and delivery["validationChecksIncludingSavedZIPReadback"] == 77636,
              {"packagingChecks": delivery["packagingIntegrity"]["checkCount"],
               "savedReadbackChecks": delivery["savedArtifactVerification"]["checkCount"],
               "checksBeforeSavedReadback": delivery["validationChecksBeforeSavedArtifactReadback"],
               "checksIncludingSavedReadback": delivery["validationChecksIncludingSavedZIPReadback"]})

        case_statuses: dict[str, int] = {}
        case_ids: set[str] = set()
        main_ids: set[str] = set()
        events = forward_count = inverse_count = 0
        case_failures = []
        for case in iter_case_objects(z.open("CASEBOOK.json", "r")):
            case_id = case["id"]
            if case_id in case_ids:
                case_failures.append({"case": case_id, "reason": "duplicate id"})
                continue
            case_ids.add(case_id)
            status = case["status"]
            case_statuses[status] = case_statuses.get(status, 0) + 1
            if case["kind"] == "main":
                main_ids.add(case_id)
            if case.get("applied") is not False:
                case_failures.append({"case": case_id, "reason": "applied flag"})
            initial = case["initialState"]
            final = case["finalState"]
            if (canonical_state_sha(initial) != case["initialSHA256"]
                    or canonical_state_sha(final) != case["finalSHA256"]):
                case_failures.append({"case": case_id, "reason": "initial/final state hash"})
                continue
            state = initial
            prior_time = state.get("time")
            for event in case["events"]:
                events += 1
                fops = event["forward"]
                iops = event["inverse"]
                forward_count += len(fops)
                inverse_count += len(iops)
                before = event["beforeState"]
                after = event["afterState"]
                good = (before == state and event["beforeSHA256"] == canonical_state_sha(before)
                        and event["afterSHA256"] == canonical_state_sha(after)
                        and len(fops) == 2 and len(iops) == 2)
                if good:
                    good = (fops[0].get("op") == "test" and fops[0].get("path") == "" and fops[0].get("value") == before
                            and fops[1].get("op") == "replace" and fops[1].get("path") == "" and fops[1].get("value") == after
                            and iops[0].get("op") == "test" and iops[0].get("path") == "" and iops[0].get("value") == after
                            and iops[1].get("op") == "replace" and iops[1].get("path") == "" and iops[1].get("value") == before)
                before_time, after_time = before.get("time"), after.get("time")
                if (isinstance(before_time, (int, float)) and isinstance(after_time, (int, float))
                        and after_time < before_time):
                    good = False
                if (isinstance(prior_time, (int, float)) and isinstance(before_time, (int, float))
                        and before_time < prior_time):
                    good = False
                if not good:
                    case_failures.append({"case": case_id, "event": event.get("id"), "reason": "chain/patch/hash/clock"})
                    break
                state = after
                prior_time = after_time
            if state != final or canonical_state_sha(state) != case["finalSHA256"]:
                case_failures.append({"case": case_id, "reason": "final chain state"})
        expected_pass_status = {k: v for k, v in case_statuses.items() if "PASS" in k or "DEMONSTRATED" in k}
        check(checks, "All 77 case states, 1,693 event chains, reversible patches, hashes, and clocks independently replay",
              len(case_ids) == 77 and len(main_ids) == 10 and events == 1693
              and forward_count == inverse_count == 3386 and not case_failures
              and sum(expected_pass_status.values()) == 69
              and sum(case_statuses.values()) == 77,
              {"cases": len(case_ids), "mainCases": len(main_ids), "events": events,
               "forwardOperations": forward_count, "inverseOperations": inverse_count,
               "statusCounts": case_statuses, "failures": case_failures[:12]})

        next_group = json.loads(z.read("NEXT_QUEUE_GROUP.json"))["nextExactGroupUnchanged"]
        check(checks, "Director names the next exact five-identity group and requires a fresh current-authority packet",
              next_group["group"] == "rank9-planar-gates5"
              and next_group["pendingIds"] == ["gate", "absolute-gate", "banishment-gate", "planar-sanctuary", "conjure-demiplane-fortress"]
              and next_group["pendingCount"] == 5 and next_group["freshPacketRequiredForCurrentAuthority"] is True,
              next_group)

    failed = [row for row in checks if not row["passed"]]
    report = {
        "id": "RANK9-KNOWLEDGEREVELATION5-RETURN198-INDEPENDENT-AUDIT",
        "status": "PASS" if not failed else "FAIL",
        "checksPassed": len(checks) - len(failed),
        "checksFailed": len(failed),
        "checks": checks,
        "sourceCommit": SOURCE_COMMIT,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_bytes, "sha256": archive_sha},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": delivery_sha},
        "acceptedIds": ACCEPTED,
        "unacceptedIds": HELD,
        "applied": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "failures": failed,
                      "report": REPORT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
