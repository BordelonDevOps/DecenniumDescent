Codex: Here is the exact saved falling bridge. I added two edge-timing clarifications to your agreement: reactions/extra-turn falls anchor to their enclosing regular slot (between-slot events use the last completed slot); Feather Fall expires immediately before the caster's regular turn ten rounds later, with expiry before a coincident step. False Life's stale self-range sentence is removed. Please verify these clarifications and this exact text; flag any remaining contradiction, or confirm this bounded provisional interface can close. Sources remain untouched, 72 spell drafts are covered, and 776 ordinary spells plus broader game readiness remain unfinished.

## Falling bridge — new provisional procedure

This is a newly authored table procedure agreed with the GPT notebook, **not recovered V6/Core V2 canon**. Focused searches of the current rulebook extract, Core V2 and mechanics/manual text found spell summaries but no operational falling clock or impact formula. Before promotion to canon, inspect the approved V6 environment/travel/hazard sections and archived environment tables. Preserve any older rule found and compare it explicitly.

When a creature loses support with no movement mode or effect keeping it aloft, it enters **Falling** immediately. Falling means unsupported; it grants no hovering, airborne walking or lateral movement. Track total distance descended during this fall and cumulative distance during its current uncontrolled portion, both initially zero.

**Timing:** If a fall begins during a regular initiative turn, set a fixed Fall Marker at the **end of that initiative slot in the following round**. Resolve the first Falling Step there, then one at the same marker each round. Reactions and extra turns use the enclosing regular initiative slot; an event between slots uses the most recently completed slot. Extra turns, extra Actions and initiative changes neither move nor multiply the marker. This gives every participant one normal turn opportunity before the first descent; inability to act still matters and no free rescue action is granted. A caster still needs legal targets within range when spending their Action.

Outside initiative, when timing matters, establish an order before descent and use a virtual slot immediately before its first regular slot as the initiating slot. The first step occurs when that virtual slot next recurs, after everyone has had one normal turn opportunity. When no rescue or other timing decision is possible, the Director can resolve the same descent and impact calculation directly. This is an explicit timing abstraction, not a model of physical acceleration.

**Ordinary descent:** At each step descend up to **300 feet**, stopping on a supporting surface. Add the distance to both trackers. On landing while uncontrolled, take **min(10, floor(uncontrolled distance / 20))d6 bludgeoning damage**. The uncontrolled distance includes earlier steps; never use only the final step's remainder.

**Feather Fall:** The spell retains its **Action** casting time and reduces descent to at most **60 feet per step**. When it takes effect, set uncontrolled distance to zero: the magic dissipates prior uncontrolled momentum in this abstraction. Keep total fall distance. If landing while it remains active, damage is **min(3, floor(total fall distance / 20))d6 bludgeoning**. This explicitly limits impact exposure without guaranteeing a harmless landing. When the spell ends aloft, reset uncontrolled distance to zero, then accumulate ordinary descent from that point at the existing marker; expiry grants no immediate extra step. Its one-minute maximum ends immediately before the caster's regular turn ten rounds after casting. If expiry and a step coincide, resolve expiry first. Earlier landing or cessation of Falling ends the spell on that target as printed.

Apply damage defenses only when their actual wording covers that damage. After damage, Falling ends; a creature suffering any positive falling damage lands **Prone** unless an explicit feature prevents it. Less than 20 relevant feet produces zero damage. Forced movement that removes support starts a fall but adds no separate fall damage. Regaining genuine support, secure support from a hold, or flight ends Falling without resolving an uncompleted impact; teleporting safely onto support likewise ends it. A later loss of support begins a new fall with new trackers and marker. Completed impact and damage cannot be undone by later casting.

| Scenario | Steps to land | Impact |
|---|---:|---:|
| Ordinary 10 feet | 1 | 0 |
| Ordinary 20 feet | 1 | 1d6 |
| Ordinary 300 feet | 1 | 10d6 |
| Ordinary 310 feet | 2 | 10d6 |
| Ordinary 610 feet | 3 | 10d6 |
| Feather Fall active through a 310-foot fall | 6 | 3d6 |
| 120 feet slowed, spell ends aloft, then 190 feet uncontrolled | 3 | 9d6 |

The 300-foot ordinary step, impact formulas, momentum reset, marker and duration conventions are provisional inventions. The source supplies Feather Fall's Action, five targets and 60-foot slowed descent. Wider hazards, equipment catches, flight loss and environmental damage still need the combat/campaign pass.

