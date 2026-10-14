# Continuity — source of truth hierarchy

**Status:** **Mandatory process** (2026-07-30) · **ReviewBible promotion:** 2026-07-31 · **Canon manifest:** 2026-08-05  
**Audience:** Continuity agents, Director docs, companion workers  
**Workspace:** `DecenniumDescent-main`  
**Rule:** **Never silently overwrite** published Player Rulebook or Director book text with owner locks, playtest composites, Matrix extract typos, Session UI limits, or companion JSON.

---

## 0. One canonical manifest (owner lock 2026-08-05 §1)

**Do not maintain two parallel Sources of Truth for the same facts.**

| Role | Path |
|------|------|
| **Domain registry** | [`docs/canon/CANON_MANIFEST.json`](../canon/CANON_MANIFEST.json) |
| **Promotion hierarchy** | [`docs/canon/REPOSITORY_PROMOTION.md`](../canon/REPOSITORY_PROMOTION.md) |
| **Incoming staging** | `DescentReviewChanges/incoming/` |

- The manifest is a **registry** (domain → authoritative file(s), version, visibility, status, supersedes). Domain facts live in those files.
- **main** = approved release · **ReviewBible** = assembled review build · **DescentReviewChanges/** = unapproved staging · **incoming/** = new packs pending review (§12).
- This ops file and the ReviewBible pack SoT **must not independently own the same override/domain facts**. Pack SoT mirrors / syncs; the manifest points at the owner file for each domain.

---

## 0a. Assembled review build — ReviewBible (owner lock 2026-07-31; clarified 2026-08-05)

**`DescentReviewChanges/ReviewBible/`** is the curated **assembled review build** continuity agents **open and audit against** for published books and companion mirrors — after checking `CANON_MANIFEST.json` for which domain file wins on a given fact.

| Role | Path |
|------|------|
| **ReviewBible root** | `C:\Github\Descent assets\DecenniumDescent-main\DescentReviewChanges\ReviewBible\` |
| **Pack README / tour** | `…/ReviewBible/README.md`, `…/ReviewBible/REPOSITORY_GUIDE.md` |
| **Pack-local SoT (book open order + sync pointer)** | `…/ReviewBible/docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` |

**What ReviewBible is:** the **distributable / review continuity bible** — Player Rulebook, DM-01 Complete Director Edition, sister Director volumes, supporting lore, curated mechanics, and companion `src/` data (main baseline + promoted changes). Archives and superseded dumps are **intentionally excluded**.

**What this file is:** the **agent ops protocol** (priority order, STOP-and-ask gate, open override tracker). It is **not** a competing domain SoT and **not** a second copy of Core Systems / Crafting / MM / feat facts.

**Do not** treat missing old paths (e.g. `The_Directors_Crucible.md`, archive `Decennium_Descent_Directors_Manual.*`, pre-edit rulebook backups) as source of truth — they are absent from ReviewBible **on purpose**.

---

## 1. Priority order (highest wins unless owner explicitly reorders)

| Priority | Layer | What it is |
|----------|-------|------------|
| **1** | **Owner spoken lock** | Direct owner chat directive — authoritative for *intent* only; **not** auto-permission to edit locked book text |
| **2** | **CANON_MANIFEST domain owners** | Authoritative path(s) registered for that domain (may be pending-review / pending-locate) |
| **3** | **ReviewBible assembled build** | Open published books/data **here** for audits and sims when the domain still lives in those books |
| **3a** | **Published books inside ReviewBible** | Player Rulebook + DM-01 (+ sister volumes) — except where the manifest assigns a domain (e.g. Core Systems spellcasting/combat/gate/economy) to a newer bible |
| **4** | **Companion code / data** | Prefer paths the manifest lists; else ReviewBible `src/data/*` / main mirrors |
| **5** | **Playtest sims & synthesis** | Historical / exploratory — never promote to canon without owner + book/manifest alignment |

### Drift / promotion (2026-08-05)

- **Domain facts:** follow `CANON_MANIFEST.json`. Do not invent a second owner.
- **Assembled build:** ReviewBible should hold main baseline + promoted changes (§11). Prefer ReviewBible for continuity opens of published books **unless** the manifest points elsewhere for that domain.
- **Legacy drift lock** (*"ReviewBible always win"*): still applies to **assembled-build vs stale main mirrors** for material that has not been reassigned by the manifest. It does **not** let ReviewBible override a newer registered domain bible (e.g. Core Systems pending-review pack, Crafting v4 when located).
- New root drops → `DescentReviewChanges/incoming/` first (§12). Never auto-promote into ReviewBible or main.
- When a change would **overwrite** locked book text: **STOP** (§4).

---

## 2. Published rulebook paths (exact) — open these under ReviewBible

Prefix all continuity opens with:

`C:\Github\Descent assets\DecenniumDescent-main\DescentReviewChanges\ReviewBible\`

### Player Rulebook

| Role | Path under ReviewBible |
|------|------------------------|
| **Primary source (Word)** | `decennium descent player rulebook.docx` |
| **Living text extract** | `rulebook_output.txt` (UTF-16LE — re-encode before grep/edit) |
| **Class-scoped extract** | `tools/oracle_rulebook_extract.txt` |

### DM Manual — published GM corpus

**DM-01:** **`docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx`** — official Director's Crucible. Sister volumes stay active; see ReviewBible `docs/manuals/BOOK_LINEUP.md`.

| Role | Path under ReviewBible |
|------|------------------------|
| **DM-01 Complete Director Edition** | `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` |
| **Lineup** | `docs/manuals/BOOK_LINEUP.md` |
| **Agent pointer** | `docs/manuals/AGENT_SIMULATION_REFERENCE.md` |
| **BB-01 Codex of the Heartcell** | `docs/manuals/Codex_of_the_Heartcell.docx` (+ `.md`) |
| **TB-01 Instruments of the Weave** | `docs/manuals/Instruments_of_the_Weave.docx` (+ `.md`) |
| **GZ-01 Chronicle** | `docs/manuals/Chronicle_of_the_Decennial_Opening.docx` (+ `.md`) |
| **BE-01 Bestiary of Aethel** | `docs/manuals/Decennium_Descent_Bestiary_of_Aethel.docx` (+ `.md`) — development / searchable; publication pass pending |
| **GZ-01a F51–100 Deep Gazetteer** | `docs/manuals/F51_100_Director_Deep_Gazetteer.md` |

Supporting GM-facing sources (same ReviewBible root):

| Role | Path under ReviewBible |
|------|------------------------|
| **Matrix of Oblivion (Word)** | `The Decennium Descent and the Matrix of Oblivion.docx` |
| **Matrix extract** | `docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md` |
| **Cosmology (Word)** | `The Cosmology of Decennium Descent.docx` |
| **Cosmology extract** | `The_Cosmology_of_Decennium_Descent_EXTRACT.txt` |
| **World of Aethel Lore (Word)** | `The_World_of_Aethel_Lore.docx` |
| **World extract** | `The_World_of_Aethel_Lore_EXTRACT.txt` |
| **Floor Encounters (Word)** | `Floor Encounters.docx` |
| **Floor extract** | `floor_encounters_new.txt` |
| **Companion mirrors** | `src/data/cosmology-lore.json`, `dungeon-mechanics.json`, `floor-encounters.json` |

**Intentionally not in ReviewBible (do not cite as live SoT):**

| Former pointer | Status |
|----------------|--------|
| `The_Directors_Crucible.md` / `.docx` (non-Complete) | Superseded / missing — use DM-01 Complete Edition |
| `docs/manuals/Decennium_Descent_Directors_Manual.*` | Archive dumps — may exist only under main working tree |
| Pre-edit rulebook backups (`*.pre-*.docx`) | Backups only |
| Third-party PDFs, `node_modules/`, build output | Excluded from distributable pack |

**GM-secret stratum:** DM-01 Ch 8 / Canon Guardrails (Q-OV-4 closed). Companion mirrors under ReviewBible `docs/mechanics/` (`SILENT_ONES_CANON.md`, etc.). Do not write into Player Rulebook.

---

## 3. Continuity audit protocol

Every continuity pass **MUST**:

1. **Open `docs/canon/CANON_MANIFEST.json`** — identify which file owns the domain under audit.
2. **Open ReviewBible** as the assembled review build for published books/companion mirrors (unless the manifest points elsewhere for that domain).
3. **Open the Player Rulebook** under ReviewBible (`rulebook_output.txt`, UTF-16LE-aware) for mechanics, expedition, class, or appendix topics — except domains reassigned by the manifest (e.g. Core Systems spellcasting/combat/gate/economy).
4. **Open DM-01** under ReviewBible plus supporting sources (Matrix + Cosmology + World + Floor Encounters as applicable) for dungeon, cosmology, horn, tier, or gate topics.
5. **Compare** owner locks and companion code against the manifest owner + ReviewBible published text — log drift; do not “fix” published text silently.
6. **Label** companion-only content (`draft: true`, code/doc debt, playtest exception) when it diverges from the books.

Encoding reminder: `rulebook_output.txt` is **UTF-16LE**. Plain-text grep without Unicode decoding **falsely reports absence**.

---

## 4. Override gate — STOP and ask the owner

If a proposed change, playtest composite, owner lock, or companion patch would **conflict with** or **overwrite** Player Rulebook or Director book text **in ReviewBible** (or a dual-written published export):

**STOP.** Do not silently edit the `.docx` or extracts. Draft an explicit owner question with:

| Field | Content |
|-------|---------|
| **(a) What the ReviewBible / published source says** | Quote or line-cite the book text |
| **(b) What would change** | The lock, sim, or companion text that conflicts |
| **(c) Options** | At minimum: **amend via ReviewBible** · **treat as GM house rule** · **keep both layers** (public vs secret) · **other** |

When the owner approves an amend: edit **ReviewBible** locked books (and dual-write to main product paths / `DescentReviewChanges` per activity-log rules). Still ask before **destructive** overwrites of locked text.

Log open questions in main ops mirrors (`src/data/CONTINUITY_REPORT.md` § ASK OWNER, `docs/playtest/READY_TO_CONTINUE.md`) until answered — those may live outside ReviewBible as agent ops.

**Never:**

- Silently overwrite rulebook canon with playtest composites (e.g. T4 24-PC roster as RAW).
- Patch Matrix extract typos into `.docx` without owner sign-off.
- Change Session UI constants (`HORN_AT`, `hornRule`) **against** owner lock without explicit approval. (Q-OV-1 closed 2026-07-31 at **1200/2400**.)
- Rewrite Player Rulebook Appendix B without owner approval on the actual rulebook file in ReviewBible.

---

## 5. Pending owner override questions (2026-07-30)

Resolved items stay logged. **Open** items still require owner confirmation before further rulebook/DM overwrites.

> **SoT split — RESOLVED 2026-08-05 (§1):** Not two competing SoT files owning the same facts. **One** `docs/canon/CANON_MANIFEST.json` registry + domain files. This main file = **ops protocol + Q-OV tracker**. ReviewBible pack SoT = **book open order + sync pointer** (mirrors baselines; does not independently own them). See `docs/canon/REPOSITORY_PROMOTION.md`.

> If ReviewBible books and an open override or a registered domain bible disagree, **STOP** and ask — do not invent a silent merge. Check the manifest first.

### Q-OV-1 — Horn timing — **RESOLVED 2026-07-31**

| | |
|---|---|
| **(a) Was** | Companion briefly taught **120 hours** as Horn PoNR; some drafts used Opening **240**. |
| **(b) Canon** | Opening **2400h / 100 days**; Horn PoNR **1200h / day 50**; soft quit Floor 50 Canticle ≠ Horn. |
| **(c) Disposition** | Literature + Session `HORN_AT` / `hornRule` / ingest **purged to 2400/1200**. |

**Closed.** Do not re-open 120-as-PoNR or 240-as-Opening as live options.

### Q-OV-2 — Expedition 12-person RAW vs T4 24-PC sims — **RESOLVED 2026-07-31**

| | |
|---|---|
| **(a) Player Rulebook** | ReviewBible `rulebook_output.txt` (and expedition canon): **up to 12 characters per Expedition**; five teams; morning/afternoon/evening periods. |
| **(b) Playtest / sims** | T4 scenario: **24 PCs (3×8 companies)** — stress-test coalition only. Companion Session has **no team/period assignment**. |
| **(c) Disposition** | Owner spoken lock (2026-07-31): **12 is max for an expedition.** Rulebook RAW stands. T4 24-PC sims are **playtest evidence only** — do **not** promote a 24-PC expedition charter as canon. Larger forces = **multiple Expeditions coordinating**, each under the 12-seat cap. |

**Closed.** Do not re-open 24-as-RAW or author a charter exception that overwrites published expedition text to 24. STOP-and-ask (§4) still applies if anyone proposes overwriting Player Rulebook / ReviewBible expedition text to 24 — owner has locked **12**.

### Q-OV-3 — Appendix B folk-religion rewrite — **PLAYER PATCH APPLIED 2026-07-31**

| | |
|---|---|
| **(a) Was** | Appendix B **"The Lore of Aethel"** as objective-setting cosmology. |
| **(b) Done** | Owner amend: rename **"Faiths and Cosmologies of Aethel"**, disclaimer, masks/abstractions — in Player Rulebook. |
| **(c) Remainder** | Optional second tone-scrub; GM-secret hierarchy stays out of player book. |

### Q-OV-4 — Silent Ones / authorship — **RESOLVED 2026-07-31**

| | |
|---|---|
| **(a) Was** | Deep Silent Ones / Heartcell lived mainly in companion docs. |
| **(b) Canon** | Labeled GM-only in **DM-01** Ch 8 + Canon Guardrails; Silent Ones ARE the Old Ones. Player Rulebook keeps public Crucible myth only. |
| **(c) Disposition** | Closed. Do not put deep Silent Ones / Heartcell spoilers in the Player Rulebook. |

### Q6 / Lock J — Level 97 / Old God — **Director crystal path locked 2026-08-05** (dual-layer)

| | |
|---|---|
| **(a) Public books today** | World Binding@97 and DM-01 Old God Interstice (T7–T8) still present as text; **must not** be treated as publicly reliable mechanics going forward. Public knowledge ceiling = **failed Sixth Gate** (`CANON_BOUNDARY.md`). |
| **(b) Owner spoken lock (2026-08-05)** | **Crystal path = Director-level canonical truth:** final known sequence → Floor 100 confrontation produces/exposes **focusing crystal** → crystal weakens / makes Old God vulnerable → confront Old God under those conditions. Floor 97 remains a **regular zone** with a **hidden chamber** (Old Ones sleep). Unprepared: L30 mind-control near wipe. |
| **(c) Disposition** | **Dual-layer:** vague contradictory rumors publicly; crystal path **Director-only**. Do **not** publish Floor 97/100, focusing crystal, or Old God vulnerability in player-facing books. Binding/Interstice may survive only as **false scholarship / corrupted translations / discarded design history** — not reliable public ops. |
| **Book rewrite** | **DEFERRED.** STOP before rewriting Player Rulebook chapters this pass. Put Director truth in sealed/continuity materials; mark public books for later Binding/Interstice scrub. |
| **Remaining gaps** | Crystal/Old God full stats; identity merge; public-book scrub pass; F97 encounter mapping — see holding doc. |

Holding doc: [`LEVEL_97_OLD_GOD_Q6_OPEN.md`](./LEVEL_97_OLD_GOD_Q6_OPEN.md).

---

## 6. Cross-references

| Doc | Role |
|-----|------|
| **`docs/canon/CANON_MANIFEST.json`** | Single domain → authoritative-file registry (2026-08-05) |
| **`docs/canon/REPOSITORY_PROMOTION.md`** | main / ReviewBible / staging / incoming hierarchy |
| **`DescentReviewChanges/ReviewBible/`** | Assembled review build (owner lock 2026-07-31; clarified 2026-08-05) |
| ReviewBible `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` | Compact in-pack book open order + sync pointer (not independent fact owner) |
| ReviewBible `docs/manuals/BOOK_LINEUP.md` | Official Director line codes |
| ReviewBible `docs/manuals/AGENT_SIMULATION_REFERENCE.md` | Sim primary references |
| This file (main) | Agent ops protocol + open override tracker |
| `.cursor/rules/continuity-rulebooks.mdc` | Agent mandatory rule |

*Process locked — 2026-07-30. Canon manifest + promotion path — 2026-08-05. SoT split resolved via registry. Q6 dual-layer crystal path (Director-only; public ends at Sixth Gate). No commit.*
