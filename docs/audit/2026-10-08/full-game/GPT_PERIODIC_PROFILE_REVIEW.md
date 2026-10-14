1. **Generic Bleed cure metadata — ACCEPT, with one DC precedence clarification.**

The overlay is reasonable as an explicit **NEW** gap-fill rather than something inherited merely from `family.bleeding`.

Use this order for the generic Medicine endpoint:

> **NEW:** An ordinary hostile Bleed without a complete cure procedure may be treated with an Action by the affected creature or an adjacent helper using WIS (Medicine). Use the Bleed application's expressly printed cure DC first; otherwise its recorded applying effect/class/spell DC when one exists; otherwise use DC 10.

This avoids manufacturing a “class DC” for a source that does not actually have one.

For multiple independent records on one target:

- **Medicine Action:** select **one** eligible Bleed record before rolling; success ends that record only.
- **One legal magical-healing event with positive pre-cap/pre-prohibition healing potential:** every active ordinary Bleed record whose cure metadata says `magicalHealing: automaticEnd` ends from that one event.
- **Shaman Blood Curse:** each active Blood Curse record independently receives its printed immediate CON save instead of automatic removal.
- An explicit `end one Bleed` removes one eligible selected record.
- An explicit `end all Bleed` removes all records within its actual stated scope.

Crimson and Dragoon may retain their printed healer's-kit Actions as additional automatic endpoints. **NEW:** each such use consumes one healer's-kit use.

For Crimson, one such Action ends all Crimson Bleed instances belonging to that source owner on that victim. For Dragoon, it ends the active Dragoon Bleed record. Pasted text

No current class Bleed becomes `specialCureRequired` or artifact-level merely because its origin is magical.

---

2. **Attached ongoing fire extinguishing — QUALIFIED ACCEPT**

Yes, explicitly registered creature-attached magical Burn-style fire may use the ordinary extinguishing overlay **unless its source says otherwise**. Magical origin by itself is not enough to make fire unextinguishable.

Use:

> **NEW:** A registered `family.ongoing-fire` record marked `ordinaryExtinguishable` may be ended by an Action from the affected creature or adjacent helper, or by full immersion of all burning portions. A source explicitly stating that mundane extinguishing does not work overrides only those mundane endpoints.

The generic DEX endpoint is also acceptable, but add this timing limitation:

> At the end of each regular target turn, if the ongoing-fire record is **still active and has at least one future scheduled tick remaining**, make its generic ending DEX save against its source DC, or DC 10 if none exists. Success ends that record.
>
> A record whose final scheduled tick has already resolved simply expires and does not make a pointless ending save.

Thus a two-start-turn Burn can be extinguished by a save after its first tick; a one-start-turn Burn ends after that sole tick before an end-turn save would matter.

No generic fire damage is added.

### Listed fire bindings

These should be explicitly registered:

- `cleric.flame.burn` — ongoing-fire, its own 2-turn source group. Pasted text
- `cleric.divine-invocation.flame-dot` — ongoing-fire, **separate group** from base Flame because the source does not say it refreshes/applies the base Flame state. Pasted text
- `mage.elemental-bolt.fire` — separate application ID in the **Mage Fire Focus stack group**. Pasted text
- `mage.elemental-fusion.fire-cold-dot` — own group. Pasted text
- `mage.cascade-storm.fire-dot` — own group. Pasted text
- `wizard.combo-surge.fire-cold-dot` — own group. Pasted text

### Elemental Mastery — one correction

The proposed restriction to only the Focus passive/Inferno plus explicit Focus-Burn references is **too narrow**.

The source says:

> “Fire Burns from your **Focus cards** last one additional turn...” Pasted text

`mage.base.elemental-bolt` is explicitly tagged `focus`, so its Fire rider qualifies.

Therefore bind Elemental Mastery to:

> any active Mage card actually tagged `focus` whose reviewed Fire rider is classified as a Burn, plus cards expressly saying they apply the Focus Burn.

That includes Elemental Bolt Fire. It does **not** include Elemental Fusion or Cascade Storm from this packet because neither is tagged `focus`, even though they use elemental damage.

---

3. **Ashblood / Purifying Crown — MOSTLY ACCEPT; poison immunity proposal needs correction**

Ashblood's delayed `1 fire at start next 2 turns` should remain:

`thief.ashblood.delayed-fire`

It is:

- part of the Ashblood poison recipe;
- not named Burn;
- not `family.ongoing-fire`;
- not subject to ordinary extinguishing;
- not the Core Poisoned condition.

So it may coexist with an actual Burn-family record at the same marker.

However, I would **not** make generic Core Poisoned immunity block the entire poison recipe. The available rules distinguish poison damage and the **Poisoned condition** as separate things.

Use:

- explicit **poison-damage immunity** → prevents Ashblood's poison damage as applicable;
- explicit **Poisoned-condition immunity** → blocks only a rider actually imposing Core Poisoned, such as Venombite;
- an effect explicitly saying immunity to **poisons/poison effects/toxins** may block the recipe itself if its wording covers that application.

