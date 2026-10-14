Below is the finite coverage map I would use as the project’s master readiness ledger. A topic does not count as finished because it has been discussed; it advances only through the explicit states below.

## Status model

- **DISCUSSED** — scope and questions identified.
- **SOURCE-AUDITED** — authoritative/current sources located, conflicts and omissions logged, provenance retained.
- **DRAFTED** — an executable provisional rule/data implementation exists for every required case in scope.
- **REVIEWED** — adversarial/source-interface review completed and corrections dispositioned.
- **VALIDATED** — automated/reference/structural or deterministic scenario checks pass for the intended scope.
- **HUMAN-TESTED** — actually used at a table; usability/friction/results recorded.

`VALIDATED` must never be treated as numerical balance certification. `HUMAN-TESTED` also does not automatically mean balanced; it means table evidence exists.

---

# Complete finite review taxonomy

| # | Domain | Required coverage | Current known state | Authored-playtest acceptance gate |
|---|---|---|---|---|
| **0** | **Authority, provenance, versioning** | Canon hierarchy, V6 authority, V7.x evidence status, IDs, source references, superseded rules, provisional labels, change log, no destructive source edits | **REVIEWED / partially VALIDATED** | Every operational rule points to source/provisional origin; conflicting originals retained; one entrypoint identifies active playtest configuration; zero accidental canon promotion |
| **1** | **Game identity & player promise** | Genre, tone, core fantasy, intended campaign structure, tactical vs narrative emphasis, lethality, complexity, progression promise, what Decennium means to play | **DISCUSSED** | One concise design charter; every major subsystem can be tested against it; contradictions logged rather than papered over |
| **2** | **Core resolution language** | Dice/check syntax, PB, ability mods, S/M/L, advantage/disadvantage, rounding, natural 1/20, DCs, opposed checks, distances, tiles, size, line of effect, target legality, timing vocabulary | **DRAFTED / partially REVIEWED** | One source-linked glossary; every card/spell/monster can execute without inventing basic math/timing |
| **3** | **Time & action economy** | Regular turns, Actions, Bonus Actions, Reactions, free triggers, extra Actions, initiative, rounds, encounter start/end, recharge, delayed effects, simultaneous events, falling markers | **DRAFTED / REVIEWED in part** | Deterministic timing order; no recursive Action grants; initiative edge cases reproducible; falling bridge incorporated as explicitly provisional |
| **4** | **Character creation** | Ancestry, background, stats, stat generation, HP, saves, proficiencies, skills, languages, starting gear, starting money/resources, spell choices, class entry | **DISCUSSED; source inspection required** | Blank sheet → legal level-1 character for every supported ancestry/background/class combination without Director invention |
| **5** | **Character sheet/data model** | Identity, stats, defenses, skills, resources, RP/RC/BG/etc., spells, conditions, concentration, companion state, equipment, wounds, cooldowns, path choices | **DISCUSSED** | Every active game state has one explicit field and ownership rule; paper and digital forms encode same state |
| **6** | **Advancement** | XP/milestone method, class levels, Base/Arch/Hero transition, ASI/feat gates, automatic vs selected features, retraining, dead/retired replacement PCs | **DRAFTED for classes; broader integration open** | Level 1→20 advancement script produces no duplicate grants, illegal prerequisites or stage leakage |
| **7** | **Multiclassing** | Whether supported, entry requirements, PB, HP, proficiencies, class-level gates, shared resources, spell access, ASIs, subclasses/paths, capstones | **UNRESOLVED AUTHOR/SOURCE DECISION** | Either explicitly unsupported, or fully operational with generated legal builds and no gate/resource exploits |
| **8** | **Respec/retraining/transformation** | Feature replacement, spell replacement, path change, Oath fall/restoration, permanent transformations, retraining cost/timing | **PARTIALLY DRAFTED** | Every allowed change states what persists, what resets, cost, timing and legality; no resource refill exploit |
| **9** | **17 class families** | Base features, Arch, Hero, path identities, resources, advancement, examples, source mapping | **VALIDATED structurally; REVIEWED; not HUMAN-TESTED as a suite** | All 17 map source→operational rules; no stage leakage; validator PASS; representative table use |
| **10** | **Class specializations** | Oaths, Mysteries/Curses, Circles, Hero paths, mutation trees, summons, class-specific spell systems | **DRAFTED/REVIEWED; many structurally VALIDATED** | Each specialization is complete, mutually legal, source-traceable and has an executable level progression |
| **11** | **Ordinary spell identity/access** | 848 IDs, 936 Core placements, school/rank per class, aliases, blocked conflicts, spellbook/preparation/known lists | **72 REVIEWED; 776 pending** | All 848 accounted; every placement mapped; aliases adjudicated or blocked; no spell access by affordability alone |
| **12** | **Ordinary spell mechanics** | Activation, range, components, targets, duration, concentration, attack/save, success result, effect, scaling, limitations | **72 DRAFTED/REVIEWED** | Every active spell has complete operational fields; unfinished entries remain unusable, not half-runnable |
| **13** | **RP / Dissonance / Refrain / rituals** | Rank prices, class-specific ranks, Retune, strain states, Refrain, class cadence exceptions, long/short-rest recovery, ritual cost/time/components | **DRAFTED/REVIEWED provisionally** | One active test configuration; no simultaneous historical Burn/fizzle system; every class-specific exception explicit |
| **14** | **Feats** | All 335: prerequisites, level gates, ASI replacement, class/path requirements, stacking, actions, resources, spell assumptions | **DISCUSSED; not yet reviewed here** | 335-source ledger; each feat operational or blocked; no obsolete engine references; acquisition validator |
| **15** | **Skills & noncombat checks** | Skill list, proficiency/expertise, passive checks, group checks, assistance, tool checks, investigation/social/exploration usage | **SOURCE INSPECTION REQUIRED** | Every common declared task has a known resolution method or explicit Director adjudication boundary |
| **16** | **Conditions** | Core conditions plus Bleed/Burn/Shaken/etc.; application, stacking, ending, immunities, repeats | **Glossary exists; integration PARTLY REVIEWED** | Every referenced condition resolves to one active definition; historical variants preserved but not co-executable |
| **17** | **Combat core** | Initiative, attack actions, Extra Attack, melee/ranged, crits, opportunity attacks, movement, disengage, reactions, saves, area attacks | **DRAFTED in shared integration; full source audit still needed** | Complete legal turn examples for martial, caster, summon, boss, downed creature; no undefined basic combat operation |
| **18** | **Control & action denial** | Grapple, Restrained, root, Stunned, Charmed, Frightened, silence, reaction denial, hard-denial ceiling | **REVIEWED provisionally** | All control has save/escape/end timing; hard-denial ledger applies consistently across classes/spells/companions |
| **19** | **Stealth, perception & vision** | Hide, concealment, invisibility, darkness, light, darkvision, blindsight if present, sound, detection, passive perception | **PARTLY DRAFTED** | Hidden/invisible state transitions and targeting consequences are deterministic; no “invisible = untargetable” ambiguity |
| **20** | **Cover & line rules** | Half/three-quarter/full cover, line of sight/effect, firing through creatures, walls, spell areas, terrain obstruction | **PARTLY DRAFTED** | One geometry procedure applies to attacks, spells, areas and detection |
| **21** | **Movement & positioning** | Speed, Dash, difficult terrain, crawling, climbing, swimming, jumping, forced movement, teleporting, flight, falling | **PARTLY REVIEWED** | Every mode has exact timing/cost; provisional Falling bridge logged; flight-loss interactions tested |
| **22** | **Hazards/environment** | Fire, cold, heat, drowning, suffocation, weather, poison, disease, traps, unstable terrain, darkness, falls, environmental damage | **DISCUSSED / source audit needed** | Environment chapter supports expedition and combat without improvised core math |
| **23** | **HP, Downed, death & Wounds** | 0 HP, death saves/checks, stabilization, massive damage if any, Wounds, death state, corpses, recovery | **PARTLY REFERENCED; SOURCE AUDIT REQUIRED** | Exact state machine from healthy→Downed→stable/dead→recovery |
| **24** | **Healing & resurrection** | Real HP, temp HP, healing dice, pool healing, resurrection eligibility/window/cost, body/soul requirements, Wounds | **PARTLY DRAFTED by integrations** | No unlimited healing; resurrection deterministic; death cannot be erased by ambiguous card wording |
| **25** | **Weapons** | Damage, type, properties, hands, reach, range, ammunition, reload, finesse, light, polearms, improvised weapons | **SOURCE INSPECTION REQUIRED** | All class weapon references resolve to exact weapon records/properties |
| **26** | **Armor/shields/defenses** | AC formula, armor categories, shield bonuses, penalties, DR, resistance, immunity, stacking | **SOURCE INSPECTION REQUIRED** | One defense calculation; no class/spell/item stacking contradiction |
| **27** | **Inventory/carrying/encumbrance** | Slots/weight if any, containers, hands, worn/readied gear, consumables, ammunition, loot burden | **MISSING FROM PRIOR HIGH-LEVEL LIST; source audit required** | Expedition gear choices have enforceable capacity/carry rules |
| **28** | **Tools, consumables & item use** | Healing items, kits, flasks, traps, scrolls/wands if any, activation, charges, crafting interfaces | **DISCUSSED** | Every item action/cost/recovery is executable and cannot bypass class resource limits |
| **29** | **Crafting system** | 687 total recipes / 433 public, recipe discovery, materials, tools, checks, time, failures, output, repair, salvage | **DISCUSSED; source inventory exists** | Every public recipe resolves all inputs/outputs; Director recipes remain segregated; zero duplication/economy loops |
| **30** | **Economy** | Currency, prices, wages, services, loot sale, rarity, markets, repair, travel costs, crafting profitability | **MISSING from prior explicit detail; needs audit** | No infinite-money path; prices and campaign-resource costs are internally usable |
| **31** | **Magic items & special equipment** | Attunement/bonding if present, charges, identification, crafting, rarity, ownership, destruction | **SOURCE INSPECTION REQUIRED** | Every public item has complete mechanical lifecycle |
| **32** | **Mounts, vehicles, siege, chases** | If present in sources: movement, riders, passengers, vehicle HP/AC, collisions, chase timing | **MISSING from prior taxonomy; check source** | Either explicitly unsupported or complete enough for sourced content |
| **33** | **Creature stat interface** | AC, HP, attacks, saves, skills, movement, traits, conditions, recharge, senses, size, tags | **Source packs exist; integration audit pending** | Every public/Director creature can execute under the same combat rules |
| **34** | **Boss/legendary interface** | Boss flag, immunities, defenses, action economy, denial interaction, phases, legendary/reaction mechanics | **KNOWN NEED; source audit pending** | Class/spell guards reference actual monster fields, not Director guesswork |
| **35** | **Summons/companions/pets** | Stat overrides, commands, shared damaging-action cap, persistence, healing, death, replacement | **DRAFTED/REVIEWED provisionally** | All summons obey one command/persistence contract unless explicit exception |
| **36** | **Encounter construction** | Difficulty methodology, party size/level assumptions, waves, terrain, objectives, bosses, retreats | **DISCUSSED** | Director can build Base/Arch/Hero encounters from explicit procedure |
| **37** | **Encounter procedures** | Start, surprise, initiative, reinforcements, morale, flee/surrender, encounter end, resource reset | **PARTLY DRAFTED** | “Encounter” cannot be player-farmed; start/end transitions deterministic |
| **38** | **Loot/reward system** | Currency, items, recipes, XP/milestone, materials, treasure tables, boss rewards | **DISCUSSED** | Rewards feed advancement/economy without invalidating campaign pacing |
| **39** | **Exploration/travel** | Distance, pace, navigation, scouting, weather, random encounters, mapping, visibility | **Existing procedures; integration audit needed** | One travel loop executes hour/day/expedition without missing checks/resources |
| **40** | **Expedition resources** | Supply, food/water, ammo, light, camp, fatigue/rest debt, pressure, encumbrance | **Existing expedition procedures; integration audit needed** | Spells/items cannot silently erase resource gameplay; all depletion/recovery exact |
| **41** | **Rest/recovery** | Short rest, long rest, interruption, safe locations, RP/class resources, Wounds, limits | **DRAFTED provisional bridge + existing source procedures** | One active recovery model with class exceptions; no rest chaining |
| **42** | **Extraction/retreat/failure** | Leaving dungeon/expedition, failed objectives, pursuit, lost characters, abandoned loot, safe return | **MISSING from prior detail; check source** | Campaign can survive failure without Director inventing consequences |
| **43** | **Haven/settlement loop** | Recovery, markets, crafting, training, contacts, faction actions, upgrades | **Existing Haven procedures; integration audit needed** | Expedition→Haven→next expedition loop fully executable |
| **44** | **Downtime** | Crafting, training, research, healing, faction work, employment, travel, respec if allowed | **DISCUSSED / source exists unknown** | Every supported downtime action has time, cost, check, output |
| **45** | **Social rules** | NPC attitude, persuasion, intimidation, deception, bargaining, reputation, social conflict | **SOURCE INSPECTION REQUIRED** | Social outcomes preserve agency and give Directors usable resolution bounds |
| **46** | **Languages/literacy/communication** | Starting languages, learning, scripts, translation, magical communication | **SOURCE INSPECTION REQUIRED** | Character creation and spell interactions share one language model |
| **47** | **World history & chronology** | Historical eras, current date, Decennium origin/cycle, key wars/events | **DISCUSSED only from this notebook** | One contradiction-audited chronology |
| **48** | **Geography & travel map** | Regions, settlements, distances, routes, hazards, borders | **SOURCE INSPECTION REQUIRED** | Locations referenced by adventures/campaign procedures exist consistently |
| **49** | **Factions & politics** | Goals, resources, relationships, ranks, reputation, conflict clocks | **SOURCE INSPECTION REQUIRED** | Director and public knowledge separated; faction behavior supports campaign play |
| **50** | **Religion/cosmology** | Gods/powers, faiths, afterlife, divine magic implications, public vs secret truth | **SOURCE INSPECTION REQUIRED** | Cleric/Paladin/Oracle lore and resurrection rules do not contradict setting truth |
| **51** | **Decennial cycle** | Exact cycle mechanics, world changes, timing, escalation, resets/non-resets | **KNOWN CORE TOPIC; not audited here** | Cycle has explicit campaign procedure and interfaces with advancement/world state |
| **52** | **Late-game/endings** | Level-20 play, endgame threats, Decennium resolution, success/failure endings, postgame | **MISSING from mechanical audit** | Campaign has intentional terminal states rather than endless extrapolation |
| **53** | **Director authority & adjudication** | What Director decides, what rules decide, uncertainty, hidden DCs, exceptions, fiat boundaries | **PARTLY DRAFTED** | Players know predictable rule surface; Director knows permitted discretion |
| **54** | **Director secrets/data separation** | Secret creatures, plot truths, hidden items, encounter notes, public leakage | **KNOWN GAP** | Automated build finds zero Director-only leakage into public package |
| **55** | **Adventure design procedure** | Hooks, objectives, encounter mix, clues, pacing, rests, rewards, failure paths, bosses | **DISCUSSED** | Director can author an adventure from a repeatable checklist |
| **56** | **Campaign design procedure** | Arcs, clocks, faction movement, Decennial advancement, milestones, world-state changes | **DISCUSSED** | Multi-session campaign can evolve mechanically without ad hoc tracking |
| **57** | **Random tables/procedural content** | Encounter tables, loot, weather, rumors, travel events if sources use them | **MISSING from prior list; source-check** | Every public table has ranges/results and no unresolved references |
| **58** | **Session zero & table contract** | Expectations, tone, character fit, PvP, attendance, lethality, content boundaries | **DISCUSSED as need only** | One concise procedure usable before play |
| **59** | **Accessibility** | Color independence, readable typography, table complexity, cognitive load, physical/digital accessibility | **NOT YET AUDITED** | Core references usable without color-only cues; critical rules available in compact form |
| **60** | **Onboarding/quickstart** | First character, first turn, first encounter, spellcasting, rests, advancement | **Quickstart exists; not yet source-audited here** | New group can complete a starter session without owner intervention |
| **61** | **Reference sheets/indexes** | Conditions, Actions, spellcasting, travel, Director procedures, class resource summaries | **PARTIAL** | Every frequently queried mechanic reachable in ≤2 lookups |
| **62** | **Examples & worked turns** | Creation, combat, casting, companions, travel, crafting, death, advancement | **Class examples exist; game-wide examples incomplete** | Examples all legal under final playtest rules and validator fixtures |
| **63** | **Companion persistence/state parity** | Paper ↔ digital, HP/resources/cooldowns, summons, campaign state, save/load/migrations | **KNOWN NEED** | Reloading/reopening cannot alter mechanical state; schema migration tested |
| **64** | **Data schemas/IDs/migrations** | Stable IDs, aliases, deprecation, source references, version migration | **PARTIALLY VALIDATED** | No duplicate canonical IDs; old saves/data can map or explicitly fail safely |
| **65** | **Public/Director build packaging** | Separate datasets, references, exports, manifests, player-only docs | **KNOWN GAP** | Zero secret leakage; zero broken public references |
| **66** | **Editing consistency** | Terminology, capitalization, units, timing phrases, condition names, cross references | **ONGOING** | Lint pass and terminology dictionary produce zero unresolved style/mechanical ambiguities |
| **67** | **Layout/publication structure** | Book order, navigation, page references, tables, callouts, glossary, appendices | **NOT YET READY** | Complete playtest books generate without missing sections/references |
| **68** | **Legal/IP/credits/licensing** | Third-party assets, fonts, art, names, licenses, contributor credits | **MISSING from prior list; required before publication** | Rights/credits ledger complete; no unlicensed publication dependency |
| **69** | **Machine verification** | Source counts, acquisition, prerequisites, ranks, resources, action limits, concentration, copies, summons, public leaks | **Class validation strong; game-wide incomplete** | Full deterministic suite passes with reproducible failures |
| **70** | **Generated scenario testing** | Legal build generation, random turns, cross-system combinations, resource invariants | **PARTIAL for classes** | Large sampled suite finds no negative resources, illegal gates, loops, double concentration, etc. |
| **71** | **Human rules playtest** | Base, Arch, Hero, mixed parties, new players, experienced players, Directors | **NOT COMPLETE** | Recorded sessions at all stages; friction and ambiguity issues dispositioned |
| **72** | **Human numerical/balance playtest** | DPR, survivability, healing, control, resource pacing, encounter difficulty, build diversity | **NOT CLAIMED** | Sufficient table evidence to make balance claims; separate from structural correctness |
| **73** | **Campaign-duration playtest** | Multi-session advancement, rests, economy, crafting, Decennial cycle, long-term state | **NOT COMPLETE** | At least one sustained campaign validates the loop rather than isolated combats |
| **74** | **Release candidate/errata process** | Version freeze, known issues, errata, migration, feedback intake | **FUTURE** | Playtest candidate versioned, reproducible, with known-issues ledger |

