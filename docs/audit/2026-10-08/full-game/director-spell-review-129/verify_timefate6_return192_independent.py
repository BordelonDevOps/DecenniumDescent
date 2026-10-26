from __future__ import annotations

import hashlib
import json
import subprocess
import traceback
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import jsonpatch


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_timefate6_return192_received"
ARCHIVE = RECEIVED / "DD_Rank9_TimeFate6_Director_Return192.zip"
DELIVERY = RECEIVED / "DD_Rank9_TimeFate6_Director_Return192_DELIVERY.json"
REPORT = AUDIT / "RANK9_TIMEFATE6_RETURN192_INDEPENDENT_AUDIT.json"
SOURCE_COMMIT = "38fec0bbf19a4480098eb10ab0d992b055790ada"
PUBLISHED_COMMIT = "430711c04d5a566ca523b1a8037a154c32184670"
AUTHORITY = {
    "reviewedApplied": 777,
    "pending": 71,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 501,
    "scopedInterfaces": 173,
}
ACCEPTED = ["time-fracture", "foresight-perfect"]
UNACCEPTED = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
GROUP = ["time-stop", "time-fracture", "foresight-perfect", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
EXPECTED_BLOCKERS = {
    "time-stop": ["TF192-B01"],
    "eternal-prophecy": ["TF192-B02"],
    "fate-rewrite": ["TF192-B04"],
    "collapse-timeline": ["TF192-B05"],
}

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


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT)


def git_blob_id(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True).strip()


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def check(label: str, passed: bool, detail=None) -> None:
    checks.append({"check": label, "passed": bool(passed), **({"detail": detail} if detail is not None else {})})
    if not passed:
        failures.append(label)


