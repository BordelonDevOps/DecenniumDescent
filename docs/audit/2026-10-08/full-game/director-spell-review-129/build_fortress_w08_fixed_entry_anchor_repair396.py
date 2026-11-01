from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zipfile
from datetime import datetime, timezone


HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "fortress_w08_support_cover_locator_repair_395"
OUT = HERE / "fortress_w08_fixed_entry_anchor_repair_396"
SOURCE_ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_SupportCoverLocator395_TESTONLY.zip"
ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_TESTONLY.zip"
CASE_MEMBER = "payload/cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json"
CASE_SHA = "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900"
TERM_NAME = "OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

PREBUILD = "PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json"
MANIFEST = "PG328-W08_PREBUILD_SOURCE_BINDINGS_396.json"
GEOMETRY = "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_396_TESTONLY.json"
CARRIER = "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_396_TESTONLY.json"
SUPPORT = "OWNER_PG328_W08_SUPPORT_COVER_CONTRACT_396_TESTONLY.json"
REQUEST = "PG328-W08_DIRECTOR_REVIEW_REQUEST_396.json"
DIRECTOR = "DIRECTOR_PG328_W08_SUPPORT_COVER_REVIEW_395.json"
DELIVERY = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_TESTONLY_DELIVERY.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jbytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def put_json(path: pathlib.Path, value: object) -> bytes:
    raw = jbytes(value)
    path.write_bytes(raw)
    return raw


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_zip_path = SOURCE / SOURCE_ZIP_NAME
    source_delivery = read_json(SOURCE / "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_SupportCoverLocator395_TESTONLY_DELIVERY.json")
    with zipfile.ZipFile(source_zip_path) as old_zip:
        old_files = {name: old_zip.read(name) for name in old_zip.namelist()}
    case_bytes = old_files[CASE_MEMBER]
    assert sha(case_bytes) == CASE_SHA
    case = json.loads(case_bytes)
    cross = case["events"][6]
    assert cross["kind"] == "CROSSING" and cross["after"]["actors"]["A"]["position"] == [15, 10, 0]
    assert cross["after"]["actors"]["A"]["plane"].endswith("/space")
    assert cross["after"]["transitReceipts"][0]["committedMovement"] == 5

    source_pointer = "/events/6"
    procedure_pointer = "payload/rules/PG328_PROCEDURE_CURRENT.json#/sharedContract/cellExtension/closure/secondaryAnchors"
    crossing_id = cross["id"]
    fixed_anchor = {
        "status": "DIRECTOR_CONFIRMED_FIXED_ADMISSION_CLOSURE_ANCHOR; BRANCH_PREMISE_REMAINS_UNADOPTED",
        "historicalAdmission": {
            "caseMember": CASE_MEMBER,
            "jsonPointer": source_pointer,
            "eventId": crossing_id,
            "eventKind": "CROSSING",
            "eventTimeSeconds": cross["time"],
            "transitReceiptId": cross["after"]["transitReceipts"][0]["id"],
            "before": {"plane": "fixture:origin", "feet": [5, 0, 0]},
            "after": {"plane": cross["after"]["actors"]["A"]["plane"], "feet": [15, 10, 0]},
            "committedMovementFeet": 5,
            "inheritedCaseBytesMutated": False,
        },
        "q27AnchorDerivation": {
            "ruleSource": procedure_pointer,
            "retainedInteriorEntryFeet": [15, 10, 0],
            "interiorEntranceReferenceFeet": [10, 10, 0],
            "stableAdmissionOffsetFeet": [5, 0, 0],
            "exteriorEntranceAnchorFeet": [10, 0, 0],
            "fixedClosureAnchorFeet": [15, 0, 0],
            "derivation": "Project the retained cell-local admission offset [5,0,0] onto the primary fixed world axes at exterior entrance [10,0,0]. The later W08 branch initialization does not redefine this recorded anchor.",
            "notAGroundProjection": True,
            "verticalAdjustmentFeet": 0,
            "directorFinding": "Q27 supplies no general projection-to-ground permission; this closure anchor is fixed by retained admission history. No falling episode follows merely from the interior/exterior height difference.",
        },
        "testOnlyBranchInitialization": {
            "status": "SEPARATE_NEW_BRANCH_PREMISE_PENDING_OWNER_ADOPTION",
            "afterRetainedAdmissionPointer": source_pointer,
            "actorAFeetBefore": [15, 10, 0],
            "actorAFeetInProposedRaisedBranch": [15, 10, 1 / 12],
            "carriedItemsRaisedByFeet": 1 / 12,
            "purpose": "Place A's complete footprint on the proposed one-inch support panel for this W08 TEST_ONLY branch.",
            "changesHistoricalEntryOrFixedClosureAnchor": False,
            "ownerAdoptionRequired": True,
        },
        "q27TerminalPlacement": {
            "fixedAnchorFeet": [15, 0, 0],
            "sourcePlane": "fixture:origin",
            "sourceSupportZ": 0,
            "verticalProjectionOrSnap": False,
            "sourcePlacementAndCollisionChecksRequired": True,
        },
    }

    director = {
        "id": "DIRECTOR-PG328-W08-SUPPORT-COVER-REVIEW-395",
        "createdAtUtc": NOW,
        "sourcePacket": source_delivery["artifact"],
        "sourcePacketSha256": source_delivery["sha256"],
        "reviewStatus": "DIRECTOR_REVIEW_COMPLETE_REQUIRES_TWO_RECORD_CORRECTIONS_BEFORE_OWNER_ADOPTION",
        "decision": "395 support, exposed-face geometry, carrier bounds, and corrected locators pass prebuild review as proposed TEST_ONLY inputs; two record corrections are required before owner adoption and integration.",
        "findings": {
            "packetIntegrity": {"bytes": 477272, "members": 30, "sha256": source_delivery["sha256"], "sourceBindingsReconcile": True, "inheritedCaseAndFinalStateUnchanged": True},
            "supportPremise": {"panel": "W08-FLOOR-PANEL-A-01", "volumeZFeet": [0, 1 / 12], "lowerFaceBearsOnInheritedZ0": True, "supportsCompleteFootprintAtZ": 1 / 12, "loadLb": 162, "newPremiseOwnerAdoptionRequired": True, "completesW01CompatibleDamage": False},
            "exposedContact": {"patchFeet": {"x": 17.5, "y": [12, 12.5], "z": [1 / 48, 1 / 16]}, "rayClearsPanelUntilContact": True, "rayClearsAItemsWallsAndStairs": True, "oncePanelPremiseAdoptedAndLawfulPaidFieldDemonstrated": "The exposed surface belongs to the occupied panel's magical structural expression; RW149-F can suppress the reached expression and Q27 then supplies whole-Fortress termination. No propagation through A, panel penetration, or hidden-volume suppression is inferred."},
            "returnPlacement": {"fixedClosureAnchorFeet": [15, 0, 0], "historicalAdmissionPointer": source_pointer, "rulePointer": procedure_pointer, "groundSnapNeeded": False, "fallingFromInteriorExteriorHeightDifference": False},
            "carrier": {"dimensionsAttachmentsHandsFocusLoadTranslationsAndCollisionChecksPass": True, "allFourCasePointersResolve": True},
            "terminationProposal386": {"status": "COHERENT_PENDING_SEPARATE_OWNER_ADOPTION", "deadlineSeconds": 66.1, "validOnlyIfEstablishmentRemainsAtWorldSeconds": 6.1},
        },
        "requiredCorrections": [
            "Replace projection/negative-one-twelfth explanations in support, geometry, carrier, and prebuild records with the fixed-admission-anchor derivation bound to unchanged /events/6; record the raised arrangement as separate TEST_ONLY branch initialization after retained admission.",
            "Set prebuild conditionalTerminalPlan/bodyA/currentFeet to [15,10,1/12] for the proposed branch while separately retaining the historical entry position and fixed closure anchor; preserve inherited case bytes.",
        ],
        "nextStep": "Bind these corrections and this ruling, obtain owner adoption of corrected support/placement premises and unchanged termination proposal 386, then build the reversible W08 witness.",
        "unchangedState": {"fixtureMutated": False, "cast": False, "settlement": False, "seal": False, "fortressAcceptedOrApplied": False, "identityHold": "PG200-B06", "queue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0}},
    }
    director_raw = jbytes(director)
    director_hash = sha(director_raw)

    geometry_name = "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_395_TESTONLY.json"
    carrier_name = "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_395_TESTONLY.json"
    support_name = "OWNER_PG328_W08_SUPPORT_COVER_CONTRACT_395_TESTONLY.json"
    request_name = "PG328-W08_DIRECTOR_REVIEW_REQUEST_395.json"
    packet = json.loads(old_files["payload/" + PREBUILD])
    geometry = json.loads(old_files["payload/proposals/" + geometry_name])
    carrier = json.loads(old_files["payload/proposals/" + carrier_name])
    support = json.loads(old_files["payload/proposals/" + support_name])

    # Geometry proposal: retain the physical panel and contact findings, correcting only the anchor interpretation.
    geometry["id"] = "PG328-W01-W08-OCCUPIED-PANEL-GEOMETRY-PROPOSAL-396"
    geometry["createdAtUtc"] = NOW
    geometry["status"] = "DIRECTOR_REVIEWED_SUPPORT_AND_CONTACT_PROPOSAL_PENDING_OWNER_ADOPTION; FIXED_ANCHOR_CORRECTION_396"
    geometry["supersedes"] = geometry["id"].replace("396", "395")
    geometry["directorReview395"] = {"path": DIRECTOR, "sha256": director_hash, "decision": "Support/contact pass as proposed TEST_ONLY inputs; apply exact anchor correction."}
    geometry["fixedClosureAnchor396"] = fixed_anchor
    geometry.pop("verticalReturnProjection395", None)
    geometry["occupiedPanel"]["branchInitialization396"] = copy.deepcopy(fixed_anchor["testOnlyBranchInitialization"])
    geometry_raw = jbytes(geometry)
    geometry_hash = sha(geometry_raw)

    # Carrier proposal: terminal coordinates already fit at the fixed anchor; remove the false projection premise.
    carrier["id"] = "PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-396"
    carrier["createdAtUtc"] = NOW
    carrier["status"] = "DIRECTOR_REVIEWED_CARRIER_CHECKS_PASS; FIXED_ADMISSION_ANCHOR_AND_BRANCH_PLACEMENT_PENDING_OWNER_ADOPTION"
    carrier["supersedes"] = carrier["id"].replace("396", "395")
    carrier["sourceBindings"][-1].update({"path": "payload/proposals/" + GEOMETRY, "sha256": geometry_hash,
                                          "use": "Director-reviewed one-inch support panel, separate raised TEST_ONLY branch initialization, and fixed Q27 admission anchor."})
    carrier["postReturnCheck"].pop("verticalReturnProjection", None)
    carrier["fixedAdmissionAnchor396"] = copy.deepcopy(fixed_anchor)
    carrier.pop("returnVerticalProjection395", None)
    carrier["reviewLimit"] = "Carrier placement and the fixed closure anchor are Director-reviewed candidate inputs; owner adoption is still required. No case mutation, cast, settlement, or integration is authorized."
    carrier_raw = jbytes(carrier)
    carrier_hash = sha(carrier_raw)

    # Support/cover contract: incorporate the Director's exact decision without adopting the premise.
    support["id"] = "OWNER-PG328-W08-SUPPORT-COVER-CONTRACT-PROPOSAL-396"
    support["createdAtUtc"] = NOW
    support["status"] = "DIRECTOR_REVIEWED_PROPOSED_TEST_ONLY_SUPPORT_AND_BRANCH_PLACEMENT_PENDING_OWNER_ADOPTION"
    support["directorFinding395"] = {"path": DIRECTOR, "sha256": director_hash, "decision": director["decision"]}
    support["fixedClosureAnchor396"] = copy.deepcopy(fixed_anchor)
    support.pop("verticalTerminalProjection", None)
    support["requestedDirectorDecision"] = [
        "The Director found the exact one-inch support panel and 162-lb supported load sufficiently precise as a proposed TEST_ONLY premise; owner adoption remains required and W01 compatible damage stays open.",
        "Once the panel premise is adopted and a lawful paid field is demonstrated, exposed-face contact reaches the occupied panel's magical structural expression for RW149-F/Q27; no hidden-volume suppression is inferred.",
        "Use the fixed Q27 closure anchor [15,0,0] derived from retained crossing /events/6 and PG328_PROCEDURE_CURRENT.json#/sharedContract/cellExtension/closure/secondaryAnchors. The later raised branch arrangement does not redefine it; no ground projection is used.",
        "Carrier dimensions, attachments, hand/focus arrangement, load, and collision checks pass; all four exact case pointers resolve.",
        "Proposal 386 remains coherent for separate owner adoption, with deadline 66.1 seconds only if establishment remains at world 6.1.",
    ]
    support["requiredOwnerAdoption"] = {
        "supportPremise": "Adopt W08-FLOOR-PANEL-A-01 as the one-inch load-bearing magical panel z=[0,1/12], lower face on inherited z=0 support, supporting A's complete footprint and 162 lb in this W08 TEST_ONLY branch only.",
        "branchInitialization": "After unchanged retained admission at /events/6 (A feet [15,10,0]), initialize a separate TEST_ONLY branch with A and carried boxes raised by 1/12 ft so A's feet are [15,10,1/12]. This does not rewrite history or the fixed closure anchor.",
        "fixedQ27Anchor": "At Q27 closure use [15,0,0] on fixture:origin, derived from retained interior entry [15,10,0], interior entrance [10,10,0], and exterior anchor [10,0,0] under the bound secondaryAnchors rule.",
        "terminationProposal386": {"path": "payload/proposals/" + TERM_NAME, "sha256": "023cae4cc3ed4e3f944a7b9c95645dee84b8b4722c121d36d3eff8d4f440c8e1", "terms": "Independent field ends after Q27 source termination without relocation, refund, or lost history; use deadline 66.1 only if established at world 6.1."},
        "limitations": ["TEST_ONLY for PG328-W08 only", "no canonical rule change", "no fixture mutation", "no cast or settlement", "no W01 compatible-damage completion", "no Fortress acceptance/application", "PG200-B06 remains held", "no ordinary queue change"],
    }
    support_raw = jbytes(support)
    support_hash = sha(support_raw)

    request = {
        "id": "PG328-W08-DIRECTOR-REVIEW-REQUEST-396",
        "createdAtUtc": NOW,
        "scope": "Exact record correction to the Director-reviewed 395 support/contact and carrier proposal; no premises adopted.",
        "sourcePacket395": {"path": source_delivery["artifact"], "sha256": source_delivery["sha256"]},
        "directorReview395": {"path": DIRECTOR, "sha256": director_hash},
        "reviewQuestions": [
            "Confirm 396 implements your exact two record corrections: binds retained admission to unchanged /events/6 and records the z=1/12 arrangement as a separate TEST_ONLY branch initialization; sets the proposed branch current feet to [15,10,1/12] while preserving historical [15,10,0] and fixed closure anchor [15,0,0].",
            "Confirm no -1/12 projection or ground snap remains, and that the fixed anchor derivation from /events/6 and secondaryAnchors is represented faithfully.",
            "Confirm the one-inch support/contact findings, carrier checks, and proposal 386 remain as previously ruled; identify any mismatch before owner adoption.",
            "If this correction packet is faithful, confirm that the remaining owner adoption is exactly the scoped support and raised-branch initialization terms in support contract 396 plus unchanged termination proposal 386, before the reversible W08 witness.",
        ],
        "doNot": ["adopt proposal 396 or proposal 386", "cast or settle", "mutate the inherited case or fixture", "accept/apply Fortress", "clear PG200-B06", "change any seal, hold, or queue"],
        "queue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
    }
    request_raw = jbytes(request)

    # Apply corrected facts to the proposed prebuild without changing its inherited case member.
    packet["id"] = "PG328-W08-OCCUPIED-ANTIMAGIC-FIXED-ENTRY-ANCHOR-CORRECTION-396"
    packet["createdAtUtc"] = NOW
    packet["status"] = "DIRECTOR_REVIEWED_RECORD_CORRECTIONS_PENDING_FINAL_DIRECTOR_CONFIRMATION_AND_OWNER_ADOPTION"
    packet["scope"]["supersedes"] = "PG328-W08-OCCUPIED-ANTIMAGIC-SUPPORT-COVER-LOCATOR-REPAIR-395"
    packet["scope"]["ownerAdoptionOf396"] = False
    packet["scope"]["ownerAdoptionOf395"] = False
    packet["scope"]["noCanonicalRuleChange"] = True
    packet["proposedGeometryProposal395"]["status"] = "SUPERSEDED_BY_PROPOSAL_396; DIRECTOR_REVIEWED_WITH_FIXED_ANCHOR_CORRECTION"
    packet["proposedCarrierBounds395"]["status"] = "SUPERSEDED_BY_PROPOSAL_396; DIRECTOR_REVIEWED_WITH_FIXED_ANCHOR_CORRECTION"
    packet["proposedSupportCoverContract395"]["status"] = "SUPERSEDED_BY_PROPOSAL_396; DIRECTOR_REVIEWED_WITH_FIXED_ANCHOR_CORRECTION"
    packet["proposedGeometryProposal394"]["status"] = "SUPERSEDED_BY_PROPOSAL_395_AND_396"
    packet["proposedCarrierBounds394"]["status"] = "SUPERSEDED_BY_PROPOSAL_395_AND_396"
    packet["proposedCastState"]["proposedCastAfterRefresh"]["centerCandidate"]["geometryProposal"] = "396 only; neither adopted nor executed"
    body = packet["conditionalTerminalPlan"]["bodyA"]
    body["currentFeet"] = [15, 10, 1 / 12]
    body["historicalEntryPositionFeet"] = [15, 10, 0]
    body["historicalEntrySource"] = {"caseMember": CASE_MEMBER, "jsonPointer": source_pointer, "eventId": crossing_id}
    body["fixedClosureAnchor396"] = copy.deepcopy(fixed_anchor["q27AnchorDerivation"])
    body["candidateExteriorPlacementFeet"] = [15, 0, 0]
    body["status"] = "Raised current feet describe the separate proposed TEST_ONLY branch after retained admission; closure placement remains the fixed Q27 anchor derived from /events/6."
    packet["candidateGeometry"].pop("verticalReturnProjection395", None)
    packet["candidateGeometry"]["sourceGeometry"]["source"] = "Q23 answer plus unchanged inherited case and Director-reviewed, unadopted proposal 396"
    packet["candidateGeometry"]["occupiedPanelProposal396"] = packet["candidateGeometry"].pop("occupiedPanelProposal395")
    packet["candidateGeometry"]["fixedClosureAnchor396"] = copy.deepcopy(fixed_anchor)
    packet["candidateGeometry"]["branchInitializationPremise"] = copy.deepcopy(fixed_anchor["testOnlyBranchInitialization"])
    packet["candidateGeometry"]["fieldIntersectionAndCoverProposal396"] = geometry["fieldIntersectionAndCover"]
    packet["candidateGeometry"].pop("fieldIntersectionAndCoverProposal395", None)
    packet["conditionalTerminalPlan"]["placementBoundsProposal"] = "PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-396"
    packet["openRequirementsBeforeIntegratedWitness"][0]["requirement"] = "Owner-adopt the Director-reviewed support panel and separate raised TEST_ONLY branch initialization; W01 compatible damage remains open."
    packet["openRequirementsBeforeIntegratedWitness"][0]["sourceStatus"] = "Director review 395 passed scoped support/contact geometry; 396 corrects fixed-anchor record and awaits owner adoption."
    packet["openRequirementsBeforeIntegratedWitness"][1]["sourceStatus"] = "Proposal 386 remains unchanged and not adopted; owner adoption is required before integrated terminal execution."
    packet["openRequirementsBeforeIntegratedWitness"][4]["requirement"] = "Only after owner adoption of the corrected support/placement premises and proposal 386, build reversible integrated W08 witness with proposal 396 carrier bounds."
    packet["directorReviewRequest"] = {"path": REQUEST, "sha256": sha(request_raw), "questions": request["reviewQuestions"]}
    packet["proposedGeometryProposal396"] = {"path": GEOMETRY, "status": geometry["status"], "sha256": geometry_hash}
    packet["proposedCarrierBounds396"] = {"path": CARRIER, "status": carrier["status"], "sha256": carrier_hash}
    packet["proposedSupportCoverContract396"] = {"path": SUPPORT, "status": support["status"], "sha256": support_hash}
    packet["fixedEntryAnchorCorrection396"] = {
        "directorReview395Sha256": director_hash,
        "sourceCrossingPointer": source_pointer,
        "fixedClosureAnchorFeet": [15, 0, 0],
        "historicalEntryPositionFeet": [15, 10, 0],
        "proposedBranchCurrentFeet": [15, 10, 1 / 12],
        "noGroundProjectionOrAdjustment": True,
        "ownerAdoptionOf396": False,
    }
    packet["ordinaryQueueSnapshot"] = {"applied": 828, "pending": 20, "acceptedUnapplied": 0}
    packet_raw = jbytes(packet)
    packet_hash = sha(packet_raw)

    manifest = json.loads(old_files["authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_395.json"])
    manifest["id"] = "PG328-W08-PREBUILD-SOURCE-BINDINGS-396"
    manifest["createdAtUtc"] = NOW
    manifest["status"] = "HASH_VERIFIED_DIRECTOR_REVIEWED_FIXED_ENTRY_ANCHOR_CORRECTION_396_PENDING_ADOPTION"
    manifest["prebuildPath"] = PREBUILD
    manifest["prebuildSha256"] = packet_hash
    manifest["supersedesManifest"] = "PG328-W08-PREBUILD-SOURCE-BINDINGS-395"
    manifest["bundleMemberPath"] = "payload/" + PREBUILD
    manifest["priorDirectorReview395"] = {"bundleMember": "payload/reviews/" + DIRECTOR, "sha256": director_hash, "bytes": len(director_raw)}
    manifest["reviewProposals396"] = [
        {"name": GEOMETRY, "bundleMember": "payload/proposals/" + GEOMETRY, "sha256": geometry_hash, "bytes": len(geometry_raw)},
        {"name": CARRIER, "bundleMember": "payload/proposals/" + CARRIER, "sha256": carrier_hash, "bytes": len(carrier_raw)},
        {"name": SUPPORT, "bundleMember": "payload/proposals/" + SUPPORT, "sha256": support_hash, "bytes": len(support_raw)},
        {"name": TERM_NAME, "bundleMember": "payload/proposals/" + TERM_NAME, "sha256": "023cae4cc3ed4e3f944a7b9c95645dee84b8b4722c121d36d3eff8d4f440c8e1", "status": "UNCHANGED; OWNER ADOPTION REQUIRED"},
    ]
    manifest["reviewRequest396"] = {"bundleMember": "payload/" + REQUEST, "sha256": sha(request_raw), "bytes": len(request_raw)}
    manifest["caseMemberBinding"]["bundleMember"] = CASE_MEMBER
    manifest["caseMemberBinding"]["memberSha256"] = CASE_SHA
    manifest["caseMemberBinding"]["memberBytes"] = len(case_bytes)
    manifest["nonAdoptionNotice"] = "The Director-reviewed support/contact findings do not adopt the new panel or raised-branch premises. Proposal 386 remains unadopted. No cast, settlement, fixture mutation, seal, Fortress acceptance/application, hold change, or queue change."
    manifest_raw = jbytes(manifest)

    files = {
        f"payload/{PREBUILD}": packet_raw,
        f"payload/{REQUEST}": request_raw,
        f"payload/proposals/{GEOMETRY}": geometry_raw,
        f"payload/proposals/{CARRIER}": carrier_raw,
        f"payload/proposals/{SUPPORT}": support_raw,
        f"authority/{MANIFEST}": manifest_raw,
        f"payload/reviews/{DIRECTOR}": director_raw,
    }
    # Save reviewable sidecars alongside the archive.
    for member, raw in files.items():
        name = pathlib.Path(member).name
        (OUT / name).write_bytes(raw)
    (OUT / DELIVERY).write_text("{}\n", encoding="utf-8")

    prior395_members = {
        "authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_395.json",
        "payload/" + PREBUILD,
        "payload/PG328-W08_DIRECTOR_REVIEW_REQUEST_395.json",
        "payload/proposals/" + geometry_name,
        "payload/proposals/" + carrier_name,
        "payload/proposals/" + support_name,
    }
    zip_path = OUT / ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in old_files.items():
            z.writestr(("prior395/" + name) if name in prior395_members else name, raw)
        for member, raw in files.items():
            z.writestr(member, raw)

    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(set(z.namelist()))
        assert z.read(CASE_MEMBER) == case_bytes and sha(z.read(CASE_MEMBER)) == CASE_SHA
        assert json.loads(z.read("payload/" + PREBUILD))["conditionalTerminalPlan"]["bodyA"]["currentFeet"] == [15, 10, 1 / 12]
        assert json.loads(z.read("payload/" + PREBUILD))["conditionalTerminalPlan"]["bodyA"]["historicalEntryPositionFeet"] == [15, 10, 0]
        assert json.loads(z.read("payload/proposals/" + GEOMETRY))["fixedClosureAnchor396"]["historicalAdmission"]["jsonPointer"] == "/events/6"
        assert json.loads(z.read("payload/proposals/" + CARRIER))["postReturnCheck"]["exteriorFeetAnchor"] == [15, 0, 0]
        joined = b"".join(files.values())
        assert b"verticalReturnProjection395" not in joined
        assert b"returnVerticalProjection395" not in joined
        assert b"explicitVerticalAdjustmentFeet" not in joined
        assert z.read(CASE_MEMBER) == old_files[CASE_MEMBER]
        assert json.loads(z.read("payload/proposals/" + SUPPORT))["scope"]["ownerAdoptionRequired"] is True

    delivery = {
        "id": "DD-RANK9-PG328-W08-FIXED-ENTRY-ANCHOR-CORRECTION-396-TESTONLY-DELIVERY",
        "createdAtUtc": NOW,
        "status": "READY_FOR_DIRECTOR_CONSISTENCY_REVIEW_PENDING_TRANSMISSION",
        "supersedes": source_delivery["id"],
        "artifact": ZIP_NAME,
        "sha256": sha(zip_path.read_bytes()),
        "bytes": zip_path.stat().st_size,
        "bundleMemberCount": len(zipfile.ZipFile(zip_path).infolist()),
        "prebuildSha256": packet_hash,
        "sourceBindingsSha256": sha(manifest_raw),
        "geometryProposalSha256": geometry_hash,
        "carrierProposalSha256": carrier_hash,
        "supportCoverContractSha256": support_hash,
        "reviewRequestSha256": sha(request_raw),
        "directorReview395Sha256": director_hash,
        "originalCaseMemberSha256": CASE_SHA,
        "originalCaseBytesUnchanged": True,
        "ownerAdoptionOf396": False,
        "terminationProposal386Sha256": "023cae4cc3ed4e3f944a7b9c95645dee84b8b4722c121d36d3eff8d4f440c8e1",
        "directorConversation": source_delivery["directorConversation"],
        "fixtureMutated": False,
        "actualCast": False,
        "q27Settlement": False,
        "fortressAcceptedOrApplied": False,
        "identityHold": "PG200-B06 remains held",
        "ordinaryQueue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
        "transmissionStatus": "NOT_YET_SENT",
    }
    put_json(OUT / DELIVERY, delivery)
    print(json.dumps({"directory": str(OUT), "zip": str(zip_path), "sha256": delivery["sha256"],
                      "bytes": delivery["bytes"], "members": delivery["bundleMemberCount"],
                      "geometrySha256": geometry_hash, "carrierSha256": carrier_hash,
                      "supportSha256": support_hash, "prebuildSha256": packet_hash,
                      "manifestSha256": sha(manifest_raw), "caseSha256": sha(case_bytes),
                      "currentFeet": body["currentFeet"], "historicalEntry": body["historicalEntryPositionFeet"],
                      "closureAnchor": body["candidateExteriorPlacementFeet"], "integrity": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