That is the finite taxonomy I would freeze. New discoveries should be assigned to one of these categories rather than creating endless new workstreams.

---

# Known project constraints from the notebook

These are things I would treat as established project constraints unless local evidence or the owner explicitly supersedes them.

### Canon/source boundaries

- The **approved V6 books** and **Core Systems Known Descent V2** remain domain authorities.
- V7/V7.1/V7.2 material is not silently promoted; **V7.2 calibration is historical testing evidence**.
- Original source material is preserved. The working policy has consistently been that source wording/provenance is retained and playtest completion is marked as provisional.
- Current class and spell work belongs in the ReviewBible/playtest layer, not as an undeclared rewrite of approved canon.

### Progression

The class-stage structure is fixed for this playtest:

- **Base: levels 1–2**
- **Arch: levels 3–9**
- **Hero: levels 10–20**

Druid, Oracle and Paladin have explicit exceptional schedules, but they still respect the stage concept.

The 17 protected class identities are:

**Bard, Cleric, Crimson Agent, Dragoon, Druid, Mage, Mirrorsage, Monk, Oracle, Paladin, Ranger, Shaman, Soldier, Thief, Tinker, Warrior, Wizard.**

Future cross-system normalization should not flatten those protected engines into one generic resource/caster chassis.

### Shared provisional integration constraints already developed

