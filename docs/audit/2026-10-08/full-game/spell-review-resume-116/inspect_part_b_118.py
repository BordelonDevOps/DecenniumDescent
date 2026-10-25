"""Fresh read-only inspection of delivered JSON; never imports its code or runs cases."""
import copy, hashlib, json, math
from pathlib import Path

A = Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
P = A / 'rank7-mechanics16-partB-118'
PA = A / 'rank7-mechanics16-partA-117'
O = A / 'spell-review-resume-116'
def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
checks = []
def check(label, result, detail=None):
    checks.append(dict(check=label, passed=bool(result), detail=detail))
def pointer(obj, path):
    for key in path.strip('/').split('/'):
        obj = obj[int(key)] if isinstance(obj, list) else obj[key.replace('~1','/').replace('~0','~')]
    return obj

m, oldm = read(P/'MODEL_PART_B.json'), read(PA/'MODEL_PART_A.json')
cb = read(P/'CASEBOOK_PART_B.json')
for key in ['procedures','sharedRules','questionDispositions']:
    check('Literal preservation '+key, m[key] == oldm[key])
check('Model mirrors delivered casebook', m['currentCasesPartB'] == cb['cases'])
cases = [item for c in cb['cases'] for item in [c,*c['independentBranches']]]
byid = {c['id']:c for c in cases}
check('Delivered counts', (len(cb['cases']),len(cases),sum(len(c['timeline']) for c in cases)) == (8,13,71))
events = {(c['id'],e['id']):e for c in cases for e in c['timeline']}
for c in cases:
    previous = c['initialState']
    for e in c['timeline']:
        tag = c['id']+'/'+str(e['index'])
        check(tag+' full state continuity', previous == e['before'])
        check(tag+' event clock', e['time'] >= previous['time'] and e['after']['time'] == e['time'])
        # Verify delivered scheduled snapshots connect; this is not a turn runner.
        actors = copy.deepcopy(e['before']['actors'])
        chain_ok = True
        for s in e['scheduledProcessing']:
            aid = s['actor']
            chain_ok &= actors[aid] == s['beforeActor']
            actors[aid] = s['afterActor']
            if s['event'] in ['nextSTART','nextEND']:
                before, after = s['beforeActor'], s['afterActor']
                check(tag+f' scheduled {aid} {s["time"]} '+s['event'],
                      abs(before[s['event']]-s['time']) < 1e-7 and
                      abs(after[s['event']]-s['time']-6) < 1e-7)
                if s['event']=='nextEND':
                    check(tag+f' idle strain {aid} {s["time"]}',
                          after['Dissonance'] == (before['Dissonance'] if before['turnHadMagic'] else max(0,before['Dissonance']-1)))
        check(tag+' scheduled snapshot chain', chain_ok and actors == e['stateAtEventAfterScheduledProcessing']['actors'])
        for aid,a in e['after']['actors'].items():
            check(tag+' actor bounds '+aid, 0<=a['HP']<=a['effectiveMaxHP']<=a['maxHP'] and 0<=a['RP']<=a['maxRP'] and a['tempHP']>=0 and a['Dissonance']>=0)
        # Every new damage receipt must account for the aggregate actual HP delta.
        pre=e['stateAtEventAfterScheduledProcessing'];post=e['after']
        nd=[r for k,r in post['receipts']['damage'].items() if k not in pre['receipts']['damage']]
        for aid,a in post['actors'].items():
            dr=[r for r in nd if r['recipient']==aid]
            check(tag+' damage delta '+aid, pre['actors'][aid]['HP']-a['HP']==sum(r['normalHPLost'] for r in dr) and pre['actors'][aid]['tempHP']-a['tempHP']==sum(r['tempAbsorbed'] for r in dr))
        previous=e['after']
    check(c['id']+' final complete state', previous==c['expectedFinalState'])

n=read(P/'NUMERICAL_STATE_EVIDENCE.json')
for item in n['castingTransactions']:
    r=item['receipt'];e=events[item['case'],item['event']];pre=e['stateAtEventAfterScheduledProcessing']['actors'][r['owner']];post=e['after']['actors'][r['owner']]
    tag=item['case']+' cast '+r['id']
    check(tag+' receipt in actual state',r==e['after']['receipts']['casts'][r['id']])
    check(tag+' payment/budget',r['RPBefore']-r['paidBase']-r['additionalRP']==r['RPAfter']==post['RP'] and pre['RP']==r['RPBefore'] and pre[r['budget']] and not post[r['budget']])
    check(tag+' strain',r['DissonanceBefore']+r['baseDissonance']+r['RefrainAdded']==r['DissonanceAfter']==post['Dissonance'])
    check(tag+' availability',pre['regularTurnActive'] or r['budget']=='reaction')
