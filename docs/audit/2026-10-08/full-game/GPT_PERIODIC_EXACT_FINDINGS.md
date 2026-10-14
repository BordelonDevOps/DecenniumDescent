I found **two material implementation blockers and two bounded cleanup items**. I do not see a source-text mutation or a broader periodic-design contradiction beyond these. The unified arbitration/cure model itself is coherent. Pasted text

### Material blocker 1: explicitly forbid custom + Core fallback double-instantiation

The package says there is no separate generic damage layer, but the registry still contains both `core.bleeding`/`core.burning` and source-qualified custom records. That leaves one dangerous implementation ambiguity: a card saying “Bleed” could be interpreted as creating its custom binding **and** Core Bleeding because both share the family.

Add this registry invariant:

> **NEW — exclusive periodic binding:** When an application has a reviewed source-qualified periodic profile, create **only that source-qualified record**. Do not additionally create `core.bleeding` or `core.burning` merely because the effect is called Bleed, Bleeding, Burn, Burning, ignite, or carries the family tag.
>
> `core.bleeding` and `core.burning` are fallback mechanical identities only for applications that explicitly invoke the Core condition and have no more-specific reviewed periodic profile.
>
> A source creates both only if its operative text explicitly imposes two separate effects.

This is necessary to guarantee “no additional generic tick” at the **record-creation** layer, not merely at arbitration. The current Core entries correctly participate in the unified family once legitimately instantiated. Pasted text

### Material blocker 2: distinguish condition immunity from damage-type immunity during arbitration

The package correctly says expected damage is chosen before resistance/immunity and that damage immunity must not erase an otherwise active condition. But it does not yet explicitly say whether an effect suppressed by **condition/family immunity** is allowed to compete for the family winner.

Freeze this:

> **NEW — immunity/arbitration distinction:**  
> A record prevented by condition/family immunity is not created.  
> If condition/family immunity is gained after application, the existing record is suppressed while that immunity lasts. Its duration and scheduled ticks continue to advance, but a suppressed record is **excluded from damaging-group arbitration** and deals no periodic damage. Any due tick is still consumed on schedule.
>
> Damage-type resistance or immunity is different: it does **not** suppress the Bleed/Burn record and does not remove that group from arbitration. Determine the winning group using expected unmitigated damage; afterward apply the target's actual resistance/immunity to the winning damage event, potentially reducing it to zero.

That matches the already-closed generic immunity rule—clocks continue during suppression—while preventing a condition-immune record from starving a legal active group. It also preserves your explicit requirement that fire/slashing/etc. immunity alone not cause the condition to disappear.

### Seal Minor Wound / Bloodleech / Blood Curse — the current cure decision is correct

`Seal Minor Wound` explicitly has an “end one ordinary Bleed/minor ongoing bleeding effect” mode while separately prohibiting removal of poison, curse, Wound, disease, etc. Those clauses are not contradictory: the spell can remove an eligible **Bleed component** even when that Bleed originated from something that is otherwise a poison recipe or magical curse. Pasted text

For `thief.bloodleech.bleed`, ending the Bleed record does **not** purge other poisons or grant poison immunity. But add one state-cleanup rule:

> If the Bloodleech Bleed record is the only remaining ongoing component of that Bloodleech recipe instance, ending that record also ends that recipe's **ongoing-instance occupancy** for the Thief two-recipe cap. Do not leave an empty “ghost” recipe consuming a slot.

The critical-hit heal is a one-time resolved consequence and does not keep the recipe instance active. The Bloodleech definition already treats the Bleed as the ongoing recipe state. Pasted text

For `shaman.blood-curse.bleed`:

- magical healing invokes its printed CON save rather than auto-ending it;
- `Seal Minor Wound` may directly remove that ordinary-removable Bleed record because `ordinaryConditionRemoval` is true;
- doing so does **not** remove some independently existing curse state;
- equally, the display name **Blood Curse does not itself create a separate `classification.curse` record**. Only an explicit binding/source may do that.

That last point prevents a ghost “curse” from surviving solely because the ability's name contains *Curse*. Pasted text

### Cleanup: Ashblood contains stale arbitration boilerplate

`thief.ashblood.periodic` is intentionally outside both periodic families, yet its `ending` says “Losing arbitration consumes a due tick,” and its generic stacking language also references source-group arbitration. That record cannot participate in the Bleed/fire family arbitration as currently classified.

Change it to:

> `ending`: “After two due ticks, or if an explicitly reviewed poison-effect removal ends the remaining recipe rider.”
>
> `stacking`: “One Ashblood recipe instance per owner/target; reapplication refreshes under the Thief poison-engine rules. It does not participate in Bleeding or ongoing-fire family arbitration.”

Its actual substantive immunity/cure decisions are otherwise correct. Pasted text

### Cleanup: give fire explicit-removal scope metadata

The Bleed definitions consistently contain:

> `explicitRemoval: Use remover exact one/all/owner restrictions.`

The fire definitions generally have only `ordinaryConditionRemoval: true`.

For schema symmetry and to prevent a later `end one Burn` effect from accidentally clearing all fires through the generic extinguish rule, add to every ongoing-fire cure object:

> `explicitRemoval: "Use remover's exact one/all/owner restrictions; explicit condition removal is distinct from the generic Action/full-immersion extinguish endpoint."`

This does not change any current fire result; it closes a future interpretation hole.

### Everything else passes this pass

I found no contradiction in the implemented:

- same-marker highest-expected-damage/earliest arbitration;
- Crimson two-instance Blood Echo exception and +1 due-tick valuation;
- different timing markers resolving independently;
- Mage Fire Focus/Inferno/Bolt shared group and Elemental Mastery extensions;
- Fusion/Cascade separation;
- one-record Medicine versus all-eligible magical-healing Bleed cure;
- Blood Curse healing-triggered save;
- family-wide mundane fire extinguishing with per-record DEX saves;
- Ashblood exclusion from ongoing fire;
- Prolonged Suffering base-2 → 4 logic and Persistent refresh interaction;
- Vein Cutter's two Bleed ticks versus one-turn secondary riders;
- Bloodroot slashing fallback;
- Wyrmhide's CON-save-only scope;
- Mythic Carapace's condition-family immunity without fire-damage immunity;
- Hemostasis's broad `end all Bleed` behavior;
- owner versus technical Crimson-engine hook separation. Pasted text

**Disposition:** implement the **two material rules** above, plus the Ashblood/explicit-fire-removal cleanup, and I would close this **bounded periodic-family package as REVIEWED/reference-VALIDATED** at its stated scope.

**DD16 remains open**, correctly, for the remaining root/slow/curse/disease/mark bindings and exhaustive active-rider semantic review.