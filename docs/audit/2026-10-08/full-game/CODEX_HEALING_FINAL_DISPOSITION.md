# Healing implementation corrections — bounded closure request

Codex → Calibration Review. Fixed both concrete findings; original implementation packet and your findings are preserved unchanged. All original source objects remain unchanged.

1. death_save_with_survival now DELEGATES to the already-reviewed custom death_save_with_hp_prohibition. The contradictory natural20 branch is removed, not duplicated. Tests require Stable0/counters0/d4 deadline/last turn preserved, no Ward spend, and exact agreement between the two entrypoints. False LifeV still has its different discussed blocked-recovery outcome.
2. excess_conversion_eligible explicitly rejects the four passive Reserve-regeneration sources for all excess conversion absent a future explicit source exception. Tested fullHP Bloodthick and Critical Regenerative (actual0/reserve0/conversion0), all four source IDs, and ordinary paid fullHP healing that retains eligible excess conversion.
3. Your confirmation retains Spiral phase through an independent successful Ward, with original clock/use unchanged.
4. Own follow-up correction: Mage Spellform expiry's third failure now offers independent Ward BEFORE final death. This was already promised by the guide but the previous helper directly killed; added targeted blockedHP→Stable0 Ward test. Also made invalid excess over-allocation transactional so a rejected request cannot consume internal-priority state; two targeted tests.

Current results:164 selected healing checks,120 unchanged Core damage states;150 control checks/9,393Speed states;98custom checks;153source checks. Six complete individually accepted spell candidates also pass preserved identity/classAccess/rank/minimum-level/RP comparisons and every class/level access boundary. No spell promoted yet.

Please explicitly close or identify remaining concrete defects for this bounded153-source interface and confirm the six individually reviewed+validated spell objects may move into operational playtest overlay. Broader DD24/131remaining matches/full temporal topology and the entire game remain open. Request individual source details if needed rather than infer them. Exact updated code/tests and validation are below; six unchanged accepted spell designs remain in the preceding packet.


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
    out,event=death_save_with_survival(dying,20,regular_turn_id=1,hp_gain_prohibited=True,stable_d4=2,now_seconds=50,ritual_ward=True)
    check('Blocked natural20 reuses reviewed Stable0 bridge',(out.hp,out.stable,out.death_successes,out.death_failures,out.stable_until_seconds,out.last_death_turn),(0,True,0,0,7250,1))
    check('Blocked natural20 creates no death or Ward spend',event['wardUsed'],False)
    check('Blocked natural20 helpers agree',out,death_save_with_hp_prohibition(dying,20,prohibited=True,regular_turn_id=1,stable_d4=2,now_seconds=50))
    out=finish_undying_spellform(dying,ritual_ward=True,hp_gain_prohibited=True,stable_d4=1,now_seconds=5)
    check('Mage expiry third failure offers independent Ward before death',(out.hp,out.dead,out.stable,out.death_failures,out.stable_until_seconds),(0,False,True,0,3605))
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
    for source,hp,wounds in [('warrior.supplement.bloodthick-node',20,()),
                              ('warrior.hero.ironskin.regenerative-mutation',19,(None,None,None))]:
        packet=healing_packet(LifeState(20,hp,wounds=wounds),10,reserve=10)
        ex=ExcessLedger(packet['genuineExcess'],internal_resolved=True)
        converted=ex.convert(3,kind='damage',source_eligible=excess_conversion_eligible(source,otherwise_eligible=True))
        check('Passive Reserve regeneration cannot power excess conversion: '+source,
              (packet['actualHpGained'],packet['reserveSpent'],converted),(0,0,0))
    check('All four passive Reserve profiles excluded',all(not excess_conversion_eligible(s,otherwise_eligible=True) for s in PASSIVE_RESERVE_REGENERATION),True)
    packet=healing_packet(LifeState(20,20),10)
    ex=ExcessLedger(packet['genuineExcess'],internal_resolved=True)
    check('Paid fullHP healing can retain legitimate excess conversion',ex.convert(4,kind='damage',source_eligible=excess_conversion_eligible('cleric.base.healing-rite',otherwise_eligible=True)),4)
    ex=ExcessLedger(2)
    rejects('Rejected internal over-allocation cannot commit ledger',lambda:ex.convert(3,kind='temp-hp',source_eligible=True,internal=True))
    check('Failed internal allocation leaves priority and quantity intact',(ex.remaining,ex.internal_resolved),(2,False))
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

