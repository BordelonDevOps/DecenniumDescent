# Playtest smoke path (~15 minutes)

**App:** Decennium Descent companion (`DecenniumDescent-main`)  
**URL:** `http://localhost:8500` (`npm run dev`)  
**Goal:** Confirm chargen → save → session → encounter handoff → dungeon reference works without crashes.  
**Refs:** [`SESSION_LOOP.md`](./SESSION_LOOP.md) · [`CHARGEN_PROGRESSION.md`](./CHARGEN_PROGRESSION.md)

---

## Before you start

| Check | Command / action |
|-------|------------------|
| Dev server | `npm run dev` in repo root (port **8500**) |
| Clean slate (optional) | DevTools → Application → Local Storage → clear `dd_characters`, `dd_session_tracker`, `dd_session_encounter_handoff` |
| Typecheck | `npx tsc --noEmit` should exit 0 |

---

## Path A — Umbrin Oracle (~8 min)

### 1. Create character (3 min)

1. Open **CHARACTERS** tab.
2. **Origin → People:** choose **Umbrin** → lineage **Obsidian Highborn** (or any Umbrin lineage).
3. **Origin → Class:** choose **Oracle**.
4. Set level **3** (**Advancement** card, right column — not Abilities) so L3 Mystery tier I is visible.
5. **Paths** tab (center column):
   - Pick **Oracle Mystery** (e.g. Ancestor or any draft mystery — draft badge is OK).
   - Pick **Oracle's Curse** (e.g. Spiral-Touched).
   - With level **3**, confirm mystery panel shows **L1 revelation** block, **Patron** + **Prophecy trigger** lines, and **Tier I (L3)** — three revelations with charge costs (1 charge each).
   - Scroll **Class & arch paths** — confirm arch path list and hero path blocks render (no blank panel).
   - *(Optional)* Drop level to **1** — confirm **Tier I revelations unlock at level 3** hint appears and Tier I list hides.
6. **Weave** tab: confirm message that Oracles use **Revelation Charges**, not RP (no RP slider for Oracle).
7. Name the hero (e.g. `Smoke Oracle`) → click **SAVE**.

**Pass:** Save succeeds; character appears in “Load saved” chips; no red console errors.

### 2. Resonance / RC check in builder (1 min)

1. Switch to **Sheet** view (top-right toggle).
2. Confirm Oracle section shows Mystery + Curse names, not Weave spell list as primary pool.
3. Switch back to **Build**.

**Pass:** Sheet renders; Oracle terminology is RC / Revelations, not “spell slots” or RP for Oracle.

### 3. Session load + RC (3 min)

1. Open **SESSION** tab.
2. Under **Add saved character**, click your Oracle → they appear in **Combatants**.
3. Confirm **Pool** column shows **RC** (violet), not RP — e.g. L3 → **4 / 4** (L1=3, +1 every odd level, cap 7).
4. Confirm subclass badges: **Mystery:** and **Curse:** under the name.
5. Click **−** on RC once, then **Party Resonance → Short rest** → RC should regain +1 (toward max).
6. Click **Long rest (+8h)** → horn clock +8h; RC restores to full; combatants unchanged otherwise.

**Pass:** RC track works; rest buttons apply without error; horn hours increase on long rest.

---

## Path B — Umbrin Mage (~5 min)

### 4. Create Mage (2 min)

1. **CHARACTERS** → **NEW** (header button) if needed.
2. **People:** **Umbrin** (any lineage).
3. **Class:** **Mage** → optional **Arch path:** Arcanist (Origin → Class dropdown).
4. **Paths** tab: confirm L1–L3 features and **ClassPathDisplay** arch/hero blocks for Mage.
5. **Weave** tab: set **Resonance Points**; note computed **max RP** for Mage L1 (draft table OK).
6. Name (`Smoke Mage`) → **SAVE**.

**Pass:** RP slider + max RP line visible; Paths tab populated.

### 5. Session RP + rests (2 min)

1. **SESSION** → add saved Mage.
2. **Pool** column shows **RP** (purple), not RC.
3. Spend a few RP (manual field or per-row controls).
4. **Short rest** → partial RP recovery (¼ max, reputation may modify).
5. **Long rest (+8h)** → full RP restore.

**Pass:** Party Resonance card shows living caster RP sum; Mage RP restores on rests.

---

## Path C — Encounters & Generators handoff (~4 min)

### 6. Encounters → Session (2 min)

1. **ENCOUNTERS** → pick **T2** (or any tier).
2. Click **Load in Session** → app switches to **SESSION** automatically.
3. Confirm amber **Scene loaded from encounters** banner (`from encounters` — lowercase source id) with tier name + brief.
4. Confirm **Current Tier** matches selected tier.
5. Confirm **Scene notes** textarea filled with encounter brief.

**Pass:** Tier + scene notes applied; banner dismissible.

### 7. Generators → Session (1 min)

1. **GENERATORS** → tier **T3** → **Build pack for Tier 3** → **Load in Session**.
2. **SESSION** opens; amber banner shows **from generators**; scene brief replaces prior tier context (T3).

**Pass:** Second handoff overwrites scene context; no stale localStorage error. Repeat **Load in Session** while already on SESSION still applies (via `goToSession` / `handoffTick` — no double-consume after wave 15).

### 8. Dungeon Cycle tab (1 min)

