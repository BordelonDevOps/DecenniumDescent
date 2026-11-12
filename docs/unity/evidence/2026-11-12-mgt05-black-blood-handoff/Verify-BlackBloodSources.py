import hashlib
import json
import subprocess
from pathlib import Path

PIN = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
ACCEPTED = "cd113b430f4ba11662efffb60eadbbbb2f420518"

def blob(revision, path):
    raw = subprocess.check_output(["git", "cat-file", "blob", f"{revision}:{path}"])
    return raw, {"revision": revision, "path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

canonical_path = "data/crafting/Decennium_Descent_Crafting_Bible_v4.json"
catalog_bytes, catalog = blob(PIN, canonical_path)
recipes = json.loads(catalog_bytes)["recipes"]
def occurrence(recipe_id):
    for recipe_index, recipe in enumerate(recipes):
        if recipe["id"] == recipe_id:
            for component_index, component in enumerate(recipe["components"]):
                if component["id"] == "drop-black_blood_sample":
                    return {
                        "recipe": recipe_id, "pointer": f"/recipes/{recipe_index}/components/{component_index}",
                        "materialId": component["id"], "tier": component["tier"], "unitMassLb": component["weight"],
                        "quantity": component["quantity"], "category": component["materialCategory"],
                        "properties": component["properties"], "role": component["role"], "consumed": component["consumed"],
                    }
    raise ValueError(recipe_id)

recipe4 = occurrence("recipe-4")
recipe14 = occurrence("recipe-14")
assert recipe4["pointer"] == "/recipes/3/components/3"
assert recipe4["quantity"] == recipe14["quantity"] == 1 and recipe4["unitMassLb"] == recipe14["unitMassLb"] == 0.38
assert all(recipe4[field] == recipe14[field] for field in ("materialId", "tier", "category", "properties", "role", "consumed"))

rules = "DescentReviewChanges/ReviewBible/docs/mechanics/"
inputs = [
    catalog,
    blob(PIN, rules + "CRAFTING_HARVEST_PLAYTEST.md")[1],
    blob(PIN, rules + "CRAFTING_TRADE_REFERENCE.md")[1],
    blob(PIN, rules + "ALCHEMY_PUBLIC_RECIPE_CARDS.md")[1],
    blob(PIN, "docs/canon/CANON_MANIFEST.json")[1],
    blob(ACCEPTED, "docs/manuals/Codex_of_the_Heartcell.md")[1],
    blob(ACCEPTED, "docs/unity/MANUFACTURING_RECIPE14_RULE_DECISIONS.md")[1],
    blob(ACCEPTED, "docs/unity/HARVEST_PRESERVATION_TREATMENT_DECISIONS.md")[1],
    blob(ACCEPTED, "docs/unity/evidence/2026-11-10-mgt05c/MGT05C_RULE_DECISIONS.md")[1],
    blob(ACCEPTED, "engine/com.decennium.foundation/Laboratory/Model/SharedManufacturing.cs")[1],
    blob(ACCEPTED, "engine/com.decennium.foundation/Runtime/Core/HarvestPreservationRecords.cs")[1],
]
for source in ("src/bestiary_data.json", "src/bestiary_data_full.json"):
    raw, row = blob(PIN, source)
    data = json.loads(raw)
    row["candidateDrops"] = [
        {"pointer": f"/{i}/loot/{tier}", "name": entry["name"], "type": entry["type"], "size": entry["size"], "rate": drop["rate"]}
        for i, entry in enumerate(data)
        for tier, drop in entry.get("loot", {}).items()
        if isinstance(drop, dict) and drop.get("drop") == "black blood sample"
    ]
    inputs.append(row)

source_first = 11584
treatment_seconds = 1800
project_seconds = 28800
first_interval = 14400
protected_seconds = 86400
first_phase = 900
settlement = source_first + treatment_seconds
assert settlement < first_interval and settlement + project_seconds < 57600
output = {
    "scope": "Pinned source occurrences and feasibility arithmetic. The selected treatment and handoff have not been implemented or authorized.",
    "sourceInputs": inputs,
    "recipe4Occurrence": recipe4,
    "recipe14Occurrence": recipe14,
    "candidateExactOldTestOnlyLot": "manufacture.recipe14.set0.component2",
    "prospectiveChronology": {
        "measuredExistingWorkshopArrival": source_first, "conditionalTreatmentStart": source_first,
        "treatmentWork": treatment_seconds, "conditionalTreatmentEndAndUnprotectedAge": settlement,
        "priorSelectedInterval": first_interval, "preservationExpiryIfSuccessful": settlement + protected_seconds,
        "conditionalEarliestResearchFinish": settlement + project_seconds,
        "firstPhase": first_phase, "ageAtPhaseEndIfImmediatelyUnprotected": settlement + first_phase,
        "firstBoundaryMargin": first_interval - settlement - first_phase,
        "spoiledBoundary": first_interval * 2,
    },
}
Path(__file__).with_name("source-findings.json").write_text(
    json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
)
