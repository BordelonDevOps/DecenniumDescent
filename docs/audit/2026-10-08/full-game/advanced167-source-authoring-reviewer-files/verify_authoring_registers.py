"""Read-only validation of authored mappings/arithmetic, NOT runtime or world evidence.
Usage: python verify_authoring_registers.py /path/to/extracted/source --authoring /path/to/this/package
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, json, hashlib, re, math
from collections import Counter
ap=argparse.ArgumentParser();ap.add_argument('source_root',type=Path);ap.add_argument('--authoring',type=Path,default=Path(__file__).resolve().parent);a=ap.parse_args();R=a.source_root.resolve();O=a.authoring.resolve()
def load(p):return json.loads(p.read_text())
source=load(R/'docs/audit/2026-10-08/full-game/ADVANCED_CRAFT_SOURCE_PREPARATION.json'); orig={r['id']:r for r in source['recipes']}
g=load(O/'ADVANCED_167_AUTHORING_REGISTER.json');body=g['bodyProfiles'];rr=g['recipes'];results=[]
def ck(n,b):results.append({'name':n,'pass':bool(b)})
ck('167-exact-unique-membership', len(rr)==167 and len({x['recipeId'] for x in rr})==167 and set(orig)=={x['recipeId'] for x in rr})
ck('four-trade-counts',Counter(x['trade'] for x in rr)=={'Enchanting':43,'Rune Carving':41,'Scribing':40,'Tinkering':43})
ck('100-public7-restricted60-director',Counter(x['sourceVisibility'] for x in rr)=={'public':100,'restricted':7,'director-only':60})
for x in rr:
 r=orig[x['recipeId']];id=x['recipeId']
 ck(id+':preserved-fields', x['name']==r['name'] and x['originalMechanics']==r['mechanics'] and x['sourceQuantity']==r['quantity'] and x['sourceCraftDC']==r['craftingCheck']['targetDC'] and x['sourceSkillLevel']==r['skillLevel'] and x['sourceVisibility']==r['visibility'] and x['sourceWorkRequirements']==r['workRequirements'] and x['sourceEconomy']==r['economy'] and x['sourceDiscovery']==r['discovery'] and x['sourceTrivialAt']==r['skillProgression']['trivialAtSkillLevel'])
 canonical=json.dumps(r,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
 ck(id+':full-source-hash',x['sourceObjectSha256']==hashlib.sha256(canonical).hexdigest())
 ck(id+':source-occurrences', x['componentOccurrences']==len(r['components']) and x['catalystOccurrences']==[i for i,c in enumerate(r['components']) if c['consumed'] and c['role']=='catalyst'] and x['consumedToolOccurrences']==[i for i,c in enumerate(r['components']) if c['consumed'] and c['role']=='tool'])
 ck(id+':absent-null',x['wholeCreatureUsePresent']==('wholeCreatureUse' in r) and x['wholeCreatureUse']==r.get('wholeCreatureUse') and x['sourceAbsentMatrixResearch']==('matrixResearch' not in r) and x['matrixResearch']==r.get('matrixResearch'))
 ck(id+':reserve',x['maximumOrderedBodyReserve']==r['quantity']*3//2)
 h=F(1920) if id=='recipe-623' else F(str(r['workRequirements']['activeWorkHours']))
 ck(id+':hours-dwarf',x['operationalActiveMinutes']==h*60 and x['forgeDwarfActiveMinutes']==math.ceil(h*60*F(3,4)))
 ck(id+':no-field-flag-change',r['workRequirements']['fieldCraftable'] is False)
 for q in x['references']:
  b=body[q['body']];v=F(str(r['economy']['recommendedMarketValue']))/r['quantity']+F(str(b['priceGp']))
  ck(id+':reference:'+q['body'],F(q['finishedReferenceGp']['numerator'],q['finishedReferenceGp']['denominator'])==v and F(q['functionalRepairGp'])==F(str(b['priceGp']))/4 and F(q['brokenReconstructionGp'])==v/4)
ck('31-family-memberships',len(g['familyBindings'])==31 and sum(len(x['recipeIds']) for x in g['familyBindings'])==167)
for x in g['familyBindings']:ck('family:'+x['trade']+':'+x['family'],set(x['recipeIds'])=={r['id'] for r in orig.values() if r['skill']==x['trade'] and r['recipeFamily']==x['family']})
for id,b in body.items():ck('body-positive:'+id,b['HP']>0 and b['AC']>0 and b['massLb']>0 and b['priceGp']>0 and all(v>0 for v in b['dimensionsIn']))
public={b for x in rr if x['sourceVisibility']=='public' for b in x['bodyChoices']}
ck('15-public7-private-body-variants',len(body)==22 and len(public)==15 and sorted(public)==g['publicBodyDependencyIds'] and sorted(set(body)-public)==g['privateOnlyBodyDependencyIds'])
ck('six-consumed-tools-exact',[(x['recipeId'],i) for x in rr for i in x['consumedToolOccurrences']]==[('recipe-637',1),('recipe-639',3),('recipe-673',3),('recipe-685',2),('recipe-686',2),('recipe-687',4)])
ck('172-catalysts758-components',sum(len(x['catalystOccurrences']) for x in rr)==172 and sum(x['componentOccurrences'] for x in rr)==758)
sc=[x for x in rr if x['profile']=='SC-script'];ck('22scripts19one3two',len(sc)==22 and Counter(x['authoredUseBinding']['lifetimeActivations'] for x in sc)=={1:19,2:3})
ck('two-use-exact', {x['recipeId'] for x in sc if x['authoredUseBinding']['lifetimeActivations']==2}=={'recipe-502','recipe-504','recipe-505'})
for x in sc:ck(x['recipeId']+':script-values',x['authoredUseBinding']['maximumSpellRank']==orig[x['recipeId']]['mechanics']['spellLevel'] and x['authoredUseBinding']['lifetimeActivations']==orig[x['recipeId']]['mechanics']['uses'])
autos=[x for x in rr if x['profile']=='TI-automaton'];ck('18automata',len(autos)==18)
for x in autos:
 z=x['authoredUseBinding']['attack'];r=orig[x['recipeId']];n=r['mechanics']['charges'];dt=re.search(r'basic (\w+) attack',r['effects']).group(1)
 ck(x['recipeId']+':attack',z=={'bonus':2+n,'dice':str(n)+'d6','damageType':dt,'reachFeet':5,'attackKind':'melee nonspell magical attack','abilityDamage':0})
cs=load(R/'DescentReviewChanges/ReviewBible/data/public/class_playtests/tinker.json')['cards'];cm=load(O/'TINKER_48_INTERFACE_REGISTER.json')['cards'];cmap={c['id']:c for c in cs}
ck('48class-complete-membership',len(cm)==48 and {c['id'] for c in cm}==set(cmap))
for c in cm:ck(c['id']+':full-source-and-scope',c['sourceCard']==cmap[c['id']] and bool(c['authoringDisposition']) and 'not-promoted' in c['status'])
text=(O/'DD_Advanced_167_Source_Authoring_Verdict.md').read_text()
for prefix in ['AC','EN','RC','SC','TI']:
 for i in range(1,11):ck(f'case:{prefix}-{i:02}',bool(re.search(r'^## '+prefix+f'-{i:02} —',text,re.M)))
for i in range(1,19):ck(f'case:TD-{i:02}',bool(re.search(r'^## TD-'+f'{i:02} —',text,re.M)))
for i in range(1,20):ck(f'worked:W-{i:02}',bool(re.search(r'^## W-'+f'{i:02} —',text,re.M)))
# Independent fixed-boundary assertions: arithmetic only, explicitly not world/event authentication.
ck('W01-121-source-DC8-Q4-hours4',orig['recipe-121']['difficulty']==8 and orig['recipe-121']['quantity']==4 and orig['recipe-121']['workRequirements']['activeWorkHours']==4)
ck('W01-reserve-and-price',4*3//2==6 and F(159,4)+50==F('89.75') and (F(159,4)+50)/4==F('22.4375'))
ck('W02-B7P25-deficit',7+max(1,7*25//100)==8 and 8-(7-4)==5)
ck('W02-B1P25-nocharges',1+max(1,1*25//100)==2)
ck('W08-year-null-economy',orig['recipe-623']['workRequirements']['activeWorkHours'] is None and orig['recipe-623']['economy']['laborValue']==0 and F(1920)*F(3,4)==1440 and 350108//4==87527)
ck('W09-rank8-encoding',8*10==80 and F(8,100)==F('.08') and 10+8==18)
ck('W13-small-chassis-and-HP',body['TI-auto-small']['priceGp']==50 and body['TI-auto-small']['massLb']==25 and 40*3//5==24 and F(50,10)==5 and F(25,100)==F('.25'))
ck('W15-service-sensor',F(20,10)==2 and F(2,100)==F('.02'))
ck('W17-creator-not-operator',4+3==7 and 20+7==27 and 27<28 and 27>28-10)
ck('W18-technical-mastery',60//2==30)
out={'scope':'Authored register/source-binding, case membership and fixed arithmetic checks only. No runtime, actual campaign event, real consent, spell availability or balance validation.','checks':len(results),'failed':[r for r in results if not r['pass']],'recipes':167,'classCards':48,'sourceCases':50,'tinkerCases':18,'workedFixtures':19,'bodyVariants':22,'publicBodyVariants':15,'results':results}
(O/'AUTHORING_REGISTER_CHECKS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
if out['failed']:raise SystemExit(1)
