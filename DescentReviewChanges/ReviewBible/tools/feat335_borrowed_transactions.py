"""Declare/pay before any roll; narrowly extend the preserved all12-card witness."""
from copy import deepcopy
import re
from core_playtest_rules import attack_roll,saving_throw,task_check
from feat335_borrowed_stunts import BorrowedStunts

class BorrowedTransactions(BorrowedStunts):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.pending=None;self.shadow_window=None;self.consumed_attack_riders={}
    def snapshot(self):
        return {**super().snapshot(),'pending':deepcopy(self.pending),'shadowWindow':deepcopy(self.shadow_window),
            'consumedAttackRiders':deepcopy(self.consumed_attack_riders)}
    def preflight(self,event,kind):
        if self.pending:raise ValueError('Resolve or lawfully interrupt the committed activation first')
        return super().preflight(event,kind)
    def commit(self,*args):
        self.shadow_window=None;return super().commit(*args)
    def begin_turn(self,*args,**kwargs):
        if self.pending:raise ValueError('A pending action is not banked across turn boundaries')
        self.shadow_window=None;return super().begin_turn(*args,**kwargs)
    def rest(self,*args,**kwargs):
        if self.pending:raise ValueError('Pending action cannot be carried into a rest')
        self.shadow_window=None;return super().rest(*args,**kwargs)
    def declare_attacks(self,event,declarations,*,stagger_deadline=None,cover_deadline=None):
        choice,card,cost=self.preflight(event,'card');kind=choice.rsplit('.',1)[-1]
        counts={'covering-fire':1,'brutal-strike':1,'quick-shot':1,'twin-strike':2,'flurry-of-blows':2}
        if kind not in counts or len(declarations)!=counts[kind]:raise ValueError('Exact source attack count required')
        declared=[];items=[];ammo={}
        for d in declarations:
            if set(d)!={'item','target','ability','legalBodyRangeLineTarget'}:raise ValueError('Declaration cannot carry any roll or damage outcome')
            target=self.world['targets'].get(d['target']);item=self.world['items'].get(d['item'])
            if not target or not item or item['heldBy']!='owner' or not d['legalBodyRangeLineTarget']:raise ValueError('Actual body/weapon/target legality required')
            profile=self.equipment[item['profile']];properties=profile['sourceFields']['Properties'].lower();ranged='ranged' in profile['category'].lower();unarmed=profile['name']=='Unarmed strike'
            if kind=='covering-fire' and not ranged:raise ValueError('Own ranged weapon required')
            if kind=='quick-shot' and profile['name'] not in {'Shortbow','Longbow'}:raise ValueError('Own bow required')
            if kind=='brutal-strike' and (ranged or unarmed):raise ValueError('Actual melee weapon required')
            if kind=='twin-strike' and (ranged or unarmed or 'light' not in properties):raise ValueError('Actual Light melee weapons required')
            if kind=='flurry-of-blows' and not unarmed:raise ValueError('Own actual unarmed profile required')
            ability=d['ability']
            if ability not in ({'DEX'} if ranged else {'STR','DEX'} if 'finesse' in properties else {'STR'}):raise ValueError('No borrowed ability substitution')
            parsed=re.fullmatch(r'(\d+)d(\d+) (\w+)',profile['sourceFields']['Damage'])
            if not parsed and profile['sourceFields']['Damage']!='1 bludgeoning':raise ValueError('Unrepresented native damage profile')
            declared.append({**deepcopy(d),'profile':item['profile'],'attackModifier':self.mod(ability)+(self.proficiency() if item['profile'] in self.acquired.training_projection['weapons'] else 0),
                'abilityModifier':self.mod(ability),'damageCount':int(parsed[1]) if parsed else 0,'damageSides':int(parsed[2]) if parsed else None,
                'damageType':parsed[3] if parsed else 'bludgeoning','flatDamage':0 if parsed else 1})
            items.append(d['item'])
            if ranged:ammo[d['item']]=ammo.get(d['item'],0)+1
        if kind=='twin-strike' and len(set(items))!=2:raise ValueError('Two separately wielded items required')
        if any(self.world['items'][item]['ammunition']<count for item,count in ammo.items()):raise ValueError('Actual ammunition required')
        if kind=='brutal-strike' and (type(stagger_deadline)is not int or stagger_deadline<=self.now):raise ValueError('Future target regular-end marker required')
        if kind=='covering-fire' and (type(cover_deadline)is not int or cover_deadline<=self.now):raise ValueError('Future owner regular-start marker required')
        provenance=self.commit(event,choice,card,cost)
        for item,count in ammo.items():self.world['items'][item]['ammunition']-=count
        self.pending={'event':event,'type':'attacks','kind':kind,'declarations':declared,'provenance':provenance,
            'staggerDeadline':stagger_deadline,'coverDeadline':cover_deadline,'paidBeforeRolls':True}
        self.events[event]['status']='committed-awaiting-rolls';return deepcopy(self.pending)
    def resolve_attacks(self,event,rolls,*,extra_die=None,con_save=None):
        p=self.pending
        if not p or p['event']!=event or p['type']!='attacks' or len(rolls)!=len(p['declarations']):raise ValueError('Actual unresolved paid attack declaration required')
        if any(not self.world['items'][d['item']]['heldBy']=='owner' for d in p['declarations']):raise ValueError('Attack body/weapon invalidated; actual interruption must be recorded, no cost refund')
        out=[];riders=[];ability_added=False
        for d,r in zip(p['declarations'],rolls):
            if set(r)!={'natural','damageFaces'}:raise ValueError('Only exact attack and native damage dice belong to resolution')
            target=self.world['targets'][d['target']];result=attack_roll(r['natural'],d['attackModifier'],target['ac'])
            count=d['damageCount']*(2 if result['critical'] else 1);faces=r['damageFaces']
            if len(faces)!=count or any(type(x)is not int or not 1<=x<=d['damageSides'] for x in faces):raise ValueError('Actual native damage faces required')
            if p['kind']=='brutal-strike':
                if not isinstance(extra_die,list) or len(extra_die)!=(2 if result['critical'] else 1) or any(type(x)is not int or not 1<=x<=6 for x in extra_die):raise ValueError('Actual fixedS1 dice required')
                save=saving_throw(con_save,target['conSave'],8+self.proficiency()+d['abilityModifier'])
            damage=0
            if result['hit']:
                damage=sum(faces)+d['flatDamage']
                if p['kind']!='quick-shot' and (p['kind']!='twin-strike' or not ability_added):damage+=d['abilityModifier'];ability_added=True
                if p['kind']=='brutal-strike':
                    damage+=sum(extra_die)
                    if not save['success']:riders.append({'kind':'Staggered','target':d['target'],'deadline':p['staggerDeadline'],'attackPenalty':-1,'speedPenalty':-5,'source':event,'donor':p['provenance']['donor']})
                if p['kind']=='covering-fire':riders.append({'kind':'CoveringFire','target':d['target'],'deadline':p['coverDeadline'],'nextAttackAgainstOtherAlly':-2,'source':event,'donor':p['provenance']['donor']})
            out.append({**result,'nativeDamage':max(0,damage),'damageType':d['damageType'],'target':d['target']})
        result={'attacks':out,'borrowedEngineResourcesGenerated':0,'extraAttacksGranted':0}
        self.riders.extend(riders);self.events[event].update(status='resolved',result=deepcopy(result));self.pending=None;return result
    def declare_task(self,event,*,ability='DEX',target=None,mechanism=None):
        choice,card,cost=self.preflight(event,'card');kind=choice.rsplit('.',1)[-1]
        if kind=='disable-device':
            d=self.world['mechanisms'].get(mechanism)
            if not self.world['owner']['usableThievesTools'] or not d or d['magical'] or not d['accessibleInReach']:raise ValueError('Actual tools and accessible nonmagical mechanism required')
            dc=d['dc'] if d['dc'] is not None else 20 if d['complex'] else 15;modifier=self.mod('DEX')+self.proficiency()
        elif kind=='feint':
            t=self.world['targets'].get(target)
            if ability not in {'DEX','CHA'} or not t or abs(t['position']-self.world['owner']['position'])>10 or not t['perceivedBothWays'] or not t['enemy']:raise ValueError('Actual perceived enemy and legal ability required')
            dc=t['passiveInsight'];modifier=self.mod(ability)+self.proficiency()
        else:raise ValueError('Not a permitted task card')
        self.commit(event,choice,card,cost);self.pending={'event':event,'type':'task','kind':kind,'dc':dc,'modifier':modifier,'target':target,'mechanism':mechanism,'paidBeforeRolls':True}
        self.events[event]['status']='committed-awaiting-rolls';return deepcopy(self.pending)
    def resolve_task(self,event,natural):
        p=self.pending
        if not p or p['event']!=event or p['type']!='task':raise ValueError('Actual unresolved paid task required')
        result=task_check(natural,p['modifier'],p['dc'])
        if p['kind']=='disable-device':
            d=self.world['mechanisms'][p['mechanism']]
            if result['success']:d['disarmed']=True
            elif p['dc']-result['total']>=5:d['triggered']=True
            result.update(disarmed=d['disarmed'],triggered=d['triggered'])
        elif result['success']:self.riders.append({'kind':'Feint','target':p['target'],'deadline':self.world['owner']['actualTurnEnd'],'turn':self.turn,'source':event,'nextWeaponAttackAdvantage':True})
        self.events[event].update(status='resolved',result=deepcopy(result));self.pending=None;return result
    def interrupt(self,event,*,actual_authorized_interrupt):
        if not self.pending or self.pending['event']!=event or not actual_authorized_interrupt:raise ValueError('An actual source-authorized interruption of the pending activation is required')
        self.events[event].update(status='interrupted-no-refund',result=None);self.pending=None
    def attacks(self,event,attacks,*,extra_die=None,con_save=None,stagger_deadline=None,cover_deadline=None):
        self.declare_attacks(event,[{k:v for k,v in x.items() if k not in {'natural','damageFaces'}} for x in attacks],stagger_deadline=stagger_deadline,cover_deadline=cover_deadline)
        return self.resolve_attacks(event,[{k:x[k] for k in ['natural','damageFaces']} for x in attacks],extra_die=extra_die,con_save=con_save)
    def task(self,event,natural,*,ability='DEX',target=None,mechanism=None,**unused):
        self.declare_task(event,ability=ability,target=target,mechanism=mechanism);return self.resolve_task(event,natural)
    def move(self,event,path):
        result=super().move(event,path)
        if self.events[event]['choice']=='thief.base.shadow-step':self.shadow_window={'event':event,'turn':self.turn,'position':self.world['owner']['position'],'eventCount':len(self.events)}
        return result
    def hide_after_shadow(self,event,move_event,natural,dc):
        w=self.shadow_window
        if not w or w['event']!=move_event or w['turn']!=self.turn or w['position']!=self.world['owner']['position'] or w['eventCount']!=len(self.events) or not self.world['owner']['canAct']:raise ValueError('Only the immediate same-position/same-turn Shadow Hide window qualifies')
        result=super().hide_after_shadow(event,move_event,natural,dc);self.shadow_window=None;return result
    def claim_next_attack_riders(self,event,*,attacker,target,weapon_attack,actual_legal_attack,target_is_other_ally=False):
        if event in self.consumed_attack_riders:raise ValueError('Same underlying attack cannot claim riders twice')
        if not actual_legal_attack:raise ValueError('No attack permission granted by rider inspection')
        advantage=False;penalty=0;consumed=[];retained=[]
        for r in self.riders:
            feint=r['kind']=='Feint' and self.now<r['deadline'] and attacker=='owner' and weapon_attack and target==r['target'] and self.turn==r['turn']
            cover=r['kind']=='CoveringFire' and self.now<r['deadline'] and attacker==r['target'] and target!='owner' and target_is_other_ally
            if feint or cover:
                advantage=advantage or feint;penalty=min(penalty,-2 if cover else 0);consumed.append(r['source'])
            else:retained.append(r)
        result={'advantage':advantage,'attackModifier':penalty,'consumedSources':consumed,'newAttackGranted':False,'consumedBeforeHitResult':True}
        self.riders=retained;self.consumed_attack_riders[event]=deepcopy(result);return result
