"""Preserve the new reading preflight and one actually pending GPT question."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
from validate_feat_exact_01_composite_casting import read,info

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_ACQUISITION_ASSEMBLY.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FULL_REVIEW_PREFLIGHT.json'
    delta=A/'FEAT335_FULL_REVIEW_PREFLIGHT_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-full-review-preflight'
    assert all(not p.exists() for p in [checkpoint,delta,preservation])
    state=read(previous);preflight=A/'FEAT335_FULL_EXACT_REVIEW_PREFLIGHT.json'
    reading=A/'FEAT335_CURRENT_READING_FILES_V2_CHECK.json';submission=A/'FEAT335_CADENCE_CHECK_01_SUBMISSION.json'
    report=read(reading);assert report['checks']==5382 and not report['failures']
    for b in report['sourceBindings']:assert info(G/b['path'])==b
    sent=read(submission);assert sent['status']=='sent-once-and-visibly-generating'
    for k in ['archive','visibleReceipt','screenshot']:assert info(G/sent[k]['path'])==sent[k]
    scope=('All335 feat acquisition records are locally assembled with4307 checks and all finite acquisition-audit groups joined. '
        'A new5382-check current reading preflight preserves all327 questions,660 original example positions,28 additional cases,eight reviewed records,complete reader procedures and public allowlists. '
        'The first reading check’s sole failure was its historical allowlist omitting the already approved ACQ03 Spell Focus policy-reference field; original checker/report are preserved and the exact-source-bound V2 passes without content changes. '
        'FEAT335-CADENCE-CHECK-01 is now actually sent and generating in Calibration Review Part2: verify the local unqualified-once-per-turn/extra-turn descriptor inference before relying on it. No resend or generic acquisition re-review is needed. '
        'The finite full-review preflight lists remaining FXC04/06–10 use,case and interface work; full335 exact submission is not ready yet. '
        'Higher spells remain187 unadopted procedures/374 examples,201 pre-push questions and47 deferred; ordinary totals412 reviewed/436 pending. No deletion,push,full-game approval or cosmology review occurred.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [reading,preflight,submission])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-full-review-preflight','recordedAtUtc':now,
                'readingChecks':5382,'cadenceReviewPending':True,'fullExactSubmissionReady':False,'fullFeatCandidateApproved':False})
            row['openIssues'].append('FEAT335_FULL_EXACT_REVIEW_PREFLIGHT.json governs remaining exact-review work. Receive the already sent FEAT335-CADENCE-CHECK-01 narrow response, correct only concrete descriptor/source mismatches, and finish named FXC04/06–10 finite interfaces before full335 exact submission. The acquisition assembly does not close all use/case/clock gates.')
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old_ledger.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');old_chain=' + read(A / "FEAT335_ALLOWANCE_ASSEMBLY_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(old_chain)==1
    text=text.replace(old_chain,old_chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Full feat exact-review preflight — remaining finite use and case work',preflight),
        ('Current reading files —5382 checks, all688 authored positions preserved',reading),
        ('Focused cadence review — actual GPT submission receipt',submission)]))
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
        assert p.read_bytes()==copy.read_bytes();preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    nav_report=read(A/'REVIEW_MAP_BUILD.json');assert not nav_report['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        featFullReviewPreflight={'preflight':info(preflight),'currentReadingCheck':info(reading),'checks':5382,
            'cadenceSubmission':info(submission),'fullExactSubmissionReady':False,'fullFeatCandidateApproved':False},
        activeGptReview={'id':sent['id'],'status':'sent-once-response-generating','submission':info(submission),
            'conversationUrl':sent['conversationUrl'],'browserId':sent['browserId'],'tabId':sent['tabId'],
            'lastObservedStopVisible':True,'instruction':'Receive the current focused cadence response; never resend on an uncertain click or read old terminal acquisition audit as a pending reply.'},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':nav_report['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint: current reading preservation checks and narrow actual GPT query only; no rule changes.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_FULL_REVIEW_PREFLIGHT. Acquisition335 assembly4307checks exists; current reading preflight5382 passes. First reading report with sole stale-allowlist failure is preserved, fixed only in V2 under actual ACQ03 authority. Do not rerun these one-use tools.',
        'FEAT335-CADENCE-CHECK-01 is genuinely sent once and currently generating in Chrome3/tab125745532 Calibration Review Part2. Read its terminal reply when available. Issue: local unqualified once-per-turn mapping may have overgeneralized regular-turn cadence. Apply only source-supported narrow corrections with preserved before/after evidence; no full feat approval requested.',
        'Read FEAT335_FULL_EXACT_REVIEW_PREFLIGHT.json and actual finite FXC acceptance contract. Full exact packet is NOT ready yet. Complete remaining distinct FXC04/06–10 use/case/physical/copy/clock interfaces; do not treat335 acquisition completion or660 authored expectations as full runtime.',
        'Useful next independent slice: three Flora modes and paid second-body/command/Trapcasting lifecycle using already corrected actual provider acquisition; alternatively12 finite borrowed stunts. Preserve completed six maneuvers,four gadgets,animal lifecycle and exact curriculum/conditional acquisition evidence rather than rerunning unchanged suites.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':nav_report['existingDistinctLinks'],'missingLinks':nav_report['missingLinks']}))

if __name__=='__main__':main()
