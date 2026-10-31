from __future__ import annotations

import copy
import hashlib
import io
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "conjure_demiplane_fortress_closure_intake_366"
OUTPUT = ROOT / "conjure_demiplane_fortress_closure_intake_367"
PAYLOAD = OUTPUT / "payload"
SOURCE_ARCHIVE_366 = SOURCE / "DD_Rank9_ConjureDemiplaneFortress_PG200B06_ClosureIntake366.zip"
ARCHIVE_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG200B06_ClosureIntake367.zip"
DELIVERY_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG200B06_ClosureIntake367_DELIVERY.json"
AUDIT_NAME = "INDEPENDENT_AUDIT_367.json"
FIXTURE_NAME = "PG328-W03_BENEFICIAL_SHORT_REST_367_TESTONLY.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pointer_part(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def join_pointer(path: str, key: str) -> str:
    return path + "/" + pointer_part(key)


def diff_ops(before: object, after: object, path: str = "") -> list[dict]:
    """Create scoped JSON-Patch operations, guarded by exact old-value tests."""
    if isinstance(before, dict) and isinstance(after, dict):
        ops: list[dict] = []
        for key in sorted(before.keys() & after.keys()):
            ops.extend(diff_ops(before[key], after[key], join_pointer(path, key)))
        for key in sorted(before.keys() - after.keys()):
            p = join_pointer(path, key)
            ops.extend([{"op": "test", "path": p, "value": before[key]}, {"op": "remove", "path": p}])
        for key in sorted(after.keys() - before.keys()):
            p = join_pointer(path, key)
            ops.append({"op": "add", "path": p, "value": after[key]})
        return ops
    if before == after:
        return []
    if path == "":
        raise ValueError("Root replacement is intentionally disallowed; keep the patch scoped.")
    return [
        {"op": "test", "path": path, "value": before},
        {"op": "replace", "path": path, "value": after},
    ]


def unescape_pointer_part(value: str) -> str:
    return value.replace("~1", "/").replace("~0", "~")


def get_at_pointer(root: object, pointer: str) -> object:
    current = root
    if pointer == "":
        return current
    for part in pointer.lstrip("/").split("/"):
        key = unescape_pointer_part(part)
        current = current[int(key)] if isinstance(current, list) else current[key]
    return current


def parent_at_pointer(root: object, pointer: str) -> tuple[object, str]:
    parent_path, _, last = pointer.rpartition("/")
    parent = get_at_pointer(root, parent_path)
    return parent, unescape_pointer_part(last)


def apply_ops(state: object, operations: list[dict]) -> object:
    result = copy.deepcopy(state)
    for operation in operations:
        op = operation["op"]
        path = operation["path"]
        if op == "test":
            if get_at_pointer(result, path) != operation["value"]:
                raise AssertionError(f"JSON patch test failed at {path}")
            continue
        parent, key = parent_at_pointer(result, path)
        if isinstance(parent, list):
            index = int(key)
            if op == "replace":
                parent[index] = copy.deepcopy(operation["value"])
            elif op == "remove":
                parent.pop(index)
            elif op == "add":
                parent.insert(index, copy.deepcopy(operation["value"]))
            else:
                raise ValueError(op)
        elif op == "replace":
            if key not in parent:
                raise AssertionError(f"replace target missing at {path}")
            parent[key] = copy.deepcopy(operation["value"])
        elif op == "remove":
            if key not in parent:
                raise AssertionError(f"remove target missing at {path}")
            del parent[key]
        elif op == "add":
            if key in parent:
                raise AssertionError(f"add target already exists at {path}")
            parent[key] = copy.deepcopy(operation["value"])
        else:
            raise ValueError(op)
    return result


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_transition(
    event_id: str,
    kind: str,
    before: dict,
    after: dict,
    event_time: dict,
    source_bindings: list[str],
    rationale: str,
) -> dict:
    forward = diff_ops(before, after)
    inverse = diff_ops(after, before)
    if apply_ops(before, forward) != after or apply_ops(after, inverse) != before:
        raise AssertionError(f"forward/inverse replay failed for {event_id}")
    return {
        "id": event_id,
        "kind": kind,
        "eventTime": event_time,
        "sourceBindings": source_bindings,
        "rationale": rationale,
        "beforeSHA256": digest(before),
        "afterSHA256": digest(after),
        "before": copy.deepcopy(before),
        "after": copy.deepcopy(after),
        "forward": forward,
        "inverse": inverse,
    }


