"""Prepare exact new history code for the existing notebook review."""
from pathlib import Path
import hashlib,json
audit=Path(__file__).resolve().parent
root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
out=audit/'CODEX_TEMPORAL_PARENT_HISTORY_REVIEW.md'
assert not out.exists()
parts=['''# Actual parent-operation history: implementation review

Following our ten parent policies and Action-budget/cadence clarification, this is the first necessary implementation layer: history over actual canonical Druid/TransformationWorld operations. It does not restore parent state and is not yet an admitted TemporalKernel integration. All seven larger domains remain open; do not treat these tests as full Time Loop validation.

It observes the existing real objects before their first form/cast, uses the host's exact wallet registry, pins actual form/cast/link/body/concentration identities, and emits creation/renewal/stabilization/ending receipts from completed native calls. It cannot import current expiry/permanent flags as history. Queries neither reactivate forms nor restore resources. Outside cast origins are explicit, and initiative operations require the actual scheduler atomic event ID/time. Real Druid regular starts use the global marker; the journal does not tick during history queries.

38 methods pass. Current ordinary form and transformation helpers, the 50+76+22 reviewed temporal files, and frozen class rules are unchanged. This does not inherit any approval for the new module.

Please review the exact code below for whether the receipts genuinely prove the source operations claimed, whether canonical references/history can be accidentally replaced, and whether failed calls can be mistaken for successful payments. The native helpers still own ordinary target/save/geometry legality. The journal records and refuses temporal admission after a native call that fails after changing parent state or an observed wallet/Druid economy; it cannot roll back committed casts or reroll failed host save resolvers. Two tests explicitly preserve those exceptional cases, including an existing special() clock advance before an unavailable Action rejects. No failed operation receives a success receipt.

Remaining implementation: proposed parent/concentration restoration, reference-safe atomic field staging, geometry/meld/current-inventory reconciliation, persistent slots, external effects, full creature/device/other parent closures, iteration-qualified ordinary wrappers, and composition with the already-reviewed control world. The ordinary wrappers here deliberately retain their non-temporal numeric turn arguments; they are observed history, not claimed replay-safe operational Time Loop APIs. Commands not handled through this layer and unobserved lifecycle changes reject its evidence validation. Final game-wide flow/GitHub gate remains open.

''']
hashes={}
for name in ('tools/temporal_parent_history.py','tools/validate_temporal_parent_history.py','docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json'):
    p=root/name;hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    parts.append(f'\n## Exact {name}\nSHA-256 `{hashes[name]}`\n\n```\n'+p.read_text(encoding='utf-8')+'\n```\n')
old=json.loads((root/'docs/mechanics/TEMPORAL_PARENT_REVIEW_STATUS.json').read_text())
for name,h in old['sourceCodeEvidenceHashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
parts.append('\n## Unchanged ordinary source hashes already supplied in the parent conference\n\n'+json.dumps(old['sourceCodeEvidenceHashes'],indent=2))
out.write_text(''.join(parts),encoding='utf-8')
(audit/'TEMPORAL_PARENT_HISTORY_SUBMISSION.json').write_text(json.dumps({'status':'38-method actual-operation journal pending independent review','hashes':hashes,'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False},indent=2)+'\n')
print(out.stat().st_size,'bytes prepared')
