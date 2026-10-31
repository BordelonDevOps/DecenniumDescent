from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def info(path: Path):
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def main():
    reconciliation_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249.json"
    reconciliation_receipt_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_RECEIPT.json"
    request_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_REQUEST.txt"
    reconciliation, receipt = read(reconciliation_path), read(reconciliation_receipt_path)
    assert reconciliation["status"] == receipt["status"] == "PASS"
    assert reconciliation["reviewedUniqueIdentityCount"] == reconciliation["pendingCount"] == 37
    assert reconciliation["acceptedIds"] == reconciliation["appliedIds"] == reconciliation["unreviewedCurrentPendingIds"] == []
    assert reconciliation["staleReturn248NextPointer"]["confirmedStale"] is True

    now = datetime.now(timezone.utc).isoformat()
    conference = BASE / "CURRENT_SPELL_REVIEW_CONFERENCE_249.md"
    conference.write_text(
        "# Final Pending Spell Review Conference 249\n\n"
        "GPT reconciled the Returns232–248 chain and confirmed all **37 current pending identities have completed sealed reviews exactly once**. All 17 return audits pass; all 37 remain held, with zero accepted and zero applied. There is no unreviewed pending identity. Return248’s pointer to Projection/Confinement was stale because that group was already held in Return232 and Miracle/Reality was held in Return233.\n\n"
        "**Recommended first closure task:** Eternal Forge (MF210-B01). Complete an actual weapon-damage then lawful repair witness using acquired Smith-tools proficiency, tools, materials, checks and work clocks. Also complete the charged item’s transfer, dawn, suppression/ending and paid new-creation lifecycle. A finite buyer is needed only if choosing the alternative sale route.\n\n"
        "**Next:** Unravel Identity (MD196-B02). Build one source-legal multiclass acquisition history that integrates class form, maxima, companion, Base/Arch/Hero capabilities, passives and suppression callbacks. Demonstrate recovery without refilling spent resources or reviving ended effects; the class source files are already present.\n\n"
        "**Other concrete witness work:** Soul Reflection needs its changed-form, attached/no-phase recipient, original-target zero/death, copied-concentration and entrusted-cargo branches integrated. Conjure Demiplane Fortress needs its support/damage, work/rest, companion, creator-death and occupied-ending cases, plus any still-missing nested entrance/anchor contract. Banishment Gate needs a lawful non-Elemental acquisition/permission history and its complete crossing/occupied-cell lifecycle.\n\n"
        "**Spell-local contracts or decisions, followed by witnesses:** Alignment Ascension, Alignment Perfection, Faction Incarnate, Corruption Purification, Imprisonment, Astral Projection, Greater Divine Intervention, Wish and Unholy Ascendance. Specify only the missing operation, profile, permission and lifecycle contract identified for each spell; a local spell decision cannot establish an external permission or an existing creature/campaign fact.\n\n"
        "**Shared dependencies:** obtain one real inserted-full-turn provider/acquisition history, then prove each affected spell’s distinct timing behavior; coordinate Time Stop with Timeless Form without circularly treating either as accepted; and resolve the guaranteed-prophecy/history-change source promise before building its compatible/incompatible timeline cases.\n\n"
        "**Narrow source facts still needed:** elemental damage and actual companion phases; lawful planar source/receiving point; native multiattack reach/range; continuing-item termination and generating-school evidence; current anatomy and remains; capture-eligible victim/custody facts; physical crate and tether specifications; stone/mithril physical and recipe facts; summon identity/control profiles and permissions; faction history/privacy/forecast records; and the concrete Faction Perfection benefit provider/terms. The per-spell audit report records the exact blocker and minimum witness for every identity.\n\n"
        "The remaining gates are (1) exact source fact, authorized spell-local contract or permission; (2) positive and adverse integrated witnesses with legal acquisition, costs, clocks, resources and custody; (3) semantic and forward/inverse integrity validation; (4) a new exact per-identity decision; and (5) independent audit before applying only explicit acceptances. Runtime, implementation, human play, balance, cosmology, domain closure, completion and release remain separate gates. No decision or canonical file changed in this conference.\n\n"
        f"See the [independent 37-identity reconciliation](ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249.json), [receipt](ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_RECEIPT.json), and [request sent to GPT](ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_REQUEST.txt).\n",
        encoding="utf-8")

    submission_path = BASE / "ALL37_PENDING_SPELL_REVIEW_CONFERENCE_249_SUBMISSION.json"
    submission = {
        "id": "ALL37-PENDING-SPELL-REVIEWS-CONFERENCE-249-SUBMISSION",
        "recordedAtUtc": now,
        "status": "GPT_CONFERENCE_COMPLETE_REMAINING_WORK_RECONCILED_811_37_0",
        "destination": "GPT director conversation: Calibration review part 6",
        "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "browserVerified": True,
        "attachedReport": info(reconciliation_path),
        "auditReceipt": info(reconciliation_receipt_path),
        "request": info(request_path),
        "outcome": {
            "returnRange": [232, 248],
            "returnCount": 17,
            "reviewedIdentityCount": 37,
            "heldIds": reconciliation["heldIds"],
            "acceptedIds": [],
            "appliedIds": [],
            "authority": reconciliation["authority"],
            "nextReviewGroup": None,
            "staleReturn248PointerCorrected": True,
            "recommendedFirstClosureTask": {"spellId": "eternal-forge", "blockerId": "MF210-B01"},
            "recommendedSecondClosureTask": {"spellId": "unravel-identity", "blockerId": "MD196-B02"},
            "canonicalChanges": False,
            "applicationChanges": False,
        },
    }
    write(submission_path, submission)

    queue_path = BASE / "CURRENT_SPELL_QUEUE_249.json"
    queue = read(queue_path)
    queue.update({"status": "GPT_CONFERENCE_COMPLETE_REMAINING_WORK_RECONCILED_811_37_0",
                  "packetStatus": "ALL37_PENDING_DIRECTOR_REVIEWS_COMPLETE_HELD",
                  "directorConferenceResponse": info(conference),
                  "directorConferenceSubmission": info(submission_path),
                  "nextGroup": None, "nextPendingIds": [],
                  "recommendedClosurePriority": ["eternal-forge", "unravel-identity"],
                  "allPendingGroupsReviewed": True})
    write(queue_path, queue)

    handoff_path = BASE / "CURRENT_HANDOFF_249.json"
    handoff = read(handoff_path)
    handoff.update({"status": "GPT_CONFERENCE_COMPLETE_REMAINING_WORK_RECONCILED_811_37_0",
                    "queue": info(queue_path), "currentQueueBinding": info(queue_path),
                    "directorConferenceResponse": info(conference),
                    "directorConferenceSubmission": info(submission_path),
                    "nextGroup": None, "nextPendingIds": [], "nextPendingCount": 0,
                    "recommendedClosurePriority": ["eternal-forge", "unravel-identity"],
                    "resumePriority": "No first-review tasks remain. GPT confirmed all 37 current pending identities have sealed held decisions across Returns232-248. Begin blocker resolution with Eternal Forge MF210-B01, followed by Unravel Identity MD196-B02; use the per-spell reconciliation for exact witnesses, then obtain new exact decisions and independently audit before application.",
                    "nextStep": "Use the completed GPT conference plan to begin targeted blocker-resolution work; no unreviewed pending spell group remains.",
                    "canonicalChanges": False, "applicationChanges": False, "githubChanges": False})
    write(handoff_path, handoff)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_249.md"
    text = snapshot_path.read_text(encoding="utf-8-sig")
    text = text.replace("Conferring with GPT on the consolidated remaining blockers and missing witnesses.", "GPT confirmed no first-review tasks remain and recommended Eternal Forge MF210-B01, then Unravel Identity MD196-B02, as the first blocker-closure tasks.")
    snapshot_path.write_text(text, encoding="utf-8")

    start_path = ROOT / "START_HERE.md"
    lines = start_path.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = ("**Current ordinary spell-review handoff [249](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_249.json):** "
                "GPT confirmed all 37 current pending identities have sealed held decisions across Returns232–248; there are no first-review tasks, zero acceptances and zero applications. "
                "The next blocker-closure priorities are Eternal Forge (MF210-B01), then Unravel Identity (MD196-B02).")
    start_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": submission["status"], "conference": info(conference),
                      "submission": info(submission_path), "queue": info(queue_path),
                      "handoff": info(handoff_path), "snapshot": info(snapshot_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
