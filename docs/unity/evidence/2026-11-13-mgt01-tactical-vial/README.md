# MGT-01 tactical packed-vial access

`ConnectedExpeditionSession.StartWithTacticalVial()` and console `-TacticalVial` select TEST_ONLY wire98/base90. The hero brings the same manufactured recipe 4 dose into the later encounter inside the exact worn Explorer's Pack. Tactical Open and Retrieve use the ordinary object-interaction ledger. Each operation adds zero seconds and no work interval. Drinking uses the existing held-dose Action. [Source and API contract](SOURCE_API_CONTRACT.md) · [GPT authorization](GPT_CONTRACT_REVIEW.md)

| Connected route | Pack entry | Retrieve and drink | Continued exploration |
| --- | --- | --- | --- |
| Closed pack | r117 at (0,3) | Open r118 spends the free interaction. Retrieve r123 spends the second interaction and Action. Same-turn use rejects. Use on turn 2 at r130 restores 5 HP from 8 potential, with actual faces 3 and 3. | r167 at 113433/2 |
| Pre-opened pack | r116 at (0,3) | Retrieve r117 spends the free interaction. Use on the same turn at r118 spends its Action with faces 1 and 3, six potential healing, and zero effective healing at 26/26. | r166 at 113431/2 |

The closed route has a live opportunity decision at r121. Retrieval rejects with identical save bytes before the defender's reaction resolves. Both routes reject drinking while contained. Opening preserves the contents and seal. Retrieving keeps companion title, hero custody and exact carried burden, then occupies one hand. Drinking retains that same body as an empty vial.

Restored console, uninterrupted console and direct public C# agree within each branch. The closed route compares 18 named saves and the pre-opened route compares 12, including denial snapshots. The real automatic defender choices are regenerated on direct replay. The focused control also checks current-grant retries, wrong seat and turn, exact resource ledgers, atomic rejection of forged spending, and explicitly detached available-hand and spent-Action contrasts. [Public results](public/results.json) · [Closed inputs](closed.jsonl) · [Pre-opened inputs](open.jsonl)

The authentic wire95 Default and Fishing Trap histories and the wire96 and wire97 restores and continuations match their references. Standalone C# 9 warnings-as-errors compilation and all 18 static checks passed. The full exact 1,494-case regression is running. Unity gameplay integration remains deferred. [Bindings](BINDINGS.json)
