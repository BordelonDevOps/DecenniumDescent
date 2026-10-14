"""Preserve the updated candidate after the initial review was interrupted."""
from pathlib import Path
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'
FILES = ('tools/temporal_playtest_rules.py', 'tools/validate_temporal_playtests.py',
         'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md', 'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json')

def main():
    target = AUDIT/'CODEX_TEMPORAL_KERNEL_REVIEW_V2.md'
    assert not target.exists(), 'Preserve actual submitted revision'
    parts = ['''# Resume the actual Time Loop kernel review: 52-test revision

Thank you for explaining the scope to the owner. The prior review did not produce a completed findings/approval response before that question. Please now complete the independent review of the actual updated code below. The owner authorized us to keep developing together. No whole-game approval or GitHub push is requested here.

While you reviewed, my own audit added six regressions and repaired physical root identity restoration, immutable provenance validation, per-restore before/after audit frames, the single canonical completed-rest epoch, current external max-HP record precedence and the original world-clock boundary. The original 46-test submitted packet remains preserved; THIS complete 52-test revision supersedes it for implementation review. All 52 tests pass locally.

Please report concrete reproducible defects and required repairs in the ADMITTED bounded fixture scope. Check conservation, atomic commit, stale-plan detection, same-ID one-shots, physical derivatives/outsiders, memory and scope claims. In particular check if a malformed or still-unclassified active record can silently get through this kernel. Do not claim full Time Loop closure: seven integrations remain explicitly unimplemented and playable_plan always rejects. Distinguish issues in this kernel from those openly missing integrations.

If there are no blockers within that limited scope, say so explicitly while keeping the full Time Loop and whole-game gates open. If blockers exist, give counterexamples so I can implement targeted repairs.
''']
    hashes = []
    for relative in FILES:
        raw = (ROOT/relative).read_bytes()
        hashes.append({'path':relative,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
        parts.append('\n## '+relative+'\n\n```\n'+raw.decode('utf-8')+'\n```\n')
    target.write_text('\n'.join(parts), encoding='utf-8')
    (AUDIT/'TEMPORAL_KERNEL_REVIEW_V2_MANIFEST.json').write_text(json.dumps({
        'status':'PREPARED; actual send and final response tracked separately', 'files':hashes,
        'packetBytes':target.stat().st_size, 'fullTimeLoopOperational':False,
    }, indent=2)+'\n',encoding='utf-8')
    print(str(target), target.stat().st_size)

if __name__ == '__main__':
    main()
