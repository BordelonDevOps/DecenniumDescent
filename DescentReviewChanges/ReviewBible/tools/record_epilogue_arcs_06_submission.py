"""Record actual51-source arc submission and preserve the preceding owner navigation."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat();receipt=A/'EPILOGUE_ARCS_06_SUBMISSION_RECEIPT.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_ARCS_06_SUBMISSION.json'
    delta=A/'EPILOGUE_ARCS_06_SUBMISSION_NAVIGATION_DELTA.json';keep=A/'navigation-before-epilogue-arcs-06-submission'
    assert all(not p.exists() for p in [receipt,target,delta,keep])
    native=A/'EPILOGUE_ARCS_06_NATIVE_DELIVERY.json';payload=read(native)['nativeRead'];turn=payload['turns'][0]
    assert turn['id']=='0ff98622-2f94-4489-871b-38a165008c05'
    archive=A/'DD_Cosmology_Epilogue_Campaign_Arcs_06.zip'
    attached=Path(next(x['path'] for x in payload['attachments'] if x['name']==archive.name))
    assert attached.read_bytes()==archive.read_bytes()
    message=A/'EPILOGUE_ARCS_06_SUBMISSION_MESSAGE.txt';assert turn['items'][0]['content'][0]['text'].startswith(message.read_text(encoding='utf-8').rstrip())
    live=A/'EPILOGUE_ARCS_06_LIVE_ACKNOWLEDGEMENT_DOM.txt';seen=live.read_text(encoding='utf-8')
    assert '51/51 source bindings verify exactly' in seen and 'button "Stop"' in seen
    proof=A/'PART4_EPILOGUE_ARCS_06_SUBMISSION_PROOF.jpg';assert proof.exists()
    checker=R/'tools/check_epilogue_arcs_return_01.py';assert checker.exists()
    rec={'recordedAtUtc':now,'threadTitle':payload['thread']['title'],'threadId':payload['thread']['id'],'browserId':'3','tabId':'125746308','userTurnId':turn['id'],
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
      'archive':info(archive),'preparation':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_06_PREPARATION.json'),'request':info(message),'nativeDelivery':info(native),'uploadedBytesExactlyMatch':True,
      'submissionProof':info(proof),'liveAcknowledgement':info(live),'sourceBindings':51,'originalCaseIds':67,'requiredCrossModuleCases':6,'semanticQuestions':21,
      'actualGptSourceVerification':'51/51 source bindings verify exactly','generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_Cosmology_Epilogue_Campaign_Arcs_01_Return.zip','returnReceived':False,
      'returnChecker':info(checker),'newRulesAdopted':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    receipt.write_bytes(encoded(rec));previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_APPLICATION_01.json'
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b);originals[p]=b;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();assert text.count(previous.relative_to(G).as_posix())==1
    text=text.replace(previous.relative_to(G).as_posix(),target.relative_to(G).as_posix(),1)
    text=text.replace('Next is the prepared EPI-15–17 conference, followed by the remaining game systems and content.','The [EPI-15–17 conference is now submitted and active in Part 4](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_06_SUBMISSION_RECEIPT.json); GPT has verified all 51 sources and is reviewing the three arcs and 21 semantic questions. The remaining game systems and content follow.',1)
    old=next(x for x in text.split('\n\n') if x.startswith('**Later campaign arcs:**'))
    new='**Later campaign arcs:** The [revision06 packet](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_06_PREPARATION.json) preserves all 44 earlier sources and 67 draft examples, adding seven current references for a total of 51. It is now submitted to actual Review Continuation Part4. GPT has verified those source bytes and is reviewing the fifteen original semantic questions plus six relic/Null integration questions. The requested return includes all 67 original cases plus at least six new integration examples. **These arcs remain unadopted**, conditional on a compatible campaign frame; the owner era and unresolved identities are not being chosen.'
    text=text.replace(old,new,1);start.write_text(text,encoding='utf-8',newline='\n')
    text=originals[guide].decode();old=next(x for x in text.split('\n\n') if x.startswith('The **current EPI-15–17 local proposal'))
    new='The **EPI-15–17 conference is now active in actual Review Continuation Part4**. The [51-source revision06 packet](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_06_PREPARATION.json) preserves the full three-arc model and67 authored examples from revision05, its44 original source records and all earlier refinements. Seven added current references carry the accepted EPI-08–14 and creature/sharing/roster interfaces. [Actual delivery is verified](../../../../../docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_06_SUBMISSION_RECEIPT.json); GPT acknowledged51/51 source hashes and is reviewing all21 semantic questions. The requested archive must preserve67 cases and add ARCX-01–06. Earlier unavailable-return status is historical; EPI-08–14 is already applied. The arcs themselves remain unadopted, with unresolved campaign-era/identity and human/runtime/balance gates unchanged.'
    text=text.replace(old,new,1).replace('EPI-15–17 remains prepared for its own conference.','EPI-15–17 is now in its own actual conference, as described below.',1);guide.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['draftEvidence'].extend([receipt.relative_to(G).as_posix(),rec['preparation']['path']])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'epilogue-arcs06-submission','recordedAtUtc':now,'sourceBindings':51,'preservedDraftCases':67,'requestedNewCases':6,'semanticQuestions':21,'actualSubmissionVerified':True,'actualGptSourceHashesVerified':51,'newRulesAdopted':False})
    assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass']);assert [x for x in before['aspects'] if x['id']!='DD-50']==[x for x in coverage['aspects'] if x['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='EPI01–14 remains jointly accepted/applied. EPI15–17 revision06 is actually submitted in Part4:51 verified sources,67 unchanged draft cases,21 semantic questions and6 requested cross-module cases. GPT confirmed51/51 hashes and is actively reviewing. No new arc rules adopted; full game and owner/human/runtime gates remain open.'
    code=originals[nav].decode();tail=' + read(A / "RELIC_NULL_APPLICATION_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_ARCS_06_SUBMISSION_NAVIGATION_DELTA.json")["changes"]\n',1)
    values=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(values)==1
    code=code.replace(ast.get_source_segment(code,values[0]),repr(scope),1)
    items=[('EPI15–17 — actual51-source conference submission',receipt.name),('EPI15–17 — current51-source preparation','COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_06_PREPARATION.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]],'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Actual three-arc conference submitted; earlier EPI01–14 acceptance remains. No arc rules applied.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousGptReviewEpi08Through14']=state['activeGptReview']
    state['activeGptReview']={'reviewId':'COSMOLOGY-EPILOGUE-CAMPAIGN-ARCS-01','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':'Browser verified active; exact51-source verification acknowledged; three-arc semantic review underway.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False,'returnChecker':info(checker)}
    state['campaignArcsRevision06']={'preparation':rec['preparation'],'archive':rec['archive'],'submission':info(receipt),'draftCases':67,'sourceCount':51,'jointReviewComplete':False,'adopted':False}
    state['safeNextActions']=['Poll the SAME actual Part4 response to user turn0ff98622-2f94-4489-871b-38a165008c05. GPT has verified51/51 source hashes and is actively reviewing. Native idle delivery status is not evidence that this browser generation stopped.','When complete, download DD_Cosmology_Epilogue_Campaign_Arcs_01_Return.zip. Verify reported byte/hash and check Downloads before repeating any timed-out download watcher. Run check_epilogue_arcs_return_01.py once with an unused suffix.','Then independently review source fidelity, full prose, all67 retained plus6 required examples, actual adventure choices, mass/support/air/contract/relic interfaces and any new changes. All arcs remain unadopted until real joint acceptance. Do not reopen accepted EPI01–14.','Remaining environment/consumable/disease, ordinary spells, feats, bestiary, Director, packaging and companion work stays open under the75-area ledger; owner campaign era remains unresolved.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope};state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'submission':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0}))

if __name__=='__main__':main()
