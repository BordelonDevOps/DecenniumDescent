"""FW07 finite paid training, ancestry and maximum-HP snapshot composition.

Class/ancestry selections and payments are source-qualified synthetic histories.
Suppression, external later training, form changes and level loss are conditional
probes, not new retraining/campaign mechanics. Full feat use is outside scope.
"""
from copy import deepcopy
from dataclasses import asdict
import re
from feat_exact_01_acquisition_models import FixedTraining,VisionChoice
from feat_exact_01_composite_casting_model import CompositeCastingHistory
from feat_exact_01_prodigy_choices import tool_projection
from feat335_source_unarmed_choices import SourceUnarmedChoices
from maximum_hp_playtest_rules import MaxHpRecord,update_maximum,source_amount
from core_playtest_rules import LifeState

BRANCHING={
 'acrobat':['Acrobatics'],'animalAffinity':['Animal Handling'],
 'athleticProdigy':['Athletics','Acrobatics'],'charismatic':['Persuasion','Deception'],
 'diplomat':['Persuasion','Insight'],'naturalist':['Nature','Survival']}
FIXED={'acrobatic':['Acrobatics'],'ranger_training':['Survival','Nature'],
 'bruiser':['Intimidation'],'deceiver':['Deception'],'hunter':['Survival'],'intimidating':['Intimidation']}
TOOLS={'herbalist':'tools.herbalism-kit','burglar':'tools.thieves-tools'}
HP={'tough','tenacity','tough_as_nails'}


class TrainingSnapshots(CompositeCastingHistory):
    def __init__(self,*args,trade_reference):
        super().__init__(*args)
        self.fixed_training=FixedTraining()
        self.tool_catalog,self.primary=tool_projection(self.equipment,trade_reference)
        self.trades={self.primary[t]:{'level':1,'xp':0} for t in self.training_projection['tools'] if t in self.primary}
        self.tool_grants={}
        self.events=[]

    def _overlay(self):
        for sid,grants in self.fixed_training.branches.items():
            if sid in self.fixed_training.suppressed:continue
            for skill,factor in grants.items():
                self.training_projection['skills'][skill]=max(factor,self.training_projection['skills'].get(skill,0))
        self.training_projection['tools'].update(self.tool_grants.values())

    def advance(self,level):
        super().advance(level)
        if hasattr(self,'fixed_training'):self._overlay()

    def acquire_fixed_training(self,sid,level):
        if sid not in set(BRANCHING)|set(FIXED)|set(TOOLS):raise ValueError('Outside the14 exact FW07 training grants')
        qualified=self.prerequisite(sid)
        before=deepcopy(self.training_projection)
        trial=deepcopy(self.fixed_training)
        if sid in BRANCHING or sid in FIXED:
            names=BRANCHING.get(sid,FIXED.get(sid))
            rules={n:'snapshot-proficiency-or-expertise' if sid in BRANCHING else 'proficiency-only' for n in names}
            branches=trial.acquire(sid,rules,before['skills'])
        else:
            if TOOLS[sid] not in self.tool_catalog:raise ValueError('Missing actual fixed tool profile')
            branches={}
        grant=self.pay.commit(sid,self.first+':'+str(level),prerequisites_met=qualified)
        self.fixed_training=trial
        if sid in TOOLS:
            tool=TOOLS[sid];self.tool_grants[sid]=tool
            # Only Herbalist expressly initializes its mapped trade.
            if sid=='herbalist':self.trades.setdefault(self.primary[tool],{'level':1,'xp':0})
        self._overlay()
        event={'feat':sid,'grant':grant,'beforeSkills':before['skills'],'fixedBranches':branches,
            'fixedTool':TOOLS.get(sid),'physicalItemsGranted':[],'newCoursesOrFacts':[]}
        self.events.append(event)
        return deepcopy(event)

    def snapshot(self):
        return {**super().snapshot(),'fixedTraining':deepcopy(self.fixed_training.__dict__),
                'toolGrants':deepcopy(self.tool_grants),'trades':deepcopy(self.trades),'trainingEvents':deepcopy(self.events)}


