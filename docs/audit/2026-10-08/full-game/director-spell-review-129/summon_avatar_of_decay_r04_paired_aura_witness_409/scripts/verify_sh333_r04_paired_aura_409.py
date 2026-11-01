#!/usr/bin/env python3
"""Independent source/replay/semantic audit. Does not import the builder."""
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import zipfile

REV = '3ade1339a286add11f669c66800809995a494116'
BASE = 'docs/audit/2026-10-08/full-game/director-spell-review-129/'
FAMILY = 'summon-avatar-of-decay'
checks = 0
categories = {}


def require(ok, path, category='semantic'):
    global checks
    checks += 1
    categories[category] = categories.get(category, 0) + 1
    if not ok:
        raise AssertionError(path)


def canonical(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()


def sha(x):
    return hashlib.sha256(x).hexdigest()


def at(x, pointer):
    if not pointer:
        return x
    for part in pointer[1:].split('/'):
        key = part.replace('~1', '/').replace('~0', '~')
        x = x[int(key)] if isinstance(x, list) else x[key]
    return x


def apply(state, operations, absent=(), allow_root=False):
    s = copy.deepcopy(state)
    for p in absent:
        try:
            at(s, p)
        except (KeyError, IndexError):
            pass
        else:
            raise AssertionError('absence precondition: ' + p)
    previous = None
    for op in operations:
        p = op['path']
        require(bool(p) or allow_root, 'no root replacement', 'replay')
        if op['op'] == 'test':
            require(at(s, p) == op['value'], 'patch test: ' + p, 'replay')
        else:
            require(op['op'] in ['replace', 'add', 'remove'], 'patch operation', 'replay')
            if op['op'] != 'add':
                require(previous is not None and previous['op'] == 'test' and previous['path'] == p,
                        'field precondition: ' + p, 'replay')
            if not p:
                s = copy.deepcopy(op['value'])
            else:
                parent, _, key = p.rpartition('/')
                obj = at(s, parent)
                key = key.replace('~1', '/').replace('~0', '~')
                if isinstance(obj, list):
                    key = int(key)
                if op['op'] == 'remove':
                    del obj[key]
                else:
                    obj[key] = copy.deepcopy(op['value'])
        previous = op
    return s


def box(v):
    x, y, z = v['pos']
    w, d, h = v['box']
    return [x-w/2, x+w/2, y-d/2, y+d/2, z, z+h]


def collision(a, b):
    return all(min(a[2*i+1], b[2*i+1]) > max(a[2*i], b[2*i]) for i in range(3))


def contained(a, b):
    return all(b[2*i] <= a[2*i] <= a[2*i+1] <= b[2*i+1] for i in range(3))


def ray_blocked(a, b, wall):
    low, high = 0, 1
    for i in range(3):
        delta = b[i]-a[i]
        if not delta:
            if not wall[2*i] < a[i] < wall[2*i+1]:
                return False
        else:
            enter, leave = sorted([(wall[2*i]-a[i])/delta, (wall[2*i+1]-a[i])/delta])
            low, high = max(low, enter), min(high, leave)
    return low < high


def gap2(a, b):
    return sum(max(a[2*i]-b[2*i+1], b[2*i]-a[2*i+1], 0)**2 for i in range(3))


def nearest_segment(a, b):
    start, end = [], []
    for i in range(3):
        alo, ahi, blo, bhi = a[2*i], a[2*i+1], b[2*i], b[2*i+1]
        if ahi < blo:
            start.append(ahi); end.append(blo)
        elif bhi < alo:
            start.append(alo); end.append(bhi)
        else:
            mid = (max(alo, blo) + min(ahi, bhi))/2
            start.append(mid); end.append(mid)
    return start, end


folder = Path(sys.argv[1])
archive = Path(sys.argv[2])
load = lambda name: json.loads((folder / name).read_bytes())
bindings = load('SOURCE_BINDINGS_409.json')
require(bindings['revision'] == REV, 'binding revision', 'source')
raw_archive = archive.read_bytes()
with zipfile.ZipFile(archive) as z:
    require(z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) == 107, 'Return285 archive integrity', 'source')
    for i, binding in enumerate(bindings['bindings']):
        raw = (folder / binding['member']).read_bytes()
        require(len(raw) == binding['bytes'] and sha(raw) == binding['sha256'], f'bindings/{i}/bytes-hash', 'source')
        require(binding['commit'] == REV, f'bindings/{i}/commit', 'source')
        if 'repositoryPath' in binding:
            exact = subprocess.check_output(['git', 'show', REV + ':' + binding['repositoryPath']])
            blob = subprocess.check_output(['git', 'rev-parse', REV + ':' + binding['repositoryPath']], text=True).strip()
            require(exact == raw and blob == binding['gitBlobSHA1'], f'bindings/{i}/git-exact', 'source')
        else:
            require(sha(raw_archive) == binding['archiveSHA256'] and len(raw_archive) == binding['archiveBytes'], f'bindings/{i}/archive', 'source')
            git = subprocess.check_output(['git', 'show', REV + ':' + binding['archiveRepositoryPath']])
            require((f'oid sha256:{binding["archiveSHA256"]}' in git.decode(errors='replace') and f'size {len(raw_archive)}' in git.decode(errors='replace')) or git == raw_archive,
                    f'bindings/{i}/repository-archive-object', 'source')
            require(z.read(binding['archiveMember']) == raw and format(z.getinfo(binding['archiveMember']).CRC, '08x') == binding['crc32'], f'bindings/{i}/member', 'source')
        for pointer in binding.get('jsonPointers', []):
            at(json.loads(raw), pointer)
            require(True, binding['member'] + '#' + pointer, 'source')

