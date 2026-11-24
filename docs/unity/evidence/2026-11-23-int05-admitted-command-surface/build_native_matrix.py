"""Index bounded native audits without treating source review as runtime coverage."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent


def read(name):
    return json.loads((PACKET / name).read_text(encoding="utf-8-sig"))


def digest(name):
    return hashlib.sha256((PACKET / name).read_bytes()).hexdigest()


def axis_name(axis):
    return axis[0] if isinstance(axis, list) else axis["axis"]


def axis_disposition(axis):
    return axis[1] if isinstance(axis, list) else axis["disposition"]


inventory = read("OPERATION_INVENTORY.json")
indexed = {row["kind"]: row for row in inventory["operations"]}
assert len(indexed) == 78
reports = [
    ("INDEPENDENT_MANAGEMENT_AUDIT.json", "semanticBranchDisposition"),
    ("INDEPENDENT_MAGIC_AUDIT.json", "branches"),
    ("INDEPENDENT_PHYSICAL_AUDIT.json", "axes"),
    ("INDEPENDENT_WORK_AUDIT.json", "semanticBranchDisposition"),
    ("INDEPENDENT_CARE_REST_AXES.json", "axes"),
    ("INDEPENDENT_TACTICAL_AXES.json", "axes"),
]
bindings = {}
inputs = [{"path": "OPERATION_INVENTORY.json", "sha256": digest("OPERATION_INVENTORY.json")}]
for name, axis_key in reports:
    report = read(name)
    inputs.append({"path": name, "sha256": digest(name)})
    for op_index, operation in enumerate(report["operations"]):
        kind = operation["kind"]
        assert kind in indexed and kind not in bindings, (name, kind)
        axes = operation[axis_key]
        assert [axis_name(axis) for axis in axes] == indexed[kind]["semanticBranchesToDisposition"], (name, kind)
        bindings[kind] = {
            "nativeAudit": name + "#/operations/" + str(op_index),
            "reviewScope": "BOUNDED_INDEPENDENT_SOURCE_AUDIT_NOT_FULL_CONTRACT_OR_EXECUTION",
            "branches": [
                {
                    "axis": axis_name(axis),
                    "audit": name + "#/operations/" + str(op_index) + "/" + axis_key + "/" + str(i),
                    "disposition": axis_disposition(axis),
                    "v1ExecutionQualified": False,
                }
                for i, axis in enumerate(axes)
            ],
        }

tactical_name = "TACTICAL_EXPLORATION_OPERATION_AUDIT.md"
tactical = (PACKET / tactical_name).read_text(encoding="utf-8-sig")
inputs.append({"path": tactical_name, "sha256": digest(tactical_name)})
assert set(bindings) == set(indexed), "Every candidate needs its exact independent branch allocation"

rows = []
for operation in inventory["operations"]:
    kind = operation["kind"]
    rows.append({
        "id": operation["id"],
        "kind": kind,
        "family": operation["family"],
        "profileBinding": "PROFILE_ADMISSION_MATRIX.json; exact host/native parameter predicates remain in the native audit",
        **bindings[kind],
        "publicFieldKeyAndPredicateContract": "OPEN_BEFORE_IMPLEMENTATION",
        "fivePathAllocation": "OPEN_BEFORE_IMPLEMENTATION",
        "runtimeQualified": False,
    })

assert len(rows) == 78
assert sum(len(row["branches"]) for row in rows) == 204
operators = [
    {"kind": kind, "nativeAudit": tactical_name, "principal": "EXISTING_SESSION_OPERATOR_ONLY",
     "fieldAndWitnessContract": "OPEN", "runtimeQualified": False}
    for kind in inventory["operatorKinds"]
]
assert len(operators) == 2
result = {
    "schemaVersion": 1,
    "status": "SOURCE_AUDIT_INDEX_WITH_EXPLICIT_OPEN_CONTRACT_FIELDS_NOT_EXECUTABLE_COVERAGE",
    "sourceApiAccepted": False,
    "runtimeAuthorized": False,
    "counts": {
        "candidateKinds": len(rows), "semanticAxes": sum(len(row["branches"]) for row in rows),
        "operatorKinds": len(operators), "supportedFactoryDeclarations": 24,
        "newApiQualifiedKinds": 0,
        "exactBranchAllocationsStillOpenAfterTacticalAudit": sum(
            axis["disposition"] == "EXACT_BRANCH_WITNESS_ALLOCATION_OPEN_AFTER_NATIVE_GUARD_AUDIT"
            for row in rows for axis in row["branches"]),
    },
    "inputs": inputs,
    "operations": rows,
    "operatorKinds": operators,
    "remaining": [
        "Finish exact public DTO field keys, native causal bindings and actual current-disclosure predicates",
        "Resolve conditional/post-time and deterministic capacity assessment mapping without legacy changes",
        "Execute allocated tactical/exploration genuine branches; preserve prospective/model-only reachability gaps",
        "Freeze supported-factory/selected-parameter equivalence witnesses and all five execution paths",
        "Complete transitive pure-read/checkpoint writer audit and instrumentation plan",
        "Obtain actual GPT and Codex full HC01-05 concurrence before runtime implementation",
    ],
}
(PACKET / "NATIVE_OPERATION_MATRIX.json").write_bytes(
    (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
print(json.dumps(result["counts"]))
