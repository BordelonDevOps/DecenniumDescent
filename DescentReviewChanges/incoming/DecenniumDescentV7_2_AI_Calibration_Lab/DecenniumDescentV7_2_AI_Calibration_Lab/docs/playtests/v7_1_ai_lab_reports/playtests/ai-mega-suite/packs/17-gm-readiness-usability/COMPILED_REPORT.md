# GM Readiness and Usability — COMPILED_REPORT

**Raw JSON results:** 178
**Evidence level:** B
**Canon edits:** none

## Executive verdict

A fresh Director can prepare and run the Tier I loop from GAMEPLAY_LOOP_CANON.md without inventing major rules, but lookup and cognitive-load failures are real—especially Rest Debt UI conflict, Haven length, and a few ambiguous combat/extract edge cases. Human confirmation still required.

## Scenario coverage

- **GM-ERROR-RECOVERY:** 50 results
- **GM-PREP-TIER1:** 7 results
- **GM-RULE-LOOKUP:** 100 results
- **GM-RUN-COMBAT:** 7 results
- **GM-RUN-EXPEDITION:** 7 results
- **GM-RUN-HAVEN:** 7 results

## Primary findings

- Novice Directors complete GM-PREP-TIER1 with ~9 lookups / ~45 min proxy; experienced GMs ~4 / ~25.
- GM-RUN-COMBAT: Standard 90 TP budget is findable; Secure Cargo discoverability weaker than Attack/Dodge.
- GM-RUN-EXPEDITION: Rest Debt prose vs ExpeditionTracker `/3` caused mid-Watch RULES_HALT.
- GM-RUN-HAVEN: Narrative GM skipped provenance/liens; Gross/Net/True profit labels prevent false profitable calls when used.
- GM-RULE-LOOKUP: 100 prompts; non-located/ambiguous=6 (Retreat double-count, Rest Debt UI, missing standalone Quickstart sheet).
- GM-ERROR-RECOVERY: Attention-every-Watch misapply is correctable from section 7; Rest Debt recovery still UI-ambiguous.

## Rules halts
Total: 18

- {'id': 'RH-17-ERR-000', 'prompt': 'Players forget to assign Rest Watch — how to recover mid-day?', 'status': 'RULES_HALT', 'note': 'If using ExpeditionTracker /3 counter, reconcile with §5 before ruling.'}
- {'id': 'RH-17-ERR-010', 'prompt': 'Players forget to assign Rest Watch — how to recover mid-day? (case 10)', 'status': 'RULES_HALT', 'note': 'If using ExpeditionTracker /3 counter, reconcile with §5 before ruling.'}
- {'id': 'RH-17-ERR-020', 'prompt': 'Players forget to assign Rest Watch — how to recover mid-day? (case 20)', 'status': 'RULES_HALT', 'note': 'If using ExpeditionTracker /3 counter, reconcile with §5 before ruling.'}
- {'id': 'RH-17-ERR-030', 'prompt': 'Players forget to assign Rest Watch — how to recover mid-day? (case 30)', 'status': 'RULES_HALT', 'note': 'If using ExpeditionTracker /3 counter, reconcile with §5 before ruling.'}
- {'id': 'RH-17-ERR-040', 'prompt': 'Players forget to assign Rest Watch — how to recover mid-day? (case 40)', 'status': 'RULES_HALT', 'note': 'If using ExpeditionTracker /3 counter, reconcile with §5 before ruling.'}
- {'id': 'RH-17-LOOKUP-031', 'prompt': 'Can Retreat Escape come from both check and winning round same round?', 'status': 'RULES_HALT', 'note': 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 — AMBIGUOUS'}
- {'id': 'RH-17-LOOKUP-032', 'prompt': 'ExpeditionTracker Rest debt /3 vs canon two-Watch window', 'status': 'RULES_HALT', 'note': 'UI vs §5 — CONFLICT'}
- {'id': 'RH-17-LOOKUP-033', 'prompt': 'Where is public-player one-page Quickstart sheet?', 'status': 'RULES_HALT', 'note': 'Not found as standalone public sheet in required sources'}
- {'id': 'RH-17-LOOKUP-066', 'prompt': 'Can Retreat Escape come from both check and winning round same round? (variant 66)', 'status': 'RULES_HALT', 'note': 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 — AMBIGUOUS'}
- {'id': 'RH-17-LOOKUP-067', 'prompt': 'ExpeditionTracker Rest debt /3 vs canon two-Watch window (variant 67)', 'status': 'RULES_HALT', 'note': 'UI vs §5 — CONFLICT'}
- {'id': 'RH-17-LOOKUP-068', 'prompt': 'Where is public-player one-page Quickstart sheet? (variant 68)', 'status': 'RULES_HALT', 'note': 'Not found as standalone public sheet in required sources'}
- {'id': 'RH-17-REST-DEBT-UI', 'prompt': 'Which Rest Debt clock is authoritative during live play?', 'status': 'RULES_HALT', 'citation': 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Rest Debt / Strain'}

## Ranked defects (clarity, not DPR)

1. Rest Debt UI vs canon (section 5 / ExpeditionTracker).
2. Retreat Escape double-count ambiguity (section 12).
3. No standalone public Quickstart sheet in required sources.
4. Haven 10-step order too long for Tier I without short path.
5. Secure Cargo / cargo-defense action discoverability.

## Human GM agenda

- Timed Tier I prep with only public sources.
- One full day (3 Watches) using ExpeditionTracker; note Rest Debt rulings.
- One Retreat and one failed Extraction Test with risk stated before choice.
- Haven settlement forced through Gross/Net/True profit boxes.