These are **active playtest decisions**, not necessarily approved-book canon:

- `S = 1/2/3/4` at class levels `1/5/11/17`.
- Effect `M = max(1, class ability modifier)` while attacks/DCs use the actual modifier.
- One extra full Action per creature per round.
- An extra Action cannot recursively grant another Action/Bonus Action/Reaction.
- One concentration burden unless a narrowly explicit exception exists.
- Hard whole-turn denial is capped once per source-character/target/encounter across that character's class features, spells and companions.
- Copies/echoes do not reproduce costs, resource generation, proc chains, conditions or further copies unless explicitly allowed.
- Permanent healing must consume a finite resource.
- Trivial targets, allies, summons, helpless captives and corpse reuse do not generate class resources.
- Temporary HP do not stack.
- Redirected damage cannot recursively redirect or generate resources.
- Summons/companions use a shared command/damaging-action budget unless explicitly overridden.
- The recently agreed **Falling bridge** is explicitly new provisional mechanics, not recovered canon.

### Spell-specific current state

- **848 ordinary spell IDs** are the source-accounting target.
- Core V2 contains additional placement-level spell evidence, including multiple school/rank placements for some IDs.
- **72** have gone through the current individual operational pass.
- **776 remain blocked/unfinished** and must not inherit assumptions automatically.
- Same-name class features/spells remain separate acquisitions.
- Class-specific spell rank/access controls legality.
- Current pilot uses Core V2 rank cost values with Dissonance/Refrain integration.
- Oracle remains an RC engine rather than ordinary RP casting.
- Soldier and Warrior do not receive general ordinary spellcasting merely because spell data exists.

