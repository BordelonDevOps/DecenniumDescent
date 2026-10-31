from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_planargates5_return243_received"
ARCHIVE = RECEIVED / "DD_Rank9_PlanarGates2_Director_Return243_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_PlanarGates2_Director_Return243_HELD_DELIVERY.json"
SOURCE_DIR = AUDIT / "rank9_planargates5_current_source_243_prepared"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_243.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_243_DELIVERY.json"
PRIOR226 = AUDIT / "rank9_planargates5_return226_received/DD_Rank9_PlanarGates2_Director_Return226.zip"
PRIOR200 = AUDIT / "rank9_planargates5_return200_received/DD_Rank9_PlanarGates5_Director_Return200.zip"
REPORT = AUDIT / "RANK9_PLANARGATES5_RETURN243_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9_PLANARGATES5_RETURN243_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = {"banishment-gate", "conjure-demiplane-fortress"}
BLOCKERS = {"banishment-gate": ["PG200-B03", "PG200-B04"],
            "conjure-demiplane-fortress": ["PG200-B06"]}
QUALIFICATIONS = {f"PG200-H{i:02d}" for i in range(1, 11)}
NEXT = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]


def digest(path: Path) -> tuple[int, str, str]:
    h = hashlib.sha256(); c = 0; n = 0
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b); c = zlib.crc32(b, c); n += len(b)
    return n, h.hexdigest(), f"{c & 0xffffffff:08x}"


def member_digest(z: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h = hashlib.sha256(); c = 0; n = 0
    with z.open(name) as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b); c = zlib.crc32(b, c); n += len(b)
    return n, h.hexdigest(), f"{c & 0xffffffff:08x}"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def zip_json(z: zipfile.ZipFile, name: str):
    return json.loads(z.read(name).decode("utf-8-sig"))


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not name.startswith(("/", "\\")) and "\\" not in name and not p.is_absolute() and ".." not in p.parts


