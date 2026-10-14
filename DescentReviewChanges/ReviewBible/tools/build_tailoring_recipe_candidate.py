"""Tailoring authored candidate under TA-D01..16; original records remain intact."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json, math
from build_leatherworking_recipe_candidate import read, sha, write, dump, ratio, unr, fmt, public_projection

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
STATUS='authored-draft-awaiting-exact-review'
AUTH={'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','turnId':'6b7474ed-1bca-40b8-81af-7bfbd843a5cc','replyId':'95ba16b4-b85f-47d8-bc61-047f9ebfcdeb','scope':'source/interface decisions TA-D01..16; exact-card review pending'}
SLOTS={'Cloak':'outerwear-benefit','Mantle':'outerwear-benefit','Gloves':'handwear-pair','Hat':'head','Garment':'body-clothing','Robe':'body-clothing','Cord':'waist-adornment','Veil':'face-accessory'}
DOMAINS={
'presentation':"Wearer's CHA (Persuasion, Deception or Performance) only when visible attire materially helps appearance, costume, ceremony or the presented role; or a genuine DEX disguise-kit check arranging the wearer's own already-worn garment. Ordinary bargaining, threats or singing merely while dressed do not qualify. Another disguise-maker and observers gain no bonus; no tools or proficiency are granted.",
'visual-concealment':"Wearer's DEX (Stealth) with actual useful coverage of outline or appearance and independently legal hiding. No cover, obscurity, invisibility or permission to hide in plain sight is created.",
'quiet-clothing-motion':"Wearer's DEX (Stealth) against their own clothing rustle, panels or snags. Armor noise and disadvantage, feet, speech and other detection consequences remain.",
'discreet-handwork':"Wearer's actual DEX (Sleight of Hand) palming or concealing a physically compatible small object using the gloved hands. No lock work, remote handling, free hand or automatic theft.",
'weather-arrangement':"Wearer's WIS (Survival) to arrange their own clothing coverage, or DEX to position their own ordinary ties and fastenings against ambient wind, rain, spray, grit, heat or cold, with real coverage. Not general navigation, shelter, crafting or repair.",
'exposure':"An actual CON ability check under an independent ordinary ambient-exposure procedure that allows clothing assistance, with the actual necessary body coverage. Never a saving throw, invented check, replacement for a save or automatic exposure success.",
'conceal-contents':"Actual Bag operator's DEX check, with Sleight of Hand only if the task genuinely qualifies, to physically arrange real noncreature cargo using actual folds, lining or other cargo against ordinary inspection. No secret compartment or detection contest is created.",
'organize-contents':"Actual Bag operator's INT check for genuinely difficult sorting/packing of known accessible cargo, or DEX for difficult physical placement/separation. Respect fit, hazards, access, actions, hands and closures; no free retrieval, identification, preservation or extra contents."
}
FAMILY_TASKS={f:['presentation','visual-concealment','quiet-clothing-motion','weather-arrangement','exposure'] for f in ('Cloak','Garment','Robe','Mantle')}
FAMILY_TASKS.update(Gloves=['presentation','discreet-handwork','weather-arrangement'],Hat=['presentation','visual-concealment','weather-arrangement','exposure'],Cord=['presentation','quiet-clothing-motion','weather-arrangement'],Veil=['presentation','visual-concealment','weather-arrangement'],Bag=['conceal-contents','organize-contents'])

def make_models(equipment):
    by={r['name']:r for r in equipment};out={}
    def add(key,name,fam,price,weight,source=None,**extras):
        ident='tailoring.'+key
        out[ident]={'id':ident,'name':name,'family':fam,'baselinePriceGp':price,'baselineWeightLb':weight,'ordinaryMaximumStructuralHP':5,'structuralAC':11,'dominantMaterial':'cloth','gradePolicy':'Standard only','benefitSlot':SLOTS.get(fam),'sourceEquipmentRecord':deepcopy(source),'tailoringLargeVariantMultiplier':1 if fam=='Bag' else 2,'sizeOverlayProvenance':'NEW TA-D02; original equipment sizing fields unchanged','ordinaryArmorFormula':None,'armorProficiencyRequired':False,'strengthMinimum':None,'genericStealthDisadvantage':False,'donMinutes':1 if fam in ('Garment','Robe') else None,'doffMinutes':1 if fam in ('Garment','Robe') else None,'donActions':None if fam in ('Garment','Robe') else 1,'doffActions':None if fam in ('Garment','Robe') else 1,**extras}
    for cap,interior,opening,exterior,axes in [(10,[12,8,6],[12,6],[13,9,7],[0,2]),(30,[18,12,8],[12,8],[20,14,10],[1,2]),(40,[24,12,8],[12,8],[26,14,10],[1,2]),(50,[30,12,8],[12,8],[32,14,10],[1,2])]:
        add('bag-'+str(cap),str(cap)+'-lb fitted textile Bag','Bag',cap//10,cap//10,benefitSlot='pouch-position' if cap==10 else 'back-cargo',physicalContentWeightLimitLb=cap,physicalContentVolumeFt3=ratio(F(cap,30)),compartmentCount=1,compartmentWeightLimitLb=cap,compartmentVolumeFt3=ratio(F(cap,30)),interiorInches=interior,openingInches=opening,exteriorInches=exterior,openingAxes=axes,closure='one fitted strap and handle; ordinary flap and ties; no lock, secret compartment, airtight seal, preservation or fluid containment',outputUnit='one complete Bag')
    for key,name,fam,price,weight,src in [
      ('cloak','Hooded cloak','Cloak',1,2,'Hooded cloak'),('gloves','Matched textile Gloves pair','Gloves',1,0.5,None),('hat','Fitted textile Hat','Hat',0.5,0.5,None),
      ('garment-common','Common-clothes outfit','Garment',0.5,3,'Clothes, common'),('garment-costume','Costume outfit','Garment',5,4,'Clothes, costume'),('garment-fine','Fine-clothes outfit','Garment',15,6,'Clothes, fine'),('garment-traveler','Traveler clothes outfit','Garment',2,4,"Clothes, traveler's"),
      ('robe','Fitted textile Robe','Robe',2,4,None),('cord','Braided clothing girdle','Cord',0.1,0.2,None),('veil','Face Veil with ties','Veil',0.5,0.1,None),('mantle','Short textile shoulder Mantle','Mantle',1,2,None)]:
        add(key,name,fam,price,weight,by[src] if src else None,outputUnit='one complete outfit with prerecorded constituents' if fam=='Garment' else 'one matched pair, both original members required' if fam=='Gloves' else 'one complete item')
    out['tailoring.cord'].update(lengthFeet=6,largeLengthFeet=12,suspendedCargoClimbingRestraintCasualtySupport=False)
    out['tailoring.veil'].update(panelInches=[24,24],largePanelInches=[48,24])
    assert len(out)==15
    return out

def model_ids(r):
    if r['recipeFamily']=='Bag':return ['tailoring.bag-'+str(r['mechanics']['capacityPounds'])]
    if r['recipeFamily']=='Garment':return ['tailoring.garment-'+s for s in ('common','costume','fine','traveler')]
    return ['tailoring.'+r['recipeFamily'].lower()]

def operational(r,models):
    m=r['mechanics'];f=r['recipeFamily'];q=r['quantity'];ids=model_ids(r);container=f=='Bag'
    bonus=m['bonus' if container else 'skillBonus'];hours=r['workRequirements']['activeWorkHours']
    actual=1920 if hours is None else hours;forge=math.ceil(F(str(actual))*45)
    unit=F(str(r['economy']['recommendedMarketValue']))/q
    text="One output transforms one complete mundane body, retaining identity and latest lawful damage. Functional means current structural HP at least 1. "
    if container:
        text+=f"While complete, functional, unsuppressed, unmelded and actually worn or directly held in its {models[ids[0]]['benefitSlot']} position, relieve up to {m['capacityPounds']} lb of eligible real contents in stable loading order. Physical capacity is separately bounded by this model's weight, volume, opening and actual packing. Its own empty body is not relieved. Credit each covered record at most min(canonical Load, covered pounds/10), retaining actual mass and canonical Load. Inner containers cannot grant another relief; external lashings are not contents. "
        text+=f"The actual operator gains +{bonus} only for the defined conceal-contents or organize-contents check using accessible functional unsuppressed fittings. This operator benefit does not require a relief slot and may assist an ally or thief at a table; it grants no ownership recognition. "
    else:
        text+=f"While complete, functional, unsuppressed, unmelded and genuinely worn in its designated {SLOTS[f]} position, the wearer gains +{bonus} on the following defined actual checks only: "+'; '.join(FAMILY_TASKS[f])+". "
        if m.get('resistance'):text+=f"Independently grant the wearer {m['resistance']} damage resistance while legally worn and active, regardless of the winning task bonus or armor formula. It protects neither item nor cargo and repeated resistance does not become immunity. "
        else:text+="No damage resistance is granted. "
    text+="All qualifying Tailoring and Leatherworking task modifiers share equipment.leather-task-enhancement: use the strongest once per actual check. Each family's allowed domains remain distinct. Tailoring supplies no AC candidate, including zero, so it cannot cancel selected Crude armor. Ordinary actions, access, actual checks, tools and proficiency once still govern."
    limits={'Hat':'Exposure covers the actual head only, never an entire body.','Cord':'Only a wearable clothing girdle: no rope, climbing, Athletics, restraint, suspended cargo or casualty support; no garment benefit while deployed across a gap.','Veil':'Actual face coverage only; no complete disguise, gas filter or invisibility.','Gloves':'Both original gloves required; no extra hand, weapon damage or component/focus exception.','Garment':'Record the complete outfit constituents before work. Splitting them does not distribute magic or duplicate inclusive mass.'}
    if f in limits:text+=' '+limits[f]
    if r['id']=='recipe-682':text+=' Bright light does not itself bar a lawful qualifying check; this Cloak creates no darkness, concealment permission or acid resistance.'
    if r['id']=='recipe-683':text+=' This is equipment, not a companion or plant; no regeneration, feeding, harvesting, independent action or Poisoned immunity.'
    if r['id']=='recipe-582':text+=' Bludgeoning resistance includes magical bludgeoning; it supplies no other damage resistance or protection from nondamage pressure, restraint or displacement.'
    return {'sharedProfileId':'tailoring.shared.v1','text':text,'baseModelIds':ids,'effect':{'type':m['type'],'taskBonus':bonus,'taskFamily':'equipment.leather-task-enhancement','taskDomainIds':FAMILY_TASKS[f],'armorBonusCandidate':None,'resistance':m.get('resistance'),'reliefAllowanceLb':m.get('capacityPounds')},'standardQuantity':q,'maximumBaseReserve':3*q//2,'outcomes':{'Standard':q,'ExceptionalYield':5*q//4,'MasterworkYield':3*q//2,'DurabilityOptionQuantity':q,'FlawedQuantity':q//2 if q>=2 else 1,'SingletonFlawedAddsPersistentFlaw':q==1,'Failed':0,'Mishap':0,'eligibleCatalystReturns':0},'work':{'sourceActiveWorkHours':hours,'operationalActiveWorkHours':actual,'nullHourOverlay':hours is None,'ordinaryFirstStablePhaseHours':min(8,actual),'eligibleForgeDwarfActiveMinutes':forge,'eligibleForgeDwarfFirstPhaseMinutes':min(480,forge),'maximumAssistants':r['workRequirements']['maximumAssistants'],'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel']},'sourceProcessUnitReferenceGp':ratio(unit),'standardModelExamples':[{'baseModelId':i,'finishedUnitReferenceGp':ratio(unit+F(str(models[i]['baselinePriceGp'])))} for i in ids],'largeModelExamples':[{'baseModelId':i,'finishedUnitReferenceGp':ratio(unit+F(str(models[i]['baselinePriceGp']))*models[i]['tailoringLargeVariantMultiplier'])} for i in ids]}

def body_table(models):
    rows=['| Body | gp | lb | HP / structural AC | Position | Don / doff |','|---|---:|---:|---|---|---|']
    for b in models.values():rows.append(f"| {b['name']} | {b['baselinePriceGp']} | {b['baselineWeightLb']} | 5 / 11 | {b['benefitSlot']} | "+('1 minute' if b['donMinutes'] else '1 Action')+' each |')
    rows+=['','| Bag | Contents lb / ft³ | Interior in | Opening in | Exterior in |','|---|---|---|---|---|']
    for b in models.values():
        if b['family']=='Bag':rows.append(f"| {b['name']} | {b['physicalContentWeightLimitLb']} / {fmt(unr(b['physicalContentVolumeFt3']))} | {b['interiorInches']} | {b['openingInches']} | {b['exteriorInches']} |")
    return '\n'.join(rows)

def card_md(c,models,internal):
    r=c['sourceRecipe'];o=c['operational'];q=r['quantity'];w=r['workRequirements'];h=o['work']
    lines=[f"## {r['id']} — {r['name']}",'',f"**DRAFT; exact review pending.** {r['visibility']}; Tailoring level {r['skillLevel']}; tier {r['tier']}; {r['rarity']}; crafting DC {r['craftingCheck']['targetDC']}; Standard quantity {q}.",'','**Preserved source effect:** '+r['effects'],'','**Operational effect:** '+o['text'],'','**Check domains:**']
    lines += ['- '+DOMAINS[d] for d in o['effect']['taskDomainIds']]
    lines+=['','**Complete body choices:**',body_table({i:models[i] for i in o['baseModelIds']}),'',f"Reserve {o['maximumBaseReserve']} actual complete nonmagical non-Broken bodies before work, in stable physical-ID order. One model, fitted size and Standard grade for the batch; Bags empty. No prior recipe imprint. Latest lawful physical state controls at completion. Missing, Broken or committed-elsewhere bodies pause the order before the roll; lawful replacement retains its position. Transform the first resolved N; no post-roll selection. Unused bodies remain separate from ingredient recovery.",'','**Source component occurrences:**','','| # | Component | Quantity | Tier | Role | Consumed | Unit lb | Unit gp | Properties |','|---|---|---:|---:|---|---|---:|---:|---|']
    for i,z in enumerate(r['components']):lines.append(f"| {i} | {z['name']} | {z['quantity']} | {z['tier']} | {z['role']} | {z['consumed']} | {z['weight']} | {z['value']} | {', '.join(z['properties'])} |")
    lines+=['','Consumed inputs are process materials paid once; finished empty mass is the actual body mass. Nonconsumed source tools remain the same physical units, not consumed inputs, output mass, catalysts or ingredient-recovery copies. Their tier, role, amount, properties and function must be satisfied; a generic kit does not automatically supply an expensive source tool. All tool profiles have ordinary HP5 and actual declared material defenses. No Tailoring catalyst returns. Formula knowledge is not consumed even when a source Pattern component is.', '',f"**Work:** DEX; reviewed Weaver's-tools credential (Tailor's tools binding); {w['station']}; {', '.join(w['requiredTools'])}. Source fieldCraftable={str(w['fieldCraftable']).lower()} controls even when timeMode={w['timeMode']}. Source time {r['craftingTime']}; activeWorkHours={json.dumps(w['activeWorkHours'])}; operational active hours {h['operationalActiveWorkHours']}"+(' under the separate 1,920-hour overlay; preserve source null and zero labor' if h['nullHourOverlay'] else '')+f". First included stable phase {h['ordinaryFirstStablePhaseHours']} hours. Eligible Forge Dwarf: {h['eligibleForgeDwarfActiveMinutes']} whole active minutes, first phase {h['eligibleForgeDwarfFirstPhaseMinutes']} minutes. Maximum assistants {h['maximumAssistants']}. Stabilize only actually incorporated materials; replacement lots keep their own age. Actual workshop access, work phases, Watches and rest remain required.",'',f"**Access and progression:** original discovery {json.dumps(r['discovery'],ensure_ascii=False)}. Exact trivialAtSkillLevel={h['trivialAtSkillLevel']}; do not regenerate level+5. Untrained level-1–4 attempts retain source disadvantage with all physical requirements met. Higher trade/formula eligibility follows the framework. Trade level is not added to the check and tool ownership grants no proficiency.",'',f"**Quality:** Standard {q}; Exceptional yield {o['outcomes']['ExceptionalYield']}; Masterwork yield {o['outcomes']['MasterworkYield']}; or {q} bodies with the strongest legal 25%/50% noncompounding durability improvement. Flawed {o['outcomes']['FlawedQuantity']} "+('with one persistent singleton half-maximum flaw' if q==1 else 'with ordinary effect, preserving existing flaws')+'. Failed/Mishap transform none. Choose yield or durability once for the batch after rolling. Preserve latest damage deficit, apply the strongest percentage to ordinary body HP and one flaw last. A functional damaged reserve can emerge Broken. Quality changes no potency, resistance, capacity, relief, grade or permission.', '',f"**Repair:** trained DEX + Weaver's-tools proficiency and actual Weaver's tools, using the Tailor's-tools binding; an actual Loom and Cutting Table; and the required Needles and Shears. The same actual implement may meet compatible overlapping requirements without duplicate purchases. Missing the actual toolkit prevents starting either route; a quotation alone grants no permission. Functional HP≥1: DC10, max(1 hour, recorded max HP/10), materials 25% actual undamaged mundane body reference. Broken HP0: DC{r['craftingCheck']['targetDC']}, max(8 hours, recorded max HP/10), materials 25% undamaged finished unit reference; recoverable original main body required, including both original Gloves members or the required original outfit constituents. Binary success restores recorded maximum and dormant imprint usability subject to suppression; failure consumes work/materials. No formula or original trade level, XP, quality, catalyst return or Forge Dwarf reduction; original rare creation-tool rows are not extra generic repair requirements. Preserve identity, fit, model, size, grade, durability and flaw. Repair returns no lost contents.",'', '**Finished ordinary unit reference:** '+'; '.join(models[z['baseModelId']]['name']+' '+fmt(unr(z['finishedUnitReferenceGp']))+' gp' for z in o['standardModelExamples'])+'. Divide the source Standard batch value by source Q, then add the actual undamaged body reference. Larger garment variants double only body price/weight/ordinary HP, not process price or potency. Keep exact precision until a real transaction; actual buyer and quote required. Tool purchases, reservations and rentals remain separate.', '', '**Preserved tags:** '+', '.join(r['tags'])+'. Names, tags and donor metadata add no powers or ingredient availability.','']
    if c.get('publicBookBinding'):lines+=['**Public V5 source paragraphs:** '+', '.join(str(p['index']) for p in c['publicBookBinding']['paragraphs'])+'.','']
    legacy={k:r[k] for k in ('legacyName','legacyEffect','wholeCreatureUse') if k in r}
    if legacy:lines+=['**Preserved inactive metadata:** '+json.dumps(legacy,ensure_ascii=False), '']
    if internal and 'directorGuidance' in r:lines+=['**Preserved optional Director guidance:** '+json.dumps(r['directorGuidance'],ensure_ascii=False),'']
    return '\n'.join(lines)

def main():
    assert not (ROOT/'docs/mechanics/TAILORING_REVIEW_STATUS.json').exists(),'Already reviewed; do not overwrite.'
    baseline=read(AUDIT/'TAILORING_PART2_REVIEW_BASELINE.json')
    assert all(sha(GAME/p)==h for p,h in baseline['files'].items()),'Protected input changed'
    source_path=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    evidence=read(AUDIT/'TAILORING_SOURCE_PREPARATION.json')
    recipes=[r for r in read(source_path)['recipes'] if r['skill']=='Tailoring']
    assert recipes==evidence['recipes'] and len(recipes)==43
    models=make_models(read(ROOT/'data/playtest/equipment_acquisition_candidate.json')['items'])
    bindings={b['recipeId']:b for b in evidence['publicBookBindings']}
    cards=[{'recipeId':r['id'],'name':r['name'],'visibility':r['visibility'],'status':STATUS,'sourceRecipeIndex':evidence['sourceIndices'][r['id']],'sourceRecipe':deepcopy(r),'publicBookBinding':deepcopy(bindings.get(r['id'])),'operational':operational(r,models)} for r in recipes]
    public=[public_projection(c) for c in cards if c['visibility']=='public']
    assert len(public)==29
    allowed={i for c in public for i in c['operational']['baseModelIds']}
    pmodels={i:b for i,b in models.items() if i in allowed}
    assert len(pmodels)==11
    shared={'id':'tailoring.shared.v1','classification':{'magical':True,'artifact':False,'attunementRequired':False,'resourceCost':0,'concentration':False,'spellActivationRequired':False},'taskFamily':'equipment.leather-task-enhancement','taskDomains':DOMAINS,'familyTaskDomains':FAMILY_TASKS,'noArmorCandidate':True,'sourceAuthority':AUTH,'bodyStructuralAC':11,'bodyOrdinaryHP':5,'reusableSpecialistToolHP':5,'fiveReliefSlots':{'back-cargo':1,'quiver':1,'waist-cargo':1,'pouch-position':2},'sourceInputsUntouched':True}
    template=(ROOT/'tools/templates/tailoring_rules.md').read_text(encoding='utf-8')
    for internal,cs,bs,base in [(True,cards,models,'director'),(False,public,pmodels,'playtest')]:
        folder='director-only' if internal else 'mechanics'
        guide=f'docs/{folder}/TAILORING_'+('INTERNAL_GUIDE' if internal else 'RECIPE_PLAYTEST')+'.md'
        cardpath=f'docs/{folder}/TAILORING_'+('INTERNAL' if internal else 'PUBLIC')+'_RECIPE_CARDS.md'
        suffix='_internal' if internal else ''
        shared_projection=deepcopy(shared)
        if not internal:shared_projection['familyTaskDomains'].pop('Mantle')
        dump(ROOT/f'data/{base}/tailoring_recipe_candidate{suffix}.json',{'schemaVersion':1,'status':STATUS,'visibility':'director-internal' if internal else 'public','sourceSha256':sha(source_path),'sourceAuthority':AUTH,'sharedOperationalProfile':shared_projection,'sharedGuide':guide,'baseModels':bs,'cards':cs,'exactRecipeApproval':False,'runtimeImplemented':False,'balanceApproved':False,'cosmology':'post-push only'})
        audience='Internal: all 43 formulas, including restricted and Director-only records.' if internal else 'Public: 29 formulas; private formulas and their body records remain separately gated.'
        write(ROOT/guide,template.replace('{{AUDIENCE}}',audience).replace('{{BODY_TABLES}}',body_table(bs)))
        write(ROOT/cardpath,'# Tailoring '+('internal' if internal else 'public')+' recipe cards\n\n**DRAFT — exact review pending.** '+audience+'\n\nEvery card uses the complete [shared guide]('+Path(guide).name+'). Full source records accompany the JSON.\n\n'+'\n'.join(card_md(c,bs,internal) for c in cs))
    dump(AUDIT/'TAILORING_AUTHORING_STATUS.json',{'status':STATUS,'authoredCards':43,'publicCards':29,'internalBaseModels':15,'publicBaseModels':11,'ordinaryModelValueCombinations':91,'protectedFilesUnchanged':len(baseline['files']),'recipesApproved':0,'sourceVerdict':AUTH,'currentReviewedRecipes':262,'remainingRecipes':425,'cosmology':'post-push only'})
    print(json.dumps({'cards':43,'public':29,'models':15,'publicModels':11,'recipesApproved':0}))

if __name__=='__main__':main()

