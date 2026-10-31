from __future__ import annotations

import hashlib
import json
import pathlib
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
OUT = AUDIT / "rank9_banishment_gate_current_source_327_prepared"
ZIP_PATH = OUT / "DD_Rank9_BanishmentGate_CurrentSource_327.zip"
DELIVERY_PATH = OUT / "DD_Rank9_BanishmentGate_CurrentSource_327_DELIVERY.json"
AC5 = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json"
AC5_RECEIPT = ROOT / "docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json"
AC5_CASEBOOK = ROOT / "docs/audit/2026-10-08/full-game/ac5-local-final-05-candidate/CASEBOOK.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
RETURN200_ZIP = AUDIT / "rank9_planargates5_return200_received/DD_Rank9_PlanarGates5_Director_Return200.zip"
RETURN200_DELIVERY = AUDIT / "rank9_planargates5_return200_received/DD_Rank9_PlanarGates5_Director_Return200_DELIVERY.json"
RETURN326_ZIP = AUDIT / "fos326_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return326_HELD.zip"
RETURN326_DELIVERY = AUDIT / "fos326_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return326_HELD_DELIVERY.json"
AUTH = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
BAN_CASES = [
    "RANK9PLANARGATES5129-BANISHMENT-GATE-A.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-B.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-A__unknown-type.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-A__stationary-type-change.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-A__touch-only.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-A__already-claimed.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-B__separate-carried-creature.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-B__summon-expiry.json",
    "RANK9PLANARGATES5129-BANISHMENT-GATE-B__primary-independent-escape.json",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def readj(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_name(name: str) -> None:
    path = pathlib.PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"unsafe member name: {name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    q = readj(AUDIT / "CURRENT_SPELL_QUEUE_327.json")
    h = readj(AUDIT / "CURRENT_HANDOFF_327.json")
    p = readj(AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_327.json")
    current_catalog = readj(CATALOG)
    current_index = readj(INDEX)
    core = readj(CORE)
    ac5 = readj(AC5)
    ac5_receipt = readj(AC5_RECEIPT)
    ac5_cases = readj(AC5_CASEBOOK)
    catalog_spells = {row["id"]: row for row in current_catalog["spells"]}
    index_rows = {row["id"]: row for row in current_index["entries"]}
    ban = catalog_spells["banishment-gate"]
    champion = catalog_spells["faction-champion"]
    ban_index = index_rows["banishment-gate"]
    champion_index = index_rows["faction-champion"]
    champion_proc = next(row for row in ac5["spells"] if row["id"] == "faction-champion")
    greater_fire_pet_proc = next(row for row in ac5["spells"] if row["id"] == "summon-greater-fire-pet")
    champion_profile = ac5["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
    fire_pet_profile = ac5["profiles"]["AC5-PROFILE-GREATER-FIRE-PET-01"]
    core_ban = [row for row in core.get("spells", []) if row.get("name") == "Banishment Gate"]
    if not core_ban:
        # The current Core data uses a nested/document-specific list in some snapshots.
        def find_core(node, out):
            if isinstance(node, dict):
                if node.get("name") == "Banishment Gate":
                    out.append(node)
                for value in node.values():
                    find_core(value, out)
            elif isinstance(node, list):
                for value in node:
                    find_core(value, out)
        find_core(core, core_ban)

    selected_ac5_cases = [
        row for row in ac5_cases.get("cases", [])
        if row.get("id") == "AC5-X14"
        or "Faction Champion creation/attack" in row.get("title", "")
        or any("AC5-PROFILE-FACTION-CHAMPION-01" in json.dumps(ref) for ref in row.get("sourceRefs", []))
    ]
    assert q["currentAuthority"] == AUTH and q["next"] == "banishment-gate"
    assert p["authority"] == AUTH and p["nextPendingIds"] == ["banishment-gate"]
    assert h["authority"] == AUTH and h["scopeIds"] == ["banishment-gate"]
    assert ban_index["authoredStatus"] == "pending-authored-procedure"
    assert champion_index["authoredStatus"] == "reviewed-authored-operational-playtest"
    assert champion_index["reviewId"] == "DD-AC5-EXACT-ACCEPTANCE-05"
    assert ac5_receipt["status"] == "exact-authored-acceptance-applied"
    assert "faction-champion" in ac5_receipt["acceptedSpellIds"]
    assert champion_profile["creatureType"] == "Humanoid"
    assert fire_pet_profile["creatureType"] == "Elemental"
    assert len(selected_ac5_cases) >= 2
    old_delivery = readj(RETURN200_DELIVERY)

    request = """Director: Packet327 is attached. Review only Banishment Gate / PG200-B03 and PG200-B04, as directed by Return326, at current 823/25/0 authority. Preserve all previously applied Rank9 Planar Gates5 procedures, the exact native Banishment Gate card, and all unrelated holds.

The packet carries Return200's sealed Banishment Gate blockers, procedure and nine original cases. Since Return200, the AC5 authored profile has been accepted and applied: Faction Champion is an explicitly typed Humanoid targeting profile with an actual level-9 Wizard source route in its authored case, but its procedure also requires alliedStatus=true, current positive standing, actual invocation permission and no aid ban. Treat its case as a conditional authored fixture, not a campaign fact or automatic source qualification. The accepted Greater Fire Pet profile remains explicitly Elemental. Please determine whether these currently accepted profiles and source routes close PG200-B03 (a real nonmatching control alongside the selected Elemental type) and which, if any, original branches they actually repair.

For PG200-B04, please reassess the touch-only, stationary type-change and already-claimed guard branches, plus living separate-body carriage, primary independent escape, dead-primary/corpse handling and finite-summon expiry with genuine loose cargo. Distinguish events backed by current accepted source procedures from rule-only fixtures. Do not infer a qualifying transition, canonical faction, body/corpse, exit route or expired source from a label or empty record.

If the exact witnesses are now complete, return a sealed Banishment Gate-only acceptance decision with exact corrected source/case bindings, retained qualifications, and explicit application disposition. Otherwise return a sealed Banishment Gate-only HOLD naming each blocker still open, the minimum exact missing witness, any narrow subparts that can be closed, and the next identity. No acceptance/application is requested by this packet; do not alter canon, runtime selection, unrelated decisions or downstream gates. After this identity the current queue names Conjure Demiplane Fortress / PG200-B06.
"""
    candidate_note = {
        "id": "PG327-SOURCE-REASSESSMENT",
        "scope": "Banishment Gate only; this note is a source-binding question, not a source adjudication.",
        "currentAuthority": AUTH,
        "banishmentGate": {"catalogRow": ban, "authoredIndexRow": ban_index, "coreEntriesNamedBanishmentGate": core_ban},
        "candidateCurrentAcceptedProfiles": [
            {
                "spellId": "summon-greater-fire-pet",
                "indexRow": index_rows.get("summon-greater-fire-pet"),
                "profile": fire_pet_profile,
                "sourceStatus": "AC5 exact authored acceptance receipt records this source cohort accepted/applied; do not infer a new creature source beyond the profile.",
            },
            {
                "spellId": "faction-champion",
                "indexRow": champion_index,
                "profile": champion_profile,
                "route": champion_proc["procedure"],
                "matchingAuthoredCases": [row.get("id") for row in selected_ac5_cases],
                "sourceStatus": "AC5 exact authored acceptance receipt records this source cohort accepted/applied; Faction Champion still has its explicit allied faction gate.",
            },
        ],
        "scopeCautions": [
            "Faction Champion is a temporary spell-generated Humanoid-targeting profile, not a transported NPC, faction member, native-plane assertion or campaign fact.",
            "AC5-X14 uses conditional Faction A/B/C fixture facts; it does not establish a real canonical faction or real campaign actor.",
            "Elemental is established only for the specified accepted Elemental profile and its legitimate source route.",
            "Return200's PG200-B03 and PG200-B04 are carried exactly; no status is changed by this packet.",
        ],
    }

    payload: dict[str, bytes] = {
        "REQUEST.md": request.encode("utf-8"),
        "authority/CURRENT_SPELL_QUEUE_327.json": pretty(q),
        "authority/CURRENT_HANDOFF_327.json": pretty(h),
        "authority/CURRENT25_PENDING_IDENTITY_AUDIT_327.json": pretty(p),
        "authority/authored_review_index_selected.json": pretty({"fileBinding": {"path": INDEX.relative_to(ROOT).as_posix(), "bytes": INDEX.stat().st_size, "sha256": sha(INDEX.read_bytes())}, "entries": [ban_index, champion_index]}),
        "authority/catalog_selected.json": pretty({"fileBinding": {"path": CATALOG.relative_to(ROOT).as_posix(), "bytes": CATALOG.stat().st_size, "sha256": sha(CATALOG.read_bytes())}, "spells": [ban, champion]}),
        "current_sources/PG327_SOURCE_REASSESSMENT.json": pretty(candidate_note),
        "current_sources/AC5_REVIEWED_SPELLS.json": AC5.read_bytes(),
        "current_sources/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json": AC5_RECEIPT.read_bytes(),
        "current_sources/AC5_FACTION_CHAMPION_CASES.json": pretty(selected_ac5_cases),
        "prior/Return326_HELD.zip": RETURN326_ZIP.read_bytes(),
        "prior/Return326_HELD_DELIVERY.json": RETURN326_DELIVERY.read_bytes(),
        "prior/Return326_RECEIPT.json": (AUDIT / "FACTION_OMNISCIENCE_SUPREME_RETURN326_RECEIPT.json").read_bytes(),
        "prior/Return326_INDEPENDENT_AUDIT.json": (AUDIT / "FACTION_OMNISCIENCE_SUPREME_RETURN326_INDEPENDENT_AUDIT.json").read_bytes(),
        "prior/PlanarGates5_Return200_DELIVERY.json": RETURN200_DELIVERY.read_bytes(),
    }
    with zipfile.ZipFile(RETURN200_ZIP) as old:
        old_decision = json.loads(old.read("DIRECTOR_DECISION.json"))
        old_ban_decision = next(row for row in old_decision["perIdentity"] if row["spellId"] == "banishment-gate")
        blockers = [row for row in old_decision["blockers"] if row["id"] in ["PG200-B03", "PG200-B04"]]
        old_cases = json.loads(old.read("CASE_DISPOSITIONS.json"))
        relevant_cases = [row for row in old_cases["cases"] if row.get("spellId") == "banishment-gate"]
        old_questions = json.loads(old.read("QUESTION_DISPOSITIONS.json"))
        qrows = old_questions.get("dispositions", old_questions.get("questions", []))
        relevant_questions = [row for row in qrows if "banishment-gate" in row.get("spellIds", []) or row.get("id") in {"PG9-Q13", "PG9-Q14", "PG9-Q15", "PG9-Q16", "PG9-Q17", "PG9-Q29", "PG9-Q30", "GATE129-ADD01"}]
        payload["prior/PG200_BANISHMENT_DIRECTOR_DISPOSITION.json"] = pretty({"identityDecision": old_ban_decision, "blockers": blockers, "caseDispositions": relevant_cases, "questionDispositions": relevant_questions, "remainingQueue": json.loads(old.read("NEXT_QUEUE_HANDOFF.json"))})
        payload["prior/procedures/banishment-gate.json"] = old.read("procedures/banishment-gate.json")
        for name in BAN_CASES:
            payload[f"prior/cases/{name}"] = old.read(f"cases/{name}")

    manifest_rows = []
    for name in sorted(payload):
        safe_name(name)
        raw = payload[name]
        manifest_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
    input_hashes = {
        "authoredReviewIndexSha256": sha(INDEX.read_bytes()),
        "catalogSha256": sha(CATALOG.read_bytes()),
        "coreSourceSha256": sha(CORE.read_bytes()),
        "AC5ReviewedSourceSha256": sha(AC5.read_bytes()),
        "AC5AcceptanceReceiptSha256": sha(AC5_RECEIPT.read_bytes()),
        "Return200DeliverySha256": sha(RETURN200_DELIVERY.read_bytes()),
        "Return326ArchiveSha256": sha(RETURN326_ZIP.read_bytes()),
    }
    manifest = {
        "id": "PG327-MANIFEST",
        "packetId": "RANK9-BANISHMENT-GATE-CURRENT-SOURCE-327",
        "targetSpellIds": ["banishment-gate"],
        "memberCount": len(manifest_rows) + 1,
        "payloadEntryCount": len(manifest_rows),
        "inputBindings": input_hashes,
        "members": manifest_rows,
    }
    all_members = dict(payload)
    all_members["MANIFEST.json"] = pretty(manifest)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        for name, raw in sorted(all_members.items()):
            z.writestr(name, raw)
    zip_raw = ZIP_PATH.read_bytes()
    delivery = {
        "id": "RANK9-BANISHMENT-GATE-CURRENT-SOURCE-327-DELIVERY",
        "status": "PREPARED_FOR_DIRECTOR",
        "targetSpellIds": ["banishment-gate"],
        "targetBlockerIds": ["PG200-B03", "PG200-B04"],
        "authority": AUTH,
        "archive": {"filename": ZIP_PATH.name, "bytes": len(zip_raw), "sha256": sha(zip_raw), "crc32": crc(zip_raw)},
        "memberCount": len(all_members),
        "payloadCount": len(payload),
        "exactAllowlist": sorted(all_members),
        "members": [
            {"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}
            for name, raw in sorted(all_members.items())
        ],
        "inputBindings": input_hashes,
        "caseCount": len(BAN_CASES),
        "caseIds": ["RANK9PLANARGATES5129-BANISHMENT-GATE-A", "RANK9PLANARGATES5129-BANISHMENT-GATE-B"],
        "candidateProfiles": ["AC5-PROFILE-GREATER-FIRE-PET-01", "AC5-PROFILE-FACTION-CHAMPION-01"],
        "previousBlockers": ["PG200-B03", "PG200-B04"],
        "nextIdentityAfterCurrent": "conjure-demiplane-fortress",
        "nextBlockerAfterCurrent": "PG200-B06",
        "sourceProgramsExecuted": False,
        "runtimeExecuted": False,
        "acceptedIds": [],
        "appliedIds": [],
    }
    DELIVERY_PATH.write_bytes(pretty(delivery))

    # Independent packet readback checks before upload.
    with zipfile.ZipFile(ZIP_PATH) as z:
        names = z.namelist()
        assert z.testzip() is None
        assert len(names) == len(set(names)) == delivery["memberCount"]
        assert set(names) == set(delivery["exactAllowlist"])
        seal = {row["path"]: row for row in delivery["members"]}
        assert all(
            len(z.read(name)) == seal[name]["bytes"]
            and sha(z.read(name)) == seal[name]["sha256"]
            and crc(z.read(name)) == seal[name]["crc32"]
            for name in names
        )
        read_manifest = json.loads(z.read("MANIFEST.json"))
        assert read_manifest["payloadEntryCount"] == len(payload)
        assert delivery["acceptedIds"] == delivery["appliedIds"] == []
        assert delivery["authority"] == AUTH

    audit = {
        "id": "BANISHMENT-GATE-PACKET327-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS",
        "archive": delivery["archive"],
        "delivery": {"filename": DELIVERY_PATH.name, "bytes": DELIVERY_PATH.stat().st_size, "sha256": sha(DELIVERY_PATH.read_bytes()), "crc32": crc(DELIVERY_PATH.read_bytes())},
        "memberCount": delivery["memberCount"],
        "payloadCount": delivery["payloadCount"],
        "caseCount": len(BAN_CASES),
        "targetSpellIds": delivery["targetSpellIds"],
        "targetBlockerIds": delivery["targetBlockerIds"],
        "authority": AUTH,
        "readbackChecks": 8,
        "readbackChecksPassed": 8,
        "checks": [
            {"check": "one target spell and exact prior blocker scope", "passed": True},
            {"check": "current authority and queue link Return326 next", "passed": True},
            {"check": "Return200 prior Director blockers/cases/procedure bound", "passed": True},
            {"check": "AC5 Faction Champion profile has exact Humanoid classification", "passed": True},
            {"check": "AC5 Faction Champion accepted/applied receipt and source acquisition gate bound", "passed": True},
            {"check": "all nine original Banishment Gate case records included", "passed": True},
            {"check": "archive CRC, exact allowlist and member hashes pass", "passed": True},
            {"check": "no acceptance, application, runtime or canon edit asserted", "passed": True},
        ],
    }
    audit_path = AUDIT / "BANISHMENT_GATE_PACKET_327_INDEPENDENT_AUDIT.json"
    audit_path.write_bytes(pretty(audit))
    print(json.dumps({"archive": str(ZIP_PATH), "bytes": len(zip_raw), "sha256": sha(zip_raw), "members": len(all_members), "cases": len(BAN_CASES), "audit": str(audit_path)}, indent=2))


if __name__ == "__main__":
    main()
