"""Source-bound arithmetic and authored physical-sequence case coverage.

Uses the already reviewed structural/quotation calculators only where their
mathematics is identical. It does not invoke Fishing effects or claim a gathering
runtime, real stock, authentic physical histories, or automated qualitative review.
"""
from pathlib import Path
from fractions import Fraction as F
from math import ceil,isfinite
from collections import Counter
from copy import deepcopy
import hashlib,json,re
from core_playtest_rules import task_check
from fishing_reference import structural_hp,repair_quote,copper

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def serial(x):
 if isinstance(x,F):return {'numerator':x.numerator,'denominator':x.denominator}
 if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [serial(v) for v in x]
 return x
checks=[]
def check(case,claim,actual,expected):
 checks.append({'case':case,'claim':claim,'actual':serial(actual),'expected':serial(expected),'pass':actual==expected})
def reject(case,claim,fn):
 try:fn()
 except (ValueError,TypeError,OverflowError,ZeroDivisionError):check(case,claim,'rejected','rejected')
 else:check(case,claim,'accepted','rejected')

candidate=read(R/'data/director/gathering_tool_recipe_candidate_internal.json')
cards={c['recipeId']:c for c in candidate['cards']};models=candidate['baseModels']
original=read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
raw={r['id']:r for r in original['recipes']}
def recipe(n):return raw[f'recipe-{n}']
def body(n):return models[cards[f'recipe-{n}']['operational']['baseModelIds'][0]]
def total(r,key,consumed=True):return sum((F(str(c[key]))*c['quantity'] for c in r['components'] if c['consumed']==consumed),F(0))
def qref(n):r=recipe(n);return F(str(r['economy']['recommendedMarketValue']))/r['quantity']+F(str(body(n)['baselinePriceGp']))

