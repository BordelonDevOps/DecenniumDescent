from __future__ import annotations

import hashlib
import json
import pathlib
import re
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = BASE / "rank9_wardcontrol6_return281_received"
ARCHIVE = RECEIVED / "DD_Rank9_WardControl6_Director_Return281_HELD.zip"
DELIVERY = RECEIVED / "DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
SOURCE_PACKET = BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip"
SOURCE_DELIVERY = BASE / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json"
SOURCE_AUDIT = BASE / "RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json"
SOURCE_RECEIPT = BASE / "RANK9_WARDCONTROL6_PACKET281_RECEIPT.json"
PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_281.json"
REPORT = BASE / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_WARDCONTROL6_RETURN281_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
TARGETS = ["nullification-wave", "reality-anchor"]
BLOCKERS = {"nullification-wave": "WC188-B01", "reality-anchor": "WC188-B02"}
NEXT = {"group": "rank9-time-fate6", "pendingIds": ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]}
checks: list[dict] = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def matches(raw: bytes, expected: dict) -> bool:
    got = digest(raw)
    return isinstance(expected, dict) and all(got.get(k) == expected.get(k) for k in ("bytes", "sha256")) and (expected.get("crc32") is None or got["crc32"] == expected["crc32"])


def safe(name: str) -> bool:
    path = pathlib.PurePosixPath(name)
    return bool(name) and not name.startswith("/") and ".." not in path.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


delivery_raw = DELIVERY.read_bytes()
delivery = read_json(delivery_raw)
archive_raw = ARCHIVE.read_bytes()
archive_hash = digest(archive_raw)
delivery_hash = digest(delivery_raw)
check("Return281 archive exactly matches the delivery byte, SHA-256 and CRC32 binding",
      delivery.get("id") == "RANK9-WARDCONTROL6-DIRECTOR-RETURN281-DELIVERY"
      and delivery.get("archive", {}).get("path") == ARCHIVE.name
      and matches(archive_raw, delivery.get("archive", {})),
      {"actual": archive_hash, "expected": delivery.get("archive")})

