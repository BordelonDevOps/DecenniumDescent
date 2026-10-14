# Decennium Descent — Mechanics Bible (Stub)

**Status:** Short design reference, not a full bible. Cites existing companion modules for detail; flags TBD where the rulebook itself is unresolved or unimplemented. Expand this doc as systems mature — don't let it drift out of sync with `src/data/`.

**Escalation reminder:** anything marked **TBD / ASK OWNER** here is a genuine open question, tracked in `docs/MECHANICS_ROADMAP.md` Director Status. Don't resolve it by editing this doc unilaterally.

---

## 1. Core resolution

**d20 + modifier vs DC**, for ability checks, saving throws, and attack rolls. (`rulebook_output.txt:5682`)

> "The three main rolls of Decennium Descent... rely on these six ability scores. The basic rule... roll a d20, add an ability modifier... and compare the total to a target number."

This is the universal resolution mechanic underneath every other system below. Standard advantage/disadvantage exists (`rulebook_output.txt:4874` etc., e.g. wearing armor without proficiency). No deviation from this layer has been found — it's stable and needs no owner input.

---

## 2. Resonance economy (dice / charges / RP) — **RESOLVED: canon is Hybrid-B ("Resonance")**

**Director Status #1 is closed.** Owner-delegated ruling, 2026-07-29: canon spellcasting economy is **Hybrid-B**, anchored on Model B below as the mechanical spine, with musical/Choir/First Song flavor and Model A's simplicity concessions layered on top. **System name is `Resonance` / `Resonance Points (RP)`** — not "Song of the Weave," which was rejected as the product-facing name (internal label for the ruling is "Hybrid-B," fine in docs/code comments only). See [`docs/mechanics/RESONANCE_MODELS.md`](mechanics/RESONANCE_MODELS.md) (full ruling + rationale) and [`docs/mechanics/RESONANCE_CANON.md`](mechanics/RESONANCE_CANON.md) (short playable summary). Helpers implemented in `src/data/resonance-economy.js` (`spellCost()`, `defaultMaxRp()`); overcast panel UI is **Phase 2** (stub only).

Decennium Descent replaces D&D-style daily spell slots with a **Resonance Points (RP)** economy. The rulebook text originally contained two different, non-reconciled versions of this system, both cited below for historical reference — **Model B is now canon** (with Model A contributing only pool-table convention and UI-simplicity framing, not its slot mechanic).

### Model A — "per-class RP-as-slots" (Ch3 class text, e.g. Druid)

Source: `rulebook_output.txt:1422-1509` (Druid section, structurally identical pattern likely repeated for other full casters).

- RP pool size is a fixed number per class/level (an explicit "Druid table" referenced but not reproduced in the extract at this location).
- **Cost:** casting a spell costs RP equal to the spell's level (i.e. functionally identical to 5e spell slots, just renamed).
- **Recovery:** full pool on long rest; partial recovery (points totaling ≤ half your level, none 6th+) on short rest via meditation.
- Worked example given: "if you are a 3rd-level druid, you have 6 Resonance Points."

### Model B — "points-buy pool" (dedicated "The Resonance System" chapter)

Source: `rulebook_output.txt:6069-6158`.