profile = load('sources/W17D.json')
profile_n = load('sources/W17N.json')
wizard = load('sources/WIZARD.json')
ferry = load('sources/FERRY333.json')
body = load('sources/BODY_PROFILES.json')['SH202-DECAY']
proc = load('sources/DECAY285.json')
residual = load('sources/RESIDUAL333.json')['branches'][3]
require(residual['id'] == 'SH333-R04' and 'source-qualified conditional encounter is sufficient' in residual['minimum'], 'R04 authorized scope', 'source')
require(load('sources/ACTOR_PROFILES.json')['W17D'] == profile, 'W17D extraction lineage', 'source')
require(load('sources/ACTOR_PROFILES.json')['W17N'] == profile_n, 'W17N extraction lineage', 'source')
require(profile['id'] != profile_n['id'] and profile['heroPath'] != profile_n['heroPath'], 'distinct bound identities and profiles', 'source')
require(at(profile, '/ordinaryLearning/16/selected/4') == at(profile, '/spellbook/57') == at(profile, '/prepared/4') == FAMILY, 'lawful W17D acquisition/book/preparation', 'source')
require(at(profile_n, '/ordinaryLearning/16/selected/4') == at(profile_n, '/spellbook/57') == at(profile_n, '/prepared/4') == FAMILY, 'lawful W17N acquisition/book/preparation', 'source')
require(profile_n['school'] == 'Necromancy' and profile_n['schoolDC'] == 21 and profile_n['hpMaximum'] == 104 and profile_n['rpMaximum'] == 64, 'W17N native derived stats', 'source')
require(at(profile_n, '/acquisitionLedger/9/choices/1/id') == 'wizard.hero.necromancer.flesh-ascendant' and wizard['cards'][44]['id'] == 'wizard.hero.necromancer.flesh-ascendant', 'Flesh Ascendant actual acquisition', 'source')
require(profile['classLevel'] == 17 and profile['PB'] == 6 and profile['M'] == 5 and profile['spellDC'] == 19, 'Wizard17 source stats', 'source')
require(profile['hpMaximum'] == 104 and profile['rpMaximum'] == 64 and profile['arcaneWard'] == 'force', 'current level17 HP/RP/Ward', 'source')
require(wizard['cards'][17]['id'] == 'wizard.base.counterspell' and wizard['cards'][17]['cost'] == '3 RP', 'Counterspell exact card', 'source')
require(any(c['id'] == 'wizard.base.counterspell' for c in profile['automaticCards']), 'automatic acquisition', 'source')
require(profile['sourceClassBinding']['sha256'] == sha((folder/'sources/WIZARD.json').read_bytes()), 'current class parity', 'source')
require(profile_n['sourceClassBinding']['sha256'] == sha((folder/'sources/WIZARD.json').read_bytes()), 'W17N current class parity', 'source')
ferry_lf = (folder/'sources/FERRY_NATIVE.md').read_bytes()
require(b'\r' not in ferry_lf and len(ferry_lf) == 4637 and sha(ferry_lf) == '393a659464c3cbc49c349df5376fb44eeea8d169984e0f3933fc2a125db52895', 'Ferry current LF exact bytes', 'source')
require(ferry['nativeSourceBinding']['sha256'] == sha(ferry_lf.replace(b'\n', b'\r\n')) and ferry['nativeSourceBinding']['bytes'] == len(ferry_lf.replace(b'\n', b'\r\n')), 'Ferry historical CRLF reconstruction parity', 'source')
require(ferry['nativeUnchanged']['HP'] == 9 and ferry['nativeUnchanged']['CON'] == 14 and ferry['nativeUnchanged']['resistances'] == ['necrotic'], 'Ferry defenses', 'source')
require(body['box'] == [10, 10, 10] and body['nativeHP'] == 250 and body['massLb'] == 900 and body['aura']['dice'] == [2, 6], 'Decay body/aura', 'source')
require('greatest rolled unsuppressed pool' in proc['commonProcedure']['aura'] and 'first future regular START' in proc['commonProcedure']['aura'], 'aura arbitration/timing source', 'source')
queue = load('sources/QUEUE404.json')
require(queue['currentAuthority'] == {'reviewedApplied': 829, 'pending': 19, 'acceptedUnapplied': 0, 'completeStandaloneProcedures': 553, 'scopedInterfaces': 173}, 'Queue404 exact authority', 'authority')
require(len(queue['remainingPendingIds']) == 19 and FAMILY in queue['remainingPendingIds'], 'identity held inventory', 'authority')

