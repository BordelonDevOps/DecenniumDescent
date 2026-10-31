#!/usr/bin/env python3
"""Verify and record Director Return332 without changing canonical spell data."""

from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
RECEIVED = A / "rank9_summon_herald_of_the_planes_return332_received"
ARCHIVE = RECEIVED / "DD_SummonHeraldOfThePlanes_Director_Return332_HELD.zip"
DELIVERY = RECEIVED / "DD_SummonHeraldOfThePlanes_Director_Return332_HELD_DELIVERY.json"
PAYLOAD = RECEIVED / "payload"
QUEUE_IN = A / "CURRENT_SPELL_QUEUE_331.json"
PENDING_IN = A / "CURRENT25_PENDING_IDENTITY_AUDIT_331.json"
HANDOFF_IN = A / "CURRENT_HANDOFF_331.json"


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
    check("archive-size", expected["bytes"] == len(archive_bytes) == 122040, str(len(archive_bytes)))
    check("archive-sha256", expected["sha256"] == sha256(archive_bytes) == "7c07332459bac1ea3dbe4b86d59e9da9b46cd99ee0f00fef76b907be226ee920", sha256(archive_bytes))
    check("archive-crc32", expected["crc32"] == crc32(archive_bytes) == "0b951f28", crc32(archive_bytes))
    check("archive-name", expected["fileName"] == ARCHIVE.name, ARCHIVE.name)

    member_rows = []
    names_safe = True
    with ZipFile(ARCHIVE) as archive:
        bad = archive.testzip()
        names = archive.namelist()
        for name in names:
            part = PurePosixPath(name)
            if part.is_absolute() or ".." in part.parts or "\\" in name:
                names_safe = False
            data = archive.read(name)
            member_rows.append({"path": name, "bytes": len(data), "sha256": sha256(data), "crc32": crc32(data)})
        check("zip-crc", bad is None, str(bad))
        check("member-path-safety", names_safe, "No absolute or traversal paths.")
        check("archive-member-count", len(names) == delivery.get("archiveMemberCount") == 33, str(len(names)))
        declared = {row["path"]: row for row in delivery.get("members", [])}
        observed = {row["path"]: row for row in member_rows}
        exact = set(declared) == set(observed)
        for name, row in declared.items():
            actual = observed.get(name, {})
            exact = exact and all(actual.get(k) == row.get(k) for k in ("bytes", "sha256", "crc32"))
        check("delivery-member-bindings", exact and len(declared) == 33, f"Compared {len(declared)} members.")
        if not names_safe or bad:
            raise RuntimeError("Unsafe or corrupt archive; extraction refused.")
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
    replay = load(PAYLOAD / "REPLAY_RESULTS.json")
    minimum = load(PAYLOAD / "MINIMUM_MISSING_WITNESS.json")
    findings = load(PAYLOAD / "SOURCE_FINDINGS.json")
    check("decision-scope", decision.get("scopeIds") == ["summon-herald-of-the-planes"] and decision.get("blockerIds") == ["SH202-B02"], str(decision.get("scopeIds")))
    check("held-not-accepted", decision.get("decision") == "HOLD" and decision.get("heldIds") == ["summon-herald-of-the-planes"] and not decision.get("acceptedIds") and not decision.get("appliedIds"), decision.get("decision", ""))
    check("no-application-authorized", decision.get("applicationAuthorizedIds") == [] and decision.get("applicationPerformed") is False, "No authorization or application.")
    check("authority-preserved", decision.get("authorityAfter") == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}, json.dumps(decision.get("authorityAfter"), sort_keys=True))
    check("replay-counts", replay.get("totals") == {"cases": 2, "events": 18, "forwardOperations": 36, "inverseOperations": 36, "fullReverseTraversals": 2, "wholePositiveCases": 0}, json.dumps(replay.get("totals"), sort_keys=True))
    check("case-results-hold", counts.get("positiveCallCases") == 0 and counts.get("wholeCaseHolds") == 2 and counts.get("paidHeraldCasts") == 0, json.dumps({k: counts.get(k) for k in ("positiveCallCases", "wholeCaseHolds", "paidHeraldCasts")}))
    check("four-minimum-witness-parts", [row.get("id") for row in minimum.get("minimumWitnessParts", [])] == ["SH332-W01", "SH332-W02", "SH332-W03", "SH332-W04"], "W01–W04 are explicit.")
    check("next-identity", decision.get("nextIdentity") == "summon-avatar-of-decay" and decision.get("nextBlockerIds") == ["SH202-B03"], str(decision.get("nextIdentity")))
    check("avatar-follow-up-preserved", decision.get("avatarFindingsRemainOpen") == ["SH331-C01", "SH331-C02", "SH331-C03"], str(decision.get("avatarFindingsRemainOpen")))
    check("fixture-provenance", "not campaign events" in decision.get("fixtureProvenance", "") and "not attributed to the user" in decision.get("fixtureProvenance", ""), decision.get("fixtureProvenance", ""))
    check("no-canonical-change", decision.get("canonicalFilesEdited") is False and delivery.get("canonicalChanges") is False, "Canonical data untouched.")
    check("source-findings-hold", findings.get("closedWholeIdentityBlockers") == [] and sum(row.get("status") == "OPEN" for row in findings.get("findings", [])) >= 3, "Whole-identity blocker remains open.")
    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return332 verification failed: " + json.dumps([row for row in checks if not row["passed"]], ensure_ascii=False))

    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    recorded = datetime.now(timezone.utc).isoformat(timespec="seconds")
    audit_path = A / "SUMMON_HERALD_PLANES_RETURN332_INDEPENDENT_AUDIT.json"
    receipt_path = A / "SUMMON_HERALD_PLANES_RETURN332_RECEIPT.json"
    audit = {
        "id": "SUMMON-HERALD-RETURN332-INDEPENDENT-AUDIT",
        "recordedAtUtc": recorded,
        "status": "PASS_RETURN332_SEALED_HOLD_SH202_B02",
        "archive": bind(ARCHIVE),
        "delivery": bind(DELIVERY),
        "archiveMemberCount": len(member_rows),
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": sum(not row["passed"] for row in checks),
        "decision": "HOLD",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-herald-of-the-planes"],
        "authority": decision["authorityAfter"],
        "nextIdentity": decision["nextIdentity"],
        "nextBlockerIds": decision["nextBlockerIds"],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(audit_path, audit)
    receipt = {
        "id": "SUMMON-HERALD-RETURN332-RECEIPT",
        "recordedAtUtc": recorded,
        "decision": "HOLD",
        "blockerIds": ["SH202-B02"],
        "archive": bind(ARCHIVE),
        "delivery": bind(DELIVERY),
        "directorDecision": bind(decision_path),
        "replayResults": bind(PAYLOAD / "REPLAY_RESULTS.json"),
        "minimumWitness": bind(PAYLOAD / "MINIMUM_MISSING_WITNESS.json"),
        "independentAudit": bind(audit_path),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-herald-of-the-planes"],
        "applicationAuthorizedIds": [],
        "authority": decision["authorityAfter"],
        "nextIdentity": decision["nextIdentity"],
        "nextBlockerIds": decision["nextBlockerIds"],
        "minimumWitnessIds": decision["minimumWitnessIds"],
        "avatarFindingsRemainOpen": decision["avatarFindingsRemainOpen"],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(receipt_path, receipt)

    queue = load(QUEUE_IN)
    pending = load(PENDING_IN)
    handoff = load(HANDOFF_IN)
    queue_path = A / "CURRENT_SPELL_QUEUE_332.json"
    pending_path = A / "CURRENT25_PENDING_IDENTITY_AUDIT_332.json"
    handoff_path = A / "CURRENT_HANDOFF_332.json"
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_332.md"
    authority = decision["authorityAfter"]
    next_id, next_blocker = "summon-avatar-of-decay", "SH202-B03"
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    audit_ref, receipt_ref = bind(audit_path), bind(receipt_path)
    decision_ref = bind(decision_path)

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-332",
        "recordedAtUtc": recorded,
        "supersedesQueue": bind(QUEUE_IN),
        "currentAuthority": authority,
        "pendingCount": 25,
        "acceptedUnapplied": 0,
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "nextGroup": "rank9-summon-hosts5",
        "next": next_id,
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "heldThisStep": ["summon-herald-of-the-planes"],
        "separatelyRetainedHolds": sorted(set(queue.get("separatelyRetainedHolds", [])) | {"summon-elemental-avatar", "summon-herald-of-the-planes"}),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoff": handoff_path.relative_to(ROOT).as_posix(),
        "currentPacket": None,
        "currentPacketStatus": "RETURN332_HERALD_HELD_AVATAR_OF_DECAY_SH202_B03_NEXT",
        "activeReview": {"spellId": next_id, "blockerIds": [next_blocker], "packet": None, "status": "DIRECTOR_RETURN332_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["summon-herald-of-the-planes"],
        "currentReturnBlockers": {"summon-elemental-avatar": ["SH202-B01"], "summon-herald-of-the-planes": ["SH202-B02"]},
        "currentDirectorInstruction": "Return332 holds Summon Herald of the Planes / SH202-B02 with minimum witnesses SH332-W01–W04; the Director-designated next priority is Summon Avatar of Decay / SH202-B03. Keep Avatar findings SH331-C01–C03 open. Apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return332 independently verified. Herald remains held; next is Summon Avatar of Decay / SH202-B03. Avatar corrections remain a separate open follow-up.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    save(queue_path, queue)

    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-332",
        "recordedAtUtc": recorded,
        "status": "PASS_CURRENT_823_25_RETURN332_HERALD_HOLD_AVATAR_DECAY_NEXT",
        "supersedes": PENDING_IN.name,
        "authority": authority,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": ["summon-herald-of-the-planes"],
        "separatelyHeldIds": sorted(set(pending.get("separatelyHeldIds", [])) | {"summon-elemental-avatar", "summon-herald-of-the-planes"}),
        "nextGroup": "rank9-summon-hosts5",
        "nextIdentity": next_id,
        "nextBlockerIds": [next_blocker],
        "nextPendingIds": [next_id],
        "nextPendingCount": 1,
        "nextStep": "Review Summon Avatar of Decay / SH202-B03 using its current source and prior Return285 evidence. Preserve Herald witness requirements SH332-W01–W04 and Avatar corrections SH331-C01–C03 as open follow-ups. Apply only an exact sealed acceptance.",
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
        "id": "CURRENT-HANDOFF-332",
        "recordedAtUtc": recorded,
        "supersedes": HANDOFF_IN.name,
        "status": "RETURN332_VERIFIED_HERALD_HELD_AVATAR_DECAY_NEXT_823_25_0",
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
        "heldThisStep": ["summon-herald-of-the-planes"],
        "separatelyRetainedHolds": sorted(set(handoff.get("separatelyRetainedHolds", [])) | {"summon-elemental-avatar", "summon-herald-of-the-planes"}),
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": next_id, "blockerId": next_blocker, "group": "rank9-summon-hosts5"},
        "nextPendingGroup": {"group": "rank9-summon-hosts5", "pendingIds": [next_id], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Summon Avatar of Decay / SH202-B03. Preserve Herald witnesses SH332-W01–W04 and Avatar corrections SH331-C01–C03 as separate open items; apply only an exact sealed acceptance.",
        "directorConnectionStatus": "Return332 sealed Herald HOLD; the Director designates Summon Avatar of Decay / SH202-B03 as next.",
    })
    save(handoff_path, handoff)

    snapshot_path.write_text(
        "# Spell review status — queue 332\n\n"
        "Return332 holds Summon Herald of the Planes / SH202-B02. Independent verification passed "
        f"{len(checks)}/{len(checks)} checks. Authority remains **823 applied, 25 pending, 0 accepted-unapplied** "
        "(547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "Both preserved cases replay with 18 events, 36 forward and 36 inverse operations, but remain source-held: "
        "no paid call, arrival, useful aid or return. Four witness parts SH332-W01–W04 remain open. Avatar findings "
        "SH331-C01–C03 also remain open.\n\n"
        f"Next Director-prioritized identity: **Summon Avatar of Decay / SH202-B03**. No canonical files changed and no application was performed.\n",
        encoding="utf-8",
    )
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": sum(row["passed"] for row in checks), "failed": sum(not row["passed"] for row in checks), "held": "summon-herald-of-the-planes", "pending": 25, "next": next_id, "payloadFiles": len(member_rows)}, indent=2))


if __name__ == "__main__":
    main()
