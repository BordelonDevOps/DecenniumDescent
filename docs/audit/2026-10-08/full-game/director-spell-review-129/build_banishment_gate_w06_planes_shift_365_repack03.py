from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import zipfile
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
W07_OUT = BASE / "banishment_gate_witness363_repack01"
W07_ZIP = W07_OUT / "DD_Rank9_BanishmentGate_W07_GustCorpse_363_Repack01_TESTONLY.zip"
W07_SEAL = BASE / "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json"
W02_SEAL = BASE / "PG327_W02_DIRECTOR_SEAL_364_REPACK03.json"
OUT = BASE / "banishment_gate_witness365_w06_planes_shift_repack03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack03_TESTONLY.zip"
ENC = "utf-8"
GATE_ID = "BG-W06-TESTONLY-GATE-365"
GUARD_ID = "Guard-W06-TESTONLY"
WP13_ID = "WP13-W06-TESTONLY"
CELL_GUARD_ID = "BG-W06-TESTONLY-CELL-GUARD-365"
CELL_WP13_ID = "BG-W06-TESTONLY-CELL-WP13-365"
ENCOUNTER_ID = "fixture:banishment-gate-w06-365"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding=ENC)


def read_json(path):
    return json.loads(path.read_text(encoding=ENC))


def pointer_parts(path):
    return [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")] if path else []


def get_at(obj, path):
    value = obj
    for part in pointer_parts(path):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def parent_at(obj, path):
    parts = pointer_parts(path)
    parent = obj
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


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


def scoped_patch(before, after):
    ops = []
    for path in changed_paths(before, after):
        old_present = True
        new_present = True
        try:
            old = copy.deepcopy(get_at(before, path))
        except (KeyError, IndexError):
            old_present = False
            old = None
        try:
            new = copy.deepcopy(get_at(after, path))
        except (KeyError, IndexError):
            new_present = False
            new = None
        if old_present:
            ops.append({"op": "test", "path": path, "value": old})
        if new_present:
            ops.append({"op": "replace" if old_present else "add", "path": path, "value": new})
        else:
            ops.append({"op": "remove", "path": path})
    return ops


def apply_patch(state, operations):
    current = copy.deepcopy(state)
    for op in operations:
        path, kind = op["path"], op["op"]
        if kind == "test":
            assert get_at(current, path) == op["value"], f"Precondition failed at {path}"
        else:
            parent, key = parent_at(current, path)
            if isinstance(parent, list):
                idx = int(key)
                if kind == "replace":
                    parent[idx] = copy.deepcopy(op["value"])
                elif kind == "remove":
                    parent.pop(idx)
                else:
                    raise AssertionError(f"List op unsupported at {path}: {kind}")
            elif kind == "add":
                assert key not in parent
                parent[key] = copy.deepcopy(op["value"])
            elif kind == "replace":
                assert key in parent
                parent[key] = copy.deepcopy(op["value"])
            elif kind == "remove":
                assert key in parent
                del parent[key]
            else:
                raise AssertionError(f"Unsupported patch operation {kind}")
    return current


if ARCHIVE.exists() or (OUT / "ARCHIVE_DELIVERY_365_REPACK03.json").exists():
    raise SystemExit(f"Refusing to overwrite a completed W06 delivery: {OUT}")
if not W07_ZIP.is_file() or not W07_SEAL.is_file() or not W02_SEAL.is_file():
    raise SystemExit("Sealed W07/W02 witness evidence is required before W06.")
PACK.mkdir(parents=True, exist_ok=True)

# Copy the exact source set whose Gate/Wizard/Guard mechanics passed sealed W07.
with zipfile.ZipFile(W07_ZIP) as w07z:
    w07_bindings = json.loads(w07z.read("SOURCE_BINDINGS_363.json"))
    w07_case = json.loads(w07z.read("W07_GUST_CORPSE_CASE_363.json"))
    w07_manifest_sha = file_sha(w07z.read("MANIFEST.json"))
    w07_source_bindings_sha = file_sha(w07z.read("SOURCE_BINDINGS_363.json"))
    binding_records = []
    for binding in w07_bindings["bindings"]:
        member = binding["packetMember"]
        data = w07z.read(member)
        dest = PACK / member
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        if binding.get("sourceCommit") == w07_bindings["sourceCommit"]:
            git_data = subprocess.check_output(["git", "show", f'{binding["sourceCommit"]}:{binding["repositoryPath"]}'], cwd=ROOT)
            assert git_data == data
        record = dict(binding)
        record["reusedFromW07ArchiveSha256"] = file_sha(W07_ZIP.read_bytes())
        record["reusedW07CaseId"] = w07_case["id"]
        binding_records.append(record)

source_commit = w07_bindings["sourceCommit"]
plane_model_path = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/planartravel6_reviewed_133/MODEL.json"
plane_actor_path = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/planartravel6_reviewed_133/ACTOR_PROFILES.json"
new_sources = []
for repo_path, member in ((plane_model_path, "sources/planartravel6/MODEL.json"), (plane_actor_path, "sources/planartravel6/ACTOR_PROFILES.json")):
    data = subprocess.check_output(["git", "show", f"{source_commit}:{repo_path}"], cwd=ROOT)
    dest = PACK / member
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    record = {
        "sourceCommit": source_commit,
        "repositoryPath": repo_path,
        "packetMember": member,
        "bytes": len(data),
        "gitSha256": file_sha(data),
        "workingTreeSha256": file_sha((ROOT / repo_path).read_bytes()),
        "bindingKind": "exact accepted Git source; independently checked by git show; later working-tree application edits are reported but are not substituted",
    }
    record["workingTreeMatchesBoundGit"] = record["workingTreeSha256"] == record["gitSha256"]
    binding_records.append(record)
    new_sources.append(record)

prior = PACK / "prior"
prior.mkdir(parents=True, exist_ok=True)
shutil.copyfile(W07_ZIP, prior / W07_ZIP.name)
shutil.copyfile(W07_SEAL, prior / W07_SEAL.name)
shutil.copyfile(W02_SEAL, prior / W02_SEAL.name)

W06_REPACK01_OUT = BASE / "banishment_gate_witness365_w06_planes_shift_repack01"
W06_REPACK01_ZIP = W06_REPACK01_OUT / "DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_TESTONLY.zip"
W06_REPACK01_DELIVERY = W06_REPACK01_OUT / "ARCHIVE_DELIVERY_365_REPACK01.json"
W06_REPACK01_AUDIT = W06_REPACK01_OUT / "INDEPENDENT_AUDIT_365_REPACK01.json"
for prior_path in (W06_REPACK01_ZIP, W06_REPACK01_DELIVERY, W06_REPACK01_AUDIT):
    if not prior_path.is_file():
        raise SystemExit(f"Missing immutable Repack01 history: {prior_path}")
    shutil.copyfile(prior_path, prior / prior_path.name)
W06_REPACK01_SHA256 = file_sha(W06_REPACK01_ZIP.read_bytes())
write_json(prior / "W06_REPACK01_SUPERSESSION_365.json", {
    "id": "PG327-W06-REPACK01-SUPERSESSION-365",
    "supersededArchive": W06_REPACK01_ZIP.name,
    "supersededArchiveSha256": W06_REPACK01_SHA256,
    "supersededDelivery": W06_REPACK01_DELIVERY.name,
    "supersededAudit": W06_REPACK01_AUDIT.name,
    "reason": "Repack01 is superseded for two reasons: its embedded TEST_ONLY wording assertion was too narrow, and its carried Wizard inventory did not follow the Wizard into Cell A. Repack03 corrects both and explicitly accounts for the released token weight.",
    "priorPacketSentToDirector": False,
    "campaignStateChanged": False,
})

W06_REPACK02_OUT = BASE / "banishment_gate_witness365_w06_planes_shift_repack02"
W06_REPACK02_ZIP = W06_REPACK02_OUT / "DD_Rank9_BanishmentGate_W06_PlaneShiftEscape_365_Repack02_TESTONLY.zip"
W06_REPACK02_DELIVERY = W06_REPACK02_OUT / "ARCHIVE_DELIVERY_365_REPACK02.json"
for prior_path in (W06_REPACK02_ZIP, W06_REPACK02_DELIVERY):
    if not prior_path.is_file():
        raise SystemExit(f"Missing immutable Repack02 history: {prior_path}")
    shutil.copyfile(prior_path, prior / prior_path.name)
W06_REPACK02_SHA256 = file_sha(W06_REPACK02_ZIP.read_bytes())
write_json(prior / "W06_REPACK02_SUPERSESSION_365.json", {
    "id": "PG327-W06-REPACK02-SUPERSESSION-365",
    "supersededArchive": W06_REPACK02_ZIP.name,
    "supersededArchiveSha256": W06_REPACK02_SHA256,
    "supersededDelivery": W06_REPACK02_DELIVERY.name,
    "reason": "The independent verification stopped before producing an audit because an equality assertion incorrectly required Repack01 snapshots to match after correcting inventory transit. Repack02 also retained the 0.1-lb token in WP13 load after dropping it. Repack03 corrects the mass transition and verifies the intended state deltas.",
    "independentAuditStatus": "NOT_PRODUCED; verification stopped at superseded-snapshot equality assertion",
    "priorPacketSentToDirector": False,
    "campaignStateChanged": False,
})

authority = PACK / "authority"
authority.mkdir(parents=True, exist_ok=True)
for name in ("CURRENT_SPELL_QUEUE_361.json", "PG327_W01_W08_WITNESS_PLAN_361.json", "PG327_W03_W06_W07_SOURCE_AUDIT_362.json"):
    shutil.copyfile(BASE / name, authority / name)
planar_acceptance = BASE / "PLANARTRAVEL6_EXACT_ACCEPTANCE_133.json"
planar_application = BASE / "PLANARTRAVEL6_APPLICATION_133.json"
planar_validation = BASE / "PLANARTRAVEL6_APPLICATION_VALIDATION_133.json"
for path in (planar_acceptance, planar_application, planar_validation):
    if not path.is_file():
        raise SystemExit(f"Missing Plane Shift acceptance/application authority: {path}")
    shutil.copyfile(path, authority / path.name)

catalog = json.loads((PACK / "sources/catalog.json").read_bytes())
w20_source = json.loads((PACK / "sources/WIZARD20_ACTOR_PROFILES.json").read_bytes())["Wizard20"]
w17_source = json.loads((PACK / "sources/W17_ACTOR_PROFILES.json").read_bytes())["profiles"][0]
guard_source = json.loads((PACK / "sources/bestiary_data_full.json").read_bytes())[326]
plane_model = json.loads((PACK / "sources/planartravel6/MODEL.json").read_bytes())
wp13_source = json.loads((PACK / "sources/planartravel6/ACTOR_PROFILES.json").read_bytes())["WP13"]
gate = next(x for x in catalog["spells"] if x.get("id") == "banishment-gate")
counterspell = next(x for x in catalog["spells"] if x.get("id") == "counterspell")["operational"]
plane_shift = plane_model["spells"][4]
plane_access = plane_shift["completeSourceAndAccess"]["classAccess"]["Wizard"]
source_audit = read_json(BASE / "PG327_W03_W06_W07_SOURCE_AUDIT_362.json")
queue = read_json(BASE / "CURRENT_SPELL_QUEUE_361.json")
plan = read_json(BASE / "PG327_W01_W08_WITNESS_PLAN_361.json")
w07_seal = read_json(W07_SEAL)
w02_seal = read_json(W02_SEAL)
pt_accept = read_json(planar_acceptance)
assert plane_shift["id"] == "plane-shift" and plane_access == {"rank": 7, "minimumClassLevel": 13, "school": "Conjuration", "baseRpCost": 17}
assert wp13_source["class"] == "Wizard" and wp13_source["classLevel"] == 13 and "plane-shift" in wp13_source["prepared"]
assert any(x.get("spellId") == "plane-shift" for x in wp13_source["spellbook"])
assert source_audit["witnessSources"]["W06"]["status"] == "SOURCE_ROUTE_APPROVED_WITNESS_OUTSTANDING"
assert w07_seal["decision"].startswith("W07 PASSES") and w02_seal["decision"].startswith("W02 PASSES")
assert "plane-shift" in pt_accept["acceptedIdentities"]
assert queue["currentAuthority"]["reviewedApplied"] == 828 and queue["currentAuthority"]["pending"] == 20

write_json(PACK / "W06_SOURCE_BINDINGS_365.json", {
    "id": "PG327-W06-SOURCE-BINDINGS-365",
    "sourceCommit": source_commit,
    "w07Reuse": {"archive": W07_ZIP.name, "archiveSha256": file_sha(W07_ZIP.read_bytes()), "manifestSha256": w07_manifest_sha, "sourceBindingsSha256": w07_source_bindings_sha},
    "planarTravelNewBindings": new_sources,
    "bindings": binding_records,
})
write_json(PACK / "W06_TESTONLY_FIXTURE_PREMISES_365.json", {
    "id": "OWNER-TESTONLY-BANISHMENT-GATE-W06-365",
    "scope": "One hypothetical W06 escape witness for Banishment Gate and the accepted Plane Shift route.",
    "classification": "TEST_ONLY deterministic fixture; no campaign occurrence, prior visit, destination knowledge, actor location, consent, or historical event is asserted.",
    "premises": {
        "WP13": "The source-qualified Wizard13 profile is instantiated as a finite TEST_ONLY actor with Humanoid type solely to exercise a matching Gate admission; this does not claim any type-changing mechanic or satisfy W03.",
        "destinationKnowledge": "WP13 has a prior personal TEST_ONLY record of the complete, bounded, world-fixed site on fixture:known-plane-beta. The record is a scenario premise, not a campaign discovery or canon-plane fact.",
        "willingness": "WP13 is willing to travel and is the Plane Shift caster, so caster-travel requirement is met without another traveler.",
        "originGeometry": "Only the declared Gate portal, two adjacent complete body tracks, and fixed clear origin anchor are present.",
        "destinationAndBlockers": "The known site is clear, supported, bounded, and fitting. No dimensional anchor, ward, suppression, or other actual transport blocker is present in this TEST_ONLY fixture.",
        "item": "W13-LOOSE-TOKEN-365 is a genuine unique TEST_ONLY object carried into Cell A, then released through the ordinary free object interaction before Plane Shift. It remains separate cargo and is not carried by the escaping caster."
    },
    "notAuthorizedOrAsserted": ["No spell identity acceptance/application.", "No W03 type-change source or creature-type transition.", "No named canonical plane, afterlife, cosmology, or runtime outcome.", "No Gate closure or change to another cell or the Gate clock."],
})

def stance(time, next_start):
    return {"id": "Mobile", "selectedAt": time, "expiresAtNextRegularStart": next_start, "noOpportunityAttackForFirstFiveFeetOfActualVoluntaryMovement": True, "grantsFreeMovement": False, "opportunityAttackDamageDieReduction": 1, "testOnlySelection": True}


def actor_common(actor_id, class_name, level, hp, max_hp, rp, max_rp, position, dimensions, speed, profile_path, profile_pointer, source_hash, conditions=None):
    x, y, h = dimensions
    cx, cy, z = position
    return {
        "id": actor_id, "class": class_name, "classLevel": level, "profilePath": profile_path, "profilePointer": profile_pointer,
        "profileSHA256": source_hash, "HP": hp, "maxHP": max_hp, "RP": rp, "maxRP": max_rp,
        "Dissonance": 0, "Refrain": 0, "preparedFamiliesUsed": [], "magicThisTurn": False,
        "spellHistory": [], "resourceHistory": [], "lastSpell": None, "concentration": None,
        "conditions": list(conditions or []), "death": {"status": "alive", "successes": 0, "failures": 0, "saveInputs": []},
        "plane": "fixture:origin", "position": position, "size": "Medium", "bodyDimensionsFeet": dimensions,
        "bodyBoxWorld": {"x": [cx - x / 2, cx + x / 2], "y": [cy - y / 2, cy + y / 2], "z": [z, z + h]},
        "orientation": "standing", "heldItems": [], "carriedItemIds": [], "hands": 2, "freeHands": ["left", "right"],
        "action": 0, "bonusAction": 0, "reaction": 1, "movement": 0, "movementSpeedFeet": speed,
        "movementHistory": [], "stance": None, "stanceHistory": [], "mobileFirstFiveFeetAllowance": None,
        "regularSchedule": None, "recharge": {}, "visible": True, "lineOfEffect": True,
    }


w20 = actor_common("W20", "Wizard", 20, 122, 122, 80, 80, [-50, 0, 0], [5, 5, 6], 30,
                   "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/ACTOR_PROFILES.json", "/Wizard20", file_sha((PACK / "sources/WIZARD20_ACTOR_PROFILES.json").read_bytes()))
w20["profileId"] = w20_source["id"]
w20.update({"preparedSpells": list(w20_source["prepared"]), "knownSpells": list(w20_source["spellbook"]), "focusId": "focus-W20", "heldItems": ["focus-W20"], "freeHands": ["right"], "voice": True,
             "counterspellAutomaticId": w20_source["automaticCards"][1]["id"], "counterspellReady": True, "counterspellRechargeRounds": 2,
             "recharge": {"wizard.base.counterspell": {"ready": True, "roundsUntilReady": 0, "rechargeRounds": 2, "lastUsed": None}},
             "regularSchedule": {"firstStart": 0.0, "period": 6.0, "endOffset": 0.9, "nextStart": 0.0, "nextEnd": 0.9, "starts": [], "ends": [], "budgetHistory": []},
             "fixturePremise": "TEST_ONLY Wizard20 with exact sealed W07 Gate acquisition/preparation binding."})
w17 = actor_common("W17", "Wizard", 17, 104, 104, 64, 64, [-26, 0, 0], [5, 5, 6], 30,
                   "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01/ACTOR_PROFILES.json", "/profiles/0", file_sha((PACK / "sources/W17_ACTOR_PROFILES.json").read_bytes()))
w17["profileId"] = w17_source["id"]
w17.update({"focusId": "focus-W17", "heldItems": ["focus-W17"], "freeHands": ["right"], "voice": True,
             "counterspellAutomaticId": "wizard.base.counterspell", "counterspellReady": True, "counterspellRechargeRounds": 2,
             "recharge": {"wizard.base.counterspell": {"ready": True, "roundsUntilReady": 0, "rechargeRounds": 2, "lastUsed": None}},
             "regularSchedule": {"firstStart": 1.0, "period": 6.0, "endOffset": 1.9, "nextStart": 1.0, "nextEnd": 1.9, "starts": [], "ends": [], "budgetHistory": []},
             "fixturePremise": "TEST_ONLY Wizard17; cost-free Counterspell decline at Gate cast, no campaign actor claim."})
guard = {
    "id": GUARD_ID, "profileId": "Guard", "profilePath": "src/bestiary_data_full.json", "profilePointer": "/326",
    "profileSHA256": file_sha((PACK / "sources/bestiary_data_full.json").read_bytes()), "name": guard_source["name"],
    "creatureType": guard_source["type"], "size": guard_source["size"], "speedFeet": 40, "armorClass": 15,
    "HP": 112, "maxHP": 112, "conditions": [], "movementPreventingConditions": [], "lifeClassification": "ALIVE_LIVING_TEST_ONLY_FIXTURE",
    "death": {"status": "alive", "successes": 0, "failures": 0, "saveInputs": []}, "plane": "fixture:origin", "position": [-2.5, -2.5, 0],
    "bodyDimensionsFeet": [5, 5, 6], "bodyBoxWorld": {"x": [-5, 0], "y": [-5, 0], "z": [0, 6]}, "orientation": "standing",
    "heldItems": [], "carriedItemIds": [], "action": 0, "bonusAction": 0, "reaction": 1, "movement": 0, "movementSpeedFeet": 40,
    "movementHistory": [], "stance": None, "stanceHistory": [], "mobileFirstFiveFeetAllowance": None,
    "regularSchedule": {"firstStart": 2.0, "period": 6.0, "endOffset": 2.9, "nextStart": 2.0, "nextEnd": 2.9, "starts": [], "ends": [], "budgetHistory": []},
    "fixturePremise": "Fresh hypothetical living Guard matching bound bestiary profile; no prior campaign state.",
}
wp13 = actor_common(WP13_ID, "Wizard", 13, 80, 80, 48, 48, [-2.5, 2.5, 0], [5, 5, 6], 30, plane_actor_path, "/WP13", file_sha((PACK / "sources/planartravel6/ACTOR_PROFILES.json").read_bytes()))
wp13.update({"profileId": "WP13", "sourceActorId": "WP13", "creatureType": "Humanoid", "creatureTypeClassification": "TEST_ONLY fixed matching type input; no type-change witness claimed",
              "abilities": wp13_source["abilities"], "PB": wp13_source["pb"], "baseAC": wp13_source["baseAC"],
              "preparedSpells": list(wp13_source["prepared"]), "spellbook": [x["spellId"] for x in wp13_source["spellbook"]],
              "focusId": "focus-WP13", "heldItems": ["focus-WP13", "W13-LOOSE-TOKEN-365"],
              "carriedItemIds": ["focus-WP13", "kit-WP13", "W13-LOOSE-TOKEN-365"], "freeHands": [], "voice": True,
              "loadLb": 10.1,
              "destinationKnowledge": {"siteId": "SITE-BETA-365", "planeId": "fixture:known-plane-beta", "personallyDocumentedBy": WP13_ID,
                                       "documentedBeforeCastVirtualMs": -1000, "worldFixedFrame": True, "fullBoundedSiteRecorded": True,
                                       "testOnlyPremise": True},
              "regularSchedule": {"firstStart": 3.0, "period": 6.0, "endOffset": 3.9, "nextStart": 3.0, "nextEnd": 3.9, "starts": [], "ends": [], "budgetHistory": []},
              "fixturePremise": "Source-qualified finite Wizard13 actor instantiated as a TEST_ONLY scene state, not a recovered campaign character."})

gate_opening = {"plane": "x=0", "y": [-5, 5], "z": [0, 15]}
destination_site = {"id": "SITE-BETA-365", "planeId": "fixture:known-plane-beta", "frameId": "fixture:world-fixed-frame-beta",
                    "worldFixed": True, "bounds": {"x": [-10, 10], "y": [-10, 10], "z": [0, 20]}, "floorSupported": True,
                    "terrain": "clear bounded floor; no walls, hazards, wards, occupants or hidden blockers", "testOnly": True}
initial = {
    "time": -0.1, "mode": "initiative", "fixture": {"id": "W06-TESTONLY-365", "campaignFact": False, "encounterId": ENCOUNTER_ID,
        "authorizationId": "OWNER-TESTONLY-BANISHMENT-GATE-W06-365", "fixtureOnlyCoordinatesAndTerrain": True},
    "actors": {"W20": w20, "W17": w17, GUARD_ID: guard, WP13_ID: wp13},
    "items": {
        "focus-W20": {"id": "focus-W20", "kind": "ordinaryWizardFocus", "ownerId": "W20", "heldBy": "W20", "hand": "left", "plane": "fixture:origin", "consumed": False},
        "focus-W17": {"id": "focus-W17", "kind": "ordinaryWizardFocus", "ownerId": "W17", "heldBy": "W17", "hand": "left", "plane": "fixture:origin", "consumed": False},
        "focus-WP13": {"id": "focus-WP13", "kind": "ordinaryWizardFocus", "ownerId": WP13_ID, "heldBy": WP13_ID, "hand": "left", "plane": "fixture:origin", "consumed": False},
        "kit-WP13": {"id": "kit-WP13", "kind": "ordinaryWizardKit", "ownerId": WP13_ID, "heldBy": WP13_ID, "weightLb": 10, "plane": "fixture:origin", "consumed": False},
        "W13-LOOSE-TOKEN-365": {"id": "W13-LOOSE-TOKEN-365", "kind": "genuineCopperToken", "ownerId": WP13_ID, "heldBy": WP13_ID, "weightLb": 0.1, "plane": "fixture:origin", "testOnly": True, "exists": True},
    },
    "destinationSites": {"SITE-BETA-365": destination_site},
    "effects": {}, "cells": {}, "crossingReceipts": {}, "hardDenialClaims": [], "transitHistory": [],
    "settlements": [], "pendingCast": None, "processedEventIds": [],
    "clocks": {"gateConcentrationDeadline": None, "cellDeadlines": {}, "otherIndependentDeadlines": {"fixture-independence-marker-365": 20.0}},
}
state = copy.deepcopy(initial)
events = []


def event(event_id, time, kind, narrative, source, inputs, mutate):
    global state
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    mutate(after)
    after["time"] = time
    after["processedEventIds"].append(event_id)
    rec = {"id": event_id, "time": time, "kind": kind, "narrative": narrative, "source": source, "authoredInputs": inputs,
           "before": before, "after": after, "beforeSHA256": sha(before), "afterSHA256": sha(after),
           "forward": scoped_patch(before, after), "inverse": scoped_patch(after, before)}
    assert apply_patch(state, rec["forward"]) == after
    state = after
    events.append(rec)


def start_w20(s):
    a = s["actors"]["W20"]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(0.0)
    a["regularSchedule"]["nextStart"] = 6.0
    a["regularSchedule"]["budgetHistory"].append({"time": 0.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})
    a["stance"] = stance(0.0, 6.0)
    a["stanceHistory"].append(a["stance"])
    a["mobileFirstFiveFeetAllowance"] = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "grantsFreeMovement": False, "expiresAtNextRegularStart": 6.0}


