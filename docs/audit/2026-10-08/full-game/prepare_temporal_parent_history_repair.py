"""Preserve the reviewed submission and submit exact repairs for the four findings."""
from pathlib import Path
import difflib,hashlib,json,re

audit=Path(__file__).resolve().parent
root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
original=(audit/'CODEX_TEMPORAL_PARENT_HISTORY_REVIEW.md').read_text(encoding='utf-8')
out=audit/'CODEX_TEMPORAL_PARENT_HISTORY_REPAIR.md'
assert not out.exists()
parts=['''# Parent history repair: all four actual review findings

Your completed 38-method review is preserved verbatim in GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md. I agree with its four findings. I independently reproduced the fake level-20 free renewal and fabricated zero-price cast before changing the code (TEMPORAL_PARENT_HISTORY_AUTHORITY_PROBES.json).

The repaired candidate has 55 passing methods. This remains an actual-operation history layer only, with no restoration, no admission to TemporalKernel, no full Time Loop and no whole-game closure. All seven larger integration domains remain open.

1. The constructor binds canonical DruidStats and frozen CasterAuthority roots (CastStats, class level, max RP, signed modifier, current known/prepared repertoire, shared cadence dict). Per-call substitute stat objects reject. Ordinary prices are rederived from the actual catalog and unchanged quote_cast immediately before casting; the complete supplied price/quote must agree. Unsupported class discounts, free copies, trauma casting and all post-cast class cadence hooks remain outside this narrow ordinary-price interface. The host still owns the actual character roots, component/target/geometry legality and actual saves. Quoting does not claim to apply the full class casting transaction.
2. A separate persistent finite-state projection binds every Druid-owned resource/rest/attunement/recharge field you listed, including the complete clock. It is checked before operations/queries and updated only after observed native calls. Shared cadence remains current and may change through the class interface. The recharge test now anchors its clock through a real observed special rather than an unobserved fixture mutation.
3. The operation-to-transition matrix restricts form creation/renewal/endings, cast/link creation, stabilization/endings and concentration changes to the exact recorded actor, requested source identity/targets, old source closure, native reason and checkpoint. Unexpected transitions produce a failed event, no successful receipts and poisoned admission. Receipts include their operation and event ID. A save-resolver guard additionally forbids nested parent/source-economy changes during a save; the demonstrated native Druid entry callback is detected before it can be laundered into the cast. Tests independently inject faulty helper bodies to exercise the matrix without relying on that guard. Legitimate concentration replacement, same-target replacement and spell-ending-Druid cases remain admitted.
4. All generic outside events use OUTSIDE_EVENT with operation/time. Only a successful cast-created receipt gets OUTSIDE_CAST. The outside Druid entry/renewal tests verify this distinction.

No second shield world was added. Historical shield amounts/IDs/dependencies remain the canonical Buffer adapter's responsibility. Ordinary transformation/Druid source helpers, the previously reviewed control/pulse interface and frozen rules are unchanged.

Please review the exact repair for reproducible remaining defects within this bounded source-history scope. If sound, confirm only this checkpoint, keeping restoration, replay-safe wrappers and all larger integrations open.
''']
hashes={}
for name in ('tools/temporal_parent_history.py','tools/validate_temporal_parent_history.py'):
    current=(root/name).read_text(encoding='utf-8')
    section=original.split('## Exact '+name+'\n',1)[1]
    old=section.split('```\n',1)[1].split('\n```',1)[0]
    parts.append('\n## Repair diff: '+name+'\n\n```diff\n'+''.join(difflib.unified_diff(old.splitlines(True),current.splitlines(True),fromfile='reviewed-38/'+name,tofile='repair-55/'+name))+'\n```\n')
for name in ('tools/temporal_parent_history.py','tools/validate_temporal_parent_history.py','docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json','tools/spell_playtest_rules.py'):
    p=root/name;hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    parts.append(f'\n## Exact {name}\nSHA-256 `{hashes[name]}`\n\n```\n'+p.read_text(encoding='utf-8')+'\n```\n')
prior=json.loads((root/'docs/mechanics/TEMPORAL_PARENT_REVIEW_STATUS.json').read_text())
for name,h in prior['sourceCodeEvidenceHashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
parts.append('\n## Unchanged source hashes\n\n'+json.dumps(prior['sourceCodeEvidenceHashes'],indent=2))
out.write_text(''.join(parts),encoding='utf-8')
(audit/'TEMPORAL_PARENT_HISTORY_REPAIR_SUBMISSION.json').write_text(json.dumps({
    'status':'55-method four-finding repair awaiting actual notebook review',
    'hashes':hashes,'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),
    'actualReview':'GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md','parentRuntimeIntegrated':False,
    'fullTimeLoopOperational':False,'remainingMajorIntegrations':7},indent=2)+'\n')
print(out.stat().st_size,'bytes prepared')
