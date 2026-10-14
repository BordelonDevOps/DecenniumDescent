"""Independent full-envelope projection and finite arithmetic evidence.

This verifies authored data/manuscripts, not a gameplay runtime. It deliberately
does not claim the still-required complete physical sequence fixture coverage.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(d):return F(d['numerator'],d['denominator'])
def rat(v):v=F(v);return {'numerator':v.numerator,'denominator':v.denominator}
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(name,ok):checks.append({'name':name,'pass':bool(ok)})

internal=read(R/'data/director/gathering_tool_recipe_candidate_internal.json')
public=read(R/'data/crafting/gathering_tool_recipe_candidate_public.json')
src=read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json');sources={r['id']:r for r in src['recipes']}
ic={c['recipeId']:c for c in internal['cards']};pc={c['recipeId']:c for c in public['cards']}
expected={f'recipe-{n}' for n in list(range(320,345))+[347,349,350,656]+list(range(507,532))+[676,677,678]+list(range(433,457))+[668]}
check('Exact public set82 independently enumerated',len(public['cards'])==82 and set(pc)==expected and expected=={r['id'] for r in src['recipes'] if r['skill'] in ['Mining','Skinning','Salvaging'] and r['visibility']=='public'})
check('All15 public models equal complete internal models',len(public['baseModels'])==15 and set(public['baseModels'])=={mid for c in pc.values() for mid in c['operational']['baseModelIds']} and all(b==internal['baseModels'][key] for key,b in public['baseModels'].items()))
check('All3 auxiliary models equal across audiences',len(public['auxiliaryModels'])==3 and public['auxiliaryModels']==internal['auxiliaryModels'])
check('Shared eligibility is equal across audiences',public['sharedCandidateRules']==internal['sharedCandidateRules'])
manuscripts={tr:(R/f'docs/mechanics/{tr.upper()}_CANDIDATE_RECIPE_CARDS.md').read_text(encoding='utf-8') for tr in ['Mining','Skinning','Salvaging']}
profile_count=0;paragraph_count=0
sourcekeys={'id','name','skill','skillLevel','difficulty','difficultyBand','craftingTime','rarity','quantity','tags','recipeFamily','outputType','effects','workRequirements','craftingCheck','discovery','economy','skillProgression','tier','visibility','knowledgeStatus','publicAvailability','components'}
for rid,c in pc.items():
 r=sources[rid];full=ic[rid];p=c['sourceRecipe'];tr=r['skill'];o=c['operational']
 check(rid+' full operational/public body-reference parity',o==full['operational'] and c['status']==internal['status'] and c['visibility']=='public')
 check(rid+' exact six source book paragraphs',c['publicBookBinding']==full['publicBookBinding'] and len(c['publicBookBinding']['paragraphs'])==6)
 paragraph_count+=len(c['publicBookBinding']['paragraphs'])
 check(rid+' bounded public source envelope',set(p)<=sourcekeys and all(p[k]==r[k] for k in p if k!='components'))
 section=manuscripts[tr].split(f"## {r['name']} — {rid}\n",1)[1].split('\n## ',1)[0]
 check(rid+' exact operative manuscript and body',section.count('**Operational effect:** '+o['text']+'\n')==1 and internal['baseModels'][o['baseModelIds'][0]]['operationalBodyText'] in section and all(str(x['index']) in section and x['text'].replace('|','\\|').replace('\n',' ') in section for x in c['publicBookBinding']['paragraphs']))
 check(rid+' component occurrences not merged',len(p['components'])==len(r['components']) and all(all(v[k]==r['components'][i][k] for k in ['name','quantity','role','consumed']) for i,v in enumerate(p['components'])))
 for i,v in enumerate(p['components']):
  raw=r['components'][i];matches=[m for m in src['materials'] if m['name'].casefold()==raw['name'].casefold() and all(m.get(k)==raw.get(k) for k in ['tier','value','weight'])]
  allowed=len(matches)==1 and matches[0].get('visibility')=='public'
  check(f'{rid}[{i}] fail-closed supplemental visibility',set(v)<=({'name','quantity','role','consumed','publicMaterialProfile'} if allowed else {'name','quantity','role','consumed'}) and ('publicMaterialProfile' in v)==allowed)
  if allowed:
   profile_count+=1;m=matches[0]
   check(f'{rid}[{i}] independently public profile fields',v['publicMaterialProfile']=={k:m[k] for k in ['name','tier','rarity','category','value','weight','properties'] if k in m})
check('Exactly492 retained paragraphs and82 public supplemental profiles',paragraph_count==492 and profile_count==82)
for tr,n in [('Mining',29),('Skinning',28),('Salvaging',25)]:
 ids=re.findall(r'^## .+ — (recipe-\d+)\s*$',manuscripts[tr],re.M)
 check(tr+' manuscript exact membership',len(ids)==n and set(ids)=={rid for rid,c in pc.items() if c['sourceRecipe']['skill']==tr})
for rid in ['recipe-347','recipe-349','recipe-350','recipe-656','recipe-676']:
 tr=sources[rid]['skill'];part=manuscripts[tr].split(f"## {sources[rid]['name']} — {rid}\n",1)[1].split('\n## ',1)[0]
 check(rid+' public omission openly labeled NEW','**NEW omission completion:**' in part)

public_files=[R/'data/crafting/gathering_tool_recipe_candidate_public.json']+list(R.glob('docs/mechanics/*CANDIDATE*GUIDE.md'))+[R/'docs/mechanics/GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md']+[R/f'docs/mechanics/{tr}_CANDIDATE_RECIPE_CARDS.md' for tr in ['MINING','SKINNING','SALVAGING']]
public_files=[p for p in public_files if p.name.startswith(('GATHERING_TOOL','MINING','SKINNING','SALVAGING','gathering_tool'))]
for p in public_files:
 text=p.read_text(encoding='utf-8')
 found=set(re.findall(r'recipe-\d+',text))
 check(p.name+' contains no private recipe identity',found<=expected)
 check(p.name+' no private source keys, dossier links or private bodies',not any(k in text for k in ['"directorGuidance"','"sourceMonsters"','"dropRate"','"dropQuantity"','"matrixResearch"','"legacyEffect"','director-only/','GPT_GATHERING','mining.drill','salvaging.recovery-rig']))
 if p.suffix=='.md':
  links=re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',text)
  check(p.name+' local links resolve',all('://' in link or (p.parent/link).exists() for link in links))

# All recipe/outcome/option rows are derived from the unchanged source Q and
# checked against authored output fields. Two labels remain explicit even where
# choosing an option is inapplicable; this is not 1,536 distinct game mechanics.
craft=[];fields={'Standard':'Standard','Flawed':'FlawedQuantity','Failed':'Failed','Mishap':'Mishap'}
for rid,c in ic.items():
 r=sources[rid];q=r['quantity'];o=c['operational'];reserve=3*q//2
 for band in ['Masterwork','Exceptional','Standard','Flawed','Failed','Mishap']:
  for option in ['yield','structural']:
   applies=band in ['Masterwork','Exceptional']
   if applies:
    percent=50 if band=='Masterwork' else 25
    expected_q=q*(100+percent)//100 if option=='yield' else q
    field=band+'Yield' if option=='yield' else 'StructuralOptionQuantity'
    structural=percent if option=='structural' else 0
   else:
    expected_q={'Standard':q,'Flawed':q//2 if q>=2 else 1,'Failed':0,'Mishap':0}[band];field=fields[band];structural=0
   ok=o['outcomes'][field]==expected_q and expected_q<=reserve and o['maximumOrderedBodyReserve']==reserve
   if structural:ok=ok and o['outcomes'][band+'StructuralPercent']==structural
   if band=='Flawed':ok=ok and o['outcomes']['SingletonFlawedAddsPersistentFlaw']==(q==1)
   craft.append({'recipeId':rid,'band':band,'option':option,'optionApplicable':applies,'expectedQuantity':expected_q,'expectedNewStructuralPercent':structural,'orderedBodyReserve':reserve,'pass':bool(ok)})
check('All1536 explicit recipe-band-option rows pass',len(craft)==1536 and all(x['pass'] for x in craft))

# The structural expectation is calculated directly from the 17 authored B5
# bodies. Broken is represented but fails creation admission, independently of
# whether a repair is possible with actual surviving primary constituents.
structural=[];positive=Counter();all_states=Counter();transitions=[]
for mid,b in internal['baseModels'].items():
 for pct in [0,25,50]:
  for flaw in [False,True]:
   mx=5*(100+pct)//100;mx=max(1,mx//2) if flaw else mx
   for hp in range(mx+1):
    all_states[b['trade']]+=1
    if hp>0:positive[b['trade']]+=1
    structural.append({'modelId':mid,'structuralPercent':pct,'persistentFlaw':flaw,'maximumHP':mx,'currentHP':hp,'positiveHPAdmission':hp>0})
    for new_pct in [0,25,50]:
     for add_flaw in [False,True]:
      final_pct=max(pct,new_pct);final_flaw=flaw or add_flaw
      final_max=5*(100+final_pct)//100;final_max=max(1,final_max//2) if final_flaw else final_max
      deficit=mx-hp;final_hp=max(0,final_max-deficit)
      ok=0<=final_hp<=final_max and (new_pct>pct or add_flaw or final_hp==hp) and (not flaw or final_flaw)
      transitions.append({'modelId':mid,'from':[pct,flaw,hp],'requestedStructuralPercent':new_pct,'addPersistentFlaw':add_flaw,'to':[final_pct,final_flaw,final_hp],'maximumHP':final_max,'damageDeficit':deficit,'creationAdmissible':hp>0,'pass':ok})
check('GI-12-C1 corrected positive442/all544 inputs',dict(positive)=={'Mining':156,'Skinning':130,'Salvaging':156} and dict(all_states)=={'Mining':192,'Skinning':160,'Salvaging':192} and len(structural)==544)
check('3264 structural reference transitions remain bounded and preserve flaw/history',len(transitions)==3264 and all(x['pass'] for x in transitions))
check('Singleton1/5 becomes Broken0/2 on new flaw',any(x['from']==[0,False,1] and x['requestedStructuralPercent']==0 and x['addPersistentFlaw'] and x['to']==[0,True,0] and x['maximumHP']==2 for x in transitions))

quotes=[]
for rid,c in ic.items():
 r=sources[rid];b=internal['baseModels'][c['operational']['baseModelIds'][0]];body=F(str(b['baselinePriceGp']));finished=F(str(r['economy']['recommendedMarketValue']))/r['quantity']+body
 for broken in [False,True]:
  expected_cost=(finished if broken else body)/4;key='broken' if broken else 'functional';rep=c['operational']['repair']
  expected_dc=r['craftingCheck']['targetDC'] if broken else 10
  ok=frac(rep[key+'MaterialReferenceGp'])==expected_cost and rep[key+'DC']==expected_dc and rep['requiredOriginalPrimaryMembers']==b['requiredOriginalPrimaryMembers'] and rep['requiresOriginalCreationRecord'] and not rep['terminalDismantlingRestorable']
  quotes.append({'recipeId':rid,'mode':key,'materialReferenceGp':rat(expected_cost),'DC':expected_dc,'maximumHPBound':7,'hoursAtAnyCurrentAuthoredMaximum':8 if broken else 1,'requiresCredentialAndActualToolsStationMaterialAndOriginalPrimaries':True,'pass':bool(ok)})
check('All256 functional/Broken quotation rows match source arithmetic and primary requirements',len(quotes)==256 and all(x['pass'] for x in quotes))

status=read(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json')
check('Every current authoring manifest artifact matches recorded bytes',all(sha(G/p)==h for p,h in status['outputs'].items()))
protected=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')['protectedFiles']
check('All82 protected inputs unchanged',len(protected)==82 and all(sha(G/p)==h for p,h in protected.items()))
check('No approval/runtime/balance promotion',all(d[k] is False for d in [internal,public] for k in ['exactRecipeApproval','runtimeImplemented','balanceApproved']))
evidence={'scope':'authored data and independent reference arithmetic only; no runtime execution','versionBoundArtifacts':status['outputs'],'manufacturingCases':craft,'structuralInputs':structural,'structuralReferenceTransitions':transitions,'restorationQuotations':quotes}
dump(A/'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json',evidence)
report={'status':'PASS authored guides/projection and arithmetic checks' if all(x['pass'] for x in checks) else 'CORRECTIONS REQUIRED','checkCount':len(checks),'checks':checks,'failedChecks':[x['name'] for x in checks if not x['pass']],'publicCards':82,'publicBodies':15,'publicBookParagraphs':paragraph_count,'publicComponentOccurrences':285,'supplementalProfilesPublished':profile_count,'supplementalProfilesWithheld':285-profile_count,'manufacturingRows':len(craft),'structuralPositiveInputs':sum(positive.values()),'structuralInputsIncludingZero':len(structural),'structuralReferenceTransitions':len(transitions),'restorationQuotationRows':len(quotes),'evidenceFile':'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json','evidenceSha256':sha(A/'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json'),'versionBoundArtifacts':status['outputs'],'recipesApproved':0,'sourceInformationDeleted':0,'remaining':['Complete source-specified finite physical/qualification sequences and eight joint seams','Separate exact GPT review of every complete card, guide and public envelope','Actual acquisition/runtime/balance and whole-game integration remain later gates'],'limitations':['Reference arithmetic does not prove world records, legitimate materials, runtime execution or balance','Projection withholds supplemental metadata without matching public authority; exact candidate review must assess the whole envelope']}
dump(A/'GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json',report)
print(json.dumps({k:report[k] for k in ['status','checkCount','failedChecks','manufacturingRows','structuralInputsIncludingZero','restorationQuotationRows','recipesApproved']}))
if report['failedChecks']:raise SystemExit(1)