event("BG-W06-365:0", 0.0, "REGULAR_START", "W20 receives its ordinary scheduled turn and selects Mobile before its first relevant spell event.", "COMBAT_ACTION_PLAYTEST.md regular starts and Mobile stance", {"marker": 0.0, "refreshCount": 1, "stance": "Mobile", "expiresAt": 6.0}, start_w20)


def gate_commit(s):
    a = s["actors"]["W20"]
    a["action"] = 0
    a["RP"] = 54
    a["lastSpell"] = "banishment-gate"
    a["Dissonance"] = 0
    a["Refrain"] = 0
    a["preparedFamiliesUsed"] = ["banishment-gate"]
    a["magicThisTurn"] = True
    a["spellHistory"].append({"castId": f"{GATE_ID}/cast", "spellId": "banishment-gate", "class": "Wizard", "rank": 9, "school": "Abjuration", "time": 0.1,
                              "costRP": 26, "components": ["V", "S", "F"], "focusId": "focus-W20", "concentration": True,
                              "firstPreparedFamily": True, "baseDissonance": 0, "Dissonance": 0, "Refrain": 0, "target": None})
    a["resourceHistory"].append({"event": f"{GATE_ID}/cast", "RP": -26, "poolAfter": 54})
    a["concentration"] = f"{GATE_ID}/cast"
    s["pendingCast"] = {"castId": f"{GATE_ID}/cast", "casterId": "W20", "spellId": "banishment-gate", "committedAt": 0.1, "resolvesAt": 0.2,
                         "actionPaid": True, "rpPaid": 26, "componentsProvided": ["V", "S", "F"], "focusId": "focus-W20",
                         "counterspellWindow": {"opensBeforeEffect": True, "eligibleReactors": [{"actorId": "W17", "distanceFeet": 24, "rangeFeet": 60,
                               "perceivesCast": True, "lineOfEffect": True, "reactionAvailable": True, "rechargeReady": True, "currentRP": 64,
                               "costRP": 3, "componentsAvailable": ["V", "S", "F"], "focusId": "focus-W17", "decision": "declines",
                               "decisionPremise": "TEST_ONLY cooperative fixture; no campaign choice", "attempted": False, "reactionSpent": False,
                               "RPSpent": 0, "cooldownChanged": False}], "result": "W17 declines; Gate resolves"}}


