"""Preserve current navigation and record the received arc return plus actual correction review."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'EPILOGUE_ARCS_RETURN_CORRECTIONS_01_SUBMISSION_RECEIPT.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ARCS_RETURN_CORRECTIONS_01.json'
    delta=A/'ARCS_RETURN_CORRECTIONS_01_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-arcs-return-corrections-01'
    assert all(not p.exists() for p in [receipt,target,delta,keep])
    initial=read(A/'EPILOGUE_ARCS_RETURN_CORRECTION_01_NATIVE_DELIVERY.json')
    clarification=read(A/'EPILOGUE_ARCS_GEOMETRY_CLARIFICATION_01_NATIVE_DELIVERY.json')
    request=A/'EPILOGUE_ARCS_RETURN_CORRECTION_REQUEST_01.txt'
    note=A/'EPILOGUE_ARCS_RETURN_GEOMETRY_CLARIFICATION_01.txt'
    assert initial['turns'][0]['items'][0]['content'][0]['text']==request.read_text(encoding='utf8').rstrip()
    assert clarification['turns'][0]['items'][0]['content'][0]['text']==note.read_text(encoding='utf8').rstrip()
    live=A/'EPILOGUE_ARCS_RETURN_CORRECTION_01_LIVE_DOM.txt'
    seen=live.read_text(encoding='utf8')
    assert 'button "Stop"' in seen and 'proper quarter-turn plus translation' in seen
    sourcecheck=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_01.json'
    assert read(sourcecheck)['failureCount']==0
    spells=A/'CURRENT_SPELL_REVIEW_RECONCILIATION_01.json'
    assert read(spells)['failureCount']==0
    rec={'recordedAtUtc':now,'threadTitle':initial['thread']['title'],'threadId':initial['thread']['id'],
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
      'browserId':'3','tabId':'125746308','initialCorrectionUserTurnId':initial['turns'][0]['id'],
      'currentUserTurnId':clarification['turns'][0]['id'],'request':info(request),'geometryClarification':info(note),
      'nativeDelivery':[info(A/n) for n in ['EPILOGUE_ARCS_RETURN_CORRECTION_01_NATIVE_DELIVERY.json','EPILOGUE_ARCS_GEOMETRY_CLARIFICATION_01_NATIVE_DELIVERY.json']],
      'receivedFirstReturn':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_01.zip'),'firstReturnSourceCheck':info(sourcecheck),
      'independentSemanticReview':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_SEMANTIC_REVIEW_01.json'),
      'originalActualVerdict':info(A/'EPILOGUE_ARCS_06_RECEIVED_VERDICT_01_DOM.txt'),
      'liveObservation':info(live),'proof':info(A/'PART4_EPILOGUE_ARCS_GEOMETRY_CLARIFICATION_01_PROOF.jpg'),
      'generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_Cosmology_Epilogue_Campaign_Arcs_02_Return.zip',
      'findings':6,'all75ReceivedCaseIdsMustBePreserved':True,'sourceBindings':51,
      'geometrySupersession':'AR1-05 original x/y swap is superseded ONLY by the preserved actual clarification: xLaunch=30-yVessel,yLaunch=xVessel,zLaunch=zVessel. GPT acknowledged this proper rotation; no source or original review record was erased.',
      'newRulesAdopted':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_ARCS_06_SUBMISSION.json'
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    saved=[];originals={}
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
        originals[p]=b;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode()
    assert text.count(previous.relative_to(G).as_posix())==1
    text=text.replace(previous.relative_to(G).as_posix(),target.relative_to(G).as_posix(),1)
    old='The [EPI-15–17 conference is now submitted and active in Part 4](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_06_SUBMISSION_RECEIPT.json); GPT has verified all 51 sources and is reviewing the three arcs and 21 semantic questions.'
    assert old in text
    text=text.replace(old,'The first EPI-15–17 return is preserved: all 51 sources and 75 authored examples passed the [86 integrity checks](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_01.json). Independent reading found [six correction areas](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_SEMANTIC_REVIEW_01.json); [GPT is reviewing those corrections](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_RETURN_CORRECTIONS_01_SUBMISSION_RECEIPT.json). The three arcs remain unapplied.',1)
    old=next(x for x in text.split('\n\n') if x.startswith('**Later campaign arcs:**'))
    new='**Later campaign arcs:** The complete first return contains the three arcs, 51 unchanged source bindings and 75 authored examples, including all 67 original IDs. Its source-integrity check passes. The independent semantic review requests corrections to shared fragment sealing, the omitted six-second takeoff, already-activated equipment clocks, chapter completeness, coordinate framing and pressure-dependent printing. The [actual correction request and proper-rotation clarification](docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_RETURN_CORRECTIONS_01_SUBMISSION_RECEIPT.json) are now under review in Part 4; wait for the same response and its requested revision02 archive. **No EPI-15–17 procedures have been adopted.**'
    text=text.replace(old,new,1)
    anchor='**Player/Director delivery is still open.**'
    assert anchor in text
    text=text.replace(anchor,'**Spell reference reconciliation:** The [current file audit](docs/audit/2026-10-08/full-game/CURRENT_SPELL_REVIEW_RECONCILIATION_01.json) resolves all 848 identities and confirms 276 legacy + 136 low-rank + 7 DI7 reviewed procedures = **419 reviewed / 429 pending**, with 2,213 reference/preservation checks and no failures. Pending work comprises 180 complete proposals awaiting dedicated review, 201 procedures still to propose, and 48 historical source-only receipts. The historical higher-spell index predates DI7 acceptance; no spell work was lost and no catalog/runtime selection was promoted.\n\n'+anchor,1)
    start.write_text(text,encoding='utf8',newline='\n')
    text=originals[guide].decode();old=next(x for x in text.split('\n\n') if x.startswith('The **EPI-15–17 conference is now active'))
    new='The **first EPI-15–17 return is received and preserved; six corrections are under actual GPT review**. All 51 source bindings and 75 authored examples passed [86 local integrity checks](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_01.json). The [independent semantic review](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_SEMANTIC_REVIEW_01.json) found shared-sealing, takeoff/resource-clock, chapter-coverage, coordinate and pressure-state gaps. The [actual Part4 correction submission](../../../../../docs/audit/2026-10-08/full-game/EPILOGUE_ARCS_RETURN_CORRECTIONS_01_SUBMISSION_RECEIPT.json) includes the later proper-rotation clarification, which supersedes only the initial proposed x/y swap. GPT is rebuilding revision02 from the same sources and must preserve all 75 IDs. EPI-01–14 remains accepted/applied; EPI-15–17 remains unapplied. Campaign-era/identity, runtime, human and balance gates remain open.'
    text=text.replace(old,new,1);guide.write_text(text,encoding='utf8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    for ident in ['DD-11','DD-12','DD-50']:
        row=next(x for x in coverage['aspects'] if x['id']==ident);oldrow=deepcopy(row)
        evidence=[receipt.relative_to(G).as_posix(),rec['independentSemanticReview']['path']] if ident=='DD-50' else [spells.relative_to(G).as_posix()]
        row['validationEvidence'].extend(evidence)
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'arcs-return-corrections01' if ident=='DD-50' else 'spell-current-reference-audit01','recordedAtUtc':now,'evidence':evidence,'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0})
        assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in coverage['aspects'] if x['id'] not in ['DD-11','DD-12','DD-50']]==[x for x in before['aspects'] if x['id'] not in ['DD-11','DD-12','DD-50']]
    ledger.write_bytes(encoded(coverage))
    scope='EPI01–14 remains jointly accepted/applied. First EPI15–17 return received:51 sources,75 authored cases,86 integrity checks pass; six independent semantic correction areas sent to actual Part4, followed by a proper-rotation clarification. GPT is actively rebuilding revision02. Spell audit verifies419 reviewed/429 pending with2213 reference checks. No new arc/catalog rules adopted; owner/human/runtime/full-game gates remain open.'
    code=originals[nav].decode();tail=' + read(A / "EPILOGUE_ARCS_06_SUBMISSION_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "ARCS_RETURN_CORRECTIONS_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(vals)==1;code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    items=[('EPI15–17 — current six-correction review',receipt.name),('EPI15–17 — independent first-return semantic review','COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_SEMANTIC_REVIEW_01.json'),('Ordinary spells — current848-identity reconciliation',spells.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]],'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='verified wait',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='First arc return preserved and independently challenged; no arc application or spell promotion.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousArcSubmission']=state['activeGptReview']
    state['activeGptReview']={'reviewId':'COSMOLOGY-EPILOGUE-CAMPAIGN-ARCS-02','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':rec['currentUserTurnId'],'precedingCorrectionUserTurnId':rec['initialCorrectionUserTurnId'],'status':'Browser verified actively generating the correction review; proper rotation acknowledged.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['campaignArcsFirstReturnReview']=rec
    state['currentSpellReferenceReconciliation']=info(spells)
    state['safeNextActions']=[
      'Poll the SAME actual Part4 response to user turn0896e261-c9ee-410e-afe0-c3e9ca0ba0c4, with the six-finding request at418e8b9e-f5a4-4e9b-bc47-924ebed3374b. Browser Stop and explicit proper-rotation acknowledgment confirm it is live. Do not treat native delivery idle as generation completion.',
      'Download the actual DD_Cosmology_Epilogue_Campaign_Arcs_02_Return.zip when complete; verify byte/hash and check Downloads before repeating a timed-out watcher. Run check_epilogue_arcs_return_01.py with unused suffix02, then additionally verify all75 first-return IDs/order (the generic source checker covers original67 and ARCX01–06 only).',
      'Independently verify every AR1 correction across model, both complete chapters, register and cases, including the proper rotation note. The old x/y swap is superseded. Do not adopt based only on source/manifest checks.',
      'Ordinary spells are authoritatively419 reviewed/429 pending; current reconciliation partitions180 complete unreviewed proposals,201 yet to propose,48 historical receipts. Next prepared cohort is15 rank4 Abjuration/Conjuration procedures; refresh current interfaces before dedicated submission. Do not rerun the historical higher-spell index builder or overwrite historical counts.',
      'Continue environment/consumable/disease, feats, bestiary, Director, packaging and companion work under the75-area ledger. Campaign era remains unanswered; no implied canon/human/runtime/balance/full-game completion.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0}))


if __name__=='__main__':main()
