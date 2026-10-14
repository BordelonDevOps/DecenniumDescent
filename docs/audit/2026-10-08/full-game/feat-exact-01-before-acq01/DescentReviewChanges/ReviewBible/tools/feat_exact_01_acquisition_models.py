"""Bounded acquisition-history models, separate from the game application.

Source ownership/acquisition prerequisites are validated outside these models;
they exercise the explicitly named permanent-score, choice and history rules.
"""
from dataclasses import dataclass,field
from copy import deepcopy


def pb(total_level):
    if not 1<=total_level<=20:raise ValueError('Invalid character level')
    return 2+(total_level-1)//4


def permanent_skill_modifier(score,total_level,proficiency_factor):
    if proficiency_factor not in {1,2}:raise ValueError('Actual proficiency or replacing Expertise required')
    return (score-10)//2+pb(total_level)*proficiency_factor


def ability_gate(permanent,minimum,temporary=0):
    return permanent>=minimum  # Deliberately excludes the temporary modifier.


@dataclass
class PaidChoices:
    class_schedules: dict
    mutation_pairs: dict
    current_classes: dict
    scores: dict
    available_curricula: set = field(default_factory=set)
    armor_proficiencies: set = field(default_factory=set)
    weapon_proficiencies: set = field(default_factory=set)
    save_proficiencies: set = field(default_factory=set)
    opportunities: dict = field(default_factory=dict)
    grants: list = field(default_factory=list)
    suppressed: set = field(default_factory=set)

    def earn_class_opportunity(self,identity,class_name,class_level):
        if identity in self.opportunities:raise ValueError('Opportunity identity already recorded')
        if class_level not in self.class_schedules.get(class_name,[]) or self.current_classes.get(class_name,0)<class_level:
            raise ValueError('No actual class-scheduled opportunity')
        source=(class_name,class_level)
        if any(x['source']==source for x in self.opportunities.values()):raise ValueError('Same class opportunity under another name')
        self.opportunities[identity]={'source':source,'spent':False}

    def canonical(self,sid):return self.mutation_pairs.get(sid,sid)

    def has(self,sid):return any(x['identity']==self.canonical(sid) for x in self.grants)

    def commit(self,sid,opportunity,choice=None,prerequisites_met=False):
        """Prerequisite truth is an explicit supplied premise, not a bypass in a builder."""
        sid=self.canonical(sid)
        if not prerequisites_met:raise ValueError('Prerequisites not established')
        op=self.opportunities.get(opportunity)
        if op is None or op['spent']:raise ValueError('No unspent earned opportunity')
        prior=[x for x in self.grants if x['identity']==sid]
        scores=deepcopy(self.scores)
        if sid=='abilityScoreImprovement':
            if not isinstance(choice,dict) or sorted(choice.values()) not in [[2],[1,1]] or any(k not in scores for k in choice):
                raise ValueError('Full +2 or two distinct +1 allocation required')
            for k,n in choice.items():
                if scores[k]+n>20:raise ValueError('Full ASI allocation exceeds ceiling')
                scores[k]+=n
        elif sid=='armorProficiency':
            if choice not in {'light','medium','heavy'} or choice in self.armor_proficiencies:
                raise ValueError('Choose a genuinely missing armor tier')
        elif sid=='resilient':
            if choice not in scores or any(x['choice']==choice for x in prior):raise ValueError('Choose a different save ability')
            scores[choice]+=max(0,min(1,20-scores[choice]))
        elif sid=='weaponFocus':
            if choice not in self.weapon_proficiencies or any(x['choice']==choice for x in prior):raise ValueError('Choose another actually proficient weapon profile')
        elif prior:raise ValueError('Nonrepeatable identity already acquired')
        if sid=='magicInitiate' or sid.startswith('magic_initiate_'):
            if sid=='magicInitiate':
                if not isinstance(choice,dict) or 'curriculum' not in choice:raise ValueError('Missing actual curriculum choice')
                curriculum=choice['curriculum']
            else:curriculum=sid.removeprefix('magic_initiate_').capitalize()
            if curriculum not in self.available_curricula:raise ValueError('Not a supplied finite curriculum')
            for g in self.grants:
                if g.get('curriculum')==curriculum:raise ValueError('Same Magic Initiate curriculum already acquired')
        else:curriculum=None
        record={'identity':sid,'opportunity':opportunity,'choice':deepcopy(choice),'abilitySnapshotBefore':deepcopy(self.scores)}
        if curriculum is not None:record['curriculum']=curriculum
        self.grants.append(record);op['spent']=True;self.scores=scores
        if sid=='armorProficiency':self.armor_proficiencies.add(choice)
        if sid=='resilient':self.save_proficiencies.add(choice)
        return deepcopy(record)

    def suppress(self,sid,value=True):
        sid=self.canonical(sid)
        if value:self.suppressed.add(sid)
        else:self.suppressed.discard(sid)

    def weapon_focus_operative(self,profile):
        return 'weaponFocus' not in self.suppressed and profile in self.weapon_proficiencies and any(
            x['identity']=='weaponFocus' and x['choice']==profile for x in self.grants)


@dataclass
class FixedTraining:
    branches: dict = field(default_factory=dict)
    suppressed: set = field(default_factory=set)
    def acquire(self,sid,rules,before):
        if sid in self.branches:raise ValueError('Training snapshot already recorded')
        out={}
        for name,rule in rules.items():
            if before.get(name,0) not in {0,1,2}:raise ValueError('Invalid proficiency contribution')
            out[name]=2 if rule=='snapshot-proficiency-or-expertise' and before.get(name,0)>=1 else 1
        self.branches[sid]=out
        return deepcopy(out)
    def contribution(self,sid,skill,independent=0):
        owned=0 if sid in self.suppressed else self.branches[sid].get(skill,0)
        return max(independent,owned)


@dataclass
class FiniteFeatUse:
    maximum: int
    current: int
    initialized: bool = True
    operative: bool = True
    completed_rests: set = field(default_factory=set)
    def spend(self,n=1):
        if not self.operative or n<1 or self.current<n:raise ValueError('Unavailable finite use')
        self.current-=n
    def capacity(self,n):
        if n<0:raise ValueError('Negative capacity')
        self.maximum=n;self.current=min(self.current,n)
    def reacquire(self):
        if self.initialized:raise ValueError('Acquisition history already initialized')
    def rest(self,identity,beneficial):
        if not beneficial or identity in self.completed_rests:return False
        self.completed_rests.add(identity);self.current=self.maximum;return True


@dataclass
class VisionChoice:
    branch: str
    operative: bool = True
    @classmethod
    def acquire(cls,independent_ranges):return cls('extension30' if independent_ranges else 'base60')
    def current(self,independent_ranges):
        base=max([0]+independent_ranges)
        if not self.operative:return base
        if self.branch=='base60':return max(base,60)
        if self.branch=='extension30':return base+30 if base else 0
        raise ValueError('Invalid fixed vision branch')