event("BG-W06-365:1", 0.1, "CAST_COMMIT", "W20 pays and commits the bound Wizard Gate spell with source range/components/concentration; W17 is eligible to Counterspell and explicitly declines without cost.",
      "sealed W07 Gate/Wizard source bindings; Return327 PG9-Q01/Q14/Q15; Counterspell operational source; Wizard class engine", {
          "gatePoint": [0, 0, 7.5], "casterBasePosition": [-50, 0, 0], "rangeFeet": 120, "distanceFeet": 50.559,
          "selectedCreatureType": "Humanoid", "actionCost": 1, "rpCost": 26, "components": ["V", "S", "F"], "counterspellWindowResolvedBeforeEffect": True}, gate_commit)


def gate_resolve(s):
    s["pendingCast"] = None
    s["effects"][GATE_ID] = {"id": GATE_ID, "spellId": "banishment-gate", "creatorId": "W20", "creatorConcentration": f"{GATE_ID}/cast",
                             "status": "active", "createdAt": 0.2, "endsAt": 600.2, "selectedCreatureType": "Humanoid", "originPlane": "fixture:origin",
                             "originAnchor": {"plane": "fixture:origin", "gatePlane": "x=0", "opening": gate_opening}, "opening": gate_opening,
                             "concentration": True, "cells": [], "closeCount": 0, "admissions": []}
    s["clocks"]["gateConcentrationDeadline"] = 600.2


