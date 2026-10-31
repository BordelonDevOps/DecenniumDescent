from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import pathlib
import subprocess
import sys
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUTPUT = AUDIT / "rank9_nullification_wave_closure355_delivery"
SOURCE_REPORT = AUDIT / "NULLIFICATION_WAVE_FORGE_BRANCH_REPLAY_355.json"
SUPPLEMENT = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255/SUPPLEMENT255_W2.json"
FORGE_MODEL = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255/MODEL.json"
FORGE_ACCEPTANCE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255/EXACT_ACCEPTANCE.json"
FORGE_DIRECTOR_ACCEPTANCE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255/DIRECTOR_ACCEPTANCE.json"
RETURN247 = AUDIT / "rank9_materialforging2_return247_received/DD_Rank9_MaterialForging2_Director_Return247_HELD.zip"
RETURN281 = AUDIT / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
QUEUE354 = AUDIT / "CURRENT_SPELL_QUEUE_354.json"
PENDING354 = AUDIT / "CURRENT22_PENDING_IDENTITY_AUDIT_354.json"
HANDOFF354 = AUDIT / "CURRENT_HANDOFF_354.json"
TARGET = "nullification-wave"
BLOCKER = "WC188-B01"
CASTER = "WC355"
CAST_ID = "WC355-NW:cast1"
SCOPE_IDS = [
    "alignment-ascension", "alignment-perfection", "astral-projection", "banishment-gate",
    "collapse-timeline", "conjure-demiplane-fortress", "corruption-purification",
    "divine-intervention-greater", "elemental-shell", "eternal-prophecy", "faction-incarnate",
    "faction-omniscience-supreme", "faction-perfection", "fate-rewrite", "final-word",
    "imprisonment", "invulnerable-sphere", "nullification-wave", "reverse-gravity-field",
    "summon-avatar-of-decay", "summon-herald-of-the-planes", "wish",
]
PRIORITY_ORDER = [
    "nullification-wave", "summon-herald-of-the-planes", "banishment-gate",
    "conjure-demiplane-fortress", "invulnerable-sphere", "elemental-shell", "final-word",
    "summon-avatar-of-decay", "reverse-gravity-field", "eternal-prophecy", "fate-rewrite",
    "collapse-timeline", "faction-omniscience-supreme", "alignment-ascension",
    "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification",
    "astral-projection", "imprisonment", "divine-intervention-greater", "wish",
]
BLOCKERS = {
    "nullification-wave": ["WC188-B01"],
    "summon-herald-of-the-planes": ["SH202-B02"],
    "banishment-gate": ["PG200-B03", "PG200-B04"],
    "conjure-demiplane-fortress": ["PG200-B06"],
    "invulnerable-sphere": ["DF218-B04"],
    "elemental-shell": ["DF218-B01", "DF218-B02"],
    "final-word": ["DR217-B01"],
    "summon-avatar-of-decay": ["SH202-B03"],
    "reverse-gravity-field": ["IE204-B02"],
    "eternal-prophecy": ["TF192-B02"],
    "fate-rewrite": ["TF192-B04", "TF192-B02"],
    "collapse-timeline": ["TF192-B05", "TF192-B02"],
    "faction-omniscience-supreme": ["KR198-B01", "KR326-C01"],
    "alignment-ascension": ["AFP211-B01"],
    "alignment-perfection": ["AFP211-B02"],
    "faction-incarnate": ["AFP211-B03"],
    "faction-perfection": ["AFP211-B04"],
    "corruption-purification": ["AFP211-B05"],
    "astral-projection": ["PC232-B01"],
    "imprisonment": ["PC232-B02"],
    "divine-intervention-greater": ["MR233-B01"],
    "wish": ["MR233-B02"],
}


