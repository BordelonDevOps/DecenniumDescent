from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUD = FULL / "director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUD / "CURRENT_SPELL_QUEUE_171.json"
HANDOFF_BEFORE = AUD / "CURRENT_HANDOFF_171.json"
PENDING = AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_171.json"
ARCHIVE = FULL / "DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_02.json"
REQUEST = FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_REQUEST_171.txt"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
RAW_URL = "https://raw.githubusercontent.com/BordelonDevOps/DecenniumDescent/codex/ordinary-spell-review-complete/docs/audit/2026-10-08/full-game/DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
BRANCH = "codex/ordinary-spell-review-complete"
COMMIT = "ecf760fee6a8f4e2fcd711086c7c45fcec215e7b"
IDS = ["cataclysmic-conjuration", "elemental-apocalypse", "planar-overload", "armageddon", "cataclysm", "arcane-apocalypse", "meteor-swarm", "starfire-core", "ragnarok", "final-spark"]
MESSAGE = f"""GPT — review the attached fresh Rank9 Catastrophe10 Conference02 packet against the current GitHub branch.

ZIP: {RAW_URL}
Size: 11,511,997 bytes
SHA-256: c0d1558b63f5fa2161ffaa7fc129fd2fc4dc148b238d7dfe06125661389d6e1f
Branch commit: {COMMIT}

Current authority is 739 applied-reviewed / 109 pending / 0 accepted-unapplied, with 463 complete standalone procedures. Review exactly {', '.join(IDS)}. Resolve all 25 preserved source questions. Return complete source-faithful procedures, selected dispositions, full cases/branches with reversible event/state evidence, exact accepted IDs and blockers, retained holds, and your independent semantic failure check. Preserve current native source/access and accepted-interface boundaries. Keep runtime, human-play, balance, cosmology, domain-closure and release qualifications explicit. Do not edit canonical files, reopen any previously applied spell cohort, or reopen the closed feat review. If the packet passes, state accepted=true and applied=false only for the exact accepted IDs."""


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(data: bytes):
    return hashlib.sha256(data).hexdigest()


