"""ACQ05 conditional chronological reference model, not CRPG implementation.

World facts and continuous work/rest support are explicit conditional premises.
No animal, consent, lawful custody, Ranger grant or campaign event is invented.
Earlier completion-first model/report remain untouched historical evidence.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import pb


class CompanionLifecycle:
    def __init__(self, world_id, templates):
        self.world_id = world_id
        self.templates = {x['id']: deepcopy(x) for x in templates}
        self.owners = {}; self.bodies = {}; self.events = []; self.work = []
        self.last_time = -1; self.sequence = 0

    def event(self, when, kind, **data):
        if type(when) is not int or when < self.last_time:
            raise ValueError('No backdated or unordered authoritative event')
        self.last_time = when; self.sequence += 1
        record = {'at': when, 'sequence': self.sequence, 'kind': kind, **deepcopy(data)}
        self.events.append(record)
        return (when, self.sequence)

    def guard_time(self, when):
        if type(when) is not int or when < self.last_time:
            raise ValueError('No backdated or unordered event')

    def add_owner(self, owner_id, history):
        if owner_id in self.owners or history.pay.has('animal_companion'):
            raise ValueError('Begin with actual unpaid owner history, not reconstructed free ownership')
        self.owners[owner_id] = {'history': history, 'alive': True, 'able': True,
            'handlingAvailable': True, 'attempts': None, 'grant': None, 'bond': None,
            'pending': None, 'release': None, 'lastEnd': None, 'lastRest': None,
            'restReceipts': [], 'workHistory': [], 'rp': 7,
            'actorBudgets': {'bonusActionSpent': True, 'offensiveCompanionActionSpent': True}}

    def add_body(self, body):
        if body.get('id') in self.bodies or body.get('worldId') != self.world_id or body.get('evidenceMode') != 'conditional_fixture':
            raise ValueError('Unique explicitly conditional body in this world required')
        self.bodies[body['id']] = deepcopy(body)

    def snapshot(self):
        owners = {}
        for sid, owner in self.owners.items():
            owners[sid] = {k: (v.snapshot() if k == 'history' else deepcopy(v)) for k, v in owner.items()}
        return {'worldId': self.world_id, 'owners': owners, 'bodies': deepcopy(self.bodies),
            'events': deepcopy(self.events), 'work': deepcopy(self.work), 'lastTime': self.last_time}

    def purchase(self, sid, when, level=4):
        self.guard_time(when); o = self.owners[sid]; h = o['history']
        if o['grant'] is not None or not o['alive'] or not self.handling(sid):
            raise ValueError('Actual eligible living owner and no prior grant required')
        grant = h.pay.commit('animal_companion', h.first + ':' + str(level),
                             prerequisites_met=h.prerequisite('animal_companion'))
        ordered = self.event(when, 'paid-feat-purchase', owner=sid, grant=grant)
        o['grant'] = {'record': grant, 'ordered': ordered, 'worldId': self.world_id,
            'ownerId': sid, 'evidenceMode': 'conditional_fixture'}
        o['attempts'] = 1

    def cancel_purchase_proposal(self, sid, when):
        self.event(when, 'canceled-purchase-proposal', owner=sid)
        # Deliberately does not undo an earlier independently recorded payment.

    def handling(self, sid):
        o = self.owners[sid]
        return o['handlingAvailable'] and o['history'].prerequisite('animal_companion')

    def eligible(self, sid, body_id, template_id, sense):
        b = self.bodies[body_id]
        required = {'id', 'worldId', 'evidenceMode', 'creatureType', 'size', 'living', 'corrupted',
            'abilities', 'ordinaryMaximumHP', 'ordinaryCurrentHP', 'nativeMovement', 'anatomy',
            'breathing', 'conditions', 'injuries', 'relations', 'lawfulAccess', 'custody',
            'currentBonds', 'keenSenses', 'currentHP', 'maximumHP', 'mode', 'budgets', 'version'}
        if not required <= b.keys() or b['worldId'] != self.world_id or b['evidenceMode'] != 'conditional_fixture':
            raise ValueError('Complete same-world conditional body evidence required')
        if b['mode'] != 'ordinary' or b['currentBonds']:
            raise ValueError('No incompatible outgoing bond or additive chassis')
        if b['creatureType'] != 'Beast' or not b['living'] or b['corrupted'] or not 0 <= b['abilities']['INT'] < 7:
            raise ValueError('Positive living noncorrupted Beast INT below7 required')
        for cur, maximum in [(b['currentHP'], b['maximumHP']), (b['ordinaryCurrentHP'], b['ordinaryMaximumHP'])]:
            if type(cur) is not int or type(maximum) is not int or not 0 < cur <= maximum:
                raise ValueError('Actual positive ordinary HP required')
        if b['currentHP'] != b['ordinaryCurrentHP'] or b['maximumHP'] != b['ordinaryMaximumHP']:
            raise ValueError('Ordinary current state and profile differ')
        relationship = b['relations'].get(sid, {})
        if sid not in b['lawfulAccess'] or not (relationship.get('willing') or relationship.get('tamed')):
            raise ValueError('Actual lawful access and willing OR tamed relation required')
        if template_id not in self.templates:
            raise ValueError('Unknown finite template')
        native = b['nativeMovement']; anatomy = set(b['anatomy'])
        match = {
            'feat-animal.ground': b['size'] in {'Small', 'Medium'} and native.get('walkFeet', 0) > 0 and 'bite' in anatomy,
            'feat-animal.flyer': b['size'] == 'Tiny' and native.get('flyFeet', 0) > 0 and 'wings' in anatomy and bool({'bite', 'peck'} & anatomy),
            'feat-animal.swimmer': b['size'] == 'Small' and native.get('swimFeet', 0) > 0 and 'bite' in anatomy,
        }
        if not match[template_id]:
            raise ValueError('Template must match native anatomy/movement/size')
        senses = set(b['keenSenses']) & ({'sight'} if template_id.endswith('flyer') else {'hearing', 'smell'})
        if (senses and sense not in senses) or (not senses and sense is not None):
            raise ValueError('Choose only an actual available permitted sense')

    def start(self, sid, when, body_id, template='feat-animal.ground', sense=None):
        self.guard_time(when); o = self.owners[sid]
        if not o['grant'] or not o['alive'] or not o['able'] or not self.handling(sid):
            raise ValueError('Owned feat and current ability/proficiency required')
        if o['bond'] or o['pending'] or o['release'] or o['attempts'] != 1:
            raise ValueError('One available attempt and no current or pending bond required')
        if o['lastEnd'] is not None and (o['lastRest'] is None or o['lastRest'] <= o['lastEnd']):
            raise ValueError('Beneficial owner LR completion must be ordered after bond end')
        self.eligible(sid, body_id, template, sense)
        if any(x['pending'] and x['pending']['bodyId'] == body_id for x in self.owners.values()):
            raise ValueError('This actual animal is already reserved for bonding work')
        ordered = self.event(when, 'spent-attempt-start', owner=sid, body=body_id)
        o['attempts'] = 0
        o['pending'] = {'id': f'attempt:{sid}:{ordered[1]}', 'ownerId': sid, 'worldId': self.world_id,
            'bodyId': body_id, 'templateId': template, 'sense': sense, 'start': when,
            'orderedStart': ordered, 'observedUntil': when, 'grantRef': deepcopy(o['grant']),
            'bodyVersionAtStart': self.bodies[body_id]['version'], 'segments': []}

    def uninterrupted_work(self, sid, until, support, release=False):
        self.guard_time(until); o = self.owners[sid]
        job = o['release' if release else 'pending']
        if not job or until <= job['observedUntil'] or until > job['start'] + 3600:
            raise ValueError('Continuous new interval within the same full hour required')
        if support.get('evidenceMode') != 'conditional_fixture' or not all(support.get(k) for k in
            ['actualWork', 'uninterrupted', 'noIncompatibleOverlap', 'withinWorkWatchAllowance']):
            raise ValueError('Actual lawful active-work support is required; not extra Watches or rest')
        if not o['alive'] or not o['able']:
            raise ValueError('Owner cannot perform work')
        if not release:
            if not support.get('touch') or not self.handling(sid):
                raise ValueError('Required touch/proficiency not evidenced')
            self.eligible(sid, job['bodyId'], job['templateId'], job['sense'])
        segment = {'start': job['observedUntil'], 'end': until, 'support': deepcopy(support),
            'bodyVersion': self.bodies[job['bodyId']]['version']}
        job['segments'].append(segment); job['observedUntil'] = until
        self.event(until, 'conditional-continuous-release-work' if release else 'conditional-continuous-bond-work',
                   owner=sid, body=job['bodyId'], segment=segment)

    def close_work(self, sid, when, job, outcome):
        record = {**deepcopy(job), 'end': when, 'outcome': outcome}
        self.work.append(record); self.owners[sid]['workHistory'].append(record)

    def interrupt(self, sid, when, cause, release=False):
        self.guard_time(when); o = self.owners[sid]; key = 'release' if release else 'pending'
        job = o[key]
        if not job:
            raise ValueError('No live work to interrupt')
        self.event(when, 'interrupted-release' if release else 'interrupted-attempt', owner=sid, cause=cause)
        self.close_work(sid, when, job, 'interrupted:' + cause); o[key] = None

    def complete(self, sid, when, evidence):
        self.guard_time(when); o = self.owners[sid]; job = o['pending']
        if not job or not isinstance(evidence, dict):
            raise ValueError('Actual prior paid grant/start and completion evidence required')
        expected = {'attemptId': job['id'], 'bodyId': job['bodyId'], 'ownerId': sid,
            'worldId': self.world_id, 'bodyVersion': self.bodies[job['bodyId']]['version']}
        if evidence != expected or when != job['start'] + 3600 or job['observedUntil'] != when:
            raise ValueError('Completion is short, mismatched, stale or lacks continuous work evidence')
        if not o['alive'] or not o['able'] or not self.handling(sid):
            raise ValueError('Owner eligibility lost')
        self.eligible(sid, job['bodyId'], job['templateId'], job['sense'])
        b = self.bodies[job['bodyId']]; template = self.templates[job['templateId']]
        total = sum(o['history'].pay.current_classes.values())
        new_max = 5 + total; hp = max(1, new_max * b['currentHP'] // b['maximumHP'])
        ordinary = deepcopy(b)
        ordered = self.event(when, 'completed-bond', owner=sid, body=b['id'])
        bond_id = f'bond:{sid}:{ordered[1]}'
        b.update(mode='feat', maximumHP=new_max, currentHP=hp, currentBonds=[bond_id],
            controlOwner=sid, pendingCommand=None, activeProfile={**deepcopy(template), 'AC': 12 + pb(total) // 2,
                'size': b['size'], 'breathing': b['breathing'], 'keenSense': job['sense']})
        b['version'] += 1
        o['bond'] = {'id': bond_id, 'bodyId': b['id'], 'ordinary': ordinary, 'orderedStart': ordered}
        self.close_work(sid, when, job, 'completed'); o['pending'] = None

    def completion_evidence(self, sid):
        job = self.owners[sid]['pending']
        return {'attemptId': job['id'], 'bodyId': job['bodyId'], 'ownerId': sid,
            'worldId': self.world_id, 'bodyVersion': self.bodies[job['bodyId']]['version']}

    def body_change(self, body_id, when, changes, cause):
        self.guard_time(when); b = self.bodies[body_id]
        if {'id', 'worldId', 'version'} & set(changes):
            raise ValueError('No overwriting identity, source world or predecessor version')
        self.event(when, 'conditional-physical-event', body=body_id, cause=cause, changes=changes)
        b.update(deepcopy(changes)); b['version'] += 1
        if b['mode'] == 'ordinary' and 'currentHP' in changes:
            b['ordinaryCurrentHP'] = b['currentHP']
        if b['currentHP'] <= 0:
            b['living'] = False
        for sid, o in self.owners.items():
            if o['bond'] and o['bond']['bodyId'] == body_id and not b['living']:
                self.end_bond(sid, when, 'animal-death')
            if o['pending'] and o['pending']['bodyId'] == body_id:
                try:
                    self.eligible(sid, body_id, o['pending']['templateId'], o['pending']['sense'])
                except (ValueError, KeyError):
                    self.interrupt(sid, when, cause)

    def owner_change(self, sid, when, **changes):
        if not set(changes) <= {'alive', 'able', 'handlingAvailable'}:
            raise ValueError('Only explicit conditional ability/eligibility changes supported')
        self.guard_time(when); o = self.owners[sid]
        self.event(when, 'conditional-owner-event', owner=sid, changes=changes); o.update(changes)
        if o['pending'] and (not o['alive'] or not o['able'] or not self.handling(sid)):
            self.interrupt(sid, when, 'owner-capacity-or-proficiency-loss')
        if o['release'] and (not o['alive'] or not o['able']):
            self.interrupt(sid, when, 'owner-capacity-loss', release=True)
        if not o['alive'] and o['bond']:
            self.end_bond(sid, when, 'owner-death')

    def beneficial_rest(self, sid, when, receipt):
        self.guard_time(when); o = self.owners[sid]
        needed = {'id', 'ownerId', 'worldId', 'start', 'end', 'kind', 'evidenceMode',
            'safe', 'supported', 'uninterrupted', 'beneficialEligible', 'debtOnly'}
        if not needed <= receipt.keys() or receipt['ownerId'] != sid or receipt['worldId'] != self.world_id or receipt['end'] != when:
            raise ValueError('Owner/world/time-bound actual rest record required')
        if receipt['id'] in o['restReceipts'] or not o['alive']:
            raise ValueError('Duplicate rest or dead owner')
        if receipt['kind'] != 'LR' or receipt['debtOnly'] or receipt['evidenceMode'] != 'conditional_fixture' or not all(
            receipt[k] for k in ['safe', 'supported', 'uninterrupted', 'beneficialEligible']):
            raise ValueError('No beneficial Long Rest recovery established')
        start = receipt['start']
        if type(start) is not int or when - start != 8 * 3600:
            raise ValueError('Actual full eight-hour Rest required')
        if o['lastRest'] is not None and when - o['lastRest'][0] < 24 * 3600:
            raise ValueError('Only one beneficial LR per24 elapsed hours')
        intervals = [(j['start'], j['end']) for j in o['workHistory']]
        intervals += [(o[k]['start'], when) for k in ['pending', 'release'] if o[k]]
        if any(max(start, a) < min(when, b) for a, b in intervals):
            raise ValueError('Active bonding/release work cannot also be rest')
        ordered = self.event(when, 'beneficial-LR', owner=sid, receipt=receipt)
        o['lastRest'] = ordered; o['restReceipts'].append(receipt['id'])
        if o['grant']:
            o['attempts'] = 1

    def start_release(self, sid, when):
        self.guard_time(when); o = self.owners[sid]
        if not o['bond'] or o['release'] or not o['alive'] or not o['able']:
            raise ValueError('Actual owned feat bond and able owner required; no Ranger release permission')
        ordered = self.event(when, 'release-start', owner=sid, bond=o['bond']['id'])
        o['release'] = {'id': f'release:{sid}:{ordered[1]}', 'ownerId': sid,
            'bodyId': o['bond']['bodyId'], 'bondId': o['bond']['id'], 'start': when,
            'observedUntil': when, 'segments': []}

    def complete_release(self, sid, when):
        self.guard_time(when); o = self.owners[sid]; job = o['release']
        if not job or not o['bond'] or job['bondId'] != o['bond']['id'] or when != job['start'] + 3600 or job['observedUntil'] != when:
            raise ValueError('One complete uninterrupted current release hour required')
        if not o['alive'] or not o['able']:
            raise ValueError('Owner cannot finish release')
        self.close_work(sid, when, job, 'completed'); o['release'] = None
        self.end_bond(sid, when, 'release')

    def end_bond(self, sid, when, reason):
        o = self.owners[sid]; bond = o['bond']; b = self.bodies[bond['bodyId']]
        if o['release']:
            self.interrupt(sid, when, 'independent-bond-ending', release=True)
        ordinary = bond['ordinary']; saved_max = ordinary['ordinaryMaximumHP']
        restored = 0 if not b['living'] else max(1, saved_max * b['currentHP'] // b['maximumHP'])
        b.update(mode='ordinary' if b['living'] else 'corpse', maximumHP=saved_max, currentHP=restored,
            ordinaryMaximumHP=saved_max, ordinaryCurrentHP=restored,
            currentBonds=[], activeProfile=None, controlOwner=None, pendingCommand=None)
        b['version'] += 1
        o['lastEnd'] = self.event(when, 'bond-ended', owner=sid, body=b['id'], cause=reason)
        o['bond'] = None

    def growth(self, sid, when, level):
        self.guard_time(when); o = self.owners[sid]; o['history'].advance(level)
        if o['bond']:
            b = self.bodies[o['bond']['bodyId']]; maximum = 5 + sum(o['history'].pay.current_classes.values())
            b['maximumHP'] = maximum; b['currentHP'] = min(b['currentHP'], maximum)
            b['activeProfile']['AC'] = 12 + pb(level) // 2; b['version'] += 1
        self.event(when, 'actual-level-growth-no-refill', owner=sid, level=level)


def validate_ranger_receiving_history(card, actor, animal, work):
    """Read-only conditional Ranger gate/cost receipt; no class grant/body engine.

