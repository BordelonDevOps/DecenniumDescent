# Spiral Worm

**MM grade:** Expedition-ready (example upgrade toward Publication)  
**Book:** MM-01 Monster Manual of the Decennium  
**Slug:** spiral-worm

> **Example entry only.** Prose is original MM-pack authorship. Combat numbers and identity pulled from ReviewBible `bestiary_data_full.json` (`combat.source: t1-5-trusted`). Codex BB-01 still flags a STUB honesty box on older generated ecology — this entry is the compilation-path rewrite, not a silent BE-01/BB-01 overwrite.

## Identity (Required)

| Field | Value |
|-------|-------|
| **Name** | Spiral Worm |
| **Size** | Large |
| **Type** | Aberration |
| **Alignment** | Chaotic Neutral |
| **Challenge** | 2 (450 XP listed — encounter-budget aid only; do not treat as a locked XP award) |
| **Tier band** | T1 |
| **Floors** | 1–10 (Yieldheart Caverns), especially crystal-veined side tunnels and abandoned stoneworks |
| **Zone (sheet)** | Yieldheart Caverns |
| **Tags** | nest-guardian, harvest-node, recon-hazard |

## Provenance (Required)

| Field | Value |
|-------|-------|
| **JSON / sheet name** | Spiral Worm |
| **Combat draft** | false |
| **Combat source** | `t1-5-trusted` |
| **BE-01 / BB-01 cite** | BE-01 lexicon; BB-01 Aberration family / Yieldheart listings (STUB ecology in Codex — superseded *for MM pack purposes* by this entry) |
| **Publication notes** | Trusted T1 combat shell. Attack name *Void Rend* is type-flavored trust-pass text — keep or renarrative freely. Loot tiers are sheet defaults; harvest flavor below is provisional pending Crafting Bible harvest-profile ingest. |

## At a Glance (Required)

Where Yieldheart’s crystal veins kink hardest, the Spiral Worm nests in the kink. It is not a predator so much as a length of wrong geometry that learned to bite: a pale, segmented bulk whose body never quite agrees with itself about which direction is “forward.” Expeditions meet it when they cut corners through glowing mineral seams, or when Resource teams chase tremor-cores into tunnels the Automatons stopped mapping.

## Player-facing rumor (Optional)

Crystalfront porters swear the worms “eat distance” — that a corridor behind you is shorter than the one ahead, and that shouting your own name near a nest makes the stone answer twice. Directors may treat the double-echo as a free Recon tell, not a separate monster.

## Ecology (Required)

### Habitat & floors
Spiral Worms favor Yieldheart’s luminescent mineral seams and the collapsed dwarf cuttings near the Abandoned Stoneworks. They avoid Automaton main routes; the machines reroute around worm-kinks the same way they stop short of Vaskor’s threshold. Floor 3–7 side galleries are the most common encounter band; Floor 1 market approaches almost never host nests unless a Cycle has cracked a new vein.

### Social structure / numbers
Usually solitary. A “nest” is one worm plus 1–2 discarded mineral casts (harmless terrain clutter that looks like eggs to panicked porters). Two worms in one gallery means the seam is freshly torn — treat as a warning that Spiral thinness is local, not as a pack hunter culture.

### Behavior & goals
The worm feeds on vibration and mineral stress, not meat first. Footfalls, hammering, and Weave cantrips that snap loudly will draw it before blood scent does. It coils to guard the kink that birthed it; kill the worm and the kink often settles within hours — which is why Research teams pay for live observations and Resource teams pay for the cooling core-grit left behind.

### Signs & omens
- Mineral glow that *pulses* out of sync with torch flicker  
- Double foot-echoes in a straight tunnel  
- Fine crystal dust arranged in a shallow helix on the floor  
- Automaton patrol chalk: a single spiral scratched beside a sealed side-mouth

## Role vs Expedition (Required)

- **Combat:** Attrition ambusher — punish tight formations in narrow seams; force the party to choose push vs backtrack.  
- **Recon:** Primary counterplay is route choice; spotting helix dust early avoids the fight.  
- **Research:** Behavior notes on vibration-hunger and seam-settling after death are valuable Cycle data.  
- **Resource:** Cooling core-grit and cast crystal are harvest targets; noisy extraction risks a second kink opening.  
- **Support:** Expect psychic shock on the opener; keep healers off the glowing centerline where Void Rend lines up cleanest.

