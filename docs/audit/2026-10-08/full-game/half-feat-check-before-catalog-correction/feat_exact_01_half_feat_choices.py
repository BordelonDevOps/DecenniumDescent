"""Permanent half-feat choices and capacity-only changes in a first-class slice.

No equipment use, combat, rest, multiclass or complete class-card build is
simulated. Hit-point records use the actual class's fixed later-level option.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices, pb
from feat_exact_01_training_prerequisite_model import materialize_training


MENUS = {
    'athlete': ('STR', 'DEX'), 'durable': ('CON',), 'heavily_armored': ('STR',),
    'lightly_armored': ('STR', 'DEX'), 'moderately_armored': ('STR', 'DEX'),
    'observant': ('INT', 'WIS'), 'resilient': ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'),
    'weapon_master': ('STR', 'DEX'),
}


class HalfFeatChoices:
    def __init__(self, actor, classes, equipment, skills, ancestry, backgrounds, contracts, actual_items):
        if actor['priorFeatChoices'] or actor['classLevels'] != {actor['firstClass']: 1}:
            raise ValueError('Begin at actual first level and earn every feat here')
        self.actor = deepcopy(actor); self.classes = classes; self.equipment = equipment; self.skills = skills; self.contracts = contracts
        self.training = materialize_training(actor, classes, equipment, skills, ancestry, backgrounds)
        self.first = actor['firstClass']; self.chassis = classes[self.first]
        self.pay = PaidChoices({n: r['asiClassLevels'] for n, r in classes.items()}, {}, {self.first: 1}, deepcopy(self.training['scores']), set(contracts))
        self.armor = set(self.training['armor']) - {'none'}; self.weapons = set(self.training['weapons'])
        self.saves = set(self.chassis['savingThrowProficiencies']); self.pay.save_proficiencies = set(self.saves)
        self.weapon_choices = {r['id']: deepcopy(r) for r in actual_items if 'weapons' in r['category'].lower() and
                               r['status'] == 'reviewed-authored-playtest' and {'Damage', 'Properties'} <= set(r['sourceFields'])}
        self.hp_bases = [self.chassis['hitDie']]; self.hp_max = self.maximum_hp(); self.hp_current = self.hp_max
        self.hit_dice_unspent = 1; self.rp_max = self.chassis['rpByClassLevel'][0]; self.rp_current = self.rp_max
        self.wounds = 0; self.events = []

    def maximum_hp(self):
        con = (self.pay.scores['CON'] - 10)//2
        return sum(max(1, base + con) for base in self.hp_bases)

    def recalculate(self):
        self.hp_max = self.maximum_hp(); self.hp_current = min(self.hp_current, self.hp_max)
        self.rp_max = self.chassis['rpByClassLevel'][self.pay.current_classes[self.first]-1]
        self.rp_current = min(self.rp_current, self.rp_max)

    def advance(self, level):
        old = self.pay.current_classes[self.first]
        if type(level) is not int or not old <= level <= 20:
            raise ValueError('Invalid actual class advancement')
        for attained in range(old + 1, level + 1):
            self.hp_bases.append(self.chassis['fixedLaterLevelHpBase']); self.hit_dice_unspent += 1
            self.pay.current_classes[self.first] = attained; self.actor['classLevels'][self.first] = attained
            self.recalculate()

    def earn(self, level):
        self.pay.earn_class_opportunity(self.first + ':' + str(level), self.first, level)

    def asi(self, level, allocation):
        grant = self.pay.commit('abilityScoreImprovement', self.first + ':' + str(level), choice=allocation,
                                prerequisites_met=self.contracts['abilityScoreImprovement']['requirements'] == {'kind': 'noPrintedPrerequisite'})
        self.recalculate(); self.events.append({'kind': 'ASI', 'grant': grant}); return grant

    def acquire(self, sid, level, ability, weapons=None):
        if sid not in MENUS or ability not in MENUS[sid]:
            raise ValueError('Choose exactly one ability from this actual feat menu')
        if sid != 'weapon_master' and weapons is not None:
            raise ValueError('This feat has no weapon selection')
        if sid == 'weapon_master':
            if not isinstance(weapons, list) or len(weapons) != 4 or len(set(weapons)) != 4 or not set(weapons) <= set(self.weapon_choices):
                raise ValueError('Select four distinct actual complete current catalog weapon profiles')
        required = self.contracts[sid]['requirements']
        if required['kind'] == 'noPrintedPrerequisite':
            qualified = True
        elif required['kind'] == 'actualProficiency' and required['credential'] in {'light armor', 'medium armor'}:
            qualified = required['credential'].removesuffix(' armor') in self.armor
        else:
            raise ValueError('Outside the exact acquired proficiency gates')
        before_score = self.pay.scores[ability]
        increase = max(0, min(1, 20-before_score))
        before = self.snapshot()
        choice = {'ability': ability, 'weapons': weapons} if sid == 'weapon_master' else ability
        grant = self.pay.commit(sid, self.first + ':' + str(level), choice=choice, prerequisites_met=qualified)
        if sid != 'resilient':
            self.pay.scores[ability] += increase
        else:
            self.saves = set(self.pay.save_proficiencies)
        self.armor.update({'heavily_armored': {'heavy'}, 'lightly_armored': {'light', 'shields'},
                           'moderately_armored': {'medium', 'shields'}}.get(sid, set()))
        if sid == 'weapon_master':
            self.weapons.update(weapons)
        self.recalculate()
        event = {'kind': 'half-feat', 'feat': sid, 'ability': ability, 'actualScoreIncrease': increase,
                 'scoreBefore': before_score, 'scoreAfter': self.pay.scores[ability], 'grant': grant,
                 'hpMaximumBefore': before['hp']['maximum'], 'hpMaximumAfter': self.hp_max,
                 'hpCurrentBefore': before['hp']['current'], 'hpCurrentAfter': self.hp_current,
                 'ordinaryHealingPerformed': False, 'resourceRecoveryPerformed': False, 'equipmentGranted': []}
        self.events.append(event); return deepcopy(event)

    def passive(self, skill):
        if skill not in {'Perception', 'Investigation'}:
            raise ValueError('Outside the two actual Observant recipients')
        ability = self.skills[skill]; factor = self.training['skills'].get(skill, 0)
        return 10 + (self.pay.scores[ability]-10)//2 + factor*pb(self.pay.current_classes[self.first]) + (5 if self.pay.has('observant') else 0)

    def snapshot(self):
        return {'actor': deepcopy(self.actor), 'payment': deepcopy(self.pay.__dict__),
                'armor': sorted(self.armor), 'weapons': sorted(self.weapons), 'saves': sorted(self.saves),
                'hp': {'bases': list(self.hp_bases), 'maximum': self.hp_max, 'current': self.hp_current, 'wounds': self.wounds},
                'resources': {'unspentHitDice': self.hit_dice_unspent, 'maximumRP': self.rp_max, 'currentRP': self.rp_current},
                'events': deepcopy(self.events)}
