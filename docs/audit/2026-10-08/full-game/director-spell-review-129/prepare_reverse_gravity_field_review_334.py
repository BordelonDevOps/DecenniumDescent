#!/usr/bin/env python3
"""Prepare a focused, current-authority reassessment packet for IE204-B02."""

from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_impactexile4_reverse_gravity_reassessment_334_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_ReverseGravityField_Review334.zip"
DELIVERY = OUT / "DD_Rank9_ReverseGravityField_Review334_DELIVERY.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_333.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_333.json"
HANDOFF = A / "CURRENT_HANDOFF_333.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
COMBAT = ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md"
EQUIPMENT = ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md"
PRIOR = A / "rank9_impactexile4_return286_received/DD_Rank9_ImpactExile4_Director_Return286_HELD.zip"
OLD_SOURCE = A / "rank9_impactexile4_current_source_286_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_286.json"
SPELL_ID = "reverse-gravity-field"
NEXT_BLOCKER = "IE204-B02"
CASE_IDS = {
    "main_a": "RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-A",
    "main_b": "RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B",
    "overlap": "RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B/overlap",
    "anchored": "RANK9IMPACTEXILE4129-REVERSE-GRAVITY-FIELD-B/anchored",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_id(node, wanted):
    if isinstance(node, dict):
        if node.get("id") == wanted:
            return node
        for value in node.values():
            found = find_id(value, wanted)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_id(value, wanted)
            if found is not None:
                return found
    return None


def case_fragment(archive: ZipFile, member: str, indexes: list[int], fields: list[str]) -> dict:
    raw = archive.read(member)
    case = json.loads(raw)
    rows = []
    for i in indexes:
        event = case["events"][i]
        row = {key: event.get(key) for key in ("id", "kind", "detail", "beforeSHA256", "afterSHA256", "forward", "inverse")}
        row["eventIndex"] = i
        for field in fields:
            section, key = field.split(".", 1)
            row[f"{section}Before"] = event.get("before", {}).get(section, {}).get(key)
            row[f"{section}After"] = event.get("after", {}).get(section, {}).get(key)
        rows.append(row)
    return {
        "caseId": case["id"],
        "member": member,
        "memberBinding": {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)},
        "eventCount": len(case.get("events", [])),
        "qualification": case.get("qualification"),
        "holdIds": case.get("holdIds", []),
        "selectedObservedEvents": rows,
        "fullHistoricalCaseNotReplayed": True,
    }


