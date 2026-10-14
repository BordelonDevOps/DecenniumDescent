"""Register FW06 source-bound paid initial states with preserved navigation."""
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
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}


def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_SHARED_STATES.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT335_DEFERRED_STATES.json'
    register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_DEFERRED_STATES.json'
    delta=A/'FEAT335_DEFERRED_STATES_PROGRESS_DELTA.json'
    preserve=A/'navigation-before-feat335-deferred-states'
    assert all(not p.exists() for p in [target,register,delta,preserve])
    state=read(previous)
    report_path=A/'FEAT335_DEFERRED_ACQUISITION_STATE_CHECK.json'
    descriptor_path=A/'FEAT335_DEFERRED_ACQUISITION_DESCRIPTORS.json'
    operation=A/'FEAT335_CURSE_CAPACITY_DERIVED_OPERATIONS.json'
    report=read(report_path);descriptors=read(descriptor_path)
    assert report['checks']==301 and not report['failures'] and report['historyCount']==29 and report['exactDescriptorCount']==20
    for binding in report['sourceBindings']:assert info(G/binding['path'])==binding
    assert info(descriptor_path)==report['descriptors']
    corrected=read(operation)['changes'][0]
    before=info(G/corrected['before']['preservedCopy'])
    assert all(before[k]==corrected['before'][k] for k in ['bytes','sha256'])
    assert info(G/corrected['after']['path'])==corrected['after']
    old_bytes=(G/corrected['before']['preservedCopy']).read_bytes()
    assert old_bytes.count(corrected['guardedBefore'].encode())==1
    assert old_bytes.replace(corrected['guardedBefore'].encode(),corrected['guardedAfter'].encode(),1)==(G/corrected['after']['path']).read_bytes()
    previous_register=G/state['feat335CorrectionFulfillment']['currentRegister']['path']
    assert info(previous_register)==state['feat335CorrectionFulfillment']['currentRegister']
    current=read(previous_register)
    fw=next(g for g in current['remainingFiniteGroups'] if g['id']=='FW-06')
    entries={x['id']:(i,x) for i,x in enumerate(descriptors['entries'])}
    assert len(entries)==20 and set(entries)==set(fw['exactMembers'])
    current.update(recordedAtUtc=now,previousRegister=info(previous_register),
        status='Four audit findings and FW05/FW06 assembly complete in finite scopes. AA01-15 fulfilled; AA16-18/FW07-09 and full feat exact review pending.')
    current['fulfilledAcceptanceGroups']=['AA-'+str(i).zfill(2) for i in range(1,16)]
    current['remainingAcceptanceGroups']=['AA-'+str(i).zfill(2) for i in range(16,19)]
    current['fulfilledFiniteGroups']=['FW-'+str(i).zfill(2) for i in range(1,7)]
    current['remainingFiniteGroups']=[g for g in current['remainingFiniteGroups'] if g['id']!='FW-06']
    for row in current['rows']:
        row['fulfilledTargetedAcceptanceGroups']=[g for g in row['acceptanceGroups'] if int(g.split('-')[1])<=15]
        row['remainingAssemblyGroups']=[g for g in row['remainingAssemblyGroups'] if g!='FW-06']
        if row['id'] in entries:
            i,entry=entries[row['id']]
            assert entry['gptInitialStateDescriptor']==row['exactInitialStateDescriptor']
            row['deferredStateEvidence']={'descriptors':info(descriptor_path),'descriptorPointer':'/entries/'+str(i),
                'report':info(report_path),'paidHistoryPointer':entry['historyPointer'],'scope':report['scope']}
    current['deferredStateEvidence']={'descriptorFile':info(descriptor_path),'paidHistoryReport':info(report_path),'sourceHelperCorrection':info(operation)}
    scope=('All four FEAT335 audit findings and FW01–06 are fulfilled within their recorded finite scopes. '
        'The latest FW06 pass binds all20 exact delayed/empty/capacity descriptors to complete source procedures and paid prerequisite histories:301 checks across29 histories, no failures. '
        'Runic Shield is armed at acquisition and creates15 ward only at a later actual encounter premise; existing familiar capacity grows without healing, while genuine new-creation starting HP remains distinct. '
        'Resource growth does not refill, and acquisition does not rewrite HP, RP, existing Strain/debt/deadlines, conditions, bodies or events. '
        'Core Infusion uses actual paid Artisan Smith-tools and Wizard Initiate; Frenzied Rage uses actual paid Berserker, without claiming conditional external branches as campaign facts. '
        'Curse Channeling helper now uses current total level when spending an older saved opportunity, matching its unchanged source. '
        'AA01–15 are fulfilled; AA16–18/FW07–09 (fixed snapshots/recipients,177 ordinary finite descriptors, conditional/null preservation and final335 mechanism join) remain. '
        'Full feat exact review, final whole-game flow agreement and human balance remain open. Higher spells remain187 unadopted procedures/374 examples,201 pre-push questions and47 deferred receipts; ordinary totals412 reviewed/436 pending.')
    ledger_path=R/'data/playtest/game_development_coverage.json';nav=R/'tools/build_review_map.py'
    assert info(ledger_path)==state['coverageLedger']
    old_ledger=read(ledger_path);ledger=deepcopy(old_ledger)
    old_issue=('AA01–14/FW01–05 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_SHARED_STATES.json. '
        'Complete FW06–09/AA15–18: delayed/empty/capacity state, fixed snapshots and recipients,177 ordinary finite descriptors, conditional/null preservation and final335 descriptor/mechanism parity. Then submit the full assembled feat candidate for actual GPT exact review.')
    for row in ledger['aspects']:
        if row['id'] in {'DD-14','DD-69'}:
            assert row['openIssues'].count(old_issue)==1
            row['openIssues'][row['openIssues'].index(old_issue)]=('AA01–15/FW01–06 are fulfilled in FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_DEFERRED_STATES.json. '
                'Complete FW07–09/AA16–18: fixed snapshots and exact training recipients,177 ordinary finite descriptors, conditional/null preservation and final335 descriptor/mechanism parity. Then submit the full assembled feat candidate for actual GPT exact review.')
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [report_path,descriptor_path,operation,register])
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'FEAT335-FW06-deferred-state-assembly','recordedAtUtc':now,
                'fulfilledAcceptanceGroup':'AA-15','exactDescriptors':20,'checks':301,'histories':29,'sourceRulesChanged':False,'fullFeatCandidateApproved':False})
    for before,after in zip(old_ledger['aspects'],ledger['aspects']):
        assert all(before.get(k)==after.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if before['id'] not in {'DD-14','DD-69'}:assert before==after
    assert {k:v for k,v in old_ledger.items() if k!='aspects'}=={k:v for k,v in ledger.items() if k!='aspects'}
    text=nav.read_text(encoding='utf-8')
    old_chain=' + read(A / "FEAT335_SHARED_STATES_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(old_chain)==1
    text=text.replace(old_chain,old_chain.rstrip('\n')+''.join(' + read(A / '+json.dumps(p.name)+')["changes"]' for p in [operation,delta])+'\n')
    assert text.count(state['status'])==1
    text=text.replace(state['status'],scope,1)
    marker='    pending = [\n';assert text.count(marker)==1
    text=text.replace(marker,marker+''.join('        ('+json.dumps(label)+', '+json.dumps(p.name)+'),\n' for label,p in [
        ('Current335-row acquisition follow-through after deferred states',register),
        ('Twenty exact delayed or empty starting-state descriptors',descriptor_path),
        ('Paid starting-state and capacity verification —301 checks',report_path),
        ('Preserved Curse Channeling current-level helper correction',operation)]))
    compile(text,str(nav),'exec')
    save(register,current)
    preserved=[]
    for p in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        copy=preserve/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
        assert p.read_bytes()==copy.read_bytes()
        preserved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preserve/'PRESERVATION_MANIFEST.json',preserved)
    save(ledger_path,ledger);nav.write_text(text,encoding='utf-8',newline='\n')
    save(delta,{'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],
        'allOtherAspectsUnchanged':True,'allClosuresAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'newGameRules':0})
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout);print(run.stderr);raise SystemExit(run.returncode)
    map_report=read(A/'REVIEW_MAP_BUILD.json');assert not map_report['missingLinks']
    assert info(G/'REVIEW_MAP.html')['sha256']==map_report['sha256']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),
        featDeferredStateAssembly={'fulfilledFiniteGroup':'FW-06','fulfilledAcceptanceGroup':'AA-15','descriptorCount':20,
            'descriptorFile':info(descriptor_path),'evidence':info(report_path),'checks':301,'histories':29,
            'sourceHelperCorrection':info(operation),'scope':report['scope'],'fullFeatCandidateApproved':False},
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':map_report['existingDistinctLinks'],'missingLinks':[]},
        newRuleAdoptions=0,newRuleAdoptionCountScope='This checkpoint only: existing source initial-state and current-total-level rules. No new game rule or full exact/runtime approval.')
    state['feat335CorrectionFulfillment'].update(currentRegister=info(register),fulfilledAcceptanceGroups=current['fulfilledAcceptanceGroups'],remainingAcceptanceGroups=current['remainingAcceptanceGroups'])
    state['featAcquisitionAudit']['currentFollowthrough']=info(register)
    state['featAcquisitionAudit']['correctionScope']='Four findings and FW05/FW06 assembly fulfilled in finite scopes; AA16-18/FW07-09 remain'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Current checkpoint AFTER_FEAT335_DEFERRED_STATES records verified progress. AA01-15/FW01-06 are fulfilled within stated scopes. All prior evidence and before-bytes remain; do not rerun one-use builders or mutate historical reports.',
        'Next FW07/AA16: bind21 exact current-source vision/HP/variant/training descriptors to fixed-versus-live paid acquisition snapshots and recipient/duplicate branches. Reuse unchanged bound evidence; do not invent substitutes, reselect permanent choices or refill HP.',
        'FW08/AA18:177 ordinary finite descriptors require exact count/owner/recipient/shared-vs-separate/rest/round epoch joins to the common initial-use mechanism.111 no-new-state entries need no invented state. Final335 current source parity must be joined to mechanisms, not treated as full acquisition evidence alone.',
        'FW09/AA17: preserve two null unavailable payloads and ACQ04 conditional branches without new cosmology positives or missing/null reinterpretation.',
        'FW06 complete source procedures and20 descriptor records live in FEAT335_DEFERRED_ACQUISITION_DESCRIPTORS.json.301 checks/29 histories verify paid acquisition/no retrospective effects, Runic conditional later encounter/rest shape, familiar existing/new distinction, and banked Curse Channeling opportunity capacity at9/10/12.',
        'Only existing helper mutation this turn: Curse Channeling current total level, not spent-opportunity level. FEAT335_CURSE_CAPACITY_DERIVED_OPERATIONS.json preserves exact before/after and is in navigation binding chain. Earlier shared/provider reports remain historical executions with this recorded descendant, not rerun against it.',
        'DeferredAcquisitionStates is a finite initialization projection, not full combat/crafting/course/rest/event runtime. Conditional bodies/events are not actual campaign proof. Engineering and external rage alternatives retain their existing independent scopes.',
        'Actual GPT335 audit remains terminal; no pending response or generic resubmission. Finish bounded acquisition assembly then submit the full assembled feat candidate for actual GPT exact review.',
        *state['safeNextActions'][-2:]]
    save(target,state)
    print(json.dumps({'checkpoint':info(target),'navigationLinks':map_report['existingDistinctLinks'],'missingLinks':map_report['missingLinks']}))


if __name__=='__main__':main()
