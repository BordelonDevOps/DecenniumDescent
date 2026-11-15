"""Verify recorded TAC08 approval amendments and source bindings, never runtime acceptance."""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
PROPOSAL = 'a7942a590b079f76bd95aa7a68c1d8604173c255'
BASELINE = '1fbfd5f9c0a1d492f6c299e8964d82d85a580a90'
ENGINE = '34229ec6f19c9569dd35fd7b6013b99f37759c85'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
RESPONSE = '384b9c53-9d93-56f3-901b-cede1f7d3028'
EXTRA = [
    ('DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md', SOURCE, 'stances-guard-exception-and-attack-opportunities'),
    ('DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md', SOURCE, 'condition-permissions-and-concentration-ending'),
    ('engine/com.decennium.foundation/Runtime/Core/ReinforcementRecords.cs', ENGINE, 'actual-carried-interval-and-admission-provenance'),
    ('engine/com.decennium.foundation/Runtime/Core/FixedEncounterRecord.cs', ENGINE, 'actual-roster-local-global-mapping'),
    ('engine/com.decennium.foundation/Runtime/Core/ClubAttackRecords.cs', ENGINE, 'existing-stance-record-and-attack-provenance'),
    ('engine/com.decennium.foundation/Laboratory/Model/TacticalMovementPolicy.cs', ENGINE, 'opportunity-attack-and-Press-movement-not-attack'),
]

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def require(value, message):
    if not value:
        raise ValueError(message)

def bind():
    path = PACKET / 'APPROVAL_BINDINGS.json'
    require(not path.exists(), 'Do not overwrite frozen approval source bindings')
    rows = []
    for filename, revision, role in EXTRA:
        ref = revision + ':' + filename
        data = git('show', ref)
        require(data == (ROOT / filename).read_bytes(), 'Additional checkout differs: ' + filename)
        rows.append(dict(path=filename, revision=revision, role=role,
                         gitBlob=git('rev-parse', ref).decode().strip(), bytes=len(data), sha256=sha(data),
                         workingBytes=len(data), workingSha256=sha(data), workingTreeComparison='EXACT'))
    value = dict(status='ACTUAL_APPROVAL_MANDATORY_AMENDMENT_BINDINGS', reviewedProposal=PROPOSAL,
                 actualReviewResponse=RESPONSE, engineSource=ENGINE, sources=rows)
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')