def main() -> None:
    d = read_json(DELIVERY)
    checks: list[dict] = []

    def record(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    zsize, zsha, zcrc = digest(ARCHIVE)
    dsize, dsha, dcrc = digest(DELIVERY)
    src_size, src_sha, src_crc = digest(SOURCE_ARCHIVE)
    src_manifest = read_json(SOURCE_DELIVERY)
    record("Downloaded Return243 archive matches sealed byte, SHA-256, and CRC32 binding",
        (zsize, zsha, zcrc) == (1_050_027, "e900c849f0fe54b55f363d247966f7125aac77355b06d5591fcd723ee6c49ded", "80704286")
        and (zsize, zsha, zcrc) == (d["archive"]["bytes"], d["archive"]["sha256"], d["archive"]["crc32"].lower()),
        {"bytes": zsize, "sha256": zsha, "crc32": zcrc})
    record("Matching delivery manifest is byte-bound and identifies the submitted Packet243",
        dsize == 43_254 and dsha == "00525c0c6c89edcbfd7fa2111c6d8716cd79e97469713b0178ab729c986eebc8"
        and (src_size, src_sha, src_crc) == (d["sourcePacket"]["bytes"], d["sourcePacket"]["sha256"], d["sourcePacket"]["crc32"].lower())
        and src_manifest["archive"]["sha256"] == src_sha,
        {"deliveryBytes": dsize, "deliverySHA256": dsha, "sourcePacketSHA256": src_sha})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist(); name_set = set(names)
        safe_names = all(safe(n) for n in names)
        outer_rows = {x["path"]: x for x in d["members"]}
        record("ZIP has 73 unique safe members and the exact delivery allowlist",
            z.testzip() is None and len(names) == len(name_set) == d["memberCount"] == 73
            and d["payloadMemberCount"] == 72 and len(outer_rows) == 73
            and name_set == set(outer_rows) and safe_names,
            {"memberCount": len(names), "deliveryRows": len(outer_rows), "safeNames": safe_names})
        bad_outer = []
        for n, row in outer_rows.items():
            got = member_digest(z, n)
            if got != (row["bytes"], row["sha256"], row["crc32"].lower()):
                bad_outer.append(n)
        record("Every payload member independently matches delivery byte/SHA/CRC values", not bad_outer,
            {"checked": len(outer_rows), "failures": bad_outer[:8]})

        internal = zip_json(z, "MEMBER_MANIFEST.json")
        inner_rows = {x["path"]: x for x in internal["members"]}
        outer_payload = {n: row for n, row in outer_rows.items() if n != "MEMBER_MANIFEST.json"}
        bad_inner = [n for n in inner_rows if n not in outer_payload or any(
            inner_rows[n][k] != outer_payload[n][k] for k in ("bytes", "sha256")
        ) or inner_rows[n]["crc32"].lower() != outer_rows[n]["crc32"].lower()]
        record("Internal manifest and self-binding reconcile all 72 payload files",
            internal["id"] == "RETURN243-MEMBER-MANIFEST" and internal["payloadMemberCount"] == 72
            and set(inner_rows) == set(outer_payload) and not bad_inner
            and internal["sourcePacket"]["sha256"] == src_sha
            and internal["authority"] == AUTHORITY,
            {"innerRows": len(inner_rows), "mismatches": bad_inner[:8]})

        decision = zip_json(z, "DIRECTOR_DECISION.json")
        exact_holds = (decision["scope"] == ["banishment-gate", "conjure-demiplane-fortress"]
            and set(decision["heldIds"]) == TARGETS and decision["accepted"] is False and decision["applied"] is False
            and decision["acceptedIds"] == decision["appliedIds"] == [] and decision["authority"] == AUTHORITY
            and d["authority"] == AUTHORITY and d["accepted"] is False and d["applied"] is False
            and d["acceptedIds"] == d["appliedIds"] == [] and set(d["heldIds"]) == TARGETS)
        decisions = {x["id"]: x for x in decision["decisions"]}
        delivery_blockers = {k: v for k, v in d["blockerIds"].items()}
        exact_per_spell = (set(decisions) == TARGETS and delivery_blockers == BLOCKERS and all(
            decisions[s]["accepted"] is False and decisions[s]["applied"] is False and decisions[s]["held"] is True
            and decisions[s]["blockerIds"] == BLOCKERS[s]
            and set(decisions[s]["conditionalQualificationIds"]) == QUALIFICATIONS
            and decisions[s]["procedure"] == f"procedures/{s}.json"
            for s in TARGETS))
        record("Director ruling and delivery hold exactly the two scoped spells at authority 811/37/0",
            exact_holds and exact_per_spell,
            {"heldIds": decision["heldIds"], "blockerIds": delivery_blockers, "authority": decision["authority"]})
        record("All three exact blockers remain open with concrete source-qualified missing witnesses",
            {x["id"] for x in decision["blockers"]} == {"PG200-B03", "PG200-B04", "PG200-B06"}
            and all(x["status"] == "OPEN" and x["blocking"] is True and x["minimumMissingWitness"] for x in decision["blockers"])
            and all(set(BLOCKERS[s]) == set(decisions[s]["blockerIds"]) for s in TARGETS),
            {x["id"]: x["minimumMissingWitness"] for x in decision["blockers"]})

        lead = zip_json(z, "SOURCE_LEAD_FACTION_ENVOY.json")
        reconciliation = zip_json(z, "SOURCE_RECONCILIATION.json")["FactionEnvoy"]
        record("Faction Envoy Humanoid lead is bound without claiming acquisition or invocation permission",
            lead["profileUnchanged"]["type"].startswith("Humanoid")
            and lead["profileUnchanged"]["status"].startswith("NEW summon-only")
            and "mechanical targeting" in lead["profileUnchanged"]["type"]
            and "membership" in lead["remaining"].lower() and "invocation permission" in lead["remaining"].lower(),
            {"profileType": lead["profileUnchanged"]["type"], "profileStatus": lead["profileUnchanged"]["status"],
             "remaining": lead["remaining"]})

        source_rows = zip_json(z, "SOURCE_BINDINGS.json")["rows"]
        with zipfile.ZipFile(SOURCE_ARCHIVE) as source_zip:
            candidate = zip_json(source_zip, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_243.json")
        candidate_rows = {x["path"]: x for x in candidate["sourceBindings"]}
        source_mismatches = []
        for row in source_rows:
            source_path = row["sourcePath"]
            expected = candidate_rows.get(source_path)
            if not expected or any(row[k] != expected[k] for k in ("bytes", "sha256", "gitBlobSHA1")):
                source_mismatches.append(source_path)
        record("All 161 return source bindings reconcile to the independently audited Packet243 candidate",
            len(source_rows) == len(candidate_rows) == 161 and not source_mismatches,
            {"returnRows": len(source_rows), "candidateRows": len(candidate_rows), "mismatches": source_mismatches[:10]})

        replay = zip_json(z, "CASE_REPLAY.json"); counts = zip_json(z, "COUNTS.json")
        replay_cases = replay["cases"]
        event_count = sum(len(c["events"]) for c in replay_cases)
        case_failures = []
        for case in replay_cases:
            events = case["events"]
            valid = (bool(events) and len(events) == len(case["events"])
                and events[0]["beforeSHA256"] == case["initialSHA256"]
                and events[-1]["afterSHA256"] == case["finalSHA256"]
                and all(a["afterSHA256"] == b["beforeSHA256"] for a, b in zip(events, events[1:]))
                and all(e["replay"] == "PASS" and len(e["beforeSHA256"]) == len(e["afterSHA256"]) == 64 for e in events)
                and case["statusUnchanged"].startswith("HELD_"))
            got = member_digest(z, case["file"]["path"])
            valid = valid and got == (case["file"]["bytes"], case["file"]["sha256"], case["file"]["crc32"].lower())
            if not valid:
                case_failures.append(case["id"])
        record("All 23 cases and their 267 state-hash event chains replay and bind to exact case bytes",
            len(replay_cases) == counts["cases"] == 23 and event_count == counts["events"] == 267
            and counts["forwardEventOperations"] == counts["inverseEventOperations"] == 534
            and counts["proposalOperations"] == 8 and counts["acceptedIds"] == counts["appliedIds"] == 0
            and not case_failures,
            {"cases": len(replay_cases), "events": event_count, "forward": counts["forwardEventOperations"],
             "inverse": counts["inverseEventOperations"], "proposalOperations": counts["proposalOperations"],
             "caseFailures": case_failures[:10]})

        case_names = [n for n in names if n.startswith("cases/") and n.endswith(".json")]
        with zipfile.ZipFile(PRIOR226) as z226:
            prior_case_names = [n for n in z226.namelist() if n.startswith("cases/") and n.endswith(".json")]
            unchanged_cases = len(case_names) == len(prior_case_names) == 23 and all(
                n in z226.namelist() and z.read(n) == z226.read(n) for n in case_names)
        record("All 23 case files remain byte-exact with the prior sealed Return226 evidence",
            unchanged_cases, {"currentCases": len(case_names), "priorCases": len(prior_case_names)})

        dispositions = zip_json(z, "CASE_DISPOSITIONS.json")["cases"]
        disposition_ok = len(dispositions) == 23 and all(
            x["demonstrated"] is False and set(x["holdIds"]) >= QUALIFICATIONS
            and set(x["holdIds"]) & set(BLOCKERS[x["spellId"]])
            for x in dispositions)
        record("All 23 case dispositions retain PG200-H01 through H10 and their spell-specific blocker",
            disposition_ok, {"dispositions": len(dispositions)})

        validation = zip_json(z, "VALIDATION.json")
        validation_checks = zip_json(z, "VALIDATION_CHECKS.json")
        package = d["packageValidation"]
        all_package_pass = package["status"] == "PASS" and package["checkCount"] == 223
        all_package_pass = all_package_pass and package["failureCount"] == 0 and all(x["pass"] is True for x in package["checks"])
        record("Sealed validation reports 10,983 checks and all 223 package checks pass",
            validation["status"] == "DATA_PASS_REQUIRED_WITNESSES_HELD" and not validation["failures"]
            and counts["totalFreshChecksBeforePackaging"] == 10_983
            and sum(len(v) for v in validation_checks.values()) == 10_983 and all(x.get("pass") is True for v in validation_checks.values() for x in v)
            and all_package_pass,
            {"freshChecks": counts["totalFreshChecksBeforePackaging"], "packageChecks": package["checkCount"],
             "packageFailures": package["failureCount"]})

        questions = zip_json(z, "ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json")
        future = zip_json(z, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        record("The package retains 30 original questions, two addenda, and all nine future obligations",
            counts["originalQuestionsPreserved"] == 30 and counts["focusedAddendaPreserved"] == 2
            and counts["futureObligationsPreserved"] == 9 and len(questions["questions"]) == 30
            and len(questions["addenda"]) == 2 and len(questions["futureObligations"]) == 9
            and len(future["obligations"]) == 6,
            {"questions": counts["originalQuestionsPreserved"], "addenda": counts["focusedAddendaPreserved"],
             "futureObligations": len(questions["futureObligations"]), "targetFutureDispositions": len(future["obligations"])})

        old_apply = zip_json(z, "context/PLANARGATES5_RETURN200_APPLICATION.json")
        old_decision = zip_json(z, "prior200/DIRECTOR_DECISION.json")
        old_external = zip_json(z, "EXTERNAL_ARCHIVE_BINDINGS.json")["priorReturn200"]
        psize, psha, pcrc = digest(PRIOR200)
        record("Return200 applied gate identities are preserved against their archived source bytes",
            old_apply["acceptedIds"] == ["gate", "absolute-gate", "planar-sanctuary"]
            and old_decision["acceptedIds"] == old_apply["acceptedIds"]
            and old_apply["status"] == "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS"
            and old_decision["applied"] is False
            and (psize, psha, pcrc) == (old_external["bytes"], old_external["sha256"], old_external["crc32"].lower()),
            {"acceptedAppliedIds": old_apply["acceptedIds"], "priorArchiveSHA256": psha})

        context242 = zip_json(z, "context/RETURN242_DIRECTOR_DECISION.json")
        record("Return242 Knowledge/Revelation hold remains unchanged outside this review",
            context242["heldIds"] == ["faction-omniscience-supreme"]
            and context242["blockerIds"] == ["KR198-B01"]
            and decision["nextPendingGroup"] == {"group": "rank9-summon-hosts5", "pendingIds": NEXT},
            {"heldIds": context242["heldIds"], "next": decision["nextPendingGroup"]})

        record("Planar candidate procedures are limited to the two pending identities",
            set(x["id"] for x in decision["decisions"]) == TARGETS
            and all(f"procedures/{s}.json" in name_set for s in TARGETS)
            and not any(n.startswith("procedures/") and n.split("/")[-1][:-5] not in TARGETS for n in names),
            {"procedures": [n for n in names if n.startswith("procedures/")]})

    failures = [c for c in checks if not c["passed"]]
    report = {"id": "RANK9-PLANARGATES5-RETURN243-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL", "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures), "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(),
            "bytes": zsize, "sha256": zsha, "crc32": zcrc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": dsize,
            "sha256": dsha, "crc32": dcrc}, "sourcePacket": {"path": SOURCE_ARCHIVE.relative_to(ROOT).as_posix(),
            "bytes": src_size, "sha256": src_sha, "crc32": src_crc}, "authority": AUTHORITY,
        "heldIds": sorted(TARGETS), "blockerIds": BLOCKERS, "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-PLANARGATES5-RETURN243-RECEIPT", "status": report["status"],
        "auditReport": REPORT.name, "auditReportSHA256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        "archive": report["archive"], "delivery": report["delivery"], "sourcePacket": report["sourcePacket"],
        "authority": AUTHORITY, "heldIds": sorted(TARGETS), "blockerIds": BLOCKERS,
        "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"]}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
        "checksFailed": report["checksFailed"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
