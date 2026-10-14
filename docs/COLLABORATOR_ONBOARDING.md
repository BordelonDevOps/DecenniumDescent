# Decennium Descent — Collaborator Onboarding

**Audience:** New writers, designers, and playtesters joining the TTRPG companion project.
**Read this first**, then `MECHANICS_ROADMAP.md` (what to work on) and `MECHANICS_BIBLE_STUB.md` (how the core systems fit together).

---

## 1. Chain of command (read before writing anything)

1. **Lore or terminology conflict?** (e.g. "does the Choir contradict the Echo Court," "is this a Spiral term or a First Song term") → escalate to **Continuity**.
2. **Scope or priority conflict, or ready to land draft/data work?** (e.g. "should I fix this now or is it someone else's lane," "is this ready to treat as accepted product content") → escalate to the **Director** for scope *and* for **Director OK** on routine `src/data/*` / docs changes (see §2).
3. **Neither Continuity nor the Director can decide, or it touches product policy / class roster / a genuine lore contradiction in the source rulebook itself / an open ASK OWNER item?** → it goes to the **human owner**, relayed through the parent chat. The Director's status reports always carry a running "ASK OWNER" list — check `MECHANICS_ROADMAP.md`'s Director Status block before assuming an answer.

**If you don't know — stop and ask.** Do not invent product policy, add or remove a class, resolve a lore contradiction, or silently pick between two conflicting rules text passages. Flag it and move to something else while you wait.

---

## 2. How changes get in

New writers and designers **may propose and draft** in `src/data/*` and `docs/`. That is not unrestricted direct ship — content counts as **accepted for the product** only after this gate:

1. **Draft** — make the change locally; keep `draft: true` on provisional entries (see §5).
2. **Continuity check** (if lore or terminology) — run past **Continuity** when names, cosmology, or canon wording are involved.
3. **Director OK** — the **Director** (project director agent / director liaison in chat) reviews and OKs routine draft/data work.
4. **Merged / accepted** — once Director OKs, the change is treated as accepted for the companion (still subject to any open ASK OWNER policy items).

**Human owner** is only required for **ASK OWNER** escalations — not for every data edit.

---

## 3. Source of truth

| Question | Answer |
|----------|--------|
| What's canon? | The **player rulebook** (`decennium descent player rulebook.docx` / its text extract `rulebook_output.txt`) and lore docx files are canon. `src/data/*` is the *implementation* of that canon — when they disagree, the rulebook wins unless a continuity pass has explicitly logged a correction (see `src/data/CONTINUITY_REPORT.md`). |
| Where does the live app read data from? | `DecenniumDescent-main/src/data/*.js` and `*.json`. This is what the Next.js companion actually renders — not the root-level `game-data.js`, `script.js`, `ENHANCED-FEATURES.JS` (legacy, unwired, do not edit for new features). |
| What's already been audited? | `src/data/CONTINUITY_REPORT.md` (terminology, class roster, Oracle/Paladin/Druid, prestige↔feats, cosmology↔dungeon, save-shape checks) and `src/data/CONTENT_GAPS.md` / `content-gap-report.json` (structured gap list with `draft`/`status`/`priority` per item). Read both before starting any task — you may find your assigned gap already has notes. |
| What's the current roadmap? | `docs/MECHANICS_ROADMAP.md` — phased, lane-assigned (A/B/C), status-tagged. |

---

## 4. The 17 canon classes

**v1 ships 17 base classes per Classes Table.**

Source of truth: `src/data/canon-classes.js` (`CANON_CLASSES` array), derived from the rulebook's Ch3 Classes Table (`rulebook_output.txt` lines 861–877).

```
Bard, Cleric, Crimson Agent, Dragoon, Druid, Mage, Monk, Mirrorsage,
Oracle, Ranger, Shaman, Soldier, Thief, Tinker, Warrior, Wizard, Paladin
```

**Do not add an 18th class.** The rulebook's intro prose says "eighteen" — this is a confirmed book typo; the 17-row Classes Table is authoritative and **final for v1** (owner-confirmed 2026-07-29). Two classes exist in data files but are **intentionally not selectable**:

- **Fighter** — full rulebook chapter exists, kept as archive/reference; Warrior/Soldier cover martial roles in the live roster.
- **Swashbuckler** — orphan entry in `class-details.js` only, no rulebook chapter; never expose in any picker.

If you think one of these should be revived, that is a roster-change question — **ask the owner**, don't just re-add it to a picker.

---

## 5. Draft flags — how to read and review them

Many data files use a `draft: true` flag (or prose noting "Aethel draft" vs "rulebook canon") on individual entries, e.g. in `oracle-mysteries.js`, `oracle-curses.js`, `paladin-oaths.js`, `class-draft-levels.js`. This means:

- **Rulebook canon** (no `draft` flag, or explicitly noted as sourced from the docx/rulebook): treat as final, don't rewrite without a source-backed reason.
- **`draft: true`**: this is Aethel-flavored content authored to fill a gap the rulebook itself doesn't cover in full (e.g. 9 of 10 Oracle mysteries only have a name in the rulebook, not a full tier tree). It is **playable now** but **not yet author-approved as permanent canon**. The UI already surfaces "(draft)" labels where relevant — don't remove those labels without also resolving the underlying gap.
- **To promote a draft to canon:** cross-check against the matching source docx (see the source doc inventory in `CONTENT_GAPS.md`), revise if needed, then remove the `draft: true` flag and note the change in a continuity pass. This is normal Lane B/C work, not an owner escalation — unless your review finds the draft actually contradicts something in the rulebook itself, in which case it becomes a Continuity question.
- **Never promote a draft to canon by just deleting the flag without review.** That silently ships unreviewed content as if it were the rulebook.

