#!/usr/bin/env python3
"""Prepare a current-source, one-identity delta review for Divine Intervention Greater."""
from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_divine_intervention_greater_review_342_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_DivineInterventionGreater_Review342.zip"
DELIVERY = OUT / "DD_Rank9_DivineInterventionGreater_Review342_DELIVERY.json"
MARKER = OUT / "PREPARATION_AUDIT_342.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_341.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_341.json"
HANDOFF = A / "CURRENT_HANDOFF_341.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_341.md"
RETURN233_ZIP = A / "rank9_miraclereality2_return233_received/DD_Rank9_MiracleReality2_Director_Return233_HELD.zip"
RETURN233_DELIVERY = A / "rank9_miraclereality2_return233_received/DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json"
RETURN233_AUDIT = A / "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json"
RETURN233_RECEIPT = A / "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json"
RETURN289_ZIP = A / "rank9_miraclereality2_return289_received/DD_Rank9_MiracleReality2_Director_Return289_HELD.zip"
RETURN289_DELIVERY = A / "rank9_miraclereality2_return289_received/DD_Rank9_MiracleReality2_Director_Return289_HELD_DELIVERY.json"
RETURN289_AUDIT = A / "RANK9MIRACLEREALITY2_RETURN289_INDEPENDENT_AUDIT.json"
RETURN289_RECEIPT = A / "RANK9MIRACLEREALITY2_RETURN289_RECEIPT.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
SPELL = "divine-intervention-greater"
BLOCKER = "MR233-B01"
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
    required = [QUEUE, PENDING, HANDOFF, SNAPSHOT, RETURN233_ZIP, RETURN233_DELIVERY, RETURN233_AUDIT, RETURN233_RECEIPT, RETURN289_ZIP, RETURN289_DELIVERY, RETURN289_AUDIT, RETURN289_RECEIPT, CATALOG, INDEX, CORE]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index, core = load(CATALOG), load(INDEX), load(CORE)
    catalog_row, index_row = find_id(catalog, SPELL), find_id(index, SPELL)
    core_rows = [{"pointer": f"/spells/{i}", "row": row} for i, row in enumerate(core.get("spells", [])) if row.get("name") == "Divine Intervention (Greater)"]
    if catalog_row is None or index_row is None or len(core_rows) != 1:
        raise RuntimeError("Current Divine Intervention Greater catalog/index/Core entries are incomplete or ambiguous.")
    if catalog_row.get("operational") is not None or index_row.get("authoredStatus") != "pending-authored-procedure":
        raise RuntimeError("Divine Intervention Greater is no longer pending; refuse stale packet.")
    if queue.get("currentAuthority") != AUTHORITY or queue.get("next") != SPELL or queue.get("activeReview", {}).get("blockerIds") != [BLOCKER]:
        raise RuntimeError("Queue341 does not designate Divine Intervention Greater / MR233-B01.")
    if handoff.get("currentBlocker") != {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP} or SPELL not in pending.get("pendingIds", []):
        raise RuntimeError("Handoff/pending audit does not match the current Director priority.")

    with ZipFile(RETURN233_ZIP) as z233, ZipFile(RETURN289_ZIP) as z289:
        if z233.testzip() is not None or z289.testzip() is not None:
            raise RuntimeError("A prior Director archive fails ZIP integrity.")
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
    if prior233_decision.get("decision") != "HELD" or prior233_decision.get("blockerIds") != [BLOCKER] or prior289_decision.get("blockerIds") != [BLOCKER] or prior289_decision.get("decision") != "HOLD" or prior233_blocker.get("status") != "OPEN" or prior289_blocker.get("status") != "OPEN":
        raise RuntimeError("Prior Director holds MR233-B01 are not intact.")
    if len(target_questions) != 15 or len(qual233) != 9 or len(qual289) != 9 or len(source_bindings289) != 153:
        raise RuntimeError("Prior target question/qualification/source history is incomplete.")
    r233_receipt, r289_receipt = load(RETURN233_RECEIPT), load(RETURN289_RECEIPT)
    r233_audit, r289_audit = load(RETURN233_AUDIT), load(RETURN289_AUDIT)
    if not (r233_receipt.get("status") == "PASS" and r289_receipt.get("status") == "PASS" and r233_audit.get("failedChecks") == 0 and r289_audit.get("failedChecks") == 0):
        raise RuntimeError("Prior Return233/289 independent receipts do not pass.")

    # Compare the exact 153-file Return289 snapshot with the present checkout.
    delta_rows = []
    missing = []
    for row in source_bindings289:
        path = ROOT / row["path"]
        if not path.is_file():
            missing.append(row["path"])
            continue
        data = path.read_bytes()
        delta_rows.append({
            "path": row["path"],
            "previousBytes": row.get("bytes"),
            "previousSha256": row.get("sha256"),
            "currentBytes": len(data),
            "currentSha256": sha(data),
            "unchangedSinceReturn289": (len(data), sha(data)) == (row.get("bytes"), row.get("sha256")),
            "previousReturn289PacketMember": row.get("packetMember"),
        })
    changed_paths = [r["path"] for r in delta_rows if not r["unchangedSinceReturn289"]]
    if missing or len(delta_rows) != 153 or changed_paths != ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]:
        raise RuntimeError(f"Unexpected Return289 source delta; missing={missing}; changed={changed_paths}")

    current_return = load(A / "IMPRISONMENT_RETURN341_RECEIPT.json")
    current_audit = load(A / "IMPRISONMENT_RETURN341_INDEPENDENT_AUDIT.json")
    if not (current_return.get("decision") == "HOLD" and current_return.get("nextIdentity") == SPELL and current_return.get("nextBlockerIds") == [BLOCKER] and current_audit.get("failed") == 0 and current_audit.get("checkCount") == current_audit.get("passed")):
        raise RuntimeError("Return341 source priority is not independently verified.")
    preserved = {
        "id": "DIVINE-INTERVENTION-GREATER-REVIEW342-PRESERVED-HOLDS",
        "scope": "Only Divine Intervention Greater / MR233-B01 is adjudicated; Wish / MR233-B02 is preserved without re-adjudication.",
        "returns336to341": [{"identity": sid, "blockers": blockers} for sid, blockers in sorted(queue.get("currentReturnBlockers", {}).items())],
        "separatelyRetainedHolds": queue.get("separatelyRetainedHolds", []),
        "closedEvidenceFinding": "AFP211-E01 CLOSED",
        "return341Imprisonment": {"heldIds": ["imprisonment"], "archive": current_return.get("archive"), "delivery": current_return.get("delivery"), "audit": binding(A / "IMPRISONMENT_RETURN341_INDEPENDENT_AUDIT.json")},
        "wish": {"heldIds": ["wish"], "blockerId": "MR233-B02", "action": "Preserve only; do not review in this packet."},
    }

    OUT.mkdir(parents=True, exist_ok=True)
    PACKET.mkdir(parents=True, exist_ok=True)
    inputs = {
        "00_CURRENT_AUTHORITY_AND_QUEUE_341.json": {"authority": AUTHORITY, "queue": binding(QUEUE), "pendingAudit": binding(PENDING), "handoff": binding(HANDOFF), "currentNext": {"identity": SPELL, "blockerId": BLOCKER, "group": GROUP}, "currentReturn341Receipt": binding(A / "IMPRISONMENT_RETURN341_RECEIPT.json")},
        "01_CURRENT_DIVINE_INTERVENTION_GREATER_CATALOG_ROW.json": catalog_row,
        "02_CURRENT_DIVINE_INTERVENTION_GREATER_INDEX_ROW.json": index_row,
        "03_CURRENT_CORE_DIVINE_INTERVENTION_GREATER_ROWS.json": {"source": binding(CORE), "rows": core_rows},
        "04_RETURN289_PRIOR_TARGET_HOLD.json": {"historicalAuthorityOnly": d289.get("authority"), "priorDecision": prior289_decision, "priorBlocker": prior289_blocker, "archive": binding(RETURN289_ZIP), "delivery": binding(RETURN289_DELIVERY), "independentAudit": binding(RETURN289_AUDIT), "receipt": binding(RETURN289_RECEIPT), "scope": "Most recent previous Director HOLD for MR233-B01; historical requirement definition, not current authority."},
        "05_RETURN233_PRIOR_TARGET_HOLD.json": {"historicalAuthorityOnly": d233.get("authority"), "priorDecision": prior233_decision, "priorBlocker": prior233_blocker, "archive": binding(RETURN233_ZIP), "delivery": binding(RETURN233_DELIVERY), "independentAudit": binding(RETURN233_AUDIT), "receipt": binding(RETURN233_RECEIPT), "scope": "First explicit MR233-B01 HOLD; historical only."},
        "06_RETURN289_RELEVANT_QUESTION_DISPOSITIONS.json": {"scope": SPELL, "records": target_questions, "priorRulingOnly": True, "wishRecords": "Shared questions remain a context boundary only; no Wish disposition is changed."},
        "07_RETURN289_QUALIFICATIONS.json": {"scope": SPELL, "records": qual289, "priorRulingOnly": True},
        "08_CURRENT_PRESERVED_HOLDS_341.json": preserved,
        "09_RETURN289_TO_CURRENT_SOURCE_DELTA.json": {"priorSourceSnapshot": {"archive": binding(A / "rank9_miraclereality2_current_source_289_prepared/DD_Rank9_MiracleReality2_CurrentSource_289.zip"), "bindingCount": 153}, "currentAuthority": AUTHORITY, "currentChangedPaths": changed_paths, "sourceBindings": delta_rows, "targetSpecificFilesChanged": False},
        "10_CURRENT_SOURCE_BINDINGS_342.json": {"target": SPELL, "catalogRowMatchesCurrent": True, "indexRowMatchesCurrent": True, "coreRowCount": len(core_rows), "fullCurrentSources": []},
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
    inputs["10_CURRENT_SOURCE_BINDINGS_342.json"]["fullCurrentSources"] = source_rows
    for name, src in [("CURRENT_SPELL_QUEUE_341.json", QUEUE), ("CURRENT25_PENDING_IDENTITY_AUDIT_341.json", PENDING), ("CURRENT_HANDOFF_341.json", HANDOFF), ("CURRENT_SPELL_REVIEW_SNAPSHOT_341.md", SNAPSHOT)]:
        dest = PACKET / "context" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
    for name, value in inputs.items():
        save(PACKET / "input" / name, value)

    request = """# Director review request — Divine Intervention Greater / MR233-B01

Review Divine Intervention Greater only, as the current Director-prioritized identity after Return341. Current authority is 823 reviewed/applied, 25 pending and 0 accepted-unapplied (547 complete standalone procedures; 173 scoped interfaces). Return233/289 authority snapshots are historical and are not current. Preserve the native Divination placement and actual Cleric/Wizard routes, rank 9, class level 17, 26 base RP, Action/120 feet/V-S-F and Core Instantaneous initiation.

Return233 and the later current-source Return289 both held MR233-B01. The packet binds the exact current catalog/index/Core rows, both target hold records and current faith, intervention, spell-acquisition, class, RP/Dissonance/cost sources. A byte-level comparison of Return289's 153 source paths to the current checkout finds only the authored review index changed; all target-specific source texts, class cards and target row remain as bound. The current index still marks this spell pending and non-operational. Reassess only this evidence delta and exact current source bindings; do not replay or re-audit the earlier case/component traces.

The prior open contracts remain: (1) a complete useful question-result contract grounded in an actual declared faith/recipient relation, available evidence and knowledge, disclosure eligibility, answer precision, uncertainty/protection and interruption boundaries, without inventing deity ontology or universal revelation; (2) an independent substantive task contract with the exact permitted change, target/geometry, actor/body/item/source/resource inputs, defenses, physical versus magical aftermath, limits, repeat/suppression/conflict and once-only ending; (3) actual acquired Cleric and Wizard positive paid casts with full legal chronology, class-adjusted costs/cadence, components, adverse branches and before/after actor/resource/custody records. “Director-determined miracle” is authority to determine a result within a defined task, not a complete universal effect model. Preserve current God/Pantheon identity boundaries and the source-local nature of all comparators.

Do not assume a deity exists or identify it with the First Choir/Fifteenfold; do not grant omniscience, universal answer access, automatic success, wish-like unrestricted task power, a success percentage, imported power cap, extra cost, invented actor or campaign witness. The packet contains no new paid spell encounter. Historical Return233/289 cases and component checks remain evidence only; authorship of historical fixtures is not attributed to the user. Preserve Return336-341 holds and AFP211-E01 CLOSED. Preserve Wish / MR233-B02 without re-adjudication, and do not change canonical files or authorize application absent an exact sealed acceptance.

If current source delta and supplied evidence do not close all requirements, seal the focused one-identity HOLD with exact open contracts, minimum missing witnesses, unchanged authority and the next pending priority. If complete source-owned rules and actual paid positive/adverse witnesses close every requirement, seal a one-identity ACCEPT and explicit application authorization for Divine Intervention Greater only. Attach a sealed ZIP and matching DELIVERY JSON.
"""
    request_path = OUT / "REQUEST_342.md"
    request_path.write_text(request, encoding="utf-8", newline="\n")

    packet_rows = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file() and path.name != "MEMBER_MANIFEST.json":
            data = path.read_bytes()
            packet_rows.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "DIVINE-INTERVENTION-GREATER-REVIEW342-PACKET-MANIFEST", "payloadMemberCount": len(packet_rows), "members": packet_rows})
    zip_rows = [{"path": "REQUEST_342.md", "bytes": request_path.stat().st_size, "sha256": sha(request_path.read_bytes()), "crc32": crc(request_path.read_bytes())}]
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            zip_rows.append({"path": "packet/" + path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED, compresslevel=9) as z:
        z.write(request_path, "REQUEST_342.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                z.write(path, "packet/" + path.relative_to(PACKET).as_posix())
    raw = ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as z:
        if z.testzip() is not None or z.namelist() != [r["path"] for r in zip_rows]:
            raise RuntimeError("Review342 ZIP integrity or allowlist failed.")
        for row in zip_rows:
            data = z.read(row["path"])
            if (len(data), sha(data), crc(data)) != (row["bytes"], row["sha256"], row["crc32"]):
                raise RuntimeError("Review342 member binding failed: " + row["path"])

    delivery = {"id":"DIVINE-INTERVENTION-GREATER-REVIEW342-DELIVERY", "reviewId":"Review342", "targetIds":[SPELL], "blockerIds":[BLOCKER], "authority":AUTHORITY, "acceptedIds":[], "appliedIds":[], "applicationAuthorizationRequestedOnlyIfExactSealedAcceptance":[SPELL], "decisionRequested":"current-source one-identity delta reassessment; preserve Wish; no canonical mutation by Director", "archive":{"fileName":ARCHIVE.name,"bytes":len(raw),"sha256":sha(raw),"crc32":crc(raw)}, "archiveMemberCount":len(zip_rows), "members":zip_rows, "exactAllowlist":[r["path"] for r in zip_rows], "currentSourceBindings":source_rows, "previousSourceSnapshotCount":153, "previousSourceChangedPaths":changed_paths, "priorReturn233":binding(RETURN233_ZIP), "priorReturn289":binding(RETURN289_ZIP), "currentReturn341Receipt":binding(A/"IMPRISONMENT_RETURN341_RECEIPT.json"), "queueBinding":binding(QUEUE), "canonicalMutation":False, "priorCasesReplayed":False}
    save(DELIVERY, delivery)

    checks = [
        {"id":"current-authority-and-director-next","passed":queue.get("currentAuthority")==AUTHORITY and queue.get("next")==SPELL and queue.get("activeReview",{}).get("blockerIds")==[BLOCKER]},
        {"id":"current-target-remains-pending","passed":catalog_row.get("id")==SPELL and index_row.get("id")==SPELL and catalog_row.get("operational") is None and index_row.get("authoredStatus")=="pending-authored-procedure" and len(core_rows)==1},
        {"id":"prior-return233-and-289-target-holds","passed":prior233_blocker.get("id")==BLOCKER and prior289_blocker.get("id")==BLOCKER and len(target_questions)==15},
        {"id":"prior-return-receipts-and-current-341","passed":r233_receipt.get("status")=="PASS" and r289_receipt.get("status")=="PASS" and current_return.get("decision")=="HOLD" and current_audit.get("failed")==0},
        {"id":"source-delta-exact","passed":len(delta_rows)==153 and not missing and changed_paths==["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]},
        {"id":"selected-current-sources-bound","passed":len(source_rows)==len(SOURCE_PATHS) and all(binding(ROOT/r["path"])=={k:v for k,v in r.items() if k!="packetMember"} for r in source_rows)},
        {"id":"archive-integrity-and-delivery","passed":len(zip_rows)==len(set(r["path"] for r in zip_rows)) and len(raw)==delivery["archive"]["bytes"] and sha(raw)==delivery["archive"]["sha256"] and crc(raw)==delivery["archive"]["crc32"]},
    ]
    if not all(r["passed"] for r in checks):
        raise RuntimeError("Review342 preparation failed: " + json.dumps(checks))
    save(MARKER, {"id":"DIVINE-INTERVENTION-GREATER-REVIEW342-PREPARATION-AUDIT", "recordedAtUtc":datetime.now(timezone.utc).isoformat(timespec="seconds"), "status":"PASS", "target":SPELL, "blocker":BLOCKER, "authority":AUTHORITY, "sourceCount":len(source_rows), "historicalBindingsRechecked":len(delta_rows), "changedSourcePaths":changed_paths, "memberCount":len(zip_rows), "checks":checks, "checkCount":len(checks), "passed":len(checks), "failed":0, "archive":{"path":ARCHIVE.relative_to(ROOT).as_posix(),**delivery["archive"]}, "delivery":{"path":DELIVERY.relative_to(ROOT).as_posix(),"bytes":DELIVERY.stat().st_size,"sha256":sha(DELIVERY.read_bytes())}, "canonicalMutation":False})
    print(json.dumps({"status":"PASS","checks":len(checks),"target":SPELL,"blocker":BLOCKER,"currentSources":len(source_rows),"historicalBindingsCompared":len(delta_rows),"changedPaths":changed_paths,"members":len(zip_rows),"archiveBytes":len(raw),"archiveSha256":sha(raw),"delivery":str(DELIVERY)},indent=2))


if __name__ == "__main__":
    main()