## tools/validate_healing_spell_candidates.py
```
"""Individual candidate validation before any active catalog promotion."""
from pathlib import Path
import json
from build_spell_playtests import FIELDS
from spell_playtest_rules import access_for,quote_cast,SpellRuleError
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
IDS={'stitch-fate','death-ward','resurrection','mass-resurrection-denial','true-resurrection','soul-bind'}

def main():
    draft=json.loads((ROOT/'data/playtest/spell_drafts/candidate_healing_death.json').read_text(encoding='utf-8'))
    sources=json.loads((AUDIT/'HEALING_DEATH_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    captured={r['spellId']:r['spell'] for r in sources['spellCatalogRecords']}
    current={s['id']:s for s in json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))['spells']}
    assert set(captured)==IDS
    assert len(draft['spells'])==6 and {s['id'] for s in draft['spells']}==IDS
    checks=[];gates=0
    for s in draft['spells']:
        ident=s['id'];original=captured[ident]
        assert all(current[ident][key]==original[key] for key in ('id','source','classAccess'))
        assert all(key in s for key in FIELDS)
        assert isinstance(s['rangeFeet'],int) and not isinstance(s['rangeFeet'],bool) and s['rangeFeet']>=0
        assert isinstance(s['concentration'],bool) and s['components']==['V','S','F']
        assert all(isinstance(s[k],str) and s[k].strip() for k in FIELDS if k not in ('rangeFeet','concentration','components'))
        candidate=dict(current[ident],operational=s,status='operational-playtest-draft')
        for cls,entry in original['classAccess'].items():
            for level in range(1,21):
                try:access_for(candidate,cls,level);allowed=True
                except SpellRuleError:allowed=False
                assert allowed==(level>=entry['minimumClassLevel']),(ident,cls,level)
                gates+=1
            cast=quote_cast(candidate,cls,20,available_spell_ids={ident},rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=3)
            assert cast['cost']==entry['baseRpCost'] and cast['rank']==entry['rank']
        checks.append({'spellId':ident,'status':'PASS','preservedClassAccess':original['classAccess'],
                       'operationalInCurrentCatalog':current[ident]['operational'] is not None})
    report={'status':'PASS','scope':'Six complete individual operational objects, preserved source identity/access/ranks/levels/RP and all authorized class-level boundaries. Source design review is separate; this validator does not promote anything.',
            'candidateCount':6,'classLevelGateCases':gates,'spells':checks}
    (ROOT/'docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS6 healing/death spell candidates; {gates} class/level boundaries; preserved ranks/RP/source metadata.')
if __name__=='__main__':main()

```

## docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json
```
{
  "status": "PASS",
  "scope": "Six complete individual operational objects, preserved source identity/access/ranks/levels/RP and all authorized class-level boundaries. Source design review is separate; this validator does not promote anything.",
  "candidateCount": 6,
  "classLevelGateCases": 420,
  "spells": [
    {
      "spellId": "stitch-fate",
      "status": "PASS",
      "preservedClassAccess": {
        "Cleric": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Divination",
          "baseRpCost": 21
        },
        "Wizard": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Divination",
          "baseRpCost": 21
        }
      },
      "operationalInCurrentCatalog": false
    },
    {
      "spellId": "death-ward",
      "status": "PASS",
      "preservedClassAccess": {
        "Cleric": {
          "rank": 4,
          "minimumClassLevel": 7,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Crimson Agent": {
          "rank": 4,
          "minimumClassLevel": 11,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Druid": {
          "rank": 4,
          "minimumClassLevel": 7,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Shaman": {
          "rank": 4,
          "minimumClassLevel": 10,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Thief": {
          "rank": 4,
          "minimumClassLevel": 18,
          "school": "Necromancy",
          "baseRpCost": 7
        },
        "Wizard": {
          "rank": 4,
          "minimumClassLevel": 7,
          "school": "Necromancy",
          "baseRpCost": 7
        }
      },
      "operationalInCurrentCatalog": false
    },
    {
      "spellId": "resurrection",
      "status": "PASS",
      "preservedClassAccess": {
        "Cleric": {
          "rank": 7,
          "minimumClassLevel": 13,
          "school": "Necromancy",
          "baseRpCost": 17
        },
        "Druid": {
          "rank": 7,
          "minimumClassLevel": 13,
          "school": "Necromancy",
          "baseRpCost": 17
        },
        "Shaman": {
          "rank": 7,
          "minimumClassLevel": 19,
          "school": "Necromancy",
          "baseRpCost": 17
        },
        "Wizard": {
          "rank": 7,
          "minimumClassLevel": 13,
          "school": "Necromancy",
          "baseRpCost": 17
        }
      },
      "operationalInCurrentCatalog": false
    },
    {
      "spellId": "mass-resurrection-denial",
      "status": "PASS",
      "preservedClassAccess": {
        "Cleric": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Necromancy",
          "baseRpCost": 21
        },
        "Druid": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Necromancy",
          "baseRpCost": 21
        },
        "Wizard": {
          "rank": 8,
          "minimumClassLevel": 15,
          "school": "Necromancy",
          "baseRpCost": 21
        }
      },
      "operationalInCurrentCatalog": false
    },
    {
      "spellId": "true-resurrection",
      "status": "PASS",
      "preservedClassAccess": {
        "Cleric": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Druid": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Wizard": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        }
      },
      "operationalInCurrentCatalog": false
    },
    {
      "spellId": "soul-bind",
      "status": "PASS",
      "preservedClassAccess": {
        "Cleric": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Druid": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        },
        "Wizard": {
          "rank": 9,
          "minimumClassLevel": 17,
          "school": "Necromancy",
          "baseRpCost": 26
        }
      },
      "operationalInCurrentCatalog": false
    }
  ]
}

```

## Corrected candidate guide
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

False LifeV quarter-max direct recovery resolves at its next regular start before the death save. Blocked recovery leaves0 without invented stability; dead creatures do not revive. Spiral phase expires at its next regular start before normal start processing. Fate-BoundIV rerolls a failed death save before committing natural1/counters; use the new result. Its generic death-effect save bonus is not an ordinary death-save modifier. A natural20 whose1HP is blocked uses the previously reviewed Decay bridge: Stable0, cleared counters, immediate d4-hour deadline and preserved used-turn marker. It does not spend Ward. This differs from blocked False LifeV, which remains dying.

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

**NEW agreed source exclusion:** Unpaid passive regeneration bounded by Mutation Recovery Reserve cannot supply excess-healing conversions unless a future source explicitly grants an exception. This covers Bloodthick Node, Rapid Coagulation, Regenerative Mutation and Bio-Stabilizer as a Bloodthick modifier. FullHP/Critical may compute mathematical excess but grants no Cosmic conversion and spends no Reserve. Do not extend this exclusion to otherwise eligible paid/finite healing merely because it restores0HP.

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

Current selected checks:164 healing/death plus120 unchanged Core damage states;150 control including2 new clarification cases;98 custom including14 cure-presence cases;153 exact source records. These are interface tests, not execution of147 complete class cards, numerical balance, whole-game completion or a substitute for human playtesting.
