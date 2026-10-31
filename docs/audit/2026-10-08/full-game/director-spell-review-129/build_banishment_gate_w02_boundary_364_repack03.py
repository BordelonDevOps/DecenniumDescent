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
OUT = BASE / "banishment_gate_witness364_repack03"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W02_Boundary_364_Repack03_TESTONLY.zip"
ENC = "utf-8"


def canon_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canon_bytes(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding=ENC)


def read_json(path):
    return json.loads(path.read_text(encoding=ENC))


def pointer_parts(path):
    return [p.replace("~1", "/").replace("~0", "~") for p in path.lstrip("/").split("/")] if path else []


def pointer_get(state, path):
    value = state
    for part in pointer_parts(path):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def pointer_parent(state, path):
    parts = pointer_parts(path)
    if not parts:
        raise AssertionError("Root-path mutation is forbidden")
    parent = state
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


def pointer_join(path, key):
    encoded = str(key).replace("~", "~0").replace("/", "~1")
    return f"{path}/{encoded}"


def scoped_patch(before, after):
    current = copy.deepcopy(before)
    operations = []

    def recurse(old, new, path):
        nonlocal current
        if type(old) is dict and type(new) is dict:
            obj = pointer_get(current, path)
            for key in sorted(old.keys() & new.keys()):
                recurse(old[key], new[key], pointer_join(path, key))
                obj = pointer_get(current, path)
            for key in sorted(old.keys() - new.keys()):
                target = pointer_join(path, key)
                value = copy.deepcopy(obj[key])
                operations.extend([{"op": "test", "path": target, "value": value}, {"op": "remove", "path": target}])
                del obj[key]
                obj = pointer_get(current, path)
            for key in sorted(new.keys() - old.keys()):
                target = pointer_join(path, key)
                operations.extend([
                    {"op": "test", "path": path, "value": copy.deepcopy(obj)},
                    {"op": "add", "path": target, "value": copy.deepcopy(new[key])},
                ])
                obj[key] = copy.deepcopy(new[key])
                obj = pointer_get(current, path)
            return
        if type(old) is type(new) and old == new:
            return
        if not path:
            raise AssertionError("Root replacement is forbidden")
        operations.extend([
            {"op": "test", "path": path, "value": copy.deepcopy(old)},
            {"op": "replace", "path": path, "value": copy.deepcopy(new)},
        ])
        parent, key = pointer_parent(current, path)
        if isinstance(parent, list):
            parent[int(key)] = copy.deepcopy(new)
        else:
            parent[key] = copy.deepcopy(new)

    recurse(before, after, "")
    assert all(op["path"] for op in operations)
    return operations


def apply_patch(state, operations):
    current = copy.deepcopy(state)
    for operation in operations:
        path, kind = operation["path"], operation["op"]
        if not path:
            raise AssertionError("Root-path patch is forbidden")
        if kind == "test":
            if pointer_get(current, path) != operation["value"]:
                raise AssertionError(f"Precondition failed at {path}")
        elif kind == "replace":
            parent, key = pointer_parent(current, path)
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                if key not in parent:
                    raise AssertionError(f"Replace target missing at {path}")
                parent[key] = copy.deepcopy(operation["value"])
        elif kind == "add":
            parent, key = pointer_parent(current, path)
            if not isinstance(parent, dict) or key in parent:
                raise AssertionError(f"Add target is not an absent field at {path}")
            parent[key] = copy.deepcopy(operation["value"])
        elif kind == "remove":
            parent, key = pointer_parent(current, path)
            if not isinstance(parent, dict) or key not in parent:
                raise AssertionError(f"Remove target missing at {path}")
            del parent[key]
        else:
            raise AssertionError(f"Unsupported patch operation: {kind}")
    return current


if OUT.exists():
    if ARCHIVE.exists() or (OUT / "ARCHIVE_DELIVERY_364_REPACK03.json").exists():
        raise SystemExit(f"Refusing to overwrite an existing W02 delivery: {OUT}")
    if any(p.is_file() for p in OUT.iterdir() if p.name != "packet"):
        raise SystemExit(f"Refusing to overwrite unrecognized output beside packet: {OUT}")
if not W07_ZIP.is_file() or not W07_SEAL.is_file():
    raise SystemExit("The exact sealed W07 Repack01 archive and local ruling record are required.")
PACK.mkdir(parents=True, exist_ok=True)

# Reuse the exact Git-bound sources and authority members from the sealed W07 packet.
with zipfile.ZipFile(W07_ZIP) as w07z:
    w07_manifest = json.loads(w07z.read("MANIFEST.json"))
    w07_bindings = json.loads(w07z.read("SOURCE_BINDINGS_363.json"))
    w07_case = json.loads(w07z.read("W07_GUST_CORPSE_CASE_363.json"))
    W07_MANIFEST_SHA256 = file_sha(w07z.read("MANIFEST.json"))
    W07_SOURCE_BINDINGS_SHA256 = file_sha(w07z.read("SOURCE_BINDINGS_363.json"))
    source_binding_records = []
    for binding in w07_bindings["bindings"]:
        member = binding["packetMember"]
        data = w07z.read(member)
        destination = PACK / member
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if destination.read_bytes() != data:
                raise SystemExit(f"Existing copied source differs from sealed W07 member: {destination}")
        else:
            destination.write_bytes(data)
        copied = dict(binding)
        copied["reusedFromW07ArchiveSha256"] = file_sha(W07_ZIP.read_bytes())
        copied["reusedW07CaseId"] = w07_case["id"]
        if binding.get("sourceCommit") == w07_bindings["sourceCommit"]:
            expected = subprocess.check_output(
                ["git", "show", f'{binding["sourceCommit"]}:{binding["repositoryPath"]}'],
                cwd=ROOT,
            )
            assert data == expected
        source_binding_records.append(copied)

