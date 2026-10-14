# A-to-Z Mastery Digest — Decennium Descent

**Purpose:** A single trustworthy pass over everything currently in the repo, written for the product owner. Every claim below is cited to a file. Nothing here is invented — where the repo is silent, ambiguous, or self-contradictory, it is flagged as such rather than resolved.

**Date:** 2026-07-30  
**Continuity process (2026-07-30):** Agents must open Player Rulebook + DM Manual extracts before auditing; see [`CONTINUITY_SOURCE_OF_TRUTH.md`](../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md). No file named "DM Manual" on disk — Matrix, Cosmology, World of Aethel, and Floor Encounters docx/extracts form the GM layer.
**Workspace read:** `C:\Github\Descent assets\DecenniumDescent-main` (product), skimmed `C:\Github\Descent assets` root for lore-only folders (none found outside `DecenniumDescent-main` — `readmes/`, `swtor/`, `extracted/`, `art/`, `Assets/`, `Movies/`, `EUALAs/` are SWTOR install/rip artifacts and are **not** product canon per the locked strategy rule).

---

## 1. Inventory — what was actually read

### Cosmology / lore (read in full or near-full)

| File | Coverage |
|---|---|
| `The Decennium Descent and the Matrix of Oblivion.docx` | Read via its verified extract (docx is binary; extract is byte-verified against `document.xml`) |
| `docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md` | Full (746 lines) |
| `docs/mechanics/SILENT_ONES_CANON.md` | Full |
| `docs/mechanics/DESCENT_WINDOW_CANON.md` | Full |
| `docs/playtest/DUNGEON_CREATION_PURPOSE.md` | Full |
| `docs/mechanics/WORLD_DUNGEON_LOOP.md` | Full |
| `docs/mechanics/UMBRIN_LORE.md` | Full |
| `docs/mechanics/RESONANCE_CANON.md` | Full |
| `The_Cosmology_of_Decennium_Descent_EXTRACT.txt` | Read Chapters I–III in full, IX–XII in full; skimmed IV–VIII via citations in `DUNGEON_CREATION_PURPOSE.md` (324 lines total, ~282KB — see Gaps) |
| `The_World_of_Aethel_Lore_EXTRACT.txt` | Full (69 lines) |
| `docs/playtest/HIDDEN_DUNGEON_EQUATION.md` | Full |
| `src/data/dungeon-mechanics.json` | Full |
| `src/data/floor-encounters.json` | Full |

### Product locks / continuity (read in full or near-full)

| File | Coverage |
|---|---|
| `.cursor/rules/ttrpg-first-strategy.mdc` | Full (always-applied rule) |
| `docs/mechanics/CONTINUITY_DETAILED_CHECK.md` | Full |
| `src/data/CONTINUITY_REPORT.md` | **Partial** — header, Watchlist, ASK OWNER table, Gates A–G table of contents, "Remaining tensions," and the newest stamps (2026-07-30) read; the ~2,350-line wave-by-wave history (waves 1–123) was **not** read line-by-line (see Gaps) |
| `src/data/CONTINUITY_GLOSSARY.md` | Full |
| `docs/mechanics/AUTHOR_REVIEW_QUEUE.md` | Full |
| `docs/MECHANICS_ROADMAP.md` | Full |
| `docs/MECHANICS_BIBLE_STUB.md` | Full |
| `docs/COLLABORATOR_ONBOARDING.md` | Full |
| `src/data/CONTENT_GAPS.md` | Full |

### Companion systems (enough to be fluent)

