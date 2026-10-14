"""Ranger first-class ability/skill slice for Nature; no inferred tool/weapon grants."""
from copy import deepcopy
from feat_exact_01_composite_casting_model import CompositeCastingHistory
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_casting_credential_model import CastingCredentials


class NatureAcquisitions(CompositeCastingHistory):
    def __init__(self,actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources):
        if actor['firstClass']!='Ranger':
            super().__init__(actor,classes,equipment,skills,ancestry,backgrounds,contracts,supplements,sources);return
        self.actor=deepcopy(actor);self.classes=classes;self.equipment=equipment;self.skills=skills
        self.ancestry=ancestry;self.backgrounds=backgrounds;self.contracts=contracts;self.supplements=supplements;self.sources=sources
        self.first='Ranger';self.initializations={}
        self.training_projection=self._ranger_skills()
        self.pay=PaidChoices({n:c['asiClassLevels'] for n,c in classes.items()},{},deepcopy(actor['classLevels']),deepcopy(self.training_projection['scores']),set(contracts)|{'proposal_spell_focus'})
        self.casting=CastingCredentials(sources,sum(actor['classLevels'].values()))

    def _ranger_skills(self):
        actor=self.actor;first=self.classes['Ranger']
        if set(actor['classLevels'])!={'Ranger'} or type(actor['classLevels']['Ranger']) is not int or not 1<=actor['classLevels']['Ranger']<=20 or actor['priorFeatChoices']:
            raise ValueError('Actual single Ranger class and separately earned feat history required')
        if actor['ancestry']!='human' or actor['variant']!='imperial-human' or actor['ancestrySkillChoice']!='Reputation':
            raise ValueError('This finite Ranger witness uses Human/Imperial and chosen Reputation')
        human=next(x for x in self.ancestry['ancestries'] if x['id']=='human');variant=next(x for x in human['variants'] if x['id']=='imperial-human')
        rolls=actor['abilityRolls']
        if set(rolls)!={'STR','DEX','CON','INT','WIS','CHA'} or any(len(d)!=4 or any(type(v) is not int or not 1<=v<=6 for v in d) for d in rolls.values()):
            raise ValueError('Actual six 4d6/drop-lowest premises required')
        scores={k:sum(d)-min(d)+variant['combinedAbilityBonuses'][k] for k,d in rolls.items()}
        if scores!=actor['permanentScores']:raise ValueError('Scores must equal actual rolls and ancestry')
        if actor['background']!='disgraced-noble-scion' or self.backgrounds[actor['background']]['skillsSource']!='History, Persuasion' or actor['backgroundDuplicateSkillChoice']!='Performance':
            raise ValueError('Actual bounded background/duplicate choice required')
        trained={'Reputation':1,'Persuasion':1,'History':1,'Performance':1}
        chosen=actor['selectedClassSkills']
        if len(chosen)!=first['skillChoices'] or len(set(chosen))!=len(chosen) or not set(chosen)<=set(first['skillOptions']) or set(chosen)&set(trained):
            raise ValueError('Actual distinct Ranger starting skill choices required')
        trained.update({s:1 for s in chosen})
        return {'scores':scores,'skills':trained,'receipts':[
            {'credential':'Reputation','source':'human/Versatility','choice':True},
            {'credential':'Persuasion','source':'imperial-human/Social Intuition'},
            {'credential':'History','source':'disgraced-noble-scion'},
            {'credential':'Performance','source':'fixed background duplicate replacement','authority':'CHARACTER_CREATION_PLAYTEST'},
            *[{'credential':s,'source':'Ranger/first-class-skill-choice'} for s in chosen]],
            'totalLevel':sum(actor['classLevels'].values()),'weapons':None,'tools':None,'armor':None,
            'unprojectedSourceTraining':{k:first[k] for k in ['weapons','tools','armor']},
            'scope':'Ability/skill credentials only; null other credentials mean unmodeled, not absent. No Survival-tools equipment alias is invented.'}

    def advance(self,level):
        if self.first!='Ranger':return super().advance(level)
        if type(level) is not int or not self.actor['classLevels']['Ranger']<=level<=20:raise ValueError('Attained Ranger levels move forward')
        self.actor['classLevels']={'Ranger':level};self.pay.current_classes={'Ranger':level};self.casting.moment=level;self.training_projection=self._ranger_skills()

    def prerequisite(self,sid):
        if self.first=='Ranger':raise ValueError('General Ranger feat prerequisites are outside the Nature ability/skill slice')
        return super().prerequisite(sid)
