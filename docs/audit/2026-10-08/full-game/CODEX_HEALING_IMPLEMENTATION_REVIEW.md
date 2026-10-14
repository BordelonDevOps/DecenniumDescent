# Exact healing/death implementation review

Codex → Calibration Review. User asks us to continue through every aspect. This is the next bounded exact review after your first, supplement and final-boundary decisions. Original class/book objects remain unchanged. Please inspect the actual guide, helpers, tests, source dispositions and all6 spell objects below. Give concrete contradictions/bugs before accepting this scope. Do NOT close whole DD24,131 other matches, temporal world rules or the game.

Current verification:155 selected healing checks plus120 unchanged Core damage states,150 control checks plus9,393 Speed states,98 custom tests,153 source integrity records. Six spells remain inactive outside batch_*.json. Please review each six-spell object individually for later operational promotion, retaining preserved class/rank/RP metadata from the source conferences.

Two exact questions remain: (1) Passive Reserve-bound regeneration at Critical/fullHP can compute excess while restoring0/spending0 reserve. Does Cosmic Equilibrium accept such a packet? I recommend explicit exclusion of unpaid passive regeneration from excess conversion; otherwise a source that says Reserve bounds regeneration could generate radiant damage with no Reserve spend. The current helper calculates quantity only and requires separately validated converter eligibility. (2) SpiralIII phase-out survives if its later fatal Wound is prevented by an independent Ward, because actual death never occurred. Please confirm/reject.

New strictness: healing causal applications use a shared root ledger across sibling branches, not just per-path visited copies, to enforce once/application/root. The temporal helper ONLY tests selected participant fields; topology/equipment/clock issues are explicitly deferred. Lethal track reconciliation is an explicit required post-success call, not hidden in unrelated systems.

Please also inspect death-save reroll before commit, zeroHP Ward/dead identity behavior, non-damage direct death, delayed FalseLifeV, cure-presence correction, would-die metrics and all source-specific restrictions. Request missing source evidence if needed; do not infer unavailable fields.


## Candidate guide
# Healing, survival and resurrection — working candidate

**IN REVIEW: exact implementation.** Three notebook conferences classify147 class sources and propose6 individual ordinary spell objects. Those spells remain inactive until individual review. This is a bounded interface, not DD24 completion:131 additional semantic matches and healing content in other domains still need dispositions. Original cards/books are preserved.

[Exact source procedures](HEALING_DEATH_SOURCE_BINDINGS.md) · [Latest boundary decisions](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_BOUNDARIES.md) · [Supplement decisions](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_SUPPLEMENT_REVIEW.md) · [Reference checks](HEALING_PLAYTEST_VALIDATION.json) · [Source integrity](HEALING_DEATH_SOURCE_VALIDATION.json)

## Distinct life operations

| Operation | Result | Restriction interface |
|---|---|---|
| Minimum-HP prevention | Preserve positiveHP instead of crossing a floor | Not HP gain; cannot create positiveHP from0 |
| Ordinary healing | Increase a living creature's normalHP | Apply modifiers, prohibitions, reserve and Critical ceiling |
| Direct state recovery | Specifically defined dying/Stable/HP recovery | Broad cannot-regain-HP applies; ordinary healing modifiers do not |
| Would-die replacement | Replace a pending death before it becomes final | Exact source eligibility; not a generic damage floor |
| Resurrection | Actually dead willing identity returns at printedHP | Separate life transition; actual corpse/soul blockers apply |
| Companion reconstruction | Restore a device/companion through its own source | No general creature resurrection permission |
| TemporaryHP | Separate nonstacking buffer | Not healing, stabilization or resurrection |

Names never select the operation. Phoenix Rebirth heals a still-living ally at0. Cleric Resurrection returns an actual dead identity. Ritual of Undeath's Ward replaces death; ordinary Death Ward is a positive-to-zero floor. Feign death and spirit manifestations are not death or resurrection.

## Damage quantities and resolution

| Quantity | Definition and use |
|---|---|
| resolvedDamage | After defenses, before tempHP; positive damage event iff greater than0 |
| tempAbsorbed | min(tempHP, resolvedDamage) |
| postTempDamage | resolvedDamage minus tempAbsorbed, uncapped by currentHP; Core Instant Death/Wounds |
| actualHpDamage | NormalHP lost to the packet after true prevention; recovery and state-assignment loss excluded |
| actualDamageDealt | NEW anti-overkill bridge: tempAbsorbed plus actualHpDamage; numeric actual-damage drains/reflections |

Ordinary “damages,” “takes damage” and “damaging hit” predicates use a positive resolved packet. Actual-HP wording (Burning Blood/Rewind Wound) uses actualHpDamage. Numeric actual-damage wording (Sanguine Rite/Echo Leech/Merciful Smite/Wound Eater/Gravebrand) uses actualDamageDealt. Source attack/hit predicates remain distinct.

Example: HP10/temp10 takes5: numeric actual damage5, actualHP damage0, positive packet. HP1 under a floor takes5: numeric0 but positive packet. HP3 takes12: numeric3, raw post-temp12. HP0 takes1: numeric0, positive packet and normal death-failure consequences.

Divine Judgment consumes its once-this-actual-target-turn entitlement on a positive packet, then reflects min(Cleric level, max(1, floor(actualDamageDealt/2))). Thus HP1-floor/numeric0 reflects1 and consumes; fully prevented resolved0 does neither. Wrathful Brand/Balanced Scales use the positive predicate where their source says damage occurred.

Resolve a damage event in this order:

1. Snapshot pre-event HP/tempHP/Wounds; resolve defenses, temp absorption and uncapped post-temp damage.
2. Core Instant Death uses postTempDamage minus preHP greater than or equal to effective maximum when reduced to0. It precedes ordinary floors. Open a legal would-die replacement; stop that packet's death procedure. No Wound save or zero-HP failure follows this branch.
3. If not Instant Death, resolve applicable true floors. They cannot raise an already0 creature. They preserve raw damage and attached conditions; a prevented drop creates no drop-only Wound trigger, but half-max/Maiming still applies.
4. Spiral-TouchedIII alone has a specific pre-Wound recovery exception. If positive-to-zero remains, spend its use, preserve that raw crossing trigger, attempt quarter-max direct recovery and apply phase-out. Broad HP-gain prohibition blocks the recovery but not the use/phase.
5. Resolve the one Core Wound save using original post-temp damage and pre-event Wounds. Fatal Wound death opens its own legal replacement window. Actual death ends Spiral phase; a successful independent Ward prevents actual death.
6. Resolve already-zero damage failures/death and its legal replacement window. A successful replacement stops skipped same-packet death branches; never replay a Wound/failure branch merely because replacement changedHP.
7. Finalize a newly surviving0 creature's dying/Stable/knockout state. Only an explicitly triggered post-zero Reaction such as Grace Reversal can act before ordinary zeroHP Reaction loss finalizes.
8. Resolve eligible post-zero Phoenix/Unyielding-style healing only if target still lives, followed by later triggers. This healing never retroactively reduces the triggering packet's numeric damage.

The affected creature chooses among simultaneously eligible offered survival effects, then rechecks remaining triggers. A paid Reaction spends its declared cost; a limited automatic survival use spends when its actual source resolves. A true floor preventing the crossing means Spiral's use is not spent. No generic extra Reaction or return from death is created.

For Ritual Ward, sufficient body and no explicitly unpreventable death are prerequisites. It can intercept Instant Death, fatal Wounds, third death-save failure, eligible direct death and lethal tracks. Positive pre-eventHP→1 is loss prevention and works through Decay. Already0 with HP gain prohibited instead becomes living Stable0: clear counters and establish a d4-hour recovery deadline immediately.

Freeze packetHpLossBeforeReplacement after true floors but before Ward. Ward metrics are min(packetHpLossBeforeReplacement, max(0, preHP minus replacementHP)); never include loss caused solely by assigning a lowerHP state. HP20 takes10 then fatal Wound/Ward1 means actualHP damage10, not19. HP5 takes100 then Ward1 means actualHP damage4, raw100.

Direct death (e.g. Wound EaterIII) produces no damage or Wound save. Its healing requires actual death; a Ward interception prevents that trigger without refunding the paid activation. False LifeI has only its printed floor and failed-death-save replacement modes sharing1/LR; it is not an all-causes Ward.

## ZeroHP permissions and start timing

A conscious but dying creature still rolls at each regular start unless Stable. Extra turns do not advance these regular-start deadlines. Further damage and actual death retain normal consequences.

Mage Undying Spellform partially overrides only zeroHP Unconscious/Incapacitated restrictions: normal speech, voluntary half-Speed movement, normal Action, legal spellcasting with that Action, and starting/maintaining concentration. No independent BA/Reaction. Existing concentration avoids automatic loss from zeroHP, but the triggering damage still requires its concentration save. Separate Stunned/Unconscious/Expedition5 or6/Silence and other restrictions still apply. Healing above0 ends the feature. Expiry at0 destabilizes, cancels the Stable recovery deadline and adds one failure; the third kills normally and permits only an eligible would-die replacement.

Oracle False LifeIII permits exactly one choice during the allowed zeroHP turn: move up to Speed, speak, or activate one Revelation. The latter uses its printed Action/BA/trigger (trigger must occur on that turn), costs and components. It can start concentration; the feature did not preserve earlier concentration. No independent actions accompany the choice.

False LifeV quarter-max direct recovery resolves at its next regular start before the death save. Blocked recovery leaves0 without invented stability; dead creatures do not revive. Spiral phase expires at its next regular start before normal start processing. Fate-BoundIV rerolls a failed death save before committing natural1/counters; use the new result. Its generic death-effect save bonus is not an ordinary death-save modifier.

## Ordinary healing arithmetic

Determine legal source, recipients, costs, clocks and available entitlements before arithmetic. The helper receives already eligible modifiers; it does not acquire class powers or validate every source for its caller.

Pre-resolution modifiers include Words of Equilibrium's formula M, Zealot's Fervor +S, Throne's Grace +1/die capped S+M, Benevolent Spirits' eligible paid-technique +M, Life Prophecy maximizing dice, and Crane's applicable +S. Conditional add-ons include Ground, Radiance, Aura of Faith, Ember Mantle, Life Linked's rolled1d4, Ranger Healing Touch, Aura of Mercy, Garden's stored+1 and Tranquil Lotus Step.

First compute without conditional add-ons. Only if this preview actually restores at least1HP, recompute that same event once with its eligible add-ons. The preview changes no pools/uses. Base5 minus5 plus a conditional3 remains0; eligible pre-resolution Benevolent3 yields3. Multiple flat class bonuses use the strongest across both passes unless an explicit source exception allows stacking. Rolled extra dice/per-die changes are separate.

Within each permitted reduction plan: formula/bonuses; per-die adjustments; compatible exact fractional multipliers with one floor after multiplication; compatible flat reductions; floor at0; broad HP prohibition; maximum/Critical/reserve caps. Intrinsic Wound Eater and systemic Corrupted remain independent factors. Duplicate same-stat per-die penalties use the strongest. Dice remain dice when maximized/shared; flat Lay on Hands and stored numeric Echoes have zero healing dice.

Blight Totem cannot compound other local healing reducers. Compare systemic factors plus Totem-half alone against systemic factors plus all otherwise compatible local reducers; use the lower result. Compatible halves multiply, compatible distinct flat penalties add, duplicate same-profile groups use strongest. Suppressed reducers do not participate.

Every present, operative, applicable next-positive-healing reduction consumes exactly once when the final event commits if its pre-reduction HP potential was positive. This includes reducers whose arithmetic branch lost to Totem or whose actual gain was later blocked. Zero potential and suppressed records consume none. Two-pass preview never consumes twice.

Critical at3Wounds caps ordinary healing at max(1, effective maximum minus1); it is not a maximumHP reduction and healing cannot lower currentHP. Reserve spends only actualHP restored. A final heal8 with room3 spends3 reserve; blocked healing spends0, other activation costs remain paid. Revival/form changes/encounter starts do not replenish reserve.

## Recovery gates, triggers and loops

False Life curse gates another creature's healing SPELL: optional Insight vs RevelationDC; success permits; failed or declined check rolls d2,1 blocks HP and2 permits. Nonspell recovery and independent nonHP components remain distinct. Burning Blood blocks the cold-tagged HP-healing component only, not independent tempHP/stabilization/resurrection.

Actual positiveHP restoration is required for Radiance's cure, Renewal's Stamina, Sanctified Reprisal and Life Prophecy's RC trigger. Meditative Healing's laterKi and Transcendent Meditation's second-pulseKi are independent components and still resolve when healing caps/blocks. Blood Tithe uses its actual qualifying hostile Bleed-death trigger and finite use; not staged farming.

Passive regeneration includes Bloodthick Node, Rapid Coagulation, Regenerative Mutation and Bio-Stabilizer's modification; these retain Reserve. Finite paid/limited pulses such as Aura of Grace, Living Pulse, Renewal Totem, Blood Feast, Exsanguinate, Hemostasis, Transcendent Meditation, Cellular Reconstruction and Adrenal Floodgate are not passive regeneration. Their own Downed/Incapacitated gates remain. A passive-regeneration prohibition is not a universal healing prohibition.

Lay on Hands retains its5×Paladin-level finite pool and ordinary Long Rest refill. Base Action spends at most level on one target; Hero1/SR spends the entire remaining pool across at most3, each allocation at least1. No RP conversion. Verdict Absolute's explicit qualifying brand-kill refill is a source exception.

Transfusion donor spends K normalHP; recipient ordinary base is K+floor(K/2). Channel Life spends X; baseX. Donor must remain at least1, tempHP cannot pay, loss is not damage and cannot be prevented/redirected/refunded when recipient gets0. Recipient legal bonuses/reductions apply.

Secondary healing retains root ID and visited application IDs in a shared causal ledger, including across sibling branches. Each link/application can fire at most once/root. Numeric add-ons remain the same packet, creating no new root/child. Legal finite primary healing may trigger unrelated eligible effects.

Stronger source flags override generic provenance: Vitality Link's child blocks every further link; Echo Leech blocks secondary healing/resource triggers; Blood Feast blocks damage/resource triggers; Merciful Smite blocks Smite/heal-copy chains; Crown Undying blocks redirection/heal-copy chains; Echoes/Spiral copies retain their explicit exclusions. Source payment and direct/actual-gain predicates still apply before a child exists.

## Excess healing

OrdinaryMissingHP = effective maximum minus currentHP. Genuine excess is max(0, legal post-reduction healing minus OrdinaryMissingHP). Broad HP prohibition makes legal healing and excess0. Critical's ceiling does not redefine missingHP: max20/HP19/Critical/legalheal10 restores0 but has9 genuine excess; the missing1 is not excess. At HP20, legalheal10 has10 excess.

This quantity alone grants no conversion. A legal converter must satisfy its own costs/caps/cadences. One excess point can fund only one conversion. Source-internal Overflowing Light resolves before outside Cosmic Equilibrium uses remaining excess. Channel Life attaches a packet-wide prohibition on ALL excess-to-tempHP conversion, including another owner's feature. It permits an otherwise eligible Cosmic damage conversion.

