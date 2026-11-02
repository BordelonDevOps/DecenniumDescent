import copy
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = REVIEW.parents[4]
WITNESS = ROOT / "W13_WITNESS_469_TESTONLY.json"
TRACE = ROOT / "W13_LIFECYCLE_TRACE_469.json"
VALIDATION = ROOT / "BUILD_VALIDATION_469.json"
MANIFEST = ROOT / "MANIFEST_469.json"
DELIVERY = ROOT / "DELIVERY_469.json"
ARCHIVE = ROOT / "DD_Fortress_W13_Reversible_Witness_469_TESTONLY.zip"
PROPOSAL = REVIEW / "fortress_w13_nested_space_owner_proposal_448" / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json"
ADOPTION = REVIEW / "fortress_w13_nested_space_owner_proposal_448" / "OWNER_PG328_W13_ADOPTION_448_TESTONLY.json"
PARENT = REVIEW / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
EXPECTED_PROPOSAL_SHA = "9254bee8a314de50cbe0c6aa71bef45e22fbea988d8668c089151b8e7f80051a"
EXPECTED_ADOPTION_SHA = "a118fa592228d6747c546364007f5b125153f2d4845374ab01525141fe20fd05"
EXPECTED_PARENT_SHA = "2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb"
EXPECTED_S030_SHA = "6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_file(path):
    return sha_bytes(Path(path).read_bytes())


def sha_object(value):
    return sha_bytes(canonical(value))


