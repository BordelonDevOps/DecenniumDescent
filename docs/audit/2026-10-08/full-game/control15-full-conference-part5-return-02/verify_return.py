"""Read-only archive/source/replay/preservation verifier for this review return.

No project engine is imported; no repository, index, registry or production flag
is written. --report writes ONLY the explicitly named verification report.
Run the isolated unit specifications separately; neither is a game-engine test.
"""
from __future__ import annotations
import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

BASE = Path(__file__).resolve().parent
CANDIDATE = 'DescentReviewChanges/ReviewBible/data/director/spell_proposals/control_15_current_12.json'
PREFIX = 'DescentReviewChanges/ReviewBible/'
checks = []

def digest(b):
    return hashlib.sha256(b).hexdigest()

def canon(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def load(rel):
    return json.loads((BASE / rel).read_bytes())

def check(category, name, condition):
    checks.append({'category': category, 'name': name, 'pass': bool(condition)})
    if not condition:
        raise AssertionError(f'{category}: {name}')

def get(obj, pointer):
    for raw in pointer.lstrip('/').split('/') if pointer else []:
        k = raw.replace('~1','/').replace('~0','~')
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    return obj

def setvalue(obj, pointer, value, remove=False):
    bits = pointer.lstrip('/').split('/')
    parent = obj
    for raw in bits[:-1]:
        k = raw.replace('~1','/').replace('~0','~')
        parent = parent[int(k)] if isinstance(parent,list) else parent[k]
    k = bits[-1].replace('~1','/').replace('~0','~')
    if isinstance(parent,list):
        if remove:
            parent.pop(int(k))
        else:
            parent[int(k)] = copy.deepcopy(value)
    elif remove:
        del parent[k]
    else:
        parent[k] = copy.deepcopy(value)

def apply(obj, ops, reverse=False, record=True, label='plan'):
    obj = copy.deepcopy(obj)
    for i, op in enumerate(reversed(ops) if reverse else ops):
        p = op['jsonPointer']
        if reverse:
            valid = get(obj,p) == op['after']
            if not valid: raise AssertionError(f'{label}: wrong after {p}')
            setvalue(obj,p,op['before'],remove=op['op']=='add')
        elif op['op'] == 'add':
            try:
                get(obj,p)
            except (KeyError,IndexError):
                exists = False
            else:
                exists = True
            valid = not exists and op.get('beforeExists') is False
            if not valid: raise AssertionError(f'{label}: add target exists {p}')
            setvalue(obj,p,op['after'])
        else:
            valid = op['op']=='replace' and get(obj,p)==op['before']
            if not valid: raise AssertionError(f'{label}: wrong before {p}')
            setvalue(obj,p,op['after'])
        if record:
            check('full-value pointer replay',f'{label}:{"reverse" if reverse else "forward"}:{i}:{p}',valid)
    return obj

def archive(rel, expected_members):
    z = zipfile.ZipFile(BASE / rel)
    names = z.namelist()
    safe = len(names)==len(set(names))
    for i in z.infolist():
        p = PurePosixPath(i.filename)
        safe = safe and not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
        safe = safe and not stat.S_ISLNK(i.external_attr >> 16)
    check('archive integrity',rel+': members',len(names)==expected_members)
    check('archive integrity',rel+': safe unique names',safe)
    check('archive integrity',rel+': CRC',z.testzip() is None)
    return z

def entries(z, key, prefix, label):
    m = json.loads(z.read('MANIFEST.json'))
    for ent in m[key]:
        b = z.read(prefix+ent['path'])
        check('exact source/member binding',label+': '+ent['path'],
              len(b)==ent['bytes'] and digest(b)==ent['sha256'])
    return m

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    parser.add_argument('--manifest-only', action='store_true')
    args = parser.parse_args()
    if args.manifest_only:
        m = load('MANIFEST.json')
        for f in m['files']:
            b = (BASE/f['path']).read_bytes()
            if len(b)!=f['bytes'] or digest(b)!=f['sha256']:
                raise AssertionError(f"Return manifest mismatch: {f['path']}")
        print(json.dumps({'manifestFilesVerified':len(m['files']),'failures':0,
                          'scope':'Return-file integrity only; no semantic/runtime claim.'},indent=2))
        return

    for f in load('INPUT_BINDINGS.json')['files']:
        b=(BASE/f['returnFile']).read_bytes()
        check('input binding',f['returnFile'],len(b)==f['bytes'] and digest(b)==f['sha256'])
    conf=archive('inputs/DD_Control_15_Conference_12.zip',94)
    ctx=archive('inputs/DD_Control_Illusion_Current_Acceptance_Context_01.zip',38)
    old=archive('history/DD_Part5_Control_Ready_Corrections_01.zip',73)
    ill=archive('history/DD_Illusion_Perception_14_Exact_13_Part5_Return_01.zip',34)
    companion=archive('history/DD_Companion_Life_10_Exact_05_Part5_Return_01.zip',26)
    cm=entries(conf,'files','sources/','conference')
    xm=entries(ctx,'sources','sources/','current context')
    entries(old,'files','','prior corrections')
    entries(ill,'files','','independent Illusion acceptance')
    entries(companion,'files','','independent Companion acceptance')
    check('source coverage','92 conference files',len(cm['files'])==92)
    check('source coverage','34 current context files',len(xm['sources'])==34)

    original_b=conf.read('sources/'+CANDIDATE)
    original=json.loads(original_b)
    check('candidate binding','Current12 exact bytes/hash',len(original_b)==1346471 and digest(original_b)=='33e1f85faab956d04bc9b9648e5cf619b12065e7f32d78ea986a284b1158835d')
    check('candidate binding','Current12 independent baseline copy',(BASE/'baseline/CONTROL15_CURRENT12.json').read_bytes()==original_b)
    for f in original['sourceBindings']:
        b=conf.read('sources/'+f['path'])
        check('recovered coverage','required: '+f['path'],len(b)==f['bytes'] and digest(b)==f['sha256'])
    cov=json.loads(old.read('SOURCE_COVERAGE.json'))
    missing=cov['unavailableBoundSources']
    check('recovered coverage','54 complete expected bindings',len(original['sourceBindings'])==54)
    check('recovered coverage','19 former missing bindings',len(missing)==19)
    for f in missing:
        b=conf.read('sources/'+f['path'])
        check('recovered coverage','recovered: '+f['path'],len(b)==f['bytes'] and digest(b)==f['sha256'])
    pre=load('inputs/PART5_CORRECTIONS_LOCAL_PREFLIGHT_01.json')
    check('preflight comparison','19 reported recovered same exact bindings',
          {(x['path'],x['bytes'],x['sha256']) for x in pre['recoveredMissingSources']} ==
          {(x['path'],x['bytes'],x['sha256']) for x in missing})

    oldops=json.loads(old.read('POINTER_OPERATIONS.json'))['operations']
    bindings=json.loads(old.read('ARTIFACT_BINDINGS.json'))['files']
    corrected=None
    for f in bindings:
        b=old.read(f['baselineFile']); a=old.read(f['correctedFile'])
        check('prior five-file binding',f['key']+': before',len(b)==f['bytes'] and digest(b)==f['sha256'])
        check('prior five-file binding',f['key']+': after',len(a)==f['correctedBytes'] and digest(a)==f['correctedSha256'])
        ops=[o for o in oldops if o['fileKey']==f['key']]
        forward=apply(json.loads(b),ops,label=f['key'])
        check('whole-byte reversibility',f['key']+': forward',canon(forward)==a)
        backward=apply(forward,ops,reverse=True,label=f['key'])
        check('whole-byte reversibility',f['key']+': reverse',canon(backward)==b)
        pf=next(p for p in pre['files'] if p['fileKey']==f['key'])
        check('preflight comparison',f['key']+': reported baseline and operations',
              pf['source']['bytes']==len(b) and pf['source']['sha256']==digest(b) and pf['operationCount']==len(ops))
        if f['key']=='control15':
            corrected=forward
            check('candidate binding','prior corrected independent copy',a==(BASE/'baseline/CONTROL15_AFTER_CORRECTIONS01.json').read_bytes())
    check('whole-byte reversibility','22 prior operations across5 files',len(oldops)==22 and len(bindings)==5)

    newplan=load('NEW_POINTER_OPERATIONS_FROM_CORRECTIONS01.json')
    fullplan=load('ALL_CONTROL_POINTER_OPERATIONS_FROM_CURRENT12.json')
    result_b=(BASE/'successor/CONTROL15_REVIEWED_SUCCESSOR13.json').read_bytes()
    result=json.loads(result_b)
    check('candidate binding','successor complete bytes',len(result_b)==newplan['result']['bytes'] and digest(result_b)==newplan['result']['sha256'])
    new=apply(corrected,newplan['operations'],label='new5')
    check('whole-byte reversibility','new5 forward complete bytes',canon(new)==result_b)
    check('whole-byte reversibility','new5 reverse complete bytes',canon(apply(new,newplan['operations'],reverse=True,label='new5'))==canon(corrected))
    all_result=apply(original,fullplan['operations'],label='combined14')
    check('whole-byte reversibility','combined14 forward complete bytes',canon(all_result)==result_b)
    check('whole-byte reversibility','combined14 reverse original complete bytes',canon(apply(all_result,fullplan['operations'],reverse=True,label='combined14'))==original_b)
    for label, obj, ops in [('new5 repeated',result,newplan['operations']),('combined14 repeated',result,fullplan['operations'])]:
        try:
            apply(obj,ops,record=False,label=label)
        except AssertionError:
            rejected=True
        else:
            rejected=False
        check('reject bad application',label,rejected)
    bad=copy.deepcopy(newplan['operations']);bad[0]['before']={'wrong':'entire value'}
    try:
        apply(corrected,bad,record=False,label='wrong before')
    except AssertionError:
        rejected=True
    else:
        rejected=False
    check('reject bad application','wrong full before rejected',rejected)

    catalog=json.loads(conf.read('sources/'+PREFIX+'data/public/spell_playtests/catalog.json'))
    core=json.loads(conf.read('sources/'+PREFIX+'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'))
    js=conf.read('sources/'+PREFIX+'src/data/spells.js').decode('utf-8')
    native=json.JSONDecoder().raw_decode(js.split('export const SPELLS = ',1)[1].lstrip())[0]
    catby={s['id']:s for s in catalog['spells']}
    cost={0:0,1:2,2:3,3:5,4:7,5:10,6:13,7:17,8:21,9:26}
    classrows=placements=0
    review_spells=load('SPELL_DISPOSITIONS.json')['dispositions']
    for i,s in enumerate(result['spells']):
        env=s['completeSourceAndAccess'];source=env['source'];sid=s['id']
        check('native source preservation',sid+': entire catalog envelope',env==catby[sid])
        check('native source preservation',sid+': full native JavaScript object',source['original']==native[sid])
        for ce in source['coreEntries']:
            check('native source preservation',sid+': Core '+str(ce['index']),core['spells'][ce['index']]==ce['original'])
        for cls,a in env['classAccess'].items():
            n=source['original'];classrows+=1
            check('actual class access',sid+': '+cls,a['rank']==n['classRanks'][cls] and a['minimumClassLevel']==n['classLearnLevels'][cls] and a['school']==n['classSchools'][cls] and a['baseRpCost']==cost[a['rank']])
        placements+=len(source['original']['placements'])
        check('procedure selection',sid+': complete proposed procedure unchanged',s['procedure']==corrected['spells'][i]['procedure'])
        check('procedure selection',sid+': full independent disposition payload',review_spells[i]['completeSelectedProcedure']==s['procedure'] and review_spells[i]['completeNativeSourceAndAccess']==env)
        check('procedure selection',sid+': risk not escalated',s['riskTier']==original['spells'][i]['riskTier'])
        route=next(r for r in result['sharedContractRouting11']['routes'] if r['spellId']==sid)
        shared=get(result,route['completeSharedPointer'])
        check('routed shared scope',sid+': complete selected values',review_spells[i]['fullSelectedSharedRouting']==route and review_spells[i]['completeApplicableSharedClauses']=={k:shared[k] for k in route['namedRelevantKeys']})
    check('native source preservation','15 identities/17placements/70access rows',len(result['spells'])==15 and placements==17 and classrows==70)
    check('routed shared scope','all original shared blocks unchanged',result['completeOriginalSharedProposals']==original['completeOriginalSharedProposals'])
    check('history preservation','all previous corrected spell records retained',result['spells']==corrected['spells'])
    check('history preservation','prior correction history exact',result['correctionHistoryPart5_01']==corrected['correctionHistoryPart5_01'])
    check('history preservation','two memory candidates unchanged',result['memorySourcesSeparated']==original['memorySourcesSeparated'] and len(result['memorySourcesSeparated'])==2)

    originals={s['id']:s for s in original['originalExamplesUnchanged']}
    review_cases=load('CASE_DISPOSITIONS.json')['cases']
    check('complete cases','30 full originals unchanged',result['originalExamplesUnchanged']==original['originalExamplesUnchanged'] and len(originals)==30)
    check('complete cases','30 full selected cases/dispositions',len(result['currentExamples'])==len(review_cases)==30)
    changedcases=[]
    for i,c in enumerate(result['currentExamples']):
        oldorig=originals[c['id']];ref=oldorig['sourceReference']
        source=json.loads(conf.read('sources/'+ref['path']))
        check('complete cases',c['id']+': native original text',get(source,ref['pointer'])==oldorig['exactOriginalText']==c['originalTextUnchanged'])
        r=review_cases[i]
        check('complete cases',c['id']+': complete original/current12/corrected/selected records',r['completeOriginalScenario']==oldorig['exactOriginalText'] and r['completeOriginalCurrent12Case']==original['currentExamples'][i] and r['completePriorCorrections01Case']==corrected['currentExamples'][i] and r['completeSelectedCurrentCase']==c)
        for rf in c.get('sourceRefs',[]):
            get(json.loads(conf.read('sources/'+rf['path'])),rf['pointer'])
        check('complete cases',c['id']+': genuine reason and source refs',bool(r['reason']) and bool(r['sourceRefs']))
        if c!=corrected['currentExamples'][i]:changedcases.append(c['id'])
    check('complete cases','only EN6-07-B further clarified',changedcases==['EN6-07-B'])
    check('complete cases','three whole positive-case holds',sum(c['disposition'].startswith('HOLD_WHOLE') for c in review_cases)==3)
    terminal=get(result,'/currentExamples/15/independentBranches/1/timeline/5')
    check('complete cases','Dance terminal explicitly conditional','conditional' in terminal['operation'].lower() and bool(terminal['branchPrecondition']) and bool(terminal['interveningSaveObligation']))
    qs=load('QUESTION_DISPOSITIONS.json')['dispositions']
    check('actual question dispositions','13 questions preserved',result['conferenceQuestions10']==original['conferenceQuestions10'] and len(qs)==13)
    for q,r in zip(original['conferenceQuestions10'],qs):
        check('actual question dispositions',q['id'],q['id']==r['id'] and q['question']==r['completeSubmittedQuestion'] and bool(r['answer']) and r['disposition'].startswith('RESOLVED'))

    idxpath=PREFIX+'data/public/spell_playtests/authored_review_index.json'
    oi=json.loads(conf.read('sources/'+idxpath));ni=json.loads(ctx.read('sources/'+idxpath))
    ob={e['id']:e for e in oi['entries']};nb={e['id']:e for e in ni['entries']}
    changed=[sid for sid in nb if nb[sid]!=ob[sid]]
    check('current/historical precedence','same848 identities and45 record changes',len(ob)==len(nb)==848 and ob.keys()==nb.keys() and len(changed)==45)
    check('current/historical precedence','historical480/368 retained',oi['authoredCounts']=={'reviewed':480,'pending':368})
    check('current/historical precedence','current525/323',ni['authoredCounts']=={'reviewed':525,'pending':323})
    status=collections.Counter(e['authoredStatus'] for e in ni['entries'])
    check('current/historical precedence','322 ordinary plus1 receipt-only pending',status['pending-authored-procedure']==322 and status['receipt-only-post-push-cosmology']==1)
    for s in result['spells']:
        check('current/historical precedence',s['id']+': pending index unchanged',ob[s['id']]==nb[s['id']])
    reg=json.loads(ctx.read('sources/'+PREFIX+'data/director/spell_review/accepted_interface_registry_06.json'))
    rb={e['id']:e for e in reg['entries']}
    check('current/historical precedence','173 current interfaces',len(reg['entries'])==173)
    for e in original['currentAcceptedInterfaceComparisons']:
        olde=e['completeEntry']
        check('reused exact interface',olde['id'],olde['exactAuthority']==rb[olde['id']]['exactAuthority'])
    for x in original['currentCompleteCounterparts']:
        if x.get('source') and x.get('procedurePointer') and x.get('completeCurrentProcedure') is not None:
            source=x['source'];path=source['path'] if isinstance(source,dict) else source
            actual=json.loads(conf.read('sources/'+path))
            check('complete counterpart binding',x['spellId'],get(actual,x['procedurePointer'])==x['completeCurrentProcedure'])
    for i,x in enumerate(original['actualItemCounterparts08']):
        actual=json.loads(conf.read('sources/'+x['source']['path']))
        check('complete counterpart binding','actual item '+str(i),get(actual,x['pointer'])==x['completeRecordUnchanged'])
    for i,x in enumerate(original['completeCreatureSourceCounterparts10']):
        actual=json.loads(conf.read('sources/'+x['source']['path']))
        check('complete counterpart binding','source-only creature '+str(i),get(actual,x['pointer'])==x['completeRecordUnchanged'])
    lich=original['actualLichSleepImmunitySource']
    actual=json.loads(conf.read('sources/'+lich['source']['path']))
    check('complete counterpart binding','actual Lich feature',get(actual,lich['pointer'])==lich['completeCard'])

    # Arithmetic checks are stipulated fixture arithmetic, NOT random draws or an engine run.
    from fractions import Fraction as F
    arithmetic=[
        ('Vision cost and damage',32-10==22 and 100-sum([3,3,4,4,4])==82),
        ('Mass Sleep ordering',60-20-25==15 and 20>15),
        ('min1 at zero and temp ignored',60-8-max(1,0)==51),
        ('Prison separate damage events',sum([6,6,6,5,5])==28 and sum([5,5,5,5,4])==24 and 100-28-24==48 and 28<50 and 24<50),
        ('Puppet movement cost',15*2==30),
        ('Puppet first END before maximum',F('8.4')<F('14.4') and F('2.4')<F('8.4')),
        ('Dance actual release clock',F('1.2')+60==F('61.2') and F('1.2')<6),
        ('Lesser Antimagic original maximum',3+60==63 and F('61.2')<63),
        ('Geas duration',30*24*60*60==2592000),
        ('Geas60sec suppression remaining',3600+60==3660 and 2592000-3660==2588340),
        ('conditional day-long Geas comparison',2592000-86400==2505600),
        ('Mass Suggestion fixed delayed trigger',86400-28800==57600),
        ('Group first apparent contact',50-2-(40+F('2.5'))==F('5.5')),
        ('Mind Fog first boundary contact',55-F('2.5')-(30+20)==F('2.5')),
        ('Eyebite supported body',30+F('2.5')==F('32.5') and 30-20==10),
        ('Actual Beast HP and AC, not CR',2*16+4==36 and 12+5//2==14)
    ]
    for name,ok in arithmetic:check('stipulated fixture arithmetic',name,ok)
    counts=collections.Counter(c['category'] for c in checks)
    report={'scope':'Read-only input/source/hash/full-value replay/preservation/fixture-arithmetic checks. Semantic dispositions are the separate authored review. No game engine/runtime, human gameplay or balance test is claimed.',
            'checkCount':len(checks),'failures':sum(not c['pass'] for c in checks),
            'categories':dict(sorted(counts.items())),'checks':checks,
            'runtimeTestsExecuted':0,'repositoryWrites':0,'liveWorkingTreeRead':False}
    if args.report:
        args.report.write_bytes(canon(report))
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
