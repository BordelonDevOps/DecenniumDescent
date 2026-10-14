# Player 2 — Casual D&D 5e

> **Historical rules snapshot:** This report preserves the terminology and mechanics used when the simulation was run. Current magic canon is [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md): RP + Dissonance/Refrain, no automatic alignment/reputation spell pricing, and Low Resonance instead of the retired Burnout subsystem. Historical observations remain useful, but superseded magic rulings are not current RAW.


**Persona:** You have a few years of D&D 5e under your belt (likely a cleric or paladin at someone else's table). You know the basics — action economy, concentration, short vs long rest — but you don't optimize builds or read every subclass online. You want a **reliable party role** (healer + buffer) and you default to "what worked in 5e."

**Expedition:** Blackglass Reach **fringe** — surface marches near The Murk: dark-glass outcrops, trade watchposts, oath-law mercenary traffic. Three **non-boss** fights, party **L3**. (`EXPEDITION_SCENARIO.md` not yet on disk; this sheet matches that brief.)

**Companion save name suggestion:** `P2 Helga Stoneprayer`

---

## Character choice

| Field | Pick | Why (5e brain) |
|-------|------|----------------|
| **People** | **Dwarf** | Stout, armored, hard to kill — classic PHB cleric vibe. |
| **Lineage** | **Mountain Dwarf** | `racial-variants.json`: Stoneheart (+15% knockback/immobilize resist), Forge racial feat. Reads like the dwarf who stays on the front line. |
| **Class** | **Cleric** (L3) | The 5e support default: armor, shield, heals, Bless, Channel Divinity. Full **canon RP table** in `resonance-economy.js` (unlike 10 draft-pool casters). |
| **Divine Domain** | *Life* (assumed) | You'd pick Life or War in 5e. Domain spells/features are **not fully wired** in the Builder (`BALANCE_PLAYER_CLASSES.md`: "domain numbers incomplete"). **Table fiction:** Life Domain — extra healing on *Cure Wounds*, Channel Divinity = Preserve Life–style burst. Confirm with DM. |
| **Background** | **Frontier Settler** | Fits Blackglass fringe: Survival, Animal Handling, improvised gear. You'd rather be useful between fights than debate theology. |
| **Alignment** | Lawful Good | Mainstream Choir sympathy; expect **Religious Orders** rep to help spell costs slightly if you're Liked+. |

---

## Ability scores (standard array, dwarf cleric)

Casual placement — max Wis, enough Con to survive, Str for mace:

| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| 14 | 10 | 14 (+2 Dwarf → **16**) | 10 | 15 | 8 |

- **CON mod:** +3  
- **WIS mod:** +2  
- **Proficiency:** +2 (L3)

---

## Sheet sketch (L3)

### Vitals

| Stat | Value | Notes |
|------|-------|-------|
| **HP** | **27** | Rulebook HD: d8 max + CON at L1, then avg d8 + CON ×2 (`class-hit-dice.js`: 8+3 + 2×(5+3)). |
| **AC** | **17** | Scale mail 14 + shield +2 + Dex 0 (medium armor). Swap to chain if loot is lighter. |
| **Speed** | **25 ft** | Dwarf base. |
| **Initiative** | +0 | Dex 10 — you'll go mid-pack; fine for a cleric. |
| **Spell save DC** | **12** | 8 + 2 prof + 2 Wis. |
| **Spell attack** | **+4** | 2 prof + 2 Wis. |

### Proficiencies & traits

- **Armor:** light, medium, shields  
- **Weapons:** simple  
- **Skills (class):** Religion, Insight *(pick 2 from Cleric list — you'd take Medicine if someone told you to)*  
- **Skills (background):** Survival, Animal Handling  
- **Dwarf:** Darkvision, Dwarven Resilience, Dwarven Combat Training, Stonecunning  
- **Mountain Dwarf:** Stoneheart; racial feat **Forge** (fire resist +10%, crafted armor durability — percentage wording is a DD quirk vs flat 5e resistance)

### Class features (L1–L3)

- **Spellcasting** (prepared divine spells — see Resonance below)  
- **Divine Domain** (Life, table-assumed)  
- **Channel Divinity** (1/short rest): Turn Undead *or* domain option  
- **L3:** access to **2nd-circle** domain spells (e.g. *Lesser Restoration*, *Spiritual Weapon* in a 5e Life list — confirm with DM)

### Cantrips (0 RP each)

| Cantrip | Use |
|---------|-----|
| **Sacred Flame** | Dex save radiant damage when you can't reach melee — your default "I attack on my turn." |
| **Light** | Fringe tunnels and dusk marches. |
| **Thaumaturgy** | Flavor / intimidation at oath-law checkpoints. |

### Prepared spells (5e habit: Wis mod + level = **5** prepared)

You'd prepare these every day:

| Spell | Circle | RP cost (base) | 5e role |
|-------|--------|----------------|---------|
| **Bless** | 1st | **2 RP** | Pre-combat buff; concentration. |
| **Cure Wounds** | 1st | **2 RP** | Touch heal after the fight or when safe. |
| **Healing Word** | 1st | **2 RP** | Bonus action pick-up — your panic button. |
| **Shield of Faith** | 1st | **2 RP** | +2 AC on the squishiest ally; concentration. |
| **Spiritual Weapon** | 2nd | **4 RP** | Action to cast; bonus action to attack — your "always something to do" spell. |

**Domain spells** (if DM grants Life): likely *Bless* always prepared, *Cure Wounds* always prepared — ask if those count against your 5.

### Resonance Points (RP) — **not spell slots**

| | |
|--|--|
| **Max RP (L3 Cleric)** | **7** (`CANON_POOL_TABLES.Cleric[3]`) |
| **Cantrips** | 0 RP |
| **Typical day budget** | ~3 first-circle casts **or** 1 second-circle + 1 first **or** mix — *not* "3 slots of each level" |

**Your mental model (wrong):** "I have three 1st-level slots and two 2nd-level slots."  
**DD truth:** One pool. Spend **2 RP per spell circle** (before affinity/rep tweaks). At 7 RP you cannot spam five different 1st-level spells *and* Spiritual Weapon without resting.

**Short rest ("Retune"):** ~**¼ max RP** + WIS mod (+ Religious/Nature rep if applicable) — at L3 that's about **1 + 2 = 3 RP** back, **not** full slots.  
**Long rest ("Full harmony"):** restore to 7 RP.

Track RP in the companion **Session** tab; label says **RP**, not slots.

---

## Combat plan (standard 5e cleric tactics)

You play the same role every fight; only the opening changes if you're surprised.

### Before contact

1. If you have a round: **Bless** on two frontliners (concentration).  
2. Tell the party: "I'm on Healing Word; yell when you're down."

### Round-by-round (typical)

| Priority | Action | Bonus | Notes |
|----------|--------|-------|-------|
| 1 | **Spiritual Weapon** on the scariest target *or* **Sacred Flame** if RP is tight | — | SW costs 4 RP — save for fights 2–3, not every skirmish. |
| 2 | Maintain concentration (Bless *or* SW — not both in 5e; pick one) | **Healing Word** if ally ≤ 0 HP | Bonus-action heal is non-negotiable. |
| 3 | **Sacred Flame** or mace if in melee | — | Sacred Flame = no RP; use when conserving pool. |
| 4 | **Shield of Faith** on tank if no Bless and someone is getting focused | — | Second concentration — only if Bless isn't up. |
| 5 | **Channel Divinity** if undead or big heal needed | — | 1/short rest — you'd use this like 5e, expecting it back on short rest (that part *does* match). |

### Between the three fringe fights

- **5e habit:** "We short rest — I get slots back."  
- **What you actually get:** ~3 RP via Retune + Channel Divinity back. **Plan RP across all three fights.**  
- **After fight 3:** long rest or camp; push for **Full harmony** before the next delve day.

### Positioning

- Stay **30–60 ft** behind frontline — Healing Word range, Sacred Flame range.  
- Use **cover** on the glassy marches (5e half cover +2 AC still applies per `COMBAT_SYSTEM_COMPARE.md`).  
- **Do not** walk up for *Cure Wounds* mid-fight unless the map is safe — that's 5e learning you'd still do.

### What you leave to others

- Face control, marks, stealth — not your job.  
- You call targets only when someone is dying: "Healing Word on [name], focus the one that dropped them."

---

## Roleplay & suboptimal-but-human choices

- You **Bless first** even when the DM hints at ambush — it's your ritual.  
- You **overcast** only if someone explains Empowered/Widened in the moment; otherwise you ignore the Session overcast row.  
- You refer to RP as **"slots"** out loud at least once; the table corrects you.  
- You offer to **short rest after fight 1** even when the horn clock or scenario pressure says keep moving.  
- On Blackglass fringe you'd **trade politely** at a watchpost, not roleplay Umbrin politics — you're a dwarf from the settlements, not a Murk native.

---

## Where DD rules will surprise you

| 5e expectation | DD reality | Playtest impact |
|----------------|------------|-----------------|
| Spell **slots** by level | **Resonance Points** — single pool, cost = circle × 2 | You burn out mid-expedition if you treat 7 RP like "7 first-level slots." |
| Short rest = warlock slots / some features | **Retune** ≈ ¼ pool + mods — Cleric gets partial RP, not full | Fight 2 hurts if you dumped RP in fight 1. |
| Long rest = everything back | **Full harmony** restores RP; horn clock +8h in dungeon sessions | Surface fringe may be looser — ask DM if horn applies. |
| Cleric domain is in the book | Domain **incomplete in companion data** | Confirm Life features with DM; don't assume Builder shows them. |
| Flat resistance (e.g. fire) | Some traits use **+10% resist** language | Ask how percentages map at the table. |
| Oracle = divine caster like you | Oracle uses **Revelation Charges (RC)**, not RP | Don't tell P1's Oracle to "save a slot." |
| Party spell slot pool | **Per-character RP** is v1 canon; Session may show party sum for reference | Track *your* 7 RP. |
| Reputation is flavor | **Religious Orders** ±1 RP on spell cost; retune tracks differ by class | Good-aligned cleric near mainstream temples = slightly cheaper casts. |
| Overcast at low level | Below 25% max RP risks **Burnout** badge | At 7 RP, dropping to 1 RP after a 4 RP cast triggers warning — you won't expect that from 5e. |
| Death at 0 HP | Death saves exist in rules; **Session tracker doesn't automate them** | Call out successes/failures manually. |
| XP after fights | **Draft** CR→XP in `xp-economy.js` — awards may land in scene notes only | Don't expect auto level-up on the sheet. |
| Class ceiling caps | Informational only (`CLASS_CEILING_CAPS.md`) — not enforced in app | DM may still use them for outliers (not you). |

---

## Companion build checklist

1. **CHARACTERS → NEW**  
2. **People:** Dwarf → **Mountain Dwarf**  
3. **Class:** Cleric → level **3**  
4. **Past:** Frontier Settler; set **Religious Orders** rep if your background grants it  
5. **Abilities:** array above (or 27-point buy Wis 16, Con 14 before racial +2)  
6. **Weave tab:** note **max RP 7**; prepare spells from list above  
7. **Save** → load in **SESSION** for RP tracking and Retune/Full buttons  

---

## Questions you'd ask the DM (5e phrasing)

1. "Do I have **three first-level slots** or is it this RP thing?"  
2. "Does **Bless** stack with your bless from the app, or is it the same spell?"  
3. "Short rest between fights — do I get **all** my spells back or just Channel Divinity?"  
4. "Is **Spiritual Weapon** still a bonus action to attack after I cast it?" *(Yes — 5e-shaped action economy.)*  
5. "Are there **undead** on the fringe, or should I prepare something else for Channel Divinity?"  
6. "Does the **120-hour horn** apply if we're not in the Decennium proper?"  

---

## Party fit

You anchor **healing and morale** for a L3 party of four. You expect one martial frontliner, one striker or rogue-type, and one arcane caster (Mage/Wizard) who burns RP faster than you. You don't optimize synergies — you **Bless who stands next to you** and **Healing Word whoever hits zero**.

*No git commit — playtest artifact only.*
