"""Read-only exact candidate preservation/envelope audit; Python standard library.
Usage: python audit_exact_submission.py EXTRACTED_ROOT REPORT_PATH [ARCHIVE_PATH]
This checks text/data contracts, not complete gameplay semantics or a runtime.
"""
from pathlib import Path
from collections import Counter
import sys,json,hashlib,zipfile,xml.etree.ElementTree as ET

def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def shab(b): return hashlib.sha256(b).hexdigest()
def readb(p): return Path(p).read_bytes()
def walk(x):
    yield x
    if isinstance(x,dict):
        for v in x.values(): yield from walk(v)
    elif isinstance(x,list):
        for v in x: yield from walk(v)

def main(root,report,archive=None):
    root=Path(root).resolve(); report=Path(report).resolve()
    if report.is_relative_to(root): raise ValueError('Report must be outside immutable input tree')
    checks=[]
    def ck(group,name,result,detail=None):
        checks.append({'group':group,'name':name,'pass':bool(result),**({'detail':detail} if not result else {})})
    manifest=load(root/'FILE_MANIFEST.json')
    ck('integrity','393 payload entries',len(manifest)==393)
    if archive:
        raw=readb(archive)
        ck('integrity','input archive size and SHA256',len(raw)==60244248 and shab(raw)=='a95210e8292f41f36df8656e71300a589790dce72c774d2b535e65be39ff1db0')
    for name,e in manifest.items():
        p=root/name
        good=p.resolve().is_relative_to(root) and p.is_file()
        raw=readb(p) if good else b''
        ck('payload',name,good and len(raw)==e['bytes'] and shab(raw)==e['sha256'])
    protected=load(root/'ORIGINAL_SOURCE_V3_FILE_MANIFEST.json')
    ck('integrity','342 protected entries',len(protected)==342)
    for name,e in protected.items():
        p=root/name; raw=readb(p)
        ck('protected',name,len(raw)==e['bytes'] and shab(raw)==e['sha256'])
    B=root/'DescentReviewChanges/ReviewBible'; A=root/'docs/audit/2026-10-08/full-game'; P=A/'low-rank137-source-reviewer-files'
    sm=load(P/'FILE_MANIFEST.json')
    # Final source package has 27 payloads plus its self-excluding manifest.
    if isinstance(sm,dict) and 'files' in sm: sm=sm['files']
    if isinstance(sm,list): sm={r['path']:r for r in sm}
    for name,e in sm.items():
        p=P/name
        h=e if isinstance(e,str) else e.get('sha256')
        ck('source-package',name,shab(readb(p))==h)
    I=load(B/'data/playtest/spell_drafts/candidate_low_rank_136.json')
    U=load(B/'data/public/spell_playtests/candidate_low_rank_136.json')
    source=load(P/'LR_137_AUTHORING_REGISTER.json')['records']
    cat=load(B/'data/public/spell_playtests/catalog.json')['spells']; catalog={r['id']:r for r in cat}
    core=load(B/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')['spells']
    qmap=load(A/'LOW_RANK_136_CANDIDATE_QUESTION_MAP.json')['records']
    ck('coverage','137 distinct source/question/card rows',len(I['spells'])==len(U['spells'])==len(source)==len(qmap)==137 and len({r['id'] for r in U['spells']})==137 and len({r['questionId'] for r in source})==137)
    ck('coverage','136 procedures plus null Blink',sum(r['operationalCandidate'] is not None for r in U['spells'])==136 and next(r for r in U['spells'] if r['id']=='blink')['operationalCandidate'] is None)
    ck('coverage','catalog remains 276/572',sum(r['operational'] is not None for r in cat)==276 and len(cat)==848)
    ck('projection','whole envelope metadata parity',{k:v for k,v in I.items() if k!='spells'}=={k:v for k,v in U.items() if k!='spells'})
    shared=load(P/'LR_SHARED_OPERATING_DIRECTIONS.json')['policies']
    ck('shared','20 complete policies',len(shared)==len(U['sharedRules'])==20)
    for actual,s in zip(U['sharedRules'],shared):ck('shared',s['id'],actual==s)
    fields={'activation':'castingTime','range':'range','components':'components','target':'targets','duration':'duration','resolution':'resolution','procedure':'effect','limitsAndLifecycle':'limitations','numericParameters':'numericParameters'}
    intros=['Adopt the supplied Silent Echo proposal as NEW authoring direction. ','Adopt the supplied Blurred Visage proposal. ','Adopt the supplied minor-disguise proposal: ','Adopt the supplied Silence proposal. ','Adopt the proposal: ']
    bookcache={}; nbook=0
    alltexts=(B/'docs/playtest/LOW_RANK_136_CANDIDATE.md').read_text()
    # Parse full ordered sections; no paragraph is accepted from another card.
    headers=[f"### {r['questionId']} — {r['name']}" for r in source]
    positions=[alltexts.index(h+'\n') for h in headers]
    ck('manuscript','137 headings in exact source order',positions==sorted(positions) and all(alltexts.count(h+'\n')==1 for h in headers))
    for idx,(i,u,s,q) in enumerate(zip(I['spells'],U['spells'],source,qmap)):
        sid=s['spellId']; qid=s['questionId']
        ck('source',qid+' source original/current receipt',u['sourceReceipt']==s['fullSourceAndCurrentAccessRecord']==catalog[sid])
        ck('source',qid+' full internal source authoring',i['internalSourceAuthoringRecord']==s)
        ck('projection',qid+' exact whole public card',u=={k:v for k,v in i.items() if k!='internalSourceAuthoringRecord'})
        ck('source',qid+' access/additional cost presence and values',all((k in u)==(k in catalog[sid]) and (k not in u or u[k]==catalog[sid][k]) for k in ['classAccess','additionalRpCost']))
        ck('status',qid+' no premature selection or approval',u['selectionEnabled'] is False and all(u['reviewEvidence'][k] is False for k in ['exactCandidateApproval','catalogPromotionAuthorized','runtimeVerified','humanPlaytested']) and catalog[sid]['operational'] is None)
        ck('source',qid+' full bindings and shared references',u['bookBindings']==s['bookBindings'] and u['sourceModeBindings']==s['sourceModeBindings'] and u['sharedRuleIds']==s['sharedPolicyRefs'])
        ck('question-map',qid+' full original question and pointers',q['questionId']==qid and q['spellId']==sid and q['sourceQuestion']==s['sourceQuestion'] and q['publicCardPointer']==f'/spells/{idx}' and q['fullOperationalPointer']==f'/spells/{idx}/operationalCandidate' and q['manuscriptHeading']==f"{qid} — {s['name']}" and q['sourceModeBindings']==s['sourceModeBindings'] and q['bookBindings']==s['bookBindings'])
        ck('source',qid+' conflicts, prerequisites and example',u['sourceConflicts']==s['explicitConflictDispositions'] and u['operationPrerequisites']==s['particularOperationPrerequisites'] and u['authoredBoundary']==s['workedBoundary'])
        segment=alltexts[positions[idx]:positions[idx+1] if idx+1<len(positions) else len(alltexts)]
        if s['authoring'] is not None:
            for src,dst in fields.items():
                expect=s['authoring'][src]
                if src=='procedure':
                    for prefix in intros:
                        if expect.startswith(prefix):
                            expect=expect[len(prefix):];expect=expect[0].upper()+expect[1:];break
                ck('operational-fields',qid+'/'+dst,u['operationalCandidate'][dst]==expect)
                text=json.dumps(expect,ensure_ascii=False,indent=2) if isinstance(expect,(dict,list)) else expect
                ck('manuscript-fields',qid+'/'+dst,text in segment)
            ck('manuscript-fields',qid+'/costProcedure',u['operationalCandidate']['costProcedure'] in segment)
        else:ck('receipt',qid+' Blink remains nonoperative',u['operationalCandidate'] is None and '**No operational procedure.**' in segment)
        for mode in u['sourceModeBindings']:
            e=core[mode['coreIndex']]
            mapping={'sourceSchool':'school','sourceRank':'level','sourceName':'name','sourceCastingTime':'casting_time','sourceRange':'range','sourceDuration':'duration','sourceComponents':'components','sourceEffect':'effect'}
            ck('source-mode',qid+'/'+str(mode['coreIndex']),all(mode[a]==e[b] for a,b in mapping.items()))
        for b in u['bookBindings']:
            nbook+=1; file=b['actualDocxFile']
            if file not in bookcache:
                with zipfile.ZipFile(root/file) as z:xml=ET.fromstring(z.read('word/document.xml'))
                ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                bookcache[file]=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:body/w:p',ns)]
            ck('actual-docx',qid+'/'+str(nbook),all(bookcache[file][v]==b['currentBookRow']['exactText'] for v in b['actualDocxZeroBasedParagraphIndices']))
    ck('coverage','141 actual book bindings',nbook==141)
    # Full ordered source-mode JSON and card section content, not effects alone.
    for idx,(u,s) in enumerate(zip(U['spells'],source)):
        segment=alltexts[positions[idx]:positions[idx+1] if idx+1<len(positions) else len(alltexts)]
        ck('manuscript-completeness',s['questionId'],json.dumps(u['sourceModeBindings'],ensure_ascii=False,indent=2) in segment and u['authoredBoundary']['wording'] in segment and all(x in segment for x in u['sourceConflicts']+u['operationPrerequisites']) and all(' | '.join([name]+[str(v.get(k,'(absent)')) for k in ['rank','minimumClassLevel','school','baseRpCost']]) in segment for name,v in u.get('classAccess',{}).items()))
    ck('projection','whole manuscript byte parity',readb(B/'docs/playtest/LOW_RANK_136_CANDIDATE.md')==readb(B/'data/public/spell_playtests/candidate_low_rank_136.md'))
    C=load(B/'data/playtest/spell_drafts/low_rank_137_authored_boundaries.json'); D=load(B/'data/public/spell_playtests/low_rank_137_authored_boundaries.json')
    ck('projection','whole 187-case envelope parity',C==D)
    ck('coverage','187 unique examples',len(C['cases'])==len({x['id'] for x in C['cases']})==187)
    casebook=(B/'docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md').read_text()
    worked=load(P/'LR_WORKED_BOUNDARIES.json'); proposal=load(P/'LR_8_PROPOSAL_DISPOSITIONS.json')
    expected=[('LR-C-'+x['questionId'],x) for x in worked['perSpellBoundaries']]+[(x['id'],x) for x in worked['jointBoundaries']]+[(x['id'],x) for p in proposal['records'] for x in p['boundaryDispositions']]
    qids={s['questionId'] for s in source}
    for c,(cid,e) in zip(C['cases'],expected):
        ck('boundary-source',cid,c['id']==cid and c['authoredExpectation']==e and c['runtimePassed'] is False)
        start=casebook.index('## '+cid+'\n');nextpos=casebook.find('\n## ',start+1); section=casebook[start:nextpos if nextpos!=-1 else len(casebook)]
        ck('boundary-manuscript',cid,json.dumps(e,ensure_ascii=False,indent=2) in section and all(q in qids for q in c['questionIds']))
    ck('projection','whole casebook byte parity',readb(B/'docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md')==readb(B/'data/public/spell_playtests/low_rank_137_authored_boundaries.md'))
    interfaces=load(P/'LR_CLASS_AND_SPELL_INTERFACE_DISPOSITIONS.json')
    for c in interfaces['classComparisons']:
        s=c['unchangedCompleteComparison']; file=s.get('path',s.get('file'))
        data=load(root/file)
        result=s['card'] in data['cards'] if 'card'in s else s['engine']==data['engine'] if 'engine'in s else s['paragraph']==data['engine'][s['engineIndex']]
        ck('class-comparison',c['id'],result and c['newClassPromotion'] is False and c['sourceChanged'] is False)
    for c in interfaces['spellCounterparts']:
        ck('counterpart',c['spellId'],c['unchangedCompleteCounterpart']==catalog[c['spellId']])
    forbidden={'internalSourceAuthoringRecord','unchangedCompleteComparison','classComparisons','spellCounterparts','matrixResearch'}
    ck('projection','no internal comparison objects projected',all(not(forbidden&set(x)) for x in walk(U) if isinstance(x,dict)))
    report.parent.mkdir(parents=True,exist_ok=True)
    result={'scope':'Read-only preservation, source/mode/question/book and complete envelope/manuscript contract checks. Does not settle the separately named semantic corrections or execute complete spell procedures.','checkCount':len(checks),'groupCounts':dict(Counter(c['group'] for c in checks)),'failedChecks':[c for c in checks if not c['pass']],'checks':checks,'candidateIdentities':137,'mechanicalProcedures':136,'blinkReceiptOnly':True,'bookBindings':nbook,'authoredBoundaries':187,'classComparisons':54,'counterparts':114}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
    return 0 if not result['failedChecks'] else 1
if __name__=='__main__':
    sys.exit(main(*sys.argv[1:]))
