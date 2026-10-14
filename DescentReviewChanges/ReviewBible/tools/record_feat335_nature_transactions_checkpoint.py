"""Append finite Nature behavior evidence without closing the two open integrations."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json,shutil,subprocess,sys
from validate_feat_exact_01_composite_casting import read,info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_JOINT_SUBMISSION.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_NATURE_TRANSACTIONS.json'
    delta=A/'FEAT335_NATURE_TRANSACTIONS_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-nature-transactions'
    report_path=A/'FEAT335_NATURE_TRANSACTIONS_CHECK.json';scope_path=A/'FEAT335_NATURE_TRANSACTIONS_SCOPE.json'
    observation=A/'DI7_BROWSER_OBSERVATION_AFTER_NATURE_TRANSACTIONS.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,scope_path,observation])
    now=datetime.now(timezone.utc).isoformat();state=read(previous);report=read(report_path)
    assert report['status']=='pass' and report['checks']==185 and len(report['histories'])==75 and not report['failures']
    assert not report['natureAll47VariantsFulfilled'] and len(report['unfulfilledAcceptanceDetails'])==2
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    save(scope_path,{'report':info(report_path),'scope':report['scope'],'counts':report['counts'],
        'unfulfilledAcceptanceDetails':report['unfulfilledAcceptanceDetails'],'remainingLimits':report['limits'],
        'newRules':0,'natureAll47VariantsFulfilled':False,'fullFeatExactApproved':False,'runtimeApproved':False,'cosmologyReviewed':False})
    save(observation,{'recordedAtUtc':now,'reviewId':'DI7-JOINT-REVIEW-01','browserId':'3','currentTabId':'125745943',
        'observedTitle':'Calibration Review Part 2','observedUrl':state['activeGptReview']['conversationUrl'],
        'previousTabId':'125745933','previousTabUnavailable':True,'sameConversationRecoveredThroughExistingBrowserTabList':True,
        'titleAndUrlReadSucceeded':True,'handoffMarked':True,'currentReplyDomReadSucceeded':False,
        'observationFailure':'The current tab is present, but DOM snapshot and selector reads timed out in the Chrome CDP focus/dispatch path.',
        'latestKnownReplyState':'The original DI7 dispatch receipt observed generation. Current completion is unknown until a successful page observation.',
        'newMessageSent':False,'requestResent':False,'replyReceived':False,'reviewAdopted':False,
        'recoveryInstruction':'Keep Chrome3 and this same conversation. Read its current response when controls recover. Do not resend DI7 solely because observation failed.'})
    scope=('Nature has185 passing source-bound transaction checks across75 explicitly conditional histories. Native Ranger1 skill/ability and acquired Human Bard4/Versatile Mastery routes, component-free activation versus physical donor signals, own1RP payment, split paid activation and check, nonspell Ready, fixed terrain, absolute minute, actual own skill math, idle/recharge clocks and one-rider replacement are exercised. '
        'Source propagation137/reproduction124 and earlier borrowed362/38 evidence remain preserved. The next actual same-named ordinary cast and a source-authorized external replacement roll remain two explicit Nature acceptance integrations; full47-variant fulfillment is not claimed. '
        'The existing DI7 review was not resent. Chrome still identifies Calibration Review Part2 at the same URL, but current reply reads timed out; its completion is presently unverified. '
        'Seven DI7 procedures remain submitted and unadopted; ordinary spells412 reviewed/436 pending and higher187 unadopted remain unchanged. Copy paid release and broader feat use remain unfinished. '
        'Latest usage was34percent weekly used; stop at50percent remains controlling. No rule, approval, source deletion, GitHub push or cosmology review follows this finite evidence.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,scope_path,observation])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-Nature-transactions','recordedAtUtc':now,'checks':185,'conditionalHistories':75,
                'natureAll47VariantsFulfilled':False,'unfulfilledAcceptanceDetails':report['unfulfilledAcceptanceDetails'],'fullUseRuntimeApproved':False})
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-09','DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "DI7_JOINT_SUBMISSION_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_NATURE_TRANSACTIONS_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in [
        ('Nature transactions —185 checks,75 conditional histories',report_path),('Nature scope —two acceptance integrations remain',scope_path),('DI7 browser observation —reply completion currently unverified',observation)]))
    old_label='Nature16 behavior groups \\u2014authored expectations pending execution'
    assert text.count(old_label)==1;text=text.replace(old_label,'Nature16 authored expectation groups \\u2014see current partial behavior evidence')
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy);assert copy.read_bytes()==p.read_bytes()
        preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newRuleAdoptions':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        natureTransactions={'report':info(report_path),'scope':info(scope_path),'checks':185,'conditionalHistories':75,'natureAll47VariantsFulfilled':False,'fullUseRuntimeApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint appends only finite behavior evidence; earlier Nature source adoption remains separately recorded.')
    state['natureSourceApplication'].update(behaviorEvidence=info(report_path),behaviorScope=info(scope_path),finiteBehaviorFulfilled=False)
    state['activeGptReview'].update(tabId='125745943',currentObservation=info(observation),status='submitted-once-current-response-observation-unavailable',
        pendingResponse=True,replyReceived=False,currentCompletionKnown=False,instruction=read(observation)['recoveryInstruction'])
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_NATURE_TRANSACTIONS. Check fresh weekly Codex usedPercent and stop/save/pause at50 under owner instruction. Latest34 was measured during this turn.',
        'Nature185 checks/75 conditional histories now cover source-bound native Ranger1 and borrowed Bard4 transactions. Preserve this new successful report/module suite as historical scoped evidence when extending it.',
        'Close the two explicit Nature integrations with new descendants: next actual same-named paid ordinary cast and real external replacement-roll source/lineage before consequences. Other wider provider/Expertise/world/scheduler limits remain explicit. Do not label all47 fulfilled until the required evidence exists.',
        'Actual DI7 submission is preserved and must not be duplicated. Current Chrome3 tab125745943 has the same Calibration Review Part2 URL/title. DOM and selector reads timed out; current completion is unknown. Recover by observing this conversation through supported browser controls.',
        'Copy source248/35 and capture189/31 still do not implement paid release. Continue own provider, RP/components/history/interrupt, shared round cap and seven recipient profiles.',
        'Higher spells:187 complete unadopted,71 comparison-only,109 unsent,7 DI7 submitted;201 remaining mechanical proposals,47 deferred. Ordinary412/436 unchanged.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))


if __name__=='__main__':main()
