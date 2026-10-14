"""Build a reviewable framework projection; preserve every source recipe verbatim."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')

def main():
    if (ROOT/'docs/mechanics/CRAFTING_ENGINE_REVIEW_STATUS.json').exists():
        raise SystemExit('Reviewed artifacts exist. Do not replace with draft generation.')
    p=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    d=json.loads(p.read_text(encoding='utf-8-sig'))
    # Binding, artisan category, minor accident damage; these are explicit new completions.
    bindings={
        'Alchemy':("Alchemist's supplies",True,'acid'),
        'Blacksmithing':("Smith's tools",True,'fire'),
        'Cooking':("Cook's utensils",True,'fire'),
        'Enchanting':("Enchanter's tools",True,'force'),
        'Fishing':('Fishing tackle',False,'piercing'),
        'Herbalism':('Herbalism kit',False,'slashing'),
        'Jewelcrafting':("Jeweler's tools",True,'piercing'),
        'Leatherworking':("Leatherworker's tools",True,'slashing'),
        'Mining':("Miner's tools",False,'bludgeoning'),
        'Poisoncrafting':("Poisoner's kit",False,'poison'),
        'Rune Carving':("Runecarver's tools",True,'force'),
        'Salvaging':("Salvager's tools",False,'slashing'),
        'Scribing':("Calligrapher's supplies",True,'piercing'),
        'Skinning':("Skinner's tools",False,'slashing'),
        'Tailoring':("Weaver's tools",True,'piercing'),
        'Tinkering':("Tinker's tools",True,'piercing')}
    newtools=[
        {'id':'crafting.enchanter-tools','name':"Enchanter's tools",'priceCp':2500,'weightLb':5,'contents':'Inscription stylus and ordinary focusing lens; no spell, RP or charge grant.'},
        {'id':'crafting.miner-tools','name':"Miner's tools",'priceCp':2500,'weightLb':10,'contents':'Pick and portable assay tools; no ore or automatic prospecting success.'},
        {'id':'crafting.runecarver-tools','name':"Runecarver's tools",'priceCp':2500,'weightLb':5,'contents':'Carving stylus and ordinary focusing crystal; no prepared rune or magical effect.'},
        {'id':'crafting.salvager-tools','name':"Salvager's tools",'priceCp':2500,'weightLb':5,'contents':'Separation tools, shallow trays and 1-pound-capacity mundane containment box; no magical stasis.'},
        {'id':'crafting.skinner-tools','name':"Skinner's tools",'priceCp':500,'weightLb':5,'contents':'Skinning knife, bone saw and scraper; no automatic harvest or food.'}]
    trades=[]
    for name,src in d['tradeskills'].items():
        primary,artisan,injury=bindings[name]
        trades.append({'name':name,'primaryTool':primary,'artisanTool':artisan,'injuryDamageType':injury,
            'source':{k:v for k,v in src.items() if k!='rankBands'},
            'bindingProvenance':'new framework completion; Tailor tools bind Weaver tools, Skinning implements form Skinner tools; no source grant is removed'})
    rows=[]
    for r in d['recipes']:
        rows.append({'recipeId':r['id'],'name':r['name'],'visibility':r['visibility'],
            'skill':r['skill'],'skillLevel':r['skillLevel'],'tier':r['tier'],'batchQuantity':r['quantity'],
            'sourceActiveHours':r['workRequirements']['activeWorkHours'],
            'candidateActiveHours':1920 if r['workRequirements']['activeWorkHours'] is None else r['workRequirements']['activeWorkHours'],
            'timeProvenance':'new workyear conversion' if r['workRequirements']['activeWorkHours'] is None else 'source',
            'requiresFormula':r['discovery']['requiresFormula'],'sourceRecommendedValue':r['economy']['recommendedMarketValue'],
            'candidateBatchReferenceValueGp':r['economy']['recommendedMarketValue'],
            'candidateUnitValueRatioGp':{'numerator':r['economy']['recommendedMarketValue'],'denominator':r['quantity']},
            'effectReviewStatus':'unreviewed','sourcePointer':'/recipes/'+str(len(rows))})
    candidate={'schemaVersion':1,'status':'draft-awaiting-GPT-review','authority':'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md',
        'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ordinaryRecipeEffectsApproved':0,
        'scope':'Framework, not recipe effects, runtime implementation or balance approval.',
        'cosmology':'Deferred until after verified authorized GitHub push.',
        'rules':{'openingElapsedHours':2400,'workdayHours':8,'workweekHours':40,'workmonthHours':160,'workyearHours':1920,
            'trainingHours':80,'defaultTuitionCp':1000,'trainedBasicAccessThroughSkillLevel':4,'maxTradeLevel':20,
            'ordinaryToolBonus':0,'ordinaryFacilityBonus':0,'genericHarvestAssistantCap':1,
            'preservationLotMaxLb':10,'preservationMinutes':30,'preservationSuppliesCp':100,'preservationSuppliesLb':0.5,
            'preservationProtectionHours':24,'defaultPreservationHours':{'bloodOrgans':1,'essence':0.5,'meat':8,'hide':12},
            'genericHarvestDCByMaterialTier':{'1':12,'2':13,'3':15,'4':16,'5':18,'6':19},
            'craftNaturalOne':'mishap','craftNaturalTwenty':'numeric total only','failureRecoveryFraction':0.25,
            'qualityYieldMultipliers':{'Masterwork':1.5,'Exceptional':1.25,'Standard':1},
            'equipmentGradeFromOutcome':False,'sameNameMaterialMerge':False,'recommendedValueIsBatch':True},
        'trades':trades,'newToolProfiles':newtools,
        'publicRecipeFrameworkIndex':[x for x in rows if x['visibility']=='public'],
        'openScope':['All 687 recipe effect cards','Magic essence/active-core containment profiles','Convoy Integrity and full expedition/Haven integration','Runtime inventory deduction','Balance playtesting']}
    save(ROOT/'data/playtest/crafting_engine_candidate.json',candidate)
    save(ROOT/'data/director/crafting_engine_recipe_index.json',{'status':candidate['status'],'visibility':'director-internal','sourceSha256':candidate['sourceSha256'],'recipes':rows,'warning':'Framework projection only. All 687 output effects remain unreviewed. Preserve restricted information.'})
    text=['# Crafting trade reference','', '**Status: authored framework candidate awaiting GPT review.** Mechanical source ability/station/tools are preserved below. Primary-tool bindings, kit grouping and injury damage types are new playtest completions. None grants a proficiency through ownership.','',
        '| Trade | Ability options | Primary proficiency | Artisan category | Mishap injury |','|---|---|---|---|---|']
    for t in trades:
        text.append(f"| {t['name']} | {' / '.join(t['source']['abilityOptions'])} | {t['primaryTool']} | {'Yes' if t['artisanTool'] else 'No'} | {t['injuryDamageType']} |")
    text+=['','Existing equipment supplies its actual price, mass and container capacity. Scribe\'s supplies use Calligrapher\'s supplies, as already reviewed. **New binding:** Tailor\'s tools use Weaver\'s tools; needles and shears are ordinary durable implements of that kit, while a loom/cutting table remains a separate station. Skinning\'s listed implements are grouped into the new Skinner\'s tools credential and kit. Fishing tackle is a permissible particular tool proficiency when a grant allows any tool; it is not an artisan-tool choice. The other non-artisan categories likewise do not become artisan tools just because a character has an artisan choice.','',
        'Arcana tools, religious implements, divination tools, survival tools, siege engineer tools, carpenter tools and unrelated proficiencies do not automatically substitute for one of these primary credentials. Explicit grants keep their actual scopes. They may support a plausible task without conferring a separate crafting trade.','',
        '## New mundane kits','', '| Kit | Price | Weight | Contents/limits |','|---|---:|---:|---|']
    for t in newtools:text.append(f"| {t['name']} | {t['priceCp']/100:g} gp | {t['weightLb']:g} lb | {t['contents']} |")
    text+=['','These kits use ordinary object/tool structural HP 5 and their actual material defenses from the equipment procedure. They grant no numeric check bonus. Their implements are tools rather than automatically weapon profiles. The Salvager box has a maximum 1-lb and 0.05-cubic-foot capacity, both required; its own mass is already in the kit weight. These prices and weights are new completions, not recovered source prices.','',
        '## Actual stations and auxiliary implements','',
        'A listed auxiliary implement already physically present inside a relevant kit can satisfy that same requirement; do not buy a duplicate simply because the source lists both the kit and its normal knife/stylus. Required simultaneous counts still matter. A nonconsumed component and the required toolkit may share an actual implement only if its form and available quantity satisfy both. A consumed incorporated part cannot simultaneously serve as the retained kit component. Heat, a forge/anvil, a loom, stable benches, secure storage, harvested ingredients and separately consumed parts are not conjured by kit ownership.','',
        '**New Haven service:** an available ordinary staffed workshop can rent one compatible station for 1 gp per eight reserved work hours, charged proportionately and rounded up once to a copper. This includes its ordinary fixed fixtures, nonconsumed auxiliary implements and ordinary operating heat/fuel, not the crafter\'s primary kit, recipe components, labor, rare reagents, magic power, protected long-term storage, legal access or a numeric bonus. Record the real facility and capacity before work. Availability and an explicit local quote take precedence. This is an ordinary rental baseline, not a construction cost or an infinite number of stations.','',
        '| Trade | Source station | Source required implements | Generally field-capable |','|---|---|---|---|']
    for t in trades:text.append(f"| {t['name']} | {t['source']['station']} | {'; '.join(t['source']['requiredTools'])} | {'Yes' if t['source']['fieldCapable'] else 'No'} |")
    text+=['','Both the actual recipe\'s fieldCraftable flag and its physical requirements still apply. A dock needs water and a mine face needs an actual deposit. Renting a room cannot supply either. A field-capable trade does not make every recipe portable.','',
        '## Source identification mapping','', '| Creature type | Knowledge skill |','|---|---|']
    for typ,skill in d['system']['harvesting']['typeSkills'].items():text.append(f'| {typ} | {skill} |')
    text+=['','Use the main supplement\'s declared manifest, finite yield pool, times, DCs and assistant limit. A creature\'s type is its actual reviewed game type; this table makes no assertion about its origin or cosmology.','']
    (ROOT/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md').write_text('\n'.join(text),encoding='utf-8')
    print(json.dumps({'trades':len(trades),'newKits':len(newtools),'publicFrameworkRows':sum(x['visibility']=='public' for x in rows),'directorRows':len(rows),'recipeEffectsApproved':0}))

if __name__=='__main__': main()
