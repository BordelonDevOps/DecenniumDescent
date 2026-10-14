# Source-qualified control states

**REVIEWED / reference-VALIDATED — supplied scope only.** This guide binds the supplied 219 source passages (179 initial candidates and 40 supplemental cards). It does not claim a complete semantic audit of every class, spell, creature or item, and does not close DD16 or DD18. Original source objects remain unchanged. NEW below marks an integration decision, not text recovered from a historical book.

Use this with [Core conditions](CONDITIONS_PLAYTEST.md), [custom riders](CUSTOM_CONDITION_BINDINGS.md), [combat timing](COMBAT_ACTION_PLAYTEST.md), [Strain](STRAIN_PLAYTEST.md), [source bindings](CONTROL_SOURCE_BINDINGS.md), and the [coverage ledger](CONTROL_STATE_COVERAGE.md). Exact structured records are in `data/playtest/control_state_bindings.json`. The source procedure supplies its costs, application triggers, target eligibility, saves, frequency, concentration and endings; a component ID alone grants nothing. Alternative modes never apply together merely because both IDs appear in a binding.

## Records, clocks and precedence

Each application records its identity, exact source, owner character, target, selected mode/components, application order, recorded source DC, deadline/marker, concentration or attachment relationship, remaining uses, and applicable immunity/suppression. Display names never create conditions or prerequisites. An owner's mark cannot satisfy another owner's class hook. A corpse marker, map point, archived spell, intrinsic Oracle Curse and hard-denial history are distinct state types.

Explicit operative effect text controls over a less-specific summary duration field. Use preserved regular-turn markers for **next** turn and bare N-round durations as in the combat guide; an in-progress current turn is not the next turn. Unqualified next turn refers to the source; explicit its/target refers to the target. Bare hostile N rounds, including hostile marks, use N future target regular ends. Beneficial/self N rounds use source regular starts. Preserve virtual markers through initiative changes and absence. Out of initiative bare N rounds use application+6N seconds, retaining that deadline on entering initiative. Explicit source/concentration endings still apply.

**NEW current-turn bridge:** “end of that turn” or the supplied bare “end turn” effects end at the end of the actual turn containing the application event, including another creature's or an extra turn. With no current turn, use application+6 seconds. An application during end-turn resolution expires at that same end after resolving, rather than acquiring a fabricated next turn. This applies to Resonant Seed, Winter's Embrace, Frost Totem and Glue. It does not override an explicit next-turn endpoint.

The reference represents an expiry as an ordered `(seconds, phase)` marker, preserving exact rational seconds from the combat clock. Every turn-end deadline uses expiry phase 20: current actual turn, source/target next regular end, Nth future target regular end, and Balanced Elements' following target end. End-trigger application/resolution occurs at phase 10 and the next event slot at phase 30. The effect therefore remains during final end events and expires afterward at that same second. Turn-start and absolute elapsed deadlines use phase 0. Callers must choose an explicit typed deadline; bare numeric expiries are rejected. No fractional-second workaround or duplicate turn is created.

Repeat saves, ordinary duration expiry and previously reviewed periodic/recharge clocks use regular turns unless an explicit exception applies. This is **not** a global rule changing every “each turn” damage trigger. Zone entry/start application checks, repeat ending saves and once-per-numbered-round caps are distinct events. Follow each source's actual trigger and cap; concentration alone grants no recurring application save.

## Speed arbitration

**NEW:** Keep soft flat reductions, soft fractional reductions, explicit Speed0 controls, and Core Grappled/Restrained separate. Terrain changes movement cost; it is not a Speed penalty. “Hostile soft control” means an adverse control record regardless of whether an enemy, ally or the victim applied it.

