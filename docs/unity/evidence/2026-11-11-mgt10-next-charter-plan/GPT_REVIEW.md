# MGT-10 next-charter planning implementation review

## Initial candidate held for the existing bill protocol

GPT reviewed exact source `db061611dffd0260c272528e384004c2420fdd1a` and evidence `c78f3208b0e9eae0ee57f1531b813ad06f966ec2` in reply `7dd67d17-8fed-49c2-8957-6cebd38a5b08`. GPT found groups 1–5 met in the inspected scope. Group 6 was held for one compatibility finding. [Actual review conversation](https://chatgpt.com/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

**B1.** The shared worker-eligibility predicate extraction changed the existing bill's public busy rejection and stored completion obstruction reason from `ExpeditionBillWorkerBusy` to `WorkerHasIncompatibleLabor`. The affected literals apply to schema 81 and later bill profiles. Positive legacy continuations passed and the separate busy-rejection path needed a targeted check. GPT requested restoring both bill-specific literals, keeping the shared predicate and planning-specific code, and adding an exact-code legacy regression with unchanged snapshot bytes. [Held evidence](README.md)

GPT inspected the relevant implementation changes, all seven planning case bodies, the focused and historical summaries, all seven legacy reports, the linked audits, and selected hash bindings. GPT reported no independently run C#, tests, saves, replay, hash audit or Unity checks. It selected no successor while B1 was open.

## Direct reproduction

The same verifier against the accepted schema 81 assemblies and the held candidate reaches a fully earned pending bill at `7228/1`, cures the representative and starts actual intake of the purchased serving. The finalization query and execution run at `7234/1`, revision 22, while that intake is active. Both builds start with the same snapshot bytes and reject without mutation. The accepted build returns `ExpeditionBillWorkerBusy`. The held candidate returns `WorkerHasIncompatibleLabor`. [Verifier](correction/Verify-LegacyBillBusyCode.ps1) · [Accepted schema 81 reproduction](correction/accepted-schema81-bill-busy.json) · [Held candidate reproduction](correction/held-bill-busy.json)
