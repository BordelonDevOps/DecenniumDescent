"""Record an actual bounded acceptance without closing broader workstreams.

Requires retained GPT verdict and explicit Codex agreement. Does not run gameplay.
"""
from pathlib import Path
import hashlib
import copy
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
SOURCE = '3c5135ae0d664d79528fff1f2676fae2198beb28'
BASE = '15907773168d620d09fa084ea3cc111c5bd0bb35'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


acceptance = read(PACKET / 'FINAL_ACCEPTANCE.json')
assert acceptance['status'] == 'ACCEPTED_BOUNDED'
assert acceptance['sourceCommit'] == SOURCE
assert acceptance['codexAgrees'] is True and acceptance['gptResponseId']
assert not acceptance['wholeEngineComplete'] and not acceptance['unityAuthorized']
review = read(PACKET / 'GPT_FINAL_REVIEW.json')
assert any(item.get('id') == acceptance['gptResponseId'] and item.get('type') == 'agentMessage'
           for turn in review['turns'] for item in turn['items'])
index = read(PACKET / 'QUALIFICATION_INDEX.json')
assert index['regression']['reconciledPassed'] == 1587
assert index['fivePaths']['crossPathHashComparisons'] == 784
status_path = ROOT / 'docs/unity/IMPLEMENTATION_STATUS.json'
status = read(status_path)
baseline = json.loads(subprocess.check_output(['git', 'show', BASE + ':docs/unity/IMPLEMENTATION_STATUS.json'], cwd=ROOT))
assert status['activeImplementation']['sourceCommit'] == SOURCE
assert len(status['workItems']) == 49
assert sum(len(r['dependencies']) for r in status['workItems']) == 120
assert sum(len(r['completionCriteria']) for r in status['workItems']) == 100
protected = ['id', 'title', 'dependencies', 'acceptance', 'currentStatus', 'wholeWorkstreamComplete', 'completionCriteria']
for old, current in zip(baseline['workItems'], status['workItems']):
    for key in protected:
        assert old[key] == current[key], (current['id'], key)
assert status['completionContract'] == baseline['completionContract']
readiness_comparison = copy.deepcopy(status['readiness'])
next(r for r in readiness_comparison['gates'] if r['id'] == 'UR-02')['remaining'] = next(
    r for r in baseline['readiness']['gates'] if r['id'] == 'UR-02')['remaining']
assert readiness_comparison == baseline['readiness']
next(r for r in status['readiness']['gates'] if r['id'] == 'UR-02')['remaining'] = (
    'Implement and qualify the required open capabilities under the concrete completion contract, following the unchanged graph and scoped prerequisite reviews. '
    'Consecration115 is accepted only within its bounded amended contract; broader required capabilities remain incomplete. '
    'The owner directs stop after the final push; no next module is authorized by this status update.')
status['priorAcceptedBaseline'] = {key: baseline[key] for key in ['implementationBaseline', 'frozenRuntime', 'qualifiedConsoleHost']}
status['status'] = 'ACCEPTED_BOUNDED_IMPLEMENTATION'
status['purpose'] = 'Current C# implementation coverage; Consecration115 bounded acceptance added. All broader completion criteria and prior exact acceptances remain authoritative. Owner directs stop after final push.'
status['implementationBaseline'] = acceptance['candidateCommit']
status['frozenRuntime'] = SOURCE
status['qualifiedConsoleHost'] = SOURCE
status['hold']['implementation'] = 'STOP_AFTER_FINAL_PUSH_BY_OWNER'
status['hold']['allowed'] = 'Retain actual Consecration115 acceptance and push final records, then stop.'
status['hold']['prohibited'] = 'No next module or Unity integration. No storage cleanup, Support action or production promotion.'
status['hold']['nextRecordedGate'] = 'Consecration115 is accepted within its amended contract and explicit allocations. Stop after the final push; no successor is started or newly selected. Broader required gaps remain in the workstream rows and pre-Unity contract.'
active = status['activeImplementation']
active.update({'status': 'ACCEPTED_BOUNDED', 'runtimeAccepted': True,
               'ownerInstruction': 'Finish Consecration, push final work, then stop. No next module or Unity integration.',
               'finalAcceptance': 'docs/unity/evidence/2026-11-17-chr05-consecration/FINAL_ACCEPTANCE.json',
               'gptResponseId': acceptance['gptResponseId'], 'evidenceCandidateCommit': acceptance['candidateCommit']})
row = next(r for r in status['workItems'] if r['id'] == 'CHR-05')
row['implementedOrAcceptedScope'] = next(r for r in baseline['workItems'] if r['id'] == 'CHR-05')['implementedOrAcceptedScope'] + ' Consecration115 additionally accepts owned paid Consecrate, original terrain expiry/recharge, source-qualified Undead attack contributions and ordered capped Ground healing within its amended TEST_ONLY contract.'
row['remainingCapabilityOrQualification'] = 'Outside activation after the already-settled owner magical-activity slot remains a broader mandatory integration gap (CG-CONTEXT-01), not a source prohibition. The entirely genuine combined Ground/final-cap/zero-Radiance/cure intersection remains UNPROVED; the explicit bounded mechanical allocation is accepted, with no modified campaign adoption or persisted-idempotency claim from a direct repeat. Broader class engines/cards, resource lifecycles, higher-level scaling and source-specific exceptions remain; Saint resurrection ownership is not supplied by Bishop entry.'
new_evidence = 'docs/unity/evidence/2026-11-17-chr05-consecration/FINAL_ACCEPTANCE.json'
if new_evidence not in row['evidence']:
    row['evidence'].append(new_evidence)
