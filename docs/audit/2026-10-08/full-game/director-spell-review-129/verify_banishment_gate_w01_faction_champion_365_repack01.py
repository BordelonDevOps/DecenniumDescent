from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness365_w01_faction_champion_verified02"
PACK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_BanishmentGate_W01_FactionChampion_365_Repack02_TESTONLY.zip"
CASE_PATH = PACK / "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02.json"
ENC = "utf-8"


def canon(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(v):
    return hashlib.sha256(canon(v)).hexdigest()


def fsha(b):
    return hashlib.sha256(b).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding=ENC))


def parent(obj, path):
    parts = [p.replace("~1", "/").replace("~0", "~") for p in path[1:].split("/")]
    cur = obj
    for p in parts[:-1]:
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    return cur, parts[-1]


def get(obj, path):
    p = obj
    for k in path[1:].split("/"):
        k = k.replace("~1", "/").replace("~0", "~")
        p = p[int(k)] if isinstance(p, list) else p[k]
    return p


def apply(obj, ops):
    cur = copy.deepcopy(obj)
    for op in ops:
        p, k = parent(cur, op["path"])
        if isinstance(p, list):
            i = int(k)
            if op["op"] == "replace": p[i] = copy.deepcopy(op["value"])
            elif op["op"] == "remove": p.pop(i)
            else: p.insert(i, copy.deepcopy(op["value"]))
        elif op["op"] == "add":
            assert k not in p
            p[k] = copy.deepcopy(op["value"])
        elif op["op"] == "remove": del p[k]
        else: p[k] = copy.deepcopy(op["value"])
    return cur


