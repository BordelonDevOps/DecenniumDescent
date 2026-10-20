#!/usr/bin/env python3
"""Read-only integrity, full-object selection and reversal verifier.

Does not run supplied project scripts or apply files. Optional --report writes only
its explicitly selected report path. --external-archive-root additionally compares
supplemental context to prior archives already present there; it never downloads.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT=Path(__file__).resolve().parent
R='DescentReviewChanges/ReviewBible/'

def digest(b):return hashlib.sha256(b).hexdigest()
def encode(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def load(name):return json.loads((ROOT/name).read_bytes())
def pointer(obj,path):
    for token in path.strip('/').split('/') if path else []:
        token=token.replace('~1','/').replace('~0','~')
        obj=obj[int(token)] if isinstance(obj,list) else obj[token]
    return obj

def parent(obj,path):
    p,_,key=path.rpartition('/')
    return pointer(obj,p),key.replace('~1','/').replace('~0','~')

def replay(original,ops,reverse=False):
    result=copy.deepcopy(original)
    for op in reversed(ops) if reverse else ops:
        obj,key=parent(result,op['pointer']);key=int(key) if isinstance(obj,list) else key
        exists=(0<=key<len(obj)) if isinstance(obj,list) else key in obj
        expected=op['after'] if reverse else op['before']
        expected_exists=True if reverse else op['beforeExists']
        if exists!=expected_exists or (exists and obj[key]!=expected):
            raise ValueError('Full value/existence mismatch: '+op['pointer'])
        if reverse and not op['beforeExists']:
            del obj[key]
        else:obj[key]=copy.deepcopy(op['before'] if reverse else op['after'])
    return result

def safe_member(info):
    n=info.filename;p=PurePosixPath(n)
    return bool(n) and not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n and not stat.S_ISLNK(info.external_attr>>16)

class Checks:
    def __init__(self):self.rows=[]
    def check(self,category,label,condition,detail=None):
        self.rows.append({'category':category,'label':label,'passed':bool(condition),**({'detail':detail} if detail is not None else {})})
    def equal(self,category,label,a,b):self.check(category,label,a==b)
    def report(self):
        cats={}
        for r in self.rows:
            q=cats.setdefault(r['category'],{'checks':0,'failures':0});q['checks']+=1;q['failures']+=not r['passed']
        return {'id':'RD8-READ-ONLY-VERIFICATION-01','checkCount':len(self.rows),'failures':sum(not r['passed'] for r in self.rows),'categories':cats,'checks':self.rows,'scope':'Source/structure/selection/full-value reversal only. No semantic acceptance from counting checks, no project/runtime execution or application.'}

def verify(external=None,verify_manifest=False):
    t=Checks();inp=load('INPUT_BINDINGS.json');raw=(ROOT/inp['archive']).read_bytes()
    t.equal('input integrity','archive byte count',len(raw),inp['bytes']);t.equal('input integrity','archive SHA256',digest(raw),inp['sha256'])
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        t.equal('input integrity','CRC',z.testzip(),None)
        names=z.namelist();t.equal('input integrity','exact member count',len(names),55)
        t.equal('input integrity','unique members',len(names),len(set(names)))
        for info in z.infolist():t.check('input integrity','safe '+info.filename,safe_member(info))
        basebytes=z.read('CANDIDATE.json');C=json.loads(basebytes);man=json.loads(z.read('MANIFEST.json'))
        t.equal('input integrity','candidate exact size',len(basebytes),830297)
        t.equal('input integrity','candidate hash',digest(basebytes),'5bd1825bc6a67e9cff6d16998621cf9011c67158a67e9217e7a4fcdd26bbe24e')
        t.equal('input integrity','baseline full original bytes',(ROOT/'baseline/CANDIDATE.json').read_bytes(),basebytes)
        t.equal('input integrity','original serialization',encode(C),basebytes)
        t.equal('source bindings','candidate/manifests full source bindings',C['sourceBindings'],man['files'])
        t.equal('source bindings','full source count',len(C['sourceBindings']),51)
        sources={}
        for b in C['sourceBindings']:
            data=z.read('sources/'+b['path']);sources[b['path']]=data
            t.equal('source bindings',b['path']+' bytes',len(data),b['bytes'])
            t.equal('source bindings',b['path']+' SHA256',digest(data),b['sha256'])
        supplied=json.loads(z.read('PREFLIGHT.json'))
        t.equal('supplied historical report','checkCount (not reexecution)',supplied.get('checkCount'),240)
        t.equal('supplied historical report','failures (not reexecution)',supplied.get('failures'),0)
    src=lambda p:json.loads(sources[p])
    catalog=src(R+'data/public/spell_playtests/catalog.json')
    spellmap={s['id']:s for s in catalog['spells']}
    registry=src(R+'data/director/spell_review/accepted_interface_registry_06.json')
    index=src(R+'data/public/spell_playtests/authored_review_index.json')
    idx={r['id']:r for r in index['entries']}
    js=sources[R+'src/data/spells.js'].decode('utf-8-sig');start=js.index('{',js.index('export const SPELLS'))
    native,_=json.JSONDecoder().raw_decode(js[start:]) # Parse JSON literal, never execute JavaScript.
    core=src(R+'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    bookraw=sources[R+'rulebook_output.txt']
    book=bookraw.decode('utf-16' if bookraw[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8-sig').splitlines()
    t.equal('authority accounting','applied count',index['authoredCounts'],{'reviewed':525,'pending':323})
    t.equal('authority accounting','standalone count',index['representationCounts']['completeReviewedStandaloneProcedures'],249)
    t.equal('authority accounting','registry entry count',len(registry['entries']),173)
    M=load('MODEL.json');spells=load('SPELL_DISPOSITIONS.json');questions=load('QUESTION_DISPOSITIONS.json');cases=load('CASE_DISPOSITIONS.json')
    history=load('ORIGINAL_HISTORIES.json');authority=load('SOURCE_AUTHORITY.json');usage=load('INTERFACE_USAGE.json');counterparts=load('COUNTERPART_DISPOSITIONS.json')
    t.equal('native preservation','all original questions',M['questions'],C['questions'])
    t.equal('native preservation','all original source bindings',M['sourceBindings'],C['sourceBindings'])
    t.equal('native preservation','all original interface comparisons',M['currentAcceptedInterfaceComparisons'],C['currentAcceptedInterfaceComparisons'])
    t.equal('native preservation','all original counterparts',M['completeAcceptedCounterparts'],C['completeAcceptedCounterparts'])
    t.equal('native preservation','complete original records in history',history['completeOriginalRecordsUnchanged'],C['records'])
    t.equal('native preservation','complete original question history',history['completeOriginalQuestionsUnchanged'],C['questions'])
    t.equal('native preservation','original operational cases',C['earlierOperationalWorkedCases'],[])
    t.equal('native preservation','original current vectors',C['currentVectors'],[])
    t.equal('native preservation','preserved semantic delta',M['semanticDelta'],C['semanticDelta'])
    t.equal('native preservation','preserved pending labels',M['pendingComparisonsNotAuthority'],C['pendingComparisonsNotAuthority'])
    t.equal('native preservation','risk tiers unchanged',M['riskCounts'],C['riskCounts'])
    t.equal('selected structures','six records',len(M['records']),6)
    rows=0;placements=0
    for i,r in enumerate(C['records']):
        sid=r['spellId'];s=r['completeCurrentCatalogSourceAndAccess'];original=s['source']['original'];selected=M['records'][i]
        t.equal('native preservation',sid+' complete source/access',selected['completeCurrentCatalogSourceAndAccess'],s)
        t.equal('native preservation',sid+' catalog source',spellmap[sid],s)
        t.equal('native preservation',sid+' native JS object',native[sid],original)
        t.equal('native preservation',sid+' unchanged pending index entry',idx[sid],r['currentIndexEntry'])
        for k,v in r.items():
            if k!='status':t.equal('native preservation',sid+' original field '+k,selected[k],v)
        qsrc=r['originalQuestionSource'];t.equal('native preservation',sid+' original full source question',pointer(src(qsrc['path']),r['originalQuestionPointer']),r['completeOriginalSourceQuestionUnchanged'])
        for c in s['source']['coreEntries']:
            t.equal('native preservation',sid+' full Core row '+str(c['index']),core['spells'][c['index']],c['original'])
        for b in r['completeCurrentBookBindings']:
            placements+=1;row=b['currentBookRow'];t.equal('native preservation',sid+' exact book line',book[row['line']-1].strip(),row['exactText'])
            t.check('native preservation',sid+' actual placement',b['catalogPlacement'] in original['placements'])
        for cls,a in s['classAccess'].items():
            rows+=1;t.equal('class access',sid+'/'+cls+' rank',a['rank'],original['classRanks'][cls])
            t.equal('class access',sid+'/'+cls+' level',a['minimumClassLevel'],original['classLearnLevels'][cls])
            t.equal('class access',sid+'/'+cls+' school',a['school'],original['classSchools'][cls])
            t.equal('class access',sid+'/'+cls+' base cost',a['baseRpCost'],21)
            classfile=src(R+'data/public/class_playtests/'+cls.lower()+'.json')
            t.equal('class access',sid+'/'+cls+' actual rank at15',classfile['maxSpellRankByClassLevel'][14],8)
        t.equal('selected structures',sid+' full procedure mirror',spells[i]['procedure'],selected['procedure'])
        t.equal('selected structures',sid+' source mirror',spells[i]['completeSourceAndAccessUnchanged'],s)
        shared=[a for a in M['selectedSharedRules'] if a['id'] in selected['selectedSharedRuleIds']]
        t.equal('selected structures',sid+' full routed shared clauses',spells[i]['completeApplicableSharedRules'],shared)
        t.equal('selected structures',sid+' routing',spells[i]['sharedRuleIds'],selected['selectedSharedRuleIds'])
    t.equal('class access','actual access rows',rows,15);t.equal('native preservation','native placements',placements,6)
    wiz=src(R+'data/public/class_playtests/wizard.json')
    t.equal('class access','School Mastery actual card',wiz['cards'][56]['id'],'wizard.supplement.school-mastery')
    t.check('class access','School Mastery total +2 is explicit','+2 total' in wiz['cards'][56]['effect'])
    t.equal('class access','Arcane Feedback actual card',wiz['cards'][60]['id'],'wizard.supplement.arcane-feedback')
    t.equal('class access','Arcane Feedback automatic level15',(wiz['cards'][60]['acquisition'],wiz['cards'][60]['minimumClassLevel']),('automatic',15))
    for cls,expected in [('wizard',56),('mage',44),('druid',42),('cleric',42)]:
        t.equal('class access',cls+' actual level15 RP',src(R+'data/public/class_playtests/'+cls+'.json')['rpByClassLevel'][14],expected)
    for i,r in enumerate(C['currentAcceptedInterfaceComparisons']):
        e=r['completeEntryUnchanged'];s=e['currentAuthoritativeSource'];p=s['path']
        t.equal('accepted interfaces',e['id']+' registry complete entry',pointer(registry,r['registryPointer']),e)
        t.equal('accepted interfaces',e['id']+' source binding',digest(sources[p]),s['sha256'])
        if 'pointer' in s:t.equal('accepted interfaces',e['id']+' complete authority',pointer(src(p),s['pointer']),e['exactAuthority'])
        else:t.check('accepted interfaces',e['id']+' exact heading text exists',e['exactAuthority'].replace('\r\n','\n') in sources[p].decode('utf-8-sig').replace('\r\n','\n'))
        t.equal('accepted interfaces',e['id']+' scoped comparison copy',usage[i]['completeOriginalComparisonUnchanged'],r)
    for i,r in enumerate(C['completeAcceptedCounterparts']):
        full=src(r['source']['path'])
        t.equal('accepted counterparts',r['spellId']+' full card',pointer(full,r['pointer']),r['completeCurrentCard'])
        t.equal('accepted counterparts',r['spellId']+' full comparison',counterparts[i]['completeCounterpartUnchanged'],r)
        t.equal('accepted counterparts',r['spellId']+' source hash',digest(sources[r['source']['path']]),r['source']['sha256'])
    t.equal('accepted interfaces','full authority set',authority['completeAcceptedInterfaces'],C['currentAcceptedInterfaceComparisons'])
    t.equal('accepted counterparts','full counterpart set',authority['completeAcceptedCounterparts'],C['completeAcceptedCounterparts'])
    t.equal('selected structures','six full shared clauses',len(M['selectedSharedRules']),6)
    t.equal('selected structures','twenty answers',len(questions),20)
    for i,q in enumerate(questions):
        t.equal('questions',q['id']+' complete original question',q['completeSubmittedQuestionUnchanged'],C['questions'][i])
        t.check('questions',q['id']+' full answer',bool(q['answer'].strip()))
        t.equal('questions',q['id']+' current model disposition',M['reviewQuestionDispositions02'][i],q)
        t.check('questions',q['id']+' explicitly proposed selection',q['decisionSelectedForProposedSuccessor'])
    t.equal('complete cases','whole case selection',M['currentVectors'],cases['allCases'])
    t.equal('complete cases','main cases',len(cases['allCases']),12)
    ids=[];branch_count=0
    for c in cases['allCases']:
        ids.append(c['id']);t.check('complete cases',c['id']+' complete positive encounter',all(c.get(k) for k in ['actorSheets','geometry','timeline','rng','intermediateAndFinalState','sourceRefs','originalScenarioHistory']))
        t.check('complete cases',c['id']+' explicitly not runtime','NOT_RUNTIME_EXECUTED' in c['disposition'])
        for b in c['independentBranches']:
            ids.append(b['id']);branch_count+=1
            t.check('complete cases',b['id']+' complete independent inputs/results',all(b.get(k) for k in ['actorSheets','geometry','timeline','finalState','qualification','reset']))
    t.equal('complete cases','unique all case IDs',len(ids),len(set(ids)))
    t.equal('complete cases','41 full independent branches',branch_count,41)
    t.equal('complete cases','branch count metadata',branch_count,cases['independentBranchCount'])
    t.equal('complete cases','engineExecution flag',cases['engineExecution'],False)
    player=(ROOT/'PLAYER_CHAPTER.md').read_text();director=(ROOT/'DIRECTOR_REVIEW.md').read_text()
    for s in spells:
        t.check('complete renderings',s['spellId']+' entire player procedure',s['procedure'] in player)
        t.check('complete renderings',s['spellId']+' entire director procedure',s['procedure'] in director)
        for cls,a in s['completeSourceAndAccessUnchanged']['classAccess'].items():
            row=f"| {cls} | {a['rank']} | {a['minimumClassLevel']} | {a['school']} | {a['baseRpCost']} |"
            t.check('complete renderings',s['spellId']+'/'+cls+' exact access row',row in player and row in director)
    for s in M['selectedSharedRules']:t.check('complete renderings',s['id']+' complete clause in both',s['wording'] in player and s['wording'] in director)
    for q in questions:t.check('complete renderings',q['id']+' full question answer block',json.dumps(q,ensure_ascii=False,indent=2) in director)
    t.check('complete renderings','all complete cases block',json.dumps(cases,ensure_ascii=False,indent=2) in director)
    context=load('CONTEXT_BINDINGS.json');t.equal('supplemental context','11 full files',len(context['files']),11)
    for b in context['files']:
        data=(ROOT/b['file']).read_bytes();t.equal('supplemental context',b['file']+' bytes',len(data),b['bytes']);t.equal('supplemental context',b['file']+' hash',digest(data),b['sha256'])
        for a in b['exactArchiveAnchors']:
            t.equal('supplemental context',b['file']+' anchor member bytes',a['bytes'],len(data));t.equal('supplemental context',b['file']+' anchor member hash',a['sha256'],digest(data))
            if external:
                p=external/a['archive'];ar=p.read_bytes();t.equal('external original anchors',a['archive']+' hash for '+b['file'],digest(ar),a['archiveSha256']);t.equal('external original anchors',a['archive']+' bytes for '+b['file'],len(ar),a['archiveBytes'])
                with zipfile.ZipFile(io.BytesIO(ar)) as az:t.equal('external original anchors',b['file']+' entire original member',az.read(a['member']),data)
    plan=load('EXACT_OPERATIONS_FROM_SOURCE.json');t.equal('full-value replay','37 operations',len(plan['operations']),37)
    t.equal('full-value replay','base plan hash',digest(basebytes),plan['base']['sha256'])
    out=replay(C,plan['operations']);t.equal('full-value replay','entire forward object',out,M)
    t.equal('full-value replay','entire forward bytes',encode(out),(ROOT/'MODEL.json').read_bytes())
    t.equal('full-value replay','entire reverse bytes',encode(replay(out,plan['operations'],True)),basebytes)
    for i,o in enumerate(plan['operations']):
        t.equal('full-value replay','operation '+str(i)+' selected full after',pointer(M,o['pointer']),o['after'])
        if o['beforeExists']:t.equal('full-value replay','operation '+str(i)+' original full before',pointer(C,o['pointer']),o['before'])
    t.equal('full-value replay','successor plan hash',digest(encode(M)),plan['successor']['sha256'])
    t.equal('full-value replay','successor plan size',len(encode(M)),plan['successor']['bytes'])
    for bad,label in [(M,'repeated forward application'),(dict(C,status='altered'),'changed baseline value')]:
        rejected=False
        try:replay(bad,plan['operations'])
        except ValueError:rejected=True
        t.check('full-value replay',label+' rejected',rejected)
    receipt=load('REVIEW_RECEIPT.json');holds=load('HOLD_REGISTER.json')
    t.equal('boundaries','receipt exact successor hash',receipt['successor']['sha256'],digest(encode(M)))
    t.equal('boundaries','receipt exact successor size',receipt['successor']['bytes'],len(encode(M)))
    t.equal('boundaries','applied baseline unchanged',M['countsUnchanged'],C['countsUnchanged'])
    for key in ['runtimeTestsExecuted','humanPlaytests','sourceInformationDeleted','cosmologyDecisions','newAppliedProjectRuleAdoptions']:
        t.equal('boundaries',key,M[key],0)
    for key in ['wholeGameComplete','runtimeImplemented','runtimeSelectionEnabled']:t.equal('boundaries',key,M[key],False)
    t.equal('boundaries','all independent content holds',holds['retainedIndependentWholePositiveCaseHolds'],['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B'])
    t.equal('boundaries','no invented missing source gap',holds['sourceFileGap'],None)
    t.equal('boundaries','no positive main behavior replaced by hold',holds['wholeRank8MainCaseHolds'],[])
    t.equal('boundaries','13 scoped authoring IDs',len(M['proposedScopedRuleSelections02']),13)
    # Reports are inspected as reports; this verifier never executes the spec script.
    if (ROOT/'SPECIFICATION_REPORT.json').exists():
        sp=load('SPECIFICATION_REPORT.json');t.equal('isolated report bindings','cases hash',sp['casesSha256'],digest((ROOT/'CASE_DISPOSITIONS.json').read_bytes()))
        t.equal('isolated report bindings','failures',sp['failures'],0);t.equal('isolated report bindings','errors',sp['errors'],0)
        t.equal('isolated report bindings','test result count',len(sp['passedTests']),sp['testsRun'])
        t.equal('isolated report bindings','no runtime tests',sp['projectRuntimeTests'],0)
    if verify_manifest:
        mf=load('MANIFEST.json');t.equal('return manifest','file count',len(mf['files']),mf['fileCount'])
        for b in mf['files']:
            p=ROOT/b['path'];data=p.read_bytes();t.equal('return manifest',b['path']+' bytes',len(data),b['bytes']);t.equal('return manifest',b['path']+' SHA256',digest(data),b['sha256'])
    return t.report()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);ap.add_argument('--external-archive-root',type=Path);ap.add_argument('--manifest',action='store_true');args=ap.parse_args()
    report=verify(args.external_archive_root,args.manifest)
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checkCount':report['checkCount'],'failures':report['failures'],'categories':report['categories']},indent=2))
    for r in report['checks']:
        if not r['passed']:print('FAIL',r['category'],r['label'])
    raise SystemExit(1 if report['failures'] else 0)
if __name__=='__main__':main()
