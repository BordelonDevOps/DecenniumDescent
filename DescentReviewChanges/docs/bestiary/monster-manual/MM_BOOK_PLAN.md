# MM-01 Book Plan — Monster Manual of the Decennium

**Proposed book code:** MM-01  
**Recommended title:** *Monster Manual of the Decennium*  
**Subtitle:** *Creatures of Aethel, the Heartcell, and the Hundred Floors*  
**Working alternate (reject if it collides in marketing):** “Bestiary of Aethel — Monster Manual” — **do not use** as the commercial spine title; it collides with published/development **BE-01 Bestiary of Aethel**.

---

## 1. Title recommendation

| Option | Verdict |
|--------|---------|
| **Monster Manual of the Decennium** (MM-01) | **Recommended** — clear product role, original framing, no title collision |
| Codex of the Heartcell (BB-01) | Keep as ecology / Gate Seal sister volume — not the MM spine |
| Bestiary of Aethel (BE-01) | Keep as searchable development encyclopedia — not overwritten by MM |
| “Bestiary of Aethel — Monster Manual” | **Avoid** as primary title; confuse BE-01 and imply overwrite |

**Elevator line:** A Director-and-player-facing creature book for Decennium Descent — full ecology, DD combat blocks, floor pressure, and harvest stakes — compiled for completeness comparable to a professional monster manual, written entirely in Aethel voice.

---

## 2. Relationship to existing Bestiary of Aethel (and Codex)

```
Excel (Bestiary.xlsx)
        │ ingest
        ▼
bestiary_data_full.json  ←── companion combat trust passes
        │
        ├──► BE-01  Bestiary of Aethel     (A–Z development dump; publication pending)
        ├──► BB-01  Codex of the Heartcell (ecology essays + Gate Seals; development)
        └──► MM-01  Monster Manual of the Decennium  (NEW — selected publication compilation)
```

| Volume | Code | Job | MM relationship |
|--------|------|-----|-----------------|
| **Bestiary of Aethel** | BE-01 | Full-index searchable encyclopedia (~707 entries); Excel-backed | **Source corpus.** MM cites and expands selected rows; does not replace the dump. |
| **Codex of the Heartcell** | BB-01 | Ecology-first Director book; Gate Seal chapters; honesty flags | **Sister depth.** MM may excerpt Gate Seal *summary* cards and point to BB-01 for full staging essays. |
| **Monster Manual of the Decennium** | MM-01 | Publication-ready creature book (curated set) | **New compilation path.** Original prose; DD mechanics; harvest hooks. |

See ReviewBible `docs/development/BESTIARY_PUBLICATION_STATUS.md`: many sheet rows remain coverage placeholders. MM publication copy must be authored Aethel material, not renamed foreign stock.

### STOP-and-ask — published ReviewBible Bestiary `.docx`

**This plan must not silently overwrite** ReviewBible (or dual-written) published/development books:

- `Decennium_Descent_Bestiary_of_Aethel.docx` / `.md` (BE-01)
- `Codex_of_the_Heartcell.docx` / `.md` (BB-01)

**Preferred path:** compile MM-01 under `docs/bestiary/monster-manual/` (+ DescentReviewChanges dual-write) as a **new** volume that **cites and expands** BE-01/BB-01. Only regenerate BE-01/BB-01 `.docx` after an explicit owner publication pass.

**Owner decision needed before any BE-01/BB-01 file replace:**

| Option | Meaning |
|--------|---------|
| **(a)** Keep BE-01 as development dump forever; MM-01 is the commercial creature book | Cleanest product story |
| **(b)** Eventually retire BE-01 title into MM-01 after a full authorship pass | Requires owner rename/merge lock |
| **(c)** Rename BE-01 to an internal “Creature Index” and ship MM-01 publicly | Marketing + continuity pass |

Until the owner picks (a)/(b)/(c), agents **only** add files under this MM pack.

---

## 3. Volume strategy

### Recommendation: **one flagship MM + optional later tier supplements**

| Volume | Scope | When |
|--------|-------|------|
| **MM-01** *Monster Manual of the Decennium* | Reading the Manual · How to read a DD block · Expedition roles vs creatures · Ecology primers · **~180–220** full/field entries (T1–5 trusted core + signature Aethel lineages + all 10 Gate Guardians as seal cards) · Appendices | **Primary ship target** |
| **MM-02** *Deep Descent Supplement* (optional) | T6–10 trash + Interstice fauna once combat trust lands; expanded Spiral / Hush / Order-Drone families | After T6–10 combat freeze |
| **MM-G** *Gate Seals folio* (optional slim) | If BB-01 Gate chapters stay Director-only, a player-safe seal summary pamphlet | Only if product needs a split |

**Why not ten tiny tier booklets at launch:** professional MM feel comes from one thick spine (how-to-read, ecologies, dense A–Z, indexes), not from fragmenting every Gate. Tier supplements are fine *after* MM-01 establishes the brand.

**Why not dump all 707 into MM-01:** BE-01 already is that dump. Shipping 707 stub/sandbox blocks as “Monster Manual” would undershoot quality and collide with publication status. Curate hard; index the rest.

---

## 4. Completeness / density goals (qualitative DD terms)

Aim for **table completeness**, not page-count cargo-cult. Industry MM-class bar (structure only — see `REFERENCE_MM_BENCHMARK.md`): on the order of **300–400+ authored entries / table-ready blocks** plus lookup appendices. DD already has ~707 JSON rows; the gap is **authored completeness**, not row count.

