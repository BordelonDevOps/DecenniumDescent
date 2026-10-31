#!/usr/bin/env python3
"""Prepare a focused Return285 reassessment packet for SH202-B03."""

from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_summon_avatar_of_decay_review_333_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_SummonAvatarOfDecay_Review333.zip"
DELIVERY = OUT / "DD_Rank9_SummonAvatarOfDecay_Review333_DELIVERY.json"
CATALOG_PATH = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX_PATH = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
RETURN285 = A / "rank9_summonhosts5_return285_received/DD_Rank9_SummonHosts5_Director_Return285_HELD.zip"
RETURN332 = A / "rank9_summon_herald_of_the_planes_return332_received/payload"
QUEUE332 = A / "CURRENT_SPELL_QUEUE_332.json"
PENDING332 = A / "CURRENT25_PENDING_IDENTITY_AUDIT_332.json"
HANDOFF332 = A / "CURRENT_HANDOFF_332.json"
SPELL_ID = "summon-avatar-of-decay"
BLOCKER = "SH202-B03"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def main() -> None:
    if (OUT / "PREPARATION_AUDIT_333.json").exists():
        raise RuntimeError(f"Packet is already prepared; refusing to overwrite: {OUT}")
    PACKET.mkdir(parents=True, exist_ok=True)
    queue, pending, handoff = load(QUEUE332), load(PENDING332), load(HANDOFF332)
    catalog, index = load(CATALOG_PATH), load(INDEX_PATH)
    spell, index_row = find_id(catalog, SPELL_ID), find_id(index, SPELL_ID)
    if spell is None or index_row is None or queue.get("next") != SPELL_ID:
        raise RuntimeError("Current queue/catalog/index does not bind the target identity.")

    with zipfile.ZipFile(RETURN285) as prior:
        prior_decision = load_from_zip(prior, "DIRECTOR_DECISION.json")
        decision = next(row for row in prior_decision["decisions"] if row.get("id") == SPELL_ID)
        dispositions = load_from_zip(prior, "CASE_DISPOSITIONS.json")["cases"]
        case_rows = [row for row in dispositions if row.get("spellId") == SPELL_ID]
        source_bindings = load_from_zip(prior, "SOURCE_BINDINGS.json")
        selected_source_rows = [
            row for row in source_bindings.get("rows", [])
            if "ferry-wraith-of-the-hush.md" in row.get("path", "").lower()
            or "class_playtests/wizard.json" in row.get("path", "").lower()
        ]
        counterparts = load_from_zip(prior, "COUNTERPART_PROFILES.json")
        actors = load_from_zip(prior, "ACTOR_PROFILES.json")
        actor = actors["W17N"]
        capability_ids = {"wizard.hero.necromancer.flesh-ascendant", "wizard.hero.necromancer.mental-binding", "wizard.hero.necromancer.ghoul-lash"}
        acquired = [row for row in actor.get("allAcquiredClassCapabilities", []) if row.get("id") in capability_ids]
        prior_meta = {
            "archive": bind(RETURN285),
            "authorityHistoricalOnly": prior_decision.get("authority"),
            "targetDecision": decision,
            "targetCaseDispositionRows": case_rows,
            "selectedSourceBindings": selected_source_rows,
            "fullReturn285NotReplayed": True,
        }
        lumen_case = load_from_zip(prior, "procedures/summon-avatar-of-decay.json")
        ferry_source = prior.read("evidence/ferry-wraith-of-the-hush.md")
        ferry_profile = counterparts["SH202-FERRY"]

    payload = {
        "00_CURRENT_AUTHORITY_332.json": {
            "authority": queue["currentAuthority"],
            "queue": bind(QUEUE332),
            "pendingAudit": bind(PENDING332),
            "handoff": bind(HANDOFF332),
            "activeReview": queue.get("activeReview"),
            "previousHeldIds": ["summon-elemental-avatar", "summon-herald-of-the-planes"],
        },
        "01_CURRENT_CATALOG_SPELL.json": spell,
        "02_CURRENT_AUTHORED_REVIEW_INDEX_ROW.json": index_row,
        "03_RETURN332_HERALD_HOLD.json": load(RETURN332 / "DIRECTOR_DECISION.json"),
        "04_RETURN285_AVATAR_DECISION_AND_BINDINGS.json": prior_meta,
        "05_RETURN285_AVATAR_PROCEDURE.json": lumen_case,
        "06_RETURN285_FERRY_COUNTERPART_PROFILE.json": ferry_profile,
        "07_RETURN285_W17N_SOURCE_ACTOR_PROFILE.json": {
            "id": actor.get("id"),
            "profileId": actor.get("profileId"),
            "level": actor.get("level"),
            "class": actor.get("class"),
            "acquisitionLedger": actor.get("acquisitionLedger"),
            "allAcquiredClassCapabilities": acquired,
            "profileSourceBinding": next((row for row in selected_source_rows if "class_playtests/wizard.json" in row.get("path", "").lower()), None),
        },
    }
    for name, value in payload.items():
        (PACKET / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (PACKET / "08_RETURN285_FERRY_SOURCE.md").write_bytes(ferry_source)

    request = """# Director review request — Summon Avatar of Decay / SH202-B03

This is one identity only. Queue332 is current: 823 reviewed/applied, 25 pending, zero accepted-unapplied. Return332 expressly designates Summon Avatar of Decay / SH202-B03 next. The separate Avatar-of-the-Planes findings SH331-C01–C03 and Herald witnesses SH332-W01–W04 remain open and are not part of this review.

Reuse the exact Return285 procedure and disposition. Preserve its already demonstrated conditional work: multi-owner control, acquired paid summons, native Undead, Mind Blank prevention, existing phases, spent hard guards, dynamic maxima, source-suppression cancellation, and the narrow Ferry physical/communication/reach choices. Do not repeat the 13-case Summon Hosts replay or treat the old 816/32 counts as current.

Focus only the residual branches: (1) a competing acquired hard-control relation and its source/guard order, (2) a real acquired classification/type transition that removes Undead eligibility (the attached Flesh Ascendant record only modifies HP/AC/saves; do not claim it changes type), (3) rider-only relay suppression without suppressing the independent body/aura, and (4) same-family aura arbitration. Reconcile the Ferry counterpart’s explicitly local box/mass/Common/reach completion with its unchanged native CR0 bestiary source; this local fixture is not canonical bestiary acceptance.

For each residual branch, decide whether an exact source-bound conditional transition can be constructed from the attached acquired profile and procedure. If so, provide ordered before/after states, observed forward/inverse operations, full reverse traversal and unaffected-path checks. Keep all hypothetical premises labeled conditional. If a branch cannot be resolved without absent source evidence, issue a precise one-identity HOLD naming the smallest missing source fact, then give the next priority after SH202-B03. State exact accepted/applied/held IDs and application authorization, counts, fixture provenance, and attach a matching sealed ZIP plus delivery manifest. Do not alter canonical data or attribute fixtures to the user.
"""
    (OUT / "REQUEST_333.md").write_text(request, encoding="utf-8")

    members = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            members.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    manifest = {"id": "SUMMON-AVATAR-OF-DECAY-REVIEW333-MANIFEST", "payloadMemberCount": len(members), "members": members}
    (PACKET / "MEMBER_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(OUT / "REQUEST_333.md", "REQUEST_333.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(PACKET).as_posix())
    archive_bytes = ARCHIVE.read_bytes()
    with zipfile.ZipFile(ARCHIVE) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Archive CRC failure at {bad}")
        archive_names = z.namelist()
        if len(archive_names) != len(set(archive_names)):
            raise RuntimeError("Duplicate archive member names.")

    catalog_binding, index_binding = bind(CATALOG_PATH), bind(INDEX_PATH)
    delivery = {
        "id": "SUMMON-AVATAR-OF-DECAY-REVIEW333-DELIVERY",
        "archive": {"fileName": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "crc32": crc(archive_bytes)},
        "archiveMemberCount": len(archive_names),
        "payloadMemberCount": len(members),
        "currentAuthority": queue["currentAuthority"],
        "currentQueue": bind(QUEUE332),
        "currentPendingAudit": bind(PENDING332),
        "currentCatalogBinding": catalog_binding,
        "currentIndexBinding": index_binding,
        "targetId": SPELL_ID,
        "blockerId": BLOCKER,
        "priorReturn285AuthorityHistoricalOnly": prior_meta["authorityHistoricalOnly"],
        "canonicalMutation": False,
    }
    DELIVERY.write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    checks = {
        "current_target_rows": spell.get("id") == SPELL_ID and index_row.get("id") == SPELL_ID,
        "current_queue_next": queue.get("next") == SPELL_ID and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER],
        "authority_823_25_0": queue.get("currentAuthority", {}).get("reviewedApplied") == 823 and queue.get("currentAuthority", {}).get("pending") == 25 and queue.get("currentAuthority", {}).get("acceptedUnapplied") == 0,
        "prior_hold_target": prior_meta["targetDecision"].get("blockerIds") == [BLOCKER] and prior_meta["targetDecision"].get("held") is True,
        "case_dispositions_include_main_cases": {row.get("id") for row in case_rows if row.get("status") == "HELD_INCOMPLETE"} >= {"RANK9SUMMONHOSTS5129-SUMMON-AVATAR-OF-DECAY-A", "RANK9SUMMONHOSTS5129-SUMMON-AVATAR-OF-DECAY-B"},
        "selected_conditional_capabilities": capability_ids <= {row.get("id") for row in acquired},
        "counterpart_is_ferry": ferry_profile.get("id") == "SH202-FERRY" and bool(ferry_profile.get("qualification")),
        "ferry_source_is_native_undead": "Medium Undead" in ferry_source.decode("utf-8"),
        "avatar_catalog_blocked": spell.get("status") == "blocked-pending-operational-review",
        "archive_crc_pass": bad is None,
    }
    if not all(checks.values()):
        raise RuntimeError("Preparation checks failed: " + json.dumps(checks, ensure_ascii=False))
    audit = {
        "id": "SUMMON-AVATAR-OF-DECAY-REVIEW333-PREPARATION-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS_PACKET_PREPARED_NOT_SENT",
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(checks.values()),
        "failed": sum(not value for value in checks.values()),
        "archive": delivery["archive"],
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes()), "crc32": crc(DELIVERY.read_bytes())},
        "authority": queue["currentAuthority"],
        "scope": [SPELL_ID],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    (OUT / "PREPARATION_AUDIT_333.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"archive": str(ARCHIVE), "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "delivery": str(DELIVERY), "checks": len(checks), "passed": sum(checks.values()), "failed": sum(not value for value in checks.values())}, indent=2))


def load_from_zip(archive: zipfile.ZipFile, member: str):
    return json.loads(archive.read(member))


if __name__ == "__main__":
    main()