**Exact-review question:** Passive Reserve-based healing can produce a computed excess quantity while restoring0 and spending0 reserve. Do those particular sources qualify for Cosmic conversion at all? No conversion is authorized by the arithmetic helper; this eligibility must be resolved before activating that combination.

## Actual resurrection and retained consequences

Require an actually dead, willing identity, legal source body/anchor, location, target limit, elapsed window, paid cost and no applicable resurrection/soul blocker. ReturnedHP is a life transition, unaffected by ordinary healing multipliers or generic living HP-gain prohibitions. Explicit corpse-local and identity/soul blockers are different scopes.

Preserve Wounds/Injuries, Corruption, intrinsic Oracle Curse, debt/legal-death/body claims and spent resources. ThreeWounds is Critical, not continuous automatic death. Clear death counters/Stable deadline but preserve used turn markers and persistent histories. No duplicate creature or resource refresh.

| Class source | Exact selected procedure |
|---|---|
| Cleric Resurrection | Touch one eligible allied body, dead≤60seconds;1HP and printed2S+M tempHP1minute;3Conviction+10RP;1/LR |
| Celestial Resurgence | Up to6 eligible allied corpses30ft, dead≤18elapsedseconds;1HP;5Conviction+10RP;1/LR |
| Divine Rebirth | One successful resurrection by your Cleric feature instead max(1,floor(effectiveMax/2))HP plus printedS+M tempHP1minute;1/LR |
| Thousand Petals | At most6total including at most2eligible corpses20ft;5Ki+5RP;1/LR. Living3S d8+M healing, dead1HP. Corpse died strictly after previous source regular end. Printed floor until next source start |
| Grace Reversal | Source Reaction on surviving positive→0;10RP;one other eligible allied corpse in Oath aura since previous source regular end; Paladin stays0 |
| Soulbound Ritual / Snap Rebuild | Companion/device reconstruction via exact token/slot/expiry restrictions; no generic creature revival |

Thousand Petals revival history is campaign-persistent per Monk-owner/target identity; another Monk/source remains independent. Grace Reversal history is per Paladin-owner/target until that Paladin's qualifying Long Rest. Death of either participant resets neither. Living healing does not spend resurrection history.

Elapsed windows are inclusive (exact60seconds qualifies); previous-end windows are strictly after that typed phase20 marker through the current event. Initiative changes do not rewrite history.

## Lethal tracks after return or replacement

Both an actual resurrection and would-die replacement retain lethal tracks. Exhaustion6 becomes protected exhaustion.lethal-collapse: alive, Unconscious, no voluntary act/travel. Its static lethal endpoint is suspended for this protected return, ending once legally below6. A qualifying Long Rest can occur unconscious with another creature's care/food/water, inactive root cause and no recovery blocker.

Expedition6 retains all six provenance-bearing points and enters its existing collapse. Only genuine24hour Haven care or explicit eligible treatment can reduce it; point removal gates persist. A later positive unprevented gain at6 reevaluates either track's lethal endpoint. A fresh independently legal finite Ward may intervene; collapse is not continuing immunity.

## Removing suppressed Bleed and fire

Cures examine present, unexpired, not-ended records, including temporary suppression/acquired immunity. Initial immunity that prevented application leaves nothing to cure. Damage arbitration and active hooks still exclude suppressed/immune records.

Medicine selects one present eligible Bleed before rolling its printed/source/fallbackDC. A legal positive-potential magical heal invokes every present applicable Bleed endpoint; each Blood Curse instead receives its printedCON save. An actualHP-gain prerequisite still controls a source that expressly requires it.

A legal extinguish Action/full immersion ends all present ordinary-extinguishable fires within its scope; protected/special prerequisite fires persist. A permitted per-record fire DEX ending save remains available while suppressed when a future tick remains; no extra save after the final consumed tick. Cured records never resume when suppression ends.

## Six ordinary spell candidates — inactive until exact review

All retain preserved Action/RP/rank/class gates, and range120ft except Ward60ft. V/S/F uses the established M/F focus alternative; no imported material cost.

| Spell | Proposed individual operation |
|---|---|
| Stitch Fate | Rank8/21RP. Living dying0, not Stable/dead. Remove one recorded failure, or direct1HP recovery/clear counters; blocked latter becomes Stable0 with immediate d4-hour deadline. Not retrospective death undo |
| Death Ward | Rank4/7RP, concentration1minute. One positive-to-zero floor at1, then ends. No Instant Death/fatalWound/thirdfailure/lethal-track protection and no already0 recovery |
| Resurrection | Rank7/17RP. One willing identity, sufficient in-range remains, death≤8elapsedhours; return1HP and retained consequences/collapse |
| Mass Resurrection Denial | Rank8/21RP. Fixed20ft-radius sphere, concentration1minute (NEW supersedes Instantaneous). Corpse-local anchor block while remains inside; movement out/conc end/eligible rank8 removal ends block. Bodyless legal formation is not automatically blocked |
| True Resurrection | Rank9/26RP. One actually dead willing known identity, death≤7elapsed days. Usable in-range body or perceived legal unoccupied formation space120ft. Return1HP; every other remains anchor loses eligibility to duplicate that identity. No true-name or guessed soul-plane knowledge requirement |
| Soul Bind | Rank9/26RP, no concentration. Living dying0 perceived targetCHA save; failed save pending60seconds. PositiveHP/Stable ends pending. Death strictly before expiry creates bound identity for24hours from death. Exact expiry wins. One family record per identity; second legal failed save refreshes pending deadline, no post-death recast. Caster death/incapacity does not end it |

Soul Bind removal targets pending creature or existing post-death remains as local anchor. With no remains, removal must expressly free the bound identity/soul; invent no physical anchor. No mind control, ownership or indefinite prison. True Resurrection still obeys actual identity/soul barriers, and an already-living identity is ineligible. Complete objects retain countering, Dissonance/Refrain, costs and source access.

## Temporal dependency and validation boundary

Spiral-TouchedV Time Loop is temporal restoration, not generic resurrection. Its discussed participant contract restores recorded position, life/death/HP/temp/counters, Wounds/linked Injuries, Core/custom conditions, RC, per-encounter uses and snapshot Soul Bind state. Post-snapshot death/body destruction is conceptually undone; already-dead-at-snapshot remains dead. Generic corpse-resurrection denial does not automatically block it.

It does not restore RP/Ki/Conviction/BG, device resources, Mutation Reserve, daily/rest uses, physical consumables or its own spent use. The helper tests that field distinction only. Full equipment/environment topology, corpse/body-part duplication and clock rebasing remain in the dedicated temporal package; Time Loop is not declared fully operational by these tests.

Current selected checks:155 healing/death plus120 unchanged Core damage states;150 control including2 new clarification cases;98 custom including14 cure-presence cases;153 exact source records. These are interface tests, not execution of147 complete class cards, numerical balance, whole-game completion or a substitute for human playtesting.