1. **DUNGEON GUIDE** → **Mechanics** tab (Cycle / Shardspire content).
2. Confirm **The Cycle & Shardspire** card: rotation text, **Classes of Entry** list (17 classes, draft badge OK), **Victory Consequences by Tier** (10 rows).
3. Skim **Expedition** teams and **Gate Bosses** — no empty crash panels.

**Pass:** Mechanics tab renders full cycle block; draft badges visible where expected.

---

## Optional stretch (if time)

| Action | Expected |
|--------|----------|
| **Multiclass RP merge (draft)** | Builder → Mage L8 + secondary **Cleric L4** → Weave tab shows **Multiclass RP merge** panel with line breakdown + **Draft** badge; Sheet shows same block; Session tooltip on `/max` shows merge summary |
| **Overcast school affinity** | Session → add **Smoke Mage** (Lawful Good alignment in save) → Overcast panel → spell lookup **Shield** or pick **Abju** school → confirm **Affinity −1 RP** on base; T1 shows base **1 RP** (not 2); **Apply cast spend** deducts total |
| **Druid wild-shape + Primal Recovery** | Builder → Druid L13+ with circle → Session → pick form → **Spend use** → timer shows **10 min**; **−1 min** ticks down; **Long rest** restores uses; **Primal Recovery** spends 1 use for +RP (L13 draft); **Short rest** resets Primal Recovery |
| **Overcast Burnout hint (Mage L17 draft)** | Builder → **Smoke Mage** L17+ → Session → set **Ethos** pill (e.g. LG) → Overcast panel → tier **8+** → spend RP until post-cast pool **below 25% max** → **Apply cast spend** → **Overcast check** line shows concentration DC + Burnout text (or low-pool hint alone if tier &lt; 8) |
| **Ethos row (affinity smoke)** | Session ally row → compact **Ethos** pills (LG…CE) → pick school in Overcast panel → live **−1/+1 RP** affinity hint updates without Builder re-add |
| **Druid arch attunement (L15 draft)** | Builder → Druid L15+ → Session → wild-shape arch form → **Shift+click** to attune (max 2) → **Arch attuned X/2** badge; swap between attuned forms while transformed skips use once/encounter |
| **Shaman totem placement (L6 / L13 draft)** | Builder → Shaman L6 → Session → place one Spirit/Echo/Divining/Blight totem, then **Recall all**; at L13 place two distinct totems and confirm a third is disabled; **Long rest (+8h)** clears placements. Effects, duration, targeting, and Totem Pulse resolution stay GM-facing. |
| Add bestiary foe from Session search | Monster row with HP from stat block |
| **Next turn** with 2+ combatants | Round increments when initiative wraps |
| **Add Gate Boss** | Stub HP = 40 + tier×25 |
| Export JSON (Characters header) | **EXPORT** button downloads `.json` file |

---

## Fail criteria (stop and file a bug)

- Blank screen or uncaught exception in browser console during any step above.
- **SAVE** does not persist character across refresh.
- Oracle shows RP pool in Session (should be RC only).
- Mage shows RC in Session (should be RP).
- **Load in Session** does not land on SESSION tab or does not populate tier/scene notes.
- `npx tsc --noEmit` fails after your session.

---

## Known non-blockers (do not fail smoke)

- Draft badges on mysteries, oaths, L11–20 milestones, dungeon victory consequences.
- HP on saved PCs may use stub formula if not set manually in save.
- No automated spell casting or death saves in Session.
- Global header tab search is placeholder (not wired); `/` focuses the tab filter only (wave 14).
- Oracle **Weave** tab is guidance-only by design.

---

*Playtest smoke — verified post wave 15 handoff idempotency; Oracle Paths L1/Tier I tip added wave 45; multiclass RP stretch added wave 58; overcast affinity + wild-shape stretch added wave 60; Burnout hint + Ethos + arch attunement stretch added wave 63 — 2026-07-30*

---

## Wave 68 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Items zero-result recovery** | **ITEMS** → enter a nonsense search (for example, `zzzz-wave-68`) or combine filters until the catalog has no matches → confirm the empty-state explanation and **Clear all filters** appear → click it → the full catalog returns and the selected-item/crafting state is not erased. |
| **Spells zero-result recovery** | **SPELLS** → select **Learned** or **Favorites**, then use a nonsense search or filters that yield no cards → click **Clear all filters** → return to **All** with discovery fields cleared; learned and favorite selections remain stored. |
| **Bestiary zero-result recovery** | **BESTIARY** → enter `zzzz-wave-68` and/or narrow dropdowns until no creatures match → click **Clear all filters** → search and dropdown filters clear together and the creature catalog returns. |
| **Burnout recovery exits** | Session → trigger an **Overcast check** hint (Mage L17 draft, tier 8+, post-cast RP below 25% max) → verify it clears after **Short rest**, trigger it again and verify **Long rest (+8h)** clears it, then trigger it once more and use that row’s **Full** control. The RP threshold badge may remain or clear according to current RP; only the one-shot hint must disappear. |

---

## Wave 70 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Floor Encounters global zero-result recovery** | **ENCOUNTERS** → enter `zzzz-wave-70` in the Floor Encounters search → the match row reads **0 tiers match** and the dedicated **No encounter tiers match** card offers **Clear filters** → click either visible reset → the query clears, all ten tier buttons remain available, and the selected tier’s encounter card still renders. |
| **Floor Encounters within-tier zero-result recovery** | **ENCOUNTERS** → choose a mapped tier with both columns (for example **T1**), then search for a term from that tier’s Safe Haven that is not present in its POI (or the reverse) → the nonmatching column says **No matching** and exposes **Clear filters** → click it → both Safe Havens and Points of Interest repopulate for the same selected tier. |

