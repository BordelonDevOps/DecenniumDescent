"""Record actual Repair04 submission, retaining prior evidence and the full goal."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, hashlib, json, subprocess, sys, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_REPAIR_03_AC6_PLANAR_02.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_REPAIR_04.json'
    receipt=A/'AC5_REPAIR_04_SUBMISSION_RECEIPT.json'; delta=A/'AC5_REPAIR_04_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-ac5-repair-04'
    assert not any(p.exists() for p in [checkpoint,receipt,delta,keep])
    native=A/'AC5_REPAIR_04_SUBMITTED_NATIVE.json';obs=read(native);turn=obs['turns'][0]
    assert turn['id']=='5e7d3717-2227-4522-9d1f-4feeee3b4f61'
    user=next(x for x in turn['items'] if x['type']=='userMessage')
    actual=''.join(x['text'] for x in user['content'] if x['type']=='text')
    suffix='\n\n[User attached 1 file; file contents were not included]'
    if actual.endswith(suffix):actual=actual[:-len(suffix)]
    request=A/'AC5_REPAIR_04_REQUEST.txt';archive=A/'DD_AC5_Repair_04.zip'
    assert actual==request.read_text(encoding='utf8')
    attachment=next(x for x in obs['attachments'] if x['name']==archive.name)
    assert Path(attachment['path']).read_bytes()==archive.read_bytes()
    with zipfile.ZipFile(archive) as z:
        bindings=json.loads(z.read('SOURCE_MANIFEST.json'))['bindings']; assert len(bindings)==92
        for x in bindings:
            b=z.read('sources/'+x['path']); assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
        assert z.read('PREVIOUS_RETURN.zip')==(A/'DD_AC5_Repair_03_Return.zip').read_bytes()
        assert z.read('REPAIR_REVIEW.json')==(A/'AC5_REPAIR_RETURN_03_SEMANTIC_REVIEW.json').read_bytes()
    screenshot=A/'PART4_AC5_REPAIR_04_SUBMITTED.png';browser=A/'AC5_REPAIR_04_SUBMITTED_BROWSER.txt'
    assert screenshot.stat().st_size>10000 and 'button "Stop"' in browser.read_text(encoding='utf8')
    submission={'id':'AC5-REPAIR-04-SUBMISSION','recordedAtUtc':now,'status':'Submitted once to actual GPT Part4. Native request/attachment exact; fresh browser shows active response and archive inspection. No returned Repair04 package yet.', 'threadId':obs['thread']['id'],'title':obs['thread']['title'],'userTurnId':turn['id'],'browserId':'3','tabId':'125746324','archive':info(archive),'request':info(request),'nativeObservation':info(native),'browserObservation':info(browser),'screenshot':info(screenshot),'uploadedAttachmentBytesMatch':True,'exactRequestMatches':True,'archiveSourcesReverified':92,'repairTopics':4,'previousReturn':info(A/'DD_AC5_Repair_03_Return.zip'),'localStructuralCheck':info(A/'AC5_REPAIR_RETURN_03_STRUCTURAL_CHECK.json'),'semanticReview':info(A/'AC5_REPAIR_RETURN_03_SEMANTIC_REVIEW.json'),'expectedReturn':'DD_AC5_Repair_04_Return.zip','expectedMinimumCases':61,'newSpellAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    receipt.write_bytes(encoded(submission))
    start=G/'START_HERE.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);originals[p]=b;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();assert text.count(previous.relative_to(G).as_posix())==1
    text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    marker='**Current GPT conference:**';begin=text.index(marker);end=text.index('\n\n',begin)
    paragraph='**Current GPT conference:** The [complete AC5 Repair03 return](docs/audit/2026-10-08/full-game/DD_AC5_Repair_03_Return.zip) is preserved with all 16 source/access records, 17 placements and 60 cases. [Independent verification](docs/audit/2026-10-08/full-game/AC5_REPAIR_RETURN_03_STRUCTURAL_CHECK.json) passed 812 preservation/reference checks. [Four remaining semantic topics](docs/audit/2026-10-08/full-game/AC5_REPAIR_RETURN_03_SEMANTIC_REVIEW.json) cover actual spell geometry, wall resumption, death-save clocks and portal transit. The [complete Repair04 packet is now submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC5_REPAIR_04_SUBMISSION_RECEIPT.json), with all 92 frozen sources. No AC5 spell is adopted yet; 435 ordinary spells remain reviewed and 413 pending.'
    start.write_text(text[:begin]+paragraph+text[end:],encoding='utf8',newline='\n')
    evidence=[receipt,A/'AC5_REPAIR_RETURN_03_STRUCTURAL_CHECK.json',A/'AC5_REPAIR_RETURN_03_SEMANTIC_REVIEW.json']
    cov=json.loads(originals[ledger]);oldcov=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac5-repair-04','recordedAtUtc':now,'status':'Full Repair03 preserved and independently reviewed; four focused remaining topics submitted in Repair04. No adoption.','ac5Identities':16,'ac5Cases':60,'structuralChecks':812,'structuralFailures':0,'repairTopics':4,'submittedSources':92,'newSpellAdoptions':0})
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in oldcov['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    code=originals[builder].decode();tail=' + read(A / "AC5_REPAIR_03_AC6_PLANAR_02_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC5_REPAIR_04_NAVIGATION_DELTA.json")["changes"]\n',1)
    additions=[('AC5 — Repair03 preservation and current references verified','AC5_REPAIR_RETURN_03_STRUCTURAL_CHECK.json'),('AC5 — four focused semantic repairs after Repair03','AC5_REPAIR_RETURN_03_SEMANTIC_REVIEW.json'),('AC5 — Repair04 actual GPT submission','AC5_REPAIR_04_SUBMISSION_RECEIPT.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in additions),1)
    code=code.replace('    featured = [\n','    featured = [\n        ("AC5 — complete Repair03 candidate, still unadopted", "docs/audit/2026-10-08/full-game/ac5-repair-03-return/PLAYER_CHAPTER.md"),\n',1)
    scope='435 reviewed / 413 pending ordinary spells. AC5 Repair03 is preserved:16 identities,17 placements,60 cases,92 sources and812 local structural checks with zero failures. Four remaining geometry/timing/operation topics are submitted in Repair04 to actual GPT Part4. No AC5 adoption. AC6 full14-identity current completion still needs remaining10 procedure revisions and dependency refresh; planar draft02 and Forge02 remain unadopted. Full75-area goal remains open.'
    values=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(values)==1
    code=code.replace(ast.get_source_segment(code,values[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':0,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1500:],run.stderr[-1500:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);prior=deepcopy(state['activeGptReview']);prior.update(status='Complete Repair03 received exactly and independently reviewed; four focused topics remain before exact acceptance.',returnReceived=True,returnedArchive=info(A/'DD_AC5_Repair_03_Return.zip'),structuralCheck=info(A/'AC5_REPAIR_RETURN_03_STRUCTURAL_CHECK.json'),semanticReview=info(A/'AC5_REPAIR_RETURN_03_SEMANTIC_REVIEW.json'))
    state.setdefault('priorCompletedGptReviews',[]).append(prior)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='no_progress: continuation visibility/status confirmation only; substantive work resumed in this turn',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Preserved full Repair03; independent verification and semantic review; four focused repairs submitted. No rule application.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview']={'reviewId':'AC5-REPAIR-04','threadId':submission['threadId'],'title':submission['title'],'browserId':'3','tabId':'125746324','conversationUrl':prior['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':submission['status'],'generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_AC5_Repair_04_Return.zip','returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(browser),'observationTimeoutMeansTerminal':False}
    state['safeNextActions']=['Continue SAME Part4 Repair04 user turn5e7d3717-2227-4522-9d1f-4feeee3b4f61. Browser confirmed responding and archive inspection. Do not resend/restart on observation timeouts. Use current live tab125746324.', 'When actual Repair04 returns, preserve exact bytes and independently review all four topics, full16 source/access records,17 placements,22 original texts,all60 retained caseIDs plus X31; verify current references and every92source binding.', 'After substantive agreement, obtain exact-file acceptance and apply accepted AC5 rules reversibly, preserving original sources and truthful counts. No candidate-only return is automatic adoption.', 'Complete remaining10 AC6 procedures and current14-identity cohort register; retain the full planar draft02 and Forge02. Refresh all AC5 source/interface bindings after actual acceptance before joint review.', 'Continue the full75-area objective, including every pending spell, environment/disease/consumables,feats,bestiary,Director,packaging,companion implementation and final GPT whole-game flow. Latest verified GitHub backup18c6e3a predates this local work.']
    state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Received exact complete AC5 Repair03, passed812 preservation/reference checks, independently identified four concrete remaining semantic topics, prepared and submitted complete92-source Repair04 to actualGPT.','evidence':info(receipt)}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'ordinarySpells':state['currentOrdinarySpellCounts'],'newSpellAdoptions':0}))

if __name__=='__main__':main()
