# Banishment — Repair 02 Director Review

## Status
This replaces the incomplete first-return closure mechanics while preserving the original source/access card and all historical case evidence. It is **NEW provisional authored playtest coherence only**.

## BAN-R02 dispositions
- **BAN-R02-01 — AGREE — REPLACE CLOSURE DESIGN (NEW scoped authorship):** The prior 120-foot terminal search was incomplete when no physically fitting candidate existed. Replace it with BAN-RETURN-RESERVE-02: each independently returnable body/object package must receive a unique protected origin-plane berth in a finite 120-foot 3D lattice before it can exist as an independent closure unit inside the cell. Primary reserves its exact vacated footprint atomically at establishment. New visitors/creatures, larger body geometry, or independently loose oversized objects cannot establish unless a berth can be reserved. Closure therefore always has a physically fitting nonoverlapping berth; transport-prevention alone is handled by the narrow terminal blocker exception.
- **BAN-R02-02 — AGREE — CORRECT PALADIN READING (correction plus NEW local classification):** Keep the three Paladin cards distinct. BAN-TRANSPORT-CLASS-02 classifies ordinary Banishment only as planar/extradimensional displacement, not teleportation. No Escape can block a voluntarily accepted Banishment because it expressly forbids voluntary extradimensional travel. Verdict Absolute cannot block Banishment because it forbids only voluntary teleportation/invisibility. Reign of Ashes cannot block it because its ash-bind denies benefit from Dash/teleportation and Banishment is not teleportation. Voluntariness is a pre-save acceptance flag independent of whether the target elects failure or rolls.
- **BAN-R02-03 — AGREE — UNIFY APPLICATION LIFECYCLE (correction):** Primary legal escape ends the Banishment application immediately. That same ending immediately invokes closure for every remaining secondary body/object and then destroys the cell even when empty. There is no branch lifetime after primary escape.
- **BAN-R02-04 — AGREE — REPAIR EVIDENCE SCHEMA (correction):** Move RP and other costs to costLedger, timing/deadlines to clockLedger, and populate every current case sourceRefs with exact frozen paths/pointers plus explicit NEW-rule pointers. Preserve every historicalSourceScenario byte-equivalent JSON object.
- **BAN-R02-05 — AGREE — CONCRETIZE CURRENT CASES (correction):** Use actual Faction Portal, Counterspell, Water Pet, Spectral Steed, Dimensional Anchor, Polymorph and Oracle reroll records where supplied. External-visitor routes to an unknown Banishment cell remain conditional because the 49 frozen sources do not themselves give Faction Portal or Spectral Steed knowledge of an arbitrary generated cell. Supply costs, rolls, actions, clocks, footprints and terminal identities in the applicable fixtures.

## Exact current Paladin distinction
- `/cards/41 No Escape`: cannot voluntarily teleport, become invisible **or enter extradimensional travel**.
- `/cards/43 Verdict Absolute`: cannot voluntarily teleport or become invisible. It does **not** contain No Escape’s extradimensional-travel clause.
- `/cards/130 Reign of Ashes`: ash-bound target cannot benefit from Dash or teleportation.

`BAN-TRANSPORT-CLASS-02` is a local Banishment classification only: Banishment is planar/extradimensional displacement and is not teleportation. A pre-save `admissionIntent=ACCEPT` makes successful admission voluntary whether the target elects failure or rolls and fails. `RESIST` plus failed save is forced. Thus No Escape blocks ACCEPT, Verdict Absolute does not block Banishment, and Reign of Ashes does not block it.

## Cast order
1. Validate actual class access/repertoire, V/S/F, Action, 60-ft range/LoE, final RP price and known target/body restrictions.
2. Record admissionIntent. Apply known No Escape if ACCEPT.
3. Commit costs and concentration; open ordinary Counterspell window.
4. Resolve CHA save (or elected failure), including exact Fate-Bound bonus/rerolls.
5. Check shared hard-control allowance.
6. Before transport, atomically reserve the primary’s exact vacated origin package berth. If a true endpoint blocker defeats establishment, no exile occurs and the hard-control claim is not spent.
7. Establish cell, body/cargo ledger and absolute deadline +60 seconds.

## BAN-RETURN-RESERVE-02 — complete physical finite-state rule
The prior return searched for a fitting place only at closure and therefore had a reachable dead end. Repair 02 reverses that dependency: **a state cannot enter the cell unless it already owns a physical return berth.**

