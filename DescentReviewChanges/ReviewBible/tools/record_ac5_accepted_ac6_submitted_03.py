"""Record joint AC5 integration and the actual complete AC6 conference, preserving navigation."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast,json,subprocess,sys,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_LOCAL_FINAL_05.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_ACCEPTED_AC6_SUBMITTED_03.json'
    receipt=A/'AC6_FULL_CURRENT_REVIEW_03_SUBMISSION_RECEIPT.json';delta=A/'AC5_ACCEPTED_AC6_SUBMITTED_03_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-ac5-accepted-ac6-submitted-03'
    assert not any(p.exists() for p in [checkpoint,receipt,delta,keep])
    native=A/'AC6_FULL_CURRENT_REVIEW_03_SUBMITTED_NATIVE.json';obs=read(native);turn=obs['turns'][0]
    assert turn['id']=='b800a2fe-388e-4810-b036-b1f2685d77bb'
    item=next(x for x in turn['items'] if x['type']=='userMessage')
    actual=''.join(x['text'] for x in item['content'] if x['type']=='text');suffix='\n\n[User attached 1 file; file contents were not included]'
    if actual.endswith(suffix):actual=actual[:-len(suffix)]
    request=A/'AC6_FULL_CURRENT_REVIEW_03_REQUEST.txt';archive=A/'DD_AC6_Full_Current_Review_03.zip'
    request_text=request.read_text(encoding='utf8')
    assert actual==request_text or actual==request_text.removesuffix('\n')
    attachment=next(x for x in obs['attachments'] if x['name']==archive.name);assert Path(attachment['path']).read_bytes()==archive.read_bytes()
    source_manifest=A/'ac6-full-current-review-03-input/SOURCE_MANIFEST.json';bindings=read(source_manifest)['bindings'];assert len(bindings)==103
    with zipfile.ZipFile(archive) as z:
        assert json.loads(z.read('SOURCE_MANIFEST.json'))['bindings']==bindings
        for b in bindings:assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes() and info(G/b['path'])==b
    browser=A/'AC6_FULL_CURRENT_REVIEW_03_SUBMITTED_BROWSER.txt';screenshot=A/'PART4_AC6_FULL_REVIEW_03_SUBMITTED.png'
    assert 'button "Stop"' in browser.read_text(encoding='utf8') and screenshot.stat().st_size>10000
    rec={'id':'AC6-FULL-CURRENT-REVIEW-03-SUBMISSION','recordedAtUtc':now,'status':'Submitted once to actual GPT Part4; exact request and attachment confirmed. GPT visibly began verification of all103 sources and full14-identity review.','threadId':obs['thread']['id'],'title':obs['thread']['title'],'userTurnId':turn['id'],'browserId':'3','tabId':'125746324','archive':info(archive),'request':info(request),'nativeObservation':info(native),'browserObservation':info(browser),'screenshot':info(screenshot),'uploadedAttachmentBytesMatch':True,'exactRequestMatches':True,'sourceBindingsVerified':103,'spellIdentities':14,'placements':16,'currentExamples':51,'historicalTexts':22,'requiredExamples':32,'currentQuestions':10,'preparation':info(A/'AC6_FULL_CURRENT_REVIEW_03_PREPARATION.json'),'acceptedAC5':info(A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'),'expectedReturn':'DD_AC6_Full_Review_03_Return.zip','newAc6Adoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    rec['exactRequestMatches']=actual==request_text
    rec['requestMatchesAfterTerminalNewlineNormalization']=True
    rec['requestTextNormalization']='Native message omits the one terminal newline; every other character matches the saved request.' if actual!=request_text else 'None'
    receipt.write_bytes(encoded(rec))
    start=G/'START_HERE.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';originals={};saved=[]
    for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);originals[p]=raw;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();assert text.count(previous.relative_to(G).as_posix())==1;text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    text=text.replace('435 reviewed / 413 pending','451 reviewed / 397 pending').replace('435 reviewed authored procedures; 413 pending','451 reviewed authored procedures; 397 pending').replace('159 procedures use complete standalone representations','175 procedures use complete standalone representations')
    paragraphs={
      '**Active spell review:**':'**Active spell review:** **All 16 AC5 spells are jointly accepted and integrated.** Read their [complete player chapter](DescentReviewChanges/ReviewBible/docs/spells/candidates/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md), [Director chapter](DescentReviewChanges/ReviewBible/docs/director-only/spells/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md), and [exact acceptance/application receipt](docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json). The exact source/access records, 17 placements, 61 current cases, 22 historical example texts and 92 frozen sources remain preserved. [Application review](docs/audit/2026-10-08/full-game/AC5_EXACT_ACCEPTANCE_05_APPLICATION_CHECK.json) passed 1,183 checks. Ordinary spells now total **451 reviewed / 397 pending**. [Ordinary Banishment remains accepted](docs/audit/2026-10-08/full-game/BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json). These are authored procedures; runtime and human balance remain unproven.',
      '**Current GPT conference:**':'**Current GPT conference:** The [complete AC6 conference packet](docs/audit/2026-10-08/full-game/DD_AC6_Full_Current_Review_03.zip) is [submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC6_FULL_CURRENT_REVIEW_03_SUBMISSION_RECEIPT.json). It carries all 14 identities, 16 printed placements, 51 current examples, 22 historical originals, 32 original example requirements and 103 complete frozen source files, refreshed against accepted AC5. Ten current questions explicitly address remaining source, timing, summon, portal and Forge choices. No AC6 spell is adopted yet.',
      '**Next spell group, prepared for review:**':'**Current rank-six review contents:** The [complete current input](docs/audit/2026-10-08/full-game/ac6-full-current-review-03-input/CURRENT_REVIEW_INPUT.json) retains all prior procedure drafts and adds source-qualified Xi Pendant removal of one Watch branch, an accepted-antimagic failed-dispel example, and actual readied Bittersap administration between Skybrand attacks. [Preparation review](docs/audit/2026-10-08/full-game/AC6_FULL_CURRENT_REVIEW_03_PREPARATION.json) passed 270 preservation and packaging checks. Real random-selection examples, source-ending events, summon suppression identity, Nexus classification and plane-wide scope remain explicit joint decisions. All old drafts, questions and partial examples are retained as history.'
    }
    for marker,paragraph in paragraphs.items():
        begin=text.index(marker);end=text.index('\n\n',begin);text=text[:begin]+paragraph+text[end:]
    start.write_text(text,encoding='utf8',newline='\n')
    evidence=[A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json',A/'AC5_EXACT_ACCEPTANCE_05_APPLICATION_CHECK.json',receipt,A/'AC6_FULL_CURRENT_REVIEW_03_PREPARATION.json']
    cov=json.loads(originals[ledger]);oldcov=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row);row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac5-accepted-ac6-submitted-03','recordedAtUtc':now,'status':'Sixteen AC5 authored procedures jointly accepted and integrated; full14-identity AC6 review submitted. Full domain closure unchanged.','newReviewedOrdinarySpells':16,'currentOrdinaryReviewed':451,'currentOrdinaryPending':397,'ac5ApplicationChecks':1183,'ac6SubmittedSources':103,'ac6Identities':14,'ac6CurrentExamples':51,'runtimeTestsExecuted':0})
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in oldcov['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    code=originals[builder].decode();tail=' + read(A / "AC5_LOCAL_FINAL_05_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC5_EXACT_ACCEPTANCE_05_OPERATIONS.json")["changes"] + read(A / "AC5_ACCEPTED_AC6_SUBMITTED_03_NAVIGATION_DELTA.json")["changes"]\n',1)
    additions=[('AC5 — sixteen spells jointly accepted and integrated','AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'),('AC5 — exact preservation and application checks','AC5_EXACT_ACCEPTANCE_05_APPLICATION_CHECK.json'),('AC6 — full fourteen-spell actual GPT submission',receipt.name),('AC6 — refreshed sources and actual worked examples','AC6_FULL_CURRENT_REVIEW_03_PREPARATION.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in additions),1)
    code=code.replace('    featured = [\n','    featured = [\n        ("AC5 — jointly accepted complete player chapter", "DescentReviewChanges/ReviewBible/docs/spells/candidates/ABJURATION_CONJURATION_RANK5_REVIEWED_05.md"),\n',1)
    scope='451 reviewed /397 pending ordinary spells. All16 AC5 procedures are jointly accepted and integrated with1183 passing preservation/application checks;61 cases22 historical texts92 sources retained. Full14-identity AC6 conference submitted to actual GPT Part4 with16 placements51 current examples22 original texts103 frozen sources. AC6 remains unadopted. Full75-area authored objective, runtime, human balance and final whole-game flow remain open.'
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':16,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);prior=deepcopy(state['activeGptReview']);prior.update(status='Exact candidate05 accepted by actual GPT; all16 spells now integrated.',returnReceived=True,accepted=True,acceptance=info(A/'ac5-exact-acceptance-05/ACCEPTANCE.json'),application=info(A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'),applicationCheck=info(A/'AC5_EXACT_ACCEPTANCE_05_APPLICATION_CHECK.json'))
    state.setdefault('priorCompletedGptReviews',[]).append(prior)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=16,newRuleAdoptionScope='Sixteen exact jointly accepted AC5 authored procedures only; source catalog unchanged; no AC6 adoption.',currentOrdinarySpellCounts={'reviewed':451,'pending':397,'total':848},ordinaryAuthoredCountsCurrent={'reviewed':451,'pending':397},currentAuthoredIndex=info(R/'data/public/spell_playtests/authored_review_index.json'),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview']={'reviewId':'AC6-FULL-CURRENT-REVIEW-03','threadId':rec['threadId'],'title':rec['title'],'browserId':'3','tabId':'125746324','conversationUrl':prior['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':rec['status'],'generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(browser),'observationTimeoutMeansTerminal':False}
    state['completedAc5Review']=prior
    state['ac6CurrentReview03']={'preparation':info(A/'AC6_FULL_CURRENT_REVIEW_03_PREPARATION.json'),'submission':info(receipt),'currentInput':info(A/'ac6-full-current-review-03-input/CURRENT_REVIEW_INPUT.json'),'sourceManifest':info(source_manifest),'identities':14,'placements':16,'currentExamples':51,'historicalTexts':22,'sourceCount':103,'status':'Actual joint review in progress; no AC6 adoption.'}
    state['safeNextActions']=['Continue SAME Part4 AC6 user turn b800a2fe-388e-4810-b036-b1f2685d77bb; browser confirmed active. Do not resend or restart due observation timeouts. Current tab125746324.','When DD_AC6_Full_Review_03_Return.zip arrives, preserve exact bytes and independently check all103 sources,14 identities16 placements,full14 procedures and both Nexus modes,51 retained current caseIDs22 original texts plus new cases, all current issue dispositions and every JSON pointer.','Review remaining semantic decisions, especially real Xi component removal, antimagic/Seal operations, actual random candidate geometry and legal interruptions, readied Bittersap Skybrand timing, full-suppression summon identity, Nexus transport classification/plane-wide scope, and all six actual Forge recipes. Seek exact acceptance only after genuine agreement; no automatic adoption from candidate return.','All16 AC5 procedures are applied; do not rerun one-shot application. Current ordinary count451 reviewed397 pending,175 complete standalone procedures. Source catalog unchanged.','Continue full75-area objective, remaining spells/environment/consumables/disease/feats/bestiary/Director/packaging/companion interfaces and final actual GPT whole-game flow. Latest verified GitHub backup18c6e3a predates current local work.']
    state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Obtained actual exact AC5 acceptance and integrated16 spells;1183 checks passed. Refreshed fullAC6 cohort with real worked-case improvements and103 sources; submitted actual joint review.','evidence':info(receipt)}
    state.setdefault('preservationManifests',[]).extend([info(A/'source-before-ac5-exact-acceptance-05/PRESERVATION_MANIFEST.json'),info(keep/'PRESERVATION_MANIFEST.json')]);checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'ordinarySpells':state['currentOrdinarySpellCounts'],'newSpellAdoptions':16}))

if __name__=='__main__':main()
