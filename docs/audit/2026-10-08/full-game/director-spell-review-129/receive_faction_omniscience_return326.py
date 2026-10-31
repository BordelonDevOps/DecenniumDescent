from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import shutil
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
DOWNLOADS = pathlib.Path(r"C:\Users\cbord\Downloads")
OUT = AUDIT / "fos326_received"
ZIP_NAME = "DD_Rank9_FactionOmniscienceSupreme_Director_Return326_HELD.zip"
DELIVERY_NAME = "DD_Rank9_FactionOmniscienceSupreme_Director_Return326_HELD_DELIVERY.json"
AUTH = {
    "reviewedApplied": 823,
    "pending": 25,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 547,
    "scopedInterfaces": 173,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def readj(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def bind(path: pathlib.Path):
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(raw),
        "sha256": sha(raw),
        "crc32": crc(raw),
    }


def safe_member(name: str) -> None:
    path = pathlib.PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"unsafe ZIP member: {name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in (ZIP_NAME, DELIVERY_NAME):
        source, target = DOWNLOADS / name, OUT / name
        if not source.is_file():
            raise FileNotFoundError(source)
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise RuntimeError(f"existing received file differs from Downloads: {target}")
        if not target.exists():
            shutil.copyfile(source, target)

    archive_path, delivery_path = OUT / ZIP_NAME, OUT / DELIVERY_NAME
    delivery = readj(delivery_path)
    archive_raw = archive_path.read_bytes()
    checks: list[dict] = []

    def ck(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    ck(
        "outer archive matches sealed byte count, SHA-256 and CRC32",
        len(archive_raw) == delivery["archive"]["bytes"]
        and sha(archive_raw) == delivery["archive"]["sha256"]
        and crc(archive_raw) == delivery["archive"]["crc32"],
        delivery["archive"],
    )
    expected_quals = [f"KR198-H0{i}" for i in range(1, 7)]
    ck(
        "sealed decision is FOS-only HOLD at KR198-B01 with no acceptance or application",
        delivery["status"] == "SEALED_HELD"
        and delivery["acceptedIds"] == []
        and delivery["appliedIds"] == []
        and delivery["heldIds"] == ["faction-omniscience-supreme"]
        and delivery["blockerIds"] == ["KR198-B01"]
        and delivery["qualificationIds"] == expected_quals
        and delivery["unresolvedSourceConflictIds"] == ["KR326-C01"]
        and delivery["canonicalEdits"] is False
        and delivery["applicationPerformed"] is False
        and delivery["allDownstreamGatesClosed"] is True,
        {k: delivery.get(k) for k in ("heldIds", "blockerIds", "qualificationIds", "unresolvedSourceConflictIds")},
    )
    ck(
        "authority and closure totals remain unchanged; Banishment Gate precedes Fortress",
        delivery["authority"] == AUTH
        and delivery["remainingClosureTasks"] == 25
        and delivery["firstReviewTasks"] == 0
        and delivery["nextIdentity"] == "banishment-gate"
        and delivery["nextGroup"] == "rank9-planar-gates5"
        and delivery["thenIdentity"] == "conjure-demiplane-fortress",
        {k: delivery.get(k) for k in ("authority", "remainingClosureTasks", "nextIdentity", "nextGroup", "thenIdentity")},
    )

    with zipfile.ZipFile(archive_path) as z:
        names = [item.filename for item in z.infolist()]
        for name in names:
            safe_member(name)
        ck(
            "ZIP CRC, unique member list, exact allowlist and declared member count",
            z.testzip() is None
            and len(names) == len(set(names)) == delivery["memberCount"] == 61
            and set(names) == set(delivery["exactAllowlist"]),
            {"memberCount": len(names)},
        )
        sealed_members = {row["path"]: row for row in delivery["members"]}
        ck(
            "delivery seals each archive member byte count, SHA-256 and CRC32",
            set(sealed_members) == set(names)
            and all(
                len(z.read(name)) == sealed_members[name]["bytes"]
                and sha(z.read(name)) == sealed_members[name]["sha256"]
                and crc(z.read(name)) == sealed_members[name]["crc32"]
                for name in names
            ),
            {"sealedMembers": len(sealed_members)},
        )
        payload = {name: z.read(name) for name in names}
        manifest = json.loads(payload["MANIFEST.json"])
        manifest_members = {row["path"]: row for row in manifest["members"]}
        ck(
            "internal manifest seals every non-manifest payload member",
            manifest["payloadEntryCount"] == 60
            and set(manifest_members) == set(names) - {"MANIFEST.json"}
            and all(
                len(payload[name]) == manifest_members[name]["bytes"]
                and sha(payload[name]) == manifest_members[name]["sha256"]
                and crc(payload[name]) == manifest_members[name]["crc32"]
                for name in manifest_members
            ),
            {"payloadCount": len(manifest_members)},
        )

        decision = json.loads(payload["DIRECTOR_DECISION.json"])
        validation = json.loads(payload["DATA_VALIDATION.json"])
        package_checks = json.loads(payload["PACKAGE_CHECKS.json"])
        results = json.loads(payload["CASE_RESULTS.json"])
        blocker = json.loads(payload["BLOCKER_REASSESSMENT.json"])
        qualifications = json.loads(payload["QUALIFICATIONS.json"])
        conflicts = json.loads(payload["UNRESOLVED_SOURCE_CONFLICTS.json"])
        evidence = json.loads(payload["SEASONAL_EVIDENCE_DISPOSITION.json"])
        semantic = json.loads(payload["INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"])
        remaining = json.loads(payload["REMAINING_QUEUE.json"])

        ck(
            "inner decision preserves FOS-only hold and 823/25/0 authority",
            decision["status"] == "HOLD"
            and decision["scopeIds"] == ["faction-omniscience-supreme"]
            and decision["acceptedIds"] == []
            and decision["appliedIds"] == []
            and decision["heldIds"] == ["faction-omniscience-supreme"]
            and decision["authorityBefore"] == decision["authorityAfter"] == AUTH
            and decision["nextIdentity"] == "banishment-gate"
            and decision["thenIdentity"] == "conjure-demiplane-fortress"
            and decision["applicationPerformed"] is False
            and decision["canonicalEdits"] is False,
            {"scope": decision["scopeIds"], "next": decision["nextIdentity"]},
        )
        counts = delivery["counts"]
        ck(
            "all 1,523 data checks pass",
            validation["status"] == "PASS"
            and validation["checkCount"] == validation["passedChecks"] == delivery["dataCheckCount"] == 1523
            and validation["failedChecks"] == 0,
            {k: validation[k] for k in ("checkCount", "passedChecks", "failedChecks")},
        )
        ck(
            "all 15 package checks pass",
            package_checks["status"] == "PASS"
            and package_checks["checkCount"] == delivery["packageConsistencyCheckCount"] == 15
            and all(row["passed"] for row in package_checks["checks"]),
            {"checkCount": package_checks["checkCount"]},
        )
        ck("124 seal readback checks are recorded", delivery["sealReadbackCheckCount"] == 124, delivery["sealReadbackCheckCount"])
        ck(
            "eight cases replay 140 events and 280 reversible operations",
            counts["targetCases"] == 8
            and counts["targetEvents"] == 140
            and counts["forwardOperations"] == counts["inverseOperations"] == 280
            and counts["fullReverseTraversals"] == 8
            and len(results["results"]) == 8
            and all(row.get("replay") == "PASS" for row in results["results"]),
            {k: counts[k] for k in ("targetCases", "targetEvents", "forwardOperations", "inverseOperations", "fullReverseTraversals")},
        )
        ck(
            "current 140-source comparison and one changed index row match submitted packet",
            counts["sourceComparisonRows"] == 140
            and counts["unchangedSourceRows"] == 139
            and counts["changedSourceRows"] == 1
            and decision["sourcePacket"]["sha256"] == delivery["sourcePacket"]["sha256"],
            {k: counts[k] for k in ("sourceComparisonRows", "unchangedSourceRows", "changedSourceRows")},
        )
        ck(
            "KR198-B01 remains open with no positive witness part closed",
            blocker["id"] == "KR198-B01"
            and blocker["status"] == "OPEN"
            and all(row["status"] == "OPEN" for row in blocker["witnessParts"])
            and evidence["sourceAuthorizedForCanonicalSpellDossier"] is False
            and evidence["newFactsPromotedToCanon"] == []
            and evidence["closedWitnessParts"] == [],
            {"witnessParts": [row["id"] for row in blocker["witnessParts"]]},
        )
        ck(
            "six KR198-H qualifications and KR326-C01 conflict are preserved unresolved",
            qualifications["qualificationIds"] == expected_quals
            and conflicts["conflictCount"] == 1
            and conflicts["conflicts"][0]["id"] == "KR326-C01"
            and conflicts["conflicts"][0]["status"] == "UNRESOLVED_SOURCE_CONFLICT"
            and semantic["unresolvedSourceConflictIds"] == ["KR326-C01"],
            {"qualifications": qualifications["qualificationIds"], "conflict": conflicts["conflicts"][0]["id"]},
        )
        ck(
            "pending list and unchanged priority name Banishment Gate then Fortress",
            remaining["closureTasks"] == 25
            and remaining["firstReviewTasks"] == 0
            and len(remaining["all25PendingIds"]) == 25
            and remaining["nextAfterThisHold"] == "banishment-gate"
            and remaining["nextGroup"] == "rank9-planar-gates5"
            and remaining["thenIdentity"] == "conjure-demiplane-fortress"
            and remaining["canonicalQueueEdited"] is False,
            {"next": remaining["nextAfterThisHold"], "then": remaining["thenIdentity"]},
        )

        for name, raw in payload.items():
            target = OUT.joinpath(*pathlib.PurePosixPath(name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != raw:
                raise RuntimeError(f"extracted member differs: {target}")
            if not target.exists():
                target.write_bytes(raw)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    audit_binding_path = AUDIT / "FACTION_OMNISCIENCE_SUPREME_RETURN326_INDEPENDENT_AUDIT.json"
    receipt_path = AUDIT / "FACTION_OMNISCIENCE_SUPREME_RETURN326_RECEIPT.json"
    receipt = {
        "id": "FACTION-OMNISCIENCE-SUPREME-RETURN326-RECEIPT",
        "recordedAtUtc": now,
        "status": "SEALED_HELD_INDEPENDENTLY_VERIFIED",
        "archive": bind(archive_path),
        "delivery": bind(delivery_path),
        "decision": readj(OUT / "DIRECTOR_DECISION.json"),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["faction-omniscience-supreme"],
        "blockerIds": ["KR198-B01"],
        "qualificationIds": expected_quals,
        "unresolvedSourceConflictIds": ["KR326-C01"],
        "authority": AUTH,
        "remainingClosureTasks": 25,
        "firstReviewTasks": 0,
        "nextIdentity": "banishment-gate",
        "nextGroup": "rank9-planar-gates5",
        "thenIdentity": "conjure-demiplane-fortress",
        "checks": checks,
        "checkCount": len(checks),
        "passedChecks": sum(row["passed"] for row in checks),
        "failedChecks": sum(not row["passed"] for row in checks),
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    }
    receipt_path.write_bytes(pretty(receipt))
    audit = {
        "id": "FACTION-OMNISCIENCE-SUPREME-RETURN326-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS",
        "archive": bind(archive_path),
        "delivery": bind(delivery_path),
        "memberCount": 61,
        "checkCount": len(checks),
        "passedChecks": sum(row["passed"] for row in checks),
        "failedChecks": sum(not row["passed"] for row in checks),
        "checks": checks,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["faction-omniscience-supreme"],
        "blockerIds": ["KR198-B01"],
        "unresolvedSourceConflictIds": ["KR326-C01"],
        "nextIdentity": "banishment-gate",
        "nextGroup": "rank9-planar-gates5",
        "thenIdentity": "conjure-demiplane-fortress",
        "authority": AUTH,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    }
    audit_binding_path.write_bytes(pretty(audit))

    q0 = readj(AUDIT / "CURRENT_SPELL_QUEUE_326.json")
    p0 = readj(AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_326.json")
    h0 = readj(AUDIT / "CURRENT_HANDOFF_326.json")
    q = copy.deepcopy(q0)
    q.update(
        {
            "id": "SPELL-REVIEW-QUEUE-327",
            "recordedAtUtc": now,
            "supersedesQueue": "SPELL-REVIEW-QUEUE-326",
            "nextGroup": "rank9-planar-gates5",
            "nextPendingIds": ["banishment-gate"],
            "nextPendingCount": 1,
            "activeReview": {
                "spellId": "banishment-gate",
                "blockerIds": ["PG200-B03", "PG200-B04"],
                "packet": None,
                "status": "DIRECTOR_AUTHORIZED_NEXT_AFTER_FOS_HOLD",
            },
            "next": "banishment-gate",
            "lastDirectorReturn": "RETURN326_HELD_VERIFIED",
            "currentReturnAcceptedIds": [],
            "currentReturnAppliedIds": [],
            "currentReturnHeldIds": ["faction-omniscience-supreme"],
            "currentReturnBlockers": {"faction-omniscience-supreme": ["KR198-B01"]},
            "currentReturnDecision": bind(OUT / "DIRECTOR_DECISION.json"),
            "currentReturnArchive": bind(archive_path),
            "currentReturnDelivery": bind(delivery_path),
            "currentReturnAudit": bind(audit_binding_path),
            "currentReturnReceipt": bind(receipt_path),
            "currentReturn": bind(receipt_path),
            "currentPacketStatus": "RETURN326_HELD_VERIFIED_PROCEED_BANISHMENT_GATE_PG200_B03_B04",
            "pendingIdentityAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT25_PENDING_IDENTITY_AUDIT_327.json",
            "directorConnectionStatus": "Return326 verified: FOS remains held at KR198-B01; seasonal candidate records remain unadjudicated and KR326-C01 remains unresolved. Director explicitly directs Banishment Gate/PG200-B03 and PG200-B04 next, then Conjure Demiplane Fortress. No acceptance/application.",
            "githubChanges": False,
            "canonicalFilesChanged": False,
            "applicationPerformed": False,
            "acceptedThisStep": [],
            "appliedThisStep": [],
            "currentDirectorInstruction": "Review Banishment Gate / PG200-B03 and PG200-B04 only, as directed by Return326. Preserve the previous Planar Gates5 decision and all unrelated holds. Require source-qualified positive actor and lifecycle evidence; no acceptance or application unless supported by a sealed decision.",
        }
    )
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_327.json"
    queue_path.write_bytes(pretty(q))

    pending = copy.deepcopy(p0)
    pending.update(
        {
            "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-327",
            "recordedAtUtc": now,
            "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_326.json",
            "status": "PASS_CURRENT_823_25_RETURN326_FOS_HOLD_BANISHMENT_GATE_NEXT",
            "acceptedIds": [],
            "appliedIds": [],
            "nextGroup": "rank9-planar-gates5",
            "nextPendingIds": ["banishment-gate"],
            "nextPendingCount": 1,
            "nextStep": "Prepare and submit a Banishment Gate / PG200-B03 and PG200-B04-only packet with exact current authority, the prior sealed Planar Gates5 decision and current source-qualified evidence. Preserve FOS/KR198-B01, EProp/TF192-B02, Collapse Timeline/TF192-B05 and Fate Rewrite/TF192-B04.",
            "sourceQueue": queue_path.relative_to(ROOT).as_posix(),
            "currentQueueBinding": bind(queue_path),
            "heldThisStep": ["faction-omniscience-supreme"],
            "currentReturn": bind(receipt_path),
            "nextIdentity": "banishment-gate",
            "nextBlockerIds": ["PG200-B03", "PG200-B04"],
            "nextPendingCount": 1,
            "canonicalFilesChanged": False,
        }
    )
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_327.json"
    pending_path.write_bytes(pretty(pending))

    handoff = copy.deepcopy(h0)
    handoff.update(
        {
            "id": "SPELL-REVIEW-HANDOFF-327",
            "recordedAtUtc": now,
            "supersedes": "CURRENT-HANDOFF-326",
            "status": "RETURN326_VERIFIED_BANISHMENT_GATE_NEXT",
            "authority": AUTH,
            "scopeIds": ["banishment-gate"],
            "blockerIds": ["PG200-B03", "PG200-B04", "KR198-B01", "TF192-B02", "TF192-B04", "TF192-B05"],
            "queue": queue_path.relative_to(ROOT).as_posix(),
            "queueBinding": bind(queue_path),
            "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
            "appliedThisStep": [],
            "acceptedThisStep": [],
            "heldThisStep": ["faction-omniscience-supreme"],
            "currentBlocker": "PG200-B03/PG200-B04",
            "nextPendingGroup": ["banishment-gate"],
            "nextStep": "Prepare and send Banishment Gate/PG200-B03 and PG200-B04 only; use current sources and Return200/Return326 context. Preserve all unrelated holds and authority.",
            "currentPacketStatus": "RETURN326_HELD_VERIFIED_PROCEED_BANISHMENT_GATE_PG200_B03_B04",
            "closureTasksRemaining": 25,
            "firstReviewTasksRemaining": 0,
            "directorConnectionStatus": "Return326 sealed and independently verified. FOS remains held at KR198-B01; next Banishment Gate/PG200-B03 and PG200-B04, then Conjure Demiplane Fortress.",
            "canonicalFilesChanged": False,
            "applicationPerformed": False,
            "currentDirectorReturn": bind(archive_path),
            "currentDirectorDelivery": bind(delivery_path),
            "currentReturnAudit": bind(audit_binding_path),
            "currentReturnReceipt": bind(receipt_path),
            "currentReturn": bind(receipt_path),
            "pendingIdentityAuditBinding": bind(pending_path),
            "runtimeExecuted": False,
        }
    )
    handoff_path = AUDIT / "CURRENT_HANDOFF_327.json"
    handoff_path.write_bytes(pretty(handoff))

    snapshot = (
        "# Current spell-review snapshot — Return326 verified\n\n"
        f"Recorded: {now}\n\n"
        "Authority remains **823 applied / 25 pending / 0 accepted-unapplied**, "
        "with **547 complete procedures / 173 scoped interfaces**. Return326 independently "
        "confirms Faction Omniscience Supreme is held at KR198-B01. The SEA-FACTION-WAR "
        "ledgers remain unadjudicated simulation evidence; KR326-C01's provenance conflict "
        "remains unresolved and closes no witness part.\n\n"
        "Next: **Banishment Gate / PG200-B03 and PG200-B04**. Then: **Conjure Demiplane "
        "Fortress / PG200-B06**. The remaining closure count is 25, with zero first-review "
        "tasks. No acceptance, application, canonical edit, runtime execution, or downstream "
        "approval occurred in this return.\n"
    )
    (AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_327.md").write_text(snapshot, encoding="utf-8")

    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_binding_path), "checks": len(checks), "passed": len(checks), "next": "banishment-gate"}, indent=2))


if __name__ == "__main__":
    main()
