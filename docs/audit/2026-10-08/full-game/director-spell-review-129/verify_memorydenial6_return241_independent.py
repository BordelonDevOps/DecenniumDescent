from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RET_DIR = BASE / "rank9_memorydenial6_return241_received"
RET_ZIP = RET_DIR / "DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip"
RET_DELIVERY = RET_DIR / "DD_Rank9_MemoryDenial2_Director_Return241_HELD_DELIVERY.json"
PACKET_DIR = BASE / "rank9_memorydenial6_current_source_241_prepared"
PACKET_ZIP = PACKET_DIR / "DD_Rank9_MemoryDenial6_CurrentSource_241.zip"
PACKET_DELIVERY = PACKET_DIR / "DD_Rank9_MemoryDenial6_CurrentSource_241_DELIVERY.json"
PACKET_AUDIT = BASE / "RANK9MEMORYDENIAL6_PACKET241_INDEPENDENT_AUDIT.json"
PACKET_RECEIPT = BASE / "RANK9MEMORYDENIAL6_PACKET241_RECEIPT.json"
PACKET_PREP = BASE / "RANK9MEMORYDENIAL6_SOURCE_PREPARATION_241.json"
RETURN224_ZIP = BASE / "rank9_memorydenial6_return224_received/DD_Rank9_MemoryDenial2_Director_Return224.zip"
RETURN224_RECEIPT = BASE / "RANK9_MEMORYDENIAL6_RETURN224_RECEIPT.json"
REPORT = BASE / "RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json"
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
IDS = ["mind-collapse", "unravel-identity"]
BLOCKERS = {"mind-collapse": ["MD196-B01"], "unravel-identity": ["MD196-B02"]}
QUALS = {"mind-collapse": ["MD196-H01", "MD196-H02", "MD196-H03", "MD196-H04", "MD196-H06", "MD196-H08"],
         "unravel-identity": ["MD196-H01", "MD196-H02", "MD196-H03", "MD196-H06", "MD196-H08"]}
NEXT = {"group": "rank9-knowledge-revelation5", "pendingIds": ["faction-omniscience-supreme"], "count": 1}


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


def readj(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def canon_sha(value) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8"))


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts)


