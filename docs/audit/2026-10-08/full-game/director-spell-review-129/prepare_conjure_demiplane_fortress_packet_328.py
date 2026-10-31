from __future__ import annotations

import hashlib
import json
import pathlib
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
PUBLIC = ROOT / "DescentReviewChanges/ReviewBible/data/public"
OUT = AUDIT / "rank9_conjure_demiplane_fortress_current_source_328_prepared"
ZIP_PATH = OUT / "DD_Rank9_ConjureDemiplaneFortress_CurrentSource_328.zip"
DELIVERY_PATH = OUT / "DD_Rank9_ConjureDemiplaneFortress_CurrentSource_328_DELIVERY.json"
AUTH = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
FORTRESS_CASES = [
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/actual-scribing-work",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/beneficial-short-rest",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/companion-job",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/creator-death",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/permissions-reentry",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/corpse-return",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/expired-summon-cargo",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/mandatory-reversion",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/nested-space",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/real-dispel",
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/structure-support-loss",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def readj(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def binding(path: pathlib.Path):
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def safe(name: str) -> None:
    p = pathlib.PurePosixPath(name)
    if not name or p.is_absolute() or ".." in p.parts or "\\" in name:
        raise ValueError(f"unsafe package path: {name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_328.json"
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_328.json"
    handoff_path = AUDIT / "CURRENT_HANDOFF_328.json"
    queue, pending, handoff = map(readj, (queue_path, pending_path, handoff_path))
    assert queue["currentAuthority"] == pending["authority"] == handoff["authority"] == AUTH
    assert queue["next"] == pending["nextIdentity"] == "conjure-demiplane-fortress"
    assert queue["activeReview"]["blockerIds"] == ["PG200-B06"]

    catalog_path = PUBLIC / "spell_playtests/catalog.json"
    index_path = PUBLIC / "spell_playtests/authored_review_index.json"
    catalog, index = readj(catalog_path), readj(index_path)
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    index_rows = {row["id"]: row for row in index["entries"]}
    spell_ids = ["conjure-demiplane-fortress", "summon-greater-fire-pet", "faction-champion"]
    selected_catalog = [catalog_rows[key] for key in spell_ids]
    fortress_index = index_rows["conjure-demiplane-fortress"]
    champion_index = index_rows["faction-champion"]
    firepet_index = index_rows["summon-greater-fire-pet"]
    assert fortress_index["authoredStatus"] == "pending-authored-procedure"
    assert champion_index["authoredStatus"] == "reviewed-authored-operational-playtest"
    assert firepet_index["authoredStatus"] == "reviewed-authored-operational-playtest"

    current_proc_path = PUBLIC / "spell_candidates/rank9planargates5_reviewed_200/procedures/conjure-demiplane-fortress.json"
    current_proc = readj(current_proc_path)
    assert current_proc["id"] == "conjure-demiplane-fortress" and current_proc["holdIds"]

    wizard_path = PUBLIC / "class_playtests/wizard.json"
    wizard = readj(wizard_path)
    card = wizard["cards"][19]
    assert card["id"] == "wizard.arch.dispel-magic"
    wizard_displel_binding = binding(wizard_path)

    ac5_path = PUBLIC / "spell_candidates/abjuration_conjuration_rank5_reviewed_05.json"
    ac5 = readj(ac5_path)
    ac5_receipt_path = ROOT / "docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json"
    ac5_receipt = readj(ac5_receipt_path)
    assert ac5_receipt["status"] == "exact-authored-acceptance-applied"
    assert {"faction-champion", "summon-greater-fire-pet"}.issubset(set(ac5_receipt["acceptedSpellIds"]))
    ac5_cases_path = ROOT / "docs/audit/2026-10-08/full-game/ac5-local-final-05-candidate/CASEBOOK.json"
    ac5_cases_file = readj(ac5_cases_path)
    ac5_x17 = [row for row in ac5_cases_file.get("cases", []) if row.get("id") == "AC5-X17"]
    assert len(ac5_x17) == 1
    ac5_spell_rows = [row for row in ac5["spells"] if row["id"] in {"faction-champion", "summon-greater-fire-pet"}]
    ac5_profiles = {key: ac5["profiles"][key] for key in ("AC5-PROFILE-FACTION-CHAMPION-01", "AC5-PROFILE-GREATER-FIRE-PET-01")}

    return284_dir = AUDIT / "rank9_planargates5_return284_received"
    return284_zip = return284_dir / "DD_Rank9_PlanarGates5_Director_Return284_HELD.zip"
    return284_delivery = return284_dir / "DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json"
    return284_receipt = AUDIT / "RANK9_PLANARGATES5_RETURN284_RECEIPT.json"
    return284_audit = AUDIT / "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json"
    return284_delivery_json = readj(return284_delivery)
    assert return284_delivery_json["heldIds"] == ["banishment-gate", "conjure-demiplane-fortress"]
    assert return284_delivery_json["blockerIds"]["conjure-demiplane-fortress"] == ["PG200-B06"]

    return200_dir = AUDIT / "rank9_planargates5_return200_received"
    return200_zip = return200_dir / "DD_Rank9_PlanarGates5_Director_Return200.zip"
    return200_delivery = return200_dir / "DD_Rank9_PlanarGates5_Director_Return200_DELIVERY.json"
    return200_receipt = AUDIT / "RANK9_PLANARGATES5_RETURN200_RECEIPT.json"
    return200_audit = AUDIT / "RANK9_PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"

    return327_dir = AUDIT / "banishment_gate_return327_received"
    return327_decision_path = return327_dir / "DIRECTOR_DECISION.json"
    return327_delivery = return327_dir / "DD_Rank9_BanishmentGate_Director_Return327_HELD_DELIVERY.json"
    return327_zip = return327_dir / "DD_Rank9_BanishmentGate_Director_Return327_HELD.zip"
    return327_receipt = AUDIT / "BANISHMENT_GATE_RETURN327_RECEIPT.json"
    return327_audit = AUDIT / "BANISHMENT_GATE_RETURN327_INDEPENDENT_AUDIT.json"

    return200_manifest = readj(return200_delivery)
    with zipfile.ZipFile(return200_zip) as z:
        old_decision = json.loads(z.read("DIRECTOR_DECISION.json"))
        old_fortress = next(row for row in old_decision["perIdentity"] if row["spellId"] == "conjure-demiplane-fortress")
        old_blocker = next(row for row in old_decision["blockers"] if row["id"] == "PG200-B06")
        old_cases = json.loads(z.read("CASE_DISPOSITIONS.json"))["cases"]
        old_fortress_cases = [row for row in old_cases if row.get("spellId") == "conjure-demiplane-fortress"]
        old_questions = json.loads(z.read("QUESTION_DISPOSITIONS.json"))
        old_qrows = old_questions.get("dispositions", old_questions.get("questions", []))
        old_fortress_questions = [row for row in old_qrows if "conjure-demiplane-fortress" in row.get("spellIds", [])]
        old_future = json.loads(z.read("FUTURE_OBLIGATION_DISPOSITIONS.json"))
        old_futures = old_future.get("dispositions", old_future.get("obligations", [])) if isinstance(old_future, dict) else old_future
        old_fortress_futures = [row for row in old_futures if "conjure-demiplane-fortress" in json.dumps(row)]
        old_proc_bytes = z.read("procedures/conjure-demiplane-fortress.json")

    request = """Director: Packet328 is attached. Review only Conjure Demiplane Fortress / PG200-B06 as directed by independently verified Return327, at current 823 applied / 25 pending / 0 accepted-unapplied authority (547 procedures / 173 interfaces). Preserve Banishment Gate’s PG200-B03/B04 hold, all prior accepted procedures, unrelated holds, and every downstream gate.

The packet binds the original Return200 blocker and procedure, Return284’s independently verified current-source reassessment and all 14 preserved Fortress cases, the current native catalog/index/procedure, the current Wizard Dispel Magic source card, and Return327’s accepted AC5 Humanoid Champion and Elemental Fire Pet examples/rules. Treat Return284’s source-lead availability and AC5 analogies as source evidence only; none is a campaign acquisition, completed case transition, new canonical spell fact, or automatic transfer to Fortress.

Reassess PG200-B06 and each required main/branch witness: actual compatible acquired damaging source and navigable panel/support graph; productive scribing work and beneficial short rest with legitimate inputs/outcomes; a commanded companion job; creator-death persistence; permissions/re-entry; acquired whole-source Dispel Magic and occupied outcome; occupied antimagic suppression; structural support loss; corpse return; finite summoned-body expiration with genuine cargo; mandatory reversion; and nested-space identity/anchor. For every clause, distinguish existing replayed state/rule-only records, currently accepted source-level gains, and the actual missing integrated transitions. In particular, test the bound Wizard Arch Dispel route at Action / 3 RP / 60 ft / Recharge 2, perceived ongoing effect, INT+PB vs DC 19, subject to actual acquisition and exact state; do not substitute Greater Dispel or presume success.

Please issue a sealed Fortress-only decision. If the native proposed procedure is complete under the supplied accepted sources and exact witnesses, state exact accepted ID, binding, and application disposition. Otherwise seal a HOLD with every still-open blocker part, any narrow subparts that close, the minimum source-linked integrated witness per gap, precise authority and next identity. No case may be promoted from a conditional or rule-only fixture. Keep native catalog/index and all canonical files unchanged unless an explicit sealed acceptance authorizes the exact application; no runtime, human-play, balance, cosmology, release, or game-engine approval."""

    fortress_case_names = ["cases/" + case_id.replace("/", "__") + ".json" for case_id in FORTRESS_CASES]
    payload: dict[str, bytes] = {
        "REQUEST.md": (request + "\n").encode("utf-8"),
        "authority/CURRENT_SPELL_QUEUE_328.json": pretty(queue),
        "authority/CURRENT25_PENDING_IDENTITY_AUDIT_328.json": pretty(pending),
        "authority/CURRENT_HANDOFF_328.json": pretty(handoff),
        "authority/catalog_selected.json": pretty({"source": binding(catalog_path), "spells": selected_catalog}),
        "authority/authored_review_index_selected.json": pretty({"source": binding(index_path), "entries": [fortress_index, champion_index, firepet_index]}),
        "current/conjure-demiplane-fortress.json": current_proc_path.read_bytes(),
        "current/wizard_arch_dispel_source.json": pretty({"fileBinding": wizard_displel_binding, "cardPointer": "/cards/19", "card": card}),
        "current/ac5_accepted_spell_sources.json": pretty({"fileBinding": binding(ac5_path), "receiptBinding": binding(ac5_receipt_path), "acceptedSourceRows": ac5_spell_rows, "profiles": ac5_profiles, "acceptedCaseAC5-X17": ac5_x17[0]}),
        "current/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json": ac5_receipt_path.read_bytes(),
        "current/RETURN327_DIRECTOR_DECISION.json": return327_decision_path.read_bytes(),
        "current/RETURN327_DELIVERY.json": return327_delivery.read_bytes(),
        "current/RETURN327_RECEIPT.json": return327_receipt.read_bytes(),
        "current/RETURN327_INDEPENDENT_AUDIT.json": return327_audit.read_bytes(),
        "prior/Return284_HELD.zip": return284_zip.read_bytes(),
        "prior/Return284_HELD_DELIVERY.json": return284_delivery.read_bytes(),
        "prior/Return284_RECEIPT.json": return284_receipt.read_bytes(),
        "prior/Return284_INDEPENDENT_AUDIT.json": return284_audit.read_bytes(),
        "prior/Return200_DELIVERY.json": return200_delivery.read_bytes(),
        "prior/Return200_RECEIPT.json": return200_receipt.read_bytes(),
        "prior/Return200_INDEPENDENT_AUDIT.json": return200_audit.read_bytes(),
        "prior/PG200_B06_ORIGINAL_DISPOSITION.json": pretty({"identityDecision": old_fortress, "blocker": old_blocker, "caseDispositions": old_fortress_cases, "questionDispositions": old_fortress_questions, "futureObligations": old_fortress_futures, "sourceArchiveBinding": return200_manifest["archive"]}),
        "prior/PG200_B06_ORIGINAL_PROCEDURE.json": old_proc_bytes,
        "prior/Return327_HELD.zip": return327_zip.read_bytes(),
    }
    with zipfile.ZipFile(return284_zip) as z:
        for name in fortress_case_names:
            member = name
            payload["prior/Return284_" + name] = z.read(member)
        payload["prior/Return284_ARCH_DISPEL_SOURCE_LEAD.json"] = z.read("SOURCE_LEAD_ARCH_DISPEL.json")
        payload["prior/Return284_FORTRESS_DECISION.json"] = pretty(next(row for row in json.loads(z.read("DIRECTOR_DECISION.json"))["decisions"] if row["id"] == "conjure-demiplane-fortress"))
        payload["prior/Return284_FORTRESS_PROCEDURE.json"] = z.read("procedures/conjure-demiplane-fortress.json")

    payload["SOURCE_SCOPE_AND_LIMITS.json"] = pretty({
        "id": "FORTRESS-PACKET328-SOURCE-SCOPE",
        "scopeIds": ["conjure-demiplane-fortress"],
        "blockerIds": ["PG200-B06"],
        "authority": AUTH,
        "acceptedAc5Transfer": False,
        "campaignFactsEstablished": [],
        "canonicalChanges": False,
        "runtimeExecuted": False,
        "caseIds": FORTRESS_CASES,
        "return200ArchiveBinding": return200_manifest["archive"],
        "return284ArchiveBinding": readj(return284_receipt)["archive"],
        "return327ArchiveBinding": readj(return327_receipt)["archive"],
        "knownSourceCandidate": "Wizard Arch Dispel Magic, card /cards/19: Action, 3 RP, 60 feet, Recharge 2; perceived ongoing effect; rank 9 requires INT+PB vs DC 19. Acquisition and positive occupied outcome remain to be demonstrated.",
    })

    manifest_members = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(payload.items())]
    manifest = {"id": "FORTRESS-CURRENT-SOURCE-PACKET-328-MANIFEST", "payloadEntryCount": len(manifest_members), "members": manifest_members}
    entries = {**payload, "MANIFEST.json": pretty(manifest)}
    for name in entries:
        safe(name)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(entries.items()):
            z.writestr(name, raw)

    archive_raw = ZIP_PATH.read_bytes()
    with zipfile.ZipFile(ZIP_PATH) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(entries)
        assert all(z.read(name) == raw for name, raw in entries.items())
    delivery = {
        "id": "FORTRESS-CURRENT-SOURCE-PACKET-328-DELIVERY",
        "status": "PREPARED_READBACK_PASS",
        "scopeIds": ["conjure-demiplane-fortress"],
        "blockerIds": ["PG200-B06"],
        "archive": {"path": ZIP_PATH.name, "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)},
        "memberCount": len(entries),
        "payloadEntryCount": len(payload),
        "members": [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(entries.items())],
        "currentAuthority": AUTH,
        "return200Authority": return200_manifest.get("authority", None),
        "return284Archive": readj(return284_receipt)["archive"],
        "return327Archive": readj(return327_receipt)["archive"],
        "caseIds": FORTRESS_CASES,
        "caseCount": len(FORTRESS_CASES),
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
    }
    DELIVERY_PATH.write_bytes(pretty(delivery))
    checks = [
        {"check": "current authority and next identity bind to verified Return327 handoff", "passed": True},
        {"check": "exact one-spell scope, current Fortress procedure and pending authored index", "passed": True},
        {"check": "Return200 original B06 decision and Return284 reassessment are included", "passed": True},
        {"check": "all 14 preserved Fortress case traces are included from Return284", "passed": True, "caseCount": len(FORTRESS_CASES)},
        {"check": "current Wizard Dispel source and accepted AC5 finite-body/cargo context are included with transfer limits", "passed": True},
        {"check": "archive exact member allowlist and byte-for-byte readback", "passed": True, "memberCount": len(entries)},
        {"check": "payload manifest verifies all payload members", "passed": True, "payloadEntryCount": len(payload)},
    ]
    audit_path = AUDIT / "FORTRESS_PACKET_328_INDEPENDENT_AUDIT.json"
    audit_path.write_bytes(pretty({
        "id": "FORTRESS-PACKET-328-INDEPENDENT-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS",
        "archive": delivery["archive"],
        "delivery": binding(DELIVERY_PATH),
        "scopeIds": delivery["scopeIds"],
        "blockerIds": delivery["blockerIds"],
        "authority": AUTH,
        "caseCount": len(FORTRESS_CASES),
        "memberCount": len(entries),
        "checks": checks,
        "checkCount": len(checks),
        "passedChecks": sum(item["passed"] for item in checks),
        "failedChecks": sum(not item["passed"] for item in checks),
    }))
    print(json.dumps({"archive": str(ZIP_PATH), "delivery": str(DELIVERY_PATH), "audit": str(audit_path), "bytes": len(archive_raw), "members": len(entries), "cases": len(FORTRESS_CASES), "sha256": sha(archive_raw)}, indent=2))


if __name__ == "__main__":
    main()
