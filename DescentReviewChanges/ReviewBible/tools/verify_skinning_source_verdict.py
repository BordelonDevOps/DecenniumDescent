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
receipt=read(A/'SKINNING_SOURCE_CONFERENCE_CAPTURE.json')
vp=A/receipt['file']; assert sha(vp)==receipt['sha256']
erratum_receipt=read(A/'SALVAGING_SOURCE_CONFERENCE_CAPTURE.json')
erratum_source=A/erratum_receipt['file'];assert sha(erratum_source)==erratum_receipt['sha256']
erratum=(A/'GPT_SKINNING_SOURCE_TALLY_ERRATUM.md').read_text(encoding='utf-8')
assert erratum==erratum_source.read_text(encoding='utf-8').split('\n---\n',1)[0]+'\n'
assert '192 component occurrences / 109 consumed rows' in erratum
sourcepath=GAME/'DescentReviewChanges/ReviewBible/data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
source=read(sourcepath)
prepared=read(A/'GATHERING_TOOL_SOURCE_PREPARATION.json')
assert sha(sourcepath)==prepared['sourceSha256']
raw={r['id']:r for r in source['recipes'] if r['skill']=='Skinning'}
assert len(raw)==43
assert all(raw[r['id']]==r for r in prepared['recipes'] if r['skill']=='Skinning')
text=vp.read_text(encoding='utf-8')
register=text.split('## GT-S17')[1].split('## GT-S18')[0]
parsed=[]
models={'Skinning Knife':('K',1,.25,5,19),'Hide Scraper':('H',1,1,5,19),'Scale Remover':('R',2,1,5,19),'Tanning Tools':('T',8,8,5,15),'Preservation Kit':('P',10,6,5,19)}
checks=[]
def check(name, condition):
    checks.append({'name':name,'pass':bool(condition)})
