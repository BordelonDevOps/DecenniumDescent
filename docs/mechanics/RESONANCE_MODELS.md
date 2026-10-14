# Resonance / Spellcasting Economy — Model A vs Model B

**Product:** Decennium Descent companion (`DecenniumDescent-main`)
**Audience:** Owner decision doc (Owner Ruling #2) — **RESOLVED**
**Source:** `rulebook_output.txt` (extracted from *Decennium Descent Player Rulebook.docx*)
**Terminology cross-ref:** [`src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md), [`CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md)
**Last updated:** 2026-07-29

> ## DIRECTOR CHOICE: Hybrid-B — canon system name is **Resonance**
>
> **Decided:** 2026-07-29 (owner-delegated ruling, Director executing).
>
> The owner picked an explicit hybrid, anchored on **Model B** (§2) as the mechanical spine, with a **musical/resonance flavor pass** tying it into existing Aethel cosmology (Choir, First Song, Turning Spiral, reputation) and a few simplicity concessions borrowed from Model A (§1). **Player-facing system name is `Resonance` / `Resonance Points (RP)` — not "Song of the Weave."** "Hybrid-B" is an internal/collaborator label for this ruling (fine in docs, code comments, draft badges) and must never appear in player-facing UI or on character sheets.
>
> **Rationale:**
> - Model A (relabeled 5e slots) was **rejected outright** — not unique, doesn't use the book's own reputation/alignment systems, and undersells the "Weave responds to who you are" pitch already promised in Ch9's intro text.
> - Model B is the mechanical spine: one fungible RP pool (not per-level slots), `spell level × 2` base cost modified by school affinity/opposition and reputation, short/long rest + optional meditation recovery, and an overcast/Burnout menu — kept close to rulebook-as-written.
> - **From Model A, kept only:** player-facing simplicity where possible (clear spend/regain UI, no parallel slot tracks) and pool-size *tables* for the four classes that have complete Ch9 numbers (Wizard/Mage/Cleric/Druid) — no separate slot-count system is implemented alongside RP.
> - **Oracle is excluded**, unchanged: Oracle keeps Revelation Charges. Ch9's contradictory "Fate Weaving" Oracle paragraph is confirmed **non-canon** and should be disregarded regardless.
> - **Multiclassing** is **TBD/draft**: Director default is highest caster-tier pool + a small off-class bonus, flagged as a draft placeholder — not a final ruling. If real numbers conflict badly once drafted, escalate ASK OWNER rather than guessing further.
>
> **Playable canon summary for collaborators:** [`RESONANCE_CANON.md`](./RESONANCE_CANON.md).
> **Code:** [`src/data/resonance-economy.js`](../../src/data/resonance-economy.js) — `spellCost()`, `defaultMaxRp()` (Phase 1, done); overcast panel is **Phase 2** (stub only).
>
> §6's CHOOSE checklist below is resolved by this ruling and kept for historical context.

**Status:** Ruling landed 2026-07-29. Model comparison below (§1–§5) stays as historical reference for *why* Hybrid-B was chosen. `CharacterBuilder.tsx` / `CharacterSheet.tsx` / `SessionTracker.tsx` now read draft/canon max-RP values from `resonance-economy.js` (see `RESONANCE_CANON.md`); the flat placeholder described in [§4](#4-current-companion-placeholder-flat-rp) is superseded except where noted Phase 2.

---

## 0. Why this doc exists

The rulebook text contains **two different, mutually incompatible descriptions** of how spellcasters spend and recover magic:

- **Model A** — a lightly-relabeled 5e-style slot system, found in the Chapter 3 class write-ups (fully spelled out for Druid; implied structurally for Wizard/Mage/Cleric/etc. via their level tables and "spell slot" language elsewhere in the book).
- **Model B** — a from-scratch "Resonance System" in **Chapter 9: Spellcasting**, with a numeric RP pool, alignment affinity discounts, reputation modifiers, and an overcast/burnout mini-game.

Both use the term "Resonance Points," both apply to the same classes, and their numbers **do not reconcile** (see [§3](#3-side-by-side-comparison)). This doc lays out each model on its own terms so the owner can pick one, or specify a hybrid, before this gets baked into `class-details.js` / the Weave tab.

---

## 1. Model A — Chapter 3 class-text slot system ("relabeled 5e")

**Where it lives:** Chapter 3: Classes (`rulebook_output.txt` line 852 onward). Most completely written out for the **Druid** (lines 1395–1479); every other Ch3 caster (Wizard, Mage, Cleric, Bard, Paladin, Ranger) has the same shape of class entry (Cantrips Known / Spellcasting Ability / Spell Save DC blocks) but the per-level table itself didn't survive the docx→text extraction (tables rendered as images in the source), so Druid is the fullest textual example of the pattern.

### Plain-English summary

This is D&D 5e's spell-slot system with "spell slots" find-and-replaced to "Resonance Points" in most (not all) places. You have a fixed number of Resonance Points **per spell level** (a "Resonance Point of level N" can only cast a spell of level N or lower, one point per casting regardless of level). You prepare a list of known spells (Wisdom/Int/Cha mod + level), spend one point equal to the spell's level to cast it, and get everything back on a long rest. Some subclasses (Circle of the Land) grant a short-rest partial-recovery feature, D&D's Arcane Recovery equivalent.

### Mechanics

| Aspect | Rule | Citation |
|---|---|---|
| **Recovery** | All expended points return on a long rest. Some subclass features (Circle of the Land's Natural Recovery) let you recover a limited amount on a short rest, once/day, capped at half your level (rounded up) and excluding 6th-level-or-higher points. | rulebook_output.txt:1422, 1508 |
| **Spend** | Cast a spell by expending **one Resonance Point of a level ≥ the spell's level** (i.e., a "slot," not a fungible currency). Cantrips are free. | rulebook_output.txt:1422–1424 |
| **Level scaling** | Follows a per-spell-level table by class ("The Druid Table" — table itself lost in extraction, but text confirms slot-by-level structure identical to 5e spell slot progression). Number of *prepared* spells = spellcasting-ability modifier + class level. | rulebook_output.txt:1420–1424, 1480 |
| **Overcast** | **None.** No mechanic for spending extra points to boost a spell. | — (absent from Ch3 text) |
| **Reputation interaction** | **None** baked into the class text itself. | — |
| **Oracle interaction** | N/A — Oracle never uses this system; it has its own Revelation Charges track (see [§5](#5-oracle--already-decided-separately)). | rulebook_output.txt:2189 |
| **Terminology leakage** | Some Ch2 racial traits (Undead/Lichborn's Arcane Recovery) and the Ch6 multiclassing rules still say "**spell slots**" verbatim, unrenamed — confirming this model is the book's original, un-refactored default. | rulebook_output.txt:839, 5316–5318 |

### Pros for playtest / companion UI

- **Zero new math.** It's 5e's slot table; any published 5e-compatible slot progression can be dropped in as-is (or reconstructed quickly) since the shape is fully known even where Aethel-specific numbers are missing.
- **Familiar to players.** Anyone who's played 5e (i.e., most of the target audience) already understands "spend a slot of the spell's level, get them all back on long rest."
- **Cheap to build.** A `resonanceSlotsByLevel[casterLevel]` lookup table + a per-spell-level counter is a small, well-understood data structure — much simpler than Model B's live-modifier stack.
- **Predictable for the GM.** No per-cast arithmetic (alignment/reputation/school modifiers) to adjudicate mid-combat.

### Cons for playtest / companion UI

- **Doesn't use any of the book's alignment/reputation/faction systems** that are otherwise a first-class, cross-cutting mechanic in this book (Ch4 Reputation Tiers, Ch7 Reputation Modifiers) — a missed opportunity for the "Weave responds to who you are" flavor promised in the Ch9 intro (rulebook_output.txt:6068).
- **Per-level slot tables for every class are incomplete** in the extracted text (only Druid's prose survived; the actual numeric tables were images) — would need reconstruction/approximation work before the companion could show real numbers for all 12+ Weave-casting classes.
- **Less distinctive** — reads as "5e with a new noun," which undercuts the "custom point-pool" flavor implied by the RP name and by Ch9's framing text.

---

## 2. Model B — Chapter 9 "The Resonance System"

**Where it lives:** Chapter 9: Spellcasting (rulebook_output.txt line 6059 onward, header "The Resonance System" at line 6069).

### Plain-English summary

This is a genuine points-pool economy, closer to a mana bar than 5e slots. You have one flat pool of Resonance Points sized by class/level/casting-attribute/**alignment**/**reputation**. Every spell costs `spell level × 2` RP as a base, modified up or down by school affinity (your alignment likes/dislikes certain schools), faction reputation, and class specialization. You regen a quarter of your pool on a short rest, all of it on a long rest, or a flat trickle via 10-minute meditation. You can spend *extra* RP to overcast (bigger damage, longer duration, wider area, bonus-action casting, etc.), but drop below 25% of your max and you risk "Resonance Burnout."

### Mechanics

| Aspect | Rule | Citation |
|---|---|---|
| **Pool size** | Determined by class + level (explicit table, L1–20, for Wizard/Mage/Cleric/Druid: e.g., L1 Wizard 4 / Mage 3 / Cleric 3 / Druid 3, scaling to L20 Wizard 80 / Mage 60 / Cleric 58 / Druid 58), further modified by primary spellcasting attribute, alignment, and reputation. | rulebook_output.txt:6072–6100 |
| **Spend** | Base cost = **spell level × 2** RP. Modified by: affinity discount (-1, aligned school), opposition penalty (+1, opposed school), reputation modifier (±1), specialization discount (-1 to -3, subclass-dependent). Cantrips cost 0. | rulebook_output.txt:6101–6108 |
| **Level scaling** | Explicit per-class, per-level table (see pool size row); pool grows faster than Model A's slot count because it's a lump sum rather than tiered slots. | rulebook_output.txt:6077–6100 |
| **Overcast** | Named "metamagic"-style menu: Empowered (+2 RP, +50% dmg/healing), Extended (+1 RP, 2× duration), Widened (+3 RP, 2× AoE), Heightened (+4 RP, +1 effective spell level), Quickened (+3 RP, bonus action), Subtle (+1 RP, no V/S), Distant (+1 RP, 2× range), Twinned (+3 RP, 2nd target). Risk of "Resonance Burnout" if pool drops below 25% max. | rulebook_output.txt:6118–6128 |
| **Reputation interaction** | Explicit, multi-faction: Academic Factions (spell-learning discounts/penalties), Religious Orders (domain RP discount / spell failure chance), Arcane Guilds (**±2 max RP**), Nature Circles (regen rate + urban-prep restriction). Casting certain spells can itself move reputation (e.g., necromancy in town). | rulebook_output.txt:6144–6158 |
| **Alignment interaction** | Good/Neutral/Evil each get a 3-school "natural affinity" (-1 RP), a neutral bucket, and a 2-school "opposition" (+1 RP) — plus location-based regen bonuses (+2 RP/rest) for aligned terrain (sacred ground for Good, wild for Neutral, corrupted for Evil) and possible alignment shift from repeated opposition-school casting. | rulebook_output.txt:6114–6143 |
| **Oracle interaction** | ⚠️ **Internally inconsistent.** Ch9 gives Oracle its own paragraph under "Specialized Casters" — a "Fate Weaving System" with a "Fate Mark" granting domain access — that **does not match** the Oracle class chapter's actual Revelation Charges / Mystery / Oracle's Curse design (rulebook_output.txt:2189–2340) already used everywhere else in the book and already implemented in the companion. Treat Ch9's Oracle blurb as a stale/unintegrated draft, not canon. | rulebook_output.txt:6419–6424 vs 2189–2340 |
| **Class-specific resource crossover** | Ch9 also layers non-RP resources on top for hybrid/specialized casters — Bard Crescendo (reduces RP cost), Dragoon Momentum (reduces RP cost), Crimson Agent HP-as-fuel (bypasses RP), Shaman spirit bonds, Mirrorsage mirror-attunement (bypasses RP) — meaning even "one model" isn't fully uniform across all 17 classes. | rulebook_output.txt:6390–6436 |

### Pros for playtest / companion UI

- **Matches the book's own framing.** Ch9's intro text explicitly sells this as *the* system ("Decennium Descent uses a Resonance System..." rulebook_output.txt:6070) and it's the only place with complete L1–20 numeric tables for Wizard/Mage/Cleric/Druid ready to transcribe today.
- **Uses reputation/alignment**, which are already real, tracked, cross-cutting systems in this book (Ch4 Reputation Tiers) — big win for "your choices matter" flavor and for a future companion Reputation tracker to plug into.
- **Richer tactical layer** (overcast options) gives spellcasters more session-to-session decisions, which fits the "meaningful progression" pitch in the book's foreword.
- **Matches the companion's existing docs.** `CONTINUITY_GLOSSARY.md` already documents "cost = spell level × 2 (modified by affinity)" and "L1 table: Wizard 4, Mage/Cleric/Druid 3" — i.e., **Model B's numbers**, not Model A's — even though no UI code enforces them yet. Choosing Model A would require correcting that glossary.

### Cons for playtest / companion UI

- **Heaviest to implement.** Every cast needs a live modifier stack (alignment × school × reputation × specialization × overcast choices) before you know the RP cost — much more UI and validation surface than a slot counter, and requires a Reputation data model that doesn't fully exist in the companion yet.
- **GM overhead at the table.** Adjudicating "is Divination aligned with your alignment, do you have Academic Faction standing, is this an overcast Empowered+Extended cast" per spell is a lot of bookkeeping for a live session — more amenable to a well-built companion UI than to paper play.
- **Numbers don't fully reconcile with the rest of the book.** The multiclassing chapter (Ch6) still computes spellcasting via "spell slots" and the Multiclass Spellcaster slot-per-level table (rulebook_output.txt:5316–5318) — if Model B is chosen, multiclassing math needs a conversion rule (RP pool merge? Slot-equivalent conversion?) that isn't specified anywhere.
- **Self-contradicts on Oracle** (see table above) — picking Model B wholesale means explicitly overriding/discarding its Oracle paragraph in favor of the Revelation Charges system already canonized elsewhere.
- **25% burnout threshold and overcast costs are unbalanced at low levels** (a L1 Wizard with 4 RP can't even afford a single Empowered/Widened/Heightened cast without risking burnout) — would need playtest tuning regardless of adoption.

---

## 3. Side-by-side comparison

| | **Model A — Ch3 slot-style** | **Model B — Ch9 Resonance System** |
|---|---|---|
| **Core shape** | Tiered slots (one pool *per spell level*) | Single fungible point pool |
| **Recovery** | All slots back on long rest; limited short-rest recovery via specific subclass features only (e.g., Circle of the Land) | 1/4 max pool on short rest (+ casting-mod), all on long rest, or flat trickle via 10-min meditation |
| **Spend** | 1 slot of level ≥ spell level (slot "level," not a scalar cost) | `spell level × 2` RP, adjusted by affinity/opposition/reputation/specialization |
| **Level scaling** | Per-spell-level slot table (5e-shaped); numeric table lost in extraction except Druid's prose | Explicit lump-sum table per class, L1–20 (fully present for Wizard/Mage/Cleric/Druid) |
| **Overcast** | None | Yes — 8 named options (Empowered, Extended, Widened, Heightened, Quickened, Subtle, Distant, Twinned), gated by Burnout risk below 25% max RP |
| **Reputation interaction** | None | Yes — 4 faction tracks modify max RP, regen rate, cast reliability, and spell-learning |
| **Alignment interaction** | None | Yes — school affinity/opposition discounts, location-based regen bonus, possible alignment drift |
| **Oracle interaction** | N/A (Oracle always separate) | Contradicts canon Oracle design; should be ignored/overridden |
| **Multiclass math** | Matches Ch6's existing "spell slots" multiclass table directly | Needs a new conversion rule — none specified |
| **Companion build cost** | Low (lookup table + counter) | Medium–high (modifier stack + reputation/alignment data model) |
| **Current doc/data lean** | Not reflected in `CONTINUITY_GLOSSARY.md` | Already the model implied by `CONTINUITY_GLOSSARY.md`'s RP formula, though not yet built |

---

## 4. Current companion placeholder (flat RP)

Today the companion implements **neither** model faithfully — it's a manual counter with no formula behind it:

- `CharacterBuilder.tsx` — `resonancePoints` state defaults to **3** for every class/level (`useState<number>(3)`), with a plain number input the player edits by hand ("Spend RP to push the Weave at the table"). No level, class, alignment, or reputation term feeds into it.
- `CharacterSheet.tsx` — displays `character.resonancePoints ?? 3` as a static badge; no derivation logic.
- `SessionTracker.tsx` — tracks a separate **party-wide** `partyResonance` pool (default 6, capped 0–24) with manual +1/-1 buttons ("Spend 1 RP" / "Gain 1 RP"), independent of any individual character's sheet value.
- Oracle characters are explicitly carved out of this RP flow in the builder UI ("Oracles use Revelation Charges and Mystery Revelations — not Weave Resonance Points").

This is a deliberate stub pending this ruling — it should **not** be read as an implicit vote for either model.

## 5. Oracle — already decided separately

Oracle does **not** participate in whichever model is chosen here. It already has its own resource track, consistent between the rulebook's Oracle chapter and the companion:

- **Revelation Charges**: starts at 3, max 7, spent to activate Mystery Revelations (1/2/3 charges by tier), recovered via each Mystery's unique **Prophecy Trigger** rather than rest-based recovery. (rulebook_output.txt:2189, 2223–2340)
- Companion: `resonancePoints: 0` is force-set for Oracle rows in `SessionTracker.tsx` (line 288); Oracle is excluded from `isSpellcasterClass()` per `CHARGEN_PROGRESSION.md`.
- Note the one contradiction flagged in §2: Ch9's Resonance chapter has a stray, non-canon "Fate Weaving" Oracle paragraph that should be disregarded regardless of which model wins.

---

## 6. CHOOSE A / B / HYBRID — **RESOLVED: Hybrid-B ("Resonance")**

- [x] **A — Adopt Ch3 slot-style system.** **Rejected** — not unique, weak musical/reputation tie-in.
- [x] **B — Adopt Ch9 dedicated Resonance System.** **Adopted as the mechanical spine** (pool, cost formula, recovery, overcast, reputation/alignment hooks).
- [x] **Hybrid — specify shape.** **This is the ruling.** Model B's pool/cost/recovery/overcast math, kept close to rulebook-as-written; Model A contributes only "no parallel slot tracks" simplicity and its pool-size table convention (applied using Model B's actual numbers for Wizard/Mage/Cleric/Druid). See the DIRECTOR CHOICE banner at the top of this doc and [`RESONANCE_CANON.md`](./RESONANCE_CANON.md) for the full playable summary.

**Completed follow-ups:** `CONTINUITY_GLOSSARY.md`, `MECHANICS_BIBLE_STUB.md`, `MECHANICS_ROADMAP.md`, and `REPUTATION.md` cross-links updated to reflect Hybrid-B as canon; `resonance-economy.js` implements `spellCost()`/`defaultMaxRp()`; `CharacterBuilder.tsx`/`CharacterSheet.tsx`/`SessionTracker.tsx` display computed max RP.

**Still open (not part of this ruling):** Ch6 multiclass slot-table reconciliation (draft default only, see `RESONANCE_CANON.md` §7), reputation → RP modifiers actually applied (currently documented, not auto-wired), overcast panel UI (Phase 2).

---

## Appendix — key line citations (`rulebook_output.txt`)

| Topic | Lines |
|---|---|
| Chapter 3 header | 852 |
| Druid spellcasting (Model A full text) | 1417–1433 |
| Druid Natural Recovery (short-rest partial recovery) | 1507–1509 |
| Undead "Arcane Recovery" (unrenamed "spell slots") | 839 |
| Ch6 Multiclass Spellcaster slot table reference | 5316–5318 |
| Chapter 9 header + Weave intro | 6059–6068 |
| The Resonance System (Model B core) | 6069–6128 |
| Alignment and Magic | 6129–6143 |
| Reputation and Magic | 6144–6158 |
| Wizard/Mage/Cleric/Druid RP tables (Model B) | 6166–6187, 6222–6243, 6279–6300, 6335–6356 |
| Hybrid/Specialized caster resource layers (Crescendo, Momentum, Blood Marks, etc.) | 6387–6436 |
| Oracle canon (Revelation Charges, Mystery, Curse) | 2189–2340 |
| Oracle non-canon Ch9 "Fate Weaving" contradiction | 6419–6424 |