def canon(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def state_hash(value: object) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def ptr(parts: tuple[str, ...]) -> str:
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def diff(before: object, after: object, path: tuple[str, ...] = ()) -> list[dict]:
    if isinstance(before, dict) and isinstance(after, dict):
        operations: list[dict] = []
        for key in sorted(before.keys() - after.keys()):
            operations += [{"op": "test", "path": ptr(path + (key,)), "value": before[key]},
                           {"op": "remove", "path": ptr(path + (key,))}]
        for key in sorted(after.keys() - before.keys()):
            operations.append({"op": "add", "path": ptr(path + (key,)), "value": after[key]})
        for key in sorted(before.keys() & after.keys()):
            operations += diff(before[key], after[key], path + (key,))
        return operations
    if before == after:
        return []
    p = ptr(path) if path else ""
    return [{"op": "test", "path": p, "value": before}, {"op": "replace", "path": p, "value": after}]


def path_parts(path: str) -> list[str]:
    if path == "":
        return []
    return [part.replace("~1", "/").replace("~0", "~") for part in path[1:].split("/")]


def get_path(document: object, path: str) -> object:
    node = document
    for part in path_parts(path):
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def parent_path(document: object, parts: list[str]) -> tuple[object, str]:
    node = document
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node, parts[-1]


def apply_ops(document: object, operations: list[dict]) -> object:
    for operation in operations:
        op, path = operation["op"], operation["path"]
        parts = path_parts(path)
        if op == "test":
            assert get_path(document, path) == operation["value"], path
            continue
        if not parts:
            assert op == "replace"
            document = copy.deepcopy(operation["value"])
            continue
        parent, key = parent_path(document, parts)
        if op == "replace":
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                parent[key] = copy.deepcopy(operation["value"])
        elif op == "add":
            if isinstance(parent, list):
                parent.insert(len(parent) if key == "-" else int(key), copy.deepcopy(operation["value"]))
            else:
                parent[key] = copy.deepcopy(operation["value"])
        elif op == "remove":
            if isinstance(parent, list):
                parent.pop(int(key))
            else:
                del parent[key]
        else:
            raise AssertionError(f"unsupported operation {op}")
    return document


def load(path: pathlib.Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    replay_report = load(SOURCE_REPORT)
    assert replay_report["status"] == "PASS_EXACT_SOURCE_ARCHIVE_REPLAY_TO_PRE_E20_SNAPSHOT"
    state = copy.deepcopy(replay_report["preE20SnapshotState"])
    base_hash = state_hash(state)
    assert base_hash == replay_report["preE20Snapshot"]["stateSHA256"]
    assert state["time"] == 172800.4
    assert state["items"]["bracelet-1"]["imprintRoot"]["id"] == "castF2"
    assert state["items"]["bracelet-1"]["imprintRoot"]["active"] is True
    assert state["actors"]["A"]["profile"]["class"] == "Wizard"
    assert "counterspell" not in state["actors"]["A"]["profile"].get("prepared", [])
    assert state["actors"]["B"]["profile"]["class"] is None
    active_roots = sorted(
        (item_id, item["imprintRoot"]["id"])
        for item_id, item in state["items"].items()
        if item.get("imprintRoot", {}).get("active") is True
    )
    assert active_roots == [("bracelet-1", "castF2")]
    assert state["pendingCasts"] == {}
    assert all(actor.get("concentration") is None for actor in state["actors"].values())
    assert not any(row.get("status") == "active" for row in state["supplement"].get("activeEffects", {}).values())

    with zipfile.ZipFile(RETURN247) as source247:
        base_case_raw = source247.read("cases/MF210-F02.json")
        base_case = json.loads(base_case_raw)
    with zipfile.ZipFile(RETURN281) as source281:
        actor_profiles_raw = source281.read("ACTOR_PROFILES.json")
        actor_profiles = json.loads(actor_profiles_raw)
        wave_case_raw = source281.read("cases/return237/preserved/WC219-NW-FORM.json")
        wave_case = json.loads(wave_case_raw)
        wave_proc_raw = source281.read("procedures/nullification-wave.json")
        wave_proc = json.loads(wave_proc_raw)
        case_index_raw = source281.read("CASE_INDEX.json")
        case_index = json.loads(case_index_raw)
        qualifications_raw = source281.read("QUALIFICATIONS.json")
        qualifications = json.loads(qualifications_raw)
        historical_wave_cases = [row for row in case_index["cases"] if row.get("spellId") == TARGET]
        assert len(historical_wave_cases) == 18
        historical_case_digests = []
        for row in historical_wave_cases:
            raw = source281.read(row["path"])
            observed = digest(raw)
            assert all(observed[k] == row[k] for k in ("bytes", "sha256"))
            historical_case_digests.append({"id": row["id"], "bytes": observed["bytes"], "sha256": observed["sha256"]})

    profile = actor_profiles["W219"]
    original_actor = copy.deepcopy(wave_case["initialState"]["actors"]["C"])
    wave_cast_event = wave_case["events"][9]
    assert wave_cast_event["id"] == "WC219-NW-FORM:10"
    assert wave_cast_event["kind"] == "paid-cast-commitment"
    assert "nullification-wave" in profile["ordinaryRepertoire"]
    level17_wave = [entry for entry in profile["spellbook"] if entry["spellId"] == TARGET and entry["level"] == 17]
    assert len(level17_wave) == 1
    assert profile["class"] == "Wizard" and profile["classLevel"] == 18 and profile["maximumRP"] == 68
    assert original_actor["profile"] == "ACTOR_PROFILES.json#/W219"
    assert original_actor["RP"] == 68 and original_actor["class"] == "Wizard"
    assert original_actor["gear"][0]["id"] == "C-focus" and original_actor["gear"][0]["state"] == "held"

    source_digests = {
        "return247Archive": digest(RETURN247.read_bytes()),
        "return247CaseMember": digest(base_case_raw),
        "supplement255W2": digest(SUPPLEMENT.read_bytes()),
        "forgeModel": digest(FORGE_MODEL.read_bytes()),
        "forgeExactAcceptance": digest(FORGE_ACCEPTANCE.read_bytes()),
        "forgeDirectorAcceptance": digest(FORGE_DIRECTOR_ACCEPTANCE.read_bytes()),
        "return281Archive": digest(RETURN281.read_bytes()),
        "actorProfilesMember": digest(actor_profiles_raw),
        "waveCaseMember": digest(wave_case_raw),
        "waveProcedureMember": digest(wave_proc_raw),
        "caseIndexMember": digest(case_index_raw),
        "qualificationsMember": digest(qualifications_raw),
    }
    current_source_bindings = []
    local_sources = [
        ("SUPPLEMENT255_W2.json", SUPPLEMENT),
        ("ETERNAL_FORGE_MODEL.json", FORGE_MODEL),
        ("ETERNAL_FORGE_EXACT_ACCEPTANCE.json", FORGE_ACCEPTANCE),
        ("ETERNAL_FORGE_DIRECTOR_ACCEPTANCE.json", FORGE_DIRECTOR_ACCEPTANCE),
    ]
    for label, path in local_sources:
        current_source_bindings.append({"label": label, "path": path.relative_to(ROOT).as_posix(), **digest(path.read_bytes())})
    current_source_bindings += [
        {"label": "Return247 source archive", "path": RETURN247.relative_to(ROOT).as_posix(), **source_digests["return247Archive"]},
        {"label": "Return247 exact base case member", "containerPath": RETURN247.relative_to(ROOT).as_posix(), "member": "cases/MF210-F02.json", **source_digests["return247CaseMember"]},
        {"label": "Return281 historical source archive", "path": RETURN281.relative_to(ROOT).as_posix(), **source_digests["return281Archive"]},
        {"label": "Return281 W219 profile", "containerPath": RETURN281.relative_to(ROOT).as_posix(), "member": "ACTOR_PROFILES.json#/W219", **source_digests["actorProfilesMember"]},
        {"label": "Return281 paid Wave precedent", "containerPath": RETURN281.relative_to(ROOT).as_posix(), "member": "cases/return237/preserved/WC219-NW-FORM.json", **source_digests["waveCaseMember"]},
        {"label": "Return281 Wave procedure", "containerPath": RETURN281.relative_to(ROOT).as_posix(), "member": "procedures/nullification-wave.json", **source_digests["waveProcedureMember"]},
    ]

    created_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    actor = copy.deepcopy(original_actor)
    actor["id"] = CASTER
    actor["profile"] = "ACTOR_PROFILES.json#/W219"
    actor["preparedSpells"] = copy.deepcopy(profile["ordinaryRepertoire"])
    actor["position"] = [10, 0, 0]
    actor["RP"] = 68
    actor["maximumHP"] = actor["HP"] = 110
    actor["castHistory"] = []
    actor["lastSpell"] = None
    actor["concentration"] = None
    actor["conditions"] = []
    actor["Dissonance"] = 0
    actor["Refrain"] = 0
    actor["families"] = []
    actor["resourceHistory"] = []
    actor["actionHistory"] = []
    actor["reactionHistory"] = []
    actor["readyHistory"] = []
    actor["turnHistory"] = []
    actor["budget"].update({"Action": 0, "BonusAction": 1, "Reaction": 1, "movementSpent": 0, "companionCommandSpent": False})
    actor["regular"] = {"starts": [], "ends": [], "nextStart": 172800.6, "nextEnd": None, "phase": 172800.6}
    actor["gear"] = copy.deepcopy(actor["gear"])
    for slot, item in enumerate(actor["gear"]):
        item["id"] = f"{CASTER}-gear-{slot + 1}"
        item["owner"] = CASTER
        item["custodian"] = CASTER
    actor["book"] = copy.deepcopy(actor["book"])
    actor["book"].update({"id": f"{CASTER}-primary-book", "custodian": CASTER, "source": "W219 profile legal level-up choices; TEST_ONLY fixture instance"})
    actor["fixtureQualification"] = "TEST_ONLY clone of the source-bound W219 Wizard profile; new local actor identifier; no campaign character identity or acquisition is claimed."

    events: list[dict] = []

    def add_event(event_id: str, kind: str, at: float, description: str, source_refs: list[str], mutate) -> None:
        before = copy.deepcopy(state)
        mutate(state)
        state["time"] = at
        if event_id not in state["processedEvents"]:
            state["processedEvents"].append(event_id)
        after = copy.deepcopy(state)
        forward = diff(before, after)
        inverse = diff(after, before)
        assert apply_ops(copy.deepcopy(before), forward) == after
        assert apply_ops(copy.deepcopy(after), inverse) == before
        events.append({
            "id": event_id,
            "kind": kind,
            "timeSeconds": at,
            "description": description,
            "sourceRefs": source_refs,
            "beforeSHA256": state_hash(before),
            "afterSHA256": state_hash(after),
            "beforeState": before,
            "afterState": after,
            "forward": forward,
            "inverse": inverse,
        })

    def admit_caster(s: dict) -> None:
        assert CASTER not in s["actors"]
        s["actors"][CASTER] = copy.deepcopy(actor)
        s["scene"]["waveClosure355"] = {
            "classification": "TEST_ONLY_AUTHORED_CONDITIONAL_BRANCH_NOT_CAMPAIGN_EVIDENCE",
            "encounterId": "WC355-NW-FORGE-ENCOUNTER",
            "branchParentEvent": "MF247-F-W2-E20-PAID-GREATER-DISPEL.before",
            "branchParentStateSHA256": base_hash,
            "participants": ["A", "B", CASTER],
            "initiativeOrder": ["B", "A", CASTER],
            "initiativeInputs": {
                "B": {"sourceEvent": "MF210-W2-ENDING-AND-RECREATION", "total": 18},
                "A": {"sourceEvent": "MF210-W2-ENDING-AND-RECREATION", "total": 12},
                CASTER: {"authoredTestInput": {"d20": 8, "DEX": 2, "total": 10}, "sourceProfile": "ACTOR_PROFILES.json#/W219"},
            },
            "firstCasterTurnAtSeconds": 172800.6,
            "casterPositionFeet": [10, 0, 0],
            "perceivedFixedCenterFeet": [10, 0, 0],
            "rangeToCenterFeet": 0,
            "lineOfEffectToCenter": "unobstructed; center is caster's own occupied origin in the declared test scene",
            "radiusFeet": 60,
            "captureShape": "closed three-dimensional sphere; immutable initial-cover snapshot; no rescan",
            "sceneWallsAtSnapshot": copy.deepcopy(s["scene"].get("walls", [])),
            "activeEffectScan": {
                "activeItemRoots": [{"itemId": item_id, "rootId": root_id} for item_id, root_id in active_roots],
                "pendingCasts": copy.deepcopy(s.get("pendingCasts", {})),
                "activeConcentrations": [actor_id for actor_id, existing in s["actors"].items()
                                          if existing.get("concentration") is not None],
                "activeEffectRegistryRows": [{"id": effect_id, **copy.deepcopy(effect)}
                                             for effect_id, effect in s["supplement"].get("activeEffects", {}).items()
                                             if effect.get("status") == "active"],
            },
            "authoredTestSceneWalls": [{
                "id": "WC355-TEST-OPAQUE-WALL-1",
                "classification": "TEST_ONLY_LOCAL_GEOMETRY_NOT_CAMPAIGN_FACT",
                "boxFeet": [[20, -5, 0], [20.5, 5, 10]],
                "material": "opaque solid total-cover test premise",
            }],
            "itemAnchorFeet": copy.deepcopy(s["items"]["bracelet-1"]["positionBoxFeet"]),
            "itemAnchorDistanceFeet": math.sqrt((10 - 2.5) ** 2 + (0 - 0) ** 2 + (0 - 3) ** 2),
            "itemLineOfEffectFromSourceScene": "source scene says unblocked to bracelet; adjacent opaque hide cover does not block line of effect to bracelet",
            "initialCoverClipsTarget": False,
            "volumeClippedByCover": True,
            "coveredSamplePointFeet": [25, 0, 3],
            "coveredSampleDistanceFeet": math.sqrt((25 - 10) ** 2 + (0 - 0) ** 2 + (3 - 0) ** 2),
            "coveredSampleExcludedByInitialCover": True,
            "actionReactionReadyLedger": {
                "classification": "complete scoped encounter ledger; source state at branch plus authored test transitions",
                "branchOpening": {
                    "B": {"initiative": 18, "regularStart": 172800.2, "Action": 0, "Reaction": 1, "ready": None, "slot": "passed without action before branch boundary"},
                    "A": {"initiative": 12, "regularStart": 172800.4, "Action": 1, "Reaction": 1, "ready": None, "slot": "current turn at branch boundary"},
                    CASTER: {"initiative": 10, "regularStart": None, "Action": 0, "Reaction": 1, "ready": None, "slot": "not yet started"},
                },
                "events": [],
            },
            "eligibleCounterResponders": [],
            "readyActions": [],
            "noOtherActiveRootAtSnapshot": True,
            "authorizedTestInputs": {
                "observerDC": 13,
                "postEndStealthD20": 10,
                "classification": "explicit authored finite test values; never observed play or campaign facts",
            },
        }
        s["supplement"]["waveWitness355"] = {
            "id": "WC355-NW-FORGE-ENCOUNTER",
            "status": "AUTHORED_TEST_ONLY_BRANCH; DIRECTOR_REVIEW_PENDING",
            "branchParentEvent": "MF247-F-W2-E20-PAID-GREATER-DISPEL.before",
            "branchParentStateSHA256": base_hash,
            "sourceBindings": current_source_bindings,
            "originalRootId": "castF2",
            "targetItemId": "bracelet-1",
            "originalCampaignClaims": False,
            "newlyAuthoredFixtureInputs": ["WC355 test caster instance", "WC355 initiative d20", "Wave center/origin", "observer DC13", "post-end d20 10"],
            "castRecords": [],
            "counterWindows": [],
            "captureRecords": [],
            "postTerminationFunctionChecks": [],
            "eventLedger": [],
        }

    add_event("WC355-NW-E01-ADMIT-CASTER", "test-fixture-caster-and-geometry-admission", 172800.4,
              "Add a distinct Wizard fixture from the W219 source profile. Keep Forge actor A and W219-derived WC355 separate; do not modify the historical pre-E20 event stream.",
              ["Return281:ACTOR_PROFILES.json#/W219", "Return281:cases/return237/preserved/WC219-NW-FORM.json#/initialState/actors/C", "SUPPLEMENT255_W2.json#eventReplay.branches[0].events[19].beforeSHA256"], admit_caster)

    def end_a_turn(s: dict) -> None:
        s["scene"]["waveClosure355"]["turnEndLedger"] = [{"actor": "A", "atSeconds": 172800.6, "unusedActionExpired": True, "reactionSpent": False, "readyExpired": False}]
        s["actors"]["A"]["Action"] = 0
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172800.6, "actor": "A", "type": "regular-turn-end",
            "ActionBefore": 1, "ActionAfter": 0, "ReactionAvailable": 1,
            "readyBefore": None, "readyAfter": None, "actions": [],
        })
        s["actors"]["A"]["ready"] = None

    add_event("WC355-NW-E02-A-PASS-TO-W219-SLOT", "regular-turn-end-no-action", 172800.6,
              "Actor A takes no Action between the exact E19 start and the next lower-initiative WC355 slot; the prior action budget expires as its turn ends.",
              ["SUPPLEMENT255_W2.json#MF247-F-W2-E19-A-START-FOR-DISPEL", "Return281:W219 initiative and actor source"], end_a_turn)

    def start_c_turn(s: dict) -> None:
        c = s["actors"][CASTER]
        c["regular"]["starts"].append(172800.6)
        c["regular"]["nextStart"] = 172806.6
        c["budget"].update({"Action": 1, "BonusAction": 1, "Reaction": 1, "movementSpent": 0, "companionCommandSpent": False})
        c["turnStartHistory"] = [{"atSeconds": 172800.6, "Action": 1, "BonusAction": 1, "Reaction": 1}]
        c["turnHistory"].append({"atSeconds": 172800.6, "phase": "start", "Action": 1, "Reaction": 1, "ready": None})
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172800.6, "actor": CASTER, "type": "regular-turn-start",
            "Action": 1, "Reaction": 1, "ready": None,
        })

    add_event("WC355-NW-E03-W219-REGULAR-START", "regular-turn-start", 172800.6,
              "WC355 begins the next regular slot after A under the declared test initiative order B18>A12>WC355-10.",
              ["Return281:ACTOR_PROFILES.json#/W219", "WC355-NW-FORGE-ENCOUNTER initiativeInputs"], start_c_turn)

    def pay_wave(s: dict) -> None:
        c = s["actors"][CASTER]
        assert c["RP"] == 68 and c["budget"]["Action"] == 1 and c["Dissonance"] == c["Refrain"] == 0
        assert TARGET in c["preparedSpells"] and len(c["preparedSpells"]) == profile["preparedCount"]
        c["RP"] = 42
        c["budget"]["Action"] = 0
        c["lastSpell"] = TARGET
        c["castHistory"].append(CAST_ID)
        c["families"].append(TARGET)
        c["turnCast"] = True
        c["resourceHistory"].append({"castId": CAST_ID, "spell": TARGET, "timeSeconds": 172800.7,
                                      "resource": "RP", "before": 68, "paid": 26, "after": 42,
                                      "action": "Action", "actionBefore": 1, "actionAfter": 0,
                                      "components": {"V": True, "S": True, "F": True},
                                      "focusId": f"{CASTER}-gear-1", "focusHeld": True,
                                      "sourceCost": "Return281 WC9-Q01 and WC219 paid-cast precedent"})
        c["actionHistory"].append({"atSeconds": 172800.7, "action": "cast", "spellId": TARGET,
                                   "castId": CAST_ID, "spent": True, "remaining": 0})
        c["turnHistory"].append({"atSeconds": 172800.7, "phase": "action", "Action": 0, "Reaction": 1, "ready": None})
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172800.7, "actor": CASTER, "type": "paid-action",
            "ActionBefore": 1, "ActionAfter": 0, "ReactionAvailable": 1,
            "readyBefore": None, "readyAfter": None, "actions": ["cast Nullification Wave"],
        })
        cast = {
            "id": CAST_ID, "caster": CASTER, "class": "Wizard", "spellId": TARGET,
            "rank": 9, "accessSchool": "Abjuration", "baseRP": 26, "additionalRP": 0,
            "paidRP": 26, "paidAction": "Action", "components": ["V", "S", "F"],
            "preparationRecord": {"prepared": True, "preparedSetSource": "ACTOR_PROFILES.json#/W219/ordinaryRepertoire",
                                  "preparedSetCount": len(c["preparedSpells"]), "preparedCapacity": profile["preparedCapacity"]},
            "focusId": f"{CASTER}-gear-1", "focusHeld": True, "refrainBefore": 0,
            "dissonanceBefore": 0, "firstPreparedFamily": True, "paidAtSeconds": 172800.7,
            "centerFeet": [10, 0, 0], "rangeFeet": 60, "radiusFeet": 60,
            "targetSelection": "no creature target; immutable source capture resolves against active effects/components in the sphere",
            "save": None, "check": None, "concentrationAdded": False,
        }
        s["pendingCasts"][CAST_ID] = {"caster": CASTER, "spell": TARGET, "rank": 9, "paidRP": 26,
                                       "paidAction": "Action", "components": "V/S/F", "status": "committed",
                                       "origin": [10, 0, 0], "authorizationFrozen": {"centerFeet": [10, 0, 0], "radiusFeet": 60}}
        s["supplement"]["waveWitness355"]["castRecords"].append(cast)

    add_event("WC355-NW-E04-PAID-WAVE-COMMIT", "paid-cast-commitment", 172800.7,
              "WC355 spends one Action and the source-supported 26 RP base cost for prepared rank-9 Nullification Wave; the source focus is held and V/S/F are available. No refund path is asserted.",
              ["Return281:ACTOR_PROFILES.json#/W219 spellbook level17 nullification-wave", "Return281:cases/return237/preserved/WC219-NW-FORM.json#WC219-NW-FORM:10", "Return281:procedures/nullification-wave.json#WC9-Q01/Q06/Q07"], pay_wave)

    def record_counter_window(s: dict) -> None:
        s["supplement"]["waveWitness355"]["counterWindows"].append({
            "id": "WC355-NW-COUNTER-WINDOW-1", "atSeconds": 172800.75,
            "afterPaymentBeforeResolution": True,
            "responders": {
                "A": {"reactionAvailable": True, "preparedCounterspell": False, "preparedSet": copy.deepcopy(s["actors"]["A"]["profile"]["prepared"]), "response": "no eligible Counterspell"},
                "B": {"reactionAvailable": True, "class": None, "spellcasting": False, "response": "no eligible counter capability"},
                CASTER: {"reactionAvailable": True, "response": "caster is not a counter-responder to own cast"},
            },
            "reactionsSpent": [], "counterspellCast": False, "counterOutcome": "no eligible interruption; proceed to resolution",
        })
        for actor_id in ("A", "B", CASTER):
            participant = s["actors"][actor_id]
            available = participant["Reaction"] if actor_id in ("A", "B") else participant["budget"]["Reaction"]
            row = {"atSeconds": 172800.75, "windowId": "WC355-NW-COUNTER-WINDOW-1",
                   "availableBefore": available, "spent": False, "availableAfter": available,
                   "ready": participant.get("ready"), "response": "no eligible interruption; no Reaction spent"}
            if actor_id == CASTER:
                participant["reactionHistory"].append(row)
            s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
                "atSeconds": 172800.75, "actor": actor_id, "type": "counter-window-response", **row,
            })

    add_event("WC355-NW-E05-COUNTER-WINDOW", "paid-cast-interruption-window", 172800.75,
              "Record the real post-payment/pre-resolution window. A is not prepared with Counterspell; B has no spellcasting; no Reaction is spent.",
              ["Return281:procedures/nullification-wave.json#WC9-Q01", "pre-E20 actor A prepared set", "pre-E20 actor B noncasting profile"], record_counter_window)

    def resolve_wave(s: dict) -> None:
        item = s["items"]["bracelet-1"]
        root = item["imprintRoot"]
        assert root == {"id": "castF2", "rank": 9, "active": True, "suppressed": False}
        start_physical = {k: copy.deepcopy(v) for k, v in item.items() if k not in {"imprintRoot", "revision"}}
        root["active"] = False
        root["endReason"] = "Nullification Wave source-sigil ending"
        root["endedAtSeconds"] = 172800.8
        item["revision"] += 1
        assert start_physical == {k: copy.deepcopy(v) for k, v in item.items() if k not in {"imprintRoot", "revision"}}
        del s["pendingCasts"][CAST_ID]
        s["terminalCasts"][CAST_ID] = {
            "caster": CASTER, "spell": TARGET, "rank": 9, "paidRP": 26,
            "paidAction": "Action", "components": "V/S/F", "status": "resolved",
            "origin": [10, 0, 0], "authorizationFrozen": {"centerFeet": [10, 0, 0],
                "radiusFeet": 60, "capturedApplications": ["castF2"], "save": None, "check": None},
        }
        s["supplement"]["imprintEndings"].append({
            "rootId": "castF2", "physicalItemId": "bracelet-1", "eventId": CAST_ID,
            "timeSeconds": 172800.8, "procedure": "Nullification Wave source-sigil ending; one source-owned root only",
            "reason": "actual-paid-nullification-wave-capture", "physicalBodyPreserved": True,
            "owner": "A", "custodian": "B-right-wrist", "HP": 2, "charges": 0,
        })
        s["supplement"]["waveWitness355"]["captureRecords"].append({
            "eventId": "WC355-NW-E06-CAPTURE-END", "castId": CAST_ID,
            "centerFeet": [10, 0, 0], "radiusFeet": 60, "shape": "closed three-dimensional sphere",
            "initialCoverSnapshot": {
                "sceneWalls": copy.deepcopy(s["scene"]["waveClosure355"]["authoredTestSceneWalls"]),
                "braceletLineOfEffect": "unblocked", "targetClipped": False,
                "volumeClippedByCover": True,
                "coveredSample": {"pointFeet": [25, 0, 3], "distanceFeet": 15,
                                  "wallId": "WC355-TEST-OPAQUE-WALL-1", "excluded": True},
            },
            "capturedApplications": ["castF2"], "capturedComponents": [{"itemId": "bracelet-1", "componentId": "castF2", "anchorFeet": [2.5, 0, 3], "distanceFeet": math.sqrt(65.25)}],
            "noRescan": True, "save": None, "check": None, "GreaterDispelDC28Check": None,
            "endingAppliedExactlyOnce": True,
        })
        s["scene"]["waveClosure355"]["captureResult"] = {"captured": ["castF2"], "save": None, "check": None,
                                                               "GreaterDispelDC28Check": None, "postCaptureRescan": False}
        c = s["actors"][CASTER]
        c["regular"]["ends"].append(172800.8)
        c["turnHistory"].append({"atSeconds": 172800.8, "phase": "end", "Action": 0, "Reaction": 1, "ready": None})
        c["readyHistory"].append({"atSeconds": 172800.8, "declared": False, "expired": False})
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172800.8, "actor": CASTER, "type": "regular-turn-end-after-resolution",
            "Action": 0, "Reaction": 1, "ready": None,
        })

    add_event("WC355-NW-E06-CAPTURE-END", "immutable-wave-capture-and-source-owned-terminal-cleanup", 172800.8,
              "The initial 60-foot 3D sphere captures the exposed castF2 anchor on bracelet-1. End that Forge root once; no Wave save, rank check, or Greater Dispel DC28 roll is used. Preserve the item body and all separate histories.",
              ["Return281:procedures/nullification-wave.json#WC9-Q06/Q07/Q08", "accepted Eternal Forge MODEL.json#/spells/0/procedure/spellLocalNEW/permanence", "pre-E20 snapshot hash f02c265c02e1046278d53dc8b4945b0bd138edd3f70ae9ea9197c88dcd328eb0"], resolve_wave)

    def start_b_next(s: dict) -> None:
        b = s["actors"]["B"]
        b.update({"regularStart": 172806.2, "nextRegularStart": 172812.2, "Action": 1, "Reaction": 1,
                  "BonusAction": 1, "freeInteraction": 1, "movementRemaining": 30, "turnCast": False})
        b["regularStartsProcessed"].append(172806.2)
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.2, "actor": "B", "type": "regular-turn-start",
            "Action": 1, "Reaction": 1, "ready": None,
        })
        s["supplement"]["waveWitness355"]["eventLedger"].append({"kind": "B-regular-start", "atSeconds": 172806.2})

    add_event("WC355-NW-E07-B-NEXT-REGULAR-START", "regular-turn-start", 172806.2,
              "Advance through the exact next B slot; no refill, creation, repair, relocation, or unrecorded action occurs before it.",
              ["SUPPLEMENT255_W2.json#MF247-F-W2-E19-A-START-FOR-DISPEL.afterState actors/B.nextRegularStart", "SUPPLEMENT255_W2.json#dawn2 charge ledger"], start_b_next)

    def probe_stealth(s: dict) -> None:
        b = s["actors"]["B"]
        item = s["items"]["bracelet-1"]
        assert item["worn"] is True and "bracelet-1" in b["worn"] and item["HP"] == 2 and item["charges"] == 0
        assert item["imprintRoot"]["active"] is False and s["scene"].get("hideOpportunity", {}).get("eligibleDEXStealth") is True
        b["Action"] = 0
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.3, "actor": "B", "type": "paid-action",
            "action": "Hide", "ActionBefore": 1, "ActionAfter": 0,
            "ReactionAvailable": 1, "readyBefore": None, "readyAfter": None,
        })
        probe = {
            "id": "WC355-NW-POST-END-HIDE-PROBE", "atSeconds": 172806.3, "actor": "B",
            "action": "Hide", "actionSpent": True, "coverBinding": "source W2 scene hideOpportunity; legal cover; no movement",
            "check": "DEX (Stealth)", "d20": 10, "dexModifier": 2, "proficiencyBonus": 0,
            "braceletPassiveBonus": 0, "bonusIfCastF2WereStillActive": 1,
            "total": 12, "fixtureObserverDC": 13, "result": "not hidden",
            "chargeSpent": 0, "ordinaryAdornmentPersists": True,
            "authorship": "finite authored test roll and observer DC; not an observed campaign outcome",
        }
        s["supplement"]["waveWitness355"]["postTerminationFunctionChecks"].append(probe)
        s["supplement"]["waveWitness355"]["eventLedger"].append({"kind": "B-post-end-stealth-use", "atSeconds": 172806.3})

    add_event("WC355-NW-E08-POST-END-STEALTH-USE", "post-termination-mundane-body-and-lost-magic-probe", 172806.3,
              "B still wears the damaged steel bracelet. A legal Hide check receives no ended Forge imprint's passive +1; the finite authored d20/DC inputs make the loss testable while the ordinary adornment remains.",
              ["JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md#recipe-241", "pre-E20 item/custody and scene.hideOpportunity", "accepted Eternal Forge model spellLocalNEW.permanence"], probe_stealth)

    def end_b_turn(s: dict) -> None:
        b = s["actors"]["B"]
        s["supplement"]["waveWitness355"]["eventLedger"].append({"kind": "B-regular-end", "atSeconds": 172806.4, "unusedActionExpired": False})
        # The Hide action already spent B's Action; no additional transition is needed.
        assert b["Action"] == 0
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.4, "actor": "B", "type": "regular-turn-end",
            "Action": 0, "Reaction": b["Reaction"], "ready": b.get("ready"),
        })

    add_event("WC355-NW-E09-B-REGULAR-END", "regular-turn-end-after-paid-hide", 172806.4,
              "Close B's post-end probe turn after the Action was spent. No Ready action or reaction was declared.",
              ["WC355-NW-E08-POST-END-STEALTH-USE"], end_b_turn)

    def start_a_final(s: dict) -> None:
        a = s["actors"]["A"]
        a.update({"regularStart": 172806.4, "nextRegularStart": 172812.4, "Action": 1, "Reaction": 1,
                  "BonusAction": 1, "freeInteraction": 1, "movementRemaining": 30, "turnCast": False})
        a["regularStartsProcessed"].append(172806.4)
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.4, "actor": "A", "type": "regular-turn-start",
            "Action": 1, "Reaction": 1, "ready": None,
        })
        s["supplement"]["waveWitness355"]["eventLedger"].append({"kind": "A-regular-start", "atSeconds": 172806.4})

    add_event("WC355-NW-E10-A-NEXT-REGULAR-START", "regular-turn-start-no-action", 172806.4,
              "Record A's next scheduled start after B's turn; no further item or spell action is taken.",
              ["SUPPLEMENT255_W2.json#MF247-F-W2-E19-A-START-FOR-DISPEL.afterState actors/A.nextRegularStart"], start_a_final)

    def start_c_final(s: dict) -> None:
        a = s["actors"]["A"]
        a["Action"] = 0
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.6, "actor": "A", "type": "regular-turn-end",
            "ActionBefore": 1, "ActionAfter": 0, "Reaction": 1, "ready": None,
        })
        c = s["actors"][CASTER]
        c["regular"]["starts"].append(172806.6)
        c["regular"]["nextStart"] = 172812.6
        c["budget"].update({"Action": 1, "BonusAction": 1, "Reaction": 1, "movementSpent": 0, "companionCommandSpent": False})
        c["turnStartHistory"].append({"atSeconds": 172806.6, "Action": 1, "BonusAction": 1, "Reaction": 1})
        c["turnHistory"].append({"atSeconds": 172806.6, "phase": "start", "Action": 1, "Reaction": 1, "ready": None})
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.6, "actor": CASTER, "type": "regular-turn-start",
            "Action": 1, "Reaction": 1, "ready": None,
        })
        s["supplement"]["waveWitness355"]["eventLedger"].append({"kind": "WC355-regular-start", "atSeconds": 172806.6})

    add_event("WC355-NW-E11-W219-NEXT-REGULAR-START", "regular-turn-start-no-action", 172806.6,
              "Record the next scheduled WC355 start after A; no second Wave cast or other action occurs.",
              ["Return281:ACTOR_PROFILES.json#/W219", "WC355 fixture phase and source schedule"], start_c_final)

    def close_encounter(s: dict) -> None:
        s["actors"]["A"]["Action"] = 0
        s["actors"][CASTER]["budget"]["Action"] = 0
        s["supplement"]["waveWitness355"]["eventLedger"].append({"kind": "encounter-close", "atSeconds": 172806.7,
                                                                    "readyActions": [], "unresolvedReactions": [],
                                                                    "outstandingDeadlines": []})
        s["scene"]["waveClosure355"]["encounterClosedAtSeconds"] = 172806.7
        c = s["actors"][CASTER]
        c["regular"]["ends"].append(172806.7)
        c["turnHistory"].append({"atSeconds": 172806.7, "phase": "end", "Action": 0, "Reaction": 1, "ready": None})
        c["readyHistory"].append({"atSeconds": 172806.7, "declared": False, "expired": False})
        s["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"].append({
            "atSeconds": 172806.7, "actor": CASTER, "type": "regular-turn-end-encounter-close",
            "Action": 0, "Reaction": 1, "ready": None,
        })

    add_event("WC355-NW-E12-CLOSE-ENCOUNTER", "close-encounter-no-further-action", 172806.7,
              "Close the test encounter after all scheduled slots through the endpoint. No Ready actions, ongoing Wave duration, or unresolved counters remain.",
              ["WC355-NW-FORGE-ENCOUNTER regular-turn ledger"], close_encounter)

    final_state = copy.deepcopy(state)
    reverse = copy.deepcopy(final_state)
    reverse_steps = []
    for event in reversed(events):
        assert state_hash(reverse) == event["afterSHA256"], event["id"]
        reverse = apply_ops(reverse, event["inverse"])
        assert state_hash(reverse) == event["beforeSHA256"], event["id"]
        reverse_steps.append(event["id"])
    assert state_hash(reverse) == base_hash

    final_item = final_state["items"]["bracelet-1"]
    final_actor = final_state["actors"][CASTER]
    end_count = sum(1 for row in final_state["supplement"]["imprintEndings"] if row.get("rootId") == "castF2")
    probe = final_state["supplement"]["waveWitness355"]["postTerminationFunctionChecks"][0]
    assert final_item["imprintRoot"]["active"] is False and final_item["HP"] == 2 and final_item["charges"] == 0
    assert final_item["owner"] == "A" and final_item["custodian"] == "B-right-wrist" and final_item["worn"] is True
    assert end_count == 1 and final_actor["RP"] == 42 and final_actor["budget"]["Action"] == 0
    assert probe["total"] == probe["d20"] + probe["dexModifier"] + probe["proficiencyBonus"] + probe["braceletPassiveBonus"]
    assert probe["result"] == "not hidden" and probe["total"] < probe["fixtureObserverDC"]

    witness = {
        "id": "NULLIFICATION-WAVE-WC188-B01-CLOSURE-WITNESS-355",
        "recordedAtUtc": created_at,
        "status": "TEST_ONLY_AUTHORED_CONDITIONAL_WITNESS_DIRECTOR_REVIEW_PENDING",
        "spellId": TARGET,
        "blockerIds": [BLOCKER],
        "baseAuthority": {"reviewedApplied": 826, "pending": 22, "acceptedUnapplied": 0,
                          "completeStandaloneProcedures": 550, "scopedInterfaces": 173},
        "scopeLimits": {
            "campaignHistoryClaimed": False,
            "canonicalRulesChanged": False,
            "acceptanceOrApplicationClaimed": False,
            "sourceStatus": "Wave procedure and scenario are submitted for Director review; this artifact does not itself authorize application.",
            "branch": "Independent conditional branch from the exact SUPPLEMENT255 W2 state before event MF247-F-W2-E20-PAID-GREATER-DISPEL.",
            "historicalGreaterDispelBranch": "Preserved byte-for-byte as source context; not replayed or rewritten in this Wave branch.",
        },
        "sourceBindings": current_source_bindings,
        "sourceSnapshot": replay_report,
        "branchInitialState": events[0]["beforeState"],
        "encounter": {
            "id": "WC355-NW-FORGE-ENCOUNTER",
            "authoringClass": "explicit TEST_ONLY finite fixture; not observed play or campaign evidence",
            "baseStateSHA256": base_hash,
            "startTimeSeconds": 172800.4,
            "endTimeSeconds": final_state["time"],
            "events": events,
            "finalState": final_state,
            "fullReverseTraversal": {"eventCount": len(events), "reversedEventIds": reverse_steps, "returnedToBaseHash": state_hash(reverse)},
        },
        "targetLifecycle": {
            "rootId": "castF2", "itemId": "bracelet-1", "sourceRank": 9,
            "preWaveActive": True, "preWaveSuppressed": False,
            "creationAndLineage": "Bound to exact MF210-F02 source case and complete 19-event W2 replay through E19; the branch starts immediately before E20.",
            "transferHistory": copy.deepcopy(events[0]["beforeState"]["supplement"]["custodyHistory"]),
            "damageHistory": copy.deepcopy(events[0]["beforeState"]["supplement"]["objectDamageEvents"]),
            "chargeHistory": {"transactions": copy.deepcopy(events[0]["beforeState"]["supplement"]["chargeTransactions"]),
                              "processedDawns": copy.deepcopy(events[0]["beforeState"]["supplement"]["dawnEvents"])},
            "endingCount": end_count,
            "preservedMundaneState": {k: final_item.get(k) for k in ["HP", "maxHP", "damageDeficit", "charges", "maximumCharges", "owner", "custodian", "worn", "melded", "positionBoxFeet", "complete"]},
            "postEndFunctionProbe": probe,
        },
        "preservation": {
            "historicalWaveCaseCount": len(historical_wave_cases),
            "historicalCaseIds": [row["id"] for row in historical_wave_cases],
            "historicalCaseIndexBinding": source_digests["caseIndexMember"],
            "historicalQualificationBinding": source_digests["qualificationsMember"],
            "qualificationIdsUnchanged": copy.deepcopy(qualifications["distinctListedQualificationIds"]),
            "return281ArchivePreserved": True,
        },
        "acceptedIds": [], "appliedIds": [], "closedBlockerIds": [], "applicationAuthorized": False,
    }

    director_return = {
        "id": "DIRECTOR-FULL-QUEUE-PREPARATION-RETURN-354",
        "recordedAtUtc": created_at,
        "source": "GPT Director browser chat: Review Time Stop Witness Evidence",
        "sourceConversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750",
        "baseCommit": "351fe708ab21d1d63e5301f16336adf3712bfbf0",
        "authority": {"reviewedApplied": 826, "pending": 22, "acceptedUnapplied": 0,
                      "completeStandaloneProcedures": 550, "scopedInterfaces": 173},
        "status": "PREPARATION_ONLY_NO_ACCEPTANCE",
        "nextAction": {"spellId": TARGET, "blockerIds": [BLOCKER],
                       "requiredArtifact": "new source-bound complete paid Wave encounter witness, independent semantic audit, and full forward/inverse verification"},
        "acceptedIds": [], "appliedIds": [], "closedBlockerIds": [], "applicationAuthorized": False,
        "fullPriorityOrder": PRIORITY_ORDER,
        "rulings": {
            "heraldW01": "GPT may serve as Director-integration authority; concrete content reconciliation remains unapproved.",
            "heraldW02": "Owner may authorize a TEST_ONLY call-state provider/record; hypothetical premises do not assert campaign facts; W03/W04 remain dependent.",
            "wave": "Branch from exact live castF2 snapshot before E20; separate legally prepared Wave caster; 26 RP/Action, 60-foot sphere, initial cover snapshot, one imprint ending, preserve physical body and all clocks/history, no save or DC28 check.",
            "queueCorrections": ["label Summon Elemental Avatar correction as historical and currently applied", "make closedBlockerIdsThisStep historical", "record Director return 354", "mark fate-rewrite submission status as historical/no current submission"],
        },
    }

    auth_record = {
        "id": "OWNER-LUMEN-W02-TEST-AUTHORIZATION-355",
        "recordedAtUtc": created_at,
        "authoritySource": "user reply to explicit W02 authorization question",
        "userAnswer": "Yes—authorize this TEST_ONLY fixture",
        "provider": "Codex acting under the project owner's express authorization",
        "stateClassification": "expressly-authorized-test-state",
        "scope": "When W01 is approved, create a hypothetical Lumen call-state fixture only for Summon Herald W03/W04 witness work.",
        "campaignEventClaimed": False,
        "conditionalOnApprovedW01": True,
        "notCreatedByThisRecord": True,
        "requiredW02Fields": ["authorityAttestation.providerRole", "authorizingRecordOrApprovalPath", "approvalTimestampUtc", "scopeOfAuthority", "targetIdentity", "sourceProfileBinding", "stateTimestampUtc", "sourceLocation", "presentOrExpresslyAuthorizedTestState", "available", "competingReservationOrConcurrentCall", "affirmativeConsentToExactCall", "permittedAidOrCommandScope", "currentHP", "conditions", "usesAndRecharge", "equipmentAndCustody", "sealState", "permittedKnowledgeAndDisclosure"],
    }

    # Carry forward the full 22-ID authority view, correcting stale current-vs-historical labels only.
    queue = load(QUEUE354)
    pending = load(PENDING354)
    handoff = load(HANDOFF354)
    now = created_at
    pending_ids = list(pending["pendingIds"])
    assert pending_ids == SCOPE_IDS and len(SCOPE_IDS) == len(PRIORITY_ORDER) == 22
    old_corr = copy.deepcopy(queue.get("correctionAuthority", {}))
    queue["correctionAuthorityHistorical"] = old_corr
    queue["correctionAuthority"] = {
        "status": "NO_CURRENT_CORRECTION_REQUEST",
        "currentHeldIds": [], "currentAcceptedIds": [], "currentAppliedIds": [],
        "historicalContext": "The prior Summon Elemental Avatar hold is superseded by the accepted/applied 350/351 closure; it is not a current hold or pending identity.",
        "historicalRecord": old_corr,
    }
    queue["closedBlockerIdsThisStepHistorical"] = copy.deepcopy(queue.get("closedBlockerIdsThisStep", []))
    queue["closedBlockerIdsThisStep"] = []
    queue.update({
        "id": "CURRENT-SPELL-QUEUE-355", "recordedAtUtc": now,
        "supersedesQueue": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_354.json",
        "pendingCount": 22, "acceptedUnapplied": 0, "nextGroup": "rank9-ward-control6",
        "nextPendingIds": [TARGET], "nextPendingCount": 1,
        "activeReview": {"scopeIds": [TARGET], "blockerIds": [BLOCKER], "status": "CLOSURE WITNESS BUILT; DIRECTOR REVIEW PENDING"},
        "continuingPriorityOrder": PRIORITY_ORDER,
        "continuingPriorityOrderIsPrioritySubset": False, "prioritySubsetOmittedPendingIds": [],
        "remainingPendingIds": SCOPE_IDS,
        "lastDirectorReturn": "DIRECTOR-FULL-QUEUE-PREPARATION-RETURN-354",
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": [TARGET],
        "currentReturnBlockers": [BLOCKER], "currentReturnDecision": "PREPARATION_ONLY_NO_ACCEPTANCE",
        "currentPacketStatus": "Closure355 authored TEST_ONLY evidence; Director review pending; no acceptance or application.",
        "currentPacket": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_nullification_wave_closure355_delivery/DD_Rank9_NullificationWave_WC188B01_Closure355.zip", "status": "DIRECTOR_REVIEW_PENDING"},
        "currentPreparation": {"scopeIds": [TARGET], "blockerIds": [BLOCKER], "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_nullification_wave_closure355_delivery/DD_Rank9_NullificationWave_WC188B01_Closure355.zip"},
        "nextIdentity": TARGET, "nextBlockerIds": [BLOCKER],
        "nextActionablePriority": {"identity": TARGET, "blockerIds": [BLOCKER]},
        "closedBlockerIdsThisStep": [], "closedResidualIdsThisStep": [],
        "acceptedThisStep": [], "appliedThisStep": False, "applicationPerformed": False,
        "canonicalFilesChanged": False, "runtimeExecuted": False, "githubChanges": False,
        "fateRewriteSubmissionStatusHistorical": pending.get("fateRewriteSubmissionStatus"),
        "fateRewriteSubmissionStatus": "NO_CURRENT_SUBMISSION",
        "currentDirectorRulingSupplement": "docs/audit/2026-10-08/full-game/director-spell-review-129/DIRECTOR_FULL_QUEUE_PREPARATION_RETURN_355.json",
        "ownerW02TestAuthorization": "docs/audit/2026-10-08/full-game/director-spell-review-129/OWNER_LUMEN_W02_TEST_AUTHORIZATION_355.json",
    })
    pending["closedBlockerIdsThisStepHistorical"] = copy.deepcopy(pending.get("closedBlockerIdsThisStep", []))
    pending["closedBlockerIdsThisStep"] = []
    pending["lastDirectorReturnHistorical"] = copy.deepcopy(pending.get("lastDirectorReturn"))
    pending.update({
        "id": "CURRENT22-PENDING-IDENTITY-AUDIT-355", "recordedAtUtc": now,
        "status": "PASS_CURRENT_826_22_WAVE_CLOSURE_REVIEW_PENDING",
        "supersedes": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT22_PENDING_IDENTITY_AUDIT_354.json", **digest(PENDING354.read_bytes())},
        "pendingCount": 22, "pendingIds": SCOPE_IDS, "acceptedIds": [], "appliedIds": [],
        "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [],
        "closureTasksRemaining": 22, "firstReviewTasksRemaining": 0,
        "nextGroup": "rank9-ward-control6", "nextPendingIds": [TARGET], "nextPendingCount": 1,
        "nextStep": "Director review of the WC188-B01 Closure355 conditional paid Wave witness; retain held status until an explicit sealed decision.",
        "currentBlocker": BLOCKER, "nextIdentity": TARGET, "nextBlockerIds": [BLOCKER],
        "continuingPriorityOrder": PRIORITY_ORDER, "continuingPriorityOrderIsPrioritySubset": False,
        "prioritySubsetOmittedPendingIds": [], "remainingPendingIds": SCOPE_IDS,
        "heldThisStep": [TARGET], "acceptedThisStep": [], "appliedThisStep": False,
        "applicationPerformed": False, "canonicalFilesChanged": False,
        "lastDirectorReturnHistorical": pending.get("lastDirectorReturn"),
        "lastDirectorReturn": {"decisionId": "DIRECTOR-FULL-QUEUE-PREPARATION-RETURN-354", "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET], "blockerIds": [BLOCKER], "applicationAuthorized": False},
        "fateRewriteSubmissionStatusHistorical": pending.get("fateRewriteSubmissionStatus"),
        "fateRewriteSubmissionStatus": "NO_CURRENT_SUBMISSION",
        "ownerW02TestAuthorization": "docs/audit/2026-10-08/full-game/director-spell-review-129/OWNER_LUMEN_W02_TEST_AUTHORIZATION_355.json",
    })
    handoff["closedBlockerIdsThisStepHistorical"] = copy.deepcopy(handoff.get("closedBlockerIds", []))
    handoff.update({
        "id": "CURRENT-HANDOFF-355", "recordedAtUtc": now,
        "supersedes": "CURRENT-HANDOFF-354",
        "status": "CURRENT DIRECTOR HANDOFF; 22 CLOSURE TASKS REMAIN; NULLIFICATION-WAVE WC188-B01 WITNESS SUBMITTED FOR REVIEW",
        "scopeIds": SCOPE_IDS, "blockerIds": [BLOCKER],
        "currentBlocker": {"identity": TARGET, "group": "rank9-ward-control6", "blockerIds": [BLOCKER]},
        "nextPendingGroup": "rank9-ward-control6",
        "nextStep": "Review Closure355. No identity acceptance or application until the Director explicitly accepts a complete submission.",
        "currentPacketStatus": "TEST_ONLY witness and independent audit built; review pending; identity remains held.",
        "continuingPriorityOrder": PRIORITY_ORDER, "continuingPriorityOrderIsPrioritySubset": False,
        "prioritySubsetOmittedPendingIds": [], "remainingPendingIds": SCOPE_IDS,
        "nextIdentity": TARGET, "nextBlockerIds": [BLOCKER],
        "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET],
        "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnHeldIds": [TARGET],
        "currentReturnBlockers": [BLOCKER], "currentReturnDecision": "PREPARATION_ONLY_NO_ACCEPTANCE",
        "currentPreparation": {"scopeIds": [TARGET], "blockerIds": [BLOCKER], "path": "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_nullification_wave_closure355_delivery/DD_Rank9_NullificationWave_WC188B01_Closure355.zip"},
        "currentDirectorSourceCheck": "DIRECTOR-FULL-QUEUE-PREPARATION-RETURN-354",
        "closedBlockerIds": [], "closedResidualIdsThisStep": [],
        "canonicalFilesChanged": False, "applicationPerformed": False, "runtimeExecuted": False,
        "closureTasksRemaining": 22, "firstReviewTasksRemaining": 0,
    })
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_355.json"
    pending_path = AUDIT / "CURRENT22_PENDING_IDENTITY_AUDIT_355.json"
    handoff_path = AUDIT / "CURRENT_HANDOFF_355.json"
    director_path = AUDIT / "DIRECTOR_FULL_QUEUE_PREPARATION_RETURN_355.json"
    auth_path = AUDIT / "OWNER_LUMEN_W02_TEST_AUTHORIZATION_355.json"
    witness_path = AUDIT / "NULLIFICATION_WAVE_CLOSURE_WITNESS_355.json"
    queue_path.write_bytes(json_bytes(queue))
    pending_path.write_bytes(json_bytes(pending))
    handoff_path.write_bytes(json_bytes(handoff))
    director_path.write_bytes(json_bytes(director_return))
    auth_path.write_bytes(json_bytes(auth_record))
    witness_path.write_bytes(json_bytes(witness))

    independent_checks = []

    def check(name: str, passed: bool, detail: str) -> None:
        independent_checks.append({"check": name, "passed": bool(passed), "detail": detail})

    check("exact pre-E20 branch snapshot", base_hash == "f02c265c02e1046278d53dc8b4945b0bd138edd3f70ae9ea9197c88dcd328eb0", base_hash)
    check("all 18 historical Wave cases preserved", len(historical_wave_cases) == 18 and len(historical_case_digests) == 18 and all(historical_case_digests[i]["sha256"] == historical_wave_cases[i]["sha256"] for i in range(18)), str(len(historical_case_digests)))
    check("legal distinct prepared W219-derived Wizard caster", final_actor["profile"] == "ACTOR_PROFILES.json#/W219" and TARGET in final_actor["preparedSpells"] and final_actor["id"] == CASTER and final_actor["RP"] == 42, "Level-17 legal Wave selection and prepared repertoire; held focus; no reuse of Forge actor A")
    check("actual Wave Action and 26 RP paid", any(e["id"] == "WC355-NW-E04-PAID-WAVE-COMMIT" for e in events) and final_actor["budget"]["Action"] == 0 and final_actor["RP"] == 42, "68 RP to 42 RP, Action spent once")
    check("capture geometry and initial cover", final_state["scene"]["waveClosure355"]["radiusFeet"] == 60 and final_state["scene"]["waveClosure355"]["initialCoverClipsTarget"] is False and final_state["scene"]["waveClosure355"]["volumeClippedByCover"] is True and final_state["scene"]["waveClosure355"]["coveredSampleExcludedByInitialCover"] is True and final_state["scene"]["waveClosure355"]["itemAnchorDistanceFeet"] < 60, "60-foot sphere snapshots a test-only opaque wall: bracelet is reachable, a point behind the wall is clipped")
    check("complete active-effect scan", final_state["scene"]["waveClosure355"]["activeEffectScan"]["activeItemRoots"] == [{"itemId": "bracelet-1", "rootId": "castF2"}] and final_state["scene"]["waveClosure355"]["activeEffectScan"]["pendingCasts"] == {} and final_state["scene"]["waveClosure355"]["activeEffectScan"]["activeConcentrations"] == [] and final_state["scene"]["waveClosure355"]["activeEffectScan"]["activeEffectRegistryRows"] == [], "Snapshot enumerates all registered roots, pending casts, concentrations and active area effects")
    check("Action/Reaction/Ready and turn histories", len(final_state["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"]) >= 12 and len(final_actor["resourceHistory"]) == 1 and final_actor["reactionHistory"] and len(final_actor["readyHistory"]) == 2, "Source opening budgets plus each fixture turn, paid Action/RP, counter window, Ready state and close are recorded")
    check("single Forge imprint ends once; body and history persist", end_count == 1 and final_item["imprintRoot"]["active"] is False and final_item["HP"] == 2 and final_item["charges"] == 0 and final_item["custodian"] == "B-right-wrist", "No repair, refill, body loss, or history rewrite")
    check("no save or Greater Dispel check added", final_state["scene"]["waveClosure355"]["captureResult"]["save"] is None and final_state["scene"]["waveClosure355"]["captureResult"]["GreaterDispelDC28Check"] is None, "Source-sigil ending is direct")
    check("post-end magical benefit unavailable; ordinary adornment remains", probe["braceletPassiveBonus"] == 0 and probe["ordinaryAdornmentPersists"] is True and probe["total"] == 12, "Authored Hide test: 10+2+0; would have been +1 if root remained")
    check("full forward/inverse replay", len(reverse_steps) == len(events) == 12 and state_hash(reverse) == base_hash, "12 inverse events restore exact start snapshot")
    check("no acceptance, application or blocker closure claimed", witness["acceptedIds"] == witness["appliedIds"] == witness["closedBlockerIds"] == [] and witness["applicationAuthorized"] is False, "Review remains pending")

    failures = [row for row in independent_checks if not row["passed"]]
    audit_report = {
        "id": "NULLIFICATION-WAVE-WC188-B01-CLOSURE355-INDEPENDENT-AUDIT",
        "recordedAtUtc": created_at,
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(independent_checks), "passedChecks": len(independent_checks) - len(failures), "failedChecks": len(failures),
        "checks": independent_checks,
        "scopeIds": [TARGET], "blockerIds": [BLOCKER],
        "authority": witness["baseAuthority"],
        "testOnlyInterpretiveLimit": "This audit verifies data bindings, source-derived rules, fixture inputs, the paid Wave trace and reversible state changes. It does not claim historical gameplay or Director acceptance.",
        "sourceBindings": source_digests,
    }
    audit_path = AUDIT / "NULLIFICATION_WAVE_CLOSURE355_INDEPENDENT_AUDIT.json"
    audit_path.write_bytes(json_bytes(audit_report))
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))
    # Independently re-read and validate the finished witness before packet assembly.
    subprocess.run([sys.executable, str(AUDIT / "verify_nullification_wave_closure355.py")], check=True)
    audit_report = load(AUDIT / "NULLIFICATION_WAVE_CLOSURE355_INDEPENDENT_AUDIT.json")
    assert audit_report["status"] == "PASS" and audit_report["failedChecks"] == 0

    request = """# Director review request — Nullification Wave Closure355

Review only `nullification-wave` / `WC188-B01` against the sealed queue and the attached witness. The full current queue remains 826 applied / 22 pending / 0 accepted-unapplied; all other dispositions and the 18 Return281 Wave cases remain preserved.

The witness starts from the exact pre-E20 Forge snapshot and binds its 19-event replay, the paid W219-derived Wave caster, source geometry and cover snapshot, counter window, 26 RP plus Action payment, one-time imprint termination, preservation of the damaged mundane bracelet, subsequent Hide probe, and full forward/inverse traversal. Every new actor, initiative roll, observer DC and d20 value is marked TEST_ONLY; no campaign event is claimed.

Please return a sealed decision with acceptedIds, appliedIds, heldIds, blockerIds, closedBlockerIds, applicationAuthorized, and any exact remaining defects. Do not infer acceptance from the successful authored trace. The current requested scope is only WC188-B01; no canonical spell procedure, source card, or application file was edited.
"""
    request_path = OUTPUT / "DIRECTOR_REQUEST_355.md"

    # Build a self-contained packet. Return281 is carried whole so all 18 cases and their qualification history remain byte-exact.
    packet_path = OUTPUT / "DD_Rank9_NullificationWave_WC188B01_Closure355.zip"
    members: dict[str, bytes] = {}

    def put(member: str, data: bytes) -> None:
        if member in members:
            raise ValueError(f"duplicate packet member {member}")
        members[member] = data

    put("DIRECTOR_REQUEST_355.md", request.encode("utf-8"))
    put("verify_nullification_wave_closure355.py", (AUDIT / "verify_nullification_wave_closure355.py").read_bytes())
    put("NULLIFICATION_WAVE_CLOSURE_WITNESS_355.json", witness_path.read_bytes())
    put("NULLIFICATION_WAVE_CLOSURE355_INDEPENDENT_AUDIT.json", audit_path.read_bytes())
    put("NULLIFICATION_WAVE_FORGE_BRANCH_REPLAY_355.json", SOURCE_REPORT.read_bytes())
    put("CURRENT_SPELL_QUEUE_355.json", queue_path.read_bytes())
    put("CURRENT22_PENDING_IDENTITY_AUDIT_355.json", pending_path.read_bytes())
    put("CURRENT_HANDOFF_355.json", handoff_path.read_bytes())
    put("DIRECTOR_FULL_QUEUE_PREPARATION_RETURN_355.json", director_path.read_bytes())
    put("OWNER_LUMEN_W02_TEST_AUTHORIZATION_355.json", auth_path.read_bytes())
    put("source/return247/MF210-F02.json", base_case_raw)
    put("source/return247/archive_binding.json", json_bytes({"archivePath": RETURN247.relative_to(ROOT).as_posix(), **source_digests["return247Archive"], "member": "cases/MF210-F02.json", "memberBinding": source_digests["return247CaseMember"]}))
    put("source/eternalforge/SUPPLEMENT255_W2.json", SUPPLEMENT.read_bytes())
    put("source/eternalforge/MODEL.json", FORGE_MODEL.read_bytes())
    put("source/eternalforge/EXACT_ACCEPTANCE.json", FORGE_ACCEPTANCE.read_bytes())
    put("source/eternalforge/DIRECTOR_ACCEPTANCE.json", FORGE_DIRECTOR_ACCEPTANCE.read_bytes())
    put("history/Return281_HELD.zip", RETURN281.read_bytes())
    put("source/return281/archive_binding.json", json_bytes({"archivePath": RETURN281.relative_to(ROOT).as_posix(), **source_digests["return281Archive"], "preservedWaveCaseCount": 18, "caseIndexBinding": source_digests["caseIndexMember"], "qualificationBinding": source_digests["qualificationsMember"], "caseIds": [row["id"] for row in historical_wave_cases]}))
    manifest = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-PACKET-MANIFEST",
        "selfExcluded": True,
        "memberCountExcludingSelf": len(members),
        "members": [{"path": name, **digest(data)} for name, data in sorted(members.items())],
    }
    members["MEMBER_MANIFEST.json"] = json_bytes(manifest)
    with zipfile.ZipFile(packet_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for member, data in sorted(members.items()):
            archive.writestr(member, data)
    packet_raw = packet_path.read_bytes()
    delivery = {
        "id": "DD-RANK9-NULLIFICATION-WAVE-WC188B01-CLOSURE355-DELIVERY",
        "recordedAtUtc": created_at,
        "archive": {"path": packet_path.relative_to(ROOT).as_posix(), **digest(packet_raw)},
        "memberCount": len(members), "payloadMemberCount": len(members) - 1,
        "targetIds": [TARGET], "blockerIds": [BLOCKER],
        "authority": witness["baseAuthority"],
        "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET], "applicationAuthorized": False,
        "preservedHistoricalWaveCases": 18,
        "independentAudit": {"path": audit_path.relative_to(ROOT).as_posix(), **digest(audit_path.read_bytes())},
        "queue": {"path": queue_path.relative_to(ROOT).as_posix(), **digest(queue_path.read_bytes())},
        "sourceBindings": source_digests,
        "interpretiveLimit": "Authored TEST_ONLY conditional evidence submitted for Director review; no campaign fact or acceptance/application is asserted.",
    }
    delivery_path = OUTPUT / "DD_Rank9_NullificationWave_WC188B01_Closure355_DELIVERY.json"
    delivery_path.write_bytes(json_bytes(delivery))

    print(json.dumps({
        "status": audit_report["status"],
        "checks": audit_report["checkCount"],
        "failedChecks": audit_report["failedChecks"],
        "eventCount": len(events),
        "reverseTraversalCount": len(reverse_steps),
        "historicalWaveCases": len(historical_wave_cases),
        "queuePending": 22,
        "packet": str(packet_path),
        "packetDigest": digest(packet_raw),
        "delivery": str(delivery_path),
        "deliveryDigest": digest(delivery_path.read_bytes()),
        "sourceReport": str(audit_path),
    }, indent=2))


if __name__ == "__main__":
    main()
