#!/usr/bin/env python3
"""Independently verify and record Director Return336; never edit canonical spell data."""

from __future__ import annotations

import hashlib
import json
import shutil
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
RECEIVED = A / "rank9_alignment_perfection_return336_received"
ARCHIVE = RECEIVED / "DD_AlignmentPerfection_Director_Return336_HELD.zip"
DELIVERY = RECEIVED / "DD_AlignmentPerfection_Director_Return336_HELD_DELIVERY.json"
PAYLOAD = RECEIVED / "payload"
DOWNLOADS = Path(r"C:\Users\cbord\Downloads")
QUEUE_IN = A / "CURRENT_SPELL_QUEUE_335.json"
PENDING_IN = A / "CURRENT25_PENDING_IDENTITY_AUDIT_335.json"
HANDOFF_IN = A / "CURRENT_HANDOFF_335.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc32(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)}


def main() -> None:
    RECEIVED.mkdir(parents=True, exist_ok=True)
    source_archive = DOWNLOADS / ARCHIVE.name
    source_delivery = DOWNLOADS / DELIVERY.name
    if source_archive.exists() and source_delivery.exists():
        shutil.copy2(source_archive, ARCHIVE)
        shutil.copy2(source_delivery, DELIVERY)
    delivery = load(DELIVERY)
    archive_bytes = ARCHIVE.read_bytes()
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"id": name, "passed": bool(ok), "detail": detail})

    expected = delivery["archive"]
    check("archive-name", expected.get("fileName") == ARCHIVE.name, ARCHIVE.name)
    check("archive-size", expected.get("bytes") == len(archive_bytes) == 310001, str(len(archive_bytes)))
    check("archive-sha256", expected.get("sha256") == sha256(archive_bytes) == "9a565faac3b3dddb5fdf86bc7bd1259498028b542c945a38ffdebc8e61e47a33", sha256(archive_bytes))
    check("archive-crc32", expected.get("crc32") == crc32(archive_bytes) == "762df56d", crc32(archive_bytes))
    check("delivery-id", delivery.get("id") == "ALIGNMENT-PERFECTION-DIRECTOR-RETURN336-DELIVERY" and delivery.get("reviewId") == "Return336", str(delivery.get("id")))

    member_rows = []
    safe = True
    with ZipFile(ARCHIVE) as archive:
        bad = archive.testzip()
        names = archive.namelist()
        for name in names:
            part = PurePosixPath(name)
            if part.is_absolute() or ".." in part.parts or "\\" in name:
                safe = False
            data = archive.read(name)
            member_rows.append({"path": name, "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)})
        check("zip-crc", bad is None, str(bad))
        check("safe-unique-member-paths", safe and len(names) == len(set(names)), f"{len(names)} unique paths.")
        check("archive-member-count", len(names) == delivery.get("archiveMemberCount") == 28, str(len(names)))
        declared = {row["path"]: row for row in delivery.get("members", [])}
        actual = {row["path"]: row for row in member_rows}
        exact = set(declared) == set(actual) == set(delivery.get("exactAllowlist", []))
        for name, row in declared.items():
            got = actual.get(name, {})
            exact = exact and all(got.get(k) == row.get(k) for k in ("bytes", "sha256", "crc32"))
        check("external-member-bindings-and-allowlist", exact and len(declared) == 28, f"Compared {len(declared)} members.")
        if not safe or bad or not exact:
            raise RuntimeError("Unsafe, corrupt, or unbound archive; extraction refused.")
        if PAYLOAD.exists() and any(PAYLOAD.iterdir()):
            for name in names:
                path = PAYLOAD.joinpath(*PurePosixPath(name).parts)
                if not path.is_file() or path.read_bytes() != archive.read(name):
                    raise RuntimeError(f"Existing extraction mismatch: {name}")
        else:
            PAYLOAD.mkdir(parents=True, exist_ok=True)
            for name in names:
                path = PAYLOAD.joinpath(*PurePosixPath(name).parts)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(archive.read(name))

    decision = load(PAYLOAD / "DIRECTOR_DECISION.json")
    counts = load(PAYLOAD / "COUNTS.json")
    hold = load(PAYLOAD / "HOLD_REGISTER.json")
    cases = load(PAYLOAD / "CASE_COVERAGE.json")
    procedure = load(PAYLOAD / "PROCEDURE_STATUS.json")
    validation = load(PAYLOAD / "VALIDATION.json")
    semantics = load(PAYLOAD / "SEMANTIC_RECONCILIATION.json")
    boundaries = load(PAYLOAD / "BOUNDARY_RECONCILIATION.json")
    qualifications = load(PAYLOAD / "QUALIFICATIONS.json")
    source_reconciliation = load(PAYLOAD / "SOURCE_RECONCILIATION.json")
    manifest = load(PAYLOAD / "MEMBER_MANIFEST.json")

    check("decision-scope", decision.get("reviewedIds") == ["alignment-perfection"] and decision.get("groupId") == "rank9-alignment-faction-purification5", str(decision.get("reviewedIds")))
    check("held-not-accepted-or-applied", decision.get("heldIds") == ["alignment-perfection"] and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("decisions", [{}])[0].get("decision") == "HOLD", str(decision.get("heldIds")))
    check("application-not-authorized", decision.get("applicationAuthorization") == {"authorized": False, "authorizedIds": [], "canonicalMutationAuthorized": False} and decision.get("canonicalMutation") is False, "No application or canonical mutation authorization.")
    authority = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
    check("authority-preserved", decision.get("authorityBefore") == authority == decision.get("authorityAfter") == counts.get("authority"), json.dumps(decision.get("authorityAfter"), sort_keys=True))
    check("next-director-priority", decision.get("nextPendingIdentity") == "faction-incarnate" and decision.get("nextBlockerId") == "AFP211-B03" and decision.get("nextPendingGroup") == "rank9-alignment-faction-purification5", str(decision.get("nextPendingIdentity")))
    reqs = hold.get("requirements", [])
    check("exact-three-open-contracts", [row.get("id") for row in reqs] == ["AFP336-W01", "AFP336-W02", "AFP336-W03"] and all(row.get("parentBlocker") == "AFP211-B02" and row.get("status") == "OPEN" for row in reqs), "Cleansing authority, useful benefit map, and benefit lifecycle.")
    check("question-allocation", {row.get("id"): row.get("questions") for row in reqs} == {"AFP336-W01": ["AP9-09", "AP9-11"], "AFP336-W02": ["AP9-10"], "AFP336-W03": ["AP9-12"]}, "Spell-specific question dispositions preserved.")
    check("integrated-witness-missing", hold.get("minimumIntegratedWitness", {}).get("status") == "MISSING_AFTER_CONTRACT_SELECTION" and hold.get("minimumIntegratedWitness", {}).get("newWitnessExecuted") is False and counts.get("completePaidPositiveEncounters") == 0, "No complete paid positive encounters.")
    check("native-procedure-incomplete", procedure.get("status") == "SOURCE_BOUND_INCOMPLETE_NOT_OPERATIONAL" and procedure.get("accepted") is False and procedure.get("applied") is False and procedure.get("nativeCard", {}).get("operational") is None, str(procedure.get("status")))
    case_rows = cases.get("rows", [])
    check("prior-cases-preserved-not-replayed", {row.get("id") for row in case_rows} == {"AFP211-AP-underlying-removal", "AFP211-AP-undefined-benefit"} and all(row.get("freshReplay") == "NOT_RUN_BY_EXPLICIT_REQUEST" and row.get("freshReaudit") == "NOT_RUN_BY_EXPLICIT_REQUEST" and row.get("completePositiveEncounter") is False for row in case_rows) and cases.get("freshCaseReplays") == 0 and cases.get("freshCaseReaudits") == 0, "Both prior conditional components retained without replay or re-audit.")
    check("source-checks-pass", validation.get("status") == "PASS" and validation.get("checkCount") == 75 and validation.get("passed") == 75 and validation.get("failed") == 0 and counts.get("sourceDataChecksPassed") == 75 and counts.get("sourceDataChecksFailed") == 0, "75 passed, 0 failed.")
    check("semantic-hold-aligned", semantics.get("status") == "HOLD" and semantics.get("passed") == 5 and semantics.get("held") == 3 and counts.get("semanticHeldFindings") == 3, "Three semantic findings remain held.")
    check("comparator-finding-remains-closed", boundaries.get("closedEvidenceFinding", {}).get("id") == "AFP211-E01" and boundaries.get("closedEvidenceFinding", {}).get("status") == "CLOSED" and boundaries.get("parentBlockerClosed") is False and boundaries.get("anyComparatorReaccepted") is False, "AFP211-E01 stays closed; no comparator is reaccepted.")
    check("four-applied-boundaries-retained", len(boundaries.get("fourAppliedSourceRecords", [])) == 4 and all(row.get("currentFileAndCardVerified") is True and row.get("noPerfectionGrant") is True for row in boundaries.get("fourAppliedSourceRecords", [])), "Lock, Anchor, Purge, and Suggestion remain comparison-only.")
    check("fixture-provenance", "not campaign/user events" in decision.get("fixtureProvenance", "") and "not established" in decision.get("fixtureProvenance", ""), decision.get("fixtureProvenance", ""))
    check("qualifications-retained", len(qualifications.get("qualificationIds", [])) == 7 and qualifications.get("noCanonicalIndexCatalogQueueHandoffGitHubMutation") is True, "Seven qualifications retained.")
    check("no-replay-or-event-operations", decision.get("priorCaseReplay") == "NOT_RUN_BY_REQUEST" and counts.get("freshCaseReplays") == 0 and counts.get("freshForwardOperations") == 0 and counts.get("freshInverseOperations") == 0, "No replay or new event operations.")
    check("source-packet-binding", delivery.get("sourcePacket", {}).get("sha256") == "4fd070c97870e8ff843e2ca0d52696ecb467f6e370e416cc3a5e637a92c5d5bc" and delivery.get("sourceDelivery", {}).get("sha256") == "cbd5243f16f1fa1d1a07cf801f9b01f2ba78a42ec530c6a75f8dab013c0d2a7a", "Review336 inputs are bound.")
    check("inner-manifest-payload-count", manifest.get("payloadMemberCount") == delivery.get("payloadMemberCount") == 27 and len(manifest.get("members", [])) == 27, json.dumps({"payload": manifest.get("payloadMemberCount"), "manifestRows": len(manifest.get("members", []))}))
    closed_finding = source_reconciliation.get("closedEvidenceFinding", {})
    check("closed-immunity-boundary-reused", closed_finding.get("id") == "AFP211-E01" and closed_finding.get("status") == "CLOSED" and closed_finding.get("reopened") is False and source_reconciliation.get("priorArchiveReaudited") is False and counts.get("closedImmunityComparisonReused") == 1, "No reopening of prior comparator finding.")
    check("delivery-exact-scope", delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("heldIds") == ["alignment-perfection"] and delivery.get("blockerIds") == ["AFP211-B02"], "Return scope matches the one-identity HOLD.")

    # Confirm the current authority excerpt is tied to the exact local queue335/handoff/pending files.
    queue335 = load(QUEUE_IN)
    pending335 = load(PENDING_IN)
    handoff335 = load(HANDOFF_IN)
    input_authority = load(PAYLOAD / "input/00_CURRENT_AUTHORITY_335.json")
    expected_queue_binding = input_authority.get("queue", {})
    expected_handoff_binding = input_authority.get("handoff", {})
    expected_pending_binding = input_authority.get("pendingAudit", {})
    check("queue335-input-binding", expected_queue_binding == bind(QUEUE_IN) and queue335.get("currentAuthority") == authority, json.dumps(expected_queue_binding, sort_keys=True))
    check("handoff335-input-binding", expected_handoff_binding == bind(HANDOFF_IN) and handoff335.get("authority") == authority, json.dumps(expected_handoff_binding, sort_keys=True))
    check("pending335-input-binding", expected_pending_binding == bind(PENDING_IN) and pending335.get("authority") == authority, json.dumps(expected_pending_binding, sort_keys=True))
    check("next-identity-not-already-held", "faction-incarnate" not in queue335.get("separatelyRetainedHolds", []) and "alignment-perfection" not in queue335.get("separatelyRetainedHolds", []), "Return336 adds only Alignment Perfection to retained holds.")

    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return336 verification failed: " + json.dumps([row for row in checks if not row["passed"]], ensure_ascii=False))

    recorded = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    hold_path = PAYLOAD / "HOLD_REGISTER.json"
    audit_path = A / "ALIGNMENT_PERFECTION_RETURN336_INDEPENDENT_AUDIT.json"
    receipt_path = A / "ALIGNMENT_PERFECTION_RETURN336_RECEIPT.json"
    next_id, next_blocker, next_group = "faction-incarnate", "AFP211-B03", "rank9-alignment-faction-purification5"

    audit = {
        "id": "ALIGNMENT-PERFECTION-RETURN336-INDEPENDENT-AUDIT",
        "recordedAtUtc": recorded,
        "status": "PASS_RETURN336_SEALED_HOLD_AFP211_B02",
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
        "heldIds": ["alignment-perfection"],
        "applicationAuthorizedIds": [],
        "authority": authority,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "openContractIds": ["AFP336-W01", "AFP336-W02", "AFP336-W03"],
        "closedEvidenceFinding": "AFP211-E01",
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(audit_path, audit)

    receipt = {
        "id": "ALIGNMENT-PERFECTION-RETURN336-RECEIPT",
        "recordedAtUtc": recorded,
        "decision": "HOLD",
        "blockerIds": ["AFP211-B02"],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "holdRegister": bind(hold_path),
        "independentAudit": bind(audit_path),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["alignment-perfection"],
        "applicationAuthorizedIds": [],
        "openContractIds": ["AFP336-W01", "AFP336-W02", "AFP336-W03"],
        "closedEvidenceFinding": "AFP211-E01",
        "authority": authority,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextGroup": next_group,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(receipt_path, receipt)

    queue_path = A / "CURRENT_SPELL_QUEUE_336.json"
    pending_path = A / "CURRENT25_PENDING_IDENTITY_AUDIT_336.json"
    handoff_path = A / "CURRENT_HANDOFF_336.json"
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_336.md"
    queue = load(QUEUE_IN)
    pending = load(PENDING_IN)
    handoff = load(HANDOFF_IN)
    held = set(queue.get("separatelyRetainedHolds", []))
    held.add("alignment-perfection")
    decision_ref, audit_ref, receipt_ref = bind(decision_path), bind(audit_path), bind(receipt_path)

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-336",
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
        "heldThisStep": ["alignment-perfection"],
        "separatelyRetainedHolds": sorted(held),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoff": handoff_path.relative_to(ROOT).as_posix(),
        "currentPacket": None,
        "currentPacketStatus": "RETURN336_ALIGNMENT_PERFECTION_HELD_FACTION_INCARNATE_AFP211_B03_NEXT",
        "activeReview": {"spellId": next_id, "blockerIds": [next_blocker], "packet": None, "status": "DIRECTOR_RETURN336_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["alignment-perfection"],
        "currentReturnBlockers": {**queue.get("currentReturnBlockers", {}), "alignment-perfection": ["AFP211-B02"]},
        "currentDirectorInstruction": "Return336 holds Alignment Perfection / AFP211-B02. Exact cleansing authority, useful benefit values/use/stacking, and the separate benefit clock remain unresolved; two paid positive/adverse encounters are absent. AFP211-E01 stays closed. The Director-designated next priority is Faction Incarnate / AFP211-B03. Apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return336 independently verified. Alignment Perfection remains held; next is Faction Incarnate / AFP211-B03.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    save(queue_path, queue)

    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-336",
        "recordedAtUtc": recorded,
        "status": "PASS_CURRENT_823_25_RETURN336_ALIGNMENT_PERFECTION_HOLD_FACTION_INCARNATE_NEXT",
        "supersedes": PENDING_IN.name,
        "authority": authority,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": ["alignment-perfection"],
        "separatelyHeldIds": sorted(held),
        "nextGroup": next_group,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "nextStep": "Review Faction Incarnate / AFP211-B03 using current authority and sources. Preserve AFP211-B02 W01-W03 and the closed AFP211-E01 comparator boundary. Apply only an exact sealed acceptance.",
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
        "id": "CURRENT-HANDOFF-336",
        "recordedAtUtc": recorded,
        "supersedes": HANDOFF_IN.name,
        "status": "RETURN336_VERIFIED_ALIGNMENT_PERFECTION_HELD_FACTION_INCARNATE_NEXT_823_25_0",
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
        "heldThisStep": ["alignment-perfection"],
        "separatelyRetainedHolds": sorted(held),
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": next_id, "blockerId": next_blocker, "group": next_group},
        "nextPendingGroup": {"group": next_group, "pendingIds": [next_id], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Faction Incarnate / AFP211-B03. Preserve the Alignment Perfection hold W01-W03 and closed comparator finding AFP211-E01; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return336 sealed Alignment Perfection HOLD; the Director designates Faction Incarnate / AFP211-B03 as next.",
    })
    save(handoff_path, handoff)

    snapshot_path.write_text(
        "# Spell review status — queue 336\n\n"
        f"Return336 holds Alignment Perfection / AFP211-B02. Independent verification passed {len(checks)}/{len(checks)} checks. "
        "Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "The exact cleansing permission, useful axis-dependent benefit values/use/stacking, and a separate benefit lifecycle remain unresolved; two complete paid positive/adverse encounters are absent. "
        "Neither Return287 component was replayed or re-audited. AFP211-E01 remains closed and no comparator powers transfer.\n\n"
        f"Next Director-prioritized identity: **Faction Incarnate / AFP211-B03**. No canonical files changed and no application was performed.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": sum(row["passed"] for row in checks), "failed": sum(not row["passed"] for row in checks), "held": "alignment-perfection", "pending": 25, "next": next_id, "archiveMembers": len(member_rows)}, indent=2))


if __name__ == "__main__":
    main()
