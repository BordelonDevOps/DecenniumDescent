"""Submit exact repairs for the six independent foundational findings."""
from pathlib import Path
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'

def main():
    target = AUDIT/'CODEX_TEMPORAL_KERNEL_REPAIRS.md'
    assert not target.exists(), 'Preserve the actual repair packet'
    intro = '''# Actual repairs for your six temporal-kernel findings

All six findings have targeted repairs and regression coverage. There are now 70 passing test methods. Please independently inspect the actual helper/tests/guide below and return the bounded repair disposition. This is still NOT a request for full Time Loop closure: the seven major integrations remain missing and playable_plan still always rejects.

1. Scheduler: regular_start requires the actor at initiative[cursor] and no active regular turn. regular_end validates the exact active TurnId, then advances cursor/round. Repeated or out-of-order starts cannot clear debts or increment real markers. A rewind clears only the active logical turn, not debts/global marker. Extra-turn sources remain outside this bounded kernel and cannot call this regular progression out of order.
2. Environment: each anchor requires matching physical identity; destroyed anchors cannot contribute blocking/support. Snapshot environment physical existence restores with its anchor. Retired post-snapshot derivatives lose both poses and anchors BEFORE geometry preflight. I reproduced the stale wall/support problem as two failing tests against the submitted52-test hash, preserved that failed report, then fixed it.
3. External dependencies: verify live presence AND exact same record/concentration for snapshot dependencies. Compare every new current dependency targeting a participant; permit only an actual supported max-HP overlay, otherwise reject. A missing dependency cannot hide behind an unchanged concentration string.
4. Maximum HP: replaced all monk-prefix inference with exact source-ID policies. Three actual trauma IDs restore; four actual permanent feat IDs conserve current records. Unsupported source policies and temporary endpoints on passive records reject. Correction to your reproducer: the pre-existing MaxHpRecord constructor already rejects the invented source 'some.participant.temporary.maxhp' and hypothetical passive 'monk.*' source; they are not constructible valid records. Its exact existing constructor/whitelist is included below. Nevertheless, a valid ordinary source such as wizard.engine[10] lacks a temporal/lifecycle adapter, so the new regression ensures it is rejected. The explicit table prevents future registry growth silently inheriting a policy.
5. BufferLedger: require every mandatory field and only the explicit optional ordinary_cast_events. Validate grant key/ID, unique active identity, mapped target, active state and positive remaining amount before capture and preflight.
6. Soul Bind: validate application/bind target identity, living dying0/non-Stable/non-Dead/no death ID for active pending; exact current dead instance for bound. Inactive expired historical records do not reactivate. Tests cover malformed state and a legitimate snapshot-dead bound target.

Please identify any remaining reproducible blocker in the admitted kernel. If these six are resolved, confirm that narrow disposition while leaving actual transformation/Druid/creature/device/remaining/feat/control-pulse integration, full Time Loop and whole-game GitHub gates open.
'''
    parts = [intro]; rows = []
    files = ('tools/temporal_playtest_rules.py', 'tools/validate_temporal_playtests.py',
             'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md', 'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json')
    for relative in files:
        raw = (ROOT/relative).read_bytes()
        rows.append({'path':relative,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
        parts.append('\n## '+relative+'\n\n```\n'+raw.decode('utf-8')+'\n```\n')
    source = ROOT/'tools/maximum_hp_playtest_rules.py'
    text = source.read_text(encoding='utf-8')
    excerpt = text[:text.index('\ndef effective_maximum(')]
    parts.append('\n## Existing maximum-HP whitelist and constructor (unchanged)\n\nSHA256 '+
                 hashlib.sha256(source.read_bytes()).hexdigest()+'\n\n```python\n'+excerpt+'\n```\n')
    target.write_text('\n'.join(parts), encoding='utf-8')
    (AUDIT/'TEMPORAL_KERNEL_REPAIRS_MANIFEST.json').write_text(json.dumps({
        'status':'PREPARED; actual submission/disposition recorded separately','files':rows,
        'packetBytes':target.stat().st_size,'fullTimeLoopOperational':False,
    },indent=2)+'\n',encoding='utf-8')
    print(str(target),target.stat().st_size)

if __name__ == '__main__':
    main()
