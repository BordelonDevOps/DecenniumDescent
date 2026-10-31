#!/usr/bin/env python3
"""Prepare a current-source, one-identity delta review for Wish / MR233-B02."""
from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_wish_review_343_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_Wish_Review343.zip"
DELIVERY = OUT / "DD_Rank9_Wish_Review343_DELIVERY.json"
MARKER = OUT / "PREPARATION_AUDIT_343.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_342.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_342.json"
HANDOFF = A / "CURRENT_HANDOFF_342.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_342.md"
R233_ZIP = A / "rank9_miraclereality2_return233_received/DD_Rank9_MiracleReality2_Director_Return233_HELD.zip"
R233_DELIVERY = A / "rank9_miraclereality2_return233_received/DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json"
R233_AUDIT = A / "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json"
R233_RECEIPT = A / "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json"
R289_ZIP = A / "rank9_miraclereality2_return289_received/DD_Rank9_MiracleReality2_Director_Return289_HELD.zip"
R289_DELIVERY = A / "rank9_miraclereality2_return289_received/DD_Rank9_MiracleReality2_Director_Return289_HELD_DELIVERY.json"
R289_AUDIT = A / "RANK9MIRACLEREALITY2_RETURN289_INDEPENDENT_AUDIT.json"
R289_RECEIPT = A / "RANK9MIRACLEREALITY2_RETURN289_RECEIPT.json"
R289_SOURCE_ZIP = A / "rank9_miraclereality2_current_source_289_prepared/DD_Rank9_MiracleReality2_CurrentSource_289.zip"
R342_RECEIPT = A / "DIVINE_INTERVENTION_GREATER_RETURN342_RECEIPT.json"
R342_AUDIT = A / "DIVINE_INTERVENTION_GREATER_RETURN342_INDEPENDENT_AUDIT.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
SPELL = "wish"
BLOCKER = "MR233-B02"
GROUP = "rank9-miracle-reality2"
AUTHORITY = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
SOURCE_PATHS = [
    "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "DescentReviewChanges/ReviewBible/rulebook_output.txt",
    "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "DescentReviewChanges/ReviewBible/docs/director-only/cosmology/GODS_PANTHEONS_REVIEWED_01.md",
    "DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md",
    "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json",
    "DescentReviewChanges/ReviewBible/data/public/class_playtests/druid.json",
    "DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json",
    "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json",
    "DescentReviewChanges/ReviewBible/docs/mechanics/RESONANCE_CANON.md",
    "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_CASTINGCOST5_REVIEWED_222.md",
    "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_RESONANCE3_REVIEWED_122.md",
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
    required = [QUEUE, PENDING, HANDOFF, SNAPSHOT, R233_ZIP, R233_DELIVERY, R233_AUDIT, R233_RECEIPT,
                R289_ZIP, R289_DELIVERY, R289_AUDIT, R289_RECEIPT, R289_SOURCE_ZIP,
                R342_RECEIPT, R342_AUDIT, CATALOG, INDEX, CORE]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index, core = load(CATALOG), load(INDEX), load(CORE)
    catalog_row, index_row = find_id(catalog, SPELL), find_id(index, SPELL)
    core_rows = [{"pointer": f"/spells/{i}", "row": row} for i, row in enumerate(core.get("spells", [])) if row.get("name", "").lower() == "wish"]
    if catalog_row is None or index_row is None or len(core_rows) != 2:
        raise RuntimeError("Current Wish catalog/index rows or two Core placement rows are incomplete or ambiguous.")
    if catalog_row.get("operational") is not None or index_row.get("authoredStatus") != "pending-authored-procedure":
        raise RuntimeError("Wish is no longer pending; refuse stale packet.")
    if queue.get("currentAuthority") != AUTHORITY or queue.get("next") != SPELL or queue.get("activeReview", {}).get("blockerIds") != [BLOCKER]:
        raise RuntimeError("Queue342 does not designate Wish / MR233-B02.")
    if handoff.get("currentBlocker") != {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP} or SPELL not in pending.get("pendingIds", []):
        raise RuntimeError("Handoff/pending audit does not match the current Director priority.")
    r342_receipt, r342_audit = load(R342_RECEIPT), load(R342_AUDIT)
    if not (r342_receipt.get("decision") == "HOLD" and r342_receipt.get("nextIdentity") == SPELL and r342_receipt.get("nextBlockerIds") == [BLOCKER] and r342_audit.get("failed") == 0 and r342_audit.get("checkCount") == r342_audit.get("passed") == 30 and r342_audit.get("historicalSourceRowsIndependentlyVerifiedAgainstWorkspace") == 153):
        raise RuntimeError("Return342 must independently pass and name Wish as next before Review343.")

    with ZipFile(R233_ZIP) as z233, ZipFile(R289_ZIP) as z289:
        if z233.testzip() is not None or z289.testzip() is not None:
            raise RuntimeError("Prior Director archive integrity failed.")
        d233, h233 = json.loads(z233.read("DIRECTOR_DECISION.json")), json.loads(z233.read("HOLD_REGISTER.json"))
        q233, qual233 = json.loads(z233.read("QUESTION_DISPOSITIONS.json")), json.loads(z233.read("QUALIFICATIONS.json"))
        d289, h289 = json.loads(z289.read("DIRECTOR_DECISION.json")), json.loads(z289.read("HOLD_REGISTER.json"))
        q289, qual289 = json.loads(z289.read("QUESTION_DISPOSITIONS.json")), json.loads(z289.read("QUALIFICATIONS.json"))
        source_bindings289 = json.loads(z289.read("SOURCE_BINDINGS.json"))
    prior233_decision = next(r for r in d233.get("perIdentityDecisions", []) if r.get("id") == SPELL)
    prior233_blocker = next(r for r in h233.get("targetBlockers", []) if r.get("id") == BLOCKER)
    prior289_decision = next(r for r in d289.get("decisions", []) if r.get("spellId") == SPELL)
    prior289_blocker = next(r for r in h289.get("targetBlockers", []) if r.get("id") == BLOCKER)
    target_questions = [r for r in q289 if SPELL in r.get("originalQuestionUnchanged", {}).get("spellIds", [])]
    if prior233_decision.get("decision") != "HELD" or prior233_decision.get("blockerIds") != [BLOCKER] or prior289_decision.get("decision") != "HOLD" or prior289_decision.get("blockerIds") != [BLOCKER] or prior233_blocker.get("status") != "OPEN" or prior289_blocker.get("status") != "OPEN":
        raise RuntimeError("Prior Director holds for Wish / MR233-B02 are not intact.")
    if len(target_questions) != 18 or len(qual233) != 9 or len(qual289) != 9 or len(source_bindings289) != 153:
        raise RuntimeError("Prior Wish question/qualification/source history is incomplete.")
    r233_receipt, r289_receipt = load(R233_RECEIPT), load(R289_RECEIPT)
    r233_audit, r289_audit = load(R233_AUDIT), load(R289_AUDIT)
    if not (r233_receipt.get("status") == "PASS" and r289_receipt.get("status") == "PASS" and r233_audit.get("failedChecks") == 0 and r289_audit.get("failedChecks") == 0):
        raise RuntimeError("Prior Return233/289 independent receipts do not pass.")

    # Directly compare Return289's exact 153-file source snapshot with the current checkout.
    delta_rows, missing = [], []
    for row in source_bindings289:
        path = ROOT / row["path"]
        if not path.is_file():
            missing.append(row["path"])
            continue
        data = path.read_bytes()
        delta_rows.append({"path": row["path"], "previousBytes": row.get("bytes"), "previousSha256": row.get("sha256"),
                           "currentBytes": len(data), "currentSha256": sha(data),
                           "unchangedSinceReturn289": (len(data), sha(data)) == (row.get("bytes"), row.get("sha256")),
                           "previousReturn289PacketMember": row.get("packetMember")})
    changed_paths = [r["path"] for r in delta_rows if not r["unchangedSinceReturn289"]]
    if missing or len(delta_rows) != 153 or changed_paths != ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]:
        raise RuntimeError(f"Unexpected Return289 source delta; missing={missing}; changed={changed_paths}")

    preserved = {
        "id": "WISH-REVIEW343-PRESERVED-HOLDS",
        "scope": "Only Wish / MR233-B02 is adjudicated; all prior holds including Divine Intervention Greater are preserved.",
        "currentReturn336to342": [{"identity": sid, "blockers": blockers} for sid, blockers in sorted(queue.get("currentReturnBlockers", {}).items())],
        "separatelyRetainedHolds": queue.get("separatelyRetainedHolds", []),
        "closedEvidenceFindings": ["AFP211-E01 CLOSED", "MR233-E01 CLOSED"],
        "return342DivineInterventionGreater": {"heldIds": ["divine-intervention-greater"], "archive": r342_receipt.get("archive"), "delivery": r342_receipt.get("delivery"), "audit": binding(R342_AUDIT)},
    }

    OUT.mkdir(parents=True, exist_ok=True)
    PACKET.mkdir(parents=True, exist_ok=True)
    inputs = {
        "00_CURRENT_AUTHORITY_AND_QUEUE_342.json": {"authority": AUTHORITY, "queue": binding(QUEUE), "pendingAudit": binding(PENDING), "handoff": binding(HANDOFF), "currentNext": {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP}, "currentReturn342Receipt": binding(R342_RECEIPT)},
        "01_CURRENT_WISH_CATALOG_ROW.json": catalog_row,
        "02_CURRENT_WISH_INDEX_ROW.json": index_row,
        "03_CURRENT_CORE_WISH_ROWS.json": {"source": binding(CORE), "rows": core_rows, "placementCount": 2},
        "04_RETURN289_PRIOR_WISH_HOLD.json": {"historicalAuthorityOnly": d289.get("authority"), "priorDecision": prior289_decision, "priorBlocker": prior289_blocker, "archive": binding(R289_ZIP), "delivery": binding(R289_DELIVERY), "independentAudit": binding(R289_AUDIT), "receipt": binding(R289_RECEIPT), "scope": "Most recent previous Director HOLD for Wish; historical requirements only, not current authority."},
        "05_RETURN233_PRIOR_WISH_HOLD.json": {"historicalAuthorityOnly": d233.get("authority"), "priorDecision": prior233_decision, "priorBlocker": prior233_blocker, "archive": binding(R233_ZIP), "delivery": binding(R233_DELIVERY), "independentAudit": binding(R233_AUDIT), "receipt": binding(R233_RECEIPT), "scope": "First explicit MR233-B02 HOLD; historical only."},
        "06_RETURN289_RELEVANT_QUESTION_DISPOSITIONS.json": {"scope": SPELL, "records": target_questions, "priorRulingOnly": True},
        "07_RETURN289_QUALIFICATIONS.json": {"scope": SPELL, "records": qual289, "priorRulingOnly": True},
        "08_CURRENT_PRESERVED_HOLDS_342.json": preserved,
        "09_RETURN289_TO_CURRENT_SOURCE_DELTA.json": {"priorSourceSnapshot": {"archive": binding(R289_SOURCE_ZIP), "bindingCount": 153}, "currentAuthority": AUTHORITY, "currentChangedPaths": changed_paths, "sourceBindings": delta_rows, "targetSpecificFilesChanged": False},
    }
    for name, value in inputs.items():
        save(PACKET / "input" / name, value)
    for path in (QUEUE, PENDING, HANDOFF, SNAPSHOT):
        (PACKET / "context" / path.name).parent.mkdir(parents=True, exist_ok=True)
        (PACKET / "context" / path.name).write_bytes(path.read_bytes())

    source_rows = []
    for i, rel in enumerate(SOURCE_PATHS):
        src = ROOT / rel
        if not src.is_file():
            raise FileNotFoundError(src)
        alias = f"{i:02d}_" + Path(rel).name
        dst = PACKET / "sources" / alias
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
        row = binding(src)
        row["packetMember"] = "sources/" + alias
        source_rows.append(row)

    request = f"""# Review343 request — Wish / MR233-B02 only

The sole current target is **Wish** (`wish`) / **MR233-B02**. Reassess it from the exact current-source bindings and the Return289-to-current source delta. The current authority is **823 reviewed/applied, 25 pending, 0 accepted-unapplied; 547 complete standalone procedures, 173 scoped interfaces**.

The packet binds both current Wish Core placements and all four current class routes: Cleric/Universal, Druid/Transmutation, Mage/Transmutation, and Wizard/Transmutation. Preserve the exact one-action, 120-foot, V/S/F, Instantaneous, 26-RP Core facts and the native broad promise. Do not add a D&D-style fixed power cap, ritual, price, spell slot, class gate, or frequency absent from the sources.

Return233 and Return289 Wish holds and their 18 Wish-relevant question records are historical evidence for this exact target; reassess only against current bindings. Preserve Return336–342 holds, AFP211-E01 CLOSED, MR233-E01 CLOSED, and all unrelated accepted/held records. Do not re-adjudicate Divine Intervention Greater or any other spell, replay prior cases, infer actual actors/casts from authored fixtures, or change canonical game files.

Determine whether the packet actually supplies complete finite operational contracts for multiple substantive outcomes and one composite, including target/geometry/consent/resistance, physical/material/resource premises, outcome ordering, interruption, partial settlement, persistent aftermath, source conflict/suppression/termination, and irreversible resource/custody history. Also require actual acquired, legal paid rank-9 witnesses for the requested routes and meaningful adverse branches; conditional review fixtures are not gameplay evidence.

If every source and paid-use requirement is satisfied, seal a one-identity ACCEPT with application authorization for Wish only. Otherwise seal the exact one-identity HOLD, open contracts, witness gaps, unchanged authority, and the remaining queue state (including whether a first-review identity remains after Wish). Return the sealed decision ZIP and matching DELIVERY JSON."""
    request_path = OUT / "REQUEST_343.md"
    request_path.write_text(request, encoding="utf-8", newline="\n")

    packet_rows = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file() and path.name != "MEMBER_MANIFEST.json":
            data = path.read_bytes()
            packet_rows.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "WISH-REVIEW343-PACKET-MANIFEST", "payloadMemberCount": len(packet_rows), "members": packet_rows})
    zip_rows = [{"path": "REQUEST_343.md", "bytes": request_path.stat().st_size, "sha256": sha(request_path.read_bytes()), "crc32": crc(request_path.read_bytes())}]
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            zip_rows.append({"path": "packet/" + path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED, compresslevel=9) as z:
        z.write(request_path, "REQUEST_343.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                z.write(path, "packet/" + path.relative_to(PACKET).as_posix())
    raw = ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as z:
        if z.testzip() is not None or z.namelist() != [r["path"] for r in zip_rows]:
            raise RuntimeError("Review343 ZIP integrity or allowlist failed.")
        for row in zip_rows:
            data = z.read(row["path"])
            if (len(data), sha(data), crc(data)) != (row["bytes"], row["sha256"], row["crc32"]):
                raise RuntimeError("Review343 member binding failed: " + row["path"])

    delivery = {"id": "WISH-REVIEW343-DELIVERY", "reviewId": "Review343", "targetIds": [SPELL], "blockerIds": [BLOCKER], "authority": AUTHORITY, "acceptedIds": [], "appliedIds": [], "applicationAuthorizationRequestedOnlyIfExactSealedAcceptance": [SPELL], "decisionRequested": "current-source one-identity Wish reassessment; preserve all prior holds; no canonical mutation by Director", "archive": {"fileName": ARCHIVE.name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}, "archiveMemberCount": len(zip_rows), "members": zip_rows, "exactAllowlist": [r["path"] for r in zip_rows], "currentSourceBindings": source_rows, "previousSourceSnapshotCount": 153, "previousSourceChangedPaths": changed_paths, "priorReturn233": binding(R233_ZIP), "priorReturn289": binding(R289_ZIP), "currentReturn342Receipt": binding(R342_RECEIPT), "queueBinding": binding(QUEUE), "canonicalMutation": False, "priorCasesReplayed": False}
    save(DELIVERY, delivery)

    checks = [
        {"id": "current-authority-and-director-next", "passed": queue.get("currentAuthority") == AUTHORITY and queue.get("next") == SPELL and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER]},
        {"id": "current-target-pending-two-core-placements", "passed": catalog_row.get("id") == SPELL and index_row.get("id") == SPELL and catalog_row.get("operational") is None and index_row.get("authoredStatus") == "pending-authored-procedure" and len(core_rows) == 2},
        {"id": "prior-return233-and289-wish-holds", "passed": prior233_blocker.get("id") == BLOCKER and prior289_blocker.get("id") == BLOCKER and len(target_questions) == 18 and len(qual233) == len(qual289) == 9},
        {"id": "prior-return-receipts-and-current342", "passed": r233_receipt.get("status") == "PASS" and r289_receipt.get("status") == "PASS" and r342_receipt.get("decision") == "HOLD" and r342_audit.get("failed") == 0},
        {"id": "source-delta-exact", "passed": len(delta_rows) == 153 and not missing and changed_paths == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]},
        {"id": "all-four-current-class-sources-bound", "passed": len(source_rows) == len(SOURCE_PATHS) == 14 and all(binding(ROOT / r["path"]) == {k: v for k, v in r.items() if k != "packetMember"} for r in source_rows)},
        {"id": "archive-integrity-and-delivery", "passed": len(zip_rows) == len(set(r["path"] for r in zip_rows)) and len(raw) == delivery["archive"]["bytes"] and sha(raw) == delivery["archive"]["sha256"] and crc(raw) == delivery["archive"]["crc32"]},
    ]
    if not all(row["passed"] for row in checks):
        raise RuntimeError("Review343 preparation failed: " + json.dumps(checks))
    save(MARKER, {"id": "WISH-REVIEW343-PREPARATION-AUDIT", "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "status": "PASS", "target": SPELL, "blocker": BLOCKER, "authority": AUTHORITY, "sourceCount": len(source_rows), "historicalBindingsRechecked": len(delta_rows), "changedSourcePaths": changed_paths, "memberCount": len(zip_rows), "checks": checks, "checkCount": len(checks), "passed": len(checks), "failed": 0, "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **delivery["archive"]}, "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())}, "canonicalMutation": False})
    print(json.dumps({"status": "PASS", "checks": len(checks), "target": SPELL, "blocker": BLOCKER, "currentSources": len(source_rows), "historicalBindingsCompared": len(delta_rows), "changedPaths": changed_paths, "members": len(zip_rows), "archiveBytes": len(raw), "archiveSha256": sha(raw), "delivery": str(DELIVERY)}, indent=2))


if __name__ == "__main__":
    main()
