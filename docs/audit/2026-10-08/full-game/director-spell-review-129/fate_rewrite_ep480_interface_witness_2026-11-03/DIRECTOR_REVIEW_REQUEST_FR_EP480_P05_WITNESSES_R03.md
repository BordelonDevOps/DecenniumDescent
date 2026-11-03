# Director evidence review — Fate Rewrite Proposal 05 witnesses, R03

R03 makes one integrity-only correction to R02 and leaves all 15 transitions semantically unchanged. The compatible target-state pointer is now derived from, and asserted equal to, the rebuilt pickup transition's post-state hash.

- Existing owner adoption: FR-EP480-INTERFACE-PROPOSAL-05, SHA-256 cd492a5bdf9c966f83a2674c31ff1db02a10d2df5f3c92fe8b4680974047386d; scope remains the two named TEST_ONLY branches.
- R02 Director review transcription: docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03/CODEX_TRANSCRIBED_DIRECTOR_REVIEW_REVISE_02.json, SHA-256 ebf97d1c16a45989c368406cd0207a0bbb9938b0a72bc1fbffaa823b64c6d333.
- R03 packet: docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03/FR_EP480_P05_TESTONLY_WITNESS_PACKET_R03.json, SHA-256 e575b9ce6738dea5c780c18da95afa8daa8e53602beaf83795d20ca5a47da799.
- R03 manifest: docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03/PACKET_MANIFEST_FR_EP480_P05_WITNESSES_R03.json.

The corrected `/branches/0/targetEvent/stateAtTargetSha256` is `23f127f668ca31f6af4939ea87605c3fad578bd125275df202f2a6a3420144ef` and equals `/branches/0/transitions/5/afterStateSHA256`. The builder asserts that binding, independently replays all 15 transitions and inverses (106 operations each way), and verifies the previously passed retry evidence remains unchanged.

Please return PASS, REVISE, or HOLD bound to the exact main commit and packet hash. No new premise or owner adoption is needed. Keep Queue481 836/12/0, TF192-B02/B04 open, EP480 unsealed, and Fate Rewrite unaccepted/unapplied. No canon, runtime, campaign, seal, blocker, identity, or queue change is requested.
