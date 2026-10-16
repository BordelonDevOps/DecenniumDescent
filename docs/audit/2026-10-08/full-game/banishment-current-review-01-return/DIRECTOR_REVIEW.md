# Banishment — Director Review and Adjudication

## Authority boundary
This file reviews the ordinary spell `banishment`. The printed records are retained without rewrite:
- Rulebook/catalog identity: rank-4 Abjuration, temporary other-plane effect.
- Core entry: Action; 60 ft; V/S/F; 7 RP; `Instantaneous`; “Automatic or opposed as described.”
- Seven class access rows exactly as recorded in `SPELL_MODEL.json`.

Because the source does not supply a save, destination, finite timer or return procedure, this candidate uses explicitly NEW authored completions `BAN-SAVE-01`, `BAN-CELL-01`, `BAN-ADMIT-01` and `BAN-CLOSE-01`. None is recovered cosmology.

## Resolution order
1. **Known preflight:** real class/repertoire access; Action; V/S/F; final price; target is one actually perceived creature within 60 ft/LoE; known obvious custody/body/tether impossibilities; known endpoint prevention.
2. **Commit:** pay actual final spell cost, commit Action, start Banishment concentration. Incompatible prior concentration ends now. Apply ordinary cast/counter sequence.
3. **Save:** NEW CHA save vs actual casting-class spell DC. Willing target may declare failure before roll. Apply actual bonuses such as Fate-Bound +2.
4. **Hard-control gate:** on failed save, check shared source-character/target/encounter hard-control allowance. If unavailable, stop: no exile and no soft fallback.
5. **Atomic transport establishment:** revalidate actual endpoint/body/custody. If a hidden/new endpoint blocker or impossible body separation defeats transport, the target stays at origin, paid cost remains, and the hard-control allowance is not claimed because removal never established.
6. **Establish:** create BAN-CELL-01, claim hard-control allowance once, move same target body + legal noncreature gear, record absolute deadline establishment+60 s, fixed world-space origin anchor and object ledger.

## BAN-CELL-01 geometry
Cell-local floor is z=0. Primary arrives centered at local (0,0) with current orientation. Initial rectangular prism = actual occupied bounding box +5 ft on each side/axis, each total axis rounded upward to 5-ft increments.

The cell **expands only outward and never contracts while active**. A legal transformation resolves atomically first; then boundaries expand enough to contain the resulting body plus clearance. A legal visitor/creation uses BAN-ADMIT-01 to reserve the arriving footprint and expands atomically as part of admission. The expansion itself moves no body and changes no unrelated source state.

The sustaining medium is deliberately procedural, not lore: it prevents the cell itself from suffocating an already-admitted body according to that body's established respiration needs, but grants no breathing trait, resistance, immunity or harvestable stock.

## BAN-ADMIT-01
External visitor:
- must possess a separate real interplanar source;
- must satisfy that source's actual destination knowledge/perception/range/cost/Action predicates;
- Banishment gives no cell address or remote sense;
- source must establish a precise fitting terminal footprint.

Internal creation:
- source must otherwise permit creation/summoning in a fitting unoccupied space;
- pay its real cost and concentration/command requirements;
- reserve footprint, expand cell, then create.

Admitted bodies are not additional Banishment targets. They retain independent lifecycles and can leave through their own legal sources.

## Clocks and suppression
Deadline is absolute establishment+60 seconds. Ordinary conditions, concentration, summon durations, Stable/death, Hunt, Opening/Horn and resource deadlines continue.

For this spell only, actual suppression of the Banishment application immediately invokes closure and ends the application. Do not pause the cell and later re-exile the same target.

## BAN-CLOSE-01 terminal ejection
No preemptive trigger exists. Body growth, occupancy changes, support loss and other atomic events complete normally before closure.

At closure:
1. primary current body/corpse, if still present;
2. secondary creatures by stable admission sequence;
3. loose noncreature objects by stable object-ID.

**Return search.** Primary starts with its fixed world origin anchor. Others start with nearest legal space to that anchor. Search deterministic 5-ft Chebyshev rings outward through 120 ft. Candidate must physically fit and not overlap another placed body. Unsupported free space is acceptable if the body fits; then Falling starts.

**Transport blockers.** Test current Dimensional Anchor/other true endpoint-prevention predicates on each candidate. Prefer the first physically legal **unblocked** candidate. If every otherwise physically legal candidate through 120 ft is blocked **solely** by transport-prevention effects, ignore only those prevention predicates and choose the nearest otherwise legal candidate. This final clause is the NEW Banishment-only terminal exception. It cannot be invoked for voluntary escape, another spell, occupancy, wall embedding, physical size, death/body removal or resource costs.

No Escape/Verdict Absolute are voluntary-only and therefore do not stop mandatory closure. They can stop a willing pre-roll election that would voluntarily enter extradimensional travel. Reign of Ashes is not silently converted into a planar block.

## Death/body lifecycle
- Living death inside remains actual death. Surviving corpse returns; no healing/resurrection.
- Hunted Death/finality remains actual.
- If an actual source removes/vanishes a body, return no replacement.
- A Null Disabled finite summon remains the same body while its own source persists; independent expiry/concentration can end it.
- Internal summoned/created bodies keep their own end rules. Their source ending beats Banishment closure because there is then no body to place.

## Cargo
Track exact object IDs. Worn/carried gear stays with its holder if still carried. Loose objects return after creatures. Consumed/destroyed/escaped objects do not return. Cell boundaries have no object IDs and yield nothing.

