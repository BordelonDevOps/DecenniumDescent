# MGT-10 episode-close implementation review

## Initial candidate held for meal-history aggregation

GPT reviewed source `32d89e7b1a0b7609f0672824fa38d39bbf950e51` and evidence `e5eef33a1635ba09c729212b946bc6c85fcf4d66` under source/API approval `4ce97c92-f7cb-4596-88f1-7a719476ad83`. Actual verdict `69acdf82-c072-47bd-8363-2888980769b1` holds acceptance for B1 only. GPT inspected the runtime, records, codec, all four focused cases, changed integration, compatibility and result reports, and traced ordinary intake. It did not execute the reproducer or run the source, Unity or the scripts. It found no additional concrete implementation blocker. [Unity Rules Engine Development](https://chatgpt.com/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

The close required a single complete intake of the full root. An interrupted intake can retain a positive debit, and a fully consumed serving can span multiple root intakes or descendant portions. GPT requires aggregating only actual terminal debits of the exact purchased root and its legitimate descendants, and retaining the complete evidence at the historical close boundary. Tests must cover interrupted and completed root work, multiple complete intakes, the supported portioned continuation, and negative active, partial and unrelated consumption. No change to ordinary eating or the historical meal profiles is required.

Codex reproduced the defect using normal commands on the exact reviewed assemblies. At time `7855/1` and revision 39 the earlier interrupted reservation had consumed 1/6 lb, the second completed reservation had consumed 1/2 lb, both claims were terminal, the root had zero remaining stock, and the actual bill was reconciled. Both query and command returned `ExpeditionCloseMealIntakeRequired`. The stored snapshot remains at the same revision with no close. [Exact pre-fix report](correction/baseline-interrupted-meal.json) · [Verifier](correction/Verify-InterruptedMealClose.ps1)

The source/API contract, earlier accepted bill and meal modules, and demonstrated bounded connected C# milestone remain in force. The current gate is the exact episode-close correction. Unity gameplay integration remains deferred.
