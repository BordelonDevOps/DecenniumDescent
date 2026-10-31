#!/usr/bin/env python3
"""Prepare a current-source, one-identity Imprisonment Director packet."""
from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_imprisonment_review_341_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_Imprisonment_Review341.zip"
DELIVERY = OUT / "DD_Rank9_Imprisonment_Review341_DELIVERY.json"
MARKER = OUT / "PREPARATION_AUDIT_341.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_340.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_340.json"
HANDOFF = A / "CURRENT_HANDOFF_340.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_340.md"
PREVIOUS_ZIP = A / "rank9_projectionconfinement2_return232_received/DD_Rank9_ProjectionConfinement2_Director_Return232_HELD.zip"
PREVIOUS_DELIVERY = A / "rank9_projectionconfinement2_return232_received/DD_Rank9_ProjectionConfinement2_Director_Return232_HELD_DELIVERY.json"
PREVIOUS_AUDIT = A / "RANK9PROJECTIONCONFINEMENT2_RETURN232_INDEPENDENT_AUDIT.json"
PREVIOUS_RECEIPT = A / "RANK9PROJECTIONCONFINEMENT2_RETURN232_RECEIPT.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"

SPELL = "imprisonment"
BLOCKER = "PC232-B02"
GROUP = "rank9-projection-confinement2"
AUTHORITY = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
SOURCE_PATHS = [
    "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "DescentReviewChanges/ReviewBible/docs/director-only/cosmology/PLANES_REVIEWED_01.md",
    "DescentReviewChanges/ReviewBible/docs/director-only/cosmology/EPILOGUE_RELIC_NULL_REVIEWED_01.md",
    "DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md",
    "DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md",
    "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/banishment_reviewed_04.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/damage_control_25_reviewed_10.json",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def binding(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def find_id(node, ident: str):
    if isinstance(node, dict):
        if node.get("id") == ident:
            return node
        for value in node.values():
            found = find_id(value, ident)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_id(value, ident)
            if found is not None:
                return found
    return None


def main() -> None:
    if OUT.exists() and any(p.is_file() for p in OUT.rglob("*")):
        raise RuntimeError(f"Refusing to overwrite existing packet directory: {OUT}")
    for path in (QUEUE, PENDING, HANDOFF, SNAPSHOT, PREVIOUS_ZIP, PREVIOUS_DELIVERY, PREVIOUS_AUDIT, PREVIOUS_RECEIPT, CATALOG, INDEX, CORE):
        if not path.is_file():
            raise FileNotFoundError(path)
    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index, core = load(CATALOG), load(INDEX), load(CORE)
    catalog_row = find_id(catalog, SPELL)
    index_row = find_id(index, SPELL)
    core_rows = [{"pointer": f"/spells/{i}", "row": row} for i, row in enumerate(core.get("spells", [])) if row.get("name") == "Imprisonment"]
    if catalog_row is None or index_row is None or len(core_rows) != 2:
        raise RuntimeError("Current Imprisonment catalog/index/Core rows are incomplete or ambiguous.")
    if catalog_row.get("operational") is not None or index_row.get("authoredStatus") != "pending-authored-procedure":
        raise RuntimeError("Imprisonment is no longer pending; refuse stale packet.")
    if queue.get("currentAuthority") != AUTHORITY or queue.get("next") != SPELL or queue.get("activeReview", {}).get("blockerIds") != [BLOCKER]:
        raise RuntimeError("Queue340 does not designate Imprisonment / PC232-B02.")
    if handoff.get("currentBlocker") != {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP}:
        raise RuntimeError("Handoff340 does not match the Director priority.")
    if pending.get("authority") != AUTHORITY or SPELL not in pending.get("pendingIds", []):
        raise RuntimeError("Current pending audit does not preserve Imprisonment at 823/25/0.")

    with ZipFile(PREVIOUS_ZIP) as old:
        old_delivery = load(PREVIOUS_DELIVERY)
        old_decision = json.loads(old.read("DIRECTOR_DECISION.json"))
        old_holds = json.loads(old.read("HOLD_REGISTER.json"))
        old_questions = json.loads(old.read("QUESTION_DISPOSITIONS.json"))
        old_qualifications = json.loads(old.read("QUALIFICATIONS.json"))
        if old.testzip() is not None:
            raise RuntimeError("Return232 archive failed CRC readback.")
    prior_decision = next((r for r in old_decision.get("perIdentityDecisions", []) if r.get("id") == SPELL), None)
    prior_blocker = next((r for r in old_holds.get("targetBlockers", []) if r.get("id") == BLOCKER), None)
    prior_questions = [r for r in old_questions if r.get("id") == "PC9-01" or r.get("id", "").startswith("IM9-")]
    if prior_decision is None or prior_decision.get("decision") != "HELD" or prior_decision.get("blockerIds") != [BLOCKER] or prior_blocker is None or prior_blocker.get("status") != "OPEN":
        raise RuntimeError("Prior sealed Imprisonment hold PC232-B02 is not intact.")
    if {r.get("id") for r in prior_questions} != {"PC9-01", *(f"IM9-{i}" for i in range(15, 25))} or len(old_qualifications) != 7:
        raise RuntimeError("Target question or qualification history is incomplete.")
    if old_delivery.get("heldIds") != ["astral-projection", "imprisonment"] or old_delivery.get("authority", {}).get("reviewedApplied") != 811:
        raise RuntimeError("Return232 historical decision did not match expected two-target hold.")

    # Bind Return340, which supplied this identity as the next Director priority.
    current_return = load(RECEIPT := A / "ASTRAL_PROJECTION_RETURN340_RECEIPT.json")
    current_audit = load(A / "ASTRAL_PROJECTION_RETURN340_INDEPENDENT_AUDIT.json")
    if not (
        current_return.get("id") == "ASTRAL-PROJECTION-RETURN340-RECEIPT"
        and current_return.get("decision") == "HOLD"
        and current_return.get("nextIdentity") == SPELL
        and current_return.get("nextBlockerIds") == [BLOCKER]
        and current_audit.get("status") == "PASS_RETURN340_SEALED_HOLD_PC232_B01"
        and current_audit.get("failed") == 0
        and current_audit.get("checkCount") == current_audit.get("passed")
    ):
        raise RuntimeError("Return340 independent receipt is not verified.")
    preserved = {
        "id": "IMPRISONMENT-REVIEW341-PRESERVED-HOLDS",
        "scope": "Only Imprisonment / PC232-B02 is adjudicated. No prior identity is reopened.",
        "returns336to340": [
            {"identity": sid, "blockers": blockers} for sid, blockers in sorted(queue.get("currentReturnBlockers", {}).items())
        ],
        "separatelyRetainedHolds": queue.get("separatelyRetainedHolds", []),
        "closedEvidenceFinding": "AFP211-E01 CLOSED",
        "astralProjectionReturn340": {"heldIds": ["astral-projection"], "archive": current_return.get("archive"), "delivery": current_return.get("delivery"), "audit": binding(A / "ASTRAL_PROJECTION_RETURN340_INDEPENDENT_AUDIT.json")},
        "return232HistoricalTargets": ["astral-projection", "imprisonment"],
        "rule": "Return232 is preserved as prior history; Return340 remains the current hold for Astral Projection. Do not re-adjudicate either here.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    PACKET.mkdir(parents=True, exist_ok=True)
    target_q = {
        "scope": SPELL,
        "records": prior_questions,
        "source": binding(PREVIOUS_ZIP),
        "note": "Prior target-specific questions plus shared PC9-01 are historical constraints only. They are not a decision on this current packet.",
    }
    inputs = {
        "00_CURRENT_AUTHORITY_AND_QUEUE_340.json": {
            "authority": AUTHORITY,
            "queue": binding(QUEUE),
            "pendingAudit": binding(PENDING),
            "handoff": binding(HANDOFF),
            "currentNext": {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP},
            "currentReturn340Receipt": binding(A / "ASTRAL_PROJECTION_RETURN340_RECEIPT.json"),
        },
        "01_CURRENT_IMPRISONMENT_CATALOG_ROW.json": catalog_row,
        "02_CURRENT_IMPRISONMENT_INDEX_ROW.json": index_row,
        "03_CURRENT_CORE_IMPRISONMENT_ROWS.json": {"source": binding(CORE), "rows": core_rows},
        "04_RETURN232_PRIOR_IMPRISONMENT_HOLD.json": {
            "historicalAuthorityOnly": old_decision.get("authority"),
            "priorDecision": prior_decision,
            "priorBlocker": prior_blocker,
            "archive": binding(PREVIOUS_ZIP),
            "delivery": binding(PREVIOUS_DELIVERY),
            "independentAudit": binding(PREVIOUS_AUDIT),
            "receipt": binding(PREVIOUS_RECEIPT),
            "scope": "Prior PC232-B02 HOLD only; current source files and current 823/25/0 authority control.",
        },
        "05_RETURN232_IMPRISONMENT_QUESTION_DISPOSITIONS.json": target_q,
        "06_RETURN232_QUALIFICATIONS.json": {"scope": SPELL, "records": old_qualifications, "priorRulingOnly": True},
        "07_CURRENT_PRESERVED_HOLDS_340.json": preserved,
        "08_CURRENT_SOURCE_BINDINGS_341.json": {"target": SPELL, "catalogRowMatchesCurrent": True, "indexRowMatchesCurrent": True, "coreRowCount": len(core_rows), "fullCurrentSources": []},
    }

    source_rows = []
    for i, rel in enumerate(SOURCE_PATHS):
        src = ROOT / rel
        if not src.is_file():
            raise FileNotFoundError(src)
        row = binding(src)
        row["packetMember"] = f"sources/{i:02d}_{src.name}"
        source_rows.append(row)
        dest = PACKET / row["packetMember"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
    inputs["08_CURRENT_SOURCE_BINDINGS_341.json"]["fullCurrentSources"] = source_rows

    for name, src in [
        ("CURRENT_SPELL_QUEUE_340.json", QUEUE),
        ("CURRENT25_PENDING_IDENTITY_AUDIT_340.json", PENDING),
        ("CURRENT_HANDOFF_340.json", HANDOFF),
        ("CURRENT_SPELL_REVIEW_SNAPSHOT_340.md", SNAPSHOT),
    ]:
        dest = PACKET / "context" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
    for name, value in inputs.items():
        save(PACKET / "input" / name, value)

    request = """# Director review request — Imprisonment / PC232-B02

Review Imprisonment only, one identity, as the next current Director priority after Return340. Current authority is 823 reviewed/applied, 25 pending and 0 accepted-unapplied (547 complete standalone procedures; 173 scoped interfaces). Historical Return232 authority 811/37/0 is not current. Preserve the two native school placements, the actual Cleric/Druid/Mage/Wizard class-school routes, rank 9, class level 17, base cost 26 RP, 1 action, 120 feet, V/S/F and Core Instantaneous initiation. School placement does not create class access.

Reassess PC232-B02 against the exact attached catalog, authored-index, Core and current source bindings. Return232 previously held for three connected but target-specific clusters: (1) a bounded, authorized menu of at least two meaningful entombment methods, with actual admitted creature/defense/resistance rules and each method's body-fit geometry, location, material or magical boundary; (2) for each method, the initiation-versus-persistent result lifecycle, needs, awareness/agency, physical or magical escape and outside rescue with real costs, barriers, tools/checks and source-owned release rules; (3) durable method-specific growth, attachments, partial suppression/resumption, collision, death/corpse/gear, recast and competing-source settlement without duplicate ownership or free resources. No method, material, dimension, defense, burial depth or component price is supplied by the short native promise “Entomb creature in various ways.”

The two existing Core rows retain Necromancy and Universal and state Action/120 feet/Instantaneous/V-S-F/26 RP. Their generic “Automatic or opposed as described” does not supply a specific defense check. The current spell is pending and non-operational. Do not turn Frozen Tomb's status, any wall/barrier, Maze, Sequester, Banishment, demiplane, Astral Projection, or other spell's destination, dimensions, conditions, materials, costs, duration, durability, or escape rules into Imprisonment modes. Comparators are boundaries only; a new Imprisonment-local rule may be recognized only if explicitly present in exact current target sources, with provenance.

The prior Return232 record is history, not a second approval or complete positive cast. Do not replay prior cases, infer witness events, or reopen Astral Projection / PC232-B01. Preserve the Return336-340 holds, their exact open contracts, all prior acceptances, and AFP211-E01 CLOSED. No canonical file changes, application, runtime execution, or unrelated adjudication are authorized.

If any native content or positive-use evidence remains missing, seal a focused one-identity HOLD with exact open contract IDs, source anchors, witness needs, unchanged 823/25/0 authority and the next priority from the current queue. A useful positive witness must show a legal paid cast against an actually defended eligible creature, failed resistance/admission, each selected entombment mode in use, and meaningful lawful escape or outside rescue with paid costs and full needs/clocks, growth, suppression/resumption, corpse/gear and competing-source branches. If exact current source rules and complete paid witnesses close every requirement, seal an exact one-identity ACCEPT and explicit application authorization for Imprisonment only; Codex will independently verify before any application. Attach a sealed ZIP and matching DELIVERY JSON.
"""
    request_path = OUT / "REQUEST_341.md"
    request_path.write_text(request, encoding="utf-8", newline="\n")

    packet_rows = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file() and path.name != "MEMBER_MANIFEST.json":
            data = path.read_bytes()
            packet_rows.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "IMPRISONMENT-REVIEW341-PACKET-MANIFEST", "payloadMemberCount": len(packet_rows), "members": packet_rows})

    zip_rows = [{"path": "REQUEST_341.md", "bytes": request_path.stat().st_size, "sha256": sha(request_path.read_bytes()), "crc32": crc(request_path.read_bytes())}]
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            zip_rows.append({"path": "packet/" + path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED, compresslevel=9) as z:
        z.write(request_path, "REQUEST_341.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                z.write(path, "packet/" + path.relative_to(PACKET).as_posix())
    raw = ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as z:
        if z.testzip() is not None or z.namelist() != [row["path"] for row in zip_rows]:
            raise RuntimeError("Review341 archive integrity or allowlist failed.")
        for row in zip_rows:
            data = z.read(row["path"])
            if (len(data), sha(data), crc(data)) != (row["bytes"], row["sha256"], row["crc32"]):
                raise RuntimeError("Review341 archive member mismatch: " + row["path"])

    delivery = {
        "id": "IMPRISONMENT-REVIEW341-DELIVERY",
        "reviewId": "Review341",
        "targetIds": [SPELL],
        "blockerIds": [BLOCKER],
        "authority": AUTHORITY,
        "acceptedIds": [],
        "appliedIds": [],
        "applicationAuthorizationRequestedOnlyIfExactSealedAcceptance": [SPELL],
        "decisionRequested": "current-source one-identity reassessment; no canonical mutation by Director",
        "archive": {"fileName": ARCHIVE.name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)},
        "archiveMemberCount": len(zip_rows),
        "members": zip_rows,
        "exactAllowlist": [row["path"] for row in zip_rows],
        "currentSourceBindings": source_rows,
        "priorReturn232ImprisonmentHold": binding(PREVIOUS_ZIP),
        "currentReturn340Receipt": binding(A / "ASTRAL_PROJECTION_RETURN340_RECEIPT.json"),
        "queueBinding": binding(QUEUE),
        "canonicalMutation": False,
        "priorCasesReplayed": False,
    }
    save(DELIVERY, delivery)
    checks = [
        {"id": "current-authority-and-director-next", "passed": queue.get("currentAuthority") == AUTHORITY and queue.get("next") == SPELL and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER]},
        {"id": "target-exact-catalog-index-core", "passed": catalog_row.get("id") == SPELL and index_row.get("id") == SPELL and len(core_rows) == 2 and index_row.get("authoredStatus") == "pending-authored-procedure"},
        {"id": "prior-target-hold-and-question-history", "passed": prior_decision.get("blockerIds") == [BLOCKER] and prior_blocker.get("id") == BLOCKER and len(prior_questions) == 11 and len(old_qualifications) == 7},
        {"id": "preserve-return340-and-all-holds", "passed": SPELL in pending.get("pendingIds", []) and "astral-projection" in queue.get("separatelyRetainedHolds", []) and current_return.get("heldIds") == ["astral-projection"] and current_audit.get("failed") == 0},
        {"id": "all-current-source-bindings", "passed": len(source_rows) == len(SOURCE_PATHS) and all(binding(ROOT / r["path"]) == {k:v for k,v in r.items() if k!="packetMember"} for r in source_rows)},
        {"id": "archive-integrity-and-binding", "passed": len(zip_rows) == len(set(r["path"] for r in zip_rows)) and len(raw) == delivery["archive"]["bytes"] and sha(raw) == delivery["archive"]["sha256"] and crc(raw) == delivery["archive"]["crc32"]},
    ]
    if not all(row["passed"] for row in checks):
        raise RuntimeError("Review341 preparation failed: " + json.dumps(checks))
    save(MARKER, {
        "id": "IMPRISONMENT-REVIEW341-PREPARATION-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS",
        "target": SPELL,
        "blocker": BLOCKER,
        "authority": AUTHORITY,
        "sourceCount": len(source_rows),
        "memberCount": len(zip_rows),
        "checks": checks,
        "checkCount": len(checks),
        "passed": len(checks),
        "failed": 0,
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **delivery["archive"]},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())},
        "canonicalMutation": False,
    })
    print(json.dumps({"status":"PASS", "checks":len(checks), "target":SPELL, "blocker":BLOCKER, "sources":len(source_rows), "members":len(zip_rows), "archiveBytes":len(raw), "archiveSha256":sha(raw), "delivery":str(DELIVERY)}, indent=2))


if __name__ == "__main__":
    main()
