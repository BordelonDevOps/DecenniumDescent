"""Finite Flora/Trapcasting use with a paid source history and conditional world.

Canonical turn/round/deadline, sight/hearing, supported ground and actual body
positions are explicit fixture facts. This does not authenticate a campaign,
simulate arbitrary geometry, or decide the unresolved loss-of-first-plant
additional-creation interpretation. No spell/RP/harvest engine is invented.
"""
from copy import deepcopy
from core_playtest_rules import saving_throw, task_check
from feat_exact_01_acquisition_models import pb


class FloraUse:
    def __init__(self, acquired, world):
        if not acquired.pay.has('conjure_flora') or 'conjure_flora' not in acquired.initializations:
            raise ValueError('An actual complete paid Flora acquisition is required')
        self.acquired=acquired;self.world=deepcopy(world)
        self.now=0;self.turn=None;self.round=None;self.regular=False
        self.actions=0;self.bonus_actions=0;self.operative=True
        self.plants={};self.conditions=[];self.history=[];self.events=set()
        self.offense=set();self.phases=set();self.turns=set();self.rests=set()
        self.second=None;self.consumed_second=set();self.entries=set()
        self.profiles={p['id']:deepcopy(p) for p in acquired.supplements['SUP-07']['floraBody']['modes']}
        if set(self.profiles)!={'lash','spore','entangle'}:raise ValueError('Exact three source modes required')

    @property
    def initial(self):return self.acquired.initializations['conjure_flora']

    def snapshot(self):
        return {'acquisition':self.acquired.snapshot(),'world':deepcopy(self.world),'now':self.now,
            'turn':self.turn,'round':self.round,'regular':self.regular,'actions':self.actions,'bonusActions':self.bonus_actions,
            'operative':self.operative,'plants':deepcopy(self.plants),'conditions':deepcopy(self.conditions),
            'history':deepcopy(self.history),'events':sorted(self.events),'offense':sorted(self.offense),
            'phases':sorted(self.phases),'turns':sorted(self.turns),'rests':sorted(self.rests),
            'second':deepcopy(self.second),'consumedSecond':sorted(self.consumed_second),'entries':sorted(self.entries)}

    def advance(self,now):
        if type(now) is not int or now<self.now:raise ValueError('Monotonic actual clock required')
        self.now=now
        for identity,p in self.plants.items():
            if p['active'] and now>=p['deadline']:self.end(identity,'original-minute-deadline')
        self.conditions=[c for c in self.conditions if now<c['deadline'] and self.plants[c['plant']]['active']]
        if self.second and now>=self.second['deadline']:
            self.consumed_second.add(self.second['use']);self.second=None
        self.sync()

    def begin_turn(self,identity,round_id,now,*,regular=True,actions=1,bonus_actions=1):
        if identity in self.turns:raise ValueError('Actual turn identity cannot be replayed')
        if type(actions) is not int or type(bonus_actions) is not int or min(actions,bonus_actions)<0:raise ValueError('Actual action budgets required')
        self.advance(now);self.turns.add(identity);self.turn=identity;self.round=round_id;self.regular=regular
        self.actions=actions;self.bonus_actions=bonus_actions

    def sync(self):
        self.initial['activePlants']=[p['id'] for p in self.plants.values() if p['active']]
        self.initial['additionalCreationPending']=self.second is not None

    def dc(self):
        return self.acquired.flora_dc_projection()['dc']

    def body(self,identity):
        p=self.plants.get(identity)
        if p is None or not p['active'] or self.now>=p['deadline']:raise ValueError('Actual active plant required')
        return p

    def position(self,identity):
        return self.world['actors'][identity]['position']

    def distance(self,a,b):
        # All fixture positions lie on one axis; this is actual scalar distance,
        # not a new general diagonal/grid rule.
        return abs(a-b)

    def line(self,a,b):
        return not any(min(a,b)<w<max(a,b) for w in self.world['walls'])

    def preflight(self,event,*,action=False,bonus=False):
        if event in self.events:raise ValueError('Underlying event already committed')
        if not self.operative or not self.world['actors']['owner']['canAct']:raise ValueError('Owner cannot use this active feat now')
        if action and self.actions<1:raise ValueError('An actual Action is required')
        if bonus and self.bonus_actions<1:raise ValueError('An actual Bonus Action is required')

    def create(self,event,identity,mode,position,deadline,*,armed=False,additional=False):
        self.preflight(event,action=True)
        if identity in self.plants or mode not in self.profiles:raise ValueError('New body identity and exact fixed mode required')
        if type(deadline) is not int or not self.now<deadline<=self.now+60:raise ValueError('Actual original source-start minute deadline required')
        if self.distance(self.position('owner'),position)>30 or not self.line(self.position('owner'),position) or position not in self.world['supportedVisibleGround']:
            raise ValueError('Visible supported ground within30 and line of effect required')
        if self.initial['fixedCastingRoute'] not in self.acquired.actual_casting_routes():
            raise ValueError('Lost-provider use is outside this source-retaining witness, not ruled illegal by this model')
        if armed and not self.acquired.pay.has('trapcasting'):raise ValueError('Actual separately acquired Trapcasting required')
        total=sum(self.acquired.pay.current_classes.values());capacity=2 if total>=10 else 1
        if sum(p['active'] for p in self.plants.values())>=capacity:raise ValueError('Actual body capacity exhausted')
        if additional:
            if total<10 or not self.second or self.now>=self.second['deadline'] or self.second['use'] in self.consumed_second:
                raise ValueError('No current additional-creation entitlement')
            if not self.plants[self.second['first']]['active']:
                raise ValueError('First-body-ended additional creation is outside this bounded witness; source adjudication still required')
            use=self.second['use']
        else:
            if self.initial['creationUses']['current']<1:raise ValueError('Creation rest use already spent')
            use=event
        current_pb=pb(total)
        self.actions-=1;self.events.add(event)
        if additional:self.consumed_second.add(use);self.second=None
        else:
            self.initial['creationUses']['current']-=1
            self.second={'use':event,'first':identity,'deadline':deadline} if total>=10 else None
        self.plants[identity]={'id':identity,'owner':'owner','mode':mode,'burstType':self.profiles[mode]['burstType'],
            'position':position,'created':self.now,'deadline':deadline,'active':True,'endReason':None,
            'maximumHP':5+current_pb,'hp':5+current_pb,'saveBonus':current_pb,'ac':12,'armed':armed,
            'creationUse':use,'noLootOrResourceOutputs':True}
        self.sync();self.history.append({'event':event,'kind':'additional-creation' if additional else 'creation','body':identity,'actionSpent':1,'restUseSpent':not additional})
        return deepcopy(self.plants[identity])

    def channel(self,p):
        owner=self.world['actors']['owner']
        return self.distance(owner['position'],p['position'])<=60 and ((owner['spokenCommand'] and not owner['silenced']) or (owner['visibleCommand'] and self.line(owner['position'],p['position'])))

    def offense_free(self):
        if self.round is None or self.round in self.offense:raise ValueError('Shared owner/numbered-round companion offense unavailable')

    def condition(self,plant,target,kind,deadline):
        if deadline<=self.now:raise ValueError('Actual future target regular-end deadline required')
        if kind in self.world['actors'][target]['conditionImmunities']:return None
        # Keep independent source records/endpoints; arbitration is ordinary
        # nonstacking outside this model, not destructive overwrite by this feat.
        value={'plant':plant,'target':target,'kind':kind,'deadline':deadline,'dc':self.dc()}
        self.conditions.append(value);return deepcopy(value)

    def resolve(self,plant,mode,targets,rolls,*,die=None,trap=False,deadlines=None):
        outcome=[];deadlines=deadlines or {}
        for target in targets:
            actor=self.world['actors'][target]
            ability='DEX' if trap or mode=='lash' else 'CON' if mode=='spore' else 'STR'
            save=saving_throw(rolls[target],actor['saves'][ability],self.dc())
            row={'target':target,'saveAbility':ability,'save':save,'dc':self.dc(),'nativeDamage':0,'condition':None}
            if mode=='lash':row.update(nativeDamage=(0 if trap else die//2) if save['success'] else die,damageType='piercing')
            elif not save['success']:row['condition']=self.condition(plant,target,'Poisoned' if mode=='spore' else 'Restrained',deadlines[target])
            outcome.append(row)
        return outcome

    def check_resolution_inputs(self,mode,targets,rolls,die,deadlines):
        if len(set(targets))!=len(targets) or not targets or set(rolls)!=set(targets):raise ValueError('Distinct actual targets and one save face each required')
        if any(t not in self.world['actors'] or type(rolls[t]) is not int or not 1<=rolls[t]<=20 for t in targets):raise ValueError('Actual creature/save required')
        if mode=='lash' and (type(die) is not int or not 1<=die<=6):raise ValueError('Actual one d6 face required')
        if mode!='lash' and any(t not in deadlines or type(deadlines[t]) is not int or deadlines[t]<=self.now for t in targets):raise ValueError('Future regular-end markers required')

    def command(self,event,participants,mode,targets,rolls,*,die=None,deadlines=None,area=None):
        self.preflight(event,bonus=True);self.offense_free();deadlines=deadlines or {}
        if not self.regular or self.turn in self.phases:raise ValueError('One attached phase after an actual owner regular turn required')
        if not participants or len(set(participants))!=len(participants):raise ValueError('Distinct participating plants required')
        plants=[self.body(x) for x in participants]
        if any(not self.channel(p) for p in plants):raise ValueError('Each participating plant must perceive a real60-foot command channel')
        if mode not in self.profiles:raise ValueError('Exact selected mode required')
        if mode!='lash' and (len(plants)!=1 or plants[0]['mode']!=mode):raise ValueError('One actual selected-mode origin supplies the one outcome')
        self.check_resolution_inputs(mode,targets,rolls,die,deadlines)
        if mode in {'lash','spore'}:
            if len(targets)!=1 or not any(self.distance(p['position'],self.position(targets[0]))<=10 and self.line(p['position'],self.position(targets[0])) for p in plants):raise ValueError('One legal target within10 of a participating plant required')
        else:
            # Conditional world has full supported square/occupancy facts; the
            # supplied area is a real10-foot square, not a scanned target list.
            if area not in self.world['areas']:raise ValueError('Actual supported10-foot square required')
            square=self.world['areas'][area]
            if not square['supported'] or self.distance(plants[0]['position'],square['origin'])>10 or not self.line(plants[0]['position'],square['origin']):raise ValueError('Area is outside the permitted plant origin')
            if set(targets)!=set(square['creatures']):raise ValueError('Every actual creature in the chosen square must resolve, including allies')
        self.bonus_actions-=1;self.events.add(event);self.phases.add(self.turn);self.offense.add(self.round)
        self.actions=0  # The attached phase is after the whole owner turn.
        outcomes=self.resolve(plants[0]['id'],mode,targets,rolls,die=die,deadlines=deadlines)
        self.history.append({'event':event,'kind':'commanded-attached-phase','regularTurn':self.turn,'round':self.round,
            'participants':participants,'mode':mode,'bonusActionSpent':1,'oneSharedOffenseSpent':True,'outcomes':deepcopy(outcomes)})
        return outcomes

    def enter(self,event,plant,target,roll,*,from_outside,meaningful_hostile,die=None,deadline=None):
        if event in self.events:raise ValueError('Physical entry event already evaluated')
        if self.round is None:raise ValueError('An actual governed numbered-round identity is required')
        p=self.body(plant)
        if not self.acquired.pay.has('trapcasting') or not p['armed']:raise ValueError('Actual armed Trapcasting plant required')
        if target not in self.world['actors'] or self.position(target)!=p['position']:raise ValueError('Actual entry into the plant square required')
        self.check_resolution_inputs(p['mode'],[target],{target:roll},die,{target:deadline})
        # Entry history records facts, including an entry that has no trigger.
        # Caller supplies actual movement/forced-entry facts, not placement.
        key=(plant,target,self.round)
        self.events.add(event)
        if not from_outside or not meaningful_hostile:return []
        if key in self.entries:return []
        self.entries.add(key)
        if self.round in self.offense:return []
        self.offense.add(self.round)
        outcomes=self.resolve(plant,p['mode'],[target],{target:roll},die=die,trap=True,deadlines={target:deadline})
        self.history.append({'event':event,'kind':'actual-entry-exception','plant':plant,'round':self.round,'outcomes':deepcopy(outcomes),'oneSharedOffenseSpent':True})
        return outcomes

    def burst(self,event,plant,targets,rolls,dice):
        self.preflight(event,bonus=True);self.offense_free();p=self.body(plant)
        if not self.acquired.pay.has('trapcasting') or self.distance(self.position('owner'),p['position'])>60 or not self.line(self.position('owner'),p['position']) or not self.world['actors']['owner']['perceivesPlants']:raise ValueError('Actual perceived owned plant within60/LoE required')
        if len(dice)!=2 or any(type(d) is not int or not 1<=d<=6 for d in dice):raise ValueError('Exactly two actual d6 faces required')
        actual={t for t,a in self.world['actors'].items() if self.distance(p['position'],a['position'])<=10 and self.line(p['position'],a['position'])}
        if set(targets)!=actual or len(targets)!=len(actual) or set(rolls)!=actual:raise ValueError('All actual burst-area creatures, including owner/allies, must resolve')
        for t in targets:saving_throw(rolls[t],self.world['actors'][t]['saves']['DEX'],self.dc())
        damage_type=p['burstType'];origin=p['position'];dc=self.dc()
        self.bonus_actions-=1;self.offense.add(self.round);self.events.add(event);self.end(plant,'consumed-before-burst')
        outcomes=[]
        for target in targets:
            save=saving_throw(rolls[target],self.world['actors'][target]['saves']['DEX'],dc)
            outcomes.append({'target':target,'save':save,'nativeDamage':sum(dice)//2 if save['success'] else sum(dice),'damageType':damage_type})
        self.history.append({'event':event,'kind':'burst','origin':origin,'plantEndedBeforePayload':not self.plants[plant]['active'],'outcomes':deepcopy(outcomes)})
        return outcomes

    def end(self,identity,reason):
        p=self.plants[identity]
        if not p['active']:return False
        p['active']=False;p['armed']=False;p['endReason']=reason
        self.conditions=[c for c in self.conditions if c['plant']!=identity]
        self.sync();return True

    def damage(self,identity,amount):
        p=self.body(identity)
        if type(amount) is not int or amount<0:raise ValueError('Actual already-resolved damage required')
        p['hp']=max(0,p['hp']-amount)
        if p['hp']==0:self.end(identity,'destroyed-at-zero-no-corpse')

    def heal(self,identity,amount):
        p=self.body(identity)
        if type(amount) is not int or amount<0:raise ValueError('Actual legal healing amount required')
        before=p['hp'];p['hp']=min(p['maximumHP'],p['hp']+amount);return p['hp']-before

    def uproot(self,identity):self.body(identity);self.end(identity,'uprooted-no-harvest')

    def disarm(self,event,identity,natural,modifier,*,tools,reach):
        if event in self.events:raise ValueError('Same manipulation event already evaluated')
        p=self.body(identity)
        if not tools or not reach or not p['armed']:raise ValueError('Actual accessible armed trap and thieves tools required')
        result=task_check(natural,modifier,self.dc());self.events.add(event)
        if result['success']:p['armed']=False
        self.history.append({'event':event,'kind':'conditional-other-actor-paid-disarm-Action','result':result,'noAutomaticExplosion':True})
        return result

    def escape(self,event,plant,target,natural,modifier,*,ability,can_act):
        if event in self.events or not can_act or ability not in {'STR(Athletics)','DEX(Acrobatics)'}:raise ValueError('Actual unique permitted escape Action required')
        matches=[c for c in self.conditions if c['plant']==plant and c['target']==target and c['kind']=='Restrained']
        if not matches:raise ValueError('Actual Flora restraint record required')
        result=task_check(natural,modifier,self.dc());self.events.add(event)
        if result['success']:self.conditions=[c for c in self.conditions if c not in matches]
        self.history.append({'event':event,'kind':'conditional-target-paid-escape-Action','ability':ability,'result':result})
        return result

    def rest(self,identity,*,beneficial,kind):
        if kind not in {'SR','LR'} or not beneficial or identity in self.rests:return False
        self.rests.add(identity);self.initial['creationUses']['current']=1
        return True
