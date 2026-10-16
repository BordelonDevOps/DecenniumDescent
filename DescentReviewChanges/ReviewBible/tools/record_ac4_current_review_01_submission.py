"""Record actual delivery of the current fifteen-spell conference."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'AC4_CURRENT_REVIEW_01_SUBMISSION_RECEIPT.json';target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC4_CURRENT_REVIEW_01_SUBMISSION.json'
    delta=A/'AC4_CURRENT_REVIEW_01_NAVIGATION_DELTA.json';keep=A/'navigation-before-ac4-current-review-01'
    assert not any(p.exists() for p in [receipt,target,delta,keep])
    native=A/'AC4_CURRENT_REVIEW_01_NATIVE_DELIVERY.json';delivery=read(native);turn=delivery['turns'][0]
    request=A/'AC4_CURRENT_REVIEW_01_REQUEST.txt';archive=A/'DD_AC4_Current_Review_01.zip';prep=A/'AC4_CURRENT_REVIEW_01_PREPARATION.json'
    assert turn['items'][0]['content'][0]['text']==request.read_text(encoding='utf8').rstrip()+'\n\n[User attached 1 file; file contents were not included]'
    attachment=Path(next(x['path'] for x in delivery['attachments'] if x['name']==archive.name));assert attachment.read_bytes()==archive.read_bytes()
    assert read(prep)['failureCount']==0 and read(prep)['archive']==info(archive)
    live=A/'AC4_CURRENT_REVIEW_01_SUBMITTED_DOM.txt';assert 'button "Stop"' in live.read_text(encoding='utf8')
    rec={'recordedAtUtc':now,'threadTitle':delivery['thread']['title'],'threadId':delivery['thread']['id'],'userTurnId':turn['id'],
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8','browserId':'3','tabId':'125746308',
      'request':info(request),'archive':info(archive),'preparation':info(prep),'nativeDelivery':info(native),'attachmentByteEqualityVerified':True,'liveObservation':info(live),'proof':info(A/'PART4_AC4_CURRENT_REVIEW_01_SUBMITTED.jpg'),
      'generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_AC4_Current_Review_01_Return.zip','cards':15,'originalExamples':30,'requestedIntegrationExamples':15,'sourceFiles':70,'currentInterfaceQuestions':9,'sourceChecks':151,
      'currentAuthoredSpellCounts':{'reviewed':419,'pending':429},'banishment':'Historical sequencing hold satisfied; separate complete-procedure authoring still required, excluded from these15.',
      'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CAMPAIGN_ARCS_APPLICATION_01.json'
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);originals[p]=raw
        saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();old=previous.relative_to(G).as_posix();assert text.count(old)==1;text=text.replace(old,target.relative_to(G).as_posix(),1)
    anchor='**Prepared disease-interface audit:**';assert text.count(anchor)==1
    text=text.replace(anchor,'**Active spell review:** The [15-card Abjuration/Conjuration conference](docs/audit/2026-10-08/full-game/AC4_CURRENT_REVIEW_01_SUBMISSION_RECEIPT.json) is now submitted to actual GPT in Part4. It carries 70 current source files, all17 class envelopes, 30 original examples, 15 requested integration examples and nine current-interface questions. Its 151 source/preservation checks pass. These spells remain unadopted until exact review; the current total is still419 reviewed/429 pending. Banishment is a separate source-only authoring obligation; its old wait-for-push restriction has been satisfied.\n\n'+anchor,1)
    start.write_text(text,encoding='utf8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in coverage['aspects'] if x['id']==ident);oldrow=deepcopy(row)
        row['validationEvidence'].extend([prep.relative_to(G).as_posix(),receipt.relative_to(G).as_posix()])
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac4-current-review01-submission','recordedAtUtc':now,'cards':15,'sources':70,'originalExamples':30,'requestedIntegrationExamples':15,'sourceChecks':151,'failureCount':0,'newRulesAdopted':False,'runtimeTestsExecuted':0})
        assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in before['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in coverage['aspects'] if x['id'] not in ['DD-11','DD-12']];ledger.write_bytes(encoded(coverage))
    scope='EPI-01–17 jointly reviewed and locally applied as provisional authored material. Actual Part4 now reviews15 AC4 spells against70 current sources/all17 class envelopes,30 original and15 requested integration examples,9 interface questions;151 source checks pass. Current spells419 reviewed/429 pending. No new spell adoption or human/runtime/balance/whole-game approval.'
    code=originals[nav].decode();tail=' + read(A / "CAMPAIGN_ARCS_APPLICATION_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC4_CURRENT_REVIEW_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    items=[('AC4 — current15-spell joint review',receipt.name),('AC4 — refreshed70-source packet',prep.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Arc application recorded in previous checkpoint; this submission adopts no spell procedures.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['completedCampaignArcsReview']=state['activeGptReview']
    state['activeGptReview']={'reviewId':'AC4-CURRENT-REVIEW-01','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':'Actual browser confirmed generating after exact archive submission; attached bytes verified.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['ac4CurrentReview']=rec
    state['safeNextActions']=['Poll the SAME actual Part4 response to user turn '+turn['id']+'. Native delivery status alone does not prove generation complete.','Receive DD_AC4_Current_Review_01_Return.zip; preserve exact bytes, verify70 source bindings and all15 original cards/30 example IDs plus15 requested integration examples, then independently read every procedure, question disposition and whole-module verdict. Do not adopt on source checks alone.','Banishment remains next separate procedure-authoring work using current planes/souls/travel sources; its old push-order hold is satisfied. Do not treat it as permanently blocked or already reviewed.','EPI-01–17 is applied within provisional authored scope; do not reopen that completed conference. Preserve campaign-era and identity holds. Continue remaining spells, environment/consumables/disease, feats, bestiary, Director, packaging and companion under the75-area ledger.','Current ordinary spells419 reviewed/429 pending; no new spell promoted. Latest verified GitHub backup18c6e3a. Joint whole-game flow and authorized final delivery remain required; human/runtime/balance gates remain separate.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope};state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0,'attachmentByteEquality':True}))

if __name__=='__main__':main()
