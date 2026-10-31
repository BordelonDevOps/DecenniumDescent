#!/usr/bin/env python3
"""Prepare a current-source, one-identity Astral Projection Director packet."""
from __future__ import annotations

import hashlib
import json
import shutil
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_astral_projection_review_340_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_AstralProjection_Review340.zip"
DELIVERY = OUT / "DD_Rank9_AstralProjection_Review340_DELIVERY.json"
MARKER = OUT / "PREPARATION_AUDIT_340.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_339.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_339.json"
HANDOFF = A / "CURRENT_HANDOFF_339.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_339.md"
PREVIOUS_RETURN = A / "rank9_projectionconfinement2_return288_received/DD_Rank9_ProjectionConfinement2_Director_Return288_HELD.zip"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
SPELL = "astral-projection"
BLOCKER = "PC232-B01"
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
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def find_id(node, ident: str):
    if isinstance(node, dict):
        if node.get("id") == ident:
            return node
        for value in node.values():
            result = find_id(value, ident)
            if result is not None:
                return result
    elif isinstance(node, list):
        for value in node:
            result = find_id(value, ident)
            if result is not None:
                return result
    return None


def named_core_rows(node, name: str, result=None):
    result = [] if result is None else result
    if isinstance(node, dict):
        if node.get("name") == name:
            result.append(node)
        for value in node.values():
            named_core_rows(value, name, result)
    elif isinstance(node, list):
        for value in node:
            named_core_rows(value, name, result)
    return result


