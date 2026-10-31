#!/usr/bin/env python3
"""Independently verify and record Director Return334; do not edit canonical spell data."""

from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
RECEIVED = A / "rank9_impactexile4_return334_received"
ARCHIVE = RECEIVED / "DD_ReverseGravityField_Director_Return334_HELD.zip"
DELIVERY = RECEIVED / "DD_ReverseGravityField_Director_Return334_HELD_DELIVERY.json"
PAYLOAD = RECEIVED / "payload"
QUEUE_IN = A / "CURRENT_SPELL_QUEUE_333.json"
PENDING_IN = A / "CURRENT25_PENDING_IDENTITY_AUDIT_333.json"
HANDOFF_IN = A / "CURRENT_HANDOFF_333.json"


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

    expected = delivery["archive"]
    check("archive-name", expected.get("fileName") == ARCHIVE.name, ARCHIVE.name)
    check("archive-size", expected.get("bytes") == len(archive_bytes) == 112395, str(len(archive_bytes)))
    check("archive-sha256", expected.get("sha256") == sha256(archive_bytes) == "e06d3543af14b1efe610049c1993fd811440a2de9743880d68964f40c9af84a2", sha256(archive_bytes))
    check("archive-crc32", expected.get("crc32") == crc32(archive_bytes) == "8f54f596", crc32(archive_bytes))

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
        if not safe or bad:
            raise RuntimeError("Unsafe or corrupt archive; extraction refused.")
        if PAYLOAD.exists() and any(PAYLOAD.iterdir()):
            for name in names:
                path = PAYLOAD.joinpath(*PurePosixPath(name).parts)
                if not path.is_file() or path.read_bytes() != archive.read(name):
                    raise RuntimeError(f"Existing extraction mismatch: {name}")
        else:
            PAYLOAD.mkdir(parents=True, exist_ok=True)
            archive.extractall(PAYLOAD)

    decision = load(PAYLOAD / "DIRECTOR_DECISION.json")
    counts = load(PAYLOAD / "COUNTS.json")
    witnesses = load(PAYLOAD / "WITNESS_REASSESSMENT.json")
    semantics = load(PAYLOAD / "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
    source_checks = load(PAYLOAD / "SOURCE_DATA_CHECKS.json")
    input_finding = load(PAYLOAD / "INPUT_PACKAGE_FINDINGS.json")
    input_bindings = load(PAYLOAD / "INPUT_BINDINGS.json")
    manifest = load(PAYLOAD / "MEMBER_MANIFEST.json")

    check("decision-scope", decision.get("scopeIds") == ["reverse-gravity-field"] and decision.get("blockerIds") == ["IE204-B02"], str(decision.get("scopeIds")))
    check("held-not-accepted-or-applied", decision.get("decision") == "HOLD" and decision.get("heldIds") == ["reverse-gravity-field"] and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [], decision.get("decision", ""))
    check("application-not-authorized", decision.get("applicationAuthorizedIds") == [] and decision.get("applicationPerformed") is False, "No application authorization.")
    authority = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
    check("authority-preserved", decision.get("authorityBefore") == authority == decision.get("authorityAfter"), json.dumps(decision.get("authorityAfter"), sort_keys=True))
    check("exact-two-held-witnesses", [row.get("id") for row in witnesses.get("witnesses", [])] == ["IE286-W1", "IE286-W2"] and all(row.get("decision") == "HELD" for row in witnesses.get("witnesses", [])), "W1 crate impact; W2 tether and anchor.")
    check("source-checks-all-pass", source_checks.get("status") == "PASS_EXTERNAL_BINDINGS_WITH_DISCLOSED_INTERNAL_MANIFEST_FINDING" and source_checks.get("checkCount") == 48 and len(source_checks.get("checks", [])) == 48 and all(row.get("passed") is True for row in source_checks.get("checks", [])), f"{sum(row.get('passed') is True for row in source_checks.get('checks', []))}/48.")
    check("input-manifest-finding-disclosed", input_finding.get("semanticBlocker") is False and input_finding.get("internalManifestStatus") == "STALE_SELF_ROW_AND_OMITTED_REQUEST" and input_finding.get("internallyUnlistedMember") == "REQUEST_334.md" and input_finding.get("externalManifestCoversActualRequestAndActualManifest") is True, json.dumps(input_finding, ensure_ascii=False)[:1000])
    check("no-case-replay-or-new-operations", counts.get("priorCasesReplayed") == 0 and counts.get("priorCasesReaudited") == 0 and counts.get("freshForwardOperations") == 0 and counts.get("freshInverseOperations") == 0 and counts.get("newEncounterTraces") == 0, json.dumps({k: counts.get(k) for k in ("priorCasesReplayed", "priorCasesReaudited", "freshForwardOperations", "freshInverseOperations", "newEncounterTraces")}))
    check("preserved-fall-and-overlap-results", semantics.get("findings", [])[4].get("status") == "PASS" and semantics.get("findings", [])[4].get("witnessId") is None, json.dumps(semantics.get("findings", [])[4], ensure_ascii=False))
    check("next-director-priority", decision.get("nextIdentity") == "alignment-ascension" and decision.get("nextBlockerIds") == ["AFP211-B01"] and decision.get("nextGroup") == "rank9-alignment-faction-purification5", str(decision.get("nextIdentity")))
    check("fixture-provenance", "not campaign events" in decision.get("fixtureProvenance", "") and "not attributed to the user" in decision.get("fixtureProvenance", ""), decision.get("fixtureProvenance", ""))
    check("output-manifest-complete", manifest.get("payloadMemberCount") == delivery.get("payloadMemberCount") == 27 and len(manifest.get("members", [])) == 27, json.dumps({"payload": manifest.get("payloadMemberCount"), "manifestRows": len(manifest.get("members", []))}))
    check("no-canonical-change", decision.get("canonicalFilesEdited") is False and decision.get("applicationPerformed") is False and decision.get("githubChanges") is False and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and delivery.get("applicationAuthorizedIds") == [], "No canonical edit or application.")

    expected_queue = input_bindings.get("currentQueueBinding", {})
    # Bind the current queue directly; the sealed return preserves its exact external binding.
    current_queue = bind(QUEUE_IN)
    queue_match = all(expected_queue.get(k) == current_queue.get(k) for k in ("path", "bytes", "sha256", "crc32"))
    check("queue333-current-binding", queue_match, json.dumps(current_queue, sort_keys=True))
    bound_authority = load(PAYLOAD / "input/00_CURRENT_AUTHORITY_333.json").get("authority", {})
    check("current-count-binding", bound_authority.get("reviewedApplied") == 823 and bound_authority.get("pending") == 25 and bound_authority.get("acceptedUnapplied") == 0, json.dumps(bound_authority, sort_keys=True))
    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return334 verification failed: " + json.dumps([row for row in checks if not row["passed"]], ensure_ascii=False))

    recorded = datetime.now(timezone.utc).isoformat(timespec="seconds")
    authority_after = decision["authorityAfter"]
    next_id, next_blocker, next_group = "alignment-ascension", "AFP211-B01", "rank9-alignment-faction-purification5"
    queue_path = A / "CURRENT_SPELL_QUEUE_334.json"
    pending_path = A / "CURRENT25_PENDING_IDENTITY_AUDIT_334.json"
    handoff_path = A / "CURRENT_HANDOFF_334.json"
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_334.md"
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    audit_path = A / "REVERSE_GRAVITY_FIELD_RETURN334_INDEPENDENT_AUDIT.json"
    receipt_path = A / "REVERSE_GRAVITY_FIELD_RETURN334_RECEIPT.json"

    audit = {
        "id": "REVERSE-GRAVITY-FIELD-RETURN334-INDEPENDENT-AUDIT",
        "recordedAtUtc": recorded,
        "status": "PASS_RETURN334_SEALED_HOLD_IE204_B02",
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
        "heldIds": ["reverse-gravity-field"],
        "applicationAuthorizedIds": [],
        "authority": authority_after,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "inputManifestFinding": input_finding,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(audit_path, audit)

    receipt = {
        "id": "REVERSE-GRAVITY-FIELD-RETURN334-RECEIPT",
        "recordedAtUtc": recorded,
        "decision": "HOLD",
        "blockerIds": ["IE204-B02"],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "witnessReassessment": bind(PAYLOAD / "WITNESS_REASSESSMENT.json"),
        "independentSemanticCheck": bind(PAYLOAD / "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"),
        "independentAudit": bind(audit_path),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["reverse-gravity-field"],
        "applicationAuthorizedIds": [],
        "missingWitnessIds": ["IE286-W1", "IE286-W2"],
        "authority": authority_after,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextGroup": next_group,
        "inputManifestFinding": input_finding,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(receipt_path, receipt)

    queue = load(QUEUE_IN)
    pending = load(PENDING_IN)
    handoff = load(HANDOFF_IN)
    held = set(queue.get("separatelyRetainedHolds", []))
    held.update({"summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field"})
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    audit_ref, receipt_ref, decision_ref = bind(audit_path), bind(receipt_path), bind(decision_path)

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-334",
        "recordedAtUtc": recorded,
        "supersedesQueue": bind(QUEUE_IN),
        "currentAuthority": authority_after,
        "pendingCount": 25,
        "acceptedUnapplied": 0,
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "nextGroup": next_group,
        "next": next_id,
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "heldThisStep": ["reverse-gravity-field"],
        "separatelyRetainedHolds": sorted(held),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoff": handoff_path.relative_to(ROOT).as_posix(),
        "currentPacket": None,
        "currentPacketStatus": "RETURN334_REVERSE_GRAVITY_HELD_ALIGNMENT_ASCENSION_AFP211_B01_NEXT",
        "activeReview": {"spellId": next_id, "blockerIds": [next_blocker], "packet": None, "status": "DIRECTOR_RETURN334_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["reverse-gravity-field"],
        "currentReturnBlockers": {**queue.get("currentReturnBlockers", {}), "reverse-gravity-field": ["IE204-B02"]},
        "currentDirectorInstruction": "Return334 holds Reverse Gravity Field / IE204-B02 with source-bound remaining witnesses IE286-W1 and IE286-W2. The Director-designated next priority is Alignment Ascension / AFP211-B01. Do not replay the six preserved cases; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return334 independently verified. Reverse Gravity Field remains held; next is Alignment Ascension / AFP211-B01.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    save(queue_path, queue)

    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-334",
        "recordedAtUtc": recorded,
        "status": "PASS_CURRENT_823_25_RETURN334_REVERSE_GRAVITY_HOLD_ALIGNMENT_ASCENSION_NEXT",
        "supersedes": PENDING_IN.name,
        "authority": authority_after,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": ["reverse-gravity-field"],
        "separatelyHeldIds": sorted(held),
        "nextGroup": next_group,
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "nextStep": "Review Alignment Ascension / AFP211-B01 using the current authority and source. Preserve IE204-W1/W2, SH331-C01–C03, SH332-W01–W04, and SH333-R01–R04 as open holds. Apply only an exact sealed acceptance.",
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
        "id": "CURRENT-HANDOFF-334",
        "recordedAtUtc": recorded,
        "supersedes": HANDOFF_IN.name,
        "status": "RETURN334_VERIFIED_REVERSE_GRAVITY_HELD_ALIGNMENT_ASCENSION_NEXT_823_25_0",
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
        "heldThisStep": ["reverse-gravity-field"],
        "separatelyRetainedHolds": sorted(held),
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": next_id, "blockerId": next_blocker, "group": next_group},
        "nextPendingGroup": {"group": next_group, "pendingIds": [next_id], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Alignment Ascension / AFP211-B01. Preserve IE286-W1/W2, SH331-C01–C03, SH332-W01–W04, and SH333-R01–R04 as separate open items; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return334 sealed Reverse Gravity Field HOLD; the Director designates Alignment Ascension / AFP211-B01 as next.",
    })
    save(handoff_path, handoff)

    snapshot_path.write_text(
        "# Spell review status — queue 334\n\n"
        "Return334 holds Reverse Gravity Field / IE204-B02. Independent verification passed "
        f"{len(checks)}/{len(checks)} checks. Authority remains **823 applied, 25 pending, 0 accepted-unapplied** "
        "(547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "The two remaining witnesses are the actual crate impact/durability/custody record (IE286-W1) and a lawful, "
        "rated tether/anchor with a rule for the upward load (IE286-W2). Conjure Rope's 300 lb static capacity is preserved "
        "without inferring dynamic restraint or anchor strength. Six previous cases were not replayed; creature, overlap, "
        "Feather Fall and other verified results remain unchanged.\n\n"
        f"Next Director-prioritized identity: **Alignment Ascension / AFP211-B01**. No canonical files changed and no application was performed.\n",
        encoding="utf-8",
    )
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": sum(row["passed"] for row in checks), "failed": sum(not row["passed"] for row in checks), "held": "reverse-gravity-field", "pending": 25, "next": next_id, "archiveMembers": len(member_rows)}, indent=2))


if __name__ == "__main__":
    main()
