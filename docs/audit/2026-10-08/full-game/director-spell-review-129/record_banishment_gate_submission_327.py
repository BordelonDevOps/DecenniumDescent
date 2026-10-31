from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
OUT = AUDIT / "rank9_banishment_gate_current_source_327_prepared"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(path: pathlib.Path):
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: pathlib.Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive = OUT / "DD_Rank9_BanishmentGate_CurrentSource_327.zip"
    delivery = OUT / "DD_Rank9_BanishmentGate_CurrentSource_327_DELIVERY.json"
    packet_audit = AUDIT / "BANISHMENT_GATE_PACKET_327_INDEPENDENT_AUDIT.json"
    message = (
        "Director: Packet327 is attached. Review only Banishment Gate / PG200-B03 and PG200-B04 as directed by Return326, at current 823/25/0 authority. "
        "The packet preserves Return200’s sealed blockers, procedure and nine cases, and adds the current AC5 accepted/applied source: Faction Champion is explicitly a Humanoid targeting profile with a Wizard source route, but requires alliedStatus, positive standing, invocation permission and no aid ban. "
        "Decide whether that closes B03 as the nonmatching control without treating its conditional fixture as a campaign fact. For B04, reassess the touch-only, stationary type-change and already-claimed guard branches, plus living separate-body carriage, primary independent escape, dead-primary/corpse handling, and finite-summon expiry with genuine cargo. "
        "Distinguish accepted source-backed transitions from rule-only fixtures. If complete, issue a sealed Banishment Gate-only acceptance with exact bindings and application disposition. Otherwise seal a hold with each remaining blocker, minimum witness, any narrow subparts closed, and next identity. "
        "No acceptance/application is requested by this packet. Preserve unrelated decisions and all downstream gates."
    )
    submission = {
        "id": "BANISHMENT-GATE-PACKET327-SUBMISSION-RECEIPT",
        "recordedAtUtc": now,
        "destination": "ChatGPT Director conversation: Calibration review part 6",
        "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682",
        "status": "SENT_DIRECTOR_RESPONSE_PENDING",
        "submissionMethod": "User-authorized browser upload and message",
        "scopeIds": ["banishment-gate"],
        "blockerIds": ["PG200-B03", "PG200-B04"],
        "archive": bind(archive),
        "delivery": bind(delivery),
        "independentAudit": bind(packet_audit),
        "message": message,
        "messageSha256": sha(message.encode("utf-8")),
        "authority": {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
    }
    receipt = AUDIT / "BANISHMENT_GATE_PACKET_327_SUBMISSION_RECEIPT.json"
    save(receipt, submission)

    q0 = read(AUDIT / "CURRENT_SPELL_QUEUE_327.json")
    p0 = read(AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_327.json")
    h0 = read(AUDIT / "CURRENT_HANDOFF_327.json")
    q = copy.deepcopy(q0)
    q.update({
        "recordedAtUtc": now,
        "activeReview": {"spellId": "banishment-gate", "blockerIds": ["PG200-B03", "PG200-B04"], "packet": {"archive": bind(archive), "delivery": bind(delivery), "independentAudit": bind(packet_audit)}, "status": "PACKET327_SUBMITTED_TO_DIRECTOR_RESPONSE_PENDING"},
        "currentPacket": {"archive": bind(archive), "delivery": bind(delivery), "independentAudit": bind(packet_audit)},
        "currentSourcePacket": bind(archive),
        "currentPreparation": bind(delivery),
        "currentSubmission": bind(receipt),
        "submissionReceipt": bind(receipt),
        "currentPacketStatus": "PACKET327_BANISHMENT_GATE_SUBMITTED_DIRECTOR_RESPONSE_PENDING",
        "directorConnectionStatus": "Packet327 for Banishment Gate/PG200-B03 and PG200-B04 was uploaded; sealed response pending. It includes the current accepted/applied AC5 Faction Champion Humanoid profile and route, with conditional-fixture limits explicit. Preserve FOS/KR198-B01, EProp/TF192-B02, Collapse Timeline/TF192-B05 and Fate Rewrite/TF192-B04.",
        "currentDirectorInstruction": bind(receipt),
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "githubChanges": False,
        "acceptedThisStep": [],
        "appliedThisStep": [],
        "currentPacketReadbackAudit": bind(packet_audit),
    })
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_327.json"
    save(queue_path, q)

    p = copy.deepcopy(p0)
    p.update({
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_823_25_BANISHMENT_GATE_PACKET327_SUBMITTED",
        "sourceQueue": queue_path.relative_to(ROOT).as_posix(),
        "currentQueueBinding": bind(queue_path),
        "currentPacketSubmission": bind(receipt),
        "currentPacketReadbackAudit": bind(packet_audit),
        "nextStep": "Await sealed Director disposition for Banishment Gate / PG200-B03 and PG200-B04. Determine if the accepted AC5 Faction Champion Humanoid profile and authored route close any witness part; preserve conditional fixtures as non-campaign facts and retain unresolved lifecycle gaps.",
        "canonicalFilesChanged": False,
        "acceptedIds": [],
        "appliedIds": [],
    })
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_327.json"
    save(pending_path, p)

    h = copy.deepcopy(h0)
    h.update({
        "recordedAtUtc": now,
        "status": "PACKET327_BANISHMENT_GATE_SUBMITTED_AWAITING_DIRECTOR",
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "queueBinding": bind(queue_path),
        "pendingIdentityAudit": pending_path.relative_to(ROOT).as_posix(),
        "pendingIdentityAuditBinding": bind(pending_path),
        "currentSubmission": bind(receipt),
        "currentReadbackAudit": bind(packet_audit),
        "nextStep": "Await Director response to Packet327. Reassess whether current accepted Faction Champion/Humanoid source evidence closes PG200-B03 and whether any Banishment Gate lifecycle branches close PG200-B04.",
        "currentPacketStatus": "PACKET327_BANISHMENT_GATE_SUBMITTED_DIRECTOR_RESPONSE_PENDING",
        "directorConnectionStatus": "Packet327 uploaded and sent. Awaiting a sealed Banishment Gate-only decision; no acceptance or application requested.",
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
        "runtimeExecuted": False,
    })
    handoff_path = AUDIT / "CURRENT_HANDOFF_327.json"
    save(handoff_path, h)
    snapshot = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_327.md"
    snapshot.write_text(
        f"# Current spell-review snapshot — Packet327 submitted\n\nRecorded: {now}\n\n"
        "Authority remains **823 applied / 25 pending / 0 accepted-unapplied**, with **547 complete procedures / 173 scoped interfaces**. "
        "The Director is reviewing Banishment Gate / PG200-B03 and PG200-B04 only. Packet327 includes Return200's exact blocker records and nine cases, current authority/queue, and the accepted/applied AC5 Faction Champion Humanoid profile and source route. The profile's allied-faction conditions and conditional-fixture limits are explicit.\n\n"
        "No acceptance, application, canonical edit or runtime execution is recorded. The next identity after this review is Conjure Demiplane Fortress / PG200-B06. Closure tasks remain 25; first-review tasks remain zero.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"submission": bind(receipt), "queue": bind(queue_path), "pendingAudit": bind(pending_path), "handoff": bind(handoff_path), "status": q["currentPacketStatus"], "authority": q["currentAuthority"]}, indent=2))


if __name__ == "__main__":
    main()
