from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PACKET = A / "rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306.zip"
DELIVERY = A / "rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306_DELIVERY.json"
AUDIT = A / "ELEMENTAL_SHELL_PACKET_306_INDEPENDENT_AUDIT.json"
OLD_RECEIPT = A / "ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT.json"
Q0 = A / "CURRENT_SPELL_QUEUE_304.json"
H0 = A / "CURRENT_HANDOFF_305.json"
P0 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_304.json"
AUTHORITY = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
ORDER = ["final-word", "elemental-shell", "timeless-form", "invulnerable-sphere", "nullification-wave", "reality-anchor",
         "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme",
         "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes",
         "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection",
         "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment",
         "divine-intervention-greater", "wish"]
NEXT = {"group": "rank9-defense-form8", "pendingIds": ["timeless-form", "invulnerable-sphere"], "pendingCount": 2,
        "status": "DIRECTOR_NEXT_AFTER_ELEMENTAL_SHELL_HOLD_306", "freshPacketRequiredForCurrentAuthority": True,
        "blockerByIdentity": {"timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]},
        "directorRequirement": "Next closure identity is Timeless Form / DF218-B03, followed by Invulnerable Sphere / DF218-B04, then Nullification Wave. Final Word remains held under DR217-B01; Elemental Shell remains held under DF218-B01/B02. Obtain current exact Timeless Form evidence requirements from Director before preparing its packet."}
DIRECTOR_RESPONSE = (
    "HOLD — elemental-shell, accepted=false, applied=false. Both DF218-B01 and DF218-B02 remain open. Packet306 preserves prior evidence but supplies neither missing integrated witness. "
    "DF218-B01: One source-qualified noncreature elemental damage event: geometry, type, amount/roll, timing, bearer occupancy and defenses, and paid Shell/deadline history. Demonstrate immunity and—where no responsible creature dealer exists—no reflected recipient or packet. The preserved SHELL-B2-ENVIRONMENT.json#/events/4 still records source-premise-held-no-packet-invented. "
    "DF218-B02: One lawfully acquired, instantiated companion/proxy with complete body/profile, equipment, native elemental attack/reach/range, controller acquisition, command payment and attached-phase history. Demonstrate the attack and reflection against the actual dealer, preserving damage, resources and custody. The preserved SHELL-B3-PROXY.json#/events/4 still stops at the missing premise. "
    "Current-source inspection confirms Dominate Beast supplies a conditional execution bridge, not the missing instantiated companion; Spectral Steed expressly supplies no damaging Action; environmental leads supply no completed qualifying event. No synthetic replacement or obligation revision is authorized. "
    "Verified 13,255,922 bytes, archive SHA-256 d165cd0f44d728a5cdb27c5dcdbdbdec0f1cf1ae4220be8efea94649566ca45b, CRC32 290c4eaa, 151 members, all 150 payload bindings and 87 source bindings. Only the index differs from Packet280. All 21 cases are byte-preserved, containing 428 events and 856 forward/856 inverse operations; preservation/count checks, not a fresh replay claim. "
    "The sole receipt correction is ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT.json#/correctedHandoff: bind the exact embedded and previously confirmed handoff, 43,340 bytes, SHA-256 f862f7d971fd7ec0eec5f65e11b638bd95acdd8e69123ab7eee0936e758492ed, CRC32 ffd04cc8. Correct that receipt binding without changing the handoff or review semantics; archive internal binding is correct. "
    "acceptedIds=[]; appliedIds=[]; heldIds=[elemental-shell]. Prior qualifications and unrelated holds, including Final Word, remain unchanged. Authority 822/26/0; 546 procedures/173 interfaces. Next Timeless Form / DF218-B03, then Invulnerable Sphere / DF218-B04, then Nullification Wave. No canonical changes or application."
)

def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def raw(path: pathlib.Path):
    return path.read_bytes()

def ref(path: pathlib.Path, data: bytes | None = None):
    b = raw(path) if data is None else data
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}

