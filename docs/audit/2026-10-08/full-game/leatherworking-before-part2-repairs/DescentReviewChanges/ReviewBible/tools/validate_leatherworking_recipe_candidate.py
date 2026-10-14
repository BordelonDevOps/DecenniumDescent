"""Independent source assertions and bounded behavioral examples; no promotion."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from collections import Counter
import json,hashlib,zipfile,xml.etree.ElementTree as ET
import leatherworking_reference as ref

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rat(x):return F(x['numerator'],x['denominator'])
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list):return [clean(v) for v in x]
    return x

def main():
    checks=[];cases=[]
    def check(name,ok,detail=None):
        checks.append({'name':name,'passed':bool(ok),**({'detail':detail} if detail is not None else {})})
    def case(name,ok,result=None):
        cases.append({'name':name,'passed':bool(ok),'result':clean(result)});check('Behavior: '+name,ok)
    def rejects(fn):
        try:fn();return False
        except ValueError:return True
    data=read(ROOT/'data/director/leatherworking_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/leatherworking_recipe_candidate.json')
    source=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    evidence=read(AUDIT/'LEATHERWORKING_SOURCE_PREPARATION.json')
    baseline=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')
    rs=[r for r in source['recipes'] if r['skill']=='Leatherworking'];by={r['id']:r for r in rs}
    cards=data['cards'];cb={c['recipeId']:c for c in cards};models=data['baseModels'];pmodels=public['baseModels']
    guides=[(ROOT/p).read_text(encoding='utf-8') for p in ['docs/mechanics/LEATHERWORKING_RECIPE_PLAYTEST.md','docs/director-only/LEATHERWORKING_INTERNAL_GUIDE.md']]
    pmd=(ROOT/'docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8');imd=(ROOT/'docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    check('44 complete original recipe records preserved in source order',[c['sourceRecipe'] for c in cards]==rs==evidence['recipes'] and len(cards)==44)
    check('All original source indices exact',all(source['recipes'][c['sourceRecipeIndex']]==c['sourceRecipe'] for c in cards))
    check('42 protected sources and reviewed dependencies unchanged',len(baseline['files'])==42 and all(sha(GAME/p)==h for p,h in baseline['files'].items()))
    check('Visibility remains 30 public,1 restricted,13 Director-only',Counter(r['visibility'] for r in rs)=={'public':30,'restricted':1,'director-only':13})
    check('All44 cards still await exact approval',not data['exactRecipeApproval'] and not data['runtimeImplemented'] and not data['balanceApproved'] and all(c['status']=='authored-draft-awaiting-exact-review' for c in cards) and not (ROOT/'docs/mechanics/LEATHERWORKING_REVIEW_STATUS.json').exists())
    check('Source conference has actual completed turn/reply provenance',data['sourceConferenceTurnId']=='86413ad7-8096-4e6f-baca-3cab34aa66a3' and data['sourceConferenceReplyId']=='4f808c26-f93b-4b50-ac05-a917b7ca2b7e' and 'No Leatherworking recipe is promoted by this conference.' in (AUDIT/'GPT_LEATHERWORKING_SOURCE_CONFERENCE.txt').read_text(encoding='utf-8'))
    public_ids={r['id'] for r in rs if r['visibility']=='public'}
    check('Exact30 public recipe IDs, no others',{c['recipeId'] for c in public['cards']}==public_ids and len(public['cards'])==30)
    def private_paths(x,path=''):
        out=[]
        if isinstance(x,dict):
            for k,v in x.items():
                if k in ('directorGuidance','directorNotes','secret','secrets') or k=='visibility' and v in ('restricted','director-only','director-internal'):out.append(path+'/'+k)
                out+=private_paths(v,path+'/'+k)
        elif isinstance(x,list):
            for i,v in enumerate(x):out+=private_paths(v,path+'/'+str(i))
        return out
    check('Public projection has no private nested guidance or visibility',not private_paths(public))
    def public_source(r):
        r=deepcopy(r)
        for key in ['directorGuidance','directorNotes','secret','secrets']:r.pop(key,None)
        return r
    check('Public source fields including legitimate nulls remain exact',all(c['sourceRecipe']==public_source(by[c['recipeId']]) for c in public['cards']))
    public_text=json.dumps(public,ensure_ascii=False)+pmd+guides[0]
    check('Hidden formula IDs and full names absent from every public artifact',all(r['id'] not in public_text and r['name'] not in public_text for r in rs if r['visibility']!='public'))
    used={id for c in public['cards'] for id in c['operational']['baseModelIds']}
    check('Public model projection contains exactly14 used bodies',len(pmodels)==14 and set(pmodels)==used and all(pmodels[id]==models[id] for id in used))
    check('Public operational cards equal corresponding internal cards',all(c['operational']==cb[c['recipeId']]['operational'] for c in public['cards']))
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    with zipfile.ZipFile(book) as z:
        tree=ET.fromstring(z.read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in tree.findall('.//w:p',ns)]
    check('All30 book bindings independently match original DOCX paragraphs',sha(book)==evidence['bookSha256'] and len(evidence['publicBookBindings'])==30 and all(all(paras[p['index']]==p['text'] for p in b['paragraphs']) and b['paragraphs'][1]['text']=='Effect. '+by[b['recipeId']]['effects'] for b in evidence['publicBookBindings']))
    ac={306:1,308:1,309:1,312:1,314:1,315:1,317:2,318:2,319:2,653:1,655:1}
    check('Eleven numerical AC overlays separately declared',len([c for c in cards if c['operational']['sourceArmorOmissionDisposition']])==11 and all(cb[f'recipe-{id}']['operational']['effect']['armorBonusCandidate']==n and 'NEW LW-D01 overlay from mechanics.armorBonus' in cb[f'recipe-{id}']['operational']['text'] and 'AC' not in by[f'recipe-{id}']['effects'] for id,n in ac.items()))
    check('Both public omissions keep actual V5 paragraph and original prose',paras[1731]=='Effect. '+by['recipe-308']['effects'] and paras[1717]=='Effect. '+by['recipe-653']['effects'] and all('AC' not in paras[i] for i in (1731,1717)))
    check('Nine zero-AC wearables create no phantom zero candidate',sum(r['mechanics'].get('armorBonus')==0 for r in rs)==9 and all(cb[r['id']]['operational']['effect']['armorBonusCandidate'] is None for r in rs if r['mechanics'].get('armorBonus')==0))
    expected_res={'recipe-312':'force','recipe-314':'force','recipe-315':'thunder','recipe-317':'thunder','recipe-318':'cold','recipe-319':'cold','recipe-655':'cold'}
    check('Exactly seven printed resistances retained',{c['recipeId']:c['operational']['effect']['resistance'] for c in cards if c['operational']['effect']['resistance']}==expected_res)
    check('Acidproof title does not add resistance',cb['recipe-653']['operational']['effect']['resistance'] is None and 'No damage resistance or environmental immunity' in cb['recipe-653']['operational']['text'])
    check('All44 task bonuses exactly match numerical source fields',all(c['operational']['effect']['taskBonus']==c['sourceRecipe']['mechanics'].get('bonus',c['sourceRecipe']['mechanics'].get('skillBonus')) for c in cards))
    check('All24 relief allowances exact and independent of physical capacity',sum('capacityPounds' in r['mechanics'] for r in rs)==24 and all(c['operational']['effect']['reliefAllowanceLb']==c['sourceRecipe']['mechanics']['capacityPounds'] and models[c['operational']['baseModelIds'][0]]['physicalContentWeightLimitLb']>=c['operational']['effect']['reliefAllowanceLb'] for c in cards if c['sourceRecipe']['outputType']=='container'))
    check('All201 component occurrences consumed; zero catalysts/tools',sum(len(r['components']) for r in rs)==201 and all(z['consumed'] and z['role'] not in ('catalyst','tool') for r in rs for z in r['components']) and all(c['operational']['outcomes']['eligibleCatalystReturns']==0 for c in cards))
    check('All field flags false; four contradictory labels preserved',all(not r['workRequirements']['fieldCraftable'] for r in rs) and {r['id'] for r in rs if r['workRequirements']['timeMode']=='field'}=={'recipe-283','recipe-285','recipe-292','recipe-293'})
    check('One-year null and zero labor preserved, overlay explicit',by['recipe-319']['workRequirements']['activeWorkHours'] is None and by['recipe-319']['economy']['laborValue']==0 and cb['recipe-319']['operational']['work']['operationalActiveWorkHours']==1920 and cb['recipe-319']['operational']['work']['eligibleForgeDwarfActiveMinutes']==86400)
    check('All work durations, assistant caps and trivial thresholds copied exactly',all(c['operational']['work']['sourceActiveWorkHours']==r['workRequirements']['activeWorkHours'] and c['operational']['work']['maximumAssistants']==r['workRequirements']['maximumAssistants'] and c['operational']['work']['trivialAtSkillLevel']==r['skillProgression']['trivialAtSkillLevel'] for c in cards for r in [by[c['recipeId']]]))
    check('All Forge Dwarf times round up to whole minute, phases included',all(c['operational']['work']['eligibleForgeDwarfActiveMinutes']==-(-(F(str(c['operational']['work']['operationalActiveWorkHours']))*45).numerator//(F(str(c['operational']['work']['operationalActiveWorkHours']))*45).denominator) and c['operational']['work']['eligibleForgeDwarfFirstPhaseMinutes']==min(480,c['operational']['work']['eligibleForgeDwarfActiveMinutes']) for c in cards))
    check('All reserve and quality quantities independently recomputed',all(c['operational']['maximumBaseReserve']==(3*r['quantity'])//2 and c['operational']['outcomes']=={'Standard':r['quantity'],'ExceptionalYield':5*r['quantity']//4,'MasterworkYield':3*r['quantity']//2,'DurabilityOptionQuantity':r['quantity'],'FlawedQuantity':max(1,r['quantity']//2),'SingletonFlawedAddsPersistentFlaw':r['quantity']==1,'Failed':0,'Mishap':0,'eligibleCatalystReturns':0} for c in cards for r in [by[c['recipeId']]]))
    eq=read(ROOT/'data/playtest/equipment_acquisition_candidate.json')['items'];eqby={z['id']:z for z in eq}
    check('Four original equipment records retained in full',sum(m['sourceEquipmentRecord'] is not None for m in models.values())==4 and all(m['sourceEquipmentRecord']==eqby[m['sourceEquipmentRecord']['id']] for m in models.values() if m['sourceEquipmentRecord']))
    check('Exactly19 bodies,12 containers and3 permitted armor suits',len(models)==19 and sum('physicalContentWeightLimitLb' in m for m in models.values())==12 and {m['name'] for m in models.values() if m['family']=='Armor'}=={'Leather','Studded leather','Hide'})
    check('Backpack body preserves fixed size flag and original values',models['leather.backpack']['sourceEquipmentRecord']['largeSizingEligible'] is False and (models['leather.backpack']['baselinePriceGp'],models['leather.backpack']['baselineWeightLb'],models['leather.backpack']['ordinaryMaximumStructuralHP'])==(2,5,10))
    expected_bodies={
      'leather.backpack':(2,5,30,F(1),10,[18,12,8],[12,8],[20,14,10],1),
      'leather.pouch-1':(1,2,10,F(1,3),5,[12,8,6],[12,6],[13,9,7],1),
      'leather.pouch-2':(2,3,20,F(2,3),5,[12,8,12],[12,12],[13,9,13],1),
      'leather.pouch-3':(3,4,30,F(1),5,[12,8,18],[12,18],[13,9,19],1),
      'leather.quiver-1':(2,2,10,F(1,3),5,[36,4,4],[4,4],[38,6,6],1),
      'leather.quiver-3':(6,6,30,F(1),5,[36,4,4],[4,4],[38,18,6],3),
      'leather.quiver-4':(8,8,40,F(4,3),5,[36,4,4],[4,4],[38,24,6],4),
      'leather.belt-1':(2,2,10,F(1,3),5,[12,8,6],[12,6],[13,9,7],1),
      'leather.belt-2':(4,4,20,F(2,3),5,[12,8,6],[12,6],[13,9,7],2),
      'leather.belt-3':(6,6,30,F(1),5,[12,8,6],[12,6],[13,9,7],3),
      'leather.belt-5':(10,10,50,F(5,3),5,[12,8,6],[12,6],[13,9,7],5),
      'leather.harness':(10,10,50,F(5,3),10,[30,12,8],[30,12],[32,14,10],1)}
    check('All12 exact container bodies match independently transcribed verdict',all((m['baselinePriceGp'],m['baselineWeightLb'],m['physicalContentWeightLimitLb'],rat(m['physicalContentVolumeFt3']),m['ordinaryMaximumStructuralHP'],m['interiorInches'],m['openingInches'],m['exteriorInches'],m['compartmentCount'])==exp for id,exp in expected_bodies.items() for m in [models[id]]))
    check('Every compartment geometric volume matches its finite body volume',all(F(m['interiorInches'][0]*m['interiorInches'][1]*m['interiorInches'][2],1728)==rat(m['compartmentVolumeFt3']) and rat(m['physicalContentVolumeFt3'])==m['compartmentCount']*rat(m['compartmentVolumeFt3']) for m in models.values() if 'compartmentCount' in m))
    check('Container fitting cannot scale price weight HP capacity',all(not m['largeSizingEligible'] and m['largePriceWeightHPMultiplier']==1 and m['gradePolicy']=='Standard only' for m in models.values() if 'compartmentCount' in m))
    check('Four accessories have exact pair/body values and size policies',all((models[id]['baselinePriceGp'],models[id]['baselineWeightLb'],models[id]['ordinaryMaximumStructuralHP'],models[id]['largePriceWeightHPMultiplier'],models[id]['gradePolicy'])==(price,weight,5,2,'Standard only') for id,price,weight in [('leather.boots',2,2),('leather.gloves',1,0.5),('leather.leather-gear',5,4),('leather.coat',10,6)]))
    check('Every card spells out its preserved and operational effects',all(imd.count('## '+c['recipeId']+' — ')==1 and '**Preserved effect:** '+c['sourceRecipe']['effects'] in imd and '**Operational effect:** '+c['operational']['text'] in imd for c in cards) and all(pmd.count('## '+c['recipeId']+' — ')==1 and '**Operational effect:** '+c['operational']['text'] in pmd for c in public['cards']))
    check('Per-item source share and model values exactly recomputed',all(rat(c['operational']['value']['sourceProcessUnitReferenceGp'])==F(str(c['sourceRecipe']['economy']['recommendedMarketValue']))/c['sourceRecipe']['quantity'] and all(rat(e['finishedUnitReferenceGp'])==rat(c['operational']['value']['sourceProcessUnitReferenceGp'])+F(str(models[e['baseModelId']]['baselinePriceGp'])) for e in c['operational']['standardModelExamples']) for c in cards))
    check('Four independently specified valuation examples',all(rat(cb[id]['operational']['standardModelExamples'][0]['finishedUnitReferenceGp'])==value for id,value in [('recipe-280',F(93,2)),('recipe-652',F(1198)),('recipe-653',F(1059)),('recipe-655',F(6292))]))

    def cargo(id,w,l=None,**kw):return {'id':id,'weight':w,'load':F(str(w))/10 if l is None and w is not None else l,**kw}
    def bag(id='pack',w=5,r=10,children=(),family='Backpack',slot='back-cargo',bearer='A',**kw):
        return cargo(id,w,contents=list(children),family=family,relief=r,slot=slot,bearer=bearer,state='worn',fit=True,hp=10,complete=True,location='floor',**kw)
    def totals(inv,pounds,load):return inv['countedPounds']==pounds and inv['effectiveLoad']==load
    def worn(fam='Boots',bonus=1,**kw):return {'family':fam,'bonus':bonus,'armorBonus':bonus,'hp':5,'fit':True,'complete':True,'state':'worn','slotValid':True,**kw}

    a=ref.defense(-1,[worn(bonus=0)]);case('LW-01 zero modifier cannot cancel Crude; positive numerical overlay can',a['enhancement']==-1 and ref.defense(-1,[worn(bonus=1)])['enhancement']==1,a)
    a=ref.defense(1,[worn('Armor',2,selectedArmorFormula=True,resistance='cold'),worn(bonus=1),worn('Gauntlets',3)])
    case('LW-02 strongest eligible enhancement; ordinary shield remains separate',a['enhancement']==3 and a['resistances']==['cold'] and 12+2+a['enhancement']+2==19,a)
    a=ref.defense(-1,[worn('Armor',2,selectedArmorFormula=False,resistance='cold'),worn(bonus=2,suppressed=True)])
    case('Unselected suit retains resistance but no recipe AC; suppression disables accessory',a=={'enhancement':-1,'resistances':['cold']},a)
    a=ref.defense(None,[{**worn(bonus=1),'state':'melded'},worn(bonus=1,slotValid=False)])
    case('Melded and invalid-slot accessories have no AC candidate',a['enhancement'] is None,a)
    def placed(d,w,vol,comp=0,pos=(0,0,0)):return {'dimensions':d,'weight':w,'volumeFt3':vol,'compartment':comp,'position':pos}
    a=ref.compartment_limits(models['leather.pouch-2'],[placed([10,7,10],20,F(700,1728))]);case('LW-03 complete20-lb cargo fits new20-lb pouch',a,a)
    case('Quiver cannot borrow adjacent sleeve space for an oversized object',not ref.compartment_limits(models['leather.quiver-3'],[placed([36,5,5],9,F(900,1728))]))
    case('Separate quiver sleeves can carry30lb with valid layouts',ref.compartment_limits(models['leather.quiver-3'],[placed([30,3,3],10,F(270,1728),i) for i in range(3)]))
    case('Belt pocket10-lb cap enforced despite unused other pockets',not ref.compartment_limits(models['leather.belt-5'],[placed([10,5,5],11,F(250,1728))]))
    case('Volume cap enforced independently of weight',not ref.compartment_limits(models['leather.pouch-1'],[placed([10,5,5],1,F(1,2))]))
    case('Explicit packing cannot overlap two objects',not ref.compartment_limits(models['leather.backpack'],[placed([5,5,5],2,F(125,1728)),placed([5,5,5],2,F(125,1728))]))
    case('Nested10-lb pouch exterior fits Backpack, larger pouch does not get compressed',ref.orthogonal_box_fit([13,9,7],[18,12,8],[12,8]) and not ref.orthogonal_box_fit([13,9,13],[18,12,8],[12,8]))
    a=ref.inventory([bag(children=['cargo']),cargo('cargo',20)],'A');case('LW-04 R10 pack retains full25lb mass, bearer15lb1.5Load',a['physicalPounds']==25 and a['canonicalLoad']==F(5,2) and totals(a,15,F(3,2)),a)
    records=[bag(r=20,children=['inner']),bag('inner',2,10,['stone'],'Pouch','pouch-1'),cargo('stone',8)]
    a=ref.inventory(records,'A');case('LW-05 nested enchanted pouch inactive, bodyandcontents covered once',a['activeContainers']==['pack'] and totals(a,5,F(1,2)) and a['physicalPounds']==15,a)
    records6=[bag(r=20,children=['sack']),cargo('sack',F(1,2),contents=['water1','water2','rock']),cargo('water1',5,inclusiveGross=True),cargo('water2',5,inclusiveGross=True),cargo('rock',4)]
    a=ref.inventory(records6,'A');case('LW-06 inclusive full waterskins count once, no second water mass',a['physicalPounds']==F(39,2) and totals(a,5,F(1,2)),a)
    case('Expanded inclusive gross record rejected',rejects(lambda:ref.custody([cargo('full',5,inclusiveGross=True,contents=['water']),cargo('water',4)])))
    five=[bag('back',5,10,['c1']),bag('quiver',2,10,['c2'],'Quiver','quiver'),bag('belt',2,10,['c3'],'Belt','waist-cargo'),bag('pouch1',2,10,['c4'],'Pouch','pouch-1'),bag('pouch2',2,10,['c5'],'Pouch','pouch-2')]+[cargo('c'+str(i),10) for i in range(1,6)]
    external=bag('external',5,10,['outside']);external.update(state='carried',slot=None)
    a=ref.inventory(five+[external,cargo('outside',10)],'A');case('LW-07 five separate relief positions, external Backpack inactive',len(a['activeContainers'])==5 and totals(a,28,F(14,5)) and a['physicalPounds']==78,a)
    case('Two simultaneously designated back-cargo occupants rejected',rejects(lambda:ref.inventory([bag('a'),bag('b')],'A')))
    a=ref.inventory([bag(children=['awkward','coins']),cargo('awkward',1,3),cargo('coins',1,F(1,10))],'A');case('LW-08 printed3Load at1lb retains2.9; coin Load can vanish',a['loadCreditById']=={'awkward':F(1,10),'coins':F(1,10)} and totals(a,5,F(17,5)),a)
    transferred=ref.transfer(records,'pack','B','held','back-cargo',True,True);old=ref.inventory(transferred,'A');new=ref.inventory(transferred,'B')
    case('LW-09 transfer moves same subtree exactly once to eligible new holder',old['physicalIds']==[] and new['physicalIds']==['pack','inner','stone'] and totals(new,5,F(1,2)) and transferred[1:]==records[1:],new)
    a=ref.inventory(ref.transfer(records,'pack','B'),'B');case('Recipient carrying without valid hold and slot gets no relief',totals(a,15,F(3,2)),a)
    suppressed=deepcopy(records);suppressed[0]['suppressed']=True;a=ref.inventory(suppressed,'A')
    case('LW-10 suppression stops relief but keeps every contents record',totals(a,15,F(3,2)) and suppressed[0]['contents']==['inner'],a)
    broken,released=ref.break_container(records,'pack');a=ref.inventory(broken,'A')
    case('LW-10 Broken releases immediate inner subtree once, body mass stays',released==['inner'] and broken[1]['contents']==['stone'] and a['physicalIds']==['pack'] and totals(a,5,F(1,2)),{'released':released,'bearer':a})
    pending,_=ref.break_container(records,'pack',same_location_legal=False,adjacent_legal=False)
    case('Unplaceable release remains pending and absent from former contents',pending[1]['state']=='pending-placement' and pending[0]['contents']==[])
    case('Integral Broken strap is not independent support',rejects(lambda:ref.break_container(records,'pack',retained=[('inner','pack')])))
    supported=records+[cargo('support',1,contents=[],hp=5,independentSupport=True,bearer='A')]
    kept,released=ref.break_container(supported,'pack',retained=[('inner','support')]);case('Genuine intact independent support retains subtree without duplication',released==[] and kept[-1]['contents']==['inner'] and kept[0]['contents']==[])
    a=ref.meld_preflight(records,['pack'],10,1);case('LW-11 voluntary meld uses full15lb1.5Load, exceeds10lb1Load',a['fits'] is False and a['pounds']==15 and a['load']==F(3,2),a)
    case('Meld subtree cannot select same contents twice',rejects(lambda:ref.meld_preflight(records,['pack','inner'],100,10)))
    a=ref.meld_preflight(records,['pack'],15,F(3,2));case('Meld exactly at full physical ceilings succeeds',a['fits'],a)
    case('LW-12 rescuer full cargo plus body, no inherited relief',a['pounds']+140==155 and a['load']+4==F(11,2),{'totalPounds':a['pounds']+140,'totalLoad':a['load']+4})
    wear=[worn('Boots',1),worn('Gloves',2)]
    case('LW-13 climb with feet/hands uses strongest task bonus once',ref.task_bonus(wear,True,{'foothold-climb','handhold-climb'})==2)
    citem=worn('Backpack',2,accessible=True);citem.update(state='on-table')
    case('LW-14 easy retrieval grants no check or bonus',ref.task_bonus([citem],False,{'unlocked-retrieval'})==0)
    case('LW-14 ally can handle functional bag on table with no relief slot',ref.task_bonus([citem],True,{'jammed-content'})==2)
    case('LW-15 theft concealment and lockpick get no handling bonus',ref.task_bonus([citem],True,{'theft-concealment','lockpick','Perception'})==0)
    case('LW-15 separate genuine thief jam handling can qualify',ref.task_bonus([citem],True,{'jammed-content'})==2)
    case('No bonus for meld, suppression, combat saves, or temperature endurance',ref.task_bonus([{**citem,'state':'melded'}],True,{'jammed-content'})==0 and ref.task_bonus([{**citem,'suppressed':True}],True,{'jammed-content'})==0 and ref.task_bonus([worn('Coat',2)],True,{'cold-endurance','save','attack'})==0)
    def base(id,current=10,**kw):return {'id':id,'model':'Backpack','size':'Medium','grade':'Standard','ordinaryHP':10,'percent':0,'flaw':False,'current':current,'weight':5,**kw}
    reserves=[base(str(i)) for i in range(6)];standard,unused=ref.complete_order(reserves,4,'Standard');master,_=ref.complete_order(reserves,4,'Masterwork')
    case('LW-16 six reserved Backpack bodies give ordered4/6 output and20/30lb', [z['id'] for z in standard]==['0','1','2','3'] and [z['id'] for z in unused]==['4','5'] and sum(z['weight'] for z in master)==30 and sum(z['weight'] for z in standard)==20)
    case('LW-17 missing and Broken reserves pause before check',rejects(lambda:ref.complete_order([base('a',missing=True)],1,'Standard')) and rejects(lambda:ref.complete_order([base('a',0)],1,'Standard')))
    flawed,_=ref.complete_order([base('x',1)],1,'Flawed');case('LW-17 latest damaged HP produces Broken singleton without free repair',flawed[0]['maximum']==5 and flawed[0]['current']==0,flawed)
    failed,unused=ref.complete_order([base('x',7)],1,'Failed');case('Failed transforms no body; unused actual damaged body returned',failed==[] and unused==[base('x',7)])
    a=ref.apply_quality(10,25,True,3,50,True);case('LW-18 strongest improvement, one flaw last, preserve deficit',a=={'ordinaryHP':10,'percent':50,'flaw':True,'maximum':7,'current':4},a)
    term=ref.repair_terms(0,7,2,F(93,2),9);case('LW-18 reconstruction keeps flawed7HP and finished-unit price',term=={'DC':9,'hours':F(8),'materialsGp':F(93,8),'restoredMaximum':7},term)
    term=ref.repair_terms(1,7,2,F(93,2),9);case('Functional repair uses mundane base reference and DC10',term=={'DC':10,'hours':F(1),'materialsGp':F(1,2),'restoredMaximum':7},term)
    case('Reconstruction cannot manufacture missing pair member',rejects(lambda:ref.repair_terms(0,5,2,1059,16,pair=True,both_members=False)))
    case('LW-19 actual one-year overlay and Forge Dwarf180 phases',cb['recipe-319']['operational']['work']['operationalActiveWorkHours']==1920 and cb['recipe-319']['operational']['work']['eligibleForgeDwarfActiveMinutes']//480==180)
    a=ref.defense(None,[worn('Boots',1),worn('Coat',1,resistance='cold')]);case('LW-20 Acidproof grants no acid resistance, Coat grants cold only',a=={'enhancement':1,'resistances':['cold']},a)
    unknown=[bag(children=['unknown']),cargo('unknown',None,3)];a=ref.inventory(unknown,'A');case('Unknown estimated weight cannot generate pound or Load relief',a['countedPounds'] is None and a['effectiveLoad']==F(7,2) and not a['coveredPoundsById'],a)
    a=ref.inventory([bag(children=['petrified']),cargo('petrified',10,3,creatureBody=True)],'A');case('Creature body and Petrified casualty excluded from relief',totals(a,15,F(7,2)),a)
    a=ref.inventory([bag(children=['rock']),cargo('rock',12)],'A');case('Partial coverage does not physically split12-lb rock',a['coveredPoundsById']['rock']==10 and a['physicalIds']==['pack','rock'] and a['physicalPounds']==17,a)
    case('Cyclic and multiply-parented inventory rejected',rejects(lambda:ref.custody([cargo('a',1,contents=['b']),cargo('b',1,contents=['a'])])) and rejects(lambda:ref.custody([cargo('a',1,contents=['c']),cargo('b',1,contents=['c']),cargo('c',1)])))
    held=bag(children=['x']);held.update(state='held',handsSatisfied=False)
    case('Direct hold still requires real hands',totals(ref.inventory([held,cargo('x',10)],'A'),15,F(3,2)))
    durability_states=0;durability_ok=True
    for b in (5,10,15,20,30):
      for oldp in (0,25,50):
       for oldf in (False,True):
        oldmax=ref.maximum_hp(b,oldp,oldf)
        for current in range(oldmax+1):
         for newp in (0,25,50):
          for newf in (False,True):
           x=ref.apply_quality(b,oldp,oldf,current,newp,newf);improved=b+(max(1,b*max(oldp,newp)//100) if max(oldp,newp) else 0);expected=max(1,improved//2) if oldf or newf else improved
           durability_states+=1;durability_ok &= x['maximum']==expected and x['current']==max(0,expected-oldmax+current) and ref.apply_quality(b,x['percent'],x['flaw'],x['current'],newp,newf)==x
    check('Independent durability-state enumeration preserves deficit and idempotence',durability_ok,{'states':durability_states})
    burden_states=0;burden_ok=True
    for r in (10,20,30,40,50):
      for w in range(0,71):
       for l in (F(w,10),F(3),F(7,3)):
        records=[bag(r=r,children=['x']),cargo('x',w,l)];snapshot=deepcopy(records);x=ref.inventory(records,'A');expected=min(r,w)
        burden_states+=1;burden_ok &= records==snapshot and x['physicalPounds']==5+w and x['canonicalLoad']==F(1,2)+l and x['countedPounds']==5+w-expected and x['effectiveLoad']==F(1,2)+l-min(l,F(expected,10))
    check('Independent burden sweep preserves physical/canonical records and credit caps',burden_ok,{'states':burden_states})
    check('Guide makes geometry, custody, body and damage constraints reviewable',all(all(t in guide for t in ['overloaded custody','stable physical-item-ID order','min(l, r/10)','NewCurrent = max(0','matched pair','equipment.defense-enhancement','equipment.leather-task-enhancement','one Action','1,920-active-hour']) for guide in guides))
    paths=['data/director/leatherworking_recipe_candidate_internal.json','data/playtest/leatherworking_recipe_candidate.json','docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md','docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md','docs/director-only/LEATHERWORKING_INTERNAL_GUIDE.md','docs/mechanics/LEATHERWORKING_RECIPE_PLAYTEST.md']
    result={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','checks':checks,'behaviorCases':cases,'boundedReferenceOnly':True,'durabilityStates':durability_states,'burdenStates':burden_states,'authoredCards':44,'publicCards':30,'recipesApproved':0,'reviewedRecipeTotalUnchanged':218,'protectedFiles':42,'artifactHashes':{p:sha(ROOT/p) for p in paths}}
    (AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:result[k] for k in ('status','durabilityStates','burdenStates','recipesApproved')}|{'checks':len(checks),'behaviorCases':len(cases),'failures':[c['name'] for c in checks if not c['passed']]}))
    if result['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
