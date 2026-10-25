# GPT maximum-HP exact implementation closure

Complete reply captured from Calibration Review through the official conversation connector. 58 supplied records; 60 targeted checks and 909 systemic states. Wider game remains open.

I find **no remaining concrete defect that blocks this bounded package**. The helper, tests, guide, and 58 bindings are consistent with the source conference and the five later boundary corrections.

One narrow predicate question should be recorded explicitly, and I have two non-blocking hardening notes.

## Rewind Wound predicate — current implementation is correct

`HpEventSnapshot.damage_left_below_half()` should **not** use the strict first-fall/crossing rule.

The source says:

> if the recorded damage **had reduced it below half maximum HP**

It does not say “first falls below,” “crosses below,” or require that the creature began at/above half.

For Rewind Wound, require:

- the historical event was genuine **damage**;
- it caused actual normal-HP decrease: `afterHP < beforeHP`;
- its resulting HP was strictly below half of the **effective maximum stored with that event**.

So:

- max100, HP60→49 from damage = qualifies;
- max100, HP40→30 from damage = also qualifies;
- max100, HP40→40 because temp HP absorbed everything = does not qualify;
- later maximum changes cannot alter the stored result.

That intentionally differs from the four “first fall” sources, which require crossing from the non-trigger side.

**Current helper is correct.**

---

# Implementation review

### Composition arithmetic

Accepted:

`preSystemic = max(1, base + compatible bonuses − global strongest Monk trauma)`

then:

`effectiveMax = max(1, floor(preSystemic × systemic factor product))`

Expedition and Exhaustion therefore continue multiplying the same otherwise-applicable maximum, with one final floor.

The 101 +20 −9 example producing 42 is correct.

No iterative recomputation drift is present.

### Modifier records

Accepted.

The ledger preserves application identity, owner, target, clocks, suppression and rest-ending status independently. Global arbitration selects rather than destroys weaker records, so suppression correctly exposes the next eligible Monk trauma.

Completed-target rest handling also correctly removes suppressed default-rest-ending trauma records.

### Global Monk arbitration

Accepted as the explicit correction to the older per-owner proposal.

One target gets one numerical Monk trauma value:

`max(all operative Monk trauma amounts across owners)`

while every application keeps its own clock/provenance.

No magnitude/clock merging occurs.

### Deathless Silence

The guide now has the correct three clocks:

- Monk self untargetability: **source-next-regular-start**;
- target defensive-passive suppression: **target-next-turn-end**;
- max-HP trauma: **completed target short/long rest**.

The max-HP helper only owns the third component; the already-reviewed control interface owns the first two.

Accepted.

### Capacity clamp

Accepted.

`apply_effective_maximum()` produces the intended result:

- normal current HP clamps downward;
- temp HP does not;
- no damage;
- no healing;
- no Wound;
- no death failure;
- no resource trigger;
- no first-fall trigger.

Removing a modifier restores capacity only.

Dead/Stable/dying states remain untouched.

### Wizard stacking exception

Accepted and correctly documented as **NEW**, rather than pretending the source explicitly supplied stacking permission.

Conjuration and Flesh Ascendant add only under this reviewed source-specific exception.

Also correct:

- Conjuration = creating Wizard level snapshot;
- its provenance stays with that summon/cast;
- controller changes do not rewrite it;
- Flesh Ascendant = current eligible controlling Wizard level;
- engine `[24]` and the named Flesh Ascendant card are one modifier identity.

### Flesh Ascendant alias note

Non-blocking implementation hardening:

The runtime should conceptually treat engine `[24]` and `wizard.hero.necromancer.flesh-ascendant` as aliases for **one effect identity**, not two independently suppressible applications.

The current group arbitration prevents numerical double-counting, so the bounded arithmetic is correct. When the later control/companion lifecycle creates actual runtime records, suppression/removal should operate on the shared Flesh Ascendant effect identity rather than suppressing one textual alias and accidentally revealing the other.

This does **not** block this package because runtime eligibility/record construction is explicitly outside its scope.

### Feat formulas

Accepted:

