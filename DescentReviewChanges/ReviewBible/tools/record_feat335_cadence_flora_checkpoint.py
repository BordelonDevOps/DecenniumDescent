"""One-use current checkpoint: completed cadence correction, pending Flora review."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FULL_REVIEW_PREFLIGHT.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_CADENCE_AND_FLORA.json'
    delta=A/'FEAT335_CADENCE_AND_FLORA_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-cadence-and-flora'
    sent_path=A/'FEAT335_FLORA_SOURCE_CHECK_01_SUBMISSION.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,sent_path])
    state=read(previous);cadence=A/'FEAT335_CADENCE_FULFILLMENT_CHECK.json';report=read(cadence)
    assert report['checks']==2290 and not report['failures']
    for k in ['descriptors','builder','assembly','sourceChanges','reproduction','receivedArchive']:assert info(G/report[k]['path'])==report[k]
    register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CADENCE.json'
    flora=A/'FEAT335_FLORA_USE_CHECK.json';qualification=A/'FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json'
    prep=read(A/'FEAT335_FLORA_SOURCE_CHECK_01_PREPARATION.json')
    receipt=A/'FEAT335_FLORA_SOURCE_CHECK_01_SENT_DOM.txt';screenshot=A/'FEAT335_FLORA_SOURCE_CHECK_01_SENT.png'
    visible=receipt.read_text(encoding='utf-8');assert prep['id'] in visible and 'button "Stop"' in visible
    assert info(G/prep['archive']['path'])==prep['archive'];assert read(flora)['checks']==114
    sent={'id':prep['id'],'recordedAtUtc':now,'status':'sent-once-and-visibly-generating',
        'archive':prep['archive'],'visibleReceipt':info(receipt),'screenshot':info(screenshot),
        'conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'browserId':'3','tabId':'125745933','oldUserTabId':'125745532',
        'tabRecovery':'After the completed cadence download reset the browser session and its old handle remained unattached, opened the same conversation in a fresh Chrome tab. No new GPT conversation or duplicate message was created.',
        'questions':['FLQ-01','FLQ-02','FLQ-03','FLQ-04'],'fullFeatExactApproved':False}
    save(sent_path,sent)
    scope=('GPT completed FEAT335-CADENCE-CHECK-01. All 381 received checks reproduce semantically; Windows CRLF is the only byte difference. '
        'Its narrow NEW FS-06 completion is applied identically in public/internal shared rules and the manuscript. Eleven unqualified turn rows and Overrun now use actual-turn keys; Savage Attacker, Eldritch Combat and the other requested exceptions retain their keys. '
        'A 2,290-check current fulfillment preserves all 335 source/acquisition records and 177 unrelated descriptor fields; old builders, reports and assemblies remain unchanged with newly named current descendants. '
        'A bounded Flora/Trapcasting pass contains 114 checks in 23 histories across three modes and six actual casting providers. Its fixed-at-creation level-10 inference is explicitly unapproved in the scope qualification; no full Flora runtime claim follows. '
        'Actual GPT is now answering FEAT335-FLORA-SOURCE-CHECK-01 in Calibration Review Part 2, covering provider loss, first-body early ending, level-10 growth and interrupted command/phase boundaries. '
        'The full feat exact-review FXC04/06–10 use/case/interfaces remain unfinished. Higher spells remain 187 unadopted procedures/374 examples, 201 pre-push questions and 47 deferred; ordinary totals remain 412 reviewed/436 pending. No source deletion, push, whole-game approval or cosmology review occurred.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    new_evidence=[cadence,register,flora,qualification,sent_path]
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in new_evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-cadence-and-bounded-Flora','recordedAtUtc':now,
                'cadenceReproducedChecks':381,'cadenceCurrentChecks':2290,'floraChecks':114,'floraHistories':23,
                'floraUnapprovedGrowthInference':True,'cadenceReviewFulfilled':True,'floraReviewPending':True,'fullFeatCandidateApproved':False})
            row['openIssues']=[('Cadence question is fulfilled in FEAT335_CADENCE_FULFILLMENT_CHECK.json; remaining exact-review scope is still governed by FEAT335_FULL_EXACT_REVIEW_PREFLIGHT.json. Receive the already sent FEAT335-FLORA-SOURCE-CHECK-01; do not promote the unapproved growth inference. Finish the distinct FXC04/06–10 use/case/interfaces before full335 submission.' if 'Receive the already sent FEAT335-CADENCE-CHECK-01' in x else x) for x in row['openIssues']]
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old_ledger.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');old_chain=' + read(A / "FEAT335_FULL_REVIEW_PREFLIGHT_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(old_chain)==1
    text=text.replace(old_chain,old_chain.rstrip('\n')+' + read(A / "FEAT335_CADENCE_DERIVED_OPERATIONS.json")["changes"] + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    links=[('Current acquisition register — cadence addendum fulfilled',register),('Cadence fulfillment — 2290 current checks and381 reproduced',cadence),
        ('Flora use —114 bounded checks, read qualification before relying on growth case',flora),('Flora scope qualification — four concrete source questions',qualification),
        ('Flora source review — sent once to actual GPT',sent_path)]
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in links))
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
        assert p.read_bytes()==copy.read_bytes();preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':1})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        cadenceFulfillment={'review':'FEAT335-CADENCE-CHECK-01','status':'fulfilled-in-narrow-scope','report':info(cadence),'checks':2290,'reproducedChecks':381,'fullFeatCandidateApproved':False},
        boundedFloraUse={'report':info(flora),'qualification':info(qualification),'checks':114,'histories':23,'fullFloraRuntimeApproved':False,'unapprovedGrowthInference':True},
        activeGptReview={'id':sent['id'],'status':'sent-once-response-generating','submission':info(sent_path),
            'conversationUrl':sent['conversationUrl'],'browserId':'3','tabId':'125745933','lastObservedStopVisible':True,
            'instruction':'Read the one pending Flora source response. Cadence and the older acquisition audit are terminal; do not resend or poll their old replies.'},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=1,newRuleAdoptionCountScope='This checkpoint: one actual-GPT-approved minimal FS06 cadence completion; no Flora source inference approved.')
    state['feat335CorrectionFulfillment']['currentRegister']=info(register);state['featAcquisitionAudit']['currentFollowthrough']=info(register)
    state['featAllowanceAssembly'].update(assembly=report['assembly'],descriptors=report['descriptors'],cadenceFulfillment=info(cadence))
    state['featFullReviewPreflight'].update(cadenceReviewFulfilled=True,cadenceFulfillment=info(cadence),fullExactSubmissionReady=False)
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_CADENCE_AND_FLORA. Cadence narrow review is fulfilled with preserved old files and new current descendants; do not rerun one-use builders/reports.',
        'Actual GPT pending FEAT335-FLORA-SOURCE-CHECK-01 in Chrome3/tab125745933, same Calibration Review Part2 conversation. Read terminal reply; never resend on uncertain actions. Four questions are in scope qualification. The original user tab125745532 remains open; use fresh working tab125745933.',
        'Flora114/23 bounded model/report is qualified: fixed-at-first-creation level10 entitlement is an unapproved inference; source-loss and first-body-early-ending branches remain out of slice; command and phase are collapsed. Do not claim these illegal or settled until GPT source ruling. Preserve historical report/model.',
        'Remaining finite exact-review FXC04/06–10 work still needed. Useful independent next slice: twelve borrowed stunts, or actual Verdant Bond message/Nature spell-route effects. No full335 submission yet.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))
if __name__=='__main__':main()
