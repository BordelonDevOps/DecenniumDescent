"""Verify the reviewable patch and record its live GPT submission without adopting it."""
from copy import deepcopy
from datetime import datetime, timezone
from collections import Counter
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_READER_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_LOCAL_PATCH_01.json'
    receipt=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_SUBMISSION_RECEIPT.json'
    validation=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_VALIDATION.json'
    delta=A/'CHRONOLOGY_LOCAL_PATCH_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-chronology-local-patch-01'
    assert all(not p.exists() for p in [target,receipt,validation,delta,preserved])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    patch=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_PROPOSAL.json';proposal=read(patch)
    candidate=G/proposal['currentCandidate'];current=read(candidate);rebuilt=read(G/proposal['source']['path'])
    checks=[]
    def check(name,ok):checks.append({'name':name,'passed':bool(ok)});assert ok,name
    check('integrated model binding',info(G/proposal['source']['path'])==proposal['source'])
    for i,change in enumerate(proposal['changes']):
        parts=change['path'].strip('/').split('/');p=rebuilt
        for s in parts[:-1]:p=p[int(s)] if isinstance(p,list) else p[s]
        k=int(parts[-1]) if isinstance(p,list) else parts[-1]
        old=p.get(k) if isinstance(p,dict) else p[k]
        check(f'patch {i+1} exact old value {change["path"]}',old==change['before']);p[k]=deepcopy(change['after'])
    check('reapplying all42patches exactly reproduces supplied candidate',rebuilt==current and len(proposal['changes'])==42)
    rows=current['researchRoute']['qualificationSchedule']['intervals']
    def seconds(t):
        v=list(map(int,t.split(':')));return v[0]*3600+v[1]*60+(v[2] if len(v)>2 else 0)
    phases={};days={}
    for i,v in enumerate(rows):
        start=(v['day']-1)*86400+seconds(v['start']);end=(v['day']-1)*86400+seconds(v['end'])
        check(f'interval{i+1} positive exact seconds',end-start==v['seconds'] and end>start)
        phases.setdefault(v['phase'],[]).append((start,end));days.setdefault((v['phase'],v['day']),[]).append(v)
    for phase,intervals in phases.items():check(phase+' no cross-day interval overlap',all(a[1]<=b[0] for a,b in zip(intervals,intervals[1:])))
    for key,vs in days.items():check(str(key)+' productive day <=16h',sum(v['seconds'] for v in vs if v['kind'] in ['work','observation'])<=57600)
    findings=[v for v in rows if v['activity'].startswith('Q-')]
    success=[v for v in findings if 'Success' in v['activity']];failed=[v for v in findings if 'Failure' in v['activity']]
    counts=Counter(v['activity'].split()[0] for v in success)
    expected={v['id'] for v in current['researchRoute']['qualificationFindings']}
    check('all10findings succeed exactly once',len(success)==10 and set(counts)==expected and set(counts.values())=={1})
    check('40h successful and4h failed findings',sum(v['seconds'] for v in success)==40*3600 and sum(v['seconds'] for v in failed)==4*3600)
    check('two real70minute windows',sum(v['seconds'] for v in rows if v['kind']=='observation')==140*60)
    check('synthesis exactly240minutes',sum(v['seconds'] for v in rows if v['activity'].startswith('RR06 synthesis'))==240*60)
    check('fixed alias outcomes agree',current['researchRoute']['nodes'][5]['fixedOutcomes']==current['researchRoute']['nodes'][5]['outcomes'])
    check('RR04 observation aliases agree',current['researchRoute']['nodes'][3]['partyObservation']==current['researchRoute']['localChangeWindow']['partyObservation'])
    check('route remains unadopted','NOT ADOPTED' in current['researchRoute']['status'] and not proposal['newRulesAdopted'])
    validation.write_bytes(encoded({'recordedAtUtc':now,'proposal':info(patch),'candidate':info(candidate),'checks':checks,'checkCount':len(checks),'failureCount':0,'scope':'Exact patch application and authored clock arithmetic only; semantic GPT review pending, no runtime/human/whole-game claim.','sourceInformationDeleted':0,'newRulesAdopted':False}))
    dom=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_SUBMISSION_DOM.txt';text=dom.read_text(encoding='utf-8')
    assert 'button "Stop"' in text and patch.name in text and candidate.name in text
    receipt.write_bytes(encoded({'recordedAtUtc':now,'statusAtObservation':'sent once; GPT responding','conversationUrl':state['activeGptReview']['conversationUrl'],'tabId':'125746244','request':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_REQUEST.txt'),'proposal':info(patch),'candidate':info(candidate),'validation':info(validation),'submissionDom':info(dom),'screenshot':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_SUBMISSION.png'),'newRulesAdopted':False,'sourceInformationDeleted':0}))
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line=line.replace('GPT Part 3 is integrating [ten concrete research-route corrections](docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_INTEGRATION_SUBMISSION_RECEIPT.json); that operating route is **not yet adopted**.','GPT Part 3 is reviewing the [exact local route patch and complete candidate](docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_SUBMISSION_RECEIPT.json). The integrated return is preserved;42corrections and a56interval schedule are checked locally. That route is **not yet adopted**.').replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_READER_01.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_LOCAL_PATCH_01.json')
    assert new_line!=line;start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    old_guide=originals[guide].decode();old_para=next(v for v in old_guide.split('\n\n') if v.startswith('The [research-route integration]'))
    new_para='The [exact local route patch](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_SUBMISSION_RECEIPT.json) is now with actual GPT Part3 for confirmation. First, revised and integrated eight-file returns are preserved. The integrated return passes263source/file/location checks but retained clock and duplicate-field defects. Codex prepared42exact corrections and a complete candidate, with56nonoverlapping intervals,40hours successful findings,4hours failed/retried Nature work,4hours synthesis, and140minutes of actual observations. The [local validation](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_VALIDATION.json) verifies exact patch application and arithmetic only. GPT semantic review remains pending; no proposed Floor68route/clues/mechanics are adopted. Prior [semantic audit](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_REVISED_SEMANTIC_AUDIT.json) remains history.'
    guide_text=old_guide.replace(old_para,new_para,1);guide.write_text(guide_text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].append(receipt.relative_to(G).as_posix());row['validationEvidence'].append(validation.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'chronology-local-patch-01','recordedAtUtc':now,'submission':receipt.relative_to(G).as_posix(),'localChecks':validation.relative_to(G).as_posix(),'newRulesAdopted':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='Chronology source/reader work saved and locally checked; original text preserved. Integrated route263source checks pass, but42exact local corrections and56interval worked clock remain unadopted pending actual GPT Part3 confirmation. Owner campaign frame pending. Ordinary spells419reviewed429pending; fullgame/runtime/human gates open. GitHub18c6e3a; later work local.'
    text=originals[nav].decode();tail=' + read(A / "CHRONOLOGY_READER_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "CHRONOLOGY_LOCAL_PATCH_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    entries=[('Research route — exact42change local patch with GPT',receipt.name),('Research route — patch and56interval clock verification',validation.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(v)+',\n' for v in entries),1);compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_para,'replacement':new_para}];changes[1]['operations']=[{'old':line,'replacement':new_line}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(status='LP01..08 exact patch and full candidate submitted once; GPT responding at observation',submission=info(receipt),verdictStatus='Integrated return received; exact local patch still pending joint confirmation.',responsePendingAtSubmission=True)
    state['cosmologyChronologyRouteReview'].update(integratedArchive=info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Integrated_Addendum_and_Evidence.zip'),integratedSourceCheck=info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_RETURN_SOURCE_CHECK_integrated.json'),localPatch=info(patch),localCandidate=info(candidate),localValidation=info(validation),latestSubmission=info(receipt),newRouteRulesAdopted=False)
    state['cosmologyChronologyResearchSites'].update(status='Source comparison saved; exact42change route patch pending GPT confirmation',latestSubmission=info(receipt))
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions'][0]='Observe actual GPT Part3 tab125746244: two files LOCAL_PATCH_PROPOSAL and LOCAL_CANDIDATE were attached and sent once for LP01..08 confirmation. Read its review; verify any SMALL additional exact patch. Do not resend/rebuild broad package or adopt purely from source hashes. Integrated return and exact patch are already downloaded/read/prepared.'
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state));print(json.dumps({'checkpoint':info(target),'checks':len(checks),'failures':0,'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0}))

if __name__=='__main__':main()
