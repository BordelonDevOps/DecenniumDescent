"""Bind every proposed fact definition to its exact source-audited normalization.

This checks document coverage and references, not runtime/disclosure correctness.
Frozen audits are preserved; explicit later decisions take precedence.
"""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent


def read(name):
    return json.loads((PACKET / name).read_text(encoding="utf-8-sig"))


def resolve(reference):
    name, pointer = reference.split("#", 1)
    value = read(name)
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


bindings = {}
inputs = []


def bind(original, audit, pointer, key, kind, cardinality):
    assert original not in bindings, original
    assert resolve(original)["key"] == key, (original, key)
    assert kind in {"Identity", "Boolean", "Integer", "Quantity", "Time", "Code", "GridCell"}, (key, kind)
    assert cardinality in {"Scalar", "List"}, (key, cardinality)
    assert resolve(audit + "#" + pointer)["key"] == key
    bindings[original] = {"key": key, "original": original,
                          "normalization": audit + "#" + pointer,
                          "kind": kind, "cardinality": cardinality}


for name in ["PHYSICAL_CARE_VALUE_NORMALIZATION.json", "MAGIC_VALUE_NORMALIZATION.json",
             "MANAGEMENT_VALUE_NORMALIZATION.json", "TACTICAL_OPERATOR_VALUE_NORMALIZATION.json"]:
    report = read(name)
    inputs.append({"path": name, "sha256": hashlib.sha256((PACKET / name).read_bytes()).hexdigest()})
    if name.startswith("PHYSICAL"):
        for i, field in enumerate(report["fieldNormalizations"]):
            original = Path(field["input"]["path"]).name + "#" + field["input"]["jsonPointer"]
            value = field["normalized"]
            bind(original, name, f"/fieldNormalizations/{i}", field["key"], value["kind"], value["cardinality"])
    elif name.startswith("MAGIC"):
        for i, field in enumerate(report["factDefinitions"]):
            bind(field["sourceContractRef"], name, f"/factDefinitions/{i}", field["key"],
                 field["kind"], field["cardinality"])
    elif name.startswith("MANAGEMENT"):
        for identity, field in report["definitions"].items():
            value = report["namedTypes"][field["typeRef"]]
            bind("MANAGEMENT_WORK_FACT_REGISTRY_PROPOSAL.json#/factDefinitions/" + identity,
                 name, "/definitions/" + identity, field["key"], value["kind"], field["cardinality"])
    else:
        for i, field in enumerate(report["fields"]):
            value = field["normalizedValue"]
            bind(field["originalDefinition"], name, f"/fields/{i}", field["key"],
                 value["kind"], value["cardinality"])

registry = read("FACT_REGISTRY_INDEX.json")
operations = registry["operations"] + registry["operatorKinds"]
references = [field["definition"] for operation in operations for field in operation["orderedFields"]]
assert len(references) == 2850
assert len(bindings) == 1097
assert set(references) == set(bindings), {
    "missing": sorted(set(references) - set(bindings)),
    "extra": sorted(set(bindings) - set(references)),
}
for operation in operations:
    for field in operation["orderedFields"]:
        assert bindings[field["definition"]]["key"] == field["key"]

result = {
    "schemaVersion": 1,
    "status": "COMPLETE_DEFINITION_BINDING_SOURCE_AUDITS_NOT_RUNTIME_QUALIFICATION",
    "sourceApiAccepted": False,
    "runtimeAuthorized": False,
    "counts": {"operationKinds": len(operations), "uniqueDefinitions": len(bindings),
               "operationFieldReferences": len(references),
               "fixedListDefinitions": sum(x["cardinality"] == "List" for x in bindings.values())},
    "inputs": inputs,
    "effectiveCorrections": "VALUE_NORMALIZATION_CORRECTIONS.md",
    "precedence": "Frozen audits retain reviewed proposal wording. Explicit actual GPT decisions and independent source corrections override only their named fields; no global access or availability expansion.",
    "definitions": list(bindings.values()),
    "verificationLimits": "Exact set/key/closed-kind/cardinality/reference binding only. Does not establish semantic source accuracy, current disclosure, emitted values, runtime purity, branch/profile execution or full HC acceptance.",
}
(PACKET / "VALUE_NORMALIZATION_INDEX.json").write_bytes(
    (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
print(json.dumps(result["counts"]))