1. Determine each possessed mode's Speed after compatible ordinary bonuses and systemic flat penalties (including serum/expedition Strain, serum side effects, cargo and stances). Their existing stacking rules still apply.
2. Evaluate every unsuppressed adverse soft-control record against that **same** pre-control Speed. Flat -10 gives `max(0, Speed-10)`; half gives `floor(Speed/2)`; use the exact registered formula for other records.
3. Use the lowest result. Different slows do not add unless an expressly reviewed source grants an exception. Keep all losing records and their independent deadlines.
4. Apply separately established global multipliers such as Exhaustion's half-Speed. Apply an active Hypermutation floor as specified below.
5. An explicit Speed0 state, Core Grappled/Restrained, Exhaustion5 or another actual immobilization overrides the numeric result. An unavailable mode remains unavailable. A separate prohibition on voluntary movement is not removed by a positive Speed.

Thus -10 and half on Speed30 yield15; Exhaustion then yields7. Two -10 records yield20, not10. Serum/expedition penalties remain independent system penalties, not competing hostile slow records. A minimum attached to a penalty cannot raise existing Speed: Iron Leash Aura uses `min(preSpeed, max(5, preSpeed-10))`.

Active adverse soft controls and explicit source Speed0 controls carry `eligibility.slowed-foe`; Core Grappled/Restrained alone, Prone, cargo, terrain and Exhaustion do not. A numerically overshadowed application still qualifies. Suppressed, expired or prevented applications do not.

Same owner/target/group/exact profile refreshes without adding magnitude or shortening its remaining deadline. Different magnitude/formula profiles retain separate deadlines within a group; a weaker later application cannot erase an unexpired stronger one. Removing/suppressing one record exposes any other valid record. Paid reapplication and source caps remain required. No arithmetic Speed result grants movement: the combat guide's common spent-movement ledger still applies.

## Mage Cold and elemental extension

One owner group `mage.cold-focus:<owner>` contains passive/Bolt/Surge flat profiles and Glacier profiles. A single hit invoking both the passive and Bolt/Surge does not create duplicate penalties. The current Cold Focus passive requires positive actual cold damage from a qualifying Cold Mage spell. Bolt/Surge explicitly apply their Cold rider on a legal hit even if damage is reduced to0. Glacier's failed-save profile does not require positive damage. A successful Glacier save can still trigger the passive if it deals positive cold damage and Cold is the current Focus.

| Candidate | Ordinary result | With **Arch** Elemental Mastery |
|---|---|---|
| Cold passive, Bolt, Surge | `max(0, preSpeed-10)` | `max(0, preSpeed-15)` |
| Glacier failed save | `floor(preSpeed/2)` | **NEW** `max(0, floor(preSpeed/2)-5)` |

Evaluate candidates independently and retain the lowest. On Speed5 unmastered flat-10 beats Glacier's2. On Speed30 mastered Glacier yields10, not5. Their endpoints remain target next regular end. A later weaker candidate cannot shorten the stronger one.

Fusion/Cascade's printed -10 riders are separate non-Focus profiles and receive no Arch-Mastery upgrade. Their positive cold damage can independently trigger the passive while Cold is the currently selected Focus. Hero Elemental Mastery changes chain eligibility and off-Focus finisher permission; it grants no other Focus passive and no Arch-Mastery modifier.

**NEW Fusion gap-fill:** Fire+Cold's slow lacks a separately printed endpoint; use target next regular end, matching its Cold+Lightning sibling. Fusion's Lightning pairs retain their printed separate Reaction/opportunity-attack clocks. This decision is recorded on its binding, not silently inferred from all elemental spells.

**NEW Balanced Elements bridge:** the character may modify an owned, explicitly classified elemental Speed-control component, including a legally acquired multiclass source. Registered members are Shaman Ice affinity, Frost Totem, Elemental Chorus and Ice Wisp Speed0; Mage Cold Focus/Glacier, Fusion and Cascade cold slows; Dragoon Dive/Lance cold slows; and the individually reviewed ordinary Ray of Frost/Frost Arrow slow records. Flask Root is not elemental from supplied evidence. Other ordinary spells require an explicit reviewed classification; a cold damage type alone does not automatically supply it.

