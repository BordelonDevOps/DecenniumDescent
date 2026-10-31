from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_summon_herald_w02_witness_358"
OUT.mkdir(parents=True, exist_ok=True)

AUTH_PATH = AUDIT / "OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json"
W17D_PATH = AUDIT / "rank9_summon_herald_of_the_planes_return332_received/payload/evidence/EXISTING_W17D_PROFILE.json"
REPACK_PATH = AUDIT / "rank9_summon_herald_w01_content_reconciliation_358_repack01/DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01.zip"
AUTH = json.loads(AUTH_PATH.read_text(encoding="utf-8"))
W17D = json.loads(W17D_PATH.read_text(encoding="utf-8"))
WPROFILE = W17D["profile"]
W17D_SOURCE_LINEAGE = {
    "extractedEvidencePath": W17D_PATH.relative_to(ROOT).as_posix(),
    "extractedEvidencePointer": "/profile",
    "parentArchivePath": W17D["parentArchive"]["path"],
    "parentArchiveBytes": W17D["parentArchive"]["bytes"],
    "parentArchiveSHA256": W17D["parentArchive"]["sha256"],
    "parentMember": W17D["parentMember"],
    "parentMemberPointer": W17D["pointer"],
    "parentMemberBytes": W17D["parentBinding"]["bytes"],
    "parentMemberSHA256": W17D["parentBinding"]["sha256"],
    "parentMemberCRC32": W17D["parentBinding"]["crc32"],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name: str, obj: object) -> Path:
    p = OUT / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


recorded = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
archive_bytes = REPACK_PATH.stat().st_size
archive_sha = sha(REPACK_PATH)
assert archive_bytes == 18212
assert archive_sha == "7819aabadd831a08024d896886aeb3570460a85c243b40856d7e6c5c144d524e"
assert AUTH["status"] == "AUTHORIZED_FUTURE_TEST_ONLY_W02_AFTER_W01_APPROVAL"
assert AUTH["scope"]["permittedRecord"] == "hypothetical TEST_ONLY call-state record for SH332-W03 and SH332-W04"
assert WPROFILE["id"] == "W17D"
assert "summon-herald-of-the-planes" in WPROFILE["prepared"]
assert "summon-herald-of-the-planes" in WPROFILE["spellbook"]
assert WPROFILE["classLevel"] == 17 and WPROFILE["rpMaximum"] == 64

w01 = {
    "id": "SH332-W01-DIRECTOR-REAFFIRMATION-CLEAN-REPACK01-358",
    "recordedAtUtc": recorded,
    "status": "APPROVED_CLEAN_REPACK01_BOUND",
    "directorRulingId": "SH332-W01-DIRECTOR-RECONCILIATION-358-R1",
    "profileVersion": "LUMEN-HERALD-W01-358-v1",
    "spellId": "summon-herald-of-the-planes",
    "targetIdentity": "Lumen of the Shattered Thread",
    "originalApproval": {
        "decision": "W01 APPROVED",
        "archive": "DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358.zip",
        "archiveSHA256": "e6a80810e4b29ec5edc589757cb724ae169891f783de20d6242843b6e6a9cd28",
        "note": "The original approval excluded one unmanifested unreadable nested ZIP from substantive content approval. That packaging binding has been superseded by the sealed clean-repack reaffirmation below."
    },
    "sealedCleanReaffirmation": {
        "archive": "DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01.zip",
        "archiveBytes": archive_bytes,
        "archiveSHA256": archive_sha,
        "w01Approved": True,
        "remainingW01DefectPaths": [],
        "remainingPackagingDefects": [],
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["summon-herald-of-the-planes"],
        "blockerIds": ["SH202-B02"],
        "closedBlockerIds": [],
        "applicationAuthorized": False,
        "verifiedContents": "Exactly ten evidence payloads plus MEMBER_MANIFEST.json; no duplicates, extras or nested ZIP; all payload hashes and CRCs passed and all ten evidence payloads are byte-identical to the prior reviewed packet.",
        "substantiveRuling": "Every substantive field and boundary in SH332-W01-DIRECTOR-RECONCILIATION-358-R1 remains unchanged. W01 approval activates preparation of the expressly authorized TEST_ONLY W02 fixture for SH332-W03/W04 only.",
        "source": "GPT Director response in the active Director review chat, sealed rebind/reaffirmation following attachment of the clean Repack01."
    },
    "approvalLimits": {
        "identityAccepted": False,
        "identityApplied": False,
        "SH202B02Closed": False,
        "canonicalPublicationAuthorized": False,
        "campaignFactsEstablished": False,
        "permittedNextWork": ["SH332-W02", "SH332-W03", "SH332-W04"],
        "profileSummary": {
            "size": "Large", "type": "Elemental", "alignment": "Chaotic Neutral",
            "challengeRating": 22, "armorClass": 19, "printedHP": 528,
            "governingAbilities": {"STR": 19, "DEX": 16, "CON": 22, "INT": 9, "WIS": 12, "CHA": 11},
            "speedFeet": {"ground": 40, "fly": 80}, "saveDC": 21,
            "ThreadLanceRangeFeet": 120, "ThreadBindRangeFeet": 60,
            "ThreadShatterRadiusFeet": 20, "occupiedGeometryFeet": [10, 10, 10],
            "call": {"action": "Action", "rp": 26, "components": "V/S/F", "rangeFeet": 120, "concentrationSeconds": 60},
            "geography": "same bounded home arena and same plane only; no Seal, Gate, arena or phase mutation"
        }
    }
}
dump("01_SH332_W01_CLEAN_REAFFIRMATION_358.json", w01)

# All coordinates, actor states, consent, custody, and history below are explicitly hypothetical.
# One Lumen identity is used in each serialized witness execution; reset between tests is harness rollback only.
arena = {
    "id": "TEST_ONLY_ARENA_358_A",
    "classification": "hypothetical fixture premise; not campaign geography",
    "planeId": "TEST_ONLY_PLANE_358_A",
    "boundsFeet": {"x": [0, 100], "y": [0, 100], "z": [0, 20]},
    "floor": {"zFeet": 0, "type": "continuous solid load-bearing test surface", "fixtureOnly": True},
    "interior": "Open and unobstructed in every source/destination and attack line specified in the witness cases.",
    "arenaState": "quiescent cooperative interval; no active arena encounter, Gate examination, Seal Pulse, unresolved objective, or scheduled phase transition during each timed call.",
    "seal": {"id": "TEST_ONLY_GATE_BOUND_SEAL_358_A", "state": "active", "boundary": "TEST_ONLY_ARENA_358_A", "mutated": False},
    "travelWards": [],
    "otherAdmissionPredicates": "No ward, permission, collision, support, cargo-fit or line-of-effect blocker except the explicitly scheduled W04 return-body overlap and suppression branch. This statement is a TEST_ONLY premise."
}

origin = {"lowerSouthwestCornerFeet": [20, 20, 0], "dimensionsFeet": [10, 10, 10], "centerFeet": [25, 25, 5]}
destination = {"lowerSouthwestCornerFeet": [50, 20, 0], "dimensionsFeet": [10, 10, 10], "centerFeet": [55, 25, 5]}
caster_body = {"lowerSouthwestCornerFeet": [40, 10, 0], "dimensionsFeet": [5, 5, 5], "centerFeet": [42.5, 12.5, 2.5]}
distance_origin_destination = 30.0
distance_caster_destination = round(((55-42.5)**2 + (25-12.5)**2 + (5-2.5)**2) ** 0.5, 3)

