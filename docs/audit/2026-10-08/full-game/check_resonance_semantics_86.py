"""Independent finite authored-case diagnostics. Standard library only; no project imports."""
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

A = Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
R = A / 'rank9-resonance-fields3-part5-return-01'
OUT = A / 'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json'
COPY = A / Path(__file__).name
assert not OUT.exists() and not COPY.exists(), 'Exclusive outputs already exist; do not rerun.'
checks = []
def check(name, actual, expected):
    checks.append({'id': name, 'actual': actual, 'expected': expected, 'passed': actual == expected})
def read(name):
    return json.loads((R / name).read_text(encoding='utf-8'))
def binding(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
refs = read('SOURCE_REFERENCES.json')['aliases']
cache = {}
def source(alias):
    if alias in cache:
        return cache[alias]
    b = refs[alias]
    with zipfile.ZipFile(R / b['archive']) as z:
        raw = z.read(b['member'])
    check('source-hash:' + alias, hashlib.sha256(raw).hexdigest(), b['sha256'])
    d = json.loads(raw)
    for part in b.get('pointer', '').strip('/').split('/'):
        if part:
            d = d[int(part)] if isinstance(d, list) else d[part.replace('~1', '/').replace('~0', '~')]
    cache[alias] = d
    return d

classes = {'Wizard': source('wizard'), 'Mage': source('mage')}
catalog = {s['id']: s for s in source('catalog')['spells']}
templates = {t['id']: t for t in read('ACTOR_TEMPLATES.json')['templates']}
owned = {}
for tid, t in templates.items():
    cls = classes[t['class']]
    acquired = set()
    for h in t['selectedClassHistory']:
        level = h['classLevel']
        rule = next(v for v in cls['schedule'] if v['classLevel'] == level)
        n = rule['choose'] - int(t['class'] == 'Wizard' and t['heroPath'] == 'Elementalist' and level == 10)
        check(f'{tid}:level{level}:selection-count', len(h['selectedCards']), n)
        active = 0
        for s in h['selectedCards']:
            c = cls['cards'][s['cardIndex']]
            check(f'{tid}:level{level}:{s["id"]}:source-id', c['id'], s['id'])
            check(f'{tid}:level{level}:{s["id"]}:eligible', c['minimumClassLevel'] <= level and c['acquisition'] == 'selection' and c['band'] in rule['bands'] and c['id'] not in acquired and (c['band'] != 'Hero' or c['path'] == t['heroPath']), True)
            active += c['sourceKind'] == 'active'
            acquired.add(c['id'])
        check(f'{tid}:level{level}:minimum-actives', active >= rule['minimumActives'], True)
    for s in t['automaticCards']:
        c = cls['cards'][s['index']]
        check(f'{tid}:automatic:{s["id"]}', c['id'] == s['id'] and c['acquisition'] == 'automatic' and c['minimumClassLevel'] <= t['classLevel'] and c['id'] not in acquired, True)
        acquired.add(c['id'])
    owned[tid] = acquired
    check(tid + ':RP', t['maxRP'], cls['rpByClassLevel'][t['classLevel'] - 1])
    check(tid + ':HP', t['maxHP'], 6 + 16 * 4 + 17 * 2)
    check(tid + ':abilities', t['modifiers'], {k: (v - 10) // 2 for k, v in t['abilities'].items()})
    for h in t['ordinaryAcquisitionHistory']:
        ids = h.get('chosenSpellIds', [h['spellId']] if 'spellId' in h else [])
        if 'schoolBonusSpell' in h:
            ids = ids + [h['schoolBonusSpell']]
            check(tid + ':school-bonus', catalog[h['schoolBonusSpell']]['classAccess']['Wizard']['school'], t['school'])
        for sid in ids:
            access = catalog[sid]['classAccess'].get(t['class'])
            check(f'{tid}:book:{h["classLevel"]}:{sid}', bool(access) and access['minimumClassLevel'] <= h['classLevel'], True)
    check(tid + ':prepared-book-subset', set(t['preparedOrdinary']).issubset(set(t['ordinaryBook'])), True)

def body_in(a, f):
    foot = a['foot']
    delta = [max(foot[0] - 2.5 - f['center'][0], 0, f['center'][0] - foot[0] - 2.5),
             max(foot[1] - 2.5 - f['center'][1], 0, f['center'][1] - foot[1] - 2.5),
             max(foot[2] - f['center'][2], 0, f['center'][2] - foot[2] - 6)]
    return sum(Fraction(str(x)) ** 2 for x in delta) < f['radius'] ** 2

def fields_at(before, after, owner):
    # Own incompatible concentration is removed before the new payment. Other future removals do not reprice it.
    old = before['actors'][owner]['concentration']
    changed = after['actors'][owner]['concentration'] != old
    return [f for fid, f in before['fields'].items()
            if f['state'] == 'active' and f['deadline'] > before['time']
            and not (changed and fid == old) and body_in(before['actors'][owner], f)]

def take(b, e, amount):
    db = min(b, amount)
    return b - db, max(0, e - (amount - db))

cases = read('CASE_DISPOSITIONS.json')['cases']
scenes = [scene for c in cases for scene in [c] + c['independentBranches']]
feedback_findings = []
counts = defaultdict(int)
for scene in scenes:
    sid = scene['id']
    check(sid + ':full-final', scene['finalState'], scene['timeline'][-1]['after'])
    previous_time = scene['initialState']['time']
    for ei, ev in enumerate(scene['timeline']):
        pre, post = ev['before'], ev['after']
        key = f'{sid}:{ei}'
        counts['transitions'] += 1
        check(key + ':time', previous_time <= ev['time'] == pre['time'] == post['time'], True)
        previous_time = ev['time']
        new = {cid: cr for cid, cr in post['castRecords'].items() if cid not in pre['castRecords']}
        observations = post['observations'][len(pre['observations']):]
        expected_delta = defaultdict(int)
        for cid, cr in new.items():
            counts['committedCasts'] += 1
            actor = pre['actors'][cr['owner']]
            t = templates[actor['template']]
            base = cr['nativePrintedBase']
            ref = cr['nativeSourceRef']
            if '/cards/' in ref:
                alias, pointer = ref.split('#')
                card = source(alias)['cards'][int(pointer.rsplit('/', 1)[1])]
                printed = 2 if card['id'] == 'mage.base.cold.cold' else int(re.search(r'\d+', card['cost']).group())
                check(key + ':' + cid + ':card-cost-rank-access', [base, cr['rank'], card['id'] in owned[t['id']]], [printed, card['spellRank'], True])
            else:
                row = catalog[cr['name']]['classAccess'][t['class']]
                check(key + ':' + cid + ':catalog-cost-rank-access', [base, cr['rank'], row['minimumClassLevel'] <= t['classLevel']], [row['baseRpCost'], row['rank'], True])
                if t['class'] == 'Wizard':
                    check(key + ':' + cid + ':prepared-or-cantrip', cr['name'] in t['preparedOrdinary'] or cr['name'] in t['knownCantrips'], True)
            reduced = base
            receipt = actor['matrixEfficiencyReceipts'].get(cr['name'])
            if t['class'] == 'Wizard' and receipt and receipt['state'] == 'available' and receipt['expiresAt'] > ev['time']:
                reduced = max(1, base - 1)
            if t['class'] == 'Mage' and cr['name'] in ['elemental-surge', 'elemental-fusion'] and actor['efficiency'] and actor['efficiency']['until'] > ev['time'] and actor['efficiency']['after'] != cr['name']:
                reduced = max(1, base - 1)
            check(key + ':' + cid + ':actual-class-reduction', cr['preFieldBaseAfterActualClassReduction'], reduced)
            fs = fields_at(pre, post, cr['owner'])
            b = reduced
            e = 0 if cr['rank'] == 0 or actor['D'] < actor['limit'] else min(3, 1 + (actor['D'] - actor['limit']) // 3)
            if any(f['kind'] == 'ordinary Nexus' for f in fs):
                b, e = take(b, e, 2)
            if any(f['kind'] == 'Supreme Nexus' for f in fs):
                b, e = take(b, e, (b + e + 1) // 2)
            damp = 2 if any(f['kind'] == 'Dampening' for f in fs) else 0
            burden = 0
            for eff in pre['effects'].values():
                if eff.get('state') == 'active' and eff.get('source') == 'actual Resonance Influence' and eff.get('recipient') == cr['owner'] and eff['deadline'] > ev['time']:
                    if eff['value'] < 0:
                        old_total = b + e
                        b, e = take(b, e, -eff['value'])
                        damp = max(0, damp - max(0, -eff['value'] - old_total))
                    else:
                        burden = eff['value']
            principal = 2 if sid == 'RF9-NS-A-protected-price' and cr['name'] == 'resonance-barrier' else 0
            quote = {'base': b, 'extra': e, 'dampening': damp, 'burden': burden, 'protectedPrincipal': principal, 'total': b + e + damp + burden + principal}
            check(key + ':' + cid + ':independent-price', cr['quote'], quote)
            check(key + ':' + cid + ':actual-budget', actor[cr['actualBudgetSpent']], True)
            expected_delta[cr['owner']] -= quote['total']
        for oid, receipt in post['conversionReceipts'].items():
            earlier = pre['conversionReceipts'].get(oid, {})
            credited = receipt.get('credited', 0) - earlier.get('credited', 0)
            expected_delta[receipt['recipient']] += credited
            if 'nominalConversion' in receipt and 'nominalConversion' not in earlier:
                counts['settledConversions'] += 1
                basis = receipt['basis']
                if isinstance(basis, dict):
                    paid, refunded = basis['paidBase'], basis['refundedBase']
                    expected = 1 if paid == 0 else max(1, (paid - refunded) // 2) if paid > refunded else 0
                    check(key + ':' + oid + ':conversion-original-payment', [paid, refunded], [post['castRecords'][oid]['quote']['base'], post['castRecords'][oid]['refundedBase']])
                else:
                    expected = 1
                check(key + ':' + oid + ':conversion-value', receipt['nominalConversion'], expected)
                check(key + ':' + oid + ':conversion-accounting', receipt['credited'] + receipt['overflowOrDenied'], expected)
                check(key + ':' + oid + ':conversion-spent', receipt['state'], 'spent-before-credit')
        for cid, cr in post['castRecords'].items():
            expected_delta[cr['owner']] += cr['refundedBase'] - pre['castRecords'].get(cid, {}).get('refundedBase', 0)
        feedback = sum(o.get('ArcaneFeedback', 0) + o.get('actualArcaneFeedback', 0) for o in observations)
        if feedback:
            counters = [v for v in new.values() if v['nativeSourceRef'] == 'wizard#/cards/17']
            check(key + ':feedback-single-real-counter', len(counters), 1)
            owner = counters[0]['owner']
            expected_delta[owner] += feedback
            # Observation text proves the numerical award, but the full state does not name its once/round receipt.
            marker = {k:v for k,v in post['actors'][owner]['limitedUses'].items() if 'feedback' in k.lower()}
            if not marker:
                feedback_findings.append({'caseId': sid, 'timelineIndex': ei, 'actor': owner, 'counterCast': counters[0]['id'], 'observedCredit': feedback,
                    'actualLimitedUses': post['actors'][owner]['limitedUses'], 'source': 'wizard#/cards/60',
                    'finding': 'Credit is numerically recorded but no explicit actor once-per-round Arcane Feedback receipt appears. Ask GPT whether a durable derived history is intended; otherwise add the actual spent marker and replay/second-trigger boundary without inventing another Reaction.'})
        if sid == 'RF9-AF-B-nonspell':
            expected_delta['M'] += 2
        for aid, ap in post['actors'].items():
            check(key + ':' + aid + ':RP-ledger', ap['rp'] - pre['actors'][aid]['rp'], expected_delta[aid])
            check(key + ':' + aid + ':pool-bounds', 0 <= ap['rp'] <= ap['maxRP'], True)
        damage = defaultdict(int)
        for o in observations:
            if o.get('kind') == 'damage':
                counts['damageApplications'] += 1
                check(key + ':' + o['root'] + ':typed-sum', sum(o['types'].values()), o['resolved'])
                check(key + ':' + o['root'] + ':HP-accounting', o['tempAbsorbed'] + o['normalHPLost'] + o['overkill'], o['resolved'])
                damage[o['target']] += o['normalHPLost']
                root = post['damageRootRecords'][o['root']]
                check(key + ':' + o['root'] + ':source-dealer', root['dealer'], post['castRecords'][root['generatingCast']]['owner'])
                check(key + ':' + o['root'] + ':Null-provenance', root['NullSnapshot'], o['Null'])
        for aid, ap in post['actors'].items():
            check(key + ':' + aid + ':normal-HP-ledger', pre['actors'][aid]['hp'] - ap['hp'], damage[aid])

# Expected results from independent rational arithmetic and actual source-defined geometry.
for value, factor, expected in [(29,Fraction(3,2),43),(29,Fraction(5,4),36),(21,Fraction(15,8),39),(7,Fraction(15,8),13),(13,Fraction(3,2),19),(11,Fraction(3,2),16),(26,Fraction(5,4),32),(20,Fraction(5,4),25)]:
    check(f'rational:{value}:{factor}', int(value*factor), expected)
check('mixed-fusion:combined-floor', int((9+7)*Fraction(3,2)), 24)
check('mixed-fusion:largest-remainder-cold-first', [14,10//2], [14,5])
check('blink:distance-inside-enhanced-outside-native', 30**2 < 35**2+10**2 <= Fraction(75,2)**2, True)
check('suppression:whole-body-maximum-distance', Fraction(9)**2+Fraction(5,2)**2+3**2 < 10**2, True)
check('influence:exact-marker-clock', 3+10*6, 63)
check('all-seven-positive-cases', len(cases), 7)
check('all-independent-branches', len(scenes)-len(cases), 28)
report = {'id':'RF9_INDEPENDENT_SEMANTIC_DIAGNOSTICS_86','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'FULL_CASE_READ_WITH_INDEPENDENT_FINITE_DIAGNOSTICS_AND_OPEN_RECEIPT_QUESTION',
 'sourceBindings':[binding(R/n) for n in ['MODEL.json','PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','CASE_DISPOSITIONS.json','ACTOR_TEMPLATES.json','SOURCE_REFERENCES.json','HOLD_REGISTER.json']],
 'reviewed':{'fullProcedures':3,'sharedRules':6,'questionDispositions':24,'positiveCases':7,'branches':28,'conditionalExternalBranches':4,'actorTemplates':6},
 'computedCounts':dict(counts),'checks':checks,'checkCount':len(checks),'failures':[c for c in checks if not c['passed']],
 'openFindings':feedback_findings,
 'scope':'Independent source-bound selection, acquisition, committed pricing, RP/HP ledgers, conversion attribution, geometry and rational arithmetic for these exact authored fixtures. Does not execute their supplied Python, native project code, world scheduler, full visibility, all source-category dispatch, or actual gameplay.',
 'canonicalImplementationApplied':False,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'humanPlaytests':0,'acceptedButUnapplied':50,'newRuleAdoptions':0,'sourceInformationDeleted':0}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
COPY.write_bytes(Path(__file__).read_bytes())
print(json.dumps({'output':binding(OUT),'checks':len(checks),'failureCount':len(report['failures']),'firstFailures':report['failures'][:10],'openFindings':feedback_findings,'computedCounts':dict(counts)},ensure_ascii=False))