for item in n['damageApplications']:
    r=item['receipt'];e=events[item['case'],item['event']];tag=item['case']+' damage '+r['id']
    check(tag+' bound receipt',r==e['after']['receipts']['damage'][r['id']])
    raw=sum(r['dice']); half=raw//2 if r['saveHalf'] else raw;resolved=half//2 if r['resistanceApplied'] else half
    check(tag+' pool arithmetic', all(1<=x<=r['dieSides'] for x in r['dice']) and raw==r['raw'] and half==r['afterSave'] and resolved==r['resolvedDamage'])
    absorb=min(r['tempBefore'],resolved);normal=resolved-absorb
    check(tag+' HP accounting',absorb==r['tempAbsorbed'] and r['tempAfter']==r['tempBefore']-absorb and normal==r['postTempDamage'] and r['normalHPAfter']==max(0,r['normalHPBefore']-normal) and r['normalHPLost']==min(r['normalHPBefore'],normal) and r['overkill']==max(0,normal-r['normalHPBefore']))
for item in n['binarySaves']:
    r=item['save'];e=events[item['case'],item['event']];a=e['stateAtEventAfterScheduledProcessing']['actors'][r['actor']]
    check(item['case']+' save '+item['event']+'/'+r['actor'],1<=r['die']<=20 and r['modifier']==a['saveBonuses'][r['ability']] and r['die']+r['modifier']==r['total'] and r['success']==(r['total']>=r['DC']))
for item in n['attackRolls']:
    r=item['attack'];t=r['d20']+r['INT']+r['PB']+r['schoolBonus'];hit=r['d20']!=1 and (r['d20']==20 or t>=r['AC'])
    check(item['case']+' attack '+item['event'], t==r['total'] and hit==r['hit'] and r['critical']==(r['d20']==20) and r['actualDiceCount']==(8 if r['critical'] else 4 if hit else 0))

# Exact reversible patch, into new audit-only files.
patch=read(P/'PART_A_REPLACEMENTS.json');out=A/'rank7-mechanics16-partA-corrected-118';out.mkdir(exist_ok=True)
copies={v['file']:read(PA/v['file']) for v in patch['completeFileBindings']}
original=copy.deepcopy(copies)
for op in patch['operations']:
    obj=copies[op['targetMemberInOriginalPartA']];parentpath,key=op['pointer'].rsplit('/',1);parent=pointer(obj,parentpath);key=int(key) if isinstance(parent,list) else key
    before=pointer(patch,op['beforeRef']);after=pointer(patch,op['afterRef'])
    check('Exact patch before '+op['targetMemberInOriginalPartA']+op['pointer'],parent[key]==before)
    parent[key]=copy.deepcopy(after)
for b in patch['completeFileBindings']:
    raw=(PA/b['file']).read_bytes();new=(json.dumps(copies[b['file']],ensure_ascii=False,indent=2)+'\n').encode()
    check('Original patch file '+b['file'],len(raw)==b['beforeBytes'] and sha(raw)==b['beforeSha256'])
    check('Corrected exact bytes '+b['file'],len(new)==b['virtualAfterBytes'] and sha(new)==b['virtualAfterSha256'])
    (out/b['file']).write_bytes(new)
for op in reversed(patch['operations']):
    obj=copies[op['targetMemberInOriginalPartA']];parentpath,key=op['pointer'].rsplit('/',1);parent=pointer(obj,parentpath);key=int(key) if isinstance(parent,list) else key;parent[key]=copy.deepcopy(pointer(patch,op['beforeRef']))
check('Reverse six edits restores both original full objects',copies==original)

report=dict(id='PART_B_LOCAL_INDEPENDENT_REVIEW_118',scope='Fresh inspection of actual delivered Part B JSON and focused Part A replacements; no code from packet executed, no historical case runner rerun.',partBZipSha256='a40790182f2f205b828d28cb5d956bc3f82a0de6717e75ed45dfe6b3707a00c9',mainCases=8,branches=5,events=71,checks=checks,passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),semanticReviewComplete=False,newAcceptedIdentities=[],canonicalApplied=False)
(O/'PART_B_LOCAL_INDEPENDENT_REVIEW_118.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
print('FAILURES',json.dumps([x for x in checks if not x['passed']],indent=2))
