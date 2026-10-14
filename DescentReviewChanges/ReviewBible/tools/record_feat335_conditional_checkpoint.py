"""Preserve current navigation and register FW09/AA17 completion only."""
from copy import deepcopy
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def info(p):
    raw=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(raw),'sha256':sha256(raw).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FIXED_SNAPSHOTS.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_CONDITIONAL_PRESERVATION.json'
    register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CONDITIONAL_PRESERVATION.json'
    delta=A/'FEAT335_CONDITIONAL_PRESERVATION_PROGRESS_DELTA.json'
    preservation=A/'navigation-before-feat335-conditional-preservation'
    assert all(not p.exists() for p in [checkpoint,register,delta,preservation])
    state=read(previous);report_path=A/'FEAT335_CONDITIONAL_PRESERVATION_CHECK.json';report=read(report_path)
    assert report['checks']==587 and not report['failures'] and report['exactDescriptorCount']==6
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    old_register=G/state['feat335CorrectionFulfillment']['currentRegister']['path']
    assert info(old_register)==state['feat335CorrectionFulfillment']['currentRegister']
    current=read(old_register)
    fw=next(g for g in current['remainingFiniteGroups'] if g['id']=='FW-09')
    entries={x['id']:(i,x) for i,x in enumerate(report['entries'])}
    assert len(entries)==6 and set(entries)==set(fw['exactMembers'])
    current.update(recordedAtUtc=now,previousRegister=info(old_register),
        status='Four audit findings plus FW01-07 and FW09 fulfilled in finite scopes. Only FW08/AA18 allowance descriptor/mechanism assembly remains before full assembled feat exact review preparation.')
    current['fulfilledAcceptanceGroups']=['AA-'+str(i).zfill(2) for i in range(1,18)]
    current['remainingAcceptanceGroups']=['AA-18']
    current['fulfilledFiniteGroups']=['FW-'+str(i).zfill(2) for i in [1,2,3,4,5,6,7,9]]
    current['remainingFiniteGroups']=[g for g in current['remainingFiniteGroups'] if g['id']!='FW-09']
    for row in current['rows']:
        row['fulfilledTargetedAcceptanceGroups']=[g for g in row['acceptanceGroups'] if int(g.split('-')[1])<=17]
        row['remainingAssemblyGroups']=[g for g in row['remainingAssemblyGroups'] if g!='FW-09']
        if row['id'] in entries:
            i,entry=entries[row['id']];assert entry['preservedDisposition']==row['exactConditionalOrDeferredDescriptor']
            row['conditionalPreservationEvidence']={'report':info(report_path),'pointer':'/entries/'+str(i)}
    current['conditionalPreservationEvidence']=info(report_path)
    scope=('The four FEAT335 findings and FW01–07/FW09 are fulfilled in their finite scopes. FW07 binds21 fixed-snapshot/training records with555 checks/39 paid histories. '
        'FW09 now passes587 preservation checks: all six exact wrappers retain their complete sources; the two payloadOperational fields remain explicit null and unavailable; '
        'all263 ACQ04 fixture files and140 historical case records remain preserved. The138 external outcomes stay104 unestablished,13 contradicted and21 conditional-only, with no campaign credential promotion. '
        'No conditional Sorcerer/Dragonborn option was added to actual current class/ancestry catalogs. This is literal preservation, not cosmology review. '
        'AA01–17 are fulfilled; FW08/AA18 remains:177 ordinary finite allowance descriptors and the final335 descriptor/mechanism assembly. '
        'Full assembled feat exact review, final whole-game flow agreement and human balance remain open. Higher spells stay187 unadopted procedures/374 examples,201 pre-push questions and47 deferred receipts; ordinary totals412 reviewed/436 pending.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    old_issue=('AA01–16/FW01–07 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FIXED_SNAPSHOTS.json. '
        'Complete FW08–09/AA17–18:177 ordinary finite allowance count/owner/recipient/identity/rest-or-round descriptors, exact conditional/null preservation and final335 descriptor/mechanism parity. Then submit the full assembled feat candidate for actual GPT exact review.')
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            assert row['openIssues'].count(old_issue)==1
            row['openIssues'][row['openIssues'].index(old_issue)]=('AA01–17 and FW01–07/FW09 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CONDITIONAL_PRESERVATION.json. '
                'Complete FW08/AA18:177 ordinary finite allowance count/owner/recipient/identity/rest-or-round descriptors and final335 descriptor/mechanism assembly. Then submit the full assembled feat candidate for actual GPT exact review.')
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,register])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-FW09-conditional-preservation','recordedAtUtc':now,
                'fulfilledAcceptanceGroup':'AA-17','exactDescriptors':6,'checks':587,'campaignRecordsAuthenticated':0,'cosmologyReviewed':False,'fullFeatCandidateApproved':False})
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old_ledger.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');old_chain=' + read(A / "FEAT335_FIXED_SNAPSHOTS_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(old_chain)==1
    text=text.replace(old_chain,old_chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Current335 follow-through — only finite allowance assembly remains',register),
        ('Conditional and null preservation —587 checks',report_path)]))
    compile(text,str(nav),'exec');save(register,current);preserved=[]
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
        featConditionalPreservation={'fulfilledFiniteGroup':'FW-09','fulfilledAcceptanceGroup':'AA-17','descriptors':6,
            'evidence':info(report_path),'checks':587,'campaignRecordsAuthenticated':0,'cosmologyReviewed':False,'fullFeatCandidateApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':nav_report['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint: exact conditional/null source preservation only. No new rules or cosmology review.')
    state['feat335CorrectionFulfillment'].update(currentRegister=info(register),fulfilledAcceptanceGroups=current['fulfilledAcceptanceGroups'],remainingAcceptanceGroups=current['remainingAcceptanceGroups'])
    state['featAcquisitionAudit'].update(currentFollowthrough=info(register),correctionScope='Four findings and all finite groups except FW08/AA18 are fulfilled in named scopes.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Current authoritative checkpoint AFTER_FEAT335_CONDITIONAL_PRESERVATION records verified progress. AA01-17 and FW01-07/FW09 are fulfilled in finite scopes. Only FW08/AA18 remains before full assembled feat exact review preparation. Do not rerun one-use builders or overwrite historical reports.',
        'Next inspect all177 exact FW08 source procedures and count/owner/recipient/identity/rest/round obligations. Build structured finite descriptors joined to the existing FS06 common mechanism and each completed explicit exception.111 no-new-state rows need no invented scenarios; all335 current source/descriptor/mechanism parity still must be recorded.',
        'FW09 report587checks preserves all6current wrappers,263historical fixture files and138external outcomes plus2paid-history references.5false campaign-labelled fixture inputs remain rejected, not approved campaign records. Two payloadOperational fields are explicit null, not absent or false. Do not infer positive external facts or begin cosmology work.',
        'After FW08/AA18, assemble the full335 exact feat candidate and required source/worked-case/interface evidence for actual GPT exact review. Actual prior335 audit remains terminal; no pending reply or generic resend of the old packet.',
        'FW07 completed555checks/39fresh paid histories and21exact descriptor joins. Preserve original fixed darkvision branches, HP acquisition/live/event distinctions, exact training recipients and sourceGoblin variant task scopes. No new rule or full runtime claim.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':nav_report['existingDistinctLinks'],'missingLinks':nav_report['missingLinks']}))

if __name__=='__main__':main()
