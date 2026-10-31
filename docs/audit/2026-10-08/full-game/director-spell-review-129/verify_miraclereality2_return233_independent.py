#!/usr/bin/env python3
"""Independent structural and evidence audit of Director Return233."""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_miraclereality2_return233_received"
ARCHIVE = RECEIVED / "DD_Rank9_MiracleReality2_Director_Return233_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json"
SOURCE = BASE / "rank9_miraclereality2_current_source_233_prepared/DD_Rank9_MiracleReality2_CurrentSource_233_CORRECTED_V2.zip"
REPORT = BASE / "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json"

checks: list[dict] = []


def digest(data: bytes) -> dict:
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}"}


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def read_json(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def record_matches(data: bytes, record: dict) -> bool:
    got = digest(data)
    return all(got.get(k) == record.get(k) for k in ("bytes", "sha256")) and (record.get("crc32") is None or got["crc32"] == record["crc32"])


def ids(items) -> list[str]:
    return [item.get("id") for item in items if isinstance(item, dict) and item.get("id")]


def safe_path(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_digest = digest(archive_bytes)
check("delivery archive byte count, SHA-256 and CRC32 match", record_matches(archive_bytes, delivery.get("archive", {})), archive_digest)
check("delivery names the received Return233 archive", delivery.get("archive", {}).get("fileName") == ARCHIVE.name, delivery.get("archive", {}).get("fileName"))
authority_expected = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
check("delivery identity and authority remain 811/37/0", delivery.get("id") == "RANK9-MIRACLE-REALITY2-DIRECTOR-RETURN233-DELIVERY" and delivery.get("authority") == authority_expected, delivery.get("authority"))
target_ids = ["divine-intervention-greater", "wish"]
check("delivery holds exactly both targets without accepting or applying", delivery.get("heldIds") == target_ids and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("accepted") is False and delivery.get("applied") is False, {k: delivery.get(k) for k in ["heldIds", "acceptedIds", "appliedIds", "accepted", "applied"]})

outer = zipfile.ZipFile(io.BytesIO(archive_bytes))
names = outer.namelist()
name_set = set(names)
delivery_members = delivery.get("members", [])
delivery_by_path = {x.get("path"): x for x in delivery_members if isinstance(x, dict)}
check("archive members are unique, safe regular paths", len(names) == len(name_set) and all(safe_path(n) for n in names) and all(not x.is_dir() for x in outer.infolist()), {"members": len(names), "unique": len(name_set)})
check("delivery allowlist exactly matches archive members", set(delivery_by_path) == name_set and len(delivery_by_path) == len(delivery_members) == delivery.get("memberCount"), {"archive": len(names), "delivery": len(delivery_members), "memberCount": delivery.get("memberCount")})
member_failures = [n for n in names if n not in delivery_by_path or not record_matches(outer.read(n), delivery_by_path[n])]
check("every archive member matches delivery SHA, byte and CRC bindings", not member_failures, member_failures[:20])
manifest_bytes = outer.read("MEMBER_MANIFEST.json")
manifest = read_json(manifest_bytes)
check("embedded member manifest is bound by delivery", record_matches(manifest_bytes, delivery.get("memberManifest", {})) and delivery.get("memberManifest", {}).get("path") == "MEMBER_MANIFEST.json", digest(manifest_bytes))
payload = manifest.get("members", [])
payload_map = {x.get("path"): x for x in payload if isinstance(x, dict)}
check("embedded manifest covers all non-manifest members", set(payload_map) == name_set - {"MEMBER_MANIFEST.json"} and len(payload_map) == len(payload) == delivery.get("payloadCount"), {"archivePayload": len(name_set)-1, "listed": len(payload), "payloadCount": delivery.get("payloadCount")})
payload_failures = [n for n, rec in payload_map.items() if n not in name_set or not record_matches(outer.read(n), rec)]
check("every payload member matches embedded manifest", not payload_failures, payload_failures[:20])

def obj(name: str):
    return read_json(outer.read(name))


decision = obj("DIRECTOR_DECISION.json")
authority = obj("CURRENT_AUTHORITY.json")
counts = obj("COUNTS.json")
questions = obj("QUESTION_DISPOSITIONS.json")
original_questions = obj("ORIGINAL_QUESTIONS.json")
additions = obj("FOCUSED_ADDITIONS.json")
main_cases = obj("MAIN_CASE_DISPOSITIONS.json")
main_obligations = obj("ORIGINAL_MAIN_CASE_OBLIGATIONS.json")
future = obj("FUTURE_CASE_DISPOSITIONS.json")
casebook = obj("CASEBOOK.json")
integrity = obj("DATA_INTEGRITY_AND_REPLAY.json")
clock = obj("CLOCK_CHECK.json")
source_bindings = obj("SOURCE_BINDINGS.json")
source_verification = obj("SOURCE_VERIFICATION.json")
preseal = obj("PRESEAL_CHECK.json")
hold_register = obj("HOLD_REGISTER.json")
next_group = obj("NEXT_GROUP.json")
packet_finding = obj("PACKET_REFERENCE_FINDING.json")

check("embedded authority mirrors delivery and exact targets", authority.get("authority") == authority_expected and authority.get("targetIds") == target_ids and authority.get("acceptedIds") == [] and authority.get("appliedIds") == [] and authority.get("unchanged") is True, authority)
check("decision has no acceptance, application, canonical, GitHub or runtime effects", decision.get("accepted") is False and decision.get("applied") is False and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("canonicalChanges") is False and decision.get("githubChanges") is False and decision.get("sourceProgramsExecuted") is False and decision.get("runtimeExecuted") is False, {k: decision.get(k) for k in ["accepted", "applied", "canonicalChanges", "githubChanges", "sourceProgramsExecuted", "runtimeExecuted"]})
expected_blockers = {"divine-intervention-greater": "MR233-B01", "wish": "MR233-B02"}
decisions = decision.get("perIdentityDecisions", [])
check("per-spell decisions are explicit holds with exact unique blockers", {x.get("id") for x in decisions} == set(target_ids) and len(decisions) == 2 and all(x.get("decision") == "HELD" and x.get("held") is True and x.get("accepted") is False and x.get("applied") is False and x.get("blockerIds") == [expected_blockers[x["id"]]] and bool(x.get("minimumMissingWitness")) for x in decisions), [{k: x.get(k) for k in ["id", "decision", "blockerIds", "minimumMissingWitness"]} for x in decisions])
outer_decisions = delivery.get("decisions", [])
check("delivery decisions mirror the sealed Director decisions", len(outer_decisions) == 2 and {x.get("id") for x in outer_decisions} == set(target_ids) and all(x.get("decision") == "HELD" and x.get("accepted") is False and x.get("applied") is False and x.get("blockerIds") == [expected_blockers[x["id"]]] for x in outer_decisions), outer_decisions)

question_ids = ids(original_questions) + ids(additions)
disposition_ids = ids(questions)
check("24 original questions and two additions are dispositioned once each", len(ids(original_questions)) == 24 and len(ids(additions)) == 2 and len(disposition_ids) == 26 and len(set(disposition_ids)) == 26 and set(disposition_ids) == set(question_ids), {"original": len(ids(original_questions)), "additions": len(ids(additions)), "dispositions": len(disposition_ids)})
check("all four original main obligations remain incomplete and held", len(main_obligations) == 4 and len(main_cases) == 4 and set(ids(main_cases)) == set(ids(main_obligations)) and all(x.get("status") == "HELD-NOT-DEMONSTRATED" and x.get("completeSpellWitness") is False and x.get("actorClockComplete") is False and x.get("blockerIds") == [expected_blockers[x.get("spellId")]] for x in main_cases), [{k: x.get(k) for k in ["id", "status", "blockerIds", "completeSpellWitness", "actorClockComplete"]} for x in main_cases])
check("all eight future requirements remain held without positive witnesses", len(future) == 8 and all(x.get("completePositiveWitness") is False for x in future), {"count": len(future), "positive": [x.get("id") for x in future if x.get("completePositiveWitness") is True]})

components = casebook.get("auditComponents", [])
component_results = integrity.get("caseResults", [])
component_files = {n.removeprefix("component_cases/").removesuffix(".json") for n in names if n.startswith("component_cases/") and n.endswith(".json")}
component_ids = {x.get("id") for x in components}
check("six audit-only components match the archived cases and replay records", len(components) == 6 and component_ids == component_files == {x.get("id") for x in component_results} and all(x.get("completeSpellWitness") is False and x.get("completeActorState") is False and all(e.get("kind") == "audit-classification" for e in x.get("events", [])) for x in components), {"components": len(components), "files": len(component_files), "results": len(component_results)})
check("105 data checks and 12 forward/12 inverse operations pass without gameplay events", integrity.get("checkCount") == 105 and integrity.get("passed") == 105 and integrity.get("failed") == 0 and integrity.get("forwardOperations") == 12 and integrity.get("inverseOperations") == 12 and integrity.get("gameplayEvents") == 0 and integrity.get("completePositiveSpellCases") == 0 and integrity.get("completeActorClockCases") == 0 and all(x.get("passed") is True for x in component_results), {k: integrity.get(k) for k in ["checkCount", "passed", "failed", "forwardOperations", "inverseOperations", "gameplayEvents", "completePositiveSpellCases", "completeActorClockCases"]})
check("clock report claims no complete actor timelines", clock.get("passed") is False and clock.get("completeActorTimelines") == 0 and clock.get("gameplayEvents") == 0, clock)
check("source, data, semantic and packaging totals reconcile with all checks passing", source_verification.get("checkCount") == 1383 and source_verification.get("passed") == 1383 and source_verification.get("failed") == 0 and counts.get("dataChecks") == 105 and counts.get("dataCheckFailures") == 0 and counts.get("semanticCriteria") == 18 and counts.get("semanticPassingCriteria") == 12 and counts.get("semanticBlockedCriteria") == 6 and counts.get("semanticFailedCriteria") == 0 and delivery.get("packageChecks", {}).get("count") == 1430 and delivery.get("packageChecks", {}).get("passed") == 1430 and delivery.get("packageChecks", {}).get("failed") == 0 and all(x.get("passed") is True for x in preseal.get("checks", [])), {"source": [source_verification.get(k) for k in ["checkCount", "passed", "failed"]], "data": [counts.get("dataChecks"), counts.get("dataCheckFailures")], "semantic": [counts.get("semanticCriteria"), counts.get("semanticPassingCriteria"), counts.get("semanticBlockedCriteria"), counts.get("semanticFailedCriteria")], "package": delivery.get("packageChecks", {}).get("count"), "presealFailed": preseal.get("failed")})
check("sealed counts reconcile to the two holds and their preserved review scope", counts.get("targetIdentities") == 2 and counts.get("acceptedIdentities") == 0 and counts.get("heldIdentities") == 2 and counts.get("originalQuestions") == 24 and counts.get("focusedAdditions") == 2 and counts.get("questionDispositions") == 26 and counts.get("requiredMainCases") == 4 and counts.get("completeMainCases") == 0 and counts.get("heldMainCases") == 4 and counts.get("futureRequirements") == 8 and counts.get("auditComponentCases") == 6 and counts.get("forwardOperations") == 12 and counts.get("inverseOperations") == 12 and counts.get("gameplayEvents") == 0 and counts.get("completeActorClockCases") == 0, counts)

packet_finding_check = packet_finding.get("id") == "MR233-E01" and packet_finding.get("status") == "CLOSED_BY_CORRECTED_V2" and packet_finding.get("outstandingBlocker") is False
check("MR233-E01 is closed with no outstanding packet-reference blocker", packet_finding_check and authority.get("packetReferenceFinding") == "MR233-E01-CLOSED" and counts.get("closedPacketFindings") == 1 and counts.get("outstandingPacketFindings") == 0, {"finding": packet_finding.get("status"), "outstanding": packet_finding.get("outstandingBlocker")})
queue_member = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_233.json"
handoff_member = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_233.json"
pending_audit_member = "evidence/current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_233.json"
ref_records = packet_finding.get("references", [])
ref_map = {x.get("field"): x for x in ref_records}
queue = read_json(outer.read(queue_member))
check("corrected packet queue, handoff and pending-audit references exist and match their promised bindings", {"currentQueue", "currentHandoff", "pendingIdentityAudit"} <= set(ref_map) and all(ref_map[k].get("exactNamedMemberPresent") is True and ref_map[k].get("exactPromisedBindingMatches") is True and ("evidence/" + ref_map[k]["includedMember"]) in name_set and record_matches(outer.read("evidence/" + ref_map[k]["includedMember"]), ref_map[k].get("includedBinding", {})) for k in ["currentQueue", "currentHandoff", "pendingIdentityAudit"]), {k: ref_map.get(k, {}).get("includedMember") for k in ["currentQueue", "currentHandoff", "pendingIdentityAudit"]})
check("corrected embedded queue matches the submitted queue and retains 17 groups / all 37 pending IDs", queue_member in name_set and handoff_member in name_set and pending_audit_member in name_set and len(queue.get("currentPendingGroups", [])) == 17 and sum(x.get("pendingCount", 0) for x in queue.get("currentPendingGroups", [])) == 37 and queue.get("currentAuthority") == authority_expected, {"groups": len(queue.get("currentPendingGroups", [])), "pending": sum(x.get("pendingCount", 0) for x in queue.get("currentPendingGroups", [])), "authority": queue.get("currentAuthority")})
with zipfile.ZipFile(SOURCE) as source_zip:
    source_queue_member = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_233.json"
    source_queue_bytes = source_zip.read(source_queue_member)
returned_queue_bytes = outer.read(queue_member)
source_queue_digest = digest(source_queue_bytes)
check("Return233 queue snapshot matches the queue embedded in corrected source Packet233 v2", returned_queue_bytes == source_queue_bytes and all(source_queue_digest.get(k) == ref_map["currentQueue"].get("expected", {}).get(k) for k in ["bytes", "sha256", "crc32"]), source_queue_digest)
source_digest = digest(SOURCE.read_bytes())
source_record = delivery.get("sourceArchive", {})
check("returned corrected source archive binding matches the received local Packet233 v2", record_matches(SOURCE.read_bytes(), source_record) and source_record.get("fileName") == SOURCE.name and source_bindings.get("sourceArchive", {}).get("sha256") == source_digest["sha256"], source_digest)

preserved_expected = {"PC232-B01", "PC232-B02", "AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05", "MF210-B01", "MF210-B02", "IR207-B02", "IE204-B02"}
preserved = {blocker for item in hold_register.get("unrelatedHoldsPreserved", []) for blocker in item.get("blockerIds", [])}
check("all previously held unrelated blocker IDs remain preserved", preserved_expected <= preserved and "AFP211-E01" in hold_register.get("closedOutsideScope", []), {"preserved": sorted(preserved), "closedOutsideScope": hold_register.get("closedOutsideScope")})
next_queue_matches = next_group.get("group") is None and next_group.get("pendingIds") == [] and next_group.get("lastListedGroup") == "rank9-miracle-reality2" and next_group.get("pendingCountUnchanged") == 37 and delivery.get("nextPendingGroup") is None and delivery.get("nextPendingIds") == []
check("director records no following group after final supplied queue row", next_queue_matches, next_group)
check("delivery reports no canonical, GitHub, application or runtime changes", delivery.get("canonicalChanges") is False and delivery.get("githubChanges") is False and delivery.get("sourceProgramsExecuted") is False and delivery.get("runtimeExecuted") is False, {k: delivery.get(k) for k in ["canonicalChanges", "githubChanges", "sourceProgramsExecuted", "runtimeExecuted"]})

failures = [x for x in checks if not x["passed"]]
report = {
    "id": "RANK9MIRACLEREALITY2-RETURN233-INDEPENDENT-AUDIT",
    "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS" if not failures else "FAIL",
    "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
    "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
    "sourceArchive": {"path": SOURCE.relative_to(ROOT).as_posix(), **source_digest},
    "authority": delivery.get("authority"),
    "heldIds": delivery.get("heldIds"),
    "blockerIds": expected_blockers,
    "nextGroup": next_group,
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
    "checks": checks,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {
    "id": "RANK9MIRACLEREALITY2-RETURN233-RECEIPT",
    "status": report["status"],
    "archive": report["archive"],
    "delivery": report["delivery"],
    "sourceArchive": report["sourceArchive"],
    "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())},
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": report["checkCount"], "passedChecks": report["passedChecks"], "failedChecks": report["failedChecks"], "failures": failures, "archiveSha256": archive_digest["sha256"]}, ensure_ascii=False, indent=2))