The extension is `max(existingDeadline, targetFollowingRegularEndMeasuredNow)`, excluding the current in-progress target end, bounded by an express governing source/concentration maximum. It does not recursively add a turn to the previous deadline, increase magnitude, reanimate ended effects or extend other components. Source once/turn/cost rules apply. Stun, silence, whole-Action denial, concentration itself, Strain, cargo and terrain remain ineligible. The alternative next-Burn-tick +1 uses the existing periodic rules and does not duplicate a Burn.

## Important source clocks

| Source component | Endpoint or cadence |
|---|---|
| Mage Cold passive/Bolt/Surge/Glacier | Target next regular end |
| Mage Fusion's -10/Cold+Lightning opportunity denial | Target next regular end; Fire+Lightning Reaction denial target next regular start |
| Mage Cascade's printed cold / lightning riders | Source next regular end / source next regular start (unqualified text) |
| Dragoon Drakestorm Dive cold / lightning | Source next regular end |
| Dragoon Elemental Lance cold / lightning | Source next regular end / target next regular start |
| Shaman Ice affinity; Elemental Chorus slow | Source next regular end |
| Shaman Ice Wisp Speed0 | Target next regular end |
| Frost Totem; Winter's Embrace; Glue; Resonant Seed slow | Current triggering actual turn end; no turn underway means6 seconds |
| Paladin Reign of Ashes ash-bound | **Target** next regular end; operative “its next turn” overrides abbreviated summary |
| Paladin Black Manifestation | Source next regular start |
| Paladin Judgment Brand | Third future target regular end; current in-progress end excluded |
| Paladin Sorrow's Weight slow | Source next regular start or spell end, whichever first |
| Paladin Standing Stone / Law's Weight slow | Target next regular start; actual source pulse application rules retained |
| Monk/Warrior custom Stagger | Target next regular end |
| Thief Vein Cutter / Crippling Lash riders | Target next regular end, or earlier consumption of the specific rider |

Other exact source endpoints are preserved in the binding reference. No generic table entry changes the separate already-reviewed periodic damage clocks.

## Root, physical restraints and suppression

Root supplies Speed0 only; it does not inherently apply Restrained, Grappled, Incapacitated, Action/Reaction loss or a teleport ban. A Speed0 source not named Root receives no invented Root identity. Multiple zero records coexist; ending one does not end another.

Printed restraint saves, escape Actions, size/anatomy limits, concentration and relationship endpoints win. **NEW fallback only** for genuine physical Restrained with no explicit escape, no sufficient fixed endpoint and no special-cure requirement: Action STR(Athletics) or DEX(Acrobatics) against recorded applying DC, otherwise10, ends **one selected** record on success. An adjacent helper may instead use Action STR(Athletics). None of the supplied active restraints needs this fallback. A fixed endpoint alone excludes it. No generic cutting, helper or object-HP escape is added to magical-only restraints.

Net Bolt retains printed Action STR(Athletics) escape, net AC10/HP5, maximum3 rounds and Huge+ -10 replacement. Tinker Net Trap retains its printed repeat save/Action escape. Earthen Grip's grounded-target requirement is an application requirement; the source does not say moving/teleporting away ends it. It persists after a legal teleport until concentration, printed time or its Action escape ends it. Tyrant's Impale and Panther retain their explicit reach/separation/reversion relationship endings. If suppression permits escape beyond a required maintained reach, the source ends and cannot resume. An attached physical net otherwise persists through suppression and can resume until removed/destroyed/expired.

Immunity suppresses only covered components; clocks and relationship checks continue. Word of Binding's Silenced and Speed0 are independent for immunity, while its successful repeat save ends both. A suppressed record does not grant active eligibility hooks. Ending one restriction does not cure unrelated damage, marks or components on the same card.

## Custom Staggered and named cures

**NEW exact-source bindings:** `monk.echoing-guard.stagger` and `warrior.brutal-strike.stagger` each impose -1 attacks and -5 Speed, refresh without stacking and end at target next regular end. They do not import Core Staggered's Guard removal or forced-movement rider. Across these custom Stagger-style attack penalties use the strongest; Speed uses the arbitration above.