w02 = {
    "id": "SUMMON-HERALD-W02-AUTHORIZED-TEST-STATE-358",
    "recordedAtUtc": recorded,
    "status": "COMPLETE_AUTHORIZED_TEST_ONLY_FIXTURE_NOT_CAMPAIGN_EVIDENCE",
    "purpose": "Supply the W02 TEST_ONLY individual state required only for the serialized SH332-W03/W04 conditional witnesses.",
    "spellId": "summon-herald-of-the-planes",
    "blockerId": "SH202-B02",
    "targetIdentity": "Lumen of the Shattered Thread",
    "uniqueIdentityKey": "LUMEN-OF-THE-SHATTERED-THREAD-UNIQUE-TEST-IDENTITY-358",
    "sourceProfileBinding": {
        "profileVersion": "LUMEN-HERALD-W01-358-v1",
        "rulingId": "SH332-W01-DIRECTOR-RECONCILIATION-358-R1",
        "cleanArchive": REPACK_PATH.name,
        "cleanArchiveSHA256": archive_sha,
        "w01Approval": True
    },
    "stateClassification": "expressly-authorized TEST_ONLY hypothetical state; not actual presence, availability, consent, campaign occurrence, history, or source fact",
    "authorityAttestation": {
        "providerRole": "Codex acting as the named provider of the expressly hypothetical fixture",
        "authorizingRecordOrApprovalPath": "OWNER-LUMEN-W02-TEST-AUTHORIZATION-358 plus sealed W01 approval and clean-repack reaffirmation",
        "authorizationSHA256": sha(AUTH_PATH),
        "approvalTimestampUtc": recorded,
        "scopeOfAuthority": "Only W02 and SH332-W03/W04 for this identity and approved W01 profile; no runtime, canonical publication, campaign claim, or other spell scope."
    },
    "stateTimestampUtc": recorded,
    "logicalClock": {
        "classification": "TEST_ONLY deterministic witness time; all scenario timestamps are virtual test labels, not observed campaign times",
        "firstScenarioVirtualUtc": "2026-10-31T16:00:00.000Z",
        "timelineUnit": "milliseconds",
        "testSequenceId": "TEST_ONLY_SH332_WITNESS_SEQUENCE_358",
        "notAnArenaEncounter": True,
        "mechanicalEncounter": {"active": True, "id": "TEST_ONLY_SH332_WITNESS_SEQUENCE_358", "purpose": "ordered TEST_ONLY spell/initiative history only", "arenaCombatPhaseActive": False, "campaignEncounterClaim": False},
        "encounterAndRechargeHistoryBinding": {
            "encounterId": "TEST_ONLY_SH332_WITNESS_SEQUENCE_358",
            "classification": "synthetic ability-history scope identifier; not an active arena encounter",
            "arenaEncounterActive": False,
            "threadShatterFirstUseInThisScope": False,
            "threadShatterWarningTimestamp": None,
            "threadShatterCurrentRechargeState": "unexpended/ready; no recharge roll due"
        },
        "regularTurnCalendars": {
            "W03": [
                {"offsetMs": 0, "actor": "TEST_ONLY_W17D_CASTER_A", "slot": "its own regular Action slot"},
                {"offsetMs": 6000, "actor": "Lumen", "slot": "existing next regular initiative slot; one slot only"},
                {"offsetMs": 60000, "actor": "call clock", "slot": "original deadline; no turn is granted"}
            ],
            "W04": [
                {"offsetMs": 0, "actor": "TEST_ONLY_W17D_CASTER_A", "slot": "its own regular Action slot"},
                {"offsetMs": 10, "actor": "TEST_ONLY_W17D_CASTER_B", "slot": "its own regular Action slot"},
                {"offsetMs": 6000, "actor": "Lumen", "slot": "existing next regular initiative slot; one slot only"},
                {"offsetMs": 12000, "actor": "TEST_ONLY_RETURN_BLOCKER_A", "slot": "its own regular movement slot"},
                {"offsetMs": 60000, "actor": "call clock", "slot": "original deadline; no turn is granted"},
                {"offsetMs": 66000, "actor": "TEST_ONLY_RETURN_BLOCKER_A", "slot": "its own next regular movement slot"},
                {"offsetMs": 72000, "actor": "Lumen", "slot": "its own next regular slot; independent movement only"}
            ]
        }
    },
    "state": {
        "sourceLocation": {
            "classification": "TEST_ONLY premise",
            "arenaId": arena["id"], "planeId": arena["planeId"],
            "bodyPlacement": origin,
            "returnAnchor": origin["lowerSouthwestCornerFeet"],
            "samePlaneAndSameHomeArena": True
        },
        "presentOrExpresslyAuthorizedTestState": "Expressly authorized hypothetical TEST_ONLY state for SH332-W03/W04; no presence or occurrence claim.",
        "available": {"value": True, "classification": "TEST_ONLY premise", "reason": "one unique body at source, no active call, no outstanding return, and no reservation at this serialized baseline"},
        "competingReservationOrConcurrentCall": {"baseline": None, "classification": "TEST_ONLY premise", "uniquenessRule": "one identity key and one body; W04 stores two pending declarations outside the active-call registry, then permits only the first resolution to reserve. A second resolution fails its final check and cannot create another body or reservation."},
        "affirmativeConsentToExactCall": {
            "value": True, "classification": "TEST_ONLY explicit premise, not real consent",
            "consentingIdentity": "Lumen of the Shattered Thread (hypothetical test persona)",
            "scope": "For W03, the one described paid temporary call. For W04, the exact TEST_ONLY concurrent-declaration race by TEST_ONLY_W17D_CASTER_A and TEST_ONLY_W17D_CASTER_B: both may pass initial eligibility while the unique identity has no active call or reservation, only the first successful resolution may reserve and move Lumen, and Lumen consents to the successful call, its same-arena/same-plane arrival, one permitted Thread Bind on its existing regular initiative, the finite cargo, the fixed 60-second deadline, blocked return and independent movement recovery. Consent to B covers the specified declaration attempt and final admission check only; it does not authorize a second movement, body, call, aid, or control.",
            "exclusions": ["no compelled obedience", "no extra action or turn", "no hidden knowledge or disclosure", "no cross-arena or cross-plane travel", "no Seal or Gate alteration", "no permanent displacement", "no transfer of another actor's action economy"]
        },
        "permittedAidOrCommandScope": {
            "classification": "TEST_ONLY consent premise bounded by the approved profile",
            "W03": "One Thread Lance against TEST_ONLY_CREATURE_A on Lumen's next original regular initiative slot.",
            "W04": "One Thread Bind against TEST_ONLY_CREATURE_A on Lumen's next original regular initiative slot.",
            "commands": "The caster requests aid; Lumen voluntarily elects the listed attack. No other command or obedience is implied."
        },
        "currentHP": {"value": 400, "maximumPrintedHP": 528, "classification": "TEST_ONLY current-state premise; not inferred from printed HP"},
        "conditions": {"value": [], "classification": "TEST_ONLY premise"},
        "usesAndRecharge": {
            "classification": "TEST_ONLY premise bound to TEST_ONLY_SH332_WITNESS_SEQUENCE_358",
            "threadShatter": {"expended": False, "firstUseInSequence": False, "visibleWarningBegun": False, "warningTimestamp": None, "rechargeState": "unexpended; no recharge roll due"},
            "otherLimitedUses": [], "rechargeResetsOnCallOrReturn": False,
            "note": "W03/W04 do not use Thread Shatter. This explicit ready-state premise is recorded rather than inferred."
        },
        "equipmentAndCustody": {
            "classification": "TEST_ONLY genuine-cargo fixture; not historical gear",
            "wornEquipment": [],
            "cargoManifest": [{"id": "TEST_ONLY_COPPER_TOKEN_358", "description": "nonmagical 1×1×1 inch copper token", "massPounds": 0.1, "custodian": "Lumen", "carriedAtBaseline": True, "containedWithinBodyBox": True, "ownershipTransfer": False}],
            "additionalObjects": [],
            "custodyRule": "Token remains in Lumen's custody if carried; any actual drop/transfer would require its own lawful ledger event. No drop/transfer occurs in the primary witnesses."
        },
        "sealState": {
            "classification": "TEST_ONLY premise", "sealId": arena["seal"]["id"], "active": True,
            "homeArenaId": arena["id"], "planeId": arena["planeId"],
            "gateBoundRemainsInForce": True, "sealGateArenaMutated": False,
            "gateExaminationActive": False, "sealPulsePending": False, "unresolvedObjective": False
        },
        "permittedKnowledgeAndDisclosure": {
            "classification": "TEST_ONLY premise under W01 limits",
            "known": ["the exact call and aid request", "visible geometry and TEST_ONLY witness target", "Lumen's own profile facts"],
            "mayDisclose": ["its own witnessed TEST_ONLY state and the approved profile facts"],
            "mayNotDisclose": ["sealed Director material", "hidden campaign facts", "facts not actually perceived or authorized"],
            "noKnowledgeOrConsentInferredFrom": ["telepathy", "truesight", "language capability", "historical arena role"]
        }
    },
    "fixtureGeometry": {
        "arena": arena,
        "lumenSourceBox": origin,
        "lumenDestinationBox": destination,
        "caster": {"id": "TEST_ONLY_W17D_CASTER_A", "body": caster_body, "locationClassification": "hypothetical", "arcaneFocusHeld": True, "componentsAvailable": {"V": True, "S": True, "F": True}, "conditions": [], "currentRP": 64, "currentDissonance": 0, "actionAvailableAtOwnSlot": True, "reactionAvailable": True, "counterspellKnownAutomaticallyAtWizard2": True, "counterspellRechargeState": "ready; 0 rounds remaining", "concentrationAvailable": True, "perception": {"canSeeCasterB": True, "clearLineOfSight": True, "distanceToCasterBFeet": 5, "spellPerceptionUnobstructed": True}, "spellAndFamilyHistory": {"spellCastHistory": [], "preparedMatrixFamilyHistory": [], "rank9FamilyHistory": [], "counterspellUses": 0}},
        "distancesFeet": {"LumenSourceCenterToDestinationCenter": distance_origin_destination, "casterCenterToDestinationCenter": distance_caster_destination},
        "supportAndFit": "The 10-foot cube has a clear, fully load-bearing z=0 base at both anchors; 20 feet of overhead clearance; no overlap with solid terrain. The token is contained inside the box.",
        "lineOfEffect": "Clear between body centers and caster/destination; no wall or ward intersects relevant lines.",
        "otherTestActors": [
            {"id": "TEST_ONLY_W17D_CASTER_B", "kind": "hypothetical second Wizard caster", "type": "Humanoid", "bodyBoxFeet": {"lowerSouthwestCorner": [40,15,0], "dimensions": [5,5,5]}, "positionRelativeToPrimaryCaster": "boundary-touch only; no overlap", "preparedHerald": True, "currentRP": 64, "currentDissonance": 0, "conditions": [], "concentrationAvailable": True, "actionAvailableAtOwnSlot": True, "reactionAvailable": True, "counterspellKnownAutomaticallyAtWizard2": True, "counterspellRechargeState": "ready; 0 rounds remaining", "arcaneFocusHeld": True, "componentsAvailable": {"V": True, "S": True, "F": True}, "perception": {"canSeeCasterA": True, "clearLineOfSight": True, "distanceToCasterAFeet": 5, "spellPerceptionUnobstructed": True}, "history": {"spellCastHistory": [], "preparedMatrixFamilyHistory": [], "rank9FamilyHistory": [], "concentrationHistory": [], "counterspellUses": 0}, "ownRegularActionSlotOffsetMs": 10},
            {"id": "TEST_ONLY_CREATURE_A", "kind": "hypothetical creature target", "type": "Construct", "AC": 15, "HP": 80, "conditions": [], "resistances": [], "bodyBoxFeet": {"lowerSouthwestCorner": [70,20,0], "dimensions": [5,5,5]}, "turnsTowardLumen": False},
            {"id": "TEST_ONLY_RETURN_BLOCKER_A", "kind": "hypothetical cooperating fixture actor", "type": "Humanoid", "AC": 10, "HP": 30, "groundSpeedFeet": 30, "bodyBoxFeetAtBaseline": {"lowerSouthwestCorner": [10,20,0], "dimensions": [5,5,5]}, "consentsToFixtureMovement": True, "movesOnlyOnItsOwnRegularSlot": True}
        ]
    },
    "casterRoute": {
        "classification": "conditional TEST_ONLY use of already-bound legal W17D acquisition/preparation route; no campaign actor or casting event is asserted",
        "sourcePath": W17D_PATH.relative_to(ROOT).as_posix(),
        "sourceFileSHA256": sha(W17D_PATH),
        "sourceProfilePointer": "/profile",
        "parentProfilePointer": W17D["pointer"],
        "parentSourceLineage": W17D_SOURCE_LINEAGE,
        "sourceProfileSHA256BeforeOwnHash": WPROFILE["profileSHA256BeforeOwnHash"],
        "profileId": WPROFILE["id"], "class": WPROFILE["class"], "classLevel": WPROFILE["classLevel"],
        "spellInSpellbook": True, "spellPrepared": True,
        "rank9Access": "Wizard level 17 and exact spell selection under the bound W17D profile; no access inferred from RP alone.",
        "testPremises": {"currentRP": 64, "currentDissonance": 0, "castHistoryForTestSequence": [], "preparedMatrixFamilyHistory": [], "rank9FamilyHistory": [], "concentrationAvailable": True, "actionAvailableOnScheduledOwnTurn": True, "reactionAvailable": True, "counterspellKnownAutomaticallyAtWizard2": True, "counterspellRechargeState": "ready; 0 rounds remaining", "componentsAvailable": {"V": True, "S": True, "F": True}, "focusHeld": True, "conditions": [], "clearPerceptionOfCasterBAt5Feet": True},
        "perSpellEnvelope": {"action": "Action", "rank": 9, "RP": 26, "components": "V/S/F", "concentration": True, "maximumDurationMilliseconds": 60000},
        "firstCastDissonance": "Rank 9 contributes 2 base Dissonance; W17D's protected first-distinct-matrix exemption suppresses only base strain, so each independently instantiated first cast receives 0 base Dissonance. No overcast or other strain-costing feature is used.",
        "casterUseForW04": "A second distinct hypothetical test caster is explicitly instantiated from the same exact Wizard 17 acquisition/preparation profile solely to make simultaneous concentration/call exclusion testable. This is a test persona, not a duplicate campaign actor or a claim that W17D has a second body."
    },
    "scenarioUse": {
        "permittedWitnesses": ["SH332-W03", "SH332-W04"],
        "executionsAreSerialized": True,
        "harnessReset": "Reset between isolated executions is analytic TEST_ONLY rollback of a synthetic scenario, not an in-world time reversal, healing, resurrection, duplicate body, or campaign event.",
        "sameUniqueLumenOnly": True
    },
    "campaignFactsEstablished": False,
    "actualConsentAsserted": False,
    "actualLocationAsserted": False,
    "actualAvailabilityAsserted": False,
    "sourceHistoricalRecordModified": False
}
dump("02_SH332_W02_AUTHORIZED_TEST_STATE_358.json", w02)

