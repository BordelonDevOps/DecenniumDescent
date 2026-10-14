Confirm. Your supersession is the cleaner and more internally consistent implementation.

The earlier generic-28 clauses should be preserved as historical review text but explicitly marked **superseded by the later unified family arbitration overlay**. The Core source quotations themselves remain unchanged.

I would freeze the replacement this way:

1. **Core Bleeding and Burning join the same registries as custom variants.**
   - Core Bleeding → `family.bleeding`
   - Core Burning → `family.ongoing-fire`
   - Each application keeps its source-qualified mechanical ID and source-owner stack group.
   - Namespacing never grants an extra tick.

2. **Periodic damage arbitration is unified across generic and custom records.**
   At any identical target timing marker:
   - consider every due stack group in that family;
   - choose the group with the highest expected unmitigated periodic damage;
   - tie → earliest application;
   - resolve only that group's permitted instances;
   - losing groups consume that scheduled tick and do not defer or bank it.

   I agree with **dropping DC as a damage-arbitration tie-breaker**. Cure difficulty should not determine which effect deals damage. DC remains attached to its record for ending procedures.

3. **Different timing markers remain independent.**
   A start-of-turn Bleed and an end-of-turn Core Bleeding can both resolve because they are genuinely different markers. A replacement-timing record never receives an extra generic Core tick.

4. **Bleed cures are record-aware.**
   - Medicine Action: choose one eligible Bleed record before the check; success ends that record.
   - Magical healing with positive pre-cap/pre-prohibition potential: ends **all active ordinary Bleed records** whose metadata says magical healing automatically cures them.
   - Shaman Blood Curse does not auto-end; each applicable Blood Curse record gets its own printed CON save.
   - `end one Bleed` removes one eligible record.
   - `end all Bleed` removes all records within the effect's stated scope.
   - Special-cure/protected records survive unless the remover explicitly covers them.

5. **Fire mundane extinguishing is family-wide for ordinary records.**
   One Action by the affected creature or adjacent helper, or qualifying full immersion, ends **all active `family.ongoing-fire` records marked `ordinaryExtinguishable`** on that creature.
   Source-specific exceptions survive.

6. **Burning DEX saves are per surviving record.**
   At the appropriate regular-turn endpoint, each active ongoing-fire record that still has future periodic damage remaining makes its own ending DEX save using its own DC/fallback.
   - passing one does not clear others;
   - a finite record whose final damage tick already resolved simply expires;
   - an indefinite generic Core Burning record counts as having future damage while it remains active.

7. **Generic Core records do not get privileged duplicate mechanics.**
   Registering Core Bleeding/Burning means their source damage, cure language, and indefinite/defined duration are represented as records inside the same system. There is no parallel “generic condition tick” running beside the family registry.

I would add one explicit migration statement:

> **SUPERSESSION — NEW PROVISIONAL INTEGRATION:** The unified Bleeding/ongoing-fire family registry supersedes earlier provisional implementation clauses that selected generic records separately, used ending DC as a periodic-damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one selected Burning save to clear all generic Burning. Those earlier decisions remain preserved in audit history but are inactive in the current candidate.

That gives you one coherent implementation model rather than two layers that can disagree.

Regenerating the generic reference and tests around this unified overlay is the right move.