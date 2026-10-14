"""Record actual ACQ-03 source application; behavioral acceptance stays open."""
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


target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ03_SOURCE_APPLICATION.json'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_LINEAGE_PREREQUISITES.json'
preservation = A / 'navigation-and-coverage-before-feat327-acq03-source-application'
delta_path = A / 'FEAT327_ACQ_03_SOURCE_COVERAGE_DELTA.json'
assert not target.exists() and not preservation.exists() and not delta_path.exists(), 'One-use checkpoint already started'
decision_path = A / 'FEAT327_ACQ_03_RECEIVED_DECISION.json'
operations_path = A / 'FEAT327_ACQ_03_DERIVED_OPERATIONS.json'
checks_path = A / 'FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json'
decision, operations, checks = map(read, [decision_path, operations_path, checks_path])
assert decision['replyMessageId'] == '67894042-55c3-44d4-bf3a-a2f31dd1140b'
assert checks['checks'] == 175 and not checks['failures'] and not checks['finiteBehavioralAcceptanceComplete']
assert info(operations_path) == checks['derivedOperations']
for change in operations['changes']:
    assert info(G / change['after']['path']) == change['after']
now = datetime.now(timezone.utc).isoformat()
ledger_path = R / 'data/playtest/game_development_coverage.json'
before = read(ledger_path); ledger = deepcopy(before); changed = {'DD-06', 'DD-14', 'DD-69'}
scope = (
    'Actual GPT ACQ-03 reply67894042-55c3-44d4-bf3a-a2f31dd1140b adopted the explicit casting-prerequisite snapshot bridge. '
    'Retained personal grants and actual repertoire govern acquisition; renewable depletion/temporary suppression do not erase the credential, '
    'while ordinary unprepared book entries need a genuine preparation exception. No school is assigned to Eldritch Blast. '
    'Eight current derived files contain the exact FS-02 insertion, FS-09 sentence correction,33 casting-node references and supplementary Spell Focus policy reference. '
    'All prior bytes are preserved.175 independent whole-file/source checks pass, including all47 candidate artifacts through measured ACQ-01/02/03 histories. '
    'A-H and additional behavioral acceptance remain outstanding;33 annotations are not33 new validated acquisitions. '
    'The latest prerequisite bookkeeping remains292 partial identities/43 other credential identities; exact feat approval and whole-game completion remain open.')
for row in ledger['aspects']:
    if row['id'] not in changed:
        continue
    row.setdefault('reviewEvidence', []).append(decision_path.relative_to(G).as_posix())
    row.setdefault('validationEvidence', []).append(checks_path.relative_to(G).as_posix())
    row.setdefault('completedScopes', []).append(scope)
    row.setdefault('currentEvidenceAddenda', []).append({
        'id': 'FEAT327-ACQ-03-SOURCE-APPLICATION', 'recordedAtUtc': now,
        'status': 'actual-source-amendment-applied-behavioral-acceptance-pending',
        'decision': decision_path.relative_to(G).as_posix(), 'operations': operations_path.relative_to(G).as_posix(),
        'sourceChecks': checks_path.relative_to(G).as_posix(), 'onlyThisNamedIssueClosed': False,
        'newSourceRuleAdopted': True, 'fullFeatCandidateApproved': False,
    })
    if row['id'] == 'DD-14':
        row.setdefault('historicalOpenIssueSnapshots', []).append({
            'recordedAtUtc': now, 'reason': 'Preserve pending ACQ-03 conference wording before its actual final source decision.',
            'status': row['status'], 'openIssues': deepcopy(row['openIssues']),
        })
        old = row['openIssues'][1]
        assert 'ACQ-03 casting snapshots are submitted and pending.' in old
        row['openIssues'][1] = old.replace('ACQ-03 casting snapshots are submitted and pending.',
            'ACQ-03 is received and its exact eight-file source application passes175 independent checks. '
            'Its source-qualified A-H and extra casting-snapshot behavioral acceptance cases still need execution; the named issue is not yet marked fulfilled.')
for x, y in zip(before['aspects'], ledger['aspects']):
    assert x['id'] == y['id'] and x.get('closure') == y.get('closure') and x.get('humanEvidence') == y.get('humanEvidence')
    if x['id'] not in changed:
        assert x == y
nav = R / 'tools/build_review_map.py'; text = nav.read_text(encoding='utf-8')
anchor = '        "FEAT_EXACT_01_LINEAGE_COVERAGE_DELTA.json",'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + '\n        "FEAT327_ACQ_03_SOURCE_COVERAGE_DELTA.json",')
anchor = '    chain = list(entries.values()) + coverage_deltas'
assert text.count(anchor) == 1
text = text.replace(anchor, '    acq03 = read(A / "FEAT327_ACQ_03_DERIVED_OPERATIONS.json")\n    chain = list(entries.values()) + acq03["changes"] + coverage_deltas')
anchor = '        ("Casting prerequisites — exact ACQ-03 question", "FEAT327_ACQ_03_CASTING_PREREQUISITE_QUESTION.txt"),'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + '\n'
    '        ("Casting prerequisites — actual GPT addendum", "FEAT327_ACQ_03_GPT_ADDENDUM.md"),\n'
    '        ("Casting prerequisites — eight preserved source changes", "FEAT327_ACQ_03_DERIVED_OPERATIONS.json"),\n'
    '        ("Casting prerequisites — independent source verification", "FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json"),')
