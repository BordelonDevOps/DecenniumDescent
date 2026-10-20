"""Class-qualified feat copies, using existing payload/quote/lifecycle rules.

The frozen Wizard adapter remains unchanged. This extends its commitment
boundary for actual Shaman/Mirrorsage providers and the canonical Mirror cap.
Ready, active price modifiers, and a full class Echo cast remain outside scope.
"""
from copy import deepcopy
from feat335_copy_release import CopyReleases, copy_quote
from feat335_copy_payloads import CopyPayloadReleases
from feat335_copy_class_providers import ClassCopyAcquisition
from feat335_copy_source_components import integer
from feat_exact_01_acquisition_models import pb
from creature_lifecycle_playtest_rules import EchoLedger
from transformation_spell_playtest_rules import ConcentrationLedger
from device_lifecycle_playtest_rules import Wallet


class ClassCopyCommit(CopyReleases):
    def _pool(self):
        h = self.captures.acquired
        if not isinstance(h, ClassCopyAcquisition) or self.pool.get('owner') != self.owner:
            raise ValueError('Actual native acquired class and canonical owner pool required')
        h.verify_class_source()
        if self.pool.get('source') != h.first + '/class-engine' or self.pool['maxRP'] != h.class_source['rpByClassLevel'][h.pay.current_classes[h.first] - 1]:
            raise ValueError('Existing actual class RP capacity required; copy grants no pool')
        integer(self.pool['rp'], 'existing RP', 0, self.pool['maxRP'])

    def commit(self, event, capture_event, *, permission, grant_id, frame):
        c = self.captures; h = c.acquired
        if not isinstance(frame, dict) or set(frame) != {'turn', 'round', 'actions', 'conscious', 'canAct', 'verbal', 'somatic', 'magicAllowed', 'knownLegalSelection', 'unmodifiedPrice', 'ordinaryActionAllowed'}:
            raise ValueError('Exact canonical conditional action frame required')
        if any(frame[k] is not True for k in set(frame) - {'turn', 'round', 'actions'}):
            raise ValueError('Actual components/action/selection and unmodified price required')
        if not c.current_turn or frame['turn'] != c.current_turn or frame['round'] != c.current_round:
            raise ValueError('Actual current turn/round required')
        integer(frame['actions'], 'available Actions', 1); integer(frame['round'], 'numbered round', 1)
        if frame['round'] in self.release_rounds:
            raise ValueError('Owner feat-copy release already spent this round')
        if h.first == 'Mirrorsage':
            if not isinstance(self.echoes, EchoLedger) or self.echoes.owner != self.owner:
                raise ValueError('Canonical owned Mirrorsage shared Echo ledger required')
            if frame['round'] in self.echoes.released_rounds:
                raise ValueError('Mirrorsage shared release allowance already spent')
        elif self.echoes is not None:
            raise ValueError('A Shaman does not acquire a Mirrorsage ledger')
        if self.action_account is not None:
            if self.action_account['actions'] != frame['actions'] or self.action_account['turnId'] != frame['turn']:
                raise ValueError('Action frame must match the canonical owner action account')
            body = self.action_account.get('body')
            if body is not None and (not body['conscious'] or not body['canAct'] or body['silenced']
                    or not body['canSpeak'] or not any(hand['usable'] and hand['holding'] is None for hand in body['hands'].values())):
                raise ValueError('Actual linked class body cannot supply required V/S and action')
        validate = getattr(self.lifecycle.ledger, 'validate_current', None)
        if validate: validate()
        if permission == 'pending':
            record = c.pending
            if not record or record['captureEvent'] != capture_event or not c.operative(record['feat']):
                raise ValueError('Actual available pending copy required')
            if record['feat'] == 'eldritch_echo' and (c.current_kind != 'regular' or c.regular_ordinal != record['releaseRegularOrdinal']):
                raise ValueError('Echo releases only on its next future regular turn')
        elif permission == 'adapted':
            record = c.adapted.get(capture_event)
            if not record or not record['active'] or not c.operative('arcane_adaptation') or c.regular_ordinal >= record['expiresAtRegularStart']:
                raise ValueError('Actual unexpired paid adapted permission required')
        else:
            raise ValueError('Pending or actual adapted permission required')
        selected = record['component']
        if selected['profile'] == 'step' and isinstance(self.lifecycle.ledger, ShamanConcentrationBridge):
            # CFI-04: the copy world has a 3-D pose; the linked native Shaman
            # uses a separate scalar pose for aura/cast queries. No approved
            # atomic pose mapping is supplied. Reject before payment instead
            # of moving one view and granting ordinary vent at the old pose.
            raise ValueError('Linked Shaman Step requires a canonical cross-world position adapter')
        if c.witnesses.select(selected['sourceEvent'], selected['profile']) != selected:
            raise ValueError('Captured source component changed')
        provider = h.provider(grant_id, selected['copyRank'])
        if grant_id != h.first + '/class-engine' and not c.operative(grant_id.split('/')[0]):
            raise ValueError('Selected actual feat-only provider unavailable')
        self._pool()
        proficiency = pb(sum(h.pay.current_classes.values()))
        modifier = (h.pay.scores[provider['ability']] - 10) // 2
        quote = copy_quote(selected, proficiency=proficiency, modifier=modifier, pool=self.pool, cadence=self.cadence)
        self.lifecycle.validate_new(event, selected['profile'])
        # All source, ownership, cap, action, resource and concentration checks
        # precede mutation. Existing callbacks are total/nonthrowing.
        frame['actions'] -= 1
        if self.action_account is not None: self.action_account['actions'] -= 1
        self.pool['rp'] = quote['rpAfterPayment']
        self.cadence.update(previousSpell=quote['castFamilyKey'], refrain=quote['refrain'], dissonance=quote['dissonanceAfter'])
        self.release_rounds.add(frame['round'])
        if self.echoes is not None: self.echoes.released_rounds.add(frame['round'])
        if permission == 'pending':
            c.events[capture_event]['recordStatus'] = 'consumed-paid-release'; c.pending = None
        self.casts[event] = {'id': event, 'captureEvent': capture_event, 'permission': permission,
            'provider': provider, 'component': deepcopy(selected), 'quote': quote,
            'round': frame['round'], 'turn': frame['turn'], 'spellAttack': proficiency + modifier,
            'spellDC': 8 + proficiency + modifier, 'copyDerived': True, 'newRepertoire': False,
            'classProcAllowed': False, 'furtherCaptureAllowed': False,
            'externalFeatAmplificationAllowed': False, 'recipientPayloadExecuted': False}
        self.lifecycle.committed(event, selected['profile'])
        return deepcopy(self.casts[event])