For the T1 path, `Crystalfront` is a deterministic Safe Haven-only query: Safe Havens remain visible while Points of Interest shows **No matching points of interest** and its local reset.

---

## Wave 101 — Session rest feedback

| Action | Expected |
|--------|----------|
| **Advance +8h** | Session's horn-clock control advances only elapsed time; it is not labelled as a rest and does not restore combatant resources. |
| **Short rest** | The Party Resonance card reports the number of affected allies and confirms the existing RC/RP recovery plus Druid Primal Recovery/free-arch-swap resets. |
| **Long rest (+8h)** | The Party Resonance card reports affected allies and confirms the existing +8h horn advance, RC/RP restoration, Druid-use reset, and Shaman-totem clearing. |

---

## Wave 72 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Persisted Ashen Grove draft propagation** | **CHARACTERS** → create/load a Druid at a hero-form level → choose **Circle of the Ashen Grove (draft)** and confirm its selected-circle notice, hero-form heading, and **Charbear** / **Blazewood Stag** carry **Draft** → **SAVE**, refresh, then open **Sheet** and confirm the circle plus both hero-form names still show draft status → **SESSION** → add that saved Druid, select either hero form, and confirm the picker plus active-form line retain **Draft**. Switch to a non-Ashen circle (or inspect one if already saved) and confirm no Ashen/draft hero-form marker leaks into it. |

---

## Wave 74 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Dungeon Guide overview zero-result recovery** | **DUNGEON GUIDE** → remain on **Overview** → enter `zzzz-wave-74` in the tier search (or combine it with **Mapped tiers only**) → the tier-card grid is replaced by **No tier overviews match the current filters** with an in-place **Clear filters** button → click it → the search and mapped-only state clear, all ten tier cards return, and the previously selected tier remains selected. |

---

## Wave 75 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Dungeon Guide paired detail/overview recovery** | **DUNGEON GUIDE** → select a tier other than T1 → **Tier Details** → enable **Mapped tiers only** and enter `zzzz-wave-75` → verify **No tier details match the current filters** and click **Clear filters** → the tier navigator returns and the previously selected tier remains selected. Switch to **Overview**, repeat `zzzz-wave-75` with **Mapped tiers only**, then clear again → all ten cards return and the same selected tier remains selected. |
| **Dungeon Guide mechanics search recovery** | **DUNGEON GUIDE** → **Mechanics** → enter `zzzz-wave-75` → under **Victory Consequences by Tier**, verify **No victory consequences match the current search** and **Clear filters** → click it → the search clears and all ten consequence rows return. |

---

## Wave 77 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **World VIII + first prestige badge pass** | **COSMOLOGY** → select **World VIII** → confirm **Races of Aethel** has a visible **Draft** marker and its five source labels remain present. **CHARACTERS** → select each of **Bloodbound**, **Forge Master**, and **Hexblade** under prestige paths → confirm **Bloodletting Strikes**, **Ember Pulse**, and **Doom Sigil** each show a small **draft** badge in Builder. Switch to **Sheet** → confirm the same selected hallmark retains its badge. |
| **Sapper / Soulrender draft provenance** | **CHARACTERS** → select **Sapper** → confirm **Demolition Pack** and **Saboteur’s Toolkit** show **draft** badges; select **Soulrender** → confirm **Echo of Death** does too. In each case, switch to **Sheet** and confirm the corresponding badge remains visible. |

---

## Wave 79 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Wave 78 hallmark provenance** | **CHARACTERS** → select **Hexblade**, **Storm Lord**, **Verdant Animist**, and **Warlock** under prestige paths. Confirm **Blade Hunger**, **Eye of the Tempest**, **Living Terrain**, and **Pact Sigils**, respectively, show a small **draft** badge in Builder. Switch to **Sheet** after each selection and confirm the same selected hallmark keeps its badge. |
| **Short-capstone draft provenance** | **CHARACTERS** → select **Battlemage**, **Gravetouched**, **Hexblade**, and **Warlock**. Confirm each visible **Capstone:** line has a small **draft** badge in Builder. Switch to **Sheet** and confirm the capstone badge stays visible for the same saved or active selection. |

---

## Wave 80 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Second capstone-batch provenance** | **CHARACTERS** → select **Sapper**, **Forge Master**, **Bloodbound**, and **Echomancer** under prestige paths. Confirm each visible **Capstone:** line carries a small **draft** badge in Builder. Switch to **Sheet** after each selection and confirm the same capstone badge persists. |

This check covers presentation provenance only: no capstone is resolved, automated, or mechanically applied by the companion.

---

## Wave 88 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Fourth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Combat** and locate **Bull Rush**, **Cleaving Momentum**, **Close Quarters Combat**, **Combat Intuition**, and **Combat Slide**; filter **Magic** for **Channeled Flow**; filter **Skill** for **Climb Anywhere** and **Cold Reader**. Each card has a compact **Draft** badge and its draft presentation line, while its existing prerequisite and effect text remain unchanged. Taking any listed feat remains a character-sheet selection only; no listed effect is automated. |