## tools/healing_playtest_rules.py
```
"""Selected healing/death interfaces under review; not a full ability engine.

Callers validate source ownership, actions, costs, actual targets, time/location,
body/soul eligibility and use history. These helpers do not create authorization,
restore resources or decide the campaign's soul cosmology.
"""
from dataclasses import dataclass, replace, field
from copy import deepcopy
from fractions import Fraction
from core_playtest_rules import LifeState, heal, kill, stabilize, saving_throw, death_save, roll_inputs
from spell_playtest_rules import integer, SpellRuleError
from control_playtest_rules import clock_marker,require_deadline,END_EFFECT_EXPIRY


@dataclass(frozen=True)
class HealingReduction:
    application_id: str
    group: str
    kind: str
    value: int | Fraction
    present: bool = True
    suppressed: bool = False
    next_healing: bool = False

    def __post_init__(self):
        if not self.application_id or not self.group:raise SpellRuleError('Reduction identity/group required')
        if self.kind not in ('factor','flat','per-die','blight-totem'):
            raise SpellRuleError('Unreviewed healing reduction')
        if self.kind in ('factor','blight-totem'):
            if not isinstance(self.value,Fraction) or not 0<=self.value<=1:
                raise SpellRuleError('Healing factors must be exact fractions from0 through1')
            if self.kind=='blight-totem' and self.value!=Fraction(1,2):
                raise SpellRuleError('Supplied Blight Totem profile is exactly one-half')
        else:integer(self.value,'healing reduction',0)


def healing_packet(state, base, *, dice_count=0, pre_flat_bonuses=(),
                   conditional_flat_bonuses=(), conditional_dice_total=0,
                   conditional_dice_count=0, per_die_bonus=0, per_die_bonus_cap=None,
                   systemic_factors=(), reductions=(), hp_gain_prohibited=False,
                   reserve=None):
    """Pure two-pass arithmetic for ALREADY ELIGIBLE modifiers/reducers.

    Base includes the printed formula and legal pre-resolution rolled dice.
    Flat class bonuses use strongest across pre/conditional sets. Callers own
    source limits, dice rolls, costs, next-heal consumption, copy/trigger rights,
    legal converters and per-round budgets. Excess is quantity, not permission.
    """
    for name,value in [('base',base),('dice count',dice_count),('conditional dice',conditional_dice_total),
                       ('conditional dice count',conditional_dice_count),('per-die bonus',per_die_bonus)]:
        integer(value,name,0)
    for value in tuple(pre_flat_bonuses)+tuple(conditional_flat_bonuses):integer(value,'flat bonus',0)
    if per_die_bonus_cap is not None:integer(per_die_bonus_cap,'per-die bonus cap',0)
    if reserve is not None:integer(reserve,'remaining recovery reserve',0)
    system=Fraction(1)
    for factor in systemic_factors:
        if not isinstance(factor,Fraction) or not 0<=factor<=1:
            raise SpellRuleError('Systemic factors require exact reduction fractions')
        system*=factor
    if len({r.application_id for r in reductions})!=len(reductions):
        raise SpellRuleError('One application may enter healing once')
    live=[r for r in reductions if r.present and not r.suppressed]
    groups={}
    for r in live:
        if r.group in groups and groups[r.group].kind!=r.kind:
            raise SpellRuleError('A reduction group cannot mix unreviewed profiles')
        previous=groups.get(r.group)
        if previous is None or (r.value<previous.value if r.kind in ('factor','blight-totem') else r.value>previous.value):
            groups[r.group]=r
    ordinary=[r for r in groups.values() if r.kind!='blight-totem']
    totem=any(r.kind=='blight-totem' for r in groups.values())
    def calculate(use_conditional):
        count=dice_count+(conditional_dice_count if use_conditional else 0)
        flat=max(tuple(pre_flat_bonuses)+(tuple(conditional_flat_bonuses) if use_conditional else ()),default=0)
        die_bonus=count*per_die_bonus
        if per_die_bonus_cap is not None:die_bonus=min(die_bonus,per_die_bonus_cap)
        potential=base+flat+die_bonus+(conditional_dice_total if use_conditional else 0)
        per_die=max((r.value for r in ordinary if r.kind=='per-die'),default=0)
        factor=system
        for r in ordinary:
            if r.kind=='factor':factor*=r.value
        adjusted=max(0,potential-count*per_die)
        ordinary_amount=max(0,(adjusted*factor).__floor__()-sum(r.value for r in ordinary if r.kind=='flat'))
        plans=[('compatible-local',ordinary_amount)]
        if totem:plans.append(('blight-totem-alone',(potential*system*Fraction(1,2)).__floor__()))
        branch,reduced=min(plans,key=lambda item:item[1])
        legal=0 if hp_gain_prohibited else reduced
        healed,report=ordinary_healing(state,legal,reserve=reserve)
        return {'state':healed,'positivePotential':potential,'postReductionAmount':reduced,
                'legalAmount':legal,'ordinaryMissingHp':state.maximum_hp-state.hp,
                'genuineExcess':max(0,legal-(state.maximum_hp-state.hp)),
                'reductionBranch':branch,'diceCount':count,**report}
    preview=calculate(False)
    eligible=preview['actualHpGained']>0
    final=calculate(True) if eligible else preview
    return {**final,'conditionalAddonsQualify':eligible,
            'previewActualHpGained':preview['actualHpGained'],
            'nextHealingCandidates':[r.application_id for r in live if r.next_healing and preview['positivePotential']>0]}


def false_life_healing_blocked(*, other_creature_spell, insight_success=False, d2=None):
    if not other_creature_spell or insight_success:return False
    integer(d2,'False Life d2',1,2)
    return d2==1


def transfer_hp_cost(donor, amount, *, transfusion=False):
    """Caller checks source amount cap/use; spend non-damage HP before healing."""
    integer(amount,'donor normal-HP cost',1)
    if donor.dead or donor.hp<=amount:raise SpellRuleError('Donor must remain at least1 HP')
    return replace(donor,hp=donor.hp-amount),amount+amount//2 if transfusion else amount


@dataclass(frozen=True)
class SoulBind:
    identity: str
    stage: str
    expires: Fraction

    def __post_init__(self):
        if not self.identity or self.stage not in ('pending','bound'):
            raise SpellRuleError('Soul Bind needs identity and valid stage')
        object.__setattr__(self,'expires',clock_marker(self.expires).seconds)


def apply_soul_bind(state, identity, now, *, failed_save, existing=None):
    now=clock_marker(now).seconds
    if state.dead or state.stable or state.hp!=0:raise SpellRuleError('Soul Bind requires living dying0')
    if existing and existing.identity!=identity:raise SpellRuleError('Bind belongs to another identity')
    if not failed_save:return existing
    if existing and existing.expires>now and existing.stage!='pending':
        raise SpellRuleError('A living target cannot retain an active post-death bind')
    expiry=max(now+60,existing.expires if existing and existing.expires>now else now)
    return SoulBind(identity,'pending',expiry)


def resolve_soul_bind(bind, state, now):
    """Invoke on life transitions and expiry. Absolute expiry wins exact ties."""
    now=clock_marker(now).seconds
    if bind is None or now>=bind.expires:return None
    if bind.stage=='bound':return bind
    if state.dead:return SoulBind(bind.identity,'bound',now+86400)
    if state.stable or state.hp>0:return None
    return bind


def survival_damage_event(state, resolved_damage, *, floor=False,
                          ritual_ward=False, replacement_legal=True,
                          hp_gain_prohibited=False, spiral_iii=False,
                          constitution_save_modifier=0, wound_natural=None,
                          injury_d6=None, critical=False, maiming=False,
                          knockout=False, melee=False, stable_d4=None, now_seconds=0):
    """Core-compatible selected survival branches, with frozen damage metrics.

    Caller selects/pays a real available source before enabling a flag. This
    implements no feature acquisition, generic Reaction permission or bodily
    reconstruction. replacement_legal includes sufficient body and no express
    unpreventable-death exception. Post-zero healing is a subsequent operation.
    """
    integer(resolved_damage,'resolved damage',0)
    if state.dead:raise SpellRuleError('Dead target is not a living damage target')
    if knockout and not melee:raise SpellRuleError('Knockout requires melee')
    out=replace(state)
    before_hp,before_wounds=state.hp,len(state.wounds)
    absorbed=min(state.temp_hp,resolved_damage)
    post_temp=resolved_damage-absorbed
    out.temp_hp-=absorbed
    out.hp=max(0,before_hp-post_temp)
    packet_loss=before_hp-out.hp
    events={'resolvedDamage':resolved_damage,'positiveDamageEvent':resolved_damage>0,
            'tempAbsorbed':absorbed,'postTempDamage':post_temp,
            'actualHpDamage':packet_loss,'actualDamageDealt':absorbed+packet_loss,
            'woundSaves':0,'injuryRolls':0,'instantDeath':False,'deathFailuresAdded':0,
            'floorUsed':False,'wardUsed':False,'spiralUsed':False,'phaseOut':False,
            'postZeroWindow':False,'deathCause':None}
    def pending_death(cause):
        events['deathCause']=cause
        if ritual_ward and replacement_legal:
            replacement_hp=1 if before_hp>0 or not hp_gain_prohibited else 0
            out.dead=False;out.hp=replacement_hp;out.stable=False
            out.stable_until_seconds=None;out.death_successes=out.death_failures=0
            if replacement_hp==0:stabilize(out,stable_d4,now_seconds)
            events['wardUsed']=True
            events['actualHpDamage']=min(packet_loss,max(0,before_hp-replacement_hp))
            events['actualDamageDealt']=absorbed+events['actualHpDamage']
        else:
            kill(out)
            events['phaseOut']=False
        return out,events
    if out.hp==0 and post_temp-before_hp>=out.maximum_hp:
        events['instantDeath']=True
        return pending_death('instant-death')
    if floor and before_hp>0 and out.hp==0:
        out.hp=1;events['floorUsed']=True
    packet_loss=before_hp-out.hp
    events['actualHpDamage']=packet_loss
    events['actualDamageDealt']=absorbed+packet_loss
    crossing=before_hp>0 and out.hp==0
    if spiral_iii and crossing:
        events['spiralUsed']=True;events['phaseOut']=True
        if not hp_gain_prohibited:out=heal(out,max(1,out.maximum_hp//4))
    trigger=crossing or 2*post_temp>=out.maximum_hp or maiming
    if trigger:
        dc=max(10,post_temp//2)
        save=saving_throw(wound_natural,constitution_save_modifier-before_wounds,dc)
        events.update(woundSaves=1,woundDC=dc,woundTotal=save['total'])
        if not save['success']:
            if before_wounds==3:return pending_death('fatal-wound')
            injury=None
            if save['failureMargin']>=5:
                integer(injury_d6,'required Injury d6',1,6)
                injury=injury_d6;events['injuryRolls']=1
            out.wounds+=(injury,)
    if before_hp==0 and post_temp>0:
        out.stable=False;out.stable_until_seconds=None
        if not out.uses_death_saves:return pending_death('ordinary-npc-zero-damage')
        failures=2 if critical else 1
        out.death_failures=min(3,out.death_failures+failures)
        events['deathFailuresAdded']=failures
        if out.death_failures>=3:return pending_death('zero-hp-failures')
    if crossing and out.hp==0:
        if knockout:stabilize(out,stable_d4,now_seconds)
        elif not out.uses_death_saves:return pending_death('ordinary-npc-drop-zero')
        else:out.stable=False;out.stable_until_seconds=None
        events['postZeroWindow']=True
    return out,events


def ordinary_healing(state, amount, *, hp_gain_prohibited=False, reserve=None):
    """Apply an ALREADY MODIFIED ordinary amount, then ceiling/reserve limits.

    This does not yet calculate stacking, conditional bonuses, triggers or copies.
    Actual HP restoration alone spends an explicitly supplied finite reserve.
    """
    integer(amount,'final healing amount',0)
    if reserve is not None:integer(reserve,'remaining recovery reserve',0)
    available=amount if reserve is None else min(amount,reserve)
    out=heal(state,0 if hp_gain_prohibited else available)
    actual=out.hp-state.hp
    return out,{'actualHpGained':actual,'reserveSpent':actual if reserve is not None else 0,
                'reserveRemaining':None if reserve is None else reserve-actual}


def finish_undying_spellform(state):
    """Only the Mage feature's explicit expiry consequence; no generic zero rule."""
    out=replace(state)
    if out.dead or out.hp>0:return out
    if not out.uses_death_saves:
        raise SpellRuleError('This player-class interface requires death-save state')
    out.stable=False
    out.stable_until_seconds=None
    out.death_failures=min(3,out.death_failures+1)
    if out.death_failures==3:kill(out)
    return out


def zero_hp_permissions(state, feature, *, chosen_oracle_option=None):
    """Permissions from THIS active feature only; unrelated prohibitions remain.

    Caller establishes feature's active duration. Stable means no regular-start
    death save; consciousness alone never erases the dying state.
    """
    if feature not in ('mage.undying-spellform','oracle.false-life-iii'):
        raise SpellRuleError('Unreviewed conscious-at-zero source')
    if chosen_oracle_option not in (None,'move','speak','revelation'):
        raise SpellRuleError('Oracle selects one printed option')
    if state.dead or state.hp>0:
        return {'exceptionApplies':False}
    if feature=='mage.undying-spellform':
        return {'exceptionApplies':True,'action':True,'bonusAction':False,'reaction':False,
                'speech':True,'startConcentration':True,'preserveConcentrationAgainstZero':True,
                'damageConcentrationSaveStillRequired':True,
                'movementFraction':(1,2),'deathSaveDueAtRegularStart':not state.stable and state.uses_death_saves}
    return {'exceptionApplies':True,'chosenOption':chosen_oracle_option,
            'chooseExactlyOneOf':('move','speak','revelation'),
            'independentBonusAction':False,'independentReaction':False,
            'revelationUsesPrintedActivation':True,
            'startConcentration':chosen_oracle_option=='revelation',
            'preserveConcentrationAgainstZero':False,
            'deathSaveDueAtRegularStart':not state.stable and state.uses_death_saves}


def stitch_fate(state, mode, *, hp_gain_prohibited=False, stable_d4=None, now_seconds=0):
    """Draft Action resolution; never a retroactive reroll or resurrection."""
    if state.dead or state.stable or state.hp!=0 or not state.uses_death_saves:
        raise SpellRuleError('Stitch Fate requires a living dying creature')
    if mode=='unravel-failure':
        if state.death_failures==0:raise SpellRuleError('No recorded failure to remove')
        return replace(state,death_failures=state.death_failures-1)
    if mode!='stitch-life':raise SpellRuleError('Unknown Stitch Fate mode')
    if not hp_gain_prohibited:return heal(state,1)
    out=replace(state)
    stabilize(out,stable_d4,now_seconds)
    return out


def returned_hp(effective_maximum, *, divine_rebirth=False):
    integer(effective_maximum,'effective maximum HP',1)
    return max(1,effective_maximum//2) if divine_rebirth else 1


def resurrection_transition(state, amount, *, identity_willing,
                            source_eligibility_met, resurrection_blocked=False):
    """Apply a valid actual resurrection; source eligibility is external.

    This is not ordinary healing. It intentionally accepts neither healing
    multipliers nor a generic HP-gain prohibition. Explicit resurrection/soul
    blockers prevent it. Call reconcile_lethal_tracks on a successful return;
    caller retains external resource/use/identity history without resets.
    """
    integer(amount,'source returned HP',1,state.maximum_hp)
    if not state.dead:raise SpellRuleError('Actual resurrection requires a dead creature')
    if not identity_willing or not source_eligibility_met or resurrection_blocked:
        raise SpellRuleError('Resurrection eligibility fails; no automatic cost refund')
    return replace(state,hp=amount,dead=False,stable=False,death_successes=0,
                   death_failures=0,stable_until_seconds=None)


def death_within_elapsed_window(death_at, now, seconds):
    """Inclusive elapsed window. Never substitute a round counter for seconds."""
    duration=clock_marker(seconds)
    death_at,now=clock_marker(death_at),clock_marker(now)
    return death_at<=now and now.seconds-death_at.seconds<=duration.seconds


def death_since_previous_end(death_at, previous_end, now):
    """Strictly after the preserved previous regular-end event marker."""
    require_deadline(previous_end)
    if previous_end.phase!=END_EFFECT_EXPIRY:
        raise SpellRuleError('Previous regular end requires end phase')
    return clock_marker(previous_end)<clock_marker(death_at)<=clock_marker(now)


def would_die_transition(state, *, ritual_ward=False, replacement_legal=True,
                         hp_gain_prohibited=False, stable_d4=None, now_seconds=0):
    """One pending non-damage death, before finalization; never resurrection.

    Caller checks exact source eligibility (e.g. Wound Eater III living dying
    hostile0), pays its costs, and reconciles lethal tracks after replacement.
    This emits no damage, Wound save or damage-trigger entitlement.
    """
    if state.dead:raise SpellRuleError('Pending death replacement cannot target actual Dead')
    out=replace(state)
    if not ritual_ward or not replacement_legal:
        kill(out)
        return out,{'wardUsed':False,'actualDeath':True}
    hp=1 if state.hp>0 or not hp_gain_prohibited else 0
    out=replace(state,hp=hp,stable=False,stable_until_seconds=None,
                death_successes=0,death_failures=0)
    if hp==0:stabilize(out,stable_d4,now_seconds)
    return out,{'wardUsed':True,'actualDeath':False}


def death_save_with_survival(state, natural, *, regular_turn_id, regular=True,
                             modifier=0, failed_reroll=None, ritual_ward=False,
                             replacement_legal=True, hp_gain_prohibited=False,
                             stable_d4=None, now_seconds=0):
    """Caller supplies only modifiers explicitly applying to death saves.

    Fate-Bound's generic death-effect +2 is NOT automatically included. A legal
    failed reroll replaces the roll before any natural1/counter consequence.
    Other printed reroll/cadence requirements are external.
    """
    total=roll_inputs(natural,modifier)
    failed=natural==1 or (natural!=20 and total<10)
    if failed_reroll is not None:
        if not failed:raise SpellRuleError('Failed-death-save reroll requires a failed roll')
        roll_inputs(failed_reroll,modifier)
        natural=failed_reroll
    out=death_save(state,natural,regular_turn_id=regular_turn_id,regular=regular,
                   modifier=modifier,stable_d4=stable_d4,now_seconds=now_seconds)
    # Natural20 is direct HP recovery: broad gain prohibition, not ordinary
    # healing multipliers. It supplies no stability when blocked.
    if natural==20 and hp_gain_prohibited:
        out=replace(state,last_death_turn=regular_turn_id)
    ward=False
    if out.dead and ritual_ward and replacement_legal:
        pending=replace(state,last_death_turn=regular_turn_id)
        out,event=would_die_transition(pending,ritual_ward=True,
                                      hp_gain_prohibited=hp_gain_prohibited,
                                      stable_d4=stable_d4,now_seconds=now_seconds)
        ward=event['wardUsed']
    return out,{'resolvedNatural':natural,'rerollUsed':failed_reroll is not None,'wardUsed':ward}


def false_life_v_recovery(state, *, due, regular, hp_gain_prohibited=False):
    """Resolve at due regular START before its death save; never at extra start."""
    if not due or not regular:return replace(state),{'deadlineConsumed':False}
    if state.dead or state.hp>0:return replace(state),{'deadlineConsumed':True}
    out=replace(state) if hp_gain_prohibited else heal(state,max(1,state.maximum_hp//4))
    return out,{'deadlineConsumed':True}


@dataclass(frozen=True)
class ExhaustionState:
    level: int = 0
    lethal_collapse: bool = False

    def __post_init__(self):
        integer(self.level,'Exhaustion level',0,6)
        if self.lethal_collapse and self.level!=6:
            raise SpellRuleError('Lethal Exhaustion collapse requires level6')


def reconcile_lethal_tracks(life, exhaustion, expedition):
    """Invoke only after a legal resurrection or would-die replacement.

    Does not cure points or root causes. The result's collapse restrictions
    compose with independent conditions, regardless of positive returned HP.
    """
    if life.dead:raise SpellRuleError('A failed return cannot establish living collapse')
    ex=replace(exhaustion,lethal_collapse=exhaustion.level==6)
    exp=replace(expedition,collapsed=expedition.expedition==6)
    collapsed=ex.lethal_collapse or exp.collapsed
    return ex,exp,{'unconscious':collapsed,'voluntaryAct':not collapsed,'voluntaryTravel':not collapsed}


def exhaustion_gain(state, amount, *, prevented=False):
    """Return pending endpoint; caller resolves death/replacement before commit."""
    integer(amount,'new Exhaustion gain',0)
    if prevented or amount==0:return state,False
    level=min(6,state.level+amount)
    return ExhaustionState(level),level==6


def exhaustion_long_rest(state, *, qualifying_rest, care_food_water,
                         root_cause_inactive, recovery_blocked=False):
    if not (qualifying_rest and care_food_water and root_cause_inactive) or recovery_blocked:
        return state
    return ExhaustionState(max(0,state.level-1))


@dataclass
class RevivalHistory:
    """Persistent identities, not encounter-local tokens; death never resets."""
    thousand_petals: set = field(default_factory=set)
    grace_reversal: set = field(default_factory=set)

    def eligible(self, feature, owner, target):
        return (owner,target) not in self._history(feature)

    def _history(self,feature):
        if feature not in ('thousand-petals','grace-reversal'):
            raise SpellRuleError('Unreviewed resurrection history')
        return self.thousand_petals if feature=='thousand-petals' else self.grace_reversal

    def record_success(self,feature,owner,target):
        history=self._history(feature)
        if (owner,target) in history:raise SpellRuleError('This owner already revived this target')
        history.add((owner,target))

    def owner_long_rest(self,owner):
        self.grace_reversal={entry for entry in self.grace_reversal if entry[0]!=owner}


def thousand_petals_targets(living_ids,corpse_ids):
    ids=tuple(living_ids)+tuple(corpse_ids)
    if not ids or len(ids)>6 or len(corpse_ids)>2 or len(ids)!=len(set(ids)):
        raise SpellRuleError('Thousand Petals:1–6 distinct total targets, at most2 corpses')
    return ids


@dataclass
class IdentityReturnLedger:
    """One authoritative identity state; remains are anchors, never new people."""
    living_identities: set = field(default_factory=set)
    eligible_remains: dict = field(default_factory=dict)

    def true_resurrection(self,identity,life,*,willing,within_window,identity_known,
                          body_anchor=None,legal_formation_space=False,
                          resurrection_blocked=False):
        if identity in self.living_identities or not life.dead:
            raise SpellRuleError('Identity is already living')
        body_legal=body_anchor is not None and body_anchor in self.eligible_remains.get(identity,set())
        # Caller additionally verifies perceived/in-range/line-of-effect/sufficient
        # body or unoccupied legal formation position before supplying the anchor.
        eligible=within_window and identity_known and (body_legal or legal_formation_space)
        out=resurrection_transition(life,1,identity_willing=willing,
                                    source_eligibility_met=eligible,resurrection_blocked=resurrection_blocked)
        self.living_identities.add(identity)
        self.eligible_remains[identity]=set()
        return out


@dataclass
class HealingCommitLedger:
    committed_event_ids: set = field(default_factory=set)
    consumed_reducer_ids: set = field(default_factory=set)

    def commit(self,event_id,packet):
        if event_id in self.committed_event_ids:raise SpellRuleError('Healing event already committed')
        ids=set(packet['nextHealingCandidates'])
        if ids & self.consumed_reducer_ids:raise SpellRuleError('One-shot reducer already spent')
        self.committed_event_ids.add(event_id)
        self.consumed_reducer_ids.update(ids)
        return ids


@dataclass
class ExcessLedger:
    remaining: int
    forbid_temp_hp: bool = False
    internal_resolved: bool = False

    def __post_init__(self):integer(self.remaining,'genuine excess',0)

    def convert(self,amount,*,kind,source_eligible,internal=False):
        integer(amount,'allocated excess points',0)
        if kind not in ('temp-hp','damage'):raise SpellRuleError('Unreviewed excess converter')
        if not internal and not self.internal_resolved:
            raise SpellRuleError('Resolve source-internal conversion before external conversion')
        if internal and self.internal_resolved:raise SpellRuleError('Internal conversion already resolved')
        if internal:self.internal_resolved=True
        if not source_eligible or (kind=='temp-hp' and self.forbid_temp_hp):return 0
        if amount>self.remaining:raise SpellRuleError('Excess points cannot be spent twice')
        self.remaining-=amount
        return amount


@dataclass
class HealingChain:
    root_id: str
    visited: set = field(default_factory=set)

    def child(self,application_id,*,kind,parent_flags=frozenset(),source_flags=frozenset()):
        """Shared ledger across branches; each source application at most1/root.

        Caller validates all actual-gain/ownership/cost/cadence eligibility.
        Returned flags accompany the child; numerical add-ons make no child.
        """
        blockers={'link':'blockLinkTriggers','healing':'blockSecondaryHealingTriggers',
                  'resource':'blockResourceTriggers','damage':'blockDamageTriggers',
                  'copy':'blockHealCopyTriggers','smite':'blockSmiteTriggers',
                  'redirection':'blockRedirectionTriggers'}
        if kind not in blockers:raise SpellRuleError('Unreviewed downstream trigger kind')
        blocked=blockers[kind] in parent_flags
        if kind in ('link','copy') and 'blockSecondaryHealingTriggers' in parent_flags:blocked=True
        if blocked or application_id in self.visited:return None
        self.visited.add(application_id)
        return {'healingRootId':self.root_id,'visitedHealingApplicationIds':frozenset(self.visited),
                'flags':frozenset(parent_flags)|frozenset(source_flags)}


TEMPORAL_PARTICIPANT_FIELDS=('position','life','conditions','revelationCharges',
                             'perEncounterUses','soulBind')


def restore_temporal_participant(current,snapshot):
    """Selected snapshot field contract only; NOT a usable Time Loop engine.

    life includes HP/temp/death counters/Wounds/linked Injuries. This does not
    solve environment/equipment/body-part duplication or clock rebasing. Those
    must be resolved in the dedicated temporal package before activation.
    """
    if any(key not in snapshot for key in TEMPORAL_PARTICIPANT_FIELDS):
        raise SpellRuleError('Incomplete participant snapshot')
    out=deepcopy(current)
    for key in TEMPORAL_PARTICIPANT_FIELDS:out[key]=deepcopy(snapshot[key])
    return out

```

