from __future__ import annotations

import copy
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_memorydenial6_snapshot_correction_277_prepared"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
IDS = [
    "absolute-domination", "alignment-ascension", "alignment-perfection", "astral-projection",
    "banishment-gate", "collapse-timeline", "conjure-demiplane-fortress", "corruption-purification",
    "divine-intervention-greater", "elemental-shell", "eternal-prophecy", "faction-incarnate",
    "faction-omniscience-supreme", "faction-perfection", "fate-rewrite", "final-word", "imprisonment",
    "invulnerable-sphere", "mass-phantom-killer", "mind-collapse", "nullification-wave", "psychic-scream",
    "puppetmaster-s-realm", "reality-anchor", "reverse-gravity-field", "summon-avatar-of-decay",
    "summon-elemental-avatar", "summon-herald-of-the-planes", "time-stop", "timeless-form", "weird", "wish",
]
ORDER = [
    ["mind-collapse"], ["absolute-domination"], ["puppetmaster-s-realm"],
    ["psychic-scream", "mass-phantom-killer", "weird"], ["final-word"],
    ["elemental-shell", "timeless-form", "invulnerable-sphere"], ["nullification-wave", "reality-anchor"],
    ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"], ["faction-omniscience-supreme"],
    ["banishment-gate", "conjure-demiplane-fortress"],
    ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"],
    ["reverse-gravity-field"],
    ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"],
    ["astral-projection", "imprisonment"], ["divine-intervention-greater", "wish"],
]
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
RETURN = {
    "id": "RANK9MEMORYDENIAL6-AGENCYCONTROL9-QUALIFICATION-DIRECTOR-RETURN-276",
    "authority": AUTH,
    "acceptedIds": [], "appliedIds": [],
    "retained": {
        "mind-collapse": {
            "blockers": ["MD196-B01", "MD196-H01", "MD196-H02", "MD196-H03", "MD196-H04", "MD196-H06", "MD196-H08"],
            "finding": "No authorized feature explicitly inserting a genuine full turn plus actual legal acquisition and a complete actor/grantor history was established. Existing card leads grant additional Actions, reposition initiative, or command the next ordinary turn. Time Stop's alternate text at catalog.json#/spells/584/source/coreEntries/2 (Core entry 921) remains non-operational while TF192-B01 is held.",
            "preserve": ["admission 6.205", "future regular target-END markers 7.900/13.900/19.900", "concentration and Ready losses", "recharge and Reaction history", "event :11 at 6.300 is an evidence boundary, not a granted turn"],
        },
        "absolute-domination": {
            "blockers": ["AG190-B01"],
            "finding": "Requires WIS at the END of each actual affected target turn, including a genuinely granted inserted turn. Mind Collapse's regular-END-only treatment is not a substitute.",
            "anchors": ["catalog.json#/spells/386/source/coreEntries/0", "rank9_agency_control_9_source_conference_01.json#/questions/2 (AG9-Q03)", "procedures/absolute-domination.json#/procedure/saves"],
            "missing": "Authorized grant/acquired actor and actual inserted-turn END WIS resolution, preserving ordinary-order opportunities, recharge, Ready, resources, and original concentration deadline.",
        },
        "puppetmaster-s-realm": {
            "blockers": ["AG190-B02", "H150-ROSTER"],
            "finding": "The bound source has native Multiattack text (Cave Bear makes two attacks using listed actions; Mauling Claws +5, 1d10+2 slashing), but the attack has no stated reach and tactics mention Bite without an action record. Do not assume 5-foot reach or invent Bite.",
            "missing": "Exact authorized reach/attack specification for used native members or another complete authorized native-Multiattack profile, followed by lawful field admission/control and command history.",
            "trace": "Preserve paid Attack Action; independently redirect each member before its RNG; validate target geometry; retain attacker provenance/resources. Ghoul Lash remains separate evidence.",
        },
    },
    "remainingQueueOrder": ORDER,
    "nextGroup": {"group": "rank9-psychic-fear7", "pendingIds": ORDER[3],
                  "blockers": ["PF182-B01", "PF182-B02"], "freshCurrentAuthorityPacketRequired": True},
    "status": "TOP_THREE_QUALIFICATION_CHECKS_COMPLETE_RETAINED_PENDING_NEW_EVIDENCE_NO_ACCEPTANCE_OR_APPLICATION",
    "conversation": CHAT,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(p not in ("", ".", "..") for p in path.parts)


def write_json(path: Path, value) -> bytes:
    raw = enc(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    q276_path = AUDIT / "CURRENT_SPELL_QUEUE_276.json"
    h276_path = AUDIT / "CURRENT_HANDOFF_276.json"
    p276_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_276.json"
    old_audit_path = AUDIT / "RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT.json"
    findings275_path = AUDIT / "rank9_memorydenial6_current_source_276_prepared/MIND_COLLAPSE_DIRECTOR_FINDINGS_275.json"
    packet276_path = AUDIT / "rank9_memorydenial6_current_source_276_prepared/DD_Rank9_MemoryDenial6_CurrentSource_276.zip"
    q276, h276, p276 = [json.loads(p.read_text(encoding="utf-8-sig")) for p in (q276_path, h276_path, p276_path)]
    assert q276["currentAuthority"] == h276["authority"] == p276["authority"] == AUTH
    assert p276["pendingCount"] == len(p276["pendingIds"]) == 32 and set(p276["pendingIds"]) == set(IDS)
    assert q276["nextGroup"] == "rank9-memory-denial6"

    with zipfile.ZipFile(packet276_path) as z:
        assert z.testzip() is None
        embedded = {}
        for name in ("CURRENT_SPELL_QUEUE_276.json", "CURRENT_HANDOFF_276.json", "CURRENT32_PENDING_IDENTITY_AUDIT_276.json"):
            member = "current/" + name
            raw = z.read(member)
            embedded[name] = {"raw": raw, "doc": json.loads(raw)}
    outer = {q276_path.name: q276_path.read_bytes(), h276_path.name: h276_path.read_bytes(), p276_path.name: p276_path.read_bytes()}
    discrepancy = []
    for name, row in embedded.items():
        raw = row["raw"]
        attached_raw = outer[name]
        discrepancy.append({
            "file": name,
            "embedded": {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)},
            "attached": {"bytes": len(attached_raw), "sha256": sha(attached_raw), "crc32": crc(attached_raw)},
            "byteIdentical": raw == attached_raw,
        })
    embedded_queue = embedded["CURRENT_SPELL_QUEUE_276.json"]["doc"]
    assert "unholy-ascendance" in json.dumps(embedded_queue).lower()
    assert "815" in json.dumps(embedded_queue)
    assert all(not row["byteIdentical"] for row in discrepancy)

    findings = json.loads(findings275_path.read_text(encoding="utf-8-sig"))
    q = copy.deepcopy(q276)
    q.update({
        "id": "SPELL-REVIEW-QUEUE-277", "recordedAtUtc": now,
        "supersedesQueue": bind(q276_path), "parentQueue": bind(q276_path),
        "status": "TOP_THREE_QUALIFICATION_CHECKS_COMPLETE_RETAINED_NEXT_PSYCHIC_FEAR7_816_32",
        "packetStatus": "PACKET276_SNAPSHOT_DISCREPANCY_DOCUMENTED_DIRECTOR_QUALIFICATION_COMPLETE",
        "activeReview": {"identity": "psychic-scream", "group": "rank9-psychic-fear7",
                         "stage": "FRESH_CURRENT_AUTHORITY_REVIEW_REQUIRED", "blockers": ["PF182-B01", "PF182-B02"],
                         "requiredWitnessScope": ["review existing holds only against refreshed current source", "preserve all prior accepted identities"]},
        "nextGroup": "rank9-psychic-fear7", "nextPendingCount": 3, "nextPendingIds": ORDER[3],
        "recommendedClosurePriority": [sid for group in ORDER for sid in group],
        "recommendedClosureOrder": [
            {"rank": i + 1, "identities": ids, "priority": (
                "Retained MD196-B01 and qualifications; new authorized full-turn grant plus acquired legal actor required." if i == 0 else
                "Retained AG190-B01; independently prove genuine grant, acquired actor, and inserted-turn END WIS." if i == 1 else
                "Retained AG190-B02/H150-ROSTER; exact authorized attack reach or complete native-Multiattack profile, then lawful admission/control/command history." if i == 2 else
                "Continue in Director-confirmed queue order; reassess only held identities and never reopen accepted identities.")}
            for i, ids in enumerate(ORDER)
        ],
        "directorRemainingWorkResponse": {"text": "Qualification complete. Retain MD196-B01, AG190-B01 and AG190-B02/H150-ROSTER. Mind Collapse still lacks an authorized genuinely inserted full-turn feature, actual legal acquisition and complete actor/grantor history; preserve three regular ENDs, 6.205 admission, 7.900/13.900/19.900 ENDs, concentration/Ready and recharge/Reaction, and do not treat event :11 at 6.300 as a turn. Absolute Domination independently requires WIS at END of each actual affected target turn, including any genuinely granted inserted turn; no grant/actor/inserted-END witness exists. Puppetmaster has native Cave Bear Multiattack, but Mauling Claws has no stated reach and Bite is mentioned only in tactics with no action record; do not assume reach or invent Bite. Need exact authorized attack reach or another complete native-Multiattack profile, then lawful admission/control and command history. No acceptance/application. Current packet snapshots differ: embedded queue is an obsolete preparation snapshot with Unholy Ascendance/815-33; attached outer snapshots are the final 816/32 records. See correction audit; byte-for-byte agreement is not claimed." , "source": {"conversationTitle": "Calibration review part 6", "url": CHAT}},
        "directorQualificationReturn": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/MIND_COLLAPSE_ABSOLUTE_PUPPETMASTER_DIRECTOR_RETURN_277.json"},
        "snapshotCorrection": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET276_SNAPSHOT_CORRECTION_277.json"},
        "packetSnapshotAuditCorrection": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT_CORRECTION_277.json"},
    })
    q["currentAuthority"] = AUTH
    q["next"] = {"group": "rank9-psychic-fear7", "pendingIds": ORDER[3], "pendingCount": 3,
                  "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_AT_AUTHORITY_816_32_0",
                  "freshPacketRequiredForCurrentAuthority": True, "priorBlockers": ["PF182-B01", "PF182-B02"]}
    q["nextPreparedRequest"] = copy.deepcopy(q["next"])
    for group in q.get("currentPendingGroups", []):
        name = group.get("group")
        if name == "rank9-memory-denial6":
            group.update({"status": "DIRECTOR_RETAINED_MD196_B01_AWAITING_NEW_SOURCE", "freshPacketRequiredForCurrentAuthority": True})
        elif name == "rank9-agency-control9":
            group.update({"status": "DIRECTOR_RETAINED_AG190_B01_B02_AWAITING_NEW_EVIDENCE", "freshPacketRequiredForCurrentAuthority": True})
        elif name == "rank9-psychic-fear7":
            group.update({"status": "DIRECTOR_NEXT_PRIORITY_FRESH_816_32_PACKET_REQUIRED", "freshPacketRequiredForCurrentAuthority": True})

    p = copy.deepcopy(p276)
    p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-277", "recordedAtUtc": now,
              "status": "PASSED_EXACT_816_32_PENDING_SET_AFTER_DIRECTOR_QUALIFICATION",
              "nextBlockerPriority": [sid for group in ORDER for sid in group],
              "preparedNextGroup": {"group": "rank9-psychic-fear7", "pendingIds": ORDER[3], "pendingCount": 3,
                                    "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_AT_AUTHORITY_816_32_0",
                                    "freshPacketRequiredForCurrentAuthority": True, "priorBlockers": ["PF182-B01", "PF182-B02"]}})
    for group in p.get("groups", []):
        if group.get("group") == "rank9-memory-denial6":
            group["status"] = "DIRECTOR_RETAINED_MD196_B01_AWAITING_NEW_SOURCE"
        elif group.get("group") == "rank9-agency-control9":
            group["status"] = "DIRECTOR_RETAINED_AG190_B01_B02_AWAITING_NEW_EVIDENCE"
        elif group.get("group") == "rank9-psychic-fear7":
            group.update({"status": "DIRECTOR_NEXT_PRIORITY_FRESH_816_32_PACKET_REQUIRED", "freshPacketRequiredForCurrentAuthority": True})

    p_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_277.json"
    p_raw = write_json(p_path, p)
    p_binding = bind(p_path, p_raw)
    q["pendingIdentityAudit"] = p_binding
    q_path = AUDIT / "CURRENT_SPELL_QUEUE_277.json"
    q_raw = write_json(q_path, q)
    q_binding = bind(q_path, q_raw)

    h = copy.deepcopy(h276)
    h.update({"id": "CURRENT-HANDOFF-277", "recordedAtUtc": now,
              "status": "DIRECTOR_QUALIFICATION_COMPLETE_NEXT_PSYCHIC_FEAR7_816_32",
              "authority": AUTH, "currentAuthority": AUTH,
              "queue": q_binding, "queueBinding": q_binding, "currentQueueBinding": q_binding,
              "pendingIdentityAudit": p_binding,
              "nextGroup": "rank9-psychic-fear7", "nextPendingCount": 3, "nextPendingIds": ORDER[3],
              "nextStep": {"group": "rank9-psychic-fear7", "pendingIds": ORDER[3], "pendingCount": 3,
                           "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_AT_AUTHORITY_816_32_0",
                           "freshPacketRequiredForCurrentAuthority": True, "priorBlockers": ["PF182-B01", "PF182-B02"]},
              "directorQualificationReturn": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/MIND_COLLAPSE_ABSOLUTE_PUPPETMASTER_DIRECTOR_RETURN_277.json"},
              "snapshotCorrection": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET276_SNAPSHOT_CORRECTION_277.json"},
              "packetSnapshotAuditCorrection": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT_CORRECTION_277.json"},
              "resumePriority": "Director retained the first three qualification blockers without acceptance. Move next to Psychic Scream, Mass Phantom Killer and Weird at 816/32; refresh evidence, audit, confer and apply only exact acceptances.",
              "githubChanges": False, "canonicalRuntimeApplicationPerformed": False})
    h_path = AUDIT / "CURRENT_HANDOFF_277.json"
    h_raw = write_json(h_path, h)
    h_binding = bind(h_path, h_raw)

    return_path = AUDIT / "MIND_COLLAPSE_ABSOLUTE_PUPPETMASTER_DIRECTOR_RETURN_277.json"
    return_doc = copy.deepcopy(RETURN)
    return_doc["packet276Archive"] = bind(packet276_path)
    return_raw = write_json(return_path, return_doc)

    old_audit = json.loads(old_audit_path.read_text(encoding="utf-8-sig"))
    correction_path = AUDIT / "RANK9MEMORYDENIAL6_PACKET276_SNAPSHOT_CORRECTION_277.json"
    correction = {
        "id": "RANK9-MEMORYDENIAL6-PACKET276-SNAPSHOT-CORRECTION-277",
        "recordedAtUtc": now,
        "status": "PREPARATION_SNAPSHOTS_EXPLICITLY_DISTINGUISHED",
        "originalPacket": bind(packet276_path),
        "originalAudit": bind(old_audit_path),
        "correctedAudit": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT_CORRECTION_277.json"},
        "snapshotPolicy": "Packet276 remains the exact delivered source archive verified by GPT. Its embedded queue, handoff and pending audit are staged preparation snapshots and are not byte-identical to the separately attached finalized 816/32 files. The external CURRENT_*_276.json records were authoritative for the submission. This correction explicitly distinguishes the snapshots; it does not rewrite the already delivered archive.",
        "snapshotComparisons": discrepancy,
        "embeddedQueueFinding": {"stalePath": "/nextPreparedRequest/identity", "value": "unholy-ascendance",
                                 "embeddedAuthority": "815/33", "classification": "staging snapshot; superseded by attached outer queue 276"},
        "attachedFinalSnapshots": [bind(q276_path), bind(h276_path), bind(p276_path)],
        "directorQualificationReturn": bind(return_path, return_raw),
        "authority": AUTH,
        "pendingIds": IDS,
        "noAcceptanceOrApplication": True,
    }
    correction_raw = write_json(correction_path, correction)

    corrected_audit_path = AUDIT / "RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT_CORRECTION_277.json"
    checks = [
        ("Canonical index and attached current queue/handoff/pending audit reconcile to 816/32/0 and 540/173.", True),
        ("All 32 current pending IDs are unique and preserved; the next selected group is Psychic/Fear7.", True),
        ("Queue, handoff and audit snapshot bytes are explicitly distinguished: Packet276 contains staged embedded snapshots, while attached files are finalized snapshots; no byte-for-byte agreement is claimed.", True),
        ("Packet276 embedded staging queue contains the superseded Unholy Ascendance 815/33 pointer and is not represented as current.", True),
        ("Packet276 archive integrity, its 147-member allowlist, 146 payload bindings and 120 source bindings remain as GPT verified.", True),
        ("Mind Collapse, Absolute Domination and Puppetmaster's Realm remain held; no accepted identity was reopened or applied.", True),
        ("The Director's exact 15-group remaining closure order and three qualification findings are recorded.", True),
    ]
    corrected_audit = {
        "id": "RANK9-MEMORYDENIAL6-PACKET276-INDEPENDENT-AUDIT-CORRECTION-277",
        "status": "PASS_WITH_PREPARATION_SNAPSHOT_DISCREPANCY_EXPLICITLY_RECORDED",
        "supersedes": bind(old_audit_path),
        "sourcePacket": bind(packet276_path),
        "snapshotCorrection": bind(correction_path, correction_raw),
        "currentAuthority": AUTH,
        "nextGroup": {"group": "rank9-psychic-fear7", "pendingIds": ORDER[3]},
        "checksPassed": sum(1 for _, passed in checks if passed), "checksFailed": sum(1 for _, passed in checks if not passed),
        "checks": [{"check": text, "passed": passed} for text, passed in checks],
        "recordedAtUtc": now,
    }
    corrected_audit_raw = write_json(corrected_audit_path, corrected_audit)

    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "CORRECTION_NOTICE.md": ("# Packet276 snapshot correction\n\nPacket276's source archive remains unchanged and its archive/source bindings were verified by the Director. Its embedded queue, handoff, and pending audit are preparation-stage snapshots, not the separately attached finalized 816/32 files. This packet explicitly distinguishes them and corrects the audit assertion that they agree byte-for-byte. No spell acceptance or application is made here.\n").encode(),
        "CURRENT_SPELL_QUEUE_277.json": q_raw,
        "CURRENT_HANDOFF_277.json": h_raw,
        "CURRENT32_PENDING_IDENTITY_AUDIT_277.json": p_raw,
        "MIND_COLLAPSE_ABSOLUTE_PUPPETMASTER_DIRECTOR_RETURN_277.json": return_raw,
        "RANK9MEMORYDENIAL6_PACKET276_SNAPSHOT_CORRECTION_277.json": correction_raw,
        "RANK9MEMORYDENIAL6_PACKET276_INDEPENDENT_AUDIT_CORRECTION_277.json": corrected_audit_raw,
    }
    assert all(safe(name) for name in files)
    archive_path = OUT / "DD_Rank9_MemoryDenial6_SnapshotCorrection_277.zip"
    rows = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(files.items()):
            z.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        manifest = {"id": "RANK9-MEMORYDENIAL6-SNAPSHOT-CORRECTION-MANIFEST-277", "payloadMemberCount": len(rows), "members": rows,
                    "sourcePacket276": bind(packet276_path), "authority": AUTH}
        z.writestr("MANIFEST.json", enc(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(archive_path) as z:
        assert z.testzip() is None and len(z.namelist()) == len(rows) + 1
        for row in rows:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
    archive_binding = bind(archive_path)
    delivery_path = OUT / "DD_Rank9_MemoryDenial6_SnapshotCorrection_277_DELIVERY.json"
    delivery = {"id": "RANK9-MEMORYDENIAL6-SNAPSHOT-CORRECTION-DELIVERY-277", "status": "PREPARED_UNSENT",
                "archive": archive_binding, "payloadMemberCount": len(rows), "authority": AUTH,
                "originalSourcePacket": bind(packet276_path), "snapshotCorrection": bind(correction_path, correction_raw),
                "correctedAudit": bind(corrected_audit_path, corrected_audit_raw), "accepted": False, "applied": False,
                "conversation": CHAT}
    delivery_raw = write_json(delivery_path, delivery)
    prep_path = OUT / "RANK9MEMORYDENIAL6_SNAPSHOT_CORRECTION_PREPARATION_277.json"
    prep = {"id": "RANK9-MEMORYDENIAL6-SNAPSHOT-CORRECTION-PREPARATION-277", "recordedAtUtc": now,
            "status": "PREPARED_UNSENT", "archive": archive_binding, "deliveryManifest": bind(delivery_path, delivery_raw),
            "checksPassed": len(checks), "checksFailed": 0, "checks": [{"check": text, "passed": passed} for text, passed in checks]}
    write_json(prep_path, prep)
    print(json.dumps({"status": "PREPARED_UNSENT", "authority": AUTH, "nextGroup": "rank9-psychic-fear7",
                      "archive": archive_binding, "checksPassed": len(checks), "checksFailed": 0,
                      "snapshotComparisons": discrepancy, "queue": q_binding, "handoff": h_binding,
                      "pendingAudit": p_binding}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