event("BG-W06-365:2", 0.2, "CAST_RESOLVE", "The fixed 10-by-15-foot Humanoid Gate opens after the interruption window; two nonoverlapping body tracks fit inside the aperture.",
      "Return327 PG9-Q14/Q15; BODY_EQUIPMENT_PLAYTEST.md occupied volumes", {"opening": gate_opening, "heightFeet": 15, "widthFeet": 10,
      "selectedCreatureType": "Humanoid", "guardTrackY": [-5, 0], "wp13TrackY": [0, 5], "tracksOverlap": False}, gate_resolve)


def w20_end(s):
    a = s["actors"]["W20"]
    a["regularSchedule"]["ends"].append(0.9)
    a["regularSchedule"]["nextEnd"] = 6.9
    a["action"] = a["bonusAction"] = a["movement"] = 0


event("BG-W06-365:3", 0.9, "TURN_END", "W20 ends its own scheduled turn; Gate concentration and its absolute clock remain active.", "COMBAT_ACTION_PLAYTEST.md regular-turn calendar", {"turnEnd": 0.9, "nextEnd": 6.9}, w20_end)


def start_w17(s):
    a = s["actors"]["W17"]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(1.0)
    a["regularSchedule"]["nextStart"] = 7.0
    a["regularSchedule"]["budgetHistory"].append({"time": 1.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})
    a["stance"] = stance(1.0, 7.0)
    a["stanceHistory"].append(a["stance"])
    a["mobileFirstFiveFeetAllowance"] = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "grantsFreeMovement": False, "expiresAtNextRegularStart": 7.0}


event("BG-W06-365:4", 1.0, "REGULAR_START", "W17 receives its one regular-turn budget and selects Mobile; the earlier Gate Counterspell decline spent no reaction, RP, or recharge.",
      "COMBAT_ACTION_PLAYTEST.md regular starts and Mobile stance; Counterspell source", {"marker": 1.0, "refreshCount": 1, "stance": "Mobile", "expiresAt": 7.0}, start_w17)


