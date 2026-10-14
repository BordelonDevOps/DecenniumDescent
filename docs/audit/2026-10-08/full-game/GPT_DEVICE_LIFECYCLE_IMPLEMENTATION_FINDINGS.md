# GPT exact device lifecycle implementation findings

I find **three concrete defects before bounded closure**. The rest of the submitted lifecycle model is consistent with our source conference and the 74+3 scope.

## 1. Named standard elemental AC is wrong

This is the clearest source mismatch.

The frozen standard-companion paragraph says:

> **AC 12 + floor(PB/2)**

The four Shaman summon cards call their creatures **standard** Ice Wisp/Airling/Cinderflame/Stonekin and do not print a replacement AC.

Current helper:

```python
if kind=='elemental':
    return {'hp':(3 if harmony else 2)*level,'ac':12+pb}
```

and the guide both use `12+PB`.

That improperly gives them the Chorus/Totem AC formula.

### Correct

Named standard elementals:

- HP = `2L`
- Harmony HP = `3L`
- **AC = `12 + floor(PB/2)`**
- other standard-companion statistics remain from the frozen paragraph except where the individual summon explicitly overrides them.

Elemental Chorus stays:

- HP `4L`, Harmony `5L`
- **AC `12+PB`**

because Chorus explicitly prints that AC.

Smallest counterexample:

> PB4 Ice Wisp → source AC14, current helper AC16.

This needs a helper, guide, and regression-test correction.

---

# 2. Scraplings are silently being promoted to generic “devices”

Current:

```python
MACHINE_KINDS=frozenset({'drone','device','salvage','reaper'})
```

This creates permissions the supplied sources do not establish.

It makes both Scrapling types automatically eligible for things such as:

- Field Repair;
- protected Dissonance routing;
- Efficient Recycling;
- Volatile Components;
- any generic machine/device predicate using `MACHINE_KINDS`.

The exact Scrapling sources do **not** say they are constructs or devices.

What they do say is narrower:

- engine[1] explicitly groups Scraplings with drones/turrets for **shared command/damaging-action economy**;
- Scrap Salvage explicitly says its Scrapling **counts as a deployable slot/shared command**;
- Scrap Reaper explicitly creates a Scrapling using the command budget but does **not** assign a slot;
- neither source grants generic machine/device targeting.

“Counts as a deployable slot” is not equivalent to “is a device for every Tinker feature.”

### Correct bounded model

Separate their lifecycle category from generic machines, e.g.:

```text
MACHINE_KINDS = drone, device
SCRAPLING_KINDS = salvage, reaper
```

Scraplings still:

- have their printed HP/AC/Speed;
- disappear/end at 0 as their temporary companion entity;
- use the shared command/damage budget;
- release any printed slot;
- obey their no-replacement/no-chain restrictions.

But under the **currently supplied sources**, do not automatically grant Scraplings:

- Field Repair;
- Repair Pulse;
- Dissonance routing;
- Efficient Recycling;
- Volatile Components;
- Snap Rebuild;
- generic device-only effects.

If we later want “Scraplings count as mechanical devices,” that needs to be an explicitly labeled **NEW integration decision** or an additional source. It should not arise from an internal Python kind name.

### Consequence for question 6

With the supplied text alone, a Salvage Scrapling's later enemy destruction does **not** presently qualify Volatile Components or Efficient Recycling, because neither source establishes that the Scrapling is a “device.”

That is the safest provenance-faithful result.

---

# 3. `noDeathTriggers` must block Scrap Reaper

Your question 5 exposes a real omission.

Current `salvage(... reaper=True ...)` tests:

- hostile destruction;
- first destruction;
- enemy hit;
- sacrifice/copy/friendly/secondary;
- no-self-replacement.

It does **not** inspect inherited `noDeathTriggers`.

Scrap Reaper is explicitly:

> **Reaction** using “one destroyed enemy-hit device”

It is therefore a destruction-triggered response.

If the damage branch that destroyed the device carries `noDeathTriggers`, Reaper cannot use that destruction as its trigger.

### Required

For Reaper:

```text
if 'noDeathTriggers' in destruction.flags:
    reject
```

This does **not** automatically prohibit later Scrap Salvage.

Scrap Salvage is:

- an Action;
- operating on existing enemy-destroyed debris;
- not itself a triggered response to the death event.

So the distinction should be:

| Flag | Volatile | Cinder burst | Scrap Reaper | Later Scrap Salvage | Recycling |
|---|---:|---:|---:|---:|---:|
| `noDeathTriggers` | blocked | blocked | **blocked** | not automatically blocked | not automatically blocked |
| `noRetaliation` | blocked | where applicable | not automatically | no | no |
| `noResourceGeneration` | no resource generation | source-specific | no | no | **refund blocked** |

Do not widen `noResourceGeneration` to non-resource material transformations.

---

# Specific requested confirmations

### Magnetic Wall → Scrap Reaper

