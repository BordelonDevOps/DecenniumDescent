# GPT maximum-HP first review — partial capture

The completed reply exceeded the connector's20,000-character limit. All58 classification rows are captured; the adversarial-example tail and any final dependencies require separate recovery.

This packet is sufficient to define a bounded maximum-HP/threshold composition model. The main correction to the earlier 131-source discussion is that **Monk maximum-HP trauma should use one global strongest reduction, not one strongest per Monk owner**; the first sentence of `monk.engine[9]` is categorical enough to control that ambiguity.

## Bounded maximum-HP procedure

### 1. Effective maximum equation

Use a source ledger and recompute from source state; never incrementally multiply the already-modified result.

Define:

`preSystemicMax = max(1, baseMaximum + permanentBonuses + activeTemporaryBonuses - activeFlatReductions)`

Then:

`effectiveMaximum = max(1, floor(preSystemicMax × product(all compatible systemic factors)))`

All rational systemic factors multiply the same `preSystemicMax`, and floor **once** at the end.

This follows the already-closed rule that Expedition/Exhaustion multiply the “otherwise applicable maximum.” Flat additions/reductions are therefore part of that otherwise-applicable maximum, not applied afterward.

Example:

- base = 101
- Flesh Warden = +20
- Monk trauma = −9
- Exhaustion = ×1/2
- Expedition = ×3/4

`101 + 20 - 9 = 112`

`112 × 1/2 × 3/4 = 42`

So effective max = **42**.

Applying −9 after the multipliers would yield 36 and is rejected.

### Modifier ledger

Every modifier retains:

- source/application ID
- source owner
- target
- modifier type
- numeric amount/formula
- active/suppressed state
- start/end clock
- stacking/arbitration group
- provenance needed for dynamic level scaling

Recompute from those records whenever one changes. Never mutate a previously computed maximum and then multiply it again.

---

## 2. Flat stacking

### Feats

**NEW integration decision:** distinct feat IDs that grant maximum HP are compatible additive bonuses unless a feat/source explicitly says otherwise.

Thus Tenacity + Tough + Tough as Nails + Dark Fortitude can all contribute.

Same feat/name does not stack with itself.

The shared “strongest same-stat flat class-technique bonus” rule does **not** collapse distinct permanent feats.

### Class bonuses

Use source-specific compatibility rather than a new blanket rule.

Notably:

- Wizard Conjuration and Flesh Ascendant are compatible additive modifiers when the same undead summon qualifies for both.
- `wizard.engine[24]` and `wizard.hero.necromancer.flesh-ascendant` describe the **same Flesh Ascendant modifier identity** and must not double-count each other.

---

# 3. Monk maximum-HP trauma

`monk.engine[9]` says both:

- Monk reductions “do not stack on the same creature”; and
- use the largest reduction from “your Monk features.”

The former is broader. I would supersede the earlier provisional per-owner interpretation with:

> **One global strongest active Monk maximum-HP reduction per target, regardless of how many Monk owners applied it.**

This is the most source-faithful reading and prevents multiple Monks bypassing the explicit nonstacking sentence.

Keep every application as a separate record, however.

So:

- different source IDs remain separate records;
- different Monk owners remain separate records;
- repeated same-card applications remain separate records;
- numerical arbitration chooses the largest currently operative amount;
- if the largest becomes suppressed, the next strongest operative record immediately becomes effective;
- suppression does not stop its clock.

Do **not** merge repeated applications into one “longest duration” record. Separate clocks matter for suppression/removal/provenance.

### Rest

For a Monk trauma using the default engine duration:

> any **completed** short or long rest by the target ends all such default Monk max-HP-trauma records on that target.

This is an effect-ending condition, not an ordinary rest-reward allowance, so rest-recovery caps do not preserve one of them.

Interrupted rest: none end.

A card with an explicit earlier/different endpoint uses that endpoint.

Deathless Silence's defensive-passive suppression ending at source-next-start is a different component; it does not shorten the max-HP reduction, which remains until rest.

---

# 4. Current HP and temporary HP

Whenever effective maximum changes:

`currentHP = min(currentHP, effectiveMaximumHP)`

That clamp:

- is not damage;
- is not HP payment;
- causes no Wound save;
- causes no death-save failure;
- generates no damage/healing/resource trigger;
- cannot be redirected;
- is unaffected by Decay.

