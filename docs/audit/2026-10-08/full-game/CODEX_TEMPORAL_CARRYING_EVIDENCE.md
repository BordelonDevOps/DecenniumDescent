# Additional exact sources: carrying, size, cargo and condition mass

This follow-up is material to the shared body/equipment conference, before adopting a mass/load bridge.

Direct source comparison found V6 carrying capacity STR×15 lb, push/drag/lift twice capacity, size multipliers, optional encumbrance, and Tiny combat space2.5×2.5ft. The existing Gameplay Loop JSON instead uses Load≈10lb, carry limit STR Load, Small−2 and Large×2, burdened at half capacity, and fixed casualty loads. These are not interchangeable formulas. Core's Secure Cargo refers to an Extraction Load class while the gameplay data separately defines physical Load and Extraction Class. The already-reviewed combat overlay explicitly leaves this terminology and capacity/durability reconciliation unfinished.

Core also says Petrified weight×10. A body/form mass rule must preserve applicable current condition effects instead of overwriting them with a bare form/default mass. Carrying a transformed body, carried containers and current melded contents need explicit treatment; casualty Load must not silently become physical body mass.

Please reconcile these exact sources with the three conference questions. Distinguish preserved V6 wording, existing Gameplay mechanics, and any new provisional precedence/conversion/size/condition rule. Do not infer that a newer filename automatically supersedes a domain source. We need one coherent candidate with explicit handling of Tiny space, fractional Loads, capacity versus extraction danger, and mass-changing conditions; the original records stay preserved. If your preceding reply assumed another carrying rule, please correct it before implementation.

## Exact local evidence

```json
{
  "qualification": "Direct source comparison, not adoption of one conflict side.",
  "v6": {
    "path": "docs\\reference\\Player_Rulebook_v6_source_text.txt",
    "sha256": "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b",
    "lines": [
      {
        "line": 7866,
        "text": ""
      },
      {
        "line": 7867,
        "text": "Lifting and Carrying"
      },
      {
        "line": 7868,
        "text": ""
      },
      {
        "line": 7869,
        "text": "Your Strength score determines the amount of weight you can bear. The following terms define what you can lift or carry."
      },
      {
        "line": 7870,
        "text": ""
      },
      {
        "line": 7871,
        "text": "Carrying Capacity. Your carrying capacity is your Strength score multiplied by 15. This is the weight (in pounds) that you can carry, which is high enough that most characters don't usually have to worry about it."
      },
      {
        "line": 7872,
        "text": ""
      },
      {
        "line": 7873,
        "text": "Push, Drag, or Lift. You can push, drag, or lift a weight in pounds up to twice your carrying capacity (or 30 times your Strength score). While pushing or dragging weight in excess of your carrying capacity, your speed drops to 5 feet."
      },
      {
        "line": 7874,
        "text": ""
      },
      {
        "line": 7875,
        "text": "Size and Strength. Larger creatures can bear more weight, whereas Tiny creatures can carry less. For each size category above Medium, double the creature's carrying capacity and the amount it can push, drag, or lift. For a Tiny creature, halve these weights."
      },
      {
        "line": 7876,
        "text": ""
      },
      {
        "line": 7877,
        "text": "Variant: Encumbrance"
      },
      {
        "line": 7878,
        "text": ""
      },
      {
        "line": 7879,
        "text": "The rules for lifting and carrying are intentionally simple. Here is a variant if you are looking for more detailed rules for determining how a character is hindered by the weight of equipment. When you use this variant, ignore the Strength column of the Armor table in Chapter 5."
      },
      {
        "line": 7880,
        "text": ""
      },
      {
        "line": 7881,
        "text": "If you carry weight in excess of 5 times your Strength score, you are encumbered, which means your speed drops by 10 feet."
      },
      {
        "line": 7882,
        "text": ""
      },
      {
        "line": 7883,
        "text": "If you carry weight in excess of 10 times your Strength score, up to your maximum carrying capacity, you are instead heavily encumbered, which means your speed drops by 20 feet and you have disadvantage on ability checks, attack rolls, and saving throws that use Strength, Dexterity, or Constitution."
      },
      {
        "line": 8141,
        "text": "Flying Movement"
      },
      {
        "line": 8142,
        "text": ""
      },
      {
        "line": 8143,
        "text": "If a flying creature is knocked prone, has its speed reduced to 0, or is otherwise unable to move, it falls unless it can hover or is held aloft by magic."
      },
      {
        "line": 8144,
        "text": ""
      },
      {
        "line": 8145,
        "text": "Creature Size"
      },
      {
        "line": 8146,
        "text": ""
      },
      {
        "line": 8147,
        "text": "Creatures occupy space from Tiny (2.5x2.5 ft) to Gargantuan (20x20 ft or larger). Most player races are Medium (5x5 ft). A creature's space is the area it controls in combat."
      },
      {
        "line": 8148,
        "text": ""
      },
      {
        "line": 8149,
        "text": "Squeezing"
      },
      {
        "line": 8150,
        "text": ""
      },
      {
        "line": 8151,
        "text": "A creature can squeeze into a space one size smaller than itself. While squeezing, movement costs 1 extra foot per foot moved, attack rolls and Dexterity saves have disadvantage, and attacks against the creature have advantage."
      }
    ]
  },
  "gameplay": {
    "path": "data\\public\\Decennium_Descent_Gameplay_Loop_v1.json",
    "sha256": "2638699842278c485ea9efdd0728c31ae90a18f25dbe741ac8c14671b0bca78b",
    "sections": {
      "load": {
        "unitApproxPounds": 10,
        "carryLimit": "Strength score",
        "sizeMods": {
          "Small": -2,
          "Medium": 0,
          "Large": "double"
        },
        "burdenedAtHalf": true,
        "burdenedEffects": [
          "Speed -10 ft.",
          "disadvantage on climb/swim/move silently"
        ]
      },
      "extractionClass": {
        "0": "Ordinary trade goods",
        "1": "Common monster parts or durable salvage",
        "2": "Uncommon, fragile, or regulated cargo",
        "3": "Rare artifact, volatile substance, or living captive",
        "4": "Very rare strategic cargo or dangerous curse",
        "5": "Epic cargo likely to attract sovereign or faction intervention",
        "6": "Legendary documented-limit cargo requiring a dedicated operation",
        "tags": [
          "Fragile",
          "Volatile",
          "Cursed",
          "Living",
          "Contraband",
          "Perishable",
          "Attention"
        ]
      },
      "casualtyLoad": {
        "Medium": 6,
        "Small": 3,
        "Large": 12
      }
    }
  },
  "core": {
    "path": "data\\public\\Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "sha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "records": [
      {
        "path": [
          "conditions",
          16
        ],
        "record": {
          "name": "Petrified",
          "rule": "Incapacitated stone-like state; resistance to damage, immunity to poison/disease, weight ×10."
        }
      },
      {
        "path": [
          "combat_maneuvers",
          9
        ],
        "record": {
          "name": "Secure Cargo",
          "rule": "Action; attach, lift, transfer, or protect up to one Extraction Load class of cargo."
        }
      }
    ]
  },
  "alreadyReviewedCombatQualification": [
    "Secure Cargo is an Action for one actual operation involving up to one Extraction Load class; actual load/handling/hands/harnesses/checks/limits/durability remain equipment/extraction dependencies.",
    "The reviewed movement candidate preserves ordinary squeezing: added movement cost, disadvantage on attacks and Dexterity saves, attacks against the creature have advantage.",
    "Current temporal kernel supports finite integer-cell ground geometry only; this is not complete game geometry."
  ]
}
```
