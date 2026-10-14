# Expedition structure — canon stamp (12-person expeditions)

**Status:** **Owner-locked RAW** (2026-07-30 — owner re-asserted rulebook content they had forgotten was in the book)  
**Scope:** How **Expeditions** in Aethel are organized — max roster, five activity teams, day periods, assignment mechanics, base camps, advancement, and parallel resolution — distinct from combat-party size  
**Do not contradict:** RAW max **12 characters per Expedition**; larger forces = **multiple expeditions coordinating**, not one oversized roster.

---

## Source of truth (this chapter)

| Priority | Artifact | Role |
|----------|----------|------|
| **1 — Authoritative** | **`decennium descent player rulebook.docx`** (Player Rulebook) · extract: `rulebook_output.txt` § **Expeditions in Aethel** (lines **3801–3926**) | **Source of truth** for expedition structure, team sizes, day periods, assignment mechanics, examples, base camps, advancement, and resolution methods |
| **2 — Mirror / subset** | `src/data/dungeon-mechanics.json` → `expedition` · `src/components/DungeonGuide.tsx` | **Companion mirror** — machine-readable subset for UI and sims; must **not** override or silently replace rulebook prose |
| **3 — Duplicate extract** | `feat_compendium_output.txt` **3802–3926** | Ingest mirror of rulebook text; cite rulebook if extracts diverge |

**Continuity policy:** Do **not** rewrite, overwrite, or “fix” **Player Rulebook** or **DM Manual** text in repo extracts or on-disk `.docx` files without **explicit owner approval**. Companion JSON, docs, and UI may **reflect** rulebook RAW but must **ask the owner** before any change that would supersede or replace authored rulebook/DM-manual wording. On conflict, **rulebook wins** until the owner says otherwise.

**Repo-wide policy doc:** [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md) (2026-07-30).

---

## Owner reminder (2026-07-30)

The owner re-asserted that **Expeditions in Aethel / The 12-Person Expedition Structure** is full rulebook RAW, not a Director invention. Treat this section as **canon for expedition management** at the table. Playtests that fielded **7–8 PCs** or **24 PCs (3×8 companies)** are **director/playtest exceptions** or **multi-expedition coalitions** — see §6.

---

## 1. Primary source locations

| Layer | Location | What it holds |
|-------|----------|---------------|
| **Player Rulebook (source of truth)** | `decennium descent player rulebook.docx` · extract `rulebook_output.txt` § **Expeditions in Aethel** → **The 12-Person Expedition Structure** (lines **3801–3926**) | Full RAW: teams, periods, skill checks, examples, base camps, advancement, conclusion — **authoritative** |
| **Duplicate extract** | `feat_compendium_output.txt` lines **3802–3926** | Mirror of rulebook extract (ingest copy) |
| **Companion JSON (mirror only)** | `src/data/dungeon-mechanics.json` → `expedition` | `maxSize: 12`, five `teams[]` with size bands + one-line `function`, `timePeriods[]` — **subset mirror**, not a second authority |
| **Companion UI (read-only display)** | `src/components/DungeonGuide.tsx` — Expedition card | Renders JSON teams; no assignment or period scheduling |
| **Ingest script** | `tools/ingest_lorebook.py` | Hard-codes `expedition` block into `dungeon-mechanics.json` (not parsed from rulebook text at ingest time) |

**Encoding note:** `rulebook_output.txt` is UTF-16LE; grep/read tools must use Unicode encoding.

---

## 2. RAW summary (with citations)

### 2.1 Definition — organizational cap, not combat cap

> In Decennium Descent, adventuring parties are known as **Expeditions** and can consist of **up to 12 characters**. This limit represents the **total number of individuals working together toward common goals, not just those engaged in combat**. An effective Expedition distributes its members across various activities to maximize efficiency, resource gathering, information collection, and overall success.

— `rulebook_output.txt` **3804–3805** (also `feat_compendium_output.txt` **3804–3805**)

### 2.2 Five activity teams (size bands)

| Team | Optimal size | Function (RAW) |
|------|--------------|----------------|
| **Combat Team** | 4–6 | Battles, dungeon delving, immediate threats |
| **Reconnaissance** | 1–3 | Scouting ahead, gathering intelligence, mapping terrain |
| **Research** | 1–3 | Studying artifacts, researching lore, identifying items, translating texts |
| **Resource** | 2–4 | Hunting, gathering, cooking, crafting, harvesting materials |
| **Support** | 1–3 | Camp management, equipment maintenance, healing, transportation |

