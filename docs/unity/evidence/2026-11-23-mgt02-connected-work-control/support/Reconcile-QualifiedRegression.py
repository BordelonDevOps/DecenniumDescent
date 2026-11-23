"""Reconcile one explicitly reviewed rerun without relabelling the raw suite."""
from pathlib import Path
import hashlib
import json

repo = Path(__file__).resolve().parents[5]
packet = Path(__file__).resolve().parent.parent
art = repo / 'engine/artifacts/connected-work-control'
full = art / 'full-01'
build = art / 'development-10/run-20261123T200453593Z-83a83fc6'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

review = read(packet / 'GPT_SUPPLEMENT_04_REVIEW.json')
assert review['singleCaseReconciliationAccepted'] is True
assert review['responseId'] and review['response'] and review['codexConcurrence']
assert review['reviewedCommit'] == '9c88acd587e15ab96116aba71d4e512d2646bea5'
raw = read(full / 'REGRESSION_RECONCILIATION.json')
assert raw['status'] == 'FAIL' and raw['registered'] == raw['completed'] == 1601
assert raw['passed'] == 1600 and raw['failed'] == 1
assert raw['preservedPredecessorInventory'] == 1592 and not raw['missingPredecessors']
assert len(raw['newCases']) == 9
assert all(w['completed'] == w['assigned'] for w in raw['workers'])
case_name = 'mgt02_work_control_native_fill_record_and_booking_caps'
failures = [c for c in raw['cases'] if not c['passed']]
assert len(failures) == 1 and failures[0]['name'] == case_name
failed = failures[0]
assert failed['sha256'] == '77b10334a1ad32e39397677b0b945a363617d5f42b8abca25bd846ad3bcf6bdd'
assert digest(repo / failed['evidence']) == failed['sha256']
assert failed['error'].startswith('System.IO.IOException: Unable to remove the file to be replaced.')

exits = read(art / 'FINAL_PROCESS_EXITS.json')
assert {x['worker'] for x in exits['workers']} == {0, 1, 2, 3}
assert len(exits['workers']) == 4
session_ids = {0:80513, 1:49260, 2:5412, 3:27544}
for x in exits['workers']:
    i = x['worker']
    assert x['sessionId'] == session_ids[i]
    assert x['observedExitCode'] == (1 if i == 2 else 0)
    worker_file = full / ('worker' + str(i)) / 'results.json'
    worker = read(worker_file)
    assert worker['status'] == ('FAIL' if i == 2 else 'PASS')
    assert worker['completed'] == worker['assigned']
    assert x['artifactSha256'] == digest(worker_file)
    assert x['finishedUtc'] == worker['finishedUtc']

rerun_path = art / 'fill-cap-io-recheck-01/results.json'
rerun = read(rerun_path)
assert digest(rerun_path) == 'bce15efdb4c194e15b2e4d1a516c77419bbe81e612f9254300c3b0f268c5b627'
assert rerun['status'] == 'PASS' and rerun['assigned'] == rerun['completed'] == rerun['passed'] == 1
assert rerun['failed'] == 0 and len(rerun['cases']) == 1
assert rerun['cases'][0]['Name'] == case_name and rerun['cases'][0]['Passed']
assert rerun['sourceHashes'] == read(build / 'results.json')['sourceHashes']
assert {a['name']:a['sha256'] for a in rerun['assemblyHashes']} == raw['assemblyHashes']
observed = read(art / 'OBSERVED_PROCESS_EXITS.json')
rerun_exit = [x for x in observed['completed'] if x['name'] == 'fill-cap-isolated-recheck']
assert len(rerun_exit) == 1 and rerun_exit[0]['sessionId'] == 19693
assert rerun_exit[0]['observedExitCode'] == 0 and rerun_exit[0]['artifactSha256'] == digest(rerun_path)
triage_path = art / 'fill-cap-io-triage-01/result.json'
triage = read(triage_path)
assert digest(triage_path) == '79c70970f13e6cbcf94aa3a23d9b9f98289872836034c916a51b29017dd3f94c'
assert triage['status'] == 'PASS_BOUNDED_TRIAGE' and triage['sameFrozenAssemblies']
for row in triage['originalFiles']:
    original = full / 'worker2/cases' / case_name / row['file']
    restored = art / 'fill-cap-io-triage-01' / (row['file'] + '.restored')
    assert row['strictRestoreExact'] and digest(original) == digest(restored) == row['sha256']

cases = []
for c in raw['cases']:
    cases.append({**c, 'rawPassed':c['passed'],
        'reconciledPassed':True,
        'qualificationEvidence':rerun_path.relative_to(repo).as_posix() if c['name'] == case_name else c['evidence'],
        'qualificationEvidenceSha256':digest(rerun_path) if c['name'] == case_name else c['sha256'],
        'disposition':'ACTUAL_GPT_REVIEWED_SINGLE_CASE_RECHECK' if c['name'] == case_name else 'ORIGINAL_PASS'})
assert len(cases) == len({c['name'] for c in cases}) == 1601
result = {
    'status':'PASS_WITH_REVIEWED_SINGLE_CASE_RECHECK',
    'rawSuite':{'status':'FAIL','completed':1601,'passed':1600,'failed':1,
        'evidence':'full-01/REGRESSION_RECONCILIATION.json',
        'sha256':digest(full / 'REGRESSION_RECONCILIATION.json'), 'workers':raw['workers']},
    'reconciledUniqueCases':1601,'reconciledPassed':1601,'unresolvedCases':[],
    'preservedPredecessorInventory':1592,'newCases':raw['newCases'],
    'sourceBuild':raw['sourceBuild'],'assemblyHashes':raw['assemblyHashes'],
    'actualReviewResponseId':review['responseId'],
    'actualReviewSha256':digest(packet / 'GPT_SUPPLEMENT_04_REVIEW.json'),
    'processEvidenceSha256':digest(art / 'FINAL_PROCESS_EXITS.json'),
    'singleCaseDisposition':{'name':case_name,'originalFailure':failed,
        'isolatedResultSha256':digest(rerun_path),'isolatedObservedExitCode':0,
        'triageSha256':digest(triage_path),
        'limit':'Unknown Windows File.Replace failure cause. Raw failure and worker exit1 retained. No persistence fix, automatic retry, environmental-cause claim or broader crash-safety qualification.'},
    'cases':cases,'runtimeAccepted':False
}
(full / 'QUALIFIED_REGRESSION_RECONCILIATION.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
print('Raw suite FAIL:1600PASS/1FAIL; reviewed reconciliation covers1601 unique passing cases; original exit1 retained.')
