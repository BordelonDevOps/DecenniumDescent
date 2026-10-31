from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_knowledgerevelation5_return242_received"
ARCHIVE = RECEIVED / "DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD_DELIVERY.json"
PACKET = BASE / "rank9_knowledgerevelation5_current_source_242_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_242.zip"
PACKET_DELIVERY = BASE / "rank9_knowledgerevelation5_current_source_242_prepared/DD_Rank9_KnowledgeRevelation5_CurrentSource_242_DELIVERY.json"
SUPPLEMENT = BASE / "rank9_knowledgerevelation5_return198_witness_supplement_242/DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_242.zip"
SUPPLEMENT_DELIVERY = BASE / "rank9_knowledgerevelation5_return198_witness_supplement_242/DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_242_DELIVERY.json"
PRIOR = BASE / "rank9_knowledgerevelation5_return198_received/DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
REPORT = BASE / "RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_KNOWLEDGEREVELATION5_RETURN242_RECEIPT.json"
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
SPELL = "faction-omniscience-supreme"
HELD = [SPELL]
BLOCKERS = ["KR198-B01"]
QUALS = ["KR198-H01", "KR198-H02", "KR198-H03", "KR198-H04", "KR198-H05", "KR198-H06"]
HOLD_IDS = BLOCKERS + QUALS
NEXT = {"group": "rank9-planar-gates5", "pendingIds": ["banishment-gate", "conjure-demiplane-fortress"]}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def file_binding(path: Path) -> dict:
    h, c, n = hashlib.sha256(), 0, 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk); c = zlib.crc32(chunk, c); n += len(chunk)
    return {"bytes": n, "sha256": h.hexdigest(), "crc32": f"{c & 0xffffffff:08x}"}


def member_binding(zf: zipfile.ZipFile, name: str) -> dict:
    h, c, n = hashlib.sha256(), 0, 0
    with zf.open(name) as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk); c = zlib.crc32(chunk, c); n += len(chunk)
    return {"bytes": n, "sha256": h.hexdigest(), "crc32": f"{c & 0xffffffff:08x}"}


