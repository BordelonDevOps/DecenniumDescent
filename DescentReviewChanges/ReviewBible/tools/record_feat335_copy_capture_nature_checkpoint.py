"""Register paid copy capture and the propagated actual Nature source decision."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, subprocess, sys
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_COPY_SOURCES.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_COPY_CAPTURE_AND_NATURE_SOURCE.json'
    delta=A/'FEAT335_COPY_CAPTURE_NATURE_PROGRESS_DELTA.json';preservation=A/'navigation-before-feat335-copy-capture-nature'
    report_path=A/'FEAT335_COPY_CAPTURE_CHECK.json';qualification=A/'FEAT335_COPY_CAPTURE_SCOPE.json'
    assert all(not p.exists() for p in [checkpoint,delta,preservation,qualification]);now=datetime.now(timezone.utc).isoformat()
    report=read(report_path);assert report['checks']==189 and not report['failures'] and len(report['histories'])==31
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    nature_report=A/'FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json'
    nature_record=A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json'
    nature_repro=A/'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json'
    nature_expect=A/'feat335-nature-source-check-01-verdict/FINITE_NATURE_EXPECTATIONS.json'
    assert read(nature_report)['checks']==137 and read(nature_repro)['checks']==124
    save(qualification,{'report':info(report_path),'scope':report['scope'],'remainingLimits':report['limits'],
        'newRules':0,'fullFeatExactApproved':False,'runtimeApproved':False,'cosmologyReviewed':False})
    state=read(previous)
    scope=('Paid Echo/Mimicry/Arcane Adaptation capture has189 passing checks across31 conditional source-qualified histories, building on248 seven-profile source checks. '
        'Actual paid class opportunities, Wizard or explicit feat-only rank0 providers, perception/geometry/Reaction gates, one pending record, paid replacement, genuine rest identities and regular-versus-extra-turn deadlines are executed in their finite scopes. '
        'Full paid release, recipient payloads, broader providers and world/scheduler authority remain unfinished. '
        'Actual GPT FEAT335-NATURE-SOURCE-CHECK-01 is terminal and received. Its124 source checks reproduce;137 local propagation/preservation checks apply3 guarded operations plus3 current mirrors while preserving all earlier source snapshots. '
        'Nature is explicitly a1RP magical nonspell technique without inherent components; fixed investigation terrain and resolution-based60-second rider, own paid check and nonspell Ready are now authored. '
        'The16 NWT groups/47 variants remain required local behavior follow-through; the historical362 suite remains partial evidence. '
        'Full335 and whole-game approval remain open. Actual final joint flow agreement precedes GitHub delivery, remote verification and careful cosmology. Stop at50percent weekly usage remains controlling.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old=read(ledger_path);ledger=deepcopy(old)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-14','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,qualification,nature_report,nature_record,nature_repro,nature_expect])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-copy-capture-and-Nature-source','recordedAtUtc':now,'checks':189,'conditionalHistories':31,'natureSourceChecks':137,'fullUseRuntimeApproved':False})
    for before,after in zip(old['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-09','DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');chain=' + read(A / "FEAT335_COPY_SOURCES_PROGRESS_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "FEAT335_NATURE_DERIVED_OPERATIONS.json")["changes"] + read(A / "FEAT335_COPY_CAPTURE_NATURE_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.relative_to(A).as_posix())+'),\n' for label,p in [
        ('Paid copy capture —189 checks,31 histories',report_path),('Copy capture —scope and pending paid release',qualification),('Nature source propagation —137 preservation checks',nature_report),('Nature controlling addendum and exact descendants',nature_record),('Nature reviewer checks —124 reproduced',nature_repro),('Nature16 behavior groups —authored expectations pending execution',nature_expect)]))
    compile(text,str(nav),'exec');preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy);assert copy.read_bytes()==p.read_bytes()
        preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved);save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':'Actual GPT Nature completion adopted; see controlling record,3 direct guarded field/paragraph operations.'})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        copyCaptures={'report':info(report_path),'scope':info(qualification),'checks':189,'conditionalHistories':31,'fullUseRuntimeApproved':False},
        natureSourceApplication={'controllingRecord':info(nature_record),'propagation':info(nature_report),'reproduction':info(nature_repro),'pendingExpectations':info(nature_expect),'finiteBehaviorFulfilled':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=3,newRuleAdoptionCountScope='Count is3 actual GPT direct guarded field/paragraph operations, plus3 current mirror propagations; semantic Nature decisions are separately recorded in the controlling addendum.')
    state.setdefault('priorCompletedGptObservations',[]).append({'supersededObservation':deepcopy(state['activeGptReview']),'receivedReview':info(nature_record)})
    state['activeGptReview'].update(status='terminal-received-source-propagated-finite-behavior-pending',pendingResponse=False,replyReceived=True,lastObservedStopVisible=False,
        responseDom=info(A/'FEAT335_NATURE_SOURCE_CHECK_01_RESPONSE_DOM.txt'),controllingRecord=info(nature_record),
        instruction='No unanswered GPT request. Do not resend Nature: exact propagation is complete; implement16 NWT groups/47 variants to fulfill the four source interfaces. Then send next genuinely prepared scoped review as appropriate.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_FEAT335_COPY_CAPTURE_AND_NATURE_SOURCE. Copy source248/35 and paid capture189/31 are distinct finite scopes. Next: full paid release and recipient payloads; no completion inferred from capture.',
        'Actual GPT Nature response is terminal. Archive194878 SHA888a7319acc2556d1ec1736cac4c78a4354e2fed574007f7d1bf376b096a2960 received and18 manifest payloads verified.124 reviewer checks reproduce;137 source propagation checks pass.',
        'Implement Nature NWR01–03 records and all16 NWT groups/47 variants in a measured descendant of borrowed skill transactions, preserving old362/38 evidence. Native and borrowed source now use exact nonspell/fixed-area/rider/Ready rules; do not rely on old actualMinorWeaveClearance.',
        *state['safeNextActions'][-2:]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    save(checkpoint,state);print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[]}))


if __name__=='__main__':main()