---

# Questions that should stay explicitly open for source inspection / owner decision

These should not be answered by inference.

1. **Multiclassing:** supported core feature, optional experimental rule, or historical scaffolding only?
2. **Exact advancement method:** XP, milestones, or another campaign-specific mechanism?
3. **Final authoritative HP/Downed/death/Wound/resurrection state machine.**
4. **Authoritative weapon/armor/item records and defense stacking.**
5. **Full feat acquisition and interaction rules for all 335 feats.**
6. **Which of the 687 crafting recipes are Director-only versus public beyond the 433 known public entries.**
7. **Canonical economy model:** prices, wages, markets, salvage and loot conversion.
8. **Boss/legendary taxonomy and the exact flags monsters expose to class/spell control systems.**
9. **Public/Director visibility ontology already present locally, if any.**
10. **Druid/Oracle/Ranger/Mirrorsage historical chassis conflicts** already preserved in playtest notes: inspect the current approved-domain source before any canon decision rather than treating provisional reconciliations as final.
11. **Retune/recovery bridge** versus any approved gameplay recovery paragraph. Current bridge is provisional.
12. **Decennial cycle mechanics and late-game/end-state rules:** source audit needed before mechanical expansion.
13. **Whether vehicles, mounts, chases and siege rules are intended supported subsystems or merely incidental source content.**
14. **Whether social conflict has a formal subsystem or relies on ordinary skill checks plus Director adjudication.**
15. **Whether player-facing world lore intentionally contains false/incomplete information distinct from Director truth.**