case = load(CASE_PATH)
queue = load(PACK / "authority/CURRENT_SPELL_QUEUE_361.json")
plan = load(PACK / "authority/PG327_W01_W08_WITNESS_PLAN_361.json")
bindings = load(PACK / "W01_SOURCE_BINDINGS_365.json")
model = load(PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json")
canonical_model = PACK / "authority/AC5_ACCEPTANCE/ACCEPTED_SPELLS_MODEL_SNAPSHOT.json"
acceptance = load(PACK / "authority/AC5_ACCEPTANCE/ACCEPTANCE.json")
receipt = load(PACK / "authority/AC5_ACCEPTANCE/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json")
accepted_archive = PACK / "authority/AC5_ACCEPTANCE/DD_AC5_Local_Final_05.zip"
source_a = PACK / "prior/CASE_A_ORIGINAL.json"
unknown = PACK / "prior/UNKNOWN_TYPE_CONTROL_ORIGINAL.json"
gate_bytes = (PACK / "sources/RETURN327_banishment-gate.json").read_bytes()
w06_bindings = load(PACK / "sources/W06_SOURCE_BINDINGS_365.json")

assert case["id"] == "W01_FACTION_CHAMPION_GATE_CASE_365_REPACK02"
assert case["witnessId"] == "W01" and case["status"].endswith("NOT_ACCEPTED; NOT_APPLIED")
assert case["identityDecision"] == "HOLD"
assert queue["currentAuthority"]["reviewedApplied"] == 828
assert queue["currentAuthority"]["pending"] == 20 and queue["currentAuthority"]["acceptedUnapplied"] == 0
assert plan["status"] == "DIRECTOR_REQUIREMENTS_TRANSCRIBED; WITNESSES_NOT_YET_ESTABLISHED"
w01 = next(w for w in plan["requirements"]["witnesses"] if w["id"] == "W01")
assert "accepted AC5 Faction Champion" in w01["requiredEvidence"] and "unknown-type" in w01["requiredEvidence"]
assert case["fixturePremises"]["campaignEventsAsserted"] is False
assert case["fixturePremises"]["identityAcceptanceOrApplication"] is False
assert case["fixturePremises"]["roles"]["B-pet"]["relation"] == "ALLY_TEST_ONLY"
assert case["fixturePremises"]["roles"]["D-pet"]["relation"] == "ENEMY_TEST_ONLY"
assert all(x["sourceAdmissionPreserved"] for x in case["fixturePremises"]["roles"].values())

# The original authored case and its final fork are byte/state pinned.
original_a = json.loads(source_a.read_text(encoding=ENC))
assert original_a["status"] == "HELD_TYPE_CONTROL"
assert fsha(source_a.read_bytes()) == case["sourceFork"]["sourceFileSha256"]
assert original_a["final"] == case["initial"]
assert case["initialSHA256"] == sha(case["initial"]) == case["sourceFork"]["forkStateSHA256"]
assert case["sourceFork"]["sourceStateIsCopiedWithoutAlteration"] is True
gate_id = case["sourceBindings"]["gateId"]
assert case["initial"]["effects"][gate_id]["selectedType"] == "Elemental"
assert case["initial"]["effects"][gate_id]["active"] is True
assert case["initial"]["actors"]["B-pet"]["plane"].endswith("/cell/B-pet")
assert case["initial"]["actors"]["D-pet"]["plane"].endswith("/cell/D-pet")
initial_cells = {k: v for k, v in case["initial"]["effects"].items() if "/cell/" in k}
assert set(initial_cells) == {f"{gate_id}/cell/B-pet", f"{gate_id}/cell/D-pet"}

# Accepted AC5 artifact and source route are exact and bound to the current canonical copy.
assert acceptance["verdict"] == "ACCEPT_FOR_AUTHORED_CAMPAIGN_PLAYTEST_INTEGRATION"
assert "faction-champion" in receipt["acceptedSpellIds"]
assert receipt["status"] == "exact-authored-acceptance-applied"
assert fsha((PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").read_bytes()) == "d782569ed8ef558f4edf54634e0d8c19926e24e2437528f1769b5ef3ce594898"
assert fsha(canonical_model.read_bytes()) == fsha((PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").read_bytes())
assert fsha(accepted_archive.read_bytes()) == "43b0fe4359021c4d8f714e3986be3d1579889cf590cfac73333dbe99b31c50cd"
with zipfile.ZipFile(accepted_archive) as ac5z:
    assert ac5z.read("candidate/SPELLS_MODEL.json") == (PACK / "authority/AC5_ACCEPTANCE/SPELLS_MODEL.json").read_bytes()
spell = next(s for s in model["spells"] if s["id"] == "faction-champion")
assert spell["completeSourceAndAccess"]["classAccess"]["Wizard"] == {
    "rank": 5, "minimumClassLevel": 9, "school": "Conjuration", "baseRpCost": 10
}
core = spell["completeSourceAndAccess"]["source"]["coreEntries"][0]["original"]
assert (core["casting_time"], core["range"], core["components"], core["duration"], core["rp_cost"]) == (
    "1 action", "60 feet", "V, S, F", "Concentration, up to 1 minute", 10)
profile = model["profiles"]["AC5-PROFILE-FACTION-CHAMPION-01"]
assert (profile["creatureType"], profile["size"], profile["hpMax"], profile["ac"], profile["weightLb"]) == ("Humanoid", "Medium", 70, 18, 180)
eligibility = model["sharedRules"]["AC5-CHAMPION-ALLY-01"]["rule"]
for term in ("alliedStatus=true", "standing > 0", "invocation permission", "no explicit aid prohibition"):
    assert term in eligibility

# Gate procedure is byte-exact to its accepted W06 source revision.
gb = w06_bindings["fixtureSpecificBindings"]["Gate"]
assert bindings["gate"]["sha256"] == fsha(gate_bytes) == gb["sha256"]
assert bindings["gate"]["repositoryPath"] == gb["sourcePath"]
git_bytes = subprocess.check_output(["git", "show", f'{gb["repositorySourceCommit"]}:{gb["sourcePath"]}'], cwd=ROOT)
assert git_bytes == gate_bytes
gate = json.loads(gate_bytes)
for clause in ("PG9-Q14", "PG9-Q16", "PG9-Q29"):
    assert clause in gate["procedure"]

# Replay every complete state transition in both directions.
state = copy.deepcopy(case["initial"])
assert len(case["events"]) == 7
for ev in case["events"]:
    assert ev["before"] == state and ev["beforeSHA256"] == sha(state)
    assert apply(state, ev["forward"]) == ev["after"]
    assert ev["afterSHA256"] == sha(ev["after"])
    assert apply(ev["after"], ev["inverse"]) == state
    state = copy.deepcopy(ev["after"])
assert state == case["final"] and case["finalSHA256"] == sha(state)
for ev in reversed(case["events"]):
    state = apply(state, ev["inverse"])
assert state == case["initial"] and case["inverseRestorationOrder"] == [e["id"] for e in reversed(case["events"])]
assert [e["time"] for e in case["events"]] == sorted(e["time"] for e in case["events"])

final = case["final"]
wizard = final["actors"]["E-W01-TESTONLY"]
champ = final["actors"]["Champion-W01-TESTONLY"]
assert wizard["class"] == "Wizard" and wizard["level"] == 9
assert wizard["RP"] == 40 and wizard["spellHistory"][-1]["costRP"] == 10
assert wizard["spellHistory"][-1]["components"] == ["V", "S", "F"]
assert wizard["spellHistory"][-1]["standingAtCommit"] == wizard["spellHistory"][-1]["standingAtResolution"] == 1
assert champ["type"] == champ["creatureType"] == "Humanoid" and champ["exists"] is True
assert (champ["HP"], champ["maxHP"], champ["AC"], champ["size"], champ["bodyMassLb"]) == (70, 70, 18, "Medium", 180)
assert champ["deadline"] == 71.2
assert champ["command"]["cost"] == "owner Bonus Action"
assert champ["movementHistory"][0]["spentFt"] == 20
assert champ["movementHistory"][0]["from"] == [10, 15, 0] and champ["position"] == [10, -5, 0]
assert champ["movement"] == 10
assert final["effects"][gate_id] == case["initial"]["effects"][gate_id]
assert {k: v for k, v in final["effects"].items() if "/cell/" in k} == initial_cells
assert final["hardDenialClaims"] == case["initial"]["hardDenialClaims"]
assert not any(k.endswith("/cell/Champion-W01-TESTONLY") for k in final["effects"])
cross = next(e for e in case["events"] if e["kind"] == "COMMANDED_MOVEMENT_THROUGH_APERTURE")
assert cross["evidence"]["bodyFits10x15"] is True
assert cross["outcome"].find("no Gate cell, save, exile") >= 0
obs = final["observations"][-1]
assert obs["result"] == "NONMATCHING_HUMANOID_PASSES; NO_GATE_EXILE_RESOLUTION"
assert obs["saveRolled"] is False and obs["newHardDenialClaim"] is False and obs["newCell"] is False

# Repack01 was an unsubmitted local build with an incorrect source snapshot and is preserved as superseded history.
prior_archive = PACK / "prior/W01_REPACK01_UNSUBMITTED.zip"
prior_delivery = load(PACK / "prior/W01_REPACK01_UNSUBMITTED_DELIVERY.json")
prior_supersession = load(PACK / "prior/W01_REPACK01_SUPERSESSION.json")
assert fsha(prior_archive.read_bytes()) == prior_delivery["sha256"] == prior_supersession["supersededArchiveSha256"]
assert prior_supersession["externalSubmission"] is False and prior_supersession["directorReviewRequested"] is False

# Unknown type is separately preserved and makes no positive resolution claim.
u = json.loads(unknown.read_text(encoding=ENC))
assert u["status"] == "HELD_NATIVE_TYPE_CONTROL"
assert not any(e.get("kind") == "AUTO_EXILE" for e in u["events"])
assert not u["final"].get("hardDenialClaims")
assert "no unproved removal claimed" in json.dumps(u["final"], ensure_ascii=False)
assert fsha(unknown.read_bytes()) == bindings["unknownTypeControl"]["sha256"]

# All package members, archive bytes and independent authority counts agree.
manifest = load(PACK / "ARCHIVE_MANIFEST.json")
for entry in manifest["members"]:
    data = (PACK / entry["path"]).read_bytes()
    assert len(data) == entry["bytes"] and fsha(data) == entry["sha256"]
with zipfile.ZipFile(ARCHIVE) as zf:
    assert zf.testzip() is None
    assert set(zf.namelist()) == {p.relative_to(PACK).as_posix() for p in PACK.rglob("*") if p.is_file()}
    for name in zf.namelist():
        assert zf.read(name) == (PACK / name).read_bytes()

audit = {
    "id": "PG327-W01-365-REPACK02-INDEPENDENT-AUDIT", "status": "PASS_TEST_ONLY_WITNESS_PACKET",
    "archive": ARCHIVE.name, "archiveSha256": fsha(ARCHIVE.read_bytes()), "archiveBytes": ARCHIVE.stat().st_size,
    "caseId": case["id"], "eventCount": len(case["events"]), "memberCount": len(manifest["members"]),
    "checks": {
        "exactAC5AcceptedSourceAndAccess": True, "fullFiniteHumanoidProfile": True,
        "sourceAExactForkAndExistingElementalAdmissions": True, "paidActionComponentsRPAndConcentration": True,
        "lawfulPaidCommandAnd20FootCrossing": True, "apertureGeometry": True,
        "noHumanoidExileSaveNewCellOrHardDenial": True, "unknownTypeSeparateNondiagnosticControl": True,
        "forwardInverseReplay": True, "archiveIntegrityAndManifest": True,
    },
    "campaignEventsAsserted": False, "identityAcceptanceOrApplication": False,
    "identityDecision": "HOLD", "queueCounts": {"reviewedApplied": 828, "pending": 20, "acceptedUnapplied": 0},
}
audit_path = OUT / "INDEPENDENT_AUDIT_365_W01_REPACK02.json"
audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding=ENC)
print(json.dumps(audit, indent=2))
