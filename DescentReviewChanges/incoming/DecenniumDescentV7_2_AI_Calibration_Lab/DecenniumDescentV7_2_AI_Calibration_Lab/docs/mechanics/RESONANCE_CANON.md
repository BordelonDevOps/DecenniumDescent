# Resonance — canon spellcasting economy (Hybrid-B)

**Status:** Canon. Owner-decided 2026-07-29 (see [`RESONANCE_MODELS.md`](./RESONANCE_MODELS.md) §6 for the full ruling and rationale).
**System name:** **Resonance** / **Resonance Points (RP)**. "Hybrid-B" is the internal build label for this ruling, not player-facing product copy — do not print "Hybrid-B" or "Song of the Weave" on character sheets or in player-facing UI. "Hybrid-B canon" is fine as an internal/collaborator subtitle (docs, code comments, draft badges).
**Helpers:** [`src/data/resonance-economy.js`](../../src/data/resonance-economy.js) — pool tables, `spellCost()`, `computeSpellCost()`, `retuneAmount()`, `fullRestore()`, reputation modifiers, overcast/Burnout helpers.
**Oracle:** excluded — see [§6](#6-oracle-exception).

---

## 1. What it is (flavor)

Every Weave caster carries an echo of the **First Song** — the primordial act of resonance that broke the Great Stillness. Casting a spell means sounding a thread of that Song back through the **Weave**, and how cleanly it rings depends on who you are: your training, your alignment, and how the **Choir**, guilds, temples, and circles of Aethel regard you.

**Resonance Points (RP)** measure how strongly and how often a caster can sound that Song before the note frays. This is **one pool**, not a rack of Vancian slots — a mana bar with musical stakes, not a spellbook with a new coat of paint.

## 2. Pool size

RP maximum is set by class and level. Rulebook-complete L1–20 tables exist for **Wizard, Mage, Cleric, and Druid** (`rulebook_output.txt:6077–6099`).

Every other Weave-casting class (Bard, Paladin, Ranger, Shaman, Mirrorsage, Crimson Agent, Dragoon, Monk, Thief, Tinker) uses **draft** L1–20 tables in `resonance-economy.js` (`DRAFT_POOL_TABLES`), derived from the Cleric curve × tier multiplier — flagged `(draft)` in UI pending author review.

**Arcane Guilds** reputation modifies max RP (±1 at liked/disliked, ±2 at honored/hated extremes). Wired in Builder, Sheet, and SessionTracker via `resolveMaxRp()`.

Oracle has **no RP pool** — see [§6](#6-oracle-exception).

## 3. Spend (casting a spell)

```
Cost = (spell level × 2)
     − 1  if the school is "in key" with your alignment (affinity)
     + 1  if the school is "dissonant" against your alignment (opposition)
     ± reputation modifier (−1 to +1, class-relevant Resonance track)
     − specialization discount (0 to −3, subclass-dependent — not wired yet)
```

Cantrips always cost 0 RP. Final cost floors at 0.

**Shipped:** `computeSpellCost()` applies affinity/opposition from alignment + class-relevant track spell-cost modifier. Builder spell list and Sheet prepared list show RP cost previews.

**Draft:** `CLASS_SPELL_REP_TRACK` mapping (which of the 4 Resonance tracks applies per class) — reasonable Director defaults, author review pending.

## 4. Recovery

| Rest type | Recovery | Helper | UI |
|---|---|---|---|
| **Short rest** ("retune") | ≈¼ max pool (+ casting-attribute modifier + Nature Circles rep bonus) | `retuneAmount()` | SessionTracker **Retune** button per combatant |
| **Long rest** ("full harmony") | Full pool | `fullRestore()` | SessionTracker **Full** button; max-RP click also restores |
| **Meditation** (optional, 10 min, 1/day) | Casting-attribute modifier only | `meditationRecovery()` | Not wired |

**Nature Circles** reputation: ±1 RP on retune (liked/honored +1, disliked/hated −1). Wired via `retuneRepBonus()`.

## 5. Overcast & Burnout

Casters can push a **louder, more dissonant surge** through the Weave — the overcast menu (Empowered, Extended, Widened, Heightened, Quickened, Subtle, Distant, Twinned) from Model B. Overcasting risks **Resonance Burnout** if the pool drops below 25% of max.

**Shipped (Phase 2 stub):**
- `OVERCAST_OPTIONS`, `overcastRpCost()`, `totalCastCost()`, `burnoutThreshold()`, `isBurnoutRisk()` in `resonance-economy.js`
- SessionTracker overcast toggle row per Weave combatant; **Apply overcast spend** deducts surcharge and sets **Burnout** badge when below threshold
- Manual base spell cost still required at table (no spell picker in tracker yet)

**Still draft / not built:**
- Full overcast panel tied to a selected spell's base cost in SessionTracker
- Burnout mechanical consequences beyond the warning badge
- Specialization discount (subclass −0..−3) in cost preview

## 5.5 Reputation hooks

**Shipped:**

| Track | Max RP | Spell cost | Retune |
|---|---|---|---|
| **Arcane Guilds** | ±1..±2 via `maxRpRepModifier()` | — (Mage/Wizard/Tinker/Crimson Agent track) | — |
| **Religious Orders** | — | ±1 via `spellCostRepModifier()` | — |
| **Academic Factions** | — | ±1 (Bard/Mirrorsage/Thief track) | — |
| **Nature Circles** | — | ±1 (Druid/Ranger track) | ±1 via `retuneRepBonus()` |

Reputation scores flow from character save → Builder/Sheet max RP and spell previews → SessionTracker when pulling a saved character.

**Not wired:** Academic Factions spell-learning discounts (Ch9 prose); Religious Orders divine spell failure chance; urban-prep restriction for low Nature standing.

## 6. Oracle exception

Oracle does **not** use Resonance Points. Oracle spends **Revelation Charges** (start 3, max 7) on Mystery Revelations, recovered via each Mystery's unique **Prophecy Trigger** — not rest-based. This is unchanged by the Hybrid-B ruling. Ch9's rulebook "Fate Weaving" Oracle paragraph is **non-canon** — disregard it; Oracle's canon design lives in the Oracle chapter (`rulebook_output.txt:2189–2340`) and is already implemented as-is.

## 7. Multiclass (approved canon — implemented)

**Director ruling (Hybrid-B, Resonance; approved 2026-07-30):** When a hero has two or more Weave-casting classes, max RP = **full pool of the highest caster-tier class** (by level in that class), **plus 25% of the secondary caster's max pool** (round up). Tertiary+ Weave classes do not add further RP in this implementation.

**Example:** Wizard 10 / Cleric 6 at L16 → Wizard L10 pool (canon table) + ⌈25% × Cleric L6 pool⌉. Reputation modifiers apply once to the merged total via Arcane Guilds.

**Implemented in code** — `defaultMaxRp()` / `resolveMaxRp()` accept optional `secondaryClass` + `secondaryLevel`, or `classLevels: { Wizard: 10, Cleric: 6 }` on a character save. Helpers: `parseMulticlassLevels()`, `mergeMulticlassMaxRp()` in `resonance-economy.js`. Single-class path unchanged when multiclass fields absent. **Character Builder** exposes optional secondary class + level dropdowns (Origin → Class); manual JSON still supported — see `CHARGEN_PROGRESSION.md`.

---

## Shipped vs still draft (2026-07-29 overnight pass)

### Shipped

- Full L1–20 pool tables: canon (Wizard/Mage/Cleric/Druid) + draft (`DRAFT_POOL_TABLES` for 10 remaining Weave casters)
- `spellCost()`, `computeSpellCost()`, `retuneAmount()`, `fullRestore()`, reputation modifiers, overcast/Burnout math
- CharacterBuilder: max RP with reputation; RP cost badge on spell cards; optional multiclass secondary class + level dropdowns
- CharacterSheet: max RP with reputation; prepared spells show RP cost
- SessionTracker: Retune / Full restore; overcast picker stub; Burnout badge; reputation-aware max RP; multiclass-aware max RP when save has `secondaryClass` / `classLevels`

### Still draft / Phase 2+

- Draft pool numbers for 10 non-canon-table classes (author review)
- No multiclass formula draft remains: the Hybrid-B merge rule in §7 is approved canon. A merged result still carries a draft marker when either contributing class uses a draft pool table.
- `CLASS_SPELL_REP_TRACK` per-class → faction mapping
- Meditation recovery UI
- Full overcast panel with spell-linked base cost
- Burnout mechanical effects (SessionTracker shows draft disadvantage / −1 action stub only)
- Subclass specialization discount in cost preview
- Academic spell-learning discounts; Religious failure chance; Nature urban-prep restriction

---

## Related docs

- [`RESONANCE_MODELS.md`](./RESONANCE_MODELS.md) — full Model A vs B comparison + Director ruling.
- [`REPUTATION.md`](./REPUTATION.md) — faction tracks that feed RP modifiers.
- [`../MECHANICS_BIBLE_STUB.md`](../MECHANICS_BIBLE_STUB.md) §2 — updated resolution status.
- [`../MECHANICS_ROADMAP.md`](../MECHANICS_ROADMAP.md) — Phase 1 Lane A work package.
- [`../../src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md) — approved terminology.
