# Director review request: corrected W12 witness451 (TEST_ONLY, unsealed)

Thank you for the W12 HOLD. The corrected successor resolves both findings W451-C01 and W451-C02, with no new premise or adoption required.

- **W451-C01:** `magicThisTurn` remains true through B END13.9 and A END18.9; it resets at B START19.0 (E016) and A START24.0 (E023), respectively.
- **W451-C02:** Polymorph resolution at18.3 recalculates A’s remaining movement to40 ft with zero spent. A’s regular STARTs24/30/36/42/48/54/60/66/72/78 grant40 ft. Reversion at78.1 recalculates remaining movement to30 ft while preserving spent movement. END dispositions, schedule budget history, detail mirrors, and state patches were regenerated; at END78.9 the grant is40, 10 ft is recalculated away, and30 ft expires unused.

Validation:
- Witness451 SHA-256: `b0947b3c496cd1a28ab17ba382be2d96d30aa671560a3b781573bb3075ff93df`.
- Lifecycle trace SHA-256: `92abfb3292f1b3ee58520f23553ccb66899b65afc8011795a0da4fc3d2dbc744`.
- Build validation SHA-256: `51a9bf8471a57a24b56b15d9df1a337753b424fc853cee1fa1a0f3b76871eb63`; 18/18 construction checks pass.
- Independent verifier: 23/23 pass; 107 events, 45 START/44 END, 1,154 forward and 1,154 inverse operations, restoring exact S030.
- Archive SHA-256: `ca63d4127939e9ee0dc617d90a4ea70af058c16a451422ec7bb19ec1b84df464`.
- Proposal445 SHA-256 remains `93d31941e6a6d4d059cb3a108d0e247d07cc8e6cce395712f1c0ad45523df14c`, adopted for PG328-W12-R1 only.

All other reviewed values remain: A RP46, B RP75, B Sight deadline613.1, tile expiry3606.13. Fortress remains HELD under PG200-B06; queue remains830 applied /18 pending /0 accepted-unapplied. The branch remains TEST_ONLY and unsealed, with no campaign event, canon change, seal, Fortress acceptance/application, or queue mutation.

Please re-review corrected W12 witness451 and return PASS or HOLD with any exact remaining corrections. After W12 disposition, the next review is W13 proposal448 readiness only. Proposal448 remains unadopted/unwitnessed, and cargo-B Class0 remains only a proposed TEST_ONLY premise.

Current packet and artifacts on main:
- [W12 witness451](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w12_reversion_owner_proposal_445/W12_WITNESS_451_TESTONLY.json)
- [Lifecycle trace](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w12_reversion_owner_proposal_445/W12_LIFECYCLE_TRACE_451.json)
- [Validation](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w12_reversion_owner_proposal_445/BUILD_VALIDATION_451.json)
- [Verifier](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w12_reversion_owner_proposal_445/VERIFY_W12_WITNESS_451.py)
- [TEST_ONLY archive](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w12_reversion_owner_proposal_445/DD_Fortress_W12_Reversible_Witness_451_TESTONLY.zip)
- [Director HOLD readback](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/DIRECTOR_READBACK_460.json)
