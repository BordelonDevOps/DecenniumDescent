# Banishment — Repair 02 Player Procedure

## Scope and source identity
This is the **NEW provisional authored procedure** for the single ordinary rank-4 **Banishment** spell. It does not alter the accepted AC4 fifteen-spell module or Cleric **Banish Unholy**. The original source remains preserved: Action, 60 feet, V/S/F, base 7 RP, and “Send a creature to another plane temporarily.” Core also prints `Instantaneous`; that metadata remains evidence. For runnability only, this procedure authors concentration up to **60 elapsed seconds**.

No named plane, afterlife, soul destination, Heartcell identity, campaign era, or origin claim is created.

## Cast, intent and save
Choose one physical creature you actually perceive within 60 feet and line of effect. The target may be you. A corpse, image, soul record or unattended object is not a creature target.

Before rolling, the target records **admissionIntent**:
- **ACCEPT:** the creature accepts Banishment if the save fails. It may elect automatic failure or roll normally. Either way, a failed save is **voluntary admission**.
- **RESIST:** a failed save is **forced admission**.

Commit the Action, V/S/F, final spell price and concentration under ordinary spell timing. Then make a **Charisma save against the actual casting-class spell DC** unless ACCEPT elected failure. Fate-Bound applies its exact +2 against banishment. A successful save creates no exile. A failed save also requires the existing shared hard-control allowance; if unavailable, no soft fallback is invented.

## NEW Banishment transport classification
For this spell only, movement into/out of the generated cell is **planar/extradimensional displacement, not teleportation**. This does not redefine any other planar effect.

Therefore:
- **No Escape** blocks ACCEPT because it expressly forbids voluntary extradimensional travel. It does not block a RESIST target forced out by a failed save.
- **Verdict Absolute** forbids voluntary teleportation/invisibility only, so it does **not** block Banishment.
- **Reign of Ashes** denies benefit from Dash/teleportation. Banishment is not teleportation, so it does not block Banishment.

## Temporary cell
A successful Banishment creates one finite, isolated extraplanar spell-cell. It is not identified with any named cosmological location. The cell supplies a level ephemeral floor, ordinary light and nonharmful sustaining medium, but no harvestable air/water/material or resistance/immunity. The target retains ordinary Actions, movement, HP, conditions, concentration and real clocks.

The cell begins large enough for the admitted package and can expand only when the **Return Berth** rule below also succeeds.

## NEW Return Berths — BAN-RETURN-RESERVE-02
Every body or independent closure package inside Banishment must already have one protected, physically fitting **return berth** on the origin plane. This is what makes closure finite.

At establishment, the primary package reserves the exact footprint it is vacating. That berth remains fixed in world coordinates even if a platform later moves.

A berth is a transparent placement exclusion, not a wall: creatures may move through it, but no later creature, persistent object, created terrain or final geometry may end a resolution occupying its volume. The spell never pushes, crushes, deletes or teleports that later entity. Support may still be destroyed, so a returning body can appear unsupported and then fall normally.

If a new visitor, summon, persistent object, or larger body would become an independent closure package, a fitting nonoverlapping berth must be reserved **before that state establishes**. If no berth exists in the finite lattice, that new arrival/creation/geometry cannot establish. Costs already committed follow the source that attempted the effect.

### Finite berth lattice
World axes are x=east, y=north, z=up. Starting from the primary origin package’s lower-southwest-bottom coordinate, candidate lower corners are offset in exact 5-foot steps `(5i,5j,5k)` where each integer is -24..+24. Search 3D Chebyshev shells `r=max(|i|,|j|,|k|)` from 0 to 24. Within one shell use vertical order `k=0,+1,-1,+2,-2...`, then y from south to north, then x from west to east, accepting only coordinates on that shell. Keep the package’s recorded orientation; the search grants no free rotation.

A candidate must physically fit the entire package, overlap no body/solid terrain/immovable object, and overlap no other Banishment berth. Support is not required.

## Visitors, summons and transformations
Banishment grants no route or destination knowledge. A visitor can enter only through an independently legal source that can actually identify/reach the cell. The current supplied Faction Portal and Spectral Steed records do **not** by themselves discover an arbitrary unknown cell.

An internally created creature such as Water Pet or Spectral Steed can be created if its own source is legal **and** a return berth is first reserved. A body-changing effect likewise needs a replacement berth if its package dimensions/orientation outgrow the old berth. If none exists, the new geometry is not a legal Banishment-cell final state and cannot establish.

## Time and ending
Successful establishment records an absolute deadline 60 elapsed seconds later. Other real clocks continue 1:1. Banishment itself grants no rest/stasis. Concentration ending, valid ending/suppression/Xi termination, the deadline, or the primary legally escaping ends the application.

**Primary escape has one lifecycle:** the application ends immediately, every remaining secondary body/object is settled once through closure, then the cell ceases even if empty.

## Closure — BAN-CLOSE-02
Each remaining package returns directly to its own protected berth. Order: primary if still present; secondary creatures by admission order; dedicated object packages by stable object ID. Because berths never overlap, one earlier return cannot consume a later body’s only space. Unsupported returns fall normally afterward.

If a current Dimensional Anchor or other true transport-prevention effect blocks a reserved berth, closure first recognizes that blocker. When the berth is otherwise physically legal and **transport prevention is the only failed predicate**, Banishment ignores only that prevention for this mandatory terminal placement. This is not a reusable Anchor bypass and never permits voluntary travel.

After settlement, all silhouettes release and the ephemeral cell is destroyed. If nothing remains, the empty cell is destroyed immediately.

Death, vanished bodies and consumed cargo are never reversed. The same corpse returns if one still exists; an ended summon is not recreated.

## Current interfaces
- Rank-4 Banishment is outside accepted Spell Shield rank 0–3 eligibility.
- Dimensional Anchor blocks ordinary establishment/voluntary escape. BAN-CLOSE-02 has only the terminal blocker-only exception above.
- Resonance Beacon keeps its actual same-plane predicates.
- Xi can end only the actual ongoing target branch through Xi’s real Action/range/perception/consent/charge rules.
- Chain of Duty still requires same plane.
- Cleric Banish Unholy remains a separate class technique.
