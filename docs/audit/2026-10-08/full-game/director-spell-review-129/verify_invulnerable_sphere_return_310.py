from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
IN = A / "rank9_defenseform8_return310_received"
RETURN_ZIP = IN / "DD_Rank9_DefenseForm8_Director_Return310_HELD.zip"
RETURN_DELIVERY = IN / "DD_Rank9_DefenseForm8_Director_Return310_HELD_DELIVERY.json"
PACKET310 = A / "rank9_defenseform8_current_source_310_prepared/DD_Rank9_DefenseForm8_CurrentSource_310.zip"
PACKET_DELIVERY = A / "rank9_defenseform8_current_source_310_prepared/DD_Rank9_DefenseForm8_CurrentSource_310_DELIVERY.json"
SPHERE_CASES = {
    "DF218-SPHERE-ACTUAL-CROWN-COMMAND",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-A",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B1-TELEPORT",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B2-CONSENT-END",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B3-HIDDEN-OCCUPANCY",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B5-CONTROL",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-COUNTER",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-access",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-components",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-range",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-resource",
    "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-READY-EXPIRES",
}
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main() -> None:
    results: list[dict] = []

    def check(name: str, passed: bool, detail: str = "") -> None:
        results.append({"check": name, "passed": bool(passed), "detail": detail})

    return_raw = RETURN_ZIP.read_bytes()
    delivery = json.loads(RETURN_DELIVERY.read_text(encoding="utf-8-sig"))
    packet_delivery = json.loads(PACKET_DELIVERY.read_text(encoding="utf-8-sig"))
    packet_sha = hashlib.sha256(PACKET310.read_bytes()).hexdigest()
    check("outer return archive matches sealed delivery",
          digest(return_raw) == {k: delivery["archive"][k] for k in digest(return_raw)},
          f"{len(return_raw)} bytes; SHA-256 {hashlib.sha256(return_raw).hexdigest()}")
    check("return decision scope and authority are held without acceptance/application",
          delivery["scopeIds"] == ["invulnerable-sphere"]
          and delivery["authority"] == AUTH
          and delivery["acceptedIds"] == delivery["appliedIds"] == []
          and delivery["heldIds"] == ["invulnerable-sphere"]
          and delivery["blockerIds"] == ["DF218-B04"]
          and delivery["closureTasksRemaining"] == 26
          and delivery["firstReviewTasksRemaining"] == 0,
          "822/26/0, one scoped hold, 26 closure tasks, zero first-review tasks")
    check("return decision binds the exact submitted Packet310 archive",
          delivery.get("externalSourceArchive", {}).get("sha256") == packet_sha
          and packet_delivery["archive"]["sha256"] == packet_sha,
          f"Packet310 SHA-256 {packet_sha}")

    with zipfile.ZipFile(RETURN_ZIP) as ret, zipfile.ZipFile(PACKET310) as packet:
        names = ret.namelist()
        name_set = set(names)
        safe = all(not pathlib.PurePosixPath(n).is_absolute()
                   and ".." not in pathlib.PurePosixPath(n).parts for n in names)
        check("ZIP integrity, safe unique names and exact member count",
              ret.testzip() is None and len(names) == len(name_set) == delivery["memberCount"] == 48 and safe,
              f"{len(names)} unique members; CRC test passed")

        manifest_raw = ret.read("MEMBER_MANIFEST.json")
        manifest = read(manifest_raw)
        external_rows = {r["path"]: r for r in delivery["members"]}
        internal_rows = {r["path"]: r for r in manifest["members"]}
        payload_names = name_set - {"MEMBER_MANIFEST.json"}
        check("internal/external allowlists and self-excluding manifest agree",
              manifest["selfExcluded"] is True
              and manifest["memberCountExcludingSelf"] == 47
              and set(manifest["exactPayloadAllowlist"]) == payload_names
              and set(internal_rows) == payload_names
              and set(delivery["exactAllowlist"]) == name_set
              and set(external_rows) == name_set
              and digest(manifest_raw) == {k: delivery["memberManifest"][k]
                                           for k in digest(manifest_raw)},
              "47 payload members plus the bound manifest")
        member_hashes_ok = True
        for name in names:
            actual = digest(ret.read(name))
            member_hashes_ok &= actual == {k: external_rows[name][k] for k in actual}
            if name != "MEMBER_MANIFEST.json":
                member_hashes_ok &= actual == {k: internal_rows[name][k] for k in actual}
        check("all internal and external member hashes/CRCs", member_hashes_ok,
              "48 external rows; 47 internal payload rows")

        package_checks = delivery["packageChecks"]
        check("Director package-check stream reports all 290 checks passing",
              package_checks["status"] == "PASS" and package_checks["checkCount"] == 290
              and package_checks["failedCount"] == 0
              and all(c["passed"] for c in package_checks["checks"]),
              "This checks the supplied validation stream in addition to recomputing archive hashes above.")
        validation = read(ret.read("VALIDATION.json"))
        check("Director return validation reports 6,818/6,818 checks passing",
              validation["status"] == "PASS" and validation["checkCount"] == 6818
              and validation["failedCount"] == 0
              and all(c["passed"] for c in validation["checks"]),
              "Supplied return validation is internally consistent; it is not treated as independent semantic proof.")

        decision = read(ret.read("DIRECTOR_DECISION.json"))
        blockers = read(ret.read("BLOCKERS.json"))
        check("sealed decision and blocker record agree on DF218-B04 HOLD",
              decision["scopeIds"] == ["invulnerable-sphere"]
              and decision["authorityBefore"] == decision["authorityAfter"] == AUTH
              and decision["acceptedIds"] == decision["appliedIds"] == []
              and decision["heldIds"] == ["invulnerable-sphere"]
              and decision["decisions"][0]["decision"] == "HOLD"
              and decision["decisions"][0]["blockerIds"] == ["DF218-B04"]
              and decision["decisions"][0]["blockerScopeRevised"] is False
              and blockers["targetId"] == "invulnerable-sphere"
              and [b["id"] for b in blockers["blockers"]] == ["DF218-B04"],
              "No acceptance, application, or blocker revision")
        missing = decision["decisions"][0]["minimumMissingWitness"]
        finding = decision["decisions"][0]["finding"]
        check("missing witness is specific and does not invent route evidence",
              len(missing) == 5
              and all(s in finding for s in ["legal acquired actor", "authorized specific other-plane endpoint",
                                                "body/cargo/custody", "paid Sphere-caused denial"])
              and all("route" in s.lower() or "actor" in s.lower() or "destination" in s.lower()
                      or "body" in s.lower() or "sphere" in s.lower() for s in missing),
              "Five narrow source/actor/endpoint/subject/integrated-witness requirements")

        source_bindings = read(ret.read("SOURCE_BINDINGS.json"))
        rows = source_bindings["sourceRows"]
        source_ok = len(rows) == 87 and source_bindings["verifiedCurrentSourceCount"] == 87
        for row in rows:
            path = row["path"]
            member = "sources_current/" + path
            current_raw = packet.read(member)
            live_path = ROOT / pathlib.Path(path)
            live_raw = live_path.read_bytes() if live_path.is_file() else b""
            source_ok &= digest(current_raw) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
            source_ok &= digest(live_raw) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
        check("87 source bindings match Packet310 and current worktree bytes", source_ok,
              "Per-path byte length, SHA-256 and CRC32")

        cases = read(ret.read("CASE_RESULTS.json"))
        case_rows = cases["cases"]
        case_ids = {c["caseId"] for c in case_rows}
        cases_ok = case_ids == SPHERE_CASES and len(case_rows) == 14
        for case in case_rows:
            old = packet.read(case["inputMember"])
            new = ret.read(case["outputMember"])
            cases_ok &= old == new and digest(new) == case["binding"]
            cases_ok &= case["dataReplay"] == case["fullReverseTraversal"] == case["recordedClockConsistency"] == "PASS"
            cases_ok &= case["newSemanticCompletionInferred"] is False
        proc_in = "history/Return218/procedures/invulnerable-sphere.json"
        procedure_ok = ret.read("procedures/invulnerable-sphere.json") == packet.read(proc_in)
        events = sum(c["events"] for c in case_rows)
        forward = sum(c["forwardOperations"] for c in case_rows)
        inverse = sum(c["inverseOperations"] for c in case_rows)
        cases_ok &= (events, forward, inverse) == (327, 654, 654)
        cases_ok &= cases["counts"]["preservedCases"] == 14
        check("Sphere procedure and all 14 cases are byte-preserved and correctly summarized",
              procedure_ok and cases_ok,
              f"14 cases; {events} events; {forward} forward and {inverse} inverse operations")

        queue = delivery["nextPendingGroup"]
        check("next identity and remaining work are explicit",
              queue == {"group": "rank9-ward-control6", "nextIdentity": "nullification-wave",
                       "blockerIds": ["WC188-B01"], "thenIdentity": "reality-anchor",
                       "thenBlockerIds": ["WC188-B02"]}
              and decision["closureTasksRemaining"] == 26
              and decision["firstReviewTasksRemaining"] == 0,
              "Nullification Wave / WC188-B01, then Reality Anchor / WC188-B02")
        check("prior holds are recorded as separate and unchanged",
              decision["separatePriorHolds"] == {
                  "final-word": ["DR217-B01"],
                  "elemental-shell": ["DF218-B01", "DF218-B02"],
                  "timeless-form": ["DF218-B03"]},
              "Final Word, Elemental Shell and Timeless Form remain held")

    failures = [r for r in results if not r["passed"]]
    report = {
        "id": "INVULNERABLE-SPHERE-RETURN310-INDEPENDENT-AUDIT",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(results), "passedChecks": len(results) - len(failures),
        "failedChecks": len(failures), "checks": results,
        "returnArchive": {"path": RETURN_ZIP.relative_to(ROOT).as_posix(), **digest(return_raw)},
        "deliveryPath": RETURN_DELIVERY.relative_to(ROOT).as_posix(),
        "submittedPacketSHA256": packet_sha,
        "interpretiveLimit": "This audit verifies package bindings, exact preservation, current source bytes, decision scope and the Director-supplied validation stream. It does not supply the missing planar-crossing witness or independently certify the semantics of a fictional encounter.",
    }
    out = A / "INVULNERABLE_SPHERE_RETURN310_INDEPENDENT_AUDIT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checkCount": report["checkCount"],
                      "failedChecks": report["failedChecks"],
                      "failures": [r for r in failures]}, indent=2))
    if failures:
        raise SystemExit("Return310 independent audit failed")


if __name__ == "__main__":
    main()
