"""Record discussed/implemented candidate work, never infer review closure."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
review=['docs/audit/2026-10-08/full-game/'+n for n in ('GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md','GPT_TRANSFORMATION_SPELL_BOUNDARIES.md','GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md')]
for row in data['aspects']:
    if row['id'] not in ('DD-08','DD-11','DD-12','DD-21','DD-24','DD-26','DD-27','DD-35'):continue
    assert row['closure']=='open'
    for key,values in [('reviewEvidence',review),('draftEvidence',['DescentReviewChanges/ReviewBible/docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md']),
                       ('validationEvidence',['DescentReviewChanges/ReviewBible/docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json'])]:
        row[key]=list(dict.fromkeys(row.get(key,[])+values))
    note='Five-spell candidate implemented with12 finite profiles,191 contract checks and729 Mass spatial scenarios. Actual implementation submitted to GPT; independent review/catalog promotion pending. This is not whole-domain closure.'
    if note not in row['openIssues']:row['openIssues'].append(note)
    if row['id']=='DD-21':
        note='Mandatory-reversion geometry conflict: return root anatomy at same anchor, expose placementConflict and prohibit free relocation/barrier traversal; canonical conflict-resolution procedure still requires a dedicated source conference.'
        if note not in row['openIssues']:row['openIssues'].append(note)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name;text=path.read_text(encoding='utf-8')
    marker='## Five-spell candidate implementation submitted'
    if marker not in text:
        text+='\n'+marker+'\n\n[Actual candidate packet](CODEX_TRANSFORMATION_SPELL_IMPLEMENTATION.md) was visibly submitted after [twelve boundaries](GPT_TRANSFORMATION_SPELL_BOUNDARIES.md) and [seven final interfaces](GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md). Five candidate spells,12 profiles,191 checks and729 occupancy scenarios are implemented. Existing form regression165/1053 passes. Active catalog remains78/770 pending independent review. Source originals and frozen class rules are unchanged. Same-anchor mandatory-reversion geometry remains an explicit broader dependency. The eight-feat completion packet remains prepared, not submitted.\n'
        path.write_text(text,encoding='utf-8')
print('Recorded candidate work and explicit geometry dependency; no review or domain closure inferred.')
