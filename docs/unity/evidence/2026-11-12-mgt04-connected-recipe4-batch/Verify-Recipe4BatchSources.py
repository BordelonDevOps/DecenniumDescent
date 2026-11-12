import hashlib
import json
import subprocess
from pathlib import Path


CANON = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
ENGINE = "246ca4e4899469241402899ba6750d4379d035a9"
EVIDENCE = "95eb1a5992cc7beaa201000bc3f08ee0f30fd559"
PACKAGE = "engine/com.decennium.foundation/"
MECHANICS = "DescentReviewChanges/ReviewBible/docs/mechanics/"
HANDOFF = "docs/unity/evidence/2026-11-12-mgt05-black-blood-handoff/"
sources = []


def read(revision, path):
    raw = subprocess.check_output(["git", "cat-file", "blob", f"{revision}:{path}"])
    sources.append(
        {"revision": revision, "path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    )
    return raw


catalogue = json.loads(read(CANON, "data/crafting/Decennium_Descent_Crafting_Bible_v4.json"))
recipe = catalogue["recipes"][3]
assert recipe["id"] == "recipe-4" and recipe["name"] == "Superior Vital Potion of Black Blood"
assert recipe["skill"] == "Alchemy" and recipe["skillLevel"] == 5 and recipe["difficulty"] == 8
assert recipe["quantity"] == 5 and recipe["mechanics"]["healing"] == "2d4+2"
assert recipe["workRequirements"]["activeWorkHours"] == 4 and recipe["workRequirements"]["maximumAssistants"] == 0
assert recipe["discovery"]["requiresFormula"] and not recipe["discovery"]["formulaConsumed"]
components = [
    {key: part[key] for key in ("id", "quantity", "weight", "role", "consumed")}
    for part in recipe["components"]
]
assert components[-1] == {
    "id": "drop-black_blood_sample", "quantity": 1, "weight": 0.38, "role": "catalyst", "consumed": True
}
cards = read(CANON, MECHANICS + "ALCHEMY_PUBLIC_RECIPE_CARDS.md").decode()
card = cards.split("## recipe-4 ", 1)[1].split("## recipe-5 ", 1)[0]
assert "2d4+2 ordinary magical nonspell HP" in card and "at full Masterwork yield 2" in card
assert "half-batch-quantity" in card and "maximum/current HP 2" in card
procedure = read(CANON, MECHANICS + "ALCHEMY_RECIPE_PLAYTEST.md").decode()
assert "actual closed working apparatus" in procedure and "while its vessel remains sealed and intact" in procedure
assert "resuming its clock upon return" in procedure
crafting = read(CANON, MECHANICS + "CRAFTING_HARVEST_PLAYTEST.md").decode()
assert "Masterwork preserves **one component unit total**" in crafting
assert "Abandonment after work starts loses consumed inputs" in crafting
read(CANON, MECHANICS + "CRAFTING_TRADE_REFERENCE.md")
read(CANON, "docs/canon/CANON_MANIFEST.json")

map_data = json.loads(read(ENGINE, "docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json"))
mapped = next(row for row in map_data["workItems"] if row["id"] == "MGT-04")
assert mapped["dependencies"] == ["MGT-01", "MGT-02", "RUL-01"]
read(ENGINE, "docs/unity/MANUFACTURING_RULE_SCOPE.md")
read(ENGINE, "docs/unity/MANUFACTURING_RECIPE14_RULE_DECISIONS.md")
read(ENGINE, PACKAGE + "Laboratory/Model/ManufacturingRules.cs")
adapter = read(ENGINE, PACKAGE + "Laboratory/Model/SharedManufacturing.cs").decode()
assert "HealingPotential(first.Value+second.Value+4)" in adapter
assert "first.Value+1,second.Value+1,potential,actualHealing" in adapter
assert "SharedManufacturingFixture.Lot(recipe.Id,c.X,i)" in adapter
dice = read(ENGINE, PACKAGE + "Runtime/Core/DiceStream.cs").decode()
assert "return new BoundedDraw((int)(value%outcomes),state,words)" in dice
read(ENGINE, PACKAGE + "Laboratory/Model/SharedConnectedFormulaResearch.cs")
read(ENGINE, PACKAGE + "Runtime/Core/ConnectedBloodSpecimen.cs")
read(ENGINE, PACKAGE + "Runtime/Core/ManufacturingRecords.cs")
read(ENGINE, PACKAGE + "Runtime/Core/HarvestPreservationRecords.cs")
timeline = json.loads(read(EVIDENCE, HANDOFF + "focused/timeline.json"))
cutoff = next(row for row in timeline["savedStates"] if row["save"].endswith("-cutoff.ddsave"))
assert cutoff["eligible"] and cutoff["amount"] == "1/1" and cutoff["manufacturingOrders"] == 0

result = {
    "status": "PASS",
    "sourceInputs": sources,
    "mappedWork": {key: mapped[key] for key in ("id", "title", "acceptance", "dependencies")},
    "recipe": {
        "pointer": "/recipes/3",
        "id": recipe["id"],
        "name": recipe["name"],
        "skill": recipe["skill"],
        "skillLevel": recipe["skillLevel"],
        "difficulty": recipe["difficulty"],
        "requiresFormula": recipe["discovery"]["requiresFormula"],
        "workRequirements": recipe["workRequirements"],
        "components": components,
        "yield": {"Flawed": 2, "Standard": 5, "ExceptionalFull": 6, "MasterworkFull": 7},
        "firstPhaseSeconds": 900,
        "remainingPhaseSeconds": 13500,
        "sourceVessels": 5,
        "supplementaryGlassVialsAtFullMasterwork": 2,
        "doseMassLb": "1/5",
        "authoredHealing": recipe["mechanics"]["healing"],
        "priorRuntimeHealing": "2d4+2",
        "runtimeHealingArithmetic": "Two zero-based values (0 through 3) plus 4 equal two recorded d4 faces plus 2.",
    },
    "acceptedCutoff": cutoff,
}
Path(__file__).with_name("source-findings.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
)
