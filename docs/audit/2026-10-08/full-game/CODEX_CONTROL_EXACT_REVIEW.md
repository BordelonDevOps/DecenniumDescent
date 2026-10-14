# Exact control-state candidate review

Please adversarially review the attached actual candidate implementation after our219-source conference and clock corrections. All original class/spell objects remain unchanged. DD16/DD18 and all-source semantics remain open. This is a bounded interface package, not full spell/card automation. Report concrete bugs first; if bounded guide/helper checks are sound, explicitly state the exact completed scope, remaining source dependencies and no broad closure.

Current checks:107 targeted control interface cases,9,393 Speed invariant states. Source integrity219records:184cards25engines10ordinaryspells. Separate binding validator checks219source procedures and179component identities, including alternative modes; counts do not prove semantics. Raw previous conferences are preserved as historicalDiscussion in JSON, explicitly non-authoritative when corrected. The operational guide and per-source overrides control.

Please inspect these points particularly:
- The guide corrects your Incapacitated shorthand: Core Incapacitated prohibitsA/BA/R/concentration but not inherently movement/Speed. Hypermutation grants no actions and cannot overcome a separate movement prohibition.
- `effective_control_speed` has per-mode Hypermutation baseline supplied by caller after legitimate snapshot; core_speed_zero and actualzero controls win. Callers still enforce voluntary movement/action restrictions, mode validity and common spent-movement ledger.
- Speed-record refresh preserves exact-profile magnitude/deadline and independent differing candidates. A single Cold hit is caller-deduplicated into one appropriate profile; helper never adds magnitudes. Source cost/application checks are caller-owned.
- Guiding Star helper returns the attack bonus the caller had to include BEFORE rolling; it does not retroactively convert a miss. Would a separate pre-roll query + post-roll consumption interface be clearer/necessary? No actual game engine currently calls it.
- No helper for blanket event dispatch/complete source application exists. Source procedures and caller validation remain authoritative. Some source records contain non-control mechanics intentionally outside this pass.
- Metadata index has explicit elemental/stagger/slowed memberships. Composite soft-fallback components must carry slowed eligibility only while their actual Speed component is active. Please identify missing semantic members (e.g. Oracle/Paladin soft fallback packages) instead of claiming all mappings complete.
- Mage Fusion Fire+Cold's Speed rider has no separately printed endpoint in that phrase; its sibling Cold+Lightning specifies target-next-end. Guide uses target-next-end for Fusion slows as a NEW bounded missing-endpoint bridge; please explicitly accept/correct that decision. Cascade remains source-clock. Does either category require an additional per-source override?
- Ray of Frost/Frost Arrow are audited ordinary cold spells with direct-attack slow; their elemental classification remains unassigned in this index pending explicit semantic decision. We can NEW classify these two cold slow components for Balanced Elements after your confirmation; this does not classify every future cold spell by name/type.
- Carrion Conductor used-corpse history is source-family/corpse scoped, not owner-scoped, so another user cannot re-use the same corpse with Carrion Conductor. Confirm this intended scope from 'corpse cannot be reused'.
- Existing Bleed/fire generic cures on suppressed records are a separate follow-up audit; Sanctify Ground explicitly removes allpresent classifiedStaggered including suppressed. Do not silently use active-hook predicate for cures.

## Exact authored files

### docs/mechanics/CONTROL_STATES_PLAYTEST.md

```markdown
# Source-qualified control states

**IN REVIEW — authored candidate.** This guide binds the supplied 219 source passages (179 initial candidates and 40 supplemental cards). It does not claim a complete semantic audit of every class, spell, creature or item, and does not close DD16 or DD18. Original source objects remain unchanged. NEW below marks an integration decision, not text recovered from a historical book.

Use this with [Core conditions](CONDITIONS_PLAYTEST.md), [custom riders](CUSTOM_CONDITION_BINDINGS.md), [combat timing](COMBAT_ACTION_PLAYTEST.md), [Strain](STRAIN_PLAYTEST.md), [source bindings](CONTROL_SOURCE_BINDINGS.md), and the [coverage ledger](CONTROL_STATE_COVERAGE.md). Exact structured records are in `data/playtest/control_state_bindings.json`. The source procedure supplies its costs, application triggers, target eligibility, saves, frequency, concentration and endings; a component ID alone grants nothing. Alternative modes never apply together merely because both IDs appear in a binding.

## Records, clocks and precedence

Each application records its identity, exact source, owner character, target, selected mode/components, application order, recorded source DC, deadline/marker, concentration or attachment relationship, remaining uses, and applicable immunity/suppression. Display names never create conditions or prerequisites. An owner's mark cannot satisfy another owner's class hook. A corpse marker, map point, archived spell, intrinsic Oracle Curse and hard-denial history are distinct state types.

Explicit operative effect text controls over a less-specific summary duration field. Use preserved regular-turn markers for **next** turn and bare N-round durations as in the combat guide; an in-progress current turn is not the next turn. Unqualified next turn refers to the source; explicit its/target refers to the target. Bare hostile N rounds, including hostile marks, use N future target regular ends. Beneficial/self N rounds use source regular starts. Preserve virtual markers through initiative changes and absence. Out of initiative bare N rounds use application+6N seconds, retaining that deadline on entering initiative. Explicit source/concentration endings still apply.

**NEW current-turn bridge:** “end of that turn” or the supplied bare “end turn” effects end at the end of the actual turn containing the application event, including another creature's or an extra turn. With no current turn, use application+6 seconds. An application during end-turn resolution expires at that same end after resolving, rather than acquiring a fabricated next turn. This applies to Resonant Seed, Winter's Embrace, Frost Totem and Glue. It does not override an explicit next-turn endpoint.

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

**NEW Balanced Elements bridge:** the character may modify an owned, explicitly classified elemental Speed-control component, including a legally acquired multiclass source. Registered members are Shaman Ice affinity, Frost Totem, Elemental Chorus and Ice Wisp Speed0; Mage Cold Focus/Glacier, Fusion and Cascade cold slows; and Dragoon Dive/Lance cold slows. Flask Root is not elemental from supplied evidence. Ordinary spells require an explicit reviewed classification; a cold damage type alone does not automatically supply it.

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

Marks retain owner, target type/cap, source clock, independent rider entitlements and eligibility tags. They are not automatically Core Marked or mutually interchangeable. Trigger wording matters: next attack spends on the qualifying attack roll; next hit spends on a qualifying hit even if damage becomes0; when damaged requires positive actual damage. Only the component named by a consumption event ends, unless the source says the whole mark ends.

| Source | Operational handling |
|---|---|
| Balanced Scales | Actual HP restored to living ally applies mark to source next regular start. First enemy positive damage triggers S+M radiant once, no retaliation recursion. Keep printed at-most-once/marked-ally/round even if healing refreshes. |
| Divine Judgment | First positive damage to another creature on each actual target turn, including extra turns, reflects half actual damage, floor, min1/maxCleric level. No off-turn trigger. Repeat ending WIS saves remain regular-end; concentration/max3 target rounds retained. |
| Carrion Conductor | Corpse-only timed marker. Separate used-corpse history survives expiry, burst or suppression; that corpse cannot be marked again by Carrion Conductor, regardless of owner. It does not ban unrelated corpse mechanics. |
| Drake Mark | One marked target, new replaces old, source next regular end. First subsequent direct polearm hit consumes; triggering leap, DoT or copies do not. AddsS in qualifying hit's damage resolution even if final damage becomes0. |
| Oracle Guiding Bolt | **NEW two entitlements:** first ally-other-than-owner attack gets+2 then spends that opportunity on hit/miss. Next qualifying ally hit before expiry addsS radiant and ends mark. A miss leaves the hit rider, without another+2. New paid application replaces/reset both, never stacks. |
| Oracle Wrathful Brand | Owner's next damaging attack hit adds half unmodified rolled base dice, floor/min1; requires positive pre-bonus actual attack damage. Separate first ally-positive-damage entitlement attempts1d6 heal and one WIS save; failed save applies printed attack penalty. Heal prevention/full HP does not refund it. Spending riders does not itself end the timed Brand. |
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

[Validation](CONTROL_PLAYTEST_VALIDATION.json) currently has107 targeted checks and9,393 Speed invariant states. [Source verification](CONTROL_STATE_SOURCE_VALIDATION.json) checks219 exact source objects/passages. Neither establishes human balance, complete spell effects, exhaustive condition mapping or whole-game completion. Still open: actual disease/curse affliction catalog, non-spell curse tiers, object/tether durability beyond printed nets, death/replacement/resurrection, other class/resource semantics, and the all-source remainder.

```

### tools/control_playtest_rules.py

