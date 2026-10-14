# Herbalism — internal Panacea procedure

**Draft awaiting exact manuscript review. Director-only.** Use with the shared Herbalism guide and internal cards. This file does not grant formula access or change ingredient availability.

## Worldroot Panacea — recipe-647

Apply one dose over **10 uninterrupted active minutes**, with one available hand and continuing touch/access to a compatible willing or Incapacitated active creature. In initiative it needs 100 consecutive regular-turn Actions and at least 600 elapsed seconds. Extra Actions and inserted turns do not shorten either requirement. Use the shared interruption/recipient-lock procedure. Spend the physical dose at legal start; interruption destroys the dose and produces no benefit, but **does not spend the recipient's seasonal entitlement**.

Before a legal attempt, establish that the actual recipient has an available entitlement. Only one Panacea application may be in progress on that recipient. Record a temporary attempt lock, not a spent entitlement. Release the lock on interruption or resolution, including applier/recipient death; changing the applier does not preserve partial progress. Check the recipient's eligibility and entitlement again immediately before resolving. If no longer legal, no result occurs; the committed dose remains spent. No parallel applications can multiply one available benefit.

At completion, choose and end **one present removable disease source, one present removable poison/toxin source, one external removable curse source, or one legally removable Exhaustion level**. Preserve all other independent records. End only the selected source/level and its explicitly dependent consequences. A suppressed but still-present removable source remains selectable. If no eligible cure target exists, skip the cure; the independent healing attempt remains possible. Then attempt **10d6+20** ordinary magical nonspell HP healing under actual caps and blockers. Cure is independent of positive HP restoration. Removing Exhaustion first may restore effective maximum HP before the healing is capped; restoring maximum itself grants no HP.

Respect actual source-specific removal exclusions. The Panacea does not remove intrinsic ancestry/class traits, an Oracle curse that is not ordinarily removable, Corruption, Wounds/linked Injuries, identity effects, or a source that expressly requires a different removal procedure. It does not restore Dead creatures. A living protected-return creature with Exhaustion 6 may lose a legally removable level under its existing lifecycle rules; a corpse cannot be revived by reducing the number.

For this exact-review draft, a **successful benefit resolution** means at least one eligible source/Exhaustion level was actually removed, positive current HP was actually restored, or an existing legitimate healing-triggered endpoint actually removed an eligible condition. Commit the recipient entitlement once at that resolution timestamp. A wholly blocked completion with none of those benefits spends the physical dose but not the entitlement. This makes the source's “can benefit only once” concrete; no refund or extra attempt is created inside one spent dose. Each retry needs a fresh full dose and full application. A callback roll alone that removes nothing is not a benefit. This success boundary is explicitly submitted for exact GPT review.

## Stable season-limit mode

Before the first Panacea benefit, fix one campaign-wide `seasonLimitMode`.

- If the campaign already has explicit campaign-season IDs, use the actual current `seasonID`. Record `recipient + seasonID` on successful benefit. Refresh only at an actual recorded campaign-season transition.
- If no such chronology exists, lock **100 elapsed days (8,640,000 seconds) from the recipient's previous successful benefit resolution** as the fallback. At the exact deadline a new attempt is eligible. Before the first benefit there is no prior timestamp.

The fallback is an openly authored limit, not proof that a campaign season or Opening canonically equals 100 days. Once selected, that mode persists unless the owner expressly approves a chronology migration. A migration must preserve previous spent benefits rather than silently reset them. Sessions, rests, travel, expeditions, contracts, stages and Openings never create a new season unless the independent recorded campaign chronology actually establishes it. Players cannot rename a season or switch modes to refresh use. Death/resurrection, another crafter, transfer of the dose, a new body or a new Opening do not reset the actual recipient's history. No cosmological account of identity is introduced by retaining the existing recipient record.

## Quality and source limits

The source batch is one dose. Flawed is Failed: the ten-minute application is not a duration to halve into a weaker cure. Exceptional/Masterwork cannot add a cure, increase healing, shorten the application, reset the seasonal limit or enlarge target scope; the generic singleton yield remains one, or its finished vial may receive max/current HP 2. Manufacturing still uses the source's full 480 active hours, level 20, DC 28, real component identities and formula/facility access. Source optional Director guidance is retained as evidence and is not a newly activated ritual or cosmology rule.
