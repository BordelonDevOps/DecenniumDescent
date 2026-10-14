# GPT further device lifecycle findings

Not a closure: two blockers and a provenance correction remain in this reviewed version.

The three previously identified defects are corrected correctly. I found **two concrete implementation blockers and one provenance-hardening issue** before I would mark the 74+3 package closed.

## 1. Dual Drone Protocols does not enforce the printed module count

`tinker.engine[2]` is exact:

> at 13 choose either **2 basic drones each with one module**, or **one drone with 2 distinct modules**.

Current `configure_drones()` only enforces a maximum:

```python
len(mods) > (1 if mode=='dual' or level<13 else 2)
```

So at level 13 these illegal configurations currently pass:

```text
dual:
Drone A = 0 modules
Drone B = 0 modules
```

and:

```text
single:
Drone A = 1 module
```

The source requires **exactly** one per Drone in dual mode and **exactly two distinct** modules in single mode at 13+.

### Required correction

For the Dual Drone Protocol choice:

```text
if level >= 13 and mode == dual:
    exactly 2 assets
    exactly 1 module on each

if level >= 13 and mode == single:
    exactly 1 asset
    exactly 2 distinct modules
```

The pre-13 module acquisition gate can remain caller-owned as stated, but once this helper claims to execute the level-13 configuration it needs exact cardinality.

Add tests for:

- dual with 0-module Drone → reject;
- dual with one empty / one populated → reject;
- single at13 with one module → reject;
- single at13 with exactly two distinct → pass.

This is a closure blocker.

---

## 2. Field Repair incorrectly requires the Drone to be deployed

This comes from reusing `machine_target()`:

```python
return self.kind in MACHINE_KINDS and self.active(now) ...
```

and `active()` means `state == 'deployed'`.

But the exact Field Repair source says:

> “One construct/device **touched**”

and the Drone source explicitly allows the Drone to be carried/retracted. We already established that retraction preserves the persistent machine, its HP, modules and disablement; it only removes it from active battlefield operation.

There is no source saying a carried/retracted positive-HP Drone becomes unrepairable.

Smallest counterexample:

> Drone is retracted, HP 5/20, Tinker is touching it, pays Action+1RP.  
> Exact Field Repair permits repairing the damaged machine. Current helper rejects it because it is not `deployed`.

The same applies to a retracted protected-disabled Drone at full HP: touching it with Field Repair should be able to clear the protected disable flag.

### Required correction

Do not use the **active battlefield device** predicate for Field Repair.

Use a narrower repair predicate such as:

```text
machine kind
positive HP
not expired/replaced/superseded
and:
    deployed device, or
    deployed/retracted available Drone
```

Then retain:

- destroyed → illegal;
- expired/replaced → illegal;
- Scrapling/Totem/Field → illegal.

Dissonance routing should continue to require an **active deployed** device. This correction is specifically about Field Repair's touched-machine permission.

I would not automatically broaden Repair Pulse in this pass; its “functional friendly devices within 30 ft” wording is less explicit about carried/retracted entities. Field Repair's touch wording is enough to resolve this one.

---

## Provenance hardening: distinguish copied object from copied incoming damage

I strongly recommend fixing this before status promotion, although it can be done as a naming/data-model correction rather than a new rule.

Current destruction record has:

```python
copied: bool
```

and `hostile_qualifies()` rejects it.

But the supplied source distinction is important:

- Volatile Components explicitly excludes **“copied objects.”**
- The frozen copy rule says a damage copy still causes **ordinary damage consequences and death**.

Therefore these are different:

### A copied object is destroyed

This can legitimately carry the source's copied-object exclusion.

### A real device is destroyed by copied damage

The fact that the incoming damage was a numeric copy does **not**, by itself, erase ordinary destruction consequences. The copy's own inherited flags may suppress triggers, but “damage was copied” is not the same thing as “destroyed device was a copied object.”

Because `resolve_entity_branch(... copied=False)` accepts this boolean at damage resolution, the present name makes it dangerously easy for a future engine caller to pass incoming-copy provenance and incorrectly suppress Volatile/Recycling/etc.

For tabletop this distinction is manageable; for a video-game implementation it should be explicit.

### Recommended model

Rename/store:

```text
entityIsCopy
```

or:

```text
copiedObject
```

on the entity/destruction provenance.

If desired, separately retain:

```text
incomingDamageWasCopy
```

for source-event history.

Only the former should satisfy these copied-object exclusions unless another source flag says otherwise.

A useful regression:

> real device destroyed by copied hostile damage, with no `noDeathTriggers`/`noDamageTriggers` restriction → ordinary destruction record remains eligible under its own target-side features.

This does not invent a mechanic; it preserves the frozen copy paragraph.

---

# Everything else from the previous review now checks out

The following are correctly corrected or retained:

- named Shaman standard elementals use `12 + floor(PB/2)`;
- Chorus remains `12+PB`;
- Harmony remains 3L / 5L;
- Scraplings are not silently promoted to machine/device status;
- Salvage Scrapling slot use does not grant device repair/recycling rights;
- Reaper has no invented deployable-slot requirement;
- Reaper's explicit own-death no-chain provenance persists;
- `noDeathTriggers` blocks Reaper before Reaction/RP/material mutation;
- later Action-based Scrap Salvage remains possible despite `noDeathTriggers`/`noResourceGeneration`, subject to its own predicate;
- `noResourceGeneration` remains specific to resource generation such as Recycling;
- Magnetic Wall transfer is enemy-caused but not an enemy attack hit on the Wall;
- therefore Magnetic Wall can qualify Volatile/ordinary hostile-destruction material but not Reaper's enemy-hit predicate;
- Emergency Protocols retains `noRetaliation`;
- first-destruction material/opportunity anti-loop behavior is preserved;
- Snap cannot manufacture a second destruction entitlement;
- long-rest Drone rebuild creates a fresh incarnation but retains asset disablement;
- the two ten-minute procedures remain separate;
- max-1 reconstruction and Repair Pulse zero result remain coherent;
- reconfiguration arithmetic and 1,200 tested states are coherent;
- Restoration Field remains a slot effect rather than an invented machine;
- parent/Echo dependency, replacement and concentration endings remain coherent;
- support/Gadget Sync/damaging-action separation remains coherent;
- Decoy consumes the engine[6] damaging allowance without consuming a BA;
- Cinder/Volatile remain outside that command allowance;
- ordinary expiry/replacement/concentration end creates no destruction rewards;
- long-rest clearing of packet-supplied timed effects is correctly documented as natural expiry, not generic cleansing.

## Disposition

With the code exactly as submitted, I would keep it:

> **IMPLEMENTED CANDIDATE / exact review pending**

for the two blockers above.

After:

1. enforcing the exact Dual Drone module cardinalities; and
2. allowing Field Repair on an otherwise legal retracted positive-HP Drone,

I see no remaining rules blocker in the supplied lifecycle model. I also recommend making the copied-object provenance distinction at the same time so the later video-game runtime cannot misinterpret the frozen copy rule.

Once those are corrected and regression-tested, the appropriate bounded status is:

> **REVIEWED / reference-VALIDATED — 74 supplied Tinker/Shaman lifecycle/command roles + 3 frozen shared-rule paragraphs, including the separately bound Magnetic Wall integration.**

That status still does **not** close the remaining 157 lifecycle candidates, the prepared 100 creature/companion/form/temp-HP sources, whole-card functionality, all companion systems, movement/collision, general targeting, items/spells, balance, or the complete tabletop/video-game runtime.
