# MGT-10 next-charter planning implementation review

## Initial candidate held for the existing bill protocol

GPT reviewed exact source `db061611dffd0260c272528e384004c2420fdd1a` and evidence `c78f3208b0e9eae0ee57f1531b813ad06f966ec2` in reply `7dd67d17-8fed-49c2-8957-6cebd38a5b08`. GPT found groups 1–5 met in the inspected scope. Group 6 was held for one compatibility finding. [Actual review conversation](https://chatgpt.com/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

**B1.** The shared worker-eligibility predicate extraction changed the existing bill's public busy rejection and stored completion obstruction reason from `ExpeditionBillWorkerBusy` to `WorkerHasIncompatibleLabor`. The affected literals apply to schema 81 and later bill profiles. Positive legacy continuations passed and the separate busy-rejection path needed a targeted check. GPT requested restoring both bill-specific literals, keeping the shared predicate and planning-specific code, and adding an exact-code legacy regression with unchanged snapshot bytes. [Held evidence](README.md)

GPT inspected the relevant implementation changes, all seven planning case bodies, the focused and historical summaries, all seven legacy reports, the linked audits, and selected hash bindings. GPT reported no independently run C#, tests, saves, replay, hash audit or Unity checks. It selected no successor while B1 was open.

## Direct reproduction

The same verifier against the accepted schema 81 assemblies and the held candidate reaches a fully earned pending bill at `7228/1`, cures the representative and starts actual intake of the purchased serving. The finalization query and execution run at `7234/1`, revision 22, while that intake is active. Both builds start with the same snapshot bytes and reject without mutation. The accepted build returns `ExpeditionBillWorkerBusy`. The held candidate returns `WorkerHasIncompatibleLabor`. [Verifier](correction/Verify-LegacyBillBusyCode.ps1) · [Accepted schema 81 reproduction](correction/accepted-schema81-bill-busy.json) · [Held candidate reproduction](correction/held-bill-busy.json)

## Corrected schema 83 accepted

GPT accepted exact correction `79580b2e44c9ec603d4385d9b32687602a05b56e` and evidence `458978879ab76d74a875d37c58060c2ddf87eac9` in reply `6dc19c50-4a43-4ea8-94f3-452e18811390`. B1 closed and all six bounded groups were met. GPT checked both restored bill-specific values in the diff, the new legacy regression, the direct verifier and three reports, all eight focused results, the historical and compilation summaries, all package checks, all seven legacy reports, two planning audits and selected bindings. GPT distinguished the executed query/rejection reproduction from the source-inspected stored reason and independently executed no C#, script, save restore, replay, hash audit or Unity step. [Actual review](https://chatgpt.com/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c) · [Correction evidence](correction/README.md)

GPT selected one prospective charter-acceptance decision for source/API review under MGT-10's mapped dependencies. Codex checked the dependency map and agrees with that order. The approved planning scope remains conditional and does not grant charter acceptance or departure. The successor's agreement terms, authority and readiness prerequisites require their own ruling. [Successor source/API packet](../2026-11-11-mgt10-next-charter-acceptance/SOURCE_API_REVIEW.md)
