"""Record Verdant message evidence and actual pending Nature source review."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'

def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_BORROWED_SKILL.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_VERDANT_AND_NATURE.json'
    delta=A/'FEAT335_VERDANT_AND_NATURE_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-verdant-and-nature'
    report_path=A/'FEAT335_VERDANT_MESSAGE_CHECK.json';qualification=A/'FEAT335_VERDANT_MESSAGE_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification]);now=datetime.now(timezone.utc).isoformat()
    report=read(report_path);assert report['checks']==92 and not report['failures'] and len(report['histories'])==19
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    submission_path=A/'FEAT335_NATURE_SOURCE_CHECK_01_SUBMISSION.json';submission=read(submission_path)
    assert submission['status']=='sent-once-response-observed-generating' and submission['stopVisible']
    assert info(G/submission['archive']['path'])==submission['archive']
    save(qualification,{'report':info(report_path),'scope':report['scope'],'remainingLimits':report['limits'],
        'paidSource':'Human Imperial Warrior with real level4 Wizard Initiate and level8 paid Verdant Bond; no Conjure Flora grant or invented plant body.',
        'testedBoundaries':['Brief25-word message; one actual uninterrupted active minute; original24-hour deadline.',
            'Designated known ally or self; genuinely future passage within10ft; no trigger merely from recording nearby.',
            'Ordinary audible delivery once, including real other hearers; no telepathy, remote confirmation or backlog when no one hears.',
            'Actual rooted stand/reach, interrupted work, destroyed stand, beneficialLR use recovery and no duration/body reset.',
            'Actual conscious/perceived/LoE plant communication limited to current coarse fear/hunger/dormancy or no response; no invented history/intelligence.'],
        'notTestedHere':['Full wilderness Nature task advantage and terrain movement integration.',
            'Actual global movement/acoustics/work/rest scheduling and arbitrary independently scoped magical suppression.',
            'Full nature-route casting, whole335 feat execution, human playtesting or balance.'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'cosmologyReviewed':False})
    state=read(previous)
    scope=('Verdant Bond stored-message and simple plant-communication follow-through passes92 checks across19 conditional paid-source histories. '
        'The finite procedure conserves oneLR use, actual minute of active recording, a25-word message, designated known ally including self, original24-hour deadline, first genuine future passage within10ft, ordinary audible one-time delivery and actual generator destruction. '
        'Invalid declarations spend nothing; interrupted paid work has no message/refund; beneficialLR restores only the use. Plant replies remain coarse present fear/hunger/dormancy or no response, with no historical knowledge. '
        'Actual work/rest/geometry/hearing/identity are conditional premises; wilderness task/terrain and full Nature casting remain separate. '
        'A new exact source mismatch is submitted once to actual GPT as FEAT335-NATURE-SOURCE-CHECK-01: Nature Whisper original minor-spell wording conflicts with an unassigned normalized rank and missing component/Dissonance/Counterspell interface. '
        'Its23-payload726171-byte packet is verified and the same Calibration Review Part2 response is visibly running. No classification is invented while that ruling is pending. '
        'Flora source interfaces and borrowed-skill transaction evidence remain fulfilled in their stated finite scopes. Full335 review, broader game work, final joint flow agreement, GitHub then cosmology sequence and50-percent usage stop remain unchanged.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification,submission_path,A/'FEAT335_NATURE_SOURCE_CHECK_01_PREPARATION.json'])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-Verdant-messages-and-Nature-source-question','recordedAtUtc':now,'checks':92,'conditionalHistories':19,'fullUseRuntimeApproved':False})
            issues=[]
            for issue in row['openIssues']:
                if 'No request is currently pending.' in issue:
                    issue=issue.replace('No request is currently pending.','Nature Whisper now has its own distinct pending source review FEAT335-NATURE-SOURCE-CHECK-01; earlier acquisition/cadence/Flora replies remain terminal.')
                if 'Remaining Flora scope includes' in issue:
                    issue=issue.replace('Verdant message/casting interfaces','Verdant wilderness-task/terrain and full casting interfaces (stored-message/simple-communication slice is now separately evidenced)')
                issues.append(issue)
            issues.append('Read the already pending FEAT335-NATURE-SOURCE-CHECK-01 terminal reply in the same actual GPT chat; do not resend. Resolve its four exact rank/classification, component, Dissonance/history and paid-activation/later-check questions before removing the earlier conditional minor-Weave-clearance limitation.')
            row['openIssues']=issues
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_BORROWED_SKILL_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_VERDANT_AND_NATURE_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Verdant message and simple plant communication —92 checks,19 histories',report_path),('Verdant message — conditional scope and remaining work',qualification),
        ('Nature Whisper source questions — actual GPT submission',submission_path),('Nature Whisper — full source packet preparation',A/'FEAT335_NATURE_SOURCE_CHECK_01_PREPARATION.json')]))
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy);assert copy.read_bytes()==p.read_bytes()
        preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations',[]).append(deepcopy(state['activeGptReview']))
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        verdantMessages={'report':info(report_path),'scope':info(qualification),'checks':92,'conditionalHistories':19,'fullUseRuntimeApproved':False},
        activeGptReview={'id':'FEAT335-NATURE-SOURCE-CHECK-01','status':'sent-once-response-observed-generating','submission':info(submission_path),
            'preparation':info(A/'FEAT335_NATURE_SOURCE_CHECK_01_PREPARATION.json'),'conversationUrl':submission['conversationUrl'],
            'browserId':'3','tabId':submission['tabId'],'pendingResponse':True,'replyReceived':False,'lastObservedStopVisible':True,
            'instruction':'Read this one pending source response. Earlier Flora, cadence and acquisition reviews are terminal; do not resend unchanged packets.'},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint adds bounded Verdant evidence and a pending source question only; no unresolved Nature classification has been adopted.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_VERDANT_AND_NATURE. Verdant92/19 stored-message and simple communication slice recorded; no whole Flora/feat runtime closure.',
        'Actual GPT FEAT335-NATURE-SOURCE-CHECK-01 is visibly running in Chrome3/tab125745933, same Calibration Review Part2. Read its eventual terminal reply; preserve exact archive and do not resend on observation timeouts.',
        'Nature classification, components, strain/history and activation/check interfaces are unresolved pending four questions. Do not replace source uncertainty with the older clearance boolean. Independent remaining work includes Verdant terrain/task, Flora trap identification, seven copy profiles, ritual/Time/transfer interfaces and full FXC06–10 finite cases.',
        *state['safeNextActions'][-2:]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))

if __name__=='__main__':main()
