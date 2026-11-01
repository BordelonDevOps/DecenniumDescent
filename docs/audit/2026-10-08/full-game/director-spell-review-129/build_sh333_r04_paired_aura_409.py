#!/usr/bin/env python3
"""Build the authorized, conditional paired-source R04 witness; no live state edits."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

REV = '3ade1339a286add11f669c66800809995a494116'
BASE = 'docs/audit/2026-10-08/full-game/director-spell-review-129/'
R333 = BASE + 'rank9_summon_avatar_of_decay_return333_received/payload/'
ROOT = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
OUT = ROOT / BASE / 'summon_avatar_of_decay_r04_paired_aura_witness_409'
FAMILY = 'summon-avatar-of-decay'
bindings = []


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write(name, x):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(x, indent=2, ensure_ascii=False, allow_nan=False).encode() + b'\n')


def source(name, path, pointers=(), locators=()):
    raw = subprocess.check_output(['git', 'show', REV + ':' + path], cwd=ROOT)
    p = OUT / 'sources' / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(raw)
    bindings.append({'member': 'sources/' + name, 'repositoryPath': path, 'commit': REV,
                     'gitBlobSHA1': subprocess.check_output(['git', 'rev-parse', REV + ':' + path], text=True).strip(),
                     'bytes': len(raw), 'sha256': sha(raw), 'jsonPointers': list(pointers), 'textLocators': list(locators),
                     'representation': 'exact Git blob bytes; text locators use normalized line counting'})
    return json.loads(raw) if name.endswith('.json') else raw.decode()


def esc(s):
    return str(s).replace('~', '~0').replace('/', '~1')


def patch(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = path + '/' + esc(k)
            if k not in a:
                out.append({'op': 'add', 'path': p, 'value': copy.deepcopy(b[k])})
            elif k not in b:
                out += [{'op': 'test', 'path': p, 'value': copy.deepcopy(a[k])}, {'op': 'remove', 'path': p}]
            else:
                out += patch(a[k], b[k], p)
        return out
    if a == b:
        return []
    assert path
    return [{'op': 'test', 'path': path, 'value': copy.deepcopy(a)}, {'op': 'replace', 'path': path, 'value': copy.deepcopy(b)}]


def bounds(pos, box):
    x, y, z = pos
    w, d, h = box
    return [x-w/2, x+w/2, y-d/2, y+d/2, z, z+h]


def distance2(a, b):
    return sum(max(a[2*i]-b[2*i+1], b[2*i]-a[2*i+1], 0)**2 for i in range(3))


OUT.mkdir(parents=True, exist_ok=True)
queue = source('QUEUE404.json', BASE + 'CURRENT_SPELL_QUEUE_404.json', ['/currentAuthority', '/continuingPriorityOrder'])
source('HANDOFF404.json', BASE + 'CURRENT_HANDOFF_404.json')
source('RESIDUAL333.json', R333 + 'RESIDUAL_BRANCH_DISPOSITIONS.json', ['/branches/3'])
source('DECISION333.json', R333 + 'DIRECTOR_DECISION.json', ['/decision', '/residualPartIds'])
proc = source('DECAY285.json', R333 + 'evidence/EXACT_RETURN285_PROCEDURE.json',
              ['/commonProcedure/casting', '/commonProcedure/formation', '/commonProcedure/aura', '/commonProcedure/damage',
               '/commonProcedure/command', '/commonProcedure/clocks', '/commonProcedure/stats', '/spellLocalProcedure/durationIdentity'])
profile = source('W17D.json', R333 + 'evidence/EXISTING_W17D_PROFILE.json',
                 ['/ordinaryLearning/16/selected/4', '/spellbook/57', '/prepared/4', '/characterFoundation/equipment',
                  '/hpMaximum', '/hpFormula', '/rpMaximum', '/automaticCards', '/saves', '/sourceClassBinding'])
profile_n = source('W17N.json', R333 + 'evidence/EXISTING_W17N_PROFILE.json',
                   ['/ordinaryLearning/16/selected/4', '/spellbook/57', '/prepared/4', '/characterFoundation/equipment',
                    '/hpMaximum', '/rpMaximum', '/schoolDC', '/acquisitionLedger/9/choices/1', '/sourceClassBinding'])
ferry = source('FERRY333.json', R333 + 'FERRY_RECONCILIATION.json', ['/nativeUnchanged', '/authorizedExistingLocalCompletion', '/ruling'])
source('FERRY_NATIVE.md', ferry['nativeSourceBinding']['path'], locators=['printed stat block and traits; exact native bytes'])
source('WIZARD.json', 'DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json', ['/cards/17', '/cards/44', '/cards/56', '/cards/57', '/engine/9', '/engine/10', '/engine/11', '/engine/12', '/engine/17'])
source('COMBAT.md', 'DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
       locators=['lines27-70 regular initiative, reaction refresh, ordered markers and periodic arbitration', 'lines115-121 stance choice/expiry/Mobile'])
source('SPELL_INTEGRATION.md', 'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md',
       locators=['lines31-57 paid commitment and Counterspell window'])
source('RULEBOOK.txt', 'docs/reference/Player_Rulebook_v6_source_text.txt',
       locators=['lines8424-8438 strain and no-spell/no-Weave end recovery', 'lines8605-8631 components'])
source('R03_SEAL408.json', BASE + 'summon_avatar_of_decay_r03_mind_blank_witness_408/DIRECTOR_R03_SEAL_408.json')
for mode in ['LARGER', 'TIE_EARLIER', 'TIE_SOURCE_ID', 'SUPPRESSED_HIGHER']:
    source('SH333-AURA-' + mode + '.json', R333 + 'components/SH333-AURA-' + mode + '.json')

raw_archive = Path(sys.argv[1]).read_bytes()
assert sha(raw_archive) == '66ca7f3bc84c96ded94055747841ce767ddd2100f40e289ad13ae3b2e9e5fc21'
with zipfile.ZipFile(sys.argv[1]) as z:
    assert z.testzip() is None
    body_raw = z.read('BODY_PROFILES.json')
    parent_profiles = z.read('ACTOR_PROFILES.json')
    assert json.loads(parent_profiles)['W17D'] == profile
    assert json.loads(parent_profiles)['W17N'] == profile_n
    for name, raw in [('BODY_PROFILES.json', body_raw), ('ACTOR_PROFILES.json', parent_profiles)]:
        (OUT / 'sources' / name).write_bytes(raw)
        bindings.append({'member': 'sources/' + name, 'archiveRepositoryPath': BASE + 'rank9_summonhosts5_return285_received/DD_Rank9_SummonHosts5_Director_Return285_HELD.zip',
                         'commit': REV, 'archiveSHA256': sha(raw_archive), 'archiveBytes': len(raw_archive), 'archiveMember': name,
                         'bytes': len(raw), 'sha256': sha(raw), 'crc32': format(z.getinfo(name).CRC, '08x'),
                         'jsonPointers': ['/SH202-DECAY'] if name.startswith('BODY') else ['/W17D', '/W17N']})
body_profile = json.loads(body_raw)['SH202-DECAY']
write('SOURCE_BINDINGS_409.json', {'revision': REV, 'bindings': bindings})

authorization = {
    'id': 'SH333-R04-AUTHORIZATION-409', 'classification': 'CONDITIONAL_TEST_ONLY',
    'ownerInstruction': 'Proceed with SH333-R04 against main 3ade1339a286add11f669c66800809995a494116. Construct only a source-grounded conditional TEST_ONLY paired paid aura witness; no campaign facts or adopted rules; preserve R01/R02, SH202-B03 and Queue404.',
    'newPremises': ['Distinct hypothetical Wizard17 P instantiates bound W17D; distinct Wizard17 Q instantiates bound W17N. Each independently binds prior acquisition/preparation and its own conditional current resources/equipment. No duplicated W17D or copied actor-state record; no campaign existence claim.',
                    'One hypothetical Ferry F uses the qualified Return333 native/local profile and intact non-operative seal. No control order, undisclosed knowledge or owner is invented.',
                    'Bounded supported empty scene, exact starting positions/item custody, light, absence of suppression/wards, initiative die faces, ordinary voluntary declines and rolled dice are conditional encounter inputs.',
                    'This is a new encounter initial state, not a change to Return285, R03 or any campaign parent. No inherited Opening/Horn/other source clocks exist in this fixture.'],
    'sourceSelection': 'Use the existing held Decay procedure as the governing procedure under test, not as an accepted spell. W17D access and Return333 physical completion are already bound. No rules are adopted.',
    'profileQualification': 'Top-level W17D/W17N hpMaximum104 and classLevel17/hpFormula govern. Preserve stale nested level20 hpChoice122 as provenance. W17N school Necromancy gives DC21; acquired Flesh Ascendant adds34 maximum HP to its one controlled Undead, without healing or two-minion AC/save bonus. Its historical force Arcane Ward label is preserved in source only; Q explicitly selects lawful necrotic after its conditional preparation under cards/57, because prepared Decay supplies necrotic. No rule or source-file repair is made.',
    'sourceByteReconciliation': {'FerryNativeCurrentRepresentation': '4637 LF bytes; SHA256 393a659464c3cbc49c349df5376fb44eeea8d169984e0f3933fc2a125db52895',
                                'HistoricalFerryBinding': '4746 CRLF bytes; SHA256 a6364713e4258c39166903ba11e3c1e8d1bb5eae10ac81483bc7dbf683a5764f',
                                'test': 'Current exact Git bytes converted LF to CRLF reproduce historical byte/hash binding; no semantic source change.'},
    'campaignEvent': False, 'runtimeImplementation': False, 'canonicalPromotion': False,
    'applicationAuthorized': False, 'acceptedIds': [], 'appliedIds': [],
    'endpoint': 'F regular end at 2.80 seconds. Both sources remain live with their original deadlines; no later pulse/expiry is claimed. Reverse audit restores the full new encounter initial state.'}
write('AUTHORIZATION_AND_SCOPE_409.json', authorization)


def actor(k, pos, phase):
    wizard = k != 'F'
    origin = profile if k == 'P' else profile_n if k == 'Q' else None
    hp, speed = (origin['hpMaximum'], origin['speed']) if wizard else (9, 40)
    return {'id': k, 'profileRef': ('sources/' + origin['id'] + '.json#') if wizard else 'sources/FERRY333.json#',
            'sourceIdentity': origin['id'] if wizard else 'FERRY333', 'classLevel': origin['classLevel'] if wizard else None,
            'school': origin['school'] if wizard else None, 'heroPath': origin['heroPath'] if wizard else None,
            'decaySaveDC': (origin['schoolDC'] if origin['school'] == 'Necromancy' else origin['spellDC']) if wizard else None,
            'openingRPBinding': ('sources/' + origin['id'] + '.json#/rpMaximum') if wizard else None,
            'conditional': True, 'plane': 'SH409-TEST-PLANE', 'pos': pos, 'box': [5, 5, 6], 'facing': '+y',
            'type': 'Humanoid' if wizard else 'Undead', 'size': 'Medium', 'massLb': 180 if wizard else 90,
            'hp': hp, 'maxHP': hp, 'tempHP': 0, 'AC': 12 if wizard else 10, 'speed': speed,
            'conditions': [], 'wounds': 0, 'resistances': ['force'] if k == 'P' else ['necrotic'],
            'arcaneWardSelection': ('force' if k == 'P' else 'necrotic') if wizard else None,
            'immunities': [] if wizard else ['poison'], 'conditionImmunities': [] if wizard else ['poisoned'],
            'saveCON': 2, 'nullDealer': False, 'nullRecipient': False, 'dead': False,
            'originalOwner': k, 'controller': k, 'concentration': None,
            'RP': origin['rpMaximum'] if wizard else None, 'Dissonance': 0 if wizard else None, 'Refrain': 0 if wizard else None,
            'lastCast': None, 'preparedFamiliesUsed': [], 'magicThisTurn': False,
            'recharge': {'wizard.base.counterspell': 0} if wizard else {}, 'castHistory': [],
            'voiceAvailable': True, 'hands': {'left': 'focus-' + k if wizard else None, 'right': None},
            'perception': {'ordinarySight': True, 'ordinaryHearing': True, 'observersVisible': ['P', 'Q', 'F'], 'eyeHeight': 5.5},
            'budget': {'Action': 0, 'BonusAction': 0, 'Reaction': 1, 'Movement': 0, 'Interaction': 0},
            'turn': {'active': False, 'phase': phase, 'nextStart': phase, 'nextEnd': phase + 80,
                     'startsConsumed': [], 'endsConsumed': [], 'refreshCount': 0},
            'stance': None, 'stanceExpires': None, 'mobileAllowance': 0,
            'commandEntitlement': {'round': 1, 'commandSpent': False, 'offenseSpent': False},
            'carriedItems': ['focus-' + k, 'book-' + k, 'kit-' + k] if wizard else ['seal-F'],
            'carriedMassLb': 10 if wizard else 0.1, 'load': 1 if wizard else 0.1,
            'capacityLb': 180, 'loadCapacity': 12, 'optionalTechniquesUsed': []}


state = {'id': 'SH333-R04-PAIRED-409', 'classification': 'CONDITIONAL_TEST_ONLY', 'tick': 0,
         'tickUnitSeconds': 0.01, 'worldElapsedSeconds': 0.0, 'round': 1,
         'scene': {'plane': 'SH409-TEST-PLANE', 'bounds': [-100, 100, -100, 100, 0, 30],
                   'floorZ': 0, 'floorCapacityLbPerSqFt': 1000, 'ceilingZ': 30, 'solids': [], 'light': 'bright',
                   'hazards': [], 'wards': [], 'suppressionSources': [], 'outsideActors': []},
         'initiative': [{'actor': 'P', 'die': 18, 'modifier': 2, 'total': 20, 'phase': 0},
                        {'actor': 'Q', 'die': 14, 'modifier': 2, 'total': 16, 'phase': 100},
                        {'actor': 'F', 'die': 10, 'modifier': 2, 'total': 12, 'phase': 200}],
         'actors': {'P': actor('P', [-30, -35, 0], 0), 'Q': actor('Q', [30, -35, 0], 100), 'F': actor('F', [0, 0, 0], 200)},
         'items': {}, 'sources': {}, 'bodies': {}, 'pendingCast': None, 'counterWindows': [],
         'aura': {'checks': [], 'roots': {}, 'settlements': [], 'familyMarkerReceipts': {}, 'duplicateChecks': []},
         'phaseLedger': [], 'commandHistory': [], 'relations': {}, 'hardGuards': {}, 'ownerHistory': [], 'eventHistory': []}
for k in ['P', 'Q']:
    x, y, _ = state['actors'][k]['pos']
    for prefix, mass, offset, box in [('focus', 1, [-0.75, 0.5, 3], [0.25, 0.25, 1]),
                                    ('book', 3, [0, -0.75, 2], [1, 0.5, 1]), ('kit', 6, [0.75, -0.5, 2], [1, 1, 1])]:
        ident = prefix + '-' + k
        state['items'][ident] = {'id': ident, 'custodian': k, 'massLb': mass,
                                 'location': 'leftHand' if prefix == 'focus' else 'carried',
                                 'bounds': bounds([x+offset[0], y+offset[1], offset[2]], box),
                                 'conditionalDimensionsAndMass': True, 'consumed': False,
                                 'contents': ['satchel', 'worn clothing', 'uniform piece', 'map', 'manacles', 'belt pouch with 10gp'] if prefix == 'kit' else [],
                                 'sourceRef': 'sources/' + ('W17D' if k == 'P' else 'W17N') + '.json#/characterFoundation/equipment'}
state['items']['seal-F'] = {'id': 'seal-F', 'custodian': 'F', 'location': 'carried', 'massLb': 0.1,
                           'bounds': [-0.25, 0.25, -0.25, 0.25, 3, 3.1], 'intact': True, 'consumed': False,
                           'contentsKnown': False, 'authorityExercised': False, 'conditionalDimensionsAndMass': True,
                           'sourceRef': 'sources/FERRY333.json#/authorizedExistingLocalCompletion/equipment'}
initial = copy.deepcopy(state)
states = {'S000': copy.deepcopy(state)}
events = []


def emit(kind, tick, mutate=lambda s: None, evidence=None, refs=()):
    global state
    before = copy.deepcopy(state)
    assert tick >= state['tick']
    state['tick'] = tick
    state['worldElapsedSeconds'] = tick / 100
    mutate(state)
    eid = 'SH409:' + str(len(events)+1)
    state['eventHistory'].append({'id': eid, 'kind': kind, 'tick': tick})
    after = copy.deepcopy(state)
    n = len(events)
    forward, inverse = patch(before, after), patch(after, before)
    events.append({'id': eid, 'kind': kind, 'tick': tick, 'beforeStateId': 'S%03d' % n, 'afterStateId': 'S%03d' % (n+1),
                   'beforeSHA256': sha(encode(before)), 'afterSHA256': sha(encode(after)),
                   'forward': forward, 'inverse': inverse,
                   'forwardAbsentPaths': [o['path'] for o in forward if o['op'] == 'add'],
                   'inverseAbsentPaths': [o['path'] for o in inverse if o['op'] == 'add'],
                   'evidence': evidence or {}, 'sourceRefs': list(refs)})
    states['S%03d' % (n+1)] = after


def start(k, tick):
    def mutation(s):
        a = s['actors'][k]
        assert not any(v['turn']['active'] for v in s['actors'].values()) and a['turn']['nextStart'] == tick
        a['stance'] = None
        a['stanceExpires'] = None
        a['mobileAllowance'] = 0
        a['budget'] = {'Action': 1, 'BonusAction': 1, 'Reaction': 1, 'Movement': a['speed'], 'Interaction': 1}
        a['recharge'] = {n: max(0, v-1) for n, v in a['recharge'].items()}
        a['magicThisTurn'] = False
        a['turn']['active'] = True
        a['turn']['nextStart'] = tick + 600
        a['turn']['startsConsumed'].append(tick)
        a['turn']['refreshCount'] += 1
    emit('regularStart', tick, mutation, {'actor': k, 'sequence': ['expiry', 'Reaction/recharge', 'no recovery/death-save due', 'periodic next', 'voluntary decisions last']}, ['sources/COMBAT.md@lines55-70'])
    # Enumerate every extant source against this actor and its original-owner bodies.
    rows = []
    recipients = {k: state['actors'][k], **{b: v for b, v in state['bodies'].items() if v['sourceOwner'] == k}}
    for rid, recipient in recipients.items():
        for sid, src in state['sources'].items():
            if src['bodyId'] == rid:
                continue
            body = state['bodies'][src['bodyId']]
            d2 = distance2(bounds(body['pos'], body['box']), bounds(recipient['pos'], recipient['box']))
            rows.append({'recipient': rid, 'source': sid, 'marker': tick, 'distanceSquared': d2,
                         'inside': d2 <= 100, 'sourceLive': src['active'], 'suppressed': False,
                         'firstFutureMarkerSatisfied': src['formedAt'] < tick, 'lineOfEffect': True})
    emit('regularAuraCoverage', tick, lambda s: s['aura']['checks'].extend(rows), {'actor': k, 'rows': rows}, ['sources/DECAY285.json#/commonProcedure/aura'])


def stance(k, tick):
    def mutation(s):
        a = s['actors'][k]
        a['stance'] = 'Mobile'
        a['stanceExpires'] = a['turn']['nextStart']
        a['mobileAllowance'] = 5
    emit('voluntaryMobileChoice', tick, mutation, {'actor': k, 'movementGranted': 0, 'movementSpent': 0}, ['sources/COMBAT.md@lines115-121'])


def cast(k, tick, anchor):
    other = 'Q' if k == 'P' else 'P'
    profile_member = 'sources/' + ('W17D' if k == 'P' else 'W17N') + '.json'
    sid = k + ':decay:409'
    def commit(s):
        a = s['actors'][k]
        assert a['turn']['active'] and a['budget']['Action'] == 1 and a['RP'] == 64 and a['concentration'] is None
        a['budget']['Action'] = 0
        a['RP'] -= 26
        a['preparedFamiliesUsed'].append(FAMILY)
        a['lastCast'] = FAMILY
        a['magicThisTurn'] = True
        a['concentration'] = sid
        a['castHistory'].append({'source': sid, 'commit': tick, 'family': FAMILY, 'school': 'Necromancy', 'rank': 9,
                                 'paidRP': 26, 'baseDissonance': 0, 'Refrain': 0, 'surcharge': 0,
                                 'firstPreparedFamily': True, 'ActionPaid': 1, 'refunded': 0})
        s['pendingCast'] = {'id': sid, 'caster': k, 'rank': 9, 'school': 'Necromancy', 'paidRP': 26,
                            'anchor': anchor, 'bodyProfile': 'SH202-DECAY', 'facing': '+y',
                            'components': {'V': True, 'S': 'rightFree', 'F': 'focus-' + k},
                            'rangeFeetGrid': 35, 'wholeBodyFit': True, 'LoE': True, 'formationDeadlineIfSuccessful': tick+10+6000}
    emit('castCommit', tick, commit, {'actor': k, 'source': sid, 'declarationPrecedesPayment': True, 'noPriorConcentration': True,
                                    'profileAccess': [profile_member+'#/ordinaryLearning/16/selected/4', profile_member+'#/spellbook/57', profile_member+'#/prepared/4']},
         ['sources/DECAY285.json#/commonProcedure/casting', 'sources/WIZARD.json#/engine/11', 'sources/SPELL_INTEGRATION.md@lines31-40'])
    rows = [{'actor': k, 'eligible': 'UNADJUDICATED', 'decision': 'TEST_ONLY_NO_ATTEMPT', 'selfCounterProhibitionAsserted': False, 'costRP': 0, 'reactionSpent': 0},
            {'actor': other, 'eligible': True, 'decision': 'TEST_ONLY_DECLINE', 'source': 'sources/WIZARD.json#/cards/17',
             'acquisition': 'automatic Wizard2; always-prepared class matrix', 'gridDistanceFeet': 60,
             'perceived': True, 'lineOfEffect': True, 'V': True, 'S': 'rightFree', 'F': 'focus-' + other,
             'ReactionAvailable': 1, 'RPAvailable': state['actors'][other]['RP'], 'baseCostRP': 3,
             'Dissonance': 0, 'limit': 13, 'surcharge': 0, 'recharge': 0, 'costRP': 0, 'reactionSpent': 0},
            {'actor': 'F', 'eligible': False, 'reason': 'No Counterspell spell/class capability in bound Ferry profile', 'costRP': 0, 'reactionSpent': 0}]
    for bid in state['bodies']:
        rows.append({'actor': bid, 'eligible': False, 'reason': 'Generated body has no spell repertoire or independent Reaction', 'costRP': 0, 'reactionSpent': 0})
    emit('counterspellWindow', tick+1, lambda s: s['counterWindows'].append({'pendingSource': sid, 'rows': rows}),
         {'rows': rows, 'pendingSpellRank': 9, 'checkDCIfAttempted': 28, 'allDecisionsCostFree': True}, ['sources/WIZARD.json#/cards/17', 'sources/DECAY285.json#/commonProcedure/command'])
    def formation(s):
        bid = sid + ':body'
        s['sources'][sid] = {'id': sid, 'owner': k, 'family': FAMILY, 'class': 'Wizard', 'rank': 9, 'school': 'Necromancy',
                             'formedAt': tick+10, 'deadline': tick+10+6000, 'active': True, 'suppressed': False,
                             'bodyId': bid, 'anchor': s['actors'][k]['pos'][:], 'paidRP': 26, 'durationSeconds': 60,
                             'concentrationOwner': k, 'sourceProfile': profile_member+'#'}
        s['bodies'][bid] = {'id': bid, 'profile': 'SH202-DECAY', 'source': sid, 'sourceOwner': k, 'controller': k,
                           'pos': anchor, 'box': body_profile['box'], 'massLb': 900, 'plane': 'SH409-TEST-PLANE', 'facing': '+y',
                           'hp': 250, 'maxHP': 284 if k == 'Q' else 250, 'tempHP': 0, 'AC': 15, 'walk': 30, 'saveBonus': 6,
                           'saveDC': s['actors'][k]['decaySaveDC'],
                           'type': 'Undead', 'size': 'Large', 'conditions': [], 'resistances': [], 'immunities': [],
                           'active': True, 'suppressed': False, 'nullDealer': False, 'cargo': [],
                           'conjurationBonusHP': 0, 'fleshAscendantBonusHP': 34 if k == 'Q' else 0,
                           'maxHPIncreaseHealing': 0, 'controlledUndeadCount': 1,
                           'nextPassiveOwnerMarker': s['actors'][k]['turn']['nextStart'],
                           'nextAttachedPhase': tick+71, 'phaseActive': False, 'movementRemaining': 0, 'offensiveActionUsed': False,
                           'dodge': False, 'ordinaryReaction': 0, 'command': None, 'ownRegularTurn': False}
        s['pendingCast'] = None
    emit('formation', tick+10, formation, {'source': sid, 'anchor': anchor, 'noCreationPulse': True,
                                          'noCommandOrControlRelation': True, 'eligibilityRechecked': True, 'noCostsRefunded': True},
         ['sources/DECAY285.json#/commonProcedure/formation', 'sources/DECAY285.json#/commonProcedure/stats', 'sources/BODY_PROFILES.json#/SH202-DECAY', 'sources/WIZARD.json#/cards/44'])


def end(k, tick):
    def mutation(s):
        a = s['actors'][k]
        assert a['turn']['active'] and a['turn']['nextEnd'] == tick
        if a['Dissonance'] is not None and not a['magicThisTurn']:
            a['Dissonance'] = max(0, a['Dissonance']-1)
        for wallet in ['Action', 'BonusAction', 'Movement', 'Interaction']:
            a['budget'][wallet] = 0
        a['turn']['active'] = False
        a['turn']['endsConsumed'].append(tick)
        a['turn']['nextEnd'] += 600
    emit('regularEnd', tick, mutation, {'actor': k, 'noDueDamageOrSave': True, 'ReactionRetained': True, 'stancePersistsUntilNextOwnStart': True},
         ['sources/COMBAT.md@lines55-70', 'sources/RULEBOOK.txt@line8438'])


def companion(k, tick):
    bid = k + ':decay:409:body'
    def opening(s):
        b = s['bodies'][bid]
        assert not s['actors'][k]['turn']['active'] and b['nextAttachedPhase'] == tick
        b['phaseActive'] = True
        b['movementRemaining'] = 30
        b['dodge'] = True
        s['phaseLedger'].append({'body': bid, 'opened': tick, 'command': None, 'behavior': 'uncommanded Dodge, no movement', 'offenseUsed': False, 'ordinaryActorRefresh': False})
    emit('companionPhaseOpen', tick, opening, {'body': bid, 'noAuraPulse': True}, ['sources/DECAY285.json#/commonProcedure/command'])
    def closing(s):
        b = s['bodies'][bid]
        b['phaseActive'] = False
        b['movementRemaining'] = 0
        b['nextAttachedPhase'] += 600
        s['phaseLedger'][-1]['closed'] = tick+1
        s['phaseLedger'][-1]['unusedMovementExpired'] = 30
    emit('companionPhaseClose', tick+1, closing, {'body': bid, 'noActorRefresh': True}, ['sources/DECAY285.json#/commonProcedure/clocks'])


start('P', 0)
stance('P', 5)
cast('P', 10, [-10, 0, 0])
end('P', 80)
companion('P', 81)
start('Q', 100)
stance('Q', 105)
cast('Q', 110, [10, 0, 0])
end('Q', 180)
companion('Q', 181)
start('F', 200)


def allocate(s):
    pools = [('P:decay:409', [3, 4]), ('Q:decay:409', [5, 6])]
    for sid, dice in pools:
        rid = sid + ':F:start200'
        s['aura']['roots'][rid] = {'id': rid, 'source': sid, 'dealer': sid+':body', 'recipient': 'F', 'marker': 200,
                                  'family': FAMILY, 'dice': dice, 'raw': sum(dice), 'suppressed': False,
                                  'formedAt': s['sources'][sid]['formedAt'], 'dealerNullAtCreation': False,
                                  'consumed': True, 'winner': sid.startswith('Q'), 'settled': False}
    s['aura']['familyMarkerReceipts']['F:200:' + FAMILY] = {'marker': 200, 'recipient': 'F', 'winner': 'Q:decay:409:F:start200',
                                                         'rootIds': [sid+':F:start200' for sid, _ in pools],
                                                         'consumed': True, 'loserDeferred': False}


emit('pairedAuraArbitration', 200, allocate,
     {'rolledPools': {'P:decay:409': [3, 4], 'Q:decay:409': [5, 6]}, 'order': 'highest unsuppressed raw pool, earlier formation, source ID',
      'winner': 'Q:decay:409', 'bothOpportunitiesConsumed': True, 'damageBeforeDefense': 11}, ['sources/DECAY285.json#/commonProcedure/aura'])


def settle(s):
    a = s['actors']['F']
    a['hp'] -= 5
    s['aura']['roots']['Q:decay:409:F:start200']['settled'] = True
    s['aura']['settlements'].append({'root': 'Q:decay:409:F:start200', 'recipient': 'F', 'save': {'ability': 'CON', 'd20': 18, 'modifier': 2, 'total': 20, 'DC': 21, 'success': False},
                                    'raw': 11, 'afterSave': 11, 'resistance': 'necrotic', 'afterResistance': 5,
                                    'tempHPBefore': 0, 'hpBefore': 9, 'hpAfter': 4, 'damageType': 'necrotic',
                                    'concentrationCheck': 'none: recipient not concentrating', 'newZeroOrWound': False,
                                    'itemDamage': False, 'ownerProc': False, 'rootCount': 1})


emit('winningAuraSaveDefenseSettlement', 200, settle, {'noSaveOrDamageForLosingRoot': True, 'noControlGuardUse': True},
     ['sources/DECAY285.json#/commonProcedure/aura', 'sources/DECAY285.json#/commonProcedure/damage', 'sources/FERRY333.json#/nativeUnchanged'])
stance('F', 205)
emit('duplicateMarkerObservation', 210, lambda s: s['aura']['duplicateChecks'].append(
    {'recipient': 'F', 'marker': 200, 'receipt': copy.deepcopy(s['aura']['familyMarkerReceipts']['F:200:' + FAMILY]),
     'damageAdded': 0, 'rollsAdded': 0, 'rootsAdded': 0, 'recordOnly': True}),
     {'recordOnly': True, 'noInWorldActionOrTimeBudget': True, 'lostOpportunityNotBanked': True}, ['sources/DECAY285.json#/commonProcedure/aura'])
end('F', 280)
write('INITIAL_409.json', initial)
write('SNAPSHOTS_409.json', states)
write('EVENTS_409.json', events)
write('EXPECTED_TERMINAL_409.json', {'terminalStateId': 'S%03d' % len(events), 'terminalSHA256': sha(encode(state)),
                                   'initialSHA256': sha(encode(initial)), 'casterRP': {'P': 38, 'Q': 38}, 'recipientHP': 4,
                                   'sourceDeadlines': {'P:decay:409': 6020, 'Q:decay:409': 6120},
                                   'firstFutureRecipientStart': 200, 'nextRecipientStart': 800,
                                   'scope': 'R04 only; finite observation ends before the next due regular marker. No future pulse or expiry is assumed.',
                                   'acceptedIds': [], 'appliedIds': [], 'heldIds': [FAMILY], 'applicationAuthorized': False})
print(json.dumps({'events': len(events), 'snapshots': len(states), 'sourceBindings': len(bindings), 'terminalSHA256': sha(encode(state))}))
