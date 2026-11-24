"""Retain care initial-assessment evidence; not complete INT-05 acceptance."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
ARTIFACTS = ROOT / 'engine/artifacts/admitted-command-surface'
OUT = PACKET / 'runtime-checkpoint-06'

def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

run = ARTIFACTS / 'development-12'
build = run / 'run-20261124T042400305Z-c274652b'
care = run / 'care'
short = care / 'mgt03_connected_short_rest_deadlines_cadence_interruption_and_restore'
flesh = care / 'tac06_flesh_warden_connected_real_healing_and_rest_replacement'
decay = care / 'tac06_connected_consume_decay_depletion_healing_and_expiry'
wound = care / 'tac06_connected_wound_treatment_ordinary_supply_and_strain'
paths = {
    'candidate11-compile-failure.json': ARTIFACTS / 'development-11/run-20261124T042025603Z-311b5b4e/results.json',
    'candidate12-profile-denials.json': build / 'results.json',
    'candidate12-connected-care.json': care / 'results.json',
    'candidate12-package.json': run / 'static-20261124T042454070Z-02e2946e/results.json',
    'source-candidate12.zip': build / 'source-frozen.zip',
    'care-profile-denial-facts.json': build / 'saves/int05-care-profile-denials.json',
    'short-rest-independent-review.json': ARTIFACTS / 'short-rest-care-cross-review-01.json',
    'wound-decay-independent-review.json': ARTIFACTS / 'wound-decay-care-cross-review-01.json',
    'short-rest-pending.ddsave': short / 'short-rest-pending.ddsave',
    'short-rest-interrupted.ddsave': short / 'short-rest-interrupted.ddsave',
    'short-rest-completed.ddsave': short / 'short-rest-completed.ddsave',
    'mutation-pending.ddsave': flesh / 'flesh-connected-pending.ddsave',
    'mutation-continued.ddsave': flesh / 'flesh-connected-continued.ddsave',
    'decay-depleted.ddsave': decay / 'consume-decay-depleted.ddsave',
    'decay-expired.ddsave': decay / 'consume-decay-expired.ddsave',
    'treatment-active.ddsave': wound / 'wound-treatment-active.ddsave',
    'treatment-completed.ddsave': wound / 'wound-treatment-completed.ddsave',
    'treatment-interrupted.ddsave': wound / 'wound-treatment-interrupted.ddsave',
    'treatment-restarted.ddsave': wound / 'wound-treatment-restarted.ddsave',
}
compiled = load(paths['candidate12-profile-denials.json'])
assert compiled['status'] == 'PASS' and compiled['passed'] == 1 and compiled['testsDiscovered'] == 1
failed = load(paths['candidate11-compile-failure.json'])
assert failed['status'] == 'FAIL' and 'CS0128' in failed['error']
report = load(paths['candidate12-connected-care.json'])
assert report['status'] == 'PASS' and len(report['cases']) == 5 and all(c['Passed'] for c in report['cases'])
assert load(paths['candidate12-package.json'])['status'] == 'PASS'
with zipfile.ZipFile(paths['source-candidate12.zip']) as z:
    assert len(z.namelist()) == len(compiled['sourceHashes'])
    for row in compiled['sourceHashes']:
        assert sha(ROOT / 'engine' / row['path']) == row['sha256'], row['path']
        assert hashlib.sha256(z.read('engine/' + Path(row['path']).as_posix())).hexdigest() == row['sha256']
for name in ['short-rest-independent-review.json', 'wound-decay-independent-review.json']:
    review = load(paths[name])
    review_pins = review.get('currentSourcePins', review.get('reviewedSourcePins', []))
    review_pins += review.get('dependencyPins', []) + review.get('contractPins', [])
    review_pins += review.get('testSourceReview', {}).get('pins', [])
    assert review_pins
    for row in review_pins:
        assert sha(ROOT / row['path']) == row['sha256'], row['path']
OUT.mkdir(exist_ok=True)
pins = []
for name, source in paths.items():
    shutil.copyfile(source, OUT / name)
    pins.append({'path': (OUT / name).relative_to(ROOT).as_posix(),
                 'original': source.relative_to(ROOT).as_posix(), 'sha256': sha(source)})
previous = load(PACKET / 'IMPLEMENTATION_CHECKPOINT_05.json')
kinds = previous['currentNativeInitialAssessmentKinds'] + [
    'BeginShortRest', 'InterruptShortRest', 'BeginMutationShortRest', 'ConsumeDecay',
    'StartWoundTreatment', 'InterruptWoundTreatment']
summary = {
    'status': 'BOUNDED_CARE_INITIAL_ASSESSMENT_NOT_MODULE_ACCEPTANCE',
    'previousCheckpointCommit': '621c2821a85bbb3f32eb949cb5c094b27d3f673b',
    'contractAcceptance': '271baf94-22dd-57cb-a2ab-5f728e989b4d',
    'implemented': [
        'Six care commands share native initial constraints with actual execution; no candidate rest, treatment job, resource claim, temporary-HP choice or mutation application is created by assessment.',
        'Short-rest pending-choice checks remain before interruption. Mutation entitlement and cadence remain before active-rest/access checks. Wound interruption remains before fresh access and supply checks.',
        'Native future-overlap predicates retain worker-first short circuiting and lazy due-time arithmetic. Actual record construction stays at its original execution stage.',
        'ClassRecoveryUnsupported and active-short-rest interruption are shared at their original outer positions. No new capability or condition gate is imposed.',
        'Existing connected short-rest, mutation and wound scenarios now perform repeated pure assessments before their actual commands; assertions check all nine forbidden-call counters and unchanged canonical state.',
    ],
    'currentNativeInitialAssessmentKinds': kinds,
    'sourceInputs': len(compiled['sourceHashes']),
    'sourceArchiveSha256': sha(paths['source-candidate12.zip']),
    'dlls': [{'name': p.name, 'sha256': sha(p)} for p in sorted(build.glob('*.dll'))],
    'rawEvidence': pins,
    'actualExits': {'candidate11Compile': 1, 'candidate12CompileAndDenials': 0,
                    'fiveConnectedCareCases': 0, 'packageValidation': 0},
    'failureReconciliation': 'Candidate11 failed compilation because a new command local reused an existing snapshot local name. Only the command local was renamed. Original raw failure retained; no zero-case pass claimed.',
    'currentCandidateChecks': {'newInt05CasePassed': 1, 'existingNamedCasesPassed': 5, 'totalPassed': 6},
    'genuinePaths': [
        'Seven authentic factory-genesis denials match actual native execution and leave canonical state unchanged.',
        'Actual short rest retains occupancy, interruption, full-duration restart, two eligible benefits and third ineligible completion; temporary-HP expiry and split/whole clocks remain qualified by the existing scenario.',
        'Actual mutation rest changes capacity only on completion, preserves interruption, same-card behavior, authority, forgery rejection and continuation. Fixture entitlement remains TEST_ONLY, not acquired production authority.',
        'Consume Decay still pays its actual Action; temporary HP can deplete or expire before actual healing and continued play. Positive assessment is exercised by the short-rest arrival route.',
        'Actual treatment consumes finite supplies only on execution, follows the shared clock, completes or interrupts, starts a fresh treatment and preserves recovery, strain and strict restoration checks.',
    ],
    'limits': [
        'Fifteen native initial-assessment kinds do not complete78 seat/two operator coverage or public V1 APIs.',
        'CommitFeasibility remains null; no terminal validation, outcome, healing, recovery or capacity prediction is certified.',
        'Stabilization, remaining native families, public descriptions/costs/choices/results/diagnostics/console, planning proof and complete transitive/profile/branch/five-path/regression/privacy qualification remain open.',
        'Independent reviews are static only. Executed reports are separate. No previous accepted module qualification was restarted.',
        'Actual final GPT runtime acceptance remains open. No successor, Unity integration, storage cleanup or Support action.',
    ],
    'runtimeAccepted': False, 'successorStarted': False, 'unityIntegration': False,
}
(PACKET / 'IMPLEMENTATION_CHECKPOINT_06.json').write_bytes((json.dumps(summary, indent=2) + '\n').encode('utf8'))
print(json.dumps({'currentCandidatePassed': 6, 'compiledInputs': len(compiled['sourceHashes']),
                  'sourceArchiveSha256': summary['sourceArchiveSha256'], 'moduleAccepted': False}, indent=2))
