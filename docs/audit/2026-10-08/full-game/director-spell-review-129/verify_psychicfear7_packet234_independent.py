#!/usr/bin/env python3
"""Independently verify Packet234, its manifest, current snapshot and history."""
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
OUT = BASE / "rank9_psychicfear7_current_source_234_prepared"
ARCHIVE = OUT / "DD_Rank9_PsychicFear7_CurrentSource_234.zip"
DELIVERY = OUT / "DD_Rank9_PsychicFear7_CurrentSource_234_DELIVERY.json"
AUDIT = BASE / "RANK9PSYCHICFEAR7_PACKET234_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9PSYCHICFEAR7_PACKET234_RECEIPT.json"
SOURCE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_01.json"
SOURCE_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Psychic_Fear_7_Source_Conference_01.zip"
PRIOR_RETURN216 = BASE / "rank9_psychicfear7_return216_received/DD_Rank9_PsychicFear3_Director_Return216_HELD.zip"
PRIOR_PACKET215 = BASE / "rank9_psychicfear7_source_packet_215/DD_Rank9_PsychicFear7_CurrentSource_215.zip"
CURRENT_SOURCE_PATHS = {
    "index": "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "catalog": "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "access": "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json",
}
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
RETURN_INFO = {
    228: ("rank9_impactexile4_return228_received", "DD_Rank9_ImpactExile1_Director_Return228.zip", "DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN228_RECEIPT.json"),
    229: ("rank9_illusionreality5_return229_received", "DD_Rank9_IllusionReality1_Director_Return229.zip", "DD_Rank9_IllusionReality1_Director_Return229_DELIVERY.json", "RANK9ILLUSIONREALITY5_RETURN229_INDEPENDENT_AUDIT.json", "RANK9ILLUSIONREALITY5_RETURN229_RECEIPT.json"),
    230: ("rank9_materialforging2_return230_received", "DD_Rank9_MaterialForging2_Director_Return230.zip", "DD_Rank9_MaterialForging2_Director_Return230_DELIVERY.json", "RANK9MATERIALFORGING2_RETURN230_INDEPENDENT_AUDIT.json", "RANK9MATERIALFORGING2_RETURN230_RECEIPT.json"),
    231: ("rank9_alignment_faction_purification5_return231_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return231_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN231_RECEIPT.json"),
    232: ("rank9_projectionconfinement2_return232_received", "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip", "DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json", "RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json", "RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json"),
    233: ("rank9_miraclereality2_return233_received", "DD_Rank9_MiracleReality2_Director_Return233_HELD.zip", "DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json", "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json", "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json"),
}

checks: list[dict] = []


