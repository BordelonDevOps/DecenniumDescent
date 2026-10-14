"""Check the Salvaging source register and tally claims; no card promotion."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json,re

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=read(A/'SALVAGING_SOURCE_CONFERENCE_CAPTURE.json');vp=A/receipt['file'];assert sha(vp)==receipt['sha256']
sp=G/'DescentReviewChanges/ReviewBible/data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
source=read(sp);prepared=read(A/'GATHERING_TOOL_SOURCE_PREPARATION.json');assert sha(sp)==prepared['sourceSha256']
raw={r['id']:r for r in source['recipes'] if r['skill']=='Salvaging'};assert len(raw)==42
assert all(raw[r['id']]==r for r in prepared['recipes'] if r['skill']=='Salvaging')
t=vp.read_text(encoding='utf-8');reg=t.split('## GT-V17')[1].split('## GT-V18')[0]
models={'Refiner':('F',10,6),'Salvaging Kit':('K',25,5),'Separator':('S',15,8),'Extractor':('E',8,3),'Salvage Tool':('T',3,2),'Recovery Rig':('R',50,25)}
checks=[];rows=[]
def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
for line in reg.splitlines():
 if not re.match(r'^\| \d+ \|',line):continue
 c=[x.strip() for x in line.strip('|').split('|')];rid='recipe-'+c[0];r=raw[rid];m=models[r['recipeFamily']];q=r['quantity'];w=r['workRequirements'];e=r['mechanics']
 expected=[c[0],m[0],f"+{e['salvageBonus']} / {e['recoveryPercent']}% / {e['qualityStep']}",f"{r['skillLevel']}/{r['tier']}",f'{q}/{q*3//2}',str(r['craftingCheck']['targetDC']),f"{w['activeWorkHours']}; {str(w['fieldCraftable']).lower()}/{w['timeMode']}",str(w['maximumAssistants']),str(r['skillProgression']['trivialAtSkillLevel'])]
 check(rid+' exact source fields and proposed body/effect mapping',c[:9]==expected)
 check(rid+' original batch reference',Fraction(c[9])==Fraction(str(r['economy']['recommendedMarketValue'])))
 value=Fraction(str(r['economy']['recommendedMarketValue']))/q+m[1]
 check(rid+' finished-unit reference arithmetic',Fraction(c[10])==value)
 rows.append({'recipeId':rid,'bodyCode':m[0],'recoveryPercent':e['recoveryPercent'],'sourceQuantity':q,'reservedBodyCount':q*3//2,'newMundaneBodyValueGp':m[1],'newBodyMassLb':m[2],'finishedReferenceGp':{'numerator':value.numerator,'denominator':value.denominator},'sourceVisibility':r['visibility']})
check('All42 source identities exactly once',len(rows)==42 and {r['recipeId'] for r in rows}==set(raw))
check('Six exact recovery-group counts13/11/6/6/3/3',[sum(r['recoveryPercent']==p for r in rows) for p in [25,35,45,55,65,75]]==[13,11,6,6,3,3])
check('Six exact body counts7/9/10/5/10/1',[sum(r['bodyCode']==b for r in rows) for b in 'FKSETR']==[7,9,10,5,10,1])
check('Bonus counts24/12/6',[sum(r['mechanics']['salvageBonus']==b for r in raw.values()) for b in [1,2,3]]==[24,12,6])
quality={'recipe-'+str(n) for n in list(range(462,471))+[669,670,671]}
check('Exact12 critical-quality sources',{rid for rid,r in raw.items() if r['mechanics']['qualityStep']==1}==quality)
check('No added extraYield field',all('extraYield' not in r['mechanics'] and 'extraYield' not in r['resultItem']['mechanics'] for r in raw.values()))
comps=[(rid,i,c) for rid,r in raw.items() for i,c in enumerate(r['components'])]
nc=[(rid,i,c) for rid,i,c in comps if not c['consumed']];con=[(rid,i,c) for rid,i,c in comps if c['consumed']]
tools=[(rid,i) for rid,i,c in con if c['role']=='tool'];cats=[(rid,i) for rid,i,c in con if c['role']=='catalyst']
check('195 entries /63 nonconsumed /132 consumed',(len(comps),len(nc),len(con))==(195,63,132))
check('All63 nonconsumed entries are tools',all(c['role']=='tool' for _,_,c in nc))
check('Consumed role counts47/37/21/16/6/5',Counter(c['role'] for _,_,c in con)=={'material':47,'vessel':37,'stabilizer':21,'ingredient':16,'tool':6,'catalyst':5})
check('Six exact consumed-tool occurrences',tools==[('recipe-668',1),('recipe-668',2),('recipe-669',1),('recipe-670',1),('recipe-670',2),('recipe-671',1)])
check('Five exact catalyst occurrences',cats==[('recipe-467',7),('recipe-467',8),('recipe-468',6),('recipe-469',5),('recipe-469',6)])
marrow=raw['recipe-462']['components'][5:7]
check('Two separate109gp/.18lb infernal-marrow occurrences',len(marrow)==2 and all(c['id']=='drop-infernal_marrow' and c['quantity']==1 and c['value']==109 and c['weight']==.18 and c['consumed'] for c in marrow) and marrow[0]['legacyName']!=marrow[1]['legacyName'])
check('Exact17 true field flags',{rid for rid,r in raw.items() if r['workRequirements']['fieldCraftable']}=={'recipe-'+str(n) for n in list(range(433,446))+[447,452,454,668]})
public={'recipe-'+str(n) for n in list(range(433,457))+[668]}
check('Exact25 public recipes',{rid for rid,r in raw.items() if r['visibility']=='public'}==public)
check('Exact2 restricted recipes',{rid for rid,r in raw.items() if r['visibility']=='restricted'}=={'recipe-459','recipe-460'})
check('Exact15 Director recipes',{rid for rid,r in raw.items() if r['visibility']=='director-only'}=={'recipe-'+str(n) for n in [457,458]+list(range(461,471))+[669,670,671]})
check('Five public body dependencies',{models[raw[rid]['recipeFamily']][0] for rid in public}==set('FKSET'))
check('Only671 has non-none matrixResearch',{rid for rid,r in raw.items() if r['matrixResearch']['level']!='none'}=={'recipe-671'})
check('Recipe671 source research catalyst flag remains distinct',raw['recipe-671']['matrixResearch']['rareCatalystRequired'] is True and not any(rid=='recipe-671' for rid,_ in cats))
allc=[c for r in prepared['recipes'] for c in r['components']]
check('All three trades reconcile580/213/367/12/10',(len(allc),sum(not c['consumed'] for c in allc),sum(c['consumed'] for c in allc),sum(c['consumed'] and c['role']=='tool' for c in allc),sum(c['role']=='catalyst' for c in allc))==(580,213,367,12,10))
check('Recipe670 finished90820/Broken22705',Fraction(str(raw['recipe-670']['economy']['recommendedMarketValue']))/raw['recipe-670']['quantity']+50==90820 and Fraction(90820,4)==22705)
headings=re.findall(r'^## (GT-V\d{2}) — (.+)$',t,re.M)
check('All18 complete decision sections',[x[0] for x in headings]==['GT-V%02d'%i for i in range(1,19)])
sub=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')
for name,h in sub['protectedFiles'].items():assert sha(G/name)==h,name
check('All82 protected conference inputs unchanged',len(sub['protectedFiles'])==82)
out={'status':'PASS source-verdict register reconciliation only' if all(c['pass'] for c in checks) else 'SOURCE VERDICT CORRECTION REQUIRED','verdictFile':vp.name,'verdictSha256':sha(vp),'sourceFile':str(sp.relative_to(G)).replace('\\','/'),'sourceSha256':sha(sp),'checks':checks,'checkCount':len(checks),'protectedInputsUnchanged':82,'rows':rows,'actualComponentCounts':{'occurrences':len(comps),'nonconsumed':len(nc),'consumed':len(con),'consumedTools':len(tools),'catalysts':len(cats)},'failedChecks':[c['name'] for c in checks if not c['pass']],'decisions':[{'id':i,'heading':h,'status':'source direction; joint reconciliation and exact review remain'} for i,h in headings],'scopeLimits':['No operational cards authored or approved by this check','Body models and procedural completions are NEW reviewer choices','Source register verification does not validate runtime,physical facts,availability,balance or final flow','Cosmology remains post-verified-push'],'recipesApproved':0,'sourceInformationDeleted':0}
(A/'SALVAGING_SOURCE_VERDICT_RECONCILIATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','checkCount','protectedInputsUnchanged','actualComponentCounts','failedChecks','recipesApproved']}))
