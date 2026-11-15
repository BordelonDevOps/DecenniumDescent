# TAC-07: lawful Cleric repertoire acquisition

**PENDING ACTUAL GPT REVIEW.** Baseline `c4b5a0ad38974ab696ca2b2d7f66fa9de9f30aaa`. The actual preceding review `b6c973bf-8890-57ea-b9e4-135b527b2ad9` selected this source/API gate under CHR-02/FND-05, permitted acquisition separately from casting, and held the selected CHR-03 advancement pending it. This proposal does not itself authorize implementation.

## Source ownership and first ranked access

The single canon manifest and promotion hierarchy remain in force. The ordinary spell catalog preserves global identities, all school placements and per-class rank/access. The normalized operational catalog and authored-review index supply exact reviewed/provisional procedures; those are not production or runtime approval. Shared class rules supply the fallback repertoire where a class has no more specific procedure. The inspected Cleric engine and guide supply no replacement known/prepared count.

At the pinned source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, Cleric is a full caster. `src/data/class-spell-progression.js` and the normalized catalog's `/classProgression/Cleric/learnLevels` put rank0 and rank1 access at Cleric1, rank2 at Cleric3. The class's maximum-rank row is1 at levels1 and2. Thus its fallback acquisition is **three cantrips and two ranked spells at initial Cleric1**, then **one additional ranked spell at Cleric2**. Cleric2 does not unlock rank2. Total character level or sufficient RP cannot bypass the class-level gate.

The raw main and ReviewBible spell/progression mirrors match the pinned metadata bytes. The catalog's whole-file SHA256 is `f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8`; the authored index's current catalog binding matches it. Each selected card's raw source hashes also match the preserved spell catalog/Core source. Preserve the exact selected whole card and current operational procedure; do not substitute an older summary.

## Selected identities

| Acquisition | Global spell ID | Catalog whole-card pointer | Cleric placement/rank/minimum class level |
|---|---|---|---|
| Initial cantrip | `arcane-ward` | `/spells/0` | Abjuration /0 /1 |
| Initial cantrip | `guidance` | `/spells/781` | Universal /0 /1 |
| Initial cantrip | `spare-the-dying` | `/spells/596` | Necromancy /0 /1 |
| Initial ranked | `sanctuary` | `/spells/21` | Abjuration /1 /1 |
| Initial ranked | `purify-food-and-drink` | `/spells/24` | Abjuration /1 /1 |
| Proposed Cleric2 earned ranked choice | `detect-magic` | `/spells/216` | Divination /1 /1 |

All six are currently `operational-playtest-draft` in the catalog and `reviewed-authored-operational-playtest` in the authored index, which points to their actual catalog procedures. The selected rank0 records have base cost0 and rank1 records base cost2; all six have additional cost0. These source cost facts are advisory metadata here, not executable cast payment or a claim that components/targets are available.

Spare the Dying's Necromancy/Universal placements are one identity. Detect Magic's Divination/Universal placements are one identity. Cleric uses its exact class binding above; an alternate placement does not create another known spell or selection credit. Preserve other classes' distinct bindings instead of copying a global rank or school into every class.

The set represents defensive combat, task support, life support, consumables and exploration information for later casting work. Acquisition supplies **none of those effects**. It cannot add AC, stabilize, modify a check, create a ward, purify stock or expose an aura merely because a spell becomes known. Learning an ordinary spell and owning a same-named class card are separate grants.

The registry may later expand by reviewed source definitions. This admission binds six identities; other lawful identities remain explicit unsupported acquisition options rather than fabricated or silently substituted spells. The exact supported choice set and initial five are intentional in this source-bound profile, not a claim that the class source permits only these choices.

Negative source controls are `flare-spark` (no Cleric access), `dispel-magic-lesser` (Cleric rank2/minimum3), and `light` (the authored index has a reviewed standalone procedure, while preserved catalog selection remains blocked and `runtimeSelectionEnabled` remains false). Light is not claimed unauthored or mechanically unresolved; this slice does not promote its distinct source/runtime status or admit it by name. A later reviewed admission may treat its whole standalone card under its proper authority.

## Initial ownership without retroactive grants

