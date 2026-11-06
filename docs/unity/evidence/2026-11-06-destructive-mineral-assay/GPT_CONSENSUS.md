# Codex / GPT prototype-policy consensus

**Discussion:** Unity Rules Engine Development chat, 2026-11-06. The chat was asked to restate the full operational policy for the schema46 destructive assay because the initial answer was clipped in the browser view. Its completed response was reviewed before implementation.

## Source rules kept distinct

The pinned MGT-07 candidate guides specify a one-active-minute WIS/Mining assay, the governing exact DC or highest assessed tier DC, supported information-only results, no reliable finding on failure, and an actual sample debit for destructive assay. They prohibit repeat checks from unchanged evidence or worker changes while allowing substantively new evidence or a concretely different evidence-bearing method. They do not specify a sample amount, portion identity or debit timing.

## Agreed provisional operational policy

- Bind the assay to one real, explicitly authored prepared portion with stable inventory identity/provenance, exact positive quantity **Q**, authored sufficiency and method compatibility. Do not infer Q from mass, price, tier or stack size. Fractional portions require existing support; this increment only accepts an already-prepared lot and does not subdivide it.
- Reserve Q, work resources and the evidence opportunity when the attempt starts. Atomically debit Q with the first positive credited destructive labor. Zero work consumes nothing. Preserve consumption provenance; do not debit the source deposit a second time or allow consumed material to reappear as a fresh sample.
- Pause/interruption keeps feasible labor and the unresolved attempt. Resume explicitly after revalidating access, tools, capability and continuing evidence. No automatic phase-reset penalty is added. A fully worked attempt blocked by temporary incapacity remains `AwaitingCheck`; eligible resume performs the pending check without extra work or a replacement sample.
- Cancel before positive labor to release unused reservations. Cancel after positive labor closes with no check, refund, findings or transferable labor. The 60 active seconds are required anew for any later attempt.
- Track physical sample identity separately from canonical inventory-lineage evidence basis, source exposure and authored assay method. Splitting, replacing an equivalent portion, renaming or changing workers does not create a new evidence opportunity. A resolved check blocks the same evidence/method across workers. Another real unconsumed sample root or a substantively different authored method may support a separate attempt if no check has resolved for that pair.
- Resolve the check after 60 active seconds using the shared simulation. Commit RNG, degree, findings, status and receipt atomically. Save/restore preserves the complete state without offline progress.

## Codex implementation boundary

The runtime binds the explicit portion amount to an existing `InventoryLotRecord` and its `WorkLedger` quantity. The evidence basis is the root inventory lot in its provenance chain. A method identity is the existing assay profile, compared by substantive profile content with the profile label excluded. Thus a renamed duplicate profile cannot create a second check. A successful check does not create residue or output because no residue disposition is authored in this fixture.

The implementation remains TEST_ONLY. The agreed amount, compatibility, reservation boundary and debit/cancel timing are prototype completions of source gaps, not text recovered from MGT-07 or release approval.