```python
"""Selected control interfaces. Callers validate actual sources, costs and clocks.

These helpers do not cast spells, apply all card effects, schedule turns, choose
targets, or grant actions. Printed application and endpoint rules remain in the
source-qualified registry and guide. No name-based condition inference occurs.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction
from spell_playtest_rules import integer, SpellRuleError


@dataclass(frozen=True)
class SpeedRecord:
    application_id: str
    owner: str
    target: str
    group: str
    profile: str
    mode: str
    amount: int = 0
    floor: int = 0
    expires: int | None = None
    active: bool = True
    suppressed: bool = False
    slowed_hook: bool = True

    def __post_init__(self):
        for value in (self.application_id, self.owner, self.target, self.group, self.profile):
            if not isinstance(value, str) or not value:
                raise SpellRuleError('Record identities must be nonempty strings')
        if self.mode not in ('flat', 'half', 'half-minus', 'zero'):
            raise SpellRuleError('Unreviewed Speed transform')
        integer(self.amount, 'Speed reduction amount', 0)
        integer(self.floor, 'source minimum Speed', 0)
        if self.expires is not None:
            integer(self.expires, 'expiry time', 0)
        if self.mode in ('half', 'zero') and (self.amount or self.floor):
            raise SpellRuleError('Half/zero profiles accept no flat amount or floor')

    def operative(self, now):
        integer(now, 'time', 0)
        return self.active and not self.suppressed and (self.expires is None or now < self.expires)

    def result(self, pre_control_speed):
        integer(pre_control_speed, 'Speed before hostile control', 0)
        if self.mode == 'zero':
            return 0
        if self.mode == 'half':
            value = pre_control_speed // 2
        elif self.mode == 'half-minus':
            value = pre_control_speed // 2 - self.amount
        else:
            value = pre_control_speed - self.amount
        # A minimum attached to a penalty must never increase an existing Speed.
        return min(pre_control_speed, max(self.floor, value, 0))


def effective_control_speed(pre_control_speed, records, *, target, now=0,
                            global_multiplier=Fraction(1), core_speed_zero=False,
                            hypermutation_baseline=None, mode_possessed=True):
    """Strongest adverse transform against ONE common baseline, then multiplier.

    Systemic flat penalties were already applied to the input; terrain is not
    included. Core Grappled/Restrained and other independently established zero
    states are passed separately. Explicit exceptional stacking/floors require
    their own reviewed adapter and are not silently guessed here.
    """
    integer(pre_control_speed, 'Speed before hostile control', 0)
    integer(now, 'time', 0)
    if not isinstance(global_multiplier, Fraction) or not 0 <= global_multiplier <= 1:
        raise SpellRuleError('Use an exact reviewed reduction multiplier')
    ids = [r.application_id for r in records]
    if len(ids) != len(set(ids)):
        raise SpellRuleError('Duplicate application ID')
    if any(r.target != target for r in records):
        raise SpellRuleError('One target per calculation')
    eligible = [r for r in records if r.operative(now)]
    speed = min([pre_control_speed] + [r.result(pre_control_speed) for r in eligible])
    speed = speed * global_multiplier.numerator // global_multiplier.denominator
    if hypermutation_baseline is not None:
        integer(hypermutation_baseline,'captured normal mode Speed',0)
        speed=max(speed,hypermutation_baseline//2)
    immobilized=core_speed_zero or any(r.mode=='zero' for r in eligible)
    return 0 if immobilized or not mode_possessed else speed


def slowed_foe(records, *, target, now=0):
    """Overshadowed is still active; suppressed/expired never grants the hook."""
    return any(r.target == target and r.slowed_hook and r.operative(now) for r in records)


def refresh_speed_record(records, incoming, *, now=0):
    """One owner/target/group/exact profile refreshes without adding magnitude.

    Differing transform/magnitude profiles keep separate deadlines, so a later
    weaker slow cannot erase an earlier strong one. No expired record is revived
    except by this caller-validated new application. This is not a free refresh.
    """
    integer(now,'application time',0)
    if incoming.expires is not None and incoming.expires<=now:
        raise SpellRuleError('A new refresh cannot have an already-passed deadline')
    key = lambda r: (r.owner, r.target, r.group, r.profile, r.mode, r.amount, r.floor)
    result = list(records)
    matching = [i for i,r in enumerate(result)
                if key(r)==key(incoming) and r.active and (r.expires is None or r.expires>now)]
    if len(matching)>1:
        raise SpellRuleError('Aggregate duplicate exact profiles before refreshing')
    if matching:
        i=matching[0]
        old=result[i]
        end=None if old.expires is None or incoming.expires is None else max(old.expires,incoming.expires)
        # Retain the existing component suppression; application did not grant immunity removal.
        result[i]=replace(old,expires=end)
    else:
        if any(r.application_id==incoming.application_id for r in result):
            raise SpellRuleError('A new application needs a unique identity')
        result.append(incoming)
    return result


@dataclass
class GuidingStarMark:
    owner: str
    target: str
    expires: int
    s: int
    attack_bonus_available: bool = True
    hit_rider_available: bool = True
    active: bool = True

    def ally_attack(self, *, actor, ally_of_owner, hit, now, legal=True, suppressed=False):
        """One already-resolved qualifying attack; bonus is announced before roll.

        Returned attackBonus states what that roll was entitled to. This helper
        does not retroactively turn a miss into a hit; caller resolves with it.
        A miss spends +2, while the next-hit entitlement survives.
        """
        if (not self.active or suppressed or now>=self.expires or not legal
                or actor==self.owner or not ally_of_owner):
            return {'attackBonus':0,'radiantBonus':0}
        bonus=2 if self.attack_bonus_available else 0
        self.attack_bonus_available=False
        damage=self.s if hit and self.hit_rider_available else 0
        if hit and self.hit_rider_available:
            self.hit_rider_available=False
            self.active=False
        return {'attackBonus':bonus,'radiantBonus':damage}


@dataclass
class WrathfulBrand:
    owner: str
    target: str
    expires: int
    owner_rider_available: bool = True
    ally_rider_available: bool = True
    active: bool = True

    def trigger(self, *, actor, ally_of_owner, now, actual_damage,
                direct_attack_hit=False, base_dice_total=0, suppressed=False):
        integer(actual_damage,'actual damage',0)
        integer(base_dice_total,'unmodified rolled base dice',0)
        result={'fireBonus':0,'healD6':False,'wisdomSave':False}
        if not self.active or suppressed or now>=self.expires or actual_damage==0:
            return result
        if actor==self.owner and direct_attack_hit and self.owner_rider_available:
            self.owner_rider_available=False
            result['fireBonus']=max(1,base_dice_total//2)
        elif actor!=self.owner and ally_of_owner and self.ally_rider_available:
            self.ally_rider_available=False
            result.update(healD6=True,wisdomSave=True)
        return result


@dataclass
class OneShotRider:
    trigger_kind: str
    available: bool = True

    def trigger(self, *, qualifying, attack_roll=False, hit=False, actual_damage=0):
        integer(actual_damage,'actual damage',0)
        if self.trigger_kind not in ('attack','hit','damage'):
            raise SpellRuleError('Unregistered consumption trigger')
        met={'attack':attack_roll,'hit':hit,'damage':actual_damage>0}[self.trigger_kind]
        if not self.available or not qualifying or not met:
            return False
        self.available=False
        return True


@dataclass
class PerTurnReflection:
    cleric_level: int
    used_turn_ids: set = field(default_factory=set)

    def reflect(self, *, target_turn_id, actual_damage, on_target_turn):
        """Caller supplies distinct actual turns, target-declared damage-event order."""
        integer(actual_damage,'actual damage to another creature',0)
        integer(self.cleric_level,'Cleric level',1,20)
        if not on_target_turn or actual_damage==0 or target_turn_id in self.used_turn_ids:
            return 0
        self.used_turn_ids.add(target_turn_id)
        return min(self.cleric_level,max(1,actual_damage//2))


def physical_escape_fallback(*, restrained, physical, explicit_escape,
                             fixed_endpoint, special_cure, source_dc=None, helper=False):
    if not restrained or not physical or explicit_escape or fixed_endpoint or special_cure:
        return None
    dc=10 if source_dc is None else integer(source_dc,'source DC',1)
    return {'activation':'Action','dc':dc,
            'checks':['STR(Athletics)'] if helper else ['STR(Athletics)','DEX(Acrobatics)'],
            'scope':'one selected restraint record'}


def disease_immunity_covers(*, classified_disease, magical, ordinary, scope):
    if scope not in ('all-disease','nonmagical-disease','ordinary-disease'):
        raise SpellRuleError('Unreviewed immunity scope')
    return classified_disease and (scope=='all-disease'
        or scope=='nonmagical-disease' and not magical
        or scope=='ordinary-disease' and ordinary)


def repeat_affliction_save(*, actual_record, source_allows_save, current_save_legal):
    return actual_record and source_allows_save and current_save_legal


def generic_curse_removable(*, classified_curse, intrinsic_class_state,
                            special_cure, ordinary_removable, curse_tier,
                            remover_tier=None):
    if not classified_curse or intrinsic_class_state or special_cure or not ordinary_removable:
        return False
    if remover_tier is None:
        return True
    integer(remover_tier,'remover tier',0)
    return curse_tier is not None and integer(curse_tier,'actual source tier',0)<=remover_tier


def curse_metadata_visible(*, detection_method, success, magical,
                          actual_curse_metadata, protected):
    if detection_method not in ('analyze-magic','arcane-sight','identify','detect-magic','aura-glimpse'):
        raise SpellRuleError('Unreviewed detection method')
    return (detection_method in ('analyze-magic','arcane-sight') and success
            and magical and actual_curse_metadata and not protected)


def regular_control_step(*, regular_turn, explicit_extra_turn_exception=False):
    """Only control repeat saves/expiry/pulses; not a universal proc rule."""
    return regular_turn or explicit_extra_turn_exception


def current_turn_endpoint(*, application_time, actual_turn_end=None):
    """Explicit 'that turn'/reviewed bare 'end turn', not a NEXT-turn rule."""
    integer(application_time,'application time',0)
    if actual_turn_end is None:
        return application_time+6
    integer(actual_turn_end,'current actual turn end',application_time)
    return actual_turn_end


def balanced_elements_endpoint(existing, following_target_end, *, owner_matches,
                               elemental_control, source_maximum=None):
    """Following endpoint is caller-computed from NOW, never old endpoint+6."""
    integer(existing,'existing expiry',0)
    integer(following_target_end,'future target regular end measured now',0)
    if not owner_matches or not elemental_control:
        return existing
    end=max(existing,following_target_end)
    if source_maximum is not None:
        integer(source_maximum,'express governing source endpoint',0)
        if existing>source_maximum:
            raise SpellRuleError('Existing record already exceeds governing source maximum')
        end=min(end,source_maximum)
    return end


def ash_bound_teleport_allowed(*, willing, source_requires_willing, otherwise_legal):
    return otherwise_legal and not willing and not source_requires_willing


def sanctify_staggered_records(records, *, target):
    """Cure all PRESENT classified records, including suppressed ones."""
    return [r['applicationId'] for r in records if r['targetId']==target
            and r.get('present',False) and 'classification.staggered' in r.get('tags',[])]


def delayed_round_order(canonical_order, delays):
    """Construct ONE round. Caller selects pending delays for that round only.

    Each record contains target, canonical snapshot, applicationSequence. The
    return value changes actual order only; virtual clocks are not inputs.
    """
    if len(canonical_order)!=len(set(canonical_order)):
        raise SpellRuleError('Canonical order requires distinct participants')
    order=list(canonical_order)
    delayed=set()
    for record in sorted(delays,key=lambda r:(r['applicationSequence'],r['target'])):
        integer(record['applicationSequence'],'stable application sequence',0)
        target=record['target']; snapshot=record['snapshot']
        if len(snapshot)!=len(set(snapshot)) or target not in snapshot:
            raise SpellRuleError('Delay snapshot must contain target exactly once')
        if target not in order or target in delayed:
            continue
        delayed.add(target)
        following=snapshot[snapshot.index(target)+1:]
        neighbor=next((person for person in following if person in order),None)
        if neighbor is not None:
            order.remove(target)
            order.insert(order.index(neighbor)+1,target)
    return order

```