for current in status['workItems']:
    current['ownerHold'] = 'Owner directs stop after the Consecration final push. No next module or Unity integration.'
    old = next(r for r in baseline['workItems'] if r['id'] == current['id'])
    assert set(old['evidence']).issubset(current['evidence'])
    if current['id'] != 'CHR-05':
        assert current['implementedOrAcceptedScope'] == old['implementedOrAcceptedScope']
status_path.write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8', newline='\n')

legacy = ROOT / 'docs/unity/evidence/2026-11-17-implementation-map/Update-ImplementationMap.py'
spec = importlib.util.spec_from_file_location('retained_map_renderer', legacy)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
text = renderer.render(status)
replacements = {
    'This update changes documentation only; it does not start the next module.': 'Consecration115 is accepted within its bounded contract. The owner directs stop after the final push; no next module is started.',
    '**Documentation review:** ACCEPTED_BOUNDED_IMPLEMENTATION.': '**Current status:** ACCEPTED_BOUNDED_IMPLEMENTATION. **Prior planning review:**',
    'Actual final map review': 'Accepted pre-Unity planning review',
    'declared geometry and Ferry-Wraith encounter.': 'declared geometry, Ferry-Wraith encounter and Consecration115.',
    'The last accepted qualification is **1,584/1,584 registered cases** and five matching 463-command paths. These are retained TAC-10 executions, not tests run for this documentation update.': 'Consecration115 reconciles **1,587/1,587 registered cases**, including two separately retained corrections, and five complete matching 428-command paths. [Actual final Consecration acceptance](evidence/2026-11-17-chr05-consecration/FINAL_ACCEPTANCE.json). Prior TAC-10 qualification remains preserved: 1,584 cases and five 463-command paths were not restarted.',
    '## Held next dependency': '## Accepted dependency and owner stop',
    'return the complete amended two-card Consecration contract.': 'accepted Consecration115 under the amended two-card contract.',
    'The five terrain interpretations remain settled. The held contract must retain recharge registration,': 'The five terrain interpretations remain settled. The accepted bounded implementation retains recharge registration,',
    'No such successor work is performed here.': 'The genuine combined cap/cure intersection remains UNPROVED under its accepted mechanical allocation; CG-CONTEXT-01 remains a broader mandatory gap. No further successor work is performed here.',
}
for before, after in replacements.items():
    assert before in text, before
    text = text.replace(before, after)
paragraph = (f"**Last accepted module:** {active['module']} at `{SOURCE}`. "
             "[Evidence and exact review](evidence/2026-11-17-chr05-consecration/README.md). "
             "CHR-05 remains PARTIAL. Whole-engine closure, reference performance and Unity readiness remain unqualified.\n\n")
text = text.replace('## Read this map\n', paragraph + '## Read this map\n', 1)
map_path = ROOT / 'docs/unity/IMPLEMENTATION_MAP.md'
map_path.write_text(text, encoding='utf-8', newline='\n')
update = (f"Current acceptance update (2026-11-17): **Consecration115 accepted; stop after final push.** "
          f"Actual GPT response `{acceptance['gptResponseId']}` and Codex agreement accept frozen C#/console `{SOURCE}` "
          f"with evidence candidate `{acceptance['candidateCommit']}`. The composite 1,587-case regression, two explicit corrections, "
          "five complete 428-command paths and 784 cross-path comparisons are retained in the [final packet](evidence/2026-11-17-chr05-consecration/README.md). "
          "Prior TAC-10 acceptance was preserved without restarting its qualification. The genuine combined cap/cure intersection remains UNPROVED under the accepted mechanical allocation; "
          "CG-CONTEXT-01 remains a broader required integration gap. CHR-05 and the full engine remain incomplete; reference performance, production and Unity remain unqualified. "
          "The owner directs stop after this push: no next module, Unity integration, storage cleanup or Support action. Earlier status paragraphs below are historical.")
for name in ['DEVELOPMENT_HANDOFF.md', 'IMPLEMENTATION_TRACE.md']:
    path = ROOT / 'docs/unity' / name
    old = path.read_text(encoding='utf-8')
    first, rest = old.split('\n\n', 1)
    if not rest.startswith(update):
        path.write_text(first + '\n\n' + update + '\n\n' + rest, encoding='utf-8', newline='\n')
report = {'status': 'PASS_DOCUMENTATION_STRUCTURE_ONLY', 'workstreams': 49, 'directEdges': 120,
          'originalCriteriaPreserved': 49, 'completionObligationsPreserved': 100,
          'priorEvidenceLinksPreserved': True, 'completionContractUnchanged': True,
          'readinessStatusesAndClosureCriteriaUnchanged': True, 'updatedReadinessProgressNarratives': ['UR-02.remaining'],
          'changedAcceptedScopeRows': ['CHR-05'], 'noWholeWorkstreamPromoted': True,
          'sourceCommit': SOURCE, 'runtimeAccepted': True, 'statusSha256': sha(status_path), 'mapSha256': sha(map_path),
          'acceptanceSha256': sha(PACKET / 'FINAL_ACCEPTANCE.json'), 'rendererSha256': sha(legacy),
          'limits': 'Document reconciliation only. Gameplay claims refer to retained completed executions and actual bounded review.'}
(PACKET / 'FINAL_MAP_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS: bounded acceptance added; 49 workstreams, 120 edges, 100 completion obligations and all prior evidence preserved; successor held.')
