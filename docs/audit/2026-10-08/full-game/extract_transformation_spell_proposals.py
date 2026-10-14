"""Preserve GPT's actual proposals, without normalizing or adopting them."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
text=(HERE/'GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md').read_text(encoding='utf-8')
decoder=json.JSONDecoder();spells=[]
for section in text.split('Complete individual draft: ')[1:]:
    start=section.index('{');obj,_=decoder.raw_decode(section[start:]);spells.append(obj)
assert len(spells)==5 and {s['id'] for s in spells}=={'harmonic-bulwark','polymorph','shapechange','true-polymorph','mass-polymorph'}
table=text.split('Profile ID\tTier\tSize\tMovement\tSpeech / hands\tAC\tNatural attack\tPassive anatomy',1)[1].split('formNormalAC uses',1)[0]
profiles=[]
for line in table.strip().splitlines():
    fields=line.split('\t')
    if len(fields)!=8:continue
    profiles.append(dict(zip(('id','tier','size','movement','speechHands','ac','naturalAttack','passiveAnatomy'),fields)))
assert len(profiles)==12 and len({p['id'] for p in profiles})==12
out={'status':'FIRST DISCUSSED PROPOSALS; boundary reconciliation and implementation pending',
     'sourceReply':'GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md',
     'notAnOperationalCatalog':'Preserves proposal wording including True Polymorph concentration string; normalize schema only after actual boundary decisions.',
     'spells':spells,'profiles':profiles}
(HERE/'TRANSFORMATION_SPELL_FIRST_PROPOSALS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved5 exact JSON proposals and12 exact profile table rows; no operational promotion.')
