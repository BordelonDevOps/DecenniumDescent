"""Apply six reviewed overlays; preserve all original spell/book/class sources."""
from pathlib import Path
import json,copy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
closure=(HERE/'GPT_HEALING_FINAL_CLOSURE.md').read_text(encoding='utf-8')
assert 'CLOSED as REVIEWED / reference-VALIDATED' in closure
assert 'approved for promotion into the operational playtest overlay' in closure
validation=json.loads((ROOT/'docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json').read_text(encoding='utf-8'))
assert validation['status']=='PASS' and validation['candidateCount']==6 and validation['classLevelGateCases']==420
draft_path=ROOT/'data/playtest/spell_drafts'
candidate=json.loads((draft_path/'candidate_healing_death.json').read_text(encoding='utf-8'))
spells=copy.deepcopy(candidate['spells'])
ev='docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_CLOSURE.md'
replacements={
 'This draft remains inactive pending exact review.':'Reviewed operational playtest overlay; provisional design decisions remain labeled NEW.',
 'inactive pending exact review.':'reviewed for the operational playtest overlay.',
 'This candidate remains inactive pending exact review.':'Apply the reviewed operational playtest overlay.',
 'Inactive pending exact source, life-state and lethal-track review.':'Reviewed with the healing, life-state and retained lethal-track interface.',
 'Inactive until individual review.':'Individually reviewed operational playtest overlay.',
 'Inactive pending individual review.':'Individually reviewed operational playtest overlay.',
 'inactive until individual review.':'individually reviewed for the operational playtest overlay.',
}
for row in spells:
 for field in ('designNotes','limitations'):
  for old,new in replacements.items():row[field]=row[field].replace(old,new)
 row['reviewEvidence']=[ev]
batch={'status':'REVIEWED / reference-VALIDATED operational-playtest drafts',
       'scope':'Six individual healing/death spell overlays. Approved books/catalog sources remain unchanged; no canon or numerical-balance certification.',
       'reviewEvidence':[ev],'spells':spells}
target=draft_path/'batch_healing_death.json'
if target.exists():assert json.loads(target.read_text(encoding='utf-8'))==batch
else:target.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=draft_path/'selected_sources.json';groups=json.loads(p.read_text(encoding='utf-8'))
backup=HERE/'SPELL_SELECTION_BEFORE_HEALING_PROMOTION.json'
if not backup.exists():
 assert sum(map(len,groups.values()))==72
 backup.write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for row in spells:
 school='Divination' if row['id']=='stitch-fate' else 'Necromancy'
 if row['id'] not in groups[school]:groups[school].append(row['id'])
assert len({ident for ids in groups.values() for ident in ids})==78
p.write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'tools/validate_spell_playtests.py';s=p.read_text(encoding='utf-8')
s=s.replace('All72 requested starter IDs have individual operational drafts','All78 individually reviewed selected IDs have operational drafts').replace('len(selected)==len(set(selected))==72','len(selected)==len(set(selected))==78')
s=s.replace('Remaining776 explicitly blocked','Remaining770 explicitly blocked').replace('for s in spells.values())==776','for s in spells.values())==770')
p.write_text(s,encoding='utf-8')
print('Applied6 reviewed draft overlays and selected78 IDs; catalog rebuild/validation required next.')
