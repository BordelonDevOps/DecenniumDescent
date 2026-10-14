**Closure count: 12/12 findings verified closed.** The revised fields implement every specific correction from the prior conference: ranges/targets for Shield, Predict Movement, Resonance Shield and False Life; Locate Object's casting-vs-detection radius; 24-hour Conjure Water limit; Unseen Servant location/reach; Message wording; Mental Flicker eligibility; Skeleton damage typing; long-rest Refrain reset; and both malformed target strings. Pasted text Pasted text

One minor documentation cleanup, not a reopened defect: **False Life's `designNotes` still contains the obsolete sentence saying operational range is Self**, followed immediately by the conference decision restoring 30 feet. Delete the stale sentence so the note does not contradict the actual card. Pasted text

## Falling interface — proposed joint decision

I agree that we should **not change Feather Fall to a Reaction**. Both preserved placements say Action, and the current sources inspected do not provide an executable falling clock or impact formula. Pasted text

I recommend this minimal rule, explicitly labeled **NEW PROVISIONAL PLAYTEST PROCEDURE — NOT RECOVERED CANON**:

> **Falling — provisional v0.1**
>
> When a creature loses all support and has no movement mode or effect keeping it aloft, mark it **Falling** immediately. It does not resolve the entire fall at that instant.
>
> A falling creature has a **Falling Step immediately before the start of its next regular turn**, and once immediately before each later regular turn while it remains unsupported. This deliberately gives the table an Action-scale rescue window.
>
> At an ordinary Falling Step, the creature descends up to **300 feet**, stopping early if it reaches a surface capable of supporting it. If it regains support, flight, a secure hold, or another effect that ends the fall before that Falling Step, no descent occurs.
>
> A creature affected by **Feather Fall** descends no more than **60 feet per Falling Step** instead of 300 feet. Feather Fall must be cast before impact; it never reverses damage from a landing that already resolved.
>
> When a Falling Step reaches the ground or another supporting surface, determine the distance descended during **that final Falling Step**. The creature takes **1d6 bludgeoning damage per full 20 feet descended during that step, maximum 10d6**. Less than 20 feet during the final step causes no falling damage. Apply ordinary damage defenses only if they expressly apply to falling/impact damage.
>
> After the landing damage resolves, Falling ends. A creature that takes any falling damage lands **Prone** unless an existing feature explicitly prevents Prone.
>
> Forced movement that removes support starts Falling normally but does not itself add extra falling damage. Teleportation or other movement that places a creature safely onto a supporting surface ends Falling without an impact.

### Why this structure

The **Falling Step before the creature's next turn** is the important part. Regardless of initiative order, other characters get a real opportunity to spend an **Action** before the first descent resolves. It therefore makes the preserved Action-speed Feather Fall usable without retroactively rewriting its casting time.

The **300 ft ordinary / 60 ft Feather Fall** distinction gives the spell's source number actual meaning. The impact formula is deliberately based on the **final step's descent**, so Feather Fall materially reduces impact without automatically guaranteeing a harmless landing: its maximum normal landing exposure becomes 3d6 rather than 10d6.

Every numerical value in that procedure—**300 ft, 20 ft per d6, 10d6 cap, and Prone on damaging impact—is newly authored playtest material**, not claimed from V6/Core V2.

I would accept this for the spell-integration guide now. Before any promotion toward approved canon, Codex should specifically search the **approved V6 gameplay/environment/travel or hazard sections and archived falling/environment tables** for an older impact-distance rule; if one exists, compare it rather than silently overwriting it.