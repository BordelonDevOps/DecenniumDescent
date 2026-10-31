import hashlib
import io
import json
import pathlib
import sys
import zipfile
import zlib


REPO = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
RECV = REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_deathrecovery7_return217_received"
ARCHIVE = RECV / "DD_Rank9_DeathRecovery3_Director_Return217.zip"
DELIVERY = RECV / "DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json"
OUT = RECV / "RETURN217_INDEPENDENT_AUDIT.json"
EXTRACT = RECV / "extracted"


def hash_bytes(data: bytes) -> dict:
    crc = zlib.crc32(data) & 0xFFFFFFFF
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "crc32": f"{crc:08x}"}


def hash_file(path: pathlib.Path) -> dict:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            size += len(chunk)
            h.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return {"bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xFFFFFFFF:08x}"}


delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
checks = []


def check(name: str, passed: bool, detail=None):
    checks.append({"check": name, "passed": bool(passed), **({"detail": detail} if detail is not None else {})})


# Verify the actual download and the unmodified director delivery binding.
archive_actual = hash_file(ARCHIVE)
archive_expected = delivery.get("archive", {})
check(
    "outer archive bytes/SHA-256/CRC32 match delivery manifest",
    all(archive_actual.get(k) == archive_expected.get(k) for k in ("bytes", "sha256", "crc32")),
    {"actual": archive_actual, "expected": archive_expected},
)
manifest_actual = hash_file(DELIVERY)
check(
    "external delivery manifest SHA-256 matches GPT-reported value",
    manifest_actual["sha256"] == "073aac40c9806e1f36d8e062cd6b0c60e80de8ed983dcfbadbd224d8f19df3f3",
    manifest_actual,
)

# Exact disposition, authority and qualification checks.
expected_dispositions = [
    {"id": "doom", "accepted": True, "applied": False, "blockerIds": []},
    {"id": "final-word", "accepted": False, "applied": False, "blockerIds": ["DR217-B01"]},
    {"id": "eternal-pact", "accepted": True, "applied": False, "blockerIds": []},
]
observed_dispositions = [
    {k: entry.get(k) for k in ("id", "accepted", "applied", "blockerIds")}
    for entry in delivery.get("perIdentity", [])
]
check("exact per-identity director decisions and blocker", observed_dispositions == expected_dispositions, observed_dispositions)
check(
    "accepted IDs are exactly doom and eternal-pact; held ID is final-word",
    delivery.get("acceptedIds") == ["doom", "eternal-pact"]
    and delivery.get("heldIds") == ["final-word"]
    and delivery.get("blockerIds") == ["DR217-B01"],
    {"acceptedIds": delivery.get("acceptedIds"), "heldIds": delivery.get("heldIds"), "blockerIds": delivery.get("blockerIds")},
)
check(
    "application is explicitly false with no applied IDs",
    delivery.get("applied") is False and delivery.get("appliedIds", []) == [],
    {"applied": delivery.get("applied"), "appliedIds": delivery.get("appliedIds")},
)
expected_authority = {
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 530,
    "pending": 42,
    "reviewedApplied": 806,
    "scopedInterfaces": 173,
}
check("source authority unchanged at 806/42/0", delivery.get("sourceAuthority") == expected_authority, delivery.get("sourceAuthority"))
check(
    "qualification boundary retained",
    delivery.get("qualifications") == [
        "static authored review only",
        "no canonical/index/catalog/queue/handoff edits",
        "applied=false; source authority remains806/42/0",
        "no runtime or implementation approval",
        "no supplied/historical programs executed",
        "no human-play/playtest/balance approval",
        "no cosmology/domain-closure/completion/release approval",
        "all unrelated holds retained",
    ],
    delivery.get("qualifications"),
)

