import copy
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET294 = A / "rank9_psychic_scream_closure_delta_294/DD_Rank9_PsychicScream_ClosureDelta_294.zip"
REQUEST294 = A / "rank9_psychic_scream_closure_delta_294/CLOSURE_REVIEW_REQUEST_294.json"
PACKET295 = A / "rank9_psychic_scream_fixture_correction_295/DD_Rank9_PsychicScream_FixtureCorrection_295.zip"
OUT = A / "rank9_psychic_scream_fixture_correction_296"
ZIP = OUT / "DD_Rank9_PsychicScream_FixtureCorrection_296.zip"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
REGISTRY = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_293.json"
HANDOFF = A / "CURRENT_HANDOFF_293.json"
PENDING = A / "CURRENT29_PENDING_IDENTITY_AUDIT_293.json"
ID = "psychic-scream"
PROPOSAL_ID = "PF182-B01-BOUNDED-ANATOMY-LIFECYCLE-CONTRACT-01"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def canonical_sha(value) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def binding(path: pathlib.Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}


def write_json(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def part(head_id: str, destructible: bool, vital: str, body_id: str, part_id: str) -> dict:
    return {
        "id": head_id,
        "destructible": destructible,
        "vitalRelationship": vital,
        "bodyAttachment": body_id,
        "remainsPartId": part_id,
        "binding": "authored synthetic fixture only; not creature source evidence",
    }


def make_state(case_id: str, fixture_id: str, heads: list[dict], form_id: str, *, epoch: int = 1, form_a=None) -> dict:
    body = {
        "bodyInstanceId": "SYNTHETIC-BODY-" + fixture_id,
        "currentForm": form_id,
        "formEpoch": epoch,
        "headCount": len(heads),
        "heads": copy.deepcopy(heads),
        "otherParts": [{"id": "PART-TORSO-" + fixture_id, "kind": "torso", "status": "intact", "present": True}],
        "anatomyBinding": "authored synthetic fixture only; not an existing creature source",
    }
    timeline = []
    if form_a:
        timeline.append(copy.deepcopy(form_a))
    else:
        timeline.append({"eventId": "FORM-INITIAL-" + fixture_id, "at": 0.0, "formId": form_id, "formEpoch": epoch, "headCount": len(heads), "heads": copy.deepcopy(heads), "deathBehavior": "retain this form at death unless an explicitly bound fixture transition says otherwise"})
    return {
        "caseId": case_id,
        "spellId": ID,
        "variant": "Wizard/Enchantment",
        "status": "PROPOSED_SYNTHETIC_CONDITIONAL_FIXTURE_NOT_ACCEPTED_NOT_APPLIED",
        "fixtureKind": "authored synthetic conditional fixture only; not runtime, observed play, campaign actor, or creature source evidence",
        "timeSeconds": 0.0,
        "clock": {"regularTurnIndex": 1, "regularStart": 0.0, "regularEndDue": 0.8, "elapsedRegularClockAdvances": 0},
        "actors": {
            "W": {
                "id": "W", "class": "Wizard", "classLevel": 17, "schoolRoute": "Enchantment", "rank": 9,
                "routeAndRepertoireFixture": "synthetic lawful-access precondition; actual campaign acquisition remains source-qualified",
                "resource": {"kind": "RP", "before": 26, "after": 26},
                "actionAvailable": True, "position": [0, 0, 0],
            },
            "T": {
                "id": "T", "body": body, "formTimeline": timeline,
                "HP": 7, "maxHP": 70, "tempHP": 0, "Wounds": 0, "life": "alive",
                "defenses": {"psychicResistance": False, "psychicImmunity": False, "damageReduction": 0, "Null": False},
                "survivalReplacement": None,
                "position": [40, 0, 0], "support": "synthetic grounded support plane",
                "equipment": {
                    "clothing": {"id": "E-CLOTHING-" + fixture_id, "owner": "T", "custodian": "T"},
                    "focus": {"id": "E-FOCUS-" + fixture_id, "owner": "T", "custodian": "T"},
                },
            },
        },
        "save": {"ability": "INT", "DC": 19, "modifier": 0, "conditionalD20": 1, "total": None, "outcome": "pending", "rngExecuted": False, "classification": "bounded synthetic input; the die value is stipulated but remains unresolved until after cast commitment; not an observed roll or derived campaign DC"},
        "castHistory": [],
        "damageHistory": [],
        "deathFormSnapshot": None,
        "headConsequence": None,
        "remains": [],
        "inputs": [
            {"id": "INT-SAVE-" + fixture_id, "domain": "d20 1..20", "selectedValue": 1, "observed": False, "rngExecuted": False, "classification": "synthetic conditional input"},
            {"id": "PSYCHIC-14D6-" + fixture_id, "domain": "14d6 each 1..6", "selectedValues": [6] * 14, "total": 84, "observed": False, "rngExecuted": False, "classification": "synthetic conditional input"},
        ],
        "eventLog": [],
    }


def add_event(case: dict, event_id: str, time_value: float, label: str, mutate) -> None:
    before = copy.deepcopy(case["state"])
    after = copy.deepcopy(before)
    mutate(after)
    before_hash = canonical_sha(before)
    after_hash = canonical_sha(after)
    event = {
        "id": event_id,
        "time": time_value,
        "kind": "AUTHORED_SYNTHETIC_CONDITIONAL_EVENT",
        "detail": label,
        "before": before,
        "beforeSHA256": before_hash,
        "after": after,
        "afterSHA256": after_hash,
        "forward": [{"op": "test", "path": "", "value": before}, {"op": "replace", "path": "", "value": after}],
        "inverse": [{"op": "test", "path": "", "value": after}, {"op": "replace", "path": "", "value": before}],
    }
    case["events"].append(event)
    case["state"] = after


def death_resolution(state: dict, fixture_id: str) -> None:
    target = state["actors"]["T"]
    # No protection changes the 84 psychic damage: HP 7 -> 0; overflow 77 >= maxHP 70.
    target["HP"] = 0
    target["life"] = "dead"
    target["deathCause"] = "instant death from this damage event"
    target["damageSettlement"] = {
        "dice": [6] * 14, "diceTotal": 84, "type": "psychic",
        "resistanceApplied": 0, "immunityApplied": False, "reductionApplied": 0,
        "temporaryHPAbsorbed": 0, "damageToReachZero": 7, "overflowPastZero": 77,
        "maximumHPThreshold": 70, "instantDeathCondition": "77 >= 70", "instantDeath": True,
        "WoundsBefore": 0, "WoundsAfter": 0, "Null": False, "survivalReplacement": None,
        "alternativeFatalWound": None,
    }
    # All valid survival and form transitions are settled before this snapshot.
    target["terminalBodySnapshot"] = {
        "bodyInstanceId": target["body"]["bodyInstanceId"],
        "formId": target["body"]["currentForm"], "formEpoch": target["body"]["formEpoch"],
        "headCount": target["body"]["headCount"], "headIds": [h["id"] for h in target["body"]["heads"]],
        "stage": "after damage, defenses, Null, survival and form rules; at final death",
    }
    state["deathFormSnapshot"] = copy.deepcopy(target["terminalBodySnapshot"])
    state["damageHistory"].append({"id": "DAMAGE-" + fixture_id, "caster": "W", "target": "T", "school": "Enchantment", "type": "psychic", "rolled": 84, "applied": 84})
    remains_parts = copy.deepcopy(target["body"]["otherParts"])
    remains_parts.extend({"id": h["remainsPartId"], "kind": "head", "headId": h["id"], "status": "intact", "present": True} for h in target["body"]["heads"])
    state["remains"] = [{
        "id": "CORPSE-" + fixture_id,
        "bodyInstanceId": target["body"]["bodyInstanceId"],
        "terminalForm": target["body"]["currentForm"], "formEpoch": target["body"]["formEpoch"],
        "location": copy.deepcopy(target["position"]), "support": target["support"],
        "parts": remains_parts,
        "equipmentCustody": copy.deepcopy(target["equipment"]),
        "noDuplicateBodyOrRemains": True,
    }]
    state["eventLog"].append({"id": "FINAL-DEATH-" + fixture_id, "kind": "single-final-death", "bodyInstanceId": target["body"]["bodyInstanceId"], "time": state["timeSeconds"]})


def head_consequence(state: dict, fixture_id: str) -> None:
    assert state["actors"]["T"]["life"] == "dead"
    assert state["deathFormSnapshot"] is not None
    target = state["actors"]["T"]
    destroyed = []
    retained = []
    for head in target["body"]["heads"]:
        if head["destructible"] is True:
            destroyed.append(head["id"])
            next(part for part in state["remains"][0]["parts"] if part["id"] == head["remainsPartId"]).update({"status": "destroyed", "present": False, "destroyedAfterFinalDeath": True})
        else:
            retained.append(head["id"])
    state["headConsequence"] = {
        "trigger": "the same Psychic Scream damage event actually established final death",
        "appliedOnlyAfterFinalDeath": True,
        "snapshotBodyAndFormMatch": state["deathFormSnapshot"]["bodyInstanceId"] == target["body"]["bodyInstanceId"] and state["deathFormSnapshot"]["formId"] == target["body"]["currentForm"],
        "destroyedHeadIds": destroyed,
        "intactHeadIds": retained,
        "headCountZeroMeansNoConsequence": len(target["body"]["heads"]) == 0,
        "extraDamage": 0, "extraSave": False, "newDeathEvent": False, "livingSeverance": False, "revivalBypass": False,
    }
    state["eventLog"].append({"id": "HEAD-CONSEQUENCE-" + fixture_id, "kind": "post-death-head-consequence", "destroyedHeadIds": destroyed, "time": state["timeSeconds"]})
    assert state["remains"][0]["equipmentCustody"] == target["equipment"]
    assert sum(event["kind"] == "single-final-death" for event in state["eventLog"]) == 1
    assert sum(event["kind"] == "post-death-head-consequence" for event in state["eventLog"]) == 1


def apply_root_ops(state, ops):
    current = copy.deepcopy(state)
    for op in ops:
        assert op["path"] == ""
        if op["op"] == "test":
            assert current == op["value"]
        elif op["op"] == "replace":
            current = copy.deepcopy(op["value"])
        else:
            raise AssertionError(op)
    return current


def make_fixture(case_id: str, fixture_id: str, heads: list[dict], form_id: str, *, changed_form: bool = False) -> dict:
    form_a = None
    initial_heads = heads
    initial_form = form_id
    if changed_form:
        form_a_heads = [part("A-H1", True, "vital", "attached-to-body", "PART-A-H1")]
        form_a = {"eventId": "FORM-A-" + fixture_id, "at": 0.0, "formId": "SYNTHETIC-FORM-A", "formEpoch": 1, "headCount": 1, "heads": form_a_heads, "deathBehavior": "no implicit transformation or death rule"}
        initial_heads = form_a_heads
        initial_form = "SYNTHETIC-FORM-A"
    state = make_state(case_id, fixture_id, initial_heads, initial_form, epoch=1, form_a=form_a)
    result = {
        "id": case_id,
        "spellId": ID,
        "correspondsToHeldRecord": (
            "RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-B/positive-final-death-head-consequence"
            if fixture_id in {"01", "04"} else
            "RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-B/headless-multihead-current-form"
        ),
        "status": "PROPOSED_SYNTHETIC_CONDITIONAL_FIXTURE_NOT_ACCEPTED_NOT_APPLIED",
        "completeConditionalProcedureCase": True,
        "actualCampaignOrRuntimeEvidence": False,
        "retainedQualification": "PF181-H03 and source-qualified actual-target anatomy/lifecycle remain required outside these authored synthetic fixtures.",
        "fixtureOnly": True,
        "observedRuntimeOrCampaign": False,
        "existingCreatureSourceEvidence": False,
        "initialState": copy.deepcopy(state),
        "events": [],
    }
    result["state"] = state
    if changed_form:
        form_b_heads = copy.deepcopy(heads)
        def change_to_b(s):
            t = s["actors"]["T"]
            t["body"]["currentForm"] = form_id
            t["body"]["formEpoch"] = 2
            t["body"]["headCount"] = len(form_b_heads)
            t["body"]["heads"] = copy.deepcopy(form_b_heads)
            t["formTimeline"].append({"eventId": "FORM-A-TO-B-" + fixture_id, "at": 0.1, "formId": form_id, "formEpoch": 2, "headCount": len(form_b_heads), "heads": copy.deepcopy(form_b_heads), "trigger": "explicit conditional fixture form-change event", "deathBehavior": "no death-triggered reversion in this fixture; Form B remains terminal form"})
            s["timeSeconds"] = 0.1
            s["clock"]["elapsedRegularClockAdvances"] = 0
        add_event(result, "FORM-CHANGE-" + fixture_id, 0.1, "Explicit synthetic Form A to Form B transition; exact body, epoch, heads and death behavior are recorded.", change_to_b)
    def fail_save(s):
        s["timeSeconds"] = 0.3
        s["save"].update({"total": 1, "outcome": "failed", "settledAt": 0.3, "castCommitmentPrecedesSave": "CAST-" + fixture_id})
        s["eventLog"].append({"id": "INITIAL-INT-SAVE-" + fixture_id, "kind": "conditional-failed-initial-INT-save", "DC": 19, "modifier": 0, "d20": 1, "total": 1, "outcome": "failure", "observed": False, "time": 0.3})
    def cast(s):
        w = s["actors"]["W"]
        w["resource"]["after"] = 0
        w["actionAvailable"] = False
        cast_record = {
            "id": "CAST-" + fixture_id, "spellId": ID, "caster": "W", "class": "Wizard", "classLevel": 17,
            "school": "Enchantment", "rank": 9, "castAction": "Action", "components": ["V", "S", "F"],
            "rpCostBase": 26, "additionalRpCost": 0, "rpBefore": 26, "rpPaid": 26, "rpAfter": 0,
            "resourceSource": "synthetic ledger input; 26 base RP and no added cost are bound to current catalog /spells/395",
            "routeOrRepertoireAcquisition": "synthetic lawful-access precondition only; does not establish campaign acquisition",
            "committed": True, "time": 0.2,
        }
        s["castHistory"].append(cast_record)
        s["timeSeconds"] = 0.2
        s["eventLog"].append({"id": cast_record["id"], "kind": "paid-Wizard-Enchantment-cast", "paidRP": 26, "time": 0.2})
    add_event(result, "CAST-" + fixture_id, 0.2, "The Wizard Enchantment cast is committed and exactly 26 RP are spent from a synthetic opening ledger; no refund is possible.", cast)
    add_event(result, "INITIAL-SAVE-" + fixture_id, 0.3, "After cast commitment, resolve the stipulated synthetic failed INT save; the input itself was recorded earlier but not resolved before commitment.", fail_save)
    def damage(s):
        s["timeSeconds"] = 0.31
        death_resolution(s, fixture_id)
    add_event(result, "DAMAGE-AND-DEATH-" + fixture_id, 0.31, "All 14 conditional d6 results, every relevant defense, survival outcome, final-death arithmetic, terminal form snapshot, corpse support, remains parts and equipment custody are settled.", damage)
    def rider(s):
        s["timeSeconds"] = 0.32
        head_consequence(s, fixture_id)
        if changed_form:
            # This case explicitly supplies its post-death rule: no reversion occurs.
            s["postDeathFormSettlement"] = {
                "ruleBinding": "synthetic fixture only",
                "deathTriggeredReversion": False,
                "terminalForm": form_id,
                "terminalEpoch": 2,
                "remainsForm": form_id,
                "reversionStage": "none; no rule exists in this fixture",
                "destroyedAndIntactPartMapping": {p["id"]: ("destroyed" if p["destructible"] else "intact") for p in s["actors"]["T"]["body"]["heads"]},
                "equipmentCustody": copy.deepcopy(s["actors"]["T"]["equipment"]),
                "noImplicitRestorationOrDuplicateRemains": True,
            }
        s["clock"]["elapsedRegularClockAdvances"] = 0
    add_event(result, "POST-DEATH-RIDER-" + fixture_id, 0.32, "Only enumerated destructible heads in the final-death snapshot are destroyed after death; equipment, remains location/support and regular clock remain unchanged.", rider)
    result["finalState"] = copy.deepcopy(result["state"])
    result["state"] = result["initialState"]
    # Replay each complete state patch forward and then backward, verifying hash and continuity.
    current = copy.deepcopy(result["initialState"])
    replay_rows = []
    for event in result["events"]:
        assert canonical_sha(event["before"]) == event["beforeSHA256"]
        assert canonical_sha(event["after"]) == event["afterSHA256"]
        assert current == event["before"]
        current = apply_root_ops(current, event["forward"])
        assert current == event["after"]
        restored = apply_root_ops(current, event["inverse"])
        assert restored == event["before"]
        replay_rows.append({"event": event["id"], "beforeSHA256": event["beforeSHA256"], "afterSHA256": event["afterSHA256"], "forwardOps": len(event["forward"]), "inverseOps": len(event["inverse"]), "inverseRestoresExactBefore": True})
        current = copy.deepcopy(event["after"])
    assert current == result["finalState"]
    reverse = copy.deepcopy(current)
    for event in reversed(result["events"]):
        reverse = apply_root_ops(reverse, event["inverse"])
        assert reverse == event["before"]
    assert reverse == result["initialState"]
    result["replayAudit"] = {"events": replay_rows, "forwardTraversalReachesFinal": True, "fullReverseTraversalRestoresInitial": True, "finalStateSHA256": canonical_sha(result["finalState"]), "initialStateSHA256": canonical_sha(result["initialState"])}
    del result["state"]
    return result


def main() -> None:
    assert not OUT.exists(), "Refusing to overwrite an existing correction package."
    OUT.mkdir(parents=True)
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    current_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    prior_request = json.loads(REQUEST294.read_text(encoding="utf-8-sig"))
    assert prior_request["authority"]["reviewedApplied"] == 819 and prior_request["authority"]["pending"] == 29
    assert binding(PACKET294)["sha256"] == "a64fbd6b4efd339c84d3bb4afd6fa5d42f72287bfa552f02e97963f81461b197"
    assert binding(PACKET295)["sha256"] == "ec0bdbd0a72101468f5bde73d3abc7ddddcde87516848117fd2f7463a62e4b4f"
    current_catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    target_card = current_catalog["spells"][395]
    assert target_card["id"] == ID
    assert target_card["classAccess"]["Wizard"] == {"rank": 9, "minimumClassLevel": 17, "school": "Enchantment", "baseRpCost": 26}
    assert target_card["additionalRpCost"] == 0
    authority = prior_request["authority"]
    auth_bindings = {"index": binding(INDEX), "catalog": binding(CATALOG), "accessRegistry": binding(REGISTRY), "queue": binding(QUEUE), "handoff": binding(HANDOFF), "pendingAudit": binding(PENDING)}
    assert auth_bindings["index"]["sha256"] == prior_request["authorityBindings"]["index"]["sha256"]
    assert auth_bindings["catalog"]["sha256"] == prior_request["authorityBindings"]["catalog"]["sha256"]
    q = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
    h = json.loads(HANDOFF.read_text(encoding="utf-8-sig"))
    pend = json.loads(PENDING.read_text(encoding="utf-8-sig"))
    assert q["currentAuthority"] == h["currentAuthority"] == pend["authority"] == authority

    positive = [part("H1", True, "vital", "attached-to-SYNTHETIC-BODY-01", "PART-H1-01")]
    headless = []
    multihead = [part("H1", True, "vital", "attached-to-SYNTHETIC-BODY-03", "PART-H1-03"), part("H2", True, "nonvital", "attached-to-SYNTHETIC-BODY-03", "PART-H2-03"), part("H3", False, "nonvital", "attached-to-SYNTHETIC-BODY-03", "PART-H3-03")]
    form_b = [part("B-H1", True, "vital", "attached-to-SYNTHETIC-BODY-04", "PART-B-H1-04"), part("B-H2", True, "nonvital", "attached-to-SYNTHETIC-BODY-04", "PART-B-H2-04")]
    fixtures = [
        make_fixture("PF182-B01-SYNTHETIC-positive-final-death-296", "01", positive, "SYNTHETIC-FORM-ONE-HEAD"),
        make_fixture("PF182-B01-SYNTHETIC-headless-final-death-296", "02", headless, "SYNTHETIC-FORM-HEADLESS"),
        make_fixture("PF182-B01-SYNTHETIC-multihead-final-death-296", "03", multihead, "SYNTHETIC-FORM-THREE-HEADS"),
        make_fixture("PF182-B01-SYNTHETIC-changed-form-final-death-296", "04", form_b, "SYNTHETIC-FORM-B", changed_form=True),
    ]
    fixtures_dir = OUT / "fixtures"
    fixture_bindings = []
    for i, fixture in enumerate(fixtures, start=1):
        fp = fixtures_dir / f"{i:02d}.json"
        write_json(fp, fixture)
        fixture_bindings.append({"fixtureId": fixture["id"], "path": fp.relative_to(OUT).as_posix(), "bytes": fp.stat().st_size, "sha256": sha(fp.read_bytes()), "events": len(fixture["events"]), "forwardOperations": sum(len(e["forward"]) for e in fixture["events"]), "inverseOperations": sum(len(e["inverse"]) for e in fixture["events"]), "stateHashes": len(fixture["events"]) * 2})

    contract = {
        "id": PROPOSAL_ID,
        "revision": 296,
        "status": "PROPOSED_FOR_DIRECTOR_ADJUDICATION_NOT_ACCEPTED_NOT_SOURCE_EVIDENCE",
        "scope": "Psychic Scream Wizard/Enchantment authored procedure only. Mage/Evocation stun, three printed placements, and two source access routes remain unchanged; Illusion placement creates no access route.",
        "newAuthoredFields": [
            "bodyInstanceId", "formTimeline[] with exact event/time/formEpoch and terminal/death behavior", "headCount", "heads[] with unique IDs/destructible/vitalRelationship/bodyAttachment/remainsPartId", "sourceOrFixtureBinding", "damageAndDefenseSettlement", "survivalAndNullSettlement", "deathFormSnapshot", "postDeathHeadConsequence[]", "postDeathFormSettlement", "remains location/support/part state", "equipment owner/custodian ledger"],
        "ordering": [
            "Commit the paid Wizard Enchantment cast and settle each 14d6 input.",
            "Apply actual damage defenses and temporary HP; settle Wounds, Null, survival and every pre-existing form/lifecycle rule.",
            "Only if that exact damage event establishes final death, snapshot the same body instance's terminal form epoch and enumerated heads.",
            "After the snapshot and final-death event, apply the head consequence solely to snapshot heads explicitly marked destructible=true.",
            "Apply only an explicitly supplied post-death form rule; never delay a source-mandated earlier reversion. Remains and equipment custody are retained by explicit IDs."],
        "syntheticFixtureChoice": {"HP": 7, "maxHP": 70, "tempHP": 0, "damageDice": [6] * 14, "damage": 84, "defenses": "none", "Null": False, "survivalReplacement": None, "overflowPastZero": 77, "instantDeathThreshold": 70, "calculation": "84 - 7 = 77; 77 >= 70, so Instant Death under the selected existing rule", "classification": "newly authored conditional fixture inputs, not source-qualified creature values"},
        "postDeathFormSettlementRuleForChangedFormFixture": "Fixture 04 explicitly has no death-triggered reversion: Form B epoch 2 remains the terminal form and remains form. This fixture does not impose ordering on actual source rules.",
        "notDefinedAsSourceFacts": True,
        "retainedActualTargetQualification": "PF181-H03 remains. Actual campaign use still requires source-qualified current body/form anatomy, enumerated heads, destructibility/vitality, and exact reversion/remains lifecycle. These synthetic fixtures cannot satisfy that actual-target requirement.",
        "supersedesOnlyIfAccepted": ["two held Psychic Scream anatomy records; exact IDs in request"],
    }
    write_json(OUT / "ANATOMY_LIFECYCLE_CONTRACT_296.json", contract)
    decision_scope = {
        "directorResponseTo294": {
            "decision": "HOLD psychic-scream / PF182-B01; accepted=false; applied=false",
            "authorizedRoute": "Bounded, explicitly NEW synthetic anatomy fixtures may be used for authored-procedure review while retaining PF181-H03 and source-qualified actual-target requirements; they may supersede two held anatomy records only after complete and verified.",
            "requiredCorrections": [
                "Positive final-death fixture must show full recipient snapshot and valid death calculation; HP7/maxHP70 with no defenses/tempHP/survival replacement and 84 damage produces 77 excess, meeting maxHP70.",
                "Changed-form fixture must fully specify each head's vitality, attachment and remains part ID, event timing, terminal form/reversion, destroyed/intact part mapping and equipment custody.",
                "Resolve all existing survival/form rules before terminal-body snapshot; only a separately defined post-death callback may follow head consequence, and it cannot postpone source-mandated earlier reversion.",
                "Provide full reversible before/after traces for positive-death, headless, multihead and changed-form cases, with remains/support/custody records, paid cast and forward/inverse verification."],
            "verifiedPreservation": "Delta294 bindings and 16 preserved cases / 227 events / 454 forward / 454 inverse operations were verified; this preserves old evidence but does not demonstrate new fixtures.",
            "nextOrder": ["mass-phantom-killer", "weird", "final-word"],
            "authority": authority,
        },
        "directorResponseTo295": {
            "decision": "HOLD psychic-scream / PF182-B01; accepted=false; applied=false",
            "substantiveCorrectionStatus": "The death calculation, terminal Form B, remains mapping and custody satisfy the substantive corrections; bounded synthetic-review route remains authorized.",
            "remainingCorrections": [
                {"id": "PF295-C01", "issue": "Save resolved at0.2 before paid cast at0.3.", "requiredChronology": ["paid CAST at0.2", "initial INT save resolved at0.3", "damage and death at0.31"], "stipulatedDieMayBePresentBeforeCast": True, "saveMustRemainUnresolvedUntilCommitment": True, "changedFormAt0.1Retained": True},
                {"id": "PF295-C02", "issue": "Head-consequence event log timestamp was0.31 while enclosing rider event was0.32.", "requiredCorrection": "Set every post-death head-consequence log entry to0.32, keep final death at0.31, and regenerate final states, hashes and reversible patches."},
            ],
            "verifiedReplay": "All17 events and34 forward/34 inverse operations passed replay, including full reverse traversal; this did not cure the chronology defects.",
            "authority": authority,
        },
        "thisCorrection": "Only the four newly-authored synthetic conditional fixtures and their bounded field/order contract are submitted. No other identity is ruled, accepted, applied, or changed.",
        "packet294": {"path": PACKET294.relative_to(ROOT).as_posix(), **binding(PACKET294)},
        "packet295": {"path": PACKET295.relative_to(ROOT).as_posix(), **binding(PACKET295)},
        "packet294Request": {"path": REQUEST294.relative_to(ROOT).as_posix(), **binding(REQUEST294)},
        "baseCommit": current_head,
        "branch": branch,
        "workingTreeSnapshot": "Current authority bindings describe an uncommitted review snapshot distinct from the base commit.",
        "authorityBindings": auth_bindings,
        "currentAuthority": authority,
        "currentPsychicScreamCard": {"pointer": "/spells/395", "currentCatalogBinding": binding(CATALOG), "id": target_card["id"], "classAccess": target_card["classAccess"], "additionalRpCost": target_card["additionalRpCost"]},
        "fixtures": fixture_bindings,
        "decisionRequested": "Adjudicate only whether the four complete, reversible, explicitly synthetic conditional fixtures and the revised NEW anatomy/lifecycle contract satisfy the Psychic Scream authored-procedure review route authorized in the HOLD. Retain PF181-H03 and all source-qualified actual-target requirements. If one trace still fails, identify its exact pointer and minimum correction. No acceptance or application is requested for any other identity.",
        "accepted": False,
        "applied": False,
    }
    write_json(OUT / "DIRECTOR_HOLD_AND_CORRECTION_SCOPE_296.json", decision_scope)

    # Independent audit of calculations, fixture distinctions, hashes, custody and bidirectional patches.
    audit_rows = []
    for fixture in fixtures:
        state = fixture["finalState"]
        target = state["actors"]["T"]
        settlement = target["damageSettlement"]
        cast_event = next(e for e in fixture["events"] if e["id"].startswith("CAST-"))
        save_event = next(e for e in fixture["events"] if e["id"].startswith("INITIAL-SAVE-"))
        head_log = next(e for e in state["eventLog"] if e["kind"] == "post-death-head-consequence")
        audit_rows.append({
            "fixtureId": fixture["id"],
            "conditionalOnly": fixture["fixtureOnly"] and not fixture["observedRuntimeOrCampaign"] and not fixture["existingCreatureSourceEvidence"],
            "paidCast": len(state["castHistory"]) == 1 and state["castHistory"][0]["rpBefore"] - state["castHistory"][0]["rpPaid"] == state["castHistory"][0]["rpAfter"] == 0,
            "chronologyCastThenSave": fixture["events"].index(cast_event) < fixture["events"].index(save_event) and cast_event["time"] == 0.2 and save_event["time"] == 0.3 and cast_event["after"]["save"]["outcome"] == "pending" and save_event["before"]["save"]["outcome"] == "pending" and save_event["after"]["save"]["outcome"] == "failed" and save_event["before"]["castHistory"],
            "allFourteenDamageDice": settlement["dice"] == [6] * 14 and sum(settlement["dice"]) == 84,
            "finalDeathThreshold": settlement["overflowPastZero"] == 77 and settlement["maximumHPThreshold"] == 70 and settlement["instantDeath"] is True,
            "defenseAndSurvivalSettlement": settlement["resistanceApplied"] == settlement["reductionApplied"] == settlement["temporaryHPAbsorbed"] == 0 and not settlement["immunityApplied"] and settlement["Null"] is False and settlement["survivalReplacement"] is None,
            "oneDeathOneDamageEvent": sum(event["kind"] == "single-final-death" for event in state["eventLog"]) == 1 and len(state["damageHistory"]) == 1 and state["headConsequence"]["newDeathEvent"] is False,
            "riderTimestampMatchesItsEvent": head_log["time"] == 0.32 and next(e for e in fixture["events"] if e["id"].startswith("POST-DEATH-RIDER-"))["time"] == 0.32 and next(e for e in state["eventLog"] if e["kind"] == "single-final-death")["time"] == 0.31,
            "remainsAndEquipmentCustody": len(state["remains"]) == 1 and state["remains"][0]["bodyInstanceId"] == target["body"]["bodyInstanceId"] and state["remains"][0]["support"] == target["support"] and state["remains"][0]["equipmentCustody"] == target["equipment"],
            "eventCount": len(fixture["events"]),
            "allBeforeAfterAndReversalsVerified": fixture["replayAudit"]["forwardTraversalReachesFinal"] and fixture["replayAudit"]["fullReverseTraversalRestoresInitial"],
        })
    outcomes = {row["fixtureId"].split("SYNTHETIC-")[-1].split("-296")[0]: row for row in audit_rows}
    assert fixtures[0]["finalState"]["headConsequence"]["destroyedHeadIds"] == ["H1"]
    assert fixtures[1]["finalState"]["headConsequence"]["destroyedHeadIds"] == []
    assert fixtures[1]["finalState"]["headConsequence"]["headCountZeroMeansNoConsequence"] is True
    assert fixtures[2]["finalState"]["headConsequence"]["destroyedHeadIds"] == ["H1", "H2"]
    assert fixtures[2]["finalState"]["headConsequence"]["intactHeadIds"] == ["H3"]
    assert fixtures[3]["finalState"]["deathFormSnapshot"]["formId"] == "SYNTHETIC-FORM-B"
    assert fixtures[3]["finalState"]["postDeathFormSettlement"]["terminalForm"] == "SYNTHETIC-FORM-B"
    assert all(all(row[k] for k in ("conditionalOnly", "paidCast", "chronologyCastThenSave", "allFourteenDamageDice", "finalDeathThreshold", "defenseAndSurvivalSettlement", "oneDeathOneDamageEvent", "riderTimestampMatchesItsEvent", "remainsAndEquipmentCustody", "allBeforeAfterAndReversalsVerified")) for row in audit_rows)
    audit = {
        "id": "PSYCHIC-SCREAM-FIXTURE-CORRECTION-INDEPENDENT-AUDIT-296",
        "recordedAtUtc": stamp,
        "status": "PASS",
        "authority": authority,
        "currentBaseCommit": current_head,
        "currentBranch": branch,
        "currentSpellCard": {"pointer": "/spells/395", "classAccess": target_card["classAccess"], "additionalRpCost": target_card["additionalRpCost"], "binding": binding(CATALOG)},
        "fixtures": audit_rows,
        "caseCount": 4,
        "eventCount": sum(len(f["events"]) for f in fixtures),
        "forwardOperations": sum(sum(len(e["forward"]) for e in f["events"]) for f in fixtures),
        "inverseOperations": sum(sum(len(e["inverse"]) for e in f["events"]) for f in fixtures),
        "stateHashCount": sum(len(f["events"]) * 2 for f in fixtures),
        "checks": [
            {"check": "Exact current spell card binds Wizard rank9 Enchantment, level17 and base cost26; no additional cost", "passed": True},
            {"check": "Each synthetic fixture records failed INT save, paid cast, all fourteen 14d6 inputs and full damage-defense-survival-death settlement", "passed": True},
            {"check": "Cast at0.2 precedes initial save at0.3; stipulated d20 remains unresolved until after paid commitment", "passed": all(row["chronologyCastThenSave"] for row in audit_rows)},
            {"check": "Head-consequence log time0.32 matches the enclosing rider event; final death remains time0.31", "passed": all(row["riderTimestampMatchesItsEvent"] for row in audit_rows)},
            {"check": "HP7/maxHP70 with 84 damage yields 77 overflow, meeting the 70 instant-death threshold", "passed": True},
            {"check": "Headless case has no head consequence; multihead destroys only enumerated destructible heads", "passed": True},
            {"check": "Changed form names exact body, head IDs/parts, event timing, terminal form, no-reversion fixture rule, remains and equipment custody", "passed": True},
            {"check": "All event state hashes, forward traversals and inverse restoration checks pass", "passed": True},
            {"check": "All proposals remain synthetic; PF181-H03 and actual source-qualified target requirements remain", "passed": True},
            {"check": "No accepted/applied field or canonical authority change is proposed", "passed": True},
        ],
        "accepted": False,
        "applied": False,
    }
    write_json(OUT / "INDEPENDENT_AUDIT_296.json", audit)
    assert all(c["passed"] for c in audit["checks"])

    manifest = {"id": "PSYCHIC-SCREAM-FIXTURE-CORRECTION-MANIFEST-296", "recordedAtUtc": stamp, "authority": authority, "baseCommit": current_head, "branch": branch, "status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT_NO_ACCEPTANCE_OR_APPLICATION", "files": []}
    write_json(OUT / "DELIVERY_MANIFEST_296.json", manifest)
    manifest["files"] = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path not in {ZIP, OUT / "DELIVERY_MANIFEST_296.json"}:
            raw = path.read_bytes()
            manifest["files"].append({"path": path.relative_to(OUT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
    write_json(OUT / "DELIVERY_MANIFEST_296.json", manifest)
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(OUT.rglob("*")):
            if path.is_file() and path != ZIP:
                archive.write(path, path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(manifest["files"]) + 1
        for row in manifest["files"]:
            raw = archive.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
    print(json.dumps({"status": "PASS", "authority": authority, "fixtureCount": 4, "eventCount": audit["eventCount"], "forwardOperations": audit["forwardOperations"], "inverseOperations": audit["inverseOperations"], "zip": {"path": ZIP.relative_to(ROOT).as_posix(), "bytes": ZIP.stat().st_size, "sha256": sha(ZIP.read_bytes()), "crc32": f"{zlib.crc32(ZIP.read_bytes()) & 0xFFFFFFFF:08x}"}, "audit": {"path": (OUT / "INDEPENDENT_AUDIT_296.json").relative_to(ROOT).as_posix(), "sha256": sha((OUT / "INDEPENDENT_AUDIT_296.json").read_bytes())}}, indent=2))


if __name__ == "__main__":
    main()
