# Observation attack effect blocking — 2026-11-06

## Acceptance

`observation_attack_rejects_known_target_through_effect_blocker` starts from the shared world with an authored transparent effect-only barrier between the active actor and the target. Direct sight and current-location knowledge both succeed. After the actual `BeginFixedEncounter` and stance commands, the ordinary `AttackClub` command is rejected as `BlockedLineOfEffect`. The rejection helper compares encoded snapshots before and after, so clock, random state, revision, receipts, combat history, inventory and observation knowledge all remain unchanged.

The fixture is TEST_ONLY. This exercises the existing sight/effect separation and combat target check; it adds no new rule or persisted record.

## Validation

- Focused case: [`FOCUSED_RESULTS.json`](FOCUSED_RESULTS.json), **PASS 1/1**.
- Full C# 9 warnings-as-errors suite: [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json), **PASS 1,176/1,176**, zero failed.
- Static package validation: [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json), **PASS 18/18; 237 assets; 237 unique GUIDs**.
- [Source and report bindings](SOURCE_BINDINGS.json) preserve the tested source hash and result references.

This case does not implement post-attack evidence disclosure. The current fixture has no supported sound, projectile-trail or other event-sensory channel, and the adopted visual-only limit cannot infer one from geometry. See [observation decisions](../../../../OBSERVATION_RULE_DECISIONS.md).