def end_w17(s):
    a = s["actors"]["W17"]
    a["regularSchedule"]["ends"].append(1.9)
    a["regularSchedule"]["nextEnd"] = 7.9
    a["action"] = a["bonusAction"] = a["movement"] = 0


event("BG-W06-365:5", 1.9, "TURN_END", "W17 ends its turn without spending a reaction or Counterspell recharge.", "COMBAT_ACTION_PLAYTEST.md regular-turn calendar", {"turnEnd": 1.9}, end_w17)


def start_guard(s):
    a = s["actors"][GUARD_ID]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 40
    a["regularSchedule"]["starts"].append(2.0)
    a["regularSchedule"]["nextStart"] = 8.0
    a["regularSchedule"]["budgetHistory"].append({"time": 2.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 40})
    a["stance"] = stance(2.0, 8.0)
    a["stanceHistory"].append(a["stance"])
    a["mobileFirstFiveFeetAllowance"] = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "grantsFreeMovement": False, "expiresAtNextRegularStart": 8.0}


event("BG-W06-365:6", 2.0, "REGULAR_START", "The Guard receives its scheduled 40-foot wallet and selects Mobile before movement.", "COMBAT_ACTION_PLAYTEST.md; bound Guard profile", {"marker": 2.0, "movement": 40, "stance": "Mobile", "expiresAt": 8.0}, start_guard)


def guard_cross(s):
    a = s["actors"][GUARD_ID]
    before_box = {"x": [-5, 0], "y": [-5, 0], "z": [0, 6]}
    after_box = {"x": [0, 5], "y": [-5, 0], "z": [0, 6]}
    a["movement"] = 35
    a["position"] = [2.5, -2.5, 0]
    a["movementHistory"].append({"time": 2.05, "from": [-2.5, -2.5, 0], "to": [2.5, -2.5, 0], "feetSpent": 5,
                                 "walletBefore": 40, "walletAfter": 35, "pathClear": True, "difficultTerrain": False,
                                 "movementPreventingCondition": False, "completeBodyCrossing": True, "gateId": GATE_ID})
    a["mobileFirstFiveFeetAllowance"].update({"usedFeet": 5, "remainingFeet": 0, "usedAt": 2.05, "opportunityAttacksPrevented": 0,
                                               "noOpportunityAttackTriggered": True})
    a["plane"] = CELL_GUARD_ID
    a["position"] = [0, 0, 0]
    a["bodyBoxWorld"] = {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 6]}
    s["cells"][CELL_GUARD_ID] = {"id": CELL_GUARD_ID, "parentGateId": GATE_ID, "primaryTargetId": GUARD_ID, "status": "active",
                                 "admittedAt": 2.05, "deadline": 62.05, "admissionPlusSeconds": 60, "localCenter": [0, 0],
                                 "bounds": {"x": [-7.5, 7.5], "y": [-7.5, 7.5], "z": [0, 15]}, "contents": [GUARD_ID], "closedAt": None, "closeCount": 0,
                                 "originAnchor": {"plane": "fixture:origin", "position": [-2.5, -2.5, 0], "bodyBox": after_box, "orientation": "standing"}}
    s["effects"][GATE_ID]["cells"].append(CELL_GUARD_ID)
    s["effects"][GATE_ID]["admissions"].append(CELL_GUARD_ID)
    crossing_id = f"{GATE_ID}/crossing/1"
    s["crossingReceipts"][crossing_id] = {"id": crossing_id, "targetId": GUARD_ID, "gateId": GATE_ID, "from": "fixture:origin", "to": CELL_GUARD_ID,
                                          "movementSource": "voluntary walking", "movementSpentFeet": 5, "walletBefore": 40, "walletAfter": 35,
                                          "bodyBoxBefore": before_box, "bodyBoxAfterBeforeExile": after_box, "completeBodyCrossing": True,
                                          "admittedAt": 2.05, "claimSpent": True, "claimKey": f"W20|{GUARD_ID}|{ENCOUNTER_ID}", "duplicateDeliveryCount": 0}
    s["hardDenialClaims"].append({"creatorId": "W20", "targetId": GUARD_ID, "encounterId": ENCOUNTER_ID, "claimId": "claim-Guard-365", "spentAt": 2.05})
    s["clocks"]["cellDeadlines"][CELL_GUARD_ID] = 62.05


event("BG-W06-365:7", 2.05, "VOLUNTARY_COMPLETE_CROSSING_AND_ADMISSION", "On its regular turn the Guard pays five feet (40 to 35) and fully crosses the Gate; the matching Humanoid is admitted into its own cell B.",
      "PG9-Q13/Q14/Q15/Q16; COMBAT_ACTION_PLAYTEST.md movement; BODY_EQUIPMENT_PLAYTEST.md occupied volume", {
          "fromBodyBox": {"x": [-5, 0], "y": [-5, 0], "z": [0, 6]}, "toBodyBox": {"x": [0, 5], "y": [-5, 0], "z": [0, 6]},
          "aperture": gate_opening, "movementSpentFeet": 5, "wallet": [40, 35], "completeBodyCrossing": True,
          "matchingType": "Humanoid", "testOnlyTypePremise": False, "admittedCell": CELL_GUARD_ID, "independentDeadline": 62.05}, guard_cross)


def end_guard(s):
    a = s["actors"][GUARD_ID]
    a["regularSchedule"]["ends"].append(2.9)
    a["regularSchedule"]["nextEnd"] = 8.9
    a["action"] = a["bonusAction"] = a["movement"] = 0


event("BG-W06-365:8", 2.9, "TURN_END", "Guard's regular slot ends; its admitted body and cell clock continue independently.", "COMBAT_ACTION_PLAYTEST.md regular-turn calendar", {"turnEnd": 2.9, "cellDeadline": 62.05}, end_guard)


def start_wp13(s):
    a = s["actors"][WP13_ID]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(3.0)
    a["regularSchedule"]["nextStart"] = 9.0
    a["regularSchedule"]["budgetHistory"].append({"time": 3.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})
    a["stance"] = stance(3.0, 9.0)
    a["stanceHistory"].append(a["stance"])
    a["mobileFirstFiveFeetAllowance"] = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "grantsFreeMovement": False, "expiresAtNextRegularStart": 9.0}


event("BG-W06-365:9", 3.0, "REGULAR_START", "WP13 receives its own scheduled Wizard13 turn, selects Mobile, and retains its source-qualified Plane Shift preparation and prior TEST_ONLY destination record.",
      "COMBAT_ACTION_PLAYTEST.md; Plane Travel6 WP13 preparation binding", {"marker": 3.0, "movement": 30, "stance": "Mobile", "expiresAt": 9.0,
      "prepared": ["plane-shift", "shield"], "destinationRecordPreexists": True}, start_wp13)


