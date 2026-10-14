"""Finite Versatile Mastery transactions in an explicit conditional encounter.

The caller provides source-validated paid ownership, class-card selections,
body/items, permission to perform magic, and canonical clock markers. This
module does not invent those facts or execute a complete class/Weave engine.
"""
from copy import deepcopy
from dataclasses import asdict
import re
from core_playtest_rules import attack_roll, saving_throw, task_check
from combat_playtest_rules import movement_cost
from feat_exact_01_acquisition_models import pb
from feat335_allowance_bindings import BoundAllowance


class BorrowedStunts:
    def __init__(self, acquired, menu, class_sources, equipment, donors, world, allowance):
        if not acquired.pay.has('versatile_mastery'):raise ValueError('An actual paid feat grant is required')
        self.acquired=acquired;self.menu={x['sourceId']:deepcopy(x) for x in menu}
        if len(self.menu)!=12:raise ValueError('Exact twelve-card menu required')
        self.class_sources=class_sources;self.equipment=equipment;self.donors=deepcopy(donors);self.world=deepcopy(world)
        self.allowance=BoundAllowance.initial('owner',allowance,pb(sum(acquired.pay.current_classes.values())))
        self.now=0;self.turn=None;self.round=None;self.actions=0;self.bonus_actions=0
        self.preparing=None;self.prepared=None;self.events={};self.history=[];self.cooldowns={};self.card_rest_spent=set()
        self.riders=[];self.turns=set();self.rests=set()
        for donor in self.donors.values():
            source=class_sources[donor['class']];schedule=source['schedule'][0];cards={c['id']:c for c in source['cards']}
            choices=donor['selectedCards']
            if donor['classLevel']!=1 or len(choices)!=schedule['choose'] or len(set(choices))!=len(choices):raise ValueError('Actual level1 selection schedule required')
            selected=[cards[x] for x in choices]
            if any(c['band'] not in schedule['bands'] or c['minimumClassLevel']>1 or c['acquisition']!='selection' for c in selected):raise ValueError('Unavailable source selection')
            if sum(c['sourceKind']=='active' for c in selected)<schedule['minimumActives']:raise ValueError('Required active selections missing')
            if not set(donor['selectedSkills'])<=set(donor['skillOptions']):raise ValueError('Skill must be an actual class training choice')

    def snapshot(self):
        return {'acquisition':self.acquired.snapshot(),'donors':deepcopy(self.donors),'world':deepcopy(self.world),
            'allowance':asdict(self.allowance),'now':self.now,'turn':self.turn,'round':self.round,
            'actions':self.actions,'bonusActions':self.bonus_actions,'preparing':deepcopy(self.preparing),'prepared':deepcopy(self.prepared),
            'events':deepcopy(self.events),'history':deepcopy(self.history),'cooldowns':dict(self.cooldowns),
            'cardRestSpent':sorted(self.card_rest_spent),'riders':deepcopy(self.riders),'turns':sorted(self.turns),'rests':sorted(self.rests)}

    def mod(self,ability):return (self.acquired.pay.scores[ability]-10)//2
    def proficiency(self):return pb(sum(self.acquired.pay.current_classes.values()))
    def advance(self,now):
        if type(now) is not int or now<self.now:raise ValueError('Monotonic clock required')
        self.now=now;self.riders=[x for x in self.riders if now<x['deadline']]
    def begin_turn(self,identity,round_id,now,*,regular=True):
        if identity in self.turns:raise ValueError('No replay of a turn')
        self.advance(now);self.turns.add(identity);self.turn=identity;self.round=round_id;self.actions=1;self.bonus_actions=1
        if regular:self.cooldowns={k:max(0,v-1) for k,v in self.cooldowns.items()}

    def donor_ok(self,identity,choice,*,distance):
        donor=self.donors.get(identity)
        if not donor or not donor['party'] or not donor['willing'] or not donor['conscious'] or not donor['sharedChannel']:
            raise ValueError('Real willing conscious party donor and shared channel required')
        if abs(donor['position']-self.world['owner']['position'])>distance:raise ValueError('Donor out of range')
        if choice in donor['suppressed'] or choice in donor['copiedOrBorrowed']:raise ValueError('Suppressed/copied/borrowed grants cannot teach')
        if choice not in donor['selectedCards'] and choice not in donor['selectedSkills']:raise ValueError('Exact class-acquired card or skill required')
        if choice in self.menu and self.menu[choice]['actualSourceClass']!=donor['class']:raise ValueError('Wrong class provenance')
        return donor

    def start_prepare(self,event,donor,choice):
        if event in self.events or self.preparing:raise ValueError('Duplicate or overlapping preparation')
        self.donor_ok(donor,choice,distance=5)
        if choice not in self.menu and choice not in self.donors[donor]['selectedSkills']:raise ValueError('Outside finite menu/class skill')
        self.preparing={'event':event,'donor':donor,'choice':choice,'start':self.now}
    def complete_prepare(self,now,*,uninterrupted):
        if not self.preparing:raise ValueError('No preparation start')
        work=deepcopy(self.preparing)
        if not uninterrupted:
            self.advance(now);self.preparing=None;self.history.append({'kind':'preparation-interrupted','work':work});return False
        if now<work['start']+60:raise ValueError('One actual uninterrupted minute required')
        self.donor_ok(work['donor'],work['choice'],distance=5)
        self.advance(now);self.prepared=work;self.preparing=None;self.events[work['event']]={'kind':'prepared','choice':work['choice']}
        return True

    def preflight(self,event,kind):
        if event in self.events or not self.prepared:raise ValueError('An unused event and actual prepared choice required')
        if not self.world['owner']['canAct'] or not self.allowance.use.operative or self.allowance.use.current<1:raise ValueError('Feat unavailable')
        choice=self.prepared['choice'];donor=self.donor_ok(self.prepared['donor'],choice,distance=30)
        if not donor['perceivesSignal']:raise ValueError('Donor must perceive and understand the signal')
        if kind=='skill':return choice
        if choice not in self.menu:raise ValueError('This is not a permitted card')
        row=self.menu[choice]
        if sum(self.acquired.pay.current_classes.values())<row['minimumBorrowerTotalLevel']:raise ValueError('Borrower level insufficient')
        card=next(c for c in self.class_sources[row['actualSourceClass']]['cards'] if c['id']==choice)
        if self.cooldowns.get(choice,0)>0 or choice in self.card_rest_spent:raise ValueError('Existing personal same-card ledger is spent')
        cost='bonus' if card['activation']=='Bonus Action' else 'action'
        if (self.bonus_actions if cost=='bonus' else self.actions)<1:raise ValueError('Actual activation cost unavailable')
        return choice,card,cost

    def commit(self,event,choice,card,cost):
        provenance=deepcopy(self.prepared);self.allowance.spend()
        if cost=='bonus':self.bonus_actions-=1
        elif cost=='action':self.actions-=1
        match=re.match(r'Recharge (\d+)',card['frequency']) if card else None
        if match:self.cooldowns[choice]=int(match[1])
        if card and card['frequency']=='1/short rest':self.card_rest_spent.add(choice)
        self.events[event]={'choice':choice,'donor':provenance['donor'],'actor':'owner','cost':cost,'committedBeforeOutcome':True}
        self.history.append({'event':event,'kind':'borrowed-activation','preparedProvenance':provenance})
        return provenance

    def move(self,event,path):
        choice,card,cost=self.preflight(event,'card');kind=choice.rsplit('.',1)[-1]
        if kind not in {'tactical-reposition','skirmisher-s-step','cunning-movement','shadow-step'}:raise ValueError('Not a movement card')
        actor=self.world['owner'];pos=actor['position'];spent=0
        if actor['restrained'] or actor['usableSpeed']<=0:raise ValueError('No actual usable movement')
        if kind=='shadow-step' and not actor['coverOrConcealment']:raise ValueError('Shadow Step needs actual cover/concealment at start')
        for segment in path:
            if segment['from']!=pos or not segment['routeLegal']:raise ValueError('Noncontiguous or impassable route')
            if segment['hostileOccupied'] and kind!='cunning-movement':raise ValueError('This borrowed card gives no hostile-space exception')
            spent+=movement_cost(abs(segment['to']-pos),segment['terrain']);pos=segment['to']
        if not path or path[-1]['occupiedEndpoint'] or spent>actor['usableSpeed']/2:raise ValueError('Actual destination/budget invalid')
        self.commit(event,choice,card,cost);actor['position']=pos
        result={'movementCost':spent,'ordinaryMovementSpent':actor['ordinaryMovementSpent'],'opportunityAttacksApply':kind=='shadow-step',
            'footfallNoiseSuppressed':kind=='shadow-step','hideAttemptPermitted':kind=='shadow-step' and path[-1]['canConceal'],
            'teleport':False,'invisibility':False,'resourceGenerated':0}
        self.events[event]['result']=result;return deepcopy(result)

    def attacks(self,event,attacks,*,extra_die=None,con_save=None,stagger_deadline=None,cover_deadline=None):
        choice,card,cost=self.preflight(event,'card');kind=choice.rsplit('.',1)[-1]
        counts={'covering-fire':1,'brutal-strike':1,'quick-shot':1,'twin-strike':2,'flurry-of-blows':2}
        if kind not in counts or len(attacks)!=counts[kind]:raise ValueError('Exact printed attack count required')
        checked=[];items=[]
        for attack in attacks:
            target=self.world['targets'].get(attack['target']);item=self.world['items'].get(attack['item'])
            if not target or not item or item['heldBy']!='owner' or not attack['legalBodyRangeLineTarget']:raise ValueError('Actual body, held profile and legal target required')
            profile=self.equipment[item['profile']];properties=profile['sourceFields']['Properties'].lower();category=profile['category'].lower()
            ranged='ranged' in category;unarmed=profile['name']=='Unarmed strike'
            if kind=='covering-fire' and not ranged:raise ValueError('Own ranged weapon required')
            if kind=='quick-shot' and profile['name'] not in {'Shortbow','Longbow'}:raise ValueError('Own legal bow required')
            if kind=='brutal-strike' and (ranged or unarmed):raise ValueError('Own melee weapon required')
            if kind=='twin-strike' and ('light' not in properties or ranged or unarmed):raise ValueError('Two Light melee weapons required')
            if kind=='flurry-of-blows' and not unarmed:raise ValueError('Own actual unarmed profile required')
            ability=attack['ability']
            if ability not in ({'DEX'} if ranged else {'STR','DEX'} if 'finesse' in properties else {'STR'}):raise ValueError('No borrowed class attack ability substitution')
            natural=attack['natural'];result=attack_roll(natural,self.mod(ability)+(self.proficiency() if item['profile'] in self.acquired.training_projection['weapons'] else 0),target['ac'])
            parsed=re.fullmatch(r'(\d+)d(\d+) (\w+)',profile['sourceFields']['Damage'])
            if parsed:
                count,sides=int(parsed[1]),int(parsed[2]);faces=attack['damageFaces']
                if result['critical']:count*=2
                if len(faces)!=count or any(type(x)is not int or not 1<=x<=sides for x in faces):raise ValueError('Actual native damage dice required')
                base=sum(faces);dtype=parsed[3]
            else:
                if profile['sourceFields']['Damage']!='1 bludgeoning':raise ValueError('Profile outside bounded source damage parser')
                base=1;dtype='bludgeoning'
            if ranged and item['ammunition']<1:raise ValueError('Actual carried ammunition required')
            checked.append((attack,item,ability,base,dtype,bool(parsed),result));items.append(attack['item'])
        if kind=='twin-strike' and len(set(items))!=2:raise ValueError('Two actual wielded items, not one aliased weapon')
        if kind=='brutal-strike':
            if not isinstance(extra_die,list) or len(extra_die)!=(2 if checked[0][-1]['critical'] else 1) or any(type(x)is not int or not 1<=x<=6 for x in extra_die) or type(con_save)is not int or not 1<=con_save<=20 or not stagger_deadline or stagger_deadline<=self.now:raise ValueError('FixedS1 damage dice, CON save and future regular endpoint required')
        if kind=='covering-fire' and (not cover_deadline or cover_deadline<=self.now):raise ValueError('Next owner regular-start marker required')
        provenance=self.commit(event,choice,card,cost);out=[];ability_added=False
        for attack,item,ability,base,dtype,dice,result in checked:
            ranged='ranged' in self.equipment[item['profile']]['category'].lower()
            if ranged:item['ammunition']-=1
            damage=0
            if result['hit']:
                damage=base
                if kind!='quick-shot' and (kind!='twin-strike' or not ability_added):damage+=self.mod(ability);ability_added=True
                if kind=='brutal-strike':
                    damage+=sum(extra_die)
                    save=saving_throw(con_save,self.world['targets'][attack['target']]['conSave'],8+self.proficiency()+self.mod(ability))
                    if not save['success']:self.riders.append({'kind':'Staggered','target':attack['target'],'deadline':stagger_deadline,'attackPenalty':-1,'speedPenalty':-5,'source':event,'donor':provenance['donor']})
                if kind=='covering-fire':self.riders.append({'kind':'CoveringFire','target':attack['target'],'deadline':cover_deadline,'nextAttackAgainstOtherAlly':-2,'source':event,'donor':provenance['donor']})
            out.append({**result,'nativeDamage':max(0,damage),'damageType':dtype,'target':attack['target']})
        self.events[event]['result']={'attacks':out,'borrowedEngineResourcesGenerated':0,'extraAttacksGranted':0}
        return deepcopy(self.events[event]['result'])

    def task(self,event,natural,*,ability='DEX',target=None,mechanism=None,skill=None,dc=None):
        choice,card,cost=self.preflight(event,'card');kind=choice.rsplit('.',1)[-1]
        if kind=='disable-device':
            device=self.world['mechanisms'].get(mechanism)
            if not self.world['owner']['usableThievesTools'] or not device or device['magical'] or not device['accessibleInReach']:raise ValueError('Accessible nonmagical device and usable tools required')
            actual_dc=device['dc'] if device['dc'] is not None else 20 if device['complex'] else 15
            modifier=self.mod('DEX')+self.proficiency()
        elif kind=='feint':
            victim=self.world['targets'].get(target)
            if ability not in {'DEX','CHA'} or not victim or abs(victim['position']-self.world['owner']['position'])>10 or not victim['perceivedBothWays'] or not victim['enemy']:raise ValueError('Actual perceptible enemy and chosen DEX/CHA required')
            actual_dc=victim['passiveInsight'];modifier=self.mod(ability)+self.proficiency()
        else:raise ValueError('Not a task card')
        result=task_check(natural,modifier,actual_dc);self.commit(event,choice,card,cost)
        if kind=='disable-device':
            if result['success']:device['disarmed']=True
            elif actual_dc-result['total']>=5:device['triggered']=True
            result.update(triggered=device['triggered'],disarmed=device['disarmed'])
        elif result['success']:self.riders.append({'kind':'Feint','target':target,'deadline':self.world['owner']['actualTurnEnd'],'turn':self.turn,'source':event,'nextWeaponAttackAdvantage':True})
        self.events[event]['result']=deepcopy(result);return result

    def nature_whisper(self,event):
        choice,card,cost=self.preflight(event,'card')
        if choice!='ranger.base.nature-s-whisper':raise ValueError('Exact prepared Nature Whisper required')
        owner=self.world['owner']
        if owner['personalRP']<1 or not owner['sourceQualifiedPersonalRPPool'] or not owner['actualMinorWeaveClearance']:raise ValueError('Existing personal RP and actual source-specific Weave clearance required')
        self.commit(event,choice,card,cost);owner['personalRP']-=1
        self.riders.append({'kind':'NatureWhisper','deadline':self.now+60,'source':event,'oneActualCheckRemaining':True})
        return {'rpSpent':1,'checkGranted':False,'automaticEvidence':False,'deadline':self.now+60}

    def use_nature_advantage(self,event,skill,faces,dc,*,distance,natural_terrain,total_cover,evidence,actual_check_action):
        rider=next((r for r in self.riders if r['kind']=='NatureWhisper' and r['oneActualCheckRemaining']),None)
        if event in self.events or not rider or self.now>=rider['deadline'] or skill not in {'Perception','Survival'} or distance>15 or not natural_terrain or total_cover:
            raise ValueError('A current remaining bonus and an actual eligible natural-evidence check required')
        if not actual_check_action or self.actions<1 or not self.world['owner']['canAct']:raise ValueError('No free check/action supplied by Whisper')
        if len(faces)!=2 or any(type(x)is not int or not 1<=x<=20 for x in faces):raise ValueError('Actual advantage dice required')
        modifier=self.mod('WIS')+self.proficiency()*self.acquired.training_projection['skills'].get(skill,0)
        result=task_check(max(faces),modifier,dc);rider['oneActualCheckRemaining']=False;self.actions-=1
        result['revealedEvidence']=deepcopy(evidence) if result['success'] else []
        self.events[event]={'kind':'actual-check-with-existing-Whisper','result':deepcopy(result),'bonusConsumed':True};return result

    def hide_after_shadow(self,event,move_event,natural,dc):
        prior=self.events.get(move_event)
        if event in self.events or not prior or prior.get('choice')!='thief.base.shadow-step' or not prior['result']['hideAttemptPermitted'] or prior.get('hideUsed'):
            raise ValueError('One immediately eligible actual Shadow Step hide attempt required')
        modifier=self.mod('DEX')+self.proficiency()*self.acquired.training_projection['skills'].get('Stealth',0)
        result=task_check(natural,modifier,dc);prior['hideUsed']=True
        self.events[event]={'kind':'Hide-after-Shadow-Step','result':result,'noInvisibilityGranted':True};return deepcopy(result)

    def borrowed_skill(self,event,skill,natural,ability,dc,*,actual_check_action):
        choice=self.preflight(event,'skill')
        if choice!=skill or choice in self.menu or not actual_check_action or self.actions<1:raise ValueError('Actual prepared class skill check and cost required')
        factor=max(1,self.acquired.training_projection['skills'].get(skill,0))
        result=task_check(natural,self.mod(ability)+factor*self.proficiency(),dc)
        self.commit(event,choice,None,'action');self.events[event]['result']=result;return deepcopy(result)

    def rest(self,identity,*,kind,beneficial):
        if identity in self.rests:return False
        if kind not in {'SR','LR'}:raise ValueError('Actual completed rest kind required')
        self.rests.add(identity);self.prepared=None;self.preparing=None
        # Completion ends preparation even when this extra rest pays debt only.
        result=self.allowance.rest('owner',identity,kind,beneficial)
        if result:self.card_rest_spent.clear()
        return result
