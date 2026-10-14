"""FLQ01–04 finite Flora descendant. Historical FloraUse remains unchanged.

Paid source records establish acquisition; clock, world, actual suppression and
phase authority are conditional fixture facts, not a campaign authenticator.
"""
from copy import deepcopy
from feat335_flora_use import FloraUse
from feat_exact_01_acquisition_models import pb


class FloraSourceFollowthrough(FloraUse):
    def __init__(self, acquired, world):
        super().__init__(acquired, world)
        grants = [g for g in acquired.pay.grants if g['identity'] == 'conjure_flora']
        route = self.initial.get('fixedCastingRoute')
        if (len(grants) != 1 or not isinstance(route, dict)
                or set(route) != {'grantId', 'ability', 'sourceClass'}
                or not route['grantId'] or not route['sourceClass']
                or route['ability'] not in {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}
                or grants[0]['choice'] != route
                or not acquired.pay.opportunities.get(grants[0]['opportunity'], {}).get('spent')):
            raise ValueError('Original paid provider/ability binding must be complete and unchanged')
        self.bound_route = deepcopy(route)
        self.pending = {}; self.closed_phases = {}; self.ended_regular_turns = set()
        self.turn_kinds = {}; self.window_closures = []

    def snapshot(self):
        return {**super().snapshot(), 'boundRoute': deepcopy(self.bound_route),
                'pending': deepcopy(self.pending), 'closedPhases': deepcopy(self.closed_phases),
                'endedRegularTurns': sorted(self.ended_regular_turns),
                'turnKinds': deepcopy(self.turn_kinds), 'windowClosures': deepcopy(self.window_closures)}

    def dc(self):
        if self.initial.get('fixedCastingRoute') != self.bound_route:
            raise ValueError('No later provider substitution')
        score = self.acquired.pay.scores.get(self.bound_route['ability'])
        if type(score) is not int:
            raise ValueError('Continuing lawful bound-ability operand required')
        return 8 + pb(sum(self.acquired.pay.current_classes.values())) + (score - 10) // 2

    def begin_turn(self, identity, round_id, now, **kwargs):
        super().begin_turn(identity, round_id, now, **kwargs)
        self.turn_kinds[identity] = self.regular

    def preflight(self, event, **kwargs):
        super().preflight(event, **kwargs)
        if self.world['actors']['owner'].get('dead', False):
            raise ValueError('Dead owner cannot take a new personal action')
        self.dc()  # Establish actual operands before any resource commitment.

    def create(self, event, identity, mode, position, deadline, *, armed=False, additional=False):
        self.preflight(event, action=True)
        if identity in self.plants or mode not in self.profiles:
            raise ValueError('New body identity and exact fixed mode required')
        if type(deadline) is not int or not self.now < deadline <= self.now + 60:
            raise ValueError('Actual original source-start minute deadline required')
        if (self.distance(self.position('owner'), position) > 30
                or not self.line(self.position('owner'), position)
                or position not in self.world['supportedVisibleGround']):
            raise ValueError('Visible supported ground within30 and line of effect required')
        if armed and not self.acquired.pay.has('trapcasting'):
            raise ValueError('Actual separately acquired Trapcasting required')
        total = sum(self.acquired.pay.current_classes.values())
        if sum(p['active'] for p in self.plants.values()) >= (2 if total >= 10 else 1):
            raise ValueError('Actual body capacity exhausted')
        if additional:
            if (total < 10 or not self.second or self.now >= self.second['deadline']
                    or self.second['use'] in self.consumed_second
                    or not self.plants[self.second['first']]['active']):
                raise ValueError('No current additional-creation entitlement')
            use = self.second['use']
        else:
            if self.initial['creationUses']['current'] < 1:
                raise ValueError('Creation rest use already spent')
            use = event
        current_pb = pb(total)
        self.actions -= 1; self.events.add(event)
        if additional:
            self.close_window('additional-creation-spent')
        else:
            self.initial['creationUses']['current'] -= 1
            self.second = {'use': event, 'first': identity, 'deadline': deadline}
        self.plants[identity] = {'id': identity, 'owner': 'owner', 'mode': mode,
            'burstType': self.profiles[mode]['burstType'], 'position': position,
            'created': self.now, 'deadline': deadline, 'active': True, 'endReason': None,
            'maximumHP': 5 + current_pb, 'hp': 5 + current_pb, 'saveBonus': current_pb,
            'ac': 12, 'armed': armed, 'creationUse': use, 'noLootOrResourceOutputs': True,
            'suppressed': False, 'canAct': True, 'deafened': False, 'blind': False,
            'perceivesTargets': True}
        self.sync()
        self.history.append({'event': event, 'kind': 'additional-creation' if additional else 'creation',
                             'body': identity, 'actionSpent': 1, 'restUseSpent': not additional})
        return deepcopy(self.plants[identity])

    def close_window(self, reason):
        if self.second:
            self.window_closures.append({**deepcopy(self.second), 'closedAt': self.now, 'reason': reason})
            self.consumed_second.add(self.second['use']); self.second = None
            self.sync()

    def end(self, identity, reason):
        ended = super().end(identity, reason)
        if ended:
            self.plants[identity]['endedAt'] = self.now
            if self.second and self.second['first'] == identity:
                self.close_window(reason)
        return ended

    def capable(self, plant):
        return (self.operative and plant['active'] and self.now < plant['deadline']
                and not plant['suppressed'] and plant['canAct'])

    def channel(self, plant):
        owner = self.world['actors']['owner']
        return self.distance(owner['position'], plant['position']) <= 60 and (
            (owner['spokenCommand'] and not owner['silenced'] and not plant['deafened'])
            or (owner['visibleCommand'] and not plant['blind']
                and self.line(owner['position'], plant['position'])))

    def legal_origins(self, participants, mode, target, area):
        plants = [self.plants[p] for p in participants if self.capable(self.plants[p])]
        if mode in {'lash', 'spore'}:
            if target not in self.world['actors'] or not self.world['actors'][target].get('legalTarget', True):
                return []
            return [p for p in plants if p['perceivesTargets']
                    and self.distance(p['position'], self.position(target)) <= 10
                    and self.line(p['position'], self.position(target))]
        square = self.world['areas'].get(area)
        if not square or not square['supported']:
            return []
        return [p for p in plants if p['perceivesTargets']
                and self.distance(p['position'], square['origin']) <= 10
                and self.line(p['position'], square['origin'])]

    def command(self, *args, **kwargs):
        raise ValueError('Use separate declare_command and resolve_attached interfaces')

    def declare_command(self, event, participants, mode, *, target=None, area=None):
        self.preflight(event, bonus=True); self.offense_free()
        if not self.regular or self.turn in self.phases or self.turn in self.ended_regular_turns:
            raise ValueError('One command on the actual unfinished owner regular turn required')
        if not participants or len(set(participants)) != len(participants):
            raise ValueError('Distinct participating plants required')
        plants = [self.body(p) for p in participants]
        if any(not self.capable(p) or not self.channel(p) for p in plants):
            raise ValueError('Each capable plant must actually receive the command')
        if mode not in self.profiles:
            raise ValueError('Exact selected mode required')
        if mode != 'lash' and (len(plants) != 1 or plants[0]['mode'] != mode):
            raise ValueError('Single original selected-mode origin required')
        if (mode == 'entangle' and target is not None) or (mode != 'entangle' and area is not None):
            raise ValueError('One mode-specific target or area, no replacement choices')
        if not self.legal_origins(participants, mode, target, area):
            raise ValueError('Actual legal nominated origin and target or area required')
        self.bonus_actions -= 1; self.offense.add(self.round); self.phases.add(self.turn); self.events.add(event)
        value = {'event': event, 'owner': 'owner', 'regularTurn': self.turn, 'round': self.round,
                 'participants': list(participants), 'mode': mode, 'target': target, 'area': area,
                 'paidBonusAction': 1, 'paidOffense': 1, 'status': 'pending'}
        self.pending[event] = deepcopy(value)
        self.history.append({'kind': 'received-paid-command', **deepcopy(value)})
        return value

    def end_regular_turn(self, identity, *, actual_end_processing_complete):
        if (not actual_end_processing_complete or not self.turn_kinds.get(identity)
                or identity in self.ended_regular_turns):
            raise ValueError('Actual original regular-turn end processing required')
        self.ended_regular_turns.add(identity)
        if self.turn == identity:
            self.actions = 0; self.bonus_actions = 0

    def close_command(self, event, reason, outcomes):
        value = self.pending.pop(event)
        self.closed_phases[event] = {**value, 'status': reason, 'closedAt': self.now,
                                     'outcomes': deepcopy(outcomes)}
        self.history.append({'kind': 'original-attached-phase-closed', **deepcopy(self.closed_phases[event])})
        return outcomes

    def resolve_attached(self, event, *, actual_phase_turn, rolls=None, die=None, deadlines=None):
        value = self.pending.get(event)
        if (not value or actual_phase_turn != value['regularTurn']
                or actual_phase_turn not in self.ended_regular_turns):
            raise ValueError('Only the original pending post-regular-turn phase may resolve')
        origins = self.legal_origins(value['participants'], value['mode'], value['target'], value['area'])
        if not origins:
            return self.close_command(event, 'no-longer-legal-no-refund', [])
        targets = (list(self.world['areas'][value['area']]['creatures'])
                   if value['mode'] == 'entangle' else [value['target']])
        rolls = {} if rolls is None else rolls; deadlines = deadlines or {}
        if not targets:
            if rolls:
                raise ValueError('No phantom occupants or rolls')
            return self.close_command(event, 'resolved-empty-area', [])
        self.check_resolution_inputs(value['mode'], targets, rolls, die, deadlines)
        self.dc()
        outcomes = self.resolve(origins[0]['id'], value['mode'], targets, rolls, die=die, deadlines=deadlines)
        return self.close_command(event, 'resolved-once', outcomes)

    def miss_attached(self, event, *, actual_phase_turn, actual_missed_phase):
        value = self.pending.get(event)
        if (not actual_missed_phase or not value or value['regularTurn'] != actual_phase_turn
                or actual_phase_turn not in self.ended_regular_turns):
            raise ValueError('Actual missed original phase required')
        return self.close_command(event, 'missed-no-backlog-no-refund', [])

    def cancel_command(self, event, *, actual_cancelling_effect):
        if not actual_cancelling_effect or event not in self.pending:
            raise ValueError('Independently authorized actual cancellation required')
        return self.close_command(event, 'expressly-cancelled-no-refund', [])

    def enter(self, event, plant, target, roll, **kwargs):
        p = self.body(plant)
        if not self.capable(p):
            return []
        self.dc()
        return super().enter(event, plant, target, roll, **kwargs)

    def burst(self, event, plant, targets, rolls, dice):
        if not self.capable(self.body(plant)):
            raise ValueError('Operative burst body required')
        return super().burst(event, plant, targets, rolls, dice)

    def verdant_spell_bonus(self, route, *, actual_legal_cast, copied=False):
        """Only the finite source predicate; no full spell casting is executed."""
        return int(actual_legal_cast and not copied and self.acquired.pay.has('verdant_bond')
            and 'verdant_bond' not in self.acquired.pay.suppressed
            and any(self.capable(p) for p in self.plants.values())
            and route in self.acquired.casting.qualifying()
            and route.get('sourceClass') in {'Druid', 'Ranger', 'Shaman'})