Propose a new explicit typed construction entry point that reuses `ClericInitialSelection` and requires a `ClericRepertoireSelection` before creating the simulation. Validate the complete three-cantrip/two-ranked bundle against source, distinct identity, actual class and first-access rules before any construction/funding. The selected default witness uses the first five identities in the table. Incorrect counts, duplicate IDs or school aliases, class-card IDs, unknown/ineligible/unbound sources and extra grants reject before a session exists.

Create known-spell records owned by the existing companion, with casting class Cleric, stable global identity, exact source-definition/placement binding, acquisition kind `InitialClassRepertoire`, class level1 and revision0 construction provenance. Link to the actual typed initial class selection. This is not a learned-through-play receipt, a preparation event, a past Long Rest or a milestone award.

The new profile is opt-in and has a distinct version/fingerprint. Authentic wire105 saves retain their exact prior unknown/unsupported repertoire state and never receive automatic backfill. The old constructor, old wire and old public projection remain versioned. Do not migrate existing saves, infer five missing grants, or choose spells for an existing character during restore.

Keep ordinary known-spell ownership separate from selected class-card ownership, RP/Conviction, inventory and preparation/spellbook records. Cleric uses the admitted known-caster procedure; do not manufacture a Wizard book or Druid preparation step. No focus, component, equipment, slot, charge, spell effect, resource funding, action or time is granted by repertoire acquisition.

## Earned entitlement and the CHR-03 handoff

The source-derived Cleric2 allowance is exactly one additional ranked selection. Detect Magic is the concrete proposed choice, still rank1; its minimum learn level1 does not supply an extra selection slot at Cleric1. Before actual advancement, it is an eligible future candidate, not owned, prepared, acquired or usable.

Propose reusable acquisition validation/settlement definitions keyed to actual chronological class-level acquisition: actor, casting class, source class level/level ordinal, acquisition kind and one entitlement identity. Initial and earned provenance remain different. The earned record must link to the real milestone consumption and advancement revision that creates Cleric2. Repeated identity/entitlement settlement must not duplicate ownership or consume another allowance.

**No synthetic connected level2 is introduced to accept TAC-07.** CHR-03 is still unimplemented. This slice establishes and exercises actual initial ownership through the connected campaign, validates the exact future earned choice and interface, and proves that attempts to obtain that sixth spell before lawful advancement reject unchanged. Pure detached eligibility/settlement controls may exercise a source-qualified level2 input; they must be labeled mechanical tests, never claimed as earned campaign acquisition or accepted save history.

The eventual CHR-03 transaction must call the acquisition component inside the same atomic command that consumes the milestone, appends the actual level and settles all other required grants. It cannot issue a separately forgeable public “give spell” command, insert a fake advancement record or grant Detect Magic before the level is committed. A failure to settle a mandatory repertoire choice must roll back the entire advancement.

Decision B below asks the reviewer to confirm this acceptance split explicitly. Actual earned ownership/replay remains a required CHR-03 connected witness after TAC-07 acceptance; passing a detached level2 control cannot satisfy it. If the reviewer requires the earned transaction in TAC-07 itself, resolve the resulting overlap with held CHR-03 before any implementation rather than bypassing the gate.

No long-rest swap, respec, free replacement, multiclass repertoire, copied book, preparation, bonus spell, future level or omitted prerequisite is supplied by this contract.

## Shared state, source definitions and public capability

Use immutable source-bound spell definitions with identity, all retained placements, exact class access, operational status/procedure hash and review provenance. Caller text never becomes a trusted definition. Authoritative owned records reference these definitions and the one shared actor/class state; canonical validation checks source and entitlement facts. Preserve deterministic ordinal ordering in serialization/views while retaining causal acquisition provenance.

Reuse the shared command authority, receipts, clock, RNG, snapshots and persistence. Initial selection is a constructor transaction; any in-play acquisition attempt goes through the normal authority/expected-revision/idempotency boundary. Do not make a second character model, resource pool, clock or random stream. The known-spell ledger is the one ownership fact; UI labels, catalog presence and class cards do not grant ordinary access.

Expose an owner-filtered read-only repertoire containing known status, acquisition source/class level, exact Cleric rank/placement and source/capability status. Show Detect Magic as unowned when inspecting the supported future choice. No projection may reveal hidden spell effects, targets, Director facts or other actors' private repertoire.

