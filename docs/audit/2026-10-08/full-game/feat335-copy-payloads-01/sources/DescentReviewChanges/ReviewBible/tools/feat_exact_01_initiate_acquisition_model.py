"""Finite, source-linked Magic Initiate acquisition; not a spell-use engine."""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_training_prerequisite_model import materialize_training

class InitiateAcquisitions:
    def __init__(self,actor,classes,equipment,skills,ancestry,backgrounds,contracts,curricula,dependencies):
        if actor['priorFeatChoices']:
            raise ValueError('Supply earlier feats through the paid history, not claimed ownership')
        self.actor=deepcopy(actor);self.classes=classes;self.curricula=curricula;self.dependencies=dependencies
        self.contracts=contracts
        training=materialize_training(actor,classes,equipment,skills,ancestry,backgrounds)
        self.pay=PaidChoices({n:c['asiClassLevels'] for n,c in classes.items()}, {},deepcopy(actor['classLevels']),
                            deepcopy(training['scores']),set(contracts),available_curricula=set(curricula))
        self.routes=[]
        # This finite actor is a Warrior with no ordinary RP pool or class repertoire.
        if actor['firstClass']!='Warrior' or set(actor['classLevels'])!={'Warrior'}:
            raise ValueError('This projection requires the supplied single-class Warrior source slice')
        if any(classes['Warrior']['rpByClassLevel']):
            raise ValueError('Warrior RP chassis changed; revalidate the source projection')
        self.rp={'maximum':0,'current':0}
        self.ordinaryClassRepertoire={}

    def snapshot(self):
        return {'actor':deepcopy(self.actor),'scores':deepcopy(self.pay.scores),
                'paidGrants':deepcopy(self.pay.grants),'opportunities':deepcopy(self.pay.opportunities),
                'featRoutes':deepcopy(self.routes),'rp':deepcopy(self.rp),
                'ordinaryClassRepertoire':deepcopy(self.ordinaryClassRepertoire)}

    def advance(self,level):
        if type(level) is not int or not self.actor['classLevels']['Warrior']<=level<=20:
            raise ValueError('Actual attained Warrior level must move forward')
        self.actor['classLevels']={'Warrior':level};self.pay.current_classes={'Warrior':level}

    def earn(self,level):self.pay.earn_class_opportunity('Warrior:'+str(level),'Warrior',level)

    def acquire(self,sid,level,choice):
        if sid not in self.contracts or (sid!='magicInitiate' and not sid.startswith('magic_initiate_')):
            raise ValueError('Not an actual generic or named Magic Initiate identity')
        if not isinstance(choice,dict) or set(choice)!={'curriculum','cantrips','rank1'}:
            raise ValueError('Record curriculum, two cantrips and one rank-one spell')
        curriculum=choice['curriculum']
        if curriculum not in self.curricula:
            raise ValueError('Curriculum is not one of the actual sixteen finite sources')
        if sid!='magicInitiate' and curriculum!=sid.removeprefix('magic_initiate_').capitalize():
            raise ValueError('Named feat cannot select a different curriculum')
        cantrips=choice['cantrips']
        if not isinstance(cantrips,list) or len(cantrips)!=2 or len(set(cantrips))!=2:
            raise ValueError('Two distinct cantrip identities are required')
        rows=self.curricula[curriculum]['choices'];selected=[]
        for spell_id,rank in [(cantrips[0],0),(cantrips[1],0),(choice['rank1'],1)]:
            matches=[r for r in rows if r['id']==spell_id and r['rank']==rank]
            if len(matches)!=1:
                raise ValueError('Spell is not an exact eligible placement in the chosen curriculum/rank')
            row=matches[0];dep=self.dependencies.get(spell_id)
            if not dep or dep['authoredIndexEntry']['authoredStatus']!='reviewed-authored-operational-playtest':
                raise ValueError('This finite pass supplies reviewed payloads only; no inactive selection is made operative')
            original=dep['originalCatalogRecord']['classAccess'].get(row['sourceClass'])
            if original!=row['fullOriginalClassAccessRow'] or original['rank']!=rank or original['school']!=row['school']:
                raise ValueError('Exact source placement differs from the current curriculum')
            selected.append({**deepcopy(row),'payloadBinding':deepcopy(dep['binding']),
                             'authoredIndexEntry':deepcopy(dep['authoredIndexEntry'])})
        if self.contracts[sid]['requirements']!={'kind':'noPrintedPrerequisite'}:
            raise ValueError('Printed acquisition gate changed; revalidate')
        # A real class opportunity and duplicate-family history still control this None prerequisite.
        record=self.pay.commit(sid,'Warrior:'+str(level),choice=choice,prerequisites_met=True)
        route={'grantIdentity':sid,'paidOpportunity':record['opportunity'],'curriculum':curriculum,
               'castingAbility':self.curricula[curriculum]['featCastingAbility'],
               'spells':selected,'rankOneCharge':{'maximum':1,'current':1},
               'classLevelsGranted':{},'rpPoolGranted':False,'ordinaryPreparedSlotsGranted':0,
               'rankProgressionGranted':False,'independentCostsWaived':False}
        self.routes.append(route)
        return deepcopy(route)

    def initial_grant_matches(self,spell_id=None,school=None,exact_rank=None,minimum_rank=None):
        """Match selected spell entitlements in the initial full-charge snapshot.

        This is not a determination of current executable casting or the broader
        'ability to cast' prerequisite. Depleted charges, suppression, preparation
        loss and temporary casting blocks require separate source interpretation.
"""
        if any(r['rankOneCharge']['current']!=r['rankOneCharge']['maximum'] for r in self.routes):
            raise ValueError('Outside the initial full-charge access snapshot')
        return any((spell_id is None or s['id']==spell_id)
                   and (school is None or s['school']==school)
                   and (exact_rank is None or s['rank']==exact_rank)
                   and (minimum_rank is None or s['rank']>=minimum_rank)
                   for r in self.routes for s in r['spells'])