---

# Dependency order to finish a coherent authored playtest candidate

This is the order I recommend—not because later subjects are less important, but because each stage needs the previous one to stop generating rework.

### Phase A — freeze interfaces

1. Authority/provenance/versioning
2. Core resolution terminology
3. Time/action/initiative
4. Conditions/control
5. HP/Downed/death/healing
6. Movement/vision/cover/environment basics
7. Character sheet state model

**Gate:** no player option should require an undefined common mechanic.

### Phase B — finish character construction

8. Character creation
9. Advancement
10. Multiclass decision
11. Respec/retraining
12. Skills/languages
13. Equipment baseline

**Gate:** Codex can build and advance legal PCs without manual correction.

### Phase C — finish player option surface

14. Classes — maintain and regression-test the existing 1,223 cards
15. Remaining 776 spells
16. 335 feats
17. Weapons/armor/items
18. Consumables
19. 687 crafting recipes
20. Economy

**Gate:** every player-selectable option is either operational or explicitly blocked.

### Phase D — finish opposition and session engine

21. Creature schema
22. Boss/legendary rules
23. Encounter building
24. Loot/rewards
25. Hazards
26. Exploration/travel
27. Expedition resources
28. Rest/recovery
29. Extraction/failure
30. Haven/downtime

**Gate:** a Director can run an expedition from departure through return without inventing core procedures.