prior_dir = PACK / "prior"
prior_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(W07_ZIP, prior_dir / "W07_Repack01_TESTONLY.zip")
shutil.copyfile(W07_SEAL, prior_dir / "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json")
W02_REPACK02 = BASE / "banishment_gate_witness364_repack02/DD_Rank9_BanishmentGate_W02_Boundary_364_Repack02_TESTONLY.zip"
W02_HOLD_REPACK02 = BASE / "PG327_W02_DIRECTOR_HOLD_364_REPACK02.json"
if not W02_REPACK02.is_file() or not W02_HOLD_REPACK02.is_file():
    raise SystemExit("The prior W02 Repack02 archive and Director HOLD record are required as immutable history.")
W02_REPACK02_SHA256 = file_sha(W02_REPACK02.read_bytes())
W02_REPACK02_HOLD = read_json(W02_HOLD_REPACK02)
assert W02_REPACK02_SHA256 == "d96a01218398630ec54366cd473dd9adfb641ec962b0ca4b8b7df507d61d17e6"
assert W02_REPACK02_HOLD["rulingId"] == "PG327-W02-364-REPACK02-DIRECTOR-HOLD"
assert {item["id"] for item in W02_REPACK02_HOLD["residuals"]} == {"W02-364-R1", "W02-364-R2"}
shutil.copyfile(W02_REPACK02, prior_dir / W02_REPACK02.name)
shutil.copyfile(W02_HOLD_REPACK02, prior_dir / W02_HOLD_REPACK02.name)
W07_ARCHIVE_SHA256 = file_sha(W07_ZIP.read_bytes())
W07_SEAL_DATA = read_json(W07_SEAL)
assert W07_SEAL_DATA["rulingId"] == "PG327-W07-363-REPACK01-DIRECTOR-SEAL"
assert W07_SEAL_DATA["decision"].startswith("W07 PASSES")
assert W07_SEAL_DATA["archiveSha256"] == W07_ARCHIVE_SHA256
write_json(PACK / "W07_SOURCE_REUSE_364.json", {
    "id": "PG327-W02-W07-SEALED-SOURCE-REUSE-364",
    "w07Archive": W07_ZIP.name,
    "w07ArchiveBytes": W07_ZIP.stat().st_size,
    "w07ArchiveSha256": W07_ARCHIVE_SHA256,
    "w07ManifestSha256": W07_MANIFEST_SHA256,
    "w07SourceBindingsSha256": W07_SOURCE_BINDINGS_SHA256,
    "w07CaseId": w07_case["id"],
    "w07DirectorRulingId": W07_SEAL_DATA["rulingId"],
    "reusedBindings": source_binding_records,
    "reuseRule": "Every reused source member is byte-identical to the member verified by sealed W07 Repack01; Git-bound members are rechecked against the cited source commit.",
})
write_json(PACK / "W02_REPACK02_HOLD_PROVENANCE_364.json", {
    "id": "PG327-W02-REPACK02-HOLD-PROVENANCE-364-REPACK03",
    "priorArchive": W02_REPACK02.name,
    "priorArchiveSha256": W02_REPACK02_SHA256,
    "directorHoldRecord": W02_HOLD_REPACK02.name,
    "directorRulingId": W02_REPACK02_HOLD["rulingId"],
    "closedByThisRepack": ["W02-364-R1", "W02-364-R2"],
    "immutability": "Repack02 and its HOLD ruling are included byte-for-byte as historical evidence and are not overwritten.",
})
write_json(PACK / "W02_OWNER_TESTONLY_AUTHORIZATION_364.json", {
    "id": "OWNER-TESTONLY-BANISHMENT-GATE-W02-364",
    "scope": "One hypothetical Banishment Gate W02 boundary-geometry witness only",
    "authorizationBasis": "User-authorized TEST_ONLY witness fixtures and GPT Director's concrete W02 construction in the current review thread.",
    "premises": [
        "A new hypothetical living Guard TEST_ONLY actor matching the bound Guard profile, opened at 112/112 HP.",
        "Fixture-only turn order, coordinates, movement wallet, unobstructed terrain and no other occupying bodies.",
        "No campaign event, real-world person, actual consent or runtime execution is asserted.",
    ],
    "notAuthorizedOrAsserted": [
        "No spell identity acceptance or application.",
        "No Gate blocker is closed by W02 alone.",
        "No type-change source, escape effect, admission, cell, hard-denial claim or return event is asserted.",
    ],
})

# Read exact source bytes from W07-reused members and derive active profile hashes.
def source_for_repo_path(repo_path):
    match = next(b for b in source_binding_records if b.get("repositoryPath") == repo_path)
    return (PACK / match["packetMember"]).read_bytes(), match


catalog_path = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
w20_path = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/ACTOR_PROFILES.json"
w17_path = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01/ACTOR_PROFILES.json"
guard_path = "src/bestiary_data_full.json"
catalog_bytes, catalog_binding = source_for_repo_path(catalog_path)
w20_bytes, w20_binding = source_for_repo_path(w20_path)
w17_bytes, w17_binding = source_for_repo_path(w17_path)
guard_bytes, guard_binding = source_for_repo_path(guard_path)
catalog = json.loads(catalog_bytes)
w20_data = json.loads(w20_bytes)["Wizard20"]
w17_data = json.loads(w17_bytes)["profiles"][0]
guard_profile = json.loads(guard_bytes)[326]
spell_list = catalog["spells"]
gate_card = next(s for s in spell_list if s.get("id") == "banishment-gate")
counterspell = next(s for s in spell_list if s.get("id") == "counterspell")["operational"]
assert w20_data["id"] == "PG200-W20" and w20_data["classLevel"] == 20
assert "banishment-gate" in w20_data["spellbook"] and "banishment-gate" in w20_data["prepared"]
assert w20_data["rpMaximum"] == 80 and w20_data["hpMaximum"] == 122
assert w17_data["id"] == "W17-f7ae29175032" and w17_data["classLevel"] == 17
assert w17_data["maximumHP"] == 104 and w17_data["PB"] == 6
assert guard_profile["name"] == "Guard" and guard_profile["type"] == "Humanoid"
assert guard_profile["size"] == "Medium" and guard_profile["hitPoints"] == 112
assert guard_profile["speed"] == "40 ft." and guard_profile["combat"]["draft"] is False
assert gate_card["classAccess"]["Wizard"]["baseRpCost"] == 26
assert counterspell["rangeFeet"] == 60 and counterspell["components"] == ["V", "S", "F"]
assert w20_data["automaticCards"][1]["id"] == "wizard.base.counterspell"
assert w17_data["automaticCards"][1]["id"] == "wizard.base.counterspell"
assert "always-prepared class matrices" in (PACK / "sources/rules/WIZARD_CLASS_ENGINE.md").read_text(encoding=ENC)
assert "within120ft" in (PACK / "sources/RETURN327_banishment-gate.json").read_text(encoding=ENC)
assert "complete qualifying" in (PACK / "sources/RETURN327_banishment-gate.json").read_text(encoding=ENC)
assert "would cross its plane" in (PACK / "sources/RETURN327_banishment-gate.json").read_text(encoding=ENC)

