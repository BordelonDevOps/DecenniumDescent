# Repeating heavy crossbow ammunition model

**Status: TEST_ONLY source-bound immutable magazine state.** Code commit: `cd8f14fa7edefd3208c4cf8c63722e17c06cef0d`, branch `Engine`. This models the authored Repeating 5 ammunition transfer and spending rules only. It does not integrate the required reload Action with a tactical turn, add magazine state to a saved combat, or authorize a ranged attack.

## Source rules

The exact candidate and procedure are pinned at source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`; see [SOURCE_BINDINGS.json](evidence/2026-11-04-repeating-crossbow/SOURCE_BINDINGS.json).

- The authored Repeating heavy crossbow has a five-bolt internal magazine and replaces Loading.
- Each attack spends one bolt, regardless of hit outcome.
- An Action with an appropriate free loading hand loads up to five actually carried bolts. Capacity limits how many fit; no new bolts are created.
- There is no spare-magazine multiplication, free refill or sixth shot.
- The Soldier kit provides 20 actual crossbow bolts, but its repeating magazine starts empty.

## Implemented boundary

`RepeatingFiveMagazine` is immutable and TEST_ONLY. It stores zero through five loaded bolts, spends one for each legal attack attempt, and cannot fire while empty. Its reload result moves only real carried bolts into remaining magazine capacity. A missing free loading hand, empty carried stock, or full magazine produces no transfer.

The pure model does not spend the reload Action. The tactical command that invokes a successful reload must validate and charge that Action separately. The model also does not own bolt lot identity, custody, equipment hands, inventory reservations, combat persistence, or attack resolution.

Seven new named cases bring the shared headless suite to **1005/1005**; static package checks pass **14/14**. The current combined evidence is [here](evidence/2026-11-04-repeating-crossbow). This does not complete ranged combat or Soldier Overwatch.
