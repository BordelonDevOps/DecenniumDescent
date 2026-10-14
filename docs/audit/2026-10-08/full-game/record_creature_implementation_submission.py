from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
coverage=json.loads(path.read_text(encoding='utf-8'))
for ident in ('DD-24','DD-35'):
    row=next(r for r in coverage['aspects'] if r['id']==ident)
    row['closure']='open'
    for field,value in (
        ('reviewEvidence','docs/audit/2026-10-08/full-game/GPT_CREATURE_LIFECYCLE_BOUNDARIES.md'),
        ('reviewEvidence','docs/audit/2026-10-08/full-game/GPT_CREATURE_LIFECYCLE_EVENT_BOUNDARIES.md'),
        ('draftEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md'),
        ('draftEvidence','docs/audit/2026-10-08/full-game/CODEX_CREATURE_LIFECYCLE_IMPLEMENTATION_COMPACT.md'),
        ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json')):
        if value not in row[field]:row[field].append(value)
    note='Five-family creature candidate:100 exact passages+5 frozen supports discussed;105 checks/2,800 Ranger conversion states pass. Visible notebook implementation review pending; full forms/tempHP and Wizard elite binding/return remain open.'
    if note not in row['openIssues']:row['openIssues'].append(note)
path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name;text=path.read_text(encoding='utf-8')
    note='\n## Creature lifecycle implementation submitted\n\n100 exact five-family passages plus5 supports are discussed in three preserved notebook replies. The [candidate guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md), helper and105 checks/2,800 Ranger conversion states are saved. [Exact compact review](CODEX_CREATURE_LIFECYCLE_IMPLEMENTATION_COMPACT.md) was visibly submitted through Chrome as a pasted text attachment after connector sends did not appear in persisted history. [Submission evidence](gpt-creature-review-submitted.png). Await exact review; no closure. The original230-candidate lexical inventory has74 as-yet-unsupplied passages retained in [remaining source snapshot](REMAINING_LIFECYCLE_SOURCE_CANDIDATES.json); this is not a completeness claim.\n'
    if '## Creature lifecycle implementation submitted' not in text:text+=note
    path.write_text(text,encoding='utf-8')
print('Recorded candidate submission; no aspect or full card promoted to closed.')