### tools/validate_control_playtests.py

```python
"""Table examples and lifecycle boundaries for the bounded control interfaces."""
from pathlib import Path
from fractions import Fraction
from dataclasses import replace
import json
from control_playtest_rules import *

ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append(name)
    def rejects(name,fn):
        try: fn()
        except SpellRuleError: checks.append(name)
        else: raise AssertionError(name)
    def slow(ident,mode='flat',amount=10,**kw):
        return SpeedRecord(ident,kw.pop('owner','mage-A'),'hero',kw.pop('group','cold-focus'),
                           kw.pop('profile',ident),mode,amount=amount,**kw)
    a=slow('cold',expires=12)
    b=slow('ray',owner='mage-B',group='ray-of-frost',expires=18)
    half=slow('crippling',mode='half',amount=0,expires=6)
    zero=slow('root',mode='zero',amount=0,expires=3)
    f=lambda rs,**kw:effective_control_speed(30,rs,target='hero',**kw)
    check('Two unrelated -10 effects retain records but produce Speed20',f([a,b]),20)
    check('Half beats -10 on Speed30 without adding both',f([a,half]),15)
    check('Exhaustion halves the arbitrated value once',f([a,half],global_multiplier=Fraction(1,2)),7)
    check('Independent Strain penalties occur before hostile arbitration',effective_control_speed(15,[a,half],target='hero'),5)
    check('Root sets zero without deleting other effects',f([a,zero]),0)
    check('Root expiry exposes still-active slow',f([a,zero],now=3),20)
    check('Stronger expiry exposes weaker candidate',f([a,half],now=6),20)
    check('All effects expire at exact boundary',f([a,b],now=18),30)
    check('Suppression does not participate in Speed arbitration',f([replace(a,suppressed=True)]),30)
    check('Suppression ending before expiry allows return',f([replace(a,suppressed=False)],now=4),20)
    check('Core Grappled remains Speed0 independently',f([a],core_speed_zero=True),0)
    check('Overshadowed adverse record still satisfies slowed-foe',slowed_foe([a,half],target='hero'),True)
    check('Suppressed slow does not satisfy hook',slowed_foe([replace(a,suppressed=True)],target='hero'),False)
    check('Expired slow does not satisfy hook',slowed_foe([a],target='hero',now=12),False)
    check('Core restriction alone carries no slowed hook',slowed_foe([],target='hero'),False)
    check('Other target never satisfies hook',slowed_foe([a],target='other'),False)
    rejects('Reject mixed-target Speed computation',lambda:f([replace(a,target='other')]))
    rejects('Reject duplicated application IDs',lambda:f([a,a]))
    rejects('Reject unreviewed transform',lambda:slow('x',mode='multiply'))
    rejects('Reject float multiplier',lambda:f([a],global_multiplier=0.5))
    leash=slow('iron-leash',floor=5)
    check('Iron Leash minimum never increases an existing Speed3',effective_control_speed(3,[leash],target='hero'),3)
    check('Iron Leash on Speed12 floors its reduction at5',effective_control_speed(12,[leash],target='hero'),5)
    check('Iron Leash floor never overrides Root',effective_control_speed(12,[leash,zero],target='hero'),0)
    master=slow('mastered-passive',amount=15,expires=12)
    glacier=slow('glacier',mode='half-minus',amount=5,expires=6)
    check('Mastered Glacier at30 is10, not5',f([master,glacier]),10)
    check('Ordinary passive beats unmastered Glacier atSpeed5',effective_control_speed(5,[a,half],target='hero'),0)
    check('Mastered passive and Glacier at10 do not go negative',effective_control_speed(10,[master,glacier],target='hero'),0)
    weaker=slow('later-passive',expires=18,profile='cold')
    refreshed=refresh_speed_record([a],weaker)
    check('One exact Focus profile refresh, not duplicate',len(refreshed),1)
    check('Refresh does not shorten its endpoint',refresh_speed_record(refreshed,replace(weaker,expires=9))[0].expires,18)
    held=refresh_speed_record([glacier],weaker)
    check('Distinct magnitude candidates remain independent',len(held),2)
    check('Later weaker profile cannot erase strong Glacier',f(held),10)
    check('Weaker profile resumes after Glacier expires',f(held,now=6),20)
    check('Cold profile owner identity prevents merged durations',len(refresh_speed_record([a],replace(weaker,owner='mage-B'))),2)
    check('Refresh does not end suppression',refresh_speed_record([replace(a,suppressed=True)],weaker)[0].suppressed,True)
    star=GuidingStarMark('oracle','enemy',18,3)
    check('Star owner cannot spend ally entitlement',star.ally_attack(actor='oracle',ally_of_owner=True,hit=True,now=1),{'attackBonus':0,'radiantBonus':0})
    check('First ally miss spends+2 only',star.ally_attack(actor='ally',ally_of_owner=True,hit=False,now=1),{'attackBonus':2,'radiantBonus':0})
    check('Next ally hit getsS without another+2',star.ally_attack(actor='ally2',ally_of_owner=True,hit=True,now=2),{'attackBonus':0,'radiantBonus':3})
    check('Consumed star supplies no third rider',star.ally_attack(actor='ally',ally_of_owner=True,hit=True,now=3),{'attackBonus':0,'radiantBonus':0})
    fresh=GuidingStarMark('oracle','enemy',18,3)
    check('Suppressed star does not spend entitlement',fresh.ally_attack(actor='ally',ally_of_owner=True,hit=True,now=1,suppressed=True),{'attackBonus':0,'radiantBonus':0})
    check('Suppressed entitlement remains',fresh.attack_bonus_available,True)
    check('Illegal attack spends no star',fresh.ally_attack(actor='ally',ally_of_owner=True,hit=True,now=1,legal=False),{'attackBonus':0,'radiantBonus':0})
    check('Star expires at exact endpoint',fresh.ally_attack(actor='ally',ally_of_owner=True,hit=True,now=18),{'attackBonus':0,'radiantBonus':0})
    brand=WrathfulBrand('oracle','enemy',18)
    check('Fully prevented owner hit does not trigger damaging-hit rider',brand.trigger(actor='oracle',ally_of_owner=True,now=1,actual_damage=0,direct_attack_hit=True,base_dice_total=9)['fireBonus'],0)
    check('Brand damage uses unmodified rolled base dice',brand.trigger(actor='oracle',ally_of_owner=True,now=2,actual_damage=12,direct_attack_hit=True,base_dice_total=9)['fireBonus'],4)
    check('Brand owner bonus cannot recur',brand.trigger(actor='oracle',ally_of_owner=True,now=3,actual_damage=12,direct_attack_hit=True,base_dice_total=9)['fireBonus'],0)
    check('First ally damage receives distinct heal/save entitlement',brand.trigger(actor='ally',ally_of_owner=True,now=4,actual_damage=1),{'fireBonus':0,'healD6':True,'wisdomSave':True})
    check('Blocked healing does not refund spent Brand entitlement',brand.trigger(actor='ally',ally_of_owner=True,now=5,actual_damage=1),{'fireBonus':0,'healD6':False,'wisdomSave':False})
    check('Consumed Brand riders do not end timed Brand itself',brand.active,True)
    hit=OneShotRider('hit')
    check('Drake/Soldier hit-based rider is not spent on miss',hit.trigger(qualifying=True,attack_roll=True),False)
    check('Hit-based rider spends even if actual damage0',hit.trigger(qualifying=True,attack_roll=True,hit=True,actual_damage=0),True)
    scan=OneShotRider('attack')
    check('Scanner spent by attack roll even miss',scan.trigger(qualifying=True,attack_roll=True,hit=False),True)
    reflect=PerTurnReflection(12)
    check('No Divine Judgment on off-turn damage',reflect.reflect(target_turn_id='one',actual_damage=20,on_target_turn=False),0)
    check('Zero damage does not consume reflection',reflect.reflect(target_turn_id='one',actual_damage=0,on_target_turn=True),0)
    check('First damage on turn reflects half',reflect.reflect(target_turn_id='one',actual_damage=9,on_target_turn=True),4)
    check('Second victim on same turn does not reflect again',reflect.reflect(target_turn_id='one',actual_damage=8,on_target_turn=True),0)
    check('Separate extra turn can reflect once',reflect.reflect(target_turn_id='extra',actual_damage=40,on_target_turn=True),12)
    check('Small actual damage still minimum1',reflect.reflect(target_turn_id='two',actual_damage=1,on_target_turn=True),1)
    base=dict(restrained=True,physical=True,explicit_escape=False,fixed_endpoint=False,special_cure=False)
    check('Physical fallback missingDC uses10',physical_escape_fallback(**base)['dc'],10)
    check('Physical fallback selects one record',physical_escape_fallback(**base)['scope'],'one selected restraint record')
    check('Helper fallback uses Athletics only',physical_escape_fallback(**base,helper=True)['checks'],['STR(Athletics)'])
    check('Fixed-duration source receives no invented escape',physical_escape_fallback(**{**base,'fixed_endpoint':True}),None)
    check('Magical restraint receives no physical fallback',physical_escape_fallback(**{**base,'physical':False}),None)
    check('Root receives no Restrained fallback',physical_escape_fallback(**{**base,'restrained':False}),None)
    check('Special cure protection controls fallback',physical_escape_fallback(**{**base,'special_cure':True}),None)
    check('Explicit source escape controls fallback',physical_escape_fallback(**{**base,'explicit_escape':True}),None)
    check('Nonmagical disease immunity excludes magical disease',disease_immunity_covers(classified_disease=True,magical=True,ordinary=True,scope='nonmagical-disease'),False)
    check('Ordinary disease immunity includes ordinary magical disease',disease_immunity_covers(classified_disease=True,magical=True,ordinary=True,scope='ordinary-disease'),True)
    check('Name alone supplies no disease immunity hook',disease_immunity_covers(classified_disease=False,magical=False,ordinary=True,scope='all-disease'),False)
    check('Repeat-save cure invents no saving throw',repeat_affliction_save(actual_record=True,source_allows_save=False,current_save_legal=True),False)
    check('Repeat save needs currently legal source save',repeat_affliction_save(actual_record=True,source_allows_save=True,current_save_legal=False),False)
    curse=dict(classified_curse=True,intrinsic_class_state=False,special_cure=False,ordinary_removable=True,curse_tier=2,remover_tier=3)
    check('Ordinary within-tier curse removable',generic_curse_removable(**curse),True)
    check('Unknown curse tier is not silently assigned',generic_curse_removable(**{**curse,'curse_tier':None}),False)
    check('Oracle intrinsic Curse not ordinary cleanse target',generic_curse_removable(**{**curse,'intrinsic_class_state':True}),False)
    check('Special curse cure cannot be bypassed',generic_curse_removable(**{**curse,'special_cure':True}),False)
    detect=dict(success=True,magical=True,actual_curse_metadata=True,protected=False)
    check('Analyze exposes permitted actual curse metadata',curse_metadata_visible(detection_method='analyze-magic',**detect),True)
    check('Identify does not automatically reveal curse',curse_metadata_visible(detection_method='identify',**detect),False)
    check('Detect Magic has no curse-detail grant',curse_metadata_visible(detection_method='detect-magic',**detect),False)
    check('Protected class Curse stays protected',curse_metadata_visible(detection_method='arcane-sight',**{**detect,'protected':True}),False)
    check('Extra turn does not manufacture repeat save',regular_control_step(regular_turn=False),False)
    check('Regular turn advances control clock',regular_control_step(regular_turn=True),True)
    check('Hypermutation protects captured walking baseline after Exhaustion',effective_control_speed(15,[a],target='hero',global_multiplier=Fraction(1,2),hypermutation_baseline=30),15)
    check('Hypermutation never defeats explicit root',f([zero],hypermutation_baseline=30),0)
    check('Hypermutation never defeats Core immobilization',f([],hypermutation_baseline=30,core_speed_zero=True),0)
    check('Hypermutation grants no absent mode',f([],hypermutation_baseline=60,mode_possessed=False),0)
    check('Captured swim floor differs from walking',effective_control_speed(5,[a],target='hero',hypermutation_baseline=20),10)
    check('New mode without snapshot gains no floor',effective_control_speed(5,[a],target='hero'),0)
    check('Zero from numeric slow differs from explicit Speed0',effective_control_speed(5,[a],target='hero',hypermutation_baseline=30),15)
    check('Current-turn off-turn entry uses actual turn end',current_turn_endpoint(application_time=2,actual_turn_end=3),3)
    check('End-trigger slow expires at that same end',current_turn_endpoint(application_time=3,actual_turn_end=3),3)
    check('No current turn uses six elapsed seconds',current_turn_endpoint(application_time=7),13)
    check('Balanced Elements extends from now not old deadline',balanced_elements_endpoint(12,18,owner_matches=True,elemental_control=True),18)
    check('Repeated extension cannot add another turn recursively',balanced_elements_endpoint(18,18,owner_matches=True,elemental_control=True),18)
    check('Longer existing deadline is never shortened by extension',balanced_elements_endpoint(24,18,owner_matches=True,elemental_control=True),24)
    check('Balanced Elements cannot outlive governing concentration',balanced_elements_endpoint(12,24,owner_matches=True,elemental_control=True,source_maximum=18),18)
    check('Balanced Elements cannot modify another owner record',balanced_elements_endpoint(12,18,owner_matches=False,elemental_control=True),12)
    check('Mundane Root has no inferred elemental metadata',balanced_elements_endpoint(12,18,owner_matches=True,elemental_control=False),12)
    check('Ash-bound forbids consenting to allied transport',ash_bound_teleport_allowed(willing=True,source_requires_willing=True,otherwise_legal=True),False)
    check('Ash-bound allows independently legal involuntary hostile displacement',ash_bound_teleport_allowed(willing=False,source_requires_willing=False,otherwise_legal=True),True)
    check('Ash-bound does not make illegal teleport legal',ash_bound_teleport_allowed(willing=False,source_requires_willing=False,otherwise_legal=False),False)
    records=[{'applicationId':'core','targetId':'hero','present':True,'tags':['classification.staggered']},
      {'applicationId':'monk','targetId':'hero','present':True,'suppressed':True,'tags':['classification.staggered']},
      {'applicationId':'plain-slow','targetId':'hero','present':True,'tags':['eligibility.slowed-foe']},
      {'applicationId':'other','targetId':'other','present':True,'tags':['classification.staggered']}]
    check('Sanctify removes suppressed Staggered but not unrelated slow',sanctify_staggered_records(records,target='hero'),['core','monk'])
    delay=lambda target,seq,snapshot=['a','b','c','d']:{'target':target,'applicationSequence':seq,'snapshot':snapshot}
    check('One initiative delay moves after next snapshot participant',delayed_round_order(['a','b','c','d'],[delay('b',1)]),['a','c','b','d'])
    check('Repeated delays on same target do not stack',delayed_round_order(['a','b','c','d'],[delay('b',1),delay('b',2)]),['a','c','b','d'])
    check('Removed neighbor skips to next surviving snapshot member',delayed_round_order(['a','b','d'],[delay('b',1)]),['a','d','b'])
    check('New entrant cannot become snapshot neighbor',delayed_round_order(['a','b','new','c','d'],[delay('b',1)]),['a','new','c','b','d'])
    check('Last participant delay leaves order unchanged',delayed_round_order(['a','b','c','d'],[delay('d',1)]),['a','b','c','d'])
    check('Chained delays use application sequence',delayed_round_order(['a','b','c','d'],[delay('b',2),delay('a',1)]),['a','c','b','d'])
    check('No pending delays restores canonical round',delayed_round_order(['a','b','c','d'],[]),['a','b','c','d'])
    rejects('Expired incoming record is not a legal refresh',lambda:refresh_speed_record([a],replace(weaker,expires=2),now=3))
    invariant_states=0
    for speed in range(101):
        for reduction in range(31):
            rec=slow('invariant',amount=reduction)
            for mode in ('flat','half','half-minus'):
                other=slow('other',mode=mode,amount=0 if mode=='half' else 5)
                result=effective_control_speed(speed,[rec,other],target='hero')
                assert 0<=result<=speed
                assert result==min(rec.result(speed),other.result(speed))
                assert effective_control_speed(speed,[rec,other],target='hero',global_multiplier=Fraction(1,2))==result//2
                invariant_states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW; selected helpers only',
        'scope':'Selected control lifecycle/arbitration interfaces, not full source/card execution or game-wide completion.',
        'checks':checks,'checkCount':len(checks),'speedInvariantStates':invariant_states}
    (ROOT/'docs/mechanics/CONTROL_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"PASS {len(checks)} control checks; {invariant_states} Speed invariant states. Review pending.")


if __name__=='__main__': main()

```

