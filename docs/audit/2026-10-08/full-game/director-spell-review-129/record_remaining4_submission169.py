from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
GROUP = "rank8-remaining4"
IDS = ["prismatic-wall", "faction-convergence", "divine-intervention-lesser", "reality-patch"]
CHAT_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
BRANCH = "codex/ordinary-spell-review-complete"
ARCHIVE = FULL / "DD_Rank8_Remaining_4_Source_Conference_02.zip"
REQUEST = FULL / "RANK8_REMAINING_4_SOURCE_CONFERENCE_02_REQUEST.txt"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_remaining_4_source_conference_02.json"
VERIFY = AUDIT / "RANK8_REMAINING_4_SOURCE_CONFERENCE_02_VERIFICATION_168.json"
OLD_QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_168.json"
OLD_HANDOFF = AUDIT / "CURRENT_HANDOFF_168.json"
RECEIPT = AUDIT / "REMAINING4_GPT_SUBMISSION_169.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_169.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_169.json"
RAW_URL = f"https://raw.githubusercontent.com/BordelonDevOps/DecenniumDescent/{BRANCH}/docs/audit/2026-10-08/full-game/DD_Rank8_Remaining_4_Source_Conference_02.zip"
MESSAGE = f"""GPT — please review the exact fresh Rank8 Remaining4 Conference02 packet attached and published on the current branch.

ZIP: {RAW_URL}
Size: 26,416,138 bytes
SHA-256: 42de110748cc76cb52f790c6cd719f5d8db7676cde6d6cd900f0e926610fbf90
Branch: https://github.com/BordelonDevOps/DecenniumDescent/tree/{BRANCH}

Use current authority 735 applied-reviewed / 113 pending / 0 accepted-unapplied; 459 complete standalone procedures. Review only prismatic-wall, faction-convergence, divine-intervention-lesser, and reality-patch. Resolve all 22 preserved source questions. Return complete source-faithful procedures, question dispositions, cases/branches, explicit accepted IDs, retained holds and an independent semantic failure check. Preserve native source/access and previously accepted-interface boundaries; retain all runtime, human-play, balance, cosmology and release qualifications. Do not edit canonical files or reopen any accepted/applied spell cohort or closed feat review. If the exact package passes, state accepted=true and applied=false only for exact accepted IDs; otherwise leave them unaccepted/unapplied and list exact blockers."""


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bind(path: Path):
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> None:
    prep = read(FULL / "RANK8_REMAINING_4_SOURCE_CONFERENCE_02_PREPARATION.json")
    checks = read(FULL / "RANK8_REMAINING_4_SOURCE_CONFERENCE_02_CHECK.json")
    verification = read(VERIFY)
    assert prep.get("status") == "PREPARED_UNSENT"
    assert checks.get("failures") == 0
    assert verification.get("status") == "PASS" and verification.get("failures") == 0
    assert bind(ARCHIVE) == prep["archive"] and bind(CANDIDATE) == prep["candidate"]
    assert not RECEIPT.exists() and not QUEUE.exists() and not HANDOFF.exists()

    sent_at = datetime.now(timezone.utc).isoformat()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    receipt = {
        "id": "REMAINING4-GPT-SUBMISSION-169",
        "sentAtUtc": sent_at,
        "destination": {"conversationTitle": "Calibration review part 6", "url": CHAT_URL},
        "attachments": [bind(ARCHIVE), bind(REQUEST)],
        "publicRawUrl": RAW_URL,
        "branch": {"name": BRANCH, "commit": commit},
        "message": MESSAGE,
        "messageSha256": hashlib.sha256(MESSAGE.encode("utf-8")).hexdigest(),
        "reviewIds": IDS,
        "authority": {
            "reviewedApplied": 735,
            "pending": 113,
            "acceptedUnapplied": 0,
            "completeReviewedStandaloneProcedures": 459,
            "scopedInterfaces": 173,
        },
        "independentPacketVerification": bind(VERIFY),
        "submissionStateObserved": "Both exact attachments were visible in the GPT composer; the message was sent and the conversation displayed Working / responding. No director decision received yet.",
    }
    write(RECEIPT, receipt)

    queue = read(OLD_QUEUE)
    queue["id"] = "SPELL-REVIEW-QUEUE-169"
    queue["recordedAtUtc"] = sent_at
    queue["packetStatus"] = "REMAINING4_SUBMITTED_AWAITING_DIRECTOR_RETURN"
    current = next(g for g in queue["currentPendingGroups"] if g["group"] == GROUP)
    current["status"] = "SUBMITTED_AWAITING_DIRECTOR_RETURN"
    current["submissionReceipt"] = bind(RECEIPT)
    queue["next"]["status"] = "SUBMITTED_AWAITING_DIRECTOR_RETURN"
    queue["sourceConferencePrepared"]["status"] = "submitted-awaiting-director-return"
    queue["sourceConferencePrepared"]["submissionReceipt"] = bind(RECEIPT)
    queue["nextPreparedRequest"] = queue["sourceConferencePrepared"]
    queue["directorSubmission"] = {
        "status": "submitted-awaiting-director-return",
        "conversation": CHAT_URL,
        "receipt": bind(RECEIPT),
        "archive": bind(ARCHIVE),
        "reviewIds": IDS,
    }
    queue["currentSubmission"] = bind(RECEIPT)
    write(QUEUE, queue)

    handoff = read(OLD_HANDOFF)
    handoff["id"] = "CURRENT-HANDOFF-169"
    handoff["recordedAtUtc"] = sent_at
    handoff["status"] = "REMAINING4_SUBMITTED_AWAITING_DIRECTOR_RETURN"
    handoff["currentQueueBinding"] = bind(QUEUE)
    handoff["currentSubmissionBinding"] = bind(RECEIPT)
    submitted = {
        "status": "submitted-awaiting-director-return",
        "conversation": CHAT_URL,
        "receipt": bind(RECEIPT),
        "archive": bind(ARCHIVE),
        "candidate": bind(CANDIDATE),
        "reviewIds": IDS,
    }
    handoff["nextPreparedRequest"] = submitted
    handoff["directorSubmission"] = submitted
    write(HANDOFF, handoff)
    print(json.dumps({"receipt": bind(RECEIPT), "queue": bind(QUEUE), "handoff": bind(HANDOFF)}, indent=2))


if __name__ == "__main__":
    main()