def state_sha(value: object) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8"))


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and ".." not in p.parts


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

    def ck(name: str, passed: bool, detail=None):
        checks.append({"id": name, "passed": bool(passed), "details": detail})
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    archive_info = file_binding(ARCHIVE)
    ck("Downloaded archive matches delivered bytes, SHA-256 and CRC32",
       archive_info == {k: d["archive"][k] for k in ("bytes", "sha256", "crc32")}, archive_info)
    packet_info, supplement_info = file_binding(PACKET), file_binding(SUPPLEMENT)
    ck("Exact submitted packet and witness supplement match their local delivery manifests",
       packet_info["sha256"] == pd["archive"]["sha256"] == d["sourcePacket"]["sha256"] and
       packet_info["bytes"] == pd["archive"]["bytes"] == d["sourcePacket"]["bytes"] and
       packet_info["crc32"] == pd["archive"]["crc32"] == d["sourcePacket"]["crc32"] and
       supplement_info["sha256"] == sd["archive"]["sha256"] and supplement_info["bytes"] == sd["archive"]["bytes"],
       {"sourcePacket": packet_info, "supplement": supplement_info})
    ck("Delivery records one held identity at authority 811/37/0 with exact blocker and qualifications",
       d["sourceAuthority"] == AUTH and d["accepted"] is False and d["applied"] is False and d["held"] is True and
       d["acceptedIds"] == d["appliedIds"] == [] and d["heldIds"] == HELD and
       d["blockerIds"] == BLOCKERS and d["conditionalQualificationIds"] == QUALS and
       d["nextPendingGroup"] == NEXT,
       {"authority": d["sourceAuthority"], "held": d["heldIds"], "blockers": d["blockerIds"], "next": d["nextPendingGroup"]})

    with zipfile.ZipFile(ARCHIVE) as zr, zipfile.ZipFile(PACKET) as zp, zipfile.ZipFile(SUPPLEMENT) as zs, zipfile.ZipFile(PRIOR) as zo:
        names = zr.namelist()
        outer = {x["path"]: x for x in d["members"]}
        mm = json.loads(zr.read("MEMBER_MANIFEST.json"))
        inner = {x["path"]: x for x in mm["members"]}
        failures = []
        for name in names:
            actual = member_binding(zr, name)
            if name not in outer or actual != {k: outer[name][k] for k in ("bytes", "sha256", "crc32")}:
                failures.append("outer:" + name)
            if name != "MEMBER_MANIFEST.json" and (name not in inner or actual != {k: inner[name][k] for k in ("bytes", "sha256", "crc32")}):
                failures.append("inner:" + name)
        ck("50-member ZIP has safe unique paths and every payload row matches outer and inner byte/SHA/CRC manifests",
           zr.testzip() is None and len(names) == len(set(names)) == d["memberCount"] == 50 and all(safe(x) for x in names) and
           set(names) == set(outer) and set(names) - {"MEMBER_MANIFEST.json"} == set(inner) and
           mm["payloadMembers"] == d["payloadMemberCount"] == len(inner) == 49 and not failures,
           {"members": len(names), "payload": len(inner), "failures": failures[:10]})
        ck("All 154 package checks passed",
           d["packageValidation"]["status"] == "PASS" and d["packageValidation"]["checkCount"] == 154 and
           d["packageValidation"]["failureCount"] == 0 and all(x.get("pass") is True for x in d["packageValidation"]["checks"]),
           {"count": d["packageValidation"]["checkCount"], "failures": d["packageValidation"]["failureCount"]})

        decision = json.loads(zr.read("DIRECTOR_DECISION.json"))
        decisions = decision["decisions"]
        ck("Sealed decision is held and unapplied, with KR198-B01 and H01-H06 retained",
           decision["authorityBaseline"] == AUTH and decision["scope"] == HELD and decision["accepted"] is False and
           decision["applied"] is False and decision["held"] is True and decision["acceptedIds"] == decision["appliedIds"] == [] and
           decision["heldIds"] == HELD and decision["blockerIds"] == BLOCKERS and decision["conditionalQualificationIds"] == QUALS and
           len(decisions) == 1 and decisions[0]["id"] == SPELL and decisions[0]["accepted"] is False and
           decisions[0]["applied"] is False and decisions[0]["blockerIds"] == BLOCKERS and
           decisions[0]["conditionalQualificationIds"] == QUALS and bool(decisions[0].get("minimumMissingWitness")),
           {"decision": decisions[0], "qualifications": decision["conditionalQualificationIds"]})
        ck("Decision explicitly reports no canonical change or supplied program execution",
           decision["canonicalChanged"] is False and decision["suppliedProgramsExecuted"] is False,
           {"canonicalChanged": decision["canonicalChanged"], "programsExecuted": decision["suppliedProgramsExecuted"]})
        ck("Director-selected next group is Planar Gates5 with the exact two identities",
           decision["nextPendingGroup"] == NEXT, decision["nextPendingGroup"])

        counts = d["counts"]
        ck("Delivery counts reconcile the one held spell, 126 sources, 8 cases and 4,567 passing checks",
           counts["procedures"] == counts["heldIds"] == 1 and counts["heldCases"] == 8 and
           counts["acceptedIds"] == counts["appliedIds"] == 0 and counts["sourceBindings"] == 126 and
           counts["cases"] == 8 and counts["mainCases"] == 2 and counts["branches"] == 6 and
           counts["events"] == 140 and counts["forwardOperations"] == counts["inverseOperations"] == 280 and
           counts["totalFreshChecksBeforePackaging"] == 4567 and counts["wholePositiveCasesComplete"] == 0,
           {k: counts[k] for k in ("procedures", "sourceBindings", "cases", "events", "forwardOperations", "inverseOperations", "totalFreshChecksBeforePackaging")})

        source_doc = json.loads(zr.read("SOURCE_BINDINGS.json"))
        source_rows = source_doc["sources"]
        source_manifest = json.loads(zp.read("MANIFEST.json"))
        manifest_rows = {x["path"]: x for x in source_manifest["members"]}
        source_errors = []
        for row in source_rows:
            name = row["path"]
            if name not in zp.namelist() or name not in manifest_rows:
                source_errors.append(name + ":missing")
                continue
            content = zp.read(name)
            blob = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()
            if (len(content) != row["bytes"] or sha(content) != row["sha256"] or blob != row["gitBlobSHA1"] or
                member_binding(zp, name) != {k: manifest_rows[name][k] for k in ("bytes", "sha256", "crc32")}):
                source_errors.append(name + ":binding")
        ck("All 126 source rows resolve to the submitted Packet242 bytes and Git blob IDs",
           len(source_rows) == 126 and source_doc["sourcePacket"]["sha256"] == packet_info["sha256"] and not source_errors,
           {"rows": len(source_rows), "errors": source_errors[:10]})

        ext = json.loads(zr.read("EXTERNAL_ARCHIVE_BINDINGS.json"))
        prior_info = file_binding(PRIOR)
        ck("Compact witness supplement and original Return198 archive are exactly bound",
           ext["sourcePacket"]["sha256"] == packet_info["sha256"] and
           ext["targetWitnessSupplement"]["sha256"] == supplement_info["sha256"] and
           ext["priorReturn198"]["sha256"] == prior_info["sha256"],
           {"supplement": ext["targetWitnessSupplement"], "priorReturn198": ext["priorReturn198"]})
        context_decisions = ["Return238_DIRECTOR_DECISION.json", "Return239_DIRECTOR_DECISION.json",
                             "Return240_DIRECTOR_DECISION.json", "Return241_DIRECTOR_DECISION.json"]
        carried_errors = []
        for n in context_decisions:
            ret_num = n[6:9]
            match = next((x for x in ext["contextArchives"] if str(x["return"]) == ret_num), None)
            path = "context/" + n
            if path not in names or match is None:
                carried_errors.append(n + ":missing")
                continue
            old_archive_path = ROOT / Path(*PurePosixPath(match["archive"]["path"].removeprefix("current/")).parts)
            if old_archive_path.is_file():
                with zipfile.ZipFile(old_archive_path) as prior_zip:
                    old_decision = prior_zip.read("DIRECTOR_DECISION.json")
                if json.loads(zr.read(path)) != json.loads(old_decision):
                    carried_errors.append(n + ":different")
        ck("Return238–241 sealed decisions are preserved with identical JSON values in the context records",
           len(context_decisions) == 4 and not carried_errors,
           {"records": context_decisions, "errors": carried_errors})

        replay_doc = json.loads(zr.read("CASE_REPLAY.json"))
        replay_rows = replay_doc["cases"]
        case_paths = sorted(n for n in names if n.startswith("cases/") and n.endswith(".json"))
        case_errors, event_count, fwd, inv = [], 0, 0, 0
        for path in case_paths:
            content = zr.read(path)
            if path not in zo.namelist() or zo.read(path) != content:
                case_errors.append(path + ":not-byte-exact-to-Return198")
                continue
            passed, f, i, e = replay(json.loads(content))
            event_count += e; fwd += f; inv += i
            if not passed:
                case_errors.append(path + ":replay")
        procedure = "procedures/faction-omniscience-supreme.json"
        procedure_ok = procedure in names and procedure in zo.namelist() and zr.read(procedure) == zo.read(procedure)
        ck("Original procedure and all eight Return198 cases are preserved byte-exactly and replay with reversible operations",
           procedure_ok and len(case_paths) == len(replay_rows) == 8 and not case_errors and
           event_count == 140 and fwd == inv == 280 and replay_doc["counts"]["events"] == 140 and
           replay_doc["counts"]["forwardOperations"] == replay_doc["counts"]["inverseOperations"] == 280,
           {"procedureExact": procedure_ok, "caseFiles": len(case_paths), "events": event_count,
            "forward": fwd, "inverse": inv, "errors": case_errors[:10]})

        validation = json.loads(zr.read("VALIDATION_CHECKS.json"))
        validation_rows = [row for rows in validation.values() for row in rows]
        validation_failures = [row["id"] for row in validation_rows if row.get("pass") is not True]
        ck("All eight detailed validation categories pass and sum to 4,567 fresh checks",
           len(validation_rows) == 4567 and not validation_failures,
           {"checks": len(validation_rows), "failures": validation_failures[:10]})
        hold_register = json.loads(zr.read("HOLD_REGISTER.json"))
        hold_record = next((x for x in hold_register["targetHoldRecords"] if x.get("id") == "KR198-B01"), {})
        ck("Held blocker has a concrete minimum missing witness and exact six linked qualifications",
           hold_register["targetHoldIds"] == HOLD_IDS and hold_record.get("originalRecordUnchanged", {}).get("status") == "OPEN" and
           bool(decisions[0]["minimumMissingWitness"]),
           {"holdIds": hold_register["targetHoldIds"], "minimumMissingWitness": decisions[0]["minimumMissingWitness"]})

    now = datetime.now(timezone.utc).isoformat()
    report = {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN242-INDEPENDENT-AUDIT", "recordedAtUtc": now,
              "status": "PASS" if all(x["passed"] for x in checks) else "FAIL",
              "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_info},
              "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **file_binding(DELIVERY)},
              "sourcePacket": {"path": PACKET.relative_to(ROOT).as_posix(), **packet_info},
              "authority": AUTH, "group": "rank9-knowledge-revelation5", "targetIds": HELD,
              "acceptedIds": [], "appliedIds": [], "heldIds": HELD, "blockers": BLOCKERS,
              "conditionalQualifications": QUALS, "nextGroup": NEXT,
              "sourceBindingsVerified": 126, "cases": 8, "events": 140,
              "forwardOperations": 280, "inverseOperations": 280,
              "checksPassed": sum(x["passed"] for x in checks), "checksFailed": sum(not x["passed"] for x in checks),
              "checkCount": len(checks), "checks": checks,
              "scopeLimitation": "Verifies sealed-package integrity, exact source and prior-case bindings, decision metadata, replay and validation ledgers; it does not independently adjudicate underlying game-rule semantics."}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-KNOWLEDGEREVELATION5-RETURN242-RECEIPT", "status": report["status"],
              "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
              "sourcePacket": report["sourcePacket"],
              "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **file_binding(REPORT)},
              "authority": AUTH, "acceptedIds": [], "appliedIds": [], "heldIds": HELD,
              "blockers": BLOCKERS, "conditionalQualifications": QUALS, "nextGroup": NEXT,
              "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"], "checkCount": report["checkCount"]}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": report["checkCount"],
                      "passed": report["checksPassed"], "failed": report["checksFailed"],
                      "heldIds": HELD, "nextGroup": NEXT}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
