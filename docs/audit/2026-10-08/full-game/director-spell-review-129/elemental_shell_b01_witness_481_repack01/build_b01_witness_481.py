from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ROOT = REVIEW.parents[4]
PROPOSAL_DIR = REVIEW / "elemental_shell_b01_test_source_proposal_478_repack01"
PROPOSAL_PATH = PROPOSAL_DIR / "OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_REPACK01_TESTONLY.json"
READBACK_PATH = PROPOSAL_DIR / "DIRECTOR_READBACK_478_REPACK01.json"
ADOPTION_PATH = PROPOSAL_DIR / "OWNER_DF218_B01_ADOPTION_478_REPACK01_TESTONLY.json"
PREP_DIR = REVIEW / "elemental_shell_caster_premise_proposal_468"
QUAL_DIR = REVIEW / "elemental_shell_caster_qualification_472_repack01"
QUEUE_PATH = REVIEW / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
DIRECTOR_HOLD_PATH = HERE / "DIRECTOR_READBACK_480_HOLD.json"
ADOPTION_ERRATUM_PATH = HERE / "OWNER_DF218_B01_ADOPTION_478_CASTER_BINDING_ERRATUM_481_TESTONLY.json"
PRIOR_WITNESS_PATH = HERE.parent / "elemental_shell_b01_witness_480_repack01" / "DF218_B01_WITNESS_480_TESTONLY.json"
PRIOR_TRACE_PATH = HERE.parent / "elemental_shell_b01_witness_480_repack01" / "B01_EVENT_TRACE_480.json"
EXPECTED_PROPOSAL_SHA = "e00c3c8fad96883b6fe1d7ac07e1ed07f4b2f7b2f275dcee1853ce30b576ea69"
OWNER_REPLY = "Adopt exact B01 Proposal478 Repack01 (Recommended)"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha(path.read_bytes())


def sha_obj(value) -> str:
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def diff(before, after, path=""):
    if isinstance(before, dict) and isinstance(after, dict):
        ops = []
        for key in sorted(set(before) | set(after)):
            child = path + "/" + pointer_escape(key)
            if key not in before:
                ops.append({"op": "replace", "path": child, "beforeExists": False, "afterExists": True, "after": copy.deepcopy(after[key])})
            elif key not in after:
                ops.append({"op": "replace", "path": child, "beforeExists": True, "before": copy.deepcopy(before[key]), "afterExists": False})
            else:
                ops.extend(diff(before[key], after[key], child))
        return ops
    if before != after:
        return [{"op": "replace", "path": path, "beforeExists": True, "before": copy.deepcopy(before), "afterExists": True, "after": copy.deepcopy(after)}]
    return []


def apply_ops(state, operations):
    result = copy.deepcopy(state)
    for op in operations:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in op["path"].split("/")[1:]]
        target = result
        for part in parts[:-1]:
            target = target[int(part)] if isinstance(target, list) else target[part]
        leaf = parts[-1]
        if isinstance(target, list):
            index = int(leaf)
            if op["afterExists"]:
                target[index] = copy.deepcopy(op["after"])
            else:
                target.pop(index)
        elif op["afterExists"]:
            target[leaf] = copy.deepcopy(op["after"])
        else:
            target.pop(leaf)
    return result


def inverse_ops(operations):
    return [
        {
            "op": "replace",
            "path": op["path"],
            "beforeExists": op["afterExists"],
            **({"before": copy.deepcopy(op["after"])} if op["afterExists"] else {}),
            "afterExists": op["beforeExists"],
            **({"after": copy.deepcopy(op["before"])} if op["beforeExists"] else {}),
        }
        for op in reversed(operations)
    ]


