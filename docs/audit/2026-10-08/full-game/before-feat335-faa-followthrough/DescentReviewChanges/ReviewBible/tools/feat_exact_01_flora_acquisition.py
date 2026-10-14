"""Complete Conjure Flora's missing mandatory route and current-level snapshot.

Earlier source-bound parent models stay unchanged so their historical evidence
remains reproducible. This override supplies the already-authored SUP07 DC
choice; it introduces no source rule, plant use or casting-engine grant.
"""
from copy import deepcopy
from feat_exact_01_casting_selections import CastingSelections
from feat_exact_01_acquisition_models import pb


class FloraAcquisition(CastingSelections):
    def acquire_named(self, sid, level, choice=None):
        if sid != 'conjure_flora':
            return super().acquire_named(sid, level, choice)
        if not self.prerequisite(sid):
            raise ValueError('Actual retained personal casting and Nature proficiency are required')
        if choice not in self.actual_casting_routes():
            raise ValueError('SUP07 requires one exact possessed casting route at acquisition')
        total = sum(self.pay.current_classes.values())
        initial = {'fixedCastingRoute': deepcopy(choice),
                   'creationUses': {'maximum': 1, 'current': 1},
                   'plantCapacity': 2 if total >= 10 else 1,
                   'activePlants': [], 'additionalCreationPending': False}
        grant = self.pay.commit(sid, self.first + ':' + str(level),
                                choice=choice, prerequisites_met=True)
        self.initializations[sid] = initial
        return grant

    def flora_dc_projection(self):
        """Numerical projection only; does not authorize an actual creation/use."""
        initial = self.initializations.get('conjure_flora')
        if not initial or not self.pay.has('conjure_flora'):
            raise ValueError('A complete paid Flora grant with recorded casting route is required')
        route = initial['fixedCastingRoute']
        current_pb = pb(sum(self.pay.current_classes.values()))
        modifier = (self.pay.scores[route['ability']] - 10) // 2
        return {'dc': 8 + current_pb + modifier, 'currentPB': current_pb,
                'currentAbilityModifier': modifier, 'fixedCastingRoute': deepcopy(route)}