w20_hash = file_sha(w20_bytes)
w17_hash = file_sha(w17_bytes)
guard_hash = file_sha(guard_bytes)
gate_id = "BG-W02-TESTONLY-GATE-364"
guard_id = "Guard-W02-TESTONLY"
gate_cast_id = f"{gate_id}/cast"


def actor_base(actor_id, profile_id, class_name, level, dc, pb, rp, max_rp, position, hp, max_hp, body_box, conditions=None):
    return {
        "id": actor_id,
        "profileId": profile_id,
        "class": class_name,
        "classLevel": level,
        "spellDC": dc,
        "PB": pb,
        "HP": hp,
        "maxHP": max_hp,
        "RP": rp,
        "maxRP": max_rp,
        "Dissonance": 0,
        "Refrain": 0,
        "preparedFamiliesUsed": [],
        "magicThisTurn": False,
        "stance": None,
        "stanceHistory": [],
        "lastSpell": None,
        "spellHistory": [],
        "resourceHistory": [],
        "concentration": None,
        "conditions": list(conditions or []),
        "death": {"status": "alive", "successes": 0, "failures": 0, "saveInputs": []},
        "plane": "fixture:origin",
        "position": position,
        "size": "Medium",
        "bodyBox": body_box,
        "bodyPositionConvention": "position is horizontal center and feet/base elevation",
        "orientation": "standing",
        "heldItems": [],
        "carriedItemIds": [],
        "hands": 2,
        "freeHands": ["left", "right"],
        "action": 0,
        "bonusAction": 0,
        "reaction": 1,
        "movement": 0,
        "movementSpeedFeet": 30,
        "movementHistory": [],
        "regularSchedule": None,
        "recharge": {},
        "visible": True,
        "lineOfEffect": True,
    }


w20 = actor_base("W20", w20_data["id"], "Wizard", 20, 19, w20_data["PB"], 80, 80, [-50, 0, 0], 122, 122, [5, 5, 6])
w20.update({
    "profilePath": w20_path,
    "profilePointer": "/Wizard20",
    "profileSHA256": w20_hash,
    "profileWorkingTreeSHA256": w20_binding["workingTreeSha256"],
    "campaignExistenceVerified": False,
    "preparedSpells": list(w20_data["prepared"]),
    "knownSpells": list(w20_data["spellbook"]),
    "focusId": "focus-W20",
    "focusAccessible": True,
    "heldItems": ["focus-W20"],
    "freeHands": ["right"],
    "voice": True,
    "counterspellAutomaticId": w20_data["automaticCards"][1]["id"],
    "counterspellCard": w20_data["automaticCards"][1],
    "counterspellReady": True,
    "counterspellRechargeRounds": 2,
    "recharge": {"wizard.base.counterspell": {"ready": True, "roundsUntilReady": 0, "rechargeRounds": 2, "lastUsed": None}},
    "counterspellComponentsAvailable": {"V": True, "S": True, "F": True, "somaticHand": "right", "focusId": "focus-W20"},
    "regularSchedule": {"firstStart": 0.0, "period": 6.0, "endOffset": 0.9, "nextStart": 0.0, "nextEnd": 0.9, "starts": [], "ends": [], "budgetHistory": []},
})
w17 = actor_base("W17", w17_data["id"], "Wizard", 17, 19, w17_data["PB"], 64, 64, [-26, 0, 0], 104, 104, [5, 5, 6])
w17.update({
    "profilePath": w17_path,
    "profilePointer": "/profiles/0",
    "profileSHA256": w17_hash,
    "profileWorkingTreeSHA256": w17_binding["workingTreeSha256"],
    "campaignExistenceVerified": False,
    "cantrips": list(w17_data["cantrips"]),
    "focusId": "focus-W17",
    "focusAccessible": True,
    "heldItems": ["focus-W17"],
    "freeHands": ["right"],
    "voice": True,
    "counterspellAutomaticId": w17_data["automaticCards"][1]["id"],
    "counterspellCard": w17_data["automaticCards"][1],
    "counterspellReady": True,
    "counterspellRechargeRounds": 2,
    "recharge": {"wizard.base.counterspell": {"ready": True, "roundsUntilReady": 0, "rechargeRounds": 2, "lastUsed": None}},
    "counterspellComponentsAvailable": {"V": True, "S": True, "F": True, "somaticHand": "right", "focusId": "focus-W17"},
    "regularSchedule": {"firstStart": 1.0, "period": 6.0, "endOffset": 1.9, "nextStart": 1.0, "nextEnd": 1.9, "starts": [], "ends": [], "budgetHistory": []},
})
guard = {
    "id": guard_id,
    "profileId": "Guard",
    "profilePath": guard_path,
    "profilePointer": "/326",
    "profileSHA256": guard_hash,
    "profileWorkingTreeSHA256": guard_binding["workingTreeSha256"],
    "name": "Guard",
    "creatureType": "Humanoid",
    "size": "Medium",
    "speedFeet": 40,
    "armorClass": 15,
    "HP": 112,
    "maxHP": 112,
    "conditions": [],
    "movementPreventingConditions": [],
    "lifeClassification": "ALIVE_LIVING_TEST_ONLY_FIXTURE",
    "fixturePremise": "A fresh hypothetical fully living Guard; no prior campaign state is claimed.",
    "death": {"status": "alive", "successes": 0, "failures": 0, "saveInputs": []},
    "plane": "fixture:origin",
    "position": [-7.5, 0, 0],
    "bodyBoxDimensionsFeet": [5, 5, 6],
    "bodyPositionConvention": "position is horizontal center and feet/base elevation",
    "bodyBoxWorld": {"x": [-10, -5], "y": [-2.5, 2.5], "z": [0, 6]},
    "orientation": "standing",
    "action": 0,
    "bonusAction": 0,
    "reaction": 1,
    "movement": 0,
    "movementSpeedFeet": 40,
    "movementHistory": [],
    "stance": None,
    "stanceHistory": [],
    "mobileFirstFiveFeetAllowance": None,
    "regularSchedule": {"firstStart": 2.0, "period": 6.0, "endOffset": 2.9, "nextStart": 2.0, "nextEnd": 2.9, "starts": [], "ends": [], "budgetHistory": []},
}