def apply_ops(state, operations):
    result = copy.deepcopy(state)
    for operation in operations:
        path = [part.replace("~1", "/").replace("~0", "~") for part in operation["path"].lstrip("/").split("/")]
        parent = result
        for part in path[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = path[-1]
        if isinstance(parent, list):
            index = int(key)
            if operation["op"] == "add":
                parent.insert(index, copy.deepcopy(operation["value"]))
            elif operation["op"] == "remove":
                parent.pop(index)
            else:
                parent[index] = copy.deepcopy(operation["value"])
        elif operation["op"] == "add":
            parent[key] = copy.deepcopy(operation["value"])
        elif operation["op"] == "remove":
            del parent[key]
        else:
            parent[key] = copy.deepcopy(operation["value"])
    return result


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    witness = load(WITNESS)
    trace = load(TRACE)
    validation = load(VALIDATION)
    manifest = load(MANIFEST)
    delivery = load(DELIVERY)
    proposal = load(PROPOSAL)
    adoption = load(ADOPTION)
    parent_doc = load(PARENT)
    parent = parent_doc["stateSnapshots"]["S030"]
    events = witness["eventTrace"]["events"]
    checks = {}
    checks["exact adopted proposal, adoption, and W01 parent hashes"] = sha_file(PROPOSAL) == EXPECTED_PROPOSAL_SHA and sha_file(ADOPTION) == EXPECTED_ADOPTION_SHA and sha_file(PARENT) == EXPECTED_PARENT_SHA and sha_object(parent) == EXPECTED_S030_SHA
    checks["adoption and witness branch scopes match"] = adoption["scope"]["branchId"] == witness["branchId"] == "PG328-W13-R1" and witness["adoption"]["exactProposalSha256"] == EXPECTED_PROPOSAL_SHA and witness["adoption"]["ownerAdopted"] is True
    checks["owner-adopted scenario copies Proposal448 exactly"] = witness["adoptedScenario"] == proposal["ownerProposedInputs"]
    checks["17 source hash and Git blob bindings pass"] = len(witness["sourceBindings"]) == 17 and all(x["matches"] and x["actualSha256"] == x["sha256"] and x["actualGitBlobSha1"] == x["gitBlobSha1"] for x in witness["sourceBindings"])
    checks["initial replay is exact unmodified S030"] = witness["stateTransitionReplay"]["initialState"] == parent and witness["stateTransitionReplay"]["initialStateSha256"] == EXPECTED_S030_SHA and witness["parent"]["parentMutated"] is False
    checks["event count and 12 START/11 END markers"] = len(events) == 47 and sum(x["kind"] in {"START", "A_START_SIGHT_TICK", "B_START_CHILD_DISPEL", "A_START_PARENT_DISPEL"} for x in events) == 12 and sum(x["kind"] in {"END", "B_END_EFF_EXPIRY"} for x in events) == 11
    state = copy.deepcopy(parent)
    chain_ok = True
    for event in events:
        transition = event["stateTransition"]
        if sha_object(state) != transition["beforeStateSha256"]:
            chain_ok = False
            break
        state = apply_ops(state, transition["forwardOperations"])
        if sha_object(state) != transition["afterStateSha256"]:
            chain_ok = False
            break
    checks["all forward event patches chain to declared terminal state"] = chain_ok and state == witness["stateTransitionReplay"]["terminalState"] and sha_object(state) == witness["stateTransitionReplay"]["terminalStateSha256"]
    reverse_state = copy.deepcopy(state)
    inverse_ok = True
    for event in reversed(events):
        transition = event["stateTransition"]
        if sha_object(reverse_state) != transition["afterStateSha256"]:
            inverse_ok = False
            break
        reverse_state = apply_ops(reverse_state, transition["inverseOperations"])
        if sha_object(reverse_state) != transition["beforeStateSha256"]:
            inverse_ok = False
            break
    checks["all inverse event patches restore exact S030"] = inverse_ok and reverse_state == parent and sha_object(reverse_state) == EXPECTED_S030_SHA
    checks["nested room ends before P5-CLOSE and Fortress closure"] = next(x for x in events if x["kind"] == "CHILD_DISPEL_RESOLVE")["timeSeconds"] < next(x for x in events if x["kind"] == "P5_CLOSE_BODY")["timeSeconds"] < next(x for x in events if x["kind"] == "Q27_ROOT_END")["timeSeconds"] and next(x for x in events if x["kind"] == "P5_CLOSE_BODY")["details"]["parentStillActive"] is True
    checks["cargo custody resolves held, then child-loose, then parent-loose"] = [(x["kind"], x["timeSeconds"]) for x in events if x["kind"] in {"SECURE_CARGO", "CHILD_ENTRY", "CARGO_SETDOWN", "P5_CLOSE_LOOSE", "Q27_LOOSE"}] == [("SECURE_CARGO", 19.01), ("CHILD_ENTRY", 19.05), ("CARGO_SETDOWN", 19.06), ("P5_CLOSE_LOOSE", 25.31), ("Q27_LOOSE", 30.31), ("Q27_LOOSE", 30.31)]
    checks["four spell costs and prepared-family records are retained"] = [(x["details"]["spellId"], x["details"]["costRP"]) for x in events if x["kind"].endswith("_COMMIT")] == [("demiplane", 21), ("wizard.arch.arcane-sight", 2), ("wizard.arch.dispel-magic", 3), ("wizard.arch.dispel-magic", 3)] and state["actors"]["A"]["preparedFamiliesUsed"] == ["conjure-demiplane-fortress", "wizard.base.minor-conjuration", "wizard.arch.arcane-sight", "wizard.arch.dispel-magic"] and state["actors"]["B"]["preparedFamiliesUsed"] == ["demiplane", "wizard.arch.dispel-magic"] and state["actors"]["A"]["RP"] == 48 and state["actors"]["B"]["RP"] == 56
    checks["child Dispel targets the exact adopted room identity"] = next(x for x in events if x["kind"] == "CHILD_DISPEL_COMMIT")["details"]["target"] == proposal["ownerProposedInputs"]["childDispel"]["targetEffect"] == "PG328-W13-R1:DEMIPLANE-B/cast1/space"
    checks["Class0 remains branch-only and records the later owner adoption"] = witness["adoptedBranchPremises"][0]["statusInThisWitness"] == "OWNER_ADOPTED_TEST_ONLY_PREMISE" and witness["adoptedBranchPremises"][0]["scope"] == "PG328-W13-R1 only" and witness["adoptedBranchPremises"][0]["canonicalOrCampaignEffect"] is False and "NOT OWNER-ADOPTED" in witness["adoptedScenario"]["resourceLedger"]["B"]["cargoExtractionClassPremise"]["classification"]
    checks["terminal concentration, recharge, and temporary tile expiry are preserved"] = state["actors"]["A"]["concentration"]["deadline"] == 618.1 and state["actors"]["A"]["recharge"]["wizard.arch.arcane-sight"] == 0 and state["actors"]["A"]["recharge"]["wizard.arch.dispel-magic"] == 2 and state["actors"]["B"]["recharge"]["wizard.arch.dispel-magic"] == 2 and state["items"]["PG328-W01-403:CLAY-TILE-1"]["expiresAtEventTime"] == 3606.13
    pairs = witness["eventTrace"]["q27CollisionPairs"]
    checks["15 Q27 body/item collision pairs are clear"] = len(pairs) == 15 and not any(x["positiveVolumeOverlap"] for x in pairs)
    checks["unsealed hold and queue state remain unchanged"] = witness["status"] == "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW" and witness["queue"]["mutated"] is False and (witness["queue"]["reviewedApplied"], witness["queue"]["pending"], witness["queue"]["acceptedUnapplied"]) == (830, 18, 0) and witness["scopeBoundary"]["PG200_B06Closed"] is False and witness["scopeBoundary"]["FortressAcceptedOrApplied"] is False
    checks["all manifest artifact byte lengths and hashes match"] = all(Path(item["path"]).stat().st_size == item["bytes"] and sha_file(REPO / item["path"]) == item["sha256"] for item in manifest["artifacts"])
    with zipfile.ZipFile(ARCHIVE) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    expected_members = {Path(item["path"]).name for item in manifest["artifacts"]} | {MANIFEST.name}
    checks["ZIP contains exact packet files with matching contents"] = set(members) == expected_members and all(members[Path(item["path"]).name] == Path(item["path"]).read_bytes() for item in manifest["artifacts"]) and members[MANIFEST.name] == MANIFEST.read_bytes()
    checks["delivery record matches packet and archive"] = delivery["status"] == "READY_FOR_DIRECTOR_REVIEW" and delivery["archive"]["sha256"] == sha_file(ARCHIVE) and delivery["witness"]["sha256"] == sha_file(WITNESS) and delivery["trace"]["sha256"] == sha_file(TRACE) and delivery["sealed"] is False
    checks["builder validation reports all checks passing"] = validation["status"] == "PASS" and validation["failed"] == 0 and validation["passed"] == 14

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        result = {"status": "FAIL", "passed": sum(checks.values()), "failed": len(failed), "checks": [{"name": name, "passed": passed} for name, passed in checks.items()]}
        print(json.dumps(result, indent=2))
        raise SystemExit(1)
    result = {"status": "PASS", "passed": len(checks), "failed": 0, "checks": [{"name": name, "passed": passed} for name, passed in checks.items()], "witnessSha256": sha_file(WITNESS), "traceSha256": sha_file(TRACE), "archiveSha256": sha_file(ARCHIVE), "terminalStateSha256": sha_object(state)}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
