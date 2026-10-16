"""Preserve actual GPT submission and expose the complete AC6 draft without adoption."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, hashlib, json, subprocess, sys, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_REPAIR_04.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_LOCAL_FINAL_05.json'
    receipt=A/'AC5_LOCAL_FINAL_05_SUBMISSION_RECEIPT.json'
    delta=A/'AC5_LOCAL_FINAL_05_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-ac5-local-final-05'
    assert not any(p.exists() for p in [checkpoint,receipt,delta,keep])
    native=A/'AC5_LOCAL_FINAL_05_SUBMITTED_NATIVE.json'; obs=read(native); turn=obs['turns'][0]
    assert turn['id']=='cc45471f-2ea4-4665-9817-c02f98793e00'
    msg=next(x for x in turn['items'] if x['type']=='userMessage')
    actual=''.join(x['text'] for x in msg['content'] if x['type']=='text')
    suffix='\n\n[User attached 1 file; file contents were not included]'
    if actual.endswith(suffix): actual=actual[:-len(suffix)]
    request=A/'AC5_LOCAL_FINAL_05_REQUEST.txt'; archive=A/'DD_AC5_Local_Final_05.zip'
    assert actual==request.read_text(encoding='utf8')
    attachment=next(x for x in obs['attachments'] if x['name']==archive.name)
    assert Path(attachment['path']).read_bytes()==archive.read_bytes()
    with zipfile.ZipFile(archive) as z:
        bindings=json.loads(z.read('SOURCE_MANIFEST.json'))['bindings']; assert len(bindings)==92
        for b in bindings:
            raw=z.read('sources/'+b['path']); assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
            assert (G/b['path']).read_bytes()==raw
        assert z.read('PREVIOUS_RETURN.zip')==(A/'DD_AC5_Repair_04_Return.zip').read_bytes()
        assert z.read('CORRECTIONS.json')==(A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json').read_bytes()
        candidate=A/'ac5-local-final-05-candidate'
        for p in candidate.iterdir(): assert z.read('candidate/'+p.name)==p.read_bytes()
    browser=A/'AC5_LOCAL_FINAL_05_SUBMITTED_BROWSER.txt'; screenshot=A/'PART4_AC5_LOCAL_FINAL_05_SUBMITTED.png'
    assert 'button "Stop"' in browser.read_text(encoding='utf8') and screenshot.stat().st_size>10000
    rec={'id':'AC5-LOCAL-FINAL-05-SUBMISSION','recordedAtUtc':now,'status':'Submitted once to actual GPT Part4; exact request and attachment confirmed. Browser shows active response inspecting the candidate. Awaiting exact acceptance or concrete findings.', 'threadId':obs['thread']['id'],'title':obs['thread']['title'],'userTurnId':turn['id'],'browserId':'3','tabId':'125746324','archive':info(archive),'request':info(request),'nativeObservation':info(native),'browserObservation':info(browser),'screenshot':info(screenshot),'uploadedAttachmentBytesMatch':True,'exactRequestMatches':True,'archiveSourcesReverified':92,'candidateFiles':8,'spellIdentities':16,'placements':17,'caseCount':61,'historicalTexts':22,'correctionCount':3,'localCheck':info(A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json'),'checkCount':617,'expectedReturn':'DD_AC5_Exact_Acceptance_05.zip','newSpellAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    receipt.write_bytes(encoded(rec))
    start=G/'START_HERE.md'; builder=R/'tools/build_review_map.py'; ledger=R/'data/playtest/game_development_coverage.json'
    originals={}; saved=[]
    for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes(); q=keep/p.relative_to(G); q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(raw); originals[p]=raw
        saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode(); assert text.count(previous.relative_to(G).as_posix())==1
    text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    paragraphs={
      '**Current GPT conference:**':'**Current GPT conference:** The [complete AC5 Repair04 return](docs/audit/2026-10-08/full-game/DD_AC5_Repair_04_Return.zip) is preserved: 16 spell identities, 17 placements, 61 cases and 92 frozen sources. [Independent structural review](docs/audit/2026-10-08/full-game/AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json) passed 858 checks. Three [local corrections](docs/audit/2026-10-08/full-game/AC5_LOCAL_FINAL_05_CORRECTIONS.json) repair antimagic and wall geometry and clarify portal movement costs; 617 local checks passed. The [exact corrected candidate is submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC5_LOCAL_FINAL_05_SUBMISSION_RECEIPT.json). Acceptance is pending. No AC5 spell is adopted yet; 435 ordinary spells remain reviewed and 413 pending.',
      '**Next spell group, prepared for review:**':'**Next spell group, prepared for review:** The [complete AC6 draft register](docs/audit/2026-10-08/full-game/AC6_COMPLETE_DRAFT_REGISTER_02.json) now covers all 14 identities and 16 printed placements. [Ten newly completed procedures](DescentReviewChanges/ReviewBible/data/director/spell_proposals/ac6_remaining_procedures_draft_02.json) add 22 current examples and correct an earlier audit error: the actual Wizard Dispel card is a rank-three spell. [Local preservation/reference review](docs/audit/2026-10-08/full-game/AC6_REMAINING_PROCEDURES_CHECK_02.json) passed 362 checks. The [three planar procedures](DescentReviewChanges/ReviewBible/data/director/spell_proposals/ac6_planar_completion_draft_02.json) retain 23 examples, and the [Forge revision](DescentReviewChanges/ReviewBible/data/director/spell_proposals/resonance_forge_revision_02.json) retains six actual-recipe examples. These are complete procedure drafts, with explicitly partial or conditional examples still requiring work. All remain unsent and unadopted. Refresh accepted AC5 dependencies and finish outstanding examples before joint AC6 review.'
    }
    for marker,paragraph in paragraphs.items():
        begin=text.index(marker); end=text.index('\n\n',begin); text=text[:begin]+paragraph+text[end:]
    start.write_text(text,encoding='utf8',newline='\n')
    evidence=[receipt,A/'AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json',A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json',A/'AC6_COMPLETE_DRAFT_REGISTER_02.json',A/'AC6_REMAINING_PROCEDURES_CHECK_02.json']
    cov=json.loads(originals[ledger]); oldcov=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident); old=deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac5-local-final-05-ac6-complete-draft-02','recordedAtUtc':now,'status':'Exact corrected AC5 candidate submitted for actual GPT acceptance; full 14-identity AC6 procedure draft assembled but partial examples/dependency refresh and joint review remain.','ac5Identities':16,'ac5Cases':61,'ac5LocalChecks':617,'ac6DraftIdentities':14,'ac6RemainingProceduresAuthored':10,'ac6NewExamples':22,'ac6LocalChecks':362,'newSpellAdoptions':0})
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in oldcov['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    code=originals[builder].decode(); tail=' + read(A / "AC5_REPAIR_04_NAVIGATION_DELTA.json")["changes"]\n'; assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC5_LOCAL_FINAL_05_NAVIGATION_DELTA.json")["changes"]\n',1)
    additions=[('AC5 — exact corrected candidate submitted for acceptance',receipt.name),('AC5 — three local geometry and movement corrections','AC5_LOCAL_FINAL_05_CORRECTIONS.json'),('AC5 — complete Repair04 preservation and source check','AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json'),('AC6 — all fourteen complete procedure drafts','AC6_COMPLETE_DRAFT_REGISTER_02.json'),('AC6 — ten remaining procedure draft checks','AC6_REMAINING_PROCEDURES_CHECK_02.json')]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in additions),1)
    code=code.replace('    featured = [\n','    featured = [\n        ("AC5 — exact corrected chapter pending acceptance", "docs/audit/2026-10-08/full-game/ac5-local-final-05-candidate/PLAYER_CHAPTER.md"),\n',1)
    scope='435 reviewed / 413 pending ordinary spells. The exact AC5 candidate05 is submitted to actual GPT Part4:16 identities,17 placements,61 cases,92 sources;617 local checks pass. No AC5 adoption. All14 AC6 identities now have complete local procedure drafts, including10 new procedures and22 examples;362 checks pass. Partial examples, accepted AC5 dependency refresh and joint review remain. The full75-area goal remains open.'
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']; assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1); compile(code,str(builder),'exec'); builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':0,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8'); assert run.returncode==0,(run.stdout[-1500:],run.stderr[-1500:])
    build=read(A/'REVIEW_MAP_BUILD.json'); assert not build['missingLinks']
    state=read(previous); prior=deepcopy(state['activeGptReview']); prior.update(status='Complete Repair04 received and preserved;858 structural checks pass. Three concrete local corrections prepared and submitted for exact acceptance.',returnReceived=True,returnedArchive=info(A/'DD_AC5_Repair_04_Return.zip'),structuralCheck=info(A/'AC5_REPAIR_RETURN_04_STRUCTURAL_CHECK.json'),localCorrectionReview=info(A/'AC5_LOCAL_FINAL_05_CORRECTIONS.json'))
    state.setdefault('priorCompletedGptReviews',[]).append(prior)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress: complete AC6 procedures and local AC5 corrections prepared',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Exact candidate05 submitted after local corrections; all AC6 procedures drafted. No rule adoption.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview']={'reviewId':'AC5-LOCAL-FINAL-05','threadId':rec['threadId'],'title':rec['title'],'browserId':'3','tabId':'125746324','conversationUrl':prior['conversationUrl'],'submission':info(receipt),'userTurnId':turn['id'],'status':rec['status'],'generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(browser),'observationTimeoutMeansTerminal':False}
    state['ac6CompleteLocalDraft02']={'register':info(A/'AC6_COMPLETE_DRAFT_REGISTER_02.json'),'remainingProcedures':info(R/'data/director/spell_proposals/ac6_remaining_procedures_draft_02.json'),'remainingCheck':info(A/'AC6_REMAINING_PROCEDURES_CHECK_02.json'),'planarProcedures':info(R/'data/director/spell_proposals/ac6_planar_completion_draft_02.json'),'forgeProcedure':info(R/'data/director/spell_proposals/resonance_forge_revision_02.json'),'completeProcedureIdentities':14,'placements':16,'newRemainingProcedures':10,'newExamples':22,'remainingChecks':362,'status':'Complete procedure drafts; explicitly partial/conditional worked examples still require completion and dependency refresh. Unsent/unadopted.','sourceCorrection':'Wizard class Dispel at wizard.json/cards/19 is a rank-three wizard-spell; earlier AC6-N02 nonspell premise is retained as superseded audit error.'}
    state['safeNextActions']=['Continue SAME Part4 exact-review user turn cc45471f-2ea4-4665-9817-c02f98793e00; do not resend on observation timeout. Current tab125746324.','Preserve actual exact acceptance or concrete findings. Verify all eight candidate file hashes,92 source bindings,16 identities17 placements61 cases22 history and zero substantive blockers before any authored adoption.','Apply accepted AC5 reversibly with exact model/source copies, truthful index counts and retained historical evidence. Candidate-only response is not acceptance.','Complete explicitly partial AC6 examples and refresh all14 drafts against accepted AC5 interfaces before actual GPT conference. Preserve full old draft and historical questions.','Continue full75-area objective, all pending spells and other systems, packaging and final actual GPT whole-game flow. Latest verified GitHub backup18c6e3a predates this local work.']
    state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Confirmed actual continuation; uploaded and submitted exact corrected AC5 candidate; complete AC6 drafts now discoverable.','evidence':info(receipt)}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json')); checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'ordinarySpells':state['currentOrdinarySpellCounts'],'newSpellAdoptions':0}))

if __name__=='__main__': main()
