# TAC-08 focus-drop clarification

Request: `f0578c8a-3a44-4b26-b20e-8e37961b5bb7`.
Actual GPT response: `94ea32c6-0c95-537d-83ec-732d1a0d171d`.
[Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af8ba86-20cc-83e9-bed0-c2d616fefcdf).

## Actual response

**Yes. Codex’s interpretation is correct. The P1 sentence I approved was overbroad.** Correct the contract and test expectation; do not add an Incapacitated drop rule.

Use this governing replacement:

> A held focus follows the existing held-equipment consequences. Each lawful new Unconscious application resolves its drop-held-items onset once; actual zero-HP/death transitions apply their existing equipment-drop rules. Incapacitated becoming effective, including resumption after suppression, ends incompatible concentration but does not itself drop equipment or replay an Unconscious onset. A worn amulet remains worn through these held-item consequences. Ending or suppressing a condition neither restores ended concentration nor retrieves dropped equipment.

The required distinction is:

| Actual event | Concentration | Held focus | Worn amulet |
|---|---|---|---|
| Standalone/resumed effective Incapacitated | Ends | Retained | Remains worn |
| Lawful Unconscious onset | Ends through applicable incapacity rules | Dropped through existing onset | Remains worn |
| Actual zero-HP/death equipment consequence | Ends under existing life rules | Follows existing drop procedure | Remains worn |

Keep the paired held/worn controls. Also preserve the distinction between a **new independent Unconscious application**, which has its own onset, and suppression ending, retry or load, which must not replay it. Retain the failed drop expectation as a disclosed contract-expectation correction.

I checked the published condition source, `ConditionLedger.Apply/Transition`, the life-equipment path and the [settled lifecycle policy](https://github.com/BordelonDevOps/DecenniumDescent/blob/35bccc0301a60ae8a39999ae2d9aea50c308592c/docs/unity/CONDITION_LIFECYCLE_RULE_DECISIONS.md); a separate reviewer confirmed the distinction. **I have not inspected or executed your in-progress adapter or controls.**

This resolves the dependent interpretation. It is a correction to contract wording, **not an evidence exception**, and grants no final TAC-08 acceptance or successor authorization.

## Codex agreement and retained correction

Codex agrees. Preserve the existing source distinction: effective Incapacitated ends concentration; only actual held-equipment consequences drop a held focus. No new generic or focus-specific Incapacitated drop rule is introduced. P1 in the approved contract is corrected to the exact governing replacement above. This is neither final TAC-08 acceptance nor an evidence exception.

The raw tool response is retained in `GPT_FOCUS_DROP_CLARIFICATION.json`. Source comparison uses `DescentReviewChanges/ReviewBible/data/playtest/core_condition_sources.json`, Incapacitated paragraphs749/750 and Unconscious paragraphs775/776, plus the existing condition ledger and life-equipment paths. Its manuscript binding is SHA256 `53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433`.

Retain the failed detached control at `engine/artifacts/tac08-cleric-casting/lifecycle-producer-clock-fixed/run-20261115T181246695Z-e4d54147/results.json`: its expectation that standalone Incapacitated drops a held focus was incorrect. The earlier control at `lifecycle-producer-tests/run-20261115T181024048Z-1a376106/results.json` also used an outdated condition-journal time; the actual `AppendCondition` producer synchronizes to the current shared clock. Corrected paired controls must cover both conditions and held/worn placement, independent new Unconscious onsets, and no onset replay on suppression, ending, retry or restore. Those execution results remain pending in this clarification record.

