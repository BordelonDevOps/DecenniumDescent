#!/usr/bin/env python3
"""Independently verify and record Director Return331 (HOLD only).

This script verifies the sealed input package, extracts its evidence, and advances
the review ledger without changing canonical spell data or application state.
"""

from __future__ import annotations

import copy
import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


A = Path(__file__).resolve().parent
ROOT = A.parents[4]
RECEIVED = A / "rank9_summon_elemental_avatar_return331_received"
ARCHIVE = RECEIVED / "DD_SummonElementalAvatar_Director_Return331_HELD.zip"
DELIVERY = RECEIVED / "DD_SummonElementalAvatar_Director_Return331_HELD_DELIVERY.json"
PAYLOAD = RECEIVED / "payload"
QUEUE_IN = A / "CURRENT_SPELL_QUEUE_329.json"
HANDOFF_IN = A / "CURRENT_HANDOFF_329.json"
PENDING_IN = A / "CURRENT25_PENDING_IDENTITY_AUDIT_329.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc32(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha256(data),
        "crc32": crc32(data),
    }


def main() -> None:
    delivery = read_json(DELIVERY)
    archive_bytes = ARCHIVE.read_bytes()
    checks: list[dict] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"id": name, "passed": bool(passed), "detail": detail})

    expected_archive = delivery["archive"]
    check("archive-name", expected_archive["fileName"] == ARCHIVE.name, ARCHIVE.name)
    check("archive-size", expected_archive["bytes"] == len(archive_bytes), str(len(archive_bytes)))
    check("archive-sha256", expected_archive["sha256"] == sha256(archive_bytes), sha256(archive_bytes))
    check("archive-crc32", expected_archive["crc32"] == crc32(archive_bytes), crc32(archive_bytes))

    member_results: list[dict] = []
    path_safe = True
    with ZipFile(ARCHIVE) as archive:
        bad_member = archive.testzip()
        names = archive.namelist()
        for name in names:
            member_path = PurePosixPath(name)
            if member_path.is_absolute() or ".." in member_path.parts or "\\" in name:
                path_safe = False
            data = archive.read(name)
            member_results.append(
                {"path": name, "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)}
            )
        check("zip-crc", bad_member is None, str(bad_member))
        check("member-path-safety", path_safe, "No absolute, parent-traversal, or backslash member paths.")
        check("archive-member-count", len(names) == delivery["archiveMemberCount"] == 24, str(len(names)))
        check("delivery-member-count", len(delivery["members"]) == len(names) == delivery["archiveMemberCount"], str(len(delivery["members"])))
        declared = {row["path"]: row for row in delivery["members"]}
        actual = {row["path"]: row for row in member_results}
        member_match = set(declared) == set(actual)
        for name, expected in declared.items():
            observed = actual.get(name, {})
            member_match = member_match and all(observed.get(k) == expected.get(k) for k in ("bytes", "sha256", "crc32"))
        check("delivery-manifest", member_match, f"Compared {len(declared)} archive member bindings.")
        embedded_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        payload_declared = {row["path"]: row for row in embedded_manifest["members"]}
        actual_payload = {row["path"]: row for row in member_results if row["path"] != "MEMBER_MANIFEST.json"}
        payload_match = set(payload_declared) == set(actual_payload)
        for name, expected in payload_declared.items():
            observed = actual_payload.get(name, {})
            payload_match = payload_match and all(observed.get(k) == expected.get(k) for k in ("bytes", "sha256", "crc32"))
        payload_match = payload_match and embedded_manifest.get("payloadMemberCount") == len(actual_payload) == delivery["payloadMemberCount"]
        check("embedded-member-manifest", payload_match, f"Compared {len(payload_declared)} payload member bindings.")

        if not path_safe or bad_member is not None:
            raise RuntimeError("Archive failed a path-safety or CRC check; no extraction performed.")
        if PAYLOAD.exists() and any(PAYLOAD.iterdir()):
            for name in names:
                extracted = PAYLOAD.joinpath(*PurePosixPath(name).parts)
                if not extracted.is_file() or extracted.read_bytes() != archive.read(name):
                    raise RuntimeError(f"Existing extraction does not match sealed archive member: {name}")
        else:
            PAYLOAD.mkdir(parents=True, exist_ok=True)
            archive.extractall(PAYLOAD)

    decision = read_json(PAYLOAD / "DIRECTOR_DECISION.json")
    counts = read_json(PAYLOAD / "COUNTS.json")
    cases = read_json(PAYLOAD / "CASE_RESULTS.json")
    findings = read_json(PAYLOAD / "EXACT_REMAINING_FINDINGS.json")
    authority = read_json(PAYLOAD / "CURRENT_AUTHORITY.json")

    check("decision-scope", decision.get("scopeIds") == ["summon-elemental-avatar"] and decision.get("blockerIds") == ["SH202-B01"], str(decision.get("scopeIds")))
    check("held-only", decision.get("decision") == "HOLD" and decision.get("heldIds") == ["summon-elemental-avatar"] and not decision.get("acceptedIds") and not decision.get("appliedIds"), str(decision.get("decision")))
    check("no-application-authorization", not decision.get("applicationAuthorizedIds") and decision.get("applicationAuthorization") is None and decision.get("applicationPerformed") is False, "No application authorized or performed.")
    check("authority-preserved", decision.get("authorityAfter") == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}, json.dumps(decision.get("authorityAfter"), sort_keys=True))
    check("case-dispositions", cases.get("semanticCasesInspected") == 6 and cases.get("completePassingCases") == 0 and cases.get("partialIncompleteCases") == 4 and cases.get("semanticFailureCases") == 2, "6 inspected; 0 pass, 4 incomplete, 2 fail.")
    check("findings", {row.get("id") for row in findings.get("findings", [])} == {"SH331-C01", "SH331-C02", "SH331-C03"}, "Three exact residual findings recorded.")
    check("next-identity", decision.get("nextIdentity") == "summon-herald-of-the-planes" and decision.get("nextBlockerIds") == ["SH202-B02"], str(decision.get("nextIdentity")))
    check("fixture-provenance", "not campaign gameplay" in decision.get("fixtureProvenance", "") and "not attributed to the user" in decision.get("fixtureProvenance", ""), decision.get("fixtureProvenance", ""))
    check("no-canonical-mutation", decision.get("canonicalFilesEdited") is False and delivery.get("noApplicationOrCanonicalMutation") is True, "No canonical edits or application.")
    check("counts-agree", counts.get("authority") == decision.get("authorityAfter") and counts.get("semanticCompletePass") == 0, "Decision and count records agree.")
    check("authority-binding", authority.get("authority") == decision.get("authorityAfter"), "Embedded current authority agrees with sealed return.")

    if any(not row["passed"] for row in checks):
        failures = [row for row in checks if not row["passed"]]
        raise RuntimeError("Return331 verification failed: " + json.dumps(failures, ensure_ascii=False))

    recorded = datetime.now(timezone.utc).isoformat(timespec="seconds")
    audit = {
        "id": "SUMMON-ELEMENTAL-AVATAR-RETURN331-INDEPENDENT-AUDIT",
        "recordedAtUtc": recorded,
        "status": "PASS_RETURN331_SEALED_HOLD_SH202_B01",
        "archive": bind(ARCHIVE),
        "delivery": bind(DELIVERY),
        "archiveMemberCount": len(member_results),
        "payloadMemberCount": len(delivery["members"]),
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": sum(not row["passed"] for row in checks),
        "decision": "HOLD",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-elemental-avatar"],
        "authority": decision["authorityAfter"],
        "nextIdentity": decision["nextIdentity"],
        "nextBlockerIds": decision["nextBlockerIds"],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    audit_path = A / "SUMMON_ELEMENTAL_AVATAR_RETURN331_INDEPENDENT_AUDIT.json"
    receipt_path = A / "SUMMON_ELEMENTAL_AVATAR_RETURN331_RECEIPT.json"
    write_json(audit_path, audit)
    receipt = {
        "id": "SUMMON-ELEMENTAL-AVATAR-RETURN331-RECEIPT",
        "recordedAtUtc": recorded,
        "decision": "HOLD",
        "blockerIds": ["SH202-B01"],
        "archive": bind(ARCHIVE),
        "delivery": bind(DELIVERY),
        "decisionFile": bind(PAYLOAD / "DIRECTOR_DECISION.json"),
        "casesFile": bind(PAYLOAD / "CASE_RESULTS.json"),
        "findingsFile": bind(PAYLOAD / "EXACT_REMAINING_FINDINGS.json"),
        "independentAudit": bind(audit_path),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-elemental-avatar"],
        "applicationAuthorizedIds": [],
        "authority": decision["authorityAfter"],
        "nextIdentity": decision["nextIdentity"],
        "nextBlockerIds": decision["nextBlockerIds"],
        "immediateCorrectionTarget": decision["immediateCorrectionTarget"],
        "minimumNextAction": decision["minimumNextAction"],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    write_json(receipt_path, receipt)

    queue = read_json(QUEUE_IN)
    pending_audit = read_json(PENDING_IN)
    handoff = read_json(HANDOFF_IN)
    queue_path = A / "CURRENT_SPELL_QUEUE_331.json"
    pending_path = A / "CURRENT25_PENDING_IDENTITY_AUDIT_331.json"
    handoff_path = A / "CURRENT_HANDOFF_331.json"
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_331.md"

    queue_ref = bind(QUEUE_IN)
    audit_ref = bind(audit_path)
    receipt_ref = bind(receipt_path)
    archive_ref = bind(ARCHIVE)
    delivery_ref = bind(DELIVERY)
    decision_ref = bind(PAYLOAD / "DIRECTOR_DECISION.json")
    next_id = "summon-herald-of-the-planes"
    next_blocker = "SH202-B02"
    authority_after = decision["authorityAfter"]

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-331",
        "recordedAtUtc": recorded,
        "supersedesQueue": queue_ref,
        "currentAuthority": authority_after,
        "pendingCount": 25,
        "acceptedUnapplied": 0,
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "nextGroup": "rank9-summon-hosts5",
        "next": next_id,
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "heldThisStep": ["summon-elemental-avatar"],
        "currentPendingIdentityAudit": "CURRENT25_PENDING_IDENTITY_AUDIT_331.json",
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoff": "CURRENT_HANDOFF_331.json",
        "currentPacket": None,
        "currentPacketStatus": "RETURN331_AVATAR_HELD_HERALD_OF_PLANES_SH202_B02_NEXT",
        "activeReview": {"spellId": next_id, "blockerIds": [next_blocker], "packet": None, "status": "DIRECTOR_RETURN331_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["summon-elemental-avatar"],
        "currentReturnBlockers": {"summon-elemental-avatar": ["SH202-B01"]},
        "currentDirectorInstruction": "Return331 holds Summon Elemental Avatar / SH202-B01. Preserve its exact three findings for a compact corrected six-case transition delta; the Director-designated next queue identity is Summon Herald of the Planes / SH202-B02. No source search or user permission is needed for the Avatar correction. Apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return331 independently verified: Avatar remains held, with 25 pending. Proceed to Summon Herald of the Planes / SH202-B02, preserving the exact Avatar correction obligation.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    write_json(queue_path, queue)

    pending_audit.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-331",
        "recordedAtUtc": recorded,
        "status": "PASS_CURRENT_823_25_RETURN331_AVATAR_HOLD_HERALD_NEXT",
        "supersedes": PENDING_IN.name,
        "authority": authority_after,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": ["summon-elemental-avatar"],
        "separatelyHeldIds": sorted(set(pending_audit.get("separatelyHeldIds", [])) | {"summon-elemental-avatar"}),
        "nextGroup": "rank9-summon-hosts5",
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "nextStep": "Review Summon Herald of the Planes / SH202-B02 using its current source and prior Return285 evidence. Preserve the exact Summon Elemental Avatar / SH202-B01 correction findings SH331-C01–C03 for a compact observed six-case transition delta. Apply only an exact sealed acceptance.",
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
    write_json(pending_path, pending_audit)

    handoff.update({
        "id": "CURRENT-HANDOFF-331",
        "recordedAtUtc": recorded,
        "supersedes": HANDOFF_IN.name,
        "status": "RETURN331_VERIFIED_AVATAR_HELD_HERALD_NEXT_823_25_0",
        "authority": authority_after,
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "queueBinding": bind(queue_path),
        "pendingIdentityAudit": pending_path.name,
        "pendingIdentityAuditBinding": bind(pending_path),
        "currentDirectorReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "heldThisStep": ["summon-elemental-avatar"],
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": next_id, "blockerId": next_blocker, "group": "rank9-summon-hosts5"},
        "nextPendingGroup": {"group": "rank9-summon-hosts5", "pendingIds": [next_id], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Summon Herald of the Planes / SH202-B02. Keep Avatar correction findings SH331-C01–C03 open; make no application without an exact sealed acceptance.",
        "directorConnectionStatus": "Return331 sealed Avatar HOLD; the Director designates Summon Herald of the Planes / SH202-B02 as next.",
    })
    write_json(handoff_path, handoff)

    snapshot_path.write_text(
        "# Spell review status — queue 331\n\n"
        "Return331 holds Summon Elemental Avatar / SH202-B01. Independent verification passed "
        f"{len(checks)}/{len(checks)} checks. Authority remains **823 applied, 25 pending, 0 accepted-unapplied** "
        "(547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "The Director found four incomplete cases and two failures: no observed reversible state transitions; "
        "C02 needs a valid recipient/root settlement; C03 must cancel the old controller’s unexecuted remainder "
        "and deny the third strike. The synthetic fixtures remain conditional review inputs, not campaign gameplay.\n\n"
        f"Next Director-prioritized identity: **Summon Herald of the Planes / SH202-B02**. The Avatar correction "
        "remains an open follow-up. No canonical files changed and no application was performed.\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "receipt": str(receipt_path),
        "audit": str(audit_path),
        "checks": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": sum(not row["passed"] for row in checks),
        "decision": "HOLD",
        "accepted": [],
        "applied": [],
        "pending": 25,
        "next": next_id,
        "payloadFiles": len(member_results),
    }, indent=2))


if __name__ == "__main__":
    main()