Restoring/increasing maximum HP raises **capacity only**. It restores no current HP.

Decay therefore does **not** prevent maximum-HP restoration.

Temporary HP remains independent and is **not clamped** merely because normal maximum HP decreases.

Dead, Stable and 0-HP creatures retain their life state and death counters unchanged when maximum HP changes. Minimum maximum HP 1 never resurrects anything.

Critical's healing ceiling recomputes afterward from:

`max(1, effectiveMaximum - 1)`

but Critical is not itself a maximum-HP modifier.

---

# 5. Summons and controlled undead

### Wizard Conjuration

`wizard.engine[10]`:

`+ Wizard level maximum HP`

belongs to the **summoning Wizard/source provenance**.

It is not transferred merely because control changes.

### Flesh Ascendant

`+2 × controlling Wizard level`

belongs to the Wizard currently supplying Flesh Ascendant to an undead creature they control.

If control is gained later:

- maximum capacity rises;
- current HP does not.

If that eligibility ends:

- remove the bonus;
- clamp current HP if necessary;
- no damage/healing event occurs.

### Both at creation

If a Wizard spell creates an undead creature and that creature also qualifies for Flesh Ascendant:

`listed base + Conjuration L + Flesh Ascendant 2L`

They are compatible additive bonuses.

A newly created creature begins at its **final creation maximum/current HP** unless the summoning source explicitly says it enters damaged.

That is creation-state construction, not healing.

Changing controller later never restores missing HP.

No new companion cap or command allowance is implied.

---

# 6. Feat-specific maximum HP

### `feat:tenacity`

Dynamic:

`+1 × current character level`

including prior levels and future levels.

### `feat:tough`

Use the exact wording literally:

> bonus equals twice your level **when you gain the feat**.

Record an acquisition snapshot:

`bonus = 2 × characterLevelAtAcquisition`

It does **not** automatically grow on later levels.

Do not import behavior from another game's Tough feat.

### `feat:tough_as_nails`

Dynamic by explicit wording:

- on acquisition: +2 per already-gained character level;
- every later level: +2 more.

Equivalent at ordinary progression to `2 × current character level` while the feat remains owned, but retain acquisition/progression history rather than rewriting its text.

### `feat:dark_fortitude`

Dynamic:

`+2 × current character level`

### `feat:familiar_bond`

The phrase “gains hit points equal to your level” is ambiguous between current HP and maximum HP.

**NEW provisional interface:** treat it as a familiar maximum-HP bonus:

`+ character level maximum HP`

When the familiar is initially created under the feat, its starting HP includes that bonus as part of creation-state construction.

Later level increases raise capacity only and do not heal missing HP.

This remains dependent on the eventual familiar/companion lifecycle package.

---

# 7. Threshold comparisons

Never derive thresholds from rounded fractions.

Use integer cross-multiplication:

- at or below quarter: `4 × HP <= maxHP`
- below quarter: `4 × HP < maxHP`
- at or below half: `2 × HP <= maxHP`
- below half: `2 × HP < maxHP`
- above half: `2 × HP > maxHP`

Use current **effective maximum HP** unless a source references a historical snapshot.

### Continuous state predicates

These recompute whenever HP or maximum HP changes:

- Wyrmhide while above half;
- Brutality Sense;
- Pain Empowerment;
- Dark Fortitude poison resistance;
- Life Drinker bonus;
- regenerative “below maximum” eligibility.

### Event-crossing triggers

These require a genuine HP transition, not merely a changed denominator:

- Anointed Guardian: first **fall** to ≤ quarter;
- Burning Blood IV: first **fall below** half;
- Death's Threshold activation: first **fall** to ≤ quarter;
- Adrenal Floodgate: first **fall** to ≤ quarter.

Changing maximum HP alone does not fire them.

### “Until healed above half”

Death's Threshold ends only when an actual HP-restoration event leaves the Oracle above half.

A maximum-HP decrease that makes unchanged current HP mathematically exceed half does **not** satisfy “healed above half.”

### Mythic Carapace / Butcherform

Their duration is best read as a **continuous duration gate**, not a once-only crossing trigger:

> while active, if `4×HP < effectiveMaximum`, the mutation ends.

**NEW integration choice.**

