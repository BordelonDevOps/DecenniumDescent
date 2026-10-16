"""Save the accepted Banishment milestone and active full AC5 conference."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, html, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def main():
    now=datetime.now(timezone.utc).isoformat()
    receipt=A/'AC5_CURRENT_REVIEW_02_SUBMISSION_RECEIPT.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_APPLICATION_AC5_SUBMISSION_02.json'
    delta=A/'BANISHMENT_APPLICATION_AC5_SUBMISSION_02_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-banishment-application-ac5-submission-02'
    assert not any(p.exists() for p in [receipt,checkpoint,delta,keep])
    native=A/'AC5_CURRENT_REVIEW_02_NATIVE_DELIVERY.json'
    request=A/'AC5_CURRENT_REVIEW_02_REQUEST.txt'
    delivery=read(native);turn=delivery['turns'][0]
    received=next(c['text'] for i in turn['items'] if i['type']=='userMessage' for c in i['content'] if c['type']=='text')
    original=request.read_text(encoding='utf8').rstrip()
    attachment_notice='\n\n[User attached 1 file; file contents were not included]'
    assert received.rstrip().endswith(attachment_notice)
    message_text=received.rstrip()[:-len(attachment_notice)]
    assert message_text==original
    attachment=next(a for a in delivery['attachments'] if a['name']=='DD_AC5_Current_Review_02.zip')
    archive=A/'DD_AC5_Current_Review_02.zip'
    raw=Path(attachment['path']).read_bytes()
    assert raw==archive.read_bytes()
    live=A/'AC5_CURRENT_REVIEW_02_LIVE_DOM.txt'
    assert 'button "Stop"' in live.read_text(encoding='utf8')
    source_check=A/'AC5_CURRENT_REVIEW_02_SOURCE_CHECK.json'
    packet=read(A/'ac5-current-review-02-input/CURRENT_REVIEW_INPUT.json')
    assert read(source_check)['failureCount']==0
    for b in packet['sourceBindings']:
        assert info(G/b['path'])==b,b['path']
    rec={
        'recordedAtUtc':now,'threadTitle':delivery['thread']['title'],'threadId':delivery['thread']['id'],
        'userTurnId':turn['id'],'browserId':'3','tabId':'125746308',
        'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
        'request':info(request),'nativeDelivery':info(native),
        'deliveryVerification':{'literalMessageTextEquality':message_text==original,'allContentPreserved':True,'normalization':'Removed only the native export attachment notice and trailing newline; message text matches exactly.'},
        'archive':info(archive),'attachmentDelivery':{'name':attachment['name'],'nativeDownloadedBytes':len(raw),'nativeDownloadedSha256':digest(raw),'byteIdenticalToSubmittedArchive':True},
        'submissionObservation':info(A/'AC5_CURRENT_REVIEW_02_SUBMITTED_DOM.txt'),'liveObservation':info(live),
        'proof':info(A/'PART4_AC5_CURRENT_REVIEW_02_SUBMITTED.jpg'),'generationConfirmedLiveAtObservation':True,
        'sourceCheck':info(source_check),'sourceFiles':86,'selectedSpells':16,'printedPlacements':17,'currentComparisons':43,
        'classEnvelopes':17,'independentlyReadClassCards':25,'historicalExamplesPreserved':22,'additionalExamplesRequested':32,
        'currentBanishmentAuthority':info(A/'BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json'),
        'expectedReturn':'DD_AC5_Current_Review_02_Return.zip','newCohortRulesAdopted':False,
        'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False,
    }
    receipt.write_bytes(encoded(rec))
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_REPAIR_04_SUBMISSION.json'
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    saved=[];originals={}
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode()
    assert text.count(previous.relative_to(G).as_posix())==1
    text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    text=text.replace('**Current joint review:** **EPI-01–17','**Reviewed cosmology:** **EPI-01–17',1)
    text=text.replace('434 reviewed / 414 pending','435 reviewed / 413 pending')
    text=text.replace('434 reviewed authored procedures; 414 pending.','435 reviewed authored procedures; 413 pending.')
    text=text.replace('158 procedures use complete standalone representations','159 procedures use complete standalone representations')
    begin=text.index('**Active spell review:**');end=text.index('\n\n',begin)
    text=text[:begin]+'**Active spell review:** **Ordinary Banishment is jointly accepted and applied.** Read the [complete spell chapter](DescentReviewChanges/ReviewBible/docs/spells/candidates/BANISHMENT_REVIEWED_04.md) and [exact acceptance/application receipt](docs/audit/2026-10-08/full-game/BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json). Its 49 frozen sources, 37 current worked cases and 28 historical scenarios are preserved. Local application completed 931 preservation/reference checks with no failures; these are not runtime or human tests. The spell now has finite ending, legal companion/escape examples, and an explicit return-placement procedure. Cleric Banish Unholy stays separate.'+text[end:]
    begin=text.index('**Next spell preparation:**');end=text.index('\n\n',begin)
    text=text[:begin]+'**Current GPT conference:** [The full 16-spell rank-five review is submitted and running in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC5_CURRENT_REVIEW_02_SUBMISSION_RECEIPT.json). Its verified package contains 86 current source files, 43 spell comparisons and all 17 class envelopes. All 16 identities/17 printed placements require full procedures, including the five previously deferred planar spells. The request preserves 22 older case texts and calls for 32 additional worked cases; no new spell from this cohort is accepted yet. [The current full spell reconciliation](docs/audit/2026-10-08/full-game/CURRENT_SPELL_REVIEW_RECONCILIATION_03.json) verifies all 848 identities and 435 reviewed/413 pending memberships with 2,421 reference/preservation checks and no failures.'+text[end:]
    start.write_text(text,encoding='utf8',newline='\n')
    cov=json.loads(originals[ledger]);before=deepcopy(cov)
    evidence=[A/'BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json',A/'BANISHMENT_EXACT_ACCEPTANCE_04_APPLICATION_CHECK.json',A/'CURRENT_SPELL_REVIEW_RECONCILIATION_03.json',receipt,source_check]
    for ident in ['DD-11','DD-12']:
        row=next(r for r in cov['aspects'] if r['id']==ident);prior=deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'banishment-accepted-ac5-submitted','recordedAtUtc':now,'acceptedSpellIds':['banishment'],'authoredCounts':{'reviewed':435,'pending':413},'applicationChecks':931,'applicationFailures':0,'reconciliationChecks':2421,'reconciliationFailures':0,'nextCohortSpells':16,'nextCohortSubmitted':True,'runtimeTestsExecuted':0})
        assert all(row[k]==prior[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [r for r in cov['aspects'] if r['id'] not in ['DD-11','DD-12']]==[r for r in before['aspects'] if r['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    scope='435 reviewed/413 pending ordinary spells. Ordinary Banishment jointly accepted/applied:49sources,37cases,28historical scenarios,931application checks; full848-ID reconciliation2421checks,0failures. Full16-spell AC5 conference submitted/live in actual Part4 with86sources,43comparisons,17class envelopes. No runtime/human/balance/whole-game/publication approval.'
    code=originals[nav].decode()
    tail=' + read(A / "BANISHMENT_REPAIR_04_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "BANISHMENT_EXACT_ACCEPTANCE_04_OPERATIONS.json")["changes"] + read(A / "BANISHMENT_APPLICATION_AC5_SUBMISSION_02_NAVIGATION_DELTA.json")["changes"]\n',1)
    values=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(values)==1;code=code.replace(ast.get_source_segment(code,values[0]),repr(scope),1)
    code=code.replace('    featured = [\n','    featured = [\n'+repr(('Banishment — jointly reviewed complete spell','DescentReviewChanges/ReviewBible/docs/spells/candidates/BANISHMENT_REVIEWED_04.md'))+',\n',1)
    items=[('AC5 — active full16-spell conference',receipt.name),('Banishment — exact accepted application','BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json'),('Spells — current435reviewed/413pending reference audit','CURRENT_SPELL_REVIEW_RECONCILIATION_03.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    for old,new in [('Banishment — active Repair04 conference','Banishment — historical Repair04 conference, now accepted'),('Banishment — active Repair03 conference','Banishment — historical Repair03 conference'),('AC5 — current16-spell source/interface audit, unsent','AC5 — earlier16-spell preparation, superseded by submission'),('AC5 —25 independently read class interfaces, unsent','AC5 —25 class interfaces included in current submission')]:
        code=code.replace(old,new)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newSpellAdoptions':1,'fullDomainClosureChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=1,newRuleAdoptionScope='One ordinary spell package, Banishment, accepted/applied; full16-spell AC5conference live but unadopted.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['ordinaryAuthoredCountsCurrent']={'reviewed':435,'pending':413}
    state['currentOrdinarySpellCounts']={'reviewed':435,'pending':413,'total':848}
    state['currentAuthoredIndex']=info(R/'data/public/spell_playtests/authored_review_index.json')
    state['currentSpellReferenceReconciliation']=info(A/'CURRENT_SPELL_REVIEW_RECONCILIATION_03.json')
    state['completedBanishmentReview']={'authority':info(A/'banishment-exact-acceptance-04/ACCEPTANCE.json'),'receipt':info(A/'BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json'),'applicationCheck':info(A/'BANISHMENT_EXACT_ACCEPTANCE_04_APPLICATION_CHECK.json'),'authoredCases':37,'sourceFiles':49,'newRulesAdopted':True,'runtimeSelectionEnabled':False}
    state['activeGptReview']={'reviewId':'AC5-CURRENT-REVIEW-02','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':rec['userTurnId'],'status':'Actual browser confirmed generating and inspecting the attached86-source package; native text and attachment bytes verified.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['ac5CurrentPreparation']={'archive':info(archive),'sourceCheck':info(source_check),'submission':info(receipt),'status':'Submitted/live; all16identities/17placements full authoring; accepted ordinary Banishment included.','sourceFiles':86,'currentComparisons':43,'selectedClassCardsRead':25,'additionalAuthoredExamplesRequired':32}
    state['safeNextActions']=[
        'Read SAME Part4 response to user turn '+rec['userTurnId']+'. No resubmission/restart on observation timeout; browser live status is authoritative.',
        'Download/preserve DD_AC5_Current_Review_02_Return.zip, expected8rootfiles. Verify all86frozen sources,16complete source/access cards,17placements,22unchanged historical texts and all32required additional examples (minimum54current cases).',
        'Review all16procedures and exact12current/10class issue dispositions independently; five formerly deferred planar spells require full effects, not source-only receipts or narrower substitutes. Preserve owner locks and distinguish uncertain provenance from false facts.',
        'Check Nexus/Dampening final-price stages, protected conversion principal, NullDisabled summon lifecycle/healing scope, real damage roots, source-dependent antimagic/dispel, faction credentials/standing and current alignment overlays. Only scoped explicit additions can extend existing authority.',
        'Ordinary Banishment is already accepted/applied,435reviewed/413pending. Do not rerun its one-shot application or reopen AC4. Exact accepted models and all previous source history are preserved.',
        'Full75-area goal remains intact. The latest verified GitHub backup18c6e3a precedes this local work. Environment/disease/consumables/feats/bestiary/Director/packaging and final actual joint flow remain open; no runtime/human/balance/publication claim.',
    ]
    state['resumedBlockedAudit']={'classification':'progress','evidence':info(A/'BANISHMENT_EXACT_ACCEPTANCE_04_APPLICATION_CHECK.json'),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'submission':info(receipt),'checkpoint':info(checkpoint),'links':build['existingDistinctLinks'],'missingLinks':0,'ordinarySpells':state['currentOrdinarySpellCounts']}))


if __name__=='__main__':
    main()
