from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import zlib


ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
Q0 = A / "CURRENT_SPELL_QUEUE_302.json"
H0 = A / "CURRENT_HANDOFF_302.json"
P0 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_302.json"
PACKET = A / "rank9_final_word_closure_delta_303/DD_Rank9_FinalWord_ClosureDelta_303.zip"
AUDIT = A / "rank9_final_word_closure_delta_303/INDEPENDENT_AUDIT_303.json"
AUTHORITY = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
NEXT_IDS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
NEXT_BLOCKERS = {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}
ORDER = [
    "final-word", "elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave", "reality-anchor",
    "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme",
    "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes",
    "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection",
    "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment",
    "divine-intervention-greater", "wish",
]
DIRECTOR_RESPONSE = (
    "HOLD — Final Word / final-word / DR217-B01. Delta303 introduces no integrity defect, but does not supply the missing positive capture witness. "
    "acceptedIds=[]; appliedIds=[]; heldIds=[final-word]; blockerIds=[DR217-B01]. Verified the 10,228,938-byte ZIP, SHA-256 087a50b901d1c7f561036d3b3f086871e5c19ebe245d549a687485da6bec57a2, exact 28-member allowlist, payload hashes and CRCs. The 74-source refresh resolves to 73 unchanged files and the updated index. The 16 cases and 223 events remain byte-preserved historical evidence; no fresh replay claim. "
    "The unresolved criterion is INDEPENDENT_SEMANTIC_AUDIT_303.json#/criteria/12 (FW303-S13). Missing: one source-qualified victim with established current living body/HP, soul availability and capture eligibility, custody/capture restrictions, Hunt status and origin/no-farming facts; and a lawful Final Word cast that actually causes that victim's final death, followed by the resulting uniquely identified reserve and lawful payment/lifecycle trace under the already-selected rules. "
    "The Chronicle's lines 145 and 332 establish historical soulbinding; line 549 is an adventure seed. None establishes present victim state or capture eligibility. No true-name prerequisite, new soul doctrine, or additional spell-design permission is required or authorized. Retain DR217-H-SOURCE, DR217-H-RUNTIME, DR217-H-BALANCE, DR217-H-COSMOLOGY, and DR217-H-RELEASE; all downstream gates remain unchanged. "
    "Authority remains 822 applied / 26 pending / 0 accepted-unapplied; 546 procedures / 173 interfaces. Next closure identity: elemental-shell — DF218-B01/B02, followed by timeless-form — DF218-B03, then invulnerable-sphere — DF218-B04. Final Word stays pending; the remaining queue order is unchanged. No other identity is ruled, accepted, or applied."
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


def write(path: pathlib.Path, value) -> None:
    path.write_bytes(encode(value))


def main() -> None:
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    assert sha(PACKET.read_bytes()) == "087a50b901d1c7f561036d3b3f086871e5c19ebe245d549a687485da6bec57a2"
    audit = read(AUDIT)
    assert audit["status"] == "PASS_WITH_DR217_B01_HELD" and audit["failedChecks"] == 0
    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index = read(INDEX)
    q0, h0, p0 = read(Q0), read(H0), read(P0)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTHORITY
    pending = {x["id"] for x in index["entries"] if x.get("authoredStatus") == "pending-authored-procedure"}
    assert len(pending) == 26 and "final-word" in pending and set(NEXT_IDS) <= pending
    assert q0["recommendedClosurePriority"] == ORDER
    decision_path = A / "FINAL_WORD_DIRECTOR_DECISION_303.json"
    decision = {
        "id": "FINAL-WORD-DR217-B01-DIRECTOR-DECISION-303", "recordedAtUtc": stamp,
        "decision": "HOLD_FINAL_WORD_PENDING_POSITIVE_SOURCE_QUALIFIED_CAPTURE_WITNESS",
        "identity": "final-word", "blocker": "DR217-B01", "accepted": False, "applied": False,
        "acceptedIds": [], "appliedIds": [], "heldIds": ["final-word"], "blockerIds": ["DR217-B01"],
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "exactDirectorResponse": DIRECTOR_RESPONSE,
        "submittedPacket": bind(PACKET), "independentAudit": bind(AUDIT),
        "unresolvedCriterion": "INDEPENDENT_SEMANTIC_AUDIT_303.json#/criteria/12 (FW303-S13)",
        "minimumMissingWitness": [
            "One source-qualified victim with an established current living body/HP, soul availability and capture eligibility, custody/capture restrictions, Hunt status and origin/no-farming facts.",
            "A lawful Final Word cast that actually causes that victim's final death, followed by a uniquely identified reserve and lawful payment/lifecycle trace under the selected rules."
        ],
        "ChronicleDisposition": "Lines 145 and 332 establish historical soulbinding; line 549 is an adventure seed and not current victim evidence.",
        "retainedQualifications": ["DR217-H-SOURCE", "DR217-H-RUNTIME", "DR217-H-BALANCE", "DR217-H-COSMOLOGY", "DR217-H-RELEASE"],
        "nextActionableIdentity": "elemental-shell", "nextBlockers": NEXT_BLOCKERS,
        "nextClosureIdentities": NEXT_IDS, "remainingQueueOrder": ORDER,
        "noOtherIdentityRuledAcceptedOrApplied": True, "canonicalFilesChangedByDirector": False,
    }
    write(decision_path, decision)
    decision_ref = bind(decision_path)
    ruling_receipt_path = A / "FINAL_WORD_HOLD_RECEIPT_303.json"
    ruling_receipt = {
        "id": "FINAL-WORD-HOLD-RECEIPT-303", "recordedAtUtc": stamp,
        "status": "DIRECTOR_HELD_FINAL_WORD_DR217_B01; NEXT_ELEMENTAL_SHELL_DF218_B01_B02",
        "acceptedIds": [], "appliedIds": [], "heldIds": ["final-word"], "blockerIds": ["DR217-B01"],
        "decision": decision_ref, "submittedPacket": bind(PACKET), "independentAudit": bind(AUDIT),
        "currentAuthority": AUTHORITY, "nextClosureIdentity": "elemental-shell", "nextClosureBlockers": NEXT_BLOCKERS["elemental-shell"],
        "remainingClosureTasks": 26, "firstReviewTasks": 0,
    }
    write(ruling_receipt_path, ruling_receipt)
    receipt_ref = bind(ruling_receipt_path)

    next_row = {
        "group": "rank9-defense-form8", "pendingIds": NEXT_IDS, "pendingCount": 3,
        "status": "DIRECTOR_NEXT_ACTIONABLE_GROUP_AFTER_FINAL_WORD_HOLD_303",
        "freshPacketRequiredForCurrentAuthority": True,
        "blockerByIdentity": NEXT_BLOCKERS,
        "directorRequirement": "Director ruled Final Word held under DR217-B01. Next closure identity is Elemental Shell / DF218-B01 and DF218-B02, then Timeless Form / DF218-B03, then Invulnerable Sphere / DF218-B04. Obtain a refreshed current-source packet and confirm exact remaining evidence for Elemental Shell.",
    }
    pending1 = copy.deepcopy(p0)
    pending1.update({
        "id": "CURRENT26_PENDING_IDENTITY_AUDIT_304", "recordedAtUtc": stamp,
        "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_FINAL_WORD_HOLD_303",
        "authority": AUTHORITY, "indexBinding": bind(INDEX, index_raw), "catalogBinding": bind(CATALOG, catalog_raw),
        "pendingCount": 26, "pendingIds": sorted(pending),
        "acceptedIds": sorted(set(p0.get("acceptedIds", []))),
        "appliedIds": sorted(set(p0.get("appliedIds", []))),
        "heldIds": sorted(set(p0.get("heldIds", [])) | {"final-word"}),
        "lastDirectorReturn": {"decisionId": decision["id"], "acceptedIds": [], "appliedIds": [], "heldIds": ["final-word"], "blockerIds": {"final-word": ["DR217-B01"]}, "identity": "final-word", "archive": bind(PACKET)},
        "lastReviewedBatch": {"return": 303, "group": "rank9-death-recovery7", "acceptedIds": [], "appliedIds": [], "heldIds": ["final-word"], "blockerIds": {"final-word": ["DR217-B01"]}, "authorityBefore": AUTHORITY, "authorityAfter": AUTHORITY},
        "directorDecision": decision_ref, "directorHoldReceipt": receipt_ref,
        "nextBlockerPriority": ORDER, "preparedNextGroup": next_row,
        "nextGroup": "rank9-defense-form8", "nextPendingIds": NEXT_IDS, "nextPendingCount": 3,
        "nextPendingGroup": next_row, "remainingPendingCount": 26, "pendingIdentityCount": 26,
        "packetStatus": "FINAL_WORD_HELD_DR217_B01; NEXT_ELEMENTAL_SHELL_DF218_B01_B02",
        "firstReviewTasksRemaining": 0,
    })
    pending_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_304.json"
    write(pending_path, pending1)
    pending_ref = bind(pending_path)

    q1 = copy.deepcopy(q0)
    full_order = copy.deepcopy(q0.get("recommendedClosureOrder", []))
    q1.update({
        "id": "SPELL-REVIEW-QUEUE-304", "recordedAtUtc": stamp,
        "supersedesQueue": bind(Q0), "parentQueue": bind(Q0), "currentAuthority": AUTHORITY,
        "currentIndexBinding": bind(INDEX, index_raw), "pendingIdentityAudit": pending_ref,
        "pendingCount": 26, "nextGroup": "rank9-defense-form8", "next": next_row,
        "nextPendingIds": NEXT_IDS, "nextPendingCount": 3, "nextSuggestedGroups": [next_row],
        "recommendedClosurePriority": ORDER, "recommendedClosureOrder": full_order,
        "heldPriorityTask": {"identity": "final-word", "blocker": "DR217-B01", "status": "HELD_PENDING_POSITIVE_SOURCE_QUALIFIED_CAPTURE_WITNESS", "remainsInPendingSet": True},
        "lastReviewedBatch": pending1["lastReviewedBatch"],
        "lastDirectorDecision": decision_ref,
        "currentDirectorPosition": {"stage": "FINAL_WORD_HELD_DR217_B01; ELEMENTAL_SHELL_NEXT_ACTIONABLE_DF218_B01_B02", "acceptedIds": [], "appliedIds": [], "heldIds": sorted(pending), "blockers": {"final-word": ["DR217-B01"], **NEXT_BLOCKERS}, "nextPendingGroup": next_row},
        "nextPriorityContext": {"identity": "elemental-shell", "blockers": NEXT_BLOCKERS["elemental-shell"], "requirement": next_row["directorRequirement"]},
        "currentPreparation": next_row, "githubChanges": False, "canonicalRuntimeApplicationPerformed": False,
        "afterNextAcceptedAppliedForecast": {"remainingIdentities": 25},
        "packetStatus": "FINAL_WORD_HELD; NEXT_ELEMENTAL_SHELL_DF218_B01_B02",
        "closureStatus": {"firstReviewTasksRemaining": 0, "closureTasksRemaining": 26, "heldPendingIdentities": ["final-word"], "nextActionableIdentity": "elemental-shell"},
    })
    queue_path = A / "CURRENT_SPELL_QUEUE_304.json"
    write(queue_path, q1)
    queue_ref = bind(queue_path)
    hand = copy.deepcopy(h0)
    hand.update({
        "id": "CURRENT-HANDOFF-304", "recordedAtUtc": stamp, "supersedes": h0.get("id"),
        "status": "FINAL_WORD_HELD_NEXT_ELEMENTAL_SHELL_822_26",
        "authority": AUTHORITY, "currentAuthority": AUTHORITY,
        "indexBinding": bind(INDEX, index_raw), "queueBinding": queue_ref,
        "queue": queue_path.relative_to(ROOT).as_posix(), "pendingIdentityAudit": pending_ref,
        "appliedThisStep": False, "acceptedThisStep": [],
        "unacceptedThisStep": ["final-word"], "appliedThisStepRecord": None,
        "lastDirectorDecision": decision_ref, "lastDirectorHoldReceipt": receipt_ref,
        "nextStep": next_row, "nextGroup": "rank9-defense-form8", "nextPendingCount": 3,
        "nextPendingIds": NEXT_IDS, "currentBlocker": {"identity": "elemental-shell", "group": "rank9-defense-form8", "blockerIds": NEXT_BLOCKERS["elemental-shell"]},
        "directorConnectionStatus": "GPT held Final Word / DR217-B01 due to missing source-qualified capture witness. No acceptance or application. Next closure identity is Elemental Shell / DF218-B01/B02.",
        "githubChanges": False, "latestBatch": {"accepted": [], "applied": [], "held": {"final-word": ["DR217-B01"]}},
        "currentPreparation": next_row, "canonicalRuntimeApplicationPerformed": False,
        "nextStepText": next_row["directorRequirement"], "currentDirectorPosition": q1["currentDirectorPosition"],
        "resumePriority": ORDER,
        "firstReviewTasksRemaining": 0, "allPendingIdentitiesReviewed": True,
    })
    hand_path = A / "CURRENT_HANDOFF_304.json"
    write(hand_path, hand)
    hand_ref = bind(hand_path)

    checks = [
        ("Director explicitly held only Final Word under DR217-B01", decision["heldIds"] == ["final-word"] and decision["acceptedIds"] == decision["appliedIds"] == []),
        ("Delta303 archive integrity was verified by Director", decision["submittedPacket"]["sha256"] == "087a50b901d1c7f561036d3b3f086871e5c19ebe245d549a687485da6bec57a2"),
        ("Current index/catalog and all 26 pending identities are unchanged", read(INDEX)["authoredCounts"] == {"reviewed": 822, "pending": 26} and len(pending) == 26 and read(CATALOG)["spells"][675]["operational"] is None),
        ("Final Word remains pending and blocked", next(x for x in index["entries"] if x["id"] == "final-word")["authoredStatus"] == "pending-authored-procedure" and next(x for x in index["entries"] if x["id"] == "final-word")["sourceStatus"] == "blocked-pending-operational-review"),
        ("The next actionable identity is Elemental Shell with the Director's DF218 blockers", q1["next"]["pendingIds"] == NEXT_IDS and q1["next"]["blockerByIdentity"] == NEXT_BLOCKERS),
        ("The full 26-identity Director order remains unchanged", q1["recommendedClosurePriority"] == ORDER and len(ORDER) == 26),
        ("No index, catalog, runtime, or acceptance/application mutation was made", INDEX.read_bytes() == index_raw and CATALOG.read_bytes() == catalog_raw and decision["acceptedIds"] == decision["appliedIds"] == []),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {
        "id": "FINAL-WORD-HOLD-AND-NEXT-QUEUE-VALIDATION-304", "recordedAtUtc": stamp,
        "status": "PASS", "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
        "checks": [{"check": name, "passed": bool(ok)} for name, ok in checks],
        "directorDecision": decision_ref, "holdReceipt": receipt_ref, "pendingIdentityAudit": pending_ref,
        "queue": queue_ref, "handoff": hand_ref, "authority": AUTHORITY,
        "heldIdentity": "final-word", "nextActionableIdentity": "elemental-shell",
        "acceptedIds": [], "appliedIds": [], "catalogByteExact": True, "runtimeSelectionEnabled": False,
    }
    validation_path = A / "FINAL_WORD_HOLD_VALIDATION_304.json"
    write(validation_path, validation)
    snapshot = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_304.md"
    snapshot.write_text(
        "# Spell Review Snapshot — Final Word Hold / Elemental Shell Next (304)\n\n"
        "Authority: **822 applied / 26 pending / 0 accepted-unapplied; 546 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "Director held Final Word / DR217-B01 because the current evidence has no source-qualified eligible victim and lawful capture-to-reserve history. The current source packet integrity passed; 73 of the previous 74 sources remain byte-exact and the authored index is the only changed source. Final Word remains pending, the catalog remains blocked, and runtime selection remains disabled.\n\n"
        "Next actionable closure identity: **Elemental Shell / DF218-B01 and DF218-B02**, then Timeless Form / DF218-B03, then Invulnerable Sphere / DF218-B04. The remaining 26-item order is unchanged.\n\n"
        "Validation: " + bind(validation_path)["path"] + " (" + bind(validation_path)["sha256"] + ").\n",
        encoding="utf-8", newline="\n",
    )
    assert INDEX.read_bytes() == index_raw and CATALOG.read_bytes() == catalog_raw
    print(json.dumps({"status": "PASS", "authority": AUTHORITY, "held": "final-word / DR217-B01", "next": next_row, "queue": queue_ref, "handoff": hand_ref, "pendingAudit": pending_ref, "validation": bind(validation_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
