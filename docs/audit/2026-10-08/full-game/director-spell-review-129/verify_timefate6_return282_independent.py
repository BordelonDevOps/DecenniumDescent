from __future__ import annotations

import gzip
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = BASE / "rank9_timefate6_return282_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_TimeFate6_Director_Return282_HELD.zip"
DELIVERY = RETURN_DIR / "DD_Rank9_TimeFate6_Director_Return282_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_timefate6_current_source_282_prepared"
SOURCE_ZIP = SOURCE_DIR / "DD_Rank9_TimeFate6_CurrentSource_282.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_TimeFate6_CurrentSource_282_DELIVERY.json"
SOURCE_PREP = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_282.json"
AUDIT = BASE / "RANK9_TIMEFATE6_RETURN282_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_TIMEFATE6_RETURN282_RECEIPT.json"
TARGETS = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
BLOCKERS = {
    "time-stop": ["TF192-B01"],
    "fate-rewrite": ["TF192-B04"],
    "collapse-timeline": ["TF192-B05"],
    "eternal-prophecy": ["TF192-B02"],
}
AUTH = {
    "reviewedApplied": 816,
    "pending": 32,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 540,
    "scopedInterfaces": 173,
}
NEXT = {
    "groupId": "rank9-knowledge-revelation5",
    "pendingIds": ["faction-omniscience-supreme"],
    "blockerIds": ["KR198-B01"],
    "requiresFreshAuthorityPacket": True,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def file_binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def main() -> None:
    checks: list[dict] = []

    def check(name: str, passed: bool, details=None) -> None:
        checks.append({"id": name, "pass": bool(passed), "details": details})

    delivery = read_json(DELIVERY)
    source_delivery = read_json(SOURCE_DELIVERY)
    source_preparation = read_json(SOURCE_PREP)
    return_binding = file_binding(RETURN_ZIP)
    delivery_binding = file_binding(DELIVERY)
    source_binding = file_binding(SOURCE_ZIP)

    check("return-sidecar-id-and-outer-archive-binding", delivery.get("id") == "RANK9-TIMEFATE6-DIRECTOR-RETURN282-DELIVERY" and all(return_binding[k] == delivery["archive"][k] for k in ("bytes", "sha256", "crc32")), return_binding)
    check("source-packet-delivery-and-preparation-bind", all(source_binding[k] == delivery["sourcePacket"][k] == source_delivery["archive"][k] for k in ("bytes", "sha256", "crc32")) and source_binding["sha256"] == source_preparation["packet"]["sha256"] and source_binding["bytes"] == source_preparation["packet"]["bytes"], source_binding)
    check("delivery-authority-is-current-816-32", delivery.get("sourceAuthority") == AUTH, delivery.get("sourceAuthority"))

    archive = zipfile.ZipFile(RETURN_ZIP)
    names = archive.namelist()
    expected_rows = {row["path"]: row for row in delivery["members"]}
    manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
    internal_rows = {row["path"]: row for row in manifest["members"]}
    check("return-zip-integrity-and-safe-unique-members", archive.testzip() is None and len(names) == len(set(names)) == delivery.get("memberCount") == 61 and all(safe_member(name) for name in names), {"members": len(names)})
    check("external-and-internal-manifests-cover-exact-payload", delivery.get("payloadMemberCount") == manifest.get("payloadMemberCount") == 60 and set(expected_rows) == set(names) and set(internal_rows) | {"MEMBER_MANIFEST.json"} == set(names) and set(internal_rows) == set(expected_rows) - {"MEMBER_MANIFEST.json"}, {"externalRows": len(expected_rows), "internalRows": len(internal_rows), "zipMembers": len(names)})
    for member, row in expected_rows.items():
        raw = archive.read(member)
        check(f"member:{member}", len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"], {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})

    decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
    counts = json.loads(archive.read("COUNTS.json"))
    binding = json.loads(archive.read("SOURCE_BINDING.json"))
    queue = json.loads(archive.read("REMAINING_QUEUE.json"))
    casebook = json.loads(gzip.decompress(archive.read("CASEBOOK.json.gz")))
    data_check = json.loads(archive.read("DATA_INTEGRITY_CHECK.json"))
    clock_check = json.loads(archive.read("CLOCK_CHECK.json"))
    source_check = json.loads(archive.read("SOURCE_VERIFICATION.json"))
    semantic_check = json.loads(archive.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
    validation = json.loads(archive.read("VALIDATION.json"))
    hold_register = json.loads(archive.read("HOLD_REGISTER.json"))

    check("exact-four-scope-all-held-unapplied", decision.get("group") == "rank9-time-fate6" and decision.get("sourceAuthority") == decision.get("postDecisionAppliedAuthority") == AUTH and decision.get("accepted") is False and decision.get("applied") is False and decision.get("acceptedIds") == decision.get("appliedIds") == [] and decision.get("heldIds") == TARGETS and delivery.get("heldIds") == TARGETS and decision.get("targetIds", TARGETS) == TARGETS, {"acceptedIds": decision.get("acceptedIds"), "appliedIds": decision.get("appliedIds"), "heldIds": decision.get("heldIds")})
    per_identity = {row["id"]: row for row in decision["perIdentity"]}
    check("per-identity-blockers-exact-and-held", set(per_identity) == set(TARGETS) and {sid: per_identity[sid]["blockerIds"] for sid in TARGETS} == BLOCKERS and all(per_identity[sid]["held"] and not per_identity[sid]["accepted"] and not per_identity[sid]["applied"] for sid in TARGETS), {sid: per_identity[sid]["blockerIds"] for sid in per_identity})
    check("minimum-missing-witness-is-recorded-for-each-hold", all(isinstance(per_identity[sid].get("minimumMissingWitness"), str) and per_identity[sid]["minimumMissingWitness"].strip() for sid in TARGETS), {sid: per_identity[sid].get("minimumMissingWitness") for sid in TARGETS})
    check("no-canonical-github-runtime-or-release-approval", decision.get("canonicalFilesModified") is False and decision.get("GitHubModified") is False and decision.get("sourceProgramsExecuted") is False and decision.get("runtimeExecuted") is False and all(decision.get(k) is False for k in ("implementationApproved", "humanPlayApproved", "balanceApproved", "cosmologyApproved", "completionApproved", "releaseApproved")), {k: decision.get(k) for k in ("canonicalFilesModified", "GitHubModified", "sourceProgramsExecuted", "runtimeExecuted", "implementationApproved", "releaseApproved")})
    check("next-queue-exactly-knowledge-revelation5", decision.get("nextPendingGroup") == NEXT and queue.get("nextPendingGroup") == NEXT and delivery.get("nextPendingGroup") == NEXT, decision.get("nextPendingGroup"))
    check("replay-scope-and-counts-reconcile", counts.get("procedures") == 4 and counts.get("cases") == len(casebook.get("cases", [])) == 62 and {case.get("spellId") for case in casebook["cases"]} == set(TARGETS) and sum(len(case.get("events", [])) for case in casebook["cases"]) == counts.get("events") == 628 and counts.get("forwardOperations") == counts.get("inverseOperations") == 1256 and counts.get("eventOperations") == 2512 and counts.get("currentSourceBindings") == 140 and counts.get("acceptedIds") == 0 and counts.get("appliedIds") == 0 and counts.get("heldIds") == 4, counts)
    check("integrity-clock-source-and-semantic-checks-pass", data_check.get("failureCount") == clock_check.get("failureCount") == source_check.get("failureCount") == 0 and all(row.get("pass") is True for report in (data_check, clock_check, source_check, semantic_check) for row in report.get("checks", [])) and data_check.get("checkCount") == counts.get("dataChecks") == 3896 and clock_check.get("checkCount") == counts.get("clockChecks") == 5734 and source_check.get("checkCount") == counts.get("sourceChecks") == 1280 and semantic_check.get("checkCount") == counts.get("semanticInvariantChecks") == 191 and semantic_check.get("result") == "ALL_FOUR_HELD" and semantic_check.get("semanticAcceptancePass") is False and len(semantic_check.get("requiredWitnessFailures", [])) == 4 and not semantic_check.get("unexpectedFailures"), {"data": data_check.get("checkCount"), "clock": clock_check.get("checkCount"), "source": source_check.get("checkCount"), "semantic": semantic_check.get("checkCount"), "requiredWitnessFailures": len(semantic_check.get("requiredWitnessFailures", [])), "unexpectedFailures": len(semantic_check.get("unexpectedFailures", []))})
    check("validation-reports-no-acceptance-or-application", validation.get("accepted") is False and validation.get("applied") is False and validation.get("dataIntegrity") == "PASS" and validation.get("sourceIntegrity") == "PASS" and validation.get("clockChecks") == "PASS_SCOPED_STATIC_INVARIANTS", validation)
    check("hold-register-preserves-all-four-blockers-and-authority", hold_register.get("currentAuthority") == AUTH and {row["id"] for row in hold_register.get("currentBlockers", [])} == {blocker for values in BLOCKERS.values() for blocker in values}, hold_register.get("currentAuthority"))

    source_binding_rows = binding.get("currentSourceBindings", [])
    source_snapshot = binding.get("sourceSnapshot", {})
    source_archive_ref = binding.get("inputArchive", {})
    check("source-snapshot-and-external-current-packet-reconcile", binding.get("sourceAuthority") == AUTH and SOURCE_ZIP.name not in names and source_snapshot.get("branch") == "main" and source_archive_ref.get("sha256") == source_binding["sha256"] and source_archive_ref.get("bytes") == source_binding["bytes"] and len(source_binding_rows) == 140, {"branch": source_snapshot.get("branch"), "bindings": len(source_binding_rows), "externalPacket": source_archive_ref})
    with zipfile.ZipFile(SOURCE_ZIP) as source_archive_zip:
        source_manifest = json.loads(source_archive_zip.read("MANIFEST.json"))
        candidate = json.loads(source_archive_zip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json"))
        packet_manifest_rows = {row["path"]: row for row in source_manifest.get("members", [])}
        candidate_rows = {row["path"]: row for row in candidate.get("sourceBindings", [])}
        returned_rows = {row["path"]: row for row in source_binding_rows}
        packet_matches = all(candidate_rows.get(path) == row == returned_rows.get(path) for path, row in candidate_rows.items())
        check("current-packet-and-return-refresh-all-140-source-bindings", len(candidate_rows) == len(returned_rows) == 140 and set(candidate_rows) == set(returned_rows) and packet_matches and source_manifest.get("payloadMemberCount") == len(source_manifest.get("members", [])) == len(source_archive_zip.namelist()) - 1, {"candidateBindings": len(candidate_rows), "returnedBindings": len(returned_rows), "packetMembers": len(source_archive_zip.namelist()), "manifestPayloadCount": source_manifest.get("payloadMemberCount")})
        check("current-packet-source-snapshot-matches-preparation", candidate.get("sourceSnapshot") == source_preparation.get("sourceSnapshot") and source_snapshot == source_preparation.get("sourceSnapshot"), {"returnBranch": source_snapshot.get("branch"), "packetBranch": candidate.get("sourceSnapshot", {}).get("branch")})

    check("outer-return-delivery-members-and-count-match", delivery.get("memberCount") == 61 and delivery.get("payloadMemberCount") == 60 and delivery.get("counts", {}).get("events") == 628 and delivery.get("counts", {}).get("forwardOperations") == 1256 and delivery.get("counts", {}).get("inverseOperations") == 1256, delivery.get("counts"))

    failed = [row for row in checks if not row["pass"]]
    audit = {
        "id": "RANK9-TIMEFATE6-RETURN282-INDEPENDENT-AUDIT",
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "FAIL",
        "checksPassed": len(checks) - len(failed),
        "checksFailed": len(failed),
        "checkCount": len(checks),
        "returnArchive": return_binding,
        "returnDelivery": delivery_binding,
        "sourceArchive": source_binding,
        "authority": AUTH,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "nextGroup": NEXT,
        "checks": checks,
    }
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    receipt = {
        "id": "RANK9-TIMEFATE6-RETURN282-INDEPENDENT-RECEIPT",
        "status": audit["status"],
        "audit": file_binding(AUDIT),
        "returnArchive": return_binding,
        "returnDelivery": delivery_binding,
        "authority": AUTH,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockers": BLOCKERS,
        "nextGroup": NEXT,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": audit["status"], "checksPassed": audit["checksPassed"], "checksFailed": len(failed), "returnArchive": return_binding, "nextGroup": NEXT, "failures": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