proposal_bytes = PROPOSAL_PATH.read_bytes()
proposal_sha = sha(proposal_bytes)
assert proposal_sha == EXPECTED_PROPOSAL_SHA, (proposal_sha, EXPECTED_PROPOSAL_SHA)
proposal = json.loads(proposal_bytes)
readback = read_json(READBACK_PATH)
assert readback["status"] == "READY_FOR_OWNER_ADOPTION"
assert readback["reviewedProposal"]["sha256"] == EXPECTED_PROPOSAL_SHA
queue = read_json(QUEUE_PATH)
assert (queue["currentAuthority"]["reviewedApplied"], queue["currentAuthority"]["pending"], queue["currentAuthority"]["acceptedUnapplied"]) == (831, 17, 0)
assert queue["nextIdentity"] == "elemental-shell"

for source in proposal["sourceBindings"]:
    path = ROOT / source["path"]
    assert path.is_file(), source["path"]
    if source.get("workingTreeSha256"):
        assert sha_file(path) == source["workingTreeSha256"], source["path"]
    raw_blob = subprocess.check_output(["git", "cat-file", "blob", source["gitBlobSha1"]], cwd=ROOT)
    assert sha(raw_blob) == source["sha256"], source["path"]

prep_path = PREP_DIR / "CASTER_PREPARATION_PREMISE_468_TESTONLY.json"
prep_proposal_path = PREP_DIR / "OWNER_DF218_SHELL_CASTER_PREMISE_PROPOSAL_468_TESTONLY.json"
prep_adoption_path = PREP_DIR / "OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json"
qualification_path = QUAL_DIR / "SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json"
qualification_readback_path = QUAL_DIR / "DIRECTOR_READBACK_472_REPACK01.json"
qualification = read_json(qualification_path)
qualification_readback = read_json(qualification_readback_path)
assert sha_file(prep_proposal_path) == proposal["ownerProposedInputs"]["casterQualificationReuse"]["proposal468Sha256"]
assert sha_file(prep_path) == qualification["adoptedPremise"]["sha256"]
assert qualification["status"].startswith("DIRECTOR_PASS_TESTONLY_CASTER")
assert qualification_readback["decision"].startswith("PASS_TEST_ONLY_CASTER")

adoption = read_json(ADOPTION_PATH)
assert sha_file(ADOPTION_PATH) == "23b99a464927dcd62d60dcb17b5f6f25a2244eafe3e6601f423b38b3405e8144"
assert adoption["ownerAuthorization"]["verbatim"] == OWNER_REPLY
assert adoption["scope"]["proposalSha256"] == EXPECTED_PROPOSAL_SHA
assert adoption["supportingCasterQualification"]["proposal468Sha256"] == "de4bd28b11d33be17a9185f925fae4c740956a10f7aaf5d89bcddc16a7bb8169"
erratum = read_json(ADOPTION_ERRATUM_PATH)
assert erratum["originalAdoption"]["sha256"] == sha_file(ADOPTION_PATH)
assert erratum["correctedBinding"]["proposalPath"] == str((PREP_DIR / "OWNER_DF218_SHELL_CASTER_PREMISE_PROPOSAL_468_TESTONLY.json").relative_to(ROOT)).replace("\\", "/")
assert erratum["correctedBinding"]["proposalSha256"] == adoption["supportingCasterQualification"]["proposal468Sha256"]
assert read_json(DIRECTOR_HOLD_PATH)["decision"] == "HOLD"

inputs = proposal["ownerProposedInputs"]
actor_src = inputs["actor"]
scene_src = inputs["scene"]
source_src = inputs["sourceContract"]
cast_src = inputs["shellCast"]
geometry = read_json(PROPOSAL_DIR / "SOURCE_GEOMETRY_PREFLIGHT_478_REPACK01.json")