| File | Coverage |
|---|---|
| `docs/mechanics/SESSION_LOOP.md` | Full |
| `docs/mechanics/XP_ADVANCEMENT_CANON.md` | Full |
| `docs/mechanics/CLASS_CEILING_CAPS.md` | Full |
| `docs/mechanics/RULESET_VULNERABILITIES.md` | Full |
| `docs/mechanics/REPUTATION.md` | Full |
| `docs/mechanics/RACE_CLASS_SYNERGY_REPORT.md` | Full |
| `docs/mechanics/BESTIARY_INGEST.md` | Full |
| `src/data/prestige-lorebook.json` | Full (18 prestige paths) |
| `src/data/races.js` | Partial (first ~80 of ~300 lines — enough to confirm Umbrin entry and data shape) |
| `rulebook_output.txt` (1.57MB) | **Grepped only** — searched for `Old Ones`, `Silent Ones`, `Matrix of Oblivion`, `Weave of Aethel`: **zero matches**. This confirms the player rulebook text is mechanics-only; the deep cosmology narrative lives exclusively in the separate cosmology docx/extract and the Matrix docx (see Gaps for what wasn't grepped) |

**Approximate total: ~35 primary sources read in depth**, plus directory listings across `docs/`, `src/data/`, and repo root to confirm what exists.

---

## 2. Cosmology spine

### 2.1 The public myth layer — Spiral, Weave, First Song, Divine Pact

Source: `The_Cosmology_of_Decennium_Descent_EXTRACT.txt` Ch. I–III, cross-referenced by `docs/playtest/DUNGEON_CREATION_PURPOSE.md`.

- **The Great Stillness** — the pre-creation state; not void, not brilliance, just undifferentiated totality (`The_Cosmology...EXTRACT.txt` Ch. 1).
- **Lumina** and **Umbra** — the first two "gestures" born from a hairline crack in the Stillness: Lumina reaches outward (revelation), Umbra folds inward (shelter). Their tension births **the Weave**, a lattice of tension/resonance.
- **Calan'thir** — coalesces out of the Weave as its warden; "one continuous song of calibration," not a being with a face or crown. Founds **the Spiral** — a corridor of recurring resonance that gives the cosmos duration and memory.
- **The Old Ones** — a "collective dreaming," pressure from beneath the Weave that wants to return everything to the silence that preceded creation. Not conquerors — they diagnosed that *all suffering requires difference*, so they seek to erase difference itself. **This is philosophically identical to, and the direct source of, the Matrix of Oblivion equation** described later in the Matrix docx.
- **Asmodeus** — steps out of a rift Calan'thir opens; "architect of law and consequence." Partners with Calan'thir to seal the Old Ones' dreaming beneath a "living perimeter" that must stay in motion (song + edge) or the seal loosens.
- **The Crucible** — the corridor/labyrinth Calan'thir and Asmodeus build around the seal, "caging potential" through trial rather than imprisoning bodies. **"Later scholars would call this labyrinth the Dungeon, though in this dawn it was known only as the Crucible."** This is the primordial ancestor of the playable Great Descent.
- **The Sundering** — Asmodeus, hungry for a decisive "verdict" rather than endless balance, leads a demonic host against the Spiral; Calan'thir summons **the Choir** (seven virtues: Courage, Balance, Law, Sorrow, Pattern, Contradiction, Transition) to hold the seal. The **Old Ones' dreaming coalesces into a singular identity, Ul'nak**, who nearly breaches the seal mid-battle; only a fused chord of Choir virtue + Asmodeus's disciplined fire reseals it (Ch. III).
- **The Divine Pact** — the negotiated outcome: Asmodeus is exiled to found Hell (the Nine Hells, devils vs. demons as an externalized, permanently-running discord-generator that also feeds the seal from a safe distance). **This is the origin of "the Pact" as a term** — later texts (Matrix docx, Silent Ones lock) use "the Divine Pact" and "the PACT" as if they are the same institution; the repo does not explicitly confirm they are identical (see §8 Contradictions).
- **Resonance** — the in-fiction cosmological principle (not to be confused with the player-facing spellcasting system of the same name, §5) is defined via ten interconnected terms in the Matrix docx: **Possibility → Choice → Difference → Conflict → Motion → Time → History → Identity → Will → Life**. So long as meaningful distinction exists, resonance stays above zero, and the seal holds.

### 2.2 The Matrix of Oblivion (public/mortal-facing dungeon-purpose text)

Source: `The Decennium Descent and the Matrix of Oblivion.docx` via `docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md`.

- **The dungeon "was created to prevent peace"** — not political peace, but the *absolute* peace of a universe where nothing moves, changes, or differs — a state the text calls **Oblivion**.
- The dungeon is **"a resonance valve constructed above the prison of the Old Ones... a living firewall."**
- **The Hundred Floors / Ten Tiers** map directly onto the ten resonance principles (Tier 1 = Possibility ... Tier 10 = Life). Each tier's Gate Guardian "regulates one portion of the dungeon's resonance system."
- **The Imprisoned Old God** sits between Tiers 7–8 (History/Identity boundary) — its persistence *after* memory is stripped is framed as proof the Matrix of Oblivion's core assumption (identity = memory) is incomplete.
- **The Matrix of Oblivion equation** is the Old Ones' formal argument: reverse the ten principles to zero (`PCDKMTHIWL → 0`) and suffering ends because nothing remains distinct enough to suffer. The docx renders this as intentionally corrupted/incomplete math (bracket placeholders like `[ = ]`, fragments like `PCDKM THIWL`, `x_i=0`, `G_n`) — **the extract explicitly instructs: "Do not infer missing symbols."** This is a deliberate authorial choice, not an extraction failure.
- **The Flaw in the Matrix** — living reality is not a closed system; it generates a spontaneous "source term" (new choices, new memories, mutations) that the Old Ones' model can't account for. The counter-proof is called **the Spiral Integral** — the idea that any state of total silence instantly seeds a new question, so the zero-state (Oblivion) can never be permanently maintained.
- **The First Completion** — for ages no mortal reached Floor 100. When one finally did and returned carrying "awareness" of the Old Gods' Unity, the dungeon recognized the breach and **rewrote itself** — becoming actively reconfiguring rather than static. The **Dungeon Warden** (custodian of the Divine Pact, not its sovereign) became active from this point, and **automatons** are its enforcement arm — they "protect the system," not individual adventurers.
- **Why it opens every ten years** — continuous access would make the dungeon routine and predictable, which *reduces* resonance; the decennial cycle guarantees each opening is a fresh "worldwide crisis of possibility."
- **The Economy of the Descent** — kingdoms, temples, scholars, goblin financiers, infernal contract-brokers, and multi-generational family quests are explicitly described as *part of* the resonance engine, not incidental to it. Greed and devotion both count.
- **The Final Paradox** — the text's own moral thesis: the Old Ones offer "peace without suffering by eliminating the sufferer"; the Divine Pact "preserves the sufferer while accepting that suffering can never be eliminated completely." Neither side is framed as simply good or evil.

### 2.3 The GM-secret stratum — Silent Ones (owner lock, 2026-07-30)

Source: `docs/mechanics/SILENT_ONES_CANON.md`, cross-linked from `docs/playtest/DUNGEON_CREATION_PURPOSE.md` and `docs/mechanics/DESCENT_WINDOW_CANON.md`.

This is a **separate, secret layer laid on top of** everything in §2.1–2.2, added by direct owner directive on 2026-07-30. Four locked statements:

1. **No one knows about the Silent Ones** — secret from the world and from typical PCs. This must never appear in player-facing or newcomer-guide content as known fact.
2. **The Silent Ones made the dungeon with loot** specifically to attract people, so that those people will discover and **release** them.
3. **The PACT wants to keep them silent** and deliberately entices **war as dissonance** — and **this is where the Matrix of Oblivion is centralized.**
4. **If the world knows peace, the Old Ones awaken to silence the universe again.**

**Round 2 (2026-07-30, same date):** the owner directly answered the open questions these four statements raised — **Silent Ones = Old Ones (same entity)**; **The PACT = the Divine Pact (confirmed, no rename)**; and a full public/secret authorship split (Calan'thir & Asmodeus as real public builders atop the Silent Ones'/Old Ones' pre-existing **Heartcell** machine). See §8 items 1–3, 7 below and [`OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](../mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md) for full quotes.

The repo's continuity docs map "The PACT" to "the Divine Pact" from §2.1 **only provisionally** ("unless owner renames") and explicitly refuse to collapse "Silent Ones" and "Old Ones" into one identity, one nested relationship, or two distinct powers — **this is the single largest open lore question in the repo** (see §8).

A layer model is given (`SILENT_ONES_CANON.md` §3):

```
[ GM-secret ]     Silent Ones built dungeon + loot → attract → discover → release
[ Pact layer ]    Keep them silent; war as dissonance; Matrix of Oblivion centralized
[ Public myth ]   Calan'thir / Asmodeus / Divine Pact; Crucible; resonance valve
[ Mortal belief ] Treasure, trial, divine war through mortals
```

Typical PCs and surface kingdoms operate at the bottom two layers only.

### 2.4 Dungeon purpose — reconciliation across all layers

`docs/playtest/DUNGEON_CREATION_PURPOSE.md` is the authoritative synthesis document; it holds five distinct claims about "who built it and why" in explicit tension rather than merging them:

| Layer | Who built it | Why | Source |
|---|---|---|---|
| **A. Primordial creation** | Calan'thir + Asmodeus, First Seal | Keep Old Ones' hush sealed via endless striving | Cosmology Ch. 1 |
| **B. Cosmic function** | (same) | Mirrors cosmic tide; teaches "unity through conversation among powers that refuse to yield identity" | Cosmology Ch. IV |
| **C. Mortal era** | Shardspire (unclear who built *it* specifically) | Playable Great Descent; Cycle victor reshapes the world | World of Aethel §VII/XII |
| **D. Post-Shardfall** | — | "The Spiral is now tuned to mortals" — mortal choice becomes cosmic input, not just a loot run | Cosmology Ch. Ten |
| **E. GM-secret** | The Silent Ones | Loot as bait → discovery → release; Pact keeps them silent via war | Owner lock 2026-07-30 |

The doc's one-paragraph plain synthesis (quoting directly): *"The dungeon begins as the Crucible — a First Seal work of Calan'thir and Asmodeus to keep the Old Ones' silence from unravelling the Spiral... The Shardspire opens that pattern to mortals every ten years... Owner lock (GM-secret): beneath public myth, Silent Ones (unknown to the world) built the dungeon with loot as bait to be discovered and released; The PACT keeps them silent via war as dissonance (Matrix centralized); peace risks Old Ones awakening to silence the universe."*

**Explicit gaps this document itself flags as unauthored:** who/what built the Shardspire specifically; why exactly 100 floors/10 tiers; the horn's in-world origin story; the owner's still-unpublished "hidden equation and counterpoint."

### 2.5 Cycle, opening window, and the horn — two clocks, not one

This is a resolved owner lock as of 2026-07-30 (`docs/mechanics/DESCENT_WINDOW_CANON.md`), and it is important enough to restate cleanly:

| Clock | Duration | Scope | Companion wiring |
|---|---|---|---|
| **Decennial opening window** | **100 days = 2400 hours** | Macro/Cycle — how long the Great Descent accepts new entrants after the Shardspire activates, before it seals for another decade | Session tracks Opening hours; seal at 2400 h |
| **Horn (PoNR)** | **1200 hours / day 50** | Midpoint of the Opening — point of no return | **Wired** — `hornRule`; Session `HORN_AT = 1200` |
| **Soft quit** | Floor 50 Canticle | Morale / expedition end — **≠** Horn | Dungeon Guide / Codex |

- Opening and Horn are **one calendar clock** with a day-50 milestone. Soft quit at Floor 50 Canticle is separate.
- Continuity: early drafts briefly used **240/120** — typo; corrected to **2400/1200** (2026-07-31). See [`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md).
- At the end of the Opening, survivors are "not necessarily killed" — they may be trapped until the next opening/Cycle.

---

## 3. World / dungeon structure

### 3.1 Ten tiers, one hundred floors

Source: `src/data/floor-encounters.json`, `src/data/dungeon-mechanics.json`, `docs/mechanics/CONTINUITY_GLOSSARY.md`.

| Tier | Floors | Zone | Gate Boss | Content status |
|---|---|---|---|---|
| 1 | 1–10 | Yieldheart Caverns | Vaskor, the Stone Maw | **Mapped** — full haven/POI prose |
| 2 | 11–20 | Bloomdeep Marsh | The Bloom That Hungers | **Mapped** |
| 3 | 21–30 | Anvil of Brogi | Ashthirst the Hollow | **Mapped** |
| 4 | 31–40 | Isles of Eternal Radiance | Gor Vekk, Architect of Ends | **Mapped** |
| 5 | 41–50 | Sanctum of Echoing Choirs | Choralith, Voice Below | **Mapped** — "where the overwhelming majority of expeditions end" |
| 6 | 51–60 | Crossroads of the Shattered Thread | Lumen of the Shattered Thread | **Draft/rumor stub** |
| 7 | 61–70 | Pactbound Arena | Xarog, the Pactbound Furnace | **Draft/rumor stub** |
| 8 | 71–80 | Duskshard Pools | Eirfax, the Dusk Crowned | **Draft/rumor stub** |
| 9 | 81–90 | Veiled Iron Spiral | Threxus, the Iron Spiral | **Draft/rumor stub** |
| 10 | 91–100 | Silencebound Void | The Marquis of Silence | **Draft/rumor stub** |

- Tiers 1–5 have full narrative (from `Floor Encounters.docx`) with named havens (e.g. **Crystalfront Market**, **Bar of Last Refuge** at Floor 43 — explicitly the game's "point of no return" narrative pressure valve) and points of interest with puzzle-gated tier gates (Warded Gate, Sporemist Gate, Lavaflow Gate, Radiance Gate, Canticle Gate).
- Tiers 6–10 are **explicitly labeled `mapped: false`, `draft: true`** — survivor-rumor GM seeds only (region names, hazards, a gate-boss seed, an encounter vibe). No routes, maps, HP, tactics, or resolution rules exist for them. Notably these seeds do selectively weave in Umbrin geography (Quiet Deep at T6/T10, Blackglass Reach at T7, Veyr-Obsid at T8, Murk iron-guild slang at T9) without forcing it onto every tier.
- **Floor 97** holds **the imprisoned Old God** (an "eleventh, unnamed and unclaimed shard" that tried to consume the Pantheon in 666 AE) — this is flagged in multiple docs as an unresolved seam against the clean 10-floor-per-tier structure (see §8).
- **Tier 5's "Bar of Last Refuge"** is called out repeatedly as the de facto narrative stopping point for most tables — worth knowing for session pacing even though nothing mechanically forces it.

### 3.2 Cycle mechanics

Source: `src/data/dungeon-mechanics.json`.

- **Calendar:** 400-day year, 10 months × 40 days; the 10th of each month is a Holyday; the final 10 days of the year are **Twilight Week**, when "divine and mortal boundaries blur."
- **Rotation:** 10-year cycle; the **Shardspire** activates in the tenth year; each Cycle is named after its victor (whoever holds the deepest gate they cleared when the horn sounds for the last time before the tenth year turns).
- **Victory consequences** are drafted per-tier (e.g. Tier 1 victory reopens/revokes automaton labor charters; Tier 10 full victory names the new Cycle and elevates Hush Beneath the Song patronage) — explicitly `draft: true`, Director-authored flavor, not rulebook-sourced.
- **Entry classes:** all 17 canon classes are eligible to attempt entry — also `draft: true`, filled by Director default because no rulebook chapter was found restricting entry by class.
- **Myth-history timeline** (`dungeon-mechanics.json.timeline`): 0 AE Fracturing of the First Light → 87 AE First Cycle begins (a farmer emerges with a crown of flame, founding Tyrnathar — "the advent of divine war through mortals") → 301 AE Betrayal of the Veil (a relic vanishes into the dungeon, permanently altering its structure) → 666 AE Imprisonment of the Old God → 710 AE current Cycle begins.

### 3.3 Expedition structure

Source: **`rulebook_output.txt` § Expeditions in Aethel (lines 3801–3926)** · [`EXPEDITION_STRUCTURE_CANON.md`](../mechanics/EXPEDITION_STRUCTURE_CANON.md) (owner lock 2026-07-30) · `src/data/dungeon-mechanics.json` · `docs/mechanics/SESSION_LOOP.md`.

- Expeditions can field **up to 12 characters**, split across five team types: **Combat** (4–6), **Reconnaissance** (1–3), **Research** (1–3), **Resource** (2–4), **Support** (1–3) — across morning/afternoon/evening time periods. RAW includes skill checks, activity results, three worked examples, base camps, advancement, and parallel resolution methods — **organizational structure, not combat party size**.
- Companion JSON holds **structure subset only**; full prose is rulebook-sourced. Session UI currently assumes the combat table exclusively; there is no wired mechanic for team assignment or off-rotation outcomes per period.
- **Playtest drift:** T4 sims used **24 PCs (3×8)** as a director coalition stress test — **not RAW**; campaign sims used **7–8 PCs** (valid under cap). See [`EXPEDITION_STRUCTURE_CANON.md`](../mechanics/EXPEDITION_STRUCTURE_CANON.md) §6.

### 3.4 Civilizations and known settlements

- Tiers 1–6 host established small civilizations — described as "among [the dungeon's] most effective resonance generators," not accidental contaminants (Matrix docx).
- Named settlements/zones with prose: Crystalfront Market, Yieldheart (also named as the neutral concord-forge city in the cosmology extract's Mortal Crucible chapter — **possible naming overlap with Tier 1's "Yieldheart Caverns"**, not explicitly reconciled — see §8), Rootlight Sanctuary, Lurkwell Refuge, Emberrest Alcove, Gearspark Forge, Sunward Terrace, Dawn's Refuge, Bar of Last Refuge, Cantor's Archive.
- The Umbrin homeland (The Murk, Veyr-Obsid, Blackglass Reach, the Quiet Deep) is a separate underworld region layered onto the deeper draft tiers — see §4.

---

## 4. Peoples & conflicts

### 4.1 Races — data shape

Source: `src/data/races.js` (partial), `docs/mechanics/RACE_CLASS_SYNERGY_REPORT.md`, `docs/mechanics/CONTINUITY_GLOSSARY.md`.

- **14 parent races**, **45 subrace variants** in the builder, **42 enriched rows** in `racial-variants.json` (3 Drakari variants use parent-race fallback data — a known small gap).
- Confirmed races glimpsed directly: Amphibian, Umbrin, Drakari (Flame/Stone/Gale/Wave subtypes implied).
- **Cosmology-only races** (Eldrin, Dreadborn, Wyrmkith, Hollowforged, Duskwalkers — from `The_World_of_Aethel_Lore_EXTRACT.txt` §VIII) are **intentionally excluded from the player character builder** per an existing gap ticket — they belong to a different, older pantheon-driven world-lore layer (see §8 on the Velkyrion/Zeharra/Kharix pantheon) and are not currently reconciled with the playable race roster.

### 4.2 Umbrin — full canon lock (owner, 2026-07-30)

Source: `docs/mechanics/UMBRIN_LORE.md`, `docs/mechanics/AUTHOR_REVIEW_QUEUE.md` §1–2.

- **Who they are:** obsidian-skinned elves of **The Murk**, exiled rather than surface-dwelling. Name echoes **Umbra** (the primordial abyssal depth from cosmology Ch. 1) but Umbrin are mortals — "a culture, not the deity." Speak Murkish + Common + Elvish.
- **Origin — the Obsidian Burn:** Umbrin forebears drew too close to Umbra's thread and refused Calan'thir's calibration; **Calan'thir and the First Choir judged them unfit for the light** and banished them into The Murk. Flesh that had known Lumina's glare cooled to an obsidian sheen. Many Umbrin wear this as proof Umbra's depth survived Choir judgment, not as shame alone.
- **Geography (locked, not open for further proposals):** **The Murk** (broad region/approach) → **Blackglass Reach** (surface/near-Murk marches) → **Veyr-Obsid** (primary Umbrin city, dark-glass metropolis of rival houses) → **the Quiet Deep** (deeper underworld beyond mapped Murk routes).
- **Faith split:** **Choir orthodoxy** treats shadow as serving the song when *bounded*; **Murk Umbra cults** invert this — "abyss as liberation... not balance" — and are explicitly heretical, not mainstream. Cleansing Orders and Anti-Cult Alliances hunt cult bleed on the surface.
- **Reputation:** default Disliked/Hated from Aethel Authorities, mainstream religious orders, and common folk — but **not universally blocked**; "strange alliances" (transactional, not redemptive) exist with the Underworld, Planar Trading Guilds, Corruption Scholars, and even Anti-Cult Alliances when a shared enemy aligns interests. No hard-coded race-based reputation lock exists in `reputation.js` — bias is applied narratively.
- **Naming convention (locked):** personal names — Vaerith, Sythra, Korven, Zelka, Dravik, Nyssara, Kethren, Vorskai; houses — House Veyr, Ashketh, Rhal-Voss, Obis-Keth; epithets — of the Blackglass, Quiet-Step, Ash-Veiled, Deepbound.
- **Product boundary (hard rule):** use **Umbrin**, never "Drow," "Dark Elf," "Umbral Elf" (a same-night superseded interim name — do not re-ratify it), Lolth, or Underdark. Legacy character saves auto-migrate `Drow`/`Umbral Elf` → `Umbrin`.

### 4.3 The older pantheon layer (World of Aethel doc)

Source: `The_World_of_Aethel_Lore_EXTRACT.txt`.

This document describes a **full separate pantheon** (Velkyrion, Zeharra, Kharix, Elyria, Threxian, Yshael, Sythrel, Naegul, Myressa, Draethon), five named NPCs bound to those gods, a different set of playable races (Eldrin, Dreadborn, Wyrmkith, Hollowforged, Duskwalkers), a different gate-boss list (Hollow King Lv10, Cindervore Lv30, Vox Prime Lv70), and "Classes of Entry" (Champions/Heralds/Infiltrators/Wardens) that don't correspond to the 17 canon classes. **`WORLD_DUNGEON_LOOP.md` explicitly marks this gate-boss list as superseded** by `floor-encounters.json` for actual play, and treats the rest of this document as legacy/scholarly-layer content that has not been reconciled with the live pantheon-free companion. It still supplies the Cycle mechanics (calendar, 10-year rotation, Shardspire) verbatim — those parts *are* live in `dungeon-mechanics.json`.

### 4.4 Alignment / ethos notes

- The rulebook's alignment axis appears in Session UI as `PLAYER_ALIGNMENTS` (LG through CE, nine-point) — used live for Resonance school-affinity/opposition cost modifiers (§5), not a separate morality subsystem.
- The cosmology extract's Chapter XII epilogue independently proposes a **virtue-alignment table** linking each of the seven Choir virtues (Courage, Balance, Law, Sorrow, Pattern, Contradiction, Transition) to 2–3 "naturally resonant" classes, plus a homebrew "Conflict Die" mechanic for playing against type. **This is flavor-text game-master toolbox material from the cosmology novel's own epilogue, not confirmed as wired into the live companion** — worth knowing exists, not worth treating as implemented.

---

## 5. Magic & Resonance

Source: `docs/mechanics/RESONANCE_CANON.md`, `docs/mechanics/RESONANCE_MODELS.md`, `docs/MECHANICS_BIBLE_STUB.md` §2, `src/data/CONTINUITY_GLOSSARY.md`.

- **Product name: "Resonance" / "Resonance Points (RP)."** The internal ruling label **"Hybrid-B" must never appear in player-facing UI or on character sheets** — it is fine only in code comments/internal docs. "Song of the Weave" was considered and **explicitly rejected** as a product name.
- **The contradiction this resolves:** the rulebook itself contained two non-reconciled spellcasting-economy drafts — Model A (Ch3 per-class text, RP-as-disguised-slots, cost = spell level) and Model B (dedicated "Resonance System" chapter, points-buy pool, cost = spell level × 2 with modifiers, larger pools, full overcast menu). **Canon is Model B as the mechanical spine**, with Model A contributing only pool-table convention/UI framing.
- **Pool size:** set by class + level. **Rulebook-complete L1–20 tables exist only for Wizard, Mage, Cleric, Druid** (`rulebook_output.txt:6077–6099`). All 13 other Weave-casting classes use **draft** tables (Cleric curve × tier multiplier), flagged `(draft)` in UI.
- **Spend formula:** `Cost = spell level × 2 − 1 (if school "in key" with alignment) + 1 (if "dissonant") ± reputation modifier − specialization discount (0 to −3, not wired yet)`. Cantrips always cost 0; final cost floors at 0.
- **Recovery:** short rest ("retune") ≈ ¼ max pool + casting mod + Nature Circles bonus; long rest ("full harmony") = full pool; meditation (10 min, 1/day, optional) = casting mod only, **not wired in UI**.
- **Overcast/Burnout:** a menu of eight overcast options (Empowered, Extended, Widened, Heightened, Quickened, Subtle, Distant, Twinned) exists as a Phase-2 stub; Burnout triggers below 25% pool but **has no mechanical consequence beyond a warning badge** — this is flagged as a "Blocks finalize" severity item in `RULESET_VULNERABILITIES.md` (M-01).
- **Oracle is fully outside this system.** Oracle spends **Revelation Charges** (start 3, max 7, +1 every odd level) on **Mystery Revelations**, recovered via each Mystery's unique **Prophecy Trigger** — never rest-based, never called RP or spell slots. This exclusion is enforced in code (`spell-utils.js` excludes Oracle from `isSpellcasterClass()`).
- **Multiclass Resonance (approved canon, Hybrid-B, 2026-07-30):** max RP = full pool of the highest-caster-tier class + **⌈25% of one secondary Weave-caster's max pool⌉** (round up). Tertiary+ Weave classes add nothing further. Implemented in `mergeMulticlassMaxRp()`. A merged result still shows a draft badge only if one of the *contributing* class pool tables is itself draft.
- **Reputation hooks (shipped):** Arcane Guilds → ±1/±2 max RP; Religious/Academic/Nature-relevant tracks → ±1 spell cost; Nature Circles → ±1 on retune.
- **13 of 17 Weave-casting classes still run on draft (unpromoted) pool-table math** — this is a live playtest risk (`RULESET_VULNERABILITIES.md` M-03), not a cosmetic label issue.

---

## 6. Play systems (high level)

### 6.1 Session loop

Source: `docs/mechanics/SESSION_LOOP.md`, `docs/mechanics/WORLD_DUNGEON_LOOP.md`.

Intended table flow: **Set tier → track the 1200h Horn PoNR clock (+8h per long rest) → load party/foes → roll initiative → run combat rounds → track per-combatant RP/RC → rest.** The one-session GM loop is Cosmology/Cycle framing → Dungeon Guide (tier + horn) → Encounters/Generators (build the scene) → Session (horn + combat) → Items/Crafting (loot + downtime) → back to Dungeon Guide.

- Party RP pool defaults to the sum of living Weave casters' max RP.
- Gate-boss "quick add" HP is a stub formula: `40 + tier × 25` — explicitly a placeholder until real bestiary stats are pulled.
- Initiative tie-break: higher Dex → player add-order → allies before foes.
- The horn clock is **display-only** — no mechanical penalty is wired for ignoring it beyond the fiction of the 10-year trap; this is a flagged, unresolved design question (`SESSION_LOOP.md` gaps table; `RULESET_VULNERABILITIES.md` D-04).

### 6.2 Expedition / crafting / research

- 623 validated crafting recipes exist (`crafting-recipes.json`), matched to bestiary loot tiers.
- No rule ties crafting or research throughput to horn-clock hours — this is an acknowledged gap; sim/GM convention (not canon) suggests 2–4h per significant craft or research action.
- 18 prestige paths (`prestige-lorebook.json`) all use a consistent **narrative-discovery unlock model** (not a level checkbox) — e.g. Battlemage requires slaying a spellcasting foe in melee while maintaining concentration; Bloodbound requires surviving a vampiric infection and willingly accepting the blood-oath. **All 18 have `draftCapstone: true`**, and several have partial `draftHallmarkIndices` — the paths are wired and playable but their capstones/hallmarks are pending an owner tone/mechanics pass.

### 6.3 XP, death, rests

- **Confirmed rulebook canon:** the L1–L20 cumulative XP threshold table and proficiency-bonus-by-level are sourced directly from the rulebook (Ch1 "Character Advancement," paragraphs 122–130 / table rows 158–179) and are wired live in `xp-economy.js` / Character Builder.
- **Everything about *awarding* XP is unconfirmed and explicitly blocked:** no rulebook source establishes CR→XP conversion, encounter budgets, party-split rules, or whether static bestiary `xp` fields follow any real formula. A draft CR→XP table, an equal-split rule, and an easy/medium/hard/deadly budget sketch exist in `xp-economy.js` and are used by Session's "Award draft XP" button — but this writes to **scene notes only, never to a character save**, and is explicitly labeled "not canon" pending owner approval.
- **Rests:** short rest = ¼ max RP + Oracle RC +1, 0 horn hours; long rest = full RP/RC restore + 8 horn hours. HP import falls back to rulebook Ch3 hit-die formula (max die + CON at L1, average die + CON per level after) when a saved character has no stored HP.
- **Death/downed states:** HP-at-0 is shown visually in Session; there is **no death-save automation** — explicitly out of scope for now.

---

## 7. Owner locks table (dated, non-negotiable)

| Lock | Date | Statement | Source |
|---|---|---|---|
| **TTRPG-first strategy** | 2026-07-28 | Finish Decennium Descent as a complete TTRPG companion before any 3D/Unity/Unreal work; keep "just enough MMO feel"; no SWTOR assets/branding/UI in the product path; source of truth is `DecenniumDescent-main`, not asset-rip folders | `.cursor/rules/ttrpg-first-strategy.mdc` |
| **17-class roster is final for v1** | 2026-07-29 | Rulebook's "eighteen" is a confirmed book typo; the 17-row Classes Table is authoritative; Fighter (archive/reference) and Swashbuckler (orphan) are never selectable | `MECHANICS_ROADMAP.md`, `CONTINUITY_REPORT.md` ASK OWNER #2/#3 |
| **Umbrin is the final player-race name** | 2026-07-29 PM | Supersedes an interim same-night "Umbral Elf" name; do not re-ratify Umbral Elf. Locked theology (Obsidian Burn), geography (Murk → Blackglass Reach → Veyr-Obsid → Quiet Deep), and transactional-alliance posture | `UMBRIN_LORE.md`, `AUTHOR_REVIEW_QUEUE.md` §1 |
| **Resonance economy is Hybrid-B** | 2026-07-29 | Canon spellcasting economy anchors on the Model B points-buy pool; product name is "Resonance"/"RP" only; "Song of the Weave" rejected; "Hybrid-B" is internal-only | `RESONANCE_CANON.md`, `RESONANCE_MODELS.md` §6 |
| **Resonance multiclass formula approved** | 2026-07-30 | Highest Weave-caster pool + ⌈25% secondary pool⌉; tertiary adds nothing; written into the rulebook text itself | `RESONANCE_CANON.md` §7, `AUTHOR_REVIEW_QUEUE.md` §4 |
| **Mystery of Shadow + Oath of Grief promoted to canon** | 2026-07-30 | Only two of 20 Oracle-mystery/Paladin-oath drafts have been promoted; all others (8 mysteries, 9 oaths incl. Mercy, 9 curses) remain `draft: true` | `AUTHOR_REVIEW_QUEUE.md` §5 |
| **Bloodbound eligibility** | 2026-07-29 | Base classes are Crimson Agent or Thief (Lv 10+) only; Gravetouched is not a prerequisite | `CONTINUITY_GLOSSARY.md`, `CONTINUITY_REPORT.md` ASK OWNER #1 |
| **Decennial opening window = 100 days / 2400 hours** | 2026-07-30 | Supersedes a 240-hour drift/typo in the source `.docx`; distinct from and never to be merged with the 120-hour horn | `DESCENT_WINDOW_CANON.md` |
| **Silent Ones — GM-secret stratum** | 2026-07-30 | Unknown to the world/PCs; built the dungeon with loot as bait for discovery→release; The PACT keeps them silent via war-as-dissonance (Matrix centralized there); world peace risks Old Ones awakening to silence the universe | `SILENT_ONES_CANON.md` |
| **Collaborator access model — "Director OK" gate** | 2026-07-29 | Collaborators may draft in `src/data/*` and `docs/`; content is accepted for the product only after Director OK; human owner is only needed for ASK OWNER-tier policy escalations | `COLLABORATOR_ONBOARDING.md` §2 |
| **Bestiary.xlsx is the single canonical authoring workbook** | 2026-07-30 | `src/bestiary_data_full.json` is a build artifact only; never hand-edit combat there; gate guardians never auto-regenerated | `BESTIARY_INGEST.md` |

---

## 8. Open questions / contradictions (explicit)

These are drawn directly from the repo's own continuity docs — none are inferred by this digest.

1. ~~**Silent Ones vs. Old Ones — undefined relationship.**~~ **RESOLVED (owner lock round 2, 2026-07-30): same entity.** "Silent Ones ARE the Old Ones (same)." See [`OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](../mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md) Q1, [`SILENT_ONES_CANON.md`](../mechanics/SILENT_ONES_CANON.md).
2. ~~**Public builder vs. secret builder.**~~ **RESOLVED (round 2): neither cover story nor separate event.** Calan'thir & Asmodeus genuinely, publicly, jointly built the Crucible; the Silent Ones/Old Ones built a pre-existing machine (the **Heartcell**) beneath it, which Calan'thir & Asmodeus discovered/claimed/modified/activated/bound themselves to. Q3 in the round-2 lock.
3. ~~**Loot-as-bait vs. "the dungeon contradicts the Old Ones through manufactured struggle."**~~ **RESOLVED (round 2): one mechanism.** Combat resonance, death essence, gate victories, loot spreading, and conditioning are all the Heartcell's operation; loot-as-bait is the on-ramp.
4. **"The world knows peace" trigger — undefined threshold.** Political truce between two kingdoms? A cosmic resonance value dropping below some number? No definition exists. **Still open — not addressed by round 2.**
5. **Horn vs. opening window.** **RESOLVED:** Horn = **1200h / day 50 = point of no return**, inside the **2400h / 100-day** Opening — one clock with a milestone. Soft quit at Floor 50 Canticle ≠ Horn. Session `HORN_AT = 1200` and `hornRule` aligned 2026-07-31. See [`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md).
6. **240h vs. 2400h typo.** **RESOLVED** — Opening is **2400h**; Matrix / Director literature aligned. Continuity stamp: [`DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md`](../mechanics/DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md).
7. ~~**The Divine Pact = "The PACT"?**~~ **RESOLVED (round 2): confirmed identity, no rename.** '"The Pact" is shorthand for the Divine Pact — the agreement between heavens and hell manifested to keep the Old Ones hidden.'
8. **Cosmology XIV gate-boss list vs. live dungeon tiers.** `cosmology-lore.json`'s Chapter XIV names Hollow King (Lv10), Cindervore (Lv30), Vox Prime (Lv70) — **formally superseded** by `floor-encounters.json`'s Vaskor/Ashthirst/Xarog/etc. for actual play, but the superseded content is still present in the data file, not deleted. **Round 2 (Q7) makes this retirement formal**, not just a draft flag.
9. **Level 97 Old God vs. the clean 10-floor-per-tier structure.** The Old God's imprisonment at "Level 97" (from the older World of Aethel myth-history) doesn't map cleanly onto the tier-band system culminating at floor 100; `WORLD_DUNGEON_LOOP.md` flags this explicitly (WDL-4) as "treat as cosmology myth, not encounter index" — ask the owner if a floor-97 room is ever actually authored. **Explicitly asked in round 2 (Q6) and explicitly NOT answered by the owner — remains open. Do not infer.**
10. **"Yieldheart" naming collision.** Tier 1's zone is "Yieldheart Caverns"; the cosmology novel's Mortal Crucible chapter independently names a neutral concord-forge city "Yieldheart." Not flagged anywhere in the continuity docs as either a deliberate callback or an accidental collision — worth an owner glance.
11. **"Turning Spiral" naming collision.** The Oracle patron "Turning Spiral" (keepers of causality) is explicitly distinguished in the glossary from Tier 9's zone name "Veiled Iron Spiral" — flagged as a known point of table confusion, not a lore contradiction, but real enough that survivor-rumor text for Tier 9 calls out "name collision with Turning Spiral patron confuses survivor theology" as in-fiction flavor.
12. **Mercy oath — glossary vs. data drift, now resolved.** Continuity docs previously called Oath of Mercy "rulebook-canon" while the code kept it `draft: true`. This has been formally reconciled (Mercy stays draft; it was *not* promoted) as of Oversight Phase C — flagged here only so nobody re-opens it based on stale references elsewhere in the doc tree.
13. **Rulebook itself contains an unreconciled RP contradiction** (Model A vs. Model B, §5) — resolved at the product-canon level (Hybrid-B), but the raw rulebook text still contains both original passages un-flagged.
14. ~~**World of Aethel's older pantheon (Velkyrion, Zeharra, Kharix, etc.) vs. the live Calan'thir/Asmodeus/Old Ones cosmology**~~ **RESOLVED (round 2, Q7): formally retired as gate-guardian/active-pantheon names.** "Use bestiary names for gate guardians (live roster). Formally retire older Velkyrion/Zeharra/Kharix-style cosmology names where they conflict." The surrounding myth-history prose (Age of Dawns, Sundering of the Beastlands, etc.) is untouched — only the named-god-as-combat-figure usage is retired. See [`OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](../mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md) Q7.

---

## 9. Gaps — what still isn't in the repo (or wasn't reachable in this pass)

**Confirmed missing from the product itself (per the repo's own audits, not this digest's opinion):**

- No numeric formula for XP awards, CR→XP conversion, or encounter difficulty budgets — rulebook-blocked, not just unwired.
- No mechanical penalty for horn overrun beyond the fiction of the 10-year trap.
- No structured combat/effect schema for most class features or spells — combat is "descriptive, not simulatable" per `RULESET_VULNERABILITIES.md` C-06.
- Tiers 6–10 have zero authored routes, maps, encounter rosters, or rewards — rumor stubs only.
- 13 of 17 Weave-casting classes still use draft (unpromoted, non-rulebook) RP pool tables.
- 8 of 10 Oracle Mysteries, 9 of 10 Oracle Curses, 9 of 10 Paladin Oaths (including Mercy) remain draft, author-written-but-unapproved trees.
- All 18 prestige capstones remain draft; several hallmark abilities within them are also draft.
- Class ceiling caps (Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker) exist only as **informational callouts** — zero mechanical enforcement anywhere in Session or resolution.
- No wild-shape use/CR tracking in Session (Druid forms exist in the Builder only).
- Cosmology "First Song" content is a single concatenated blob with an incomplete chapter navigation index (Ch. IX–XII nav gap noted repeatedly across continuity docs).
- The owner's own promised "hidden equation and counterpoint" is explicitly **not yet uploaded anywhere in the repo** — `docs/playtest/HIDDEN_DUNGEON_EQUATION.md` is only a search report proving it doesn't exist yet, not a recovery of it.

**Not reachable / not fully read in this specific pass (agent-side limitation, flagged for honesty):**

- `src/data/cosmology-lore.json` (303KB) — the ingested/structured mirror of the cosmology extract text — was not opened directly; this digest relies on the extract `.txt` files and on continuity docs that cite specific line ranges within the JSON.
- `rulebook_output.txt` (1.57MB, the full player rulebook text extract) — only grepped for four cosmology terms (all zero hits, confirming rulebook ≠ cosmology source); the mechanics content itself (classes, spells, feats tables) was read only through the many synthesis docs that already cite exact line numbers from it, not read directly end-to-end.
- The ~2,350-line wave-by-wave history inside `src/data/CONTINUITY_REPORT.md` (waves 1–123) was sampled at the header/summary level, not read wave-by-wave — the substance is already captured via `CONTINUITY_DETAILED_CHECK.md` and the "Remaining tensions" / "Already in good shape" sections that were read in full.
- `docs/mechanics/OVERNIGHT_HANDOFF.md` (252KB), `OVERNIGHT_PROGRESS.md` (292KB), `OVERNIGHT_STATUS_MIDNIGHT.md` (70KB), `PLAYTEST_SMOKE.md`, `BALANCE_REPORT.md`/`BALANCE_COMBAT_SIM.md`/`BALANCE_DM_XP.md`/`BALANCE_PLAYER_CLASSES.md`, and the `docs/playtest/SIM_*` / `T4_*` play reports — these are large process/playtest logs; their conclusions are already captured secondhand via `RULESET_VULNERABILITIES.md` and `CONTINUITY_DETAILED_CHECK.md`, which directly cite and summarize them, but the raw logs themselves were not read line-by-line.
- Individual data modules not opened directly: `oracle-mysteries.js`, `oracle-curses.js`, `paladin-oaths.js`, `class-details.js`, `class-paths.js`, `class-draft-levels.js`, `feats.js` (336 entries), `spells.js` (832 entries), `backgrounds.js` (20 entries), `crafting-recipes.json` (623 recipes), `canon-classes.js`, `builder-races.js`. All of these are described accurately and specifically by the synthesis docs that were read in full (glossary, roadmap, bible stub, content gaps), so the *facts* in this digest about them should be reliable, but a line-by-line audit of the raw data was not performed.
- Chapters IV–VIII of `The_Cosmology_of_Decennium_Descent_EXTRACT.txt` (roughly lines 61–194 — covering "The Planes Ascendant," "The Shadow of the Fall," "The Gods' Awakening," "The Weave's Refraction," "The Sentience of the Pact") were **not read directly** in this pass — only their headline claims as cited secondhand in `DUNGEON_CREATION_PURPOSE.md`. If deep cosmology work touches planar structure, the Fall, or "the Sentience of the Pact" specifically, those five chapters should be read directly before writing anything new.

---

## § Gap closure (2026-07-30, second pass)

**Scope of this pass:** close the four items the first digest flagged as unread/unreachable — `rulebook_output.txt` end-to-end, `src/data/cosmology-lore.json` directly, the remaining wave continuity history, and a re-check of parent-folder lore. No commit/push performed.

### G1. `rulebook_output.txt` — the "zero grep hits" in the first digest were a tooling artifact, not an absence of content

The first pass's grep for `Old Ones` / `Silent Ones` / `Matrix of Oblivion` / `Weave of Aethel` returned zero matches and concluded the player rulebook was "mechanics-only." **That conclusion was wrong, and the cause is now identified:** the file is **UTF-16LE encoded**. Reading/grepping it as plain text produces every character separated by a stray byte, so literal substring search silently fails even though the text is there (confirmed via `[System.IO.File]::ReadAllBytes()` — every character is followed by a `0x00` byte). After converting to UTF-8 (`Get-Content -Encoding Unicode` → `WriteAllText(...UTF8)`), the file opened cleanly at 8,193 lines and searches work normally. **Any future agent reading this file must re-encode it first**, or every keyword search against it will falsely report absence.

With proper encoding, direct reads confirm:

- **Chapters 1–8** (`rulebook_output.txt:25–5913`) are player-facing character creation, races, classes, equipment, ability scores, and combat — no cosmology, consistent with the first digest's read of the synthesis docs.
- **Chapter 9: Spellcasting** (line ~6059) contains **"The Weave of Aethel"** intro text and the full Resonance System (pool tables, cost formula, overcast menu) already cited by `RESONANCE_MODELS.md` and `RESONANCE_CANON.md` at the exact same line numbers this pass independently found (6069–6128, 6072–6100) — this **cross-validates** that those two docs already read this file correctly in an earlier session; only the first digest's live grep pass was fooled by the encoding.
- **Appendix A: Conditions** (line 7666) — standard condition rules, no lore content.
- **Appendix B: "The Lore of Aethel"** (line 7743 to end of file, ~450 lines) — **this is new territory; no other document in the repo cites it.** See G1a below — this is the single most important finding of this pass.

### G1a. NEW CONTRADICTION — a second, fully separate creation myth and pantheon live inside the actual player rulebook text

`rulebook_output.txt` Appendix B ("The Lore of Aethel," lines 7743–8189) contains a **complete, self-contained cosmology that does not use any of the Spiral/Choir/Calan'thir/Old Ones vocabulary** used everywhere else in the product:

- **Creation myth:** Lumina ("Radiant Consciousness") and Umbra ("Abyssal Depth") emerge from a primordial Void, weave **the Weave** (eight threads: Order/Chaos/Time/Space/Energy/Matter/Life/Consciousness), and their disagreement causes **the Sundering** — splitting the Material Plane from the Upper/Lower Planes.
- **The Primeval Pantheon** — fifteen greater gods born from Lumina/Umbra's shattered consciousness: **Solarius, Caelestra, Terralith, Aquaria, Vitalis** (from Lumina); **Nocturn, Tempestia, Infernus, Mortalis, Voidus** (from Umbra); **Chronos, Spatia, Arcanus, Naturae, Animus** (Neutral, "born from the balanced threads of the Weave itself").
- A full **Great Wheel planar cosmology** — Ethereal/Astral/Shadowfell/Feywild, Elemental Planes, and Upper Planes (Elysium, **Celestia**, Arborea, Arcadia, Bytopia) / Lower Planes (**the Nine Hells**, the Abyss, Carceri, Hades, Gehenna) / Neutral Planes (Mechanus, Limbo, the Outlands, Ysgard, Acheron) — plus a **Blood War** between devils and demons, Githyanki, Sigil, modrons, slaadi (standard D&D multiverse terms).
- A full **world history** (Dawn Era → Age of Wonders → the Cataclysm → Age of Darkness → Age of Renewal → Imperial Era → Modern Era) with its own continents (**Thalassia, Nordheim, Zephyria**), nations, and factions — entirely independent of the Cycle/Shardspire/Great Descent history used in `dungeon-mechanics.json`.

**Why this matters:** this text lives inside the actual document titled *"decennium descent player rulebook.docx"* — i.e., it is literally in the book a player could read — yet:

- `CONTINUITY_REPORT.md`'s Terms watchlist (line 36) lists the approved vocabulary as "Spiral, Choir, First Song, Echo Court, Turning Spiral, Hush, Shardspire, Tenfold, Resonance, Weave" — **no mention of Solarius, the Primeval Pantheon, or the Great Wheel.**
- Neither `Solarius`, `Primeval Pantheon`, nor `Appendix B` appears anywhere else in `docs/` or `src/` (confirmed by repo-wide search) — **it has never been audited, referenced, or reconciled by any continuity pass.**
- `src/data/cosmology-lore.json` — the app's actual structured/rendered cosmology (see G2) — never mentions Solarius or the Primeval Pantheon either.

**Partial reconciliation, not a clean split:** Asmodeus and the Nine Hells archdevils (Moloch, Dispater, Belial, Fierna, Mephistopheles, Glasya, Innorbatos) **do** appear by name inside the "canon" cosmology (`cosmology-lore.json` Ch. V, see G2) fighting a Blood-War-style conflict against demons — so the Nine Hells/Asmodeus layer is genuinely shared continuity. **It is specifically the Lumina/Umbra-split-into-15-elemental-gods creation myth and the Great Wheel plane list that is the unintegrated, orphaned half of Appendix B** — not the whole appendix.

**Recommended owner framing (not a decision made here):** treat Appendix B's pantheon/plane-list section as either (a) legacy 5e-SRD-style boilerplate never scrubbed when the Spiral/Choir cosmology was authored, to be deleted/replaced, or (b) an intentional "mortal folk religion" layer distinct from cosmic truth (mortals worship Solarius etc. without knowing the Choir/Old Ones truth) — the repo currently supports neither reading explicitly. **This is now added to §8 as open tension #15.**

### G2. `src/data/cosmology-lore.json` — opened and read directly; structure and gap-chapters confirmed

This file was not opened in the first pass; it has now been parsed directly. Its `source` field states it is **"The Cosmology of Decennium Descent.docx + The World of Aethel Lore.docx (player rulebook canon)"** — i.e., it is the app's structured/authoritative mirror of the two `.txt` extracts already read in the first pass (`firstSongSections` = the 12 cosmology chapters, `worldSections` = the 10 World-of-Aethel sections), not a third source.

- **Chapters IV–VIII of the First Song — the explicit gap flagged in the first digest — have now been read in full** (`firstSongSections[3..7].body`, ~27,000–37,000 characters each):
  - **Ch. IV, "The Planes Ascendant":** post-Sundering, four proto-realms crystallize (Bastion of Flame, Veiled Expanse, Radiant Currents, Boundless Void), each shepherded by one or two of the seven Choir virtues; Asmodeus seeds "infernal crystalline law" into them from exile; first mortal souls appear on Aethel and are given "subtle attunement pathways" into the planes.
  - **Ch. V, "The Shadow of the Fall":** the devil/demon war (Asmodeus's Nine Hells vs. the Abyss) intensifies and strains the Divine Pact; the Choir is introduced by name for the first time as seven individually named archon-virtues — **Korvelan (Courage), Vaerilune (Balance), Delvaran (Law), Shaelara (Sorrow), Xalarex (Pattern), Thalirion (Contradiction), Virellian (Passage/Transition)** — a naming layer the first digest did not have; Asmodeus's archdukes (Moloch, Dispater, Belial, Fierna, Mephistopheles, Glasya, Innorbatos) are named directly; the Choir "parleys" with Ul'nak/the hush directly and wins a temporary truce; ends with the "Blade of Remembrance" planted in Asmodeus's own throne room as a seed of future doubt.
  - **Ch. VI, "The Gods' Awakening":** new, lesser gods begin coalescing from mortal resonance rather than from Lumina/Umbra — the **Watch Convocation** (Seven Thrones, tested by trial-of-self rather than granted) and Vaerilune's **Verdant Crucible** (seed-pearls of nascent divinity grown from paired acts of compassion+severity) are the two mechanisms; nobody sits a Throne by the chapter's end — "Awakening" is diffuse, not a coronation.
  - **Ch. VII, "The Weave's Refraction":** the **Candescent Loom** begins archiving mortal *intention* (not just outcome) as visible light; concrete micro-settings appear — **Hearth Embers** (a hamlet where Mirrorsage Serit teaches via truth-revealing lanterns) and the **Violet Ledger** in the Veiled Expanse (tracks concealed mercies/cruelties). Phlegethos's co-rulers Belial and Fierna clash over discipline vs. indulgence; Mephistopheles's "Divine Algorithm" gambit fails.
  - **Ch. VIII, "The Sentience of the Pact":** the Divine Pact itself becomes self-aware ("a will... like gravity"); the Dungeon grows a new **Echo Crucible** chamber that judges visitors by concealed alignment rather than declared alignment; a living **Oracle of Consequence** (a talking tree) appears as a dialogue point with no command authority; the **Liminal Treasury** (deepest level reached at that point) is introduced, keyed to ancestral unresolved vows; chapter explicitly ends by teasing a "Planar War of Threads" as the next escalation.
  - **None of Chapters IV–VIII mention "Silent Ones," "Solarius," or the Primeval Pantheon** — confirmed by direct string search of the full JSON file. The GM-secret stratum remains uncontaminated in this data source, and the Appendix-B pantheon (G1a) does not leak in either.
- **`worldSections[0]` ("I–VI. World primer") has a literally empty body field (`length: 0`)** — this is not an agent-side reading gap, it's confirmed empty in the source data itself. The World of Aethel material genuinely starts at Section VII, matching the 69-line `.txt` extract read in the first pass.
- **Cross-reference confirms `CONTINUITY_REPORT.md`'s own resolution:** Chapter XIV's gate-boss list (Hollow King/Cindervore/Vox Prime) carries a `draftNote: "[superseded by Dungeon Guide]"` in the live data, matching the Director's 2026-07-29 ruling already cited in the first digest's §8 item 8 — **this was already correctly reported as resolved; no correction needed, just confirmed at the data level.**

### G3. Wave continuity history (`src/data/CONTINUITY_REPORT.md`) — reviewed at full length (1,236 lines, not ~2,350 as estimated in the first pass)

The file is shorter than the first digest's inventory guessed. A full header-to-tail pass (not just the samples read the first time) surfaces:

- **Confirms, does not change:** the Cosmology XIV supersession (above), the Umbrin/Calan'thir exile lore ("Calan'thir and the First Choir judged them unfit for the light... banished them into The Murk" — verbatim match to `UMBRIN_LORE.md`, no new facts), and the Bloodbound/Gravetouched resolution already in the first digest's owner-locks table.
- **New operational fact worth flagging:** `rulebook_output.txt` is **not a frozen source file** — it has been actively hand-edited by the continuity process itself (e.g., a wave explicitly "replaces 38 legacy Drow-era references... with Umbrin" directly inside the rulebook extract). This raises the stakes on G1a: the team has proven willingness and process to edit this file for continuity, but Appendix B's orphaned pantheon was never touched by that process — it wasn't missed because it's unreachable, it was missed because nobody had cause to open Appendix B specifically.
- **`RESONANCE_MODELS.md`** (not separately listed in the first digest's inventory table, though its conclusions were already reflected in §5) was read directly this pass — it fully confirms §5's Model A/Model B account with matching line citations (`rulebook_output.txt:1417–1433` for Model A, `6069–6128` for Model B) and adds one detail not previously surfaced: **Chapter 9 itself contains a stray, non-canon "Fate Weaving" Oracle paragraph** (`rulebook_output.txt:6419–6424`) that contradicts the real Revelation Charges design and is explicitly flagged in that doc as "stale/unintegrated draft... should be disregarded regardless of which model wins."
- **Prestige lore:** no unread prestige content was found. `prestige-lorebook.json` (18 paths, read in full in the first pass) is the complete authoring source; the wave history confirms 0 missing feat cross-references and the Bloodbound/Gravetouched question closed — nothing new to add.
- The `docs/mechanics/OVERNIGHT_HANDOFF.md` (252KB) and `OVERNIGHT_PROGRESS.md` (292KB) logs were grepped (not read line-by-line, given their process-log nature and size) for `Silent Ones`, `Old Ones`, `Calan'thir`, `Umbra`, `cosmology`, `pantheon` — all hits are wave-stamp references to already-known facts (Umbrin/Calan'thir lore stub polish, cosmology draft-flavor batches for World sections VII/VIII/X/XI). No new lore substance found in either file.

### G4. Parent folder (`C:\Github\Descent assets`) — re-confirmed, nothing new

Directory listing repeated at the parent level: `art/`, `Assets/`, `EUALAs/`, `extracted/`, `Movies/`, `readmes/`, `swtor/` are present. **`readmes/` is empty** (zero files, confirmed via recursive listing). All other parent folders and the ~15 loose files at repo root (`launcher.exe`, `.version` files, `SWTOR Customer Support.url`, etc.) are SWTOR installer/launcher artifacts, consistent with the locked strategy rule. **No lore-only folder exists outside `DecenniumDescent-main`** — this matches and reconfirms the first digest's finding; there was nothing to close here.

### Updated §8 — new open tension

**15. Appendix B's Primeval Pantheon vs. the Spiral/Choir cosmology.** **RESOLVED (owner lock round 2, 2026-07-30):** "Keep, but as mortal folk religion — not objective canon... Rename toward 'Faiths and Cosmologies of Aethel' with disclaimer." Full rewrite brief, locked 7-rung hierarchy (Spiral → Old Ones/Ul'nak → Heartcell → Calan'thir & Asmodeus → First Choir (7) → Fifteenfold Pantheon → Cultural gods/ascended), and player know/don't-know tables: [`APPENDIX_B_FOLK_RELIGION.md`](../mechanics/APPENDIX_B_FOLK_RELIGION.md). **The `rulebook_output.txt` text itself is not yet patched** — that patch is logged as TODO in that file rather than performed silently.

### Gaps closed vs. still open

**Closed by this pass:**
- `rulebook_output.txt` read end-to-end with correct encoding (was previously mis-read as absent-of-content due to a UTF-16 decoding failure).
- `src/data/cosmology-lore.json` opened and read directly (was previously inferred only via its `.txt` source siblings).
- Cosmology extract Chapters IV–VIII read in full (was the single largest named gap in the first digest's §9).
- `RESONANCE_MODELS.md` read directly (previously only reflected secondhand).
- Wave continuity history (`CONTINUITY_REPORT.md`) reviewed at full length rather than sampled.
- Parent-folder lore re-check — reconfirmed empty, no new folders.

**Still genuinely unread (not reachable at reasonable cost in this pass either):**
- `docs/mechanics/OVERNIGHT_HANDOFF.md` (252KB), `OVERNIGHT_PROGRESS.md` (292KB), `OVERNIGHT_STATUS_MIDNIGHT.md` (70KB) — grepped for lore terms only (see G3), not read line-by-line; their conclusions are already captured secondhand via `RULESET_VULNERABILITIES.md` and `CONTINUITY_DETAILED_CHECK.md`.
- Individual data modules (`oracle-mysteries.js`, `oracle-curses.js`, `paladin-oaths.js`, `class-details.js`, `feats.js`, `spells.js`, etc.) — still not opened directly; not in scope for this pass's explicit ask (rulebook, cosmology JSON, wave continuity, parent lore).
- `rulebook_output.txt` Chapter 9's non-Resonance content (spell schools, class-specific resource crossover text past line ~6436) was located but not transcribed line-by-line beyond what `RESONANCE_MODELS.md` already cites — no indication of further cosmology content there, but flagging for honesty.

---

## Related documents

- [`READY_TO_CONTINUE.md`](./READY_TO_CONTINUE.md) — one-page owner-facing summary of this ingest
- [`../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`](../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md) — **rulebook/DM priority hierarchy + override questions (2026-07-30)**
- [`DUNGEON_CREATION_PURPOSE.md`](./DUNGEON_CREATION_PURPOSE.md) — the authoritative cosmology-reconciliation source this digest leans on most heavily
- [`../mechanics/SILENT_ONES_CANON.md`](../mechanics/SILENT_ONES_CANON.md) — GM-secret stratum, full text
- [`../mechanics/DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md) — Opening 2400h / Horn PoNR 1200h day 50
- [`../mechanics/CONTINUITY_DETAILED_CHECK.md`](../mechanics/CONTINUITY_DETAILED_CHECK.md) — Gate A–G audit trail
- [`../../src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md) — approved terminology, source of truth for names

*No commit/push performed, per brief.*
