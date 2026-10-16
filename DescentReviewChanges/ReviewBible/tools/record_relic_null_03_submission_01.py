"""Record actual Part4 revision03 submission and preserve navigation predecessors."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_SUBMISSION_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_03_SUBMISSION_01.json'
    delta=A/'RELIC_NULL_03_SUBMISSION_01_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-relic-null-03-submission-01'
    checker=R/'tools/check_cosmology_epilogue_relic_null_return_03.py'
    assert all(not p.exists() for p in [receipt,target,delta,keep,checker])
    native=A/'RELIC_NULL_03_NATIVE_DELIVERY_01.json';payload=read(native)['nativeRead']
    request=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_REVISION_REQUEST_01.txt'
    attached=Path(next(v['path'] for v in payload['attachments'] if v['name']=='Pasted text(20261016-052055).txt'))
    assert attached.read_bytes()==request.read_bytes()
    turn=payload['turns'][0];assert turn['id']=='2a6ef2b3-519e-479f-b120-7bfbf39c9d44'
    proof=A/'PART4_RELIC_NULL_03_SUBMISSION_PROOF_01.jpg';assert proof.is_file()
    review=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_02_FOLLOWUP_REVIEW_01.json'
    resolution=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_02_SOURCE_FORMAT_RESOLUTION_01.json'
    rec={'recordedAtUtc':now,'destinationTitle':'Review Continuation Part 4','threadId':payload['thread']['id'],
      'browserId':'3','tabId':'125746308','userTurnId':turn['id'],
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
      'request':info(request),'actualPastedAttachmentName':attached.name,'attachedBytesMatchSavedRequest':True,
      'nativeDelivery':info(native),'proofScreenshot':info(proof),'submitted':True,
      'reviewedArchive':info(A/'DD_Cosmology_Epilogue_Relic_Null_02_Return_02.zip'),
      'earlierRevision02Archive':info(A/'DD_Cosmology_Epilogue_Relic_Null_02_Return_01.zip'),
      'sourceFormatResolution':info(resolution),'independentSemanticReview':info(review),'remainingFindingGroups':9,
      'browserGenerationEvidence':{'heading':'Inspecting and Listing Archive Files','stopVisible':True,
        'assistantProgressExcerpt':'The revision02 archive on disk matches Codex’s reviewed build exactly: 102,637 bytes and SHA-256 de3a15bee044b7e631cf46a572a104589f928913c5b618c246369a50d7925905. I’m using RN2-01–09 as review findings, not rulings, and will only add scoped NEW mechanics where the existing 84-source record cannot execute the branch cleanly.'},
      'expectedReturn':'DD_Cosmology_Epilogue_Relic_Null_03_Return.zip','returnReceived':False,
      'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanBalanceApproved':False,'wholeGameFlowConfirmed':False}
    receipt.write_bytes(encoded(rec))
    code=(R/'tools/check_cosmology_epilogue_relic_null_return_02.py').read_text(encoding='utf-8')
    code=code.replace('Relic_Null_02_Return','Relic_Null_03_Return').replace('relic-null-02-return','relic-null-03-return').replace('RELIC_NULL_02_RETURN_SOURCE_CHECK','RELIC_NULL_03_RETURN_SOURCE_CHECK')
    old="e==expected[name] and len(actual)==e['bytes'] and sha(actual)==e['sha256']"
    new="(e==expected[name] if name != 'DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md' else all(e.get(k)==v for k,v in expected[name].items()) and set(e)-set(expected[name]) <= {'bindingStatus'}) and len(actual)==e['bytes'] and sha(actual)==e['sha256']"
    assert code.count(old)==1;code=code.replace(old,new)
    code=code.replace("A/'cosmology-epilogue-relic-null-01-return/CASEBOOK.json'","A/'cosmology-epilogue-relic-null-02-return-02/CASEBOOK.json'")
    compile(code,str(checker),'exec');checker.write_text(code,encoding='utf-8',newline='\n')
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    operations={start:[],guide:[]}
    def replace(p,old,new):
        text=p.read_text(encoding='utf-8');assert text.count(old)==1,(str(p),old)
        p.write_text(text.replace(old,new,1),encoding='utf-8',newline='\n');operations[p].append({'old':old,'replacement':new})
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PART4_HANDOFF_01.json'
    replace(start,previous.relative_to(G).as_posix(),target.relative_to(G).as_posix())
    replace(start,'GPT has verified the uploaded handoff and all 84 source bindings and is working on the correction request.',
      'Both revision02 returns are now preserved. All 84 source identities and bytes match; [one strict metadata-format flag is resolved](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_SOURCE_FORMAT_RESOLUTION_01.json). The latest 75-case revision still has [nine semantic finding groups](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_FOLLOWUP_REVIEW_01.json). The [revision03 follow-up is submitted](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_03_SUBMISSION_01.json), and GPT has acknowledged the exact latest archive and begun corrections.')
    old=next(x for x in guide.read_text(encoding='utf-8').split('\n\n') if x.startswith('**Current review:**'))
    replace(guide,old,'**Current review:** Review Continuation Part 4 has returned two preserved revision02 archives. The latest is [102,637 bytes](../../../../../docs/audit/2026-10-08/full-game/DD_Cosmology_Epilogue_Relic_Null_02_Return_02.zip) with 75 authored cases. All84 supplied source identities/bytes match; the [single strict dictionary-check flag](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_SOURCE_FORMAT_RESOLUTION_01.json) is an added explanatory bindingStatus label, not source drift. Its original receipt remains unchanged. The [independent follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_FOLLOWUP_REVIEW_01.json) records nine remaining semantic issue groups. The [revision03 request is submitted and acknowledged](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_03_SUBMISSION_01.json); continue from that same live Part4 response. **No EPI-08–14 rule is adopted.** Original and both revision02 returns are retained, and older applied conferences are not being restarted.')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage)
    row=next(x for x in coverage['aspects'] if x['id']=='DD-50');oldrow=deepcopy(row)
    row['draftEvidence'].extend(p.relative_to(G).as_posix() for p in [resolution,review,receipt])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'part4-relic-null-revision03-submission01','recordedAtUtc':now,
      'sourceBindingsVerified':84,'revision02ReturnsPreserved':2,'existingCaseIds':75,'remainingSemanticFindingGroups':9,
      'revision03Submitted':True,'revision03ReturnReceived':False,'newRulesAdopted':False})
    for key in ['status','closure','humanEvidence','completionClass']:assert row[key]==oldrow[key]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope='Actual Part4 revision03 follow-up submitted and acknowledged. Two revision02 archives preserved; latest102637 bytes/75 cases/84 verified source bindings. Strict lifecycle-record mismatch is extra bindingStatus metadata only. Nine semantic finding groups still block adoption. GPT verified the exact latest archive and is generating corrections. No new rules, runtime or whole-game gates adopted.'
    code=originals[nav].decode();tail=' + read(A / "PART4_HANDOFF_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "RELIC_NULL_03_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('EPI08–14 — verified latest revision02 archive','DD_Cosmology_Epilogue_Relic_Null_02_Return_02.zip'),('EPI08–14 — metadata flag resolution',resolution.name),('EPI08–14 — remaining semantic findings',review.name),('Part4 — revision03 actual submission',receipt.name)]
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
      newRuleAdoptionScope='Two actual revision02 returns recovered and source verified; revision03 semantic correction conference submitted. No revised rule applied.',
      navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['previousActiveGptReviewBeforeRevision03']=state['activeGptReview']
    state['activeGptReview']={'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-RELIC-NULL-03','threadId':rec['threadId'],
      'title':rec['destinationTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],
      'submission':info(receipt),'status':'Browser generation verified; exact revision02 acknowledged; RN2-01–09 correction work underway.',
      'generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False,'readinessCheck':info(checker)}
    state['relicNullRevision02']={'latestArchive':rec['reviewedArchive'],'earlierArchive':rec['earlierRevision02Archive'],'sourceVerification':info(resolution),'semanticReview':info(review),'adopted':False}
    state['safeNextActions']=['Recheck the SAME Part4 response to actual user turn2a6ef2b3-519e-479f-b120-7bfbf39c9d44. GPT verified latest revision02 and is correcting RN2-01–09. Do not duplicate requests based on native idle delivery metadata.',
      'Download exact revision03 archive after completion. Download watcher may time out even on success; inspect exact Downloads file/hash before clicking again. Use checker03 once with an unused suffix; it preserves all75 existing case IDs and verifies84 sources while tolerating only source84 bindingStatus metadata.',
      'Independently review all nine follow-up groups plus regressions and full chapter parity before adoption. Keep older returns/receipts unchanged; runtime/human/whole-game approval remains open.',
      'Keep later arcs, consumable and environment drafts separate and unadopted until their own joint reviews.']
    state['resumedBlockedAudit']={'classification':'progress','previousConnectionBlockerResolved':True,'evidence':info(receipt),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'submission':info(receipt),'checkpoint':info(target),'checker':info(checker),'links':build['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
