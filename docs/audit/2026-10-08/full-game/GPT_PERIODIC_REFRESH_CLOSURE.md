Yes. Close both exactly that way.

### 1. Prolonged Suffering vs Persistent Bleed — your interpretation is correct

My earlier `1 → 2` and `3 → 3` Persistent examples were **without Prolonged Suffering**.

For any Bleed whose underlying profile has a **base duration of exactly 2 target turns**:

- without Prolonged Suffering, a qualifying Persistent Bleed refresh uses `max(currentRemaining, 2)`;
- with Prolonged Suffering, the source explicitly changes that eligible profile to **4 turns** and says subsequent refreshes set it to 4 rather than adding 4. Therefore use `max(currentRemaining, 4)`. Pasted text Pasted text

I would freeze the rule as:

> **NEW integration clarification:** Determine whether Prolonged Suffering applies from the Bleed profile's printed **base duration**, not its current remaining duration. For an eligible base-2-turn Bleed owned by that character, Prolonged Suffering changes its application and refresh duration to 4 target turns. A later qualifying refresh sets remaining duration to `max(currentRemaining, 4)`. Without Prolonged Suffering, Persistent Bleed uses `max(currentRemaining, 2)`.
>
> Duration modifiers are nonadditive unless explicitly stated otherwise.

And yes:

> A printed base duration is **not** a hard cap.

A hard cap exists only where the operative source actually expresses a maximum or otherwise expressly limits extension.

Examples:

- Thief Bloodleech base 2 + Prolonged → 4.
- Ranger owner-created base-2 Bleed + Prolonged in a legal multiclass build → 4.
- Dragoon owner-created base-2 Bleed + Prolonged → 4.
- Eligible record at 1 remaining + Persistent + Prolonged → 4.
- Eligible record at 3 remaining + Persistent + Prolonged → 4.
- Eligible record already at 4 → stays 4.
- Crimson base 3 → **not eligible for Prolonged**.
- Crimson Arterial Cut's express maximum of 5 is an actual hard cap for its own extension system; Prolonged never enters that calculation because the underlying profile is not base 2.

That distinction should be encoded separately as:

`baseDuration`  
`refreshDuration`  
`explicitHardCap`

rather than treating every original duration as a cap.

---

### 2. Generic extinguishing — agree: one Action clears all eligible attached fires

I agree with your proposed freeze.

> **NEW generic extinguish rule:** One Action by the affected creature or an adjacent helper ends **all active `family.ongoing-fire` records on that creature that are currently marked `ordinaryExtinguishable`**.
>
> Full immersion likewise ends all such ordinary-extinguishable attached-fire records.

This is preferable to one Action per namespaced fire. Otherwise three mechanically ordinary Burns from three different owners would artificially require three Actions solely because the registry preserved their source identities.

There is no compelling source or balance reason here to force one-record extinguishing.

Precedence should be:

1. Explicit source-specific prohibition or special extinguishing requirement.
2. Explicit source-specific cure procedure where it replaces the generic procedure.
3. Generic Action/full-immersion removal for remaining `ordinaryExtinguishable` records.

So, for example:

- ordinary Mage Burn + Dragoon Burn + Tinker Burn on one creature → one extinguish Action can end all three;
- a magical fire explicitly saying mundane extinguishing cannot end it survives;
- a source with a special removal prerequisite survives unless that prerequisite is satisfied.

### DEX saves

Also confirm your handling:

> End-turn DEX removal saves are resolved **per surviving eligible record**, using each record's own source DC/fallback and endpoint.

Because those records may have different:

- source DCs;
- remaining tick counts;
- cure exceptions;
- owners.

Passing one record's DEX save does not automatically count as passing another's unless an actual effect says it ends all ongoing fire.

And all of this remains independent from the **same-marker damage arbitration**: only the permitted damaging stack group ticks at a shared marker, but every surviving record retains its own duration and removal state.

**Both rules are settled.**