def initial_state():
    return {
        "schemaVersion": 1,
        "branchId": proposal["scope"]["branchId"],
        "classification": "HYPOTHETICAL_TEST_ONLY_BRANCH_STATE",
        "campaignEvent": False,
        "timeSeconds": 0.0,
        "phase": "BEFORE_ORDER_ZERO_START",
        "scene": {
            "id": scene_src["id"],
            "coordinateConvention": scene_src["coordinateConvention"],
            "clock": copy.deepcopy(scene_src["clock"]),
            "groundSupport": copy.deepcopy(scene_src["groundSupport"]),
            "otherBodiesOrObstacles": copy.deepcopy(scene_src["otherBodiesOrObstacles"]),
        },
        "casterQualification": {
            "actorId": actor_src["id"],
            "classLevel": "Wizard18",
            "ordinaryPreparedCount": 24,
            "elementalShellOrdinaryPosition": True,
            "divinationOnlyPosition": "UNASSIGNED",
            "proposal468Sha256": proposal["ownerProposedInputs"]["casterQualificationReuse"]["proposal468Sha256"],
            "qualification472Status": qualification["status"],
            "noCampaignHistoryClaimed": True,
        },
        "actor": {
            "id": actor_src["id"],
            "identity": actor_src["identity"],
            "class": actor_src["class"],
            "classLevel": actor_src["classLevel"],
            "path": actor_src["path"],
            "stats": copy.deepcopy(actor_src["stats"]),
            "proficiencyBonus": actor_src["proficiencyBonus"],
            "spellAttack": actor_src["spellAttack"],
            "spellDC": actor_src["spellDC"],
            "bodySizeFeet": copy.deepcopy(actor_src["bodySizeFeet"]),
            "bodyBoundsFeet": copy.deepcopy(actor_src["bodyBoundsFeet"]),
            "positionFeet": copy.deepcopy(scene_src["bearerPositionFeet"]),
            "plane": "DF218-B01-SCENE-R1",
            "vitals": copy.deepcopy(actor_src["currentFixtureVitals"]),
            "alive": actor_src["currentStateAndConsent"]["alive"],
            "voice": actor_src["currentStateAndConsent"]["voice"],
            "consentsToSelfShell": actor_src["currentStateAndConsent"]["consentsToSelfShell"],
            "hands": {
                "left": inputs["equipmentAndHands"]["leftHand"],
                "right": inputs["equipmentAndHands"]["rightHand"],
                "verbalComponent": inputs["equipmentAndHands"]["verbalComponent"],
            },
            "focus": copy.deepcopy(inputs["equipmentAndHands"]["focus"]),
            "turn": {
                "status": "NOT_STARTED",
                "actionAvailable": False,
                "bonusActionAvailable": False,
                "reactionAvailable": False,
                "movementAvailableFeet": 0,
                "startSeconds": None,
                "endSeconds": None,
                "magicThisTurn": False,
            },
            "preparedFamiliesUsed": [],
            "lastSpell": None,
            "pendingCast": None,
            "castHistory": [],
            "resourceHistory": [],
            "activeEffects": [],
            "damageLedger": [],
            "reflectionLedger": [],
        },
        "environment": {
            "source": {
                "id": source_src["id"],
                "kind": source_src["kind"],
                "actorId": source_src["actorId"],
                "controllerId": source_src["controllerId"],
                "responsibleCreatureDealer": source_src["responsibleCreatureDealer"],
                "damageClassification": source_src["damageClassification"],
                "boundsFeet": copy.deepcopy(source_src["event"]["exposureVolumeFeet"]),
                "sourceVolumeIsNonSolidAndDoesNotObstruct": source_src["sourceVolumeIsNonSolidAndDoesNotObstruct"],
                "oneShotOnly": source_src["oneShotOnly"],
                "eventPending": True,
                "eventEmittedCount": 0,
            },
            "geometryAudit": copy.deepcopy(geometry),
        },
        "createdReflectionRoots": [],
        "emittedReflectedPackets": [],
    }


states = [initial_state()]
events = []