Does not invent when Ranger's4RP is paid or how its outgoing bond terminates.
The supplied receipt must already establish that payment and its native hour.
"""
    if actor.get('evidenceMode') != 'conditional_fixture' or actor.get('rangerLevel', 0) < card['minimumClassLevel'] or actor.get('heroPath') != card['path']:
        raise ValueError('Actual Ranger16 Warder source-qualified selection required')
    choice = actor.get('selectedFeature', {})
    if choice.get('featureId') != card['id'] or choice.get('acquisition') != 'selection' or not choice.get('earnedSlot') or not choice.get('committed'):
        raise ValueError('Class name or custody alone is not an acquired feature')
    if not animal.get('living') or animal.get('currentHP', 0) <= 0 or animal.get('currentBonds') or animal.get('creatureType') != 'Beast' or animal.get('corrupted') or not 0 <= animal['abilities']['INT'] < 7:
        raise ValueError('Actual eligible unbonded living Beast required')
    if type(animal.get('CR')) not in (int, float) or not 0 <= animal['CR'] <= actor['rangerLevel']:
        raise ValueError('Actual CR cannot exceed Ranger class level')
    relation = animal.get('relations', {}).get(actor['id'], {})
    if actor['id'] not in animal.get('lawfulAccess', []) or not (relation.get('willing') or relation.get('tamed')):
        raise ValueError('Real receiving-owner access/relationship required')
    if work.get('ownerId') != actor['id'] or work.get('bodyId') != animal['id'] or work.get('worldId') != animal['worldId'] or work.get('evidenceMode') != 'conditional_fixture':
        raise ValueError('Actual same-body owner/world work evidence required')
    if work.get('seconds') != 3600 or work.get('touchSeconds') != 3600 or work.get('interruptions') != [] or not work.get('nativeAttemptAvailable'):
        raise ValueError('Native once/LR full uninterrupted touch hour required')
    if work.get('paidRP') != 4 or work.get('rpBefore', -1) < 4 or work.get('rpAfter') != work['rpBefore'] - 4:
        raise ValueError('Actual4RP cost cannot borrow the feat no-RP route')
    return {'status': 'conditional-receiving-gates-and-paid-hour-established',
        'nativeChassisInstalled': False, 'rangerGrantCreated': False, 'featGrantRequired': False}
