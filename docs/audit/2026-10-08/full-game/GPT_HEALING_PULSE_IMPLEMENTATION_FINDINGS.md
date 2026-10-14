# GPT pulse exact implementation findings

Complete connector reply from the exact implementation turn, retrieved separately from the later notebook provenance instruction.

The scheduler architecture is sound, and the five specific source interpretations are consistent with the prior conference. I found **one implementation family defect with two manifestations**: exact-marker paid effects do not always terminate immediately when their required later payment/maintenance is unavailable. I would fix that before bounded closure.

## 1. Enhanced Garden — confirm replacement entitlement

Confirm the candidate interpretation.

`Enhanced Garden of Restoration` should **replace**, not add to, the base Garden first-contact cure entitlement.

Operationally:

- Base Garden: first eligible **entry or start** for that creature gives one entitlement to end Poisoned **or** repeat one permitted disease save.
- Enhanced Garden: that entitlement moves to the creature's **first Garden healing pulse** and upgrades to ending Poisoned **and** one disease that explicitly permits magical curing.
- Entry before that first pulse grants no separate base cure.
- The first enhanced pulse consumes the one entitlement even if HP gain is blocked.
- No creature can receive an entry cure and then a second enhanced pulse cure from the same Garden.

Label this **NEW source-specific mastery integration**. The mastery text clearly points to the “first Garden pulse” and “rather than” the lesser benefit, but it does not independently spell out removal of the earlier entry trigger.

Current `FirstContactLedger` correctly implements this.

---

## 2. Whole-effect suppression versus HP-only blocking

Confirm.

A due scheduled occurrence has three distinct concepts:

1. opportunity occurred;
2. named benefit was delivered;
3. actual HP was gained.

### Whole-effect suppression

If the **entire effect/pulse** is suppressed:

- consume that pulse/window opportunity;
- no catch-up;
- no output targets;
- no independent source component covered by that suppression;
- do **not** claim Circle's global named-benefit target/round ledger.

Thus another legal Circle instance could affect that creature later in the same numbered round because the creature never actually received the named Circle benefit.

### HP gain only blocked

If the pulse itself resolves normally but HP restoration is later reduced/prohibited:

- cost/opportunity remains spent;
- target receives/attempts the named pulse;
- normal target/round budget is claimed;
- independent cures/resources resolve according to their own predicates.

Decay/full HP is therefore **not** `whole_effect_suppressed`.

The helper currently represents this correctly.

---

## 3. Unfinished Chorus timing — confirm

The current two-pulse model is correct.

`oracle.supplement.bones.unfinished-chorus`:

- Action + 3 RC activates during a regular source turn.
- That activation includes **pulse/drain 1 during that same source turn**.
- Fixed Oracle roster remains up to 3 enemies + 3 allies under engine[26].
- On the next regular source turn, one later drain opportunity exists.
- Before that later pulse, pay **1 RC**.
- No Bonus Action is invented.
- The actual drain chooses one legal living enemy; heal destination is self or one legal ally as printed and validated by caller.
- If required later upkeep is not completed by that source turn's end, Chorus ends then.
- Otherwise its two-round duration ends at the following source-start deadline.
- Revelation backlash begins after Chorus ends according to its own printed clock.

So there are **two drain opportunities total**, not activation plus two later pulses.

Current profile/count and successful-pulse test match this.

---

## 4. Renewal / Echo Totem — confirm source-specific integration

Correct to stop referring to this as though the existing Blight-Totem healing-reduction helper already implements Echo arbitration.

For Renewal + its Echo:

- one parent family;
- one upkeep;
- one concentration burden;
- one pulse opportunity;
- one ≤3-recipient family budget;
- parent source base = 2;
- Echo source base = `floor(2/2)=1`.

`renewal_branch_bases()` correctly returns **alternative source bases** only.

Caller must then:

1. construct each currently legal branch from its own correct source base;
2. apply modifiers in their proper stages;
3. compare the resulting legal same-name alternatives;
4. commit one strongest legal application.

Do not:

- add parent + Echo;
- halve the already fully modified parent final healing;
- expand to six targets.

Parent/Echo destruction linkage remains deferred to the object lifecycle. Caller-provided anchor-active/coverage state is the correct boundary.

---

## 5. Independent Renewal instances — confirm

Correct.

No global:

`Renewal + target + numberedRound`

ban should be invented.

Instead:

- parent+Echo of one Renewal = one family instance;
- simultaneous/same-opportunity overlapping Renewal effects use strongest legal nonstacking result;
- separately created Renewal instances with genuinely different scheduled pulse opportunities may each heal the same target within one numbered round.

That honors “same-name/stat auras do not stack” without converting it into “a creature can only ever receive Renewal once per round.”

Current helper appropriately expects caller arbitration for competing independent instances.

---

# Concrete blocker: exact-marker payment failure

This is the remaining implementation defect.

