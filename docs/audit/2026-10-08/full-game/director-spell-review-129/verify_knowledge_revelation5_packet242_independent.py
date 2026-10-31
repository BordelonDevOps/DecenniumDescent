from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET_DIR = AUDIT / "rank9_knowledgerevelation5_current_source_242_prepared"
SUP_DIR = AUDIT / "rank9_knowledgerevelation5_return198_witness_supplement_242"
PACKET = PACKET_DIR / "DD_Rank9_KnowledgeRevelation5_CurrentSource_242.zip"
PACKET_DELIVERY = PACKET_DIR / "DD_Rank9_KnowledgeRevelation5_CurrentSource_242_DELIVERY.json"
SUPPLEMENT = SUP_DIR / "DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_242.zip"
SUPPLEMENT_DELIVERY = SUP_DIR / "DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_242_DELIVERY.json"
PRIOR_RETURN = AUDIT / "rank9_knowledgerevelation5_return198_received/DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
REPORT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_PACKET_242_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_PACKET_242_RECEIPT.json"
IDS = ["faction-omniscience-supreme"]
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def state_sha(value: object) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))


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
    packet_delivery = json.loads(PACKET_DELIVERY.read_text(encoding="utf-8-sig"))
    supplement_delivery = json.loads(SUPPLEMENT_DELIVERY.read_text(encoding="utf-8-sig"))
    packet_raw, supplement_raw = PACKET.read_bytes(), SUPPLEMENT.read_bytes()
    checks = []

    def check(name: str, passed: bool, detail=None):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    pb = {"bytes": len(packet_raw), "sha256": sha(packet_raw), "crc32": crc(packet_raw)}
    sb = {"bytes": len(supplement_raw), "sha256": sha(supplement_raw), "crc32": crc(supplement_raw)}
    check("Packet and supplement archive byte/hash bindings match delivery", pb["bytes"] == packet_delivery["archive"]["bytes"]
          and pb["sha256"] == packet_delivery["archive"]["sha256"] and pb["crc32"] == packet_delivery["archive"]["crc32"]
          and sb["bytes"] == supplement_delivery["archive"]["bytes"] and sb["sha256"] == supplement_delivery["archive"]["sha256"],
          {"packet": pb, "supplement": sb})

    with zipfile.ZipFile(PACKET) as zp, zipfile.ZipFile(SUPPLEMENT) as zs, zipfile.ZipFile(PRIOR_RETURN) as zold:
        pn, sn = zp.namelist(), zs.namelist()
        check("ZIP CRCs pass and paths are unique and safe", zp.testzip() is None and zs.testzip() is None
              and len(pn) == len(set(pn)) and len(sn) == len(set(sn)) and all(safe(x) for x in pn + sn),
              {"packetMembers": len(pn), "supplementMembers": len(sn)})
        pm = json.loads(zp.read("MANIFEST.json")); sm = json.loads(zs.read("SUPPLEMENT_MANIFEST.json"))
        prow = {x["path"]: x for x in pm["members"]}; srow = {x["path"]: x for x in sm["members"]}
        pgood = set(pn) - {"MANIFEST.json"} == set(prow)
        sgood = set(sn) - {"SUPPLEMENT_MANIFEST.json"} == set(srow)
        for name, row in prow.items():
            pgood = pgood and binding(zp, name) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
        for name, row in srow.items():
            sgood = sgood and binding(zs, name) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
        check("All packet and supplement members match their internal byte/SHA/CRC manifests", pgood and sgood,
              {"packet": len(prow), "supplement": len(srow)})

        source_context = json.loads(zp.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_242.json"))
        current_context = json.loads(zp.read("CURRENT_CONTEXT_242.json"))
        index = json.loads(zp.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
        catalog = json.loads(zp.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
        pending = json.loads(zp.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_241.json"))
        entry = next(x for x in index["entries"] if x["id"] == IDS[0])
        card = next(x for x in catalog["spells"] if x["id"] == IDS[0])
        exact_target = (packet_delivery["sourceAuthority"] == AUTH and current_context["sourceAuthority"] == AUTH
                        and source_context["sourceAuthority"] == AUTH and packet_delivery["pendingIds"] == IDS
                        and source_context["scope"]["pendingIds"] == IDS and pending["pendingCount"] == 37
                        and IDS[0] in pending["pendingIds"] and entry["authoredStatus"] == "pending-authored-procedure"
                        and entry["sourceStatus"] == "blocked-pending-operational-review"
                        and source_context["currentIndexEntry"] == entry and source_context["currentCatalogCard"] == card)
        check("Packet covers exactly one still-pending identity at authority 811/37/0", exact_target,
              {"authority": AUTH, "pendingCount": pending["pendingCount"], "target": IDS[0], "indexStatus": entry["authoredStatus"]})

        carry_paths = [
            "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json", "RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json",
            "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json",
            "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip",
            "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json", "RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
            "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json",
            "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip",
            "RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json", "RANK9_CASTINGCOST5_RETURN240_RECEIPT.json",
            "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD_DELIVERY.json",
            "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip",
            "RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json", "RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json",
            "rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD_DELIVERY.json",
            "rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip",
        ]
        carry_errors = []
        for path in carry_paths:
            member = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/" + path
            local = AUDIT / path
            if member not in pn or not local.is_file() or zp.read(member) != local.read_bytes():
                carry_errors.append(path)
        carry_receipts = [
            json.loads(zp.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/" + p))
            for p in ["RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json", "RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
                      "RANK9_CASTINGCOST5_RETURN240_RECEIPT.json", "RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json"]
        ]
        carry_good = (all(x["status"] == "PASS" or x["status"].startswith("ALL_FOUR_HELD") or
                          x["status"].startswith("UNHOLY_ASCENDANCE_HELD") for x in carry_receipts)
                      and carry_receipts[-1]["heldIds"] == ["mind-collapse", "unravel-identity"]
                      and carry_receipts[-1]["blockers"] == {"mind-collapse": ["MD196-B01"], "unravel-identity": ["MD196-B02"]})
        check("Packets 238 through 241 and their audited decision records are carried byte-for-byte",
              not carry_errors and carry_good,
              {"records": len(carry_paths), "errors": carry_errors, "return241Held": carry_receipts[-1].get("heldIds")})

        source_rows = source_context["currentSourceBindings"]
        failures = []
        for row in source_rows:
            name = row["packetMember"]
            if name not in pn:
                failures.append({"path": row["path"], "reason": "missing"})
                continue
            raw = zp.read(name)
            blob_sha1 = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or blob_sha1 != row["gitBlobSHA1"]:
                failures.append({"path": row["path"], "reason": "binding mismatch"})
        check("All 126 refreshed source rows match packed bytes, SHA-256, and Git blob IDs", len(source_rows) == 126 and not failures,
              {"rows": len(source_rows), "failures": failures[:10]})

        case_meta = json.loads(zs.read("CASE_METADATA.json"))
        origins = json.loads(zs.read("ORIGINAL_MEMBER_BINDINGS.json"))["copiedMembers"]
        origin_rows = {x["destination"]: x for x in origins}
        case_paths = sorted(n for n in sn if n.startswith("cases/") and n.endswith(".json"))
        case_failures = []; event_count = forward = inverse = 0
        for path in case_paths:
            case_raw = zs.read(path); case = json.loads(case_raw)
            if path not in zold.namelist() or zold.read(path) != case_raw:
                case_failures.append({"path": path, "reason": "not exact prior member"}); continue
            o = origin_rows.get(path, {})
            if len(case_raw) != o.get("bytes") or sha(case_raw) != o.get("sha256") or crc(case_raw) != o.get("crc32"):
                case_failures.append({"path": path, "reason": "original member binding"}); continue
            passed, fops, iops, events = replay(case)
            event_count += events; forward += fops; inverse += iops
            if not passed:
                case_failures.append({"path": path, "reason": "replay"})
        procedure_path = f"procedures/{IDS[0]}.json"
        procedure_exact = (procedure_path in sn and zold.read(procedure_path) == zs.read(procedure_path)
                           and sha(zs.read(procedure_path)) == origin_rows[procedure_path]["sha256"])
        check("Prior procedure and all eight exact target cases are preserved and case traces replay", procedure_exact
              and len(case_paths) == 8 and not case_failures and event_count == case_meta["events"] == 140
              and forward == inverse == case_meta["forwardOperations"] == 280,
              {"procedureExact": procedure_exact, "cases": len(case_paths), "events": event_count,
               "forwardOperations": forward, "inverseOperations": inverse, "failures": case_failures[:10]})

        prior_decision = json.loads(zs.read("PRIOR_DIRECTOR_DECISION_CONTEXT.json"))
        check("KR198-B01 and its six qualification holds are preserved without reopening prior acceptances",
              prior_decision["targetBlocker"]["id"] == "KR198-B01"
              and prior_decision["targetHoldIds"] == ["KR198-B01", "KR198-H01", "KR198-H02", "KR198-H03", "KR198-H04", "KR198-H05", "KR198-H06"]
              and prior_decision["priorAcceptedIds"] == ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"]
              and prior_decision["targetDecision"]["accepted"] is False,
              {"targetHoldIds": prior_decision["targetHoldIds"], "priorAcceptedIds": prior_decision["priorAcceptedIds"]})

        sup_embedded = zp.read("CURRENT_RETURN198_TARGET_WITNESS_SUPPLEMENT_242.zip")
        check("Current packet embeds the same bound Return198 witness supplement", sha(sup_embedded) == sb["sha256"]
              and len(sup_embedded) == sb["bytes"], {"bytes": len(sup_embedded), "sha256": sha(sup_embedded)})

    failures = [x for x in checks if not x["passed"]]
    report = {"id": "RANK9-KNOWLEDGEREVELATION5-PACKET242-INDEPENDENT-AUDIT",
              "status": "PASS" if not failures else "FAIL", "checksPassed": len(checks) - len(failures),
              "checksFailed": len(failures), "packet": {"path": str(PACKET.relative_to(ROOT)), **pb},
              "delivery": {"path": str(PACKET_DELIVERY.relative_to(ROOT)), "sha256": sha(PACKET_DELIVERY.read_bytes())},
              "supplement": {"path": str(SUPPLEMENT.relative_to(ROOT)), **sb}, "authority": AUTH,
              "acceptedIds": [], "heldIds": IDS, "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-KNOWLEDGEREVELATION5-PACKET242-INDEPENDENT-RECEIPT", "status": report["status"],
               "auditReport": REPORT.name, "auditReportSHA256": sha(REPORT.read_bytes()),
               "packet": report["packet"], "delivery": report["delivery"], "supplement": report["supplement"],
               "authority": AUTH, "pendingIds": IDS, "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"]}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
