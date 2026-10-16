# Banishment — Repair 03 Director Review

## Current authority
This is the ordinary rank-4 Banishment replacement candidate after Repair03. Preserve the printed source/access card unchanged. The Core's `Instantaneous` metadata remains source evidence; the finite 60-second concentration layer is explicit NEW authorship for runnability.

Current Banishment-only rule IDs:
- `BAN-SAVE-01`
- `BAN-CELL-03`
- `BAN-ADMIT-03`
- `BAN-TRANSPORT-CLASS-02`
- `BAN-CLOSE-03`
- `BAN-PLACEMENT-HANDOFF-03`

`BAN-CLOSE-01`, `BAN-CLOSE-02` and `BAN-RETURN-RESERVE-02` are superseded historical proposals and are not operative.

## Resolution sequence
1. Validate actual class/repertoire, Action, V/S/F, price, concentration, one creature target, 60-foot range/LoE and known obvious endpoint/custody failures.
2. Record `admissionIntent = ACCEPT | RESIST`.
3. Commit Action/RP and Banishment concentration under current spell integration.
4. Resolve the NEW CHA save; ACCEPT may elect failure before roll. Apply actual save features.
5. On failed save, check the shared hard-control allowance.
6. Revalidate actual endpoint/body/custody. A current Dimensional Anchor may defeat establishment.
7. On success, snapshot the origin plane as an opaque existing plane reference, fixed world anchor/orientation and current transported object IDs; establish BAN-CELL-03 and absolute deadline t+60 seconds.

## BAN-CELL-03 exact geometry
Cell-local x=east, y=north, z=up. Floor z=0. Primary horizontal footprint center = (0,0).

Initial width/depth = current footprint +10 feet, each total axis rounded up to 5 feet. Initial height = actual occupied body height +5 feet, rounded up to 5 feet.

Example: Medium 5x5, occupied height6 -> x/y[-7.5,+7.5], z[0,15]. Primary occupies x/y[-2.5,+2.5].

The current boundary is real for target preflight. An internal summon at x[10,15] is illegal in that example because it is outside the cell. Banishment cannot expand before the source legally targets/resolves.

Voluntary geometry changes use current cell space and the actual body-rule preflight.

Mandatory death, concentration/source ending, Polymorph expiry/0HP reversion, summon expiry and other mandatory events are never rejected to preserve Banishment geometry. Resolve the event, then expand the cell if required to contain the resulting current anatomy plus clearance.

## BAN-ADMIT-03
External arrival remains conditional unless an actual source can identify/reach this generated cell. Faction Portal and Spectral Steed do not generically discover an arbitrary unknown cell.

Internal creation:
- source target footprint must already be wholly inside current cell;
- source perception/LoE and support predicates must already pass;
- pay actual source Action/RP/frequency/concentration;
- after successful body creation, expansion may restore clearance but cannot retroactively legalize the target.

## BAN-TRANSPORT-CLASS-02
Ordinary Banishment is planar/extradimensional displacement, not teleportation. Scope: this spell only.

Paladin exact predicates:
- No Escape `/cards/41`: blocks voluntary extradimensional admission. ACCEPT+elect-fail and ACCEPT+roll-fail are blocked; RESIST+roll-fail is forced and not blocked by this card.
- Verdict Absolute `/cards/43`: only voluntary teleport/invisibility; does not block Banishment.
- Reign of Ashes `/cards/130`: prevents benefit from Dash/teleportation; does not block Banishment.

## BAN-CLOSE-03
Any application ending invokes closure, including primary legal escape. The cell ends even when empty.

### 1. Return plane and anchors
Primary uses the snapshotted exact origin plane/world anchor/orientation.

For a secondary body, record at legal admission a closure anchor equal to the primary world anchor plus that body's cell-local offset from primary local origin. This is metadata only; it reserves/protects nothing.

At closure, carried gear stays with its current carrier. Loose object anchors are projected from their current cell-local positions.

### 2. Mandatory terminal plane return
End the extraplanar Banishment state and assign each remaining extant body/corpse/object to the snapshotted origin plane.

**NEW terminal endpoint exception:** if a true transport-prevention predicate such as Dimensional Anchor would block only this mandatory closure transition, ignore only that prevention for this terminal return. Do not ignore physical terrain/occupancy/anatomy/support, real death/body removal, item existence, or voluntary-travel restrictions. This exception is not usable for escape or any other spell.

### 3. Creature placement: accepted canonical rule
Resolve primary first, then secondary creatures by admission order.

At each entity's closure anchor:
1. current anatomy at same position;
2. legal squeeze under COMBAT_ACTION_PLAYTEST;
3. nearest legal adjacent placement in the same unobstructed region.

The accepted body rule controls ties: minimum displacement, greatest footprint overlap, then the Director's fixed neutral board order. Do not pass through walls/closed barriers/occupied space. Do not search farther afield. No crushing damage or invented movement is added.

Earlier successfully placed bodies are ordinary occupied space for later bodies.

### 4. Placement conflict state
The inherited BODY_EQUIPMENT rule decides whether a placement conflict exists. Repair04 does **not** change that global rule.

If same-anchor, legal squeeze and nearest legal adjacent/same-unobstructed-region placement all fail, Banishment has already ended and the cell is destroyed. Record the same identity on the origin plane with the fixed closure anchor and `placementConflict=true`.

