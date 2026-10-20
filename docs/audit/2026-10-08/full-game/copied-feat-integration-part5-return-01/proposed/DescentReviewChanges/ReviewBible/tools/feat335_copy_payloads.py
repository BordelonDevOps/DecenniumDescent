"""SUP-07 recipient effects over actual paid CopyReleases.

Conditional world integration, not a complete game runtime. The caller owns
perception, body-space/range/LoE queries, explicit current target defenses,
turn markers, action frames and RNG visibility/interrupt scheduling. This
adapter executes bounded payload arithmetic, canonical LifeState/BufferLedger
mutations, source-owned slow/boon records, deadlines and concentration cleanup.
Ready and other unresolved provider/allowance integrations are excluded.
"""
from copy import deepcopy
from dataclasses import asdict, replace
from fractions import Fraction
from feat335_copy_release import CopyReleases, CopyConcentration, CONCENTRATION
from feat335_copy_source_components import bounded_native_numeric, integer
from core_playtest_rules import LifeState, attack_roll, saving_throw
from form_temphp_playtest_rules import BufferLedger, BufferGrant
from healing_playtest_rules import healing_packet
from control_playtest_rules import ClockMarker, clock_marker, regular_control_endpoint, SpeedRecord, effective_control_speed


def require(value, message):
    if not value:raise ValueError(message)


def selected_d20(faces, mode):
    require(mode in {'normal','advantage','disadvantage'},'Actual resolved roll mode required')
    count=1 if mode=='normal' else 2
    require(isinstance(faces,list) and len(faces)==count,'Complete actual d20 procedure required')
    for face in faces:integer(face,'d20 result',1,20)
    return faces[0] if mode=='normal' else max(faces) if mode=='advantage' else min(faces)


class PayloadConcentration(CopyConcentration):
    def __init__(self, owner, ledger, profiles, world):
        super().__init__(owner,ledger,profiles);self.world=world

    def _ended(self, event, reason):
        super()._ended(event,reason)
        self.world.end_source(self.owner,event,reason)


class CopyPayloadWorld:
    def __init__(self, actors, buffers):
        require(isinstance(buffers,BufferLedger),'Canonical shared buffer ledger required')
        self.actors=actors;self.buffers=buffers;self.now=ClockMarker(0)
        self.observations={};self.effects={};self.speed_records=[];self.resolutions={}
        for actor in actors.values():
            require(isinstance(actor['life'],LifeState),'Canonical existing LifeState required')
            require(actor['life'].temp_hp==buffers.amount(actor['id']),'One canonical temporary-HP balance required')
            require(actor['id'] in actors and actors[actor['id']] is actor,'Canonical actor identity required')
            for key in ['creature','living','willing','coreSpeedZero','ordinaryReactionAllowed','magicAllowed','hpGainProhibited','copyHindranceImmune','conscious','canAct','verbalAvailable','somaticAvailable']:
                require(type(actor[key]) is bool,'Actual Boolean world state required: '+key)
            for key in ['ordinaryAC','speedBeforeControl','flatDamageReduction']:
                integer(actor[key],key)
            require(all(isinstance(actor[k],set) for k in ['damageImmunities','damageResistances']),'Actual typed damage-defense sets required')

    def snapshot(self):
        return deepcopy({'now':self.now,'actors':self.actors,'observations':self.observations,
            'effects':self.effects,'speedRecords':self.speed_records,'buffers':self.buffers.__dict__,
            'resolutions':self.resolutions})

    def projection(self):
        for ident,actor in self.actors.items():actor['life'].temp_hp=self.buffers.amount(ident)

    def end_source(self, owner, event, reason):
        dependency=owner+'::feat-copy::'+event
        self.buffers.end_dependency(dependency)
        for effect in self.effects.values():
            if effect['owner']==owner and effect['cast']==event and effect['active']:
                effect.update(active=False,endReason=reason)
        self.speed_records=[replace(r,active=False) if r.owner==owner and r.application_id==dependency else r for r in self.speed_records]
        self.projection()

    def speed(self, target):
        return effective_control_speed(self.actors[target]['speedBeforeControl'],
            [r for r in self.speed_records if r.target==target],target=target,now=self.now,
            core_speed_zero=self.actors[target]['coreSpeedZero'])

    def reaction_allowed(self, target):
        return self.actors[target]['ordinaryReactionAllowed'] and not any(
            e['target']==target and e['profile']=='hindrance' and e['active'] and self.now<e['deadline']
            for e in self.effects.values())

    def ac(self,target):
        ordinary=self.actors[target]['ordinaryAC']
        # Caller ordinaryAC already includes its own non-copy arbitration.
        copy=max((1 for e in self.effects.values() if e['target']==target and e['profile']=='boon'
            and e['statistic']=='AC' and e['active'] and self.now<e['deadline']),default=0)
        return ordinary+copy

    def advance(self, now, releases):
        marker=clock_marker(now);require(marker>=self.now,'World time cannot move backward')
        # Bound all live copy sources to the same shared ledgers.
        by_owner={r.owner:r for r in releases}
        require(len(by_owner)==len(releases),'One copy engine per owner required')
        for e in self.effects.values():
            if e['active']:require(e['owner'] in by_owner and by_owner[e['owner']].world is self,'All live source engines required for expiry')
        for engine in releases:
            validate = getattr(engine.lifecycle.ledger, 'validate_current', None)
            if validate: validate()
        self.now=marker
        for effect in list(self.effects.values()):
            if effect['active'] and marker>=effect['deadline']:
                engine=by_owner[effect['owner']]
                engine.lifecycle.end_at_deadline(effect['cast'],actual_source_deadline=True)
        self.buffers.expire(marker);self.projection()


