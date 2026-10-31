#!/usr/bin/env python3
"""Independent integrity and decision audit of Director Return289."""
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
RECEIVED = BASE / "rank9_miraclereality2_return289_received"
ARCHIVE = RECEIVED / "DD_Rank9_MiracleReality2_Director_Return289_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_MiracleReality2_Director_Return289_HELD_DELIVERY.json"
SOURCE = BASE / "rank9_miraclereality2_current_source_289_prepared/DD_Rank9_MiracleReality2_CurrentSource_289.zip"
PRIOR = BASE / "rank9_miraclereality2_return233_received/DD_Rank9_MiracleReality2_Director_Return233_HELD.zip"
REPORT = BASE / "RANK9MIRACLEREALITY2_RETURN289_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9MIRACLEREALITY2_RETURN289_RECEIPT.json"

TARGETS = ["divine-intervention-greater", "wish"]
AUTHORITY = {
    "reviewedApplied": 816,
    "pending": 32,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 540,
    "scopedInterfaces": 173,
}
BLOCKERS = {"divine-intervention-greater": "MR233-B01", "wish": "MR233-B02"}
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


def matches(data: bytes, record: dict) -> bool:
    got = digest(data)
    return all(got.get(k) == record.get(k) for k in ("bytes", "sha256")) and (
        record.get("crc32") is None or got["crc32"] == record["crc32"]
    )


