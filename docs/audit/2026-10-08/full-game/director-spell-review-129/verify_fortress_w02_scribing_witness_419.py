#!/usr/bin/env python3
"""Independently validate the packaged Fortress W02 scribing TEST_ONLY branches."""

from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent / "fortress_w02_scribing_witness_419"
PACKET = OUT / "DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_419_TESTONLY.zip"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha(canonical(value))


def load_json(raw: bytes) -> Any:
    return json.loads(raw)


def main() -> None:
    delivery = json.loads((OUT / "DELIVERY_419.json").read_text(encoding="utf-8"))
    packet_bytes = PACKET.read_bytes()
    if len(packet_bytes) != delivery["packetBytes"] or sha(packet_bytes) != delivery["packetSha256"]:
        raise ValueError("Delivery packet bytes/hash do not match DELIVERY_419")

    with zipfile.ZipFile(PACKET) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"Packet ZIP CRC failed at {bad_member}")
        payload = {name.removeprefix("payload/"): archive.read(name)
                   for name in archive.namelist() if name.startswith("payload/") and not name.endswith("/")}
    if "MANIFEST.json" not in payload:
        raise ValueError("Packet has no manifest")
    manifest = load_json(payload["MANIFEST.json"])
    if sha(payload["MANIFEST.json"]) != delivery["manifestSha256"]:
        raise ValueError("Delivery manifest hash does not match packet bytes")
    listed = {row["path"]: row for row in manifest["files"]}
    actual = set(payload) - {"MANIFEST.json"}
    if actual != set(listed):
        raise ValueError("Manifest file set differs from packet payload")
    for path, row in listed.items():
        if len(payload[path]) != row["bytes"] or sha(payload[path]) != row["sha256"]:
            raise ValueError(f"Payload manifest mismatch: {path}")

    proposal_raw = payload["authority/OWNER_PG328_W02_SCRIBING_PREMISE_PROPOSAL_415_TESTONLY.json"]
    adoption_raw = payload["authority/OWNER_PG328_W02_SCRIBING_PREMISE_ADOPTION_419_TESTONLY.json"]
    proposal = load_json(proposal_raw)
    adoption = load_json(adoption_raw)
    expected_proposal_sha = "b817816f040898cdbe290275fd13007670c0ef455d357ac12f0fc457c5665930"
    if sha(proposal_raw) != expected_proposal_sha or adoption["scope"]["proposalSha256"] != expected_proposal_sha:
        raise ValueError("The packet does not preserve the exact owner-adopted Proposal 415 bytes")
    if adoption["ownerAuthorization"]["verbatim"] != "Adopt Proposal 415 exactly":
        raise ValueError("The owner adoption text or scope changed")
    if adoption["scope"]["branchId"] != "PG366-W02-R1" or adoption["scope"]["witnessId"] != "PG328-W02":
        raise ValueError("Owner adoption exceeds or differs from its permitted branch scope")

    queue = load_json(payload["authority/CURRENT_SPELL_QUEUE_404.json"])
    if (queue["id"] != "CURRENT-SPELL-QUEUE-404" or queue["currentAuthority"]["reviewedApplied"] != 829
            or queue["currentAuthority"]["pending"] != 19 or queue["currentAuthority"]["acceptedUnapplied"] != 0):
        raise ValueError("Queue404 counts changed in the review packet")
    if queue["nextIdentity"] != "conjure-demiplane-fortress":
        raise ValueError("Packet does not preserve the active queue priority")

    source_archive_bytes = payload["authority/PG328_HELD_ARCHIVE.zip"]
    preflight = load_json(payload["authority/OWNER_PG328_W02_SCRIBING_SOURCE_PREFLIGHT_397_TESTONLY.json"])
    if sha(source_archive_bytes) != preflight["sourceRulesScreened"][1]["archiveSha256"]:
        raise ValueError("Pinned W02 source archive changed")
    import io

    with zipfile.ZipFile(io.BytesIO(source_archive_bytes)) as source_archive:
        wizard_raw = source_archive.read("evidence/current_bound_wizard.json")
        profile_raw = source_archive.read("evidence/RETURN284_WIZARD20_PROFILE.json")
    if sha(wizard_raw) != preflight["sourceRulesScreened"][0]["sha256"]:
        raise ValueError("Pinned Wizard spell-scribing card changed")
    if sha(profile_raw) != preflight["actorProfileScreen"]["profileMemberSha256"]:
        raise ValueError("Pinned Wizard20 profile changed")

    parent_archive_bytes = payload["parent/Return284_HELD.zip"]
    proposal_parent = proposal["sourceBindings"]["parentArchive"]
    with zipfile.ZipFile(io.BytesIO(parent_archive_bytes)) as parent_archive:
        parent_raw = parent_archive.read(proposal_parent["member"])
    parent = load_json(parent_raw)
    if sha(parent_raw) != proposal_parent["memberSha256"] or len(parent_raw) != proposal_parent["memberBytes"]:
        raise ValueError("Historical parent member does not match its immutable source binding")
    if digest(parent["final"]) != parent["finalSHA256"] or digest(parent["events"][8]["after"]) != parent["finalSHA256"]:
        raise ValueError("Parent terminal state hash or W02 fork point changed")

    catalog_entry = load_json(payload["sources/FLAME_ARMOR_CATALOG_ENTRY_121.json"])["entry"]
    authored_entry = load_json(payload["sources/FLAME_ARMOR_AUTHORED_INDEX_ENTRY_121.json"])["entry"]
    if catalog_entry["id"] != "flame-armor" or catalog_entry["classAccess"]["Wizard"]["rank"] != 1:
        raise ValueError("Flame Armor identity/rank binding changed")
    if authored_entry["id"] != "flame-armor":
        raise ValueError("Authored-index spell identity binding changed")

    completion = load_json(payload["case/PG328_W02_SCRIBING_COMPLETION_BRANCH_419_TESTONLY.json"])
    abandonment = load_json(payload["case/PG328_W02_SCRIBING_ABANDONMENT_BRANCH_419_TESTONLY.json"])
    branches = (completion, abandonment)
    for branch in branches:
        if branch["status"] != "DIRECTOR_REVIEW_PENDING" or branch["scope"]["branchId"] != "PG366-W02-R1":
            raise ValueError("Branch is sealed or outside the adopted scope")
        if branch["lineage"]["parentCaseMemberSha256"] != sha(parent_raw):
            raise ValueError("Branch lineage is not bound to the immutable parent")
        if branch["lineage"]["parentFinalStateSha256"] != parent["finalSHA256"]:
            raise ValueError("Branch parent state hash differs from the preserved parent")
        if branch["ownerAdoptedPremises"]["proposalSha256"] != expected_proposal_sha:
            raise ValueError("Branch's owner premises do not bind the exact adopted proposal")
        if branch["testOnlyLimits"]["fortressAcceptedOrApplied"] or branch["testOnlyLimits"]["queueChanged"]:
            raise ValueError("Branch claims acceptance/application or a queue change")
        if branch["terminalOutcome"]["actorA"]["RP"] != 54 or branch["terminalOutcome"]["actorA"]["newSpellCast"]:
            raise ValueError("The scribing branch unexpectedly changed spellcasting resources")
        clocks = branch["terminalOutcome"]["worldClocks"]
        if round(clocks["elapsedSeconds"] - branch["workTimeline"]["terminalSeconds"], 10) != 0.1:
            raise ValueError("World-clock offset is not preserved")
        if clocks["Hunt"] is not None:
            raise ValueError("A new Hunt clock was introduced")

    completion_start = proposal["proposedOwnerPremises"]["timingAndOutcomes"]["workStartsAtSeconds"]
    if completion["workTimeline"]["terminalSeconds"] - completion_start != 3600:
        raise ValueError("Completion does not meet the one-hour per rank interval")
    if abandonment["workTimeline"]["terminalSeconds"] - completion_start != 1800:
        raise ValueError("Abandonment branch duration is not the adopted 30 minutes")
    entry = completion["terminalOutcome"]["spellbookEntryAdded"]
    if entry is None or entry["spellId"] != "flame-armor" or entry["copySourceManuscriptId"] != "PG328-W02-MANUSCRIPT-FLAME-ARMOR-001":
        raise ValueError("Completed copy lacks its exact source-linked spellbook entry")
    if not entry["existingBookContentsPreserved"] or entry["spellPreparationChanged"]:
        raise ValueError("Completed copy changes existing contents or spell preparation")
    if abandonment["terminalOutcome"]["spellbookEntryAdded"] is not None:
        raise ValueError("Abandonment branch added a spellbook entry")
    if abandonment["terminalOutcome"]["materials"]["refund"] or abandonment["terminalOutcome"]["materials"]["abandonedWorkCreditGranted"]:
        raise ValueError("Abandoned materials/work were refunded or credited")

    ink = proposal["proposedOwnerPremises"]["finiteSupplies"]["inkBottles"]
    paper = proposal["proposedOwnerPremises"]["finiteSupplies"]["paperSheets"]
    gp_total = ink["count"] * ink["eachValueGp"] + paper["count"] * paper["eachValueGp"]
    if round(gp_total, 6) != 25:
        raise ValueError("Finite ink and paper do not reconcile to the adopted 25 gp cost")

    checks = {
        "deliveryAndZipIntegrity": True,
        "payloadManifestAllFilesMatch": True,
        "exactOwnerAdoptedProposal415Bytes": True,
        "ownerScopeLimitedToPG328W02R1": True,
        "currentQueue404Unchanged829_19_0": True,
        "wizardScribingSourceAndCapabilityBound": True,
        "parentArchiveMemberAndForkStateVerified": True,
        "flameArmorWizardRankOneBound": True,
        "oneHourCompletionAndThirtyMinuteAbandonment": True,
        "25GpFiniteMaterialArithmetic": True,
        "completionEntryProvenanceAndNoPreparationChange": True,
        "abandonmentNoOutputNoRefundNoCredit": True,
        "noSpellCastOrRPChange": True,
        "worldClockOffsetPreserved": True,
        "noAcceptanceApplicationOrQueueMutation": True,
    }
    audit_path = OUT / "INDEPENDENT_AUDIT_419.json"
    recorded_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if audit_path.exists():
        prior_audit = json.loads(audit_path.read_text(encoding="utf-8"))
        if prior_audit.get("packetSha256") == sha(packet_bytes):
            recorded_at = prior_audit.get("recordedAtUtc", recorded_at)
    audit = {
        "schemaVersion": 1,
        "recordId": "PG328-W02-INDEPENDENT-AUDIT-419",
        "recordedAtUtc": recorded_at,
        "classification": "INDEPENDENT_PACKAGE_AND_BRANCH_VALIDATION_TEST_ONLY",
        "status": "PASS_DIRECTOR_REVIEW_PENDING",
        "packetPath": PACKET.name,
        "packetBytes": len(packet_bytes),
        "packetSha256": sha(packet_bytes),
        "manifestSha256": sha(payload["MANIFEST.json"]),
        "checkCount": len(checks),
        "checks": checks,
        "queue": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
        "parentBytesMutated": False,
        "fixtureMutated": False,
        "runtimeExecuted": False,
        "witnessSealed": False,
        "fortressAcceptedOrApplied": False,
    }
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": audit["status"], "checks": len(checks), "packetSha256": audit["packetSha256"], "auditPath": str(audit_path)}, indent=2))


if __name__ == "__main__":
    main()
