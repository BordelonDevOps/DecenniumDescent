"""Independent compact transcription of source recipe amounts from Part A.
Checks the supplied source-verdict register, not repository byte preservation.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from audit_inputs import CARDS,BODY_GP,BODY_LB,REGISTER
import fishing_reference_submitted as ref

ids=list(range(160,200))+list(range(640,644))
batches=[468,146,33,127,66,24,56,50,25,32,2400,2104,30,75,290,986,3381,1772,2311,1209,854,1020,892,359,638,23313,7225,16981,9763,10376,11990,50589,46717,42442,82876,50771,351424,541957,186471,523548,208,1102,1096,36911]
quantities=[5,1,1,5,4,3,3,2,1,3,2,3,5,4,5]+[1]*29
families='Lure Trap Bait Trap Hook Lure Net Net Trap Net Bait Bait Tackle Tackle Lure Net Net Tackle Hook Rod Rod Lure Line Line Lure Lure Line Line Bait Line Line Line Net Line Trap Hook Hook Trap Bait Bait Hook Line Rig Lure'.split()
dcs=[10,11,10,10,8,10,10,11,12,8,11,11,9,12,10,16,13,14,16,14,16,15,15,15,14,20,19,18,19,18,19,21,23,23,22,22,23,24,24,28,13,16,16,24]
occurrences=[3,4,4,4,3,2,4,4,3,2,4,2,3,2,3,3,5,5,4,5,5,5,5,5,5,5,4,4,6,4,6,6,7,7,8,7,9,8,8,11,4,4,5,5]
assert len(ids)==len(batches)==len(quantities)==len(families)==len(dcs)==44
checks=[];quotes=[]
for n,v,q,fam,dc in zip(ids,batches,quantities,families,dcs):
    c=CARDS['recipe-'+str(n)]['sourceRecipe']
    assert (c['quantity'],c['recipeFamily'],c['craftingCheck']['targetDC'])==(q,fam,dc)
    assert c['economy']['recommendedMarketValue']==v
    finished=F(v,q)+BODY_GP[fam]
    assert finished==F(next(z['finishedGp'] for z in REGISTER if z['recipeId']==c['id']))
    checks.append({'recipeId':c['id'],'finishedGp':str(finished),'pass':True})
    if fam!='Bait':
        for current in (0,1):
            expected=(finished if current==0 else BODY_GP[fam])/4
            actual=ref.repair_quote(c,{'baselinePriceGp':str(BODY_GP[fam])},current,5,['original'],['original'])
            assert actual['materialReferenceGp']==expected
            quotes.append({'recipeId':c['id'],'state':'Broken' if current==0 else 'functional','referenceGp':str(expected),'purchaseGp':str(actual['purchaseGp'])})
assert sum(occurrences)==212
quality_count=0
for c in CARDS.values():
    r=c['sourceRecipe'];q=r['quantity']
    for band in ('Standard','Exceptional','Masterwork','Flawed','Failed','Mishap'):
        for option in ('yield','property'):
            out=ref.quality(r,band,option)
            if band=='Flawed' and q==1 and r['recipeFamily']=='Bait':expected=0
            elif band in ('Failed','Mishap'):expected=0
            elif band=='Flawed':expected=max(1,q//2)
            elif option=='property' or band=='Standard':expected=q
            else:expected=q*(5 if band=='Exceptional' else 6)//4
            assert out['quantity']==expected and out['catalystsReturned']==0
            quality_count+=1
structural_count=0
for p in (0,25,50):
    for flawed in (False,True):
        oldmax={0:5,25:6,50:7}[p]//(2 if flawed else 1)
        for hp in range(1,oldmax+1):
            for newp in (0,25,50):
                for newf in (False,True):
                    maximum={0:5,25:6,50:7}[max(p,newp)]//(2 if flawed or newf else 1)
                    out=ref.structural_hp(5,oldmax,hp,p,newp,flawed,newf)
                    assert out['maximumHP']==maximum and out['currentHP']==max(0,maximum-oldmax+hp)
                    structural_count+=1
result={'scope':'Local independent arithmetic over compact Part A source transcription; not complete source-object or repository hash validation',
        'sourceRegisterRows':len(checks),'sourceComponentOccurrences':sum(occurrences),'qualityCalculations':quality_count,
        'structuralCalculations':structural_count,'repairQuotes':len(quotes),'allPassed':True,'rows':checks,'quotes':quotes}
Path(__file__).with_name('arithmetic_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','quotes')}))
