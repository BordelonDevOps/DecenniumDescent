"""Register finite Nature fulfillment and received/reproduced DI7 source verdict."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json,hashlib,shutil,subprocess,sys
from validate_feat_exact_01_composite_casting import read,info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';V=A/'di7-joint-review-01-verdict'


def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_NATURE_TRANSACTIONS.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_NATURE_FULFILLMENT_AND_DI7_VERDICT.json'
    delta=A/'NATURE_FULFILLMENT_DI7_VERDICT_PROGRESS_DELTA.json';preservation=A/'navigation-before-nature-fulfillment-di7-verdict'
    receipt=A/'DI7_JOINT_REVIEW_01_RECEIVED.json';reproduced=A/'DI7_JOINT_REVIEW_01_REPRODUCED.json'
    qualification=A/'FEAT335_NATURE_FINITE_FULFILLMENT_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,receipt,reproduced,qualification])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    nature_path=A/'FEAT335_NATURE_FINITE_FULFILLMENT.json';nature=read(nature_path);cast_path=A/'FEAT335_NATURE_SPELL_INTEGRATION_CHECK.json';casts=read(cast_path)
    assert nature['checks']==208 and len(nature['histories'])==3 and len(nature['expectationMatrix'])==47 and nature['natureAll47VariantsFulfilledInFiniteScope']
    assert casts['checks']==77 and len(casts['histories'])==28
    for report in [nature,casts]:
        assert report['status']=='pass' and not report['failures']
        for b in report['sourceBindings']:assert info(G/b['path'])==b
    save(qualification,{'report':info(nature_path),'castIntegrationReport':info(cast_path),'scope':nature['scope'],'disposition':nature['disposition'],
        'counts':nature['counts'],'remainingLimits':nature['limits'],'natureAll47VariantsFulfilledInFiniteScope':True,
        'fullFeatExactApproved':False,'runtimeApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False})
    archive=A/'DI7_Joint_Review_01_Addendum_and_Evidence.zip';bound=info(archive)
    assert bound['bytes']==1934397 and bound['sha256']=='e508bc89f5b05fddff0aa9e4f3f3e3482b85bb3eece1c2ffe43938206f33e7ff'
    manifest=read(V/'FILE_MANIFEST.json');assert len(manifest['files'])==manifest['payloadCount']==26
    verified=[]
    for name,b in manifest['files'].items():
        current=info(V/name);assert current['bytes']==b['bytes'] and current['sha256']==b['sha256'];verified.append(current)
    comparisons=[]
    for local,original,count in [('DI7_JOINT_REVIEW_01_LOCAL_REFERENCE_RESULTS.json','reviewer_check_results.json',484),('DI7_JOINT_REVIEW_01_LOCAL_DELIVERABLE_RESULTS.json','deliverable_check_results.json',150)]:
        lp=A/local;op=V/original;x=lp.read_bytes();y=op.read_bytes();d=read(lp)
        assert read(lp)==read(op) and d['checks']==d['passed']==count and d['failed']==0
        assert x.replace(b'\r\n',b'\n')==y.replace(b'\r\n',b'\n')
        comparisons.append({'local':info(lp),'reviewer':info(op),'checks':count,'JSONEqual':True,'rawBytesEqual':x==y,'equalAfterOnlyCRLFToLF':True})
    save(reproduced,{'recordedAtUtc':now,'reviewId':'DI7-JOINT-REVIEW-01','status':'pass','checks':634,'comparisons':comparisons,
        'categories':read(A/'DI7_JOINT_REVIEW_01_LOCAL_REFERENCE_RESULTS.json')['categories'],
        'scope':'484 source/static and bounded reference/rejection checks plus150 excerpt/descendant/manuscript/anchor checks reproduce exactly as JSON; raw Windows CRLF differs from frozen LF only. No full spell runtime or exact-card approval.',
        'scriptsInspectedBeforeExecution':True,'submittedSourceChanged':False,'reviewerDiagnosticPreserved':True})
    dom=A/'DI7_JOINT_REVIEW_01_RECEIVED_DOM.txt';shot=A/'DI7_JOINT_REVIEW_01_RECEIVED.png';text=dom.read_text(encoding='utf-8')
    assert 'DI7-JOINT-REVIEW-01 — final source-authoring verdict' in text and 'e508bc89f5b05fddff0aa9e4f3f3e3482b85bb3eece1c2ffe43938206f33e7ff' in text and shot.exists()
    save(receipt,{'recordedAtUtc':now,'reviewId':'DI7-JOINT-REVIEW-01','status':'terminal-source-authoring-verdict-received-and-reproduced',
        'submission':info(A/'DI7_JOINT_REVIEW_01_SUBMISSION.json'),'archive':bound,'manifest':info(V/'FILE_MANIFEST.json'),'verifiedPayloads':verified,
        'payloadCount':26,'currentBrowserId':'3','currentTabId':'125745946','conversationUrl':state['activeGptReview']['conversationUrl'],
        'recovery':'Fresh tab opened the exact same conversation after old tab CDP timeouts. No review request was resent. Initial load temporarily exposed disabled file controls; hydrated DOM provided the archive download.',
        'downloadEventTimedOutButExactLocalArchiveVerified':True,'responseDom':info(dom),'screenshot':info(shot),'reproduction':info(reproduced),
        'sourceIssuesResolved':list(range(1,14)),'excludedReceiptIssue':'DI7-X14','mechanicalSpells':7,'originalExamples':14,
        'guardedDirectionOperations':18,'existingCounterpartException':'AP-AS-01','APASRepresentations':2,
        'followthroughGroups':16,'authoredVariants':49,'sourceConferenceComplete':True,'exactCardsApproved':False,
        'sourceOperationsAppliedLocally':False,'pendingResponse':False,'replyReceived':True,'selectionEnabled':False,'sourceInformationDeleted':0,'cosmologyReviewed':False})
    scope=('Nature NWQ01–04 finite follow-through is fulfilled under the actual GPT contract: all16 groups/47 variants map to preserved source evidence and explicitly conditional histories. '
        'The earlier185 checks/75 histories are supplemented by77 paid ordinary-cast/Fate Coin checks across28 histories and208 acceptance/source-binding checks with3 additional histories, including genuinely paid replacing Expertise and existing Bard rhythm. '
        'This is named Nature interface fulfillment only, not full335, full spell runtime or balance approval. '
        'Actual GPT DI7-JOINT-REVIEW-01 is terminal and received through a fresh tab of the same conversation, without resending. Its1934397-byte archive and26 payloads verify;484 source/reference checks plus150 deliverable checks reproduce. '
        'All7 Divination source directions and13 mechanical issues are resolved for authorship.18 guarded corrections,2 AP-AS-01 counterpart representations,16 groups/49 variants and a complete exact-candidate review remain to implement; no spell count/status is promoted. '
        'Ordinary spells remain412 reviewed/436 pending;187 higher proposals remain unadopted. Latest weekly usage35percent used; stop at50 remains controlling. '
        'Final whole-game agreement precedes authorized GitHub push, verified remote and careful cosmology. No source deletion or push occurred.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py';assert info(ledger_path)==state['coverageLedger']
    old=read(ledger_path);ledger=deepcopy(old)
    evidence=[nature_path,cast_path,qualification,receipt,reproduced,V/'DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json']
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope);row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'Nature-finite-fulfillment-and-DI7-source-verdict','recordedAtUtc':now,
                'natureFiniteVariants':47,'DI7SourceConferenceReceived':True,'DI7ExactCardsApproved':False,'fullUseRuntimeApproved':False})
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-09','DD-12','DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    nav_text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_NATURE_TRANSACTIONS_PROGRESS_DELTA.json")["changes"]\n';assert nav_text.count(chain)==1
    nav_text=nav_text.replace(chain,chain.rstrip('\n')+' + read(A / "NATURE_FULFILLMENT_DI7_VERDICT_PROGRESS_DELTA.json")["changes"]\n')
    assert nav_text.count(state['status'])==1;nav_text=nav_text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert nav_text.count(marker)==1
    items=[('Nature finite47-variant fulfillment and exact evidence matrix',nature_path),('Nature ordinary cast and actual Fate Coin integration —77 checks',cast_path),
        ('Nature finite fulfillment —scope and wider limits',qualification),('DI7 source-authoring verdict —received26 payloads',receipt),('DI7 checks —484 plus150 reproduced',reproduced),
        ('DI7 complete source directions',V/'DI7_COMPLETE_OPERATING_DIRECTIONS.md'),('DI7 later exact-review requirements',V/'DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json'),('DI7 received verdict —visible proof',shot)]
    nav_text=nav_text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in items))
    replacements={'Nature scope \\u2014two acceptance integrations remain':'Nature earlier scope \\u2014two gaps subsequently closed in finite fulfillment',
        'DI7 browser observation \\u2014reply completion currently unverified':'DI7 historical browser timeout \\u2014subsequently recovered',
        'Nature16 authored expectation groups \\u2014see current partial behavior evidence':'Nature16 authored expectation groups \\u2014see later47-variant fulfillment',
        'DI7 actual joint review \\u2014sent once; response pending':'DI7 original dispatch \\u2014sent once; see received verdict'}
    for before,after in replacements.items():assert nav_text.count(before)==1;nav_text=nav_text.replace(before,after)
    compile(nav_text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preservation/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);assert dest.read_bytes()==p.read_bytes()
        preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(nav_text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosureAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newRuleAdoptions':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,coverageLedger=info(ledger_path),coverageDelta=info(delta),
        natureFiniteFulfillment={'receipt':info(nature_path),'castIntegration':info(cast_path),'scope':info(qualification),'groups':16,'variants':47,'finiteBehaviorFulfilled':True,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint records source directions received and Nature finite fulfillment. DI7 guarded operations are not yet applied.')
    state['natureSourceApplication'].update(finiteBehaviorFulfilled=True,finiteFulfillment=info(nature_path))
    state['natureTransactions'].update(laterFulfillment=info(nature_path),earlierTwoOpenDetailsResolvedBy=info(cast_path))
    state.setdefault('priorCompletedGptObservations',[]).append(deepcopy(state['activeGptReview']))
    state['activeGptReview'].update(status='terminal-source-authoring-verdict-received-reproduced',tabId='125745946',currentObservation=info(receipt),
        pendingResponse=False,replyReceived=True,currentCompletionKnown=True,lastObservedStopVisible=False,
        instruction='DI7 source response is received. Do not resend. Apply18 guarded new-descendant corrections, propagate AP-AS-01 through every actual active counterpart reader with original bytes preserved, fulfill16 groups/49 variants and assemble seven complete public/internal candidates for separate exact review.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_NATURE_FULFILLMENT_AND_DI7_VERDICT. Fresh usage35percent used during this turn. At50 or above save and pause under owner instruction.',
        'Nature NWQ01–04 is finite-fulfilled:185/75 original transactions,77/28 ordinary-cast/reroll integration,208 acceptance/source checks and3 additional histories produce the full47-row trace. Preserve all earlier evidence and use the later scope receipt; do not reopen the unchanged Nature conference.',
        'Actual GPT DI7 source response is terminal. Archive1934397 SHAe508bc89f5b05fddff0aa9e4f3f3e3482b85bb3eece1c2ffe43938206f33e7ff and all26 payloads verified.484+150 reviewer checks reproduce (JSON and newline-normalized bytes equal). See di7-joint-review-01-verdict.',
        'Read complete DI7 directions/18 guarded operations/AP-AS-01 amendment. Author seven final complete internal/public candidates preserving the original proposal and bound input; AP-AS-01 must be implemented in every active counterpart reader, with preserved history and measured current bindings. No promotion before separate exact review.',
        'Execute the finite DI7 16 groups/49 variants with source-qualified conditional actors, Ready/cost/counter/history/recipient/audience interfaces and explicit limits. Then send the seven actual exact candidates plus complete envelopes to the same Calibration Review Part2. User authorization for GPT collaboration persists.',
        'Chrome3 live recovered tab125745946 is the same conversation. Old125745943 timed out; fresh-tab navigation recovered its terminal reply without resending. Re-mark the live tab for continuation.',
        'Continue copy paid release and other remaining full-feat procedures. Higher proposals187 unadopted,71 comparison-only,109 unsent,7 source-reviewed DI7 pending assembly/exact review;201 remaining mechanical proposals,47 deferred. Ordinary412/436 unchanged.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'));save(checkpoint,state)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'natureVariants':47,'DI7ReproducedChecks':634}))


if __name__=='__main__':main()