Thus a maximum-HP increase can make the character newly below quarter and end the form, even without damage. This avoids allowing activation/continuation while already below the expressly stated duration boundary.

Exact quarter remains legal because the text says **below** one-quarter.

---

# 8. Percentage amounts

Unless the source records an earlier snapshot, percentage healing/loss/damage uses effective maximum at the moment that amount resolves.

Examples:

- Wound Eater III:
  `floor(self effectiveMax / 4)`
  and **no minimum 1**.
- Wound Eater V target loss:
  `min(floor(target effectiveMax / 4), Oracle level + M)`.
- its self-heal cap:
  `floor(self effectiveMax / 2)`.
- Spiral III / False Life V:
  `max(1, floor(effectiveMax / 4))` because source expressly grants min1.
- Unyielding Light:
  `max(1, floor(effectiveMax / 3))`.
- Divine Rebirth:
  reviewed resurrection bridge remains `max(1, floor(effectiveMax / 2))`; the min1 comes from the already-reviewed viable-return bridge, not newly from this source.
- Ledger Unbound damage cap:
  `floor(target effectiveMax / 4)` before its save halving.
- Repair Pulse / Snap Rebuild:
  `floor(device effectiveMax / 2)` under their device rules.

---

# 9. Historical threshold snapshots

### Rewind Wound

Store with the referenced damage event:

- pre-event HP;
- post-event HP;
- effective maximum HP at that event.

Its “had reduced it below half maximum HP” test uses that **recorded maximum**, not the target's later changed maximum.

No retroactive qualification.

### Flesh to Ash

Explicitly determine half threshold **before rolling its damage**.

### Death Touch

Uses target state when the strike began.

### Blessing of the Meek

Uses target state before the healing.

### Mass Healing Light

Uses threshold when each target is chosen.

### Final Verdict

Target must satisfy ≤half when the feature is activated/targeted.

### Fearbrand / Malicious Execution

Use pre-damage/pre-rider target state.

### Echo Strike

Its RC rider checks the state **after that copied damage resolves** using the target's then-current effective maximum.

Brutality Progress keeps its already-reviewed snapshot/progress rules; do not reopen them in this package.

---

# 10. Damage attack + maximum-HP reduction ordering

For Monk attack features that both deal ordinary attack damage and impose max-HP trauma:

1. Snapshot pre-event effective maximum.
2. Resolve attack roll.
3. Resolve ordinary attack damage.
4. Resolve temp HP/normal HP/Wounds/Instant Death/death replacement using that **pre-trauma effective maximum**.
5. Freeze damage metrics.
6. If the target remains a legal target for the rider, resolve the printed CON save.
7. On failure add the max-HP reduction record.
8. Recompute effective maximum from the ledger.
9. Clamp current HP if above the new maximum.
10. That clamp creates no damage/Wound/threshold-crossing trigger.

The later reduction cannot retroactively change:

- Instant Death threshold;
- Wound DC/trigger;
- `actualHpDamage`;
- `actualDamageDealt`;
- concentration packet.

Example: max30, HP30, attack deals4; HP→26 under max30. Bone-Breaking then reduces max by15 → effective max15 and current HP clamps26→15. The extra 11-point clamp is **not damage**.

If ordinary attack damage already kills the target and no survival replacement preserves it, do not invent a meaningful temporary combat-trauma application to the corpse.

A same-event maximum-HP increase likewise never rewrites already-frozen damage metrics.

---

# All 58 classifications