## tools/validate_healing_playtests.py
```
"""Bounded life-state cases only; not full healing/card/spell validation."""
from pathlib import Path
from fractions import Fraction
import json
from healing_playtest_rules import *
from control_playtest_rules import ClockMarker,turn_end_deadline
from core_playtest_rules import damage_event
from strain_playtest_rules import StrainState,StrainPoint,expedition_gain,ordinary_recovery
ROOT=Path(__file__).resolve().parents[1]
def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    living=LifeState(30,27)
    out,info=ordinary_healing(living,8,reserve=10)
    check('Only actual3HP spends reserve',(out.hp,info['reserveSpent'],info['reserveRemaining']),(30,3,7))
    out,info=ordinary_healing(LifeState(30,5),8,reserve=3)
    check('Reserve caps actual restoration',(out.hp,info['reserveRemaining']),(8,0))
    out,info=ordinary_healing(living,8,reserve=10,hp_gain_prohibited=True)
    check('Blocked healing spends no reserve',(out.hp,info['reserveSpent'],info['reserveRemaining']),(27,0,10))
    critical=LifeState(30,29,wounds=(None,None,None))
    out,info=ordinary_healing(critical,10,reserve=10)
    check('Critical ceiling preserves reserve',(out.hp,info['reserveSpent']),(29,0))
    rejects('Healing dead is not resurrection',lambda:ordinary_healing(LifeState(30,0,dead=True),10))
    dying=LifeState(30,0,death_failures=2)
    check('Mage at0 still owes regular-start death save',zero_hp_permissions(dying,'mage.undying-spellform')['deathSaveDueAtRegularStart'],True)
    check('Mage feature grants no ordinary Reaction',zero_hp_permissions(dying,'mage.undying-spellform')['reaction'],False)
    stable=LifeState(30,0,stable=True,stable_until_seconds=3600)
    check('Stable Mage does not roll death saves',zero_hp_permissions(stable,'mage.undying-spellform')['deathSaveDueAtRegularStart'],False)
    out=finish_undying_spellform(stable)
    check('Mage expiry destabilizes and adds1',(out.stable,out.stable_until_seconds,out.death_failures),(False,None,1))
    check('Mage expiry third failure kills',finish_undying_spellform(dying).dead,True)
    check('Mage expiry never damages recovered creature',finish_undying_spellform(living),living)
    dead=LifeState(30,0,dead=True)
    check('Dead Mage has no acting exception',zero_hp_permissions(dead,'mage.undying-spellform'),{'exceptionApplies':False})
    check('Oracle selection retains exactly one printed option',zero_hp_permissions(dying,'oracle.false-life-iii',chosen_oracle_option='revelation')['chosenOption'],'revelation')
    rejects('Oracle cannot select an invented option',lambda:zero_hp_permissions(dying,'oracle.false-life-iii',chosen_oracle_option='all'))
    check('Stitch unravels one failure',stitch_fate(dying,'unravel-failure').death_failures,1)
    out=stitch_fate(dying,'stitch-life')
    check('Stitch Life clears counters and gives1',(out.hp,out.death_failures,out.stable),(1,0,False))
    out=stitch_fate(dying,'stitch-life',hp_gain_prohibited=True,stable_d4=2,now_seconds=10)
    check('Blocked Stitch establishes real Stable deadline',(out.hp,out.stable,out.death_failures,out.stable_until_seconds),(0,True,0,7210))
    rejects('Stitch cannot undo completed death',lambda:stitch_fate(dead,'stitch-life'))
    rejects('Stitch cannot target Stable creature',lambda:stitch_fate(stable,'stitch-life'))
    rejects('No failed save cannot be removed',lambda:stitch_fate(LifeState(30,0),'unravel-failure'))
    check('Divine Rebirth floors odd effective maximum',returned_hp(101,divine_rebirth=True),50)
    check('Divine Rebirth minimum1',returned_hp(1,divine_rebirth=True),1)
    corpse=LifeState(30,0,dead=True,wounds=(1,None,4),death_failures=3,last_death_turn=7)
    out=resurrection_transition(corpse,15,identity_willing=True,source_eligibility_met=True)
    check('Resurrection preserves all Wounds',out.wounds,(1,None,4))
    check('Resurrection gives printed HP and clears dying counters',(out.hp,out.dead,out.stable,out.death_failures),(15,False,False,0))
    check('Resurrection cannot replay a used death-save turn',out.last_death_turn,7)
    rejects('Resurrection blocker stops transition',lambda:resurrection_transition(corpse,1,identity_willing=True,source_eligibility_met=True,resurrection_blocked=True))
    rejects('Unwilling identity cannot be revived',lambda:resurrection_transition(corpse,1,identity_willing=False,source_eligibility_met=True))
    rejects('Source body/window/range prerequisite must hold',lambda:resurrection_transition(corpse,1,identity_willing=True,source_eligibility_met=False))
    rejects('Living0 target is not a corpse',lambda:resurrection_transition(dying,1,identity_willing=True,source_eligibility_met=True))
    check('One-minute death window includes exactly60seconds',death_within_elapsed_window(3,63,60),True)
    check('One-minute death window excludes61seconds',death_within_elapsed_window(3,64,60),False)
    check('Future death cannot be targeted',death_within_elapsed_window(64,63,60),False)
    check('Fractional death age is not rounded',death_within_elapsed_window(Fraction(1,2),Fraction(121,2),60),True)
    check('Death before prior end-phase is excluded',death_since_previous_end(ClockMarker(6,10),turn_end_deadline(6),12),False)
    check('Death strictly after prior end-phase is included',death_since_previous_end(ClockMarker(6,30),turn_end_deadline(6),12),True)
    rejects('Previous regular end cannot be an ambiguous integer',lambda:death_since_previous_end(7,6,12))
    rejects('Previous regular end cannot be a start phase',lambda:death_since_previous_end(7,ClockMarker(6),12))
    flat=HealingReduction('flat5','doomed','flat',5,next_healing=True)
    target=LifeState(40,10)
    result=healing_packet(target,5,reductions=[flat],conditional_flat_bonuses=(3,))
    check('Conditional bonus cannot bootstrap zero restoration',(result['actualHpGained'],result['conditionalAddonsQualify']),(0,False))
    check('Pre-resolution bonus can overcome flat reduction',healing_packet(target,5,reductions=[flat],pre_flat_bonuses=(3,))['actualHpGained'],3)
    result=healing_packet(target,6,reductions=[flat],pre_flat_bonuses=(2,),conditional_flat_bonuses=(3,))
    check('Two-pass uses strongest pre/conditional flat, not their sum',(result['previewActualHpGained'],result['actualHpGained']),(3,4))
    check('Preview does not consume next-healing twice',result['nextHealingCandidates'],['flat5'])
    check('Two compatible halves floor only once',healing_packet(target,7,systemic_factors=(Fraction(1,2),Fraction(1,2)))['actualHpGained'],1)
    half=HealingReduction('half','suppression','factor',Fraction(1,2))
    totem=HealingReduction('totem','blight-totem','blight-totem',Fraction(1,2))
    result=healing_packet(target,20,reductions=[totem,half,flat])
    check('Blight Totem does not compound other local reductions',(result['actualHpGained'],result['reductionBranch']),(5,'compatible-local'))
    result=healing_packet(target,20,reductions=[totem,HealingReduction('small','small','flat',2)])
    check('Stronger totem-alone branch wins',(result['actualHpGained'],result['reductionBranch']),(10,'blight-totem-alone'))
    check('Systemic half remains with totem branch',healing_packet(target,20,systemic_factors=(Fraction(1,2),),reductions=[totem])['actualHpGained'],5)
    per_die=HealingReduction('desecrated','desecrated','per-die',1)
    check('Per-die penalty precedes multiplier',healing_packet(target,10,dice_count=3,reductions=[per_die,half])['actualHpGained'],3)
    check('Flat Lay on Hands has no per-die penalty',healing_packet(target,10,dice_count=0,reductions=[per_die])['actualHpGained'],10)
    check('Shared/maximized roll still carries printed die count',healing_packet(target,16,dice_count=2,reductions=[per_die])['actualHpGained'],14)
    check('Per-die bonus preserves its explicit cap',healing_packet(target,10,dice_count=4,per_die_bonus=1,per_die_bonus_cap=3)['actualHpGained'],13)
    check('Duplicate local profile group uses strongest reduction',healing_packet(target,15,reductions=[flat,HealingReduction('flat3','doomed','flat',3)])['actualHpGained'],10)
    check('Distinct flat reductions compose',healing_packet(target,15,reductions=[flat,HealingReduction('flat3','dirge','flat',3)])['actualHpGained'],7)
    check('Same-stat per-die reductions do not add',healing_packet(target,10,dice_count=2,reductions=[per_die,HealingReduction('per2','other','per-die',2)])['actualHpGained'],6)
    result=healing_packet(LifeState(20,19,wounds=(None,None,None)),10)
    check('Critical blocked last HP is not itself convertible excess',(result['actualHpGained'],result['genuineExcess']),(0,9))
    check('Broad prohibition prevents excess conversion',healing_packet(LifeState(20,19),10,hp_gain_prohibited=True)['genuineExcess'],0)
    check('Full-HP legal heal has genuine excess',healing_packet(LifeState(20,20),10)['genuineExcess'],10)
    check('Blocked positive-potential next-heal is identified once',healing_packet(target,5,reductions=[flat],hp_gain_prohibited=True)['nextHealingCandidates'],['flat5'])
    check('Zero potential does not identify next-heal spend',healing_packet(target,0,reductions=[flat])['nextHealingCandidates'],[])
    check('Suppressed next-heal reducer does not qualify or spend',healing_packet(target,10,reductions=[replace(flat,suppressed=True)])['nextHealingCandidates'],[])
    rejects('Float factors are not silently rounded',lambda:healing_packet(target,10,systemic_factors=(0.5,)))
    rejects('Duplicate application cannot subtract twice',lambda:healing_packet(target,10,reductions=[flat,flat]))
    check('Declined Insight uses same d2 block',false_life_healing_blocked(other_creature_spell=True,d2=1),True)
    check('Failed/declined Insight d2=2 permits healing',false_life_healing_blocked(other_creature_spell=True,d2=2),False)
    check('Successful Insight needs no d2',false_life_healing_blocked(other_creature_spell=True,insight_success=True),False)
    check('Non-spell recovery ignores False Life spell gate',false_life_healing_blocked(other_creature_spell=False),False)
    donor=LifeState(20,10,temp_hp=50)
    paid,base=transfer_hp_cost(donor,5,transfusion=True)
    received=ordinary_healing(target,base,hp_gain_prohibited=True)[0]
    check('Transfusion donor pays despite recipient prohibition',(paid.hp,paid.temp_hp,base,received.hp),(5,50,7,10))
    rejects('Temporary HP cannot fund donor normal-HP cost',lambda:transfer_hp_cost(donor,10))
    pending=apply_soul_bind(dying,'victim',10,failed_save=True)
    check('Soul Bind pending uses60seconds',pending.expires,Fraction(70))
    refreshed=apply_soul_bind(dying,'victim',30,failed_save=True,existing=pending)
    check('Second Soul Bind refreshes one pending identity',refreshed,SoulBind('victim','pending',90))
    check('Successful target save leaves existing pending intact',apply_soul_bind(dying,'victim',30,failed_save=False,existing=pending),pending)
    check('Stabilization ends pending Soul Bind',resolve_soul_bind(pending,stable,20),None)
    check('Positive HP ends pending Soul Bind',resolve_soul_bind(pending,living,20),None)
    bound=resolve_soul_bind(pending,dead,69)
    check('Soul Bind death conversion starts new24hours',bound,SoulBind('victim','bound',86469))
    check('Death at exact pending expiry cannot convert',resolve_soul_bind(pending,dead,70),None)
    check('Death after pending expiry cannot convert',resolve_soul_bind(pending,dead,71),None)
    check('Bound state ends at exact24hour boundary',resolve_soul_bind(bound,dead,86469),None)
    rejects('Dead target cannot be rebound by this spell',lambda:apply_soul_bind(dead,'victim',100,failed_save=True))
    rejects('Soul record cannot transfer identities',lambda:apply_soul_bind(dying,'other',30,failed_save=True,existing=pending))
    out,event=survival_damage_event(LifeState(40,10,temp_hp=10),5)
    check('Temporary HP absorbs real damage for numeric drains',(out.hp,event['tempAbsorbed'],event['postTempDamage'],event['actualHpDamage'],event['actualDamageDealt'],event['positiveDamageEvent']),(10,5,0,0,5,True))
    out,event=survival_damage_event(LifeState(40,1),5,floor=True)
    check('Floor preserves1 but still counts positive damage packet',(out.hp,event['actualHpDamage'],event['actualDamageDealt'],event['positiveDamageEvent']),(1,0,0,True))
    check('Floor prevents drop-only Wound trigger',event['woundSaves'],0)
    out,event=survival_damage_event(LifeState(40,3),12,wound_natural=20)
    check('Overkill cannot inflate numeric drain',(out.hp,event['postTempDamage'],event['actualHpDamage'],event['actualDamageDealt']),(0,12,3,3))
    out,event=survival_damage_event(LifeState(40,0),1)
    check('ZeroHP damage has consequences despite zero numeric drain',(out.death_failures,event['actualDamageDealt'],event['positiveDamageEvent']),(1,0,True))
    out,event=survival_damage_event(LifeState(30,8),38,floor=True)
    check('Instant Death equality defeats ordinary floor',(out.dead,event['floorUsed'],event['woundSaves']),(True,False,0))
    out,event=survival_damage_event(LifeState(40,20),25,floor=True,wound_natural=20)
    check('Floor preserves raw half-max Wound threshold',(out.hp,event['postTempDamage'],event['woundSaves']),(1,25,1))
    out,event=survival_damage_event(LifeState(40,5),8,floor=True,hp_gain_prohibited=True)
    check('Decay cannot block loss prevention',out.hp,1)
    out,event=survival_damage_event(LifeState(40,5),100,ritual_ward=True,hp_gain_prohibited=True)
    check('Ward prevents Instant Death at positiveHP through Decay',(out.hp,out.dead,event['wardUsed']),(1,False,True))
    check('Intercepted Instant Death never replays Wound/failure branch',(event['woundSaves'],event['deathFailuresAdded']),(0,0))
    check('Ward preserves1 without reducing raw100damage',(event['postTempDamage'],event['actualHpDamage'],event['actualDamageDealt']),(100,4,4))
    out,event=survival_damage_event(LifeState(40,20,wounds=(None,None,None)),10,maiming=True,wound_natural=1,ritual_ward=True)
    check('Ward cannot inflate damage with a lower state assignment',(out.hp,event['actualHpDamage'],event['actualDamageDealt']),(1,10,10))
    out,event=survival_damage_event(LifeState(40,0,death_failures=2),1,ritual_ward=True,hp_gain_prohibited=True,stable_d4=2,now_seconds=10)
    check('ZeroHP Ward under Decay establishes Stable deadline',(out.hp,out.stable,out.death_failures,out.stable_until_seconds),(0,True,0,7210))
    check('ZeroHP replacement creates no negative damage',event['actualHpDamage'],0)
    out,event=survival_damage_event(LifeState(40,5),100,ritual_ward=True,replacement_legal=False)
    check('Ineligible body/death exception cannot be bypassed',(out.dead,event['wardUsed']),(True,False))
    out,event=survival_damage_event(LifeState(40,5),8,spiral_iii=True,wound_natural=20)
    check('SpiralIII recovers before its preserved drop Wound save',(out.hp,event['spiralUsed'],event['phaseOut'],event['woundSaves']),(10,True,True,1))
    check('Spiral recovery never erases triggering damage metrics',event['actualHpDamage'],5)
    out,event=survival_damage_event(LifeState(40,5),8,spiral_iii=True,hp_gain_prohibited=True,wound_natural=20)
    check('Decay blocks Spiral HP but not spent use/phase',(out.hp,event['spiralUsed'],event['phaseOut'],event['postZeroWindow']),(0,True,True,True))
    out,event=survival_damage_event(LifeState(40,5,wounds=(None,None,None)),8,spiral_iii=True,wound_natural=1)
    check('Fatal Wound after Spiral kills and ends phase',(out.dead,event['spiralUsed'],event['phaseOut']),(True,True,False))
    out,event=survival_damage_event(LifeState(40,5,wounds=(None,None,None)),8,spiral_iii=True,wound_natural=1,ritual_ward=True)
    check('Independent Ward can prevent actual death after Spiral',(out.dead,out.hp,event['spiralUsed'],event['phaseOut']),(False,1,True,True))
    out,event=survival_damage_event(LifeState(40,5),8,spiral_iii=True,floor=True)
    check('True floor prevents Spiral trigger and use',(out.hp,event['floorUsed'],event['spiralUsed']),(1,True,False))
    out,event=survival_damage_event(LifeState(40,5),100,spiral_iii=True)
    check('Spiral cannot intercept Core Instant Death',(out.dead,event['spiralUsed']),(True,False))
    permissions=zero_hp_permissions(dying,'mage.undying-spellform')
    check('Mage can speak cast and preserve concentration against zero only',
          (permissions['speech'],permissions['action'],permissions['startConcentration'],
           permissions['preserveConcentrationAgainstZero'],permissions['damageConcentrationSaveStillRequired']),
          (True,True,True,True,True))
    permissions=zero_hp_permissions(dying,'oracle.false-life-iii',chosen_oracle_option='revelation')
    check('Oracle Revelation can establish new concentration but preserves no old concentration',
          (permissions['startConcentration'],permissions['preserveConcentrationAgainstZero']),(True,False))
    check('Oracle movement choice grants no concentration activation',zero_hp_permissions(dying,'oracle.false-life-iii',chosen_oracle_option='move')['startConcentration'],False)
    out,event=false_life_v_recovery(dying,due=True,regular=True)
    check('False LifeV regular-start quarter recovery clears dying before save',(out.hp,out.death_failures,event['deadlineConsumed']),(7,0,True))
    out,event=false_life_v_recovery(dying,due=True,regular=False)
    check('Extra start neither consumes nor resolves delayed recovery',(out,event['deadlineConsumed']),(dying,False))
    out,event=false_life_v_recovery(dying,due=True,regular=True,hp_gain_prohibited=True)
    check('Blocked delayed recovery remains dying without invented stability',(out.hp,out.stable,out.death_failures,event['deadlineConsumed']),(0,False,2,True))
    check('Delayed recovery cannot resurrect',false_life_v_recovery(dead,due=True,regular=True)[0].dead,True)
    out,event=death_save_with_survival(dying,1,regular_turn_id=1,failed_reroll=10)
    check('FateBound reroll replaces natural1 before fatal counters',(out.dead,out.death_failures,out.death_successes,event['resolvedNatural']),(False,2,1,10))
    out,event=death_save_with_survival(LifeState(30,0),8,regular_turn_id=1)
    check('Death-effect bonus is not silently added to ordinary death save',out.death_failures,1)
    rejects('Successful death save cannot use failed-save reroll',lambda:death_save_with_survival(dying,10,regular_turn_id=1,failed_reroll=20))
    out,event=death_save_with_survival(dying,1,regular_turn_id=1,ritual_ward=True,hp_gain_prohibited=True,stable_d4=3,now_seconds=5)
    check('Ward replaces third death-save failure with blocked Stable0',(out.dead,out.stable,out.death_failures,out.stable_until_seconds,event['wardUsed']),(False,True,0,10805,True))
    check('Replacement preserves used regular death-save marker',out.last_death_turn,1)
    rejects('Ward does not permit another save on same turn',lambda:death_save_with_survival(replace(out,stable=False,stable_until_seconds=None),10,regular_turn_id=1))
    out,event=death_save_with_survival(dying,20,regular_turn_id=1,hp_gain_prohibited=True)
    check('Blocked natural20 recovery does not manufacture stability',(out.hp,out.stable,out.death_failures),(0,False,2))
    out,event=would_die_transition(dying)
    check('Explicit direct death actually kills without damage',(out.dead,event), (True,{'wardUsed':False,'actualDeath':True}))
    out,event=would_die_transition(dying,ritual_ward=True)
    check('Direct death intercepted by Ward gives no actual-death healing trigger',(out.hp,event['actualDeath']),(1,False))
    rejects('Ward is not retrospective resurrection',lambda:would_die_transition(dead,ritual_ward=True))
    points=tuple(StrainPoint(str(i),'old-gain',removal_gate_met=i!=0) for i in range(6))
    ex,exp,permissions=reconcile_lethal_tracks(LifeState(30,1),ExhaustionState(6),StrainState(points=points))
    check('Return retains both lethal tracks and adds collapse',(ex.level,ex.lethal_collapse,exp.points,exp.collapsed,permissions['voluntaryAct']),(6,True,points,True,False))
    check('Root cause still active bars Exhaustion recovery',exhaustion_long_rest(ex,qualifying_rest=True,care_food_water=True,root_cause_inactive=False),ex)
    check('Recovery prohibition bars Exhaustion recovery',exhaustion_long_rest(ex,qualifying_rest=True,care_food_water=True,root_cause_inactive=True,recovery_blocked=True),ex)
    check('Unconscious patient can rest with real care',exhaustion_long_rest(ex,qualifying_rest=True,care_food_water=True,root_cause_inactive=True),ExhaustionState(5))
    check('Later positive Exhaustion gain6 opens new death',exhaustion_gain(ex,1),(ExhaustionState(6),True))
    check('Prevented gain preserves current collapse',exhaustion_gain(ex,1,prevented=True),(ex,False))
    out_exp,out_life,event=expedition_gain(exp,LifeState(30,1),1,event_id='later',source_id='hazard')
    check('Later Expedition gain6 kills again despite earlier return',(out_life.dead,event['added'],event['endpoint']),(True,0,'death'))
    check('Ordinary Long Rest cannot remove collapse points',ordinary_recovery(exp,'long'),(exp,[]))
    recovered,removed=ordinary_recovery(exp,'haven')
    check('Qualified24h Haven retains gated point',(len(removed),recovered.points,recovered.collapsed),(5,(points[0],),False))
    history=RevivalHistory()
    history.record_success('thousand-petals','monk-A','ally')
    history.record_success('grace-reversal','paladin-A','ally')
    history.record_success('grace-reversal','paladin-B','ally')
    check('Other Monk can revive same identity',history.eligible('thousand-petals','monk-B','ally'),True)
    history.owner_long_rest('monk-A')
    check('Monk Long Rest cannot reset campaign resurrection history',history.eligible('thousand-petals','monk-A','ally'),False)
    history.owner_long_rest('paladin-A')
    check('Only owner Paladin rest resets owner-target pair',(history.eligible('grace-reversal','paladin-A','ally'),history.eligible('grace-reversal','paladin-B','ally')),(True,False))
    check('Thousand Petals6 total includes2corpses',len(thousand_petals_targets(['a','b','c','d'],['e','f'])),6)
    rejects('Thousand Petals cannot target6living plus2corpses',lambda:thousand_petals_targets(list('abcdef'),['g','h']))
    rejects('Thousand Petals cannot target3corpses',lambda:thousand_petals_targets([],list('abc')))
    rejects('One creature cannot count in both target categories',lambda:thousand_petals_targets(['a'],['a']))
    ledger=IdentityReturnLedger(eligible_remains={'ally':{'body-A','body-B'}})
    out=ledger.true_resurrection('ally',dead,willing=True,within_window=True,identity_known=True,legal_formation_space=True)
    check('Bodyless return disables every duplicate remains anchor',(out.hp,ledger.eligible_remains['ally']),(1,set()))
    rejects('Second body cannot create living duplicate',lambda:ledger.true_resurrection('ally',dead,willing=True,within_window=True,identity_known=True,body_anchor='body-B'))
    rejects('Bodyless return still requires actual legal space',lambda:IdentityReturnLedger().true_resurrection('other',dead,willing=True,within_window=True,identity_known=True))
    rejects('Bodyless return still respects soul blocker',lambda:IdentityReturnLedger().true_resurrection('other',dead,willing=True,within_window=True,identity_known=True,legal_formation_space=True,resurrection_blocked=True))
    committed=HealingCommitLedger()
    packet=healing_packet(target,10,reductions=[flat,totem],hp_gain_prohibited=True)
    check('Preview did not spend reducer',committed.consumed_reducer_ids,set())
    check('One commit spends reducer despite blocked gain',committed.commit('root',packet),{'flat5'})
    rejects('Two-pass arithmetic cannot commit event twice',lambda:committed.commit('root',packet))
    excess=ExcessLedger(9)
    rejects('External converter cannot jump source-internal priority',lambda:excess.convert(3,kind='damage',source_eligible=True))
    check('Internal converter spends first excess points',excess.convert(5,kind='temp-hp',source_eligible=True,internal=True),5)
    check('External converter only gets remaining points',excess.convert(4,kind='damage',source_eligible=True),4)
    rejects('Excess cannot be double-converted',lambda:excess.convert(1,kind='damage',source_eligible=True))
    excess=ExcessLedger(9,forbid_temp_hp=True)
    check('Channel Life blocks source-internal tempHP conversion',excess.convert(9,kind='temp-hp',source_eligible=True,internal=True),0)
    check('Channel Life blocks external tempHP conversion',excess.convert(9,kind='temp-hp',source_eligible=True),0)
    check('Channel Life genuine excess can use eligible damage conversion',excess.convert(4,kind='damage',source_eligible=True),4)
    chain=HealingChain('paid-root')
    first=chain.child('shared-A',kind='link')
    second=chain.child('shared-B',kind='link',parent_flags=first['flags'])
    check('Cross-owner secondary heals retain root',(first['healingRootId'],second['healingRootId']),('paid-root','paid-root'))
    check('Returning through earlier link is blocked',chain.child('shared-A',kind='link'),None)
    vitality=chain.child('vitality',kind='link',source_flags={'blockLinkTriggers'})
    check('Vitality child cannot trigger any new link',chain.child('shared-C',kind='link',parent_flags=vitality['flags']),None)
    echo=chain.child('echo-leech',kind='healing',source_flags={'blockSecondaryHealingTriggers','blockResourceTriggers'})
    check('Echo child cannot trigger new healing',chain.child('new-heal',kind='healing',parent_flags=echo['flags']),None)
    check('Echo child cannot trigger resource recovery',chain.child('new-RC',kind='resource',parent_flags=echo['flags']),None)
    current={'position':'later','life':corpse,'conditions':['Bleed'],'revelationCharges':0,
             'perEncounterUses':{'dodge':True},'soulBind':bound,
             'RP':2,'Ki':0,'Conviction':0,'BG':0,'recoveryReserve':0,'dailyUses':{'time-loop':True},'consumables':[]}
    snapshot={'position':'old','life':LifeState(30,20,wounds=(4,)),
              'conditions':[],'revelationCharges':3,'perEncounterUses':{'dodge':False},'soulBind':None,
              'RP':100,'Ki':10,'dailyUses':{},'consumables':['potion']}
    restored=restore_temporal_participant(current,snapshot)
    check('Temporal participant contract restores life Wounds andRC',(restored['life'].dead,restored['life'].hp,restored['life'].wounds,restored['revelationCharges']),(False,20,(4,),3))
    check('Temporal restoration preserves expended ordinary resources',(restored['RP'],restored['Ki'],restored['dailyUses'],restored['consumables'],restored['recoveryReserve']),(2,0,{'time-loop':True},[],0))
    check('Post-snapshot Soul Bind removed',restored['soulBind'],None)
    snapshot['soulBind']=pending;snapshot['life']=dead
    restored=restore_temporal_participant(current,snapshot)
    check('Pre-snapshot dead participant and bind retained',(restored['life'].dead,restored['soulBind']),(True,pending))
    core_parity_states=0
    for hp in (0,1,5):
      for temp in (0,3):
       for amount in (0,1,4,8,13):
        for wounds in ((),(None,None,None)):
         for critical_hit in (False,True):
          before=LifeState(10,hp,temp_hp=temp,wounds=wounds)
          options=dict(wound_natural=10,injury_d6=1,critical=critical_hit,stable_d4=2)
          expected,old_events=damage_event(before,amount,**options)
          actual,new_events=survival_damage_event(before,amount,**options)
          assert actual==expected,(before,amount,actual,expected)
          assert all(new_events[k]==v for k,v in old_events.items())
          core_parity_states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW; exact implementation not yet submitted',
            'scope':'Selected two-pass healing, damage/survival, delayed recovery/rerolls, lethal-track collapse, revival history/identity, Soul Bind, excess/provenance and participant snapshot field contract. No complete source engine, temporal world restoration, numerical balance or spell promotion.',
            'checkCount':len(checks),'coreParityStates':core_parity_states,'checks':checks}
    (ROOT/'docs/mechanics/HEALING_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} selected healing/death checks and {core_parity_states} unchanged Core damage states; implementation review pending.')
if __name__=='__main__':main()

```

