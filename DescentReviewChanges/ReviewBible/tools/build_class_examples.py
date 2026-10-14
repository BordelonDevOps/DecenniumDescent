"""Readable acquisition examples from the validator's actual successful runs."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/public/class_playtests';DOC=ROOT/'docs/mechanics'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
report=read(DOC/'CLASS_PLAYTEST_VALIDATION.json')
out=['# Class playtest — legal build examples','','[Class library](CLASS_PLAYTEST_INDEX.md) · [Shared rules](CLASS_PLAYTEST_RULES.md) · [Validation data](CLASS_PLAYTEST_VALIDATION.json)','','These are legal acquisition examples, not recommendations or claims of optimal balance. Each ordinary table was produced by the validator from eligible cards. Add the automatic grants, equipment, ability scores and spells stated in its class guide. ASI/feat milestones are separate. No later-stage ability is available to a level-1 Base character.','','Bard retains its original [complete worked build and card packet](BARD_PLAYTEST_v0_1.md).','']
for name,stats in report['buildExamples'].items():
 slug=name.lower().replace(' ','-');d=read(DATA/(slug+'.json'));cards={c['id']:c for c in d['cards']}
 out += [f'## {name}','',f'[Class guide](classes/{slug}.md). {stats["sampleCount"]} sampled complete builds, {stats["successful"]} successful.','']
 for path,rows in stats['examples'].items():
  out += [f'### {path}','','| Level | Selected cards |','|---:|---|']
  for row in rows:
   names=[cards[i]['name'] for i in row['selected']]
   if name=='Monk':names=[n+' (choose Tank Discipline for Tortoise eligibility)' if n=='Discipline Initiate' else n for n in names]
   out += [f'| {row["classLevel"]} | '+('; '.join(names) or 'Automatic grants only')+' |']
  out += ['']
out += ['## Druid — all seven Circles','','[Druid guide](classes/druid.md). At level 1 all characters know Wolf, Bear, Hawk, Boar and Panther; choose only one Circle at 2. Choose two Arch forms at 11, independently of the Circle. The validator checks all 7 × 10 = 70 Circle/Arch-form-pair configurations. The following examples use Dire Wolf and Sky Serpent at 11.','','| Circle chosen at 2 | Hero forms available at 10 | Later Circle feature at 14 |','|---|---|---|']
d=read(DATA/'druid.json')
for circle in ['Land','Moon','Storm','Thorns','Winterfang','Rotshaper','Ashen Grove']:
 hero=[c['name'] for c in d['cards'] if c['path']==circle and c['minimumClassLevel']==10 and c['sourceKind']=='form']
 later=[c['name'] for c in d['cards'] if c['path']==circle and c['minimumClassLevel']==14]
 out += ['| '+circle+' | '+'; '.join(hero)+' | '+'; '.join(later)+' |']
out+=['','The full 20-level schedule is in the guide. All examples retain finite Buffer/Form Surge reserves even after unlimited shifting at 20.','','## Oracle — each Mystery, any one Curse','','[Oracle guide](classes/oracle.md). The validator checks 1,800 combinations: 10 Mysteries × 10 Curses × 3 Tier I choices × 3 first Tier II choices × 2 distinct second Tier II choices. Any one Curse supplies Boons at 3/5/10/15/20; it never supplies a second Mystery. The table gives one example for each Mystery, choosing the first Tier I and first two Tier II options. At 15 choose the mastery enhancement of the fixed Tier III Revelation, which every example knows.','','| Mystery at 1 | Tier I at 3 | Tier II at 6 | Second Tier II at 13 | Fixed Tier III at 9 | Final at 20 |','|---|---|---|---|---|---|']
d=read(DATA/'oracle.json')
for i in range(10):
 def find(f):return next(c for c in d['cards'] if c['source'].get('reference')==f'MYSTERIES.ORACLE_MYSTERIES[{i}].{f}')
 out += ['| '+find('level1')['path']+' | '+' | '.join(find(f)['name'] for f in ['tierI[0]','tierII[0]','tierII[1]','tierIII','finalRevelation'])+' |']
out+=['','## Paladin — one Oath, with a separate inversion','','[Paladin guide](classes/paladin.md). Begin with the fixed Base abilities, choose Defense style at 2 for these examples, choose one Oath at 3, and enter mastery of that same Oath at 10. Aura15ft at 6, 20ft at 10, 30ft at 15. These examples choose the +1 fear/charm-save secondary aura at 6. Each Oath automatically teaches its five Revelation spells at 3/5/9/13/17.','','| Oath at 3 | Signature at 11 | Final at 20 | Alternative inverted Signature at 11 |','|---|---|---|---|']
d=read(DATA/'paladin.json')
for i in range(10):
 def find(f):return next((c for c in d['cards'] if c['source'].get('reference')==f'SACRED_OATHS[{i}].{f}'),None)
 c=find('smiteType')
 if not c:continue
 out += ['| '+c['path']+' | '+' | '.join(find(f)['name'] for f in ['signaturePower','finalOathGift','oathbreaker.blasphemousWord'])+' |']
out+=['','An inversion replaces the Smite/Aura/Signature/Revelation package; it is not an additional package. Use the shared five Forbidden spells instead of the five Oath spells, the existing current Lay on Hands points for Death Touch, and Black Manifestation at 20. The validator checks 10 Oaths × 2 modes × 3 styles × 2 secondary aura choices = 120 configurations. A story transition preserves spent resources.','']
(DOC/'CLASS_PLAYTEST_BUILD_EXAMPLES.md').write_text('\n'.join(out),encoding='utf-8')
print('Wrote legal examples for ordinary Hero paths and all exceptional class families.')
