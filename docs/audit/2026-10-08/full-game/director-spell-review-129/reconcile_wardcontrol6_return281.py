from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ARCHIVE = BASE / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
DELIVERY = BASE / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
AUDIT = BASE / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_WARDCONTROL6_RETURN281_RECEIPT.json"
SOURCE_PACKET = BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip"


def bind(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


authority = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
targets = ["nullification-wave", "reality-anchor"]
next_group = "rank9-time-fate6"
next_ids = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
decision = json.loads(zipfile.ZipFile(ARCHIVE).read("DIRECTOR_DECISION.json"))
delivery = read(DELIVERY)
audit = read(AUDIT)
receipt = read(RECEIPT)
assert audit["status"] == receipt["status"] == "PASS" and audit["checkCount"] == 17 and audit["failedChecks"] == 0
assert decision["acceptedIds"] == decision["appliedIds"] == [] and decision["heldIds"] == targets
assert delivery["authority"] == decision["authorityAfter"] == authority
assert delivery["nextPendingGroup"] == {"group": next_group, "pendingIds": next_ids}

ruling_path = BASE / "RANK9_WARDCONTROL6_DIRECTOR_RULING_281.json"
write(ruling_path, decision)
ruling_binding = bind(ruling_path)
crosscheck_path = BASE / "RANK9_WARDCONTROL6_RETURN281_CROSSCHECK.json"
crosscheck = {
    "id": "RANK9-WARDCONTROL6-RETURN281-CROSSCHECK",
    "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS",
    "archive": bind(ARCHIVE), "deliveryManifest": bind(DELIVERY),
    "directorRuling": ruling_binding, "independentAudit": bind(AUDIT), "receipt": bind(RECEIPT),
    "checkCount": 17, "passedChecks": 17, "failedChecks": 0,
    "acceptedIds": [], "appliedIds": [], "heldIds": targets,
    "blockerIds": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]},
    "authority": authority, "nextPendingGroup": delivery["nextPendingGroup"],
    "minimumMissingWitnesses": {row["spellId"]: row["minimumMissingWitness"] for row in decision["decisions"]},
    "scopeLimitation": "Crosschecks sealed package and authority fields; the game-rule adjudication remains the Director's ruling."
}
write(crosscheck_path, crosscheck)

q_path = BASE / "CURRENT_SPELL_QUEUE_282.json"
h_path = BASE / "CURRENT_HANDOFF_282.json"
p_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_282.json"
q = read(BASE / "CURRENT_SPELL_QUEUE_281.json")
h = read(BASE / "CURRENT_HANDOFF_281.json")
p = read(BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_281.json")
assert q["currentAuthority"] == h["currentAuthority"] == p["authority"] == authority
assert q["nextGroup"] == h["nextGroup"] == "rank9-ward-control6"

archive_binding, delivery_binding = bind(ARCHIVE), bind(DELIVERY)
audit_binding, receipt_binding = bind(AUDIT), bind(RECEIPT)
crosscheck_binding = bind(crosscheck_path)
source_packet_binding = bind(SOURCE_PACKET)
source_delivery_binding = bind(BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json")
return_record = {"return": 281, "group": "rank9-ward-control6", "pendingIds": targets,
                 "acceptedIds": [], "appliedIds": [], "heldIds": targets,
                 "blockerIds": {"nullification-wave": ["WC188-B01"], "reality-anchor": ["WC188-B02"]},
                 "authorityAfter": authority, "archive": archive_binding, "delivery": delivery_binding,
                 "directorRuling": ruling_binding, "crosscheck": crosscheck_binding,
                 "independentAudit": audit_binding, "receipt": receipt_binding,
                 "sourcePacket": source_packet_binding, "sourcePacketDelivery": source_delivery_binding,
                 "auditStatus": "PASS", "auditChecks": 17}
next_row = {"group": next_group, "pendingIds": next_ids, "pendingCount": 4,
            "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_816_32",
            "freshPacketRequiredForCurrentAuthority": True}

for row in q.get("currentPendingGroups", []):
    if row.get("group") == "rank9-ward-control6":
        row.update({"status": "DIRECTOR_RETURN281_HELD_816_32", "acceptedIds": [], "appliedIds": [],
                    "heldIds": targets, "blockerIds": return_record["blockerIds"],
                    "directorRuling": ruling_binding, "archive": archive_binding,
                    "delivery": delivery_binding, "independentAudit": audit_binding,
                    "receipt": receipt_binding, "crosscheck": crosscheck_binding})
    if row.get("group") == next_group:
        row.update({"status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_816_32",
                    "freshPacketRequiredForCurrentAuthority": True})
q.update({"id": "SPELL-REVIEW-QUEUE-282", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_WARDCONTROL6_RETURN281_HELD_816_32_NEXT_TIMEFATE6",
          "packetStatus": "RETURN281_HELD_NEXT_TIMEFATE6_CURRENT_PACKET_REQUIRED_816_32",
          "lastReviewedBatch": return_record, "currentReturnArchive": archive_binding,
          "currentReturnDelivery": delivery_binding, "currentReturnRuling": ruling_binding,
          "currentReturnCrosscheck": crosscheck_binding, "currentReturnAudit": audit_binding,
          "currentReturnReceipt": receipt_binding, "currentReturnSourcePacket": source_packet_binding,
          "currentReturnSourceDelivery": source_delivery_binding, "currentIndependentAudit": audit_binding,
          "currentReceipt": receipt_binding, "nextGroup": next_group,
          "nextPendingIds": next_ids, "nextPendingCount": len(next_ids), "next": next_row,
          "nextPreparedRequest": {"group": next_group, "pendingIds": next_ids,
                                  "status": "CURRENT_SOURCE_PACKET_REQUIRED_816_32"},
          "nextSuggestedGroups": [next_row], "githubChanges": False,
          "canonicalRuntimeApplicationPerformed": False})
q_path.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
q_binding = bind(q_path)

p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-282", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RETURN281_HELD_816_32_NEXT_TIMEFATE6",
          "preparedNextGroup": {"group": next_group, "pendingIds": next_ids, "pendingCount": 4,
                                "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_816_32",
                                "freshPacketRequiredForCurrentAuthority": True},
          "lastDirectorReturn": return_record})
