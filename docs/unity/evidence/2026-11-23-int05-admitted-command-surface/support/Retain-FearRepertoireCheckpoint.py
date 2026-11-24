"""Retain fear and repertoire initial-assessment evidence, not module acceptance."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
ARTIFACTS = ROOT / 'engine/artifacts/admitted-command-surface'
OUT = PACKET / 'runtime-checkpoint-07'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

run = ARTIFACTS / 'development-13'
build = run / 'run-20261124T043128261Z-31b6ec64'
connected = run / 'fear-repertoire'
fear = connected / 'tac05_frightened_connected_activation_restore_and_recharge'
paths = {
    'candidate13-profile-denials.json': build / 'results.json',
    'candidate13-connected.json': connected / 'results.json',
    'candidate13-package.json': run / 'static-20261124T043221638Z-d4a78435/results.json',
    'source-candidate13.zip': build / 'source-frozen.zip',
    'profile-denial-facts.json': build / 'saves/int05-fear-repertoire-denials.json',
    'independent-review.json': ARTIFACTS / 'fear-repertoire-cross-review-01.json',
    'fear-after-use.ddsave': fear / 'frightened-after-use.ddsave',
    'fear-active.ddsave': fear / 'frightened-active.ddsave',
    'fear-after-recharge.ddsave': fear / 'frightened-after-recharge.ddsave',
    'fear-continued.ddsave': fear / 'frightened-continued.ddsave',
    'repertoire-paid.ddsave': connected / 'tac07_cleric_repertoire_connected_payment_restore_and_denials/repertoire-paid.ddsave',
}
compiled = load(paths['candidate13-profile-denials.json'])
assert compiled['status'] == 'PASS' and compiled['passed'] == 1 and compiled['testsDiscovered'] == 1
report = load(paths['candidate13-connected.json'])
assert report['status'] == 'PASS' and len(report['cases']) == 3 and all(c['Passed'] for c in report['cases'])
assert load(paths['candidate13-package.json'])['status'] == 'PASS'
with zipfile.ZipFile(paths['source-candidate13.zip']) as z:
    assert len(z.namelist()) == len(compiled['sourceHashes'])
    for row in compiled['sourceHashes']:
        assert sha(ROOT / 'engine' / row['path']) == row['sha256'], row['path']
        assert hashlib.sha256(z.read('engine/' + Path(row['path']).as_posix())).hexdigest() == row['sha256']
review = load(paths['independent-review.json'])
assert review['sourcePins']
for row in review['sourcePins']:
    assert sha(ROOT / row['path']) == row['sha256'], row['path']
OUT.mkdir(exist_ok=True)
pins = []
for name, source in paths.items():
    shutil.copyfile(source, OUT / name)
    pins.append({'path': (OUT / name).relative_to(ROOT).as_posix(),
                 'original': source.relative_to(ROOT).as_posix(), 'sha256': sha(source)})
previous = load(PACKET / 'IMPLEMENTATION_CHECKPOINT_06.json')
summary = {
    'status': 'BOUNDED_FEAR_AND_REPERTOIRE_INITIAL_ASSESSMENT_NOT_MODULE_ACCEPTANCE',
    'previousCheckpointCommit': 'a2c2df976d25483b7323ba37e84f44cbc053a5c4',
    'contractAcceptance': '271baf94-22dd-57cb-a2ab-5f728e989b4d',
    'implemented': [
        'UseIntimidatingPresence shares all18 existing guards with execution: selected source, current turn, ownership, capability, action, recharge, geometry, mutual sight and history capacity in native order.',
        'AcquireEarnedSpell and old-profile CastKnownSpell share four repertoire outcomes. Unsupported acquisition remains denied; no spell, class level or entitlement is created.',
        'Fear remains before active-short-rest interruption; selected casting remains before repertoire fallback. Native execution and diagnostics are unchanged.',
        'Actual recharged fear commands have repeated pure assessments; actual delivery pays/draws once, exact receipt reads bypass new eligibility, and a fresh command after payment reads ActionAlreadySpent.',
    ],
    'currentNativeInitialAssessmentKinds': previous['currentNativeInitialAssessmentKinds'] + ['UseIntimidatingPresence', 'AcquireEarnedSpell'],
    'sourceInputs': len(compiled['sourceHashes']),
    'sourceArchiveSha256': sha(paths['source-candidate13.zip']),
    'dlls': [{'name': p.name, 'sha256': sha(p)} for p in sorted(build.glob('*.dll'))],
    'rawEvidence': pins,
    'actualExits': {'compileAndProfileDenials': 0, 'threeConnectedCases': 0, 'packageValidation': 0},
    'currentCandidateChecks': {'newInt05CasePassed': 1, 'existingNamedCasesPassed': 3, 'totalPassed': 4},
    'genuinePaths': [
        'Seven authentic factory-genesis denials match native execution unchanged: selected/unselected repertoire, settlement-dependent acquisition and selected/unselected fear context.',
        'Existing connected fear scenario performs two actual reuses after recharge, produces actual independent fear applications, preserves payment/retries, target markers, expiry, strict save restoration and continued play.',
        'Existing repertoire scenario keeps source-owned spells and real Cleric payment/continuation while read and execution agree that casting/acquisition remain unsupported in that old profile.',
        'Existing selected-casting authority/payload/source-denial scenario remains passing after the repertoire fallback extension.',
    ],
    'limits': [
        'Seventeen native initial-assessment kinds do not complete78 seat/two operator coverage or public V1 APIs.',
        'The source review is static only; actual test execution is recorded separately. RecoveryOpponent, all target subsets and wider privacy/profile qualification remain open.',
        'CommitFeasibility remains null; no dice, save, fear application, recharge, acquisition or future result is predicted.',
        'Remaining native families, public descriptions/costs/choices/results/diagnostics/console, planning proof and full transitive/branch/five-path/regression qualification remain open.',
        'Actual final GPT runtime acceptance remains open. No successor, Unity integration, storage cleanup or Support action.',
    ],
    'runtimeAccepted': False, 'successorStarted': False, 'unityIntegration': False,
}
(PACKET / 'IMPLEMENTATION_CHECKPOINT_07.json').write_bytes((json.dumps(summary, indent=2) + '\n').encode('utf8'))
print(json.dumps({'currentCandidatePassed': 4, 'compiledInputs': len(compiled['sourceHashes']),
                  'sourceArchiveSha256': summary['sourceArchiveSha256'], 'moduleAccepted': False}, indent=2))
