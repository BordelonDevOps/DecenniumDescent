"""Mass Revelation's four conditional information categories and observer effects.

Actual trap/magic/intent/assertion facts and senses/protection/channel permissions
are Director-established premises. This layer performs the paid snapshot and
does not invent facts, disarm traps, grant senses or implement language inference.
"""
from copy import deepcopy
from di7_area_geometry import AreaGeometryTransactions
from di7_vision_transactions import ConditionalInformation
from condition_playtest_rules import attack_condition_modifiers


class MassTransactions(AreaGeometryTransactions):
    def __init__(self,*args,dossier,records,assertions,**kwargs):
        super().__init__(*args,**kwargs)
        self.information=ConditionalInformation(dossier); self.records=deepcopy(records); self.assertions=deepcopy(assertions)
        self.revelations={}; self.knowledge={}; self.communications=[]
        for record in self.records.values():
            if not record.get('authorityEvent') or not record.get('sourceVersion'):
                raise ValueError('Actual categorized world-record provenance required')
            if record['category'] not in {'trap','enemy','magic'}: raise ValueError('Unsupported actual record category')

    def snapshot(self):
        return {**super().snapshot(),'privateInformationDossier':deepcopy(self.information.data),'actualRecords':deepcopy(self.records),
            'assertions':deepcopy(self.assertions),'revelations':deepcopy(self.revelations),'knowledge':deepcopy(self.knowledge),'communications':deepcopy(self.communications)}

    def _value(self,fid):
        projected=self.information.project(fid,now=self.now)
        return projected.get('value') if projected else None

    def _actual(self,fid):
        fact=self.information.data['facts'].get(fid)
        return fact['publicFields'].get('value') if fact and fact['establishedAt']<=self.now else None

    def _hostile(self,intent,caster):
        party={caster,*self.world['currentParty'][caster]}
        return isinstance(intent,dict) and intent.get('state') in {'intending','executing'} and intent.get('meaningfulHostileAct') is True and bool(party.intersection(intent.get('targetIds',[])))

    def _remember_location(self,observer,subject,revision,footprint,*,cast_id):
        self.knowledge.setdefault(observer,{})[subject]={'revision':revision,'localFootprint':deepcopy(footprint),'snapshotCast':cast_id,'learnedAt':self.now}
        creature=self.world['creatures'].get(subject)
        if creature and creature['locationRevision']==revision:
            state=self.world['observerStates'].get(observer+'>'+subject)
            if state: state['hidden']=False

    def knows_current_location(self,observer,subject):
        receipt=self.knowledge.get(observer,{}).get(subject); creature=self.world['creatures'].get(subject)
        return bool(receipt and creature and receipt['revision']==creature['locationRevision'])

    def resolve_mass(self,cast_id):
        cast=self.casts[cast_id]
        if cast['spellId']!='mass-revelation': raise ValueError('Actual paid Mass Revelation required')
        gate=self.resolve_area_geometry(cast_id)
        if gate is None: return None
        caster=cast['actor']; readable={p['portionId']:p for p in gate['readableSpatialPortions']}
        public={'traps':[],'enemies':[],'magic':[],'lies':[]}; private={}; next_reference=1
        def add(category,row,metadata=None):
            nonlocal next_reference
            reference='reading-'+str(next_reference); next_reference+=1
            row={'reference':reference,**row}; public[category].append(row)
            if metadata: private[reference]=metadata
            return reference
        for record in self.records.values():
            if not record['existsNow']: continue
            local=[readable[p] for p in record['portionIds'] if p in readable]
            if not local or self._value(record['existenceFact']) is not True: continue
            kind=record['category']
            if kind=='trap' and record.get('actualPhysicalTrap') is not True: continue
            if kind=='magic' and record.get('actuallyMagical') is not True: continue
            if kind=='enemy':
                # An alignment, species, caller flag or reputation cannot supply
                # either actual hostile intent or readable knowledge of it.
                if not self._hostile(self._actual(record['intentFact']),caster) or not self._hostile(self._value(record['intentFact']),caster): continue
            location_readable=self._value(record['locationFact']) is True
            footprint=[p['localFootprint'] for p in local] if location_readable else 'Indeterminate'
            row={'localFootprint':footprint}
            if kind=='trap':
                for field in ['armedState','immediateTriggerCategory']:
                    value=self._value(record['fieldFacts'].get(field)); row[field]='Indeterminate' if value is None else value
                add('traps',row)
            elif kind=='magic':
                for field in ['spellOrNonspell','school','rank','state']:
                    value=self._value(record['fieldFacts'].get(field)); row[field]='Indeterminate' if value is None else value
                add('magic',row)
            else:
                subject=record['subject']; revision=self.world['creatures'][subject]['locationRevision']
                metadata={'subject':subject,'revision':revision,'localFootprint':deepcopy(footprint)} if location_readable else None
                add('enemies',row,metadata)
                if location_readable: self._remember_location(caster,subject,revision,footprint,cast_id=cast_id)
        for assertion in self.assertions:
            if not assertion.get('authorityEvent') or assertion['semanticKind']!='actual-assertion': continue
            if not self.now-6<=assertion['at']<=self.now: continue
            speaker=self.world['creatures'].get(assertion['speaker'])
            if not speaker or not any(p in readable for p in speaker['currentPortions']): continue
            reception=assertion['actualReception'].get(caster)
            if not reception or not reception['authorityEvent'] or not reception['perceived'] or not reception['understood']: continue
            if self._value(assertion['existenceFact']) is not True: continue
            # Truth of the proposition is deliberately not used. The supplied
            # fact concerns the speaker's actual knowledge/belief at assertion.
            if self._actual(assertion['beliefFact']) is not True or self._value(assertion['beliefFact']) is not True: continue
            add('lies',{'understoodAssertion':reception['understoodAssertion'],'assertedAt':assertion['at'],'deliberateDeception':True})
        public['readableEnemyCount']=len(public['enemies'])
        public['scope']='Instantaneous readable snapshot; undefined/protected information is not certified absent.'
        self.revelations[cast_id]={'caster':caster,'at':self.now,'public':public,'privateLocationBindings':private}
        cast.update(status='resolved',resolvedAt=self.now,castingCompletedAt=self.now,informationPayloadExecuted=True,privateRecipient=caster)
        return deepcopy(public)

    def attack_modifiers(self,attacker,target,*,other_advantage=False,other_disadvantage=False):
        return attack_condition_modifiers(self.world['creatures'][attacker]['conditions'],self.world['creatures'][target]['conditions'],
            attacker_invisible_location_known=self.knows_current_location(target,attacker),target_invisible_location_known=self.knows_current_location(attacker,target),
            other_advantage=other_advantage,other_disadvantage=other_disadvantage)

    def communicate(self,cast_id,listener,channel_id):
        revelation=self.revelations[cast_id]; channel=self.world['informationChannels'].get(channel_id)
        if not channel or not channel['authorityEvent'] or channel['from']!=revelation['caster'] or channel['to']!=listener or channel['at']!=self.now or not channel['received'] or not channel['understood']:
            raise ValueError('Actual authorized delivered and understood channel event required')
        if any(x['channelId']==channel_id for x in self.communications): raise ValueError('Communication event cannot be replayed')
        delivered=channel['deliveredRecords']; available=[r for category in ['traps','enemies','magic','lies'] for r in revelation['public'][category]]
        if not delivered or any(row not in available for row in delivered): raise ValueError('Only the actual literal delivered snapshot records are implemented')
        for row in delivered:
            meta=revelation['privateLocationBindings'].get(row['reference'])
            if meta: self._remember_location(listener,meta['subject'],meta['revision'],meta['localFootprint'],cast_id=cast_id)
        receipt={'channelId':channel_id,'at':self.now,'listener':listener,'deliveredRecords':deepcopy(delivered)}
        self.communications.append(receipt); return deepcopy(receipt)