preserved = p.get("preservedRecentHolds", [])
preserved.append({"return": 281, "ids": targets, "blockerIds": return_record["blockerIds"],
                  "acceptedIds": [], "appliedIds": [], "archive": archive_binding,
                  "delivery": delivery_binding, "ruling": ruling_binding,
                  "independentAudit": audit_binding, "receipt": receipt_binding,
                  "crosscheck": crosscheck_binding})
p["preservedRecentHolds"] = preserved
write(p_path, p)
p_binding = bind(p_path)
q["pendingIdentityAudit"] = p_binding
write(q_path, q)
q_binding = bind(q_path)

h.update({"id": "CURRENT-HANDOFF-282", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
          "status": "RANK9_WARDCONTROL6_RETURN281_HELD_816_32_NEXT_TIMEFATE6",
          "currentAuthority": authority, "latestBatch": return_record,
          "currentReturnArchive": archive_binding, "currentReturnDelivery": delivery_binding,
          "currentReturnRuling": ruling_binding, "currentReturnCrosscheck": crosscheck_binding,
          "currentReturnAudit": audit_binding, "currentReturnReceipt": receipt_binding,
          "currentReturnSourceArchive": source_packet_binding, "currentReturnSourceDelivery": source_delivery_binding,
          "queue": q_binding, "queueBinding": q_binding, "currentQueueBinding": q_binding,
          "pendingIdentityAudit": p_binding, "nextGroup": next_group,
          "nextStep": {"group": next_group, "pendingIds": next_ids, "pendingCount": 4,
                       "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_816_32"},
          "nextStepText": "Prepare and independently audit fresh Time/Fate6 sources at 816/32; send only time-stop, fate-rewrite, collapse-timeline and eternal-prophecy to the GPT Director. Keep polling; apply only exact independently audited acceptances.",
          "appliedThisStep": False, "githubChanges": False,
          "canonicalRuntimeApplicationPerformed": False})
write(h_path, h)

snapshot = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_282.md"
snapshot.write_text(
    "# Current ordinary spell-review checkpoint 282\n\n"
    "Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces.\n\n"
    "Return281 held nullification-wave (WC188-B01) and reality-anchor (WC188-B02), independently audited PASS (17/17). The Wave still lacks an authorized continuing property and source-owned permanent ending/remainder contract; Anchor lacks a complete continuing-property deny/allow, suppression, expiry and resumption history. All 32 preserved cases replayed, but held and superseded records do not establish positive witnesses. No acceptance or application occurred.\n\n"
    "Next is **Time/Fate6**: time-stop, fate-rewrite, collapse-timeline and eternal-prophecy. A fresh 816/32 packet is required.\n\n"
    "See [handoff](CURRENT_HANDOFF_282.json), [queue](CURRENT_SPELL_QUEUE_282.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_282.json), [Return281 ruling](RANK9_WARDCONTROL6_DIRECTOR_RULING_281.json), and [independent audit](RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json).\n",
    encoding="utf-8")
start = ROOT / "START_HERE.md"
old = start.read_text(encoding="utf-8-sig")
first, sep, rest = old.partition("\n\n")
if "Current ordinary spell-review handoff [281]" in first:
    start.write_text(
        "**Current ordinary spell-review handoff [282](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_282.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. Return281 is independently audited PASS (17/17), held both Ward/Control6 identities, and selected Time/Fate6 next. See [ruling](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_DIRECTOR_RULING_281.json) and [audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json).\n\n"
        + rest, encoding="utf-8", newline="\n")
print(json.dumps({"authority": authority, "returnAudit": audit_binding,
                  "heldIds": targets, "blockers": return_record["blockerIds"],
                  "nextGroup": next_row, "queue": bind(q_path),
                  "handoff": bind(h_path), "pendingAudit": bind(p_path)}, indent=2))