def write(path: pathlib.Path, value):
    b = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(b)
    return b

def main():
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    packet_raw = raw(PACKET)
    assert hashlib.sha256(packet_raw).hexdigest() == "d165cd0f44d728a5cdb27c5dcdbdbdec0f1cf1ae4220be8efea94649566ca45b"
    audit, delivery, old_receipt = read(AUDIT), read(DELIVERY), read(OLD_RECEIPT)
    assert audit["status"] == "PASS" and audit["checkCount"] == 15 and audit["failedChecks"] == 0
    assert delivery["authority"] == AUTHORITY and delivery["targetIds"] == ["elemental-shell"]
    assert old_receipt["acceptedIds"] == old_receipt["appliedIds"] == []
    with zipfile.ZipFile(PACKET) as z:
        embedded = z.read("current/CURRENT_HANDOFF_305.json")
        embedded_ref = {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_305.json",
                        "bytes": len(embedded), "sha256": hashlib.sha256(embedded).hexdigest(),
                        "crc32": f"{zlib.crc32(embedded) & 0xffffffff:08x}"}
        assert embedded_ref == {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_305.json",
                                "bytes": 43340, "sha256": "f862f7d971fd7ec0eec5f65e11b638bd95acdd8e69123ab7eee0936e758492ed", "crc32": "ffd04cc8"}
    stale = copy.deepcopy(old_receipt.get("correctedHandoff"))
    corrected = copy.deepcopy(old_receipt)
    corrected.update({"id": "ELEMENTAL-SHELL-DELTA-306-SUBMISSION-RECEIPT-CORRECTED-307",
                      "recordedAtUtc": stamp, "status": "DIRECTOR_HELD_DF218_B01_B02_RECEIPT_BINDING_CORRECTED",
                      "supersedes": ref(OLD_RECEIPT), "supersededCorrectedHandoffBinding": stale,
                      "correctedHandoff": embedded_ref,
                      "directorCorrection": "Receipt corrected to bind the exact handoff bytes embedded in Packet306. The handoff and review semantics were not changed."})
    receipt_path = A / "ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT_CORRECTED_307.json"
    receipt_ref = ref(receipt_path, write(receipt_path, corrected))

    decision = {"id": "ELEMENTAL-SHELL-DF218-B01-B02-DIRECTOR-DECISION-306", "recordedAtUtc": stamp,
                "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
                "scopeIds": ["elemental-shell"], "decision": "HOLD", "accepted": False, "applied": False,
                "acceptedIds": [], "appliedIds": [], "heldIds": ["elemental-shell"],
                "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"]},
                "unresolvedEvidence": {"DF218-B01": "One source-qualified noncreature elemental damage event with exact geometry/type/amount-or-roll/timing, bearer occupancy/defenses, paid Shell/deadline history, and immunity; where no responsible creature dealer exists, no reflected recipient/packet. Existing SHELL-B2-ENVIRONMENT.json#/events/4 still states source-premise-held-no-packet-invented.",
                                      "DF218-B02": "One lawfully acquired, instantiated companion/proxy with full body/profile/equipment, native elemental attack/reach/range, controller acquisition, command payment, attached-phase history, and attack/reflection against actual dealer with damage/resources/custody. Existing SHELL-B3-PROXY.json#/events/4 stops at missing premise."},
                "currentSourceFindings": ["Dominate Beast is only a conditional execution bridge, not the missing instantiated companion.", "Spectral Steed supplies no damaging Action.", "Environmental leads contain no completed qualifying event."],
                "noSyntheticReplacementOrObligationRevisionAuthorized": True,
                "packetVerification": {"archive": ref(PACKET), "delivery": ref(DELIVERY), "independentAudit": ref(AUDIT), "members": 151, "payloadMembers": 150, "sourceBindings": 87, "preservedCases": 21, "preservedEvents": 428, "preservedForwardOperations": 856, "preservedInverseOperations": 856, "freshReplayClaim": False, "onlyDifferenceFromPacket280": "authored_review_index.json"},
                "receiptCorrection": receipt_ref, "embeddedHandoffBinding": embedded_ref,
                "retainedQualificationsAndUnrelatedHolds": True, "nextOrder": ["timeless-form", "invulnerable-sphere", "nullification-wave"],
                "currentAuthority": AUTHORITY, "canonicalFilesChanged": False}
    decision_path = A / "ELEMENTAL_SHELL_DIRECTOR_DECISION_306.json"
    decision_ref = ref(decision_path, write(decision_path, decision))

    hold_receipt = {"id": "ELEMENTAL-SHELL-HOLD-RECEIPT-306", "recordedAtUtc": stamp,
                    "status": "DIRECTOR_HELD_ELEMENTAL_SHELL_DF218_B01_B02",
                    "acceptedIds": [], "appliedIds": [], "heldIds": ["elemental-shell"],
                    "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"]},
                    "decision": decision_ref, "packet": ref(PACKET), "independentAudit": ref(AUDIT),
                    "correctedPacketReceipt": receipt_ref, "canonicalFilesChanged": False}
    hold_path = A / "ELEMENTAL_SHELL_HOLD_RECEIPT_306.json"
    hold_ref = ref(hold_path, write(hold_path, hold_receipt))

    q0, h0, p0 = read(Q0), read(H0), read(P0)
    idx_raw, cat_raw = raw(INDEX), raw(CATALOG)
    pending_ids = sorted(r["id"] for r in read(INDEX)["entries"] if r.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending_ids) == 26 and "elemental-shell" in pending_ids and "timeless-form" in pending_ids
    p1 = copy.deepcopy(p0)
    p1.update({"id": "CURRENT26-PENDING-IDENTITY-AUDIT-307", "recordedAtUtc": stamp,
               "status": "PASS_CURRENT_822_26_AFTER_ELEMENTAL_SHELL_HOLD_306",
               "supersedes": ref(P0), "authority": AUTHORITY, "pendingCount": 26, "pendingIds": pending_ids,
               "acceptedIds": copy.deepcopy(p0.get("acceptedIds", [])), "appliedIds": copy.deepcopy(p0.get("appliedIds", [])),
               "heldIds": sorted(set(p0.get("heldIds", [])) | {"elemental-shell"}),
               "lastDirectorDecision": decision_ref, "lastDirectorHoldReceipt": hold_ref,
               "lastDirectorReturn": {"decision": decision_ref, "acceptedIds": [], "appliedIds": [], "heldIds": ["elemental-shell"], "blockerIds": ["DF218-B01", "DF218-B02"]},
               "nextPendingGroup": copy.deepcopy(NEXT), "nextGroup": NEXT["group"], "nextPendingIds": NEXT["pendingIds"], "nextPendingCount": NEXT["pendingCount"],
               "canonicalFilesChanged": False})
    p_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_307.json"
    p_ref = ref(p_path, write(p_path, p1))

    q1 = copy.deepcopy(q0)
    q1.update({"id": "SPELL-REVIEW-QUEUE-307", "recordedAtUtc": stamp,
               "supersedesQueue": ref(Q0), "parentQueue": ref(Q0), "currentAuthority": AUTHORITY,
               "currentIndexBinding": ref(INDEX), "pendingIdentityAudit": p_ref,
               "pendingCount": 26, "nextGroup": NEXT["group"], "next": copy.deepcopy(NEXT),
               "nextPendingIds": NEXT["pendingIds"], "nextPendingCount": NEXT["pendingCount"], "nextSuggestedGroups": [copy.deepcopy(NEXT)],
               "recommendedClosurePriority": ORDER,
               "heldPriorityTask": {"identity": "final-word", "blocker": "DR217-B01", "status": "HELD_PENDING_POSITIVE_SOURCE_QUALIFIED_CAPTURE_WITNESS", "remainsInPendingSet": True},
               "lastDirectorDecision": decision_ref, "lastDirectorHoldReceipt": hold_ref,
               "lastReviewedBatch": {"return": 306, "group": "rank9-defense-form8", "acceptedIds": [], "appliedIds": [], "heldIds": ["elemental-shell"], "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"]}, "authorityBefore": AUTHORITY, "authorityAfter": AUTHORITY},
               "currentDirectorPosition": {"stage": "ELEMENTAL_SHELL_HELD_DF218_B01_B02; NEXT_TIMELESS_FORM_DF218_B03", "acceptedIds": [], "appliedIds": [],
                                           "heldIds": sorted(set(p1["heldIds"])), "blockers": {"final-word": ["DR217-B01"], "elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}, "nextPendingGroup": copy.deepcopy(NEXT)},
               "currentPreparation": copy.deepcopy(NEXT), "nextPriorityContext": {"identity": "timeless-form", "blockers": ["DF218-B03"], "requirement": "Refresh with Director for current exact Time Stop source/acquisition and chronology evidence before submission."},
               "packetStatus": "ELEMENTAL_SHELL_HELD_DF218_B01_B02; NEXT_TIMELESS_FORM_DF218_B03",
               "closureStatus": {"firstReviewTasksRemaining": 0, "closureTasksRemaining": 26, "heldPendingIdentities": sorted(set(p1["heldIds"])), "nextActionableIdentity": "timeless-form"},
               "canonicalRuntimeApplicationPerformed": False, "githubChanges": False})
    q_path = A / "CURRENT_SPELL_QUEUE_307.json"
    q_ref = ref(q_path, write(q_path, q1))

    h1 = copy.deepcopy(h0)
    h1.update({"id": "CURRENT-HANDOFF-307", "recordedAtUtc": stamp, "supersedes": "CURRENT-HANDOFF-306 / file CURRENT_HANDOFF_305.json",
               "status": "ELEMENTAL_SHELL_HELD_NEXT_TIMELESS_FORM_822_26",
               "authority": AUTHORITY, "currentAuthority": AUTHORITY,
               "indexBinding": ref(INDEX), "queueBinding": q_ref, "currentQueueBinding": q_ref,
               "queue": q_path.relative_to(ROOT).as_posix(), "pendingIdentityAudit": p_ref,
               "lastDirectorDecision": decision_ref, "lastDirectorHoldReceipt": hold_ref,
               "lastPacketReceiptCorrection": receipt_ref,
               "nextStep": copy.deepcopy(NEXT), "nextGroup": NEXT["group"], "nextPendingCount": NEXT["pendingCount"], "nextPendingIds": NEXT["pendingIds"],
               "nextPendingGroup": copy.deepcopy(NEXT), "currentPreparation": copy.deepcopy(NEXT),
               "currentBlocker": {"identity": "timeless-form", "group": "rank9-defense-form8", "blockerIds": ["DF218-B03"]},
               "directorConnectionStatus": "Director held Elemental Shell under DF218-B01/B02; packet306 passed integrity but supplied neither integrated witness. Receipt binding correction recorded separately; no handoff semantics or canonical review state changed. Final Word remains held. Next Timeless Form / DF218-B03, then Invulnerable Sphere / DF218-B04, then Nullification Wave.",
               "acceptedThisStep": [], "unacceptedThisStep": ["elemental-shell"], "appliedThisStep": False,
               "latestBatch": {"accepted": [], "applied": [], "held": {"elemental-shell": ["DF218-B01", "DF218-B02"]}},
               "firstReviewTasksRemaining": 0, "allPendingIdentitiesReviewed": True,
               "nextStepText": NEXT["directorRequirement"], "canonicalRuntimeApplicationPerformed": False, "githubChanges": False})
    h_path = A / "CURRENT_HANDOFF_307.json"
    h_ref = ref(h_path, write(h_path, h1))

    # Validate the Director ruling, corrected receipt binding, and successor queue.
    checks = [
        ("Director exact hold has no acceptance or application", decision["heldIds"] == ["elemental-shell"] and decision["acceptedIds"] == decision["appliedIds"] == []),
        ("Both existing Elemental Shell blockers remain open with exact minimum witnesses", decision["blockerIds"]["elemental-shell"] == ["DF218-B01", "DF218-B02"] and all(k in decision["unresolvedEvidence"] for k in ("DF218-B01", "DF218-B02"))),
        ("Packet internal handoff binding is the exact corrected receipt value", embedded_ref == corrected["correctedHandoff"] and stale != embedded_ref),
        ("The correction changes only the receipt pointer and preserves its prior wrong binding", corrected["supersededCorrectedHandoffBinding"] == stale and corrected["correctedHandoff"] == embedded_ref and corrected["packet"] == old_receipt["packet"]),
        ("Archive evidence and 21 case preservation match Director verification", delivery["archive"]["sha256"] == decision["packetVerification"]["archive"]["sha256"] and delivery["memberCount"] == 151 and decision["packetVerification"]["preservedCases"] == 21 and decision["packetVerification"]["preservedEvents"] == 428),
        ("Current authority and exact pending index set remain unchanged", p1["authority"] == AUTHORITY and len(pending_ids) == 26 and p1["pendingIds"] == pending_ids),
        ("Next actionable queue matches Director's exact order", q1["next"]["pendingIds"] == ["timeless-form", "invulnerable-sphere"] and NEXT["blockerByIdentity"]["timeless-form"] == ["DF218-B03"]),
        ("Corrected handoff resolves its queue and pending-audit bindings", h1["queueBinding"] == q_ref and h1["pendingIdentityAudit"] == p_ref and h1["nextPendingGroup"] == h1["currentPreparation"]),
        ("Authored index and native catalog remain byte-exact", raw(INDEX) == idx_raw and raw(CATALOG) == cat_raw),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {"id": "ELEMENTAL-SHELL-HOLD-RECEIPT-CORRECTION-VALIDATION-307", "recordedAtUtc": stamp,
                  "status": "PASS", "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
                  "checks": [{"check": n, "passed": bool(ok)} for n, ok in checks],
                  "directorDecision": decision_ref, "correctedReceipt": receipt_ref, "holdReceipt": hold_ref,
                  "queue": q_ref, "pendingAudit": p_ref, "handoff": h_ref,
                  "authority": AUTHORITY, "canonicalFilesChanged": False, "acceptedIds": [], "appliedIds": []}
    val_path = A / "ELEMENTAL_SHELL_HOLD_VALIDATION_307.json"
    val_ref = ref(val_path, write(val_path, validation))
    snapshot = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_307.md"
    snapshot.write_text("# Spell Review Snapshot — Elemental Shell Held (307)\n\n"
                        "Authority remains **822 applied / 26 pending / 0 accepted-unapplied; 546 procedures / 173 interfaces**.\n\n"
                        "Director held Elemental Shell under DF218-B01 and DF218-B02. The source-qualified noncreature elemental event and the lawfully acquired, instantiated companion/proxy with complete attack/reflection history are still absent. Synthetic replacement is not authorized. Packet306 integrity and preservation checks passed; 21 prior cases / 428 events / 856 forward and inverse operations are preserved, not newly replayed.\n\n"
                        "Director identified and corrected one receipt-only handoff binding; the packet’s embedded handoff bytes are unchanged. Final Word remains separately held under DR217-B01. Next: Timeless Form / DF218-B03, then Invulnerable Sphere / DF218-B04, then Nullification Wave.\n\n"
                        "Validation: " + val_ref["path"] + " (" + val_ref["sha256"] + ").\n", encoding="utf-8", newline="\n")
    assert raw(INDEX) == idx_raw and raw(CATALOG) == cat_raw
    print(json.dumps({"status": "PASS", "authority": AUTHORITY, "held": decision["heldIds"],
                      "blockers": decision["blockerIds"], "correctedReceipt": receipt_ref,
                      "queue": q_ref, "pendingAudit": p_ref, "handoff": h_ref, "validation": val_ref,
                      "next": NEXT["pendingIds"]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
