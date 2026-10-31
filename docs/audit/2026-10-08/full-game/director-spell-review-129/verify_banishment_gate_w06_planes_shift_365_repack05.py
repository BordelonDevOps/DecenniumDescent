from __future__ import annotations

import copy
import hashlib
import json
import math
import subprocess
import zipfile
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness365_w06_planes_shift_repack05_verified03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack05_TESTONLY.zip"
CASE = PACK / "W06_PLANESHIFT_ESCAPE_CASE_365_REPACK05.json"
GATE_ID = "BG-W06-TESTONLY-GATE-365"
GUARD_ID = "Guard-W06-TESTONLY"
WP13_ID = "WP13-W06-TESTONLY"
CELL_GUARD = "BG-W06-TESTONLY-CELL-GUARD-365"
CELL_WP13 = "BG-W06-TESTONLY-CELL-WP13-365"
ENC = "utf-8"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding=ENC))


def parts(path):
    return [x.replace("~1", "/").replace("~0", "~") for x in path[1:].split("/")] if path else []


def get_at(obj, path):
    value = obj
    for part in parts(path):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def parent_at(obj, path):
    path_parts = parts(path)
    parent = obj
    for part in path_parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, path_parts[-1]


def changed_paths(before, after, path=""):
    if type(before) is dict and type(after) is dict:
        out = []
        for key in sorted(before.keys() | after.keys()):
            child = path + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key not in before or key not in after:
                out.append(child)
            else:
                out.extend(changed_paths(before[key], after[key], child))
        return out
    if type(before) is type(after) and before == after:
        return []
    assert path
    return [path]


def apply_patch(state, operations):
    current = copy.deepcopy(state)
    for operation in operations:
        path, kind = operation["path"], operation["op"]
        assert path
        if kind == "test":
            assert get_at(current, path) == operation["value"], f"precondition {path}"
            continue
        parent, key = parent_at(current, path)
        if isinstance(parent, list):
            idx = int(key)
            if kind == "replace":
                parent[idx] = copy.deepcopy(operation["value"])
            elif kind == "remove":
                parent.pop(idx)
            else:
                raise AssertionError(f"unsupported list operation {kind} at {path}")
        elif kind == "add":
            assert key not in parent
            parent[key] = copy.deepcopy(operation["value"])
        elif kind == "replace":
            assert key in parent
            parent[key] = copy.deepcopy(operation["value"])
        elif kind == "remove":
            assert key in parent
            del parent[key]
        else:
            raise AssertionError(f"unsupported operation {kind}")
    return current


