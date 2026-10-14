"""Bounded BS-01 reference model, not installed game runtime.

Inputs are already-adjudicated lawful attacks, actual host-turn identities, and
elapsed game time. This model grants no action, target or turn permission.
"""
from dataclasses import dataclass, field
from fractions import Fraction


def seconds(value):
    return Fraction(str(value))


@dataclass
class RiderItem:
    physical_item_id: str
    time: Fraction = Fraction(0)
    mode: str = 'outside'
    host_turn: str | None = None
    outside_origin: Fraction | None = None
    spent_windows: set = field(default_factory=set)
    spent_turns: set = field(default_factory=set)
    last_trigger: dict | None = None
    trigger_events: dict = field(default_factory=dict)
    guards: dict = field(default_factory=dict)

    def advance(self, now):
        now = seconds(now)
        if now < self.time:
            raise ValueError('Elapsed game time cannot go backward in this reference.')
        self.time = now
        for guard in self.guards.values():
            if guard['status'] == 'pending' and now >= guard['deadline']:
                guard['status'] = 'expired'

    def assign_pending(self):
        if self.mode != 'initiative' or self.host_turn is None:
            return
        for guard in self.guards.values():
            if guard['status'] == 'pending' and self.time < guard['deadline']:
                guard['status'] = 'assigned'
                guard['assignedHostTurnId'] = self.host_turn
                self.spent_turns.add(self.host_turn)

    def enter_initiative(self, now, host_turn=None):
        self.advance(now)
        self.mode = 'initiative'
        self.host_turn = host_turn
        last = self.last_trigger
        if last and last['context'] == 'outside' and self.time < last['time'] + 6:
            self.guards.setdefault(last['eventId'], {
                'originatingTriggerEventId': last['eventId'],
                'deadline': last['time'] + 6,
                'status': 'pending', 'assignedHostTurnId': None})
        self.assign_pending()

    def host(self, now, turn_id, kind='regular'):
        if self.mode != 'initiative' or not turn_id or kind not in {'regular', 'extra', 'resume'}:
            raise ValueError('Only an authoritative actual initiative host turn may be supplied.')
        self.advance(now)
        self.host_turn = turn_id
        self.assign_pending()

    def between_turns(self, now):
        self.advance(now)
        self.host_turn = None

    def leave_initiative(self, now):
        self.advance(now)
        self.mode = 'outside'
        self.host_turn = None

    def outside_index(self):
        if self.outside_origin is None:
            return None
        return (self.time - self.outside_origin) // 6

    def attack(self, now, event_id, *, lawful=True, actual_item=True, copied=False,
               hit=True, choose=True, functional=True, suppressed=False, melded=False,
               starts_encounter=False, encounter_host=None, mitigated_to_zero=False):
        self.advance(now)
        # Encounter routing precedes any outside-origin/window operation.
        if starts_encounter and self.mode == 'outside':
            self.enter_initiative(now, encounter_host)
        relevant = lawful and actual_item and not copied and functional and not melded
        if relevant and self.mode == 'outside' and self.outside_origin is None:
            self.outside_origin = self.time
        if not relevant or not hit or not choose or suppressed:
            return False
        if self.mode == 'initiative':
            if self.host_turn is None or self.host_turn in self.spent_turns:
                return False
        else:
            last = self.last_trigger
            if last and last['context'] == 'initiative' and self.time < last['time'] + 6:
                return False
            if self.outside_index() in self.spent_windows:
                return False
        if not event_id or event_id in self.trigger_events:
            raise ValueError('An actual rider trigger needs a fresh authoritative event identity.')
        if self.mode == 'initiative':
            self.spent_turns.add(self.host_turn)
        else:
            self.spent_windows.add(self.outside_index())
        # Expenditure occurs before mitigation. Zero damage has no refund path.
        trigger = {'time': self.time, 'context': self.mode, 'eventId': event_id}
        self.last_trigger = trigger
        self.trigger_events[event_id] = dict(trigger)
        return True

    def snapshot(self):
        def portable(value):
            if isinstance(value, Fraction):
                return str(value)
            if isinstance(value, dict):
                return {k: portable(v) for k, v in value.items()}
            return value
        return {'physicalItemId': self.physical_item_id, 'gameTime': str(self.time),
                'mode': self.mode, 'hostTurnId': self.host_turn,
                'outsideWindowOriginTime': None if self.outside_origin is None else str(self.outside_origin),
                'spentOutsideWindowIndices': sorted(self.spent_windows),
                'spentActualTurnIds': sorted(self.spent_turns),
                'lastActualTrigger': portable(self.last_trigger),
                'triggerEvents': portable(self.trigger_events), 'transitionGuards': portable(self.guards)}