for line in register.splitlines():
    if not re.match(r'^\| \d+ \|',line): continue
    c=[x.strip() for x in line.strip('|').split('|')]
    rid='recipe-'+c[0]; r=raw[rid]; m=models[r['recipeFamily']]
    q=r['quantity'];w=r['workRequirements']; mech=r['mechanics']
    group={1:'A',2:'B',3:'C'}[mech['skinningBonus']]
    expected=[c[0],m[0]+'/'+group,f"{r['skillLevel']}/{r['tier']}",f'{q}/{q*3//2}',str(r['craftingCheck']['targetDC']),str(w['activeWorkHours']),str(w['fieldCraftable']).lower()+'/'+w['timeMode'],str(w['maximumAssistants']),str(r['skillProgression']['trivialAtSkillLevel'])]
    check(rid+' source fields and body/effect mapping',c[:9]==expected)
    check(rid+' exact source batch value',Fraction(c[9])==Fraction(str(r['economy']['recommendedMarketValue'])))
    value=Fraction(str(r['economy']['recommendedMarketValue']))/q+m[1]
    check(rid+' finite finished reference arithmetic',Fraction(c[10])==value)
    parsed.append({'recipeId':rid,'bodyCode':m[0],'effectGroup':group,'sourceQuantity':q,'reservedBodyCount':q*3//2,'newMundaneBodyValueGp':m[1],'newBodyMassLb':m[2],'finishedReferenceGp':{'numerator':value.numerator,'denominator':value.denominator},'sourceVisibility':r['visibility']})
check('All43 identities appear exactly once in reviewer register',len(parsed)==43 and {r['recipeId'] for r in parsed}==set(raw))
check('Exact27/12/4 effect distribution',[sum(r['effectGroup']==g for r in parsed) for g in 'ABC']==[27,12,4])
check('Exact9/13/9/7/5 body distribution',[sum(r['bodyCode']==g for r in parsed) for g in 'KHRTP']==[9,13,9,7,5])
omissions=['recipe-'+str(i) for i in list(range(532,542))+[676,679]]
check('All12 new omission overlays retain both extraYield1 source fields',all(raw[i]['mechanics']['extraYield']==raw[i]['resultItem']['mechanics']['extraYield']==1 and 'additional' not in raw[i]['effects'].lower() for i in omissions))
components=[(r['id'],i,c) for r in raw.values() for i,c in enumerate(r['components'])]
nonconsumed=[(rid,i) for rid,i,c in components if not c['consumed']]
consumedtools=[(rid,i) for rid,i,c in components if c['consumed'] and c['role']=='tool']
catalysts=[(rid,i) for rid,i,c in components if c['role']=='catalyst']
check('Confirmed erratum:192 occurrences /83 reusable /109 consumed',len(components)==192 and len(nonconsumed)==83 and len(components)-len(nonconsumed)==109)
check('Zero consumed-tool occurrences',consumedtools==[])
check('Zero catalyst occurrences',catalysts==[])
check('All83 nonconsumed occurrences are tools',all(c['role']=='tool' for _,_,c in components if not c['consumed']))
check('20true /23false field flags',{rid for rid,r in raw.items() if r['workRequirements']['fieldCraftable']}=={'recipe-'+str(i) for i in list(range(507,522))+[524,527,530,677,678]})
public={'recipe-'+str(i) for i in list(range(507,532))+[676,677,678]}
check('Exact28 public formulas', {rid for rid,r in raw.items() if r['visibility']=='public'}==public)
check('Exact2 restricted formulas',{rid for rid,r in raw.items() if r['visibility']=='restricted'}=={'recipe-532','recipe-535'})
check('Exact13 Director formulas',len(raw)-len(public)-2==13)
check('Five actual public body dependencies',{models[raw[rid]['recipeFamily']][0] for rid in public}==set('KHRTP'))
fangs=raw['recipe-540']['components'][6:8]
check('Two separate original eldritch-fang occurrence units',len(fangs)==2 and all(c['id']=='drop-eldritch_fang' and c['quantity']==1 and c['weight']==.32 and c['value']==469 and c['consumed'] for c in fangs) and fangs[0]['legacyName']!=fangs[1]['legacyName'])
check('Recipe540 original consumed value18938',raw['recipe-540']['economy']['consumedMaterialValue']==18938)
check('Recipe676 original consumed mass1.01lb',raw['recipe-676']['economy']['consumedWeight']==1.01)
submission=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')
for name,digest in submission['protectedFiles'].items(): assert sha(GAME/name)==digest,name
check('All82 current conference protected inputs unchanged',len(submission['protectedFiles'])==82)
headings=re.findall(r'^## (GT-S\d{2}) — (.+)$',text,re.M)
check('All18 decision sections retained',[h[0] for h in headings]==['GT-S%02d'%i for i in range(1,19)])
out={'status':'PASS source-verdict register reconciliation only' if all(c['pass'] for c in checks) else 'SOURCE VERDICT CORRECTION REQUIRED','verdictFile':vp.name,'verdictSha256':sha(vp),'sourceFile':str(sourcepath.relative_to(GAME)).replace('\\','/'),'sourceSha256':sha(sourcepath),'checks':checks,'checkCount':len(checks),'protectedInputsUnchanged':82,'rows':parsed,'actualComponentCounts':{'occurrences':len(components),'nonconsumed':len(nonconsumed),'consumed':len(components)-len(nonconsumed),'consumedTools':len(consumedtools),'catalysts':len(catalysts)},'failedChecks':[c['name'] for c in checks if not c['pass']],'decisions':[{'id':a,'heading':b,'status':'source-authoring direction; awaiting source erratum, three-trade reconciliation and exact candidate review'} for a,b in headings],'scopeLimits':['No operational cards authored or approved by this check','New body values are reviewer choices, not recovered source fields','Does not verify runtime, world facts, balance, acquisition or final flow','Cosmology remains post-verified-push'],'recipesApproved':0,'sourceInformationDeleted':0}
out['confirmedTallyErratum']={'file':'GPT_SKINNING_SOURCE_TALLY_ERRATUM.md','sourceVerdictFile':erratum_source.name,'sourceVerdictSha256':sha(erratum_source),'replyId':erratum_receipt['replyId'],'originalFailedCheckEvidence':'skinning-before-confirmed-tally-erratum/SKINNING_SOURCE_VERDICT_RECONCILIATION.json','originalVerdictUnchanged':True}
for d in out['decisions']:d['status']='source-authoring direction; tally corrected; three-trade reconciliation and exact review remain'
write(A/'SKINNING_SOURCE_VERDICT_RECONCILIATION.json',out)
print(json.dumps({k:out[k] for k in ['status','checkCount','protectedInputsUnchanged','actualComponentCounts','failedChecks','recipesApproved']}))
