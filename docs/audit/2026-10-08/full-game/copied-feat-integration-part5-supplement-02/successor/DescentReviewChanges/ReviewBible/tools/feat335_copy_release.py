"""Paid feat-copy commitment and concentration integration (CRS-01..03).

The direct-Action adapter consumes actual CopyCaptures permissions and the same
RP/cadence/concentration objects supplied by its caller. It does not implement
recipient payloads, a world scheduler, price modifiers, or other class routes.
The separate Ready lifecycle adapter accepts an already-paid preparation; it
does not decide the unintegrated Ready/shared-release-allowance timing.
"""
from copy import deepcopy
from feat335_copy_capture import CopyCaptures
from feat335_copy_source_components import integer
from feat_exact_01_acquisition_models import pb
from transformation_spell_playtest_rules import ConcentrationLedger

PRICES = (0, 2, 3, 5, 7, 10, 13, 17, 21, 26)
CONCENTRATION = dict(strike=False, burst=False, mend=False, ward=True,
                     hindrance=True, boon=True, step=False)


def copy_quote(component, *, proficiency, modifier, pool, cadence):
    """FS-09 arithmetic only; this function grants no casting permission."""
    identity = component.get('sourceSpellId')
    if not isinstance(identity, str) or not identity.strip():
        raise ValueError('Stable witnessed underlying source identity required')
    original = integer(component['originalRank'], 'original source rank', 0, 9)
    rank = integer(component['copyRank'], 'copy rank', 0, 9)
    if rank != (0 if original == 0 else max(1, original // 2)):
        raise ValueError('Copy rank must follow the actual source rank')
    integer(proficiency, 'actual PB', 2, 6)
    integer(modifier, 'actual casting modifier', -5, 10)
    integer(pool['maxRP'], 'existing maximum RP')
    integer(pool['rp'], 'existing current RP', 0, pool['maxRP'])
    dissonance = integer(cadence['dissonance'], 'Dissonance')
    previous = integer(cadence['refrain'], 'Refrain', 0, 3)
    family = 'feat-copy::' + identity
    limit = max(4, 2 * proficiency + modifier)
    state = 3 if dissonance >= limit + 6 else 2 if dissonance >= limit + 3 else 1 if dissonance >= limit else 0
    if rank and state == 3:
        raise ValueError('Fractured blocks this ranked feat copy')
    surcharge = state if rank else 0
    cost = PRICES[rank] + surcharge
    if pool['rp'] < cost:
        raise ValueError('Insufficient existing RP')
    refrain = min(3, previous + 1) if cadence['previousSpell'] == family else 0
    base = 0 if rank == 0 else 1 if rank <= 5 else 2
    return {'castFamilyKey': family, 'rank': rank, 'limit': limit,
            'baseRpCost': PRICES[rank], 'surcharge': surcharge, 'cost': cost,
            'rpAfterPayment': pool['rp'] - cost, 'refrain': refrain,
            'baseDissonance': base, 'dissonanceAdded': base + refrain,
            'dissonanceAfter': dissonance + base + refrain,
            'classHooksApplied': []}


class CopyConcentration:
    """One real shared concentration ledger, including paid Ready holds.

    Recipient application/cleanup is a downstream integration requirement. The
    effect records here track lifecycle, not HP, movement or combat modifiers.
    """
    def __init__(self, owner, ledger, profiles):
        if not owner or not isinstance(ledger, ConcentrationLedger):
            raise ValueError('Canonical owner and shared concentration ledger required')
        if {p['id']: p['concentrationRequired'] for p in profiles} != CONCENTRATION:
            raise ValueError('Exact current seven CRS-02 profile tags required')
        self.owner = owner; self.ledger = ledger; self.casts = {}

    def snapshot(self):
        return {'casts': deepcopy(self.casts),
                'currentBurden': self.ledger.current.get(self.owner, (None,))[0]}

    def validate_new(self, event, profile):
        if not isinstance(event, str) or not event or event in self.casts or profile not in CONCENTRATION:
            raise ValueError('Distinct cast identity and supported profile required')

    def committed(self, event, profile, *, ready=False):
        self.validate_new(event, profile)
        if type(ready) is not bool:
            raise ValueError('Explicit paid Ready preparation classification required')
        record = {'id': event, 'profile': profile, 'ready': ready,
                  'state': 'committed', 'effectActive': False,
                  'concentrationRequired': CONCENTRATION[profile]}
        self.casts[event] = record
        if ready or CONCENTRATION[profile]:
            record['displacedConcentration'] = self.ledger.start_committed(
                self.owner, event, lambda reason: self._ended(event, reason))

    def _ended(self, event, reason):
        record = self.casts[event]
        record.update(state='ended', effectActive=False, endReason=reason)

    def after_counter_window(self, event, *, countered, effect_established=False):
        record = self.casts[event]
        if type(countered) is not bool or type(effect_established) is not bool or record['state'] not in {'committed', 'ended'} or 'counterWindowOutcome' in record:
            raise ValueError('One actual committed counter-window outcome required')
        if countered and effect_established or record['ready'] and effect_established:
            raise ValueError('Countered or held spell cannot already have a payload')
        if record['state'] == 'ended' and effect_established:
            raise ValueError('Lost concentration cannot establish a lasting payload')
        record['counterWindowOutcome'] = 'countered' if countered else 'not-countered'
        if record['state'] == 'ended':
            return
        if countered:
            self.ledger.detach(self.owner, event)
            record.update(state='countered', effectActive=False)
        elif record['ready']:
            record['state'] = 'held'
        else:
            self._resolved(record, effect_established)

    def _resolved(self, record, established):
        lasting = record['concentrationRequired'] and established
        record.update(state='active' if lasting else 'resolved', effectActive=lasting)
        if not lasting:
            self.ledger.detach(self.owner, record['id'])

    def release_ready(self, event, *, actual_legal_release, effect_established=False):
        record = self.casts[event]
        if actual_legal_release is not True or type(effect_established) is not bool or record['state'] != 'held':
            raise ValueError('Live paid hold and actual legal Reaction release required')
        if self.ledger.current.get(self.owner, (None,))[0] != event:
            raise ValueError('The same Ready concentration must still exist')
        self._resolved(record, effect_established)

    def end_at_deadline(self, event, *, actual_source_deadline):
        if actual_source_deadline is not True:
            raise ValueError('Caller must supply the actual profile-specific deadline event')
        record = self.casts[event]
        if record['state'] not in {'held', 'active'}:
            raise ValueError('Only a live hold/effect can expire')
        self.ledger.detach(self.owner, event)
        self._ended(event, 'source-deadline')


class CopyReleases:
    """Direct Action slice: acquired Wizard / actual feat-only Blast providers.

    The caller supplies a canonical conditional action frame and physical
    predicates. Only unmodified prices are supported; active price modifiers
    fail closed. Ready, Mirrorsage shared allowance, Shaman/other providers and
    world payload execution remain separate integration work.
    """
    def __init__(self, captures, owner, pool, cadence, concentration):
        if not isinstance(captures, CopyCaptures):
            raise ValueError('Actual paid acquisitions and source-qualified captures required')
        # CFI-02: all supported routes share one actual concentration ledger.
        # Rebuilding this adapter must not refresh its owner-round cap or receipts.
        # Migration/save-load remains separate; reuse the registered adapter.
        registered = getattr(concentration, '_feat_copy_engine_owners', set())
        if owner in registered:
            raise ValueError('One canonical feat-copy engine per owner; reuse the existing adapter')
        self.captures = captures; self.owner = owner; self.pool = pool; self.cadence = cadence
        self.lifecycle = CopyConcentration(owner, concentration,
            captures.acquired.supplements['SUP-07']['copyProfileContract']['profiles'])
        self.casts = {}; self.release_rounds = set()
        self._pool()
        concentration._feat_copy_engine_owners = registered
        registered.add(owner)

    def _pool(self):
        acquired = self.captures.acquired
        if self.pool.get('owner') != self.owner:
            raise ValueError('Use the owner existing pool, not a new copy pool')
        level = acquired.pay.current_classes.get('Wizard')
        if level:
            if self.pool.get('source') != 'Wizard/class-engine' or self.pool['maxRP'] != acquired.sources.wizard['rpByClassLevel'][level - 1]:
                raise ValueError('Actual Wizard RP capacity required')
        elif self.pool.get('source') != 'no-acquired-RP-pool' or self.pool['maxRP'] != 0 or self.pool['rp'] != 0:
            raise ValueError('Feat-only route creates no RP pool')
        integer(self.pool['rp'], 'existing RP', 0, self.pool['maxRP'])

    def snapshot(self):
        return {'captures': self.captures.snapshot(), 'pool': deepcopy(self.pool),
                'cadence': deepcopy(self.cadence), 'lifecycle': self.lifecycle.snapshot(),
                'casts': deepcopy(self.casts), 'releaseRounds': sorted(self.release_rounds)}

    def commit(self, event, capture_event, *, permission, grant_id, frame):
        c = self.captures; acquired = c.acquired
        if not isinstance(frame, dict) or set(frame) != {'turn', 'round', 'actions', 'conscious', 'canAct', 'verbal', 'somatic', 'magicAllowed', 'knownLegalSelection', 'unmodifiedPrice', 'ordinaryActionAllowed'}:
            raise ValueError('Exact canonical conditional action frame required')
        for field in set(frame) - {'turn', 'round', 'actions'}:
            if frame[field] is not True:
                raise ValueError('Actual components/action/selection and unmodified price required')
        if not c.current_turn or frame['turn'] != c.current_turn or frame['round'] != c.current_round:
            raise ValueError('Current actual turn and numbered round required')
        integer(frame['actions'], 'available Actions', 1)
        integer(frame['round'], 'numbered round', 1)
        if frame['round'] in self.release_rounds:
            raise ValueError('The owner already committed a feat-copy release this numbered round')
        if permission == 'pending':
            record = c.pending
            if not record or record['captureEvent'] != capture_event or not c.operative(record['feat']):
                raise ValueError('Current available one-use pending copy required')
            if record['feat'] == 'eldritch_echo' and (c.current_kind != 'regular' or c.regular_ordinal != record['releaseRegularOrdinal']):
                raise ValueError('Echo must release on the next future regular turn')
        elif permission == 'adapted':
            record = c.adapted.get(capture_event)
            if not record or not record['active'] or not c.operative('arcane_adaptation') or c.regular_ordinal >= record['expiresAtRegularStart']:
                raise ValueError('Actual unexpired adapted permission required')
        else:
            raise ValueError('Pending or actual adapted permission required')
        selected = record['component']
        # Reconstruct from the witnessed event, never trust edited copy fields.
        if c.witnesses.select(selected['sourceEvent'], selected['profile']) != selected:
            raise ValueError('Exact captured source component changed')
        provider = acquired.provider(grant_id, selected['copyRank'])
        if grant_id != 'Wizard/class-engine':
            grant_feat = grant_id.split('/')[0]
            if not c.operative(grant_feat):
                raise ValueError('The selected feat-only casting provider is unavailable')
        self._pool()
        proficiency = pb(sum(acquired.pay.current_classes.values()))
        modifier = (acquired.pay.scores[provider['ability']] - 10) // 2
        quote = copy_quote(selected, proficiency=proficiency, modifier=modifier,
                           pool=self.pool, cadence=self.cadence)
        self.lifecycle.validate_new(event, selected['profile'])
        # All fallible preflight precedes payment/consumption. Shared ledger end
        # callbacks obey ConcentrationLedger's total/nonthrowing contract.
        frame['actions'] -= 1
        self.pool['rp'] = quote['rpAfterPayment']
        self.cadence.update(previousSpell=quote['castFamilyKey'], refrain=quote['refrain'], dissonance=quote['dissonanceAfter'])
        self.release_rounds.add(frame['round'])
        if permission == 'pending':
            c.events[capture_event]['recordStatus'] = 'consumed-paid-release'
            c.pending = None
        self.casts[event] = {'id': event, 'captureEvent': capture_event,
            'permission': permission, 'provider': provider, 'component': deepcopy(selected),
            'quote': quote, 'round': frame['round'], 'turn': frame['turn'],
            'spellAttack': proficiency + modifier, 'spellDC': 8 + proficiency + modifier,
            'copyDerived': True, 'newRepertoire': False, 'classProcAllowed': False,
            'furtherCaptureAllowed': False, 'externalFeatAmplificationAllowed': False,
            'recipientPayloadExecuted': False}
        self.lifecycle.committed(event, selected['profile'])
        return deepcopy(self.casts[event])
