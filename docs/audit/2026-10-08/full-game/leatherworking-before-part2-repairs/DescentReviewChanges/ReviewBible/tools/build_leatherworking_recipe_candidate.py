"""Author the Leatherworking candidate under the captured LW-D01..09 conference.

Never edits source recipes/equipment or marks the new cards reviewed.
"""
from pathlib import Path
from fractions import Fraction
from copy import deepcopy
import json, hashlib, math

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
STATUS = 'authored-draft-awaiting-exact-review'
THREAD = '6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b'
TURN = '86413ad7-8096-4e6f-baca-3cab34aa66a3'
REPLY = '4f808c26-f93b-4b50-ac05-a917b7ca2b7e'
AC_IDS = {306:1,308:1,309:1,312:1,314:1,315:1,317:2,318:2,319:2,653:1,655:1}
FAMILY_IDS = {'Backpack':[280,286,287,293,297,303,652], 'Pouch':[281,285,290,295,302,311],
 'Quiver':[283,292,305,313], 'Belt':[291,300,304,307,310,316], 'Harness':[654],
 'Boots':[282,308,309,312,314,318,653], 'Gloves':[284,294,298,299,306],
 'Leather Gear':[288,296,315,317], 'Armor':[289,301,319], 'Coat':[655]}
SLOTS = {'Backpack':'back-cargo','Harness':'back-cargo','Quiver':'quiver',
 'Belt':'waist-cargo','Pouch':'pouch-position','Boots':'footwear-pair',
 'Gloves':'handwear-pair','Leather Gear':'torso-accessory','Coat':'outerwear-benefit','Armor':'armor-suit'}
TASKS = {
 'Boots': 'STR (Athletics) for actual foothold climbing or a jump that requires a check; DEX (Acrobatics) to balance on narrow, unstable or slippery support using the feet.',
 'Gloves': 'STR (Athletics) for climbing with actual handholds or rope grip; STR (Athletics) or DEX to retain, lower or position noncreature cargo by hand; DEX for ordinary nonlocking ties, straps, clasps or a jammed small object.',
 'Leather Gear': 'STR (Athletics) for actual climbing; DEX (Acrobatics) for controlled movement through a cramped or obstructed passage when a check is actually required.',
 'Armor': 'STR (Athletics) for actual climbing; DEX (Acrobatics) for controlled movement through a cramped or obstructed passage when a check is actually required.',
 'Coat': 'STR (Athletics) for actual climbing; DEX (Acrobatics) for controlled movement through a cramped or obstructed passage when a check is actually required. This is not a temperature-endurance bonus.',
 'container': 'Actual difficult cargo handling to secure its ordinary closure/retainers or retrieve through an unlocked closure, jam, tangle or other physical difficulty: DEX for dexterous work or STR (Athletics) for forceful handling of noncreature cargo.'}