This is a presentation-provenance smoke only. The eight records remain draft pending author rules review.

---

## Wave 87 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Third generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Combat** and locate **Battlefield Commander**, **Berserker Rage**, **Bleeding Edge**, **Brace for Impact**, and **Break Line**; filter **Skill** for **Battlefield Tactician** and **Beast Whisperer**; filter **Magic** for **Blood Magic**. Each card has a compact **Draft** badge and its draft presentation line, while its existing prerequisite and effect text remain unchanged. Taking any listed feat remains a character-sheet selection only; no listed effect is automated. |

This is a presentation-provenance smoke only. The eight records remain draft pending author rules review.

---

## Wave 86 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Second generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** and locate **Arcane Recall** and **Arcane Transfusion**; filter **Combat** for **Armor Crusher**; filter **General** for **Battle Awareness**. Each card has a compact **Draft** badge and its new draft presentation line, while its existing prerequisite and effect text remain unchanged. Taking any of these feats remains a character-sheet selection only; no listed effect is automated. |

This is a presentation-provenance smoke only. The four records remain draft pending author rules review.

---

## Wave 85 optional-stretch addendum
| Action | Expected |
|--------|----------|
| **Unmapped-depth draft extract visibility** | **DUNGEON GUIDE** → **Tier Details** → select **T6**, then repeat for **T7–T10**. Each selected tier shows a red-outline **Draft extract** badge beside its floor/difficulty/boss metadata and an amber warning panel beginning **Draft extract.** The panel repeats that the content is presentation-only and that routes, hazards, encounter resolution, and maps remain unconfirmed. Confirm the tier still shows its existing survivor-rumor haven and POI labels; do not treat them as mapped procedures. |
| **Feat draft provenance** | **CHARACTERS** → **Feats** → filter **Skill** and locate **Acrobatic Mastery**, then filter **Magic** and locate **Arcane Armor**, **Arcane Flexibility**, and **Arcane Pulse**. Each card shows a compact **Draft** badge and its enriched description while preserving the existing prerequisite and effect text. Selecting a feat remains a normal character-sheet selection only; no feat effect is automated. |

This is a presentation smoke only. T6–T10 stay unmapped, and the four feat entries remain draft pending author rules review.

---

## Wave 83 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Final capstone-batch provenance** | **CHARACTERS** → select **Beastmaster** and **Chronomancer** under prestige paths. Confirm each visible **Capstone:** line carries a small **draft** badge in Builder. Switch to **Sheet** after each selection and confirm the same capstone badge persists. |

This check covers presentation provenance only: no capstone is resolved, automated, or mechanically applied by the companion.

---

## Wave 82 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Fourth capstone-batch provenance** | **CHARACTERS** → select **Soulrender**, **Blademaster**, **Berserker**, and **Storm Lord** under prestige paths. Confirm each visible **Capstone:** line carries a small **draft** badge in Builder. Switch to **Sheet** after each selection and confirm the same capstone badge persists. |

This check covers presentation provenance only: no capstone is resolved, automated, or mechanically applied by the companion.

---

## Wave 81 optional-stretch addendum

| Action | Expected |
|--------|----------|
| **Third capstone-batch provenance** | **CHARACTERS** → select **Wyrmslayer**, **Verdant Animist**, **Mooncursed**, and **Giant Killer** under prestige paths. Confirm each visible **Capstone:** line carries a small **draft** badge in Builder. Switch to **Sheet** after each selection and confirm the same capstone badge persists. |

This check covers presentation provenance only: no capstone is resolved, automated, or mechanically applied by the companion.

---

## Wave 83 final append — capstone provenance

| Action | Expected |
|--------|----------|
| **Final capstone-batch provenance** | **CHARACTERS** → select **Beastmaster** and **Chronomancer** under prestige paths. Confirm each visible **Capstone:** line carries a small **draft** badge in Builder. Switch to **Sheet** after each selection and confirm the same capstone badge persists. |

This check covers presentation provenance only: no capstone is resolved, automated, or mechanically applied by the companion.

---

## Wave 88 final feat-provenance append

