# Newcomer GM guide — Decennium Descent

**Audience:** First-time GMs running a Decennium Descent table with the Next.js companion  
**Scope:** Session zero, Resonance basics, Session tracker workflow, bestiary/combat data hygiene, common friction from playtest  
**Companion app:** `npm run dev` → `http://localhost:8500` (port **8500**)  
**Do not commit/push** unless the owner asks.

---

## Before you sit down (one-page checklist)

Print or keep this open beside the Session tab.

| ☐ | Task | Where / note |
|---|------|--------------|
| ☐ | **Dev server running** | `npm run dev` in `DecenniumDescent-main` |
| ☐ | **Characters built and SAVED** | **CHARACTERS** tab → each PC named → **SAVE** (localStorage `dd_characters`) |
| ☐ | **Session zero Resonance briefing done** | See [§ Session zero](#session-zero--resonance-101) — ban “spell slots” for Weave casters |
| ☐ | **Oracle vs Weave clarified** | Oracles = **RC** (Revelation Charges), not RP |
| ☐ | **Tier + horn clock set** | **SESSION** → tier picker; reset or set hours (120 h gate delves; fringe scenarios may use shorter budgets — see scenario brief) |
| ☐ | **Scene brief loaded** | Encounters/Generators **Load in Session** *or* paste into Scene notes |
| ☐ | **Foes from bestiary** | Search → add; confirm **AC/HP**; note **`combat.draft: true`** on sandbox rows |
| ☐ | **Paper death-save tracker** | Session shows 0 HP visually; **no death-save automation** |
| ☐ | **Umbrin / sunlight ruling** | Pre-agree dim vs direct sunlight for the opening scenes |
| ☐ | **Draft XP expectations** | Awards are **session tally only** — apply level XP in Builder manually |
| ☐ | **Class ceiling caps** (if needed) | Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker — informational only |
| ☐ | **Cheat sheet for casters** | [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) (one page) |
| ☐ | **Optional clean slate** | DevTools → clear `dd_characters`, `dd_session_tracker` if you want a fresh run |

**Minimum viable first session:** 2–4 saved PCs → **SESSION** → add PCs → one bestiary encounter → initiative → **Next turn** → track HP + RP/RC → short rest between fights.

---

## Session zero + Resonance 101

Run this **before** dice hit the table. Goal: 5e veterans unlearn “slots”; newcomers learn **one pool**.

### Frame the game (2 minutes)

- **Setting hook:** Aethel, Shardspire delves, Choir/Weave cosmology — pick one sentence from **Cosmology** or your scenario brief ([`EXPEDITION_SCENARIO.md`](./EXPEDITION_SCENARIO.md) is a worked fringe example).
- **Companion role:** Character builder + session tracker + reference library — **not** a VTT with automated rules. You narrate; the app tracks HP, initiative, horn hours, RP/RC, and labels.
- **Draft honesty:** UI badges `(draft)` on non-canon pool tables, bestiary combat, XP awards, and some subclass trees. Say so up front so players trust canon numbers (Cleric/Mage/Wizard/Druid RP) vs draft numbers (Bard, Monk, etc.).

### Resonance briefing (Weave casters)

**Canon:** Hybrid-B **Resonance Points (RP)** — one fungible pool, not Vancian slots ([`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md), [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md)).

| Teach this | Not this |
|------------|----------|
| **One RP pool** per Weave caster | “You have four 1st-level slots” |
| **Cantrips = 0 RP** | Every cast spends a “slot” |
| **Cost ≈ spell level × 2** (± affinity, opposition, faction rep) | Flat 1 RP per level |
| **Short rest = Retune** — ≈¼ max pool + casting ability mod (+ Nature Circles rep) | Full slot recovery on short rest |
| **Long rest = Full harmony** — pool to max; Session also **+8 h horn** | — |
| **Retune is free** during a short rest (playtest default; no authored action cost) | Retune costs an action mid-fight |

**L3 canon pools (reference):** Cleric **7** · Mage **8** · Wizard **10** · Druid **7**.  
**Draft pools (UI flagged):** Bard, Paladin, Ranger, Shaman, Mirrorsage, Crimson Agent, Dragoon, Monk, Thief, Tinker — derived from Cleric curve × tier multiplier; treat as playtest numbers.

**Classes with no RP column:** **Oracle** (RC), **Warrior**, **Soldier** — Session is correct when those rows show no RP.

**Separate resources:** Bard **Crescendo**, Paladin **Lay on Hands**, Warrior **mutations**, Monk **Ki Chain** / stances, etc. — not RP. Point players to their sheet features.

### Oracle briefing (30 seconds)

| | Weave casters | Oracle |
|---|---------------|--------|
| Resource | **RP** | **Revelation Charges (RC)** — start 3, max 7 (L1 = 3, +1 every odd level) |
| Spend on | Prepared Weave spells | **Mystery Revelations** (1 / 2 / 3 RC by tier) |
| Recovery | Retune / full harmony | Each Mystery’s **Prophecy Trigger** — **not** rest-based in design |
| Companion convenience | — | Session **Short rest** grants **RC +1** toward max ([`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md)) — tell Oracles this is a table aid, not canon recovery |

**Never call RC “spell slots” or RP.**

### Chargen expectations

Walk the table through **CHARACTERS** once ([`CHARGEN_PROGRESSION.md`](../mechanics/CHARGEN_PROGRESSION.md)):

1. **People** → lineage → abilities  
2. **Class** (17 canon only) → L3 is a good first playtest level (subclass/oath/mystery tiers online)  
3. **Paths / Features** — Oracle Mystery + Curse L1; Paladin Oath L3; Druid Circle L2; `(draft)` badges OK  
4. **Weave** tab (RP) or Oracle revelations (RC)  
5. **SAVE** — required before Session can load the PC  

Optional: [`PLAYTEST_SMOKE.md`](../mechanics/PLAYTEST_SMOKE.md) (~15 min) if you want a solo dry run.

---

## Death saves and 0 HP

**Rulebook canon** (`rulebook_output.txt` § Dropping to 0 Hit Points / Death Saving Throws; summarized in [`COMBAT_SYSTEM_COMPARE.md`](../mechanics/COMBAT_SYSTEM_COMPARE.md)):

| Situation | Rule |
|-----------|------|
| Damage to 0 HP, remainder **< max HP** | Unconscious; **death saves** at start of each of your turns |
| Damage to 0 HP, remainder **≥ max HP** | **Instant death** |
| Death save | d20, no mod unless a feature grants one; **10+** success, **9−** failure |
| **3 successes** | Stable (unconscious, no more saves) |
| **3 failures** | Dead |
| Nat **1** | Counts as **2** failures |
| Nat **20** | Regain **1** HP |
| Damage while at 0 HP | **1** failure (**2** if crit); instant death if damage ≥ max HP |
| **Healing** any HP while at 0 | Regain consciousness; **death saves reset** (5e-style — used at EXP-BGR-01 table) |
| **Stabilize** | Action + DC 10 WIS (Medicine); stable = unconscious, no saves; 1 HP after 1d4 hours |
| **Monsters** | Usually die at 0 HP |

**Session tracker:** HP can go to 0; **no death-save counter**. Use scratch paper or chips. Call out saves loudly — playtest showed twice-downed parties in hard fights.

**Healing priority:** Remind support players: **Healing Word on a healthy ally while another PC is at 0** is a common novice mistake ([`EXPEDITION_FRICTION_LOG.md`](./EXPEDITION_FRICTION_LOG.md)).

---

## Rests — table vs companion

### What the rulebook / Resonance canon says

| Rest | RP (Weave) | Oracle RC | Other |
|------|------------|-----------|-------|
| **Short rest** (“Retune”) | ≈¼ max + casting mod (+ Nature Circles rep) | Design: trigger-based; Session grants **+1 RC** | Class features (Second Wind, etc.) — **manual** |
| **Long rest** (“Full harmony”) | Full RP | Full RC in Session | **+8 h horn** in Session |

**Not in Session UI (call out explicitly):**

- **Hit Dice** spending on short rest (5e habit) — **not wired**; only Retune/RC bump applies  
- **Automatic concentration** tracking — **manual** (label e.g. `Concentration: Bless` in conditions)  
- **Meditation** recovery (10 min, 1/day, casting mod only) — documented, **not wired**

### Horn clock

- **Full gate delve:** Opening **2400 hours**; Horn PoNR at **1200 hours / day 50** → retreat or **10-year trap** ([`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md), `dungeon-mechanics.json`). Soft quit at Floor 50 Canticle ≠ Horn — see [`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md).
- **Cycle opening:** When the Shardspire activates, the Great Descent stays open **100 days (2400 hours)** before sealing ([`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md)).  
- **Long rest** in Session: **+8 h** on horn.  
- **Fringe / scenario clocks:** Shorter on-site budgets are valid (e.g. EXP-BGR-01 uses **16 h** on-site — not the 120 h gate rule). Set expectations in session zero.

---

## Session tracker tips

**Surface:** **SESSION** tab (`SessionTracker`) · persists to `localStorage` `dd_session_tracker`  
**Deep reference:** [`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md)

### Recommended loop

1. Set **tier** (T1–T10) and **horn hours**  
2. **Add saved characters** (must be SAVED in CHARACTERS first)  
3. **Add foes** — bestiary search or gate-boss stub  
4. **Initiative** — auto d20+Dex on add; override as needed; **Next turn** advances round  
5. Fight — HP ± buttons, spend **RP** or **RC**, type **conditions**  
6. **Short rest** / **Long rest (+8h)** between scenes  
7. **Award draft XP** when a foe hits 0 HP (optional tally)

### RP vs Oracle RC

| Column | Who | Notes |
|--------|-----|-------|
| **RP** (purple) | Weave casters (Wizard, Mage, Cleric, Druid, Bard, …) | Per-character pool is v1 canon; party pool display = sum of living casters’ **max** for reference |
| **RC** (violet) | **Oracle only** | L3 example: **4 / 4** (3 + 1 at odd level) |
| *(no pool)* | Warrior, Soldier | Correct — use class features, not RP |

**Terminology** ([`CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md)):

- Say **Resonance Points (RP)** and **Revelation Charges (RC)**  
- Avoid **“spell slots”**, **“Weave charges”** for Oracle  

**Initiative tie-break:** higher initiative → higher Dex → add order → **allies before foes**.

### Draft XP awards

**Status:** **Not canon** — playtest tally only ([`XP_ADVANCEMENT_CANON.md`](../mechanics/XP_ADVANCEMENT_CANON.md)).

- When a foe reaches **0 HP**, click **Award draft XP** on that row  
- Appends a line to **Scene notes** and adds **`draftXpSession`** per participating PC  
- **Does not** write XP to character saves — update levels in **CHARACTERS → Advancement** manually  
- Split rule (draft): total CR-based XP **÷ party size**, round down  
- **Confirmed canon:** L1–L20 **threshold table** only (e.g. L3→L4 = **1,800** XP gap)

Tell optimizers: milestone leveling is fine if you skip draft XP entirely.

### Conditions as labels

- Conditions are **free text + quick-add chips** — not automated rules  
- Common chips: Prone, Blessed, Poisoned, Stunned, Feared, Blinded, Restrained, Invisible, Dazed, Slowed (`session-utils.ts`)  
- Use for **concentration**, **Stunned 1 round** rulings, **Sunlight** reminders, etc.  
- **No duration, saves, or stacking** — you adjudicate  

**Also manual:** death saves, Bardic Inspiration, Ki, Momentum, mutation activations/round, class ceiling caps.

---

## Bestiary — Excel-first, draft combat

**Authoring source of truth:** `Bestiary.xlsx` (`Monsters` sheet) — **not** hand-edited JSON ([`BESTIARY_INGEST.md`](../mechanics/BESTIARY_INGEST.md)).

| Step | Command / action |
|------|------------------|
| Edit stats | Excel → AC, HP, attacks, recharge columns |
| Rebuild JSON | `python scripts/ingest_bestiary_from_excel.py` or `npm run ingest:bestiary` |
| Regenerate draft combat columns | `python scripts/generate_bestiary_combat_sandbox.py` (backs up first) |

**At the table:**

- **`combat.draft: true`** / `source: excel-sandbox` — CR-band generated; validate AC, HP, attack names  
- **Gate guardians** (10 named bosses) — authored CR/XP/combat; Excel wins when populated  
- **698+** rows carry sandbox combat; names may still show pre-scrub labels (e.g. “Freak Bite”) — acceptable draft placeholders  
- **Recharge** abilities (e.g. Gloom Weaver *Shadow Weave* ~33% probability in sim) — roll at table; Session does not auto-recharge  
- **Low-CR HP tuning** (draft % bumps CR ≤ 3) may inflate HP — note when fights run long  

**Session import:** Bestiary search pulls **AC, HP, CR** into combatants; adjust initiative/HP/conditions live.

**Not proof of balance:** Combat sim and EV party-loss % are planning sketches ([`BALANCE_COMBAT_SIM.md`](../mechanics/BALANCE_COMBAT_SIM.md)).

---

## Class ceiling caps (informational)

**Status:** Draft playtest guardrails — **not canon**, **not enforced** in Session ([`CLASS_CEILING_CAPS.md`](../mechanics/CLASS_CEILING_CAPS.md)).

Builder/Sheet show **Draft ceiling caps** for six outlier classes. Use when a player asks “can I do this twice in one round?”

| Class | Example cap (draft) |
|-------|---------------------|
| **Warrior** | **1 mutation activation / round**; Action Surge + 1 mutation max same round |
| **Oracle** | **1 Revelation activation / round**; RC recovery from triggers **1 / round** combined |
| **Paladin** | Extra Attack + **1** smite **or** 1 leveled spell rider; one aura bonus active |
| **Mirrorsage** | **1** copy release / round; echo slot limits |
| **Dragoon** | Momentum cap 5 (6 L13+); **1** Wyvern’s Flow **or** Apex Assault / round |
| **Tinker** | **3** concurrent deployables; **1** deploy + **1** detonation / round |

When prose and caps conflict during playtest, **caps win**; log conflicts for author review.

---

## Umbrin + Sunlight Sensitivity

**Product race:** **Umbrin** (The Murk) — locked lore [`UMBRIN_LORE.md`](../mechanics/UMBRIN_LORE.md). Traits on sheet: Superior Darkvision, **Sunlight Sensitivity**, Umbrin Magic, Umbrin Weapon Training (`races.js`).

### Sunlight Sensitivity (rule text)

From racial trait (compendium / Umbrin ingest):

> You have **disadvantage on attack rolls** and on **Wisdom (Perception) checks that rely on sight** when you, the target of your attack, or whatever you are trying to perceive is in **direct sunlight**.

**GM callouts:**

- **Pre-brief in session zero** if any PC is Umbrin — players forget mid-scene ([`EXPEDITION_FRICTION_LOG.md`](./EXPEDITION_FRICTION_LOG.md) #P1-6).  
- **Scene lighting:** Overcast dusk, torchlit caverns, mixed darkvision → often **no penalty**; open bridge at noon → **yes**. Document your ruling once per location.  
- **Not automated** in Session — note `Sunlight` in conditions if needed.  

### Table / social notes

- Umbrin face **Disliked/Hated** bias from mainstream factions — roleplay via [`UMBRIN_LORE.md`](../mechanics/UMBRIN_LORE.md) reputation table; no hard race lock in `reputation.js`.  
- **Murkish** language and Obsidian Burn lore are engagement hooks, not mechanical buffs unless you grant them.  
- **Two Umbrin in one party** is fine (EXP-BGR-01 did) — double-check sunlight scenes affect both.

---

## Common table failures (EXP-BGR-01)

From [`EXPEDITION_FRICTION_LOG.md`](./EXPEDITION_FRICTION_LOG.md) — use as a “watch list” for your first session.

### Player confusion (high impact)

| Failure | Who | Fix at table |
|---------|-----|--------------|
| **RP called “spell slots”** | Novice + 5e cleric | Repeat: **one pool**; cantrips **0 RP**; show [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) |
| **Draft vs canon pool trust** | Bard (draft 4) vs Cleric (canon 7) | Point to `(draft)` badge; don’t promise parity |
| **Healing healthy ally at 0 HP crisis** | Novice bard | “Who is dying?” before accepting heal |
| **Bardic Inspiration on self pre-fight** | Novice | Remind: support is for allies |
| **Hit Dice on short rest** | 5e cleric | “Retune only — no HD button in app” |
| **Expected full slot recovery on Retune** | 5e cleric | Show partial math: ¼ max + WIS |
| **Death saves not in app** | All | Paper tracker + verbal countdown |

### Rules / adjudication gaps

| Topic | Playtest call |
|-------|---------------|
| Retune action cost | **Free** during short rest |
| Healing at 0 HP | Any HP ends death saves (5e-style) |
| Concentration broken | Manual; remove condition label |
| Monk % crit / DR in prose | Narrative until executable |
| Combo Step stun duration | Table: **1 round** (example DC 13 WIS) |
| Flanking / flat-footed | **No flanking**; Help action OK |
| Sunlight | Per-scene lighting ruling |
| Shadow Weave–style AoE | Full-party save when ability says so |
| Draft XP 387/PC | Label **draft**; not milestone promise |

### System / companion

| Gap | Workaround |
|-----|------------|
| No death-save automation | Scratch paper |
| No Hit Dice on rest | Narrate HD if you house-rule; app won’t track |
| Conditions = labels only | You enforce duration/saves |
| Bestiary placeholder attack names | Accept or rename in notes |
| Warrior **CLASS_CEILING_CAPS** | Enforce **1 mutation / round** for optimizers |

**Balance note:** EXP-BGR-01 L3 party (**101 HP**) took **~93% EV party HP** across three fights — **lethal if naive**; viable with focus fire, Retune, and heals. Ease up for P1-heavy tables (fewer foes, short rest after E1).

---

## First session run sheet (90-minute sketch)

| Phase | Time | GM actions |
|-------|------|------------|
| **Session zero** | 20 min | Safety, tone, Resonance 101, Oracle RC if needed, Umbrin sunlight, companion tour |
| **Chargen or load** | 15 min | Pre-gens OK — [`EXPEDITION_SCENARIO.md`](./EXPEDITION_SCENARIO.md) + character stubs in `docs/playtest/characters/` |
| **Scene 1** | 20 min | Load Session → 1 moderate encounter → Award draft XP → Short rest |
| **Scene 2** | 20 min | Harder encounter → check RP/HP → Long rest only if fiction allows (+8 h horn) |
| **Debrief** | 15 min | What confused people? Note friction for next time |

**Starter scenario:** [`EXPEDITION_SCENARIO.md`](./EXPEDITION_SCENARIO.md) (Glassbite Hollow, 3 fights, 16 h on-site clock).  
**After action:** [`EXPEDITION_PLAY_REPORT.md`](./EXPEDITION_PLAY_REPORT.md) template style — optional notes file for your table.

---

## Related docs (quick index)

| Topic | Doc |
|-------|-----|
| Resonance canon | [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) |
| Resonance one-pager | [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) |
| Session UI loop | [`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md) |
| World / dungeon frame | [`WORLD_DUNGEON_LOOP.md`](../mechanics/WORLD_DUNGEON_LOOP.md) |
| Expedition teams (12 max) | [`EXPEDITION_STRUCTURE_CANON.md`](../mechanics/EXPEDITION_STRUCTURE_CANON.md) — not every PC fights at once; Session UI is combat-only |
| XP canon vs draft | [`XP_ADVANCEMENT_CANON.md`](../mechanics/XP_ADVANCEMENT_CANON.md) |
| Bestiary pipeline | [`BESTIARY_INGEST.md`](../mechanics/BESTIARY_INGEST.md) |
| Class caps | [`CLASS_CEILING_CAPS.md`](../mechanics/CLASS_CEILING_CAPS.md) |
| Umbrin lore | [`UMBRIN_LORE.md`](../mechanics/UMBRIN_LORE.md) |
| Playtest friction log | [`EXPEDITION_FRICTION_LOG.md`](./EXPEDITION_FRICTION_LOG.md) |
| Collaborator onboarding | [`COLLABORATOR_ONBOARDING.md`](../COLLABORATOR_ONBOARDING.md) |

---

## Continuity stamp

| Field | Value |
|-------|-------|
| **Agent** | Playtest docs — newcomer GM guide |
| **Date** | 2026-07-30 |
| **Deliverable** | `docs/playtest/NEWCOMER_GM_GUIDE.md` |
| **Sources** | `RESONANCE_CANON.md` · `SESSION_LOOP.md` · `rulebook_output.txt` (death saves) · `rulebook_output.txt` (Sunlight Sensitivity) · `UMBRIN_LORE.md` · `BESTIARY_INGEST.md` · `CLASS_CEILING_CAPS.md` · `XP_ADVANCEMENT_CANON.md` · `EXPEDITION_FRICTION_LOG.md` · `EXPEDITION_PLAY_REPORT.md` · `EXPEDITION_SCENARIO.md` · `RESONANCE_CHEATSHEET.md` · `CHARGEN_PROGRESSION.md` · `COMBAT_SYSTEM_COMPARE.md` · `session-utils.ts` · `SessionTracker.tsx` |
| **Draft flags** | 10 Weave RP pool tables · bestiary sandbox combat · draft XP awards · class ceiling caps · Burnout consequences · Oracle RC +1 on short rest (companion convenience) |
| **No commit/push** | Per playtest brief |
