from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_knowledgerevelation5_return225_received"
ARCHIVE = RECEIVED / "DD_Rank9_KnowledgeRevelation1_Director_Return225.zip"
DELIVERY = RECEIVED / "DD_Rank9_KnowledgeRevelation1_Director_Return225_DELIVERY.json"
PACKET = AUDIT / "rank9_knowledgerevelation5_current_source_225_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_225.zip"
PACKET_DELIVERY = AUDIT / "rank9_knowledgerevelation5_current_source_225_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_225_DELIVERY.json"
SUPPLEMENT = AUDIT / "rank9_knowledgerevelation5_return198_witness_supplement_225/DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_225.zip"
SUPPLEMENT_DELIVERY = AUDIT / "rank9_knowledgerevelation5_return198_witness_supplement_225/DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_225_DELIVERY.json"
PRIOR_RETURN = AUDIT / "rank9_knowledgerevelation5_return198_received/DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
REPORT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN225_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN225_RECEIPT.json"
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
HELD = ["faction-omniscience-supreme"]
HOLD_IDS = ["KR198-B01", "KR198-H01", "KR198-H02", "KR198-H03", "KR198-H04", "KR198-H05", "KR198-H06"]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def state_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha(raw)


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name


def binding(zf: zipfile.ZipFile, name: str) -> dict:
    h = hashlib.sha256(); c = 0; n = 0
    with zf.open(name) as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            n += len(b); h.update(b); c = zlib.crc32(b, c)
    return {"bytes": n, "sha256": h.hexdigest(), "crc32": f"{c & 0xffffffff:08x}"}


def replay(case: dict) -> tuple[bool, int, int, int]:
    if state_sha(case["initialState"]) != case["initialSHA256"] or state_sha(case["finalState"]) != case["finalSHA256"]:
        return False, 0, 0, 0
    state = case["initialState"]; prior_time = float("-inf"); ftotal = itotal = 0
    for event in case["events"]:
        before, after = event["beforeState"], event["afterState"]
        fops, iops = event["forward"], event["inverse"]
        ftotal += len(fops); itotal += len(iops)
        t = after.get("time")
        if (before != state or state_sha(before) != event["beforeSHA256"] or state_sha(after) != event["afterSHA256"]
                or len(fops) != 2 or len(iops) != 2 or (isinstance(t, (int, float)) and t < prior_time)):
            return False, ftotal, itotal, len(case["events"])
        if isinstance(t, (int, float)):
            prior_time = t
        if not (fops[0] == {"op": "test", "path": "", "value": before}
                and fops[1] == {"op": "replace", "path": "", "value": after}
                and iops[0] == {"op": "test", "path": "", "value": after}
                and iops[1] == {"op": "replace", "path": "", "value": before}):
            return False, ftotal, itotal, len(case["events"])
        state = after
    return state == case["finalState"], ftotal, itotal, len(case["events"])