route = {
    "id": "SH332-W17D-CASTING-ROUTE-358",
    "classification": "conditional TEST_ONLY route binding",
    "sourcePath": W17D_PATH.relative_to(ROOT).as_posix(),
    "sourceFileBytes": W17D_PATH.stat().st_size,
    "sourceFileSHA256": sha(W17D_PATH),
    "memberBinding": {**W17D["parentBinding"], "parentArchivePath": W17D["parentArchive"]["path"], "parentArchiveSHA256": W17D["parentArchive"]["sha256"], "memberName": W17D["parentMember"], "pointerWithinParentMember": W17D["pointer"]},
    "profilePointer": "/profile",
    "parentProfilePointer": W17D["pointer"],
    "parentSourceLineage": W17D_SOURCE_LINEAGE,
    "profileId": WPROFILE["id"],
    "profileSHA256BeforeOwnHash": WPROFILE["profileSHA256BeforeOwnHash"],
    "class": WPROFILE["class"], "classLevel": WPROFILE["classLevel"],
    "classStats": {"INT": WPROFILE["abilityScores"]["INT"], "PB": WPROFILE["PB"], "spellDC": WPROFILE["spellDC"], "spellAttack": WPROFILE["spellAttack"], "RPMax": WPROFILE["rpMaximum"], "dissonanceLimit": WPROFILE["dissonanceLimit"]},
    "spellInSpellbook": "summon-herald-of-the-planes" in WPROFILE["spellbook"],
    "spellPrepared": "summon-herald-of-the-planes" in WPROFILE["prepared"],
    "level17SelectedSpell": "summon-herald-of-the-planes" in WPROFILE["ordinaryLearning"][16]["selected"],
    "acquisitionEvidence": WPROFILE["ordinaryLearning"][16],
    "RPAndStrain": {"perCastRP": 26, "startingRP": 64, "rank9BaseDissonance": 2, "firstDistinctMatrixBaseDissonanceExemption": True, "perCastState": "For each independent TEST_ONLY caster's first prepared-matrix cast in the synthetic witness encounter, base strain is suppressed under W17D's protected interface; current Dissonance remains 0. No overcast or other strain-costing feature is used.", "overcast": False},
    "testCasterInstances": [
        {"id":"TEST_ONLY_W17D_CASTER_A","profileIdentity":"W17D route instance A","sourceBoundRoute":"This bound profile's acquired/spellbook/prepared Herald route","classification":"TEST_ONLY persona, not a campaign actor","body":caster_body,"currentRP":64,"currentDissonance":0,"conditions":[],"castHistory":[],"preparedMatrixFamilyHistory":[],"rank9FamilyHistory":[],"freeConcentration":True,"actionState":"ready at own regular slot","reactionState":"available","counterspell":{"knownAutomaticallyAtWizard2":True,"eligibleTrigger":"another creature it perceives beginning a spell within 60 feet","recharge":"ready; zero rounds remaining","usesInFixture":0},"perception":{"canSeeCasterB":True,"clearLineOfSight":True,"distanceToCasterBFeet":5,"spellPerceptionUnobstructed":True},"focusHeld":True,"componentsAvailable":{"V":True,"S":True,"F":True}},
        {"id":"TEST_ONLY_W17D_CASTER_B","profileIdentity":"independent synthetic instance of the same legal Wizard17 route","sourceBoundRoute":"TEST_ONLY instantiation of the exact W17D level-17 Herald selection/preparation route; expressly not actual W17D","classification":"TEST_ONLY persona, not a campaign actor","body":{"lowerSouthwestCornerFeet":[40,15,0],"dimensionsFeet":[5,5,5],"centerFeet":[42.5,17.5,2.5]},"currentRP":64,"currentDissonance":0,"conditions":[],"castHistory":[],"preparedMatrixFamilyHistory":[],"rank9FamilyHistory":[],"freeConcentration":True,"actionState":"ready at its own phase +10ms slot","reactionState":"available","counterspell":{"knownAutomaticallyAtWizard2":True,"eligibleTrigger":"another creature it perceives beginning a spell within 60 feet","recharge":"ready; zero rounds remaining","usesInFixture":0},"perception":{"canSeeCasterA":True,"clearLineOfSight":True,"distanceToCasterAFeet":5,"spellPerceptionUnobstructed":True},"focusHeld":True,"componentsAvailable":{"V":True,"S":True,"F":True}}
    ],
    "disclaimer": "EXISTING_W17D_PROFILE.json itself labels campaign existence unverified and its scope as conditional caster acquisition context, not an actual actor or call. These witnesses instantiate test personas only."
}
dump("03_SH332_W17D_CASTING_ROUTE_358.json", route)

def ev(eid: str, at_ms: int, subject: str, forward: str, inverse: str) -> dict:
    return {"eventId": eid, "virtualOffsetMilliseconds": at_ms, "subject": subject, "forwardOperation": forward, "inverseOperation": inverse}

def wrap_scenario(sid: str, events: list[dict], coverage: list[str], terminal: str, paid_calls: list[dict], aid: dict | None = None) -> dict:
    inv = [{"undoOf": e["eventId"], "operation": e["inverseOperation"]} for e in reversed(events)]
    return {
        "scenarioId": sid, "classification": "TEST_ONLY conditional witness; no campaign occurrence",
        "sameLumenIdentityKey": w02["uniqueIdentityKey"], "oneLumenBodyAtEveryForwardStep": True,
        "startingStateSHA256": hashlib.sha256(json.dumps(w02["state"],sort_keys=True,separators=(",",":" )).encode()).hexdigest(),
        "paidCallDeclarations": paid_calls, "usefulAid": aid,
        "counterHistory": {"eligibleCounterAttempts": [], "record": "TEST_ONLY bounded window contains no counterer declaration; no counter cost or outcome is inferred."},
        "forwardEvents": events, "inverseTraversal": inv,
        "inverseEventOrderIsExactReverse": [x["undoOf"] for x in inv] == [e["eventId"] for e in reversed(events)],
        "coverage": coverage, "terminalState": terminal,
        "harnessRollbackAfterCapture": "Apply the listed analytic inverse traversal and verify the full hypothetical W02 baseline hash. This is not an in-world event."
    }

# W03 successful useful aid, genuine cargo, exact original deadline, ordinary return.
w03_normal_events = [
    ev("W03N-01-DECLARE-AND-PAY",0,"TEST_ONLY_W17D_CASTER_A","Use its own scheduled Action; declare the prepared rank-9 spell with V/S/F, pay exactly 26 RP (64→38), begin concentration, and set immutable deadline T0+60000ms.","Restore caster Action, RP 64, free concentration, and empty cast-history for the isolated baseline."),
    ev("W03N-02-COUNTER-WINDOW",0,"TEST_ONLY_WITNESS_WINDOW","No counterer begins a counter; the cast proceeds without counter cost or resolution branch.","Restore the explicitly empty counter-attempt history."),
    ev("W03N-03-ATOMIC-ADMISSION",500,"Lumen","Recheck W01/W02 predicates; atomically reserve the one identity and relocate same 10-cube body plus TEST_ONLY_COPPER_TOKEN_358 from origin to destination; no duplicate or intermediate projection.","Move the same body and token from destination back to exact origin, then clear the scenario reservation/call."),
    ev("W03N-04-USEFUL-OWN-TURN-AID",6000,"Lumen","On its next original regular slot, choose the consented Thread Lance. Roll d20=12 +11=23 vs target AC15; roll 4d10=[3,4,5,6], +10 = 28 radiant; TEST_ONLY_CREATURE_A HP 80→52. No other attack or rider.","Restore target HP 80 and clear only this synthetic attack record; leave Lumen at its pre-attack test HP/conditions."),
    ev("W03N-05-ORIGINAL-DEADLINE",60000,"Herald call","At declaration+60000ms, end concentration/call; one automatic return attempt checks same-arena/plane, anchor fit/support, LoE, wards, cargo and permission. All pass; relocate same body and still-carried token to exact recorded origin. Release reservation; no Action/RP payment, retry, phase or recharge reset.","Restore the active-call snapshot at T0+59999ms for reverse traversal, then undo the admission and declaration events in their listed reverse order.")
]
w03_normal_paid = [{"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":0,"action":"Action","rank":9,"RPcost":26,"RPbefore":64,"RPafter":38,"components":{"V":True,"S":True,"F":True,"focusHeld":True},"concentrationStarted":True,"deadlineOffsetMs":60000,"counterHistory":"none attempted"}]
w03_normal = wrap_scenario("SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358",w03_normal_events,["paid declaration and source route","arrival and 10-cube supported fit","useful aid on Lumen's original regular initiative","finite cargo is returned in custody","original 60000ms deadline","normal return to exact anchor","resources and state preserved","complete forward and inverse traversal"],"One Lumen body at exact source anchor; HP400; no conditions; token in Lumen custody; call ended; no reservation; Gate-Bound Seal unchanged.",w03_normal_paid,{"ability":"Thread Lance","target":"TEST_ONLY_CREATURE_A","damage":"28 radiant","usefulResult":"target test-state HP reduced 80→52"})