---

## 6. What NOT to touch

- **No Unity, Unreal, or any 3D game client work.** Strategy is locked (2026-07-28): finish the TTRPG companion first; 3D only after that's solid or on an explicit user pivot. If you're asked to "just wire up a quick 3D viewer," stop and check with the Director — this contradicts locked strategy.
- **No SWTOR (Star Wars: The Old Republic) assets, models, branding, UI, or lore in the product.** Ripped SWTOR assets may exist on disk elsewhere in the workspace as *private reference only* — they must never be imported, referenced, or wired into `DecenniumDescent-main/src/`.
- **No other copyrighted-setting leakage.** If you spot Forgotten Realms / D&D-specific proper nouns (deities, established NPCs, place names) in bestiary or other data — e.g. entries referencing Lolth — do not "fix" it yourself by guessing an Aethel replacement. This is flagged as an owner decision (IP risk, not lore taste) in the current roadmap.
- **Legacy unwired files** (`game-data.js`, `script.js`, `ENHANCED-FEATURES.JS`, `COSMOLOGY-VIEWER.JS`, root `bestiary_data.json`) — don't build new features on these; they predate the Next.js app and aren't imported by `src/app`.
- **Don't silently resolve the Resonance Points contradiction** described in `MECHANICS_ROADMAP.md` Phase 1 / Director Status #1. Two incompatible spellcasting-economy rules exist in the rulebook itself. This is an owner decision — implement nothing beyond the current flat placeholder until it's resolved.

---

## 7. How to review draft Oracle / Paladin / Druid content specifically

These three classes have the deepest draft content and the most active author-review needs:

- **Oracle** (`src/data/oracle-mysteries.js`, `oracle-curses.js`): Ancestor mystery + Spiral-Touched curse are rulebook-canon (full tier trees exist in the source). The other 9 mysteries and 9 curses are Aethel-authored draft trees. Review against `rulebook_output.txt` Ch3 Oracle section for tone/name consistency; there is no docx source for the missing 9 — this is original content pending author sign-off, not a transcription task.
- **Paladin** (`src/data/paladin-oaths.js`): Mercy oath is fully rulebook/docx-sourced. The other 9 oaths have draft revelation spell lists — cross-check against `Paladin_Oaths_Core.docx` and `Paladin_Oaths_Oathbreaker_Revised.docx` when doing a promotion pass; these docx files likely have more detail than what's currently wired.
- **Druid** (`src/data/druid-shapeshifting.js`, `class-paths.js` circles): Circle structure (7 circles) is wired and cross-referenced with class-paths; `Druid_Shapeshifting_System.docx` is the source for Arch Druid Forms/CR tables — spot-check current data against it if expanding.

For all three: if a review turns up a contradiction with the rulebook's Classes Table or Ch3 text (not just "missing detail"), that's a Continuity escalation, not something to silently overwrite.

---

## 8. Where things live (quick map)

```
DecenniumDescent-main/
  rulebook_output.txt              ← canon rulebook text extract (search this first)
  *_EXTRACT.txt                    ← cosmology / world lore extracts
  src/data/
    canon-classes.js               ← the 17-class source of truth
    class-details.js               ← per-class armor/weapons/skills/level features
    class-paths.js                 ← arch (L3–9) & hero (L10+) skill trees
    class-draft-levels.js          ← L11–20 fill-in (mostly draft)
    oracle-mysteries.js / oracle-curses.js
    paladin-oaths.js
    druid-shapeshifting.js
    prestige-lorebook.json         ← 18 prestige paths
    feats.js                       ← 336 feats
    spells.js                      ← 832 spells
    backgrounds.js                 ← 20 backgrounds
    races.js / builder-races.js / racial-variants.json
    dungeon-mechanics.json         ← horn clock, cycle, gate bosses, prestige unlock rules
    floor-encounters.json          ← 10 tiers, havens/POIs/bosses
    cosmology-lore.json            ← planes, First Song, world sections
    crafting-recipes.json          ← 623 recipes
    CONTINUITY_REPORT.md           ← latest audit (read this)
    CONTENT_GAPS.md / content-gap-report.json  ← structured gap tracker (read this)
  src/lib/character-storage.js     ← saved-character shape + normalization
  src/components/                  ← CharacterBuilder, CharacterSheet, SessionTracker,
                                       DungeonGuide, CosmologyViewer, SpellsLibrary,
                                       MonstersLibrary, ItemsLibrary, CraftingBuilder,
                                       EncountersBrowser, GeneratorsPanel
  docs/                            ← this doc + MECHANICS_ROADMAP.md + MECHANICS_BIBLE_STUB.md
```

---

## 9. First-week checklist for a new collaborator

1. Read this doc, then `MECHANICS_ROADMAP.md`, then `MECHANICS_BIBLE_STUB.md`.
2. Read `src/data/CONTINUITY_REPORT.md` and `src/data/CONTENT_GAPS.md` in full — most "obvious" questions are already answered there.
3. Find your lane (A/B/C) in `MECHANICS_ROADMAP.md` and pick a `draft` or `missing` item scoped to it.
4. Before touching Oracle/Paladin/Druid draft content, re-read section 7 above.
5. If your task needs a decision not covered by the docs — **stop, write down the exact question, and escalate** (Continuity for lore, Director for scope and Director OK, owner only for ASK OWNER policy). Don't guess and ship.
6. When your draft is ready, request **Director OK** before treating it as accepted product content (see §2).
7. When done, note what you changed and why in a short update to whichever gap doc tracked the item (follow the existing `CONTINUITY_REPORT.md` format).
