"""Validate source fidelity, secrecy and arithmetic of the Alchemy manuscript."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    raw=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    src={x['id']:x for x in raw['recipes'] if x['skill']=='Alchemy'}
    full=read(ROOT/'data/director/alchemy_recipe_candidate_internal.json');pub=read(ROOT/'data/playtest/alchemy_recipe_candidate.json')
    cards=full['cards'];by={x['recipeId']:x for x in cards};b=read(AUDIT/'ALCHEMY_REVIEW_BASELINE.json')
    checks=[]
    def check(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail})
    check('All seventeen source/prior-rule artifacts unchanged',all(sha(GAME/p)==h for p,h in b['files'].items()),len(b['files']))
    check('45 exact Alchemy identities with no duplication',len(cards)==len(by)==len(src)==45 and set(by)==set(src))
    check('27 exact public identities',len(pub['cards'])==27 and {c['recipeId'] for c in pub['cards']}=={id for id,r in src.items() if r['visibility']=='public'})
    check('Five restricted and thirteen Director-only retained internally',sum(c['visibility']=='restricted' for c in cards)==5 and sum(c['visibility']=='director-only' for c in cards)==13)
    check('Public cards equal their internal counterparts',all(c==by[c['recipeId']] for c in pub['cards']))
    check('Source names, visibility and effect text preserved',all(c['name']==src[c['recipeId']]['name'] and c['visibility']==src[c['recipeId']]['visibility'] and c['sourceEffect']==src[c['recipeId']]['effects'] for c in cards))
    check('Source mechanics preserved independently of operational decisions',all(c['sourceMechanics']==src[c['recipeId']]['mechanics'] for c in cards))
    check('All original crafting requirements retained exactly',all(all(src[c['recipeId']][k]==v for k,v in c['sourceRequirements'].items()) for c in cards))
    check('Legacy absence distinguished from null/value',all(c['legacyName']==src[c['recipeId']].get('legacyName') and c['legacyNameSourcePresent']==('legacyName' in src[c['recipeId']]) and c['legacyEffect']==src[c['recipeId']].get('legacyEffect') and c['legacyEffectSourcePresent']==('legacyEffect' in src[c['recipeId']]) for c in cards))
    check('Source pointers resolve exact identity',all(raw['recipes'][c['sourceRecipeIndex']]['id']==c['recipeId'] for c in cards))
    check('All source hashes match current bible',full['sourceSha256']==pub['sourceSha256']==sha(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json') and all(c['sourceSha256']==full['sourceSha256'] for c in cards))
    evidence=read(AUDIT/'ALCHEMY_PUBLIC_BOOK_BINDINGS.json')
    check('27 public book bindings agree with exact effects',len(evidence['publicRecipes'])==27 and all(x['effectMatchesMechanicalSource'] and any(p['text']=='Effect. '+src[x['recipeId']]['effects'] for p in x['passages']) for x in evidence['publicRecipes']))
    for field in ['sourceVesselUnits','additionalStandardGlassVials','additionalMasterworkGlassVials']:
        ok=True
        for c in cards:
            r=src[c['recipeId']];q=r['quantity'];v=sum(x['quantity'] for x in r['components'] if x['consumed'] and x['role']=='vessel')
            expect={'sourceVesselUnits':v,'additionalStandardGlassVials':max(0,q-v),'additionalMasterworkGlassVials':max(0,q*3//2-v)}[field]
            ok &= c['operational']['craft'][field]==expect
        check('Packaging arithmetic '+field,ok)
    check('Maximum quality compound mass is physically funded even after one retained catalyst',all(Fraction(str(c['operational']['craft']['minimumNonVesselMassAfterOneCatalystLb']))>=Fraction(src[c['recipeId']]['quantity']*3//2,10) for c in cards))
    check('Finished gross mass includes one vial and one compound portion',all(Fraction(str(c['operational']['physical']['grossWeightLb']))==Fraction(str(c['operational']['physical']['compoundWeightLb']))+Fraction(str(c['operational']['physical']['containerWeightLb']))==Fraction(1,5) for c in cards))
    check('Known supplementary Glass Vial binding matches equipment price/mass',any(x['id']=='alchemical-containers.glass-vial' and x['unitPriceCp']==100 and x['unitWeightLb']==0.1 for x in read(ROOT/'data/playtest/equipment_acquisition_candidate.json')['items']))
    check('All batch values preserved with exact unit ratios',all(c['operational']['value']['sourceStandardBatchReferenceGp']==src[c['recipeId']]['economy']['recommendedMarketValue'] and c['operational']['value']['unitReferenceGp']=={'numerator':src[c['recipeId']]['economy']['recommendedMarketValue'],'denominator':src[c['recipeId']]['quantity']} for c in cards))
    check('Three Strength tonics do not inherit attack accuracy',all(by[id]['operational']['effect']['attackRollBonus']==0 and by[id]['operational']['effect']['strengthCheckBonus']==1 and by[id]['operational']['effect']['meleeDamageRollBonus']==1 for id in ['recipe-11','recipe-12','recipe-16']))
    check('Actual rarity gates Veiled invisibility',by['recipe-23']['operational']['effect']['invisibleRiderEligible'] is False and all(by[id]['operational']['effect']['invisibleRiderEligible'] is True for id in ['recipe-30','recipe-35']))
    check('Cold immunity retains distinct follow-on resistance',by['recipe-41']['operational']['effect']['immunitySeconds']==86400 and by['recipe-41']['operational']['effect']['followingResistanceSeconds']==3600 and 'resistanceSeconds' not in by['recipe-41']['operational']['effect'])
    check('Mental prose-only telepathy mapped for all three doses',[by[id]['operational']['effect']['telepathyFeet'] for id in ['recipe-24','recipe-27','recipe-626']]==[40,50,70])
    check('Until-LR mental duration not invented as finite hours',by['recipe-626']['operational']['effect']['durationSeconds'] is None and by['recipe-626']['operational']['effect']['endsAtNextBeneficialLongRest'] is True)
    check('All six healing dice retained, with exactly three actual cure riders',all(c['operational']['effect']['healing']==src[c['recipeId']]['mechanics']['healing'] for c in cards if src[c['recipeId']]['outputType']=='consumable_healing') and {c['recipeId'] for c in cards if c['operational']['effect'].get('independentCureCount')==1}=={'recipe-36','recipe-38','recipe-40'})
    check('Three RP restoration values retain exact recipient/recipe limit',[by[id]['operational']['effect']['rpRestored'] for id in ['recipe-3','recipe-37','recipe-627']]==[1,4,6] and all(by[id]['operational']['effect']['limitKey']=='recipient+recipeId' for id in ['recipe-3','recipe-37','recipe-627']))
    bombs=[c for c in cards if src[c['recipeId']]['outputType']=='thrown_explosive']
    check('Five bomb damage/radius/DC source profiles preserved',len(bombs)==5 and all(all(c['operational']['effect'][k]==src[c['recipeId']]['mechanics'][k] for k in ['damage','damageType','saveDC','radiusFeet']) for c in bombs))
    check('No bomb effect accidentally gains attack roll or object targets',all(c['operational']['effect']['attackRoll'] is False and c['operational']['effect']['objectsAffected'] is False for c in bombs))
    check('Base multi-unit Flawed batches floor yield once',all(c['operational']['craft']['flawed']['mode']=='half-batch-quantity' and c['operational']['craft']['flawed']['quantity']==src[c['recipeId']]['quantity']//2 for c in cards if src[c['recipeId']]['quantity']>=2))
    check('Instantaneous or until-LR singleton Flawed gives no product',all(c['operational']['craft']['flawed']['mode']=='treat-as-Failed' for c in cards if src[c['recipeId']]['quantity']==1 and (src[c['recipeId']]['outputType'] in ['consumable_resonance','consumable_healing','thrown_explosive'] or c['recipeId']=='recipe-626')))
    check('Two-stage immunity Flawed phases both halved',by['recipe-41']['operational']['craft']['flawed']=={'mode':'half-fixed-duration','primarySeconds':43200,'followingResistanceSeconds':1800})
    publictext=(ROOT/'docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    internaltext=(ROOT/'docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    check('Public manuscript headings contain only public IDs',publictext.count('\n## recipe-')==27 and all(('\n## '+c['recipeId']+' — ') in publictext for c in pub['cards']) and all(('\n## '+c['recipeId']+' — ') not in publictext for c in cards if c['visibility']!='public'))
    check('Internal manuscript has all45 headings',internaltext.count('\n## recipe-')==45 and all(('\n## '+c['recipeId']+' — ') in internaltext for c in cards))
    def card_text_matches(text,c):
        section=text.split('\n## '+c['recipeId']+' — ',1)[1].split('\n## recipe-',1)[0]
        return '**Operational effect:** '+c['operational']['text'] in section
    check('All45 internal card effects match operational projection',all(card_text_matches(internaltext,c) for c in cards))
    check('All27 public card effects match operational projection',all(card_text_matches(publictext,c) for c in pub['cards']))
    check('Quality packaging is reserved before outcome with no partial bonus yield',all(c['operational']['craft']['supplementaryInputsReserveTiming']=='before-completion-check' and c['operational']['craft']['postRollPackagingAcquisitionAllowed'] is False and c['operational']['craft']['qualityYieldRequiresFullPackaging'] is True and c['operational']['craft']['partialBonusYieldAllowed'] is False for c in cards))
    check('Three Strength bonuses require direct successful melee attacks',all(by[id]['operational']['effect']['meleeDamagePredicate']=='direct rolled damage of successful melee attack' and by[id]['operational']['effect']['criticalDoublesFlatBonus'] is False and by[id]['operational']['effect']['appliesToIndependentRiders'] is False for id in ['recipe-11','recipe-12','recipe-16']))
    check('Mental initial perception requirement encoded',all(by[id]['operational']['effect']['telepathyRequiresPerception'] is True and by[id]['operational']['effect']['telepathyPerceptionTiming']=='initial-contact-only' for id in ['recipe-24','recipe-27','recipe-626']))
    check('Cure independence and sequence encoded for three real riders',all(by[id]['operational']['effect']['cureTiming']=='after-healing-attempt' and by[id]['operational']['effect']['cureIndependentOfPositiveHpRestoration'] is True and by[id]['operational']['effect']['cureRequiresPresentRemovableEffect'] is True for id in ['recipe-36','recipe-38','recipe-40']))
    check('RP limits do not clear spell pressure or create pools',all(by[id]['operational']['effect']['requiresExistingRpPool'] is True and by[id]['operational']['effect']['cappedAtActualRpMaximum'] is True and by[id]['operational']['effect']['clearsDissonance'] is False and by[id]['operational']['effect']['clearsRefrain'] is False for id in ['recipe-3','recipe-37','recipe-627']))
    check('Immunity tail requires normal expiry',by['recipe-41']['operational']['effect']['followingResistanceTrigger']=='normal-immunity-expiry-only' and by['recipe-41']['operational']['effect']['earlyImmunityEndingTriggersResistance'] is False)
    check('Bomb range measured once to origin without chain detonation',all(c['operational']['effect']['longRangeBandMeasuredToBurstOrigin'] is True and c['operational']['effect']['chainDetonation'] is False for c in bombs))
    check('Summoned recipient is legal but damage bonus never propagates to another creature',all(by[id]['operational']['effect']['propagatesToRecipientsSummons'] is False and by[id]['operational']['effect']['recipientMayBeSummonedCreature'] is True and 'appliesToSummonedCreatureDamage' not in by[id]['operational']['effect'] for id in ['recipe-11','recipe-12','recipe-16']))
    oral=[c for c in cards if c not in bombs]
    check('Forty oral doses return only ordinary spent containers',len(oral)==40 and all(c['operational']['physical']['postUseContainer']['referenceValueCp']==100 and c['operational']['physical']['postUseContainer']['magicalUsesRemaining']==0 and c['operational']['physical']['postUseContainer']['ingredientPropertiesRecovered'] is False and c['operational']['physical']['postUseContainer']['originalIngredientValueRecovered'] is False and c['operational']['physical']['postUseContainer']['reuseRequiresRepurchase'] is False for c in oral))
    check('Five used bombs return no container',all(c['operational']['physical']['postUseContainer'] is None for c in bombs))
    check('No runtime or balance approval claimed',full['runtimeImplemented'] is False and full['balanceApproved'] is False and pub['runtimeImplemented'] is False and pub['balanceApproved'] is False)
    result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','scope':'Source fidelity, visibility, authored-field agreement and independent arithmetic only; no runtime/balance certification.','checkCount':len(checks),'checks':checks}
    (AUDIT/'ALCHEMY_CANDIDATE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[x['name'] for x in checks if not x['pass']]}))
    if result['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
