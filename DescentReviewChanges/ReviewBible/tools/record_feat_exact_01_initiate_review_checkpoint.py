"""Record the received focused review, finite Initiate work, and ACQ-03 dispatch once."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_INITIATE_SELECTIONS.json'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_OWNED_FEAT_CHAINS.json'
preservation = A / 'navigation-and-coverage-before-feat-exact-01-initiate-selections'
delta_path = A / 'FEAT_EXACT_01_INITIATE_REVIEW_COVERAGE_DELTA.json'
assert not target.exists() and not preservation.exists() and not delta_path.exists(), 'One-use checkpoint already started'
report_path = A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json'
notes_path = A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_NOTES.md'
review_path = A / 'FEAT327_FXC05_TRAINING_OWNERSHIP_REVIEW_RECEIPT.json'
dispatch_path = A / 'FEAT327_ACQ_03_SUBMISSION.json'
plan_path = A / 'FEAT_EXACT_01_REMAINING_CREDENTIAL_SOURCE_PLAN.json'
report, review, dispatch, plan = map(read, [report_path, review_path, dispatch_path, plan_path])
assert report['status'] == 'passed-finite-initiate-acquisitions' and report['checks'] == 466 and not report['failures']
assert report['counts']['newlyClosedCredentialPredicateIdentities'] == 0
assert report['counts']['remainingCredentialDependentIdentities'] == 56
assert review['status'] == 'actual-gpt-keep-partial-evidence-verified-locally' and not review['requiredCorrections']
assert dispatch['sent'] and not dispatch['replyReceived'] and not dispatch['newRuleAdopted']
for bound in report['sourceBindings'] + plan['sourceBindings'] + dispatch['sourceBindingsVerifiedBeforeReceipt']:
    assert info(G / bound['path']) == bound, bound['path']
for key in ['archive', 'extractedManifest', 'verdict', 'register', 'visibleReply']:
    assert info(G / review[key]['path']) == review[key]
for key in ['request', 'preparation', 'submissionScreenshot']:
    assert info(G / dispatch[key]['path']) == dispatch[key]
now = datetime.now(timezone.utc).isoformat()
ledger_path = R / 'data/playtest/game_development_coverage.json'
before = read(ledger_path)
ledger = deepcopy(before)
changed = {'DD-06', 'DD-14', 'DD-69'}
for row in ledger['aspects']:
    if row['id'] not in changed:
        continue
    row.setdefault('validationEvidence', []).append(report_path.relative_to(G).as_posix())
    row.setdefault('reviewEvidence', []).extend([review_path.relative_to(G).as_posix(), dispatch_path.relative_to(G).as_posix()])
    row.setdefault('completedScopes', []).append(
        'Actual GPT accepted the48-training and10-owned-feat reports as partial prerequisite/payment evidence with no required corrections. '
        'Its20-payload returned archive and all34 submitted payloads are locally verified;33 repository inputs are unchanged and one README is package-only. '
        'Both reproduced JSON reports match locally except creation timestamps. GPT reports230 additional finite reference checks. '
        'A separate local Magic Initiate pass has466 passing checks over16 curricula, six named plus one generic identity, and39 paid selection histories. '
        'It verifies selected spell entitlements and initialization only, adds zero new prerequisite identities, and does not establish complete acquisitions or use. '
        'ACQ-03 is now submitted to settle casting-prerequisite snapshots; no proposed ruling has been adopted.')
    row.setdefault('currentEvidenceAddenda', []).append({
        'id': 'FEAT-EXACT-01-INITIATE-AND-FOCUSED-REVIEW', 'recordedAtUtc': now,
        'status': 'focused-evidence-reviewed-initiate-local-casting-question-pending',
        'report': report_path.relative_to(G).as_posix(), 'notes': notes_path.relative_to(G).as_posix(),
        'actualGptReview': review_path.relative_to(G).as_posix(),
        'nextCastingQuestion': dispatch_path.relative_to(G).as_posix(),
        'reviewScope': 'Only the earlier training and ownership partial evidence; no full feat approval or new source rule.',
        'newSourceRuleOrFeatApproval': False,
    })
    if row['id'] == 'DD-14':
        row.setdefault('historicalOpenIssueSnapshots', []).append({
            'recordedAtUtc': now, 'reason': 'Preserve the earlier pending focused-review state before receipt of its actual KEEP verdict.',
            'status': row['status'], 'openIssues': deepcopy(row['openIssues']),
        })
        assert '56 other credential-dependent' in row['openIssues'][1]
        row['openIssues'][1] = (
            'FXC-05 has209 numeric/level/None,12 Warrior,48 training and10 owned-feat partial prerequisite identities, leaving56 other credential-dependent identities. '
            'Actual GPT accepted the48+10 evidence within its tested scope with no corrections. The16-curriculum Magic Initiate selection pass adds466 local checks '
            'and39 histories but zero new predicate identities. ACQ-03 casting snapshot clarification is submitted and pending. '
            'Track acquired class-feature credentials explicitly, including Frenzied Rage: actual qualifying acquired class-rage ability or the legal Berserker alternative, '
            'with CON15 and a separately earned unspent opportunity. Do not infer that receipt from a class/resource name. '
            'All named selections, finite resource/use procedures and complete class builds remain separate;279 partial identities do not mean279 complete acquisitions.')
for old, new in zip(before['aspects'], ledger['aspects']):
    assert old['id'] == new['id']
    assert old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
    if old['id'] not in changed:
        assert old == new
assert {x['id'] for x, y in zip(before['aspects'], ledger['aspects']) if x != y} == changed

nav = R / 'tools/build_review_map.py'
nav_text = nav.read_text(encoding='utf-8')
anchor = '        "FEAT_EXACT_01_OWNED_FEAT_COVERAGE_DELTA.json",'
assert nav_text.count(anchor) == 1
nav_text = nav_text.replace(anchor, anchor + '\n        "FEAT_EXACT_01_INITIATE_REVIEW_COVERAGE_DELTA.json",')
anchor = '        ("Training and ownership — focused review request", "FEAT327_FXC05_TRAINING_OWNERSHIP_REQUEST.txt"),'
assert nav_text.count(anchor) == 1
nav_text = nav_text.replace(anchor, anchor + '\n'
    '        ("Training and ownership — received GPT review receipt", "FEAT327_FXC05_TRAINING_OWNERSHIP_REVIEW_RECEIPT.json"),\n'
    '        ("Training and ownership — complete GPT verdict", "feat327-fxc05-training-ownership-review/FEAT327_FXC05_REVIEW_VERDICT.md"),\n'
    '        ("Magic Initiate — all sixteen curricula selection notes", "FEAT_EXACT_01_INITIATE_ACQUISITION_NOTES.md"),\n'
    '        ("Magic Initiate — 39 paid selection histories", "FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json"),\n'
    '        ("Casting prerequisites — actual ACQ-03 dispatch", "FEAT327_ACQ_03_SUBMISSION.json"),\n'
    '        ("Casting prerequisites — exact ACQ-03 question", "FEAT327_ACQ_03_CASTING_PREREQUISITE_QUESTION.txt"),\n'
    '        ("Remaining credentials — source preparation", "FEAT_EXACT_01_REMAINING_CREDENTIAL_SOURCE_PLAN.json"),')
anchor = 'The48-training and ten-ownership evidence, with34 full payloads, was submitted to actual GPT for focused evidence review; that reply is pending.'
assert nav_text.count(anchor) == 1
nav_text = nav_text.replace(anchor,
    'Actual GPT accepted the48-training and ten-ownership partial reports with no required corrections; its20-payload returned archive is verified, and both reproduced reports match except timestamps. '
    'The acquired class-feature branch for Frenzied Rage is explicitly tracked, without inventing a rage ability or receipt. '
    'Magic Initiate now has466 local selection checks over16 curricula and39 histories, preserving exact source spell identities, schools and abilities; this adds zero new prerequisite identities. '
    'ACQ-03 is submitted for the separate casting-prerequisite boundary involving depletion, preparation and suppression; no ruling is adopted while its reply is pending.')
compile(nav_text, str(nav), 'exec')
saved = []
for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
    original = info(path)
    dest = preservation / path.relative_to(G)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, dest)
    assert dest.read_bytes() == path.read_bytes()
    saved.append({**original, 'preservedCopy': dest.relative_to(G).as_posix()})
manifest_path = preservation / 'PRESERVATION_MANIFEST.json'
write(manifest_path, saved)
write(ledger_path, ledger)
write(delta_path, {
    'recordedAtUtc': now, 'status': 'verified-scoped-coverage-update',
    'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
    'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
    'previousFeatOpenIssuesPreservedVerbatim': True, 'validation': [info(report_path), info(notes_path)],
    'previousCoverageDelta': info(A / 'FEAT_EXACT_01_OWNED_FEAT_COVERAGE_DELTA.json'),
    'receivedActualGptReview': info(review_path), 'pendingCastingDispatch': info(dispatch_path),
    'newSourceRuleOrFeatApproval': False,
})
nav.write_text(nav_text, encoding='utf-8', newline='\n')
result = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
if result.returncode:
    print(result.stderr)
    raise SystemExit(result.returncode)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
for bound in report['sourceBindings']:
    assert info(G / bound['path']) == bound
state = read(previous)
state.update({
    'recordedAtUtc': now, 'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: ten paid ownership chains and submitted focused evidence review',
    'previousCheckpoint': info(previous),
    'status': 'Actual GPT KEEP verdict received and verified for48 training plus10 ownership partial evidence; all16 Magic Initiate curricula have466 local selection checks. ACQ-03 casting credential clarification is submitted and pending.56 other credential identities and full acquisition/use/exact-review work remain.',
    'featTrainingOwnershipActualReview': {
        'receipt': info(review_path), 'disposition': review['status'], 'requiredCorrections': [],
        'additionalReviewerReferenceChecks': review['additionalReviewerChecks'],
        'fullCandidateApproved': False, 'nextWorkClarification': review['nextWorkClarification'],
    },
    'featInitiateSelectionPass': {
        'report': info(report_path), 'notes': info(notes_path), 'counts': report['counts'], 'checks': report['checks'],
        'checkKinds': report['checkKinds'], 'failures': 0, 'scope': report['scope'],
        'model': info(R / 'tools/feat_exact_01_initiate_acquisition_model.py'),
        'validator': info(R / 'tools/validate_feat_exact_01_initiate_acquisitions.py'),
        'unresolvedCastingQuestion': report['unresolvedCastingQuestion'], 'noNewRulesAdopted': True,
        'allSevenFeatsFullUsesValidated': False, 'candidateReadyForSubmission': False,
    },
    'remainingCredentialSourcePlan': info(plan_path),
    'activeGptReview': {
        'id': dispatch['reviewId'], 'status': dispatch['status'], 'dispatch': info(dispatch_path),
        'chatUrl': dispatch['chatUrl'], 'browserId': dispatch['browserId'], 'tabId': dispatch['tabId'],
        'requestMessageId': None, 'wholeExactCandidateApprovalRequested': False, 'replyReceived': False,
        'observationLimit': 'Full question converted by ChatGPT into a pasted-text attachment; new submitted entry and responding UI verified. No ID captured; do not resend.',
    },
    'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
                   'links': navigation['existingDistinctLinks'], 'missingLinks': []},
    'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path),
    'navigationBindingPolicy': 'Explicit preserved coverage chain Warrior -> Training -> Owned-feat -> Initiate and received review. ACQ-01/02 current source corrections retain their separate receipts. No blanket mismatch exemption.',
})
old_actions = state['safeNextActions']
state['safeNextActions'] = [
    'Read the final actual FEAT327-ACQ-03 reply in Chrome3 tab125745639. It was submitted as Pasted text(20261012-033155).txt and showed ChatGPT responding. Preserve exact source directions and any returned archive; do not resend or adopt the proposed boundary before the actual reply.',
    'The prior FEAT327-FXC05-TRAINING-OWNERSHIP review is terminal KEEP with no required corrections. Its20-payload archive is preserved and verified; both reports equal the reviewer reproductions except timestamps. No unchanged resubmission or extra correction gate is needed.',
    'Magic Initiate:16 curricula, six named plus one generic identity,39 paid selection histories,466 passing checks. Exact selected entitlements and one-curriculum duplication are modeled; actual spell use and depleted/suppressed casting credentials are not established. These seven identities were already in the numeric/None cohort;56 remaining stays56.',
    review['nextWorkClarification']['wording'],
    'Continue remaining56 actual casting/supplement ownership/lineage/trade/context branches with source-qualified acquired credentials. Preserve independent noncasting alternatives for Core Infusion, Curse Channeling, Lightning Affinity and Companion Training. Class names, source lists, RP capacity and check modifiers do not manufacture those credentials.',
    'The remaining source plan is preparation only: no Drakari-to-Dragonborn or modern-to-legacy lineage alias, no invented Sorcerer class, and no inferred trade level or campaign event. Positive synthetic premises must remain explicitly conditional and source-bound.',
] + old_actions[2:]
state['safeNextActions'] = [x.replace('Complete numeric-cohort named choices/repeatability/initialization;114 credential-dependent trees;', 'Complete named choices/repeatability/initialization across all cohorts;56 remaining credential-dependent identities;') for x in state['safeNextActions']]
state.setdefault('preservationManifests', []).append(info(manifest_path))
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(state, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
    'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
    'focusedReview': 'KEEP partial training/ownership evidence; zero corrections', 'initiateChecks': 466,
    'remainingCredentialDependentIdentities': 56, 'pendingGptQuestion': dispatch['reviewId'],
    'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False}, indent=2))
