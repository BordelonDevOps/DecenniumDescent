"""Record received corrections and the exact example-patch conference without adoption."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'AC4_EXACT_CASE_PATCH_03_SUBMISSION_RECEIPT.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC4_EXACT_CASE_PATCH_03_SUBMISSION.json'
    delta=A/'AC4_EXACT_CASE_PATCH_03_NAVIGATION_DELTA.json';keep=A/'navigation-before-ac4-exact-case-patch-03'
    assert not any(p.exists() for p in [receipt,target,delta,keep])
    native=A/'AC4_EXACT_CASE_PATCH_03_NATIVE_DELIVERY.json';d=read(native);turn=d['turns'][0]
    request=A/'AC4_EXACT_CASE_PATCH_03_REQUEST.txt';archive=A/'DD_AC4_Exact_Case_Patch_03.zip';prep=A/'AC4_EXACT_CASE_PATCH_03_PREPARATION.json';dom=A/'AC4_EXACT_CASE_PATCH_03_SUBMITTED_DOM.txt'
    assert turn['items'][0]['content'][0]['text']==request.read_text(encoding='utf8').rstrip()+'\n\n[User attached 1 file; file contents were not included]'
    attachment=Path(next(x['path'] for x in d['attachments'] if x['name']==archive.name));assert attachment.read_bytes()==archive.read_bytes()
    assert 'button "Stop"' in dom.read_text(encoding='utf8')
    assert read(A/'AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json')['failureCount']==0
    rec={'recordedAtUtc':now,'threadTitle':d['thread']['title'],'threadId':d['thread']['id'],'userTurnId':turn['id'],'browserId':'3','tabId':'125746308',
      'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
      'archive':info(archive),'request':info(request),'preparation':info(prep),'nativeDelivery':info(native),'attachmentByteEqualityVerified':True,'liveObservation':info(dom),'proof':info(A/'PART4_AC4_EXACT_CASE_PATCH_03_SUBMITTED.jpg'),
      'generationConfirmedLiveAtObservation':True,'correctedActualReturn':info(A/'DD_AC4_Corrections_02_Return.zip'),'correctedReturnSourceCheck':info(A/'AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json'),
      'independentSemanticReadingComplete':True,'casePatch':info(A/'ac4-exact-case-patch-03/EXACT_PATCH.json'),'changedExamples':['AC4-X01','AC4-X08','AC4-X09'],'unchangedRulePayloads':6,'cards':15,'authoredCases':48,'sourceFiles':70,
      'requestPurpose':'Exact whole-candidate acceptance of three example repairs beside unchanged corrected rules; actual acceptance not yet received.',
      'banishmentAddendum':info(A/'BANISHMENT_CLASS_INTERFACE_ADDENDUM_02.json'),'banishmentStatus':'Unsubmitted/unadopted discussion draft plus17-class lexical navigation,15 independently read class cards and10 additional unresolved review scenarios.',
      'authoredCounts':{'reviewed':419,'pending':429},'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC4_CORRECTIONS_02_SUBMISSION.json'
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);originals[p]=b;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();old=previous.relative_to(G).as_posix();assert text.count(old)==1;text=text.replace(old,target.relative_to(G).as_posix(),1)
    begin=text.index('**Active spell review:**');end=text.index('\n\n',begin)
    text=text[:begin]+'**Active spell review:** GPT returned the corrected15-spell AC4 module with48 authored examples. [248 independent source/prose checks](docs/audit/2026-10-08/full-game/AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json) pass. Codex read the revised rules, profiles, chapters and examples, then [submitted three exact example repairs](docs/audit/2026-10-08/full-game/AC4_EXACT_CASE_PATCH_03_SUBMISSION_RECEIPT.json) for final GPT agreement: actual Acid Arrow reflection, Grand Reservoir base-cost waiver, and correct Medium-rider Load. The corrected model/rules and both chapters remain unchanged. No spell adoption yet:419 reviewed/429 pending. [Banishment remains a separate unadopted draft](docs/audit/2026-10-08/full-game/BANISHMENT_LOCAL_DRAFT_01_PREPARATION.json), now supplemented by [current class-interface evidence and ten additional review scenarios](docs/audit/2026-10-08/full-game/BANISHMENT_CLASS_INTERFACE_ADDENDUM_02.json).'+text[end:]
    start.write_text(text,encoding='utf8',newline='\n')
    cov=json.loads(originals[ledger]);before=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident);oldrow=deepcopy(row)
        row['validationEvidence'].extend([receipt.relative_to(G).as_posix(),rec['correctedReturnSourceCheck']['path'],rec['banishmentAddendum']['path']])
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac4-exact-case-patch03-submission','recordedAtUtc':now,'cards':15,'cases':48,'sourceChecks':248,'failureCount':0,'exampleRepairs':3,'newRulesAdopted':False,'runtimeTestsExecuted':0})
        assert all(row[k]==oldrow[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in before['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    scope='Corrected15-spell AC4 return independently read;248 source/prose checks pass. Three exact example repairs now submitted for actual Part4 whole-candidate agreement beside unchanged rules/chapters.48 authored cases,70 unchanged source files. Banishment remains an unadopted separate draft with expanded class comparisons.419 reviewed/429 pending; no new adoption or runtime/human/balance/whole-game approval.'
    code=originals[nav].decode();tail=' + read(A / "AC4_CORRECTIONS_02_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC4_EXACT_CASE_PATCH_03_NAVIGATION_DELTA.json")["changes"]\n',1)
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    items=[('AC4 — exact three-example final check',receipt.name),('AC4 — corrected return248 source checks','AC4_CORRECTIONS_02_RETURN_SOURCE_CHECK.json'),('Banishment — class-interface addendum','BANISHMENT_CLASS_INTERFACE_ADDENDUM_02.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:]);build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='no progress: visibility/status confirmation; revalidated and advanced this turn',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Completed independent semantic review and submitted exact example-only repair; no adoption yet.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['receivedAc4Corrections02']=state['activeGptReview'];state['receivedAc4Corrections02'].update(returnReceived=True,status='Actual corrected return preserved/source-checked and semantically read; three example repairs submitted separately.',returnArchive=rec['correctedActualReturn'])
    state['activeGptReview']={'reviewId':'AC4-EXACT-CASE-PATCH-03','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':'Actual browser confirmed generating; exact attachment bytes verified. Await bounded exact-candidate acceptance or specific corrections.','generationConfirmedLiveAtObservation':True,'returnReceived':False,'newRulesAdopted':False}
    state['ac4ExactCasePatch03']=rec;state['banishmentClassInterfaceAddendum']=rec['banishmentAddendum']
    state['safeNextActions']=['Poll SAME actual Part4 response to user turn '+turn['id']+'. Browser confirmed live; native idle alone is not terminal.','Verify returned exact candidate approval against all8 payload hashes in ac4-exact-case-patch-03/EXACT_PATCH.json. No rule/model/chapter changes were made, only3 current case adjudications and their output manifest.','Once actual exact agreement exists and any specific corrections are resolved, integrate complete15 procedures/shared/profile/example evidence in authored index with source-preserving receipts; intended counts434/414 only after that actual promotion. Apply scoped AC4-ALIGN-01 consistently to active Suggestion interfaces without rewriting historical sources.','Banishment draft remains unsubmitted/unadopted. Include new17-class source inventory/15 read comparisons and10 unresolved scenarios alongside original26-source draft. Resolve finite return, visitors, new bodies, blockers, tethers, actual No Escape/Reign of Ashes and class-rescue boundaries with GPT.','Full75-area objective remains active. EPI-01–17 already applied; latest verified GitHub backup18c6e3a. Human/runtime/balance/publication gates and final whole-game coherence remain separate and unproven.']
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(receipt),'meaningfulProgress':scope};state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(target),'links':build['existingDistinctLinks'],'missingLinks':0,'attachmentByteEquality':True}))

if __name__=='__main__':main()
