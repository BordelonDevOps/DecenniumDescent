"""Retain and reconcile completed qualification; never substitutes artifacts for execution."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
ARTIFACTS = ROOT/'engine/artifacts/mgt03-cleric-long-rest'
SOURCE = 'e0994929b444b15fc38957eb80cc34ab19d56db6'
NEW_CASES = ['mgt03_long_rest_genesis_and_unearned_denial',
             'mgt03_long_rest_genuine_first_funding_and_paid_continuation']

def longpath(path):
    value = str(path.resolve())
    return Path('\\\\?\\'+value) if os.name == 'nt' and not value.startswith('\\\\?\\') else Path(value)

def digest(path):
    return hashlib.sha256(longpath(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(longpath(path).read_text(encoding='utf-8-sig'))

def lines(path):
    return longpath(path).read_text(encoding='utf-8-sig').splitlines()

def write(path, value):
    path = longpath(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode())

def copy(source, destination):
    source, destination = longpath(source), longpath(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert digest(source) == digest(destination)

def tree(source, destination):
    source, destination = longpath(source), longpath(destination)
    for path in source.rglob('*'):
        if path.is_file() and path.suffix.lower() not in {'.dll','.pdb'}:
            copy(path, destination/path.relative_to(source))

def passed(path):
    result = read(path)
    assert result.get('status',result.get('Status')) == 'PASS', str(path)
    return result

def archive_dlls(directory, destination):
    directory, destination = longpath(directory), longpath(destination)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(directory.glob('*.dll')):
            item = zipfile.ZipInfo(path.name, date_time=(1980,1,1,0,0,0))
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, path.read_bytes())

def main():
    global ARTIFACTS
    ARTIFACTS = longpath(ARTIFACTS)
    parser = argparse.ArgumentParser()
    parser.add_argument('--qualification', type=Path, required=True)
    parser.add_argument('--regression', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    qualification, regression, build, output = [longpath(p) for p in
        (args.qualification,args.regression,args.build,args.output)]
    assert not subprocess.check_output(['git','diff',SOURCE,'--','engine'],cwd=ROOT).strip(), 'Frozen engine changed'
    assert read(output/'SOURCE_AUDIT.json')['implementationCommit'] == SOURCE
    launch = read(regression/'launch.json')
    assert launch['sourceCommit'] == SOURCE and launch['requiredCount'] == 1553
    assert launch['retainedPredecessors'] == 1551 and launch['sourceCommitted']
    inventory = lines(regression/'all-names.txt')
    assert len(inventory) == len(set(inventory)) == 1553
    old = lines(PACKET.parent/'2026-11-15-tac08-cleric-casting/implementation-amended/regression/all-names.txt')
    assert [n for n in inventory if n not in NEW_CASES] == old and len(old) == 1551
    assert digest(regression/'all-names.txt') == launch['inventorySha256']
    workers = read(regression/'processes.json')
    all_rows, completions = [], []
    for worker in workers:
        group = worker['group']
        started = read(regression/(group+'.started.json'))
        complete = read(regression/(group+'.execution.json'))
        assert lines(regression/(group+'.done')) == ['DONE']
        for record in (started,complete):
            assert record['runId'] == launch['runId'] and record['pid'] == worker['pid'] and record['group'] == group
            assert record['inventorySha256'] == launch['inventorySha256']
            assert record['assignmentSha256'] == launch['assignments'][group] == digest(regression/(group+'-names.txt'))
            for name, expected in launch['assemblies'].items():
                assert record['assemblies'][name]['sha256'] == expected == digest(regression/'execution-assemblies'/name)
                assert record['assemblies'][name]['moduleId'] == started['assemblies'][name]['moduleId']
        assert complete['startedUtc'] == started['startedUtc']
        assert datetime.fromisoformat(complete['completedUtc'].replace('Z','+00:00')) >= datetime.fromisoformat(started['startedUtc'].replace('Z','+00:00'))
        assert complete['journalSha256'] == digest(regression/(group+'.jsonl'))
        rows = [json.loads(line) for line in lines(regression/(group+'.jsonl'))]
        assert [r['Name'] for r in rows] == lines(regression/(group+'-names.txt'))
        assert len(rows) == worker['cases'] == complete['cases'] and all(r['Passed'] and not r['Error'] for r in rows)
        assert not (regression/(group+'.err')).read_bytes().strip(), group
        all_rows.extend(rows)
        completions.append(complete)
    assert len(workers) == 6 and len(all_rows) == 1553 and len({r['Name'] for r in all_rows}) == 1553
    assert {r['Name'] for r in all_rows} == set(inventory)
    prefix_report = output/'EXECUTION_CHECKPOINT.json'
    if prefix_report.exists():
        prefix = read(prefix_report)
        assert prefix['runId'] == launch['runId'] and prefix['implementationCommit'] == SOURCE
        for worker in prefix['originalWorkers']:
            group = worker['group']
            journal = output/'regression-checkpoint'/(group+'.jsonl')
            assert digest(journal) == worker['journalPrefixSha256']
            assert (regression/(group+'.jsonl')).read_bytes().startswith(journal.read_bytes())
        for name, metadata in read(output/'CHECKPOINT_ARTIFACT_INDEX.json')['artifacts'].items():
            retained = output/name
            assert retained.stat().st_size == metadata['bytes'] and digest(retained) == metadata['sha256'], name

    # Inspect every saved checkpoint and both public seats, rather than trusting only a PASS label.
    campaigns = [('terminal',qualification/'trace-terminal',qualification/'paths-terminal')]
    for name in ('before','after','whole','capped-debt'):
        campaigns.append((name,qualification/'additional-campaigns'/('trace-'+name),qualification/'additional-campaigns'/('paths-'+name)))
    passed(qualification/'additional-campaigns/results.json')
    campaign_results = []
    canonical_count = view_count = 0
    expected_modes = {'ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay'}
    for name, trace, paths in campaigns:
        manifest = read(trace/'manifest.json')
        result = passed(paths/'results.json')
        assert set(result['paths']) == expected_modes
        assert result['traceSha256'] == digest(trace/'inputs.jsonl')
        for mode, details in result['paths'].items():
            assert details['commands'] == manifest['revision']
            for mark in manifest['marks']:
                assert digest(trace/'reference'/mark['name']) == mark['sha256'] == digest(paths/mode/mark['name'])
                assert details['checkpoints'][mark['name']] == mark['sha256']
                canonical_count += 1
                for seat in ('Player','FirstOpponent'):
                    view = mark['views'][seat]
                    assert digest(trace/'reference'/view['name']) == view['sha256'] == digest(paths/mode/view['name'])
                    assert details['checkpoints'][view['name']] == view['sha256']
                    view_count += 1
        assert digest(Path(manifest['finalSource'])) == manifest['finalSha256']
        campaign_results.append({'name':name,'commands':manifest['revision'],'checkpoints':len(manifest['marks']),
            'paths':sorted(expected_modes),'finalSha256':manifest['finalSha256'],'resultSha256':digest(paths/'results.json')})
    genuine = regression/'saves'/NEW_CASES[1]
    # The original full run and separately compiled focused execution must agree at every principal checkpoint.
    agreeing = []
    for path in sorted((build/'saves').glob('long-rest-*.ddsave')):
        other = genuine/path.name
        assert other.exists() and digest(other) == digest(path), path.name
        agreeing.append({'name':path.name,'sha256':digest(path)})
    compatibility = passed(qualification/'compatibility/results.json')
    assert len(compatibility['Cases']) == 25
    for case in compatibility['Cases']:
        source = PACKET.parent/case['Source']
        earlier = PACKET.parent/case['Earlier']
        assert digest(source) == case['SourceSha256'] == case['RoundtripSha256'] == case['ContinuedSha256']
        assert digest(earlier) == case['EarlierSha256'] and case['Commands'] > 0
    legacy = passed(qualification/'legacy-projections/results.json')
    assert legacy['predecessorCommit'] == '0e5928bddd5abce47c16ff86172f5613423a2460'
    assert len(legacy['cases']) == 25 and sum(c['views'] for c in legacy['cases']) == 100
    for i, case in enumerate(legacy['cases']):
        folder = qualification/'legacy-projections'/f'case-{i}-wire{case["wire"]}'
        assert digest(folder/'old.jsonl') == case['oldOutputSha256']
        assert digest(folder/'new.jsonl') == case['newOutputSha256']
        old_views = [json.loads(line) for line in lines(folder/'old.jsonl')]
        new_views = [json.loads(line) for line in lines(folder/'new.jsonl')]
        assert len(old_views) == len(new_views) == 5
        assert old_views[2]['Response'] == new_views[2]['Response'] == 'Restored'
        assert all(old_views[j] == new_views[j] for j in (0,1,3,4))
    parser_result = passed(qualification/'parser/results.json')
    assert parser_result['rejected'] == 10 and parser_result['beforeSha256'] == parser_result['afterSha256']
    for name in ('commands','branches','boundaries-corrected'):
        passed(qualification/name/'results.json')
    unchanged = []
    for directory in ('commands','boundaries-corrected'):
        for before in sorted((qualification/directory).glob('*-before.ddsave')):
            after = before.with_name(before.name.replace('-before.ddsave','-after.ddsave'))
            assert digest(before) == digest(after)
            unchanged.append({'scope':directory,'before':before.name,'after':after.name,'sha256':digest(before)})

    # Retain originals byte-for-byte. Historical attempts never contribute to current pass counts.
    output.mkdir(parents=True,exist_ok=True)
    for path in regression.iterdir():
        if path.is_file(): copy(path,output/'regression'/path.name)
    for name in NEW_CASES: tree(regression/'saves'/name,output/'focused'/name)
    for directory in qualification.iterdir():
        if directory.is_dir() and directory != regression:
            tree(directory,output/'qualification'/directory.name)
        elif directory.is_file():
            copy(directory,output/'qualification'/directory.name)
    tree(build/'saves',output/'focused-development')
    copy(build/'results.json',output/'builds/focused/results.json')
    for category in ('compile','static'):
        root = ARTIFACTS/'development/view-correction'/category
        reports = list(root.glob('*/results.json'))
        assert len(reports) == 1
        passed(reports[0]);copy(reports[0],output/'builds'/category/'results.json')
    for path in (ARTIFACTS/'development').rglob('*'):
        if path.is_file() and (path.name == 'results.json' or path.suffix in {'.ps1','.py','.txt'}):
            copy(path,output/'development-reports'/path.relative_to(ARTIFACTS/'development'))
    old_run = ARTIFACTS/'qualification/regression-20261116T0042Z'
    abandoned = read(old_run/'abandoned.json')
    assert abandoned['status'] == 'ABANDONED_AFTER_EXTERNAL_QUALIFICATION_FAILURE'
    for worker in abandoned['workers']:
        assert digest(old_run/(worker['group']+'.jsonl')) == worker['journalSha256']
        assert len(lines(old_run/(worker['group']+'.jsonl'))) == worker['retainedLines']
    for path in old_run.iterdir():
        if path.is_file():copy(path,output/'prior-attempts/regression'/path.name)
    archive_dlls(old_run/'execution-assemblies',output/'prior-attempts/regression/execution-assemblies.zip')
    for directory in (ARTIFACTS/'qualification').iterdir():
        if directory.is_dir() and directory != old_run:
            tree(directory,output/'prior-attempts'/directory.name)
    write(output/'RESULTS.json',{
        'status':'EVIDENCE_READY_FOR_ACTUAL_FINAL_REVIEW','implementationCommit':SOURCE,
        'atUtc':datetime.now(timezone.utc).isoformat(),'contractApproval':'8588491a-0698-50ec-9830-b4ad4208d1ce',
        'fullRegression':{'runId':launch['runId'],'passed':1553,'required':1553,'failed':0,'predecessors':1551,
                          'newCases':NEW_CASES,'originalWorkers':completions},
        'campaigns':campaign_results,'canonicalCheckpointComparisons':canonical_count,'filteredViewComparisons':view_count,
        'fullRunFocusedCheckpointsAgree':agreeing,'authenticSaveContinuations':25,'legacyConsoleViews':100,
        'unchangedCommandPairs':unchanged,'parserOnlyRejected':10,
        'supplementaryControls':{'commands':'qualification/commands/results.json','boundaries':'qualification/boundaries-corrected/results.json',
            'wholeSplitAndCappedDebt':'qualification/branches/results.json',
            'detached':'Explicitly labeled actual policy interruption/admission/completion and numeric HD controls; no genuine positive HD recovery or external encounter is claimed.'},
        'limitations':['Earned Cleric2 only; no party rest or Cleric Short Rest consumption.',
            'No genuine positive HD spending/recovery, Conviction expenditure or positive Strain-point removal.',
            'Actual shortages block Strain recovery offers; Rest Debt removal classification remains unresolved.',
            'LR-HP-01 and the selected site/interruption profile are provisional consensus and TEST_ONLY.',
            'No inherited evidence exceptions or promotion into production authority.'],
        'priorRuns':{'originalRegression':abandoned,'failedView':'prior-attempts/paths-terminal-20261116T0057Z/results.json',
                     'supplementalCheckerFailure':'qualification/boundaries/results.json'},
        'actualFinalGptReview':'PENDING','unityIntegration':'DEFERRED','wholeEngineCompletion':'UNFINISHED'})
    index = {}
    for path in sorted(output.rglob('*')):
        if path.is_file() and path.name != 'ARTIFACT_INDEX.json':
            index[path.relative_to(output).as_posix()]={'bytes':path.stat().st_size,'sha256':digest(path)}
    write(output/'ARTIFACT_INDEX.json',{'artifacts':index})
    print(f'RETAINED: {len(index)} artifacts, {sum(x["bytes"] for x in index.values())} bytes; all1553 original cases; {canonical_count} canonical and {view_count} view comparisons.')

if __name__ == '__main__':
    main()