# Revalidate the four previously complete component traces without promoting them to encounters.
component_count = 0
for mode in ['LARGER', 'TIE_EARLIER', 'TIE_SOURCE_ID', 'SUPPRESSED_HIGHER']:
    c = load('sources/SH333-AURA-' + mode + '.json')
    require(not c['providerActivationOrPaidEncounterDemonstrated'], 'component remains component: ' + mode, 'component')
    state = copy.deepcopy(c['initialState'])
    require(sha(canonical(state)) == c['initialSHA256'], 'component initial hash', 'component')
    for event in c['events']:
        require(state == event['before'] and sha(canonical(state)) == event['beforeSHA256'], 'component before', 'component')
        state = apply(state, event['forward'], allow_root=True)
        require(state == event['after'] and sha(canonical(state)) == event['afterSHA256'], 'component after', 'component')
    winner = sorted([p for p in c['initialState']['pools'] if not p['suppressed']], key=lambda p: (-p['raw'], p['application'], p['id']))[0]
    require(state['allocation']['winner'] == winner['id'] and all(p['consumed'] for p in state['pools']), 'component true winner/loser consumption', 'component')
    require(state == c['finalState'] and sha(canonical(state)) == c['finalSHA256'], 'component final', 'component')
    for event in reversed(c['events']):
        state = apply(state, event['inverse'], allow_root=True)
    require(state == c['initialState'], 'component full restoration', 'component')
    component_count += 1

