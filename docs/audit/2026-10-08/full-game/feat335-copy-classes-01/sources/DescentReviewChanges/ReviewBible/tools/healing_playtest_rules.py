"""Reviewed selected healing/death interfaces; not a full ability engine.

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
from custom_condition_rules import death_save_with_hp_prohibition


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


def finish_undying_spellform(state, *, ritual_ward=False, replacement_legal=True,
                            hp_gain_prohibited=False, stable_d4=None, now_seconds=0):
    """Only the Mage feature's explicit expiry consequence; no generic zero rule."""
    out=replace(state)
    if out.dead or out.hp>0:return out
    if not out.uses_death_saves:
        raise SpellRuleError('This player-class interface requires death-save state')
    out.stable=False
    out.stable_until_seconds=None
    out.death_failures=min(3,out.death_failures+1)
    if out.death_failures==3:
        # Offer replacement while death is pending, not after publishing Dead.
        pending=replace(state,stable=False,stable_until_seconds=None)
        out,_=would_die_transition(pending,ritual_ward=ritual_ward,
                                   replacement_legal=replacement_legal,
                                   hp_gain_prohibited=hp_gain_prohibited,
                                   stable_d4=stable_d4,now_seconds=now_seconds)
        if out.dead:out.death_failures=3
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
    # Delegate to the previously reviewed Decay bridge: blocked natural20
    # becomes Stable0 with cleared counters and immediate d4-hour deadline.
    out=death_save_with_hp_prohibition(state,natural,prohibited=hp_gain_prohibited,
                  regular_turn_id=regular_turn_id,regular=regular,modifier=modifier,
                  stable_d4=stable_d4,now_seconds=now_seconds)
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
        allowed=source_eligible and not (kind=='temp-hp' and self.forbid_temp_hp)
        if allowed and amount>self.remaining:raise SpellRuleError('Excess points cannot be spent twice')
        if internal:self.internal_resolved=True
        if not allowed:return 0
        self.remaining-=amount
        return amount


PASSIVE_RESERVE_REGENERATION=frozenset({
    'warrior.supplement.bloodthick-node',
    'warrior.supplement.rapid-coagulation',
    'warrior.hero.ironskin.regenerative-mutation',
    'warrior.supplement.bio-stabilizer',
})


def excess_conversion_eligible(source_id, *, otherwise_eligible,
                               explicit_passive_source_exception=False):
    """Source gate before allocating excess; not a cost/cadence validator.

    Bio-Stabilizer modifies Bloodthick and inherits its family exclusion. No
    current source grants the explicit future exception flag. Do not apply this
    exclusion to other finite/paid healing merely because actual HP gain is0.
    """
    return otherwise_eligible and (source_id not in PASSIVE_RESERVE_REGENERATION
                                  or explicit_passive_source_exception)


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