# W03 suppression branch: original clock continues; no revival after transport restoration.
w03_suppress_events = [
    ev("W03S-01-DECLARE-AND-PAY",0,"TEST_ONLY_W17D_CASTER_A","Pay 26 RP (64→38) for one legal Action/V/S/F cast and start a 60000ms concentration clock.","Restore caster baseline, including RP64 and no concentration."),
    ev("W03S-02-ARRIVAL",500,"Lumen","Recheck all admission predicates; reserve the unique identity and arrive at the supported destination with the same token.","Return the same body/token to the recorded source and clear the active reservation in analytic rollback."),
    ev("W03S-03-USEFUL-AID",6000,"Lumen","On its original regular slot, resolve consented Thread Lance against TEST_ONLY_CREATURE_A; d20=11 +11=22 vs AC15; 4d10=[2,5,4,6]+10=27 radiant; target HP80→53.","Restore TEST_ONLY_CREATURE_A HP to80 and remove this synthetic attack result."),
    ev("W03S-04-TEST-ONLY-SUPPRESSION",59900,"Call transport state","The isolated harness sets returnTransportSuppressed=true as an explicit TEST_ONLY branch input. It does not suppress or move Lumen, alter the arena, restart the clock, or claim a world ward.","Remove the synthetic suppression input after the captured branch; do not change the already-ended call."),
    ev("W03S-05-EXPIRY-WHILE-SUPPRESSED",60000,"Herald call","The original deadline expires. Automatic return is attempted once and blocked solely because call transport is currently suppressed. End call/concentration, release active reservation, keep same body and token at actual destination, preserve HP/conditions/custody, set returnOutstanding=true; no retry or extension.","Restore the exact pre-expiry active-call state only in the analytic replay, then reverse arrival and paid declaration."),
    ev("W03S-06-RESTORATION-NO-REVIVAL",61000,"Call transport state","Restore the hypothetical transport channel. The expired call stays expired and makes no automatic retry; returnOutstanding remains true.","Reapply the synthetic suppressed flag to recover the prior captured branch state."),
    ev("W03S-07-INDEPENDENT-LEGAL-RECOVERY",66000,"Lumen","On Lumen's own next regular slot after suppression clears, use 30ft of ordinary ground movement (≤40ft) over clear supported floor to the exact origin. No call transport, Action, RP, extra turn or refreshed resource. Clear returnOutstanding only upon arrival.","For analytic inverse, restore Lumen to the test endpoint and reinstate returnOutstanding=true; this is not an in-world rewind.")
]
w03_suppress = wrap_scenario("SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358",w03_suppress_events,["paid W17D-route cast","supported arrival and finite cargo","useful aid on original initiative","suppression at deadline","original clock not extended","one blocked return with explicit predicate","restoration does not revive expired call","independent legal movement resolves outstanding return","complete forward and inverse traversal"],"After independent recovery: same body at origin; call remains expired; reservation released; returnOutstanding=false; token remains in Lumen custody.",[{"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":0,"action":"Action","rank":9,"RPcost":26,"RPbefore":64,"RPafter":38,"components":"V/S/F; focus held","concentrationStarted":True,"deadlineOffsetMs":60000}],{"ability":"Thread Lance","target":"TEST_ONLY_CREATURE_A","damage":"27 radiant","usefulResult":"target test-state HP reduced 80→53"})

# W03 death branch: death is a declared test input and follows the core monster-at-zero default; no resurrection.
w03_death_events = [
    ev("W03D-01-DECLARE-AND-PAY",0,"TEST_ONLY_W17D_CASTER_A","Pay 26 RP (64→38), declare one prepared rank-9 Action/V/S/F cast, and begin the fixed 60000ms deadline.","Restore caster baseline and clear test-only cast history."),
    ev("W03D-02-ARRIVAL",500,"Lumen","Recheck admission, atomically reserve and relocate the single body plus finite token to supported destination.","Move the same body/token to exact origin and clear the reservation in analytic rollback."),
    ev("W03D-03-USEFUL-AID",6000,"Lumen","On its original regular slot, resolve consented Thread Lance; d20=14+11=25 vs AC15; 4d10=[2,3,5,6]+10=26 radiant; target HP80→54.","Restore target HP80 and erase the synthetic attack record."),
    ev("W03D-04-TEST-LETHAL-INPUT",12000,"Lumen","Explicit TEST_ONLY input applies 400 force damage to current HP400; W01 profile has no force resistance/immunity. The test premise classifies this unique persona under the Player Rulebook v6 default 'Most monsters die at 0 HP' (source text line 8279), not as a significant NPC with discretionary death saves. At 12000ms HP becomes 0 and death is confirmed; this ends concentration and the call at exactly 12000ms. The single legal automatic return attempt then relocates the same physical corpse and carried token to exact origin; no deletion, duplicate, healing, resurrection or loot creation.","Restore only the complete pre-input active-call/destination state in analytic harness traversal, then undo the death/call-end transition and earlier events in exact reverse order; no in-world rewind is claimed."),
    ev("W03D-05-CORPSE-RETURN-LOG",12001,"Herald call","Record-only confirmation at 12001ms: the call and concentration already ended at 12000ms, and the same corpse/token were already returned by that trigger. This one-millisecond-later record is not a delayed call end or a second transport attempt.","Remove only this post-trigger log timestamp; the mechanical death and return remain owned by the 12000ms transition until its own inverse is applied.")
]
w03_death = wrap_scenario("SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358",w03_death_events,["paid W17D-route call","useful aid on original initiative","source-bounded 0-HP death test premise","ending trigger at confirmed death","same corpse and carried cargo returned if predicates pass","no vanish or resurrection","complete forward and inverse traversal"],"Same Lumen corpse and token at exact origin; HP0, confirmed dead; call ended and reservation released; no resurrection or campaign claim.",[{"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":0,"action":"Action","rank":9,"RPcost":26,"RPbefore":64,"RPafter":38,"components":"V/S/F; focus held","concentrationStarted":True,"deadlineOffsetMs":60000}],{"ability":"Thread Lance","target":"TEST_ONLY_CREATURE_A","damage":"26 radiant","usefulResult":"target test-state HP reduced 80→54"})

w03 = {
    "id":"SH332-W03-BOUNDED-CALL-LIFECYCLE-358",
    "profileVersion":"LUMEN-HERALD-W01-358-v1",
    "w02Binding":"SUMMON-HERALD-W02-AUTHORIZED-TEST-STATE-358",
    "classification":"conditional TEST_ONLY witness bundle; no campaign event asserted",
    "witnesses":[w03_normal,w03_suppress,w03_death],
    "coverageSummary":{"arrival":True,"original60SecondExpiry":True,"ordinaryReturn":True,"blockedReturn":True,"cargoPreserved":True,"suppression":True,"deathAndCorpse":True,"usefulAidOnOriginalInitiative":True,"paidCalls":True,"noNewLumenIdentity":True,"allCallsBoundedToSameArenaAndPlane":True},
    "excludedClaims":["actual campaign occurrence","actual consent","actual current state","actual Gate or Seal event","general summon rules","cross-plane or permanent transport","canonical bestiary publication"]
}
dump("04_SH332_W03_LIFECYCLE_WITNESSES_358.json",w03)

# W04: two distinct synthetic casters; the first reserves the only Lumen. Second cast is paid, then fails admission.
w04_events = [
    ev("W04-01-CASTER-A-DECLARE-PAY",0,"TEST_ONLY_W17D_CASTER_A","On its own regular Action, declare the prepared rank-9 Herald cast, pay 26 RP (64→38), supply V/S/F, and begin concentration. Its initial eligibility check passes because no active call or reservation yet exists. Resolution is queued; no identity reservation is taken at declaration.","Restore caster A RP64, free concentration and Action in the isolated baseline."),
    ev("W04-02-CASTER-B-DECLARE-PAY",10,"TEST_ONLY_W17D_CASTER_B","Before either resolution, the distinct TEST_ONLY Wizard17 using the exact W17D preparation route declares on its own regular Action, pays 26 RP (64→38), supplies V/S/F and begins its own concentration. Its initial eligibility check also passes while no active call/reservation exists. Track both pending declarations separately; neither has reserved Lumen.","Restore caster B RP64, free concentration and Action in the isolated baseline."),
    ev("W04-03-PRIMARY-ADMISSION-ARRIVAL",500,"Lumen","Resolve caster A first. Recheck W01/W02 predicates and atomically reserve the unique identity before moving the same body/token from exact source to supported destination.","Move the same body/token back to source and clear the reservation in analytic rollback."),
    ev("W04-04-CASTER-B-RESOLUTION-FAILS",600,"TEST_ONLY_W17D_CASTER_B","Resolve B's already-paid candidate after A's reservation. Final admission recheck now fails solely because the same unique Lumen is reserved. B's 26 RP and Action remain spent; no refund, second body, second reservation, persistent concentration or retry.","Restore B's paid pending cast state, then reverse its declaration and payment."),
    ev("W04-05-USEFUL-AID-ORIGINAL-TURN",6000,"Lumen","On its existing regular slot, elect consented Thread Bind. Roll d20=10+11=21 vs AC15; damage 3d10=[4,6,5]+8=23 force; target HP80→57. No restraint rider.","Restore target HP80 and clear the synthetic attack result."),
    ev("W04-06-RETURN-BLOCKER-ENTERS",12000,"TEST_ONLY_RETURN_BLOCKER_A","On its own regular slot move 10ft from [10,20,0] to [20,20,0] at 30ft ground speed. Its 5-cube overlaps the recorded 10-cube return anchor; movement is voluntary TEST_ONLY fixture movement.","Move the same test blocker back to [10,20,0] on its own regular slot in analytic inverse."),
    ev("W04-07-DEADLINE-BLOCKED-RETURN",60000,"Herald call","At original declaration+60000ms, end call/concentration. One automatic return attempt fails solely on occupied-volume overlap with TEST_ONLY_RETURN_BLOCKER_A at exact source anchor. Record returnOutstanding=true, release active reservation after outcome, retain Lumen body/cargo/HP/conditions/custody at actual destination; no retry, extension, forced placement or second body.","Restore the active call at T0+59999ms in the analytic replay, then reverse blocker movement, aid, competing failed cast, arrival and primary payment."),
    ev("W04-08-BLOCKER-CLEARS",66000,"TEST_ONLY_RETURN_BLOCKER_A","On its own regular slot, 54 seconds after entering (nine six-second rounds later), move 10ft back to [10,20,0]. It no longer overlaps Lumen's exact origin box; no forced or magical movement.","Restore blocker to its overlapping [20,20,0] position for the captured branch state."),
    ev("W04-09-INDEPENDENT-LUMEN-RECOVERY",72000,"Lumen","After passing its regular slot at T+66000ms, on its next regular slot at T+72000ms use 30ft ordinary ground movement from [50,20,0] to exact origin [20,20,0], within ground speed40. This independent personal movement settles returnOutstanding; no Action/RP/transport power or extra turn is created.","Move the test body back to its actual post-block destination and set returnOutstanding=true in analytic replay; no in-world rewind is claimed.")
]
w04_paid=[
    {"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":0,"resolutionOffsetMs":500,"initialEligibilityPassedBeforeAnyReservation":True,"RPcost":26,"RPbefore":64,"RPafter":38,"action":"Action","components":"V/S/F; focus held","concentrationStartedAtDeclaration":True,"resolution":"final recheck passes; reserves Lumen"},
    {"casterId":"TEST_ONLY_W17D_CASTER_B","route":"independently instantiated TEST_ONLY Wizard17 using the exact W17D acquisition/preparation profile","declarationOffsetMs":10,"resolutionOffsetMs":600,"initialEligibilityPassedBeforeAnyReservation":True,"RPcost":26,"RPbefore":64,"RPafter":38,"action":"its own Action, spent on failed paid resolution","components":"V/S/F; focus held","concentrationStartedAtDeclaration":True,"resolution":"both declarations passed initial check before either reservation; final recheck fails because A now holds the unique identity reservation; no refund, no second body or persistent concentration"}
]
w04_main=wrap_scenario("SH332-W04-TWO-PAID-CASTS-USEFUL-AID-AND-BLOCKED-RETURN-358",w04_events,["two distinct paid declarations","exact W17D route for primary; separately labeled synthetic peer route for competing call","atomic one-identity reservation","competing call excluded at resolution after payment","useful permitted aid on Lumen's own original initiative","finite cargo remains with Lumen","original 60-second deadline","blocked return names exact occupied-volume predicate","no automatic retry or extension","independent lawful movement settles outstanding return","same-arena/same-plane Gate-Bound compatibility","full forward and inverse traversal"],"Same Lumen body is at exact origin after independent movement; call expired, active reservation released, returnOutstanding=false, HP400, token still in custody; no second Lumen body ever existed.",w04_paid,{"ability":"Thread Bind","target":"TEST_ONLY_CREATURE_A","damage":"23 force","usefulResult":"target test-state HP reduced 80→57"})
w04={"id":"SH332-W04-PAID-EXCLUSION-AND-BLOCKED-RETURN-358","profileVersion":"LUMEN-HERALD-W01-358-v1","w02Binding":"SUMMON-HERALD-W02-AUTHORIZED-TEST-STATE-358","classification":"conditional TEST_ONLY witness; no campaign occurrence asserted","witness":w04_main,"counterHistory":{"eligibleCounterAttempts":[],"record":"No counter actor begins during either declaration; no counter cost or outcome is inferred."},"casterBStatus":"Second test caster is explicitly hypothetical, separately individuated, not W17D or an actual campaign actor. Its exact spell access/preparation and current resources are test premises from the bound W17D route template; GPT Director review is requested for this fixture route.","identityInvariant":"At every step the unique registry contains one Lumen identity and at most one Lumen body. Caster B's failed resolution adds no body, clone, projection, reservation or call.","coverage":{"arrival":True,"paidPositivePrimaryCall":True,"usefulAid":True,"originalInitiative":True,"concurrentCallExclusion":True,"secondCallCostsNotRefunded":True,"ordinaryCallExpiration":True,"blockedReturn":True,"explicitReturnOutstanding":True,"independentRecovery":True,"cargoCustody":True,"forwardInverseComplete":True}}
dump("05_SH332_W04_CONCURRENT_CALL_WITNESS_358.json",w04)