SHARED = {
 'id':'leatherworking.shared.v1','status':STATUS,
 'classification':{'magical':True,'artifact':False,'attunementRequired':False,'resourceCost':0,'concentration':False,'spellActivationRequired':False},
 'sourceAuthority':{'threadId':THREAD,'turnId':TURN,'replyId':REPLY,'scope':'source/interface direction only; no exact card approval'},
 'defense':{'family':'equipment.defense-enhancement','combination':'strongest actual eligible suit-grade, Blacksmithing or Leatherworking modifier','zeroRecipeMeansNoCandidate':True,'ordinarySelectedShieldOutsideFamily':True,'armorRequiresSelectedWornFormula':True,'functionalMinimumHP':1,'resistanceRequiresSelectedFormula':False,'resistanceProtects':'wearer only','requiresCompleteWornUnsuppressedUnmeldedItem':True,'duplicateResistanceGrantsImmunity':False},
 'task':{'family':'equipment.leather-task-enhancement','combination':'strongest qualifying Leatherworking wearable/container once per actual check','proficiencyOnce':True,'containerOperatorMayBeAllyOrThief':True,'containerHandlingRequiresReliefSlot':False,'containerHandlingRequiresAccessibleUnsuppressedFunctionalFittings':True,'routineHandlingInventsCheck':False,'savesAttacksStealthOrPerceptionBonus':False},
 'relief':{'sourceField':'mechanics.capacityPounds','physicalMassChanges':False,'canonicalLoadChanges':False,'ordinaryPoundCarryComparisonChanges':True,'inventoryLoadCreditPerRecord':'min(canonicalLoad, coveredPounds/10)','allocation':'stable recorded loading order; inner body then descendants','selfBodyEligible':False,'partialAccountingCoverage':True,'knownWeightRequired':True,'creaturesCasualtiesBodiesEligible':False,'ordinaryInnerContainersEligible':True,'nestedMagicContainerActive':False,'externalAttachmentEligible':False,'fiveSlots':{'back-cargo':1,'quiver':1,'waist-cargo':1,'pouch-position':2},'directWornOrHeldRequired':True,'anatomySpaceFitAndHandsRequired':True,'donDoffRefitActions':1,'transferResetsAnything':False,'supportsAndRescuersUseFullMass':True,'strengthPushDragLiftCasualtyCapacityChanges':False},
 'physical':{'containersFixedAcrossSize':True,'accessoryLargePriceWeightHPMultiplier':2,'armorUsesReviewedSizeGradeRules':True,'accessoryContainerGrade':'Standard only','pairsOneIdentityBothMembersRequired':True,'glovesShareBlacksmithGauntletSlot':True,'nonArmorDonDoffActions':1,'defaultStructuralAC':15,'brokenHP':0,'brokenRemovesContainment':True,'suppressionRemovesContainment':False,'brokenRetainsBodyAndMass':True,'noAutomaticSpillDamage':True,'repairReloadsContents':False},
 'meld':{'preflightBeforeVoluntaryPayment':True,'useFullPoundsAndCanonicalLoad':True,'ceilingsRemainFixedPreTransformation':True,'loadedContainerMovesAsSubtree':True,'mandatoryOverflowFallback':'stable physical-item-ID order','returnUsesExternalEquipmentPriority':True,'reliefRequiresActualReturnedLegalWornHeldSlot':True},
 'baseReservation':{'completeNonmagicalBodyPerOutput':True,'maximum':'floor(1.5*Q)','containersEmpty':True,'oneModelSizeGradePerBatch':True,'orderedBeforeWork':True,'functionalDamagedEligible':True,'brokenOrImprintedEligible':False,'missingBrokenCommittedElsewherePausesBeforeRoll':True,'replacementKeepsPosition':True,'postRollSelection':False,'transformFirstResolvedN':True,'latestCompletionHPControls':True,'unusedBodiesSeparateFromIngredientRecovery':True,'finishedMass':'actual base body mass; no second body from component mass'},
 'durability':{'ordinaryB':'ordinary body HP after actual size and applicable grade','positivePercent':'strongest of 0,25,50','improvedMax':'B + (max(1,floor(B*P/100)) if P>0 else 0)','flaw':'one persistent floor(ImprovedMax/2), minimum1, applied last','newCurrent':'max(0,FinalMax-(OldMax-OldCurrent)), capped at FinalMax','potencyCapacityGradeChanges':False,'repairRemovesFlawOrCompoundsImprovement':False},
 'work':{'abilityOptions':['Dexterity'],'primaryProficiency':"Leatherworker's tools",'station':'Tannery Bench','requiredTools':["Leatherworker's tools",'Awl','Cutting knife'],'allFieldCraftable':False,'firstStablePhase':'min(8 hours, actual adjusted active time)','onlyActuallyIncorporatedComponentsStabilize':True,'forgeDwarfCreationMultiplier':0.75,'roundUpToWholeMinute':True,'forgeDwarfStandardOutputBecomesExceptional':True,'sourceTrivialityThresholdControls':True},
 'quality':{'Standard':'Q','ExceptionalYield':'floor(1.25*Q)','MasterworkYield':'floor(1.5*Q)','DurabilityQuantity':'Q','Flawed':'floor(Q/2) ordinary effects if Q>=2, otherwise1 with persistent flaw','FailedMishap':0,'eligibleCatalystReturns':0,'declaredAfterRollOncePerBatch':True},
 'repair':{'actualLeatherworkerProficiencyRequired':True,'ability':'Dexterity','station':'Tannery Bench','tools':["Leatherworker's tools",'Awl','Cutting knife'],'positiveHP':{'DC':10,'hours':'max(1,maxHP/10)','materials':'25% mundane size/grade base reference'},'zeroHP':{'DC':'original recipe DC','hours':'max(8,maxHP/10)','materials':'25% undamaged finished unit reference','recoverableOriginalMainBodyRequired':True,'bothOriginalPairMembersRequired':True},'binary':True,'successRestoresRecordedMaximum':True,'failureConsumesMaterialsAndWork':True,'formulaOrOriginalTradeLevelRequired':False,'teachesFormula':False,'qualityXPReturnOrForgeDwarfReduction':False},
 'valuation':{'sourceUnit':'Standard batch reference / Q','finishedUnit':'sourceUnit + actual undamaged mundane base reference','keepExactPrecisionUntilTransaction':True,'ownedBodiesRepurchased':False,'automaticArtifactOrQualityMultiplier':False,'finiteActualBuyerAndQuoteRequired':True},
 'runtimeImplemented':False,'balanceApproved':False,'cosmologyReviewed':False}

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,t): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,d): write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def ratio(x):
    x=Fraction(str(x)); return {'numerator':x.numerator,'denominator':x.denominator}