All ordinary casting remains unavailable, including zero-base-cost cantrips. Public and direct typed attempts must produce an explicit unchanged capability denial through the shared boundary; parser rejection alone is not the authority proof. A known-spell flag cannot bypass missing cast payment, components, timing, targets, concentration, strain or effect handlers. Queries consume no time, RNG, resources or receipts. Existing tactical Healing Rite remains the same separate class-card command and retains its reviewed finite payment.

## Persistence and validation

Add only the versioned data required for known ownership, its initial source selection and the future earned-origin contract. Use a separate supported envelope/fingerprint and canonical restore; do not weaken wire105's fixed class/funding/HP/RP invariants or any predecessor save.

Validate the actual actor/class and source, exact initial bundle, acquisition level/kind/revision, identity uniqueness and legal slot/category counts. Reject forged current/earned ownership, switched class/rank/school/procedure hashes, unsupported source status, duplicate alias placements, borrowed class-card ownership and a second initial acquisition. Reconstructed canonical state and real command history must agree; imported descriptive names alone are never sufficient.

An earned-origin record requires a compatible actual advancement audit/entitlement at that same revision. In the initial-only TAC-07 connected profile, a forged earned row must reject. Saving/loading and scene/combat transitions cannot earn another spell, reset source provenance, turn unowned Detect Magic into owned, restore RP or enable casting.

## Required evidence and preserved connected gameplay

Run the accepted Cleric route with the new initial repertoire through explore → first encounter → acquire → manage/research/manufacture → prepare → real later encounter → Healing Rite → continue. The same five ordinary spells remain owned throughout; Detect Magic remains unowned. Actual tactical Healing Rite still uses one Action/2RP for genuine injury, shared RNG3+2 heals1, RP3→1, a later available Action gets the unchanged insufficient-RP denial, and paid ordinary continuation follows. Six genuine manufactured doses remain unspent. No ordinary spell effect or free resource is inserted to make the route work.

Require source/registry/selection controls, full constructor rejection, source-status/class/rank/category/identity/count errors, known-versus-class-card separation, unauthorized/stale/conflicting/repeated acquisition and cast-capability requests, forged earned ownership and all invariant state/RNG/clock pairs. Demonstrate actual public queries and independent typed submissions; do not count parser-only failures as authority or transactional proof. Source catalogs and prepared future APIs alone are not gameplay acceptance.

Retain uninterrupted console, disk-restored console, receipt replay and independent typed dispatch with canonical checkpoint equality and every denial/retry pair. Keep authentic wire95–105 original files, byte-for-byte round trips, actual remaining receipt continuation and cross-profile rejection. Require exact C#9 warnings-as-errors standalone/headless compilation, static package checks, all1,506 accepted cases plus new registered cases, immutable run/assembly/source bindings, exact-file commits and actual final GPT review.

At acceptance, explicitly report that initial acquisition is connected, earned acquisition integration is still required in CHR-03, and casting remains unsupported. This slice neither completes TAC-07's broader acquisition/preparation coverage nor the engine.

## Requested decisions

**A — Source admission and construction.** Approve or correct the exact six-identity source set, first-ranked-access proof, initial3+2 selection and new-profile-only construction. Confirm preservation of raw global identities/placements and the explicit unsupported casting/source statuses.

**B — Earned integration boundary.** Approve the reusable source-qualified Cleric2 entitlement/settlement interface with no connected earned grant before actual advancement. TAC-07 acceptance should require actual initial ownership through the full route, unchanged rejection of premature earned selection and clearly labeled detached eligibility controls. Actual acquisition of Detect Magic in the same atomic earned advancement is then mandatory in the returned CHR-03 contract/witness. No dummy level2/milestone or synthetic history may substitute.

**C — Acceptance and exact successor.** Confirm the regression/save/replay/unchanged-capability evidence above and that, after actual TAC-07 acceptance, the next gate returns to the complete CHR-03 Radiance/Conviction-capacity/earned-milestone settlement contract. TAC-08 still has TAC-07/TAC-02/TAC-05 prerequisites and does not become implemented by this known-spell ledger.

No runtime implementation, compilation or new gameplay test is claimed for this source/API packet. Production authority, whole-engine completion and Unity gameplay integration remain deferred.
