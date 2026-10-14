# Overnight Briefing — Director (1am–7am push)

**Role:** Director, acting with final say on scope/priority/naming decisions except mass deletion, while the owner sleeps.
**Window:** 2026-07-29 ~1am–7am.
**Workers active overnight:** Continuity (lore/terminology arbiter), Resonance, Session, Chargen, Race.
**Companion doc:** [`OVERNIGHT_HANDOFF.md`](./OVERNIGHT_HANDOFF.md) — the morning-facing summary. This file is the Director's working log; the handoff is what the owner should actually read first.

---

## Mission

1. Give the Drow player race an exotic, IP-safe rename — prefer real in-world coinage over an invented word. *(Overnight AM: ratified interim **Umbral Elf**; superseded late 2026-07-29 by **Umbrin** — see Decision 1 addendum.)*
2. Clear vagueness escalated by Continuity and workers — resolve what a Director reasonably can, draft-fill what has no source but blocks play, and only pass genuine policy conflicts to the human owner.
3. Develop gaps aggressively — don't let "missing" sit as "missing" overnight if a sensible, clearly-labeled `draft: true` fill is possible.
4. Leave a clean, low-risk morning handoff: nothing mass-deleted, everything reversible, every draft labeled as draft.

## Success criteria (by ~7am)

- [x] Drow rename decided and implemented; Director has ratified it in this doc and in `MECHANICS_ROADMAP.md`.
- [x] No genuinely blocking ASK OWNER item left ambiguously "vague" — all 7 rows of `CONTINUITY_REPORT.md`'s table are resolved, closed as a false escalation, or draft-filled with a clear `directorNote`. (`CHARGEN_PROGRESSION.md` keeps 5 lower-stakes author-review/prioritization rows open by design — those aren't contradictions, just backlog, and closing them would mean guessing policy that isn't mine to guess.)
- [x] `MECHANICS_ROADMAP.md` Director Status reflects the overnight wave.
- [x] `OVERNIGHT_HANDOFF.md` is complete and readable in under 5 minutes over the owner's first coffee.
- [x] `npx tsc --noEmit` stays clean through the end of the window (spot-checked after each code-touching change; last clean run after the dungeon/entryClasses edit and again after the overnight wave settled).
- [ ] Nothing was mass-deleted; every content change is additive, a rename, or a `draft: true` flag — never a silent removal.

---

## Director decisions log (append-only, most recent last)

### Decision 1 — Drow rename: interim "Umbral Elf" → **Umbrin** (current)

**When:** overnight AM, after the Race worker's pass landed; **superseded late 2026-07-29 PM** by Director/owner direction.
**Ask:** owner wanted an exotic rename for the Drow player race, preferring found in-world coinage first, falling back to aligning with the bestiary's interim Umbral Elf rename.
**Overnight AM decision (historical):** ratified **Umbral Elf** (id `umbral-elf`) as a bestiary-aligned fallback when no stronger demonym surfaced. Also absorbed **Undercommon** → **Murkish** (D&D term removal).
**Current decision (late 2026-07-29):** **Umbrin** is the product race name (id `umbrin`). Obsidian-skinned elves of The Murk; noble subrace **Obsidian Highborn**; traits **Umbrin Magic** / **Umbrin Weapon Training**; exile by **Calan'thir** and the **First Choir**; Murk **Umbra** cult heresy. Umbral Elf was interim only — legacy saves (`Drow`, `Umbral Elf`, `Noble Umbral Elf`) migrate on load.
**Status:** **Final (Umbrin).** Lore stub: `docs/mechanics/UMBRIN_LORE.md`. See `src/data/CONTINUITY_REPORT.md` item 14 and `src/data/CONTINUITY_GLOSSARY.md`.

### Decision 2 — Session/Resonance defaults if workers escalate

**Standing default (should not need re-litigating tonight):** the Resonance/RP economy question was already closed by the owner before this overnight window (Hybrid-B, product name "Resonance"/"RP" — see `RESONANCE_CANON.md`). If the Resonance or Session workers escalate anything overnight, the default ruling is:
- **Do not reopen the Hybrid-B model choice.** Only escalate to me if a *drafted* multiclass RP formula or a *drafted* rest/recovery number conflicts badly with the existing `resonance-economy.js` helpers — not for routine wiring questions.
- **Oracle stays on Revelation Charges, never RP.** Any escalation that tries to merge the two pools gets bounced back with this line quoted.
- **Session party-RP pool sizing (VQ-11) default:** if Session needs an answer overnight rather than leaving it manual, default to **sum of loaded characters' individual computed max RP** (from `defaultMaxRp()`), not a flat GM-fiat number — this is the least-invented option since the per-character math already exists. Flag `draft: true` on the aggregation, not on the underlying per-character formula.
- **Rest/recovery wiring (VQ-10):** if Session needs short/long rest buttons before I'm back, use the existing `shortRestRecovery()` / `longRestRecovery()` / `meditationRecovery()` helpers from `resonance-economy.js` as-is — don't invent new percentages.

### Decision 3 — Cosmology vs dungeon: dungeon wins

