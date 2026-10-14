"""Selected paid Stone totems and the ordinary Shaman step5 vent interface.

This finite adapter executes actual Base selection, Totem Casting's object/
concentration lifecycle, ordinary/copy casting and the clarified strain order.
Stone's damage/shove benefits and other profiles are not exercised here.
"""
from copy import deepcopy
import math
from di7_cast_transactions import DI7Sources
from di7_alignment_clock import ClockedFateTransactions
from apply_di7_ap_as_01 import G,R,info
from control_playtest_rules import regular_control_endpoint


class ShamanSources(DI7Sources):
    def spell(self,sid,provider):
        if sid!='detect-poison': return super().spell(sid,provider)
        source=self.ordinary[sid]
        if provider!='Shaman' or source['status']!='operational-playtest-draft' or source['classAccess'][provider]['rank']!=0 or source['classAccess'][provider]['school']!='Divination':
            raise ValueError('Only the actual Shaman rank0 Detect Poison adapter is supplied')
        return deepcopy(source),deepcopy(source['operational']),{**info(self.catalog_path),'pointer':'/spells/'+str(self.catalog['spells'].index(source))},False


class ShamanTransactions(ClockedFateTransactions):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.selected_kits={}; self.cantrips={}; self.totems={}; self.vent_uses={}; self.vent_events=[]; self.extra_actions={}
        self.ready_vent_context=None
        self.round_origin=self.world['roundClock']['origin']
        if not self.world['roundClock']['authorityEvent']: raise ValueError('Actual source-governed six-second round clock required')

    def snapshot(self):
        return {**super().snapshot(),'selectedBaseKits':deepcopy(self.selected_kits),'cantripLearning':deepcopy(self.cantrips),
            'totems':deepcopy(self.totems),'ventUses':deepcopy(self.vent_uses),'ventEvents':deepcopy(self.vent_events),'extraActions':deepcopy(self.extra_actions)}

    def round_key(self): return str(math.floor((self.now-self.round_origin)/6))
    def burden(self,actor): return 'totem-concentration/'+actor

    def select_base_kit(self,actor,ids,event,*,affinity='Earth'):
        a=self.actors[actor]; source=self.sources.classes['Shaman']; schedule=source['schedule'][0]
        if a['provider']!='Shaman' or actor in self.selected_kits or not event or any(x.get('event')==event for x in self.events):
            raise ValueError('One actual Shaman Base selection opportunity required')
        cards={c['id']:c for c in source['cards']}
        if len(ids)!=schedule['choose'] or len(set(ids))!=len(ids) or any(i not in cards for i in ids): raise ValueError('Exact distinct Base choice count required')
        chosen=[cards[i] for i in ids]
        if any(c['acquisition']!='selection' or c['band'] not in schedule['bands'] or c['minimumClassLevel']>1 for c in chosen) or sum(c['sourceKind']=='active' for c in chosen)<schedule['minimumActives']:
            raise ValueError('Actual first-level Base prerequisites and minimum active choices required')
        if affinity not in {'Fire','Ice','Air','Earth'}: raise ValueError('Actual automatic Elemental Affinity choice required')
        path=G/self.sources.chassis['Shaman']['classCandidatePath']
        self.selected_kits[actor]={'atClassLevel':1,'event':event,'choices':deepcopy(ids),'affinity':affinity,'sourceBinding':info(path),
            'cardBindings':[{**info(path),'pointer':'/cards/'+str(source['cards'].index(c))} for c in chosen]}
        self.events.append({'event':event,'kind':'actual-conditional-Base-selection','actor':actor,'chosen':deepcopy(ids)})

    def learn_cantrip(self,actor,sid,event):
        a=self.actors[actor]; card,op,binding,_=self.sources.spell(sid,a['provider'])
        if a['provider']!='Shaman' or sid!='detect-poison' or card['classAccess']['Shaman']['minimumClassLevel']>1 or self.sources.chassis['Shaman']['weaveTier']=='full':
            raise ValueError('This finite adapter uses Shaman first-access hybrid cantrip selection only')
        if not event or any(x.get('event')==event for x in self.events) or sid in self.cantrips.get(actor,{}) or len(self.cantrips.get(actor,{}))>=2:
            raise ValueError('Unspent actual first-access cantrip choice required')
        self.cantrips.setdefault(actor,{})[sid]={'event':event,'atClassLevel':1,'sourceBinding':binding,'rank':0,'allowanceAtFirstAccess':2}
        self.events.append({'event':event,'kind':'actual-conditional-cantrip-selection','actor':actor,'spellId':sid})

    def route(self,actor,sid):
        if sid!='detect-poison': return super().route(actor,sid)
        a=self.actors[actor]; result=self.sources.spell(sid,a['provider']); credential=self.cantrips.get(actor,{}).get(sid)
        if not credential or credential['sourceBinding']!=result[2] or not a['providerRetained'] or a['heroPath']=='Bloodcaller':
            raise ValueError('Actual retained acquired ordinary Shaman cantrip required')
        return result

    def _target(self,actor,sid,request,op):
        if sid=='detect-poison':
            target=self._line(actor,request.get('target'),30)
            if target['kind'] not in {'creature','object'}: raise ValueError('Actual perceived creature/object required')
            return
        return super()._target(actor,sid,request,op)

    def _live(self,totem):
        a=self.actors[totem['owner']]
        return totem['state']=='active' and self.now<totem['deadline'] and totem['hp']>0 and a['concentration']==self.burden(totem['owner']) and a['body']['conscious'] and a['body']['canAct']

    def _qualifying_aura(self,actor):
        a=self.actors[actor]
        for tid,t in self.totems.items():
            if t['owner']!=actor or not self._live(t) or t['suppressed'] or abs(a['positionFeet']-t['positionFeet'])>15: continue
            relation=self.world['auraLines'].get(actor+'>'+tid)
            if relation and relation['authorityEvent'] and relation['lineOfEffect']: return tid
        return None

    def _vent_qualifies(self,actor,op,*,ready=False):
        a=self.actors[actor]
        return (a['provider']=='Shaman' and a['providerRetained'] and a['heroPath']!='Bloodcaller' and not op['concentration'] and not ready
            and self.round_key() not in self.vent_uses.get(actor,{}) and self._qualifying_aura(actor) is not None)

    def _quote(self,actor,sid,*,state=None,copied_from=None,rp=None):
        quote,strain,op,binding=super()._quote(actor,sid,state=state,copied_from=copied_from,rp=rp)
        ready=self.ready_vent_context==actor
        if not copied_from and self._vent_qualifies(actor,op,ready=ready): strain=max(0,strain-1)
        return quote,strain,op,binding

    def _end_totem(self,tid,reason,at=None):
        t=self.totems[tid]
        if t['state']=='active': t.update(state='ended',endedAt=self.now if at is None else at,endReason=reason)

    def _sync_totems(self):
        for tid,t in self.totems.items():
            if t['state']!='active': continue
            a=self.actors[t['owner']]
            if self.now>=t['deadline']: self._end_totem(tid,'original-duration-expiry',t['deadline'])
            elif t['hp']<=0: self._end_totem(tid,'actual-object-destruction')
            elif a['concentration']!=self.burden(t['owner']): self._end_totem(tid,'concentration-displaced')
            elif not a['body']['conscious'] or not a['body']['canAct']: self._end_totem(tid,'source-incapacity-concentration-loss')
        for actor,a in self.actors.items():
            if a['concentration']==self.burden(actor) and not any(t['owner']==actor and t['state']=='active' for t in self.totems.values()): a['concentration']=None

    def advance(self,now):
        super().advance(now)
        if hasattr(self,'totems'): self._sync_totems()

    def cast_totem(self,actor,tid,site,*,replace=None):
        a=self.actors[actor]; kit=self.selected_kits.get(actor); spot=self.world['totemSites'].get(site)
        if a['provider']!='Shaman' or not kit or 'shaman.base.totem-casting' not in kit['choices'] or kit['sourceBinding']!=info(G/self.sources.chassis['Shaman']['classCandidatePath']):
            raise ValueError('Actually selected retained Totem Casting required')
        if tid in self.totems or self.stack or self.active_actor!=actor or a['actions']<1 or not a['body']['conscious'] or not a['body']['canAct']:
            raise ValueError('Actual available own Action and legal acting body required')
        if not spot or not spot['authorityEvent'] or not spot['perceived'] or not spot['lineOfEffect'] or not spot['groundSupportsTinyObject'] or spot['occupiedByCreature'] or abs(a['positionFeet']-spot['positionFeet'])>30:
            raise ValueError('Actual legal visible supported unoccupied local totem site required')
        if a['rp']-self.reserved(actor)<2: raise ValueError('Actual unreserved2 RP required')
        current=[t['id'] for t in self.totems.values() if t['owner']==actor and self._live(t)]
        capacity=2 if a['classLevel']>=13 else 1
        if len(current)>=capacity and replace not in current: raise ValueError('Capacity needs an explicit existing own replacement')
        if replace is not None and replace not in current: raise ValueError('Actual own live replacement required')
        if self.alignment.mode=='initiative-virtual-source-start':
            if actor not in self.alignment.schedule: raise ValueError('Actual original source-start schedule required')
            deadline=float(regular_control_endpoint(self.now,self.alignment.schedule[actor],count=3,boundary='start').seconds)
        else: deadline=self.now+18
        a['actions']-=1; a['rp']-=2
        if replace: self._end_totem(replace,'capacity-replacement-no-refund')
        prior=a['concentration']
        if prior and prior!=self.burden(actor): a['endConcentrationHistory'].append({'id':prior,'reason':'actual-Totem-Casting','replacedBy':self.burden(actor),'at':self.now})
        a['concentration']=self.burden(actor); self._sync_alignment_concentration(); self._expire_lost_holds()
        pb=2+(a['totalLevel']-1)//4
        self.totems[tid]={'id':tid,'owner':actor,'profile':'Stone','state':'active','positionFeet':spot['positionFeet'],'radiusFeet':15,
            'createdAt':self.now,'deadline':deadline,'hp':2*a['classLevel'],'maximumHP':2*a['classLevel'],'ac':12+pb,'size':'Tiny',
            'magical':True,'visible':True,'immobile':True,'suppressed':False,'conditionsImmune':True,'damageImmunities':['poison','psychic'],
            'sourceBinding':deepcopy(kit['sourceBinding']),'selectedFeature':'shaman.base.totem-casting','paidRP':2,
            'stoneBeneficiaries':[actor],'stoneDamageAndShoveBenefitsExecuted':False}
        self.events.append({'event':'totem/'+tid,'kind':'paid-selected-Totem-Casting','actor':actor,'at':self.now,'rp':2,'ordinarySpell':False})
        return deepcopy(self.totems[tid])

    def declare(self,actor,sid,cast_id,request):
        ready=sid=='fate-echo' and request.get('readyTrigger') is not None
        super().declare(actor,sid,cast_id,request)
        cast=self.casts[cast_id]; a=self.actors[actor]
        if ready:
            prior=a['concentration']
            if prior and prior!=cast_id: a['endConcentrationHistory'].append({'id':prior,'reason':'Ready-held-spell-commit','replacedBy':cast_id,'at':self.now})
            a['concentration']=cast_id; cast['readyHoldConcentrationAtCommit']=True
            self._sync_alignment_concentration()
        self._sync_totems()
        _,op,_,_=self.sources.spell(sid,a['provider'])
        if self._vent_qualifies(actor,op,ready=ready):
            aura=self._qualifying_aura(actor); raw=cast['dissonanceAdded']; reduction=min(1,raw)
            self.vent_uses.setdefault(actor,{})[self.round_key()]={'castId':cast_id,'at':self.now,'auraAtCheckpoint':aura,'generatedBefore':raw,'reduction':reduction}
            a['dissonance']-=reduction; cast['dissonanceAdded']-=reduction; cast['classHooks'].append('Shaman-own-active-totem-step5-first-ordinary-cast')
            self.vent_events.append({'actor':actor,'castId':cast_id,'round':self.round_key(),'at':self.now,'auraAtStep5':aura,'generatedBefore':raw,'reduction':reduction,'rpReduction':0})
        cast['afterCommit']={k:deepcopy(a[k]) for k in cast['before']}
        return deepcopy(cast)

    def begin_fate(self,actor,cast_id,original_id,request=None,*,ready_trigger=None):
        if ready_trigger is None: return super().begin_fate(actor,cast_id,original_id,request)
        # Explicit Ready variant of the existing parent sequence: all forecast
        # checks precede commitment; the held concentration is set in declare
        # before this layer's vent checkpoint, never after beginning strain.
        if cast_id in self.casts or self.stack or actor in self.holds: raise ValueError('Unique unheld outer cast required')
        if not isinstance(ready_trigger,str) or not ready_trigger: raise ValueError('Specific perceivable trigger required')
        self._admit_original(actor,original_id,freshness=True); a=self.actors[actor]
        self.ready_vent_context=actor
        try:
            quote,strain,op,_=self._quote(actor,'fate-echo'); self._components(actor,op)
            if a['actions']<1 or a['turnId'] is None or self.active_actor!=actor: raise ValueError('Actual own Action required')
            forecast={'dissonance':a['dissonance']+strain,'previousSpell':'fate-echo','refrain':quote['refrain']}
            child_quote,child_strain,_,_=self._child_check(actor,original_id,{},state=forecast,rp=a['rp']-quote['cost']-self.reserved(actor),targets=False)
            self.fate_admission_context=(actor,original_id)
            try: paid=self.declare(actor,'fate-echo',cast_id,{'originalCast':original_id,'childRequest':None,'readyTrigger':ready_trigger})
            finally: self.fate_admission_context=None
            assert paid['quote']==quote and paid['dissonanceAdded']==strain
            self.reservations[cast_id]={'actor':actor,'rp':child_quote['cost'],'kind':'unspent-exclusive-child-reservation','reservedAt':self.now,'materials':[],'independentUses':[],
                'sourceQualification':'Complete admitted Fate Coin/Suggestion modes have no independent consumed stock; no generic waiver.'}
            self.composites[cast_id]={'actor':actor,'originalCast':original_id,'request':None,'forecast':forecast,'forecastChildQuote':child_quote,
                'forecastChildStrain':child_strain,'selectedAt':self.now,'originalAgeAtSelection':self.now-self.casts[original_id]['castingCompletedAt'],
                'readyTrigger':ready_trigger,'state':'outer-pending'}
            return deepcopy(self.composites[cast_id])
        finally: self.ready_vent_context=None

    def _commit_child(self,outer_id,request):
        result=super()._commit_child(outer_id,request); self._sync_totems(); return result

    def resolve_counter(self,*args,**kwargs):
        result=super().resolve_counter(*args,**kwargs); self._sync_totems(); return result

    def suppress_totem(self,tid,suppressed):
        if type(suppressed) is not bool or self.totems[tid]['state']!='active': raise ValueError('Actual live totem and suppression state required')
        self.totems[tid]['suppressed']=suppressed

    def resolve_detect_poison(self,cast_id):
        cast=self.casts[cast_id]
        if cast['spellId']!='detect-poison': raise ValueError('Actual paid acquired cantrip required')
        receipt=self.take_payload_resolution(cast_id)
        if receipt['status']!='ready-for-payload': return None
        try: target=self._line(cast['actor'],cast['request']['target'],30)
        except ValueError:
            cast.update(status='failed-target-no-refund',resolvedAt=self.now); return None
        records=target['actualPoisonRecords']
        if not target['poisonHistoryAuthority'] or not target['explicitPoisonAbsenceOrCompleteRecords']:
            raise ValueError('Explicit actual poison/absence premise required; no invented negative diagnosis')
        if any(not r.get('authorityEvent') or not r.get('sourceVersion') for r in records): raise ValueError('Actual source-linked poison records required')
        answer={'containsPoison':any(r['active'] and r['poisonLinked'] for r in records)}
        cast.update(status='resolved',resolvedAt=self.now,castingCompletedAt=self.now,privateResult=answer)
        return deepcopy(answer)

    def conditional_extra_action(self,actor,event):
        key=actor+'/'+self.round_key()
        if not event.get('authorityEvent') or not event.get('sourceVersion') or not event.get('actualLegalGrant') or key in self.extra_actions or self.stack or self.active_actor!=actor:
            raise ValueError('One separately legal source-qualified extra Action per creature per round required')
        self.extra_actions[key]=deepcopy(event); self.actors[actor]['actions']+=1
