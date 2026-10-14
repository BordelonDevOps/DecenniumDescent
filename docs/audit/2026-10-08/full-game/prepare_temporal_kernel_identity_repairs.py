"""Build an exact small diff against the already-reviewed 70-test packet."""
from pathlib import Path
import hashlib
import difflib
import json
import re

AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'

def main():
    target=AUDIT/'CODEX_TEMPORAL_KERNEL_IDENTITY_REPAIRS.md'
    assert not target.exists(), 'Preserve submitted repair packet'
    # Reverse exactly the packet writer's one Windows newline-conversion pass.
    # Universal-newline reading would also erase CRLF in embedded source files.
    previous=(AUDIT/'CODEX_TEMPORAL_KERNEL_REPAIRS.md').read_bytes().decode('utf-8').replace('\r\n','\n')
    manifest=json.loads((AUDIT/'TEMPORAL_KERNEL_REPAIRS_MANIFEST.json').read_text(encoding='utf-8'))
    parts=['''# Exact fixes for the three identity/admission findings

Thank you for confirming the original six repairs. The remaining three now have targeted fixes and regressions; all76 methods pass. This packet is an exact verified unified diff against the complete70-test helper/tests/guide you just reviewed. The original packet and hashes are preserved. There are no unshown edits to these files.

1. Public regular-start API is now TemporalKernel.regular_start(actor, now). It obtains self.wallets[actor] internally, accepts NO wallet argument, and rejects actors aliasing one Wallet. Scheduler._regular_start is private implementation only; the unsafe public scheduler.regular_start entry point is removed. All existing tests use the public world wrapper. A new regression tries supplying B's actual Wallet for A and confirms rejection without mutation, then confirms a proper A start leaves B's Reaction/debt untouched.
2. Capture and preflight now independently validate EVERY live one-shot record, even if inserted directly without register(): exact key/ID/source, original absolute Agony clock/no rest substitute, canonical scene owner/target and boolean availability. History validates set/token/event shapes, nonfuture iterations, corresponding committed event evidence and no duplicate consumption pair. An available record cannot simultaneously be consumed in the current generation. Sixteen direct-malformation subcases cover capture/preflight plus dedicated conflicting-history cases.
3. Every ExternalEffect dictionary key must equal its identity, and maximum-HP entries must match record application/owner/target. New dependency satisfaction also explicitly requires dep.effect_id == effect.identity. Tests cover both capture and preflight with and without a misleading dependency lookup key.

Please confirm whether the three findings are resolved in this admitted scope, or give any remaining reproducible blocker. This is only a bounded foundational checkpoint: playable_plan remains unavailable, seven source integrations remain absent, and whole-game/GitHub gates remain open.
''']
    rows=[]
    for entry in manifest['files']:
        relative=entry['path']
        pattern=r'\n## '+re.escape(relative)+r'\n\n```\n(.*?)\n```\n'
        match=re.search(pattern,previous,re.S)
        assert match, relative
        before=match.group(1)
        assert hashlib.sha256(before.encode('utf-8')).hexdigest()==entry['sha256'], 'Old packet/hash mismatch: '+relative
        after=(ROOT/relative).read_bytes().decode('utf-8')
        diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='reviewed70/'+relative,tofile='current76/'+relative))
        rows.append({'path':relative,'beforeSha256':entry['sha256'],'afterSha256':hashlib.sha256(after.encode()).hexdigest()})
        parts.append('\n## '+relative+'\n\n```diff\n'+diff+'\n```\n')
    target.write_bytes('\n'.join(parts).encode('utf-8'))
    (AUDIT/'TEMPORAL_KERNEL_IDENTITY_REPAIRS_MANIFEST.json').write_text(json.dumps({
        'status':'PREPARED; actual send/disposition tracked separately','files':rows,
        'packetBytes':target.stat().st_size,'fullTimeLoopOperational':False,
    },indent=2)+'\n',encoding='utf-8')
    print(str(target),target.stat().st_size)

if __name__=='__main__':main()