def main() -> None:
    d = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    pd = json.loads(PACKET_DELIVERY.read_text(encoding="utf-8-sig"))
    sd = json.loads(SUPPLEMENT_DELIVERY.read_text(encoding="utf-8-sig"))
    checks: list[dict] = []

    def check(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    raw = ARCHIVE.read_bytes(); archive_binding = {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}
    check("Return archive matches the director-stated byte/SHA/CRC binding",
          all(archive_binding[k] == d["archive"][k] for k in ("bytes", "sha256", "crc32")), archive_binding)
    check("Downloaded Return225 delivery JSON matches the browser-listed SHA and size",
          len(DELIVERY.read_bytes()) == 46253 and sha(DELIVERY.read_bytes()) == "c49ec3d3ce674bb968bb3047276785a4fed91c71d1f1a930329e4549f8b61dfb",
          {"bytes": len(DELIVERY.read_bytes()), "sha256": sha(DELIVERY.read_bytes())})
    check("Delivery and returned archive declare exact hold-only disposition and current authority",
          d["authorityBaseline"] == AUTH and d["accepted"] is False and d["applied"] is False
          and d["acceptedIds"] == [] and d["heldIds"] == HELD
          and d["decision"]["holdIds"] == HOLD_IDS and d["decision"]["blockerIds"] == ["KR198-B01"],
          {"authority": d["authorityBaseline"], "heldIds": d["heldIds"], "holdIds": d["decision"]["holdIds"]})
    check("Current source packet and target supplement are the exact locally prepared inputs",
          d["sourcePacket"]["bytes"] == len(PACKET.read_bytes()) and d["sourcePacket"]["sha256"] == sha(PACKET.read_bytes())
          and d["sourcePacket"]["crc32"] == crc(PACKET.read_bytes())
          and d["sourcePacket"]["delivery"]["bytes"] == len(PACKET_DELIVERY.read_bytes())
          and d["sourcePacket"]["delivery"]["sha256"] == sha(PACKET_DELIVERY.read_bytes())
          and d["targetSupplement"]["bytes"] == len(SUPPLEMENT.read_bytes())
          and d["targetSupplement"]["sha256"] == sha(SUPPLEMENT.read_bytes())
          and d["targetSupplement"]["crc32"] == crc(SUPPLEMENT.read_bytes())
          and d["targetSupplement"]["delivery"]["bytes"] == len(SUPPLEMENT_DELIVERY.read_bytes())
          and d["targetSupplement"]["delivery"]["sha256"] == sha(SUPPLEMENT_DELIVERY.read_bytes()),
          {"packet": d["sourcePacket"], "supplement": d["targetSupplement"]})

    with zipfile.ZipFile(ARCHIVE) as zr, zipfile.ZipFile(PACKET) as zp, zipfile.ZipFile(SUPPLEMENT) as zs, zipfile.ZipFile(PRIOR_RETURN) as zo:
        names = zr.namelist(); bad_paths = [n for n in names if not safe(n)]
        check("Return ZIP CRCs pass and its 51 unique member paths are safe", zr.testzip() is None
              and len(names) == len(set(names)) == d["memberCount"] == 51 and not bad_paths,
              {"memberCount": len(names), "badPaths": bad_paths})
        member_rows = {x["path"]: x for x in d["members"]}
        payload_ok = set(names) == set(member_rows) == set(d["allowlist"])
        member_failures = []
        if payload_ok:
            for name, row in member_rows.items():
                if binding(zr, name) != {k: row[k] for k in ("bytes", "sha256", "crc32")}:
                    member_failures.append(name)
        check("All return members exactly match delivery allowlist and byte/SHA/CRC bindings",
              payload_ok and not member_failures and d["payloadCountExcludingManifest"] == 50,
              {"deliveryMembers": len(member_rows), "archiveMembers": len(names), "failures": member_failures[:10]})
        mm = json.loads(zr.read("MEMBER_MANIFEST.json")); mm_rows = {x["path"]: x for x in mm["members"]}
        mm_ok = set(names) - {"MEMBER_MANIFEST.json"} == set(mm_rows) and mm["memberCountExcludingSelf"] == 50
        if mm_ok:
            for name, row in mm_rows.items():
                if binding(zr, name) != {k: row[k] for k in ("bytes", "sha256", "crc32")}:
                    mm_ok = False; break
        check("Internal member manifest independently validates all 50 payload members", mm_ok,
              {"manifestEntries": len(mm_rows), "externalArchives": mm.get("externalArchives", [])})

        decision = json.loads(zr.read("DIRECTOR_DECISION.json")); counts = json.loads(zr.read("COUNTS.json"))
        target_decisions = decision["decisions"]
        exact_decision = (decision["authorityBaseline"] == AUTH and decision["accepted"] is False and decision["applied"] is False
                          and decision["acceptedIds"] == [] and decision["heldIds"] == HELD
                          and len(target_decisions) == 1 and target_decisions[0]["id"] == HELD[0]
                          and target_decisions[0]["accepted"] is False and target_decisions[0]["applied"] is False
                          and target_decisions[0]["holdIds"] == HOLD_IDS
                          and len(decision["blockers"]) == 1 and decision["blockers"][0]["id"] == "KR198-B01"
                          and decision["blockers"][0]["status"] == "OPEN")
        check("Director decision holds exactly the one in-scope identity and retains KR198-B01/H01-H06", exact_decision,
              {"ids": decision["heldIds"], "blocker": decision["blockers"][0].get("id"), "counts": counts})
        check("Return authority and reviewed case/operation counts are internally consistent",
              counts["procedures"] == counts["held"] == 1 and counts["accepted"] == 0
              and counts["cases"] == 8 and counts["events"] == 140
              and counts["forwardEventOperations"] == counts["inverseEventOperations"] == 280
              and counts["eventOperations"] == 560 and counts["currentSourceBindings"] == 126
              and counts["freshAssertions"] == 6678 and counts["freshFailedAssertions"] == 0,
              counts)
        next_group = decision.get("nextPendingGroup", {})
        next_ok = next_group.get("group") == "rank9-planar-gates5" and set(next_group.get("pendingIds", [])) == {"banishment-gate", "conjure-demiplane-fortress"}
        check("Next pending group matches the director response", next_ok, next_group)

        source_bindings = json.loads(zr.read("SOURCE_BINDINGS.json"))
        rows = source_bindings["currentSourceBindings"]
        source_failures = []
        if len(rows) == 126:
            for row in rows:
                member = row["packetMember"]
                if member not in zp.namelist():
                    source_failures.append({"path": row["path"], "reason": "missing from bound source packet"})
                    continue
                content = zp.read(member)
                blob = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()
                if (len(content) != row["bytes"] or sha(content) != row["sha256"]
                        or blob != row["gitBlobSHA1"]):
                    source_failures.append({"path": row["path"], "reason": "source packet binding mismatch"})
        check("All 126 return source rows match the exact current packet and Git blob IDs",
              len(rows) == 126 and not source_failures,
              {"rows": len(rows), "failures": source_failures[:10]})

        replay_doc = json.loads(zr.read("CASE_REPLAY.json")); cases = replay_doc["cases"]
        case_failures = []; ev = fwd = inv = 0
        case_paths = sorted(n for n in names if n.startswith("cases/") and n.endswith(".json"))
        for path in case_paths:
            content = zr.read(path)
            if path not in zo.namelist() or zo.read(path) != content:
                case_failures.append({"path": path, "reason": "not byte-exact to Return198"}); continue
            case = json.loads(content); ok, fo, io, ec = replay(case)
            ev += ec; fwd += fo; inv += io
            if not ok:
                case_failures.append({"path": path, "reason": "round-trip replay failed"})
        procedure_path = "preserved/procedures/faction-omniscience-supreme.json"
        prior_procedure_path = "procedures/faction-omniscience-supreme.json"
        procedure_ok = procedure_path in names and prior_procedure_path in zo.namelist() and zr.read(procedure_path) == zo.read(prior_procedure_path)
        check("Original procedure and eight Return198 cases are byte-exact; all event operations independently replay",
              procedure_ok and len(case_paths) == 8 and len(cases) == 8 and not case_failures
              and ev == replay_doc["events"] == 140 and fwd == replay_doc["forwardOperations"] == 280
              and inv == replay_doc["inverseOperations"] == 280 and replay_doc["freshFailures"] == 0,
              {"procedureExact": procedure_ok, "caseFiles": len(case_paths), "replayRows": len(cases),
               "events": ev, "forward": fwd, "inverse": inv, "failures": case_failures[:10]})

        validations = json.loads(zr.read("VALIDATION_CHECKS.json"))
        package_checks = d["packageChecks"]
        checks_clean = (validations["checkCount"] == len(validations["checks"]) == 6678
                        and validations["failures"] == [] and all(x["passed"] for x in validations["checks"])
                        and package_checks["count"] == len(package_checks["checks"]) == 258
                        and package_checks["failed"] == 0 and all(x["passed"] for x in package_checks["checks"]))
        check("Embedded validation lists 6,678 passed assertions and package manifest lists 258 passed checks",
              checks_clean, {"validationChecks": validations["checkCount"], "packageChecks": package_checks["count"]})

        holds = json.loads(zr.read("HOLD_REGISTER.json"))
        current_blocker = holds["blocker"]
        blocker_ok = (current_blocker["id"] == "KR198-B01" and current_blocker["status"] == "OPEN"
                      and current_blocker["blocking"] is True
                      and current_blocker["minimumMissingWitness"]
                      and [x["id"] for x in holds["conditionalQualifications"]] == HOLD_IDS[1:])
        check("Retained blocker gives a concrete minimum missing witness and keeps all six conditional holds", blocker_ok,
              {"id": current_blocker.get("id"), "minimumMissingWitness": current_blocker.get("minimumMissingWitness"),
               "qualifications": holds.get("conditionalQualifications")})

    failures = [x for x in checks if not x["passed"]]
    report = {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN225-INDEPENDENT-AUDIT",
              "status": "PASS" if not failures else "FAIL", "checksPassed": len(checks) - len(failures),
              "checksFailed": len(failures), "archive": {"path": str(ARCHIVE.relative_to(ROOT)), **archive_binding},
              "delivery": {"path": str(DELIVERY.relative_to(ROOT)), "bytes": len(DELIVERY.read_bytes()),
                           "sha256": sha(DELIVERY.read_bytes())}, "authority": AUTH,
              "acceptedIds": [], "heldIds": HELD, "nextGroup": "rank9-planar-gates5", "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN225-INDEPENDENT-RECEIPT", "status": report["status"],
               "auditReport": REPORT.name, "auditReportSHA256": sha(REPORT.read_bytes()),
               "archive": report["archive"], "delivery": report["delivery"], "authority": AUTH,
               "acceptedIds": [], "heldIds": HELD, "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"]}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