## Current spell/class interfaces
### Spell Shield
Generating rank is 4. Accepted Spell Shield only reflects rank 0–3; no reflection.

### Dimensional Anchor
Establishment and voluntary escape respect endpoint prevention. A later Anchor over the old return anchor does not freeze the cell: closure searches outward and uses the narrowly scoped last-resort closure exception only if prevention alone blocks every physically legal candidate through 120 ft.

### Resonance Beacon
Same-plane requirement remains literal. Outside beacon != cell plane. An inside beacon can serve only its own actual cell-plane travelers/destination.

### Xi
`Declare Contradiction` needs the bearer to perceive the selected creature, know the spell record, spend its Action, obtain actual caster+target consent, and spend charge only on valid completion. Isolation often prevents those predicates. No remote possession-based cancel exists.

### Paladin
- No Escape: voluntary teleport/invisibility/extradimensional travel only.
- Verdict Absolute: voluntary teleport/invisibility only.
- Chain of Duty: same-plane + within 60 ft; old anchor metadata is not location.
- Reign of Ashes: retains its exact speed/benefit wording; do not broaden it.

### Oracle
Fate-Bound Boon IV +2 applies to this save. No other Oracle immunity/resistance is inferred.

### Cleric
Banish Unholy is separate: WIS save, radiant damage, push; only a failure by 10+ gains its own until-end-next-turn banishment rider. Do not merge it with BAN-CELL-01.

## Plane-erasure boundary
The supplied current source set contains no executable rule that deletes an established plane from existence. Do not invent a cosmological successor plane to solve a nonexistent current state. If a future authored source introduces true whole-plane destruction, that source must define what happens to locations/bodies associated with the erased plane before interoperability can be adjudicated.

## Review dispositions
- **BAN-01 — REVISE (NEW scoped authorship):** A generated isolated extraplanar spell-cell preserves the printed temporary-other-plane effect without naming or identifying any reviewed plane. The draft topology is retained only as a local spell-space and revised to an elastic finite enclosure so body/atomic geometry changes do not require a hidden preemptive interrupt.
- **BAN-02 — REVISE (NEW scoped authorship):** Use Action/60 ft/V-S-F/base 7 RP and actual class spell DC; NEW CHA save, willing pre-roll failure, concentration up to 60 elapsed seconds, one-live-application guard, and the existing shared hard-control allowance. Concentration begins at legal cast commitment and a failed/countered cast does not restore displaced concentration.
- **BAN-03 — REVISE (NEW scoped authorship):** Reject the draft's pre-change early-return interrupt. Geometry changes resolve normally inside the elastic cell. Source ending performs one deterministic closure-ejection transaction. Ordinary endpoint blockers are respected first; a narrowly scoped terminal closure exception prevents an endpoint blocker from converting a temporary spell into indefinite imprisonment.
- **BAN-04 — REVISE (NEW scoped authorship):** Independently legal entrants and internally created creatures may exist only through their own real permissions/costs. Admission expands the finite cell only enough to fit the actual admitted body. At closure all remaining real occupants and loose objects are ejected once by stable order; escaped/ended/consumed identities are not recreated.
- **BAN-05 — AGREE WITH CLARIFICATION (correction/clarification):** The spell transports exactly the selected creature plus genuine noncreature worn/carried gear. Separate creature bodies—including passengers, mounts, swallowed creatures and companions—do not become gear. Impossible separation/tethers can defeat establishment. Transformations, death, body removal, Null Disabled summons and cargo keep their own source lifecycles.
- **BAN-06 — AGREE WITH CURRENT INTERFACES (correction/clarification):** Use accepted AC4 interfaces: rank-4 Banishment is ineligible for Spell Shield; Dimensional Anchor blocks ordinary planar endpoints; Resonance Beacon remains same-plane; Xi can end only the actual ongoing target branch with its exact consent/perception/range/charge procedure. Cleric Banish Unholy remains a different class technique.
- **BAN-07 — AGREE WITH SOURCE PREDICATES (correction/clarification):** No Escape and Verdict Absolute bar voluntary teleport/extradimensional travel, not an involuntary failed-save exile or mandatory closure. A willing election to fail is voluntary admission and is blocked while those predicates apply. Reign of Ashes blocks benefit from teleportation but Banishment is authored here as planar displacement, not a teleport benefit. Fate-Bound gets its actual +2 save bonus. Chain of Duty still requires same plane.
- **BAN-08 — REVISE (NEW scoped authorship):** Add BAN-ADMIT-01: a legal visitor/created body can be admitted only when its own source has a real destination/creation permission, cost and fitting terminal footprint. The cell expands atomically around that footprint; admission grants no route, knowledge, immunity, command or return resource beyond terminal cell closure.
- **BAN-09 — REVISE (NEW scoped authorship):** No universal interrupt or rewind is created. Events finish at their normal atomic boundaries; the cell expands instead of preempting transformations/occupancy changes. Final return uses BAN-CLOSE-01. The current 49-source set contains no executable whole-plane-erasure mechanic, so no speculative cosmology fallback is invented; a future source that can erase an established plane requires its own explicit successor-location interface.
- **BAN-10 — AGREE (review discipline):** Accepted AC4 procedures are interoperability authority only within their recorded scope; lexical class hits are navigation evidence only. Preserve all historical scenario text as evidence, author current adjudications separately, and claim no runtime/human/balance approval.

## Authored-example status
`CASEBOOK.json` contains 30 authored adjudications. They demonstrate the written procedure only. They are not executable runtime tests, human playtests or balance evidence.