def run_cases():
    cases = []

    def check(name, passed, item):
        cases.append({'name': name, 'pass': bool(passed), 'finalState': item.snapshot()})

    a = RiderItem('A')
    assert not a.attack(0, 'miss', hit=False)
    v = [a.attack('5.9', 'first'), a.attack('5.99', 'blocked'), a.attack(6, 'next')]
    check('BS01-01 fixed origin after miss; 5.9 and exact 6 boundary', v == [True, False, True] and a.outside_origin == 0 and a.spent_windows == {0, 1}, a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1, 'A-turn')
    check('BS01-02 unused first host turn consumes entry guard immediately', a.spent_turns == {'A-turn'} and a.guards['outside']['status'] == 'assigned' and a.last_trigger['time'] == 0, a)
    a.host(2, 'B-turn')
    check('BS01-03 later genuine turn before deadline retains independent budget', a.attack(2, 'B-hit') and a.last_trigger['time'] == 2, a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1, 'A-turn')
    check('BS01-04 assigned host stays spent beyond six-second deadline', not a.attack(7, 'late-A') and a.guards['outside']['assignedHostTurnId'] == 'A-turn', a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1); a.host(6, 'boundary')
    check('BS01-05 unassigned guard expires at exact deadline', a.guards['outside']['status'] == 'expired' and a.attack(6, 'boundary-hit'), a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1, 'enemy-running-turn')
    check('BS01-06 midturn entry guards host, including a wielder reaction', not a.attack(2, 'reaction') and a.spent_turns == {'enemy-running-turn'}, a)

    a = RiderItem('A'); a.enter_initiative(0, 'parent')
    parent = a.attack(0, 'parent-hit'); a.host(0, 'extra', 'extra'); extra = a.attack(0, 'extra-hit'); a.host(0, 'parent', 'resume')
    check('BS01-07 interrupted parent retains its own expenditure', parent and extra and not a.attack(0, 'resumed-hit') and a.spent_turns == {'parent', 'extra'}, a)

    a = RiderItem('A'); a.attack(0, 'initial-miss', hit=False); a.enter_initiative(1, 'turn'); a.attack(2, 'initiative-hit'); a.leave_initiative(3)
    v = [a.attack('7.999', 'early'), a.attack(8, 'at-deadline')]
    check('BS01-08 exit lockout derives from trigger time, not exit', v == [False, True] and a.outside_origin == 0 and a.spent_windows == {1}, a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1, 'host'); before = dict(a.guards['outside']); a.leave_initiative(2); a.enter_initiative(2, 'host')
    same = not a.attack(2, 'same-host'); a.leave_initiative(2); a.enter_initiative(2, 'genuine-next')
    check('BS01-09 toggling preserves origin, expenditure and one guard assignment', same and a.guards['outside'] == before and len(a.guards) == 1 and a.outside_origin == 0 and a.attack(2, 'next-hit'), a)

    a = RiderItem('A'); a.enter_initiative(0, 'host'); used = a.attack(0, 'immune-hit', mitigated_to_zero=True)
    check('BS01-10 zero mitigated damage does not refund accepted use', used and not a.attack(0, 'second') and a.last_trigger['eventId'] == 'immune-hit', a)

    a = RiderItem('A'); a.enter_initiative(0)
    check('BS01-11 no actual host provides no rider or borrowed outside window', not a.attack(1, 'between') and a.outside_origin is None and not a.trigger_events, a)

    a = RiderItem('A'); a.enter_initiative(0, 'host'); a.attack(0, 'spent')
    unavailable = [a.attack(1, 'suppressed', suppressed=True), a.attack(2, 'melded', melded=True), a.attack(3, 'returned-after-transfer')]
    a.host(3, 'next'); still_suppressed = a.attack(3, 'suppressed-next', suppressed=True); recovered = a.attack(3, 'unsuppressed-next')
    check('BS01-12 suppression transfer and melding preserve spending; only fresh unblocked recovery', unavailable == [False, False, False] and not still_suppressed and recovered, a)

    a = RiderItem('A'); a.enter_initiative(0, 'host'); b = RiderItem('B'); b.enter_initiative(0, 'host')
    check('Independent physical copies use separate budgets', a.attack(0, 'A-hit') and b.attack(0, 'B-hit'), b)

    a = RiderItem('A'); a.enter_initiative(0, 'host')
    values = [a.attack(0, 'miss', hit=False), a.attack(0, 'declined', choose=False), a.attack(0, 'copied', copied=True), a.attack(0, 'unlawful', lawful=False), a.attack(0, 'real')]
    check('Miss decline copy and ineligible events neither spend nor refund', values == [False, False, False, False, True] and set(a.trigger_events) == {'real'}, a)

    a = RiderItem('A'); a.enter_initiative(0, 'other-creature')
    check('Off-turn reaction/readied event shares actual host budget', a.attack(0, 'reaction') and not a.attack(0, 'readied-same-host'), a)

    a = RiderItem('A'); routed = a.attack(0, 'encounter-first', starts_encounter=True, encounter_host='entry-turn')
    check('Encounter-starting attack is routed before outside origin', routed and a.outside_origin is None and a.last_trigger['context'] == 'initiative', a)

    a = RiderItem('A'); a.attack(0, 'declined', choose=False); a.attack(18, 'window3')
    check('Skipped fixed windows do not bank uses or reanchor origin', not a.attack(18, 'second-window3') and a.outside_origin == 0 and a.spent_windows == {3}, a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1)
    before = a.snapshot()
    try:
        a.host(2, 'virtual-marker', 'virtual')
        rejected = False
    except ValueError:
        rejected = True
    check('Virtual duration marker cannot assign guard or manufacture a turn', rejected and a.snapshot() == before, a)

    a = RiderItem('A'); a.attack(0, 'outside'); a.enter_initiative(1); a.leave_initiative(2); a.enter_initiative(3); a.host('5.99', 'actual')
    check('Pending guard survives mode toggles and assigns once before deadline', a.guards['outside']['status'] == 'assigned' and a.spent_turns == {'actual'} and not a.attack(7, 'late-same-host'), a)

    a = RiderItem('A'); a.attack(0, 'old-outside'); a.enter_initiative(1, 'guarded'); a.host(2, 'new'); a.attack(2, 'initiative'); a.leave_initiative(3)
    # Window 1 is independently already spent only through an actual outside use;
    # inject its preserved history to exercise conjunction with an elapsed lockout.
    a.spent_windows.add(1)
    check('Expired exit lockout still requires an unspent anchored window', not a.attack(8, 'spent-window') and a.attack(12, 'new-window'), a)
    return cases


if __name__ == '__main__':
    import json
    results = run_cases()
    print(json.dumps({'cases': len(results), 'failed': [x['name'] for x in results if not x['pass']]}, indent=2))
    if not all(x['pass'] for x in results):
        raise SystemExit(1)
