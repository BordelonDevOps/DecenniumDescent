"""Independent source/register/manuscript checks for the initial128-card draft.

This check remains limited to source/register/manuscript parity. The separate
guide/projection validator covers its own scope; exact approval remains pending.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(d):return F(d['numerator'],d['denominator'])
d=read(R/'data/director/gathering_tool_recipe_candidate_internal.json')
source=read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes'];raw={r['id']:r for r in source}
prepared=read(A/'GATHERING_TOOL_SOURCE_PREPARATION.json');bindings={x['recipeId']:x for x in prepared['publicBookBindings']}
register={r['recipeId']:r for tr in ['MINING','SKINNING','SALVAGING'] for r in read(A/(tr+'_SOURCE_VERDICT_RECONCILIATION.json'))['rows']}
checks=[]
def check(n,v):checks.append({'name':n,'pass':bool(v)})
check('Exactly128 unique complete source identities',len(d['cards'])==128 and {c['recipeId'] for c in d['cards']}==set(register))
texts={tr:(R/f'docs/director-only/{tr.upper()}_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8') for tr in ['Mining','Skinning','Salvaging']}
for c in d['cards']:
 rid=c['recipeId'];r=raw[rid];o=c['operational'];b=d['baseModels'][o['baseModelIds'][0]];v=register[rid];q=r['quantity'];tr=r['skill']
 check(rid+' lossless original source, index and full book binding',c['sourceRecipe']==r and source[c['sourceRecipeIndex']]==r and c['sourceRecipeIndex']==prepared['sourceIndices'][rid] and c['publicBookBinding']==bindings.get(rid))
 check(rid+' independently reviewed body and finished reference',b['code']==v['bodyCode'] and b['baselinePriceGp']==v['newMundaneBodyValueGp'] and b['baselineWeightLb']==v['newBodyMassLb'] and frac(o['finishedUnitReferenceGp'])==frac(v['finishedReferenceGp']))
 check(rid+' source requirements, quantities and repair quotations',o['work']['sourceActiveHours']==r['workRequirements']['activeWorkHours'] and o['work']['fieldCraftable']==r['workRequirements']['fieldCraftable'] and o['work']['timeMode']==r['workRequirements']['timeMode'] and o['work']['requiredTools']==r['workRequirements']['requiredTools'] and o['work']['station']==r['workRequirements']['station'] and o['work']['maximumAssistants']==r['workRequirements']['maximumAssistants'] and o['work']['trivialAtSkillLevel']==r['skillProgression']['trivialAtSkillLevel'] and o['maximumOrderedBodyReserve']==v['reservedBodyCount'] and frac(o['repair']['functionalMaterialReferenceGp'])==F(str(b['baselinePriceGp']))/4 and frac(o['repair']['brokenMaterialReferenceGp'])==frac(v['finishedReferenceGp'])/4 and o['repair']['brokenDC']==r['craftingCheck']['targetDC'])
 ek={'Mining':'miningBonus','Skinning':'skinningBonus','Salvaging':'salvageBonus'}[tr]
 check(rid+' exact printed numeric effects',o['effect']['checkBonus']==r['mechanics'][ek] and o['effect']['qualityStep']==r['mechanics']['qualityStep'] and (o['effect']['recoveryPercent']==r['mechanics']['recoveryPercent'] if tr=='Salvaging' else o['effect']['extraYield']==r['mechanics'].get('extraYield',0)))
 section=texts[tr].split(f"## {r['name']} — {rid}\n",1)[1].split('\n## ',1)[0]
 check(rid+' exact effect and complete occurrence table in manuscript',o['text'] in section and r['effects'] in section and b['operationalBodyText'] in section and all(f"| {i} | " in section and x['id'] in section for i,x in enumerate(r['components'])))
 check(rid+' no promotion or source-flag relabeling',c['status']==d['status'] and c['sourceRecipe'].get('status')==r.get('status') and c['sourceRecipe'].get('needsReview')==r.get('needsReview') and c['visibility']==r['visibility'])
for tr,count in [('Mining',43),('Skinning',43),('Salvaging',42)]:
 ids=re.findall(r'^## .+ — (recipe-\d+)\s*$',texts[tr],re.M)
 check(tr+' exact manuscript membership',len(ids)==count and set(ids)=={c['recipeId'] for c in d['cards'] if c['sourceRecipe']['skill']==tr})
check('All17 physical families represented',len(d['baseModels'])==17 and set(d['baseModels'])=={c['operational']['baseModelIds'][0] for c in d['cards']})
check('Audience membership retained82/6/40',[sum(c['visibility']==v for c in d['cards']) for v in ['public','restricted','director-only']]==[82,6,40])
check('All580 ingredient occurrences retained',sum(len(c['sourceRecipe']['components']) for c in d['cards'])==580)
check('Exact approval, runtime and balance remain false',d['exactRecipeApproval'] is False and d['runtimeImplemented'] is False and d['balanceApproved'] is False)
protected=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')['protectedFiles']
check('All82 protected inputs unchanged',len(protected)==82 and all(sha(G/p)==h for p,h in protected.items()))
out={'status':'PASS internal source/register/manuscript checks' if all(x['pass'] for x in checks) else 'INTERNAL DRAFT CORRECTIONS REQUIRED','checkCount':len(checks),'checks':checks,'failedChecks':[x['name'] for x in checks if not x['pass']],'cardsChecked':128,'protectedInputsUnchanged':82,'sourceInformationDeleted':0,'recipesApproved':0,'limits':['Complete physical sequence and cross-trade validation remains pending','Public guide/projection evidence is separately recorded in GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json','Joint source directions are reconciled; exact GPT card review remains pending','No runtime, availability or balance certification']}
(A/'GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','checkCount','cardsChecked','failedChecks','recipesApproved']}))