def main() -> None:
    marker = OUT / "PREPARATION_AUDIT_334.json"
    if OUT.exists() and (not marker.exists() or load(marker).get("id") != "REVERSE-GRAVITY-FIELD-REVIEW334-PREPARATION-AUDIT"):
        raise RuntimeError(f"Output exists without this generator's preparation marker; refusing to overwrite: {OUT}")
    PACKET.mkdir(parents=True, exist_ok=True)

    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index = load(CATALOG), load(INDEX)
    spell, index_row, rope = find_id(catalog, SPELL_ID), find_id(index, SPELL_ID), find_id(catalog, "conjure-rope")
    if spell is None or index_row is None or rope is None:
        raise RuntimeError("Current spell rows needed for focused source comparison are missing.")

    with ZipFile(PRIOR) as prior:
        prior_decision = load_from_zip(prior, "DIRECTOR_DECISION.json")
        held = next(row for row in prior_decision["perIdentity"] if row.get("spellId") == SPELL_ID)
        source_reassessment = load_from_zip(prior, "SOURCE_REASSESSMENT.json")
        hold_register = load_from_zip(prior, "HOLD_REGISTER.json")
        target_hold = next(row for row in hold_register["localRecords"] if row.get("id") == NEXT_BLOCKER)
        question_dispositions = load_from_zip(prior, "QUESTION_DISPOSITIONS.json")
        target_questions = [row for row in question_dispositions.get("currentTargetDispositions", []) if SPELL_ID in row.get("spellIds", [])]
        fragments = {
            CASE_IDS["main_a"]: case_fragment(prior, f"cases/{CASE_IDS['main_a']}.json", [28], ["items.crate"]),
            CASE_IDS["main_b"]: case_fragment(prior, f"cases/{CASE_IDS['main_b']}.json", [28], ["items.crate"]),
            CASE_IDS["overlap"]: case_fragment(prior, f"cases/{CASE_IDS['overlap'].replace('/', '__')}.json", [33], ["items.crate"]),
            CASE_IDS["anchored"]: case_fragment(prior, f"cases/{CASE_IDS['anchored'].replace('/', '__')}.json", [0, 5], ["geometry.attachments", "items.crate"]),
        }
        prior_binding = bind(PRIOR)

    old_source = load(OLD_SOURCE)
    prior_source_bindings = {row["path"]: row for row in old_source.get("sourceBindings", [])}
    relevant_paths = [
        "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
        "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
        "DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md",
    ]
    current_source_rows = []
    for relative in relevant_paths:
        path = ROOT / Path(relative)
        current = bind(path)
        previous = prior_source_bindings.get(relative)
        current_source_rows.append({"source": current, "return286Binding": previous, "unchangedSinceReturn286": bool(previous and previous.get("bytes") == current["bytes"] and previous.get("sha256") == current["sha256"])})

    source_diff = []
    same, changed, missing = 0, [], []
    for row in old_source.get("sourceBindings", []):
        p = ROOT / Path(row["path"])
        if not p.is_file():
            missing.append(row["path"])
            continue
        now = bind(p)
        if now["bytes"] == row.get("bytes") and now["sha256"] == row.get("sha256"):
            same += 1
        else:
            changed.append({"path": row["path"], "old": {"bytes": row.get("bytes"), "sha256": row.get("sha256")}, "current": {"bytes": now["bytes"], "sha256": now["sha256"]}})
    source_diff = {"priorBindingCount": len(old_source.get("sourceBindings", [])), "unchangedCount": same, "changed": changed, "missing": missing, "targetIndexRowUnchanged": old_source["records"][next(i for i, r in enumerate(old_source["records"]) if r.get("spellId") == SPELL_ID)]["currentIndexEntry"] == index_row}

    current_core = load(CORE)
    core_matches = []
    def collect_core(node):
        if isinstance(node, dict):
            if node.get("name") == "Reverse Gravity Field":
                core_matches.append(node)
            for value in node.values():
                collect_core(value)
        elif isinstance(node, list):
            for value in node:
                collect_core(value)
    collect_core(current_core)
    if len(core_matches) != 1:
        raise RuntimeError(f"Expected one exact core row, found {len(core_matches)}.")

    payload = {
        "00_CURRENT_AUTHORITY_333.json": {
            "authority": queue["currentAuthority"],
            "queue": bind(QUEUE),
            "pendingAudit": bind(PENDING),
            "handoff": bind(HANDOFF),
            "activeReview": queue.get("activeReview"),
            "directorReturn333": queue.get("currentReturn"),
            "priorRetainedHolds": queue.get("separatelyRetainedHolds", []),
        },
        "01_CURRENT_CATALOG_SPELL.json": spell,
        "02_CURRENT_AUTHORED_REVIEW_INDEX_ROW.json": index_row,
        "03_CURRENT_CONJURE_ROPE_CATALOG_ROW.json": rope,
        "04_CURRENT_CORE_REVERSE_GRAVITY_ROW.json": core_matches[0],
        "05_RETURN286_DECISION_AND_HOLD.json": {"historicalAuthorityOnly": prior_decision["authority"], "decision": held, "holdRecord": target_hold, "archiveBinding": prior_binding},
        "06_RETURN286_SOURCE_REASSESSMENT.json": source_reassessment,
        "07_RETURN286_TARGET_QUESTION_DISPOSITIONS.json": target_questions,
        "08_RETURN286_OBSERVED_CASE_FRAGMENTS.json": fragments,
        "09_CURRENT_RELEVANT_SOURCE_RECONCILIATION.json": {
            "priorSourceCandidate": bind(OLD_SOURCE),
            "priorSourceBindingSetReconciliation": source_diff,
            "relevantCurrentSourceBindings": current_source_rows,
            "catalogBinding": bind(CATALOG),
            "indexBinding": bind(INDEX),
            "coreBinding": bind(CORE),
            "combatActionsBinding": bind(COMBAT),
            "equipmentProceduresBinding": bind(EQUIPMENT),
        },
    }
    for name, value in payload.items():
        (PACKET / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (PACKET / "10_COMBAT_ACTION_PLAYTEST.md").write_bytes(COMBAT.read_bytes())
    (PACKET / "11_EQUIPMENT_ITEM_PROCEDURES.md").write_bytes(EQUIPMENT.read_bytes())

    request = """# Director review request — Reverse Gravity Field / IE204-B02

One identity only. The Director selected Reverse Gravity Field / IE204-B02 after Return333. Current Queue333 is authoritative at 823 reviewed/applied, 25 pending, zero accepted-unapplied. Return286's 816/32 authority is historical only. The attached current spell and index rows are the exact current rows; the index file changed since the old packet, but the target row itself is unchanged.

Do not replay or re-audit the six old cases. Reconcile the two exact open witnesses from the preserved Return286 HOLD against the current bound source: (W1) the identified 20 lb crate's actual material, structural durability/defenses, applicable 60 ft and 120 ft impact/breakage rules, and exact post-impact contents/ownership/custody; (W2) a real lawful tether AND anchor with actual attachment, geometry/slack, rated strength, and a rule for the Reverse Gravity upward load. Preserve the already demonstrated creature 60 ft/3d6, overlap 120 ft/6d6, Feather Fall, other unchanged outcomes, and all applicable qualifications.

The packet includes the exact current core row, current Conjure Rope operational row, relevant equipment/combat source documents, source-hash comparison from Return286, and only the event fragments bound by W1/W2. Conjure Rope's printed 300 lb static-load capacity is a real source fact, but do not silently treat it as a dynamic upward-force, anchor-rating, or authorization to command a lift; reconcile its explicit no-haul/no-free-lift limits. Likewise, known crate mass/volume do not establish material, hit points, resistance, breakage, salvage or custody.

If a current source supplies both missing witnesses, provide exact source pointers, conditional preconditions and only a minimal reversible delta. Otherwise seal an exact one-identity HOLD naming the smallest missing facts, accepted/applied/held IDs, application authorization, authority/counts, qualifications, and the next current pending priority. Conditional review fixtures are not campaign events or user-authored events. Do not alter canonical data. Return a sealed ZIP plus matching complete delivery JSON; do not claim application without exact sealed authorization.
"""
    (OUT / "REQUEST_334.md").write_text(request, encoding="utf-8")

    members = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            members.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "REVERSE-GRAVITY-FIELD-REVIEW334-PAYLOAD-MANIFEST", "payloadMemberCount": len(members), "members": members})
    archive_members = [{"path": "REQUEST_334.md", "bytes": (OUT / "REQUEST_334.md").stat().st_size, "sha256": sha((OUT / "REQUEST_334.md").read_bytes()), "crc32": crc((OUT / "REQUEST_334.md").read_bytes())}]
    archive_members.extend({"path": path.relative_to(PACKET).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes()), "crc32": crc(path.read_bytes())} for path in sorted(PACKET.rglob("*")) if path.is_file())
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(OUT / "REQUEST_334.md", "REQUEST_334.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(PACKET).as_posix())
    archive_bytes = ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as z:
        bad = z.testzip()
        names = z.namelist()
        if bad or len(names) != len(set(names)) or set(names) != {row["path"] for row in archive_members}:
            raise RuntimeError(f"Archive verification failed: {bad}; {len(names)} entries")
        for row in archive_members:
            data = z.read(row["path"])
            if len(data) != row["bytes"] or sha(data) != row["sha256"] or crc(data) != row["crc32"]:
                raise RuntimeError(f"Archive member binding mismatch: {row['path']}")

    checks = {
        "current_authority_823_25_0": queue.get("currentAuthority") == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
        "director_selected_reverse_gravity": queue.get("next") == SPELL_ID and queue.get("activeReview", {}).get("blockerIds") == [NEXT_BLOCKER],
        "current_rows_exact": spell.get("id") == index_row.get("id") == SPELL_ID,
        "current_spell_still_pending_source_review": spell.get("status") == "blocked-pending-operational-review" and spell.get("operational") is None,
        "current_rope_row_is_source_bound": rope.get("id") == "conjure-rope" and "300 pounds total static load" in rope.get("operational", {}).get("effect", "") and "cannot" in rope.get("operational", {}).get("limitations", ""),
        "return286_exact_hold_preserved": held.get("decision") == "HOLD" and held.get("blockerIds") == [NEXT_BLOCKER] and {r.get("id") for r in held.get("minimumMissingWitnesses", [])} == {"IE286-W1", "IE286-W2"},
        "prior_target_dispositions_preserved": len(target_questions) == 8 and all(SPELL_ID in row.get("spellIds", []) for row in target_questions),
        "target_index_row_unchanged": source_diff["targetIndexRowUnchanged"] is True,
        "only_targeted_history_fragments_included": set(fragments) == set(CASE_IDS.values()) and all(v["fullHistoricalCaseNotReplayed"] for v in fragments.values()),
        "source_bindings_current": all(row["unchangedSinceReturn286"] for row in current_source_rows),
        "archive_crc_and_allowlist": bad is None and len(names) == len(archive_members),
    }
    if not all(checks.values()):
        raise RuntimeError("Review334 preparation failed: " + json.dumps(checks, ensure_ascii=False))

    delivery = {
        "id": "REVERSE-GRAVITY-FIELD-REVIEW334-DELIVERY",
        "archive": {"fileName": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "crc32": crc(archive_bytes)},
        "archiveMemberCount": len(archive_members),
        "payloadMemberCount": len(members) + 1,
        "exactAllowlist": sorted(row["path"] for row in archive_members),
        "members": archive_members,
        "targetId": SPELL_ID,
        "blockerId": NEXT_BLOCKER,
        "authority": queue["currentAuthority"],
        "currentQueue": bind(QUEUE),
        "currentPendingAudit": bind(PENDING),
        "currentCatalog": bind(CATALOG),
        "currentIndex": bind(INDEX),
        "priorReturn286": prior_binding,
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalMutation": False,
    }
    save(DELIVERY, delivery)
    audit = {
        "id": "REVERSE-GRAVITY-FIELD-REVIEW334-PREPARATION-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS_PACKET_PREPARED_NOT_SENT",
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(checks.values()),
        "failed": sum(not value for value in checks.values()),
        "archive": delivery["archive"],
        "delivery": bind(DELIVERY),
        "authority": queue["currentAuthority"],
        "scope": [SPELL_ID],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(OUT / "PREPARATION_AUDIT_334.json", audit)
    print(json.dumps({"archive": str(ARCHIVE), **delivery["archive"], "delivery": str(DELIVERY), "checks": len(checks), "passed": sum(checks.values()), "failed": sum(not value for value in checks.values()), "priorSourceBindings": source_diff}, indent=2))


def load_from_zip(archive: ZipFile, member: str):
    return json.loads(archive.read(member))


if __name__ == "__main__":
    main()
