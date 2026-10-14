"""Record actual approval of reference transport without claiming parent restoration."""
from pathlib import Path
import hashlib,json
audit=Path(__file__).resolve().parent;game=audit.parents[3];root=game/'DescentReviewChanges/ReviewBible'
evidence='docs/audit/2026-10-08/full-game/GPT_TEMPORAL_REFERENCE_TRANSACTION_CLOSURE.md'
reply=(game/evidence).read_text(encoding='utf-8')
assert 'bounded exact-reference transport checkpoint' in reply and 'REVIEWED / reference-VALIDATED' in reply
submission=json.loads((audit/'TEMPORAL_REFERENCE_TRANSACTION_SUBMISSION.json').read_text())
for name,h in submission['hashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
status=dict(submission);status.update({
 'status':'REVIEWED / reference-VALIDATED — exact original form/concentration reference transport through the existing atomic Transaction only',
 'independentEvidence':evidence,'reviewedHashes':submission['hashes'],
 'priorFoundationArchive':'docs/audit/2026-10-08/full-game/temporal_playtest_rules_control_checkpoint.py',
 'parentRuntimeIntegrated':False,'wholeGameClosure':False,'githubPushed':False,
 'requiredNext':'Watch/stage complete form/Cast/Link/body/buffer/geometry/inventory/dependency closures; transport alone certifies no source legality.'})
p=root/'docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json';assert not p.exists()
p.write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
p=root/'docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md';text=p.read_text(encoding='utf-8')
text=text.replace('Reference-safe callback staging, full dependency reconciliation, temporal turn wrappers and integration with the existing kernel remain required below.',
 'The [reference-transport extension](TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json) is now jointly reviewed with 15 new checks and 207 regression checks. It carries exact original FormInstance and concentration slot/callback references in the same atomic transaction, including rollback. It certifies identity transport only. Full source planning, dependency reconciliation, temporal turn wrappers and kernel integration remain required below.')
p.write_text(text,encoding='utf-8')
p=root/'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md';text=p.read_text(encoding='utf-8')
text+='\nThe [exact-parent reference transport extension](TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json) is now jointly reviewed:15 new checks plus the existing207 pass. The prior control-checkpoint foundation is preserved at `docs/audit/2026-10-08/full-game/temporal_playtest_rules_control_checkpoint.py`; the current kernel hash has its own explicit review manifest. Only identity transport/rollback is added. Active form admission and full parent restoration remain gated.\n'
p.write_text(text,encoding='utf-8')
p=game/'START_HERE.md';text=p.read_text(encoding='utf-8')
text=text.replace('This establishes reliable source history; it does not yet restore forms or concentration.',
 'This establishes reliable source history. The subsequent [atomic reference-transport extension](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json) also passed joint review with 15 new checks and 207 regression checks. Complete form/concentration restoration remains next.')
p.write_text(text,encoding='utf-8')
p=root/'data/playtest/game_development_coverage.json';packet=json.loads(p.read_text(encoding='utf-8'))
for row in packet['aspects']:
    if any('Parent operation-history journal jointly reviewed with59 checks' in issue for issue in row['openIssues']):
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[evidence]))
        row['validationEvidence']=list(dict.fromkeys(row['validationEvidence']+[
         'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_VALIDATION.json',
         'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json']))
        row['openIssues']=[issue.replace('all six evidence findings resolved.',
          'all six evidence findings resolved. Exact-reference transaction transport also reviewed with15 new checks and207 regressions; source legality remains the complete planner responsibility.') for issue in row['openIssues']]
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
note='''
## Original-reference transaction transport closed

The notebook [confirmed exact-reference staging](GPT_TEMPORAL_REFERENCE_TRANSACTION_CLOSURE.md) after 15 targeted checks and the existing207 checks passed. The same Transaction now transports exact Druid.current and concentration slot/callback references, detects stale bindings and rolls back exact original references on a later failure. No callbacks run at commit or rollback. The [manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json) binds this extension to the current foundation hash; the former reviewed foundation is preserved intact in temporal_playtest_rules_control_checkpoint.py.

This completes the transport prerequisite, not parent source planning. Full mutable source/dependency/gear/geometry watches and an integrated legal restore remain required. Seven major integrations remain open; no game content was deleted or pushed.
'''
for name in ('REVIEW_STATUS.md','TEMPORAL_PARENT_INTEGRATION_NEXT.md'):
 p=audit/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
print('Recorded reviewed reference transport; complete parent planning remains open.')