- `feat:tenacity`: dynamic +current level.
- `feat:tough`: acquisition snapshot `2 × acquisitionLevel`.
- `feat:tough_as_nails`: effectively dynamic `2 × currentLevel`, supported by explicit later-level growth.
- `feat:dark_fortitude`: dynamic `2 × currentLevel`.
- `feat:familiar_bond`: explicitly provisional maximum-capacity interpretation, dynamic with eligible owner's current level.

Distinct feat identities add; duplicate same feat does not.

No full feat-system promotion follows.

### Threshold mathematics

Accepted.

Cross multiplication correctly avoids rounded threshold mistakes.

The tests for odd maximum 101 are especially useful.

Strict first-fall behavior is correct:

- quarter inclusive: pre `>¼`, post `≤¼`;
- Burning Blood half: pre `≥½`, post `<½`.

Damage/direct HP loss can establish the transition.

Capacity-only changes cannot.

A refreshed use while already below threshold does not trigger from another loss that remains below.

### Continuous thresholds

Accepted:

- Wyrmhide;
- Brutality Sense;
- Pain Empowerment;
- Dark Fortitude conditional resistance;
- Life Drinker conditional damage;
- Regenerative Mutation eligibility.

They read current effective maximum when evaluated.

### Mythic Carapace / Butcherform

The guide correctly labels the interpretation **NEW**:

strictly below quarter is a continuous duration-ending state.

Thus max-HP changes alone can end these forms.

Exact quarter does not.

No issue.

### Death's Threshold exit

Accepted.

`healed_above_half()` requires a genuine positive HP-healing event whose resulting state is above half.

A capacity decrease alone cannot end Death's Threshold.

As previously decided, if a capacity change has already made the creature above half, a later genuine positive healing event while it remains above half satisfies “healed above half”; a crossing from below is not separately required.

### Percentage formulas

Accepted.

The primitive correctly avoids inventing min1:

- Wound Eater III at max3 → 0;
- source-explicit quarter recoveries → min1;
- viable resurrection bridge → min1 under that already-reviewed interface.

### Attack → Monk trauma ordering

Accepted.

The implementation boundary is correct:

1. hit;
2. feature chosen/cost committed;
3. ordinary attack damage;
4. Wounds/Instant Death/survival;
5. frozen damage metrics;
6. if still living/eligible, trauma CON save using then-current save modifier;
7. apply trauma;
8. recompute maximum;
9. clamp without damage.

The later stat change cannot alter already-resolved Wound, concentration, Instant Death or actual-damage metrics.

---

## Validation sufficiency

The current **60 targeted checks + 909 systemic parity states** adequately cover this bounded primitive.

Two additional regressions would be useful later but are not closure blockers:

- Mythic Carapace: HP10/max40 remains active, maximum changes to41 → continuous threshold becomes below-quarter.
- Rewind Wound: HP40→30/max100 qualifies despite already beginning below half, explicitly distinguishing it from `falls_across()`.

Those would make the two unusual semantic distinctions visually obvious in the report.

---

# Final disposition

> **Maximum-HP / percentage-threshold bounded interface: REVIEWED / reference-VALIDATED for the supplied 58 records (51 class passages + 7 feat records).**

Accepted evidence:

- **58 exact live source records/hashes PASS**
- **60 targeted maximum-HP checks PASS**
- **909 systemic composition states PASS**
- prior Strain maximum-HP composition remains intact
- original class/feat sources remain unchanged
- NEW interpretations and source-specific exceptions are labeled rather than silently attributed to source text

This bounded closure includes:

- additive modifier ledger;
- rational systemic composition;
- global strongest Monk trauma;
- capacity clamp semantics;
- Monk rest clearing;
- feat growth/snapshot modes represented here;
- Wizard Conjuration/Flesh Ascendant exception;
- exact percentage comparisons;
- first-fall crossings;
- continuous threshold predicates;
- historical event maximums;
- percentage amount calculations;
- attack-before-trauma ordering.

It does **not** close unsupplied item/spell/monster/disease/curse modifiers, non-Monk max-HP reductions, base HP/Constitution/multiclass advancement, feat retraining/duplication policy, familiar/companion/control lifecycle, unusual device viability, balance, human testing, publication readiness, or the game as a whole.