`classification.staggered` links Core Staggered and these two records for actual named readers/removers, including Paladin Sanctify Ground. Choosing Staggered there ends **all present classified records** on that creature, including suppressed ones; none can resume from suppression afterward. This does not remove unrelated -1 attacks/-5 Speed records or grant immunity against a later new application. One cleansing choice per creature per pulse remains. This classification supplies no additional mechanical penalties.

## Marks and one-use components

Marks retain owner, target type/cap, source clock, independent rider entitlements and eligibility tags. They are not automatically Core Marked or mutually interchangeable. Trigger wording matters: next attack spends on the qualifying attack roll; next hit spends on a qualifying hit even if damage becomes0; when damaged requires a positive resolved-damage packet after defenses but before temporaryHP. Only the component named by a consumption event ends, unless the source says the whole mark ends.

**Reviewed healing-conference clarification:** numeric actualDamageDealt is tempHP absorbed plus actual normalHP lost to the packet, excluding overkill and later recovery/state assignments. A positive packet against an HP1 floor can have numeric0: Divine Judgment still reflects its minimum1 and consumes that actual turn's entitlement. A fully prevented resolved0 packet does neither. The [healing guide](HEALING_DEATH_PLAYTEST.md) defines the complete distinction; this clarification adds2 checks to the previously reviewed148-case control scope.

Guiding Star's reference API begins the legal qualifying attack **before** rolling: consume the available+2 entitlement and return the bonus plus a unique attack token. After the roll, resolve that token once with the hit outcome to receive any remainingS radiant rider. A miss leaves that hit rider for a later ally attack. Duplicate or foreign token resolution is rejected. Suppressed/illegal attack starts spend nothing. If the mark expires or becomes suppressed before resolution, it grants no hit rider; beginning an attack never refunds its spent attack bonus.

| Source | Operational handling |
|---|---|
| Balanced Scales | Actual HP restored to living ally applies mark to source next regular start. First enemy positive damage triggers S+M radiant once, no retaliation recursion. Keep printed at-most-once/marked-ally/round even if healing refreshes. |
| Divine Judgment | First positive damage to another creature on each actual target turn, including extra turns, reflects half actual damage, floor, min1/maxCleric level. No off-turn trigger. Repeat ending WIS saves remain regular-end; concentration/max3 target rounds retained. |
| Carrion Conductor | Corpse-only timed marker. Separate used-corpse history survives expiry, burst or suppression; that corpse cannot be marked again by Carrion Conductor, regardless of owner. It does not ban unrelated corpse mechanics. |
| Drake Mark | One marked target, new replaces old, source next regular end. First subsequent direct polearm hit consumes; triggering leap, DoT or copies do not. AddsS in qualifying hit's damage resolution even if final damage becomes0. |
| Oracle Guiding Bolt | **NEW two entitlements:** first ally-other-than-owner attack gets+2 then spends that opportunity on hit/miss. Next qualifying ally hit before expiry addsS radiant and ends mark. A miss leaves the hit rider, without another+2. New paid application replaces/reset both, never stacks. |
| Oracle Wrathful Brand | Owner's next damaging attack hit adds half unmodified rolled base dice, floor/min1; requires positive pre-bonus resolved attack damage. Separate first ally-positive-damage entitlement attempts1d6 heal and one WIS save; failed save applies printed attack penalty. Heal prevention/full HP does not refund it. Spending riders does not itself end the timed Brand. |
| Oracle Constellation | Owner mark set, printed2 targets/3 mastery; recast replaces previous set. Its+1d6 cap is once/numbered round across set, not per target. |
| Oracle Omen Reader | Triggering -2 attack adjustment consumed once; subsequent star-ash+1 ally attack benefit persists through target-next-end. |
| Paladin Vengeance | Preserve Smite/Brand/Retribution IDs and owner-qualified eligibility. Retribution die consumption does not end its opportunity-attack advantage or remaining mark. |
| Paladin Linked Ward / Chain of Duty | Willing-ally concentration links with separate redirection/teleport triggers, not generic Marked. Ordinary Reaction and printed per-round limits apply. |
| Ranger Track Target | One quarry, new replaces old,1minute; does not reveal through total cover. Predator's Mark upgrades underlying quarry; ending its concentration leaves underlying quarry until its own endpoint. |
| Ranger Pathfinder's Mark | Fixed point,24h; navigation state, not creature condition. |
| Soldier Marked for Death | One target; saves penalty through source-next-start. First qualifying hit against another ally spends its -1 damage rider even if damage0; does not consume the persistent save penalty. No stacking with Intimidating Presence where printed. |
| Tinker Target Scanner | First qualifying ally attack gets+1 and consumes that scanner record on the roll, hit or miss; source-next-start deadline. |
| Wizard Binding Sigil | One target; only owner's Wizard spell attacks gain advantage; source-next-end. No companion/echo/environmental application. |
| Wizard Gravebrand | Source-qualified mark and necrotic periodic effect; the name/Pact does not classify it as an inflicted curse. |

