# Actual GPT exact manuscript review

This candidate is very close. I approve the substantive reconciliations, including the Counterspell correction. I find **one required geometry repair affecting two cards** and **one small Counterspell wording safeguard**. Everything else is manuscript-ready as written.

## 1. Dispel Magic (Lesser) — approved

The rank ceiling and one-effect interpretation are correct.

- Actual generating **spell rank ≤2** controls.
- “Tier 2” does not expand beyond rank 2.
- One selected ongoing effect per cast.
- Automatic when eligible.
- No invented high-rank check.
- Curse only if itself an eligible removable ongoing spell effect.
- Ending invokes that effect’s own ending procedure without historical rollback.

No repair.

## 2. Protection from Energy — approved

Confirmed exactly as authored:

**acid, cold, fire, lightning, thunder, force, necrotic, radiant**

and specifically **not**:

- bludgeoning/piercing/slashing;
- poison;
- psychic;
- Corruption.

Preserve actual **immunity**, 1 minute, no concentration.

One application per target across all casters with replacement is correct. Immunity does not remove unrelated riders and cannot mitigate a post-defense transfer branch explicitly barred from a second mitigation stage.

No repair.

## 3. Barrier of Faith — one required overlap repair

The no-support/Falling principle is correct, but this sentence is too broad:

> “if permitted Falling leaves a creature straddling the wall, it may finish leaving the overlap to either side”

That can let a creature that clearly approached the boundary from one side use the overlap state to choose the forbidden opposite side.

Use:

> **If unsupported Falling leaves a matching creature overlapping the wall, and the creature had a determinate legal side immediately before that overlap, it must clear the overlap back to that side using ordinary legal movement. If it descended from above with no determinate prior side, it may clear the overlap to either side using ordinary legal movement. Clearing overlap grants no free movement, added displacement, damage, or later permission to cross the wall.**

Everything else is approved.

This preserves the special case you correctly identified: descending vertically from above can produce an overlap with **no previous side**, while preventing deliberate wall-crossing by manufacturing an overlap from a known side.

## 4. Corruption Cleanse — approved

The environmental extent clarification is correct.

For area mode:

- entire active environmental effect must fit inside the bounded 10-ft-radius/10-ft-high cleansing area;
- **unless its own source explicitly permits localized cleansing**;
- then only the bounded portion is removed.

This prevents “touch one corner, cleanse a continent.”

Ordinary Corrupted remains an eligible minor condition. No Unity Exposure/numeric-track reduction, causal-major-source erasure, Oracle Curse removal, historical alignment restoration, Wound/death reversal, or reapplication grace period.

No repair.

## 5. Faction Ward — approved

The behavioral ward is complete and correctly separated from Faction Seal.

Confirmed:

- authorized canonical `factionId`;
- negative means −3/−2/−1;
- missing standing = unknown;
- already-inside creatures remain/leave;
- willing entry prohibited;
- forced movement, Falling, and teleportation pass;
- no detection effect;
- no legality/membership/standing/morality creation.

No repair.

## 6. Counterspell — approve the Core roll correction

Your correction is better supported than my earlier binary-check formulation.

The ordinary spell should use the existing fixed-DC **task/check degree system**, because the Core overlay already establishes that procedure and Counterspell explicitly calls for an ability check.

Therefore approve:

**spellcasting ability + PB vs DC 10 + 2 × actual triggering spell rank**

with:

- four ordinary task degrees;
- natural 20 improves one degree;
- natural 1 worsens one degree;
- then collapse Critical Success/Success → **success**;
- collapse Failure/Critical Failure → **failure**;
- no extra Counterspell effect from either critical degree.

Your examples are correct.

The existing Wizard/Mage class cards similarly use their **printed Intelligence check + PB**, under the same generic fixed-DC check rules unless those cards later receive an explicit exception.

### Cross-namespace attempt limit

Confirmed. “One attempt by this creature against this pending cast” is shared across:

- ordinary Counterspell spell;
- Wizard Counterspell card;
- Mage Counterspell card;
- any other same-named source that does not explicitly override the attempt limit.

Switching source namespaces cannot manufacture a second attempt against the same cast.

Add one small safeguard to the limitations:

> **An exact source that expressly grants an additional Counterspell attempt against the same pending cast overrides this default; merely granting another Reaction does not.**

That prevents this manuscript rule from accidentally nullifying some future explicit feature while retaining the current anti-double-attempt boundary.

### Counter timing

Approved.

The chronological sequence is:

1. Cast starts.
2. Verify legality.
3. Commit RP/material/other costs.
4. Perform components.
5. End incompatible prior concentration / establish new concentration state as required.
6. Apply Dissonance, Refrain, and hooks whose exact trigger is casting/beginning the spell.
7. Open Counterspell reactions.
8. Resolve nested counters last-in, first-out.
9. If original cast survives, resolve its effect.
10. Resolve success/damage/effect hooks at their own printed timing.

Negated casts refund nothing and do not restore displaced concentration.

Each nested cast owns its own chronological Refrain/Dissonance update. Resuming a parent does not “recast” it or rewrite history.

Ready gets this window at **preparation only**, never release.

Counterspell is not whole-Action denial.

That is ready to propagate into the shared integration manuscript after these cards are approved.

## 7. Magic Circle — same required overlap repair as Barrier of Faith

Replace:

> “if permitted Falling ends with a matching creature straddling the boundary, it may leave that overlap to either side…”

with:

> **If unsupported Falling leaves a matching creature overlapping the lateral boundary, and it had a determinate legal side immediately before that overlap, it must clear the overlap back to that side using ordinary legal movement. If it descended from above with no determinate prior side, it may clear the overlap to either side using ordinary legal movement. Clearing overlap grants no free movement or subsequent permission to re-enter through the boundary.**

