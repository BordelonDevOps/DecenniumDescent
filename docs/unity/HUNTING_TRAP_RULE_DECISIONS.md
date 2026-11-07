# Ordinary hunting-trap prototype decisions

**Status:** TEST_ONLY implementation. The authored procedure below is reviewed PLAYTEST material; integration timings and event policies are delegated prototype completions agreed by Codex and “Unity Rules Engine Development.” They are not original-book wording, production approval or release selection.

## Pinned procedure

The governing row is the hunting-trap entry in `EQUIPMENT_ITEM_PROCEDURES.md`, “Traps and restraints,” pinned at Git revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba`. The snapshot and hash are retained in the [schema55 evidence folder](evidence/2026-11-07-hunting-trap/SOURCE_BINDINGS.json).

- Set a hunting trap with an Action at a suitable anchor. Establish actual anatomy and weight compatibility before deployment.
- The first entrant makes a DC 13 DEX save. On failure, it takes 1d4 piercing damage and is tethered within 3 feet of the anchor.
- The trapped creature or an adjacent other can spend an Action and attempt a DC 13 STR check to free it. Failure deals 1 piercing damage to the trapped creature.
- Reset with an Action before another use.
- The tether does not impose Restrained.
- The physical catalog identifies `adventuring-gear.hunting-trap` at 25 lb and 5 gp. The price does not grant inventory stock or acquisition authority.

## Delegated prototype completions

| Integration point | Adopted completion | Status |
| --- | --- | --- |
| Exploration work | Setting, resetting and freeing take six active seconds outside initiative, using the project’s already adopted ordinary-action timing. Pay the Action once at start; use existing interruption and completed-work treatment. | Prototype policy; not supplied by the trap row. |
| Tactical work | Use the existing tactical Action allowance. Do not also charge six exploration seconds. | Reuses the tactical action scheduler. |
| First entry | The first eligible entrant consumes the armed use whether the DEX save succeeds or fails. No second entrant can claim the sprung deployment. | Prototype clarification of “first entrant.” |
| Event order | Preserve recorded application-time/sequence ordering and stable identity tie-breaks for effects from the same occurrence. Do not globally prioritize traps over reactions. A departure reaction remains before the step’s entry event. | Reuses existing event ordering. |
| Route entry | Only an actual arrival at a different authored route checkpoint may create an entry. Resolve it at that checkpoint through the shared movement-event path. A failed save pauses unfinished route travel there; it does not auto-resume after release. Explicit Resume rechecks existing travel prerequisites. An arrival that completes the segment retains `SegmentComplete`. | Bounded to explicit checkpoint geometry. |
| Tether | Enforce the exact three-foot planar distance. Do not convert it into Speed 0, a five-foot rounding or Restrained. The current tactical grid cannot represent a three-foot move. | Unsupported fractional tactics stay gated. |
| Overwatch Push during pending entry | If a pending entry’s target selects a Push destination beyond the trap anchor’s three-foot radius, reject that rider as `UnsupportedPendingTrapDisplacement` before the rider save or displacement. Keep the resolved shot, damage, spending and RNG. Do not cancel or reorder the trap occurrence or snap the target back. | Bounded capability gate until delayed entry beyond leash is defined. |
| Bounded history | Reserve one trigger-history slot and a worst-case tether slot for every unresolved entry before marking the deployment sprung or drawing RNG. Pending entries reserve from retained tether history as well as active tethers; success releases the unused reservation and failure converts it to the tether record. | Derived reservation from pending trigger records. |

## Explicit implementation limits

The TEST_ONLY profile uses explicit fixture facts for compatible entrant identities, trigger cells and suitable anchors. It supports completed admitted exploration and tactical grid steps plus authored route checkpoint arrivals. It does not infer geometry from item weight or tether reach. Concealed-trap discovery, arbitrary continuous or route mid-leg triggers, moving or destroyed anchors, aerial/anatomically incompatible entrants, teleport entry, and tactical fractional displacement remain unsupported. Other hazards, including caltrops, ball bearings, fire and weather, require their own sourced procedures.

See the [implementation trace](IMPLEMENTATION_TRACE.md#2026-11-07--ordinary-hunting-trap-lifecycle-schema55-test_only) and [evidence](evidence/2026-11-07-hunting-trap/README.md) for records, dependencies, acceptance and exact validation reports.
