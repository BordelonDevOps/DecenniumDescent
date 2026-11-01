#!/usr/bin/env python3
"""Build and independently validate the owner-adopted Fortress W02 TEST_ONLY branches."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "fortress_w02_scribing_witness_419"
PAYLOAD = OUT / "payload"

PROPOSAL_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w02_scribing_source_preflight_397/OWNER_PG328_W02_SCRIBING_PREMISE_PROPOSAL_415_TESTONLY.json"
ADOPTION_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w02_scribing_source_preflight_397/OWNER_PG328_W02_SCRIBING_PREMISE_ADOPTION_419_TESTONLY.json"
PREFLIGHT_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w02_scribing_source_preflight_397/OWNER_PG328_W02_SCRIBING_SOURCE_PREFLIGHT_397_TESTONLY.json"
SOURCE_MATCH_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w02_scribing_source_preflight_397/DIRECTOR_PG328_W02_SOURCE_MATCH_READBACK_398.json"
QUEUE_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_404.json"
HANDOFF_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_404.json"
GEOMETRY_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/GEOMETRY_405.json"
GEOMETRY_READBACK_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_geometry_405/DIRECTOR_GEOMETRY_READBACK_405.json"
CATALOG_REL = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX_REL = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
PARENT_ARCHIVE_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/conjure_demiplane_fortress_return328_received/evidence/packet328/prior/Return284_HELD.zip"
SOURCE_ARCHIVE_REL = "docs/audit/2026-10-08/full-game/director-spell-review-129/conjure_demiplane_fortress_closure_intake_367/payload/authority/PG328_HELD_ARCHIVE.zip"

PARENT_MEMBER = "cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A__actual-scribing-work.json"
RULES_MEMBER = "evidence/current_bound_wizard.json"
PROFILE_MEMBER = "evidence/RETURN284_WIZARD20_PROFILE.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return sha(canonical(value))


def git_bytes(relative_path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"HEAD:{relative_path}"], cwd=ROOT)


def git_json(relative_path: str) -> Any:
    return json.loads(git_bytes(relative_path))


def exact_bound_bytes(relative_path: str, expected_sha256: str) -> tuple[bytes, str]:
    """Resolve a source hash against exact working bytes or the published Git blob."""
    working = (ROOT / relative_path).read_bytes()
    if sha(working) == expected_sha256:
        return working, "working_tree_exact_bytes"
    published = git_bytes(relative_path)
    if sha(published) == expected_sha256:
        return published, "published_git_blob_bytes"
    raise ValueError(f"Neither working-tree nor Git blob bytes match the pinned source hash: {relative_path}")


def write_bytes(relative_path: str, data: bytes) -> None:
    destination = PAYLOAD / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)


def write_json(relative_path: str, value: Any) -> None:
    write_bytes(relative_path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def read_zip_member(archive_bytes: bytes, member: str) -> bytes:
    from io import BytesIO

    with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
        return archive.read(member)


def branch_record(
    *,
    kind: str,
    terminal_seconds: float,
    outcome: str,
    proposal: dict[str, Any],
    owner_premises: dict[str, Any],
    lineage: dict[str, Any],
    spell_rule: dict[str, Any],
    spell_row: dict[str, Any],
    authored_row: dict[str, Any],
    source_refs: dict[str, Any],
) -> dict[str, Any]:
    copy_time = proposal["proposedOwnerPremises"]["timingAndOutcomes"]
    materials = proposal["proposedOwnerPremises"]["finiteSupplies"]
    entry = {
        "id": "PG328-W02-FLAME-ARMOR-ENTRY-419",
        "spellId": spell_row["id"],
        "rank": spell_row["classAccess"]["Wizard"]["rank"],
        "school": spell_row["classAccess"]["Wizard"]["school"],
        "addedToSpellbookId": proposal["proposedOwnerPremises"]["spellbook"]["id"],
        "copySourceManuscriptId": proposal["proposedOwnerPremises"]["manuscript"]["id"],
        "sourceCustodianRetainsOwnershipAndCustody": proposal["proposedOwnerPremises"]["manuscript"]["custodianRetainsOwnershipAndCustody"],
        "copyPermission": proposal["proposedOwnerPremises"]["manuscript"]["copyingPermissionForA"],
        "existingBookContentsPreserved": proposal["proposedOwnerPremises"]["spellbook"]["existingContentsPreserved"],
        "spellPreparationChanged": False,
        "provenance": "Owner-adopted TEST_ONLY copy from the complete, legible finite manuscript; no campaign acquisition or occurrence is asserted.",
    }
    is_completion = kind == "completion"
    start = copy_time["workStartsAtSeconds"]
    duration = terminal_seconds - start
    terminal_clock = (proposal["proposedOwnerPremises"]["preservedParent"]["elapsedClockSeconds"]
                      + (terminal_seconds - proposal["proposedOwnerPremises"]["preservedParent"]["timeSeconds"]))
    terminal = {
        "eventTimeSeconds": terminal_seconds,
        "elapsedClockSeconds": round(terminal_clock, 10),
        "clockOffsetSeconds": round(terminal_clock - terminal_seconds, 10),
        "workStatus": "complete" if is_completion else "abandoned",
        "productiveDurationSeconds": duration,
        "spellbookEntryAdded": entry if is_completion else None,
        "materials": {
            "commitAtSeconds": materials["commitAtSeconds"],
            "committedAtStartAndUnavailableForReuse": True,
            "allCommittedInputsLostAtTerminalOutcome": True,
            "refund": False,
            "abandonedWorkCreditGranted": False if not is_completion else None,
            "residueAtWorksiteUnderCustodyOf": "A",
            "residueDescription": materials["terminalResidue"],
            "residueMassOrSalvageInvented": False,
        },
        "actorA": {
            "RP": proposal["proposedOwnerPremises"]["preservedParent"]["rp"],
            "positionFeet": proposal["proposedOwnerPremises"]["preservedParent"]["positionFeet"],
            "newSpellCast": False,
            "restBenefitOrResourceRecovery": False,
            "regularScheduleMarkersPreserved": True,
            "futureInitiativeDispatch": False,
        },
        "worldClocks": {
            "OpeningRemaining": round(lineage["parentClock"]["OpeningRemaining"] - (terminal_clock - lineage["parentClock"]["elapsedSeconds"]), 6),
            "HornRemaining": round(lineage["parentClock"]["HornRemaining"] - (terminal_clock - lineage["parentClock"]["elapsedSeconds"]), 6),
            "Hunt": lineage["parentClock"]["Hunt"],
            "elapsedSeconds": round(terminal_clock, 10),
            "otherClockOffsetsPreserved": True,
        },
    }
    events = [
        {
            "id": f"PG328-W02-R1-{kind.upper()}-419:setup",
            "timeSeconds": copy_time["setupCompleteBySeconds"],
            "kind": "TEST_ONLY_SETUP_COMPLETE",
            "details": "Use only the owner-adopted fixed amenity, already staged legal copy, existing spellbook, tools and finite materials. No initiative action or schedule dispatch is granted.",
        },
        {
            "id": f"PG328-W02-R1-{kind.upper()}-419:deadline",
            "timeSeconds": copy_time["settleInheritedSpellEfficiencyDeadlineOnceAtSeconds"],
            "kind": "SETTLE_INHERITED_SPELL_EFFICIENCY_DEADLINE_ONCE",
            "details": "The inherited Fortress spell-efficiency deadline expires once before scribing begins; it grants no scribing discount or additional benefit.",
        },
        {
            "id": f"PG328-W02-R1-{kind.upper()}-419:scribe-start",
            "timeSeconds": start,
            "kind": "TEST_ONLY_SCRIBING_START_AND_INPUT_COMMITMENT",
            "details": "Commit both ink-bottle contents and all 25 sheets to this one attempt; they cannot be reused. Preserve WIP inputs until the terminal outcome.",
        },
        {
            "id": f"PG328-W02-R1-{kind.upper()}-419:terminal",
            "timeSeconds": terminal_seconds,
            "kind": "TEST_ONLY_SCRIBING_COMPLETION" if is_completion else "TEST_ONLY_SCRIBING_ABANDONMENT",
            "details": "Exactly one provenance-linked spellbook entry is added." if is_completion else "No spellbook entry is added; expended materials and work are not refunded or credited.",
        },
    ]
    return {
        "schemaVersion": 1,
        "recordId": f"PG328-W02-{kind.upper()}-BRANCH-419",
        "classification": "OWNER_ADOPTED_TEST_ONLY_BRANCH_FOR_DIRECTOR_REVIEW",
        "status": "DIRECTOR_REVIEW_PENDING",
        "scope": {
            "identity": "conjure-demiplane-fortress",
            "blockerId": "PG200-B06",
            "witnessId": "PG328-W02",
            "branchId": "PG366-W02-R1",
            "branchKind": kind,
            "parentCaseId": proposal["scope"]["parentCaseId"],
        },
        "lineage": lineage,
        "sourceBindings": source_refs,
        "ownerAdoptedPremises": owner_premises,
        "scribeRule": {
            "ruleText": spell_rule["cards"][1]["effect"],
            "engineText": spell_rule["engine"][7],
            "wizardCapability": "Spell Scribing capability is present in the conditional Wizard20 profile bound by the preflight.",
            "spell": {
                "catalogEntry": spell_row,
                "authoredIndexEntry": authored_row,
                "rank": 1,
                "legalFoundCopyPremise": "The exact finite manuscript, provenance, custody and copying permission are supplied only by the owner-adopted TEST_ONLY premises.",
            },
            "derivedWorkIntervalSeconds": 3600,
            "derivedMaterialRequirementGp": 25,
            "arithmetic": "Rank 1 × 1 hour and rank 1 × 25 gp; the adopted work interval is 3600 seconds and the two ink bottles plus 25 sheets equal 25 gp.",
        },
        "parentForkState": {
            "pointer": "/events/8/after",
            "eventTimeSeconds": 0.9,
            "elapsedClockSeconds": 1.0,
            "actorA": {
                "positionFeet": [15, 10, 0],
                "RP": 54,
                "fortressPaymentAlreadyRecorded": True,
                "cargoAWeightLb": 10,
                "carriedWeightLb": 12,
                "movementRemainingFt": 25,
                "scheduledEndAtSeconds": 0.9,
                "spellEfficiencyDeadlineSeconds": 6.9,
            },
            "stateSha256": lineage["parentFinalStateSha256"],
        },
        "workTimeline": {
            "events": events,
            "workStartSeconds": start,
            "terminalSeconds": terminal_seconds,
            "expectedDurationSeconds": duration,
            "expectedDurationMatchesRule": duration == 3600 if is_completion else duration == 1800,
            "completionAtSeconds": copy_time["completionAtSeconds"] if is_completion else None,
            "abandonmentAtSeconds": copy_time["abandonmentAtSeconds"] if not is_completion else None,
        },
        "terminalOutcome": terminal,
        "testOnlyLimits": {
            "campaignOccurrence": False,
            "canonicalRuleChanged": False,
            "liveFixtureMutated": False,
            "parentBytesChanged": False,
            "fortressAcceptedOrApplied": False,
            "queueChanged": False,
            "w01SupportOrZ40HoldResolved": False,
            "otherFortressHoldsResolved": False,
        },
        "directorQuestion": "Does the completed positive branch satisfy only the PG328-W02 evidence obligation under owner-adopted TEST_ONLY premises? Confirm the exact completion and abandonment accounting, source bindings, parent preservation, and unchanged Queue404. Do not accept/apply Fortress or change any hold.",
    }


def main() -> None:
    proposal_raw, proposal_byte_form = exact_bound_bytes(
        PROPOSAL_REL, "b817816f040898cdbe290275fd13007670c0ef455d357ac12f0fc457c5665930"
    )
    preflight_raw, preflight_byte_form = exact_bound_bytes(
        PREFLIGHT_REL, "6029cca46dd3a456f5a2aee71149ba245bcc5c7098ebb9bda3c3bc9ebafae027"
    )
    geometry_raw, geometry_byte_form = exact_bound_bytes(
        GEOMETRY_REL, "2ec0b2448eb4dd03a028a2c3edfd78c262fbef0309eb3e6ff49a41ca8850a147"
    )
    catalog_raw, catalog_byte_form = exact_bound_bytes(
        CATALOG_REL, "f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8"
    )
    index_raw, index_byte_form = exact_bound_bytes(
        INDEX_REL, "3186236a711c1d798eef3df0a4b784ba2a6cf76f69997df969b383502fe799ee"
    )
    adoption_raw = (ROOT / ADOPTION_REL).read_bytes()
    source_match_raw = (ROOT / SOURCE_MATCH_REL).read_bytes()
    queue_raw = git_bytes(QUEUE_REL)
    handoff_raw = git_bytes(HANDOFF_REL)
    geometry_readback_raw = git_bytes(GEOMETRY_READBACK_REL)
    proposal = json.loads(proposal_raw)
    adoption = json.loads(adoption_raw)
    preflight = json.loads(preflight_raw)
    queue = git_json(QUEUE_REL)
    handoff = git_json(HANDOFF_REL)
    geometry_readback = json.loads(geometry_readback_raw)
    catalog = json.loads(catalog_raw)
    authored_index = json.loads(index_raw)

    if sha(proposal_raw) != "b817816f040898cdbe290275fd13007670c0ef455d357ac12f0fc457c5665930":
        raise ValueError("Proposal 415 bytes do not match the exact owner-authorized SHA-256")
    if adoption["ownerAuthorization"]["verbatim"] != "Adopt Proposal 415 exactly":
        raise ValueError("The owner adoption record does not bind the user's exact authorization")
    if adoption["scope"]["proposalSha256"] != sha(proposal_raw):
        raise ValueError("Owner adoption is not bound to the exact Proposal 415 bytes")
    if proposal["ownerAdoption"]["status"] != "NOT_RECEIVED":
        raise ValueError("Proposal 415's historical proposal bytes unexpectedly changed")
    if sha(preflight_raw) != proposal["sourceBindings"]["sourcePreflight"]["sha256"]:
        raise ValueError("Proposal's source-preflight binding changed")
    if sha(geometry_raw) != proposal["sourceBindings"]["geometry405"]["sha256"]:
        raise ValueError("Proposal's Geometry405 binding changed")
    if sha(catalog_raw) != proposal["sourceBindings"]["flameArmor"]["catalogSha256"]:
        raise ValueError("Bound spell catalog changed")
    if sha(index_raw) != proposal["sourceBindings"]["flameArmor"]["authoredIndexSha256"]:
        raise ValueError("Bound authored spell index changed")
    if queue["id"] != "CURRENT-SPELL-QUEUE-404" or queue["currentAuthority"] != {
        "reviewedApplied": 829,
        "pending": 19,
        "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 553,
        "scopedInterfaces": 173,
    }:
        raise ValueError("Queue404 is not the reviewed 829/19/0 authority")
    if queue["nextIdentity"] != "conjure-demiplane-fortress" or "PG200-B06" not in handoff["nextStep"]:
        raise ValueError("Fortress is no longer the current queue/handoff target")

    parent_archive = (ROOT / PARENT_ARCHIVE_REL).read_bytes()
    source_archive = (ROOT / SOURCE_ARCHIVE_REL).read_bytes()
    parent_archive_sha = sha(parent_archive)
    source_archive_sha = sha(source_archive)
    expected_source_archive_sha = preflight["sourceRulesScreened"][1]["archiveSha256"]
    if source_archive_sha != expected_source_archive_sha:
        raise ValueError("The bound held archive source changed")
    with zipfile.ZipFile(ROOT / PARENT_ARCHIVE_REL) as parent_zip:
        parent_raw = parent_zip.read(PARENT_MEMBER)
    parent = json.loads(parent_raw)
    parent_member_sha = sha(parent_raw)
    if parent_member_sha != proposal["sourceBindings"]["parentArchive"]["memberSha256"]:
        raise ValueError("The immutable historical parent member changed")
    if len(parent_raw) != proposal["sourceBindings"]["parentArchive"]["memberBytes"]:
        raise ValueError("The immutable historical parent member length changed")
    parent_final = parent["final"]
    fork_state = parent["events"][8]["after"]
    if digest(parent_final) != parent["finalSHA256"] or digest(fork_state) != parent["finalSHA256"]:
        raise ValueError("The selected W02 fork state no longer matches the held parent final state")
    if proposal["sourceBindings"]["parentArchive"]["preservedThroughPointer"] != "/events/8/after" or len(parent["events"]) <= 8:
        raise ValueError("Proposal's W02 fork pointer does not resolve to parent event 8")
    actor_a = fork_state["actors"]["A"]
    clock = fork_state["clock"]
    if (fork_state["time"] != 0.9 or clock["elapsedSeconds"] != 1.0 or actor_a["position"] != [15, 10, 0]
            or actor_a["RP"] != 54 or actor_a["carriedWeightLb"] != 12 or actor_a["movement"] != 25):
        raise ValueError("Parent fork state does not match the adopted W02 snapshot")

    wizard_source_raw = read_zip_member(source_archive, RULES_MEMBER)
    profile_source_raw = read_zip_member(source_archive, PROFILE_MEMBER)
    if sha(wizard_source_raw) != preflight["sourceRulesScreened"][0]["sha256"]:
        raise ValueError("Bound Wizard source card bytes changed")
    if sha(profile_source_raw) != preflight["actorProfileScreen"]["profileMemberSha256"]:
        raise ValueError("Bound Wizard20 profile bytes changed")
    spell_rule = json.loads(wizard_source_raw)
    profile = json.loads(profile_source_raw)
    if "Spell Scribing" not in str(spell_rule["cards"][1].get("name", "")):
        raise ValueError("Bound Wizard card is not Spell Scribing")
    if "Spell Scribing" not in json.dumps(profile, ensure_ascii=False):
        raise ValueError("Bound Wizard20 profile does not show the acquired Spell Scribing capability")

    spell_row = catalog["spells"][121]
    authored_row = authored_index["entries"][121]
    if spell_row["id"] != "flame-armor" or spell_row["classAccess"]["Wizard"]["rank"] != 1:
        raise ValueError("Bound Flame Armor source is no longer a Wizard rank-1 spell")
    if authored_row.get("id") != "flame-armor":
        raise ValueError("Bound authored-review entry does not match Flame Armor")
    premises = proposal["proposedOwnerPremises"]
    materials = premises["finiteSupplies"]
    material_total = materials["inkBottles"]["count"] * materials["inkBottles"]["eachValueGp"] + materials["paperSheets"]["count"] * materials["paperSheets"]["eachValueGp"]
    material_weight = materials["inkBottles"]["count"] * materials["inkBottles"]["eachWeightLbGross"] + materials["paperSheets"]["count"] * materials["paperSheets"]["eachWeightLb"]
    if round(material_total, 6) != 25 or round(material_weight, 6) != materials["materialsInitialGrossWeightLb"]:
        raise ValueError("Adopted consumable material quantity/value/weight no longer reconciles")
    if premises["timingAndOutcomes"]["completionAtSeconds"] - premises["timingAndOutcomes"]["workStartsAtSeconds"] != 3600:
        raise ValueError("Owner-adopted completion interval is not exactly one hour")
    if premises["timingAndOutcomes"]["abandonmentAtSeconds"] - premises["timingAndOutcomes"]["workStartsAtSeconds"] != 1800:
        raise ValueError("Owner-adopted abandonment interval is not exactly 30 minutes")
    table_review = proposal["sourceBindings"]["geometry405"].get("directorReadback", "").lower()
    if "table envelope is clear" not in table_review or "2660 panels" not in table_review:
        raise ValueError("Proposal 415 no longer contains the Director-reviewed W02 table-clearance readback")

    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    parent_clock = {
        "elapsedSeconds": clock["elapsedSeconds"],
        "OpeningRemaining": clock["OpeningRemaining"],
        "HornRemaining": clock["HornRemaining"],
        "Hunt": clock["Hunt"],
    }
    lineage = {
        "parentArchivePath": PARENT_ARCHIVE_REL,
        "parentArchiveBytes": len(parent_archive),
        "parentArchiveSha256": parent_archive_sha,
        "parentCaseMember": PARENT_MEMBER,
        "parentCaseMemberBytes": len(parent_raw),
        "parentCaseMemberSha256": parent_member_sha,
        "parentCaseId": parent["id"],
        "parentFinalStateSha256": parent["finalSHA256"],
        "parentFinalStateContentDigest": digest(parent_final),
        "parentWasHeld": parent["status"] == "HELD_MISSING_POSITIVE_BRANCH",
        "parentHoldIds": parent["holdIds"],
        "preservedThroughPointer": "/events/8/after",
        "parentBytesMutated": False,
        "parentClock": parent_clock,
        "constructedAgainstMainCommit": git_commit,
    }
    source_refs = {
        "proposal415": {"path": PROPOSAL_REL, "sha256": sha(proposal_raw)},
        "proposal415GitBlobSha256": sha(git_bytes(PROPOSAL_REL)),
        "proposal415ByteForm": proposal_byte_form,
        "ownerAdoption419": {"path": ADOPTION_REL, "sha256": sha(adoption_raw), "gitBlobSha256": sha(git_bytes(ADOPTION_REL))},
        "sourcePreflight397": {"path": PREFLIGHT_REL, "sha256": sha(preflight_raw)},
        "sourcePreflight397GitBlobSha256": sha(git_bytes(PREFLIGHT_REL)),
        "sourcePreflight397ByteForm": preflight_byte_form,
        "directorSourceMatchReadback398": {"path": SOURCE_MATCH_REL, "sha256": sha(source_match_raw)},
        "geometry405": {"path": GEOMETRY_REL, "sha256": sha(geometry_raw), "gitBlobSha256": sha(git_bytes(GEOMETRY_REL)), "byteForm": geometry_byte_form},
        "directorGeometryReadback405": {"path": GEOMETRY_READBACK_REL, "sha256": sha(geometry_readback_raw)},
        "currentSpellQueue404": {"path": QUEUE_REL, "sha256": sha(queue_raw)},
        "currentHandoff404": {"path": HANDOFF_REL, "sha256": sha(handoff_raw)},
        "heldArchiveSource": {"path": SOURCE_ARCHIVE_REL, "sha256": source_archive_sha, "wizardRuleMember": RULES_MEMBER, "wizardRuleMemberSha256": sha(wizard_source_raw), "wizardProfileMember": PROFILE_MEMBER, "wizardProfileMemberSha256": sha(profile_source_raw)},
        "spellCatalogEntry": {"path": CATALOG_REL + "#/spells/121", "sourceSha256": sha(catalog_raw), "gitBlobSha256": sha(git_bytes(CATALOG_REL)), "byteForm": catalog_byte_form, "spellId": spell_row["id"]},
        "authoredIndexEntry": {"path": INDEX_REL + "#/entries/121", "sourceSha256": sha(index_raw), "gitBlobSha256": sha(git_bytes(INDEX_REL)), "byteForm": index_byte_form, "spellId": authored_row["id"]},
    }

    if OUT.exists():
        import shutil

        shutil.rmtree(OUT)
    PAYLOAD.mkdir(parents=True)

    # Preserve authoritative inputs byte-for-byte where possible.
    for rel, raw in ((PROPOSAL_REL, proposal_raw), (ADOPTION_REL, adoption_raw), (PREFLIGHT_REL, preflight_raw),
                     (SOURCE_MATCH_REL, source_match_raw), (QUEUE_REL, queue_raw), (HANDOFF_REL, handoff_raw),
                     (GEOMETRY_REL, geometry_raw), (GEOMETRY_READBACK_REL, geometry_readback_raw)):
        write_bytes("authority/" + Path(rel).name, raw)
    write_bytes("authority/PG328_HELD_ARCHIVE.zip", source_archive)
    write_bytes("parent/Return284_HELD.zip", parent_archive)
    write_bytes("sources/current_bound_wizard.json", wizard_source_raw)
    write_bytes("sources/RETURN284_WIZARD20_PROFILE.json", profile_source_raw)
    write_json("sources/FLAME_ARMOR_CATALOG_ENTRY_121.json", {"sourcePath": CATALOG_REL, "sourceSha256": sha(catalog_raw), "pointer": "/spells/121", "entry": spell_row})
    write_json("sources/FLAME_ARMOR_AUTHORED_INDEX_ENTRY_121.json", {"sourcePath": INDEX_REL, "sourceSha256": sha(index_raw), "pointer": "/entries/121", "entry": authored_row})

    owner_premises = {
        "proposalId": proposal["recordId"],
        "proposalSha256": sha(proposal_raw),
        "adoptionId": adoption["recordId"],
        "adoptionSha256": sha(adoption_raw),
        "exactProposedOwnerPremises": copy.deepcopy(premises),
        "noAdditionalOwnerPremisesIntroduced": True,
    }
    completion = branch_record(kind="completion", terminal_seconds=3607.0, outcome="completed", proposal=proposal,
                               owner_premises=owner_premises, lineage=lineage, spell_rule=spell_rule,
                               spell_row=spell_row, authored_row=authored_row, source_refs=source_refs)
    abandonment = branch_record(kind="abandonment", terminal_seconds=1807.0, outcome="abandoned", proposal=proposal,
                                owner_premises=owner_premises, lineage=lineage, spell_rule=spell_rule,
                                spell_row=spell_row, authored_row=authored_row, source_refs=source_refs)
    write_json("case/PG328_W02_SCRIBING_COMPLETION_BRANCH_419_TESTONLY.json", completion)
    write_json("case/PG328_W02_SCRIBING_ABANDONMENT_BRANCH_419_TESTONLY.json", abandonment)

    checks = {
        "proposal415ExactOwnerAuthorizedSha256": sha(proposal_raw) == adoption["scope"]["proposalSha256"],
        "ownerAdoptionScopeMatches": adoption["scope"]["branchId"] == "PG366-W02-R1",
        "parentArchiveMemberBytesAndShaMatch": parent_member_sha == proposal["sourceBindings"]["parentArchive"]["memberSha256"],
        "parentStateContentDigestMatchesReceipt": digest(parent_final) == parent["finalSHA256"],
        "branchForkUsesExactParentEvents8After": digest(fork_state) == digest(parent_final),
        "wizardScribingCapabilityAndRuleSourceBound": sha(wizard_source_raw) == preflight["sourceRulesScreened"][0]["sha256"],
        "flameArmorWizardRankOne": spell_row["id"] == "flame-armor" and spell_row["classAccess"]["Wizard"]["rank"] == 1,
        "legalCopyManuscriptAndCustodyExplicit": premises["manuscript"]["complete"] and premises["manuscript"]["copyingPermissionForA"] and premises["manuscript"]["custodianRetainsOwnershipAndCustody"],
        "receivingSpellbookIdentityAndCustodyExplicit": premises["spellbook"]["id"] == "A-SPELLBOOK-01" and premises["spellbook"]["existingContentsPreserved"],
        "materialsExactly25Gp": round(material_total, 6) == 25,
        "completionExactlyOneHourAfterStart": completion["workTimeline"]["expectedDurationSeconds"] == 3600,
        "abandonmentExactlyThirtyMinutesAfterStart": abandonment["workTimeline"]["expectedDurationSeconds"] == 1800,
        "completionAddsOnlyOneProvenanceLinkedEntry": completion["terminalOutcome"]["spellbookEntryAdded"]["spellId"] == "flame-armor",
        "abandonmentAddsNoEntryAndNoRefundOrCredit": abandonment["terminalOutcome"]["spellbookEntryAdded"] is None and not abandonment["terminalOutcome"]["materials"]["refund"] and abandonment["terminalOutcome"]["materials"]["abandonedWorkCreditGranted"] is False,
        "noInitiativeOrRestBenefitGranted": not completion["terminalOutcome"]["actorA"]["futureInitiativeDispatch"] and not completion["terminalOutcome"]["actorA"]["restBenefitOrResourceRecovery"],
        "clockOffsetAndRunningClocksReconcile": round(completion["terminalOutcome"]["worldClocks"]["elapsedSeconds"] - completion["workTimeline"]["terminalSeconds"], 10) == 0.1 and round(abandonment["terminalOutcome"]["worldClocks"]["elapsedSeconds"] - abandonment["workTimeline"]["terminalSeconds"], 10) == 0.1,
        "runningWorldClocksAdvanceByElapsedInterval": round(parent_clock["OpeningRemaining"] - completion["terminalOutcome"]["worldClocks"]["OpeningRemaining"], 6) == round(completion["terminalOutcome"]["worldClocks"]["elapsedSeconds"] - parent_clock["elapsedSeconds"], 6) and round(parent_clock["HornRemaining"] - completion["terminalOutcome"]["worldClocks"]["HornRemaining"], 6) == round(completion["terminalOutcome"]["worldClocks"]["elapsedSeconds"] - parent_clock["elapsedSeconds"], 6) and round(parent_clock["OpeningRemaining"] - abandonment["terminalOutcome"]["worldClocks"]["OpeningRemaining"], 6) == round(abandonment["terminalOutcome"]["worldClocks"]["elapsedSeconds"] - parent_clock["elapsedSeconds"], 6) and round(parent_clock["HornRemaining"] - abandonment["terminalOutcome"]["worldClocks"]["HornRemaining"], 6) == round(abandonment["terminalOutcome"]["worldClocks"]["elapsedSeconds"] - parent_clock["elapsedSeconds"], 6),
        "queue404UnchangedAt829_19_0": queue["currentAuthority"]["reviewedApplied"] == 829 and queue["currentAuthority"]["pending"] == 19 and queue["currentAuthority"]["acceptedUnapplied"] == 0,
        "noFortressAcceptanceOrApplication": completion["testOnlyLimits"]["fortressAcceptedOrApplied"] is False and abandonment["testOnlyLimits"]["fortressAcceptedOrApplied"] is False,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"W02 branch validation failed: {failed}")

    validation = {
        "schemaVersion": 1,
        "recordId": "PG328-W02-BRANCH-VALIDATION-419",
        "classification": "BUILDER_STRUCTURAL_AND_SOURCE_VALIDATION_TEST_ONLY",
        "status": "PASS_DIRECTOR_REVIEW_PENDING",
        "builtAgainstMainCommit": git_commit,
        "checkCount": len(checks),
        "checks": checks,
        "materialArithmetic": {
            "inkGp": materials["inkBottles"]["count"] * materials["inkBottles"]["eachValueGp"],
            "paperGp": materials["paperSheets"]["count"] * materials["paperSheets"]["eachValueGp"],
            "totalRequiredGp": material_total,
            "grossMaterialWeightLb": material_weight,
            "oneHourSeconds": 3600,
            "abandonmentSeconds": 1800,
        },
        "parentBytesPreserved": True,
        "fixtureMutated": False,
        "runtimeExecuted": False,
        "w02Sealed": False,
        "fortressAcceptedOrApplied": False,
        "queue404": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
    }
    write_json("validation/BUILD_VALIDATION_419.json", validation)
    write_bytes("README.md", (
        "# Fortress W02 owner-adopted scribing branches (TEST_ONLY)\n\n"
        "This packet models two bounded branches under the exact owner-adopted Proposal 415 terms: a one-hour completed Flame Armor copy and a 30-minute abandonment. The preserved Return284 parent and live fixture are unchanged. The completion branch is submitted to the GPT Director for a W02 evidence sufficiency readback; it is not an acceptance or application of Fortress.\n\n"
        "The adopted premise is scoped to PG328-W02 / PG366-W02-R1. The table/support statement is local to this test and does not close the W01 support or z40 holds. The packet grants no rest benefit, resource recovery, new initiative dispatch, or canonical rule. Queue404 remains 829 reviewed/applied, 19 pending, 0 accepted-unapplied.\n\n"
        "`BUILD_VALIDATION_419.json` checks exact proposal/parent/source bindings, material and time arithmetic, branch outputs, clock offsets, and queue preservation. No runtime is claimed.\n"
    ).encode("utf-8"))

    request = {
        "schemaVersion": 1,
        "recordId": "DIRECTOR-REVIEW-REQUEST-PG328-W02-419",
        "classification": "TEST_ONLY_BRANCH_REVIEW_REQUEST",
        "reviewedMainCommit": git_commit,
        "packetPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w02_scribing_witness_419/",
        "proposal": {"path": PROPOSAL_REL, "sha256": sha(proposal_raw)},
        "ownerAdoption": {"path": ADOPTION_REL, "sha256": sha(adoption_raw), "verbatim": adoption["ownerAuthorization"]["verbatim"]},
        "branches": [
            "case/PG328_W02_SCRIBING_COMPLETION_BRANCH_419_TESTONLY.json",
            "case/PG328_W02_SCRIBING_ABANDONMENT_BRANCH_419_TESTONLY.json",
        ],
        "request": [
            "Verify the completion and abandonment branches against the exact adopted premises and cited source bytes.",
            "Confirm whether the completed, provenance-linked rank-1 Flame Armor copy is sufficient for PG328-W02 only.",
            "Confirm that the abandonment branch adds no entry, refunds no inputs, and grants no work credit.",
            "Confirm the original Return284 parent remains byte-identical and no W01/global support rule or z40 issue is resolved.",
            "Confirm Queue404 remains 829/19/0, Fortress remains held pending review of other obligations, and no acceptance/application occurred.",
        ],
        "noAcceptanceOrApplicationRequested": True,
        "noQueueChangeRequested": True,
    }
    write_json("authority/DIRECTOR_REVIEW_REQUEST_419.json", request)

    payload_files = sorted(p for p in PAYLOAD.rglob("*") if p.is_file() and p.name != "MANIFEST.json")
    manifest = {
        "schemaVersion": 1,
        "packageId": "DD-RANK9-FORTRESS-W02-SCRIBING-419-TESTONLY",
        "classification": "TEST_ONLY_DIRECTOR_REVIEW_PACKET",
        "files": [
            {"path": p.relative_to(PAYLOAD).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p.read_bytes())}
            for p in payload_files
        ],
        "sourceMainCommit": git_commit,
        "parentCaseMemberSha256": parent_member_sha,
        "ownerProposalSha256": sha(proposal_raw),
        "ownerAdoptionSha256": sha(adoption_raw),
    }
    write_json("MANIFEST.json", manifest)

    zip_path = OUT / "DD_Rank9_ConjureDemiplaneFortress_W02_Scribing_419_TESTONLY.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in PAYLOAD.rglob("*") if p.is_file()):
            arc = "payload/" + path.relative_to(PAYLOAD).as_posix()
            info = zipfile.ZipInfo(arc, date_time=(2026, 11, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    delivery = {
        "schemaVersion": 1,
        "deliveryId": "DD-RANK9-FORTRESS-W02-SCRIBING-419-TESTONLY-DELIVERY",
        "classification": "TEST_ONLY_NOT_CANONICAL_NOT_ACCEPTED",
        "packet": zip_path.name,
        "packetBytes": zip_path.stat().st_size,
        "packetSha256": sha(zip_path.read_bytes()),
        "manifestSha256": sha((PAYLOAD / "MANIFEST.json").read_bytes()),
        "validationPath": "payload/validation/BUILD_VALIDATION_419.json",
        "reviewRequestPath": "payload/authority/DIRECTOR_REVIEW_REQUEST_419.json",
        "queueAtBuild": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0},
        "fortressDisposition": "HELD_PENDING_DIRECTOR_REVIEW_AND_OTHER_OPEN_OBLIGATIONS",
        "identityAcceptedOrApplied": False,
        "parentBytesMutated": False,
        "fixtureMutated": False,
        "runtimeExecuted": False,
    }
    (OUT / "DELIVERY_419.json").write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "DIRECTOR_REVIEW_REQUEST_419.json").write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "BUILD_VALIDATION_419.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": validation["status"], "checks": len(checks), "packet": str(zip_path), "packetBytes": delivery["packetBytes"], "packetSha256": delivery["packetSha256"], "mainCommit": git_commit}, indent=2))


if __name__ == "__main__":
    main()
