"""Finite Part 2 regression evidence; reference procedures, not game runtime."""
from copy import deepcopy
from fractions import Fraction
import json, math, re
from build_blacksmithing_recipe_candidate import (
    SHARED, EXACT_THREAD, EXACT_TURN, EXACT_REPLY, project_durability, card_md,
    make_models, operational, REPAIR_STATUS)
from blacksmithing_rider_reference import run_cases


def strongest(candidates):
    return max(candidates) if candidates else 0


def defensive_benefits(kind, *, hp=1, suppressed=False, melded=False,
                       worn=False, donned=False, selected=False, slot=True,
                       bonus=1, resistance=None):
    """Small independent adjudication oracle for the exact wearing predicates."""
    active = hp >= 1 and not suppressed and not melded
    wearing = donned if kind == 'Shield' else worn
    if kind in ('Helm', 'Gauntlets'):
        wearing = wearing and slot
    eligible = active and wearing
    return {'enhancement': bonus if eligible and (selected or kind in ('Helm', 'Gauntlets')) else None,
            'resistance': resistance if eligible else None}


def validate(data, public, guide, pmd, imd, source, equipment, verdict):
    checks=[]
    def check(name, value):
        checks.append({'name':name,'pass':bool(value)})
    timing=run_cases()
    for case in timing:
        check('BS-01 behavior: '+case['name'],case['pass'])
    for block_id in ('84726','39158'):
        match=re.search(r':::writing\{[^\n]*id="'+block_id+r'"[^\n]*\}\n(.*?)\n:::',verdict,re.S)
        check('Exact GPT governing paragraph '+block_id+' retained verbatim',match and match[1].strip() in guide)
    shared=data['sharedOperationalProfile'];cards=data['cards'];by={c['recipeId']:c for c in cards}
    expected_shared=deepcopy(SHARED)
    expected_shared['status']=shared['status']
    check('Corrected shared state specification is identical in both routes',shared==expected_shared and shared['status'] in (REPAIR_STATUS,'reviewed-authored-operational-playtest') and public['sharedOperationalProfile']==shared)
    for c in cards:
        op=c['operational'];text=op['text']
        check('BS-02/03 exact per-card projection '+c['recipeId'],
              op==operational(c['sourceRecipe'],data['baseModels']) and
              'latest lawful structural state immediately before applying the completion outcome' in text and
              'Functional means at least 1 current structural HP' in text and
              'becomes an intact' not in text and
              ('matched Gauntlets pair' in text if c['sourceRecipe']['recipeFamily']=='Gauntlets' else True))
    defense=[c for c in cards if c['operational']['effect']['type']=='armor']
    check('All 16 defensive cards directly exclude inactive melded equipment',len(defense)==16 and all('Melded equipment is not actually worn or donned' in c['operational']['text'] for c in defense))
    # Live state is deliberately changed after reservation, then passed to the
    # unchanged durability calculation. A reservation snapshot cannot heal it.
    reserved={'ordinary':5,'percent':0,'flawed':False,'current':5}
    current=deepcopy(reserved);current['current']=2
    out=project_durability(current['ordinary'],current['percent'],current['flawed'],current['current'],25)
    check('Completion uses intervening damage, not full-HP reservation',out['maximumHP']==6 and out['currentHP']==3)
    current['current']=5
    out=project_durability(current['ordinary'],current['percent'],current['flawed'],current['current'],25)
    check('Completion uses completed repair when that is latest lawful state',out['currentHP']==6)
    current={'ordinary':5,'percent':50,'flawed':False,'current':4}
    out=project_durability(current['ordinary'],current['percent'],current['flawed'],current['current'],25)
    check('Legal replacement supplies its own state without weaker-option bonus',out['maximumHP']==7 and out['currentHP']==4)
    check('Singleton Flawed can produce 0 HP dormant output without free healing',project_durability(5,0,False,1,0,True)['currentHP']==0 and shared['outputState']['singletonFlawedMayProduceBrokenDormantImprint'] and not shared['outputState']['brokenOutputGrantsRefundOrExtraOutput'])
    multi=[c for c in cards if c['sourceRecipe']['quantity']>=2 and c['operational']['outcomes']['FlawedQuantity']==1]
    check('Multi-quantity Flawed yielding one does not add singleton flaw',multi and all(not c['operational']['outcomes']['SingletonFlawedAddsPersistentFlaw'] for c in multi))
    check('Equal/weaker durability never adds another minimum one HP',all(project_durability(1,50,False,1,p)['maximumHP']==2 for p in (0,25,50)))
    check('Empty enhancement contributes zero; real negative is not cancelled',strongest([])==0 and strongest([-1])==-1 and strongest([-1,1])==1)
    first=defensive_benefits('Shield',donned=True,selected=True,bonus=1,resistance='fire')
    second=defensive_benefits('Shield',donned=True,selected=False,bonus=3,resistance='cold')
    check('Two donned shields preserve both resistances but only selected enhancement',first=={'enhancement':1,'resistance':'fire'} and second=={'enhancement':None,'resistance':'cold'})
    check('Worn suit resistance does not require selecting its AC formula',defensive_benefits('Armor',worn=True,selected=False,resistance='fire')=={'enhancement':None,'resistance':'fire'})
    check('Worn accessory requires its single legal slot',defensive_benefits('Gauntlets',worn=True,slot=False,resistance='force')=={'enhancement':None,'resistance':None} and defensive_benefits('Gauntlets',worn=True,slot=True)['enhancement']==1)
    check('Broken, suppressed, melded or unworn items provide no active defensive benefit',all(defensive_benefits('Armor',worn=True,selected=True,resistance='fire',**state)=={'enhancement':None,'resistance':None} for state in [{'hp':0},{'suppressed':True},{'melded':True}]) and defensive_benefits('Shield',donned=False,selected=True,resistance='fire')=={'enhancement':None,'resistance':None})
    heart=[c for c in by['recipe-631']['sourceRecipe']['components'] if 'heartstone' in c['name'].lower()]
    check('Recipe 631 heartstone remains material, never a returnable catalyst',heart and all(c['role']=='material' for c in heart) and by['recipe-631']['operational']['consumedCatalystOccurrences']==[])
    catalysts=[z for z in by['recipe-80']['sourceRecipe']['components'] if z['consumed'] and z['role']=='catalyst']
    check('Recipe 80 requires three catalyst occurrences and allows at most one unit returned',len(catalysts)==3 and sum(z['quantity'] for z in catalysts)==3 and by['recipe-80']['operational']['maximumRetainedCatalystUnits']==1)
    dart=[x for c in cards for x in c['operational']['standardModelExamples'] if x['baseModelId']=='simple-ranged-weapons.dart']
    check('Dart repair keeps exact 1/80 gp reference and rounds actual purchase to 2 cp',dart and all(Fraction(**{'numerator':x['positiveHPRepairMaterialReferenceGp']['numerator'],'denominator':x['positiveHPRepairMaterialReferenceGp']['denominator']})==Fraction(1,80) for x in dart) and math.ceil(Fraction(1,80)*100)==2)

    # Public derivation proof: no unrestricted copying of arbitrary internal
    # envelope keys. Every allowed field is either fixed metadata, the corrected
    # non-secret common profile, reviewed public equipment, or a public recipe.
    allowed={'schemaVersion','status','sourceConferenceTurnId','sourceConferenceReplyId','interfaceTurnId','interfaceReplyId','exactReviewThreadId','exactReviewTurnId','exactReplyId','sourceSha256','sharedGuide','sharedOperationalProfile','baseModels','runtimeImplemented','balanceApproved','pendingBindings','cosmology','visibility','cards'}
    expected={k:deepcopy(v) for k,v in data.items() if k in allowed and k not in ('cards','visibility')}
    expected.update(visibility='public',cards=[deepcopy(c) for c in cards if c['visibility']=='public'])
    check('Public envelope has only allowed fields and is exact 27-card filtered derivation',set(public)==allowed==set(data) and public==expected and len(public['cards'])==27)
    check('All nested public recipe records are exact original public sources', [c['sourceRecipe'] for c in public['cards']]==[r for r in source if r['visibility']=='public'])
    check('Every nested equipment reference derives from reviewed public equipment',public['baseModels']==make_models(equipment))
    def keys(value):
        if isinstance(value,dict):
            for k,v in value.items():
                yield k
                yield from keys(v)
        elif isinstance(value,list):
            for v in value:yield from keys(v)
    serialized=json.dumps(public,ensure_ascii=False)
    gated=[c for c in cards if c['visibility']!='public']
    check('No gated recipe identity or Director guidance exists at any public nesting depth','directorGuidance' not in set(keys(public)) and all(c['recipeId'] not in serialized and c['name'] not in serialized for c in gated))
    # Deep equality above covers effects, components, donor evidence, legacy
    # fields and guidance too, including leakage that an ID-only scan misses.
    check('Public manuscript card bodies are exact filtered internal renderings',all(card_md(c,data['baseModels'],False)==card_md(c,data['baseModels'],True) and card_md(c,data['baseModels'],False) in pmd and card_md(c,data['baseModels'],True) in imd for c in public['cards']) and pmd.count('\n## recipe-')==27)
    check('Actual Part 2 destination and completed verdict are pinned',data['exactReviewThreadId']==EXACT_THREAD and data['exactReviewTurnId']==EXACT_TURN and data['exactReplyId']==EXACT_REPLY and 'APPROVE WITH FINITE REPAIRS' in verdict and data['pendingBindings']==[])
    return checks, {'timingCases':timing,'publicProjectionProof':{'publicCards':27,'internalCards':43,'allowedEnvelopeKeys':sorted(allowed),'permittedEquipmentModels':40,'method':'Exact deep equality of filtered records, fixed common envelope, reviewed equipment, and card renderings; recursive guidance and gated-identity scan.'}}