| Action | Expected |
|--------|----------|
| **Fourth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Combat** for **Bull Rush**, **Cleaving Momentum**, **Close Quarters Combat**, **Combat Intuition**, and **Combat Slide**; filter **Magic** for **Channeled Flow**; filter **Skill** for **Climb Anywhere** and **Cold Reader**. Every card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking one remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 99 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Fifteenth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **General** for **Tenacity** and **Tough as Nails**; filter **Skill** for **Tinker Adept**, **Trap Sense**, **Unshakeable**, and **Versatile Artisan**; filter **Magic** for **Twin Cast**; filter **Combat** for **Unstoppable Force**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 98 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Fourteenth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Skill** for **Steady Hands**; filter **Magic** for **Still Casting** and **Temporal Flux**; filter **General** for **Stubborn Resolve** and **Tactical Insight**; filter **Combat** for **Sure Shot**, **Tactical Flanker**, and **Target Mark**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 95 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Eleventh generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Combat** for **Precision Throw**, **Punishing Blow**, and **Reckless Swing**; filter **Magic** for **Protective Casting** and **Quick Ritualist**; filter **Skill** for **Quick Learner**; filter **General** for **Quick Recovery** and **Resilient Mind**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 93 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Ninth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Combat** for **Lunge**; filter **Magic** for **Magical Fortitude**, **Mana Burn**, **Mental Buffer**, **Mirror Cast**, and **Mystic Focus**; filter **General** for **Mental Fortress**; filter **Skill** for **Merchant’s Guile**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 92 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Eighth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Skill** for **Herbalist**, **Intuitive Reflex**, **Librarian's Eye**, and **Lock Savant**; filter **Magic** for **Illusionist’s Trick** and **Lingering Magic**; filter **General** for **Inspiring Presence** and **Jack of All Trades**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 91 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Seventh generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** for **Ether Anchor**, **Flash Cast**, and **Foresight Surge**; filter **Combat** for **Exploit Weakness**; filter **General** for **Field Medic** and **Fleet of Foot**; filter **Skill** for **Field Surgeon** and **Forensic Investigator**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 90 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Sixth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** for **Dispel Precision**, **Echo Spell**, **Efficient Caster**, **Empowered Summoning**, and **Energy Sink**; filter **Combat** for **Double Tap** and **Draw Cut**; filter **Skill** for **Dungeon Cartographer**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 89 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Fifth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** for **Concentrated Will** and **Counterspell Adept**; filter **Combat** for **Crippling Strike** and **Disarming Blow**; filter **Skill** for **Cultural Expert**, **Diligent Researcher**, and **Disguise Expert**; filter **General** for **Danger Sense**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 94 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Tenth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** for **Mystic Recoil**, **Overchannel**, and **Planar Knowledge**; filter **General** for **Natural Leader** and **Night Hunter**; filter **Combat** for **Overrun** and **Precise Shot**; filter **Skill** for **Polyglot**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 96 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Twelfth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** for **Ritual Channeler** and **Runic Shield**; filter **Skill** for **Rogue’s Escape** and **Runic Scholar**; filter **Combat** for **Savage Momentum**, **Shattering Smash**, **Shield Bash**, and **Shield Expert**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 97 feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Thirteenth generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **Magic** for **Silent Casting**, **Spell Deflection**, **Spell Reservoir**, and **Spellweave**; filter **Skill** for **Silent Movement**, **Silver Tongue**, and **Spell Scribe**; filter **General** for **Skill feats1. Master Tracker**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |

Presentation provenance only: all eight records remain draft pending author rules review.

---

## Wave 100 final feat draft provenance addendum

| Action | Expected |
|--------|----------|
| **Final generic-feat draft batch** | **CHARACTERS** → **Feats** → filter **General** for **Versatile Grip** and **Wilderness Walker**; filter **Combat** for **Volley**, **Weapon Finesse**, **Weapon Mastery**, **Whip Control**, and **Whirlwind Striker**; filter **Skill** for **Wilderness Chef**. Each card shows the compact **Draft** badge and its presentation line; its existing prerequisite and effect text remain unchanged. Taking a listed feat remains a character-sheet selection only; no listed effect is automated. |
| **Duplicate record author check** | Filter **Skill** for **Master Tracker**. Its existing `master_tracker` record now has the same bounded draft presentation and badge as the already-drafted `skill_feats1_master_tracker` record. Confirm their identical prerequisite/effect strings; do not choose an identity, type, or deduplication action in the companion. |

Presentation provenance only: the eight canonical records and the duplicate placeholder repair remain draft pending author rules review. The two Master Tracker records require an author decision; neither was deleted or mechanically changed.

---

## Wave 102 — encounter handoff and rest-feedback stretch

| Action | Expected |
|--------|----------|
| **Specific encounter site handoff** | **ENCOUNTERS** → choose a mapped tier with two or more Points of Interest → press **Use as site in Session** on a non-default site → SESSION opens with **Scene loaded** and Scene notes identify that exact site. The tier, gate boss, and listed fallback haven remain present. |
| **Specific fallback-haven handoff** | **ENCOUNTERS** → on the same tier, press **Use as fallback haven in Session** on a non-default haven → SESSION opens with Scene notes identifying that exact fallback haven. The selected/default site, tier, and gate boss remain present. |
| **Rest feedback persistence and distinction** | **SESSION** → add at least one ally → click **Advance +8h** and confirm no rest-outcome line appears → click **Short rest** and confirm its status line names the current ally count and short-rest tracks → click **Long rest (+8h)** and confirm its status line names the current ally count and the horn’s 8h advance. The Short-rest line must not claim a horn advance; the Long-rest line must. |

---

## Wave 103 — Generator pack handoff guardrails

| Action | Expected |
|--------|----------|
| **Pack-first Session handoff** | **GENERATORS** → choose **T3** → confirm **Load in Session** is disabled and the helper says to build a pack first → **Build pack for Tier 3** → confirm the displayed pack is for T3 and **Load in Session** enables → press it → SESSION opens with the existing `from generators` handoff banner and the displayed pack’s tier/brief. |
| **Tier-change freshness** | **GENERATORS** → build a pack for **T3** → select **T4** → the T3 output clears and **Load in Session** disables until a T4 pack is built, preventing the prior tier’s text from being staged with T4 metadata. |
| **Copy feedback** | Generate any spark → press **Copy last spark** → confirm **Last spark copied.** appears, or (where clipboard permission is unavailable) the visible recovery message explains that the text can be selected manually. |

---

## Wave 104 — Bestiary foe handoff

