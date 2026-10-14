"""Record the actual bounded review without promoting the full ability."""
from pathlib import Path
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
GAME = AUDIT.parents[3]
ROOT = GAME/'DescentReviewChanges/ReviewBible'
REVIEWED_HASH = 'b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151'

def main():
    assert hashlib.sha256((ROOT/'tools/temporal_playtest_rules.py').read_bytes()).hexdigest() == REVIEWED_HASH
    closure = AUDIT/'GPT_TEMPORAL_KERNEL_FOUNDATION_CLOSURE.md'
    assert 'no remaining reproducible blocker' in closure.read_text(encoding='utf-8')
    report = json.loads((ROOT/'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json').read_text(encoding='utf-8'))
    status = {
        'status': 'REVIEWED / reference-VALIDATED bounded foundational transaction kernel',
        'helperSha256': REVIEWED_HASH,
        'independentEvidence': str(closure.relative_to(GAME)),
        'fullTimeLoopOperational': False,
        'remainingIntegrations': ['transformations', 'druid', 'creatures', 'devices', 'remaining-lifecycle', 'feats', 'control-pulses'],
        'wholeGameClosure': False,
        'githubPushed': False,
        'validation': report,
    }
    target = ROOT/'docs/mechanics/TEMPORAL_KERNEL_REVIEW_STATUS.json'
    assert not target.exists(), 'Closure already recorded'
    target.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    coverage_path = ROOT/'data/playtest/game_development_coverage.json'
    (AUDIT/'COVERAGE_BEFORE_TEMPORAL_KERNEL_CLOSURE.json').write_bytes(coverage_path.read_bytes())
    coverage = json.loads(coverage_path.read_text(encoding='utf-8'))
    for row in coverage['aspects']:
        if row['id'] not in ('DD-03','DD-08','DD-09','DD-21','DD-24','DD-27','DD-35','DD-63','DD-64'):
            continue
        row['openIssues'] = [x for x in row['openIssues'] if not x.startswith('Time Loop: twelve source boundaries settled; actual notebook review')]
        row['openIssues'].append('Time Loop: bounded foundational transaction kernel jointly reviewed with76 passing test methods; all nine independent findings resolved. Seven larger integrations remain missing and full playable activation stays disabled. No whole-domain closure.')
        row['reviewEvidence'] = list(dict.fromkeys(row['reviewEvidence'] + [str(closure.relative_to(GAME)).replace('\\','/')]))
    coverage_path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    guide = ROOT/'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md'
    text = guide.read_text(encoding='utf-8').replace('# Time Loop: foundational transaction candidate','# Time Loop: reviewed foundational transaction kernel')
    text = text.replace('**Status: implementation candidate, independent review pending. Full Time Loop remains unavailable.**','**Status: REVIEWED / reference-VALIDATED within the bounded foundational scope. Full Time Loop remains unavailable.**')
    text = text.replace('Those now have targeted repairs and six additional test methods; their independent confirmation is still pending.','Those repairs and six additional test methods received [actual independent closure](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_KERNEL_FOUNDATION_CLOSURE.md). The [review status](TEMPORAL_KERNEL_REVIEW_STATUS.json) binds that disposition to the exact helper hash; the submitted helper remains unchanged.')
    text = text.replace('Next, independently review this actual code and its narrow claims, repair defects, then add the seven missing integrations and exact source policies.','Next, add the seven missing integrations and exact source policies, with their own independent reviews.')
    guide.write_text(text,encoding='utf-8')
    nav = GAME/'START_HERE.md'
    text = nav.read_text(encoding='utf-8').replace('76 passing reference tests, and focused independent repair review in progress.','76 passing reference tests, and completed joint review of the bounded foundation.')
    text = text.replace('its implementation and independent review are now in progress.','its bounded foundation has completed joint review, while seven larger integrations remain unfinished.')
    nav.write_text(text,encoding='utf-8')
    note = '''
## Bounded temporal foundation jointly reviewed

The [actual completed GPT reply](GPT_TEMPORAL_KERNEL_FOUNDATION_CLOSURE.md) finds no remaining reproducible blocker in the admitted foundation. The [exact identity-repair diff](CODEX_TEMPORAL_KERNEL_IDENTITY_REPAIRS.md) resolves the three follow-up findings; the six earlier findings also remain resolved. All76 adversarial test methods pass. Reviewed helper SHA256: `b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151`.

This closes only the bounded foundational checkpoint. Seven real integrations remain: transformations/concentration, Druid, creatures, devices, remaining lifecycles, complete FeatWorld, and control/healing pulses. Full Time Loop stays unavailable and unpromoted. The final whole-game flow/GitHub gate remains open. No original was deleted and nothing was pushed.

A source scan confirms the existing healing ledger is the only other production helper directly reading `consumed_reducer_ids`; the temporal subclass overrides that commit method. FeatWorld uses returned canonical application IDs. This is compatibility evidence for the admitted interface, not proof of the still-missing full FeatWorld synchronization.
'''
    for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_KERNEL_REPAIR_LOG.md'):
        p = AUDIT/name
        p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
    print('Recorded actual bounded closure; source/helper unchanged; full feature remains gated.')

if __name__ == '__main__':
    main()
