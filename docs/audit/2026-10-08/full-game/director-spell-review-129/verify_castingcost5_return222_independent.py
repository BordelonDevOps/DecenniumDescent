from __future__ import annotations

import gzip
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import jsonpatch

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN = BASE / "rank9_castingcost5_return222_received"
ARCHIVE = RETURN / "DD_Rank9_CastingCost2_Director_Return222.zip"
DELIVERY = RETURN / "DD_Rank9_CastingCost2_Director_Return222_DELIVERY.json"
SOURCE_PACKET = BASE / "rank9_castingcost5_current_source_222_prepared_retry1/DD_Rank9_CastingCost5_CurrentSource_222.zip"
SOURCE_DELIVERY = BASE / "rank9_castingcost5_current_source_222_prepared_retry1/DD_Rank9_CastingCost5_CurrentSource_222_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
REPORT = BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 810, "pending": 38, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 534, "scopedInterfaces": 173}
SCOPE = ["perfect-spell", "unholy-ascendance"]


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def readj(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts)


def verify() -> dict:
    checks: list[dict] = []

    def check(name: str, ok: bool, detail=None):
        checks.append({"check": name, "passed": bool(ok), **({"detail": detail} if detail is not None else {})})

    archive_raw = ARCHIVE.read_bytes()
    delivery_raw = DELIVERY.read_bytes()
    delivery = readj(delivery_raw)
    source_delivery_raw = SOURCE_DELIVERY.read_bytes()
    source_delivery = readj(source_delivery_raw)
    check("Return ZIP byte count and SHA-256 match external delivery", len(archive_raw) == delivery["archive"]["bytes"] == 4_737_535 and digest(archive_raw) == delivery["archive"]["sha256"] == "6884e7b0c564383355754cc325371b36bfbd0b3fd3113519c1fb00a6e3381af8")
    check("Return delivery manifest SHA-256 matches GPT-reported binding", digest(delivery_raw) == "04a9ea15361ac8cc8d742861181e266e7e1a40eab292114ac9a9b7c414ada3ab")
    check("Director records only the exact two pending IDs", delivery["sourceAuthority"] == AUTHORITY and delivery["acceptedIds"] == ["perfect-spell"] and delivery["heldIds"] == ["unholy-ascendance"] and delivery["applied"] is False)
    check("Return binds the exact submitted current-source packet", delivery["sourcePacket"]["bytes"] == source_delivery["archive"]["bytes"] and delivery["sourcePacket"]["sha256"] == source_delivery["archive"]["sha256"] == "fd28704b4f79063f828ed2abc3a6c22a9254bea1828194b9db4e057da473f9b9")

    with zipfile.ZipFile(ARCHIVE) as zf:
        names = zf.namelist()
        allow = set(delivery["exactAllowlist"])
        delivery_rows = {r["path"]: r for r in delivery["members"]}
        check("Return ZIP has a clean CRC and exact safe unique 29-member allowlist", zf.testzip() is None and len(names) == len(set(names)) == delivery["memberCount"] == 29 and set(names) == allow == set(delivery_rows) and all(safe_member(n) for n in names))

        member_manifest = readj(zf.read("MEMBER_MANIFEST.json"))
        member_rows = {r["path"]: r for r in member_manifest["members"]}
        check("Internal manifest binds all 28 payload members and correct two-ID authority", member_manifest["payloadMemberCount"] == 28 and member_manifest["sourceAuthority"] == AUTHORITY and set(member_rows) == set(names) - {"MEMBER_MANIFEST.json"})
        all_member_hashes = True
        for name in names:
            raw = zf.read(name)
            drow = delivery_rows[name]
            if len(raw) != drow["bytes"] or digest(raw) != drow["sha256"] or crc(raw) != drow["crc32"].lower():
                all_member_hashes = False
                break
            if name != "MEMBER_MANIFEST.json":
                mrow = member_rows[name]
                if len(raw) != mrow["bytes"] or digest(raw) != mrow["sha256"] or crc(raw) != mrow["crc32"].lower():
                    all_member_hashes = False
                    break
        check("All 29 external and 28 internal member size/SHA/CRC bindings recalculate", all_member_hashes)

        context = readj(zf.read("evidence/CURRENT_CONTEXT.json"))
        source_binding = readj(zf.read("SOURCE_BINDING.json"))
        decision = readj(zf.read("DIRECTOR_DECISION.json"))
        holds = readj(zf.read("HOLD_REGISTER.json"))
        failure = readj(zf.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        counts = readj(zf.read("COUNTS.json"))
        validation = readj(zf.read("VALIDATION.json"))
        source_verification = readj(zf.read("SOURCE_VERIFICATION.json"))
        data_check = readj(zf.read("DATA_INTEGRITY_CHECK.json"))
        clock_check = readj(zf.read("CLOCK_CHECK.json"))
        focused = readj(zf.read("FOCUSED_CASES.json"))
        trace = readj(zf.read("TRACE_INDEX.json"))
        procedures = {sid: readj(zf.read(f"procedures/{sid}.json")) for sid in SCOPE}
        input_delivery = zf.read("evidence/INPUT_DELIVERY.json")

        check("Current context preserves the submitted working-tree commit, branch and authority", context["sourceAuthority"] == AUTHORITY and context["sourceSnapshot"]["headCommit"] == "197366eae0c786415de55a0e4739e83f49f1a65f" and context["sourceSnapshot"]["branch"] == "main")
        check("Embedded input delivery bytes exactly match the uploaded source sidecar", input_delivery == source_delivery_raw)
        check("Return source binding names the exact uploaded archive and does not claim it is embedded", source_binding["externalSourceArchive"]["sha256"] == delivery["sourcePacket"]["sha256"] and source_binding["archiveIncluded"] is False and delivery["sourceArchiveIncluded"] is False)
        check("Director decision is per-identity and unapplied", decision["scope"] == SCOPE and decision["acceptedIds"] == ["perfect-spell"] and decision["heldIds"] == ["unholy-ascendance"] and decision["applied"] is False)
        decisions = {d["id"]: d for d in decision["decisions"]}
        check("Perfect Spell exactly resolves CC194-B01 with all six conditional qualifications", decisions["perfect-spell"]["accepted"] is True and decisions["perfect-spell"]["applied"] is False and decisions["perfect-spell"]["blockerIds"] == [] and decisions["perfect-spell"]["resolvedBlockerIds"] == ["CC194-B01"] and set(decisions["perfect-spell"]["conditionalQualificationIds"]) == {"CC194-H01", "CC194-H02", "CC194-H05", "CC194-H06", "CC194-H07", "CC194-H08"})
        check("Unholy Ascendance remains held only under CC194-B04 with its source/lifecycle qualifications", decisions["unholy-ascendance"]["accepted"] is False and decisions["unholy-ascendance"]["applied"] is False and decisions["unholy-ascendance"]["blockerIds"] == ["CC194-B04"] and set(decisions["unholy-ascendance"]["conditionalQualificationIds"]) == {"CC194-H01", "CC194-H02", "CC194-H07", "CC194-H08"})
        blockers = {b["id"]: b for b in holds["currentBlockers"]}
        check("CC194-B04 retains concrete Undead recipient-lifecycle witnesses", "CC194-B04" in blockers and blockers["CC194-B04"]["blockingForIds"] == ["unholy-ascendance"] and len(blockers["CC194-B04"]["requiredWitnesses"]) == 4)
        check("Failure check records B01 resolved by named traces and B04 still open", failure["sourceReassessment"]["perfect-spell"]["status"] == "RESOLVED_BY_PS222_FUNDED_AND_FRESH_TRACES" and failure["sourceReassessment"]["unholy-ascendance"]["status"] == "OPEN_REASSESSED_CURRENT_BYTES" and failure["applied"] is False)

        check("GPT package source checks all pass", source_verification["checkCount"] == 969 and source_verification["failureCount"] == 0 and all(c["pass"] for c in source_verification["checks"]))
        check("GPT package data-integrity checks all pass", data_check.get("failureCount", 0) == 0 and all(c.get("pass") is True for c in data_check.get("checks", [])) and len(data_check.get("checks", [])) == 2714)
        check("GPT package clock checks all pass", clock_check.get("failureCount", 0) == 0 and all(c.get("pass") is True for c in clock_check.get("checks", [])) and len(clock_check.get("checks", [])) == 3465)
        package_checks = delivery["packageValidation"]["checks"]
        check("All 119 GPT package checks pass", delivery["packageValidation"]["checkCount"] == 119 and delivery["packageValidation"]["failureCount"] == 0 and all(c["pass"] for c in package_checks))
        check("Validation reports pass with all downstream/runtime gates off", validation["status"] == "PASS_STATIC_INTEGRITY_AND_PER_IDENTITY_SEMANTIC_DECISION" and validation["applied"] is False and counts["appliedIds"] == 0 and not validation["unexpectedFailures"])
        check("Reported scope/counts reconcile to 34 cases, 522 events and 2,088 patch operations", counts["procedures"] == 2 and counts["acceptedIds"] == 1 and counts["heldIds"] == 1 and counts["cases"] == trace["caseCount"] == 34 and counts["events"] == trace["events"] == 522 and counts["forwardOperations"] == counts["inverseOperations"] == 1044 and counts["eventOperations"] == 2088)

        # Bind all 117 refreshed source files to the current packet actually sent to GPT.
        with zipfile.ZipFile(SOURCE_PACKET) as source_zip:
            source_candidate = readj(source_zip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_222.json"))
            packet_bindings = {x["path"]: x for x in source_candidate["sourceBindings"]}
            returned_sources = source_binding["refreshedSources"]
            source_matches = len(packet_bindings) == len(returned_sources) == 117
            for rb in returned_sources:
                path = rb["path"].removeprefix("sources_current/")
                pb = packet_bindings.get(path)
                member = "sources_current/" + path
                if not pb or member not in source_zip.namelist() or len(source_zip.read(member)) != rb["bytes"] or digest(source_zip.read(member)) != rb["sha256"]:
                    source_matches = False
                    break
                if pb["bytes"] != rb["bytes"] or pb["sha256"] != rb["sha256"]:
                    source_matches = False
                    break
            check("All 117 refreshed source bindings match the exact submitted packet", source_matches)
            catalog = readj(source_zip.read("sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
            candidate_index = readj(source_zip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_222.json"))
            catalog_rows = {x["id"]: x for x in catalog["spells"]}
            candidate_rows = {x["spellId"]: x for x in candidate_index["records"]}
            cards_match = True
            for sid in SCOPE:
                proc = procedures[sid]
                if proc["completeSourceAndAccess"] != catalog_rows[sid] or candidate_rows[sid]["completeCurrentCatalogSourceAndAccess"] != catalog_rows[sid] or candidate_rows[sid]["currentIndexEntry"]["authoredStatus"] != "pending-authored-procedure":
                    cards_match = False
            check("Both procedures preserve exact current catalog cards and were pending at submission", cards_match)

        # Independently verify all preserved and new before/after state transitions.
        old_book = readj(gzip.decompress(zf.read("PRESERVED_CASEBOOK.json.gz")))
        old_cases = old_book["cases"]
        new_cases = focused["cases"]
        case_map = {x["id"]: x for x in old_cases + new_cases}
        check("Exactly 25 prior cases and nine fresh focused cases are included", len(old_cases) == 25 and len(new_cases) == 9 and len(case_map) == 34 and len(new_cases) == counts["newFocusedCases"])
        total_events = total_forward = total_inverse = 0
        replay_ok = True
        replay_errors = []
        for row in trace["cases"]:
            case = case_map.get(row["caseId"])
            if not case or digest(canonical(case)) != row["canonicalCaseSHA256"]:
                replay_ok = False
                replay_errors.append(f"case-binding:{row['caseId']}")
                continue
            state = case["initialState"]
            if digest(canonical(state)) != row["initialStateSHA256"] or state != case["events"][0]["before"]:
                replay_ok = False
                replay_errors.append(f"initial-state:{row['caseId']}")
                continue
            total_events += len(case["events"])
            seen = set()
            for event in case["events"]:
                if event["id"] in seen or event["before"] != state:
                    replay_ok = False
                    replay_errors.append(f"event-order:{event['id']}")
                    break
                seen.add(event["id"])
                if digest(canonical(event["before"])) != event["beforeSHA256"] or digest(canonical(event["after"])) != event["afterSHA256"]:
                    replay_ok = False
                    replay_errors.append(f"event-hash:{event['id']}")
                    break
                try:
                    if jsonpatch.JsonPatch(event["forward"]).apply(event["before"], in_place=False) != event["after"]:
                        replay_ok = False
                        replay_errors.append(f"forward:{event['id']}")
                        break
                    if jsonpatch.JsonPatch(event["inverse"]).apply(event["after"], in_place=False) != event["before"]:
                        replay_ok = False
                        replay_errors.append(f"inverse:{event['id']}")
                        break
                except Exception as exc:
                    replay_ok = False
                    replay_errors.append(f"patch:{event['id']}:{type(exc).__name__}")
                    break
                total_forward += len(event["forward"])
                total_inverse += len(event["inverse"])
                state = event["after"]
            if not replay_ok:
                break
            if state != case["finalState"] or digest(canonical(state)) != row["finalStateSHA256"] or row["events"] != len(case["events"]):
                replay_ok = False
                replay_errors.append(f"final-state:{row['caseId']}")
                break
        check("All indexed case hashes and 522 forward/inverse transitions independently replay", replay_ok and total_events == 522 and total_forward == total_inverse == 1044, replay_errors[:10])

        focused_by_id = {x["id"]: x for x in new_cases}
        funded_ok = True
        for case_id, x in [("CC222-PS-funded-X2", 2), ("CC222-PS-funded-PB6", 6)]:
            c = focused_by_id[case_id]
            actor = c["finalState"]["actors"]["A"]
            leaf = [r for r in actor["resourceHistory"] if r.get("kind") == "protected-conversion-payment"]
            expected_cost = 26 + x
            funded_ok = funded_ok and c["runtimeExecuted"] is False and leaf and leaf[-1]["actualBasePaid"] == 0 and leaf[-1]["baseWaived"] == 5 and leaf[-1]["actualXPaid"] == x and leaf[-1]["creditedRP"] == x and leaf[-1]["rootPaymentCredited"] == 0 and leaf[-1]["surchargeCredited"] == 0 and actor["rp"] == c["initialState"]["actors"]["A"]["rp"] - expected_cost and actor["tempHPSource"]["offered"] == 5 * x and actor["action"] == 0
        check("Paid-X cases enforce waived base, real X payment, 5X credit, 26+X total RP and one root Action", funded_ok)

        rejected_ok = True
        for case_id in ["CC222-PS-zero-credit-rejected", "CC222-PS-over-cap-rejected", "CC222-PS-insufficient-RP-rejected"]:
            c = focused_by_id[case_id]
            a0, a1 = c["initialState"]["actors"]["A"], c["finalState"]["actors"]["A"]
            rejected_ok = rejected_ok and a1["rp"] == a0["rp"] and a1["action"] == a0["action"] and a1.get("tempHP", 0) == a0.get("tempHP", 0) and a1.get("resourceHistory", []) == a0.get("resourceHistory", [])
        check("Zero-credit, over-cap and insufficient-RP branches reject before spending root resources", rejected_ok)

        arbitration_ok = True
        for case_id, wanted_cast, wanted_hp in [("CC222-PS-equal-offer-retained", "cast1-A", 10), ("CC222-PS-weaker-offer-retained", "cast1-A", 20), ("CC222-PS-stronger-offer-replaces", "cast2-A", 20)]:
            a = focused_by_id[case_id]["finalState"]["actors"]["A"]
            arbitration_ok = arbitration_ok and a["tempHP"] == wanted_hp and wanted_cast in a["tempHPSource"]["id"]
        counter = focused_by_id["CC222-PS-countered-paid-X"]["finalState"]["actors"]["A"]
        counter_ok = counter["tempHPSource"] is None and counter["rp"] == 52 and any(r.get("kind") == "protected-conversion-payment" and r.get("actualXPaid") == 2 for r in counter["resourceHistory"])
        check("Equal/weaker offers preserve the old grant, stronger replaces it, and countering retains paid X without granting a shield", arbitration_ok and counter_ok)

        qualification_text = " ".join(delivery["qualifications"]).lower()
        qualification_gates = all(term in qualification_text for term in ["no runtime execution", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"])
        hold_gates = {"CC194-H02", "CC194-H07", "CC194-H08"} <= set(decisions["perfect-spell"]["conditionalQualificationIds"])
        check("Runtime/implementation/play/balance/cosmology/domain/completion/release gates remain explicit", qualification_gates and hold_gates and all(decisions[s]["applied"] is False for s in SCOPE))

    passed = sum(c["passed"] for c in checks)
    report = {
        "id": "RANK9-CASTING-COST5-RETURN222-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checksPassed": passed,
        "checksFailed": len(checks) - passed,
        "checks": checks,
        "acceptedIds": ["perfect-spell"],
        "heldIds": ["unholy-ascendance"],
        "applied": False,
        "sourceAuthority": AUTHORITY,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(archive_raw), "sha256": digest(archive_raw), "crc32": crc(archive_raw)},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_raw), "sha256": digest(delivery_raw), "crc32": crc(delivery_raw)},
        "replay": {"cases": 34, "events": total_events, "forwardPatchOps": total_forward, "inversePatchOps": total_inverse},
        "nextGroup": "rank9-memory-denial6",
        "note": "This audit independently recalculates ZIP/member/source bindings and state patch replay. Semantic acceptance is the director's per-identity ruling; this report does not apply it.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    receipt = {"id": "RANK9-CASTING-COST5-RETURN222-RECEIPT", "recordedAtUtc": report["recordedAtUtc"],
               "status": "INDEPENDENT_AUDIT_PASSED_ACCEPTED_UNAPPLIED_HELD_RETAINED" if report["status"] == "PASS" else "INDEPENDENT_AUDIT_FAILED_NO_APPLICATION",
               "reviewedIds": SCOPE, "acceptedIds": ["perfect-spell"], "appliedIds": [], "heldIds": ["unholy-ascendance"],
               "blockers": {"unholy-ascendance": ["CC194-B04"]}, "sourceAuthority": AUTHORITY,
               "directorReturn": report["returnArchive"], "deliveryManifest": report["deliveryManifest"],
               "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), "bytes": REPORT.stat().st_size, "sha256": digest(REPORT.read_bytes())},
               "counts": {"cases": 34, "events": total_events, "forwardOperations": total_forward, "inverseOperations": total_inverse},
               "canonicalFilesModified": False, "GitHubModified": False, "runtimeExecuted": False}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": passed, "checksFailed": len(checks) - passed,
                      "acceptedIds": report["acceptedIds"], "heldIds": report["heldIds"], "applied": False,
                      "replay": report["replay"], "archiveSha256": digest(archive_raw),
                      "deliverySha256": digest(delivery_raw), "receipt": receipt["status"]}, indent=2))


if __name__ == "__main__":
    verify()
