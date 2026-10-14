"""Nature's Whisper activation/check transactions under NWQ01–04.

The world, observation, native card selection, task permission and interrupt
facts are conditional fixtures. Source and actor records constrain them; the
records themselves never authenticate that a campaign event actually happened.
"""
from copy import deepcopy
from core_playtest_rules import task_check
from feat_exact_01_acquisition_models import pb
from feat335_borrowed_skill_transactions import BorrowedSkillTransactions

NATURE='ranger.base.nature-s-whisper'


class NativeNatureActor:
    def __init__(self, acquired, world):
        self.acquired=acquired;self.world=deepcopy(world);self.now=0;self.turn=None;self.round=None
        self.actions=0;self.bonus_actions=0;self.cooldowns={};self.pending=None;self.events={};self.turns=set()

    def advance(self,now):
        if type(now) is not int or now<self.now:raise ValueError('Monotonic clock required')
        self.now=now

    def begin_turn(self,identity,round_id,now,*,regular=True):
        if self.pending or identity in self.turns:raise ValueError('No pending action or replayed turn')
        self.advance(now);self.turns.add(identity);self.turn=identity;self.round=round_id
        self.actions=1;self.bonus_actions=1
        if regular:self.cooldowns={k:max(0,v-1) for k,v in self.cooldowns.items()}

    def snapshot(self):
        return {'acquisition':self.acquired.snapshot(),'world':deepcopy(self.world),'now':self.now,
            'turn':self.turn,'round':self.round,'actions':self.actions,'bonusActions':self.bonus_actions,
            'cooldowns':deepcopy(self.cooldowns),'pending':deepcopy(self.pending),'events':deepcopy(self.events),'turns':sorted(self.turns)}


class NatureBorrowedTransactions(BorrowedSkillTransactions):
    def complete_prepare(self,now,*,uninterrupted):
        result=super().complete_prepare(now,uninterrupted=uninterrupted)
        if result:self.prepared.update(completedAt=now,elapsedSeconds=now-self.prepared['start'])
        return result

    def nature_whisper(self,*args,**kwargs):
        raise ValueError('Use the NWQ source-bound split Nature procedure; old clearance adapter is historical')

    def use_nature_advantage(self,*args,**kwargs):
        raise ValueError('Use the NWQ separate paid check declaration before faces')


