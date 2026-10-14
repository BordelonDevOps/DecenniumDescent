"""Only run after visible browser submission evidence exists."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
assert (HERE/'gpt-form-temphp-submitted.png').exists()
p=HERE/'FORM_TEMP_HP_CONFERENCE_SOURCES.json';d=json.loads(p.read_text(encoding='utf-8'))
d['status']='UNREVIEWED:175 source roles+5 supports visibly submitted to Calibration Review; first individual discussion pending'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
 p=HERE/name;text=p.read_text(encoding='utf-8');title='## Form and temporary-HP conference submitted'
 if title not in text:
  text+='\n'+title+'\n\nThe [175+5 source conference](CODEX_FORM_TEMP_HP_CONFERENCE.md) was visibly submitted through Chrome. It includes all66 Druid passages/metadata,64 other initial class/Bard buffer passages,26 semantic form/guard cards,7 feats,9 spell originals/current overlays and3 recovered V6 ancestry traits. Five supports include V6 default buffer duration and compatible Core HP/death rules. [Source integrity](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_SOURCE_VALIDATION.json) passes; individual classification/decisions are pending. [Submission proof](gpt-form-temphp-submitted.png).\n'
  p.write_text(text,encoding='utf-8')
p=ROOT/'data/playtest/game_development_coverage.json';d=json.loads(p.read_text(encoding='utf-8'))
for r in d['aspects']:
 if r['id'] not in ('DD-24','DD-35'):continue
 for key,items in {'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_SOURCE_BINDINGS.md'],
                   'validationEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/FORM_TEMP_HP_SOURCE_VALIDATION.json']}.items():
  r[key]=list(dict.fromkeys(r[key]+items))
 r['openIssues']=[v for v in r['openIssues'] if not v.startswith('Next form/tempHP corpus175')]
 r['openIssues'].append('Form/tempHP175+5 source conference submitted; source integrity passes, individual discussion and implementation pending. Complete original Druid corpus plus explicit/semantic other class, Bard, feat, spell and recovered ancestry candidates. No whole-card/catalog completion implied.')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded visible175+5 submission; no discussion or implementation closure.')
