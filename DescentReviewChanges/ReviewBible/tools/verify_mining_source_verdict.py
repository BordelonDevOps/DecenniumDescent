"""Verify source-table claims in GPT's verdict; grants no operational approval."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re

GAME=Path(r'C:\Github\DecenniumDescent')
A=GAME/'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt=read(A/'MINING_SOURCE_CONFERENCE_CAPTURE.json')
vp=A/receipt['file']; assert sha(vp)==receipt['sha256']
sourcepath=GAME/'DescentReviewChanges/ReviewBible/data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
source=read(sourcepath)
prepared=read(A/'GATHERING_TOOL_SOURCE_PREPARATION.json')
assert sha(sourcepath)==prepared['sourceSha256']
raw={r['id']:r for r in source['recipes'] if r['skill']=='Mining'}
assert len(raw)==43
assert all(raw[r['id']]==r for r in prepared['recipes'] if r['skill']=='Mining')
text=vp.read_text(encoding='utf-8')
register=text.split('## GT-M17')[1].split('## GT-M18')[0]
parsed=[]
models={'Mining Pick':('P',2,10,5,19),'Gem Cutter':('G',10,2,5,19),'Ore Extractor':('X',8,4,5,19),'Prospecting Tools':('T',25,10,5,15),'Mining Tool':('S',5,3,5,15),'Drill':('D',25,8,5,19)}
checks=[]
def check(name, condition):
    checks.append({'name':name,'pass':bool(condition)})
    assert condition,name
for line in register.splitlines():
    if not re.match(r'^\| \d+ \|',line): continue
    c=[x.strip() for x in line.strip('|').split('|')]
    rid='recipe-'+c[0]; r=raw[rid]; m=models[r['recipeFamily']]
    q=r['quantity'];w=r['workRequirements']; mech=r['mechanics']
    group={1:'A',2:'B',3:'C'}[mech['miningBonus']]
    expected=[c[0],m[0]+'/'+group,f"{r['skillLevel']}/{r['tier']}",f'{q}/{q*3//2}',str(r['craftingCheck']['targetDC']),str(w['activeWorkHours']),str(w['fieldCraftable']).lower()+'/'+w['timeMode'],str(w['maximumAssistants']),str(r['skillProgression']['trivialAtSkillLevel'])]
    check(rid+' source fields and body/effect mapping',c[:9]==expected)
    check(rid+' exact source batch value',Fraction(c[9])==Fraction(str(r['economy']['recommendedMarketValue'])))
    value=Fraction(str(r['economy']['recommendedMarketValue']))/q+m[1]
    check(rid+' finite finished reference arithmetic',Fraction(c[10])==value)
    parsed.append({'recipeId':rid,'bodyCode':m[0],'effectGroup':group,'sourceQuantity':q,'reservedBodyCount':q*3//2,'newMundaneBodyValueGp':m[1],'newBodyMassLb':m[2],'finishedReferenceGp':{'numerator':value.numerator,'denominator':value.denominator},'sourceVisibility':r['visibility']})
check('All43 identities appear exactly once in reviewer register',len(parsed)==43 and {r['recipeId'] for r in parsed}==set(raw))
check('Exact25/13/5 effect distribution',[sum(r['effectGroup']==g for r in parsed) for g in 'ABC']==[25,13,5])
omissions=['recipe-'+str(i) for i in list(range(345,356))+[656,657]]
check('All13 new omission overlays retain both extraYield1 source fields',all(raw[i]['mechanics']['extraYield']==raw[i]['resultItem']['mechanics']['extraYield']==1 and 'additional' not in raw[i]['effects'].lower() for i in omissions))
components=[(r['id'],i,c) for r in raw.values() for i,c in enumerate(r['components'])]
nonconsumed=[(rid,i) for rid,i,c in components if not c['consumed']]
consumedtools=[(rid,i) for rid,i,c in components if c['consumed'] and c['role']=='tool']
catalysts=[(rid,i) for rid,i,c in components if c['role']=='catalyst']
check('193occurrences /67 reusable /126consumed',len(components)==193 and len(nonconsumed)==67 and len(components)-len(nonconsumed)==126)
check('Six exact consumed-tool occurrences',consumedtools==[('recipe-657',1),('recipe-657',2),('recipe-657',3),('recipe-658',3),('recipe-659',1),('recipe-659',3)])
check('Five exact catalyst occurrences',catalysts==[('recipe-353',6),('recipe-355',7),('recipe-356',7),('recipe-357',7),('recipe-357',8)])
check('17true /26false field flags',{rid for rid,r in raw.items() if r['workRequirements']['fieldCraftable']}=={'recipe-'+str(i) for i in list(range(320,335))+[339,343]})
public={'recipe-'+str(i) for i in list(range(320,345))+[347,349,350,656]}
check('Exact29 public formulas', {rid for rid,r in raw.items() if r['visibility']=='public'}==public)
check('Exact2 restricted formulas',{rid for rid,r in raw.items() if r['visibility']=='restricted'}=={'recipe-348','recipe-351'})
check('Exact12 Director formulas',len(raw)-len(public)-2==12)
check('Five actual public body dependencies',{models[raw[rid]['recipeFamily']][0] for rid in public}==set('PGXTS'))
submission=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')
for name,digest in submission['protectedFiles'].items(): assert sha(GAME/name)==digest,name
check('All82 current conference protected inputs unchanged',len(submission['protectedFiles'])==82)
headings=re.findall(r'^## (GT-M\d{2}) — (.+)$',text,re.M)
check('All18 decision sections retained',[h[0] for h in headings]==['GT-M%02d'%i for i in range(1,19)])
out={'status':'PASS source-verdict register reconciliation only','verdictFile':vp.name,'verdictSha256':sha(vp),'sourceFile':str(sourcepath.relative_to(GAME)).replace('\\','/'),'sourceSha256':sha(sourcepath),'checks':checks,'checkCount':len(checks),'protectedInputsUnchanged':82,'rows':parsed,'decisions':[{'id':a,'heading':b,'status':'source-authoring direction; awaiting three-trade reconciliation and exact candidate review'} for a,b in headings],'scopeLimits':['No operational cards authored or approved by this check','New body values are reviewer choices, not recovered source fields','Does not verify runtime, world facts, balance, acquisition or final flow','Cosmology remains post-verified-push'],'recipesApproved':0,'sourceInformationDeleted':0}
write(A/'MINING_SOURCE_VERDICT_RECONCILIATION.json',out)
print(json.dumps({k:out[k] for k in ['status','checkCount','protectedInputsUnchanged','recipesApproved']}))
