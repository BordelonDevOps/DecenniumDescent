## Missing adversarial examples 6–15

6. Conjured undead base20, Wizard L10, Flesh Ascendant same controller → `20 + 10 + 20 = 50` maximum HP; if created under both effects, it begins at 50/50. Later loss of Flesh Ascendant lowers capacity to30 and clamps current HP if needed, without damage.

7. Tough acquired at level5 → +10 permanently under its acquisition snapshot. At level10 it is still +10. Tenacity at level10 → +10. Tough as Nails at level10 → +20. Distinct feat benefits stack under the proposed feat rule.

8. Max changes 40→60 while HP12: Adrenal Floodgate does **not** trigger merely because the new ratio is ≤quarter.

9. Death's Threshold active at HP11/max40; max falls to20, so HP is now above half. It remains active because the card says **healed above half**, and no healing occurred.

10. Mythic Carapace at HP10/max40 is exactly quarter and remains active. If maximum rises to41 with HP still10, it becomes strictly below quarter and ends under the proposed continuous-duration interpretation.

11. Wound Eater III at effective max3 heals `floor(3/4)=0`; no invented minimum1.

12. Rewind Wound records a damage event HP30→14/max40. That event qualified as reducing below half. A later max change to20 does not retroactively alter the recorded qualification.

13. Ribcrusher/Bone-Breaking attack damage resolves against the pre-trauma maximum for Instant Death/Wounds/damage metrics. The later maximum reduction and clamp cannot rewrite them.

14. Dead, Stable0 or dying0 creature has maximum HP increased/reduced: life state, Stable state and death counters are unchanged.

15. Temp HP25 with effective normal maximum later reduced to10 remains temp HP25 unless another source expressly changes temp HP.

## Remaining evidence dependencies

Before any whole-game maximum-HP closure, still needed:

- item, unfinished spell, monster, disease/curse and Director-rule maximum-HP modifiers;
- general feat duplication/retraining/respec rules;
- familiar/companion creation and ownership lifecycle;
- broader summon/control provenance rules;
- unusual device maximum-HP/reconstruction rules;
- any non-Monk flat maximum-HP reductions;
- any exact source stating its max-HP modifier applies after systemic multipliers.

**Current disposition remains: SOURCE-AUDITED / DRAFTABLE**, not REVIEWED/reference-VALIDATED until the exact modifier ledger/composition/threshold implementation is returned.

---

# 1. Deathless Silence clocks

Confirm the correction. It has **three independent components**:

1. **Monk self-protection:**  
   cannot be targeted by opportunity attacks or Reactions until **source-next-regular-start**.

2. **Target defensive-passive suppression:**  
   on failed CON save, suppress one eligible non-core defensive passive until **that target's next-turn end**.

3. **Maximum-HP trauma:**  
   `−(4S+M)` under the Monk max-HP rule until the **target completes a short or long rest**, unless another exact source gives that max-HP component an earlier endpoint.

The target-end passive suppression does not shorten the trauma record. The source-start self-protection does not control either target-side record.

Preserve the already-reviewed 219-source control binding for the passive-suppression clock. My earlier source-next-start phrasing for that component was incorrect.

---

# 2. Wizard Conjuration + Flesh Ascendant

Confirm compatible addition, but label it exactly as:

> **NEW source-specific stacking exception** to the frozen same-stat strongest-flat class-technique default.

The supplied Wizard text does not expressly say these two separate bonuses stack. We are choosing compatibility because they arise from distinct interfaces:

- Conjuration modifies creatures **summoned by your Wizard spells**.
- Flesh Ascendant modifies **undead creatures you control**.

### Modifier identities

`wizard.engine[24]` and `wizard.hero.necromancer.flesh-ascendant` are one Flesh Ascendant modifier identity and never double-count.

### Conjuration

Use:

`+ WizardLevelAtSummonCreation`

Snapshot the summoning caster's Wizard level when the creature is created.

It does **not** dynamically increase if that caster later levels while an unusually long-lasting summon still exists.

Its provenance remains the creating Wizard/spell. Changing controller does not transfer or recompute the Conjuration modifier.

### Flesh Ascendant

Use:

`+ 2 × current Wizard level of the controller currently supplying Flesh Ascendant`

This is dynamic while eligibility exists.

If control changes:

- old controller's Flesh Ascendant eligibility ends;
- a new controller supplies a Flesh Ascendant bonus only if that controller actually has the feature;
- recompute using that eligible controller's current Wizard level;
- current HP only clamps downward if necessary; gaining the new capacity does not heal.

No controller change transfers the original Conjuration provenance.

### Familiar Bond

Retain the provisional rule:

`+ current eligible owner's character level` maximum HP.

Dynamic as that owner levels. Familiar identity/ownership transfer and creation/replacement remain for the companion package.

---

# 3. Monk global strongest trauma

