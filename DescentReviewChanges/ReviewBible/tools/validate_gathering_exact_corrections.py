"""Current-byte GEX completion gate; reference arithmetic, not a game runtime."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,subprocess,sys,zipfile
from core_playtest_rules import task_check
from build_gathering_tool_internal_draft import card_md
from build_gathering_tool_guides_projection import public_card_md,bodies_md
from apply_gathering_exact_repairs import REPLACEMENTS,SHARED_NEW,MINING_NEW,SUPPLY_NEW,INTERNAL_NEW

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def serial(v):
 if isinstance(v,F):return {'numerator':v.numerator,'denominator':v.denominator}
 if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [serial(x) for x in v]
 return v

def main():
 cap=read(A/'GATHERING_128_EXACT_VERDICT_CAPTURE.json');assert cap['completedFinalResponseCaptured']
 applied=read(A/'GATHERING_128_EXACT_CORRECTIONS_APPLIED.json')
 summary=read(A/'GATHERING_128_EXACT_VERDICT_SCOPE.json')
 assert summary['promotionAfterConditionsAuthorized'] and summary['all128Covered']
 assert applied['corrections']==['GEX-01','GEX-02']
 reports=[]
 for script,out in [('validate_gathering_tool_internal_draft.py','GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json'),('validate_gathering_tool_guides_projection.py','GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json'),('validate_gathering_worked_cases.py','GATHERING_TOOL_WORKED_CASE_VALIDATION.json')]:
  result=subprocess.run([sys.executable,'-X','utf8',str(R/'tools'/script)],capture_output=True,text=True,encoding='utf-8')
  assert result.returncode==0,(script,result.stdout,result.stderr)
  report=read(A/out);assert all(c['pass'] for c in report['checks']) and not report['failedChecks']
  reports.append({'file':rel(A/out),'sha256':sha(A/out),'script':rel(R/'tools'/script),'scriptSha256':sha(R/'tools'/script),'checks':report['checkCount'],'allPassed':True})
 checks=[]
 def check(name,value):checks.append({'name':name,'pass':bool(value)})
 submission=read(A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json')
 status=read(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json')
 internal=read(R/'data/director/gathering_tool_recipe_candidate_internal.json')
 public=read(R/'data/crafting/gathering_tool_recipe_candidate_public.json')
 cards={c['recipeId']:c for c in internal['cards']};pubs={c['recipeId']:c for c in public['cards']}
 raw=read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json');sources={c['id']:c for c in raw['recipes']}
 check('Completed final authority file still exact',sha(A/'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md')==cap['verdictSha256'])
 check('Reviewed v1 archive unchanged',sha(A/submission['bundleFile'])==submission['bundleSha256']==summary['archiveSha256'])
 check('Every protected input unchanged',all(sha(G/p)==h for p,h in submission['protectedFiles'].items()))
 for name in REPLACEMENTS:
  p=R/name;expected=applied['changes'][rel(p)]
  check('Current recorded correction bytes: '+name,sha(p)==expected['afterSha256'])
 with zipfile.ZipFile(A/submission['bundleFile']) as z:
  for p,h in submission['artifactHashes'].items():
   if p not in applied['changes']:check('Unchanged submitted artifact: '+p,sha(G/p)==h)
  for name,pairs in REPLACEMENTS.items():
   p=R/name;old=z.read(rel(p));new=(R/name).read_bytes()
   reconstructed=old.decode('utf-8')
   for a,b in pairs:reconstructed=reconstructed.replace(a,b,1)
   check('Correction-only reversible delta: '+name,reconstructed.encode('utf-8')==new)
 check('All current authoring hashes match',all(sha(G/p)==h for p,h in status['outputs'].items()))
 current_bound=read(A/'GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json')['versionBoundArtifacts']
 check('Fresh reference evidence bound to corrected artifacts',current_bound==status['outputs'] and all(sha(G/p)==h for p,h in current_bound.items()))
 mining_ids=[rid for rid,c in cards.items() if c['sourceRecipe']['skill']=='Mining' and c['sourceRecipe']['recipeFamily'] in ['Gem Cutter','Prospecting Tools','Mining Tool']]
 supply_ids=[rid for rid,c in cards.items() if c['sourceRecipe']['skill']=='Salvaging' and any(x['name'] in ['Purification agent','Stabilizer'] and x['consumed'] for x in c['sourceRecipe']['components'])]
 check('GEX-01 exact26 affected identities and18 public',mining_ids==summary['namedCorrections']['GEX-01']['affectedRecipeIds'] and len(mining_ids)==26 and sum(x in pubs for x in mining_ids)==18)
 check('GEX-02 exact29 affected identities and15 public',supply_ids==summary['namedCorrections']['GEX-02']['affectedRecipeIds'] and len(supply_ids)==29 and sum(x in pubs for x in supply_ids)==15)
 shared=(R/'docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md').read_text(encoding='utf-8')
 mining=(R/'docs/mechanics/MINING_CANDIDATE_GUIDE.md').read_text(encoding='utf-8')
 internalguide=(R/'docs/director-only/GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md').read_text(encoding='utf-8')
 generator=(R/'tools/build_gathering_tool_guides_projection.py').read_text(encoding='utf-8')
 check('Both public training statements explicit',SHARED_NEW in shared and MINING_NEW in mining)
 check('Public/internal/generation supply rules agree',SUPPLY_NEW in shared and INTERNAL_NEW in internalguide and INTERNAL_NEW in generator)
 # These are declared legal-roll premises. The helper does not establish access,
 # stock, operation, entitlement, training, or the truth of a campaign record.
 untrained=task_check(min(17,8),2+1,12)
 check('GEX-01 required17/8,WIS2,item1,DC12 =>11 Failure',untrained=={'total':11,'degree':'failure','success':False})
 check('GEX-01 no proficiency in specified regression',untrained['total']==8+2+1 and untrained['total']!=17+2+1)
 regressions={'GEX-01':{'dice':[17,8],'selectedDie':8,'declaredWIS':2,'declaredEligibleToolBonus':1,'PB':0,'DC':12,'result':untrained,'scope':'Arithmetic with explicit authored eligibility premises, not runtime qualification'}}
 rows=[]
 for rid in ['recipe-433','recipe-668']:
  r=sources[rid]
  for i,c in enumerate(r['components']):
   if not c['consumed']:disposition='retained capital';qty=F(str(c['quantity']))
   else:
    disposition='Failed creation recovered';u=F(1,100) if c['name'] in ['Purification agent','Stabilizer'] else F(1)
    qty=(F(str(c['quantity']))/4//u)*u
   rows.append({'recipeId':rid,'componentIndex':i,'name':c['name'],'consumed':c['consumed'],'sourceQuantity':c['quantity'],'disposition':disposition,'quantity':qty,'massLb':qty*F(str(c['weight']))})
 def row(rid,name):return next(x for x in rows if x['recipeId']==rid and x['name']==name)
 stabilizer=row('recipe-433','Stabilizer');purifier=row('recipe-668','Purification agent')
 check('GEX-02 recipe433 five Stabilizer =>1.25 units/.125lb',(stabilizer['sourceQuantity'],stabilizer['quantity'],stabilizer['massLb'])==(5,F('1.25'),F('.125')))
 check('GEX-02 recipe433 indivisible fang =>0',all(x['quantity']==0 for x in rows if x['recipeId']=='recipe-433' and 'fang' in x['name'].lower()))
 check('GEX-02 retained Weave Filter is capital',any('weave filter' in x['name'].lower() and not x['consumed'] and x['disposition']=='retained capital' for x in rows if x['recipeId']=='recipe-433'))
 check('GEX-02 recipe668 one Purification agent =>.25/.025lb',(purifier['sourceQuantity'],purifier['quantity'],purifier['massLb'])==(1,F('.25'),F('.025')))
 discrete668=[x for x in rows if x['recipeId']=='recipe-668' and x['consumed'] and x['name']!='Purification agent']
 check('GEX-02 recipe668 consumed tools and fused cog =>0',len(discrete668)==3 and all(x['quantity']==0 for x in discrete668))
 mfg=read(A/'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json')['manufacturingCases']
 check('Both Failed batches produce zero enchanted output',all(x['expectedQuantity']==0 for x in mfg if x['recipeId'] in ['recipe-433','recipe-668'] and x['band']=='Failed'))
 regressions['GEX-02']={'sourceBoundComponents':rows,'zeroFinishedOutputs':True,'scope':'Exact-identity arithmetic with source-unit premises; actual receipt, continuing clocks and containment remain required'}
 manuscripts=[]
 for tr in ['Mining','Skinning','Salvaging']:
  for public_view,data,path in [(False,cards,R/f'docs/director-only/{tr.upper()}_INTERNAL_RECIPE_CARDS.md'),(True,pubs,R/f'docs/mechanics/{tr.upper()}_CANDIDATE_RECIPE_CARDS.md')]:
   text=path.read_text(encoding='utf-8');parts=re.split(r'^## (.+?) — (recipe-\d+)\s*\n',text,flags=re.M)
   for n in range(1,len(parts),3):
    name,rid,body=parts[n:n+3];c=data[rid];b=internal['baseModels'][c['operational']['baseModelIds'][0]]
    expected=public_card_md(c,b,cards[rid]) if public_view else card_md(c,b)
    manuscripts.append({'recipeId':rid,'audience':'public' if public_view else 'internal','pass':expected.rstrip()==('## '+name+' — '+rid+'\n\n'+body).rstrip()})
 check('Complete210 manuscript sections still equal inspected generation',len(manuscripts)==210 and all(x['pass'] for x in manuscripts))
 for is_public,obj,name in [(False,internal,'docs/director-only/GATHERING_TOOL_INTERNAL_BODY_CATALOGUE.md'),(True,public,'docs/mechanics/GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md')]:
  check('Complete body catalogue: '+name,bodies_md(obj['baseModels'],obj['auxiliaryModels'],not is_public).rstrip()==(R/name).read_text(encoding='utf-8').rstrip())
 check('Restricted profiles remain withheld',all('publicMaterialProfile' not in pubs[rid]['sourceRecipe']['components'][i] for rid,i in [('recipe-333',1),('recipe-436',2)]))
 check('Exact public identity boundary preserved',set(pubs)=={rid for rid,c in cards.items() if c['visibility']=='public'} and len(pubs)==82)
 artifacts={p:sha(G/p) for p in submission['artifactHashes']}
 auxiliary={rel(R/name):sha(R/name) for name in REPLACEMENTS if rel(R/name) not in artifacts}
 evidence={'status':'PASS' if all(x['pass'] for x in checks) else 'CORRECTIONS REQUIRED','completionGateSatisfied':all(x['pass'] for x in checks),'authority':applied['authority'],'conditionsSatisfied':['GEX-01','GEX-02'] if all(x['pass'] for x in checks) else [],'existingSuites':reports,'existingChecks':sum(x['checks'] for x in reports),'focusedChecks':len(checks),'checks':checks,'failedChecks':[x['name'] for x in checks if not x['pass']],'regressions':serial(regressions),'completeManuscriptChecks':manuscripts,'artifactHashes':artifacts,'generationHashes':auxiliary,'validatorSha256':sha(Path(__file__)),'protectedInputsUnchanged':len(submission['protectedFiles']),'recipesPromoted':0,'runtimeImplemented':False,'humanBalanceApproved':False,'scope':'Authored rule carry-through, exact file/source parity and reference arithmetic; no campaign-fact authentication'}
 dump(A/'GATHERING_128_EXACT_COMPLETION_VALIDATION.json',evidence)
 print(json.dumps({k:evidence[k] for k in ['status','completionGateSatisfied','existingChecks','focusedChecks','failedChecks','recipesPromoted']}))
 assert evidence['completionGateSatisfied']

if __name__=='__main__':main()
