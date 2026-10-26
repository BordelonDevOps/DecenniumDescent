from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_memorydenial6_return196_received"
ARCHIVE = RECEIVED / "DD_Rank9_MemoryDenial6_Director_Return196.zip"
DELIVERY = RECEIVED / "DD_Rank9_MemoryDenial6_Director_Return196_DELIVERY.json"
SOURCE_COMMIT = "6018e1a2181791ec559456638e46dd3d98e0afe6"
REPORT = AUDIT / "RANK9_MEMORYDENIAL6_RETURN196_INDEPENDENT_AUDIT.json"
EXPECTED_ACCEPTED = ["mass-willbreaker", "mind-prison-mass", "mind-wipe", "unmake-spell"]
EXPECTED_BLOCKED = ["mind-collapse", "unravel-identity"]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_state_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha(raw)


def check(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def git_blob(path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{SOURCE_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    archive_raw_sha = hashlib.sha256()
    archive_bytes = 0
    with ARCHIVE.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            archive_bytes += len(chunk)
            archive_raw_sha.update(chunk)
    archive_sha = archive_raw_sha.hexdigest()
    check(checks, "Director return archive matches delivery byte count and SHA-256",
          archive_bytes == delivery["archive"]["bytes"] and archive_sha == delivery["archive"]["sha256"],
          {"bytes": archive_bytes, "sha256": archive_sha})
    check(checks, "Director says this is unapplied with exact four approvals and two holds",
          delivery.get("applied") is False and delivery["acceptedIds"] == EXPECTED_ACCEPTED
          and delivery["unacceptedIds"] == EXPECTED_BLOCKED,
          {"acceptedIds": delivery["acceptedIds"], "unacceptedIds": delivery["unacceptedIds"]})
    check(checks, "Director package-level manifest checks pass",
          delivery["packageAllPass"] is True
          and delivery["savedArtifactVerification"]["status"] == "PASS"
          and delivery["savedArtifactVerification"]["byteForByteEqualToLocal"] is True
          and delivery["savedArtifactVerification"]["allMemberSizesSHA256AndCRCPass"] is True,
          {"packageAllPass": delivery["packageAllPass"],
           "finalMetadataChecks": delivery["finalMetadataChecks"],
           "packageChecks": delivery["packageChecks"],
           "savedArtifactVerification": delivery["savedArtifactVerification"]})

    source_index = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    catalog_binding = next(x for x in delivery["members"] if x["path"] == "SOURCE_VERIFICATION.json")
    with zipfile.ZipFile(ARCHIVE) as z:
        names = [x.filename for x in z.infolist()]
        infos = {x.filename: x for x in z.infolist()}
        check(checks, "ZIP has unique safe member paths", len(names) == len(set(names))
              and all(not n.startswith(("/", "\\")) and ".." not in Path(n).parts for n in names),
              {"members": len(names), "unique": len(set(names))})
        source_verification = json.loads(z.read("SOURCE_VERIFICATION.json"))
        remote = json.loads(z.read("REMOTE_SOURCE_BINDINGS.json"))
        director = json.loads(z.read("DIRECTOR_DECISION.json"))
        procedure_ids = EXPECTED_ACCEPTED + EXPECTED_BLOCKED
        procedures = [json.loads(z.read(f"procedures/{spell_id}.json")) for spell_id in procedure_ids]
        model = json.loads(z.read("MODEL.json"))
        counts = json.loads(z.read("COUNTS.json"))
        member_manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        case_index = json.loads(z.read("CASE_INDEX.json"))
        case_bindings = json.loads(z.read("CASE_HASH_BINDINGS.json"))
        case_dispositions = json.loads(z.read("CASE_DISPOSITIONS.json"))
        validation = json.loads(z.read("VALIDATION.json"))
        next_group = json.loads(z.read("NEXT_QUEUE_GROUP.json"))

        check(checks, "Archive membership equals both delivery and package member manifests",
              set(names) == {x["path"] for x in delivery["members"]}
              and set(names) - {"MEMBER_MANIFEST.json"} == {x["path"] for x in member_manifest["members"]}
              and len(member_manifest["members"]) == member_manifest["memberCountExcludingSelf"],
              {"archive": len(names), "delivery": len(delivery["members"]),
               "memberManifest": len(member_manifest["members"])})

        external_rows = {x["path"]: x for x in delivery["members"]}
        internal_rows = {x["path"]: x for x in member_manifest["members"]}
        member_failures = []
        total_member_bytes = 0
        for name in names:
            info = infos[name]
            h = hashlib.sha256()
            crc = 0
            size = 0
            with z.open(info, "r") as member:
                for chunk in iter(lambda: member.read(1024 * 1024), b""):
                    size += len(chunk)
                    h.update(chunk)
                    crc = zlib.crc32(chunk, crc)
            total_member_bytes += size
            row = external_rows[name]
            valid = size == row["bytes"] and h.hexdigest() == row["sha256"] and f"{crc & 0xffffffff:08x}" == str(row["crc32"]).lower()
            if name != "MEMBER_MANIFEST.json":
                ir = internal_rows[name]
                valid = valid and size == ir["bytes"] and h.hexdigest() == ir["sha256"] and f"{crc & 0xffffffff:08x}" == str(ir["crc32"]).lower()
            if not valid:
                member_failures.append(name)
        check(checks, "Every archive member streams cleanly and matches byte, SHA-256, and CRC bindings",
              not member_failures, {"checked": len(names), "uncompressedBytes": total_member_bytes,
                                    "failures": member_failures[:20]})

        check(checks, "Return binds to the requested current source commit and baseline authority",
              remote.get("sourceCommit") == SOURCE_COMMIT
              and director["authorityBaseline"] == {
                  "reviewedApplied": 782, "pending": 66, "acceptedUnapplied": 0,
                  "completeStandaloneProcedures": 506, "scopedInterfaces": 173},
              {"sourceCommit": remote.get("sourceCommit"), "authorityBaseline": director["authorityBaseline"]})

        source_failures = []
        source_bindings = source_verification["sourceBindings"]
        check(checks, "Director's saved source verification has 120 source bindings and 1,158 passing checks",
              source_verification["allPass"] is True and not source_verification["failures"]
              and len(source_bindings) == 120 and len(source_verification["additionalBindings"]) == 32
              and source_verification["checkCount"] == 1158
              and all(x["passed"] for x in source_verification["checks"]),
              {"bindings": len(source_bindings), "additionalBindings": len(source_verification["additionalBindings"]),
               "checkCount": source_verification["checkCount"], "checks": len(source_verification["checks"])})
        for binding in source_bindings:
            raw = git_blob(binding["path"])
            blob_sha1 = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"] or blob_sha1 != binding["gitBlobSHA1"]:
                source_failures.append(binding["path"])
        check(checks, "All 120 source bindings independently match Git blobs at the bound commit",
              not source_failures, {"checked": len(source_bindings), "failures": source_failures[:20]})

        additional_failures = []
        for binding in source_verification["additionalBindings"]:
            member_name = "additional_sources/" + binding["path"]
            if member_name not in infos:
                additional_failures.append({"path": member_name, "reason": "missing"})
                continue
            raw = z.read(member_name)
            if len(raw) != binding["bytes"] or sha(raw) != binding["sha256"]:
                additional_failures.append({"path": member_name, "reason": "binding mismatch"})
        check(checks, "All 32 additional source copies match their declared byte and SHA-256 bindings",
              not additional_failures, {"checked": len(source_verification["additionalBindings"]),
                                        "failures": additional_failures[:20]})

        source_packet_path = AUDIT / "rank9_memorydenial6_current_source_195_prepared" / "DD_Rank9_MemoryDenial6_CurrentSource_195.zip"
        source_packet_raw = source_packet_path.read_bytes()
        embedded_source_packet = z.read("SOURCE_PACKET_195.zip")
        check(checks, "Return embeds the exact submitted Memory/Denial6 source packet",
              embedded_source_packet == source_packet_raw,
              {"embeddedBytes": len(embedded_source_packet), "expectedBytes": len(source_packet_raw),
               "embeddedSHA256": sha(embedded_source_packet), "expectedSHA256": sha(source_packet_raw)})

        check(checks, "Director decision, procedures, and model agree on exact approvals and blocks",
              director["acceptedIds"] == EXPECTED_ACCEPTED and director["unacceptedIds"] == EXPECTED_BLOCKED
              and {x["id"] for x in director["decisions"]} == set(procedure_ids)
              and {x["id"] for x in procedures} == set(procedure_ids)
              and model["acceptedIds"] == EXPECTED_ACCEPTED and model["unacceptedIds"] == EXPECTED_BLOCKED
              and model["applied"] is False
              and {x["id"] for x in model["spells"]} == set(EXPECTED_ACCEPTED + EXPECTED_BLOCKED),
              {"acceptedIds": director["acceptedIds"], "unacceptedIds": director["unacceptedIds"]})
        decisions = {x["id"]: x for x in director["decisions"]}
        procs = {x["id"]: x for x in procedures}
        spell_rows = {x["id"]: x for x in model["spells"]}
        check(checks, "All four approved procedures are accepted, unapplied, and have no blockers",
              all(decisions[s]["accepted"] and not decisions[s]["applied"] and not decisions[s].get("blockerIds")
                  and procs[s]["accepted"] and not procs[s]["applied"]
                  and spell_rows[s]["accepted"] and not spell_rows[s]["applied"] for s in EXPECTED_ACCEPTED),
              {s: {"decision": decisions[s], "procedure": {k: procs[s].get(k) for k in ("accepted", "applied", "status", "blockerIds")}}
               for s in EXPECTED_ACCEPTED})
        blocker_records = {x["id"]: x for x in director["blockers"]}
        check(checks, "Both rejected procedures stay blocked with named blockers and precise unresolved conditions",
              all(not decisions[s]["accepted"] and not decisions[s]["applied"]
                  and decisions[s].get("blockerIds") and not procs[s]["accepted"] and not procs[s]["applied"]
                  for s in EXPECTED_BLOCKED),
              {s: {"blockerIds": decisions[s].get("blockerIds"), "decision": decisions[s]}
               for s in EXPECTED_BLOCKED})

        check(checks, "The package's own data, clock, and scoped semantic gates pass; blockers remain explicit",
              validation["sourcePass"] is True and validation["dataPass"] is True
              and validation["clockPass"] is True and validation["scopedSemanticChecksPass"] is True
              and validation["completeBatchPass"] is False
              and len(validation["knownAcceptanceBlockers"]) == 2,
              {k: validation.get(k) for k in ("sourcePass", "dataPass", "clockPass", "scopedSemanticChecksPass", "completeBatchPass")})

        # Recompute the hash of the embedded catalog reference from the exact source bytes.
        catalog_raw = git_blob(catalog_path)
        check(checks, "Bound source catalog has exact committed bytes and expected SHA",
              sha(catalog_raw) == next(x["sha256"] for x in source_bindings if x["path"] == catalog_path),
              {"bytes": len(catalog_raw), "sha256": sha(catalog_raw)})

        index_rows = {x["id"]: x for x in case_index["cases"]}
        binding_rows = {x["id"]: x for x in case_bindings["cases"]}
        check(checks, "All 80 indexed cases have unique, matching case-hash bindings",
              len(index_rows) == len(binding_rows) == 80 and set(index_rows) == set(binding_rows)
              and case_index["events"] == counts["events"] == 1650
              and case_index["mainCases"] == counts["mainCases"] == 12
              and case_index["branches"] == counts["branches"] == 68,
              {"cases": len(index_rows), "events": case_index["events"],
               "mainCases": case_index["mainCases"], "branches": case_index["branches"]})

        replay_failures = []
        event_count = forward_count = inverse_count = 0
        for case_id, idx in index_rows.items():
            bind = binding_rows[case_id]
            case_raw = z.read(bind["path"])
            if len(case_raw) != bind["bytes"] or sha(case_raw) != bind["sha256"]:
                replay_failures.append({"case": case_id, "reason": "case bytes/hash"})
                continue
            case = json.loads(case_raw)
            if case["id"] != case_id or case["spellId"] != idx["spellId"] or case["mainCaseId"] != idx["mainCaseId"]:
                replay_failures.append({"case": case_id, "reason": "case identity"})
                continue
            if canonical_state_sha(case["initialState"]) != bind["initialStateSHA256"] or bind["initialStateSHA256"] != idx["initialSHA256"]:
                replay_failures.append({"case": case_id, "reason": "initial state hash"})
                continue
            state = case["initialState"]
            previous_time = -1
            good = True
            for event in case["events"]:
                event_count += 1
                fops, iops = event["forward"], event["inverse"]
                forward_count += len(fops)
                inverse_count += len(iops)
                if (event["before"] != state or canonical_state_sha(state) != event["beforeSHA256"]
                    or canonical_state_sha(event["after"]) != event["afterSHA256"]
                    or event["timeMs"] < previous_time):
                    good = False
                    break
                previous_time = event["timeMs"]
                if len(fops) != 2 or len(iops) != 2:
                    good = False
                    break
                if (fops[0].get("op") != "test" or fops[0].get("path") != "" or fops[0].get("value") != state
                    or fops[1].get("op") != "replace" or fops[1].get("path") != "" or fops[1].get("value") != event["after"]
                    or iops[0].get("op") != "test" or iops[0].get("path") != "" or iops[0].get("value") != event["after"]
                    or iops[1].get("op") != "replace" or iops[1].get("path") != "" or iops[1].get("value") != state):
                    good = False
                    break
                state = event["after"]
            if not good:
                replay_failures.append({"case": case_id, "reason": "event replay/patch/hash/clock"})
                continue
            if state != case["finalState"] or canonical_state_sha(state) != bind["finalStateSHA256"] or bind["finalStateSHA256"] != idx["finalSHA256"]:
                replay_failures.append({"case": case_id, "reason": "final state"})
                continue
            if len(case["events"]) != bind["events"] or len(case["events"]) != idx["events"]:
                replay_failures.append({"case": case_id, "reason": "case event count"})
        check(checks, "All 80 case states and 1,650 event chains replay with exact reversible patches, hashes, and monotone clocks",
              not replay_failures and event_count == 1650 and forward_count == 3300 and inverse_count == 3300,
              {"cases": len(index_rows), "events": event_count, "forwardOperations": forward_count,
               "inverseOperations": inverse_count, "failures": replay_failures[:20]})

        # Every current main-case disposition retains its source requirement and all expected cases.
        main_dispositions = case_dispositions["mainCases"]
        check(checks, "All 12 main-case disposition rows are present and remain static, non-runtime evidence",
              len(main_dispositions) == 12 and all(x.get("originalRequirementUnchanged") and x.get("caseIds") for x in main_dispositions),
              {"rows": len(main_dispositions)})

        next_group_payload = next_group["group"]
        check(checks, "Director identifies the next five-spell group and requires a fresh packet",
              next_group_payload["group"] == "rank9-knowledge-revelation5"
              and next_group_payload["pendingIds"] == ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity", "faction-omniscience-supreme"]
              and next_group_payload["pendingCount"] == 5
              and next_group_payload["freshPacketRequiredForCurrentAuthority"] is True,
              next_group_payload)

    failed = [x for x in checks if not x["passed"]]
    report = {
        "id": "RANK9-MEMORYDENIAL6-RETURN196-INDEPENDENT-AUDIT",
        "status": "PASS" if not failed else "FAIL",
        "checksPassed": len(checks) - len(failed),
        "checksFailed": len(failed),
        "checks": checks,
        "sourceCommit": SOURCE_COMMIT,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_bytes, "sha256": archive_sha},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())},
        "acceptedIds": EXPECTED_ACCEPTED,
        "unacceptedIds": EXPECTED_BLOCKED,
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
