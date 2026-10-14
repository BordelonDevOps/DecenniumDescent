"""Bind the actual notebook closure to exactly the reviewed files."""
from pathlib import Path
import hashlib
import json

audit = Path(__file__).resolve().parent
game = audit.parents[3]
root = game / 'DescentReviewChanges/ReviewBible'
submission = json.loads((audit/'TEMPORAL_CONTROL_BINDING_REPAIR_SUBMISSION.json').read_text())
closure = audit/'GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md'
assert 'I confirm the bounded transaction checkpoint.' in closure.read_text(encoding='utf-8')
for name, digest in submission['hashes'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, name
manifest = {
    'status': 'REVIEWED / reference-VALIDATED bounded live control/healing-pulse transaction interface',
    'independentEvidence': str(closure.relative_to(game)).replace('\\','/'),
    'reviewedHashes': submission['hashes'],
    'testMethods': {'integration':50, 'foundation':76, 'paymentOutput':22, 'total':148},
    'fullControlPulseRestoration': False,
    'fullTimeLoopOperational': False,
    'remainingMajorIntegrations': 7,
    'wholeGameClosure': False,
    'githubPushed': False,
    'authorizationNote': 'The human already authorized GitHub delivery after joint whole-game flow confirmation. This bounded approval does not satisfy that condition.'
}
p = root/'docs/mechanics/TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json'
assert not p.exists()
p.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

p = root/'docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md'
text = p.read_text(encoding='utf-8')
text = text.replace('**Source policies discussed; implementation in progress. Full Time Loop remains unavailable.**', '**Bounded live control/pulse transaction interface jointly reviewed and reference-validated. Full Time Loop remains unavailable.**')
start = text.index('The new `tools/temporal_control_world.py` candidate')
end = text.index(' It restores selected same-object fields', start)
text = text[:start] + ('The `tools/temporal_control_world.py` integration passes 50 methods, alongside the 76 foundation and 22 payment/output methods. The [actual notebook closure](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md) confirms the bounded interface after four review rounds. Its [review manifest](TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json) binds the exact helper, tests and foundation extension; it does not transfer this approval to future edits.') + text[end:]
text = text.replace('All nine-family restoration remains in progress.', 'Complete nine-family/source restoration remains in progress.')
text = text.replace('[Candidate validation](TEMPORAL_CONTROL_WORLD_VALIDATION.json) is engineering evidence, not full Time Loop approval.', '[Validation](TEMPORAL_CONTROL_WORLD_VALIDATION.json) and the bounded approval do not certify full Time Loop.')
needle = 'No original missing-HP reserve or share is recomputed.'
text = text.replace(needle, needle + '\n\nSnapshot concentration bindings include the actual owner, concentration ID, slot object and callback object. Retained references prevent identity-token reuse. A same-ID replacement, even with the same callback or subsequently registered components, rejects before writes. This preserves the original later-ending callback; it does not restore ended/replaced concentration.')
p.write_text(text,encoding='utf-8')

p = root/'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md'
text = p.read_text(encoding='utf-8')
text = text.replace('Those extensions are a subsequent review candidate, not covered by that historical approval. The 76 foundation regressions still pass.', 'Those extensions are now covered by the separate [bounded control/pulse review manifest](TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json), following actual notebook confirmation. They do not inherit the historical approval. The 76 foundation regressions still pass.')
text = text.replace('the submitted helper remains unchanged.', 'the originally submitted helper is preserved in the audit archive; the later extension has its own review manifest.')
text = text.replace('nine source-policy families discussed and22 payment/output checks jointly reviewed.', 'nine source-policy families discussed,22 payment/output checks and50 bounded live-holder transaction methods jointly reviewed.')
p.write_text(text,encoding='utf-8')

p = game/'START_HERE.md'
text = p.read_text(encoding='utf-8')
old = 'The subsequent live-holder integration is under actual notebook review; its foundation extension has not inherited the earlier approval.'
assert old in text
text = text.replace(old, 'The subsequent live-holder transaction interface has also completed joint review:50 integration methods pass (148 across the three suites), with its foundation extension covered by an exact separate review manifest.')
p.write_text(text,encoding='utf-8')

p = root/'data/playtest/game_development_coverage.json'
backup = audit/'COVERAGE_BEFORE_TEMPORAL_CONTROL_WORLD_CLOSURE.json'
assert not backup.exists()
backup.write_bytes(p.read_bytes())
packet = json.loads(p.read_text(encoding='utf-8'))
for row in packet['aspects']:
    if row['id'] not in ('DD-03','DD-08','DD-09','DD-16','DD-18','DD-21','DD-35','DD-63','DD-64'): continue
    row['validationEvidence'] = list(dict.fromkeys(row['validationEvidence'] + [str(closure.relative_to(game)).replace('\\','/'), 'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json']))
    row['openIssues'] = [x for x in row['openIssues'] if not x.startswith('Live control/pulse holder restoration is a subsequent candidate')]
    row['openIssues'].append('The bounded live control/pulse transaction interface and exact foundation extension are jointly reviewed (50+76+22 methods). Complete source parents, final output application and all seven larger temporal integrations remain open.')
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

note = '''
## Bounded live control/pulse transaction closure

The [actual GPT response](GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md) confirms the exact 50-method revision after the [callback-binding repair](CODEX_TEMPORAL_CONTROL_BINDING_REPAIR.md). It accepts all three same-ID replacement rejection cases and keeps the previous clock, admission, collection, shared-output and Bloom repairs closed. The separate `TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json` binds the exact live adapter, tests, foundation extension and unchanged payment bridge. 50 integration +76 foundation +22 payment/output methods pass.

This closes this bounded engineering checkpoint only. Complete source/parent lifecycles, final HP/Ki/Conviction application, all seven major Time Loop integrations, the full feature and whole-game flow review remain open. The human's conditional GitHub authorization persists; GPT's reference to an authorization gate is recorded as its own wording, not a request for renewed human permission. No original source was deleted and no GitHub push occurred.
'''
for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_ADAPTER_ENGINEERING_NOTES.md','TEMPORAL_CONTROL_WORLD_REPAIR_LOG.md'):
    p = audit/name
    p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
print('Actual bounded closure recorded; broad completion counts unchanged.')
