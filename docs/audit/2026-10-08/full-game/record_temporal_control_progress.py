"""Record completed policy discussion and incomplete implementation honestly."""
from pathlib import Path
import json

AUDIT=Path(__file__).resolve().parent
GAME=AUDIT.parents[3]
ROOT=GAME/'DescentReviewChanges/ReviewBible'

def main():
    path=ROOT/'data/playtest/game_development_coverage.json'
    prior=AUDIT/'COVERAGE_BEFORE_TEMPORAL_CONTROL_PROGRESS.json'
    assert not prior.exists()
    prior.write_bytes(path.read_bytes())
    data=json.loads(path.read_text(encoding='utf-8'))
    evidence='docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md'
    draft='DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md'
    for row in data['aspects']:
        if row['id'] not in ('DD-03','DD-08','DD-09','DD-16','DD-18','DD-21','DD-35','DD-63','DD-64'):continue
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[evidence]))
        row['draftEvidence']=list(dict.fromkeys(row['draftEvidence']+[draft]))
        row['openIssues'].append('Temporal control/pulse source conference completed for nine holder families. Canonical payment and resolved Ki/Conviction-output guards pass22 focused tests and await independent code review. Source-clock/parent restoration and native receipts remain unfinished; Rapid Coagulation needs snapshot movement history. No full temporal integration or whole-domain closure.')
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    note='''
## Temporal control/pulse source conference completed; code review in progress

The [actual nine-part response](GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md) settles the source policies. Sacred Chant's Conviction joins Transcendent Meditation's Ki under a conserved independent-output opportunity. Native healing gets one evaluated opportunity at a real regular start; declined, ineligible or unaffordable starts cannot be retried. Rapid Coagulation remains dependent on a missing movement-history adapter.

The [actual incremental code packet](CODEX_TEMPORAL_PULSE_BRIDGE_REVIEW.md) contains22 passing payment/output tests and explicit limits. It asks the notebook to confirm ordinary maintenance retry wording and immutable initiative-start membership. It does not implement full pulse restoration or reduce the seven missing integrations. The current readable guide is `DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md`. No source promotion, deletion or GitHub push occurred.
'''
    for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_ADAPTER_ENGINEERING_NOTES.md'):
        p=AUDIT/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
    p=GAME/'START_HERE.md'
    text=p.read_text(encoding='utf-8')
    text=text.replace('The full Time Loop integration and whole-game candidate remain unfinished.',
        'The [control/healing-pulse source conference](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md) is complete; its first22 payment/output checks pass and independent code review is in progress. The full Time Loop integration and whole-game candidate remain unfinished.')
    p.write_text(text,encoding='utf-8')
    print('Recorded actual source conference and22-check implementation candidate; no full integration closure.')

if __name__=='__main__':main()
