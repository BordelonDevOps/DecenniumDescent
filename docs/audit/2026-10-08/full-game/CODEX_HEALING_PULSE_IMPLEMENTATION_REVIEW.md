# Exact pulse implementation review

Codex → Calibration Review. Reply below15,000 characters. Review exacthelper/tests/guide against100 suppliedclassrecords plus6supportingpassages. Source integrity passes;71targetedchecks and301 reservepartitions pass. Original books/cards/frozenclassguide unchanged. Broader gameopen.

Implemented families: maintained BA windowsincludingLifewellfirstBA; Song/EnhancedlaterRC; prepaidMeditation/Bloom; delayedWoundEater/Hemostasis; Oraclefundedtargetwindows; Nano commandcap; fixed/repickedrecipients; Circle globalnamedbudget versus Field/Oracle/Renewalfamilyinstance; nativecadence withoutthreecap;finiteBloompartitions; Garden/Seedcontactentitlements; sourcebaseRenewal/Echo alternatives.

Caller boundary is deliberate: exact original virtualmarkers and actualsourceauthorizedexpiry; canonicalRP/RC andBAavailability; initialcosts alreadycommitted; actualsourceownership/targetlegality andsidecaps (3allies+3enemies, never6allies); range/alive/line-of-effect; allowedsuppression/maintenance; concentration/source-death state; olddeviceanchorlifeandcommandbudget. This is a boundedreference, notfullclassexecution. BlockedHP/Decay/fullHP doesnotbecomewhole_effect_suppressed.

Specific reviewquestions:
1. EnhancedGarden says 'firstGardenpulse' whilebasecure saysfirstentryORstart. Candidate treatsEnhancedvariant asreplacingbasecontact entitlement withfirst-pulse cureboth (oneentitlement, noentrycurethenextraenhancedcure). Explicitlyproposedin guide; please confirmorcorrect.
2. Entireeffectsuppressed scheduledoccurrence stillconsumesownopportunity/window, butgrantsno namedbenefit anddoesnotclaimglobalCirclebenefitledger; onlyHPgainblocked stillclaimsthenormalbenefitbudget. Confirm.
3. UnfinishedChorus ownturn drain is modeledinitialincluded, one laterownregularturnpaid1RC withnoBA, fixedroster≤3+3 butoneenemy/onehealdestinationperpulsecheckedbycaller. Firstreplysourceclassification saidincludedfirstsource-turnpulse. Please verifyexacttiming/end.
4. Earlierwording invoked 'alreadyreviewedhealing/totemarbitration' forEcho. Actual existinghealing_packet Totembranch rule is BLIGHT reduction, notEchoRenewal. I have explicitlylabeledEcho shared-family/strongestpreview assource-specificintegration ratherthanpretendingexistinghelperalreadyimplementsit. renewal_branch_bases returns2parent/1Echo alternatives ONLY; callerpreviewsappropriatelymodifiedbranchesandcommitsone. Parentdestruction remainsdeferred.
5. Sameopportunity independentRenewals strongestnonstack isguide/callerarbitration; helperreceivesalreadywinnerlegalapplication. Separateinstancesatdifferenttimesmayeachhealsameround. NoinventedglobalRenewalroundcap.

Please identifyconcretedefects beforeboundeddisposition, includingclocksatlateobservations, paymentfailures, fixedrosters, missedpulses, suppression andsubtle sourceexceptions. All100classificationrows staydiscussionroleonlypendingthisreview; closure ifgrantedappliesonlysuppliedroles/schedulerprimitive, notwholecards. Broadercompanion230candidateinventory awaitsnextconference.


## docs/mechanics/HEALING_PULSE_PLAYTEST.md

# Healing pulses, sustained zones and upkeep

**IN REVIEW.** The100 source candidates have individual discussion roles in the [source register](HEALING_PULSE_SOURCE_BINDINGS.md); many are guards, one-time effects or already reviewed modifiers. The [boundary conference](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_BOUNDARIES.md) corrects the first proposals. Original cards, books and the frozen class guide remain unchanged.

This overlay defines the supplied recurring-healing schedules. Each legal healing application still uses the [healing interface](HEALING_DEATH_PLAYTEST.md). Resource cost, pulse occurrence, actual HP restored and independent cure/resource components are different events.

## Keep the original clock

Use the original source or target regular-turn markers. Extra turns do not advance periodic healing, refill opportunities, generate upkeep, or reset these deadlines. Leaving/reentering initiative, reordering and source removal do not restart clocks.

Outside initiative preserve existing virtual markers. For activation at second2 with source starts0/6/12/18, later starts are6/12, not8/14. Establish one coherent six-second virtual schedule only when none exists. Bare outside-initiative round durations still use their separately reviewed absolute deadline; do not run both timing models for one component.

Ordinary start-expiry precedes start triggers. Explicit finite sequences own their printed due opportunities: Hemostasis's third target-start tick and Wound Eater IV's third source-start tick resolve before their sequence ends. A three-round target-start aura instead expires at its normal source deadline even if a creature received fewer than three pulses.

## Source schedules

Activation costs below are paid before the series exists; quoted later costs never refund an activation, limited use, BG, Ki, slot or Conviction.

| Source | First opportunity | Later opportunities and cost | End |
|---|---|---|---|
| Lifewell | Action4RP + all BG (at least3) establishes it; first same-turn heal still needs BA+1RP | Next2 regular source turns, each BA+1RP; fixed≤3 allies | Missed maintenance: that source turn end; otherwise startturn4 |
| Healing Briar | Action4RP includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies in fixed natural-ground zone | Same |
| Circle of Harmony | Action2Ki+3RP includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies in fixed zone | Same |
| Restoration Field | Action3RP + slot includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies/functional devices | Same; this exact lifetime is a labeled default integration |
| Renewal Totem | Action2RP includes first heal | Next2 regular turns BA+1RP; repick≤3 allies | Same; Extended Totem adds one paid fourth turn and expires startturn5 |
| Sacred Chant | Action1RP includes nonhealing pulse1 | Next2 regular turns BA,0RP | Same; printed Conviction only, no invented healing |
| Sacrament / Dark Sacrament | Printed Action/Conviction/RP includes first pulse | Next2 regular turns BA+1RP, supplied by Cleric engine5 | Same; up to3 allies and3 qualifying enemies separately |
| Desecrated Ground | Action7RP includes first damage pulse | Next2 regular turns BA+1RP,≤3 enemies | Same; no healing output |
| Song of Mending | Action3RC includes pulse1, fixed≤3 allies | Source-next-regular-start pulse2 costs1RC; Enhanced adds second-later-start pulse3 for another1RC | Unpaid due pulse ends immediately; normal2/3-round duration otherwise |
| Unfinished Chorus | Action3RC includes first source-turn drain | One later regular source-turn drain costs1RC, no invented upkeep action; choose from the fixed zone set | Two-round deadline; missed upkeep ends that source turn |
| Transcendent Meditation | Action3Ki+4RP/short-rest use includes pulse1 | Next2 source regular starts, prepaid, fixed self+≤3 allies | Normal3-source-turn duration; concentration required |
| Eternal Bloom | Final Action/long-rest use; activation installment1 | Next2 source regular starts; prepaid installments2/3 | Normal3-round duration; no extraRC |
| Wound Eater IV | BA2RC establishes aura; first drain at next source regular start | Following2 source starts cost1RC each | After third pulse; unpaid later pulse ends at its due marker |
| Hemostasis | Pay printed additional1RP with eligible application | Next3 target regular starts, prepaid | After third opportunity |
| Cellular Reconstruction / Cleric Echoes | Printed activation/trigger stores one delayed event | Next source regular start, prepaid | After that opportunity; full stasis/copy rules are separately owned |
| Nano-Aegis Drone | Action2RP enters support mode; no immediate heal | Each legal BA command costs1RP; choose heal OR temporaryHP; at most3 total | Three-round mode; skipping command does not end mode |

All listed concentration requirements remain. Starting replacement concentration or becoming Incapacitated ends those effects immediately. An effect with no concentration requirement does not gain one merely because it is in this table. Incapacity still prevents required actions. A suppressed maintenance activation is illegal if the actual suppression says so; output suppression alone need not prevent an otherwise legal payment.

For ordinary paid three-pulse effects, maintenance must occur by the end of the corresponding regular source turn. Missing it ends the effect at that turn's end, with no later resumption. Lifewell also checks its activation turn. Paying early for a future turn is not permitted. A legal empty pulse can maintain a source that permits up toN targets; it consumes its cost and opportunity.

**Worked Lifewell example:** starting with12RP and3BG, activation plus first BA pulse spends5RP and all3BG, leaving7RP. Turn2 maintenance leaves6RP; turn3 leaves5RP. Losing the turn2 maintenance ends Lifewell that turn; neither the daily use nor first payments return.

## Oracle target-start windows

Garden, Resonant Seed and Burning Blood V have activation-funded window1. At each of the next two original source regular starts, pay1RC once to fund the next window, or end the effect. No upkeep action is invented. Each window ends at the following source regular start. Their persistent zones require concentration and fixed sets of at most3 allies and3 enemies, as applicable to each source.

Burning Blood V is a Curse Boon, separately gained alongside the Mystery Final; it receives no Final payment exemption. Its enemy-start damage does not turn its once-on-your-turn self-healing trigger into a heal on every enemy turn.

Crown Restored is a Final: its finite windows are prepaid, with no generic extraRC. Its fixed ally set contains at most3 including the Oracle if selected. A BA self-cast after that turn's start can give the Oracle only2 subsequent self-start heals before startturn4 expiry. Maximum3 per creature is a cap, not a promise.

Evaluate target-start effects on that target's original regular marker while it is eligible and inside the live zone. Both the funded window and numbered-round budget must be available. Entry/reentry or moving a Totem does not create entry healing. An ally that missed a start while outside loses that opportunity; it does not bank healing.

Oracle zone benefits use one fixed set across healing, floors, immunity and other aura benefits unless a source explicitly separates sets. Eternal Bloom's chosen≤3 living allies must be inside at activation; new entrants gain no reserve, floor or necrotic immunity. Selected targets regain applicable continuous benefits on legal reentry while the source remains active.

## Targets, payments and separate budgets

Declare legal recipients before rolling or learning outcomes. Fixed targets cannot be replaced. For repicked sources, select a new legal set for each pulse before its outcomes. Loss of eligibility after declaration skips that application without replacing it or refunding payment.

Commit the legal upkeep action/resource and opportunity before HP resolution. Full HP, Decay and zero actual healing do not refund costs, restore a pulse, or allow a replacement target. Healing prohibition does not automatically suppress an independent printed cure. All source target restrictions, ally/enemy subcaps and clear line of effect remain caller responsibilities.

| Budget | Domain |
|---|---|
| Circle of Harmony | NEW global named effect + target + numbered round, across owners |
| Restoration Field | Field instance + target + numbered round |
| Oracle engine26 | Zone instance + target + numbered round, plus one application per funded window |
| Renewal + its Echo | One parent-family instance, one pulse ID, one up-to3 recipient budget and target/round ledger |
| Separate Renewal instances | No invented global once/round ceiling; simultaneous same-opportunity overlap uses the strongest legal branch |
| Nano-Aegis | Printed max3 commands per mode; caller enforces the applicable shared companion command limit |

A paid pulse at a distinct scheduled time from another independent Renewal can heal in the same round. Same-opportunity overlapping Renewal auras never add together.

Parent/Echo Renewal shares one upkeep payment, concentration and opportunity. From legal coverage, parent source base is2 and Echo source base is1. Construct the separate legal branches with correct modifier placement, select the stronger preview, then commit one healing application. Never add both or halve the already modified parent final heal. This is a source-specific new scheduling/arbitration integration; the existing Blight Totem reduction comparison is a different rule.

The scheduler takes each anchor's active/coverage state from the future object lifecycle. Parent destruction does not yet authorize this package to destroy or preserve its Echo. Both anchors never supply a six-target budget.

## Finite installments and independent components

Eternal Bloom records each chosen ally's missingHP at activation. Divide into3 integer installments; assign remainder to earlier pulses:10 becomes4/3/3,1 becomes1/0/0. At each scheduled opportunity consume the next installment. Outside, dead or suppressed targets lose it. Returning later never recovers the lost share, and new damage never grows the original reserve.

Bloom's once-per-selected-ally 1HP floor is separately tracked by the already reviewed survival interface. It neither consumes nor replenishes installments. The target must still be eligible and inside; full healing prohibition does not turn prevention into healing.

Garden gives a first-entry-or-start cure opportunity independent of HP gain. Seed's cure belongs to its first healing pulse, not entry. **Proposed precise mastery interpretation, pending exact review:** Enhanced Garden replaces this with its printed first-pulse cure-both opportunity, using one entitlement rather than granting both an entry cure and a second enhanced cure.

Transcendent Meditation's second pulse supplies its printed1Ki even if every HP gain is blocked. Suppressing the whole effect also suppresses Ki for that occurrence; suppressing only healing does not. No missed independent component is banked.

Hemostasis and other prepaid effects preserve each target/source clock. A late observation records missed opportunities without performing catch-up recovery.

Hemostasis permits only one such healing effect per target. Creating a separate series does not authorize stacking a second instance; the caller enforces active-effect eligibility. For Unfinished Chorus the fixed zone roster remains≤3 allies/3 enemies, but a drain chooses only one eligible enemy and one healing destination (self or one eligible ally) per pulse.

## Native recurrence and device limits

Aura of Grace, Living Pulse and Thief Exsanguinate retain their optional1RP regular-start heal and their printed eligibility gates. Regenerative Mutation, Bloodthick Node and Rapid Coagulation retain their real-encounter, mutation and movement gates and spend Mutation Recovery Reserve per actual HP restored. Bio-Stabilizer modifies Bloodthick; it is not another pulse.

These native effects have no generic three-pulse ceiling. Extra turns provide no new periodic recovery tick. Explicit restrictions on Downed, Incapacitated, enemy proximity or natural terrain remain source-specific.

Efficient Power Cells extends eligible nonhealing deployments only. Mech Overdrive extends eligible device duration, never healing capacity, charges, ammunition or resource recovery. A disabled device's duration continues. Whether it can accept a support command or maintenance depends on the actual disabled-state rule; the scheduler grants no permission.

## Reference boundary

The reference helper accepts already paid legal activation, exact original clock markers, a canonical wallet/action state and a shared recipient ledger. It does not itself pay initial BG/Conviction/Ki, enforce acquisition, choose targets, roll/heal, compute Echo final previews, implement object destruction, or execute the entire companion command engine.

Profile target caps of6 for mixed Oracle/Cleric effects mean3 allies plus3 eligible enemies, not6 of one side. The caller must validate these subcaps before creating a fixed roster or committing recipients. The helper's generic recipient count does not grant broader targeting.

Source-qualified independent components and remaining guard/exclusion records retain their separate guides. The supplied100 class passages and the negative scan of78 operational spell drafts do not cover770 unfinished spells or unsupplied items/monsters.


## tools/healing_pulse_playtest_rules.py

"""Bounded pulse clocks/budgets. Source legality, actions and HP pipeline stay separate.

IN REVIEW. Callers supply the original virtual clock markers, canonical wallet
and shared target ledger. These helpers never cast, heal, repair, create a
companion, or infer permission to maintain a suppressed/incapacitated effect.
"""
from dataclasses import dataclass,field
from spell_playtest_rules import integer,SpellRuleError
from control_playtest_rules import ClockMarker,require_deadline


@dataclass
class PulseWallet:
    rp:int=0
    rc:int=0
    bonus_action:bool=True
    def spend(self,amount,currency='RP',*,bonus_action=False):
        integer(self.rp,'RP',0);integer(self.rc,'RC',0)
        integer(amount,'pulse cost',0)
        if currency not in ('RP','RC'):raise SpellRuleError('Unknown pulse currency')
        attr=currency.lower()
        if getattr(self,attr)<amount or (bonus_action and not self.bonus_action):
            raise SpellRuleError('Required pulse resource/action unavailable')
        setattr(self,attr,getattr(self,attr)-amount)
        if bonus_action:self.bonus_action=False


@dataclass
class RecipientLedger:
    claimed:set=field(default_factory=set)
    def check(self,domain,targets,round_number):
        integer(round_number,'numbered round',1)
        if domain and any((domain,t,round_number) in self.claimed for t in targets):
            raise SpellRuleError('Target already received this domain this numbered round')
    def commit(self,domain,targets,round_number):
        self.check(domain,targets,round_number)
        if domain:self.claimed.update((domain,t,round_number) for t in targets)


