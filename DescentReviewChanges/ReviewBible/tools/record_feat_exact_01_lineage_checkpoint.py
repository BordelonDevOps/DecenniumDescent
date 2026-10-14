"""One-use lineage evidence checkpoint with preserved navigation/coverage history."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def write(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_LINEAGE_PREREQUISITES.json'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_INITIATE_SELECTIONS.json'
preservation = A / 'navigation-and-coverage-before-feat-exact-01-lineage-prerequisites'
delta_path = A / 'FEAT_EXACT_01_LINEAGE_COVERAGE_DELTA.json'
assert not target.exists() and not preservation.exists() and not delta_path.exists(), 'One-use checkpoint already started'
report_path = A / 'FEAT_EXACT_01_LINEAGE_PREREQUISITE_CHECK.json'
notes_path = A / 'FEAT_EXACT_01_LINEAGE_PREREQUISITE_NOTES.md'
report = read(report_path)
assert report['status'] == 'passed-current-lineage-prerequisite-projections' and not report['failures']
assert report['counts']['lineagePredicateIdentities'] == 13 and report['counts']['remainingCredentialDependentIdentities'] == 43
for bound in report['sourceBindings']:
    assert info(G / bound['path']) == bound, bound['path']
now = datetime.now(timezone.utc).isoformat()
ledger_path = R / 'data/playtest/game_development_coverage.json'
before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
scope = (
    'Thirteen current-lineage prerequisite identities have3130 passing local checks across14 ancestries,45 variants and585 variant/feat pairs. '
    'Source-qualified synthetic histories check actual variant membership, combined ability bonuses once, literal original-string versus normalized-tree agreement, '
    'and unearned/earned/spent/later class opportunities. No target feat is granted from lineage alone. '
    'Legacy Half-elf/Half-orc/Dragonborn positive receipts are not fabricated. Dragon Blood stays unresolved; Drakari is not silently Dragonborn. '
    'This is partial predicate evidence:209+12+48+10+13=292 identities, with43 others remaining, not292 complete acquisitions. '
    'Prodigy selections and all complete feat uses remain separate. ACQ-03 is still an actual pending casting question, not an adopted rule.')
for row in ledger['aspects']:
    if row['id'] not in changed:
        continue
    row.setdefault('validationEvidence', []).append(report_path.relative_to(G).as_posix())
    row.setdefault('completedScopes', []).append(scope)
    row.setdefault('currentEvidenceAddenda', []).append({
        'id': 'FEAT-EXACT-01-CURRENT-LINEAGE-13', 'recordedAtUtc': now, 'status': 'local-partial-predicate-evidence',
        'report': report_path.relative_to(G).as_posix(), 'notes': notes_path.relative_to(G).as_posix(),
        'newSourceRuleOrFeatApproval': False,
    })
    if row['id'] == 'DD-14':
        row.setdefault('historicalOpenIssueSnapshots', []).append({
            'recordedAtUtc': now, 'reason': 'Preserve the earlier56-identity state before the thirteen current-lineage predicate projections.',
            'status': row['status'], 'openIssues': deepcopy(row['openIssues']),
        })
        assert 'leaving56 other credential-dependent identities' in row['openIssues'][1]
        row['openIssues'][1] = (
            'FXC-05 partial predicate bookkeeping:209 numeric/level/None,12 Warrior,48 training,10 owned-feat and13 current-lineage identities;43 other credential-dependent identities remain. '
            'Actual GPT KEEP applies only to the earlier48+10 training/ownership evidence. Magic Initiate has466 local selection checks; current lineages have3130 local checks. '
            'No complete292-acquisition claim is made. Dragon Blood needs an actual qualifying legacy/bloodline and damage-type source; no Drakari alias. '
            'Prodigy still needs ordered skill/tool/language/Expertise selections. Acquired class-feature credentials, source trade levels, actual context and remaining casting/ownership branches remain. '
            'ACQ-03 casting snapshots are submitted and pending. Full selection, resource, use and exact-candidate review remain open.')
for old, new in zip(before['aspects'], ledger['aspects']):
    assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
    if old['id'] not in changed:
        assert old == new
assert {x['id'] for x, y in zip(before['aspects'], ledger['aspects']) if x != y} == changed
nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
anchor = '        "FEAT_EXACT_01_INITIATE_REVIEW_COVERAGE_DELTA.json",'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_LINEAGE_COVERAGE_DELTA.json",')
anchor = '        ("Remaining credentials — source preparation", "FEAT_EXACT_01_REMAINING_CREDENTIAL_SOURCE_PLAN.json"),'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + '\n'
    '        ("Lineage prerequisites — all current variants", "FEAT_EXACT_01_LINEAGE_PREREQUISITE_NOTES.md"),\n'
    '        ("Lineage prerequisites — 585 variant/feat pairs", "FEAT_EXACT_01_LINEAGE_PREREQUISITE_CHECK.json"),')
anchor = 'These are prerequisite/payment projections, not279 complete feat acquisitions; full choice, resource and use work remains.'
assert text.count(anchor) == 1
text = text.replace(anchor,
    'A further13 current-lineage predicate identities now have3130 local checks across all45 variants and585 variant/feat pairs. '
    'Current source identities and variant membership are used literally; no missing legacy ancestry or Drakari/Dragonborn alias is invented. '
    'This later pass leaves43 other credential-dependent identities; Dragon Blood remains among them. '
    'The cumulative292 identities are partial prerequisite/payment projections, not292 complete feat acquisitions; full choice, resource and use work remains.')
compile(text, str(nav), 'exec')
saved = []
for p in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
    old = info(p); dest = preservation / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, dest); assert dest.read_bytes() == p.read_bytes()
    saved.append({**old, 'preservedCopy': dest.relative_to(G).as_posix()})
manifest = preservation / 'PRESERVATION_MANIFEST.json'; write(manifest, saved)
write(ledger_path, ledger)
write(delta_path, {'recordedAtUtc': now, 'status': 'verified-scoped-coverage-update',
    'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
    'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
    'previousFeatOpenIssuesPreservedVerbatim': True, 'validation': [info(report_path), info(notes_path)],
    'previousCoverageDelta': info(A / 'FEAT_EXACT_01_INITIATE_REVIEW_COVERAGE_DELTA.json'), 'newSourceRuleOrFeatApproval': False})
nav.write_text(text, encoding='utf-8', newline='\n')
result = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
if result.returncode:
    print(result.stderr); raise SystemExit(result.returncode)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
state = read(previous)
state.update({
    'recordedAtUtc': now, 'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: actual focused GPT KEEP verified, Initiate selections recorded, ACQ-03 submitted',
    'previousCheckpoint': info(previous), 'status': scope,
    'featCurrentLineagePrerequisitePass': {'report': info(report_path), 'notes': info(notes_path),
        'counts': report['counts'], 'checks': report['checks'], 'checkKinds': report['checkKinds'], 'failures': 0,
        'scope': report['scope'], 'limits': report['limits'],
        'model': info(R / 'tools/feat_exact_01_lineage_prerequisite_model.py'),
        'validator': info(R / 'tools/validate_feat_exact_01_lineage_prerequisites.py'),
        'allCohortCompleteAcquisitionsValidated': False, 'candidateReadyForSubmission': False},
    'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
        'links': navigation['existingDistinctLinks'], 'missingLinks': []},
    'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path),
    'navigationBindingPolicy': 'Preserved coverage steps: Warrior -> Training -> Owned-feat -> Initiate/review -> current lineage. Actual ACQ-01/02 source corrections retain separate measured receipts.',
})
state['safeNextActions'].insert(2,
    'Current-lineage pass is complete within its partial scope:13 identities,45 actual variants,3130 local checks;43 other credential identities remain in the new report. No target feat was acquired from lineage alone. Prodigy choices, all use procedures and positive unavailable legacy receipts remain separate. Keep Dragon Blood unresolved without a genuine source; no Drakari/Mage alias.')
state['safeNextActions'] = [x.replace('Continue remaining56 actual casting', 'Continue remaining43 actual casting').replace(
    '56 remaining credential-dependent identities;', '43 remaining credential-dependent identities;') for x in state['safeNextActions']]
state.setdefault('preservationManifests', []).append(info(manifest))
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(state, stream, ensure_ascii=False, indent=2); stream.write('\n')
print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
    'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'lineageChecks': report['checks'],
    'remainingCredentialDependentIdentities': 43, 'pendingGptQuestion': state['activeGptReview']['id'],
    'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False}, indent=2))