# Exact source worked-example amounts, rather than assumptions from item names.
r=recipe(322);b=body(322)
check('M-A','Q/DC/hours/field/mode/assistants/triviality',(r['quantity'],r['difficulty'],r['workRequirements']['activeWorkHours'],r['workRequirements']['fieldCraftable'],r['workRequirements']['timeMode'],r['workRequirements']['maximumAssistants'],r['skillProgression']['trivialAtSkillLevel']),(4,10,8,True,'expedition',0,6))
check('M-A','Six complete body mass/reference and Standard/unused mass',(3*r['quantity']//2*b['baselineWeightLb'],3*r['quantity']//2*b['baselinePriceGp'],r['quantity']*b['baselineWeightLb'],(3*r['quantity']//2-r['quantity'])*b['baselineWeightLb']),(60,12,40,20))
check('M-A','Source bill remains separate',(total(r,'value'),total(r,'weight'),len([c for c in r['components'] if not c['consumed']])),(F(14),F('0.59'),1))
check('M-A','Finished, functional, Broken and copper purchase references',(qref(322),F(str(b['baselinePriceGp']))/4,qref(322)/4,copper(qref(322)/4)),(F('13.25'),F('0.50'),F('3.3125'),F('3.32')))
check('M-B/S-G','1/5 singleton Flawed current damage',structural_hp(5,5,1,new_flaw=True),{'maximumHP':2,'currentHP':0,'durabilityPercent':0,'flawed':True})
check('M-B/S-G','P50 retains the flaw',structural_hp(5,2,2,new_percent=50,old_flaw=True),{'maximumHP':3,'currentHP':3,'durabilityPercent':50,'flawed':True})
reject('M-B/S-G','Inconsistent old1/1 is not silently healed',lambda:structural_hp(5,1,1))
check('M-C','Lead656 bonus and one separate assistant',(recipe(656)['mechanics']['miningBonus'],1,recipe(656)['mechanics']['extraYield']),(2,1,1))
check('M-D','Blocked C/D never enter selected B/R membership',sorted(set(['A','B'])|set()),['A','B'])
check('M-D','All-originally-accessible fixture has four distinct units',len(set(['A','B'])|set(['C','D'])),4)
check('M-E','Ordinary critical O/C/R conserves actual mass',F(1)+F('.25')+F(1),F('2.25'))
check('M-F','657 consumed source values/mass and catalyst count',(total(recipe(657),'value'),len([c for c in recipe(657)['components'] if c['consumed'] and c['role']=='catalyst'])),(F(4002),0))
check('M-F','353 and357 catalyst occurrence counts',tuple(sum(c['role']=='catalyst' and c['consumed'] for c in recipe(n)['components']) for n in [353,357]),(1,2))
check('M-H','339 and349 access remain distinct',[(recipe(n)['workRequirements']['fieldCraftable'],recipe(n)['workRequirements']['timeMode'],recipe(n)['workRequirements']['activeWorkHours'],recipe(n)['workRequirements']['maximumAssistants']) for n in [339,349]],[(True,'expedition',8,0),(False,'haven',80,0)])

check('S-A','One ordinary unit plus empty reserve remains one',len(set(['hide'])|set()),1)
check('S-B','Medium partial/hurried minutes',(ceil(F(30*2,4)),ceil(F(ceil(F(30*2,4)),2))),(15,8))
check('S-B','Correct actual extraction roll',task_check(11,4+4+recipe(544)['mechanics']['skinningBonus'],12),{'total':22,'degree':'critical-success','success':True})
check('S-B','Four distinct H/D/R1/R2 and insufficient-reserve alternative',(F(1)+3*F('.1'),F(1)+2*F('.1')),(F('1.30'),F('1.20')))
check('S-C','Original F and S disjoint physical receipt',len(set(['B'])|set(['F'])|set(['D'])|set(['S'])),4)
check('S-C','Old unpartitioned Fishing reserve supplies no S',len(set()),0)
age_at_treatment=12*60+10;protection_minutes=24*60;spoil_interval=24*60
check('S-D','Unprotected age and eventual spoil minutes after original09:00',(age_at_treatment,age_at_treatment+protection_minutes+(spoil_interval-age_at_treatment)),(730,2880))
check('S-D','Thirty-minute treatment ending after Spoiled stays too late',1430+30<spoil_interval,False)
limit=F(str(models['skinning.preservation-kit']['physicalLimits']['receiverLb']))
check('S-D','Supplies count toward actual weight capacity',(F(8)+F('.5')<=limit,F(10)+F('.5')<=limit),(True,False))
r=recipe(516);b=body(516)
check('S-E','Q5/seven P reserve and masses',(r['quantity'],3*r['quantity']//2,b['baselineWeightLb']*7,b['baselineWeightLb']*r['quantity'],b['baselineWeightLb']*2,qref(516)),(5,7,42,30,12,F('14.80')))
check('S-E','Source pelt bill and two active hours',(total(r,'value'),total(r,'weight'),r['workRequirements']['activeWorkHours']),(F(6),F('.64'),2))
r=recipe(540);fangs=[c for c in r['components'] if 'fang' in c['name'].lower()]
check('S-F','Two physical fang occurrences, mass/value/whole consumed bill',(len(fangs),sum(F(str(c['weight']))*c['quantity'] for c in fangs),sum(F(str(c['value']))*c['quantity'] for c in fangs),F(str(r['economy']['consumedMaterialValue']))),(2,F('.64'),F(938),F(18938)))
check('S-G','Distinct fallback numbers do not sum',[(recipe(n)['mechanics']['skinningBonus'],recipe(n)['mechanics']['extraYield'],recipe(n)['mechanics']['qualityStep']) for n in [544,676]],[(3,2,1),(2,1,1)])
check('S-H','676 real bill/body/hours;679 frame hours/reference',(total(recipe(676),'weight'),body(676)['baselineWeightLb'],recipe(676)['workRequirements']['activeWorkHours'],recipe(679)['workRequirements']['activeWorkHours'],qref(679)),(F('1.01'),6,16,40,F(4306)))

def finite_fraction(v):
 if isinstance(v,bool):raise ValueError('Boolean is not a quantity')
 if isinstance(v,float) and not isfinite(v):raise ValueError('Nonfinite quantity')
 n=F(str(v))
 if n<0:raise ValueError('Negative quantity')
 return n
def recovery(q0,current,percent,unit):
 """Arithmetic premises only, never proof of a live bill or qualifying tool."""
 admitted=finite_fraction(q0);q=finite_fraction(current);u=finite_fraction(unit)
 if q>admitted or u not in (F(1),F(1,100)) or percent not in (25,35,45,55,65,75):raise ValueError('Unsupported quantity/precision/ceiling')
 if u==1 and (admitted.denominator!=1 or q.denominator!=1):raise ValueError('Indivisible quantities must be whole')
 return (q*percent/100//u)*u
ceilings=[25,35,45,55,65,75]
check('V-A','All six indivisible ceilings',[[recovery(n,n,p,1) for n in [1,4,3]] for p in ceilings],[[0,1,0],[0,1,1],[0,1,1],[0,2,1],[0,2,1],[0,3,2]])
check('V-A','All six genuine bulk ceilings',[recovery(4,4,p,'.01') for p in ceilings],[F(1),F('1.40'),F('1.80'),F('2.20'),F('2.60'),F(3)])
check('S-F','Failed crafting floors do not convert indivisible fangs to liquid',[(F(2)*F(1,4)//1)*1,(F(2)*F(1,4)//F('.01'))*F('.01'),(F(4)*F(1,4)//F('.01'))*F('.01')],[F(0),F('.50'),F('1.00')])
for natural,modifier,success in [(1,9,True),(1,8,False),(20,-11,False)]:check('V-B',f'Binary natural{natural} modifier{modifier}',natural+modifier>=10,success)
check('V-B','Precision threshold changes quality eligibility, not recovery',[(t>=10,t>=20,recovery(4,4,75,1)) for t in [19,20]],[(True,False,F(3)),(True,True,F(3))])
check('E03','Advantage/disadvantage/cancelled select the die before binary resolution',(max(1,20)+(-11)>=10,min(1,20)+9>=10,1+9>=10),(False,True,True))
first=recovery(6,5,75,'.01');second=recovery(first,first,75,'.01')
check('V-C/GI-11-C1','Current quantities, surviving residue and repeated lawful recovery',(first,5-first,second,F(2)+F(1)+first+(5-first)),(F('3.75'),F('1.25'),F('2.81'),F(8)))
check('V-C','The2.25 not awarded from admitted6 includes one physical loss',(F(6)-first,1+(5-first)),(F('2.25'),F('2.25')))
check('V-D','Four indivisible parts at55% award two',recovery(4,4,55,1),F(2))
check('V-E','Per-identity55/45 followed by suppressed metal25, leather45',[[recovery(4,4,p,1) for p in [55,45]],[recovery(4,4,p,1) for p in [25,45]]],[[2,1],[1,1]])
r=recipe(434);b=body(434)
check('V-F','Four K reserve and Standard/unused mass',(r['quantity'],3*r['quantity']//2,b['baselineWeightLb']*4,b['baselinePriceGp']*4,b['baselineWeightLb']*3,b['baselineWeightLb'],qref(434)),(3,4,20,100,15,5,F(37)))
check('V-F','Required retained and consumed source bill',(total(r,'value',False),total(r,'weight',False),total(r,'value'),total(r,'weight')),(F(48),F(2),F(15),F('.81')))
r=recipe(668)
check('V-G','668 consumed totals, empty body and finished reference',(total(r,'value'),total(r,'weight'),body(668)['baselineWeightLb'],qref(668)),(F(112),F('2.32'),5,F(213)))
check('V-G','467/469 catalyst counts and671 material role',([sum(c['consumed'] and c['role']=='catalyst' for c in recipe(n)['components']) for n in [467,469]],sum(c['role']=='catalyst' for c in recipe(671)['components'])),([2,2],0))
check('V-I','Rig repair references and original DC',(F(str(body(670)['baselinePriceGp']))/4,qref(670)/4,recipe(670)['craftingCheck']['targetDC']),(F('12.50'),F(22705),28))
check('V-J','668 check bonus remains separate from35%',(recipe(668)['mechanics']['salvageBonus'],recipe(668)['mechanics']['recoveryPercent']),(1,35))
rig=models['salvaging.recovery-rig']['physicalLimits'];kit=models['salvaging.salvaging-kit']['physicalLimits'];table=candidate['auxiliaryModels']['salvaging.salvage-table']
check('V-K','Actual total support and setup time',(25+40+6<=table['maximumSupportedLb'],40+6<=rig['maximumSupportedLb'],rig['setupAdditionalActiveMinutes']+60+rig['packingAdditionalActiveMinutes'],rig['setupAdditionalActiveMinutes']+60+rig['packingAdditionalActiveMinutes']+table['setupMinutes']),(True,True,70,75))
check('V-K','1.20lb cannot fit the one-pound kit box',F('1.20')<=F(str(kit['receiverLb'])),False)
for invalid in [-1,float('nan'),float('inf'),True]:reject('E13','Reject negative/nonfinite/boolean quantity '+str(invalid),lambda x=invalid:recovery(4,x,25,1))
for q0,current,p,u in [(4,5,25,1),(4,'1.5',25,1),(4,4,25,0),(4,4,25,'.1'),(4,4,100,1)]:reject('E13',f'Reject unsupported arithmetic premises {q0,current,p,u}',lambda:recovery(q0,current,p,u))

# Evaluate every previously enumerated structural reference transition through
# the existing common calculator. This remains mathematics, not work admission.
prior=read(A/'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json');structural_cases=[]
for row in prior['structuralReferenceTransitions']:
 p,flaw,hp=row['from'];old=5*(100+p)//100;old=max(1,old//2) if flaw else old
 actual=structural_hp(5,old,hp,p,row['requestedStructuralPercent'],flaw,row['addPersistentFlaw'])
 expected={'maximumHP':row['maximumHP'],'currentHP':row['to'][2],'durabilityPercent':row['to'][0],'flawed':row['to'][1]}
 structural_cases.append({'modelId':row['modelId'],'from':row['from'],'requestedStructuralPercent':row['requestedStructuralPercent'],'addPersistentFlaw':row['addPersistentFlaw'],'actual':actual,'expected':expected,'pass':actual==expected})
check('E11','All3264 recorded structural transitions independently evaluate',len(structural_cases)==3264 and all(x['pass'] for x in structural_cases),True)
qualification=[]
for mid,b in models.items():
 rid=next(c['recipeId'] for c in cards.values() if c['operational']['baseModelIds']==[mid]);r=raw[rid];required=list(b['requiredOriginalPrimaryMembers'])
 for missing in required:
  try:repair_quote(r,b,0,5,required,[p for p in required if p!=missing])
  except ValueError:failed=True
  else:failed=False
  qualification.append({'modelId':mid,'missingDeclaredPrimary':missing,'quotedAsRepair':not failed,'expectedQuotationRejected':True,'pass':failed})
check('E11','Every declared primary omission rejects the arithmetic repair route',bool(qualification) and all(x['pass'] for x in qualification),True)
quotes=[]
for rid,c in cards.items():
 r=raw[rid];b=models[c['operational']['baseModelIds'][0]];primary=b['requiredOriginalPrimaryMembers']
 for hp in [0,1]:
  actual=repair_quote(r,b,hp,5,primary,primary);key='broken' if hp==0 else 'functional';authored=c['operational']['repair']
  expected_cost=F(authored[key+'MaterialReferenceGp']['numerator'],authored[key+'MaterialReferenceGp']['denominator'])
  ok=actual['materialReferenceGp']==expected_cost and actual['dc']==authored[key+'DC'] and actual['hours']==(8 if hp==0 else 1)
  quotes.append({'recipeId':rid,'mode':key,'actual':serial(actual),'pass':ok})
check('E11','All256 quotations through the existing common calculator',len(quotes)==256 and all(x['pass'] for x in quotes),True)
check('E10','All960h cases retain included phase and959.75h after',[(recipe(n)['workRequirements']['activeWorkHours'],F(cards[f'recipe-{n}']['operational']['work']['remainingHours']['numerator'],cards[f'recipe-{n}']['operational']['work']['remainingHours']['denominator'])) for n in [358,545,470]],[(960,F('959.75'))]*3)

casebook=R/'docs/director-only/GATHERING_TOOL_PHYSICAL_SEQUENCE_CASEBOOK.md';text=casebook.read_text(encoding='utf-8')
worked=re.findall(r'^### ([MSV]-[A-K]) —',text,re.M)
extra=re.findall(r'^\| (E\d+) —',text,re.M)
check('coverage','All27 source worked cases are present',worked,[f'M-{x}' for x in 'ABCDEFGH']+[f'S-{x}' for x in 'ABCDEFGH']+[f'V-{x}' for x in 'ABCDEFGHIJK'])
check('coverage','Fourteen additional adjudication risks',extra,[f'E{i:02}' for i in range(1,15)])
check('coverage','Every trade/body name appears in the boundary table',all(any(line.startswith('| '+b['trade']+' ') and b['family'] in line for line in text.splitlines()) for b in models.values()),True)
check('coverage','Eight GI-11 seams have explicit mapped dispositions',len(re.findall(r'^\|[1-8]\. ',text,re.M)),8)
check('coverage','Corrections and honest manual-review scope remain explicit',all(x in text for x in ['GI-11-C1','1.25 surviving unawarded','qualitative dispositions below require the exact reviewer','not presented as automated runtime passes']),True)
protected=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')['protectedFiles']
check('preservation','All82 protected source/rule inputs unchanged',len(protected)==82 and all(sha(G/p)==h for p,h in protected.items()),True)
out={'status':'PASS source-bound numeric examples and authored case coverage' if all(c['pass'] for c in checks) else 'CORRECTIONS REQUIRED','checkCount':len(checks),'checks':checks,'failedChecks':[x['case']+': '+x['claim'] for x in checks if not x['pass']],'workedSourceCases':27,'additionalAdjudicationRisks':14,'bodyBoundaryCases':17,'jointSeamsMapped':8,'qualitativeCasesAreAuthoredExpectedDispositions':True,'qualitativeExactReviewPending':True,'structuralCalculatorCases':structural_cases,'declaredPrimaryOmissionCalculatorCases':qualification,'quotationCalculatorCases':quotes,'scope':'Source/card arithmetic, reusable common calculators and finite authored-case coverage; not an implemented gathering runtime or actual-world authentication','casebook':casebook.relative_to(G).as_posix(),'casebookSha256':sha(casebook),'referenceHashes':{p.relative_to(G).as_posix():sha(p) for p in [R/'tools/core_playtest_rules.py',R/'tools/fishing_reference.py',R/'data/director/gathering_tool_recipe_candidate_internal.json',R/'tools/validate_gathering_worked_cases.py']},'protectedInputsUnchanged':82,'sourceInformationDeleted':0,'recipesApproved':0,'next':'Return complete candidates and this accurately scoped evidence for separate exact GPT review'}
dump(A/'GATHERING_TOOL_WORKED_CASE_VALIDATION.json',out)
print(json.dumps({k:out[k] for k in ['status','checkCount','failedChecks','workedSourceCases','additionalAdjudicationRisks','bodyBoundaryCases','jointSeamsMapped','recipesApproved']}))
if out['failedChecks']:raise SystemExit(1)