initial = load('INITIAL_409.json')
require(initial['actors']['P']['sourceIdentity'] == 'W17D' and initial['actors']['Q']['sourceIdentity'] == 'W17N', 'separate actor source identities', 'source')
require(initial['actors']['P']['profileRef'] == 'sources/W17D.json#' and initial['actors']['Q']['profileRef'] == 'sources/W17N.json#', 'separate active profile pointers', 'source')
require(initial['actors']['P']['carriedItems'] != initial['actors']['Q']['carriedItems'] and not set(initial['actors']['P']['carriedItems']) & set(initial['actors']['Q']['carriedItems']), 'distinct equipment identities', 'source')
require(initial['actors']['Q']['resistances'] == ['necrotic'] and initial['actors']['Q']['arcaneWardSelection'] == 'necrotic' and wizard['cards'][57]['id'] == 'wizard.supplement.arcane-ward', 'lawful branch preparation Ward choice; preserved historical force label not exercised', 'source')
states = load('SNAPSHOTS_409.json')
events = load('EVENTS_409.json')
require(initial == states['S000'] and len(states) == len(events)+1, 'snapshot references/count', 'replay')
state = copy.deepcopy(initial)
for i, event in enumerate(events):
    require(event['beforeStateId'] == 'S%03d' % i and event['afterStateId'] == 'S%03d' % (i+1), f'events/{i}/references', 'replay')
    require(state == states[event['beforeStateId']] and sha(canonical(state)) == event['beforeSHA256'], f'events/{i}/before', 'replay')
    require(event['tick'] >= state['tick'], f'events/{i}/monotone', 'replay')
    state = apply(state, event['forward'], event['forwardAbsentPaths'])
    require(state == states[event['afterStateId']] and sha(canonical(state)) == event['afterSHA256'], f'events/{i}/after', 'replay')
    require(state['tick'] == event['tick'] and state['worldElapsedSeconds'] == event['tick']/100, f'events/{i}/clock', 'replay')
    for ref in event['sourceRefs']:
        member, pointer = ref.split('#', 1) if '#' in ref else (ref.split('@', 1)[0], None)
        require((folder/member).is_file(), ref, 'source')
        if pointer is not None:
            at(load(member), pointer)
terminal = copy.deepcopy(state)
expected = load('EXPECTED_TERMINAL_409.json')
require(sha(canonical(terminal)) == expected['terminalSHA256'] and sha(canonical(initial)) == expected['initialSHA256'], 'full terminal comparison', 'replay')
for i, event in reversed(list(enumerate(events))):
    state = apply(state, event['inverse'], event['inverseAbsentPaths'])
    require(state == states[event['beforeStateId']] and sha(canonical(state)) == event['beforeSHA256'], f'events/{i}/inverse', 'replay')
require(state == initial, 'exact initial restoration', 'replay')

# Independently calculate geometry and check invariants for every full snapshot.
for name, s in states.items():
    require(s['scene'] == initial['scene'] and s['items'] == initial['items'], name + '/scene and property', 'geometry')
    entities = dict(s['actors'], **s['bodies'])
    for k, v in entities.items():
        bb = box(v)
        require(contained(bb, s['scene']['bounds']) and bb[4] == 0, name + '/' + k + '/support-clearance', 'geometry')
        total_mass = v['massLb'] + v.get('carriedMassLb', 0)
        require(total_mass / (v['box'][0]*v['box'][1]) <= s['scene']['floorCapacityLbPerSqFt'], name + '/' + k + '/support-capacity', 'geometry')
        require(not any(collision(bb, w) for w in s['scene']['solids']), name + '/' + k + '/no-solid-overlap', 'geometry')
    for (ka, va), (kb, vb) in itertools.combinations(entities.items(), 2):
        require(not collision(box(va), box(vb)), name + '/' + ka + '/' + kb + '/no-body-overlap', 'geometry')
    for k, a in s['actors'].items():
        require(a['pos'] == initial['actors'][k]['pos'] and a['conditions'] == [], name + '/' + k + '/stationary-able', 'semantic')
        require(a['carriedMassLb'] == sum(s['items'][item]['massLb'] for item in a['carriedItems']), name + '/' + k + '/load-mass', 'geometry')
        for item in a['carriedItems']:
            require(s['items'][item]['custodian'] == k and contained(s['items'][item]['bounds'], box(a)), name + '/' + item + '/custody-envelope', 'geometry')
        require(a['budget']['Reaction'] == 1, name + '/' + k + '/declines-do-not-spend-Reaction', 'semantic')
        require(a['controller'] == a['originalOwner'] == k, name + '/' + k + '/agency', 'semantic')
        require(a['Refrain'] == (None if k == 'F' else 0), name + '/' + k + '/no-unearned-history-reset', 'semantic')
    require(sum(a['turn']['active'] for a in s['actors'].values()) <= 1, name + '/no-overlapping-turns', 'timing')
    require(s['relations'] == s['hardGuards'] == {} and s['commandHistory'] == [], name + '/no-control-scope-creep', 'authority')
    for sid, src in s['sources'].items():
        require(src['deadline'] == src['formedAt'] + 6000 and s['actors'][src['owner']]['concentration'] == sid,
                name + '/' + sid + '/independent-source-clock', 'timing')
        require(src['active'] and not src['suppressed'] and src['paidRP'] == 26, name + '/' + sid + '/source-paid-live', 'semantic')
        b = s['bodies'][src['bodyId']]
        is_necro = src['owner'] == 'Q'
        require(b['sourceOwner'] == b['controller'] == src['owner'] and b['hp'] == 250 and b['maxHP'] == (284 if is_necro else 250) and b['AC'] == 15 and b['saveDC'] == (21 if is_necro else 19),
                name + '/' + sid + '/owner-and-derived-stats', 'semantic')
        require(b['conjurationBonusHP'] == 0 and b['fleshAscendantBonusHP'] == (34 if is_necro else 0) and b['maxHPIncreaseHealing'] == 0 and b['controlledUndeadCount'] == 1 and b['saveBonus'] == 6 and b['ordinaryReaction'] == 0 and b['cargo'] == [], name + '/' + sid + '/acquired-effects-no-unselected-benefits', 'semantic')