def digest(data: bytes) -> dict:
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}"}


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def read_json(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def matches(data: bytes, record: dict) -> bool:
    got = digest(data)
    return all(got.get(k) == record.get(k) for k in ("bytes", "sha256")) and (record.get("crc32") is None or got["crc32"] == record["crc32"])


def safe_path(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_digest = digest(archive_bytes)
check("archive byte count, SHA-256 and CRC32 match DELIVERY", matches(archive_bytes, delivery.get("archive", {})), archive_digest)
check("delivery names exact Packet234 archive and scope", pathlib.PurePosixPath(delivery.get("archive", {}).get("path", "")).name == ARCHIVE.name and delivery.get("group") == "rank9-psychic-fear7" and delivery.get("targetIds") == TARGETS, {k: delivery.get(k) for k in ["group", "targetIds"]})
check("delivery binds exact 811/37/0 and 535/173 authority", delivery.get("authority") == AUTHORITY and delivery.get("accepted") is False and delivery.get("applied") is False, delivery.get("authority"))

outer = zipfile.ZipFile(io.BytesIO(archive_bytes))
names = outer.namelist()
name_set = set(names)
external_members = delivery.get("members", [])
external_by_path = {m.get("path"): m for m in external_members if isinstance(m, dict)}
check("ZIP has unique safe paths and no directory entries", len(names) == len(name_set) and all(safe_path(n) for n in names) and all(not i.is_dir() for i in outer.infolist()), {"members": len(names), "unique": len(name_set)})
check("delivery allowlist exactly covers every archive member", set(external_by_path) == name_set and len(external_by_path) == delivery.get("memberCount") == len(names) and delivery.get("payloadCount") == len(names) - 1, {"members": len(names), "delivery": len(external_by_path)})
member_failures = [n for n in names if n not in external_by_path or not matches(outer.read(n), external_by_path[n])]
check("all archive members match external byte/SHA/CRC bindings", not member_failures, member_failures[:20])
manifest_bytes = outer.read("MANIFEST.json")
manifest = read_json(manifest_bytes)
check("embedded manifest is bound by delivery", matches(manifest_bytes, delivery.get("memberManifest", {})) and delivery.get("memberManifest", {}).get("path") == "MANIFEST.json", digest(manifest_bytes))
manifest_rows = manifest.get("members", [])
manifest_by_path = {m.get("path"): m for m in manifest_rows if isinstance(m, dict)}
check("internal manifest exactly covers all payload members", set(manifest_by_path) == name_set - {"MANIFEST.json"} and len(manifest_rows) == delivery.get("payloadCount"), {"manifest": len(manifest_rows), "archivePayload": len(name_set)-1})
manifest_failures = [n for n, rec in manifest_by_path.items() if not matches(outer.read(n), rec)]
check("all payload members match internal manifest", not manifest_failures, manifest_failures[:20])

context = read_json(outer.read("CURRENT_CONTEXT_234.json"))
candidate = read_json(outer.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_234.json"))
embedded_request = outer.read("REQUEST_234.txt").decode("utf-8")
check("current context identifies only GPT-selected psychic/fear identities", context.get("targetGroup") == {"group": "rank9-psychic-fear7", "pendingIds": TARGETS, "count": 3} and candidate.get("currentPendingGroup", {}).get("spellIds") == TARGETS, context.get("targetGroup"))
check("context and candidate bind exact current authority and main base", context.get("currentAuthority") == AUTHORITY and candidate.get("currentAuthority") == AUTHORITY and delivery.get("sourceCommitBase") == candidate.get("sourceCommitBase") and delivery.get("sourceBranch") == "main", {"authority": context.get("currentAuthority"), "base": delivery.get("sourceCommitBase"), "branch": delivery.get("sourceBranch")})
check("request scopes only three identities and preserves explicit exclusions", all(sid in embedded_request for sid in TARGETS) and "Review ONLY psychic-scream, mass-phantom-killer and weird" in embedded_request and "Do not edit canonical/runtime/GitHub files" in embedded_request, embedded_request[:800])
check("prior 806/42/0 blockers are marked historical for reassessment", candidate.get("priorDirectorDecision216", {}).get("acceptedIds") == [] and {x.get("id") for x in candidate.get("priorBlockersForFreshReassessment", [])} == {"PF182-B01", "PF182-B02"} and "not an automatic current ruling" in " ".join(x.get("currentAuthorityDisposition", "") for x in candidate.get("targetRecords", [])), {"priorBlockerIds": [x.get("id") for x in candidate.get("priorBlockersForFreshReassessment", [])]})
check("previous questions, selected dispositions, obligations and cases are preserved", len(candidate.get("originalQuestionsUnchanged", [])) == 23 and len(candidate.get("targetRelevantOriginalQuestionIds", [])) == 13 and len(candidate.get("focusedAdditionalQuestionsUnchanged", [])) == 2 and len(candidate.get("priorSelectedQuestionDispositions", [])) == 15 and len(candidate.get("priorTargetMainCaseObligations", [])) == 6 and candidate.get("priorReturn216Counts", {}).get("preservedCases") == 47 and candidate.get("priorReturn216Counts", {}).get("heldCases") == 4, {k: candidate.get(k) if not isinstance(candidate.get(k), list) else len(candidate.get(k)) for k in ["originalQuestionsUnchanged", "targetRelevantOriginalQuestionIds", "focusedAdditionalQuestionsUnchanged", "priorSelectedQuestionDispositions", "priorTargetMainCaseObligations"]})
check("candidate lists exactly the three target records with current index/catalog values", {x.get("spellId") for x in candidate.get("targetRecords", [])} == set(TARGETS) and {x.get("spellId") for x in candidate.get("currentTargets", [])} == set(TARGETS) and all(x.get("currentIndexEntry", {}).get("authoredStatus") == "pending-authored-procedure" and x.get("currentCatalogCard", {}).get("id") == x.get("spellId") for x in candidate.get("currentTargets", [])), [x.get("spellId") for x in candidate.get("targetRecords", [])])

queue_member = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_234.json"
handoff_member = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_234.json"
pending_member = "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_234.json"
queue_snapshot = read_json(outer.read(queue_member))
handoff_snapshot = read_json(outer.read(handoff_member))
pending_snapshot = read_json(outer.read(pending_member))
check("context’s queue, handoff and pending-audit bindings resolve to exact archived snapshots", all(context.get(k, {}).get("sha256") == digest(outer.read(member))["sha256"] and context.get(k, {}).get("bytes") == len(outer.read(member)) for k, member in [("currentQueue", queue_member), ("currentHandoff", handoff_member), ("pendingIdentityAudit", pending_member)]), {"queue": digest(outer.read(queue_member)), "handoff": digest(outer.read(handoff_member)), "pending": digest(outer.read(pending_member))})
check("embedded queue and pending audit preserve all 37 pending identities and 17 groups", queue_snapshot.get("currentAuthority") == AUTHORITY and len(queue_snapshot.get("currentPendingGroups", [])) == 17 and sum(g.get("pendingCount", 0) for g in queue_snapshot.get("currentPendingGroups", [])) == 37 and pending_snapshot.get("pendingCount") == 37 and len(pending_snapshot.get("pendingIds", [])) == 37 and pending_snapshot.get("authority") == AUTHORITY, {"groups": len(queue_snapshot.get("currentPendingGroups", [])), "queuePending": sum(g.get("pendingCount", 0) for g in queue_snapshot.get("currentPendingGroups", [])), "auditPending": pending_snapshot.get("pendingCount")})
selected_queue_row = next((x for x in queue_snapshot.get("currentPendingGroups", []) if x.get("group") == "rank9-psychic-fear7"), {})
check("queue target row reflects corrected Return216 history and GPT’s Packet234 priority", selected_queue_row.get("pendingIds") == TARGETS and selected_queue_row.get("historicalPhase") == "prior-director-return-216-held" and "GPT confirmed" in selected_queue_row.get("directorPriority", "") and queue_snapshot.get("next", {}).get("group") == "rank9-psychic-fear7", selected_queue_row)
check("Return233 is recorded as latest completed held batch with its audit receipt", queue_snapshot.get("lastReviewedBatch", {}).get("group") == "rank9-miracle-reality2" and queue_snapshot.get("lastReviewedBatch", {}).get("heldIds") == ["divine-intervention-greater", "wish"] and pending_snapshot.get("lastDirectorReturn", {}).get("heldIds") == ["divine-intervention-greater", "wish"], queue_snapshot.get("lastReviewedBatch"))

index = read_json(outer.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
catalog = read_json(outer.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
index_entries = {x.get("id"): x for x in index.get("entries", [])}
catalog_spells = {x.get("id"): x for x in catalog.get("spells", [])}
pending_ids = {x.get("id") for x in index.get("entries", []) if x.get("authoredStatus") == "pending-authored-procedure"}
check("current archived index and catalog retain all three pending IDs exactly", set(TARGETS) <= pending_ids and all(index_entries[sid].get("sourceStatus") == "blocked-pending-operational-review" and sid in catalog_spells for sid in TARGETS) and index.get("authoredCounts") == {"reviewed": 811, "pending": 37}, {"pendingCount": len(pending_ids), "targets": {sid: index_entries.get(sid, {}).get("authoredStatus") for sid in TARGETS}})

source_bindings = candidate.get("sourceBindings", [])
source_failures = []
for binding in source_bindings:
    member = "sources_current/" + binding["path"]
    if member not in name_set or not matches(outer.read(member), binding):
        source_failures.append(binding.get("path"))
check("all 84 refreshed historical source bindings match archived current-source bytes", len(source_bindings) == 84 and not source_failures, {"bindings": len(source_bindings), "failures": source_failures[:20], "changed": len(candidate.get("sourceBindingRefresh", {}).get("changedHistoricalBindings", []))})
old_candidate = read_json(outer.read("evidence/PSYCHIC_FEAR_SOURCE_CANDIDATE_01.json"))
check("historical candidate and conference archive are preserved byte-exactly", outer.read("evidence/PSYCHIC_FEAR_SOURCE_CANDIDATE_01.json") == SOURCE_CANDIDATE.read_bytes() and outer.read("evidence/PSYCHIC_FEAR_SOURCE_CONFERENCE_01.zip") == SOURCE_ARCHIVE.read_bytes() and len(old_candidate.get("records", [])) == 7, {"records": len(old_candidate.get("records", [])), "sourceBindings": len(old_candidate.get("sourceBindings", []))})

prior_packet_bytes = outer.read("evidence/PACKET215.zip")
prior_packet_delivery = read_json(outer.read("evidence/PACKET215_DELIVERY.json"))
check("historical Packet215 archive matches its preserved delivery and remains labeled historical", digest(prior_packet_bytes)["bytes"] == prior_packet_delivery.get("bytes") and digest(prior_packet_bytes)["sha256"] == prior_packet_delivery.get("sha256") and digest(prior_packet_bytes)["crc32"] == prior_packet_delivery.get("crc32") and prior_packet_delivery.get("authority", {}).get("reviewedApplied") == 806, {"bytes": len(prior_packet_bytes), "authority": prior_packet_delivery.get("authority")})
prior_manifest = outer.read("evidence/return216_excerpt/EXCERPT_MANIFEST.json")
excerpt = read_json(prior_manifest)
prior_zip = zipfile.ZipFile(PRIOR_RETURN216)
excerpt_failures = [row["path"] for row in excerpt.get("membersCopiedByteExactFromOriginalArchive", []) if row["path"] not in prior_zip.namelist() or not matches(outer.read("evidence/return216_excerpt/" + row["path"]), row) or outer.read("evidence/return216_excerpt/" + row["path"]) != prior_zip.read(row["path"])]
check("Return216 excerpt members are byte-exact to the bound original archive", not excerpt_failures and excerpt.get("originalArchive", {}).get("sha256") == hashlib.sha256(PRIOR_RETURN216.read_bytes()).hexdigest(), {"copied": len(excerpt.get("membersCopiedByteExactFromOriginalArchive", [])), "failures": excerpt_failures[:20]})
check("prior Return216 decision, blockers and audit are preserved exactly", outer.read("evidence/return216_excerpt/DIRECTOR_DECISION_216.json") == (BASE / "rank9_psychicfear7_return216_received/DIRECTOR_DECISION_216.json").read_bytes() and outer.read("evidence/return216_excerpt/BLOCKERS_216.json") == (BASE / "rank9_psychicfear7_return216_received/BLOCKERS_216.json").read_bytes() and outer.read("evidence/return216_excerpt/INDEPENDENT_AUDIT.json") == (BASE / "rank9_psychicfear7_return216_received/RETURN216_INDEPENDENT_AUDIT.json").read_bytes(), {"blockers": [x.get("id") for x in read_json(outer.read("evidence/return216_excerpt/BLOCKERS_216.json"))]})

recent_failures = []
for number, (folder, archive_name, delivery_name, audit_name, receipt_name) in RETURN_INFO.items():
    received = BASE / folder
    zip_member = f"evidence/RETURN{number}.zip"
    delivery_member = f"evidence/RETURN{number}_DELIVERY.json"
    for local_path, member in [(received / archive_name, zip_member), (received / delivery_name, delivery_member),
                               (BASE / audit_name, f"current/evidence/RETURN{number}_INDEPENDENT_AUDIT.json"),
                               (BASE / receipt_name, f"current/evidence/RETURN{number}_RECEIPT.json")]:
        if member not in name_set or outer.read(member) != local_path.read_bytes():
            recent_failures.append({"return": number, "member": member, "local": str(local_path)})
check("Returns228–233 ZIPs, delivery manifests, independent audits and receipts are preserved byte-exactly", not recent_failures, recent_failures[:20])

check("Packet234 declares no acceptance, application, canonical, runtime or GitHub changes", delivery.get("accepted") is False and delivery.get("applied") is False and delivery.get("canonicalChanges") is False and delivery.get("applicationChanges") is False and delivery.get("runtimeExecuted") is False and delivery.get("githubChanges") is False, {k: delivery.get(k) for k in ["accepted", "applied", "canonicalChanges", "applicationChanges", "runtimeExecuted", "githubChanges"]})

failures = [x for x in checks if not x["passed"]]
report = {"id": "RANK9PSYCHICFEAR7-PACKET234-INDEPENDENT-AUDIT", "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest},
          "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())}, "authority": AUTHORITY,
          "group": "rank9-psychic-fear7", "targetIds": TARGETS, "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "checks": checks}
AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9PSYCHICFEAR7-PACKET234-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"],
           "independentAudit": {"path": AUDIT.relative_to(ROOT).as_posix(), **digest(AUDIT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": report["checkCount"], "passedChecks": report["passedChecks"], "failedChecks": report["failedChecks"], "failures": failures, "archiveSha256": archive_digest["sha256"]}, ensure_ascii=False, indent=2))