| Action | Expected |
|--------|----------|
| **Bestiary → Session foe** | **BESTIARY** → select any creature with a visible positive HP value → press **Add foe in Session** → SESSION opens and shows the red **Foe added from Bestiary** confirmation naming that creature and its HP. In **Combatants**, exactly one editable foe has been added with the source creature name, HP, and notes containing its CR and zone. Adjusted initiative, HP, and conditions remain table-facing. |

---

## Wave 105 — saved-character refresh discoverability

| Action | Expected |
|--------|----------|
| **Saved-character return path** | **CHARACTERS** → make or load a hero → **SAVE** → **SESSION** → confirm **Add saved character** explains that it reads browser saves and that adding copies the hero into the current encounter. The hero button identifies its class and level; add it and confirm one editable ally appears in Combatants. |
| **Refresh feedback** | While on **SESSION**, use **Refresh saved list** → confirm its accessible status line reports the refreshed saved-character count. With no `dd_characters` data, confirm the empty state directs the player to **CHARACTERS → SAVE**, then back to Session to refresh. |
| **Import boundary** | Confirm the empty state does not imply Session can import a JSON file: Session has no separate JSON-import action and only reads the existing browser saved-character list. |

---

## Wave 106 — spell cast-preview handoff

| Action | Expected |
|--------|----------|
| **Spell reference → Session** | **SPELLS** → find any non-Oracle-reference spell (for example, `Shield`) → press **Preview in Session** → SESSION opens with the indigo **Cast preview from Spells** banner naming the spell, school, tier, casting time, range, and duration. |
| **Manual resolution boundary** | Confirm the banner directs the player to choose a caster and use that row’s existing spell lookup / Overcast controls as appropriate. The handoff must not add a combatant, deduct RP, alter a saved character, or resolve a cast. |

---

## Wave 107 — item reference-preview handoff

| Action | Expected |
|--------|----------|
| **Item reference → Session** | **ITEMS** → select any dropped or crafted item → press **Preview in Session** → SESSION opens with the teal **Item preview from Items** banner naming the item, rarity, tier, category, source type, and existing description. |
| **GM-resolution boundary** | Confirm the preview does not write Scene notes, add inventory, add a combatant, change a saved character, or alter resources. The banner directs the GM to resolve acquisition, use, crafting, and any inventory change manually; relevant detail may be copied into Scene notes by hand. |

---

## Wave 108 — Session handoff suite consolidation

Run the existing handoff rows as one pass: saved character (Wave 105), spell preview (Wave 106), item preview (Wave 107), Bestiary foe (Wave 104), selected POI/haven (Wave 102), and Generator pack (Wave 103). For each arrival, confirm its named banner or copied combatant/scene context appears once, remains dismissible or editable where applicable, and preserves its documented boundary: no automated inventory, character-save mutation, RP spend, cast resolution, or encounter resolution.

When the Combatants list is filtered or automatically collapses foes, confirm the heading reports the visible subset (for example, **3 of 7 shown**) and that the existing filter controls or **Show foes** control restores the intended rows. This is display guidance only; it does not alter initiative, turn order, or combatant data.

---

## Wave 109 — reveal hidden active turn

| Action | Expected |
|--------|----------|
| **Filtered ally turn** | **SESSION** → add enough combatants to expose filters, choose **Foes**, then use **Next turn** until an ally is active. The existing notice names that hidden ally; **Show active turn** switches to **Allies** and reveals the highlighted active row. |
| **Collapsed foe turn** | **SESSION** → add at least four foes plus an ally so the default view collapses foes → advance until a foe is active. The notice names that foe; **Show active turn** selects **Foes**, expands the foe view, and reveals the highlighted active row. |

This is visibility recovery only: it does not change initiative values or order, advance/reset the turn or round, or alter combatant data.

---

## Wave 110 — Session arrival-notice and empty-table recovery

| Action | Expected |
|--------|----------|
| **Dismiss stacked arrival notices** | **SESSION** → stage two or more existing arrivals (for example, an encounter handoff and an Item or Spell preview) → confirm the compact **Dismiss all notices** control appears and states its boundary → click it → all arrival banners close while Scene notes, tier, horn time, combatants, turn/round, and resources remain unchanged. |
| **Empty combatant table orientation** | **SESSION** → with no combatants, confirm the empty state names the three existing entry routes: saved character, Bestiary, and Ally / Enemy controls. Confirm it explicitly states that current Scene notes, tier, horn time, and arrival notices are retained; add an Ally and verify those fields remain intact. |

Both are state-preserving display recovery only. The bulk action closes local arrival notices and does not consume or alter any staged or table-facing data.

---

## Wave 111 — printable draft-badge parity

| Action | Expected |
|--------|----------|
| **Prestige draft provenance in print** | **CHARACTERS** → select a prestige path with a drafted hallmark or capstone (for example, Bloodbound, Forge Master, or Hexblade) → switch to **Sheet** → confirm each applicable hallmark/capstone shows **Draft** onscreen → use **Print sheet** / print preview → confirm the same **Draft** labels remain visible in the printed sheet. |

This is print-presentation provenance only. It does not change prestige selection, prerequisites, capstones, or any feat/class behavior.

---

## Wave 112 — Session dismissal confirmation

