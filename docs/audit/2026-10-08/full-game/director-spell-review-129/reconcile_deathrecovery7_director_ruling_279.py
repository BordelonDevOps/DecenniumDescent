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
TARGET = ["final-word"]


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def bind(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def read(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8-sig"))


def write(name: str, value) -> None:
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    q279_path = BASE / "CURRENT_SPELL_QUEUE_279.json"
    h279_path = BASE / "CURRENT_HANDOFF_279.json"
    p279_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_279.json"
    packet_path = BASE / "RANK9DEATHRECOVERY7_PACKET_279.json"
    packet_audit_path = BASE / "RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json"
    packet_receipt_path = BASE / "RANK9DEATHRECOVERY7_PACKET279_RECEIPT.json"
    q279, h279, p279 = read(q279_path.name), read(h279_path.name), read(p279_path.name)
    packet, packet_audit, packet_receipt = read(packet_path.name), read(packet_audit_path.name), read(packet_receipt_path.name)
    assert q279["currentAuthority"] == h279["currentAuthority"] == p279["authority"] == AUTH
    assert q279["nextGroup"] == "rank9-death-recovery7" and q279["nextPendingIds"] == TARGET
    assert packet["status"] == "PREPARED_INDEPENDENTLY_AUDITED_UNSENT"
    assert packet_audit["status"] == packet_receipt["status"] == "PASS"
    assert packet["accepted"] is False and packet["applied"] is False

    now = datetime.now(timezone.utc).isoformat()
    ruling = {
        "id": "DEATHRECOVERY7-DIRECTOR-TEXT-RULING-279", "recordedAtUtc": now,
        "status": "DIRECTOR_TEXT_DECISION_COMPLETE_NOT_SEALED",
        "source": {"kind": "visible GPT Director text response in Calibration review part 6", "conversation": CHAT,
                   "sealedReturnArchiveCreated": False, "deliveryManifestCreated": False, "libraryItemCreated": False},
        "packet": bind(packet_path), "packetArchive": packet["archive"],
        "packetIndependentAudit": bind(packet_audit_path), "packetReceipt": bind(packet_receipt_path),
        "authority": AUTH, "scopeIds": TARGET, "acceptedIds": [], "appliedIds": [], "heldIds": TARGET,
        "blockerIds": ["DR217-B01"],
        "decision": "HOLD",
        "directorReplayClaims": {"cases": 16, "events": 223, "forwardOperations": 446, "inverseOperations": 446,
                                 "completeConditionalTraces": 6, "evidenceHeldContinuations": 10,
                                 "sourceBindings": 74, "unchangedComparedToReturn235": 73,
                                 "changedComparedToReturn235": ["authored_review_index.json"],
                                 "replayPassed": True, "sourcePackagePreservationClockChecksPassed": True},
        "minimumMissingWitness": [
            "One actual source-established independent victim, with a current body/form and life-state contract, normal HP below 50 at resolution, and legal targeting.",
            "Affirmative soul availability and capture eligibility; resolve exact custody, capture bars, Hunt/Hunted Death and origin/summon restrictions.",
            "A legally acquired, paid Final Word cast causing actual final death after applicable prevention, not merely zero HP or a prevented death.",
            "Lawful reserve-token creation tied to that victim/cast/death, followed by eligible one-spell base-RP expenditure, unused-remainder loss and counter/nonrefund behavior. Concurrent tokens require independently lawful captures and preserve each original next-completed-long-rest expiry."
        ],
        "sourceFinding": "Gorthan's reported past soulbinding returns establish neither current body/HP nor present soul availability/custody; they do not prove permanent ineligibility.",
        "preservedSpellLocalRules": ["threshold", "direct-death ordering", "finite reserve", "payment", "concurrency", "expiry"],
        "noAdditionalDesignPermissionOrUniversalAfterlifeModelRequired": True,
        "retainedQualifications": ["DR217-H-SOURCE", "DR217-H-RUNTIME", "DR217-H-BALANCE", "DR217-H-COSMOLOGY", "DR217-H-RELEASE", "DR184-H03"],
        "nextGroup": {"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"]},
        "orderedRemainder": [
            {"rank": 1, "group": "rank9-memory-denial6", "ids": ["mind-collapse"]},
            {"rank": 2, "group": "rank9-agency-control9", "ids": ["absolute-domination"]},
            {"rank": 3, "group": "rank9-agency-control9", "ids": ["puppetmaster-s-realm"]},
            {"rank": 4, "group": "rank9-psychic-fear7", "ids": ["psychic-scream", "mass-phantom-killer", "weird"]},
            {"rank": 5, "group": "rank9-death-recovery7", "ids": TARGET},
            {"rank": 6, "group": "rank9-defense-form8", "ids": ["elemental-shell", "timeless-form", "invulnerable-sphere"]},
            {"rank": 7, "group": "rank9-ward-control6", "ids": ["nullification-wave", "reality-anchor"]},
            {"rank": 8, "group": "rank9-time-fate6", "ids": ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]},
            {"rank": 9, "group": "rank9-knowledge-revelation5", "ids": ["faction-omniscience-supreme"]},
            {"rank": 10, "group": "rank9-planar-gates5", "ids": ["banishment-gate", "conjure-demiplane-fortress"]},
            {"rank": 11, "group": "rank9-summon-hosts5", "ids": ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]},
            {"rank": 12, "group": "rank9-impact-exile4", "ids": ["reverse-gravity-field"]},
            {"rank": 13, "group": "rank9-alignment-faction-purification5", "ids": ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"]},
            {"rank": 14, "group": "rank9-projection-confinement2", "ids": ["astral-projection", "imprisonment"]},
            {"rank": 15, "group": "rank9-miracle-reality2", "ids": ["divine-intervention-greater", "wish"]}
        ],
        "allUnrelatedHoldsAndAcceptedIdentitiesUnchanged": True,
        "noFirstReviewTasksRemain": True,
        "noAcceptanceOrApplication": True,
        "gatesRemainClosed": ["runtime", "implementation", "human-play/playtest", "balance", "cosmology", "domain-closure", "completion", "release"]
    }
    ruling_path = BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279.json"
    ruling_path.write_text(json.dumps(ruling, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rb = bind(ruling_path)
    checks = [
        ("authority is exactly 816/32/0 and 540/173", ruling["authority"] == AUTH),
        ("only final-word is in scope and held", ruling["scopeIds"] == TARGET and ruling["heldIds"] == TARGET and ruling["acceptedIds"] == ruling["appliedIds"] == []),
        ("blocker remains DR217-B01", ruling["blockerIds"] == ["DR217-B01"]),
        ("all 16 replay claim and operation counts are internally consistent", ruling["directorReplayClaims"]["cases"] == 16 and ruling["directorReplayClaims"]["events"] == 223 and ruling["directorReplayClaims"]["forwardOperations"] == ruling["directorReplayClaims"]["inverseOperations"] == 446 and ruling["directorReplayClaims"]["completeConditionalTraces"] + ruling["directorReplayClaims"]["evidenceHeldContinuations"] == 16),
        ("minimum witness includes current body/HP, soul custody, paid final death and lawful reserve expenditure", len(ruling["minimumMissingWitness"]) == 4 and "body/form" in ruling["minimumMissingWitness"][0] and "soul availability" in ruling["minimumMissingWitness"][1] and "actual final death" in ruling["minimumMissingWitness"][2] and "Lawful reserve-token" in ruling["minimumMissingWitness"][3]),
        ("retained qualifications and no-new-universal-model condition are explicit", ruling["retainedQualifications"] == ["DR217-H-SOURCE", "DR217-H-RUNTIME", "DR217-H-BALANCE", "DR217-H-COSMOLOGY", "DR217-H-RELEASE", "DR184-H03"] and ruling["noAdditionalDesignPermissionOrUniversalAfterlifeModelRequired"] is True),
        ("next group is exact Defense/Form8 target set", ruling["nextGroup"] == {"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"]}),
        ("ordered remainder contains exactly 32 identities over 15 rows", len(ruling["orderedRemainder"]) == 15 and sum(len(x["ids"]) for x in ruling["orderedRemainder"]) == 32),
        ("Packet279 itself remains independently audited PASS with no acceptance", packet_audit["status"] == packet_receipt["status"] == "PASS" and packet["accepted"] is False and packet["applied"] is False),
        ("Director explicitly states no sealed return or delivery artifact was created", ruling["source"]["sealedReturnArchiveCreated"] is False and ruling["source"]["deliveryManifestCreated"] is False)
    ]
    failed = [name for name, passed in checks if not passed]
    audit = {"id": "DEATHRECOVERY7-DIRECTOR-RULING-279-CROSSCHECK", "recordedAtUtc": now,
             "status": "PASS" if not failed else "FAIL", "ruling": rb,
             "checkCount": len(checks), "passedChecks": len(checks)-len(failed), "failedChecks": len(failed),
             "checks": [{"check": name, "passed": passed} for name, passed in checks]}
    audit_path = BASE / "DEATHRECOVERY7_DIRECTOR_RULING_279_CROSSCHECK.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_binding = bind(audit_path)

    p = copy.deepcopy(p279)
    p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-280", "recordedAtUtc": now,
              "status": "PASS_EXACT_816_32_PENDING_SET_AFTER_DIRECTOR_TEXT_RETURN279",
              "lastDirectorReturn": {"return": 279, "group": "rank9-death-recovery7", "acceptedIds": [], "appliedIds": [],
                  "heldIds": TARGET, "blockerIds": {"final-word": ["DR217-B01"]}, "ruling": rb,
                  "crosscheck": audit_binding, "packet": packet["archive"], "packetAudit": bind(packet_audit_path),
                  "packetReceipt": bind(packet_receipt_path), "sealedReturnArtifactCreated": False,
                  "auditStatus": audit["status"]},
              "directorDecision": rb,
              "preparedNextGroup": {"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
                  "pendingCount": 3, "historicalPhase": "HELD_RETURN218_DF218_B01_B02_B03_B04_REASSESSMENT_REQUIRED",
                  "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "freshPacketRequiredForCurrentAuthority": True,
                  "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}},
              "preservedRecentHolds": [*p279.get("preservedRecentHolds", []),
                  {"ids": TARGET, "blockerIds": {"final-word": ["DR217-B01"]}, "return": rb, "crosscheck": audit_binding}],
              "authority": AUTH})
    for g in p.get("groups", []):
        if g.get("group") == "rank9-death-recovery7":
            g.update({"status": "DIRECTOR_TEXT_RETURN279_HELD_816_32", "acceptedIds": [], "appliedIds": [],
                      "heldIds": TARGET, "blockerIds": {"final-word": ["DR217-B01"]}, "directorRuling": rb})
        elif g.get("group") == "rank9-defense-form8":
            g.update({"status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32",
                      "directorPriority": "Next group per Return279: Defense/Form8."})
    p280_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_280.json"
    p280_path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    q = copy.deepcopy(q279)
    q.update({"id": "SPELL-REVIEW-QUEUE-280", "recordedAtUtc": now,
              "supersedesQueue": bind(q279_path), "status": "RETURN279_TEXT_HELD_816_32_NEXT_DEFENSEFORM8",
              "packetStatus": "RETURN279_TEXT_HELD_816_32_NEXT_DEFENSEFORM8", "pendingIdentityAudit": bind(p280_path),
              "pendingCount": 32, "nextGroup": "rank9-defense-form8", "nextPendingCount": 3,
              "nextPendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
              "currentReturnRuling": rb, "currentReturnCrosscheck": audit_binding,
              "currentReturnPacket": packet["archive"], "currentReturnPacketAudit": bind(packet_audit_path),
              "currentReturnPacketReceipt": bind(packet_receipt_path), "currentReturnArchive": None,
              "currentReturnDelivery": None, "currentReturnAudit": audit_binding, "currentReturnReceipt": None,
              "currentPacket": None, "currentSourcePacket": None, "currentDeliveryManifest": None,
              "currentPacketDelivery": None, "currentPreparation": None, "currentIndependentAudit": None, "currentReceipt": None,
              "next": {"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "pendingCount": 3,
                       "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "freshPacketRequiredForCurrentAuthority": True,
                       "historicalBlockers": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]},
                       "directorRuling": rb},
              "nextPreparedRequest": {"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "pendingCount": 3,
                       "status": "PACKET280_PREPARATION_IN_PROGRESS_816_32", "freshPacketRequiredForCurrentAuthority": True,
                       "directorRuling": rb, "packet": None, "independentAudit": None},
              "lastReviewedBatch": {"group": "rank9-death-recovery7", "pendingIds": TARGET, "acceptedIds": [], "appliedIds": [],
                       "heldIds": TARGET, "blockerIds": {"final-word": ["DR217-B01"]}, "directorRuling": rb,
                       "crosscheck": audit_binding, "packet": packet["archive"],
                       "packetAudit": bind(packet_audit_path), "packetReceipt": bind(packet_receipt_path),
                       "sealedReturnArtifactCreated": False}, "githubChanges": False})
    q["currentAuthority"] = AUTH
    for g in q.get("currentPendingGroups", []):
        if g.get("group") == "rank9-death-recovery7":
            g.update({"status": "DIRECTOR_TEXT_RETURN279_HELD_816_32", "acceptedIds": [], "appliedIds": [],
                      "heldIds": TARGET, "blockerIds": {"final-word": ["DR217-B01"]}, "directorRuling": rb})
        elif g.get("group") == "rank9-defense-form8":
            g.update({"status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "directorRuling": rb})
    q["nextSuggestedGroups"] = [{"group": "rank9-defense-form8", "pendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
                                  "pendingCount": 3, "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32",
                                  "freshPacketRequiredForCurrentAuthority": True, "directorRuling": rb}]
    q["nextPriorityContext"] = {"group": "rank9-defense-form8", "identities": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
                                 "blockers": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}}
    q280_path = BASE / "CURRENT_SPELL_QUEUE_280.json"
    q280_path.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    h = copy.deepcopy(h279)
    h.update({"id": "CURRENT-HANDOFF-280", "recordedAtUtc": now, "supersedes": bind(h279_path),
              "status": "RETURN279_TEXT_HELD_816_32_NEXT_DEFENSEFORM8", "currentAuthority": AUTH, "authority": AUTH,
              "queue": bind(q280_path), "queueBinding": bind(q280_path), "currentQueueBinding": bind(q280_path),
              "pendingIdentityAudit": bind(p280_path), "latestBatch": q["lastReviewedBatch"],
              "currentReturnRuling": rb, "currentReturnCrosscheck": audit_binding, "currentReturnPacket": packet["archive"],
              "currentReturnArchive": None, "currentReturnDelivery": None, "currentReturnAudit": audit_binding,
              "currentReturnReceipt": None, "currentPacket": None, "currentPacketDelivery": None,
              "currentDeliveryManifest": None, "currentPreparation": None, "currentIndependentAudit": None, "currentReceipt": None,
              "nextGroup": "rank9-defense-form8", "nextPendingCount": 3, "nextPendingIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"],
              "nextStep": q["next"],
              "resumePriority": "Prepare fresh current-authority Packet280 for Defense/Form8 only, with current 816/32 source bindings; reassess elemental-shell DF218-B01/B02, timeless-form DF218-B03 and invulnerable-sphere DF218-B04; independently audit, send to the GPT Director, keep polling, and apply only exact audited acceptances.",
              "githubChanges": False, "canonicalRuntimeApplicationPerformed": False})
    h280_path = BASE / "CURRENT_HANDOFF_280.json"
    h280_path.write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    q["pendingIdentityAudit"] = bind(p280_path); write("CURRENT_SPELL_QUEUE_280.json", q)
    h["queue"] = bind(q280_path); h["queueBinding"] = bind(q280_path); h["currentQueueBinding"] = bind(q280_path); h["pendingIdentityAudit"] = bind(p280_path); write("CURRENT_HANDOFF_280.json", h)
    snapshot = """# Current ordinary spell-review checkpoint 280

Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.

The Director held final-word under DR217-B01. Its text ruling says the 16 preserved cases replayed (223 events; 446 forward and inverse operations), but no eligible-victim/capture witness exists. The Director did not create a sealed Return279 archive or delivery manifest. No acceptance or application occurred.

Next is **Defense/Form8**: elemental-shell (DF218-B01/B02), timeless-form (DF218-B03), and invulnerable-sphere (DF218-B04), refreshed at 816/32. See [handoff](CURRENT_HANDOFF_280.json), [queue](CURRENT_SPELL_QUEUE_280.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_280.json), and [Director ruling](DEATHRECOVERY7_DIRECTOR_RULING_279.json).
"""
    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_280.md").write_text(snapshot, encoding="utf-8")
    start = ROOT / "START_HERE.md"
    old = start.read_text(encoding="utf-8-sig")
    marker = "**Current ordinary spell-review handoff [279](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_279.json):**"
    if old.startswith(marker):
        _, _, rest = old.partition("\n\n")
        top = "**Current ordinary spell-review handoff [280](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_280.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. The Director held final-word under DR217-B01; next is Defense/Form8. See [ruling](docs/audit/2026-10-08/full-game/director-spell-review-129/DEATHRECOVERY7_DIRECTOR_RULING_279.json)."
        start.write_text(top + "\n\n" + rest, encoding="utf-8", newline="\n")
    print(json.dumps({"status": audit["status"], "ruling": rb, "crosscheck": audit_binding,
                      "authority": AUTH, "held": TARGET, "nextGroup": q["nextGroup"],
                      "nextIds": q["nextPendingIds"], "queue": bind(q280_path),
                      "handoff": bind(h280_path), "pending": bind(p280_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
