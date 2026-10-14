"""Preserved FW07/AA16 descriptor/paid-history assembly checkpoint."""
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
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_DEFERRED_STATES.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_FIXED_SNAPSHOTS.json'
    register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FIXED_SNAPSHOTS.json'
    delta=A/'FEAT335_FIXED_SNAPSHOTS_PROGRESS_DELTA.json'
    preservation=A/'navigation-before-feat335-fixed-snapshots'
    assert all(not p.exists() for p in [checkpoint,register,delta,preservation])
    state=read(previous)
    report_path=A/'FEAT335_FIXED_SOURCE_SNAPSHOT_CHECK.json'
    descriptor_path=A/'FEAT335_FIXED_SOURCE_SNAPSHOT_DESCRIPTORS.json'
    report=read(report_path);descriptors=read(descriptor_path)
    assert report['checks']==555 and not report['failures'] and report['historyCount']==39 and report['exactDescriptorCount']==21
    assert info(descriptor_path)==report['descriptors']
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    old_register=G/state['feat335CorrectionFulfillment']['currentRegister']['path']
    assert info(old_register)==state['feat335CorrectionFulfillment']['currentRegister']
    current=read(old_register)
    expected=next(g for g in current['remainingFiniteGroups'] if g['id']=='FW-07')
    entries={x['id']:(i,x) for i,x in enumerate(descriptors['entries'])}
    assert len(entries)==21 and set(entries)==set(expected['exactMembers'])
    current.update(recordedAtUtc=now,previousRegister=info(old_register),
        status='Four audit findings and FW01-07 assembly fulfilled in stated finite scopes. AA01-16 fulfilled; FW08-09/AA17-18 and full assembled feat exact review pending.')
    current['fulfilledAcceptanceGroups']=['AA-'+str(i).zfill(2) for i in range(1,17)]
    current['remainingAcceptanceGroups']=['AA-17','AA-18']
    current['fulfilledFiniteGroups']=['FW-'+str(i).zfill(2) for i in range(1,8)]
    current['remainingFiniteGroups']=[g for g in current['remainingFiniteGroups'] if g['id']!='FW-07']
    for row in current['rows']:
        row['fulfilledTargetedAcceptanceGroups']=[g for g in row['acceptanceGroups'] if int(g.split('-')[1])<=16]
        row['remainingAssemblyGroups']=[g for g in row['remainingAssemblyGroups'] if g!='FW-07']
        if row['id'] in entries:
            i,entry=entries[row['id']]
            assert entry['gptInitialState']==row['exactInitialStateDescriptor']
            assert entry['gptMandatorySelectionsAndSnapshots']==row['exactMandatorySelectionAndSnapshotDescriptor']
            row['fixedSnapshotEvidence']={'descriptors':info(descriptor_path),'pointer':'/entries/'+str(i),
                'report':info(report_path),'freshPaidHistoryPointers':entry['freshPaidHistoryPointers'],'reusedPaidEvidence':entry['reusedPaidEvidence']}
    current['fixedSnapshotEvidence']={'descriptors':info(descriptor_path),'report':info(report_path)}
    scope=('All four FEAT335 findings and FW01–07 assembly groups are fulfilled in their finite scopes. '
        'Latest FW07/AA16 binds21 exact fixed-snapshot/training descriptors with555 checks across39 paid histories and reused source-bound Tavern Brawler/shared branch evidence. '
        'Tough keeps its actual acquisition-level snapshot, Tenacity stays live, and Tough as Nails preserves distinct level contributions through conditional loss/restoration without duplicate credit or healing. '
        'Darkvision modes remain fixed through underlying-source/suppression changes. Exact skill/tool recipients and duplicate branches are retained, with no replacement skill, free kit, extra trade progression or4PB stacking. '
        'Cultural Legacy binds actual Boom/Scrap/Shadow Goblin variants and only their defined rolled-task scopes; no new proficiency, lore or item is granted. '
        'AA01–16 are fulfilled; AA17–18/FW08–09 remain:177 ordinary finite allowance descriptors, conditional/null preservation and final335 mechanism/descriptor parity. '
        'Full assembled feat exact review, final whole-game flow agreement and human balance remain open. Higher spells stay187 unadopted procedures/374 examples,201 pre-push questions and47 deferred receipts; ordinary totals412 reviewed/436 pending.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    old_issue=('AA01–15/FW01–06 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_DEFERRED_STATES.json. '
        'Complete FW07–09/AA16–18: fixed snapshots and exact training recipients,177 ordinary finite descriptors, conditional/null preservation and final335 descriptor/mechanism parity. Then submit the full assembled feat candidate for actual GPT exact review.')
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            assert row['openIssues'].count(old_issue)==1
            row['openIssues'][row['openIssues'].index(old_issue)]=('AA01–16/FW01–07 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FIXED_SNAPSHOTS.json. '
                'Complete FW08–09/AA17–18:177 ordinary finite allowance count/owner/recipient/identity/rest-or-round descriptors, exact conditional/null preservation and final335 descriptor/mechanism parity. Then submit the full assembled feat candidate for actual GPT exact review.')
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,descriptor_path,register])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-FW07-fixed-snapshots','recordedAtUtc':now,
                'fulfilledAcceptanceGroup':'AA-16','exactDescriptors':21,'checks':555,'histories':39,'fullFeatCandidateApproved':False})
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in ledger.items() if k!='aspects'}=={k:v for k,v in old_ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    old_chain=' + read(A / "FEAT335_DEFERRED_STATES_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(old_chain)==1
    text=text.replace(old_chain,old_chain.rstrip('\n')+' + read(A / '+json.dumps(delta.name)+')["changes"]\n')
    assert text.count(state['status'])==1
    text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Current335 acquisition follow-through after fixed snapshots',register),
        ('Twenty-one exact fixed choice and training descriptors',descriptor_path),
        ('Paid fixed-snapshot and recipient evidence —555 checks',report_path)]))
    compile(text,str(nav),'exec')
    save(register,current)
    preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
        assert p.read_bytes()==copy.read_bytes()
        preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preservation/'PRESERVATION_MANIFEST.json',preserved)
    save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    nav_report=read(A/'REVIEW_MAP_BUILD.json');assert not nav_report['missingLinks']
    assert info(G/'REVIEW_MAP.html')['sha256']==nav_report['sha256']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        featFixedSnapshotAssembly={'fulfilledFiniteGroup':'FW-07','fulfilledAcceptanceGroup':'AA-16','descriptorCount':21,
            'descriptorFile':info(descriptor_path),'evidence':info(report_path),'checks':555,'histories':39,'scope':report['scope'],'fullFeatCandidateApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':nav_report['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint only: existing fixed training/snapshot and HP rules; no new mechanics or exact/runtime approval.')
    state['feat335CorrectionFulfillment'].update(currentRegister=info(register),fulfilledAcceptanceGroups=current['fulfilledAcceptanceGroups'],remainingAcceptanceGroups=current['remainingAcceptanceGroups'])
    state['featAcquisitionAudit']['currentFollowthrough']=info(register)
    state['featAcquisitionAudit']['correctionScope']='Four findings and FW05-07 assembly fulfilled in finite scopes; AA17-18/FW08-09 remain'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Current checkpoint AFTER_FEAT335_FIXED_SNAPSHOTS records verified progress. AA01-16/FW01-07 are fulfilled within named scopes. Source helpers written this turn are new; no existing gameplay/helper source was mutated. All prior reports remain immutable.',
        'Next FW08/AA18:177 exact ordinary finite allowance descriptors need count/formula, owner/recipient, shared-versus-separate identity and rest/round epoch bindings to the common initial-use mechanism. Reuse current immutable FS06 evidence and exceptions already completed;111 no-new-state rows require no invented fixtures.',
        'FW09/AA17: preserve two null unavailable spell wrappers and ACQ04 external branches with exact absence/null and conditional labels. No new pre-push positive cosmology/history requirement.',
        'Final all335 source/descriptor/mechanism assembly must include all completed finite groups and unchanged relevant evidence, but is not full runtime or human balance approval. Submit the entire assembled feat candidate for actual GPT exact review after assembly.',
        'FW07 descriptors bind21 IDs.555 checks/39 fresh paid histories plus retained Tavern Brawler/shared branch evidence verify fixed versus live HP, nonduplicated conditional restored-level events, actual60/120/no-darkvision sources, exact tool/skill recipients, and all3Goblin variants. Conditional loss/suppression/later-source and advanced Herbalism progression probes are not actual campaign events.',
        'The new darkvision parser explicitly reads both actual source forms: dim light within N feet, and Shadow Goblin darkvision has a radius of120 feet. No source wording or independent-range stacking rule changed.',
        'Actual GPT335 audit remains terminal; no pending response or generic resubmission. Prior corrections and exact source decisions remain controlling.',
        *state['safeNextActions'][-2:]]
    save(checkpoint,state)
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':nav_report['existingDistinctLinks'],'missingLinks':nav_report['missingLinks']}))


if __name__=='__main__':main()