with zipfile.ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    name_set = set(names)
    check("ZIP directory is valid and all member paths are unique and safe",
          archive.testzip() is None and len(names) == len(name_set) and all(safe(n) for n in names),
          {"members": len(names), "unique": len(name_set)})
    allowlist = delivery.get("exactAllowlist", [])
    check("delivery allowlist exactly matches the 87 ZIP members",
          delivery.get("memberCount") == len(names) == len(allowlist) == 87 and set(allowlist) == name_set,
          {"zip": len(names), "allowlist": len(allowlist), "declared": delivery.get("memberCount")})

    manifest = read_json(archive.read("MEMBER_MANIFEST.json"))
    member_rows = manifest.get("members", [])
    member_map = {row.get("path"): row for row in member_rows if isinstance(row, dict)}
    check("embedded manifest covers the 86 non-self members exactly",
          manifest.get("memberCountExcludingSelf") == 86 and manifest.get("manifestSelfExcluded") is True
          and set(member_map) == name_set - {"MEMBER_MANIFEST.json"},
          {"manifestRows": len(member_map), "declared": manifest.get("memberCountExcludingSelf")})
    bad_members = [n for n, row in member_map.items() if not matches(archive.read(n), row)]
    check("all payload members match embedded size, SHA-256 and CRC32", not bad_members, bad_members[:15])

    decision = read_json(archive.read("DIRECTOR_DECISION.json"))
    counts = read_json(archive.read("COUNTS.json"))
    validation = read_json(archive.read("VALIDATION.json"))
    semantic = read_json(archive.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
    replay = read_json(archive.read("REPLAY_RESULTS.json"))
    source_check = read_json(archive.read("SOURCE_CHECK.json"))
    remaining = read_json(archive.read("REMAINING_QUEUE.json"))
    source_bindings = read_json(archive.read("SOURCE_BINDINGS.json"))
    check("decision and delivery hold exactly both requested identities with no acceptance or application",
          decision.get("group") == "rank9-ward-control6" and decision.get("accepted") is False and decision.get("applied") is False
          and decision.get("acceptedIds") == delivery.get("acceptedIds") == []
          and decision.get("appliedIds") == delivery.get("appliedIds") == []
          and decision.get("heldIds") == delivery.get("heldIds") == TARGETS
          and delivery.get("accepted") is False and delivery.get("applied") is False,
          {"accepted": delivery.get("acceptedIds"), "applied": delivery.get("appliedIds"), "held": delivery.get("heldIds")})
    decisions = {row.get("spellId"): row for row in decision.get("decisions", [])}
    decision_blockers = {sid: decisions.get(sid, {}).get("blockerIds") for sid in TARGETS}
    check("per-identity whole-spell blockers remain WC188-B01 and WC188-B02 with explicit missing witnesses",
          decision_blockers == {sid: [BLOCKERS[sid]] for sid in TARGETS}
          and all(decisions.get(sid, {}).get("decision") == "HOLD" and decisions.get(sid, {}).get("minimumMissingWitness") for sid in TARGETS)
          and set(delivery.get("blockerIds", [])) == set(BLOCKERS.values()),
          {"blockers": decision_blockers})
    check("authority is unchanged and Time/Fate6 is the exact next group",
          decision.get("authorityBefore") == decision.get("authorityAfter") == delivery.get("authority") == AUTHORITY
          and decision.get("nextPendingGroup") == delivery.get("nextPendingGroup") == NEXT,
          {"before": decision.get("authorityBefore"), "after": decision.get("authorityAfter"), "next": decision.get("nextPendingGroup")})
    check("semantic validation passes its data assertions while explicitly holding both acceptances",
          semantic.get("status") == "HOLD_FOR_BOTH_IDENTITY_ACCEPTANCES" and semantic.get("dataAssertions") == "PASS"
          and semantic.get("checkCount") == semantic.get("passedChecks") == 69 and semantic.get("failedAssertions") == [],
          {"status": semantic.get("status"), "checks": [semantic.get("passedChecks"), semantic.get("checkCount")], "failed": semantic.get("failedAssertions")})
    check("fresh source-binding checks all pass for the 91 bound current source files",
          len(source_check.get("checks", [])) == 594 and all(row.get("passed") is True for row in source_check.get("checks", []))
          and source_bindings.get("sourcePacket", {}).get("sha256") == digest(SOURCE_PACKET.read_bytes())["sha256"]
          and len(source_bindings.get("currentBindings", [])) == 91,
          {"checks": len(source_check.get("checks", [])), "failed": len([x for x in source_check.get("checks", []) if not x.get("passed")]), "bindings": len(source_bindings.get("currentBindings", []))})
    replay_counts = replay.get("counts", {})
    replay_rows = replay.get("caseResults", [])
    check("32 preserved cases replay all 1,472 events with no failure",
          replay.get("failures") == [] and replay_counts.get("caseFiles") == len(replay_rows) == 32
          and replay_counts.get("events") == 1472 and replay_counts.get("forwardOperations") == 2944
          and replay_counts.get("inverseOperations") == 2944 and replay_counts.get("checkCount") == 32842
          and replay_counts.get("failures") == 0 and all(row.get("numericReplay") == "PASS" for row in replay_rows),
          {"counts": replay_counts})
    check("case evidence statuses preserve 25 finite, five held and two superseded records",
          replay_counts.get("evidenceStatusCounts") == {"FINITE_STATIC_COMPONENT_EVIDENCE": 25, "HELD_NOT_POSITIVE_WITNESS": 5, "SUPERSEDED_HISTORICAL": 2}
          and counts.get("caseFiles") == 32 and counts.get("heldCaseRecords") == 5 and counts.get("supersededHistoricalCases") == 2,
          {"evidenceStatusCounts": replay_counts.get("evidenceStatusCounts")})
    check("prepared packet, delivery, independent audit and receipt are bound into Return281 inputs",
          archive.read("input_receipts/DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json") == SOURCE_DELIVERY.read_bytes()
          and read_json(archive.read("input_receipts/RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json")) == read_json(SOURCE_AUDIT.read_bytes())
          and read_json(archive.read("input_receipts/RANK9_WARDCONTROL6_PACKET281_RECEIPT.json")) == read_json(SOURCE_RECEIPT.read_bytes())
          and read_json(SOURCE_AUDIT.read_bytes()).get("status") == read_json(SOURCE_RECEIPT.read_bytes()).get("status") == "PASS"
          and read_json(SOURCE_AUDIT.read_bytes()).get("checkCount") == 17,
          {"packetAudit": read_json(SOURCE_AUDIT.read_bytes()).get("status"), "packetAuditChecks": read_json(SOURCE_AUDIT.read_bytes()).get("checkCount")})
    pending = read_json(PENDING.read_bytes())
    queue = read_json((BASE / "CURRENT_SPELL_QUEUE_281.json").read_bytes())
    ordered = remaining.get("orderedPendingIds", [])
    source_order = [sid for group in queue.get("currentPendingGroups", []) for sid in group.get("pendingIds", [])]
    check("exact 32-identity ordered remainder preserves Final Word and Return280 holds",
          remaining.get("count") == len(ordered) == 32 and set(ordered) == set(pending.get("pendingIds", []))
          and ordered == source_order
          and remaining.get("preservedFinalWord", {}).get("blockerId") == "DR217-B01"
          and remaining.get("preservedDefenseForm", {}).get("heldIds") == ["elemental-shell", "timeless-form", "invulnerable-sphere"]
          and remaining.get("nextPendingGroup") == NEXT,
          {"count": len(ordered), "matchesPendingSet": set(ordered) == set(pending.get("pendingIds", [])),
           "matchesQueueOrder": ordered == source_order, "next": remaining.get("nextPendingGroup")})
    current_q = read_json(archive.read("authority/CURRENT_SPELL_QUEUE_281.json"))
    current_h = read_json(archive.read("authority/CURRENT_HANDOFF_281.json"))
    current_p = read_json(archive.read("authority/CURRENT32_PENDING_IDENTITY_AUDIT_281.json"))
    check("embedded Packet281 authority inputs agree on 816/32 and the exact Ward/Control6 review scope",
          current_q.get("currentAuthority") == current_h.get("currentAuthority") == current_p.get("authority") == AUTHORITY
          and current_q.get("nextGroup") == current_h.get("nextGroup") == "rank9-ward-control6"
          and current_p.get("preparedNextGroup", {}).get("pendingIds") == TARGETS,
          {"queueAuthority": current_q.get("currentAuthority"), "handoffAuthority": current_h.get("currentAuthority"), "pendingAuthority": current_p.get("authority")})
    check("no canonical edits, GitHub changes, or downstream gates are claimed as completed",
          decision.get("canonicalChanged") is False and decision.get("githubChanged") is False
          and all(gate in decision.get("closedGates", []) for gate in ["runtime", "implementation", "human-play", "playtest", "balance", "cosmology", "domain-closure", "completion", "release"]),
          {"canonicalChanged": decision.get("canonicalChanged"), "githubChanged": decision.get("githubChanged"), "closedGates": decision.get("closedGates")})
    check("validation report agrees with published counts and records zero failed checks",
          validation.get("status") == "PASS_DATA_AND_PRESERVATION_WITH_SEMANTIC_HOLDS" and validation.get("failedChecks") == 0
          and validation.get("counts") == counts and counts.get("sourceChecks") == 594
          and counts.get("replayPreservationAndClockChecks") == 32842 and counts.get("semanticAssertions") == 69,
          {"status": validation.get("status"), "failedChecks": validation.get("failedChecks"), "counts": counts})

failures = [row for row in checks if not row["passed"]]
report = {"id": "RANK9-WARDCONTROL6-RETURN281-INDEPENDENT-AUDIT",
          "checkedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL",
          "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_hash},
          "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_hash},
          "authority": delivery.get("authority"), "acceptedIds": delivery.get("acceptedIds"),
          "appliedIds": delivery.get("appliedIds"), "heldIds": delivery.get("heldIds"),
          "blockerIds": delivery.get("blockerIds"), "nextPendingGroup": delivery.get("nextPendingGroup"),
          "checkCount": len(checks), "passedChecks": len(checks) - len(failures),
          "failedChecks": len(failures), "checks": checks,
          "scopeLimitation": "Independently verifies the sealed package, source/authority bindings, replay claims and Director decision fields; the game-rule adjudication remains the Director's ruling."}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9-WARDCONTROL6-RETURN281-RECEIPT", "status": report["status"],
           "archive": report["archive"], "deliveryManifest": report["deliveryManifest"],
           "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())},
           "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures),
           "scopeLimitation": report["scopeLimitation"]}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks) - len(failures),
                  "failedChecks": len(failures), "failures": failures, "archive": report["archive"],
                  "heldIds": delivery.get("heldIds"), "next": delivery.get("nextPendingGroup")}, ensure_ascii=False, indent=2))
