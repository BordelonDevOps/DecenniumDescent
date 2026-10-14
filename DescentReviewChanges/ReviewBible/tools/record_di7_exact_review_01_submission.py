"""Record a verified single exact-review dispatch without implying acceptance."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_BOUNDARY_AND_COPY_SOURCE.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_EXACT_SUBMISSION.json'
    delta=A/'DI7_EXACT_SUBMISSION_PROGRESS_DELTA.json'; preservation=A/'navigation-before-di7-exact-submission'
    dispatch_path=A/'DI7_EXACT_REVIEW_01_SUBMISSION.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,dispatch_path])
    state=read(previous); now=datetime.now(timezone.utc).isoformat()
    preparation_path=A/'DI7_EXACT_REVIEW_01_PREPARATION.json'; prepared=read(preparation_path)
    report_path=A/'DI7_FATE_MODE_ADMISSION_CHECK.json'; report=read(report_path)
    assert report['status']=='pass' and report['checks']==43 and report['historyCount']==12 and not report['failures']
    for b in report['sourceBindings']: assert info(G/b['path'])==b
    for key in ['archive','manifest','request','context']: assert info(G/prepared[key]['path'])==prepared[key]
    assert prepared['payloadsVerified']==213
    dom_path=A/'DI7_EXACT_REVIEW_01_SENT_DOM.txt'; screenshot=A/'DI7_EXACT_REVIEW_01_SENT.png'
    dom=dom_path.read_text(encoding='utf-8')
    assert 'DD_DI7_Exact_Review_01.zip' in dom and 'DI7-EXACT-REVIEW-01' in dom and 'ChatGPT is responding' in dom
    assert screenshot.is_file()
    context=read(G/prepared['context']['path']); assert len(context['currentClassEnvelopes'])==17 and all(x['matchesEmbeddedEnvelope'] for x in context['currentClassEnvelopes'])
    dispatch={'reviewId':'DI7-EXACT-REVIEW-01','recordedAtUtc':now,'status':'sent-once-response-running-at-observation',
        'archive':prepared['archive'],'manifest':prepared['manifest'],'request':prepared['request'],'context':prepared['context'],
        'preparation':info(preparation_path),'payloadsVerified':213,'browserId':'3','tabId':'125745960',
        'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'sentDOM':info(dom_path),'visibleProof':info(screenshot),'pendingResponse':True,'replyReceived':False,
        'sevenCardExactReviewSubmitted':True,'fullFiniteFulfilled':False,'exactApproved':False,
        'scope':'Complete exact seven-card review with full envelopes, original sources,14 examples/14 issues,93-case evidence and explicit source-only/unsupported runtime qualifications.',
        'instruction':'Observe this same conversation. A transient timeout is not a missing/terminal response. Do not resend or replace the submitted package.',
        'sourceInformationDeleted':0,'cosmologyReviewed':False,'pushed':False}
    dispatch_path.write_bytes(encoded(dispatch))
    scope=('Complete seven-card DI7 exact review is now actually sent once to Calibration Review Part2; GPT is visibly responding. '
        'The21,577,110-byte archive SHA22831b3aa3f6ba40083ba3dbcfb4f2d18505e9c690c73f9784b303c01e2ae9df contains213 verified payloads plus manifest, all current seven public/internal/manuscript cards,49+44 finite expectations,14 original/corrected examples,13 mechanical issues and DI7-X14 receipt. '
        'All17 current class envelopes match the embedded comparisons. Original18 substitutions, AP-AS actual readers, subsequent exact source addenda and preserved before bytes accompany full governing/source files and evaluator import closure. '
        'Fate admission adds43 checks/12 histories plus11 source/cost proofs: actual observed paid Counterspell Reaction and Lifedraw miss fail before any Fate spend; exact necessary source predicates reject damaging summon/recursive/Reaction/rank9/incomplete modes without fabricating their cast histories. '
        'The selected Coin/Suggestion sources have no separate consumed material or acquired charge; all other indispensable independent-entitlement payload adapters remain explicitly unavailable. This qualification is called out for GPT verdict; no blanket full49/93, arbitrary runtime or exact approval is claimed. '
        'The first local staging attempt hit Windows nested path limits; no source was lost. Partial staging copies remain; the complete archive was built directly from originals and all213 payload hashes verified. '
        'Ordinary412/436, human evidence and source/selection flags remain unchanged. Fresh weekly usage46percent; owner stop at50 remains mandatory. Nothing deleted or pushed, and cosmology remains after actual final joint whole-game flow, authorized push and verified remote.')
    ledger_path=R/'data/playtest/game_development_coverage.json'; nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']; before=read(ledger_path); ledger=deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,preparation_path,dispatch_path])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'DI7-exact-seven-actual-submission','recordedAtUtc':now,'checks':43,'histories':12,'sourceProofs':11,'payloadsVerified':213,'sent':True,'exactApproved':False,'full49Fulfilled':False})
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k)==new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-09','DD-12','DD-14','DD-69'}: assert old==new
    assert {k:v for k,v in before.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "DI7_BOUNDARY_COPY_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain)==1 and text.count(state['status'])==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "DI7_EXACT_SUBMISSION_PROGRESS_DELTA.json")["changes"]\n').replace(state['status'],scope,1)
    marker='    pending = [\n'; assert text.count(marker)==1
    items=[('Actual complete DI7 exact submission —GPT response pending',dispatch_path),('Complete213-payload exact review archive',G/prepared['archive']['path']),
        ('Fate mode gate —43 checks,12 paid histories and11 scoped source proofs',report_path),('Exact-review request and evidence qualifications',G/prepared['request']['path']),('Exact submission visible proof',screenshot)]
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in items))
    compile(text,str(nav),'exec'); preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preservation/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(p.read_bytes())
        assert dest.read_bytes()==p.read_bytes(); preserved.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text,encoding='utf-8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],'allOtherAspectsUnchanged':True,'allClosureAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'spellPromotions':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        di7FateModeAdmission={'report':info(report_path),'module':info(R/'tools/di7_fate_mode_admission.py'),'checks':43,'histories':12,'sourceProofs':11,'qualifications':report['conditionalPremises']},
        di7ExactReviewSubmission={'receipt':info(dispatch_path),**dispatch},activeGptReview=dispatch)
    state['di7FiniteEvidenceInventory']['actualSubmission']=info(dispatch_path)
    state['di7FiniteEvidenceInventory']['currentModeGateEvidence']=info(report_path)
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_EXACT_SUBMISSION. Fresh weekly usage46percent; stop at50 mandatory.',
        'Actual GPT DI7-EXACT-REVIEW-01 sent once to Chrome3 Calibration Review Part2 tab125745960, same saved conversation URL. Latest observed ChatGPT is responding; no verdict yet. Re-poll same live page, never resend on timeout. Re-mark handoff each turn.',
        'Archive213payloads+manifest,21,577,110bytes SHA22831b3aa3f6ba40083ba3dbcfb4f2d18505e9c690c73f9784b303c01e2ae9df. The archive is authoritative; input folder contains a preserved PARTIAL first-attempt staging tree after Windows long-path failure. Build succeeded by zip direct from current originals; all payloads verified. Do not mistake partial local staging copies for complete current package.',
        'Full exact card/procedure/source/current public/internal/manuscript,17 matching classes,14 examples/14issues,source-direction preservation and all historical/current evidence are included. GPT request explicitly calls out negative necessary-condition proofs and two selected-mode empty independent cost sets versus unimplemented nonempty-cost adapters. Await its concrete exact verdict; no full49/93 or arbitrary-runtime claim.',
        'Mode gate43/12 plus11 source/cost proofs is successful; do not rerun/overwrite. Real Counterspell Reaction and Lifedraw natural1 miss are paid/observed before atomic Fate rejection. Lifedraw hit branch is intentionally unsupported; rejected summon/recursive modes have source proofs, not fabricated cast histories. Fate child positive Coin still pays19 and preserves original separate object.',
        'All existing ordinary412/436, candidate statuses and approvals remain unchanged. If GPT returns guarded corrections preserve exact package bytes first; apply only concrete reviewed changes with same-path delta/inverse evidence. Source guidance never equals full-game acceptance.',
        'While exact review runs, independent remaining work includes feat-copy paid releases, bestiary/Director prepared reviews and whole-game packaging. User stop50 takes precedence; at threshold save pending review details, explicitly pause goal, report and stop.',state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state)); print(json.dumps({'checkpoint':info(checkpoint),'submission':info(dispatch_path),'navigationLinks':navigation['existingDistinctLinks'],'weeklyUsagePercent':46,'gptResponsePending':True}))


if __name__=='__main__': main()