| Action | Expected |
|--------|----------|
| **Confirm stacked-notice dismissal** | **SESSION** → stage two or more existing arrival notices → record current Scene notes, tier, horn time, combatants, turn/round, and resources → click **Dismiss all notices** → all arrival banners close and an accessible confirmation names the dismissed count and confirms every recorded table field is unchanged. |
| **New arrival clears stale confirmation** | After the confirmation appears, stage any existing Session handoff → confirm the new arrival banner appears and the prior dismissal confirmation is no longer shown. |

This is local-notice feedback only. It does not change handoff payload outcomes, Scene notes, combatants, initiative, tier, horn time, resources, or any manual-resolution boundary.

---

## Wave 113 — Session filtered-table recovery

| Action | Expected |
|--------|----------|
| **Empty Foes view** | **SESSION** → add one or more allies but no foes → select the existing **Foes** table filter → confirm **No combatants match this view** appears with **Show all combatants** → use it → all existing ally rows return. |
| **State-preserving recovery** | Record an ally's HP, initiative, resources, conditions, notes, plus the current turn/round → enter an empty side filter and recover with **Show all combatants** → confirm every recorded field is unchanged. |

This is view-state recovery only. It changes neither combatant data nor initiative, turn/round, scene context, handoff state, or manual-resolution boundaries.

---

## Wave 114 — Builder and printable-feat clarity

| Action | Expected |
|--------|----------|
| **Non-Weave secondary class** | **CHARACTERS** → choose a Weave caster such as Mage, then choose **Soldier**, **Warrior**, or **Oracle** as Secondary class → confirm the Class tab explicitly says the selection is recorded but does not add a second Weave pool. Change to another Weave caster → confirm the existing purple **Multiclass RP merge** draft panel returns with its line breakdown. |
| **Selected draft feat provenance** | **CHARACTERS** → **Feats** → take any feat with the existing **Draft** card badge → confirm it retains a compact **Draft** badge under **Chosen feats** → switch to **Sheet** → confirm the selected feat retains its **Draft** badge onscreen and in print preview. |

These are selection and presentation checks only. They do not validate feat effects, resolve multiclass progression, alter RP manually, or change character-save data.

---

## Wave 115 — Character Sheet printable multiclass and feature provenance

| Action | Expected |
|--------|----------|
| **Eligible RP merge in print** | **CHARACTERS** → create/load a Weave-caster pair that already exposes the draft **Multiclass RP merge** (for example, Mage L8 + Cleric L4) → switch to **Sheet** → use **Print sheet** / print preview → confirm the merge heading, **Draft** badge, and all existing calculation lines remain together and legible. |
| **Recorded non-Weave secondary in print** | **CHARACTERS** → choose Mage plus Soldier, Warrior, or Oracle as Secondary class → switch to **Sheet** → use print preview → confirm **Secondary class recorded** names the class/level and states that it adds no second Weave pool. |
| **Level-feature draft legend in print** | Load any class with visible draft milestones → **Sheet** → print preview → confirm the class-feature legend states the draft-milestone count, shows a legible **Draft** sample badge, and each draft feature retains its own legible badge. |

This is print-presentation provenance only. It does not change multiclass rules, class features, RP, character-save data, or any feature resolution.

---

## Wave 116 — prestige-path intent boundary

| Action | Expected |
|---|---|
| **Recorded prestige-path intent** | **CHARACTERS** → choose a base class with an available prestige path → **Class** tab → select an **Arch path** → confirm the compact notice says the choice records intended path only, directs the player to **Paths** for requirements and draft markers, and states that selection grants neither prerequisites nor features. Switch to **Paths** and confirm the existing selected-path requirements and any draft badges remain visible. |

This is selection clarity only. It does not validate requirements, grant prestige features, change class/save data, or automate progression.

---

## Wave 117 — prestige-path Sheet intent parity

| Action | Expected |
|---|---|
| **Recorded prestige-path intent on Sheet** | **CHARACTERS** → choose a base class with an available prestige path → **Class** tab → select an **Arch path** → switch to **Sheet** → confirm the selected prestige panel repeats: “Recorded path intent only — this selection does not grant prerequisites or features.” Confirm its existing requirements and any **Draft** badges still render; use **Print sheet** / print preview to confirm the intent note remains legible. |

This is saved-selection and presentation coverage only. It does not validate requirements, grant prestige features, change class/save data, or automate progression.

---

## Wave 118 — Ethos recorded-state clarity

| Action | Expected |
|---|---|
| **Blank ethos on Builder and Sheet** | **CHARACTERS** → leave **Ethos** unselected → confirm Builder says **No ethos recorded** and identifies its existing save/spell-cost-preview use → **SAVE** → switch to **Sheet** → confirm the identity badges show **Ethos not recorded**, including in print preview. |
| **Chosen ethos on Sheet** | Return to **Ethos** → select any existing ethos → confirm the Builder shows **Chosen** → **SAVE** → switch to **Sheet** → confirm the selected ethos replaces the blank-state badge. |

This is saved-state presentation only. It does not add ethos rules, alter spell costs, change character storage shape, or automate progression.

---

## Wave 119 — Sacred Oath recorded-state clarity

| Action | Expected |
|---|---|
| **Blank oath on Builder and Sheet** | **CHARACTERS** → choose **Paladin** at L1 and leave **Sacred Oath** unselected → **Paths** confirms **No Sacred Oath recorded** and that the choice is made at L3 → **SAVE** → switch to **Sheet** → confirm its Paladin callout repeats **No Sacred Oath recorded (chosen at L3)**, including in print preview. |
| **Required oath remains clear at L3** | Set the same Paladin to L3 without selecting an oath → confirm the Builder keeps the existing required marker and the blank-state explanation → **SAVE** → Sheet/print says **No Sacred Oath recorded (required at L3)** and directs the player to Character Builder. |

