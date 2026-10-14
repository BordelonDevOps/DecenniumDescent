"""Conditional AP-AS-01 resolution/lifecycle component, not a casting engine.

The caller supplies a conditional committed-cast receipt. This component does
not authenticate acquisition, RP payment, components, range, or Counterspell.
It implements only outside-initiative elapsed-time fixtures. Existing
Suggestion virtual/regular-start timing requires the later shared clock adapter.
"""
from copy import deepcopy
import math

AXES = {'order': ['Lawful', 'Neutral', 'Chaotic'], 'ethics': ['Good', 'Neutral', 'Evil']}
SPELLS = {'alignment-suggestion', 'alignment-purge'}


def number(value):
    if type(value) not in {int, float} or not math.isfinite(value) or value < 0:
        raise ValueError('Finite nonnegative time required')
    return value


def alignment(value):
    if not isinstance(value, dict) or set(value) != set(AXES):
        raise ValueError('Two explicit canonical axis slots required, including nulls')
    if any(value[k] is not None and value[k] not in AXES[k] for k in AXES):
        raise ValueError('Unknown is null, not a fabricated canonical alignment')
    return deepcopy(value)


class AlignmentComponent:
    def __init__(self, actors, source_bindings):
        if set(source_bindings) != SPELLS:
            raise ValueError('Both exact actual candidate/counterpart bindings required')
        self.actors = deepcopy(actors)
        for actor in self.actors.values():
            alignment(actor['underlying'])
            if not isinstance(actor['immunities'], list):
                raise ValueError('Actual source-scoped immunity records required')
        self.sources = deepcopy(source_bindings)
        self.now = 0
        self.casts = {}
        self.effects = {}
        self.concentration = {}
        self.events = []

    def snapshot(self):
        return {'now': self.now, 'actors': deepcopy(self.actors), 'casts': deepcopy(self.casts),
            'effects': deepcopy(self.effects), 'concentration': deepcopy(self.concentration), 'events': deepcopy(self.events)}

    def end(self, effect_id, reason):
        e = self.effects.get(effect_id)
        if e and e['state'] == 'live':
            e.update(state='ended', endedAt=self.now, endReason=reason)
        for caster, cast in list(self.concentration.items()):
            if cast == effect_id:
                del self.concentration[caster]

    def advance(self, when):
        number(when)
        if when < self.now:
            raise ValueError('Ordered time cannot rewind')
        self.now = when
        for effect_id, e in self.effects.items():
            if e['state'] == 'live' and when >= e['deadline']:
                self.end(effect_id, 'elapsed-deadline')

    def active(self, target, spell):
        return [e for e in self.effects.values() if e['target'] == target and e['spellId'] == spell and e['state'] == 'live' and not e['suppressed'] and self.now < e['deadline']]

    def effective(self, actor_id):
        result = deepcopy(self.actors[actor_id]['underlying'])
        for e in self.active(actor_id, 'alignment-suggestion'):
            result.update(e['values'])
        if self.active(actor_id, 'alignment-purge'):
            result = {'order': 'Neutral', 'ethics': 'Neutral'}
        return result

    def begin_conditional_committed_cast(self, receipt):
        required = {'castId', 'spellId', 'sourceBinding', 'caster', 'target', 'committedAt', 'paymentPremise', 'clockMode'}
        if set(receipt) != required or receipt['spellId'] not in SPELLS or receipt['castId'] in self.casts:
            raise ValueError('Unique complete conditional cast receipt required')
        if receipt['sourceBinding'] != self.sources[receipt['spellId']]:
            raise ValueError('Wrong source version')
        if receipt['caster'] not in self.actors or receipt['target'] not in self.actors:
            raise ValueError('Actual conditional actors required')
        if receipt['clockMode'] != 'outside-initiative-elapsed' or receipt['committedAt'] != self.now:
            raise ValueError('Only current outside-initiative fixtures are implemented here')
        premise = receipt['paymentPremise']
        if premise.get('kind') != 'conditional-upstream-commit-not-executed-here' or not premise.get('fixtureId'):
            raise ValueError('Explicitly bounded upstream premise required')
        caster = receipt['caster']
        previous = self.concentration.get(caster)
        if previous:
            self.end(previous, 'cast-start-concentration-displacement')
        self.concentration[caster] = receipt['castId']
        self.casts[receipt['castId']] = {**deepcopy(receipt), 'state': 'committed', 'refund': 0}
        self.events.append({'event': 'conditional-cast-start', 'cast': receipt['castId'], 'time': self.now})

    def counter_conditional_cast(self, cast_id):
        cast = self.casts[cast_id]
        if cast['state'] != 'committed':
            raise ValueError('One unresolved conditional cast required')
        cast['state'] = 'countered'
        self.end(cast_id, 'countered')

    def resolve(self, cast_id, *, face, modifier, dc):
        cast = self.casts[cast_id]
        if cast['state'] != 'committed' or self.concentration.get(cast['caster']) != cast_id:
            raise ValueError('Current unresolved cast and surviving concentration required')
        if type(face) is not int or not 1 <= face <= 20 or type(modifier) is not int or type(dc) is not int:
            raise ValueError('Actual complete binary save operands required')
        target = self.actors[cast['target']]
        total = face + modifier
        immune = any(x.get('affects') == 'alignment-alteration' and x.get('source') for x in target['immunities'])
        values = {}
        orientation = None
        if total < dc and not immune:
            baseline = deepcopy(target['underlying'])
            if cast['spellId'] == 'alignment-purge':
                if all(baseline[k] in AXES[k] for k in AXES):
                    values = {'order': 'Neutral', 'ethics': 'Neutral'}
            else:
                orientation = self.effective(cast['caster'])
                for key, choices in AXES.items():
                    if baseline[key] is None or orientation[key] is None or baseline[key] == orientation[key]:
                        continue
                    start, toward = choices.index(baseline[key]), choices.index(orientation[key])
                    values[key] = choices[start + (1 if toward > start else -1)]
        cast.update(state='resolved', resolvedAt=self.now, save={'face': face, 'modifier': modifier, 'total': total, 'dc': dc, 'succeeded': total >= dc}, orientationSnapshot=orientation)
        if values:
            for effect_id, old in list(self.effects.items()):
                if old['target'] == cast['target'] and old['spellId'] == cast['spellId'] and old['state'] == 'live':
                    self.end(effect_id, 'same-family-replacement')
            self.effects[cast_id] = {'id': cast_id, 'spellId': cast['spellId'], 'caster': cast['caster'], 'target': cast['target'],
                'values': values, 'appliedAt': self.now, 'deadline': self.now + 60, 'state': 'live', 'suppressed': False,
                'sourceBinding': deepcopy(cast['sourceBinding'])}
        else:
            self.end(cast_id, 'no-new-application')
        self.events.append({'event': 'conditional-resolution', 'cast': cast_id, 'time': self.now})
        # No state-diagnostic result is returned to the caster by this component.
        return {'resolutionComplete': True, 'informationGranted': False, 'refund': 0}

    def set_underlying(self, actor_id, values, source_event):
        values = alignment(values)
        if not source_event or any(x.get('eventId') == source_event for x in self.events):
            raise ValueError('Unique independent authorized-change premise required')
        before = deepcopy(self.actors[actor_id]['underlying'])
        self.actors[actor_id]['underlying'] = values
        self.events.append({'event': 'conditional-independent-change', 'eventId': source_event, 'actor': actor_id, 'before': before, 'after': values, 'time': self.now})

    def suppress(self, effect_id, value):
        if type(value) is not bool or effect_id not in self.effects or self.effects[effect_id]['state'] != 'live':
            raise ValueError('An existing live effect and explicit suppression state required')
        self.effects[effect_id]['suppressed'] = value

    def caster_loses_concentration(self, caster, reason):
        if reason not in {'death', 'incapacitated', 'failed-concentration-save', 'voluntary-end'}:
            raise ValueError('Explicit supported concentration ending required')
        effect_id = self.concentration.get(caster)
        if effect_id:
            self.end(effect_id, reason)
