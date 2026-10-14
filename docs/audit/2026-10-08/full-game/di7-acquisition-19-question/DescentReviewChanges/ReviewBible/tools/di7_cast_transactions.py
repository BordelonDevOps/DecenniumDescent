"""Source-bound conditional casting transactions for the unapproved DI7 cards.

This is a test-only authored-rule evaluator. The seven candidate source records
remain unapproved/null in the actual catalog. Actors, attained levels, bodies,
world relations and completed rests are explicit hypothetical campaign premises.
Learning, preparation, budgets, RP, strain, concentration and nested ordinary
Counterspell commitments are executed here. Spell payloads remain separate.
"""
from copy import deepcopy
import math
from apply_di7_ap_as_01 import G, R, info
from spell_playtest_rules import quote_cast, integer
from core_playtest_rules import task_check
import json


def read(p):
    return json.loads(p.read_bytes())


class DI7Sources:
    def __init__(self):
        self.candidate_path = R / 'data/public/spell_candidates/divination_rank7_exact_01.json'
        self.catalog_path = R / 'data/public/spell_playtests/catalog.json'
        self.foundation_path = R / 'data/playtest/character_foundation.json'
        self.candidate = read(self.candidate_path)
        self.catalog = read(self.catalog_path)
        self.chassis = {x['class']: x for x in read(self.foundation_path)['classes']}
        self.classes = {n: read(G / self.chassis[n]['classCandidatePath']) for n in ['Cleric', 'Wizard', 'Mirrorsage', 'Shaman']}
        self.cards = {x['id']: x for x in self.candidate['cards']}
        self.ordinary = {x['id']: x for x in self.catalog['spells']}
        if self.candidate['selectionEnabled'] or self.candidate['exactReviewReceived']:
            raise ValueError('This evaluator is bound to the unapproved candidate stage')
        self.bindings = [info(p) for p in [self.candidate_path, self.catalog_path, self.foundation_path,
            *[G / self.chassis[n]['classCandidatePath'] for n in self.classes],
            R / 'docs/mechanics/CLASS_PLAYTEST_RULES.md', R / 'docs/mechanics/SPELL_INTEGRATION_RULES.md']]

    def spell(self, sid, provider):
        source = self.ordinary.get(sid)
        if not source or provider not in source['classAccess']:
            raise ValueError('No actual ordinary source-class placement')
        if sid in self.cards:
            card = self.cards[sid]
            if card['preservedSourceAndProposalFields']['fullSourceAndCurrentAccessRecord'] != source or source['operational'] is not None:
                raise ValueError('Candidate no longer matches its preserved source')
            op = card['operationalCandidate']
            view = deepcopy(source)
            # Local helper input only: the existing common quote function demands
            # this label. No source/card/index object is changed or promoted.
            view['status'] = 'operational-playtest-draft'
            projection = {'activation': op['activation'], 'rangeFeet': op['rangeFeet'], 'components': op['components'],
                'concentration': op['concentrationRequiredByOuterEffect'], 'completeProcedure': op['completeProcedure']}
            binding = {**info(self.candidate_path), 'pointer': '/cards/' + str(list(self.cards).index(sid)) + '/operationalCandidate'}
            return view, projection, binding, True
        if source['status'] != 'operational-playtest-draft' or not source['operational']:
            raise ValueError('Unapproved non-DI7 payload is not available to this evaluator')
        if sid not in {'counterspell', 'alignment-suggestion', 'fate-coin', 'arcane-ward'}:
            raise ValueError('No payload adapter supplied for this ordinary counterpart')
        return deepcopy(source), deepcopy(source['operational']), {**info(self.catalog_path), 'pointer': '/spells/' + str(self.catalog['spells'].index(source))}, False