def w03_counter_review(scenario_id: str) -> dict:
    cast_id={"SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358":"W03N-01-DECLARE-AND-PAY","SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358":"W03S-01-DECLARE-AND-PAY","SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":"W03D-01-DECLARE-AND-PAY"}[scenario_id]
    return {"castDeclarationEventId":cast_id,"eligibleWindows":[],"ineligibleWindows":[
        {"countererId":"TEST_ONLY_W17D_CASTER_A","triggerCasterId":"TEST_ONLY_W17D_CASTER_A","result":"INELIGIBLE_SELF_CAST","basis":"The automatic Counterspell trigger concerns another creature's casting; the caster cannot counter its own declaration."},
        {"countererId":"Lumen","result":"INELIGIBLE_FEATURE_ABSENT","basis":"The bound W01 identity is an Elemental profile, not a Wizard profile; no Counterspell feature is granted in the bound W01 capability set."},
        {"countererId":"TEST_ONLY_CREATURE_A","result":"INELIGIBLE_FEATURE_ABSENT_AND_NOT_CASTING","basis":"The hypothetical target is explicitly a Construct without a Counterspell capability and does not begin casting in this window."}
    ],"eligibleCounterAttempts":[],"resourceOutcome":"No counter attempt occurs; no RP, Reaction or recharge is spent. TEST_ONLY caster A's automatically acquired Counterspell remains ready."}

for scenario in w03["witnesses"]:
    scenario["counterHistory"]=w03_counter_review(scenario["scenarioId"])

w04_counter_windows=[
    {"windowId":"W04-CS-B-DECLINES-A","offsetMs":0,"triggerCastId":"W04-A-CALL","countererId":"TEST_ONLY_W17D_CASTER_B","triggerCasterId":"TEST_ONLY_W17D_CASTER_A","counterspellKnownAutomatically":True,"reactionAvailableAtTrigger":True,"rechargeStateAtTrigger":"ready","perceivesTrigger":True,"lineOfSight":True,"distanceFeet":5,"within60Feet":True,"eligible":"YES","decision":"EXPLICIT_TEST_ONLY_DECLINE; no Counterspell attempt","rpSpent":0,"reactionSpent":False,"reactionAfter":"available","rechargeAfter":"ready"},
    {"windowId":"W04-CS-A-DECLINES-B","offsetMs":10,"triggerCastId":"W04-B-CALL","countererId":"TEST_ONLY_W17D_CASTER_A","triggerCasterId":"TEST_ONLY_W17D_CASTER_B","counterspellKnownAutomatically":True,"reactionAvailableAtTrigger":True,"rechargeStateAtTrigger":"ready","perceivesTrigger":True,"lineOfSight":True,"distanceFeet":5,"within60Feet":True,"eligible":"YES","decision":"EXPLICIT_TEST_ONLY_DECLINE; no Counterspell attempt","rpSpent":0,"reactionSpent":False,"reactionAfter":"available","rechargeAfter":"ready"}
]
w04_main["counterHistory"]={"eligibleWindows":deepcopy(w04_counter_windows),"eligibleCounterAttempts":[],"resourceOutcome":"Both opposite Wizard Counterspell windows are eligible and explicitly declined. Neither wizard spends RP or Reaction; each automatic Counterspell feature remains ready with zero rounds of recharge remaining."}
w04["counterHistory"]=deepcopy(w04_main["counterHistory"])

def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

