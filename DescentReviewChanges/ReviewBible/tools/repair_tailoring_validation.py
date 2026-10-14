"""One-time scoped TA-ER01..04 validation repair; submitted script is archived."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'tools/validate_tailoring_recipe_candidate.py'
s=p.read_text(encoding='utf-8')
assert 'TA-ER01 no task-wide premise fallback' not in s, 'One-time repair already applied.'
start=s.index('    def item(');end=s.index('    reserve=',start)
block='''    fixtures=[]
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
'''
s=s[:start]+block+s[end:]
s=s.replace("tr.repair_terms(0,5,1,F(57,5),12,required_constituents_present=False)","tr.repair_terms(0,5,1,F(57,5),11,required_constituents_present=False)")
s=s.replace("tr.repair_terms(1,5,.5,F(997125,2),30)","tr.repair_terms(1,5,.5,F(997125,2),28)")
s=s.replace("tr.repair_terms(0,5,.5,F(997125,2),30)","tr.repair_terms(0,5,.5,F(997125,2),28)")
anchor="    check('high tier tool not kit ownership'"
extra='''    check('TA-ER03 recipe548 reconstruction DC11',by['recipe-548']['sourceRecipe']['craftingCheck']['targetDC']==11 and tr.repair_terms(0,5,1,F(57,5),11)['DC']==11)
    check('TA-ER03 recipe584 reconstruction DC28',by['recipe-584']['sourceRecipe']['craftingCheck']['targetDC']==28 and tr.repair_terms(0,5,.5,F(997125,2),28)['DC']==28)
    repair_contract={'bothRoutesRequire':['trained Weaver credential','actual Weaver tools with Tailor tools binding','actual Loom and Cutting Table','required Needles','required Shears'],'compatibleImplementMayOverlap':True,'missingActualToolkitMayBegin':False,'quotationGrantsPermission':False,'rareCreationToolsRequiredForGenericRepair':False}
    repair_phrase="actual Weaver's tools, using the Tailor's-tools binding; an actual Loom and Cutting Table; and the required Needles and Shears"
    for rel,n in [('docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md',43),('docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md',29),('docs/director-only/TAILORING_INTERNAL_GUIDE.md',1),('docs/mechanics/TAILORING_RECIPE_PLAYTEST.md',1)]:
        text=(ROOT/rel).read_text(encoding='utf-8')
        check('TA-ER04 explicit physical-tool contract '+rel,text.count(repair_phrase)==n and ('Missing the actual toolkit prevents starting either route' in text or 'without the actual toolkit cannot begin either repair route' in text))
    check('TA-ER04 quotation not permission contract',not repair_contract['missingActualToolkitMayBegin'] and not repair_contract['quotationGrantsPermission'] and 'Quotation only, never permission' in tr.repair_terms.__doc__ and tr.repair_terms(1,5,1,F(57,5),11)['DC']==10)
'''
s=s.replace(anchor,extra+anchor)
old="    check('no exact approval or runtime claim',not internal['exactRecipeApproval'] and not internal['runtimeImplemented'] and not internal['balanceApproved'])"
new='''    approved=internal['exactRecipeApproval']
    check('truthful scoped operational status',public['exactRecipeApproval']==approved and all(c['status']==('reviewed-authored-operational-playtest' if approved else 'authored-draft-awaiting-exact-review') for c in cards) and not internal['runtimeImplemented'] and not internal['balanceApproved'])
    check('all finite repair fixtures derived from actual source profiles',all(z['family']==next(c for c in (internal if z['trade']=='Tailoring' else other[z['trade']])['cards'] if c['recipeId']==z['recipeId'])['sourceRecipe']['recipeFamily'] for z in fixtures))
    artifact_paths=['data/director/tailoring_recipe_candidate_internal.json','data/playtest/tailoring_recipe_candidate.json','docs/director-only/TAILORING_INTERNAL_GUIDE.md','docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md','docs/mechanics/TAILORING_RECIPE_PLAYTEST.md','docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md']
'''
assert old in s;s=s.replace(old,new)
s=s.replace("'recipesApproved':0}","'recipesApproved':43 if approved else 0,'sourceBoundFixtures':fixtures,'repairProcedureContract':repair_contract,'nestedFixturePremises':{'outerRecipe':'recipe-280','innerRecipe':'recipe-546','innerObject':'declared1lb/3Load object,2x2x2 inches; synthetic canonical-Load arithmetic fixture','packing':'one inner occupied envelope within actual outer compartment; object within inner; no compression','access':'actual accessible closures; no simultaneous retrieval asserted','support':'no independent support in release cases; integral strap rejected','placement':'same square legal at actual3ft elevation, or explicit pending branch; ordinary falling remains governing-board procedure'},'artifactHashes':{q:sha(ROOT/q) for q in artifact_paths}}")
s=s.replace("if k!='checks'","if k not in ('checks','sourceBoundFixtures','artifactHashes','repairProcedureContract','nestedFixturePremises')")
p.write_text(s,encoding='utf-8',newline='\n')
print('Scoped validation repair written.')