The guide correctly says:

- Song later pulse: pay 1 RC **before that pulse or end**.
- Enhanced Song third pulse: same.
- Wound Eater IV later pulses: pay 1 RC **before each later pulse or end**.
- Oracle funded windows: pay at the exact source regular-start marker or end.

But `PulseSeries.resolve()` does not currently end a `sequence` or `delayed-sequence` effect when `wallet.spend()` fails at an exact paid due marker.

Example:

```python
song.resolve(1, ClockMarker(6), ..., PulseWallet(rc=0))
```

`wallet.spend()` raises, but Song remains pending/active until a later `advance()` notices the missed marker.

Worse, the caller could technically call `resolve()` again at the same marker after obtaining/replacing RC and succeed. That contradicts the current source contract: **if the required payment is unavailable when the pulse is due, the effect ends then.**

### Required correction

For exact-marker later payments in:

- `sequence`
- `delayed-sequence`

when `index > 0` and `later_cost > 0`:

```text
attempt required payment
if payment fails:
    end(now, "unpaid due pulse")
    re-raise
```

No ledger/declaration/pulse state should commit before successful payment.

This applies presently to:

- `song-of-mending`
- `enhanced-song`
- `wound-eater-iv`

It should **not** change ordinary maintenance effects such as Briar/Lifewell/Circle/Restoration Field/Chorus, because those may satisfy maintenance at any legal point before their **turn-end deadline**.

For those, failure at an early attempt can leave the opportunity pending until turn end.

---

## Same issue for `upkeep_legal=False` on exact due windows

`fund()` currently ends correctly when the wallet cannot pay, but not when:

```python
upkeep_legal=False
```

It merely raises.

For an actual regular source marker where an Oracle window's required upkeep is due, if the actual source state makes that upkeep **illegal**, the window/effect should end at that due marker. It cannot be resumed later in the same window.

Likewise for exact-marker paid Song/Wound Eater pulses.

Distinguish this from an extra turn:

- `regular=False` is not the real due regular marker and should not terminate anything merely because someone tried to call the helper there.
- At the actual registered regular marker with `regular=True`, an illegal required upkeep means the due payment cannot occur → effect ends.

Recommended behavior:

```text
if actual due regular marker:
    if upkeep not legal:
        end(now, "illegal due upkeep")
        reject
    if required payment fails:
        end(now, "unpaid due upkeep")
        reject
```

For turn-window maintenance modes, continue using the later turn-end deadline instead.

### Regression tests needed

At minimum:

- Song second pulse with RC0 → rejects **and `ended_at == dueMarker`**.
- Wound Eater second pulse with RC0 → same.
- Garden window2 `upkeep_legal=False` at source marker → ends immediately.
- Lifewell early failed payment attempt does **not** immediately end before its maintenance deadline.

That last test protects the deliberate difference between exact-marker upkeep and by-turn-end maintenance.

---

# Other reviewed boundaries

I find the following correct as submitted:

- original virtual source/target markers retained;
- no activation+6 drift when a schedule already exists;
- ordinary duration expiry before start triggers;
- explicit Hemostasis/Wound Eater sequences receive their final scheduled tick before sequence termination;
- Crown/Garden normal source-duration expiry can result in fewer than three target-start benefits;
- fixed Oracle beneficiary sets;
- Eternal Bloom ≤3 initial selected allies only;
- Bloom reserve partitions and lost installments;
- Garden entry cure versus Seed first-pulse cure;
- fixed versus repicked recipients;
- payment/declaration committed before healing outcomes;
- full HP/Decay does not refund paid opportunities;
- empty legal maintenance allowed where no minimum recipient is required;
- Transcendent Meditation pulse-2 Ki independent of actual HP gain;
- whole-effect suppression suppresses that independent Ki occurrence;
- native recurrence has no invented three-pulse cap;
- Circle global named-effect budget versus Field/Oracle/instance budgets;
- Nano-Aegis has no free activation pulse and missing commands do not terminate mode;
- Nano's printed max-three cap survives duration extension;
- companion command ceiling remains caller-owned rather than reinvented here;
- disabled/suppressed clocks continue and never bank opportunities.

One non-blocking hardening test would also be useful: a suppressed Circle occurrence should consume its own pulse but leave the shared named-target-round ledger unclaimed, allowing another Circle to affect that target that round. The code appears to do this already.

## Disposition

The package should remain:

> **IN REVIEW — bounded 100-source recurring-healing/pulse scheduler**

until the exact-marker illegal/unpaid-upkeep termination behavior above is corrected and regression-tested.

After that correction, I see no other blocker in the submitted scheduler primitive. The eventual closure would apply only to the supplied **100 source roles + 6 supporting passages and their scheduling/budget interfaces**, not to whole cards, the 770 unfinished spells, companion/object lifecycle, general action/command execution, or whole-game healing-zone completeness.