def tracked_baseline(with_second_caster: bool = False) -> dict:
    def caster(cid: str, body: list[int], phase: int) -> dict:
        return {"id":cid,"bodyLowerSouthwestCornerFeet":body,"bodyDimensionsFeet":[5,5,5],"rp":64,"dissonance":0,"castHistory":[],"preparedMatrixFamilyHistory":[],"rank9FamilyHistory":[],"actionHistory":[],"counterHistory":[],"conditions":[],"concentrationCallId":None,"concentrationAvailable":True,"lastResolution":None,"focusHeld":True,"componentsAvailable":{"V":True,"S":True,"F":True},"spellAccess":{"class":"Wizard","classLevel":17,"spellInSpellbook":True,"spellPrepared":True,"level17Selection":True,"routeId":"SH332-W17D-CASTING-ROUTE-358"},"perception":{"clearSightToOtherCaster":True if with_second_caster else None,"lineOfSightToOtherCaster":True if with_second_caster else None,"distanceToOtherCasterFeet":5 if with_second_caster else None},"counterspell":{"featureId":"wizard.base.counterspell","acquisition":"automatic at Wizard 2","perceivesAnotherCasterWithin60Feet":True if with_second_caster else None,"rangeFeet":60,"reactionCostRP":3,"reactionAvailable":True,"rechargeRounds":2,"rechargeState":"ready","roundsUntilReady":0,"usesThisFixture":0,"lastWindow":None},"phaseOffsetMs":phase,"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False,"counterspellRecharge":"ready; no use in this fixture"}}
    caster_a=caster("TEST_ONLY_W17D_CASTER_A",[40,10,0],0)
    caster_b=caster("TEST_ONLY_W17D_CASTER_B",[40,15,0],10) if with_second_caster else None
    return {"clockOffsetMs":0,"arenaId":arena["id"],"planeId":arena["planeId"],"sealActive":True,"arenaCombatPhaseActive":False,"scheduledPhaseTransition":False,
      "casters":{"A":caster_a,"B":caster_b},
      "lumen":{"identityKey":w02["uniqueIdentityKey"],"bodyLowerSouthwestCornerFeet":[20,20,0],"dimensionsFeet":[10,10,10],"hp":400,"alive":True,"confirmedDead":False,"conditions":[],"cargoCustody":{"TEST_ONLY_COPPER_TOKEN_358":"Lumen"},"call":None,"reservationId":None,"returnOutstanding":False,"transportSuppressed":False,"threadShatter":{"expended":False,"firstUse":False,"warningTimestamp":None,"recharge":"ready"},"initiativeActions":[],"movementUsedFeet":0,"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}},
      "target":{"id":"TEST_ONLY_CREATURE_A","hp":80,"ac":15,"conditions":[],"resistances":[],"turnsTowardLumen":False,"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}},
      "blocker":{"id":"TEST_ONLY_RETURN_BLOCKER_A","bodyLowerSouthwestCornerFeet":[10,20,0],"dimensionsFeet":[5,5,5],"groundSpeedFeet":30,"conditions":[],"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}},"counterHistory":[],"pendingCallDeclarations":[],"uniqueLumenBodyCount":1}

def path_get(state: dict, pointer: str) -> object:
    value=state
    for part in pointer.strip("/").split("/"): value=value[part]
    return value

def path_set(state: dict, pointer: str, value: object) -> None:
    parts=pointer.strip("/").split("/"); parent=state
    for part in parts[:-1]: parent=parent[part]
    parent[parts[-1]]=deepcopy(value)

def attach_replay(scenario: dict, initial: dict, updates: dict[str,dict[str,object]], turn_ledger: list[dict]) -> None:
    state=deepcopy(initial); records=[]
    authored=deepcopy(scenario["forwardEvents"])
    actor_paths={"TEST_ONLY_W17D_CASTER_A":"/casters/A","TEST_ONLY_W17D_CASTER_B":"/casters/B","TEST_ONLY_CREATURE_A":"/target","TEST_ONLY_RETURN_BLOCKER_A":"/blocker","Lumen":"/lumen"}
    actor_order={"TEST_ONLY_W17D_CASTER_A":10,"TEST_ONLY_W17D_CASTER_B":20,"TEST_ONLY_CREATURE_A":25,"TEST_ONLY_RETURN_BLOCKER_A":26,"Lumen":30}
    end_ms=max((e["virtualOffsetMilliseconds"] for e in authored),default=0)
    matched=set()
    scheduled=[]
    for row in turn_ledger:
        if "slotOffsetMs" not in row or row["actor"] not in actor_paths:
            continue
        actor=row["actor"]; at=row["slotOffsetMs"]
        matches=[e for e in authored if e["virtualOffsetMilliseconds"]==at and e["subject"]==actor and e["eventId"] not in matched]
        slot={"actor":actor,"offsetMs":at,"roundIndex":row["roundIndex"],"initiativePhaseOffsetMs":row.get("initiativePhaseOffsetMs"),"firstScheduledSlotOffsetMs":row.get("firstScheduledSlotOffsetMs"),"actionTaken":row.get("actionTaken",row.get("event","pass")),"regularStartOffsetMs":at,"regularEndOffsetMs":at+5999,"budgetRefresh":{"Action":"ready","BonusAction":"ready","Reaction":"available","movementUsedFeet":0,"companionCommandSpent":False},"counterspellRechargeAtStart":"ready; no use in these windows"}
        if matches:
            event=matches[0]; matched.add(event["eventId"]); event["scheduledTurnStart"]=slot; scheduled.append(event)
        else:
            scheduled.append({"eventId":f"TURN-START-{actor}-{at}","virtualOffsetMilliseconds":at,"subject":actor,"eventType":"regular-turn-start-and-budget-refresh","forwardOperation":slot["actionTaken"],"inverseOperation":"Restore only this actor's exact prior turn budget and active-slot state.","scheduledTurnStart":slot})
        if at+5999<=end_ms:
            scheduled.append({"eventId":f"TURN-END-{actor}-{at+5999}","virtualOffsetMilliseconds":at+5999,"subject":actor,"eventType":"regular-turn-end","forwardOperation":f"Record the regular slot ending at {at+5999}ms; no resource, recharge or extra turn is granted.","inverseOperation":"Remove only this regular-slot end marker.","scheduledTurnEnd":{"actor":actor,"regularStartOffsetMs":at,"regularEndOffsetMs":at+5999,"roundIndex":row["roundIndex"]}})
    for event in authored:
        if event["eventId"] not in matched:
            scheduled.append(event)
    def order_key(event: dict) -> tuple:
        at=event["virtualOffsetMilliseconds"]
        if event.get("eventType") is None and event.get("subject")=="Herald call":
            priority=0 # The original deadline resolves before regular slots at the boundary.
        elif event.get("eventType")=="regular-turn-end":
            priority=1
        elif event.get("scheduledTurnStart"):
            priority=2+actor_order.get(event["scheduledTurnStart"]["actor"],50)
        else:
            priority=100+next((i for i,x in enumerate(authored) if x["eventId"]==event["eventId"]),0)
        return (at,priority,event["eventId"])
    scheduled.sort(key=order_key)
    scenario["forwardEvents"]=scheduled
    for event in scheduled:
        before=deepcopy(state); desired={"/clockOffsetMs":event["virtualOffsetMilliseconds"]}
        slot=event.get("scheduledTurnStart")
        if slot:
            actor_path=actor_paths[slot["actor"]]
            actor_state=deepcopy(path_get(state,actor_path))
            actor_state["turnState"]={"currentRegularSlotStartMs":slot["regularStartOffsetMs"],"scheduledRegularSlotEndMs":slot["regularEndOffsetMs"],"roundIndex":slot["roundIndex"],"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False,"counterspellRecharge":"ready; no use in this fixture"}
            desired[actor_path]=actor_state
        desired.update(updates.get(event["eventId"],{})); forward=[]; inverse=[]
        for pointer,value in desired.items():
            old=deepcopy(path_get(state,pointer))
            if old==value: continue
            forward.append({"op":"replace","path":pointer,"value":deepcopy(value)}); inverse.insert(0,{"op":"replace","path":pointer,"value":old}); path_set(state,pointer,value)
        record={"eventId":event["eventId"],"virtualOffsetMilliseconds":event["virtualOffsetMilliseconds"],"eventType":event.get("eventType","witness-state-transition"),"stateBeforeSHA256":canonical_hash(before),"stateBefore":before,"forwardPatch":forward,"stateAfterSHA256":canonical_hash(state),"stateAfter":deepcopy(state),"inversePatch":inverse,"noStateChange":len(forward)==0}
        records.append(record)
        event["stateBeforeSHA256"]=record["stateBeforeSHA256"]; event["stateBefore"]=before
        event["forwardPatch"]=deepcopy(forward); event["stateAfterSHA256"]=record["stateAfterSHA256"]; event["stateAfter"]=deepcopy(state); event["inversePatch"]=deepcopy(inverse)
    terminal=deepcopy(state); undo=deepcopy(terminal)
    for record in reversed(records):
        assert canonical_hash(undo)==record["stateAfterSHA256"], (scenario["scenarioId"],record["eventId"],"inverse precondition")
        for operation in record["inversePatch"]: path_set(undo,operation["path"],operation["value"])
        assert canonical_hash(undo)==record["stateBeforeSHA256"], (scenario["scenarioId"],record["eventId"],"inverse operation")
    initial_hash=canonical_hash(initial); terminal_hash=canonical_hash(terminal); undo_hash=canonical_hash(undo)
    scenario["startingState"]=deepcopy(initial); scenario["startingStateSHA256"]=initial_hash
    scenario["terminalState"]=deepcopy(terminal); scenario["terminalStateSHA256"]=terminal_hash
    scenario["restoredState"]=deepcopy(undo); scenario["restoredStateSHA256"]=undo_hash; scenario["inverseRestoresInitial"]=undo_hash==initial_hash
    traversal=[]
    for record in reversed(records):
        traversal.append({"undoOf":record["eventId"],"preconditionStateSHA256":record["stateAfterSHA256"],"inversePatch":deepcopy(record["inversePatch"]),"restoredStateSHA256":record["stateBeforeSHA256"],"operationScope":"Undo only the field values changed by this one forward transition."})
    scenario["inverseTraversal"]=traversal
    scenario["inverseEventOrderIsExactReverse"]=[x["undoOf"] for x in traversal]==[e["eventId"] for e in reversed(scheduled)]
    calendar_rows=[]
    for r in turn_ledger:
        row=deepcopy(r)
        if "slotOffsetMs" in row and row.get("actor")!="Herald call clock":
            row.update({"regularStartOffsetMs":row["slotOffsetMs"],"regularEndOffsetMs":row["slotOffsetMs"]+5999,"regularEndOccurredWithinWitness":row["slotOffsetMs"]+5999<=end_ms,"budgetRefreshAtStart":{"Action":"ready","BonusAction":"ready","Reaction":"available","movementUsedFeet":0,"companionCommandSpent":False},"counterspellRechargeCheck":"ready; no use in this fixture; no recharge roll due"})
        elif row.get("actor")=="Herald call clock":
            row["orderedBeforeRegularStartsAtSameBoundary"]=True
        calendar_rows.append(row)
    scenario["regularTurnLedger"]={"roundDurationMilliseconds":6000,"roundDurationSeconds":6,"phaseConvention":"Each actor repeats at its recorded initiative phase every 6000ms. Every scheduled regular start has a budget refresh, and each regular end through the witness endpoint is explicitly represented at start+5999ms. The original 60000ms call deadline resolves before starts at that exact boundary. Idle slots are explicit passes; dead actors receive no regular slot after death.","slots":calendar_rows,"replayEventsIncludeEveryRegularStartAndEndThroughEndpoint":True}
    scenario["replay"]={"trackedScope":"Full spell-relevant TEST_ONLY state for both independent caster instances, regular action/reaction/movement budgets, Counterspell eligibility and recharge, one unique Lumen body, reservation/call, HP/conditions, cargo custody, target, blocker, Seal/arena and clock.","hashEncoding":"SHA-256 of UTF-8 JSON with sorted keys, compact separators, ensure_ascii=False.","initialState":initial,"initialStateSHA256":initial_hash,"events":records,"terminalState":terminal,"terminalStateSHA256":terminal_hash,"inverseTraversal":traversal,"inverseTraversalAppliedInExactReverse":True,"inverseFinalState":undo,"inverseFinalStateSHA256":undo_hash,"inverseMatchesInitial":undo_hash==initial_hash,"status":"PASS" if undo_hash==initial_hash else "FAIL"}

def slots(actor: str, end_ms: int, phase_ms: int, actions: dict[int,str], start_ms: int|None=None) -> list[dict]:
    rows=[]; offset=phase_ms
    while offset<=end_ms:
        if start_ms is None or offset>=start_ms: rows.append({"actor":actor,"slotOffsetMs":offset,"roundIndex":offset//6000,"initiativePhaseOffsetMs":phase_ms%6000,"firstScheduledSlotOffsetMs":phase_ms,"actionTaken":actions.get(offset,"pass; no Action, movement, Reaction, recharge roll, or extra resource" )})
        offset+=6000
    return rows

def make_turn_ledger(sid: str) -> list[dict]:
    end_ms={"SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358":60000,"SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358":66000,"SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":12000,"SH332-W04-TWO-PAID-CASTS-USEFUL-AID-AND-BLOCKED-RETURN-358":72000}[sid]
    rows=slots("TEST_ONLY_W17D_CASTER_A",end_ms,0,{0:"declare and pay one Herald call"})
    if sid.startswith("SH332-W04"): rows+=slots("TEST_ONLY_W17D_CASTER_B",end_ms,10,{10:"pay competing call before either candidate resolves; final reservation check fails"})
    rows+=slots("TEST_ONLY_CREATURE_A",end_ms,3000,{})
    lumen_actions={6000:"elect consented aid on original regular initiative"}
    if sid=="SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358": lumen_actions[60000]="deadline return is resolved before this slot; pass"
    if sid=="SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358": lumen_actions[66000]="ordinary 30-foot recovery movement to exact anchor"
    if sid=="SH332-W04-TWO-PAID-CASTS-USEFUL-AID-AND-BLOCKED-RETURN-358": lumen_actions[66000]="pass after blocker clears; move on next regular slot"
    if sid=="SH332-W04-TWO-PAID-CASTS-USEFUL-AID-AND-BLOCKED-RETURN-358": lumen_actions[72000]="ordinary 30-foot recovery movement to exact anchor"
    if sid=="SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358": lumen_actions.pop(12000,None)
    rows+=slots("Lumen",end_ms,6000,lumen_actions)
    if sid=="SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":
        rows=[r for r in rows if not (r["actor"]=="Lumen" and r["slotOffsetMs"]==12000)]
        rows.append({"actor":"Lumen","scheduledTimeOffsetMs":12000,"roundIndex":2,"event":"no regular turn: confirmed dead before this scheduled slot"})
    if sid.startswith("SH332-W04"):
        rows+=slots("TEST_ONLY_RETURN_BLOCKER_A",end_ms,0,{12000:"move 10 feet into the origin box",66000:"move 10 feet out of the origin box"})
    if sid!="SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358": rows.append({"actor":"Herald call clock","slotOffsetMs":60000,"roundIndex":10,"event":"original 60000ms deadline; resolve expiry/return before slots at this boundary unless death has already ended the call"})
    order={"TEST_ONLY_W17D_CASTER_A":10,"TEST_ONLY_W17D_CASTER_B":20,"TEST_ONLY_CREATURE_A":25,"TEST_ONLY_RETURN_BLOCKER_A":26,"Lumen":30,"Herald call clock":0}
    return sorted(rows,key=lambda r:(r.get("slotOffsetMs",r.get("scheduledTimeOffsetMs",0)),order.get(r["actor"],40)))

def call_state(cid: str,status: str,end: int|None=None,suppressed: bool=False,outcome: str|None=None) -> dict:
    return {"callId":cid,"status":status,"casterId":"TEST_ONLY_W17D_CASTER_A","startOffsetMs":0,"deadlineOffsetMs":60000,"endOffsetMs":end,"returnAnchorFeet":[20,20,0],"destinationFeet":[50,20,0],"transportSuppressed":suppressed,"outcome":outcome}

patches={
"SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358":{
"W03N-01-DECLARE-AND-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W03N-CALL","counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358"),"/counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358")},
"W03N-03-ATOMIC-ADMISSION":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W03N-CALL","active"),"/lumen/reservationId":"W03N-CALL"},
"W03N-04-USEFUL-OWN-TURN-AID":{"/target/hp":52,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":6000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"}]},
"W03N-05-ORIGINAL-DEADLINE":{"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/call":call_state("W03N-CALL","ended-normal",60000,outcome="normal-return"),"/lumen/reservationId":None,"/lumen/returnOutstanding":False,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True}},
"SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358":{
"W03S-01-DECLARE-AND-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W03S-CALL","counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358"),"/counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358")},
"W03S-02-ARRIVAL":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W03S-CALL","active"),"/lumen/reservationId":"W03S-CALL"},
"W03S-03-USEFUL-AID":{"/target/hp":53,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":6000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"}]},
"W03S-04-TEST-ONLY-SUPPRESSION":{"/lumen/call":call_state("W03S-CALL","active",suppressed=True)},
"W03S-05-EXPIRY-WHILE-SUPPRESSED":{"/lumen/call":call_state("W03S-CALL","ended-blocked",60000,True,"return-transport-suppressed"),"/lumen/reservationId":None,"/lumen/returnOutstanding":True,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True},
"W03S-06-RESTORATION-NO-REVIVAL":{"/lumen/call":call_state("W03S-CALL","ended-blocked",60000,False,"return-transport-suppressed")},
"W03S-07-INDEPENDENT-LEGAL-RECOVERY":{"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/returnOutstanding":False,"/lumen/movementUsedFeet":30,"/lumen/turnState/movementUsedFeet":30,"/lumen/initiativeActions":[{"offsetMs":6000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"},{"offsetMs":66000,"slot":"Lumen-original-regular-turn-11","movementFeet":30}]}},
"SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":{
"W03D-01-DECLARE-AND-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W03D-CALL","counterHistory":w03_counter_review("SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358"),"/counterHistory":w03_counter_review("SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358")},
"W03D-02-ARRIVAL":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W03D-CALL","active"),"/lumen/reservationId":"W03D-CALL"},
"W03D-03-USEFUL-AID":{"/target/hp":54,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":6000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"}]},
"W03D-04-TEST-LETHAL-INPUT":{"/lumen/hp":0,"/lumen/alive":False,"/lumen/confirmedDead":True,"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/call":call_state("W03D-CALL","ended-death",12000,outcome="corpse-return"),"/lumen/reservationId":None,"/lumen/returnOutstanding":False,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True}},
"SH332-W04-TWO-PAID-CASTS-USEFUL-AID-AND-BLOCKED-RETURN-358":{
"W04-01-CASTER-A-DECLARE-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W04-A-CALL","pendingCallDeclarations":[{"candidateId":"W04-A-CALL","casterId":"TEST_ONLY_W17D_CASTER_A","initialEligibility":"PASS","resolution":"pending"}],"/casters/B/counterspell/lastWindow":w04_counter_windows[0],"/casters/B/counterHistory":[w04_counter_windows[0]],"/counterHistory":[w04_counter_windows[0]]},
"W04-02-CASTER-B-DECLARE-PAY":{"/casters/B/rp":38,"/casters/B/turnState/action":"spent","/casters/B/concentrationAvailable":False,"/casters/B/actionHistory":[{"atMs":10,"action":"Action","costRP":26,"paid":True}],"/casters/B/castHistory":[{"atMs":10,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/B/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/B/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/B/concentrationCallId":"W04-B-CALL","counterHistory":[w04_counter_windows[0]],"pendingCallDeclarations":[{"candidateId":"W04-A-CALL","casterId":"TEST_ONLY_W17D_CASTER_A","initialEligibility":"PASS","resolution":"pending"},{"candidateId":"W04-B-CALL","casterId":"TEST_ONLY_W17D_CASTER_B","initialEligibility":"PASS","resolution":"pending"}],"/casters/A/counterspell/lastWindow":w04_counter_windows[1],"/casters/A/counterHistory":[w04_counter_windows[1]],"/counterHistory":[w04_counter_windows[0],w04_counter_windows[1]]},
"W04-03-PRIMARY-ADMISSION-ARRIVAL":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W04-A-CALL","active"),"/lumen/reservationId":"W04-A-CALL","pendingCallDeclarations":[{"candidateId":"W04-B-CALL","casterId":"TEST_ONLY_W17D_CASTER_B","initialEligibility":"PASS","resolution":"pending"}]},
"W04-04-CASTER-B-RESOLUTION-FAILS":{"/casters/B/concentrationCallId":None,"/casters/B/concentrationAvailable":True,"/casters/B/lastResolution":"paid-failure:unique-Lumen-reservation-already-held; Action and 26RP remain spent","pendingCallDeclarations":[]},
"W04-05-USEFUL-AID-ORIGINAL-TURN":{"/target/hp":57,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":6000,"slot":"Lumen-original-regular-turn-1","action":"Thread Bind"}]},
"W04-06-RETURN-BLOCKER-ENTERS":{"/blocker/bodyLowerSouthwestCornerFeet":[20,20,0],"/blocker/turnState/movementUsedFeet":10},
"W04-07-DEADLINE-BLOCKED-RETURN":{"/lumen/call":call_state("W04-A-CALL","ended-blocked",60000,outcome="occupied-volume-overlap-at-return-anchor"),"/lumen/reservationId":None,"/lumen/returnOutstanding":True,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True},
"W04-08-BLOCKER-CLEARS":{"/blocker/bodyLowerSouthwestCornerFeet":[10,20,0],"/blocker/turnState/movementUsedFeet":10},
"W04-09-INDEPENDENT-LUMEN-RECOVERY":{"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/returnOutstanding":False,"/lumen/movementUsedFeet":30,"/lumen/turnState/movementUsedFeet":30,"/lumen/initiativeActions":[{"offsetMs":6000,"slot":"Lumen-original-regular-turn-1","action":"Thread Bind"},{"offsetMs":72000,"slot":"Lumen-original-regular-turn-12","movementFeet":30}]}}
}
for scenario in w03["witnesses"]+[w04_main]:
    sid=scenario["scenarioId"]
    attach_replay(scenario,tracked_baseline(sid.startswith("SH332-W04")),patches[sid],make_turn_ledger(sid))
w02["logicalClock"]["regularTurnCalendars"]={
    "W03":{s["scenarioId"]:deepcopy(s["regularTurnLedger"]) for s in w03["witnesses"]},
    "W04":{w04_main["scenarioId"]:deepcopy(w04_main["regularTurnLedger"])}
}
w02["logicalClock"]["calendarBinding"]="Every participant's scheduled regular start, Action/Bonus Action/Reaction/movement refresh, exact 6-second phase, and regular end through the witness endpoint is bound to the replay events in its W03/W04 scenario. The target is a stationary TEST_ONLY Construct with explicit pass slots. Death ends the call at 12000ms and stops Lumen's later regular slots; call deadline precedes regular starts at the same 60000ms boundary."
dump("02_SH332_W02_AUTHORIZED_TEST_STATE_358.json",w02)
dump("04_SH332_W03_LIFECYCLE_WITNESSES_358.json",w03)
dump("05_SH332_W04_CONCURRENT_CALL_WITNESS_358.json",w04)

# Machine-readable binding and sanity checks. This audit verifies structure, scope, geometry, costs and inverses.
scenario_list = w03["witnesses"] + [w04_main]
checks = []
def check(cid: str, ok: bool, detail: str) -> None:
    checks.append({"id":cid,"passed":bool(ok),"detail":detail})

check("W01_CLEAN_REPACK_BINDING", w01["sealedCleanReaffirmation"]["w01Approved"] and not w01["sealedCleanReaffirmation"]["remainingPackagingDefects"] and archive_sha == w01["sealedCleanReaffirmation"]["archiveSHA256"], "W01 remains approved and bound to exact clean Repack01 SHA-256.")
check("W02_OWNER_AUTHORIZATION", AUTH["status"] == "AUTHORIZED_FUTURE_TEST_ONLY_W02_AFTER_W01_APPROVAL" and w02["sourceProfileBinding"]["w01Approval"], "Owner authorization applies only after W01 approval and only to W02/W03/W04.")
check("W02_NO_CAMPAIGN_ASSERTION", not w02["campaignFactsEstablished"] and not w02["actualConsentAsserted"] and not w02["actualLocationAsserted"] and not w02["actualAvailabilityAsserted"], "All synthetic state facts are expressly hypothetical.")
check("W17D_LEGAL_ROUTE", route["spellInSpellbook"] and route["spellPrepared"] and route["level17SelectedSpell"] and route["classLevel"] == 17 and route["RPAndStrain"]["perCastRP"] == 26 and route["profilePointer"]=="/profile" and route["parentProfilePointer"]=="/W17D" and route["parentSourceLineage"]["parentMember"]=="ACTOR_PROFILES.json", "The extracted evidence file is bound at /profile; /W17D is explicitly preserved as the pointer within its parent ACTOR_PROFILES.json archive member.")
check("GEOMETRY_SAME_ARENA", distance_origin_destination <= 120 and distance_caster_destination <= 120 and origin["dimensionsFeet"] == [10,10,10] and destination["dimensionsFeet"] == [10,10,10], "Caster target, body-to-body line and 10-cube fit remain within same hypothetical bounded arena.")
check("ONE_LUMEN_PER_RUN", all(s["oneLumenBodyAtEveryForwardStep"] and s["sameLumenIdentityKey"] == w02["uniqueIdentityKey"] for s in scenario_list), "Each serial scenario uses the same unique Lumen key and never duplicates the body.")
check("PAID_CALL_COSTS", all(all(c.get("RPcost") == 26 for c in s["paidCallDeclarations"]) for s in scenario_list), "Every paid cast attempt uses the approved 26 RP cost.")
check("USEFUL_AID_ON_ORIGINAL_TURN", all(s["usefulAid"] is not None and "original" in " ".join(s["coverage"]).lower() for s in scenario_list), "Each primary positive witness records useful aid on Lumen's original regular initiative.")
check("FULL_INVERSE_TRAVERSAL", all(s["inverseEventOrderIsExactReverse"] and len(s["inverseTraversal"]) == len(s["forwardEvents"]) and s.get("replay",{}).get("status")=="PASS" and s["replay"]["inverseMatchesInitial"] and len(s["replay"]["events"])==len(s["forwardEvents"]) and isinstance(s["startingState"],dict) and isinstance(s["terminalState"],dict) and s["restoredState"]==s["startingState"] and s["inverseRestoresInitial"] and all(set(i["path"] for i in irec["inversePatch"]).issubset({p["path"] for p in frec["forwardPatch"]}) for irec,frec in zip(s["inverseTraversal"],reversed(s["replay"]["events"]))) for s in scenario_list), "Each event carries complete pre/post states, forward and field-scoped inverse patches; full terminal state reverses to an equal, hash-matched starting state in exact reverse order.")
check("SIX_SECOND_TURN_CALENDAR", all(s["regularTurnLedger"]["roundDurationMilliseconds"]==6000 and s["regularTurnLedger"]["replayEventsIncludeEveryRegularStartAndEndThroughEndpoint"] and all((r.get("event") or r["slotOffsetMs"]%6000==r["initiativePhaseOffsetMs"]) for r in s["regularTurnLedger"]["slots"]) and sum(1 for e in s["forwardEvents"] if e.get("scheduledTurnStart"))==sum(1 for r in s["regularTurnLedger"]["slots"] if "slotOffsetMs" in r and r["actor"] in {"TEST_ONLY_W17D_CASTER_A","TEST_ONLY_W17D_CASTER_B","TEST_ONLY_CREATURE_A","TEST_ONLY_RETURN_BLOCKER_A","Lumen"}) and sum(1 for e in s["forwardEvents"] if e.get("scheduledTurnEnd"))==sum(1 for r in s["regularTurnLedger"]["slots"] if "slotOffsetMs" in r and r["actor"] in {"TEST_ONLY_W17D_CASTER_A","TEST_ONLY_W17D_CASTER_B","TEST_ONLY_CREATURE_A","TEST_ONLY_RETURN_BLOCKER_A","Lumen"} and r["slotOffsetMs"]+5999<=max(e["virtualOffsetMilliseconds"] for e in s["forwardEvents"])) for s in scenario_list) and (66000-12000)%6000==0, "Every participating actor's start, budget refresh and regular end through each endpoint is listed and replayed on its recorded 6s phase; blocker moves at 12s and 66s nine rounds apart.")
check("FULL_STATE_UNIQUE_IDENTITY", all(e["stateBefore"].get("uniqueLumenBodyCount")==1 and e["stateAfter"].get("uniqueLumenBodyCount")==1 for s in scenario_list for e in s["replay"]["events"]), "Every full replay state carries exactly one Lumen identity/body.")
check("LIFECYCLE_COVERAGE", w03["coverageSummary"]["ordinaryReturn"] and w03["coverageSummary"]["blockedReturn"] and w03["coverageSummary"]["suppression"] and w03["coverageSummary"]["deathAndCorpse"] and w04["coverage"]["concurrentCallExclusion"], "Normal/blocked returns, suppression, death/corpse, cargo and concurrent-call exclusion covered.")
check("COUNTERSPELL_WINDOWS", all(all(x["result"].startswith("INELIGIBLE") for x in s["counterHistory"]["ineligibleWindows"]) and not s["counterHistory"]["eligibleWindows"] for s in w03["witnesses"]) and len(w04["counterHistory"]["eligibleWindows"])==2 and all(x["eligible"]=="YES" and x["decision"].startswith("EXPLICIT_TEST_ONLY_DECLINE") and x["reactionSpent"] is False and x["rpSpent"]==0 and x["rechargeAfter"]=="ready" for x in w04["counterHistory"]["eligibleWindows"]), "Each W03 casting window records exact Counterspell ineligibility; both W04 opposite-caster windows record automatic feature, perception, range, available Reaction/recharge and explicit no-cost declines.")
death_terminal=w03["witnesses"][2]["terminalState"]
check("DEATH_ENDS_AT_TRIGGER", death_terminal["lumen"]["confirmedDead"] and death_terminal["lumen"]["call"]["endOffsetMs"]==12000 and w03["witnesses"][2]["forwardEvents"][-1]["virtualOffsetMilliseconds"]==12001 and "not a delayed call end" in w03["witnesses"][2]["forwardEvents"][-1]["forwardOperation"].lower(), "Confirmed death ends concentration/call and returns the same corpse at 12000ms; 12001ms is a record-only note, not a later termination.")
check("GATE_BOUND_SCOPE", all(s["terminalState"]["arenaId"]==arena["id"] and s["terminalState"]["planeId"]==arena["planeId"] and s["terminalState"]["sealActive"] and s["terminalState"]["lumen"]["bodyLowerSouthwestCornerFeet"]==origin["lowerSouthwestCornerFeet"] for s in scenario_list), "Full terminal states remain inside the same TEST_ONLY home arena and plane, at the recorded origin; Seal remains active.")

validation={"id":"SH332-W02-W03-W04-BUILD-VALIDATION-358","recordedAtUtc":recorded,"status":"PASS" if all(c["passed"] for c in checks) else "FAIL","checks":checks,"witnessCount":len(scenario_list),"coverage":{"W03_normal_return":True,"W03_suppression":True,"W03_death_corpse":True,"W04_paid_concurrent_exclusion":True,"W04_blocked_return_and_independent_recovery":True,"cargo":True,"usefulAid":True,"forwardInverse":True},"limitations":["Builder sanity checks only; a separate replay verifier runs below.","Conditional TEST_ONLY evidence is not identity acceptance.","No canonical catalog, runtime, public spell procedure, or campaign history is modified."]}
dump("06_SH332_W02_W03_W04_BUILD_VALIDATION_358.json", validation)
if validation["status"] != "PASS":
    raise SystemExit("Witness validation failed")

verifier_path=OUT/"verify_herald_w02_witness_358.py"
if not verifier_path.exists():
    raise SystemExit("Independent verifier source is missing")
subprocess.run([sys.executable,str(verifier_path)],check=True)

# Include only intended evidence. The manifest is self-excluded from its own member list.
members = [
    "01_SH332_W01_CLEAN_REAFFIRMATION_358.json",
    "OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json",
    "02_SH332_W02_AUTHORIZED_TEST_STATE_358.json",
    "03_SH332_W17D_CASTING_ROUTE_358.json",
    "04_SH332_W03_LIFECYCLE_WITNESSES_358.json",
    "05_SH332_W04_CONCURRENT_CALL_WITNESS_358.json",
    "06_SH332_W02_W03_W04_BUILD_VALIDATION_358.json",
    "07_SH332_W02_W03_W04_INDEPENDENT_VALIDATION_358.json",
    "verify_herald_w02_witness_358.py",
]
if not (OUT/"OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").exists():
    (OUT/"OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").write_bytes(AUTH_PATH.read_bytes())
manifest={"id":"SH332-W02-W03-W04-TESTONLY-358-REPACK02-MANIFEST","classification":"test-only witness delivery manifest","memberCountExcludingSelf":len(members),"members":[{"path":n,"bytes":(OUT/n).stat().st_size,"sha256":sha(OUT/n)} for n in members],"selfExcluded":True}
dump("MEMBER_MANIFEST.json",manifest)
zip_path=OUT/"DD_Rank9_SummonHerald_SH332_W02_W03_W04_TESTONLY_358_Repack02.zip"
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for n in members: z.write(OUT/n,n)
    z.write(OUT/"MEMBER_MANIFEST.json","MEMBER_MANIFEST.json")
with zipfile.ZipFile(zip_path) as z:
    names=z.namelist()
    assert len(names)==len(set(names)) and set(names)==set(members+['MEMBER_MANIFEST.json'])
    for m in manifest["members"]:
        b=z.read(m["path"])
        assert len(b)==m["bytes"] and hashlib.sha256(b).hexdigest()==m["sha256"]
independent=json.loads((OUT/"07_SH332_W02_W03_W04_INDEPENDENT_VALIDATION_358.json").read_text(encoding="utf-8"))
delivery={"id":"SH332-W02-W03-W04-TESTONLY-358-DELIVERY","archive":zip_path.name,"archiveBytes":zip_path.stat().st_size,"archiveSHA256":sha(zip_path),"manifestPath":str((OUT/'MEMBER_MANIFEST.json').relative_to(ROOT)).replace('\\','/'),"manifestSHA256":sha(OUT/'MEMBER_MANIFEST.json'),"memberCount":len(members),"status":"READY_FOR_DIRECTOR_REVIEW_NOT_IDENTITY_ACCEPTANCE","buildValidationStatus":validation["status"],"independentReplayValidationStatus":independent["status"],"identityDisposition":{"decision":"HOLD","acceptedIds":[],"appliedIds":[],"blockerIds":["SH202-B02"],"applicationAuthorized":False}}
dump("DELIVERY.json",delivery)
print(json.dumps({"output":str(OUT),"validation":validation["status"],"archive":str(zip_path),"archiveBytes":zip_path.stat().st_size,"archiveSHA256":sha(zip_path),"checks":len(checks)},indent=2))