### Coordinate construction
Use the primary package’s origin-plane lower-southwest-bottom coordinate `A=(Ax,Ay,Az)`. Candidate lower corners are `A+(5i,5j,5k)` feet for integers -24..+24. Search shells `r=max(|i|,|j|,|k|)` from 0 through 24. Within each shell: k order `0,+1,-1,+2,-2...`; then j from -r..+r; then i from -r..+r; only shell-r positions qualify. Use recorded orientation; no free rotation.

A berth is physically eligible only if the full package prism is empty of creature/solid terrain/immovable object at reservation time and overlaps no other active Banishment berth. Support is irrelevant.

### Protected silhouette
Once allocated, the berth is a transparent placement exclusion until this application closes. Movement can pass through, but a later final placement, persistent created object/body or created terrain cannot end overlapping it. The later event must use its own legal alternative or fail to establish. The silhouette causes no damage, push or teleport and does not protect support beneath it.

### Primary
The primary reserves its exact currently occupied origin package before leaving. It therefore has a physically fitting berth by construction. The reservation persists until full application closure, including after primary escape if cargo remains.

### Secondary bodies and objects
Before external admission or internal creature creation, allocate a unique berth. If none exists, that arrival/creation cannot establish. No source in the supplied 49 files is treated as knowing the generated cell merely because it is interplanar.

Creature packages include assigned noncreature gear. Loose ordinary gear remains assigned to its last carrier for terminal placement. An independently persistent object too large for its assigned package must receive its own berth before separation/creation establishes.

### Geometry changes
When an existing package would change occupied dimensions/orientation beyond its berth, reserve a replacement before the new geometry establishes. For a voluntary source this is a preflight gate. For an indivisible involuntary event, if no berth exists the event cannot establish as a legal Banishment-cell final state and fails as a whole; do not split, rewind or preemptively return the body. This is expressly NEW and Banishment-only.

## BAN-CLOSE-02 lifecycle
Every application ending invokes closure, including primary legal escape, even if the cell is empty. Place remaining primary package, secondary creature packages by admission order, then dedicated object packages by stable ID directly into their own berths. No physical search is needed at closure and no earlier placement can consume another package’s space.

If a true endpoint transport blocker covers a reserved berth, and physical fit/reservation are otherwise valid, ignore only that prevention for the mandatory terminal placement. All other rules of that blocker remain. This exception cannot be used for voluntary escape or any other spell.

Place unsupported bodies normally, then begin Falling. Preserve real death, body disappearance, summon expiry, cargo destruction/consumption and ownership. After settlement release all silhouettes and destroy the cell; empty cell also destroys immediately.

## Concrete current-source integrations
- **Counterspell:** current ordinary record uses Reaction, 60 ft, 5 RP at rank 3 and check DC `10 + 2*triggering rank`; rank-4 Banishment therefore DC18.
- **Faction Portal:** Action, 5 RP at rank 3, one-way 5-ft by 8-ft doorway to a known canonical faction HQ with positive reputation; it can be a concrete escape route from inside the cell when the banished caster has that real knowledge/standing. It does not prove an outsider can discover the arbitrary cell.
- **Summon Spectral Steed:** Action, rank3/5 RP, Large body; internal creation can be concrete if a berth exists. Its Planar Crossing requires a specific known destination; Banishment does not make the generated cell known to an outside Steed owner.
- **Summon Water Pet:** Action, rank4/7 RP, Medium HP35/AC14 body; creation inside requires a return berth and preserves its own concentration/Null Disabled lifecycle.
- **Polymorph:** Action, rank4/7 RP; current body guide fixes Large footprint at 10x10 feet and current Polymorph requires space preflight. Repair 02 adds the Banishment return-berth preflight.
- **Dimensional Anchor:** current endpoint prevention applies normally at establishment/voluntary travel; terminal exception is Banishment-only.

## Conditional visitor coverage
`BAN-C11` and `BAN-C23` remain explicitly conditional. The current 49 files do not prove that Faction Portal or Spectral Steed can target a previously unknown generated Banishment cell. They therefore demonstrate what BAN-ADMIT-01 would do **if** an exact source later supplied that destination permission, not that such permission currently exists.

## Evidence discipline
Every current case carries frozen-source pointers and/or explicit NEW-rule pointers. Historical source scenarios are preserved unchanged. Examples are authored adjudication demonstrations, not executed runtime tests, human playtests or numerical balance evidence.