Current consequence is correct.

Magnetic Wall interception:

- preserves genuine enemy cause;
- does **not** give the Wall attack-hit identity.

Therefore Wall destruction from transferred enemy damage may satisfy:

- Volatile Components, assuming other predicates;
- Scrap Salvage's **enemy-destroyed** predicate.

It does **not** satisfy Scrap Reaper:

> “destroyed **enemy-hit** device”

because the Wall was not hit by the attack. It received a transferred damage branch.

No override should be added.

### Decoy damaging trigger

Current command interpretation is correct.

The engine[6] Decoy destruction burst:

- may occur off-turn;
- spends the owner's numbered-round **damaging companion/device allowance**;
- spends no BA because it is an automatic profile trigger;
- if that damage allowance is already gone, Decoy's damage is suppressed/lost rather than banked.

The engine[6] restriction does not absorb separately printed:

- Volatile Components;
- Cinderflame's destruction burst.

Those use their own frequencies and source predicates.

Gadget Sync still requires its actual bomb-trigger/once-own-turn legality from the caller.

### Reaper own-death chain

Independent of the broader Scrapling-type defect, the Reaper text:

> “No chain from deliberate sacrifice or its own death.”

must remain a hard provenance property.

So even if a future explicit rule eventually classifies a Reaper Scrapling as a device, its own destruction must not become a new Volatile/Recycling/Salvage/Reaper chain unless some later source explicitly overrides that prohibition.

I recommend storing an entity/source property such as:

`noOwnDestructionChain=True`

rather than relying only on `no_replacement`, because “no chain” is broader than “cannot create another Scrapling.”

---

# Long-rest Drone rebuild

The current treatment is correct for this 74-source packet.

A fresh long-rest Drone incarnation:

- full current maximum HP;
- zero temp HP;
- fresh destruction/material identity;
- keeps persistent asset identity;
- keeps persistent protected-disable state;
- keeps current module configuration subject to the actual long-rest configuration procedure.

`new.effects={}` is acceptable here **because every timed effect supplied in this packet would have expired during the completed long rest anyway**.

That should be documented as clock expiration, not as:

> “long-rest rebuild cleanses all effects.”

If a future effect explicitly survives a long rest or is permanent, its source would control and should not be erased merely by reconstruction.

Canonical per-rest use refresh remains a separate rest-system operation, as currently stated.

---

# First-destruction/material model

I find this correctly implemented.

For one deployment instance:

- first actual destruction establishes its sole destruction/material opportunity set;
- first-event provenance remains authoritative;
- Snap consumes that physical material;
- reconstruction does not create another first-event set;
- second physical destruction can end the object again but generates no new material/Volatile opportunity;
- actual new paid deployment or explicit LR Drone incarnation creates a new instance.

Efficient Recycling is also now correct:

- enemy cause not required;
- friendly/accidental destruction can qualify;
- deliberate sacrifice/copy excluded;
- `noResourceGeneration` blocks refund;
- refund ≤ actual paid deployment RP;
- expired timer does not erase already-existing debris, though it kills Snap eligibility.

---

# Other reviewed areas

I find no blocker in the submitted implementation for:

- orthogonal protected-disable state;
- short-rest versus LR disable behavior;
- separate ten-minute Drone reconstruction and ten-minute disable-clear;
- Snap preserving disablement;
- original slot footprint reacquisition;
- atomic Totem replacement;
- dependent Echo ending;
- Echo ordinary Totem HP/AC;
- Echo half numerical aura values only;
- Chorus as one package at 4L/5L;
- persistent Drone current actual INT/level/PB behavior;
- creation-snapshot deployable/Totem statistics;
- NEW max1 machine reconstruction minimum;
- Repair Pulse max1 = 0;
- NEW reconfiguration fraction;
- Restoration Field as slot effect without fabricated machine anchor;
- direct-HP Volatile Injection;
- Magnetic Wall post-defense transfer and flags;
- no second Wall mitigation;
- hostile attribution through Wall interception;
- Emergency Protocols `noRetaliation`;
- Advanced Turret Bay capacity behavior;
- Gadget Sync command/damage arbitration;
- Dual Drone configuration;
- expiry/replacement/concentration creating no destruction rewards.

## Disposition

Keep the package:

> **IMPLEMENTED CANDIDATE / exact review not yet closed**

until these three corrections are made and regression-tested:

1. standard elemental AC → `12 + floor(PB/2)`;
2. remove Salvage/Reaper Scraplings from silent generic machine/device eligibility unless explicitly adopted as a NEW rule;
3. make inherited `noDeathTriggers` reject Scrap Reaper's destruction-triggered Reaction.

After those corrections, I do not presently see another blocker to **REVIEWED / reference-VALIDATED** disposition for the supplied **74 lifecycle/command roles + 3 frozen shared paragraphs only**. The other 157 lifecycle candidates, whole-card behavior, broader companions, items/spells, and whole-game runtime remain open.
