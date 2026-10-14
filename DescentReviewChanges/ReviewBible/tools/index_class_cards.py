from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'data/playtest/class_sources'
result={}
for p in source.glob('*.json'):
 if p.name in ['supplements.json','card_index.json']:continue
 d=json.loads(p.read_text(encoding='utf-8'));name=d['class']
 if name in ['Druid','Oracle','Paladin']:continue
 mode=None;band='Base';hero=None;cards=[]
 for row in d['bookLines']:
  s=row['text']
  if s.startswith('Playing '):break
  if s.startswith('Level 1-2'):band='Base'
  if s.startswith('Level 3-9'):band='Arch'
  if s.endswith('(Hero Path)'):band='Hero';hero=s.removesuffix('(Hero Path)').strip()
  if s in ['Passive Skills','Active Skills']:mode=s.split()[0].lower();continue
  if s=='':mode=None;continue
  if mode and ':' in s:
   clean=re.sub(r'^(?:Capstone\s*[–—:-]\s*|Final(?:e| Miracle| Cut| Flight| Form)?\s*[–—:-]\s*)','',s)
   if clean.startswith('Veinweave:'):skill=':'.join(clean.split(':')[:2])
   else:skill=clean.split(':')[0]
   cards.append({'line':row['line'],'name':skill.strip(),'band':band,'path':hero if band=='Hero' else None,'sourceKind':mode,'originalText':s,'automatic':bool(re.search('Capstone',s,re.I) or s.startswith(('Final ', 'Finale:')))})
 # Explicit supplemental choices and final theorems are not under passive/active headers.
 extras={
  'Cleric':list(range(1974,1980)),
  'Mage':[2907,2908,2909],
  'Monk':[3228,3229,3230,3258,3259,3260,3261,3262],
  'Wizard':[5256,5285,5316]
 }.get(name,[])
 for line in extras:
  r=next(x for x in d['bookLines'] if x['line']==line);s=r['text']
  if any(c['line']==line for c in cards):continue
  if name=='Cleric':b='Invocation';h=s.split(':')[0]
  elif name=='Mage':b='Focus';h=s.split(':')[0]
  elif name=='Monk':b='Stance' if line<3232 else 'Discipline';h=None if line<3232 else 'Tortoise'
  else:b='Hero';h={5256:'Spellbinder',5285:'Elementalist',5316:'Necromancer'}[line]
  cards.append({'line':line,'name':s.split(':')[0].strip(),'band':b,'path':h,'sourceKind':'supplement','originalText':s,'automatic':True})
 result[name]=sorted(cards,key=lambda c:c['line'])
target=ROOT/'data/playtest/class_sources/card_index.json'
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name,cs in result.items():print(name,len(cs),{b:sum(c['band']==b for c in cs) for b in dict.fromkeys(c['band'] for c in cs)})