def unr(x): return Fraction(x['numerator'],x['denominator'])
def fmt(x):
    x=Fraction(x)
    return str(x.numerator) if x.denominator==1 else str(float(x)) if x.denominator in (2,4,5,10,20,25,50,100) else str(x)
def public_projection(x):
    omitted=object()
    def visit(v):
        if isinstance(v,dict):
            if v.get('visibility') in ('restricted','director-only','director-internal'): return omitted
            result={}
            for k,z in v.items():
                if k in ('directorGuidance','directorNotes','secret','secrets'): continue
                clean=visit(z)
                if clean is not omitted: result[k]=clean
            return result
        if isinstance(v,list):
            clean=[visit(z) for z in v]
            return [z for z in clean if z is not omitted]
        return deepcopy(v)
    result=visit(x)
    return None if result is omitted else result

def make_models(equipment):
    by={z['name']:z for z in equipment}; out={}
    def add(key,name,family,price,weight,hp,source=None,**extra):
        out[key]={'id':key,'name':name,'family':family,'baselinePriceGp':price,'baselineWeightLb':weight,'ordinaryMaximumStructuralHP':hp,'structuralAC':15,'dominantMaterial':'leather or leather-and-wood load-bearing body','gradePolicy':'reviewed armor-suit grades' if family=='Armor' else 'Standard only','largeSizingEligible':family not in ('Backpack','Pouch','Quiver','Belt','Harness'),'largePriceWeightHPMultiplier':2 if family in ('Armor','Boots','Gloves','Leather Gear','Coat') else 1,'benefitSlot':SLOTS[family],'sourceEquipmentRecord':deepcopy(source),'provenance':'preserved source equipment plus LW-D02/LW-D06 completions' if source else 'NEW mundane body under LW-D02/LW-D06','outputUnit':'one matched pair' if family in ('Boots','Gloves') else 'one item',**extra}
    def cargo(key,name,fam,n,price,weight,cap,vol,hp,interior,mouth,exterior,compartments=1,compcap=None,compvol=None):
        add(key,name,fam,price,weight,hp,by['Backpack'] if fam=='Backpack' else None,
            physicalContentWeightLimitLb=cap,physicalContentVolumeFt3=ratio(vol),compartmentCount=compartments,
            compartmentWeightLimitLb=compcap if compcap is not None else cap,
            compartmentVolumeFt3=ratio(compvol if compvol is not None else vol),
            interiorInches=interior,openingInches=mouth,exteriorInches=exterior,
            openingAxes=[0,2] if fam in ('Pouch','Belt') else [0,1] if fam=='Harness' else [1,2],
            exteriorIsPerPocket=fam=='Belt',n=n,closure='open retaining cradle; compatible inner container required for loose small cargo or fluid' if fam=='Harness' else 'ordinary flaps and ties; no lock, seal or preservation',
            ordinaryArmorFormula=None,donActions=1,doffActions=1)
    cargo('leather.backpack','Backpack','Backpack',None,2,5,30,1,10,[18,12,8],[12,8],[20,14,10])
    for n in (1,2,3): cargo(f'leather.pouch-{n}','Cargo pouch '+str(10*n)+' lb','Pouch',n,n,n+1,10*n,Fraction(n,3),5,[12,8,6*n],[12,6*n],[13,9,6*n+1])
    for n in (1,3,4): cargo(f'leather.quiver-{n}','Cargo quiver '+str(10*n)+' lb','Quiver',n,2*n,2*n,10*n,Fraction(n,3),5,[36,4,4],[4,4],[38,6*n,6],n,10,Fraction(1,3))
    for n in (1,2,3,5): cargo(f'leather.belt-{n}','Cargo belt '+str(10*n)+' lb','Belt',n,2*n,2*n,10*n,Fraction(n,3),5,[12,8,6],[12,6],[13,9,7],n,10,Fraction(1,3))
    cargo('leather.harness','Cargo harness','Harness',None,10,10,50,Fraction(5,3),10,[30,12,8],[30,12],[32,14,10])
    for name,hp in [('Leather',10),('Studded leather',10),('Hide',15)]:
        z=by[name];add(z['id'],name,'Armor',z['unitPriceCp']/100,z['unitWeightLb'],hp,z,
            ordinaryArmorFormula=z['sourceFields']['Armor Class (AC)'],armorCategory=z['group'],armorProficiencyRequired=True,strengthMinimum=None,stealthDisadvantage=False,donMinutes=5 if name=='Hide' else 1,doffMinutes=1)
    for fam,name,price,weight in [('Boots','Boots pair',2,2),('Gloves','Gloves pair',1,0.5),('Leather Gear','Leather mobility vest',5,4),('Coat','Lined leather/hide coat',10,6)]:
        add('leather.'+fam.lower().replace(' ','-'),name,fam,price,weight,5,
            ordinaryArmorFormula=None,armorProficiencyRequired=False,strengthMinimum=None,stealthDisadvantage=False,donActions=1,doffActions=1,grantsFreeHandsOrWeaponDamage=False)
    assert len(out)==19
    return out

