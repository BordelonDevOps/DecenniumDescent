from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
import zlib
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = AUDIT / "rank9_memorydenial6_return224_received"
SOURCE_DIR = AUDIT / "rank9_memorydenial6_current_source_224_prepared"
SUPPLEMENT_DIR = AUDIT / "rank9_memorydenial6_return196_witness_supplement_224"
ARCHIVE = RETURN_DIR / "DD_Rank9_MemoryDenial2_Director_Return224.zip"
DELIVERY = RETURN_DIR / "DD_Rank9_MemoryDenial2_Director_Return224_DELIVERY.json"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_MemoryDenial6_CurrentSource_224.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_MemoryDenial6_CurrentSource_224_DELIVERY.json"
SUPPLEMENT_ARCHIVE = SUPPLEMENT_DIR / "DD_Rank9_MemoryDenial6_Return196_TargetWitnesses_224.zip"
SUPPLEMENT_DELIVERY = SUPPLEMENT_DIR / "DD_Rank9_MemoryDenial6_Return196_TargetWitnesses_224_DELIVERY.json"
REPORT = AUDIT / "RANK9_MEMORYDENIAL6_RETURN224_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9_MEMORYDENIAL6_RETURN224_RECEIPT.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(value: object) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))


def file_binding(path: Path) -> dict:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            size += len(chunk)
            h.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return {"bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xffffffff:08x}"}


def member_binding(zf: zipfile.ZipFile, name: str) -> dict:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with zf.open(name) as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            size += len(chunk)
            h.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return {"bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xffffffff:08x}"}


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and not name.startswith("/")