### tools/validate_control_bindings.py

```python
"""Integrity/coverage of supplied bindings, not proof of full mechanical execution."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def main():
 data=json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
 coverage=json.loads((ROOT/'data/playtest/control_state_coverage.json').read_text(encoding='utf-8'))
 packets=[json.loads((GAME/'docs/audit/2026-10-08/full-game'/name).read_text(encoding='utf-8')) for name in ('CONTROL_STATE_SOURCE_PACKET.json','CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json')]
 expected={}
 for packet in packets:
  for r in packet['records']:
   kind=r['kind'];owner=r.get('owner','ordinary')
   ident=r['card']['id'] if kind=='class-card' else r['engineIndex'] if kind=='class-engine' else r['spellId']
   key=f'{kind}:{owner}:{ident}'
   if kind=='class-card': procedure={k:r['card'].get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
   elif kind=='class-engine':procedure={'effect':r['text']}
   else:procedure=r['operational']
   expected[key]=(r,procedure)
 bindings={b['bindingId']:b for b in data['bindings']}
 assert len(bindings)==len(data['bindings'])==219
 assert set(bindings)==set(expected)=={r['candidateId'] for r in coverage['candidates']}
 components={c['mechanicalId']:c for c in data['componentIndex']}
 assert len(components)==len(data['componentIndex'])
 definitions=json.loads((ROOT/'data/playtest/condition_playtests.json').read_text(encoding='utf-8'))['conditions']
 core={'core.'+d['id'] for d in definitions}
 counts={}
 for ident,b in bindings.items():
  source,procedure=expected[ident]
  assert b['sourcePath']==source['path'],ident
  assert b['sourceSha256']==source.get('sourceObjectSha256',source.get('textSha256',source.get('operationalSha256'))),ident
  assert b['sourceProcedure']==procedure,ident
  assert b['classification'] in ('STATE','APPLY','HOOK','BOOK','NONSTATE','DEFER','ALREADY'),ident
  counts[b['classification']]=counts.get(b['classification'],0)+1
  if b['classification'] in ('STATE','APPLY'):assert b['componentIds'],ident
  for component in b['componentIds']:
   assert component in components,(ident,component)
   assert ident in components[component]['applicationBindings'],(ident,component)
   if component.startswith('core.'):assert component in core,component
  for evidence in b['reviewEvidence']:assert (GAME/evidence).is_file(),evidence
 for c in components.values():
  assert len(c['applicationBindings'])==len(set(c['applicationBindings'])),c['mechanicalId']
  for ident in c['applicationBindings']:assert c['mechanicalId'] in bindings[ident]['componentIds']
 assert (ROOT/data['operationalGuide']).is_file()
 for ident in ('core.staggered','monk.echoing-guard.stagger','warrior.brutal-strike.stagger'):
  assert 'classification.staggered' in components[ident]['metadata']
 assert 'classification.elemental-control' not in components['shaman.flask.root']['metadata']
 assert 'eligibility.slowed-foe' not in components['core.restrained']['metadata']
 assert 'eligibility.slowed-foe' not in components['core.grappled']['metadata']
 report={'status':'PASS','scope':'219 supplied binding/source/coverage identities and component links. No complete-card execution, exhaustive-source or balance claim.',
         'sourceBindings':len(bindings),'componentIdentities':len(components),'classifications':counts,
         'issues':[],'reviewStatus':data['status']}
 (ROOT/'docs/mechanics/CONTROL_BINDING_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(f"PASS {len(bindings)} source bindings; {len(components)} component identities; exact procedures preserved.")


if __name__=='__main__':main()

```