def wp13_cross(s):
    a = s["actors"][WP13_ID]
    before_box = {"x": [-5, 0], "y": [0, 5], "z": [0, 6]}
    after_box = {"x": [0, 5], "y": [0, 5], "z": [0, 6]}
    a["movement"] = 25
    a["mobileFirstFiveFeetAllowance"].update({"usedFeet": 5, "remainingFeet": 0, "usedAt": 3.05, "opportunityAttacksPrevented": 0,
                                               "noOpportunityAttackTriggered": True})
    a["movementHistory"].append({"time": 3.05, "from": [-2.5, 2.5, 0], "to": [2.5, 2.5, 0], "feetSpent": 5,
                                 "walletBefore": 30, "walletAfter": 25, "pathClear": True, "difficultTerrain": False,
                                 "movementPreventingCondition": False, "completeBodyCrossing": True, "gateId": GATE_ID})
    a["plane"] = CELL_WP13_ID
    a["position"] = [0, 0, 0]
    a["bodyBoxWorld"] = {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 6]}
    for item_id in ("focus-WP13", "kit-WP13", "W13-LOOSE-TOKEN-365"):
        s["items"][item_id]["plane"] = CELL_WP13_ID
    s["cells"][CELL_WP13_ID] = {"id": CELL_WP13_ID, "parentGateId": GATE_ID, "primaryTargetId": WP13_ID, "status": "active",
                                "admittedAt": 3.05, "deadline": 63.05, "admissionPlusSeconds": 60, "localCenter": [0, 0],
                                "bounds": {"x": [-7.5, 7.5], "y": [-7.5, 7.5], "z": [0, 15]},
                                "contents": [WP13_ID, "focus-WP13", "kit-WP13"], "looseObjectIds": [], "closedAt": None, "closeCount": 0,
                                "originAnchor": {"plane": "fixture:origin", "position": [-2.5, 2.5, 0], "bodyBox": after_box, "orientation": "standing"}}
    s["effects"][GATE_ID]["cells"].append(CELL_WP13_ID)
    s["effects"][GATE_ID]["admissions"].append(CELL_WP13_ID)
    crossing_id = f"{GATE_ID}/crossing/2"
    s["crossingReceipts"][crossing_id] = {"id": crossing_id, "targetId": WP13_ID, "gateId": GATE_ID, "from": "fixture:origin", "to": CELL_WP13_ID,
                                          "movementSource": "voluntary walking", "movementSpentFeet": 5, "walletBefore": 30, "walletAfter": 25,
                                          "bodyBoxBefore": before_box, "bodyBoxAfterBeforeExile": after_box, "completeBodyCrossing": True,
                                          "admittedAt": 3.05, "claimSpent": True, "claimKey": f"W20|{WP13_ID}|{ENCOUNTER_ID}", "duplicateDeliveryCount": 0}
    s["hardDenialClaims"].append({"creatorId": "W20", "targetId": WP13_ID, "encounterId": ENCOUNTER_ID, "claimId": "claim-WP13-365", "spentAt": 3.05})
    s["clocks"]["cellDeadlines"][CELL_WP13_ID] = 63.05


event("BG-W06-365:10", 3.05, "VOLUNTARY_COMPLETE_CROSSING_AND_ADMISSION", "On its regular turn WP13 pays five feet and completely crosses into the matching Gate, establishing its own primary cell A; the fixed type is only a TEST_ONLY match premise and establishes no W03 type-change source.",
      "PG9-Q13/Q14/Q15/Q16; COMBAT_ACTION_PLAYTEST.md movement; BODY_EQUIPMENT_PLAYTEST.md occupied volume; WP13 actor profile", {
          "fromBodyBox": {"x": [-5, 0], "y": [0, 5], "z": [0, 6]}, "toBodyBox": {"x": [0, 5], "y": [0, 5], "z": [0, 6]},
          "aperture": gate_opening, "movementSpentFeet": 5, "wallet": [30, 25], "completeBodyCrossing": True,
          "matchingType": "Humanoid", "testOnlyTypePremise": True, "admittedCell": CELL_WP13_ID, "independentDeadline": 63.05}, wp13_cross)


def drop_token(s):
    a = s["actors"][WP13_ID]
    token = s["items"]["W13-LOOSE-TOKEN-365"]
    token.update({"heldBy": None, "ownerId": None, "plane": CELL_WP13_ID, "cellLocalPosition": [5, 0, 0],
                  "itemBoundsLocal": {"x": [4.75, 5.25], "y": [-0.25, 0.25], "z": [0, 0.5]}, "status": "genuine loose object", "dropCount": 1})
    assert a["loadLb"] == 10.1 and token["weightLb"] == 0.1
    a["loadLb"] = round(a["loadLb"] - token["weightLb"], 1)
    a["heldItems"].remove("W13-LOOSE-TOKEN-365")
    a["carriedItemIds"].remove("W13-LOOSE-TOKEN-365")
    a["freeHands"].append("right")
    a["freeObjectInteractions"] = {"available": 0, "used": 1, "eventId": "BG-W06-365:11"}
    c = s["cells"][CELL_WP13_ID]
    c["contents"].append("W13-LOOSE-TOKEN-365")
    c["looseObjectIds"].append("W13-LOOSE-TOKEN-365")
    c["looseObjectAnchors"] = {"W13-LOOSE-TOKEN-365": {"cellLocalPosition": [5, 0, 0], "originPlanePosition": [7.5, 2.5, 0], "projectedFromPrimaryFixedAnchor": True}}


event("BG-W06-365:11", 3.06, "ORDINARY_FREE_OBJECT_INTERACTION_DROP", "WP13 uses its one ordinary free object interaction to leave a genuine unique token on the supported cell floor; it remains separate from the caster and will be settled at closure.",
      "COMBAT_ACTION_PLAYTEST.md ordinary free object interaction; BODY_EQUIPMENT_PLAYTEST.md item custody; BAN-CLOSE-03 looseObjectAnchors", {
          "itemId": "W13-LOOSE-TOKEN-365", "interaction": "drop", "ordinaryFreeInteractionCost": 1, "cellLocalPosition": [5, 0, 0],
          "fitsCurrentCell": True, "notCarriedByPlaneShiftGroup": True, "uniqueIdentity": True}, drop_token)


def plane_shift_commit(s):
    a = s["actors"][WP13_ID]
    a["action"] = 0
    a["RP"] = 31
    a["lastSpell"] = "plane-shift"
    a["Dissonance"] = 0
    a["Refrain"] = 0
    a["preparedFamiliesUsed"] = ["plane-shift"]
    a["magicThisTurn"] = True
    a["spellHistory"].append({"castId": "W06-365-PLANESHIFT-CAST", "spellId": "plane-shift", "class": "Wizard", "rank": 7,
                              "school": "Conjuration", "time": 3.1, "costRP": 17, "components": ["V", "S", "F"],
                              "focusId": "focus-WP13", "participants": [WP13_ID], "destinationSiteId": "SITE-BETA-365",
                              "firstPreparedFamily": True, "baseDissonance": 0, "Dissonance": 0, "Refrain": 0,
                              "preparedFamiliesUsedAfterCast": ["plane-shift"], "instantaneous": True})
    a["resourceHistory"].append({"event": "W06-365-PLANESHIFT-CAST", "RP": -17, "poolAfter": 31, "refund": 0})
    a["turnState"] = {"Action": "spent", "BonusAction": "ready", "Reaction": "available", "movementSpentFeet": 5, "freeObjectInteractionsUsed": 1}
    s["pendingCast"] = {"castId": "W06-365-PLANESHIFT-CAST", "casterId": WP13_ID, "spellId": "plane-shift", "rank": 7,
                         "committedAt": 3.1, "resolvesAt": 3.11, "actionPaid": True, "rpPaid": 17,
                         "componentsProvided": ["V", "S", "F"], "focusId": "focus-WP13", "participants": [WP13_ID],
                         "destination": {"siteId": "SITE-BETA-365", "planeId": "fixture:known-plane-beta", "frameId": "fixture:world-fixed-frame-beta",
                                         "coordinates": [0, 0, 0], "bounds": {"x": [-10, 10], "y": [-10, 10], "z": [0, 20]},
                                         "worldFixed": True, "personallyDocumentedBy": WP13_ID, "testOnlyPriorRecord": True,
                                         "nativeRangeFeet": 120, "participantDistanceFeet": 0, "rangeUsedForTravelDistance": False},
                         "counterspellWindow": {"opensAfterCommitBeforeEffect": True, "eligibleReactors": [],
                             "ineligible": [
                                 {"actorId": WP13_ID, "reason": "The caster cannot Counterspell its own cast."},
                                 {"actorId": "W20", "reason": "Outside Cell A; opaque cell boundary blocks perception and ordinary line of effect."},
                                 {"actorId": "W17", "reason": "Outside Cell A; opaque cell boundary blocks perception and ordinary line of effect."},
                                 {"actorId": GUARD_ID, "reason": "Inside a different opaque cell; no perception or line of effect to Cell A."}],
                             "result": "No eligible Counterspell reactor; no counter attempt."},
                         "knownBlockers": [], "hiddenBlockerSearch": False}


