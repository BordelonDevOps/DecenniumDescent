"""Record the complete independent review and actual correction-conference delivery."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'AC4_CORRECTIONS_02_SUBMISSION_RECEIPT.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC4_CORRECTIONS_02_SUBMISSION.json'
    delta=A/'AC4_CORRECTIONS_02_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-ac4-corrections-02'
    assert not any(p.exists() for p in [receipt,target,delta,keep])
    native=A/'AC4_CORRECTIONS_02_NATIVE_DELIVERY.json';delivery=read(native);turn=delivery['turns'][0]
    request=A/'AC4_CORRECTIONS_02_REQUEST.txt';archive=A/'DD_AC4_Corrections_02.zip';prep=A/'AC4_CORRECTIONS_02_PREPARATION.json'
    assert turn['items'][0]['content'][0]['text']==request.read_text(encoding='utf8').rstrip()+'\n\n[User attached 1 file; file contents were not included]'
    attachment=Path(next(x['path'] for x in delivery['attachments'] if x['name']==archive.name))
    assert attachment.read_bytes()==archive.read_bytes()
    assert read(prep)['failureCount']==0 and read(prep)['archive']==info(archive)
    live=A/'AC4_CORRECTIONS_02_SUBMITTED_DOM.txt'
    assert 'button "Stop"' in live.read_text(encoding='utf8')
    rec={'recordedAtUtc':now,'threadTitle':delivery['thread']['title'],'threadId':delivery['thread']['id'],'userTurnId':turn['id'],
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8','browserId':'3','tabId':'125746308',
      'request':info(request),'archive':info(archive),'preparation':info(prep),'nativeDelivery':info(native),'attachmentByteEqualityVerified':True,
      'liveObservation':info(live),'proof':info(A/'PART4_AC4_CORRECTIONS_02_SUBMITTED.jpg'),'generationConfirmedLiveAtObservation':True,
      'priorReturn':info(A/'DD_AC4_Current_Review_01_Return_01.zip'),'priorReturnSourceCheck':info(A/'AC4_CURRENT_REVIEW_01_RETURN_SOURCE_CHECK_01.json'),
      'independentFindings':info(A/'ac4-corrections-02-input/INDEPENDENT_FINDINGS.json'),'semanticReadingCompleted':True,'findings':8,'originalExamples':30,'integrationExamples':15,
      'expectedReturn':'DD_AC4_Corrections_02_Return.zip','cards':15,'sourceFiles':70,'currentSourceAndProseChecks':85,
      'banishmentDraft':info(A/'BANISHMENT_LOCAL_DRAFT_01_PREPARATION.json'),'banishmentStatus':'Unsubmitted/unadopted local discussion draft; six open questions remain. Old pre-push hold satisfied.',
      'currentAuthoredSpellCounts':{'reviewed':419,'pending':429},'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC4_CURRENT_REVIEW_01_SUBMISSION.json'
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);originals[p]=raw
        saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();old=previous.relative_to(G).as_posix();assert text.count(old)==1;text=text.replace(old,target.relative_to(G).as_posix(),1)
    begin=text.index('**Active spell review:**');end=text.index('\n\n',begin)
    paragraph='**Active spell review:** The first 15-card AC4 return is preserved and independently read, with 175 source-integrity checks passing. [Eight semantic/completeness findings](docs/audit/2026-10-08/full-game/ac4-corrections-02-input/INDEPENDENT_FINDINGS.json) are [submitted to actual GPT in Part4](docs/audit/2026-10-08/full-game/AC4_CORRECTIONS_02_SUBMISSION_RECEIPT.json) with all70 unchanged source files, the complete prior return, and eight exact comparison records. A further85 current-source/prose checks pass. Corrections cover clocks, faction eligibility, damage-root creation, Null at0, the missing Envoy profile, healing/transport predicates, exact Steed identity and concrete integration examples. No spell adoption yet:419 reviewed/429 pending. [Banishment has a separate unadopted local draft](docs/audit/2026-10-08/full-game/BANISHMENT_LOCAL_DRAFT_01_PREPARATION.json),18 conditional authored examples and six open questions; its old wait-for-push restriction is satisfied.'
    text=text[:begin]+paragraph+text[end:];start.write_text(text,encoding='utf8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in coverage['aspects'] if x['id']==ident);oldrow=deepcopy(row)
        row['validationEvidence'].extend([prep.relative_to(G).as_posix(),receipt.relative_to(G).as_posix(),rec['independentFindings']['path'],rec['banishmentDraft']['path']])
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac4-corrections02-submission','recordedAtUtc':now,'cards':15,'sources':70,'semanticFindings':8,'currentSourceAndProseChecks':85,'failureCount':0,'newRulesAdopted':False,'runtimeTestsExecuted':0})
        assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in before['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in coverage['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(coverage))
    scope='EPI-01–17 applied provisionally. First15-spell AC4 return independently read and source-checked; eight semantic/completeness findings now submitted to actual Part4 with70 unchanged sources,45 existing examples and full prior return. Banishment local draft unsubmitted with six open questions. Current spells419 reviewed/429 pending; no new adoption or human/runtime/balance/whole-game approval.'
    code=originals[nav].decode();tail=' + read(A / "AC4_CURRENT_REVIEW_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC4_CORRECTIONS_02_NAVIGATION_DELTA.json")["changes"]\n',1)
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    items=[('AC4 — eight findings correction conference',receipt.name),('AC4 — first returned candidate source checks','AC4_CURRENT_REVIEW_01_RETURN_SOURCE_CHECK_01.json'),('Banishment — unadopted discussion draft','BANISHMENT_LOCAL_DRAFT_01_PREPARATION.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='no progress: continuation visibility/status confirmation only; revalidated and advanced this turn',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='No spell adoption; complete semantic review and correction submission only.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousAc4Review']=state['activeGptReview'];state['previousAc4Review'].update(returnReceived=True,status='Complete actual return preserved and independently reviewed; eight findings require resolution before adoption.',returnArchive=rec['priorReturn'])
    state['activeGptReview']={'reviewId':'AC4-CORRECTIONS-02','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':'Actual browser confirmed generating after exact correction-archive submission; attachment bytes verified.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['ac4Corrections02']=rec;state['banishmentLocalDraft']=read(A/'BANISHMENT_LOCAL_DRAFT_01_PREPARATION.json')
    state['safeNextActions']=['Poll SAME actual Part4 response to user turn '+turn['id']+'. Observe browser completion, not native idle alone; do not resubmit on observation timeout.','Preserve DD_AC4_Corrections_02_Return.zip; verify70 source bindings,15 IDs/full original records,30 original case texts and X01..15 identities, all eight finding dispositions and full playable profiles. Independently review all actual changes before adoption.','Banishment draft remains unsubmitted/unadopted, with six explicit open questions and conditional18 examples. Resolve finite-cell termination, visitors, blocked returns and current corrected transport interfaces with actual GPT before promotion.','Current ordinary spells419 reviewed/429 pending. EPI-01–17 is applied within provisional scope; no need to reopen that completed conference. Continue the full75-area backlog after these exact integrations.','Latest verified GitHub backup18c6e3a; final coherent authored-candidate joint review and delivery remain required. Human/runtime/balance/publication gates are separate and unproven.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0,'attachmentByteEquality':True}))

if __name__=='__main__':main()
