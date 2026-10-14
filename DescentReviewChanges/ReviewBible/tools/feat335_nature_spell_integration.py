"""Nature with finite paid ordinary casts and Fate Coin's original-check lineage.

Supports native Ranger-known Fate Coin and Wizard known Arcane Ray/prepared
Fate Coin. It is not a general spell, counterspell, custody or initiative engine.
"""
from copy import deepcopy
from feat335_nature_transactions import NatureTransactions
from feat_exact_01_acquisition_models import pb
from spell_playtest_rules import quote_cast
from core_playtest_rules import attack_roll


class NatureSpellIntegration(NatureTransactions):
    def __init__(self,*args,spell_sources,**kwargs):
        super().__init__(*args,**kwargs)
        self.spell_sources=spell_sources;self.ranger_known={};self.spell_receipts={};self.coins={};self.coin_history=[]
        self.roll_guards={};self.replacement_receipts={};self.wizard_school=None;self.wizard_matrix_families=set()

    def snapshot(self):
        return {**super().snapshot(),'rangerKnown':deepcopy(self.ranger_known),'spellReceipts':deepcopy(self.spell_receipts),
            'coins':deepcopy(self.coins),'coinHistory':deepcopy(self.coin_history),'rollGuards':deepcopy(self.roll_guards),
            'replacementReceipts':deepcopy(self.replacement_receipts),'wizardSchool':self.wizard_school,'wizardMatrixFamilies':sorted(self.wizard_matrix_families)}

    def learn_ranger_fate_coin(self,event):
        if self.acquired.first!='Ranger' or self.ranger_known or event in self.actor.events:raise ValueError('One actual native Ranger learning subset required')
        level=self.acquired.pay.current_classes['Ranger'];route=self.spell_sources.ordinary('fate-coin','Ranger')
        if level<route['minimumClassLevel'] or route['rank']>self.class_sources['Ranger']['maxSpellRankByClassLevel'][level-1]:raise ValueError('Actual Ranger class gate required')
        # Shared missing-count fallback: 2 ranked spells at first access, +1 at each later even class level.
        first=next(i+1 for i,n in enumerate(self.class_sources['Ranger']['maxSpellRankByClassLevel']) if n>=1)
        capacity=2+sum(i%2==0 for i in range(first+1,level+1))
        self.ranger_known['fate-coin']={'route':route,'learningEvent':event,'learnedAtClassLevel':level,'knownSubsetCount':1,'rankedCapacity':capacity,
            'authority':'CLASS_PLAYTEST_RULES/shared missing repertoire fallback; Ranger has no overriding book/preparation count.'}
        self.actor.events[event]={'kind':'conditional-actual-learning','spellId':'fate-coin','sourceClass':'Ranger'}
        self.version+=1

    def set_wizard_specialization(self,school):
        if self.acquired.first!='Wizard' or self.wizard_school is not None or school not in {'Abjuration','Conjuration','Divination','Enchantment','Evocation','Illusion','Necromancy','Transmutation'}:
            raise ValueError('Actual one-time Wizard specialization selection required')
        self.wizard_school=school
        self.version+=1

    def _spell_route(self,sid):
        first=self.acquired.first;level=self.acquired.pay.current_classes[first]
        if first=='Ranger' and sid=='fate-coin' and sid in self.ranger_known:
            route=deepcopy(self.ranger_known[sid]['route']);ability='WIS'
        elif first=='Wizard' and sid in {'arcane-ray','fate-coin'} and self.wizard_school is not None:
            route=next((deepcopy(r) for r in self.acquired.casting.qualifying() if r['spellId']==sid and r['sourceClass']=='Wizard' and r['kind'] in {'wizard-known','wizard-prepared'}),None)
            if route is None:raise ValueError('Actual current Wizard known/prepared credential required')
            ability='INT'
        else:raise ValueError('This finite integration requires actual Ranger-known or Wizard-owned repertoire')
        current=self.spell_sources.ordinary(sid,first)
        if route['payloadBinding']!=current['payloadBinding'] or route['rank']!=current['rank'] or current['minimumClassLevel']>level:
            raise ValueError('Exact current source-class gate and payload required')
        if route['rank']>self.class_sources[first]['maxSpellRankByClassLevel'][level-1]:raise ValueError('Actual class rank gate required')
        return route,ability

    def _physical_hand(self,hand,*,free=False):
        owner=self.owner
        if hand not in owner['hands'] or not owner['hands'][hand]['usable']:raise ValueError('Actual usable physical hand required')
        if free and owner['hands'][hand]['holding'] is not None:raise ValueError('Actual free receiving hand required')

    def _end_coin(self,coin,status):
        coin['state']=status;held=coin['heldHand']
        if self.owner['hands'][held]['holding']==coin['id']:
            self.owner['hands'][held]['holding']=None;self.owner['freeHands']+=1
        self.coin_history.append(deepcopy(coin))

    def advance(self,now,*,outside_initiative=False):
        super().advance(now,outside_initiative=outside_initiative)
        for coin in self.coins.values():
            if coin['state']=='active' and now>=coin['deadline']:self._end_coin(coin,'expired')

    def declare_spell(self,event,sid,*,expected_version,target=None,hand=None):
        if expected_version!=self.version or self.actor.pending or event in self.actor.events or self.actor.turn is None or self.actor.actions<1:
            raise ValueError('Current version, unused cast identity and actual Action required')
        if not self.owner['conscious'] or not self.owner['canAct'] or self.owner['ordinarySpellProhibited']:raise ValueError('Actual ordinary spell permission required')
        route,ability=self._spell_route(sid);card=self.spell_sources.dependencies[sid]['completeCurrentProcedureCard'];op=card['operational']
        if op['activation']!='Action' or op['concentration'] or op['components'] not in [['V','S'],['V','S','F']]:raise ValueError('Outside this exact finite ordinary cast adapter')
        if self.owner['silenced'] or self.owner['freeHands']<1 or 'F' in op['components'] and not self.owner['hasFocus']:
            raise ValueError('Ordinary spell components still required')
        if sid=='fate-coin':
            if target is not None:raise ValueError('This finite Fate Coin cast is to the caster own hand only')
            self._physical_hand(hand,free=True)
        else:
            t=self.actor.world['spellTargets'].get(target)
            if not t or not t['creature'] or not t['perceived'] or not t['lineOfEffect'] or t['totalCover'] or abs(t['position']-self.owner['position'])>op['rangeFeet']:
                raise ValueError('Actual Arcane Ray target/body/range/line required')
        level=self.acquired.pay.current_classes[self.acquired.first];maximum=self.class_sources[self.acquired.first]['rpByClassLevel'][level-1]
        if self.owner['poolKind']!='personal-RP' or self.owner['poolOwner']!='owner':raise ValueError('Existing personal class RP pool required')
        history=deepcopy(self.spell_history);modifier=(self.acquired.pay.scores[ability]-10)//2;proficiency=pb(sum(self.acquired.pay.current_classes.values()))
        quote=quote_cast(card,self.acquired.first,level,available_spell_ids={sid},rp=self.owner['personalRP'],max_rp=maximum,
            dissonance=history['dissonance'],proficiency=proficiency,casting_modifier=modifier,previous_spell_id=history['previousSpell'],previous_refrain=history['refrain'])
        added=quote['dissonanceAddedBeforeClassInterface'];hooks=[]
        prepared=route.get('kind')=='wizard-prepared'
        if prepared and sid not in self.wizard_matrix_families:
            added-=0 if quote['rank']==0 else 1 if quote['rank']<=5 else 2;hooks.append('first-prepared-matrix-base-exemption')
        stabilization=history['classRecords'].get('ranger-stabilization')
        if self.acquired.first=='Ranger' and stabilization and stabilization['active'] and not stabilization['consumed'] and self.actor.now<stabilization['deadline']:
            added=max(0,added-1);hooks.append('existing-Ranger-single-use-stabilization')
        self.actor.actions-=1;self.owner['personalRP']=quote['rpAfterPayment']
        self.spell_history.update(dissonance=history['dissonance']+added,previousSpell=sid,refrain=quote['refrain'])
        if 'existing-Ranger-single-use-stabilization' in hooks:self.spell_history['classRecords']['ranger-stabilization'].update(active=False,consumed=True,consumedBy=event)
        if prepared:self.wizard_matrix_families.add(sid)
        if self.turn_meta[self.actor.turn]['regular']:self.magical_turns.add(self.actor.turn)
        self.version+=1
        receipt={'type':'ordinary-spell','event':event,'spellId':sid,'route':route,'ability':ability,'modifier':modifier,'proficiency':proficiency,
            'components':deepcopy(op['components']),'quote':quote,'classHooks':hooks,'dissonanceAdded':added,'historyBefore':history,'historyAfter':deepcopy(self.spell_history),
            'target':target,'receivingHand':hand,'committedAt':self.actor.now,'turn':self.actor.turn,'stateVersion':self.version,'paidBeforeOutcome':True,
            'concentrationTransition':'none; these exact two sources are nonconcentration','status':'paid-pending'}
        self.actor.pending=deepcopy(receipt);self.actor.events[event]={'kind':'ordinary-spell','status':'paid-pending'};self.spell_receipts[event]=receipt
        return deepcopy(receipt)

    def resolve_spell(self,event,*,face=None,damage_faces=None):
        p=self.actor.pending
        if not p or p['event']!=event or p['type']!='ordinary-spell':raise ValueError('Current paid pending ordinary spell required')
        if not self.owner['conscious'] or not self.owner['canAct'] or self.owner['ordinarySpellProhibited']:
            result={'resolved':False,'refund':0,'reason':'Current covering incapacity/prohibition'}
        elif p['spellId']=='fate-coin':
            if face is not None or damage_faces is not None:raise ValueError('Fate Coin creation has no flip success roll')
            try:self._physical_hand(p['receivingHand'],free=True)
            except ValueError:result={'resolved':False,'refund':0,'reason':'Original receiving hand no longer qualifies'}
            else:
                for coin in self.coins.values():
                    if coin['state']=='active':self._end_coin(coin,'replaced')
                coin={'id':'coin/'+event,'sourceSpell':'fate-coin','castEvent':event,'sourceBinding':deepcopy(p['route']['payloadBinding']),
                    'caster':'owner','holder':'owner','heldHand':p['receivingHand'],'appliedAt':self.actor.now,'deadline':self.actor.now+3600,
                    'state':'active','ac':10,'hp':1,'massPounds':0.01,'currency':False}
                self.coins[coin['id']]=coin;self.owner['hands'][p['receivingHand']]['holding']=coin['id'];self.owner['freeHands']-=1
                result={'resolved':True,'coin':deepcopy(coin),'refund':0}
        else:
            if type(face) is not int or not 1<=face<=20 or not isinstance(damage_faces,list):raise ValueError('Actual complete spell attack and damage faces required')
            t=self.actor.world['spellTargets'][p['target']];bonus=1 if self.wizard_school==p['route'].get('school') else 0
            attack=attack_roll(face,p['modifier']+p['proficiency']+bonus,t['ac']);count=2 if attack['critical'] else 1
            if len(damage_faces)!=count or any(type(n) is not int or not 1<=n<=6 for n in damage_faces):raise ValueError('Actual Arcane Ray d6 count including ordinary critical rule required')
            raw=sum(damage_faces) if attack['hit'] else 0
            dealt=0 if t['forceImmunity'] else raw//2 if t['forceResistance'] else raw
            before=t['hp'];t['hp']=max(0,before-dealt)
            result={'resolved':True,'attack':attack,'nativeDamage':raw,'afterForceDefense':dealt,'actualHpLoss':before-t['hp'],'hpAfter':t['hp'],'refund':0}
        self.spell_receipts[event].update(status='resolved' if result['resolved'] else 'failed-no-refund',result=deepcopy(result))
        self.actor.events[event].update(status=self.spell_receipts[event]['status'],result=deepcopy(result));self.actor.pending=None;self.version+=1
        return result

    def interrupt(self,event,interrupt_id):
        replacement=self.actor.pending.get('replacementPending') if self.actor.pending else None
        super().interrupt(event,interrupt_id)
        if event in self.spell_receipts:self.spell_receipts[event]['status']='interrupted-no-refund'
        if replacement:
            self.replacement_receipts[replacement]['status']='interrupted-no-refund'
            self.actor.events[replacement]['status']='interrupted-no-refund'

    def roll_check(self,event,faces):
        p=self.actor.pending
        if not p or p['type']!='nature-check' or p['event']!=event or 'originalFaces' in p:raise ValueError('Unrolled original committed check required')
        count=2 if p['mode']=='advantage' else 1
        if not isinstance(faces,list) or len(faces)!=count or any(type(n) is not int or not 1<=n<=20 for n in faces):raise ValueError('Complete original d20 procedure required')
        p.update(originalFaces=list(faces),currentFaces=list(faces),lineageRoot=event,rollPhase='faces-visible-before-consequences',replacementPending=None)
        self.version+=1;return deepcopy(p)

    def commit_coin_reroll(self,event,use_event,coin_id,die_index,*,expected_version):
        p=self.actor.pending;coin=self.coins.get(coin_id)
        if expected_version!=self.version or not p or p['type']!='nature-check' or p['event']!=event or p.get('rollPhase')!='faces-visible-before-consequences' or p.get('replacementPending'):
            raise ValueError('Actual complete visible original roll before consequences required')
        if event in self.roll_guards or use_event in self.actor.events or use_event in self.replacement_receipts:raise ValueError('Original-roll lineage already reserved or identity reused')
        if not coin or coin['state']!='active' or coin['hp']<1 or self.actor.now>=coin['deadline'] or coin['holder']!='owner':raise ValueError('Actual active current held coin required')
        self._physical_hand(coin['heldHand'])
        if self.owner['hands'][coin['heldHand']]['holding']!=coin_id:raise ValueError('Physical custody does not match')
        if self.reactions<1 or not self.owner['reactionLegal'] or not self.owner['conscious'] or not self.owner['canAct']:
            raise ValueError('Actual permitted remaining Reaction required')
        observation=self.actor.world['ownRollObservation']
        if not observation['facesAvailableUnderNormalRules'] or not observation['actualGeneratorPerceived'] or not observation['lineOfEffect'] or observation['distanceFeet']>30:
            raise ValueError('Actual permitted roll information and perceived local generator within30ft required')
        if type(die_index) is not int or not 0<=die_index<len(p['originalFaces']):raise ValueError('Exactly one die of the original complete roll required')
        self.reactions-=1;self._end_coin(coin,'expended');self.roll_guards[event]={'source':'fate-coin','useEvent':use_event,'reservedBeforeReplacement':True}
        receipt={'useEvent':use_event,'source':'fate-coin','coinId':coin_id,'originalCheck':event,'lineageRoot':event,'dieIndex':die_index,
            'facesBefore':list(p['currentFaces']),'status':'paid-awaiting-replacement','reactionSpent':1,'noNewTaskAction':True,'noNewNatureUse':True,'committedAt':self.actor.now}
        self.replacement_receipts[use_event]=receipt;p['replacementPending']=use_event;self.actor.events[use_event]={'kind':'Fate Coin Reaction','status':'paid-awaiting-replacement'}
        self.version+=1;return deepcopy(receipt)

    def resolve_coin_reroll(self,event,use_event,new_face):
        p=self.actor.pending;r=self.replacement_receipts.get(use_event)
        if not p or p['event']!=event or p.get('replacementPending')!=use_event or not r or r['status']!='paid-awaiting-replacement':raise ValueError('Current committed replacement required')
        if type(new_face) is not int or not 1<=new_face<=20:raise ValueError('One mandatory replacement d20 face required')
        p['currentFaces'][r['dieIndex']]=new_face;p['replacementPending']=None;r.update(status='resolved',replacementFace=new_face,facesAfter=list(p['currentFaces']))
        self.actor.events[use_event]['status']='resolved';self.version+=1;return deepcopy(r)

    def finish_check(self,event):
        p=self.actor.pending
        if not p or p['event']!=event or p.get('rollPhase')!='faces-visible-before-consequences' or p.get('replacementPending'):
            raise ValueError('Complete original/replacement faces before one consequence application required')
        faces=list(p['currentFaces']);lineage={'root':event,'originalFaces':list(p['originalFaces']),'finalFaces':faces,'rerollGuard':deepcopy(self.roll_guards.get(event))}
        result=super().resolve_check(event,faces);result['rollLineage']=lineage
        self.actor.events[event]['result']=deepcopy(result);return result

    def resolve_check(self,event,faces):
        # Preserve the old one-call interface only when no face stage has happened.
        self.roll_check(event,faces);return self.finish_check(event)
