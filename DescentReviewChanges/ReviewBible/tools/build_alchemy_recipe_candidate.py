"""Author explicit Alchemy cards while retaining source evidence and visibility."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def seconds(s):
    if 'long rest' in s:return None
    n,unit=s.split(' ',1)
    return int(n)*(60 if unit.startswith('minute') else 3600)

def main():
    if (ROOT/'docs/mechanics/ALCHEMY_REVIEW_STATUS.json').exists():raise SystemExit('Reviewed Alchemy exists; do not overwrite with draft generation.')
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    src=json.loads(source.read_text(encoding='utf-8-sig'))
    recipes=[x for x in src['recipes'] if x['skill']=='Alchemy']
    assert len(recipes)==45
    guide='docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md'
    cards=[]
    compact=[]
    for r in recipes:
        ident=r['id'];m=r['mechanics'];kind=r['outputType'];q=r['quantity']
        duration=m.get('duration');time=seconds(duration) if duration else None
        eff={'type':kind,'tag':m['tag'],'magical':True,'spell':False,'concentration':False,'sourceCreatureTypeExclusion':None}
        prose=''
        if kind=='consumable_resistance':
            eff.update(damageType=m['damageType'],resistanceSeconds=time)
            prose=f"Gain resistance to {m['damageType']} damage for {duration}."
            if ident=='recipe-41':
                eff.pop('resistanceSeconds');eff.update(immunitySeconds=86400,followingResistanceSeconds=3600)
                prose='Gain cold-damage immunity for24 elapsed hours; at that normal expiry gain cold-damage resistance for1 additional hour. Early ending does not trigger the follow-on resistance.'
        elif kind=='consumable_resonance':
            eff.update(rpRestored=m['resonanceRestored'],recipientUseLimit=1,recharge='beneficial-long-rest',limitKey='recipient+recipeId',entitlementCommit='legal administration start',convertsOtherResources=False)
            prose=f"Restore {m['resonanceRestored']} expended RP, capped at the actual RP maximum. One recipient use of this recipe per beneficial Long Rest, spent at legal administration start even on zero/blocked recovery. No pool or no capacity grants no RP; no RC or other-resource conversion."
        elif kind=='consumable_healing':
            cure=ident in ['recipe-36','recipe-38','recipe-40']
            eff.update(healing=m['healing'],operation='ordinary-magical-nonspell-current-HP-healing',independentCureCount=1 if cure else 0,independentCureScope='one removable present poison/disease effect' if cure else None)
            prose=f"Restore {m['healing']} ordinary magical nonspell HP under actual caps and blockers."
            if cure:prose+=' After the healing attempt, independently end one selected present removable poison or disease effect as defined in the shared guide. No Wound, intrinsic trait, curse, Corruption or resurrection removal.'
        elif kind=='consumable_buff' and m['tag']=='Strength':
            eff.update(strengthCheckBonus=m['attackBonus'],meleeDamageRollBonus=m['damageBonus'],attackRollBonus=0,durationSeconds=time)
            prose=f"Gain +{m['attackBonus']} to Strength ability checks and +{m['damageBonus']} to actual melee damage rolls for {duration}. No attack-roll or saving-throw bonus."
        elif kind=='consumable_buff' and m['tag']=='Stealth':
            eligible=r['rarity'] in ['Rare','Very Rare','Legendary','Mythic']
            eff.update(stealthCheckBonus=m['stealthBonus'],durationSeconds=time,invisibleRiderEligible=eligible,invisibleUsesPerDose=1 if eligible else 0,invisibleAction='Bonus Action' if eligible else None,invisibleEnd='recipient next regular-turn end or parent expiry, whichever first' if eligible else None)
            prose=f"Gain +{m['stealthBonus']} to Stealth checks for {duration}. "
            prose+=('Once during this actual dose record, Bonus Action: become Invisible until the recipient\'s next regular-turn end or the dose\'s expiry, whichever first. Use Core Invisible observer/location rules.' if eligible else 'Actual rarity is Uncommon, so the source Rare-or-higher Invisible rider is unavailable; its Tier/name does not unlock it.')
        elif kind=='consumable_mental':
            radius={'recipe-24':40,'recipe-27':50,'recipe-626':70}[ident]
            eff.update(saveAdvantageConditions=m['saveAdvantage'],durationSeconds=time,endsAtNextBeneficialLongRest=time is None,telepathyFeet=radius,telepathyPartners=1,telepathyLanguage='shared language',telepathyRequiresWilling=True,telepathyRequiresLineOfEffect=True)
            prose=f"For {duration}, gain advantage on saves against Charmed/Frightened and willing two-way telepathic communication with one partner within {radius} feet under the shared perception, line, language and communication rules. Neither mind-reading nor an existing-condition cure."
        elif kind=='thrown_explosive':
            eff.update(damage=m['damage'],damageType=m['damageType'],saveAbility='DEX',saveDC=m['saveDC'],radiusFeet=m['radiusFeet'],normalRangeFeet=30,longRangeFeet=60,longRangeEffect='targets gain advantage on DEX save',attackRoll=False,onSave='half rounded down',targets='all creatures in sphere with line from origin',objectsAffected=False)
            prose=f"Action: throw to a seen legal point30/60 feet; {m['radiusFeet']}-foot-radius sphere. Every exposed creature makes DC {m['saveDC']} DEX; failure {m['damage']} {m['damageType']}, success half. One shared damage roll. Beyond30 feet targets have save advantage. Area-origin cover applies; no attack roll, ability damage, object damage or persistent zone."
        else:raise ValueError((ident,kind))
        if q>=2:flaw={'mode':'half-batch-quantity','quantity':q//2,'effectChange':None}
        elif time is not None:
            flaw={'mode':'half-fixed-duration','primarySeconds':max(6,(time//12)*6)}
            if ident=='recipe-41':flaw['followingResistanceSeconds']=1800
        else:flaw={'mode':'treat-as-Failed','quantity':0,'recovery':'framework 25% non-catalyst'}
        vessels=sum(c['quantity'] for c in r['components'] if c['role']=='vessel' and c['consumed'])
        nonvessel=sum(Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed'] and c['role']!='vessel')
        maxcat=max((Fraction(str(c['weight'])) for c in r['components'] if c['role']=='catalyst' and c['consumed']),default=Fraction(0))
        master=q*3//2
        component_floor=nonvessel-maxcat
        assert component_floor>=Fraction(master,10),(ident,component_floor,master)
        operation={'text':prose,'effect':eff,'activation':{'action':'Action','handRequired':1,'delivery':'throw' if kind=='thrown_explosive' else 'drink or feed','recipientRangeFeet':None if kind=='thrown_explosive' else 5,'cost':'one actual dose; no RP/RC','spellRank':None,'school':None},
            'physical':{'compoundWeightLb':0.1,'containerWeightLb':0.1,'grossWeightLb':0.2,'containerAC':13,'containerHP':1,'doses':1,'vialSlots':1,'classification':'magical-nonspell-consumable; no default artifact status','sealedShelfLife':'indefinite while intact in ordinary conditions','openedLifetimeSeconds':3600,'bombContainerDestroyedOnUse':kind=='thrown_explosive'},
            'craft':{'batchQuantity':q,'sourceVesselUnits':vessels,'additionalStandardGlassVials':max(0,q-vessels),'additionalMasterworkGlassVials':max(0,master-vessels),'extraPackagingItemId':'alchemical-containers.glass-vial','extraPackagingUnitCp':100,'firstStabilizationPhaseMinutes':15,'firstPhaseIncludedInTotal':True,'sourceNonVesselMassLb':float(nonvessel),'minimumNonVesselMassAfterOneCatalystLb':float(component_floor),'flawed':flaw,'qualityPotencyBonus':False,'qualityDurabilityOption':'container HP1 to HP2 only; contents unchanged'},
            'value':{'sourceStandardBatchReferenceGp':r['economy']['recommendedMarketValue'],'unitReferenceGp':{'numerator':r['economy']['recommendedMarketValue'],'denominator':q},'extraPackagingIncludedInSourceCost':False},
            'sharedRules':guide}
        cards.append({'recipeId':ident,'name':r['name'],'visibility':r['visibility'],'status':'draft-awaiting-GPT-review','sourceSha256':sha(source),'sourceRecipeIndex':src['recipes'].index(r),'sourceEffect':r['effects'],'sourceMechanics':deepcopy(m),'legacyEffect':r.get('legacyEffect'),'legacyEffectSourcePresent':'legacyEffect' in r,'legacyName':r.get('legacyName'),'legacyNameSourcePresent':'legacyName' in r,'sourceRequirements':{k:deepcopy(r[k]) for k in ['skill','skillLevel','difficulty','tier','rarity','quantity','craftingTime','workRequirements','discovery','components','economy','skillProgression']},'operational':operation})
        compact.append({k:deepcopy(r[k]) for k in ['id','name','visibility','effects','legacyEffect','legacyName','mechanics','skill','skillLevel','difficulty','tier','rarity','quantity','craftingTime','workRequirements','discovery','components','economy','skillProgression'] if k in r})
    envelope={'schemaVersion':1,'status':'draft-awaiting-GPT-review','sourceSha256':sha(source),'sharedRules':guide,'cosmology':'not evaluated; after verified authorized GitHub push only','runtimeImplemented':False,'balanceApproved':False}
    save(ROOT/'data/playtest/alchemy_recipe_candidate.json',{**envelope,'visibility':'public','cards':[x for x in cards if x['visibility']=='public']})
    save(ROOT/'data/director/alchemy_recipe_candidate_internal.json',{**envelope,'visibility':'director-internal','cards':cards})
    save(AUDIT/'ALCHEMY_COMPACT_SOURCE_BINDINGS.json',{'sourceSha256':sha(source),'visibility':'director-internal','records':compact})
    for public,path in [(True,ROOT/'docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md'),(False,ROOT/'docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md')]:
        selected=[x for x in cards if x['visibility']=='public'] if public else cards
        out=['# Alchemy '+('public' if public else 'Director internal')+' recipe cards','',
            '**Draft awaiting joint review.** '+('27 public entries.' if public else 'All45 entries, including5 restricted and13 Director-only; do not distribute this file as a player artifact.'),
            '', 'Every card uses ALCHEMY_RECIPE_PLAYTEST.md for complete activation, targeting, stack/expiry, packaging, manufacture, quality and market procedures. Original metadata and component rows are retained in the corresponding JSON. Printed source references are batch values, not per-unit automatic prices. Names do not grant equipment grades.','']
        for c in selected:
            req=c['sourceRequirements'];op=c['operational'];cr=op['craft'];flaw=cr['flawed']
            out+=['## '+c['recipeId']+' — '+c['name'],'',f"**Source:** {c['visibility']}; Alchemy skill {req['skillLevel']}; Tier {req['tier']}; actual rarity {req['rarity']}; DC {req['difficulty']}; {req['workRequirements']['activeWorkHours']} active hours; {req['quantity']} units. Standard batch reference {req['economy']['recommendedMarketValue']} gp.",'',
                '**Preserved effect:** '+c['sourceEffect'],'','**Operational effect:** '+op['text'],'',
                '**Work:** '+req['workRequirements']['station']+'; '+', '.join(req['workRequirements']['requiredTools'])+f". Mode {req['workRequirements']['timeMode']}; field flag {str(req['workRequirements']['fieldCraftable']).lower()}; maximum assistants {req['workRequirements']['maximumAssistants']}; formula required {str(req['discovery']['requiresFormula']).lower()}.",'',
                '**Exact ingredients:** '+'; '.join(f"{x['quantity']} × {x['name']} (component tier{x['tier']}; {x['weight']} lb/unit; {x['value']} gp/unit; {x['role']}; {'consumed' if x['consumed'] else 'returned'})" for x in req['components'])+'.','',
                f"**Packaging:** source vessel count {cr['sourceVesselUnits']}; additional Glass Vials needed at Standard {cr['additionalStandardGlassVials']}, at full Masterwork yield {cr['additionalMasterworkGlassVials']}. Each finished unit0.2 lb including its actual0.1-lb container. Supplementary packaging1 gp per new Glass Vial when bought at the reviewed base price; actual supplier terms apply.",'',
                '**Flawed:** '+json.dumps(flaw,ensure_ascii=False)+'. No extra potency on Exceptional/Masterwork; select finite yield or physical container durability only.','',
                '**Source preservation:** '+((c['legacyName']+' remains the legacy name. ') if c['legacyNameSourcePresent'] else 'No legacy name is stored on this source record. ')+('Its older effect is inactive; exact legacy wording is retained in JSON/source bindings. ' if c['legacyEffectSourcePresent'] else 'No legacy effect is stored on this source record. ')+'No source information is deleted.','']
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text('\n'.join(out),encoding='utf-8')
    baseline=AUDIT/'ALCHEMY_REVIEW_BASELINE.json'
    if not baseline.exists():
        frozen=[source,GAME/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json',ROOT/'src/data/crafting-recipes.json',GAME/'src/data/crafting-recipes.json',GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx',ROOT/'data/playtest/equipment_acquisition_candidate.json',ROOT/'data/playtest/crafting_engine_candidate.json',ROOT/'data/director/crafting_engine_recipe_index.json']
        frozen += [ROOT/'docs/mechanics'/n for n in ['CRAFTING_HARVEST_PLAYTEST.md','CRAFTING_TRADE_REFERENCE.md','CORE_RESOLUTION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','SPELL_INTEGRATION_RULES.md','EQUIPMENT_ITEM_PROCEDURES.md','CLASS_PLAYTEST_RULES.md']]
        save(baseline,{'scope':'All listed source and reviewed-rule artifacts must remain byte-identical during the Alchemy card review.','files':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in frozen}})
    print(json.dumps({'cards':len(cards),'public':sum(x['visibility']=='public' for x in cards),'restricted':sum(x['visibility']=='restricted' for x in cards),'directorOnly':sum(x['visibility']=='director-only' for x in cards),'allMaximumCompoundMassChecksPass':True}))

if __name__=='__main__':main()
