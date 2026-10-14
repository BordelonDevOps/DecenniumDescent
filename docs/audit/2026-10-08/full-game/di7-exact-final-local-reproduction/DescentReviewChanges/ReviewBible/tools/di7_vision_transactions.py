"""Paid Vision Quest, ordered trance lifecycle and conditional fact projection.

World facts, concise supported text, semantic question equivalence, causal step
feasibility and native protection scope/grants are explicit upstream premises.
This evaluator implements no new protection source, natural-language oracle,
campaign authentication, general movement/condition scheduler or rest activity.
"""
from copy import deepcopy
from dataclasses import asdict
import math
from di7_fate_transactions import FateTransactions
from core_playtest_rules import LifeState, saving_throw
from healing_playtest_rules import survival_damage_event


class ConditionalInformation:
    def __init__(self, dossier):
        self.data = deepcopy(dossier)
        if self.data.get('kind') != 'explicit-conditional-Director-established-world':
            raise ValueError('A labeled actual-world premise is required, not source prose treated as fact')
        self.internal_queries = []
        for fid, fact in self.data['facts'].items():
            if fact['id'] != fid or not fact.get('authorityVersion') or not fact.get('authorityEvent'):
                raise ValueError('Fact identity, version and authoritative world event required')
        for protection in self.data['protections']:
            native = protection['nativeScopePremise']
            if native.get('kind') != 'conditional-actual-native-protection-scope' or not native.get('sourceVersion') or not native.get('sourceGrantEvent') or not native.get('completeScopeText'):
                raise ValueError('Native source/grant/scope premise required; query invents no protection')
            if protection['mode'] not in {'block', 'mask'}:
                raise ValueError('Actual source protection behavior required')
            if protection['mode'] == 'mask' and not native.get('explicitlyAuthorizesAlteredResult'):
                raise ValueError('No generic false result without native source authority')

    def _applies(self, protection, fact, *, now, rank, school):
        return (protection['activeFrom'] <= now < protection['activeUntil']
            and fact['subject'] in protection['subjects'] and school in protection['querySchools']
            and protection['minimumQueryRank'] <= rank <= protection['maximumQueryRank']
            and fact['category'] in protection['categories']
            and protection['factTimeFrom'] <= fact['actualTime'] < protection['factTimeUntil'])

    def project(self, fid, *, now, rank=7, school='Divination'):
        fact = self.data['facts'].get(fid)
        if not fact or not fact['establishedAt'] <= now:
            return None
        applicable = [p for p in self.data['protections'] if self._applies(p, fact, now=now, rank=rank, school=school)]
        if any(p['protectsExistence'] and p['mode'] == 'block' for p in applicable):
            return None
        out = deepcopy(fact['publicFields'])
        # Multiple native masks/blocks would need their actual source arbitration.
        # The supplied finite dossier deliberately has no conflicting overrides.
        for field in list(out):
            matches = [p for p in applicable if field in p['fields']]
            if len(matches) > 1: raise ValueError('Native overlapping protection arbitration not supplied')
            if matches:
                p = matches[0]; out[field] = p['maskedFields'][field] if p['mode'] == 'mask' else None
        return out

    def answer(self, question, *, now, caster, cast_id):
        specification = self.data['questions'].get(question)
        fallback = {'text': 'The inquiry supplies no actionable answer.', 'steps': []}
        if not specification:
            result = fallback
        else:
            canonical = specification['canonicalQuestion']
            spec = self.data['canonicalQuestions'][canonical]
            central = self.project(spec['centralFact'], now=now)
            # Absence/unknown/protection share a non-diagnostic public fallback.
            if not central or not central.get('text'):
                result = fallback
            else:
                parts = [central['text']]; steps = []
                horizon = now + 30 * 86400 if spec['future'] else None
                if spec['future']:
                    forecast_time = self.data['facts'][spec['centralFact']].get('forecastForTime')
                    if forecast_time is not None and not now <= forecast_time <= horizon:
                        result = fallback
                        self.internal_queries.append({'caster': caster, 'castId': cast_id, 'question': question, 'at': now, 'result': deepcopy(result)})
                        return result
                    uncertainty = self.project(spec['uncertaintyFact'], now=now)
                    if not uncertainty or not uncertainty.get('text'):
                        result = fallback
                        self.internal_queries.append({'caster': caster, 'castId': cast_id, 'question': question, 'at': now, 'result': deepcopy(result)})
                        return result
                    parts.append(uncertainty['text'])
                if len(' '.join(parts).split()) > 150:
                    raise ValueError('A source-supported concise central projection within150 words is required')
                for step_id in spec['orderedPracticalSteps']:
                    step = self.data['steps'][step_id]
                    if not step['actualFeasibilityEvent'] or not step['feasible']:
                        continue
                    if horizon is not None and not now <= step['earliestActionAt'] <= horizon:
                        continue
                    support = [self.project(fid, now=now) for fid in step['requiredReadableFacts']]
                    projected = self.project(step['instructionFact'], now=now)
                    if any(x is None or not x.get('text') for x in support) or not projected or not projected.get('text'):
                        continue
                    instruction = projected['text']
                    if len(' '.join(parts + steps + [instruction]).split()) <= 150:
                        steps.append(instruction)
                    if len(steps) == 3: break
                result = {'text': ' '.join(parts + steps), 'steps': steps}
                if horizon is not None: result['guidanceHorizonEndsAt'] = horizon
                assert len(result['text'].split()) <= 150
        self.internal_queries.append({'caster': caster, 'castId': cast_id, 'question': question, 'at': now, 'result': deepcopy(result)})
        return deepcopy(result)


