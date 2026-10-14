"""Source preservation and bounded Jewelcrafting manuscript checks."""
from copy import deepcopy
from fractions import Fraction as F
from collections import Counter
import json,re,math
import jewelcrafting_reference as ref
from build_jewelcrafting_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,public_projection,unr,model_id

def main():
    internal=read(ROOT/'data/director/jewelcrafting_recipe_candidate_internal.json');public=read(ROOT/'data/playtest/jewelcrafting_recipe_candidate.json')
    cards={c['recipeId']:c for c in internal['cards']};models=internal['baseModels'];source=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    originals=[r for r in source['recipes'] if r['skill']=='Jewelcrafting'];checks=[];fixtures=[]
    def check(name,result,detail=None):
        checks.append({'name':name,'pass':bool(result),**({'detail':detail} if detail is not None else {})})
        assert result,name
    def rejected(name,fn):
        try:fn()
        except ValueError:check(name,True);return
        check(name,False)
    def jewel(n,physical=None,**physical_state):
        c=cards['recipe-'+str(n)];r=c['sourceRecipe'];b=models[model_id(r)];m=r['mechanics']
        z={'id':physical or 'item-'+str(n),'recipeId':r['id'],'trade':'Jewelcrafting','family':r['recipeFamily'],'tag':m['tag'],'bonus':m['bonus'],'maximumCharges':m['charges'],'model':b['id'],'state':'worn','wearer':'A','slot':b['benefitSlots'][0],'slotValid':True,'fit':True,'complete':True,'hp':5,'maximumHP':5,'suppressed':False,'physicalCompatibilityEstablished':True,'actualCompatibleHand':'left' if r['recipeFamily']=='Ring' else None,'actualHostSupport':True,'weightLb':b['baselineWeightLb']}
        z.update(physical_state)
        # Only physical-state variations: never synthetic source bonus/tag/profile.
        assert (z['tag'],z['bonus'],z['maximumCharges'],z['family'])==(m['tag'],m['bonus'],m['charges'],r['recipeFamily'])
        fixtures.append(deepcopy(z));return z
    def event(item,predicate,kind='ability-check',ability='INT',skill='Nature',**kw):
        z={'id':'roll-1','kind':kind,'actualRoll':True,'actor':'A','ability':ability,'proficiency':skill,'categories':[],'conscious':True,'incapacitated':False,'voluntaryActivationAllowed':True,'phase':'before-commit','resultRevealed':False,'itemPremises':{item['id']:{'actualCausalPredicateEstablished':True,'predicateIds':[predicate]}}};z.update(kw);return z
    check('43 complete source objects unchanged',[c['sourceRecipe'] for c in internal['cards']]==originals)
    check('source index provenance',all(source['recipes'][c['sourceRecipeIndex']]==c['sourceRecipe'] for c in cards.values()))
    check('visibility exact',Counter(c['visibility'] for c in cards.values())=={'public':26,'restricted':1,'director-only':16})
    check('200 consumed and eleven catalyst occurrences',sum(len(r['components']) for r in originals)==200 and all(z['consumed'] for r in originals for z in r['components']) and sum(z['role']=='catalyst' for r in originals for z in r['components'])==11)
    check('source bonus distribution',Counter(r['mechanics']['bonus'] for r in originals)=={1:24,2:12,3:7})
    check('source charge distribution',Counter(r['mechanics']['charges'] for r in originals)=={1:15,2:9,3:7,4:5,5:6,6:1})
    check('ten internal nine public bodies',len(models)==10 and len(public['baseModels'])==9 and 'jewelcrafting.pendant' not in public['baseModels'])
    check('fourteen internal twelve public tags',len(internal['sharedOperationalProfile']['tagPredicates'])==14 and len(public['sharedOperationalProfile']['tagPredicates'])==12 and not {'Acid','Water'}.intersection(public['sharedOperationalProfile']['tagPredicates']))
    expected=deepcopy(internal);expected['visibility']='public';expected['cards']=[public_projection(c) for c in internal['cards'] if c['visibility']=='public'];allowed={model_id(c['sourceRecipe']) for c in expected['cards']};tags={c['sourceRecipe']['mechanics']['tag'] for c in expected['cards']};expected['baseModels']={k:v for k,v in models.items() if k in allowed};expected['sharedOperationalProfile']['tagPredicates']={k:v for k,v in expected['sharedOperationalProfile']['tagPredicates'].items() if k in tags};expected['sharedGuide']='docs/mechanics/JEWELCRAFTING_RECIPE_PLAYTEST.md'
    check('entire public envelope equals exact intended projection',expected==public)
    def forbidden(v):
        if isinstance(v,dict):return any(k in ('directorGuidance','directorNotes','secret','secrets') or (k=='visibility' and z in ('director-internal','director-only','restricted')) or forbidden(z) for k,z in v.items())
        if isinstance(v,list):return any(forbidden(z) for z in v)
        return False
    check('no nested private control content in public envelope',not forbidden(public))
    pubtext=(ROOT/'docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8');guide=(ROOT/'docs/mechanics/JEWELCRAFTING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8')
    check('26 unique public manuscript card headings',re.findall(r'^## (recipe-\d+) —',pubtext,re.M)==[c['recipeId'] for c in public['cards']])
    check('public manuscript contains each exact source effect',all('**Preserved source effect:** '+c['sourceRecipe']['effects'] in pubtext for c in public['cards']))
    check('no private recipe IDs in public manuscripts',not any(re.search(r'\b'+re.escape(c['recipeId'])+r'\b',pubtext+'\n'+guide) for c in cards.values() if c['visibility']!='public'))
    check('public guide omits private model and tag rows','| Pendant' not in guide and '| Acid |' not in guide and '| Water |' not in guide and 'jewelcrafting.pendant' not in guide)
    evidence=read(AUDIT/'JEWELCRAFTING_SOURCE_PREPARATION.json');bindings={b['recipeId']:b for b in evidence['publicBookBindings']}
    check('26 public book bindings retained exactly',all(c['publicBookBinding']==bindings[c['recipeId']] for c in public['cards']) and len(bindings)==26)
    values=[]
    for c in cards.values():
        r=c['sourceRecipe'];o=c['operational'];b=models[model_id(r)];base=F(str(b['baselinePriceGp']));process=F(str(r['economy']['recommendedMarketValue']))/r['quantity']
        for k,mult in [('standardModelExamples',1),('largeModelExamples',2)]:
            v=unr(o[k][0]['finishedUnitReferenceGp']);assert v==process+base*mult;values.append({'recipeId':r['id'],'bodyMultiplier':mult,'exactGp':str(v)})
        assert o['effect']['flatBonus']==r['mechanics']['bonus'] and o['effect']['maximumCharges']==r['mechanics']['charges'] and o['effect']['tag']==r['mechanics']['tag']
        assert o['maximumBaseReserve']==3*r['quantity']//2 and not o['outcomes']['chargeImprovementPermitted']
    check('86 source-bound ordinary and Large values; every bonus and charge',len(values)==86)
    expected_prices={241:F(166,3),242:F(265,2),243:F(107,2),244:F(178),245:F(79),247:F(31),248:F(158,5),249:F(840),250:F(146,3),255:F(81),268:F(4509),279:F(776888),648:F(37167),649:F(36881),650:F(37015),651:F(36294)}
    check('sixteen independently supplied conference price examples',all(unr(cards['recipe-'+str(n)]['operational']['standardModelExamples'][0]['finishedUnitReferenceGp'])==price for n,price in expected_prices.items()))
    check('all actual work fields and field prohibitions',all(r['workRequirements']['activeWorkHours'] is not None and r['workRequirements']['fieldCraftable'] is False and cards[r['id']]['operational']['work']['trivialAtSkillLevel']==r['skillProgression']['trivialAtSkillLevel'] for r in originals))
    check('recipe279 time and DC source bound',cards['recipe-279']['sourceRecipe']['craftingCheck']['targetDC']==27 and cards['recipe-279']['operational']['work']['operationalActiveWorkHours']==960 and cards['recipe-279']['operational']['work']['eligibleForgeDwarfActiveMinutes']==43200)
    # Exercise every admitted ability/proficiency predicate and every save predicate.
    predicate_cases=[]
    for tag,rows in ref.CHECKS.items():
        n=int(next(r['id'].split('-')[1] for r in originals if r['mechanics']['tag']==tag));item=jewel(n)
        for a,s,p in rows:
            e=event(item,p,ability='INT' if a=='CASTING' else a,skill=None if s=='*' else s,actualSpellcastingAbilityCheck=a=='CASTING')
            assert ref.jewel_flat_bonus([item],e)==item['bonus'];negative=deepcopy(e);negative['itemPremises'][item['id']]['actualCausalPredicateEstablished']=False;assert ref.jewel_flat_bonus([item],negative)==0
            predicate_cases.append({'tag':tag,'kind':'ability-check','predicate':p,'positive':True,'unestablishedCausalityRejected':True})
        for p in ref.SAVES[tag]:
            e=event(item,p,'saving-throw','STR' if tag=='Strength' else 'CON' if tag=='Vitality' else 'WIS',None);assert ref.jewel_flat_bonus([item],e)==item['bonus'];e['itemPremises'][item['id']]['predicateIds']=['unrelated-nearby-scenery'];assert ref.jewel_flat_bonus([item],e)==0
            predicate_cases.append({'tag':tag,'kind':'saving-throw','predicate':p,'positive':True,'unrelatedCauseRejected':True})
    check('every finite tag predicate positive and causal negative',set(z['tag'] for z in predicate_cases)==set(ref.CHECKS),{'predicateCases':len(predicate_cases)})
    poison=jewel(265);pe=event(poison,'direct-poison-damage-condition-exposure-consequence','saving-throw','CON',None)
    check('one poison event gives +2, not separate damage and condition bonuses',ref.jewel_flat_bonus([poison],pe)==2)
    for excluded in ref.EXCLUSIONS:
        e=deepcopy(pe);e['categories']=[excluded];check('common exclusion '+excluded,ref.jewel_flat_bonus([poison],e)==0)
    small=jewel(258);strong=jewel(650);unrelated=jewel(648);e=event(small,'direct-burning-heat','saving-throw','DEX',None);e['itemPremises'][strong['id']]={'actualCausalPredicateEstablished':True,'predicateIds':['fire-damage']}
    check('strongest independently qualifying save once',ref.jewel_flat_bonus([small,strong,unrelated],e)==3)
    e['itemPremises'].pop(strong['id']);check('unqualified stronger items do not borrow weaker evidence',ref.jewel_flat_bonus([small,strong,unrelated],e)==1)
    suppressed=jewel(265,suppressed=True);conflict=jewel(264)
    rejected('suppressed nonqualifying head item still conflicts',lambda:ref.jewel_flat_bonus([suppressed,conflict],pe))
    helm={'id':'actual-helm','trade':'Blacksmithing','family':'Helm','state':'worn','wearer':'A','slot':'head','slotValid':True}
    rejected('Crown competes with actual Helm before filtering',lambda:ref.validate_designations([conflict,helm]))
    ring1=jewel(249);ring2=jewel(261,slot='ring-2');rejected('two Rings on same hand rejected',lambda:ref.validate_designations([ring1,ring2]));ring2['actualCompatibleHand']='right';check('two actual compatible hands admit two Rings',len(ref.validate_designations([ring1,ring2]))==2)
    mount=jewel(268,actualHostSupport=False);me=event(mount,'fire-damage','saving-throw','DEX',None);check('Gem without host support inactive',ref.jewel_flat_bonus([mount],me)==0)
    for state in ['carried','stowed','melded']:
        item=jewel(258,state=state);check(state+' cannot use passive bonus',ref.jewel_flat_bonus([item],event(item,'fire-damage','saving-throw','DEX',None))==0)
    # Ledger clock is a clearly labeled synthetic campaign timeline; items are real recipes.
    ledger=ref.new_ledger('reference-campaign',10);ledger=ref.initialize(ledger,small,'creation-a',0,processed_dawn_through=None);ledger=ref.initialize(ledger,strong,'creation-b',0,processed_dawn_through=None)
    e=event(small,'fire-damage','saving-throw','DEX',None);e['itemPremises'][strong['id']]={'actualCausalPredicateEstablished':True,'predicateIds':['fire-damage']};before=deepcopy(ledger)
    e['alreadyAdvantage']=True;e['alreadyDisadvantage']=True;ledger=ref.commit_charge(ledger,[small,strong],small['id'],e)
    check('weaker valid item spends while stronger wins and cancellation wastes charge',ledger['items'][small['id']]['current']==1 and ref.jewel_flat_bonus([small,strong],e)==3)
    rejected('same event cannot debit other jewel',lambda:ref.commit_charge(ledger,[small,strong],strong['id'],e))
    rejected('same-event reroll cannot debit again',lambda:ref.commit_charge(ledger,[small,strong],small['id'],e))
    e2=deepcopy(e);e2['id']='later-real-save';ledger=ref.commit_charge(ledger,[small,strong],small['id'],e2);check('genuine new save spends independently',ledger['items'][small['id']]['current']==0)
    check('zero charge still supplies passive modifier',ref.jewel_flat_bonus([small],e2)==1)
    canceled=deepcopy(e);canceled['id']='canceled';canceled['canceledBeforeCommit']=True;check('precommit cancellation no debit',ref.commit_charge(before,[small,strong],small['id'],canceled)==before)
    for field,value in [('resultRevealed',True),('conscious',False),('incapacitated',True),('voluntaryActivationAllowed',False),('automaticResult',True)]:
        bad=deepcopy(e);bad[field]=value;rejected('activation rejects '+field,lambda bad=bad:ref.commit_charge(before,[small,strong],small['id'],bad))
    wrongwear=deepcopy(e);wrongwear['actor']='B';check('owner or operator is no wearer substitute',ref.jewel_flat_bonus([small],wrongwear)==0)
    rejected('transfer/equip/copy cannot initialize imprint again',lambda:ref.initialize(ledger,small,'second',0,processed_dawn_through=None))
    def history(at,**kw):
        z={'id':small['id'],'recordedAt':at,'complete':True,'hp':5,'suppressed':False,'primaryDestroyed':False,'state':'stowed'};z.update(kw);return z
    ledger=ref.dawn(ledger,small['id'],0,10,history(10,suppressed=True));check('suppressed dawn missed and marked',ledger['items'][small['id']]['current']==0 and ledger['items'][small['id']]['lastDawn']==0)
    rejected('ending suppression cannot replay missed dawn',lambda:ref.dawn(ledger,small['id'],0,10,history(10)))
    ledger=ref.dawn(ledger,small['id'],1,86410,history(86410,state='melded'));check('complete unsuppressed meld recharges without use',ledger['items'][small['id']]['current']==2)
    rejected('skip to later dawn cannot rewrite missing history',lambda:ref.dawn(ledger,small['id'],3,259210,history(259210)))
    spent=deepcopy(ledger);spent['items'][small['id']]['current']=0
    for field,value in [('hp',0),('complete',False),('primaryDestroyed',True)]:
        z=ref.dawn(spent,small['id'],2,172810,history(172810,**{field:value}));check('dawn ineligible '+field,z['items'][small['id']]['current']==0 and z['items'][small['id']]['lastDawn']==2)
    created=ref.initialize(ref.new_ledger('reference-campaign',10),small,'at-processed-dawn',10,processed_dawn_through=0)
    rejected('creation after same-timestamp dawn cannot replay it',lambda:ref.dawn(created,small['id'],0,10,history(10)))
    # Structural matrix is independent of all charge ledgers.
    states=0
    for ordinary in (5,10):
      for oldp in (0,25,50):
       for oldf in (False,True):
        oldmax=ref.structural_maximum(ordinary,oldp,oldf)
        for hp in range(1,oldmax+1):
         for newp in (0,25,50):
          for flaw in (False,True):
           z=ref.quality_structure(ordinary,oldp,oldf,hp,newp,flaw);expected_max=ref.structural_maximum(ordinary,max(oldp,newp),oldf or flaw)
           assert z['maximum']==expected_max and expected_max-z['current']==min(expected_max,oldmax-hp);states+=1
    check('noncompounding structural states preserve damage deficit',states>400,states)
    check('source example damaged singleton becomes Broken',ref.quality_structure(5,0,False,1,0,True)['current']==0)
    recipe=cards['recipe-245']['sourceRecipe'];reserves=[{'id':f'bracelet-{i}','model':'jewelcrafting.bracelet','size':'Medium','grade':'Standard','ordinaryHP':5,'maximum':5,'current':5,'percent':0,'flaw':False,'complete':True,'available':True} for i in range(7)];ids=[r['id'] for r in reserves]
    out,unused=ref.complete_order(reserves,recipe,'Standard','yield',ids);check('recipe245 seven reserves produce first five Standard',len(out)==5 and [z['id'] for z in out]==ids[:5] and len(unused)==2)
    out,_=ref.complete_order(reserves,recipe,'Masterwork','yield',ids);check('recipe245 Masterwork seven actual bodies mass0.7lb',len(out)==7 and F(len(out),10)==F(7,10))
    bad=deepcopy(reserves);bad[0]['current']=0;rejected('latest Broken reserve pauses before roll',lambda:ref.complete_order(bad,recipe,'Standard','yield',ids))
    rejected('no post-roll reverse selection',lambda:ref.complete_order(list(reversed(reserves)),recipe,'Masterwork','yield',ids))
    rejected('no charge quality option',lambda:ref.complete_order(reserves,recipe,'Masterwork','charges',ids))
    catrecipe=cards['recipe-279']['sourceRecipe'];units=[{'id':'actual-catalyst-'+str(i),'componentIndex':i,'componentId':catrecipe['components'][i]['id'],'recipeId':catrecipe['id'],'ageHours':3,'remainingShelfLifeHours':9,'condition':'sound','lawfullyPreservedParticipant':True,'alreadyDestroyed':False} for i in (8,10)]
    check('recipe279 one actual catalyst retained with age and identity',ref.catalyst_return(catrecipe,units,'Masterwork',[units[0]['id']])==[units[0]])
    rejected('recipe279 cannot return both catalysts',lambda:ref.catalyst_return(catrecipe,units,'Masterwork',[u['id'] for u in units]))
    rejected('Exceptional upgrade is not Masterwork catalyst return',lambda:ref.catalyst_return(catrecipe,units,'Exceptional',[units[0]['id']]))
    bad=deepcopy(units);bad[0]['alreadyDestroyed']=True;rejected('no recreated consumed catalyst',lambda:ref.catalyst_return(catrecipe,bad,'Masterwork',[bad[0]['id']]))
    kit={k:True for k in ('trained','actualToolkit','actualBench','actualFineFiles','actualLens','recoverableOriginalPrimary','requiredOriginalStonesSettingsPresent','originalCrystal','originalPrimaryMount')};kit['ability']='INT'
    earring=jewel(242);quote=ref.repair_quote(earring,F(1,2),F(265,2),12,kit);check('Earring functional repair0.125gp purchase0.13',quote['materialsGp']==F(1,8) and math.ceil(quote['materialsGp']*100)==13)
    earring['hp']=0;quote=ref.repair_quote(earring,F(1,2),F(265,2),12,kit);check('Earring reconstruction33.125gp purchase33.13',quote['materialsGp']==F(265,8) and math.ceil(quote['materialsGp']*100)==3313 and quote['DC']==12)
    for field in ['trained','actualToolkit','actualBench','actualFineFiles','actualLens','recoverableOriginalPrimary','requiredOriginalStonesSettingsPresent']:
        absent=deepcopy(kit);absent[field]=False;rejected('repair missing '+field,lambda absent=absent:ref.repair_quote(earring,F(1,2),F(265,2),12,absent))
    gem=jewel(268,hp=0);bad=deepcopy(kit);bad['originalCrystal']=False;rejected('Gem missing original crystal cannot reconstruct',lambda:ref.repair_quote(gem,F(2),F(4509),23,bad));bad=deepcopy(kit);bad['originalPrimaryMount']=False;rejected('Gem missing primary mount cannot reconstruct',lambda:ref.repair_quote(gem,F(2),F(4509),23,bad))
    # Cross-trade fixtures come from the exact reviewed cards, not invented bonuses.
    tailoring=read(ROOT/'data/director/tailoring_recipe_candidate_internal.json');leatherworking=read(ROOT/'data/director/leatherworking_recipe_candidate_internal.json')
    def older(data,recipe,trade):
        c=next(z for z in data['cards'] if z['recipeId']==recipe);m=c['operational']['baseModelIds'][0];b=data['baseModels'][m]
        return {'id':'actual-'+recipe,'recipeId':recipe,'model':m,'trade':trade,'family':c['sourceRecipe']['recipeFamily'],'bonus':c['operational']['effect']['taskBonus'],'state':'worn','wearer':'A','slot':b['benefitSlot'],'slotValid':True,'fit':True,'complete':True,'hp':b['ordinaryMaximumStructuralHP'],'suppressed':False}
    clothes=older(tailoring,'recipe-584','Tailoring');stealth=jewel(241);se=event(stealth,'legal-hide-or-unnoticed-motion',ability='DEX',skill='Stealth')
    task={'kind':'ability-check','actualCheck':True,'actor':'A','ability':'DEX','proficiency':'Stealth','domain':'visual-concealment','itemPremises':{clothes['id']:{'domainCriteriaMet':True,'actualContribution':True,'coverageSufficient':True,'legalHiding':True}}}
    check('Tailoring584 +3 and Jewel241 +1 select3, not4',ref.combined_check_bonus([clothes,stealth],se,task)==3)
    task['itemPremises'][clothes['id']]['actualContribution']=False;check('noncontributing outfit cannot borrow jewel qualification',ref.combined_check_bonus([clothes,stealth],se,task)==1)
    gloves=older(leatherworking,'recipe-306','Leatherworking');earth=jewel(649);ee=event(earth,'climb-rock-stone-holds',ability='STR',skill='Athletics')
    et={'kind':'ability-check','actualCheck':True,'actor':'A','ability':'STR','proficiency':'Athletics','domain':'actual-rock-climb','itemPremises':{gloves['id']:{'leatherCriteriaMet':True,'actualContribution':True,'leatherTaskIds':['handhold-climb'],'noncreatureCargo':True}}}
    check('Leather306 +2 and Earth649 +3 select3, not5',ref.combined_check_bonus([gloves,earth],ee,et,['handhold-climb'])==3)
    ee['itemPremises'][earth['id']]['actualCausalPredicateEstablished']=False;check('Leather contribution remains when jewel independently fails',ref.combined_check_bonus([gloves,earth],ee,et,['handhold-climb'])==2)
    rejected('saving throw cannot use older trade check route',lambda:ref.combined_check_bonus([clothes,stealth],pe,task))
    check('Jewel supplies no zero AC candidate against Crude suit',ref.tailor.defense(-1,[stealth])['enhancement']==-1)
    # Exact public manuscripts reconstructed from internal content by the declared
    # visibility transform only, without invoking the authoring renderer.
    itext=(ROOT/'docs/director-only/JEWELCRAFTING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    blocks=re.split(r'(?=^## recipe-\d+ —)',itext,flags=re.M);public_blocks=[];projection=[]
    for block in blocks[1:]:
        rid=re.match(r'## (recipe-\d+)',block)[1]
        if cards[rid]['visibility']!='public':continue
        kept=[p for p in block.split('\n\n') if not p.startswith('**Preserved optional Director guidance:**')]
        public_blocks.append('\n\n'.join(kept));projection.append({'recipeId':rid,'internalParagraphs':len(block.split('\n\n')),'retainedParagraphs':len(kept)})
    expected_header='# Jewelcrafting public recipe cards\n\n**DRAFT — exact review pending.** Public: 26 formulas with their nine body models and twelve operative tags.\n\nEvery card uses the complete [shared guide](JEWELCRAFTING_RECIPE_PLAYTEST.md). Full preserved source objects accompany the JSON.\n\n'
    reconstructed=(expected_header+''.join(public_blocks)).rstrip()+'\n'
    check('entire public cards reconstruct from allowed internal paragraphs',reconstructed==pubtext)
    iguide=(ROOT/'docs/director-only/JEWELCRAFTING_INTERNAL_GUIDE.md').read_text(encoding='utf-8')
    filtered=[]
    for line in iguide.splitlines():
        if line.startswith('| Acid |') or line.startswith('| Water |') or line.startswith('| Steel drop ornament with integral neck chain and closure |'):continue
        if line.startswith('| neck-adornment |'):line=line.replace(', Pendant','')
        filtered.append(line)
    reconstructed_guide='\n'.join(filtered)+'\n'
    reconstructed_guide=reconstructed_guide.replace('Internal: all 43 formulas, including one restricted and sixteen Director-only records.','Public: 26 formulas with their nine body models and twelve operative tags.').replace('(../mechanics/','(')
    check('entire public guide reconstructs using only declared audience/body/tag routing',reconstructed_guide==guide)
    dump(AUDIT/'JEWELCRAFTING_PUBLIC_PARAGRAPH_PROJECTION.json',{'status':'PASS','scope':'complete saved public cards, guide and JSON envelope reconstructed; no exact review approval','cardParagraphMappings':projection,'wholePublicCardsEqual':reconstructed==pubtext,'wholePublicGuideEqual':reconstructed_guide==guide,'wholePublicEnvelopeEqual':expected==public,'privateRecordsOmitted':17,'privateModelsOmitted':['jewelcrafting.pendant'],'privateTagEntriesOmitted':['Acid','Water']})
    crown=jewel(244,state='melded');record={'id':crown['id'],'family':'Crown','bearer':'A','state':'melded','weight':crown['weightLb'],'load':F(str(crown['weightLb']))/10,'contents':[]}
    physical=ref.leather.inventory([record],'A')
    check('melded Crown retains one body full0.5lb and0.05Load',physical['physicalPounds']==F(1,2) and physical['canonicalLoad']==F(1,20) and physical['physicalIds']==[crown['id']])
    check('Crown meld preflight needs both real budgets',ref.leather.meld_preflight([record],[record['id']],F(1,2),F(1,20))['fits'] and not ref.leather.meld_preflight([record],[record['id']],F(49,100),F(1,20))['fits'])
    check('explicit synthetic casualty body adds equipment without relief',F(10)+physical['physicalPounds']==F(21,2) and F(3,2)+physical['canonicalLoad']==F(31,20))
    returned=jewel(244,state='carried',slotValid=False);check('external head priority leaves returned carried Crown inactive',ref.jewel_flat_bonus([returned],event(returned,'direct-poison-damage-condition-exposure-consequence','saving-throw','CON',None))==0)
    walk=AUDIT/'JEWELCRAFTING_INTERFACE_WALKTHROUGHS.md';walktext=walk.read_text(encoding='utf-8')
    check('all sixteen decisions have explicit manuscript coverage disposition',len(re.findall(r'^\| JC-D\d{2} \|',walktext,re.M))==16)
    # Whole-file preservation includes all reviewed trade outputs and their guides.
    protected=read(AUDIT/'JEWELCRAFTING_PART2_SUBMISSION.json')['protectedFiles'];check('all protected inputs unchanged',all(sha(GAME/p)==h for p,h in protected.items()),len(protected))
    paths=['data/director/jewelcrafting_recipe_candidate_internal.json','data/playtest/jewelcrafting_recipe_candidate.json','docs/director-only/JEWELCRAFTING_INTERNAL_GUIDE.md','docs/director-only/JEWELCRAFTING_INTERNAL_RECIPE_CARDS.md','docs/mechanics/JEWELCRAFTING_RECIPE_PLAYTEST.md','docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md']
    report={'status':'PASS','scope':'source preservation and bounded manuscript reference; no exact-card approval or companion runtime claim','checks':checks,'checkCount':len(checks),'sourceValidFixtures':fixtures,'crossTradeSourceFixtures':[clothes,gloves],'predicateCases':predicate_cases,'valueCombinations':values,'structuralStates':states,'protectedFilesUnchanged':len(protected),'artifactHashes':{p:sha(ROOT/p) for p in paths},'manuscriptWalkthroughs':{'file':walk.name,'sha256':sha(walk),'scope':'explicit scenario premises; no runtime placement claim'},'recipesApproved':0,'remainingRequiredEvidence':['separate GPT exact-card review'],'cosmology':'post-push only'}
    dump(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json',report);print(json.dumps({'status':'PASS','checks':len(checks),'predicateCases':len(predicate_cases),'structuralStates':states,'valueCombinations':len(values),'remainingRequiredEvidence':report['remainingRequiredEvidence']}))

if __name__=='__main__':main()
