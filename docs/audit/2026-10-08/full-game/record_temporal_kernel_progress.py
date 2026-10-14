"""Record actual intermediate implementation, preserving all earlier evidence."""
from pathlib import Path
import json

AUDIT = Path(__file__).resolve().parent
GAME = AUDIT.parents[3]
ROOT = GAME/'DescentReviewChanges/ReviewBible'

def main():
    path = ROOT/'data/playtest/game_development_coverage.json'
    before = AUDIT/'COVERAGE_BEFORE_TEMPORAL_KERNEL.json'
    assert not before.exists(), 'Intermediate implementation already recorded'
    assert (AUDIT/'gpt-temporal-kernel-review.png').exists()
    before.write_bytes(path.read_bytes())
    data = json.loads(path.read_text(encoding='utf-8'))
    for row in data['aspects']:
        if row['id'] not in ('DD-03','DD-08','DD-09','DD-21','DD-24','DD-27','DD-35','DD-63','DD-64'):
            continue
        row['openIssues'] = [x for x in row['openIssues']
                             if not x.startswith('Time Loop world transaction is source-discussed/draftable.')]
        row['openIssues'].append('Time Loop: twelve source boundaries settled. A bounded foundational transaction kernel has 46 passing adversarial test methods and was sent to the actual GPT notebook for independent review. Full playable activation remains disabled; transformation/Druid, creature/device/remaining lifecycle, full FeatWorld and control/pulse integrations are not yet implemented. No temporal closure.')
        row['sourceEvidence'] = list(dict.fromkeys(row['sourceEvidence'] + [
            'DescentReviewChanges/ReviewBible/tools/temporal_playtest_rules.py',
            'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md']))
        row['reviewEvidence'] = list(dict.fromkeys(row['reviewEvidence'] + [
            'docs/audit/2026-10-08/full-game/GPT_TEMPORAL_WORLD_BOUNDARIES.md',
            'docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_KERNEL_REVIEW.md']))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    note = '''
## Time Loop foundational kernel under actual notebook review

The [twelve temporal boundaries](GPT_TEMPORAL_WORLD_BOUNDARIES.md) are settled. The [actual intermediate code packet](CODEX_TEMPORAL_KERNEL_REVIEW.md), including 46 passing adversarial test methods and the precise unimplemented scope, was sent to Calibration Review. [Submission proof](gpt-temporal-kernel-review.png) is retained locally. This is an intermediate review, not Time Loop closure. Full playable activation remains explicitly disabled until the seven remaining integrations and final independent review exist. No original source was removed and no GitHub push occurred.
'''
    for name in ('README.md', 'REVIEW_STATUS.md'):
        path = AUDIT/name
        path.write_text(path.read_text(encoding='utf-8')+note, encoding='utf-8')
    path = AUDIT/'TEMPORAL_ADAPTER_ENGINEERING_NOTES.md'
    old = path.read_text(encoding='utf-8')
    old = old.replace('Implementation preparation only. The12 boundary decisions are still under GPT conference; no temporal rule or implementation is approved by this file.',
                      'Historical engineering preparation, followed by current implementation notes. The twelve boundary decisions are now captured in GPT_TEMPORAL_WORLD_BOUNDARIES.md. The foundational kernel is implemented and under independent review; the full temporal adapter set remains unfinished. This file is not independent approval.')
    path.write_text(old, encoding='utf-8')
    print('Recorded bounded kernel progress; no additional domain closed.')

if __name__ == '__main__':
    main()