The Thief engine still requires its relevant failed CON save; do not invent automatic success merely from Poisoned-condition immunity. Pasted text

Generic `end Poisoned` likewise does **not** remove Ashblood's delayed fire.

A cure explicitly neutralizing/removing the underlying poison recipe may remove its remaining recipe riders if the cure's reviewed scope covers active poison effects.

**Purifying Crown:** agree. Its repeated fire+radiant damage is an aura-bound divine damage procedure, not a creature-attached Burn. Exclude it from `family.ongoing-fire`. Pasted text

---

4. **Vein Cutter and Thief Bleed extensions — ACCEPT WITH TWO CORRECTIONS**

### Vein Cutter

The effect text specifically says:

`Bleed 1d4 next 2 turns`

while its general duration field says until end next target turn. The effect is more specific for the Bleed component.

Bind:

- Bleed: two target regular-turn ticks;
- Speed -10: until end next target regular turn;
- `-1 next attack damage`: consumed by the next qualifying attack, or expires at end next target regular turn;
- the consumed poison does **not** create a normal poison-recipe instance because the card expressly replaces its normal recipe effect. Pasted text

That is a source reconciliation; no reason to compress the Bleed to one tick.

### Prolonged Suffering

Your ownership interpretation is correct.

It says **your Bleed application**, not “your Thief Bleed,” so in a future legal multiclass build it can modify another class's Bleed owned by that character **only when that Bleed's base duration is exactly 2 target turns**.

Therefore examples include qualifying owner-created:

- Dragoon 2-turn Bleed;
- Ranger 2-turn Bleed;
- Thief 2-turn Bleed;
- relevant Warrior 2-turn Bleeds.

It does **not** apply to Crimson's base 3-turn Bleed or Shaman Blood Curse's 3-turn Bleed. Pasted text

So an “Arterial 5 vs Prolonged 4” conflict should never arise: Crimson's base duration is not 2, so Prolonged Suffering does not modify it.

### Persistent Bleed

Use:

> On its actual qualifying trigger, set the selected owned Bleed's remaining duration to `max(currentRemaining, 2 target turns)`, without changing dice, instance count, or exceeding that Bleed's true source hard cap.

It must never shorten a currently longer Bleed.

It does not restore a record merely because it is “about to expire”; its own qualifying weapon-hit trigger must actually occur. Pasted text

### Extension precedence

Use this general rule:

> **NEW:** duration replacements/extensions are nonadditive unless a source explicitly says otherwise. Determine the duration supplied by each applicable modifier, use the greatest legal resulting duration, and clamp to the underlying record's true hard cap. A refresh never shortens current remaining duration.

Examples:

- ordinary Thief base 2 + Prolonged → 4;
- later qualifying Persistent refresh while 3 remain → remains 3, not reduced to 2;
- later qualifying Persistent while 1 remains → becomes 2;
- Crimson Arterial may reach its own printed maximum 5 through its own engine; Prolonged does not apply.

---

5. **Bloodroot / Tyrant's Impale / clocks — ACCEPT**

### Bloodroot Trail Bleed type

Keep the already agreed fallback.

Bloodroot's initial zone packet is explicitly **necrotic**, but the follow-up merely says `Bleed 1d4 next turn`; it does not say the Bleed itself is necrotic. Pasted text

There is no applying physical hit from which to inherit bludgeoning/piercing/slashing.

Therefore:

> `shaman.bloodroot-trail.bleed` uses the ordinary fallback **slashing** damage.

Do not infer necrotic merely from the preceding zone damage. This is exactly why Shaman Blood Curse, which explicitly prints necrotic Bleed, remains different.

### Tyrant's Impale

Bind its word **Bleeding** to the existing Dragoon Bleed engine profile:

- `1d4 physical`
- start of next 2 target regular turns
- Dragoon cure metadata.

The **pin/Restrained** state remains independent and ends according to its own end-of-next-turn/reach/escape rules. Ending the pin does not automatically erase the Bleed, and curing the Bleed does not free the pin. Pasted text

### Periodic clocks

Confirm:

> Every class periodic Bleed/Burn clock whose source is expressed in target turns advances only on the target's **regular turns**. Extra turns neither tick nor consume its duration.

Outside initiative:

> preserve the existing periodic clock and resolve one due periodic step per complete 6 elapsed seconds. Entering or leaving initiative never duplicates an already consumed six-second interval or scheduled tick.

No record may receive both its explicit replacement tick and a generic family tick.

## Disposition

All five bridges are implementable with the corrections above.

The two material corrections are:

1. **Elemental Mastery must include Elemental Bolt Fire because Elemental Bolt is actually tagged `focus`;** do not hard-code the upgrade only to the base passive/Inferno.
2. **Core Poisoned immunity must not be treated as blanket immunity to every Thief poison recipe.** Keep poison damage, Poisoned-condition immunity, and explicit poison-effect immunity as separate scopes.

Everything else can proceed into the provisional binding overlay without altering the original cards.