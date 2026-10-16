"""Record the recovered revision, actual patch approval and pending final module review."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'RELIC_NULL_03_LOCAL_PATCH_01_REVIEW_RECEIPT.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_PATCH_REVIEW_01.json'
    delta=A/'RELIC_NULL_PATCH_REVIEW_01_NAVIGATION_DELTA.json';keep=A/'navigation-before-relic-null-patch-review-01'
    assert all(not x.exists() for x in [receipt,target,delta,keep])
    confirmation=A/'RELIC_NULL_03_LOCAL_PATCH_01_CONFIRMATION_DOM.txt';seen=confirmation.read_text(encoding='utf-8')
    archive=A/'DD_Relic_Null_03_Local_Patch_01.zip';assert info(archive)['sha256'] in seen
    assert all(f'RN3-{i:02} —' in seen for i in range(1,10)) and seen.count('strong: AGREE.')==9
    assert 'No replacement text is required' in seen
    validation=A/'RELIC_NULL_03_LOCAL_PATCH_01_VALIDATION.json';assert read(validation)['failureCount']==0
    native=A/'RELIC_NULL_LOCAL_PATCH_01_NATIVE_DELIVERY.json';payload=read(native)['nativeRead'];turn=payload['turns'][0]
    proof=A/'PART4_RELIC_NULL_FINAL_MODULE_01_SUBMISSION_PROOF.jpg';assert proof.exists()
    rec={'recordedAtUtc':now,'threadTitle':'Review Continuation Part 4','threadId':payload['thread']['id'],'browserId':'3','tabId':'125746308',
      'patchSubmittedUserTurnId':turn['id'],'nativeDelivery':info(native),'archive':info(archive),
      'revision03Archive':info(A/'DD_Cosmology_Epilogue_Relic_Null_03_Return_01.zip'),
      'revision03SourceCheck':info(A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_RETURN_SOURCE_CHECK_01.json'),
      'semanticReview':info(A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_SEMANTIC_REVIEW_01.json'),
      'patchValidation':info(validation),'patchConfirmation':info(confirmation),'patchApprovedGroups':9,
      'approvalScope':'Exact RN3-01..09 correction patch approved by actual GPT; not yet a complete-module acceptance.',
      'completeModuleRequest':info(A/'RELIC_NULL_03_FINAL_MODULE_REVIEW_REQUEST_01.txt'),'completeModuleSubmissionProof':info(proof),
      'completeModuleReplyReceived':False,'newRulesAdopted':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DISEASE_INTERFACE_AUDIT_01.json'
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);originals[p]=raw
        saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();old=next(s for s in text.split('\n\n') if s.startswith('**Current joint review:**'))
    current='**Current joint review:** EPI-01–07 remains jointly confirmed and locally applied. For EPI-08–14, [revision03 is preserved](docs/audit/2026-10-08/full-game/DD_Cosmology_Epilogue_Relic_Null_03_Return_01.zip) and passed [247 source checks](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_03_RETURN_SOURCE_CHECK_01.json). Codex completed the prose and 75-example review, then supplied a [bounded correction patch](docs/audit/2026-10-08/full-game/DD_Relic_Null_03_Local_Patch_01.zip). **GPT agreed with all nine corrections and the exact archive hash.** Its 87 preservation/replay checks passed. The [complete-module verdict is now requested in Review Continuation Part 4](docs/audit/2026-10-08/full-game/RELIC_NULL_03_LOCAL_PATCH_01_REVIEW_RECEIPT.json); no EPI-08–14 rule has yet been applied. Continue from the [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_PATCH_REVIEW_01.json), [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md) or [review map](REVIEW_MAP.html). Ordinary spells remain **419 reviewed / 429 pending**. Campaign era, unresolved identities, runtime, human playtesting, balance and whole-game flow remain open. Latest verified GitHub backup is **18c6e3a**; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    text=text.replace(old,current,1)
    text=text.replace('Part4 revision03 remains the current live joint review.','Part 4 is now reviewing the complete corrected EPI-08–14 module.',1)
    text=text.replace('**Current position: 15 October 2026.**','**Current position: 16 October 2026.**',1)
    marker='**Current independent development:**'
    text=text.replace(marker,'**Later campaign arcs:** The [44-source EPI-15–17 packet](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_05_PREPARATION.json) contains 67 authored cases, including the bounded voyage, annual contract, atmosphere and patent-scene proposals. It remains prepared, unsubmitted and unadopted. Earlier detailed progress and links are preserved in the navigation history.\n\n'+marker,1)
    start.write_text(text,encoding='utf-8',newline='\n')
    text=originals[guide].decode();old=next(s for s in text.split('\n\n') if s.startswith('**Current review:**'))
    new='**Current review:** Revision03 was recovered and passed 247 source/citation/identity checks. Its four relics, twelve rooms, eight actors, Null/flora/antidote rules and all75 authored examples received independent semantic review. Actual GPT in Review Continuation Part4 has **agreed with all nine exact local corrections** in [the preserved patch](../../../../../docs/audit/2026-10-08/full-game/DD_Relic_Null_03_Local_Patch_01.zip); 87 patch preservation/replay checks pass. The original84 source records are unchanged, and source85 supplies the existing Expedition roster cap. The [final complete-module verdict is pending](../../../../../docs/audit/2026-10-08/full-game/RELIC_NULL_03_LOCAL_PATCH_01_REVIEW_RECEIPT.json). **No EPI-08–14 rule is applied yet.** Older returns and the full correction history are preserved; source checks and examples are not runtime or balance approval.'
    text=text.replace(old,new,1);guide.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['draftEvidence'].extend(p.relative_to(G).as_posix() for p in [receipt,confirmation,validation,A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_SEMANTIC_REVIEW_01.json'])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'relic-null-patch-review01','recordedAtUtc':now,'revision03Checks':247,'patchChecks':87,'authoredCases':75,'sourceBindings':85,'patchFindingsJointlyConfirmed':9,'completeModuleVerdictPending':True,'newRulesAdopted':False})
    assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in before['aspects'] if x['id']!='DD-50']==[x for x in coverage['aspects'] if x['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='Revision03 recovered:247 source checks; full prose/75-example semantic review complete. Exact local patch jointly approved for all9 RN3 findings;87 preservation/replay checks pass. Complete EPI08–14 combined-module verdict now pending in actual Part4. No rules applied; no runtime/human/whole-game approval.'
    code=originals[nav].decode();tail=' + read(A / "DISEASE_INTERFACE_AUDIT_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "RELIC_NULL_PATCH_REVIEW_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    values=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(values)==1
    code=code.replace(ast.get_source_segment(code,values[0]),repr(scope),1)
    items=[('EPI08–14 — revision03 complete semantic review','COSMOLOGY_EPILOGUE_RELIC_NULL_03_SEMANTIC_REVIEW_01.json'),('EPI08–14 — exact patch and final-review receipt',receipt.name),('EPI08–14 — actual GPT patch confirmation',confirmation.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Exact local correction approved; final combined-module verdict pending; no gameplay rules applied.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['relicNullRevision03']={'archive':rec['revision03Archive'],'sourceCheck':rec['revision03SourceCheck'],'semanticReview':rec['semanticReview'],'patch':rec['archive'],'validation':rec['patchValidation'],'patchApproved':True,'moduleApplied':False}
    state['activeGptReview'].update(reviewId='RELIC-NULL-03-FINAL-MODULE-REVIEW-01',submission=info(receipt),status='Actual browser shows full-module review in progress after exact patch approval.',returnReceived=True,expectedReturn='Text-only full-module verdict; no archive regeneration requested.',generationConfirmedLiveAtObservation=True,newRulesAdopted=False)
    state['safeNextActions']=['Read the SAME Part4 response to RELIC_NULL_03_FINAL_MODULE_REVIEW_REQUEST_01.txt. GPT is assessing the complete candidate, after agreeing RN3-01..09. Do not regenerate or duplicate the request based on native idle status.','If complete-module ACCEPT is explicit, preserve exact response/hash, then apply the already validated candidate as NEW provisional authored reference with separate confirmation metadata. Keep original candidates/returns and owner/human/runtime gates unchanged.','If GPT identifies a real remaining blocker, preserve it and make only the necessary bounded correction for joint review.','Later campaign arcs, consumables, environment and disease audits remain separate unsubmitted proposals; broad spell/feat/bestiary/Director work remains open.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope};state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0}))

if __name__=='__main__':main()
