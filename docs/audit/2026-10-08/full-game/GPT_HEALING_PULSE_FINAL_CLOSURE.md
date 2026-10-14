# GPT healing-pulse final closure

Complete reply captured from Calibration Review, paired with CODEX_HEALING_PULSE_FINAL_DISPOSITION.md. Bounded100+6 source interface;89 targeted checks,301 reserve partitions and33 profile provenance checks. Whole-game work remains open.

I find **no remaining concrete defect that blocks this bounded scheduler package**. The previous exact-marker payment/illegal-upkeep defect is correctly fixed, and the new regressions cover the failure modes I requested.

## Final disposition

> **Healing pulse / sustained-zone scheduling interface: REVIEWED / reference-VALIDATED for the supplied 100 class records + 6 supporting passages.**

Accepted evidence:

- **100 exact source records: PASS**
- **6 exact supporting passages: PASS**
- **33 internal scheduling/native/contact aliases have explicit provenance: PASS**
- **89 targeted scheduler checks: PASS**
- **301 Eternal Bloom reserve partitions: PASS**
- original class/card objects and frozen shared class guide remain unchanged

The 33 helper labels are internal aliases only. They do **not** constitute new spells, abilities, feats, class cards, or game content.

## Exact-marker correction — accepted

The corrected distinction is now right.

For exact due-marker payments:

- Song of Mending
- Enhanced Song
- Wound Eater IV
- Oracle funded windows

if the required resource is unavailable at the actual registered marker:

- payment fails atomically;
- no declaration/recipient ledger commits;
- effect ends at that due marker;
- acquiring resources afterward cannot retry the same marker.

If upkeep is actually illegal at that marker, the same immediate-end behavior applies.

`regular=False` extra-turn calls correctly:

- grant no pulse/payment opportunity;
- do not kill the real pending opportunity;
- do not advance the registered regular-turn cadence.

By-turn-end maintenance remains intentionally different:

- Lifewell
- Briar
- Circle
- Renewal
- Restoration Field
- Sacrament/Dark Sacrament
- similar maintenance profiles

An early failed payment attempt does not itself end those. They remain pending until their actual maintenance deadline.

Accepted.

---

## Enhanced Garden — accepted

The guide now accurately records the approved **NEW source-specific mastery integration**.

Base Garden:

- first eligible entry or start → one cure entitlement;
- choose Poisoned removal or disease-save repeat.

Enhanced Garden replaces that entitlement:

- no separate entry cure;
- first actual Garden pulse → may end both Poisoned and one magically curable disease;
- only one entitlement from that Garden instance;
- HP gain may be blocked without invalidating the independent cure opportunity.

`FirstContactLedger` matches this.

---

## Whole-effect suppression — accepted

The distinction is now correct.

A wholly suppressed scheduled occurrence:

- consumes its own opportunity;
- receives no catch-up;
- produces no output target benefit;
- suppresses covered independent components;
- does **not** claim Circle's global named-effect benefit ledger.

Thus another operative Circle can benefit that target in the same numbered round.

Conversely, ordinary HP blocking such as:

- full HP;
- Decay;
- healing reduction to zero,

does not mean the pulse itself was suppressed. Its named benefit/opportunity is still consumed and its ordinary budget remains claimed.

The new Circle regression confirms the intended behavior.

---

## Unfinished Chorus — accepted

Current profile is correct:

- activation Action +3 RC;
- first drain on activation/source turn is included;
- one later regular-source-turn drain;
- later drain requires 1 RC;
- no invented Bonus Action;
- exactly **two** drain opportunities;
- fixed Oracle roster remains bounded;
- caller handles the printed one-enemy drain and self/one-ally heal destination.

The scheduler does not invent a third pulse.

Accepted.

---

## Renewal / Echo Totem — accepted

The implementation now describes what it actually does instead of borrowing terminology from the unrelated Blight Totem healing-reduction rule.

`renewal_branch_bases()` correctly exposes:

- parent legal source base = 2;
- Echo legal source base = 1.

Those are alternatives.

Caller then applies each branch's legitimate modifiers at their proper stages and selects the strongest legal same-name result.

Correct prohibitions:

- do not add parent + Echo;
- do not halve the fully modified parent's final output;
- do not double the recipient budget;
- do not create another upkeep payment;
- do not create another pulse.

Parent/Echo destruction coupling remains correctly deferred.

Independent Renewals also remain separate. There is no invented global Renewal-per-target-per-round ceiling. Same-opportunity overlapping Renewals use strongest nonstacking coverage, while genuinely separate scheduled pulses may both heal in one numbered round.

