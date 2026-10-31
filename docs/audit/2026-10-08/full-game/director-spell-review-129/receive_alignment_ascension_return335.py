#!/usr/bin/env python3
"""Independently verify and record Director Return335; never edit canonical spell data."""

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
RECEIVED = A / "rank9_alignment_ascension_return335_received"
ARCHIVE = RECEIVED / "DD_AlignmentAscension_Director_Return335_HELD.zip"
DELIVERY = RECEIVED / "DD_AlignmentAscension_Director_Return335_HELD_DELIVERY.json"
PAYLOAD = RECEIVED / "payload"
DOWNLOADS = Path(r"C:\Users\cbord\Downloads")
QUEUE_IN = A / "CURRENT_SPELL_QUEUE_334.json"
PENDING_IN = A / "CURRENT25_PENDING_IDENTITY_AUDIT_334.json"
HANDOFF_IN = A / "CURRENT_HANDOFF_334.json"


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
    check("archive-size", expected.get("bytes") == len(archive_bytes) == 70991, str(len(archive_bytes)))
    check("archive-sha256", expected.get("sha256") == sha256(archive_bytes) == "9fc432fa0cdbddff529f86e20139d647798d7db6a780bfef6a22ae9a6d4c43d2", sha256(archive_bytes))
    check("archive-crc32", expected.get("crc32") == crc32(archive_bytes) == "b2b3edbe", crc32(archive_bytes))
    check("delivery-id", delivery.get("id") == "ALIGNMENT-ASCENSION-DIRECTOR-RETURN335-DELIVERY" and delivery.get("reviewId") == "Return335", str(delivery.get("id")))

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
        check("archive-member-count", len(names) == delivery.get("archiveMemberCount") == 29, str(len(names)))
        declared = {row["path"]: row for row in delivery.get("members", [])}
        actual = {row["path"]: row for row in member_rows}
        exact = set(declared) == set(actual) == set(delivery.get("exactAllowlist", []))
        for name, row in declared.items():
            got = actual.get(name, {})
            exact = exact and all(got.get(k) == row.get(k) for k in ("bytes", "sha256", "crc32"))
        check("external-member-bindings-and-allowlist", exact and len(declared) == 29, f"Compared {len(declared)} members.")
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
    coverage = load(PAYLOAD / "CASE_COVERAGE.json")
    procedure = load(PAYLOAD / "PROCEDURE_STATUS.json")
    semantics = load(PAYLOAD / "SEMANTIC_RECONCILIATION.json")
    source_reconciliation = load(PAYLOAD / "SOURCE_RECONCILIATION.json")
    validation = load(PAYLOAD / "VALIDATION.json")
    qualifications = load(PAYLOAD / "QUALIFICATIONS.json")
    comparator = load(PAYLOAD / "COMPARATOR_SCOPE.json")
    manifest = load(PAYLOAD / "MEMBER_MANIFEST.json")

    check("decision-scope", decision.get("reviewedIds") == ["alignment-ascension"] and decision.get("groupId") == "rank9-alignment-faction-purification5", str(decision.get("reviewedIds")))
    check("held-not-accepted-or-applied", decision.get("heldIds") == ["alignment-ascension"] and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("decisions", [{}])[0].get("decision") == "HOLD", str(decision.get("heldIds")))
    check("application-not-authorized", decision.get("applicationAuthorization") == {"authorized": False, "authorizedIds": [], "canonicalMutationAuthorized": False} and decision.get("canonicalMutation") is False, "No application or canonical mutation authorization.")
    authority = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
    check("authority-preserved", decision.get("authorityBefore") == authority == decision.get("authorityAfter") == counts.get("authority"), json.dumps(decision.get("authorityAfter"), sort_keys=True))
    check("next-director-priority", decision.get("nextPendingIdentity") == "alignment-perfection" and decision.get("nextBlockerId") == "AFP211-B02" and decision.get("nextPendingGroup") == "rank9-alignment-faction-purification5", str(decision.get("nextPendingIdentity")))
    check("exact-three-contract-holds", [row.get("id") for row in hold.get("minimumContractSections", [])] == ["AFP335-W01", "AFP335-W02", "AFP335-W03"] and all(row.get("parentBlocker") == "AFP211-B01" for row in hold.get("minimumContractSections", [])), "Form, finite lifecycle, and useful insight remain unresolved.")
    check("integrated-witness-and-payment-missing", hold.get("minimumIntegratedWitness", {}).get("status") == "NOT_PRESENT" and hold.get("minimumIntegratedWitness", {}).get("completePaidPositiveEncounters") is None and counts.get("completePaidPositiveEncounters") == 0, "No complete paid positive encounters.")
    check("native-procedure-still-incomplete", procedure.get("status") == "SOURCE_BOUND_INCOMPLETE_NOT_OPERATIONAL" and procedure.get("operational") is None, str(procedure.get("status")))
    check("previous-cases-preserved-not-replayed", len(coverage.get("cases", [])) == 2 and all(row.get("currentReplay") == "NOT_RUN_BY_EXPLICIT_REQUEST" and row.get("currentCaseReaudit") == "NOT_RUN_BY_EXPLICIT_REQUEST" and row.get("completeSpellWitness") is False for row in coverage.get("cases", [])) and counts.get("freshCaseReplays") == 0 and counts.get("freshCaseReaudits") == 0, "Two conditional cases retained; no replay or re-audit.")
    check("source-checks-pass", validation.get("status") == "PASS_WITH_DISCLOSED_INPUT_PACKAGING_FINDING" and validation.get("checkCount") == 61 and validation.get("passed") == 61 and validation.get("failed") == 0 and counts.get("sourceDataChecksPassed") == 61 and counts.get("sourceDataChecksFailed") == 0, "61 passed, 0 failed.")
    check("comparator-boundary", comparator.get("closedEvidenceFinding", {}).get("id") == "AFP211-E01" and comparator.get("closedEvidenceFinding", {}).get("status") == "CLOSED" and comparator.get("scopeDoesNotAcceptComparatorsAgain") is True, "AFP211-E01 remains closed within comparator scope.")
    check("fixture-provenance", "not attributed to the user" in decision.get("fixtureProvenance", "") and "No gameplay observation" in decision.get("fixtureProvenance", ""), decision.get("fixtureProvenance", ""))
    check("qualifications-retained", len(qualifications.get("qualificationIds", [])) == 7 and qualifications.get("noCanonicalIndexCatalogQueueHandoffGitHubMutation") is True, "Seven qualifications retained.")
    check("no-prior-case-replay", decision.get("priorCaseReplay") == "NOT_RUN_BY_REQUEST" and counts.get("freshCaseReplays") == 0 and counts.get("freshForwardOperations") == 0 and counts.get("freshInverseOperations") == 0, "No replay or new event operations.")
    check("source-packet-binding", delivery.get("sourcePacket", {}).get("sha256") == "31d037b586604a222a913b6492f34d87205d7258c28b341c2ec7aaa5af14a9a6" and delivery.get("sourceDelivery", {}).get("sha256") == "5eff89158406c1dc3783304bb3b9d67cd6316e5f6f430255317377d1d9ace5d0", "Review335 inputs are bound.")
    check("manifest-payload-count", manifest.get("payloadMemberCount") == delivery.get("payloadMemberCount") == 28 and len(manifest.get("members", [])) == 28, json.dumps({"payload": manifest.get("payloadMemberCount"), "manifestRows": len(manifest.get("members", []))}))
    check("semantic-reconciliation-no-acceptance", semantics.get("acceptanceAuthorized") is not True and counts.get("semanticHeldFindings") == 3 and decision.get("acceptedIds") == [], "Three target findings remain held; no acceptance.")
    check("source-reconciliation-no-canonical-change", source_reconciliation.get("canonicalMutation") is not True and decision.get("canonicalMutation") is False, "No canonical changes.")
    check("delivery-exact-scope", delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("heldIds") == ["alignment-ascension"] and delivery.get("blockerIds") == ["AFP211-B01"], "Return scope matches the one-identity HOLD.")

    # Bind the exact current queue used for the next review before advancing authority.
    input_authority = load(PAYLOAD / "input/00_CURRENT_AUTHORITY_334.json")
    queue334 = load(QUEUE_IN)
    check("input-authority-823-25-0", input_authority.get("authority", {}) == authority and queue334.get("currentAuthority") == authority, "Review335 uses queue334 authority.")
    check("next-identity-not-already-held", "alignment-perfection" not in queue334.get("separatelyRetainedHolds", []) and "alignment-ascension" not in queue334.get("separatelyRetainedHolds", []), "Only Return335 adds Alignment Ascension to retained holds.")

    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return335 verification failed: " + json.dumps([row for row in checks if not row["passed"]], ensure_ascii=False))

    recorded = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    audit_path = A / "ALIGNMENT_ASCENSION_RETURN335_INDEPENDENT_AUDIT.json"
    receipt_path = A / "ALIGNMENT_ASCENSION_RETURN335_RECEIPT.json"
    next_id, next_blocker, next_group = "alignment-perfection", "AFP211-B02", "rank9-alignment-faction-purification5"

    audit = {
        "id": "ALIGNMENT-ASCENSION-RETURN335-INDEPENDENT-AUDIT",
        "recordedAtUtc": recorded,
        "status": "PASS_RETURN335_SEALED_HOLD_AFP211_B01",
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
        "heldIds": ["alignment-ascension"],
        "applicationAuthorizedIds": [],
        "authority": authority,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "openContractIds": ["AFP335-W01", "AFP335-W02", "AFP335-W03"],
        "closedEvidenceFinding": "AFP211-E01",
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(audit_path, audit)

    receipt = {
        "id": "ALIGNMENT-ASCENSION-RETURN335-RECEIPT",
        "recordedAtUtc": recorded,
        "decision": "HOLD",
        "blockerIds": ["AFP211-B01"],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "holdRegister": bind(PAYLOAD / "HOLD_REGISTER.json"),
        "independentAudit": bind(audit_path),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["alignment-ascension"],
        "applicationAuthorizedIds": [],
        "openContractIds": ["AFP335-W01", "AFP335-W02", "AFP335-W03"],
        "closedEvidenceFinding": "AFP211-E01",
        "authority": authority,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextGroup": next_group,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(receipt_path, receipt)

    queue_path = A / "CURRENT_SPELL_QUEUE_335.json"
    pending_path = A / "CURRENT25_PENDING_IDENTITY_AUDIT_335.json"
    handoff_path = A / "CURRENT_HANDOFF_335.json"
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_335.md"
    queue = load(QUEUE_IN)
    pending = load(PENDING_IN)
    handoff = load(HANDOFF_IN)
    held = set(queue.get("separatelyRetainedHolds", []))
    held.add("alignment-ascension")
    decision_ref, audit_ref, receipt_ref = bind(decision_path), bind(audit_path), bind(receipt_path)

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-335",
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
        "heldThisStep": ["alignment-ascension"],
        "separatelyRetainedHolds": sorted(held),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoff": handoff_path.relative_to(ROOT).as_posix(),
        "currentPacket": None,
        "currentPacketStatus": "RETURN335_ALIGNMENT_ASCENSION_HELD_ALIGNMENT_PERFECTION_AFP211_B02_NEXT",
        "activeReview": {"spellId": next_id, "blockerIds": [next_blocker], "packet": None, "status": "DIRECTOR_RETURN335_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["alignment-ascension"],
        "currentReturnBlockers": {**queue.get("currentReturnBlockers", {}), "alignment-ascension": ["AFP211-B01"]},
        "currentDirectorInstruction": "Return335 holds Alignment Ascension / AFP211-B01. Three spell-local contracts (form, lifecycle, useful insight) and two paid useful encounters remain. AFP211-E01 is closed within comparator scope. The Director-designated next priority is Alignment Perfection / AFP211-B02. Apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return335 independently verified. Alignment Ascension remains held; next is Alignment Perfection / AFP211-B02.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    save(queue_path, queue)

    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-335",
        "recordedAtUtc": recorded,
        "status": "PASS_CURRENT_823_25_RETURN335_ALIGNMENT_ASCENSION_HOLD_ALIGNMENT_PERFECTION_NEXT",
        "supersedes": PENDING_IN.name,
        "authority": authority,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": ["alignment-ascension"],
        "separatelyHeldIds": sorted(held),
        "nextGroup": next_group,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "nextStep": "Review Alignment Perfection / AFP211-B02 using current authority and sources. Preserve AFP211-B01's three contract holds and closed AFP211-E01 comparator boundary. Apply only an exact sealed acceptance.",
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
        "id": "CURRENT-HANDOFF-335",
        "recordedAtUtc": recorded,
        "supersedes": HANDOFF_IN.name,
        "status": "RETURN335_VERIFIED_ALIGNMENT_ASCENSION_HELD_ALIGNMENT_PERFECTION_NEXT_823_25_0",
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
        "heldThisStep": ["alignment-ascension"],
        "separatelyRetainedHolds": sorted(held),
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": next_id, "blockerId": next_blocker, "group": next_group},
        "nextPendingGroup": {"group": next_group, "pendingIds": [next_id], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Alignment Perfection / AFP211-B02. Preserve the Alignment Ascension hold and closed comparator finding AFP211-E01; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return335 sealed Alignment Ascension HOLD; the Director designates Alignment Perfection / AFP211-B02 as next.",
    })
    save(handoff_path, handoff)

    snapshot_path.write_text(
        "# Spell review status — queue 335\n\n"
        f"Return335 holds Alignment Ascension / AFP211-B01. Independent verification passed {len(checks)}/{len(checks)} checks. "
        "Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "The spell-local energy-body form, finite lifecycle, and bounded useful-insight contract remain undefined; two paid useful encounters are also absent. "
        "Two conditional component cases were retained without replay. AFP211-E01 remains closed within comparator scope; no comparator powers transfer to Ascension.\n\n"
        f"Next Director-prioritized identity: **Alignment Perfection / AFP211-B02**. No canonical files changed and no application was performed.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": sum(row["passed"] for row in checks), "failed": sum(not row["passed"] for row in checks), "held": "alignment-ascension", "pending": 25, "next": next_id, "archiveMembers": len(member_rows)}, indent=2))


if __name__ == "__main__":
    main()