def bind(path: Path, rel: str | None = None):
    data = path.read_bytes()
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def write_json(path: Path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def main():
    now = datetime.now(timezone.utc).isoformat()
    queue0, handoff0 = read(QUEUE_BEFORE), read(HANDOFF_BEFORE)
    index_bytes, catalog_bytes = INDEX.read_bytes(), CATALOG.read_bytes()
    prep = read(FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_PREPARATION_171.json")
    verification = read(FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_VERIFICATION_171.json")
    assert queue0["packetStatus"] == "RANK9_CATASTROPHE10_FRESH_PACKET_PREPARED_UNSENT"
    assert handoff0["status"] == "RANK9_CATASTROPHE10_FRESH_PACKET_PREPARED_UNSENT"
    assert verification["status"] == "PASS" and verification["checksFailed"] == 0
    assert prep["currentAuthority"] == {"reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173}
    assert bind(ARCHIVE)["sha256"] == prep["archive"]["sha256"] == "c0d1558b63f5fa2161ffaa7fc129fd2fc4dc148b238d7dfe06125661389d6e1f"
    assert bind(CANDIDATE)["sha256"] == prep["candidate"]["sha256"]
    assert read(PENDING)["pendingCount"] == 109 and all(sid in read(PENDING)["pendingIds"] for sid in IDS)
    assert read(INDEX)["authoredCounts"] == {"reviewed": 739, "pending": 109}

    msg_path = FULL / "RANK9_CATASTROPHE10_DIRECTOR_SUBMISSION_172.txt"
    msg_bytes = MESSAGE.encode("utf-8")
    msg_path.write_bytes(msg_bytes)
    receipt_path = AUD / "RANK9_CATASTROPHE10_GPT_SUBMISSION_172.json"
    receipt = {
        "id": "RANK9-CATASTROPHE10-GPT-SUBMISSION-172",
        "sentAtUtc": now,
        "status": "FRESH_PACKET_SUBMITTED_AWAITING_DIRECTOR_RETURN",
        "destination": {"conversationTitle": "Calibration review part 6", "url": URL},
        "attachments": [bind(ARCHIVE), bind(REQUEST)],
        "publicRawUrl": RAW_URL,
        "branch": {"name": BRANCH, "commit": COMMIT, "url": f"https://github.com/BordelonDevOps/DecenniumDescent/tree/{BRANCH}"},
        "message": {"path": msg_path.relative_to(ROOT).as_posix(), "bytes": len(msg_bytes), "sha256": sha(msg_bytes)},
        "reviewIds": IDS,
        "authority": prep["currentAuthority"],
        "independentPacketVerification": bind(FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_VERIFICATION_171.json"),
        "submissionStateObserved": "Both exact attachments appeared in the GPT composer and the message was sent; the conversation displayed Working / responding.",
    }
    write_json(receipt_path, receipt)

    pending = read(PENDING)
    queue = copy.deepcopy(queue0)
    queue.update({"id": "SPELL-REVIEW-QUEUE-172", "recordedAtUtc": now, "packetStatus": "RANK9_CATASTROPHE10_SUBMITTED_AWAITING_DIRECTOR_RETURN", "directorSubmission": {"status": "submitted-awaiting-return", "conversation": URL, "receipt": bind(receipt_path), "reviewIds": IDS, "archive": bind(ARCHIVE)}, "currentSubmissionBinding": bind(receipt_path)})
    queue["currentPendingGroups"][0].update({"status": "SUBMITTED_AWAITING_DIRECTOR_RETURN", "freshPacketRequiredForCurrentAuthority": False, "submissionReceipt": bind(receipt_path)})
    queue["next"] = {"group": "rank9-catastrophe10", "pendingCount": 10, "candidate": bind(CANDIDATE), "archive": bind(ARCHIVE), "freshPacketRequiredForCurrentAuthority": False, "status": "SUBMITTED_AWAITING_DIRECTOR_RETURN", "submissionReceipt": bind(receipt_path)}
    queue_path = AUD / "CURRENT_SPELL_QUEUE_172.json"
    write_json(queue_path, queue)

    handoff = copy.deepcopy(handoff0)
    handoff.update({"id": "CURRENT-HANDOFF-172", "recordedAtUtc": now, "status": "RANK9_CATASTROPHE10_SUBMITTED_AWAITING_DIRECTOR_RETURN", "currentIndexBinding": bind(INDEX, "authority/authored_review_index.json"), "currentCatalogBinding": bind(CATALOG, "authority/catalog.json"), "currentQueueBinding": bind(queue_path), "pendingIdentityAudit": {"id": pending["id"], "path": PENDING.name, "pendingCount": 109, "sha256": sha(PENDING.read_bytes())}, "nextGroup": "rank9-catastrophe10", "currentSubmissionBinding": bind(receipt_path), "directorSubmission": {"status": "submitted-awaiting-return", "conversation": URL, "receipt": bind(receipt_path), "archive": bind(ARCHIVE), "candidate": bind(CANDIDATE), "reviewIds": IDS}, "resumePriority": "Check the same GPT director for the exact Rank9 Catastrophe10 return, independently audit its data and semantics, apply only the exact accepted identities, push that batch, and continue until pending reaches zero."})
    handoff_path = AUD / "CURRENT_HANDOFF_172.json"
    write_json(handoff_path, handoff)

    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig")
    marker = "**Prior checkpoint: ["
    at = old_start.find(marker)
    history = old_start[at:] if at >= 0 else ""
    start.write_text(
        "# Decennium Descent — start here\n\n"
        "**Current ordinary spell-review checkpoint [172](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_172.json):** Rank8 Remaining4 is applied at **739 reviewed / 109 pending / 0 accepted-unapplied**. The fresh Rank9 Catastrophe10 Conference02 packet was independently verified against current authority and sent to GPT with both packet and request attached. It is awaiting the director’s return.\n\n"
        "The packet covers exactly ten Catastrophe spells, preserves 25 unselected source questions, and binds 86 current sources. Closed feats and applied spell cohorts remain closed. Runtime, human-play, balance, cosmology, and release approval remain separate. Continue the director review, apply only accepted IDs, push each batch, and continue until pending reaches zero.\n\n"
        f"See [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/{handoff_path.name}), [current queue](docs/audit/2026-10-08/full-game/director-spell-review-129/{queue_path.name}), [submission receipt](docs/audit/2026-10-08/full-game/director-spell-review-129/{receipt_path.name}), [packet](docs/audit/2026-10-08/full-game/DD_Rank9_Catastrophe_10_Source_Conference_02.zip), and [verification](docs/audit/2026-10-08/full-game/RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_VERIFICATION_171.json).\n\n"
        + history,
        encoding="utf-8", newline="\n",
    )
    (ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_172.md").write_text(
        "# Ordinary spell review snapshot — Rank9 Catastrophe10 submitted\n\n"
        "Current authority is **739 reviewed / 109 pending / 0 accepted-unapplied** with 463 complete standalone procedures. Rank8 Remaining4’s exact four IDs have been applied and pushed. The next ten Rank9 Catastrophe IDs were packaged in a fresh 739/109 Conference02 source packet, independently verified across 15 checks and 86 current source bindings, pushed to GitHub, and sent to the GPT director with the request file. GPT is now responding.\n\n"
        "No Catastrophe decision or application has been made yet. Continue from [current handoff](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_172.json), [submission receipt](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CATASTROPHE10_GPT_SUBMISSION_172.json), and [packet verification](docs/audit/2026-10-08/full-game/RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_VERIFICATION_171.json). Preserve all source, content, lifecycle, runtime, playtest, balance, cosmology, and release holds. Continue until pending reaches zero.\n",
        encoding="utf-8", newline="\n",
    )
    assert INDEX.read_bytes() == index_bytes and CATALOG.read_bytes() == catalog_bytes
    print(json.dumps({"status": "SUBMISSION_RECORDED", "receipt": bind(receipt_path), "queue": bind(queue_path), "handoff": bind(handoff_path), "authority": prep["currentAuthority"], "reviewIds": IDS}, indent=2))


if __name__ == "__main__":
    main()
