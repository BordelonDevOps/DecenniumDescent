from __future__ import annotations

import gzip
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = BASE / "rank9_timefate6_return239_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_TimeFate4_Director_Return239_HELD.zip"
DELIVERY = RETURN_DIR / "DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_timefate6_current_source_239_prepared"
SOURCE_ZIP = SOURCE_DIR / "DD_Rank9_TimeFate6_CurrentSource_239.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_TimeFate6_CurrentSource_239_DELIVERY.json"
SOURCE_PREP = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_239.json"
TARGETS = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
EXPECTED_BLOCKERS = {
    "time-stop": ["TF192-B01"],
    "fate-rewrite": ["TF192-B04"],
    "collapse-timeline": ["TF192-B05"],
    "eternal-prophecy": ["TF192-B02"],
}
AUTH = {
    "reviewedApplied": 811,
    "pending": 37,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 535,
    "scopedInterfaces": 173,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def enc(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def write(path: Path, value) -> None:
    path.write_text(enc(value), encoding="utf-8", newline="\n")


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def check(checks: list[dict], name: str, passed: bool, details=None) -> None:
    checks.append({"id": name, "passed": bool(passed), "details": details})
    if not passed:
        raise AssertionError(f"Audit check failed: {name}: {details}")


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    delivery = readj(DELIVERY)
    source_delivery = readj(SOURCE_DELIVERY)
    preparation = readj(SOURCE_PREP)
    checks: list[dict] = []

    return_bytes = RETURN_ZIP.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    return_info = info(RETURN_ZIP)
    delivery_info = info(DELIVERY)
    check(checks, "downloaded-return-size-sha-crc-match-sidecar", all(return_info[k] == delivery["archive"][k] for k in ("bytes", "sha256", "crc32")), return_info)
    check(checks, "return-sidecar-is-valid-json-and-target-bound", delivery["id"] == "RETURN239-DELIVERY" and delivery["sourceAuthority"] == AUTH, {"deliveryId": delivery["id"], "authority": delivery["sourceAuthority"]})

    source_bytes = SOURCE_ZIP.read_bytes()
    source_info = info(SOURCE_ZIP)
    source_delivery_info = info(SOURCE_DELIVERY)
    source_binding_path = delivery["sourceArchive"]
    check(checks, "source-archive-packet239-binding-matches-local-bytes", all(source_info[k] == source_binding_path[k] == source_delivery["archive"][k] for k in ("bytes", "sha256", "crc32")), source_info)
    check(checks, "source-delivery-manifest-binds-packet239", source_delivery["archive"]["sha256"] == preparation["packet"]["sha256"] and source_delivery["archive"]["bytes"] == preparation["packet"]["bytes"], source_delivery["archive"])

    archive = zipfile.ZipFile(RETURN_ZIP)
    check(checks, "return-zip-crc-integrity", archive.testzip() is None, None)
    names = archive.namelist()
    expected_rows = {row["path"]: row for row in delivery["members"]}
    internal_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
    internal_rows = {row["path"]: row for row in internal_manifest["members"]}
    check(checks, "return-member-set-unique-safe-and-exact", len(names) == len(set(names)) == delivery["memberCount"] == 43 and all(safe_member(name) for name in names), {"members": len(names)})
    check(checks, "external-and-internal-member-manifests-reconcile", delivery["payloadMemberCount"] == internal_manifest["payloadMemberCount"] == 42 and set(expected_rows) == set(names) and set(internal_rows) | {"MEMBER_MANIFEST.json"} == set(names) and set(internal_rows) == set(expected_rows) - {"MEMBER_MANIFEST.json"}, {"externalRows": len(expected_rows), "internalRows": len(internal_rows), "zipMembers": len(names)})
    for name, row in expected_rows.items():
        raw = archive.read(name)
        check(checks, f"member:{name}", len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"], {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})

    source_binding = json.loads(archive.read("SOURCE_BINDING.json"))
    decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
    counts = json.loads(archive.read("COUNTS.json"))
    casebook = json.loads(gzip.decompress(archive.read("CASEBOOK.json.gz")))
    hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
    integrity = json.loads(archive.read("INTEGRITY_CHECK.json"))
    clock = json.loads(archive.read("CLOCK_CHECK.json"))
    source_check = json.loads(archive.read("SOURCE_CHECK.json"))
    preservation = json.loads(archive.read("PRESERVATION_CHECK.json"))
    semantic = json.loads(archive.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))

    check(checks, "exact-four-target-current-authority-and-held-scope", delivery["sourceAuthority"] == AUTH and delivery["accepted"] is False and delivery["applied"] is False and delivery["acceptedIds"] == [] and delivery["appliedIds"] == [] and delivery["heldIds"] == TARGETS and decision["targetIds"] == TARGETS and decision["sourceAuthority"] == AUTH and decision["accepted"] is False and decision["applied"] is False and decision["heldIds"] == TARGETS, {"acceptedIds": delivery["acceptedIds"], "appliedIds": delivery["appliedIds"], "heldIds": delivery["heldIds"]})
    decisions = {row["spellId"]: row for row in decision["decisions"]}
    check(checks, "exact-per-identity-blockers-and-held-rulings", set(decisions) == set(TARGETS) and {sid: decisions[sid]["blockerIds"] for sid in TARGETS} == EXPECTED_BLOCKERS and all(decisions[sid]["held"] is True and decisions[sid]["accepted"] is False and decisions[sid]["applied"] is False for sid in TARGETS), {sid: decisions[sid]["blockerIds"] for sid in decisions})
    check(checks, "next-pending-group-is-casting-cost5-only", delivery["nextPendingGroup"] == {"group": "rank9-casting-cost5", "pendingIds": ["unholy-ascendance"], "authority": "Requires fresh packet/authority after independent audit; no next-group review performed here."}, delivery["nextPendingGroup"])
    check(checks, "four-target-procedures-and-casebook-scope", counts["procedures"] == 4 and len(casebook.get("cases", [])) == counts["cases"] == 62 and {case.get("spellId") for case in casebook["cases"]} == set(TARGETS), {"procedures": counts["procedures"], "cases": len(casebook.get("cases", []))})
    events = sum(len(case.get("events", [])) for case in casebook["cases"])
    check(checks, "event-forward-inverse-counts-reconcile", events == counts["events"] == delivery["counts"]["events"] == 628 and counts["forwardOperations"] == counts["inverseOperations"] == 1256 and counts["eventOperations"] == 2512 and delivery["counts"] == counts, {"events": events, "forward": counts["forwardOperations"], "inverse": counts["inverseOperations"]})
    check(checks, "integrity-clock-source-preservation-and-semantic-reports-pass", all(report["failureCount"] == 0 and all(item.get("pass", False) for item in report["checks"]) for report in (integrity, clock, source_check, preservation, semantic)) and integrity["checkCount"] == counts["integrityChecks"] == 9100 and clock["checkCount"] == counts["clockChecks"] == 5728 and source_check["checkCount"] == counts["sourceChecks"] == 1272 and preservation["checkCount"] == counts["preservationChecks"] == 163 and semantic["checkCount"] == counts["semanticChecks"] == 16 and semantic["status"] == "ALL_FOUR_HELD", {"integrity": integrity["checkCount"], "clock": clock["checkCount"], "source": source_check["checkCount"], "preservation": preservation["checkCount"], "semantic": semantic["checkCount"]})

    prep_snapshot = preparation["sourceSnapshot"]
    check(checks, "return-source-snapshot-matches-current-preparation", source_binding["sourceSnapshot"]["headCommit"] == prep_snapshot["headCommit"] and source_binding["sourceSnapshot"]["branch"] == prep_snapshot["branch"] == "main" and source_binding["sourceSnapshot"]["indexBinding"] == prep_snapshot["indexBinding"] and source_binding["sourceSnapshot"]["catalogBinding"] == prep_snapshot["catalogBinding"], source_binding["sourceSnapshot"])
    check(checks, "return-source-packet-sidecar-and-authority-match", source_binding["externalSourceArchive"]["sha256"] == source_info["sha256"] and source_binding["externalSourceArchive"]["bytes"] == source_info["bytes"] and source_binding["sourceAuthority"] == AUTH and source_binding["sourceArchiveIncluded"] is False, source_binding["externalSourceArchive"])

    with zipfile.ZipFile(SOURCE_ZIP) as source_archive:
        source_manifest = json.loads(source_archive.read("MANIFEST.json"))
        candidate = json.loads(source_archive.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_239.json"))
        source_member_rows = {row["path"]: row for row in source_manifest["members"]}
        candidate_bindings = {row["path"]: row for row in candidate["sourceBindings"]}
        returned_bindings = {row["path"]: row for row in source_binding["currentSourceBindings"]}
        all_bindings_match = len(candidate_bindings) == len(returned_bindings) == len(source_binding["currentSourceBindings"]) == 140
        binding_errors = []
        for path, candidate_row in candidate_bindings.items():
            returned = returned_bindings.get("sources_current/" + path)
            archive_row = source_member_rows.get("sources_current/" + path)
            if returned is None or archive_row is None:
                all_bindings_match = False
                binding_errors.append(path)
                continue
            raw = source_archive.read("sources_current/" + path)
            local_path = ROOT / Path(*PurePosixPath(path).parts)
            local_raw = local_path.read_bytes()
            valid = (
                len(raw) == candidate_row["bytes"] == returned["bytes"] == archive_row["bytes"] == len(local_raw)
                and candidate_row["sha256"] == returned["sha256"] == archive_row["sha256"] == sha(raw) == sha(local_raw)
                and returned["crc32"] == archive_row["crc32"] == crc(raw) == crc(local_raw)
            )
            if not valid:
                all_bindings_match = False
                binding_errors.append(path)
    check(checks, "all-140-refreshed-source-bindings-match-packet-and-working-tree", all_bindings_match and not binding_errors, {"matched": 140 - len(binding_errors), "errors": binding_errors[:10]})

    prior221 = BASE / "rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD.zip"
    prior238 = BASE / "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip"
    prior221_info, prior238_info = info(prior221), info(prior238)
    check(checks, "prior-return221-and-return238-identities-match", source_binding["priorReturn221Archive"]["bytes"] == prior221_info["bytes"] and source_binding["priorReturn221Archive"]["sha256"] == prior221_info["sha256"] and archive.read("prior238/DIRECTOR_DECISION.json") and archive.read("prior238/HOLD_REGISTER.json"), {"return221": prior221_info, "return238": prior238_info})
    with zipfile.ZipFile(prior238) as prior238_archive:
        prior238_decision = json.loads(prior238_archive.read("DIRECTOR_DECISION.json"))
        prior238_holds = json.loads(prior238_archive.read("HOLD_REGISTER.json"))
        returned_prior238_decision = json.loads(archive.read("prior238/DIRECTOR_DECISION.json"))
        returned_prior238_holds = json.loads(archive.read("prior238/HOLD_REGISTER.json"))
        prior_blockers = {row["id"]: row for row in prior238_holds["blockers"]}
        check(checks, "agency-control9-prior-holds-retained", returned_prior238_decision == prior238_decision and returned_prior238_holds == prior238_holds and prior238_decision["acceptedIds"] == prior238_decision["appliedIds"] == [] and prior238_decision["heldIds"] == ["absolute-domination", "puppetmaster-s-realm"] and set(prior_blockers) == {"AG190-B01", "AG190-B02"} and all(prior_blockers[bid]["status"] == "OPEN" for bid in prior_blockers) and hold_register["inheritedRegister"]["carryForwardExact"] == ["AG190-B01", "AG190-B02"], {"heldIds": prior238_decision["heldIds"], "priorBlockers": sorted(prior_blockers)})
    check(checks, "no-acceptance-or-application-and-preservation-gate", decision["accepted"] is False and decision["applied"] is False and decision["acceptedIds"] == decision["appliedIds"] == delivery["acceptedIds"] == delivery["appliedIds"] == [] and preservation["failureCount"] == 0 and "No application, canonical changes" in delivery["qualifications"], {"acceptedIds": decision["acceptedIds"], "appliedIds": decision["appliedIds"]})

    audit_path = BASE / "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json"
    independent_audit = {
        "id": "RANK9-TIMEFATE6-RETURN239-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS_PACKAGE_BINDING_AND_SCOPE; ALL_FOUR_SEMANTIC_HOLDS_RETAINED",
        "returnArchive": return_info,
        "deliveryManifest": delivery_info,
        "sourcePacket": source_info,
        "sourceDeliveryManifest": source_delivery_info,
        "checksPassed": len(checks),
        "checksFailed": 0,
        "checks": checks,
        "limitations": [
            "The return ZIP and delivery manifest, all 43 members, current-source packet binding, all 140 refreshed source files, authority, scope, hold IDs and previous-return preservation were independently checked.",
            "Replay counts and all reported integrity, clock, source, preservation and semantic-check records were verified for internal consistency. GPT-supplied programs were not executed and the semantic replay was not independently reproduced.",
        ],
    }
    audit_path.write_text(enc(independent_audit), encoding="utf-8", newline="\n")

    blocker_reasons = {sid: {"blockerIds": decisions[sid]["blockerIds"], "minimumMissingWitness": decisions[sid]["minimumMissingWitness"], "qualificationIds": decisions[sid]["conditionalQualificationIds"]} for sid in TARGETS}
    receipt = {
        "id": "RANK9-TIMEFATE6-DIRECTOR-RETURN-239-RECEIPT",
        "recordedAtUtc": now,
        "status": "ALL_FOUR_HELD; RETURN_ARCHIVE_AND_SOURCE_BINDINGS_INDEPENDENTLY_VERIFIED",
        "reviewedIds": TARGETS,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockers": blocker_reasons,
        "sourceAuthority": AUTH,
        "sourcePacket": source_info,
        "directorReturn": return_info,
        "deliveryManifest": delivery_info,
        "counts": counts,
        "independentAudit": {"path": audit_path.relative_to(ROOT).as_posix(), "checksPassed": len(checks), "checksFailed": 0},
        "nextGroup": "rank9-casting-cost5",
        "canonicalFilesModified": False,
        "GitHubModified": False,
        "runtimeExecuted": False,
    }
    receipt_path = BASE / "RANK9_TIMEFATE6_RETURN239_RECEIPT.json"
    receipt_path.write_text(enc(receipt), encoding="utf-8", newline="\n")

    submission_path = BASE / "RANK9_TIMEFATE6_PACKET_239_SUBMISSION.json"
    submission = readj(submission_path)
    submission["status"] = "RETURN239_AUDIT_PASS_ALL_HELD_811_37_0"
    submission["directorReturn"] = return_info
    submission["directorReturnDelivery"] = delivery_info
    submission["returnIndependentAudit"] = info(audit_path)
    submission["returnReceipt"] = info(receipt_path)
    submission["acceptedIds"] = []
    submission["appliedIds"] = []
    submission["heldIds"] = TARGETS
    write(submission_path, submission)

    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_239.json"
    pending = readj(pending_path)
    pending["status"] = "RETURN239_AUDIT_PASS_ALL_HELD_811_37_0"
    pending["currentReturnAudit"] = info(audit_path)
    pending["lastDirectorReturn"] = {
        "return": 239,
        "group": "rank9-time-fate6",
        "reviewedIds": TARGETS,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockers": blocker_reasons,
        "independentAudit": info(audit_path),
        "receipt": info(receipt_path),
    }
    write(pending_path, pending)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_239.json"
    queue = readj(queue_path)
    queue["recordedAtUtc"] = now
    queue["status"] = queue["packetStatus"] = "RETURN239_AUDIT_PASS_ALL_HELD_811_37_0"
    queue["pendingIdentityAudit"] = info(pending_path)
    queue["currentReturn"] = return_info
    queue["currentReturnDelivery"] = delivery_info
    queue["currentReturnAudit"] = info(audit_path)
    queue["currentReturnReceipt"] = info(receipt_path)
    queue["currentReturnAuditStatus"] = independent_audit["status"]
    queue["currentReturnAuditChecks"] = len(checks)
    queue["currentReturnAuditFailures"] = 0
    queue["currentSubmission"] = info(submission_path)
    queue["nextGroup"] = "rank9-casting-cost5"
    queue["next"] = {"group": "rank9-casting-cost5", "pendingIds": ["unholy-ascendance"], "pendingCount": 1, "status": "DIRECTOR_SELECTED_AWAITING_FRESH_CURRENT_SOURCE_PACKET"}
    row = next(group for group in queue["currentPendingGroups"] if group["group"] == "rank9-time-fate6")
    row["status"] = "RETURN239_AUDIT_PASS_ALL_FOUR_HELD"
    row["freshPacketRequiredForCurrentAuthority"] = True
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_239.json"
    handoff = readj(handoff_path)
    handoff["recordedAtUtc"] = now
    handoff["status"] = "RETURN239_AUDIT_PASS_ALL_HELD_811_37_0"
    handoff["pendingIdentityAudit"] = info(pending_path)
    handoff["queue"] = info(queue_path)
    handoff["currentQueueBinding"] = info(queue_path)
    handoff["currentReturn"] = return_info
    handoff["currentReturnDelivery"] = delivery_info
    handoff["currentReturnAudit"] = info(audit_path)
    handoff["currentReturnReceipt"] = info(receipt_path)
    handoff["currentReturnAuditStatus"] = independent_audit["status"]
    handoff["currentReturnAuditChecks"] = len(checks)
    handoff["currentReturnAuditFailures"] = 0
    handoff["currentSubmission"] = info(submission_path)
    handoff["nextGroup"] = "rank9-casting-cost5"
    handoff["nextStep"] = "Return239 is independently package/source-bound and all four Time/Fate6 identities remain held. Prepare a fresh current-authority packet for the director-selected rank9-casting-cost5 identity unholy-ascendance."
    handoff["resumePriority"] = "Authority remains 811 reviewed/applied, 37 pending and 0 accepted-unapplied. Time/Fate6 holds are TF192-B01, TF192-B04, TF192-B05 and TF192-B02. Next director-selected group is rank9-casting-cost5 — unholy-ascendance."
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_239.md"
    snapshot = snapshot_path.read_text(encoding="utf-8")
    snapshot = snapshot.replace("Packet239 is submitted to GPT and awaiting its director decision.", "Return239 independently passed package/source-binding verification; all four Time/Fate6 identities remain held.")
    snapshot += "\n\nGPT selected **rank9-casting-cost5 — unholy-ascendance** as the next review. Authority remains **811/37/0**.\n"
    snapshot_path.write_text(snapshot, encoding="utf-8", newline="\n")

    print(json.dumps({"status": independent_audit["status"], "checksPassed": len(checks), "checksFailed": 0, "return": return_info, "nextGroup": receipt["nextGroup"], "authority": AUTH}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
