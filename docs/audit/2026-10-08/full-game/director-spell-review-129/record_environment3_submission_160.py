from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
REVIEW = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates"
QUEUE_IN = AUDIT / "CURRENT_SPELL_QUEUE_159.json"
HANDOFF_IN = AUDIT / "CURRENT_HANDOFF_159.json"
QUEUE_OUT = AUDIT / "CURRENT_SPELL_QUEUE_160.json"
HANDOFF_OUT = AUDIT / "CURRENT_HANDOFF_160.json"
SUBMISSION = AUDIT / "RANK8_ENVIRONMENT3_SUBMISSION_160.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_environment_3_source_conference_02.json"
ARCHIVE = FULL / "DD_Rank8_Environment_3_Source_Conference_02.zip"
REQUEST = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_REQUEST.txt"
CHECK = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_PREPARATION.json"
INDEPENDENT = AUDIT / "RANK8_ENVIRONMENT3_SOURCE_CONFERENCE02_INDEPENDENT_VERIFICATION_159.json"
EXPECTED_ARCHIVE_SHA = "4d81358a29f0d6dc0e123883dd02044c794e84b02d6cc1f87e5e8942605d56e1"
EXPECTED_REQUEST_SHA = "5c0ff66885e3bd65d379490d43a586583b285e5f31383b25ea68815bb97424f3"
SUBMITTED_MESSAGE_SHA = "963cabe4184285192475a4871d40e614a9eeeedb885209ec4c47fa7bda4828c8"
BRANCH = "codex/ordinary-spell-review-complete"
BRANCH_COMMIT = "349b640b62153af2bddc7342caff9d424c7d5652"
CONVERSATION_ID = "6adc506d-8770-83ea-b64c-0345d9b9b682"
SUBMITTED_AT = "2026-10-25T21:19:21Z"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    assert not any(p.exists() for p in [QUEUE_OUT, HANDOFF_OUT, SUBMISSION])
    queue = read(QUEUE_IN)
    handoff = read(HANDOFF_IN)
    candidate, archive, request = binding(CANDIDATE), binding(ARCHIVE), binding(REQUEST)
    check, preparation, independent = binding(CHECK), binding(PREPARATION), binding(INDEPENDENT)
    assert archive["sha256"] == EXPECTED_ARCHIVE_SHA
    assert request["sha256"] == EXPECTED_REQUEST_SHA
    assert queue["currentAuthority"]["reviewedApplied"] == 723 and queue["currentAuthority"]["pending"] == 125
    assert handoff["currentAuthority"] == queue["currentAuthority"]
    assert queue["currentPendingGroups"][0]["group"] == "rank8-environment3"
    assert queue["currentPendingGroups"][0]["candidate"] == candidate
    assert queue["currentPendingGroups"][0]["archive"] == archive
    assert read(INDEPENDENT)["status"] == "PASS" and read(INDEPENDENT)["failures"] == 0

    submission = {
        "id": "RANK8-ENVIRONMENT3-SUBMISSION-160",
        "submittedAtUtc": SUBMITTED_AT,
        "status": "SUBMITTED_AWAITING_DIRECTOR_RETURN",
        "director": "GPT Calibration review part6",
        "conversationId": CONVERSATION_ID,
        "userVisibleStateAfterSend": "ChatGPT is responding; working indicator visible in the target conversation.",
        "branch": BRANCH,
        "branchCommit": BRANCH_COMMIT,
        "candidate": candidate,
        "archive": archive,
        "request": request,
        "preparation": preparation,
        "sourceCheck": check,
        "independentVerification": independent,
        "submittedMessageSha256": SUBMITTED_MESSAGE_SHA,
        "attachments": [ARCHIVE.name, REQUEST.name],
        "targetIds": ["absolute-silence", "control-weather", "earthquake"],
        "authority": {"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0},
        "acceptanceScope": "Static authored review only. Apply only exact identities explicitly accepted after independent verification.",
        "canonicalEditsMadeBySubmission": False,
    }
    write(SUBMISSION, submission)

    queue.update({
        "id": "SPELL-REVIEW-QUEUE-160",
        "packetStatus": "RANK8_ENVIRONMENT3_PACKET02_SUBMITTED_AWAITING_DIRECTOR_RETURN_723_125",
        "directorSubmission": {
            "record": SUBMISSION.relative_to(ROOT).as_posix(),
            "status": submission["status"],
            "conversationId": CONVERSATION_ID,
            "submittedAtUtc": SUBMITTED_AT,
            "messageSha256": SUBMITTED_MESSAGE_SHA,
        },
        "recordedAtUtc": SUBMITTED_AT,
    })
    queue["currentPendingGroups"][0]["submission"] = binding(SUBMISSION)
    queue["currentPendingGroups"][0]["status"] = "SUBMITTED_AWAITING_DIRECTOR_RETURN"
    write(QUEUE_OUT, queue)

    handoff.update({
        "id": "CURRENT-HANDOFF-160",
        "recordedAtUtc": SUBMITTED_AT,
        "status": "RANK8_ENVIRONMENT3_PACKET02_SUBMITTED_AWAITING_DIRECTOR_RETURN_723_125",
        "currentQueueBinding": binding(QUEUE_OUT),
        "directorSubmission": {
            "record": SUBMISSION.relative_to(ROOT).as_posix(),
            "status": submission["status"],
            "conversationId": CONVERSATION_ID,
            "submittedAtUtc": SUBMITTED_AT,
            "messageSha256": SUBMITTED_MESSAGE_SHA,
        },
        "nextGroup": "rank8-environment3",
        "nextPreparedRequest": {
            "group": "rank8-environment3",
            "candidate": candidate,
            "archive": archive,
            "preparation": preparation,
            "request": request,
            "submission": binding(SUBMISSION),
            "status": "submitted-awaiting-director-return",
        },
        "resumePriority": "Wait for GPT's exact Environment3 return, download and bind its archive and delivery record, independently audit every decision/procedure/case/operation, apply only exact accepted IDs, and continue until current pending reaches zero.",
    })
    write(HANDOFF_OUT, handoff)
    print(json.dumps({
        "status": submission["status"],
        "submission": binding(SUBMISSION),
        "queue": binding(QUEUE_OUT),
        "handoff": binding(HANDOFF_OUT),
        "branchCommit": BRANCH_COMMIT,
        "messageSha256": SUBMITTED_MESSAGE_SHA,
    }, indent=2))


if __name__ == "__main__":
    main()
