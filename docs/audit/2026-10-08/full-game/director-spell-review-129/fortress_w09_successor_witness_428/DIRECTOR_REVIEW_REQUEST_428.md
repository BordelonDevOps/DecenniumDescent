# Director review request — Fortress W01 overlays and W09-R1 (TEST_ONLY)

Please review the exact owner-adopted W01 successor overlays 425 and PG328-W09-R1 reversible witness 428. The owner adopted both W01 proposals exactly (record 424) and adopted W09 Repack01 by exact proposal hash (record 427; proposal SHA-256 `f4dfbf3403c63f603ef188be972c4425cc627309d4fb77cc86934afecd6b8a9d`).

W01 overlays 425: static verifier PASS, 8,134 checks, 0 failures; independent verification 9/9. W09 witness 428: reversible replay PASS, 146 events including 128 regular-turn markers, 100-foot route, 12 stipulated attacks, 18 dependent stair parts and the specified 4-foot hypothetical fall. The entire unchanged S030 parent snapshot is embedded and bound by hash. Each attack explicitly traces the held tile from carry bounds to the strike bounds and back with inverse operations. No actual campaign occurrence is asserted.

Please return precise findings on the W01 support/z46 overlays, each W09 source binding and event sequence, all movement/carry/contact geometry, attack submotions and inputs, support loss, falling result, reversibility, and non-effects. State explicitly whether any correction remains and whether Fortress is ready for identity acceptance. Do not treat this packet as a seal, campaign event, canonical change, or application.

- W01 package: `fortress_w01_successor_overlays_425/DD_Fortress_W01_Successor_Overlays_425_TESTONLY.zip` (SHA-256 `8d1857bcedc412181d90ab2cb6347b2f40b0694c648a081ca2af40f58ad4200e`)
- W09 witness: `W09_REPLAY_428_TESTONLY.json` (SHA-256 `c64ae8c72b06df8e37d6b1ed32cb30bb9d485211554ada708710f02353668404`)
- W09 packet: `DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip`; verify hash in `DELIVERY_428.json`.
- Current authority: `CURRENT_SPELL_QUEUE_428_REPACK01.json`, 830 applied / 18 pending / 0 accepted-unapplied.
- Current handoff: `CURRENT_HANDOFF_428_REPACK01.json`.
