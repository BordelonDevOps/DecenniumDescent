# Portable equipment and carrying — prototype decisions

**2026-11-04 — Codex / Unity Rules Engine Development consensus, under the owner's delegated rule-decision authority.** This records a narrow schema20 TEST_ONLY implementation. It is not source text, a general equipment model, production runtime selection, or release approval.

## Source-backed facts

- The reviewed source gives a backpack/sack capacity of 30 lb and 1 cubic foot, a 4-pint waterskin, one pound of water per pint, and one pound for an empty waterskin. A full waterskin therefore has a 5 lb gross weight; its contents must not be added twice.
- The reviewed Explorer's Pack fixture has 20 lb of rations, a full 5 lb waterskin, 1 lb thieves' tools, 1 lb mess kit, and 1 lb tinderbox: 28 lb internally. Its 7 lb bedroll, 10 lb of torches and 10 lb hemp rope are attached externally; the rope is expressly strapped to the side. The pack body is 5 lb. Existing rules keep the actor's 1 lb pouch and held 2 lb club in the same carrying calculation.
- The item source supplies no general volume for each item, and a bundle listing does not prove that its contents fit inside the pack.

The source snapshots and SHA-256 bindings are in [the portable equipment evidence](evidence/2026-11-04-portable-equipment/SOURCE_BINDINGS.json). The reviewed pack's exact internal-fit arrangement is a fixture fact, not a rule inferred from its weight or volume.

## Consensus implementation policy

- Use distinct physical equipment identities and explicit `Carried`, `Worn`, `Contained`, `Attached` and `Ground` placement. Existing nutrition lots, water vessels and cache credentials remain authoritative; equipment records link to them rather than duplicating their quantities, freshness, ownership or use state.
- Decompose the full waterskin into its source-backed 1 lb tare and the linked water lot. Its operational carrying mass is tare plus the current water quantity, so draining it updates weight without double-counting its 5 lb full source value. The waterskin still uses the existing 4-pint capacity rule.
- Preserve source mass and current operational mass separately. Count attached gear as carried weight, but exclude it from the pack's internal capacity and fit set. The pack's internal fixture fit set is exactly its six named contents, including the water nested inside the waterskin. Apply the 30 lb capacity and known 28 lb fixture arrangement; do not infer item volume or permit un-authored fit combinations.
- In exploration, each supported pickup, drop, retrieval, stow, handover, wear, removal, open or close operation takes one active second. Reserve that worker interval and advance the shared simulation before the physical state changes. At tactical time, consume the existing object-interaction allowance and do not advance the world clock.
- A handover requires adjacency, recipient consent, an available hand and capacity. Custody changes only after completion; owner identity, provenance and freshness remain unchanged. Descendants travel with a handed-over whole container.
- A worn container must be removed before dropping or handing it over. Moving an item or a container is rejected while a descendant resource, vessel or tool has active reserved work. Retrieve actual tools before using a cache procedure that requires them.
- Check the recipient's active traversal before accepting a handover, so the recipient cannot move away during the one-second transfer. Portion lots retain the explicit fit identity of their authored source; retrieving the remainder does not make an already split subset cease to fit.
- Count the companion's carried empty waterskin tare and its linked water amount as it is filled or consumed. Label unrelated food lots as generic prototype food rather than implying they are the pack's ration profile.
- Reject the optional key variant of the cache fixture because its mass is unsourced. Gate movement of the older unlinked cache waterskin in schema20; it remains in its recorded cache location until that fixture is modeled in the portable system.
- Reject any operation that would exceed a carrier's capacity or require unsupported fit data. Prior schemas 1–19 keep their original serialization and behavior; schema20 is explicit and has no automatic migration.

## Limits

Schema20 currently exercises one reviewed Explorer's Pack fixture connected to the shared clock, inventory, waterskins, cache credential and tactical interaction ledger. It does not implement the complete item catalog, arbitrary containers or volume calculation, general armor/weapon equipment, equipment slots, containers with unknown contents, broader transfer rules, or all acquisition and crafting outputs. General equipment stack splitting beyond the nutrition-lot portion procedure is not implemented. The current 63 lb fixture total (6.3 Load) makes the medium STR 10 actor burdened and lowers the prototype walking speed from 30 ft to 20 ft under the existing provisional carrying policy. The cache's older waterskin transfer is gated because it is not yet represented as portable equipment. All of this remains TEST_ONLY and provisional.

Verification is recorded in [the headless results](evidence/2026-11-04-portable-equipment/HEADLESS_RESULTS.json), [the package checks](evidence/2026-11-04-portable-equipment/PACKAGE_RESULTS.json), and [the independent review](evidence/2026-11-04-portable-equipment/INDEPENDENT_REVIEW.md).