**NEW Divine Judgment simultaneous-target order:** use printed source target order; otherwise declared target/list order fixed before damage, or stable area target application order established before resolving. First recipient taking positive damage supplies reflection magnitude; never sum victims. The turn entitlement is then spent.

Corpses, intrinsic class progression, Monk hard-denial history and Mirrorsage/Wizard archive-retention markers are bookkeeping rather than creature Marked. Existing Crimson Blood Mark, Oracle Mark of the Doomed, Paladin Grief and Warrior Vulnerable identities retain their reviewed rules.

## Curse and disease

`classification.curse` and `classification.disease` are metadata on actual inflicted affliction records, not new generic conditions or inherent penalties. This packet adds no disease-producing source and no generic inflicted curse source. Oracle intrinsic Curse/Burden/Boons/Manifestation, quest/pact unlocks, Blood Curse's name and Shaman hex-damage wording do not create those affliction categories. Plague Bearer/Infectious Mutation explicitly do not create diseases.

A repeat-save feature only repeats a currently legal saving throw that the actual affliction allows. It creates no new save, DC or cure. Ordinary curse removal respects explicit removability, special cures, protection and tier limits. Cleansing Brand's unknown non-spell curse tier is a dependency, not permission to invent a favorable tier.

**NEW disease-immunity bridge:** covered new disease applications are prevented; covered mechanical effects of existing diseases are suppressed while immunity lasts, with records and progression clocks retained. Nonmagical/ordinary/all-disease scopes are distinct. Suppression is not cure. Lethal/progressive diseases must individually specify whether immunity blocks progression, its endpoint, or just penalties; do not universally postpone death or resurrect through immunity. The disease catalog remains open.

Analyze Magic/Arcane Sight may reveal actual permitted magical curse/link metadata within their printed examination procedures. They do not overcome protected Oracle class information. Identify does not automatically reveal curses; Detect Magic/Aura Glimpse do not gain that extra information. Neither a display name nor the absence of metadata proves a successful cure/detection.

## Compulsion, action denial and initiative

Keep Charmed/Frightened, one commanded Action, Reaction denial, Speed0/half and attack restrictions as distinct components. The shared source-character/target/encounter hard-denial guard controls new hard components across feature names. A used allowance blocks only a new hard component; apply an expressly printed soft fallback, otherwise do not invent one. Hard-control immunity and source restrictions still apply.

Oracle Bone Whisper, Ledger's Command, Marquis's Glimpse, Slumber Glimpse and Moment's Pause soft fallback records, and Paladin Decree/Echo of Ages soft fallbacks, carry slowed-foe eligibility only while their actual Speed component is active. Spiral Opens instead has a distinct player-Speed0 component; choosing a repeated action or using NPC Forced Echo does not gain that tag. Passive Stars Revelation Mastery is a HOOK authorizing a later enhanced Guiding Bolt component, not an immediate applied slow. The registry separates application, modifier and reader/bookkeeping references.

Ledger's Command may command one hostile Action under that guard; subsequent qualifying failures use its Reaction+Speed0 fallback. Bone Whisper, Marquis's Glimpse, Slumber Glimpse and Moment's Pause retain their own hard/fallback splits. Slumber's -2 initiative rider affects the next eligible initiative roll/check before encounter end, never an already-established slot. Its attack bonus is independently consumed.