def safe_path(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


def ids(items) -> list[str]:
    return [x.get("id") for x in items if isinstance(x, dict) and x.get("id")]


delivery = read_json(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_hash = digest(archive_bytes)
check("delivery archive binding matches the received ZIP", matches(archive_bytes, delivery.get("archive", {})) and delivery["archive"].get("path") == ARCHIVE.name, archive_hash)
check("delivery ID and authority match the active 816/32/0 ledger", delivery.get("id") == "RANK9-MIRACLEREALITY2-DIRECTOR-RETURN289-DELIVERY" and delivery.get("authority") == AUTHORITY, delivery.get("authority"))
check("delivery records exactly the two held targets and no acceptance/application", delivery.get("heldIds") == TARGETS and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("accepted") is False and delivery.get("applied") is False, {k: delivery.get(k) for k in ["heldIds", "acceptedIds", "appliedIds", "accepted", "applied"]})

outer = zipfile.ZipFile(io.BytesIO(archive_bytes))
names = outer.namelist()
name_set = set(names)
records = delivery.get("members", [])
member_map = {x.get("path"): x for x in records if isinstance(x, dict)}
check("ZIP CRC test passes", outer.testzip() is None, {"members": len(names)})
check("archive paths are unique, safe and regular files", len(names) == len(name_set) and all(safe_path(n) for n in names) and all(not x.is_dir() for x in outer.infolist()), {"members": len(names), "unique": len(name_set)})
check("delivery member table exactly covers the complete ZIP", set(member_map) == name_set and len(records) == len(member_map) == delivery.get("zipMemberCount"), {"zip": len(names), "members": len(records), "zipMemberCount": delivery.get("zipMemberCount")})
bad_members = [n for n, rec in member_map.items() if n not in name_set or not matches(outer.read(n), rec)]
check("each payload matches its delivered SHA, byte count and CRC binding", not bad_members, bad_members[:20])
manifest = read_json(outer.read("MEMBER_MANIFEST.json"))
manifest_map = {x.get("path"): x for x in manifest.get("members", []) if isinstance(x, dict)}
check("embedded member manifest matches the same complete payload allowlist", manifest.get("payloadCount") == len(manifest_map) == len(name_set) - 1 and set(manifest_map) == name_set - {"MEMBER_MANIFEST.json"} and all(matches(outer.read(n), rec) for n, rec in manifest_map.items()), {"payloadCount": manifest.get("payloadCount"), "entries": len(manifest_map)})
check("manifest scope is Return289", manifest.get("id") == "RETURN289-EXACT-MEMBER-MANIFEST", manifest.get("id"))


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
replay = obj("REPLAY_RESULTS.json")
source_bindings = obj("SOURCE_BINDINGS.json")
source_verification = obj("SOURCE_VERIFICATION.json")
preseal = obj("PRESEAL_CHECK.json")
next_group = obj("NEXT_GROUP.json")
source_binding = obj("SOURCE_PACKET_BINDING.json")

decisions = decision.get("decisions", [])
expected_decisions = {x.get("spellId"): x for x in decisions}
check("sealed Director decision mirrors authority, scope and no-change limits", decision.get("id") == "RANK9-MIRACLEREALITY2-DIRECTOR-RETURN289" and decision.get("authority") == AUTHORITY and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("heldIds") == TARGETS and decision.get("accepted") is False and decision.get("applied") is False and decision.get("noCanonicalChanges") is True and decision.get("noRuntimeExecution") is True, {k: decision.get(k) for k in ["id", "acceptedIds", "appliedIds", "heldIds", "noCanonicalChanges", "noRuntimeExecution"]})
check("each target has a specific held decision, blocker and minimum witness", set(expected_decisions) == set(TARGETS) and len(decisions) == 2 and all(x.get("decision") == "HOLD" and x.get("accepted") is False and x.get("applied") is False and x.get("held") is True and x.get("blockerIds") == [BLOCKERS[x["spellId"]]] and bool(x.get("minimumMissingWitness")) and bool(x.get("requiredContent")) for x in decisions), [{k: x.get(k) for k in ["spellId", "decision", "blockerIds", "minimumMissingWitness"]} for x in decisions])
check("current authority snapshot matches delivery and records no application", authority.get("authority") == AUTHORITY and authority.get("acceptedIds") == [] and authority.get("appliedIds") == [] and authority.get("heldIds") == TARGETS, authority)
check("two blocker IDs and nine qualifications are preserved; only MR233-E01 closes", set(x.get("id") for x in obj("HOLD_REGISTER.json").get("targetBlockers", [])) == set(BLOCKERS.values()) and len(obj("QUALIFICATIONS.json")) == 9 and decision.get("closedEvidenceFindingIds") == ["MR233-E01"], {"targetBlockers": [x.get("id") for x in obj("HOLD_REGISTER.json").get("targetBlockers", [])], "qualifications": len(obj("QUALIFICATIONS.json")), "closed": decision.get("closedEvidenceFindingIds")})

question_ids = ids(original_questions) + ids(additions)
disposition_ids = ids(questions)
check("24 original and two focused questions each have one disposition", len(ids(original_questions)) == 24 and len(ids(additions)) == 2 and len(disposition_ids) == 26 and len(set(disposition_ids)) == 26 and set(disposition_ids) == set(question_ids), {"original": len(ids(original_questions)), "focused": len(ids(additions)), "dispositions": len(disposition_ids)})
check("all four required main cases remain held and incomplete", len(main_obligations) == 4 and len(main_cases) == 4 and {x.get("id") for x in main_cases} == set(ids(main_obligations)) and all(x.get("status") == "HELD-NOT-DEMONSTRATED" and x.get("completeSpellWitness") is False and x.get("actorClockComplete") is False and x.get("blockerIds") == [BLOCKERS[x.get("spellId")]] for x in main_cases), [{k: x.get(k) for k in ["id", "status", "blockerIds", "completeSpellWitness", "actorClockComplete"]} for x in main_cases])
check("all eight future requirements remain held without positive encounters", len(future) == 8 and all(x.get("completePositiveWitness") is False for x in future), {"count": len(future), "positive": [x.get("id") for x in future if x.get("completePositiveWitness") is True]})

components = casebook.get("auditComponents", [])
component_ids = {x.get("id") for x in components}
component_files = {n.removeprefix("component_cases/").removesuffix(".json") for n in names if n.startswith("component_cases/") and n.endswith(".json")}
results = replay.get("results", [])
check("six component-only cases match six archived files and replay results", len(components) == 6 and component_ids == component_files == {x.get("id") for x in results} and all(x.get("completeSpellWitness") is False and x.get("completeActorState") is False and all(e.get("kind") == "audit-classification" for e in x.get("events", [])) for x in components), {"cases": len(components), "files": len(component_files), "results": len(results)})
check("replay has six audit events, 12 forward/inverse operations and no gameplay or complete actor clocks", replay.get("auditEvents") == 6 and replay.get("gameplayEvents") == 0 and replay.get("forwardOperations") == 12 and replay.get("inverseOperations") == 12 and replay.get("fullReverseTraversals") == 6 and replay.get("completeActorClockCases") == 0 and replay.get("completePositiveSpellCases") == 0 and all(x.get("result") == "PASS_COMPONENT_ONLY" for x in results), {k: replay.get(k) for k in ["auditEvents", "gameplayEvents", "forwardOperations", "inverseOperations", "fullReverseTraversals", "completeActorClockCases", "completePositiveSpellCases"]})
check("3,344 source/data/replay checks pass with no failures", source_verification.get("checkCount") == 3344 and source_verification.get("passed") == 3344 and source_verification.get("failed") == 0 and counts.get("sourceDataReplayChecks") == 3344 and counts.get("sourceDataReplayPassed") == 3344 and counts.get("sourceDataReplayFailed") == 0, {"sourceVerification": [source_verification.get(k) for k in ["checkCount", "passed", "failed"]], "counts": [counts.get(k) for k in ["sourceDataReplayChecks", "sourceDataReplayPassed", "sourceDataReplayFailed"]]})
check("533 package checks and all pre-seal checks pass", delivery.get("packageChecks", {}).get("checkCount") == 533 and delivery.get("packageChecks", {}).get("passed") == 533 and delivery.get("packageChecks", {}).get("failed") == 0 and all(x.get("passed") is True for x in delivery.get("packageChecks", {}).get("checks", [])) and preseal.get("passed") == preseal.get("checkCount") and preseal.get("failed") == 0 and all(x.get("passed") is True for x in preseal.get("checks", [])), {"package": delivery.get("packageChecks", {}).get("checkCount"), "preseal": [preseal.get("checkCount"), preseal.get("passed"), preseal.get("failed")]})
check("semantic audit has 23 criteria: 17 pass, 6 blocked, none failed", counts.get("semanticCriteria") == 23 and counts.get("semanticPassing") == 17 and counts.get("semanticBlocked") == 6 and counts.get("semanticFailed") == 0, {k: counts.get(k) for k in ["semanticCriteria", "semanticPassing", "semanticBlocked", "semanticFailed"]})

changed = [x.get("path") for x in source_bindings if x.get("unchangedSince233") is False]
check("153 source bindings show only the authored review index changed since Return233", len(source_bindings) == 153 and counts.get("sourceBindings") == 153 and changed == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"] and counts.get("unchangedSourcesSince233") == 152 and counts.get("changedSourcesSince233") == 1, {"bindings": len(source_bindings), "changed": changed})
source_digest = digest(SOURCE.read_bytes())
source_rec = source_binding.get("sourceArchive", {})
check("Return289 binds the independently prepared Packet289 source ZIP", matches(SOURCE.read_bytes(), source_rec) and source_rec.get("sha256") == "913c81c3b6bf7bf5e96202c3d284015c264832d4cbf44dc27ce871b804880b06" and source_binding.get("sourceCommitBase") == "197366eae0c786415de55a0e4739e83f49f1a65f", source_digest)
prior_digest = digest(PRIOR.read_bytes())
check("prior Return233 archive is bound byte-exactly and retained as history", matches(PRIOR.read_bytes(), source_binding.get("priorReturn233Archive", {})) and source_binding.get("priorReturn233Archive", {}).get("sha256") == "75d844ac9e6ae496ce59d8b1334ba5b3d48ed9e74a774d4a40b30a5b274cdcbf", prior_digest)
packet_audit = read_json(outer.read("evidence/packet289/RANK9MIRACLEREALITY2_PACKET_289_INDEPENDENT_AUDIT.json"))
check("embedded Packet289 preparation audit is PASS 18/18", packet_audit.get("status") == "PASS" and packet_audit.get("checkCount") == 18 and packet_audit.get("passedChecks") == 18 and packet_audit.get("failedChecks") == 0, {k: packet_audit.get(k) for k in ["status", "checkCount", "passedChecks", "failedChecks"]})
check("next closure priority is mind-collapse under MD196-B01 and avoids stale queue repetition", next_group.get("nextPendingGroup") == "rank9-memory-denial6" and next_group.get("pendingIds") == ["mind-collapse"] and next_group.get("blockerIds") == ["MD196-B01"] and next_group.get("firstReviewTasksRemaining") == 0 and next_group.get("remainingPending") == 32 and "no automatic repetition" in next_group.get("purpose", "").lower() and delivery.get("nextPendingGroup") == "rank9-memory-denial6", next_group)
check("no canonical, runtime or application changes are declared", delivery.get("noCanonicalChanges") is True and delivery.get("noRuntime") is True and delivery.get("noApplication") is True and decision.get("noCanonicalChanges") is True and decision.get("noRuntimeExecution") is True, {k: delivery.get(k) for k in ["noCanonicalChanges", "noRuntime", "noApplication"]})

failures = [x for x in checks if not x["passed"]]
report = {
    "id": "RANK9MIRACLEREALITY2-RETURN289-INDEPENDENT-AUDIT",
    "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS" if not failures else "FAIL",
    "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_hash},
    "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
    "sourceArchive": {"path": SOURCE.relative_to(ROOT).as_posix(), **source_digest},
    "priorReturn233Archive": {"path": PRIOR.relative_to(ROOT).as_posix(), **prior_digest},
    "authority": delivery.get("authority"),
    "acceptedIds": delivery.get("acceptedIds"),
    "appliedIds": delivery.get("appliedIds"),
    "heldIds": delivery.get("heldIds"),
    "blockerIds": delivery.get("blockerIds"),
    "next": next_group,
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
    "checks": checks,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {
    "id": "RANK9MIRACLEREALITY2-RETURN289-RECEIPT",
    "status": report["status"],
    "archive": report["archive"],
    "delivery": report["delivery"],
    "sourceArchive": report["sourceArchive"],
    "priorReturn233Archive": report["priorReturn233Archive"],
    "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())},
    "checkCount": len(checks),
    "passedChecks": len(checks) - len(failures),
    "failedChecks": len(failures),
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": report["checkCount"], "passedChecks": report["passedChecks"], "failedChecks": report["failedChecks"], "failures": failures, "archiveSha256": archive_hash["sha256"]}, ensure_ascii=False, indent=2))