def main() -> None:
    if OUT.exists() and any(path.is_file() for path in OUT.rglob("*")):
        raise RuntimeError(f"Refusing to overwrite existing packet directory: {OUT}")
    if not PREVIOUS_RETURN.is_file():
        raise FileNotFoundError("Prior sealed Return288 archive is missing.")
    OUT.mkdir(parents=True, exist_ok=True)
    PACKET.mkdir(parents=True, exist_ok=True)
    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index, core = load(CATALOG), load(INDEX), load(CORE)
    catalog_row, index_row = find_id(catalog, SPELL), find_id(index, SPELL)
    core_rows = named_core_rows(core, "Astral Projection")
    if catalog_row is None or index_row is None or len(core_rows) != 4:
        raise RuntimeError("Current Astral Projection catalog/index/Core rows are incomplete or ambiguous.")
    if catalog_row.get("operational") is not None or index_row.get("authoredStatus") != "pending-authored-procedure":
        raise RuntimeError("Astral Projection current status changed; do not prepare a stale packet.")
    if queue.get("currentAuthority") != AUTHORITY or queue.get("next") != SPELL or queue.get("activeReview", {}).get("blockerIds") != [BLOCKER]:
        raise RuntimeError("Queue339 does not designate Astral Projection / PC232-B01.")
    if handoff.get("currentBlocker") != {"identity": SPELL, "blockerId": BLOCKER, "group": "rank9-projection-confinement2"}:
        raise RuntimeError("Handoff339 blocker does not match the Director priority.")

    with ZipFile(PREVIOUS_RETURN) as old_zip:
        old_decision = json.loads(old_zip.read("DIRECTOR_DECISION.json"))
        old_holds = json.loads(old_zip.read("HOLD_REGISTER.json"))
        old_questions = json.loads(old_zip.read("QUESTION_DISPOSITIONS.json"))
        old_qualifications = json.loads(old_zip.read("QUALIFICATIONS.json"))
        old_sources = json.loads(old_zip.read("SOURCE_EVIDENCE_FINDINGS.json"))
    previous_spell_decision = next(row for row in old_decision.get("perIdentityDecisions", []) if row.get("id") == SPELL)
    previous_blocker = next(row for row in old_holds.get("targetBlockers", []) if row.get("id") == BLOCKER)
    target_questions = [
        row for row in old_questions
        if row.get("id") == "PC9-01" or row.get("id", "").startswith("AP9-") or row.get("id", "").startswith("PROJECTION129-ADD")
    ]
    qualification_rows = [row for row in old_qualifications if row.get("id", "").startswith("PC232-Q")]
    if previous_spell_decision.get("decision") != "HOLD" or previous_spell_decision.get("accepted") is not False or previous_spell_decision.get("applied") is not False:
        raise RuntimeError("The prior Astral Projection decision is not a sealed hold.")
    if previous_spell_decision.get("blockerIds") != [BLOCKER] or previous_blocker.get("status") != "OPEN":
        raise RuntimeError("Prior PC232-B01 blocker record is missing or changed.")
    if len(target_questions) != 15 or len(qualification_rows) != 7:
        raise RuntimeError("The target-scoped prior question/qualification record is incomplete.")

    current_holds = {
        "id": "ASTRAL-PROJECTION-REVIEW340-PRESERVED-HOLDS",
        "scope": "No prior identity is reopened or adjudicated by this one-target packet.",
        "return336": {"heldIds": ["alignment-perfection"], "evidenceFinding": "AFP211-E01 CLOSED"},
        "return337": {"heldIds": ["faction-incarnate"], "evidenceFinding": "AFP211-E01 CLOSED"},
        "return338": {"heldIds": ["faction-perfection"], "openContracts": ["AFP338-W01", "AFP338-W02"]},
        "return339": {"heldIds": ["corruption-purification"], "openContracts": ["AFP339-W01", "AFP339-W02", "AFP339-W03"], "evidenceFinding": "AFP211-E01 CLOSED"},
        "queue339SeparatelyRetainedHolds": queue.get("separatelyRetainedHolds", []),
        "rule": "Preserve exact prior holds, open contracts, prior acceptances and AFP211-E01 closed; do not copy any other identity into this review.",
    }
    input_data = {
        "00_CURRENT_AUTHORITY_AND_QUEUE_339.json": {
            "authority": AUTHORITY,
            "queue": binding(QUEUE),
            "pendingAudit": binding(PENDING),
            "handoff": binding(HANDOFF),
            "currentNext": {"identity": SPELL, "blockerId": BLOCKER, "group": "rank9-projection-confinement2"},
        },
        "01_CURRENT_ASTRAL_PROJECTION_CATALOG_ROW.json": catalog_row,
        "02_CURRENT_ASTRAL_PROJECTION_INDEX_ROW.json": index_row,
        "03_CURRENT_CORE_ASTRAL_PROJECTION_ROWS.json": {
            "source": binding(CORE),
            "rows": [{"pointer": f"/spells/{i}", "row": row} for i, row in enumerate(core.get("spells", [])) if row.get("name") == "Astral Projection"],
        },
        "04_RETURN288_PRIOR_ASTRAL_HOLD.json": {
            "historicalAuthorityOnly": old_decision.get("authority"),
            "priorDecision": previous_spell_decision,
            "priorBlocker": previous_blocker,
            "priorArchive": binding(PREVIOUS_RETURN),
            "currentSourceFinding": old_sources.get("astral"),
            "scope": "Historical blocker and audit boundary only; current source files are attached separately and control current facts.",
        },
        "05_RETURN288_PRIOR_ASTRAL_QUESTION_DISPOSITIONS.json": {
            "scope": SPELL,
            "records": target_questions,
            "note": "Prior selected constraints are not automatic acceptance. Only Astral Projection/AP9 and shared PC9-01 records are included; Imprisonment was not reviewed here.",
        },
        "06_RETURN288_PRIOR_ASTRAL_QUALIFICATIONS.json": {
            "scope": SPELL,
            "records": qualification_rows,
            "priorRulingOnly": True,
        },
        "07_CURRENT_PRESERVED_HOLDS_339.json": current_holds,
        "08_CURRENT_SOURCE_BINDINGS_340.json": {
            "target": SPELL,
            "catalogRowMatchesCurrent": True,
            "indexRowMatchesCurrent": True,
            "coreRowCount": len(core_rows),
            "fullCurrentSources": [],
            "priorSourceBindingsAreHistoricalOnly": True,
        },
    }

    source_rows = []
    for index_num, rel in enumerate(SOURCE_PATHS):
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(f"Missing current source: {rel}")
        row = binding(path)
        row["packetMember"] = f"sources/{index_num:02d}_{path.name}"
        source_rows.append(row)
        dest = PACKET / row["packetMember"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
    input_data["08_CURRENT_SOURCE_BINDINGS_340.json"]["fullCurrentSources"] = source_rows

    for name, source in [
        ("CURRENT_SPELL_QUEUE_339.json", QUEUE),
        ("CURRENT25_PENDING_IDENTITY_AUDIT_339.json", PENDING),
        ("CURRENT_HANDOFF_339.json", HANDOFF),
        ("CURRENT_SPELL_REVIEW_SNAPSHOT_339.md", SNAPSHOT),
    ]:
        dest = PACKET / "context" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    for filename, value in input_data.items():
        save(PACKET / "input" / filename, value)

    request = """# Director review request — Astral Projection / PC232-B01

Review only Astral Projection, one identity, under the current Director-prioritized queue 339. Current authority is 823 reviewed/applied, 25 pending and 0 accepted-unapplied (547 complete standalone procedures; 173 scoped interfaces). The historical Return288 authority of 816/32 is not current. Preserve the four native school placements and actual class-school routes, rank 9, class level 17, base cost 26 RP, 1 action, 120 feet, V/S/F and Core Instantaneous initiation. Do not drop a school placement or infer additional class access.

Reassess PC232-B01 against the attached exact current catalog, authored index, Core and full source documents. Return288 previously held for three missing clusters: (1) an authorized operational Astral destination/site with actual arrival selection, body-fit, support/environment, useful legal movement/action and endpoint restrictions; (2) an explicit projection relation for the original and projected bodies, anatomy, location, awareness/control, one actor schedule, conserved HP/resources/conditions and exact gear/component/passenger custody; (3) a complete continuing-result lifecycle for individual return and cohort persistence, source loci, both clocks, injury/0HP/death/Null, original-body movement/loss, suppression/dispel, replacement and finite fit/custody settlement.

The destination remains the Astral Plane. Named mortal teachings or sites do not themselves specify operational arrival geometry, navigation or transport permissions. Local scene projections, Null recipient branches, and the printed Core duration do not define this spell’s projected-body relation or ongoing result. Do not import a silver cord, copied body/resources, participant cap, time conversion, travel speed, breathing, universal destination knowledge, Sequester stasis, Maze/Banishment endpoints, Plane Shift permissions, or other spell’s dimensions. The attached comparator envelopes are scope boundaries only and confer no Astral Projection permission.

The minimum positive witness remains a legally acquired rank9 caster with multiple distinct willing companions actually arriving and taking useful actions, then one companion independently returning after real movement and item/component use while others continue. Include actual source-qualified actor/site facts, legal payment and resource history, original-body movement/confinement/loss, actual ward predicates, injury/Null, suppression, return-fit conflict and conserved clocks/custody. Historical source checks and component traces are not paid casts or actor encounters; do not replay old cases or assert fictional campaign events.

Preserve all Return336/337/338/339 holds and their open contracts, the prior acceptances, and AFP211-E01 CLOSED. Do not review Imprisonment or any unrelated identity. If missing content or a complete paid useful witness remains, seal an exact one-identity HOLD with the smallest source-grounded contracts and next priority from the attached current queue. If all source and witness requirements are met, seal an exact one-identity ACCEPT and explicit application authorization for Astral Projection only, without changing canonical files; Codex will independently verify the sealed return before applying it. Attach the sealed ZIP and matching DELIVERY.
"""
    request_path = OUT / "REQUEST_340.md"
    request_path.write_text(request, encoding="utf-8", newline="\n")

    packet_members = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file() and path.name != "MEMBER_MANIFEST.json":
            data = path.read_bytes()
            packet_members.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "ASTRAL-PROJECTION-REVIEW340-PACKET-MANIFEST", "payloadMemberCount": len(packet_members), "members": packet_members})

    zip_members = [{"path": "REQUEST_340.md", "bytes": request_path.stat().st_size, "sha256": sha(request_path.read_bytes()), "crc32": crc(request_path.read_bytes())}]
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            zip_members.append({"path": "packet/" + path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(request_path, "REQUEST_340.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                archive.write(path, "packet/" + path.relative_to(PACKET).as_posix())
    archive_bytes = ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as archive:
        if archive.testzip() is not None or archive.namelist() != [row["path"] for row in zip_members]:
            raise RuntimeError("Review340 ZIP integrity or exact member roster failed.")
        for row in zip_members:
            data = archive.read(row["path"])
            if (len(data), sha(data), crc(data)) != (row["bytes"], row["sha256"], row["crc32"]):
                raise RuntimeError("Review340 ZIP member mismatch: " + row["path"])

    delivery = {
        "id": "ASTRAL-PROJECTION-REVIEW340-DELIVERY",
        "reviewId": "Review340",
        "targetIds": [SPELL],
        "blockerIds": [BLOCKER],
        "authority": AUTHORITY,
        "acceptedIds": [],
        "appliedIds": [],
        "applicationAuthorizationRequestedOnlyIfExactSealedAcceptance": [SPELL],
        "decisionRequested": "current-source one-identity reassessment; no canonical mutation by Director",
        "archive": {"fileName": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "crc32": crc(archive_bytes)},
        "archiveMemberCount": len(zip_members),
        "members": zip_members,
        "exactAllowlist": [row["path"] for row in zip_members],
        "currentSourceBindings": source_rows,
        "priorReturn288": binding(PREVIOUS_RETURN),
        "queueBinding": binding(QUEUE),
        "canonicalMutation": False,
        "priorCasesReplayed": False,
    }
    save(DELIVERY, delivery)

    checks = [
        {"id": "current-authority-and-director-next", "passed": queue.get("currentAuthority") == AUTHORITY and queue.get("next") == SPELL and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER]},
        {"id": "target-current-rows-exact", "passed": catalog_row.get("id") == SPELL and index_row.get("id") == SPELL and len(core_rows) == 4 and catalog_row.get("source", {}).get("coreEntries") == [{"index": i, "original": row} for i, row in enumerate(core.get("spells", [])) if row.get("name") == "Astral Projection"]},
        {"id": "prior-astral-hold-scoped", "passed": previous_spell_decision.get("blockerIds") == [BLOCKER] and previous_blocker.get("id") == BLOCKER and len(target_questions) == 15 and len(qualification_rows) == 7},
        {"id": "preserve-other-prior-holds", "passed": set(queue.get("separatelyRetainedHolds", [])) >= {"alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"}},
        {"id": "all-source-bindings-current", "passed": len(source_rows) == len(SOURCE_PATHS) and all((ROOT / row["path"]).is_file() and binding(ROOT / row["path"]) == {k: v for k, v in row.items() if k != "packetMember"} for row in source_rows)},
        {"id": "archive-member-bindings-and-delivery", "passed": len(zip_members) == len(set(row["path"] for row in zip_members)) and len(archive_bytes) == delivery["archive"]["bytes"] and sha(archive_bytes) == delivery["archive"]["sha256"] and crc(archive_bytes) == delivery["archive"]["crc32"]},
    ]
    if not all(check["passed"] for check in checks):
        raise RuntimeError("Review340 preparation failed: " + json.dumps(checks))
    save(MARKER, {
        "id": "ASTRAL-PROJECTION-REVIEW340-PREPARATION-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS",
        "target": SPELL,
        "blocker": BLOCKER,
        "authority": AUTHORITY,
        "sourceCount": len(source_rows),
        "memberCount": len(zip_members),
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": 0,
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **delivery["archive"]},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())},
        "canonicalMutation": False,
    })
    print(json.dumps({"status": "PASS", "checks": len(checks), "target": SPELL, "blocker": BLOCKER, "sources": len(source_rows), "members": len(zip_members), "archiveBytes": len(archive_bytes), "archiveSha256": sha(archive_bytes), "delivery": str(DELIVERY)}, indent=2))


if __name__ == "__main__":
    main()
