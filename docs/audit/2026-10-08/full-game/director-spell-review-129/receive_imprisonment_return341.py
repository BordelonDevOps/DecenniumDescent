#!/usr/bin/env python3
"""Independently verify sealed Imprisonment Return341 and advance the queue."""
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
PREP = A / "rank9_imprisonment_review_341_prepared"
PREP_ZIP = PREP / "DD_Rank9_Imprisonment_Review341.zip"
PREP_DELIVERY = PREP / "DD_Rank9_Imprisonment_Review341_DELIVERY.json"
DOWNLOADS = Path.home() / "Downloads"
IN_ZIP = DOWNLOADS / "DD_Imprisonment_Director_Return341_HELD.zip"
IN_DELIVERY = DOWNLOADS / "DD_Imprisonment_Director_Return341_HELD_DELIVERY.json"
RECEIVED = A / "rank9_imprisonment_return341_received"
PAYLOAD = RECEIVED / "payload"
ARCHIVE = RECEIVED / IN_ZIP.name
DELIVERY = RECEIVED / IN_DELIVERY.name
AUDIT = A / "IMPRISONMENT_RETURN341_INDEPENDENT_AUDIT.json"
RECEIPT = A / "IMPRISONMENT_RETURN341_RECEIPT.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_341.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_341.json"
HANDOFF = A / "CURRENT_HANDOFF_341.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_341.md"
AUTHORITY = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
SPELL = "imprisonment"
BLOCKER = "PC232-B02"
NEXT = "divine-intervention-greater"
NEXT_BLOCKER = "MR233-B01"
NEXT_GROUP = "rank9-miracle-reality2"
checks: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def check(ident: str, passed: bool, detail: str) -> None:
    checks.append({"id": ident, "passed": bool(passed), "detail": detail})


def safe_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and ":" not in name and not name.startswith("/")


