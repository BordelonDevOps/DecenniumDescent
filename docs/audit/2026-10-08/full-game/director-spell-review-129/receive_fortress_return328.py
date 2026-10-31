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
OUT = AUDIT / "conjure_demiplane_fortress_return328_received"
ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_Director_Return328_HELD.zip"
DELIVERY_NAME = "DD_Rank9_ConjureDemiplaneFortress_Director_Return328_HELD_DELIVERY.json"
ARCHIVE_SHA = "47af8e23be318210229f7fd2b360be809b2b7ed5d73b08abcbeaf7a078c3f1f4"
DELIVERY_SHA = "ba085a89c5235b0561acae9dcfa899d54fe59b193cc47b97b7d22e294dcdd68b"
AUTH = {
    "reviewedApplied": 823,
    "pending": 25,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 547,
    "scopedInterfaces": 173,
}
SPELL = "conjure-demiplane-fortress"
BLOCKER = "PG200-B06"
NEXT = "summon-elemental-avatar"
NEXT_BLOCKER = "SH202-B01"


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
    archive_raw, delivery_raw = archive_path.read_bytes(), delivery_path.read_bytes()
    delivery = readj(delivery_path)
    checks: list[dict] = []

    def ck(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    ck(
        "downloaded Director archive and delivery match sealed SHA-256 bindings",
        sha(archive_raw) == ARCHIVE_SHA == delivery["archive"]["sha256"]
        and len(archive_raw) == delivery["archive"]["bytes"] == 2237857
        and crc(archive_raw) == delivery["archive"]["crc32"] == "8f47593d"
        and sha(delivery_raw) == DELIVERY_SHA,
        {"archive": bind(archive_path), "delivery": bind(delivery_path)},
    )
    ck(
        "delivery records an exact one-spell HOLD with no acceptance or application",
        delivery["semanticStatus"] == "HOLD"
        and delivery["acceptedIds"] == delivery["appliedIds"] == []
        and delivery["heldIds"] == [SPELL]
        and delivery["blockerIds"] == [BLOCKER]
        and delivery["canonicalFilesChanged"] is False,
        {key: delivery.get(key) for key in ("semanticStatus", "heldIds", "blockerIds", "acceptedIds", "appliedIds", "canonicalFilesChanged")},
    )
    ck(
        "sealed authority and next identity match the current queue",
        delivery["authorityUnchanged"] == AUTH
        and delivery["closureTasksRemaining"] == 25
        and delivery["firstReviewTasksRemaining"] == 0
        and delivery["nextIdentity"] == NEXT
        and delivery["nextBlockerIds"] == [NEXT_BLOCKER],
        {key: delivery.get(key) for key in ("authorityUnchanged", "closureTasksRemaining", "nextIdentity", "nextBlockerIds")},
    )

    with zipfile.ZipFile(archive_path) as z:
        infos = z.infolist()
        names = [item.filename for item in infos]
        for name in names:
            safe_member(name)
        ck(
            "ZIP CRC, unique members, allowlist and declared member count pass",
            z.testzip() is None
            and len(names) == len(set(names)) == delivery["memberCount"] == 67
            and set(names) == set(delivery["exactAllowlist"]),
            {"members": len(names)},
        )
        payload = {name: z.read(name) for name in names}
        sealed_members = {row["path"]: row for row in delivery["members"]}
        ck(
            "external delivery seals every archive member byte-for-byte",
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
            "internal manifest seals all 66 non-manifest archive members",
            manifest["payloadEntryCount"] == 66
            and set(manifest_members) == set(names) - {"MANIFEST.json"}
            and all(
                len(payload[name]) == manifest_members[name]["bytes"]
                and sha(payload[name]) == manifest_members[name]["sha256"]
                and crc(payload[name]) == manifest_members[name]["crc32"]
                for name in manifest_members
            ),
            {"payloadMembers": len(manifest_members)},
        )

        decision = json.loads(payload["DIRECTOR_DECISION.json"])
        blocker = json.loads(payload["BLOCKER_REASSESSMENT.json"])
        counts = json.loads(payload["COUNTS.json"])
        remaining = json.loads(payload["REMAINING_QUEUE.json"])
        provenance = json.loads(payload["AUTHORSHIP_AND_PROVENANCE.json"])
        validation = json.loads(payload["VALIDATION.json"])
        ck(
            "inner decision preserves Fortress-only HOLD and unchanged authority",
            decision["decision"] == "HOLD"
            and decision["targetIds"] == decision["heldIds"] == [SPELL]
            and decision["acceptedIds"] == decision["appliedIds"] == []
            and decision["blockerIds"] == [BLOCKER]
            and decision["authorityBefore"] == decision["authorityAfter"] == AUTH
            and decision["nextIdentity"] == NEXT
            and decision["nextBlockerIds"] == [NEXT_BLOCKER]
            and decision.get("applicationDisposition") is None,
            {key: decision.get(key) for key in ("decision", "targetIds", "blockerIds", "nextIdentity", "nextBlockerIds")},
        )
        open_parts = blocker["blocker"]["minimalCorrection"]
        ck(
            "PG200-B06 remains open with exactly the 13 recorded witness parts",
            blocker["targetId"] == SPELL
            and blocker["blocker"]["id"] == BLOCKER
            and blocker["blocker"]["status"] == "OPEN"
            and blocker["blocker"]["blocking"] is True
            and open_parts == [f"PG328-W{i:02d}" for i in range(1, 14)]
            and len(blocker["remainingWitnessParts"]) == 13
            and all(row["status"] == "OPEN" for row in blocker["remainingWitnessParts"]),
            {"openWitnessParts": len(open_parts), "sourceGains": [row["id"] for row in blocker["sourceLevelGains"]]},
        )
        gain = {row["id"]: row for row in blocker["sourceLevelGains"]}["PG328-G01"]
        ck(
            "only the verified conditional Arch Dispel acquisition/source subpart is closed",
            "PG328-G01" in blocker["blocker"]["closedSourceSubparts"]
            and gain["status"] == "SOURCE_AND_SELECTED_ACQUISITION_VERIFIED"
            and "Perception" in gain["stillMissing"]
            and "occupied whole-source ending" in gain["stillMissing"],
            {"closedSourceSubparts": blocker["blocker"]["closedSourceSubparts"], "gainStatus": gain["status"]},
        )
        ck(
            "replay/integrity counts and semantic HOLD match the sealed summary",
            counts["cases"] == 14
            and counts["events"] == 138
            and counts["forwardOperations"] == counts["inverseOperations"] == 276
            and counts["dataIntegrityChecks"] == 1398
            and counts["dataFailures"] == 0
            and counts["openWitnessParts"] == 13
            and validation["status"] == "DATA_PASS_SEMANTIC_HOLD"
            and validation["dataCheckCount"] == 1398,
            {key: counts.get(key) for key in ("cases", "events", "forwardOperations", "inverseOperations", "dataIntegrityChecks", "dataFailures", "openWitnessParts")},
        )
        ck(
            "conditional fixture provenance is explicit and no user-event authorship is claimed",
            provenance["actualGameplayClaim"] is False
            and provenance["userEventAuthorshipClaim"] is False
            and provenance["wholeIdentityAccepted"] is False,
            {key: provenance.get(key) for key in ("actualGameplayClaim", "userEventAuthorshipClaim", "wholeIdentityAccepted")},
        )
        ck(
            "embedded next queue retains the 25 pending identities and names Summon Elemental Avatar",
            remaining["authorityUnchanged"] == AUTH
            and remaining["closureTasksRemaining"] == 25
            and remaining["firstReviewTasksRemaining"] == 0
            and remaining["nextIdentity"] == NEXT
            and remaining["nextBlockerIds"] == [NEXT_BLOCKER]
            and SPELL in remaining["pendingIds"]
            and NEXT in remaining["pendingIds"],
            {key: remaining.get(key) for key in ("closureTasksRemaining", "nextIdentity", "nextBlockerIds")},
        )

        for name, raw in payload.items():
            parts = pathlib.PurePosixPath(name).parts
            if len(parts) != 1:
                continue
            target = OUT / parts[0]
            if target.exists() and target.read_bytes() != raw:
                raise RuntimeError(f"extracted member differs: {target}")
            if not target.exists():
                target.write_bytes(raw)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    audit_path = AUDIT / "FORTRESS_RETURN328_INDEPENDENT_AUDIT.json"
    receipt_path = AUDIT / "FORTRESS_RETURN328_RECEIPT.json"
    audit = {
        "id": "FORTRESS-RETURN328-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS",
        "archive": bind(archive_path),
        "delivery": bind(delivery_path),
        "memberCount": 67,
        "checkCount": len(checks),
        "passedChecks": sum(row["passed"] for row in checks),
        "failedChecks": sum(not row["passed"] for row in checks),
        "checks": checks,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "blockerIds": [BLOCKER],
        "closedSourceSubparts": ["PG328-G01"],
        "openWitnessIds": [f"PG328-W{i:02d}" for i in range(1, 14)],
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "authority": AUTH,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    }
    receipt = {
        "id": "FORTRESS-RETURN328-RECEIPT",
        "recordedAtUtc": now,
        "status": "SEALED_HELD_INDEPENDENTLY_VERIFIED",
        "archive": bind(archive_path),
        "delivery": bind(delivery_path),
        "decision": readj(OUT / "DIRECTOR_DECISION.json"),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "blockerIds": [BLOCKER],
        "closedSourceSubparts": ["PG328-G01"],
        "openWitnessIds": [f"PG328-W{i:02d}" for i in range(1, 14)],
        "authority": AUTH,
        "remainingClosureTasks": 25,
        "firstReviewTasks": 0,
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
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

    q0 = readj(AUDIT / "CURRENT_SPELL_QUEUE_328.json")
    p0 = readj(AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_328.json")
    h0 = readj(AUDIT / "CURRENT_HANDOFF_328.json")
    queue = copy.deepcopy(q0)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-329",
        "recordedAtUtc": now,
        "supersedesQueue": "SPELL-REVIEW-QUEUE-328",
        "activeReview": {"spellId": NEXT, "blockerIds": [NEXT_BLOCKER], "packet": None, "status": "DIRECTOR_AUTHORIZED_NEXT_AFTER_FORTRESS_HOLD"},
        "next": NEXT,
        "lastDirectorReturn": "RETURN328_HELD_VERIFIED",
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": [SPELL],
        "currentReturnBlockers": {SPELL: [BLOCKER]},
        "currentReturnDecision": bind(OUT / "DIRECTOR_DECISION.json"),
        "currentReturnArchive": bind(archive_path),
        "currentReturnDelivery": bind(delivery_path),
        "currentReturnAudit": bind(audit_path),
        "currentReturnReceipt": bind(receipt_path),
        "currentReturn": bind(receipt_path),
        "currentPacketStatus": "RETURN328_FORTRESS_HELD_VERIFIED_PROCEED_SUMMON_ELEMENTAL_AVATAR_SH202_B01",
        "pendingIdentityAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT25_PENDING_IDENTITY_AUDIT_329.json",
        "directorConnectionStatus": "Return328 independently verified. Fortress remains held at PG200-B06; the conditional Arch Dispel source/acquisition subpart is closed, while 13 integrated witness parts remain open. Proceed to Summon Elemental Avatar / SH202-B01.",
        "acceptedThisStep": [],
        "appliedThisStep": [],
        "heldThisStep": [SPELL],
        "githubChanges": False,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "currentDirectorInstruction": "Review Summon Elemental Avatar / SH202-B01 next, reusing Return285 source findings. Do not infer a genuine extra-turn provider or combined-damage source; identify any exact scope/design decision the Director can make versus the missing source-bound witnesses. Preserve all unrelated holds and apply only an exact sealed acceptance.",
    })
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_329.json"
    queue_path.write_bytes(pretty(queue))

    pending = copy.deepcopy(p0)
    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-329",
        "recordedAtUtc": now,
        "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_328.json",
        "status": "PASS_CURRENT_823_25_RETURN328_FORTRESS_HOLD_SUMMON_ELEMENTAL_AVATAR_NEXT",
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": [SPELL],
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "nextPendingIds": [NEXT],
        "nextPendingCount": 1,
        "nextStep": "Review Summon Elemental Avatar / SH202-B01 using current spell source and Return285. Reassess the source-qualified genuine full-extra-turn provider, source-bound mixed fire/force damage witness, and four control/aura transitions. Distinguish Director-authorable scoped rulings from missing source facts. Apply only an exact sealed acceptance.",
        "sourceQueue": queue_path.relative_to(ROOT).as_posix(),
        "currentQueueBinding": bind(queue_path),
        "currentReturn": bind(receipt_path),
        "currentReturnAudit": bind(audit_path),
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    })
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_329.json"
    pending_path.write_bytes(pretty(pending))

    handoff = copy.deepcopy(h0)
    handoff.update({
        "id": "SPELL-REVIEW-HANDOFF-329",
        "recordedAtUtc": now,
        "supersedes": "CURRENT-HANDOFF-328",
        "status": "RETURN328_VERIFIED_SUMMON_ELEMENTAL_AVATAR_NEXT",
        "authority": AUTH,
        "scopeIds": [NEXT],
        "blockerIds": [BLOCKER, NEXT_BLOCKER],
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "queueBinding": bind(queue_path),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "pendingIdentityAuditBinding": bind(pending_path),
        "acceptedThisStep": [],
        "appliedThisStep": [],
        "heldThisStep": [SPELL],
        "currentBlocker": NEXT_BLOCKER,
        "nextPendingGroup": [NEXT],
        "nextStep": "Review Summon Elemental Avatar / SH202-B01 using current source-qualified findings and the sealed Return285 HOLD. Preserve all other decisions and do not apply anything without exact sealed acceptance authorization.",
        "currentPacketStatus": "RETURN328_FORTRESS_HELD_VERIFIED_PROCEED_SUMMON_ELEMENTAL_AVATAR_SH202_B01",
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "Return328 sealed and independently verified. Fortress remains held at PG200-B06; the next identity is Summon Elemental Avatar / SH202-B01.",
        "currentDirectorReturn": bind(archive_path),
        "currentDirectorDelivery": bind(delivery_path),
        "currentReturnAudit": bind(audit_path),
        "currentReturnReceipt": bind(receipt_path),
        "currentReturn": bind(receipt_path),
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    })
    (AUDIT / "CURRENT_HANDOFF_329.json").write_bytes(pretty(handoff))
    (AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_329.md").write_text(
        "# Current spell-review snapshot — Return328 verified\n\n"
        f"Recorded: {now}\n\n"
        "Authority remains **823 applied / 25 pending / 0 accepted-unapplied**, with **547 complete procedures / 173 scoped interfaces**. Return328 independently confirms Conjure Demiplane Fortress remains held at PG200-B06. The conditional Wizard20 Arch Dispel source/acquisition subpart is verified; 13 integrated witness parts remain open. No acceptance or application occurred.\n\n"
        "Next: **Summon Elemental Avatar / SH202-B01**. Reuse Return285 findings and distinguish source-bound missing witnesses from any scoped design ruling within the Director’s authority. There are 25 closure tasks remaining and zero first-review tasks.\n",
        encoding="utf-8",
    )
    print(json.dumps({"receipt": str(receipt_path), "audit": str(audit_path), "checks": len(checks), "passed": len(checks), "accepted": [], "applied": [], "next": NEXT}, indent=2))


if __name__ == "__main__":
    main()
