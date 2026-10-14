"""Record actual DI7 dispatch without adopting any proposed spell rule."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    submission=A/'DI7_JOINT_REVIEW_01_SUBMISSION.json';check_path=A/'DI7_JOINT_REVIEW_01_DISPATCH_CHECK.json'
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_COPY_CAPTURE_AND_NATURE_SOURCE.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_JOINT_SUBMISSION.json'
    delta=A/'DI7_JOINT_SUBMISSION_PROGRESS_DELTA.json';preservation=A/'navigation-before-di7-joint-submission'
    assert all(not p.exists() for p in [submission,check_path,checkpoint,delta,preservation])
    now=datetime.now(timezone.utc).isoformat();prep_path=A/'DI7_JOINT_REVIEW_01_PREPARATION.json';prep=read(prep_path)
    assert info(G/prep['archive']['path'])==prep['archive']
    dom=A/'DI7_JOINT_REVIEW_01_SENT_DOM.txt';shot=A/'DI7_JOINT_REVIEW_01_SENT.png';text=dom.read_text(encoding='utf-8')
    last=text[text.rfind('heading "You said:"'):]
    assert 'DI7-JOINT-REVIEW-01' in last and 'DD_DI7_Joint_Review_01.zip' in last and 'ChatGPT is responding' in last and 'button "Stop"' in last
    assert shot.exists()
    proposal=read(R/'data/director/spell_proposals/divination_rank7.json');ids={r['spellId'] for r in proposal['records']};assert len(ids)==7
    save(submission,{'recordedAtUtc':now,'reviewId':'DI7-JOINT-REVIEW-01','status':'sent-once-response-observed-generating',
        'archive':prep['archive'],'preparation':info(prep_path),'payloads':58,'mechanicalSpellIds':sorted(ids),
        'authoredExamples':14,'deferredReceiptExcludedFromReview':'planar-summons-greater',
        'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'browserId':'3','tabId':'125745933','sentDom':info(dom),'screenshot':info(shot),'pendingResponse':True,'replyReceived':False,
        'selectionEnabled':False,'sourceInformationDeleted':0,'cosmologyReviewed':False})
    state=read(previous);index_path=R/'data/director/higher_spell_operating_proposal_index.json';old_index=read(index_path);index=deepcopy(old_index)
    changed=[]
    for row in index['entries']:
        if row['spellId'] in ids:
            assert row['proposalState']=='complete-unadopted-proposal' and not row['jointReviewCompleted'] and not row['dedicatedSpellReviewSubmitted']
            row.update(dedicatedSpellReviewSubmitted=True,dedicatedReviewId='DI7-JOINT-REVIEW-01',dedicatedSubmissionReceipt=submission.relative_to(G).as_posix())
            changed.append(row['spellId'])
    assert set(changed)==ids
    unsent=[r for r in index['entries'] if r['proposalState']=='complete-unadopted-proposal' and not r['sharedAsFeatComparison'] and not r['dedicatedSpellReviewSubmitted']]
    dedicated=[r for r in index['entries'] if r['dedicatedSpellReviewSubmitted']]
    assert len(unsent)==109 and len(dedicated)==7 and index['counts']['completeUnadoptedProcedures']==187
    index['counts']['completeUnadoptedUnsentProcedures']=109;index['counts']['dedicatedReviewSubmittedUnadoptedProcedures']=7
    index['status']='Navigation only:187 complete unadopted procedures;71 shared only as feat comparisons,109 unsent,7 under dedicated DI7 joint review. No new spell approval follows dispatch.'
    for before,after in zip(old_index['entries'],index['entries']):
        if before['spellId'] not in ids:assert before==after
        else:
            restored=deepcopy(after);restored['dedicatedSpellReviewSubmitted']=False
            del restored['dedicatedReviewId'];del restored['dedicatedSubmissionReceipt'];assert restored==before
    scope=('Seven rank7 Divination mechanical procedures are now submitted once to actual GPT as DI7-JOINT-REVIEW-01, with58 manifest-verified payloads, all46 source input files,17 current class envelopes and complete counterpart/governing context. '
        'The response is visibly generating in Calibration Review Part2. Greater Planar Summons stays a literal excluded post-push receipt. '
        'Higher-spell totals remain187 unadopted procedures/374 authored examples:71 comparison-only,109 unsent and7 submitted for dedicated review;201 further mechanical proposals remain unwritten. Ordinary reviewed/pending counts remain412/436. '
        'Nature124 reproduced and137 propagation checks are complete, but16 NWT groups/47 variants remain local behavior follow-through. Copy source248/35 and capture189/31 remain finite evidence; paid releases and recipient outcomes remain open. '
        'No new rule is adopted by this dispatch. Final joint whole-game flow precedes GitHub push, verified remote and careful cosmology. Stop at50percent weekly usage remains controlling.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py';old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    assert info(ledger_path)==state['coverageLedger']
    for row in ledger['aspects']:
        if row['id'] in {'DD-12','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('reviewEvidence',[]).append(submission.relative_to(G).as_posix())
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [prep_path,check_path])
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-12','DD-69'}:assert before==after
    nav_text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_COPY_CAPTURE_NATURE_PROGRESS_DELTA.json")["changes"]\n';assert nav_text.count(chain)==1
    nav_text=nav_text.replace(chain,chain.rstrip('\n')+' + read(A / "DI7_JOINT_SUBMISSION_PROGRESS_DELTA.json")["changes"]\n')
    assert nav_text.count(state['status'])==1;nav_text=nav_text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert nav_text.count(marker)==1
    nav_text=nav_text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in [
        ('DI7 actual joint review —sent once; response pending',submission),('DI7 complete source package —58 payloads',prep_path),('DI7 dispatch and unchanged-rule checks',check_path),('DI7 visible GPT submission',shot)]))
    compile(nav_text,str(nav),'exec');preserved=[]
    for p in [index_path,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preservation/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        assert dest.read_bytes()==p.read_bytes();preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(index_path,index);save(ledger_path,ledger);nav.write_text(nav_text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [index_path,ledger_path,nav]],
        'sourceInformationDeleted':0,'newRuleAdoptions':0,'allApprovalAndClosureFlagsUnchanged':True})
    save(check_path,{'recordedAtUtc':now,'status':'pass','submittedIds':sorted(ids),'submittedCount':7,'unchangedOtherHigherSpellEntries':len(index['entries'])-7,
        'counts':index['counts'],'currentIndex':info(index_path),'submission':info(submission),'allSevenPreviouslyUnsent':True,
        'onlyDispatchMetadataChanged':True,'allOriginalSourceAndProcedureFieldsUnchanged':True,'deferredReceiptUnchangedAndExcluded':True,
        'allClosureAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newRulesAdopted':0,'cosmologyReviewed':False})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).append(deepcopy(state['activeGptReview']))
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),higherSpellIndex=info(index_path),higherSpellCounts=index['counts'],
        higherSpellIndexCheck=info(check_path),activeGptReview=read(submission),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='DI7 dispatch only. Prior Nature source adoption remains recorded in its controlling record and preceding checkpoint.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_JOINT_SUBMISSION. Actual GPT DI7-JOINT-REVIEW-01 is visibly responding in Chrome3/tab125745933. Inspect that same pending reply; never resend solely for elapsed time or observation timeout.',
        'Continue local Nature NWR01–03 and16 NWT groups/47 variants against received nonspell/fixed-area/rider/Ready completion. Preserve historical362/38 suite and original source snapshots.',
        'Copy source248/35 and capture189/31 do not implement paid release. Continue current own route, RP/components/history/interrupt, shared round cap and all seven recipient payload integrations.',
        'Higher spells:187 complete unadopted,71 comparison-only,109 unsent,7 DI7 submitted;201 remaining pre-push mechanical proposals,47 deferred receipts. Ordinary counts412/436 unchanged.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'submitted':7,'unsent':109}))


if __name__=='__main__':main()
