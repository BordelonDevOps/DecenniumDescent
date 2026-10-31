from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = A / "rank9_wardcontrol6_return312_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_WardControl6_Director_Return312_HELD.zip"
RETURN_DELIVERY = RETURN_DIR / "DD_Rank9_WardControl6_Director_Return312_HELD_DELIVERY.json"
SOURCE_PACKET = A / "rank9_wardcontrol6_source_packet_312_prepared/DD_Rank9_WardControl6_CurrentSource_312.zip"
SOURCE_PACKET_AUDIT = A / "NULLIFICATION_WAVE_PACKET_312_INDEPENDENT_AUDIT.json"
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def main() -> None:
    results: list[dict] = []

    def check(name: str, passed: bool, detail: str = "") -> None:
        results.append({"check": name, "passed": bool(passed), "detail": detail})

    raw = RETURN_ZIP.read_bytes()
    delivery_raw = RETURN_DELIVERY.read_bytes()
    delivery = read(delivery_raw)
    expected_auth = AUTH
    packet_hash = hashlib.sha256(SOURCE_PACKET.read_bytes()).hexdigest()
    packet_audit = json.loads(SOURCE_PACKET_AUDIT.read_text(encoding="utf-8-sig"))
    check("sealed Return312 archive matches its exact delivery record",
          digest(raw) == {k: delivery["archive"][k] for k in digest(raw)}
          and delivery["archive"]["fileName"] == RETURN_ZIP.name,
          f"{len(raw)} bytes; SHA-256 {hashlib.sha256(raw).hexdigest()}")
    check("submitted Packet312 and its independent audit are the bound source",
          packet_audit.get("status") == "PASS"
          and packet_audit.get("failedChecks") == 0
          and delivery.get("sourceArchive", {}).get("sha256") == packet_hash,
          f"Packet312 SHA-256 {packet_hash}")
    check("decision is limited to a held Wave identity with no acceptance/application",
          delivery["scopeIds"] == ["nullification-wave"]
          and delivery["authority"] == expected_auth
          and delivery["acceptedIds"] == delivery["appliedIds"] == []
          and delivery["heldIds"] == ["nullification-wave"]
          and delivery["blockerIds"] == ["WC188-B01"]
          and delivery["closureTasksRemaining"] == 26
          and delivery["firstReviewTasksRemaining"] == 0,
          "822 applied / 26 pending / 0 accepted-unapplied; Wave only")

    with zipfile.ZipFile(RETURN_ZIP) as ret, zipfile.ZipFile(SOURCE_PACKET) as packet:
        names = ret.namelist()
        name_set = set(names)
        safe = all(not pathlib.PurePosixPath(n).is_absolute()
                   and ".." not in pathlib.PurePosixPath(n).parts for n in names)
        check("ZIP CRCs, unique safe paths and exact outer member count",
              ret.testzip() is None and len(names) == len(name_set) == delivery["archive"]["memberCount"] == 66 and safe,
              f"{len(names)} distinct members; ZIP CRC scan passed")

        manifest_raw = ret.read("MEMBER_MANIFEST.json")
        manifest = read(manifest_raw)
        external_rows = {r["path"]: r for r in delivery["members"]}
        internal_rows = {r["path"]: r for r in manifest["members"]}
        payload_names = name_set - {"MEMBER_MANIFEST.json"}
        check("internal and external member allowlists/manifests agree",
              manifest["selfExcluded"] is True
              and manifest["memberCount"] == 65
              and manifest["exactAllowlist"] == sorted(payload_names)
              and set(internal_rows) == payload_names
              and set(delivery["exactAllowlist"]) == name_set
              and set(external_rows) == name_set
              and digest(manifest_raw) == {k: delivery["memberManifest"][k] for k in digest(manifest_raw)},
              "65 payload members plus the separately bound internal manifest")
        member_hashes_ok = True
        for name in names:
            actual = digest(ret.read(name))
            member_hashes_ok &= actual == {k: external_rows[name][k] for k in actual}
            if name != "MEMBER_MANIFEST.json":
                member_hashes_ok &= actual == {k: internal_rows[name][k] for k in actual}
        check("all external and internal member byte/hash/CRC bindings recompute", member_hashes_ok,
              "Every archive member was checked against applicable manifests")

        decision = read(ret.read("DIRECTOR_DECISION.json"))
        decision_row = decision["decisions"][0]
        check("sealed decision agrees with delivery and retains WC188-B01 only",
              decision["scopeIds"] == ["nullification-wave"]
              and decision["authorityBefore"] == decision["authorityAfter"] == AUTH
              and decision["acceptedIds"] == decision["appliedIds"] == []
              and decision["heldIds"] == ["nullification-wave"]
              and decision_row["decision"] == "HOLD"
              and decision_row["blockerIds"] == ["WC188-B01"]
              and decision_row["spellId"] == "nullification-wave",
              "No canonical change, acceptance, application or blocker closure")
        check("missing Wave evidence is an explicit paid, integrated positive witness",
              len(decision_row["minimumMissingWitness"]) == 5
              and any("actual Wave payment" in x for x in decision_row["minimumMissingWitness"])
              and any("subsequent use" in x.lower() for x in decision_row["minimumMissingWitness"])
              and "no complete paid Nullification Wave encounter" in decision_row["finding"],
              "The exact Forge imprint is source-grounded; the integrated paid Wave encounter is absent")

        validation = read(ret.read("VALIDATION.json"))
        checks = validation["checks"]
        warnings = validation["inputMetadataWarnings"]
        check("Director validation stream has no failed assertions and discloses input warnings",
              validation["status"] == "PASS_WITH_INPUT_METADATA_WARNINGS"
              and validation["checkCount"] == 17511
              and validation["failedCount"] == 0
              and len(checks) == validation["checkCount"]
              and all(c.get("passed") is True for c in checks)
              and len(warnings) == 2
              and all(w["inputToken"] == "-Infinity" and w["actualFinalTimestampDeciseconds"] == -1
                      and w["actualEventCount"] == 0 for w in warnings),
              "Two preserved non-standard input sentinels are documented; source history is not rewritten")

        semantic = read(ret.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        semantic_findings = {c["id"]: c["result"] for c in semantic["checks"]}
        check("semantic review agrees that no new Wave positive witness exists",
              semantic["result"] == "HOLD_REQUIRED_POSITIVE_WITNESS_MISSING"
              and semantic_findings.get("R312-S07") == "GAP_WHOLE_IDENTITY_HELD"
              and semantic["numericSuccessIsNotSemanticCompletion"] is True
              and semantic["gates"]["applicationPerformed"] is False,
              "Return312 distinguishes source contract from whole-identity Wave completion")

        source_rows = read(ret.read("SOURCE_BINDINGS.json"))
        current_rows = source_rows["currentBindings"]
        extra_rows = source_rows["extraBindings"]
        current_ok = len(current_rows) == source_rows["sourceCount"] == 91
        for row in current_rows:
            member = "sources_current/" + row["path"]
            current_ok &= digest(packet.read(member)) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
            live = ROOT / pathlib.Path(row["path"])
            current_ok &= live.is_file() and digest(live.read_bytes()) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
        extra_ok = len(extra_rows) == source_rows["extraBindingRowCount"] == 11
        for row in extra_rows:
            archive = ret if row["member"] in name_set else packet
            extra_ok &= row["member"] in archive.namelist()
            if row["member"] in archive.namelist():
                extra_ok &= digest(archive.read(row["member"])) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
            live = ROOT / pathlib.Path(row["path"])
            extra_ok &= live.is_file() and digest(live.read_bytes()) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
        check("91 refreshed source bindings match the exact Packet312 archive and worktree", current_ok,
              "Each current source is checked in Packet312 and again against the live worktree")
        check("11 direct component-source bindings match Return312 payload bytes", extra_ok,
              "Included Forge and Glove evidence is checked against exact byte/hash/CRC bindings")

        case_results = read(ret.read("CASE_RESULTS.json"))
        cases_ok = len(case_results["cases"]) == 18
        event_counts = forward = inverse = 0
        for case in case_results["cases"]:
            old = packet.read(case["inputMember"])
            new = ret.read(case["returnMember"])
            cases_ok &= old == new and digest(new)["sha256"] == case["sha256"] and len(new) == case["bytes"]
            cases_ok &= case["numericReplay"] == case["dataReplay"] == "PASS"
            cases_ok &= case["fullReverseTraversal"] == "PASS"
            cases_ok &= (case["recordedEventClockCheck"] == "PASS"
                         or (case["events"] == 0
                             and case["evidenceStatus"] == "HELD_NOT_POSITIVE_WITNESS"
                             and case["recordedEventClockCheck"] == "NOT_APPLICABLE_ZERO_EVENTS"))
            cases_ok &= case["newSemanticCompletionInferred"] is False
            event_counts += case["events"]
            forward += case["forwardOperations"]
            inverse += case["inverseOperations"]
        cases_ok &= (event_counts, forward, inverse) == (967, 1934, 1934)
        check("18 Wave case records are byte-preserved from Packet312 and count consistently",
              cases_ok, f"18 cases; {event_counts} events; {forward} forward and {inverse} inverse operations")

        queue = read(ret.read("REMAINING_QUEUE.json"))
        next_group = queue["nextPendingGroup"]
        check("next separate task and priority order are explicit and match Director response",
              next_group["nextIdentity"] == "reality-anchor"
              and next_group["blockerIds"] == ["WC188-B02"]
              and next_group["separatePacket"] is True
              and queue["closureTasksRemaining"] == 26
              and queue["firstReviewTasksRemaining"] == 0,
              "Reality Anchor / WC188-B02 is next; Time Stop → Fate Rewrite → Collapse Timeline → Eternal Prophecy follow")

    failures = [r for r in results if not r["passed"]]
    report = {
        "id": "NULLIFICATION-WAVE-RETURN312-INDEPENDENT-AUDIT",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(results), "passedChecks": len(results) - len(failures),
        "failedChecks": len(failures), "checks": results,
        "returnArchive": {"path": RETURN_ZIP.relative_to(ROOT).as_posix(), **digest(raw)},
        "delivery": {"path": RETURN_DELIVERY.relative_to(ROOT).as_posix(), **digest(delivery_raw)},
        "submittedPacket": {"path": SOURCE_PACKET.relative_to(ROOT).as_posix(), **digest(SOURCE_PACKET.read_bytes())},
        "interpretiveLimit": "This verifies sealed decision bindings, archive integrity, exact preservation, current source bytes, and consistency with the Director-supplied validation stream. It does not create the missing integrated paid Wave witness or independently validate fictional encounter semantics.",
    }
    out = A / "NULLIFICATION_WAVE_RETURN312_INDEPENDENT_AUDIT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": report["checkCount"],
                      "failedChecks": report["failedChecks"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit("Return312 independent audit failed")


if __name__ == "__main__":
    main()