def model_ids(r):
    f=r['recipeFamily'];m=r['mechanics']
    if f=='Armor': return ['armor-and-shields.leather','armor-and-shields.studded-leather','armor-and-shields.hide']
    if f in ('Pouch','Quiver','Belt'): return [f'leather.{f.lower()}-{m["capacityPounds"]//10}']
    return ['leather.'+f.lower().replace(' ','-')]

def operational(r,models):
    m=r['mechanics'];q=r['quantity'];f=r['recipeFamily'];ids=model_ids(r);is_container=m['type']=='container'
    hours=r['workRequirements']['activeWorkHours'];effective=1920 if hours is None else hours
    minutes=math.ceil(Fraction(str(effective))*45);unit=Fraction(str(r['economy']['recommendedMarketValue']))/q
    prefix='One output transforms one complete '+('matched pair' if f in ('Boots','Gloves') else 'mundane body')+', retaining its physical identity and latest lawful completion damage state. Functional means at least 1 current structural HP; the singleton Flawed result can emerge Broken with a dormant imprint. '
    effect={'type':m['type'],'taskBonus':m['bonus'] if is_container else m['skillBonus'],'taskFamily':'equipment.leather-task-enhancement','taskScope':TASKS['container' if is_container else f],'armorBonus':m.get('armorBonus',0),'armorBonusCandidate':m.get('armorBonus') or None,'resistance':m.get('resistance'),'requiresSelectedArmorFormulaForAC':f=='Armor','resistanceRequiresSelectedArmorFormula':False}
    text=prefix
    if is_container:
        b=models[ids[0]]
        effect.update(reliefAllowanceLb=m['capacityPounds'],reliefSlot=SLOTS[f])
        text+=f"While functional, unsuppressed, unmelded, properly fitted and worn or directly held in its recorded {SLOTS[f]} relief position, cover up to {m['capacityPounds']} lb of eligible contents in stable loading order. Physical capacity remains {b['physicalContentWeightLimitLb']} lb and {fmt(unr(b['physicalContentVolumeFt3']))} ft³, subject to its actual opening, shape and compartment limits. Its own body is not relieved. For each covered record, subtract covered pounds from the direct bearer's pound-carrying comparison and at most min(canonical Load, covered pounds/10) from Inventory Load; preserve actual mass and canonical Load. Enclosed enchanted containers are inactive; ordinary inner bodies and descendants count once. External lashings do not become contents. "
        text+=f"The actual operator receives +{m['bonus']} on a qualifying handling check: {effect['taskScope']} This handling benefit needs accessible functional unsuppressed fittings, not a relief slot, and can apply on a table or for an ally. "
    else:
        text+=f"While complete, functional, unsuppressed, unmelded and actually worn in its {SLOTS[f]} benefit slot, receive +{m['skillBonus']} only on these actual checks: {effect['taskScope']} "
        if m['armorBonus']:
            text+=f"NEW LW-D01 overlay from mechanics.armorBonus: offer +{m['armorBonus']} to equipment.defense-enhancement; this AC benefit is omitted by the preserved prose. "+('The suit must supply the worn-armor formula being used. ' if f=='Armor' else 'The complete accessory must occupy its one legal benefit slot. ')+"Use the strongest actual eligible Leatherworking, Blacksmithing or suit-grade modifier; ordinary selected shield AC remains separate. "
        else: text+='The source armorBonus of 0 creates no recipe AC candidate and does not cancel a Crude suit penalty. '
        if m['resistance']: text+=f"Separately grant the wearer resistance to {m['resistance']} damage while complete, functional, unsuppressed and actually worn, regardless of the winning enhancement or selected suit formula; no protection automatically extends to the item or contents. "
        else: text+='No damage resistance or environmental immunity is granted. '
    text+='Only the strongest qualifying Leatherworking task bonus applies once per actual check. No routine check is invented; ordinary actions, hands, access, proficiency and competing slot requirements still apply. Broken stops positive functions; suppression stops recipe magic, not physical capacity or workmanship. Use the complete shared guide for custody, melding, quality, repair and value.'
    return {'sharedProfileId':SHARED['id'],'text':text,'effect':effect,'baseModelIds':ids,'sourceEffectPreservedSeparately':True,'sourceArmorOmissionDisposition':'LW-D01 numerical-field overlay' if m.get('armorBonus',0)>0 else None,'standardQuantity':q,'maximumBaseReserve':3*q//2,
        'outcomes':{'Standard':q,'ExceptionalYield':5*q//4,'MasterworkYield':3*q//2,'DurabilityOptionQuantity':q,'FlawedQuantity':q//2 if q>=2 else 1,'SingletonFlawedAddsPersistentFlaw':q==1,'Failed':0,'Mishap':0,'eligibleCatalystReturns':0},
        'work':{'sourceActiveWorkHours':hours,'operationalActiveWorkHours':effective,'nullHourOverlay':hours is None,'ordinaryFirstStablePhaseHours':min(8,effective),'eligibleForgeDwarfActiveMinutes':minutes,'eligibleForgeDwarfFirstPhaseMinutes':min(480,minutes),'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel'],'maximumAssistants':r['workRequirements']['maximumAssistants'],'craftingDC':r['craftingCheck']['targetDC']},
        'value':{'sourceStandardBatchReferenceGp':r['economy']['recommendedMarketValue'],'sourceProcessUnitReferenceGp':ratio(unit),'actualBaseReferenceAdded':True},
        'standardModelExamples':[{'baseModelId':id,'finishedUnitReferenceGp':ratio(unit+Fraction(str(models[id]['baselinePriceGp'])))} for id in ids]}