initial = {
    "time": -0.1,
    "mode": "initiative",
    "fixture": {
        "id": "W02-TESTONLY-364",
        "campaignFact": False,
        "authorizationId": "OWNER-TESTONLY-BANISHMENT-GATE-W02-364",
        "fixtureOnlyCoordinatesAndTerrain": True,
        "otherBodies": [],
        "terrainBlockers": [],
        "difficultTerrain": False,
    },
    "actors": {"W20": w20, "W17": w17, guard_id: guard},
    "items": {
        "focus-W20": {"id": "focus-W20", "ownerId": "W20", "kind": "ordinaryWizardFocus", "testOnly": True, "heldBy": "W20", "hand": "left", "consumed": False},
        "focus-W17": {"id": "focus-W17", "ownerId": "W17", "kind": "ordinaryWizardFocus", "testOnly": True, "heldBy": "W17", "hand": "left", "consumed": False},
    },
    "effects": {},
    "spaces": {"fixture:origin": {"kind": "TEST_ONLY ordinary origin plane", "existsOnlyForTest": True, "blockers": [], "opaqueCover": [], "hazards": []}},
    "pendingCast": None,
    "crossingReceipts": {},
    "admissions": [],
    "movementReceipts": [],
    "hardDenialClaims": [],
    "processedEventIds": [],
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
    record = {
        "id": event_id,
        "time": time,
        "kind": kind,
        "narrative": narrative,
        "source": source,
        "authoredInputs": inputs,
        "before": before,
        "after": after,
        "beforeSHA256": sha(before),
        "afterSHA256": sha(after),
        "forward": scoped_patch(before, after),
        "inverse": scoped_patch(after, before),
    }
    assert apply_patch(state, record["forward"]) == after
    state = after
    events.append(record)


def w20_start(s):
    a = s["actors"]["W20"]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(0.0)
    a["regularSchedule"]["nextStart"] = 6.0
    a["regularSchedule"]["budgetHistory"].append({"time": 0.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})
    stance = {"id": "Mobile", "selectedAt": 0.0, "expiresAtNextRegularStart": 6.0, "noOpportunityAttackForFirstFiveFeetOfActualVoluntaryMovement": True, "grantsFreeMovement": False, "opportunityAttackDamageDieReduction": 1, "testOnlySelection": True}
    allowance = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "appliesToActualVoluntaryMovement": True, "grantsFreeMovement": False, "expiresAtNextRegularStart": 6.0}
    a["stance"] = stance
    a["stanceHistory"].append(stance)
    a["mobileFirstFiveFeetAllowance"] = allowance


event("BG-W02-TESTONLY-GATE-364:0", 0.0, "REGULAR_START", "Wizard20 receives one ordinary regular-turn budget and selects Mobile stance before the first relevant use; it grants no free movement.", "COMBAT_ACTION_PLAYTEST.md regular turn schedule and Mobile stance", {"marker": 0.0, "refreshCount": 1, "stanceSelection": "Mobile", "stanceExpiresAt": 6.0, "grantsFreeMovement": False}, w20_start)


def gate_commit(s):
    caster = s["actors"]["W20"]
    caster["action"] = 0
    caster["RP"] = 54
    caster["lastSpell"] = "banishment-gate"
    caster["Dissonance"] = 0
    caster["Refrain"] = 0
    caster["preparedFamiliesUsed"].append("banishment-gate")
    caster["magicThisTurn"] = True
    caster["spellHistory"].append({"castId": gate_cast_id, "spellId": "banishment-gate", "class": "Wizard", "rank": 9, "time": 0.1, "costRP": 26, "components": ["V", "S", "F"], "focusId": "focus-W20", "concentration": True, "target": None, "school": "Abjuration", "firstPreparedFamily": True, "baseDissonance": 0, "Dissonance": 0, "Refrain": 0, "DissonanceAfterCast": 0, "RefrainAfterCast": 0, "preparedFamiliesUsedAfterCast": ["banishment-gate"]})
    caster["resourceHistory"].append({"event": gate_cast_id, "RP": -26, "poolAfter": 54, "discount": False})
    caster["concentration"] = gate_cast_id
    s["pendingCast"] = {
        "castId": gate_cast_id,
        "casterId": "W20",
        "spellId": "banishment-gate",
        "committedAt": 0.1,
        "resolvesAt": 0.2,
        "actionPaid": True,
        "rpPaid": 26,
        "componentsProvided": ["V", "S", "F"],
        "focusId": "focus-W20",
        "counterspellWindow": {
            "opensAfterCommitBeforeEffect": True,
            "eligibleReactors": [{
                "actorId": "W17",
                "automaticCardId": "wizard.base.counterspell",
                "distanceFeet": 24,
                "rangeFeet": counterspell["rangeFeet"],
                "perceivesCast": True,
                "lineOfEffect": True,
                "reactionAvailable": True,
                "rechargeReady": True,
                "currentRP": 64,
                "costRP": 3,
                "componentsAvailable": ["V", "S", "F"],
                "focusId": "focus-W17",
                "somaticHand": "right",
                "decision": "declines",
                "decisionPremise": "TEST_ONLY cooperative fixture protocol; cost-free decline; no campaign fact",
                "attempted": False,
                "reactionSpent": False,
                "RPSpent": 0,
                "cooldownChanged": False,
            }],
            "ineligible": [
                {"actorId": "W20", "reason": "Casting creature cannot counter its own pending cast"},
                {"actorId": guard_id, "reason": "No Counterspell source is bound for the Guard"},
            ],
            "result": "eligible W17 declines; Gate resolves with no counter attempt",
        },
    }


