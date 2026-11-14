# TAC-06 Consume Decay temporary HP

`ConnectedExpeditionSession.StartWithConsumeDecay()` and console `-ConsumeDecay` select TEST_ONLY wire102/base90. The hero can spend one tactical Action and the fixture's one available use at the fixed bed of decaying organic matter. The offer uses actual total level and expires after one elapsed hour. The shared life record owns the remaining buffer. [Source/API contract](SOURCE_API_CONTRACT.md) · [GPT authorization](GPT_CONTRACT_REVIEW.md) · [Pinned sources](SOURCE_BINDINGS.json)

| Executed public event | Result |
| --- | --- |
| Early activation, r122 at `113341/2` | Three temporary HP. Normal HP and maximum remain 26. The Action and source use are spent without a roll. |
| Early depletion, r124 | The defender's real three-point opportunity hit depletes the grant. Normal HP stays 26. |
| Early normal damage, r129 checkpoint | A separate real two-point hit leaves 24 normal HP. |
| Early healing and continuation, r143–184 | The manufactured vial restores two normal HP. The empty buffer remains empty. The hero closes the encounter and moves to (0,1). |
| Late activation, r193 at `113453/2` | The genuinely injured hero has 18/26 normal HP and gains three temporary HP during turn 27, while the resolved encounter remains open. |
| Late healing and exit, r199–200 | The held recipe-4 vial restores eight normal HP and leaves the full buffer in place through encounter closure. |
| Late expiry, r203–204 | At `120651/2` the hero has three temporary HP after paid ordinary movement. At `120653/2` they expire at (0,1) without changing 26/26 normal HP, Wounds, posture or RNG. |

The late witness uses the real encounter after the defender is defeated and before the legal close command, preserving the buffer for the expiry witness. The focused case tests detached same-packet overflow through shared damage, along with strongest-only comparison and blocked or spent-Action activation. Live retries, denials, corrupted grant history, and authentic predecessor controls retain the original authority boundary. The profile has one entitlement and one granting source. Beneficial Long Rest refresh, additional granting effects, production ancestry, general maximum-HP modifiers and revival remain outside this slice. Unity gameplay integration remains deferred. [Early inputs](early.jsonl) · [Late inputs](late.jsonl) · [Replay evidence](public/results.json) · [Bindings](BINDINGS.json)

The focused review asked for explicit checks of which grant identity and deadline survives arbitration. Corrected source `a8a66cd8764174c3bf28e2f233a0b2aa1c71b141` uses the same selection and expiry operation for the live source and the detached controls. Larger compares against actual remaining points, equal and smaller preserve the existing grant and deadline, and stale endpoints cannot clear or restore another grant. [Initial focused review](GPT_INITIAL_FOCUSED_REVIEW.md)

The corrected exact regression passed all **1,498 cases** with zero failures. The ordered inventory contains all 1,497 accepted predecessors plus the registered Consume Decay case. The public routes agree across 17 early and 19 late checkpoints in restored console, uninterrupted console and direct C#. C# 9 standalone compilation and all 18 static checks pass, and authentic wire95–101 controls retain their reference outcomes. The original completed run is retained against its original source and assemblies. [Corrected focused review](GPT_FOCUSED_REVIEW.md) · [Corrected regression](regression/results.json) · [Save compatibility](prior/results.json) · [Original regression](regression/original/README.md)
