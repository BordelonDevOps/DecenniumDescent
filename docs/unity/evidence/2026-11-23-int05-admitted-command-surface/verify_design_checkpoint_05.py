"""Read-only checkpoint05 document/source verification; never runs the engine."""
import hashlib
import json
import subprocess
from pathlib import Path

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = "6bf494b716bf325271839ac11c4849cba26c91e7"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def read(name):
    return json.loads((PACKET / name).read_text(encoding="utf-8-sig"))

def digest(data):
    return hashlib.sha256(data).hexdigest()

historical = {}
for reconciliation in ("INPUT_VERSION_RECONCILIATION_04.json", "INPUT_VERSION_RECONCILIATION_05.json"):
    for pin in read(reconciliation)["historicalInputs"]:
        historical[(pin["originalPath"],pin["sha256"])] = ROOT/pin["retainedPath"]
reports = [
    "INDEPENDENT_TACTICAL_AXES.json", "CODEC_TRANSITIVE_SOURCE_AUDIT.json",
    "PHYSICAL_FACT_REGISTRY_PROPOSAL.json", "MANAGEMENT_WORK_FACT_REGISTRY_PROPOSAL.json",
    "MAGIC_ADVANCEMENT_FACT_REGISTRY_PROPOSAL.json", "TACTICAL_OPERATOR_FACT_REGISTRY_PROPOSAL.json",
    "CARE_REST_FACT_REGISTRY_PROPOSAL.json", "INDEPENDENT_CARE_FACT_REVIEW.json",
    "CARE_FACT_REGISTRY_SUPPLEMENT.json", "CHECKPOINT_REVIEW_04.json",
    "CURRENT_COPY_ALIAS_AUDIT.json", "PHYSICAL_CARE_PARAMETER_CONTRACT_PROPOSAL.json",
    "MAGIC_ADVANCEMENT_PARAMETER_CONTRACT_PROPOSAL.json", "MANAGEMENT_WORK_PARAMETER_CONTRACT_PROPOSAL.json",
    "TACTICAL_OPERATOR_PARAMETER_CONTRACT_PROPOSAL.json", "PARAMETER_CROSS_FAMILY_REVIEW_01.json",
    "CURRENT_FACT_HELPER_AUDIT.json", "CURRENT_PERMISSION_SIGHT_AUDIT.json", "PROCEDURE_INVENTORY_READ_AUDIT.json",
    "TACTICAL_OPERATOR_READ_EXTRACTION_PLAN.json", "MAGIC_READ_EXTRACTION_PLAN.json", "MANAGEMENT_READ_EXTRACTION_PLAN.json",
    "PHYSICAL_CARE_READ_EXTRACTION_PLAN.json", "CHECKPOINT_REVIEW_05.json", "MAGIC_EXAMPLE_RECIPES.json",
]
verified = set()
historical_uses = []
git_cache = {}
for name in reports:
    report = read(name)
    for key in ("pins", "sourcePins", "inputPins", "reviewedDocuments", "referencePins", "contractPins", "nativeSourcePins", "independentlyInspectedNativePins", "principalNativeSourcePins"):
        for pin in report.get(key, []):
            path, expected = pin["path"], pin["sha256"]
            data = (ROOT / path).read_bytes()
            if digest(data) != expected:
                retained = historical.get((path, expected))
                assert retained is not None and digest(retained.read_bytes()) == expected, (name, path)
                historical_uses.append({"report": name, "originalPath": path, "sha256": expected})
            else:
                revision = pin.get("revision", pin.get("originalAuthorityRevision"))
                if not revision and path.startswith("engine/com.decennium.foundation/"):
                    revision = BASELINE
                if revision:
                    binding = (revision, path)
                    if binding not in git_cache:
                        git_cache[binding] = git("show", revision + ":" + path)
                    assert data == git_cache[binding], (name, revision, path)
            verified.add((path, expected))

inventory = read("OPERATION_INVENTORY.json")
ops = {o["kind"]: o for o in inventory["operations"]}
assert len(ops) == 78
assert sum(len(o["semanticBranchesToDisposition"]) for o in ops.values()) == 204
assert len(inventory["operatorKinds"]) == 2
tactical = read("TACTICAL_OPERATOR_FACT_REGISTRY_PROPOSAL.json")
axes = 0
for op in tactical["operations"]:
    if op["operatorOnly"]:
        assert op["kind"] in inventory["operatorKinds"]
    else:
        assert op["semanticBranchesToDisposition"] == ops[op["kind"]]["semanticBranchesToDisposition"]
        assert [a["axis"] for a in op["branchDispositions"]] == op["semanticBranchesToDisposition"]
        axes += len(op["branchDispositions"])
