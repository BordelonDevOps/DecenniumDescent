"""Record the candidate without promoting discussion or passing tests to approval."""
from pathlib import Path
import json

audit=Path(__file__).resolve().parent
game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
p=root/'data/playtest/game_development_coverage.json'
backup=audit/'COVERAGE_BEFORE_TEMPORAL_CONTROL_WORLD_PROGRESS.json'
assert not backup.exists()
backup.write_bytes(p.read_bytes())
packet=json.loads(p.read_text(encoding='utf-8'))
candidate='DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json'
for row in packet['aspects']:
    if row['id'] not in ('DD-03','DD-08','DD-09','DD-16','DD-18','DD-21','DD-35','DD-63','DD-64'):continue
    row['validationEvidence']=list(dict.fromkeys(row['validationEvidence']+[candidate]))
    row['openIssues'].append('Live control/pulse holder restoration is a subsequent candidate under actual notebook review. Its current foundation extension is not covered by the archived foundation approval. Full source parents, final output application and all seven integrations remain open.')
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=game/'START_HERE.md'
text=p.read_text(encoding='utf-8')
old='Full control/pulse restoration is still in progress.'
assert old in text
text=text.replace(old,'The subsequent live-holder integration is under actual notebook review; its foundation extension has not inherited the earlier approval. Full control/pulse restoration is still in progress.',1)
p.write_text(text,encoding='utf-8')
note='''
## Live control/pulse transaction candidate submitted

[The actual 36-method submission](CODEX_TEMPORAL_CONTROL_WORLD_REVIEW.md) includes the complete new holder adapter, tests, and a diff from the preserved approved foundation. The original foundation is preserved byte-for-byte as `temporal_playtest_rules_reviewed_foundation.py`; approval still binds that original hash. The current extension also passes the 76 foundation and 22 payment/output checks. No old approval has been transferred to the extension.

The candidate binds selected actual holders to the atomic transaction, verifies aliases and original clocks, requires genuine regular starts, distinguishes target-start Hemostasis, and checks current parent receipts for Bloom/contact benefits. Whole-card/source-parent behavior, outside-initiative round import, final HP/resource mutation and several dependent source families remain unfinished. During review, the source audit also identified Eternal Bloom/Crown Restored's required concentration via `oracle.engine[26]`; a local corrective check is being added and will be included in the next actual packet.

The seven major temporal integrations and whole-game/GitHub gates remain open. No original content was deleted, no catalog status was promoted and no push occurred.
'''
for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_ADAPTER_ENGINEERING_NOTES.md'):
    p=audit/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
print('Recorded actual submission; no completion promotion.')
