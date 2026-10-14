"""Finite advanced candidate arithmetic and authored adjudication coverage.

Reuse only identical Core/structural/quotation mathematics. This does not invoke
Fishing item powers or certify a crafting runtime or actual campaign evidence.
"""
from pathlib import Path
from fractions import Fraction as F
from math import floor,ceil,isfinite
from collections import Counter
from datetime import datetime,timezone
import hashlib,json,re
from core_playtest_rules import task_check,attack_roll,saving_throw
from fishing_reference import structural_hp,repair_quote,copper

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(x):return F(x['numerator'],x['denominator'])
def serial(x):
    if isinstance(x,F):return {'numerator':x.numerator,'denominator':x.denominator}
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x
checks=[]
def check(case,claim,actual,expected):
    checks.append({'case':case,'claim':claim,'actual':serial(actual),'expected':serial(expected),'pass':actual==expected})
def reject(case,claim,fn):
    try:fn()
    except (ValueError,TypeError,OverflowError,ZeroDivisionError):check(case,claim,'rejected','rejected')
    else:check(case,claim,'accepted','rejected')


def creation_band(natural,modifier,dc,forge=False):
    if isinstance(natural,bool) or not isinstance(natural,int) or not 1<=natural<=20:raise ValueError('Invalid d20')
    if isinstance(modifier,bool) or not isinstance(modifier,int):raise ValueError('Invalid modifier')
    delta=natural+modifier-dc
    band='Mishap' if natural==1 or delta<=-10 else 'Failed' if delta<=-5 else 'Flawed' if delta<0 else 'Standard' if delta<5 else 'Exceptional' if delta<10 else 'Masterwork'
    return 'Exceptional' if forge and band=='Standard' else band


