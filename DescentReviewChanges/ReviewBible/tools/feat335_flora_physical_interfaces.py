"""Bounded actual task and movement interfaces for Flora and Verdant Bond.

Actor training is source-materialized. World geometry, legal task work/senses,
held usable tools, hazards and canonical action budgets are conditional inputs.
No campaign facts, new permission, free Action or automatic hazard immunity.
"""
from copy import deepcopy
from dataclasses import asdict
from core_playtest_rules import task_check
from combat_playtest_rules import MovementLedger, movement_cost
from feat_exact_01_acquisition_models import pb


class FloraPhysicalInterfaces:
    def __init__(self, flora, inspectors):
        self.flora = flora; self.inspectors = inspectors
        self.pending = {}; self.events = {}; self.knowledge = {}; self.movements = {}
        self.movement = MovementLedger()

    def snapshot(self):
        return {'flora': self.flora.snapshot(), 'inspectors': {
                k: {**deepcopy({n:v for n,v in x.items() if n != 'acquired'}), 'acquired': x['acquired'].snapshot()}
                for k,x in self.inspectors.items()},
            'pending': deepcopy(self.pending), 'events': deepcopy(self.events),
            'knowledge': deepcopy(self.knowledge), 'movements': deepcopy(self.movements),
            'movement': asdict(self.movement)}

    def actor(self, identity):
        if identity == 'owner':
            return self.flora.acquired, self.flora.world['actors']['owner'], self.flora.actions
        if identity not in self.inspectors: raise ValueError('Actual actor and training required')
        x = self.inspectors[identity]
        return x['acquired'], x, x['actions']

    def task_preflight(self, event, actor):
        if event in self.events or event in self.pending or event in self.flora.events:
            raise ValueError('Underlying event identity already used')
        if any(p['actor'] == actor for p in self.pending.values()):
            raise ValueError('Resolve or interrupt the actual pending Action first')
        acquired, state, actions = self.actor(actor)
        if not state['canAct'] or actions < 1:
            raise ValueError('Actual capable actor and unspent Action required')
        return acquired, state

    def commit(self, event, actor, value):
        if actor == 'owner': self.flora.actions -= 1
        else: self.inspectors[actor]['actions'] -= 1
        value = {'event': event, 'actor': actor, 'actionPaid': 1, **deepcopy(value)}
        self.pending[event] = value
        self.events[event] = {'status': 'paid-awaiting-roll', 'declaration': deepcopy(value)}
        return deepcopy(value)

    @staticmethod
    def modifier(acquired, ability, skill=None, tool=None):
        factor = acquired.training_projection['skills'].get(skill, 0) if skill else 0
        if tool:
            factor = int(tool in acquired.training_projection['tools'])
        return (acquired.pay.scores[ability] - 10) // 2 + factor * pb(sum(acquired.pay.current_classes.values()))

    def declare_nature(self, event, *, actual_wilderness, actual_work_and_senses, dc,
                       other_advantage=False, disadvantage=False):
        acquired, _ = self.task_preflight(event, 'owner')
        if not actual_work_and_senses or type(dc) is not int or dc < 0:
            raise ValueError('Actual Nature task, ordinary work/senses and DC required')
        feat_advantage = (acquired.pay.has('verdant_bond') and 'verdant_bond' not in acquired.pay.suppressed
                          and actual_wilderness)
        advantage = bool(other_advantage or feat_advantage)
        mode = 'normal' if advantage == bool(disadvantage) else 'higher' if advantage else 'lower'
        return self.commit(event, 'owner', {'kind': 'Nature-task', 'dc': dc,
            'modifier': self.modifier(acquired, 'INT', skill='Nature'), 'rollMode': mode,
            'verdantAdvantage': bool(feat_advantage), 'noPlantRequired': True})

    def declare_identify(self, event, actor, plant, *, actual_legal_inspection):
        acquired, _ = self.task_preflight(event, actor); p = self.flora.body(plant)
        if not p['armed'] or not actual_legal_inspection:
            raise ValueError('Actual visible armed Flora and ordinary legal inspection required')
        return self.commit(event, actor, {'kind': 'identify-armed-mode', 'plant': plant,
            'dc': self.flora.dc(), 'modifier': self.modifier(acquired, 'INT', skill='Investigation'), 'rollMode': 'normal'})

    def declare_disarm(self, event, actor, plant, *, actual_tool, actual_in_reach):
        acquired, state = self.task_preflight(event, actor); p = self.flora.body(plant)
        if not p['armed'] or not actual_in_reach or actual_tool not in state.get('usableHeldThievesTools', []):
            raise ValueError('Actual accessible armed plant and usable held thieves tools required')
        return self.commit(event, actor, {'kind': 'disarm-armed-plant', 'plant': plant,
            'dc': self.flora.dc(), 'modifier': self.modifier(acquired, 'DEX', tool=actual_tool), 'rollMode': 'normal'})

    def resolve(self, event, faces):
        p = self.pending.get(event)
        if not p: raise ValueError('Actual pending paid task required')
        count = 1 if p['rollMode'] == 'normal' else 2
        if len(faces) != count or any(type(n) is not int or not 1 <= n <= 20 for n in faces):
            raise ValueError('Exact ordinary kept-die input required')
        if 'plant' in p:
            plant = self.flora.plants[p['plant']]
            if not plant['active'] or not plant['armed'] or self.flora.now >= plant['deadline']:
                return self.interrupt(event, actual_authorized_interruption=True, reason='original-armed-body-no-longer-present')
        natural = max(faces) if p['rollMode'] == 'higher' else min(faces) if p['rollMode'] == 'lower' else faces[0]
        result = {**task_check(natural, p['modifier'], p['dc']), 'keptNatural': natural}
        if p['kind'] == 'identify-armed-mode':
            if result['success']:
                mode = self.flora.plants[p['plant']]['mode']
                self.knowledge.setdefault(p['actor'], {})[p['plant']] = mode
                result['identifiedMode'] = mode
            else: result['identifiedMode'] = None
        elif p['kind'] == 'disarm-armed-plant':
            if result['success']: self.flora.plants[p['plant']]['armed'] = False
            result.update(disarmed=result['success'], automaticExplosion=False)
        self.events[event].update(status='resolved', result=deepcopy(result)); self.pending.pop(event)
        return result

    def interrupt(self, event, *, actual_authorized_interruption, reason='actual-authorized-interruption'):
        if event not in self.pending or not actual_authorized_interruption:
            raise ValueError('Actual paid task and authorized interruption required')
        self.events[event].update(status='interrupted-no-refund', reason=reason, result=None)
        self.pending.pop(event)
        return None

    def move_owner(self, event, distance, *, actual_endpoint, terrain, causes, current_speed, actual_legal_route,
                   crawling=False, squeezing=False, actual_hazards=()):
        if event in self.movements or event in self.events or event in self.flora.events:
            raise ValueError('Actual movement identity cannot be replayed')
        if (not actual_legal_route or not self.flora.world['actors']['owner']['canAct']
                or type(current_speed) is not int or current_speed <= 0):
            raise ValueError('Actual route, moving actor and nonzero current Speed required')
        if not isinstance(causes, list) or not causes:
            raise ValueError('Actual terrain causes required')
        if (type(actual_endpoint) is not int or type(distance) is not int
                or abs(actual_endpoint - self.flora.position('owner')) != distance):
            raise ValueError('Actual contiguous one-axis route distance and endpoint required')
        acquired = self.flora.acquired
        active_flora = self.flora.operative and any(p['active'] and self.flora.now < p['deadline']
            and not p['suppressed'] for p in self.flora.plants.values())
        benefit = (acquired.pay.has('verdant_bond') and 'verdant_bond' not in acquired.pay.suppressed
            and active_flora and terrain == 'difficult' and set(causes) == {'nonmagical-plants'})
        effective = 'normal' if benefit else terrain
        cost = movement_cost(distance, effective, crawling=crawling, squeezing=squeezing)
        self.movement.spend(cost, current_speed)
        self.flora.world['actors']['owner']['position'] = actual_endpoint
        record = {'distance': distance, 'originalTerrain': terrain, 'effectiveTerrain': effective,
            'cost': cost, 'spentTotal': self.movement.spent, 'verdantDiscount': benefit,
            'remainingMovement': self.movement.remaining(current_speed), 'actualEndpoint': actual_endpoint,
            'hazardsStillRequireOrdinaryResolution': list(actual_hazards), 'hazardsNegated': False}
        self.movements[event] = deepcopy(record)
        return record
