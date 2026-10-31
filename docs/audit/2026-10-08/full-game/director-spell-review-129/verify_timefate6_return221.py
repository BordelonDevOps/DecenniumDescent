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
RETURN_DIR = BASE / "rank9_timefate6_return221_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_TimeFate4_Director_Return221_HELD.zip"
DELIVERY = RETURN_DIR / "DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_timefate6_current_source_221_prepared"
SOURCE_ZIP = SOURCE_DIR / "DD_Rank9_TimeFate6_CurrentSource_221.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_TimeFate6_CurrentSource_221_DELIVERY.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_221.json"
HANDOFF = BASE / "CURRENT_HANDOFF_221.json"
PENDING_AUDIT = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_221.json"
CAPTURE220 = BASE / "RANK9_AGENCYCONTROL9_RETURN220_INLINE_CAPTURE.json"
TARGETS = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
EXPECTED_BLOCKERS = {
    "time-stop": ["TF192-B01"],
    "fate-rewrite": ["TF192-B04"],
    "collapse-timeline": ["TF192-B05"],
    "eternal-prophecy": ["TF192-B02"],
}
COMMON_QUALIFICATIONS = [
    "TF192-Q-SOURCE", "TF192-Q-PHYSICAL", "TF192-Q-RUNTIME", "TF192-Q-PLAY",
    "TF192-Q-BALANCE", "TF192-Q-COSMOLOGY", "TF192-Q-DOMAIN",
    "TF192-Q-COMPLETION", "TF192-Q-RELEASE",
]
AUTH = {
    "reviewedApplied": 810,
    "pending": 38,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 534,
    "scopedInterfaces": 173,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(p not in ("", ".", "..") for p in path.parts)


def checked(checks: list[dict], name: str, ok: bool, details=None):
    checks.append({"id": name, "passed": bool(ok), "details": details})
    if not ok:
        raise AssertionError(f"Audit check failed: {name}: {details}")


def main():
    now = datetime.now(timezone.utc).isoformat()
    delivery = readj(DELIVERY)
    input_delivery = readj(SOURCE_DELIVERY)
    checks = []

    return_bytes = RETURN_ZIP.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    checked(checks, "return-zip-size-sha-crc-match-sidecar", len(return_bytes) == delivery["archive"]["bytes"] and sha(return_bytes) == delivery["archive"]["sha256"] and crc(return_bytes) == delivery["archive"]["crc32"], {"bytes": len(return_bytes), "sha256": sha(return_bytes), "crc32": crc(return_bytes)})
    checked(checks, "return-sidecar-sha-captured", len(delivery_bytes) == 12375 and sha(delivery_bytes) == "d02a717738ecf880a9693419015ba0a48f1009e70795cc93ec38068a33d19808", {"bytes": len(delivery_bytes), "sha256": sha(delivery_bytes)})
    checked(checks, "source-packet-sidecar-matches-delivery", delivery["sourcePacket"]["sha256"] == input_delivery["archive"]["sha256"] and delivery["sourcePacket"]["bytes"] == input_delivery["archive"]["bytes"], delivery["sourcePacket"])
    source_bytes = SOURCE_ZIP.read_bytes()
    checked(checks, "source-packet-local-bytes-match-return-binding", len(source_bytes) == delivery["sourcePacket"]["bytes"] and sha(source_bytes) == delivery["sourcePacket"]["sha256"] and crc(source_bytes) == delivery["sourcePacket"]["crc32"], {"bytes": len(source_bytes), "sha256": sha(source_bytes), "crc32": crc(source_bytes)})
    archive = zipfile.ZipFile(RETURN_ZIP)
    source_binding_early = json.loads(archive.read("SOURCE_BINDING.json"))
    source_delivery_binding = source_binding_early["sourceDelivery"]
    source_delivery_bytes = SOURCE_DELIVERY.read_bytes()
    checked(checks, "source-delivery-manifest-binding-matches", len(source_delivery_bytes) == source_delivery_binding["bytes"] and sha(source_delivery_bytes) == source_delivery_binding["sha256"] and crc(source_delivery_bytes) == source_delivery_binding["crc32"], source_delivery_binding)
    checked(checks, "return-zip-crc-integrity", archive.testzip() is None, None)
    names = archive.namelist()
    checked(checks, "return-member-set-unique-safe-and-exact", len(names) == len(set(names)) == delivery["memberCount"] and all(safe_member(n) for n in names), {"members": len(names)})
    expected_members = {row["path"]: row for row in delivery["members"]}
    internal_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
    internal_paths = {row["path"] for row in internal_manifest["members"]}
    checked(checks, "delivery-and-internal-member-manifests-reconcile", len(expected_members) == delivery["memberCount"] == len(names) == 23 and delivery["payloadMemberCount"] == internal_manifest["payloadMemberCount"] == len(internal_paths) == 22 and set(expected_members) == set(names) == internal_paths | {"MEMBER_MANIFEST.json"}, {"sidecarMemberRows": len(expected_members), "zipMembers": len(names), "payloadRowsExcludingSelfManifest": len(internal_paths)})
    for name, row in expected_members.items():
        raw = archive.read(name)
        checked(checks, f"member:{name}", len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"], {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})

    decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
    casebook = json.loads(gzip.decompress(archive.read("CASEBOOK.json.gz")))
    counts = json.loads(archive.read("COUNTS.json"))
    data_integrity = json.loads(archive.read("DATA_INTEGRITY_CHECK.json"))
    clock_check = json.loads(archive.read("CLOCK_CHECK.json"))
    source_verification = json.loads(archive.read("SOURCE_VERIFICATION.json"))
    source_binding = source_binding_early
    package_verification = delivery["packageVerification"]

    checked(checks, "delivery-scope-and-authority", delivery["scope"] == TARGETS and delivery["sourceAuthority"] == AUTH, {"scope": delivery["scope"], "authority": delivery["sourceAuthority"]})
    checked(checks, "all-four-held-not-accepted-or-applied", delivery["accepted"] is False and delivery["applied"] is False and delivery["acceptedIds"] == [] and delivery["heldIds"] == TARGETS and decision["accepted"] is False and decision["applied"] is False and decision["acceptedIds"] == [] and decision["heldIds"] == TARGETS, {"accepted": delivery["accepted"], "applied": delivery["applied"], "held": delivery["heldIds"]})
    checked(checks, "director-return-authority", decision["sourceAuthority"] == AUTH, decision["sourceAuthority"])

    per_identity = {row["id"]: row for row in decision["perIdentity"]}
    checked(checks, "exact-four-identity-decisions", set(per_identity) == set(TARGETS), sorted(per_identity))
    checked(checks, "retained-blocker-ids", {sid: per_identity[sid]["blockerIds"] for sid in TARGETS} == EXPECTED_BLOCKERS, {sid: per_identity[sid]["blockerIds"] for sid in TARGETS})
    checked(checks, "all-decisions-held", all(per_identity[sid]["decision"] == "HELD" and per_identity[sid]["accepted"] is False and per_identity[sid]["applied"] is False for sid in TARGETS), None)
    checked(checks, "common-qualification-set", delivery["qualifications"] == COMMON_QUALIFICATIONS, delivery["qualifications"])
    checked(checks, "shared-qualifications-preserved-per-spell", all(set(COMMON_QUALIFICATIONS).issubset(set(per_identity[sid]["qualificationIds"])) for sid in TARGETS), None)

    cases = casebook.get("cases", [])
    case_ids = {case.get("spellId") for case in cases}
    event_count = sum(len(case.get("events", [])) for case in cases)
    checked(checks, "casebook-exact-target-scope", len(cases) == 62 and case_ids == set(TARGETS), {"caseCount": len(cases), "spellIds": sorted(case_ids)})
    checked(checks, "casebook-event-count", event_count == counts["events"] == delivery["counts"]["events"] == 628, {"events": event_count})
    checked(checks, "forward-inverse-operation-counts-reconcile", counts["forwardOperations"] == counts["inverseOperations"] == 1256 and counts["eventOperations"] == 2512 and delivery["counts"] == counts, counts)
    checked(checks, "reported-data-integrity-and-clock-checks-pass", data_integrity["checkCount"] == counts["dataIntegrityChecks"] == 3266 and data_integrity["failureCount"] == 0 and all(item.get("pass", False) for item in data_integrity["checks"]) and clock_check["checkCount"] == counts["clockChecks"] == 1240 and clock_check["failureCount"] == 0 and all(item.get("pass", False) for item in clock_check["checks"]), {"dataIntegrity": data_integrity["checkCount"], "clock": clock_check["checkCount"]})
    checked(checks, "reported-source-and-package-checks-pass", source_verification["checkCount"] == counts["sourceChecks"] == 1121 and source_verification["failureCount"] == 0 and all(item.get("pass", False) for item in source_verification["checks"]) and package_verification["checkCount"] == 72 and package_verification["failureCount"] == 0 and all(item.get("pass", False) for item in package_verification["checks"]), {"sourceChecks": source_verification["checkCount"], "packageChecks": package_verification["checkCount"]})

    candidate_path = SOURCE_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_221.json"
    candidate = readj(candidate_path)
    candidate_bindings = {"sources_current/" + row["path"]: row for row in candidate["sourceBindings"]}
    returned_bindings = {row["path"]: row for row in source_binding["refreshedSources"]}
    source_reconciliation = []
    with zipfile.ZipFile(SOURCE_ZIP) as source_archive:
        source_manifest = json.loads(source_archive.read("MANIFEST.json"))
        manifest_rows = {row["path"]: row for row in source_manifest["members"]}
        all_source_bindings_match = len(candidate_bindings) == len(returned_bindings) == 140
        for path, row in candidate_bindings.items():
            returned = returned_bindings.get(path)
            manifest_row = manifest_rows.get(path)
            if not returned or not manifest_row:
                all_source_bindings_match = False
                continue
            raw = source_archive.read(path)
            if not (len(raw) == row["bytes"] == returned["bytes"] == manifest_row["bytes"] and row["sha256"] == returned["sha256"] == manifest_row["sha256"] == sha(raw) and row.get("crc32", manifest_row["crc32"]) == returned["crc32"] == manifest_row["crc32"] == crc(raw)):
                all_source_bindings_match = False
            source_reconciliation.append(path)
    checked(checks, "all-140-refreshed-source-bindings-match-source-packet", all_source_bindings_match and len(source_reconciliation) == 140, {"matched": len(source_reconciliation)})
    checked(checks, "canonical-and-github-unchanged-per-decision", decision["canonicalFilesModified"] is False and decision["GitHubModified"] is False, {"canonicalFilesModified": decision["canonicalFilesModified"], "GitHubModified": decision["GitHubModified"]})

    blocker_reasons = {sid: {"reason": per_identity[sid]["reason"], "qualificationIds": per_identity[sid]["qualificationIds"]} for sid in TARGETS}
    independent_audit = {
        "id": "RANK9-TIMEFATE6-RETURN221-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS_PACKAGE_BINDING_AND_SCOPE; ALL_FOUR_SEMANTIC_HOLDS_RETAINED",
        "returnArchive": {"path": RETURN_ZIP.relative_to(ROOT).as_posix(), "bytes": len(return_bytes), "sha256": sha(return_bytes), "crc32": crc(return_bytes)},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_bytes), "sha256": sha(delivery_bytes), "crc32": crc(delivery_bytes)},
        "sourcePacket": {"path": SOURCE_ZIP.relative_to(ROOT).as_posix(), "bytes": len(source_bytes), "sha256": sha(source_bytes), "crc32": crc(source_bytes)},
        "sourceDeliveryManifest": {"path": SOURCE_DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(SOURCE_DELIVERY.read_bytes()), "sha256": sha(SOURCE_DELIVERY.read_bytes()), "crc32": crc(SOURCE_DELIVERY.read_bytes())},
        "checksPassed": len(checks),
        "checksFailed": 0,
        "checks": checks,
        "limitations": [
            "Return-package hashes, member list, authority, decision scope and current-source bindings were independently verified.",
            "The semantic simulation/replay results are reported in the director package and their integrity/counts were checked; this audit did not execute GPT-supplied programs or independently reproduce the semantic replay.",
        ],
    }
    audit_path = BASE / "RANK9_TIMEFATE6_RETURN221_INDEPENDENT_AUDIT.json"
    audit_path.write_text(json.dumps(independent_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    receipt = {
        "id": "RANK9-TIMEFATE6-DIRECTOR-RETURN-221-RECEIPT",
        "recordedAtUtc": now,
        "status": "ALL_FOUR_HELD; RETURN_ARCHIVE_AND_SIDECAR_INDEPENDENTLY_VERIFIED",
        "reviewedIds": TARGETS,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": TARGETS,
        "blockers": blocker_reasons,
        "sourceAuthority": AUTH,
        "sourcePacket": {"path": SOURCE_ZIP.relative_to(ROOT).as_posix(), "bytes": len(source_bytes), "sha256": sha(source_bytes)},
        "directorReturn": {"path": RETURN_ZIP.relative_to(ROOT).as_posix(), "bytes": len(return_bytes), "sha256": sha(return_bytes)},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": len(delivery_bytes), "sha256": sha(delivery_bytes)},
        "commonQualifications": COMMON_QUALIFICATIONS,
        "counts": counts,
        "independentAudit": {"path": audit_path.relative_to(ROOT).as_posix(), "checksPassed": len(checks), "checksFailed": 0},
        "nextGroup": "rank9-casting-cost5",
        "canonicalFilesModified": False,
        "GitHubModified": False,
        "runtimeExecuted": False,
    }
    receipt_path = BASE / "RANK9_TIMEFATE6_RETURN221_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": independent_audit["status"], "checksPassed": len(checks), "checksFailed": 0, "cases": len(cases), "events": event_count, "blockers": EXPECTED_BLOCKERS, "receipt": receipt_path.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
