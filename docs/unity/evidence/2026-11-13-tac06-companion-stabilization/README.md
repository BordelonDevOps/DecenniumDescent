# TAC-06 ordinary companion stabilization

`ConnectedExpeditionSession.StartWithCompanionStabilization()` and console `-CompanionStabilization` select TEST_ONLY wire100/base90. The hero spends an Action on a Wisdom (Medicine) check against DC 10 for the actual living, dying companion within five feet and clear delivery. The same shared life state, calendar and RNG govern the result. The connected routes keep the manufactured vial packed so the hero has a free hand. [Source/API contract](SOURCE_API_CONTRACT.md) · [GPT authorization](GPT_CONTRACT_REVIEW.md)

| Actual connected event | Failure route | Success route |
| --- | --- | --- |
| Genuine dying companion on hero turn | r298, 113645/2, one death-save success | r294, 113633/2, zero death-save successes |
| Actual paid attempt | r301, natural 6 + 0, one RNG word | r297, natural 12 + 0, two RNG words including recovery d4 |
| Immediate result | Still dying at 0 HP, no Medicine recovery roll or deadline | Stable and Unconscious at 0 HP, recovery d4 2, deadline 128033/2 |
| Paid ordinary continuation | r350 at 113745/2, after the companion later becomes Stable through its own death saves | r319 at 113685/2, still Stable |
| Absolute recovery | The distinct native death-save deadline is outside this branch's recorded duration. | r320 at 128033/2, one HP recovered once, no RNG at expiry. |

Both histories use the existing public reinforcement and defender controller. They preserve independent Wounds and Prone, reject out-of-range, same-turn repeat and fresh attempts on an already-Stable patient, and prove exact receipt retries are idempotent. The case also exercises detached dead, blocked delivery, unavailable hand and Stable interruption controls. The strict restore rejects a forged Medicine modifier atomically. [Failure inputs](failure.jsonl) · [Success inputs](success.jsonl) · [Public results](public/results.json)

The restored console, uninterrupted console and direct C# replay agree at each retained save within each branch. Authentic wire95 Default and Fishing Trap and wire96 through wire99 profiles match their references. C# 9 warnings-as-errors compilation, all 18 static checks and the registered focused case passed. All 1,496 exact-source regression cases passed across six shards. Unity gameplay integration remains deferred. [Bindings](BINDINGS.json) · [Regression](regression/results.json) · [GPT focused review](GPT_FOCUSED_REVIEW.md)