class LineageSnapshots(SourceUnarmedChoices):
    def __init__(self,actor,ancestry,classes,equipment,contracts,monk_engine):
        super().__init__(actor,ancestry,classes,equipment,contracts,monk_engine)
        self.initializations={};self.vision={};self.hp_sources={}
        self.independent_vision=[]
        base=next(x for x in ancestry['ancestries'] if x['id']==self.lineage['ancestryId'])
        variant=next(x for x in base['variants'] if x['id']==self.lineage['variantId'])
        self.lineage_traits=deepcopy(base['traits']+variant['traits'])
        for trait in self.lineage_traits:
            if 'darkvision' in trait['name'].lower():
                match=re.search(r'(?:dim light within|darkvision has a radius of) (\d+) feet',trait['text'])
                if not match:raise ValueError('No finite actual darkvision range in this source projection')
                self.independent_vision.append({'sourceTrait':deepcopy(trait),'range':int(match.group(1)),'operative':True})
        self.life=LifeState(self.base_maximum(),7,temp_hp=2)
        self.hp_events=[]

    def base_maximum(self):
        level=sum(self.pay.current_classes.values());con=(self.pay.scores['CON']-10)//2
        return max(1,self.chassis['hitDie']+con)+(level-1)*max(1,self.chassis['fixedLaterLevelHpBase']+con)

    def prerequisite(self,sid):
        def evaluate(node):
            kind=node['kind']
            if kind=='noPrintedPrerequisite':return True
            if kind=='permanentAbility':return self.pay.scores[node['ability']]>=node['minimum']
            if kind=='totalCharacterLevel':return sum(self.pay.current_classes.values())>=node['minimum']
            if kind=='actualLineageReceipt':return self.lineage['lineage']==node['lineage']
            raise ValueError('Unsupported predicate in the finite lineage snapshot cohort')
        return evaluate(self.contracts[sid]['requirements'])

    def acquire_snapshot(self,sid,level):
        if sid not in HP|{'night_hunter','dark_affinity','cultural_legacy'}:raise ValueError('Outside six fixed lineage/HP snapshot identities')
        total=sum(self.pay.current_classes.values())
        if sid=='cultural_legacy' and self.lineage['variantId'] not in {'boom-goblin','scrap-goblin','shadow-goblin'}:
            raise ValueError('Use an actual current Goblin variant; no new variant menu')
        grant=self.pay.commit(sid,self.first+':'+str(level),prerequisites_met=self.prerequisite(sid))
        if sid in {'night_hunter','dark_affinity'}:
            self.vision[sid]=VisionChoice.acquire([x['range'] for x in self.independent_vision])
            self.initializations[sid]={'fixedVisionBranch':self.vision[sid].branch,
                'acquisitionVisionSources':deepcopy(self.independent_vision)}
            if sid=='dark_affinity':self.initializations[sid]['shadowStepUses']={'maximum':1,'current':1}
        elif sid=='cultural_legacy':
            self.initializations[sid]={'fixedVariantId':self.lineage['variantId'],
                'actualLineageReceipt':deepcopy(self.lineage),'sourceTraits':deepcopy(self.lineage_traits),
                'proficiencyGranted':[],'physicalItemsGranted':[]}
        else:
            self.hp_sources[sid]={'acquisitionLevel':total,'paidGrant':deepcopy(grant),
                'levelContributions':{n:2 for n in range(1,total+1)} if sid=='tough_as_nails' else {},
                'activeLevelIds':list(range(1,total+1)) if sid=='tough_as_nails' else []}
            self.recompute_hp()
        return grant

    def recompute_hp(self):
        records=[];level=sum(self.pay.current_classes.values())
        for sid,source in self.hp_sources.items():
            if sid=='tough':amount=source_amount('feat:tough',character_level=source['acquisitionLevel'],acquisition_level=source['acquisitionLevel'])
            elif sid=='tough_as_nails':amount=sum(source['levelContributions'][n] for n in source['activeLevelIds'])
            else:amount=source_amount('feat:tenacity',character_level=level)
            records.append(MaxHpRecord('paid:'+sid,'feat:'+sid,'owner','owner',amount,suppressed=sid in self.pay.suppressed))
        self.life,event=update_maximum(self.life,self.base_maximum(),records,target='owner')
        self.hp_events.append(event)
        return event

    def advance(self,level):
        super().advance(level)
        if hasattr(self,'hp_sources'):
            for sid,source in self.hp_sources.items():
                if sid=='tough_as_nails':
                    for n in range(1,level+1):source['levelContributions'].setdefault(n,2)
                    source['activeLevelIds']=list(range(1,level+1))
            self.recompute_hp()

    def conditional_level_loss_or_restoration(self,level):
        if type(level) is not int or not 1<=level<=20:raise ValueError('Actual bounded level required')
        for source in self.hp_sources.values():
            if source['levelContributions'] and level>max(source['levelContributions']):
                raise ValueError('A restoration cannot invent a level never gained')
        self.actor['classLevels'][self.first]=level;self.pay.current_classes[self.first]=level
        for sid,source in self.hp_sources.items():
            if sid=='tough_as_nails':source['activeLevelIds']=list(range(1,level+1))
        return self.recompute_hp()

    def vision_range(self,sid,conditional_independent_ranges=None):
        ranges=[x['range'] for x in self.independent_vision if x['operative']] if conditional_independent_ranges is None else conditional_independent_ranges
        return self.vision[sid].current(ranges)

    def cultural_bonus(self,ability,skill,task,total,rolled=True):
        record=self.initializations.get('cultural_legacy')
        if not record or not rolled or 'cultural_legacy' in self.pay.suppressed:return 0
        variant=record['fixedVariantId']
        eligible=(skill=='Stealth' or variant=='boom-goblin' and ability=='INT' and task in {'alchemy','explosives','incendiaries'} or
                  variant=='scrap-goblin' and ((ability=='WIS' and skill=='Perception' and task in {'useful-junk','hidden-objects'}) or
                                              (ability=='DEX' and skill=='Sleight of Hand' and task=='hidden-objects')))
        return max(0,total)//10 if eligible else 0

    def snapshot(self):
        return {**super().snapshot(),'initializations':deepcopy(self.initializations),'independentVision':deepcopy(self.independent_vision),
            'visionChoices':{k:deepcopy(v.__dict__) for k,v in self.vision.items()},'hpSources':deepcopy(self.hp_sources),
            'life':asdict(self.life),'hpEvents':deepcopy(self.hp_events)}
