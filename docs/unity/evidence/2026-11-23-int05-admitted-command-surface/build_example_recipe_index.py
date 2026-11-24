"""Reconcile finite example recipes with frozen kinds, semantic axes and ordinals."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent


def read(name):
    return json.loads((PACKET / name).read_text(encoding="utf-8-sig"))


parameters = read("PARAMETER_CONTRACT_INDEX.json")
expected = {x["kind"]: x for x in parameters["operations"] + parameters["operatorKinds"]}
operations = {}
inputs = []
for name in ["PHYSICAL_CARE_EXAMPLE_RECIPES.json", "MAGIC_EXAMPLE_RECIPES.json",
             "MANAGEMENT_EXAMPLE_RECIPES.json", "TACTICAL_OPERATOR_EXAMPLE_RECIPES.json"]:
    report = read(name)
    inputs.append({"path": name, "sha256": hashlib.sha256((PACKET / name).read_bytes()).hexdigest()})
    for i, operation in enumerate(report["operations"]):
        kind = operation["kind"]
        assert kind not in operations
        contract = expected[kind]
        assert operation["exactAxes"] == contract["exactAxes"], kind
        variants = [{"variantKey": x["variantKey"], "variantOrdinal": x["variantOrdinal"],
                     "recipe": f"{name}#/operations/{i}/variants/{j}"}
                    for j, x in enumerate(operation["variants"])]
        assert [(x["variantKey"], x["variantOrdinal"]) for x in variants] == [
            (x["variantKey"], x["variantOrdinal"]) for x in contract["variants"]], kind
        operations[kind] = {"kind": kind, "operatorOnly": contract["operatorOnly"],
                            "exactAxes": operation["exactAxes"], "variants": variants,
                            "recipe": f"{name}#/operations/{i}", "runtimeQualified": False}

assert operations.keys() == expected.keys()
ordered = [operations[x["kind"]] for x in parameters["operations"] + parameters["operatorKinds"]]
counts = {"candidateKinds": sum(not x["operatorOnly"] for x in ordered),
          "operatorKinds": sum(x["operatorOnly"] for x in ordered),
          "candidateAxes": sum(len(x["exactAxes"]) for x in ordered if not x["operatorOnly"]),
          "registeredVariants": sum(len(x["variants"]) for x in ordered),
          "executedExampleRecipes": 0}
assert (counts["candidateKinds"], counts["operatorKinds"], counts["candidateAxes"],
        counts["registeredVariants"]) == (78, 2, 204, 145)
result = {
    "schemaVersion": 1,
    "status": "FINITE_RECIPE_ALLOCATION_NOT_EXECUTED_OR_FULL_CONTRACT_ACCEPTANCE",
    "counts": counts, "inputs": inputs, "operations": ordered,
    "effectiveOrder": "Actual GPT06: native numeric CommandKind, frozen variantOrdinal, then Core-owned StringComparer.Ordinal on existing internal Command.Fingerprint for authorized candidate payloads; identical canonical payloads coalesced with associations, differing effective payload ties block qualification. Public ordinal assigned after filtering; no hidden/private index or generated-ID tie break.",
    "effectiveRepresentation": "REPRESENTATION_DECISIONS_07.md and VALUE_NORMALIZATION_CORRECTIONS.md override only exact pending wording in frozen recipes/audits.",
    "limits": [
        "Finite example recipes are not exhaustive constrained rational domains or actual gameplay witnesses.",
        "Descriptions preserve lawful domains when no currently authorized concrete example exists.",
        "Management single-preference mining sampling proposal, exact owned-lot unit bindings and differing portable/lot identity joins still need their precise dispositions.",
        "All recipe output, derived-ID/current-principal collision handling, native order/purity and five-path parity remain to be executed after full HC agreement.",
    ],
    "sourceApiAccepted": False, "runtimeAuthorized": False,
}
(PACKET / "EXAMPLE_RECIPE_INDEX.json").write_bytes(
    (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
print(json.dumps(counts))