gate_point = [0, 0, 7.5]
gate_caster_base = [-50, 0, 0]
gate_distance = sum((target - origin) ** 2 for target, origin in zip(gate_point, gate_caster_base)) ** 0.5
event("BG-W02-TESTONLY-GATE-364:1", 0.1, "CAST_COMMIT", "W20 commits the source-bound Wizard Gate casting; Mobile was selected before the cast; first prepared-family Abjuration casting settles Dissonance/Refrain and turn casting state; one Action and 26 RP are paid, V/S/F are supplied, and the eligible Counterspell window resolves before effect.", "W07 Repack01 exact Gate/Wizard source bindings; PG9-Q01/Q14/Q15; Counterspell operational source; WIZARD_CLASS_ENGINE.md; COMBAT_ACTION_PLAYTEST.md", {
    "gatePoint": gate_point,
    "casterBasePositionFeet": gate_caster_base,
    "distanceModel": "3D Euclidean from Wizard20 feet/base position to point",
    "distanceFeet": gate_distance,
    "rangeFeet": 120,
    "rangeSource": "Return327 procedure source index: Banishment Gate original range 120 feet; PG9-Q14 fixed portal within120ft",
    "selectedCreatureType": "Humanoid",
    "components": ["V", "S", "F"],
    "actionCost": 1,
    "rpCost": 26,
    "school": "Abjuration",
    "firstPreparedFamily": True,
    "baseDissonance": 0,
    "DissonanceAfterCast": 0,
    "RefrainAfterCast": 0,
    "preparedFamiliesUsedAfterCast": ["banishment-gate"],
    "magicThisTurnAfterCast": True,
}, gate_commit)


def gate_resolve(s):
    s["pendingCast"] = None
    s["effects"][gate_id] = {
        "id": gate_id,
        "spellId": "banishment-gate",
        "creatorId": "W20",
        "creatorConcentration": gate_cast_id,
        "status": "active",
        "createdAt": 0.2,
        "endsAt": 600.2,
        "selectedCreatureType": "Humanoid",
        "originPlane": "fixture:origin",
        "opening": {"plane": "x=0", "y": [-5, 5], "z": [0, 15]},
        "concentration": True,
        "cells": [],
        "admissions": [],
        "closeCount": 0,
    }


event("BG-W02-TESTONLY-GATE-364:2", 0.2, "CAST_RESOLVE", "Gate opens with its fixed 10-by-15-foot vertical aperture. No body crosses or is admitted at creation.", "PG9-Q14; W07 sealed Gate procedure source", {"opening": {"plane": "x=0", "y": [-5, 5], "z": [0, 15]}, "selectedCreatureType": "Humanoid", "admission": False, "cell": False, "claim": False}, gate_resolve)


def w20_end(s):
    a = s["actors"]["W20"]
    a["regularSchedule"]["ends"].append(0.9)
    a["regularSchedule"]["nextEnd"] = 6.9
    a["action"] = a["bonusAction"] = a["movement"] = 0


event("BG-W02-TESTONLY-GATE-364:3", 0.9, "TURN_END", "W20's scheduled turn ends; Gate concentration continues.", "COMBAT_ACTION_PLAYTEST.md regular-turn schedule", {"turnEnd": 0.9, "nextEnd": 6.9}, w20_end)


def w17_start(s):
    a = s["actors"]["W17"]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(1.0)
    a["regularSchedule"]["nextStart"] = 7.0
    a["regularSchedule"]["budgetHistory"].append({"time": 1.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})
    stance = {"id": "Mobile", "selectedAt": 1.0, "expiresAtNextRegularStart": 7.0, "noOpportunityAttackForFirstFiveFeetOfActualVoluntaryMovement": True, "grantsFreeMovement": False, "opportunityAttackDamageDieReduction": 1, "testOnlySelection": True}
    allowance = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "appliesToActualVoluntaryMovement": True, "grantsFreeMovement": False, "expiresAtNextRegularStart": 7.0}
    a["stance"] = stance
    a["stanceHistory"].append(stance)
    a["mobileFirstFiveFeetAllowance"] = allowance


event("BG-W02-TESTONLY-GATE-364:4", 1.0, "REGULAR_START", "W17 receives its regular-turn budgets once and selects Mobile before its turn ends; its cost-free TEST_ONLY Counterspell decline spent no Reaction, RP, or recharge.", "COMBAT_ACTION_PLAYTEST.md Mobile stance; Wizard Counterspell source; W07 sealed ruling", {"marker": 1.0, "refreshCount": 1, "stanceSelection": "Mobile", "stanceExpiresAt": 7.0, "grantsFreeMovement": False}, w17_start)


