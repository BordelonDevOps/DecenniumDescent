# GPT creature event model boundaries

Paired with CODEX_CREATURE_LIFECYCLE_EVENT_BOUNDARIES.md. Exact notebook reply; source-audited, implementation pending.

These four distinctions can be fixed as event-model rules without expanding the source set.

## 1. Auto-Raise and the attached companion phase

Confirm the proposal with one qualification: the attached companion phase gets an **event-resolution checkpoint**, not a second regular turn marker.

### Ordinary sequence

For a commanded standard undead:

1. Wizard finishes the whole regular turn.
2. Attached companion phase begins.
3. Commanded movement/action resolves.
4. Resolve immediate consequences of that action in normal causal order.
5. Resolve any already-due attached-phase damage/death events in stable application order.
6. **Auto-Raise checkpoint.**
7. Resolve any expressly attached-phase ending cleanup.
8. Attached phase closes.

If the commanded attack kills an eligible creature, Auto-Raise therefore resolves at **that attached phase's checkpoint in the same numbered round**. It does not wait until the Wizard's next turn and does not reopen the already-finished Wizard end marker.

This checkpoint does **not** provide:

- another Action;
- another turn;
- Reaction refresh;
- recharge tick;
- death save;
- extra command;
- another regular duration marker.

It exists only to settle events whose source requires resolution from that attached command sequence.

### Kills during end processing

If an eligible killing blow happens during step 4 or 5, before the Auto-Raise checkpoint, it may reserve normally and resolve at step 6.

If a killing blow exists only **after the Auto-Raise checkpoint has closed**, such as from later administrative cleanup:

- it does not create an orphan reservation;
- it does not roll forward to next round;
- no Auto-Raise occurs from that kill.

If the owner's once/round Auto-Raise opportunity had not otherwise been used, it technically remains unused, but that expired trigger is gone. Only another independently valid trigger before an eligible still-open checkpoint could use it. The current bounded companion model normally supplies no second attached phase that round.

**NEW integration:** `attachedCompanionEnd` is therefore a queue checkpoint, not a new regular-turn clock.

---

## 2. Source owner, controller and stat provenance

Confirm. Store these separately.

At minimum:

- `sourceOwnerId`
- `currentControllerId`
- `sourceClass`
- `creationSourceId`
- creation-stat snapshots where applicable

### Source owner

The character whose class feature/spell created, bound or owns the creature.

Mage/Wizard references such as:

- Mage spell attack;
- Mage DC;
- Wizard spell attack;
- Wizard DC;
- source class level;

refer to the appropriate **source owner**, not whichever character may temporarily control the creature later.

Where a statistic was previously ruled creation-snapshot-based, snapshot the source owner's value at creation.

Where a source is dynamic, such as Mage elite current maximum HP, read the current value of that same source owner's class level.

A later controller does not silently substitute:

- their PB;
- their INT;
- their class level;
- their spell attack;
- their DC.

### Controller

Controls command issuance and relevant owner-wide action/command ledgers when an actual source grants control.

It does not rewrite stat provenance.

### Explicit exception

Flesh Ascendant remains the already-reviewed exception:

> its dynamic bonus follows the **current eligible controller**.

Conjuration remains tied to its original creating Wizard snapshot.

### Reflective Companion

The creature remains the original creature:

- original creature identity;
- HP;
- conditions;
- ongoing effects;
- attack/stat provenance.

The Mirrorsage is:

- current compulsion/controller source;
- BA-command payer;
- hard-denial source-character;
- owner of the applicable companion command/offensive ledgers for the forced order.

No unrestricted ownership-transfer or permanent rebinding API is created.

---

## 3. Reflective Companion future reservations

Confirm the proposed reservation model.

### At most one pending order

A controlled Reflective Companion can have at most **one pending forced Action order**.

A second attempted order while one is pending fails **before**:

- BA payment;
- RP or other costs;
- command-ledger mutation.

### When its Action is future-round

On valid issuance:

- spend the BA command in the **issuance round**;
- reserve the offensive-companion allowance in the **future numbered round in which its Action slot will resolve**;
- do not yet spend the Mirrorsage→target hard-denial allowance.