## Source identity / classification / component bindings / current explicit overrides

```json
[{"bindingId":"class-card:cleric:cleric.base.judging-light","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:cleric:cleric.base.judgment.judgment","classification":"ALREADY","componentIds":["cleric.judged"],"operationalOverrides":[]},{"bindingId":"class-card:cleric:cleric.hero.saint.celestial-resurgence","classification":"DEFER","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:cleric:cleric.hero.priest.balanced-scales","classification":"STATE","componentIds":["cleric.balanced-scales.mark"],"operationalOverrides":[]},{"bindingId":"class-card:cleric:cleric.hero.priest.word-of-binding","classification":"STATE","componentIds":["cleric.word-of-binding.damage-hook","cleric.word-of-binding.speed-zero","core.silenced"],"operationalOverrides":[]},{"bindingId":"class-card:cleric:cleric.hero.priest.divine-judgment","classification":"STATE","componentIds":["cleric.divine-judgment.mark"],"operationalOverrides":["Reflection triggers once each actual target turn, including extra turns, only first positive actual damage. Ordered victim resolution before damage, no summed victims. Off-turn damage none. Repeat saves/maximum expiry remain regular markers."]},{"bindingId":"class-card:cleric:cleric.hero.cultist.ritual-of-undeath","classification":"DEFER","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:crimson-agent:3","classification":"ALREADY","componentIds":["crimson-agent.blood-mark"],"operationalOverrides":[]},{"bindingId":"class-engine:crimson-agent:6","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.base.blood-mark","classification":"ALREADY","componentIds":["crimson-agent.blood-mark"],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.arch.rupture-trigger","classification":"ALREADY","componentIds":["crimson-agent.bleed"],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.arch.rupture","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.hero.bloodweaver.purify-blood","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.hero.shadow-operative.phantom-strike","classification":"ALREADY","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.hero.thirstborn.hemorrhagic-plague","classification":"ALREADY","componentIds":["crimson-agent.bleed"],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.hero.thirstborn.carrion-conductor","classification":"STATE","componentIds":["crimson-agent.carrion-conductor.corpse-mark","crimson-agent.carrion-conductor.used-corpse"],"operationalOverrides":["Separate persistent source-specific used-corpse history survives expiration/consumption/suppression; no second Carrion use by any owner. No universal ban on unrelated corpse mechanics."]},{"bindingId":"class-card:dragoon:dragoon.base.draconic-discipline","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:dragoon:dragoon.hero.dragon-guardian.aegis-leap","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:dragoon:dragoon.hero.drake-rider.drake-mark","classification":"STATE","componentIds":["dragoon.drake-mark"],"operationalOverrides":[]},{"bindingId":"class-card:dragoon:dragoon.hero.dragon-tyrant.tyrant-s-impale","classification":"STATE","componentIds":["core.restrained","dragoon.bleed","dragoon.tyrants-impale.restraint"],"operationalOverrides":[]},{"bindingId":"class-engine:druid:6","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.base.panther-form-stealth","classification":"STATE","componentIds":["core.grappled","druid.panther.grapple"],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.hero.timeless-body","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.hero.land.nature-s-ward","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.hero.land.tanglemaw","classification":"STATE","componentIds":["core.restrained","druid.tanglemaw.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.hero.thorns.tanglemaw","classification":"STATE","componentIds":["core.restrained","druid.tanglemaw.restraint","druid.thorns-tanglemaw.restrained-damage"],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.arch.winterfang.winter-s-embrace","classification":"STATE","componentIds":["druid.winters-embrace.slow"],"operationalOverrides":["Slow ends at current triggering actual turn end. No turn underway:6 elapsed seconds; printed once/enemy/round cap retained."]},{"bindingId":"class-card:druid:druid.hero.winterfang.snow-leopard","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:druid:druid.hero.rotshaper.carrion-rat-king","classification":"APPLY","componentIds":["core.poisoned"],"operationalOverrides":[]},{"bindingId":"class-engine:mage:16","classification":"DEFER","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.hero.archmage.purifying-beam","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.hero.lich.undead-immunities","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:mirrorsage:mirrorsage.hero.light-weaver.light-binding","classification":"STATE","componentIds":["core.restrained","mirrorsage.light-binding.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:mirrorsage:mirrorsage.hero.light-weaver.purifying-reflection","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:mirrorsage:mirrorsage.hero.mirror-mage.reflected-repertoire","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:monk:8","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:monk:18","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:monk:monk.base.stunning-strike","classification":"APPLY","componentIds":["core.stunned","monk.stunning-strike.reaction-denial"],"operationalOverrides":[]},{"bindingId":"class-card:monk:monk.hero.enlightened-master.serenity-breaker-palm","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:monk:monk.hero.enlightened-master.healing-touch","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:monk:monk.hero.enlightened-master.purifying-palm","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:monk:monk.hero.way-of-shadow.nerve-strike","classification":"STATE","componentIds":["monk.nerve-strike.reaction-bonus-denial","monk.nerve-strike.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:2","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:3","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:15","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:16","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:17","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:20","classification":"STATE","componentIds":["oracle.curse-manifestation.self-state"],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:21","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:22","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:oracle:24","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.oracle-s-curse","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.curse-manifestation","classification":"STATE","componentIds":["oracle.curse-manifestation.self-state"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.oracle-s-burden","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.curse-boon-i","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.ability-score-improvement-oracle-4","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.curse-boon-ii","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.curse-boon-iii","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.curse-boon-iv","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shared.curse-boon-v","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.spiral-touched.spiral-touched-boon-ii","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.curse.soul-cracked","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.soul-cracked.soul-cracked-boon-v","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.burning-blood.burning-blood-boon-i","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.burning-blood.burning-blood-boon-ii","classification":"ALREADY","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.curse.false-life","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.battle.mark-of-the-doomed","classification":"ALREADY","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.bones.bone-whisper","classification":"STATE","componentIds":["core.incapacitated","oracle.bone-whisper.soft-fallback"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.bones.ledger-s-memory","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.flame.wrathful-brand","classification":"STATE","componentIds":["oracle.wrathful-brand","oracle.wrathful-brand.attack-penalty"],"operationalOverrides":["Owner damage bonus needs actual positive pre-bonus attack damage. One shared ally-positive-damage entitlement for heal attempt+WIS save; no refund from prevented healing. Timed Brand can persist after riders spent."]},{"bindingId":"class-card:oracle:oracle.supplement.flame.purging-flame","classification":"STATE","componentIds":["oracle.purging-flame.undead-attack-penalty"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.flame.zealot-s-renewal","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.life.thorned-shelter","classification":"STATE","componentIds":["oracle.thorned-shelter.buff","oracle.thorned-shelter.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.life.garden-of-restoration","classification":"STATE","componentIds":["oracle.garden-of-restoration.undead-attack-penalty","oracle.garden-of-restoration.zone"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.life.bloom-oracle","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.life.life-revelation-mastery","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.shadow.marquis-s-glimpse","classification":"STATE","componentIds":["oracle.marquis-glimpse.hard-control","oracle.marquis-glimpse.soft-fallback"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.stars.guiding-bolt","classification":"STATE","componentIds":["oracle.guiding-bolt.star-mark"],"operationalOverrides":["Two independent entitlements: next ally-other-than-owner attack+2 spends on roll; next qualifying ally hit addsS and ends mark, including after a prior miss. Paid reapplication resets both without stacking."]},{"bindingId":"class-card:oracle:oracle.supplement.stars.constellation-mark","classification":"STATE","componentIds":["oracle.constellation-mark"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.stars.omen-reader","classification":"STATE","componentIds":["oracle.omen-reader.star-ash"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.stars.concord-alignment","classification":"STATE","componentIds":["oracle.concord-alignment.aura"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.stars.stars-revelation-mastery","classification":"STATE","componentIds":["oracle.guiding-bolt.enhanced-slow"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.time.rewind-wound","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.time.paradox-skin","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:paladin:2","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.base.lay-on-hands","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.base.sacred-touch","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.divine-health","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-mercy.sanctify-ground","classification":"HOOK","componentIds":[],"operationalOverrides":["Selecting Staggered ends ALL present classification.staggered records on selected creature, including suppressed records. One named cleansing choice per creature per pulse; no immunity against later applications."]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.vengeful-smite","classification":"ALREADY","componentIds":["paladin.vengeance-mark.smite"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.aura-of-judgment","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.judgment-brand","classification":"ALREADY","componentIds":["paladin.vengeance-mark.judgment-brand"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.mark-of-retribution","classification":"ALREADY","componentIds":["paladin.vengeance-mark.retribution"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.relentless-pursuit","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.sentence-of-doom","classification":"STATE","componentIds":["paladin.sentence-of-doom.empowerment"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.no-escape","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-vengeance.final-verdict","classification":"STATE","componentIds":["paladin.final-verdict.hp-prohibition"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-dominion.binding-word","classification":"STATE","componentIds":["core.restrained","paladin.binding-word.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.purifying-smite","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.aura-of-purification","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.holy-inferno","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.cleansing-brand","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.zealot-s-flame","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.sanctified-immolation","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-flame.purifying-crown","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.ancient-smite","classification":"STATE","componentIds":["paladin.ancients.root"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.thorn-crown","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.roots-of-memory","classification":"STATE","componentIds":["core.restrained","paladin.roots-of-memory.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.primordial-surge","classification":"STATE","componentIds":["paladin.ancients.root"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.primordial-crown","classification":"STATE","componentIds":["paladin.ancients.root","paladin.primordial-crown.attack-target-restriction"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-chain.linked-ward","classification":"STATE","componentIds":["paladin.linked-ward.link"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-chain.chain-of-duty","classification":"STATE","componentIds":["paladin.chain-of-duty.link"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash","classification":"STATE","componentIds":["paladin.iron-leash.action-denial","paladin.iron-leash.reaction-denial","paladin.iron-leash.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-grief.mourning-smite","classification":"ALREADY","componentIds":["paladin.grief-mark"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-grief.sorrow-s-weight","classification":"STATE","componentIds":["paladin.sorrows-weight.slow"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.liberating-smite","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.aura-of-liberation","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.righteous-quake","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.break-bonds","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.shatter-shackles","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.revolution-s-cry","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.unbound-host","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-chains-broken.liberty-unbound","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes-aura","classification":"STATE","componentIds":["paladin.reign-of-ashes-aura.buff-suppression","paladin.reign-of-ashes-aura.slow"],"operationalOverrides":[]},{"bindingId":"class-engine:ranger:0","classification":"STATE","componentIds":["ranger.track-target.quarry"],"operationalOverrides":[]},{"bindingId":"class-engine:ranger:4","classification":"STATE","componentIds":["ranger.emberroot.burn","ranger.glacial-thorn.speed-zero","ranger.venomlash.damage-penalty"],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.base.track-target","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.arch.pathfinder-s-mark","classification":"STATE","componentIds":["ranger.pathfinders-mark.location"],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.arch.predator-s-mark","classification":"STATE","componentIds":["ranger.predators-mark.upgrade"],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.hero.warder.rootcall-quake","classification":"STATE","componentIds":["ranger.rootcall-quake.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.hero.outrider.toxic-affinity","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.hero.outrider.venom-rain","classification":"APPLY","componentIds":["core.poisoned"],"operationalOverrides":[]},{"bindingId":"class-card:ranger:ranger.hero.outrider.plague-bearer","classification":"APPLY","componentIds":["core.poisoned"],"operationalOverrides":[]},{"bindingId":"class-engine:shaman:1","classification":"STATE","componentIds":["shaman.flame-totem.burn","shaman.frost-totem.slow"],"operationalOverrides":["Frost slow current triggering actual turn end; no turn underway6sec. Printed entry/start and once/creature/round caps unchanged."]},{"bindingId":"class-engine:shaman:4","classification":"STATE","componentIds":["core.stunned","shaman.flask.burn","shaman.flask.reaction-denial","shaman.flask.root","shaman.flask.weaken"],"operationalOverrides":[]},{"bindingId":"class-card:shaman:shaman.base.flask-use","classification":"BOOK","componentIds":["shaman.flask.burn"],"operationalOverrides":[]},{"bindingId":"class-card:shaman:shaman.arch.enhanced-elemental-attunement","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:shaman:shaman.hero.theurgist.summon-ice-wisp","classification":"STATE","componentIds":["shaman.ice-wisp.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-engine:soldier:1","classification":"STATE","componentIds":["soldier.overwatch.bleed","soldier.overwatch.snare"],"operationalOverrides":[]},{"bindingId":"class-card:soldier:soldier.arch.suppression-fire","classification":"STATE","componentIds":["soldier.suppression-fire.slow"],"operationalOverrides":[]},{"bindingId":"class-card:soldier:soldier.arch.hold-the-line","classification":"STATE","componentIds":["soldier.hold-the-line.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-card:soldier:soldier.hero.champion.guardian-s-rush","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:soldier:soldier.hero.champion.divine-lockdown","classification":"STATE","componentIds":["soldier.divine-lockdown.reaction-denial","soldier.divine-lockdown.slow","soldier.divine-lockdown.speed-zero"],"operationalOverrides":[]},{"bindingId":"class-card:soldier:soldier.hero.artillerist.net-bolt","classification":"STATE","componentIds":["core.restrained","soldier.net-bolt.large-slow","soldier.net-bolt.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:soldier:soldier.hero.tyrant.marked-for-death","classification":"STATE","componentIds":["soldier.marked-for-death"],"operationalOverrides":[]},{"bindingId":"class-card:thief:thief.arch.crippling-strike","classification":"STATE","componentIds":["thief.crippling-strike.slow"],"operationalOverrides":[]},{"bindingId":"class-engine:tinker:3","classification":"STATE","componentIds":["core.stunned","tinker.burn-injector.burn","tinker.poison-vents.attack-penalty","tinker.target-scanner.mark","tinker.target-taunter.attack-penalty"],"operationalOverrides":[]},{"bindingId":"class-engine:tinker:5","classification":"STATE","componentIds":["tinker.cryo.speed-zero","tinker.glue.slow","tinker.overload-core.reaction-denial","tinker.shock.construct-reaction-denial","tinker.shock.verbal-block"],"operationalOverrides":["Glue slow current triggering actual turn end, not invented next regular turn. No turn underway6sec. Other bomb components retain their own source clocks; Glue terrain lasts its independent3 rounds."]},{"bindingId":"class-engine:tinker:6","classification":"STATE","componentIds":["core.restrained","tinker.decoy-dummy.attack-penalty","tinker.net-trap.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:tinker:tinker.arch.bomb-specialization","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:tinker:tinker.arch.deploy-net-trap","classification":"STATE","componentIds":["core.restrained","tinker.net-trap.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:tinker:tinker.hero.warmachine.overpressure-bombs","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.base.brutality-sense","classification":"ALREADY","componentIds":["warrior.brutality-vulnerable"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.arch.brutality-momentum","classification":"ALREADY","componentIds":["warrior.brutality-vulnerable"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.hero.wardborn.stabilizing-injection","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.hero.ironskin.cellular-reconstruction","classification":"ALREADY","componentIds":["warrior.cellular-reconstruction.stasis"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.hero.dreadspawn.infectious-mutation","classification":"STATE","componentIds":["warrior.infectious-mutation.roll-penalty"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.supplement.shoulder-spike-cluster","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-engine:wizard:15","classification":"BOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.base.analyze-magic","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.arch.arcane-sight","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.spellbinder.sigil-authority","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.spellbinder.runic-snare","classification":"STATE","componentIds":["core.restrained","wizard.runic-snare.restraint"],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.necromancer.will-domination","classification":"APPLY","componentIds":["core.stunned","wizard.will-domination.reaction-denial"],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.necromancer.binding-sigil","classification":"STATE","componentIds":["wizard.binding-sigil.mark"],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.necromancer.infernal-pact-quest-based-unlock","classification":"STATE","componentIds":["wizard.gravebrand"],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.necromancer.mental-binding","classification":"STATE","componentIds":["core.charmed","wizard.mental-binding.command"],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.necromancer.arcane-domination","classification":"STATE","componentIds":["core.charmed","wizard.arcane-domination.command","wizard.arcane-domination.reaction-denial"],"operationalOverrides":[]},{"bindingId":"class-card:wizard:wizard.hero.necromancer.mind-prison","classification":"STATE","componentIds":["core.incapacitated","wizard.mind-prison.command","wizard.mind-prison.reaction-denial","wizard.mind-prison.slow"],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:dispel-minor","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:seal-minor-wound","classification":"ALREADY","componentIds":[],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:earthen-grip","classification":"APPLY","componentIds":["core.restrained","ordinary.earthen-grip.restraint"],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:elemental-bolt","classification":"NONSTATE","componentIds":[],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:aura-glimpse","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:identify","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:detect-magic","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:ray-of-frost","classification":"STATE","componentIds":["ordinary.ray-of-frost.slow"],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:frost-arrow","classification":"STATE","componentIds":["ordinary.frost-arrow.slow"],"operationalOverrides":[]},{"bindingId":"ordinary-spell:ordinary:feather-fall","classification":"ALREADY","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:crimson-agent:crimson-agent.hero.shadow-operative.veinjammer","classification":"STATE","componentIds":["crimson-agent.veinjammer.concentration-penalty","crimson-agent.veinjammer.slow"],"operationalOverrides":[]},{"bindingId":"class-card:dragoon:dragoon.hero.drake-rider.drakestorm-dive","classification":"STATE","componentIds":["dragoon.burn","dragoon.drakestorm-dive.cold-slow","dragoon.drakestorm-dive.reaction-denial"],"operationalOverrides":["Cold slow and lightning Reaction denial: SOURCE next regular END, correcting earlier discussion. Fire uses existing independent periodic binding."]},{"bindingId":"class-card:dragoon:dragoon.hero.drake-rider.elemental-lance","classification":"STATE","componentIds":["dragoon.elemental-lance.cold-slow","dragoon.elemental-lance.opportunity-denial"],"operationalOverrides":["Cold slow: SOURCE next regular END. Lightning opportunity-attack denial: TARGET next regular START. Preserve distinct clocks."]},{"bindingId":"class-card:mage:mage.base.elemental-bolt","classification":"STATE","componentIds":["mage.cold-focus.flat","mage.elemental-bolt.burn"],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.base.cold.cold","classification":"STATE","componentIds":["mage.cold-focus.flat","mage.cold-focus.glacier"],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.arch.elemental-mastery","classification":"HOOK","componentIds":["mage.fire-focus.burn","mage.inferno-lance.burn"],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.arch.elemental-surge","classification":"STATE","componentIds":["mage.cold-focus.flat","mage.fire-focus.burn"],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.hero.elementalist.elemental-fusion","classification":"STATE","componentIds":["mage.elemental-fusion.burn","mage.elemental-fusion.opportunity-denial","mage.elemental-fusion.reaction-denial","mage.elemental-fusion.slow"],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.hero.elementalist.cascade-storm","classification":"STATE","componentIds":["mage.cascade-storm.burn","mage.cascade-storm.cold-slow","mage.cascade-storm.reaction-denial"],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.hero.elementalist.elemental-mastery","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:mage:mage.hero.lich.undying-spellform","classification":"STATE","componentIds":["mage.undying-spellform.mobility-cap"],"operationalOverrides":[]},{"bindingId":"class-card:monk:monk.arch.tortoise.echoing-guard","classification":"STATE","componentIds":["monk.echoing-guard.stagger"],"operationalOverrides":["Custom -1 attacks/-5Speed only; not Core Staggered. classification.staggered for named readers/removers. Strongest same-style attack penalty, no addition with Warrior version."]},{"bindingId":"class-card:monk:monk.arch.pressure-point-strike","classification":"STATE","componentIds":["monk.pressure-point.arm","monk.pressure-point.leg"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.bones.ledger-s-command","classification":"STATE","componentIds":["oracle.ledger-command.control","oracle.ledger-command.soft-fallback"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.bones.bones-revelation-mastery","classification":"HOOK","componentIds":[],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.cataclysm.tremor-sense","classification":"STATE","componentIds":["core.prone","oracle.tremor-sense.slow"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.cataclysm.shardburst","classification":"STATE","componentIds":["core.prone","oracle.shardburst.slow"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.cataclysm.gale-of-unmaking","classification":"STATE","componentIds":["oracle.gale-of-unmaking.slow"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.cataclysm.seal-s-fracture","classification":"STATE","componentIds":["oracle.seals-fracture.backlash"],"operationalOverrides":[]},{"bindingId":"class-card:oracle:oracle.supplement.dream.slumber-glimpse","classification":"STATE","componentIds":["oracle.slumber-glimpse.action-denial","oracle.slumber-glimpse.attack-bonus","oracle.slumber-glimpse.initiative-penalty","oracle.slumber-glimpse.reaction-denial","oracle.slumber-glimpse.soft-fallback"],"operationalOverrides":["Initiative-2 is next eligible roll/check before encounter end; no existing-slot change. Retain separate original hard/fallback and next-attack riders."]},{"bindingId":"class-card:oracle:oracle.supplement.life.resonant-seed","classification":"STATE","componentIds":["oracle.resonant-seed.slow"],"operationalOverrides":["Slow ends at end of actual triggering turn, including off-turn entry or extra turn. No turn underway:6 elapsed seconds. Printed per-creature/round pulse cap retained."]},{"bindingId":"class-card:oracle:oracle.supplement.time.moment-s-pause","classification":"STATE","componentIds":["oracle.moments-pause.action-denial","oracle.moments-pause.initiative-delay","oracle.moments-pause.reaction-denial","oracle.moments-pause.soft-fallback"],"operationalOverrides":["Pending next-numbered-round canonical snapshot delay, nonstack per target. Stable application order, move after first surviving later snapshot participant, ignore new entrants. No duplicate/lost turns or changes to virtual markers. Guide procedure controls."]},{"bindingId":"class-card:oracle:oracle.supplement.time.the-spiral-opens","classification":"STATE","componentIds":["oracle.spiral-opens.forced-echo"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oathbreaker-shared.black-manifestation","classification":"STATE","componentIds":["paladin.black-manifestation.reaction-denial","paladin.black-manifestation.slow"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-dominion.law-s-weight","classification":"STATE","componentIds":["paladin.laws-weight.control"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-dominion.decree-of-submission","classification":"STATE","componentIds":["core.charmed","core.frightened","paladin.decree-of-submission.command","paladin.decree-of-submission.soft-fallback"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.echo-of-ages","classification":"STATE","componentIds":["paladin.echo-of-ages.attack-denial","paladin.echo-of-ages.soft-fallback"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-ancients.standing-stone","classification":"STATE","componentIds":["paladin.standing-stone.slow"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash-aura","classification":"STATE","componentIds":["paladin.iron-leash-aura.movement-limit","paladin.iron-leash-aura.slow"],"operationalOverrides":[]},{"bindingId":"class-card:paladin:paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes","classification":"STATE","componentIds":["paladin.reign-of-ashes.ash-bound"],"operationalOverrides":["Operative its-next-turn wins over summary: target next regular END. Half-Speed/noDash/no willing teleport benefit, including consent to allied transport. Legal involuntary hostile teleport remains source-governed."]},{"bindingId":"class-card:paladin:paladin.supplement.oath-of-the-martyr-king.royal-decree","classification":"STATE","componentIds":["core.prone","paladin.royal-decree.choice"],"operationalOverrides":[]},{"bindingId":"class-card:shaman:shaman.base.elemental-affinity","classification":"STATE","componentIds":["shaman.elemental-affinity.ice-slow"],"operationalOverrides":["Ice slow: SOURCE next regular END. Enhanced Attunement replaces5 with10, not another slow."]},{"bindingId":"class-card:shaman:shaman.hero.theurgist.elemental-chorus","classification":"STATE","componentIds":["shaman.elemental-chorus.slow"],"operationalOverrides":["Slow: SOURCE next regular END, correcting earlier discussion."]},{"bindingId":"class-card:shaman:shaman.hero.soothsayer.balanced-elements","classification":"HOOK","componentIds":[],"operationalOverrides":["Owned explicitly classified elemental control may include legal multiclass sources. No Shaman-class-only restriction. Extend from NOW to target following regular end, max with existing endpoint, capped by governing source/concentration maximum; no recursive deadline addition. Actual elemental membership in guide/metadata."]},{"bindingId":"class-card:thief:thief.hero.shadowblade.vein-cutter","classification":"STATE","componentIds":["thief.vein-cutter.attack-damage-penalty","thief.vein-cutter.bleed","thief.vein-cutter.slow"],"operationalOverrides":[]},{"bindingId":"class-card:thief:thief.hero.blackguard.crippling-lash","classification":"STATE","componentIds":["thief.crippling-lash.slow","thief.crippling-lash.weapon-hit-damage-penalty"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.base.brutal-strike","classification":"STATE","componentIds":["warrior.brutal-strike.stagger"],"operationalOverrides":["Custom -1 attacks/-5Speed only; not Core Staggered. classification.staggered for named readers/removers. Strongest same-style attack penalty, no addition with Monk version."]},{"bindingId":"class-card:warrior:warrior.arch.mutation-overload","classification":"STATE","componentIds":["warrior.mutation-overload.backlash"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.supplement.stonecore","classification":"STATE","componentIds":["warrior.stonecore.speed-side-effect"],"operationalOverrides":[]},{"bindingId":"class-card:warrior:warrior.supplement.hypermutation-spike","classification":"STATE","componentIds":["warrior.hypermutation-spike.speed-floor"],"operationalOverrides":["Snapshot each possessed movement mode ordinary sheet Speed, including currently qualifying persistent passive modifiers. Exclude temporary/systemic changes. Half-baseline floor after numeric penalties, no explicit zero/absent-mode/movement-prohibition bypass. Incapacitated itself does not set Speed0 and floor grants no Actions."]}]
```