case = load(CASE)
source_bindings = load(PACK / "W06_SOURCE_BINDINGS_365.json")
fixture = load(PACK / "W06_TESTONLY_FIXTURE_PREMISES_365.json")
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
source_audit = load(PACK / "authority/PG327_W03_W06_W07_SOURCE_AUDIT_362.json")
plan = load(PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json")
w07_seal = load(PACK / "prior/PG327_W07_DIRECTOR_SEAL_363_REPACK01.json")
w02_seal = load(PACK / "prior/PG327_W02_DIRECTOR_SEAL_364_REPACK03.json")
prior_w06_archive = PACK / "prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_TESTONLY.zip"
prior_w06_delivery = load(PACK / "prior/ARCHIVE_DELIVERY_365_REPACK01.json")
prior_w06_audit = load(PACK / "prior/INDEPENDENT_AUDIT_365_REPACK01.json")
prior_w06_supersession = load(PACK / "prior/W06_REPACK01_SUPERSESSION_365.json")
prior_w06_repack02_archive = PACK / "prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack02_TESTONLY.zip"
prior_w06_repack02_delivery = load(PACK / "prior/ARCHIVE_DELIVERY_365_REPACK02.json")
prior_w06_repack02_supersession = load(PACK / "prior/W06_REPACK02_SUPERSESSION_365.json")
prior_w06_repack03_archive = PACK / "prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack03_TESTONLY.zip"
prior_w06_repack03_delivery = load(PACK / "prior/ARCHIVE_DELIVERY_365_REPACK03.json")
prior_w06_repack03_audit = load(PACK / "prior/INDEPENDENT_AUDIT_365_REPACK03.json")
prior_w06_repack03_supersession = load(PACK / "prior/W06_REPACK03_SUPERSESSION_365.json")
prior_w06_repack04_archive = PACK / "prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack04_TESTONLY.zip"
prior_w06_repack04_delivery = load(PACK / "prior/ARCHIVE_DELIVERY_365_REPACK04.json")
prior_w06_repack04_audit = load(PACK / "prior/INDEPENDENT_AUDIT_365_REPACK04.json")
prior_w06_repack04_hold = load(PACK / "prior/PG327_W06_DIRECTOR_HOLD_365_REPACK04.json")
prior_w06_repack04_supersession = load(PACK / "prior/W06_REPACK04_SUPERSESSION_365.json")
pt_acceptance = load(PACK / "authority/PLANARTRAVEL6_EXACT_ACCEPTANCE_133.json")
assert case["id"] == "W06_PLANESHIFT_ESCAPE_CASE_365_REPACK05" and case["witnessId"] == "W06"
assert case["fixturePremises"] == fixture
assert len(case["supersedesSubmissions"]) == 4
assert case["supersedesSubmissions"][0]["archive"] == prior_w06_archive.name
assert case["supersedesSubmissions"][0]["archiveSha256"] == file_sha(prior_w06_archive.read_bytes())
assert case["supersedesSubmissions"][1]["archive"] == prior_w06_repack02_archive.name
assert case["supersedesSubmissions"][1]["archiveSha256"] == file_sha(prior_w06_repack02_archive.read_bytes())
assert case["supersedesSubmissions"][2]["archive"] == prior_w06_repack03_archive.name
assert case["supersedesSubmissions"][2]["archiveSha256"] == file_sha(prior_w06_repack03_archive.read_bytes())
assert case["supersedesSubmissions"][3]["archive"] == prior_w06_repack04_archive.name
assert case["supersedesSubmissions"][3]["archiveSha256"] == file_sha(prior_w06_repack04_archive.read_bytes())
assert prior_w06_repack04_delivery["sha256"] == file_sha(prior_w06_repack04_archive.read_bytes())
assert prior_w06_repack04_audit["archiveSha256"] == file_sha(prior_w06_repack04_archive.read_bytes())
assert prior_w06_repack04_hold["decision"] == "PG327-W06-365-REPACK04-DIRECTOR-HOLD"
assert prior_w06_repack04_hold["remainingResidualIds"] == ["W06-365-R1", "W06-365-R2", "W06-365-R3", "W06-365-R4"]
assert prior_w06_repack04_supersession["supersededArchiveSha256"] == file_sha(prior_w06_repack04_archive.read_bytes())
assert prior_w06_delivery["sha256"] == file_sha(prior_w06_archive.read_bytes())
assert prior_w06_audit["archiveSha256"] == file_sha(prior_w06_archive.read_bytes())
assert prior_w06_supersession["supersededArchiveSha256"] == file_sha(prior_w06_archive.read_bytes())
assert prior_w06_supersession["priorPacketSentToDirector"] is False
assert prior_w06_repack02_delivery["sha256"] == file_sha(prior_w06_repack02_archive.read_bytes())
assert prior_w06_repack02_supersession["supersededArchiveSha256"] == file_sha(prior_w06_repack02_archive.read_bytes())
assert prior_w06_repack02_supersession["independentAuditStatus"].startswith("NOT_PRODUCED")
assert prior_w06_repack03_delivery["sha256"] == file_sha(prior_w06_repack03_archive.read_bytes())
assert prior_w06_repack03_audit["archiveSha256"] == file_sha(prior_w06_repack03_archive.read_bytes())
assert prior_w06_repack03_supersession["supersededArchiveSha256"] == file_sha(prior_w06_repack03_archive.read_bytes())
assert prior_w06_repack03_supersession["priorPacketSentToDirector"] is True
with zipfile.ZipFile(prior_w06_archive) as prior_zf:
    prior_case = json.loads(prior_zf.read("W06_PLANESHIFT_ESCAPE_CASE_365_REPACK01.json"))
    assert prior_case["initial"]["actors"][WP13_ID]["loadLb"] == 10.0
    assert prior_case["events"][10]["after"]["items"]["focus-WP13"]["plane"] == "fixture:origin"
with zipfile.ZipFile(prior_w06_repack02_archive) as prior_zf:
    prior_case = json.loads(prior_zf.read("W06_PLANESHIFT_ESCAPE_CASE_365_REPACK02.json"))
    assert prior_case["initial"]["actors"][WP13_ID]["loadLb"] == 10.1
    assert prior_case["events"][10]["after"]["items"]["focus-WP13"]["plane"] == CELL_WP13
    assert prior_case["events"][11]["after"]["actors"][WP13_ID]["loadLb"] == 10.1
with zipfile.ZipFile(prior_w06_repack03_archive) as prior_zf:
    prior_case = json.loads(prior_zf.read("W06_PLANESHIFT_ESCAPE_CASE_365_REPACK03.json"))
    assert prior_case["events"][7]["after"]["cells"][CELL_GUARD]["originAnchor"]["position"] == [-2.5, -2.5, 0]
    assert prior_case["events"][10]["after"]["cells"][CELL_WP13]["originAnchor"]["position"] == [-2.5, 2.5, 0]
assert case["status"] == "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED"
assert "does not claim any type-changing mechanic" in fixture["premises"]["WP13"]
assert "no type-changing mechanic" not in fixture["premises"]["WP13"]
embedded_verifier = (PACK / "verification/verify_banishment_gate_w06_planes_shift_365_repack05.py").read_text(encoding=ENC)
assert '"does not claim any type-changing mechanic"' in embedded_verifier
assert len(case["events"]) == 14
assert w07_seal["decision"].startswith("W07 PASSES") and w02_seal["decision"].startswith("W02 PASSES")
assert source_audit["witnessSources"]["W06"]["status"] == "SOURCE_ROUTE_APPROVED_WITNESS_OUTSTANDING"
assert "plane-shift" in pt_acceptance["acceptedIdentities"] and pt_acceptance["approvedForCanonicalApplication"] is True

# Every event has exact snapshots, changed-field-only operations and exact reverse restoration.
state = copy.deepcopy(case["initial"])
for event in case["events"]:
    assert event["before"] == state and event["beforeSHA256"] == sha(state)
    assert sorted(op["path"] for op in event["forward"] if op["op"] != "test") == sorted(changed_paths(event["before"], event["after"]))
    state = apply_patch(state, event["forward"])
    assert state == event["after"] and event["afterSHA256"] == sha(state)
assert state == case["final"] and case["finalSHA256"] == sha(state)
for event in reversed(case["events"]):
    assert event["after"] == state
    state = apply_patch(state, event["inverse"])
    assert state == event["before"]
assert state == case["initial"] and case["inverseRestorationOrder"] == [e["id"] for e in reversed(case["events"])]

# Reused W07 members are bound to the byte-exact sealed archive. Every newly used Plane Shift source is bound to the same Git revision as the accepted source audit.
prior_w07 = PACK / "prior/DD_Rank9_BanishmentGate_W07_GustCorpse_363_Repack01_TESTONLY.zip"
assert file_sha(prior_w07.read_bytes()) == w07_seal["archiveSha256"]
with zipfile.ZipFile(prior_w07) as zf:
    w07_bindings = json.loads(zf.read("SOURCE_BINDINGS_363.json"))
    assert source_bindings["sourceCommit"] == w07_bindings["sourceCommit"]
    for binding in source_bindings["bindings"]:
        data = (PACK / binding["packetMember"]).read_bytes()
        if "bytes" in binding:
            assert len(data) == binding["bytes"]
        if binding in w07_bindings["bindings"]:
            assert data == zf.read(binding["packetMember"])
            if binding.get("sourceCommit") == source_bindings["sourceCommit"]:
                assert data == subprocess.check_output(["git", "show", f'{binding["sourceCommit"]}:{binding["repositoryPath"]}'], cwd=ROOT)
    w07_source_reuse = zf.namelist()
    assert w07_source_reuse
assert len(source_bindings["bindings"]) == len(w07_bindings["bindings"]) + 2
new_bindings = {b["repositoryPath"]: b for b in source_bindings["planarTravelNewBindings"]}
model_path = source_audit["witnessSources"]["W06"]["source"]["path"]
actor_path = source_audit["witnessSources"]["W06"]["acquisitionPreparation"]["path"]
assert new_bindings[model_path]["gitSha256"] == source_audit["witnessSources"]["W06"]["source"]["sha256"]
assert new_bindings[actor_path]["gitSha256"] == source_audit["witnessSources"]["W06"]["acquisitionPreparation"]["sha256"]
for binding in new_bindings.values():
    data = (PACK / binding["packetMember"]).read_bytes()
    assert len(data) == binding["bytes"] and file_sha(data) == binding["gitSha256"]
    assert data == subprocess.check_output(["git", "show", f'{binding["sourceCommit"]}:{binding["repositoryPath"]}'], cwd=ROOT)

# Exact source bindings for the four Repack04 Director HOLD residuals.
fixture_bindings = source_bindings["fixtureSpecificBindings"]
gate_binding = fixture_bindings["Gate"]
gate_bytes = (PACK / gate_binding["packetMember"]).read_bytes()
assert gate_binding["sourcePath"].endswith("rank9planargates5_reviewed_200/RETURN327_banishment-gate.json")
assert gate_binding["sha256"] == file_sha(gate_bytes) == "39c216e978e1c06da3dbea7fb27a60f8611ce08b36143c403fbca989f155fb00"
gate_source = json.loads(gate_bytes)
assert isinstance(get_at(gate_source, gate_binding["procedurePointer"]), str)
assert isinstance(get_at(gate_source, gate_binding["cellExtensionPointer"]), dict)
assert case["sourceBindings"]["Gate"]["procedurePointer"] == "/procedure"
assert case["sourceBindings"]["Gate"]["cellExtensionPointer"] == "/sharedContract/cellExtension"
cs_binding = fixture_bindings["WP13Counterspell"]
cs_actor = json.loads((PACK / cs_binding["packetMember"]).read_bytes())
cs_catalog = json.loads((PACK / cs_binding["catalogPacketMember"]).read_bytes())
assert cs_binding["actorProfileSha256"] == file_sha((PACK / cs_binding["packetMember"]).read_bytes())
assert get_at(cs_actor, cs_binding["actorProfilePointer"])["id"] == "wizard.base.counterspell"
assert get_at(cs_catalog, cs_binding["catalogPointer"]) == ["V", "S", "F"]
assert cs_binding["catalogSha256"] == file_sha((PACK / cs_binding["catalogPacketMember"]).read_bytes())
rule_binding = source_bindings["somaticRuleGitBinding"]
rule_data = (PACK / rule_binding["packetMember"]).read_bytes()
assert len(rule_data) == rule_binding["bytes"] and file_sha(rule_data) == rule_binding["gitSha256"]
assert rule_data == subprocess.check_output(["git", "show", f'{rule_binding["sourceCommit"]}:{rule_binding["repositoryPath"]}'], cwd=ROOT)
assert b"**S** requires a free hand or a class feature expressly permitting the gesture;" in rule_data
pt_arrival_binding = fixture_bindings["PT133Arrival"]
pt_model = json.loads((PACK / pt_arrival_binding["packetMember"]).read_bytes())
assert get_at(pt_model, pt_arrival_binding["pointer"])["id"] == "PT133-ARRIVAL"
assert case["sourceBindings"]["PT133Arrival"]["ruleId"] == "PT133-ARRIVAL"

# Plane Shift access and WP13 acquisition/preparation are exact and accepted; destination is a TEST_ONLY premise, not a source ability.
model = json.loads((PACK / "sources/planartravel6/MODEL.json").read_bytes())
wp13_source = json.loads((PACK / "sources/planartravel6/ACTOR_PROFILES.json").read_bytes())["WP13"]
plane = model["spells"][4]
assert plane["id"] == "plane-shift"
assert plane["completeSourceAndAccess"]["classAccess"]["Wizard"] == {"rank": 7, "minimumClassLevel": 13, "school": "Conjuration", "baseRpCost": 17}
assert wp13_source["class"] == "Wizard" and wp13_source["classLevel"] == 13
assert any(x.get("spellId") == "plane-shift" and x.get("completeAccess", {}).get("rank") == 7 for x in wp13_source["spellbook"])
assert "plane-shift" in wp13_source["prepared"]
assert wp13_source["preparationHistory"]["prepared"] == wp13_source["prepared"]
assert fixture["premises"]["destinationKnowledge"].startswith("WP13 has a prior personal TEST_ONLY record")

# Admission geometry and costs: two complete, nonoverlapping bodies cross the fixed opening on paid voluntary movement.
events = case["events"]
guard_cross = events[7]
wp_cross = events[10]
for event, from_box, to_box, start_wallet, end_wallet in (
    (guard_cross, {"x": [-5, 0], "y": [-5, 0], "z": [0, 6]}, {"x": [0, 5], "y": [-5, 0], "z": [0, 6]}, 40, 35),
    (wp_cross, {"x": [-5, 0], "y": [0, 5], "z": [0, 6]}, {"x": [0, 5], "y": [0, 5], "z": [0, 6]}, 30, 25),
):
    inputs = event["authoredInputs"]
    assert inputs["fromBodyBox"] == from_box and inputs["toBodyBox"] == to_box
    assert inputs["aperture"] == {"plane": "x=0", "y": [-5, 5], "z": [0, 15]}
    assert inputs["movementSpentFeet"] == 5 and inputs["wallet"] == [start_wallet, end_wallet]
    assert inputs["completeBodyCrossing"] is True and inputs["admittedCell"]
assert case["initial"]["actors"][WP13_ID]["creatureType"] == "Humanoid"
assert case["initial"]["actors"][WP13_ID]["creatureTypeClassification"].startswith("TEST_ONLY")
assert "does not claim any type-changing mechanic" in fixture["premises"]["WP13"]
assert guard_cross["after"]["actors"][GUARD_ID]["movement"] == 35
assert wp_cross["after"]["actors"][WP13_ID]["movement"] == 25
assert guard_cross["after"]["cells"][CELL_GUARD]["deadline"] == 62.05
assert wp_cross["after"]["cells"][CELL_WP13]["deadline"] == 63.05
for crossing, cell_id, expected in ((guard_cross, CELL_GUARD, [2.5, -2.5, 0]), (wp_cross, CELL_WP13, [2.5, 2.5, 0])):
    anchor = crossing["after"]["cells"][cell_id]["originAnchor"]
    box = anchor["bodyBox"]
    center = [(box[axis][0] + box[axis][1]) / 2 for axis in ("x", "y")] + [box["z"][0]]
    assert anchor["position"] == expected == center
assert wp_cross["before"]["actors"][WP13_ID]["loadLb"] == 10.1
assert wp_cross["after"]["actors"][WP13_ID]["loadLb"] == 10.1
for item_id in ("focus-WP13", "kit-WP13", "W13-LOOSE-TOKEN-365"):
    assert wp_cross["after"]["items"][item_id]["plane"] == CELL_WP13

# The only remaining object is genuinely dropped before casting and is separated from the travel group.
drop = events[11]
assert drop["authoredInputs"]["ordinaryFreeInteractionCost"] == 1
assert drop["after"]["items"]["W13-LOOSE-TOKEN-365"]["status"] == "genuine loose object"
assert drop["after"]["items"]["W13-LOOSE-TOKEN-365"]["cellLocalPosition"] == [5, 0, 0]
assert drop["before"]["actors"][WP13_ID]["loadLb"] == 10.1
assert drop["after"]["actors"][WP13_ID]["loadLb"] == 10.0
assert drop["after"]["items"]["W13-LOOSE-TOKEN-365"]["weightLb"] == 0.1
wp13_anchor = wp_cross["after"]["cells"][CELL_WP13]["originAnchor"]["position"]
projected = drop["after"]["cells"][CELL_WP13]["looseObjectAnchors"]["W13-LOOSE-TOKEN-365"]["originPlanePosition"]
assert projected == [wp13_anchor[0] + 5, wp13_anchor[1], wp13_anchor[2]] == [7.5, 2.5, 0]
assert "W13-LOOSE-TOKEN-365" not in drop["after"]["actors"][WP13_ID]["carriedItemIds"]
assert "W13-LOOSE-TOKEN-365" not in drop["after"]["pendingCast"].get("participants", []) if drop["after"].get("pendingCast") else True

# The cast uses the accepted route, its real costs and component/focus constraints; travel destination is a complete known bounded site.
commit = events[12]
cast_inputs = commit["authoredInputs"]
assert cast_inputs["spellId"] == "plane-shift" and cast_inputs["classLevel"] == 13 and cast_inputs["school"] == "Conjuration"
assert cast_inputs["rank"] == 7 and cast_inputs["actionCost"] == 1 and cast_inputs["rpCost"] == 17
assert cast_inputs["rpBeforeAfter"] == [48, 31] and cast_inputs["components"] == ["V", "S", "F"]
assert cast_inputs["participants"] == [WP13_ID] and cast_inputs["casterTravels"] is True
assert cast_inputs["participantDistanceFeet"] == 0 <= cast_inputs["nativeRangeFeet"] == 120
assert cast_inputs["siteKnownBeforeCast"] and cast_inputs["siteWorldFixed"] and cast_inputs["destinationClear"]
assert cast_inputs["transportBlockers"] == [] and cast_inputs["eligibleCounterspellReactors"] == []
destination = cast_inputs["destinationBounds"]
body = cast_inputs["destinationBodyBox"]
for axis in ("x", "y", "z"):
    assert destination[axis][0] <= body[axis][0] < body[axis][1] <= destination[axis][1]
pending = commit["after"]["pendingCast"]
assert pending["componentsProvided"] == ["V", "S", "F"] and pending["focusId"] == "focus-WP13"
assert len(pending["counterspellWindow"]["eligibleReactors"]) == 0
assert len(pending["counterspellWindow"]["ineligible"]) == 4

# Successful escape closes only Cell A. Its loose contents settle once; the Gate and Cell B clocks are unchanged.
escape = events[13]
before, after = escape["before"], escape["after"]
assert after["actors"][WP13_ID]["plane"] == "fixture:known-plane-beta"
assert after["actors"][WP13_ID]["transitHistory"][0]["identityPreserved"] is True
assert after["actors"][WP13_ID]["carriedItemIds"] == ["focus-WP13", "kit-WP13"]
assert after["items"]["focus-WP13"]["plane"] == after["items"]["kit-WP13"]["plane"] == "fixture:known-plane-beta"
assert after["actors"][WP13_ID]["loadLb"] == 10.0
token = after["items"]["W13-LOOSE-TOKEN-365"]
assert token["plane"] == "fixture:origin" and token["position"] == [7.5, 2.5, 0]
assert token["settlementCount"] == 1 and token["settlementSourceCell"] == CELL_WP13
assert after["cells"][CELL_WP13]["status"] == "destroyed" and after["cells"][CELL_WP13]["closeCount"] == 1
assert after["cells"][CELL_WP13]["settlementCounts"] == {"W13-LOOSE-TOKEN-365": 1}
assert after["cells"][CELL_GUARD] == before["cells"][CELL_GUARD]
assert after["cells"][CELL_GUARD]["status"] == "active" and after["cells"][CELL_GUARD]["closeCount"] == 0
assert after["effects"][GATE_ID]["status"] == "active" and after["effects"][GATE_ID]["closeCount"] == 0
assert after["effects"][GATE_ID]["cells"] == [CELL_GUARD]
assert after["actors"][GUARD_ID]["plane"] == CELL_GUARD
assert after["actors"]["W20"]["concentration"] == f"{GATE_ID}/cast"
assert after["clocks"]["gateConcentrationDeadline"] == before["clocks"]["gateConcentrationDeadline"] == 600.2
assert after["clocks"]["cellDeadlines"][CELL_GUARD] == before["clocks"]["cellDeadlines"][CELL_GUARD] == 62.05
assert after["clocks"]["otherIndependentDeadlines"] == before["clocks"]["otherIndependentDeadlines"]
assert escape["authoredInputs"]["gateDeadlineBeforeAfter"] == [600.2, 600.2]
assert escape["authoredInputs"]["otherCellDeadlineBeforeAfter"] == [62.05, 62.05]
assert len(after["settlements"]) == 1 and after["settlements"][0]["settlementId"] == "W06-365-CELL-A-CLOSE"

# WP13's Gate-Counterspell window is evaluated from source-bound readiness and hand state.
initial_wp13 = case["initial"]["actors"][WP13_ID]
gate_cast = case["events"][1]
window = gate_cast["after"]["pendingCast"]["counterspellWindow"]
wp13_interrupt = next(x for x in window["ineligible"] if x["actorId"] == WP13_ID)
assert initial_wp13["counterspellAutomaticId"] == "wizard.base.counterspell"
assert initial_wp13["counterspellReady"] is True
assert initial_wp13["recharge"]["wizard.base.counterspell"] == {"ready": True, "roundsUntilReady": 0, "rechargeRounds": 2, "lastUsed": None}
assert wp13_interrupt["distanceFeet"] < wp13_interrupt["rangeFeet"] == 60
assert wp13_interrupt["perceivesCast"] and wp13_interrupt["lineOfEffect"] and wp13_interrupt["reactionAvailable"] and wp13_interrupt["rechargeReady"]
assert wp13_interrupt["currentRP"] == 48 and wp13_interrupt["costRP"] == 3
assert wp13_interrupt["components"] == ["V", "S", "F"] and wp13_interrupt["freeHands"] == []
assert "free hand" in wp13_interrupt["reason"] and wp13_interrupt["attempted"] is False
assert wp13_interrupt["reactionSpent"] is False and wp13_interrupt["RPSpent"] == 0 and wp13_interrupt["cooldownChanged"] is False
assert gate_cast["after"]["actors"][WP13_ID]["recharge"]["wizard.base.counterspell"]["ready"] is True

# PT133 snapshots this cast's immediate origin, keeps creation provenance separate, and commits only on success.
plane_shift_commit = case["events"][12]
plane_shift_success = case["events"][13]
arrival_actor_before = plane_shift_commit["before"]["actors"][WP13_ID]
arrival_pending = plane_shift_commit["after"]["pendingCast"]
arrival_actor_after = plane_shift_success["after"]["actors"][WP13_ID]
assert arrival_actor_before["lastArrivedFromPlaneKey"] is None
assert arrival_actor_before["creationPlaneKey"] == "fixture:origin"
assert arrival_actor_before["creationPlaneProvenance"].startswith("TEST_ONLY")
assert arrival_pending["prospectiveOriginPlaneKey"] == CELL_WP13
assert arrival_pending["priorLastArrivedFromPlaneKey"] is None
assert plane_shift_commit["authoredInputs"]["prospectiveOriginPlaneKey"] == CELL_WP13
assert plane_shift_commit["after"]["actors"][WP13_ID]["lastArrivedFromPlaneKey"] is None
assert arrival_actor_after["lastArrivedFromPlaneKey"] == CELL_WP13
assert arrival_actor_after["creationPlaneKey"] == "fixture:origin"
assert arrival_actor_after["transitHistory"][0]["fromPlaneKey"] == CELL_WP13
assert arrival_actor_after["transitHistory"][0]["priorLastArrivedFromPlaneKey"] is None
assert arrival_actor_after["transitHistory"][0]["lastArrivedFromPlaneKey"] == CELL_WP13
assert plane_shift_success["before"]["actors"][WP13_ID]["lastArrivedFromPlaneKey"] is None

# Every carried item has an explicit volume and rigid carrier-frame map through admission and arrival.
def box_union(boxes):
    return {axis: [min(b[axis][0] for b in boxes), max(b[axis][1] for b in boxes)] for axis in ("x", "y", "z")}
def box_contains(outer, inner):
    return all(outer[axis][0] <= inner[axis][0] <= inner[axis][1] <= outer[axis][1] for axis in ("x", "y", "z"))
wp13_items = case["initial"]["items"]
initial_body = initial_wp13["bodyBoxWorld"]
assert set(initial_wp13["carriedItemIds"]) == {"focus-WP13", "kit-WP13", "W13-LOOSE-TOKEN-365"}
for item_id in initial_wp13["carriedItemIds"]:
    item = wp13_items[item_id]
    bounds = item["carrierLocalBoundsFeet"]
    volume = math.prod(bounds[a][1] - bounds[a][0] for a in ("x", "y", "z"))
    assert item["occupiedVolumeCubicFeet"] == volume > 0
    assert item["coordinateFrame"] == "WP13-foot-anchor-local-feet" and item["carrierId"] == WP13_ID
    assert item["worldBoundsFeet"] == {axis: [bounds[axis][0] + initial_wp13["position"][i], bounds[axis][1] + initial_wp13["position"][i]] for i, axis in enumerate(("x", "y", "z"))}
local_cargo = [wp13_items[i]["carrierLocalBoundsFeet"] for i in initial_wp13["carriedItemIds"]]
for i, a in enumerate(local_cargo):
    for b in local_cargo[i+1:]:
        assert any(a[axis][1] <= b[axis][0] or b[axis][1] <= a[axis][0] for axis in ("x", "y", "z"))
assert fixture["premises"]["WP13OccupiedCargo"]["pairwiseCargoVolumesDisjoint"] is True
admission = case["events"][10]
admit_after = admission["after"]
admit_cell = admit_after["cells"][CELL_WP13]
admit_inputs = admission["authoredInputs"]
assert admit_cell["contents"].count("W13-LOOSE-TOKEN-365") == 1
assert set(admit_cell["contents"]) == {WP13_ID, "focus-WP13", "kit-WP13", "W13-LOOSE-TOKEN-365"}
assert admit_inputs["carriedCargoItemIds"] == initial_wp13["carriedItemIds"]
assert admit_inputs["completeEnvelopeFitsCell"] is True
assert box_union([admit_after["actors"][WP13_ID]["bodyBoxWorld"], *[admit_after["items"][i]["worldBoundsFeet"] for i in initial_wp13["carriedItemIds"]]]) == admit_inputs["completeTravelerEnvelopeCellFeet"]
assert box_contains(admit_cell["bounds"], admit_inputs["completeTravelerEnvelopeCellFeet"])
drop = case["events"][11]
assert drop["before"]["cells"][CELL_WP13]["contents"].count("W13-LOOSE-TOKEN-365") == 1
assert drop["after"]["cells"][CELL_WP13]["contents"].count("W13-LOOSE-TOKEN-365") == 1
assert drop["after"]["items"]["W13-LOOSE-TOKEN-365"]["coordinateFrame"] == "cell-local-feet"
assert drop["after"]["cells"][CELL_WP13]["looseObjectIds"] == ["W13-LOOSE-TOKEN-365"]
cast_inputs = plane_shift_commit["authoredInputs"]
site_bounds = case["destinationSite"]["bounds"]
assert cast_inputs["carriedCargoItemIds"] == ["focus-WP13", "kit-WP13"]
assert "W13-LOOSE-TOKEN-365" not in cast_inputs["carriedCargoItemIds"]
assert cast_inputs["destinationFloorSupported"] and cast_inputs["cargoVolumesPairwiseDisjoint"] and cast_inputs["completeEnvelopeFitsDestination"]
assert box_union([cast_inputs["destinationBodyBox"], *[cast_inputs["destinationCargoMappings"][i]["worldBoundsFeet"] for i in cast_inputs["carriedCargoItemIds"]]]) == cast_inputs["destinationCompleteTravelerEnvelopeFeet"]
assert box_contains(site_bounds, cast_inputs["destinationCompleteTravelerEnvelopeFeet"])
assert cast_inputs["destinationCompleteTravelerEnvelopeFeet"]["z"][0] == 0
for item_id in cast_inputs["carriedCargoItemIds"]:
    assert plane_shift_success["after"]["items"][item_id]["worldBoundsFeet"] == cast_inputs["destinationCargoMappings"][item_id]["worldBoundsFeet"]
assert case["assertions"]["gateSourceProcedureBound"] and case["assertions"]["wp13GateCounterspellWindowAdjudicated"]
assert case["assertions"]["pt133ProspectiveOriginCommittedOnSuccess"] and case["assertions"]["completeCargoGeometryMapped"]

# W03 and identity/application boundaries remain honest.
assert case["assertions"]["w03SourceGapClosed"] is False
assert source_audit["witnessSources"]["W03"]["status"] == "SOURCE_HOLD_NO_QUALIFYING_ACCEPTED_SOURCE_FOUND"
assert queue["currentAuthority"]["reviewedApplied"] == 828 and queue["currentAuthority"]["pending"] == 20
assert queue["currentAuthority"]["acceptedUnapplied"] == 0
assert case["assertions"]["spellAccepted"] is False and case["assertions"]["spellApplied"] is False
assert case["assertions"]["applicationAuthorized"] is False

# Verify archive metadata and exact payload member hashes.
with zipfile.ZipFile(ARCHIVE) as zf:
    assert zf.testzip() is None
    names = zf.namelist()
    assert len(names) == len(set(names))
    manifest = json.loads(zf.read("MANIFEST.json"))
    assert len(names) == len(manifest["members"]) + 2
    checked = 0
    for member in manifest["members"]:
        data = zf.read(member["path"])
        assert len(data) == member["bytes"] and file_sha(data) == member["sha256"]
        assert f"{zlib.crc32(data) & 0xffffffff:08x}" == member["crc32"]
        checked += 1
    archived_case = json.loads(zf.read("W06_PLANESHIFT_ESCAPE_CASE_365_REPACK05.json"))
    assert archived_case == case
    assert file_sha(zf.read("prior/DD_Rank9_BanishmentGate_W07_GustCorpse_363_Repack01_TESTONLY.zip")) == w07_seal["archiveSha256"]
    assert file_sha(zf.read("prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_TESTONLY.zip")) == prior_w06_supersession["supersededArchiveSha256"]
    assert file_sha(zf.read("prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack02_TESTONLY.zip")) == prior_w06_repack02_supersession["supersededArchiveSha256"]
    assert file_sha(zf.read("prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack03_TESTONLY.zip")) == prior_w06_repack03_supersession["supersededArchiveSha256"]
    assert file_sha(zf.read("prior/DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack04_TESTONLY.zip")) == prior_w06_repack04_supersession["supersededArchiveSha256"]

delivery = load(OUT / "ARCHIVE_DELIVERY_365_REPACK05.json")
archive_bytes = ARCHIVE.read_bytes()
assert delivery["bytes"] == len(archive_bytes) and delivery["sha256"] == file_sha(archive_bytes)
assert delivery["memberCount"] == len(names) and delivery["zipTest"] == "PASS"

report = {
    "id": "PG327-W06-INDEPENDENT-AUDIT-365-REPACK05",
    "status": "PASS_TESTONLY_W06_PLANESHIFT_ESCAPE; DIRECTOR_REVIEW_REQUIRED",
    "archive": ARCHIVE.name,
    "archiveBytes": len(archive_bytes),
    "archiveSha256": file_sha(archive_bytes),
    "memberCount": len(names),
    "payloadHashesAndCrcsVerified": checked,
    "sourceBindings": len(source_bindings["bindings"]),
    "gitSourceBindings": len(source_bindings["planarTravelNewBindings"]),
    "eventCount": len(case["events"]),
    "forwardReplay": "PASS; changed-field-scoped operations with preconditions",
    "inverseReplay": "PASS; exact initial state restored in reverse order",
    "actualAdmissions": 2,
    "planeShiftCost": {"action": 1, "rp": 17, "components": ["V", "S", "F"]},
    "destination": "Known TEST_ONLY different-plane site; bounded, world-fixed, clear and fits the caster.",
    "cellA": "Primary escapes; cell closes once; remaining loose token is settled once at its fixed origin anchor.",
    "otherCellB": "Remains active with original deadline 62.05; Gate remains active to 600.2.",
    "w03": "OPEN SOURCE GAP; no fixture type assignment substituted",
    "spellAccepted": False,
    "spellApplied": False,
    "applicationAuthorized": False,
    "queueAuthority": "Queue361: 828 applied / 20 pending / 0 accepted-unapplied",
}
(OUT / "INDEPENDENT_AUDIT_365_REPACK05.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding=ENC)
print(json.dumps(report, ensure_ascii=False, indent=2))