def verify():
    rows = sum((load(PACKET / name)['sources'] for name in
                ('SOURCE_BINDINGS.json', 'CONTRACT_BINDINGS.json', 'APPROVAL_BINDINGS.json')), [])
    require(len(rows) == 95 and len({x['path'] for x in rows}) == 95, 'Approved binding inventory differs')
    sources = {}
    for row in rows:
        ref = row['revision'] + ':' + row['path']
        data = git('show', ref)
        working = (ROOT / row['path']).read_bytes()
        require(len(data) == row['bytes'] and sha(data) == row['sha256']
                and git('rev-parse', ref).decode().strip() == row['gitBlob'], 'Pinned source differs: ' + ref)
        require(len(working) == row['workingBytes'] and sha(working) == row['workingSha256'], 'Inspected source changed')
        require(data == working or row['path'] == 'docs/canon/CANON_MANIFEST.json'
                and row['workingTreeComparison'] == 'CRLF_ONLY'
                and data.replace(b'\r\n', b'\n') == working.replace(b'\r\n', b'\n'), 'Unrecorded source difference')
        sources[row['path']] = data
    old = load(PACKET / 'CONTRACT_AUDIT.json')
    prefix = 'docs/unity/evidence/2026-11-15-tac08-cleric-casting/'
    for row in old['artifacts']:
        blob = git('show', PROPOSAL + ':' + prefix + row['path'])
        require(len(blob) == row['bytes'] and sha(blob) == row['sha256']
                and blob == (PACKET / row['path']).read_bytes(), 'Original proposal artifact changed: ' + row['path'])
    require(git('show', PROPOSAL+':'+prefix+'CONTRACT_AUDIT.json') == (PACKET/'CONTRACT_AUDIT.json').read_bytes(),
            'Historical proposal audit changed')
    require(not git('diff', BASELINE, '--', 'engine'), 'Engine changed before approval recording')
    review = (PACKET / 'GPT_CONTRACT_REVIEW.md').read_text(encoding='utf-8-sig')
    require(RESPONSE in review and '**Approved for bounded TEST_ONLY implementation' in review
            and 'Codex agrees with the bounded implementation approval and every mandatory amendment.' in review,
            'Actual approval/agreement record missing')
    contract = (PACKET / 'APPROVED_CASTING_CONTRACT.md').read_text(encoding='utf-8-sig')
    requirements = {
        'active-detect-focus-magic': 'active Detect focus also counts as magical activity',
        'passive-concentration-not-activity': 'Passive concentration alone does not count as activity',
        'no-check-hide-search': 'A Hide or Search path which performs no check',
        'no-new-hide-retry': 'Guidance does not itself authorize an otherwise prohibited unchanged Hide retry',
        'sanctuary-original-targets': "source's original legal target set and trigger window",
        'no-reaction-action-conversion': 'no Reaction-to-Action conversion is allowed',
        'forgo-original-occurrence': 'using its existing decline semantics, resumes the suspended parent',
        'defender-controller': "including the later defender's controller",
        'carried-interval': 'never fabricate a Start or call GlobalTurn(-1)',
        'pure-eligibility': 'must not simulate the future WIS result',
        'focused-generating-cast': 'consume that election once at its generating cast',
        'guard-exception': "Guarded +1 coexists with Guard's first-attack +2",
        'sanctuary-narrow-exception': "The sole **P8** exception is this Sanctuary's own automatic defensive admission save",
        'taint-and-freshness': 'no freshness reset, and remaining ineligible contamination does not become safe',
        'paid-protected-focus': 'spends its Action even if school information is protected',
        'blocked-aura': 'A blocked or unperceived aura supplies no selectable observation',
        'ready-inventory': 'Current Ready supports club/unarmed attacks, not readied ranged',
        'press-inventory': 'Press continuation is movement, not an independent attack',
    }
    for key, marker in requirements.items():
        require(marker in contract, 'Mandatory amendment missing: ' + key)
    require('through an offensive source' not in contract, 'Rejected general offensive-source restriction retained')
    for path, marker in [
        (EXTRA[0][0], b'Its +1 can coexist with Guard'),
        (EXTRA[0][0], b'Choose +1 save DC for one spell'),
        (EXTRA[1][0], b'concentration ending'),
        (EXTRA[2][0], b'public sealed class ReinforcementCarry'),
        (EXTRA[5][0], b'TacticalMoveKind.Press'),
    ]:
        require(marker in sources[path], 'Added source anchor missing: ' + path)
    files = ['APPROVED_CASTING_CONTRACT.md', 'APPROVAL_BINDINGS.json', 'GPT_CONTRACT_REVIEW.md',
             'REVIEW_REQUEST.json', 'support/Verify-Approval.py']
    result = dict(status='PASS_RECORDED_APPROVAL_AND_SOURCE_BINDINGS_ONLY',
                  atUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), reviewedProposal=PROPOSAL,
                  baseline=BASELINE, engineSource=ENGINE, actualResponse=RESPONSE,
                  sourceFiles=95, additionalApprovalFiles=6, preservedProposalArtifacts=7,
                  mandatoryAmendments=list(requirements), engineUnchanged=True,
                  approval='BOUNDED_TEST_ONLY_IMPLEMENTATION_AUTHORIZED',
                  runtimeAcceptance='NOT_GRANTED', compilation='NOT_RUN_DOCUMENTATION_ONLY',
                  runtimeTests='NOT_RUN_DOCUMENTATION_ONLY', wholeEngine='NOT_COMPLETE', unity='DEFERRED',
                  artifacts=[dict(path=x, bytes=len((PACKET/x).read_bytes()), sha256=sha((PACKET/x).read_bytes())) for x in files])
    (PACKET/'APPROVAL_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS recorded approval/source bindings only: 95 sources, 18 mandatory amendment assertions, seven original artifacts unchanged; no runtime acceptance.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--bind',action='store_true')
    args=parser.parse_args()
    if args.bind:
        bind()
    verify()