## data/playtest/spell_drafts/candidate_healing_death.json
```
{
  "status": "IN_REVIEW_NOT_OPERATIONAL",
  "scope": "Individual healing/death spell candidates. This filename is intentionally outside batch_*.json and is not loaded into the operational catalog. Source class access, ranks and RP costs remain in the preserved catalog.",
  "requiredSpellIds": [
    "stitch-fate",
    "death-ward",
    "resurrection",
    "mass-resurrection-denial",
    "true-resurrection",
    "soul-bind"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md",
    "docs/audit/2026-10-08/full-game/GPT_HEALING_SUPPLEMENT_REVIEW.md",
    "docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_BOUNDARIES.md"
  ],
  "spells": [
    {
      "id": "stitch-fate",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "One living dying creature at 0 HP you can perceive within range and line of effect. Dead and Stable creatures are ineligible.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Choose one mode before paying. Unravel Failure requires at least one recorded failed death save and removes one failure. Stitch Life clears death-save counters and restores 1 HP as direct state recovery.",
      "effect": "Unravel Failure leaves the creature dying at 0 HP with its other recorded successes/failures intact. Stitch Life restores a living dying creature to 1 HP, ending its zero-HP dying state. If a broad cannot-regain-HP effect blocks that 1 HP, instead clear its death counters, make it Stable at 0, and roll its ordinary d4-hour recovery deadline from now. A still-active HP prohibition can defer that eventual recovery; damage or death cancels it normally.",
      "scaling": "None. The spell changes only one recorded failure or the defined 1-HP state recovery.",
      "limitations": "An Action cannot interrupt or retroactively change a completed death. This is not resurrection or ordinary HP healing; ordinary healing bonuses/halves do not alter the 1-HP state value. It removes no Wounds, Corruption, class Curse, conditions, debt or spent-resource consequences. Normal class access, RP, Dissonance, Refrain, components and countering rules apply. No refund after a legally paid cast is countered or fails at resolution.",
      "designNotes": "Core Divination rank8, 21RP, Action, 120ft, V/S/F and Instantaneous are preserved. Source says change one failed death save or auto-revive a dying target. NEW: two explicit modes; recorded-failure removal instead of a retroactive reroll; living-dying eligibility; 1-HP state recovery and blocked-recovery Stable bridge. This draft remains inactive pending exact review."
    },
    {
      "id": "death-ward",
      "activation": "Action",
      "rangeFeet": 60,
      "targets": "One living creature you can perceive within range and line of effect",
      "duration": "Concentration, up to 1 minute; ends when its prevention is used",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "No initial save. While the spell remains active, the first eligible effect that would reduce the target from positive HP to 0 without Core Instant Death or another outright-death result instead leaves it at 1 HP; then the ward ends.",
      "effect": "Prevent one positive-to-zero HP crossing. Preserve the raw damage packet, Core Instant Death check, half-maximum/Maiming Wound triggers and attached conditions. The prevented positive-to-zero crossing does not itself create a drop-only Wound save. This is loss prevention, not healing, so a cannot-regain-HP effect does not stop it. Other eligible survival effects are rechecked after the selected prevention resolves; no duplicate automatic use is consumed after the crossing has already been prevented.",
      "scaling": "None. Always one eligible crossing and a 1-HP floor.",
      "limitations": "Does not trigger while the target is already at 0. Does not resurrect, repair a vital body, prevent third death-save failure/fatal Wound death/lethal-track death or override explicitly unpreventable HP loss. Cannot legalize an otherwise unaffordable HP cost. If multiple independently owned wards exist, use only the chosen eligible prevention; unused records retain their own concentration/deadline. This is distinct from Cleric Ritual of Undeath's would-die replacement. Normal spell costs and risk apply.",
      "designNotes": "Core Necromancy rank4, 7RP, Action, 60ft and concentration1minute retained with exact class gates. M/F uses the already-reviewed class-focus alternative; no unstated material cost. NEW: living target, explicit positive crossing, outright-death exclusion and competing-prevention procedure. The agreed damage/HP-loss interface is in the candidate guide; inactive pending exact review."
    },
    {
      "id": "resurrection",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "One willing dead creature whose sufficiently intact remains are within range and line of effect, and whose death occurred no more than 8 elapsed hours ago",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "No attack or save. Check the dead identity's willingness, sufficient body, exact elapsed death window, location and actual resurrection/soul blockers. On a legal successful resolution, return that identity to life at 1 HP.",
      "effect": "Change Dead to Living, assign 1 returned HP, clear death-save counters and any previous Stable recovery deadline. Preserve Wounds, Corruption, Oracle Curse, other persistent death consequences and spent resources. This returned HP is a resurrection state transition, not ordinary healing; ordinary healing reductions and generic living HP-gain prohibitions do not change it. Explicit resurrection or soul blockers prevent return.",
      "scaling": "None. One identity returns at 1 HP; no additional targets or restored resources.",
      "limitations": "Does not create a missing viable body, duplicate a creature, compel an unwilling return, bypass a real planar/soul barrier, clear lethal tracks or repair otherwise lethal persistent afflictions. After successful return, retain Exhaustion6/Expedition6 and enter their protected living-collapse states. Later positive unprevented gain is lethal again; qualifying care and point gates still apply. This candidate remains inactive pending exact review. Known illegal prerequisites prevent activation; a legal cast already paid receives no refund for a later refusal, counter or changed eligibility. Normal RP, Dissonance, Refrain and component rules apply.",
      "designNotes": "Core Necromancy rank7, 17RP, Action, 120ft, V/S/F and Instantaneous retained. Class gates remain Cleric/Druid/Wizard13 and Shaman19. NEW provisional design: one target, willingness/body/line requirements, eight-hour elapsed window and1 returned HP. No imported diamond cost or hour-long cast. Inactive pending exact source, life-state and lethal-track review."
    },
    {
      "id": "mass-resurrection-denial",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "A fixed 20-foot-radius sphere centered on a point you can perceive within range and line of effect",
      "duration": "Concentration, up to 1 minute",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "No initial attack or save. Establish the zone; only remains physically inside its area are affected while the spell remains active.",
      "effect": "A corpse/remains inside the zone cannot serve as the target or anchor of an effect returning that creature to life. Moving the remains outside removes this spell's block; bringing remains inside while the zone exists subjects them to the block again. Ending concentration or a legal effect capable of dispelling this rank8 spell ends the zone. This spell does not itself damage creatures, animate corpses, bind souls or reverse a resurrection already completed.",
      "scaling": "None. The radius, duration and effect do not scale.",
      "limitations": "Bodyless True Resurrection that uses a legal formation space rather than the blocked remains is not stopped by this corpse-local prohibition alone. No generic dispel or free Counterspell is granted: a remover must already have an operational source that can affect this spell/rank. Normal concentration, costs, Dissonance and Refrain apply. Does not become a permanent resurrection ban after expiry.",
      "designNotes": "Core Necromancy rank8, 21RP, Action, 120ft and M/F focus alternative retained; exact class gates stay Cleric/Druid/Wizard15. NEW: 20ft fixed spherical area; concentration up to1minute replaces contradictory Instantaneous metadata because the source describes an ongoing corpse block. Scope and counterplay are explicit provisional decisions. Inactive until individual review."
    },
    {
      "id": "true-resurrection",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "One unambiguously identified willing dead creature that died no more than7 elapsed days ago; choose usable remains within range and line of effect or one legal unoccupied body-formation space you can perceive within range",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "No attack or save. The chosen identity must actually be dead and willing to return, satisfy the death window, and have no applicable identity/soul blocker. Usable remains may be the anchor; otherwise form a viable body in the chosen space. A true name or knowledge of an inferred afterlife-plane location is not required.",
      "effect": "Return the one identity to life at1HP, clearing death-save counters and any former Stable recovery deadline. Preserve Wounds, linked persistent consequences, Corruption, Oracle Curse, debts and spent resources. The returned HP is a resurrection state transition, not ordinary healing. Any other remains of this identity lose eligibility to create a second living instance; they remain mundane remains/history evidence as appropriate. No equipment, resources or second creature are created from duplicate remains.",
      "scaling": "None. One creature at1HP, with no restored class resources.",
      "limitations": "An already-living identity is ineligible. A bodyless mode does not bypass an actual soul/identity resurrection block or a source expressly preventing return through a planar barrier. A corpse-local denial alone does not bind the identity. Lethal tracks and persistent afflictions remain; apply their reviewed reconciliation rather than silently removing them. Refusal or a counter after a legal paid activation refunds nothing. Normal spell risk and component rules apply.",
      "designNotes": "Core Necromancy rank9, 26RP, Action, 120ft, V/S/F and explicit bodyless return retained with Cleric/Druid/Wizard17 access. NEW provisional7-day window, returned1HP, formation-space/identity eligibility and anti-duplication consequence. Soul cosmology remains a separate dependency; no true-name requirement, diamond cost or hour-long cast imported. Inactive pending individual review."
    },
    {
      "id": "soul-bind",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "One living dying creature at0HP you can perceive within range and line of effect; a Dead or Stable creature is ineligible",
      "duration": "Pending tether up to1 minute; if target dies while pending, bound identity for24 elapsed hours from that death",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Target makes a Charisma save against your spell save DC. On success no effect. On failure create a pending Soul Bind tether with an absolute expiry60 seconds after resolution. Target death before that expiry converts it into one soul-bound identity record with expiry24 hours after the death.",
      "effect": "Before death, gaining positiveHP or becoming Stable ends the pending tether. After conversion, that identity cannot return by resurrection until the24-hour record ends or a legally capable source removes it. Neither state requires concentration or ends merely because a caster dies/incapacitates. If death begins at or after the pending absolute expiry, conversion does not occur. Only one Soul Bind family record may exist per identity; another failed-save application while still living/dying refreshes to the later pending endpoint without stacked prisons. No post-death recast is legal because the spell targets a living dying creature.",
      "scaling": "None. No increased targets, indefinite duration or automatic save failure.",
      "limitations": "Pending dispel/removal targets the creature. After death, existing remains serve as the local magical anchor for an otherwise eligible dispel/removal; if no remains exist, a source must expressly free the bound identity/soul rather than inventing a physical anchor. A generic cure or under-ranked dispel is not sufficient. The spell grants no commands, ownership, memories, personality change or control over the player. Soul-specific temporal restoration uses its own reviewed interface. Normal costs, Dissonance, Refrain and countering apply.",
      "designNotes": "Core Necromancy rank9, 26RP, Action, 120ft, V/S/F and dying-target/resurrection-block purpose retained with Cleric/Druid/Wizard17 access. NEW: Charisma save,1-minute pending/24-hour bound states, no concentration, exact expiry collision, source-family refresh and local removal anchor. These replace the otherwise nonoperational Instantaneous summary with explicit finite aftermath. Wider soul cosmology remains open; inactive until individual review."
    }
  ],
  "pendingIndividualDrafts": []
}

```