def models_table(models):
    lines=['| Mundane body | Price gp | Empty lb | Ordinary HP / structural AC | Benefit slot | Ordinary use |','|---|---:|---:|---|---|---|']
    for b in models.values():
        use=(str(b['physicalContentWeightLimitLb'])+' lb / '+fmt(unr(b['physicalContentVolumeFt3']))+' ft³ contents') if 'physicalContentWeightLimitLb' in b else b['ordinaryArmorFormula'] or b['outputUnit']
        lines.append(f"| {b['name']} | {b['baselinePriceGp']:g} | {b['baselineWeightLb']:g} | {b['ordinaryMaximumStructuralHP']} / {b['structuralAC']} | {b['benefitSlot']} | {use} |")
    lines+=['','| Container | Compartments | Interior per compartment, inches | Opening, inches | Exterior, inches | Each compartment limit |','|---|---:|---|---|---|---|']
    for b in models.values():
        if 'compartmentCount' not in b: continue
        dims=lambda xs:' × '.join(str(x) for x in xs)
        lines.append(f"| {b['name']} | {b['compartmentCount']} | {dims(b['interiorInches'])} | {dims(b['openingInches'])} | {dims(b['exteriorInches'])}"+(' per pocket' if b['exteriorIsPerPocket'] else '')+f" | {b['compartmentWeightLimitLb']} lb / {fmt(unr(b['compartmentVolumeFt3']))} ft³ |")
    return '\n'.join(lines)