# Three real regular slots, exactly once, no implied six-second refresh at arbitrary events.
for k, phase in [('P', 0), ('Q', 100), ('F', 200)]:
    a = terminal['actors'][k]
    require(a['turn']['startsConsumed'] == [phase] and a['turn']['endsConsumed'] == [phase+80] and a['turn']['refreshCount'] == 1, k + '/ordered-single-grants', 'timing')
    require(a['turn']['nextStart'] == phase+600 and a['turn']['nextEnd'] == phase+680 and not a['turn']['active'], k + '/future-markers', 'timing')
    require(a['budget'] == {'Action': 0, 'BonusAction': 0, 'Reaction': 1, 'Movement': 0, 'Interaction': 0}, k + '/expired-wallets', 'timing')
    require(a['stance'] == 'Mobile' and a['stanceExpires'] == phase+600 and a['mobileAllowance'] == 5, k + '/stance-lifetime-no-free-move', 'timing')
    start_event = next(e for e in events if e['kind'] == 'regularStart' and e['evidence']['actor'] == k)
    stance_event = next(e for e in events if e['kind'] == 'voluntaryMobileChoice' and e['evidence']['actor'] == k)
    require(start_event['tick'] < stance_event['tick'], k + '/stance-after-start', 'timing')

for k, commit_tick in [('P', 10), ('Q', 110)]:
    sid = k + ':decay:409'
    ce = next(e for e in events if e['kind'] == 'castCommit' and e['evidence']['actor'] == k)
    pre, paid = states[ce['beforeStateId']], states[ce['afterStateId']]
    require(ce['tick'] == commit_tick and pre['actors'][k]['turn']['active'], k + '/own-Action-time', 'casting')
    require(pre['actors'][k]['RP'] == 64 and paid['actors'][k]['RP'] == 38 and pre['actors'][k]['budget']['Action'] == 1 and paid['actors'][k]['budget']['Action'] == 0,
            k + '/paid26-and-Action', 'casting')
    require(paid['actors'][k]['preparedFamiliesUsed'] == [FAMILY] and paid['actors'][k]['magicThisTurn'] and paid['actors'][k]['Dissonance'] == 0,
            k + '/protected-first-family', 'casting')
    require(paid['pendingCast']['school'] == 'Necromancy' and paid['pendingCast']['rank'] == 9 and paid['actors'][k]['concentration'] == sid, k + '/paid-school-concentration', 'casting')
    source_profile = 'sources/' + ('W17D' if k == 'P' else 'W17N') + '.json'
    require(ce['evidence']['profileAccess'] == [source_profile+'#/ordinaryLearning/16/selected/4', source_profile+'#/spellbook/57', source_profile+'#/prepared/4'], k + '/own-acquisition-not-cloned', 'casting')
    a = paid['actors'][k]
    require(a['voiceAvailable'] and a['hands']['right'] is None and a['hands']['left'] == 'focus-'+k and paid['items']['focus-'+k]['location'] == 'leftHand', k + '/VSF', 'casting')
    anchor = paid['pendingCast']['anchor']
    require(max(abs(anchor[i]-a['pos'][i]) for i in range(3)) == 35 <= 120, k + '/range', 'geometry')
    proposed = box({'pos': anchor, 'box': [10, 10, 10]})
    require(not any(collision(proposed, box(v)) for v in dict(pre['actors'], **pre['bodies']).values()), k + '/declared-whole-body-fit', 'geometry')
    eye = [a['pos'][0], a['pos'][1], 5.5]
    ray_end = [anchor[0], anchor[1], 5]
    obstacles = [box(v) for key, v in dict(pre['actors'], **pre['bodies']).items() if key != k] + pre['scene']['solids']
    require(not any(ray_blocked(eye, ray_end, b) for b in obstacles), k + '/formation-LoE', 'geometry')
    window = next(e for e in events if e['kind'] == 'counterspellWindow' and e['evidence']['rows'][0]['actor'] == k)
    form = next(e for e in events if e['kind'] == 'formation' and e['evidence']['source'] == sid)
    require(ce['tick'] < window['tick'] < form['tick'] == commit_tick+10, k + '/commit-window-resolution', 'casting')
    wbefore, wafter = states[window['beforeStateId']], states[window['afterStateId']]
    require(wbefore['actors'] == wafter['actors'] and wbefore['pendingCast'] == wafter['pendingCast'], k + '/cost-free-window', 'casting')
    other = 'Q' if k == 'P' else 'P'
    row = next(r for r in window['evidence']['rows'] if r['actor'] == other)
    oa = wbefore['actors'][other]
    require(row['eligible'] and row['decision'] == 'TEST_ONLY_DECLINE' and oa['RP'] >= 3 and oa['recharge']['wizard.base.counterspell'] == 0, k + '/opposite-caster-eligible', 'casting')
    require(oa['voiceAvailable'] and oa['hands']['right'] is None and oa['hands']['left'] == 'focus-'+other and oa['budget']['Reaction'] == 1, k + '/responder-components', 'casting')
    other_eye = [oa['pos'][0], oa['pos'][1], 5.5]
    require(max(abs(eye[i]-other_eye[i]) for i in range(3)) == row['gridDistanceFeet'] == 60, k + '/counter-range-inclusive', 'geometry')
    require(not any(ray_blocked(other_eye, eye, box(v)) for key, v in dict(wbefore['actors'], **wbefore['bodies']).items() if key not in [k, other]), k + '/counter-perception-LoE', 'geometry')
    require(all(r['costRP'] == r['reactionSpent'] == 0 for r in window['evidence']['rows']), k + '/all-declines-no-cost', 'casting')
    require(window['evidence']['rows'][0]['eligible'] == 'UNADJUDICATED' and not window['evidence']['rows'][0]['selfCounterProhibitionAsserted'], k + '/no-invented-self-prohibition', 'casting')
    require(states[form['afterStateId']]['aura']['roots'] == {}, k + '/no-entry-or-formation-pulse', 'timing')