## Control damage consumers
```python
@dataclass
class WrathfulBrand:
    owner: str
    target: str
    expires: ClockMarker
    owner_rider_available: bool = True
    ally_rider_available: bool = True
    active: bool = True

    def __post_init__(self):
        require_deadline(self.expires)

    def trigger(self, *, actor, ally_of_owner, now, resolved_damage,
                direct_attack_hit=False, base_dice_total=0, suppressed=False):
        integer(resolved_damage,'resolved damage before temporary HP',0)
        integer(base_dice_total,'unmodified rolled base dice',0)
        result={'fireBonus':0,'healD6':False,'wisdomSave':False}
        if not self.active or suppressed or clock_marker(now)>=self.expires or resolved_damage==0:
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

    def trigger(self, *, qualifying, attack_roll=False, hit=False, resolved_damage=0):
        integer(resolved_damage,'resolved damage before temporary HP',0)
        if self.trigger_kind not in ('attack','hit','damage'):
            raise SpellRuleError('Unregistered consumption trigger')
        met={'attack':attack_roll,'hit':hit,'damage':resolved_damage>0}[self.trigger_kind]
        if not self.available or not qualifying or not met:
            return False
        self.available=False
        return True


@dataclass
class PerTurnReflection:
    cleric_level: int
    used_turn_ids: set = field(default_factory=set)

    def reflect(self, *, target_turn_id, positive_damage_event, actual_damage_dealt, on_target_turn):
        """Caller supplies distinct actual turns, target-declared damage-event order."""
        integer(actual_damage_dealt,'temp absorption plus actual HP damage',0)
        if not isinstance(positive_damage_event,bool) or (actual_damage_dealt>0 and not positive_damage_event):
            raise SpellRuleError('Numeric damage requires a positive damage event')
        integer(self.cleric_level,'Cleric level',1,20)
        if not on_target_turn or not positive_damage_event or target_turn_id in self.used_turn_ids:
            return 0
        self.used_turn_ids.add(target_turn_id)
        return min(self.cleric_level,max(1,actual_damage_dealt//2))



```