This is saved-state presentation only. It does not add oaths, alter oath rules, change character storage shape, grant class features, or automate progression.

---

## Wave 120 — Oracle Mystery and Curse recorded-state clarity

| Action | Expected |
|---|---|
| **Blank Mystery and Curse on Builder and Sheet** | **CHARACTERS** → choose **Oracle** at L1 and leave both **Oracle Mystery** and **Oracle's Curse** unselected → **Paths** confirms **No Oracle Mystery recorded** and **No Oracle's Curse recorded**, including that each choice is made at L1 → **SAVE** → switch to **Sheet** → confirm both Oracle callouts repeat the recorded-state language, retain their existing **Draft** badges, and remain visible in print preview. |
| **One recorded selection leaves the other clear** | Return to **Paths** → choose any existing Mystery but leave Curse blank → confirm the Mystery's existing draft status and detail remain unchanged while the Curse blank-state explanation remains → **SAVE** → Sheet/print shows the Mystery plus only **No Oracle's Curse recorded (required at L1)**. Repeat with a Curse selected and Mystery blank if time permits. |

This is saved-state presentation only. It does not add Mystery or Curse content, alter Oracle rules, change character storage shape, grant revelations or boons, or automate progression.

---

## Wave 121 — People traits and feat-filter recovery

| Action | Expected |
|---|---|
| **Empty feat filter** | **CHARACTERS** → **Feats** → enter a search term with no existing feat match, optionally with a type selected → confirm the panel says no feats match the current filter and directs the player to change the type or search. Confirm no feat is selected or changed. |
| **Saved people traits on Sheet** | **CHARACTERS** → **People** → choose any existing people and optional lineage → **SAVE** → switch to **Sheet** → confirm **People & traits** repeats the saved people, lineage when present, and existing sourced trait names, including in print preview. |
| **Blank people state on Sheet** | Start a new character without choosing a people → **SAVE** → **Sheet** → confirm **People & traits** says no people is recorded and directs the player to Character Builder. |

This is existing-state presentation only. It does not add people or feat source data, change selection/storage semantics, validate feat prerequisites, grant trait or feat effects, or automate inventory, RP, casts, or progression.

---

## Wave 122 — draft extract and Wave 121 recovery

| Action | Expected |
|---|---|
| **Cosmology draft-extract context** | **COSMOLOGY** → open **World of Aethel** and then **First Song**. When either existing collection contains draft sections, confirm the picker has a visible **Draft extract** notice and marks each draft section with **†** before it is selected. Select one marked section in each tab and confirm its existing per-section draft note remains visible; no new lore or rules appear. |
| **Feat no-match recovery** | **CHARACTERS** → **Feats** → enter a term with no existing feat match, optionally with a type selected. Confirm the panel identifies the empty filter and directs the player to change type or search; no feat selection changes. |
| **Saved and blank People traits on Sheet** | **CHARACTERS** → **People** → save once with an existing people and optional lineage, then inspect **Sheet** and print preview for the saved people, lineage, and existing trait names. Start a fresh character without a people, save, and confirm **People & traits** instead says no people is recorded and directs the player to Character Builder. |

This is presentation and recovery coverage only. It does not add lore, people, trait, feat, class, or dungeon data; alter save semantics; map T6–T10; or automate inventory, RP, casts, progression, or encounter resolution.

---

## Wave 123 — path-reference clarity + Cosmology draft notice

| Action | Expected |
|---|---|
| **Hero-path reference gap** | **CHARACTERS** → choose a class whose existing path data has no hero-path entries → **Paths** confirms **No hero-path entries are recorded in the current reference for this class** instead of leaving a blank hero-path area. If arch paths exist, their existing cards remain visible. **SAVE** → **Sheet** and print preview repeat the same reference-boundary note. |
| **Cosmology draft notice** | **COSMOLOGY** → open **World of Aethel**, then **First Song** → before selecting a section, confirm each picker that has draft sections shows **Draft extract** and marks those existing options with **†**. Select a marked option and confirm its existing per-section draft note remains visible. |

This is presentation-only coverage. It does not create hero paths, alter class/progression/save rules, add lore or dungeon material, map T6–T10, or automate inventory, RP, casts, or encounters.

---

## Worker 1 — XP advancement gap-fill (2026-07-30)

| Action | Expected |
|--------|----------|
| **Confirmed Builder thresholds** | **CHARACTERS** → **Advancement** card → level **+1** at L2 shows **300 XP** (not legacy 500); scroll table lists rulebook values (L5 = 6,500; L20 = 355,000). |
| **Draft Session XP on defeat** | **SESSION** → add a Bestiary foe → set HP to **0** → **Award draft XP** → Scene notes gain a `[Draft XP]` line; each living ally shows **Draft session XP** tally. Saved character XP in Builder is unchanged. |
| **Double-award guard** | After awarding, foe shows **Draft XP logged**; repeat click does not duplicate the Scene note line. |

Draft CR→XP and split follow `XP_ADVANCEMENT_CANON.md` provisional section only. No Encounters calculator, no character-save write-back.