class VisionTransactions(FateTransactions):
    def __init__(self, *args, dossier, **kwargs):
        super().__init__(*args, **kwargs)
        self.information = ConditionalInformation(dossier)
        self.trances = {}; self.memories = {}; self.vision_events = []; self.sequence = 0
        self.last_order = None; self.life = {aid: LifeState(100, 100, temp_hp=5) for aid in self.actors}
        self.life_premise = 'Conditional maximum100/current100/temp5 life-state slice; no source acquisition of that HP is authenticated.'

    def snapshot(self):
        return {**super().snapshot(), 'trances': deepcopy(self.trances), 'memories': deepcopy(self.memories),
            'visionEvents': deepcopy(self.vision_events), 'lastOrder': list(self.last_order) if self.last_order else None,
            'life': {a: asdict(s) for a, s in self.life.items()}, 'lifePremise': self.life_premise,
            'privateInformationDossier': deepcopy(self.information.data), 'internalQueries': deepcopy(self.information.internal_queries)}

    def _trance(self, actor):
        return next((t for t in self.trances.values() if t['actor'] == actor and t['status'] == 'active'), None)

    def _components(self, actor_id, op):
        if self._trance(actor_id): raise ValueError('End the actual trance before a voluntary casting action/Reaction')
        return super()._components(actor_id, op)

    def end_trance(self, cast_id, reason):
        trance = self.trances[cast_id]
        if trance['status'] != 'active': return
        trance.update(status='interrupted', endedAt=self.now, endReason=reason, answerDelivered=False)
        actor = self.actors[trance['actor']]
        if actor['concentration'] == cast_id: actor['concentration'] = None
        self.vision_events.append({'kind': 'trance-ended', 'castId': cast_id, 'at': self.now, 'reason': reason})

    def resolve_vision(self, cast_id):
        cast = self.casts[cast_id]
        if cast['spellId'] != 'vision-quest': raise ValueError('Actual Vision Quest cast required')
        receipt = self.take_payload_resolution(cast_id)
        if receipt['status'] != 'ready-for-payload': return None
        actor = self.actors[cast['actor']]
        if actor['concentration'] != cast_id:
            cast.update(status='failed-payload-no-refund'); return None
        self.sequence += 1
        trance = {'castId': cast_id, 'actor': cast['actor'], 'question': cast['request']['question'],
            'anchor': cast['request']['target'], 'startedAt': self.now, 'deadline': self.now + 60,
            'position': actor['positionFeet'], 'applicationSequence': self.sequence, 'status': 'active',
            'answerDelivered': False, 'concentrationChecks': [], 'parallelWorkCredit': 0}
        self.trances[cast_id] = trance
        cast.update(status='resolved', resolvedAt=self.now, castingCompletedAt=self.now, tranceId=cast_id)
        return deepcopy(trance)

    def _key(self, trance):
        return (trance['deadline'], 0, trance['startedAt'], trance['applicationSequence'], trance['castId'])

    def _complete(self, trance):
        aid = trance['actor']; actor = self.actors[aid]
        if not actor['body']['conscious'] or not actor['body']['canAct'] or actor['concentration'] != trance['castId'] or actor['positionFeet'] != trance['position']:
            self.end_trance(trance['castId'], 'required-interval-state-lost'); return
        answer = self.information.answer(trance['question'], now=trance['deadline'], caster=aid, cast_id=trance['castId'])
        self.memories.setdefault(aid, []).append({'castId': trance['castId'], 'deliveredAt': trance['deadline'], 'answer': answer})
        trance.update(status='completed', completedAt=trance['deadline'], answerDelivered=True)
        actor['concentration'] = None
        self.vision_events.append({'kind': 'normal-completion-and-answer', 'castId': trance['castId'], 'at': trance['deadline']})

    def _due_before(self, limit):
        for trance in sorted(self.trances.values(), key=self._key):
            key = self._key(trance)
            if trance['status'] == 'active' and key < limit:
                super().advance(trance['deadline']); self.last_order = key; self._complete(trance)

    def advance(self, now):
        if type(now) not in {int, float} or not math.isfinite(now) or now < self.now:
            raise ValueError('Ordered finite time required')
        self._due_before((now, math.inf, math.inf, math.inf, ''))
        super().advance(now)

    def event(self, *, at, phase, applied_at, application_sequence, source_id, kind, actor, **payload):
        if type(at) not in {int, float} or not math.isfinite(at) or at < self.now:
            raise ValueError('Event time must be current or future and finite')
        if type(phase) is not int or phase < 0 or type(application_sequence) is not int or application_sequence < 0:
            raise ValueError('Actual event phase/application sequence required')
        if type(applied_at) not in {int, float} or not math.isfinite(applied_at) or not 0 <= applied_at <= at or not source_id:
            raise ValueError('Actual original application time/source required')
        if kind not in {'forced-movement', 'incapacitated', 'suppression', 'lose-concentration', 'silence', 'damage'}:
            raise ValueError('Only source-qualified explicit event adapters are implemented')
        key = (at, phase, applied_at, application_sequence, source_id)
        if self.last_order is not None and key <= self.last_order: raise ValueError('Previously resolved canonical event cannot be replayed/backdated')
        if kind == 'forced-movement' and (type(payload.get('position')) not in {int, float} or not math.isfinite(payload['position'])):
            raise ValueError('Actual new finite position required')
        if kind == 'damage':
            if type(payload.get('resolvedDamage')) is not int or payload['resolvedDamage'] < 0:
                raise ValueError('Final actual post-defense damage required')
            saving_throw(payload['natural'], payload['constitutionSaveModifier'], max(10, payload['resolvedDamage'] // 2))
        self._due_before(key); super().advance(at); self.last_order = key
        a = self.actors[actor]; trance = self._trance(actor)
        if kind == 'forced-movement':
            moved = payload['position'] != a['positionFeet']; a['positionFeet'] = payload['position']
            self.world['entities'][actor]['positionFeet'] = payload['position']
            if trance and moved: self.end_trance(trance['castId'], 'actual-involuntary-displacement')
        elif kind == 'incapacitated':
            a['body']['canAct'] = False
            if trance: self.end_trance(trance['castId'], 'actual-incapacitation')
        elif kind in {'suppression', 'lose-concentration'}:
            if trance: self.end_trance(trance['castId'], kind)
        elif kind == 'silence': a['body']['silenced'] = True
        else:
            before = self.life[actor]
            after, life_event = survival_damage_event(before, payload['resolvedDamage'], now_seconds=self.now,
                **payload.get('lifeOptions', {}))
            self.life[actor] = after
            if trance:
                if after.dead or after.hp == 0:
                    a['body']['conscious'] = False; self.end_trance(trance['castId'], 'damage-incapacity-or-death')
                elif payload['resolvedDamage'] > 0:
                    outcome = saving_throw(payload['natural'], payload['constitutionSaveModifier'], max(10, payload['resolvedDamage'] // 2))
                    trance['concentrationChecks'].append({'at': at, 'source': source_id, 'dc': max(10, payload['resolvedDamage'] // 2), 'outcome': outcome,
                        'modifierPremise': 'Actual current CON/save modifier supplied, including source-qualified bonuses/penalties; no unknown proficiency or feat is inferred.'})
                    if not outcome['success']: self.end_trance(trance['castId'], 'failed-damage-concentration-save')
            self.vision_events.append({'kind': 'damage-life-resolution', 'actor': actor, 'at': at, 'before': asdict(before), 'after': asdict(after), 'event': life_event})
        self.vision_events.append({'kind': kind, 'actor': actor, 'key': list(key), 'payload': deepcopy(payload)})

    def public_memory(self, actor):
        return deepcopy(self.memories.get(actor, []))

    def communicate(self, speaker, listener, cast_id, channel_event):
        if self._trance(speaker): raise ValueError('No deliberate communication while maintaining the trance')
        source = next((x for x in self.memories.get(speaker, []) if x['castId'] == cast_id), None)
        channel = self.world.get('communicationEvents', {}).get(channel_event)
        if not source or not channel or not channel.get('sourceFact') or channel.get('speaker') != speaker or channel.get('listener') != listener or channel.get('at') != self.now or not channel.get('actuallyReceivedUnderstood'):
            raise ValueError('Actual contemporaneous source-qualified received/understood channel required')
        if channel.get('used'): raise ValueError('Communication event already delivered')
        delivered = channel.get('deliveredText')
        if not isinstance(delivered, str) or not delivered.strip() or delivered not in source['answer']['text']:
            raise ValueError('This bounded adapter requires the actual received literal excerpt of the remembered answer')
        # A paraphrase/lie can exist under its own communication adjudication;
        # this finite adapter neither authenticates it nor copies omitted facts,
        # step lists or the private answer metadata into the listener's knowledge.
        report = {'text': delivered}
        channel['used'] = True
        self.memories.setdefault(listener, []).append({'learnedFrom': speaker, 'channelEvent': channel_event,
            'deliveredAt': self.now, 'answer': report})
        return deepcopy(report)
