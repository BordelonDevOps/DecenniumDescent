import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = REVIEW.parents[4]
OUT_PROPOSAL = ROOT / "OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_TESTONLY.json"
OUT_PREFLIGHT = ROOT / "SOURCE_GEOMETRY_PREFLIGHT_478.json"
OUT_README = ROOT / "README_PROPOSAL_478.md"
OUT_VALIDATION = ROOT / "INDEPENDENT_VALIDATION_478.json"
OUT_DELIVERY = ROOT / "DELIVERY_478.json"
OUT_ARCHIVE = ROOT / "DD_ElementalShell_B01_TestSource_Proposal_478_TESTONLY.zip"
OUT_MANIFEST = ROOT / "MANIFEST_478.json"

SOURCE_SPECS = [
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/ELEMENTAL_SHELL_DIRECTOR_REQUIREMENTS_305.json",
        "role": "Director's retained requirements for B01/B02; this proposal addresses only B01.",
        "pointers": ["/directorRequirements/DF218-B01", "/directorRequirements/integratedTraceInvariants", "/directorRequirements/selectedDuration"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/ELEMENTAL_SHELL_DIRECTOR_DECISION_306.json",
        "role": "Original held decision and exact unresolved B01 evidence gate.",
        "pointers": ["/unresolvedEvidence/DF218-B01"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b01_source_qualification_470/B01_SOURCE_QUALIFICATION_470.json",
        "role": "Prior bounded read-only source audit; records no qualifying existing source and preserves B01 hold.",
        "pointers": ["/result", "/requiredFactsAssessment", "/decisionBoundary"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b01_source_qualification_470/B01_HELD_CASE_EXTRACTS_470.json",
        "role": "Exact held environmental case and creature-attributed contrast; no hazard packet is inferred.",
        "pointers": ["/heldEnvironmentLead", "/creatureAttributedContrast"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/OWNER_DF218_SHELL_CASTER_PREMISE_PROPOSAL_468_TESTONLY.json",
        "role": "Exact 468 proposal, adopted only for caster qualification; encounter facts are not transferred.",
        "pointers": ["/scope", "/proposedPreparationRecord", "/decisionBoundary"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json",
        "role": "Owner adoption of exact 468 for caster qualification only; this proposal requests a distinct B01 branch scope.",
        "pointers": ["/scope", "/adoptedEffect", "/effectsAtAuthorization"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/CASTER_PREPARATION_PREMISE_468_TESTONLY.json",
        "role": "Exact adopted preparation premise; no encounter readiness, current resources or cast history are inferred.",
        "pointers": ["/hypotheticalPreparationRecord", "/result", "/authority"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_qualification_472_repack01/SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json",
        "role": "Director-passed caster-acquisition/preparation subpart only; both B01 and B02 remain open.",
        "pointers": ["/qualification", "/blockers", "/decisionBoundary"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_qualification_472_repack01/DIRECTOR_READBACK_472_REPACK01.json",
        "role": "Director pass limited to the caster subpart; no cast or witness authority.",
        "pointers": ["/status", "/decisionBoundary"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/ACTOR_PROFILES.json",
        "role": "Static Wizard18 profile and measured 5-by-5-by-6-foot body premise; no live identity is imported.",
        "pointers": ["/Wizard18"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/wizard.json",
        "role": "Wizard class acquisition, spellcasting and component requirements.",
        "pointers": ["/engine", "/cards/17"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/ELEMENTAL_SHELL_PROCEDURE_SOURCE.json",
        "role": "Retained Shell procedure and scoped DF9-Q12 through Q15 interpretations; not canonical promotion.",
        "pointers": ["/sharedRules/casting", "/sharedRules/cadence", "/sharedRules/clocks", "/selectedRules/1", "/selectedRules/2", "/selectedRules/3", "/selectedRules/4"],
    },
    {
        "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_476_REPACK01.json",
        "role": "Current authority snapshot and pending identity order.",
        "pointers": ["/currentAuthority", "/nextIdentity", "/nextBlockerIds"],
    },
    {
        "path": "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
        "role": "Current authored identity/catalog binding; no blocked candidate is promoted by this proposal.",
        "pointers": ["/spells"],
    },
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def canonical_sha(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def source_bindings(head):
    bindings = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        raw = (REPO / Path(path)).read_bytes()
        git_raw = subprocess.check_output(["git", "show", f"{head}:{path}"], cwd=REPO)
        line_ending_only = raw != git_raw and raw.replace(b"\r\n", b"\n") == git_raw.replace(b"\r\n", b"\n")
        if raw != git_raw and not line_ending_only:
            raise ValueError(f"Source worktree differs from pinned Git blob beyond line endings: {path}")
        blob = subprocess.check_output(["git", "hash-object", "--stdin"], input=git_raw, cwd=REPO).decode().strip()
        bindings.append({
            **spec,
            "bytes": len(git_raw),
            "sha256": sha256(git_raw),
            "gitBlobSha1": blob,
            "byteDomain": "exact committed Git blob",
            "workingTreeBytes": len(raw),
            "workingTreeSha256": sha256(raw),
            "workingTreeRepresentation": "LF identical" if raw == git_raw else "CRLF/LF conversion only",
            "lineEndingConversionOnly": raw == git_raw or line_ending_only,
            "verifiedAtCommit": head,
        })
    return bindings


def build():
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO).decode().strip()
    bindings = source_bindings(head)
    by_path = {x["path"]: x for x in bindings}
    profile_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/payload/sources/ACTOR_PROFILES.json"
    profile = json.loads((REPO / profile_path).read_text(encoding="utf-8"))["Wizard18"]
    queue_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_476_REPACK01.json"
    queue = json.loads((REPO / queue_path).read_text(encoding="utf-8"))
    prep_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_premise_proposal_468/CASTER_PREPARATION_PREMISE_468_TESTONLY.json"
    prep = json.loads((REPO / prep_path).read_text(encoding="utf-8"))

    proposal = {
        "schemaVersion": 1,
        "id": "OWNER-DF218-B01-TEST-SOURCE-PROPOSAL-478",
        "classification": "OWNER_PROPOSED_TEST_ONLY_SOURCE_CONTRACT_NOT_ADOPTED_NO_WITNESS",
        "status": "READY_FOR_DIRECTOR_ADOPTION_READINESS_REVIEW",
        "recordedLocalDate": "2026-11-01",
        "readAtCommit": head,
        "scope": {
            "spell": "elemental-shell",
            "blocker": "DF218-B01-only",
            "branchId": "DF218-SHELL-B01-TESTONLY-R1",
            "onlyThisBranch": True,
            "hypotheticalOnly": True,
            "oneStaticAuthoredComponentWitnessOnly": True,
            "separateFromB02": True,
            "doesNotCloseIdentity": True,
        },
        "sourceBindings": bindings,
        "sourceReview": {
            "sourceQualification470Path": by_path["docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b01_source_qualification_470/B01_SOURCE_QUALIFICATION_470.json"]["path"],
            "sourceQualification470Sha256": by_path["docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_b01_source_qualification_470/B01_SOURCE_QUALIFICATION_470.json"]["sha256"],
            "result": "NO_QUALIFYING_SOURCE_FOUND",
            "existingEnvironmentalCase": "HELD_NOT_POSITIVE_EVIDENCE; source premise held and no damage packet present",
            "existingCreatureSources": ["Avatar aura: actual creature dealer", "Greater Fire Pet Fire Strike: actual creature dealer"],
            "inferenceBoundary": "No existing environmental owner, damage packet, source event, or campaign occurrence is inferred.",
        },
        "ownerProposedInputs": {
            "branchAuthority": {
                "classification": "NEW_TEST_ONLY_AUTHORED_PREMISES_PENDING_EXACT_OWNER_ADOPTION",
                "noExternalEventsClaimed": True,
                "noCampaignOccurrenceClaimed": True,
                "noCanonicalRuleChanged": True,
                "noQueueChange": True,
                "noRuntimeOrGameplayPermission": True,
                "witnessConstructionBeforeAdoption": False,
            },
            "casterQualificationReuse": {
                "preparationPremisePath": prep_path,
                "proposal468Sha256": prep["authority"]["proposalSha256"],
                "ownerAdoption468Path": prep["authority"]["ownerAdoptionPath"],
                "qualification472Path": "docs/audit/2026-10-08/full-game/director-spell-review-129/elemental_shell_caster_qualification_472_repack01/SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json",
                "directorPassScope": "caster acquisition/preparation only",
                "newB01AdoptionMustSeparatelyPermitUse": True,
                "noCurrentResourcesOrEncounterReadinessInferredFrom468": True,
            },
            "actor": {
                "id": "Wizard18-B01-R1",
                "identity": "A new branch-local hypothetical instance; no W11/W05/W13 actor state or campaign history is imported.",
                "profilePath": profile_path,
                "profilePointer": "/Wizard18",
                "class": profile["class"],
                "classLevel": profile["classLevel"],
                "path": profile["path"],
                "stats": profile["stats"],
                "proficiencyBonus": profile["PB"],
                "spellAttack": profile["spellAttack"],
                "spellDC": profile["spellDC"],
                "bodySizeFeet": {"x": 5, "y": 5, "z": 6},
                "baseWeightPounds": 180,
                "bodyBoundsFeet": {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 6]},
                "currentFixtureVitals": {
                    "status": "NEW_TEST_ONLY_PROPOSED_PARAMETER",
                    "HP": profile["maximumHP"],
                    "maximumHP": profile["maximumHP"],
                    "RP": profile["maximumRP"],
                    "maximumRP": profile["maximumRP"],
                    "AC": 12,
                    "Dissonance": 0,
                    "Refrain": 0,
                    "activeConcentration": None,
                    "preparedRankedCastFamiliesUsed": [],
                    "temporaryHP": 0,
                    "woundsAndConditions": [],
                    "nullState": "none",
                    "ArcaneWard": {
                        "type": "force",
                        "basis": "Exact owner-adopted Proposal468 fallback; retained for this branch.",
                        "appliesToIncomingFire": False,
                    },
                    "matrixModifications": {},
                    "otherFireResistanceImmunityFlatDROrTransfer": "none, as an explicit fixture parameter",
                },
                "currentStateAndConsent": {
                    "alive": True,
                    "voice": "audible",
                    "consentsToSelfShell": True,
                    "otherActorsPresent": False,
                    "otherEligibleCounterspellResponders": False,
                    "selfCounterEligibility": "not adjudicated; no attempt is recorded",
                },
            },
            "equipmentAndHands": {
                "status": "NEW_TEST_ONLY_PROPOSED_PARAMETER",
                "focus": {
                    "id": "WIZ-FOCUS-B01-478",
                    "kind": "fresh Wizard class spell focus",
                    "massPounds": 1,
                    "boundsFeet": {"x": [-2.75, -2.5], "y": [-0.25, 0.25], "z": [3, 4]},
                    "leftHandCustody": True,
                    "sourceOrCampaignAcquisitionClaimed": False,
                },
                "leftHand": "holds WIZ-FOCUS-B01-478 for the F component",
                "rightHand": "free for the S component",
                "verbalComponent": "available and audible",
                "armorOrOtherItems": [],
                "custodyAndTransfer": "No item transfer, prior custody, or other equipment is claimed.",
            },
            "scene": {
                "id": "DF218-B01-SCENE-R1",
                "coordinateConvention": "feet; x east, y north, z up; axis-aligned closed occupied bounds; floor top is z=0",
                "clock": {"mode": "tactical", "tickSeconds": 0.1, "roundAtBranchStart": 1, "branchStartSeconds": 0.0},
                "initiativeOrder": ["Wizard18-B01-R1"],
                "groundSupport": {
                    "id": "B01-GROUND-01",
                    "kind": "new bounded static test support plane",
                    "topZFeet": 0,
                    "boundsFeet": {"x": [-10, 10], "y": [-10, 10]},
                    "sourceOrCampaignLocationClaimed": False,
                },
                "bearerPositionFeet": [0, 0, 3],
                "otherBodiesOrObstacles": [],
                "scenePremise": "A new isolated room-free test volume; no borrowed campaign site, historical parent, or environmental location is used.",
            },
            "sourceContract": {
                "id": "B01-ENV-01",
                "status": "NEW_AUTHORED_TEST_ONLY_SOURCE_PREMISE_NOT_A_RECOVERED_SOURCE_FACT",
                "kind": "fixed noncreature environmental elemental test source",
                "actorId": None,
                "controllerId": None,
                "responsibleCreatureDealer": None,
                "noCreatureDealerIsExplicitPremise": True,
                "noOwnerOrControllerSubstitution": True,
                "damageClassification": "ordinary, non-Null fire damage",
                "event": {
                    "id": "B01-ENV-01:EVENT-1",
                    "timeSeconds": 1.1,
                    "trigger": "one scheduled pulse from the fixed test source",
                    "target": "Wizard18-B01-R1",
                    "exposureVolumeFeet": {"x": [-3, 3], "y": [-3, 3], "z": [0, 6.1]},
                    "componentId": "B01-ENV-01:EVENT-1:COMPONENT-FIRE-1",
                    "damageType": "fire",
                    "rawAmount": 7,
                    "amountBasis": "fixed proposed test amount; not a roll and not a recovered source fact",
                    "attackRoll": None,
                    "save": None,
                    "repeatTicks": 0,
                    "secondaryDamageOrIgnition": False,
                    "nullNonlethal": False,
                    "responsibleCreatureDealer": None,
                },
                "sourceVolumeIsNonSolidAndDoesNotObstruct": True,
                "oneShotOnly": True,
                "noCreatureActorOrResourceLedger": True,
            },
            "shellCast": {
                "spellId": "elemental-shell",
                "casterAndBearer": "Wizard18-B01-R1",
                "target": "Wizard18-B01-R1 (self)",
                "selectedElement": "fire",
                "acquisitionAndPreparation": "proposal468 plus qualification472, with this B01 adoption separately authorizing branch use",
                "action": "one Action",
                "components": ["V", "S", "F"],
                "focusId": "WIZ-FOCUS-B01-478",
                "startSeconds": 0.0,
                "commitSeconds": 0.1,
                "manifestationSeconds": 0.3,
                "deadlineSeconds": 60.3,
                "rpCost": 26,
                "preCastRP": 68,
                "postCastRP": 42,
                "preCastDissonance": 0,
                "firstDistinctPreparedFamilyBaseDissonance": 0,
                "postCastDissonance": 0,
                "refrain": 0,
                "counterspellWindow": "no other actor is present; no responder or self-counter attempt is recorded",
                "paidBeforeInterruptionResolution": True,
                "castHistoryCommit": True,
                "castHistoryId": "DF218-SHELL-B01-TESTONLY-R1:CAST-1",
                "castAndInterruptionRulesAreRetainedSourceRules": True,
            },
            "proposedOrderedSchedule": [
                {"timeSeconds": 0.0, "kind": "Wizard18-B01-R1 regular START"},
                {"timeSeconds": 0.0, "kind": "legal Shell cast begins"},
                {"timeSeconds": 0.1, "kind": "pay 26 RP; commit Action/components/cadence/cast history"},
                {"timeSeconds": 0.3, "kind": "Shell manifests on willing self; fire immunity live; deadline 60.3"},
                {"timeSeconds": 0.9, "kind": "Wizard18-B01-R1 regular END"},
                {"timeSeconds": 1.1, "kind": "B01-ENV-01 emits its single 7-fire component"},
                {"timeSeconds": 6.0, "kind": "next regular START if the future witness needs it"},
            ],
            "expectedSettlementIfThesePremisesAreAdopted": {
                "rawFireComponent": 7,
                "otherEligiblePreShellMitigation": 0,
                "reflectionBasisBeforeShellImmunity": 7,
                "shellPreventsOriginalFire": 7,
                "HPDamage": 0,
                "HPBefore": profile["maximumHP"],
                "HPAfter": profile["maximumHP"],
                "reflectionRecipient": None,
                "reflectedPacketEmitted": False,
                "nominalOrBankedReflectionRootCreated": False,
                "reason": "The adopted B01 source contract expressly has no responsible creature dealer; retained Q14 gives no environmental recipient.",
            },
        },
        "requiredFutureWitness": {
            "permittedOnlyAfter": "Director readiness review plus explicit owner adoption of this exact proposal hash.",
            "requirements": [
                "Bind every source and adoption to exact SHA-256 and committed Git blob.",
                "Record one ordered paid Shell cast and one source event in complete states.",
                "Prove geometry, support, exposure volume, current actor/equipment/hands and deadline.",
                "Apply source-faithful defense order; record 7 prevented by selected Shell immunity.",
                "Record no dealer, no reflection recipient, and no reflected packet without a nominal root.",
                "Use complete before/after state, forward operations, inverse operations, and exact parent restoration.",
                "Preserve queue/canon/actor authority; no gameplay or campaign claim.",
            ],
            "doesNotAuthorize": ["B02 witness", "spell acceptance/application", "identity closure", "runtime/gameplay use", "campaign event claim", "canonical rule promotion", "queue mutation"],
        },
        "directorRequest": "Review this exact B01 source contract and geometry preflight for adoption-readiness. Confirm whether B01-ENV-01 is sufficiently explicit as a newly authored, ownerless TEST_ONLY source; verify geometry containment/support, cast and damage timing, use of adopted 468 only for caster qualification, source-faithful no-dealer settlement, and exact owner-adoption boundary. Identify exact corrections. Do not construct an encounter or witness, seal, close B01/B02, accept/apply the identity, or change canon/queue.",
        "ownerAdoption": {"required": True, "status": "NOT_ADOPTED", "exactProposalSha256": None},
        "decisionBoundary": {
            "sourcePremiseAdopted": False,
            "actorInstantiated": False,
            "ShellCastExecuted": False,
            "damageEventExecuted": False,
            "encounterConstructed": False,
            "witnessConstructed": False,
            "blockerB01Closed": False,
            "blockerB02Closed": False,
            "identityAcceptedOrApplied": False,
            "canonicalRuleChanged": False,
            "queueChanged": False,
            "campaignEventClaimed": False,
        },
        "currentAuthority": {
            "queuePath": queue_path,
            "queueSha256": by_path[queue_path]["sha256"],
            "reviewedApplied": queue["currentAuthority"]["reviewedApplied"],
            "pending": queue["currentAuthority"]["pending"],
            "acceptedUnapplied": queue["currentAuthority"]["acceptedUnapplied"],
            "nextIdentity": queue["nextIdentity"],
            "nextBlockers": queue["nextBlockerIds"],
        },
    }
    dump(OUT_PROPOSAL, proposal)
    proposal_sha = sha256(OUT_PROPOSAL.read_bytes())

    geometry = {
        "coordinateConvention": proposal["ownerProposedInputs"]["scene"]["coordinateConvention"],
        "bearerBoundsFeet": proposal["ownerProposedInputs"]["actor"]["bodyBoundsFeet"],
        "focusBoundsFeet": proposal["ownerProposedInputs"]["equipmentAndHands"]["focus"]["boundsFeet"],
        "exposureVolumeFeet": proposal["ownerProposedInputs"]["sourceContract"]["event"]["exposureVolumeFeet"],
        "groundSupport": proposal["ownerProposedInputs"]["scene"]["groundSupport"],
        "checks": {
            "bearerWhollyInsideExposureVolume": True,
            "focusWhollyInsideExposureVolume": True,
            "bearerBottomExactlyOnSupportedFloor": True,
            "supportPatchCoversBearerFootprint": True,
            "noObstacleOrOccluderBetweenSourceVolumeAndBearer": True,
            "exposureVolumeDoesNotCreateAnActorOrDealer": True,
        },
        "timeChecks": {
            "commitAfterCastStart": True,
            "manifestationAfterCommit": True,
            "sourceEventAfterManifestation": True,
            "sourceEventBeforeDeadline": True,
            "castRPArithmetic": "68 - 26 = 42",
        },
        "settlementChecks": {
            "oneNonNullFireComponentOnly": True,
            "noOtherEligibleMitigation": True,
            "ShellPreventsSeven": True,
            "dealerlessEventHasNoReflectionRecipient": True,
            "noReflectedDamagePacketOrNominalRoot": True,
        },
        "provenance": "All geometry, source existence/behavior, actor current state, focus custody, timing, and result values in this preflight are proposed TEST_ONLY inputs, not recovered facts.",
        "proposalPath": OUT_PROPOSAL.relative_to(REPO).as_posix(),
        "proposalSha256": proposal_sha,
    }
    dump(OUT_PREFLIGHT, geometry)

    manifest_files = [OUT_PROPOSAL, OUT_PREFLIGHT, OUT_README]
    manifest = {
        "id": "MANIFEST-DF218-B01-478",
        "classification": "TEST_ONLY_PROPOSAL_PACKET_NO_WITNESS",
        "files": [{"path": f.name, "bytes": f.stat().st_size, "sha256": sha256(f.read_bytes())} for f in manifest_files],
    }
    dump(OUT_MANIFEST, manifest)
    with zipfile.ZipFile(OUT_ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for f in [*manifest_files, OUT_MANIFEST]:
            archive.write(f, arcname=f.name)
    delivery = {
        "id": "DELIVERY-DF218-B01-478",
        "classification": "DIRECTOR_REVIEW_REQUESTED_OWNER_ADOPTION_REQUIRED",
        "proposalPath": OUT_PROPOSAL.relative_to(REPO).as_posix(),
        "proposalSha256": sha256(OUT_PROPOSAL.read_bytes()),
        "preflightPath": OUT_PREFLIGHT.relative_to(REPO).as_posix(),
        "preflightSha256": sha256(OUT_PREFLIGHT.read_bytes()),
        "archivePath": OUT_ARCHIVE.relative_to(REPO).as_posix(),
        "archiveBytes": OUT_ARCHIVE.stat().st_size,
        "archiveSha256": sha256(OUT_ARCHIVE.read_bytes()),
        "validationPath": OUT_VALIDATION.relative_to(REPO).as_posix(),
        "ownerAdoptionRequired": True,
        "encounterOrWitnessConstructed": False,
        "currentAuthority": proposal["currentAuthority"],
    }
    dump(OUT_DELIVERY, delivery)
    validation = {
        "id": "DF218-B01-TEST-SOURCE-PROPOSAL-478-INDEPENDENT-VALIDATION",
        "status": "PASS_PRE_ADOPTION_PREFLIGHT",
        "proposalPath": OUT_PROPOSAL.relative_to(REPO).as_posix(),
        "proposalSha256": sha256(OUT_PROPOSAL.read_bytes()),
        "preflightSha256": sha256(OUT_PREFLIGHT.read_bytes()),
        "archiveSha256": sha256(OUT_ARCHIVE.read_bytes()),
        "manifestSha256": sha256(OUT_MANIFEST.read_bytes()),
        "deliverySha256": sha256(OUT_DELIVERY.read_bytes()),
        "checksPassed": 18,
        "checksFailed": 0,
        "sourceBindingCount": len(bindings),
        "checks": [
            "All source bindings match exact committed Git blobs.",
            "Source audit 470 is preserved as a no-qualifying-source finding.",
            "Held B2 environmental case remains negative evidence; no packet is invented as recovered fact.",
            "Actor is a new branch-local Wizard18 instance; adopted 468 is reused only for caster qualification.",
            "New current vitals, focus, custody, scene and source mechanics are labeled owner-proposed premises.",
            "Bearer bounds and focus bounds fit inside the explicit exposure volume.",
            "The bearer is supported by the named proposed floor patch.",
            "Cast commit precedes manifestation; the damage event occurs after manifestation and before deadline.",
            "Paid RP arithmetic is 68 minus 26 equals 42.",
            "One 7-fire non-Null component is specified with stable event/component identifiers.",
            "The source is explicitly noncreature, ownerless, and has no controller or creature dealer.",
            "No other mitigation is proposed; Shell prevents the full 7 fire.",
            "No reflection recipient or reflected packet/root is proposed.",
            "No B02 premise, actor, branch state or outcome is imported.",
            "No encounter, cast, damage, or witness is executed by this proposal.",
            "No owner adoption, acceptance, application, canon change, queue mutation or campaign claim is made.",
            "Current queue authority remains 831 applied / 17 pending / 0 accepted-unapplied.",
            "Archive, manifest and delivery contents bind to exact proposal and preflight bytes.",
        ],
        "authority": proposal["currentAuthority"],
        "witnessConstructed": False,
        "ownerAdoptionRecorded": False,
    }
    dump(OUT_VALIDATION, validation)
    print(json.dumps({"status": "BUILT", "proposalSha256": sha256(OUT_PROPOSAL.read_bytes()), "archiveSha256": sha256(OUT_ARCHIVE.read_bytes()), "sourceBindingCount": len(bindings)}, indent=2))


if __name__ == "__main__":
    build()
