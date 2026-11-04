# Supply cache prototype decisions

Status: TEST_ONLY, provisional implementation on `Engine`, 2026-11-04. This increment adds one authored cache path to the shared C# simulation. It does not add general container rules, lock content, discovery, traps, destruction, or release-approved rules.

The owner delegated unresolved engine decisions to Codex and **Unity Rules Engine Development** consensus and authorized proceeding when both agree. The preceding GPT guidance for this bounded slice proposed a fixed visible cache, existing ration and waterskin stock, a physical key or actual thieves' tools, separate opening, and a save-resumable explore-to-retrieval loop. The delegated consensus adopted the following new provisional execution details; these values are not recovered source text:

- An exploration key or pick attempt occupies six active seconds. It spends the interval Action when it starts, resolves once at completion after same-time automatic events, and rechecks actor capability, reach, hands and the physical credential. Interruption retains elapsed time and the paid Action but makes no check or lock progress. Failed pick attempts leave the lock unchanged and retries pay the full cost again.
- Exploration opening is a separate one-active-second closure interaction. Tactical unlocking is a regular Action with no exploration seconds. Tactical opening and physical retrieval use the ordinary-interaction allowance; a second tactical interaction spends the interval Action.
- Command receipts, attempt records, finite lot history, stock contents and condition-aware check results persist in schema19. Old schemas retain their existing state format.

## Source-backed procedure

- `EQUIPMENT_ITEM_PROCEDURES.md:53`: an ordinary lock opens with a key and Action, or actual thieves' tools and a DEX check against DC15. Training is not required to attempt the tool check; relevant training is required to add proficiency bonus.
- `CORE_RESOLUTION_PLAYTEST.md:29`: task/tool checks use four degrees and natural 1/20 shift one degree. When the printed procedure has only success/failure, collapse the two upper degrees to success and the two lower degrees to failure. No extra critical consequence is added. Implementation calls `PlaytestRolls.TaskCheck` before reading its binary success result.
- `CONDITIONS_PLAYTEST.md:115, 536-544`: Blinded automatically fails checks that require sight; Poisoned imposes disadvantage on ability checks. The fixture states that this cache's tool-picking task requires sight. Key use is not a check.
- `CORE_RESOLUTION_PLAYTEST.md:79-83`: Fine-Motor Trauma penalizes tool checks and DEX checks primarily manipulating a lock/device; Exertion Trauma penalizes STR/DEX ability checks. Only the strongest applicable Injury penalty applies once. The pick modifier includes the linked Injury calculation.
- `INVENTORY_RULE_DECISIONS.md:A`: ordinary handling is a separate interaction; opening a closure is distinct, and the second tactical ordinary interaction costs an Action.
- `EQUIPMENT_SOURCE_BINDINGS.md:303, 321, 369` and `EQUIPMENT_ACQUISITION_PLAYTEST.md:142, 149-151`: one-day ration bundle weighs2lb; a four-pint waterskin weighs1lb empty plus1lb per pint of water; thieves' tools weigh1lb; a chest accepts up to300lb and12 cubic feet. These values do not infer the cache contents' volume or general container fit.

## Authored fixture facts and limits

`SupplyCacheFixture` supplies one stationary, already-discovered chest at grid coordinate (1,2), owned by the controlled hero. It begins locked and closed, with the existing2lb ration lot and an actual waterskin containing four pints. The fixture asserts fit for these exact items; it does not compute arbitrary item volume. There are no traps, hidden contents, other locks, or forced-entry rules. Each credential is a separate physical record held by the hero. The default full-loop fixture starts with thieves' tools; the physical-key route is exercised separately.

The source tables do not give the ordinary key a mass. While a key is carried, `CarriedBurden` returns unknown mass/Load and any subsequent carrying-capacity decision fails closed as `CarryingCapacityNotEstablished`. The end-to-end retrieval fixture does not carry a key, and no zero-weight default is invented. The source-backed one-pound thieves' tools mass is included in the default burden.

The cache owner and the actual credential owner need host inventory grants. The command derives these claims from state before duplicate-receipt handling, so revoked access blocks a duplicate retry. Authority remains host-owned; command payloads do not grant it.

The initial cache is TEST_ONLY, not a general quest, encounter, loot, equipment acquisition or inventory template. The fixture's static position, owner, discovered state, contents, credential possession and sight requirement must be replaced by authored world facts in a production ruleset. There is no rule promotion or Unity integration here.

## Implementation and coverage

The implementation lives in `engine/com.decennium.foundation/Runtime/Core/SupplyCacheRecords.cs`, `Runtime/Persistence/SupplyCacheCodec.cs`, and the gated LabModel partial `Laboratory/Model/SharedSupplyCache.cs`. `SharedWorldCombatPolicy` routes tactical inventory operations through the shared WorldInterval interaction ledger. The cases are registered through `Tests/EditMode/SupplyCacheCases.cs`.

Coverage includes approach, closed access, key and tools paths, grants and revoked duplicate grants, staged progress, same-time incapacity interruption, Dazed Action prevention, Poisoned disadvantage, Fine-Motor penalty, Blinded sight failure, separate opening, finite ration/water retrieval, custody and provenance, intake, save/load, key-mass uncertainty, tactical interaction/action spending, tactical incapacity rejection, and the schema14 gate.

This slice does not complete general carrying equipment, container volume, key-weight data, general lock/content authoring, tactical intake, Unity compilation, or the full engine.