def transition(event_id, time, kind, detail, mutate):
    before_state_id = f"S{len(states)-1:03d}"
    after_state_id = f"S{len(states):03d}"
    before = copy.deepcopy(states[-1])
    after = copy.deepcopy(before)
    mutate(after)
    after["timeSeconds"] = time
    after["phase"] = kind
    forward = diff(before, after)
    inverse = inverse_ops(forward)
    assert apply_ops(before, forward) == after
    assert apply_ops(after, inverse) == before
    before_hash, after_hash = sha_obj(before), sha_obj(after)
    states.append(after)
    events.append({
        "eventId": event_id,
        "timeSeconds": time,
        "kind": kind,
        "detail": detail,
        "beforeStateId": before_state_id,
        "afterStateId": after_state_id,
        "beforeStateSha256": before_hash,
        "afterStateSha256": after_hash,
        "forwardOperations": forward,
        "inverseOperations": inverse,
    })


def start_and_begin(s):
    a = s["actor"]
    a["turn"].update({"status": "ACTIVE", "actionAvailable": True, "bonusActionAvailable": True, "reactionAvailable": True, "movementAvailableFeet": 30, "startSeconds": 0.0, "magicThisTurn": False})
    a["pendingCast"] = {"spellId": cast_src["spellId"], "castId": cast_src["castHistoryId"], "caster": a["id"], "target": a["id"], "startedAt": 0.0, "status": "CASTING_NOT_YET_COMMITTED", "components": copy.deepcopy(cast_src["components"]), "selectedElement": cast_src["selectedElement"]}


def commit_cast(s):
    a = s["actor"]
    assert a["vitals"]["RP"] == cast_src["preCastRP"]
    a["vitals"]["RP"] = cast_src["postCastRP"]
    a["turn"]["actionAvailable"] = False
    a["turn"]["magicThisTurn"] = True
    a["preparedFamiliesUsed"].append(cast_src["spellId"])
    a["vitals"]["preparedRankedCastFamiliesUsed"].append(cast_src["spellId"])
    a["lastSpell"] = cast_src["spellId"]
    a["pendingCast"].update({"status": "COMMITTED_AWAITING_RESOLUTION", "committedAt": cast_src["commitSeconds"], "paidBeforeResolution": True, "rpCost": cast_src["rpCost"]})
    a["castHistory"].append({"castId": cast_src["castHistoryId"], "spellId": cast_src["spellId"], "rank": 9, "committedAt": cast_src["commitSeconds"], "costRP": cast_src["rpCost"], "preCastRP": cast_src["preCastRP"], "postCastRP": cast_src["postCastRP"], "firstDistinctPreparedFamily": True, "baseDissonance": cast_src["firstDistinctPreparedFamilyBaseDissonance"], "dissonanceAfter": cast_src["postCastDissonance"], "refrain": cast_src["refrain"], "target": a["id"], "components": copy.deepcopy(cast_src["components"])})
    a["resourceHistory"].append({"eventId": cast_src["castHistoryId"], "resource": "RP", "delta": -cast_src["rpCost"], "poolAfter": cast_src["postCastRP"], "discount": False})


def manifest(s):
    a = s["actor"]
    a["pendingCast"] = None
    a["activeEffects"].append({"effectId": "DF218-SHELL-B01-TESTONLY-R1:SHELL-1", "spellId": cast_src["spellId"], "bearer": a["id"], "selectedElement": cast_src["selectedElement"], "manifestedAt": cast_src["manifestationSeconds"], "deadlineSeconds": cast_src["deadlineSeconds"], "active": True, "preventsIncomingFire": True, "preventsDamage": True, "reflectionRequiresResponsibleCreatureDealer": True})


def end_turn(s):
    a = s["actor"]
    a["turn"].update({"status": "ENDED", "actionAvailable": False, "bonusActionAvailable": False, "movementAvailableFeet": 0, "endSeconds": 0.9})