event("BG-W06-365:12", 3.1, "CAST_COMMIT", "WP13 legally commits its acquired, prepared Wizard13 Plane Shift from inside Cell A: Action, 17 RP and V/S/F paid; the caster is the sole willing participant and must travel. Its previously documented bounded world-fixed destination fits the complete body; the 120-foot range applies only to participant selection. Cell walls prevent any external Counterspell reactor from perceiving or targeting this cast.",
      "PlanarTravel6 MODEL.json#/spells/4/procedure and Wizard access; ACTOR_PROFILES.json#/WP13/spellbook/41,/prepared,/preparationHistory; exact acceptance 133; COMBAT_ACTION_PLAYTEST.md cast-interruption; BAN-CELL-03 boundary", {
          "spellId": "plane-shift", "class": "Wizard", "classLevel": 13, "school": "Conjuration", "rank": 7, "actionCost": 1, "rpCost": 17,
          "rpBeforeAfter": [48, 31], "components": ["V", "S", "F"], "focusHeld": True, "participants": [WP13_ID], "casterTravels": True,
          "participantDistanceFeet": 0, "nativeRangeFeet": 120, "destinationSiteId": "SITE-BETA-365", "siteKnownBeforeCast": True,
          "siteWorldFixed": True, "destinationBodyBox": {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 6]},
          "destinationBounds": destination_site["bounds"], "destinationClear": True, "transportBlockers": [], "eligibleCounterspellReactors": []}, plane_shift_commit)


def plane_shift_escape_and_close_cell_a(s):
    a = s["actors"][WP13_ID]
    a["plane"] = "fixture:known-plane-beta"
    a["position"] = [0, 0, 0]
    a["bodyBoxWorld"] = {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 6]}
    a["transitHistory"] = [{"transitId": "W06-365-PLANESHIFT-TRANSIT", "spellId": "plane-shift", "fromCell": CELL_WP13_ID,
                             "toPlane": "fixture:known-plane-beta", "destinationSiteId": "SITE-BETA-365", "resolvedAt": 3.11,
                             "participants": [WP13_ID], "identityPreserved": True, "originalInventoryPreserved": True, "duration": "Instantaneous"}]
    for item_id in ("focus-WP13", "kit-WP13"):
        s["items"][item_id]["plane"] = "fixture:known-plane-beta"
        s["items"][item_id]["heldBy"] = WP13_ID
    s["items"]["W13-LOOSE-TOKEN-365"].update({"plane": "fixture:origin", "position": [7.5, 2.5, 0], "heldBy": None,
                                               "ownerId": None, "settlementCount": 1, "settlementSourceCell": CELL_WP13_ID,
                                               "settledAt": 3.11, "placement": "legal same-anchor object placement"})
    cell = s["cells"][CELL_WP13_ID]
    cell.update({"status": "destroyed", "closedAt": 3.11, "closeCount": 1, "closureReason": "primary legally escaped by Plane Shift",
                 "escapedPrimaryId": WP13_ID, "settledContents": ["W13-LOOSE-TOKEN-365"], "settledContentIds": ["W13-LOOSE-TOKEN-365"],
                 "settlementCounts": {"W13-LOOSE-TOKEN-365": 1}, "activeContents": [], "cellDestroyedDespiteNoReturnOfPrimary": True})
    gate_state = s["effects"][GATE_ID]
    gate_state["cells"].remove(CELL_WP13_ID)
    gate_state["admissions"].remove(CELL_WP13_ID)
    gate_state["escapeHistory"] = [{"primaryId": WP13_ID, "cellId": CELL_WP13_ID, "spellId": "plane-shift", "escapedAt": 3.11,
                                    "cellClosedImmediately": True, "otherCellIdsUnchanged": [CELL_GUARD_ID], "gateRemainsActive": True,
                                    "escapedPrimaryRecalled": False, "closureCount": 1}]
    s["settlements"].append({"settlementId": "W06-365-CELL-A-CLOSE", "cellId": CELL_WP13_ID, "trigger": "primary legal escape",
                             "resolvedAt": 3.11, "escapedPrimaryId": WP13_ID, "remainingContents": [{"id": "W13-LOOSE-TOKEN-365", "kind": "object", "outcome": "placed once at projected anchor", "count": 1}],
                             "cellDestroyed": True, "sameIdentityPreserved": True})
    s["clocks"]["otherIndependentDeadlines"]["fixture-independence-marker-365"] = 20.0
    s["pendingCast"] = None


event("BG-W06-365:13", 3.11, "PLANE_SHIFT_SUCCESS_AND_PRIMARY_ESCAPE_CELL_CLOSURE", "Plane Shift instantly carries the same WP13 identity and its carried focus/kit to the documented site. The primary's Banishment application ends immediately; Cell A closes exactly once, and the remaining genuine loose token is mandatorily returned to its projected fixed-origin anchor exactly once. The Gate, Guard's separate live Cell B and their independent clocks remain unchanged.",
      "Plane Shift source procedure; PG9-Q15/Q17; BAN-CLOSE-03/BAN-PLACEMENT-HANDOFF-03; unchanged Gate/cell clocks", {
          "escapedPrimaryId": WP13_ID, "escapeSource": "plane-shift", "destination": "fixture:known-plane-beta/SITE-BETA-365", "cellAClosedOnce": True,
          "tokenSettlementCount": 1, "tokenOriginAnchor": [7.5, 2.5, 0], "gateRemainsActive": True, "gateDeadlineBeforeAfter": [600.2, 600.2],
          "otherCellId": CELL_GUARD_ID, "otherCellStatusBeforeAfter": ["active", "active"], "otherCellDeadlineBeforeAfter": [62.05, 62.05],
          "otherCellCloseCount": 0, "independentFixtureClockBeforeAfter": [20.0, 20.0], "primaryRecalled": False}, plane_shift_escape_and_close_cell_a)