The remainder is approved:

- rank-3 Abjuration and Universal same procedure;
- 10-ft radius;
- 10-ft-high lateral cylinder;
- inward-only restriction;
- existing matching occupants may leave;
- no reverse prison;
- no roof/floor;
- teleportation not physical crossing;
- no save.

## 8. Dispel Magic — approved

Correctly bounded to one ongoing effect generated by **rank 0–3**.

The Universal wording does not create unlimited dispelling.

All Lesser/Resonance principles carry correctly:

- originating cast rank;
- no global purge;
- no unknown-rank guessing;
- no permanent item/class engine/trait stripping;
- no historical rollback;
- protected curses/effects retain protection.

No repair.

## 9. Barrier Field — approved, including the origin rule

The proposed origin procedure is the right way to prevent “I place the fireball center six inches past the dome, therefore nothing crossed it.”

Keep:

> for a cast that directly deals damage, trace from caster/source to the target or initial area origin.

If that damaging projection must cross the hemisphere, its damaging part is blocked.

Also confirmed:

- friendly intent does not bypass it;
- target willingness does not bypass it;
- attacks/damage are blocked both directions;
- nondamaging separable components may resolve;
- movement and nondamaging magic remain legal;
- existing independent effects use their actual established source/origin;
- no global antimagic;
- no general prohibition on creatures inside taking Actions or attacking targets on the same side.

For later persistent damaging zones, use the same principle naturally: the **initial establishment of that damaging source** must satisfy the boundary rule. Once legally established, subsequent packets use that effect’s actual current origin. This closes the only obvious “create hostile zone across the dome” loophole without needing another card rule.

No textual repair required if that is already covered by your shared origin procedure; it is an interpretation of the authored language, not extra card power.

## 10. Remove Curse — approved

The hidden-curse procedure is correct and does not provide free diagnosis.

Legal target = perceived creature/object.

Then:

- pay/cast;
- Director resolves actual curse records;
- known distinguishable curse may be selected;
- otherwise Director selects one eligible hidden removable curse;
- if none exists, nothing happens and there is no refund or diagnostic response beyond the observable lack of removal.

No invented rank ceiling.

Explicit special cures/non-removability/protected information override.

Oracle intrinsic Curse/Burden remains outside eligibility.

No repair.

## 11. Protection from Scrying — approved

The operational interpretation properly preserves “immune to divination and scrying” without making it immunity to damage merely because a spell belongs to Divination.

Confirmed:

- protects against **new information about the target**;
- hostile and beneficial Divination/Scrying both fail;
- area/multi-target sources can still learn legal information about others;
- actual source classification controls;
- class senses are suppressed only where their actual source qualifies;
- no underlying engine deletion;
- no memory erasure, retroactivity, invisibility, disguise, or combat defense.

One hour/no concentration is an acceptable required duration completion.

No repair.

## 12. Resonance Anchor — approved

The location-versus-shape distinction is correct.

“Fix in place” means:

- spatial origin cannot move/recenter;
- source-authorized radius/shape evolution can still occur;
- nonspatial state evolution continues normally.

So, for example, a source that explicitly expands from radius 10 → 15 while remaining centered at the same origin may still expand. Anchor does not freeze its entire state machine.

Also confirmed:

- own concentration-dependent target rejected **at preflight**;
- no wasteful payment for a target known to disappear during Anchor’s concentration transition;
- another caster can maintain their concentration;
- Anchor cannot target itself/another Anchor;
- Anchor itself remains dispellable;
- no duration extension, pulse reset, resource restoration, revival, Time Loop change, or retroactive counter protection.

No repair.

## 13. Alignment Sanctuary — approved

The save-window completion is good and gives this effect a deterministic cadence.

### Rank-3 Abjuration

Approve one recorded entry result keyed to:

**source character + mode + target**

until target’s **next future regular-start marker**, or +6 seconds outside initiative.

During that window:

- success permits otherwise legal entry attempts through that ward;
- failure blocks all non-Falling entry attempts;
- repeated pushes/carry attempts/teleports do not manufacture rerolls;
- same-caster replacement/recast does not reset the existing window;
- different casters remain independent;
- success against Ward A never authorizes crossing Ward B.

That is cleaner than “save every inch of movement.”

Unsupported Falling remains outside this entry-save process because the area supplies no physical support.

### Rank-6 Conjuration/Shaman

Requiring **both actual caster alignment axes to be explicitly recorded before casting** is correct. Otherwise the spell would create an unusable sanctuary from unknown data.

Admission likewise requires both target axes explicitly recorded and exactly matching the snapshot.

### Rank-6 Abjuration placement

Correctly remains preserved but **unassigned/unavailable**. Its vague “aligned creatures gain benefits” text contributes nothing to either playable mode.

No repair.

---

# Manuscript disposition

Apply these exact changes:

1. **Barrier of Faith:** replace the unrestricted “either side” Falling-overlap clearance with determinate-prior-side / no-prior-side wording above.
2. **Magic Circle:** same repair.
3. **Counterspell:** add the narrow explicit-source-override sentence for the one-attempt rule.

Everything else is approved as authored.

After those three textual repairs, I approve all thirteen as:

> **REVIEWED authored operational PLAYTEST manuscript — runtime and balance validation pending**

The selectable catalog may then move from **107 → 120**, leaving **728 unfinished** of the preserved 848 identities.

The 18 placements/Core records remain preserved, including both Counterspell placements, both Magic Circle placements, both Dispel Magic placements, the two operational Alignment Sanctuary modes, and the unassigned rank-6 Abjuration Alignment Sanctuary evidence.