# Audit exact member inventory and every decompressed member's size, digest and CRC.
members_manifest = delivery.get("members", [])
expected_by_path = {entry.get("path"): entry for entry in members_manifest}
allowlist = delivery.get("allArchiveMemberPaths", [])
check(
    "manifest inventory has 80 unique members and 79 payload members",
    len(members_manifest) == delivery.get("memberCount") == 80
    and len(expected_by_path) == 80
    and len(allowlist) == 80
    and len(set(allowlist)) == 80
    and set(expected_by_path) == set(allowlist)
    and delivery.get("payloadCountExcludingInternalManifest") == 79,
    {"members": len(members_manifest), "manifestMemberCount": delivery.get("memberCount"), "allowlist": len(allowlist), "payloadCountExcludingInternalManifest": delivery.get("payloadCountExcludingInternalManifest")},
)
member_results = []
zip_errors = []
names = []
internal_json = {}
with zipfile.ZipFile(ARCHIVE, "r") as zf:
    names = zf.namelist()
    bad = zf.testzip()
    check("ZIP decompression and CRC test", bad is None, bad)
    check(
        "archive exact 80-member allowlist with no duplicates",
        len(names) == 80 and len(set(names)) == 80 and set(names) == set(allowlist),
        {"archiveMemberCount": len(names), "duplicateNames": len(names) - len(set(names)), "missing": sorted(set(allowlist) - set(names)), "extra": sorted(set(names) - set(allowlist))},
    )
    unsafe = [n for n in names if pathlib.PurePosixPath(n).is_absolute() or ".." in pathlib.PurePosixPath(n).parts or "\\" in n or n.startswith(".")]
    check("archive paths contain no traversal or hidden members", not unsafe, unsafe)
    for name in names:
        expected = expected_by_path.get(name)
        if expected is None:
            continue
        h = hashlib.sha256()
        crc = 0
        size = 0
        try:
            with zf.open(name, "r") as stream:
                while chunk := stream.read(1024 * 1024):
                    size += len(chunk)
                    h.update(chunk)
                    crc = zlib.crc32(chunk, crc)
            actual = {"path": name, "bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xFFFFFFFF:08x}"}
            ok = all(actual[k] == expected.get(k) for k in ("bytes", "sha256", "crc32"))
            member_results.append({**actual, "expected": expected, "passed": ok})
            if not ok:
                zip_errors.append(name)
        except Exception as exc:
            zip_errors.append(name + ": " + repr(exc))
    for name in ("DIRECTOR_DECISION.json", "COUNTS.json", "DATA_INTEGRITY_CHECK.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "VALIDATION.json", "NEXT_QUEUE_HANDOFF.json", "MEMBER_MANIFEST.json"):
        if name in names:
            try:
                internal_json[name] = json.loads(zf.read(name).decode("utf-8-sig"))
            except Exception as exc:
                internal_json[name] = {"_parseError": repr(exc)}

check(
    "all 80 member SHA-256/size/CRC bindings match external manifest",
    len(member_results) == 80 and not zip_errors and all(entry["passed"] for entry in member_results),
    {"verified": len(member_results), "errors": zip_errors[:25]},
)

# The package's saved replay and failure check must agree with the independent summary.
counts = internal_json.get("COUNTS.json", {})
data_check = internal_json.get("DATA_INTEGRITY_CHECK.json", {})
semantic_check = internal_json.get("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", {})
check(
    "internal counts report 14,881 replay checks",
    any(v == 14881 for v in counts.values() if isinstance(v, int))
    or any(v == 14881 for v in data_check.values() if isinstance(v, int)),
    {"counts": counts, "dataIntegrity": data_check},
)
check(
    "internal semantic check parses without error",
    isinstance(semantic_check, dict) and "_parseError" not in semantic_check,
    semantic_check,
)

# Bind the current authority and historical decision sources to this checkout.
baseline_paths = {
    "current/CURRENT42_PENDING_IDENTITY_AUDIT_216.json": REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT42_PENDING_IDENTITY_AUDIT_216.json",
    "current/CURRENT_HANDOFF_216.json": REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_216.json",
    "current/CURRENT_SPELL_QUEUE_216.json": REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_216.json",
    "current/RETURN216_CANDIDATE_BINDING_RECONCILIATION.json": REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_deathrecovery7_source_packet_216_refreshed/CURRENT_CANDIDATE_BINDING_RECONCILIATION.json",
    "prior/Return184.zip": REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_deathrecovery7_return184_received/DD_Rank9_DeathRecovery7_Director_Return184.zip",
    "source/CurrentSource216.zip": REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_deathrecovery7_source_packet_216_refreshed/DD_Rank9_DeathRecovery7_CurrentSource_216.zip",
}
baseline_results = []
with zipfile.ZipFile(ARCHIVE, "r") as zf:
    for member_name, local_path in baseline_paths.items():
        try:
            embedded = zf.read(member_name)
            local = local_path.read_bytes()
            embedded_hash = hash_bytes(embedded)
            local_hash = hash_bytes(local)
            ok = embedded == local
            baseline_results.append({"member": member_name, "localPath": str(local_path.relative_to(REPO)), "embedded": embedded_hash, "local": local_hash, "passed": ok})
        except Exception as exc:
            baseline_results.append({"member": member_name, "localPath": str(local_path), "error": repr(exc), "passed": False})
check("six authority, source and prior bindings match local byte-exact evidence", len(baseline_results) == 6 and all(x.get("passed") for x in baseline_results), baseline_results)

# Verify all preserved Return184 target cases byte-for-byte against their prior archive copies.
preserved_results = []
with zipfile.ZipFile(ARCHIVE, "r") as current_zip, zipfile.ZipFile(baseline_paths["prior/Return184.zip"], "r") as prior_zip:
    prior_by_basename = {pathlib.PurePosixPath(n).name: n for n in prior_zip.namelist() if not n.endswith("/")}
    preserved_names = [n for n in names if n.startswith("preserved_cases/") and n.endswith(".json")]
    for name in preserved_names:
        basename = pathlib.PurePosixPath(name).name
        prior_name = prior_by_basename.get(basename)
        try:
            same = prior_name is not None and current_zip.read(name) == prior_zip.read(prior_name)
            preserved_results.append({"currentMember": name, "priorMember": prior_name, "passed": same})
        except Exception as exc:
            preserved_results.append({"currentMember": name, "priorMember": prior_name, "error": repr(exc), "passed": False})
check(
    "45 preserved Return184 target cases match the exact prior archive",
    len(preserved_names) == 45 and len(preserved_results) == 45 and all(x.get("passed") for x in preserved_results),
    {"preservedCount": len(preserved_names), "mismatches": [x for x in preserved_results if not x.get("passed")][:10]},
)

# Confirm the pending set and current queue authority at intake.
queue_data = json.loads((REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_216.json").read_text(encoding="utf-8-sig"))
check(
    "current queue still binds authority 806/42/0 and the three Death/Recovery IDs",
    queue_data.get("currentAuthority", {}).get("reviewedApplied") == 806
    and queue_data.get("currentAuthority", {}).get("pending") == 42
    and queue_data.get("currentAuthority", {}).get("acceptedUnapplied") == 0
    and any(g.get("group") == "rank9-death-recovery7" and g.get("pendingIds") == ["doom", "final-word", "eternal-pact"] for g in queue_data.get("currentPendingGroups", [])),
    queue_data.get("currentAuthority"),
)

all_passed = all(entry["passed"] for entry in checks)
result = {
    "id": "RETURN217-INDEPENDENT-AUDIT",
    "status": "PASS" if all_passed else "FAIL",
    "archive": {"path": str(ARCHIVE.relative_to(REPO)), **archive_actual},
    "deliveryManifest": {"path": str(DELIVERY.relative_to(REPO)), **manifest_actual},
    "acceptedIds": delivery.get("acceptedIds"),
    "heldIds": delivery.get("heldIds"),
    "applied": delivery.get("applied"),
    "authorityBeforeApplication": delivery.get("sourceAuthority"),
    "checks": checks,
    "verifiedMemberCount": len(member_results),
    "memberResults": member_results,
    "baselineBindings": baseline_results,
    "preservedCaseChecks": preserved_results,
    "internalRecords": internal_json,
}
if all_passed:
    extract_root = EXTRACT.resolve()
    for name in names:
        target = (EXTRACT / pathlib.PurePosixPath(name)).resolve()
        if not target.is_relative_to(extract_root):
            raise RuntimeError("Unsafe archive path: " + name)
    with zipfile.ZipFile(ARCHIVE, "r") as zf:
        zf.extractall(EXTRACT)
    result["extracted"] = True
    result["extractionRoot"] = str(EXTRACT.relative_to(REPO))
else:
    result["extracted"] = False

OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
summary = {
    "status": result["status"],
    "checkCount": len(checks),
    "checksPassed": sum(entry["passed"] for entry in checks),
    "verifiedMembers": len(member_results),
    "preservedCases": len(preserved_results),
    "acceptedIds": delivery.get("acceptedIds"),
    "heldIds": delivery.get("heldIds"),
    "authority": delivery.get("sourceAuthority"),
    "audit": str(OUT.relative_to(REPO)),
    "extracted": result.get("extracted"),
}
print(json.dumps(summary, indent=2))
if not all_passed:
    sys.exit(1)
