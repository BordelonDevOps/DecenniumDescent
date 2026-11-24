"""Retain stabilization assessment qualification; full INT-05 acceptance stays open."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]; ROOT = PACKET.parents[3]
ARTIFACTS = ROOT / 'engine/artifacts/admitted-command-surface'
OUT = PACKET / 'runtime-checkpoint-08'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

run = ARTIFACTS / 'development-14'
build = run / 'run-20261124T043756530Z-f269f0bd'
connected = run / 'stabilization'
medicine = connected / 'tac06_connected_companion_stabilization_paid_failure_and_absolute_recovery'
guidance = connected / 'tac08_genuine_guidance_medicine_stabilization'
paths = {
    'candidate14-profile-denials.json': build / 'results.json',
    'candidate14-connected.json': connected / 'results.json',
    'candidate14-package.json': run / 'static-20261124T043849323Z-aab9d5f6/results.json',
    'source-candidate14.zip': build / 'source-frozen.zip',
    'profile-denial-facts.json': build / 'saves/int05-stabilization-denials.json',
    'independent-review.json': ARTIFACTS / 'stabilization-cross-review-01.json',
    'medicine-failed-ready.ddsave': medicine / 'stabilization-failure-ready.ddsave',
    'medicine-failed-attempt.ddsave': medicine / 'stabilization-failure-attempt.ddsave',
    'medicine-success-ready.ddsave': medicine / 'stabilization-success-ready.ddsave',
    'medicine-success-attempt.ddsave': medicine / 'stabilization-success-attempt.ddsave',
    'guidance-before-medicine.ddsave': guidance / 'tac08-guidance-before-medicine.ddsave',
    'guidance-medicine.ddsave': guidance / 'tac08-guidance-medicine.ddsave',
}
compiled = load(paths['candidate14-profile-denials.json'])
assert compiled['status'] == 'PASS' and compiled['passed'] == 1 and compiled['testsDiscovered'] == 1
report = load(paths['candidate14-connected.json'])
assert report['status'] == 'PASS' and len(report['cases']) == 3 and all(c['Passed'] for c in report['cases'])
assert load(paths['candidate14-package.json'])['status'] == 'PASS'
with zipfile.ZipFile(paths['source-candidate14.zip']) as z:
    assert len(z.namelist()) == len(compiled['sourceHashes'])
    for row in compiled['sourceHashes']:
        assert sha(ROOT / 'engine' / row['path']) == row['sha256'], row['path']
        assert hashlib.sha256(z.read('engine/' + Path(row['path']).as_posix())).hexdigest() == row['sha256']
review = load(paths['independent-review.json']); assert review['sourcePins']
for row in review['sourcePins']: assert sha(ROOT / row['path']) == row['sha256'], row['path']
OUT.mkdir(exist_ok=True); pins = []
for name, source in paths.items():
    shutil.copyfile(source, OUT / name)
    pins.append({'path': (OUT / name).relative_to(ROOT).as_posix(),
                 'original': source.relative_to(ROOT).as_posix(), 'sha256': sha(source)})
previous = load(PACKET / 'IMPLEMENTATION_CHECKPOINT_07.json')
summary = {
    'status': 'BOUNDED_STABILIZATION_INITIAL_ASSESSMENT_NOT_MODULE_ACCEPTANCE',
    'previousCheckpointCommit': '5494e03af3a3d80a70ca07d7975f6324984b828b',
    'contractAcceptance': '271baf94-22dd-57cb-a2ab-5f728e989b4d',
    'implemented': [
        'StabilizeCompanion shares its original profile, payload, pending, turn, Action, capability, busy, hand, reach and dying-patient guards with execution.',
        'Seven existing search/hide/retreat/recovery/care/rest constraint helpers now return exact typed native origins behind unchanged legacy string wrappers.',
        'Sealed wound stock and occupied participants share their original outer guards. The stabilization assessment follows its exact position before reinforcement control and later charter/meal/route/advancement branches.',
        'Assessment consumes no Guidance, dice or Action, creates no attempt, and establishes no Stable deadline. Original actual execution remains the only producer.',
    ],
    'currentNativeInitialAssessmentKinds': previous['currentNativeInitialAssessmentKinds'] + ['StabilizeCompanion'],
    'sourceInputs': len(compiled['sourceHashes']), 'sourceArchiveSha256': sha(paths['source-candidate14.zip']),
    'dlls': [{'name': p.name, 'sha256': sha(p)} for p in sorted(build.glob('*.dll'))], 'rawEvidence': pins,
    'actualExits': {'compileAndProfileDenials': 0, 'threeSelectedCases': 0, 'packageValidation': 0},
    'currentCandidateChecks': {'newInt05CasePassed': 1, 'priorInt05CasePassed': 1, 'existingNamedCasesPassed': 2, 'totalPassed': 4},
    'genuinePaths': [
        'Three authentic factory denials retain exact profile/context and sealed-stock-before-stabilization ordering; actual rejected execution agrees and canonical state is unchanged.',
        'Actual failed Medicine spends one Action and its original d20 without life changes. Actual successful Medicine spends Action, d20 and recovery die, leaves zero HP and sets the exact two-hour Stable deadline; both attempts restore and retry without repeat payment.',
        'The actual previously cast Guidance remains present through pure assessment, then contributes its original d4 before the real Medicine d20. The consumed effect and causal check history restore exactly.',
        'Seven prior native care/profile denials remain passing after shared outer-guard extraction.',
    ],
    'limits': [
        'Eighteen native initial-assessment kinds do not complete78 seat/two operator coverage or public V1 APIs.',
        'This batch does not qualify every shared search/hide/rest profile, all stabilization/Guidance branches, or wider field/privacy contracts. Independent review is static only; actual execution reports are separate.',
        'CommitFeasibility remains null; no result, check, recovery or terminal-capacity prediction is certified.',
        'Remaining native families, public descriptions/costs/choices/results/diagnostics/console, planning proof and full transitive/branch/five-path/regression qualification remain open.',
        'Actual final GPT runtime acceptance remains open. No successor, Unity integration, storage cleanup or Support action.',
    ],
    'runtimeAccepted': False, 'successorStarted': False, 'unityIntegration': False,
}
(PACKET / 'IMPLEMENTATION_CHECKPOINT_08.json').write_bytes((json.dumps(summary, indent=2) + '\n').encode('utf8'))
print(json.dumps({'currentCandidatePassed': 4, 'compiledInputs': len(compiled['sourceHashes']),
                  'sourceArchiveSha256': summary['sourceArchiveSha256'], 'moduleAccepted': False}, indent=2))