def card_md(c,models,internal):
    r=c['sourceRecipe'];o=c['operational'];w=r['workRequirements'];q=r['quantity'];ids=o['baseModelIds'];m=r['mechanics'];h=o['work']
    lines=[f"## {r['id']} — {r['name']}",'',f"**DRAFT; exact review pending.** {r['visibility']}; Leatherworking level {r['skillLevel']}; tier {r['tier']}; {r['rarity']}; DC {r['craftingCheck']['targetDC']}. Standard quantity {q}; source Standard batch reference {r['economy']['recommendedMarketValue']} gp.",'','**Preserved effect:** '+r['effects'],'','**Operational effect:** '+o['text'],'', '**Legal mundane bases:** '+', '.join(models[id]['name'] for id in ids)+'. One model, actual fit and legal grade for the whole batch. Buy, own or legitimately commission complete bodies; no stock-construction recipe is implied.','',f"**Physical reserve:** {o['maximumBaseReserve']} complete, nonmagical, non-Broken bases in a stable physical-ID order before work; containers empty. No existing imprint. Missing/Broken/committed bases pause before the roll; repair or replace at the same position. Transform the first resolved N, using latest lawful completion HP. Keep unused bodies in their actual state outside ingredient recovery.",'',models_table({id:models[id] for id in ids}),'', '**Exact source component occurrences:**','','| # | Component | Quantity | Tier | Role / consumed | Unit lb | Unit gp | Required properties |','|---|---|---:|---:|---|---:|---:|---|']
    for i,z in enumerate(r['components']):lines.append(f"| {i} | {z['name']} | {z['quantity']} | {z['tier']} | {z['role']} / {str(z['consumed']).lower()} | {z['weight']:g} | {z['value']} | {', '.join(z['properties'])} |")
    lines+=['','All listed inputs are additional consumed process/reinforcement materials. Finished empty mass is the actual body mass; process waste supplies no second body or automatically valuable salvage. No source component is a catalyst; even Masterwork returns zero catalyst units. Independently required tools remain tools.','',f"**Work and access:** DEX with actual Leatherworker's-tools proficiency as the shared framework permits; {w['station']}; {', '.join(w['requiredTools'])}. Maximum assistants {w['maximumAssistants']}. Source fieldCraftable={str(w['fieldCraftable']).lower()}; preserved timeMode={w['timeMode']}; the false field flag controls. Source time: {r['craftingTime']}; source activeWorkHours={json.dumps(w['activeWorkHours'])}. Operational required active time {h['operationalActiveWorkHours']} hours"+(' under the explicitly new 1,920-hour one-year overlay; source null and labor value stay unchanged' if h['nullHourOverlay'] else '')+f". First stable phase {h['ordinaryFirstStablePhaseHours']} hours, included in total. Eligible Forge Dwarf: {h['eligibleForgeDwarfActiveMinutes']} minutes, first phase {h['eligibleForgeDwarfFirstPhaseMinutes']} minutes. Stabilize only components actually incorporated in the completed first phase; other lots keep their clocks.",'',f"**Progression:** exact source trivialAtSkillLevel={h['trivialAtSkillLevel']}; use this threshold rather than regenerating level+5. Actual formula access: "+json.dumps(r['discovery'],ensure_ascii=False,separators=(',',':'))+'. The framework controls trade eligibility, proficiency once, assistant qualifications, Watches, rest, interruptions, XP and mishaps.','',f"**Output:** Standard {q}; Exceptional yield {o['outcomes']['ExceptionalYield']}; Masterwork yield {o['outcomes']['MasterworkYield']}; or {q} units with strongest noncompounding structural improvement 25%/50%. Flawed: "+(f"{q//2} ordinary-effect units, preserving existing physical durability state." if q>=2 else 'one persistent half-maximum flaw applied after size/grade and strongest improvement, minimum1; preserve damage deficit and possible Broken output.')+' Failed/Mishap transforms none; source input recovery/loss remains separate. Quality changes no capacity, relief, check bonus, AC, resistance or grade.','',f"**Repair:** trained Leatherworker's tools, Tannery Bench, Awl and Cutting knife. Functional HP≥1: DEX + applicable proficiency DC10; max(1 hour, recorded max HP/10); materials 25% mundane base reference. Broken HP0: DEX + applicable proficiency DC{r['craftingCheck']['targetDC']}; max(8 hours, recorded max HP/10); materials 25% finished per-item reference; recoverable original main body required"+(' with both original pair members' if r['recipeFamily'] in ('Boots','Gloves') else '')+'. Binary success restores recorded maximum, including the persistent flaw; failure consumes materials and time. No formula or original trade-level eligibility required or granted, quality roll, XP, catalyst return or Forge Dwarf creation reduction. No lost contents return.','', '**Finished ordinary Standard reference examples:** '+ '; '.join(models[e['baseModelId']]['name']+' = '+fmt(unr(e['finishedUnitReferenceGp']))+' gp' for e in o['standardModelExamples'])+'. Source process share '+fmt(unr(o['value']['sourceProcessUnitReferenceGp']))+' gp/unit plus actual undamaged mundane size/grade body reference. Retain exact precision until the actual transaction; no automatic buyer, quality premium, artifact multiplier or mundane-table magic buyback.','', '**Preserved tags:** '+', '.join(r['tags'])+'. Tags, current/legacy names, donors and whole-creature metadata add no powers or availability.','']
    if c.get('publicBookBinding'):lines+=['**Public source binding:** V5 '+', '.join('¶'+str(x['index']) for x in c['publicBookBinding']['paragraphs'])+'. The original effect remains verbatim; any AC overlay above is separate.','']
    legacy={k:r[k] for k in ('legacyName','legacyEffect','wholeCreatureUse') if k in r}
    if legacy:lines+=['**Preserved inactive legacy/metadata:** '+json.dumps(legacy,ensure_ascii=False)+'.','']
    if internal and 'directorGuidance' in r:lines+=['**Preserved optional Director guidance:** '+json.dumps(r['directorGuidance'],ensure_ascii=False)+'. No automatic extra prerequisite.','']
    return '\n'.join(lines)