## Combat block (Required)

**Armor** 13 · **Hit Points** 68 · **Speed** 40 ft.

**Defenses**

| | |
|--|--|
| Resistances | None listed |
| Immunities | None listed |
| Condition immunities | None listed |

**Save DC (creature)** —

**Senses / languages** (provisional) Tremorsense 30 ft. while in contact with stone or crystal; no language. *Provisional sense — not in JSON combat object; label at table.*

### Actions (Required)

- **Void Rend** — *kind:* attack · *cost:* action · *usage:* atWill  
  - +5 to hit · reach 10 ft. · one creature  
  - 1d10+2 psychic (avg 7.5)  
  - The wound feels like a skipped step: on a hit, the target’s next move that turn counts 5 ft. of difficult geometry along crystal seams (Director fiat terrain — narrative pressure, not a second damage rider).

### Traits / passives (Optional)

- **Seam-Coil.** In a tunnel 10 ft. wide or less, the Spiral Worm ignores the first opportunity attack each round as its body occupies “two places” along the kink.  
- **Vibration Hunger.** Loud tools, collapsed ceilings, or explosive Weave effects within 60 ft. draw the worm toward the noise on its next turn if it is not already engaged.

### Tactics (Required)

Open from a side seam or ceiling kink — never from the lit centerline the party expects. Use Void Rend on the lead scout or on a caster mid-cantrip. If the party freezes to heal in place, coil past them toward the noisiest Support ritual. The worm does not negotiate and rarely flees; if reduced below a quarter of its hit points and the seam is broken (pitons, mining charges, successful Research “settle the kink” check), it thrashes once and tries to withdraw into stone rather than fight to annihilation.

## Weave interaction (Optional)

Cantrips and low-pool Weave effects that create sharp sound or bright geometric light agitate the nest. Silent, careful casting is safer than flashy opener spells. Directors may impose disadvantage on the worm’s next attack if the party spends a round damping vibration (blanket lines, soft footwraps, Stabilizing craft tools) — a Support/Resource teamwork beat, not a free stun.

## Lair & terrain (Optional)

A typical lair is a dogleg gallery where crystal veins braid into a helix. Difficult terrain along the braid; one false floor of cast crystal that drops into a 10-ft. chute (bludgeoning + noise). Light sources flicker on the braid even when oil is fresh.

## Harvest & craft hooks (Required)

| Field | Value |
|-------|-------|
| **Loot tiers (sheet)** | Tier 1: Elemental Core (Tier 1), rate 0.54, value 12 · Tier 2: Pure Element (Tier 2), rate 0.45, value 24 |
| **Primary parts** | Cooling core-grit; spiral cast-crystal; (provisional) seam-oil from the kink |
| **Harvest difficulty** | Risky — noisy extraction can reopen a lesser kink (wandering hazard, not a second full CR 2 unless you want it) |
| **Recipe hooks** | Resource teams: elemental/core crafting at Crystalfront and early Anvil brokers; cite Instruments / Crafting Bible when mapping exact recipes — do not invent locked Matrical processes |
| **Spoil / preservation** | Core-grit cools within ~4 Opening hours; after that it is dull mineral (flavor only unless a recipe says otherwise) |

## Variants (Optional)

- **Seam-Hatchling (Field Brief candidate).** Medium, half HP, CR 1 budget — same Void Rend at −1 to hit. Use as foreshadow before a full nest.  
- **Gate-shadowed Worm.** Near Floor 10 approaches to Vaskor, worms grow sluggish and stone-dark; Directors may swap psychic damage for bludgeoning without changing numbers — foreshadow the Stone Maw without stealing the seal.

## Director secrets (Optional)

Automatons do not “fear” Spiral Worms; they treat worm-kinks as map errors. An Expedition carrying Automaton chalk-spirals can sometimes bribe a sentinel for a bypass route — political color for early floors, not a combat bypass for Vaskor.

## See also (Required)

- BE-01 / companion JSON: **Spiral Worm**  
- BB-01: Aberration ecology primer; Yieldheart Gate Seal I (Vaskor) for upstream foreshadow  
- Related: Spiral Breach family (higher floors); crystal harvest nodes in Yieldheart gazetteer  
- Trust stamp: `docs/mechanics/T1_5_BESTIARY_COMBAT_2026-07-31.md`

---
**Entry stamp:** 2026-08-04 · Agent 3 (Book Architecture) · dual-written: yes
