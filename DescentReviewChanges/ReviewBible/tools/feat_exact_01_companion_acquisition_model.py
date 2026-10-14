"""Completed conditional Animal Companion acquisition histories.

This validates a supplied successful one-hour history. Rejection means that the
submitted history cannot prove an acquisition; it does not implement interrupted
attempt refunds, a taming system, command phases or an animal combat engine.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import pb
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains


class CompanionAcquisition(RemainingOwnedChains):
    def acquire_companion_from_completed_history(self, level, ordinary_body, receipt, template_id):
        before = self.snapshot()
        body = deepcopy(ordinary_body)
        if self.pay.has('animal_companion') or 'animal_companion' in self.initializations:
            raise ValueError('Nonrepeatable Animal Companion grant already recorded')
        if not self.prerequisite('animal_companion'):
            raise ValueError('Actual Animal Handling proficiency is required')
        required_body = {'id', 'worldId', 'evidenceMode', 'creatureType', 'size', 'living', 'corrupted', 'abilities',
                         'ordinaryMaximumHP', 'ordinaryCurrentHP', 'nativeMovement', 'anatomy', 'breathing',
                         'conditions', 'injuries', 'controllerRelation', 'currentBonds', 'keenSenses'}
        if not required_body <= set(body):
            raise ValueError('Complete existing ordinary body and HP evidence required')
        if body['evidenceMode'] != 'conditional_fixture' or receipt.get('evidenceMode') != 'conditional_fixture':
            raise ValueError('This finite model handles only explicitly conditional records')
        if body['creatureType'] != 'Beast' or not body['living'] or body['corrupted'] or not 0 <= body['abilities']['INT'] < 7:
            raise ValueError('Body must be a living noncorrupted Beast with INT below7')
        old_max, old_current = body['ordinaryMaximumHP'], body['ordinaryCurrentHP']
        if type(old_max) is not int or type(old_current) is not int or not 0 < old_current <= old_max:
            raise ValueError('Actual positive ordinary current/max HP required; no invented full health')
        if body['currentBonds']:
            raise ValueError('Body already has another bond; no additive Ranger/feat chassis')
        relation = body['controllerRelation']
        if relation.get('actorId') != receipt.get('actorId') or relation.get('kind') not in {'willing', 'tamed'}:
            raise ValueError('This body needs an actual declared willing/tamed relationship to this actor')
        if body['worldId'] != receipt.get('worldId') or body['id'] != receipt.get('bodyId'):
            raise ValueError('Bond work and body identity differ')
        if receipt.get('ordinaryProfileBefore') != body:
            raise ValueError('Completed history must preserve the same complete ordinary profile')
        if receipt.get('completedMinutes') != 60 or receipt.get('interruptions') != [] or receipt.get('touchMinutes') != 60:
            raise ValueError('A full uninterrupted hour at touch range is required')
        if receipt.get('firstAttemptInEpoch') != {'epoch': 'initial-acquisition', 'ordinal': 1}:
            raise ValueError('This finite witness supplies only the first initial-allowance attempt')
        if receipt.get('opportunity') != self.first + ':' + str(level):
            raise ValueError('Completed acquisition must use its actual selected opportunity')
        templates = {x['id']: x for x in self.supplements['SUP-02']}
        if template_id not in templates:
            raise ValueError('Unknown source body template')
        native = body['nativeMovement']; anatomy = body['anatomy']
        eligible = {
            'feat-animal.ground': body['size'] in {'Small', 'Medium'} and native.get('walkFeet', 0) > 0 and 'bite' in anatomy,
            'feat-animal.flyer': body['size'] == 'Tiny' and native.get('flyFeet', 0) > 0 and 'wings' in anatomy and bool({'bite', 'peck'} & set(anatomy)),
            'feat-animal.swimmer': body['size'] == 'Small' and native.get('swimFeet', 0) > 0 and 'bite' in anatomy,
        }
        if not eligible[template_id]:
            raise ValueError('Template does not fit the existing body/native movement')
        template = templates[template_id]; total = sum(self.pay.current_classes.values())
        new_max = 5 + total; new_current = max(1, new_max * old_current // old_max)
        allowed_senses = {'sight'} if template_id == 'feat-animal.flyer' else {'hearing', 'smell'}
        available_senses = set(body['keenSenses']) & allowed_senses
        chosen_sense = receipt.get('keenSenseChoice')
        if (available_senses and chosen_sense not in available_senses) or (not available_senses and chosen_sense is not None):
            raise ValueError('No invented keen sense; select one actually sourced permitted sense')
        grant = self.pay.commit('animal_companion', self.first + ':' + str(level),
            choice={'bodyId': body['id'], 'templateId': template_id, 'keenSense': chosen_sense}, prerequisites_met=True)
        self.initializations['animal_companion'] = {
            'ordinaryProfile': body, 'completedHistory': deepcopy(receipt), 'bodyId': body['id'], 'templateId': template_id,
            'currentBody': {'id': body['id'], 'size': body['size'], 'abilities': deepcopy(template['abilities']),
                'movement': deepcopy(template['movement']), 'breathing': deepcopy(body['breathing']),
                'conditions': deepcopy(body['conditions']), 'injuries': deepcopy(body['injuries']),
                'maximumHP': new_max, 'currentHP': new_current, 'AC': 12 + pb(total) // 2,
                'keenSense': chosen_sense, 'controlPhase': 'attached-after-owner-regular-turn'},
            'bondAttemptAllowance': {'maximum': 1, 'current': 0, 'epoch': 'initial-acquisition'},
            'scope': 'Successful completed initial bond only; no replacement, release, commands, mount phase or actual campaign authentication.'}
        return grant

    def advance(self, level):
        super().advance(level)
        if 'animal_companion' in self.initializations:
            current = self.initializations['animal_companion']['currentBody']
            total = sum(self.pay.current_classes.values()); current['maximumHP'] = 5 + total
            current['currentHP'] = min(current['currentHP'], current['maximumHP'])
            current['AC'] = 12 + pb(total) // 2