## Custom condition helper (cure correction among previously reviewed logic)
```python
"""Selected reviewed custom-rider interfaces, not a full effect engine."""
from dataclasses import replace
from core_playtest_rules import death_save, stable_recovery, stabilize, heal
from spell_playtest_rules import integer, SpellRuleError


def present_record(record):
    """The existing active field means unexpired/not-ended, even when suppressed.

    Suppression and acquired condition immunity disable effects, not record
    presence. Initial immunity that prevented application creates no record.
    """
    return record.get('active', False)


def active_record(record):
    return present_record(record) and not record.get('suppressed', False) and not record.get('immune', False)


def qualifies_hook(hook, record, actor):
    if not active_record(record):
        return False
    tags = set(record.get('tags', []))
    owned = record.get('ownerCharacterId') == actor
    ident = record['mechanicalId']
    if hook == 'cleric.judging-light':
        return bool(tags & {'eligibility.weakened', 'classification.curse'})
    if hook == 'thief.sneak-condition':
        return owned and ('family.bleeding' in tags or ident in ('core.poisoned', 'thief.crippled'))
    if hook == 'thief.vile-tactics':
        return 'family.bleeding' in tags or ident in ('core.poisoned', 'thief.crippled')
    if hook == 'crimson.bleed-engine':
        return owned and record.get('sourceEngine') == 'crimson-agent.bleed' and 'family.bleeding' in tags
    if hook == 'warrior.terror-engine':
        return owned and record.get('sourceClass') == 'Warrior' and ident in ('warrior.shaken', 'warrior.disoriented.active', 'core.frightened')
    if hook == 'druid.snow-leopard':
        return 'eligibility.slowed-foe' in tags
    if hook == 'paladin.vengeance':
        return owned and 'eligibility.paladin-vengeance-marked' in tags
    raise SpellRuleError('Unknown reviewed hook')


def periodic_marker_arbitration(groups, *, family):
    """Choose ONE due stack group in one family at one target timing marker.

    Caller has already applied each group's printed cap and determined its due
    records. Expected damage is doubled to keep arithmetic exact. All due groups
    consume their scheduled ticks; losing groups never bank postponed damage.
    Nonperiodic detonations, procs and later markers are outside this helper.
    """
    if family not in ('family.bleeding', 'family.ongoing-fire'):
        raise SpellRuleError('Only explicitly registered periodic families arbitrate')
    if any(group.get('family', family) != family for group in groups):
        raise SpellRuleError('Do not arbitrate different families together')
    if not groups:
        return {'damagingGroup': None, 'consumedTickGroups': []}
    ids, candidates = set(), []
    for group in groups:
        ident = group['stackGroupId']
        if ident in ids:
            raise SpellRuleError('Each stack group must be aggregated once')
        ids.add(ident)
        expected = integer(group['expectedDamageTwice'], 'twice expected group damage', 0)
        first = integer(group['firstApplicationSequence'], 'stable first-application sequence', 0)
        candidates.append((expected, -first, ident))
    # Sequence should normally be unique. ID is a deterministic final tie breaker.
    chosen = sorted(candidates, key=lambda x: (-x[0], -x[1], x[2]))[0][2]
    return {'damagingGroup': chosen, 'consumedTickGroups': [g['stackGroupId'] for g in groups]}


def bleed_marker_arbitration(groups):
    """Compatibility entry point for the reviewed Bleed interface."""
    return periodic_marker_arbitration(groups, family='family.bleeding')


def periodic_binding_for_component(*, specific_profile=None,
                                   explicit_core_condition=None,
                                   condition_immune=False):
    """One textual effect component creates at most one periodic identity.

    Call separately only when operative source text creates separate effects.
    Display-name matching or a family tag never independently creates a record.
    """
    if explicit_core_condition not in (None, 'core.bleeding', 'core.burning'):
        raise SpellRuleError('Unsupported explicit Core periodic fallback')
    if condition_immune:
        return None
    return specific_profile or explicit_core_condition


def arbitrate_periodic_applications(records, *, family, marker):
    """Resolve eligible due records for ONE target and marker, without dice.

    All active due clocks consume a tick, including suppressed records. Active
    means an existing, not-expired record here; suppressed/immune is separate.
    Caller has already enforced application/refresh caps, source costs and time.
    Damage-type defenses are intentionally not used until damage resolution.
    """
    if family not in ('family.bleeding', 'family.ongoing-fire'):
        raise SpellRuleError('Unsupported periodic family')
    due=[r for r in records if r.get('active',False)
         and family in r.get('tags',[]) and r.get('dueMarker')==marker]
    if len({r['targetId'] for r in due})>1:
        raise SpellRuleError('Arbitrate one target at a time')
    ids=[r['applicationId'] for r in due]
    if len(ids)!=len(set(ids)):
        raise SpellRuleError('Duplicate application cannot create duplicate ticks')
    groups={}
    for r in due:
        if not active_record(r):
            continue
        integer(r['expectedDamageTwice'],'twice expected damage',0)
        integer(r['applicationSequence'],'application sequence',0)
        groups.setdefault(r['stackGroupId'],[]).append(r)
    candidates=[]
    permitted={}
    for group, members in groups.items():
        policies={r['withinGroupPolicy'] for r in members}
        caps={integer(r['instanceCap'],'instance cap',1) for r in members}
        if len(policies)!=1 or len(caps)!=1:
            raise SpellRuleError('One group requires one reviewed policy and cap')
        policy=next(iter(policies))
        if policy=='strongest':
            chosen=[min(members,key=lambda r:(-r['expectedDamageTwice'],r['applicationSequence'],r['applicationId']))]
        elif policy=='sum-permitted':
            if len(members)>next(iter(caps)):
                raise SpellRuleError('Apply source instance cap before arbitration')
            chosen=members
        else:
            raise SpellRuleError('Unknown source-group damage policy')
        permitted[group]=[r['applicationId'] for r in chosen]
        candidates.append({'stackGroupId':group,'family':family,
            'expectedDamageTwice':sum(r['expectedDamageTwice'] for r in chosen),
            'firstApplicationSequence':min(r['applicationSequence'] for r in members)})
    winner=periodic_marker_arbitration(candidates,family=family)['damagingGroup']
    return {'damagingGroup':winner,'damageApplications':permitted.get(winner,[]),
            'consumedTickApplications':ids}


def recipe_occupies_slot(components):
    """Suppressed ongoing components still occupy; resolved one-time riders do not."""
    return any(c.get('active',False) and c.get('ongoing',False) for c in components)


def healing_triggered_bleed_cure(record, *, legal_effect, magical,
                                 potential, actual_hp_gained=0,
                                 remover_requires_actual_hp=False):
    """Return the applicable cure procedure, without rolling or mutating records.

    Potential is the positive rolled/calculated amount before HP caps, reductions
    or prohibitions. A caller must validate targets, pay costs and resolve the
    healing effect; this helper never makes an illegal heal legal.
    """
    integer(potential, 'pre-cap healing potential', 0)
    integer(actual_hp_gained, 'actual HP gained', 0)
    if (not present_record(record) or not legal_effect or not magical or potential == 0
            or 'family.bleeding' not in record.get('tags', [])
            or (remover_requires_actual_hp and actual_hp_gained == 0)):
        return 'none'
    # The registry, not a guessed display name, must provide the endpoint.
    endpoint = record.get('magicalHealingEndpoint', 'none')
    if endpoint not in ('end', 'saveToEnd', 'none'):
        raise SpellRuleError('Unknown healing cure endpoint')
    return endpoint


def refresh_bleed_duration(remaining, base_duration, *, requested=2,
                           prolonged=False, owned=True, qualifying_trigger=True,
                           explicit_hard_cap=None):
    """Refresh an EXISTING finite Bleed; base duration is never itself a cap."""
    integer(remaining, 'existing remaining ticks', 1)
    integer(base_duration, 'printed base duration', 1)
    integer(requested, 'requested legal refresh duration', 1)
    if explicit_hard_cap is not None:
        integer(explicit_hard_cap, 'express source hard cap', 1)
        if remaining > explicit_hard_cap:
            raise SpellRuleError('Existing duration already exceeds its stated hard cap')
    if not owned or not qualifying_trigger:
        return remaining
    replacement = max(requested, 4 if prolonged and base_duration == 2 else 0)
    refreshed = max(remaining, replacement)
    return min(refreshed, explicit_hard_cap) if explicit_hard_cap is not None else refreshed


def extinguishable_records(records):
    """IDs ended by one legal Action/full immersion; caller validates that action."""
    return [r['applicationId'] for r in records if present_record(r)
            and 'family.ongoing-fire' in r.get('tags', [])
            and r.get('ordinaryExtinguishable', False)
            and not r.get('mundaneExtinguishingProhibited', False)
            and not r.get('specialExtinguishingPrerequisiteUnmet', False)]


def fire_ending_save_eligible(record, *, regular_turn_end):
    """Called after due damage/tick consumption; None ticks means indefinite."""
    if not regular_turn_end or not present_record(record) or 'family.ongoing-fire' not in record.get('tags', []):
        return False
    remaining = record.get('remainingTicks')
    if remaining is not None:
        integer(remaining, 'remaining scheduled ticks', 0)
    return record.get('genericDexEndingSave', False) and (remaining is None or remaining > 0)


def brutality_pre_damage(hp, maximum_hp, *, perceived, hostile, distance, operative=True):
    integer(maximum_hp, 'maximum HP', 1)
    integer(hp, 'pre-damage current HP', 0, maximum_hp)
    integer(distance, 'distance', 0)
    return operative and perceived and hostile and distance <= 60 and 4*hp <= maximum_hp


def consume_retribution(record):
    if record['mechanicalId'] != 'paladin.vengeance-mark.retribution' or not active_record(record):
        raise SpellRuleError('An active Retribution mark is required')
    if record.get('nextSmiteBonusSpent', False):
        raise SpellRuleError('Retribution die already spent')
    # Preserve expiry, opportunity benefit, eligibility and unrelated marks.
    return dict(record, nextSmiteBonusSpent=True)


def doomed_timestamp_expiry(expiry, now, *, finite_positive_buff, already_accelerated_this_turn=False):
    integer(expiry, 'buff expiry timestamp', 0)
    integer(now, 'current timestamp', 0)
    if not finite_positive_buff or already_accelerated_this_turn:
        return expiry
    return max(0, expiry-6)


def hp_recovery(state, amount, *, prohibited=False):
    integer(amount, 'HP restoration amount', 0)
    return heal(state, 0 if prohibited else amount)


def death_save_with_hp_prohibition(state, natural, *, prohibited=False, **kwargs):
    """Keep core legal-roll/turn validation; replace only blocked natural-20 gain.

    No intermediate result is published and no healing/condition hooks fire here.
    For a blocked natural20, kwargs must supply stable_d4 and now_seconds as for
    ordinary stabilization; the original state remains unchanged.
    """
    out = death_save(state, natural, **kwargs)
    if natural == 20 and prohibited:
        out = replace(out, hp=0)
        stabilize(out, kwargs.get('stable_d4'), kwargs.get('now_seconds', 0))
    return out


def stable_recovery_with_hp_prohibition(state, now_seconds, *, prohibited=False):
    integer(now_seconds, 'current timestamp', 0)
    if prohibited:
        # Preserve the original deadline even when already due. Core damage/death
        # handling cancels it if stability is lost; ending prohibition can retry it.
        return replace(state)
    return stable_recovery(state, now_seconds)

```

