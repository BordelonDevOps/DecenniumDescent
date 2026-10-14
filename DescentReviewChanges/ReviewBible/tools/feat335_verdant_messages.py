"""Finite paid Verdant message lifecycle with actual world/elapsed-time premises.

This executes only the stored-message and bounded plant-communication clauses.
Rooted stands, reach, ordinary communication, completed active work, beneficial
rest and actual future passages are conditional facts, not generated entities.
"""
from copy import deepcopy


class VerdantMessages:
    def __init__(self, acquired, world):
        if not acquired.pay.has('verdant_bond') or 'verdant_bond' not in acquired.initializations:
            raise ValueError('Complete actual paid Verdant Bond grant required')
        self.acquired = acquired; self.world = deepcopy(world)
        self.now = 0; self.pending = None; self.records = {}; self.events = set(); self.history = []
        self.rests = set(); self.operative = True

    @property
    def allowance(self): return self.acquired.initializations['verdant_bond']['messageUses']

    def snapshot(self):
        return {'acquisition': self.acquired.snapshot(), 'world': deepcopy(self.world), 'now': self.now,
            'pending': deepcopy(self.pending), 'records': deepcopy(self.records), 'events': sorted(self.events),
            'history': deepcopy(self.history), 'rests': sorted(self.rests), 'operative': self.operative}

    def advance(self, now):
        if type(now) is not int or now < self.now:
            raise ValueError('Actual monotonic elapsed time required')
        self.now = now
        for message in self.records.values():
            if message['active'] and now >= message['deadline']:
                message.update(active=False, endReason='original24-hour-expiry', endedAt=message['deadline'])

    def stand(self, identity):
        stand = self.world['stands'].get(identity)
        if not stand or not stand['rooted'] or not stand['alive']:
            raise ValueError('An actual surviving rooted plant stand is required')
        return stand

    def in_reach(self, stand):
        owner = self.world['owner']
        return abs(owner['position'] - stand['position']) <= owner['actualReach'] and stand['reachable']

    def start(self, event, stand_id, message, recipient):
        if event in self.events or self.pending or not self.operative or not self.world['owner']['canAct']:
            raise ValueError('A new lawful personal recording attempt required')
        if self.allowance['current'] < 1:
            raise ValueError('Actual Long-Rest message allowance is spent')
        stand = self.stand(stand_id)
        if not self.in_reach(stand) or not self.world['owner']['actualRecordingCommunication']:
            raise ValueError('Actual reach and ordinary recording communication required')
        if not isinstance(message, str) or not 1 <= len(message.split()) <= 25:
            raise ValueError('One actual brief message of at most25 ordinary words required')
        if recipient not in self.world['knownAllyIds']:
            raise ValueError('One designated actual known ally identity required')
        self.allowance['current'] -= 1; self.events.add(event)
        self.pending = {'event': event, 'owner': 'owner', 'stand': stand_id,
                        'message': message, 'recipient': recipient, 'started': self.now, 'usePaid': 1}
        self.history.append({'kind': 'recording-start', **deepcopy(self.pending)})
        return deepcopy(self.pending)

    def interrupt(self, *, actual_interruption):
        if not self.pending or not actual_interruption:
            raise ValueError('Actual pending work and interruption required')
        self.history.append({'kind': 'recording-interrupted-no-refund', 'endedAt': self.now, **deepcopy(self.pending)})
        self.pending = None

    def complete(self, now, *, actual_uninterrupted_active_work):
        if not self.pending or type(now) is not int or now < self.pending['started'] + 60 or now < self.now:
            raise ValueError('A complete actual uninterrupted active minute is required')
        stand = self.stand(self.pending['stand'])
        if (not actual_uninterrupted_active_work or not self.operative
                or not self.world['owner']['canAct'] or not self.in_reach(stand)
                or not self.world['owner']['actualRecordingCommunication']):
            raise ValueError('Work was not continuously legal; record its real interruption without refund')
        self.advance(now)
        record = {**deepcopy(self.pending), 'recordedAt': now, 'deadline': now + 86400,
                  'active': True, 'endReason': None}
        self.records[record['event']] = record; self.pending = None
        self.history.append({'kind': 'message-recorded-no-immediate-trigger', **deepcopy(record)})
        return deepcopy(record)

    def passage(self, event, *, actor, stand_id, now, actual_future_passage, within_ten_feet, actual_hearers):
        if event in self.events:
            raise ValueError('Actual passage event cannot be replayed')
        if actor not in self.world['actors'] or any(h not in self.world['actors'] for h in actual_hearers):
            raise ValueError('Real passage actor and ordinary hearers required')
        if not isinstance(actual_future_passage, bool) or not isinstance(within_ten_feet, bool):
            raise ValueError('Actual movement/geometry predicates required')
        self.stand(stand_id); self.advance(now); self.events.add(event)
        deliveries = []
        for message in self.records.values():
            if (message['active'] and message['stand'] == stand_id and message['recipient'] == actor
                    and now > message['recordedAt'] and actual_future_passage and within_ten_feet):
                message.update(active=False, endReason='first-future-designated-passage', endedAt=now)
                deliveries.append({'record': message['event'], 'audibleMessage': message['message'],
                    'actualHearers': list(actual_hearers), 'recipient': actor,
                    'privateTelepathy': False, 'remoteConfirmation': False})
        self.history.append({'kind': 'actual-passage', 'event': event, 'actor': actor,
                             'stand': stand_id, 'at': now, 'deliveries': deepcopy(deliveries)})
        return deliveries

    def destroy_stand(self, identity, now):
        stand = self.stand(identity); self.advance(now); stand['alive'] = False
        for message in self.records.values():
            if message['active'] and message['stand'] == identity:
                message.update(active=False, endReason='stand-destroyed', endedAt=now)
        if self.pending and self.pending['stand'] == identity:
            self.interrupt(actual_interruption=True)
        self.history.append({'kind': 'actual-stand-destroyed', 'stand': identity, 'at': now})

    def rest(self, identity, *, kind, beneficial):
        if self.pending:
            raise ValueError('Active recording work cannot be silently carried through a rest')
        if kind not in {'SR', 'LR'}:
            raise ValueError('Actual completed rest type required')
        if identity in self.rests or not beneficial or kind != 'LR': return False
        self.rests.add(identity); self.allowance['current'] = self.allowance['maximum']
        return True

    def communicate(self, stand_id, *, actual_brief_simple_ideas, actual_coarse_reply):
        if not self.operative or not self.world['owner']['conscious']:
            raise ValueError('Conscious operative owner required')
        stand = self.stand(stand_id)
        if (abs(self.world['owner']['position'] - stand['position']) > 60
                or not stand['perceived'] or not stand['lineOfEffect']
                or not actual_brief_simple_ideas or not self.world['owner']['actualOrdinaryCommunication']):
            raise ValueError('Actual perceived plant within60/LoE and ordinary simple communication required')
        if actual_coarse_reply not in {None, 'fear', 'hunger', 'dormancy'}:
            raise ValueError('Only actual coarse current response; no history, identity, vision or compulsion')
        return {'reply': actual_coarse_reply, 'newIntelligence': False, 'historyExtracted': False,
                'compelled': False, 'remoteKnowledge': False}