Accepted.

---

## Clock handling — accepted

The helper now preserves the existing Combat timing model:

- original virtual source/target markers;
- no activation+6 drift where a marker already exists;
- no restart from initiative reorder/reentry;
- extra turns do not generate regular periodic opportunities;
- ordinary source-controlled duration expiry precedes start triggers;
- explicit delayed sequences such as Hemostasis and Wound Eater IV get their printed final tick before sequence exhaustion.

The test at activation second2 with next marker6 verifies the important phase-preservation case.

No issue remains here.

---

## Fixed and repicked targeting — accepted

The bounded responsibilities are appropriately divided.

Scheduler enforces:

- fixed roster membership where applicable;
- recipient count;
- instance/named round budget;
- no replacing a fixed target;
- no replay.

Caller still owns:

- ally/enemy subcaps;
- living/functional state;
- range;
- line of effect;
- current source authorization.

The generic cap6 for mixed-source profiles is correctly documented as:

> maximum three allies **plus** maximum three enemies,

not six interchangeable creatures.

One implementation expectation should remain explicit at the caller boundary: for sources whose exact text says **each fixed target** receives the pulse, the caller supplies all currently eligible fixed targets rather than arbitrarily withholding one. That is target-resolution legality, not a scheduler defect.

---

## Eternal Bloom — accepted

`installments()` and `BloomReserve` correctly implement:

- fixed selected roster ≤3;
- missing HP snapshot at activation;
- three integer installments;
- earlier installments receive remainder;
- 10 → 4/3/3;
- 1 → 1/0/0;
- absence/ineligibility loses the scheduled installment;
- later damage cannot expand the reserve;
- no catch-up;
- no new entrant.

Its separate 1-HP floor remains outside the healing installment arithmetic.

301 exhaustive reserve partitions are sufficient for this primitive.

---

## Native recurrence — accepted

The package correctly does **not** force native recurrence into a three-pulse model.

This includes:

- Aura of Grace
- Living Pulse
- Thief Exsanguinate
- Regenerative Mutation
- Bloodthick Node
- Rapid Coagulation

Their individual eligibility/cost/reserve conditions remain caller/source responsibilities.

Extra turns do not manufacture another regular recurrence.

Accepted.

---

## Nano-Aegis — accepted within boundary

The scheduler correctly enforces only what this package owns:

- support mode activation has no free heal;
- BA command +1 RP per support output;
- heal **or** temp HP;
- maximum 3 pulses;
- skipped commands do not terminate support mode;
- duration extensions cannot create a fourth healing pulse;
- an extra full Action alone cannot satisfy a Bonus Action requirement.

The broader shared companion-command budget remains deliberately outside this package.

That is the correct separation.

---

## Provenance review

The explicit `healing_pulse_profiles.json` mapping resolves the concern about accidental invented content.

Every currently executable helper label maps to supplied sources:

- **24 schedule profiles**
- **6 native recurrence profiles**
- **3 contact variants**

No unmapped spell/ability name is being treated as game content.

The scheduler may use internal identifiers such as `enhanced-song` or `renewal-extended`, but those are implementation aliases for the actual listed sources, not new cards.

That provenance requirement should remain mandatory for future helper profiles.

---

# Bounded closure record

I would update the package statuses to:

> **REVIEWED / reference-VALIDATED — supplied healing-pulse, sustained-zone, upkeep, recurrence, finite-installment and contact-entitlement scheduling interface.**

This closure includes only:

- the supplied 100 source roles;
- the 6 supporting timing/class passages;
- the 33 provenanced runtime aliases;
- payment/action scheduling;
- missed-upkeep termination;
- original virtual markers;
- fixed/repicked roster mechanics represented here;
- named/instance target budgets;
- Oracle funded windows;
- delayed sequences;
- finite Bloom reserves;
- Renewal/Echo pulse-family arbitration;
- native recurrence cadence;
- Nano-Aegis's printed pulse ceiling.

It does **not** close:

- complete behavior of all 100 cards;
- the companion command engine;
- Totem/device destruction and reconstruction lifecycle;
- Echo-parent destruction behavior;
- the prepared 74-device/Totem packet;
- Magnetic Wall semantics;
- the 770 unfinished spells;
- unsupplied items/monsters;
- all zone sources across the game;
- numerical balance or human testing;
- publication readiness or the game as a whole.

The newly captured **Magnetic Wall** should remain untouched until the next 74-passage device/Totem conference; its discovery correctly demonstrates why lexical candidate counts are evidence sets, not completeness guarantees.

