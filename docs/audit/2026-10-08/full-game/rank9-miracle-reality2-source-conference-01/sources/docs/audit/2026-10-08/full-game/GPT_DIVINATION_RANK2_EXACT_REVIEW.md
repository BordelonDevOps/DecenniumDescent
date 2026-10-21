# Rank-two Divination — exact manuscript review

Conversation: Calibration Review
Turn: 011bae89-9716-46bf-93cd-75f05c75f98d

I find **three small manuscript repairs**, all for the same reason: hidden facts should be resolved by the information effect after costs are committed, not accidentally exposed during target-legality preflight. The substantive mechanics of all eight cards are otherwise approved.

## 1. Augury — approved

The exact completion is sound.

Confirmed:

- Self informational casting.
- Course must be intended to begin within 60 seconds.
- The 30-minute horizon begins at that proposed start, not at spell resolution.
- Yes = materially favors stated practical goal.
- No = materially harms/frustrates it.
- Neutral/mixed/insufficiently weighted = Unclear.
- “Good/bad” is not moral alignment.
- No obligation actually to begin the course.
- Future agency/new events can alter the predicted outcome.
- Equivalent course/goal inquiries under unchanged circumstances do not produce reroll-fishing across casters.

No repair.

## 2. Divine Perception — approved

The independent category/provenance handling is correct.

It may report any readable combination of:

- Blessed;
- Cursed;
- Possessed;
- Other Divine Influence;
- plus `Indeterminate` where a relevant category/provenance cannot be resolved.

Multiple influences of the same category do not create a count.

`No Divine Influence` is valid only when absence can actually be established; unknown/protected provenance cannot be converted into false negative evidence.

Also correct: the spell does **not** automatically disclose deity/controller identity, location, statistics, theology, or removal method simply because some deeper Director record contains those facts.

No repair.

## 3. Clairvoyance — approved

The remote point interface is complete and remains faithful to the conference.

Approved:

- explicit 1-mile effect range over raw Core 30 ft;
- one fixed point;
- uniquely designated unseen points may qualify through precise relative location;
- no originating sight/LoE;
- point cannot occupy solid matter;
- Sight **or** Hearing chosen at cast;
- no mode switching;
- all-direction attention from the fixed point is allowed;
- point itself never translates/moves/pans;
- ordinary light/sound/obscurity;
- Blindness/Deafened suppress corresponding feed;
- local senses retained;
- same-plane/1-mile tether;
- no concentration;
- one active point per caster.

No repair.

## 4. Vision Trap — approved

The later-cast rider handling is correct:

- failed save: new pending rider applies/replaces the old pending rider;
- successful save: no new rider exists, so an already-valid older rider is not erased;
- every cast still resolves its own instantaneous damage.

The hostile one-round endpoint is also correct: first future target regular-turn **end strictly after application**, with no counting an end phase already underway.

Damage and rider remain separable for defenses.

No repair.

## 5. Locate Person — one required target/preflight repair

The actual effect is approved, but the `targets` field currently says:

> “one specific individual person ... **within 1 mile on your plane**.”

Those are precisely facts the spell is meant to discover. Under the shared casting model, hidden target legality should not tell the caster for free that the person is within one mile, on this plane, alive, or otherwise eligible before costs are paid.

Replace `targets` with:

> **Self; designate one intended specific person through personal acquaintance or a reliable identity description/name intended to refer to one actual individual.**

Then retain the resolution gate, preferably as:

> **After costs are committed, resolve whether the designation identifies one actual qualifying person and whether that person currently exists as an eligible creature on your plane within 5,280 feet with readable location information. If so, privately learn the direction. Otherwise receive no direction, without distinguishing ambiguity, death/destruction, range, plane, eligibility or protection.**

This keeps the active Undead/Construct continuing-person interpretation and all other approved behavior unchanged.

## 6. Faction Spy — one required target/preflight repair

The substantive spell is approved, including:

- any-distance **same-plane** observation;
- no reputation/membership gate;
- specific identifiable HQ;
- known room/common-area selection or deterministic primary-area fallback;
- center-of-usable-room viewpoint at ordinary eye height;
- nearest legal point within that same selected room if obstructed;
- one point per caster;
- sight + hearing;
- no viewpoint translation;
- mobile structure carries its room;
- institutional relocation/ownership change does not retarget an already-created point;
- same-plane separation suppresses feed without resetting time.

But `targets` currently says:

> “... headquarters ... **at any distance on your plane**.”

Again, actual plane status can itself be unknown information. Avoid making that a pre-payment legality diagnostic.

Replace `targets` with:

> **Self; choose one specifically identifiable headquarters of one exact canonical faction and the qualifying room/area to observe.**

Then in resolution/effect explicitly keep:

> **The observation feed operates only while the selected physical viewpoint and caster are on the same plane. If they are not, no remote sight or hearing is received and the spell does not identify plane separation as the reason.**

This does **not** grant interplanar viewing or secret-HQ discovery; it merely moves the same-plane check to effect resolution where it belongs.

The existing room-selection language is otherwise approved. Knowing a real specifically established room can identify it; the spell does not discover an unknown secret room merely because one exists.

## 7. Alignment Prediction — approved

This remains a forecast rather than coercion.

Approved:

- one specific imminent situation expected within 60 seconds;
- one most likely immediate voluntary response;
- actual individual alignment may inform the result without stereotyping;
- other motives/facts can outweigh alignment;
- no forced behavior, PvP, oath violation, or automatic moral rule;
- no free exact alignment reading;
- no thoughts/motives dump;
- `Indeterminate` only where genuinely needed;
- materially equivalent scenarios do not sample alternate futures.

No repair.

## 8. Resonance Tracking — one required target/preflight wording repair

The detailed tracking procedure is approved, including all of the exact-card additions you called out:

- current Resonance Tracking cast cannot select itself;
- older Tracking casts can leave their own origin trace;
- observing a trace creates no copy/path/refreshed age;
- equal timestamps use cast-start order, then fixed neutral event order;
- known protected event gives no read rather than silently switching;
- unknown selection uses most recent readable qualifying event;
- ongoing spell components become readable only after actually occurring;
- every component expires at **original cast start + 3,600 seconds**;
- at the exact 3,600-second endpoint, it is gone;
- therefore initial age eligibility is strictly `< 3,600`;
- independent later planar travel only permits reading genuine local segments there;
- no remote interplanar sensor.

However, the current `targets` begins:

> “Self; initially select one **actual spell-casting trace within 30 feet and line of effect**...”

That can imply a qualifying trace must already exist as a legal target before payment, conflicting with the later rule that a legal cast can simply find nothing.

Replace it with:

> **Self; search the area within 30 feet and line of effect for one qualifying actual spell-casting trace, then track the selected event’s surviving local trace under this spell’s rules.**

Keep actual trace existence/age/protection selection entirely in `resolution`.

That avoids free “there is/isn't a trace here” target validation and matches the authored no-result procedure.

---

## Disposition

Apply exactly these three wording repairs:

1. **Locate Person:** remove actual range/plane/existence eligibility from the `targets` preflight field; resolve those facts after commitment.
2. **Faction Spy:** remove “on your plane” as target-legality information; enforce same-plane only as the observation-feed condition.
3. **Resonance Tracking:** make Self/search-area the legal target rather than requiring an actual qualifying trace before casting.

All other functional fields are approved unchanged.

After those repairs, all eight may be promoted to:

> **REVIEWED authored operational PLAYTEST manuscript — runtime, numerical balance, and broader Divination/information-system validation pending**

The catalog may then move from **182 → 190 reviewed identities**, leaving **658 unfinished** of the preserved 848.

