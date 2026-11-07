# Independent review

**Scope:** uncommitted shared skill-training query, `AbilityCheckRules` snapshot overload, runtime consumer migrations, and focused test.

**Finding:** no confirmed blocker. The query and consumers reuse `Snapshot.SkillTraining`, `SkillTrainingRecord`, `CharacterRuleFacts.ForActor`, and existing `AbilityCheckRules` calculations. Missing training remains rank 0; explicit rank-0 records remain distinguishable in lookup but are untrained; duplicate actor/skill rows fail closed consistently with malformed-snapshot handling. No save-layout or replay-state change was found.

**Limitations recorded:** the focused test does not itself exercise save/restore or replay; those paths are covered by the full connected and procedure-specific suite. `Find` ignores null rows, but snapshot validation rejects null training records before these consumers run.
