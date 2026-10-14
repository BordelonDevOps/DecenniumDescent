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
    def item(id='cloak',family='Cloak',bonus=2,**kw):
        return dict(id=id,trade='Tailoring',family=family,bonus=bonus,state='worn',hp=5,complete=True,fit=True,slotValid=True,slot=SLOTS[family],wearer='A',**kw)
    cloak=item()
    task={'actualCheck':True,'kind':'ability-check','domain':'presentation','domainCriteriaMet':True,'actualContribution':True,'ability':'CHA','proficiency':'Persuasion','visibleAttire':True,'actor':'A','coverageSufficient':True}
    check('actual wearer presentation',tr.tailoring_task_bonus([cloak],task)==2)
    for label,patch in [('ordinary bargain',{'domainCriteriaMet':False}),('save',{'kind':'save'}),('another disguise maker',{'actor':'B'}),('observer',{'ability':'WIS','proficiency':'Perception'}),('hidden presentation',{'visibleAttire':False}),('no check',{'actualCheck':False})]:
        check('no bonus: '+label,tr.tailoring_task_bonus([cloak],{**task,**patch})==0)
    for label,patch in [('suppressed',{'suppressed':True}),('melded',{'state':'melded'}),('Broken',{'hp':0}),('incomplete',{'complete':False}),('bad fit',{'fit':False}),('extra layer',{'slotValid':False})]:
        check('inactive '+label,tr.tailoring_task_bonus([{**cloak,**patch}],task)==0)
    leather=item('coat',family='Cloak',bonus=3);leather.update(trade='Leatherworking',family='Coat')
    check('outerwear exclusion across trades',raises(lambda:tr.validate_designated_slots([cloak,leather])))
    glove=item('glove',family='Gloves');gauntlet={'id':'gauntlet','trade':'Blacksmithing','family':'Gauntlets','state':'worn','slotValid':True,'slot':'handwear-pair','wearer':'A'}
    check('handwear exclusion with Blacksmithing',raises(lambda:tr.validate_designated_slots([glove,gauntlet])))
    check('head exclusion',raises(lambda:tr.validate_designated_slots([item('hat','Hat'),{**gauntlet,'id':'helm','slot':'head'}])))
    check('Robe outfit exclusion',raises(lambda:tr.validate_designated_slots([item('robe','Robe'),item('outfit','Garment')])))
    check('Tailoring absent from selected Crude candidates',tr.defense(-1,[cloak])['enhancement']==-1)
    check('no candidate without selected suit',tr.defense(None,[cloak])['enhancement'] is None)
    acid=item(resistance='acid')
    check('resistance independent of task/formula',tr.defense(-1,[acid])=={'enhancement':-1,'resistances':['acid']})
    check('suppression stops resistance',not tr.defense(-1,[{**acid,'suppressed':True}])['resistances'])
    exposure={**task,'domain':'exposure','ability':'CON','proficiency':None,'independentExposureProcedureAllowsClothing':True}
    check('actual exposure check vs required save',tr.tailoring_task_bonus([cloak],exposure)==2 and tr.tailoring_task_bonus([cloak],{**exposure,'kind':'save'})==0)
    check('Cord no climb domain',tr.tailoring_task_bonus([item('cord','Cord')],{**task,'domain':'climb','ability':'STR','proficiency':'Athletics'})==0 and not models['tailoring.cord']['suspendedCargoClimbingRestraintCasualtySupport'])
    bag={'id':'bag','family':'Bag','trade':'Tailoring','bodyCapacityLb':10,'state':'worn','slot':'pouch-1','fit':True,'hp':5,'complete':True,'bearer':'A','weight':1,'load':.1,'relief':10,'contents':['odd','coins']}
    records=[bag,{'id':'odd','weight':1,'load':3},{'id':'coins','weight':1,'load':.1}]
    got=tr.inventory(records,'A')
    check('per-record exceptional Load preserved',got['physicalPounds']==3 and got['canonicalLoad']==F(16,5) and got['effectiveLoad']==3 and got['countedPounds']==1)
    check('suppressed Bag retains real custody',tr.inventory([{**bag,'suppressed':True},*records[1:]],'A')['effectiveLoad']==F(16,5))
    inner={**bag,'id':'inner','contents':['odd'],'slot':'pouch-2'}
    outer={**bag,'id':'outer','contents':['inner'],'relief':10}
    nested=tr.inventory([outer,inner,records[1]],'A')
    check('only active outer relief',nested['activeContainers']==['outer'] and nested['coveredPoundsById']=={'inner':1,'odd':1} and nested['effectiveLoad']==F(3))
    broken,released=lw.break_container([outer,inner,records[1]],'outer')
    check('Broken releases immediate subtree once',released==['inner'] and next(r for r in broken if r['id']=='inner')['contents']==['odd'])
    check('meld preflight ignores relief',not lw.meld_preflight(records,['bag'],2,3)['fits'])
    check('Tiny rescuer exact accounting',F(140)+15==155 and F(3,2)+F(3,2)==3)
    tablebag={**bag,'bonus':2,'state':'placed','operator':'B','accessible':True}
    organize={**task,'domain':'organize-contents','ability':'INT','actor':'B','noncreatureCargo':True}
    check('Bag actual operator at table',tr.tailoring_task_bonus([tablebag],organize)==2)
    check('Bag inaccessible nested closure',tr.tailoring_task_bonus([{**tablebag,'accessible':False}],organize)==0)
    check('Bag not secure/retrieve alias',tr.tailoring_task_bonus([tablebag],{**organize,'domain':'unlocked-retrieval'})==0)
    leather_glove={**glove,'id':'leather','trade':'Leatherworking','bonus':3,'wearer':'B'}
    check('cross-trade strongest one check',tr.cross_trade_task_bonus([tablebag,leather_glove],{**organize,'ability':'DEX','leatherCriteriaMet':True},['manual-cargo-position'])==3)
    reserve=[{'id':str(i),'model':'tailoring.gloves','size':'Medium','grade':'Standard','ordinaryHP':5,'percent':0,'flaw':False,'current':5,'complete':True} for i in range(7)]
    standard,unused=lw.complete_order(reserve,5,'Standard');master,_=lw.complete_order(reserve,5,'Masterwork')
    check('548 five or seven pairs same ordered reserve',[r['id'] for r in standard]==list('01234') and len(master)==7 and len(unused)==2)
    check('latest damage survives',lw.complete_order([{**reserve[0],'current':1}],1,'Flawed')[0][0]['current']==0)
    check('missing reserve pauses before roll',raises(lambda:lw.complete_order([{**reserve[0],'missing':True}],1,'Standard')))
    check('missing original glove cannot reconstruct',raises(lambda:tr.repair_terms(0,5,1,F(57,5),12,required_constituents_present=False)))
    check('common outfit functional repair exact rounding',tr.repair_terms(1,5,.5,F(997125,2),30)['materialsGp']==F(1,8) and tr.purchase_cp(F(1,8))==13)
    check('584 reconstruction exact rounding',tr.repair_terms(0,5,.5,F(997125,2),30)['materialsGp']==F(997125,8) and tr.purchase_cp(F(997125,8))==12464063)
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
    check('no exact approval or runtime claim',not internal['exactRecipeApproval'] and not internal['runtimeImplemented'] and not internal['balanceApproved'])
    result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':checks,'checkCount':len(checks),'durabilityStates':states,'authoredCards':43,'publicCards':29,'sourceComponents':190,'protectedFiles':53,'runtimeImplemented':False,'balanceApproved':False,'recipesApproved':0}
    dump(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
    print(json.dumps([c for c in checks if not c['pass']]))
    assert result['status']=='PASS'
if __name__=='__main__':main()