assert axes == 58
physical = read("PHYSICAL_CARE_PARAMETER_CONTRACT_PROPOSAL.json")
assert physical["counts"]["operations"] == 23 and physical["counts"]["axes"] == 64
assert not read("FACT_REGISTRY_INDEX.json")["runtimeAuthorized"]
assert read("FACT_REGISTRY_INDEX.json")["counts"]["candidateKindsWithProposedFields"] == 78
assert read("FACT_REGISTRY_INDEX.json")["counts"]["operatorKindsWithProposedFields"] == 2
assert read("FACT_REGISTRY_INDEX.json")["counts"]["newApiQualifiedKinds"] == 0
assert read("NATIVE_OPERATION_MATRIX.json")["counts"]["exactBranchAllocationsStillOpenAfterTacticalAudit"] == 0

parameters = read("PARAMETER_CONTRACT_INDEX.json")
extraction = read("READ_EXTRACTION_INDEX.json")
for index in (parameters, extraction, read("FACT_REGISTRY_INDEX.json")):
    assert not index["sourceApiAccepted"] and not index["runtimeAuthorized"]
    for pin in index["inputs"]:
        assert digest((PACKET/pin["path"]).read_bytes()) == pin["sha256"], pin["path"]
    assert {o["kind"] for o in index["operations"]} == set(ops)
    assert {o["kind"] for o in index["operatorKinds"]} == set(inventory["operatorKinds"])
for index in (parameters,extraction):
    for row in index["operations"]:
        assert row["exactAxes"] == ops[row["kind"]]["semanticBranchesToDisposition"]
        assert not row["runtimeQualified"]
for row in parameters["operations"]+parameters["operatorKinds"]:
    assert [v["variantOrdinal"] for v in row["variants"]] == list(range(len(row["variants"])))
assert parameters["counts"]["registeredVariants"] == 145
hide = next(o for o in read("FACT_REGISTRY_INDEX.json")["operations"] if o["kind"] == "Hide")
assert next(f for f in hide["orderedFields"] if f["key"]=="guidance.consumed.actual")["effectiveDisposition"] == "Withheld"

care = read("INDEPENDENT_CARE_FACT_REVIEW.json")
assert digest((PACKET / "CARE_REST_FACT_REGISTRY_PROPOSAL.json").read_bytes()) == care["reviewedSha256"]
route = read("PRINCIPAL_ROUTE_ALLOCATION.json")
assert len(route["orderedCommands"]) == 244
assert [r["revision"] for r in route["orderedCommands"]] == list(range(244))
assert len(route["checkpointRevisions"]) == 28
for pin in route["archiveBinding"]["members"]:
    data = (ROOT / pin["path"]).read_bytes()
    assert len(data) == pin["bytes"] and digest(data) == pin["sha256"], pin["path"]

old_status = json.loads(git("show", BASELINE + ":docs/unity/IMPLEMENTATION_STATUS.json"))
new_status = json.loads((ROOT / "docs/unity/IMPLEMENTATION_STATUS.json").read_text(encoding="utf-8"))
old_status["nextModule"]["latestDesignReview"] = new_status["nextModule"]["latestDesignReview"]
assert old_status == new_status
assert not new_status["nextModule"]["implementationAuthorized"]
assert not new_status["nextModule"]["runtimeStarted"]
assert not git("diff", BASELINE, "--", "engine/com.decennium.foundation", "engine/tools", "engine/hosts").strip()
for name in ("OPERATION_INVENTORY.json", "PROFILE_ADMISSION_MATRIX.json", "MODULE_DEFINITION.md"):
    rel = (PACKET / name).relative_to(ROOT).as_posix()
    assert (PACKET / name).read_bytes() == git("show", BASELINE + ":" + rel), name

parsed = 0
for path in PACKET.glob("*.json"):
    json.loads(path.read_text(encoding="utf-8-sig"))
    parsed += 1
result = {
    "status": "PASS_DOCUMENT_AND_SOURCE_VERIFICATION_ONLY",
    "baseline": BASELINE,
    "reviewReports": len(reports),
    "uniquePinnedPathAndHashPairs": len(verified),
    "gitBlobBindingsVerified": len(git_cache),
    "retainedHistoricalDesignInputUses": historical_uses,
    "packetJsonParsed": parsed,
    "candidateKinds": 78,
    "operatorKinds": 2,
    "semanticAxes": 204,
    "proposedOperationFieldReferences": read("FACT_REGISTRY_INDEX.json")["counts"]["operationFieldEntries"],
    "parameterKinds": 80,
    "registeredParameterVariants": 145,
    "readExtractionKinds": 80,
    "principalCommands": 244,
    "principalCheckpoints": 28,
    "machineStatusOnlyLatestDesignReviewChanged": True,
    "runtimeToolsHostsUnchanged": True,
    "runtimeBuildsTestsGameplayOrQualificationExecuted": False,
    "sourceApiAccepted": False,
}
print(json.dumps(result, indent=2))
