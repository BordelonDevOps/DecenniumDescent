"""Paid alignment resolution with current target and concentration boundaries.

This finite extension preserves earlier component/cast reports. Conditional
world grants, movement and body changes remain external, explicit premises.
"""
from copy import deepcopy
from di7_alignment_clock import ClockedFateTransactions


class AlignmentTransactions(ClockedFateTransactions):
    def _sync_actual_alignment(self):
        for actor_id, actor in self.actors.items():
            pending = self.alignment.concentration.get(actor_id)
            if pending:
                if not actor['body']['conscious'] or not actor['body']['canAct']:
                    self.alignment.end(pending, 'actual-caster-incapacity')
                elif actor['concentration'] != pending:
                    self.alignment.end(pending, 'actual-upstream-concentration-ended')
            own = actor['concentration']
            if own in self.alignment.casts and self.alignment.concentration.get(actor_id) != own:
                actor['concentration'] = None

    def advance(self, now):
        super().advance(now)
        self._sync_actual_alignment()

    def resolve_alignment(self, cast_id, *, face, modifier):
        cast = self.casts.get(cast_id)
        if not cast or cast['spellId'] not in {'alignment-purge', 'alignment-suggestion'} or cast['status'] != 'pending' or not self.stack or self.stack[-1] != cast_id:
            raise ValueError('Actual surviving top paid alignment cast required')
        if type(face) is not int or not 1 <= face <= 20 or type(modifier) is not int:
            raise ValueError('Actual complete binary save operands required')
        self.advance(self.now)
        actor = self.actors[cast['actor']]
        reason = None
        if actor['concentration'] != cast_id or not actor['body']['conscious'] or not actor['body']['canAct'] or actor['body']['ordinarySpellProhibited']:
            reason = 'actual-cast-interrupted'
        else:
            source_provider = self.casts[cast['copyLineage']['original']]['provider'] if cast.get('route') == 'fate-echo-copy' else cast['provider']
            _, op, source_binding, _ = self.sources.spell(cast['spellId'], source_provider)
            if source_binding != cast['sourceBinding']:
                raise ValueError('Exact generating source binding must survive to resolution')
            try:
                self._target(cast['actor'], cast['spellId'], cast['request'], op)
            except ValueError:
                reason = 'actual-target-no-longer-legal'
        if reason:
            self.stack.pop()
            outcome = {'resolutionComplete': True, 'informationGranted': False, 'refund': 0}
            cast.update(status='failed-payload-no-refund', resolvedAt=self.now, failure=reason, result=outcome)
            self.alignment.casts[cast_id].update(state='interrupted', resolvedAt=self.now)
            self.alignment.end(cast_id, reason)
            self._sync_actual_alignment()
            return deepcopy(outcome)
        result = super().resolve_alignment(cast_id, face=face, modifier=modifier)
        # A successful cross-caster family replacement also releases the former
        # caster's real concentration slot at this same resolution boundary.
        self._sync_actual_alignment()
        return result

    def end_alignment(self, cast_id, reason, source_event):
        if reason not in {'dispel', 'voluntary-end', 'failed-concentration-save', 'death', 'incapacitated'} or not source_event or any(e.get('sourceEvent') == source_event for e in self.events):
            raise ValueError('Unique explicit conditional legal ending required')
        if cast_id not in self.alignment.effects or self.alignment.effects[cast_id]['state'] != 'live':
            raise ValueError('One actual live alignment application required')
        self.events.append({'kind': 'conditional-upstream-concentration-or-dispel-ending', 'sourceEvent': source_event, 'reason': reason, 'castId': cast_id, 'at': self.now})
        self.alignment.end(cast_id, reason)
        self._sync_actual_alignment()
