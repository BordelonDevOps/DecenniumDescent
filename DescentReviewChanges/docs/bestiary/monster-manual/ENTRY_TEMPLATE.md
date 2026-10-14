# MM entry template — Monster Manual of the Decennium

**Use:** Copy into `entries/<slug>.md`. Fill every **Required** field. Optional fields may be `—` or omitted only if marked Optional.

**Mechanics source of truth for numbers:** ReviewBible `src/bestiary_data_full.json` combat payload + sheet Armor/HP/Speed (see `docs/mechanics/MONSTER_COMBAT_SCHEMA.md`).  
**Fiction / floors:** Prefer Chronicle gazetteer + combat-trust zone tables when sheet flavor text conflicts.  
**Do not** paste foreign OGL ecology. Write original Aethel prose.

---

## Filename

`entries/<kebab-case-name>.md`  
Example: `spiral-worm.md`

---

## Template

```markdown
# <Creature Name>

**MM grade:** Publication | Expedition-ready | Development cite  
**Book:** MM-01 Monster Manual of the Decennium  
**Slug:** <kebab-case-name>

## Identity (Required)

| Field | Value |
|-------|-------|
| **Name** | |
| **Size** | Tiny / Small / Medium / Large / Huge / Gargantuan |
| **Type** | Aberration, Beast, Celestial, Construct, Dragon, Elemental, Fey, Fiend, Giant, Humanoid, Monstrosity, Ooze, Plant, Undead, … |
| **Alignment** | |
| **Challenge** | <CR> (<XP listed — budget aid only; XP awards may be BLOCKED — see advancement canon>) |
| **Tier band** | T1–T10 or Surface |
| **Floors** | e.g. 1–10 (Yieldheart) — gazetteer-facing |
| **Zone (sheet)** | Excel / JSON `zoneFound` string |
| **Tags** | e.g. harvest-node, patrol, nest-guardian, political-actor, seal-minion |

## Provenance (Required)

| Field | Value |
|-------|-------|
| **JSON / sheet name** | Exact bestiary name if different from display |
| **Combat draft** | true / false |
| **Combat source** | e.g. `t1-5-trusted`, `gate-guardian-trusted`, `band-trusted` |
| **BE-01 / BB-01 cite** | Section or “lexicon A–Z” |
| **Publication notes** | Placeholder? Type/Size corrected in fiction? Honesty flags |

## At a Glance (Required)

2–4 sentences: what the creature *is*, what it *wants*, and why an Expedition meets it (pressure type: attrition / ambush / politics / harvest / seal foreshadow).

## Player-facing rumor (Optional)

What survivors say. Keep Silent Ones / Heartcell secrets out unless Director-only section below is used and clearly labeled.

## Ecology (Required for Full Entry; Optional for Field Brief)

### Habitat & floors
Where it lives; how Yieldheart/Bloomdeep/etc. shape its behavior.

### Social structure / numbers
Solitary, pairs, packs, drone cadres, broker retinues, etc.

### Behavior & goals
What it protects, eats, bargains for, or ignores.

### Signs & omens
Recon tells before initiative.

## Role vs Expedition (Required)

One line each (use `—` if none):

- **Combat:**  
- **Recon:**  
- **Research:**  
- **Resource:**  
- **Support:**  

## Combat block (Required)

*Map to DD companion fields. Prefer JSON `combat` when present.*

**Armor** <armorClass> · **Hit Points** <hitPoints> · **Speed** <speed>

**Defenses**

| | |
|--|--|
| Resistances | <combat.defenses.resistances or None> |
| Immunities | <combat.defenses.immunities or None> |
| Condition immunities | <combat.defenses.conditionImmunities or None> |

**Save DC (creature)** <combat.saveDc or —>

**Senses / languages** (Optional) Tremorsense, darkvision, languages, telepathy — only if sourced or clearly marked provisional.

### Actions (Required)

For each attack / save action:

- **<Name>** — *kind:* attack|save · *cost:* action|bonus|reaction · *usage:* atWill|recharge|limited  
  - Attack bonus / save (ability + DC + onSuccess)  
  - Range / reach / radius  
  - Targets  
  - Damage (dice, average, type) × count  
  - Special text (original)  

### Traits / passives (Optional)

Named traits with mechanical effect in DD terms.

### Seal Pulse / lair pulse (Optional — bosses & seals only)

Terrain or free reaction between turns. **Do not** label as foreign “legendary actions.”

### Tactics (Required for Full Entry)

How the Director should open, pressure roles, and quit conditions (morale / flee / bargain).

## Weave interaction (Optional but recommended)

How Weave casting, Burnout proximity, silence, or Spiral thinness changes the fight. Use DD magic language only.

## Lair & terrain (Optional — recommended for Full Entry)

Room features, hazards, chokepoints, harvestable nodes in the space.

## Harvest & craft hooks (Required for Full Entry; Optional for Field Brief)

| Field | Value |
|-------|-------|
| **Loot tiers (sheet)** | JSON `loot` summary |
| **Primary parts** | Named materials (cite Crafting Bible / Instruments when known) |
| **Harvest difficulty** | Easy / Risky / Forbidden — provisional OK if labeled |
| **Recipe hooks** | Point to recipe ids or “Resource team: …” without inventing locked Matrical craft |
| **Spoil / preservation** | Opening-calendar note if relevant |

## Variants (Optional)

Named variants with delta stats only.

## Director secrets (Optional — clearly labeled)

GM-only. No Silent Ones invention beyond locked DM-01 / continuity docs.

## See also (Required)

- BE-01 / BB-01 pointers  
- Related creatures / Gate foreshadow  
- Encounter toolkit or floor gazetteer refs  

---
**Entry stamp:** YYYY-MM-DD · author/agent · dual-written: yes/no
```

---

## Field map — template ↔ DD data

| Template field | JSON / system |
|----------------|---------------|
| Name, Size, Type, Alignment | `name`, `size`, `type`, `alignment` |
| Challenge, XP | `challengeRating`, `xp` (budget; awards may be blocked) |
| Zone | `zoneFound` |
| Floors / Tier | Chronicle + `T1_5` / `T6_10` combat-trust tables (not raw description text) |
| Armor / HP / Speed | `armorClass`, `hitPoints`, `speed` |
| Defenses | `combat.defenses.*` |
| Save DC | `combat.saveDc` |
| Actions | `combat.attacks[]` (`kind`, `attackBonus`, `save`, `recharge`, `damage[]`, …) |
| Draft / source | `combat.draft`, `combat.source` |
| Harvest | `loot` + Crafting Bible harvest profiles when present |
| Weave | Player Rulebook / companion Weave rules — narrative + optional save interactions |

---

## Grades — minimum required sections

| Grade | Must include |
|-------|--------------|
| **Publication (Full Entry)** | Identity, Provenance, At a Glance, Ecology, Role vs Expedition, Combat + Actions, Tactics, Harvest, See also |
| **Expedition-ready (Field Brief)** | Identity, Provenance, At a Glance, Role vs Expedition, Combat + Actions, See also |
| **Development cite** | Identity, Provenance, one-line At a Glance, pointer to BE-01/JSON only |

---

*Template stamp: 2026-08-04 — Agent 3.*