Confirmed as an explicit supersession of the earlier per-owner proposal.

For every Monk maximum-HP trauma application, preserve independently:

- application ID;
- source ID;
- Monk owner;
- magnitude;
- clock/endpoint;
- suppression state;
- `defaultRestEnding` flag.

Numerically:

> use the **single largest operative Monk max-HP reduction on that target across all Monk owners**.

Do not merge “largest magnitude” with “longest duration.”

Example:

- Monk A: −9, expires after target rest;
- Monk B: −5, expires earlier.

While both operative → −9.  
Suppress −9 → −5 becomes effective.  
When −5 expires while −9 remains suppressed → no Monk reduction until −9 becomes operative again or ends.

Repeated same-card applications also remain separate records rather than refreshing into one synthetic record unless that exact source later says to refresh.

A completed target short or long rest ends **all active default-rest-ending Monk trauma records**, regardless of ordinary rest-reward limits.

Interrupted rest ends none.

Explicitly different endpoints remain independent.

---

# 4. “First fall” threshold semantics

Use **strict crossing**, not merely “a further HP decrease while already below.”

For these first-fall sources, a qualifying event must move actual normal HP from the non-trigger side to the trigger side using the **same event-effective maximum**.

### At-or-below quarter

For Anointed Guardian, Death's Threshold, Adrenal Floodgate:

`pre: 4 × HP > max`  
`post: 4 × HP <= max`

### Strictly below half

For Burning Blood IV:

`pre: 2 × HP >= max`  
`post: 2 × HP < max`

This is a **NEW common interpretation of “fall to/below” wording**.

### What HP changes count?

A genuine decrease in normal HP can establish the crossing whether caused by:

- damage; or
- direct HP loss,

unless that source expressly limits its trigger to damage.

A pure maximum-HP recomputation/clamp does **not** establish a threshold crossing for these event-trigger cards.

For a same-event max-HP change, snapshot the threshold transition from the real HP-changing portion before the stat clamp.

### Already below when rearmed

If a short rest refreshes a “first fall” use while the creature is already below the threshold:

- refreshing the use does not trigger it;
- taking another 1 HP loss while remaining below does not trigger it;
- the creature must first return to the non-trigger side, then genuinely cross again.

So Death's Threshold at HP5/max40 after a short rest does not immediately activate and does not activate from 5→4. If later healed above quarter and then falls back to ≤quarter, it can trigger.

A source saying “first time you **are** at/below…” would be different, but none of these four supplied crossing cards uses that construction.

---

# 5. Monk hit → damage → trauma ordering

Yes, with one precision.

### Cost/choice timing

For Ribcrusher Strike and analogous after-hit options:

1. Attack hits.
2. At the legal on-hit declaration window, choose the feature and pay its Ki/cost.
3. Cost/use is now committed.
4. Resolve ordinary attack damage and all ordinary consequences.
5. Resolve Wounds/Instant Death/death replacement.
6. If target is still an eligible **living creature** afterward, resolve the max-HP-trauma CON save.
7. On failure, add the trauma record.
8. Recompute effective maximum and clamp current HP if necessary.

If the attack ultimately kills the target and it remains Dead, the already-spent cost is not refunded and no transient Monk trauma needs to be attached to the corpse.

If a legal death replacement keeps/returns it living within that same damage resolution, the later rider may still resolve.

### CON save modifier

Use the target's **current applicable CON-save modifier at the rider-save step**, including consequences already established by the attack's Wound resolution.

So if that same attack generated a new Wound whose reviewed rule penalizes CON saves, that penalty applies to the subsequent trauma save.

### Frozen damage metrics

The max-HP reduction/clamp cannot retroactively change:

- pre-trauma Instant Death threshold;
- Wound trigger/DC;
- attack damage;
- `actualHpDamage`;
- `actualDamageDealt`;
- concentration damage.

The clamp is a stat consequence, not a second damage event.

This ordering is a **NEW shared hit-rider integration rule** for these supplied Monk trauma cards, not a claim about every hit rider in the game.

---

## Bounded decision record

These five points can be added to the implementation contract:

- Deathless Silence uses **source-next-start / target-next-end / target-rest** as three independent clocks.
- Conjuration + Flesh Ascendant stacking is a **NEW explicit Wizard-specific exception**; Conjuration level snapshots at creation, Flesh Ascendant is dynamically controller-qualified.
- Monk trauma arbitration is **global strongest across owners**, with independent records/clocks and target-rest clearing of default records.
- “First fall” means an actual **crossing**, including qualifying direct HP loss, not merely remaining below or changing maximum HP.
- Monk trauma riders resolve **after ordinary attack damage/survival**, with already-paid cost retained and current CON-save state used.

Maximum-HP composition remains **SOURCE-AUDITED / DRAFTABLE** pending exact implementation and tests; no whole-game completion is implied.