class CopyPayloadReleases(CopyReleases):
    def __init__(self, captures, owner, pool, cadence, concentration, world):
        require(isinstance(world,CopyPayloadWorld) and owner in world.actors,'Canonical recipient world required')
        super().__init__(captures,owner,pool,cadence,concentration)
        self.world=world
        self.lifecycle=PayloadConcentration(owner,concentration,
            captures.acquired.supplements['SUP-07']['copyProfileContract']['profiles'],world)
        self.selections={}

    def snapshot(self):
        return {**super().snapshot(),'selections':deepcopy(self.selections),'world':self.world.snapshot()}

    def _component(self,capture_event,permission):
        record=self.captures.pending if permission=='pending' else self.captures.adapted.get(capture_event) if permission=='adapted' else None
        require(record is not None,'Actual captured permission required')
        return record['component']

    def _selection(self, component, selection, *, preflight):
        profile=component['profile']
        require(isinstance(selection,dict),'Explicit bounded-profile selection required')
        if profile=='step':
            require(set(selection)=={'destination','distanceFeet','visible','fitting','unoccupied','lineOfEffect','teleportAllowed'},'Exact personal teleport selection required')
            require(component.get('wasTeleport') is True,'Only the actually witnessed Mist Step teleport is integrated')
            require(isinstance(selection['destination'],list) and len(selection['destination'])==3 and all(type(n) is int for n in selection['destination']),'Finite actual destination coordinates required')
            integer(selection['distanceFeet'],'actual body-to-destination distance')
            limit=min(15,component['observedDistance']//2)
            legal=selection['distanceFeet']<=limit and all(selection[k] is True for k in ['visible','fitting','unoccupied','lineOfEffect','teleportAllowed'])
            if preflight:require(legal,'Known legal visible fitting personal teleport destination required')
            return [self.owner] if legal else []
        fields={'targets','statistic'} if profile=='boon' else {'targets','area'} if profile=='burst' else {'targets'}
        require(set(selection)==fields,'Exact bounded target/area/statistic selection required')
        targets=selection['targets'];require(isinstance(targets,list) and all(isinstance(t,str) for t in targets) and len(set(targets))==len(targets),'Distinct declared target identities required')
        require(1<=len(targets)<=3 if profile=='burst' else len(targets)==1,'Printed target count exceeded')
        if profile=='boon':
            require(selection['statistic'] in component['benefitedStatistics'],'Only a statistic actually benefited by this witnessed source may be chosen')
            require(selection['statistic']=='AC','Current Shield source adapter supplies AC only; next-attack/save source adapters remain open')
        area=None
        if profile=='burst':
            area=selection['area']
            require(isinstance(area,dict) and set(area)=={'id','distanceFeet','knownPoint','lineOfEffect'},'Actual declared area query required')
            integer(area['distanceFeet'],'actual casting-point distance')
            if not (area['distanceFeet']<=30 and area['knownPoint'] is True and area['lineOfEffect'] is True):
                if preflight:raise ValueError('Legal area point within30 feet required')
                return []
        legal=[]
        for target in targets:
            actor=self.world.actors.get(target);obs=self.world.observations.get((self.owner,target))
            require(actor is not None and obs is not None,'Actual target and spatial/perception observation required')
            integer(obs['distanceFeet'],'actual target distance')
            good=actor['creature'] is True and not actor['life'].dead and obs['perceived'] is True
            if profile=='burst':
                query=obs['areas'].get(area['id'])
                require(query is not None,'Declared-area occupied-body query required')
                integer(query['distanceFeet'],'actual area-to-body distance')
                good=good and query['distanceFeet']<=10 and query['lineOfEffect'] is True
            else:good=good and obs['distanceFeet']<=(60 if profile=='strike' else 30) and obs['lineOfEffect'] is True
            if profile in {'mend','ward'}:good=good and actor['living'] is True and actor['willing'] is True
            if profile=='boon':good=good and actor['willing'] is True
            if preflight:require(good,'Known target eligibility/range/perception/line of effect failed')
            if good:legal.append(target)
        return legal

    def declare(self,event,capture_event,*,permission,grant_id,frame,selection):
        component=self._component(capture_event,permission)
        self._selection(component,selection,preflight=True)
        owner=self.world.actors[self.owner]
        for frame_key,world_key in [('conscious','conscious'),('canAct','canAct'),('magicAllowed','magicAllowed'),('verbal','verbalAvailable'),('somatic','somaticAvailable')]:
            require(frame[frame_key] is owner[world_key],'Action frame must use canonical caster body state')
        for target in selection.get('targets',[]):
            actor=self.world.actors[target]
            # Named replacement/redirect/next-heal integrations need their own
            # real interruption and source-use engines, not Boolean free grants.
            require(actor['unsupportedInterceptors']==[],'Unintegrated active interceptors require their actual adapters')
            if component['profile']=='mend':
                require(not any(r.next_healing for r in actor['healingReductions']),'Next-healing consumption needs its source-owned adapter')
        receipt=super().commit(event,capture_event,permission=permission,grant_id=grant_id,frame=frame)
        self.selections[event]={'declared':deepcopy(selection),'current':deepcopy(selection),'declaredAt':self.world.now}
        return receipt

    def _deadline(self, profile, target):
        owner=self.world.actors[self.owner];now=self.world.now.seconds
        second_start=regular_control_endpoint(now,owner['regularStartPhase'],count=2,boundary='start')
        if profile=='ward':return second_start
        if profile=='hindrance':
            actor=self.world.actors[target]
            end=regular_control_endpoint(now,actor['regularEndPhase'],boundary='end',excluded_current_marker=actor['inProgressRegularEnd'])
            return min(end,second_start)
        return regular_control_endpoint(now,owner['regularEndPhase'],boundary='end',excluded_current_marker=owner['inProgressRegularEnd'])

    def _damage(self, target, amount, damage_type, event, options, preview_buffers):
        actor=self.world.actors[target];life=actor['life']
        integer(actor['flatDamageReduction'],'current strongest flat reduction')
        reduced=max(0,amount-actor['flatDamageReduction'])
        if damage_type in actor['damageImmunities']:reduced=0
        elif damage_type in actor['damageResistances']:reduced//=2
        require(set(options)=={'constitutionSaveModifier','woundNatural','injuryD6','critical'},'Exact Core damage operands required')
        require(type(options['critical']) is bool,'Actual critical classification required')
        result,details=preview_buffers.core_damage(target,self.owner+'::'+event,life,reduced,now=self.world.now,
            constitution_save_modifier=options['constitutionSaveModifier'],wound_natural=options['woundNatural'],
            injury_d6=options['injuryD6'],critical=options['critical'],now_seconds=int(self.world.now.seconds))
        return result,{'damageType':damage_type,'afterSave':amount,'afterDefenses':reduced,
                       'actualHpLost':life.hp-result.hp,**details}

    def _owner_can_resolve(self):
        return all(self.world.actors[self.owner][k] is True
                   for k in ['magicAllowed', 'conscious', 'canAct'])

    def resolve(self,event,*,countered=False,rolls=None):
        require(type(countered) is bool,'Actual counter result required')
        # CFI-03: reject unintegrated native concentration drift before any
        # payload, buffer, clock or lifecycle mutation. Do not overwrite it.
        validate = getattr(self.lifecycle.ledger, 'validate_current', None)
        if validate: validate()
        cast=self.casts.get(event);state=self.lifecycle.casts.get(event);key=(self.owner,event)
        require(cast is not None and state is not None and event in self.selections and key not in self.world.resolutions,'One unresolved actual paid cast required')
        require('counterWindowOutcome' not in state and state['state'] in {'committed','ended'},'Counter window already resolved outside this integrated adapter')
        profile=cast['component']['profile'];selection=self.selections[event]['current'];rolls={} if rolls is None else rolls
        require(isinstance(rolls,dict),'Actual profile RNG operands required')
        if countered or state['state']=='ended' or not self._owner_can_resolve():
            require(not rolls,'Blocked payload consumes no attack/save/damage RNG here')
            self.lifecycle.after_counter_window(event,countered=countered)
            result={'resolved':False,'reason':'countered' if countered else 'concentration-ended-or-magic-blocked','refund':0}
        else:
            # Current scene queries may change, but declarations cannot retarget.
            declared=self.selections[event]['declared']
            fixed=('targets','statistic') if profile=='boon' else ('targets',) if profile!='step' else ('destination',)
            require(all(selection.get(k)==declared.get(k) for k in fixed),'Cannot retarget the paid cast')
            if profile=='burst':require(selection['area']['id']==declared['area']['id'],'Cannot change the declared area')
            eligible=self._selection(cast['component'],selection,preflight=False)
            if not eligible:
                require(not rolls,'No eligible recipient means no payload RNG')
                self.lifecycle.after_counter_window(event,countered=False)
                result={'resolved':False,'reason':'declared-recipients-no-longer-eligible','refund':0}
            else:
                result=self._payload(event,cast,selection,eligible,rolls)
        self.world.resolutions[key]=deepcopy(result)
        self.casts[event]['recipientPayloadExecuted']=result['resolved']
        self.casts[event]['payloadResult']=deepcopy(result)
        return deepcopy(result)

    def _payload(self,event,cast,selection,eligible,rolls):
        component=cast['component'];profile=component['profile'];owner=self.owner;world=self.world
        effect_id=owner+'::feat-copy::'+event;updates={};results={};effect=None;speed=None;offer=None
        preview=deepcopy(world.buffers);native=None
        for target in eligible:
            require(world.actors[target]['unsupportedInterceptors']==[],'Resolve newly active actual interceptors through their source adapters first')
        if profile=='mend':
            require(not any(r.next_healing for r in world.actors[eligible[0]]['healingReductions']),'New next-healing source needs its actual consumption adapter')
        if profile in {'strike','burst','mend','ward'}:
            required={'nativeDice','targets'} if profile in {'strike','burst'} else {'nativeDice'}
            require(set(rolls)==required,'Exact native-copy and target RNG required')
            if profile=='strike':
                target=eligible[0];actor=world.actors[target]
                require(set(rolls['targets'])=={target},'One actual target roll required')
                inputs=rolls['targets'][target];require(set(inputs)=={'faces','core'},'Exact strike attack/Core operands required')
                attack=attack_roll(selected_d20(inputs['faces'],actor['incomingAttackRollMode']),cast['spellAttack'],world.ac(target))
                if not attack['hit']:
                    require(rolls['nativeDice']==[] and inputs['core'] is None,'Miss has no damage or Wound RNG')
                    results[target]={'attack':attack,'actualHpLost':0}
                else:
                    native=bounded_native_numeric(component,rolls['nativeDice'])
                    require(inputs['core']['critical']==attack['critical'],'Actual critical status required; critical adds no copy damage dice')
                    updates[target],details=self._damage(target,native,component['damageType'],event,inputs['core'],preview)
                    results[target]={'attack':attack,**details}
            elif profile=='burst':
                require(set(rolls['targets'])==set(eligible),'Exactly the eligible declared recipient saves required')
                native=bounded_native_numeric(component,rolls['nativeDice'])
                for target in eligible:
                    inputs=rolls['targets'][target];actor=world.actors[target]
                    require(set(inputs)=={'faces','core'},'Exact Burst save/Core operands required')
                    save=saving_throw(selected_d20(inputs['faces'],actor['dexSaveRollMode']),actor['dexSaveModifier'],cast['spellDC'])
                    require(inputs['core']['critical'] is False,'Area save damage is not a critical attack')
                    updates[target],details=self._damage(target,native//2 if save['success'] else native,component['damageType'],event,inputs['core'],preview)
                    results[target]={'save':save,**details}
            else:
                target=eligible[0];actor=world.actors[target];native=bounded_native_numeric(component,rolls['nativeDice'])
                if profile=='mend':
                    packet=healing_packet(actor['life'],native,dice_count=component['copyRank']+1,
                        systemic_factors=actor['healingSystemicFactors'],reductions=actor['healingReductions'],
                        hp_gain_prohibited=actor['hpGainProhibited'])
                    updates[target]=packet.pop('state');results[target]=packet
                else:
                    deadline=self._deadline(profile,target)
                    grant=BufferGrant(effect_id,'feat-copy::'+component['sourceSpellId'],owner,target,native,
                        expiry=deadline,dependencies=(effect_id,))
                    offer=preview.offer(grant,world.now);results[target]={'offer':offer}
                    if offer['accepted']:
                        effect={'id':effect_id,'cast':event,'owner':owner,'target':target,'profile':profile,'deadline':deadline,'active':True}
        elif profile=='hindrance':
            require(set(rolls)=={'faces'},'One actual WIS save required')
            target=eligible[0];actor=world.actors[target]
            save=saving_throw(selected_d20(rolls['faces'],actor['wisSaveRollMode']),actor['wisSaveModifier'],cast['spellDC'])
            results[target]={'save':save,'controlImmune':actor['copyHindranceImmune']}
            if not save['success'] and not actor['copyHindranceImmune']:
                deadline=self._deadline(profile,target)
                effect={'id':effect_id,'cast':event,'owner':owner,'target':target,'profile':profile,'deadline':deadline,'active':True}
                speed=SpeedRecord(effect_id,owner,target,'feat-copy-hindrance','flat-minus10','flat',amount=10,expires=deadline)
        elif profile=='boon':
            require(not rolls,'The actual +1 AC copy has no RNG')
            target=eligible[0];deadline=self._deadline(profile,target)
            effect={'id':effect_id,'cast':event,'owner':owner,'target':target,'profile':profile,'statistic':'AC','deadline':deadline,'active':True}
            results[target]={'statistic':'AC','bonus':1}
        elif profile=='step':
            require(not rolls,'The actual personal teleport has no RNG')
            results[owner]={'positionBefore':deepcopy(world.actors[owner]['position']),
                            'positionAfter':deepcopy(selection['destination']),'teleport':True,'passengers':[]}
        # All fallible computations have completed on previews. Commit once to
        # the same canonical objects; never replace a held LifeState reference.
        world.buffers.__dict__.clear();world.buffers.__dict__.update(preview.__dict__)
        for target,life in updates.items():world.actors[target]['life'].__dict__.update(deepcopy(life.__dict__))
        if effect:world.effects[effect_id]=effect
        if speed:world.speed_records.append(speed)
        if profile=='step':world.actors[owner]['position'][:]=selection['destination']
        world.projection()
        self.lifecycle.after_counter_window(event,countered=False,effect_established=effect is not None)
        return {'resolved':True,'profile':profile,'nativeBoundedAmount':native,'targets':results,
            'effectId':effect_id if effect else None,'refund':0,'resourceConversionAllowed':False,
            'furtherCopyAllowed':False,'externalAmplificationApplied':False}
