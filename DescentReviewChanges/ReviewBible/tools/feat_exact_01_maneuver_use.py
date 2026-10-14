"""Six feat maneuvers in an explicit, conditional one-dimensional encounter.

Paid feat history is source-derived. Body, custody, obstacle, fear and incoming
damage records belong to the stated test world, not an authenticated campaign.
Core roll/movement helpers retain their own scope. This is not a CRPG engine.
"""
from copy import deepcopy
from core_playtest_rules import attack_roll, opposed_check, task_check
from combat_playtest_rules import movement_cost, ReactionClock
from feat_exact_01_acquisition_models import pb

PREFIX = 'feat-maneuver.'
KINDS = {'measured-strike', 'driving-shove', 'disarming-feint',
         'guarding-deflection', 'measured-advance', 'rallying-signal'}


class ManeuverUse:
    def __init__(self, acquired, world):
        self.acquired = acquired
        if not acquired.pay.has('martialAdept') or 'feat_superiority' not in acquired.initializations:
            raise ValueError('An actual paid Martial Adept history and its pool are required')
        self.world = deepcopy(world); self.actor = self.world['actors']['owner']
        self.reaction = ReactionClock(available=self.actor.pop('reactionAvailable'))
        self.actions = 1; self.bonus_actions = 1; self.attack_slots = 0
        self.own_turn = True; self.regular_turn = True; self.operative = True
        self.events = {}; self.log = []; self.pending_movement = None

    @property
    def pool(self):
        return self.acquired.initializations['feat_superiority']

    def snapshot(self):
        return {'acquisition': self.acquired.snapshot(), 'world': deepcopy(self.world),
                'reaction': deepcopy(self.reaction.__dict__), 'actions': self.actions,
                'bonusActions': self.bonus_actions, 'attackSlots': self.attack_slots,
                'ownTurn': self.own_turn, 'regularTurn': self.regular_turn,
                'operative': self.operative, 'events': deepcopy(self.events),
                'log': deepcopy(self.log), 'pendingMovement': self.pending_movement}

    def begin_attack_action(self):
        if not self.own_turn or not self.actor['canAct'] or self.actions < 1 or self.attack_slots:
            raise ValueError('No legal ordinary Attack Action')
        # This witness uses the ordinary one-attack grant. It models no class
        # Extra Attack, Ready release or independently granted additional Action.
        self.actions -= 1; self.attack_slots = 1
        self.log.append({'event': 'ordinary-Attack-Action', 'actionSpent': 1, 'legalAttackSlots': 1})

    def modifier(self, ability, proficiency=False):
        return (self.acquired.pay.scores[ability]-10)//2 + (
            pb(sum(self.acquired.pay.current_classes.values())) if proficiency else 0)

    def athletics_modifier(self):
        factor = self.acquired.training_projection['skills'].get('Athletics', 0)
        return self.modifier('STR') + factor * pb(sum(self.acquired.pay.current_classes.values()))

    def reachable(self, target, reach=5):
        return abs(target['position']-self.actor['position']) <= reach and not any(
            min(target['position'], self.actor['position']) < wall < max(target['position'], self.actor['position'])
            for wall in self.world['walls'])

    def target(self, identity):
        if identity not in self.world['actors']:
            raise ValueError('An actual target in this fixture is required')
        return self.world['actors'][identity]

    def declare(self, identity, event_id, *, target=None, mode=None, item=None, style=None, fear=None, packet=None):
        kind = identity.removeprefix(PREFIX)
        if identity != PREFIX + kind or kind not in KINDS or identity not in self.pool['maneuvers']:
            raise ValueError('Maneuver must be one of the actual permanently acquired identities')
        if not self.operative or not self.actor['canAct'] or self.pool['current'] < 1:
            raise ValueError('Maneuver unavailable or superiority pool exhausted')
        if event_id in self.events or self.pending_movement is not None:
            raise ValueError('No duplicate underlying event or banked/interleaved special movement')
        context = {'target': target, 'mode': mode, 'item': item, 'style': style, 'fear': fear}
        action_cost = bonus_cost = attack_cost = reaction_cost = 0
        if kind in {'measured-strike', 'driving-shove', 'disarming-feint'}:
            if self.attack_slots < 1:
                raise ValueError('A real available Attack Action attack is required in this witness')
            victim = self.target(target)
            if not self.reachable(victim): raise ValueError('Target is beyond actual reach or obstructed')
            attack_cost = 1
            if kind == 'measured-strike':
                weapon = self.world['items'].get(item)
                if not weapon or weapon['heldBy'] != 'owner' or weapon['profile'] != 'martial-melee-weapons.longsword':
                    raise ValueError('This witness needs its actual held longsword profile')
                context['attackModifier'] = self.modifier('STR', weapon['profile'] in self.acquired.training_projection['weapons'])
                context['armorClass'] = victim['armorClass']
            elif kind == 'driving-shove':
                if victim['size'] > self.actor['size']+1 or mode not in {'push', 'prone'}:
                    raise ValueError('Ordinary Shove size cap and one declared outcome apply')
                context['actorModifier'] = self.athletics_modifier()
            else:
                held = self.world['items'].get(item)
                if not held or held['heldBy'] != target or not held['droppable']:
                    raise ValueError('A reachable actually held droppable object is required')
                if style not in {'Athletics', 'weapon-check'}:
                    raise ValueError('Not an ordinary opposed Disarm; save-based feat/Whip routes are separate')
                if style == 'weapon-check':
                    weapon = self.world['items'].get('owner-sword')
                    if not weapon or weapon['heldBy'] != 'owner': raise ValueError('No actual checking weapon')
                    context['actorModifier'] = self.modifier('STR', weapon['profile'] in self.acquired.training_projection['weapons'])
                else: context['actorModifier'] = self.athletics_modifier()
        elif kind == 'guarding-deflection':
            if not self.reaction.available or self.reaction.surprise_pending or not self.actor['canReact']:
                raise ValueError('Actual ordinary Reaction is unavailable')
            if not packet or packet['recipient'] != 'owner' or packet['stage'] != 'after-passive-before-tempHP' or \
                    packet['kind'] != 'direct-damage' or not packet['recipientMitigationAllowed']:
                raise ValueError('This packet cannot receive another mitigation step')
            if not packet['components'] or any(type(x['amount']) is not int or x['amount'] < 0 for x in packet['components']) or \
                    sum(x['amount'] for x in packet['components']) <= 0:
                raise ValueError('One genuinely pending positive damage event is required')
            context['packet'] = deepcopy(packet); reaction_cost = 1
        elif kind == 'measured-advance':
            if not self.own_turn or not self.regular_turn or self.bonus_actions < 1:
                raise ValueError('Requires a real BA on the own regular turn')
            if mode not in self.actor['modes'] or self.actor['modes'][mode] <= 0:
                raise ValueError('Choose an already available movement mode with nonzero Speed')
            bonus_cost = 1
        else:
            if not self.own_turn or self.actions < 1:
                raise ValueError('No ordinary Action available for this Rally witness')
            ally = self.target(target)
            chosen = next((r for r in ally['fear'] if r['id'] == fear), None)
            if not ally['ally'] or abs(ally['position']-self.actor['position']) > 30 or not ally['perceivesRally'] or \
                    not chosen or not chosen['active'] or chosen['condition'] != 'Frightened':
                raise ValueError('Choose one perceived in-range ally and one active actual Frightened record')
            context['sourceDC'] = chosen['sourceDC'] if chosen['sourceDC'] is not None else 10
            context['actorModifier'] = self.modifier('CHA'); action_cost = 1
        self.pool['current'] -= 1; self.actions -= action_cost; self.bonus_actions -= bonus_cost; self.attack_slots -= attack_cost
        if reaction_cost: self.reaction.spend()
        self.events[event_id] = {'identity': identity, 'kind': kind, 'context': context, 'status': 'committed-before-rolls',
            'cost': {'d6': 1, 'Action': action_cost, 'BA': bonus_cost, 'attack': attack_cost, 'Reaction': reaction_cost}}
        self.log.append({'event': event_id, 'stage': 'cost-committed-before-any-roll', 'poolRemaining': self.pool['current']})
        return deepcopy(self.events[event_id])

    def roll_die(self, event_id, face):
        event = self.events[event_id]
        if event['status'] != 'committed-before-rolls' or type(face) is not int or not 1 <= face <= 6:
            raise ValueError('One d6 can be rolled once after commitment')
        event['die'] = face; event['status'] = 'die-rolled'
        self.log.append({'event': event_id, 'stage': 'superiority-die-rolled', 'face': face})

    def interrupt(self, event_id):
        event = self.events[event_id]
        if event['status'] not in {'committed-before-rolls', 'die-rolled', 'moving'}:
            raise ValueError('No unresolved committed attempt to interrupt')
        if event['status'] == 'moving':
            event['discardedDistance'] = event['movementRemaining']
            event['movementRemaining'] = 0
        event['status'] = 'interrupted-costs-retained'
        if self.pending_movement == event_id: self.pending_movement = None
        self.log.append({'event': event_id, 'stage': 'interrupted', 'refunded': False})

    def resolve(self, event_id, actor_die=None, defender_die=None, defender_skill=None, drop=None):
        event = self.events[event_id]
        if event['status'] != 'die-rolled': raise ValueError('The committed attempt needs its one d6 first')
        kind, ctx, face = event['kind'], event['context'], event['die']
        if kind == 'measured-strike':
            result = attack_roll(actor_die, ctx['attackModifier'] + face, ctx['armorClass'])
            result.update(damageBonus=0, additionalAttackGranted=False)
        elif kind in {'driving-shove', 'disarming-feint'}:
            victim = self.target(ctx['target'])
            if defender_skill not in {'Athletics', 'Acrobatics'}: raise ValueError('Defender chooses one actual ordinary defense')
            result = opposed_check(actor_die, ctx['actorModifier'] + face, defender_die, victim['opposedModifiers'][defender_skill])
            if kind == 'disarming-feint' and result['changesState']:
                adjacent = [victim['position']-5, victim['position']+5]
                legal = [x for x in adjacent if x not in self.world['walls'] and x not in {a['position'] for a in self.world['actors'].values()}]
                required = legal if legal else [victim['position']]
                if drop not in required: raise ValueError('Choose a legal adjacent empty drop, otherwise the target own space')
            if result['changesState']:
                if kind == 'driving-shove':
                    if ctx['mode'] == 'prone': victim['prone'] = True
                    else:
                        direction = 1 if victim['position'] >= self.actor['position'] else -1
                        destination = victim['position'] + 5 * direction
                        if destination not in self.world['walls'] and destination not in {a['position'] for a in self.world['actors'].values()}:
                            victim['position'] = destination
                        result['ordinaryOpportunityAttackTriggered'] = False
                else:
                    held = self.world['items'][ctx['item']]
                    held['heldBy'] = None; held['position'] = drop
                    result['newCustodian'] = None
            result['damage'] = 0
        elif kind == 'guarding-deflection':
            packet = deepcopy(ctx['packet']); remaining_reduction = face
            for component in packet['components']:
                removed = min(component['amount'], remaining_reduction)
                component['amount'] -= removed; remaining_reduction -= removed
            result = {'packet': packet, 'prevented': face-remaining_reduction,
                      'riposteParryTrigger': False, 'damageAppliedToHP': False}
        elif kind == 'rallying-signal':
            result = task_check(actor_die, ctx['actorModifier'] + face, ctx['sourceDC'])
            if result['success']:
                next(x for x in self.target(ctx['target'])['fear'] if x['id'] == ctx['fear'])['active'] = False
            result.update(HPGranted=0, tempHPGranted=0, extraTurnGranted=False)
        else:
            event['movementRemaining'] = 5 * face; event['status'] = 'moving'; self.pending_movement = event_id
            result = {'separateMovementCostBudget': 5 * face, 'ordinaryMovementRefilled': False,
                      'newMovementModes': [], 'disengageGranted': False}
        if kind != 'measured-advance': event['status'] = 'resolved'
        event['result'] = deepcopy(result); self.log.append({'event': event_id, 'stage': event['status']})
        return deepcopy(result)

    def advance_step(self, event_id, destination, *, terrain='normal', crawling=False, squeezing=False,
                     opportunity_outcome=None):
        event = self.events[event_id]
        if self.pending_movement != event_id or event['status'] != 'moving': raise ValueError('No immediate movement budget')
        if not self.actor['canAct'] or self.actor['modes'][event['context']['mode']] <= 0:
            self.interrupt(event_id); return {'moved': False, 'interrupted': True}
        distance = abs(destination-self.actor['position'])
        if distance != 5 or destination in self.world['walls'] or destination in {a['position'] for k, a in self.world['actors'].items() if k != 'owner'}:
            raise ValueError('This fixture requires one traversable unoccupied five-foot step')
        cost = movement_cost(distance, terrain, crawling=crawling, squeezing=squeezing)
        if cost > event['movementRemaining']: raise ValueError('Insufficient separate movement-cost budget')
        provoking = [key for key, foe in self.world['actors'].items() if key != 'owner' and not foe['ally'] and
            foe.get('canSeeOwner', False) and foe.get('reactionAvailable', False) and
            abs(foe['position']-self.actor['position']) <= 5 < abs(foe['position']-destination) and not self.actor['disengaged']]
        if provoking:
            if opportunity_outcome is None:
                return {'moved': False, 'awaitingOpportunityResponseBeforeExit': provoking}
            if opportunity_outcome not in {'decline', 'conditional-interruption'}:
                raise ValueError('Only explicit declined or separately supplied interrupting OA outcomes are represented')
            if opportunity_outcome == 'conditional-interruption' and len(provoking) != 1:
                raise ValueError('This bounded witness accepts one interrupting foe; multiple reaction ordering is outside its scope')
            self.log.append({'event': event_id, 'stage': 'ordinary-opportunity-before-exit',
                             'foes': provoking, 'outcome': opportunity_outcome,
                             'opportunityAttackDamageNotExecuted': True})
            if opportunity_outcome == 'conditional-interruption':
                self.world['actors'][provoking[0]]['reactionAvailable'] = False
                self.actor['canAct'] = False; self.interrupt(event_id)
                return {'moved': False, 'interruptedBeforeExit': True}
        self.actor['position'] = destination; event['movementRemaining'] -= cost
        return {'moved': True, 'cost': cost, 'remaining': event['movementRemaining']}

    def finish_advance(self, event_id):
        event = self.events[event_id]
        if self.pending_movement != event_id or event['status'] != 'moving': raise ValueError('No live immediate movement')
        event['discardedDistance'] = event['movementRemaining']; event['movementRemaining'] = 0
        event['status'] = 'resolved'; self.pending_movement = None
