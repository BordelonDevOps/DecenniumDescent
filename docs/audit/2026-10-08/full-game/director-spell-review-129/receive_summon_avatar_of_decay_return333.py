#!/usr/bin/env python3
"""Independently verify and record Director Return333; do not edit canonical spell data."""

from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
RECEIVED = A / "rank9_summon_avatar_of_decay_return333_received"
ARCHIVE = RECEIVED / "DD_SummonAvatarOfDecay_Director_Return333_HELD.zip"
DELIVERY = RECEIVED / "DD_SummonAvatarOfDecay_Director_Return333_HELD_DELIVERY.json"
PAYLOAD = RECEIVED / "payload"
QUEUE_IN = A / "CURRENT_SPELL_QUEUE_332.json"
PENDING_IN = A / "CURRENT25_PENDING_IDENTITY_AUDIT_332.json"
HANDOFF_IN = A / "CURRENT_HANDOFF_332.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc32(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)}


def main() -> None:
    delivery = load(DELIVERY)
    archive_bytes = ARCHIVE.read_bytes()
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"id": name, "passed": bool(ok), "detail": detail})

    archive_binding = delivery["archive"]
    check("archive-name", archive_binding.get("fileName") == ARCHIVE.name, ARCHIVE.name)
    check("archive-size", archive_binding.get("bytes") == len(archive_bytes) == 180837, str(len(archive_bytes)))
    check("archive-sha256", archive_binding.get("sha256") == sha256(archive_bytes) == "93c63971f08e74f2526b050e9301b80ccff9746d4089e9d638306acdcef16f44", sha256(archive_bytes))
    check("archive-crc32", archive_binding.get("crc32") == crc32(archive_bytes) == "926fb885", crc32(archive_bytes))

    member_rows = []
    names_safe = True
    duplicate_names = False
    with ZipFile(ARCHIVE) as archive:
        bad = archive.testzip()
        names = archive.namelist()
        duplicate_names = len(names) != len(set(names))
        for name in names:
            part = PurePosixPath(name)
            if part.is_absolute() or ".." in part.parts or "\\" in name:
                names_safe = False
            data = archive.read(name)
            member_rows.append({"path": name, "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)})
        check("zip-crc", bad is None, str(bad))
        check("member-path-safety", names_safe, "No absolute or traversal paths.")
        check("member-name-uniqueness", not duplicate_names, f"{len(names)} unique path entries.")
        check("archive-member-count", len(names) == delivery.get("archiveMemberCount") == 41, str(len(names)))
        declared = {row["path"]: row for row in delivery.get("members", [])}
        observed = {row["path"]: row for row in member_rows}
        exact = set(declared) == set(observed)
        for name, row in declared.items():
            actual = observed.get(name, {})
            exact = exact and all(actual.get(k) == row.get(k) for k in ("bytes", "sha256", "crc32"))
        exact = exact and set(delivery.get("exactAllowlist", [])) == set(observed)
        check("delivery-member-bindings-and-allowlist", exact and len(declared) == 41, f"Compared {len(declared)} member rows and allowlist.")
        if not names_safe or bad or duplicate_names:
            raise RuntimeError("Unsafe, corrupt, or duplicate-member archive; extraction refused.")
        if PAYLOAD.exists() and any(PAYLOAD.iterdir()):
            for name in names:
                extracted = PAYLOAD.joinpath(*PurePosixPath(name).parts)
                if not extracted.is_file() or extracted.read_bytes() != archive.read(name):
                    raise RuntimeError(f"Existing extraction mismatch: {name}")
        else:
            PAYLOAD.mkdir(parents=True, exist_ok=True)
            archive.extractall(PAYLOAD)

    decision = load(PAYLOAD / "DIRECTOR_DECISION.json")
    counts = load(PAYLOAD / "COUNTS.json")
    residuals = load(PAYLOAD / "RESIDUAL_BRANCH_DISPOSITIONS.json")
    semantic = load(PAYLOAD / "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
    input_findings = load(PAYLOAD / "INPUT_PACKAGE_FINDINGS.json")
    source_checks = load(PAYLOAD / "SOURCE_DATA_CHECKS.json")
    input_bindings = load(PAYLOAD / "INPUT_BINDINGS.json")
    member_manifest = load(PAYLOAD / "MEMBER_MANIFEST.json")
    input_manifest = load(PAYLOAD / "input/MEMBER_MANIFEST.json")
    inputs = input_bindings.get("inputMembers", [])
    input_rows = {row.get("path"): row for row in inputs}

    check("decision-scope", decision.get("scopeIds") == ["summon-avatar-of-decay"] and decision.get("blockerIds") == ["SH202-B03"], str(decision.get("scopeIds")))
    check("held-not-accepted", decision.get("decision") == "HOLD" and decision.get("heldIds") == ["summon-avatar-of-decay"] and not decision.get("acceptedIds") and not decision.get("appliedIds"), decision.get("decision", ""))
    check("no-application-authorized", decision.get("applicationAuthorizedIds") == [] and decision.get("applicationPerformed") is False, "No authorization or application.")
    expected_authority = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
    check("authority-preserved", decision.get("authorityBefore") == expected_authority == decision.get("authorityAfter"), json.dumps(decision.get("authorityAfter"), sort_keys=True))
    check("seven-component-reversals", counts.get("newConditionalComponentCases") == 7 and counts.get("newConditionalEvents") == 12 and counts.get("forwardOperations") == counts.get("inverseOperations") == 44 and counts.get("fullReverseTraversals") == 7, json.dumps({k: counts.get(k) for k in ("newConditionalComponentCases", "newConditionalEvents", "forwardOperations", "inverseOperations", "fullReverseTraversals")}))
    check("historical-replay-not-repeated", counts.get("historicalCasesHashVerified") == 13 and counts.get("historicalCasesFreshlyReplayed") == 0 and counts.get("historicalEventsNotReplayed") == 2209, json.dumps({k: counts.get(k) for k in ("historicalCasesHashVerified", "historicalCasesFreshlyReplayed", "historicalEventsNotReplayed")}))
    check("four-residual-branches", [row.get("id") for row in residuals.get("branches", [])] == ["SH333-R01", "SH333-R02", "SH333-R03", "SH333-R04"], "R01–R04 are separately recorded.")
    check("whole-identity-semantic-hold", semantic.get("wholeIdentity") == "HOLD" and semantic.get("semanticCompletion") is False, json.dumps({k: semantic.get(k) for k in ("wholeIdentity", "semanticCompletion")}))
    check("source-manifest-finding-disclosed", input_findings.get("semanticBlocker") is False and input_findings.get("internalManifest") == "STALE_SELF_ROW_AND_UNLISTED_REQUEST" and len(input_findings.get("mismatches", [])) == 1 and input_findings.get("unlistedMembers") == ["REQUEST_333.md"], json.dumps(input_findings, ensure_ascii=False)[:1000])
    source_rows_pass = len(source_checks.get("checks", [])) == 43 and all(row.get("passed") is True for row in source_checks.get("checks", []))
    check("source-and-data-checks", source_checks.get("status") == "PASS_WITH_DISCLOSED_INPUT_MANIFEST_FINDING" and source_checks.get("checkCount") == 43 and source_rows_pass, json.dumps({"status": source_checks.get("status"), "checkCount": source_checks.get("checkCount"), "passedRows": sum(row.get("passed") is True for row in source_checks.get("checks", []))}))
    check("input-request-binding", input_rows.get("REQUEST_333.md", {}).get("sha256") == "36f126614599b4f9c38eb79dd52fe0f696b2967e2a122a0b8d9be76eceae3e42", str(input_rows.get("REQUEST_333.md", {}).get("sha256")))
    check("input-manifest-defect-precisely-scoped", input_findings["mismatches"][0].get("path") == "MEMBER_MANIFEST.json" and "next successor" in input_findings.get("explanation", ""), "Only the input package manifest discrepancy is disclosed.")
    check("complete-output-payload-manifest", len(member_manifest.get("members", [])) == delivery.get("payloadMemberCount") == 40 and member_manifest.get("payloadMemberCount") == 40, str(member_manifest.get("payloadMemberCount")))
    check("retained-prior-finding-holds", decision.get("avatarFindingsRemainOpen") == ["SH331-C01", "SH331-C02", "SH331-C03"] and decision.get("heraldWitnessesRemainOpen") == ["SH332-W01", "SH332-W02", "SH332-W03", "SH332-W04"], "SH331 and SH332 findings remain open.")
    check("next-identity", decision.get("nextIdentity") == "reverse-gravity-field" and decision.get("nextBlockerIds") == ["IE204-B02"] and decision.get("nextGroup") == "rank9-impact-exile4", str(decision.get("nextIdentity")))
    check("fixture-provenance", "not campaign events" in decision.get("fixtureProvenance", "") and "not attributed to the user" in decision.get("fixtureProvenance", ""), decision.get("fixtureProvenance", ""))
    check("no-canonical-change", decision.get("canonicalChanges") is False and decision.get("applicationPerformed") is False and decision.get("githubChanges") is False and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("applicationAuthorizedIds") == [], "Canonical data untouched; hold only.")

    for label, path, expected_key in [
        ("current catalog binding", CATALOG, "currentCatalog"),
        ("current index binding", INDEX, "currentIndex"),
        ("Queue332 binding", QUEUE_IN, "queue332"),
        ("pending audit332 binding", PENDING_IN, "pendingAudit332"),
    ]:
        expected = input_bindings.get(expected_key, {})
        actual = bind(path)
        check(label, all(actual.get(k) == expected.get(k) for k in ("bytes", "sha256", "crc32")), json.dumps(actual, sort_keys=True))
    check("input-member-manifest-finding-matches-archive", len(input_manifest.get("members", [])) == 10 and input_findings.get("mismatches", [{}])[0].get("expected", {}).get("sha256") == next((row.get("sha256") for row in input_manifest.get("members", []) if row.get("path") == "MEMBER_MANIFEST.json"), None), "The stale self-row is bound to the preserved input manifest.")

    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return333 verification failed: " + json.dumps([row for row in checks if not row["passed"]], ensure_ascii=False))

    recorded = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    audit_path = A / "SUMMON_AVATAR_DECAY_RETURN333_INDEPENDENT_AUDIT.json"
    receipt_path = A / "SUMMON_AVATAR_DECAY_RETURN333_RECEIPT.json"
    authority = decision["authorityAfter"]
    next_id, next_blocker, next_group = "reverse-gravity-field", "IE204-B02", "rank9-impact-exile4"
    queue_path = A / "CURRENT_SPELL_QUEUE_333.json"
    pending_path = A / "CURRENT25_PENDING_IDENTITY_AUDIT_333.json"
    handoff_path = A / "CURRENT_HANDOFF_333.json"
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_333.md"

    audit = {
        "id": "SUMMON-AVATAR-DECAY-RETURN333-INDEPENDENT-AUDIT",
        "recordedAtUtc": recorded,
        "status": "PASS_RETURN333_SEALED_HOLD_SH202_B03",
        "archive": archive_ref,
        "delivery": delivery_ref,
        "archiveMemberCount": len(member_rows),
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": sum(not row["passed"] for row in checks),
        "decision": "HOLD",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-avatar-of-decay"],
        "applicationAuthorizedIds": [],
        "authority": authority,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "inputManifestFinding": input_findings,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(audit_path, audit)

    receipt = {
        "id": "SUMMON-AVATAR-DECAY-RETURN333-RECEIPT",
        "recordedAtUtc": recorded,
        "decision": "HOLD",
        "blockerIds": ["SH202-B03"],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "residualBranchDispositions": bind(PAYLOAD / "RESIDUAL_BRANCH_DISPOSITIONS.json"),
        "semanticFailureCheck": bind(PAYLOAD / "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"),
        "independentAudit": bind(audit_path),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-avatar-of-decay"],
        "applicationAuthorizedIds": [],
        "authority": authority,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "openResidualBranchIds": ["SH333-R01", "SH333-R02", "SH333-R03", "SH333-R04"],
        "priorAvatarFindingsRemainOpen": decision["avatarFindingsRemainOpen"],
        "priorHeraldWitnessesRemainOpen": decision["heraldWitnessesRemainOpen"],
        "inputManifestFinding": input_findings,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(receipt_path, receipt)

    queue = load(QUEUE_IN)
    pending = load(PENDING_IN)
    handoff = load(HANDOFF_IN)
    held_before = set(queue.get("separatelyRetainedHolds", []))
    held_before.update({"summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"})
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    audit_ref, receipt_ref, decision_ref = bind(audit_path), bind(receipt_path), bind(decision_path)

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-333",
        "recordedAtUtc": recorded,
        "supersedesQueue": bind(QUEUE_IN),
        "currentAuthority": authority,
        "pendingCount": 25,
        "acceptedUnapplied": 0,
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "nextGroup": next_group,
        "next": next_id,
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "heldThisStep": ["summon-avatar-of-decay"],
        "separatelyRetainedHolds": sorted(held_before),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoff": handoff_path.relative_to(ROOT).as_posix(),
        "currentPacket": None,
        "currentPacketStatus": "RETURN333_AVATAR_DECAY_HELD_REVERSE_GRAVITY_FIELD_IE204_B02_NEXT",
        "activeReview": {"spellId": next_id, "blockerIds": [next_blocker], "packet": None, "status": "DIRECTOR_RETURN333_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["summon-avatar-of-decay"],
        "currentReturnBlockers": {
            "summon-elemental-avatar": ["SH202-B01"],
            "summon-herald-of-the-planes": ["SH202-B02"],
            "summon-avatar-of-decay": ["SH202-B03"],
        },
        "currentDirectorInstruction": "Return333 holds Summon Avatar of Decay / SH202-B03. Preserve SH331-C01–C03 and SH332-W01–W04. The Director-designated next priority is Reverse Gravity Field / IE204-B02. Do not replay the 13 prior cases or apply without an exact sealed acceptance.",
        "directorConnectionStatus": "Return333 independently verified. Avatar of Decay remains held; next is Reverse Gravity Field / IE204-B02.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    save(queue_path, queue)

    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-333",
        "recordedAtUtc": recorded,
        "status": "PASS_CURRENT_823_25_RETURN333_AVATAR_DECAY_HOLD_REVERSE_GRAVITY_NEXT",
        "supersedes": PENDING_IN.name,
        "authority": authority,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": ["summon-avatar-of-decay"],
        "separatelyHeldIds": sorted(held_before),
        "nextGroup": next_group,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "nextStep": "Review Reverse Gravity Field / IE204-B02 using its current source and bound review history. Keep SH331-C01–C03, SH332-W01–W04, and SH333-R01–R04 open. Apply only an exact sealed acceptance.",
        "sourceQueue": queue_path.relative_to(ROOT).as_posix(),
        "currentQueueBinding": bind(queue_path),
        "currentReturn": receipt_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnReceipt": receipt_ref,
        "noPendingTargetSilentlyAccepted": True,
        "allCurrentPendingIdentitiesReviewed": True,
        "unreviewedPendingIds": [],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    })
    save(pending_path, pending)

    handoff.update({
        "id": "CURRENT-HANDOFF-333",
        "recordedAtUtc": recorded,
        "supersedes": HANDOFF_IN.name,
        "status": "RETURN333_VERIFIED_AVATAR_DECAY_HELD_REVERSE_GRAVITY_NEXT_823_25_0",
        "authority": authority,
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "queueBinding": bind(queue_path),
        "pendingIdentityAudit": pending_path.name,
        "pendingIdentityAuditBinding": bind(pending_path),
        "currentDirectorReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "heldThisStep": ["summon-avatar-of-decay"],
        "separatelyRetainedHolds": sorted(held_before),
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": next_id, "blockerId": next_blocker, "group": next_group},
        "nextPendingGroup": {"group": next_group, "pendingIds": [next_id], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Reverse Gravity Field / IE204-B02. Preserve SH331-C01–C03, SH332-W01–W04, and SH333-R01–R04 as separate open items; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return333 sealed Avatar of Decay HOLD; the Director designates Reverse Gravity Field / IE204-B02 as next.",
    })
    save(handoff_path, handoff)

    snapshot_path.write_text(
        "# Spell review status — queue 333\n\n"
        "Return333 holds Summon Avatar of Decay / SH202-B03. Independent verification passed "
        f"{len(checks)}/{len(checks)} checks. Authority remains **823 applied, 25 pending, 0 accepted-unapplied** "
        "(547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "Seven Director-authored conditional component tests passed (12 transitions; 44 forward and 44 inverse operations; "
        "seven reversals), but no complete paid/source-qualified witness closes the four residual branches SH333-R01–R04. "
        "The 13 historical cases were not replayed. The input package’s stale self-manifest row and omitted request are "
        "disclosed without changing their source bytes. SH331-C01–C03 and SH332-W01–W04 remain open.\n\n"
        f"Next Director-prioritized identity: **Reverse Gravity Field / IE204-B02**. No canonical files changed and no application was performed.\n",
        encoding="utf-8",
    )
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": sum(row["passed"] for row in checks), "failed": sum(not row["passed"] for row in checks), "held": "summon-avatar-of-decay", "pending": 25, "next": next_id, "payloadFiles": len(member_rows)}, indent=2))


if __name__ == "__main__":
    main()
