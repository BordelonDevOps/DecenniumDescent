# Decennium Descent — Mechanics Bible

**Purpose:** compact current-system reference. The Player Rulebook remains authoritative for player rules; the Director's Crucible and `docs/canon/` own deeper setting truth.

## 1. Core Resolution

Decennium Descent uses **d20 + modifier vs target number** for attacks, ability checks, and saving throws. Advantage/disadvantage modifies the roll where a feature or situation grants it.

## 2. Character Progression

- **17 selectable base classes** — `src/data/canon-classes.js`
- **Arch specialization:** begins at level 3 for the primary class framework
- **Hero Path:** begins at level 10
- Hero Paths describe **philosophy, method, and consequence**, not an objective Good/Neutral/Evil rating.
- Character advancement runs to level 20; the setting treats levels above ordinary adventuring play as increasingly legendary and metaphysically significant.

### Class-specific resources

Different classes should feel mechanically distinct:

- Bard — **Crescendo**
- Cleric — **Conviction**
- Crimson Agent — **Blood Gauge / Blood Marks**
- Dragoon — **Momentum**
- Oracle — **Revelation Charges**
- Druid — **Shapeshifting uses/forms**
- Paladin — oath features and class pools
- Weave casters — **Resonance Points** where their class uses the general magic economy

## 3. Resonance

The current generic Weave economy is a **flat Resonance Point pool**, not a multiclass spell-slot table.

Canonical reference: `docs/mechanics/RESONANCE_CANON.md`.

Core principles:

- cantrips cost 0 RP;
- leveled magic consumes RP based on spell level and modifiers defined by the Resonance rules;
- class, specialization, affinity, reputation, and overcasting can alter cost or recovery where the rules specify;
- short rests restore a limited amount; long rests restore the full pool;
- pushing a pool too low can create Burnout risk;
- multiclass Weave casters use the merged-pool rule in `RESONANCE_CANON.md` rather than stacking full caster pools;
- Oracle never converts Revelation Charges into RP.

Historical slot-like drafts are design history only and are not the current rules target.

## 4. Combat and Session Loop

- Initiative: d20 + Dexterity modifier unless a feature changes it.
- Combat uses actions, movement, reactions, positioning, conditions, terrain, and class-resource timing.
- Expedition play is larger than combat: reconnaissance, research, resource acquisition, support, downtime, camps, reputation, and the Opening clock all create pressure.
- The Director should treat encounter consequences as persistent when the fiction supports it.

## 5. The Opening Clock

- Opening: **2,400 hours / 100 days**
- Horn / point of no return: **1,200 hours / day 50**
- A Floor-50 morale/withdrawal opportunity is not the Horn.
- Time is a design pressure, not only bookkeeping; it converts deferred options into costly choices.

Reference: `docs/mechanics/DESCENT_WINDOW_CANON.md`.

## 6. Expeditions

Player-facing expedition structure permits up to **12 characters** in an expedition, divided among functional teams such as Combat, Reconnaissance, Research, Resource, and Support. Large simulations must be labeled as coalitions or multiple expeditions rather than silently redefining RAW expedition size.

Reference: `docs/mechanics/EXPEDITION_STRUCTURE_CANON.md`.

## 7. Dungeon Structure

| Tier | Floors | Zone | Gate Guardian |
|---|---:|---|---|
| 1 | 1–10 | Yieldheart Caverns | Vaskor, the Stone Maw |
| 2 | 11–20 | Bloomdeep Marsh | The Bloom That Hungers |
| 3 | 21–30 | Anvil of Brogi | Ashthirst the Hollow |
| 4 | 31–40 | Isles of Eternal Radiance | Gor Vekk, Architect of Ends |
| 5 | 41–50 | Sanctum of Echoing Choirs | Choralith, Voice Below |
| 6 | 51–60 | Crossroads of the Shattered Thread | Lumen of the Shattered Thread |
| 7 | 61–70 | Pactbound Arena | Xarog, the Pactbound Furnace |
| 8 | 71–80 | Duskshard Pools | Eirfax, the Dusk Crowned |
| 9 | 81–90 | Veiled Iron Spiral | Threxus, the Iron Spiral |
| 10 | 91–100 | Silencebound Void | The Marquis of Silence |

The Level-97 Old God remains a protected unresolved lore point: do not invent a relationship to the Silent Ones/Heartcell until that owner question is explicitly settled.

## 8. Prestige

Prestige advancement is **discovery-driven**. Requirements can include level, class, feat, skill, reputation, action, location, ritual, NPC, or narrative accomplishment. Prestige should feel earned through the world rather than appearing only as a menu unlock.

## 9. Reputation

Faction reputation affects social access, information, logistics, prices, support, hostility, and—where Resonance rules specify—magic. Reputation should record consequences of choices rather than function as a universal morality score.

Reference: `docs/mechanics/REPUTATION.md`.

## 10. Matrix Design Test

The Director-facing thematic grammar is:

**Possibility → Choice → Difference → Conflict → Motion → Time → History → Memory → Identity → Will → Life**

This is not a player-facing eleven-room checklist. It is an authoring test: major content should create meaningful alternatives, force commitment, change something, and leave consequences someone remembers.

Reference: `docs/canon/THEMATIC_DESIGN_LANGUAGE.md`.

## 11. Data Sources

- Player rules: `decennium descent player rulebook.docx` / `rulebook_output.txt`
- Director rules: `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx`
- Bestiary source: `Bestiary.xlsx`
- Bestiary metadata source: `bestiary_metadata_source.xlsx`
- Crafting source: `decennium_descent_crafting_recipes_validated.xlsx`
- Companion implementation: `src/`

See `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` before resolving contradictions.
