# Ashthirst the Hollow

**MM grade:** Publication  
**Book:** MM-01 Monster Manual of the Decennium  
**Slug:** ashthirst-the-hollow

## Identity (Required)

| Field | Value |
|-------|-------|
| **Name** | Ashthirst the Hollow |
| **Size** | Huge |
| **Type** | Elemental |
| **Alignment** | Neutral Evil |
| **Challenge** | 14 (11500 XP listed -- budget aid only; XP awards may be BLOCKED -- see advancement canon) |
| **Tier band** | T3 |
| **Floors** | 21-30 (Anvil of Brogi); Seal: Lavaflow Gate F30 |
| **Zone (sheet)** | Anvil of Brogi |
| **Tags** | Gate Guardian, seal, campaign-threshold |

## Provenance (Required)

| Field | Value |
|-------|-------|
| **JSON / sheet name** | Ashthirst the Hollow |
| **Combat draft** | false |
| **Combat source** | gate-guardian-trusted |
| **BE-01 / BB-01 cite** | BE-01 lexicon A-Z / ecologies; Codex seal notes if Gate Guardian |
| **Publication notes** | Combat draft=false; Lore-pass JSON may list Elemental Type CR 14; Codex lexicon shows authored Ash Claw / Hollow Wail draft. Prefer Codex attack names for fiction; keep JSON AC/HP/Speed/CR when combat.source is trusted -- Director reconciles if both present. |

## At a Glance (Required)

Ashthirst the Hollow is the Tier 3 Gate Guardian -- a hollow of ash and wind that resents anyone who gets to leave the forge. It wants pauses to become deaths. Seal fight: terrain, talk, and necrotic/psychic pressure per Codex staging.

## Player-facing rumor (Optional)

[DRAFT expansion] Survivors speak in half-true nicknames and haven gossip; Directors keep Silent Ones / Heartcell / Level 97 chamber lore out of PC rumors.

## Ecology (Required for Full Entry; Optional for Field Brief)

### Habitat & floors
Canonical: Anvil of Brogi, Lavaflow Gate end of Floor 30 (Chronicle / Codex / Director one-pager). Sheet zone strings that say jungles or "Fields of Whispering Grasses" are **unreconciled leftover flavor** -- do not run them (Codex honesty).

### Social structure / numbers
Unique seal-intelligence. Not a random spawn.

### Behavior & goals
Endure; drink life from hesitation; deceive Support with false comfort.

### Signs & omens
One cold spot in a hot realm; Chained Anvil timing; corridors that resent presence (Rivetworks Maze).

## Role vs Expedition (Required)

- **Combat:** Seal boss -- Ash Claw pressure, Hollow Wail clustering punish.
- **Recon:** Slag key route; Quenching Pool; steam fail states.
- **Research:** Omens vs true forge lore; ignore leftover jungle text.
- **Resource:** Deep loot-as-bait (Aberrant Ichor / Mind Crystal / Reality Shard bands per Codex) -- expect rival Expeditions.
- **Support:** Resist deception; keep party from clustering on "safe" cold tiles.

## Combat block (Required)

*Numbers from ReviewBible `bestiary_data_full.json` unless noted.*

**Armor** 16 * **Hit Points** 464 * **Speed** 40 ft., fly 60 ft. (hover)

**Defenses**

| | |
|--|--|
| Resistances | None listed |
| Immunities | None listed |
| Condition immunities | None listed |

**Save DC (creature)** 18

### Actions (Required)

- **Ash Claw** -- *kind:* attack * *cost:* action * *usage:* atWill
  - Attack bonus +9
  - Targets: 1 creature x action count 2
  - Damage: 3d8+7 (20.5) necrotic
- **Cinder Lash** -- *kind:* attack * *cost:* action * *usage:* atWill
  - Attack bonus +9
  - Targets: 1 creature x action count 1
  - Damage: 2d10+5 (16.0) fire
- **Hollow Wail** -- *kind:* save * *cost:* action * *usage:* recharge
  - Save wisdom DC 18 (onSuccess: half)
  - Recharge: {'minimumRoll': 5, 'dieSides': 6}
  - Targets: 1 creatures-in-area x action count 1
  - Damage: 6d8 (27.0) psychic

### Traits / passives (Optional)

-- (none listed in JSON combat payload)

### Seal Pulse / lair pulse (Optional -- bosses & seals only)

Codex staging: terrain and talk as pressure between turns -- do not label foreign legendary actions.

### Tactics (Required for Full Entry)

Codex: talk before and during -- false comfort/warnings. Ash Claw twin pressure; Hollow Wail when the party clusters away from lava. Hover above molten hazards grounded PCs cannot share. Failed slag key = steam/metal before initiative.

## Weave interaction (Optional but recommended)

Forge heat and Weave fatigue stack; silence is worse than noise here -- Ashthirst *is* the quiet.

## Lair & terrain (Optional -- recommended for Full Entry)

Lavaflow Gate chamber: the cold hollow over molten floor. Flying/hover lets it ignore lava tiles. Key: cooled slag quenched in Brogi's Quenching Pool.

## Harvest & craft hooks (Required for Full Entry; Optional for Field Brief)

| Field | Value |
|-------|-------|
| **Loot tiers (sheet)** | tier1: Strange Tentacle (Tier 1) (0.99 / val 22); tier2: Aberrant Ichor (Tier 2) (0.83 / val 44); tier3: Mind Crystal (Tier 3) (0.66 / val 88); tier4: Reality Shard (Tier 4) (0.5 / val 176) |
| **Primary parts** | See loot drops; cross-check Crafting Bible / Instruments before locking recipes |
| **Harvest difficulty** | Seal loot is bait -- Codex: unusually deep for T3; rival Expeditions and brokers contest before surface markets. Expedition charter max 12; coalitions use coalition rules. |
| **Recipe hooks** | Resource team: log Opening-day and floor of harvest; avoid inventing locked Matrical crafts |
| **Spoil / preservation** | Opening-calendar sensitive where noted in ecology |

## Variants (Optional)

--

## Director secrets (Optional -- clearly labeled)

Gate Guardians are Heartcell public-face seal myth (BE-01). Do not lecture Silent Ones / Old Ones authorship at the table. Level 97 hidden chamber is unrelated content -- do not merge.

## See also (Required)

- Codex_of_the_Heartcell.md -- Gate Seal III
- Chronicle_of_the_Decennial_Opening.md -- Tier 3
- HOW_TO_RUN_FLOOR_1_100_DIRECTOR_ONE_PAGER.md tier ladder
- T1_5 encounter toolkit -- Ashthirst card
- Related foreshadow: Corrosion Grazer, forge mephits (toolkit), Hollowforged echo themes

---
**Entry stamp:** 2026-08-04 * Agent 5 (Tranche B) * dual-written: yes
