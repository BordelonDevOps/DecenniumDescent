# Monster combat schema

`bestiary_data_full.json` may attach an optional `combat` object to a monster. A missing object means that the companion has no executable combat payload for that record; it does **not** imply that the monster has no attacks.

All newly authored combat data without a cited rulebook source must set `draft: true`. The first pilot deliberately follows this rule.

## Shape

```json
{
  "combat": {
    "schemaVersion": 1,
    "draft": true,
    "source": "companion-authored draft",
    "defaultActionId": "multiattack",
    "saveDc": 14,
    "defenses": {
      "resistances": ["poison"],
      "immunities": [],
      "conditionImmunities": []
    },
    "attacks": [
      {
        "id": "multiattack",
        "name": "Multiattack",
        "kind": "attack",
        "actionCost": "action",
        "usage": "atWill",
        "count": 2,
        "attackBonus": 6,
        "range": { "reachFt": 10 },
        "targets": { "count": 1, "scope": "creature" },
        "damage": [{ "dice": "2d8+4", "average": 13, "type": "piercing" }]
      },
      {
        "id": "spore-burst",
        "name": "Spore Burst",
        "kind": "save",
        "actionCost": "action",
        "usage": "recharge",
        "recharge": { "minimumRoll": 5, "dieSides": 6 },
        "save": { "ability": "constitution", "dc": 14, "onSuccess": "half" },
        "range": { "radiusFt": 20 },
        "targets": { "scope": "creatures-in-area" },
        "damage": [{ "dice": "4d6", "average": 14, "type": "poison" }]
      }
    ]
  }
}
```

## Required fields

`combat` requires `schemaVersion`, `draft`, `source`, `defenses`, and a non-empty `attacks` array. `defenses` always provides `resistances`, `immunities`, and `conditionImmunities` arrays, even when empty.

Every attack requires `id`, `name`, `kind` (`attack` or `save`), `actionCost`, `usage` (`atWill`, `recharge`, or `limited`), `targets`, and non-empty `damage`. Each damage component requires `dice`, numeric `average`, and `type`.

- An `attack` action requires numeric `attackBonus`; `count` defaults to 1.
- A `save` action requires `save.ability`, numeric `save.dc`, and `save.onSuccess` (`none` or `half`). `combat.saveDc` is an optional convenience default only.
- `range` may state `reachFt`, `rangeFt`, and/or `radiusFt`.
- A `recharge` action requires `recharge.minimumRoll` and `recharge.dieSides`; it must not be treated as at-will DPR.
- A `limited` action requires a `uses` count and reset description in `reset`.

`defaultActionId` identifies the at-will action used for sustained single-target simulation. The balance harness uses at-will DPR by default and may optionally add **expected recharge DPR** via `expectedRechargeDpr()` / `totalExpectedMonsterDpr()` in `src/lib/monster-combat.mjs`.

### Recharge expected DPR (draft sim assumptions)

When the combat sim includes recharge (`includeRecharge: true`), it applies these **explicit simplifications** — not rules-complete 5e:

1. **Availability:** Recharge is treated as available on round 1. Each later turn, steady-state availability equals `P(d6 roll ≥ minimumRoll)` (e.g. recharge `5-6` → **2/6 ≈ 0.33** per round).
2. **Save actions:** Flat **55%** save-fail rate vs a level-appropriate party; success halves damage (`onSuccess: half`).
3. **Area scope:** `creatures-in-area` recharges are modeled as **single-target full expected damage** (conservative — real area hits may increase party loss).
4. **Action economy:** Recharge and at-will damage stack in the same round when recharge is available (upper-bound burst, not mutually exclusive action choices).

These assumptions are for **draft balance alerts only** until initiative, action economy, and multi-target saves are modeled.

## Adapter contract

`resolveMonsterCombat(monster)` from `src/lib/monster-combat.mjs` returns:

- `{ combat, reason: null }` when the optional payload is structurally usable;
- `{ combat: null, reason }` for absent, malformed, or attackless payloads.

Consumers must surface the reason and fall back only to a clearly labeled estimate. They must never silently convert missing combat data into a zero-DPR monster.
