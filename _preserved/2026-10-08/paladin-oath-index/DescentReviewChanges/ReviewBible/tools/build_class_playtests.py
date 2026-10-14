"""Build readable, source-linked class packets from reviewed provisional drafts."""
from pathlib import Path
import json,re,hashlib,math
from class_text_spacing import spaced,changes
from oracle_boon_fields import boon_fields
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'data/playtest/class_sources';D=ROOT/'data/playtest/class_drafts'
OUT=ROOT/'data/public/class_playtests';DOC=ROOT/'docs/mechanics/classes'
OUT.mkdir(parents=True,exist_ok=True);DOC.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
index=read(S/'card_index.json');supplements=read(S/'supplements.json')
progress=supplements['class-spell-progression']['CLASS_SPELL_PROGRESSION']
core=read(ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
def pool(name):
 if name in ['Oracle','Soldier','Warrior']:return [0]*20,'No RP: protected class contract'
 if name in core['caster_pools']:return core['caster_pools'][name],'Direct Core Systems V2 table'
 factor=.5 if name=='Crimson Agent' else .35
 return [max(1,math.floor(x*factor+.5)) for x in core['caster_pools']['Cleric']],f'Explicit fallback: Cleric CoreV2 curve ×{factor}, halves upward'
def rank(name,lv):return max([int(r) for r,l in progress[name]['learnLevels'].items() if l<=lv]+[0])
def druid_path(line):
 for a,b,n in [(2654,2687,'Land'),(2691,2708,'Moon'),(2711,2730,'Storm'),(2734,2753,'Thorns'),(2756,2774,'Winterfang'),(2777,2797,'Rotshaper'),(2800,2820,'Ashen Grove')]:
  if a<=line<=b:return n
 return None
def reference_objects(ref,source):
 """Resolve explicit data references only; text is never evaluated as code."""
 found=[]
 if not ref:return found
 roots={'MYSTERIES':supplements['oracle-mysteries'],'CURSES':supplements['oracle-curses'],
        'OATHS':supplements['paladin-oaths'],'PALADIN':supplements['paladin-oaths'],
        'mainRegistry':source['mainRegistry']}
 for root,body in roots.items():
  for m in re.finditer(r'\b'+root+r'((?:\.[A-Za-z_][A-Za-z_0-9]*|\[\d+\])+)',ref):
   obj=body
   try:
    for field,num in re.findall(r'\.([A-Za-z_][A-Za-z_0-9]*)|\[(\d+)\]',m[1]):obj=obj[field] if field else obj[int(num)]
    found.append({'reference':m[0],'value':obj})
   except (KeyError,IndexError,TypeError):pass
 # Accept unprefixed exact export references used by supplemental authoring.
 for key,body in [('SACRED_OATHS',supplements['paladin-oaths']['SACRED_OATHS'])]:
  for m in re.finditer(r'\b'+key+r'(\[\d+\](?:\.[A-Za-z_][A-Za-z_0-9]*|\[\d+\])*)',ref):
   obj=body
   try:
    for field,num in re.findall(r'\.([A-Za-z_][A-Za-z_0-9]*)|\[(\d+)\]',m[1]):obj=obj[field] if field else obj[int(num)]
    found.append({'reference':m[0],'value':obj})
   except (KeyError,IndexError,TypeError):pass
 return found
AUTO={
 'Cleric':[1971], 'Mage':[2890,2891], 'Soldier':[4211], 'Tinker':[4595],
 'Thief':[4450], 'Shaman':[4011,4082],
}
def ordinary_schedule(name):
 rows=[]
 for lv in range(1,21):
  if lv==1:n,b,a=4,['Base'],2
  elif lv==2:n,b,a=2,['Base'],0
  elif lv==3:n,b,a=2,['Arch'],1
  elif lv==10:n,b,a=2,['Hero'],1
  elif lv in [12,14,16,18]:n,b,a=1,['Hero'],0
  elif lv==20:n,b,a=(1,['Hero'],0) if name=='Mage' else (0,[],0)
  else:n,b,a=1,['Base','Arch'],0
  if lv in [5,7,9]:b=['Arch']
  # Some GPT drafts permit either pool at4–9; preserve that explicit variant.
  if name in ['Cleric','Mage','Warrior'] and 4<=lv<=8:b=['Base','Arch']
  if name=='Mage' and lv==9:b=['Base','Arch']
  rows.append({'classLevel':lv,'choose':n,'bands':b,'minimumActives':a,'asiOrFeat':lv in[4,8,12,16,19]})
 return rows

def exception_schedule(name):
 if name=='Druid':
  return {1:'Druidic, spellcasting, five Base forms; 2 shifts/long rest',2:'Choose ONE Circle; only its level-2 benefits',3:'Enter the chosen Circle Arch; Land gains terrain spells',4:'3 shifts; third cantrip',5:'Land terrain spells',6:'Chosen Circle level-6 feature',7:'4 shifts; Land terrain spells',8:'General advancement only',9:'Land terrain spells',10:'Chosen Circle Hero forms; 5 shifts; fourth cantrip; Land Nature’s Ward',11:'Attune any TWO of five Arch forms at each long rest',12:'General advancement only',13:'6 shifts',14:'Chosen Circle level-14 feature',15:'General advancement only',16:'7 shifts',17:'General advancement only',18:'Timeless Body and Beast Spells',19:'8 shifts',20:'Archdruid: unlimited shifting; finite reserves remain'}
 if name=='Oracle':
  return {1:'Choose ONE Mystery and ONE Curse; Mystery identity/Prophecy, RC3, Channel Revelation, Insight, Sense',2:'Curse Manifestation, Trance and Burden',3:'Choose ONE of your Mystery’s three Tier I options; Curse Boon I; RC4',4:'General advancement only',5:'Curse Boon II',6:'Choose ONE of three Tier II options; Mystery Surge; RC5',7:'General advancement only',8:'General advancement only',9:'Fixed Mystery Tier III; RC6',10:'Curse Boon III; Final foreshadow only',11:'RC7 and encounter-start floor',12:'Chosen Mystery Mystic Insight',13:'Choose a SECOND, distinct Tier II option',14:'Oracle-specific advancement milestone',15:'Choose one eligible Mystery mastery; Curse Boon IV',16:'Prophecy Trigger Mastery',17:'Foreshadow — Proven Outcome',18:'ONE Prophetic Surge use shared with Mystery Prophecy variant',19:'General advancement only',20:'Chosen Mystery Final Revelation; selected Curse Boon V'}
 if name=='Paladin':
  return {1:'Lay on Hands, Sense, Martial Proficiency, Strike, Protective Stance, Sacred Touch',2:'Challenge, Bolstering Presence, ONE Fighting Style, spell access',3:'Choose ONE Oath: Smite rider, aura, first Oath spell; Divine Health',4:'General advancement only',5:'Extra Attack; second Oath spell',6:'Aura15ft and one daily secondary benefit',7:'Reactive aura attack once/short rest',8:'General advancement only',9:'Third Oath spell',10:'Hero mastery of the SAME Oath; aura20ft and brief persistence',11:'Chosen Oath Signature (or its inverted Word)',12:'General advancement only',13:'Divine Resistance and fourth Oath spell',14:'General advancement only; no extra ASI',15:'Aura30ft and initiative benefit',16:'General advancement only; no undefined free spell rider',17:'Aura Surge, Lay on Hands Wave and fifth Oath spell',18:'Improved Divine Sense',19:'General advancement only',20:'Chosen Oath Final Gift OR Black Manifestation; Divine Manifestation aura'}
 return {}

def normalize(raw,source):
 name=raw['class'];lookup={x['line']:x for x in index.get(name,[])};lines={x['line']:x['text'] for x in source['bookLines']};cards=[]
 for row in raw['cards']:
  line,lv,act,cost,target,duration,freq,effect=row
  meta=lookup.get(line)
  if meta:
   title=meta['name'];orig=meta['originalText'];band=meta['band'];path=meta['path'];kind=meta['sourceKind']
   auto=meta['automatic']
   if band in ['Invocation','Focus','Stance']:band='Base';auto=True
   if band=='Discipline':band='Arch';auto=(line==3262)
  else:
   assert name in['Druid','Paladin'],(name,line,'not indexed')
   title=lines[line].split(':')[0];orig=lines[line];band='Base' if lv<=2 else 'Arch' if lv<10 else 'Hero';path=druid_path(line) if name=='Druid' else None;kind='form' if 'shift' in cost.lower() else 'feature';auto=True
   if name=='Druid' and line in [2632,2636,2640,2644,2648]:band='Arch'
   ends={2412:2413,2414:2432,2433:2449,2475:2476,2477:2478,2479:2481,2654:2655,2656:2661,2670:2672,2673:2674,2685:2687,2691:2692,2693:2694,2695:2696,2707:2708,2711:2713,2714:2715,2716:2717,2728:2730,2734:2735,2736:2738,2739:2741,2752:2753,2756:2757,2758:2759,2760:2762,2773:2774,2777:2778,2779:2781,2782:2784,2795:2797,2800:2801,2802:2804,2805:2807,2818:2820,3675:3682,3687:3699,3701:3702,3704:3705,3707:3708,3710:3711}
   if name=='Druid' or line in ends:
    nextline=min([r[0] for r in raw['cards'] if r[0]>line]+[line+5])
    end=ends.get(line,nextline-1)
    orig='\n'.join(lines.get(n,'') for n in range(line,end+1)).strip()
  if line in AUTO.get(name,[]):auto=True
  if 'automatic' in freq.lower():auto=True
  if name=='Wizard' and 'Counterspell.' in effect:band='Base';auto=True
  if name=='Wizard' and any(x in effect for x in ['Arcane Tradition.','School Mastery.']):auto=True
  if name=='Monk' and line in range(3258,3262):auto=False
  if name=='Shaman' and 'Elemental Affinity.' in effect:auto=True
  c={'id':f'{slug(name)}.{band.lower()}.{slug(path)+"." if path else ""}{slug(title)}',
     'name':title,'className':name,'band':band,'path':path,'sourceKind':kind,
     'minimumClassLevel':lv,'acquisition':'automatic' if auto else 'selection',
     'activation':spaced(act),'cost':spaced(cost),'rangeAndTarget':spaced(target),
     'duration':spaced(duration),'frequency':spaced(freq),'effect':spaced(effect),
     'source':{'extract':source['sourcePath'],'line':line,'originalText':orig},
     'designStatus':'provisional-playtest','spellRank':None}
  if name in ['Mage','Wizard'] and (f'{name.lower()}-spell' in effect or (name=='Mage' and line in[2907,2908,2909])):
   c['spellRank']=max(1,rank(name,lv))
  cards.append(c)
 extra_cards=[]
 for original in raw.get('extraCards',[]):
  if name=='Oracle' and original.get('kind')=='curse':
   parts=re.split(r'BOON (I|II|III|IV|V)\s*[—–-]\s*Oracle\s*(3|5|10|15|20)\s*:',original['effect'])
   assert len(parts)==16,(original['name'],'missing five boon gates')
   base=dict(original);base['effect']=parts[0].strip();base['acquisition']='choose one Curse at1';extra_cards.append(base)
   for j in range(1,len(parts),3):
    roman,gate,effect=parts[j:j+3];gate=int(gate)
    boon=dict(original);boon.update(name=f'{original["name"]} — Boon {roman}',level=gate,band='Arch' if gate<10 else 'Hero',path=original['name'],kind='curseBoon',effect=effect.strip(),acquisition='automatic for selected Curse',prerequisite=f'Oracle{gate}; selected Curse:{original["name"]}',frequency='As the boon states')
    boon.update(boon_fields(original['name'],(j-1)//3))
    extra_cards.append(boon)
  else:extra_cards.append(original)
 for i,e in enumerate(extra_cards):
  lv=e['level'];band=e.get('band') or ('Base' if lv<=2 else 'Arch' if lv<10 else 'Hero');path=e.get('path')
  source_line=e.get('sourceLine')
  if not source_line:
   m=re.search(r'Source progression line (\d+)',e['effect'])
   if m:source_line=int(m[1])
  c={'id':f'{slug(name)}.supplement.{slug(path)+"." if path else ""}{slug(e["name"])}',
     'name':e['name'],'className':name,'band':band,'path':path,'sourceKind':e.get('kind','supplement'),
     'minimumClassLevel':lv,'acquisition':e.get('acquisition','supplement'),
     'activation':spaced(e['activation']),'cost':spaced(e['cost']),'rangeAndTarget':spaced(e['rangeAndTarget']),
     'duration':spaced(e['duration']),'frequency':spaced(e['frequency']),'effect':spaced(e['effect']),
     'prerequisite':spaced(e.get('prerequisite','See class engine and progression.')),
     'source':{'line':source_line, 'reference':e.get('sourceRef'),
       'originalText':lines.get(source_line,''),'status':'source-derived' if source_line or e.get('sourceRef') else 'explicit-new-playtest-completion'},
     'designStatus':'provisional-playtest','spellRank':None}
  resolved=reference_objects(e.get('sourceRef'),source)
  if resolved:c['source']['originalObjects']=resolved
  if name in['Mage','Wizard'] and f'{name.lower()}-spell' in e['effect']:c['spellRank']=max(1,rank(name,lv))
  if name=='Wizard' and source_line:c['acquisition']='automatic'
  if name=='Warrior' and source_line in range(4788,4799):c['acquisition']='automatic'
  if name=='Oracle' and (e['kind'] in ['core','framework','automatic','progression','capstone','final'] or 'Automatic' in e['frequency']):c['acquisition']='automatic'
  if name=='Oracle' and 'MYSTERIES.ORACLE_MYSTERIES[' in str(e.get('sourceRef')):
   ref=e['sourceRef']
   c['acquisition']='automatic for chosen Mystery'
   if '.tierI[' in ref:c['acquisition']='choose one at Oracle 3'
   if '.tierII[' in ref:c['acquisition']='choose first at Oracle 6; a distinct second at Oracle 13'
   if '.revelationMastery' in ref:c['acquisition']='choose one eligible enhancement at Oracle 15'
  if name=='Paladin' and e.get('sourceRef') and e.get('kind')!='new forbidden spell':c['acquisition']=e.get('acquisition','automatic for chosen Oath')
  if name=='Paladin' and e.get('sourceRef') and 'smiteType' in e['sourceRef']:
   m=re.search(r'SACRED_OATHS\[(\d+)\]',e['sourceRef'])
   if m:c['conductClauses']=supplements['paladin-oaths']['SACRED_OATHS'][int(m[1])]['conductClause']
  if name=='Paladin' and e.get('kind') in['revelationSpell','oathSpell','new forbidden spell']:c['spellRank']={3:1,5:2,9:3,13:4,17:5}.get(lv)
  cards.append(c)
 rp,authority=pool(name)
 return {'schemaVersion':'1.0','version':'0.1-playtest','class':name,'status':'provisional-card-draft-not-balance-approved',
 'sourceExtractSha256':source['sourceSha256'],'protectedInterfaceOriginal':source['mainRegistry']['core']['resonanceInterface'],
 'rpByClassLevel':rp,'rpAuthority':authority,'maxSpellRankByClassLevel':[rank(name,l) for l in range(1,21)],
 'asiClassLevels':[4,8,14,19] if name=='Oracle' else [4,8,12,16,19],
 'engine':[spaced(s) for s in raw['engine']], 'workedExample':[spaced(s) for s in raw['workedExample']],
 'balanceQuestions':raw['balanceQuestions'],'cards':cards,
 'schedule':ordinary_schedule(name) if name not in ['Druid','Oracle','Paladin'] else [],
 'exceptionSchedule':exception_schedule(name),
 'sourceFiles':[f'../../../data/playtest/class_sources/{slug(name)}.json','../../../data/playtest/class_sources/supplements.json'],
 'authoringNotes':raw.get('reviewStatus','Draft authored; editorial review pending')}

def render(d,source):
 name=d['class'];cards=d['cards'];rp=d['rpByClassLevel'];ranks=d['maxSpellRankByClassLevel'];paths=list(dict.fromkeys(c['path'] for c in cards if c['band']=='Hero' and c['path']))
 chunks=[f'# {name} — class playtest v0.1','', '**PROVISIONAL — exact numbers and acquisition are proposals for table testing.** Approved source books remain intact. The17 class names identify Base classes; Arch and Hero are later stages, with explicit exceptions below.','',
 '[All classes](../CLASS_PLAYTEST_INDEX.md) · [Shared test rules](../CLASS_PLAYTEST_RULES.md) · [Session log](../CLASS_PLAYTEST_SESSION_LOG.md)', '',
 f'[Preserved book and registry evidence](../../../data/playtest/class_sources/{slug(name)}.json) · [Normalized card data](../../../data/public/class_playtests/{slug(name)}.json)','',
 '## Class engine and setup','']
 # Keep book setup readable and clearly distinguished from new numerical rules.
 setup=[]
 for x in source['bookLines']:
  if x['text'].startswith(('Main Attribute:','Secondary Attribute','Hit Points:','Armor Proficiency:','Weapon Proficiency:','Tool Proficiency:')):setup.append(x['text'])
 if setup:chunks+=['**Book setup (provisional engine resolves any explicit conflicts below):**','']+['- '+x for x in setup]+['']
 chunks+=d['engine'][:1]+['']
 for s in d['engine'][1:]:chunks+=[s,'']
 chunks+=['**Protected source interface:** '+d['protectedInterfaceOriginal'],'',
 '## Advancement and resources','',f'RP authority: {d["rpAuthority"]}. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.','',
 '| Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |','|---:|---|---:|---:|---|']
 for lv in range(1,21):
  auto=[c['name']+(f' ({c["path"]})' if c['path'] else '') for c in cards if c['minimumClassLevel']==lv and c['acquisition']=='automatic']
  stage='Base' if lv<3 else 'Arch' if lv<10 else 'Hero'
  if d['schedule']:
   row=d['schedule'][lv-1];n=row['choose'];s=f'Choose {n} '+('/'.join(row['bands'])) if n else 'No ordinary selection'
   if row['minimumActives']:s+=f'; at least{row["minimumActives"]} active'
  else:s=d['exceptionSchedule'][lv]
  if auto and d['schedule']:s+='; automatic: '+', '.join(auto)
  if name=='Wizard' and lv==10:s+='; Elementalist counts automatic Affinity as one of its two acquisitions and chooses only one additional card'
  if lv in ([4,8,14,19] if name=='Oracle' else [4,8,12,16,19]):s+='; ASI or feat'
  chunks.append(f'| {lv} | {stage} | {rp[lv-1]} | {ranks[lv-1] if name not in["Oracle","Soldier","Warrior"] else "—"} | {spaced(s)} |')
 chunks+=['','Source-listed options for mutually exclusive paths are alternatives, not simultaneous grants. A minimum level on an Arch card may be above9; that card remains an Arch option during later progression.','',
 'See [legal build examples](../CLASS_PLAYTEST_BUILD_EXAMPLES.md) for actual level-by-level choices and exceptional progression combinations.','',
 '## Worked encounter','']
 chunks += [f'{i}. {s}' for i,s in enumerate(d['workedExample'],1)]+['']
 for band in ['Base','Arch','Hero']:
  group=[c for c in cards if c['band']==band]
  if not group:continue
  chunks +=[f'## {band} cards','']
  previous=object()
  for c in group:
   if c['path']!=previous:
    if c['path']:chunks +=[f'### {c["path"]}','']
    previous=c['path']
   chunks +=[f'#### {c["name"]}','',f'**Level {c["minimumClassLevel"]} · {c["acquisition"]} · {c["id"]}**','',
     '| Activation | Cost | Range / targets | Duration | Frequency |','|---|---|---|---|---|',
     '| '+' | '.join(str(c[k]).replace('|','/') for k in ['activation','cost','rangeAndTarget','duration','frequency'])+' |','',c['effect'],'']
   if c.get('prerequisite'):chunks+=['Prerequisite: '+c['prerequisite'],'']
   if c.get('conductClauses'):chunks+=['Preserved Oath conduct clauses:','']+['- '+s for s in c['conductClauses']]+['']
   if c['spellRank'] is not None:chunks +=[f'Class-spell rank: **{c["spellRank"]}** for Dissonance, countering and rank restrictions; pay printed RP only.','']
   src=c['source']
   if src.get('originalText'):chunks+=['<details><summary>Preserved source wording'+(f' — book line{src["line"]}' if src.get('line') else '')+'</summary>','',src['originalText'],'','</details>','']
   elif src.get('originalObjects'):
    chunks+=['<details><summary>Preserved supplemental source wording</summary>','','```json',json.dumps(src['originalObjects'],ensure_ascii=False,indent=2),'```','','</details>','']
   elif src.get('reference'):chunks+=['Source reference: `'+str(src['reference'])+'` in the preserved supplements/book evidence.','']
   else:chunks+=['Source status: **new playtest completion**, not recovered historical wording.','']
 chunks+=['## Source appendix and open balance questions','',f'The complete original {name} book section, including lore, examples and alternate progression, is preserved in the [source evidence JSON](../../../data/playtest/class_sources/{slug(name)}.json). The supplemental source tables are [preserved separately](../../../data/playtest/class_sources/supplements.json). Do not stack older level-table features on top of this draft.','']
 if name=='Druid':
  chunks+=['Land Circle always-prepared spell pairs, preserved exactly:','']+[x['text'] for x in source['bookLines'] if 2662<=x['line']<=2669]+['']
 chunks +=['- '+q for q in d['balanceQuestions']]+['','A complete card specification is not balance approval. Record actual play results, particularly resource exhaustion, condition locks, survival and how often choices become unusable.','']
 return '\n'.join(chunks)

def main():
 manifest=[]
 for p in sorted(D.glob('*.json')):
  raw=read(p);name=raw['class'];source=read(S/f'{slug(name)}.json')
  d=normalize(raw,source);dump(OUT/f'{slug(name)}.json',d)
  (DOC/f'{slug(name)}.md').write_text(render(d,source),encoding='utf-8')
  manifest.append({'class':name,'cards':len(d['cards']),'guide':f'classes/{slug(name)}.md','data':f'../../data/public/class_playtests/{slug(name)}.json','stageCounts':{b:sum(c['band']==b for c in d['cards']) for b in['Base','Arch','Hero']}})
 # The approved-for-testing Bard draft stays byte-for-byte untouched and linked.
 b=read(ROOT/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json')
 manifest.insert(0,{'class':'Bard','cards':len(b['cards']),'guide':'BARD_PLAYTEST_v0_1.md','data':'../../data/public/Decennium_Descent_Bard_Playtest_v0_1.json','stageCounts':{band:sum(c['band']==band for c in b['cards']) for band in['Base','Arch','Hero']}})
 dump(OUT/'manifest.json',{'version':'0.1-playtest','classes':manifest,'totalCards':sum(x['cards'] for x in manifest),'expectedClasses':17,'completeCount':len(manifest),'status':'DRAFT; validation and table testing are distinct'})
 dump(ROOT/'data/playtest/class_spacing_changes.json',changes)
 text=['# Class playtest library','', '**Base classes first, then Arch and Hero.** This library extends the Bard treatment across the class families. Every exact mechanic is a provisional test specification; original books, lore, alternatives and GPT replies are preserved.','', '[Start with a Base class](BASE_CLASSES_START_HERE.md) · [Legal builds](CLASS_PLAYTEST_BUILD_EXAMPLES.md) · [Shared rules](CLASS_PLAYTEST_RULES.md) · [Session log](CLASS_PLAYTEST_SESSION_LOG.md) · [Validation report](CLASS_PLAYTEST_VALIDATION.json)','',f'Currently built: **{len(manifest)} of 17 classes**, {sum(x["cards"] for x in manifest)} cards. Validation report determines completeness; this count alone is not approval.','', '| Base class | Cards | Base / Arch / Hero | Guide | Data |','|---|---:|---|---|---|']
 for x in manifest:text.append(f'| {x["class"]} | {x["cards"]} | '+ ' / '.join(str(x['stageCounts'][b]) for b in['Base','Arch','Hero'])+f' | [Open]({x["guide"]}) | [JSON]({x["data"]}) |')
 text+=['','Start with a Base-level character. Enter its Arch progression only at the stated gate and choose one Hero path later. Druid, Oracle and Paladin have explicit progression exceptions; forms, Mysteries, Curses and Oaths are not additional Base classes.','', 'The packets provide costs, actions, targets, durations, frequency, source wording, progression and worked turns. They preserve the protected class engines and call out new rules where the sources were incomplete or conflicting.','']
 (ROOT/'docs/mechanics/CLASS_PLAYTEST_INDEX.md').write_text('\n'.join(text),encoding='utf-8')
 print(f'Built{len(manifest)} classes /{sum(x["cards"] for x in manifest)} cards')
if __name__=='__main__':main()
