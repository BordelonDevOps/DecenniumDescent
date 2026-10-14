from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
p=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(p.read_text(encoding='utf-8'))
for row in data['aspects']:
    if row['number'] in (3,17,18,19,20,21):
        row['status']='implemented-bounded-candidate; final-disposition-pending'
        additions={'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md'],
                   'validationEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_PLAYTEST_VALIDATION.json'],
                   'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_COMBAT_COUNTEREXAMPLE_REVIEW.md','docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md','docs/audit/2026-10-08/full-game/CODEX_COMBAT_FINAL_DISPOSITION.md']}
        for field,values in additions.items():
            for value in values:
                if value not in row[field]:
                    row[field].append(value)
    if row['number'] in (16,40,41):
        for field,value in [('sourceEvidence','docs/audit/2026-10-08/full-game/STRAIN_SOURCE_BINDINGS.json'),
                            ('reviewEvidence','docs/audit/2026-10-08/full-game/CODEX_STRAIN_EXACT_CONFERENCE.md'),
                            ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_SOURCE_VALIDATION.json')]:
            if value not in row[field]:
                row[field].append(value)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=AUDIT/'REVIEW_STATUS.md'
text=p.read_text(encoding='utf-8')
text+='\n## Combat candidate implementation\n\nThe [current combat guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md) implements the supplied source/action/timing/vision scope. The [exact findings](GPT_COMBAT_EXACT_FINDINGS.md) identified a marker double-skip and missing maneuver interval-budget validation. Both are fixed in the [disposition](CODEX_COMBAT_FINAL_DISPOSITION.md); 112 checks and285 movement-cost scenarios pass. Final bounded confirmation is pending; DD03/17/18/19/20/21 remain open. Source-card exceptions such as Mind Shock are preserved rather than erased by the ordinary Reaction helper.\n\nThe [Strain conference](CODEX_STRAIN_EXACT_CONFERENCE.md) now supplies17 exact Warrior cards,8 engines,3 campaign sections and12 Core paragraphs. [Source checks](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_SOURCE_VALIDATION.json) pass; namespace, penalty and recovery interpretations are still under discussion.\n'
p.write_text(text,encoding='utf-8')
print('Registered combat candidate and Strain source conference; no broader closure.')
