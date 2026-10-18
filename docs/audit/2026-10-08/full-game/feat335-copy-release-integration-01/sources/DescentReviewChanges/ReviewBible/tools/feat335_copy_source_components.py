"""Finite source-component witnesses for SUP-07's seven feat-copy profiles.

This is a source adapter, not a capture/release or ordinary casting engine.
Actual completion, direct perception and upstream legality remain explicit
scenario premises. Only the named spell procedures below are executable here.
"""
from copy import deepcopy


def integer(value, label, minimum=0, maximum=None):
    if type(value) is not int or value < minimum or maximum is not None and value > maximum:
        raise ValueError('Invalid ' + label)
    return value


def dice(values, number, sides):
    if not isinstance(values, list) or len(values) != number:
        raise ValueError('Exact original native dice required')
    return sum(integer(v, 'native die', 1, sides) for v in values)


class CopySourceComponents:
    SUPPORTED = {'arcane-ray', 'burning-hands', 'lifedraw', 'false-life', 'slow', 'shield', 'mist-step'}

    def __init__(self, sources):
        self.sources = sources
        self.events = {}

    def snapshot(self):
        return deepcopy(self.events)

    def witness(self, event, spell_id, source_class, source_level, premises, outcome):
        if not isinstance(event, str) or not event or event in self.events:
            raise ValueError('One new canonical source event required')
        if spell_id not in self.SUPPORTED:
            raise ValueError('No executable source adapter for this spell; do not infer a role from its name')
        if set(premises) != {'resolved', 'directlyWitnessed', 'actualLegalSourceCast', 'copyDerived', 'protectedFeature'}:
            raise ValueError('Exact upstream source premises required')
        if any(premises[k] is not True for k in ['resolved', 'directlyWitnessed', 'actualLegalSourceCast']):
            raise ValueError('Actual directly witnessed legally resolved source required')
        if premises['copyDerived'] is not False or premises['protectedFeature'] is not False:
            raise ValueError('Copies and protected features are not eligible in this finite ordinary-spell slice')
        route = self.sources.ordinary(spell_id, source_class)
        integer(source_level, 'actual source class level', route['minimumClassLevel'], 20)
        card = self.sources.dependencies[spell_id]['completeCurrentProcedureCard']
        operational = card.get('operational') or card.get('operationalCandidate')
        components = []

        def exact(keys):
            if not isinstance(outcome, dict) or set(outcome) != set(keys):
                raise ValueError('Exact source outcome operands required; no generic magnitude or invented rider')

        def component(profile, **kwargs):
            components.append({'profile': profile, **kwargs})

        if spell_id == 'arcane-ray':
            assert '1d6 force damage' in operational['resolution']
            exact(['actualHit', 'ordinaryNativeDice'])
            if type(outcome['actualHit']) is not bool:
                raise ValueError('Actual attack outcome required')
            if outcome['actualHit']:
                component('strike', nativeMagnitude=dice(outcome['ordinaryNativeDice'], 1, 6), damageType='force')
            elif outcome['ordinaryNativeDice'] != []:
                raise ValueError('Miss has no native damage roll')
        elif spell_id == 'burning-hands':
            assert '3d6 fire damage' in operational['resolution']
            exact(['ordinaryNativeDice', 'actualResolvedArea'])
            if outcome['actualResolvedArea'] is not True:
                raise ValueError('Actual area component required')
            component('burst', nativeMagnitude=dice(outcome['ordinaryNativeDice'], 3, 6), damageType='fire')
        elif spell_id == 'lifedraw':
            assert 'half the actual necrotic damage dealt, rounded down' in operational['effect']
            exact(['actualHit', 'ordinaryNativeDice', 'actualNecroticDamageDealt', 'targetCategory'])
            if type(outcome['actualHit']) is not bool:
                raise ValueError('Actual attack outcome required')
            actual = integer(outcome['actualNecroticDamageDealt'], 'actual damage')
            allowed = {'living-hostile', 'undead', 'construct', 'farmed-summon', 'ally', 'helpless-captive', 'corpse', 'other-nonliving'}
            if outcome['targetCategory'] not in allowed:
                raise ValueError('Actual source target eligibility required')
            if outcome['actualHit']:
                component('strike', nativeMagnitude=dice(outcome['ordinaryNativeDice'], 3, 6), damageType='necrotic')
                if actual > 0 and outcome['targetCategory'] == 'living-hostile':
                    component('mend', nativeMagnitude=actual // 2)
            elif outcome['ordinaryNativeDice'] or actual:
                raise ValueError('Miss cannot produce damage or healing')
        elif spell_id == 'false-life':
            assert '1d4+4 temporary HP' in operational['effect']
            exact(['ordinaryNativeDice', 'actualWillingLivingRecipient'])
            if outcome['actualWillingLivingRecipient'] is not True:
                raise ValueError('Actual legal temporary-HP recipient required')
            component('ward', nativeMagnitude=dice(outcome['ordinaryNativeDice'], 1, 4) + 4)
        elif spell_id == 'slow':
            assert 'half Speed' in operational['effect']
            exact(['actualFailedSave', 'actualSurvivingControlComponent', 'mode'])
            if outcome['mode'] != route['school']:
                raise ValueError('Actual source class determines Slow mode')
            if any(type(outcome[k]) is not bool for k in ['actualFailedSave', 'actualSurvivingControlComponent']):
                raise ValueError('Actual binary save and component defense outcomes required')
            if outcome['actualFailedSave'] and outcome['actualSurvivingControlComponent']:
                component('hindrance')
        elif spell_id == 'shield':
            assert '+5 AC' in operational['effect']
            exact(['actualAcBenefitEstablished'])
            if type(outcome['actualAcBenefitEstablished']) is not bool:
                raise ValueError('Actual AC benefit outcome required')
            if outcome['actualAcBenefitEstablished']:
                component('boon', benefitedStatistics=['AC'])
        elif spell_id == 'mist-step':
            assert 'Teleport to the chosen visible unoccupied space within 30 feet' in operational['effect']
            exact(['observedDistance', 'actualLegalTeleportCompleted'])
            distance = integer(outcome['observedDistance'], 'actual completed distance', 0, 30)
            if type(outcome['actualLegalTeleportCompleted']) is not bool:
                raise ValueError('Actual source teleport outcome required')
            if outcome['actualLegalTeleportCompleted']:
                component('step', observedDistance=distance, wasTeleport=True)

        record = {'sourceEvent': event, 'spellId': spell_id, 'sourceRoute': route,
            'sourceClassLevel': source_level, 'premises': deepcopy(premises), 'outcome': deepcopy(outcome),
            'originalRank': route['rank'], 'components': components,
            'scope': 'conditional-source-component-witness; no capture/payment/release executed'}
        self.events[event] = record
        return deepcopy(record)

    def select(self, event, profile):
        record = self.events.get(event)
        if not record:
            raise ValueError('Existing canonical resolved source event required')
        choices = [x for x in record['components'] if x['profile'] == profile]
        if len(choices) != 1:
            raise ValueError('Source event did not actually express this profile')
        rank = record['originalRank']
        return {'sourceEvent': event, 'sourceSpellId': record['spellId'],
            'sourcePayloadBinding': deepcopy(record['sourceRoute']['payloadBinding']),
            'originalRank': rank, 'copyRank': 0 if rank == 0 else max(1, rank // 2),
            **deepcopy(choices[0]), 'captureAuthorized': False, 'releaseExecuted': False}


def bounded_native_numeric(component, rolled):
    if component['profile'] not in {'strike', 'burst', 'mend', 'ward'}:
        raise ValueError('This profile has no numeric damage/healing/ward roll')
    q = integer(component['copyRank'], 'copy rank', 0, 9)
    magnitude = integer(component['nativeMagnitude'], 'original native magnitude')
    return min(dice(rolled, q + 1, 6), magnitude // 2)
