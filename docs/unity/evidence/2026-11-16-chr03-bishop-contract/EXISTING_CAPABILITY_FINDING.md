# Existing provisioning and rest capability investigation

**Historical capability finding; proposed prerequisite decision superseded by actual timing review.** Response `a8da8b2d-23e4-5e6c-b9e1-f1139f98a173` required testing earlier existing rests first. That finite route now executes through the actual wire111 encounter and surviving third-rest continuation: [survival amendment](SURVIVAL_AMENDMENT.md). The admission gaps below remain real, but are not unavoidable prerequisites for this bounded route. Runtime awaits actual amendment review.


This is diagnostic execution of accepted, unchanged gameplay `6d840c4dfce268115904ea0dda6b475450f7be6f`, using its frozen assemblies and the authentic wire110 `cleric-advanced.ddsave`. It is not Bishop implementation, a new regression run or proof that all possible routes fail. Actual contract review `9730ae44-9e01-5291-a4b2-d3515fedf2f7` requested this investigation. Codex agrees with its hold.

## Executed stock access

The definitive `access-at-site` run has 45 public inputs and 45 responses. All three positioning steps commit: the companion pays to reach (2,3), adjacent to the existing clean pool at (3,3); the hero then pays east and south to the now-vacant berth at (1,3). At the respective actual positions, nine requested operations return the intentionally bounded public `Unavailable`. Each request has byte-identical canonical saves immediately before and after it:

| Actor and request | Target / quantity | Source boundary inspected |
| --- | --- | --- |
| Companion StartWaterFill | clean-pool, 4 pints into companion-skin | Connected session does not admit StartWaterFill |
| Companion StartIntake | clean-pool, 4 pints | Ground pool lacks ready vessel custody |
| Companion HandleInventory | clean-pool, 4 pints | Connected handling only admits selected cache pickup |
| Companion StartIntake | water-pints, 8 pints | Crop resource has NutritionKind.None |
| Companion StartWaterFill | water-pints, 4 pints into companion-skin | Connected fill admission absent; crop record also lacks nutritional water qualification |
| Companion HandlePortableEquipment | clean-pool, 1 item | Pool is not declared portable equipment |
| Hero BeginRest | cleric-long-rest-berth | Connected session does not admit ordinary BeginRest |
| Hero BeginLongRest | cleric-long-rest-berth | Connected Long Rest is explicitly companion-only |
| Hero ScheduleRestWatch | day.1 | Connected session does not admit scheduling |

The public result does not expose private resolver failure codes. The source explanations above are inspection findings, not extra diagnostics emitted by the console. Ordinary rest also has an explicit inner `s.ConnectedClericLongRest` rejection, `UseSourceBoundLongRestCommand`; exposing the adapter alone would not suffice. Two preliminary access runs are retained: the first omitted `walk` on the companion step; the second attempted a blocked hero edge. Neither establishes the definitive positioning claim. The final run corrects both and retains all failed attempts rather than rewriting them.

## Actual intake and boundary consequences

The separate `one-day` run uses 40 public inputs, all with the expected successful responses. It branches from genuine earned Cleric2 at56720.5, hero16/26HP and companion8/13HP. It consumes only existing hero-owned stock:

| Intake | Amount | Start | Completion |
| --- | --- | --- | --- |
| TEST_ONLY.pack-rations, already carried/ready | 2 pounds | 56720.5 | 58520.5 |
| TEST_ONLY.ready-water, ready custody | 4 pints | 58520.5 | 58760.5 |
| TEST_ONLY.pack-water, inside carried pack-skin | 4 pints | 58760.5 | 59000.5 |

The companion begins its full rest at57600 while the hero eats; it completes Eligible at86400. The daily ledger records the hero's actual2-pound/8-pint intake and **no day0 shortfall**. The companion retains its historical2/3-pound meal and no water, and its own shortfall. A real paid Guidance and Healing Rite follow; the Rite heals the genuine hero injury to26HP. Second and third companion rests complete Eligible at172800 and259200. No free supplies, clocks, balances or life states are injected.

The hero still dies at259200: two remaining daily shortfalls plus the four actual unpaid/missed debt gains reach6. This differs from the original unprovisioned run, where death occurs before the final provisioning gain. The companion survives13HP and can lawfully cast own Guidance, then Detect, and complete a paid edge; **those successful solo actions do not satisfy the living-party contract**. This is existing Cleric2 execution, with no new encounter, level3, Invocation, Aura or Dispel.

The existing accessible8 pints fully fund only one hero day. The32-pint pool is finite nutritional water but the connected interface has no admitted filling path. The512-pint crop stock is not ordinary nutritional water. The separate contaminated pint needs actual paid Purify and still cannot by itself supply another8-pint day; no purification, mixing or conversion is assumed here. Available ration stock does not compensate for missing water.

## Decision requested from GPT

The existing public route has a concrete admission gap. Codex proposes reviewing a **bounded ordinary-rest integration for the hero**, reusing the existing RestIntervals, Watch/Debt/strain clock and persistence, as the preferred prerequisite to the Bishop attempt. The already declared safe berth and existing ordinary BeginRest procedure are a candidate, not new approved authority. The connected contract must preserve its one-occupant limit, actual geometry and work, elapsed pressure, interruption, debt clearing, recovery choices and historical saves. The inner source-bound rejection requires explicit versioned integration, not merely a new adapter switch. The source/API review must determine whether the proposed rest also necessarily entails full character Long Rest benefits; neither omitting required HP/Hit Dice/class consequences nor silently granting them is approved by this proposal. Cleric RP cannot be granted to the hero.

Candidate sequencing for source/API review: retain the companion's first rest57600–86400, actual care/departure and earned advancement; pay to vacate the berth, let the hero complete a full ordinary rest before its144000 deadline, then vacate it for the companion's144000–172800 funding rest. After the genuine post-recovery encounter, a further hero rest before230400 could precede the companion's230400–259200 rest. Every arrival, start, occupancy, deadline and post-combat completion must be proved; these are not executed hero-rest outcomes. Provisioning shortfalls remain unless actually supplied. No new map edge or prerequisite implementation is yet approved.

Alternatively, GPT may prefer the existing finite-water filling/intake integration if its complete custody, carrying, two-hand work, transfer and portable-history obligations form a smaller lawful dependency. Neither path may be implemented before actual review establishes the next gate. The core Bishop mechanics remain as reviewed, with its survival amendment outstanding.

## Retention and verification

[RESULTS.json](access-probe/RESULTS.json) records all four runs, public responses, pressure ledgers, canonical rejection pairs and the archive index. [EXECUTION.zip](access-probe/EXECUTION.zip) preserves75 exact members /6,942,560 expanded bytes, including raw inputs/outputs, canonical saves and the diagnostic input builders. Every extracted member was byte-hashed against its retained index; ZIP integrity passes. [SOURCE_BINDINGS.json](access-probe/SOURCE_BINDINGS.json) pins11 further API/source/input blobs. Accepted assembly identities remain bound by [the earlier probe](pressure-probe/bindings.json). The83-pin source audit was rerun successfully, with engine diff still empty. No new compilation or full regression was performed.

Storage/Support stay on hold; Unity remains deferred; the full C# gameplay simulation is unfinished.