anchor = 'ACQ-03 is submitted for the separate casting-prerequisite boundary involving depletion, preparation and suppression; no ruling is adopted while its reply is pending.'
assert text.count(anchor) == 1
text = text.replace(anchor,
    'Actual GPT ACQ-03 reply67894042-55c3-44d4-bf3a-a2f31dd1140b now supplies the explicit retained-entitlement/preparation/suppression bridge. '
    'Eight current derived files contain its exact two shared-wording amendments,33 casting-node annotations and Spell Focus binding, with prior bytes preserved. '
    '175 independent source/whole-file checks pass; A-H and additional behavioral acceptance still remain, so the named issue is not yet marked fulfilled. '
    'Eldritch Blast retains its absent school; no Wizard engine, original card, null payload or runtime flag changes.')
compile(text, str(nav), 'exec')
saved = []
for p in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
    bound = info(p); dest = preservation / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, dest); assert dest.read_bytes() == p.read_bytes()
    saved.append({**bound, 'preservedCopy': dest.relative_to(G).as_posix()})
manifest = preservation / 'PRESERVATION_MANIFEST.json'; write(manifest, saved)
write(ledger_path, ledger)
write(delta_path, {'recordedAtUtc': now, 'status': 'verified-scoped-coverage-update',
    'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
    'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
    'previousFeatOpenIssuesPreservedVerbatim': True, 'validation': [info(checks_path)],
    'previousCoverageDelta': info(A / 'FEAT_EXACT_01_LINEAGE_COVERAGE_DELTA.json'),
    'actualGptDecision': info(decision_path), 'derivedOperations': info(operations_path),
    'newSourceRuleAdopted': True, 'onlyThisNamedIssueClosed': False, 'fullFeatCandidateApproved': False})
nav.write_text(text, encoding='utf-8', newline='\n')
result = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
if result.returncode:
    print(result.stderr); raise SystemExit(result.returncode)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
state = read(previous)
state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: thirteen lineage predicate identities across45 variants',
    'previousCheckpoint': info(previous), 'status': scope,
    'featACQ03SourceApplication': {'decision': info(decision_path), 'operations': info(operations_path),
        'independentSourceVerification': info(checks_path), 'descendants': 8, 'checks': 175, 'failures': 0,
        'annotatedCastingNodes': 33, 'newSourceRuleAdopted': True, 'behavioralAcceptanceComplete': False,
        'onlyThisNamedIssueClosed': False, 'candidateReadyForSubmission': False},
    'activeGptReview': {'id': 'FEAT327-ACQ-03', 'status': 'completed-source-decision-local-behavioral-acceptance-pending',
        'replyReceived': True, 'replyMessageId': decision['replyMessageId'], 'decision': info(decision_path),
        'chatUrl': decision['chatUrl'], 'browserId': '3', 'tabId': '125745639', 'wholeExactCandidateApprovalRequested': False,
        'note': 'No pending response or resubmission is needed for this source question.'},
    'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
        'links': navigation['existingDistinctLinks'], 'missingLinks': []},
    'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path),
    'navigationBindingPolicy': 'Explicit preserved coverage chain through ACQ-03 source application; source-file changes additionally follow the eight measured ACQ-03 operations after ACQ-01/02. No blanket hash exemptions.'})
state['safeNextActions'][0] = (
    'ACQ-03 actual reply67894042-55c3-44d4-bf3a-a2f31dd1140b is terminal and locally applied to eight derived files. Do not resend. '
    'Execute its exact A-H and additional behavioral acceptance using source-qualified retained personal grants, actual preparation/ritual exceptions, absent-versus-null school fields and actual paid Spell Focus choices. '
    'The175-check independent source report proves only the exact source operations; a policy annotation is not a qualifying witness.')
state['safeNextActions'].insert(1,
    'Current contracts/shared/supplement hashes legitimately changed through ACQ-03. Preserve pre-ACQ-03 Magic Initiate, lineage, training and ownership evidence as history. Use FEAT327_ACQ_03_DERIVED_OPERATIONS.json to resolve exactly eight current descendants. Do not rerun old binding checks blindly or rewrite historical snapshots.')
state['safeNextActions'].insert(2,
    'Prodigy required choices remain to implement: one genuinely new skill, one genuinely profiled tool from any allowed category, one actual eligible language/mode choice, then one now-proficient nonexpert skill. The reviewed CHARACTER_CREATION_PLAYTEST duplicate/exhaustion rule and LANGUAGE_COMMUNICATION_PLAYTEST grants/actual Director contact list control; primary tool initializes its actual trade at1/zeroXP under CRAFTING_HARVEST_PLAYTEST and CRAFTING_TRADE_REFERENCE. No ability increase or tool Expertise.')
state.setdefault('preservationManifests', []).extend([info(manifest), info(G / operations['preservationManifest']['path'])])
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(state, stream, ensure_ascii=False, indent=2); stream.write('\n')
print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
    'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0, 'sourceChecks': 175,
    'behavioralAcceptanceComplete': False, 'remainingCredentialDependentIdentities': 43,
    'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False}, indent=2))
