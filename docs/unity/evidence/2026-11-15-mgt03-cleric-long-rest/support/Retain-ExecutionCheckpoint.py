"""Retain an explicitly incomplete original-run checkpoint for actual implementation review."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess

support = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('qualification_retention', support/'Retain-Qualification.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)

def main():
    parser=argparse.ArgumentParser()
    for name in ('qualification','regression','build','output'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    qualification,regression,build,output=[q.longpath(getattr(args,n)) for n in ('qualification','regression','build','output')]
    assert not subprocess.check_output(['git','diff',q.SOURCE,'--','engine'],cwd=q.ROOT).strip()
    source=q.passed(output/'SOURCE_AUDIT.json')
    assert source['implementationCommit']==q.SOURCE
    terminal=q.passed(qualification/'paths-terminal/results.json')
    manifest=q.read(qualification/'trace-terminal/manifest.json')
    modes={'ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay'}
    assert set(terminal['paths'])==modes
    for mode,details in terminal['paths'].items():
        for mark in manifest['marks']:
            assert q.digest(qualification/'paths-terminal'/mode/mark['name'])==mark['sha256']==details['checkpoints'][mark['name']]
            for view in mark['views'].values():
                assert q.digest(qualification/'paths-terminal'/mode/view['name'])==view['sha256']==details['checkpoints'][view['name']]
    before_root=qualification/'additional-campaigns'
    before_result=q.passed(before_root/'paths-before/results.json')
    before_manifest=q.read(before_root/'trace-before/manifest.json')
    assert set(before_result['paths'])==modes
    for mode,details in before_result['paths'].items():
        for mark in before_manifest['marks']:
            assert q.digest(before_root/'paths-before'/mode/mark['name'])==mark['sha256']==details['checkpoints'][mark['name']]
            for view in mark['views'].values():
                assert q.digest(before_root/'paths-before'/mode/view['name'])==view['sha256']==details['checkpoints'][view['name']]
    compatibility=q.passed(qualification/'compatibility/results.json')
    assert len(compatibility['Cases'])==25
    for name in ('parser','commands','branches','boundaries-corrected'):
        q.passed(qualification/name/'results.json')
    launch=q.read(regression/'launch.json');workers=q.read(regression/'processes.json')
    assert launch['sourceCommit']==q.SOURCE and launch['requiredCount']==1553
    checkpoint=output/'regression-checkpoint'
    assert not checkpoint.exists(), 'Never overwrite a retained checkpoint'
    checkpoint.mkdir(parents=True)
    for name in ('launch.json','processes.json','all-names.txt','compiled-source-report.json'):
        q.copy(regression/name,checkpoint/name)
    totals=[];names=[]
    for worker in workers:
        group=worker['group'];started=q.read(regression/(group+'.started.json'))
        assert started['runId']==launch['runId'] and started['pid']==worker['pid']
        assert started['assignmentSha256']==launch['assignments'][group]==q.digest(regression/(group+'-names.txt'))
        for name,expected in launch['assemblies'].items():assert started['assemblies'][name]['sha256']==expected
        # Capture journal bytes once. A truncated append cannot be promoted into a complete row.
        data=(regression/(group+'.jsonl')).read_bytes()
        assert data.endswith(b'\n'), group
        rows=[json.loads(line) for line in data.decode('utf-8-sig').splitlines()]
        assert all(row['Passed'] and not row['Error'] for row in rows)
        assert [r['Name'] for r in rows]==q.lines(regression/(group+'-names.txt'))[:len(rows)]
        names.extend(r['Name'] for r in rows)
        (checkpoint/(group+'.jsonl')).write_bytes(data)
        for suffix in ('.started.json','-names.txt'):q.copy(regression/(group+suffix),checkpoint/(group+suffix))
        totals.append({'group':group,'pid':worker['pid'],'passedPrefix':len(rows),'assigned':worker['cases'],
            'journalPrefixSha256':q.digest(checkpoint/(group+'.jsonl')),'completeClaimed':False})
    assert len(names)==len(set(names)) and all(name in names for name in q.NEW_CASES)
    assert len(names)<1553,'Use the final retainer for a completed run'
    for name in q.NEW_CASES:q.tree(regression/'saves'/name,output/'focused'/name)
    q.tree(build/'saves',output/'focused-development')
    q.copy(build/'results.json',output/'builds/focused/results.json')
    for kind in ('compile','static'):
        reports=list((q.ARTIFACTS/'development/view-correction'/kind).glob('*/results.json'))
        assert len(reports)==1;q.passed(reports[0]);q.copy(reports[0],output/'builds'/kind/'results.json')
    for name in ('trace-terminal','paths-terminal','parser','commands','branches','boundaries','boundaries-corrected','compatibility'):
        q.tree(qualification/name,output/'qualification'/name)
    for name in ('trace-before','paths-before'):
        q.tree(before_root/name,output/'qualification/additional-campaigns'/name)
    q.copy(qualification/'focused-parity.json',output/'qualification/focused-parity.json')
    # Preserve the concrete discrepancy, its source/binary identities and abandoned original workers.
    prior=q.longpath(q.ARTIFACTS/'qualification')
    for name in ('trace-terminal-20261116T0048Z','paths-terminal-20261116T0057Z'):
        q.tree(prior/name,output/'prior-attempts'/name)
    old=prior/'regression-20261116T0042Z'
    for path in old.iterdir():
        if path.is_file():q.copy(path,output/'prior-attempts/regression'/path.name)
    q.archive_dlls(old/'execution-assemblies',output/'prior-attempts/regression/execution-assemblies.zip')
    result={'status':'INCOMPLETE_EXECUTION_CHECKPOINT_FOR_ACTUAL_REVIEW','implementationCommit':q.SOURCE,
        'capturedUtc':datetime.now(timezone.utc).isoformat(),'runId':launch['runId'],'passedPrefix':len(names),'required':1553,'failed':0,
        'originalWorkers':totals,'terminalCampaign':{'commands':manifest['revision'],'checkpoints':len(manifest['marks']),
            'executionPaths':sorted(modes),'canonicalComparisons':5*len(manifest['marks']),'filteredViewComparisons':10*len(manifest['marks'])},
        'before24hCampaign':{'commands':before_manifest['revision'],'checkpoints':len(before_manifest['marks']),
            'executionPaths':sorted(modes),'canonicalComparisons':5*len(before_manifest['marks']),'filteredViewComparisons':10*len(before_manifest['marks'])},
        'authenticSaveContinuations':25,
        'remaining':['Finish all1553 cases on the same six original workers.','Finish remaining three five-path campaigns.',
            'Finish100 older console projections.','Reconcile final artifacts and obtain actual final acceptance.'],
        'actualFinalReview':'PENDING','successor':'NOT_AUTHORIZED','wholeEngineCompletion':'UNFINISHED','unity':'DEFERRED'}
    q.write(output/'EXECUTION_CHECKPOINT.json',result)
    index={}
    for path in sorted(output.rglob('*')):
        if path.is_file() and path.name not in ('ARTIFACT_INDEX.json','CHECKPOINT_ARTIFACT_INDEX.json'):
            index[path.relative_to(output).as_posix()]={'bytes':path.stat().st_size,'sha256':q.digest(path)}
    q.write(output/'CHECKPOINT_ARTIFACT_INDEX.json',{'artifacts':index})
    print(f'INCOMPLETE CHECKPOINT: {len(names)}/1553 passing original cases; {len(index)} retained artifacts; terminal five paths pass. Final acceptance remains pending.')

if __name__=='__main__':main()
