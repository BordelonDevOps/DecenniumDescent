"""Bounded paid ownership chains, using source-derived training and real ASIs.

This models acquisition prerequisites and the named selection/initialization
fields only. It is not a class builder, combat engine or proof of campaign awards.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices, VisionChoice
from feat_exact_01_training_prerequisite_model import materialize_training, meets_training_prerequisite

TARGETS = {
    'alertness_improved','athlete_improved','climber_improved','martial_adept_advanced',
    'giant_slayer','life_drinker','precision_strike','quickened_thought','slayer_s_resolve','undying_flesh',
}
PARENTS = {
    'alert','alertness','athlete','climber','martialAdept','dark_affinity','hemocraft',
    'weaponFocus','arcane_calculus','temporal_theory','favored_enemy_dragon','necrotic_affinity',
    'dark_fortitude','abilityScoreImprovement',
}

class OwnershipChain:
    def __init__(self, actor, classes, equipment, skill_abilities, ancestry, backgrounds, contracts, maneuvers):
        self.actor=deepcopy(actor)
        if actor['priorFeatChoices']:
            raise ValueError('All prior feats must be earned and bought through this history')
        self.first=actor['firstClass']
        self.classes=classes;self.equipment=equipment;self.skills=skill_abilities
        self.ancestry=ancestry;self.backgrounds=backgrounds;self.contracts=contracts
        self.maneuvers=set(maneuvers)
        initial=materialize_training(actor,classes,equipment,skill_abilities,ancestry,backgrounds)
        self.pay=PaidChoices({name:row['asiClassLevels'] for name,row in classes.items()}, {},
                            deepcopy(actor['classLevels']),deepcopy(initial['scores']),set(contracts),
                            weapon_proficiencies=set(initial['weapons']))
        self.initializations={}

    def snapshot(self):
        return {'actor':deepcopy(self.actor),'payment':deepcopy(self.pay.__dict__),
                'initializations':deepcopy(self.initializations)}

    def training(self):
        result=materialize_training(self.actor,self.classes,self.equipment,self.skills,self.ancestry,self.backgrounds)
        # Permanent increases are recorded in the paid history; they are not new rolls.
        result['scores']=deepcopy(self.pay.scores)
        return result

    def advance(self,level):
        old=self.actor['classLevels'][self.first]
        if type(level) is not int or not old<=level<=20:
            raise ValueError('History must advance through attained legal class levels')
        self.actor['classLevels']={self.first:level};self.pay.current_classes={self.first:level}
        for sid in ['hemocraft','life_drinker']:
            if sid in self.initializations:
                reserve=self.initializations[sid]['recoveryReserve']
                reserve['maximum']=2*level
                reserve['current']=min(reserve['current'],reserve['maximum'])

    def earn(self,class_level):
        self.pay.earn_class_opportunity(self.first+':'+str(class_level),self.first,class_level)

    def prerequisite(self,sid,choice=None):
        t=self.training();actor=deepcopy(self.actor)
        if sid=='weaponFocus':actor['weaponChoice']=choice
        def evaluate(node):
            if node['kind']=='ownedFeat':
                return self.pay.has(node['id'])
            if node['kind']=='all':
                return bool(node['requirements']) and all(evaluate(x) for x in node['requirements'])
            if node['kind']=='any':
                return bool(node['requirements']) and any(evaluate(x) for x in node['requirements'])
            return meets_training_prerequisite(node,actor,t,self.equipment,self.skills)
        return evaluate(self.contracts[sid]['requirements'])

    def acquire(self,sid,at_class_level,choice=None):
        if sid not in TARGETS|PARENTS:
            raise ValueError('Identity outside this finite owned-feat cohort')
        qualified=self.prerequisite(sid,choice)
        if not qualified:
            raise ValueError('Actual source prerequisite not established by the paid history')
        additions={}
        if sid=='athlete':
            if choice not in {'STR','DEX'}:
                raise ValueError('Athlete requires a permanent Strength or Dexterity choice')
            additions={'ability':choice,'increase':max(0,min(1,20-self.pay.scores[choice]))}
        if sid in {'martialAdept','martial_adept_advanced'}:
            if not isinstance(choice,list) or len(choice)!=2 or len(set(choice))!=2 or not set(choice)<=self.maneuvers:
                raise ValueError('Choose two different entries from the actual six-maneuver menu')
            if sid=='martial_adept_advanced':
                known=self.initializations['martialAdept']['maneuverIds']
                if set(choice)&set(known):
                    raise ValueError('Advanced choices must be two additional maneuvers')
            additions={'maneuverIds':deepcopy(choice)}
        if sid=='dark_affinity':
            # These witnesses supply no independent darkvision source; no class-card grants are inferred.
            if choice!={'independentDarkvisionRanges':[]}:
                raise ValueError('This source slice establishes only the no-independent-darkvision branch')
            additions={'darkvisionBranch':VisionChoice.acquire([]).branch,'teleportUses':{'maximum':1,'current':1}}
        if sid=='hemocraft':
            if choice not in {'INT','CHA'}:
                raise ValueError('Hemocraft requires its permanent Intelligence or Charisma DC choice')
            additions={'governingAbility':choice,'recoveryReserve':{'maximum':2*self.training()['totalLevel'],'current':0}}
        if sid=='life_drinker':
            additions={'recoveryReserve':{'maximum':2*self.training()['totalLevel'],'current':2*self.training()['totalLevel']}}
        # PaidChoices validates real opportunities, identity/repetition and Weapon Focus/ASI choices atomically.
        record=self.pay.commit(sid,self.first+':'+str(at_class_level),choice=choice,prerequisites_met=qualified)
        if sid=='athlete':self.pay.scores[choice]+=additions['increase']
        if sid=='martialAdept':additions['superiorityPool']={'die':'d6','maximum':1,'current':1}
        if sid=='martial_adept_advanced':
            parent=self.initializations['martialAdept']
            parent['maneuverIds'].extend(choice)
            parent['superiorityPool']['maximum']+=1
            parent['superiorityPool']['current']+=1
            additions['sharedPoolOwner']='martialAdept'
        if additions:self.initializations[sid]=additions
        return record
