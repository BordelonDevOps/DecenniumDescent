# GPT final device source predicates

1. **Efficient Recycling — confirm correction.** My earlier enemy/hostile requirement was too broad. The exact source controls.

Efficient Recycling requires:

- your destroyed device;
- usable debris within reach;
- after combat, 1 minute;
- 1/short rest;
- destruction was **not deliberate sacrifice**;
- object was **not a copy**;
- refund ≤ `min(1 RP, actual RP paid to deploy that object)`;
- inherited `noResourceGeneration` blocks the RP refund.

Friendly or accidental destruction can therefore qualify. Enemy-caused destruction is **not** required. Scrap Salvage, Scrap Reaper, and Volatile retain their stricter predicates.

---

2. **First-destruction entitlement set — confirm the stronger NEW rule.**

For one `deploymentInstanceId`, its **first actual destruction** establishes the only destruction/debris opportunity set for that deployment.

At that first destruction:

- capture cause/provenance/flags;
- evaluate each destruction-linked feature against that event;
- qualifying opportunities may be used or declined;
- nonqualifying opportunities are closed for that deployment;
- create at most one usable debris record.

So:

> friendly destruction → Snap Rebuild → later enemy destruction

does **not** manufacture a fresh Volatile/Scrap/Recycle/debris opportunity set.

The later enemy hit can physically destroy the rebuilt object again, but it does not create a second harvestable destruction history.

This is the approved **NEW anti-loop integration** supported by Snap's “does not reset ... destruction triggers.”

The original first-event debris may remain after the device's original duration expires if a salvage source still permits using debris. Expiry only kills **Snap eligibility**.

Snap Rebuild consumes/reconstitutes that destroyed object from its available destruction set, so the same debris is no longer separately available for Recycling/Salvage/Reaper afterward.

A genuinely new paid deployment or explicit long-rest Drone rebuild gets a new `deploymentInstanceId` and therefore a new future first-destruction event.

---

3. **Destroyed + disabled and the two 10-minute procedures**

Keep them separate.

### Protected-disable tools procedure

The engine[7] procedure:

> 10 minutes + 1 RP using tinker's tools

may clear the protected-disable flag even if the persistent machine is currently destroyed, because disablement is orthogonal and the flag can be cleared independently.

It does **not** restore HP or revive the object.

### Destroyed Drone repair

Engine[2]:

> 10 minutes + 1 RP → destroyed Drone returns at half HP, once/short rest

is a separate permission.

It restores the Drone but does **not** automatically clear protected disablement.

Therefore a destroyed-and-disabled Drone can require both procedures.

**Do not combine them into one 10-minute/1RP operation merely because their costs and duration happen to match.** There is no supplied source saying one procedure satisfies both rights.

Field Repair remains:

- unable to revive a destroyed target;
- able to clear protected disablement on an otherwise legal Field Repair target.

Snap likewise restores HP but preserves the disable flag.

---

4. **Long-rest Drone rebuild — confirm persistent disable flag**

Confirm.

A long-rest Drone rebuild:

- restores the owned Drone to full HP;
- creates a fresh `deploymentInstanceId`;
- resets the old physical deployment/destruction/debris history as appropriate for that new rebuild;
- does **not** silently clear `protectedDisabled`.

Keep protected disablement associated with the persistent Drone **asset**, not merely the discarded deployment instance.

Engine[7] expressly supplies automatic clearance at:

> next completed **short rest**

and separately by its repair procedures.

Do not infer that a long rest counts as that short-rest marker.

So a Drone can emerge from its long-rest rebuild:

- full HP;
- new deployment history;
- still protected-disabled,

until Field Repair, the separate 10-minute tools disable-clear, or an actual completed short rest clears that flag.

These four corrections leave the lifecycle package internally consistent and keep source predicates separate from the NEW anti-loop integration.
