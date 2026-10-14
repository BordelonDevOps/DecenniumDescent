"""Finite Fate Echo composite/Ready evaluator over actual conditional cast history.

Complete reviewed Fate Coin and Alignment Suggestion are the admitted child
sources here. Their object and alignment results are resolved; the alignment
component retains its explicitly limited elapsed-clock scope. No other spell
mode is approximated. This adds no approval to the unapproved DI7 candidates.
"""
from copy import deepcopy
from di7_cast_transactions import DI7CastTransactions
from di7_alignment_component import AlignmentComponent
from spell_playtest_rules import quote_cast, integer


class FateTransactions(DI7CastTransactions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observations = {}; self.reservations = {}; self.composites = {}; self.holds = {}; self.coins = {}
        self.fate_admission_context = None; self.ready_original_context = None
        self.active_actor = None
        bindings = {sid: self.sources.spell(sid, 'Wizard')[2] for sid in ['alignment-suggestion', 'alignment-purge']}
        self.alignment = AlignmentComponent(self.world['alignmentActors'], bindings)
        self.alignment.advance(self.now)

    def snapshot(self):
        return {**super().snapshot(), 'observations': deepcopy(self.observations), 'reservations': deepcopy(self.reservations),
            'composites': deepcopy(self.composites), 'holds': deepcopy(self.holds), 'coins': deepcopy(self.coins), 'activeActor': self.active_actor,
            'alignmentComponent': self.alignment.snapshot()}

    def reserved(self, actor_id, excluding=None):
        return sum(x['rp'] for key, x in self.reservations.items() if key != excluding and x['actor'] == actor_id)

    def _quote(self, actor_id, sid, *, state=None, copied_from=None, rp=None):
        actor = self.actors[actor_id]; state = actor if state is None else state
        modifier = (actor['abilityScore'] - 10) // 2; proficiency = 2 + (actor['totalLevel'] - 1) // 4
        if copied_from:
            original = self.casts[copied_from]
            card, op, binding, _ = self.sources.spell(sid, original['provider'])
            placement = {'rank': original['rank'], 'school': original['school'], 'minimumClassLevel': 1,
                'baseRpCost': self.sources.catalog['costByRank'][str(original['rank'])]}
            card['classAccess'] = {actor['provider']: placement}
            card['status'] = 'operational-playtest-draft'
        else:
            card, op, binding, _ = self.route(actor_id, sid)
        quote = quote_cast(card, actor['provider'], actor['classLevel'], available_spell_ids={sid},
            rp=actor['rp'] if rp is None else rp, max_rp=actor['maxRP'], dissonance=state['dissonance'],
            proficiency=proficiency, casting_modifier=modifier, previous_spell_id=state['previousSpell'], previous_refrain=state['refrain'])
        strain = quote['dissonanceAddedBeforeClassInterface']
        if not copied_from and actor['provider'] == 'Wizard' and self.world['encounter']['isRealEncounter'] and sid not in actor['wizardFamilies']:
            strain -= 0 if quote['rank'] == 0 else 1 if quote['rank'] <= 5 else 2
        return quote, strain, op, binding

    def _target(self, actor_id, sid, request, op):
        if sid == 'fate-echo':
            if self.fate_admission_context != (actor_id, request.get('originalCast')):
                raise ValueError('Complete preflight and forecast must authorize this outer commit')
            return
        if self.ready_original_context == (actor_id, sid):
            if sid != 'fate-coin':
                raise ValueError('Only the complete Fate Coin original Ready adapter is supplied')
            return
        return super()._target(actor_id, sid, request, op)

    def declare(self, actor_id, sid, cast_id, request):
        if sid != 'counterspell' and self.active_actor != actor_id:
            raise ValueError('An Action cast requires the actual current actor turn')
        quote, _, _, _ = self._quote(actor_id, sid)
        if quote['cost'] > self.actors[actor_id]['rp'] - self.reserved(actor_id):
            raise ValueError('Committed reservation cannot be spent by another declaration')
        result = super().declare(actor_id, sid, cast_id, request)
        self._register_alignment_commit(cast_id)
        self._sync_alignment_concentration()
        self._expire_lost_holds()
        return result

    def _register_alignment_commit(self, cast_id):
        cast = self.casts[cast_id]
        if cast['spellId'] in {'alignment-suggestion', 'alignment-purge'}:
            self.alignment.begin_conditional_committed_cast({'castId': cast_id, 'spellId': cast['spellId'],
                'sourceBinding': self.alignment.sources[cast['spellId']], 'caster': cast['actor'], 'target': cast['request']['target'],
                'committedAt': self.now, 'clockMode': 'outside-initiative-elapsed',
                'paymentPremise': {'kind': 'conditional-upstream-commit-not-executed-here', 'fixtureId': 'executed-in-parent-evaluator/' + cast_id,
                    'upstreamExecutedQuote': deepcopy(cast['quote']), 'upstreamExecutedBudgetAndHistory': deepcopy(cast['afterCommit'])}})

    def _sync_alignment_concentration(self):
        for caster, cast_id in list(self.alignment.concentration.items()):
            if caster in self.actors and self.actors[caster]['concentration'] != cast_id:
                self.alignment.end(cast_id, 'actual-upstream-concentration-ended')

    def resolve_alignment(self, cast_id, *, face, modifier):
        cast = self.casts[cast_id]
        if cast['spellId'] not in {'alignment-suggestion', 'alignment-purge'} or cast['status'] != 'pending' or not self.stack or self.stack[-1] != cast_id:
            raise ValueError('Actual pending paid alignment spell required')
        outcome = self.alignment.resolve(cast_id, face=face, modifier=modifier, dc=cast['dc'])
        self.stack.pop(); cast.update(status='resolved', resolvedAt=self.now, castingCompletedAt=self.now, result=outcome)
        if self.alignment.concentration.get(cast['actor']) != cast_id and self.actors[cast['actor']]['concentration'] == cast_id:
            self.actors[cast['actor']]['concentration'] = None
        return deepcopy(outcome)

    def observe_cast(self, observer, cast_id, identity_evidence):
        cast = self.casts.get(cast_id)
        if not cast or cast['status'] != 'pending' or cast['committedAt'] != self.now:
            raise ValueError('Direct observation at the original actual casting event required')
        if (observer + '/' + cast_id) in self.observations:
            raise ValueError('Observation already recorded')
        self._line(observer, cast['actor'], 120)
        permitted = self.world.get('identificationFacts', {}).get(identity_evidence)
        if not permitted or permitted != {'observer': observer, 'castId': cast_id, 'kind': 'conditional-actual-direct-identification'}:
            raise ValueError('Actual source-qualified direct identification premise required')
        self.observations[observer + '/' + cast_id] = {'observer': observer, 'castId': cast_id, 'sourceBinding': deepcopy(cast['sourceBinding']),
            'observedAt': self.now, 'identityEvidence': identity_evidence, 'kind': 'direct-cast-observation', 'within120AndLineOfEffectAtEvent': True}

    def _admit_original(self, actor_id, original_id, *, freshness):
        original = self.casts.get(original_id); observation = self.observations.get(actor_id + '/' + original_id)
        if not original or original['status'] != 'resolved' or original.get('copyLineage') or original['spellId'] == 'fate-echo':
            raise ValueError('One successfully resolved original noncopy spell required')
        if not observation or observation['kind'] != 'direct-cast-observation' or observation['sourceBinding'] != original['sourceBinding']:
            raise ValueError('Matching actual direct observation, not a report or history query')
        rank = original['rank']
        if type(rank) is not int or not 0 <= rank <= 7:
            raise ValueError('Actual rank0..7 required; null is not zero')
        card, op, binding, _ = self.sources.spell(original['spellId'], original['provider'])
        if binding != original['sourceBinding'] or card['classAccess'][original['provider']]['rank'] != rank or card['classAccess'][original['provider']]['school'] != original['school']:
            raise ValueError('The exact generating source/mode/rank/school changed')
        if op['activation'] not in {'Action', 'Bonus Action'}:
            raise ValueError('Reaction and longer original modes are not eligible')
        if original['spellId'] not in {'fate-coin', 'alignment-suggestion'}:
            raise ValueError('No complete nondamage/independent-entitlement adapter supplied for this mode')
        age = self.now - original['castingCompletedAt']
        if freshness and not 0 <= age <= 18:
            raise ValueError('Original casting completion must be0..18 seconds old, not its Ready release')
        return original, op

    def _child_check(self, actor_id, original_id, request, *, state=None, rp=None, targets=True):
        original, op = self._admit_original(actor_id, original_id, freshness=False)
        actor = self.actors[actor_id]
        if not actor['providerRetained'] or actor['provider'] == 'Shaman' and actor['heroPath'] == 'Bloodcaller':
            raise ValueError('Actual Fate provider no longer retained')
        self._components(actor_id, op)
        if targets:
            super()._target(actor_id, original['spellId'], request, op)
        return self._quote(actor_id, original['spellId'], state=state, copied_from=original_id, rp=rp)

    def begin_fate(self, actor_id, cast_id, original_id, request=None, *, ready_trigger=None):
        if cast_id in self.casts or self.stack or actor_id in self.holds:
            raise ValueError('Unique outer cast and no pending cast/hold required in this finite adapter')
        self._admit_original(actor_id, original_id, freshness=True)
        outer_quote, outer_strain, outer_op, _ = self._quote(actor_id, 'fate-echo')
        self._components(actor_id, outer_op)
        actor = self.actors[actor_id]
        if actor['actions'] < 1 or actor['turnId'] is None:
            raise ValueError('Own actual Action required')
        if ready_trigger is not None and (not isinstance(ready_trigger, str) or not ready_trigger):
            raise ValueError('A specific perceivable Ready trigger is required')
        forecast = {'dissonance': actor['dissonance'] + outer_strain, 'previousSpell': 'fate-echo', 'refrain': outer_quote['refrain']}
        available_after = actor['rp'] - outer_quote['cost'] - self.reserved(actor_id)
        child_quote, child_strain, _, _ = self._child_check(actor_id, original_id, request or {}, state=forecast, rp=available_after, targets=ready_trigger is None)
        self.fate_admission_context = (actor_id, original_id)
        try:
            paid = self.declare(actor_id, 'fate-echo', cast_id, {'originalCast': original_id, 'childRequest': deepcopy(request), 'readyTrigger': ready_trigger})
        finally:
            self.fate_admission_context = None
        assert paid['quote'] == outer_quote and paid['dissonanceAdded'] == outer_strain
        self.reservations[cast_id] = {'actor': actor_id, 'rp': child_quote['cost'], 'kind': 'unspent-exclusive-child-reservation', 'reservedAt': self.now,
            'materials': [], 'independentUses': [], 'sourceQualification': 'These two exact ordinary child sources require no separate consumed stock/charge; no general waiver.'}
        self.composites[cast_id] = {'actor': actor_id, 'originalCast': original_id, 'request': deepcopy(request), 'forecast': forecast,
            'forecastChildQuote': child_quote, 'forecastChildStrain': child_strain, 'selectedAt': self.now,
            'originalAgeAtSelection': self.now - self.casts[original_id]['castingCompletedAt'], 'readyTrigger': ready_trigger, 'state': 'outer-pending'}
        if ready_trigger is not None:
            prior = actor['concentration']
            if prior:
                actor['endConcentrationHistory'].append({'id': prior, 'reason': 'Ready-held-spell-commit', 'replacedBy': cast_id, 'at': self.now})
            actor['concentration'] = cast_id
            self.casts[cast_id]['readyHoldConcentrationAtCommit'] = True
            self._sync_alignment_concentration()
        return deepcopy(self.composites[cast_id])

    def _release_reservation(self, cast_id, reason):
        released = self.reservations.pop(cast_id, None)
        if released:
            self.events.append({'event': 'reservation-release/' + cast_id + '/' + reason, 'kind': 'unspent-reservation-released-not-refunded',
                'castId': cast_id, 'rp': released['rp'], 'reason': reason, 'at': self.now})

    def resolve_counter(self, cast_id, natural):
        outcome = super().resolve_counter(cast_id, natural)
        self._sync_alignment_concentration()
        for outer, composite in self.composites.items():
            if self.casts[outer]['status'] == 'countered' and composite['state'] == 'outer-pending':
                composite['state'] = 'outer-countered-no-child'; self._release_reservation(outer, 'outer-countered')
        self._expire_lost_holds()
        return outcome

    def finish_fate_outer(self, cast_id):
        c = self.composites[cast_id]
        if c['state'] != 'outer-pending' or not self.stack or self.stack[-1] != cast_id or self.casts[cast_id]['status'] != 'pending':
            raise ValueError('The surviving pending outer must resolve once')
        actor = self.actors[c['actor']]
        if not actor['body']['conscious'] or not actor['body']['canAct'] or actor['body']['ordinarySpellProhibited']:
            self.stack.pop(); self.casts[cast_id]['status'] = 'interrupted-no-refund'; c['state'] = 'interrupted-no-child'
            self._release_reservation(cast_id, 'outer-interrupted')
            if actor['concentration'] == cast_id: actor['concentration'] = None
            return None
        if c['readyTrigger'] is not None:
            if actor['concentration'] != cast_id:
                self.stack.pop(); self.casts[cast_id]['status'] = 'interrupted-no-refund'; c['state'] = 'lost-hold-no-child'
                self._release_reservation(cast_id, 'lost-hold'); return None
            self.stack.pop(); self.casts[cast_id].update(status='held', castingCompletedAt=self.now)
            c['state'] = 'held'
            self.holds[c['actor']] = {'castId': cast_id, 'kind': 'fate', 'trigger': c['readyTrigger'], 'preparedOnTurn': actor['turnId']}
            return {'held': cast_id, 'childNotCommitted': True}
        self.stack.pop()
        return self._commit_child(cast_id, c['request'])

    def _commit_child(self, outer_id, request):
        c = self.composites[outer_id]; actor_id = c['actor']; actor = self.actors[actor_id]
        original = self.casts[c['originalCast']]
        try:
            quote, strain, op, binding = self._child_check(actor_id, c['originalCast'], request,
                rp=actor['rp'] - self.reserved(actor_id, excluding=outer_id))
        except ValueError as error:
            c.update(state='outer-resolved-child-precommit-failed', childFailure=str(error))
            self.casts[outer_id].update(status='resolved-no-child', resolvedAt=self.now)
            self._release_reservation(outer_id, 'child-now-ineligible')
            return None
        child_id = outer_id + '/child'
        if child_id in self.casts:
            raise ValueError('No second child opportunity')
        before = {k: deepcopy(actor[k]) for k in ['rp', 'dissonance', 'previousSpell', 'refrain', 'concentration', 'actions', 'reactions']}
        actor.update(rp=quote['rpAfterPayment'], dissonance=actor['dissonance'] + strain, previousSpell=original['spellId'], refrain=quote['refrain'])
        if op['concentration']:
            if actor['concentration']:
                actor['endConcentrationHistory'].append({'id': actor['concentration'], 'reason': 'Fate-child-commit', 'replacedBy': child_id, 'at': self.now})
            actor['concentration'] = child_id
        modifier = (actor['abilityScore'] - 10) // 2; proficiency = 2 + (actor['totalLevel'] - 1) // 4
        self.reservations.pop(outer_id)
        self.casts[child_id] = {'id': child_id, 'actor': actor_id, 'spellId': original['spellId'], 'provider': actor['provider'],
            'sourceBinding': binding, 'candidateSimulationOnly': True, 'rank': original['rank'], 'school': original['school'],
            'abilityModifier': modifier, 'proficiency': proficiency, 'dc': 8 + modifier + proficiency,
            'scalingClassLevel': actor['classLevel'], 'components': deepcopy(op['components']), 'request': deepcopy(request),
            'committedAt': self.now, 'quote': quote, 'dissonanceAdded': strain, 'classHooks': [],
            'before': before, 'afterCommit': {k: deepcopy(actor[k]) for k in before}, 'status': 'pending', 'refund': 0,
            'route': 'fate-echo-copy', 'copyLineage': {'outer': outer_id, 'original': c['originalCast']},
            'noSecondActionOrBonusAction': True, 'suppressedDuplicateClassFeatProcs': True}
        self.casts[outer_id].update(status='resolved', resolvedAt=self.now, castingCompletedAt=self.casts[outer_id].get('castingCompletedAt', self.now), childCast=child_id)
        c.update(state='child-committed', childCast=child_id, actualChildQuote=quote)
        self.stack.append(child_id)
        self._register_alignment_commit(child_id)
        self._sync_alignment_concentration()
        return deepcopy(self.casts[child_id])

    def resolve_fate_coin(self, cast_id):
        cast = self.casts[cast_id]
        if cast['spellId'] != 'fate-coin' or cast['status'] != 'pending' or not self.stack or self.stack[-1] != cast_id:
            raise ValueError('Actual pending Fate Coin cast required')
        _, op, _, _ = self.sources.spell('fate-coin', cast['provider'])
        # Target changes during real interruptions can prevent the actual result.
        try:
            body = self.actors[cast['actor']]['body']
            if not body['conscious'] or not body['canAct'] or body['ordinarySpellProhibited']:
                raise ValueError('Actual postcommit incapacity or casting prohibition')
            super()._target(cast['actor'], 'fate-coin', cast['request'], op)
        except ValueError as error:
            self.stack.pop(); cast.update(status='resolved-no-effect', failure=str(error), refund=0); return None
        self.stack.pop()
        return self._apply_coin(cast_id)

    def _apply_coin(self, cast_id):
        cast = self.casts[cast_id]; target = self.world['entities'][cast['request']['target']]; hand = target['hands'][cast['request']['hand']]
        for coin in self.coins.values():
            if coin['caster'] == cast['actor'] and coin['state'] == 'active':
                self._end_coin(coin, 'replaced')
        coin = {'id': 'coin/' + cast_id, 'caster': cast['actor'], 'holder': cast['request']['target'], 'hand': cast['request']['hand'],
            'castId': cast_id, 'sourceBinding': deepcopy(cast['sourceBinding']), 'copyLineage': deepcopy(cast.get('copyLineage')),
            'createdAt': self.now, 'deadline': self.now + 3600, 'hp': 1, 'ac': 10, 'massPounds': 0.01, 'currency': False, 'state': 'active'}
        hand['holding'] = coin['id']; self.coins[coin['id']] = coin
        if coin['holder'] in self.actors:
            self.actors[coin['holder']]['body']['hands'][coin['hand']]['holding'] = coin['id']
        cast.update(status='resolved', resolvedAt=self.now, castingCompletedAt=cast.get('castingCompletedAt', self.now), result={'coinId': coin['id']})
        return deepcopy(coin)

    def _end_coin(self, coin, reason):
        holder = self.world['entities'][coin['holder']]['hands'][coin['hand']]
        if holder['holding'] == coin['id']: holder['holding'] = None
        if coin['holder'] in self.actors:
            body_hand = self.actors[coin['holder']]['body']['hands'][coin['hand']]
            if body_hand['holding'] == coin['id']: body_hand['holding'] = None
        coin.update(state=reason, endedAt=self.now)

    def advance(self, now):
        super().advance(now)
        self.alignment.advance(now)
        for actor_id, actor in self.actors.items():
            if actor['concentration'] in self.alignment.casts and self.alignment.concentration.get(actor_id) != actor['concentration']:
                actor['concentration'] = None
        for coin in self.coins.values():
            if coin['state'] == 'active' and now >= coin['deadline']: self._end_coin(coin, 'expired')
        self._expire_lost_holds()

    def _expire_lost_holds(self):
        for actor_id, hold in list(self.holds.items()):
            actor = self.actors[actor_id]
            if actor['concentration'] != hold['castId'] or not actor['body']['conscious'] or not actor['body']['canAct']:
                self._end_hold(actor_id, 'lost-concentration-or-incapacity')

    def _end_hold(self, actor_id, reason):
        hold = self.holds.pop(actor_id); cast_id = hold['castId']
        self.casts[cast_id].update(status='held-spell-ended', holdEndReason=reason)
        if self.actors[actor_id]['concentration'] == cast_id: self.actors[actor_id]['concentration'] = None
        if hold['kind'] == 'fate':
            self.composites[cast_id]['state'] = 'held-ended-no-child'; self._release_reservation(cast_id, reason)

    def begin_turn(self, actor_id, turn_id):
        # Prevalidate the base operation before expiring a held spell.
        if self.stack or turn_id in self.actors[actor_id]['turnHistory']:
            raise ValueError('New actual regular turn with no unresolved cast required')
        if actor_id in self.holds: self._end_hold(actor_id, 'next-regular-own-start')
        super().begin_turn(actor_id, turn_id)
        self.active_actor = actor_id

    def release_fate_ready(self, actor_id, occurrence_id, request, *, declined=False):
        hold = self.holds.get(actor_id); actor = self.actors[actor_id]
        if not hold or hold['kind'] != 'fate' or self.stack or actor['concentration'] != hold['castId']:
            raise ValueError('One existing actual held Fate Echo required')
        occurrence = self.world.get('triggerEvents', {}).get(occurrence_id)
        if not occurrence or occurrence['trigger'] != hold['trigger'] or occurrence['at'] != self.now or not occurrence['perceivedBy'].get(actor_id):
            raise ValueError('Actual just-completed perceived trigger required')
        if declined: return {'released': False, 'reason': 'declined', 'reactionSpent': 0}
        c = self.composites[hold['castId']]
        try:
            if actor['reactions'] < 1 or not actor['body']['reactionLegal']:
                raise ValueError('Actual release Reaction unavailable')
            self._child_check(actor_id, c['originalCast'], request, rp=actor['rp'] - self.reserved(actor_id, excluding=hold['castId']))
        except ValueError as error:
            return {'released': False, 'reason': str(error), 'reactionSpent': 0}
        actor['reactions'] -= 1; actor['concentration'] = None; self.holds.pop(actor_id)
        c['releasedByTrigger'] = occurrence_id; c['releasedAt'] = self.now
        child = self._commit_child(hold['castId'], request)
        return {'released': True, 'reactionSpent': 1, 'child': child}

    def begin_readied_coin_original(self, actor_id, cast_id, trigger):
        if actor_id in self.holds or not trigger:
            raise ValueError('One current Ready and a stated trigger required')
        self.ready_original_context = (actor_id, 'fate-coin')
        try: paid = self.declare(actor_id, 'fate-coin', cast_id, {'readyTrigger': trigger})
        finally: self.ready_original_context = None
        actor = self.actors[actor_id]
        if actor['concentration']:
            actor['endConcentrationHistory'].append({'id': actor['concentration'], 'reason': 'Ready-held-original', 'replacedBy': cast_id, 'at': self.now})
        actor['concentration'] = cast_id; self.casts[cast_id]['readyOriginal'] = True
        self._sync_alignment_concentration()
        return paid

    def hold_readied_coin_original(self, cast_id):
        cast = self.casts[cast_id]
        if not cast.get('readyOriginal') or cast['status'] != 'pending' or not self.stack or self.stack[-1] != cast_id or self.actors[cast['actor']]['concentration'] != cast_id:
            raise ValueError('Surviving prepared original required')
        self.stack.pop(); cast.update(status='held-original', castingCompletedAt=self.now)
        self.holds[cast['actor']] = {'castId': cast_id, 'kind': 'ordinary-coin', 'trigger': cast['request']['readyTrigger'], 'preparedOnTurn': self.actors[cast['actor']]['turnId']}

    def release_readied_coin_original(self, actor_id, occurrence_id, request):
        actor = self.actors[actor_id]; hold = self.holds.get(actor_id)
        if not hold or hold['kind'] != 'ordinary-coin' or self.stack or actor['concentration'] != hold['castId']:
            raise ValueError('Actual original Ready hold required')
        occurrence = self.world.get('triggerEvents', {}).get(occurrence_id)
        if not occurrence or occurrence['trigger'] != hold['trigger'] or occurrence['at'] != self.now or not occurrence['perceivedBy'].get(actor_id):
            raise ValueError('Actual trigger required')
        _, op, _, _ = self.sources.spell('fate-coin', actor['provider'])
        try:
            if actor['reactions'] < 1 or not actor['body']['reactionLegal']: raise ValueError('Reaction unavailable')
            super()._target(actor_id, 'fate-coin', request, op)
        except ValueError:
            return None
        actor['reactions'] -= 1; actor['concentration'] = None; self.holds.pop(actor_id)
        cast = self.casts[hold['castId']]; cast['request'] = deepcopy(request)
        return self._apply_coin(hold['castId'])
