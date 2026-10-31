#!/usr/bin/env python3
"""Read-only independent audit of director Return232 and its source evidence."""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import zlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_projectionconfinement2_return232_received"
ARCHIVE = RECEIVED / "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json"
REPORT = BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json"

checks: list[dict] = []


def digest(data: bytes) -> dict:
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}",
    }


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def read_json(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def sha_matches(data: bytes, record: dict) -> bool:
    actual = digest(data)
    return all(actual.get(k) == record.get(k) for k in ("bytes", "sha256")) and (
        record.get("crc32") is None or actual["crc32"] == record.get("crc32")
    )


def ids_of(items) -> list[str]:
    if isinstance(items, list):
        return [x.get("id") for x in items if isinstance(x, dict) and x.get("id")]
    if isinstance(items, dict):
        return [x.get("id") for x in items.values() if isinstance(x, dict) and x.get("id")]
    return []


def safe_member(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_digest = digest(archive_bytes)
check("outer delivery archive size, SHA-256 and CRC32 match", sha_matches(archive_bytes, delivery["archive"]), archive_digest)
check("delivery names the exact received archive", delivery["archive"].get("fileName") == ARCHIVE.name, delivery["archive"].get("fileName"))
check("delivery identity and authority remain current", delivery.get("id") == "RANK9-PROJECTION-CONFINEMENT2-DIRECTOR-RETURN232-DELIVERY" and delivery.get("authority") == {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}, delivery.get("authority"))
check("delivery holds exactly the two scoped identities", delivery.get("heldIds") == ["astral-projection", "imprisonment"] and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("accepted") is False and delivery.get("applied") is False, {"heldIds": delivery.get("heldIds"), "acceptedIds": delivery.get("acceptedIds"), "appliedIds": delivery.get("appliedIds")})

outer = zipfile.ZipFile(io.BytesIO(archive_bytes))
names = outer.namelist()
name_set = set(names)
check("archive has unique, safe, regular member paths", len(names) == len(name_set) and all(safe_member(n) for n in names) and all(not i.is_dir() for i in outer.infolist()), {"members": len(names), "unique": len(name_set)})
delivery_members = delivery.get("members", [])
delivery_by_path = {x.get("path"): x for x in delivery_members if isinstance(x, dict)}
check("delivery allowlist exactly matches archive member names", set(delivery_by_path) == name_set and len(delivery_by_path) == len(delivery_members) == delivery.get("memberCount"), {"actual": len(names), "delivery": len(delivery_members), "memberCount": delivery.get("memberCount")})

member_failures = []
for name in names:
    data = outer.read(name)
    expected = delivery_by_path.get(name)
    if expected is None or not sha_matches(data, expected):
        member_failures.append(name)
check("every archive member matches the exact external delivery allowlist", not member_failures, member_failures[:20])

internal_manifest_bytes = outer.read("MEMBER_MANIFEST.json")
internal_manifest = read_json(internal_manifest_bytes)
check("internal member manifest is itself bound by delivery", sha_matches(internal_manifest_bytes, delivery.get("memberManifest", {})) and delivery.get("memberManifest", {}).get("path") == "MEMBER_MANIFEST.json", digest(internal_manifest_bytes))
payload_members = internal_manifest.get("members", [])
payload_by_path = {x.get("path"): x for x in payload_members if isinstance(x, dict)}
check("internal manifest covers every non-manifest archive member", set(payload_by_path) == (name_set - {"MEMBER_MANIFEST.json"}) and len(payload_by_path) == len(payload_members) == delivery.get("payloadCount"), {"actualPayload": len(name_set - {"MEMBER_MANIFEST.json"}), "listed": len(payload_members), "payloadCount": delivery.get("payloadCount")})
internal_failures = []
for name, expected in payload_by_path.items():
    if name not in name_set or not sha_matches(outer.read(name), expected):
        internal_failures.append(name)
check("every payload member matches the embedded member manifest", not internal_failures, internal_failures[:20])

def obj(name: str):
    return read_json(outer.read(name))


decision = obj("DIRECTOR_DECISION.json")
authority = obj("CURRENT_AUTHORITY.json")
counts = obj("COUNTS.json")
procedures = obj("PROCEDURES.json")
questions = obj("QUESTION_DISPOSITIONS.json")
original_questions = obj("ORIGINAL_QUESTIONS.json")
focused = obj("FOCUSED_ADDITIONS.json")
main_cases = obj("MAIN_CASE_DISPOSITIONS.json")
main_obligations = obj("ORIGINAL_MAIN_CASE_OBLIGATIONS.json")
future_cases = obj("FUTURE_CASE_DISPOSITIONS.json")
integrity = obj("DATA_INTEGRITY_AND_REPLAY.json")
casebook = obj("CASEBOOK.json")
clock = obj("CLOCK_CHECK.json")
source_bindings = obj("SOURCE_BINDINGS.json")
source_reconciliation = obj("SOURCE_RECONCILIATION.json")
source_verification = obj("SOURCE_VERIFICATION.json")
hold_register = obj("HOLD_REGISTER.json")
preseal = obj("PRESEAL_CHECK.json")
next_group = obj("NEXT_GROUP.json")

target_ids = ["astral-projection", "imprisonment"]
check("decision and current-authority records agree on exact targets and no prior ruling", decision.get("priorDirectorRuling") is None and authority.get("noPriorDirectorRuling") is True and authority.get("targetIds") == target_ids and authority.get("acceptedIds") == [] and authority.get("appliedIds") == [] and authority.get("unchanged") is True, authority)
check("director decision has no acceptance, application, canonical, GitHub or runtime effects", decision.get("accepted") is False and decision.get("applied") is False and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("canonicalChanges") is False and decision.get("githubChanges") is False and decision.get("sourceProgramsExecuted") is False and decision.get("runtimeExecuted") is False, {k: decision.get(k) for k in ["accepted", "applied", "canonicalChanges", "githubChanges", "sourceProgramsExecuted", "runtimeExecuted"]})
decisions = decision.get("perIdentityDecisions", [])
expected_blockers = {"astral-projection": "PC232-B01", "imprisonment": "PC232-B02"}
check("per-identity decisions are exactly the two explicit holds", {x.get("id") for x in decisions} == set(target_ids) and len(decisions) == 2 and all(x.get("decision") == "HELD" and x.get("held") is True and x.get("accepted") is False and x.get("applied") is False and x.get("blockerIds") == [expected_blockers[x["id"]]] for x in decisions), [{k: x.get(k) for k in ["id", "decision", "accepted", "applied", "blockerIds", "minimumMissingWitness"]} for x in decisions])
delivery_decisions = delivery.get("decisions", [])
check("outer delivery decisions exactly mirror the director ruling", len(delivery_decisions) == 2 and {x.get("id") for x in delivery_decisions} == set(target_ids) and all(x.get("decision") == "HELD" and x.get("accepted") is False and x.get("applied") is False and x.get("blockerIds") == [expected_blockers[x["id"]]] for x in delivery_decisions), [{k: x.get(k) for k in ["id", "decision", "accepted", "applied", "blockerIds"]} for x in delivery_decisions])
qualification_ids = [f"PC232-Q{i:02d}" for i in range(1, 8)]
check("both target decisions preserve the seven explicit qualifications", all(x.get("qualificationIds") == qualification_ids for x in decisions), {x.get("id"): x.get("qualificationIds") for x in decisions})
check("procedure mirror keeps both spells held and operationally incomplete", {x.get("id") for x in procedures} == set(target_ids) and all(x.get("accepted") is False and x.get("applied") is False and x.get("held") is True and x.get("completeOperationalProcedure") is False and x.get("blockerIds") == [expected_blockers[x["id"]]] for x in procedures), [{k: x.get(k) for k in ["id", "held", "completeOperationalProcedure", "blockerIds"]} for x in procedures])

question_ids = ids_of(original_questions) + ids_of(focused)
question_disposition_ids = ids_of(questions)
check("all 24 original questions and both focused additions are dispositioned exactly once", len(ids_of(original_questions)) == 24 and len(ids_of(focused)) == 2 and len(question_disposition_ids) == 26 and len(set(question_disposition_ids)) == 26 and set(question_disposition_ids) == set(question_ids), {"original": len(ids_of(original_questions)), "additions": len(ids_of(focused)), "dispositions": len(question_disposition_ids)})
check("question dispositions do not auto-adopt historical recommendations", all(x.get("historicalRecommendationAdoptedAutomatically") is False for x in questions), {"unexpected": [x.get("id") for x in questions if x.get("historicalRecommendationAdoptedAutomatically") is not False]})
main_ids = ids_of(main_obligations)
check("four unchanged main obligations all remain incomplete holds", len(main_obligations) == 4 and len(main_cases) == 4 and set(ids_of(main_cases)) == set(main_ids) and all(x.get("status") == "HELD-NOT-DEMONSTRATED" and x.get("accepted") is False and x.get("applied") is False and x.get("completeSpellWitness") is False and x.get("actorClockComplete") is False for x in main_cases), {"obligations": len(main_obligations), "mainCases": [{k: x.get(k) for k in ["id", "status", "completeSpellWitness", "actorClockComplete"]} for x in main_cases]})
check("eight future requirements remain preserved without positive witnesses", len(future_cases) == 8 and all(x.get("completePositiveWitness") is False for x in future_cases), [{k: x.get(k) for k in ["id", "status", "completePositiveWitness", "blockerIds"]} for x in future_cases])

audit_components = casebook.get("auditComponents", [])
case_results = integrity.get("caseResults", [])
component_ids = {x.get("id") for x in audit_components if isinstance(x, dict)}
result_ids = {x.get("id") for x in case_results if isinstance(x, dict)}
case_files = {n.removeprefix("component_cases/").removesuffix(".json") for n in names if n.startswith("component_cases/") and n.endswith(".json")}
check("eight audit-only component cases match case files and replay results", len(audit_components) == 8 and len(case_files) == 8 and component_ids == case_files == result_ids and all(x.get("kind") == "reversible-source-audit-component" and x.get("completeSpellWitness") is False and x.get("completeActorState") is False for x in audit_components), {"components": len(audit_components), "files": len(case_files), "results": len(case_results)})
check("all component forward/inverse operations pass without gameplay events", integrity.get("checkCount") == 129 and integrity.get("passed") == 129 and integrity.get("failed") == 0 and len(case_results) == 8 and all(x.get("passed") is True and x.get("completeSpellWitness") is False and x.get("forwardOperations") == 2 and x.get("inverseOperations") == 2 for x in case_results) and integrity.get("forwardOperations") == 16 and integrity.get("inverseOperations") == 16 and integrity.get("gameplayEvents") == 0 and integrity.get("completePositiveSpellCases") == 0 and integrity.get("clockCertifiedCases") == 0, {k: integrity.get(k) for k in ["checkCount", "passed", "failed", "auditComponentCases", "auditEvents", "forwardOperations", "inverseOperations", "gameplayEvents", "completePositiveSpellCases", "clockCertifiedCases"]})
check("actor-clock report does not claim complete timelines", clock.get("passed") is False and clock.get("completeActorTimelines") == 0 and clock.get("gameplayEvents") == 0 and clock.get("noUniversalAstralClockSelected") is True, clock)

binding_records = source_bindings.get("currentSourceFiles", [])
refresh_records = source_reconciliation.get("refresh", [])
source_archive_path = BASE / "rank9_projectionconfinement2_current_source_232_prepared/DD_Rank9_ProjectionConfinement2_CurrentSource_232.zip"
source_delivery_path = "evidence/packet232/DD_Rank9_ProjectionConfinement2_CurrentSource_232_DELIVERY.json"
nested_source_zip_bytes = source_archive_path.read_bytes()
nested_source_delivery = read_json(outer.read(source_delivery_path))
source_delivery_local = read_json((BASE / "rank9_projectionconfinement2_current_source_232_prepared/DD_Rank9_ProjectionConfinement2_CurrentSource_232_DELIVERY.json").read_bytes())
check("original audited packet232 source ZIP matches its embedded and local DELIVERY manifests", sha_matches(nested_source_zip_bytes, nested_source_delivery.get("archive", {})) and sha_matches(nested_source_zip_bytes, source_bindings.get("sourceArchive", {})) and nested_source_delivery == source_delivery_local and pathlib.PurePosixPath(nested_source_delivery.get("archive", {}).get("path", "")).name == "DD_Rank9_ProjectionConfinement2_CurrentSource_232.zip", digest(nested_source_zip_bytes))
packet_audit_local = (BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_232_INDEPENDENT_AUDIT.json").read_bytes()
packet_receipt_local = (BASE / "RANK9PROJECTIONCONFINEMENT2_PACKET_232_RECEIPT.json").read_bytes()
check("submitted packet audit and receipt are preserved byte-exactly in Return232", outer.read("evidence/packet232/RANK9PROJECTIONCONFINEMENT2_PACKET_232_INDEPENDENT_AUDIT.json") == packet_audit_local and outer.read("evidence/packet232/RANK9PROJECTIONCONFINEMENT2_PACKET_232_RECEIPT.json") == packet_receipt_local, {"auditBytes": len(packet_audit_local), "receiptBytes": len(packet_receipt_local)})
nested_source = zipfile.ZipFile(io.BytesIO(nested_source_zip_bytes))
nested_source_names = set(nested_source.namelist())
source_failures = []
for rec in binding_records:
    member = rec.get("returnMember") if rec.get("embedded") else None
    if member:
        source_member = rec.get("archiveMember")
        if member not in name_set or not sha_matches(outer.read(member), rec):
            source_failures.append(rec.get("path"))
    else:
        member = rec.get("archiveMember")
        if member not in nested_source_names or not sha_matches(nested_source.read(member), rec):
            source_failures.append(rec.get("path"))
check("all 135 current source bindings resolve to exact raw bytes in the sealed evidence", len(binding_records) == 135 and not source_failures, {"bindings": len(binding_records), "failures": source_failures[:20]})
unembedded_bindings = sum(1 for x in binding_records if x.get("embedded") is False)
check("nine program/source bindings remain explicitly external to the return ZIP and are bound to the attached source packet", unembedded_bindings == len(delivery.get("externalSourceEvidence", [])) == 9 and all(x.get("embedded") is False and x.get("sourceArchive", {}).get("sha256") == source_bindings.get("sourceArchive", {}).get("sha256") for x in delivery.get("externalSourceEvidence", [])), {"unembeddedBindings": unembedded_bindings, "externalEvidenceRows": len(delivery.get("externalSourceEvidence", []))})
classification_counts = source_reconciliation.get("classificationCounts", {})
classifications = {k: sum(1 for x in refresh_records if x.get("classification") == k) for k in ["raw-exact", "line-ending-only", "changed-current-authority-or-content"]}
check("135 refreshed historical bindings reconcile as 39 raw, 95 line-ending-only and one refreshed index", len(refresh_records) == 135 and classifications == {"raw-exact": 39, "line-ending-only": 95, "changed-current-authority-or-content": 1} and classification_counts == classifications and [x.get("path") for x in refresh_records if x.get("classification") == "changed-current-authority-or-content"] == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"], classifications)
source_failures = []
for rec in refresh_records:
    binding = next((x for x in binding_records if x.get("path") == rec.get("path")), None)
    if not binding or any(binding.get(k) != rec.get("currentBinding", {}).get(k) for k in ["path", "bytes", "sha256", "gitBlobSHA1"]):
        source_failures.append(rec.get("path"))
check("source refresh ledger agrees with the raw binding inventory", len(refresh_records) == 135 and not source_failures, source_failures[:20])

comparators = obj("CURRENT_COMPARISON_BOUNDARIES.json")
reconciled_comparators = [x for x in comparators if x.get("acceptedEnvelopeReconciliation")]
comparator_failures = []
for item in reconciled_comparators:
    path = item.get("procedureSourcePath", "")
    current_path = "evidence/sources_current/" + path
    indexed_path = "evidence/indexed_accepted_bytes/" + path
    current = outer.read(current_path)
    indexed = outer.read(indexed_path)
    info = item["acceptedEnvelopeReconciliation"]["indexedBinding"]
    if digest(indexed)["bytes"] != info.get("bytes") or digest(indexed)["sha256"] != info.get("sha256") or current.replace(b"\r\n", b"\n") != indexed or item["acceptedEnvelopeReconciliation"].get("LFNormalizationMatchesExactIndexedBytes") is not True:
        comparator_failures.append(path)
check("six accepted comparator files match indexed accepted bytes after CRLF normalization", len(reconciled_comparators) == 6 and not comparator_failures, comparator_failures)
check("source and data audits report their complete passing totals", source_verification.get("checkCount") == 1215 and source_verification.get("passed") == 1215 and source_verification.get("failed") == 0 and source_verification.get("sourceProgramsExecuted") is False, {k: source_verification.get(k) for k in ["checkCount", "passed", "failed", "sourceProgramsExecuted"]})
check("preseal and package checks report no failures", preseal.get("count") == 179 and preseal.get("failed") == 0 and all(x.get("passed") is True for x in preseal.get("checks", [])) and delivery.get("packageChecks", {}).get("failed") == 0 and delivery.get("packageChecks", {}).get("passed") == 1268, {"preseal": preseal.get("count"), "presealFailed": preseal.get("failed"), "package": delivery.get("packageChecks")})

expected_unrelated = {"AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05", "MF210-B01", "MF210-B02", "IR207-B02", "IE204-B02"}
check("prior blockers and closed AFP211-E01 remain unchanged", set(hold_register.get("unrelatedHoldsPreserved", [])) == expected_unrelated and hold_register.get("closedOutsideScope") == ["AFP211-E01"], {"preserved": hold_register.get("unrelatedHoldsPreserved"), "closed": hold_register.get("closedOutsideScope")})
check("next group is exactly the current pending Miracle/Reality pair", next_group.get("group") == "rank9-miracle-reality2" and next_group.get("pendingIds") == ["divine-intervention-greater", "wish"] and delivery.get("nextPendingGroup") == next_group.get("group") and delivery.get("nextPendingIds") == next_group.get("pendingIds"), next_group)
check("held counts and full-return counts reconcile", counts.get("targetIdentities") == 2 and counts.get("acceptedIdentities") == 0 and counts.get("heldIdentities") == 2 and counts.get("nativePlacements") == 6 and counts.get("classAccessRows") == 8 and counts.get("sourceBindings") == 135 and counts.get("originalQuestions") == 24 and counts.get("focusedAdditions") == 2 and counts.get("questionDispositions") == 26 and counts.get("requiredMainCases") == 4 and counts.get("completeMainCases") == 0 and counts.get("heldMainCases") == 4 and counts.get("futureRequirements") == 8 and counts.get("auditComponentCases") == 8 and counts.get("forwardOperations") == 16 and counts.get("inverseOperations") == 16, counts)

failures = [x for x in checks if not x["passed"]]
report = {
    "id": "RANK9PROJECTIONCONFINEMENT2-RETURN232-INDEPENDENT-AUDIT",
    "checkedAtUtc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    "status": "PASS" if not failures else "FAIL",
    "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
    "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
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
report_bytes = REPORT.read_bytes()
receipt = {
    "id": "RANK9PROJECTIONCONFINEMENT2-RETURN232-RECEIPT",
    "status": report["status"],
    "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
    "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
    "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(report_bytes)},
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": report["checkCount"], "passedChecks": report["passedChecks"], "failedChecks": report["failedChecks"], "failures": [x for x in failures], "archiveSha256": archive_digest["sha256"]}, ensure_ascii=False, indent=2))
