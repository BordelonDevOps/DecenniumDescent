"""Record actual Part4 delivery, superseding the old notebook connection blocker."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'PART4_RELIC_NULL_HANDOFF_01_SUBMISSION.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PART4_HANDOFF_01.json'
    delta=A/'PART4_HANDOFF_01_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-part4-handoff-01'
    assert all(not p.exists() for p in [receipt,target,delta,keep])
    packet=A/'DD_Part4_Relic_Null_Revision_Handoff_01.zip'
    native=A/'PART4_RELIC_NULL_HANDOFF_01_NATIVE_DELIVERY.json'
    proof=A/'PART4_RELIC_NULL_SUBMISSION_PROOF_01.jpg'
    prep=A/'PART4_RELIC_NULL_HANDOFF_01_PREPARATION.json'
    payload=read(native)['nativeRead'];turn=payload['turns'][0]
    assert payload['thread']['id']=='6ad1acef-455c-83ea-bc33-56e4adaec9c8'
    assert turn['id']=='f02d58a7-e558-4945-b4c5-093dd732ba4f'
    assert any(a['name']==packet.name for a in payload['attachments'])
    from pathlib import Path
    attachment=Path(next(a['path'] for a in payload['attachments'] if a['name']==packet.name))
    assert attachment.read_bytes()==packet.read_bytes()
    text='\n'.join(c['text'] for item in turn['items'] if item['type']=='userMessage' for c in item['content'] if c['type']=='text')
    assert 'RNX-01–14' in text and '84 total' in text
    rec={'recordedAtUtc':now,'destinationTitle':'Review Continuation Part 4','threadId':payload['thread']['id'],
      'browserId':'3','tabId':'125746308','conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
      'preparation':info(prep),'submittedArchive':info(packet),'nativeDelivery':info(native),'proofScreenshot':info(proof),
      'userTurnId':turn['id'],'actualUserPrompt':text,'attachmentBytesMatchLocalArchive':True,'submitted':True,
      'browserGenerationEvidence':{'statusAtObservation':'Generating; Stop control visible; assistant progress text verified',
         'heading':'Inspecting Original Zips and Semantic Review Data',
         'assistantProgressExcerpt':'The handoff itself verifies exactly: 3,236,968 bytes and SHA-256 2f5c9116e8afea759c99b5fcea014f5208cc620c4c544b10418b31f92462379c. I’ve also confirmed it contains the preserved original GPT return, original 83-source review packet, semantic audit, revision request, three application receipts, and the current creature-lifecycle source as the 84th binding.',
         'scope':'Observed browser progress, not a completed verdict or returned archive. Recheck this same live conversation; do not restart from the native user-turn completed/idle fields alone.'},
      'openingCheckpointCorrection':'Part4 initially proposed restarting souls/death. Actual later application receipts and current EPI08–14 revision task were supplied and acknowledged.',
      'originalSources':83,'additionalCurrentSources':1,'findingsSubmitted':14,'originalCases':47,'requestedAdditionalCases':28,
      'expectedReturn':'DD_Cosmology_Epilogue_Relic_Null_02_Return.zip','returnReceived':False,'newRulesAdopted':False,
      'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanBalanceApproved':False,'wholeGameFlowConfirmed':False}
    receipt.write_bytes(encoded(rec))
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    operations={start:[],guide:[]}
    def replace(p,old,new):
        value=p.read_text(encoding='utf-8');assert value.count(old)==1,(str(p),old)
        p.write_text(value.replace(old,new,1),encoding='utf-8',newline='\n');operations[p].append({'old':old,'replacement':new})
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_RECOVERY_01.json'
    replace(start,previous.relative_to(G).as_posix(),target.relative_to(G).as_posix())
    replace(start,'Chrome reading/download works, while the chat currently displays a usage-limit alert. The [revision request](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_REVISION_REQUEST.txt) is prepared, not submitted.',
      'The [current review has been submitted to Review Continuation Part 4](docs/audit/2026-10-08/full-game/PART4_RELIC_NULL_HANDOFF_01_SUBMISSION.json). GPT has verified the uploaded handoff and all 84 source bindings and is working on the correction request. The opening stale checkpoint was corrected with actual application receipts; no earlier completed module is being restarted.')
    replace(start,'Actual GPT exchange remains unavailable: the delivered [text-only four-item review](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_FOUR_HOLDS_TEXT_REVIEW_01.json) ended without an assistant reply. No live generation is verified.',
      'The earlier [text-only four-item review](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_FOUR_HOLDS_TEXT_REVIEW_01.json) still has no assistant reply. Actual joint work has resumed in Part 4 on the EPI-08–14 correction packet; the consumable and environment packets await their own later review.')
    value=guide.read_text(encoding='utf-8');old=next(x for x in value.split('\n\n') if x.startswith('**Current recovery point:**'))
    replace(guide,old,'**Current review:** The exact EPI-08–14 original return is [preserved locally](../../../../../docs/audit/2026-10-08/full-game/DD_Cosmology_Epilogue_Relic_Null_01_Return_01.zip), with its original size/hash and all 234 source/file/citation checks verified. The [semantic audit](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.md) has 14 correction findings and 28 required scenarios. The [complete handoff was submitted to Review Continuation Part 4](../../../../../docs/audit/2026-10-08/full-game/PART4_RELIC_NULL_HANDOFF_01_SUBMISSION.json); GPT verified the packet and all 84 bindings, including the added current companion-lifecycle reference, and began the revision. **No EPI-08–14 rule is adopted.** The previous Part3 limit is historical; use the actual Part4 conversation and wait for its corrected return rather than restarting old exports or already-applied conferences.')
    replace(guide,'Exact EPI-08–14 recovery/integration, joint semantic review, final Player/Director prose and the owner campaign era remain open.',
      'Exact EPI-08–14 recovery is complete. Its correction review/integration, final Player/Director prose and the owner campaign era remain open.')
    replace(guide,'The review is the same Part3 conversation; the current readable Chrome3 tab is125746298 (Calibration Review Continuation), with a visible usage-limit alert.',
      'The current review is Review Continuation Part 4 in Chrome3/tab125746308; its thread is6ad1acef-455c-83ea-bc33-56e4adaec9c8. Earlier Part3 records remain preserved.')
    replace(guide,'Part 3 is active and no continuation permission is pending.','Part 4 is current and no continuation permission is pending.')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['draftEvidence'].extend([prep.relative_to(G).as_posix(),receipt.relative_to(G).as_posix()])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'part4-epilogue-relic-null-revision-submission01','recordedAtUtc':now,
       'actualConversation':'Review Continuation Part 4','sourceBindings':84,'revisionFindings':14,'requestedCases':75,
       'submitted':True,'sourceVerificationAcknowledgedByGpt':True,'returnReceived':False,'newRulesAdopted':False})
    for k in ['status','closure','humanEvidence','completionClass']:assert row[k]==oldrow[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope='Actual review resumed in Review Continuation Part4, thread6ad1acef-455c-83ea-bc33-56e4adaec9c8/tab125746308. EPI08–14 correction packet submitted and acknowledged:84 bound sources,14 RNX findings,47 original plus28 requested cases. Browser shows live source inspection; native user-turn idle/completed is only delivery metadata. Exact original return preserved; corrected return not yet received. No new rules or whole-game gates adopted.'
    code=originals[nav].decode();tail=' + read(A / "RELIC_NULL_RECOVERY_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "PART4_HANDOFF_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('Part4 — actual revision submission and verified progress',receipt.name),('Part4 — exact handoff archive',packet.name),('Part4 — submission screenshot',proof.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]]
    for change,p in zip(changes,[start,guide,ledger,nav]):
        if p in operations:change['operations']=operations[p]
        elif p==ledger:change['operations']=[{'aspectId':'DD-50','old':oldrow,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-2500:]);raise SystemExit(run.returncode)
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',
      status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,
      newRuleAdoptionScope='Actual Part4 correction conference submitted; no revised rule applied.',
      navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousActiveGptReviewBeforePart4']=state['activeGptReview']
    state['activeGptReview']={'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-RELIC-NULL-02','threadId':rec['threadId'],
      'title':rec['destinationTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],
      'submission':info(receipt),'archive':info(packet),'status':'Browser generation verified; source packet acknowledged, correction work underway.',
      'generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False,
      'readinessCheck':info(R/'tools/check_cosmology_epilogue_relic_null_return_02.py')}
    state['part4Handoff']=info(receipt)
    state['safeNextActions']=['Recheck the SAME actual Part4 browser conversation for the current response; Stop/source-inspection progress was verified. Native delivery-only idle metadata must not trigger a duplicate authoring request.',
      'When the revision finishes, retrieve its exact original ZIP, verify eight roots/84 sources/all47+28 case IDs with the prepared02 checker, then independently review all14 semantic corrections before adoption.',
      'Keep the later arcs, consumable and environment drafts separate and unadopted until their own actual joint conferences. Preserve the original return and all owner/source constraints.']
    state['resumedBlockedAudit']={'classification':'progress','previousConnectionBlockerResolved':True,'evidence':info(receipt),
      'meaningfulProgress':'Owner created Part4; actual84-source correction handoff submitted, received and verified by GPT. Current generation observed in browser.'}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'submission':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0,'sourceBindings':84,'newRulesAdopted':False}))

if __name__=='__main__':main()
