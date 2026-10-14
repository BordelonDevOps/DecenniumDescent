"""Submit the atomic parent-reference transport extension with exact evidence."""
from pathlib import Path
import hashlib,json,difflib
audit=Path(__file__).resolve().parent;root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
before=audit/'temporal_playtest_rules_control_checkpoint.py'
assert hashlib.sha256(before.read_bytes()).hexdigest()=='45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577'
current=root/'tools/temporal_playtest_rules.py';out=audit/'CODEX_TEMPORAL_REFERENCE_TRANSACTION_REVIEW.md'
assert not out.exists()
parts=['''# Atomic transport of the exact original parent references

The actual 59-method history closure is recorded. The next necessary parent restoration component is exact-reference staging in the EXISTING Transaction. The prior reviewed transaction accepted only copied data values; concentration contains callbacks and Druid.current must remain the original FormInstance. Copying either would violate the ten source policies.

This is an extension to the existing common transaction, not a separate commit mechanism. It adds only two specific write paths: canonical Druid.current (original registered instance or None), and ConcentrationLedger.current (a shallow map whose slot tuples must be the originals in the supplied retained-slot registry). They share the same write-conflict namespace, all-before-write stale checks, one commit and rollback. No callback, cast, entry or ending helper runs at commit. Prepared concentration maps are detached from the input map; exact slot/callback objects remain shared and pinned. Reference audit rows store object tokens rather than trying to serialize callbacks.

This layer provides identity transport, not source legality. The future parent planner must still prove complete original closures, valid clocks, paid renewal/stabilization history, nonparticipant protection, current suppression, gear/inventory/enrollment/geometry reconciliation and dependent shield/creature state. A transport-only test deliberately demonstrates that clearing Druid.current alone does NOT run ordinary child cleanup: that cleanup must be explicitly staged by the complete planner.

15 new tests pass. They cover exact original form and concentration objects, rejection of equal-looking replacements, stale current/instance/retained registries, edited prepared maps, shared conflict checks, no entry payment, no ending hook at commit, rollback of data and exact original references after an injected later assignment failure, and a subsequent REAL concentration ending reaching the original TransformationWorld link. Existing suites also pass:76 foundation +22 payment/output +50 control/pulse +59 history, 222 total including these15. No active form is yet admitted to the kernel; full Time Loop remains disabled and all seven larger integrations remain open.

The previous exact foundation is preserved separately at temporal_playtest_rules_control_checkpoint.py. Its historical approval is not silently inherited by this extension. Ordinary source helpers and the actual history module are unchanged.

Please inspect this exact transaction diff and regression evidence for atomicity/reference defects. Confirm only reference transport if sound. Parent planning and full game/GitHub flow are still open.
''']
parts.append('\n## Exact full-file diff\n\n```diff\n'+''.join(difflib.unified_diff(
 before.read_text(encoding='utf-8').splitlines(True),current.read_text(encoding='utf-8').splitlines(True),
 fromfile='reviewed-control-checkpoint/temporal_playtest_rules.py',tofile='reference-candidate/temporal_playtest_rules.py'))+'\n```\n')
text=current.read_text(encoding='utf-8');start=text.index('def data(');end=text.index('@dataclass(frozen=True)\nclass RoundId')
parts.append('\n## Complete current value-copy and transaction code\n\n```python\n'+text[start:end]+'\n```\n')
hashes={'tools/temporal_playtest_rules.py':hashlib.sha256(current.read_bytes()).hexdigest()}
for name in ('tools/validate_temporal_reference_transactions.py','docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_VALIDATION.json',
 'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json','docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json'):
 p=root/name;hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 parts.append('\n## Exact '+name+'\nSHA-256 `'+hashes[name]+'`\n\n```\n'+p.read_text(encoding='utf-8')+'\n```\n')
out.write_text(''.join(parts),encoding='utf-8')
(audit/'TEMPORAL_REFERENCE_TRANSACTION_SUBMISSION.json').write_text(json.dumps({
 'status':'15-method reference transport candidate pending notebook review','hashes':hashes,
 'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'testMethods':{'reference':15,'foundation':76,'payment':22,'control':50,'history':59,'total':222},
 'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False,'remainingMajorIntegrations':7},indent=2)+'\n')
print(out.stat().st_size,'bytes prepared')
