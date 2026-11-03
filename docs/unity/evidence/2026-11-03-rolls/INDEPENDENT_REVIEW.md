# Independent review: development restart and declared rolls

Date: 2026-11-03. Reviewer: separate read-only Codex agent `/root/source_review`, requested under `engine/AGENTS.md` and brief section 14. The implementing agent authored this record from the reviewer's returned findings. The reviewer made no file changes.

## Source review

- Identified `C:/Github/DecenniumDescent-review-push-134` as the newest inspected reviewed candidate source root. Its explicit handoff 476 supersedes 475; root START_HERE is stale. Linked handoff/queue/pending/application receipts matched their stated hashes and sizes. Current ordinary spell counts are 831 reviewed / 17 pending / 0 accepted-unapplied, for authored review only.
- Selected the provisional core overlay's **Rolls** section and four Python functions as a bounded source for development-only C# work. This does not promote the candidate into production. Existing validator examples independently specify expected results.
- Confirmed the core prose and Python reference agree between the inspected source roots after newline normalization. The implementation binds exact working-file bytes, not Git-normalized bytes.
- Identified reviewed expedition/crafting/gathering/fishing sources for later scope, while retaining their runtime and selection limits. Tool/recipe review does not establish autonomous companion job behavior or direct world control.

## Implementation review

**No actionable findings in the bounded implementation.** The reviewer checked:

- All four resolvers against the preserved prose and Python reference.
- Natural-roll exceptions, degree thresholds and shifts, opposed ties, expanded critical ranges and input rejection.
- Promotion to `long` before potentially overflowing operations across the supported `int` input range.
- All 19 added regression cases for literal source examples and meaningful boundary expectations.
- Baseline diffs: the existing cases remain intact; the partial class and `*Cases.cs` runner include the new suite.
- Existing laboratory assembly/preprocessor gates, and absence of added production selection, timing, geometry or effects.
- All four source snapshot sizes/hashes and current implementation hashes against the 60/60 passing report.

Scope statements were assessed as accurate: supplied legal roll resolution only, without dice selection, action/target authorization, damage application or a combat implementation.

## Limits

This was independent source/code/evidence review. The reviewer did not independently execute the suite or validate Unity import, Edit Mode, Play Mode or player builds. The implementing agent ran the fresh-process headless suite and package checks. Those reports accurately mark Unity gates NOT RUN. The review does not certify playability, balance, final rule approval or complete-game readiness.
