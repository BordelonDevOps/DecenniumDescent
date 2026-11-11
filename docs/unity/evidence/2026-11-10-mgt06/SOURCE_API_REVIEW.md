# MGT-06 source/API review — responsibility handover

**Review stage:** This records the source/API gate completed before implementation. GPT later inspected and accepted implementation commit `9f8478b88399fae8fc8f4818f7518718d16afa20`; see [the actual implementation review](GPT_IMPLEMENTATION_REVIEW.md). GPT did not independently execute C# checks.

## Source binding

- Source revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.
- Canonical source file at the pinned revision: `DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_RECIPE_PLAYTEST.md`.
- Later evidence copy: `docs/unity/evidence/2026-11-05-fishing-trap/sources/FISHING_RECIPE_PLAYTEST.md`, introduced at `ea259f8df18da59cd47a2f5763eeb9a2a1f68720`.
- Both paths resolve to Git blob `01aa68782e604c3e2b2e06ca1caf582d8cd01305`; the pinned revision does not contain the later evidence-copy path.
- Local SHA-256: `447c77740e42a561346fdbbb0a5ed4e785421c27c4f399bfbd53ab45240d36cf`.
- Relevant source rule: an unresolved Fishing deployment is limited to one per lead; the unattended Trap check is `d20 + WIS + one applicable proficiency contribution`. The pinned source does not specify a general transfer transaction or consent authority.

## GPT's actual source/API direction

GPT confirmed MGT-05A/B/C accepted and identified MGT-06 as the next mapped dependency. It approved a bounded schema38 TEST_ONLY handover behavior profile with no schema wire addition and no parallel event ledger. The implementation contract is:

1. Keep `FishingTrapAttemptRecord.ResponsibleHolderId` as the only current-holder state. Commands, revisions and existing receipts establish the change and deterministic replay.
2. Append a distinct `CommandKind` for handover. The current holder is `Command.Actor`; the willing recipient is `Command.Target`; expected revision is present; coordinates and command payloads are empty. It transfers the sender's unique occupied deployment obligation. Discovery identifies that obligation, and query and execution use the same assessment.
3. Require host-derived authority to control the sender, require `Authority.ConsentsToHandover(recipient)`, require a distinct existing recipient and require that recipient to have no occupied allowance. Do not gate this command on `CanModifyWorld`; do not grant inventory or physical custody.
4. Keep transfer instantaneous and exploration-only: no `RuleClock` advancement, labor, Action, Reaction or RNG. It applies only after setup commits and while the physical Trap remains deployed, including before or after its check. Existing working or paused retrieval remains unchanged and with its original worker.
5. Let the former holder use its existing capacity for a genuinely independent deployment. Prevent the recipient from setting another while its handed-over deployment is still active. Preserve setter-only setup pause/resume/cancel; use the current-holder route for abandonment; keep actual retrieval governed by the existing capable-worker path.
6. Correct the source mismatch only inside the new profile: derive and capture WIS at setup from the shared character record. Preserve the historical schema37/38 profile's old calculation, fingerprint and replay. Handover never recalculates the recorded check.

GPT's bounded acceptance scenario was: commit a first Trap setup and save/restore it; transfer A→B; prove no state change besides holder, receipt and revision; show A can start an independent deployment while B is blocked; restore after handover; compare the due check with a no-handover control using the original setter facts, deadline, die and outcome; retrieve the same physical Trap through the existing work/capacity/path rules; and verify byte-identical replay and exact command retry after restore. Rejections cover unwilling, self, unknown or already-occupied recipients, nonholder/unauthorized actor, stale or malformed command, and forged holder-state edits. Existing retrieval and historical-profile behavior also remain covered.

## Scope boundaries

This contract authorizes only the TEST_ONLY fixture profile described above. It does not define production consent, ownership disputes, travel to the Trap, negotiation, tactical transfer, general companion assignment, broad deployment-allowance rules, or a general inventory handover. Those remain unimplemented. GPT approved the source/API contract before implementation; the separate implementation review records its acceptance, evidence qualifications and next dependency.