case = {
    "id": "W06_PLANESHIFT_ESCAPE_CASE_365_REPACK03", "witnessId": "W06", "spellId": "banishment-gate", "escapeSpellId": "plane-shift",
    "sourceCommit": source_commit, "status": "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED", "holdIds": ["PG200-B04"],
    "scenarioQualification": "Hypothetical TEST_ONLY evidence only; it establishes neither campaign events nor a Gate identity disposition.",
    "fixturePremises": read_json(PACK / "W06_TESTONLY_FIXTURE_PREMISES_365.json"),
    "sourceBindings": {"Gate": {"sourcePath": source_audit["witnessSources"]["W06"]["source"]["path"], "selectedType": "Humanoid", "baseRpCost": 26},
                       "PlaneShift": {"modelPath": plane_model_path, "procedurePointer": "/spells/4/procedure", "modelGitSha256": new_sources[0]["gitSha256"],
                                      "accessPointer": "/spells/4/completeSourceAndAccess/classAccess/Wizard", "actorProfilePath": plane_actor_path,
                                      "actorProfilePointer": "/WP13", "actorProfileGitSha256": new_sources[1]["gitSha256"], "accepted": True}},
    "supersedesSubmissions": [
        {"archive": W06_REPACK01_ZIP.name, "archiveSha256": W06_REPACK01_SHA256, "reason": "corrected embedded verifier wording and inventory transit across Gate"},
        {"archive": W06_REPACK02_ZIP.name, "archiveSha256": W06_REPACK02_SHA256, "reason": "corrected dropped-token load by 0.1 lb and updated independent validation for intended state changes"},
    ],
    "destinationKnowledge": copy.deepcopy(wp13["destinationKnowledge"]),
    "destinationSite": destination_site,
    "initial": initial, "events": events, "final": state,
    "initialSHA256": sha(initial), "finalSHA256": sha(state), "inverseRestorationOrder": [e["id"] for e in reversed(events)],
    "assertions": {"actualGateAdmissionForEscapingPrimary": True, "planeShiftAcquiredAndPrepared": True, "planeShiftActionPaid": True,
                   "planeShiftRP17Paid": True, "componentsVSTFProvided": True, "casterTravels": True, "knownDifferentPlaneSite": True,
                   "destinationFitsAndClear": True, "escapeCounterspellOpportunityEvaluated": True, "primaryIdentityPreserved": True,
                   "primaryCellClosedOnce": True, "remainingLooseObjectSettledOnce": True, "objectIdentityDuplicated": False,
                   "gateRemainsActive": True, "otherCellRemainsActive": True, "otherCellClockUnchanged": True,
                   "gateConcentrationClockUnchanged": True, "independentClockUnchanged": True,
                   "w03SourceGapClosed": False, "spellAccepted": False, "spellApplied": False, "applicationAuthorized": False},
    "coverage": {"W06": "actual admission followed by acquired Plane Shift escape and single-cell closure submitted",
                 "W07": "sealed PASS preserved unchanged as prior evidence", "W02": "sealed PASS preserved unchanged",
                 "W03": "open source gap; no TEST_ONLY creature-type premise substitutes", "W01": "not evidenced by this packet",
                 "W04": "not evidenced by this packet", "W05": "not evidenced by this packet", "W08": "not evidenced by this packet"},
    "dispositionBoundary": {"gate": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False,
                            "queue": "Queue361 828 applied / 20 pending / 0 accepted-unapplied"},
}
write_json(PACK / "W06_PLANESHIFT_ESCAPE_CASE_365_REPACK03.json", case)

readme = """# Banishment Gate W06 TEST_ONLY Plane Shift escape witness 365 Repack03

This packet submits W06 only. It reuses the exact sealed W07 Gate/Wizard/Guard source set, and adds the exact accepted Plane Shift model and WP13 acquisition/preparation profile. Prior W07 and W02 seals are preserved. The spell identity remains HOLD; no acceptance, application, campaign event, canonical plane, or runtime result is asserted.

W20 opens a Humanoid Gate using its bound Wizard source, Action, 26 RP, V/S/F, concentration, range, and interruption opportunity. W17 is in range with Counterspell and explicitly declines without cost. A living Guard crosses during its scheduled turn and occupies its own cell B. Later, the source-qualified Wizard13 profile is instantiated only as a TEST_ONLY actor with a fixed Humanoid matching premise; the case claims no type-changing source and does not close W03. WP13 spends five actual movement feet through the aperture and is admitted as the primary of cell A.

In cell A, WP13 drops a unique genuine TEST_ONLY token through its one ordinary free object interaction. WP13 then pays the acquired and prepared Plane Shift Action, 17 RP and V/S/F. The sole participant is the caster, who travels as required. Its personally documented destination is an explicitly TEST_ONLY complete, bounded, world-fixed site on a different fixture plane; the body fits and the site has no blockers. The 120-foot source range is used for participant selection, not travel distance. The counterspell window is assessed: no external creature can perceive or establish ordinary line of effect through the opaque cell wall, and the caster cannot counter its own spell.

Plane Shift preserves WP13, carried focus/kit and the destination; the escaped primary is not recalled. Cell A closes once. The remaining loose token returns to its projected fixed origin anchor once, with the same object identity. Gate concentration and Gate deadline remain unchanged. Guard and cell B remain in place with the original independent 60-second deadline unchanged. The unrelated fixture clock also remains unchanged.

The packet provides complete ordered before/after state, canonical hashes, field-scoped forward/inverse patches, exact reverse restoration, bounded geometry, clock comparisons, source bindings, W01-W08 coverage, manifest, delivery, and an independent verifier. Repack03 fixes inventory transit through Gate and records WP13 load decreasing from 10.1 lb to 10.0 lb when the 0.1-lb token is dropped. It supersedes two unsent drafts and is evidence for one W06 branch only; it neither resolves the W03 source gap nor accepts or applies Banishment Gate.
"""
(PACK / "README.md").write_text(readme, encoding=ENC)

verifier_source = BASE / "verify_banishment_gate_w06_planes_shift_365_repack03.py"
verifier_member = PACK / "verification/verify_banishment_gate_w06_planes_shift_365_repack03.py"
verifier_member.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(verifier_source, verifier_member)

members = sorted(p for p in PACK.rglob("*") if p.is_file() and p.name not in {"MANIFEST.json", "DELIVERY.json"})
manifest = {"id": "PG327-W06-MANIFEST-365-REPACK03", "packetId": "DD-RANK9-BANISHMENT-GATE-W06-PLANESHIFT-365-TESTONLY",
            "sourceCommit": source_commit, "scope": "W06 Plane Shift escape from one primary cell only", "members": [
                {"path": p.relative_to(PACK).as_posix(), "bytes": p.stat().st_size, "sha256": file_sha(p.read_bytes()), "crc32": f"{zlib.crc32(p.read_bytes()) & 0xffffffff:08x}"} for p in members]}
write_json(PACK / "MANIFEST.json", manifest)
delivery = {"id": "PG327-W06-DELIVERY-365-REPACK03", "packetId": manifest["packetId"], "archive": ARCHIVE.name,
            "scope": ["banishment-gate/W06"], "requestedDirectorAction": "Audit W06 only. Seal W06 if the paid Plane Shift escape, primary-cell closure, one-time remaining-content settlement, and unchanged Gate/other-cell clocks pass; otherwise return exact defects.",
            "spellDispositionRequested": "NONE", "applicationRequested": False,
            "authority": {"queue": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0, "heldIds": ["banishment-gate"], "blockers": ["PG200-B03", "PG200-B04"]},
            "preservedWitnessSeals": ["W07 sealed PASS", "W02 sealed PASS"], "sourceGap": {"id": "W03", "status": "OPEN; fixture type premise does not satisfy it"}, "members": manifest["members"]}
write_json(PACK / "DELIVERY.json", delivery)

with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(p for p in PACK.rglob("*") if p.is_file()):
        zf.write(path, path.relative_to(PACK).as_posix())
with zipfile.ZipFile(ARCHIVE) as zf:
    infos = zf.infolist()
    names = [x.filename for x in infos]
    assert len(names) == len(set(names)) and zf.testzip() is None
    assert sorted(names) == sorted(p.relative_to(PACK).as_posix() for p in PACK.rglob("*") if p.is_file())
    for entry in manifest["members"]:
        data = zf.read(entry["path"])
        assert file_sha(data) == entry["sha256"] and f"{zlib.crc32(data) & 0xffffffff:08x}" == entry["crc32"]
archive_bytes = ARCHIVE.read_bytes()
write_json(OUT / "ARCHIVE_DELIVERY_365_REPACK03.json", {"id": "PG327-W06-ARCHIVE-DELIVERY-365-REPACK03", "archive": ARCHIVE.name,
    "bytes": len(archive_bytes), "sha256": file_sha(archive_bytes), "crc32": f"{zlib.crc32(archive_bytes) & 0xffffffff:08x}",
    "memberCount": len(infos), "uniqueMembers": True, "memberHashesAndCrcsVerified": True, "zipTest": "PASS", "caseEvents": len(events),
    "directorDisposition": "W06 evidence only; Gate remains HOLD; no acceptance or application"})
print(json.dumps({"archive": str(ARCHIVE), "bytes": len(archive_bytes), "sha256": file_sha(archive_bytes), "members": len(infos),
                  "events": len(events), "initialSHA256": sha(initial), "finalSHA256": sha(state)}, ensure_ascii=False, indent=2))
