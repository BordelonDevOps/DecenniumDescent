# Decennium Descent — Mechanics Readiness Roadmap

**Owner:** Director (game mechanics readiness)
**Date:** 2026-07-29
**Purpose:** Ordered path from chargen → session play → dungeon, what's done vs draft vs missing, and who owns each gap when collaborators (writers, designers, playtesters) join.

**Inputs used:** `src/data/CONTINUITY_REPORT.md`, `src/data/CONTENT_GAPS.md`, `src/data/content-gap-report.json`, `src/data/canon-classes.js`, `src/data/class-details.js`, `src/data/class-paths.js`, `src/data/prestige-lorebook.json`, `src/data/dungeon-mechanics.json`, `rulebook_output.txt`, `src/components/SessionTracker.tsx`, `src/lib/character-storage.js`.

**Chain of command:** Workers escalate lore/terminology conflicts to **Continuity**, and scope/priority conflicts to the **Director**. Routine draft/data work in `src/data/*` and `docs/` is **accepted for the product only after Director OK** (owner ruling #6 — see `COLLABORATOR_ONBOARDING.md` §2). The Director escalates anything neither can resolve to the **human owner** — see the Director Status block at the end of this doc and in `COLLABORATOR_ONBOARDING.md`. Nobody should invent product policy, add/remove a class, or resolve a lore contradiction unilaterally — stop and ask.

---

## How to read this roadmap

- **Status:** `done` (rulebook-canon, wired, no known gaps) · `draft` (playable but flagged `draft: true` or otherwise provisional; needs author/owner promotion) · `missing` (no data or no UI wiring yet).
- **Lane:** which worker lane (A/B/C, defined below) should pick this up.
- **Ask Owner:** flagged where the Director cannot assign work without a human decision.

---

## Worker lanes

| Lane | Scope | Primary files |
|------|-------|----------------|
| **A — Core resolution & session** | d20 core roll, Resonance/RP economy, rest/overcast rules, initiative, horn clock, session tracker, reputation | `rulebook_output.txt` Ch7–8 & "Resonance System", `src/components/SessionTracker.tsx`, `src/data/dungeon-mechanics.json` (hornRule) |
| **B — Character progression & chargen** | Races, backgrounds, classes, class-paths (arch/hero), prestige, feats, spells, Oracle/Paladin/Druid subsystems, L11–20 tables | `src/data/canon-classes.js`, `class-details.js`, `class-paths.js`, `class-draft-levels.js`, `feats.js`, `spells.js`, `prestige-lorebook.json`, `oracle-mysteries.js`, `oracle-curses.js`, `paladin-oaths.js`, `druid-shapeshifting.js`, `racial-variants.json`, `backgrounds.js` |
| **C — World / dungeon / encounters / items** | Cosmology, dungeon tiers/cycle/gate bosses, floor encounters, bestiary, crafting/items, generators | `cosmology-lore.json`, `dungeon-mechanics.json`, `floor-encounters.json`, `src/bestiary_data_full.json`, `crafting-recipes.json`, `src/components/GeneratorsPanel.tsx`, `DungeonGuide.tsx`, `EncountersBrowser.tsx` |

Continuity (lore/terminology arbiter) is a cross-cutting reviewer for all three lanes, not a 4th production lane.

---

## Phase 0 — Foundation audit (done)

Completed by Continuity pass 2026-07-29 (`CONTINUITY_REPORT.md`). No action needed unless new contradictions surface.

- 17-class roster locked (`canon-classes.js`), Swashbuckler/Fighter archived correctly.
- Oracle Revelation Charges vs spell-slot language corrected in UI.
- Druid class-paths now cover all 7 circles.
- Prestige↔feat cross-references: 0 missing (18 prestige paths).
- Cosmology↔dungeon gate bosses: all 10 aligned.

---

## Phase 1 — Core resolution economy (Lane A) — **status: Resonance economy resolved, wiring in progress**

| Item | Status | Detail | Lane | Ask Owner? |
|------|--------|--------|------|------------|
| d20 core roll (ability check / save / attack) | done | `rulebook_output.txt:5682` — roll d20 + modifier vs DC. Standard, no gaps. | A | no |
| **Resonance Points (RP) economy** | **RESOLVED (canon: Hybrid-B, "Resonance")** | Owner-delegated ruling, 2026-07-29: canon is Hybrid-B, anchored on the Ch9 pool-based model (Base Cost = Spell Level × 2, alignment/reputation modifiers, overcasting menu, burnout at 25%) with musical/Choir flavor and Model A's UI-simplicity concessions layered on. **System name is `Resonance`/`RP`, not "Song of the Weave."** See `docs/mechanics/RESONANCE_CANON.md`. Pool-size + cost formula implemented in `src/data/resonance-economy.js` (`spellCost()`, `defaultMaxRp()`); `character-storage.js`'s flat `resonancePoints` field is unchanged (still player-editable) but `CharacterBuilder.tsx`/`CharacterSheet.tsx`/`SessionTracker.tsx` now show the computed max alongside it. | A | **no — resolved** |
| Horn clock (120-hour retreat rule) | done (lore) / draft (UI) | `dungeon-mechanics.json.hornRule`; wired as an elapsed-hours display in `SessionTracker.tsx`. No penalty/consequence logic beyond display. | A | no |
| Initiative | done | `rollInitiative()` in `SessionTracker.tsx`, standard d20 + Dex. | A | no |
| Reputation / faction standing | **done (session + RP link shipped overnight)** | Live tracker (`ReputationPanel.tsx`, `reputation.js`, `REPUTATION.md`). Reputation → RP wired overnight: Arcane Guilds ±1/±2 max RP, Religious/Academic/Nature tracks ±1 spell cost, Nature Circles ±1 retune — via `resolveMaxRp()`/`computeSpellCost()`/`retuneRepBonus()` in `resonance-economy.js`, consumed by Builder/Sheet/SessionTracker. | A | no — resolved |
| Overcasting (Empowered/Extended/Widened/etc.) | **draft (Phase 2 stub shipped overnight)** | `OVERCAST_OPTIONS`/`overcastRpCost()`/`totalCastCost()`/`burnoutThreshold()`/`isBurnoutRisk()` in `resonance-economy.js`; SessionTracker now has an overcast toggle row + "Apply overcast spend" + Burnout badge per combatant. Not yet tied to a spell picker's base cost (manual entry at table). | A | no |
| Short/long rest recovery | **done (wired overnight)** | `retuneAmount()`/`fullRestore()` now called from SessionTracker **Retune** / **Full** buttons per combatant (RP + Oracle RC together); `meditationRecovery()` still unwired (low priority). | A | no |

**Lane A work package (updated, overnight waves 1–5):** RP model decision is closed; reputation→RP wiring, rest buttons, Phase 2 overcast stub, and **multiclass RP merge** (`mergeMulticlassMaxRp()` per `RESONANCE_CANON.md` §7 — still `draft: true`) all **shipped overnight**. Remaining Lane A work: (1) `CLASS_SPELL_REP_TRACK` per-class→faction mapping needs author review (Director defaults), (2) tie the overcast panel to an actual spell's base cost instead of manual entry, (3) meditation recovery UI. None require another owner decision unless numbers conflict badly.

---

## Phase 2 — Chargen (Lane B) — **status: mostly done, drafts flagged**

| Item | Status | Detail | Ask Owner? |
|------|--------|--------|------|
| Races (14 builder + 42 variants) | done (partial) | Cosmology-only races (Eldrin, Dreadborn, etc.) intentionally excluded from player builder per existing gap ticket. `races.js` vs `builder-races.js` duplication should be deduped by Lane B. **Drow → Umbrin rename complete overnight** (interim "Umbral Elf" superseded by direct owner direction late 2026-07-29 — see Director Status #3 and `docs/mechanics/UMBRIN_LORE.md`). | no — resolved |
| Backgrounds (20) | done | Aligned with rulebook Ch4. | no |
| 17 canon classes | done | Locked, dev-time drift guard in place. | no — **do not reopen without owner sign-off (see Director Status #2)** |
| Class-paths (arch L3–9 / hero L10+) | done for all 17 | Continuity pass completed Druid/Oracle/Paladin. | no |
| L11–20 class progressions | **draft (full coverage shipped overnight)** | `class-draft-levels.js` — **all 17 canon classes now have L11–20 representation** (canon where `class-details.js` has it — Druid full canon; Oracle/Paladin/Wizard canon + new draft milestones for remaining levels; other 13 classes on existing draft milestones). Still `draft: true` pending rulebook table cross-check. | no — author review, not a policy question |
| Oracle mysteries (10) | draft (9 of 10) | Ancestor + Spiral-Touched are rulebook canon; Battle–Time mysteries are Aethel-authored draft trees pending review. | no |
| Oracle curses (10) | draft (9 of 10) | Same pattern; Spiral-Touched canon. | no |
| Paladin Sacred Oaths (10) | draft (9 of 10) | Mercy is rulebook-canon; 9 have draft revelation lists pending `Paladin_Oaths_*.docx` reconciliation. | no |
| Druid shapeshifting (7 circles) | done (core) / draft (session tracking) | Circle/form data wired in Builder; Session tab doesn't track wild-shape uses/CR yet. | no |
| Prestige paths (18) | done | Cross-checked against feats, 0 missing references. Spot-check vs `Decennium_Prestige_Classes.docx` still open (low priority). | no |
| Feats (336 live vs 330-title doc) | **draft/missing** | Placeholder descriptions on some entries; root `game-data.js`/`additional-feats.js` unwired legacy. | no |
| Racial feats | partial | 42 subrace variants exist; not yet surfaced as searchable Feats-tab entries. | no |
| Multiclass (secondary class + level) | **done (UI + RP merge, wave 3–4)** | Builder optional secondary class/level; `mergeMulticlassMaxRp()` per `RESONANCE_CANON.md` §7 — formula `draft: true` pending Ch6 cross-check. | no |
| Skill modifiers | draft | `CharacterBuilder` skills use static hardcoded modifiers, not derived from ability scores/proficiencies. | no |

**Lane B work package:**
1. Promote or revise Oracle/Paladin draft trees against source docx (author review, not invention).
2. Fill `class-draft-levels.js` L11–20 from rulebook tables where they exist; flag remainder `draft: true` until source found.
3. Reconcile feats compendium (330 doc vs 336 live), remove placeholder text, wire `additional-feats.js`.
4. Derive skill modifiers from abilities + proficiencies instead of hardcoded values.
5. Dedupe `races.js` vs `builder-races.js`.

---

## Phase 3 — Session play (Lane A, with Lane B/C data dependencies) — **status: functional core, thin edges**

| Item | Status | Detail | Ask Owner? |
|------|--------|--------|------|
| Combat tracker (initiative, HP, resonance display) | done | `SessionTracker.tsx` — pulls saved characters + bestiary foes. | no |
| Horn clock display | done (display only) | See Phase 1. | no |
| Party Resonance pool display | **done (shipped overnight)** | Party RP pool now defaults to **sum of living Weave casters' max RP** (`sumWeaveCasterMaxRp`) instead of an independent manual counter; per-combatant RP/Oracle RC, Retune/Full rest buttons, and overcast/Burnout stub also live in `SessionTracker.tsx` (`session-utils.ts`). See `docs/mechanics/SESSION_LOOP.md`. | no |
| Reputation/faction tracking in session | done | Session picker adjusts saved-character faction scores; persists via `upsertCharacter()`. | no |
| Wild-shape use/CR tracking | missing | Druid forms defined but not tracked in combat. | no |
| Global search across spells/monsters/feats/encounters | missing | Header search box is decorative, no handler. | no |

**Lane A work package:** Reputation tracker + RP/RC session wiring and **rulebook HP import** (`class-hit-dice.js` → `estimatePcMaxHp()`) done overnight (waves 1 + 4). Remaining: wild-shape tracker, global search index (`docs/mechanics/SESSION_LOOP.md` gaps table).

---

## Phase 4 — Dungeon / world / encounters (Lane C) — **status: strong core, prose gaps**

| Item | Status | Detail | Ask Owner? |
|------|--------|--------|------|
| Dungeon tiers (10), gate bosses | done | All 10 tiers/bosses cross-validated against cosmology. | no |
| Cycle mechanics (10-year rotation, Shardspire) | done (lore) | `dungeon-mechanics.json.cycle`. | no |
| Cycle entry classes (who may enter each Cycle) | **draft (filled overnight)** | `entryClasses` now lists all 17 `CANON_CLASSES` as eligible + a `victoryConsequences.byTier` draft (10 entries, themed from `floor-encounters.json`); both `draft: true` in `dungeon-mechanics.json`. `DungeonGuide.tsx` updated to render the new shape. | no — Director default, re-open only if a real source is found |
| Floor encounters (10 tiers) | done (narrative) / partial (tables) | Per-floor encounter tables from `Floor Encounters.docx` may be richer than current JSON. | no |
| Bestiary (718 monsters) | done (data) / partial (location) | Canonical file lives outside `src/data/` (`src/bestiary_data_full.json`); stale 50-row subset still at repo root. | no |
| Bestiary D&D leakage | **resolved** | 54 entries renamed to Aethel-neutral labels — original scrub used Drow→Umbral Elf, since re-synced to **Umbrin** (Umbrin, Umbrin Spider-Priestess, Umbrin Matron, etc. — see Director Status #3; Mind Flayer→Voidmind, Beholder→Gaze Tyrant, etc. unaffected) — see `docs/mechanics/BESTIARY_SCRUB_LOG.md`. | no — resolved, see Director Status #3 |
| Cosmology First Song chapters | draft | Single concatenated blob; chapter nav incomplete (IX–XII). | no |
| Cosmology world sections | draft | Many subsections are bullet stubs, not full prose. | no |
| Crafting (623 recipes) | done | Validated against xlsx. | no |
| Generators (loot etc.) | done (data) / partial (linkage) | Uses recipe names for loot only; could expand to full encounter/NPC generation. | no |

**Lane C work package:**
1. Move canonical bestiary JSON into `src/data/`, retire stale root subset.
2. ~~Audit and remove/replace any remaining non-Aethel (D&D setting) proper nouns in bestiary~~ — **done** (54 entries, see `BESTIARY_SCRUB_LOG.md`); generic SRD labels (Owlbear etc.) remain out of scope per that log.
3. Split cosmology First Song extract into per-chapter JSON.
4. ~~Parse Cycle `entryClasses` from source once located; otherwise mark `draft: true` explicitly~~ — **done overnight**: filled from the 17-class roster and marked `draft: true` (no source located yet). Promote/revise if `rulebook_output.txt` Ch XII turns up.

---

## Cross-cutting: what NOT to touch

- **No Unity/Unreal/3D client work.** Strategy locked 2026-07-28: TTRPG-first, 3D only after the companion is complete or on explicit user pivot.
- **No SWTOR assets, branding, lore, or UI patterns in the product path.** Reference-only if they exist on disk; never wired into `src/`.
- **No 18th class, no roster changes.** v1 ships 17 base classes per Classes Table (owner final 2026-07-29). Rulebook "eighteen" prose is a confirmed typo; Fighter/Swashbuckler stay archive/orphan.
- **No silent invention of RP/resolution mechanics** — the contradiction in Phase 1 must go to the owner, not be guessed by a worker.

---

## Director status

### ASK OWNER (top decisions the Director cannot make alone)

**Status (post waves 1–5): all items below resolved — no open ASK OWNER blockers.**

1. ~~**Resolve the Resonance Points contradiction.**~~ **RESOLVED (owner-delegated ruling, 2026-07-29): canon is Hybrid-B, product name `Resonance`/`Resonance Points (RP)`.** Anchored on the Ch9 points-buy pool as the mechanical spine (cost formula, recovery, overcast/burnout), with musical/Choir/First Song flavor and a few Model A simplicity concessions (no parallel slot tracks; pool-table convention). "Song of the Weave" was considered and explicitly **rejected** as the system name — it may not appear in player-facing UI. See `docs/mechanics/RESONANCE_MODELS.md` (full ruling) and `docs/mechanics/RESONANCE_CANON.md` (playable summary). Multiclass RP math wired overnight wave 4 (`mergeMulticlassMaxRp()`) — still `draft: true`; re-escalate only if a drafted formula conflicts badly with Ch6.
2. ~~**Confirm the 17-class roster is final for v1.**~~ **Resolved (owner 2026-07-29):** v1 ships 17 base classes per Classes Table. Rulebook "eighteen" is a typo. Fighter (archive/reference) and Swashbuckler (orphan in `class-details.js` only) are not selectable and stay that way for v1.
3. ~~**Bestiary D&D-setting leakage**~~ **RESOLVED (owner 2026-07-29):** 54 creature entries renamed to Aethel-neutral labels (`BESTIARY_SCRUB_LOG.md`). **Extended overnight to the player race, in two steps:**
   - **Step 1 (2026-07-29 AM, interim):** Director ratified `races.js`/`builder-races.js`/`racial-variants.json` "Drow" → **Umbral Elf** (id `umbral-elf`), aligning with the bestiary's original scrub term, since no stronger player-race-specific coinage had surfaced beyond the region name "The Murk"/"Murkish".
   - **Step 2 (2026-07-29 PM, current/final direction) — SUPERSEDES Step 1:** direct owner update specified a one-word name clearly derived from **Umbra** (the primordial abyss), tied to obsidian, exile from **Calan'thir**/the First Choir's light, a perverse Umbra-worshipping heresy, an EverQuest-style dark-elf tone, and capacity for strange alliances. Director default and shipped name: **Umbrin** (id `umbrin`; noble subrace **Obsidian Highborn**; traits Umbrin Magic/Umbrin Weapon Training; language Undercommon → **Murkish**). Bestiary re-synced to match (Umbrin, Umbrin Spider-Priestess, Umbrin Matron, etc.); legacy saves (`Drow`, `Umbral Elf`, and subrace variants) migrate to Umbrin in `character-storage.js`. Full lore: `docs/mechanics/UMBRIN_LORE.md`.
   - **Do not re-ratify Umbral Elf as final** — it was a same-night interim step, fully superseded. See `src/data/CONTINUITY_REPORT.md` item 14 and `src/data/CONTINUITY_GLOSSARY.md` (Umbrin entry).
4. ~~**Reputation/faction system scope**~~ **RESOLVED (overnight waves 1–2):** live tracker (`ReputationPanel.tsx`, `reputation.js`) **and** reputation → RP modifiers wired (`resolveMaxRp()` / `computeSpellCost()` / `retuneRepBonus()` in `resonance-economy.js`, consumed by Builder / Sheet / SessionTracker). No further scope decision needed unless new faction tracks are added.

### Resolved (owner input received)

5. **Collaborator access model** — **RESOLVED: Director OK gate** (owner ruling #6, 2026-07-29). Collaborators may draft in `src/data/*` and `docs/`; content is accepted for the product only after **Director OK**. Not unrestricted direct ship; human owner only for ASK OWNER escalations. See `COLLABORATOR_ONBOARDING.md` §2.
6. **Resonance economy — canon is Hybrid-B ("Resonance")** — see item #1 above. Logged here too since it closes out what was previously the single biggest Lane A blocker.

### Director decided (no owner input needed, logged for transparency)

- Locked worker lanes A/B/C as defined above, mapped to existing file ownership boundaries already implied by the continuity/gap reports.
- Treated all `draft: true` items as author-review work, not policy questions — assigned to the relevant lane rather than escalated.
- **17-class roster final for v1** (owner 2026-07-29): Fighter/Swashbuckler stay archive/orphan; collaborator FAQ one-liner is "v1 ships 17 base classes per Classes Table."
- Implemented the Hybrid-B Resonance ruling in `resonance-economy.js` and wired display-only max-RP into `CharacterBuilder.tsx`/`CharacterSheet.tsx`/`SessionTracker.tsx`; did not touch the live-editable `resonancePoints` field's behavior or build the overcast panel (Phase 2), to keep this a light, reversible pass.
- Did not attempt to resolve the original RP contradiction by averaging or picking the "newer-looking" table — the owner's Hybrid-B ruling explicitly specifies which pieces of each model carry over.

### Overnight waves 1–5 (2026-07-29 — see `docs/mechanics/OVERNIGHT_HANDOFF.md` for owner skim; `OVERNIGHT_PROGRESS.md` for file touch lists)

**Wave 1 (core mechanics & chargen)**
- **Drow → Umbrin player-race rename OK'd** (interim Umbral Elf superseded same-night by direct owner direction) — see item #3 above. Full sync across `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `character-storage.js` legacy alias, bestiary, continuity docs. Draft lore stub: `docs/mechanics/UMBRIN_LORE.md`.
- **Resonance/RP economy wired end-to-end** — reputation modifiers, Retune/Full rest, overcast/Burnout stub; party RP pool from per-PC max. Canon doc: `docs/mechanics/RESONANCE_CANON.md`.
- **L11–20 full 17-class coverage** in `class-draft-levels.js` (Oracle/Paladin/Wizard gap-filled; draft-flagged where not rulebook-sourced).
- **Dungeon `entryClasses` / `victoryConsequences` draft-filled** — all 17 eligible; 10 tier consequences; `DungeonGuide.tsx` updated. Closes `CONTINUITY_REPORT.md` ASK OWNER #5.
- **Gravetouched ASK OWNER #6 closed as false escalation**; **cosmology XIV vs dungeon (ASK OWNER #7) — dungeon wins** (XIV marked superseded).
- Prestige feat cross-check: 0 missing (53 refs).

**Wave 2 (playtest smoke)**
- `docs/mechanics/PLAYTEST_SMOKE.md` — 15-min smoke path. **Load in Session** fix (Encounters/Generators → SESSION tab). Build + typecheck clean.

**Wave 3 (collaborator day 1)**
- `docs/mechanics/COLLABORATOR_DAY1.md` — onboarding read → smoke → Umbrin lore + Resonance canon skim.
- Multiclass Builder UI (secondary class + level); Generators People spark; Cosmology Key terms panel.

**Wave 4 (author-draft consistency + math)**
- **HP import:** `class-hit-dice.js` (Ch3 HD) → `estimatePcMaxHp()` in `session-utils.ts` (closes VQ-09).
- **Multiclass RP merge:** `mergeMulticlassMaxRp()` in `resonance-economy.js`; Builder/Sheet/Session multiclass-aware (closes VQ-12; formula still `draft: true`).
- Oracle Ancestor charge-cost fix; Paladin Vengeance/Flame L20 `finalOathGift` drafts; `CharacterSheet.tsx` secondary-class + oath progression display.

**Wave 5 (legacy root scrub)**
- `index.html` + `game-data.js` synced to **Umbrin** (closes VQ-27 — last product-path Drow strings outside `src/`).

**Overnight exit criteria:** No new ASK OWNER items opened. All prior open items (#1–#7) resolved or closed. Vague queue P0 = 0, P1 = 0 (`OVERNIGHT_VAGUE_QUEUE.md`). `npx tsc --noEmit` clean after every code touch. No commits (per owner request).

**Escalation reminder for all lanes:** if you hit a lore/terminology conflict, escalate to Continuity. If you hit a scope/priority conflict or need acceptance for draft/data work, escalate to the Director (Director OK gate). If neither Continuity nor the Director can decide, it goes to the human owner via the parent chat — check back in with `docs/mechanics/OVERNIGHT_HANDOFF.md` first thing. Do not invent product policy, class roster changes, or lore resolutions in the meantime.