def add(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    source_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
    supplement_delivery = json.loads(SUPPLEMENT_DELIVERY.read_text(encoding="utf-8-sig"))

    ret_file = file_binding(ARCHIVE)
    ret_declared = delivery["archive"]
    add(checks, "Return224 archive bytes, SHA-256, and CRC32 match delivery",
        ret_file == {k: ret_declared[k] for k in ("bytes", "sha256", "crc32")}, ret_file)

    source_file = file_binding(SOURCE_ARCHIVE)
    source_declared = source_delivery["archive"]
    add(checks, "Current-source archive bytes and SHA-256 match its delivery",
        source_file["bytes"] == source_declared["bytes"] and source_file["sha256"] == source_declared["sha256"], source_file)
    supplement_file = file_binding(SUPPLEMENT_ARCHIVE)
    supplement_declared = supplement_delivery["archive"]
    add(checks, "Return196 witness supplement bytes and SHA-256 match its delivery",
        supplement_file["bytes"] == supplement_declared["bytes"] and supplement_file["sha256"] == supplement_declared["sha256"], supplement_file)

    target_ids = ["mind-collapse", "unravel-identity"]
    expected_authority = {
        "reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173,
    }
    add(checks, "Return224 decisions are exactly two held, unapplied identities at the submitted authority",
        delivery["authorityBaseline"] == expected_authority
        and delivery["accepted"] is False and delivery["applied"] is False
        and delivery["acceptedIds"] == [] and delivery["heldIds"] == target_ids
        and {x["id"] for x in delivery["decisions"]} == set(target_ids)
        and all(x["accepted"] is False and x["applied"] is False for x in delivery["decisions"]),
        {"authority": delivery["authorityBaseline"], "heldIds": delivery["heldIds"], "decisions": delivery["decisions"]})

    local_by_name = {
        SOURCE_ARCHIVE.name: (SOURCE_ARCHIVE, source_delivery),
        SUPPLEMENT_ARCHIVE.name: (SUPPLEMENT_ARCHIVE, supplement_delivery),
    }
    external_expected = delivery["externalSourceArchives"]
    external_results = []
    for row in external_expected:
        pair = local_by_name.get(Path(row["path"]).name)
        if not pair:
            external_results.append({"path": row["path"], "passed": False, "reason": "unknown external archive"})
            continue
        p, local_delivery = pair
        actual = file_binding(p)
        good = actual["bytes"] == row["bytes"] and actual["sha256"] == row["sha256"]
        if "crc32" in row:
            good = good and actual["crc32"] == str(row["crc32"]).lower()
        good = good and actual["bytes"] == local_delivery["archive"]["bytes"] and actual["sha256"] == local_delivery["archive"]["sha256"]
        external_results.append({"path": row["path"], "passed": good, **actual})
    add(checks, "Return224 external source archives bind to the exact locally submitted packets",
        len(external_results) == 2 and all(x["passed"] for x in external_results), external_results)

    # Stream all archive members and verify the outer and inner manifests.
    with zipfile.ZipFile(ARCHIVE) as zret, zipfile.ZipFile(SOURCE_ARCHIVE) as zsrc, zipfile.ZipFile(SUPPLEMENT_ARCHIVE) as zsup:
        ret_names = [x.filename for x in zret.infolist()]
        ret_unique_safe = len(ret_names) == len(set(ret_names)) and all(safe_member(x) for x in ret_names)
        add(checks, "Return224 ZIP paths are unique, safe, and CRC-clean", ret_unique_safe and zret.testzip() is None,
            {"members": len(ret_names), "unique": len(set(ret_names)), "testzip": zret.testzip()})

        internal = json.loads(zret.read("MEMBER_MANIFEST.json"))
        outer_rows = {x["path"]: x for x in delivery["members"]}
        inner_rows = {x["path"]: x for x in internal["members"]}
        members_ok = set(ret_names) == set(outer_rows) == set(delivery["allowlist"])
        members_ok = members_ok and set(ret_names) - {"MEMBER_MANIFEST.json"} == set(inner_rows)
        members_ok = members_ok and internal["memberCountExcludingSelf"] == len(inner_rows) == 67
        member_failures = []
        for name in ret_names:
            if not safe_member(name):
                member_failures.append({"path": name, "reason": "unsafe"})
                continue
            actual = member_binding(zret, name)
            expected = outer_rows.get(name)
            good = bool(expected) and all(actual[k] == expected.get(k) for k in ("bytes", "sha256", "crc32"))
            if name != "MEMBER_MANIFEST.json":
                expected_inner = inner_rows.get(name)
                good = good and bool(expected_inner) and all(actual[k] == expected_inner.get(k) for k in ("bytes", "sha256", "crc32"))
            if not good:
                member_failures.append({"path": name, "actual": actual})
        add(checks, "All 68 Return224 members match outer delivery rows and exact 67-member inner manifest",
            members_ok and not member_failures and len(ret_names) == delivery["memberCount"] == 68,
            {"members": len(ret_names), "innerMembers": len(inner_rows), "failures": member_failures[:12]})

        # Verify the two submitted input archives against their own external delivery manifests.
        packet_results = []
        for label, zf, d, expected_filename in [
            ("current-source", zsrc, source_delivery, SOURCE_ARCHIVE.name),
            ("witness-supplement", zsup, supplement_delivery, SUPPLEMENT_ARCHIVE.name),
        ]:
            names = [x.filename for x in zf.infolist()]
            manifest_name = "MANIFEST.json" if label == "current-source" else "SUPPLEMENT_MANIFEST.json"
            source_manifest = json.loads(zf.read(manifest_name))
            rows = {x["path"]: x for x in source_manifest["members"]}
            safe_unique = len(names) == len(set(names)) and all(safe_member(x) for x in names)
            ok = (safe_unique and set(names) - {manifest_name} == set(rows)
                  and len(names) == d["members"] and len(rows) == d["manifestBindings"]
                  and source_manifest.get("memberCountExcludingSelf") == len(rows) and zf.testzip() is None)
            failures = []
            for name in names:
                if not safe_member(name):
                    failures.append(name)
                    continue
                if name == manifest_name:
                    continue
                actual = member_binding(zf, name)
                row = rows.get(name, {})
                if not all(actual[k] == row.get(k) for k in ("bytes", "sha256", "crc32")):
                    failures.append(name)
            packet_results.append({"archive": label, "members": len(names), "manifestRows": len(rows),
                                   "passed": ok and not failures, "failures": failures[:12], "expectedFilename": expected_filename})
        add(checks, "Input packet and supplement ZIP members match their own delivery manifests",
            all(x["passed"] for x in packet_results), packet_results)

        source_bindings = json.loads(zret.read("SOURCE_BINDINGS.json"))
        source_rows = source_bindings["sources"]
        source_failures = []
        for row in source_rows:
            member = row["packetMember"]
            if member not in zsrc.namelist():
                source_failures.append({"path": row["path"], "reason": "missing source member", "member": member})
                continue
            raw = zsrc.read(member)
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or blob_sha != row["gitBlobSHA1"]:
                source_failures.append({"path": row["path"], "reason": "source/hash binding mismatch"})
        add(checks, "All 120 current source rows match their packed bytes, SHA-256, and Git blob IDs",
            len(source_rows) == 120 and not source_failures,
            {"rows": len(source_rows), "failures": source_failures[:16]})

        # The exact Return196 procedures/cases in the witness supplement must survive unchanged.
        return_case_paths = {n for n in ret_names if n.startswith("cases/") and n.endswith(".json")}
        supplement_case_paths = {n for n in zsup.namelist() if n.startswith("cases/") and n.endswith(".json")}
        byte_diff = []
        for name in sorted(return_case_paths | supplement_case_paths):
            if name not in ret_names or name not in zsup.namelist() or zret.read(name) != zsup.read(name):
                byte_diff.append(name)
        add(checks, "All 28 Return196 target cases are preserved byte-for-byte in Return224",
            len(return_case_paths) == len(supplement_case_paths) == 28 and not byte_diff,
            {"returnCases": len(return_case_paths), "supplementCases": len(supplement_case_paths), "differences": byte_diff[:12]})

        replay = json.loads(zret.read("CASE_REPLAY.json"))
        index = json.loads(zret.read("prior/CASE_INDEX.json"))
        bindings = json.loads(zret.read("prior/CASE_HASH_BINDINGS.json"))
        replay_rows = replay["cases"]
        index_rows = {x["id"]: x for x in index["cases"] if x.get("spellId") in target_ids}
        binding_rows = {x["id"]: x for x in bindings["cases"]
                        if x.get("id", "").startswith("RANK9MEMORYDENIAL6129-MIND-COLLAPSE-")
                        or x.get("id", "").startswith("RANK9MEMORYDENIAL6129-UNRAVEL-IDENTITY-")}
        replay_failures = []
        event_count = forward_count = inverse_count = 0
        statuses: dict[str, int] = {}
        if len(replay_rows) != 28 or set(index_rows) != set(binding_rows) or set(index_rows) != {x["id"] for x in replay_rows}:
            replay_failures.append({"reason": "index/binding/replay identities differ"})
        for summary in replay_rows:
            cid = summary["id"]
            path = summary["file"]
            if path not in ret_names:
                replay_failures.append({"case": cid, "reason": "case member missing"})
                continue
            raw = zret.read(path)
            case = json.loads(raw)
            idx = index_rows.get(cid, {})
            bind = binding_rows.get(cid, {})
            crc = f"{zlib.crc32(raw) & 0xffffffff:08x}"
            if not (case.get("id") == cid and case.get("spellId") == summary.get("spellId")
                    and case.get("mainCaseId") == summary.get("mainCaseId")
                    and len(raw) == summary["binding"]["bytes"] == bind.get("bytes")
                    and sha(raw) == summary["binding"]["sha256"] == bind.get("sha256")
                    and crc == summary["binding"]["crc32"]):
                replay_failures.append({"case": cid, "reason": "case identity or byte/hash/CRC binding"})
                continue
            initial = case["initialState"]
            final = case["finalState"]
            if (canonical_sha(initial) != case["initialSHA256"]
                    or case["initialSHA256"] != summary["initialSHA256"]
                    or case["initialSHA256"] != idx.get("initialSHA256")
                    or canonical_sha(final) != case["finalSHA256"]
                    or case["finalSHA256"] != summary["finalSHA256"]
                    or case["finalSHA256"] != idx.get("finalSHA256")):
                replay_failures.append({"case": cid, "reason": "initial/final state hash"})
                continue
            state = initial
            prior_time = -1
            good = True
            for event in case["events"]:
                event_count += 1
                fops = event["forward"]
                iops = event["inverse"]
                forward_count += len(fops)
                inverse_count += len(iops)
                if (event["before"] != state or canonical_sha(event["before"]) != event["beforeSHA256"]
                        or canonical_sha(event["after"]) != event["afterSHA256"]
                        or event["timeMs"] < prior_time or len(fops) != 2 or len(iops) != 2):
                    good = False
                    break
                prior_time = event["timeMs"]
                if (fops[0].get("op") != "test" or fops[0].get("path") != "" or fops[0].get("value") != state
                        or fops[1].get("op") != "replace" or fops[1].get("path") != "" or fops[1].get("value") != event["after"]
                        or iops[0].get("op") != "test" or iops[0].get("path") != "" or iops[0].get("value") != event["after"]
                        or iops[1].get("op") != "replace" or iops[1].get("path") != "" or iops[1].get("value") != state):
                    good = False
                    break
                # Forward replay and immediate inverse must each be exact.
                state = fops[1]["value"]
                if iops[1]["value"] != state and iops[1]["value"] != event["before"]:
                    good = False
                    break
                state = iops[1]["value"]
                if state != event["before"]:
                    good = False
                    break
                state = event["after"]
            if not good or state != final:
                replay_failures.append({"case": cid, "reason": "forward/inverse operation replay or monotone clock"})
                continue
            if not (len(case["events"]) == summary["events"] == idx.get("events") == bind.get("events")):
                replay_failures.append({"case": cid, "reason": "event count binding"})
                continue
            statuses[case["status"]] = statuses.get(case["status"], 0) + 1
            if not (summary["freshReplayPassed"] is True and summary["failures"] == 0
                    and summary["events"] == len(case["events"])
                    and summary["forwardOperations"] == len(case["events"]) * 2
                    and summary["inverseOperations"] == len(case["events"]) * 2):
                replay_failures.append({"case": cid, "reason": "replay summary disagreement"})
        totals = replay.get("totals", {})
        replay_good = (not replay_failures and len(replay_rows) == 28 and event_count == 553
                       and forward_count == inverse_count == 1106
                       and totals.get("events") == event_count
                       and totals.get("forwardOperations") == forward_count
                       and totals.get("inverseOperations") == inverse_count)
        add(checks, "All 28 case chains independently replay with exact forward/inverse patches, hashes, and clocks",
            replay_good,
            {"cases": len(replay_rows), "events": event_count, "forwardOperations": forward_count,
             "inverseOperations": inverse_count, "statusCounts": statuses, "totals": totals,
             "failures": replay_failures[:20]})

        # Independently confirm the one declared historical source-cache reconciliation.
        reconciliation = json.loads(zret.read("SOURCE_RECONCILIATION.json"))
        historical_index_raw = zret.read("prior/CLASS_CAPABILITY_SOURCE_INDEX.json")
        index_data = json.loads(historical_index_raw)
        warrior_index = next(x for x in index_data["classes"] if x["class"].lower() == "warrior")
        warrior_row = next(x for x in source_rows if x["path"].lower().endswith("/warrior.json"))
        warrior_data = json.loads(zsrc.read(warrior_row["packetMember"]))
        current_by_id = {x["id"]: x for x in warrior_data["cards"]}
        compared = 0
        recon_failures = []
        comparable = ("id", "band", "path", "minimumClassLevel", "acquisition", "sourceKind", "activation", "effect")
        for old_card in warrior_index["cards"]:
            now = current_by_id.get(old_card["id"])
            if now is None or any(old_card.get(k) != now.get(k) for k in comparable):
                recon_failures.append(old_card["id"])
            compared += 1
        actual_warrior_sha = sha(zsrc.read(warrior_row["packetMember"]))
        reconciliation_good = (reconciliation["status"] == "RECONCILED_NOT_ACCEPTANCE_BLOCKER"
                                and reconciliation["indexedCardsCompared"] == compared == 126
                                and reconciliation["actualCurrentSHA256"] == actual_warrior_sha == warrior_row["sha256"]
                                and reconciliation["recordedHistoricalSHA256"] != actual_warrior_sha
                                and not recon_failures)
        add(checks, "Warrior cache mismatch is independently reconciled across all 126 indexed card fields",
            reconciliation_good,
            {"cardsCompared": compared, "actualCurrentSHA256": actual_warrior_sha,
             "recordedHistoricalSHA256": reconciliation["recordedHistoricalSHA256"],
             "differences": recon_failures[:12]})

        source_reassessment = json.loads(zret.read("FULL_TURN_SOURCE_REASSESSMENT.json"))
        add(checks, "The retained Mind Collapse blocker is tied to the complete 16-class source scan",
            source_reassessment["blockerId"] == "MD196-B01" and source_reassessment["filesInspected"] == 16
            and source_reassessment["conclusion"] and len(source_reassessment["matches"]) == 39,
            {"filesInspected": source_reassessment["filesInspected"], "matches": len(source_reassessment["matches"]),
             "conclusion": source_reassessment["conclusion"]})

        decision = json.loads(zret.read("DIRECTOR_DECISION.json"))
        decision_rows = {x["id"]: x for x in decision["decisions"]}
        exact_blockers = {"mind-collapse": ["MD196-B01"], "unravel-identity": ["MD196-B02"]}
        add(checks, "Exact blocker and qualification records remain attached to each held spell",
            decision["acceptedIds"] == [] and decision["heldIds"] == target_ids and decision["applied"] is False
            and all(decision_rows[s]["blockerIds"] == exact_blockers[s]
                    and decision_rows[s]["accepted"] is False and decision_rows[s]["applied"] is False
                    and decision_rows[s]["holdIds"] and decision_rows[s]["conditionalQualificationIds"]
                    for s in target_ids),
            {s: {"blockerIds": decision_rows[s]["blockerIds"], "holdIds": decision_rows[s]["holdIds"]}
             for s in target_ids})

        # Compare the retained prior witness and all prior cases to the supplementary source.
        prior_proc_checks = []
        for spell in target_ids:
            path = f"prior/procedures/{spell}.json"
            supplement_path = f"procedures/{spell}.json"
            prior_proc_checks.append(path in zret.namelist() and supplement_path in zsup.namelist()
                                     and zret.read(path) == zsup.read(supplement_path))
        add(checks, "Both exact Return196 procedures match the independently delivered witness supplement",
            all(prior_proc_checks), {"procedures": dict(zip(target_ids, prior_proc_checks))})

        # Confirm the declared current next group and its pending IDs.
        next_group = decision["nextQueueGroup"]
        add(checks, "Director names a single next queue group without changing authority",
            next_group.get("group") == "rank9-knowledge-revelation5"
            and next_group.get("pendingIds") == ["faction-omniscience-supreme"]
            and delivery["authorityBaseline"] == expected_authority,
            next_group)

    package_checks = delivery["packageChecks"]
    check_rows = package_checks.get("checks", [])
    row_pass_values = [x.get("passed", x.get("pass")) for x in check_rows]
    add(checks, "GPT package checks contain 343 passing assertions and no failures",
        package_checks.get("count") == len(check_rows) == 343 and package_checks.get("failed") == 0
        and all(x is True for x in row_pass_values),
        {"declaredCount": package_checks.get("count"), "rows": len(check_rows), "failed": package_checks.get("failed"),
         "nonPassingRows": [x for x in check_rows if x.get("passed", x.get("pass")) is not True][:12]})

    failed = [x for x in checks if not x["passed"]]
    report = {
        "id": "RANK9-MEMORYDENIAL6-RETURN224-INDEPENDENT-AUDIT",
        "status": "PASS" if not failed else "FAIL",
        "returnArchive": {"path": str(ARCHIVE.relative_to(ROOT)), **ret_file},
        "deliveryManifest": {"path": str(DELIVERY.relative_to(ROOT)), "sha256": sha(DELIVERY.read_bytes())},
        "sourceArchive": {"path": str(SOURCE_ARCHIVE.relative_to(ROOT)), **source_file},
        "supplementArchive": {"path": str(SUPPLEMENT_ARCHIVE.relative_to(ROOT)), **supplement_file},
        "authority": expected_authority,
        "decisions": {x["id"]: {"accepted": x["accepted"], "applied": x["applied"], "blockerIds": x["blockerIds"]}
                      for x in delivery["decisions"]},
        "checksPassed": len(checks) - len(failed),
        "checksFailed": len(failed),
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "id": "RANK9-MEMORYDENIAL6-RETURN224-INDEPENDENT-RECEIPT",
        "status": report["status"],
        "auditReport": REPORT.name,
        "auditReportSHA256": sha(REPORT.read_bytes()),
        "returnArchive": report["returnArchive"],
        "deliveryManifest": report["deliveryManifest"],
        "authorityAfterReturn": expected_authority,
        "acceptedIds": [],
        "heldIds": target_ids,
        "canonicalChangesApplied": False,
        "checksPassed": report["checksPassed"],
        "checksFailed": report["checksFailed"],
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "report": str(REPORT),
                      "receipt": str(RECEIPT), "failed": failed}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