def w17_end(s):
    a = s["actors"]["W17"]
    a["regularSchedule"]["ends"].append(1.9)
    a["regularSchedule"]["nextEnd"] = 7.9
    a["action"] = a["bonusAction"] = a["movement"] = 0


event("BG-W02-TESTONLY-GATE-364:5", 1.9, "TURN_END", "W17's scheduled turn ends without spending its Reaction or Counterspell recharge.", "COMBAT_ACTION_PLAYTEST.md regular-turn schedule", {"turnEnd": 1.9, "nextEnd": 7.9}, w17_end)


def guard_start(s):
    g = s["actors"][guard_id]
    g["action"], g["bonusAction"], g["reaction"], g["movement"] = 1, 1, 1, 40
    g["regularSchedule"]["starts"].append(2.0)
    g["regularSchedule"]["nextStart"] = 8.0
    g["regularSchedule"]["budgetHistory"].append({"time": 2.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 40})
    stance = {"id": "Mobile", "selectedAt": 2.0, "expiresAtNextRegularStart": 8.0, "noOpportunityAttackForFirstFiveFeetOfActualVoluntaryMovement": True, "grantsFreeMovement": False, "opportunityAttackDamageDieReduction": 1, "testOnlySelection": True}
    g["stance"] = stance
    g["stanceHistory"].append(stance)
    g["mobileFirstFiveFeetAllowance"] = {"totalFeet": 5, "usedFeet": 0, "remainingFeet": 5, "appliesToActualVoluntaryMovement": True, "grantsFreeMovement": False, "expiresAtNextRegularStart": 8.0}


event("BG-W02-TESTONLY-GATE-364:6", 2.0, "REGULAR_START", "The living Guard reaches its own original scheduled regular-start marker, receives its 40-foot movement wallet exactly once, and selects Mobile; the stance adds no movement.", "COMBAT_ACTION_PLAYTEST.md Mobile stance; Guard source profile Speed 40 feet", {"marker": 2.0, "sourceSpeedFeet": 40, "movementWalletBefore": 0, "movementWalletAfterStart": 40, "stanceSelection": "Mobile", "stanceExpiresAt": 8.0, "grantsFreeMovement": False}, guard_start)


def guard_move_to_touch(s):
    g = s["actors"][guard_id]
    g["position"] = [-2.5, 0, 0]
    g["bodyBoxWorld"] = {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]}
    g["movement"] = 35
    g["mobileFirstFiveFeetAllowance"].update({"usedFeet": 5, "remainingFeet": 0, "usedAt": 2.05, "opportunityAttacksPrevented": 0, "noOpportunityAttackWasTriggered": True})
    g["movementHistory"].append({
        "time": 2.05,
        "kind": "lawful voluntary walking",
        "from": [-7.5, 0, 0],
        "to": [-2.5, 0, 0],
        "direction": "+x",
        "feetSpent": 5,
        "walletBefore": 40,
        "walletAfter": 35,
        "pathClear": True,
        "difficultTerrain": False,
        "movementPreventingCondition": False,
        "destinationIsOriginPlane": True,
        "completeBodyCrossing": False,
        "positiveInteriorOverlapBeyondGatePlane": False,
        "leadingFaceOnlyTouchesPlane": True,
        "mobileAllowanceUsedFeet": 5,
        "mobileAllowanceGrantsFreeMovement": False,
        "opportunityAttacksPrevented": 0,
        "admission": False,
        "cell": False,
        "hardDenialClaim": False,
    })
    s["movementReceipts"] = [{
        "actorId": guard_id,
        "sourcePlane": "fixture:origin",
        "destinationPlane": "fixture:origin",
        "fromBodyBox": {"x": [-10, -5], "y": [-2.5, 2.5], "z": [0, 6]},
        "toBodyBox": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]},
        "gatePlane": "x=0",
        "aperture": {"y": [-5, 5], "z": [0, 15]},
        "movementSpent": 5,
        "movementWallet": {"before": 40, "after": 35},
        "interiorBeyondPlane": False,
        "triggeredGate": False,
        "admission": False,
        "cell": False,
        "claim": False,
    }]


event("BG-W02-TESTONLY-GATE-364:7", 2.05, "LAWFUL_MOVEMENT_TO_BOUNDARY_WITHOUT_CROSSING", "During its own scheduled turn, the living Guard spends 5 feet walking toward +x. Mobile's first-five-foot allowance is recorded as used, with no free movement granted and no opportunity attack triggered. Its leading face ends exactly at x=0; occupied interior remains wholly on the origin side, so the Gate does not trigger.", "Guard source profile / speed; BODY_EQUIPMENT_PLAYTEST.md occupied volume; COMBAT_ACTION_PLAYTEST.md movement wallet and Mobile stance; PG9-Q14 crossing predicate", {
    "fromBodyBox": {"x": [-10, -5], "y": [-2.5, 2.5], "z": [0, 6]},
    "toBodyBox": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]},
    "gatePlane": "x=0",
    "apertureY": [-5, 5],
    "apertureZ": [0, 15],
    "movementSpentFeet": 5,
    "mobileAllowanceUsedFeet": 5,
    "mobileAllowanceGrantsFreeMovement": False,
    "opportunityAttacksPrevented": 0,
    "wallet": [40, 35],
    "unobstructedPath": True,
    "difficultTerrain": False,
    "movementPreventingCondition": False,
    "positiveInteriorOverlapBeyondPlane": False,
    "trigger": False,
    "admission": False,
    "cell": False,
    "claim": False,
}, guard_move_to_touch)


def end_concentration(s):
    gate = s["effects"][gate_id]
    gate["status"] = "ended"
    gate["concentrationEndedAt"] = 2.1
    gate["endReason"] = "W20 voluntarily ends concentration after the boundary movement witness"
    gate["closeCount"] = 1
    gate["cells"] = []
    gate["admissions"] = []
    w = s["actors"]["W20"]
    w["concentration"] = None


