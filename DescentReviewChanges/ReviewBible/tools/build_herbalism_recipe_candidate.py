"""Build the Herbalism overlay and cards; original records remain immutable."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
GUIDE='docs/mechanics/HERBALISM_RECIPE_PLAYTEST.md'
INTERNAL='docs/director-only/HERBALISM_INTERNAL_PROCEDURES.md'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def duration(s):
    if 'long rest' in s:return None
    m=re.search(r'(\d+) (minute|hour)',s)
    if not m:raise ValueError(s)
    return int(m[1])*(60 if m[2]=='minute' else 3600)

def main():
    if (ROOT/'docs/mechanics/HERBALISM_REVIEW_STATUS.json').exists():raise SystemExit('Reviewed set exists; refusing draft overwrite.')
    evidence=read(AUDIT/'HERBALISM_SOURCE_EVIDENCE.json')
    src=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    recipes=[r for r in src['recipes'] if r['skill']=='Herbalism']
    assert evidence['recipes']==recipes
    policy=read(AUDIT/'HERBALISM_AUTHORING_DECISIONS.json')
    cards=[]
    for r in recipes:
        m=r['mechanics'];rid=r['id'];q=r['quantity'];family=r['recipeFamily']
        kind='panacea' if family=='Panacea' else 'antidote' if family=='Antidote' else 'hazard-buff' if r['outputType']=='remedy_buff' else 'topical-healing'
        timed=kind in ['antidote','hazard-buff'];secs=duration(r['effects']) if timed else None
        eff={'kind':kind,'sourceTags':r['tags'],'magical':True,'spell':False,'concentration':False,'createsResourcePool':False}
        if kind=='antidote':
            eff.update(poisonedRemoval='all present removable Poisoned applications; underlying independent causes remain',poisonSaveAdvantage=True,numericSaveBonus=0,durationSeconds=secs,endsAtNextBeneficialLongRest=secs is None,conditionCureIndependentOfSaveBuff=True)
            desc='End every present removable Poisoned application, without deleting its independent underlying cause; future exposure may reapply it. Gain advantage on saves against poison '+('until the next completed beneficial Long Rest' if secs is None else f'for {secs//60} elapsed minutes')+'. No added numeric bonus, poison immunity, resistance, disease or intoxication cure.'
        elif kind=='hazard-buff':
            eff.update(hazardTag=m['tag'],checkAndSaveBonus=m['bonus'],scope=deepcopy(policy['hazardScopes'][m['tag']]),durationSeconds=secs,endsAtNextBeneficialLongRest=secs is None,stacking='strongest Herbalism numeric bonus per actual qualifying roll')
            desc=f"Gain +{m['bonus']} on the recipient's own qualifying checks and saves against {m['tag']} hazards "+('until the next completed beneficial Long Rest' if secs is None else f'for {secs//60} elapsed minutes')+'. '+policy['hazardScopes'][m['tag']]['text']+' No attack/damage bonus, automatic resistance, extra save or resource recovery.'
        elif kind=='topical-healing':
            eff.update(healing=m['healing'],operation='ordinary-magical-nonspell-current-HP-healing',localCare=deepcopy(policy['localCare']),woundsRemoved=0)
            desc=f"After one uninterrupted active minute, attempt {m['healing']} ordinary magical nonspell HP healing under actual caps and blockers. "+policy['localCare']['text']
        else:
            eff.update(healing=m['healing'],operation='ordinary-magical-nonspell-current-HP-healing',cure=deepcopy(policy['panacea']['cure']),cooldown=deepcopy(policy['panacea']['cooldown']))
            desc=policy['panacea']['text']
        if q>=2:flaw={'mode':'half-batch-quantity','quantity':q//2,'effectChange':None}
        elif timed and secs is not None:flaw={'mode':'half-fixed-duration','durationSeconds':max(6,(secs//12)*6),'instantCureUnchanged':kind=='antidote'}
        else:flaw={'mode':'treat-as-Failed','quantity':0,'recovery':'framework 25 percent non-catalyst inputs'}
        mass=sum(Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed'])
        cat=max((Fraction(str(c['weight'])) for c in r['components'] if c['consumed'] and c['role']=='catalyst'),default=Fraction(0))
        maximum=q*3//2
        physical={'compoundWeightLb':0.1,'containerWeightLb':0.1,'grossWeightLb':0.2,'containerAC':13,'containerHP':1,'doses':1,'vialSlots':1,'classification':'magical-nonspell-consumable; no default artifact status','sealedShelfLife':'indefinite while intact in ordinary conditions','openedLifetimeSeconds':3600,'postUseContainer':{'kind':'ordinary-spent-dose-vial','weightLb':0.1,'AC':13,'capacityDoses':1,'actualCurrentAndMaxHpRetained':True,'magicalUsesRemaining':0,'ingredientTierBenefit':None,'ingredientPropertiesRecovered':False,'originalIngredientValueRecovered':False,'referenceValueCp':100,'supplementaryPackagingReuseIfIntact':True,'reuseRequiresRepurchase':False}}
        minutes=10 if kind=='panacea' else 1 if kind=='topical-healing' else 0
        activation={'action':'continuous active application' if minutes else 'Action','activeMinutes':minutes,'consecutiveRegularTurnActions':minutes*10 if minutes else 1,'requiresElapsedTimeAndActions':bool(minutes),'availableHands':1,'recipientRangeFeet':5,'delivery':'topical touch' if minutes else 'drink or feed','recipientConsent':'willing or Incapacitated; actual anatomical compatibility required','doseCommit':'legal administration start','interruptionRefund':False,'recipientIdentityLocked':True,'spellRank':None,'school':None}
        craft={'batchQuantity':q,'sourceVesselUnits':0,'additionalStandardGlassVials':q,'additionalExceptionalGlassVials':q*5//4,'additionalMasterworkGlassVials':maximum,'extraPackagingItemId':'alchemical-containers.glass-vial','extraPackagingUnitCp':100,'packagingAndCarrierReservedBeforeCheck':True,'postRollAcquisitionAllowed':False,'sourceConsumedMassLb':float(mass),'maximumReturnedCatalystMassLb':float(cat),'minimumAvailableCompoundMassLb':float(mass-cat),'masterworkSupplementaryCarrierLb':float(max(Fraction(0),Fraction(maximum,10)-(mass-cat))),'firstStabilizationPhaseMinutes':15,'firstPhaseIncludedInTotal':True,'flawed':flaw,'qualityPotencyBonus':False,'qualityDurabilityOption':{'batchQuantity':'Standard','allFinishedContainersMaxAndCurrentHP':2,'bonusYieldCombined':False}}
        cards.append({'recipeId':rid,'name':r['name'],'visibility':r['visibility'],'status':'draft-awaiting-GPT-exact-review','sourceSha256':evidence['sourceSha256'],'sourceRecipeIndex':evidence['sourceIndices'][rid],'sourceEffect':r['effects'],'sourceMechanics':deepcopy(m),'sourceLegacyFields':{k:deepcopy(r[k]) for k in ['legacyName','legacyEffect'] if k in r},'sourceRequirements':{k:deepcopy(r[k]) for k in ['skill','skillLevel','difficulty','tier','rarity','quantity','craftingTime','workRequirements','craftingCheck','discovery','components','economy','skillProgression']},'operational':{'text':desc,'effect':eff,'activation':activation,'physical':physical,'craft':craft,'value':{'sourceStandardBatchReferenceGp':r['economy']['recommendedMarketValue'],'unitReferenceGp':{'numerator':r['economy']['recommendedMarketValue'],'denominator':q},'extraPackagingIncludedInSourceCost':False},'sharedRules':GUIDE,'privateRules':INTERNAL if kind=='panacea' else None}})
    envelope={'schemaVersion':1,'status':'draft-awaiting-GPT-exact-review','sourceSha256':evidence['sourceSha256'],'sharedRules':GUIDE,'sourceConferenceTurnId':policy['sourceConferenceTurnId'],'runtimeImplemented':False,'balanceApproved':False}
    dump(ROOT/'data/playtest/herbalism_recipe_candidate.json',{**envelope,'visibility':'public','cards':[c for c in cards if c['visibility']=='public']})
    dump(ROOT/'data/director/herbalism_recipe_candidate_internal.json',{**envelope,'visibility':'director-internal','cards':cards})
    for public,path in [(True,ROOT/'docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md'),(False,ROOT/'docs/director-only/HERBALISM_INTERNAL_RECIPE_CARDS.md')]:
        selected=[c for c in cards if c['visibility']=='public'] if public else cards
        link='HERBALISM_RECIPE_PLAYTEST.md' if public else '../mechanics/HERBALISM_RECIPE_PLAYTEST.md'
        out=['# Herbalism '+('public' if public else 'Director internal')+' recipe cards','','**Draft awaiting exact GPT review.** '+('29 public formulas.' if public else 'All 45 formulas: 29 public, three restricted and 13 Director-only. Keep this file internal.'),'',f'Use the [shared procedures]({link}) with every card. Original fields remain in the JSON and source evidence. Names do not grant equipment grades or additional powers. Prices below refer to an entire Standard batch and need an actual buyer/supplier quote.','']
        for c in selected:
            req=c['sourceRequirements'];op=c['operational'];cr=op['craft']
            out += ['## '+c['recipeId']+' — '+c['name'],'',f"**Source:** {c['visibility']}; Herbalism level {req['skillLevel']}; tier {req['tier']}; {req['rarity']}; DC {req['difficulty']}; {req['workRequirements']['activeWorkHours']} active hours; {req['quantity']} doses. Standard batch reference {req['economy']['recommendedMarketValue']} gp.",'','**Preserved effect:** '+c['sourceEffect'],'','**Operational effect:** '+op['text'],'',
                '**Administration:** '+(f"{op['activation']['activeMinutes']} uninterrupted active minute(s), requiring {op['activation']['consecutiveRegularTurnActions']} consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available." if op['activation']['activeMinutes'] else 'Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet.')+' Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.','',
                '**Work:** '+req['workRequirements']['station']+'; '+', '.join(req['workRequirements']['requiredTools'])+f". Mode {req['workRequirements']['timeMode']}; field flag {str(req['workRequirements']['fieldCraftable']).lower()}; up to {req['workRequirements']['maximumAssistants']} assistants; formula required {str(req['discovery']['requiresFormula']).lower()}.",'',
                '**Exact ingredients:** '+'; '.join(f"{x['quantity']} × {x['name']} (component tier {x['tier']}; {x['weight']} lb/unit; {x['value']} gp/unit; {x['role']}; {'consumed' if x['consumed'] else 'returned'})" for x in req['components'])+'.','',
                f"**Packaging:** no source vessels. Reserve {cr['additionalStandardGlassVials']} actual Glass vials for Standard output; {cr['additionalExceptionalGlassVials']} for Exceptional yield; {cr['additionalMasterworkGlassVials']} for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve {cr['masterworkSupplementaryCarrierLb']:g} lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.",'',
                '**Flawed:** '+json.dumps(cr['flawed'],ensure_ascii=False)+'. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.','',
                '**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.','']
            if op['privateRules']:out+=['**Director procedure:** [Panacea recipient limit and cure order](HERBALISM_INTERNAL_PROCEDURES.md).','']
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text('\n'.join(out),encoding='utf-8')
    print(json.dumps({'status':'draft','cards':len(cards),'public':sum(c['visibility']=='public' for c in cards)}))

if __name__=='__main__':main()
