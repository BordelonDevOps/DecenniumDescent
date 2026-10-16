"""Record verified GPT repair submission and preserve independent AC6 planar work."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, hashlib, json, subprocess, sys, zipfile
from pathlib import Path
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    native=A/'AC5_REPAIR_03_SUBMITTED_NATIVE.json'; screenshot=A/'PART4_AC5_REPAIR_03_SUBMITTED.png'; archive=A/'DD_AC5_Repair_03.zip'; request=A/'AC5_REPAIR_03_REQUEST.txt'
    receipt=A/'AC5_REPAIR_03_SUBMISSION_RECEIPT.json'
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_INTERFACE_PREPARATION_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_REPAIR_03_AC6_PLANAR_02.json'
    delta=A/'AC5_REPAIR_03_AC6_PLANAR_02_NAVIGATION_DELTA.json'; keep=A/'navigation-before-ac5-repair-03-ac6-planar-02'
    assert not any(p.exists() for p in [receipt,checkpoint,delta,keep])
    obs=read(native); turn=obs['turns'][0]; assert turn['id']=='52b6d86f-9c53-4976-a528-731bbe5e02b2'
    user=next(x for x in turn['items'] if x['type']=='userMessage')
    actual=''.join(x['text'] for x in user['content'] if x['type']=='text')
    suffix='\n\n[User attached 1 file; file contents were not included]'
    if actual.endswith(suffix):actual=actual[:-len(suffix)]
    assert actual==request.read_text(encoding='utf8'), repr(actual[-200:])
    attachment=next(x for x in obs['attachments'] if x['name']=='DD_AC5_Repair_03.zip')
    assert Path(attachment['path']).read_bytes()==archive.read_bytes()
    sourcecheck=[]
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('SOURCE_MANIFEST.json'))
        for x in manifest['bindings']:
            raw=z.read('sources/'+x['path']);assert len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256'];sourcecheck.append(x['path'])
        assert len(sourcecheck)==92
        assert z.read('REPAIR_REVIEW.json')==(A/'AC5_CURRENT_RETURN_02_SEMANTIC_REVIEW.json').read_bytes()
        assert z.read('PREVIOUS_RETURN.zip')==(A/'DD_AC5_Current_Review_02_Return.zip').read_bytes()
    assert screenshot.is_file() and screenshot.stat().st_size>10000
    submission={'id':'AC5-REPAIR-03-SUBMISSION','recordedAtUtc':now,'status':'Submitted exactly once to actual GPT Part4; screenshot shows GPT inspecting archive and acknowledging92sources. No returned repair package yet.','threadId':obs['thread']['id'],'title':obs['thread']['title'],'userTurnId':turn['id'],'browserId':'3','tabId':'125746308','archive':info(archive),'request':info(request),'nativeObservation':info(native),'screenshot':info(screenshot),'uploadedAttachmentBytesMatch':True,'exactRequestMatches':True,'archiveSourcesReverified':92,'originalSourceCount':86,'supplementalSourceCount':6,'firstReturn':info(A/'DD_AC5_Current_Review_02_Return.zip'),'localStructuralCheck':info(A/'AC5_CURRENT_RETURN_02_STRUCTURAL_CHECK.json'),'semanticReview':info(A/'AC5_CURRENT_RETURN_02_SEMANTIC_REVIEW.json'),'expectedReturn':'DD_AC5_Repair_03_Return.zip','newSpellAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    receipt.write_bytes(encoded(submission))
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw); originals[p]=raw;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();assert text.count(previous.relative_to(G).as_posix())==1;text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    marker='**Current GPT conference:**';begin=text.index(marker);end=text.index('\n\n',begin)
    text=text[:begin]+'**Current GPT conference:** The [first complete 16-spell AC5 return](docs/audit/2026-10-08/full-game/DD_AC5_Current_Review_02_Return.zip) is preserved with all 16 source/access records, 17 placements and 54 worked cases. [Independent review](docs/audit/2026-10-08/full-game/AC5_CURRENT_RETURN_02_SEMANTIC_REVIEW.json) found ten repair topics, including 22 invalid current references and inconsistent examples. The [complete repair packet is submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC5_REPAIR_03_SUBMISSION_RECEIPT.json), with 92 frozen sources and the newly located real Flame Drakari spell grant. No AC5 spell is adopted yet; the manuscript count remains 435 reviewed / 413 pending.'+text[end:]
    marker='**Next spell group, prepared for review:**';begin=text.index(marker);end=text.index('\n\n',begin)
    text=text[:begin]+'**Next spell group, prepared for review:** [The AC6 source/interface audit](docs/audit/2026-10-08/full-game/AC6_CURRENT_SOURCE_INTERFACE_AUDIT_01.json) covers 14 identities and 16 printed placements. The [complete planar draft](DescentReviewChanges/ReviewBible/data/director/spell_proposals/ac6_planar_completion_draft_02.json) now supplies Planar Barrier, Greater Planar Ally and both Alignment Nexus operations with 23 examples; [local review](docs/audit/2026-10-08/full-game/AC6_PLANAR_COMPLETION_LOCAL_REVIEW_02.json) records five corrections and 62 passing checks. The [Forge revision](DescentReviewChanges/ReviewBible/data/director/spell_proposals/resonance_forge_revision_02.json) supplies six actual-recipe examples. These remain unsent and unadopted. AC5 dependencies and source bindings must be refreshed before joint AC6 review.'+text[end:]
    start.write_text(text,encoding='utf8',newline='\n')
    planar=R/'data/director/spell_proposals/ac6_planar_completion_draft_02.json';planarcheck=A/'AC6_PLANAR_COMPLETION_LOCAL_REVIEW_02.json'
    assert read(planarcheck)['failureCount']==0
    evidence=[receipt,A/'AC5_CURRENT_RETURN_02_STRUCTURAL_CHECK.json',A/'AC5_CURRENT_RETURN_02_SEMANTIC_REVIEW.json',planar,planarcheck]
    cov=json.loads(originals[ledger]);before=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac5-repair-03-ac6-planar-02','recordedAtUtc':now,'status':'AC5 first return reviewed and returned for repairs; complete AC6 planar draft remains unadopted.','ac5Identities':16,'ac5Cases':54,'ac5StructuralChecks':780,'ac5ReferenceFailures':22,'repairTopics':10,'submittedSources':92,'ac6PlanarIdentities':3,'ac6PlanarOperations':4,'ac6PlanarExamples':23,'ac6LocalChecks':62,'ac6LocalFailures':0,'newSpellAdoptions':0})
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in before['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    code=originals[nav].decode();tail=' + read(A / "AC6_INTERFACE_PREPARATION_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC5_REPAIR_03_AC6_PLANAR_02_NAVIGATION_DELTA.json")["changes"]\n',1)
    additions=[('AC5 — first full return, structural findings','AC5_CURRENT_RETURN_02_STRUCTURAL_CHECK.json'),('AC5 — independent full review and ten repair topics','AC5_CURRENT_RETURN_02_SEMANTIC_REVIEW.json'),('AC5 — repair03 actual GPT submission','AC5_REPAIR_03_SUBMISSION_RECEIPT.json'),('AC6 — complete planar draft local review, not acceptance','AC6_PLANAR_COMPLETION_LOCAL_REVIEW_02.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in additions),1)
    code=code.replace('    featured = [\n','    featured = [\n        ("AC6 — complete planar draft02, awaiting joint review", "DescentReviewChanges/ReviewBible/data/director/spell_proposals/ac6_planar_completion_draft_02.json"),\n',1)
    scope='435 reviewed / 413 pending ordinary spells. Banishment is accepted/applied. The full AC5 first return is preserved; independent review found22 invalid references plus semantic/procedure topics, and ten repair topics with92sources are now submitted to actual GPT Part4. No AC5 adoption yet. Complete AC6 planar draft02 covers3identities/4operations/23examples; Forge02 has6examples. Both remain unadopted and require refresh after AC5. No runtime/human balance or whole-game approval.'
    values=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(values)==1
    code=code.replace(ast.get_source_segment(code,values[0]),repr(scope),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newSpellAdoptions':0,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1500:],run.stderr[-1500:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);prior=deepcopy(state['activeGptReview']);prior.update(status='Complete first return preserved and independently reviewed; requires repair before acceptance.',returnReceived=True,returnedArchive=info(A/'DD_AC5_Current_Review_02_Return.zip'),structuralCheck=info(A/'AC5_CURRENT_RETURN_02_STRUCTURAL_CHECK.json'),semanticReview=info(A/'AC5_CURRENT_RETURN_02_SEMANTIC_REVIEW.json'))
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Independent full AC5 first-return review, repair submission and complete unadopted AC6 planar draft. No rule application.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousAc5Review']=prior
    state['activeGptReview']={'reviewId':'AC5-REPAIR-03','threadId':submission['threadId'],'title':submission['title'],'browserId':'3','tabId':'125746308','conversationUrl':prior['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':submission['status'],'generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_AC5_Repair_03_Return.zip','returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(screenshot),'observationTimeoutMeansTerminal':False}
    state['ac6CurrentPreparation'].update(planarDraft=info(planar),planarLocalReview=info(planarcheck),planarIdentities=3,planarOperations=4,planarWorkedExamples=23,planarLocalChecks=62,planarLocalFailures=0,status='Complete local planar and Forge drafts remain unsent/unadopted. Refresh current AC5 after exact acceptance before joint AC6 review.')
    state['safeNextActions']=['Continue the SAME Part4 AC5 Repair03 user turn52b6d86f-9c53-4976-a528-731bbe5e02b2. It was submitted exactly once; screenshot shows GPT inspecting it. Do not resubmit on an observation timeout.', 'Preserve DD_AC5_Repair_03_Return.zip when actually returned. Verify all92source bindings,16full source/access records/17placements,22historical texts and54retainedcaseIDs plus six or more substantial new cases. Check all current pointers including authored refs and critically resolve all10repair topics.', 'After substantive agreement, obtain exact final-file acceptance and apply only accepted AC5 procedures with source preservation and truthful counts. First-return approval language alone is insufficient while local contradictions remain.', 'Keep complete AC6 planar draft02 and Forge02 separate from accepted rules. Refresh pending AC5 comparisons, hash bindings and relevant planar/antimagic/price/companion decisions before sending the complete14-identity AC6 cohort.', 'The entire75-area goal remains intact: further ordinary spells, environment/disease/consumables, feats, bestiary, Director, packaging, companion implementation and final joint flow. Latest verified GitHub backup18c6e3a predates this local work.']
    state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Preserved and independently reviewed complete16-spell AC5 return; verified source preservation, found22current reference errors and10repair topics, located actual ancestrygrant, submitted92-source repair to actualGPT; saved complete3-identity/4-operation AC6 planar draft with23examples.','evidence':info(receipt)}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'ordinarySpells':state['currentOrdinarySpellCounts'],'newSpellAdoptions':0}))

if __name__=='__main__':main()
