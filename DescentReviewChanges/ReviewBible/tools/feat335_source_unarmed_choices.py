"""Finite FAA-03 source-authenticated profile/payment histories.

This projects actual selected ancestry, first-class weapon training and earned
feat payments. Skills, background, HP, equipment, attacks and campaign events are
outside the projection. Conditional loss/body queries establish no world event.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_lineage_prerequisite_model import current_lineage
from feat_exact_01_training_prerequisite_model import weapon_profiles_for
from feat_exact_01_weapon_profile_choices import WeaponProfileChoices, UNARMED

CLAWS = 'troll--claws'


class SourceUnarmedChoices(WeaponProfileChoices):
    def __init__(self, actor, ancestry, classes, equipment, contracts, monk_engine):
        self.actor = deepcopy(actor)
        self.lineage = current_lineage(actor, ancestry)
        self.first = actor['firstClass']
        if self.first not in {'Monk', 'Warrior', 'Thief'}:
            raise ValueError('First class outside this finite profile witness')
        if actor['classLevels'] != {self.first: 1} or actor['priorFeatChoices']:
            raise ValueError('Start with an actual first level and earn each payment')
        self.classes = classes
        self.chassis = classes[self.first]
        self.equipment = equipment
        self.contracts = contracts
        self.monk_engine = monk_engine
        self.pay = PaidChoices({n: r['asiClassLevels'] for n, r in classes.items()}, {},
                              {self.first: 1}, deepcopy(self.lineage['scores']), set(contracts))
        self.weapons = weapon_profiles_for(self.first, equipment)
        self.profile_receipts = {
            wid: {'profile': wid, 'grant': self.first+'/first-class-weapons',
                  'sourceClause': self.chassis['weapons'], 'conditional': False}
            for wid in self.weapons}
        self.weapon_choices = {}  # No inventory-selection menu in this projection.
        self.conditional_profiles = {}
        self.source_unarmed_profiles = {}
        self.events = []
        if self.lineage['ancestryId'] == 'troll':
            base = next(x for x in ancestry['ancestries'] if x['id'] == 'troll')
            i, trait = next((i, x) for i, x in enumerate(base['traits']) if x['id'] == CLAWS)
            if 'Your claws are natural weapons, which you can use to make unarmed strikes.' not in trait['text']:
                raise ValueError('No explicit current Claws/unarmed bridge')
            self.source_unarmed_profiles[CLAWS] = {
                'id': CLAWS, 'category': 'specific natural melee weapon',
                'trait': deepcopy(trait), 'lineageReceipt': deepcopy(self.lineage),
                'traitPointer': self.lineage['ancestryPointer']+'/traits/'+str(i),
                'actualSourceBodyProfile': True, 'attackOrTransformationCreated': False}
            self._cover_claws()
        self.pay.weapon_proficiencies = set(self.weapons)

    def _cover_claws(self):
        if CLAWS in self.source_unarmed_profiles and UNARMED in self.weapons:
            self.weapons.add(CLAWS)
            self.profile_receipts[CLAWS] = {
                'profile': CLAWS, 'grant': deepcopy(self.profile_receipts[UNARMED]['grant']),
                'coveringUnarmedTraining': deepcopy(self.profile_receipts[UNARMED]),
                'traitPointer': self.source_unarmed_profiles[CLAWS]['traitPointer'],
                'bridge': 'FEAT335 FAA-03 / FS-02', 'conditional': False}

    def advance(self, level):
        if type(level) is not int or not self.pay.current_classes[self.first] <= level <= 20:
            raise ValueError('Only actual forward first-class progression is represented')
        self.pay.current_classes[self.first] = level
        self.actor['classLevels'][self.first] = level

    def acquire_tavern_brawler(self, level):
        row = self.contracts['tavern_brawler']
        if (row['requirements'] != {'kind': 'noPrintedPrerequisite'} or
                not row['completeOperativeProcedure'].startswith('Gain actual improvised-weapon and unarmed-strike proficiency.')):
            raise ValueError('Unexpected real Tavern Brawler training clause')
        grant = self.pay.commit('tavern_brawler', self.first+':'+str(level), prerequisites_met=True)
        self.weapons.add(UNARMED)
        self.profile_receipts.setdefault(UNARMED, {
            'profile': UNARMED, 'grant': deepcopy(grant),
            'sourceClause': row['completeOperativeProcedure'], 'conditional': False})
        self._cover_claws()
        self.pay.weapon_proficiencies = set(self.weapons)
        self.events.append({'kind': 'paid-unarmed-training', 'grant': grant,
                            'improvisedProficiencyAlsoGranted': True,
                            'equipmentGranted': [], 'attackOrGrapplePerformed': False})
        return deepcopy(grant)

    def acquire_half(self, *args, **kwargs):
        raise ValueError('Use the separate 40-inventory-profile Weapon Master projection')

    def monk_unarmed_statistics(self):
        if self.first != 'Monk':
            raise ValueError('Class naming or unarmed training alone supplies no Monk progression')
        level = self.pay.current_classes['Monk']
        die = 12 if level >= 17 else 10 if level >= 11 else 8 if level >= 5 else 6
        return {'profile': UNARMED, 'classLevel': level, 'dieSides': die,
                'ability': 'DEX', 'sourceEnginePointer': '/engine/17',
                'sourceText': self.monk_engine, 'attackOrDamagePerformed': False,
                'combinedMonkClawsDamageFormulaSupplied': False}

    def snapshot(self):
        return {'actor': deepcopy(self.actor), 'lineage': deepcopy(self.lineage),
                'payment': deepcopy(self.pay.__dict__), 'weapons': sorted(self.weapons),
                'profileReceipts': deepcopy(self.profile_receipts),
                'sourceUnarmedProfiles': deepcopy(self.source_unarmed_profiles),
                'conditionalProfiles': deepcopy(self.conditional_profiles),
                'events': deepcopy(self.events)}
