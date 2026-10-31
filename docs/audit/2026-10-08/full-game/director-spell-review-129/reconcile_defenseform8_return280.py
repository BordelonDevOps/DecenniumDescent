from __future__ import annotations

import copy
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
BLOCKERS = {"elemental-shell": ["DF218-B01", "DF218-B02"],
            "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def bind(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())}


def read(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8-sig"))


def write(name: str, value) -> None:
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    received = BASE / "rank9_defenseform8_return280_received"
    archive_path = received / "DD_Rank9_DefenseForm8_Director_Return280_HELD.zip"
    delivery_path = received / "DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json"
    audit_path = BASE / "RANK9DEFENSEFORM8_RETURN280_INDEPENDENT_AUDIT.json"
    receipt_path = BASE / "RANK9DEFENSEFORM8_RETURN280_RECEIPT.json"
    q280_path, h280_path, p280_path = (BASE / n for n in ("CURRENT_SPELL_QUEUE_280.json", "CURRENT_HANDOFF_280.json", "CURRENT32_PENDING_IDENTITY_AUDIT_280.json"))
    q280, h280, p280 = (read(p.name) for p in (q280_path, h280_path, p280_path))
    delivery, audit, receipt = (json.loads(p.read_text(encoding="utf-8-sig")) for p in (delivery_path, audit_path, receipt_path))
    with zipfile.ZipFile(archive_path) as z:
        assert z.testzip() is None
        decision_raw = z.read("DIRECTOR_DECISION.json")
        queue_raw = z.read("REMAINING_QUEUE.json")
        semantic_raw = z.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
    decision = json.loads(decision_raw.decode("utf-8-sig"))
    queue = json.loads(queue_raw.decode("utf-8-sig"))
    semantic = json.loads(semantic_raw.decode("utf-8-sig"))
    expected_order = [sid for row in read("DEATHRECOVERY7_DIRECTOR_RULING_279.json")["orderedRemainder"] for sid in row["ids"]]
    checks = [
        ("Return280 archive and corrected external delivery are independently audited PASS", audit["status"] == receipt["status"] == "PASS" and audit["failedChecks"] == receipt["failedChecks"] == 0),
        ("all three Defense/Form8 identities are held with exact DF218 blockers", delivery["heldIds"] == TARGETS and delivery["acceptedIds"] == delivery["appliedIds"] == [] and {r["id"]: r["blockerIds"] for r in delivery["perIdentity"]} == BLOCKERS),
        ("authority remains exactly 816/32/0 and 540/173", delivery["authority"] == AUTH and q280["currentAuthority"] == h280["currentAuthority"] == p280["authority"] == AUTH),
        ("Director queue and 32-item ordered remainder match the prior queue", delivery["remainingOrderedIds"] == queue["orderedPendingIds"] == expected_order and len(expected_order) == 32),
        ("next group is Ward/Control6 with its two exact pending identities", delivery["nextPendingGroup"] == queue["nextPendingGroup"] == "rank9-ward-control6" and delivery["nextPendingIds"] == queue["nextPendingIds"] == ["nullification-wave", "reality-anchor"]),
        ("all 24,596 integrity/preservation/replay/clock checks passed with no canonical application", delivery["counts"]["freshCheckTotal"] == 24596 and delivery["counts"]["freshCheckFailures"] == 0 and delivery["applicationPerformed"] is False and delivery["canonicalChanges"] is False),
        ("semantic report preserves only the four missing source-witness blockers", semantic["result"] == "HOLD_REQUIRED_WITNESSES" and semantic["dataIntegrityPassed"] is True and set(semantic["blockerIds"]) == {"DF218-B01", "DF218-B02", "DF218-B03", "DF218-B04"}),
    ]
    failed = [name for name, passed in checks if not passed]
    assert not failed, failed

    decision_path = BASE / "RANK9_DEFENSEFORM8_DIRECTOR_RULING_280.json"
    decision_path.write_bytes(decision_raw)
    ruling_binding = bind(decision_path)
    crosscheck = {"id": "RANK9-DEFENSEFORM8-RETURN280-CROSSCHECK", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                  "status": "PASS", "decision": ruling_binding, "archive": bind(archive_path),
                  "delivery": bind(delivery_path), "independentAudit": bind(audit_path), "receipt": bind(receipt_path),
                  "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
                  "checks": [{"check": n, "passed": p} for n, p in checks]}
    crosscheck_path = BASE / "RANK9_DEFENSEFORM8_RETURN280_CROSSCHECK.json"
    crosscheck_path.write_text(json.dumps(crosscheck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cross_binding = bind(crosscheck_path)

    p = copy.deepcopy(p280)
    p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-281", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
              "status": "PASS_EXACT_816_32_PENDING_SET_AFTER_DIRECTOR_RETURN280_HELD",
              "lastDirectorReturn": {"return": 280, "group": "rank9-defense-form8", "acceptedIds": [], "appliedIds": [],
                  "heldIds": TARGETS, "blockerIds": BLOCKERS, "authority": AUTH, "ruling": ruling_binding,
                  "crosscheck": cross_binding, "archive": bind(archive_path), "delivery": bind(delivery_path),
                  "independentAudit": bind(audit_path), "receipt": bind(receipt_path), "auditStatus": audit["status"]},
              "directorDecision": ruling_binding,
              "preparedNextGroup": {"group": "rank9-ward-control6", "pendingIds": ["nullification-wave", "reality-anchor"],
                  "pendingCount": 2, "historicalBlockers": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]},
                  "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "freshPacketRequiredForCurrentAuthority": True},
              "preservedRecentHolds": [*p280.get("preservedRecentHolds", []),
                  {"ids": TARGETS, "blockerIds": BLOCKERS, "return": ruling_binding, "crosscheck": cross_binding}],
              "authority": AUTH})
    for g in p.get("groups", []):
        if g.get("group") == "rank9-defense-form8":
            g.update({"status": "DIRECTOR_RETURN280_HELD_816_32", "acceptedIds": [], "appliedIds": [],
                      "heldIds": TARGETS, "blockerIds": BLOCKERS, "directorRuling": ruling_binding, "independentAudit": bind(audit_path)})
        elif g.get("group") == "rank9-ward-control6":
            g.update({"status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32",
                      "directorPriority": "Next group per Return280: Ward/Control6."})
    p281_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_281.json"
    p281_path.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    q = copy.deepcopy(q280)
    q.update({"id": "SPELL-REVIEW-QUEUE-281", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
              "supersedesQueue": bind(q280_path), "status": "RETURN280_HELD_816_32_NEXT_WARDCONTROL6",
              "packetStatus": "RETURN280_HELD_816_32_NEXT_WARDCONTROL6", "pendingIdentityAudit": bind(p281_path),
              "pendingCount": 32, "nextGroup": "rank9-ward-control6", "nextPendingCount": 2,
              "nextPendingIds": ["nullification-wave", "reality-anchor"], "currentAuthority": AUTH,
              "currentReturnRuling": ruling_binding, "currentReturnCrosscheck": cross_binding,
              "currentReturnArchive": bind(archive_path), "currentReturnDelivery": bind(delivery_path),
              "currentReturnAudit": bind(audit_path), "currentReturnReceipt": bind(receipt_path),
              "currentReturnPacket": q280.get("currentPacket"), "currentReturnPacketAudit": q280.get("currentIndependentAudit"),
              "currentReturnPacketReceipt": q280.get("currentReceipt"), "currentPacket": None,
              "currentSourcePacket": None, "currentDeliveryManifest": None, "currentPacketDelivery": None,
              "currentPreparation": None, "currentIndependentAudit": None, "currentReceipt": None,
              "next": {"group": "rank9-ward-control6", "pendingIds": ["nullification-wave", "reality-anchor"], "pendingCount": 2,
                       "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "freshPacketRequiredForCurrentAuthority": True,
                       "historicalBlockers": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]}, "directorRuling": ruling_binding},
              "nextPreparedRequest": {"group": "rank9-ward-control6", "pendingIds": ["nullification-wave", "reality-anchor"], "pendingCount": 2,
                       "status": "PACKET281_PREPARATION_REQUIRED_816_32", "freshPacketRequiredForCurrentAuthority": True,
                       "directorRuling": ruling_binding, "packet": None, "independentAudit": None},
              "lastReviewedBatch": {"group": "rank9-defense-form8", "pendingIds": TARGETS, "acceptedIds": [], "appliedIds": [],
                       "heldIds": TARGETS, "blockerIds": BLOCKERS, "directorRuling": ruling_binding,
                       "crosscheck": cross_binding, "archive": bind(archive_path), "delivery": bind(delivery_path),
                       "independentAudit": bind(audit_path), "receipt": bind(receipt_path)}, "githubChanges": False})
    for g in q.get("currentPendingGroups", []):
        if g.get("group") == "rank9-defense-form8":
            g.update({"status": "DIRECTOR_RETURN280_HELD_816_32", "acceptedIds": [], "appliedIds": [],
                      "heldIds": TARGETS, "blockerIds": BLOCKERS, "directorRuling": ruling_binding,
                      "independentAudit": bind(audit_path), "receipt": bind(receipt_path)})
        elif g.get("group") == "rank9-ward-control6":
            g.update({"status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32", "directorRuling": ruling_binding})
    q["nextSuggestedGroups"] = [{"group": "rank9-ward-control6", "pendingIds": ["nullification-wave", "reality-anchor"],
                                  "pendingCount": 2, "status": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED_816_32",
                                  "freshPacketRequiredForCurrentAuthority": True, "directorRuling": ruling_binding}]
    q["nextPriorityContext"] = {"group": "rank9-ward-control6", "identities": ["nullification-wave", "reality-anchor"],
                                 "blockers": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]}}
    q281_path = BASE / "CURRENT_SPELL_QUEUE_281.json"
    q281_path.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    h = copy.deepcopy(h280)
    h.update({"id": "CURRENT-HANDOFF-281", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
              "supersedes": bind(h280_path), "status": "RETURN280_HELD_816_32_NEXT_WARDCONTROL6",
              "currentAuthority": AUTH, "authority": AUTH, "queue": bind(q281_path),
              "queueBinding": bind(q281_path), "currentQueueBinding": bind(q281_path),
              "pendingIdentityAudit": bind(p281_path), "latestBatch": q["lastReviewedBatch"],
              "currentReturnRuling": ruling_binding, "currentReturnCrosscheck": cross_binding,
              "currentReturnArchive": bind(archive_path), "currentReturnDelivery": bind(delivery_path),
              "currentReturnAudit": bind(audit_path), "currentReturnReceipt": bind(receipt_path),
              "currentPacket": None, "currentPacketDelivery": None, "currentDeliveryManifest": None,
              "currentPreparation": None, "currentIndependentAudit": None, "currentReceipt": None,
              "nextGroup": "rank9-ward-control6", "nextPendingCount": 2,
              "nextPendingIds": ["nullification-wave", "reality-anchor"], "nextStep": q["next"],
              "resumePriority": "Prepare fresh current-authority Packet281 for Ward/Control6 only, reassessing nullification-wave under WC188-B01 and reality-anchor under WC188-B02; refresh all 91 sources, preserve prior acceptances and Return280, send to GPT, keep polling, and apply only exact independently audited acceptances.",
              "githubChanges": False, "canonicalRuntimeApplicationPerformed": False})
    h281_path = BASE / "CURRENT_HANDOFF_281.json"
    h281_path.write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    q["pendingIdentityAudit"] = bind(p281_path); write(q281_path.name, q)
    h["queue"] = bind(q281_path); h["queueBinding"] = bind(q281_path); h["currentQueueBinding"] = bind(q281_path)
    h["pendingIdentityAudit"] = bind(p281_path); write(h281_path.name, h)
    snapshot = """# Current ordinary spell-review checkpoint 281

Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.

The Director held Defense/Form8: elemental-shell (DF218-B01/B02), timeless-form (DF218-B03), and invulnerable-sphere (DF218-B04). The corrected Return280 archive and delivery manifest preserve the same ZIP SHA-256 and pass the 15-check independent audit; all 46 cases replayed and 24,596 package/source/preservation/replay/clock checks passed. No acceptance or application occurred.

Next is **Ward/Control6**: nullification-wave (WC188-B01) and reality-anchor (WC188-B02), refreshed at 816/32. See [handoff](CURRENT_HANDOFF_281.json), [queue](CURRENT_SPELL_QUEUE_281.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_281.json), [Return280 ruling](RANK9_DEFENSEFORM8_DIRECTOR_RULING_280.json), and [independent audit](RANK9DEFENSEFORM8_RETURN280_INDEPENDENT_AUDIT.json).
"""
    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_281.md").write_text(snapshot, encoding="utf-8")
    start = ROOT / "START_HERE.md"
    old = start.read_text(encoding="utf-8-sig")
    _, _, rest = old.partition("\n\n")
    top = "**Current ordinary spell-review handoff [281](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_281.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. Return280 held Defense/Form8 after a 15/15 independent audit; next is Ward/Control6. See [ruling](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_DIRECTOR_RULING_280.json)."
    start.write_text(top + "\n\n" + rest, encoding="utf-8", newline="\n")

    print(json.dumps({"status": audit["status"], "authority": AUTH, "heldIds": TARGETS,
                      "blockers": BLOCKERS, "nextGroup": q["nextGroup"], "nextIds": q["nextPendingIds"],
                      "crosscheck": bind(crosscheck_path), "queue": bind(q281_path),
                      "handoff": bind(h281_path), "pending": bind(p281_path)}, indent=2))


if __name__ == "__main__":
    main()