- RP pool determined by class/level, primary casting attribute, **alignment**, and **reputation** — with an explicit table (Wizard/Mage/Cleric/Druid, levels 1–20) showing much larger pools than Model A (e.g. 3rd-level Druid = **7** RP here vs **6** in Model A's own worked example).
- **Cost:** Base Cost = Spell Level × 2, modified by school affinity (-1 RP if aligned, +1 if opposed), reputation (-1 to +1), and class specialization (-1 to -3). Cantrips = 0 RP.
- **Recovery:** Short rest = 1/4 max pool + casting-stat modifier; long rest = full; meditation (10 min, 1/day) = casting-stat modifier. Alignment/location bonuses (+2 RP/rest) apply.
- **Overcasting menu:** Empowered (+2 RP, +50% dmg/healing), Extended (+1 RP, double duration), Widened (+3 RP, double area), Heightened (+4 RP, +1 effective level), Quickened (+3 RP, bonus action), Subtle (+1 RP, no V/S), Distant (+1 RP, double range), Twinned (+3 RP, second target). Burnout risk below 25% pool.
- Full alignment-affinity and reputation-tier tables exist (Good/Neutral/Evil × 8 schools; Academic/Religious/Arcane/Nature faction tiers).

### What's actually implemented today

`src/lib/character-storage.js` still stores a flat, player-editable `resonancePoints` number (default 3) — that field is unchanged. What's new: `src/data/resonance-economy.js` exports canon Model B pool tables (Wizard/Mage/Cleric/Druid, rulebook-complete) plus draft tier-scaled pools for the other Weave casters, and a `spellCost()` implementing the Base Cost/affinity/opposition/reputation/specialization formula. `CharacterBuilder.tsx`, `CharacterSheet.tsx`, and `SessionTracker.tsx` now display this computed max RP next to the manual counter (with a "(draft)" flag for non-canon classes) and a "sync to max" action — the manual counter itself is not forcibly overwritten. **Not yet built:** live overcast/Burnout panel, and reputation→RP modifiers are documented but not auto-applied (see `REPUTATION.md`).

**Resolved:** Hybrid-B ("Resonance") is canon. See `MECHANICS_ROADMAP.md` Director Status #1 (resolved) and `docs/mechanics/RESONANCE_CANON.md`.

### Class-specific charge systems (not RP, and not in conflict)

Some classes use their own resource layered on top of / instead of RP, and these are **not** part of the contradiction above:

- **Oracle — Revelation Charges** (not spell slots): starts at 3, max 7 (`class-details.js` Oracle L1; confirmed correct per Continuity pass, replacing earlier "spell slot" language). Distinct currency from RP; Oracle is excluded from `isSpellcasterClass()` in `spell-utils.js` for this reason.
- **Bard — Crescendo die**: stacks 1 per ability used in rhythm without interruption, max 5, consumed for bonus effects at max stack (`rulebook_output.txt:957`, `class-paths.js` Bard arch/hero trees). A tempo/rhythm resource, not RP.
- **Paladin — Divine Smite / Lay on Hands**: pool-based (Lay on Hands has a healing pool by level) rather than RP-metered; Sacred Oath (10 options, see §4) gates signature powers.
- **Druid — Wild Shape**: uses/CR-gated by level, tracked in Builder but not yet in Session combat tracker (roadmap Phase 3 gap).

These class-specific resources are stable and can be built on now. The **generic RP economy** is resolved (Hybrid-B/"Resonance," §2); remaining work (reputation modifiers, overcast panel, multiclass formula) is Phase 2, not a blocked decision.

---

## 3. Session / horn clock

- **Horn Clock:** Opening **2400 h / 100 days**; Horn PoNR at **1200 h / day 50** ([`DESCENT_WINDOW_CANON.md`](./mechanics/DESCENT_WINDOW_CANON.md)). Soft quit at Floor 50 Canticle ≠ Horn PoNR. Wired in `SessionTracker.tsx` (`HORN_AT = 1200`) and `hornRule` JSON. Elapsed-hours UI only — **TBD** whether "trapped 10 years" gets an in-session consequence table or stays GM fiat.
- **Initiative:** standard d20 + Dex modifier (`SessionTracker.tsx: rollInitiative`).
- **Expeditions:** up to 12 characters split across Combat (4–6), Reconnaissance (1–3), Research (1–3), Resource (2–4), Support (1–3) teams, across morning/afternoon/evening time periods (`dungeon-mechanics.json.expedition`). Not fully wired into Session UI yet (roadmap Phase 3/4 boundary — Lane A for the tracker, Lane C for narrative content).
- **Reputation:** rulebook Ch4 defines faction standing (Liked/Disliked/Hated) that also feeds Resonance's regen/max-RP bonuses (§2, now canon). A live faction tracker exists (`ReputationPanel.tsx`, `reputation.js`); wiring those scores into RP math is the next Phase 1 Lane A step, not yet done.

---

## 4. Class frameworks

- **17 canon classes**, source of truth `src/data/canon-classes.js`. See `COLLABORATOR_ONBOARDING.md` §4 for the full roster and the Fighter/Swashbuckler archive rule.
- **Per-class kit:** armor/weapon/tool/skill proficiencies + level-by-level features in `class-details.js`.
- **Arch paths (L3–9) and Hero paths (L10+):** subclass-equivalent skill trees in `class-paths.js`, one arch path + typically 2–3 alignment-flavored hero paths per class (e.g. Bard: Virtuoso arch path → Harmony/Virtuoso/Discord hero paths).
- **L11–20 capstone tier:** `class-draft-levels.js` — largely `draft: true` pending author review against rulebook tables (roadmap Phase 2).
- **Subclass-equivalent special systems** (deeper than a normal arch/hero tree):
  - **Oracle:** Mystery (10, chosen L1) + Curse (10, chosen L1) + Revelation Charges, tiered revelations at L3/6/9/12/15/18/20 (`oracle-mysteries.js`, `oracle-curses.js`, `class-details.js` Oracle levels).
  - **Paladin:** Sacred Oath (10, chosen L3) gating a Signature Power at L11 and a Final Oath Gift at L20 (`paladin-oaths.js`).
  - **Druid:** Circle (7, chosen L2) gating Wild Shape forms, with Arch Druid Forms unlocking L11+ (`druid-shapeshifting.js`, `class-paths.js`).

---

## 5. Prestige classes

18 prestige paths in `prestige-lorebook.json`, each with: base-class prerequisite (usually "Class X or Y, Lv 10+"), feat/skill/alignment requirements, a narrative unlock trigger (discovery-based, not just level-gated), 3–5 hallmark abilities, and a capstone. Example: Battlemage (Warrior/Mage L10+, unlocked by killing a caster in melee while concentrating).

- All prestige feat requirements cross-checked against `feats.js` — **0 missing** (Continuity pass, 2026-07-29).
- Unlock model is consistently **narrative discovery**, not a checkbox — per `dungeon-mechanics.json.prestigeUnlock`: "Narrative discovery via location, NPC, ritual, or thematic quest chain." This is a deliberate design pattern worth preserving in any new prestige content: prestige should never be purely mechanical (hit level X, click button).
- Docx spot-check (`Decennium_Prestige_Classes.docx` vs live `prestige-lorebook.json`) is still open, low priority (roadmap Phase 2).

---

## 6. Dungeon tiers

10 tiers, each spanning 10 floors (1–100 total), each with a named **gate boss**, **zone**, and floor range (`dungeon-mechanics.json.gateBosses`, cross-validated against `floor-encounters.json` and cosmology — 0 mismatches per Continuity pass).

| Tier | Floors | Zone | Gate Boss |
|------|--------|------|-----------|
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

Floor 97 holds the imprisoned "Old God" (eleventh, unclaimed shard) per cosmology myth-history — a fixed narrative anchor, not adjustable without a Continuity-level lore change.

**Cycle:** 400-day year (10 months × 40 days, Holyday on the 10th of each month, final 10 days = Twilight Week), 10-year rotation, Shardspire activates in year 10, Cycles named after their victor. `entryClasses` and `victoryConsequences` are **Director draft-filled** in `dungeon-mechanics.json` (all 17 CANON_CLASSES eligible; tier-themed consequences; both `draft: true`) — re-open only if rulebook Ch XII specifies class restrictions.

---

## 7. Open TBDs summary (for quick reference)

| # | TBD | Type | Where tracked |
|---|-----|------|----------------|
| 1 | ~~Resonance economy Model A vs B vs hybrid~~ | **RESOLVED: Hybrid-B ("Resonance"), 2026-07-29** | Roadmap Director Status #1; `docs/mechanics/RESONANCE_CANON.md` |
| 2 | ~~17 vs "eighteen" class roster~~ | **RESOLVED (owner 2026-07-29):** v1 ships 17 per Classes Table; "eighteen" is book typo. | Roadmap Director Status #2 |
| 3 | ~~Bestiary D&D-setting leakage (IP risk)~~ | **RESOLVED (owner 2026-07-29):** 54 entries scrubbed; player race **Umbrin** aligned (Umbral Elf interim superseded). See `BESTIARY_SCRUB_LOG.md`, `UMBRIN_LORE.md`. | Roadmap Director Status #3 |
| 4 | Reputation system build priority | **ASK OWNER** | Roadmap Director Status #4 |
| 5 | Collaborator write-access model | **RESOLVED: Director OK gate** (owner ruling #6) | `COLLABORATOR_ONBOARDING.md` §2; Roadmap Director Status #5 |
| 6 | Horn Clock overrun penalty (mechanical vs GM fiat) | Design (Lane A), not owner-blocking | This doc §3 |
| 7 | ~~Cycle `entryClasses` source text~~ | **RESOLVED (Director draft 2026-07-29):** 17 CANON_CLASSES eligible; `victoryConsequences.byTier` draft-filled. Re-open if rulebook Ch XII restricts. | `dungeon-mechanics.json`; OVERNIGHT_VAGUE_QUEUE VQ-07 |
| 8 | 9/10 Oracle mysteries, 9/10 curses, 9/10 Paladin oaths | Author review (Lane B), not owner-blocking | Roadmap Phase 2 |
| 9 | L11–20 class progressions | Author review (Lane B), not owner-blocking | Roadmap Phase 2 |

Anything not on this list that looks ambiguous should be raised the same way: Continuity for lore, Director for scope and Director OK on draft/data work, owner for ASK OWNER policy — per the chain of command in `COLLABORATOR_ONBOARDING.md` §1–§2.
