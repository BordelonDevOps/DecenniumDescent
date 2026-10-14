"""Independent source/projection checks and bounded Fishing arithmetic.

This preliminary evidence does not replace the required complete FI scenario
walkthrough or GPT's separate exact review. Results explicitly retain that gate.
"""
from copy import deepcopy
from collections import Counter
from fractions import Fraction as F
import json,re
import fishing_reference as ref
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,unr,model_id


def main():
    internal=read(ROOT/'data/director/fishing_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/fishing_recipe_candidate.json')
    source=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    originals=[r for r in source['recipes'] if r['skill']=='Fishing']
    cards={c['recipeId']:c for c in internal['cards']};models=internal['baseModels']
    checks=[];quotes=[];quality_cases=[];structural_cases=[]
    def check(name,result,detail=None):
        checks.append({'name':name,'pass':bool(result),**({'detail':detail} if detail is not None else {})})
        assert result,name
    def rejected(name,fn):
        try:fn()
        except ValueError:check(name,True);return
        check(name,False)
    check('All 44 complete source objects unchanged',[c['sourceRecipe'] for c in internal['cards']]==originals)
    check('Original indices resolve exactly',all(source['recipes'][c['sourceRecipeIndex']]==c['sourceRecipe'] for c in cards.values()))
    check('Source classification 28/3/13',Counter(r['visibility'] for r in originals)=={'public':28,'restricted':3,'director-only':13})
    check('212 consumed component occurrences; no catalyst',sum(len(r['components']) for r in originals)==212 and all(z['consumed'] and z['role']!='catalyst' for r in originals for z in r['components']))
    check('Source bonus and extra distributions',Counter(r['mechanics']['fishingBonus'] for r in originals)=={1:26,2:13,3:5} and all(r['mechanics']['fishingBonus']==r['mechanics']['extraYield'] for r in originals))
    check('Nine body models for both audiences',len(models)==9 and public['baseModels']==models)
    check('14 internal / 13 public affinities',len(internal['sharedOperationalProfile']['affinityRegistry'])==14 and len(public['sharedOperationalProfile']['affinityRegistry'])==13 and 'Cold' not in public['sharedOperationalProfile']['affinityRegistry'])
    # Independent recursive projection, deliberately not importing the builder's filter.
    private={'restricted','director-only','director-internal'}
    def project(v):
        if isinstance(v,dict):
            if v.get('visibility') in private:return None
            return {k:project(x) for k,x in v.items() if k not in {'directorGuidance','directorNotes','secret','secrets'} and not(isinstance(x,dict) and x.get('visibility') in private)}
        if isinstance(v,list):return [project(x) for x in v if not(isinstance(x,dict) and x.get('visibility') in private)]
        return deepcopy(v)
    expected=deepcopy(internal);expected['visibility']='public';expected=project(expected)
    expected['sharedOperationalProfile']['affinityRegistry'].pop('Cold')
    expected['sharedGuide']='docs/mechanics/FISHING_RECIPE_PLAYTEST.md'
    check('Entire public JSON matches independent projection',expected==public)
    ptext=(ROOT/'docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    guide=(ROOT/'docs/mechanics/FISHING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8')
    itext=(ROOT/'docs/director-only/FISHING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    check('28 and 44 ordered manuscript cards',re.findall(r'^## (recipe-\d+) —',ptext,re.M)==[c['recipeId'] for c in public['cards']] and re.findall(r'^## (recipe-\d+) —',itext,re.M)==list(cards))
    check('Private recipe IDs/names absent from public manuscripts',all(not re.search(r'\b'+re.escape(c['recipeId'])+r'\b',ptext+guide) and c['name'] not in ptext+guide for c in cards.values() if c['visibility']!='public'))
    check('Public guide has no unused private Cold row','| Cold |' not in guide)
    check('Public files contain no Director link',not re.search(r'\]\([^)]*director-only',ptext+guide))
    bindings={b['recipeId']:b for b in read(AUDIT/'FISHING_SOURCE_PREPARATION.json')['publicBookBindings']}
    check('All six paragraphs in all 28 bindings preserved',len(bindings)==28 and all(c['publicBookBinding']==bindings[c['recipeId']] and len(c['publicBookBinding']['paragraphs'])==6 and all(p['text'].replace('|','\\|') in ptext for p in c['publicBookBinding']['paragraphs']) for c in public['cards']))
    check('Original effects preserved in manuscripts',all('**Preserved source effect:** '+c['sourceRecipe']['effects'] in itext for c in cards.values()))
    check('No premature approval',not internal['exactRecipeApproval'] and not internal['runtimeImplemented'] and not internal['balanceApproved'] and all(c['status']=='authored-draft-awaiting-exact-review' for c in cards.values()))
    verdict=(AUDIT/'GPT_FISHING_SOURCE_CONFERENCE.md').read_text(encoding='utf-8')
    register=[]
    for line in verdict.split('## Source-bound authoring register',1)[1].split('## Final authorization',1)[0].splitlines():
        if re.match(r'^\| \d+ \|',line):register.append([s.strip() for s in line.strip('|').split('|')])
    check('44 rows in independent GPT register',len(register)==44)
    for row in register:
        num,family,q,bonus,dc,hours,field,assist,trivial,value=row
        c=cards['recipe-'+num];r=c['sourceRecipe'];o=c['operational'];w=o['work']
        check('Source-bound conference register '+num,
            family==r['recipeFamily']+' / '+r['mechanics']['attracts'] and int(q)==r['quantity'] and
            bonus==f"+{r['mechanics']['fishingBonus']} / {r['mechanics']['extraYield']}" and
            int(dc)==r['craftingCheck']['targetDC'] and F(hours)==F(str(w['operationalActiveWorkHours'])) and
            (field=='yes')==w['fieldCraftable'] and int(assist)==w['maximumAssistants'] and int(trivial)==w['trivialAtSkillLevel'] and
            F(value)==unr(o['finishedUnitReferenceGp'])==ref.finished_reference(r,models[model_id(r)]))
    true_ids={f'recipe-{n}' for n in list(range(160,175))+[180,182,183,640]}
    check('All 19 true and 25 false field flags exact',{c['recipeId'] for c in cards.values() if c['operational']['work']['fieldCraftable']}==true_ids)
    check('Every exact work/access field and no artisan exception',all(c['operational']['work']['sourceActiveWorkHours']==c['sourceRecipe']['workRequirements']['activeWorkHours'] and c['operational']['work']['maximumAssistants']==c['sourceRecipe']['workRequirements']['maximumAssistants'] and c['operational']['work']['timeMode']==c['sourceRecipe']['workRequirements']['timeMode'] and not c['operational']['work']['forgeDwarfEligible'] and c['operational']['work']['includedFirstStablePhaseHours']==.25 for c in cards.values()))
    last=cards['recipe-199'];check('Recipe 199 keeps 960 hours, DC28, three assistants, trivial20',last['operational']['work']['remainingActiveWorkHours']==959.75 and last['sourceRecipe']['craftingCheck']['targetDC']==28 and last['operational']['work']['maximumAssistants']==3 and last['operational']['work']['trivialAtSkillLevel']==20)
    for c in cards.values():
        r=c['sourceRecipe'];q=r['quantity'];b=models[model_id(r)]
        for band in ['Standard','Exceptional','Masterwork','Flawed','Failed','Mishap']:
            for option in ['yield','property']:
                actual=ref.quality(r,band,option)
                expected_n={'Standard':q,'Exceptional':q*5//4,'Masterwork':q*3//2,'Flawed':q//2 if q>1 else 1,'Failed':0,'Mishap':0}[band]
                if r['recipeFamily']=='Bait' and band=='Flawed' and q==1:expected_n=0
                if option=='property' and band in ('Exceptional','Masterwork'):expected_n=q
                assert actual['quantity']==expected_n and actual['catalystsReturned']==0
                quality_cases.append({'recipeId':r['id'],'band':band,'choice':option,**actual})
        if r['recipeFamily']=='Bait':
            rejected('No Bait repair '+r['id'],lambda r=r,b=b:ref.repair_quote(r,b,0,1,['dose'],['dose']))
        else:
            for hp in (0,1):
                v=ref.repair_quote(r,b,hp,5,['primary'],['primary'])
                expected_cost=(F(str(r['economy']['recommendedMarketValue']))/q+F(str(b['baselinePriceGp'])) if hp==0 else F(str(b['baselinePriceGp'])))/4
                assert v['materialReferenceGp']==expected_cost and v['dc']==(r['craftingCheck']['targetDC'] if hp==0 else 10) and v['hours']==(8 if hp==0 else 1)
                quotes.append({'recipeId':r['id'],'state':'Broken' if hp==0 else 'functional','referenceGp':str(expected_cost),'purchaseGp':str(v['purchaseGp']),'dc':v['dc'],'hours':str(v['hours'])})
            rejected('Missing original primary cannot repair '+r['id'],lambda r=r,b=b:ref.repair_quote(r,b,0,5,['primary','original-unique'],['primary']))
    check('528 source-bound quality choices',len(quality_cases)==528)
    check('76 source-bound durable repair quotes',len(quotes)==76)
    fixed={179:(14,F('302.375'),F('302.38')),175:(16,F(247),F(247)),642:(16,F('274.50'),F('274.50'))}
    for num,(dc,price,buy) in fixed.items():
        r=cards['recipe-'+str(num)]['sourceRecipe'];v=ref.repair_quote(r,models[model_id(r)],0,5,['p'],['p'])
        check('Independent Broken repair example '+str(num),v['dc']==dc and v['hours']==8 and v['materialReferenceGp']==price and v['purchaseGp']==buy)
    r=cards['recipe-179']['sourceRecipe'];v=ref.repair_quote(r,models[model_id(r)],1,5,['shaft'],['shaft'])
    check('Rod functional .125 gp rounds up once to .13',v['materialReferenceGp']==F(1,8) and v['purchaseGp']==F(13,100))
    for oldpercent in (0,25,50):
        for oldflaw in (False,True):
            oldmax={0:5,25:6,50:7}[oldpercent]
            if oldflaw:oldmax=max(1,oldmax//2)
            for hp in range(1,oldmax+1):
                for newpercent in (0,25,50):
                    for newflaw in (False,True):
                        v=ref.structural_hp(5,oldmax,hp,oldpercent,newpercent,oldflaw,newflaw)
                        n={0:5,25:6,50:7}[max(oldpercent,newpercent)]
                        if oldflaw or newflaw:n=max(1,n//2)
                        assert v['maximumHP']==n and v['currentHP']==max(0,n-(oldmax-hp))
                        structural_cases.append([oldpercent,oldflaw,hp,newpercent,newflaw,v])
    check('All functional B5 durability/flaw/damage combinations',len(structural_cases)==156)
    check('Singleton 1/5 Flawed becomes Broken 0/2',ref.structural_hp(5,5,1,new_flaw=True)['currentHP']==0 and ref.structural_hp(5,5,1,new_flaw=True)['maximumHP']==2)
    reserve=[{'id':f'body-{i}','inventoryEvidenceRef':f'fixture-inventory#{i}','reservationEvidenceRef':'fixture-order#1','ownerOrderId':'order-1','state':'available-reserved','grade':'Standard','priorMagicalAlteration':False,'originalConstituentIds':[f'frame-{i}',f'funnel-{i}'],'currentHP':5,'maximumHP':5,'durabilityPercent':0,'flawed':False} for i in range(7)]
    r=cards['recipe-163']['sourceRecipe'];out=ref.ordered_output(r,'Masterwork',reserve)
    check('Trap Q5 needs seven real bodies and produces 28 lb maximum',len(out['selected'])==7 and 7*models['fishing.trap']['baselineWeightLb']==28 and F(str(r['economy']['consumedWeight']))==F('1.47'))
    out=ref.ordered_output(r,'Standard',reserve)
    check('Standard takes first five; unused bodies stay ordinary',[x['id'] for x in out['selected']]==[f'body-{i}' for i in range(5)] and [x['id'] for x in out['unused']]==['body-5','body-6'])
    damaged=deepcopy(reserve);damaged[0]['currentHP']=1
    out=ref.ordered_output(r,'Exceptional',damaged,'property')
    check('Latest damage preserved during durability gain',out['selected'][0]['maximumHP']==6 and out['selected'][0]['currentHP']==2)
    broken=deepcopy(reserve);broken[6]['currentHP']=0
    rejected('Broken unused maximum reserve pauses before rolling',lambda:ref.ordered_output(r,'Standard',broken))
    duplicate=deepcopy(reserve);duplicate[6]['id']=duplicate[0]['id']
    rejected('Duplicate reserve body rejected',lambda:ref.ordered_output(r,'Masterwork',duplicate))
    baitreserve=[{'id':f'dose-blank-{i}','inventoryEvidenceRef':f'fixture-stock#{i}','reservationEvidenceRef':'fixture-bait-order','ownerOrderId':'bait-order','state':'available-reserved','grade':'Standard','priorMagicalAlteration':False,'carrierLb':.10,'wrapperLb':.01,'materialCondition':'eligible'} for i in range(4)]
    r=cards['recipe-171']['sourceRecipe'];out=ref.ordered_output(r,'Masterwork',baitreserve)
    check('Bait Q3 reserves four real packets .44 lb independent of .14 lb process bill',len(out['selected'])==4 and 4*F('0.11')==F('.44') and F(str(r['economy']['consumedWeight']))==F('.14'))
    small={'bodyMassLb':.4,'baseline':[{'id':'small-meat','massLb':.4,'material':'ordinary-fish-meat'}],'extraReserve':[],'damagedBaseline':[],'unique':[]}
    check('Small fish manifest remains .40 lb',ref.validate_material_manifest(small))
    bad=deepcopy(small);bad['extraReserve']=[{'id':'fake-extra','massLb':1,'material':'ordinary-fish-meat'}]
    rejected('Extra unit cannot exceed real body mass',lambda:ref.validate_material_manifest(bad))
    bad=deepcopy(small);bad['bodyMassLb']=2;bad['extraReserve']=deepcopy(bad['baseline'])
    rejected('Baseline and reserve unit identities cannot overlap',lambda:ref.validate_material_manifest(bad))
    bad=deepcopy(small);bad['bodyMassLb']=2;bad['extraReserve']=[{'id':'fractional-extra','massLb':.4,'material':'ordinary-fish-meat'}]
    rejected('Fractional ordinary-meat extra unit rejected',lambda:ref.validate_material_manifest(bad))
    rejected('Bare availability boolean is not world evidence',lambda:ref.WorldEvidence({'x':True}))
    record={'id':'fixture','authority':'synthetic test fixture only','citations':['FI-D08 synthetic case; no actual campaign claim'],'checkpoint':[0,0,0],'fixture':True,'kind':'opportunity'}
    rejected('Fixture cannot certify production world evidence',lambda:ref.WorldEvidence({'fixture':record}))
    world=ref.WorldEvidence({'fixture':record},test_fixture=True)
    rejected('Current state cannot replace historical record',lambda:world.record('fixture','opportunity',[5,0,0]))
    for rel in ['docs/mechanics/FISHING_RECIPE_PLAYTEST.md','docs/director-only/FISHING_INTERNAL_GUIDE.md','docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md','docs/director-only/FISHING_INTERNAL_RECIPE_CARDS.md']:
        p=ROOT/rel;t=p.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)',t):
            if not re.match(r'[a-z]+:',link):assert (p.parent/link.split('#')[0]).exists(),(rel,link)
    check('All authored local guide links resolve',True)
    baseline=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    check('All 63 protected input hashes unchanged',len(baseline)==63 and all(sha(GAME/p)==h for p,h in baseline.items()))
    status={'status':'preliminary source/projection/arithmetic checks passed; full scenario evidence still pending',
        'checks':checks,'qualityCases':quality_cases,'structuralCases':structural_cases,'repairQuotes':quotes,
        'recipesApproved':0,'currentReviewedRecipes':348,'remainingRecipes':339,
        'completeExactReviewReady':False,'catchLedgerScenarioCoverageComplete':False,
        'remainingEvidence':['all FI-01..24 worked play sequences','source-bound item/check/response fixtures','concurrent and chronological journal cases','unattended Trap and bait expiry sequences','live capture, recapture, harvesting and placement sequences','complete source-protected exact-review packet'],
        'referenceLimits':'Arithmetic and a bounded evidence journal only; does not authenticate world facts or implement game/companion runtime.',
        'sourceInformationDeleted':False,'cosmology':'post-push only'}
    dump(AUDIT/'FISHING_PRELIMINARY_VALIDATION.json',status)
    print(json.dumps({'checksPassed':len(checks),'qualityCases':len(quality_cases),'structuralCases':len(structural_cases),
        'repairQuotes':len(quotes),'protectedFiles':len(baseline),'recipesApproved':0,'exactReviewReady':False}))


if __name__=='__main__':main()