class ClassCopyPayloadReleases(CopyPayloadReleases, ClassCopyCommit):
    """MRO keeps the existing selection/payload implementation intact."""
    def __init__(self, captures, owner, pool, cadence, concentration, world, *, echoes=None, action_account=None):
        # Validate the link before registering this owner or changing captures.
        if not isinstance(action_account, dict):
            raise ValueError('Actual canonical class Action/Reaction account required')
        fields = [k for k in ('reaction', 'reactions') if k in action_account]
        if len(fields) != 1:
            raise ValueError('One explicit canonical Reaction field required; no duplicate budgets')
        field = fields[0]; value = action_account[field]
        if field == 'reaction':
            if type(value) is not bool:
                raise ValueError('Actual Boolean Reaction account required')
        else:
            integer(value, 'actual counted Reaction account')
        if (captures._reaction_account is not None or captures.events
                or captures.regular_turns or captures.extra_turns or captures.current_turn is not None):
            raise ValueError('Create the class link before capture/turn history; no late budget merging')
        self.echoes = echoes; self.action_account = action_account
        super().__init__(captures, owner, pool, cadence, concentration, world)
        captures.bind_reaction_account(action_account, field, self._capture_reaction_legal)

    def _capture_reaction_legal(self):
        actor = self.world.actors[self.owner]
        if not actor['conscious'] or not actor['canAct'] or not self.world.reaction_allowed(self.owner):
            return False
        body = self.action_account.get('body')
        return body is None or (body['conscious'] and body['canAct'] and body['reactionLegal'])

    def _owner_can_resolve(self):
        # Components already performed at commitment are not performed again.
        # Consult the linked body for surviving-caster eligibility, not the old
        # copy-world snapshot alone. General body-end processing is still open.
        body = self.action_account.get('body')
        return super()._owner_can_resolve() and (body is None or
            body['conscious'] is True and body['canAct'] is True)

    def snapshot(self):
        return {**super().snapshot(), 'classAcquisition': self.captures.acquired.snapshot(),
                'sharedEchoes': deepcopy(self.echoes.__dict__) if self.echoes is not None else None,
                'canonicalActionAccount': deepcopy(self.action_account)}


class ShamanConcentrationBridge(ConcentrationLedger):
    """Adopt the existing paid totem burden, then share copy lifecycle endings.

This narrow bridge recognizes totems and registered copy casts only. A changed
ordinary concentration must be integrated by its actual adapter; mismatch is
rejected before any copy payment. It does not manufacture a parallel burden.
"""
    def __init__(self, shaman, owner):
        super().__init__(); self.shaman = shaman; self.owner = owner
        self.actor = shaman.actors[owner]
        burden = self.actor['concentration']
        if burden is not None:
            if burden != shaman.burden(owner) or not any(t['owner'] == owner and shaman._live(t) for t in shaman.totems.values()):
                raise ValueError('Only an existing live paid totem concentration can be adopted')
            self.current[owner] = (burden, self._end_totems)

    def _end_totems(self, reason):
        for tid, t in self.shaman.totems.items():
            if t['owner'] == self.owner: self.shaman._end_totem(tid, reason)

    def validate_current(self):
        if self.actor['concentration'] != self.current.get(self.owner, (None,))[0]:
            raise ValueError('Canonical Shaman concentration changed outside this finite bridge')

    def end(self, owner, reason):
        old = super().end(owner, reason)
        if owner == self.owner: self.actor['concentration'] = None
        return old

    def start_committed(self, owner, cast_id, on_end):
        old = super().start_committed(owner, cast_id, on_end)
        if owner == self.owner: self.actor['concentration'] = cast_id
        return old

    def detach(self, owner, cast_id):
        super().detach(owner, cast_id)
        if owner == self.owner and self.actor['concentration'] == cast_id:
            self.actor['concentration'] = None


class SharedClassWallet(Wallet):
    """The creature interface spends the SAME dict RP/actions as feat copies."""
    def __init__(self, state):
        self.state = state; self.used = set()

    @property
    def rp(self): return self.state['rp']
    @rp.setter
    def rp(self, value): self.state['rp'] = value
    @property
    def actions(self): return self.state['actions']
    @actions.setter
    def actions(self, value): self.state['actions'] = value
    @property
    def bonus_action(self): return self.state['bonus_action']
    @bonus_action.setter
    def bonus_action(self, value): self.state['bonus_action'] = value
    @property
    def reaction(self): return self.state['reaction']
    @reaction.setter
    def reaction(self, value): self.state['reaction'] = value
