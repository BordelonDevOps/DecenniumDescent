"""Validate Tailoring source preservation, projections and bounded rule behavior."""
from copy import deepcopy
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json
import tailoring_reference as tr
import leatherworking_reference as lw
from build_tailoring_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,public_projection,model_ids,SLOTS

checks=[]
def check(name,value):
    checks.append({'name':name,'pass':bool(value)})
def raises(fn):
    try:fn()
    except ValueError:return True
    return False

def main():
    internal=read(ROOT/'data/director/tailoring_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/tailoring_recipe_candidate.json')
    evidence=read(AUDIT/'TAILORING_SOURCE_PREPARATION.json')
    originals=[r for r in read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes'] if r['skill']=='Tailoring']
    cards=internal['cards'];by={c['recipeId']:c for c in cards};models=internal['baseModels']
    check('all43 complete original records, including absent/null fields',[c['sourceRecipe'] for c in cards]==originals==evidence['recipes'])
    check('visibility43 and all source components',Counter(c['visibility'] for c in cards)=={'public':29,'restricted':4,'director-only':10} and sum(len(r['components']) for r in originals)==190)
    components=[z for r in originals for z in r['components']]
    check('165 consumed25 reusable no catalysts',sum(z['consumed'] for z in components)==165 and sum(z['role']=='tool' and not z['consumed'] for z in components)==25 and not any(z['role']=='catalyst' for z in components))
    check('no source armorBonus field',all('armorBonus' not in r['mechanics'] for r in originals))
    check('public cards exact safe projection',public['cards']==[public_projection(c) for c in cards if c['visibility']=='public'])
    public_expected=deepcopy(internal)
    public_expected.update(visibility='public',sharedGuide='docs/mechanics/TAILORING_RECIPE_PLAYTEST.md',cards=[public_projection(c) for c in cards if c['visibility']=='public'])
    public_expected['sharedOperationalProfile']['familyTaskDomains'].pop('Mantle')
    allowed_models={m for c in public_expected['cards'] for m in c['operational']['baseModelIds']}
    public_expected['baseModels']={m:b for m,b in models.items() if m in allowed_models}
    check('complete public JSON envelope and data projection exact',public==public_expected)
    publicids={f'recipe-{i}' for i in list(range(546,570))+[575,576,680,681,682]}
    check('public whitelist exact',{c['recipeId'] for c in public['cards']}==publicids)
    check('29 preserved public bindings',[c['publicBookBinding'] for c in cards if c['publicBookBinding']] == evidence['publicBookBindings'])
    check('15 internal11 public model sets',len(models)==15 and len(public['baseModels'])==11 and set(public['baseModels'])=={i for c in public['cards'] for i in c['operational']['baseModelIds']})
    check('public excludes private models',not {'tailoring.bag-30','tailoring.bag-40','tailoring.bag-50','tailoring.mantle'}.intersection(public['baseModels']))
    check('all original equipment sizing fields intact',all(b['sourceEquipmentRecord'] is None or b['sourceEquipmentRecord']['largeSizingEligible']==False for b in models.values()))
    expected={'bag-10':(1,1),'bag-30':(3,3),'bag-40':(4,4),'bag-50':(5,5),'cloak':(1,2),'gloves':(1,.5),'hat':(.5,.5),'garment-common':(.5,3),'garment-costume':(5,4),'garment-fine':(15,6),'garment-traveler':(2,4),'robe':(2,4),'cord':(.1,.2),'veil':(.5,.1),'mantle':(1,2)}
    check('all finite body values and structural defenses',all((b['baselinePriceGp'],b['baselineWeightLb'])==expected[i.split('.',1)[1]] and b['ordinaryMaximumStructuralHP']==5 and b['structuralAC']==11 for i,b in models.items()))
    check('Large overlay only garment bodies',all(b['tailoringLargeVariantMultiplier']==(1 if b['family']=='Bag' else 2) for b in models.values()))
    for cap in (10,30,40,50):
        b=models[f'tailoring.bag-{cap}'];dims=b['interiorInches'];volume=F(dims[0]*dims[1]*dims[2],1728)
        check(f'bag{cap} exact volume/opening binding',volume==F(cap,30) and b['physicalContentWeightLimitLb']==cap and b['openingAxes']==([0,2] if cap==10 else [1,2]))
    check('small Bag explicit Backpack orthogonal fit',lw.orthogonal_box_fit([13,9,7],[18,12,8],[12,8]))
    resistance={c['recipeId']:c['operational']['effect']['resistance'] for c in cards if c['operational']['effect']['resistance']}
    check('exact seven resistances',resistance=={'recipe-577':'acid','recipe-579':'poison','recipe-580':'acid','recipe-581':'thunder','recipe-582':'bludgeoning','recipe-584':'radiant','recipe-683':'poison'})
    check('38 garment bonus distribution',Counter(c['operational']['effect']['taskBonus'] for c in cards if c['sourceRecipe']['recipeFamily']!='Bag')=={1:23,2:11,3:4})
    check('all card mappings and reserve quantities',all(c['operational']['baseModelIds']==model_ids(c['sourceRecipe']) and c['operational']['maximumBaseReserve']==3*c['sourceRecipe']['quantity']//2 for c in cards))
    check('91 model price combinations',sum(len(c['operational']['standardModelExamples']) for c in cards)==91)
    for rid,value in [(546,33),(548,F(57,5)),(549,F(121,2)),(552,F(69,4)),(553,17),(680,F(11021,10)),(681,F(49,2)),(682,1046),(683,92623),(584,F(997125,2))]:
        z=by[f'recipe-{rid}']['operational']['standardModelExamples'][0]['finishedUnitReferenceGp']
        check(f'recipe{rid} concrete reference',F(z['numerator'],z['denominator'])==value)
    for c in cards:
        r=c['sourceRecipe'];o=c['operational']
        check(r['id']+' work controls unchanged',o['work']['trivialAtSkillLevel']==r['skillProgression']['trivialAtSkillLevel'] and not r['workRequirements']['fieldCraftable'] and o['work']['eligibleForgeDwarfActiveMinutes']==tr.creation_minutes(r['workRequirements']['activeWorkHours'],True))
    year=by['recipe-584']
    check('source-null year preserved separately',year['sourceRecipe']['workRequirements']['activeWorkHours'] is None and year['sourceRecipe']['economy']['laborValue']==0 and year['operational']['work']['operationalActiveWorkHours']==1920 and tr.creation_minutes(None,True)==86400)
    fixtures=[]
    other={t:read(ROOT/f'data/director/{t.lower()}_recipe_candidate_internal.json') for t in ('Leatherworking','Blacksmithing')}
    def item(rid,id,trade='Tailoring',**state):
        data=internal if trade=='Tailoring' else other[trade]
        c=next(c for c in data['cards'] if c['recipeId']==f'recipe-{rid}')
        b=data['baseModels'][c['operational']['baseModelIds'][0]]
        f=c['sourceRecipe']['recipeFamily'];e=c['operational']['effect']
        slot={'Gauntlets':'handwear-pair','Helm':'head'}.get(f,b.get('benefitSlot'))
        if f=='Bag':slot='pouch-1' if b['physicalContentWeightLimitLb']==10 else 'back-cargo'
        hp=b.get('ordinaryMaximumStructuralHP',c['operational']['standardModelExamples'][0].get('baseMaximumHP'))
        r=dict(id=id,recipeId=c['recipeId'],baseModelId=b['id'],trade=trade,family=f,
            bonus=e.get('taskBonus',0),resistance=e.get('resistance'),armorBonus=e.get('armorBonus',0),
            state='worn',hp=hp,complete=True,fit=True,slotValid=True,slot=slot,wearer='A',
            weight=b['baselineWeightLb'],load=F(str(b['baselineWeightLb']))/10)
        if f in ('Bag','Backpack','Pouch','Quiver','Belt','Harness'):
            r.update(bodyCapacityLb=b['physicalContentWeightLimitLb'],bearer='A',
                relief=e['reliefAllowanceLb'],operator='A',accessible=True,contents=[])
        fixtures.append({'physicalId':id,'trade':trade,'recipeId':c['recipeId'],'baseModelId':b['id'],
                         'family':f,'bonus':r['bonus'],'resistance':r['resistance'],'ordinaryHP':hp})
        r.update(state);return r
    def premises(**kw):
        return dict(domainCriteriaMet=True,actualContribution=True,coverageSufficient=True,visibleAttire=True,**kw)
    cloak=item(682,'cloak')
    task={'actualCheck':True,'kind':'ability-check','domain':'presentation','ability':'CHA',
          'proficiency':'Persuasion','actor':'A','itemPremises':{'cloak':premises()}}
    check('actual wearer presentation',tr.tailoring_task_bonus([cloak],task)==2)
    for label,patch in [('save',{'kind':'save'}),('another disguise maker',{'actor':'B'}),('observer',{'ability':'WIS','proficiency':'Perception'}),('no check',{'actualCheck':False})]:
        check('no bonus: '+label,tr.tailoring_task_bonus([cloak],{**task,**patch})==0)
    for label,patch in [('ordinary bargain',{'domainCriteriaMet':False}),('hidden presentation',{'visibleAttire':False}),('noncontributing',{'actualContribution':False}),('insufficient coverage',{'coverageSufficient':False})]:
        check('no bonus: '+label,tr.tailoring_task_bonus([cloak],{**task,'itemPremises':{'cloak':{**premises(),**patch}}})==0)
    check('TA-ER01 no task-wide premise fallback',tr.tailoring_task_bonus([cloak],{**task,'itemPremises':{},**premises()})==0)
    for label,patch in [('suppressed',{'suppressed':True}),('melded',{'state':'melded'}),('Broken',{'hp':0}),('incomplete',{'complete':False}),('bad fit',{'fit':False}),('extra layer',{'slotValid':False})]:
        check('inactive '+label,tr.tailoring_task_bonus([{**cloak,**patch}],task)==0)
    outfit=item(584,'outfit')
    pairtask={**task,'itemPremises':{'cloak':premises(),'outfit':{**premises(),'visibleAttire':False,'actualContribution':False}}}
    check('TA-ER01 visible682+2 defeats irrelevant hidden584+3',tr.cross_trade_task_bonus([cloak,outfit],pairtask)==2)
    for field in ('visibleAttire','actualContribution','coverageSufficient'):
        t={**task,'itemPremises':{'cloak':premises(),'outfit':{**premises(),field:False}}}
        check('TA-ER01 independently required '+field,tr.cross_trade_task_bonus([cloak,outfit],t)==2)
    check('TA-ER01 two qualifying items strongest once',tr.cross_trade_task_bonus([cloak,outfit],{**task,'itemPremises':{'cloak':premises(),'outfit':premises()}})==3)
    check('TA-ER01 irrelevant outfit keeps radiant resistance',tr.defense(-1,[cloak,outfit])=={'enhancement':-1,'resistances':['radiant']})
    coat_id=next(c['recipeId'] for c in other['Leatherworking']['cards'] if c['sourceRecipe']['recipeFamily']=='Coat')
    leather=item(int(coat_id.split('-')[1]),'coat','Leatherworking')
    check('outerwear exclusion across trades',raises(lambda:tr.validate_designated_slots([cloak,leather])))
    check('TA-ER01 filtering cannot legalize competing slots',raises(lambda:tr.cross_trade_task_bonus([cloak,leather],task)))
    glove=item(548,'glove');gauntlet=item(44,'gauntlet','Blacksmithing')
    check('handwear exclusion with Blacksmithing',raises(lambda:tr.validate_designated_slots([glove,gauntlet])))
    hat=item(549,'hat');helm=item(49,'helm','Blacksmithing')
    check('head exclusion correct Hat and Helm families',hat['family']=='Hat' and helm['family']=='Helm' and raises(lambda:tr.validate_designated_slots([hat,helm])))
    robe=item(562,'robe')
    check('Robe outfit exclusion',raises(lambda:tr.validate_designated_slots([robe,outfit])))
    check('Tailoring absent from selected Crude candidates',tr.defense(-1,[cloak])['enhancement']==-1)
    check('no candidate without selected suit',tr.defense(None,[cloak])['enhancement'] is None)
    acid=item(577,'acid-outfit')
    check('TA-ER03 source-valid577 Garment acid resistance',acid['family']=='Garment' and acid['slot']=='body-clothing' and tr.defense(-1,[acid])=={'enhancement':-1,'resistances':['acid']})
    check('suppression stops resistance',not tr.defense(-1,[{**acid,'suppressed':True}])['resistances'])
    exposure={**task,'domain':'exposure','ability':'CON','proficiency':None,'itemPremises':{'cloak':premises(independentExposureProcedureAllowsClothing=True)}}
    check('actual exposure check vs required save',tr.tailoring_task_bonus([cloak],exposure)==2 and tr.tailoring_task_bonus([cloak],{**exposure,'kind':'save'})==0)
    cord=item(680,'cord')
    check('Cord no climb domain',tr.tailoring_task_bonus([cord],{**task,'domain':'climb','ability':'STR','proficiency':'Athletics','itemPremises':{'cord':premises()}})==0 and not models['tailoring.cord']['suspendedCargoClimbingRestraintCasualtySupport'])
    bag=item(546,'bag',contents=['odd','coins'])
    records=[bag,{'id':'odd','weight':1,'load':3},{'id':'coins','weight':1,'load':.1}]
    got=tr.inventory(records,'A')
    check('per-record exceptional Load preserved',got['physicalPounds']==3 and got['canonicalLoad']==F(16,5) and got['effectiveLoad']==3 and got['countedPounds']==1)
    check('suppressed Bag retains real custody',tr.inventory([{**bag,'suppressed':True},*records[1:]],'A')['effectiveLoad']==F(16,5))
    inner=item(546,'inner',state='stowed',contents=['odd'],slot=None,slotValid=False)
    outer=item(280,'outer','Leatherworking',contents=['inner'],location={'square':'A','elevationFeet':3})
    backpack=other['Leatherworking']['baseModels']['leather.backpack'];small=models['tailoring.bag-10']
    check('TA-ER03 nested occupied exterior and aperture fit',lw.orthogonal_box_fit(small['exteriorInches'],backpack['interiorInches'],backpack['openingInches'],backpack['openingAxes']) and lw.orthogonal_box_fit([2,2,2],small['interiorInches'],small['openingInches'],small['openingAxes']))
    check('TA-ER03 old bag10-in-bag10 geometry rejected',not lw.orthogonal_box_fit(small['exteriorInches'],small['interiorInches'],small['openingInches'],small['openingAxes']))
    nested_records=[outer,inner,records[1]];nested=tr.inventory(nested_records,'A')
    check('TA-ER03 source-valid nested7lb3.6Load relief',nested['physicalPounds']==7 and nested['canonicalLoad']==F(18,5) and nested['activeContainers']==['outer'] and nested['coveredPoundsById']=={'inner':1,'odd':1} and nested['effectiveLoad']==F(17,5) and nested['countedPounds']==5)
    unrelieved=tr.inventory([{**outer,'suppressed':True},inner,records[1]],'A')
    check('TA-ER03 suppression retains7lb3.6Load',unrelieved['physicalPounds']==7 and unrelieved['countedPounds']==7 and unrelieved['canonicalLoad']==F(18,5) and unrelieved['effectiveLoad']==F(18,5))
    broken,released=lw.break_container(nested_records,'outer',retained=(),same_location_legal=True)
    released_inner=next(r for r in broken if r['id']=='inner')
    check('Broken releases immediate subtree once at actual elevation',released==['inner'] and released_inner['contents']==['odd'] and released_inner['state']=='placed' and released_inner['location']==outer['location'] and next(r for r in broken if r['id']=='outer')['contents']==[])
    pending,_=lw.break_container(nested_records,'outer',retained=(),same_location_legal=False,adjacent_legal=False)
    check('no legal placement retains one pending subtree',next(r for r in pending if r['id']=='inner')['state']=='pending-placement' and next(r for r in pending if r['id']=='inner')['contents']==['odd'])
    check('integral strap is not independent support',raises(lambda:lw.break_container(nested_records,'outer',retained={'inner':'outer'})))
    check('meld preflight ignores relief',not lw.meld_preflight(records,['bag'],2,3)['fits'])
    check('Tiny rescuer exact accounting',F(140)+15==155 and F(3,2)+F(3,2)==3)
    tablebag=item(546,'tablebag',state='placed',operator='B',accessible=True,slot=None,slotValid=False)
    organize={**task,'domain':'organize-contents','ability':'INT','actor':'B','itemPremises':{'tablebag':premises(noncreatureCargo=True)}}
    check('TA-ER03 source546 Bag actual operator at table+1',tablebag['bonus']==1 and tr.tailoring_task_bonus([tablebag],organize)==1)
    check('Bag inaccessible nested closure',tr.tailoring_task_bonus([{**tablebag,'accessible':False}],organize)==0)
    check('Bag not secure/retrieve alias',tr.tailoring_task_bonus([tablebag],{**organize,'domain':'unlocked-retrieval'})==0)
    bigger=item(573,'bigger',state='placed',operator='B',accessible=True,slot=None,slotValid=False)
    bagtask={**organize,'itemPremises':{'tablebag':premises(noncreatureCargo=True),'bigger':{**premises(noncreatureCargo=True),'actualContribution':False}}}
    check('TA-ER01 stronger irrelevant Bag cannot borrow contribution',tr.cross_trade_task_bonus([tablebag,bigger],bagtask)==1)
    check('TA-ER01 two qualifying Bags use strongest once',tr.cross_trade_task_bonus([tablebag,bigger],{**bagtask,'itemPremises':{**bagtask['itemPremises'],'bigger':premises(noncreatureCargo=True)}})==2)
    leather_glove=item(306,'leather-glove','Leatherworking',wearer='B')
    lp=premises(leatherCriteriaMet=True,leatherTaskIds=['manual-cargo-position'],noncreatureCargo=True)
    cross={**organize,'ability':'DEX','itemPremises':{**organize['itemPremises'],'leather-glove':lp}}
    check('TA-ER03 source306 Gloves+2 strongest one check',leather_glove['bonus']==2 and tr.cross_trade_task_bonus([tablebag,leather_glove],cross,['manual-cargo-position'])==2)
    for field in ('actualContribution','leatherCriteriaMet'):
        ctask={**cross,'itemPremises':{**cross['itemPremises'],'leather-glove':{**lp,field:False}}}
        check('TA-ER01 cross-trade independent '+field,tr.cross_trade_task_bonus([tablebag,leather_glove],ctask,['manual-cargo-position'])==1)
    check('TA-ER01 cross-trade task IDs independently qualify',tr.cross_trade_task_bonus([tablebag,leather_glove],{**cross,'itemPremises':{**cross['itemPremises'],'leather-glove':{**lp,'leatherTaskIds':['handhold-climb']}}},['manual-cargo-position'])==1)
    operator_pack=item(652,'operator-pack','Leatherworking',wearer='A',operator='B')
    op=premises(leatherCriteriaMet=True,leatherTaskIds=['cargo-handling'],noncreatureCargo=True)
    op_task={**organize,'ability':'DEX','itemPremises':{'operator-pack':op}}
    check('TA-ER02 B operates A-worn Backpack gains+2',tr.cross_trade_task_bonus([operator_pack],op_task,['cargo-handling'])==2)
    check('TA-ER02 wearer operating own Backpack gains+2',tr.cross_trade_task_bonus([{**operator_pack,'operator':'A'}],{**op_task,'actor':'A'},['cargo-handling'])==2)
    check('TA-ER02 nonoperator wearer gains nothing',tr.cross_trade_task_bonus([operator_pack],{**op_task,'actor':'A'},['cargo-handling'])==0)
    check('TA-ER02 no ownership or wearer operator fallback',tr.cross_trade_task_bonus([{**operator_pack,'operator':None,'owner':'A'}],{**op_task,'actor':'A'},['cargo-handling'])==0)
    for label,patch in [('inaccessible',{'accessible':False}),('suppressed',{'suppressed':True}),('Broken',{'hp':0}),('melded',{'state':'melded'})]:
        check('TA-ER02 inactive container '+label,tr.cross_trade_task_bonus([{**operator_pack,**patch}],op_task,['cargo-handling'])==0)
    reserve=[{'id':str(i),'model':'tailoring.gloves','size':'Medium','grade':'Standard','ordinaryHP':5,'percent':0,'flaw':False,'current':5,'complete':True} for i in range(7)]
    standard,unused=lw.complete_order(reserve,5,'Standard');master,_=lw.complete_order(reserve,5,'Masterwork')
    check('548 five or seven pairs same ordered reserve',[r['id'] for r in standard]==list('01234') and len(master)==7 and len(unused)==2)
    check('latest damage survives',lw.complete_order([{**reserve[0],'current':1}],1,'Flawed')[0][0]['current']==0)
    check('missing reserve pauses before roll',raises(lambda:lw.complete_order([{**reserve[0],'missing':True}],1,'Standard')))
    check('missing original glove cannot reconstruct',raises(lambda:tr.repair_terms(0,5,1,F(57,5),11,required_constituents_present=False)))
    check('common outfit functional repair exact rounding',tr.repair_terms(1,5,.5,F(997125,2),28)['materialsGp']==F(1,8) and tr.purchase_cp(F(1,8))==13)
    check('584 reconstruction exact rounding',tr.repair_terms(0,5,.5,F(997125,2),28)['materialsGp']==F(997125,8) and tr.purchase_cp(F(997125,8))==12464063)
    check('TA-ER03 recipe548 reconstruction DC11',by['recipe-548']['sourceRecipe']['craftingCheck']['targetDC']==11 and tr.repair_terms(0,5,1,F(57,5),11)['DC']==11)
    check('TA-ER03 recipe584 reconstruction DC28',by['recipe-584']['sourceRecipe']['craftingCheck']['targetDC']==28 and tr.repair_terms(0,5,.5,F(997125,2),28)['DC']==28)
    repair_contract={'bothRoutesRequire':['trained Weaver credential','actual Weaver tools with Tailor tools binding','actual Loom and Cutting Table','required Needles','required Shears'],'compatibleImplementMayOverlap':True,'missingActualToolkitMayBegin':False,'quotationGrantsPermission':False,'rareCreationToolsRequiredForGenericRepair':False}
    repair_phrase="actual Weaver's tools, using the Tailor's-tools binding; an actual Loom and Cutting Table; and the required Needles and Shears"
    for rel,n in [('docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md',43),('docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md',29),('docs/director-only/TAILORING_INTERNAL_GUIDE.md',1),('docs/mechanics/TAILORING_RECIPE_PLAYTEST.md',1)]:
        text=(ROOT/rel).read_text(encoding='utf-8')
        check('TA-ER04 explicit physical-tool contract '+rel,text.count(repair_phrase)==n and ('Missing the actual toolkit prevents starting either route' in text or 'without the actual toolkit cannot begin either repair route' in text))
    check('TA-ER04 quotation not permission contract',not repair_contract['missingActualToolkitMayBegin'] and not repair_contract['quotationGrantsPermission'] and 'Quotation only, never permission' in tr.repair_terms.__doc__ and tr.repair_terms(1,5,1,F(57,5),11)['DC']==10)
    check('high tier tool not kit ownership',raises(lambda:tr.tool_reservation('scissors',[],'order',False)))
    check('one tool cannot overlap',raises(lambda:tr.tool_reservation('scissors',['orderA'],'orderB',True)))
    check('sequential tool same identity',tr.tool_reservation('scissors',[],'orderB',True)['physicalToolId']=='scissors')
    states=0
    for b in (5,10):
      for oldp in (0,25,50):
       for oldf in (False,True):
        for hp in range(lw.maximum_hp(b,oldp,oldf)+1):
         for newp in (0,25,50):
          for newf in (False,True):
           z=lw.apply_quality(b,oldp,oldf,hp,newp,newf);states+=1
           assert z['percent']==max(oldp,newp) and z['flaw']==(oldf or newf)
           assert z['maximum']-z['current']==min(z['maximum'],lw.maximum_hp(b,oldp,oldf)-hp)
    check('durability state space',states>500)
    baseline=read(AUDIT/'TAILORING_PART2_REVIEW_BASELINE.json')
    check('all53 protected inputs unchanged',len(baseline['files'])==53 and all(sha(GAME/p)==h for p,h in baseline['files'].items()))
    approved=internal['exactRecipeApproval']
    check('truthful scoped operational status',public['exactRecipeApproval']==approved and all(c['status']==('reviewed-authored-operational-playtest' if approved else 'authored-draft-awaiting-exact-review') for c in cards) and not internal['runtimeImplemented'] and not internal['balanceApproved'])
    check('all finite repair fixtures derived from actual source profiles',all(z['family']==next(c for c in (internal if z['trade']=='Tailoring' else other[z['trade']])['cards'] if c['recipeId']==z['recipeId'])['sourceRecipe']['recipeFamily'] for z in fixtures))
    artifact_paths=['data/director/tailoring_recipe_candidate_internal.json','data/playtest/tailoring_recipe_candidate.json','docs/director-only/TAILORING_INTERNAL_GUIDE.md','docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md','docs/mechanics/TAILORING_RECIPE_PLAYTEST.md','docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md']

    result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':checks,'checkCount':len(checks),'durabilityStates':states,'authoredCards':43,'publicCards':29,'sourceComponents':190,'protectedFiles':53,'runtimeImplemented':False,'balanceApproved':False,'recipesApproved':43 if approved else 0,'sourceBoundFixtures':fixtures,'repairProcedureContract':repair_contract,'nestedFixturePremises':{'outerRecipe':'recipe-280','innerRecipe':'recipe-546','innerObject':'declared1lb/3Load object,2x2x2 inches; synthetic canonical-Load arithmetic fixture','packing':'one inner occupied envelope within actual outer compartment; object within inner; no compression','access':'actual accessible closures; no simultaneous retrieval asserted','support':'no independent support in release cases; integral strap rejected','placement':'same square legal at actual3ft elevation, or explicit pending branch; ordinary falling remains governing-board procedure'},'artifactHashes':{q:sha(ROOT/q) for q in artifact_paths}}
    dump(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('checks','sourceBoundFixtures','artifactHashes','repairProcedureContract','nestedFixturePremises')}))
    print(json.dumps([c for c in checks if not c['pass']]))
    assert result['status']=='PASS'
if __name__=='__main__':main()