class DI7CastTransactions:
    def __init__(self, sources, actors, world, *, now=3600):
        self.sources = sources; self.actors = deepcopy(actors); self.world = deepcopy(world)
        self.now = now; self.casts = {}; self.stack = []; self.attempts = set(); self.events = []
        for actor_id, actor in self.actors.items():
            provider = actor['provider']; level = integer(actor['classLevel'], 'class level', 1, 20)
            integer(actor['totalLevel'], 'total level', level, 20); integer(actor['abilityScore'], 'ability', 1, 30)
            if provider not in sources.classes:
                raise ValueError('Only the four actual DI7 providers are implemented')
            if not actor.get('attainmentPremise'):
                raise ValueError('Conditional attained-level provenance required')
            maximum = sources.classes[provider]['rpByClassLevel'][level - 1]
            actor.update(maxRP=maximum, rp=maximum, dissonance=0, previousSpell=None, refrain=0,
                learned={}, prepared=[], preparationHistory=[], wizardFamilies=[], concentration=None,
                actions=1, reactions=1, turnId=None, turnHistory=[], endConcentrationHistory=[])
            if provider == 'Wizard' and actor['specialization'] not in {'Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation'}:
                raise ValueError('Actual Wizard school choice required')

    def snapshot(self):
        return {'now': self.now, 'actors': deepcopy(self.actors), 'world': deepcopy(self.world),
            'casts': deepcopy(self.casts), 'stack': list(self.stack), 'attempts': [list(x) for x in sorted(self.attempts)], 'events': deepcopy(self.events)}

    def advance(self, now):
        if type(now) not in {int, float} or not math.isfinite(now) or now < self.now:
            raise ValueError('Ordered finite time required')
        self.now = now

    def learn(self, actor_id, sid, at_level, event):
        actor = self.actors[actor_id]; provider = actor['provider']
        integer(at_level, 'learning level', 1, actor['classLevel'])
        if event in [x['event'] for x in self.events] or sid in actor['learned']:
            raise ValueError('Unique actual learning opportunity and spell required')
        card, _, binding, candidate = self.sources.spell(sid, provider)
        rank = card['classAccess'][provider]['rank']
        if card['classAccess'][provider]['minimumClassLevel'] > at_level or rank > self.sources.classes[provider]['maxSpellRankByClassLevel'][at_level - 1]:
            raise ValueError('Spell was not legal at the actual learning level')
        if rank == 0:
            raise ValueError('Ranked learning only in this finite adapter')
        if provider == 'Wizard':
            capacity = 6 if at_level == 1 else 2 if at_level <= 4 else 3 if at_level <= 8 else 4 if at_level <= 12 else 5 if at_level <= 16 else 6
        else:
            first = next(i + 1 for i, rank_limit in enumerate(self.sources.classes[provider]['maxSpellRankByClassLevel']) if rank_limit >= 1)
            full = self.sources.chassis[provider]['weaveTier'] == 'full'
            capacity = 2 if at_level == first else 1 if full or at_level % 2 == 0 else 0
        already = sum(x['atClassLevel'] == at_level for x in actor['learned'].values())
        if already >= capacity:
            raise ValueError('No unspent ranked learning addition at this class level')
        actor['learned'][sid] = {'spellId': sid, 'atClassLevel': at_level, 'event': event, 'sourceBinding': binding,
            'kind': 'wizard-level-up-book-addition' if provider == 'Wizard' else 'shared-known-spell-level-addition',
            'availableAdditionsAtLevel': capacity, 'rank': rank, 'candidateSimulationOnly': candidate}
        self.events.append({'event': event, 'kind': 'conditional-learning-executed', 'actor': actor_id, 'spellId': sid, 'classLevel': at_level})

    def prepare_wizard(self, actor_id, spells, event, rest):
        actor = self.actors[actor_id]
        if actor['provider'] != 'Wizard' or actor['preparationHistory'] or not actor['bookPresent']:
            raise ValueError('One actual initial book study is implemented')
        if rest.get('actor') != actor_id or rest.get('completedAt') != 0 or not rest.get('sourceEvent'):
            raise ValueError('An explicitly conditional completed own long rest at time0 is required')
        if self.now < 3600 or not actor['studyUninterrupted']:
            raise ValueError('The required uninterrupted one-hour study must finish')
        if len(spells) != len(set(spells)) or not set(spells) <= set(actor['learned']):
            raise ValueError('Actual spellbook subset required')
        if len(spells) > max(1, actor['classLevel'] + (actor['abilityScore'] - 10) // 2):
            raise ValueError('Prepared capacity exceeded')
        actor['prepared'] = list(spells)
        actor['preparationHistory'].append({'event': event, 'rest': deepcopy(rest), 'studyStart': 0, 'studyEnd': 3600, 'spells': list(spells)})

    def begin_turn(self, actor_id, turn_id):
        actor = self.actors[actor_id]
        if self.stack or turn_id in actor['turnHistory']:
            raise ValueError('New actual regular turn with no unresolved cast required')
        actor.update(turnId=turn_id, actions=1, reactions=1)
        actor['turnHistory'].append(turn_id)

    def route(self, actor_id, sid):
        actor = self.actors[actor_id]; provider = actor['provider']
        card, op, binding, candidate = self.sources.spell(sid, provider)
        if actor['heroPath'] == 'Bloodcaller' and provider == 'Shaman':
            raise ValueError('Bloodcaller has lost ordinary Shaman casting')
        if not actor['providerRetained']:
            raise ValueError('The actual ordinary provider is no longer retained')
        placement = card['classAccess'][provider]
        if actor['classLevel'] < placement['minimumClassLevel'] or placement['rank'] > self.sources.classes[provider]['maxSpellRankByClassLevel'][actor['classLevel'] - 1]:
            raise ValueError('Actual provider level/rank gate fails')
        credential = actor['learned'].get(sid)
        if not credential or credential['sourceBinding'] != binding:
            raise ValueError('A matching actual learning history is required')
        if provider == 'Wizard' and sid not in actor['prepared']:
            raise ValueError('Ordinary Wizard spell is not currently prepared')
        return card, op, binding, candidate

    def _components(self, actor_id, op):
        actor = self.actors[actor_id]; body = actor['body']
        if not body['conscious'] or not body['canAct'] or body['ordinarySpellProhibited']:
            raise ValueError('Current body/ordinary casting restriction')
        if 'V' in op['components'] and (body['silenced'] or not body['canSpeak']):
            raise ValueError('Audible verbal component unavailable')
        if 'S' in op['components'] and not any(x['usable'] and x['holding'] is None for x in body['hands'].values()):
            raise ValueError('Actual free usable somatic hand unavailable')
        focus = body['focus']
        if 'F' in op['components'] and (not focus or focus['owner'] != actor_id or actor['provider'] not in focus['qualifiedClasses'] or not focus['accessible']):
            raise ValueError('Own actual accessible class-qualified focus unavailable')

    def _line(self, actor_id, target_id, range_feet, *, sight=False):
        actor = self.actors[actor_id]; target = self.world['entities'].get(target_id)
        relation = self.world['relations'].get(actor_id + '>' + target_id)
        if not target or not relation or not relation['sourceFact'] or not relation['lineOfEffect'] or not relation['perceived']:
            raise ValueError('Actual source-qualified perception and line of effect required')
        if sight and not relation['visible']:
            raise ValueError('This source requires actual sight')
        if abs(actor['positionFeet'] - target['positionFeet']) > range_feet:
            raise ValueError('Out of range in this straight-line geometry fixture')
        return target

    def _target(self, actor_id, sid, request, op):
        if sid == 'fate-echo':
            raise ValueError('Fate requires the later atomic outer/child adapter; no standalone outer bypass')
        if sid == 'counterspell':
            trigger = self.casts.get(request.get('pendingCast'))
            if not trigger or trigger['status'] != 'pending' or not self.stack or self.stack[-1] != trigger['id'] or trigger['actor'] == actor_id:
                raise ValueError('Another actual currently pending top cast required')
            if (actor_id, trigger['id']) in self.attempts:
                raise ValueError('One attempt per creature against this pending cast')
            self._line(actor_id, trigger['actor'], 60)
            return
        if sid == 'mass-revelation':
            direction = request.get('direction')
            if not isinstance(direction, list) or len(direction) != 3 or any(type(n) not in {float, int} or not math.isfinite(n) for n in direction) or sum(n*n for n in direction) <= 0:
                raise ValueError('A genuine recorded facing vector is required')
            return
        target = self._line(actor_id, request.get('target'), op['rangeFeet'], sight=sid == 'arcane-ward')
        if sid in {'premonition-shield', 'alignment-purge', 'alignment-suggestion', 'arcane-ward'} and target['kind'] != 'creature':
            raise ValueError('Actual creature required')
        if sid in {'premonition-shield', 'arcane-ward'} and not target['willing']:
            raise ValueError('Actual willingness required')
        if sid == 'premonition-shield' and not target['alliedTo'].get(actor_id):
            raise ValueError('Actual allied target required')
        if sid == 'vision-quest' and (not request.get('question') or request['question'] not in target['relatedQuestions']):
            raise ValueError('Specific question needs an actually related anchor')
        if sid == 'faction-omniscience' and (target['kind'] != 'creature' or request.get('faction') not in self.actors[actor_id]['knownFactions'] or request.get('faction') not in self.world['establishedFactions']):
            raise ValueError('Known exact faction and perceived creature reference required')
        if sid == 'resonance-sight-supreme' and target['kind'] != 'point':
            raise ValueError('The exact perceived sphere center is required')
        if sid == 'fate-coin':
            hand = target.get('hands', {}).get(request.get('hand'))
            if target['kind'] != 'creature' or not target['willing'] or not hand or not hand['usable'] or hand['holding'] is not None:
                raise ValueError('Actual willing free receiving hand required')

    def declare(self, actor_id, sid, cast_id, request):
        if cast_id in self.casts:
            raise ValueError('Duplicate cast identity')
        actor = self.actors[actor_id]
        card, op, binding, candidate = self.route(actor_id, sid)
        self._components(actor_id, op); self._target(actor_id, sid, request, op)
        counter = sid == 'counterspell'
        if counter:
            if actor['reactions'] < 1 or not actor['body']['reactionLegal']:
                raise ValueError('Actual legal remaining Reaction required')
        elif actor['turnId'] is None or actor['actions'] < 1 or self.stack:
            raise ValueError('Own available Action and no pending resolution required')
        modifier = (actor['abilityScore'] - 10) // 2; proficiency = 2 + (actor['totalLevel'] - 1) // 4
        quote = quote_cast(card, actor['provider'], actor['classLevel'], available_spell_ids={sid}, rp=actor['rp'], max_rp=actor['maxRP'],
            dissonance=actor['dissonance'], proficiency=proficiency, casting_modifier=modifier, previous_spell_id=actor['previousSpell'], previous_refrain=actor['refrain'])
        strain = quote['dissonanceAddedBeforeClassInterface']; hooks = []
        if actor['provider'] == 'Wizard' and self.world['encounter']['isRealEncounter'] and sid not in actor['wizardFamilies']:
            strain -= 0 if quote['rank'] == 0 else 1 if quote['rank'] <= 5 else 2
            hooks.append('Wizard-first-prepared-family-base-only')
        # No source totem/aura is supplied in this adapter; no Shaman vent is
        # inferred from class membership. A later actual aura adapter may add it.
        before = {k: deepcopy(actor[k]) for k in ['rp', 'dissonance', 'previousSpell', 'refrain', 'concentration', 'actions', 'reactions']}
        actor['reactions' if counter else 'actions'] -= 1
        actor.update(rp=quote['rpAfterPayment'], dissonance=actor['dissonance'] + strain, previousSpell=sid, refrain=quote['refrain'])
        if actor['provider'] == 'Wizard' and self.world['encounter']['isRealEncounter'] and sid not in actor['wizardFamilies']:
            actor['wizardFamilies'].append(sid)
        if op['concentration']:
            previous = actor['concentration']
            if previous:
                actor['endConcentrationHistory'].append({'id': previous, 'reason': 'new-cast-commit', 'replacedBy': cast_id, 'at': self.now})
            actor['concentration'] = cast_id
        placement = card['classAccess'][actor['provider']]
        dc = 8 + proficiency + modifier + (1 if actor['provider'] == 'Wizard' and placement['school'] == actor['specialization'] else 0)
        receipt = {'id': cast_id, 'actor': actor_id, 'spellId': sid, 'provider': actor['provider'], 'sourceBinding': binding,
            'candidateSimulationOnly': candidate, 'quoteHelperStatusProjectionOnly': candidate, 'rank': quote['rank'], 'school': placement['school'],
            'abilityModifier': modifier, 'proficiency': proficiency, 'dc': dc, 'components': deepcopy(op['components']),
            'request': deepcopy(request), 'committedAt': self.now, 'quote': quote, 'dissonanceAdded': strain, 'classHooks': hooks,
            'before': before, 'afterCommit': {k: deepcopy(actor[k]) for k in before}, 'status': 'pending', 'refund': 0}
        self.casts[cast_id] = receipt; self.stack.append(cast_id)
        if counter:
            self.attempts.add((actor_id, request['pendingCast']))
        return deepcopy(receipt)

    def resolve_counter(self, cast_id, natural):
        if not self.stack or self.stack[-1] != cast_id or self.casts[cast_id]['spellId'] != 'counterspell' or self.casts[cast_id]['status'] != 'pending':
            raise ValueError('Resolve the actual surviving top Counterspell first')
        cast = self.casts[cast_id]; trigger = self.casts[cast['request']['pendingCast']]
        outcome = task_check(natural, cast['abilityModifier'] + cast['proficiency'], 10 + 2 * trigger['rank'])
        self.stack.pop(); cast.update(status='resolved', resolvedAt=self.now, counterOutcome=outcome)
        if outcome['success']:
            if not self.stack or self.stack[-1] != trigger['id']:
                raise ValueError('Corrupted nested cast order')
            self.stack.pop(); trigger.update(status='countered', negatedBy=cast_id)
            owner = self.actors[trigger['actor']]
            if owner['concentration'] == trigger['id']:
                owner['concentration'] = None
        return deepcopy(outcome)

    def take_payload_resolution(self, cast_id):
        if not self.stack or self.stack[-1] != cast_id or self.casts[cast_id]['status'] != 'pending' or self.casts[cast_id]['spellId'] == 'counterspell':
            raise ValueError('One surviving top cast required for its separate payload adapter')
        cast = self.casts[cast_id]
        self.stack.pop()
        owner = self.actors[cast['actor']]
        body = owner['body']
        if not body['conscious'] or not body['canAct'] or body['ordinarySpellProhibited']:
            cast.update(status='interrupted-no-refund', payloadBoundaryAt=self.now)
            if owner['concentration'] == cast_id:
                owner['concentration'] = None
        else:
            cast.update(status='ready-for-payload', payloadBoundaryAt=self.now)
        return deepcopy(cast)
