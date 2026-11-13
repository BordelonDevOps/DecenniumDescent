# TAC-06 companion administration

`ConnectedExpeditionSession.StartWithCompanionDose()` and the console's `-CompanionDose` select TEST_ONLY wire99/base90. The hero carries the same recipe 4 vial and can feed it to the eligible named companion on a lawful tactical turn. The profile binds willingness and compatible ingestion for this exact companion. It reuses the player's existing grant for the one selected reinforcement command and the existing defender, roster and turn procedures. [Source/API contract](SOURCE_API_CONTRACT.md) · [GPT authorization](GPT_CONTRACT_REVIEW.md)

| Actual connected event | Revision | Observation |
| --- | ---: | --- |
| Hero enters combat | 118 | Vial is packed. Companion is staged at (2,3), outside the initial roster. |
| Hero retrieves the same vial | 120 | One free interaction. Companion administration is unavailable before admission. |
| Companion is admitted | 128 | Physical arrival at (1,3), paid end-round roster transition and one regular-turn ledger. |
| Defender damages companion | 137 checkpoint | One real point of HP loss, from 26 to 25. No wound. |
| Hero steps back into reach | 141 | Hero at (0,2), companion at (1,3). Out-of-reach attempt rejected beforehand. |
| Hero feeds the dose | 142 | Hero turn 6, clock 113369/2. Actual faces 3 and 2 give seven potential healing and one effective HP. Hero HP stays 21. |
| Hero resumes ordinary travel | 183 | Clock 113445/2 after actual encounter exit and paid movement. |

Feeding spends one hero Action and keeps the current interaction count and clock. The companion retains title and maker provenance. The hero keeps the same empty vial in hand and carried weight falls by exactly 1/10 lb. The sibling dose stays at the bench.

The restored console, uninterrupted console and direct public C# agree at all 18 named saves. Exact public retries and live pre-admission and range denials preserve the full snapshot. The registered case additionally covers a live pending opportunity, wrong seat, contained dose, revoked authority, conflicting command ID, and atomic strict rejection of forged recipient and Action histories. Detached blocked-delivery, zero-HP and spent-Action probes are identified separately from connected gameplay. [Walkthrough](walkthrough.jsonl) · [Public results](public/results.json)

Authentic wire95 Default and Fishing Trap histories and authentic wire96–98 selected restores and continuations match their references. The C# 9 warnings-as-errors build and all 18 static checks passed. All 1,495 exact-source regression cases passed across six shards. Unity gameplay integration remains deferred. [Bindings](BINDINGS.json) · [Regression](regression/results.json) · [GPT focused review](GPT_FOCUSED_REVIEW.md)