| Density band | Target feel | MM-01 launch spine | Line goal (MM-01 + authorship + optional MM-02) |
|--------------|-------------|--------------------|--------------------------------------------------|
| **Full Entry** | Director can run without Excel: look, wants, floors, tactics, full combat, harvest | **120–150** | Grow toward **250+** |
| **Field Brief** | Condensed combat + short ecology (trusted trash) | **50–70** | **100+** (variants count toward block bar) |
| **Seal Card** | Gate Guardian one-spread → “see BB-01 for staging” | **10** | **10** |
| **Index-only** | Pointer into BE-01 / companion for unauthored rows | Appendix | Shrink as authorship lands |

**Launch vs parity:** Ship MM-01 when T1–5 Directors can stay in-book for ordinary foes (**~180–220** Full+Field+Seals). Treat **300–400+** authored blocks as the **product completeness bar** (benchmark), reached by continued entry upgrades and/or MM-02 deep-tier fauna — not by pasting the 707-row dump.

**Qualitative parity with a classic MM:**

- Opening “how to use this book” in **DD language** (Expedition roles, Opening clocks, draft honesty, Seal Pulses — not foreign legendary jargon).
- Ecology / lore-family chapters (benchmark: Volo-like depth *pattern*, original Aethel content) teaching **floors and harvest pressure**.
- Lexicon + appendices: conditions, DIY→Excel ingest, CR/tier index, floor/zone index, harvest quick-ref, stat-block index.

**Benchmark file:** `REFERENCE_MM_BENCHMARK.md` — structure/density norms only. Never copy foreign product text, tables, or creature writeups.

---

## 5. Table of contents (MM-01 outline)

### Front matter
0. Title, book code, continuity stamp, honesty about draft/publication status  
1. **How to Use This Manual** — Expedition roles (Combat / Recon / Research / Resource / Support); when to open BE-01 vs BB-01 vs MM  
2. **How to Read a Decennium Creature Block** — Size/Type/Alignment; Challenge (budget aid, XP awards still blocked per advancement canon); Zone vs Floor/Tier; Armor / Hit Points / Speed; defenses; attacks & recharge; Weave interaction notes; Seal Pulse rules (pointer)  
3. **Creature Provenance & Trust** — publication vs expedition-ready vs development cite; `combat.draft` / trust stamps  

### Part I — Ecologies of Pressure
4. Reading the Spiral — aberrations & breach fauna  
5. Yieldheart & the upper stone — beasts, constructs, early seals  
6. Bloomdeep & verdant attrition — plants, spores, wet hazards  
7. Anvil heat & forged purpose — elementals, constructs, fire cultures  
8. Radiance, Choir, and hush bargains — celestials/echoes, fiends of the Hush, floor politics  
9. Deep Iron & silence — T6–10 primers (short; full fauna → MM-02 if split)  
10. Peoples of the floors — humanoid cultures as encounters (parley-first)  

### Part II — Gate Seals of the Ten Divisions
11–20. One **Seal Card** per Guardian (Vaskor → Marquis), each with: lore hook, floor, combat summary, reward-as-bait one-liner, **“Full staging: BB-01”**  

### Part III — Creature Lexicon
21. **Full Entries** A–Z (or by family, then CR — pick one sort key and stick to it; recommend **family chapters matching Part I, then CR within family**, with A–Z index in back)  
22. **Field Briefs** — condensed trusted trash  

### Part IV — Director’s Workshop
23. Building a creature for Aethel (Excel → ingest → MM entry upgrade path)  
24. Lair omens & floor pressure tables (tier bands)  
25. Harvest & craft hooks (pointer to Instruments / Crafting Bible; whole-creature harvest summary)  

### Appendices
A. Conditions & monster-facing effects (DD terms)  
B. Challenge index  
C. Floor / tier index  
D. Harvest material index  
E. Name change / IP scrub ledger pointer (Director only)  
F. Full BE-01 name index (page/pointer only — “development dump lives in BE-01”)  

---

## 6. Naming & marketing language (DD-original)

Use / prefer:

- Monster Manual of the Decennium, Heartcell, Spiral, Opening, Expedition, Seal / Seal Pulse, Weave, Gate Division, harvest node, draft honesty  

Avoid in MM body:

- Foreign product book titles as in-world terms  
- “Legendary actions” labeling (use **Seal Pulse**)  
- Silent overwrite claims like “this volume replaces the Bestiary of Aethel” without owner lock  

---

## 7. Compilation pipeline (agents)

1. Prefer ReviewBible JSON + trust docs for numbers.  
2. Author markdown under `entries/` using `ENTRY_TEMPLATE.md`.  
3. Dual-write to `DescentReviewChanges/docs/bestiary/monster-manual/`.  
4. Track publication counts in activity logs; do not auto-regen BE-01/BB-01.  
5. When ~120 Full Entries + 10 Seal Cards exist for T1–5, propose owner `.docx` build for MM-01 only.

---

## 8. Open questions for owner

1. Confirm title **Monster Manual of the Decennium** (MM-01) vs alternate.  
2. Choose BE-01 relationship option **(a)/(b)/(c)** in §2.  
3. Confirm MM-01 single-spine first vs immediate T1–5 / T6–10 split.  
4. Player-facing vs Director-only for Gate Seal full tactics (default: summary in MM, depth in BB-01/DM-01).  

---

*Plan stamp: 2026-08-04 — Agent 3 (Book Architecture). Continuity: ReviewBible wins; no silent rulebook/BE-01 overwrite.*