def main() -> None:
    for path in (IN_ZIP, IN_DELIVERY, PREP_ZIP, PREP_DELIVERY, A / "CURRENT_SPELL_QUEUE_340.json", A / "CURRENT25_PENDING_IDENTITY_AUDIT_340.json", A / "CURRENT_HANDOFF_340.json"):
        if not path.is_file():
            raise FileNotFoundError(path)
    RECEIVED.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(IN_ZIP, ARCHIVE)
    shutil.copyfile(IN_DELIVERY, DELIVERY)
    archive_bytes = ARCHIVE.read_bytes()
    delivery = json.loads(DELIVERY.read_bytes())
    expected_archive = delivery.get("archive", {})

    check("delivery-identity", delivery.get("id") == "IMPRISONMENT-DIRECTOR-RETURN341-HELD-DELIVERY" and delivery.get("reviewId") == "Return341", "Return341 delivery identity.")
    check("archive-name-size-sha-crc", expected_archive.get("fileName") == ARCHIVE.name and (expected_archive.get("bytes"), expected_archive.get("sha256"), expected_archive.get("crc32")) == (len(archive_bytes), sha(archive_bytes), crc(archive_bytes)), json.dumps(expected_archive))
    check("single-target-hold-no-accept-or-apply", delivery.get("targetIds") == [SPELL] and delivery.get("heldIds") == [SPELL] and delivery.get("blockerIds") == [BLOCKER] and delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [], "Imprisonment / PC232-B02 only.")
    check("application-not-authorized", delivery.get("applicationAuthorized") is False and delivery.get("canonicalMutation") is False and delivery.get("releaseApproved") is False, "No application or canonical mutation authorized.")
    check("authority-unchanged", delivery.get("authority") == AUTHORITY, repr(delivery.get("authority")))
    check("next-priority-exact", delivery.get("nextPendingIdentity") == NEXT and delivery.get("nextBlockerIds") == [NEXT_BLOCKER] and delivery.get("nextPendingGroup") == NEXT_GROUP, "Divine Intervention Greater / MR233-B01 is next; Wish follows.")
    seal_rows = delivery.get("sealChecks", [])
    check("director-seal-claims-pass", len(seal_rows) == 87 and all(row.get("passed") is True for row in seal_rows), "Director reports 87/87 seal checks passing.")
    check("top-level-seal-counts", delivery.get("sealCheckCount") == 87 and delivery.get("sealPassed") == 87 and delivery.get("sealFailed") == 0, "Delivery seal counts agree.")

    with ZipFile(ARCHIVE) as z:
        names = z.namelist()
        name_set = set(names)
        check("zip-crc-and-safe-unique-names", z.testzip() is None and len(names) == len(name_set) == 41 and all(safe_name(n) for n in names), f"members={len(names)}")
        external_rows = delivery.get("members", [])
        external_map = {row.get("path"): row for row in external_rows}
        check("external-roster-and-allowlist", len(external_rows) == len(external_map) == 41 and delivery.get("archiveMemberCount") == 41 and delivery.get("payloadMemberCount") == 40 and delivery.get("exactAllowlist") == names == list(external_map), "Exact 41-member roster and order.")
        external_ok = True
        for row in external_rows:
            data = z.read(row["path"])
            external_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("all-external-member-bindings", external_ok, "Every DELIVERY size/SHA/CRC matches its exact ZIP member.")

        root_manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        manifest_rows = root_manifest.get("members", [])
        payload_names = [n for n in names if n != "MEMBER_MANIFEST.json"]
        manifest_ok = root_manifest.get("id") == "IMPRISONMENT-DIRECTOR-RETURN341-MEMBER-MANIFEST" and root_manifest.get("payloadMemberCount") == 40 and root_manifest.get("exactPayloadAllowlist") == payload_names and len(manifest_rows) == 40
        for row in manifest_rows:
            member = row.get("path", "")
            if member not in name_set or member == "MEMBER_MANIFEST.json":
                manifest_ok = False
                continue
            data = z.read(member)
            manifest_ok &= (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("root-manifest-exact-payload", manifest_ok, "The root manifest binds the exact 40 payload members.")

        decision = json.loads(z.read("DIRECTOR_DECISION.json"))
        hold = json.loads(z.read("HOLD_REGISTER.json"))
        queue_status = json.loads(z.read("QUEUE_STATUS.json"))
        coverage = json.loads(z.read("CASE_COVERAGE.json"))
        counts = json.loads(z.read("COUNTS.json"))
        validation = json.loads(z.read("VALIDATION.json"))
        source_rec = json.loads(z.read("SOURCE_RECONCILIATION.json"))
        check("sealed-director-decision", decision.get("id") == "IMPRISONMENT-DIRECTOR-RETURN341" and decision.get("decision") == "HOLD" and decision.get("targetIds") == [SPELL] and decision.get("heldIds") == [SPELL] and decision.get("acceptedIds") == [] and decision.get("appliedIds") == [] and decision.get("applicationAuthorized") is False and decision.get("canonicalMutation") is False, "One identity held; no application/canonical mutation.")
        per_identity = decision.get("perIdentity", [])
        check("decision-blocker-and-open-contracts", len(per_identity) == 1 and per_identity[0].get("id") == SPELL and per_identity[0].get("decision") == "HOLD" and per_identity[0].get("blockerIds") == [BLOCKER] and per_identity[0].get("openContractAndWitnessIds") == ["PC341-W01", "PC341-W02", "PC341-W03", "PC341-W04"], "Four explicit Imprisonment contracts remain open.")
        contracts = hold.get("openContractsAndWitnessNeeds", [])
        check("four-open-return341-contracts", hold.get("spellId") == SPELL and hold.get("blockerId") == BLOCKER and hold.get("status") == "OPEN" and [c.get("id") for c in contracts] == ["PC341-W01", "PC341-W02", "PC341-W03", "PC341-W04"] and [c.get("status") for c in contracts] == ["OPEN", "OPEN", "OPEN", "MISSING_AFTER_CONTRACTS"], "Method menu/admission; per-mode lifecycle/rescue; durable settlement; paid-use witnesses.")
        check("no-witness-or-replay-claimed", coverage.get("scope") == SPELL and coverage.get("priorCasesReplayed") is False and coverage.get("priorCasesReaudited") is False and coverage.get("freshCaseCount") == 0 and coverage.get("completePaidUsefulWitnesses") == 0 and counts.get("completePaidUsefulWitnesses") == 0 and counts.get("freshCases") == 0 and counts.get("freshEvents") == 0, "No paid witness or case replay claimed.")
        pending_before = load(A / "CURRENT25_PENDING_IDENTITY_AUDIT_340.json").get("pendingIds", [])
        check("queue-authority-next-priority-and-pending", queue_status.get("authority") == AUTHORITY and queue_status.get("pendingCount") == 25 and set(queue_status.get("allPendingIdsUnchanged", [])) == set(pending_before) and len(pending_before) == 25 and queue_status.get("nextPendingIdentity") == NEXT and queue_status.get("nextBlockerIds") == [NEXT_BLOCKER] and queue_status.get("nextPendingGroup") == NEXT_GROUP and queue_status.get("closureTasksRemaining") == 25 and queue_status.get("firstReviewTasksRemaining") == 0, "25 pending identities unchanged; Director next priority exact.")
        vchecks = validation.get("checks", [])
        check("reported-validation-record", validation.get("status") == "PASS_INTEGRITY_AND_SOURCE_DATA_WITH_SEMANTIC_HOLD" and len(vchecks) == 133 and all(c.get("passed") is True for c in vchecks), "Director reports 133/133 source/data checks passing; semantic status remains HOLD.")
        check("source-binding-roster", source_rec.get("scope") == SPELL and source_rec.get("currentFullSourceCount") == 12 and len(source_rec.get("currentBindings", [])) == 12 and source_rec.get("historicalStatusListsNotCurrentAuthority") is True, "12 current source bindings are declared; historical authority is not substituted.")

        submitted_zip = decision.get("inputPacket", {})
        submitted_delivery = decision.get("inputDelivery", {})
        check("submitted-review341-packet-binding", submitted_zip.get("fileName") == PREP_ZIP.name and (submitted_zip.get("bytes"), submitted_zip.get("sha256"), submitted_zip.get("crc32")) == (PREP_ZIP.stat().st_size, sha(PREP_ZIP.read_bytes()), crc(PREP_ZIP.read_bytes())), "Return decision binds the exact pushed Review341 ZIP.")
        check("submitted-review341-delivery-binding", submitted_delivery.get("fileName") == PREP_DELIVERY.name and (submitted_delivery.get("bytes"), submitted_delivery.get("sha256"), submitted_delivery.get("crc32")) == (PREP_DELIVERY.stat().st_size, sha(PREP_DELIVERY.read_bytes()), crc(PREP_DELIVERY.read_bytes())) and z.read("evidence/Review341_DELIVERY.json") == PREP_DELIVERY.read_bytes(), "Embedded Review341 DELIVERY exactly matches the one sent.")
        sources_ok = True
        with ZipFile(PREP_ZIP) as sent:
            for row in source_rec.get("currentBindings", []):
                live = ROOT / row["path"]
                data = live.read_bytes() if live.is_file() else b""
                returned_member = "evidence/packet/" + row["packetMember"]
                sent_member = "packet/" + row["packetMember"]
                sources_ok &= live.is_file() and data == z.read(returned_member) == sent.read(sent_member) and (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("12-live-source-and-sent-packet-bindings", sources_ok, "All 12 live source files match the returned and submitted packet members.")
        packet_manifest = json.loads(z.read("evidence/packet/MEMBER_MANIFEST.json"))
        packet_rows = packet_manifest.get("members", [])
        packet_names = {n[len("evidence/packet/"):] for n in names if n.startswith("evidence/packet/") and not n.endswith("/MEMBER_MANIFEST.json")}
        packet_ok = len(packet_rows) == packet_manifest.get("payloadMemberCount") and {r.get("path") for r in packet_rows} == packet_names
        for row in packet_rows:
            member = "evidence/packet/" + row.get("path", "")
            data = z.read(member) if member in name_set else b""
            packet_ok &= member in name_set and (len(data), sha(data), crc(data)) == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
        check("nested-review341-packet-manifest", packet_ok, f"The nested manifest binds {len(packet_rows)} exact packet members.")

        preserved = queue_status.get("preservedHolds", {})
        preserved_ok = preserved.get("closedEvidenceFinding") == "AFP211-E01 CLOSED" and preserved.get("astralProjectionReturn340", {}).get("heldIds") == ["astral-projection"] and preserved.get("return232HistoricalTargets") == ["astral-projection", "imprisonment"] and preserved.get("scope", "").startswith("Only Imprisonment")
        check("prior-holds-and-return232-preserved", preserved_ok, "Return336-340 holds and the Return232 history are preserved without Astral re-adjudication.")

    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return341 independent verification failed: " + json.dumps([c for c in checks if not c["passed"]]))

    with ZipFile(ARCHIVE) as z:
        for name in sorted(n for n in z.namelist() if n != "MEMBER_MANIFEST.json"):
            dst = PAYLOAD.joinpath(*PurePosixPath(name).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(z.read(name))

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref = bind(ARCHIVE), bind(DELIVERY)
    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    hold_path = PAYLOAD / "HOLD_REGISTER.json"
    audit = {
        "id": "IMPRISONMENT-RETURN341-INDEPENDENT-AUDIT",
        "recordedAtUtc": timestamp,
        "status": "PASS_RETURN341_SEALED_HOLD_PC232_B02",
        "archive": archive_ref,
        "delivery": delivery_ref,
        "archiveMemberCount": 41,
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": sum(not row["passed"] for row in checks),
        "decision": "HOLD",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationAuthorizedIds": [],
        "authority": AUTHORITY,
        "openContractIds": ["PC341-W01", "PC341-W02", "PC341-W03", "PC341-W04"],
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(AUDIT, audit)
    receipt = {
        "id": "IMPRISONMENT-RETURN341-RECEIPT",
        "recordedAtUtc": timestamp,
        "decision": "HOLD",
        "blockerIds": [BLOCKER],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "holdRegister": bind(hold_path),
        "independentAudit": bind(AUDIT),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationAuthorizedIds": [],
        "openContractIds": audit["openContractIds"],
        "authority": AUTHORITY,
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "nextGroup": NEXT_GROUP,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(RECEIPT, receipt)

    previous_queue = load(A / "CURRENT_SPELL_QUEUE_340.json")
    previous_pending = load(A / "CURRENT25_PENDING_IDENTITY_AUDIT_340.json")
    previous_handoff = load(A / "CURRENT_HANDOFF_340.json")
    retained = sorted(set(previous_queue.get("separatelyRetainedHolds", [])) | set(previous_queue.get("currentReturnHeldIds", [])) | {SPELL})
    audit_ref, receipt_ref = bind(AUDIT), bind(RECEIPT)
    decision_ref = bind(decision_path)

    queue = dict(previous_queue)
    queue.update({
        "id": "SPELL-REVIEW-QUEUE-341",
        "recordedAtUtc": timestamp,
        "supersedesQueue": bind(A / "CURRENT_SPELL_QUEUE_340.json"),
        "currentAuthority": AUTHORITY,
        "pendingCount": 25,
        "acceptedUnapplied": 0,
        "closureTasksRemaining": 25,
        "firstReviewTasksRemaining": 0,
        "nextGroup": NEXT_GROUP,
        "next": NEXT,
        "nextPendingIds": [NEXT],
        "nextPendingCount": 1,
        "heldThisStep": [SPELL],
        "separatelyRetainedHolds": retained,
        "pendingIdentityAudit": PENDING.relative_to(ROOT).as_posix(),
        "currentHandoff": HANDOFF.relative_to(ROOT).as_posix(),
        "currentPacket": None,
        "currentPacketStatus": "RETURN341_IMPRISONMENT_HELD_DIVINE_INTERVENTION_GREATER_MR233_B01_NEXT",
        "activeReview": {"spellId": NEXT, "blockerIds": [NEXT_BLOCKER], "packet": None, "status": "DIRECTOR_RETURN341_NEXT_PRIORITY"},
        "currentReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnAcceptedIds": [],
        "currentReturnAppliedIds": [],
        "currentReturnHeldIds": [SPELL],
        "currentReturnBlockers": {**previous_queue.get("currentReturnBlockers", {}), SPELL: [BLOCKER]},
        "currentDirectorInstruction": "Return341 holds Imprisonment / PC232-B02. PC341-W01 authorized finite entombment method menu and admission/geometry; W02 per-method persistent lifecycle, agency, needs, escape/rescue; W03 durable body/gear/source ownership and once-only terminal settlement; W04 complete paid useful positive/adverse encounters remain open. No application is authorized. Return336-340 holds and AFP211-E01 CLOSED remain unchanged. Next Director priority: Divine Intervention Greater / MR233-B01; Wish follows.",
        "directorConnectionStatus": "Return341 independently verified. Imprisonment remains held; next is Divine Intervention Greater / MR233-B01, then Wish.",
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "githubChanges": False,
    })
    save(QUEUE, queue)

    pending = dict(previous_pending)
    pending.update({
        "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-341",
        "recordedAtUtc": timestamp,
        "status": "PASS_CURRENT_823_25_RETURN341_IMPRISONMENT_HOLD_DIVINE_INTERVENTION_GREATER_NEXT",
        "supersedes": (A / "CURRENT25_PENDING_IDENTITY_AUDIT_340.json").name,
        "authority": AUTHORITY,
        "pendingCount": 25,
        "acceptedIds": [],
        "appliedIds": [],
        "heldThisStep": [SPELL],
        "separatelyHeldIds": retained,
        "nextGroup": NEXT_GROUP,
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "nextPendingIds": [NEXT],
        "nextPendingCount": 1,
        "nextStep": "Review Divine Intervention Greater / MR233-B01 from current exact catalog/index/Core sources. Preserve Return336-341 holds and AFP211-E01 closed; apply only an exact sealed acceptance. Wish follows.",
        "sourceQueue": QUEUE.relative_to(ROOT).as_posix(),
        "currentQueueBinding": bind(QUEUE),
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
    save(PENDING, pending)

    handoff = dict(previous_handoff)
    handoff.update({
        "id": "CURRENT-HANDOFF-341",
        "recordedAtUtc": timestamp,
        "supersedes": (A / "CURRENT_HANDOFF_340.json").name,
        "status": "RETURN341_VERIFIED_IMPRISONMENT_HELD_DIVINE_INTERVENTION_GREATER_NEXT_823_25_0",
        "authority": AUTHORITY,
        "queue": QUEUE.relative_to(ROOT).as_posix(),
        "queueBinding": bind(QUEUE),
        "pendingIdentityAudit": PENDING.name,
        "pendingIdentityAuditBinding": bind(PENDING),
        "currentDirectorReturn": receipt_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnAudit": audit_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "heldThisStep": [SPELL],
        "separatelyRetainedHolds": retained,
        "acceptedIds": [],
        "appliedIds": [],
        "applicationPerformed": False,
        "canonicalFilesChanged": False,
        "currentBlocker": {"identity": NEXT, "blockerId": NEXT_BLOCKER, "group": NEXT_GROUP},
        "nextPendingGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT], "pendingCount": 1, "reportedByDirector": True},
        "nextStep": "Review Divine Intervention Greater / MR233-B01 using current exact source bindings; preserve Return336-341 holds and AFP211-E01 closed; apply only an exact sealed acceptance. Wish follows.",
        "directorConnectionStatus": "Return341 sealed Imprisonment HOLD; the Director designates Divine Intervention Greater / MR233-B01 next, with Wish after it.",
    })
    save(HANDOFF, handoff)
    SNAPSHOT.write_text(
        "# Spell review status — queue 341\n\n"
        f"Return341 independently verified {len(checks)}/{len(checks)} checks and holds Imprisonment / PC232-B02. "
        "Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "Four contracts remain open: authorize at least two useful entombment methods with exact admission and geometry; define per-method lifecycle, agency, needs and lawful escape/rescue; settle durability, suppression, growth, death/corpse/gear and once-only competing ownership; and demonstrate complete paid useful positive/adverse encounters. Return336-340 holds and AFP211-E01 CLOSED remain unchanged; no application is authorized.\n\n"
        "Next Director-prioritized identity: **Divine Intervention Greater / MR233-B01**, then **Wish**.\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"status":"PASS", "checks":len(checks), "passed":sum(r["passed"] for r in checks), "failed":sum(not r["passed"] for r in checks), "archiveMembers":41, "held":SPELL, "authority":AUTHORITY, "next":NEXT, "receipt":str(RECEIPT)}, indent=2))


if __name__ == "__main__":
    main()
