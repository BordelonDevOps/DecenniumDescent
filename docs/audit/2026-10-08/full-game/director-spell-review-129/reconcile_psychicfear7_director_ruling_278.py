from __future__ import annotations

import copy
import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
BLOCKERS = {"psychic-scream": ["PF182-B01"], "mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def bind(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def read(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8-sig"))


def write(name: str, value) -> None:
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    q278_path = BASE / "CURRENT_SPELL_QUEUE_278.json"
    h278_path = BASE / "CURRENT_HANDOFF_278.json"
    p278_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_278.json"
    packet_path = BASE / "RANK9PSYCHICFEAR7_PACKET_278.json"
    packet_audit_path = BASE / "RANK9PSYCHICFEAR7_PACKET278_INDEPENDENT_AUDIT.json"
    packet_receipt_path = BASE / "RANK9PSYCHICFEAR7_PACKET278_RECEIPT.json"
    assert all(p.is_file() for p in [q278_path, h278_path, p278_path, packet_path, packet_audit_path, packet_receipt_path])
    q278, h278, p278 = read(q278_path.name), read(h278_path.name), read(p278_path.name)
    packet, packet_audit, packet_receipt = read(packet_path.name), read(packet_audit_path.name), read(packet_receipt_path.name)
    assert q278["currentAuthority"] == h278["currentAuthority"] == p278["authority"] == AUTH
    assert packet["status"] == "PREPARED_INDEPENDENTLY_AUDITED_UNSENT"
    assert packet_audit["status"] == packet_receipt["status"] == "PASS"
    assert packet["accepted"] is False and packet["applied"] is False
    assert packet["independentAudit"]["sha256"] == bind(packet_audit_path)["sha256"]
    assert packet["archive"]["sha256"] == packet_audit["archive"]["sha256"]
    assert packet_audit["targetIds"] == TARGETS and packet_audit["authority"] == AUTH

    now = datetime.now(timezone.utc).isoformat()
    ruling = {
        "id": "PSYCHIC-FEAR7-DIRECTOR-RULING-278",
        "recordedAtUtc": now,
        "status": "VISIBLE_DIRECTOR_TEXT_RULING_CAPTURED_AND_RECONCILED",
        "source": {"kind": "visible GPT Director response in Calibration review part 6", "conversation": CHAT,
                   "sealedReturnArchiveSupplied": False},
        "packet": bind(packet_path), "packetArchive": packet["archive"],
        "packetIndependentAudit": bind(packet_audit_path), "packetReceipt": bind(packet_receipt_path),
        "authority": AUTH,
        "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS,
        "decisions": [
            {"spellId": "psychic-scream", "decision": "HOLD", "blockerIds": ["PF182-B01"],
             "retainedQualifications": ["PF181-H03"],
             "incompleteCases": ["RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-B/positive-final-death-head-consequence",
                                 "RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-B/headless-multihead-current-form"],
             "sourceAnchors": ["catalog.json#/spells/395", "Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json#/spells/409",
                               "Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json#/spells/514",
                               "Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json#/spells/620"],
             "minimumWitness": "Authorized recipient/current-form anatomy with head count, destructibility, vital-head relationship, reversion/remains; integrated defenses, survival, Null/form rules, final death, permitted head consequence and remains/equipment custody."},
            {"spellId": "mass-phantom-killer", "decision": "HOLD", "blockerIds": ["PF182-B02"],
             "retainedQualifications": ["PF181-H05"],
             "incompleteCases": ["RANK9PSYCHICFEAR7-180-MASS-PHANTOM-KILLER-B/genuine-extra-turn-and-attached-phase"],
             "sourceAnchors": ["catalog.json#/spells/576", "Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json#/spells/609"],
             "minimumWitness": "Authorized genuine inserted-full-turn grant, legally acquired actor and grantor history, stored-action expenditure, limits, fatigue/timing, and integrated regular-turn/inserted-turn/attached-phase trace preserving damage, saves, recharge, Ready, resources and original clocks."},
            {"spellId": "weird", "decision": "HOLD", "blockerIds": ["PF182-B02"],
             "retainedQualifications": ["PF181-H05", "H149-01", "H149-02", "H149-03", "H149-06", "H149-07", "H149-08", "H149-10", "H149-11", "H149-12", "H149-13"],
             "incompleteCases": ["RANK9PSYCHICFEAR7-180-WEIRD-B/genuine-extra-turn-source-hold"],
             "sourceAnchors": ["catalog.json#/spells/396", "Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json#/spells/410",
                               "Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json#/spells/616"],
             "minimumWitness": "Same qualified grant dependency, separately integrated against Weird damage, captivity, ending saves and original clock."}
        ],
        "directorVerificationClaims": {
            "archiveMembers": 103, "refreshedSourceBindings": 84, "archiveChecksPassed": 959, "archiveCheckFailures": 0,
            "preservedCases": 47, "events": 2464, "forwardOperations": 4928, "inverseOperations": 4928,
            "assertions": 34590, "replayFailures": 0, "incompleteWitnessCases": 4,
            "interpretation": "Replay verifies the held records and mechanics, not the missing positive outcomes."
        },
        "turnGrantSourceLead": {"name": "Chrono Collapse", "source": "rulebook_output.txt", "lines": "7412-7424",
            "finding": "Printed lead describes three back-to-back turns and class/feat/skill/Temporal Tower prerequisites, but packet lacks acquired actor, activation, stored-action expenditure, limits, fatigue and timing contract; wording alone is insufficient."},
        "timeStop": {"catalog": "/spells/584", "core": "/spells/921", "sourceParagraph": 10122,
            "finding": "Alternate grant is real, but remains unresolved and nonoperational; TF192-B01 unchanged and cannot supply the witness."},
        "nextGroup": {"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "blockerIds": ["DR217-B01"],
            "minimumWitness": "Source-qualified capture/reserve-use trace for an eligible victim: current body and HP, soul availability, custody, capture and subsequent lawful reserve expenditure."},
        "remainingIdentityCount": 32,
        "noAcceptanceOrApplication": True,
        "noFirstReviewTasksRemain": True
    }
    ruling_path = BASE / "PSYCHICFEAR7_DIRECTOR_RULING_278.json"
    ruling_path.write_text(json.dumps(ruling, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ruling_binding = bind(ruling_path)

    checks = [
        ("authority remains exactly 816/32/0 and 540/173", ruling["authority"] == AUTH),
        ("Director explicitly holds exactly the three packet targets", ruling["heldIds"] == TARGETS and ruling["acceptedIds"] == ruling["appliedIds"] == []),
        ("blocker mapping matches the Director's text ruling", {x["spellId"]: x["blockerIds"] for x in ruling["decisions"]} == BLOCKERS),
        ("all three decisions preserve explicit prior qualifications", all(x["retainedQualifications"] for x in ruling["decisions"])),
        ("next group is the exact Director-confirmed final-word identity", ruling["nextGroup"]["group"] == "rank9-death-recovery7" and ruling["nextGroup"]["pendingIds"] == ["final-word"] and ruling["nextGroup"]["blockerIds"] == ["DR217-B01"]),
        ("Packet278 remains independently audited PASS and non-accepting", packet_audit["status"] == "PASS" and packet["accepted"] is False and packet["applied"] is False),
        ("Director source/replay claims identify four incomplete cases", ruling["directorVerificationClaims"]["archiveCheckFailures"] == 0 and ruling["directorVerificationClaims"]["incompleteWitnessCases"] == 4)
    ]
    failed = [name for name, passed in checks if not passed]
    response_audit = {"id": "PSYCHICFEAR7-DIRECTOR-RULING-278-CROSSCHECK", "recordedAtUtc": now,
                      "status": "PASS" if not failed else "FAIL", "ruling": ruling_binding,
                      "checkCount": len(checks), "passedChecks": len(checks)-len(failed), "failedChecks": len(failed),
                      "checks": [{"check": name, "passed": passed} for name, passed in checks]}
    response_audit_path = BASE / "PSYCHICFEAR7_DIRECTOR_RULING_278_CROSSCHECK.json"
    response_audit_path.write_text(json.dumps(response_audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    response_audit_binding = bind(response_audit_path)

    p = copy.deepcopy(p278)
    p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-279", "recordedAtUtc": now,
              "status": "PASS_EXACT_816_32_PENDING_SET_AFTER_DIRECTOR_RETURN278",
              "lastDirectorReturn": {"return": 278, "group": "rank9-psychic-fear7", "acceptedIds": [], "appliedIds": [],
                  "heldIds": TARGETS, "blockerIds": BLOCKERS, "ruling": ruling_binding,
                  "crosscheck": response_audit_binding, "packet": packet["archive"],
                  "packetAudit": bind(packet_audit_path), "packetReceipt": bind(packet_receipt_path), "auditStatus": response_audit["status"]},
              "directorDecision": ruling_binding,
              "preparedNextGroup": {"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1,
                  "historicalPhase": "HELD_RETURN217_DR217-B01_REASSESSMENT_REQUIRED",
                  "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32",
                  "freshPacketRequiredForCurrentAuthority": True,
                  "requirements": ruling["nextGroup"]["minimumWitness"]},
              "preservedRecentHolds": [*p278.get("preservedRecentHolds", []),
                  {"ids": TARGETS, "blockerIds": BLOCKERS, "return": ruling_binding, "audit": response_audit_binding}],
              "authority": AUTH})
    for group in p.get("groups", []):
        if group.get("group") == "rank9-psychic-fear7":
            group.update({"status": "DIRECTOR_RETURN278_HELD_816_32", "acceptedIds": [], "appliedIds": [],
                          "heldIds": TARGETS, "blockerIds": BLOCKERS, "directorRuling": ruling_binding})
        elif group.get("group") == "rank9-death-recovery7":
            group.update({"status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "directorPriority": "Next after Return278; final-word DR217-B01."})
    p279_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_279.json"
    p279_path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    q = copy.deepcopy(q278)
    q.update({"id": "SPELL-REVIEW-QUEUE-279", "recordedAtUtc": now,
              "supersedesQueue": bind(q278_path), "status": "RETURN278_AUDITED_HELD_816_32_NEXT_FINAL_WORD",
              "packetStatus": "RETURN278_AUDITED_HELD_816_32_NEXT_FINAL_WORD",
              "pendingIdentityAudit": bind(p279_path), "pendingCount": 32,
              "nextGroup": "rank9-death-recovery7", "nextPendingCount": 1, "nextPendingIds": ["final-word"],
              "currentReturnRuling": ruling_binding, "currentReturnCrosscheck": response_audit_binding,
              "currentReturnPacket": packet["archive"], "currentReturnPacketAudit": bind(packet_audit_path),
              "currentReturnPacketReceipt": bind(packet_receipt_path), "currentPacket": None,
              "currentDeliveryManifest": None, "currentPacketDelivery": None, "currentPreparation": None,
              "currentSourcePacket": None, "currentIndependentAudit": None, "currentReceipt": None,
              "next": {"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1,
                       "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "freshPacketRequiredForCurrentAuthority": True,
                       "historicalHold": "Return217 DR217-B01", "directorRuling": ruling_binding,
                       "minimumWitness": ruling["nextGroup"]["minimumWitness"]},
              "nextPreparedRequest": {"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1,
                       "status": "PACKET279_PREPARATION_IN_PROGRESS_816_32", "freshPacketRequiredForCurrentAuthority": True,
                       "historicalHold": "Return217 DR217-B01", "directorRuling": ruling_binding,
                       "minimumWitness": ruling["nextGroup"]["minimumWitness"], "packet": None, "independentAudit": None},
              "lastReviewedBatch": {"group": "rank9-psychic-fear7", "pendingIds": TARGETS,
                       "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS, "blockerIds": BLOCKERS,
                       "directorRuling": ruling_binding, "crosscheck": response_audit_binding,
                       "packet": packet["archive"], "packetAudit": bind(packet_audit_path), "packetReceipt": bind(packet_receipt_path)},
              "githubChanges": False})
    q["currentAuthority"] = AUTH
    q["currentPendingGroups"] = [
        {"rank": 1, "group": "qualification-holds", "pendingIds": ["mind-collapse", "absolute-domination", "puppetmaster-s-realm"], "pendingCount": 3, "status": "RETAINED_HELD_DIRECTOR_RETURN277"},
        {"rank": 2, "group": "rank9-psychic-fear7", "pendingIds": TARGETS, "pendingCount": 3, "status": "DIRECTOR_RETURN278_HELD_816_32", "blockerIds": BLOCKERS},
        {"rank": 3, "group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1, "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "blockerIds": {"final-word": ["DR217-B01"]}},
        *[copy.deepcopy(x) for x in q278.get("currentPendingGroups", []) if x.get("group") not in {"rank9-psychic-fear7", "rank9-death-recovery7", "rank9-memory-denial6", "rank9-agency-control9"}]
    ]
    q["recommendedClosureOrder"] = [
        {"rank": 1, "identities": ["mind-collapse"], "priority": "Retained MD196-B01 and qualifications."},
        {"rank": 2, "identities": ["absolute-domination"], "priority": "Retained AG190-B01."},
        {"rank": 3, "identities": ["puppetmaster-s-realm"], "priority": "Retained AG190-B02/H150-ROSTER."},
        {"rank": 4, "identities": TARGETS, "priority": "Return278 held all three under PF182-B01/B02."},
        {"rank": 5, "identities": ["final-word"], "priority": "Director next group; retained DR217-B01."},
        *[copy.deepcopy(x) for x in q278.get("recommendedClosureOrder", [])[5:]]
    ]
    q["nextSuggestedGroups"] = [{"group": "rank9-death-recovery7", "pendingIds": ["final-word"], "pendingCount": 1,
                                  "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32",
                                  "freshPacketRequiredForCurrentAuthority": True,
                                  "directorRuling": ruling_binding,
                                  "minimumWitness": ruling["nextGroup"]["minimumWitness"]}]
    q["nextPriorityContext"] = {"identity": "final-word", "group": "rank9-death-recovery7", "blocker": "DR217-B01",
                                "requirements": [ruling["nextGroup"]["minimumWitness"]]}
    q279_path = BASE / "CURRENT_SPELL_QUEUE_279.json"
    q279_path.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    h = copy.deepcopy(h278)
    h.update({"id": "CURRENT-HANDOFF-279", "recordedAtUtc": now,
              "supersedes": bind(h278_path), "status": "RETURN278_AUDITED_HELD_816_32_NEXT_FINAL_WORD",
              "currentAuthority": AUTH, "authority": AUTH, "queue": bind(q279_path), "queueBinding": bind(q279_path),
              "currentQueueBinding": bind(q279_path), "pendingIdentityAudit": bind(p279_path),
              "latestBatch": q["lastReviewedBatch"], "currentReturnRuling": ruling_binding,
              "currentReturnCrosscheck": response_audit_binding, "currentReturnPacket": packet["archive"],
              "currentPacket": None, "currentPacketDelivery": None, "currentDeliveryManifest": None,
              "currentPreparation": None, "nextGroup": "rank9-death-recovery7", "nextPendingCount": 1,
              "nextPendingIds": ["final-word"],
              "nextStep": q["next"],
              "resumePriority": "Prepare fresh current-authority Packet279 for final-word only under DR217-B01; prove source-qualified eligible victim body/HP, soul availability, custody, capture, and lawful reserve expenditure; independently audit, submit to the GPT Director and keep polling; apply only exact accepted identities.",
              "githubChanges": False, "canonicalRuntimeApplicationPerformed": False})
    h279_path = BASE / "CURRENT_HANDOFF_279.json"
    h279_path.write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    snapshot = f"""# Current ordinary spell-review checkpoint 279

Authority is **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.

The Director held Psychic Scream (PF182-B01), Mass Phantom Killer (PF182-B02) and Weird (PF182-B02). Packet278 passed the local 16-check audit; the Director reports 959 archive checks and a 47-case replay with 34,590 assertions, zero replay failures and four incomplete positive-witness cases. No acceptance or application occurred.

Next is **rank9-death-recovery7 — final-word only**, retained under DR217-B01. Required evidence: eligible victim current body/HP, soul availability, custody, capture, and subsequent lawful reserve expenditure. See [handoff](CURRENT_HANDOFF_279.json), [queue](CURRENT_SPELL_QUEUE_279.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_279.json), and [Director ruling](PSYCHICFEAR7_DIRECTOR_RULING_278.json).
"""
    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_279.md").write_text(snapshot, encoding="utf-8")
    start = ROOT / "START_HERE.md"
    old = start.read_text(encoding="utf-8-sig")
    marker = "**Current ordinary spell-review handoff [278](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_278.json):**"
    if old.startswith(marker):
        first, _, rest = old.partition("\n\n")
        head = "**Current ordinary spell-review handoff [279](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_279.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. The Director held Psychic Scream, Mass Phantom Killer and Weird; next is final-word under DR217-B01. See [ruling](docs/audit/2026-10-08/full-game/director-spell-review-129/PSYCHICFEAR7_DIRECTOR_RULING_278.json)."
        start.write_text(head + "\n\n" + rest, encoding="utf-8", newline="\n")
    print(json.dumps({"status": response_audit["status"], "ruling": ruling_binding,
                      "crosscheck": response_audit_binding, "authority": AUTH,
                      "accepted": [], "applied": [], "held": TARGETS, "nextGroup": "rank9-death-recovery7",
                      "nextIds": ["final-word"], "queue": bind(q279_path), "handoff": bind(h279_path),
                      "pending": bind(p279_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
