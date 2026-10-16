"""Record the exact local patch submission without promoting its pending rules."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from pathlib import Path
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'EPILOGUE_ARCS_LOCAL_PATCH_01_SUBMISSION_RECEIPT.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ARCS_LOCAL_PATCH_01_SUBMISSION.json'
    delta=A/'ARCS_LOCAL_PATCH_01_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-arcs-local-patch-01'
    assert not any(p.exists() for p in [receipt,target,delta,keep])
    native=A/'EPILOGUE_ARCS_LOCAL_PATCH_01_NATIVE_DELIVERY.json'
    delivery=read(native)
    request=A/'EPILOGUE_ARCS_LOCAL_PATCH_01_REVIEW_REQUEST.txt'
    turn=delivery['turns'][0]
    delivered_text=turn['items'][0]['content'][0]['text']
    attachment_notice='\n\n[User attached 1 file; file contents were not included]'
    assert delivered_text==request.read_text(encoding='utf8').rstrip()+attachment_notice
    archive=A/'DD_Campaign_Arcs_02_Local_Patch_01.zip'
    attachment=Path(next(x['path'] for x in delivery['attachments'] if x['name']==archive.name))
    assert attachment.read_bytes()==archive.read_bytes()
    live=A/'EPILOGUE_ARCS_LOCAL_PATCH_01_SUBMITTED_DOM.txt'
    assert 'button "Stop"' in live.read_text(encoding='utf8')
    assert read(A/'arcs02-local-patch-01/LOCAL_VALIDATION.json')['failures']==0
    semantic=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_02_SEMANTIC_REVIEW_01.json'
    rec={'recordedAtUtc':now,'threadTitle':delivery['thread']['title'],'threadId':delivery['thread']['id'],
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
      'browserId':'3','tabId':'125746308','userTurnId':turn['id'],'request':info(request),'nativeDelivery':info(native),
      'archive':info(archive),'attachmentByteEqualityVerified':True,'sourceReturn':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_02.zip'),
      'sourceCheck':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_02.json'),'semanticReview':info(semantic),
      'validation':info(A/'arcs02-local-patch-01/LOCAL_VALIDATION.json'),'liveObservation':info(live),
      'proof':info(A/'PART4_EPILOGUE_ARCS_LOCAL_PATCH_01_SUBMITTED.jpg'),'generationConfirmedLiveAtObservation':True,
      'findings':6,'sourceBindings':51,'caseIds':78,'caseRecordsCorrected':3,'modelAndSourceLedgerBytesUnchanged':True,
      'newRulesAdopted':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
      'expectedReturn':'Same-thread exact AR2-01..06 dispositions and full-module verdict for the submitted archive hash, or exact corrections.'}
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ARCS_RETURN_CORRECTIONS_01.json'
    start=G/'START_HERE.md'; guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py'; ledger=R/'data/playtest/game_development_coverage.json'
    saved=[]; originals={}
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes(); q=keep/p.relative_to(G); q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    scope='EPI-01–14 remains jointly accepted/applied. Return02 for EPI-15–17 is preserved with51 unchanged source bindings and78 cases. Six remaining presentation/example regressions are corrected in an exact local package now under actual GPT review;996 preservation/reference/coverage checks pass. Model and source ledger bytes are unchanged. The arcs remain unapplied; runtime, human, balance, canon, whole-game and publication gates remain separate.'
    text=originals[start].decode(); old=previous.relative_to(G).as_posix()
    assert text.count(old)==1;text=text.replace(old,target.relative_to(G).as_posix(),1)
    old='The first EPI-15–17 return is preserved: all 51 sources and 75 authored examples passed the [86 integrity checks](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_01.json). Independent reading found [six correction areas](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_SEMANTIC_REVIEW_01.json); [GPT is reviewing those corrections](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_RETURN_CORRECTIONS_01_SUBMISSION_RECEIPT.json). The three arcs remain unapplied.'
    assert old in text
    text=text.replace(old,'The second EPI-15–17 return is preserved with 51 source bindings and 78 examples. Six remaining presentation/example regressions have an [exact local correction package under GPT review](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_LOCAL_PATCH_01_SUBMISSION_RECEIPT.json). The model and source ledger are unchanged; the three arcs remain unapplied.',1)
    old=next(x for x in text.split('\n\n') if x.startswith('**Later campaign arcs:**'))
    text=text.replace(old,'**Later campaign arcs:** Return02 corrected the six-second takeoff, actual equipment clocks, rotation and current press readiness. Independent reading then found mismatched atmosphere rows, vent timing, lost example scope, incomplete chapters and a new unintended vessel prerequisite. The [source-preserving local patch](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_LOCAL_PATCH_01_SUBMISSION_RECEIPT.json) restores complete chapter coverage and corrects only three of 78 examples; 996 preservation/reference/coverage checks pass. GPT is reviewing the exact package in Part 4. **No EPI-15–17 procedures have been adopted.**',1)
    start.write_text(text,encoding='utf8',newline='\n')
    text=originals[guide].decode();old=next(x for x in text.split('\n\n') if x.startswith('The **first EPI-15–17 return'))
    text=text.replace(old,'The **second EPI-15–17 return is preserved; an exact local correction package is under actual GPT review**. Its 51 source bindings and 78 example IDs are intact. The [independent second-return review](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_02_SEMANTIC_REVIEW_01.json) documents six remaining presentation/example regressions. The [submitted local patch](../../../../../docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_LOCAL_PATCH_01_SUBMISSION_RECEIPT.json) preserves the model and source ledger byte-for-byte, restores full chapter procedures, and corrects three examples. All 996 local preservation/reference/coverage checks pass; these are not runtime or human tests. Await the same Part4 response and exact full-module verdict. EPI-01–14 remains applied; EPI-15–17 remains unapplied. Campaign-era/identity, balance and whole-game gates remain open.',1)
    guide.write_text(text,encoding='utf8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    evidence=[receipt.relative_to(G).as_posix(),semantic.relative_to(G).as_posix()]
    row['validationEvidence'].extend(evidence)
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'arcs-local-patch01-submission','recordedAtUtc':now,'evidence':evidence,'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0})
    assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in before['aspects'] if x['id']!='DD-50']==[x for x in coverage['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    code=originals[nav].decode();tail=' + read(A / "ARCS_RETURN_CORRECTIONS_01_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1;code=code.replace(tail,tail.rstrip('\n')+' + read(A / "ARCS_LOCAL_PATCH_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(vals)==1;code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    items=[('EPI15–17 — current exact local correction review',receipt.name),('EPI15–17 — independent second-return semantic review',semantic.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]],'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Exact arc corrections submitted for actual GPT review; no rule adoption.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousArcCorrectionReview']=state['activeGptReview']
    state['activeGptReview']={'reviewId':'ARCS02-LOCAL-PATCH01','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':'Actual browser confirmed generating after submission; attachment bytes verified against local archive.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['campaignArcsSecondReturnLocalPatchReview']=rec
    state['safeNextActions']=[
      'Read the SAME Part4 response to user turn '+turn['id']+'. Do not infer completion from native delivery status; inspect the actual browser terminal response.',
      'Independently assess each AR2 disposition and full-module verdict against the exact archive hash. If more changes are required, preserve all prior bytes and apply only verified exact corrections. No arc application before actual joint agreement.',
      'If accepted, apply the three conditional arcs and78 examples with source-preserving bindings and player/Director separation, validate integration, and update navigation. Keep original source/cosmology authority and campaign-era holds intact.',
      'Continue current spell backlog from419 reviewed/429 pending; next prepared cohort is15 rank4 Abjuration/Conjuration procedures requiring refreshed interfaces. Do not rerun historical count builders.',
      'Continue the remaining75-area ledger including environment, consumables, disease, feats, bestiary, Director, packaging and companion. Human/runtime/balance/full-game gates remain open.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0,'attachmentByteEquality':True}))

if __name__=='__main__':main()
