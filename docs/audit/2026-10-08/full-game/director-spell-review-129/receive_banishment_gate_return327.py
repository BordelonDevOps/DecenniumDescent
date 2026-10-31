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
OUT = AUDIT / "banishment_gate_return327_received"
ZIP_NAME = "DD_Rank9_BanishmentGate_Director_Return327_HELD.zip"
DELIVERY_NAME = "DD_Rank9_BanishmentGate_Director_Return327_HELD_DELIVERY.json"
AUTH = {
    "reviewedApplied": 823,
    "pending": 25,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 547,
    "scopedInterfaces": 173,
}
BLOCKERS = ["PG200-B03", "PG200-B04"]
NEXT = "conjure-demiplane-fortress"
NEXT_BLOCKERS = ["PG200-B06"]


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
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


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
        "archive matches Director delivery byte count, SHA-256 and CRC32",
        len(archive_raw) == delivery["archive"]["bytes"] == 757821
        and sha(archive_raw) == delivery["archive"]["sha256"] == "3bd6b2f192c4e63fcee587b234e0d6877ce20c152ab99891ca797030e32755c7"
        and crc(archive_raw) == delivery["archive"]["crc32"] == "dc50d4c4",
        delivery["archive"],
    )
    ck(
        "delivery records a one-spell sealed HOLD with exact blockers and no application",
        delivery["semanticStatus"] == "HOLD"
        and delivery["acceptedIds"] == []
        and delivery["appliedIds"] == []
        and delivery["heldIds"] == ["banishment-gate"]
        and delivery["blockerIds"] == BLOCKERS
        and delivery["application"] is False
        and delivery["canonicalFilesChanged"] is False,
        {key: delivery.get(key) for key in ("semanticStatus", "heldIds", "blockerIds", "application", "canonicalFilesChanged")},
    )
    ck(
        "authority, closure counts and next identity match the sealed queue",
        delivery["authorityUnchanged"] == AUTH
        and delivery["closureTasksRemaining"] == 25
        and delivery["firstReviewTasksRemaining"] == 0
        and delivery["nextIdentity"] == NEXT
        and delivery["nextBlockerIds"] == NEXT_BLOCKERS,
        {key: delivery.get(key) for key in ("authorityUnchanged", "closureTasksRemaining", "nextIdentity", "nextBlockerIds")},
    )

    with zipfile.ZipFile(archive_path) as z:
        names = [item.filename for item in z.infolist()]
        for name in names:
            safe_member(name)
        ck(
            "ZIP CRC, unique members, exact allowlist and declared count",
            z.testzip() is None
            and len(names) == len(set(names)) == delivery["memberCount"] == 48
            and set(names) == set(delivery["exactAllowlist"]),
            {"members": len(names)},
        )
        sealed_members = {row["path"]: row for row in delivery["members"]}
        payload = {name: z.read(name) for name in names}
        ck(
            "delivery seals every archive member byte count, SHA-256 and CRC32",
            set(sealed_members) == set(names)
            and all(
                len(payload[name]) == sealed_members[name]["bytes"]
                and sha(payload[name]) == sealed_members[name]["sha256"]
                and crc(payload[name]) == sealed_members[name]["crc32"]
                for name in names
            ),
            {"sealedMembers": len(sealed_members)},
        )
        manifest = json.loads(payload["MANIFEST.json"])
        manifest_members = {row["path"]: row for row in manifest["members"]}
        ck(
            "internal manifest seals the 46 manifest-bound payload members; nested source manifest is outer-sealed",
            manifest["payloadEntryCount"] == 46
            and set(manifest_members) == set(names) - {"MANIFEST.json", "evidence/packet327/MANIFEST.json"}
            and all(
                len(payload[name]) == manifest_members[name]["bytes"]
                and sha(payload[name]) == manifest_members[name]["sha256"]
                and crc(payload[name]) == manifest_members[name]["crc32"]
                for name in manifest_members
            ),
            {"payloadMembers": len(manifest_members)},
        )

        decision = json.loads(payload["DIRECTOR_DECISION.json"])
        blockers = json.loads(payload["BLOCKER_REASSESSMENT.json"])
        validation = json.loads(payload["VALIDATION.json"])
        counts = json.loads(payload["COUNTS.json"])
        data_check = json.loads(payload["DATA_INTEGRITY_CHECK.json"])
        replay = json.loads(payload["REPLAY_RESULTS.json"])
        cases = json.loads(payload["CASE_DISPOSITIONS.json"])
        qualifications = json.loads(payload["QUALIFICATIONS.json"])
        remaining = json.loads(payload["REMAINING_QUEUE.json"])
        semantic = json.loads(payload["INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"])

        ck(
            "inner decision is Banishment Gate-only HOLD; authority and other gates are unchanged",
            decision["decision"] == "HOLD"
            and decision["targetIds"] == decision["heldIds"] == ["banishment-gate"]
            and decision["acceptedIds"] == decision["appliedIds"] == []
            and decision["blockerIds"] == BLOCKERS
            and decision["authorityBefore"] == decision["authorityAfter"] == AUTH
            and decision["nextIdentity"] == NEXT
            and decision["nextBlockerIds"] == NEXT_BLOCKERS
            and decision["applicationDisposition"].startswith("None."),
            {key: decision.get(key) for key in ("decision", "targetIds", "blockerIds", "nextIdentity")},
        )
        gains = {row["id"]: row for row in decision["sourceLevelGains"]}
        ck(
            "both source-level gains are narrow and leave encounter blockers open",
            set(gains) == {"PG327-B03-SOURCE-PROFILE", "PG327-B04-FINITE-CARGO-CONTRACT"}
            and gains["PG327-B03-SOURCE-PROFILE"]["status"] == "CLOSED_SOURCE_AVAILABILITY_SUBPART_ONLY"
            and gains["PG327-B04-FINITE-CARGO-CONTRACT"]["status"] == "CLOSED_SOURCE_RULE_AVAILABILITY_SUBPART_ONLY"
            and all(row["status"] == "OPEN" for row in blockers["blockers"]),
            {key: value["status"] for key, value in gains.items()},
        )
        ck(
            "all ten inherited PG200 qualifications remain retained",
            [row["id"] for row in qualifications["qualifications"]] == [f"PG200-H{i:02d}" for i in range(1, 11)]
            and all(row["status"] == "RETAINED" for row in qualifications["qualifications"]),
            {"qualificationCount": len(qualifications["qualifications"])},
        )
        ck(
            "all 1,096 integrity checks pass while the two semantic blockers stay held",
            validation["status"] == "DATA_PASS_SEMANTIC_HOLD"
            and validation["dataCheckCount"] == data_check["checkCount"] == data_check["passed"] == 1096
            and validation["dataFailed"] == data_check["failed"] == 0
            and all(row["pass"] for row in data_check["checks"])
            and validation["semanticHoldIds"] == BLOCKERS
            and semantic["identityDecision"] == "HOLD"
            and semantic["blockerIds"] == BLOCKERS,
            {"dataChecks": validation["dataCheckCount"], "semanticHolds": semantic["blockerIds"]},
        )
        ck(
            "nine preserved cases and all reversible event operations match the sealed summary",
            counts["preservedCases"] == 9
            and counts["events"] == 129
            and counts["forwardOperations"] == counts["inverseOperations"] == 258
            and counts["fullReverseTraversals"] == 9
            and counts["ruleOnlyBranchRecords"] == 7
            and counts["wholeRequiredMainCasesComplete"] == 0
            and replay["status"] == "PASS"
            and replay["counts"]["preservedCases"] == 9
            and len(replay["cases"]) == 9
            and all(row.get("replay") == "PASS" for row in replay["cases"])
            and all(not row.get("wholeRequiredCaseComplete", False) for row in cases["cases"]),
            {key: counts[key] for key in ("preservedCases", "events", "forwardOperations", "inverseOperations", "ruleOnlyBranchRecords")},
        )
        ck(
            "PG200-B03/B04 remain open with exact eight minimum witnesses; only source subparts close",
            {row["id"]: row for row in blockers["blockers"]}["PG200-B03"]["status"] == "OPEN"
            and {row["id"]: row for row in blockers["blockers"]}["PG200-B04"]["status"] == "OPEN"
            and set(decision["minimumWitnessIds"]) == {f"PG327-W{i:02d}" for i in range(1, 9)}
            and len(blockers["sourceLevelGains"]) == 2,
            {"minimumWitnessIds": decision["minimumWitnessIds"]},
        )
        ck(
            "priority queue remains unchanged and Conjure Demiplane Fortress is next",
            remaining["authorityUnchanged"] == AUTH
            and remaining["closureTasksRemaining"] == 25
            and remaining["firstReviewTasksRemaining"] == 0
            and remaining["nextIdentity"] == NEXT
            and remaining["nextBlockerIds"] == NEXT_BLOCKERS
            and "banishment-gate" in remaining["pendingIds"],
            {key: remaining.get(key) for key in ("closureTasksRemaining", "nextIdentity", "nextBlockerIds")},
        )

        for name, raw in payload.items():
            target = OUT.joinpath(*pathlib.PurePosixPath(name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != raw:
                raise RuntimeError(f"extracted member differs: {target}")
            if not target.exists():
                target.write_bytes(raw)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    receipt_path = AUDIT / "BANISHMENT_GATE_RETURN327_RECEIPT.json"
    audit_path = AUDIT / "BANISHMENT_GATE_RETURN327_INDEPENDENT_AUDIT.json"
    audit = {
        "id": "BANISHMENT-GATE-RETURN327-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS",
        "archive": bind(archive_path),
        "delivery": bind(delivery_path),
        "memberCount": 48,
        "checkCount": len(checks),
        "passedChecks": sum(row["passed"] for row in checks),
        "failedChecks": sum(not row["passed"] for row in checks),
        "checks": checks,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["banishment-gate"],
        "blockerIds": BLOCKERS,
        "sourceLevelGains": ["PG327-B03-SOURCE-PROFILE", "PG327-B04-FINITE-CARGO-CONTRACT"],
        "minimumWitnessIds": [f"PG327-W{i:02d}" for i in range(1, 9)],
        "nextIdentity": NEXT,
        "nextBlockerIds": NEXT_BLOCKERS,
        "authority": AUTH,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    }
    receipt = {
        "id": "BANISHMENT-GATE-RETURN327-RECEIPT",
        "recordedAtUtc": now,
        "status": "SEALED_HELD_INDEPENDENTLY_VERIFIED",
        "archive": bind(archive_path),
        "delivery": bind(delivery_path),
        "decision": readj(OUT / "DIRECTOR_DECISION.json"),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["banishment-gate"],
        "blockerIds": BLOCKERS,
        "sourceLevelGains": ["PG327-B03-SOURCE-PROFILE", "PG327-B04-FINITE-CARGO-CONTRACT"],
        "minimumWitnessIds": [f"PG327-W{i:02d}" for i in range(1, 9)],
        "authority": AUTH,
        "remainingClosureTasks": 25,
        "firstReviewTasks": 0,
        "nextIdentity": NEXT,
        "nextBlockerIds": NEXT_BLOCKERS,
        "checks": checks,
        "checkCount": len(checks),
        "passedChecks": sum(row["passed"] for row in checks),
        "failedChecks": sum(not row["passed"] for row in checks),
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    }
    audit_path.write_bytes(pretty(audit))
    receipt_path.write_bytes(pretty(receipt))

    q0 = readj(AUDIT / "CURRENT_SPELL_QUEUE_327.json")
    p0 = readj(AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_327.json")
    h0 = readj(AUDIT / "CURRENT_HANDOFF_327.json")
    queue = copy.deepcopy(q0)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-328",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-327",
        "nextGroup": "rank9-planar-gates5",
        "nextPendingIds": [NEXT],
        "nextPendingCount": 1,
        "activeReview": {"spellId": NEXT, "blockerIds": NEXT_BLOCKERS, "packet": None, "status": "DIRECTOR_AUTHORIZED_NEXT_AFTER_BANISHMENT_GATE_HOLD"},
        "next": NEXT,
        "lastDirectorReturn": "RETURN327_HELD_VERIFIED",
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": ["banishment-gate"],
        "currentReturnBlockers": {"banishment-gate": BLOCKERS},
        "currentReturnDecision": bind(OUT / "DIRECTOR_DECISION.json"),
        "currentReturnArchive": bind(archive_path),
        "currentReturnDelivery": bind(delivery_path),
        "currentReturnAudit": bind(audit_path),
        "currentReturnReceipt": bind(receipt_path),
        "currentReturn": bind(receipt_path),
        "currentPacketStatus": "RETURN327_BANISHMENT_GATE_HELD_VERIFIED_PROCEED_FORTRESS_PG200_B06",
        "pendingIdentityAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT25_PENDING_IDENTITY_AUDIT_328.json",
        "directorConnectionStatus": "Return327 independently verified. Banishment Gate remains held at PG200-B03/B04; AC5 source profile and finite cargo rules close only source-availability subparts. Proceed to Conjure Demiplane Fortress / PG200-B06.",
        "githubChanges": False,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "acceptedThisStep": [],
        "appliedThisStep": [],
        "currentDirectorInstruction": "Review Conjure Demiplane Fortress / PG200-B06 only, as directed by sealed Return327. Preserve Banishment Gate PG200-B03/B04 and every unrelated hold. No acceptance or application unless supported by an explicit sealed Director decision.",
    })
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_328.json"
    queue_path.write_bytes(pretty(queue))

    pending = copy.deepcopy(p0)
    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-328",
        "recordedAtUtc": now,
        "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_327.json",
        "status": "PASS_CURRENT_823_25_RETURN327_BANISHMENT_GATE_HOLD_FORTRESS_NEXT",
        "acceptedIds": [],
        "appliedIds": [],
        "nextGroup": "rank9-planar-gates5",
        "nextPendingIds": [NEXT],
        "nextPendingCount": 1,
        "nextStep": "Prepare and submit a Conjure Demiplane Fortress / PG200-B06-only packet with current source-qualified authority, Return200 and Return327 evidence, and all required lifecycle witnesses. Preserve the two Banishment Gate blockers and unrelated holds.",
        "sourceQueue": queue_path.relative_to(ROOT).as_posix(),
        "currentQueueBinding": bind(queue_path),
        "heldThisStep": ["banishment-gate"],
        "currentReturn": bind(receipt_path),
        "nextIdentity": NEXT,
        "nextBlockerIds": NEXT_BLOCKERS,
        "nextPendingCount": 1,
        "canonicalFilesChanged": False,
    })
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_328.json"
    pending_path.write_bytes(pretty(pending))

    handoff = copy.deepcopy(h0)
    handoff.update({
        "id": "SPELL-REVIEW-HANDOFF-328",
        "recordedAtUtc": now,
        "supersedes": "CURRENT-HANDOFF-327",
        "status": "RETURN327_VERIFIED_FORTRESS_NEXT",
        "authority": AUTH,
        "scopeIds": [NEXT],
        "blockerIds": BLOCKERS + ["PG200-B06", "KR198-B01", "TF192-B02", "TF192-B04", "TF192-B05"],
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "queueBinding": bind(queue_path),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "appliedThisStep": [],
        "acceptedThisStep": [],
        "heldThisStep": ["banishment-gate"],
        "currentBlocker": "PG200-B06",
        "nextPendingGroup": [NEXT],
        "nextStep": "Prepare and send a Conjure Demiplane Fortress / PG200-B06-only source packet. Preserve Return327 Banishment Gate hold and all unrelated decisions.",
        "currentPacketStatus": "RETURN327_BANISHMENT_GATE_HELD_VERIFIED_PROCEED_FORTRESS_PG200_B06",
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "Return327 sealed and independently verified. Banishment Gate remains held at PG200-B03/B04; next Conjure Demiplane Fortress / PG200-B06.",
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "currentDirectorReturn": bind(archive_path),
        "currentDirectorDelivery": bind(delivery_path),
        "currentReturnAudit": bind(audit_path),
        "currentReturnReceipt": bind(receipt_path),
        "currentReturn": bind(receipt_path),
        "pendingIdentityAuditBinding": bind(pending_path),
        "runtimeExecuted": False,
    })
    (AUDIT / "CURRENT_HANDOFF_328.json").write_bytes(pretty(handoff))
    snapshot = (
        "# Current spell-review snapshot — Return327 verified\n\n"
        f"Recorded: {now}\n\n"
        "Authority remains **823 applied / 25 pending / 0 accepted-unapplied**, with **547 complete procedures / 173 scoped interfaces**. "
        "Return327 independently confirms Banishment Gate remains held at PG200-B03 and PG200-B04. AC5 closes only the Humanoid source-profile and finite cargo-rule availability subparts; the integrated Gate crossings, guard branches, living carriage, escape, corpse, and expiry/cargo witnesses remain open.\n\n"
        "Next: **Conjure Demiplane Fortress / PG200-B06**. The remaining closure count is 25, with zero first-review tasks. No acceptance, application, canonical edit, runtime execution, or downstream approval occurred in Return327.\n"
    )
    (AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_328.md").write_text(snapshot, encoding="utf-8")
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": len(checks), "next": NEXT}, indent=2))


if __name__ == "__main__":
    main()