**NEW BAN-CONFLICT-04** supplies the Banishment-origin semantics that the global placement text does not specify:
- `closureAnchorReference` is the logical spatial reference for range and source predicates; it is not an occupied footprint.
- Do not grant movement, adjacency, occupancy, cover, squeeze state, wall passage, overlap, flanking or support-contact benefits from that reference.
- Evaluate perception and line of effect through actual terrain from the reference point. A solid wall/collapse can block them.
- Do not categorically suppress Actions/Reactions/targeting. Evaluate each attempted effect's real activation, components, target, range, perception, path, support and geometry predicates.
- Ordinary movement cannot begin because no legal occupied footprint/path origin exists. An independently legal relocation effect may resolve the conflict if its own source can use the anchor reference as the origin location and establish a legal destination.
- HP, Wounds, conditions, concentration, summon/death/body clocks and already-attached effects continue normally unless their own sources end them.
- When obstruction is removed/changed, rerun the inherited placement procedure immediately from the same anchor/current anatomy. This mandatory normalization spends no movement and triggers no opportunity/charge/movement rider.
- A successful legal relocation clears the conflict and establishes its destination footprint.

The current accepted **Dimensional Door** is one demonstrable relocation: self + actual legal gear, known fitting same-plane destination within 500 feet, exact destination footprint/orientation chosen before payment, with no traversed path or destination LoE requirement and atomic failure if the destination becomes illegal. It can therefore resolve a conflict when the caster can still perform its Action/V/S/F and all actual Dimensional Door predicates pass. This is not generic teleport permission.

### 5. Falling and loose objects
A legal unsupported placement starts ordinary Falling from that actual position. A placement conflict alone does not create a legal unsupported footprint, so Falling waits until actual placement/relocation establishes one. Real terrain/support at the anchor still applies to effects whose own predicates reference it.

Loose objects resolve after creatures by stable object ID using the existing equipment-return placement rule. If no legal item position exists, record item placement pending; the item remains real.

### 6. End cell
After every remaining identity is legally placed, in origin-plane placement conflict/pending-item state, or confirmed absent, destroy the cell immediately.

## Mandatory-reversion example
A root-Medium creature is legally Tiny from Polymorph when banished from a 2.5-foot alcove. Polymorph expires at t20 inside the cell. Reversion to Medium occurs regardless of origin fit; Banishment may not veto it. At t60 the Medium body returns to the origin plane. If same-anchor/squeeze/nearest-adjacent all fail, record the canonical placement conflict there and destroy the cell. This is finite Banishment ending, not continued exile.

## Real secondary-body escape example
A banished Mage7 can spend Action/4 RP on `mage.arch.conjure-elemental-familiar` in one currently visible unoccupied in-cell space. The familiar lasts 10 minutes and has no printed concentration. The Mage later starts Faction Portal concentration (Action/5 RP) and crosses to a known positive-standing faction HQ. Primary escape ends Banishment; the familiar and loose cargo remain for BAN-CLOSE-03 and are returned/placed exactly once.

## Repair03 dispositions
- **BAN-R03-01 — AGREE:** protected berths removed; mandatory endings preserved; canonical origin-plane placement conflict is the physical-exhaustion terminal state.
- **BAN-R03-02 — AGREE:** only BAN-CLOSE-03/BAN-PLACEMENT-HANDOFF-03 are current.
- **BAN-R03-03 — AGREE:** current cell bounds and pre-cast in-cell targeting are explicit.
- **BAN-R03-04 — AGREE:** BAN-X04 uses the real nonconcentration Elemental Familiar plus actual Faction Portal.

The examples are authored adjudications, not runtime, human-playtest or balance tests.

## Repair04 dispositions
- **BAN-R04-01 — AGREE — CORRECT ORACLE AUTHORITY AND COUNTERSPELL RECHARGE (correction):** BAN-C17 now cites Oracle /cards/31 Spiral-Touched Boon I, uses its current frequency Reroll 1/long rest, and must use the new reroll result. Wizard /cards/17 remains the special 3 RP Counterspell with INT+PB vs 10+2*rank and now records its actual 2-round recharge.
- **BAN-R04-02 — AGREE — REMOVE LAST RESERVATION REMNANTS AND FIX CURRENT CELL ID (correction):** BAN-C27 now tracks only the extant corpse, surviving real cargo and absence of the expired summon. Current cosmologyBoundary names BAN-CELL-03. Reservation/berth wording survives only in explicitly historical material.
- **BAN-R04-03 — AGREE — CORRECT OPEN-TERRAIN ANCHOR AND IN-CELL SUMMON GEOMETRY (correction):** BAN-C13 returns the Large body at the same spatial anchor on open terrain. BAN-C24 records the required eastward post-admission clearance expansion. BAN-C30 records the Steed-driven expanded cell and an exact Water Pet preflight square that is already visible, fitting and unoccupied before the new concentration ends the Steed.
- **BAN-R04-04 — AGREE — NARROWLY AUTHOR CONFLICT REFERENCE SEMANTICS (NEW scoped authorship over inherited placement conflict):** The accepted BODY_EQUIPMENT rule supplies placement order/conflict but not all spatial semantics while conflict persists. BAN-CONFLICT-04 therefore adds only a Banishment-origin conflict reference: the fixed closure anchor remains the logical location for range and source predicates, while no legal occupied footprint exists for movement/adjacency/body-space claims. Perception/LoE use real terrain from that reference and each effect's actual prerequisites; attached nonspatial effects and all clocks continue. Obstruction removal reruns canonical normalization; an independently legal relocation such as accepted Dimensional Door can move the same identity to a legal destination and clear the conflict. This does not alter the global body rule.