## All153 source-qualified roles/overrides (unchanged exact procedures in prior source packets)
[
  {
    "bindingId": "class-engine:cleric:7",
    "classification": "BOOK/guard: healing/resurrection limits",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.base.healing-rite",
    "classification": "HEAL ordinary",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.saint.divine-rebirth",
    "classification": "RESURRECTION MODIFIER",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.saint.unyielding-light",
    "classification": "LIVING-ZERO HP RECOVERY",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.saint.celestial-resurgence",
    "classification": "RESURRECTION",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.saint.mass-healing-light",
    "classification": "HEAL",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.saint.resurrection",
    "classification": "RESURRECTION",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.cultist.blasphemous-tongue",
    "classification": "HEALING REDUCTION / ALREADY Doomed",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.cultist.rite-of-the-crimson-choir",
    "classification": "COMPANION + LIFE-DRAIN HEALING, not resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.cultist.blood-sacrifice",
    "classification": "DIRECT HP LOSS WITH 1-HP COST FLOOR",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.cultist.ritual-of-undeath",
    "classification": "COMPANION REANIMATION + WOULD-DIE REPLACEMENT",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Would-die Ward can replace damage or non-damage death if body/explicit source eligibility permits. Positive pre-eventHP→1 is loss prevention through Decay; already0 blockedHP→Stable0 with immediate d4-hour deadline. Stop same-packet skipped death branches. Reconcile retained lethal tracks."
    ]
  },
  {
    "bindingId": "class-card:dragoon:dragoon.hero.dragon-guardian.bastion-descent",
    "classification": "TEMP HP / damage protection, not healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.archmage.harmonized-core",
    "classification": "TEMP HP, explicitly not healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.lich.undying-spellform",
    "classification": "CONSCIOUS-AT-ZERO STATE",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Partial zero override: speech, half movement, normal Action and concentration allowed; no independent BA/Reaction. Existing concentration avoids automatic zero loss but damage save remains. Separate restrictions apply. Expiry at0 destabilizes and adds1 failure."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.lich.soul-reservoir",
    "classification": "RESOURCE trigger, no healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.lich.resonance-to-flesh",
    "classification": "HEAL / DIRECT HP COST depending mode",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.lich.soulbound-ritual",
    "classification": "COMPANION RECONSTRUCTION",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:mirrorsage:5",
    "classification": "BOOK anti-copy/resource guard",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mirrorsage:mirrorsage.hero.light-weaver.radiant-archive",
    "classification": "SUPPORT COPY, explicitly no resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mirrorsage:mirrorsage.hero.light-weaver.divine-reflection",
    "classification": "COPY/BOOK hook, excludes resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:monk:16",
    "classification": "BOOK healing/death guard",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.base.crane-stance-support",
    "classification": "HEAL modifier + paid healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.breath-of-the-thousand-petals",
    "classification": "HEAL + RESURRECTION + DAMAGE FLOOR",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "At most6 total targets including at most2 eligible corpses. Each source Monk may resurrect each target identity once in the campaign. Living healing does not consume that history. Strict post-previous-end death marker; use/cost/floor clocks retained."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.healing-touch",
    "classification": "HEAL",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.circle-of-harmony",
    "classification": "PAID HEALING PULSES",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.shared-breath",
    "classification": "DAMAGE REDIRECT + HEALING ECHO",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Child healing shares root causal ledger. Every link application can fire once/root; no return path or sibling branch repeats an already visited link."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.way-of-shadow.veinlock-nerve-jab",
    "classification": "HP/FINITE-RESOURCE RECOVERY PROHIBITION",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:oracle:3",
    "classification": "BOOK: Oracle Curse persists through resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:oracle:13",
    "classification": "BOOK: healing/resurrection guard",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.shared.oracle-s-burden",
    "classification": "BOOK/protected class state",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.curse.wound-eater",
    "classification": "HEALING MULTIPLIER / rest condition",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.false-life.false-life-boon-i",
    "classification": "DAMAGE FLOOR + DEATH-SAVE DEATH REPLACEMENT",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Distinct positive-to-zero damage-floor and failed-death-save would-die replacement modes share the printed1/LR use. Do not promote this into an all-causes Ward."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.false-life.false-life-boon-ii",
    "classification": "FEIGN-DEATH STATE, not death/revival",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.false-life.false-life-boon-iii",
    "classification": "CONSCIOUS-AT-ZERO STATE",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Exactly one permitted turn choice: move, speak or Revelation using its printed activation/costs. Revelation can start concentration; prior concentration is not preserved by this feature."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.ancestor.echo-armor",
    "classification": "DAMAGE REDUCTION + 1-HP FLOOR",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.ancestor.echo-crowned",
    "classification": "ALLY 1-HP FLOOR / RC option",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.battle.battle-prophecy-trigger",
    "classification": "RESOURCE trigger at hostile 0 HP",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.battle.avatar-of-the-war-chorus",
    "classification": "ALLY 1-HP FLOOR / resource banners",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.bones.bones-prophecy-trigger",
    "classification": "RESOURCE trigger on actual death",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.bones.marrow-drain",
    "classification": "LIFE-DRAIN HEAL + HP-RECOVERY BLOCK",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.bones.rotting-touch",
    "classification": "ALREADY Decay / broad HP prohibition + corpse block",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.flame.undying-ember",
    "classification": "SELF 1-HP FLOOR + ordinary ally healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.bloom-ward",
    "classification": "HEAL modifier + damage absorb",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.overflowing-light",
    "classification": "HEAL + excess-to-temp-HP conversion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.thorned-shelter",
    "classification": "HEAL modifier",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.verdant-pulse",
    "classification": "post-heal rider + ally 1-HP floor",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.song-of-mending",
    "classification": "HEAL pulses + per-ally 1-HP floor",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.eternal-bloom",
    "classification": "pre-recorded HEAL reserve + per-ally 1-HP floor",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.base.protective-stance",
    "classification": "DAMAGE REDIRECTION, not healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.base.sacred-touch",
    "classification": "STABILIZATION, explicitly not healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-shared.last-reproach",
    "classification": "ordinary ally HEAL after damage",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.aura-of-mercy",
    "classification": "HEAL modifier",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.miracle-veil",
    "classification": "persistent 1-HP DAMAGE FLOOR",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.blessing-of-the-meek",
    "classification": "HEAL",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.grace-reversal",
    "classification": "RESURRECTION Reaction",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Only source-specific post-zero Reaction window after survival/Wounds, before zero Reaction loss finalizes. No self-target. Identity history is per source Paladin/target until that Paladin Long Rest; death does not reset it."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.grace-eternal",
    "classification": "Miracle floor + post-floor HEAL",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression",
    "classification": "HEALING ×1/2",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-vengeance.final-verdict",
    "classification": "broad cannot-regain-HP rider",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-flame.phoenix-rebirth",
    "classification": "LIVING-ZERO HP HEAL, not resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified",
    "classification": "PASSIVE-REGENERATION BLOCK",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura",
    "classification": "PASSIVE-REGENERATION BLOCK",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom",
    "classification": "DAMAGE + LIFE-DRAIN HEAL + source-local target floor",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-grief.echo-of-the-fallen",
    "classification": "SPIRIT MANIFESTATION, explicitly not resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-grief.dirge-of-passage",
    "classification": "HP-recovery prohibition on selected undead + death-save bonus",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura",
    "classification": "RESURRECTION BLOCK + flat HEALING reduction",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin",
    "classification": "broad cannot-regain-HP rider",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-the-martyr-king.last-king-s-gift",
    "classification": "1-HP FLOOR + TEMP HP",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura",
    "classification": "conditional HP-healing gate only",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:ranger:ranger.hero.outrider.blight-infusion",
    "classification": "next-healing flat reduction",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:ranger:ranger.hero.outrider.withering-shot",
    "classification": "next-healing ×1/2",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.hero.bloodcaller.blight-totem",
    "classification": "nonstacking HEALING ×1/2 aura",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:soldier:soldier.arch.fortify-zone",
    "classification": "NON-HEAL false-positive source",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:soldier:soldier.hero.champion.rallying-cry",
    "classification": "TEMP HP, not healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:tinker:tinker.base.field-repair",
    "classification": "MACHINE REPAIR, no destroyed-object resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:tinker:tinker.hero.artificer.repair-pulse",
    "classification": "MACHINE REPAIR, functional devices only",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.hero.wardborn.stabilizing-injection",
    "classification": "HEAL",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.hero.ironskin.regenerative-mutation",
    "classification": "PASSIVE REGENERATION / reserve-paid actual healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.redundant-organs",
    "classification": "1-HP DAMAGE FLOOR",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.hemophage-core",
    "classification": "LIFE-DRAIN HEAL / reserve-paid actual healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.base.consecrated-ground",
    "classification": "Restoration-conditioned flat healing add-on; same packet; once/creature/Rite pulse",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.base.radiance.radiance",
    "classification": "Restoration-conditioned flat add-on + cleanse; once owner turn",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.base.renewal.renewal",
    "classification": "Post-actual-HP non-healing Stamina recovery",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.base.echoes.echoes",
    "classification": "Delayed copied numeric heal/damage; no conditions/resources/triggers",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.arch.aura-of-faith",
    "classification": "Restoration-conditioned flat healing add-on",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.arch.sanctified-reprisal",
    "classification": "Post-actual-heal Smite empowerment; not additional healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.saint.aura-of-grace",
    "classification": "Finite paid healing pulse; not passive regeneration",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.priest.words-of-equilibrium",
    "classification": "Pre-resolution formula/M modifier",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.priest.cosmic-equilibrium",
    "classification": "Excess-heal→damage converter + radiant-damage→heal converter; separate once/round entitlements; no mutual recursion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.cultist.sanguine-rite",
    "classification": "Damage-driven finite healing based on actualDamageDealt",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:cleric:cleric.hero.cultist.zealot-s-fervor",
    "classification": "Pre-resolution flat healing-roll modifier; strongest-flat rules",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:crimson-agent:crimson-agent.base.blood-tithe",
    "classification": "Limited triggered healing after qualifying death; anti-farm",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:crimson-agent:crimson-agent.arch.hemostasis",
    "classification": "Bleed cure + ordinary finite healing; cure remains legal even when healing is later blocked",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:crimson-agent:crimson-agent.hero.bloodweaver.hemostasis",
    "classification": "Paid finite delayed healing pulses; explicit no healing-loop behavior",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:crimson-agent:crimson-agent.hero.bloodweaver.transfusion",
    "classification": "Non-damage donor HP cost + finite recipient healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Donor pays K normalHP before recipient baseK+floor(K/2) ordinary healing. No damage/redirection/temp payment/refund; donor remains1. Recipient legal modifiers/restrictions apply."
    ]
  },
  {
    "bindingId": "class-card:crimson-agent:crimson-agent.hero.bloodweaver.veinweave-vitality-link",
    "classification": "Separate triggered M-HP secondary heal; requires actual paid-Agent restoration; cannot retrigger link",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Separate child heal requires actual restoration by paid Agent source; child carries blockLinkTriggers for every downstream link, shared root/provenance retained."
    ]
  },
  {
    "bindingId": "class-engine:mirrorsage:2",
    "classification": "BOOK/profile engine: Mend is copied finite healing; Ward temp HP; no role conversion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:mirrorsage:mirrorsage.hero.shattered-one.echo-leech",
    "classification": "Paid damage-drain healing using actualDamageDealt; no secondary healing/resource procs",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.base.stance-shift",
    "classification": "Pre-heal Reaction state switch; can establish applicable stance before healing resolves",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.arch.meditative-healing",
    "classification": "Finite self-healing + independent post-resolution Ki restoration",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.tranquil-lotus-step",
    "classification": "Stored restoration-conditioned flat add-on to next heal",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.balance-beyond-flesh",
    "classification": "Paid finite triggered healing from qualifying resource expenditure",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:monk:monk.hero.enlightened-master.transcendent-meditation",
    "classification": "Finite paid healing pulses + independent second-pulse Ki restoration",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.spiral-touched.spiral-touched-boon-iii",
    "classification": "Zero-HP direct recovery + phase-out; not floor/resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Specific pre-Wound recovery after Instant Death fails and no true floor prevents crossing. Preserve original drop Wound trigger; spend use, attempt quarter-maximum direct recovery, phase out, then Wound. Fatal Wound ends phase unless independently replaced."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.spiral-touched.spiral-touched-boon-v",
    "classification": "DEFER temporal snapshot restoration, explicitly not generic resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "DEFER: snapshot participant contract is discussed/tested, including Wounds, RC, per-encounter use and Soul Bind restoration. Full clocks/environment/equipment/body duplication semantics require temporal package; no complete execution claim."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.wound-eater.wound-eater-boon-iii",
    "classification": "Direct death effect + heal only if target actually dies",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Direct pending death of a legal living dying hostile0 target emits no damage/Wound event. Legal Ward may intercept. Healing requires actual death; paid use/action remains spent."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.wound-eater.wound-eater-boon-iv",
    "classification": "Paid finite damage/drain pulses; self heal from actualDamageDealt",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.wound-eater.wound-eater-boon-v",
    "classification": "Direct non-damage HP loss + heal from actual HP lost",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.curse.burning-blood",
    "classification": "Cold-tagged HP-healing gate + actual-HP-damage ignition",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.curse.false-life",
    "classification": "Other-creature healing-spell gate with Insight/d2 procedure",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.false-life.false-life-boon-v",
    "classification": "Delayed start-turn direct HP recovery at 0; not resurrection",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Delayed quarter-maximum direct recovery at next regular start before death save. Extra turn does not advance it. Dead target is not revived; broad gain prohibition leaves0 without invented stability."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.fate-bound.fate-bound-boon-iv",
    "classification": "Death-effect save bonus + pre-commit failed-death-save reroll",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Reroll failed death save before committing natural1/failure counters, then use new result. Generic death-effect save bonus does not apply to ordinary death saves."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.bones.unfinished-chorus",
    "classification": "Zone corpse-raising block + finite damage/drain healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.flame.ember-mantle",
    "classification": "Restoration-conditioned external-healing flat add-on",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.life-prophecy-trigger",
    "classification": "Resource trigger requiring ≥1 actual HP; copies/reflections/staged excluded",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.garden-of-restoration",
    "classification": "Finite paid-zone healing pulses + stored restoration-conditioned +1 add-on",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.life-linked",
    "classification": "Damage-transfer link + rolled restoration-conditioned 1d4 add-on",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.life.life-prophecy",
    "classification": "Free Revelation activation + pre-resolution maximize-dice modifier + stored future flat healing add-on + nonrecursive radiant rider",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.time.rewind-wound",
    "classification": "Finite HP healing based specifically on actualHpDamage + bounded event-condition removal",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.time.the-spiral-opens",
    "classification": "Copied healing interface; explicit no triggers/procs and must still pay printed copied-healing cost/use",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:paladin:0",
    "classification": "BOOK finite Lay-on-Hands pool; Long Rest default refill",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:paladin:11",
    "classification": "BOOK sustained Oath healing-zone cadence",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.base.lay-on-hands",
    "classification": "Finite pool healing/cleanse",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.hero.lay-on-hands",
    "classification": "Finite pool mass allocation; entire remaining pool, 1/SR",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oathbreaker-shared.desecrated-ground",
    "classification": "Per-healing-die reduction; same-stat nonstacking",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.merciful-smite",
    "classification": "Damage-derived finite healing pool using actualDamageDealt; no Smite/heal-copy chain",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-mercy.channel-life",
    "classification": "Non-damage donor HP cost + finite recipient healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Donor non-damage HP cost first, cannot be prevented/refunded, must remain1. Recipient ordinary heal accepts legal modifiers. Packet forbids ALL excess-to-tempHP conversion across owners; eligible excess-to-damage conversion remains possible."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-vengeance.verdict-absolute",
    "classification": "Explicit source-specific Lay-on-Hands full refill",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-grief.last-rites",
    "classification": "Stabilization + death-save/necrotic protection; not healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-the-martyr-king.throne-s-grace",
    "classification": "Range bridge + pre-resolution +1 per healing die; no pool-point bonus",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:paladin:paladin.supplement.oath-of-the-martyr-king.crown-undying",
    "classification": "Damage redirect + finite secondary healing based on actually absorbed damage; no redirection/heal-copy chain",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:ranger:ranger.hero.warder.living-pulse",
    "classification": "Paid finite self-healing; explicitly unavailable Downed/Incapacitated; not passive regen",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:ranger:ranger.hero.warder.healing-touch",
    "classification": "Restoration-conditioned flat add-on to own paid spell/item healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:shaman:1",
    "classification": "BOOK Renewal Totem finite paid three-pulse healing package",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.hero.theurgist.benevolent-spirits",
    "classification": "Pre-resolution flat modifier to one qualifying paid technique; excludes copies/triggered heals",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.hero.bloodcaller.blood-feast",
    "classification": "Paid finite self-heal; unavailable Downed; no damage/resource proc",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.hero.bloodcaller.blood-curse",
    "classification": "Bleed cure interface; positive-potential magical healing grants its printed CON save, not auto-cure",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.hero.bloodcaller.talon-strike",
    "classification": "One-shot next-healing flat reduction",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:thief:thief.hero.blackguard.exsanguinate",
    "classification": "Paid finite self-heal; unavailable Incapacitated",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:tinker:tinker.hero.techsmith.snap-rebuild",
    "classification": "Device reconstruction, not living healing/resurrection; original slot/expiry retained",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-engine:warrior:24",
    "classification": "BOOK Mutation Recovery Reserve; spends only actual HP restored",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.",
      "Reserve spends only actualHP gained; unchanged reserve does not itself grant permission for excess conversion. Passive-reserve/excess eligibility remains explicit implementation-review question."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.hero.ironskin.cellular-reconstruction",
    "classification": "Finite delayed self-healing after stasis; not passive regeneration",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.bloodthick-node",
    "classification": "Passive regeneration, Reserve-limited",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.flesh-warden",
    "classification": "Maximum-HP stat modifier; never healing",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.rapid-coagulation",
    "classification": "Passive regeneration, Reserve-limited",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.adrenal-floodgate",
    "classification": "Finite 1/encounter triggered healing, not passive regeneration",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:warrior:warrior.supplement.bio-stabilizer",
    "classification": "Modifier to Bloodthick passive regeneration",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "class-card:wizard:wizard.hero.necromancer.infernal-pact-quest-based-unlock",
    "classification": "Gravebrand periodic damage + finite damage-drain healing based on actualDamageDealt",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "ordinary-spell:stitch-fate",
    "classification": "INDIVIDUAL DRAFT: stitch-fate; exact object pending review/promotion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "ordinary-spell:death-ward",
    "classification": "INDIVIDUAL DRAFT: death-ward; exact object pending review/promotion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "ordinary-spell:resurrection",
    "classification": "INDIVIDUAL DRAFT: resurrection; exact object pending review/promotion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "ordinary-spell:mass-resurrection-denial",
    "classification": "INDIVIDUAL DRAFT: mass-resurrection-denial; exact object pending review/promotion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "ordinary-spell:true-resurrection",
    "classification": "INDIVIDUAL DRAFT: true-resurrection; exact object pending review/promotion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  },
  {
    "bindingId": "ordinary-spell:soul-bind",
    "classification": "INDIVIDUAL DRAFT: soul-bind; exact object pending review/promotion",
    "overrides": [
      "Apply HEALING_DEATH_PLAYTEST.md only to this source's classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences."
    ]
  }
]