I agree with the counterproposal. It fixes both defects in my version: the rescue-window failure and the final-step/modulo exploit. The examples all calculate correctly under the revised model.

### Falling — NEW provisional playtest procedure

**This procedure is newly authored for playtesting. It is not recovered V6/Core V2 canon and does not change Feather Fall's source casting time.**

When a creature loses support and has no effect or movement mode keeping it aloft, it enters **Falling** immediately. Falling means unsupported; it does not grant hovering, airborne movement, or permission to remain stationary in the air.

**Fall marker.** If Falling begins during a regular initiative turn, record a fixed Fall Marker at the **end of that same initiative slot in the following round**. The first Falling Step occurs at that marker. Further Falling Steps occur at the same marker once per round. Extra turns, extra Actions, initiative changes, and reactions do not create additional Falling Steps or move the marker.

This guarantees one normal initiative-cycle opportunity for creatures to act before the first Falling Step. A creature that is unable or unwilling to act receives no special rescue action.

**Outside initiative.** If Falling begins outside initiative and timing matters, establish initiative before resolving descent. Treat a virtual slot immediately before the first regular initiative slot as the initiating slot. The first Falling Step occurs at that virtual marker in the following round, after every participant has had one regular-turn opportunity to act. If timing does not matter, the Director may resolve the fall directly.

**Ordinary descent.** At each Falling Step, an unsupported creature descends up to **300 feet**, stopping if it reaches a supporting surface. Track **uncontrolledDistance**, the cumulative distance descended during the current uninterrupted uncontrolled portion of the fall.

On landing while uncontrolled, take:

`min(10, floor(uncontrolledDistance / 20))d6 bludgeoning damage`

If this produces at least 1 point of falling damage, the creature lands **Prone**, unless an existing feature explicitly prevents Prone.

**Feather Fall.** While Feather Fall affects a creature, its Falling Step descends no more than **60 feet**. When Feather Fall first takes effect, set `uncontrolledDistance = 0`; the magic has dissipated prior uncontrolled momentum for this abstraction.

If the creature lands while Feather Fall is still active, use the total distance descended during the current fall and take:

`min(3, floor(totalDistanceDescendedInThisFall / 20))d6 bludgeoning damage`

Feather Fall therefore limits impact exposure but does not guarantee a harmless landing.

If Feather Fall ends while the creature remains aloft, set `uncontrolledDistance = 0` and begin accumulating uncontrolled distance from that point forward. Ending the spell does **not** cause an immediate Falling Step; descent waits for the existing Fall Marker.

A resolved landing cannot be retroactively prevented. Regaining genuine support ends Falling. If support is lost again later, that is a **new fall** with a new Fall Marker and new distance tracking.

### Example check

- 10 ft ordinary → **0**
- 20 ft ordinary → **1d6**
- 300 ft ordinary → **10d6**
- 310 ft ordinary over two steps → cumulative 310 → **10d6**
- 610 ft ordinary over three steps → cumulative 610 → **10d6**
- 310 ft entirely under Feather Fall → **3d6**
- 120 ft under Feather Fall, spell ends aloft, then 190 ft uncontrolled → `floor(190/20)=9` → **9d6**

No remaining mechanical defect in this falling procedure stands out to me. I would log this as the agreed **provisional falling interface**, while leaving the broader spell baseline and game readiness open.