event("BG-W02-TESTONLY-GATE-364:8", 2.1, "CONCENTRATION_END_NO_CELL", "W20 lawfully ends Gate concentration after the Guard’s boundary-touch movement. No cell exists to close; the Guard remains living and in origin-plane custody at the touch pose.", "W07 sealed approved Gate concentration-ending procedure; PG200-CELL-EXT applies only to an admitted cell", {
    "concentrationEnd": 2.1,
    "scheduledMarkersProcessedThroughEnd": [0.0, 0.9, 1.0, 1.9, 2.0],
    "guardNextScheduledEnd": 2.9,
    "terminalGuardPlane": "fixture:origin",
    "terminalGuardBodyBox": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]},
    "admissions": 0,
    "cells": 0,
    "hardDenialClaims": 0,
}, end_concentration)

case = {
    "id": "W02_BOUNDARY_CASE_364_REPACK03",
    "witnessId": "W02",
    "scopeId": "banishment-gate",
    "sourceCommit": w07_bindings["sourceCommit"],
    "kind": "TEST_ONLY_movement_to_gate_boundary_without_crossing",
    "status": "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED",
    "holdIds": ["PG200-B03", "PG200-B04"],
    "supersedesWitness": None,
    "priorSealedWitness": {
        "witnessId": "W07",
        "archive": W07_ZIP.name,
        "archiveBytes": W07_ZIP.stat().st_size,
        "archiveSha256": W07_ARCHIVE_SHA256,
        "directorRulingId": W07_SEAL_DATA["rulingId"],
        "sourceBindingsSha256": W07_SOURCE_BINDINGS_SHA256,
    },
    "scenarioQualification": "A new owner-authorized hypothetical TEST_ONLY living Guard state; no campaign or real-world facts.",
    "supersedesSubmission": {"caseId": "W02_BOUNDARY_CASE_364_REPACK02", "archive": W02_REPACK02.name, "archiveSha256": W02_REPACK02_SHA256, "directorHoldRulingId": W02_REPACK02_HOLD["rulingId"]},
    "sourceBindings": {
        "Wizard20": {"path": w20_path, "pointer": "/Wizard20", "gitSha256": w20_hash, "profileWorkingTreeSha256": w20_binding["workingTreeSha256"], "acquired": True, "prepared": True},
        "Wizard17": {"path": w17_path, "pointer": "/profiles/0", "gitSha256": w17_hash, "profileWorkingTreeSha256": w17_binding["workingTreeSha256"]},
        "Guard": {"path": guard_path, "pointer": "/326", "gitSha256": guard_hash, "profileWorkingTreeSha256": guard_binding["workingTreeSha256"], "profileId": "Guard"},
        "Gate": {"catalogPath": catalog_path, "spellId": "banishment-gate", "classAccess": "Wizard", "baseRpCost": 26},
        "Counterspell": {"catalogPath": catalog_path, "spellId": "counterspell", "rangeFeet": counterspell["rangeFeet"], "components": counterspell["components"]},
    },
    "fixturePremises": read_json(PACK / "W02_OWNER_TESTONLY_AUTHORIZATION_364.json"),
    "geometry": {
        "gatePlane": "x=0",
        "aperture": {"y": [-5, 5], "z": [0, 15]},
        "selectedCreatureType": "Humanoid",
        "openingGuardBodyBox": {"x": [-10, -5], "y": [-2.5, 2.5], "z": [0, 6]},
        "terminalGuardBodyBox": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 6]},
        "positiveInteriorOverlapBeyondPlane": False,
    },
    "initial": initial,
    "events": events,
    "final": state,
    "initialSHA256": sha(initial),
    "finalSHA256": sha(state),
    "inverseRestorationOrder": [e["id"] for e in reversed(events)],
    "coverage": {
        "W02": "complete movement-to-touch witness submitted",
        "W07": "previously sealed PASS; preserved as a separate witness",
        "W01": "not evidenced by this packet",
        "W03": "open source gap; no fixture type assignment substitutes",
        "W04": "not evidenced by this packet",
        "W05": "not evidenced by this packet",
        "W06": "approved Plane Shift route; witness outstanding",
        "W08": "not evidenced by this packet",
    },
    "assertions": {
        "livingGuardAt112Of112": True,
        "originalScheduledGuardStartAt2Seconds": True,
        "guardMovementWallet40To35": True,
        "completeBodyStopsWithLeadingFaceTouchAtX0": True,
        "positiveInteriorCrossing": False,
        "admissionCount": 0,
        "cellCount": 0,
        "hardDenialClaimCount": 0,
        "originPlaneCustodyRetained": True,
        "gateEndedAfterAllMarkersDueThrough2_1": True,
        "spellAccepted": False,
        "spellApplied": False,
        "applicationAuthorized": False,
    },
}
write_json(PACK / "W02_BOUNDARY_CASE_364_REPACK03.json", case)
write_json(PACK / "W02_SOURCE_BINDINGS_364.json", {
    "id": "PG327-W02-SOURCE-BINDINGS-364",
    "sourceCommit": w07_bindings["sourceCommit"],
    "reusedFrom": "sealed W07 Repack01; see W07_SOURCE_REUSE_364.json",
    "bindings": source_binding_records,
    "hashConvention": "Git-bound source members are exact Git bytes verified against their sourceCommit. Reused members are also bound to the sealed W07 Repack01 archive SHA.",
})