def fire_event(s):
    a = s["actor"]
    source = s["environment"]["source"]
    ev = source_src["event"]
    assert a["activeEffects"][0]["active"] and ev["timeSeconds"] < cast_src["deadlineSeconds"]
    source["eventPending"] = False
    source["eventEmittedCount"] = 1
    a["damageLedger"].append({"eventId": ev["id"], "timeSeconds": ev["timeSeconds"], "sourceId": source_src["id"], "sourceActorId": ev["responsibleCreatureDealer"], "responsibleCreatureDealer": ev["responsibleCreatureDealer"], "damageType": ev["damageType"], "rawAmount": ev["rawAmount"], "mitigatedBeforeShell": 0, "shellPrevents": ev["rawAmount"], "hpDamage": 0, "hpBefore": 110, "hpAfter": 110})
    a["reflectionLedger"].append({"eventId": ev["id"], "reflectionBasisBeforeShellImmunity": ev["rawAmount"], "recipient": None, "reflectedPacketEmitted": False, "nominalOrBankedReflectionRootCreated": False, "reason": "The adopted noncreature test source has no responsible creature dealer; retained Q14 provides no environmental recipient."})


transition("B01-E001", 0.0, "REGULAR_START_AND_CAST_BEGIN", "Order-zero START refreshes ordinary budgets; the legal self-targeted Shell cast begins without spending before commitment.", start_and_begin)
transition("B01-E002", 0.1, "PAID_CAST_COMMIT", "Commit Action, components, cast history and 26 RP before resolution; RP 68→42.", commit_cast)
transition("B01-E003", 0.2, "NO_COUNTERSPELL_RESPONDER", "No other actor or eligible responder is present; the response window advances without reaction, expenditure, roll or interruption.", lambda s: None)
transition("B01-E004", 0.3, "SHELL_MANIFESTATION", "Shell manifests on the consenting self; fire immunity is active through deadline 60.3.", manifest)
transition("B01-E005", 0.9, "REGULAR_END", "Regular END clears the active-turn flag; committed costs and spell history remain.", end_turn)
transition("B01-E006", 1.1, "NONCREATURE_FIRE_EVENT", "One scheduled ordinary non-Null 7-fire pulse is prevented; no HP loss and no reflection recipient/root/packet.", fire_event)

initial, final = states[0], states[-1]
undo = copy.deepcopy(final)
for event in reversed(events):
    undo = apply_ops(undo, event["inverseOperations"])
assert undo == initial
assert final["actor"]["vitals"]["RP"] == 42
assert final["actor"]["vitals"]["HP"] == 110
assert final["actor"]["damageLedger"][-1]["shellPrevents"] == 7
assert final["actor"]["reflectionLedger"][-1]["recipient"] is None
assert final["emittedReflectedPackets"] == [] and final["createdReflectionRoots"] == []

source_bindings = []
for binding in proposal["sourceBindings"]:
    source_bindings.append({"path": binding["path"], "role": binding["role"], "sha256": binding["sha256"], "gitBlobSha1": binding["gitBlobSha1"], "byteDomain": binding["byteDomain"], "workingTreeSha256": binding.get("workingTreeSha256"), "workingTreeRepresentation": binding.get("workingTreeRepresentation"), "pointers": binding.get("pointers", [])})
source_bindings.extend([
    {"path": str(PROPOSAL_PATH.relative_to(ROOT)).replace("\\", "/"), "role": "exact owner-adopted B01 test-source proposal", "sha256": EXPECTED_PROPOSAL_SHA, "gitBlobSha1": blob(PROPOSAL_PATH)},
    {"path": str(READBACK_PATH.relative_to(ROOT)).replace("\\", "/"), "role": "Director readiness receipt", "sha256": sha_file(READBACK_PATH), "gitBlobSha1": blob(READBACK_PATH)},
    {"path": str(ADOPTION_PATH.relative_to(ROOT)).replace("\\", "/"), "role": "exact B01 owner adoption", "sha256": sha_file(ADOPTION_PATH), "gitBlobSha1": blob(ADOPTION_PATH)},
    {"path": str(prep_path.relative_to(ROOT)).replace("\\", "/"), "role": "Proposal468 caster preparation premise", "sha256": sha_file(prep_path), "gitBlobSha1": blob(prep_path)},
    {"path": str(prep_proposal_path.relative_to(ROOT)).replace("\\", "/"), "role": "Proposal468 exact adopted caster preparation proposal", "sha256": sha_file(prep_proposal_path), "gitBlobSha1": blob(prep_proposal_path)},
    {"path": str(prep_adoption_path.relative_to(ROOT)).replace("\\", "/"), "role": "Proposal468 exact owner adoption", "sha256": sha_file(prep_adoption_path), "gitBlobSha1": blob(prep_adoption_path)},
    {"path": str(qualification_path.relative_to(ROOT)).replace("\\", "/"), "role": "Director-passed caster qualification subpart", "sha256": sha_file(qualification_path), "gitBlobSha1": blob(qualification_path)},
    {"path": str(qualification_readback_path.relative_to(ROOT)).replace("\\", "/"), "role": "Director pass for caster qualification only", "sha256": sha_file(qualification_readback_path), "gitBlobSha1": blob(qualification_readback_path)},
])

