from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import zipfile
import zlib
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
DOWNLOADS = pathlib.Path(r"C:\Users\cbord\Downloads")
OUT = AUDIT / "rank9_time_stop_return318_received"
ZIP_NAME = "DD_Rank9_TimeStop_Director_Return318_HELD.zip"
DELIVERY_NAME = "DD_Rank9_TimeStop_Director_Return318_HELD_DELIVERY.json"
CONTRACT_NAME = "TF318_JOINT_INTERFACE_CONTRACT.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(p: pathlib.Path) -> dict[str, Any]:
    raw = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read_json(p: pathlib.Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def safe_member(name: str) -> None:
    path = pathlib.PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"unsafe ZIP member: {name}")


def main() -> None:
    src_zip = DOWNLOADS / ZIP_NAME
    src_delivery = DOWNLOADS / DELIVERY_NAME
    src_contract = DOWNLOADS / CONTRACT_NAME
    for src in (src_zip, src_delivery, src_contract):
        if not src.is_file():
            raise FileNotFoundError(src)
    OUT.mkdir(parents=True, exist_ok=True)
    local_zip, local_delivery, local_contract = OUT / ZIP_NAME, OUT / DELIVERY_NAME, OUT / CONTRACT_NAME
    for source, dest in ((src_zip, local_zip), (src_delivery, local_delivery), (src_contract, local_contract)):
        if dest.exists() and dest.read_bytes() != source.read_bytes():
            raise RuntimeError(f"existing file differs from downloaded sealed artifact: {dest}")
        if not dest.exists():
            shutil.copyfile(source, dest)

    delivery = read_json(local_delivery)
    archive_raw = local_zip.read_bytes()
    checks: list[dict[str, Any]] = []
    def check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
        if not passed:
            raise AssertionError(f"failed: {name}: {detail}")

    actual_archive = {"filename": local_zip.name, "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": f"{zlib.crc32(archive_raw) & 0xffffffff:08x}"}
    check("outer archive matches sealed DELIVERY size, SHA-256 and CRC32", actual_archive == delivery["archive"], actual_archive)
    check("Director delivery scope/status is exact Time Stop HOLD", delivery["status"] == "SEALED_HELD" and delivery["acceptedIds"] == [] and delivery["appliedIds"] == [] and delivery["heldIds"] == ["time-stop"] and delivery["blockerIds"] == ["TF192-B01"], {k: delivery.get(k) for k in ["status", "acceptedIds", "appliedIds", "heldIds", "blockerIds"]})

    with zipfile.ZipFile(local_zip) as zf:
        names = zf.namelist()
        expected_names = delivery["exactAllowlist"]
        bad = []
        for name in names:
            try:
                safe_member(name)
            except ValueError:
                bad.append(name)
        check("ZIP CRC, unique member names, exact allowlist and safe paths", zf.testzip() is None and len(names) == len(set(names)) and set(names) == set(expected_names) and not bad, {"count": len(names), "unsafe": bad})
        member_errors = []
        member_meta = {x["path"]: x for x in delivery["members"]}
        for name in names:
            raw = zf.read(name)
            meta = member_meta.get(name)
            if not meta or len(raw) != meta["bytes"] or sha(raw) != meta["sha256"] or f"{zlib.crc32(raw) & 0xffffffff:08x}" != meta["crc32"]:
                member_errors.append(name)
            out_path = OUT / pathlib.Path(*pathlib.PurePosixPath(name).parts)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if out_path.exists() and out_path.read_bytes() != raw:
                raise RuntimeError(f"existing extracted member differs from archive: {out_path}")
            if not out_path.exists():
                out_path.write_bytes(raw)
        check("all member bytes, SHA-256 and CRC32 match the sealed manifest", not member_errors and len(member_meta) == len(names), {"errors": member_errors})
        contract_raw = zf.read("TF318_JOINT_INTERFACE_CONTRACT.md")
        check("standalone contract download exactly matches sealed archive contract", local_contract.read_bytes() == contract_raw and len(contract_raw) == delivery["jointContract"]["bytes"] and sha(contract_raw) == delivery["jointContract"]["sha256"], {"bytes": len(contract_raw), "sha256": sha(contract_raw)})

        decision = read_json(OUT / "DIRECTOR_DECISION.json")
        joint = read_json(OUT / "JOINT_INTERFACE_AUTHORIZATION.json")
        queue_director = read_json(OUT / "REMAINING_QUEUE.json")
        checks_blob = read_json(OUT / "PACKAGE_CHECKS.json")
        validation = read_json(OUT / "DATA_VALIDATION.json")
        check("sealed decision binds exact Time Stop-only HOLD and unchanged 823/25/0", decision["scopeIds"] == ["time-stop"] and decision["acceptedIds"] == [] and decision["appliedIds"] == [] and decision["heldIds"] == ["time-stop"] and decision["authorityAfter"] == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}, {"authority": decision["authorityAfter"], "next": decision["nextIdentity"]})
        check("joint interface is authorized only for conditional witness construction; both blockers stay open", joint["id"] == "TF318-JOINT-INTERFACE-01" and joint["status"] == "AUTHORIZED_FOR_CONDITIONAL_WITNESS_CONSTRUCTION_ONLY" and joint["wholeSpellBlockersClosed"] == [] and joint["linkedBlockerIds"] == ["TF192-B01", "DF218-B03"] and joint["acceptedIds"] == [] and joint["appliedIds"] == [], {"status": joint["status"], "blockers": joint["linkedBlockerIds"]})
        check("all 12 Director package checks and 1,266 data checks pass", checks_blob["status"] == "PASS" and all(x["passed"] for x in checks_blob["checks"]) and delivery["dataCheckCount"] == 1266, {"checks": len(checks_blob["checks"]), "data": delivery["dataCheckCount"]})
        check("14 cases replay across 216 events and 432 forward/432 inverse operations", delivery["counts"]["cases"] == 14 and delivery["counts"]["events"] == 216 and delivery["counts"]["forwardOperations"] == 432 and delivery["counts"]["inverseOperations"] == 432 and delivery["counts"]["fullReverseTraversals"] == 14 and validation["status"] == "PASS", delivery["counts"])
        check("the sealed queue retains all 25 pending identities and directs Fate Rewrite next", len(queue_director["pendingIds"]) == 25 and queue_director["nextAfterThisHold"] == "fate-rewrite" and decision["nextIdentity"] == "fate-rewrite" and decision["nextBlocker"] == "TF192-B04", {"next": queue_director["nextAfterThisHold"], "pending": len(queue_director["pendingIds"])})
        expected_closed_gates = {"runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"}
        check("five unrelated holds and all downstream approval gates remain preserved/closed", set(queue_director["separatelyRetainedHoldsUnchanged"]) == {"final-word", "elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave"} and delivery["canonicalEdits"] is False and delivery["applicationPerformed"] is False and delivery["allDownstreamGatesClosed"] is True and set(decision["gatesClosed"]) == expected_closed_gates, {"separateHolds": queue_director["separatelyRetainedHoldsUnchanged"], "application": delivery["applicationPerformed"], "gatesClosed": decision["gatesClosed"]})

    current_queue317 = read_json(AUDIT / "CURRENT_SPELL_QUEUE_317.json")
    local_index = (ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json").read_bytes()
    local_catalog = (ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json").read_bytes()
    check("sealed Return318 input queue317 is byte-exact to the local authority record", (OUT / "authority/CURRENT_SPELL_QUEUE_317.json").read_bytes() == (AUDIT / "CURRENT_SPELL_QUEUE_317.json").read_bytes(), bind(AUDIT / "CURRENT_SPELL_QUEUE_317.json"))
    check("Return318 confirms canonical index/catalog were unchanged and current snapshots remain unchanged", decision["noChanges"]["index"] and decision["noChanges"]["catalog"] and local_catalog == (ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json").read_bytes() and sha(local_index) == "c6dd6d30703911864a3e2784d8abb3d79835b39bc01804c4335f80a1c4bea7b2", {"indexSha256": sha(local_index), "catalogBytes": len(local_catalog)})

    audit = {
        "id": "TIME-STOP-RETURN318-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS",
        "archive": bind(local_zip), "delivery": bind(local_delivery), "jointContract": bind(local_contract),
        "memberCount": len(delivery["members"]), "checkCount": len(checks), "passedChecks": sum(1 for x in checks if x["passed"]), "failedChecks": sum(1 for x in checks if not x["passed"]),
        "checks": checks,
        "decision": {"acceptedIds": [], "appliedIds": [], "heldIds": ["time-stop"], "blockerIds": ["TF192-B01"]},
        "authority": decision["authorityAfter"], "remainingClosureTasks": 25, "firstReviewTasks": 0,
        "nextIdentity": "fate-rewrite", "nextBlocker": "TF192-B04",
        "jointInterfaceId": joint["id"], "jointInterfaceStatus": joint["status"],
        "canonicalFilesChanged": False, "applicationPerformed": False, "runtimeExecuted": False,
    }
    audit_path = AUDIT / "TIME_STOP_RETURN318_INDEPENDENT_AUDIT.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "id": "TIME-STOP-RETURN318-RECEIPT",
        "recordedAtUtc": audit["recordedAtUtc"], "status": "SEALED_HELD_VERIFIED",
        "archive": bind(local_zip), "delivery": bind(local_delivery), "jointContract": bind(local_contract), "independentAudit": bind(audit_path),
        "acceptedIds": [], "appliedIds": [], "heldIds": ["time-stop"], "blockerIds": ["TF192-B01"],
        "jointInterfaceAuthorizationId": "TF318-JOINT-INTERFACE-01", "jointInterfaceStatus": joint["status"],
        "authority": decision["authorityAfter"], "remainingClosureTasks": 25, "firstReviewTasks": 0,
        "nextIdentity": "fate-rewrite", "nextBlocker": "TF192-B04",
        "missingWitness": "Complete actor/acquisition histories and independently reversible natural-completion, legal-interruption and failed-removal branches under TF318-JOINT-INTERFACE-01. Time Stop remains pending; neither spell is accepted by the contract.",
        "canonicalFilesChanged": False, "applicationPerformed": False, "runtimeExecuted": False,
    }
    receipt_path = AUDIT / "TIME_STOP_RETURN318_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    queue318 = read_json(AUDIT / "CURRENT_SPELL_QUEUE_318.json")
    queue319 = dict(queue318)
    queue319.update({
        "id": "SPELL-REVIEW-QUEUE-319", "recordedAtUtc": audit["recordedAtUtc"], "supersedesQueue": "SPELL-REVIEW-QUEUE-318",
        "activeReview": {"spellId": "fate-rewrite", "blockerIds": ["TF192-B04"], "packet": "FRESH_AUTHORITY_PACKET_REQUIRED_823_25", "status": "NEXT_PRIORITY"},
        "next": "fate-rewrite", "nextPendingIds": ["fate-rewrite", "collapse-timeline", "eternal-prophecy"], "nextPendingCount": 3,
        "timeStopDisposition": {"held": True, "blockerIds": ["TF192-B01"], "resubmissionPermitted": True, "jointInterfaceAuthorizationId": "TF318-JOINT-INTERFACE-01", "jointInterfaceStatus": joint["status"], "requiredEvidence": receipt["missingWitness"]},
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": ["time-stop"],
        "currentReturnBlockers": {"time-stop": ["TF192-B01"]}, "currentReturnDecision": bind(OUT / "DIRECTOR_DECISION.json"),
        "currentReturnArchive": bind(local_zip), "currentReturnDelivery": bind(local_delivery), "currentReturnAudit": bind(audit_path),
        "currentJointInterfaceContract": bind(local_contract), "currentReturnReceipt": bind(receipt_path),
        "currentPendingIdentityAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT25_PENDING_IDENTITY_AUDIT_319.json",
        "currentHandoff": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_319.json",
        "pendingCount": 25, "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "Return318 sealed HOLD verified; TF318-JOINT-INTERFACE-01 authorized for witness construction only. Time Stop remains pending. Fate Rewrite / TF192-B04 is next.",
        "githubChanges": False, "canonicalFilesChanged": False, "applicationPerformed": False,
    })
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_319.json"
    queue_path.write_text(json.dumps(queue319, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pending317 = read_json(AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_317.json")
    pending319 = dict(pending317)
    pending319.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-319", "recordedAtUtc": audit["recordedAtUtc"],
        "status": "PASS_CURRENT_823_25_TIME_STOP_HELD_FATE_REWRITE_NEXT", "supersedes": "CURRENT25_PENDING_IDENTITY_AUDIT_317.json",
        "sourceQueue": bind(queue_path), "pendingCount": 25, "acceptedIds": [], "appliedIds": [],
        "heldThisStep": ["time-stop"], "timeStopBlockers": ["TF192-B01"], "timeStopJointInterfaceAuthorization": bind(local_contract),
        "nextGroup": "rank9-time-fate6", "nextPendingIds": queue319["nextPendingIds"], "nextPendingCount": 3,
        "nextStep": "Prepare a fresh Fate Rewrite-only authority/source packet at 823/25/0 for TF192-B04, confer with Director, and keep Time Stop held with TF318 witness construction authorized.",
        "currentReturn": bind(local_zip), "currentReturnDelivery": bind(local_delivery), "currentReturnAudit": bind(audit_path),
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0, "canonicalFilesChanged": False,
    })
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_319.json"
    pending_path.write_text(json.dumps(pending319, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff318 = read_json(AUDIT / "CURRENT_HANDOFF_318.json")
    handoff319 = dict(handoff318)
    handoff319.update({
        "id": "SPELL-REVIEW-HANDOFF-319", "recordedAtUtc": audit["recordedAtUtc"], "supersedes": "CURRENT-HANDOFF-318",
        "status": "RETURN318_HELD_VERIFIED_FATE_REWRITE_NEXT", "scopeIds": ["time-stop"],
        "acceptedThisStep": [], "appliedThisStep": [], "heldThisStep": ["time-stop"], "currentBlocker": "TF192-B01",
        "queue": queue_path.relative_to(ROOT).as_posix(), "queueBinding": bind(queue_path),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(), "pendingIdentityAuditBinding": bind(pending_path),
        "currentReturnReceipt": bind(receipt_path), "currentDirectorReturn": bind(local_zip), "currentDirectorDelivery": bind(local_delivery),
        "currentReturnAudit": bind(audit_path), "jointInterfaceContract": bind(local_contract),
        "nextPendingGroup": ["fate-rewrite", "collapse-timeline", "eternal-prophecy"],
        "nextStep": "Prepare Fate Rewrite / TF192-B04-only packet at current authority 823/25/0. Retain Time Stop as held; its paired witness may be re-submitted under TF318-JOINT-INTERFACE-01.",
        "closureTasksRemaining": 25, "firstReviewTasksRemaining": 0, "canonicalFilesChanged": False,
    })
    handoff_path = AUDIT / "CURRENT_HANDOFF_319.json"
    handoff_path.write_text(json.dumps(handoff319, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    snapshot_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_319.md"
    snapshot_path.write_text("# Spell review snapshot 319\n\nAuthority: **823 applied / 25 pending / 0 accepted-unapplied**; 547 procedures / 173 scoped interfaces. Return318 holds Time Stop / TF192-B01. TF318-JOINT-INTERFACE-01 authorizes witness construction only; both Time Stop and Timeless Form remain pending. The next Director-directed identity is Fate Rewrite / TF192-B04. Closure tasks: 25; first-review tasks: 0.\n", encoding="utf-8")

    print(json.dumps({"status": audit["status"], "checks": len(checks), "passed": audit["passedChecks"], "archive": receipt["archive"], "delivery": receipt["delivery"], "contract": receipt["jointContract"], "authority": decision["authorityAfter"], "remainingClosureTasks": 25, "nextIdentity": "fate-rewrite", "audit": bind(audit_path), "receipt": bind(receipt_path), "queue": bind(queue_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