def main() -> None:
    checks = []
    def ck(name: str, ok: bool, detail=None):
        checks.append({"id": name, "passed": bool(ok), "details": detail})
        if not ok:
            raise AssertionError(f"{name}: {detail}")

    d = json.loads(RET_DELIVERY.read_text(encoding="utf-8-sig"))
    pd = json.loads(PACKET_DELIVERY.read_text(encoding="utf-8-sig"))
    prep = json.loads(PACKET_PREP.read_text(encoding="utf-8-sig"))
    packet_audit = json.loads(PACKET_AUDIT.read_text(encoding="utf-8-sig"))
    packet_receipt = json.loads(PACKET_RECEIPT.read_text(encoding="utf-8-sig"))
    rb = file_binding(RET_ZIP)
    ck("downloaded Return241 matches delivery size, SHA-256 and CRC32",
       rb == {k: d["archive"][k] for k in ("bytes", "sha256", "crc32")}, rb)
    ck("downloaded source Packet241 matches its delivery and passing independent receipt",
       file_binding(PACKET_ZIP)["sha256"] == pd["archive"]["sha256"] == prep["packet"]["sha256"] and
       packet_audit["status"] == packet_receipt["status"] == "PASS" and packet_audit["checksFailed"] == 0,
       {"packet": file_binding(PACKET_ZIP), "audit": packet_audit["status"], "checks": packet_audit["checkCount"]})

    with zipfile.ZipFile(RET_ZIP) as ret, zipfile.ZipFile(PACKET_ZIP) as packet:
        names = ret.namelist()
        outer = {row["path"]: row for row in d["members"]}
        manifest = readj(ret.read("MEMBER_MANIFEST.json"))
        inner = {row["path"]: row for row in manifest["members"]}
        member_bad = []
        for name in names:
            actual = member_binding(ret, name)
            expected = outer.get(name)
            if expected is None or actual != {k: expected[k] for k in ("bytes", "sha256", "crc32")}:
                member_bad.append(name)
            if name != "MEMBER_MANIFEST.json":
                expected_i = inner.get(name)
                if expected_i is None or actual != {k: expected_i[k] for k in ("bytes", "sha256", "crc32")}:
                    member_bad.append("inner:" + name)
        ck("Return241 ZIP is CRC-clean, unique, safe, and every member matches both manifests",
           ret.testzip() is None and len(names) == len(set(names)) == 58 and all(safe(n) for n in names) and
           set(names) == set(outer) and set(names) - {"MEMBER_MANIFEST.json"} == set(inner) and
           manifest["payloadMemberCount"] == 57 and not member_bad,
           {"members": len(names), "payload": len(inner), "failures": member_bad[:12]})

        decision = readj(ret.read("DIRECTOR_DECISION.json"))
        decisions = {x["id"]: x for x in decision["decisions"]}
        ck("sealed ruling holds exactly the two requested identities without acceptance or application",
           decision["authorityBaseline"] == AUTH and decision["scope"] == IDS and
           decision["accepted"] is False and decision["applied"] is False and
           decision["acceptedIds"] == decision["appliedIds"] == [] and decision["heldIds"] == IDS and
           set(decisions) == set(IDS) and all(not x["accepted"] and not x["applied"] for x in decisions.values()),
           {"authority": decision["authorityBaseline"], "accepted": decision["accepted"], "held": decision["heldIds"]})
        ck("exact blockers and conditional qualifications are retained for each held identity",
           all(decisions[i]["blockerIds"] == BLOCKERS[i] and decisions[i]["conditionalQualificationIds"] == QUALS[i]
               and decisions[i]["holdIds"] == BLOCKERS[i] + [q for q in QUALS[i] if q not in BLOCKERS[i]]
               for i in IDS),
           {i: {"blockers": decisions[i]["blockerIds"], "qualifications": decisions[i]["conditionalQualificationIds"]} for i in IDS})
        ck("GPT selected the exact next one-spell Knowledge/Revelation5 group",
           decision["nextPendingGroup"] == {k: NEXT[k] for k in ("group", "pendingIds")} and
           d["nextPendingGroup"] == {k: NEXT[k] for k in ("group", "pendingIds")},
           {"decision": decision["nextPendingGroup"], "delivery": d["nextPendingGroup"]})

        source_binding = readj(ret.read("SOURCE_BINDING.json"))
        source_manifest = readj(packet.read("MANIFEST.json"))
        candidate = readj(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_241.json"))
        packet_rows = {x["path"]: x for x in source_manifest["members"]}
        source_errors = []
        current_rows = source_binding["currentSourceBindings"]
        for row in current_rows:
            name = row["path"]
            m = packet_rows.get(name)
            if m is None or member_binding(packet, name) != {k: row[k] for k in ("bytes", "sha256", "crc32")}:
                source_errors.append(name + ":packet")
                continue
            local = ROOT.joinpath(*PurePosixPath(name.removeprefix("sources_current/")).parts)
            if not local.is_file() or file_binding(local) != {k: row[k] for k in ("bytes", "sha256", "crc32")}:
                source_errors.append(name + ":workspace")
        ck("all 120 source bindings match Packet241 manifest and current workspace files",
           len(current_rows) == 120 and len(candidate["sourceBindings"]) == 120 and not source_errors,
           {"verified": len(current_rows) - len(source_errors), "errors": source_errors[:10]})
        overlay_rows = source_binding["workingTreeOverlayBindings"]
        overlay_errors = []
        for row in overlay_rows:
            name = row["path"]
            local = ROOT.joinpath(*PurePosixPath(name.removeprefix("current/")).parts)
            expected_overlay = {k: row[k] for k in ("bytes", "sha256")}
            if name not in packet_rows or any(member_binding(packet, name)[k] != v for k, v in expected_overlay.items()):
                overlay_errors.append(name + ":packet")
            elif not local.is_file() or any(file_binding(local)[k] != v for k, v in expected_overlay.items()):
                overlay_errors.append(name + ":workspace")
        ck("working-tree overlay captures match Packet241 and local bytes",
           bool(overlay_rows) and not overlay_errors, {"bindings": len(overlay_rows), "errors": overlay_errors[:10]})
        ck("Return241 is bound to Packet241 source authority and exact main commit",
           source_binding["sourceAuthority"] == AUTH and source_binding["sourceBranch"] == "main" and
           source_binding["sourceCommit"] == "197366eae0c786415de55a0e4739e83f49f1a65f" and
           source_binding["externalSourceArchive"]["sha256"] == pd["archive"]["sha256"] and
           decision["sourcePacket"]["sha256"] == pd["archive"]["sha256"],
           {"branch": source_binding["sourceBranch"], "commit": source_binding["sourceCommit"]})

        counts = decision["counts"]
        casebook = json.loads(gzip.decompress(ret.read("CASEBOOK.json.gz")))
        case_errors, events, fops, iops = [], 0, 0, 0
        status_counts: dict[str, int] = {}
        for case in casebook["cases"]:
            status_counts[case["status"]] = status_counts.get(case["status"], 0) + 1
            state = case["initialState"]
            if canon_sha(state) != case["initialSHA256"] or canon_sha(case["finalState"]) != case["finalSHA256"]:
                case_errors.append(case["id"] + ":state-hash")
                continue
            for event in case["events"]:
                events += 1
                before, after = event["before"], event["after"]
                forward, inverse = event["forward"], event["inverse"]
                fops += len(forward); iops += len(inverse)
                if (before != state or canon_sha(before) != event["beforeSHA256"] or canon_sha(after) != event["afterSHA256"]
                    or len(forward) != 2 or len(inverse) != 2
                    or forward[0] != {"op": "test", "path": "", "value": before}
                    or forward[1] != {"op": "replace", "path": "", "value": after}
                    or inverse[0] != {"op": "test", "path": "", "value": after}
                    or inverse[1] != {"op": "replace", "path": "", "value": before}):
                    case_errors.append(case["id"] + ":event-" + str(events))
                    break
                state = after
            if state != case["finalState"]:
                case_errors.append(case["id"] + ":final-state")
        ck("all 28 retained cases replay with exact state hashes and reversible operations",
           len(casebook["cases"]) == counts["cases"] == 28 and events == counts["events"] == 553 and
           fops == counts["forwardOperations"] == 1106 and iops == counts["inverseOperations"] == 1106 and not case_errors,
           {"cases": len(casebook["cases"]), "events": events, "forward": fops, "inverse": iops,
            "statuses": status_counts, "failures": case_errors[:10]})

        check_names = ["CLOCK_CHECK.json", "SOURCE_CHECK.json", "PRESERVATION_CHECK.json", "INTEGRITY_CHECK.json",
                       "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "COVERAGE_CHECK.json", "SOURCERECONCILIATION_CHECK.json"]
        totals, failures = 0, []
        check_summary = {}
        for name in check_names:
            obj = readj(ret.read(name)); totals += obj["checkCount"]
            bad = [x.get("id") for x in obj["checks"] if not x.get("pass", False)]
            if obj["failureCount"] != 0 or len(obj["checks"]) != obj["checkCount"] or bad:
                failures.append({"file": name, "reported": obj["failureCount"], "bad": bad[:5]})
            check_summary[name] = obj["checkCount"]
        ck("all six detailed validation ledgers pass and reconcile to the 17,045 reported checks",
           totals == counts["totalFreshChecksBeforePackaging"] == 17045 and not failures,
           {"checks": totals, "byLedger": check_summary, "failures": failures})
        package = d["packageValidation"]
        ck("delivery package validation reports all 178 checks passed",
           package["checkCount"] == 178 and package["failureCount"] == 0,
           package)

        # Compare the carried forward prior holds with the locally audited Return224/238/239/240 records.
        prior224 = readj(RETURN224_RECEIPT.read_bytes())
        ck("Return224 held decision is locally present and was independently audited",
           prior224["status"] == "PASS" and prior224["heldIds"] == IDS and prior224["acceptedIds"] == [] and
           source_binding["priorReturn224Archive"]["sha256"] == file_binding(RETURN224_ZIP)["sha256"],
           {"status": prior224["status"], "held": prior224["heldIds"]})

    now = datetime.now(timezone.utc).isoformat()
    report = {"id": "RANK9-MEMORYDENIAL6-RETURN241-INDEPENDENT-AUDIT", "recordedAtUtc": now,
              "status": "PASS" if all(x["passed"] for x in checks) else "FAIL",
              "archive": {"path": RET_ZIP.relative_to(ROOT).as_posix(), **rb},
              "deliveryManifest": {"path": RET_DELIVERY.relative_to(ROOT).as_posix(), **file_binding(RET_DELIVERY)},
              "sourcePacket": {"path": PACKET_ZIP.relative_to(ROOT).as_posix(), **file_binding(PACKET_ZIP)},
              "sourceAuthority": AUTH, "group": "rank9-memory-denial6", "targetIds": IDS,
              "acceptedIds": [], "appliedIds": [], "heldIds": IDS,
              "blockers": BLOCKERS, "conditionalQualifications": QUALS,
              "nextPendingGroup": NEXT, "currentSourceBindingsVerified": 120,
              "caseCount": 28, "events": 553, "forwardOperations": 1106, "inverseOperations": 1106,
              "checkCount": len(checks), "checksPassed": sum(x["passed"] for x in checks),
              "checksFailed": sum(not x["passed"] for x in checks), "checks": checks,
              "scopeLimitation": "Verifies sealed package integrity, exact source bindings, decision metadata, retained case replay and validation ledgers; it does not independently adjudicate game-rule semantics."}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-MEMORYDENIAL6-RETURN241-RECEIPT", "status": report["status"],
              "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
              "sourcePacket": report["sourcePacket"],
              "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **file_binding(REPORT)},
              "checkCount": report["checkCount"], "checksPassed": report["checksPassed"],
              "checksFailed": report["checksFailed"], "acceptedIds": [], "appliedIds": [],
              "heldIds": IDS, "blockers": BLOCKERS, "nextPendingGroup": NEXT}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": report["checkCount"],
                      "passed": report["checksPassed"], "failed": report["checksFailed"],
                      "held": IDS, "next": NEXT}, indent=2))


if __name__ == "__main__":
    main()