At the target's Action slot, revalidate:

- Charm/control still active;
- target still capable of taking the commanded Action;
- order remains legal;
- Mirrorsage→target hard-denial allowance still unused.

If valid:

- replace that creature's normal Action;
- spend the hard-denial allowance;
- consume the offensive reservation.

### Cancellation

If before execution:

- charm ends;
- target becomes incapable;
- control source ends;
- another feature from that Mirrorsage spends the same target's hard-denial allowance;

then:

- cancel the pending order;
- release the unused future offensive reservation;
- retain the already-spent BA/other issuance costs;
- do **not** spend the Reflective hard-denial allowance.

No fallback is invented.

### Ordinary attached companion command contrast

Ordinary attached companions commit:

- current-round BA command;
- current-round offensive allowance where applicable,

when the order is issued.

If execution later becomes impossible, those commitments are lost without refund.

That difference is necessary because Reflective Companion's action can resolve in a different numbered round.

### Mirror-origin Echo on extra turns

Mirrorsage has **no Mage/Wizard-style “regular turn only” command language** in the supplied source.

Therefore:

**NEW clarification:** Mirror-origin Echo may be used on an actual extra own turn if all of these genuinely exist and remain unused/legal:

- an Action;
- a Bonus Action;
- the owner-wide BA companion-command allowance for that numbered round;
- the Mirrorsage release cap for that numbered round;
- RP/record;
- target/origin legality.

An **extra full Action alone** is insufficient because it provides no Bonus Action.

Extra turns do not refresh:

- the companion-command cap;
- release cap;
- recharge;
- regular virtual markers.

The Echo still resolves immediately as the Mirrorsage's Action; there is no attached Beast phase for the release.

---

## 4. Ranger Beast damage and Wounds

Use the **HP-only bounded companion damage layer**.

Do not apply the player-character organic Wound/death-save subsystem to the bonded Beast from this source packet.

This is the cleanest source-faithful result because Beast Companion explicitly uses the **standard companion stats** with specific Beast modifications, while no supplied Beast source grants:

- Wound saves;
- Stable state;
- death saves;
- Critical-state healing ceiling;
- Hit Dice;
- a companion-specific injury table.

### Bonded Beast damage model

After legal defenses/temp HP:

- reduce ordinary HP;
- no newly generated Core Wound check;
- no death-save state;
- no Stable state;
- at `0 HP` apply the already-labeled **NEW Ranger-specific immediate death rule**.

This is not generic living-creature law.

### Existing state survives bonding

The profile conversion does **not** cleanse the real animal.

Preserve legally existing:

- conditions;
- disease;
- poison;
- source-explicit Injury/trauma;
- ongoing timed effects;
- relevant causal/provenance records.

If a future exact Ranger/companion source defines an Injury or Wound mechanic, that source can add it. This bounded interface does not invent one.

### Healing

“Heal normally” means the bonded Beast may receive legal ordinary HP restoration from effects that can target it.

It does **not** imply:

- Hit Dice;
- automatic short-rest healing;
- automatic long-rest healing;
- Wound recovery;
- resurrection rights.

Those remain future-source dependencies.

### Initial wounded conversion remains

Keep the prior **NEW profile-conversion rule**:

`newMax = max(1, 2 × Ranger level + actual WIS modifier)`

For a living Beast with previous current/max HP:

`newHP = max(1, floor(newMax × oldHP / oldMaxHP))`

Thus bonding a wounded living Beast preserves proportional injury rather than healing it to full.

This conversion itself:

- is not healing;
- causes no damage;
- creates no Wound roll;
- preserves conditions/injury provenance.

---

## Implementation status

These definitions complete the event-model ambiguities I see before coding the 100-source overlay:

- Auto-Raise has a non-turn attached-phase checkpoint with no orphan queues.
- Source owner and controller identities cannot overwrite one another.
- Reflective Companion has deterministic cross-round order reservation/cancellation.
- Ranger Beast uses a bounded HP-only companion damage model while preserving actual prior state.

The package remains **SOURCE-AUDITED / DRAFTABLE — implementation pending**, not yet reference-validated.
