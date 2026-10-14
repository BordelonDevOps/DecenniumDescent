"""Record actual sent candidate; preserve prior ledger before updating active status."""
from pathlib import Path
import json

AUDIT=Path(__file__).resolve().parent
GAME=AUDIT.parents[3]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
assert (AUDIT/'gpt-buffer-feat-implementation.png').exists()
path=ROOT/'data/playtest/game_development_coverage.json'
snapshot=AUDIT/'COVERAGE_BEFORE_BUFFER_FEAT_CANDIDATE.json'
assert not snapshot.exists(),'Status checkpoint already recorded'
snapshot.write_bytes(path.read_bytes())
coverage=json.loads(path.read_text(encoding='utf-8'))
for row in coverage['aspects']:
    issues=[]
    for issue in row['openIssues']:
        issue=issue.replace('78 individual spell drafts reviewed;770 unfinished.',
                            '83 individual spell drafts reviewed;765 unfinished.')
        issue=issue.replace('Five named transformation/buffer spell source conference is in progress.',
                            'Five named transformation/buffer spells are reviewed and provisionally promoted; broader catalog work remains.')
        old='Form/tempHP175+5 source conference submitted; source integrity passes, individual discussion and implementation pending. Complete original Druid corpus plus explicit/semantic other class, Bard, feat, spell and recovered ancestry candidates. No whole-card/catalog completion implied.'
        issue=issue.replace(old,'The175+5 form/tempHP interface is reviewed; finish remaining full-option clauses and Time Loop world conservation. No whole-card/catalog completion implied.')
        if issue.startswith('Eight complete source-discussed feat proposals exist:'):
            issue='Eight full feat candidates now have reconciled dependency decisions, implementation and local validation (131 checks/2,520 funding cases). Actual code review was sent to GPT and is pending; no feat promoted. Complete the remaining327 source objects separately.'
        issues.append(issue)
    row['openIssues']=issues
    if row['id']=='DD-14':
        row['status']='eight-full-feat-candidates-in-implementation-review'
        for field,paths in {
            'sourceEvidence':['docs/audit/2026-10-08/full-game/BUFFER_FEAT_COMPLETION_SOURCES.json',
                              'docs/audit/2026-10-08/full-game/BUFFER_FEAT_DEPENDENCY_SOURCES.json'],
            'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_BOUNDARIES.md',
                              'docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FINAL_BRIDGES.md'],
            'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/BUFFER_FEAT_PLAYTEST.md',
                             'DescentReviewChanges/ReviewBible/data/playtest/feat_drafts/candidate_buffers.json'],
            'validationEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/BUFFER_FEAT_PLAYTEST_VALIDATION.json',
                                  'DescentReviewChanges/ReviewBible/docs/mechanics/BUFFER_FEAT_SOURCE_VALIDATION.json']}.items():
            row[field]=list(dict.fromkeys(row[field]+paths))
path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=AUDIT/name;text=path.read_text(encoding='utf-8')
    text+='\n## Eight-feat complete candidate implementation submitted\n\nThe full Chef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and Soul Cage candidates now incorporate the [15 dependency decisions](GPT_BUFFER_FEAT_BOUNDARIES.md) and [five final bridges](GPT_BUFFER_FEAT_FINAL_BRIDGES.md). The [actual implementation packet](CODEX_BUFFER_FEAT_IMPLEMENTATION.md) was visibly sent to Calibration Review. Local validation passes131 targeted checks and2,520 healing-funding boundary cases. The original335 feat objects and legacy text remain unchanged. No feat is promoted; independent review is pending, and the remaining327 feats stay open.\n'
    if name=='REVIEW_STATUS.md':
        text=text.replace('1,223 class cards; 78 ordinary spell drafts reviewed,770 still unfinished.',
                          '1,223 class cards;83 ordinary spell drafts reviewed,765 still unfinished.')
    path.write_text(text,encoding='utf-8')
print('Eight-feat review checkpoint recorded; historical ledger retained; no domain falsely closed.')