@dataclass(frozen=True)
class PulseProfile:
    mode:str
    count:int
    initial:bool=True
    later_cost:int=0
    currency:str='RP'
    fixed:bool=False
    target_cap:int=3
    round_domain:str=''
    maintenance_bonus_action:bool=True


PROFILES={
    'sacred-chant':PulseProfile('maintenance',3,target_cap=0),
    'sacrament':PulseProfile('maintenance',3,later_cost=1,target_cap=6),
    'dark-sacrament':PulseProfile('maintenance',3,later_cost=1,target_cap=6),
    'healing-briar':PulseProfile('maintenance',3,later_cost=1),
    'circle-of-harmony':PulseProfile('maintenance',3,later_cost=1,round_domain='named-circle'),
    'renewal':PulseProfile('maintenance',3,later_cost=1,round_domain='instance'),
    'renewal-extended':PulseProfile('maintenance',4,later_cost=1,round_domain='instance'),
    'restoration-field':PulseProfile('maintenance',3,later_cost=1,round_domain='instance'),
    'desecrated-ground':PulseProfile('maintenance',3,later_cost=1),
    'lifewell':PulseProfile('maintenance',3,initial=False,later_cost=1,fixed=True),
    'unfinished-chorus':PulseProfile('maintenance',2,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance',maintenance_bonus_action=False),
    'song-of-mending':PulseProfile('sequence',2,later_cost=1,currency='RC',fixed=True,round_domain='instance'),
    'enhanced-song':PulseProfile('sequence',3,later_cost=1,currency='RC',fixed=True,round_domain='instance'),
    'transcendent-meditation':PulseProfile('sequence',3,fixed=True,target_cap=4),
    'eternal-bloom':PulseProfile('sequence',3,fixed=True,round_domain='instance'),
    'wound-eater-iv':PulseProfile('delayed-sequence',3,later_cost=1,currency='RC',fixed=True,round_domain='instance'),
    'hemostasis':PulseProfile('delayed-sequence',3,fixed=True,target_cap=1),
    'cellular-reconstruction':PulseProfile('delayed-sequence',1,fixed=True,target_cap=1),
    'cleric-echoes':PulseProfile('delayed-sequence',1,fixed=True,target_cap=1),
    'resonant-seed':PulseProfile('window',3,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance'),
    'garden':PulseProfile('window',3,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance'),
    'burning-blood-v':PulseProfile('window',3,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance'),
    'crown-restored':PulseProfile('window',3,fixed=True,round_domain='instance'),
    'nano-aegis':PulseProfile('command',3,initial=False,later_cost=1,target_cap=1),
}


def distinct_targets(values,cap):
    values=tuple(values)
    if any(not isinstance(v,str) or not v for v in values) or len(values)!=len(set(values)) or len(values)>cap:
        raise SpellRuleError('Invalid, duplicate or excessive declared recipients')
    return values


@dataclass
class PulseSeries:
    instance_id:str
    profile_name:str
    activation:ClockMarker
    future_starts:tuple
    ledger:RecipientLedger
    roster:tuple=()
    # For maintenance: activation turn end, then one end for each later turn.
    maintenance_ends:tuple=()
    # Override only for an actual source-authorized duration extension, never cap.
    expires:ClockMarker|None=None
    states:list=field(init=False)
    declarations:dict=field(default_factory=dict,init=False)
    applications:set=field(default_factory=set,init=False)
    ended_at:ClockMarker|None=field(default=None,init=False)
    ended_reason:str|None=field(default=None,init=False)

    def __post_init__(self):
        if not self.instance_id or self.profile_name not in PROFILES:raise SpellRuleError('Unknown pulse instance/profile')
        self.profile=PROFILES[self.profile_name]
        require_deadline(self.activation)
        self.future_starts=tuple(require_deadline(v) for v in self.future_starts)
        needed=self.profile.count if self.profile.mode!='command' else 3
        if len(self.future_starts)!=needed or any(a>=b for a,b in zip((self.activation,)+self.future_starts,self.future_starts)):
            raise SpellRuleError('Supply strictly ordered original virtual future markers')
        self.roster=distinct_targets(self.roster,self.profile.target_cap)
        if not self.profile.fixed and self.roster:raise SpellRuleError('Repicked source has no fixed roster')
        if self.profile.mode=='maintenance':
            self.maintenance_ends=tuple(require_deadline(v) for v in self.maintenance_ends)
            opens=(self.activation,)+self.future_starts[:-1]
            if len(self.maintenance_ends)!=self.profile.count or any(not (a<b<c) for a,b,c in zip(opens,self.maintenance_ends,self.future_starts)):
                raise SpellRuleError('Supply each actual source-turn maintenance deadline')
        elif self.maintenance_ends:raise SpellRuleError('Unexpected maintenance turn ends')
        if self.expires is not None:require_deadline(self.expires)
        if self.profile.mode=='delayed-sequence':
            if self.expires is not None:raise SpellRuleError('Explicit delayed sequence ends after final opportunity')
            self.opens=self.future_starts
        elif self.profile.mode=='command':
            self.opens=()
            self.expires=self.expires or self.future_starts[-1]
        else:
            self.opens=(self.activation,)+self.future_starts[:-1]
            self.expires=self.expires or self.future_starts[-1]
        if self.expires is not None and self.expires<=self.activation:raise SpellRuleError('Invalid effect expiry')
        self.states=['pending']*self.profile.count
        if self.profile.mode=='window':
            # Initial activation funds first window; printed Final funds all.
            self.states[0]='funded'
            if self.profile.later_cost==0:self.states=['funded']*self.profile.count

    def domain(self):
        if self.profile.round_domain=='named-circle':return 'named:Circle of Harmony'
        return 'pulse:'+self.instance_id if self.profile.round_domain=='instance' else ''

    def end(self,at,reason):
        require_deadline(at)
        if self.ended_at is None:
            self.ended_at=at;self.ended_reason=reason
            self.states=['lost' if s in ('pending','funded') else s for s in self.states]

    def advance(self,now):
        """Retire missed markers; never perform catch-up healing or refund costs."""
        require_deadline(now)
        if now<self.activation:raise SpellRuleError('Cannot observe before activation')
        if self.ended_at is not None:return
        mode=self.profile.mode
        if mode=='command':
            if now>=self.expires:self.end(self.expires,'duration')
            return
        observation_limit=min(now,self.expires) if self.expires is not None else now
        if mode=='window':
            for i,status in enumerate(self.states):
                if status=='funded' and now>=self.future_starts[i]:self.states[i]='closed'
        for i,status in enumerate(self.states):
            if status!='pending':continue
            if mode=='maintenance':
                deadline=self.maintenance_ends[i]
                missed=observation_limit>=deadline
            else:
                deadline=self.opens[i];missed=observation_limit>deadline
            if not missed:continue
            self.states[i]='lost'
            if mode in ('maintenance','window') or (mode=='sequence' and i>0 and self.profile.later_cost) or (mode=='delayed-sequence' and i>0 and self.profile.later_cost):
                self.end(deadline,'missed upkeep');return
        if mode=='delayed-sequence' and all(s!='pending' for s in self.states):
            self.end(self.opens[-1],'sequence exhausted')
        elif self.expires is not None and now>=self.expires:self.end(self.expires,'duration')

    def _targets(self,targets):
        targets=distinct_targets(targets,self.profile.target_cap)
        if self.profile.fixed and not set(targets)<=set(self.roster):raise SpellRuleError('Recipient was not fixed at activation')
        return targets

    def resolve(self,index,now,targets,wallet,*,round_number,regular=True,
                upkeep_legal=True,whole_effect_suppressed=False):
        """Commit one non-window opportunity before HP outcomes.

        Caller supplies already legal declared recipients, source-specific
        ally/enemy subcaps, and source eligibility. HP blocks/fullHP are NOT
        whole-effect suppression. Whole suppression consumes clock/opportunity
        but grants no target benefit/independent component.
        """
        integer(index,'pulse index',0,self.profile.count-1)
        self.advance(now)
        if self.ended_at is not None:raise SpellRuleError('Effect ended')
        mode=self.profile.mode
        if mode in ('window','command'):raise SpellRuleError('Use the correct window/command method')
        if not regular or not upkeep_legal:raise SpellRuleError('Not a legal regular pulse/maintenance')
        if self.states[index]!='pending':raise SpellRuleError('Opportunity already consumed')
        if any(s=='pending' for s in self.states[:index]):raise SpellRuleError('Earlier opportunity unresolved')
        initial_included=index==0 and self.profile.initial and mode!='delayed-sequence'
        if mode=='maintenance' and not initial_included:
            if not self.opens[index]<=now<self.maintenance_ends[index]:raise SpellRuleError('Outside maintenance window')
            needs_ba=self.profile.maintenance_bonus_action
        else:
            if now!=self.opens[index]:raise SpellRuleError('Not the exact registered due marker')
            needs_ba=False
        chosen=self._targets(targets)
        output=() if whole_effect_suppressed else chosen
        self.ledger.check(self.domain(),output,round_number)
        cost=0 if initial_included or (mode=='delayed-sequence' and index==0) else self.profile.later_cost
        wallet.spend(cost,self.profile.currency,bonus_action=needs_ba)
        self.ledger.commit(self.domain(),output,round_number)
        self.states[index]='committed';self.declarations[index]=chosen
        result={'pulseId':f'{self.instance_id}:{index}','occurred':True,'declaredTargets':chosen,
                'outputTargets':output,'cost':cost,'bonusActionSpent':needs_ba,
                'independentKi':1 if self.profile_name=='transcendent-meditation' and index==1 and not whole_effect_suppressed else 0}
        if mode=='delayed-sequence' and index==self.profile.count-1:self.end(now,'sequence exhausted')
        return result

    def fund(self,index,now,wallet,*,regular=True,upkeep_legal=True):
        integer(index,'window index',0,self.profile.count-1)
        self.advance(now)
        if self.ended_at is not None or self.profile.mode!='window':raise SpellRuleError('Not an active window effect')
        if not regular or not upkeep_legal or now!=self.opens[index] or self.states[index]!='pending':
            raise SpellRuleError('Window funding is due once at its original source marker')
        try:wallet.spend(self.profile.later_cost,self.profile.currency)
        except SpellRuleError:
            self.end(now,'unpaid due window')
            raise
        self.states[index]='funded'

    def target_start(self,target,now,*,round_number,regular=True,eligible=True,
                     whole_effect_suppressed=False):
        self.advance(now)
        if self.ended_at is not None or self.profile.mode!='window':return None
        if not regular or not eligible:return None
        self._targets((target,))
        index=next((i for i in range(self.profile.count) if self.opens[i]<=now<self.future_starts[i]),None)
        if index is None or self.states[index]!='funded':return None
        if (index,target) in self.applications:return None
        integer(round_number,'numbered round',1)
        self.applications.add((index,target))
        if (self.domain(),target,round_number) in self.ledger.claimed:return None
        # A suppressed occurrence is lost; it does not deliver a named benefit.
        if not whole_effect_suppressed:self.ledger.commit(self.domain(),(target,),round_number)
        return {'pulseId':f'{self.instance_id}:{index}:{target}','occurred':True,
                'outputTargets':() if whole_effect_suppressed else (target,)}

    def command(self,now,target,wallet,*,option,command_legal=True):
        self.advance(now)
        if self.ended_at is not None or self.profile.mode!='command':raise SpellRuleError('Not an active command mode')
        if option not in ('heal','temporary-hp') or not command_legal:raise SpellRuleError('Illegal support command')
        self._targets((target,))
        try:index=self.states.index('pending')
        except ValueError:raise SpellRuleError('Command pulse cap exhausted') from None
        wallet.spend(1,'RP',bonus_action=True)
        self.states[index]='committed';self.declarations[index]=(target,)
        return {'pulseId':f'{self.instance_id}:{index}','option':option,'target':target}


def installments(reserve,count=3):
    integer(reserve,'recorded missing HP',0);integer(count,'installment count',1)
    base,remainder=divmod(reserve,count)
    return tuple(base+int(i<remainder) for i in range(count))


def renewal_branch_bases(*,parent_active,parent_covers,echo_active,echo_covers):
    """Preview legal source bases, then caller applies/compares healing branches.

    This supplied Renewal has flat2 base. Echo half occurs here, before target
    modifiers; both anchors share ONE PulseSeries and its three-recipient cap.
    No parent-destruction relationship is inferred.
    """
    result={}
    if parent_active and parent_covers:result['parent']=2
    if echo_active and echo_covers:result['echo']=1
    return result


@dataclass
class BloomReserve:
    roster_missing:dict
    consumed:set=field(default_factory=set)
    def __post_init__(self):
        distinct_targets(self.roster_missing,3)
        self.shares={target:installments(value) for target,value in self.roster_missing.items()}
    def consume(self,index,*,eligible_targets):
        integer(index,'Bloom installment',0,2)
        if index in self.consumed:raise SpellRuleError('Installment already consumed')
        if self.consumed!=set(range(index)):raise SpellRuleError('Consume every scheduled installment in order')
        eligible=set(eligible_targets)
        if not eligible<=set(self.shares):raise SpellRuleError('Bloom cannot add new entrants')
        self.consumed.add(index)
        return {target:parts[index] for target,parts in self.shares.items() if target in eligible}


@dataclass
class FirstContactLedger:
    profiles:dict
    consumed:set=field(default_factory=set)
    def __post_init__(self):
        if any(source not in ('garden','enhanced-garden','resonant-seed') for source in self.profiles.values()):
            raise SpellRuleError('Unknown cure contact source')
    def claim(self,instance,target,*,event,eligible=True):
        if instance not in self.profiles:raise SpellRuleError('Unknown contact instance')
        source=self.profiles[instance]
        if event not in ('entry','pulse','start'):raise SpellRuleError('Unknown contact event')
        if not eligible or (source=='resonant-seed' and event!='pulse') or (source=='enhanced-garden' and event!='pulse'):
            return False
        key=(instance,target)
        if key in self.consumed:return False
        self.consumed.add(key)
        return True


@dataclass
class NativeOccurrenceLedger:
    consumed:set=field(default_factory=set)
    def commit(self,source,owner,marker,wallet,*,regular=True,eligible=True):
        costs={'aura-of-grace':1,'living-pulse':1,'thief-exsanguinate':1,
               'regenerative-mutation':0,'bloodthick-node':0,'rapid-coagulation':0}
        if source not in costs:raise SpellRuleError('Unknown native recurrence source')
        require_deadline(marker)
        if not owner:raise SpellRuleError('Native pulse needs owner identity')
        key=(source,owner,marker)
        if not regular or not eligible or key in self.consumed:return False
        wallet.spend(costs[source])
        self.consumed.add(key)
        return True


## tools/validate_healing_pulse_playtests.py

"""Adversarial scheduling/budget checks; does not certify full source execution."""
from pathlib import Path
import json
from healing_pulse_playtest_rules import *
ROOT=Path(__file__).resolve().parents[1]

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append({'name':name,'result':'PASS'})
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append({'name':name,'result':'PASS'})
        else:raise AssertionError(name)
    def series(profile,ident='effect',roster=(),ledger=None,activation=None,expires=None):
        p=PROFILES[profile];n=p.count if p.mode!='command' else 3
        starts=tuple(ClockMarker(6*(i+1)) for i in range(n))
        ends=tuple(ClockMarker(6*i,20) for i in range(n)) if p.mode=='maintenance' else ()
        return PulseSeries(ident,profile,activation or ClockMarker(0,5),starts,
                           ledger or RecipientLedger(),roster,ends,expires)
    w=PulseWallet(rp=8);briar=series('healing-briar')
    a=briar.resolve(0,ClockMarker(0,5),('a','b'),w,round_number=1)
    check('Initial Briar included without BA/additionalRP',(a['cost'],w.rp,w.bonus_action),(0,8,True))
    a=briar.resolve(1,ClockMarker(6,10),('c',),w,round_number=2)
    check('Later Briar repicks before outcomes and pays BA1RP',(a['declaredTargets'],w.rp,w.bonus_action),(('c',),7,False))
    rejects('Cannot replay paid pulse',lambda:briar.resolve(1,ClockMarker(6,11),('d',),w,round_number=2))
    check('Replay never charges again',w.rp,7)
    briar.advance(ClockMarker(12,20))
    check('Missed upkeep ends at due turn end',(briar.ended_at,briar.ended_reason),(ClockMarker(12,20),'missed upkeep'))
    rejects('Cannot resume missed upkeep',lambda:briar.resolve(2,ClockMarker(18,10),('a',),PulseWallet(rp=4),round_number=4))
    lw=series('lifewell',roster=('a','b'));w=PulseWallet(rp=8)
    a=lw.resolve(0,ClockMarker(0,10),('a',),w,round_number=1)
    check('Lifewell first pulse already costs BA1RP',(w.rp,w.bonus_action,a['cost']),(7,False,1))
    rejects('Lifewell cannot replace fixed target',lambda:lw.resolve(1,ClockMarker(6,10),('new',),PulseWallet(rp=4),round_number=2))
    absent=series('lifewell',roster=('a',));absent.advance(ClockMarker(0,20))
    check('No Lifewell first BA ends at activation turn end',absent.ended_at,ClockMarker(0,20))
    b=series('dark-sacrament');w=PulseWallet(rp=3)
    b.resolve(0,ClockMarker(0,5),('ally','enemy'),w,round_number=1)
    b.resolve(1,ClockMarker(6,10),(),w,round_number=2)
    check('Empty legal DarkSacrament pulse maintains with BA1RP',(w.rp,w.bonus_action,b.states[1]),(2,False,'committed'))
    b=series('restoration-field');w=PulseWallet(rp=4)
    b.resolve(0,ClockMarker(0,5),('full','decayed'),w,round_number=1)
    b.resolve(1,ClockMarker(6,10),('full','decayed'),w,round_number=2)
    check('Full/Decay outcomes cannot refund committed Field',(w.rp,b.declarations[1]),(3,('full','decayed')))
    b=series('renewal-extended');w=PulseWallet(rp=5)
    b.resolve(0,ClockMarker(0,5),('a',),w,round_number=1)
    for i in (1,2,3):
        w.bonus_action=True;b.resolve(i,ClockMarker(i*6,10),('a',),w,round_number=i+1)
    check('Extended Renewal fourth requires total3upkeepRP',w.rp,2)
    rejects('Extended Renewal never fifth',lambda:b.resolve(4,ClockMarker(24,10),('a',),w,round_number=5))
    b.advance(ClockMarker(24));check('Extended Renewal expires startturn5',b.ended_at,ClockMarker(24))
    circles=RecipientLedger()
    c1=series('circle-of-harmony','c1',ledger=circles)
    c2=series('circle-of-harmony','c2',ledger=circles)
    c1.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    rejects('Circle named cap crosses owner instances',lambda:c2.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1))
    c2.resolve(0,ClockMarker(0,5),('b',),PulseWallet(),round_number=1)
    check('Other legal Circle target still available',c2.declarations[0],('b',))
    common=RecipientLedger()
    f1=series('restoration-field','f1',ledger=common);f2=series('restoration-field','f2',ledger=common)
    for f in (f1,f2):f.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    check('Independent Field instances may each affect same target',len(common.claimed),2)
    ren1=series('renewal','r1',ledger=common);ren2=series('renewal','r2',ledger=common,activation=ClockMarker(0,6))
    ren1.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    ren2.resolve(0,ClockMarker(0,6),('a',),PulseWallet(),round_number=1)
    check('Separate Renewal scheduled moments not global round banned',len(common.claimed),4)
    song=series('song-of-mending',roster=('a',));w=PulseWallet(rc=1)
    song.resolve(0,ClockMarker(0,5),('a',),w,round_number=1)
    song.resolve(1,ClockMarker(6),('a',),w,round_number=2)
    check('Song second pulse consumes1RC withoutBA',(w.rc,w.bonus_action),(0,True))
    song=series('enhanced-song',roster=('a',));w=PulseWallet(rc=2)
    for i,at in enumerate(song.opens):song.resolve(i,at,('a',),w,round_number=i+1)
    check('EnhancedSong both laterpulses cost2RC',w.rc,0)
    meditation=series('transcendent-meditation',roster=('owner','a'))
    meditation.resolve(0,ClockMarker(0,5),('owner','a'),PulseWallet(),round_number=1)
    event=meditation.resolve(1,ClockMarker(6),('owner','a'),PulseWallet(),round_number=2)
    check('Meditation independentKi even when callerblocksallHP',event['independentKi'],1)
    meditation=series('transcendent-meditation',roster=('owner',))
    meditation.resolve(0,ClockMarker(0,5),('owner',),PulseWallet(),round_number=1)
    event=meditation.resolve(1,ClockMarker(6),('owner',),PulseWallet(),round_number=2,whole_effect_suppressed=True)
    check('EntireMeditation suppressed losesHPoutputsandKi',(event['outputTargets'],event['independentKi']),((),0))
    wound=series('wound-eater-iv',roster=('e',));w=PulseWallet(rc=2)
    rejects('WoundEater no activation drain',lambda:wound.resolve(0,ClockMarker(0,5),('e',),w,round_number=1))
    for i,at in enumerate(wound.opens):event=wound.resolve(i,at,('e',),w,round_number=i+2)
    check('Delayedthirdpulse resolves BEFOREsequenceends',(wound.states,w.rc,wound.ended_at),(['committed']*3,0,ClockMarker(18)))
    hemo=series('hemostasis',roster=('a',))
    for i,at in enumerate(hemo.opens):hemo.resolve(i,at,('a',),PulseWallet(),round_number=i+2)
    check('Hemostasis includes exactlythirdtargetstart',hemo.states,['committed']*3)
    hemo=series('hemostasis',roster=('a',))
    hemo.advance(ClockMarker(7))
    check('Lateobservation missesfirsttick withoutcatchup',hemo.states,['lost','pending','pending'])
    hemo.resolve(1,ClockMarker(12),('a',),PulseWallet(),round_number=3)
    check('Later prepaidtickstillresolves',hemo.states[1],'committed')
    g=series('garden',roster=('a','owner'));w=PulseWallet(rc=2)
    event=g.target_start('a',ClockMarker(3),round_number=1)
    check('Activation-funded Garden window permitsone targetstart',event['outputTargets'],('a',))
    check('Samewindow replay blocked',g.target_start('a',ClockMarker(3),round_number=1),None)
    g.fund(1,ClockMarker(6),w)
    check('Newwindow cannot bypass numberedround',g.target_start('a',ClockMarker(6,1),round_number=1),None)
    g.fund(2,ClockMarker(12),w)
    check('Newround eligible Garden pulse',g.target_start('a',ClockMarker(15),round_number=3)['outputTargets'],('a',))
    check('Garden pays perwindow notperrecipient',w.rc,0)
    check('Garden expires beforeownerthirdfuturestart',g.target_start('owner',ClockMarker(18),round_number=4),None)
    g=series('garden',roster=('a',));g.advance(ClockMarker(7))
    check('Missedfunding ends atoriginalduemarker',g.ended_at,ClockMarker(6))
    g=series('garden',roster=('a',))
    rejects('Unpayableduewindowrejects',lambda:g.fund(1,ClockMarker(6),PulseWallet()))
    check('Unpayableduewindowends immediately',g.ended_at,ClockMarker(6))
    crown=series('crown-restored',roster=('owner',))
    got=[]
    for n in (1,2,3):
        if crown.target_start('owner',ClockMarker(6*n),round_number=n+1):got.append(n)
    check('CrownselfBAcast can onlyreceive2 beforeexpiry',got,[1,2])
    crown=series('crown-restored',roster=('a',))
    rejects('Crowncannotaddunselectedentrants',lambda:crown.target_start('new',ClockMarker(3),round_number=1))
    check('Extra targetturn creates no pulse',crown.target_start('a',ClockMarker(3),round_number=1,regular=False),None)
    crown.target_start('a',ClockMarker(3),round_number=1,whole_effect_suppressed=True)
    check('Suppressed occurrence cannotcatchup',crown.target_start('a',ClockMarker(4),round_number=1),None)
    reserve=BloomReserve({'a':10,'b':1})
    check('Bloom remainder toearlierinstallments',reserve.shares,{'a':(4,3,3),'b':(1,0,0)})
    check('Bloom first declaredreserve',reserve.consume(0,eligible_targets=('a','b')),{'a':4,'b':1})
    check('Outside target loses middleinstallment',reserve.consume(1,eligible_targets=()),{})
    check('Reentry gets thirdonly, no accumulatedmissing',reserve.consume(2,eligible_targets=('a',)),{'a':3})
    rejects('Bloom installment cannotreplay',lambda:reserve.consume(2,eligible_targets=('a',)))
    rejects('Bloom cannotnewroster',lambda:BloomReserve({'a':10}).consume(0,eligible_targets=('new',)))
    contacts=FirstContactLedger({'g':'garden','s':'resonant-seed','eg':'enhanced-garden'})
    check('Gardenentrycure independent ofHP',contacts.claim('g','a',event='entry'),True)
    check('Gardenlaterpulse cannotdoublecure',contacts.claim('g','a',event='pulse'),False)
    check('Seedentry is notfirstpulse',contacts.claim('s','a',event='entry'),False)
    check('Seedfirstpulse cure evenHPblocked',contacts.claim('s','a',event='pulse'),True)
    check('EnhancedGardenexplicitfirstpulsetiming',contacts.claim('eg','a',event='entry'),False)
    nano=series('nano-aegis');w=PulseWallet(rp=4)
    check('Nano noinitialheal',nano.states,['pending']*3)
    nano.advance(ClockMarker(6))
    check('SkippingNano commanddoesnotend',nano.ended_at,None)
    for i in (1,2,3):
        w.bonus_action=True;nano.command(ClockMarker(6,i),'a',w,option='heal')
    check('Nano printedcap independent ofcallercommandceiling',w.rp,1)
    rejects('Nano4thpulseprohibited',lambda:nano.command(ClockMarker(12),'a',w,option='heal'))
    nano=series('nano-aegis');w=PulseWallet(rp=2,bonus_action=False)
    rejects('ExtraActionalone cannotpayrequiredBA',lambda:nano.command(ClockMarker(6),'a',w,option='temporary-hp'))
    check('RejectedNano command noRPcharged',w.rp,2)
    nano=series('nano-aegis',expires=ClockMarker(60));w=PulseWallet(rp=4)
    for i in (1,2,3):
        w.bonus_action=True;nano.command(ClockMarker(i*12),'a',w,option='heal')
    rejects('Overdrivecannotcreate4thhealingpulse',lambda:nano.command(ClockMarker(48),'a',w,option='heal'))
    native=NativeOccurrenceLedger();w=PulseWallet(rp=10)
    for i in range(5):native.commit('aura-of-grace','cleric',ClockMarker(6*i),w)
    check('Nativefivepaidregularpulses',(len(native.consumed),w.rp),(5,5))
    check('Nativereplaynofee',native.commit('aura-of-grace','cleric',ClockMarker(24),w),False)
    check('Nativeextraturnnofee',native.commit('aura-of-grace','cleric',ClockMarker(25),w,regular=False),False)
    rejects('Unknownsourceprofile',lambda:PulseSeries('x','invented',ClockMarker(0),(),RecipientLedger()))
    shifted=PulseSeries('phase','song-of-mending',ClockMarker(2),(ClockMarker(6),ClockMarker(12)),RecipientLedger(),('a',))
    shifted.resolve(0,ClockMarker(2),('a',),PulseWallet(rc=1),round_number=1)
    check('Existingvirtualphase retainsnext6 notactivationplus6',shifted.opens[1],ClockMarker(6))
    early=series('song-of-mending',roster=('a',),expires=ClockMarker(4))
    early.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    early.advance(ClockMarker(20))
    check('Actual earlierexpiry notoverwrittenbylatermissedupkeep',early.ended_at,ClockMarker(4))
    unpaid=series('lifewell',roster=('a',));w=PulseWallet(rp=0)
    rejects('UnpayableBApulse chargesnoaction',lambda:unpaid.resolve(0,ClockMarker(0,10),('a',),w,round_number=1))
    check('UnpayableBApulse remainsunspent untildeadline',(w.bonus_action,unpaid.states[0]),(True,'pending'))
    check('Echoonly active anchor yieldssourcebase1',renewal_branch_bases(parent_active=False,parent_covers=True,echo_active=True,echo_covers=True),{'echo':1})
    check('Overlap suppliesalternativebases neveradds',renewal_branch_bases(parent_active=True,parent_covers=True,echo_active=True,echo_covers=True),{'parent':2,'echo':1})
    renewal=series('renewal')
    rejects('ParentplusEcho do notcreate6targetbudget',lambda:renewal.resolve(0,ClockMarker(0,5),('a','b','c','d'),PulseWallet(),round_number=1))
    check('Rejectedexcessrecipientsdoesnotconsumepulse',renewal.states[0],'pending')
    chorus=series('unfinished-chorus',roster=('enemy','ally'));w=PulseWallet(rc=1)
    chorus.resolve(0,ClockMarker(0,5),('enemy','ally'),w,round_number=1)
    chorus.resolve(1,ClockMarker(6,10),('enemy','ally'),w,round_number=2)
    check('Choruslaterownturnpulse1RC no inventedBA',(w.rc,w.bonus_action),(0,True))
    states=0
    for reserve_value in range(301):
        parts=installments(reserve_value)
        assert len(parts)==3 and sum(parts)==reserve_value and max(parts)-min(parts)<=1 and tuple(sorted(parts,reverse=True))==parts
        states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW','checkCount':len(checks),'reservePartitionStates':states,
            'scope':'Bounded source/target pulse clocks, resource/action commitments, fixed/repicked targets, named/instance round budgets, reserves and contact entitlements. Caller owns actual target eligibility, subgroup caps, canonical action economy, anchor/device lifecycle and healing outputs.','checks':checks}
    (ROOT/'docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS{len(checks)} pulse checks;{states} reserve partition states. Exact review pending.')
if __name__=='__main__':main()


## docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json

{
  "status": "PASS",
  "reviewStatus": "IN_REVIEW",
  "checkCount": 71,
  "reservePartitionStates": 301,
  "scope": "Bounded source/target pulse clocks, resource/action commitments, fixed/repicked targets, named/instance round budgets, reserves and contact entitlements. Caller owns actual target eligibility, subgroup caps, canonical action economy, anchor/device lifecycle and healing outputs.",
  "checks": [
    {
      "name": "Initial Briar included without BA/additionalRP",
      "result": "PASS"
    },
    {
      "name": "Later Briar repicks before outcomes and pays BA1RP",
      "result": "PASS"
    },
    {
      "name": "Cannot replay paid pulse",
      "result": "PASS"
    },
    {
      "name": "Replay never charges again",
      "result": "PASS"
    },
    {
      "name": "Missed upkeep ends at due turn end",
      "result": "PASS"
    },
    {
      "name": "Cannot resume missed upkeep",
      "result": "PASS"
    },
    {
      "name": "Lifewell first pulse already costs BA1RP",
      "result": "PASS"
    },
    {
      "name": "Lifewell cannot replace fixed target",
      "result": "PASS"
    },
    {
      "name": "No Lifewell first BA ends at activation turn end",
      "result": "PASS"
    },
    {
      "name": "Empty legal DarkSacrament pulse maintains with BA1RP",
      "result": "PASS"
    },
    {
      "name": "Full/Decay outcomes cannot refund committed Field",
      "result": "PASS"
    },
    {
      "name": "Extended Renewal fourth requires total3upkeepRP",
      "result": "PASS"
    },
    {
      "name": "Extended Renewal never fifth",
      "result": "PASS"
    },
    {
      "name": "Extended Renewal expires startturn5",
      "result": "PASS"
    },
    {
      "name": "Circle named cap crosses owner instances",
      "result": "PASS"
    },
    {
      "name": "Other legal Circle target still available",
      "result": "PASS"
    },
    {
      "name": "Independent Field instances may each affect same target",
      "result": "PASS"
    },
    {
      "name": "Separate Renewal scheduled moments not global round banned",
      "result": "PASS"
    },
    {
      "name": "Song second pulse consumes1RC withoutBA",
      "result": "PASS"
    },
    {
      "name": "EnhancedSong both laterpulses cost2RC",
      "result": "PASS"
    },
    {
      "name": "Meditation independentKi even when callerblocksallHP",
      "result": "PASS"
    },
    {
      "name": "EntireMeditation suppressed losesHPoutputsandKi",
      "result": "PASS"
    },
    {
      "name": "WoundEater no activation drain",
      "result": "PASS"
    },
    {
      "name": "Delayedthirdpulse resolves BEFOREsequenceends",
      "result": "PASS"
    },
    {
      "name": "Hemostasis includes exactlythirdtargetstart",
      "result": "PASS"
    },
    {
      "name": "Lateobservation missesfirsttick withoutcatchup",
      "result": "PASS"
    },
    {
      "name": "Later prepaidtickstillresolves",
      "result": "PASS"
    },
    {
      "name": "Activation-funded Garden window permitsone targetstart",
      "result": "PASS"
    },
    {
      "name": "Samewindow replay blocked",
      "result": "PASS"
    },
    {
      "name": "Newwindow cannot bypass numberedround",
      "result": "PASS"
    },
    {
      "name": "Newround eligible Garden pulse",
      "result": "PASS"
    },
    {
      "name": "Garden pays perwindow notperrecipient",
      "result": "PASS"
    },
    {
      "name": "Garden expires beforeownerthirdfuturestart",
      "result": "PASS"
    },
    {
      "name": "Missedfunding ends atoriginalduemarker",
      "result": "PASS"
    },
    {
      "name": "Unpayableduewindowrejects",
      "result": "PASS"
    },
    {
      "name": "Unpayableduewindowends immediately",
      "result": "PASS"
    },
    {
      "name": "CrownselfBAcast can onlyreceive2 beforeexpiry",
      "result": "PASS"
    },
    {
      "name": "Crowncannotaddunselectedentrants",
      "result": "PASS"
    },
    {
      "name": "Extra targetturn creates no pulse",
      "result": "PASS"
    },
    {
      "name": "Suppressed occurrence cannotcatchup",
      "result": "PASS"
    },
    {
      "name": "Bloom remainder toearlierinstallments",
      "result": "PASS"
    },
    {
      "name": "Bloom first declaredreserve",
      "result": "PASS"
    },
    {
      "name": "Outside target loses middleinstallment",
      "result": "PASS"
    },
    {
      "name": "Reentry gets thirdonly, no accumulatedmissing",
      "result": "PASS"
    },
    {
      "name": "Bloom installment cannotreplay",
      "result": "PASS"
    },
    {
      "name": "Bloom cannotnewroster",
      "result": "PASS"
    },
    {
      "name": "Gardenentrycure independent ofHP",
      "result": "PASS"
    },
    {
      "name": "Gardenlaterpulse cannotdoublecure",
      "result": "PASS"
    },
    {
      "name": "Seedentry is notfirstpulse",
      "result": "PASS"
    },
    {
      "name": "Seedfirstpulse cure evenHPblocked",
      "result": "PASS"
    },
    {
      "name": "EnhancedGardenexplicitfirstpulsetiming",
      "result": "PASS"
    },
    {
      "name": "Nano noinitialheal",
      "result": "PASS"
    },
    {
      "name": "SkippingNano commanddoesnotend",
      "result": "PASS"
    },
    {
      "name": "Nano printedcap independent ofcallercommandceiling",
      "result": "PASS"
    },
    {
      "name": "Nano4thpulseprohibited",
      "result": "PASS"
    },
    {
      "name": "ExtraActionalone cannotpayrequiredBA",
      "result": "PASS"
    },
    {
      "name": "RejectedNano command noRPcharged",
      "result": "PASS"
    },
    {
      "name": "Overdrivecannotcreate4thhealingpulse",
      "result": "PASS"
    },
    {
      "name": "Nativefivepaidregularpulses",
      "result": "PASS"
    },
    {
      "name": "Nativereplaynofee",
      "result": "PASS"
    },
    {
      "name": "Nativeextraturnnofee",
      "result": "PASS"
    },
    {
      "name": "Unknownsourceprofile",
      "result": "PASS"
    },
    {
      "name": "Existingvirtualphase retainsnext6 notactivationplus6",
      "result": "PASS"
    },
    {
      "name": "Actual earlierexpiry notoverwrittenbylatermissedupkeep",
      "result": "PASS"
    },
    {
      "name": "UnpayableBApulse chargesnoaction",
      "result": "PASS"
    },
    {
      "name": "UnpayableBApulse remainsunspent untildeadline",
      "result": "PASS"
    },
    {
      "name": "Echoonly active anchor yieldssourcebase1",
      "result": "PASS"
    },
    {
      "name": "Overlap suppliesalternativebases neveradds",
      "result": "PASS"
    },
    {
      "name": "ParentplusEcho do notcreate6targetbudget",
      "result": "PASS"
    },
    {
      "name": "Rejectedexcessrecipientsdoesnotconsumepulse",
      "result": "PASS"
    },
    {
      "name": "Choruslaterownturnpulse1RC no inventedBA",
      "result": "PASS"
    }
  ]
}


## docs/mechanics/HEALING_PULSE_SOURCE_VALIDATION.json

{
  "status": "PASS",
  "exactRecords": 100,
  "scope": "100 exact class candidate passages, including guards and exclusions. Source integrity only, not complete game zone coverage.",
  "issues": []
}


## docs/mechanics/HEALING_PULSE_SUPPORT_VALIDATION.json

{
  "status": "PASS",
  "exactSupportingRecords": 6,
  "scope": "Exact supplemental source equality and hashes, including frozen full shared class guide hash.",
  "issues": []
}


## Complete100 source-role bindings

{
  "status": "IN_PROGRESS",
  "scope": "100 lexical healing/zone/turn candidates. Classify exclusions and already-reviewed interfaces separately; no broad class or zone completeness claim.",
  "bindings": [
    {
      "bindingId": "cleric.base.consecrated-ground",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.base.consecrated-ground",
      "sourceSha256": "f4b71531332377e2ca7b3ea4b4646e46df57b264d265473b30abfbc2f86bdb55",
      "sourceProcedure": {
        "name": "Consecrated Ground",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Passive",
        "frequency": "Always",
        "effect": "Consecrated Ground. Tags: rite, healing, passive. Whenever one of your healing Rites restores HP to a living creature standing in terrain created by your Consecrate feature, that creature regains S additional HP. Apply this once per creature per Rite pulse; it is flat healing and is not itself another healing trigger."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: +S once/creature/Rite pulse after actual restoration; not child heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.base.radiance.radiance",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.base.radiance.radiance",
      "sourceSha256": "35f3566de386bca746618537d03e3561d74b8a35e1633c073ddef7e77f507821",
      "sourceProcedure": {
        "name": "Radiance",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "Automatic only if Radiance was selected",
        "effect": "Invocation Path — Radiance. Tags: invocation, radiance, healing. Once on each of your turns when one of your Rites restores HP to at least one living creature, choose one creature healed by that Rite. It regains S additional HP and may immediately end either Frightened or Poisoned on itself."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Once/own turn after Rite actually restores HP.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.base.echoes.echoes",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.base.echoes.echoes",
      "sourceSha256": "66a5241b20fcfd81448ba872aa1cd3fd5b59cadb5eb540467e9f5bdaf14cb155",
      "sourceProcedure": {
        "name": "Echoes",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "One original target within 30 feet",
        "duration": "Until start of your next regular turn",
        "frequency": "At most one pending Echoes-path repeat",
        "effect": "Invocation Path — Echoes. Tags: invocation, echoes. Once on each of your turns after a Smite or Rite produces rolled immediate damage or healing, store one original target and that raw dice total. At the start of your next regular turn, if the target is legal, repeat floor(raw dice total/10), minimum 1 for a positive total, as the same damage or healing type. This repeat carries no conditions, resources or triggers."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI/COPY",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One delayed source-next-start numeric repeat; no triggers/resources.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.base.sacred-chant",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.base.sacred-chant",
      "sourceSha256": "4053fdc1a1a48cc3fdb2accfef3abad95e23fce696a30321c714a2934e4a66b2",
      "sourceProcedure": {
        "name": "Sacred Chant",
        "activation": "Action",
        "cost": "1 RP to start; 0 RP maintenance",
        "rangeAndTarget": "Self; audible 15-foot prayer aura",
        "duration": "Concentration, maximum 3 Cleric turns",
        "frequency": "At will while RP remains",
        "effect": "Sacred Chant. Tags: chant, sustained, conviction. Pulse on start and once when maintained on each later regular turn with a Bonus Action. Under the base feature, the third pulse generates 1 Conviction. Only a real encounter can generate Conviction this way. Maintenance itself does not otherwise heal, damage or grant Conviction."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X/MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Nonhealing sustained 3-pulse chant; start + later BA maintenance.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.arch.aura-of-faith",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.arch.aura-of-faith",
      "sourceSha256": "56acc5fb191e255889bc45374d73b2ba55798a82fe5b5ab193731ab3d57ad448",
      "sourceProcedure": {
        "name": "Aura of Faith",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Allies within 15 feet who can perceive you",
        "duration": "Passive while conscious",
        "frequency": "Always",
        "effect": "Aura of Faith. Tags: aura, bishop. Allies in the aura gain +1 on saving throws. Whenever your Rite restores HP to an ally in the aura, that ally also regains 1 additional HP. Multiple Aura of Faith bonuses do not stack."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: +1 after actual Rite HP restoration in aura.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.arch.divine-invocation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.arch.divine-invocation",
      "sourceSha256": "7dae262ad987193dc14e8ce21c6d45c5a2ad7d0f2008377d0217f5959e2848c2",
      "sourceProcedure": {
        "name": "Divine Invocation",
        "activation": "Action",
        "cost": "2 Conviction + 3 RP",
        "rangeAndTarget": "Mode-dependent; maximum 60 feet",
        "duration": "Instantaneous unless mode states otherwise",
        "frequency": "Recharge 3 rounds",
        "effect": "Divine Invocation. Tags: invocation, bishop. Use only your selected Invocation Path. Radiance: up to 3 allies within 30 feet each regain S d8+M HP; one may end Frightened or Poisoned. Judgment: one enemy within 60 feet makes a Wisdom save, taking (S+1)d8 radiant on failure or half on success; failure also applies Judged for 2 rounds. Renewal: up to 2 allies within 30 feet each regain S d8+M HP and 5 Stamina. Flame: creatures in a 15-foot cone make Dexterity saves, taking (S+1)d8 fire on failure or half on success; failed targets also take 1d6 fire at the start of their next turn. Veil: up to 3 allies within 30 feet can see invisible/ethereal creatures within 30 feet and gain advantage on saves against illusions for 3 rounds. Echoes: choose one eligible Smite or Rite you resolved this turn or previous regular turn and one original target within 30 feet; repeat 50% of its immediate unmodified rolled damage or healing dice, rounded down once, minimum 1 for a positive source, with no copied conditions, resources or triggers."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I/COPY",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Instant modes; Renewal/Radiance heal, Echoes numeric repeat; no sustained schedule.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.saint.aura-of-grace",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.saint.aura-of-grace",
      "sourceSha256": "7dff7e8271aba866c1b596528fe2e7d1e3f9a1558eeec233922585461bcc9854",
      "sourceProcedure": {
        "name": "Aura of Grace",
        "activation": "Triggered and passive",
        "cost": "1 RP per healing pulse",
        "rangeAndTarget": "Living allies within 15 feet",
        "duration": "Passive during real encounters",
        "frequency": "Healing once/own regular turn; critical reduction once/ally/round",
        "effect": "Aura of Grace. At the start of your regular turn during a real encounter, you may pay 1 RP to heal S HP to up to 3 living allies within 15 ft below half maximum HP. You must be conscious. Separately, once per ally per round when an ally in the aura suffers a critical hit, reduce its added critical damage by one damage die, minimum 0 extra dice. No unlimited free healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "NR",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Source regular-start; optional 1 RP; once/own regular turn, no 3-cap.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.priest.balanced-scales",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.priest.balanced-scales",
      "sourceSha256": "7e7adca22a150348e1afd85fcf4ca10e7c6a2395883b66b2d889b097f8200b98",
      "sourceProcedure": {
        "name": "Balanced Scales",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Living creatures healed by your Cleric features",
        "duration": "Until start of your next regular turn",
        "frequency": "At most once per marked ally per round",
        "effect": "Balanced Scales. Tags: priest, healing, retaliation. After you restore HP to a living ally, mark it until the start of your next regular turn. The first enemy to damage that ally during the mark takes S + M radiant damage. The retaliation is not an attack, cannot critically hit and cannot recursively trigger another Balanced Scales event."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Actual-gain mark; no healing pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.priest.word-of-power",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.priest.word-of-power",
      "sourceSha256": "b238551c3ab4549273d2ad295301aba312d27d3cc75f8768e800cc67fb23c175",
      "sourceProcedure": {
        "name": "Word of Power",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "One creature within 30 feet",
        "duration": "Instantaneous",
        "frequency": "Recharge 2 rounds",
        "effect": "Word of Power. Tags: priest, divine. Choose one mode. Mercy: one willing living creature regains S d8+M HP. Rebuke: one Undead or Fiend makes a Constitution save, taking (S+1)d8 radiant on failure or half on success; failure also removes its Reaction until the start of its next turn. Command: one other hostile creature makes a Wisdom save; failure knocks it Prone and removes its Reaction until the start of its next turn. No mode changes beliefs, loyalty or ideology."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Mercy single heal only.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.priest.cosmic-equilibrium",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.priest.cosmic-equilibrium",
      "sourceSha256": "511b9a9abd80cc33649c3a30d73c03139189a2443a25ae92b7905fbdb0251787",
      "sourceProcedure": {
        "name": "Cosmic Equilibrium",
        "activation": "Action",
        "cost": "7 RP",
        "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
        "duration": "Concentration, maximum 3 rounds",
        "frequency": "1/short rest",
        "effect": "Cosmic Equilibrium. Tags: priest, zone, healing, radiant. Once per round, when a living ally in the zone receives healing beyond its missing HP, redirect up to S+M of that excess as radiant damage to one enemy in the zone. Separately, once per round when an enemy in the zone takes radiant damage from one of your Cleric features, one ally in the zone regains up to S+M HP, not exceeding half the actual radiant damage dealt. These two conversions cannot trigger each other."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH/G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Trigger conversions once/round; no autonomous pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.sanguine-rite",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.sanguine-rite",
      "sourceSha256": "b043e78dd641a9e31b86b49c238105f2b4ee4138c21f4e2ae9e194fee44169f9",
      "sourceProcedure": {
        "name": "Sanguine Rite",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self and one ally within 30 feet",
        "duration": "Instantaneous",
        "frequency": "At most once on each of your turns",
        "effect": "Sanguine Rite. Tags: cultist, rite, healing. When one of your Rites deals damage to at least one enemy, choose one living ally within 30 feet. That ally regains HP equal to half the actual damage dealt to one chosen damaged enemy, rounded down, maximum S+M HP. This healing cannot trigger Sanguine Rite again."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Once/own turn damage-derived finite heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.blasphemous-tongue",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.blasphemous-tongue",
      "sourceSha256": "793dec5aa60dff80f8da02ed52a55b22c28c0b8975ca949d9dc9bf4374e6f1c6",
      "sourceProcedure": {
        "name": "Blasphemous Tongue",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Enemies affected by your Sacrament",
        "duration": "Until the next Sacrament pulse or effect end",
        "frequency": "Once per target per pulse",
        "effect": "Blasphemous Tongue. Tags: cultist, sacrament, doomed. At each pulse of your Sacrament, each enemy affected by that pulse makes a Wisdom save. On failure it becomes Doomed until the next pulse. While Doomed, HP healing it receives is reduced by S+M, minimum 0, and each positive timed buff on it counts down one additional round at the end of its turn. Repeated failures refresh rather than stack."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Healing reduction applied by Sacrament pulses.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.zealot-s-touch",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.zealot-s-touch",
      "sourceSha256": "d419c667240c84d69d12a5f639b9466ef00ed47af9eb2a0eea3e9c3d924649e6",
      "sourceProcedure": {
        "name": "Zealot's Touch",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Healing-over-time Rites you control",
        "duration": "Passive",
        "frequency": "Always",
        "effect": "Zealot's Touch. Tags: cultist, rite, necrotic. When starting a Rite whose printed pulse would restore HP over multiple turns, you may designate a hostile creature instead of a healing recipient. At each applicable pulse that enemy makes a Wisdom save. On failure it takes necrotic damage equal to the Rite's rolled healing dice; on success it takes half. Flat healing bonuses are not converted. The enemy receives no healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Converts qualifying HoT pulse dice to damage; inherits source pulse cadence.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.dark-sacrament",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.dark-sacrament",
      "sourceSha256": "86c14c628a3b9ee335e2c7316844416ed1cd61e83f60f83d5af04d2e216071f4",
      "sourceProcedure": {
        "name": "Dark Sacrament",
        "activation": "Action",
        "cost": "3 Conviction + 5 RP to start; 1 RP maintenance",
        "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
        "duration": "Concentration, maximum 3 Cleric turns",
        "frequency": "Recharge 4 rounds",
        "effect": "Dark Sacrament. Tags: cultist, sacrament, rite, sustained, zone. On start and each paid maintenance pulse, roll S d6 once. Up to three enemies in the zone make Constitution saves, taking that roll as necrotic damage on failure or half on success. If at least one enemy takes damage, up to three living allies in the zone each regain floor(roll/2)+M HP. Maximum 3 pulses. The Conviction expenditure can vent Dissonance once."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start pulse included; later 1 RP maintenance; max3. Maintenance action unspecified here.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "cleric.hero.cultist.zealot-s-fervor",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/cleric.json",
      "sourceId": "cleric.hero.cultist.zealot-s-fervor",
      "sourceSha256": "c54199ee73ebfbe5c2c47cd5771fc43fd4f7609dfef775292d0798b409d44e4f",
      "sourceProcedure": {
        "name": "Zealot's Fervor",
        "activation": "Bonus Action",
        "cost": "2 Conviction",
        "rangeAndTarget": "Self",
        "duration": "3 rounds",
        "frequency": "1/short rest",
        "effect": "Zealot's Fervor. Tags: cultist, stance. For 3 rounds, once on each of your turns add S to one damage roll from a Cleric feature and S to one HP-healing roll from a Cleric feature. While the Fervor lasts, your AC is reduced by 1. The Conviction expenditure is not a Rite or Invocation and therefore does not vent Dissonance by itself."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: +S to one healing roll/own turn for 3 rounds.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "crimson-agent.engine[2]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": 2,
      "sourceSha256": "44a38acbffca3c994c2444d9f9183f7d8013ddda451f37182a4c2c25150755ea",
      "sourceProcedure": {
        "text": "Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Bleed/healing-version distinction; no healing scheduler.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "crimson-agent.hero.bloodweaver.hemostasis",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": "crimson-agent.hero.bloodweaver.hemostasis",
      "sourceSha256": "fd035eba7d0e2ed5547d745a6e3e52207bfa499b87cd0c693f1f00bb932b87f0",
      "sourceProcedure": {
        "name": "Hemostasis",
        "activation": "Passive",
        "cost": "1 additional RP per application",
        "rangeAndTarget": "One willing living ally in range of your Bleed application",
        "duration": "3 target turns",
        "frequency": "Once/own turn",
        "effect": "You may replace a new Bleed application on that ally with healing 1d4 at start of its next 3 turns. Pay extra RP even if original application was free. One such healing effect per target; it cannot spread, detonate, generate BG or trigger healing loops."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Prepaid 1d4 at target-next 3 regular starts; no upkeep.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "crimson-agent.hero.bloodweaver.lifewell",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/crimson-agent.json",
      "sourceId": "crimson-agent.hero.bloodweaver.lifewell",
      "sourceSha256": "df6aec7b14a71408fb30b0e66b2051a09d3570829b228e4e04c55b7cb0ae2568",
      "sourceProcedure": {
        "name": "Lifewell",
        "activation": "Action",
        "cost": "4 RP; all BG, minimum 3",
        "rangeAndTarget": "Up to 3 living allies within 15 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "1/long rest",
        "effect": "Spend K BG. At start and on each of your next 2 turns, use Bonus Action and pay 1 RP to pulse healing: each chosen ally still within 15 ft regains 1d8+K HP. Without maintenance it ends at turn end. Total 3 pulses; no triggers create more BG."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: First same-turn BA+1RP; next2 BA+1RP; fixed targets; missed maintenance ends.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "dragoon.engine[4]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/dragoon.json",
      "sourceId": 4,
      "sourceSha256": "250848ddbb6f7e2f67c7ae07765b704f2c2dfcee59e1acb21e1b1c32c622a8cd",
      "sourceProcedure": {
        "text": "Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Burn/Bleed periodic damage only.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "druid.engine[4]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/druid.json",
      "sourceId": 4,
      "sourceSha256": "7befb5eef095e247cb6cab325a66a0e3b84d24b9ea7771ba28fa9a13c2afa976",
      "sourceProcedure": {
        "text": "Transformation reserves prevent unlimited replacement HP: at long rest record Buffer Reserve=2 L+M and Form Surge Reserve=PB. A form giving temporary HP draws that many from Buffer Reserve, up to remaining amount, with normal nonstacking; never real healing. A form special described once/transformation also spends 1 Form Surge and cannot be refreshed by resuming the form. Form Surge refills only long rest. Forms cannot grant free casts, RP or shift uses. Auras affect at most 3 enemies and once per enemy per round; retaliation once/round total; ongoing riders refresh, never stack. Entering a legal Shapeshift clears the Refrain counter and remembered repeated-spell name, as the protected source contract requires. It does not reduce accumulated Dissonance. Natural attacks do not clear Refrain."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X/G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Temp-HP reserve and aura guards; not real recurring healing.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "mirrorsage.hero.mirror-mage.reality-fracture",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mirrorsage.json",
      "sourceId": "mirrorsage.hero.mirror-mage.reality-fracture",
      "sourceSha256": "01db39e48e6febb6fea905259253d2c146292352ba0876f75fc6101b79c195cd",
      "sourceProcedure": {
        "name": "Reality Fracture",
        "activation": "Action",
        "cost": "6 RP; 1 long-rest use",
        "rangeAndTarget": "Fixed 10 ft-radius zone within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "1/long rest",
        "effect": "While you stand inside, once/turn add 1d6 to one Echo damage/healing amount or impose-1 on one target's Echo save. Choose before resolving. No free releases, random recasts, resource refunds or extra targets."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Once/turn optional +1d6 to existing Echo heal; no pulse creation.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "mirrorsage.hero.shattered-one.fractured-dominion",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/mirrorsage.json",
      "sourceId": "mirrorsage.hero.shattered-one.fractured-dominion",
      "sourceSha256": "7eb5063a016220234c5eca407a3ccd2eb580379e56ac90b5fb8dc4ade2315150",
      "sourceProcedure": {
        "name": "Fractured Dominion",
        "activation": "Bonus Action",
        "cost": "8 RP; 1 long-rest use",
        "rangeAndTarget": "Self",
        "duration": "2 of your turns",
        "frequency": "1/long rest",
        "effect": "Your first damage release on each of these 2 turns adds one half-dice component against a DIFFERENT enemy within 10 ft of an original target. Same package and shared copy cap; excludes healing/control. Never recursively copies a copy or adds a release action."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Damage copy only; healing excluded.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "monk.base.crane-stance-support",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.base.crane-stance-support",
      "sourceSha256": "e674e9a4ae8aa0f0d52cd371b86e9173b9ba7f00a2447db64e31c14f44b42314",
      "sourceProcedure": {
        "name": "Crane Stance (Support)",
        "activation": "Passive",
        "cost": "0 for stance; healing costs 1 Ki and 1 RP",
        "rangeAndTarget": "Self; one ally within 15 feet for healing rider",
        "duration": "While active",
        "frequency": "Automatic core stance",
        "effect": "Crane Stance. Tags: stance, support. While unarmored, whenever you move at least 15 feet on your turn, gain +1 AC until the start of your next turn. HP healing you receive from another creature gains +S HP once per round. When you begin an unarmed strike at exactly 5 Ki and hit, spend 1 Ki and 1 RP; you and one living ally within 15 feet each regain S+M HP, at most once per turn."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD/TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Incoming-heal +S once/round; paid hit rider heal once/turn.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "monk.hero.enlightened-master.breath-of-the-thousand-petals",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.enlightened-master.breath-of-the-thousand-petals",
      "sourceSha256": "ef8e3a96a396ed3d48f95c0e4138b0eae186fe297b746cae0c83c40004fa508e",
      "sourceProcedure": {
        "name": "Breath of the Thousand Petals",
        "activation": "Action",
        "cost": "5 Ki + 5 RP",
        "rangeAndTarget": "Up to six allies within 20 feet",
        "duration": "Until start of your next regular turn",
        "frequency": "1/long rest; automatic Hero Final",
        "effect": "Final — Breath of the Thousand Petals. Tags: hero, enlightened, final, resurrection, weave. Living or Downed allies in range regain 3 S d8+M HP. Up to two allied creatures that died since the end of your previous regular turn return to life at 1 HP if their bodies can sustain life. Until the start of your next turn, affected living allies cannot be reduced below 1 HP by damage, though instant-death effects still function. It removes no Wounds and cannot revive the same creature twice."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One Final heal/resurrection event; no recurring pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "monk.hero.enlightened-master.circle-of-harmony",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.enlightened-master.circle-of-harmony",
      "sourceSha256": "df3b3c65b152fd7b3a217eac2e551b3fc473a00b9704fcbb98bfe0dc9611c4bd",
      "sourceProcedure": {
        "name": "Circle of Harmony",
        "activation": "Action",
        "cost": "2 Ki + 3 RP to start; 1 RP maintenance",
        "rangeAndTarget": "10-foot-radius fixed zone centered within 30 feet",
        "duration": "Concentration, maximum 3 Monk turns",
        "frequency": "Recharge 4 rounds",
        "effect": "Circle of Harmony. Tags: hero, enlightened, healing, zone, weave, sustained. On start and each paid Bonus Action maintenance pulse, up to three living allies in the zone regain S d6+M HP. Maximum 3 pulses. A creature receives this named effect at most once per round. It removes no Wounds and cannot restore the dead."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start included; later BA+1RP; max3; repick≤3/pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "monk.hero.enlightened-master.transcendent-meditation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/monk.json",
      "sourceId": "monk.hero.enlightened-master.transcendent-meditation",
      "sourceSha256": "ef26fc5933a98d0d06c511e4ecddeda4ea9dab8ee064bc4f2eec65d028589803",
      "sourceProcedure": {
        "name": "Transcendent Meditation",
        "activation": "Action",
        "cost": "3 Ki + 4 RP",
        "rangeAndTarget": "Self and up to three allies within 15 feet",
        "duration": "Concentration, maximum 3 Monk turns",
        "frequency": "1/short rest",
        "effect": "Transcendent Meditation. Tags: hero, enlightened, healing, weave, sustained. On start and at the start of each of your next two regular turns while concentration holds, each target regains S d6 HP. You regain 1 Ki on the second pulse only, never above 5. Targets must remain within 15 feet. This finite healing cannot be restarted until the short-rest use refreshes."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start + next2 source regular-start automatic pulses; fixed targets; concentration.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.engine[26]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": 26,
      "sourceSha256": "dd6003b655e77deb78cbdc17b83837c51b1f4798eb77d546cbd9b865cdf725b2",
      "sourceProcedure": {
        "text": "Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G/TW",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Generic Oracle persistent-zone schedule: fixed sets, concentration, ≤3 funded windows.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.spiral-touched.spiral-touched-boon-iii",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.spiral-touched.spiral-touched-boon-iii",
      "sourceSha256": "a6358be2e17db52d461c11e2df79d972481dba2c95ebd29ecd7c31a02987d377",
      "sourceProcedure": {
        "name": "Spiral-Touched — Boon III",
        "activation": "Triggered at 0 HP",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Until start of next regular turn",
        "frequency": "1/long rest",
        "effect": "1/long rest when damage would reduce you to 0 HP without killing you outright, instead regain floor(max HP/4), minimum 1, and phase out until the start of your next regular turn; while phased you cannot be targeted, affect other creatures or activate Revelations."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One direct recovery; not pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.wound-eater.wound-eater-boon-iv",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.wound-eater.wound-eater-boon-iv",
      "sourceSha256": "9028f42b10e75ba44b130f18695a0ef9411d99df43b4929f1b89d1e4ead2d127",
      "sourceProcedure": {
        "name": "Wound Eater — Boon IV",
        "activation": "Bonus Action; start-of-turn pulses",
        "cost": "2 RC start; 1 RC per later pulse",
        "rangeAndTarget": "Up to three living enemies within 10 feet",
        "duration": "Concentration; at most three pulses",
        "frequency": "One aura; once/target/round",
        "effect": "pay 2 RC as a Bonus Action to activate a 10-foot drain aura, requiring concentration for at most three pulses; pay 1 RC before each pulse after the first or end it. You may suppress it freely. During a real encounter, at the start of your turn up to three meaningful living enemies in the aura takes S necrotic damage; regain HP equal to the total actually dealt, capped at S+M per turn."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: First drain next source start; two later 1RC source-start pulses.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.burning-blood.burning-blood-boon-v",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.burning-blood.burning-blood-boon-v",
      "sourceSha256": "2632f2e1356764183fce28146213368f6ddea68646318394a679610edc8c2d83",
      "sourceProcedure": {
        "name": "Burning Blood — Boon V",
        "activation": "Bonus Action",
        "cost": "0",
        "rangeAndTarget": "Self; up to three enemies/allies within 15 feet",
        "duration": "Three rounds",
        "frequency": "1/long rest; one pulse/target/round",
        "effect": "1/long rest as a Bonus Action become a living pyre for 3 rounds. At the start of each hostile creature's turn within 15 feet it takes S d6 fire damage. Once per your turn when at least one enemy takes fire damage from you, regain 1d6 HP, capped at S+M HP per turn. Allies in the aura gain fire resistance and hidden/invisible creatures within 10 feet cannot benefit from mundane darkness or visual concealment against creatures illuminated by your pyre."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TW/TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Target-start damaging aura + once/own-turn heal trigger; engine26 applies unless later source marks Final exception.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.consumed.consumed-boon-v",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.consumed.consumed-boon-v",
      "sourceSha256": "50d2ca5f682a506377c7b843b7ce6a077296b98aa74cd95085384509ac42ccd0",
      "sourceProcedure": {
        "name": "Consumed — Boon V",
        "activation": "Bonus Action",
        "cost": "0",
        "rangeAndTarget": "Self and up to three allies within 10 feet",
        "duration": "Three rounds",
        "frequency": "1/long rest",
        "effect": "1/long rest as a Bonus Action fully embody your Mystery for 3 rounds. Gain immunity to the theme damage type, +2 on Revelation attack rolls and Revelation save DC, and add S to one Revelation damage or healing roll each turn. Allies within 10 feet gain +1 AC. Visible transformation cannot be suppressed during this embodiment."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: +S to one Revelation heal/turn; no pulse itself.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.bones.rotting-touch",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.bones.rotting-touch",
      "sourceSha256": "2a184115c77c3e39626229f0d95c4b73218e849b6ccc078dd5ae170ccfdf3475",
      "sourceProcedure": {
        "name": "Rotting Touch",
        "activation": "Action",
        "cost": "2 RC",
        "rangeAndTarget": "One creature you can touch",
        "duration": "Maximum 3 rounds",
        "frequency": "At will while RC remains",
        "effect": "Make a Revelation attack. On hit the target makes a Constitution save. On failure it gains Decay for up to 3 rounds: attacks against it add S damage once per attacker per turn, it takes -1 on saving throws and cannot regain HP. At the end of each turn it repeats the save, ending Decay on success. Corpses within 2 tiles of a Decayed creature cannot be raised while Decay persists. If the target is undead, it also takes 2d6 necrotic damage on the initial hit and you regain half the actual damage dealt, capped at S+M HP. At most three allied hits per round receive the vulnerability rider; it is additional flat damage, not multiplication of an entire attack."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH/G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Initial undead damage-derived heal; Decay blocks healing; no healing pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.bones.unfinished-chorus",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.bones.unfinished-chorus",
      "sourceSha256": "d0c65305f314bb6bbb3b9245ec88c655a5d4b815b553e84d3cddcca489dfe535",
      "sourceProcedure": {
        "name": "Unfinished Chorus",
        "activation": "Action",
        "cost": "3 RC",
        "rangeAndTarget": "Enemies, controlled undead and corpses within 4 tiles",
        "duration": "2 rounds; Revelation backlash 1 round",
        "frequency": "At will while RC remains",
        "effect": "For 2 rounds, enemies within 4 tiles suffer Dread: -1 on attack rolls and saving throws. Once on each of your turns choose one living enemy in range; it takes 1d6 necrotic damage and you either regain half the actual damage dealt, rounded down, or one living ally within 3 tiles of you regains that amount, maximum S+M HP. Undead you control add S damage to one attack each turn and reduce first damage each round by 1. Corpses in the area cannot be raised while the Chorus lasts. Afterward you are suffering Revelation backlash until end of your next turn: -1 attacks/saves and Speed -5 feet. Choose up to three enemies and three allies. Enemies make Wisdom saves on entry and at the end of each turn, ending their debuff on success. The drain allows a Constitution save for half damage; healing is capped at S+M total per pulse. Concentration and pulse upkeep apply."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP/TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: First source-turn drain included; later engine26 upkeep; 2-round cadence, fixed candidate sets.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.flame.zealot-s-renewal",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.flame.zealot-s-renewal",
      "sourceSha256": "c5be3b9f61b1d449a60c73c0d7441db0451cec2ddf56b73113e480ccb08aaf91",
      "sourceProcedure": {
        "name": "Zealot's Renewal",
        "activation": "Action",
        "cost": "2 RC",
        "rangeAndTarget": "One living ally within 3 tiles; adjacent enemies",
        "duration": "Instantaneous; fire ward until start of your next turn",
        "frequency": "At will while RC remains",
        "effect": "The ally regains 2 S d8+M HP, then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it. It may end Poisoned or immediately repeat one disease save. Until the start of your next turn it reduces the first fire damage it takes by S. Hostile creatures adjacent to the healed ally take 1d4 fire damage once from scattering embers."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Single healing event + independent cure/backlash.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.flame.first-flame-convergence",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.flame.first-flame-convergence",
      "sourceSha256": "25282e2ec8de9b5017e44ff952f9082abcada88b6d5990dbb595d67b44540b76",
      "sourceProcedure": {
        "name": "First Flame Convergence",
        "activation": "Action",
        "cost": "3 RC",
        "rangeAndTarget": "Self and allies within 4 tiles",
        "duration": "2 rounds",
        "frequency": "At will while RC remains",
        "effect": "For 2 rounds, once on each of your turns when a Flame Revelation deals fire damage, add one extra die matching that Revelation's primary damage die to one damage roll. Once per turn when one of your Flame Revelations damages a meaningful hostile creature, one living ally within 4 tiles regains 1d6 HP. Allies within 4 tiles are immune to Frightened. Once per turn when this effect heals an ally, that ally reduces the first damage it takes before your next turn by 1. Zealot's Renewal deals no backlash while Convergence lasts."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Once/turn damage-triggered heal; no generic zone pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.flame.crown-restored",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.flame.crown-restored",
      "sourceSha256": "354e4fb2b53a1b46b121c1edc36df4e364f0dbf66931fa7bdb453e68d6f3ab8f",
      "sourceProcedure": {
        "name": "Crown Restored",
        "activation": "Bonus Action",
        "cost": "0 RC",
        "rangeAndTarget": "Self and allies within 5 tiles",
        "duration": "3 rounds",
        "frequency": "1/long rest",
        "effect": "Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI/TW",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Limited Final target-start pulses, max3/creature; no generic upkeep.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.resonant-seed",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.resonant-seed",
      "sourceSha256": "ee79b90bfc9c7117d99edebc2dc66e6b79b37bbc5f732ac6a2c4bedabab152ab",
      "sourceProcedure": {
        "name": "Resonant Seed",
        "activation": "Action",
        "cost": "1 RC",
        "rangeAndTarget": "2-tile-radius fixed zone centered within 4 tiles",
        "duration": "3 rounds",
        "frequency": "At will while RC remains; one Seed zone at a time",
        "effect": "When a living ally starts its turn in the zone, it regains 1d4 HP, at most once per round and for at most three pulses from this use, and may end Frightened or Poisoned on the first pulse it receives. Undead entering or starting their turn in the zone take 1d4 radiant damage once per round and make a Strength save; on failure their Speed is reduced by 1 tile until the end of that turn. Healing requires the paid 1 RC activation and ends after 3 rounds."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TW",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Activation-funded window1; later engine26 1RC windows2/3; fixed Oracle set.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.garden-of-restoration",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.garden-of-restoration",
      "sourceSha256": "faaa0f647c20d847d84790b2a353bb9e9fcf3946f210c911e003d08474a7de93",
      "sourceProcedure": {
        "name": "Garden of Restoration",
        "activation": "Action",
        "cost": "2 RC",
        "rangeAndTarget": "4-tile-radius fixed zone centered within 5 tiles",
        "duration": "3 rounds",
        "frequency": "At will while RC remains; one Garden at a time",
        "effect": "At the start of each living ally's turn in the Garden, it regains 1d6 HP, maximum three pulses per creature from this use, and gains +1 HP the next time another finite healing effect restores HP before its next turn. The first time each ally enters or starts in a given Garden, it may end Poisoned or immediately repeat one disease save. Undead starting in the Garden take 1d6 radiant damage and make a Wisdom save; on failure they take -1 on attack rolls until the end of that turn."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TW",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Same funded-window model; first-contact cure independent of HP gain.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.verdant-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.verdant-pulse",
      "sourceSha256": "feb0f82538549fb2d540cfa9a68b89f517d4f1138b44ade546065fc7300c24f9",
      "sourceProcedure": {
        "name": "Verdant Pulse",
        "activation": "Passive and Reaction",
        "cost": "0 RC",
        "rangeAndTarget": "Allies you heal; emergency ally within 4 tiles",
        "duration": "Buff until end of ally's next turn; emergency instantaneous",
        "frequency": "Buff once per ally per short rest; emergency 1/encounter",
        "effect": "When one of your paid or finite Oracle effects restores HP to an ally who was below half maximum HP, that ally reduces the first damage it takes before the end of its next turn by S and adds 1 HP to one later finite healing effect during that period. Separately, once per encounter when a living ally within 4 tiles would be reduced to 0 HP without instant death, use your Reaction to leave it at 1 HP instead and end Frightened or Poisoned on it."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Triggered after actual finite HP restoration; emergency floor separate.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.song-of-mending",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.song-of-mending",
      "sourceSha256": "ca7500f38966fc943c0398ff2fbddfe96070ca9caf15a6d0b24cee7d2fa2def1",
      "sourceProcedure": {
        "name": "Song of Mending",
        "activation": "Action",
        "cost": "3 RC",
        "rangeAndTarget": "Living allies within 5 tiles",
        "duration": "2 rounds",
        "frequency": "At will while RC remains",
        "effect": "On activation and at the start of your next regular turn, each living ally still within 5 tiles regains 2d6 HP, for exactly two possible pulses per use. Once during the duration for each ally, when one damage event would reduce it below 1 HP without instant death, it remains at 1 HP instead. When this prevention triggers, that ally may end Frightened or Poisoned and gains +S HP the next time a separate finite healing effect restores HP before Song ends. This removes no Wounds and cannot resurrect."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Activation + next source regular-start; Enhanced adds second-later start; no target-start upkeep.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.life-revelation-mastery",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.life-revelation-mastery",
      "sourceSha256": "f231bdb47b3545daad32777e23dd58122092961abb95c826436a646ab5e62b44",
      "sourceProcedure": {
        "name": "Life Revelation Mastery",
        "activation": "Passive",
        "cost": "0 RC",
        "rangeAndTarget": "One eligible known Life Revelation",
        "duration": "Permanent",
        "frequency": "Choose one upgrade at Oracle 15",
        "effect": "Choose one mastery for a Revelation you know. Enhanced Overflowing Light: maximum temporary HP from excess healing becomes 20. Enhanced Garden of Restoration: the first Garden pulse a creature receives may end both Poisoned and one disease that explicitly allows magical curing, rather than only one of those benefits. Enhanced Song of Mending: duration becomes 3 rounds and gains one additional 2d6 healing pulse at the start of your second later regular turn; each ally still receives only one 1-HP death prevention per use."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Modifies Garden/Song; creates no pulse alone.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.life.eternal-bloom",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.life.eternal-bloom",
      "sourceSha256": "3d97cb828d42d1ec6f4f674e4328a37f916f47c15513a4e357cff80a706f7d02",
      "sourceProcedure": {
        "name": "Eternal Bloom",
        "activation": "Action",
        "cost": "0 RC",
        "rangeAndTarget": "5-tile-radius fixed sanctuary centered within 5 tiles",
        "duration": "3 rounds",
        "frequency": "1/long rest",
        "effect": "When Eternal Bloom appears, record each living ally's missing HP while it is inside the zone. Divide that recorded missing HP into three healing installments as evenly as possible, with any remainder assigned to earlier pulses. On activation and at the start of each of your next two regular turns, each qualifying ally still inside regains its next installment; later damage does not increase this reserve. Once per ally during the Bloom, when damage would reduce it to 0 HP without instant death, it remains at 1 HP instead. Allies in the zone have necrotic immunity for the 3 rounds. When the Bloom ends, petals create light obscurement in the zone until the start of your next turn. It removes no Wounds and does not resurrect."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Three fixed reserve installments; activation + next2 source starts; no upkeep.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.time.rewind-wound",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.time.rewind-wound",
      "sourceSha256": "eb01bdc7533669a80e0862bf3130c342b3b8c9c3f4199f8925953086e6bc898c",
      "sourceProcedure": {
        "name": "Rewind Wound",
        "activation": "Action",
        "cost": "2 RC",
        "rangeAndTarget": "One living ally you touch",
        "duration": "Healing instantaneous; protection until start of your next turn",
        "frequency": "At will while RC remains; same damage event can be rewound once",
        "effect": "Reference the most recent single damage event the target suffered since the start of its previous regular turn and restore HP equal to that event's actual HP damage, maximum Oracle level+M. If that exact event directly imposed one condition with a finite duration, remove that condition if it is still present and is not a Wound, curse, death state or permanent transformation. The ally reduces the first damage it takes before your next turn by 1 and gains +2 initiative for the current round. If the recorded damage had reduced it below half maximum HP, regain 1 RC after resolution, at most once per round. Rewind does not undo attacks, spent resources, movement, deaths of other creatures or proc effects."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One historical-damage heal; no recurring pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "oracle.supplement.time.the-spiral-opens",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/oracle.json",
      "sourceId": "oracle.supplement.time.the-spiral-opens",
      "sourceSha256": "b15b7a477b14185e1510967e1d24c7e46a856a400ef1575f876d2adbaa39ee28",
      "sourceProcedure": {
        "name": "The Spiral Opens",
        "activation": "Action",
        "cost": "0 RC",
        "rangeAndTarget": "Self; one known beneficial Time Revelation or one enemy within 5 tiles",
        "duration": "3 rounds",
        "frequency": "1/long rest",
        "effect": "For 3 rounds, at the start of each of your regular turns choose ONE temporal option, each usable at most once during this Final. ECHO REVELATION: repeat only the immediate numeric damage, healing, movement or buff component of one beneficial Time Revelation you personally resolved during the previous round, paying 0 RC; this copy is not a new Revelation cast, copies no resource restoration, action grant, hard control, condition trigger, Prophecy Trigger or proc. FORCED ECHO: choose one non-player enemy within 5 tiles and one ordinary weapon attack or non-resource movement action it took during its previous turn. The enemy makes a Wisdom save. On failure, during its next turn it must repeat that action pattern if legally possible, but it chooses all legal targets and paths; it spends no limited resources and cannot be forced to harm itself. A player-controlled creature instead, on a failed save, loses its Reaction and must choose either repeat one ordinary non-resource action type from its prior turn or have Speed reduced to 0 until turn end. Allies retain memory of all temporal echoes. This Final never creates more than one additional full Action for any creature in a round. There are only two options in this Final; after using both once, remaining rounds provide only the printed temporal presence, without another echo. An echoed healing amount also pays 1 RC or consumes an unused per-rest healing use; a temporal copy cannot create an uncosted healing reserve."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "COPY/FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Up to one healing echo option; requires 1RC or unused healing use; no free reserve.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.engine[11]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": 11,
      "sourceSha256": "965790fb859474dc7264c2a1afe1c947eb45153cea27d16eb10fe47c027ad779",
      "sourceProcedure": {
        "text": "Sustained Oath spell damage/healing zones use concentration, at most three pulses, and 1 RP upkeep after the first pulse unless a priced card expressly supplies a different finite cadence. Native Oath auras retain their printed passive cadence and target cap. Final auras last their stated finite duration and include their pulses. All hard-denial effects, including compelled Actions, share the common once/source/target/encounter guard; later failures only remove Reactions and reduce Speed by half for one turn."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G/MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Sustained Oath zones: first included, later1RP upkeep, ≤3; Finals/native auras exempt.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.hero.lay-on-hands",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.hero.lay-on-hands",
      "sourceSha256": "4c5b19d2b558ca46e38f1d530683c19801b878d8bdf7027cb796e856c5ebcc75",
      "sourceProcedure": {
        "name": "Lay on Hands",
        "activation": "Action",
        "cost": "All remaining Lay on Hands points; minimum 1",
        "rangeAndTarget": "Up to 3 living allies in aura",
        "duration": "Instant",
        "frequency": "1/short rest and pool cost",
        "effect": "Allocate remaining points among targets, at least 1 each; restore 1 HP per point. You may instead allocate 5 points per target to end Poisoned or Frightened. Spend entire pool, cannot multiply it by recipient count, raise the dead or remove Wounds. Oathbreakers instead deal allocated necrotic damage to 3 enemies, CON half, same pool cost."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Single pool-spend heal; corrected Wave cadence belongs elsewhere.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-shared.dread-shelter",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-shared.dread-shelter",
      "sourceSha256": "21aacaa2a10867f745124fcb7d6c76eb33b0c79c19178726cd324df4b92df562",
      "sourceProcedure": {
        "name": "Dread Shelter",
        "activation": "Bonus Action",
        "cost": "3 RP",
        "rangeAndTarget": "Self",
        "duration": "Concentration, 1 minute",
        "frequency": "At will while RP remains",
        "effect": "New rank 2 Forbidden spell. Gain 2 S+M temporary HP on casting and 1 flat DR against weapon damage for duration. No recurring temp HP pulse or healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One temp-HP grant; explicitly no recurring heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-shared.desecrated-ground",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-shared.desecrated-ground",
      "sourceSha256": "5bcc361442663e6799678be29cff54b4a1d6ebd29793db87ec39edc2845513e9",
      "sourceProcedure": {
        "name": "Desecrated Ground",
        "activation": "Action; Bonus Action maintenance",
        "cost": "7 RP start; 1 RP per later pulse",
        "rangeAndTarget": "10 ft radius fixed point 30 ft, up to 3 enemies",
        "duration": "Concentration, maximum 3 pulses",
        "frequency": "Recharge 4",
        "effect": "New rank 4 Forbidden spell. Initial and each paid pulse CON save for S d6 necrotic, half success. A failed target receives 1 less HP per healing die until start of your next turn. Penalty cannot make healing negative or stack with another same-stat reduction."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X/MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Nonhealing damage zone; initial + paid BA pulses under engine11.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-shared.last-reproach",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-shared.last-reproach",
      "sourceSha256": "895f333185c3eb243fcbe76dcc36a38ed52f8b1f4994746abf250a0102f7015d",
      "sourceProcedure": {
        "name": "Last Reproach",
        "activation": "Reaction after an enemy damages an ally",
        "cost": "10 RP",
        "rangeAndTarget": "That enemy 60 ft; one living ally in your aura",
        "duration": "Instant",
        "frequency": "1/short rest",
        "effect": "New rank 5 Forbidden spell. Enemy WIS save for 3 S d8 necrotic, half success; ally regains S d8 HP after triggering damage. Does not revive dead or undo conditions. Uses ordinary spell strain and your Reaction."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I/TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One reaction heal after damage; no pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-mercy.aura-of-mercy",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-mercy.aura-of-mercy",
      "sourceSha256": "2601db1c3ead6e19e3cda88af15a2f7525e96d2d2a1171d037fc874d9c47ae35",
      "sourceProcedure": {
        "name": "Aura of Mercy",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 chosen allies in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets at start of each turn",
        "effect": "The first time each round a selected ally receives HP healing from a finite or paid effect, add S HP. Each selected ally also reduces the first necrotic damage it takes each round by S. These benefits do not stack with another Aura of Mercy from the same source."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: First finite/paid heal per selected ally/round gets +S.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-mercy.blessing-of-the-meek",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-mercy.blessing-of-the-meek",
      "sourceSha256": "de83f7216e4f442bf324e7e9650e69091077d79b1be79d0753257dfbce13cde4",
      "sourceProcedure": {
        "name": "Blessing of the Meek",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "One living ally within 30 feet",
        "duration": "Healing instantaneous; AC bonus until start of your next regular turn",
        "frequency": "At will while RP remains",
        "effect": "The target regains 2d6+M HP. If it was below half maximum HP before this healing, it also gains +2 AC until the start of your next regular turn. This spell cannot resurrect, remove Wounds or generate additional healing triggers beyond ordinary once-per-effect rules."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Single heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-mercy.grace-eternal",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-mercy.grace-eternal",
      "sourceSha256": "9144f23fd7fb45d1beb6c300bb20b85cd3eb172e4a6ac53003c0260770f94a25",
      "sourceProcedure": {
        "name": "Grace Eternal",
        "activation": "Bonus Action",
        "cost": "0 RP",
        "rangeAndTarget": "Up to 3 allies in your Oath aura",
        "duration": "Until start of your next regular turn",
        "frequency": "1/long rest",
        "effect": "Apply Miracle Veil to up to 3 allies in your aura without spending its short-rest use or RP. Once during this Veil for each affected ally, if damage would reduce it to 0 HP, it remains at 1 HP and immediately regains 2d8 HP. It also gains necrotic resistance until the end of its next turn. During Grace Eternal you may use Lay on Hands once without an Action, but must still spend points from your current Lay on Hands pool and may target only one creature."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I/MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Finite floor+heal per ally; one actionless LoH permission; no pulse schedule.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression",
      "sourceSha256": "1613079d8c08dac41dc4b7fe98b3dbbf5f4534a28a2d30282e93522bd69fdbde",
      "sourceProcedure": {
        "name": "Healing Suppression",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets at start of each turn",
        "effect": "HP healing received by each selected creature is halved, rounded down. Temporary HP, damage prevention and resurrection are not healing for this effect. This suppression cannot reduce healing below 0 or convert prevented healing into damage."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Incoming HP healing halved; no pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate",
      "sourceSha256": "7fdfc30a56a5fbfec418c11a859f48cc7636e45998913a574f3b8dd80d7d14f5",
      "sourceProcedure": {
        "name": "Exsanguinate",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 living creatures in your Oath aura",
        "duration": "Instantaneous",
        "frequency": "1/short rest; replaces Signature Power use",
        "effect": "Each target makes a Constitution save, taking 2 S d8 necrotic damage on failure or half on success. Regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. Undead and constructs are unaffected and cannot be used to generate healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Single damage-derived heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-flame.phoenix-rebirth",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-flame.phoenix-rebirth",
      "sourceSha256": "0a38ac2a6f534b9b6eefaa79733078371cc3169aa85ed60b825247cdfdf6ffd9",
      "sourceProcedure": {
        "name": "Phoenix Rebirth",
        "activation": "Reaction",
        "cost": "10 RP",
        "rangeAndTarget": "One living ally in your Oath aura reduced to 0 HP",
        "duration": "Revival instantaneous; fire shield until end of target's next turn",
        "frequency": "Once per combat per ally",
        "effect": "Trigger when the ally reaches 0 HP without being killed outright. It immediately regains HP equal to half its maximum, rounded down, minimum 1. Until the end of its next turn it has fire resistance. Once during that duration when a creature within melee reach damages it with a melee attack, that attacker takes 2d6 fire damage. Phoenix Rebirth removes no Wounds and cannot restore a creature destroyed beyond recovery."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "I",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Single zero-HP recovery; no recurring heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood",
      "sourceSha256": "d622135b269bb89a3f32d0f6ef20481b4d3b7a70ffe4601e14e0212048d385b5",
      "sourceProcedure": {
        "name": "Death Touch — Blighting Blood",
        "activation": "Action",
        "cost": "Declare and spend 1 through 2 S+M points from current Lay on Hands pool, even on miss",
        "rangeAndTarget": "One creature within melee reach; its occupied space",
        "duration": "Damage instantaneous; blighted space until start of your next regular turn",
        "frequency": "At will while Lay on Hands points remain; terrain rider once per turn",
        "effect": "Make a melee divine attack using PB+Charisma. On hit deal necrotic damage equal to the declared points and blight the target's space until the start of your next turn. The first hostile creature other than the original target that enters or starts its turn in that space takes S necrotic damage. The patch creates no corpse, healing or resource trigger."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Damage/terrain only; explicitly no healing trigger.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified",
      "sourceSha256": "cbfc7808eaa7713c9e05331e24397dcbea9a3a6642ed0d08f088e4c582a950e8",
      "sourceProcedure": {
        "name": "Scorch the Sanctified",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 enemies in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets at start of each turn",
        "effect": "Selected enemies cannot regain HP from passive regeneration. At the start of each selected enemy's turn it makes a Charisma save. On failure, one temporary beneficial magical effect on it chosen by the Director from eligible non-innate effects is suppressed until the start of its next turn. Immunities, class engines, permanent traits and attunement are never suppressed."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Blocks passive regeneration only.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word",
      "sourceSha256": "792ec5718045963e10d1e82e7880f66c22de6fa172a81242389edb31ea7c38f6",
      "sourceProcedure": {
        "name": "Scorch the Sanctified — Blasphemous Word",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 creatures in your Oath aura",
        "duration": "Instantaneous; suppressed effect until end of next turn",
        "frequency": "1/short rest; replaces Signature Power use",
        "effect": "Each target makes a Constitution save, taking S d6 fire plus S d6 necrotic damage on failure or half on success. A failing target also has one eligible temporary beneficial spell or regeneration effect suppressed until the end of its next turn. You may knowingly include allies among the targets; the effect offers them no protection."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G/X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Damage + temporary regeneration-effect suppression.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura",
      "sourceSha256": "ab791099a2d42dd7017f37b891cda2e14f4c1c3ae23f73ef652dd3f459028af2",
      "sourceProcedure": {
        "name": "Lifeleech Bloom Aura",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 enemies in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets and one damage type at start of each turn",
        "effect": "Selected enemies cannot regain HP from passive regeneration. Also choose acid, cold, fire, lightning, necrotic, poison, radiant or thunder. A selected enemy's resistance to that chosen type is suppressed while it remains selected in the aura; immunity is never suppressed."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Blocks passive regeneration; not all finite healing.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom",
      "sourceSha256": "08c5946db93747abe8a71ed1a6aa82258108a072d3873c9f85a8ddae94fba83f",
      "sourceProcedure": {
        "name": "Lifeleech Bloom",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 living creatures or plant creatures in your Oath aura",
        "duration": "Instantaneous",
        "frequency": "1/short rest; replaces Signature Power use",
        "effect": "Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. You regain HP equal to half the total actual damage dealt, rounded down, maximum Paladin level+M. You may include willing allies among the targets, but they receive no protection and cannot be reduced below 1 HP by this Blasphemous Word. Constructs and ordinary unattended plants provide no healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Single damage-derived heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-grief.dirge-of-passage",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-grief.dirge-of-passage",
      "sourceSha256": "df1f6705254fc3dcbf79d5c08aae5baf78e792c21ce9e059969dfe4627c62200",
      "sourceProcedure": {
        "name": "Dirge of Passage",
        "activation": "Bonus Action",
        "cost": "0 RP",
        "rangeAndTarget": "Memories of up to 2 fallen allies; creatures in your Oath aura",
        "duration": "2 rounds",
        "frequency": "1/long rest",
        "effect": "For 2 rounds maintain two Final Vigil memories simultaneously and gain both selected benefits. Up to three selected hostile undead in your aura take an additional S radiant damage from your first damaging Paladin feature each round and cannot regain HP. Living allies in your aura gain +2 on death saves. No spirit gains its own turn, resources, spellcasting or complete former statistics. This flat rider replaces blanket damage vulnerability and never doubles a whole attack."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G/X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Prevents hostile-undead HP regain; no healing pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura",
      "sourceSha256": "65f1ac74f274a2f171571f40d3ce938061c6e4c58fba8925270b949fcec183ff",
      "sourceProcedure": {
        "name": "Dirge of Ruin Aura",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
        "duration": "While conscious and target remains in aura",
        "frequency": "Choose targets at start of each turn",
        "effect": "Selected living creatures cannot be returned from death while inside the aura, and HP healing they receive is reduced by S+M, minimum 0. This never converts healing into damage and cannot retroactively reverse a resurrection completed before the creature entered the aura."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Flat healing reduction + resurrection denial.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin",
      "sourceSha256": "16cc8982591672cdbad5aa34bf755e2c4b8024c032fb29dba978ec14eb4d6407",
      "sourceProcedure": {
        "name": "Dirge of Ruin",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 creatures in your Oath aura",
        "duration": "Damage instantaneous; healing block until end of next turn",
        "frequency": "1/short rest; replaces Signature Power use",
        "effect": "Each target makes a Constitution save, taking 2 S d6 necrotic damage on failure or half on success. A failing target cannot regain HP until the end of its next turn. This does not prevent temporary HP or remove healing already received."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G/X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Damage plus temporary no-HP-regain.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.crown-of-embers",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.crown-of-embers",
      "sourceSha256": "0ff07991fa0838522e96deb9434534c8c584850c6203ed3b47e8eeaf4246980f",
      "sourceProcedure": {
        "name": "Crown of Embers",
        "activation": "Bonus Action",
        "cost": "2 RP",
        "rangeAndTarget": "Up to 3 allies in your Oath aura",
        "duration": "Until start of your next regular turn",
        "frequency": "1/short rest",
        "effect": "Selected allies reduce the first damage they take before the start of your next turn by S. During this period you may redirect damage from one selected ally to yourself without using a Reaction, once total for the Crown, up to Paladin level+M damage. Redirected damage retains type and cannot be redirected again. The Crown grants no healing by itself."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Prevention/redirection only; expressly no healing.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.burden-shared",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.burden-shared",
      "sourceSha256": "2a0ff54276d9127ac30458bae7ea5dc0f1295b5ec34ca63bb5ce22efdabb29d1",
      "sourceProcedure": {
        "name": "Burden Shared",
        "activation": "Reaction when an ally takes damage",
        "cost": "5 RP",
        "rangeAndTarget": "Triggering ally and up to two other willing allies in your aura",
        "duration": "One damage event",
        "frequency": "While RP remains",
        "effect": "After applying the original target’s defenses once, divide up to Paladin level+M of the remaining damage among the willing recipients as you choose; each recipient must explicitly accept its amount. The original ally takes the remainder. Transferred damage keeps its type and cannot be reduced again, redirected, reflected or trigger healing/resources. This uses the one redirection event per round."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Redirection only; transferred branch cannot trigger healing.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.throne-s-grace",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.throne-s-grace",
      "sourceSha256": "084a132d73f1f54d9155a932605eb82e4da34e8e1f61e69ca51c5031b3c502ad",
      "sourceProcedure": {
        "name": "Throne’s Grace",
        "activation": "Action",
        "cost": "7 RP",
        "rangeAndTarget": "Self and up to three allies in your aura",
        "duration": "Concentration; three rounds",
        "frequency": "While RP remains",
        "effect": "Your Lay on Hands and touch-range Paladin healing can target selected allies anywhere in your current aura with clear line of effect. Normal activation, pool/RP costs, rank gates and use limits remain. Rolled healing you grant them adds 1 HP per die, maximum S+M additional HP per effect; pool-point healing adds no dice bonus. Selected allies gain +1 on death saves. The spell itself restores no HP."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Modifies other Paladin heals; itself restores none.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oath-of-the-martyr-king.crown-undying",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oath-of-the-martyr-king.crown-undying",
      "sourceSha256": "f8de6f3fe586c6b30d10bbdd31c93e0976aa46dfb3631afbbcbebe8ebe1d0b1d",
      "sourceProcedure": {
        "name": "Crown Undying",
        "activation": "Bonus Action",
        "cost": "0 RP",
        "rangeAndTarget": "Up to three selected allies in your aura",
        "duration": "Three rounds; no concentration",
        "frequency": "1/long rest",
        "effect": "For three rounds apply Crown of Embers protection without consuming its short-rest use. Selected allies reduce their first damage each round by S and gain +1 on saves; this save bonus does not stack with Aura of the Crown. You may redirect from up to two selected allies each round, at most Paladin level+M damage total per round, without a Reaction. Original-target defenses apply once; redirected damage cannot be reduced again. Each protected ally then heals half the damage you actually absorbed for it, rounded down, maximum S+M per ally per round. This is a finite Final healing exception, cannot heal you, cannot exceed maximum HP, and cannot trigger another redirection or heal-copy chain. It does not reset the daily Lay on Hands pool."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Finite redirection-derived healing; redirection ledger governs cadence.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/paladin.json",
      "sourceId": "paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura",
      "sourceSha256": "e4341a3bd789ba5baa4c0bf1817a7a16ec61fc0d98d9ca79101397f9f984f203",
      "sourceProcedure": {
        "name": "Crownshatter Decree Aura",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Up to three selected enemies in your aura",
        "duration": "While conscious and in aura",
        "frequency": "Each incoming healing event",
        "effect": "A selected enemy receives HP healing only if it has taken actual damage from a meaningful hostile creature since the start of its previous regular turn. If it has not, that healing restores 0 HP; its source still spends its normal costs. Temporary HP, stabilization and resurrection are not HP healing for this restriction. This aura never creates damage, transfers healing or reverses recovery that already resolved."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Conditional incoming-heal permission; source costs still spent when blocked.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "ranger.engine[5]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/ranger.json",
      "sourceId": 5,
      "sourceSha256": "f45c0cef68da878ce0d7921f372222c3698711b0f412f432597bbc20445859da",
      "sourceProcedure": {
        "text": "Chosen Hero grants a sixth Arrow at 11. Warder Nature's Wrath: ranged attack weapon+S d6 piercing; up to 2 allies within 10 ft gain M temporary HP (finite mitigation, not repeatable real healing). Stalker Phantom: two ranged attacks against different aligned targets within 60 ft, each weapon damage, no extra dice; one Arrow activation. Outrider Corruption: place 10 ft-radius zone within 60 ft, concentration until start next turn; up to 3 enemies entering/starting there take S d4 necrotic once each, CON half. Arrow copies cannot generate extra attacks, resources or permanent terrain changes."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Temp HP / damage-zone interfaces; no recurring real heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "ranger.hero.warder.living-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/ranger.json",
      "sourceId": "ranger.hero.warder.living-pulse",
      "sourceSha256": "e1b7bfa045b543de315480c9e783e4da0cc13ea5adad64a79ca535d32af375bd",
      "sourceProcedure": {
        "name": "Living Pulse",
        "activation": "Triggered",
        "cost": "1 RP",
        "rangeAndTarget": "Self in natural terrain",
        "duration": "Start of your regular turn",
        "frequency": "Once/turn",
        "effect": "You may pay 1 RP to regain 2 HP. Does not trigger when Downed or incapacitated, cannot exceed maximum and never counts as another healing spell. Replaces unlimited passive regeneration with a finite cost."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "NR",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Once source regular-start/turn, optional1RP, self2HP.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "ranger.hero.warder.healing-briar",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/ranger.json",
      "sourceId": "ranger.hero.warder.healing-briar",
      "sourceSha256": "d1ca2d633ca412393953afab0065f0439a3ad3a7f95d50500385078c999e1f6f",
      "sourceProcedure": {
        "name": "Healing Briar",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "Fixed 10 ft-radius natural-ground zone within 30 ft; 3 allies/pulse",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 4",
        "effect": "On start heal 1d8+M per chosen living ally; on next 2 turns Bonus Action+1 RP repeats pulse. Maximum 3 pulses; no passive additional entry healing and no Wound removal."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI/paid",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start included; next2 source turns BA+1RP; max3; repick≤3.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.engine[1]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 1,
      "sourceSha256": "2a2a89b4f440277a59743d2dc2936f2a625be9557882f5796fa8fb71d4b76d80",
      "sourceProcedure": {
        "text": "Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Renewal start included; next2 BA+1RP; ≤3 beneficiaries/pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.engine[2]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 2,
      "sourceSha256": "673d1b3887e874041180d1c813ee02efa51962dbc07a33844853a708b1468a5a",
      "sourceProcedure": {
        "text": "On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Movement competes with upkeep; movement creates no extra pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.arch.extended-totem-duration",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.extended-totem-duration",
      "sourceSha256": "d3e1a07ab47f089ce66a98f3ef5083eb604f55174892955836175df7c94724bb",
      "sourceProcedure": {
        "name": "Extended Totem Duration",
        "activation": "Passive",
        "cost": "0; full upkeep for extra Renewal pulse",
        "rangeAndTarget": "One of your totems",
        "duration": "Maximum 4 of your turns",
        "frequency": "Continuous",
        "effect": "Totems last 1 extra turn. Renewal may have a fourth pulse only if you pay Bonus Action+1 RP on that turn; no fifth pulse and no automatic free healing. Concentration still required."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD/MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: One fourth Renewal opportunity only with BA+1RP.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.arch.spirit-cache",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.spirit-cache",
      "sourceSha256": "9a84d6cf21f387bfc7fc32c7e9e7344aa7449da4abd8e24b96e76710e18249ce",
      "sourceProcedure": {
        "name": "Spirit Cache",
        "activation": "Triggered",
        "cost": "1 short-rest use",
        "rangeAndTarget": "One flask/to-tem effect you directly used",
        "duration": "Stored until encounter end",
        "frequency": "1/short rest",
        "effect": "Store its profile, not an active copy. On a later turn use normal Action/Bonus Action and pay all RP and a new flask unit or full totem cost to repeat it. Add 1d6 to one numerical damage/heal amount; no copy of refund/limited use."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "COPY",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Recast profile later with full costs/new stock; not active pulse copy.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.arch.totem-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.totem-pulse",
      "sourceSha256": "da88a2c237b85efcd2b52a63b65f8a2decafbdc6671d11820ab72f859f0c0ce6",
      "sourceProcedure": {
        "name": "Totem Pulse",
        "activation": "Passive",
        "cost": "1 RP optional",
        "rangeAndTarget": "Up to 3 creatures inside newly placed non-healing totem",
        "duration": "Instant",
        "frequency": "Once/turn",
        "effect": "On placement pay 1 RP: allies gain M temporary HP OR enemies make DEX save for S affinity damage, half on success. No immediate second Renewal healing pulse, no repeat from moving the totem."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Nonhealing placement pulse; no extra Renewal heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.arch.spirit-saturation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.spirit-saturation",
      "sourceSha256": "e25c049b60111d478b8844f935bfdf3b1f6068d80100de6a8c2d702a9723f543",
      "sourceProcedure": {
        "name": "Spirit Saturation",
        "activation": "Triggered",
        "cost": "1 long-rest use",
        "rangeAndTarget": "One non-Renewal totem you place",
        "duration": "Normal duration",
        "frequency": "1/long rest",
        "effect": "Waive its 2 RP placement cost once. Still use Action, concentration, capacity and any added costs. Cannot create a healing totem or be cached/refunded to generate more free casts."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X/G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Cannot waive/create Renewal healing totem.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.echo-totem",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.echo-totem",
      "sourceSha256": "20874e77366801074f6dc417c26450a1957dab6d55ca77ba083e370fec3fa92b",
      "sourceProcedure": {
        "name": "Echo Totem",
        "activation": "Triggered",
        "cost": "1 additional RP",
        "rangeAndTarget": "Adjacent empty space within 5 ft of newly placed totem",
        "duration": "Same remaining duration",
        "frequency": "Once/placement",
        "effect": "Create a weak echo anchor of that totem. It counts toward capacity; if no space in capacity, cannot create it. Its radius 10 ft and numerical bonuses/healing are half, rounded down. Shared concentration/upkeep and same-name nonstacking prevent double healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD/MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Shares parent pulse/upkeep; half amount; NEW shared target budget/no double heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.hero.bloodcaller.blight-totem",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.bloodcaller.blight-totem",
      "sourceSha256": "56bd3dd7b141931dda883f3728d30221c8e34ba30347d55c87fe66dc2f338805",
      "sourceProcedure": {
        "name": "Blight Totem",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "Totem within 30 ft; 15 ft aura affecting all creatures",
        "duration": "3 of your turns",
        "frequency": "Ordinary totem capacity/concentration",
        "effect": "HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Healing-halving aura only.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.hero.bloodcaller.blood-curse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.bloodcaller.blood-curse",
      "sourceSha256": "34064d553a32ec2626c5cf9fd9dffdfc4c7a53c5027914e0b3a927be699b9319",
      "sourceProcedure": {
        "name": "Blood Curse",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "One living enemy within 60 ft",
        "duration": "3 target turns",
        "frequency": "Recharge 3",
        "effect": "CON save or Bleed 1d4 necrotic at start of each of next 3 turns. Action plus successful Medicine check against class DC ends it; magical healing also permits an immediate CON save to end. Never permanently unhealable; no repeated stacking."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Magical healing permits cure save; healing itself not scheduled.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "shaman.supplement.elder-spirit-accord-new-hero-capstone",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.supplement.elder-spirit-accord-new-hero-capstone",
      "sourceSha256": "14135567a903c049f854953b8feb74893959b5f92c58123af008a3d8e67eac70",
      "sourceProcedure": {
        "name": "Elder Spirit Accord — new Hero capstone",
        "activation": "Triggered",
        "cost": "1 long-rest use",
        "rangeAndTarget": "Your chosen Hero ultimate",
        "duration": "One activation",
        "frequency": "1/long rest",
        "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Adds M to one healing roll/use; no duration/pulse increase.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "soldier.engine[4]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/soldier.json",
      "sourceId": 4,
      "sourceSha256": "f4f11a1404b15b950d423edee89296a42130ca4ca686b322d4259ecda7e1b6ed",
      "sourceProcedure": {
        "text": "Base 1–2, Commander Arch 3–9, then Champion/Artillerist/Tyrant Hero 10–20. Palisade 5 is automatic; Intercepting Shot has minimum 6 and Fortify Zone 9. Other cards require selection. There is no source automatic Arch capstone. At 20 gain the new Final Command below, clearly a playtest addition. No spell or sustained technique may be used to obtain infinite ammunition, structures, actions or permanent healing."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Anti-infinite-healing guard only.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "thief.hero.blackguard.exsanguinate",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/thief.json",
      "sourceId": "thief.hero.blackguard.exsanguinate",
      "sourceSha256": "37e182dce2daee77d1a02e8e10618f449d263f1fd06d4a1ea9a7db6937821a2f",
      "sourceProcedure": {
        "name": "Exsanguinate",
        "activation": "Triggered",
        "cost": "1 RP",
        "rangeAndTarget": "Self; bleeding enemy within 15 ft",
        "duration": "Instant",
        "frequency": "Once/own turn",
        "effect": "At start of your regular turn with a hostile bleeding enemy nearby you may pay 1 RP to regain S HP. No multiplying by enemy count or healing while incapacitated; not an ordinary spell or Dissonance-generating technique."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "NR",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Source regular-start/turn, optional1RP, once/own turn.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.engine[7]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 7,
      "sourceSha256": "9429949777c5be914254699b4403f903a1e617504b801672deaff80b2f0ae0d4",
      "sourceProcedure": {
        "text": "Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Healing pulse caps/costs remain; disabled duration continues.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.base.field-repair",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.field-repair",
      "sourceSha256": "612a9f00b4e33a8bfc77c3f83ff1e1d839fa1237e8d20e65b703bea1431b6d7f",
      "sourceProcedure": {
        "name": "Field Repair",
        "activation": "Action",
        "cost": "1 RP",
        "rangeAndTarget": "One construct/device touched",
        "duration": "Instant",
        "frequency": "Recharge 2",
        "effect": "Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "DEV/X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Instant functional-device repair; not organic healing pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.efficient-power-cells",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.efficient-power-cells",
      "sourceSha256": "c9738585ed8fae504de1ec5a0603fbea55a31fbcc5c4711838d7c7a252736c44",
      "sourceProcedure": {
        "name": "Efficient Power Cells",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your nonhealing deployables",
        "duration": "Deployment",
        "frequency": "Continuous",
        "effect": "A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X/G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Nonhealing duration extension only; healing pulse count unchanged.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.nano-aegis-drone",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.nano-aegis-drone",
      "sourceSha256": "a3117289c319bbe6ef18ae9437975f46db8da26795fd3f271cb54b443b93ee01",
      "sourceProcedure": {
        "name": "Nano-Aegis Drone",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Your drone within 15 ft",
        "duration": "3 rounds",
        "frequency": "Recharge 4",
        "effect": "Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI/command",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Up to3 paid BA-command healing/tempHP pulses during3 rounds.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.repair-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.repair-pulse",
      "sourceSha256": "bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593",
      "sourceProcedure": {
        "name": "Repair Pulse",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "Upto 3 friendly devices within 30 ft",
        "duration": "Instant; AC until start next turn",
        "frequency": "1/short rest",
        "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "DEV/X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Instant device repair; no organic healing.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.restoration-field",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.restoration-field",
      "sourceSha256": "a791259766db2192f9effe98f8946304ee8ef85d4ff243faa87c04665bf96ffa",
      "sourceProcedure": {
        "name": "Restoration Field",
        "activation": "Action",
        "cost": "3 RP start; 1 RP maintenance; one slot",
        "rangeAndTarget": "10 ft radius within 30 ft",
        "duration": "Maximum 3 pulses",
        "frequency": "Recharge 4",
        "effect": "Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MP",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Initial pulse + later BA+1RP maintenance; max3; organic/device applications distinct.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "tinker.supplement.mech-overdrive",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.supplement.mech-overdrive",
      "sourceSha256": "0a3d5549a68c395cdfa364bac06f334436af7ac848ca5fed71a0a9bc141aec73",
      "sourceProcedure": {
        "name": "Mech Overdrive",
        "activation": "Triggered on deploying a device",
        "cost": "1 long-rest use plus original deployment cost",
        "rangeAndTarget": "One of your newly deployed devices",
        "duration": "Until encounter end, maximum 1 minute",
        "frequency": "1/long rest; automatic Hero capstone",
        "effect": "Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "G",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Duration extension only; never increases healing pulses.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.hero.ironskin.regenerative-mutation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.ironskin.regenerative-mutation",
      "sourceSha256": "9dcfe6b7b149360e470c0d7940937b13c7bbdc4f696999b93710257158818fd1",
      "sourceProcedure": {
        "name": "Regenerative Mutation",
        "activation": "Passive",
        "cost": "Spend healing amount from Mutation Recovery Reserve",
        "rangeAndTarget": "Self",
        "duration": "While at least one mutation is active in a real encounter",
        "frequency": "Once at the start of each regular turn",
        "effect": "Regenerative Mutation. At the start of your regular turn during a real encounter, if at least one mutation is active and you are below maximum HP, regain S+M HP. This regeneration functions only during a real encounter, cannot restore the dead or remove Wounds, and cannot be increased by remaining in initiative without meaningful opposition. Each HP actually restored spends 1 Mutation Recovery Reserve; heal only up to remaining reserve."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "NR",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start each source regular turn; reserve-paid actual restoration; no3-cap.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.hero.ironskin.cellular-reconstruction",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.ironskin.cellular-reconstruction",
      "sourceSha256": "e8bd145d4393467058e51509e15230c1bc315884f24f96ccfb509faa5186d56c",
      "sourceProcedure": {
        "name": "Cellular Reconstruction",
        "activation": "Action",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Until start of your next regular turn, then instantaneous recovery",
        "frequency": "1/long rest",
        "effect": "Cellular Reconstruction. Enter stasis until the start of your next regular turn: your Speed becomes 0, you cannot take Actions, Bonus Actions or Reactions, and attacks against you have advantage. At the start of your next turn regain 3d8 + M HP and end Poisoned plus one mundane or magical disease that does not explicitly require a special cure. This removes no Wounds and cannot function while dead."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Delayed one-time source-next-start recovery after stasis.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.hero.dreadspawn.pain-empowerment",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.hero.dreadspawn.pain-empowerment",
      "sourceSha256": "2b76787a8cddab4ebacdbf316a7c566f95cc8e0607dcc02cafc57f0dc09741ab",
      "sourceProcedure": {
        "name": "Pain Empowerment",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "While below maximum HP",
        "frequency": "Always",
        "effect": "Pain Empowerment. For every full 10% of your maximum HP currently missing, add +1 damage to one weapon or natural-weapon damage roll on each of your turns, maximum +5. Determine the bonus immediately before the chosen damage roll. Healing can reduce the bonus during the encounter. It does not increase mutation retaliation, ongoing damage or area effects."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Threshold damage passive, not healing recurrence.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.supplement.primed",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.primed",
      "sourceSha256": "4ed45f7e4cbd2ee61dab2a5126f7d5494750257f17b5699d5ff4bb5fcffbc324",
      "sourceProcedure": {
        "name": "Primed",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "One active mutation each turn",
        "duration": "While BT remains at least 2",
        "frequency": "Once per turn",
        "effect": "Enhance one active mutation's numeric benefit for the turn: +1 to one AC, DR, attack, save or flat damage bonus; +5 feet to one movement/reach bonus; or +1 damage/healing to one mutation-generated roll. Primed never increases duration, targets, immunity or resource generation."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: +1 to one mutation heal roll/turn; no new pulse.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.supplement.transcendent",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.transcendent",
      "sourceSha256": "473a344f361727b78897d649edbcc5fa6ad32f5edee5a0a6e9c943f027272f3c",
      "sourceProcedure": {
        "name": "Transcendent",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Until start of your next regular turn",
        "frequency": "1/encounter total, regardless of trigger",
        "effect": "At Warrior 12+, the first time this encounter you cross 100% Brutality Progress or reach stored BT 4, activate all equipped mutations until start of your next regular turn. No serum profile or immediate healing trigger is granted. This is one total pulse, never a permanent BT 4 concurrency increase. At end choose active mutations up to normal limit, with their original remaining durations; others become dormant."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Explicitly no immediate healing trigger.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.supplement.bloodthick-node",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.bloodthick-node",
      "sourceSha256": "d0a5ce3e76d61b789bfa1ab1daebf96399f56187b8fc796a0e44a1697007618b",
      "sourceProcedure": {
        "name": "Bloodthick Node",
        "activation": "Passive while active",
        "cost": "One mutation slot; serum activation",
        "rangeAndTarget": "Self",
        "duration": "While active during a real encounter",
        "frequency": "Once at start of each regular turn",
        "effect": "Regain HP equal to current BT, maximum 3 HP per turn or 4 with Stack Overflow. No healing occurs outside a real encounter and it removes no Wounds. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "NR",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start each regular turn, reserve-limited; no3-cap.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.supplement.rapid-coagulation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.rapid-coagulation",
      "sourceSha256": "8f6169026b8720168ba76650964f555e611eb7cc5c65f24be359a3561fbaa8ad",
      "sourceProcedure": {
        "name": "Rapid Coagulation",
        "activation": "Passive while active",
        "cost": "One mutation slot; serum activation",
        "rangeAndTarget": "Self",
        "duration": "While active during a real encounter",
        "frequency": "Start of turn",
        "effect": "If you did not move during your previous turn, regain 2 HP at the start of your current turn. This does not function outside a real encounter. Each HP actually restored spends 1 Mutation Recovery Reserve; heal no more than remaining reserve."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "NR",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Start each regular turn if prior-turn no movement; reserve-limited.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "warrior.supplement.bio-stabilizer",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/warrior.json",
      "sourceId": "warrior.supplement.bio-stabilizer",
      "sourceSha256": "1bc1a0dd29cac0774f73c5c357f1c81ade4efca327bf104ce4004eaad84de7b7",
      "sourceProcedure": {
        "name": "Bio-Stabilizer",
        "activation": "Passive",
        "cost": "Feat choice",
        "rangeAndTarget": "Self",
        "duration": "Permanent",
        "frequency": "Always",
        "effect": "While at least two mutations are active, Bloodthick Node heals 1 additional HP on each of its valid encounter-only regeneration pulses."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "MOD",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: +1 to valid Bloodthick pulse; no independent heal.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "wizard.engine[10]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/wizard.json",
      "sourceId": 10,
      "sourceSha256": "673521960e487b21772372733af6aaa0c478c7f3308b6a58607a3c5ac2d83f99",
      "sourceProcedure": {
        "text": "ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "X",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Temp HP/max-HP school effects; Necromancy tempHP is not healing.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    },
    {
      "bindingId": "wizard.hero.necromancer.infernal-pact-quest-based-unlock",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/wizard.json",
      "sourceId": "wizard.hero.necromancer.infernal-pact-quest-based-unlock",
      "sourceSha256": "3ec78d206b84e52afbca7eefd488313b4aeb4371a3edb80e5f9e6e14636d053d",
      "sourceProcedure": {
        "name": "Infernal Pact (Quest-based unlock)",
        "activation": "Bonus Action",
        "cost": "3 RP",
        "rangeAndTarget": "One creature within 60 feet",
        "duration": "Maximum 3 rounds",
        "frequency": "1/long rest; quest-gated",
        "effect": "Infernal Pact — Gravebrand. Tags: hero, necromancer, infernal, necrotic, dark-content. This card can be selected only after completing the campaign's Infernal Pact quest and its dark-trauma check-in. Mark one creature. At the start of each of its turns it makes a Constitution save; on failure it takes 1d6 necrotic damage and you regain HP equal to the actual damage dealt, maximum S+M; success ends Gravebrand. Gravebrand ignores necrotic resistance but not immunity. While you possess this Pact, Corpse Harvest and Auto-Raise may also treat Fiend corpses as eligible; other creature types remain ineligible."
      },
      "status": "DISCUSSED; exact boundaries and implementation pending",
      "classification": "TH/FI",
      "operationalOverrides": [
        "FIRST PROPOSAL; read later source corrections before implementing: Target-start damage; heal from actual damage, max3-round source; not a healing pulse itself.",
        "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending."
      ],
      "reviewEvidence": [
        "GPT_HEALING_PULSE_FIRST_REVIEW.md",
        "GPT_HEALING_PULSE_BOUNDARIES.md"
      ],
      "openIssues": [
        "Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed."
      ]
    }
  ]
}