Key roles, skill considerations, and alignment notes for Combat are in the rulebook block (**3808–3832**). JSON alignment: `dungeon-mechanics.json` `expedition.teams[]` matches names, size bands, and shortened functions.

### 2.3 Time periods and assignment

> Each expedition day is divided into three periods: **morning, afternoon, and evening**  
> Characters can be assigned to different activities during each period  
> Some activities require multiple time periods to complete (e.g., deep research, long-distance scouting)

— `rulebook_output.txt` **3834–3837**

**Skill checks:** activities require appropriate skill checks; proficiency grants advantages; specialized tools may be required or grant bonuses (**3838–3841**).

**Activity results (benefits per team):** Combat → advancement, treasure, reputation, monster parts; Reconnaissance → maps, information, future encounter advantages; Research → knowledge, spell discoveries, historical context; Resource → food, materials, crafting components; Support → extended expedition duration, equipment bonuses, recovery (**3842–3848**).

### 2.4 Worked examples (rulebook)

Three full allocation examples — **Dungeon Exploration**, **Wilderness Expedition**, **Urban Investigation** — with 12-seat breakdowns including NPC specialists (**3849–3882**). Use these as RAW templates, not mandatory loadouts.

### 2.5 Benefits of role distribution

1. Resource efficiency — parallel gathering while combat advances  
2. Risk management — not all members exposed to the same dangers  
3. Downtime productivity — injured PCs contribute off-combat  
4. Narrative depth — non-combat engagement with the world  

— `rulebook_output.txt` **3883–3895**

### 2.6 Managing non-combat activities — resolution methods

| Method | Use |
|--------|-----|
| **Quick Resolution** | Simple skill checks with predetermined outcomes |
| **Scene-Based** | Brief RP scenes with key decision points |
| **Parallel Play** | Split session focus across teams |
| **Between-Session** | Resolve off-clock activities between sessions |

**Spotlight:** rotate detailed attention; use montages; players may control multiple characters across teams (**3896–3905**).

### 2.7 Expedition base camps

Operational centers with functions: safe rest, supply storage, workshop, team coordination (**3906–3912**).

**Types:** Temporary Camp · Fortified Outpost · Research Station · Forward Base (**3913–3917**).

### 2.8 Expedition advancement

Reputation, equipment/tools, base improvements, NPC specialist allies, logistics network (**3918–3923**).

### 2.9 Conclusion (organizational vs combat party)

> The **12-person expedition limit** in Decennium Descent represents a **complex organizational structure rather than simply a combat party size**. By strategically assigning characters to different activities, players can maximize their effectiveness, gather valuable resources, and create a more immersive and realistic adventuring experience. This system encourages creative problem-solving, teamwork, and engagement with all aspects of the game world **beyond combat**.

— `rulebook_output.txt` **3925–3926**

---

## 3. What is wired vs prose-only

| RAW element | Companion | Session UI |
|-------------|-----------|------------|
| Max 12 per Expedition | ✅ `expedition.maxSize` | ❌ No roster cap enforcement |
| Five teams + size bands | ✅ `expedition.teams[]` | ❌ No team assignment |
| Morning / afternoon / evening | ✅ `expedition.timePeriods[]` | ❌ No period scheduler |
| Skill checks & activity results | Prose only | ❌ |
| Examples, base camp types, advancement tracks | Prose only | ❌ |
| Parallel resolution methods | Prose only (GM procedure) | ❌ |
| Horn clock coupling to periods | Not in rulebook expedition block | Combat-centric horn only (`SESSION_LOOP.md`) |

**Display-only today:** Dungeon Guide → Overview → Expedition card shows summary + team grid from JSON.

**Product gaps (do not build UI in this pass unless trivial — listed for backlog):**

1. **Expedition roster manager** — assign up to 12 PCs/NPCs to teams  
2. **Day-period planner** — morning/afternoon/evening assignment per character  
3. **Off-combat activity tracker** — research/resource/support outcomes tied to horn hours or periods  
4. **Base camp tier** — temporary / fortified / research / forward base state  
5. **Multi-expedition coalition view** — link 2+ 12-seat expeditions without breaking RAW cap  

See also `docs/mechanics/SESSION_LOOP.md` § Gaps — "Expedition teams (combat vs recon)".