Wizard Mental Binding/Arcane Domination and Paladin Decree of Submission retain only their printed first commanded turn; ongoing Charmed/Reaction/Speed riders cannot command another Action. Mind Prison's first Incapacitated/commanded replacement is separate from later half-Speed/no-Reaction riders. The player retains printed target/route choices and prohibitions on self-harm, beliefs, resource expenditure and permanent allegiance. An NPC Forced Echo from The Spiral Opens spends the hard-denial allowance and has no invented NPC fallback after it is used. Its player branch stays distinct. Royal Decree's target-chosen Prone-or-safe-movement retains Action/target choice and does not spend the whole-Action denial allowance.

Echo of Ages' attack denial uses the shared hard guard; later actual qualifying failed applications use its printed soft fallback. It does not gain a repeat trigger every round from concentration. Reign of Ashes is soft half-Speed/noDash/**no willing teleport benefit**, ending target-next-end. **NEW:** target cannot self-teleport or consent to another's transport; independently legal involuntary hostile displacement can still affect it unless that effect needs willingness. No Root/Restrained or universal planar anchoring is added.

**NEW Moment's Pause delay:** snapshot canonical initiative order excluding temporary delays. One pending delay per target per next numbered round; repeated applications do not stack. At next-round construction process stable application order. Find the first still-participating snapshot creature after the target, skipping removed/dead and ignoring new entrants absent from that snapshot; move target immediately after it. With no surviving later snapshot member leave current position. Chained delays are deterministic in application order; no participant is duplicated/deleted and no virtual duration/falling/recovery marker changes. The next following round resumes canonical order. This is distinct from modifying an initiative roll.

## Hypermutation and systemic penalties

**NEW Hypermutation Spike:** at that Butcherform activation snapshot each possessed movement mode's ordinary sheet Speed: ancestry/creature or replacement form base, permanent innate increases and currently qualifying persistent passives (including unarmored-Speed). Exclude temporary/timed buffs, stances, debuffs, Strain, cargo, Exhaustion and Hypermutation itself. A conditional passive changing later does not recalculate the snapshot.

Each captured mode's floor is half that snapshot, rounded down. After compatible numeric changes and multipliers, enforce the floor. Never grant a lost/absent/newly gained mode, bypass explicit Speed0/Root/Grappled/Restrained/Exhaustion5, terrain cost or a voluntary-movement prohibition. Incapacitated itself does **not** set Speed0 under the reviewed Core condition; the floor simply grants no Actions, Bonus Actions, Reactions or concentration. Shared movement already spent remains spent.

Serum side effects, Mutation Overload/Oracle backlash and Undying Spellform's half-Speed voluntary-movement cap stay outside adverse-control arbitration. The broader remaining-conscious/death/replacement/resurrection interfaces remain open. A positive movement number does not waive those rules.

## Verification and remaining work

The reference helpers cover selected arithmetic, consumption, suppression/expiry, metadata gates, source clocks and initiative permutation. The caller still validates source access, costs, target legality, actual attack/save outcomes, concentration, turn identity and event ordering. They are not the combat engine or all-card implementation.

[Validation](CONTROL_PLAYTEST_VALIDATION.json) currently has150 targeted checks and9,393 Speed invariant states, including the reviewed healing damage clarification. [Source verification](CONTROL_STATE_SOURCE_VALIDATION.json) checks219 exact source objects/passages. Neither establishes human balance, complete spell effects, exhaustive condition mapping or whole-game completion. The [selected healing/death interface](HEALING_DEATH_PLAYTEST.md) is separately reviewed. Still open: actual disease/curse affliction catalog, non-spell curse tiers, object/tether durability beyond printed nets, broader body/soul and resurrection content, other class/resource semantics, and the all-source remainder.

[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_CONTROL_FINAL_REVIEW.md) approves this supplied interface after correcting pre-roll mark bonuses, binding roles, fallback tags and all turn-end clock phases.