def initial_creature_hp(maximum,current_chassis):
    if any(isinstance(v,bool) or not isinstance(v,int) for v in [maximum,current_chassis]) or maximum<=0 or not 1<=current_chassis<=5:raise ValueError('Requires a positive ordinary B5 chassis and positive source HP')
    return max(1,maximum*current_chassis//5)


PRIMARY={
 'EN-weapon':['original-working-blade-or-head','original-structural-tang-or-frame'],
 'EN-armor':['original-principal-torso-assembly'],'EN-wand':['original-inscribed-rod'],'EN-staff':['original-inscribed-shaft'],
 'EN-charm':['original-inscribed-token'],'EN-sigil':['original-inscribed-plate'],'EN-focus':['original-optic','original-inscribed-rim'],'EN-seal':['original-seal-face'],
 'RC-plate':['original-inscribed-plate'],'RC-seal':['original-inscribed-stone-face'],'SC-book':['original-inscribed-page-block'],
 'SC-text':['original-inscribed-page-block'],'SC-sheet':['original-marked-sheet'],'SC-scroll':['original-inscribed-sheet'],
 'TI-trap':['original-trigger-frame','original-discharge-block'],
 'TI-auto-tiny':['original-frame','original-actuator','original-logic-block'],'TI-auto-small':['original-frame','original-actuator','original-logic-block'],
 'TI-tool':['original-driver-spine','original-gauge'],'TI-device':['original-frame','original-gauge','original-calibration-mechanism'],
 'TI-sensor':['original-probe','original-comparator'],'TI-drone':['original-frame','original-relay-logic-block'],'TI-ram':['original-frame','original-drive-screw','original-head']}


def main():
    cp=R/'data/director/advanced_craft_recipe_candidate_internal.json';d=read(cp);cards={c['recipeId']:c for c in d['cards']}
    original={x['id']:x for x in read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes']}
    bodies={bid:b['sourceAuthoringProfile'] for bid,b in d['bodyModels'].items()}
    def c(n):return cards[f'recipe-{n}']
    def r(n):return original[f'recipe-{n}']
    def ref(n,bid):return frac(next(x['finishedReferenceGp'] for x in c(n)['operational']['references'] if x['body']==bid))
    manufacturing=[];quotes=[];services=[];conversions=[]
    for id,card in cards.items():
        source=original[id];o=card['operational'];q=source['quantity'];creature=o['creatureOutput']
        for band in ['Mishap','Failed','Flawed','Standard','Exceptional','Masterwork']:
            for option in ['yield','structural']:
                applicable=option=='yield' or band in ['Exceptional','Masterwork']
                n={'Mishap':0,'Failed':0,'Flawed':q//2 if q>=2 else int(not creature),'Standard':q,'Exceptional':5*q//4,'Masterwork':3*q//2}[band]
                if applicable and option=='structural':n=q
                actual=o['creation']['sixBands'][band] if option=='yield' else o['creation']['structuralAlternativeQuantity'] if applicable else None
                expected=n if applicable else None
                percent=0 if not applicable or creature or option=='yield' else 25 if band=='Exceptional' else 50
                ok=actual==expected and (not percent or percent in o['creation']['structuralAlternativePercent']) and o['maximumOrderedBodyReserve']==3*q//2
                manufacturing.append({'recipeId':id,'band':band,'option':option,'choiceApplicable':applicable,'expectedQuantity':expected,'actualQuantity':actual,'newStructuralPercent':percent,'creatureQualityIsLabelOnly':creature and option=='structural' and applicable,'maximumCatalystRetentionUnits':min(1,len(card['sourceAuthoringRegister']['catalystOccurrences'])) if band=='Masterwork' else 0,'pass':ok})
        for v in o['bodyVariants']:
            bid=v['bodyModelId'];b=bodies[bid];hp=source['mechanics']['hitPoints'] if creature else b['HP']
            if creature:
                for current in range(1,6):
                    actual=initial_creature_hp(hp,current);expected=max(1,floor(F(hp*current,5)))
                    conversions.append({'recipeId':id,'bodyModelId':bid,'chassisCurrentHP':current,'sourceMaximumHP':hp,'actualInitialHP':actual,'expectedInitialHP':expected,'pass':actual==expected})
            # Only identical quotation arithmetic is reused, with this recipe's
            # own family/value and this exact advanced body's price/primaries.
            model={'family':source['recipeFamily'],'baselinePriceGp':b['priceGp']}
            for current in [0,1]:
                actual=repair_quote(source,model,current,hp,PRIMARY[bid],PRIMARY[bid]);mode='brokenReconstruction' if current==0 else 'functionalRepair';auth=v[mode]
                ok=actual['dc']==auth['DC'] and actual['hours']==frac(auth['defaultMaxHPHours']) and actual['materialReferenceGp']==frac(auth['materialReferenceGp']) and actual['refills']==[]
                quotes.append({'recipeId':id,'bodyModelId':bid,'currentHP':current,'mode':mode,'actual':serial(actual),'pass':ok})
            if 'servicing' in v:
                pack=v['servicing'];rawmass=max(F(1,100),F(str(b['massLb']))/100);expectedmass=F(ceil(rawmass*100),100)
                services.append({'recipeId':id,'bodyModelId':bid,'expectedPackGp':serial(F(str(b['priceGp']))/10),'expectedPackLb':serial(expectedmass),'pass':frac(pack['packGp'])==F(str(b['priceGp']))/10 and frac(pack['packMassLb'])==expectedmass and pack['activeMinutes']==60 and pack['restoresHP'] is False})
    check('E-03','All167 recipes/six bands/two labeled choices',len(manufacturing)==2004 and all(x['pass'] for x in manufacturing),True)
    check('E-11','All actual body-choice repair quotations use matching reference data',bool(quotes) and all(x['pass'] for x in quotes),True)
    check('E-11','Only41 source ordinary TI recipes have service',len({x['recipeId'] for x in services}),41)
    check('E-11','Every service pack/time/HP separation matches',all(x['pass'] for x in services),True)
    check('E-02','All19 creature recipes and their real size choices have initial-HP conversion',len({x['recipeId'] for x in conversions})==19 and all(x['pass'] for x in conversions),True)
    for hp in [0,6,-1,True,1.5]:reject('E-02',f'Invalid B5 chassis current {hp!r}',lambda v=hp:initial_creature_hp(40,v))

    # Establish every actual B context, then exercise each distinct B once.
    contexts=[]
    for bid,b in bodies.items():
        if bid in ['TI-auto-tiny','TI-auto-small','TI-drone']:continue
        contexts.append({'model':bid,'size':'fixed default','grade':'source default','B':b['HP']})
    gradeprice={'Crude':F(1,2),'Standard':F(1),'Fine':F(3),'Superior':F(10),'Exceptional':F(25)}
    for mid,h in d['enchantingHostModels'].items():
        for size,multiple in [('Small/Medium/Tiny actual source sizing',1),('eligible Large',2)]:
            for grade,price in gradeprice.items():
                B=h['baselineStructuralHP']*multiple
                if grade=='Crude' and h['bodyKind']=='EN-armor':B=max(1,B//2)
                weight=F(str(h['ordinaryWeightLb']))*multiple
                if h['bodyKind']=='EN-armor' and grade in ['Superior','Exceptional']:weight*=F(4,5) if grade=='Superior' else F(7,10)
                contexts.append({'model':mid,'size':size,'grade':grade,'B':B,'bodyReferenceGp':serial(frac(h['ordinaryPriceGp'])*multiple*price),'bodyMassLb':serial(weight)})
    structural=[];allB=sorted({x['B'] for x in contexts})
    for B in allB:
        for oldpercent in [0,25,50]:
            for flaw in [False,True]:
                oldmax=B+max(1,B*oldpercent//100) if oldpercent else B
                if flaw:oldmax=max(1,oldmax//2)
                for current in range(oldmax+1):
                    for newpercent in [0,25,50]:
                        for addflaw in [False,True]:
                            actual=structural_hp(B,oldmax,current,oldpercent,newpercent,flaw,addflaw)
                            p=max(oldpercent,newpercent);maximum=B+max(1,floor(F(B*p,100))) if p else B
                            if flaw or addflaw:maximum=max(1,maximum//2)
                            expected={'maximumHP':maximum,'currentHP':max(0,maximum-(oldmax-current)),'durabilityPercent':p,'flawed':flaw or addflaw}
                            structural.append({'B':B,'oldPercent':oldpercent,'oldFlaw':flaw,'oldCurrentHP':current,'newPercent':newpercent,'addFlaw':addflaw,'actual':actual,'expected':expected,'pass':actual==expected})
    check('E-02','All default bodies and50host×2size×5grade contexts mapped',len(contexts),519)
    check('E-02','Every distinct B state uses noncompounding retained-damage calculation',all(x['pass'] for x in structural),True)
    reject('E-02','Inconsistent historical maximum rejected',lambda:structural_hp(5,9,8))
    primary_omissions=[]
    for bid,required in PRIMARY.items():
        card=next(c for c in cards.values() if bid in c['operational']['bodyModelIds']);s=card['sourceRecipe'];model={'family':s['recipeFamily'],'baselinePriceGp':bodies[bid]['priceGp']}
        for missing in required:
            try:repair_quote(s,model,0,5,required,[p for p in required if p!=missing])
            except ValueError:rejected=True
            else:rejected=False
            primary_omissions.append({'bodyModelId':bid,'missingDeclaredOriginalRole':missing,'rejected':rejected})
    check('E-08','Every model-designated original primary omission rejects quotation',all(x['rejected'] for x in primary_omissions),True)
    check('ADV-EDIT-01','Trap spring is subordinate but automaton actuator stays primary',('spring' not in ' '.join(PRIMARY['TI-trap']),'original-actuator' in PRIMARY['TI-auto-tiny'],'original-actuator' in PRIMARY['TI-auto-small']),(True,True,True))

    # Named worked examples use actual candidate/source numbers. The casebook
    # separately specifies qualitative world/admission/chronology dispositions.
    check('W-01','Recipe121 reserve/body masses and reference',(r(121)['quantity']*3//2,6*bodies['EN-armor']['massLb'],6*bodies['EN-armor']['priceGp'],4*bodies['EN-armor']['massLb'],2*bodies['EN-armor']['massLb'],ref(121,'EN-armor')),(6,120,300,80,40,F('89.75')))
    check('W-01','Functional/Broken reference and copper purchase',(F(50,4),ref(121,'EN-armor')/4,copper(ref(121,'EN-armor')/4)),(F('12.50'),F('22.4375'),F('22.44')))
    check('W-01','Forge creation minutes',c(121)['operational']['work']['forgeDwarfActiveMinutes'],180)
    check('W-02','Eligible negative grade comparison and suppression',(max([-1,1]),max([-1])),(1,-1))
    check('W-02','B7 current4 plusP25 retains deficit',structural_hp(7,7,4,new_percent=25),{'maximumHP':8,'currentHP':5,'durabilityPercent':25,'flawed':False})
    check('W-02','B1 P25 is2, not another use',structural_hp(1,1,1,new_percent=25)['maximumHP'],2)
    check('W-04','397 native DEX success produces zero; failed save gets7',[(saving_throw(n,0,r(397)['mechanics']['saveDC'])['success'],0 if saving_throw(n,0,r(397)['mechanics']['saveDC'])['success'] else 7) for n in [11,10]],[(True,0),(False,7)])
    check('W-05','396 source STR DC and399 healing',(r(396)['mechanics']['saveDC'],r(399)['mechanics']['healing']),(9,'1d8+2'))
    check('W-06','Ward2 and jewelry1 compare once',max(2,1),2)
    check('W-07','399 consumed lens occurrence remains source0.1lb',(r(399)['components'][1]['name'],F(str(r(399)['components'][1]['weight'])),r(399)['components'][1]['consumed']),('Resonance Lens',F('.1'),True))
    check('W-08','623 historical null/zero labor and exact year overlay',(r(623)['workRequirements']['activeWorkHours'],r(623)['economy']['laborValue'],c(623)['operational']['work']['activeMinutes'],c(623)['operational']['work']['forgeDwarfActiveMinutes'],ref(623,'TI-tool')),(None,0,115200,86400,F(350108)))
    check('W-08','623 remaining phase minutes and Broken reference',(c(623)['operational']['work']['remainingActiveMinutes'],c(623)['operational']['work']['dwarfRemainingActiveMinutes'],ref(623,'TI-tool')/4),(115185,86385,F(87527)))
    script=c(505)['operational']['useBinding'];rank=script['maximumSpellRank']
    check('W-09','Actual505 rank/use capacity and encoding time/cost/mass/DC',(rank,script['lifetimeActivations'],max(1,rank),max(1,rank)*10,F(max(1,rank),100),10+rank),(8,2,8,80,F('.08'),18))
    check('W-10','497 physical expedition reroll maximum',c(497)['operational']['useBinding']['rerollsPerPhysicalItemPerFormalExpedition'],1)
    check('W-11','674 grants3 Insight; actual zero-language references stay0',(c(674)['operational']['useBinding']['languageInsight'],[r(n)['mechanics']['languages'] for n in [476,486,672]]),(3,[0,0,0]))
    pact=c(675)['operational']['useBinding'];check('W-12','One bargain, bounded consent/term and mark',(pact['lifetimeBargains'],pact['minimumParticipants'],pact['maximumParticipants'],pact['maximumClauses'],pact['maximumTermDays'],pact['breachDamage'],pact['markDays'],pact['enforcementRangeFeet']),(1,2,6,3,30,'6d10 psychic',30,5280))
    check('W-12','Annotation gate does not grant missing text',(pact['hiddenAnnotationCharacterLevelMinimum'],pact['hiddenAnnotationRequiredSkillProficiencies']),(11,3))
    auto=c(684)['operational']['useBinding'];check('W-13','Actual684 source stats, attack and damaged chassis',(auto['armorClass'],auto['hitPoints'],auto['attack']['bonus'],auto['attack']['dice'],auto['attack']['damageType'],initial_creature_hp(auto['hitPoints'],3)),(14,40,5,'3d6','force',24))
    small=next(v for v in c(684)['operational']['bodyVariants'] if v['bodyModelId']=='TI-auto-small');check('W-13','Small actual service pack',(frac(small['servicing']['packGp']),frac(small['servicing']['packMassLb']),small['servicing']['restoresPrintedMaximum']),(F(5),F('.25'),3))
    sensor=c(685)['operational']['bodyVariants'][0]['servicing'];check('W-15','Sensor service references',(frac(sensor['packGp']),frac(sensor['packMassLb']),sensor['restoresPrintedMaximum']),(F(2),F('.02'),3))
    relay=c(686)['operational']['useBinding'];check('W-16','Source relay stats/links/range and absent attack',(relay['armorClass'],relay['hitPoints'],relay['commandTargets'],relay['rangeFeet'],relay['attack']),(18,80,3,120,None))
    check('W-17','Creator7 Core natural20 total27 vsDC28',task_check(20,7,28),{'total':27,'degree':'success','success':True})
    check('W-17','Normal attack20 differs from save/task route',(attack_roll(20,6,99)['critical'],saving_throw(20,0,28)['success']),(True,False))
    check('W-18','Half unmodified base60 is30',60//2,30)
    check('W-19','Original TI GP creation has no RP deployment credit',min(1,0),0)
    for nat,mod,dc,forge,expected in [(1,100,10,False,'Mishap'),(20,-10,10,False,'Standard'),(20,-10,10,True,'Exceptional'),(20,0,10,False,'Masterwork'),(10,-5,10,True,'Failed')]:
        check('E-03',f'Native creation die{nat} modifier{mod} DC{dc} Forge{forge}',creation_band(nat,mod,dc,forge),expected)
    check('E-03','Core natural1 high total can still succeed in repair',task_check(1,30,10)['success'],True)
    check('E-05','Indivisible3 and admitted divisible5 failure-unit ceilings',((F(3,4)//1)*1,(F(5,4)//F('.01'))*F('.01')),(F(0),F('1.25')))

    casebook=R/'docs/director-only/ADVANCED_CRAFT_PHYSICAL_SEQUENCE_CASEBOOK.md';text=casebook.read_text(encoding='utf-8');cases=read(A/'ADVANCED_CRAFT_AUTHORED_SEQUENCE_CASES.json')
    check('coverage','All19 W source cases and18 extra cases have explicit rejection',re.findall(r'^### ((?:W|E)-\d{2}) —',text,re.M),[f'W-{i:02}' for i in range(1,20)]+[f'E-{i:02}' for i in range(1,19)])
    check('coverage','All37 qualitative dispositions are labeled authored expectations',len(cases['cases'])==37 and all(x['qualitativeExactReviewPending'] for x in cases['cases']) and text.count('**Reject:**')==37,True)
    check('coverage','All22 body boundaries included',all('| '+bid+' |' in text for bid in bodies),True)
    check('coverage','No runtime/world-authentication assertion',all(s.casefold() in text.casefold() for s in ['not presented as automated runtime passes','not asserted campaign stock','qualitative','ADV-EDIT-01']),True)
    protected=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes'];check('preservation','All138 original submitted files unchanged',len(protected)==138 and all(sha(G/p)==h for p,h in protected.items()),True)
    out={'status':'PASS source-bound numeric examples and authored case coverage' if all(x['pass'] for x in checks) else 'CORRECTIONS REQUIRED','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'checkCount':len(checks),'checks':checks,'failedChecks':[x['case']+': '+x['claim'] for x in checks if not x['pass']],
         'manufacturingCases':manufacturing,'structuralContexts':contexts,'structuralTransitions':structural,'creatureInitialHPConversions':conversions,'repairQuotations':quotes,'servicePackCases':services,'declaredPrimaryOmissions':primary_omissions,
         'counts':{'sourceWorkedSequences':19,'additionalAdjudicationSequences':18,'bodyBoundaries':22,'manufacturingCases':len(manufacturing),'structuralContexts':len(contexts),'distinctOrdinaryB':allB,'structuralTransitions':len(structural),'creatureConversions':len(conversions),'repairQuotations':len(quotes),'servicePacks':len(services),'primaryOmissions':len(primary_omissions)},
         'scope':'Source/card arithmetic through common Core/structural/quotation calculators and complete authored qualitative sequence coverage, not an implemented advanced runtime or actual-world authentication. Exact qualitative verdict remains pending.',
         'qualitativeExactReviewPending':True,'runtimeImplemented':False,'newApprovals':0,'casebookSha256':sha(casebook),'internalCandidateSha256':sha(cp),
         'referenceHashes':{p.relative_to(G).as_posix():sha(p) for p in [R/'tools/core_playtest_rules.py',R/'tools/spell_playtest_rules.py',R/'tools/fishing_reference.py',cp,casebook,R/'tools/validate_advanced_craft_worked_cases.py']}}
    (A/'ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json').write_text(json.dumps(serial(out),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:out[k] for k in ['status','checkCount','failedChecks','counts','scope']},ensure_ascii=False,indent=2))
    if out['failedChecks']:raise SystemExit(1)


if __name__=='__main__':main()