for path, role in [
    (DIRECTOR_HOLD_PATH, "GPT Director hold and exact four-correction receipt for witness480"),
    (ADOPTION_ERRATUM_PATH, "narrow adoption metadata binding erratum; original adoption remains byte-identical"),
    (PRIOR_WITNESS_PATH, "preserved predecessor witness480 reviewed by the Director"),
    (PRIOR_TRACE_PATH, "preserved predecessor event trace480 reviewed by the Director"),
]:
    source_bindings.append({
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "role": role,
        "sha256": sha_file(path),
        "gitBlobSha1": blob(path),
        "byteDomain": "exact committed Git blob",
        "workingTreeSha256": sha_file(path),
        "workingTreeRepresentation": "LF identical",
        "pointers": [],
    })

snapshots = [{"stateId": f"S{i:03d}", "timeSeconds": state["timeSeconds"], "phase": state["phase"], "stateSha256": sha_obj(state), "completeState": state} for i, state in enumerate(states)]
witness = {
    "schemaVersion": 1,
    "id": "DF218-B01-WITNESS-481-REPACK01",
    "classification": "ADOPTED_HYPOTHETICAL_TEST_ONLY_REVERSIBLE_WITNESS",
    "status": "CONSTRUCTED_FOR_DIRECTOR_REVIEW_NOT_SEALED",
    "branchId": proposal["scope"]["branchId"],
    "component": "DF218-B01",
    "hypotheticalOnly": True,
    "noCampaignEventClaim": True,
    "adoption": {"path": str(ADOPTION_PATH.relative_to(ROOT)).replace("\\", "/"), "sha256": sha_file(ADOPTION_PATH), "proposalSha256": EXPECTED_PROPOSAL_SHA, "directorReadinessPath": str(READBACK_PATH.relative_to(ROOT)).replace("\\", "/"), "ownerAuthorization": OWNER_REPLY, "casterBindingErratumPath": str(ADOPTION_ERRATUM_PATH.relative_to(ROOT)).replace("\\", "/"), "casterBindingErratumSha256": sha_file(ADOPTION_ERRATUM_PATH)},
    "correctedFrom": {"witnessPath": str(PRIOR_WITNESS_PATH.relative_to(ROOT)).replace("\\", "/"), "witnessSha256": sha_file(PRIOR_WITNESS_PATH), "directorHoldPath": str(DIRECTOR_HOLD_PATH.relative_to(ROOT)).replace("\\", "/"), "directorHoldSha256": sha_file(DIRECTOR_HOLD_PATH)},
    "sourceBindings": source_bindings,
    "adoptedScenario": {
        "startingState": initial,
        "casterPreparation": copy.deepcopy(states[0]["casterQualification"]),
        "actorAndConsent": copy.deepcopy(inputs["actor"]),
        "equipmentAndHands": copy.deepcopy(inputs["equipmentAndHands"]),
        "geometry": copy.deepcopy(geometry),
        "environmentalSource": copy.deepcopy(source_src),
        "shellCast": copy.deepcopy(cast_src),
        "orderedSchedule": copy.deepcopy(inputs["proposedOrderedSchedule"]),
        "expectedSettlement": copy.deepcopy(inputs["expectedSettlementIfThesePremisesAreAdopted"]),
    },
    "stateTransitionReplay": {
        "classification": "TEST_ONLY_REVERSIBLE_BRANCH_STATE_RECONSTRUCTION",
        "initialStateId": "S000",
        "finalStateId": f"S{len(states)-1:03d}",
        "initialStateSha256": sha_obj(initial),
        "finalStateSha256": sha_obj(final),
        "stateSnapshots": snapshots,
        "eventTransitions": events,
        "completeForwardOperations": [op for event in events for op in event["forwardOperations"]],
        "completeInverseOperations": [op for event in reversed(events) for op in event["inverseOperations"]],
        "inverseReplayResult": {"restoresExactInitialState": undo == initial, "restoredStateSha256": sha_obj(undo), "expectedInitialStateSha256": sha_obj(initial)},
    },
    "terminalStateSummary": {
        "actorId": actor_src["id"], "HPBefore": 110, "HPAfter": 110, "RPBefore": 68, "RPAfter": 42,
        "Dissonance": 0, "Refrain": 0, "selectedElement": "fire", "shellDeadlineSeconds": 60.3,
        "incomingRawFire": 7, "otherEligiblePreShellMitigation": 0, "preventedByShell": 7,
        "hpDamage": 0, "reflectionBasisBeforeShellImmunity": 7, "reflectionRecipient": None,
        "reflectedPacketEmitted": False, "nominalOrBankedReflectionRootCreated": False,
        "environmentEventEmittedCount": 1, "actorOrCreatureDealer": None,
    },
    "decisionBoundary": {
        "B01WitnessConstructed": True, "B01DirectorPass": False, "B01Closed": False, "B02WitnessConstructed": False,
        "identityAcceptedOrApplied": False, "canonicalRuleChanged": False, "queueChanged": False,
        "runtimeOrGameplayUse": False, "campaignEventClaimed": False,
    },
}
write_json(HERE / "DF218_B01_WITNESS_481_TESTONLY.json", witness)
write_json(HERE / "B01_EVENT_TRACE_481.json", {"id": "DF218-B01-EVENT-TRACE-481", "classification": "TEST_ONLY", "witnessSha256": sha_file(HERE / "DF218_B01_WITNESS_481_TESTONLY.json"), "events": events, "terminalStateSha256": sha_obj(final), "noCampaignEventClaim": True})

