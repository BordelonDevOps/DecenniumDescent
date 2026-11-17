"""Retain genuine Invocation epoch transfer and creature knockout/life boundaries."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
PACKET=HERE.parent
ART=ROOT/'engine/artifacts/ferry-wraith/dash-correction'
BUILD=ART/'run-20261117T110451175Z-06a69ef8'
OUT=PACKET/'lifecycle-checkpoint'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    assert not OUT.exists(), 'Never overwrite retained evidence.'
    members,reports={},{}
    specs=[('failed-epoch','invocation-epoch-20261117T1320Z','Probe-FerryInvocationEpoch.ps1','0b9ebd367'),
           ('epoch','invocation-epoch-20261117T1331Z','Probe-FerryInvocationEpoch.ps1','fb8c7bf01'),
           ('creature','creature-knockout-20261117T1331Z','Probe-FerryCreatureKnockout.ps1','fb8c7bf01')]
    compile_report=read(BUILD/'results.json')
    assert compile_report['status']==compile_report['coreCompilation']=='PASS' and len(compile_report['sourceHashes'])==468
    for row in compile_report['sourceHashes']:
        assert sha((ROOT/'engine'/row['path'].replace('\\','/')).read_bytes())==row['sha256']
    for label,name,script,commit in specs:
        folder=ART/name;report=read(folder/'RESULT.json');reports[label]=report
        executed=folder/(script[:-4]+'.executed.ps1')
        raw=subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+(HERE/script).relative_to(ROOT).as_posix()])
        assert raw==executed.read_bytes() and sha(raw)==report['script']['sha256']
        for row in report['assemblies']:
            assert row['sha256']==sha((BUILD/('Decennium.Foundation.'+row['name']+'.dll')).read_bytes())
        for pair in report['restorePairs']:
            original=folder/(pair['name']+'.ddsave');restored=folder/(pair['name']+'-restored.ddsave')
            assert original.read_bytes()==restored.read_bytes() and sha(original.read_bytes())==pair['sha256']
        for path in sorted(folder.iterdir()):
            assert path.is_file()
            members[label+'/'+path.name]=path.read_bytes()
    failed,epoch,creature=reports['failed-epoch'],reports['epoch'],reports['creature']
    assert failed['status']=='FAIL' and failed['failedRevision']==347
    assert 'did not transfer to the exact new epoch' in failed['error']
    assert epoch['status']=='PASS_GENUINE_INVOCATION_EPOCH_TRANSFER'
    assert len(epoch['commands'])==len(epoch['expandedCommands'])==20 and len(epoch['restorePairs'])==7
    assert [r['receipt']['Revision'] for r in epoch['expandedCommands']]==list(range(346,366))
    assert epoch['paidRecharge']['Remaining']==3 and epoch['paidRecharge']['EpochId']=='TEST_ONLY.post-recovery-calendar'
    observations=epoch['observations']
    assert len(observations)==19
    first,last=observations[0],observations[-1]
    assert first['actualOwnerStarts']==0 and first['ownerStart']==-1 and first['recharge']['Remaining']==3
    assert first['recharge']['EpochId']=='TEST_ONLY.post-recovery-calendar'
    starts={r['ownerStart']:r['recharge']['Remaining'] for r in observations if r['ownerStart']>=0}
    assert starts=={1:2,4:1,7:0} and last['actualOwnerStarts']==3
    assert all(r['recharge']['Remaining']==max(0,3-r['actualOwnerStarts']) for r in observations)
    assert creature['status']=='PASS_GENUINE_CREATURE_KNOCKOUT_AND_MECHANICAL_RECOVERY'
    assert len(creature['commands'])==72 and len(creature['restorePairs'])==3
    assert [r['response']['Revision'] for r in creature['commands']]==list(range(367,439))
    life=creature['knockedLife']
    assert life['Hp']==0 and life['Stable'] and not life['Dead'] and not life['UsesDeathSaves']
    assert creature['attack']['Instruction']=='KnockOutIfEligible' and creature['attack']['Damage']['StableD4']==1
    assert creature['deniedClosure']['Response']=='Unavailable' and creature['exactRetry']['Response']=='Duplicate'
    controls=creature['mechanicalRecovery'];assert [c['boundary'] for c in controls]==['before','at','after']
    for row in controls:
        assert row['detachedOnly'] and row['rngBefore']==row['rngAfter'] and not row['life']['Dead'] and not row['life']['UsesDeathSaves']
        assert row['life']['Hp']==(0 if row['boundary']=='before' else 1)
        assert len(row['newEvents'])==(0 if row['boundary']=='before' else 1)
    folder=ART/'creature-knockout-20261117T1331Z'
    assert (folder/'actual-stable-next-start.ddsave').read_bytes()==(folder/'live-after-mechanical-controls.ddsave').read_bytes()
    members['support/Retain-FerryLifecycle.py']=Path(__file__).read_bytes()
    members['references/dash-regression-RETENTION.json']=(PACKET/'dash-regression-checkpoint/RETENTION.json').read_bytes()
    rows=[dict(path=name,bytes=len(raw),sha256=sha(raw)) for name,raw in sorted(members.items())]
    OUT.mkdir();output=OUT/'lifecycle.zip'
    with zipfile.ZipFile(output,'x') as archive:
        for name,raw in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            archive.writestr(info,raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist()==[r['path'] for r in rows]
        for row in rows:
            raw=archive.read(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    summary=dict(status='PASS_BOUNDED_EPOCH_AND_CREATURE_LIFE_NOT_MODULE_ACCEPTANCE',runtimeCommit='c8ffee78d5047131317ff923c8e3a575b6c51f3a',
                 sourceInputs=468,epochCommands=20,epochObservations=19,actualNewOwnerStarts=[1,4,7],remainingRecharge=[2,1,0],
                 creatureCommands=72,creatureReplayedPrefixCommands=70,creatureNewCommands=2,strictRestorePairs=10,
                 detachedRecoveryControls=3,failedDriverAttempts=1,members=len(rows),archiveBytes=output.stat().st_size,
                 archiveSha256=sha(output.read_bytes()),collectorSha256=sha(Path(__file__).read_bytes()),moduleAccepted=False,
                 limits='Creature Stable recovery uses the actual shared RecoverDue helper on detached copies at the lawful knockout deadline; these are mechanical life controls, not a two-hour gameplay continuation. The live session stays at its genuine next creature Start. Initial epoch failure was a wrong driver assertion: recharge history relabels only on the actual owner Start, not admission. No C# change.')
    (OUT/'MEMBERS.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    (OUT/'RETENTION.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
