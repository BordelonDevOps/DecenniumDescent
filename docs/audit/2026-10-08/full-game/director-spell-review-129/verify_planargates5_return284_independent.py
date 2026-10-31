from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_planargates5_return284_received"
ARCHIVE = RECEIVED / "DD_Rank9_PlanarGates5_Director_Return284_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json"
SOURCE_DIR = AUDIT / "rank9_planargates5_current_source_284_prepared"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_284.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_284_DELIVERY.json"
SOURCE_PACKET_AUDIT = AUDIT / "RANK9PLANARGATES5_PACKET_284_INDEPENDENT_AUDIT.json"
PRIOR243 = AUDIT / "rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD.zip"
PRIOR200 = AUDIT / "rank9_planargates5_return200_received/DD_Rank9_PlanarGates5_Director_Return200.zip"
REPORT = AUDIT / "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9_PLANARGATES5_RETURN284_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
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


def state_hash(state: dict) -> str:
    raw = json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


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
    record("Downloaded Return284 archive matches its sealed byte, SHA-256, and CRC32 binding",
        (zsize, zsha, zcrc) == (1_101_950, "32bd4aefadb49b5ccc6cfba306825f2d50c45a76b6bdeeebb63937b78fd53fd0", "ad1d121b")
        and (zsize, zsha, zcrc) == (d["archive"]["bytes"], d["archive"]["sha256"], d["archive"]["crc32"].lower()),
        {"bytes": zsize, "sha256": zsha, "crc32": zcrc})
    record("Delivery JSON and current-source archive match independent and attached bindings",
        dsize == 67_299 and dsha == "37785c25a536975a6fa4d3e81a57948b3605b2ccdd7b29a44fe2c57b2f24cd02"
        and dcrc == "fcb00d5f"
        and (src_size, src_sha, src_crc) == (d["sourcePacket"]["bytes"], d["sourcePacket"]["sha256"], d["sourcePacket"]["crc32"].lower())
        and src_manifest["archive"]["sha256"] == src_sha,
        {"deliveryBytes": dsize, "deliverySHA256": dsha, "sourcePacketSHA256": src_sha})

    source_packet_audit = read_json(SOURCE_PACKET_AUDIT)
    record("Packet284 source packet was independently audited before the Director submission",
        source_packet_audit.get("status") == "PASS" and source_packet_audit.get("checksFailed") == 0
        and source_packet_audit.get("archive", {}).get("sha256") == src_sha,
        {"status": source_packet_audit.get("status"), "checksPassed": source_packet_audit.get("checksPassed"),
         "checksFailed": source_packet_audit.get("checksFailed")})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist(); name_set = set(names)
        outer_rows = {x["path"]: x for x in d["members"]}
        record("Return284 has 83 unique safe members and the exact delivery allowlist",
            z.testzip() is None and len(names) == len(name_set) == d["archiveMemberCount"] == 83
            and d["payloadMemberCount"] == 82 and len(outer_rows) == 83
            and name_set == set(outer_rows) and all(safe(n) for n in names),
            {"archiveMembers": len(names), "deliveryRows": len(outer_rows), "safeNames": all(safe(n) for n in names)})
        bad_outer = [n for n, row in outer_rows.items()
            if member_digest(z, n) != (row["bytes"], row["sha256"], row["crc32"].lower())]
        record("Every Return284 member independently matches delivery byte/SHA/CRC values", not bad_outer,
            {"checked": len(outer_rows), "failures": bad_outer[:8]})

        internal = zip_json(z, "MEMBER_MANIFEST.json")
        inner_rows = {x["path"]: x for x in internal["members"]}
        outer_payload = {n: row for n, row in outer_rows.items() if n != "MEMBER_MANIFEST.json"}
        bad_inner = [n for n in inner_rows if n not in outer_payload or any(
            inner_rows[n][k] != outer_payload[n][k] for k in ("bytes", "sha256")
        ) or inner_rows[n]["crc32"].lower() != outer_payload[n]["crc32"].lower()]
        record("Internal self-excluding manifest and delivery reconcile all 82 payload members",
            internal["id"] == "RANK9-PLANARGATES5-DIRECTOR-RETURN284-MEMBER-MANIFEST"
            and internal["payloadMemberCount"] == 82 and set(inner_rows) == set(outer_payload) and not bad_inner
            and internal["sourcePacket"] == d["sourcePacket"] and internal["authority"] == AUTHORITY,
            {"manifestRows": len(inner_rows), "mismatches": bad_inner[:8]})

        decision = zip_json(z, "DIRECTOR_DECISION.json")
        exact_holds = (decision["scope"] == ["banishment-gate", "conjure-demiplane-fortress"]
            and set(decision["heldIds"]) == TARGETS and decision["accepted"] is False and decision["applied"] is False
            and decision["acceptedIds"] == decision["appliedIds"] == [] and decision["authority"] == AUTHORITY
            and d["authority"] == AUTHORITY and d["accepted"] is False and d["applied"] is False
            and d["acceptedIds"] == d["appliedIds"] == [] and set(d["heldIds"]) == TARGETS)
        decisions = {x["id"]: x for x in decision["decisions"]}
        exact_per_spell = (set(decisions) == TARGETS and d["blockerIds"] == BLOCKERS and all(
            decisions[s]["accepted"] is False and decisions[s]["applied"] is False and decisions[s]["held"] is True
            and decisions[s]["blockerIds"] == BLOCKERS[s]
            and set(decisions[s]["conditionalQualificationIds"]) == QUALIFICATIONS
            and decisions[s]["procedure"] == f"procedures/{s}.json"
            for s in TARGETS))
        record("Director holds exactly the two scoped spells at authority 816/32/0",
            exact_holds and exact_per_spell,
            {"heldIds": decision["heldIds"], "blockerIds": d["blockerIds"], "authority": decision["authority"]})
        blocker_rows = {x["id"]: x for x in decision["blockers"]}
        missing = {"PG200-B03", "PG200-B04", "PG200-B06"}
        record("Three concrete source-qualified blockers remain open, preserving all ten qualifications",
            set(blocker_rows) == missing and all(blocker_rows[b]["status"] == "OPEN" and blocker_rows[b]["blocking"] is True
                and bool(blocker_rows[b]["minimumMissingWitness"]) for b in missing)
            and all(set(decisions[s]["conditionalQualificationIds"]) == QUALIFICATIONS for s in TARGETS),
            {b: blocker_rows[b]["minimumMissingWitness"] for b in sorted(missing)})

        source_rows = zip_json(z, "SOURCE_BINDINGS.json")["rows"]
        with zipfile.ZipFile(SOURCE_ARCHIVE) as source_zip:
            candidate = zip_json(source_zip, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_284.json")
            candidate_rows = {x["path"]: x for x in candidate["sourceBindings"]}
            source_mismatches = []
            for row in source_rows:
                expected = candidate_rows.get(row["path"])
                if not expected or any(row[k] != expected[k] for k in ("bytes", "sha256", "gitBlobSHA1")):
                    source_mismatches.append({"path": row["path"], "reason": "binding mismatch"})
                    continue
                packet_member = row["packetMember"]
                raw = source_zip.read(packet_member)
                if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"] or git_blob(raw) != row["gitBlobSHA1"]:
                    source_mismatches.append({"path": row["path"], "reason": "embedded current source bytes mismatch"})
            packet_entries = source_zip.namelist()
            source_manifest = zip_json(source_zip, "MANIFEST.json")
            source_manifest_rows = {x["path"]: x for x in source_manifest["members"]}
            bad_packet_members = [n for n, row in source_manifest_rows.items()
                if n not in packet_entries or member_digest(source_zip, n) !=
                    (row["bytes"], row["sha256"], row["crc32"].lower())]
        record("All 175 live source bindings match the candidate and source bytes embedded in Packet284",
            len(source_rows) == len(candidate_rows) == 175 and not source_mismatches
            and candidate["currentAuthority"] == AUTHORITY
            and candidate["currentPendingGroup"].get("group") == "rank9-planar-gates5"
            and set(candidate["currentPendingGroup"].get("spellIds", [])) == TARGETS,
            {"returnRows": len(source_rows), "candidateRows": len(candidate_rows), "mismatches": source_mismatches[:8]})
        record("All 250 Packet284 archive members match its internal manifest",
            len(packet_entries) == 250 and source_manifest["memberCountExcludingSelf"] == 249
            and len(source_manifest_rows) == 249 and not bad_packet_members,
            {"archiveMembers": len(packet_entries), "manifestPayloadMembers": len(source_manifest_rows),
             "mismatches": bad_packet_members[:8]})

        replay = zip_json(z, "CASE_REPLAY.json")
        counts = zip_json(z, "COUNTS.json")
        case_summaries = replay["cases"]
        case_names = [n for n in names if n.startswith("cases/") and n.endswith(".json")]
        event_total = 0; state_hash_failures = []; event_shape_failures = []
        for name in case_names:
            case = zip_json(z, name)
            events = case["events"]
            event_total += len(events)
            try:
                chain_ok = (bool(events) and state_hash(case["initial"]) == case["initialSHA256"]
                    and state_hash(case["final"]) == case["finalSHA256"]
                    and events[0]["beforeSHA256"] == case["initialSHA256"]
                    and events[-1]["afterSHA256"] == case["finalSHA256"]
                    and all(state_hash(e["before"]) == e["beforeSHA256"] and state_hash(e["after"]) == e["afterSHA256"] for e in events)
                    and all(a["afterSHA256"] == b["beforeSHA256"] for a, b in zip(events, events[1:]))
                    and all(bool(e.get("forward")) and bool(e.get("inverse")) for e in events))
            except (KeyError, TypeError):
                chain_ok = False
            if not chain_ok:
                state_hash_failures.append(name)
            summary = next((c for c in case_summaries if c["caseId"] == case["id"]), None)
            if not summary or summary["events"] != len(events) or summary["initialSHA256"] != case["initialSHA256"] or summary["finalSHA256"] != case["finalSHA256"]:
                event_shape_failures.append(name)
        record("All 23 preserved case byte streams contain 267 canonical state-hash-verified events",
            len(case_names) == len(case_summaries) == counts["cases"] == 23
            and event_total == replay["events"] == counts["events"] == 267
            and replay["freshReplay"] is True and replay["noCasesModified"] is True
            and counts["forwardOperations"] == counts["inverseOperations"] == 534
            and counts["proposalOperations"] == 8 and not state_hash_failures and not event_shape_failures,
            {"cases": len(case_names), "events": event_total, "stateHashFailures": state_hash_failures[:8],
             "summaryFailures": event_shape_failures[:8]})
        with zipfile.ZipFile(PRIOR243) as prior:
            prior_case_names = [n for n in prior.namelist() if n.startswith("cases/") and n.endswith(".json")]
            unchanged = len(prior_case_names) == len(case_names) == 23 and all(
                n in prior.namelist() and z.read(n) == prior.read(n) for n in case_names)
        record("All 23 Return284 case files remain byte-exact with sealed Return243 evidence",
            unchanged, {"currentCases": len(case_names), "priorCases": len(prior_case_names)})
        dispositions = zip_json(z, "CASE_DISPOSITIONS.json")["cases"]
        record("All retained cases remain explicitly incomplete with relevant held blocker and qualifications",
            len(dispositions) == 23 and all(x["demonstrated"] is False
                and set(x["holdIds"]) >= QUALIFICATIONS and set(x["holdIds"]) & set(BLOCKERS[x["spellId"]])
                for x in dispositions), {"dispositions": len(dispositions)})

        validation = zip_json(z, "VALIDATION.json")
        validation_checks = zip_json(z, "VALIDATION_CHECKS.json")
        package = d["packageChecks"]
        record("Return284 reports 16,689 pre-seal checks without failures and all 419 seal checks pass",
            validation["status"] == "PASS_DATA_PRESERVATION_AND_REPLAY_WITH_SEMANTIC_HOLDS"
            and validation["failedChecks"] == [] and validation["semanticClosure"] is False
            and len(validation_checks) == 16_689 and all(x.get("pass") is True for x in validation_checks)
            and counts["freshChecksBeforeSeal"] == 16_689 and counts["failedChecksBeforeSeal"] == 0
            and package["status"] == "PASS" and package["checks"] == 419 and package["failures"] == []
            and all(x.get("pass") is True for x in package["results"])
            and d["totalChecksIncludingSeal"] == 17_108,
            {"freshChecks": len(validation_checks), "failedChecks": len(validation["failedChecks"]),
             "sealChecks": package["checks"], "totalIncludingSeal": d["totalChecksIncludingSeal"]})

        question_data = zip_json(z, "ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json")
        future = zip_json(z, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        record("All original questions and obligations are preserved through the reassessment",
            counts["questionsPreserved"] == 30 and counts["focusedAddenda"] == 2
            and counts["futureRequirementsPreserved"] == 9 and len(question_data["questions"]) == 30
            and len(question_data["addenda"]) == 2 and len(question_data["futureObligations"]) == 9
            and len(future["obligations"]) == 6,
            {"questions": len(question_data["questions"]), "addenda": len(question_data["addenda"]),
             "futureObligations": len(question_data["futureObligations"]), "dispositions": len(future["obligations"])})

        prior200_binding = zip_json(z, "EXTERNAL_ARCHIVE_BINDINGS.json")["return200"]
        prior200_size, prior200_sha, prior200_crc = digest(PRIOR200)
        old200 = zip_json(z, "context/PLANARGATES5_RETURN200_APPLICATION.json")
        old200_decision = zip_json(z, "context/PLANARGATES5_RETURN200_DECISION.json")
        record("Return200 applied gate identities stay source-bound and closed",
            old200["acceptedIds"] == ["gate", "absolute-gate", "planar-sanctuary"]
            and old200_decision["acceptedIds"] == old200["acceptedIds"]
            and old200["status"] == "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS"
            and (prior200_size, prior200_sha) ==
                (prior200_binding["bytes"], prior200_binding["sha256"]),
            {"closedAppliedIds": old200["acceptedIds"], "priorReturn200SHA256": prior200_sha})
        context283 = zip_json(z, "context/RETURN283_DIRECTOR_DECISION.json")
        next_group = decision["nextPendingGroup"]
        record("Return283 hold remains unchanged and Director selects the exact Summon Hosts5 next group",
            context283["heldIds"] == ["faction-omniscience-supreme"]
            and context283["blockerIds"] == ["KR198-B01"]
            and next_group["group"] == "rank9-summon-hosts5" and next_group["ids"] == NEXT
            and next_group["blockerIds"] == ["SH202-B01", "SH202-B02", "SH202-B03"]
            and d["nextPendingGroup"] == next_group,
            {"priorHold": context283["heldIds"], "nextPendingGroup": next_group})
        record("Return284 procedures are limited to the two scoped pending identities",
            set(decisions) == TARGETS and all(f"procedures/{s}.json" in name_set for s in TARGETS)
            and not any(n.startswith("procedures/") and n.split("/")[-1][:-5] not in TARGETS for n in names),
            {"procedures": [n for n in names if n.startswith("procedures/")]})

    failures = [c for c in checks if not c["passed"]]
    report = {"id": "RANK9-PLANARGATES5-RETURN284-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL", "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures), "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(),
            "bytes": zsize, "sha256": zsha, "crc32": zcrc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": dsize,
            "sha256": dsha, "crc32": dcrc}, "sourcePacket": {"path": SOURCE_ARCHIVE.relative_to(ROOT).as_posix(),
            "bytes": src_size, "sha256": src_sha, "crc32": src_crc}, "authority": AUTHORITY,
        "heldIds": sorted(TARGETS), "blockerIds": BLOCKERS, "semanticDisposition": "Director holds all targeted identities; integrity and replay checks do not establish semantic closure.", "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-PLANARGATES5-RETURN284-RECEIPT", "status": report["status"],
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