# Coverage is independently reconstructed for each regular-start marker, including body-owner markers.
for e in [e for e in events if e['kind'] == 'regularAuraCoverage']:
    s = states[e['beforeStateId']]
    who = e['evidence']['actor']
    recipients = {who: s['actors'][who], **{k: v for k, v in s['bodies'].items() if v['sourceOwner'] == who}}
    expected_rows = []
    for rid, r in recipients.items():
        for sid, src in s['sources'].items():
            if src['bodyId'] == rid:
                continue
            bb, rb = box(s['bodies'][src['bodyId']]), box(r)
            d2 = gap2(bb, rb)
            start, finish = nearest_segment(bb, rb)
            obstacles = [box(v) for k, v in dict(s['actors'], **s['bodies']).items() if k not in [rid, src['bodyId']]] + s['scene']['solids']
            clear = not any(ray_blocked(start, finish, wall) for wall in obstacles)
            expected_rows.append({'recipient': rid, 'source': sid, 'marker': e['tick'], 'distanceSquared': d2, 'inside': d2 <= 100,
                                  'sourceLive': True, 'suppressed': False, 'firstFutureMarkerSatisfied': src['formedAt'] < e['tick'], 'lineOfEffect': clear})
    require(e['evidence']['rows'] == expected_rows, e['id'] + '/exact-coverage', 'geometry')

