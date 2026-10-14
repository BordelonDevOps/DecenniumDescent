"""Contraption Crafter transactions in an explicit conditional object scene.

The ancestry and paid opportunity are source-derived. Physical supply, access,
turn, hearing, edge and custody records are fixture facts, not campaign proof.
Elapsed clocks use seconds. Geometry is a bounded unobstructed line.
"""
from copy import deepcopy

SID = 'contraption_crafter'


class GadgetUse:
    def __init__(self, lineage, profiles, world):
        self.lineage = lineage
        self.profiles = {x['die']: deepcopy(x) for x in profiles}
        if set(self.profiles) != {1, 2, 3, 4}:
            raise ValueError('Four source profiles are required')
        self.world = deepcopy(world)
        self.now = 0; self.next_start = None; self.work = None; self.active = None
        self.objects = {}; self.events = []; self.constructions = 0

    def snapshot(self):
        return {'lineageHistory': self.lineage.snapshot(), 'world': deepcopy(self.world),
                'now': self.now, 'nextConstructionAt': self.next_start, 'work': deepcopy(self.work),
                'activeObject': self.active, 'objects': deepcopy(self.objects),
                'events': deepcopy(self.events), 'constructionCount': self.constructions}

    def acquire(self, opportunity):
        result = self.lineage.pay.commit(SID, opportunity,
            prerequisites_met=self.lineage.prerequisite(SID))
        # Ownership gives permission and an initially unused elapsed-time allowance.
        # It supplies no tools, parts, proficiency, gadget, class device or reserve.
        self.events.append({'type': 'paid-acquisition', 'payment': result})

    def advance(self, when):
        if type(when) is not int or when < self.now:
            raise ValueError('Monotonic elapsed seconds required')
        if self.work and when > self.work['completeAt']:
            raise ValueError('Resolve the scheduled construction milestone before later events')
        self.now = when
        for gadget in self.objects.values():
            if gadget['active'] and when >= gadget['expiresAt']:
                self.end(gadget, 'expired', at=gadget['expiresAt'])

    def reachable(self, actor, position):
        return abs(self.world['actors'][actor]['position'] - position) <= 5

    def usable_tool(self, identity):
        tool = self.world['tools'].get(identity)
        return bool(tool and tool['kind'] == 'tinkers-tools' and tool['usable'] and
                    'maker' in tool['accessibleTo'] and self.reachable('maker', tool['position']))

    def start(self, tool_id, parts_id):
        maker = self.world['actors']['maker']; parts = self.world['parts'].get(parts_id)
        if not self.lineage.pay.has(SID) or SID in self.lineage.pay.suppressed or not maker['canWork']:
            raise ValueError('Actual operative feat and an able constructor are required')
        if self.work or (self.next_start is not None and self.now < self.next_start):
            raise ValueError('Construction already underway or 24 elapsed hours have not passed')
        if not self.usable_tool(tool_id): raise ValueError('Actual accessible usable tinkers tools required')
        if not parts or parts['owner'] != 'maker' or not parts['suitableMundaneParts'] or \
                parts['creditedCopper'] < 500 or not self.reachable('maker', parts['position']):
            raise ValueError('Five gp of suitable owned accessible parts required; coins are not parts')
        parts['creditedCopper'] -= 500
        self.next_start = self.now + 86400
        if self.active is not None: self.end(self.objects[self.active], 'new-legal-construction')
        self.constructions += 1
        self.work = {'id': 'construction-' + str(self.constructions), 'startedAt': self.now,
                     'completeAt': self.now + 600, 'tool': tool_id, 'parts': parts_id, 'spentCopper': 500}
        self.events.append({'type': 'construction-started-costs-committed', **deepcopy(self.work)})

    def interrupt(self, reason):
        if not self.work: raise ValueError('No construction underway')
        self.events.append({'type': 'construction-interrupted', 'at': self.now,
                            'work': deepcopy(self.work), 'reason': reason, 'refundCopper': 0})
        self.work = None

    def complete(self, face, placement):
        if not self.work or self.now != self.work['completeAt']:
            raise ValueError('Complete the full uninterrupted ten-minute milestone')
        if type(face) is not int or face not in self.profiles:
            raise ValueError('An openly supplied d4 face is required; no choice or reroll')
        if not self.world['actors']['maker']['canWork'] or not self.usable_tool(self.work['tool']):
            raise ValueError('The supplied ongoing work/access record is no longer valid')
        if not self.reachable('maker', placement) or placement not in self.world['legalObjectSpaces']:
            raise ValueError('A reachable legal placement is required')
        identity = self.work['id'] + '-object'
        gadget = {'id': identity, 'profile': self.profiles[face]['id'], 'd4': face,
                  'size': 'Tiny', 'weightLb': 1, 'armorClass': 10, 'maximumHP': 1, 'hp': 1,
                  'completedAt': self.now, 'expiresAt': self.now + 3600,
                  'active': True, 'owner': 'maker', 'holder': None, 'position': placement,
                  'lit': False, 'armedThread': None, 'clampedObject': None, 'fan': None,
                  'creditedReclaimCopper': 0, 'creatureTurn': False}
        self.objects[identity] = gadget; self.active = identity
        self.events.append({'type': 'construction-completed-d4', 'work': deepcopy(self.work),
                            'face': face, 'object': identity})
        self.work = None
        return identity

    def get_live(self, identity):
        obj = self.objects.get(identity)
        if not obj or not obj['active'] or self.now >= obj['expiresAt']:
            raise ValueError('No live gadget at this clock')
        return obj

    def object_position(self, gadget):
        return self.world['actors'][gadget['holder']]['position'] if gadget['holder'] else gadget['position']

    def pay_action(self, user, gadget):
        actor = self.world['actors'][user]
        if self.world['activeActor'] != user or not actor['canAct'] or actor['actions'] < 1 or \
                not self.reachable(user, self.object_position(gadget)):
            raise ValueError('One actual usable Action and reachable object required')
        actor['actions'] -= 1

    def regular_start(self, user, serial):
        actor = self.world['actors'][user]
        if type(serial) is not int or serial <= actor['regularSerial']:
            raise ValueError('A later actual regular-turn receipt is required')
        actor['regularSerial'] = serial; actor['actions'] = 1; actor['interactions'] = 1
        self.world['activeActor'] = user
        for obj in self.objects.values():
            if obj['fan'] and obj['fan']['user'] == user and serial >= obj['fan']['endAtRegularStart']:
                obj['fan'] = None

    def extra_turn(self, user):
        # An explicitly supplied extra turn grants its own ordinary Action but
        # does not advance a deadline tied to the next regular turn.
        self.world['activeActor'] = user; self.world['actors'][user]['actions'] = 1
        self.world['actors'][user]['interactions'] = 1

    def transfer(self, identity, giver, receiver):
        gadget = self.get_live(identity); source = self.world['actors'][giver]; target = self.world['actors'][receiver]
        if gadget['owner'] != giver or gadget['holder'] not in {None, giver} or gadget['armedThread'] or gadget['clampedObject']:
            raise ValueError('An unattached actual object in the giver custody is required')
        if self.world['activeActor'] != giver or source['interactions'] < 1 or not source['canAct'] or \
                not target['willingToReceive'] or not self.reachable(giver, self.object_position(gadget)) or \
                not self.reachable(giver, target['position']) or target['freeHands'] < 1:
            raise ValueError('A lawful reachable handoff, ordinary interaction and receiving hand required')
        source['interactions'] -= 1
        if gadget['holder'] == giver: source['freeHands'] += 1
        target['freeHands'] -= 1
        gadget.update(owner=receiver, holder=receiver, position=target['position'])
        self.events.append({'type': 'same-object-handoff', 'id': identity, 'from': giver, 'to': receiver,
                            'expiresAt': gadget['expiresAt']})

    def lamp(self, identity, user, lit):
        gadget = self.get_live(identity)
        if gadget['d4'] != 1 or type(lit) is not bool: raise ValueError('Only the shaded lamp has this operation')
        self.pay_action(user, gadget); gadget['lit'] = lit
        return {'brightFeet': 10 if lit else 0, 'additionalDimFeet': 10 if lit else 0,
                'penetratesMagicalDarkness': False, 'fuelGranted': 0, 'ignitesOtherObjects': False}

    def arm_bell(self, identity, user, passage_id):
        gadget = self.get_live(identity); passage = self.world['passages'].get(passage_id)
        if gadget['d4'] != 2 or gadget['armedThread'] or not passage or not passage['ground'] or \
                passage['widthFeet'] > 5 or not self.reachable(user, passage['position']):
            raise ValueError('A reachable ground passage within the integral five-foot thread is required')
        self.pay_action(user, gadget)
        if gadget['holder']: self.world['actors'][gadget['holder']]['freeHands'] += 1
        gadget.update(holder=None, position=passage['position'], armedThread=passage_id)
        return {'threadFeet': 5, 'loadBearing': False, 'automaticHiddenDC': None}

    def cross_bell(self, identity, body_id, passage_id, physical_contact):
        gadget = self.get_live(identity)
        if gadget['d4'] != 2 or gadget['armedThread'] is None: raise ValueError('No armed line bell')
        body = self.world['bodies'].get(body_id)
        if not body: raise ValueError('An actual supplied body is required')
        if gadget['armedThread'] != passage_id or not physical_contact or not body['corporeal']:
            return {'rang': False}
        result = {'rang': True, 'audibleFeet': 30,
                  'heardBy': [key for key, actor in self.world['actors'].items()
                              if actor['canHear'] and abs(actor['position']-gadget['position']) <= 30],
                  'revealsIdentity': False, 'damage': 0, 'restrains': False, 'trips': False}
        self.events.append({'type': 'line-bell-rang', 'object': identity, 'at': self.now})
        self.end(gadget, 'thread-released-spent')
        return result

    def clamp(self, identity, user, edge_id, object_id):
        gadget = self.get_live(identity); edge = self.world['edges'].get(edge_id); obj = self.world['cargo'].get(object_id)
        if gadget['d4'] != 3 or gadget['clampedObject'] or not edge or not edge['mundane'] or \
                not 0 < edge['thicknessInches'] <= 2 or not self.reachable(user, edge['position']) or \
                not obj or not 0 <= obj['weightLb'] <= 5 or obj['creature'] or \
                not (obj['unattended'] or obj['willinglyPresented']) or not self.reachable(user, obj['position']):
            raise ValueError('Reachable mundane edge <=2in and one unattended/willing object <=5lb required')
        self.pay_action(user, gadget)
        if gadget['holder']: self.world['actors'][gadget['holder']]['freeHands'] += 1
        gadget.update(holder=None, position=edge['position'], clampedObject=object_id)
        obj.update(attachedTo=identity, position=edge['position'])
        return {'supportsClimber': False, 'barsDoor': False, 'restrains': False, 'checkBonus': 0, 'extraHands': 0}

    def unclamp(self, identity, user):
        gadget = self.get_live(identity)
        if gadget['d4'] != 3 or not gadget['clampedObject']: raise ValueError('No attached light clamp')
        self.pay_action(user, gadget); self.release_cargo(gadget, 'removed')

    def fan(self, identity, user):
        gadget = self.get_live(identity)
        if gadget['d4'] != 4 or gadget['holder'] != user: raise ValueError('The actual fan must be held')
        self.pay_action(user, gadget)
        gadget['fan'] = {'user': user, 'endAtRegularStart': self.world['actors'][user]['regularSerial'] + 1,
                         'coneFeet': 5, 'ordinaryAirOnly': True}
        return {'coneFeet': 5, 'comfortCooling': True, 'stirsLoosePaperDust': True,
                'damage': 0, 'creatureMovement': 0, 'removesRulesGas': False,
                'suffocationRelief': False, 'hazardImmunity': False, 'identifiesSubstance': False}

    def release_cargo(self, gadget, reason):
        if gadget['clampedObject']:
            obj = self.world['cargo'][gadget['clampedObject']]
            obj['attachedTo'] = None
            # Ordinary falling is explicitly delegated, never converted into a
            # gadget damage or attack. The fixture retains that pending event.
            self.events.append({'type': 'ordinary-object-fall-required', 'object': gadget['clampedObject'],
                                'position': obj['position'], 'reason': reason})
            gadget['clampedObject'] = None

    def end(self, gadget, reason, at=None):
        if not gadget['active']: return
        self.release_cargo(gadget, reason)
        gadget.update(active=False, lit=False, armedThread=None, fan=None, creditedReclaimCopper=0)
        if self.active == gadget['id']: self.active = None
        self.events.append({'type': 'gadget-inert', 'object': gadget['id'],
                            'reason': reason, 'at': self.now if at is None else at, 'refundedCopper': 0})

    def damage(self, identity, resolved_damage):
        gadget = self.get_live(identity)
        if type(resolved_damage) is not int or resolved_damage < 0:
            raise ValueError('Already resolved nonnegative ordinary object damage required')
        gadget['hp'] = max(0, gadget['hp']-resolved_damage)
        if gadget['hp'] == 0: self.end(gadget, 'destroyed')

    def dismantle(self, identity, user):
        # Only the already-authorized physical dismantling result is represented.
        # This function invents no feat-specific dismantling action/time rule.
        gadget = self.get_live(identity)
        if gadget['owner'] != user or not self.reachable(user, self.object_position(gadget)):
            raise ValueError('Actual owner access required for this dismantling witness')
        self.end(gadget, 'conditionally-authorized-dismantling')
