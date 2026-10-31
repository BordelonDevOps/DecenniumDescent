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
OUT = AUDIT / "rank9_summon_herald_w02_witness_358_repack04"
OUT.mkdir(parents=True, exist_ok=True)

AUTH_PATH = AUDIT / "OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json"
W17D_PATH = AUDIT / "rank9_summon_herald_of_the_planes_return332_received/payload/evidence/EXISTING_W17D_PROFILE.json"
REPACK_PATH = AUDIT / "rank9_summon_herald_w01_content_reconciliation_358_repack01/DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01.zip"
READY_SOURCE_PATH = ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md"
READY_SOURCE_TEXT = READY_SOURCE_PATH.read_text(encoding="utf-8").splitlines()
READY_SOURCE_BINDING = {
    "sourcePath": READY_SOURCE_PATH.relative_to(ROOT).as_posix(),
    "sourceSHA256": hashlib.sha256(READY_SOURCE_PATH.read_bytes()).hexdigest(),
    "sourceLines": [97, 111],
    "sourceExcerpt": "\n".join(READY_SOURCE_TEXT[96:111]),
    "rulesApplied": {
        "preparation": "Ready spends the caster's Action, declares a perceivable trigger and casts the spell at preparation; verify legality, pay costs, provide components, resolve cast triggers and Counterspell opportunity once.",
        "hold": "Every held spell requires concentration from preparation; Ready expires at the caster's next regular own-turn start.",
        "release": "The trigger occurs first; the readied response immediately follows before later events. Release spends the normal Reaction and rechecks target and other prerequisites.",
        "targetAndClock": "Select the legal target at release and recheck without repaying. A concentration spell continues as ordinary concentration after release. Preserve any sealed source-specific duration clock: Summon Herald W01 fixes its temporary-call deadline at paid declaration/preparation+60000ms. Ready release manifests the call at release but does not reset that deadline. In W04, preparation=0ms, release=1000ms, deadline=60000ms, leaving 59000ms active.",
        "counterspell": "Counterspell opportunity occurs at preparation, not again at release."
    }
}
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
                {"offsetMs": 0, "actor": "TEST_ONLY_W17D_CASTER_A", "slot": "phase 0; its own regular Action slot; ends before target phase 2000"},
                {"offsetMs": 2000, "actor": "TEST_ONLY_CREATURE_A", "slot": "phase 2000; pass if idle; ends before Lumen phase 4000"},
                {"offsetMs": 4000, "actor": "Lumen", "slot": "phase 4000; original regular initiative aid slot; ends at 5999"},
                {"offsetMs": 60000, "actor": "call clock", "slot": "original deadline; no turn is granted"}
            ],
            "W04": [
                {"offsetMs": 0, "actor": "TEST_ONLY_W17D_CASTER_B", "slot": "phase 0; Ready Action prepares and pays the spell; turn ends at 999"},
                {"offsetMs": 1000, "actor": "TEST_ONLY_W17D_CASTER_A", "slot": "phase 1000; its own ordinary Action; B releases from outside its turn by Reaction"},
                {"offsetMs": 2000, "actor": "TEST_ONLY_CREATURE_A", "slot": "phase 2000; pass if idle"},
                {"offsetMs": 3000, "actor": "Lumen", "slot": "phase 3000; original regular initiative aid slot"},
                {"offsetMs": 4000, "actor": "TEST_ONLY_RETURN_BLOCKER_A", "slot": "phase 4000; blocker moves at 16000 and 70000ms"},
                {"offsetMs": 60000, "actor": "call clock", "slot": "W01 paid-preparation+60000ms deadline; resolves before B's regular start at this same offset"},
                {"offsetMs": 75000, "actor": "Lumen", "slot": "next legal regular slot after the blocker clears; independent movement only"}
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
        "competingReservationOrConcurrentCall": {"baseline": None, "classification": "TEST_ONLY premise", "uniquenessRule": "one identity key and one body; in W04, B's correctly Readied spell is held outside the active-call registry while A begins a later ordered ordinary cast. B's legal Reaction release reserves first; A's pending ordinary cast fails its final check and cannot create another body, reservation or call."},
        "affirmativeConsentToExactCall": {
            "value": True, "classification": "TEST_ONLY explicit premise, not real consent",
            "consentingIdentity": "Lumen of the Shattered Thread (hypothetical test persona)",
            "scope": "For W03, the one described paid temporary call. For W04, B's TEST_ONLY Ready preparation on B's earlier ordered turn and one triggered Reaction release when A begins a later-turn cast: B selects Lumen at release, passes the then-current admission predicates and establishes the sole call; A's pending cast fails its final uniqueness check. Lumen consents to the successful same-arena/same-plane arrival, one permitted Thread Bind on its original regular initiative, the finite cargo, the immutable W01 60000ms deadline measured from paid Ready preparation; the active manifestation lasts the remaining 59000ms, blocked return and independent recovery. Consent does not authorize a second movement, body, call, aid, or control.",
            "exclusions": ["no compelled obedience", "no extra action or turn", "no hidden knowledge or disclosure", "no cross-arena or cross-plane travel", "no Seal or Gate alteration", "no permanent displacement", "no transfer of another actor's action economy"]
        },
        "permittedAidOrCommandScope": {
            "classification": "TEST_ONLY consent premise bounded by the approved profile",
            "W03": "One Thread Lance against TEST_ONLY_CREATURE_A on Lumen's next original regular initiative slot.",
        "W04": "One Thread Bind against TEST_ONLY_CREATURE_A on Lumen's original regular initiative slot at phase 3000ms.",
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
            {"id": "TEST_ONLY_W17D_CASTER_B", "kind": "hypothetical second Wizard caster", "type": "Humanoid", "bodyBoxFeet": {"lowerSouthwestCorner": [40,15,0], "dimensions": [5,5,5]}, "positionRelativeToPrimaryCaster": "boundary-touch only; no overlap", "preparedHerald": True, "currentRP": 64, "currentDissonance": 0, "conditions": [], "concentrationAvailable": True, "actionAvailableAtOwnSlot": True, "reactionAvailable": True, "counterspellKnownAutomaticallyAtWizard2": True, "counterspellRechargeState": "ready; 0 rounds remaining", "arcaneFocusHeld": True, "componentsAvailable": {"V": True, "S": True, "F": True}, "perception": {"canSeeCasterA": True, "clearLineOfSight": True, "distanceToCasterAFeet": 5, "spellPerceptionUnobstructed": True}, "history": {"spellCastHistory": [], "preparedMatrixFamilyHistory": [], "rank9FamilyHistory": [], "concentrationHistory": [], "counterspellUses": 0}, "ownRegularActionSlotOffsetMs": 0, "W04Action": "Ready Action prepares the spell on B's own earlier slot; release uses B's Reaction on A's later-turn trigger."},
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
        "casterUseForW04": "A second distinct hypothetical test caster uses the bound Wizard17 acquisition/preparation route. B prepares the Action-time spell with Ready on B's earlier ordered turn; it is cast and paid at preparation, held under concentration, then released with B's Reaction on A's later-turn trigger. This is a test persona, not a duplicate campaign actor or a claim that W17D has a second body."
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
        {"id":"TEST_ONLY_W17D_CASTER_B","profileIdentity":"independent synthetic instance of the same legal Wizard17 route","sourceBoundRoute":"TEST_ONLY instantiation of the exact W17D level-17 Herald selection/preparation route; expressly not actual W17D","classification":"TEST_ONLY persona, not a campaign actor","body":{"lowerSouthwestCornerFeet":[40,15,0],"dimensionsFeet":[5,5,5],"centerFeet":[42.5,17.5,2.5]},"currentRP":64,"currentDissonance":0,"conditions":[],"castHistory":[],"preparedMatrixFamilyHistory":[],"rank9FamilyHistory":[],"freeConcentration":True,"actionState":"B's phase-0 own slot prepares a Ready spell; release at A's later-turn trigger spends B's Reaction","reactionState":"available through the preparation and A-cast Counterspell windows; spent only to release the held spell","counterspell":{"knownAutomaticallyAtWizard2":True,"eligibleTrigger":"another creature it perceives beginning a spell within 60 feet","recharge":"ready; zero rounds remaining","usesInFixture":0},"perception":{"canSeeCasterA":True,"clearLineOfSight":True,"distanceToCasterAFeet":5,"spellPerceptionUnobstructed":True},"focusHeld":True,"componentsAvailable":{"V":True,"S":True,"F":True}}
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
    ev("W03N-04-USEFUL-OWN-TURN-AID",4000,"Lumen","On its next original regular slot, choose the consented Thread Lance. Roll d20=12 +11=23 vs target AC15; roll 4d10=[3,4,5,6], +10 = 28 radiant; TEST_ONLY_CREATURE_A HP 80→52. No other attack or rider.","Restore target HP 80 and clear only this synthetic attack record; leave Lumen at its pre-attack test HP/conditions."),
    ev("W03N-05-ORIGINAL-DEADLINE",60000,"Herald call","At declaration+60000ms, end concentration/call; one automatic return attempt checks same-arena/plane, anchor fit/support, LoE, wards, cargo and permission. All pass; relocate same body and still-carried token to exact recorded origin. Release reservation; no Action/RP payment, retry, phase or recharge reset.","Restore the active-call snapshot at T0+59999ms for reverse traversal, then undo the admission and declaration events in their listed reverse order.")
]
w03_normal_paid = [{"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":0,"action":"Action","rank":9,"RPcost":26,"RPbefore":64,"RPafter":38,"components":{"V":True,"S":True,"F":True,"focusHeld":True},"concentrationStarted":True,"deadlineOffsetMs":60000,"counterHistory":"none attempted"}]
w03_normal = wrap_scenario("SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358",w03_normal_events,["paid declaration and source route","arrival and 10-cube supported fit","useful aid on Lumen's original regular initiative","finite cargo is returned in custody","original 60000ms deadline","normal return to exact anchor","resources and state preserved","complete forward and inverse traversal"],"One Lumen body at exact source anchor; HP400; no conditions; token in Lumen custody; call ended; no reservation; Gate-Bound Seal unchanged.",w03_normal_paid,{"ability":"Thread Lance","target":"TEST_ONLY_CREATURE_A","damage":"28 radiant","usefulResult":"target test-state HP reduced 80→52"})

# W03 suppression branch: original clock continues; no revival after transport restoration.
w03_suppress_events = [
    ev("W03S-01-DECLARE-AND-PAY",0,"TEST_ONLY_W17D_CASTER_A","Pay 26 RP (64→38) for one legal Action/V/S/F cast and start a 60000ms concentration clock.","Restore caster baseline, including RP64 and no concentration."),
    ev("W03S-02-ARRIVAL",500,"Lumen","Recheck all admission predicates; reserve the unique identity and arrive at the supported destination with the same token.","Return the same body/token to the recorded source and clear the active reservation in analytic rollback."),
    ev("W03S-03-USEFUL-AID",4000,"Lumen","On its original regular slot, resolve consented Thread Lance against TEST_ONLY_CREATURE_A; d20=11 +11=22 vs AC15; 4d10=[2,5,4,6]+10=27 radiant; target HP80→53.","Restore TEST_ONLY_CREATURE_A HP to80 and remove this synthetic attack result."),
    ev("W03S-04-TEST-ONLY-SUPPRESSION",59900,"Call transport state","The isolated harness sets returnTransportSuppressed=true as an explicit TEST_ONLY branch input. It does not suppress or move Lumen, alter the arena, restart the clock, or claim a world ward.","Remove the synthetic suppression input after the captured branch; do not change the already-ended call."),
    ev("W03S-05-EXPIRY-WHILE-SUPPRESSED",60000,"Herald call","The original deadline expires. Automatic return is attempted once and blocked solely because call transport is currently suppressed. End call/concentration, release active reservation, keep same body and token at actual destination, preserve HP/conditions/custody, set returnOutstanding=true; no retry or extension.","Restore the exact pre-expiry active-call state only in the analytic replay, then reverse arrival and paid declaration."),
    ev("W03S-06-RESTORATION-NO-REVIVAL",61000,"Call transport state","Restore the hypothetical transport channel. The expired call stays expired and makes no automatic retry; returnOutstanding remains true.","Reapply the synthetic suppressed flag to recover the prior captured branch state."),
    ev("W03S-07-INDEPENDENT-LEGAL-RECOVERY",64000,"Lumen","On Lumen's own next regular slot after suppression clears, use 30ft of ordinary ground movement (≤40ft) over clear supported floor to the exact origin. No call transport, Action, RP, extra turn or refreshed resource. Clear returnOutstanding only upon arrival.","For analytic inverse, restore Lumen to the test endpoint and reinstate returnOutstanding=true; this is not an in-world rewind.")
]
w03_suppress = wrap_scenario("SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358",w03_suppress_events,["paid W17D-route cast","supported arrival and finite cargo","useful aid on original initiative","suppression at deadline","original clock not extended","one blocked return with explicit predicate","restoration does not revive expired call","independent legal movement resolves outstanding return","complete forward and inverse traversal"],"After independent recovery: same body at origin; call remains expired; reservation released; returnOutstanding=false; token remains in Lumen custody.",[{"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":0,"action":"Action","rank":9,"RPcost":26,"RPbefore":64,"RPafter":38,"components":"V/S/F; focus held","concentrationStarted":True,"deadlineOffsetMs":60000}],{"ability":"Thread Lance","target":"TEST_ONLY_CREATURE_A","damage":"27 radiant","usefulResult":"target test-state HP reduced 80→53"})

# W03 death branch: death is a declared test input and follows the core monster-at-zero default; no resurrection.
w03_death_events = [
    ev("W03D-01-DECLARE-AND-PAY",0,"TEST_ONLY_W17D_CASTER_A","Pay 26 RP (64→38), declare one prepared rank-9 Action/V/S/F cast, and begin the fixed 60000ms deadline.","Restore caster baseline and clear test-only cast history."),
    ev("W03D-02-ARRIVAL",500,"Lumen","Recheck admission, atomically reserve and relocate the single body plus finite token to supported destination.","Move the same body/token to exact origin and clear the reservation in analytic rollback."),
    ev("W03D-03-USEFUL-AID",4000,"Lumen","On its original regular slot, resolve consented Thread Lance; d20=14+11=25 vs AC15; 4d10=[2,3,5,6]+10=26 radiant; target HP80→54.","Restore target HP80 and erase the synthetic attack record."),
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

# W04: B legally readies its Action-time spell on the earlier ordered turn, then releases by Reaction when A begins a later-turn cast.
w04_events = [
    ev("W04-01-CASTER-B-READY-PREPARE",0,"TEST_ONLY_W17D_CASTER_B","On B's own first regular turn, spend Ready Action to cast the prepared rank-9 Herald with V/S/F and pay 26 RP (64→38). Declare the perceivable trigger: A begins casting this prepared Herald on Lumen while the identity is not reserved. Verify route/source legality; hold the spell under B's concentration, with next-own-turn expiry at 6000ms. Select and recheck the target at release. The TEST_ONLY manifestation begins at release, while sealed W01 fixes the call deadline at paid preparation+60000ms (60000ms absolute; 59000ms remain after release). No reservation or Lumen movement occurs yet.","Restore B RP64, free concentration, ready Action, no Ready state and empty cast/prepared-history in the isolated baseline."),
    ev("W04-02-COUNTERSPELL-A-DECLINES-B-PREPARATION",0,"TEST_ONLY_W17D_CASTER_A","At B's Ready preparation cast trigger, A has an eligible automatic Counterspell window, perceives the caster within 60 feet, and explicitly declines without spending Reaction or RP. Ready source permits only this preparation-time cast window; no Counterspell window is created again at B's later release.","Restore A's ready Counterspell/reaction state and remove this fixture-only decline record."),
    ev("W04-03-CASTER-A-DECLARE-PAY",1000,"TEST_ONLY_W17D_CASTER_A","On A's own later regular Action, declare the ordinary prepared rank-9 Herald cast at Lumen, pay 26 RP (64→38), supply V/S/F and begin concentration. Its initial admission check passes while Lumen is unreserved; keep A's candidate pending until 1200ms. This occurs after B's regular turn ended at 999ms.","Restore A RP64, free concentration, ready Action and empty cast/prepared-history in the isolated baseline."),
    ev("W04-04-COUNTERSPELL-B-DECLINES-A-CAST",1000,"TEST_ONLY_W17D_CASTER_B","A's ordinary cast begins while B's own earlier turn is complete. B has a currently available Reaction, perceives A within 60 feet, and explicitly declines its eligible automatic Counterspell window at cast start without spending RP/Reaction. It then uses that same still-available Reaction for the triggered Ready release below. The decline is not an additional Reaction spend.","Restore B's eligible window state and remove its decline record; the Ready preparation/action history is reversed by its own inverse."),
    ev("W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN",1000,"TEST_ONLY_W17D_CASTER_B","The declared trigger has occurred, so B immediately spends its normal Reaction and releases the already-cast held spell before later events. Select TEST_ONLY Lumen as the target now and recheck source, consent, fit, same-arena/plane, line, permission and uniqueness. All pass before either candidate has reserved; atomically reserve the one identity, move the same body/token to supported destination and begin the manifested call at release while preserving the sealed W01 absolute deadline of 60000ms from paid preparation (59000ms remain). B's held concentration continues as ordinary concentration; no second cast, payment, cast-trigger or Counterspell window occurs at release.","Return the same body/token to exact source and restore B's pending Ready state/reaction only for analytic rollback; reverse no other candidate or resource."),
    ev("W04-06-CASTER-A-FINAL-ADMISSION-FAILS",1200,"TEST_ONLY_W17D_CASTER_A","Resolve A's already-paid ordinary cast within A's own still-open turn. Its final admission recheck now fails solely because B's earlier Ready release holds the unique Lumen reservation. A's 26 RP and Action remain spent; end only A's failed concentration/candidate. No refund, second body, second reservation, persistent A concentration or retry.","Restore A's paid pending-cast state, then reverse A's declaration and payment."),
    ev("W04-07-USEFUL-AID-ORIGINAL-TURN",3000,"Lumen","On its existing original regular slot after the successful 1000ms release, elect consented Thread Bind. Roll d20=10+11=21 vs AC15; damage 3d10=[4,6,5]+8=23 force; target HP80→57. No restraint rider.","Restore target HP80 and clear the synthetic attack result."),
    ev("W04-08-RETURN-BLOCKER-ENTERS",16000,"TEST_ONLY_RETURN_BLOCKER_A","On its own phase-4000 regular slot, move 10ft from [10,20,0] to [20,20,0] at 30ft ground speed. Its 5-cube overlaps the recorded 10-cube return anchor; movement is voluntary TEST_ONLY fixture movement.","Move the same test blocker back to [10,20,0] on its own regular slot in analytic inverse."),
    ev("W04-09-DEADLINE-BLOCKED-RETURN",60000,"Herald call","At the sealed W01 absolute deadline, paid preparation+60000ms (60000ms), end B's active call/concentration. One automatic return attempt fails solely on occupied-volume overlap with TEST_ONLY_RETURN_BLOCKER_A at exact source anchor. Record returnOutstanding=true, release active reservation after outcome, retain Lumen body/cargo/HP/conditions/custody at actual destination; no retry, extension, forced placement or second body. Resolve this absolute clock at 60000ms before B's regular-start marker at the same offset.","Restore the active call at T0+59999ms for analytic replay, then reverse blocker movement, aid, failed A cast, B release, counter windows and B preparation in reverse order."),
    ev("W04-10-BLOCKER-CLEARS",70000,"TEST_ONLY_RETURN_BLOCKER_A","On its own phase-4000 regular slot, 54 seconds after entering at 16000ms (nine six-second rounds later), move 10ft back to [10,20,0]. It no longer overlaps Lumen's exact origin box; no forced or magical movement.","Restore blocker to its overlapping [20,20,0] position for the captured branch state."),
    ev("W04-11-INDEPENDENT-LUMEN-RECOVERY",75000,"Lumen","After its 69000ms regular slot passes while the anchor remains blocked, on its next regular slot at 75000ms use 30ft ordinary ground movement from [50,20,0] to exact origin [20,20,0], within ground speed40. This independent personal movement settles returnOutstanding; no Action/RP/transport power or extra turn is created.","Move the test body back to its actual post-block destination and set returnOutstanding=true in analytic replay; no in-world rewind is claimed.")
]
w04_paid=[
    {"casterId":"TEST_ONLY_W17D_CASTER_B","route":"independently instantiated TEST_ONLY Wizard17 using the exact W17D acquisition/preparation profile","preparationOffsetMs":0,"preparationAction":"Ready Action; B's ordered regular slot is 0–999ms","readyTrigger":"A begins an ordinary prepared Herald cast on Lumen while Lumen has no reservation; perceivable V/S/F casting at 5 feet","castAndCostAtPreparation":True,"RPcost":26,"RPbefore":64,"RPafter":38,"components":"V/S/F; focus held","concentrationStartsAtPreparation":True,"readyExpiryNextOwnTurnStartMs":6000,"counterspellOpportunity":"at preparation only; A explicitly declines","releaseOffsetMs":1000,"releaseCost":"B's normal Reaction, spent once","targetSelectedAtRelease":True,"effectDurationStartsAtRelease":True,"effectDurationRemainingMsAtRelease":59000,"deadlineAnchor":"sealed W01 paid Ready preparation at 0ms + 60000ms","deadlineOffsetMs":60000,"resolution":"release final check passes and reserves Lumen; held concentration continues as the active call"},
    {"casterId":"TEST_ONLY_W17D_CASTER_A","route":"SH332-W17D-CASTING-ROUTE-358","declarationOffsetMs":1000,"resolutionOffsetMs":1200,"action":"ordinary Action on A's ordered regular slot 1000–1999ms","RPcost":26,"RPbefore":64,"RPafter":38,"initialEligibilityPassedBeforeReservation":True,"components":"V/S/F; focus held","concentrationStartedAtDeclaration":True,"counterspellOpportunity":"at cast start; B explicitly declines before using its Reaction to release Ready","resolution":"final recheck fails solely because B's earlier-legal Ready release now holds the unique identity reservation; Action/RP remain spent and failed concentration ends"}
]
w04_main=wrap_scenario("SH332-W04-READY-RELEASE-UNIQUE-ADMISSION-AND-BLOCKED-RETURN-358",w04_events,["B prepares and casts Ready spell on its own earlier ordered regular turn","Ready hold requires concentration and expires at B's next own regular start","B releases with one normal Reaction on A's later-turn trigger","target selected and rechecked at release without repaying","the manifestation begins at release; the immutable W01 deadline remains paid preparation+60000ms (60000ms absolute; 59000ms active after release)","opposite-caster Counterspell windows occur only at actual preparation/cast starts and are explicitly declined","one identity reservation; A's later final admission fails without duplicate","useful permitted aid on Lumen's original initiative","finite cargo remains with Lumen","blocker enters and clears only on its own ordered regular slots","deadline blocked-return names exact occupied-volume predicate","independent lawful movement settles outstanding return","same-arena/same-plane Gate-Bound compatibility","full forward and inverse traversal"],"Same Lumen body is at exact origin after independent movement; B's released call expired, active reservation released, returnOutstanding=false, HP400, token still in custody; no second Lumen body ever existed.",w04_paid,{"ability":"Thread Bind","target":"TEST_ONLY_CREATURE_A","damage":"23 force","usefulResult":"target test-state HP reduced 80→57"})
w04={"id":"SH332-W04-READY-RELEASE-AND-BLOCKED-RETURN-358","profileVersion":"LUMEN-HERALD-W01-358-v1","w02Binding":"SUMMON-HERALD-W02-AUTHORIZED-TEST-STATE-358","classification":"conditional TEST_ONLY witness; no campaign occurrence asserted","witness":w04_main,"readyRuleBinding":READY_SOURCE_BINDING,"counterHistory":{"eligibleCounterAttempts":[],"record":"Both preparation/cast-start Counterspell windows are explicit, eligible and cost-free declined. B then spends its ordinary Reaction once to release the held spell; the Ready release creates no second Counterspell window."},"casterBStatus":"Second test caster is explicitly hypothetical, separately individuated, not W17D or an actual campaign actor. It uses a correctly sourced Ready Action on an earlier ordered turn, holds its already-cast spell under concentration, then spends its ordinary Reaction at the exact later-turn trigger. Target selection and effect duration begin at release; the held concentration continues as the active call.","identityInvariant":"At every step the unique registry contains one Lumen identity and at most one Lumen body. B's successful Ready release creates the single reservation; A's later failed admission adds no body, clone, projection or second reservation.","coverage":{"arrival":True,"paidPositivePrimaryCall":True,"usefulAid":True,"originalInitiative":True,"readyPreparedAndReleasedLegally":True,"orderedTurnSequence":True,"concurrentAdmissionExclusion":True,"concurrentCallExclusion":True,"secondCallCostsNotRefunded":True,"ordinaryCallExpirationFromRelease":True,"blockedReturn":True,"explicitReturnOutstanding":True,"independentRecovery":True,"cargoCustody":True,"forwardInverseComplete":True}}
dump("05_SH332_W04_CONCURRENT_CALL_WITNESS_358.json",w04)
dump("08_READY_ACTION_RULE_BINDING_358.json",READY_SOURCE_BINDING)

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
    {"windowId":"W04-CS-A-DECLINES-B-READY-PREPARATION","offsetMs":0,"triggerCastId":"W04-B-HELD-READY-SPELL","countererId":"TEST_ONLY_W17D_CASTER_A","triggerCasterId":"TEST_ONLY_W17D_CASTER_B","counterspellKnownAutomatically":True,"reactionAvailableAtTrigger":True,"rechargeStateAtTrigger":"ready","perceivesTrigger":True,"lineOfSight":True,"distanceFeet":5,"within60Feet":True,"eligible":"YES","decision":"EXPLICIT_TEST_ONLY_DECLINE; no Counterspell attempt","rpSpent":0,"reactionSpent":False,"reactionAfter":"available","rechargeAfter":"ready","windowTiming":"Ready spell preparation cast; no second window at release"},
    {"windowId":"W04-CS-B-DECLINES-A-CAST","offsetMs":1000,"triggerCastId":"W04-A-CALL","countererId":"TEST_ONLY_W17D_CASTER_B","triggerCasterId":"TEST_ONLY_W17D_CASTER_A","counterspellKnownAutomatically":True,"reactionAvailableAtTrigger":True,"rechargeStateAtTrigger":"ready","perceivesTrigger":True,"lineOfSight":True,"distanceFeet":5,"within60Feet":True,"eligible":"YES","decision":"EXPLICIT_TEST_ONLY_DECLINE; no Counterspell attempt","rpSpent":0,"reactionSpent":False,"reactionAfter":"available before Ready release","rechargeAfter":"ready","windowTiming":"A's ordinary cast-start window; B then spends its still-available Reaction on the triggered Ready release"}
]
w04_main["counterHistory"]={"eligibleWindows":deepcopy(w04_counter_windows),"eligibleCounterAttempts":[],"resourceOutcome":"Both actual preparation/cast-start Counterspell windows are eligible and explicitly declined without RP or Reaction cost. B then spends its ordinary Reaction once on the Ready release; no new Counterspell opportunity occurs at release."}
w04["counterHistory"]=deepcopy(w04_main["counterHistory"])

def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

def tracked_baseline(with_second_caster: bool = False) -> dict:
    def caster(cid: str, body: list[int], phase: int) -> dict:
        return {"id":cid,"bodyLowerSouthwestCornerFeet":body,"bodyDimensionsFeet":[5,5,5],"rp":64,"dissonance":0,"castHistory":[],"preparedMatrixFamilyHistory":[],"rank9FamilyHistory":[],"actionHistory":[],"counterHistory":[],"conditions":[],"concentrationCallId":None,"concentrationAvailable":True,"readySpell":None,"lastResolution":None,"focusHeld":True,"componentsAvailable":{"V":True,"S":True,"F":True},"spellAccess":{"class":"Wizard","classLevel":17,"spellInSpellbook":True,"spellPrepared":True,"level17Selection":True,"routeId":"SH332-W17D-CASTING-ROUTE-358"},"perception":{"clearSightToOtherCaster":True if with_second_caster else None,"lineOfSightToOtherCaster":True if with_second_caster else None,"distanceToOtherCasterFeet":5 if with_second_caster else None},"counterspell":{"featureId":"wizard.base.counterspell","acquisition":"automatic at Wizard 2","perceivesAnotherCasterWithin60Feet":True if with_second_caster else None,"rangeFeet":60,"reactionCostRP":3,"reactionAvailable":True,"rechargeRounds":2,"rechargeState":"ready","roundsUntilReady":0,"usesThisFixture":0,"lastWindow":None},"phaseOffsetMs":phase,"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False,"counterspellRecharge":"ready; no use in this fixture"}}
    caster_a=caster("TEST_ONLY_W17D_CASTER_A",[40,10,0],1000 if with_second_caster else 0)
    caster_b=caster("TEST_ONLY_W17D_CASTER_B",[40,15,0],0) if with_second_caster else None
    return {"clockOffsetMs":0,"arenaId":arena["id"],"planeId":arena["planeId"],"sealActive":True,"arenaCombatPhaseActive":False,"scheduledPhaseTransition":False,
      "casters":{"A":caster_a,"B":caster_b},
      "lumen":{"identityKey":w02["uniqueIdentityKey"],"bodyLowerSouthwestCornerFeet":[20,20,0],"dimensionsFeet":[10,10,10],"hp":400,"alive":True,"confirmedDead":False,"conditions":[],"cargoCustody":{"TEST_ONLY_COPPER_TOKEN_358":"Lumen"},"call":None,"reservationId":None,"returnOutstanding":False,"transportSuppressed":False,"threadShatter":{"expended":False,"firstUse":False,"warningTimestamp":None,"recharge":"ready"},"initiativeActions":[],"movementUsedFeet":0,"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}},
      "target":{"id":"TEST_ONLY_CREATURE_A","hp":80,"ac":15,"conditions":[],"resistances":[],"turnsTowardLumen":False,"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}},
      "blocker":{"id":"TEST_ONLY_RETURN_BLOCKER_A","bodyLowerSouthwestCornerFeet":[10,20,0],"dimensionsFeet":[5,5,5],"groundSpeedFeet":30,"conditions":[],"turnState":{"currentRegularSlotStartMs":None,"scheduledRegularSlotEndMs":None,"roundIndex":None,"action":"ready","bonusAction":"ready","reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}},"counterHistory":[],"pendingCallDeclarations":[],"pendingReadySpellDeclarations":[],"uniqueLumenBodyCount":1}

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
    phase_by_actor={r["actor"]:r["initiativePhaseOffsetMs"] for r in turn_ledger if "slotOffsetMs" in r and r["actor"] in actor_paths}
    initiative_order=[a for a,_ in sorted(phase_by_actor.items(),key=lambda pair:pair[1])]
    actor_order={actor:i for i,actor in enumerate(initiative_order)}
    end_ms=max((e["virtualOffsetMilliseconds"] for e in authored),default=0)
    matched=set()
    scheduled=[]
    regular_rows=[r for r in turn_ledger if "slotOffsetMs" in r and r["actor"] in actor_paths]
    regular_rows.sort(key=lambda r:(r["slotOffsetMs"],actor_order[r["actor"]]))
    starts_by_actor_phase={actor:phase for actor,phase in phase_by_actor.items()}
    row_end={}
    for i,row in enumerate(regular_rows):
        at=row["slotOffsetMs"]
        later=[r["slotOffsetMs"] for r in regular_rows[i+1:] if r["slotOffsetMs"]>at]
        if later:
            next_start=min(later)
        else:
            round_base=(at//6000)*6000
            candidates=[]
            for phase in starts_by_actor_phase.values():
                candidate=round_base+phase
                if candidate<=at: candidate+=6000
                candidates.append(candidate)
            next_start=min(candidates)
        if next_start<=at:
            raise AssertionError((scenario["scenarioId"],row["actor"],at,next_start,"initiative slot overlap"))
        row_end[(row["actor"],at)]=next_start-1
    for row in regular_rows:
        actor=row["actor"]; at=row["slotOffsetMs"]
        matches=[e for e in authored if e["virtualOffsetMilliseconds"]==at and e["subject"]==actor and e["eventId"] not in matched]
        turn_end=row_end[(actor,at)]
        slot={"actor":actor,"offsetMs":at,"roundIndex":row["roundIndex"],"initiativeRank":actor_order[actor],"initiativePhaseOffsetMs":row.get("initiativePhaseOffsetMs"),"firstScheduledSlotOffsetMs":row.get("firstScheduledSlotOffsetMs"),"actionTaken":row.get("actionTaken",row.get("event","pass")),"regularStartOffsetMs":at,"regularEndOffsetMs":turn_end,"endRule":"immediately before the next ordered initiative slot starts; never start+5999 by default","budgetRefresh":{"Action":"ready","BonusAction":"ready","Reaction":"available","movementUsedFeet":0,"companionCommandSpent":False},"counterspellRechargeAtStart":"ready; no use in these windows"}
        if matches:
            event=matches[0]; matched.add(event["eventId"]); event["scheduledTurnStart"]=slot; scheduled.append(event)
        else:
            scheduled.append({"eventId":f"TURN-START-{actor}-{at}","virtualOffsetMilliseconds":at,"subject":actor,"eventType":"regular-turn-start-and-budget-refresh","forwardOperation":slot["actionTaken"],"inverseOperation":"Restore only this actor's exact prior turn budget and active-slot state.","scheduledTurnStart":slot})
        if turn_end<=end_ms:
            scheduled.append({"eventId":f"TURN-END-{actor}-{turn_end}","virtualOffsetMilliseconds":turn_end,"subject":actor,"eventType":"regular-turn-end","forwardOperation":f"Resolve this ordered slot's end processing, then finish the regular turn immediately before the next initiative slot at {turn_end+1}ms; no resource, recharge or extra turn is granted.","inverseOperation":"Remove only this regular-slot end marker.","scheduledTurnEnd":{"actor":actor,"regularStartOffsetMs":at,"regularEndOffsetMs":turn_end,"nextRegularStartOffsetMs":turn_end+1,"roundIndex":row["roundIndex"],"initiativeRank":actor_order[actor]}})
    for event in authored:
        if event["eventId"] not in matched:
            scheduled.append(event)
    def order_key(event: dict) -> tuple:
        at=event["virtualOffsetMilliseconds"]
        if event.get("eventType") is None and event.get("subject")=="Herald call":
            priority=0 # Absolute spell clocks resolve before a regular start at the same offset.
        elif event.get("eventType")=="regular-turn-end":
            priority=1
        elif event.get("scheduledTurnStart"):
            priority=2+actor_order[event["scheduledTurnStart"]["actor"]]
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
            if actor_state.get("counterspell") is not None:
                actor_state["counterspell"]["reactionAvailable"]=True
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
    slot_end_lookup={(r["actor"],r["slotOffsetMs"]):row_end[(r["actor"],r["slotOffsetMs"])] for r in regular_rows}
    for r in turn_ledger:
        row=deepcopy(r)
        if "slotOffsetMs" in row and row.get("actor")!="Herald call clock":
            row.update({"initiativeRank":actor_order[row["actor"]],"regularStartOffsetMs":row["slotOffsetMs"],"regularEndOffsetMs":slot_end_lookup[(row["actor"],row["slotOffsetMs"])],"regularEndOccurredWithinWitness":slot_end_lookup[(row["actor"],row["slotOffsetMs"])]<=end_ms,"budgetRefreshAtStart":{"Action":"ready","BonusAction":"ready","Reaction":"available","movementUsedFeet":0,"companionCommandSpent":False},"counterspellRechargeCheck":"ready; no use in this fixture; no recharge roll due"})
        elif row.get("actor")=="Herald call clock":
            row["orderedBeforeRegularStartsAtSameBoundary"]=True
        calendar_rows.append(row)
    scenario["regularTurnLedger"]={"roundDurationMilliseconds":6000,"roundDurationSeconds":6,"initiativeOrder":initiative_order,"phaseConvention":"TEST_ONLY initiative assigns distinct ordered phase offsets within each six-second round. A regular slot ends after its own turn-end processing immediately before the next ordered participant's regular start; it does not overlap another participant and is not extended to start+5999ms. Equal-time starts, if any are introduced later, use initiativeOrder rank and are serialized end-before-start. Every regular start refreshes that actor's own budget exactly once. Absolute spell clocks resolve before a regular start at the same offset. Idle slots are explicit passes; actors already dead receive no later regular slot.","slots":calendar_rows,"replayEventsIncludeEveryRegularStartAndEndThroughEndpoint":True,"nonOverlappingOrderedSlots":True,"equalTimeRule":"No two actors share a phase in this fixture; any equal-time tie is processed by listed initiativeOrder with the prior slot's end processing before the next slot start."}
    scenario["replay"]={"trackedScope":"Full spell-relevant TEST_ONLY state for both independent caster instances, regular action/reaction/movement budgets, Counterspell eligibility and recharge, one unique Lumen body, reservation/call, HP/conditions, cargo custody, target, blocker, Seal/arena and clock.","hashEncoding":"SHA-256 of UTF-8 JSON with sorted keys, compact separators, ensure_ascii=False.","initialState":initial,"initialStateSHA256":initial_hash,"events":records,"terminalState":terminal,"terminalStateSHA256":terminal_hash,"inverseTraversal":traversal,"inverseTraversalAppliedInExactReverse":True,"inverseFinalState":undo,"inverseFinalStateSHA256":undo_hash,"inverseMatchesInitial":undo_hash==initial_hash,"status":"PASS" if undo_hash==initial_hash else "FAIL"}

def slots(actor: str, end_ms: int, phase_ms: int, actions: dict[int,str], start_ms: int|None=None) -> list[dict]:
    rows=[]; offset=phase_ms
    while offset<=end_ms:
        if start_ms is None or offset>=start_ms: rows.append({"actor":actor,"slotOffsetMs":offset,"roundIndex":offset//6000,"initiativePhaseOffsetMs":phase_ms%6000,"firstScheduledSlotOffsetMs":phase_ms,"actionTaken":actions.get(offset,"pass; no Action, movement, Reaction, recharge roll, or extra resource" )})
        offset+=6000
    return rows

def make_turn_ledger(sid: str) -> list[dict]:
    end_ms={"SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358":60000,"SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358":64000,"SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":12001,"SH332-W04-READY-RELEASE-UNIQUE-ADMISSION-AND-BLOCKED-RETURN-358":75000}[sid]
    rows=[]
    if sid.startswith("SH332-W04"):
        rows+=slots("TEST_ONLY_W17D_CASTER_B",end_ms,0,{0:"Ready Action: cast/pay/hold rank-9 Herald under concentration; trigger is A beginning its later-turn cast"})
        rows+=slots("TEST_ONLY_W17D_CASTER_A",end_ms,1000,{1000:"ordinary Action: declare/pay rank-9 Herald while unique Lumen is still unreserved"})
        rows+=slots("TEST_ONLY_CREATURE_A",end_ms,2000,{})
        rows+=slots("Lumen",end_ms,3000,{3000:"elect consented aid on original regular initiative",69000:"pass while the return anchor remains blocked",75000:"ordinary 30-foot recovery movement to exact anchor"})
        rows+=slots("TEST_ONLY_RETURN_BLOCKER_A",end_ms,4000,{16000:"move 10 feet into the origin box",70000:"move 10 feet out of the origin box"})
        rows.append({"actor":"Herald call clock","slotOffsetMs":60000,"roundIndex":10,"event":"sealed W01 paid Ready preparation+60000ms deadline; resolve expiry/return before B regular turn start at this same offset","orderedBeforeRegularStartsAtSameBoundary":True})
    else:
        rows+=slots("TEST_ONLY_W17D_CASTER_A",end_ms,0,{0:"declare and pay one Herald call"})
        rows+=slots("TEST_ONLY_CREATURE_A",end_ms,2000,{})
        lumen_actions={4000:"elect consented aid on original regular initiative"}
        if sid=="SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358": lumen_actions[64000]="ordinary 30-foot recovery movement to exact anchor"
        rows+=slots("Lumen",end_ms,4000,lumen_actions)
        if sid=="SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":
            rows.append({"actor":"Lumen","scheduledTimeOffsetMs":16000,"roundIndex":2,"event":"no regular turn: confirmed dead at 12000ms before this next scheduled start"})
        if sid!="SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358": rows.append({"actor":"Herald call clock","slotOffsetMs":60000,"roundIndex":10,"event":"original 60000ms deadline; resolve expiry/return before the A regular start at this same offset","orderedBeforeRegularStartsAtSameBoundary":True})
    return sorted(rows,key=lambda r:(r.get("slotOffsetMs",r.get("scheduledTimeOffsetMs",0)),r.get("initiativePhaseOffsetMs",6000),r["actor"]))

def call_state(cid: str,status: str,end: int|None=None,suppressed: bool=False,outcome: str|None=None,start:int=0,deadline:int=60000,caster:str="TEST_ONLY_W17D_CASTER_A") -> dict:
    return {"callId":cid,"status":status,"casterId":caster,"startOffsetMs":start,"deadlineOffsetMs":deadline,"endOffsetMs":end,"returnAnchorFeet":[20,20,0],"destinationFeet":[50,20,0],"transportSuppressed":suppressed,"outcome":outcome}

patches={
"SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358":{
"W03N-01-DECLARE-AND-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W03N-CALL","counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358"),"/counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-NORMAL-RETURN-358")},
"W03N-03-ATOMIC-ADMISSION":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W03N-CALL","active"),"/lumen/reservationId":"W03N-CALL"},
"W03N-04-USEFUL-OWN-TURN-AID":{"/target/hp":52,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":4000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"}]},
"W03N-05-ORIGINAL-DEADLINE":{"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/call":call_state("W03N-CALL","ended-normal",60000,outcome="normal-return"),"/lumen/reservationId":None,"/lumen/returnOutstanding":False,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True}},
"SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358":{
"W03S-01-DECLARE-AND-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W03S-CALL","counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358"),"/counterHistory":w03_counter_review("SH332-W03-PAID-USEFUL-AID-SUPPRESSED-RETURN-BRANCH-358")},
"W03S-02-ARRIVAL":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W03S-CALL","active"),"/lumen/reservationId":"W03S-CALL"},
"W03S-03-USEFUL-AID":{"/target/hp":53,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":4000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"}]},
"W03S-04-TEST-ONLY-SUPPRESSION":{"/lumen/call":call_state("W03S-CALL","active",suppressed=True)},
"W03S-05-EXPIRY-WHILE-SUPPRESSED":{"/lumen/call":call_state("W03S-CALL","ended-blocked",60000,True,"return-transport-suppressed"),"/lumen/reservationId":None,"/lumen/returnOutstanding":True,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True},
"W03S-06-RESTORATION-NO-REVIVAL":{"/lumen/call":call_state("W03S-CALL","ended-blocked",60000,False,"return-transport-suppressed")},
"W03S-07-INDEPENDENT-LEGAL-RECOVERY":{"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/returnOutstanding":False,"/lumen/movementUsedFeet":30,"/lumen/turnState/movementUsedFeet":30,"/lumen/initiativeActions":[{"offsetMs":4000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"},{"offsetMs":64000,"slot":"Lumen-original-regular-turn-11","movementFeet":30}]}},
"SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358":{
"W03D-01-DECLARE-AND-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":0,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W03D-CALL","counterHistory":w03_counter_review("SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358"),"/counterHistory":w03_counter_review("SH332-W03-DEATH-CORPSE-RETURN-TEST-BRANCH-358")},
"W03D-02-ARRIVAL":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W03D-CALL","active"),"/lumen/reservationId":"W03D-CALL"},
"W03D-03-USEFUL-AID":{"/target/hp":54,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":4000,"slot":"Lumen-original-regular-turn-1","action":"Thread Lance"}]},
"W03D-04-TEST-LETHAL-INPUT":{"/lumen/hp":0,"/lumen/alive":False,"/lumen/confirmedDead":True,"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/call":call_state("W03D-CALL","ended-death",12000,outcome="corpse-return"),"/lumen/reservationId":None,"/lumen/returnOutstanding":False,"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True}},
"SH332-W04-READY-RELEASE-UNIQUE-ADMISSION-AND-BLOCKED-RETURN-358":{
"W04-01-CASTER-B-READY-PREPARE":{"/casters/B/rp":38,"/casters/B/turnState/action":"spent","/casters/B/concentrationAvailable":False,"/casters/B/actionHistory":[{"atMs":0,"action":"Ready Action","costRP":26,"paid":True,"preparedSpell":"summon-herald-of-the-planes"}],"/casters/B/castHistory":[{"atMs":0,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"castMode":"Ready preparation","heldUntilRelease":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/B/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/B/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/B/concentrationCallId":"W04-B-HELD-READY-SPELL","/casters/B/readySpell":{"spellId":"summon-herald-of-the-planes","candidateId":"W04-B-CALL","preparedAtMs":0,"releaseTrigger":"TEST_ONLY_W17D_CASTER_A begins the ordinary Herald cast on Lumen while unreserved","expiresAtNextOwnTurnStartMs":6000,"concentrationStartedAtMs":0,"targetSelectedAtRelease":True,"counterspellWindowOccurredAtPreparation":True,"counterspellWindowAtRelease":False,"pending":True},"pendingReadySpellDeclarations":[{"candidateId":"W04-B-CALL","casterId":"TEST_ONLY_W17D_CASTER_B","preparationEligibility":"PASS","targetSelection":"at release","releaseTrigger":"W04-A-CALL cast begins","readyExpiresAtMs":6000}],"/casters/A/counterspell/lastWindow":w04_counter_windows[0],"/casters/A/counterHistory":[w04_counter_windows[0]],"/counterHistory":[w04_counter_windows[0]]},
"W04-02-COUNTERSPELL-A-DECLINES-B-PREPARATION":{"/casters/A/counterspell/lastWindow":w04_counter_windows[0],"/casters/A/counterHistory":[w04_counter_windows[0]],"/counterHistory":[w04_counter_windows[0]]},
"W04-03-CASTER-A-DECLARE-PAY":{"/casters/A/rp":38,"/casters/A/turnState/action":"spent","/casters/A/concentrationAvailable":False,"/casters/A/actionHistory":[{"atMs":1000,"action":"Action","costRP":26,"paid":True}],"/casters/A/castHistory":[{"atMs":1000,"spellId":"summon-herald-of-the-planes","rank":9,"prepared":True,"components":{"V":True,"S":True,"F":True},"firstDistinctPreparedMatrix":True,"baseDissonanceApplied":0}],"/casters/A/preparedMatrixFamilyHistory":["summon-herald-of-the-planes"],"/casters/A/rank9FamilyHistory":["summon-herald-of-the-planes"],"/casters/A/concentrationCallId":"W04-A-CALL","pendingCallDeclarations":[{"candidateId":"W04-A-CALL","casterId":"TEST_ONLY_W17D_CASTER_A","initialEligibility":"PASS_WHILE_UNRESERVED","resolution":"pending ordinary cast"}],"/casters/B/counterspell/lastWindow":w04_counter_windows[1],"/casters/B/counterHistory":[w04_counter_windows[1]],"/counterHistory":[w04_counter_windows[0],w04_counter_windows[1]]},
"W04-04-COUNTERSPELL-B-DECLINES-A-CAST":{"/casters/B/counterspell/lastWindow":w04_counter_windows[1],"/casters/B/counterHistory":[w04_counter_windows[1]],"/counterHistory":[w04_counter_windows[0],w04_counter_windows[1]]},
"W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN":{"/lumen/bodyLowerSouthwestCornerFeet":[50,20,0],"/lumen/call":call_state("W04-B-CALL","active",start=1000,deadline=60000,caster="TEST_ONLY_W17D_CASTER_B"),"/lumen/reservationId":"W04-B-CALL","pendingCallDeclarations":[{"candidateId":"W04-A-CALL","casterId":"TEST_ONLY_W17D_CASTER_A","initialEligibility":"PASS_WHILE_UNRESERVED","resolution":"pending ordinary cast"}],"pendingReadySpellDeclarations":[],"/casters/B/concentrationCallId":"W04-B-CALL","/casters/B/concentrationAvailable":False,"/casters/B/readySpell":None,"/casters/B/lastResolution":"readied Herald released successfully at 1000ms; 26 RP was paid at preparation; Reaction spent once" ,"/casters/B/turnState/reaction":"spent","/casters/B/counterspell/reactionAvailable":False},
"W04-06-CASTER-A-FINAL-ADMISSION-FAILS":{"/casters/A/concentrationCallId":None,"/casters/A/concentrationAvailable":True,"/casters/A/lastResolution":"paid-failure:unique-Lumen-reservation-already-held; ordinary Action and 26RP remain spent","pendingCallDeclarations":[]},
"W04-07-USEFUL-AID-ORIGINAL-TURN":{"/target/hp":57,"/lumen/turnState/action":"spent","/lumen/initiativeActions":[{"offsetMs":3000,"slot":"Lumen-original-regular-turn-1","action":"Thread Bind"}]},
"W04-08-RETURN-BLOCKER-ENTERS":{"/blocker/bodyLowerSouthwestCornerFeet":[20,20,0],"/blocker/turnState/movementUsedFeet":10},
"W04-09-DEADLINE-BLOCKED-RETURN":{"/lumen/call":call_state("W04-B-CALL","ended-blocked",60000,outcome="occupied-volume-overlap-at-return-anchor",start=1000,deadline=60000,caster="TEST_ONLY_W17D_CASTER_B"),"/lumen/reservationId":None,"/lumen/returnOutstanding":True,"/casters/B/concentrationCallId":None,"/casters/B/concentrationAvailable":True},
"W04-10-BLOCKER-CLEARS":{"/blocker/bodyLowerSouthwestCornerFeet":[10,20,0],"/blocker/turnState/movementUsedFeet":10},
"W04-11-INDEPENDENT-LUMEN-RECOVERY":{"/lumen/bodyLowerSouthwestCornerFeet":[20,20,0],"/lumen/returnOutstanding":False,"/lumen/movementUsedFeet":30,"/lumen/turnState/movementUsedFeet":30,"/lumen/initiativeActions":[{"offsetMs":3000,"slot":"Lumen-original-regular-turn-1","action":"Thread Bind"},{"offsetMs":75000,"slot":"Lumen-original-regular-turn-13","movementFeet":30}]}}
}
for scenario in w03["witnesses"]+[w04_main]:
    sid=scenario["scenarioId"]
    attach_replay(scenario,tracked_baseline(sid.startswith("SH332-W04")),patches[sid],make_turn_ledger(sid))
w02["logicalClock"]["regularTurnCalendars"]={
    "W03":{s["scenarioId"]:deepcopy(s["regularTurnLedger"]) for s in w03["witnesses"]},
    "W04":{w04_main["scenarioId"]:deepcopy(w04_main["regularTurnLedger"])}
}
w02["logicalClock"]["calendarBinding"]="Every participant's start, one-time budget refresh, ordered non-overlapping slot end, exact six-second initiative phase, and spell-clock boundary is bound to replay events. W04 B prepares the spell on phase 0, A acts on phase 1000, then B releases by Reaction. The target is a stationary TEST_ONLY Construct. Death ends the call at 12000ms; absolute deadlines precede regular starts when offsets coincide."
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
def calendar_pass(s):
    ledger=s["regularTurnLedger"]
    slots=[r for r in ledger["slots"] if "slotOffsetMs" in r and r["actor"]!="Herald call clock"]
    starts=[e for e in s["forwardEvents"] if e.get("scheduledTurnStart")]
    ends=[e for e in s["forwardEvents"] if e.get("scheduledTurnEnd")]
    endpoint=max(e["virtualOffsetMilliseconds"] for e in s["forwardEvents"])
    ordered=sorted(slots,key=lambda r:(r["slotOffsetMs"],r["initiativeRank"]))
    no_overlap=all(a["regularEndOffsetMs"]<b["regularStartOffsetMs"] and a["regularEndOffsetMs"]+1==b["regularStartOffsetMs"] for a,b in zip(ordered,ordered[1:]))
    unique_phases=len({r["initiativePhaseOffsetMs"] for r in slots})==len({r["actor"] for r in slots})
    expected_ends=sum(1 for r in slots if r["regularEndOffsetMs"]<=endpoint)
    refresh_once=all(e["scheduledTurnStart"]["budgetRefresh"]=={"Action":"ready","BonusAction":"ready","Reaction":"available","movementUsedFeet":0,"companionCommandSpent":False} for e in starts)
    return ledger["roundDurationMilliseconds"]==6000 and ledger["nonOverlappingOrderedSlots"] and unique_phases and no_overlap and refresh_once and len(starts)==len(slots) and len(ends)==expected_ends and all(r["slotOffsetMs"]%6000==r["initiativePhaseOffsetMs"] for r in slots)
check("ORDERED_NONOVERLAPPING_SIX_SECOND_TURN_CALENDAR", all(calendar_pass(s) for s in scenario_list), "All W03/W04 starts follow distinct ordered initiative phases; each slot ends immediately before the next, each refresh occurs once, and every end through the witness endpoint is replayed.")
ready_events={e["eventId"]:e for e in w04_main["replay"]["events"]}
ready_events={e["eventId"]:e for e in w04_main["replay"]["events"]}
ready_ok=(w04_main["scenarioId"]=="SH332-W04-READY-RELEASE-UNIQUE-ADMISSION-AND-BLOCKED-RETURN-358" and READY_SOURCE_BINDING["sourceLines"]==[97,111] and "Spell-effect duration begins at release" in READY_SOURCE_BINDING["sourceExcerpt"] and "W01 fixes its temporary-call deadline at paid declaration/preparation+60000ms" in READY_SOURCE_BINDING["rulesApplied"]["targetAndClock"] and ready_events["W04-01-CASTER-B-READY-PREPARE"]["stateAfter"]["casters"]["B"]["turnState"]["action"]=="spent" and ready_events["W04-01-CASTER-B-READY-PREPARE"]["stateAfter"]["casters"]["B"]["concentrationAvailable"] is False and ready_events["W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN"]["stateAfter"]["casters"]["B"]["turnState"]["reaction"]=="spent" and ready_events["W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN"]["stateAfter"]["lumen"]["call"]["startOffsetMs"]==1000 and ready_events["W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN"]["stateAfter"]["lumen"]["call"]["deadlineOffsetMs"]==60000 and ready_events["W04-09-DEADLINE-BLOCKED-RETURN"]["virtualOffsetMilliseconds"]==60000 and ready_events["W04-09-DEADLINE-BLOCKED-RETURN"]["stateAfter"]["lumen"]["call"]["endOffsetMs"]==60000 and w04_paid[0]["effectDurationRemainingMsAtRelease"]==59000 and ready_events["W04-06-CASTER-A-FINAL-ADMISSION-FAILS"]["stateAfter"]["lumen"]["reservationId"]=="W04-B-CALL" and ready_events["W04-06-CASTER-A-FINAL-ADMISSION-FAILS"]["stateAfter"]["casters"]["A"]["rp"]==38)
check("SOURCE_LEGAL_READY_COMPETING_CALL", ready_ok, "B pays and casts at Ready preparation, holds concentration, declines Counterspell at the later cast trigger, spends one Reaction to release before later events, manifests the call at release while preserving the sealed W01 preparation+60000ms deadline (59000ms remaining), and wins the unique reservation before A resolves.")
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

revision={"id":"SH332-W02-W03-W04-REPACK04-CORRECTION-358","status":"READY_FOR_DIRECTOR_RECHECK","supersedesArchive":"DD_Rank9_SummonHerald_SH332_W02_W03_W04_TESTONLY_358_Repack03.zip","supersededArchiveSHA256":"b83f58298089f180431b193abf08de052e30c7ba0dc08f8944369aa15ecb4937","directorResidualsAddressed":["SH358-R4: distinct synthetic initiative phases, non-overlapping turn end before next ordered start, one budget refresh per start, equal-time precedence, regenerated states/patches/hashes and mirrored W02 calendars","SH358-R5: B's source-bound Ready preparation and paid cast on its earlier turn, held concentration and trigger; A's later ordinary Action; B's single Reaction release before later events; target and effect manifest at release while preserving sealed W01 paid-preparation+60000ms deadline; A's final admission fails after B's reservation"],"sourceBinding":READY_SOURCE_BINDING,"unchangedBoundaries":["W01 approval and clean Repack01 hash are unchanged","owner-authorized W02 state remains explicitly TEST_ONLY and limited to W03/W04","no campaign event, actual consent, runtime procedure, canonical publication, unrelated identity or application is asserted"],"builderValidationStatus":validation["status"],"independentValidation":"pending builder execution","identityDisposition":{"decision":"HOLD_PENDING_DIRECTOR_R4_R5_RECHECK","acceptedIds":[],"appliedIds":[],"applicationAuthorized":False}}
dump("09_SH332_W02_W03_W04_REPACK04_CORRECTION_358.json",revision)

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
    "08_READY_ACTION_RULE_BINDING_358.json",
    "09_SH332_W02_W03_W04_REPACK04_CORRECTION_358.json",
    "verify_herald_w02_witness_358.py",
]
if not (OUT/"OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").exists():
    (OUT/"OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").write_bytes(AUTH_PATH.read_bytes())
manifest={"id":"SH332-W02-W03-W04-TESTONLY-358-REPACK04-MANIFEST","classification":"test-only witness delivery manifest","memberCountExcludingSelf":len(members),"members":[{"path":n,"bytes":(OUT/n).stat().st_size,"sha256":sha(OUT/n)} for n in members],"selfExcluded":True}
dump("MEMBER_MANIFEST.json",manifest)
zip_path=OUT/"DD_Rank9_SummonHerald_SH332_W02_W03_W04_TESTONLY_358_Repack04.zip"
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
delivery={"id":"SH332-W02-W03-W04-TESTONLY-358-REPACK04-DELIVERY","archive":zip_path.name,"archiveBytes":zip_path.stat().st_size,"archiveSHA256":sha(zip_path),"manifestPath":str((OUT/'MEMBER_MANIFEST.json').relative_to(ROOT)).replace('\\','/'),"manifestSHA256":sha(OUT/'MEMBER_MANIFEST.json'),"memberCount":len(members),"status":"READY_FOR_DIRECTOR_REVIEW_NOT_IDENTITY_ACCEPTANCE","buildValidationStatus":validation["status"],"independentReplayValidationStatus":independent["status"],"identityDisposition":{"decision":"HOLD_PENDING_DIRECTOR_R4_R5_RECHECK","acceptedIds":[],"appliedIds":[],"blockerIds":["SH202-B02"],"applicationAuthorized":False}}
dump("DELIVERY.json",delivery)
print(json.dumps({"output":str(OUT),"validation":validation["status"],"archive":str(zip_path),"archiveBytes":zip_path.stat().st_size,"archiveSHA256":sha(zip_path),"checks":len(checks)},indent=2))