---

## 4. Relationship to other canon

| Doc | Relationship |
|-----|--------------|
| [`DESCENT_WINDOW_CANON.md`](./DESCENT_WINDOW_CANON.md) | Macro opening window (2400 h) and horn PoNR are **separate clocks** from expedition day periods |
| [`WORLD_DUNGEON_LOOP.md`](./WORLD_DUNGEON_LOOP.md) | GM loop — expedition structure persists across Cycle reshapes |
| [`SESSION_LOOP.md`](./SESSION_LOOP.md) | Session tab = combat + horn; expedition teams narrative-only today |
| [`HIDDEN_DUNGEON_EQUATION.md`](../playtest/HIDDEN_DUNGEON_EQUATION.md) | Sim synthesis — explicitly **not** a rulebook time equation for teams |

**Alignment compatibility (adjacent RAW):** `rulebook_output.txt` **3755–3777** — Good/Evil divide affects Expedition stability; Combat team should maintain alignment compatibility (**3811–3812**).

---

## 5. JSON alignment check

`src/data/dungeon-mechanics.json` `expedition` block **aligns** with rulebook team names, size bands, and period list. **Not ingested from rulebook at parse time** — maintained via `tools/ingest_lorebook.py` hard-code (same values). **Missing from JSON:** examples, resolution methods, base camp types, advancement tracks, skill-check procedure — correctly left as prose-only unless owner requests structured fields. **If JSON and rulebook diverge, rulebook wins** — reconcile JSON toward rulebook only with owner sign-off (see **Source of truth** above).

---

## 6. Playtest drift — not RAW

| Playtest | Roster | Status |
|----------|--------|--------|
| **T4 sims** (`T4_EXPEDITION_SCENARIO.md`, `T4_ROSTER.md`, `T4_EXPEDITION_PLAY_REPORT*.md`) | **24 PCs = 3×8 companies** | **Director/playtest exception** — tri-company coalition stress test; `T4_EXPEDITION_PLAY_REPORT_R2.md` explicitly notes 24 exceeds 12-seat cap. Model as **three coordinated 8-seat expeditions** (each under cap). **Q-OV-2 closed 2026-07-31:** owner locked **12 max** — do **not** promote 24-PC charter as RAW. |
| **Campaign sims #1–#4** (`SIM_01` … `SIM_04`, `SIM_CAMPAIGN_PLAN.md`) | **7–8 PCs** | **Valid under RAW** (under cap); sims used narrative team splits without Session UI support |
| **Fringe combat** (`EXPEDITION_SCENARIO.md`) | Smaller combat-focused table | Valid subset; does not exercise full 12-seat structure |

**Recommendation (owner-aligned):** RAW max **12 per Expedition**. Kingdom-scale or multi-company delves = **multiple expeditions coordinating** (shared base camp, staggered combat teams, coalition command) — not a single 24-seat roster.

Historical playtest logs are **intentionally not rewritten** (same policy as horn-clock drift in [`OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](./OWNER_COSMOLOGY_LOCKS_2026-07-30.md)).

---

## 7. Related docs

| File | Role |
|------|------|
| [`WORLD_DUNGEON_LOOP.md`](./WORLD_DUNGEON_LOOP.md) | Table loop wiring |
| [`SESSION_LOOP.md`](./SESSION_LOOP.md) | Session UI gaps |
| [`DESCENT_WINDOW_CANON.md`](./DESCENT_WINDOW_CANON.md) | Opening window + horn |
| [`A_TO_Z_MASTERY_DIGEST.md`](../playtest/A_TO_Z_MASTERY_DIGEST.md) | §3.3 digest pointer |
| [`SIM_CAMPAIGN_PLAN.md`](../playtest/SIM_CAMPAIGN_PLAN.md) | Campaign sim roster notes |
| [`READY_TO_CONTINUE.md`](../playtest/READY_TO_CONTINUE.md) | Agent lock list |
| [`src/data/dungeon-mechanics.json`](../../src/data/dungeon-mechanics.json) | Machine-readable subset |
| [`src/data/CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md) | Continuity stamp |
| [`CONTINUITY_DETAILED_CHECK.md`](./CONTINUITY_DETAILED_CHECK.md) | Oversight stamp |

*Stamp issued 2026-07-30 — owner re-assertion of rulebook RAW. No commit/push per brief.*