def verify_pointer(document: object, pointer: str) -> None:
    get_at_pointer(document, pointer)


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"Refusing to overwrite existing output folder: {OUTPUT}")
    PAYLOAD.mkdir(parents=True)
    with zipfile.ZipFile(SOURCE_ARCHIVE_366) as source_archive:
        if source_archive.testzip() is not None:
            raise AssertionError("The sealed Intake366 source archive failed CRC testing.")
        for name in source_archive.namelist():
            parts = Path(name).parts
            if Path(name).is_absolute() or ".." in parts:
                raise AssertionError(f"Unsafe source archive member path: {name}")
        source_archive.extractall(PAYLOAD)

    old_fixture_path = PAYLOAD / "fixtures/PG328-W03_BENEFICIAL_SHORT_REST_366_TESTONLY.json"
    old_fixture_path.unlink()

    held_archive_path = PAYLOAD / "authority/PG328_HELD_ARCHIVE.zip"
    held_archive_bytes = held_archive_path.read_bytes()
    nested = zipfile.ZipFile(io.BytesIO(held_archive_bytes))
    baseline_member = (
        "evidence/packet328/prior/Return284_cases/"
        "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A__beneficial-short-rest.json"
    )
    baseline_member_bytes = nested.read(baseline_member)
    baseline = json.loads(baseline_member_bytes)
    nested.close()

    # Resolve every operative locator against the exact payload copy before
    # declaring a source binding usable in the new fixture.
    profile = json.loads((PAYLOAD / "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json").read_text(encoding="utf-8-sig"))
    wizard = json.loads((PAYLOAD / "sources/wizard.json").read_text(encoding="utf-8-sig"))
    procedure = json.loads((PAYLOAD / "rules/PG328_PROCEDURE_CURRENT.json").read_text(encoding="utf-8-sig"))
    for document, pointers in [
        (profile, ["/rpMaximum", "/abilityScores/INT", "/modifiers/INT"]),
        (wizard, ["/cards/0"]),
        (procedure, ["/procedure", "/sharedContract", "/sharedContract/clocks"]),
    ]:
        for pointer in pointers:
            verify_pointer(document, pointer)
    player_rule_lines = (PAYLOAD / "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt").read_text(encoding="utf-8").splitlines()
    combat_lines = (PAYLOAD / "sources/COMBAT_ACTION_PLAYTEST.md").read_text(encoding="utf-8").splitlines()
    if "1/4 your maximum pool + primary spellcasting modifier" not in player_rule_lines[8390]:
        raise AssertionError("The ordinary short-rest RP locator no longer resolves to line 8391.")
    if "Retune: A short rest resets Dissonance" not in player_rule_lines[8439]:
        raise AssertionError("The Retune locator no longer resolves to line 8440.")
    if len(combat_lines) < 47 or not combat_lines[46].strip():
        raise AssertionError("The inherited virtual-deadline text locator no longer resolves to line 47.")
    parent_state = copy.deepcopy(baseline["final"])
    if digest(parent_state) != baseline["finalSHA256"]:
        raise AssertionError("The preserved Return284 final state does not match its sealed hash.")
    if parent_state["mode"] != "initiative" or set(parent_state["actors"]) != {"A", "B", "C", "D"}:
        raise AssertionError("Unexpected preserved baseline state shape.")
    if len(parent_state["items"]) != 12:
        raise AssertionError("Unexpected preserved baseline inventory count.")

    fortress_space = parent_state["actors"]["A"]["plane"]
    ration_id = "REST-FOOD-367-A"
    water_id = "REST-WATER-367-A"
    if ration_id in parent_state["items"] or water_id in parent_state["items"]:
        raise AssertionError("TEST_ONLY supply item IDs collide with inherited inventory.")

    fork_state = copy.deepcopy(parent_state)
    fork_state["actors"]["A"]["equipment"].extend([ration_id, water_id])
    fork_state["actors"]["A"]["carriedWeightLb"] += 10
    fork_state["actors"]["A"]["carriedLoad"] = round(fork_state["actors"]["A"]["carriedLoad"] + 1.0, 3)
    fork_state["items"][ration_id] = {
        "id": ration_id,
        "kind": "mundane ration",
        "massLb": 2,
        "load": 0.2,
        "owner": "A",
        "custodian": "A",
        "plane": fortress_space,
        "position": None,
        "exists": True,
        "quantity": 1,
        "quantityConsumed": 0,
        "quantityRemaining": 1,
        "provenance": "explicit TEST_ONLY branch-inventory premise; mundane; not created or replenished by Fortress",
        "consumed": False,
        "consumptionStatus": "TEST_ONLY_INPUT; quantity consumed is explicitly 0 because no bound consumption rule is supplied",
        "sizeFeet": [0.5, 0.5, 0.5],
    }
    fork_state["items"][water_id] = {
        "id": water_id,
        "kind": "mundane drinking water",
        "massLb": 8,
        "load": 0.8,
        "owner": "A",
        "custodian": "A",
        "plane": fortress_space,
        "position": None,
        "exists": True,
        "quantity": 1,
        "quantityConsumed": 0,
        "quantityRemaining": 1,
        "provenance": "explicit TEST_ONLY branch-inventory premise; mundane; not created or replenished by Fortress",
        "consumed": False,
        "consumptionStatus": "TEST_ONLY_INPUT; quantity consumed is explicitly 0 because no bound consumption rule is supplied",
        "sizeFeet": [0.5, 0.5, 1],
    }
    fork_forward = diff_ops(parent_state, fork_state)
    fork_inverse = diff_ops(fork_state, parent_state)
    if apply_ops(parent_state, fork_forward) != fork_state or apply_ops(fork_state, fork_inverse) != parent_state:
        raise AssertionError("The TEST_ONLY inventory fork extension does not reverse exactly.")

    before = copy.deepcopy(fork_state)
    after_mode = copy.deepcopy(before)
    after_mode["mode"] = "outside_initiative"
    mode_event = make_transition(
        "PG328-W03-367-E1",
        "TEST_ONLY_MODE_SWITCH_TO_OUTSIDE_INITIATIVE",
        before,
        after_mode,
        {"initiativeCoordinate": 0.9, "worldElapsedSeconds": 1.0},
        ["rules/PG328_PROCEDURE_CURRENT.json#/sharedContract/clocks"],
        "Use the operative outside-initiative elapsed-time mode after A's completed END. Preserve every inherited regularSchedule marker and budget; no new turn or reset is created.",
    )

    after_virtual_deadline = copy.deepcopy(after_mode)
    actor_a = after_virtual_deadline["actors"]["A"]
    marker = actor_a["spellEfficiency"]["until"]
    marker_delta = marker - after_virtual_deadline["time"]
    if marker != actor_a["regularSchedule"]["nextEnd"]:
        raise AssertionError("The A spell-efficiency deadline no longer matches the preserved virtual end marker.")
    after_virtual_deadline["clock"]["elapsedSeconds"] += marker_delta
    after_virtual_deadline["clock"]["OpeningRemaining"] -= marker_delta
    after_virtual_deadline["clock"]["HornRemaining"] -= marker_delta
    actor_a["spellEfficiency"] = None
    deadline_world = after_virtual_deadline["clock"]["elapsedSeconds"]
    deadline_event = make_transition(
        "PG328-W03-367-E2",
        "VIRTUAL_SOURCE_DEADLINE_EXPIRES",
        after_mode,
        after_virtual_deadline,
        {
            "mode": "outside_initiative",
            "preservedScheduleMarker": marker,
            "worldElapsedSeconds": deadline_world,
            "elapsedSecondsAdvanced": marker_delta,
        },
        [
            "sources/COMBAT_ACTION_PLAYTEST.md#line=47",
            "rules/PG328_PROCEDURE_CURRENT.json#/sharedContract/clocks",
        ],
        "Expire A's source-start spell-efficiency at its inherited virtual marker. The initiative coordinate remains the last initiative time; world/Opening/Horn clocks advance 1:1.",
    )

    after_interval = copy.deepcopy(after_virtual_deadline)
    remaining_interval = 3600.0 - marker_delta
    after_interval["clock"]["elapsedSeconds"] += remaining_interval
    after_interval["clock"]["OpeningRemaining"] -= remaining_interval
    after_interval["clock"]["HornRemaining"] -= remaining_interval
    interval_end_world = after_interval["clock"]["elapsedSeconds"]
    interval_event = make_transition(
        "PG328-W03-367-E3",
        "ELAPSED_TEST_ONLY_REST_CANDIDATE_INTERVAL_END_UNADJUDICATED",
        after_virtual_deadline,
        after_interval,
        {
            "mode": "outside_initiative",
            "candidateIntervalStartWorldElapsedSeconds": 1.0,
            "intervalEndWorldElapsedSeconds": interval_end_world,
            "elapsedSecondsAdvanced": remaining_interval,
            "candidateIntervalTotalSeconds": 3600,
        },
        ["rules/PG328_PROCEDURE_CURRENT.json#/sharedContract/clocks"],
        "Advance elapsed time and inherited source clocks. Do not assert rest eligibility, completion, recovery, use-counter change, or an actual campaign event.",
    )

    transitions = [mode_event, deadline_event, interval_event]
    for previous, current in zip(transitions, transitions[1:]):
        if previous["after"] != current["before"]:
            raise AssertionError(f"Transition continuity failed between {previous['id']} and {current['id']}.")

    inventory_overlay = {
        "status": "CONDITIONAL_TEST_ONLY_FORK_INPUT",
        "parentStateSHA256": baseline["finalSHA256"],
        "extendedForkStateSHA256": digest(fork_state),
        "forward": fork_forward,
        "inverse": fork_inverse,
        "testOnlyInputs": [
            {"itemId": ration_id, "quantity": 1, "quantityConsumed": 0, "quantityRemaining": 1, "custodian": "A", "plane": fortress_space, "consumed": False},
            {"itemId": water_id, "quantity": 1, "quantityConsumed": 0, "quantityRemaining": 1, "custodian": "A", "plane": fortress_space, "consumed": False},
        ],
        "limitation": "These branch inventory premises extend the preserved final snapshot only; they do not alter the source case or assert an actual campaign transit/history.",
    }

    fixture = {
        "id": "PG328-W03-BENEFICIAL-SHORT-REST-367-TESTONLY",
        "targetId": "conjure-demiplane-fortress",
        "blockerId": "PG328-W03",
        "status": "CONDITIONAL_TEST_ONLY_FOR_DIRECTOR_ADJUDICATION",
        "purpose": "Exercise a hypothetical ordinary-RP short-rest candidate in the persistent Fortress while retaining the complete inherited case state, inventory, schedules, effects and source clocks.",
        "notCampaignOccurrence": True,
        "notCanonicalOrRuntimeImplementation": True,
        "supersedesFixture": "PG328-W03-BENEFICIAL-SHORT-REST-366-TESTONLY",
        "priorDirectorDisposition": {
            "decision": "HOLD",
            "sealedWitnessIds": [],
            "remainingResidualIds": ["PG366-W03-R1"],
            "revisedForFreshAdjudication": ["PG366-W03-R2", "PG366-W03-R3", "PG366-W03-R4", "PG366-M01"],
            "note": "The new fixture addresses the state, reversible evidence, locator and count findings. No finding is marked closed until the Director rechecks this revision.",
        },
        "sourceBindings": [
            {
                "file": "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt",
                "sha256": file_digest(PAYLOAD / "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt"),
                "locators": [
                    {"kind": "text_line", "line": 8391},
                    {"kind": "text_line", "line": 8440},
                ],
                "supports": "Line 8391: ordinary short-rest RP formula. Line 8440: if a short rest qualifies, Retune resets Dissonance; that is not an extra RP award.",
            },
            {
                "file": "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json",
                "sha256": file_digest(PAYLOAD / "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json"),
                "locators": [
                    {"kind": "json_pointer", "pointer": "/rpMaximum"},
                    {"kind": "json_pointer", "pointer": "/abilityScores/INT"},
                    {"kind": "json_pointer", "pointer": "/modifiers/INT"},
                ],
                "supports": "Conditional Wizard20 profile: maximum RP80 and INT20/modifier+5.",
            },
            {
                "file": "sources/wizard.json",
                "sha256": file_digest(PAYLOAD / "sources/wizard.json"),
                "locators": [{"kind": "json_pointer", "pointer": "/cards/0"}],
                "supports": "Arcane Recovery source is present; this conditional path does not invoke it.",
            },
            {
                "file": "rules/PG328_PROCEDURE_CURRENT.json",
                "sha256": file_digest(PAYLOAD / "rules/PG328_PROCEDURE_CURRENT.json"),
                "locators": [
                    {"kind": "json_pointer", "pointer": "/procedure", "paragraphLabel": "PG9-Q26"},
                    {"kind": "json_pointer", "pointer": "/procedure", "paragraphLabel": "PG9-Q28"},
                    {"kind": "json_pointer", "pointer": "/sharedContract"},
                    {"kind": "json_pointer", "pointer": "/sharedContract/clocks"},
                ],
                "supports": "Q26/Q28 require real supplies, safety, duration and limits; Fortress creates no food/water and is not a universal safe haven. Shared clocks require outside-initiative elapsed deadlines and preservation of prior markers.",
            },
            {
                "file": "sources/COMBAT_ACTION_PLAYTEST.md",
                "sha256": file_digest(PAYLOAD / "sources/COMBAT_ACTION_PLAYTEST.md"),
                "locators": [{"kind": "text_line", "line": 47}],
                "supports": "Existing effects keep their virtual marker when initiative changes; the existing schedule is not restarted.",
            },
            {
                "file": "authority/PG328_HELD_ARCHIVE.zip",
                "sha256": file_digest(held_archive_path),
                "member": baseline_member,
                "pointer": "/final",
                "supports": "Complete preserved parent state at the exact Return284 branch end; this source member is byte-preserved.",
            },
        ],
        "baselineCase": {
            "archive": "authority/PG328_HELD_ARCHIVE.zip",
            "member": baseline_member,
            "memberSHA256": hashlib.sha256(baseline_member_bytes).hexdigest(),
            "finalStateSHA256": baseline["finalSHA256"],
            "event": "END at initiative coordinate 0.9; complete A/B/C/D state, twelve items, active Fortress and all source clocks preserved.",
            "forkOverlay": "The two mundane supply objects are explicit TEST_ONLY branch inventory at the fork checkpoint; the preserved source member is not modified.",
        },
        "forkExtension": inventory_overlay,
        "testOnlyInputs": {
            "restDurationSeconds": 3600,
            "durationStatus": "UNADJUDICATED_TEST_ONLY_INPUT; no bound accepted source specifies a short-rest minimum duration.",
            "shortRestEligibility": "UNADJUDICATED; this fixture ends a candidate interval and does not assert a qualifying completed rest.",
            "candidateIntervalStartWorldElapsedSeconds": 1.0,
            "candidateIntervalEndWorldElapsedSeconds": interval_end_world,
            "lastBeneficialLongRestAgeAtStartSeconds": 86401.0,
            "shortRestsSinceLongAtStart": 0,
            "supplyInventory": [
                {"itemId": ration_id, "quantity": 1, "quantityConsumed": 0, "quantityRemaining": 1, "custodian": "A", "consumed": False},
                {"itemId": water_id, "quantity": 1, "quantityConsumed": 0, "quantityRemaining": 1, "custodian": "A", "consumed": False},
            ],
            "safety": "No hostile creature/hazard is present during the hypothetical interval; this is a fixture premise and does not imply Fortress grants safety.",
            "noInterruption": "TEST_ONLY premise: no attack, labor, travel, casting or Weave ability during the candidate interval.",
            "consumption": "Each inventory item records quantityConsumed=0 and quantityRemaining=1. This is a deliberate no-consumption claim, because no bound consumption rule is supplied; the Director must not infer that the supplies legally suffice for rest.",
            "noOtherRecovery": "No Arcane Recovery, meditation, Retune, long-rest recovery, or other RP source is applied while eligibility is unadjudicated.",
        },
        "conditionalCalculation": {
            "eligibility": "UNADJUDICATED; no state transition is authorized from this arithmetic alone.",
            "maxRP": 80,
            "oneQuarterMaximum": 20,
            "primarySpellcastingModifier": 5,
            "ordinaryRecoveryIfQualified": 25,
            "RPBefore": 54,
            "RPAfterIfQualified": 79,
            "capApplied": False,
            "ArcaneRecoveryApplied": False,
            "DissonanceBefore": 0,
            "RetuneIfQualified": "0 remains 0; this is not an additional RP award.",
            "stateSettlementApplied": False,
        },
        "before": before,
        "modeBridge": {
            "from": "initiative",
            "to": "outside_initiative",
            "source": "rules/PG328_PROCEDURE_CURRENT.json#/sharedContract/clocks",
            "preservedScheduleMarkers": {
                actor: {
                    "nextStart": state["regularSchedule"]["nextStart"],
                    "nextEnd": state["regularSchedule"]["nextEnd"],
                    "period": state["regularSchedule"]["period"],
                }
                for actor, state in before["actors"].items()
            },
            "actualTurnStartsOrEndsDuringCandidateInterval": 0,
            "budgetReset": False,
            "scheduleRebased": False,
            "deadlineMapping": {
                "actor": "A",
                "preservedVirtualMarker": marker,
                "baselineInitiativeCoordinate": before["time"],
                "baselineWorldElapsedSeconds": before["clock"]["elapsedSeconds"],
                "derivedWorldElapsedDeadline": deadline_world,
                "derivation": "baselineWorldElapsedSeconds + (preservedVirtualMarker - lastInitiativeCoordinate)",
            },
        },
        "transitions": transitions,
        "after": after_interval,
        "sourceClockObligations": {
            "worldElapsedSeconds": [before["clock"]["elapsedSeconds"], after_interval["clock"]["elapsedSeconds"]],
            "OpeningRemaining": [before["clock"]["OpeningRemaining"], after_interval["clock"]["OpeningRemaining"]],
            "HornRemaining": [before["clock"]["HornRemaining"], after_interval["clock"]["HornRemaining"]],
            "FortressSource": "remains active and permanent in the full effects/spaces state; no rest renews or recreates it.",
            "otherActors": "B, C and D remain present with their complete inherited actor records and unchanged regularSchedule markers.",
        },
        "requiredToSealW03": [
            "Bind an accepted operative short-rest definition establishing minimum duration and applicable activity/interruption conditions, or submit a separately reviewed NEW eligibility rule.",
            "Director must adjudicate the 3600-second candidate against that authority; the RP settlement remains unapplied until then.",
        ],
        "disposition": {
            "acceptedIds": [],
            "appliedIds": [],
            "heldIds": ["conjure-demiplane-fortress"],
            "blockerIds": ["PG200-B06"],
            "closedBlockerIds": [],
            "applicationAuthorized": False,
        },
    }
    fixture_path = PAYLOAD / "fixtures" / FIXTURE_NAME
    write_json(fixture_path, fixture)

    coverage_path = PAYLOAD / "COVERAGE_MAP_366.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8-sig"))
    coverage["id"] = "PG200-B06_COVERAGE_MAP_367"
    coverage["newWitnessParts"] = [
        "PG328-W03 TEST_ONLY short-rest candidate with complete inherited state, explicit outside-initiative clock bridge, source-deadline processing, full inventory and reversible scoped replay; rest eligibility remains unadjudicated."
    ]
    coverage["priorDirectorReview"] = {
        "reviewedIntake": "366",
        "decision": "HOLD",
        "sealedWitnessIds": [],
        "residualIds": ["PG366-W03-R1", "PG366-W03-R2", "PG366-W03-R3", "PG366-W03-R4", "PG366-M01"],
        "revision367AddressedForFreshReview": ["PG366-W03-R2", "PG366-W03-R3", "PG366-W03-R4", "PG366-M01"],
        "stillUnresolved": ["PG366-W03-R1"],
    }
    for witness in coverage["witnessParts"]:
        if witness["witnessPartId"] == "PG328-W03":
            witness["priorRemainingGap"] = "No accepted operative short-rest definition supplies minimum duration and activity/interruption criteria; W03 remains unsealed."
            witness["priorMinimumWitness"] = "Extend the exact complete inherited Return284 final state, actors, inventory, schedules, effects and clocks. Use a source-supported mode bridge preserving virtual deadlines, represent physical supplies and consumption in inventory, and supply deterministic state hashes with scoped reversible patches. Bind a qualifying short-rest rule before applying RP recovery; an arithmetic-only candidate does not seal W03."
            witness["availableSources"] = [
                "fixtures/" + FIXTURE_NAME,
                "sources/PLAYER_RULEBOOK_V6_SOURCE_TEXT.txt#line=8391",
                "sources/COMBAT_ACTION_PLAYTEST.md#line=47",
                "rules/PG328_PROCEDURE_CURRENT.json#/sharedContract/clocks",
            ]
            witness["intakeFinding"] = "Revision367 carries the full inherited state and clocks, inventory fork, virtual deadline, deterministic hashes, and reversible scoped patches; accepted numeric rest eligibility is still absent, so the conditional RP settlement is not applied."
            witness["status"] = "OPEN"
    coverage_path.unlink()
    coverage_path = PAYLOAD / "COVERAGE_MAP_367.json"
    write_json(coverage_path, coverage)

    old_readme = PAYLOAD / "README.md"
    readme = """# Conjure Demiplane Fortress / PG200-B06 closure intake 367

This revision resubmits the Fortress closure intake after GPT's review of Intake366. It keeps the identity and Banishment Gate held and introduces no acceptance, application, campaign event, runtime implementation, or canonical change.

The W03 TEST_ONLY candidate now extends the complete preserved Return284 branch state. A reversible inventory fork adds one mundane ration and one water container as explicit conditional inputs; the fixture retains actors A/B/C/D, all inherited items/effects/spaces/history/schedules, and the active Fortress. It uses the operative outside-initiative elapsed-time mode, preserves existing virtual schedule markers, expires A's carried spell-efficiency effect at its inherited deadline, and advances world, Opening and Horn clocks 1:1. Every state transition has deterministic SHA-256 before/after hashes and scoped forward/inverse patches.

The bound sources support ordinary short-rest arithmetic (80/4 + INT modifier 5 = 25; 54 would become 79 if eligible) and Retune's Dissonance reset. They do not establish a numeric minimum short-rest duration. The 3,600-second candidate is therefore UNADJUDICATED, no RP or rest counter update is applied, and PG328-W03 remains open pending an accepted rest definition or a separately reviewed new eligibility rule.

The ZIP has 37 unique archive members: 36 manifest payload files and the self-excluded manifest. See the delivery JSON and independent audit for hashes and replay checks. All 13 Fortress witness parts remain open.
"""
    old_readme.unlink()
    (PAYLOAD / "README.md").write_text(readme, encoding="utf-8")

    manifest_path = PAYLOAD / "MANIFEST_366.json"
    if manifest_path.exists():
        manifest_path.unlink()
    payload_files = sorted(p for p in PAYLOAD.rglob("*") if p.is_file())
    manifest_members = [
        {
            "path": path.relative_to(PAYLOAD).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": file_digest(path),
        }
        for path in payload_files
    ]
    manifest = {
        "id": "PG200-B06_CLOSURE_INTAKE_367",
        "schemaVersion": 1,
        "payloadFileCount": len(manifest_members),
        "selfExcluded": True,
        "members": manifest_members,
    }
    if len(manifest_members) != 36:
        raise AssertionError(f"Expected 36 payload files, found {len(manifest_members)}")
    write_json(PAYLOAD / "MANIFEST_367.json", manifest)

    archive_path = OUTPUT / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in PAYLOAD.rglob("*") if p.is_file()):
            rel = path.relative_to(PAYLOAD).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(2026, 10, 31, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive_path) as zf:
        if zf.testzip() is not None:
            raise AssertionError("The generated ZIP failed CRC testing.")
        names = zf.namelist()
        if len(names) != 37 or len(names) != len(set(names)):
            raise AssertionError(f"Expected 37 unique archive members, got {len(names)}")
        verified_manifest = json.loads(zf.read("MANIFEST_367.json"))
        for member in verified_manifest["members"]:
            data = zf.read(member["path"])
            if len(data) != member["bytes"] or hashlib.sha256(data).hexdigest() != member["sha256"]:
                raise AssertionError(f"Manifest verification failed for {member['path']}")

    fixture_hash = digest(fixture)
    audit = {
        "id": "PG200-B06_CLOSURE_INTAKE_367_INDEPENDENT_AUDIT",
        "archiveFile": ARCHIVE_NAME,
        "archiveBytes": archive_path.stat().st_size,
        "archiveSha256": file_digest(archive_path),
        "archiveUniqueMembers": 37,
        "manifestPayloadFilesVerified": 36,
        "zipTest": "PASS",
        "payloadHashes": "PASS",
        "sourceBindings": "PASS; all exact hashes and JSON/text locators resolve",
        "coverageMapParts": 13,
        "fixture": {
            "file": "fixtures/" + FIXTURE_NAME,
            "sha256CanonicalJson": fixture_hash,
            "parentBaselineFinalStateSha256": baseline["finalSHA256"],
            "forkBeforeStateSha256": digest(before),
            "finalStateSha256": digest(after_interval),
            "parentStateAndTestInventoryForkReversesExactly": True,
            "actorsPreserved": sorted(before["actors"]),
            "inventoryCountBeforeFork": len(parent_state["items"]),
            "inventoryCountAtCandidateRest": len(before["items"]),
            "supplyItems": [ration_id, water_id],
            "supplyQuantitiesRemainExplicit": True,
            "supplyConsumptionClaimed": False,
            "transitionCount": len(transitions),
            "transitionStateHashes": "PASS",
            "forwardReplay": "PASS",
            "inverseReplayExactRestoration": "PASS",
            "changedJsonPatchPaths": [
                sorted({op.get("path") for event in transitions for op in event["forward"] if op["op"] != "test"})
            ][0],
            "modeBridge": "PASS; operative outside-initiative elapsed clock; all inherited regularSchedule markers preserved",
            "virtualDeadline": {
                "scheduleMarker": marker,
                "worldElapsedSeconds": deadline_world,
                "effectExpired": after_virtual_deadline["actors"]["A"]["spellEfficiency"] is None,
            },
            "testOnlyIntervalSeconds": 3600,
            "durationQualification": "UNADJUDICATED_TEST_ONLY_INPUT",
            "conditionalOrdinaryRPRecovery": 25,
            "RPBefore": 54,
            "RPAfterIfQualified": 79,
            "RPSettlementApplied": False,
            "shortRestsSinceLongAtEnd": after_interval["actors"]["A"]["shortRestsSinceLong"],
            "ArcaneRecoveryUsed": after_interval["actors"]["A"]["arcaneRecoveryUsed"],
            "worldClockAdvanceSeconds": after_interval["clock"]["elapsedSeconds"] - before["clock"]["elapsedSeconds"],
            "OpeningClockAdvanceSeconds": before["clock"]["OpeningRemaining"] - after_interval["clock"]["OpeningRemaining"],
            "HornClockAdvanceSeconds": before["clock"]["HornRemaining"] - after_interval["clock"]["HornRemaining"],
            "FortressPersists": after_interval["effects"][next(iter(after_interval["effects"]))]["active"],
        },
        "priorDirectorFindings": {
            "PG366-W03-R1": "UNRESOLVED: accepted operative rest definition with minimum duration and activity/interruption conditions is absent.",
            "PG366-W03-R2": "Revised for fresh review: complete inherited state, actors, inventory, schedules, effect and source-clock obligations are retained; mode bridge is explicit.",
            "PG366-W03-R3": "Revised for fresh review: every transition has deterministic hashes and scoped reversible patches with exact restoration.",
            "PG366-W03-R4": "Revised for fresh review: source locators are split and resolvable; source hashes match.",
            "PG366-M01": "Corrected: payload count is 36; total ZIP members are 37 including the self-excluded manifest.",
        },
        "limitations": [
            "No accepted rest-duration or eligibility source is supplied.",
            "The candidate interval and supply inventory are TEST_ONLY premises, not campaign facts.",
            "No recovery or short-rest counter change is applied while eligibility is unadjudicated.",
            "No W03 or other witness part is claimed sealed by Intake367.",
        ],
        "authorityAssertions": {
            "fortressAcceptedIds": [],
            "fortressAppliedIds": [],
            "applicationAuthorized": False,
            "banishmentGateHeld": True,
        },
    }
    write_json(OUTPUT / AUDIT_NAME, audit)

    delivery = {
        "id": "PG200-B06_CLOSURE_INTAKE_367_DELIVERY",
        "targetId": "conjure-demiplane-fortress",
        "blockerIds": ["PG200-B06"],
        "supersedes": "PG200-B06_CLOSURE_INTAKE_366",
        "archive": {
            "fileName": ARCHIVE_NAME,
            "bytes": archive_path.stat().st_size,
            "sha256": file_digest(archive_path),
        },
        "payloadMemberCount": 36,
        "archiveMemberCount": 37,
        "requestedDirectorAction": "Re-review Intake367. Freshly check the full inherited W03 state, source-preserving mode bridge, virtual deadline, inventory, state hashes/scoped inverse replay, corrected source locators and corrected count. Keep W03 and Fortress held unless each required predicate is source-qualified; identify any remaining paths.",
        "priorDirectorDisposition": {
            "intake": "366",
            "decision": "HOLD",
            "sealedWitnessIds": [],
            "addressedForFreshReview": ["PG366-W03-R2", "PG366-W03-R3", "PG366-W03-R4", "PG366-M01"],
            "unresolved": ["PG366-W03-R1"],
        },
        "disposition": {
            "decision": "HOLD_PENDING_DIRECTOR_REVIEW",
            "acceptedIds": [],
            "appliedIds": [],
            "heldIds": ["conjure-demiplane-fortress"],
            "applicationAuthorized": False,
        },
        "preservation": {
            "banishmentGate": "HOLD",
            "blockerIds": ["PG200-B03", "PG200-B04"],
            "acceptedIds": [],
            "appliedIds": [],
            "applicationAuthorized": False,
            "runtimeEnabled": False,
            "canonicalChanges": False,
            "priorWitnessSealsPreserved": ["W05", "W06", "W07", "W08"],
        },
        "queue361": {
            "applied": 828,
            "pending": 20,
            "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 552,
            "scopedInterfaces": 173,
            "firstReviewsRemaining": 0,
            "closureTasksRemaining": 20,
        },
    }
    write_json(OUTPUT / DELIVERY_NAME, delivery)

    # Final package-level semantic assertions.
    if len(coverage["witnessParts"]) != 13 or any(w["status"] != "OPEN" for w in coverage["witnessParts"]):
        raise AssertionError("Coverage map no longer preserves the 13 open witness parts.")
    if after_interval["actors"]["A"]["RP"] != 54 or after_interval["actors"]["A"]["shortRestsSinceLong"] != 0:
        raise AssertionError("Unadjudicated recovery was incorrectly applied.")
    if after_interval["actors"]["A"]["arcaneRecoveryUsed"] is not False:
        raise AssertionError("Arcane Recovery must remain unused.")
    if after_interval["clock"]["elapsedSeconds"] != 3601.0:
        raise AssertionError("Candidate interval clock endpoint mismatch.")
    if digest(parent_state) != inventory_overlay["parentStateSHA256"]:
        raise AssertionError("Fork parent state hash changed unexpectedly.")
    print(json.dumps({
        "output": str(OUTPUT),
        "archive": str(archive_path),
        "archiveBytes": archive_path.stat().st_size,
        "archiveSha256": file_digest(archive_path),
        "payloadFiles": 36,
        "archiveMembers": 37,
        "parentStateHash": baseline["finalSHA256"],
        "forkStateHash": digest(before),
        "finalStateHash": digest(after_interval),
        "transitions": len(transitions),
        "restEligibility": "UNADJUDICATED",
        "RPSettlementApplied": False,
        "allWitnessParts": "OPEN",
    }, indent=2))


if __name__ == "__main__":
    main()