### Phase E — finish campaign/world layer

31. History/chronology
32. Geography
33. Factions
34. Religion/cosmology
35. Social/reputation
36. Settlements
37. Decennial cycle
38. Late-game/endings
39. Campaign-state progression

**Gate:** mechanics and setting no longer contradict each other.

### Phase F — finish Director product

40. Director adjudication
41. Secret/public boundaries
42. Adventure-building method
43. Campaign-building method
44. Random/procedural tables
45. Representative Base/Arch/Hero adventures

### Phase G — finish usability/product layer

46. Session zero
47. Accessibility
48. Quickstart
49. Pregens
50. Reference sheets
51. Examples
52. Companion persistence
53. Digital state parity
54. Public/Director builds
55. Editing/indexing/layout
56. IP/credits

### Phase H — verify and test

57. Machine validation
58. Generated scenario tests
59. Human Base play
60. Human Arch play
61. Human Hero play
62. Multi-session campaign play
63. Numerical/balance iteration
64. Release candidate and errata process

The critical distinction is:

**An authored playtest candidate can be finished before numerical balance is certified.**

For that milestone, I would require every relevant subsystem through Phase G to reach at least:

**SOURCE-AUDITED → DRAFTED → REVIEWED → VALIDATED**

and label the build clearly:

**“Mechanically integrated provisional playtest candidate; human balance and publication approval not yet certified.”**

Human tests then move domains into **HUMAN-TESTED** and supply the evidence for balance decisions rather than forcing speculative tuning into the authoring pass.