## Exact metadata index

```json
[{"mechanicalId":"cleric.judged","metadata":[]},{"mechanicalId":"cleric.balanced-scales.mark","metadata":[]},{"mechanicalId":"cleric.word-of-binding.damage-hook","metadata":[]},{"mechanicalId":"cleric.word-of-binding.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"core.silenced","metadata":[]},{"mechanicalId":"cleric.divine-judgment.mark","metadata":[]},{"mechanicalId":"crimson-agent.blood-mark","metadata":[]},{"mechanicalId":"crimson-agent.bleed","metadata":[]},{"mechanicalId":"crimson-agent.carrion-conductor.corpse-mark","metadata":[]},{"mechanicalId":"crimson-agent.carrion-conductor.used-corpse","metadata":[]},{"mechanicalId":"dragoon.drake-mark","metadata":[]},{"mechanicalId":"core.restrained","metadata":[]},{"mechanicalId":"dragoon.bleed","metadata":[]},{"mechanicalId":"dragoon.tyrants-impale.restraint","metadata":[]},{"mechanicalId":"core.grappled","metadata":[]},{"mechanicalId":"druid.panther.grapple","metadata":[]},{"mechanicalId":"druid.tanglemaw.restraint","metadata":[]},{"mechanicalId":"druid.thorns-tanglemaw.restrained-damage","metadata":[]},{"mechanicalId":"druid.winters-embrace.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"core.poisoned","metadata":[]},{"mechanicalId":"mirrorsage.light-binding.restraint","metadata":[]},{"mechanicalId":"core.stunned","metadata":[]},{"mechanicalId":"monk.stunning-strike.reaction-denial","metadata":[]},{"mechanicalId":"monk.nerve-strike.reaction-bonus-denial","metadata":[]},{"mechanicalId":"monk.nerve-strike.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.curse-manifestation.self-state","metadata":[]},{"mechanicalId":"core.incapacitated","metadata":[]},{"mechanicalId":"oracle.bone-whisper.soft-fallback","metadata":[]},{"mechanicalId":"oracle.wrathful-brand","metadata":[]},{"mechanicalId":"oracle.wrathful-brand.attack-penalty","metadata":[]},{"mechanicalId":"oracle.purging-flame.undead-attack-penalty","metadata":[]},{"mechanicalId":"oracle.thorned-shelter.buff","metadata":[]},{"mechanicalId":"oracle.thorned-shelter.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.garden-of-restoration.undead-attack-penalty","metadata":[]},{"mechanicalId":"oracle.garden-of-restoration.zone","metadata":[]},{"mechanicalId":"oracle.marquis-glimpse.hard-control","metadata":[]},{"mechanicalId":"oracle.marquis-glimpse.soft-fallback","metadata":[]},{"mechanicalId":"oracle.guiding-bolt.star-mark","metadata":[]},{"mechanicalId":"oracle.constellation-mark","metadata":[]},{"mechanicalId":"oracle.omen-reader.star-ash","metadata":[]},{"mechanicalId":"oracle.concord-alignment.aura","metadata":[]},{"mechanicalId":"oracle.guiding-bolt.enhanced-slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.vengeance-mark.smite","metadata":[]},{"mechanicalId":"paladin.vengeance-mark.judgment-brand","metadata":[]},{"mechanicalId":"paladin.vengeance-mark.retribution","metadata":[]},{"mechanicalId":"paladin.sentence-of-doom.empowerment","metadata":[]},{"mechanicalId":"paladin.final-verdict.hp-prohibition","metadata":[]},{"mechanicalId":"paladin.binding-word.restraint","metadata":[]},{"mechanicalId":"paladin.ancients.root","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.roots-of-memory.restraint","metadata":[]},{"mechanicalId":"paladin.primordial-crown.attack-target-restriction","metadata":[]},{"mechanicalId":"paladin.linked-ward.link","metadata":[]},{"mechanicalId":"paladin.chain-of-duty.link","metadata":[]},{"mechanicalId":"paladin.iron-leash.action-denial","metadata":[]},{"mechanicalId":"paladin.iron-leash.reaction-denial","metadata":[]},{"mechanicalId":"paladin.iron-leash.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.grief-mark","metadata":[]},{"mechanicalId":"paladin.sorrows-weight.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.reign-of-ashes-aura.buff-suppression","metadata":[]},{"mechanicalId":"paladin.reign-of-ashes-aura.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"ranger.track-target.quarry","metadata":[]},{"mechanicalId":"ranger.emberroot.burn","metadata":[]},{"mechanicalId":"ranger.glacial-thorn.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"ranger.venomlash.damage-penalty","metadata":[]},{"mechanicalId":"ranger.pathfinders-mark.location","metadata":[]},{"mechanicalId":"ranger.predators-mark.upgrade","metadata":[]},{"mechanicalId":"ranger.rootcall-quake.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"shaman.flame-totem.burn","metadata":[]},{"mechanicalId":"shaman.frost-totem.slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"shaman.flask.burn","metadata":[]},{"mechanicalId":"shaman.flask.reaction-denial","metadata":[]},{"mechanicalId":"shaman.flask.root","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"shaman.flask.weaken","metadata":[]},{"mechanicalId":"shaman.ice-wisp.speed-zero","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"soldier.overwatch.bleed","metadata":[]},{"mechanicalId":"soldier.overwatch.snare","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"soldier.suppression-fire.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"soldier.hold-the-line.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"soldier.divine-lockdown.reaction-denial","metadata":[]},{"mechanicalId":"soldier.divine-lockdown.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"soldier.divine-lockdown.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"soldier.net-bolt.large-slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"soldier.net-bolt.restraint","metadata":[]},{"mechanicalId":"soldier.marked-for-death","metadata":[]},{"mechanicalId":"thief.crippling-strike.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"tinker.burn-injector.burn","metadata":[]},{"mechanicalId":"tinker.poison-vents.attack-penalty","metadata":[]},{"mechanicalId":"tinker.target-scanner.mark","metadata":[]},{"mechanicalId":"tinker.target-taunter.attack-penalty","metadata":[]},{"mechanicalId":"tinker.cryo.speed-zero","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"tinker.glue.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"tinker.overload-core.reaction-denial","metadata":[]},{"mechanicalId":"tinker.shock.construct-reaction-denial","metadata":[]},{"mechanicalId":"tinker.shock.verbal-block","metadata":[]},{"mechanicalId":"tinker.decoy-dummy.attack-penalty","metadata":[]},{"mechanicalId":"tinker.net-trap.restraint","metadata":[]},{"mechanicalId":"warrior.brutality-vulnerable","metadata":[]},{"mechanicalId":"warrior.cellular-reconstruction.stasis","metadata":[]},{"mechanicalId":"warrior.infectious-mutation.roll-penalty","metadata":[]},{"mechanicalId":"wizard.runic-snare.restraint","metadata":[]},{"mechanicalId":"wizard.will-domination.reaction-denial","metadata":[]},{"mechanicalId":"wizard.binding-sigil.mark","metadata":[]},{"mechanicalId":"wizard.gravebrand","metadata":[]},{"mechanicalId":"core.charmed","metadata":[]},{"mechanicalId":"wizard.mental-binding.command","metadata":[]},{"mechanicalId":"wizard.arcane-domination.command","metadata":[]},{"mechanicalId":"wizard.arcane-domination.reaction-denial","metadata":[]},{"mechanicalId":"wizard.mind-prison.command","metadata":[]},{"mechanicalId":"wizard.mind-prison.reaction-denial","metadata":[]},{"mechanicalId":"wizard.mind-prison.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"ordinary.earthen-grip.restraint","metadata":[]},{"mechanicalId":"ordinary.ray-of-frost.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"ordinary.frost-arrow.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"crimson-agent.veinjammer.concentration-penalty","metadata":[]},{"mechanicalId":"crimson-agent.veinjammer.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"dragoon.burn","metadata":[]},{"mechanicalId":"dragoon.drakestorm-dive.cold-slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"dragoon.drakestorm-dive.reaction-denial","metadata":[]},{"mechanicalId":"dragoon.elemental-lance.cold-slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"dragoon.elemental-lance.opportunity-denial","metadata":[]},{"mechanicalId":"mage.cold-focus.flat","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"mage.elemental-bolt.burn","metadata":[]},{"mechanicalId":"mage.cold-focus.glacier","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"mage.fire-focus.burn","metadata":[]},{"mechanicalId":"mage.inferno-lance.burn","metadata":[]},{"mechanicalId":"mage.elemental-fusion.burn","metadata":[]},{"mechanicalId":"mage.elemental-fusion.opportunity-denial","metadata":[]},{"mechanicalId":"mage.elemental-fusion.reaction-denial","metadata":[]},{"mechanicalId":"mage.elemental-fusion.slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"mage.cascade-storm.burn","metadata":[]},{"mechanicalId":"mage.cascade-storm.cold-slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"mage.cascade-storm.reaction-denial","metadata":[]},{"mechanicalId":"mage.undying-spellform.mobility-cap","metadata":[]},{"mechanicalId":"monk.echoing-guard.stagger","metadata":["eligibility.slowed-foe","classification.staggered"]},{"mechanicalId":"monk.pressure-point.arm","metadata":[]},{"mechanicalId":"monk.pressure-point.leg","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.ledger-command.control","metadata":[]},{"mechanicalId":"oracle.ledger-command.soft-fallback","metadata":[]},{"mechanicalId":"core.prone","metadata":[]},{"mechanicalId":"oracle.tremor-sense.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.shardburst.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.gale-of-unmaking.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.seals-fracture.backlash","metadata":[]},{"mechanicalId":"oracle.slumber-glimpse.action-denial","metadata":[]},{"mechanicalId":"oracle.slumber-glimpse.attack-bonus","metadata":[]},{"mechanicalId":"oracle.slumber-glimpse.initiative-penalty","metadata":[]},{"mechanicalId":"oracle.slumber-glimpse.reaction-denial","metadata":[]},{"mechanicalId":"oracle.slumber-glimpse.soft-fallback","metadata":[]},{"mechanicalId":"oracle.resonant-seed.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"oracle.moments-pause.action-denial","metadata":[]},{"mechanicalId":"oracle.moments-pause.initiative-delay","metadata":[]},{"mechanicalId":"oracle.moments-pause.reaction-denial","metadata":[]},{"mechanicalId":"oracle.moments-pause.soft-fallback","metadata":[]},{"mechanicalId":"oracle.spiral-opens.forced-echo","metadata":[]},{"mechanicalId":"paladin.black-manifestation.reaction-denial","metadata":[]},{"mechanicalId":"paladin.black-manifestation.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.laws-weight.control","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"core.frightened","metadata":[]},{"mechanicalId":"paladin.decree-of-submission.command","metadata":[]},{"mechanicalId":"paladin.decree-of-submission.soft-fallback","metadata":[]},{"mechanicalId":"paladin.echo-of-ages.attack-denial","metadata":[]},{"mechanicalId":"paladin.echo-of-ages.soft-fallback","metadata":[]},{"mechanicalId":"paladin.standing-stone.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.iron-leash-aura.movement-limit","metadata":[]},{"mechanicalId":"paladin.iron-leash-aura.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.reign-of-ashes.ash-bound","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"paladin.royal-decree.choice","metadata":[]},{"mechanicalId":"shaman.elemental-affinity.ice-slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"shaman.elemental-chorus.slow","metadata":["eligibility.slowed-foe","classification.elemental-control"]},{"mechanicalId":"thief.vein-cutter.attack-damage-penalty","metadata":[]},{"mechanicalId":"thief.vein-cutter.bleed","metadata":[]},{"mechanicalId":"thief.vein-cutter.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"thief.crippling-lash.slow","metadata":["eligibility.slowed-foe"]},{"mechanicalId":"thief.crippling-lash.weapon-hit-damage-penalty","metadata":[]},{"mechanicalId":"warrior.brutal-strike.stagger","metadata":["eligibility.slowed-foe","classification.staggered"]},{"mechanicalId":"warrior.mutation-overload.backlash","metadata":[]},{"mechanicalId":"warrior.stonecore.speed-side-effect","metadata":[]},{"mechanicalId":"warrior.hypermutation-spike.speed-floor","metadata":[]},{"mechanicalId":"core.staggered","metadata":["classification.staggered"]}]
```
