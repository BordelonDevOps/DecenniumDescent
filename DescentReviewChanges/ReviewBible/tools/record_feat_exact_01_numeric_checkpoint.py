"""Preserve owner navigation and record finite numeric prerequisite evidence."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data),
            'sha256': sha256(data).hexdigest()}


target = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_NUMERIC_PREREQUISITES.json'
previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_ACQUISITION.json'
preservation = A/'navigation-before-feat-exact-01-numeric-prerequisites'
assert not target.exists() and not preservation.exists(), 'One-use checkpoint already recorded'
report_path = A/'FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json'
notes_path = A/'FEAT_EXACT_01_NUMERIC_PREREQUISITE_NOTES.md'
report = read(report_path)
assert not report['failures'] and report['status'] == 'passed-finite-numeric-projections'
assert report['counts']['numericPredicateFeats'] == 209
assert report['counts']['remainingCredentialDependentFeats'] == 126
assert not report['allNumericCohortCompleteAcquisitionsValidated']
for source in report['sourceBindings']:
    assert info(G/source['path']) == source, source['path']

nav = R/'tools/build_review_map.py'
text = nav.read_text(encoding='utf-8')
anchor = '        ("Feat acquisition history — current reference checks", "FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json"),'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + '\n'
    '        ("Feat numeric prerequisites — 209 source-qualified projections", "FEAT_EXACT_01_NUMERIC_PREREQUISITE_NOTES.md"),\n'
    '        ("Feat numeric prerequisites — independent printed-string checks", "FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json"),')
anchor = 'The remaining finite acceptance evidence, full package and actual exact review remain outstanding.'
assert text.count(anchor) == 1
text = text.replace(anchor,
    'A numeric prerequisite pass now covers209 of335 identities across62 printed forms and1678 boundary cases, '
    'using416 source-qualified synthetic ability/class-history projections. Independent printed-string and normalized-tree '
    'results agree;11846 checks pass, including all17 class ASI schedules. This proves numeric/level/None predicates '
    'and earned unspent opportunity gates only, not complete character builds or feat acquisitions. The other126 identities '
    'still require actual proficiency, spell, lineage, mutation, owned-feat, trade or context credentials. '
    + anchor)
compile(text, str(nav), 'exec')
preserved = []
for path in (nav, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json'):
    original = info(path)
    copy = preservation/original['path']
    copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, copy)
    assert copy.read_bytes() == path.read_bytes()
    preserved.append({**original, 'preservedCopy': copy.relative_to(G).as_posix()})
manifest = preservation/'PRESERVATION_MANIFEST.json'
manifest.write_text(json.dumps(preserved, indent=2)+'\n', encoding='utf-8')
nav.write_text(text, encoding='utf-8', newline='\n')
result = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True,
                        text=True, encoding='utf-8')
if result.returncode:
    print(result.stderr)
    raise SystemExit(result.returncode)
navigation = read(A/'REVIEW_MAP_BUILD.json')
assert not navigation['missingLinks']
assert info(G/'REVIEW_MAP.html')['sha256'] == navigation['sha256']

state = read(previous)
state.update({
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: all335 contracts and fulfilled actual GPT ACQ-01; full acquisition cases remained open.',
    'previousCheckpoint': info(previous),
    'status': '209 numeric/level/None prerequisite trees now have independent printed-string boundary checks '
              'with source-qualified synthetic projections and actual class feat schedules. '
              '126 credential-dependent trees and complete acquisition choices/history remain open. '
              'No source rules, feat procedures, operative candidates or GPT review state changed.',
    'featNumericPrerequisitePass': {
        'report': info(report_path), 'notes': info(notes_path), 'counts': report['counts'],
        'checks': report['checks'], 'checkKinds': report['checkKinds'], 'failures': 0,
        'model': info(R/'tools/feat_exact_01_numeric_prerequisite_model.py'),
        'validator': info(R/'tools/validate_feat_exact_01_numeric_prerequisites.py'),
        'scope': report['scope'],
        'allNumericCohortCompleteAcquisitionsValidated': False,
        'all335ActualAcquisitionBoundaryCasesExecuted': False,
        'candidateReadyForSubmission': False,
        'noNewRulesAdopted': True,
    },
    'navigation': {'map': info(G/'REVIEW_MAP.html'), 'receipt': info(A/'REVIEW_MAP_BUILD.json'),
                   'links': navigation['existingDistinctLinks'], 'missingLinks': []},
})
state['safeNextActions'] = [
    'Numeric prerequisites are no longer an untested string inventory:209 identities/62 forms have1678 independent '
    'printed-string boundary cases and416 synthetic permanent-score/class-history projections.11846 checks pass. '
    'The report contains below/equal/above grids, OR-arm isolation, actual once-only Human/Imperial bonuses, '
    'earned/unspent opportunities and all17 class schedules. Keep its explicit partial-snapshot scope; '
    'it does not close complete acquisitions or authenticate human rolls/campaign awards.',
    'Continue FXC-05 with the126 credential-dependent records listed in FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json /remaining. '
    'Per-identity nonnumeric atom counts overlap:26 actualProficiency,25 actualSpellcastingRoute,17 actualWeaponProficiency, '
    '14 classLevel,7 equippedMutation,5 distinctEquippedMutations,8 actualCastAccess,13 permanentSkillModifier, '
    '14 actualLineageReceipt,4 actualEstablishedReceipt,18 ownedFeat,1 ownedSupplementFeat,1 trainedTradeLevel. '
    'Use actual first-class/multiclass training, selected skill choices, reviewed spell placements/repertoire, '
    'legal Warrior slots and specific lineage/context source receipts. Do not invent missing legacy identities or campaign history.',
    'The209 numeric cohort still needs feat-specific selection choices, repeatability histories, finite initialization '
    'and use/payload availability as applicable; None is not a free feat or permission to activate deferred spells. '
    'Existing897 acquisition-history checks support their stated subsets only. The numeric validator is read-only '
    'against source/candidates and refuses report overwrite; if new concerns justify a rerun, supply new --report and --notes paths.',
] + state['safeNextActions'][1:]
state.setdefault('preservationManifests', []).append(info(manifest))
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(state, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps({'checkpoint': info(target), 'navigationLinks': navigation['existingDistinctLinks'],
                  'numericPredicateFeats': 209, 'credentialDependentFeatsRemaining': 126,
                  'sourceInformationDeleted': False, 'candidateReadyForSubmission': False,
                  'pushed': False, 'cosmologyReviewed': False}, indent=2))
