# TAC-06 ordinary companion Wound treatment

`ConnectedExpeditionSession.StartWithWoundTreatment()` and console `-WoundTreatment` select TEST_ONLY wire101/base90. The current Player commands use the hero's actual Wisdom (Medicine) and the approved Tier I DC 12. Start consumes one sealed basket through WorkLedger and reserves the fixed kit and healer/patient access. Interruption releases future access and the kit. The patient can start Stable at 0 HP. [Source/API contract](SOURCE_API_CONTRACT.md) · [GPT authorization](GPT_CONTRACT_REVIEW.md)

| Actual event | Time and result |
| --- | --- |
| Genuine encounter exit, r317 | `113673/2`, hero at (1,2), Stable companion at (1,3) with 0 HP, Prone and one Wound |
| Start, r318 | Same time, one whole basket spent, kit reserved, no roll |
| Native Stable recovery, r320 | `128033/2`, 0→1 HP, no recovery RNG word, treatment still active |
| Uninterrupted completion, r321 | `171273/2`, natural 17 + 0, one RNG word, removes the Wound and preserves 1 HP and Prone |
| Ordinary continuation, r323 | Existing pressure blocks the northward edge. Paid eastward movement reaches (2,2). |
| Alternate interruption, r321 | `128033/2`, first basket remains spent, future occupancy released, no treatment RNG or benefit |
| Alternate restart, r323 | `166400`, second basket spent, fresh deadline `195200` |
| Alternate Critical Failure, r324 | Natural 2 + 0, one RNG word, retains Wound and adds one shared expedition Strain to the companion |

The alternate branch uses the existing pressure-watch settlements on the shared clock to reach the genuine later roll. First-point Strain applies −1 to initiative and expedition checks with zero attack and save penalties. Both branches preserve exact finite lots, the same vessel identities and empty tare, existing pressure, and independent life and posture. The approved witness contains one Wound with no linked Injury. Multiple Wounds, second-Wound patient selection, revival, generic medical-kit substitution, rest credit, and production rules remain outside this increment. [Success inputs](success.jsonl) · [Interruption and Critical Failure inputs](interrupted-critical-failure.jsonl) · [Public results](public/results.json)

The retained headless test exercises seat and current-state denials, rollback, stock conservation, recovery ordering and strict rejection of forged Medicine or missing Strain evidence. The public walkthrough compares restored console, uninterrupted console and direct C# receipt replay. The existing compatibility scripts verify authentic wire95–100 saves and continuations. Unity gameplay integration remains deferred. [Evidence bindings](BINDINGS.json)

The first full run exposed a null WorkLedger read on legitimate legacy saves. Corrected source `11a15fd6a69ba073a7443843eb913e132b97e270` preserves those saves, and the existing checksum regression that exposed the issue passes on the correction. The first evidence commit `c61a28f00c8ed5d1bdcadb4af955eea4e52d7a0d` is superseded for acceptance. [Correction evidence](LEGACY_WORK_LEDGER_CORRECTION.json)