| Exact source ID | Role | Disposition |
|---|---|---|
| `cleric.engine[7]` | GUARD | Healing/max-HP ceiling guard; no modifier. |
| `cleric.arch.anointed-guardian` | THRESHOLD_CROSSING | First genuine fall to ≤quarter; max-only change does not trigger. |
| `cleric.hero.saint.aura-of-grace` | THRESHOLD_HEAL_ELIGIBILITY | Below-half checked at pulse target selection. |
| `cleric.hero.saint.divine-rebirth` | PERCENT_RESURRECTION_HP | Half effective max at return; reviewed viable-return min1 applies. |
| `cleric.hero.saint.merciful-sacrament` | THRESHOLD_COST_GATE | Initial-zone ally ≤quarter snapshot when Sacrament starts. |
| `cleric.hero.saint.unyielding-light` | PERCENT_ZERO_HP_RECOVERY | `max(1,floor(max/3))`. |
| `cleric.hero.saint.mass-healing-light` | THRESHOLD_HEAL_BONUS | Below-half snapshot when target chosen. |
| `cleric.hero.cultist.corrupt-divinity` | THRESHOLD_CONTROL | NPC ≤quarter checked at initial resolution. |
| `dragoon.hero.dragon-guardian.wyrmhide` | CONTINUOUS_THRESHOLD | Above-half predicate recomputes with effective max. |
| `mage.hero.lich.flesh-to-ash` | THRESHOLD_DAMAGE | Explicit pre-damage half snapshot. |
| `mage.hero.lich.soulbound-ritual` | PERCENT_COMPANION_RECONSTRUCTION | Returns companion at half effective max; wider companion lifecycle open. |
| `monk.engine[9]` | MAX_HP_REDUCTION_ENGINE | Global strongest operative Monk trauma; separate records/clocks. |
| `monk.engine[16]` | GUARD | Healing/death guard only. |
| `monk.hero.iron-fist-master.ribcrusher-strike` | MAX_HP_REDUCTION | −(S+M), after attack damage, until completed rest. |
| `monk.hero.iron-fist-master.bone-breaking-strike` | MAX_HP_REDUCTION | −(2S+M), after attack damage. |
| `monk.hero.way-of-shadow.deathless-silence` | MAX_HP_REDUCTION + OTHER | −(4S+M); defensive-passive suppression has separate shorter clock. |
| `monk.hero.way-of-shadow.death-touch` | THRESHOLD_DAMAGE | ≤quarter snapshot at strike start. |
| `oracle.engine[13]` | GUARD | Healing/max ceiling only. |
| `oracle.supplement.spiral-touched.spiral-touched-boon-iii` | PERCENT_DIRECT_RECOVERY | Quarter effective max, source min1. |
| `oracle.supplement.wound-eater.wound-eater-boon-iii` | PERCENT_HEAL | `floor(selfMax/4)`; no min1. |
| `oracle.supplement.wound-eater.wound-eater-boon-v` | PERCENT_HP_LOSS + HEAL_CAP | Target quarter-max loss; self half-max recovery cap. |
| `oracle.supplement.burning-blood.burning-blood-boon-iv` | THRESHOLD_CROSSING | Genuine first fall strictly below half. |
| `oracle.supplement.false-life.false-life-boon-v` | PERCENT_DELAYED_RECOVERY | Quarter effective max at due start, min1. |
| `oracle.supplement.bones.death-s-threshold` | THRESHOLD_CROSSING + HEALED_EXIT | Trigger by genuine fall ≤quarter; exit requires actual heal to >half. |
| `oracle.supplement.bones.ledger-unbound` | PERCENT_DAMAGE_CAP | Damage ≤floor(targetMax/4), then save; cannot reduce below1. |
| `oracle.supplement.flame.crown-restored` | GUARD | Healing capped by ordinary maximum; no max modifier. |
| `oracle.supplement.life.verdant-pulse` | THRESHOLD_HEAL_RIDER + FLOOR | “was below half” uses pre-heal state; emergency floor separate. |
| `oracle.supplement.time.echo-strike` | POST_DAMAGE_THRESHOLD | RC check after echo damage using then-effective max. |
| `oracle.supplement.time.rewind-wound` | HISTORICAL_THRESHOLD | Uses maximum snapshot stored with referenced damage event. |
| `paladin.supplement.oath-of-mercy.merciful-smite` | DAMAGE_DERIVED_HEAL | No max modifier; healing maximum guard only. |
| `paladin.supplement.oath-of-mercy.blessing-of-the-meek` | THRESHOLD_HEAL_RIDER | Below-half checked before healing. |
| `paladin.supplement.oath-of-mercy.channel-life` | GUARD / DIRECT_HP_LOSS | No max modifier; donor/current-max legality only. |
| `paladin.supplement.oath-of-vengeance.final-verdict` | THRESHOLD_TARGET_GATE | Must be ≤half at activation. |
| `paladin.supplement.oathbreaker-oath-of-vengeance.death-touch-malicious-execution` | THRESHOLD_DAMAGE | “already” ≤half before rider damage. |
| `paladin.supplement.oathbreaker-oath-of-vengeance.fearbrand` | THRESHOLD_DAMAGE | Below-half bonus assessed before its damage. |
| `paladin.supplement.oath-of-the-martyr-king.crown-undying` | GUARD | Heal cannot exceed max; no max modifier. |
| `shaman.hero.bloodcaller.talon-strike` | EXCLUSION | Explicitly no permanent/max-HP reduction. |
| `tinker.hero.artificer.repair-pulse` | PERCENT_DEVICE_REPAIR | Functional device restores floor(max/2). |
| `tinker.hero.techsmith.snap-rebuild` | PERCENT_DEVICE_RECONSTRUCTION | Destroyed device restored to floor(max/2); device lifecycle handles viability. |
| `warrior.engine[8]` | PERCENT_THRESHOLD_RESOURCE_ENGINE | Brutality contribution/thresholds use reviewed max-HP snapshots; unchanged. |
| `warrior.engine[15]` | GUARD | Warrior healing maximum/death guard. |
| `warrior.base.brutality-sense` | CONTINUOUS_THRESHOLD | Visible hostile ≤quarter recalculates continuously. |
| `warrior.hero.ironskin.regenerative-mutation` | CONTINUOUS_BELOW_MAX_HEAL | Eligible while current HP < effective max. |
| `warrior.hero.dreadspawn.pain-empowerment` | CONTINUOUS_PERCENT_MISSING | Exact full 10% bands from current effective max. |
| `warrior.supplement.flesh-warden` | MAX_HP_BONUS | +2×Warrior level while equipped; capacity only. |
| `warrior.supplement.adrenal-floodgate` | THRESHOLD_CROSSING | First genuine fall to ≤quarter. |
| `warrior.supplement.mythic-carapace` | CONTINUOUS_DURATION_THRESHOLD | NEW: ends whenever state is strictly below quarter; >20 actual-damage rider separate. |
| `warrior.supplement.butcherform-chassis` | CONTINUOUS_DURATION_THRESHOLD | NEW: ends whenever state is strictly below quarter. |
| `wizard.engine[10]` | MAX_HP_BONUS + EXCLUSIONS | Conjuration +L to Wizard-summoned creatures; other school clauses separate. |
| `wizard.engine[24]` | MAX_HP_BONUS_ENGINE | Flesh Ascendant +2L after listed base; same modifier identity as card. |
| `wizard.hero.necromancer.flesh-ascendant` | MAX_HP_BONUS | Same Flesh Ascendant bonus as engine[24], not cumulative with it. |
| `feat:exploit_weakness` | THRESHOLD_ATTACK | 19–20 crit range only while target strictly below half. |
| `feat:familiar_bond` | MAX_HP_BONUS_PROVISIONAL | NEW: familiar +owner level max HP; creation starts with boosted max/current, later growth capacity only. |
| `feat:tenacity` | MAX_HP_BONUS_DYNAMIC | +1 per current character level. |
| `feat:tough` | MAX_HP_BONUS_SNAPSHOT | +2×level at feat acquisition; no inferred future growth. |
| `feat:tough_as_nails` | MAX_HP_BONUS_DYNAMIC | +2 per current level with explicit later-level growth. |
| `feat:dark_fortitude` | MAX_HP_BONUS_DYNAMIC + CONTINUOUS_THRESHOLD | +2/current level; poison resistance while strictly below half. |
| `feat:life_drinker` | HEALING + CONTINUOUS_THRESHOLD | Crit/kill healing plus +1d4 necrotic while strictly below half. |

---

# Adversarial examples to require in implementation

1. `base101 + FleshWarden20 − Monk9`, Exhaustion4, Expedition4 → **42**, floor once.
2. Suppress Monk−9 → `(101+20)×3/8 = 45`.
3. Two Monks apply −5 and −9 → effective Monk reduction **−9**, not −14; suppress −9 → −5 immediately.
4. Target completes short rest → all default Monk trauma records end; current HP unchanged while maximum rises.
5. max30/HP26 after damage; Monk−15 → max15, HP clamps15; clamp produces no damage/Wound/resource trigger.
6. Conjured undead base20, Wizard L10, Flesh Ascendant same controller → max `20+10+20=50`; initial creation HP50. Later controller loses Flesh Asc

[CAPTURE TRUNCATED]
