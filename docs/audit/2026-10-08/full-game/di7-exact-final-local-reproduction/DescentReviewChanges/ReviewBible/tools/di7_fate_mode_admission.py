"""Exact current-source admission proofs and a finite paid Lifedraw miss.

Source proofs reject a mode regardless of its possible upstream result. They
do not fabricate cast receipts or claim to execute a summon/recursive spell.
The only admitted child payload adapters remain Coin and Suggestion.
"""
from copy import deepcopy
from di7_alignment_transactions import AlignmentTransactions
from di7_cast_transactions import DI7Sources
from core_playtest_rules import attack_roll
from apply_di7_ap_as_01 import info


class AdmissionSources(DI7Sources):
    def mode_gate(self, sid, provider):
        source = self.ordinary.get(sid)
        if not source or provider not in source['classAccess']:
            return {'admitted': False, 'reason': 'no-actual-source-placement'}
        route = source['classAccess'][provider]
        binding = {**info(self.catalog_path), 'pointer': '/spells/'+str(self.catalog['spells'].index(source))}
        result = {'spellId': sid, 'provider': provider, 'placement': deepcopy(route), 'sourceBinding': binding}
        if type(route['rank']) is not int or not 0 <= route['rank'] <= 7:
            return {**result, 'admitted': False, 'reason': 'actual-rank-outside0-through7'}
        op = source.get('operational')
        if source['status'] != 'operational-playtest-draft' or not op:
            return {**result, 'admitted': False, 'reason': 'no-complete-authorized-operative-adapter'}
        if op['activation'] not in {'Action', 'Bonus Action'}:
            return {**result, 'admitted': False, 'reason': 'not-Action-or-Bonus-Action', 'operativeField': 'activation', 'operativeText': op['activation']}
        forbidden = {
            'lifedraw': ('resolution', 'On hit, deal 3d6 necrotic damage.', 'damaging-mode-even-when-missed'),
            'ray-of-frost': ('effect', '1d8 cold damage', 'damaging-mode-even-when-missed'),
            'summon-lesser-skeleton': ('effect', 'deals 1d6', 'damaging-summon-mode'),
            'arcane-echo': ('resolution', 'generate one repeat permission', 'further-casting-access-mode')}
        if sid in forbidden:
            field, needle, reason = forbidden[sid]
            assert needle in op[field], (sid, field)
            return {**result, 'admitted': False, 'reason': reason, 'operativeField': field, 'operativeText': op[field]}
        if sid not in {'fate-coin', 'alignment-suggestion'}:
            return {**result, 'admitted': False, 'reason': 'indispensable-complete-payload-or-independent-entitlement-adapter-not-supplied',
                'qualification': 'This does not declare the authored mode inherently forbidden. A future explicit source-qualified adapter may establish it.'}
        assert op['activation'] == 'Action' and op['components'] == ['V', 'S', 'F']
        return {**result, 'admitted': True, 'reason': 'complete-selected-current-adapter',
            'independentConsumedMaterials': [], 'independentAcquiredUses': [],
            'qualification': 'Only these exact ordinary spell sources have no independent consumed material or acquired charge. Ordinary focus is still required; no universal cost waiver is inferred.'}

    def spell(self, sid, provider):
        if sid != 'lifedraw': return super().spell(sid, provider)
        source = self.ordinary[sid]
        if provider not in source['classAccess'] or source['status'] != 'operational-playtest-draft' or not source['operational']:
            raise ValueError('Actual complete ordinary Lifedraw source required')
        return deepcopy(source), deepcopy(source['operational']), {**info(self.catalog_path), 'pointer': '/spells/'+str(self.catalog['spells'].index(source))}, False


class FateAdmissionTransactions(AlignmentTransactions):
    def _admit_original(self, actor_id, original_id, *, freshness):
        original = self.casts.get(original_id)
        if original:
            gate = self.sources.mode_gate(original['spellId'], original['provider'])
            if not gate['admitted']:
                raise ValueError(gate['reason'])
        return super()._admit_original(actor_id, original_id, freshness=freshness)

    def _target(self, actor_id, sid, request, op):
        if sid == 'lifedraw':
            target = self._line(actor_id, request.get('target'), op['rangeFeet'])
            if target['kind'] != 'creature': raise ValueError('Actual perceived Lifedraw creature required')
            return
        return super()._target(actor_id, sid, request, op)

    def resolve_lifedraw_miss(self, cast_id, *, natural):
        cast = self.casts.get(cast_id)
        if not cast or cast['spellId'] != 'lifedraw' or cast['status'] != 'pending' or not self.stack or self.stack[-1] != cast_id:
            raise ValueError('Actual top paid Lifedraw required')
        target = self.world['entities'][cast['request']['target']]
        armor = target.get('armor')
        if not armor or not armor.get('authorityEvent'):
            raise ValueError('Actual current source-qualified AC required')
        result = attack_roll(natural, cast['abilityModifier']+cast['proficiency'], armor['value'])
        if result['hit']:
            raise ValueError('This finite miss adapter does not supply hit damage/healing resolution')
        _, op, _, _ = self.sources.spell('lifedraw', cast['provider'])
        self._target(cast['actor'], 'lifedraw', cast['request'], op)
        if not self.actors[cast['actor']]['body']['canAct'] or not self.actors[cast['actor']]['body']['conscious']:
            raise ValueError('Actual surviving casting body required')
        self.stack.pop()
        cast.update(status='resolved', resolvedAt=self.now, castingCompletedAt=self.now,
            result={'attack':result, 'damage':0, 'healing':0, 'sourceModeStillDamaging':True})
        return deepcopy(cast['result'])