def verify_nested_packet(source_raw: bytes, inner_delivery: dict, source_rows: list[dict]) -> tuple[int, int]:
    import io

    with zipfile.ZipFile(io.BytesIO(source_raw)) as packet:
        names = packet.namelist()
        assert packet.testzip() is None and len(names) == len(set(names)) and all(safe_member(n) for n in names)
        delivery = inner_delivery
        manifest = read_json(packet.read("MANIFEST.json"))
        rows = manifest["members"]
        rows_by_name = {row["path"]: row for row in rows}
        assert manifest["memberCountExcludingSelf"] == len(rows) == len(names) - 1
        assert set(rows_by_name) == set(names) - {"MANIFEST.json"}
        assert delivery["members"] == len(names) == 169
        assert delivery["manifestBindings"] == len(rows) == 168
        for row in rows:
            raw = packet.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"].lower()
        context = read_json(packet.read("CURRENT_CONTEXT_191.json"))
        candidate = read_json(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_191.json"))
        assert context["sourceCommit"] == SOURCE_COMMIT
        assert context["sourceAuthority"] == AUTHORITY
        assert candidate["currentSourceCommit"] == SOURCE_COMMIT
        assert candidate["currentAuthority"] == AUTHORITY
        assert [row["spellId"] for row in candidate["records"]] == GROUP
        assert delivery["sourceAuthority"] == AUTHORITY
        assert delivery["sourceCommit"] == SOURCE_COMMIT and delivery["sourceFilesRefreshed"] == len(source_rows) == 140
        for row in source_rows:
            raw = packet.read("sources_current/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        return len(rows), len(names)


def replay_case(case: dict, binding: dict) -> tuple[int, int, int]:
    state = case["initialState"]
    assert sha(canonical(state)) == binding["initialStateSHA256"]
    assert case["events"], f"case has no events: {case['id']}"
    assert state == case["events"][0]["before"]
    seen: set[str] = set()
    forward_ops = inverse_ops = 0
    last_world_ms = state.get("world", {}).get("nowMs")
    for event in case["events"]:
        assert event["id"] not in seen, f"duplicate event {event['id']} in {case['id']}"
        seen.add(event["id"])
        before, after = event["before"], event["after"]
        assert state == before, f"event chain break {event['id']}"
        assert sha(canonical(before)) == event["beforeSHA256"]
        assert sha(canonical(after)) == event["afterSHA256"]
        now_ms = after.get("world", {}).get("nowMs")
        if last_world_ms is not None and now_ms is not None:
            assert now_ms >= last_world_ms, f"world clock moved backward in {event['id']}"
        calculated = jsonpatch.JsonPatch(event["forward"]).apply(before, in_place=False)
        restored = jsonpatch.JsonPatch(event["inverse"]).apply(after, in_place=False)
        assert calculated == after, f"forward patch mismatch {event['id']}"
        assert restored == before, f"inverse patch mismatch {event['id']}"
        forward_ops += len(event["forward"])
        inverse_ops += len(event["inverse"])
        state, last_world_ms = after, now_ms
    assert state == case["finalState"]
    assert sha(canonical(state)) == binding["finalStateSHA256"]
    return len(case["events"]), forward_ops, inverse_ops


def verify() -> dict:
    delivery_raw = DELIVERY.read_bytes()
    delivery = read_json(delivery_raw)
    archive_sha = sha_file(ARCHIVE)
    check(
        "Separate delivery record binds exact return ZIP bytes",
        ARCHIVE.stat().st_size == delivery["archive"]["bytes"] == 90_939_303
        and archive_sha == delivery["archive"]["sha256"] == "358e40cd8f68a5115f57d6375f178440201aac1a969c2cdf717e20acf8aa461c",
        {"bytes": ARCHIVE.stat().st_size, "sha256": archive_sha},
    )
    check(
        "Delivery record is unapplied and names exactly two accepted IDs",
        delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED
        and delivery["applied"] is False and delivery["appliedIds"] == []
        and delivery["canonicalFilesModified"] is False and delivery["sourceProgramsExecuted"] is False
        and delivery["runtimeExecuted"] is False and delivery["sourceAuthority"] == AUTHORITY,
    )
    try:
        with zipfile.ZipFile(ARCHIVE) as archive:
            names = archive.namelist()
            delivery_members = {row["path"]: row for row in delivery["members"]}
            manifest = read_json(archive.read("MEMBER_MANIFEST.json"))
            manifest_members = {row["path"]: row for row in manifest["members"]}
            check(
                "Return ZIP members are unique, safe, CRC-clean and exactly delivery-allowlisted",
                archive.testzip() is None and len(names) == len(set(names)) == len(delivery_members) == 129
                and set(names) == set(delivery_members) and all(safe_member(n) for n in names),
                {"archiveMembers": len(names), "deliveryMembers": len(delivery_members)},
            )
            check(
                "Internal member manifest covers every archive member except itself",
                manifest["memberCountExcludingSelf"] == len(manifest_members) == len(names) - 1
                and manifest["totalArchiveMembers"] == len(names)
                and set(manifest_members) == set(names) - {"MEMBER_MANIFEST.json"},
            )
            member_hashes_ok = True
            for name in names:
                raw = archive.read(name)
                row = delivery_members[name]
                if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" != row["crc32"].lower():
                    member_hashes_ok = False
                    break
                if name != "MEMBER_MANIFEST.json" and (len(raw) != manifest_members[name]["bytes"] or sha(raw) != manifest_members[name]["sha256"] or f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" != manifest_members[name]["crc32"].lower()):
                    member_hashes_ok = False
                    break
            check("All 129 outer ZIP members match independent byte, SHA-256 and CRC32 recalculation", member_hashes_ok)

            # Verify declared current source bytes against both the source anchor and published HEAD.
            source_bindings = read_json(archive.read("SOURCE_BINDINGS.json"))
            source_ok = source_bindings["sourceCommit"] == SOURCE_COMMIT and source_bindings["publishedCommit"].startswith(PUBLISHED_COMMIT[:8])
            source_rows = source_bindings["currentSourceBindingsUnchanged"]
            source_ok = source_ok and len(source_rows) == 140
            for row in source_rows:
                raw_anchor = git_blob(SOURCE_COMMIT, row["path"])
                raw_head = git_blob("HEAD", row["path"])
                if (len(raw_anchor), sha(raw_anchor), git_blob_id(SOURCE_COMMIT, row["path"])) != (row["bytes"], row["sha256"], row["gitBlobSHA1"]):
                    source_ok = False
                    break
                if raw_head != raw_anchor:
                    source_ok = False
                    break
            check("All 140 current-source bindings match Git blobs at packet anchor and current HEAD", source_ok, {"count": len(source_rows), "sourceCommit": source_bindings["sourceCommit"]})

            for supplemental in source_bindings["supplementalBindings"]:
                binding = supplemental["exactSourceBinding"]
                raw = git_blob(supplemental["sourceCommit"], binding["path"])
                assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
                assert raw == archive.read(supplemental["packagePath"])
            check("All three explicitly scoped supplemental source bindings match Git and archive bytes", len(source_bindings["supplementalBindings"]) == 3)

            # The inner source packet is verification material, never executed.
            inner_raw = archive.read("source/DD_Rank9_TimeFate6_CurrentSource_191.zip")
            inner_delivery_raw = archive.read("source/DD_Rank9_TimeFate6_CurrentSource_191_DELIVERY.json")
            inner_delivery = read_json(inner_delivery_raw)
            inner_row = source_bindings["packet"]
            assert inner_row["bytes"] == len(inner_raw) and inner_row["sha256"] == sha(inner_raw)
            assert inner_delivery["archive"]["bytes"] == len(inner_raw) and inner_delivery["archive"]["sha256"] == sha(inner_raw)
            inner_count, inner_total = verify_nested_packet(inner_raw, inner_delivery, source_rows)
            check("Nested current-source packet validates its source anchor, authority, 169 members and exact hashes", inner_count == 168 and inner_total == 169)

            decision = read_json(archive.read("DIRECTOR_DECISION.json"))
            procedures_doc = read_json(archive.read("PROCEDURES.json"))
            procedures = {row["spellId"]: row for row in procedures_doc["spells"]}
            decisions = {row["spellId"]: row for row in decision["perIdentity"]}
            check(
                "Director decision, procedures and authority agree on exact partial acceptance",
                decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == UNACCEPTED
                and decision["applied"] is False and decision["appliedIds"] == []
                and decision["authorityAtReview"] == AUTHORITY and decision["recordedAuthorityUnchanged"] is True
                and procedures_doc["acceptedIds"] == ACCEPTED and procedures_doc["appliedIds"] == []
                and set(procedures) == set(GROUP),
            )
            blocker_map = {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED}
            check("Four nonaccepted identities retain exact named blockers", blocker_map == EXPECTED_BLOCKERS)
            prior_blockers = json.loads((AUDIT / "RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_INDEPENDENT_AUDIT.json").read_text(encoding="utf-8-sig"))
            prior_return = json.loads((AUDIT / "rank9_agencycontrol9_return190_reconciled01_received/DD_Rank9_AgencyControl9_Director_Return190_Reconciled01_DELIVERY.json").read_text(encoding="utf-8-sig"))
            old_blockers = prior_return["decisions"].get("retainedInheritedBlockers") or prior_return.get("retainedInheritedBlockers")
            exact_carry = decision["carryForwardExact"]
            check("Return190’s two unresolved blockers are carried forward verbatim", len(exact_carry) == 2 and {row["id"] for row in exact_carry} == {"AG190-B01", "AG190-B02"})

            # Verify current catalog and index rows are the exact copies the director reviewed.
            index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
            catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
            index = json.loads(index_path.read_text(encoding="utf-8-sig"))
            catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
            index_rows = {row["id"]: row for row in index["entries"]}
            catalog_rows = {row["id"]: row for row in catalog["spells"]}
            exact_snapshots = True
            for sid, proc in procedures.items():
                exact_snapshots &= proc["currentCatalogSourceAndAccessUnchanged"] == catalog_rows[sid]
                exact_snapshots &= proc["currentIndexEntryUnchanged"] == index_rows[sid]
                exact_snapshots &= proc["applied"] is False
                native_rows = proc["nativeBookBindingsUnchanged"]
                placements = catalog_rows[sid]["source"]["original"]["placements"]
                exact_snapshots &= len(native_rows) == len(placements)
                for native in native_rows:
                    exact_snapshots &= native["spellId"] == sid and native["summaryDifferencePreserved"] is False
                    exact_snapshots &= native["catalogPlacement"] in placements
                    for field in ("name", "school", "level", "summary"):
                        exact_snapshots &= native["currentBookRow"].get(field) == native["catalogPlacement"].get(field)
            check("All six exact native cards and index rows match current canonical catalog and index", exact_snapshots)
            check("Only the two accepted procedures are free of acceptance blockers", all(procedures[s]["accepted"] and decisions[s]["accepted"] for s in ACCEPTED) and all(not procedures[s]["accepted"] for s in UNACCEPTED))

            # Recalculate case hashes and replay every event for the two accepted identities.
            casebook = read_json(archive.read("CASEBOOK.json"))
            cases = {case["id"]: case for case in casebook["cases"]}
            assert len(cases) == 90
            case_bindings = read_json(archive.read("CASE_HASH_BINDINGS.json"))
            case_hash_rows = {row["id"]: row for row in case_bindings}
            for cid, row in case_hash_rows.items():
                raw = archive.read(f"cases/{cid}.json")
                assert sha(canonical(read_json(raw))) == row["caseSHA256"]
            check("All 90 independent case files match their case hash bindings", len(case_hash_rows) == 90)

            replayed_cases = replayed_events = replayed_forward = replayed_inverse = 0
            for sid in ACCEPTED:
                proc = procedures[sid]
                selected = {cid for cid, case in cases.items() if case["spellId"] == sid}
                assert selected == set(proc["caseIds"])
                for cid in selected:
                    e, f, i = replay_case(cases[cid], case_hash_rows[cid])
                    replayed_cases += 1
                    replayed_events += e
                    replayed_forward += f
                    replayed_inverse += i
            check(
                "Every accepted identity case replays with continuous state, monotonic world time, valid hashes and exact forward/inverse patches",
                replayed_cases == 28 and replayed_events == 822 and replayed_forward == replayed_inverse == 1_644,
                {"cases": replayed_cases, "events": replayed_events, "forwardPatchOps": replayed_forward, "inversePatchOps": replayed_inverse},
            )

            # Human semantic screen of the accepted authored scope against the printed cards.
            fracture = procedures["time-fracture"]["procedure"]
            foresight = procedures["foresight-perfect"]["procedure"]
            semantic = {
                "time-fracture": all(term in fracture["replacement"].lower() for term in ["mandatory", "disadvantage", "no recursive replacement"])
                and "t+60seconds" in fracture["lifecycle"]
                and "within120ft" in fracture["selection"]
                and all(term in fracture["lineage"].lower() for term in ["de4-guard-01", "no re-entry", "fixed substitution"]),
                "foresight-perfect": all(term in foresight["benefits"].lower() for term in ["surprise", "critical hit", "advantage", "saving throw"])
                and "3600 elapsed world seconds" in foresight["benefits"]
                and "Self only" in foresight["target"]
                and all(term in foresight["lifecycle"].lower() for term in ["suppression", "dispel", "death"]),
            }
            check("Accepted procedures stay within their printed effect and state finite timing/source, counter and target limits", all(semantic.values()), semantic)
            check("All nine scope qualifications remain explicit; no runtime, balance, release, cosmology or closure approval is implied", all(len(procedures[s]["boundaries"]) == 9 and all(procedures[s]["boundaries"].values()) for s in ACCEPTED))

            next_queue = read_json(archive.read("NEXT_QUEUE_GROUP.json"))
            next_group = delivery["nextQueueGroup"]
            check("Next group record is still explicitly pending fresh authority", next_group.get("group") == "rank9-casting-cost5" and next_group.get("freshPacketRequiredForCurrentAuthority") is True and next_queue["nextAfterThisExactGroup"] == next_group)
    except Exception as exc:
        check("Independent verification completed without an exception", False, traceback.format_exc())

    report = {
        "id": "RANK9-TIMEFATE6-RETURN192-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "checksPassed": sum(1 for row in checks if row["passed"]),
        "checksFailed": len(failures),
        "failures": failures,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": ARCHIVE.stat().st_size, "sha256": sha_file(ARCHIVE)},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_raw), "sha256": sha(delivery_raw)},
        "sourceCommit": SOURCE_COMMIT,
        "publishedCommit": PUBLISHED_COMMIT,
        "sourceAuthority": AUTHORITY,
        "acceptedIds": ACCEPTED,
        "unacceptedIds": UNACCEPTED,
        "applied": False,
        "replay": {"acceptedCases": replayed_cases if "replayed_cases" in locals() else 0, "events": replayed_events if "replayed_events" in locals() else 0, "forwardOperations": replayed_forward if "replayed_forward" in locals() else 0, "inverseOperations": replayed_inverse if "replayed_inverse" in locals() else 0},
        "semanticScreen": semantic if "semantic" in locals() else {},
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    result = verify()
    raise SystemExit(0 if result["status"] == "PASS" else 1)