readme = f"""# Elemental Shell DF218-B01 witness 481\n\nThis is one reversible, hypothetical TEST_ONLY witness for the exact owner-adopted B01 Proposal478 Repack01 (`{EXPECTED_PROPOSAL_SHA}`). The owner adoption is recorded separately at `{ADOPTION_PATH.relative_to(ROOT).as_posix()}`.\n\nIt models a branch-local Wizard18 self-cast and one bounded noncreature 7-fire pulse. The cast pays 26 RP (68→42), Shell manifests before the pulse, prevents all 7 fire, and the actor remains at 110 HP. Because the source has no responsible creature dealer, the branch records no reflection recipient, reflected packet, or nominal/banked reflection root.\n\nThis corrected packet addresses the four findings in GPT Director hold480. It asserts no campaign event. It closes neither B01 nor B02, changes no canon or queue, and does not accept or apply Elemental Shell. It is awaiting GPT Director review of the correction packet.\n"""
(HERE / "README_481.md").write_text(readme, encoding="utf-8", newline="\n")
print(json.dumps({"status": "BUILT_TEST_ONLY_WITNESS", "proposalSha256": EXPECTED_PROPOSAL_SHA, "adoptionPath": str(ADOPTION_PATH), "witnessPath": str(HERE / "DF218_B01_WITNESS_481_TESTONLY.json"), "events": len(events), "stateSnapshots": len(snapshots), "sourceBindings": len(source_bindings), "queue": "831/17/0", "restoresInitialState": undo == initial}, indent=2))