def main():
    assert not (ROOT/'docs/mechanics/LEATHERWORKING_REVIEW_STATUS.json').exists(), 'Already reviewed; do not overwrite.'
    source_path=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    source=read(source_path);evidence=read(AUDIT/'LEATHERWORKING_SOURCE_PREPARATION.json')
    rs=[r for r in source['recipes'] if r['skill']=='Leatherworking'];assert rs==evidence['recipes'] and len(rs)==44
    baseline=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')
    assert all(sha(GAME/p)==h for p,h in baseline['files'].items())
    models=make_models(read(ROOT/'data/playtest/equipment_acquisition_candidate.json')['items'])
    bindings={x['recipeId']:x for x in evidence['publicBookBindings']};cards=[]
    for r in rs:cards.append({'recipeId':r['id'],'name':r['name'],'visibility':r['visibility'],'status':STATUS,'sourceRecipeIndex':evidence['sourceIndices'][r['id']],'sourceRecipe':deepcopy(r),'publicBookBinding':deepcopy(bindings.get(r['id'])),'operational':operational(r,models)})
    public=[public_projection(c) for c in cards if c['visibility']=='public'];assert len(public)==30
    pids={id for c in public for id in c['operational']['baseModelIds']};pmodels={k:v for k,v in models.items() if k in pids}
    envelope={'schemaVersion':1,'status':STATUS,'sourceSha256':sha(source_path),'sourceConferenceThreadId':THREAD,'sourceConferenceTurnId':TURN,'sourceConferenceReplyId':REPLY,'sharedOperationalProfile':SHARED,'runtimeImplemented':False,'balanceApproved':False,'exactRecipeApproval':False,'cosmology':'post-push only'}
    template=(ROOT/'tools/templates/leatherworking_rules.md').read_text(encoding='utf-8')
    for internal,chosen,bs,jsonpath,guidepath,mdpath in [
      (True,cards,models,'data/director/leatherworking_recipe_candidate_internal.json','docs/director-only/LEATHERWORKING_INTERNAL_GUIDE.md','docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md'),
      (False,public,pmodels,'data/playtest/leatherworking_recipe_candidate.json','docs/mechanics/LEATHERWORKING_RECIPE_PLAYTEST.md','docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md')]:
        dump(ROOT/jsonpath,{**envelope,'visibility':'director-internal' if internal else 'public','sharedGuide':guidepath,'baseModels':bs,'cards':chosen})
        label='Internal: includes restricted and Director-only formulas.' if internal else 'Public projection: 30 public formulas; hidden formula/body records remain separately gated.'
        write(ROOT/guidepath,template.replace('{{AUDIENCE}}',label).replace('{{BODY_TABLES}}',models_table(bs)))
        write(ROOT/mdpath,'# Leatherworking '+('internal' if internal else 'public')+' recipe cards\n\n**DRAFT — exact review pending.** '+label+'\n\nAll cards require the complete [shared guide]('+Path(guidepath).name+'). Full preserved source records accompany the JSON; operational overlays never replace the historical text.\n\n'+'\n'.join(card_md(c,bs,internal) for c in chosen))
    dump(AUDIT/'LEATHERWORKING_AUTHORING_STATUS.json',{'status':STATUS,'authoredCards':44,'publicCards':30,'internalBaseModels':19,'publicBaseModels':len(pmodels),'protectedFilesUnchanged':42,'recipesApproved':0,'sourceVerdict':{'threadId':THREAD,'turnId':TURN,'replyId':REPLY},'currentReviewedRecipes':218,'remainingRecipes':469,'cosmology':'post-push only'})
    print(json.dumps({'authoredCards':44,'publicCards':30,'baseModels':19,'publicModels':len(pmodels),'recipesApproved':0}))

if __name__=='__main__': main()