readme = """# Banishment Gate W02 TEST_ONLY boundary witness 364 Repack03

This packet submits only W02: lawful movement reaches the portal boundary without crossing. It supersedes the W02 Repack02 submission, whose two precise residuals are closed here. W02 Repack02 and its HOLD ruling, and W07 Repack01 and its seal, are included byte-for-byte as prior evidence. Gate remains HOLD under PG200-B03/PG200-B04. This packet grants no identity acceptance, application, campaign fact, runtime execution, type-change mechanic or escape mechanic.

W20 legally commits Banishment Gate using its source-bound Wizard acquisition and preparation, Action, 26 RP, V/S/F, held focus, concentration, range and eligible Counterspell window. The opposing Wizard's cost-free TEST_ONLY decline is recorded. A fresh living Guard opens at 112/112 HP, Humanoid, Medium, Speed 40 feet, with no movement-preventing condition. The Gate is fixed to Humanoid at x=0 with opening y=[-5,5], z=[0,15].

W20, W17, and the Guard select Mobile stance before their first relevant use or turn end, with each expiry at that actor's next regular start. Mobile grants no free movement. The Guard's first-five-foot allowance is recorded as used by the actual 5-foot movement; no opportunity attack is triggered or prevented in this fixture. W20 records Dissonance, Refrain, prepared-family use and turn casting state; W17 records untouched casting state after its cost-free decline.

On the Guard's actual scheduled regular turn at 2.0 seconds, its movement wallet refreshes to 40 feet once. It spends 5 feet walking +x from center -7.5 to -2.5. Its measured standing body changes from x=[-10,-5] to x=[-5,0], with y=[-2.5,2.5], z=[0,6]. The leading face touches the Gate plane; no occupied interior passes x=0. The Guard remains on the origin plane. No crossing receipt, admission, cell, or hard-denial claim is created. Gate concentration then ends at 2.1 seconds after all scheduled markers due through that endpoint.

All nine events carry full before/after snapshots and deterministic hashes. Forward and inverse operations are field-scoped JSON Patch with precondition tests. The independent verifier checks every changed field, source binding, geometry, turn calendar, movement cost, zero-admission result, exact reverse restoration, nested W07 archive, manifest and CRCs.
"""
(PACK / "README.md").write_text(readme, encoding=ENC)

verifier_source = BASE / "verify_banishment_gate_w02_boundary_364_repack03.py"
verifier_member = PACK / "verification/verify_banishment_gate_w02_boundary_364_repack03.py"
verifier_member.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(verifier_source, verifier_member)

members = sorted(p for p in PACK.rglob("*") if p.is_file() and p.name not in {"MANIFEST.json", "DELIVERY.json"})
manifest = {
    "id": "PG327-W02-MANIFEST-364-REPACK03",
    "packetId": "DD-RANK9-BANISHMENT-GATE-W02-BOUNDARY-364-REPACK03-TESTONLY",
    "sourceCommit": w07_bindings["sourceCommit"],
    "scope": "W02 movement-to-touch without crossing only; W07 archive is prior sealed evidence",
    "metadataSidecars": "MANIFEST.json and DELIVERY.json are archive members excluded from the payload self-hash list; final archive bytes are bound by external ARCHIVE_DELIVERY_364_REPACK03.json.",
    "members": [{"path": p.relative_to(PACK).as_posix(), "bytes": p.stat().st_size, "sha256": file_sha(p.read_bytes()), "crc32": f"{zlib.crc32(p.read_bytes()) & 0xffffffff:08x}"} for p in members],
}
write_json(PACK / "MANIFEST.json", manifest)
delivery = {
    "id": "PG327-W02-DELIVERY-364-REPACK03",
    "packetId": manifest["packetId"],
    "archive": ARCHIVE.name,
    "scope": ["banishment-gate/W02"],
    "requestedDirectorAction": "Audit W02 movement-to-touch only, including corrections for W02-364-R1 and W02-364-R2; seal W02 if it passes or return exact defects. Keep Gate HOLD and leave all other witness dispositions unchanged.",
    "spellDispositionRequested": "NONE",
    "applicationRequested": False,
    "priorW07": {"decision": "SEALED_PASS_TEST_ONLY_WITNESS", "archiveSha256": W07_ARCHIVE_SHA256, "rulingId": W07_SEAL_DATA["rulingId"]},
    "authority": {"queue": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0, "heldIds": ["banishment-gate"], "blockers": ["PG200-B03", "PG200-B04"]},
    "sourceGap": {"id": "W03", "status": "OPEN; no fixture type assignment substitutes"},
    "members": manifest["members"],
}
write_json(PACK / "DELIVERY.json", delivery)

with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(p for p in PACK.rglob("*") if p.is_file()):
        zf.write(path, path.relative_to(PACK).as_posix())
with zipfile.ZipFile(ARCHIVE) as zf:
    infos = zf.infolist()
    names = [item.filename for item in infos]
    assert len(names) == len(set(names))
    assert zf.testzip() is None
    assert sorted(names) == sorted(p.relative_to(PACK).as_posix() for p in PACK.rglob("*") if p.is_file())
    for member in manifest["members"]:
        data = zf.read(member["path"])
        assert file_sha(data) == member["sha256"]
        assert f"{zlib.crc32(data) & 0xffffffff:08x}" == member["crc32"]

archive_bytes = ARCHIVE.read_bytes()
write_json(OUT / "ARCHIVE_DELIVERY_364_REPACK03.json", {
    "id": "PG327-W02-ARCHIVE-DELIVERY-364-REPACK03",
    "archive": ARCHIVE.name,
    "bytes": len(archive_bytes),
    "sha256": file_sha(archive_bytes),
    "crc32": f"{zlib.crc32(archive_bytes) & 0xffffffff:08x}",
    "memberCount": len(infos),
    "uniqueMembers": True,
    "memberHashesAndCrcsVerified": True,
    "zipTest": "PASS",
    "caseEvents": len(events),
    "directorDisposition": "W02 evidence only; Gate remains HOLD; no acceptance or application",
})
print(json.dumps({"out": str(OUT), "archive": str(ARCHIVE), "bytes": len(archive_bytes), "sha256": file_sha(archive_bytes), "members": len(infos), "events": len(events), "initialSHA256": sha(initial), "finalSHA256": sha(state)}, ensure_ascii=False, indent=2))