roots = terminal['aura']['roots']
require(len(roots) == 2 and all(r['marker'] == 200 and r['recipient'] == 'F' for r in roots.values()), 'two actual roots / one actual marker', 'aura')
for k, dice in [('P', [3, 4]), ('Q', [5, 6])]:
    r = roots[k+':decay:409:F:start200']
    require(r['dice'] == dice and len(dice) == 2 and all(1 <= x <= 6 for x in dice) and r['raw'] == sum(dice), k + '/native-dice', 'aura')
    require(r['consumed'] and not r['suppressed'] and not r['dealerNullAtCreation'] and r['dealer'] == k+':decay:409:body', k + '/root-ownership-consumption', 'aura')
winner = sorted(roots.values(), key=lambda r: (-r['raw'], r['formedAt'], r['source']))[0]
require(winner['source'] == 'Q:decay:409' and winner['raw'] == 11, 'higher pool wins before defense', 'aura')
require(sum(r['settled'] for r in roots.values()) == 1 and not roots['P:decay:409:F:start200']['settled'], 'loser-no-damage-packet', 'aura')
settlement = terminal['aura']['settlements']
require(len(settlement) == 1, 'one settled packet', 'aura')
v = settlement[0]
con = (ferry['nativeUnchanged']['CON']-10)//2
after_save = winner['raw']//2 if 18+con >= profile_n['schoolDC'] else winner['raw']
damage = after_save//2
require(v['save'] == {'ability': 'CON', 'd20': 18, 'modifier': con, 'total': 18+con, 'DC': 21, 'success': False}, 'real recipient save against W17N school DC', 'aura')
require(v['raw'] == 11 and v['afterSave'] == after_save == 11 and v['afterResistance'] == damage == 5 and terminal['actors']['F']['hp'] == 9-damage == 4, 'save-then-resistance-settlement', 'aura')
require(terminal['actors']['P']['hp'] == terminal['actors']['Q']['hp'] == 104 and all(b['hp'] == 250 for b in terminal['bodies'].values()), 'no unrelated damage', 'aura')
duplicate = next(e for e in events if e['kind'] == 'duplicateMarkerObservation')
before, after = states[duplicate['beforeStateId']], states[duplicate['afterStateId']]
require(before['actors'] == after['actors'] and before['aura']['roots'] == after['aura']['roots'] and before['aura']['settlements'] == after['aura']['settlements'], 'duplicate marker no replay', 'aura')
require(len(terminal['phaseLedger']) == 2 and all(p['closed'] == p['opened']+1 and p['unusedMovementExpired'] == 30 and not p['offenseUsed'] for p in terminal['phaseLedger']), 'two genuine closed nonoffensive phases', 'timing')
require(terminal['tick'] == 280 and min(a['turn']['nextStart'] for a in terminal['actors'].values()) == 600, 'all due markers through endpoint; future clocks retained', 'timing')
require(terminal['sources']['P:decay:409']['deadline'] == 6020 and terminal['sources']['Q:decay:409']['deadline'] == 6120, 'independent 60-second clocks', 'timing')
scope = load('AUTHORIZATION_AND_SCOPE_409.json')
require(scope['classification'] == 'CONDITIONAL_TEST_ONLY' and not scope['campaignEvent'] and not scope['canonicalPromotion'] and not scope['applicationAuthorized'], 'scope boundary', 'authority')
require(expected['acceptedIds'] == expected['appliedIds'] == [] and not expected['applicationAuthorized'], 'no identity/application action', 'authority')

report = {'id': 'SH333-R04-INDEPENDENT-VERIFICATION-409', 'result': 'PASS', 'revision': REV,
          'assertions': checks, 'categories': categories, 'sourceBindings': len(bindings['bindings']),
          'forwardTransitions': len(events), 'inverseTransitions': len(events), 'snapshots': len(states),
          'preservedComponentCasesReplayedBothWays': component_count, 'exactInitialRestoration': True,
          'terminalSHA256': sha(canonical(terminal)), 'initialSHA256': sha(canonical(initial)),
          'scope': 'Separate verifier; does not import builder. Source bytes, pointers, patch replay, independent geometry, casting, chronology and settlement checks. No game runtime execution.',
          'remainingR04Defects': [], 'acceptedIds': [], 'appliedIds': [], 'applicationAuthorized': False,
          'queueAuthorityUnchanged': queue['currentAuthority']}
(folder/'VERIFICATION_409.json').write_bytes(json.dumps(report, indent=2).encode()+b'\n')
print(json.dumps(report))
