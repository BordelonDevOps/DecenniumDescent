"""Render the resumed implementation map; no runtime execution or old evidence rewriting."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
legacy = ROOT / 'docs/unity/evidence/2026-11-17-implementation-map/Update-ImplementationMap.py'
spec = importlib.util.spec_from_file_location('accepted_map_renderer', legacy)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
status_path = ROOT / 'docs/unity/IMPLEMENTATION_STATUS.json'
current = json.loads(status_path.read_text())
baseline = json.loads(subprocess.check_output(['git', 'show', '15907773168d620d09fa084ea3cc111c5bd0bb35:docs/unity/IMPLEMENTATION_STATUS.json'], cwd=ROOT))
assert len(current['workItems']) == 49
assert sum(len(r['dependencies']) for r in current['workItems']) == 120
protected = ('id', 'title', 'dependencies', 'acceptance', 'currentStatus', 'wholeWorkstreamComplete', 'implementedOrAcceptedScope', 'evidence', 'completionCriteria')
for old, new in zip(baseline['workItems'], current['workItems']):
    for key in protected:
        assert old[key] == new[key], (new['id'], key)
assert sum(len(r['completionCriteria']) for r in current['workItems']) == 100
assert baseline['completionContract'] == current['completionContract']
assert baseline['frozenRuntime'] == current['frozenRuntime']
assert not current['activeImplementation']['runtimeAccepted']
text = renderer.render(current)
changes = {
    '**Unity gameplay integration is not ready. Development remains paused.** This update changes documentation only; it does not start the next module.': '**Unity gameplay integration is not ready. The owner resumed source-bound C# implementation.** The accepted baseline above is preserved; the active candidate below has separate qualification status.',
    '**Documentation review:**': '**Prior documentation review:**',
    'Actual final map review': 'Accepted planning-map review (before this implementation update)',
    'Source authority, prior exact acceptances and the owner hold remain unchanged.': 'Source authority and prior exact acceptances remain unchanged. The owner has resumed C# implementation; Unity and production gates remain.',
    '## Held next dependency': '## Active dependency',
    'return the complete amended two-card Consecration contract.': 'accepted amended two-card Consecration contract → implemented Consecration115 candidate → pending qualification/final review.',
    'The five terrain interpretations remain settled. The held contract must retain recharge registration,': 'The five terrain interpretations remain settled. The implemented candidate retains recharge registration,',
    'No such successor work is performed here.': 'Implementation is active; runtime acceptance remains pending.',
    'Every new implementation is held by the owner.': 'The owner resumed implementation under the existing source-bound consensus process.',
    '. Implementation is held.': '. The broader workstream remains incomplete.',
}
for before, after in changes.items():
    assert before in text, before
    text = text.replace(before, after)
active = current['activeImplementation']
paragraph = (f"**Active implementation:** {active['module']} at `{active['sourceCommit']}`. "
             f"**{active['status']}**. Source/API review is accepted; final module acceptance, whole-workstream closure, "
             "performance qualification and Unity readiness are not claimed. [Candidate packet](evidence/2026-11-17-chr05-consecration/README.md).\n\n")
text = text.replace('## Read this map\n', paragraph + '## Read this map\n', 1)
output = ROOT / 'docs/unity/IMPLEMENTATION_MAP.md'
output.write_text(text)
report = {'status': 'PASS_DOCUMENTATION_STRUCTURE_ONLY', 'workstreams': 49, 'directEdges': 120,
          'originalCriteriaPreserved': 49, 'completionObligationsPreserved': 100,
          'acceptedScopeAndEvidenceRecordsUnchanged': 49, 'priorAcceptancePointersUnchanged': True,
          'sourceCommit': active['sourceCommit'], 'runtimeAccepted': False,
          'statusSha256': hashlib.sha256(status_path.read_bytes()).hexdigest(),
          'mapSha256': hashlib.sha256(output.read_bytes()).hexdigest(),
          'rendererSha256': hashlib.sha256(legacy.read_bytes()).hexdigest(),
          'limits': 'Structural comparison/rendering only. Not a new source audit, gameplay test, historical-link audit or acceptance.'}
(PACKET / 'CURRENT_MAP_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS: 49 rows, 120 edges, 49 original criteria and 100 completion obligations preserved.')
