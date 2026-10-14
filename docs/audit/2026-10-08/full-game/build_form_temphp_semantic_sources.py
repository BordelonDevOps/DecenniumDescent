"""Add exact semantic form candidates and recovered V6/Core context."""
from pathlib import Path
import json,re,hashlib
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
prior=json.loads((HERE/'FORM_TEMP_HP_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
known={r['card']['id'] for r in prior['classRecords'] if r['kind']=='class-card'}
selected={
 'mage':['mage.hero.lich.undead-immunities'],
 'mirrorsage':['mirrorsage.arch.advanced-mirrorcall','mirrorsage.arch.mirror-shift'],
 'warrior':['warrior.base.serum-tolerance','warrior.arch.intimidating-transformation','warrior.hero.wardborn.controlled-transformation','warrior.hero.wardborn.aegis-incarnate','warrior.hero.wardborn.warding-mutation','warrior.hero.ironskin.adaptive-perfection','warrior.hero.ironskin.adaptive-mutation','warrior.hero.dreadspawn.abomination-ascendant','warrior.hero.dreadspawn.apex-aberration-1-day','warrior.hero.dreadspawn.horrific-mutation','warrior.supplement.apex-form','warrior.supplement.butcherform-chassis'],
 'monk':['monk.arch.tortoise.final-form-bastion-of-breath','monk.hero.iron-fist-master.steel-reflection-form'],
 'oracle':['oracle.supplement.shared.oracle-s-burden','oracle.supplement.curse.consumed','oracle.supplement.consumed.consumed-boon-i','oracle.supplement.consumed.consumed-boon-ii','oracle.supplement.consumed.consumed-boon-iii','oracle.supplement.consumed.consumed-boon-iv','oracle.supplement.consumed.consumed-boon-v','oracle.supplement.ancestor.spirit-walk','oracle.supplement.stars.clarity'],
 'paladin':['paladin.hero.divine-sense']}
rows=[]
for owner,ids in selected.items():
 path=f'data/public/class_playtests/{owner}.json';byid={c['id']:c for c in json.loads((ROOT/path).read_text(encoding='utf-8'))['cards']}
 for ident in ids:
  if ident in known:continue
  c=byid[ident];rows.append({'kind':'class-card','owner':owner,'path':path,'card':c,'sourceObjectSha256':digest(c),
                           'candidateOrigin':'Semantic form/anatomy/disguise/natural-attack or perception guard; classify exact role, not whole-card approval'})
path='src/data/spells.js'
spells=json.JSONDecoder().raw_decode((ROOT/path).read_text(encoding='utf-8').split('export const SPELLS = ',1)[1])[0]
overlay_path='data/public/spell_playtests/catalog.json';overlays={r['id']:r for r in json.loads((ROOT/overlay_path).read_text(encoding='utf-8'))['spells']}
spell_rows=[]
for ident in ('shapechange','polymorph','true-polymorph','mass-polymorph'):
 s=spells[ident];o=overlays[ident]
 spell_rows.append({'kind':'ordinary-spell','sourcePath':path,'sourceId':ident,'sourceObject':s,'sourceObjectSha256':digest(s),
                    'overlayPath':overlay_path,'overlayObject':o,'overlayObjectSha256':digest(o)})
file=GAME/'docs/reference/Player_Rulebook_v6_source_text.txt';lines=file.read_text(encoding='utf-8').splitlines()
v6=[]
for prefix in ('Temporary Hit Points','Consume Decay.','Battle Cry.','Soul Drain.'):
 i=next(i for i,t in enumerate(lines) if t.startswith(prefix))
 text='\n'.join(lines[i:i+3]) if prefix=='Temporary Hit Points' else lines[i]
 v6.append({'kind':'v6-source-passage','sourcePath':'docs/reference/Player_Rulebook_v6_source_text.txt','sourceRoot':'game',
            'line':i+1,'prefix':prefix,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()})
file=ROOT/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md'
core=[]
for p in file.read_text(encoding='utf-8').split('\n\n'):
 if ('Temporary HP' in p or 'temporary HP' in p or 'Post-temp' in p) and not p.startswith('|'):
  core.append({'sourcePath':'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md','text':p,'textSha256':hashlib.sha256(p.encode()).hexdigest()})
druid=json.loads((ROOT/'data/public/class_playtests/druid.json').read_text(encoding='utf-8'))
meta={k:druid[k] for k in ('protectedInterfaceOriginal','workedExample','exceptionSchedule','rpByClassLevel','maxSpellRankByClassLevel')}
data={'status':'UNREVIEWED_SOURCE_CANDIDATES','scope':'Semantic supplement, not all-form/catalog completeness. Full Druid metadata preserved alongside its66 source passages; other named forms require role classification and may retain separate implementation dependencies.',
      'classRecords':rows,'spellRecords':spell_rows,'v6Records':v6,'coreSupports':core,'druidMetadata':meta,'druidMetadataSha256':digest(meta)}
(HERE/'FORM_TEMP_HP_SEMANTIC_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Preserved {len(rows)} semantic class cards,4 transformation spells,4 V6 passages,{len(core)} Core supports and Druid metadata.')
for r in spell_rows:print(r['sourceId'],r['overlayObject']['status'])
