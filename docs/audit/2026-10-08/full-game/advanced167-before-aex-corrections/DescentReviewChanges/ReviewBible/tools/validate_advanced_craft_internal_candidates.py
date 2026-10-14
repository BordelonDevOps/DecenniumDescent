"""Independent source/field/manuscript and finite arithmetic validation.

No application runtime, campaign-world authentication or balance claim.
The full state-sequence review and public-envelope validation remain separate.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
import hashlib
import json
import math
import re
import zipfile

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
V = A/'advanced167-source-authoring-reviewer-files'


def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(r): return F(r['numerator'], r['denominator'])


def main():
    checks = []
    def ck(n, ok, detail=None):
        checks.append({'name':n, 'pass':bool(ok), **({'detail':detail} if detail is not None else {})})
    candidate = R/'data/director/advanced_craft_recipe_candidate_internal.json'
    d = load(candidate); cards = d['cards']; byid = {c['recipeId']:c for c in cards}
    source = load(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes']
    smap = {r['id']:r for r in source}
    preparation = load(A/'ADVANCED_CRAFT_SOURCE_PREPARATION.json')
    register = load(V/'ADVANCED_167_AUTHORING_REGISTER.json'); rows = {r['recipeId']:r for r in register['recipes']}
    bs = register['bodyProfiles']; minutes623 = 115200
    ck('Exact original167 unique membership',len(cards)==167 and set(byid)==set(rows))
    ck('Four trade counts',Counter(c['sourceRecipe']['skill'] for c in cards)=={'Enchanting':43,'Rune Carving':41,'Scribing':40,'Tinkering':43})
    ck('Audience counts',Counter(c['visibility'] for c in cards)=={'public':100,'restricted':7,'director-only':60})
    ck('No exact approval or runtime/balance claim',d['exactRecipeApproval'] is False and d['runtimeImplemented'] is False and d['balanceApproved'] is False)
    ck('Final authority',d['sourceVerdictSha256']==sha(A/'GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md')=='48f885becd03e4a99ba8d6243ce286c1e1e88cfefc776af9ff89a9182c79c8e0')
    ck('Complete version and name differences',d['versionAudit']==preparation['versionAudit'] and d['sourceNameCorrespondences']==preparation['sourceNameCorrespondences'])
    docx = G/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    with zipfile.ZipFile(docx) as z:
        xml = ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    bookparas = [''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:body//w:p',ns)]
    manuscripts = {t:(R/f"docs/director-only/{t.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md").read_text(encoding='utf-8') for t in ['Enchanting','Rune Carving','Scribing','Tinkering']}
    allcases=[]
    for c in cards:
        id=c['recipeId']; s=smap[id]; x=rows[id]; o=c['operational']; w=o['work']; q=s['quantity']
        creature=o['profile'] in ['TI-automaton','TI-drone']
        ck(id+':whole original source and source index',c['sourceRecipe']==s and source[c['sourceRecipeIndex']]==s)
        canonical=json.dumps(s,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        ck(id+':canonical original hash',c['sourceObjectSha256']==hashlib.sha256(canonical).hexdigest())
        ck(id+':complete original authoring binding',c['sourceAuthoringRegister']==x and o['useBinding']==x['authoredUseBinding'])
        ck(id+':body choices and all maximum reserves',o['bodyModelIds']==x['bodyChoices'] and o['maximumOrderedBodyReserve']==math.floor(F(3*q,2)))
        ck(id+':preserved check/access/discovery/progression',w['DC']==s['craftingCheck']['targetDC'] and w['sourceRequirements']==s['workRequirements'] and w['sourceDiscovery']==s['discovery'] and w['sourceSkillProgression']==s['skillProgression'])
        wanted=minutes623 if id=='recipe-623' else F(str(s['workRequirements']['activeWorkHours']))*60
        ck(id+':source null and operational hours',w['sourceActiveHours']==s['workRequirements']['activeWorkHours'] and w['activeMinutes']==wanted and w['forgeDwarfActiveMinutes']==math.ceil(wanted*F(3,4)))
        ck(id+':included phases',w['includedFirstPhaseMinutes']+w['remainingActiveMinutes']==wanted and w['dwarfIncludedFirstPhaseMinutes']+w['dwarfRemainingActiveMinutes']==w['forgeDwarfActiveMinutes'] and w['includedFirstPhaseMinutes']==min(15,wanted) and w['laterPhaseMaximumMinutes']==480)
        ck(id+':no field creation or invented ability',w['sourceRequirements']['fieldCraftable'] is False and w['ability']=='Intelligence' and s['craftingCheck']['abilityOptions']==['Intelligence'])
        expected={'Mishap':0,'Failed':0,'Flawed':q//2 if q>1 else int(not creature),'Standard':q,'Exceptional':q*5//4,'Masterwork':q*3//2}
        for band,n in expected.items():
            ck(id+':output '+band,o['creation']['sixBands'][band]==n)
            allcases.append({'recipeId':id,'band':band,'yield':n,'structuralAlternativeQuantity':q if band in ['Exceptional','Masterwork'] else None,'creatureStructuralImprovement':False if creature else None})
        ck(id+':creature/singleton quality exception',o['creatureOutput']==creature and o['creation']['singletonFlawedMapsToFailed']==(creature and q==1) and o['creation']['singletonFlawedAddsPersistentStructuralFlaw']==(not creature and q==1))
        ck(id+':no critical20 shift',o['creation']['naturalOneIsMishap'] is True and o['creation']['naturalTwentyShiftsBand'] is False)
        ck(id+':component occurrence count',len(o['componentOccurrences'])==len(s['components']))
        bulk={'Enchanting':{'Veilthread'},'Rune Carving':{'Runic ink','Binding agent'},'Scribing':{'Ink','Preservation treatment'},'Tinkering':set()}[s['skill']]
        for i,comp in enumerate(s['components']):
            oc=o['componentOccurrences'][i]
            ck(id+f':occurrence{i} original and roles',oc['index']==i and oc['sourceComponent']==comp and oc['masterworkCatalystEligible']==(comp['consumed'] and comp['role']=='catalyst') and oc['consumedTool']==(comp['consumed'] and comp['role']=='tool') and oc['retainedTool']==(not comp['consumed'] and comp['role']=='tool'))
            ck(id+f':occurrence{i} failure precision',frac(oc['defaultFailurePrecision'])==(F(1,100) if comp['name'] in bulk else 1) and oc['failedRecoveryEligible']==(comp['consumed'] and comp['role']!='catalyst'))
        for variant in o['bodyVariants']:
            bid=variant['bodyModelId']; b=bs[bid]; v=F(str(s['economy']['recommendedMarketValue']))/q+F(str(b['priceGp']))
            ref=next(z for z in o['references'] if z['body']==bid)
            ck(id+':'+bid+' exact prices',frac(ref['finishedReferenceGp'])==v and frac(variant['functionalRepair']['materialReferenceGp'])==F(str(b['priceGp']))/4 and frac(variant['brokenReconstruction']['materialReferenceGp'])==v/4)
            hp=x['authoredUseBinding']['hitPoints'] if creature else b['HP']
            ck(id+':'+bid+' repair durations use actual creature/body maximum',frac(variant['functionalRepair']['defaultMaxHPHours'])==max(1,F(hp,10)) and frac(variant['brokenReconstruction']['defaultMaxHPHours'])==max(8,F(hp,10)))
            if 'servicing' in variant:
                service=variant['servicing']; required_mass=max(F(1,100),F(str(b['massLb']))/100)
                rounded_mass=F(math.ceil(required_mass*100),100)
                ck(id+':'+bid+' finite maintenance pack',frac(service['packGp'])==F(str(b['priceGp']))/10 and frac(service['packMassLb'])==rounded_mass and service['activeMinutes']==60 and service['DC']==10 and service['restoresPrintedMaximum']==s['mechanics']['charges'] and service['restoresHP'] is False)
        if creature:
            ck(id+':no structural creature improvement',all(v['unflawedStructuralMaximumByChoice'] is None for v in o['bodyVariants']) and o['creation']['structuralAlternativePercent']==[])
        ps=o['paragraphs']; doc=manuscripts[s['skill']]
        ck(id+':complete manuscript exactly in trade document',doc.count(c['manuscriptText'])==1)
        ck(id+':every actual operational paragraph rendered',all(('**'+p['label']+'**\n\n'+p['text']+'\n') in c['manuscriptText'] for p in ps) and len({p['label'] for p in ps})==len(ps))
        ck(id+':required procedures exist',all(k in d['procedureSections'] for k in o['requiredSharedSections']))
        if c['visibility']=='public':
            bind=c['publicBookBinding'];ck(id+':six actual book paragraphs',bind is not None and len(bind['paragraphs'])==6 and all(bookparas[p['index']]==p['text'] for p in bind['paragraphs']))
        else:
            ck(id+':private has no invented book binding',c['publicBookBinding'] is None)
    tk=load(R/'data/public/class_playtests/tinker.json')['cards']; tm=d['tinkerInterfaceRegister']['cards']
    ck('48 exact complete class-card interfaces',len(tm)==48 and {c['id'] for c in tm}=={c['id'] for c in tk} and all(c['sourceCard']==next(z for z in tk if z['id']==c['id']) for c in tm))
    ck('22 exact body defaults/variants',len(d['bodyModels'])==22 and all(b['sourceAuthoringProfile']==bs[k] for k,b in d['bodyModels'].items()))
    ck('15 public body dependencies',{k for c in cards if c['visibility']=='public' for k in c['operational']['bodyModelIds']}==set(register['publicBodyDependencyIds']))
    ck('Precise six consumed tools',[(c['recipeId'],o['index']) for c in cards for o in c['operational']['componentOccurrences'] if o['consumedTool']]==[('recipe-637',1),('recipe-639',3),('recipe-673',3),('recipe-685',2),('recipe-686',2),('recipe-687',4)])
    correction=next(x for x in d['controllingCorrections'] if x['id']=='ADV-EDIT-01')
    ck('Actual completed trap correction bound',correction['sha256']==sha(G/correction['file']) and correction['replyId']=='a01ad150-d04b-4fb8-ae18-9ea476535a93' and d['openExactReviewIssues']==[])
    traps=[c for c in cards if c['operational']['profile']=='TI-trap']
    ck('All11 trap manuscripts contain controlling spring correction',len(traps)==11 and all(correction['rule'] in c['manuscriptText'] for c in traps))
    ck('Historical body source unchanged; corrected operational primary explicit',d['bodyModels']['TI-trap']['sourceAuthoringProfile']==bs['TI-trap'] and 'captive spring/actuation member' in d['bodyModels']['TI-trap']['operationalPrimaryRule'] and 'replaceable only with actual compatible stock' in d['bodyModels']['TI-trap']['operationalPrimaryRule'])
    ck('Corrected AC09 does not waive automaton primaries','missing model-designated primary frame/actuator' in d['procedureSections']['AC-09']['controllingText'] and 'Original-actuator requirements for automaton chassis and other bodies are unchanged.' in correction['rule'])
    ck('172 catalysts and90 retained tools',sum(z['masterworkCatalystEligible'] for c in cards for z in c['operational']['componentOccurrences'])==172 and sum(z['retainedTool'] for c in cards for z in c['operational']['componentOccurrences'])==90)
    eq=load(R/'data/playtest/equipment_acquisition_candidate.json')['items']
    for key,h in d['enchantingHostModels'].items():
        e=next(e for e in eq if e['id']==key)
        ck('Host '+key+':source/economy',h['sourceEquipmentRecord']==e and frac(h['ordinaryPriceGp'])==F(str(e['unitPriceCp']))/100 and h['ordinaryWeightLb']==e['unitWeightLb'])
        ck('Host '+key+':genuine weapon/suit',e.get('group') in ['Light Armor','Medium Armor','Heavy Armor'] or (e['category'].endswith('weapons') and bool(re.search(r'\d',e['sourceFields'].get('Damage','')))))
    # Independently fixed expectations from named worked examples, reading actual card data.
    ck('W01 candidate reserve/default finished value',byid['recipe-121']['operational']['maximumOrderedBodyReserve']==6 and frac(byid['recipe-121']['operational']['references'][0]['finishedReferenceGp'])==F('89.75'))
    ck('W08 source nulls and authored one-year overlay',byid['recipe-623']['sourceRecipe']['workRequirements']['activeWorkHours'] is None and byid['recipe-623']['sourceRecipe']['economy']['laborValue']==0 and byid['recipe-623']['operational']['work']['activeMinutes']==115200 and byid['recipe-623']['operational']['work']['forgeDwarfActiveMinutes']==86400 and frac(byid['recipe-623']['operational']['references'][0]['finishedReferenceGp'])==350108)
    ck('W09 rank8 two lifetime cast starts',byid['recipe-505']['operational']['useBinding']['maximumSpellRank']==8 and byid['recipe-505']['operational']['useBinding']['lifetimeActivations']==2)
    ck('W13 immutable684 attack/HP/service',byid['recipe-684']['operational']['useBinding']['attack']=={'bonus':5,'dice':'3d6','damageType':'force','reachFeet':5,'attackKind':'melee nonspell magical attack','abilityDamage':0} and byid['recipe-684']['operational']['useBinding']['hitPoints']==40 and byid['recipe-684']['operational']['useBinding']['serviceMaximum']==3)
    sensor=byid['recipe-685']['operational']['bodyVariants'][0]['servicing']
    ck('W15 sensor2gp0.02lb',frac(sensor['packGp'])==2 and frac(sensor['packMassLb'])==F('.02'))
    ck('W17 default breachDC28 separate attack+6',byid['recipe-687']['operational']['useBinding']['magicalBreachDefaultDC']==28 and byid['recipe-687']['operational']['useBinding']['attackBonus']==6)
    for path,h in load(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes'].items():
        ck('Protected source unchanged:'+path,sha(G/path)==h)
    report={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL', 'checkedAtUtc':datetime.now(timezone.utc).isoformat(),
            'scope':'Independent complete-source/book preservation, actual manuscript equality, source-bound candidate fields, six-band output arithmetic and fixed named-boundary values. Not state-sequence/runtime, public-envelope, world or balance validation.',
            'candidateSha256':sha(candidate), 'recipes':167, 'checks':len(checks), 'failed':[c for c in checks if not c['pass']],
            'manufacturingOutcomeRows':len(allcases), 'exactApprovalsGranted':0, 'publicProjectionValidated':False,
            'stateSequenceValidationComplete':False, 'results':checks}
    (A/'ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (A/'ADVANCED_CRAFT_INTERNAL_MANUFACTURING_OUTCOMES.json').write_text(json.dumps({'scope':'All167 six-band authored yield values; no actual campaign work-order evidence','cases':allcases},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False,indent=2))
    if report['failed']:raise SystemExit(1)


if __name__=='__main__':main()
