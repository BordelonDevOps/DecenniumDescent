# Exact recovered-model deadline sources

## Ordinary Ready

Full file: `sources/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`. SHA256 `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6`.

```text
L97: ## Ready
L98: 
L99: Spend an Action to declare a perceivable trigger and one legal Action-time action or movement. It expires next regular own-turn start. **NEW:** only one pending Ready per creature; replacing it loses the prior setup and any paid held-spell costs. No Bonus Action/Reaction ability, long ritual or multi-minute activity can be prepared by generic Ready.
L100: 
L101: The trigger happens first, then the readied response immediately follows before later events, unless a specific effect explicitly interrupts. On release spend the normal Reaction and recheck target, range, sight/perception, line of effect, ammunition and other prerequisites. An invalid or declined occurrence spends no release resource; the Ready can wait for another valid occurrence before expiry. This does not undo setup costs. Once released, it is consumed.
L102: 
L103: For ordinary nonspell actions, feature/ammunition costs are paid on release unless text charges setup. A readied **Attack Action** gets its legally available ordinary attack count; a feature limited to your own turn does not thereby work off-turn. Core Overwatch is explicitly one ranged attack, not that full Attack Action and not Soldier's distinct engine.
L104: 
L105: A readied spell is actually **cast at preparation**: choose spell/mode, verify legality, pay RP/material/other costs, provide components, resolve Dissonance/Refrain and cast-trigger effects once. Counterspell/cast-interruption opportunity occurs then, not again at release. Every held spell requires concentration, even ordinarily non-concentration spells; incompatible prior concentration ends. Lost concentration loses the held spell and costs. NEW: select the legal target/area point at release and recheck legality without repaying. At release the hold continues as ordinary spell concentration if required, otherwise ends after resolution. Expired/replaced/countered held spells do not refund paid costs.
L106: 
L107: Ready movement grants a separate current-Speed budget on release, pays terrain costs and can provoke ordinary opportunity attacks. It grants no extra Action, Bonus Action or interaction.
```

The supplied current branch is `MODEL.json` → `/currentVectors/2/independentBranches/0`. Its actual cadence is55/61, preparation56.1, Meta expiry60.5 and release60.9. Six original62 values conflict with this deadline; the recovered MODEL already corrects them to61. This delivery copies those bytes, rather than making a new selection.

## Scope of the independent boundary diagnostic

The state after the existing Meta expiry is reused as a frozen paid input. The actual complete actor profiles, spell/mode, source provenance and supplied positive RNG remain available in the full case. At61 and61.1 the diagnostic only proves hold expiry; it does not simulate the regular START or grant refreshed budgets. Those overdue phase fields are explicitly frozen diagnostic inputs, not an alleged live world snapshot.

## Historical reports

The preserved original request and completed reply are in `history/recovery_input/evidence/`. The historical reply's703/797 checks and172 tests are reported history only; they were not reproduced here, and no original Return03 ZIP is claimed available. New recovery verification and boundary diagnostics have their own reports.
