"""Validate and index proposed field registries without granting disclosure or runtime acceptance."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent

def read(name):
    return json.loads((PACKET / name).read_text(encoding="utf-8-sig"))

def digest(name):
    return hashlib.sha256((PACKET / name).read_bytes()).hexdigest()

inventory = read("OPERATION_INVENTORY.json")
bindings = {}
inputs = []
reports = [
    ("MANAGEMENT_WORK_FACT_REGISTRY_PROPOSAL.json", "management"),
    ("PHYSICAL_FACT_REGISTRY_PROPOSAL.json", "physical"),
    ("MAGIC_ADVANCEMENT_FACT_REGISTRY_PROPOSAL.json", "magic"),
    ("CARE_REST_FACT_REGISTRY_PROPOSAL.json", "care"),
    ("TACTICAL_OPERATOR_FACT_REGISTRY_PROPOSAL.json", "management"),
]
for name, family in reports:
    report = read(name)
    inputs.append({"path": name, "sha256": digest(name)})
    for i, operation in enumerate(report["operations"]):
        kind = operation["kind"]
        assert kind not in bindings, kind
        fields = []
        if family == "management":
            for reference in operation["factDefinitionRefs"]:
                field = report["factDefinitions"][reference]
                fields.append((field["key"], "#/factDefinitions/" + reference))
            assert [f[0] for f in fields] == operation["requiredFactKeys"]
        elif family == "physical":
            groups = {g["id"]: (n, g) for n, g in enumerate(report["factGroups"])}
            group_ids = operation.get("groups", [])
            for variant in operation.get("variants", []):
                group_ids = group_ids + variant["groups"]
            for group_id in group_ids:
                n, group = groups[group_id]
                for f, field in enumerate(group["fields"]):
                    fields.append((field["key"], "#/factGroups/" + str(n) + "/fields/" + str(f)))
        elif family == "magic":
            for f, field in enumerate(operation["facts"]):
                fields.append((field["key"], "#/operations/" + str(i) + "/facts/" + str(f)))
            for group_id in operation.get("currentFactGroupRefs", []):
                for f, field in enumerate(report["currentFactGroups"][group_id]):
                    fields.append((field["key"], "#/currentFactGroups/" + group_id + "/" + str(f)))
        elif family == "care":
            for group_id in operation["fieldGroups"]:
                for f, field in enumerate(report["fieldGroups"][group_id]["fields"]):
                    fields.append((field["key"], "#/fieldGroups/" + group_id + "/fields/" + str(f)))
        assert len({key for key, _ in fields}) == len(fields), (kind, "duplicate key")
        bindings[kind] = {
            "proposal": name + "#/operations/" + str(i),
            "fieldCount": len(fields),
            "orderedFields": [{"key": key, "definition": name + ref} for key, ref in fields],
            "status": "PROPOSED_EXACT_FIELDS_WITH_EXPLICIT_UNAPPROVED_DISCLOSURE_NOT_FULL_CONTRACT_ACCEPTANCE",
        }

supplement_name = "CARE_FACT_REGISTRY_SUPPLEMENT.json"
supplement = read(supplement_name)
inputs.append({"path": supplement_name, "sha256": digest(supplement_name)})
assert supplement["parentRegistryReviewedSha256"] == digest("CARE_REST_FACT_REGISTRY_PROPOSAL.json")
for i, addition in enumerate(supplement["operationAdditions"]):
    binding = bindings[addition["kind"]]
    binding["supplement"] = supplement_name + "#/operationAdditions/" + str(i)
    for group_id in addition["appendGroups"]:
        for f, field in enumerate(supplement["fieldGroups"][group_id]["fields"]):
            assert field["key"] not in {row["key"] for row in binding["orderedFields"]}
            binding["orderedFields"].append({
                "key": field["key"],
                "definition": supplement_name + "#/fieldGroups/" + group_id + "/fields/" + str(f),
            })
    binding["fieldCount"] = len(binding["orderedFields"])

rows = []
for operation in inventory["operations"]:
    kind = operation["kind"]
    rows.append({"kind": kind, "family": operation["family"], **bindings.get(kind, {
        "status": "EXACT_FIELD_REGISTRY_IN_PROGRESS",
        "fieldCount": 0,
        "orderedFields": [],
    }), "newApiQualified": False})
assert len(rows) == 78
assert set(bindings) == {row["kind"] for row in rows} | set(inventory["operatorKinds"])
operators = [{"kind": kind, **bindings[kind], "newApiQualified": False}
             for kind in inventory["operatorKinds"]]
result = {
    "schemaVersion": 1,
    "status": "SOURCE_DESIGN_INDEX_NOT_DISCLOSURE_AUTHORITY_OR_RUNTIME_COVERAGE",
    "sourceApiAccepted": False,
    "runtimeAuthorized": False,
    "counts": {
        "candidateKinds": len(rows),
        "operatorKinds": len(operators),
        "candidateKindsWithProposedFields": sum(row["fieldCount"] > 0 for row in rows),
        "candidateKindsAwaitingProposal": sum(row["fieldCount"] == 0 for row in rows),
        "operatorKindsWithProposedFields": len(operators),
        "operationFieldEntries": sum(row["fieldCount"] for row in rows + operators),
        "newApiQualifiedKinds": 0,
    },
    "commonAttemptFacts": "DETAILED_RESULT_CONTRACT.md; actual result/receipt/continuation fields apply separately",
    "inputs": inputs,
    "operations": rows,
    "operatorKinds": operators,
    "remaining": [
        "Independently reconcile all proposed family fields and private/public boundaries as one contract",
        "Concur on each explicitly new historical/current disclosure predicate and any withheld retained family",
        "Normalize exact DTO types, instance context, optional sentinel applicability and public vocabulary",
        "Freeze the full parameter/domain and per-profile/branch/five-path expected-output allocation",
        "Verify every V1 read dependency, exact state/copy invariants and concrete materialized-condition carrier",
        "Obtain actual GPT and Codex full HC01-05 agreement before runtime",
    ],
}
(PACKET / "FACT_REGISTRY_INDEX.json").write_bytes(
    (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
print(json.dumps(result["counts"]))
