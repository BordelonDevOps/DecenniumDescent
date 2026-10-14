"""Current-source ancestry credentials and earned-opportunity prerequisite gates.

This is a conditional character projection, not a full acquisition or lineage
conversion system. It creates no legacy ancestry, feat effects or campaign facts.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices

TARGETS = frozenset({
    'contraption_crafter', 'crushing_advance', 'cultural_legacy', 'elvenAccuracy',
    'elven_grace', 'forge', 'glamourborn', 'nightfang_training', 'orcish_fury',
    'orcish_warpath', 'primal_recovery', 'prodigy', 'versatile_mastery',
})
ABILITIES = frozenset({'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'})


def current_lineage(actor, ancestry):
    """Resolve only a real source ancestry/variant pair and its permanent scores."""
    matches = [(i, row) for i, row in enumerate(ancestry['ancestries']) if row['id'] == actor['ancestryId']]
    if len(matches) != 1:
        raise ValueError('A current source ancestry is required; names do not establish legacy credentials')
    ancestry_index, base = matches[0]
    variants = [(i, row) for i, row in enumerate(base['variants']) if row['id'] == actor['variantId']]
    if len(variants) != 1:
        raise ValueError('The variant must actually belong to the chosen source ancestry')
    variant_index, variant = variants[0]
    rolls = actor['abilityRolls']
    if set(rolls) != ABILITIES or any(
        len(dice) != 4 or any(type(die) is not int or not 1 <= die <= 6 for die in dice)
        for dice in rolls.values()
    ):
        raise ValueError('Six actual four-d6/drop-lowest witnesses are required')
    scores = {ability: sum(dice) - min(dice) + variant['combinedAbilityBonuses'].get(ability, 0)
              for ability, dice in rolls.items()}
    if scores != actor['permanentScores']:
        raise ValueError('Permanent scores must apply the combined ancestry/variant increase exactly once')
    return {
        'ancestryId': base['id'], 'lineage': base['name'], 'variantId': variant['id'],
        'ancestryPointer': '/ancestries/' + str(ancestry_index),
        'variantPointer': '/ancestries/' + str(ancestry_index) + '/variants/' + str(variant_index),
        'combinedAbilityBonuses': deepcopy(variant['combinedAbilityBonuses']), 'scores': scores,
    }


class LineagePrerequisites:
    def __init__(self, actor, ancestry, classes, contracts):
        self.actor = deepcopy(actor)
        self.source = current_lineage(actor, ancestry)
        if len(actor['classLevels']) != 1 or 'Warrior' not in actor['classLevels']:
            raise ValueError('This finite projection records only an actual single Warrior progression')
        if type(actor['classLevels']['Warrior']) is not int or not 1 <= actor['classLevels']['Warrior'] <= 20:
            raise ValueError('Invalid attained Warrior level')
        self.contracts = contracts
        self.pay = PaidChoices({name: row['asiClassLevels'] for name, row in classes.items()}, {},
                              deepcopy(actor['classLevels']), deepcopy(self.source['scores']), set(contracts))

    def has_lineage(self, literal_name):
        # No display label, shape, variant nickname, trait name or invented alias contributes.
        return self.source['lineage'] == literal_name

    def prerequisite(self, feat_id):
        if feat_id not in TARGETS:
            raise ValueError('Outside the thirteen current-lineage predicate identities')

        def evaluate(node):
            if node['kind'] == 'actualLineageReceipt':
                return self.has_lineage(node['lineage'])
            if node['kind'] == 'any':
                return bool(node['requirements']) and any(evaluate(child) for child in node['requirements'])
            raise ValueError('Unexpected requirement in the current-lineage cohort')

        return evaluate(self.contracts[feat_id]['requirements'])

    def earned_gate(self, feat_id, opportunity):
        receipt = self.pay.opportunities.get(opportunity)
        return bool(self.prerequisite(feat_id) and receipt is not None and not receipt['spent'])

    def earn(self, level):
        self.pay.earn_class_opportunity('Warrior:' + str(level), 'Warrior', level)

    def advance(self, level):
        if type(level) is not int or not self.pay.current_classes['Warrior'] <= level <= 20:
            raise ValueError('Only attained forward progression is modeled')
        self.actor['classLevels']['Warrior'] = level
        self.pay.current_classes['Warrior'] = level

    def snapshot(self):
        return {'actor': deepcopy(self.actor), 'sourceProjection': deepcopy(self.source),
                'payment': deepcopy(self.pay.__dict__)}
