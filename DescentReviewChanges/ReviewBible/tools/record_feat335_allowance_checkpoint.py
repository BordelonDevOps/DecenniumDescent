"""One-use, source-preserving navigation/ledger registration of FW08/AA18."""
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
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_CONDITIONAL_PRESERVATION.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_ACQUISITION_ASSEMBLY.json'
    register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_COMPLETE.json'
    delta=A/'FEAT335_ALLOWANCE_ASSEMBLY_PROGRESS_DELTA.json'
    preservation=A/'navigation-before-feat335-allowance-assembly'
    assert all(not p.exists() for p in [checkpoint,register,delta,preservation])
    state=read(previous);report_path=A/'FEAT335_ALLOWANCE_ASSEMBLY_CHECK.json';report=read(report_path)
    descriptor=A/'FEAT335_ALLOWANCE_DESCRIPTORS.json';assembly=A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY.json'
    assert report['checks']==4307 and not report['failures'] and info(assembly)==report['assembly']
    for b in report['sourceBindings']:assert info(G/b['path'])==b
    old_register=G/state['feat335CorrectionFulfillment']['currentRegister']['path']
    assert info(old_register)==state['feat335CorrectionFulfillment']['currentRegister']
    current=read(old_register);joined=read(assembly)['entries'];descriptors=read(descriptor)['entries']
    assert len(joined)==335 and len(descriptors)==177
    index={x['id']:n for n,x in enumerate(joined)};dindex={x['id']:n for n,x in enumerate(descriptors)}
    current.update(recordedAtUtc=now,previousRegister=info(old_register),
        status='All four audit findings, FW01–09 and AA01–18 fulfilled in finite acquisition/initial-state source and evidence assembly. Full assembled335 feat exact review remains pending.',
        fulfilledAcceptanceGroups=['AA-'+str(i).zfill(2) for i in range(1,19)],remainingAcceptanceGroups=[],
        fulfilledFiniteGroups=['FW-'+str(i).zfill(2) for i in range(1,10)],remainingFiniteGroups=[],
        fullAcquisitionAssemblyComplete=True,all335FullAcquisitionsExecuted=False,
        allowanceAssemblyEvidence={'descriptors':info(descriptor),'assembly':info(assembly),'report':info(report_path)})
    for row in current['rows']:
        sid=row['id'];row['fulfilledTargetedAcceptanceGroups']=deepcopy(row['acceptanceGroups']);row['remainingAssemblyGroups']=[]
        row['completeAcquisitionAssemblyEvidence']={'assembly':info(assembly),'pointer':'/entries/'+str(index[sid]),'report':info(report_path)}
        if sid in dindex:row['ordinaryAllowanceEvidence']={'descriptors':info(descriptor),'pointer':'/entries/'+str(dindex[sid])}
        row['descriptorBindingScope']='Current full wrapper/source/menu/raw-field and exact reviewed acquisition/initial-state descriptor joined to all requested finite evidence. No assertion of335 freshly executed full acquisitions, full-use runtime or exact feat approval.'
    scope=('The FEAT335 acquisition audit follow-through is assembled: all four findings, FW01–09 and AA01–18 are fulfilled in their finite scopes. '
        'The new4307-check assembly joins all335 complete current source wrappers and exact acquisition descriptors to the preserved evidence. '
        'FW08 contains177 entries:111 no-new-consumable/active-effect entries plus66 specific initial-state entries, including60 feats with62 finite allowances and38 entries with explicit cadence identities. '
        'Rest owner/type, elapsed24-hour construction, actual encounter reentry, shared recipient/round and separate trap-type boundaries are bound; shared FS06 evidence is reused without rerunning historical suites. '
        'Full335 feat exact review by actual GPT is next; runtime, human balance and final whole-game flow approval remain open. '
        'Higher spells stay187 unadopted procedures/374 examples,201 pre-push questions and47 deferred receipts; ordinary totals412 reviewed/436 pending. No source deletion, GitHub push or cosmology review occurred.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger'];old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    old_issue=('AA01–17 and FW01–07/FW09 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CONDITIONAL_PRESERVATION.json. '
        'Complete FW08/AA18:177 ordinary finite allowance count/owner/recipient/identity/rest-or-round descriptors and final335 descriptor/mechanism assembly. Then submit the full assembled feat candidate for actual GPT exact review.')
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            assert row['openIssues'].count(old_issue)==1
            row['openIssues'][row['openIssues'].index(old_issue)]=('All AA01–18/FW01–09 acquisition-audit groups are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_COMPLETE.json. '
                'Prepare and submit the full335 exact feat candidate with complete source, worked-case and interface evidence to actual GPT. Full feat approval and complete-use runtime remain open.')
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [descriptor,assembly,report_path,register])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-FW08-AA18-assembly','recordedAtUtc':now,
                'checks':4307,'joinedRecords':335,'ordinaryDescriptorCount':177,'newPaidAcquisitionsExecuted':0,
                'fullAcquisitionAssemblyComplete':True,'fullFeatCandidateApproved':False,'cosmologyReviewed':False})
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old_ledger.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8');old_chain=' + read(A / "FEAT335_CONDITIONAL_PRESERVATION_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(old_chain)==1
    text=text.replace(old_chain,old_chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1;text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Current335 acquisition audit follow-through — all finite groups assembled',register),
        ('All335 complete acquisition source and evidence assembly',assembly),
        ('177 allowance descriptors —111 plain plus66 specific',descriptor),
        ('Allowance and final335 assembly check —4307 checks',report_path)]))
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
        featAllowanceAssembly={'fulfilledFiniteGroup':'FW-08','fulfilledAcceptanceGroup':'AA-18',
            'evidence':info(report_path),'assembly':info(assembly),'descriptors':info(descriptor),'checks':4307,
            'fullAcquisitionAssemblyComplete':True,'all335FullAcquisitionsExecuted':False,'fullFeatCandidateApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':nav_report['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint: finite acquisition descriptor/mechanism/source assembly only; no new rules or cosmology review.')
    state['feat335CorrectionFulfillment'].update(currentRegister=info(register),fulfilledAcceptanceGroups=current['fulfilledAcceptanceGroups'],
        remainingAcceptanceGroups=[],fullAcquisitionAssemblyComplete=True,all335FullAcquisitionsExecuted=False)
    state['featAcquisitionAudit'].update(currentFollowthrough=info(register),correctionScope='Four findings and all nine finite work groups are fulfilled in named scopes; full exact review remains pending.')
    state['safeNextActions']=[state['safeNextActions'][0],
        'Current authoritative checkpoint AFTER_FEAT335_ACQUISITION_ASSEMBLY records all AA01–18/FW01–09 fulfilled in finite scopes. Do not rerun one-use builders or overwrite historical reports.',
        'Next prepare the full335 exact feat candidate for actual GPT in Calibration Review Part2. Include full current cards, all eight reviewed records, full supplements/menus, source and correction receipts, acquisition assembly and preserved worked-case/interface evidence. Check the earlier full exact-review requirements before packaging; the terminal old acquisition audit is not a pending reply or a substitute for this review.',
        'New assembly4307 checks joins335 records.177 FW08 entries include111 plain and66 specific;60 feats supply62 finite allowances,38 entries have explicit cadence keys. New traces are conditional mechanism/identity boundaries, not actual campaign credentials or full feat-use simulations.',
        'Preserve all historical reports, raw null/absence and conditional external-credential limits. Full game/runtime/human balance and exact feat approval remain open. Do not begin cosmology review.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':nav_report['existingDistinctLinks'],'missingLinks':nav_report['missingLinks']}))

if __name__=='__main__':main()