class NatureTransactions:
    def __init__(self,actor,class_sources,authority,*,native_selection=None,spell_history=None):
        self.actor=actor;self.acquired=actor.acquired;self.class_sources=class_sources
        self.card=next(c for c in class_sources['Ranger']['cards'] if c['id']==NATURE)
        if (authority['reviewId']!='FEAT335-NATURE-SOURCE-CHECK-01' or
            authority['effect']!=self.card['effect'] or self.card['spellRank'] is not None or
            self.card['cost']!='1 RP' or self.card['frequency']!='Recharge 3' or
            'magical nonspell class technique' not in self.card['effect']):
            raise ValueError('Exact current Nature source and controlling addendum required')
        self.authority=deepcopy(authority);self.native_selection=deepcopy(native_selection)
        if native_selection is not None:
            if self.acquired.first!='Ranger' or self.acquired.pay.current_classes.get('Ranger',0)<1:
                raise ValueError('Actual Ranger class level required')
            cards={c['id']:c for c in class_sources['Ranger']['cards']};schedule=class_sources['Ranger']['schedule'][0]
            selected=native_selection['selectedAtClassLevel1']
            if len(selected)!=schedule['choose'] or len(set(selected))!=len(selected) or NATURE not in selected:
                raise ValueError('Actual native level1 card choices required')
            if any(cards[s]['minimumClassLevel']>1 or cards[s]['band'] not in schedule['bands'] or cards[s]['acquisition']!='selection' for s in selected):
                raise ValueError('Unavailable native selection')
            if sum(cards[s]['sourceKind']=='active' for s in selected)<schedule['minimumActives']:
                raise ValueError('Native minimum active choices required')
        self.spell_history=deepcopy(spell_history or {'dissonance':0,'previousSpell':None,'refrain':0,'classRecords':{}})
        self.rider=None;self.rider_history=[];self.tasks={};self.ready=None;self.reactions=1
        self.regular_ordinal=0;self.turn_meta={};self.idle_ticks=set();self.magical_turns=set();self.clock_ticks={}
        self.next_elapsed_recharge=None;self.version=0;self.history=[]

    @property
    def owner(self):return self.actor.world['owner']

    def snapshot(self):
        return {'actor':self.actor.snapshot(),'authority':deepcopy(self.authority),'nativeSelection':deepcopy(self.native_selection),
            'spellHistory':deepcopy(self.spell_history),'rider':deepcopy(self.rider),'riderHistory':deepcopy(self.rider_history),
            'tasks':deepcopy(self.tasks),'ready':deepcopy(self.ready),'reactions':self.reactions,'regularOrdinal':self.regular_ordinal,
            'turnMeta':deepcopy(self.turn_meta),'idleTicks':sorted(self.idle_ticks),'magicalTurns':sorted(self.magical_turns),
            'clockTicks':deepcopy(self.clock_ticks),'nextElapsedRecharge':self.next_elapsed_recharge,'version':self.version,'history':deepcopy(self.history)}

    def advance(self,now,*,outside_initiative=False):
        if type(now) is not int or now<self.actor.now:raise ValueError('Monotonic actual time required')
        self.actor.advance(now)
        if outside_initiative and self.next_elapsed_recharge is not None:
            while self.next_elapsed_recharge<=now and self.actor.cooldowns.get(NATURE,0)>0:
                t=self.next_elapsed_recharge
                if t not in self.clock_ticks:
                    self.actor.cooldowns[NATURE]-=1;self.clock_ticks[t]='outside-six-second-boundary'
                self.next_elapsed_recharge+=6
        if self.rider and self.rider['state']=='unused' and now>=self.rider['deadline']:
            self.rider['state']='expired';self.rider_history.append(deepcopy(self.rider));self.rider=None
        for r in self.spell_history.get('classRecords',{}).values():
            if isinstance(r,dict) and r.get('active') and 'deadline' in r and now>=r['deadline']:r['active']=False

    def begin_turn(self,identity,round_id,now,*,regular=True):
        if self.actor.pending or self.actor.turn is not None or identity in self.actor.turns:raise ValueError('Pending operation, unfinished current turn or reused turn')
        before=self.actor.cooldowns.get(NATURE,0)
        self.advance(now)
        self.actor.begin_turn(identity,round_id,now,regular=regular)
        if regular:
            self.regular_ordinal+=1;self.reactions=1
            if before>0:
                if now in self.clock_ticks:self.actor.cooldowns[NATURE]=before
                else:self.clock_ticks[now]='regular-start'
                self.next_elapsed_recharge=now+6
            if self.ready:
                self.actor.events[self.ready['event']]['status']='ready-expired';self.ready=None
        self.turn_meta[identity]={'regular':regular,'ordinal':self.regular_ordinal,'ended':False,'beganAt':now}

    def end_turn(self,identity,*,actual_end,otherwise_idle=True):
        meta=self.turn_meta.get(identity)
        if not actual_end or not meta or meta['ended'] or self.actor.turn!=identity or self.actor.pending:
            raise ValueError('Actual complete current turn required')
        before=self.spell_history['dissonance'];meta['ended']=True
        if meta['regular']:
            if identity in self.idle_ticks:raise ValueError('Idle tick cannot replay')
            self.idle_ticks.add(identity)
            if otherwise_idle and identity not in self.magical_turns:self.spell_history['dissonance']=max(0,before-1)
        self.actor.turn=None
        return {'before':before,'after':self.spell_history['dissonance'],'regularTick':meta['regular']}

    def _area(self,area_id,footprint=None):
        area=self.actor.world['areas'].get(area_id)
        if not area or not area['cells']:raise ValueError('Actual nonempty natural investigation area required')
        current={cid:self.actor.world['terrain'][cid]['position'] for cid in area['cells']}
        if footprint is not None and current!=footprint:raise ValueError('Original fixed area cannot be moved or replaced')
        for cid,pos in current.items():
            cell=self.actor.world['terrain'][cid]
            if not cell['natural'] or abs(pos-self.owner['position'])>15 or not cell['activationPerceived'] or not cell['activationLine']:
                raise ValueError('Actual natural terrain, perception, line and within15ft range required')
        return current

    def _pool(self):
        first=self.acquired.first;level=self.acquired.pay.current_classes[first]
        maximum=self.class_sources[first]['rpByClassLevel'][level-1]
        if self.owner['poolKind']!='personal-RP' or self.owner['poolOwner']!='owner' or maximum<1:
            raise ValueError('Existing actual personal class RP pool required')
        current=self.owner['personalRP']
        if type(current) is not int or not 1<=current<=maximum:raise ValueError('Actual available personal RP within source capacity required')
        return {'class':first,'classLevel':level,'maximum':maximum,'currentBefore':current}

    def _signal(self,signal_id,donor_id):
        signal=self.actor.world['signals'].get(signal_id);donor=self.actor.donors[donor_id]
        if not signal or signal['donor']!=donor_id or not signal['actorCanProduce'] or not signal['donorCanPerceive']:
            raise ValueError('Actual physically possible donor signal required')
        if not signal['sharedMeaningRecord'] or signal['sharedMeaningRecord'] not in self.actor.world['agreedSignals']:
            raise ValueError('Existing shared signal meaning required, no invented channel')
        if signal['kind']=='audible':
            if self.owner['silenced'] or not donor['canHear']:raise ValueError('Actual audible signal blocked')
        elif signal['kind']=='visible':
            if not donor['canSee'] or signal['needsFreeHand'] and self.owner['freeHands']<1:raise ValueError('Actual visible signal blocked')
        else:raise ValueError('Unmodeled communication channel; no automatic telepathy')
        return deepcopy(signal)

    def _entitlement(self,route,signal):
        if route=='native':
            if self.native_selection is None or NATURE in self.owner['suppressedCards']:raise ValueError('Actual native acquired unsuppressed card required')
            return {'route':'native','selection':deepcopy(self.native_selection)}
        if route!='borrowed' or not isinstance(self.actor,NatureBorrowedTransactions):raise ValueError('Actual native or prepared borrowed route required')
        b=self.actor
        if not b.acquired.pay.has('versatile_mastery') or 'versatile_mastery' in b.acquired.pay.suppressed or not b.allowance.use.operative or b.allowance.use.current<1:
            raise ValueError('Actual paid available Versatile Mastery use required')
        if not b.prepared or b.prepared['choice']!=NATURE or b.prepared.get('elapsedSeconds',0)<60 or 'completedAt' not in b.prepared:
            raise ValueError('Actual completed60-second Nature preparation required')
        donor=b.donor_ok(b.prepared['donor'],NATURE,distance=30)
        if not donor['perceivesSignal']:raise ValueError('Donor must actually receive and understand the signal')
        return {'route':'borrowed','preparation':deepcopy(b.prepared),'signal':self._signal(signal,b.prepared['donor'])}

    def _capable(self):
        return self.owner['conscious'] and self.owner['canAct'] and not self.owner['magicalTechniqueProhibited'] and NATURE not in self.owner['suppressedCards']

    def _task_capable(self):
        return self.owner['conscious'] and self.owner['canAct']

    def declare(self,event,area_id,*,route,signal=None,expected_version,ready_trigger=None):
        if expected_version!=self.version or self.actor.pending or event in self.actor.events:raise ValueError('Current state version and unused activation identity required')
        if not self._capable() or self.actor.cooldowns.get(NATURE,0)>0:raise ValueError('Actual capable actor and ready same-card recharge required')
        provenance=self._entitlement(route,signal);footprint=self._area(area_id);pool=self._pool()
        action_cost='action'
        if ready_trigger is not None:
            trigger=self.actor.world['triggerEvents'].get(ready_trigger)
            if not self.ready or self.ready['route']!=route or not trigger or not trigger['perceived'] or not trigger['actualEvent'] or trigger['kind']=='private-ability-name' or trigger['matches']!=self.ready['trigger']:
                raise ValueError('Actual perceivable matching Ready trigger and current setup required')
            if self.reactions<1 or not self.owner['reactionLegal']:raise ValueError('Actual legal Ready Reaction required')
            action_cost='reaction'
        elif self.actor.turn is None or self.actor.actions<1:raise ValueError('Actual legal Action required')
        if route=='borrowed':
            self.actor.commit(event,NATURE,self.card,action_cost)
        else:
            self.actor.events[event]={'choice':NATURE,'actor':'owner','cost':action_cost,'committedBeforeOutcome':True}
            if action_cost=='action':self.actor.actions-=1
        if action_cost=='reaction':
            self.reactions-=1;self.actor.events[self.ready['event']]['status']='ready-released';self.ready=None
        self.owner['personalRP']-=1;self.actor.cooldowns[NATURE]=3;self.next_elapsed_recharge=self.actor.now+6
        if self.actor.turn is not None and self.turn_meta[self.actor.turn]['regular']:self.magical_turns.add(self.actor.turn)
        self.version+=1
        p={'type':'nature-activation','event':event,'sourceId':NATURE,'authority':self.authority['reviewId'],
            'actor':'owner','committedAt':self.actor.now,'turn':self.actor.turn,'round':self.actor.round,
            'stateVersion':self.version,'area':area_id,'fixedFootprint':footprint,'commitPosition':self.owner['position'],
            'provenance':provenance,'personalPool':pool,'paidRP':1,'actionCost':action_cost,'paidBeforeOutcome':True,
            'classification':'magical-nonspell','spellRank':None,'concentration':False,'components':[],
            'spellHistoryAtCommit':deepcopy(self.spell_history)}
        self.actor.pending=p;self.actor.events[event].update(status='paid-pending',receipt=deepcopy(p))
        return deepcopy(p)

    def resolve(self,event):
        p=self.actor.pending
        if not p or p['event']!=event or p['type']!='nature-activation':raise ValueError('Current paid pending Nature activation required')
        valid=self._capable()
        try:self._area(p['area'],p['fixedFootprint'])
        except ValueError:valid=False
        if valid:
            if self.rider:
                self.rider['state']='replaced';self.rider_history.append(deepcopy(self.rider))
            self.rider={'sourceId':NATURE,'activation':event,'actor':'owner','area':p['area'],'fixedFootprint':deepcopy(p['fixedFootprint']),
                'resolvedAt':self.actor.now,'deadline':self.actor.now+60,'state':'unused','provenance':deepcopy(p['provenance'])}
        result={'resolved':bool(valid),'riderCreated':bool(valid),'deadline':self.actor.now+60 if valid else None,'refund':0}
        self.actor.events[event].update(status='resolved' if valid else 'failed-no-refund',result=result)
        self.actor.pending=None;self.version+=1;return deepcopy(result)

    def interrupt(self,event,interrupt_id):
        p=self.actor.pending;cause=self.actor.world['interruptions'].get(interrupt_id)
        if not p or p['event']!=event or not cause or not cause['actualSource'] or not cause['actualTrigger'] or not cause['coversPendingOperation']:
            raise ValueError('Actual source-defined covering interrupt required')
        if cause['kind'] in {'ordinary-counterspell','rank-limited-spell-dispel','ordinary-damage-only','announced-private-name'}:
            raise ValueError('This source supplies no Nature interruption or concentration test')
        if cause['kind']!='incapacitating-condition' or self.owner['canAct']:
            raise ValueError('This finite interrupt fixture requires actual sourced incapacity')
        self.actor.events[event].update(status='interrupted-no-refund',interrupt=deepcopy(cause))
        if p['type']=='nature-check':self.tasks[event]['state']='interrupted-no-refund'
        self.actor.pending=None;self.version+=1

    def ready_setup(self,event,route,trigger):
        if self.actor.pending or event in self.actor.events or not self._capable() or self.actor.turn is None or self.actor.actions<1:
            raise ValueError('Actual legal Ready setup Action required')
        if route=='native':
            if self.native_selection is None:raise ValueError('Native Nature entitlement required')
        elif route=='borrowed':
            if not isinstance(self.actor,NatureBorrowedTransactions) or not self.actor.prepared or self.actor.prepared['choice']!=NATURE:
                raise ValueError('Actually prepared borrowed Nature action required')
        else:raise ValueError('Exact Nature route required')
        if trigger not in self.actor.world['triggerDefinitions']:raise ValueError('Actual perceivable trigger definition required')
        if self.ready:self.actor.events[self.ready['event']]['status']='ready-replaced'
        self.actor.actions-=1;self.ready={'event':event,'route':route,'trigger':trigger,'setupAt':self.actor.now,'expiresAtNextRegularStart':True}
        self.actor.events[event]={'kind':'nonspell-Ready','status':'ready-pending','setupActionSpent':1};self.version+=1
        return deepcopy(self.ready)

    def start_task(self,event,task_id):
        task=self.actor.world['tasks'].get(task_id)
        if self.actor.pending or event in self.tasks or event in self.actor.events or not task or not task['actualLawfulCheck'] or not self._task_capable() or self.actor.turn is None or self.actor.actions<1:
            raise ValueError('Actual separately lawful task and its Action required')
        if task['requiresHands'] and self.owner['freeHands']<1 or task['requiresTools'] and not self.owner['usableTaskTools']:
            raise ValueError('Actual task physical requirements remain')
        self.actor.actions-=1;self.tasks[event]={'taskId':task_id,'start':self.actor.now,'paidAction':1,'state':'paid-working'}
        self.version+=1;return deepcopy(self.tasks[event])

    def declare_check(self,event,*,expected_version):
        work=self.tasks.get(event)
        if expected_version!=self.version or self.actor.pending or not work or work['state']!='paid-working':raise ValueError('Actual pending paid task and current version required')
        task=self.actor.world['tasks'][work['taskId']];r=self.rider
        if not r or r['state']!='unused' or self.actor.now>=r['deadline'] or self.actor.now<work['start']+task['minimumSeconds']:
            raise ValueError('Unused rider at actual completed-task adjudication before deadline required')
        if task['skill'] not in {'Perception','Survival'} or not task['actualLawfulCheck'] or not self._task_capable():raise ValueError('Actual lawful applicable check required')
        if self.owner.get('natureRiderSuppressed',False):raise ValueError('Actual covering rider suppression applies')
        cell_id=task['cell'];cell=self.actor.world['terrain'][cell_id]
        if cell_id not in r['fixedFootprint'] or cell['position']!=r['fixedFootprint'][cell_id] or not cell['natural'] or abs(cell['position']-self.owner['position'])>15 or not cell['taskPerceived'] or not cell['taskLine'] or not cell['taskAccessible'] or cell['totalCover']:
            raise ValueError('Original fixed natural area, actual senses/access/line and current15ft required')
        if task['requiresHands'] and self.owner['freeHands']<1 or task['requiresTools'] and not self.owner['usableTaskTools']:raise ValueError('Task physical requirements still apply')
        if type(task['dc']) is not int or task['dc']<0:raise ValueError('Actual source task DC required')
        skill=task['skill'];ability=self.acquired.skills[skill];factor=self.acquired.training_projection['skills'].get(skill,0)
        modifier=(self.acquired.pay.scores[ability]-10)//2+factor*pb(sum(self.acquired.pay.current_classes.values()))
        disadvantage=bool(task['disadvantageSources'])
        mode='normal' if disadvantage else 'advantage'
        p={'type':'nature-check','event':event,'taskId':work['taskId'],'dc':task['dc'],'modifier':modifier,'ability':ability,
            'ownTrainingFactor':factor,'mode':mode,'advantageSources':['Nature/'+r['activation'],*task['advantageSources']],
            'disadvantageSources':deepcopy(task['disadvantageSources']),'consumedBeforeFaces':True,'rider':deepcopy(r)}
        r['state']='consumed';r['check']=event;self.rider_history.append(deepcopy(r));self.rider=None
        work['state']='committed-awaiting-faces';self.actor.pending=p;self.actor.events[event]={'kind':'Nature-benefited-check','status':'paid-pending','receipt':deepcopy(p)}
        self.version+=1;return deepcopy(p)

    def resolve_check(self,event,faces):
        p=self.actor.pending
        if not p or p['type']!='nature-check' or p['event']!=event:raise ValueError('Actual committed Nature check required')
        if not isinstance(faces,list) or len(faces)!=(2 if p['mode']=='advantage' else 1) or any(type(n) is not int or not 1<=n<=20 for n in faces):raise ValueError('Actual face count follows ordinary advantage cancellation')
        result=task_check(max(faces) if p['mode']=='advantage' else faces[0],p['modifier'],p['dc'])
        task=self.actor.world['tasks'][p['taskId']]
        evidence=deepcopy(task['supportedEvidence']) if result['success'] and task['evidenceState']=='established' else []
        result.update(revealedEvidence=evidence,unknownDataDoesNotProveAbsence=True,grantsSight=False,passiveBonus=0)
        self.tasks[event]['state']='resolved';self.actor.events[event].update(status='resolved',result=deepcopy(result))
        self.actor.pending=None;self.version+=1;return result