**Standing default, reaffirmed overnight:** where cosmology lore (`cosmology-lore.json`) and dungeon/play data (`dungeon-mechanics.json`, `floor-encounters.json`) disagree on anything a player will actually see at the table (gate boss names, tier structure, level bands), **the dungeon data wins for play**, and the cosmology entry gets a `[superseded by Dungeon Guide]` draft note rather than being deleted or silently rewritten. This was already applied by Continuity overnight to the Cosmology XIV vs `gateBosses[]` conflict (ASK OWNER #7 / VQ-01) before I reviewed it — I'm ratifying it here as the standing rule for the rest of the night so nobody re-litigates it: **any future cosmology/dungeon conflict resolves the same way without re-escalating**, unless it's a case where cosmology content isn't actually superseded (e.g., pure myth-history/flavor with no dungeon-side equivalent) — in that case it's not a conflict at all and both stand.

### Decision 4 — Close Gravetouched ASK OWNER #6 as a false escalation

**Context:** Continuity's overnight pass flagged that the original "Gravetouched definition not in available canon sources" escalation (from feat stub text) was never actually blocked — Gravetouched is prestige path **#10** in `prestige-lorebook.json` with a complete entry: base classes Cleric/Warrior/Crimson Agent (Lv 10+), full requirements list. The real, separate question (does Gravetouched count as a Bloodbound base class) was already resolved by the owner before tonight (**no** — Bloodbound is Crimson Agent/Thief only).
**Decision:** close ASK OWNER #6 outright. Updated `src/data/CONTINUITY_REPORT.md` (ASK OWNER table + "Already in good shape" section) and `docs/mechanics/CHARGEN_PROGRESSION.md` (ASK OWNER row 4 + prestige-paths note) to reflect this. Individual `feats.js` blurbs referencing "Gravetouched definition not in available canon sources" may still read as thin/draft — that's normal author-polish work, not a blocker, and Lane B should not treat it as an open policy question anymore.

### Decision 5 — Draft-fill dungeon `entryClasses` / `victoryConsequences` rather than leave them vague

**Context:** `dungeon-mechanics.json`'s `cycle.entryClasses` was a two-line placeholder ("Classes of Entry:" / "Victory Consequences: ...") and `cycle.victoryConsequences` was an empty string — both had been sitting as ASK OWNER #5 with no source found. Continuity's overnight note explicitly told me: fill from the 17 `CANON_CLASSES` + sensible draft victory notes per tier from `floor-encounters.json` themes, and not leave this as a vague ASK OWNER if I can draft it.
**Decision:**
- `entryClasses` → `{ draft: true, directorNote, eligible: [...17 CANON_CLASSES], policy: "..." }`. Policy: the Great Descent does not bar entry by class; all 17 canon classes may attempt entry when the Shardspire opens. No rulebook source was found restricting entry, so "no restriction" is the least-invented default — much safer than guessing which classes are excluded.
- `victoryConsequences` → `{ draft: true, directorNote, summary, byTier: [10 entries] }`, one sentence of in-fiction consequence per tier, derived directly from that tier's existing boss/zone name and theme in `floor-encounters.json` (e.g., Tier 3's Brogi-forge theme → forge-priesthood/weapon-tax law; Tier 10's Marquis of Silence/Hush theme → Hush Beneath the Song becomes the dominant state rite). This follows the exact pattern already established in `dungeon-mechanics.json`'s own `mythHistory` array (e.g., "a farmer emerged with a crown of flame, founding Tyrnathar"), so it's extending an existing authored pattern, not inventing a new one.
- **Light-touch code follow-up:** `DungeonGuide.tsx` read `entryClasses` as an array and `victoryConsequences` as a string — both would have broken on the new object shape. Updated the "Cycle & Shardspire" card to render the new structure with "(draft)" badges. Verified `npx tsc --noEmit` clean afterward.
- Updated `src/data/CONTINUITY_REPORT.md` (ASK OWNER #5), `docs/mechanics/CHARGEN_PROGRESSION.md` (row 10), and `src/data/content-gap-report.json` (`dungeon-cycle-entry-classes` gap → `status: "draft-filled"`) to match.
- **Not closed, intentionally:** this is a Director default, not a real source. Re-open (don't just silently promote out of draft) if `rulebook_output.txt` Ch XII or a lore extract ever turns up actual restrictions or consequences.

---

## What's explicitly NOT being decided by the Director tonight

- No 18th class, no roster change (locked, owner-final).
- No promotion of draft Oracle/Paladin/Druid trees to canon without author/docx cross-check — Lane B territory, not a Director call.
- No Unity/Unreal/3D work, no SWTOR asset wiring (locked strategy, see `.cursor/rules/ttrpg-first-strategy.mdc`).
- No mass deletion of any kind. Every change tonight is a targeted rename, a `draft: true` fill, or a doc status update.

---

## Reference

- Chain of command / gates: `docs/COLLABORATOR_ONBOARDING.md`
- Living audit: `src/data/CONTINUITY_REPORT.md`
- Continuity's overnight vague-item backlog: `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md`
- Roadmap + Director Status: `docs/MECHANICS_ROADMAP.md`
- Morning handoff: `docs/mechanics/OVERNIGHT_HANDOFF.md`
