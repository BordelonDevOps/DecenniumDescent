# Session loop — Expedition Session UI

**Surface:** `SessionTracker` (`/`, tab **SESSION**)  
**Storage:** `localStorage` key `dd_session_tracker`  
**Canon refs:** `floor-encounters.json`, `dungeon-mechanics.json`, `CONTINUITY_GLOSSARY.md`, rulebook Ch Oracle / Weave, [`EXPEDITION_STRUCTURE_CANON.md`](./EXPEDITION_STRUCTURE_CANON.md) (12-person teams — owner lock 2026-07-30)  
**Director defaults:** `src/lib/session-utils.ts` (2026-07-29)

---

## Intended table loop

1. **Set tier** — pick T1–T10; gate boss name + stub HP shown for quick add.
2. **Horn clock** — track Opening hours toward PoNR (`HORN_AT = 1200` in `SessionTracker.tsx`; Opening seals at **2400 h**). +8h on long rest. Soft quit at Floor 50 Canticle ≠ Horn. See [`DESCENT_WINDOW_CANON.md`](./DESCENT_WINDOW_CANON.md).
3. **Load party** — pull saved characters (localStorage `dd_characters`) or add manual allies.
4. **Add foes** — bestiary search or quick enemy / gate boss stub.
5. **Initiative** — auto-roll on add (d20 + Dex mod for saved chars); manual override supported.
6. **Combat rounds** — **Next turn** advances round when wrap completes; active combatant highlighted.
7. **Resources** — per-combatant **RP** (Weave) or **RC** (Oracle); optional party RP pool (sum of max).
8. **HP / conditions** — bump buttons, free-text conditions with quick-add chips.
9. **Rest** — Short rest (retune ¼ RP + RC +1) or Long rest (full RP/RC + 8h horn).

---

## Wired today

| Mechanic | UI | Rulebook / continuity |
|----------|-----|------------------------|
| Horn clock | Countdown, progress bar, ±1h / +8h on long rest | **1200 h / day 50** PoNR inside **2400 h** Opening → retreat or 10-year trap (`dungeon-mechanics.json` `hornRule`; `HORN_AT = 1200`) |
| Tier & gate boss | Tier picker, “Add Gate Boss” with tier-scaled stub HP | `gateBossStubHp(tier)` = 40 + tier×25 until bestiary wired |
| Initiative order | Sort high→low, turn pointer, round counter | d20 + Dex; ties: higher Dex → player add-order → allies before foes |
| HP track | Current/max, ±1 / ±5 | Stored `hp`/`maxHp` from save; fallback rulebook HD formula (`class-hit-dice.js`) |
| Party RP pool | Spend / gain / sync-to-max, living-caster sum display | Default cap = sum of living Weave casters' max RP |
| Per-combatant RP | Number field + max link | v1 canon — per-character RP from save or class max |
| Oracle RC | Per-combatant RC current/max, spend/regain | L1=3, +1 every odd level, cap 7 (`maxRevelationCharges`) |
| Short / long rest | Buttons in Party Resonance card | Short: ¼ max RP + RC+1; Long: full RP/RC + 8h horn |
| Conditions | Text + common quick-add chips | Freeform tracker (no automated condition rules) |
| Subclass identity | Badges: Oath, Circle, Mystery, Curse | Resolved from save ids → display names |
| Bestiary import | Search → HP from stat block or CR stub | Name, CR, zone in notes |
| Persist session | Auto-save to localStorage | Survives refresh |
| Scene notes | Textarea, persisted | Encounter brief / fiction beats |
| Encounter handoff | From generators → session | Sets tier + scene brief (`session-handoff`) |

---

## Director defaults (RESOLVED)

| Topic | Default | Implementation |
|-------|---------|----------------|
| **Party RP pool** | Per-character RP is v1 canon. Pool cap defaults to **sum of living Weave casters' max RP**; UI shows living casters' current RP sum for reference. | `sumWeaveCasterMaxRp`, `sumWeaveCasterCurrentRp` |
| **HP import** | Use stored `hp`/`maxHp` when present. Fallback: **rulebook Ch3 HD** — L1 = max die + CON; each level after = avg die + CON (`estimatePcMaxHp` → `class-hit-dice.js`, all 17 CANON_CLASSES). | `resolvePcHp`, `estimatePcMaxHp` |
| **RC scaling** | L1 = 3, +1 every odd level, max 7. | `maxRevelationCharges(level)` |
| **Rest economy** | Short: retune ¼ max RP (Weave) + RC +1 to max (Oracle). Long: full RP/RC + 8h horn. | `applyShortRest`, `applyLongRest`, Session buttons |
| **Initiative tie-break** | Higher initiative → higher Dex → player add-order (allies before foes). | `compareInitiativeOrder` |
| **Gate boss stub stats** | `40 + tier×25` HP placeholder; label notes bestiary when ready. | `gateBossStubHp` |

---

## Gaps (not blocking playtest stub)

| Gap | Severity | Notes |
|-----|----------|-------|
| Multiclass HP | Low | Fallback uses primary class HD only — no per-class level split on import |
| Spell / Revelation casting | Out of scope | No spell picker in session — table resolves at narration |
| Death saves / downed | Low | HP 0 shown visually; no death-save automation |
| Condition mechanics | Low | Labels only — no duration, saves, or stacking rules |
| Enemy conditions & RP | N/A | Foes don't use RP/RC |
| Expedition teams (combat vs recon) | Low | `dungeon-mechanics.json` defines teams; Session assumes combat table only — full RAW in [`EXPEDITION_STRUCTURE_CANON.md`](./EXPEDITION_STRUCTURE_CANON.md) §3 |

---

## Terminology (Continuity)

| Use | Avoid for Oracle |
|-----|------------------|
| **Resonance Points (RP)** | — |
| **Revelation Charges (RC)** | “Spell slots”, “RP”, “Weave charges” |
| **Mystery Revelations** | Generic “spells” without Mystery context |
| **Party Resonance** | Shared pool display — per-character RP remains v1 canon |

Oracles: `spell-utils.js` excludes Oracle from Weave casters; session shows **RC** column, not RP.

---

## Collaborator quick start

1. Build & **SAVE** characters in **CHARACTERS**.
2. Open **SESSION** → add saved PCs → add monsters from bestiary.
3. Roll/adjust initiative → **Next turn** during fights (note tie-break under Round / Turn).
4. Track horn hours as GM narrates delves; use **Long rest (+8h)** between delves.
5. Spend **Party RP** for Weave effects; adjust per-PC **RP** or Oracle **RC** manually.
6. **Short rest** between fights for partial RP/RC recovery.
7. Tap condition chips or type custom conditions.

---

*Last updated: 2026-07-30 — expedition structure canon cross-link*
