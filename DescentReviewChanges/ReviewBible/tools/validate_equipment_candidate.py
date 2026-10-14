"""Check source preservation, exact projections and inventory references."""
from pathlib import Path
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    s=json.loads((ROOT/'data/playtest/equipment_source_catalog.json').read_text(encoding='utf-8'))
    c=json.loads((ROOT/'data/playtest/equipment_acquisition_candidate.json').read_text(encoding='utf-8'))
    e=json.loads((AUDIT/'EQUIPMENT_SOURCE_EVIDENCE.json').read_text(encoding='utf-8'))
    baseline=json.loads((AUDIT/'EQUIPMENT_REVIEW_BASELINE.json').read_text(encoding='utf-8'))
    checks=[]
    def check(label,passed,detail=None):checks.append({'check':label,'passed':bool(passed),'detail':detail})
    check('All 273 source rows and all seven source packs retained',len(s['records'])==273 and len(s['packs'])==7)
    check('Source catalog has unique identifiers',len({x['id'] for x in s['records']})==len(s['records']))
    actual={x['sourceLine']:x for x in s['records']}
    check('Every source table cell remains exact',all(actual[x['line']]['sourceFields']==x['fields'] for t in e['tables'] for x in t['rows']))
    check('Player source byte hash unchanged',sha(GAME/s['source']['path'])==s['source']['sha256'])
    for path,h in baseline['files'].items():check('Protected file '+path,sha(GAME/path)==h)
    check('Candidate binds exact source-catalog bytes',c['sourceCatalogSha256']==sha(ROOT/'data/playtest/equipment_source_catalog.json'))
    ids={x['id']:x for x in c['items']}
    def units(ref):return ref.get('grantedUnits',ref['quantity'])
    check('220 distinct records with 25 explicit additions',len(c['items'])==220 and len(ids)==220 and sum(x['sourceLine'] is None for x in c['items'])==25)
    check('Source item fields unmodified by operational completion',all(x['sourceFields']==actual[x['sourceLine']]['sourceFields'] and x['sourceWeightLb']==actual[x['sourceLine']]['sourceWeightLb'] and x['sourcePriceCp']==actual[x['sourceLine']]['sourcePriceCp'] for x in c['items'] if x['sourceLine'] is not None))
    check('All item weights finite and nonnegative',all(isinstance(x['unitWeightLb'],(int,float)) and math.isfinite(x['unitWeightLb']) and x['unitWeightLb']>=0 for x in c['items']))
    check('No absent source weight silently becomes source zero',all(x['sourceWeightLb'] is None and x['weightProvenance'].startswith('new') for x in c['items'] if x['sourceLine'] is not None and actual[x['sourceLine']]['sourceWeightLb'] is None))
    check('Retail bundle/unit masses and prices reconcile',all(abs(x['unitWeightLb']*x['bundleSize']-x['operationalBundleWeightLb'])<1e-8 and (x['sourcePriceCp'] is None or abs(x['unitPriceCp']*x['bundleSize']-x['sourcePriceCp'])<1e-8) for x in c['items']))
    refrows=[]
    for p in c['packs']:refrows+=p['contents']
    for k in c['classKits']:
        refrows+=k['contents']
        for choice in k['choices']:refrows+=choice['options']
    check('Every pack/class choice references one existing item',all(x['itemId'] in ids and x['quantity']>0 for x in refrows),len(refrows))
    packs={x['id']:x for x in c['packs']}
    check('Seven unique source packs',len(packs)==len(c['packs'])==7)
    check('All pack gross weights count actual contents once',all(abs(p['grossWeightLb']-sum(ids[x['itemId']]['unitWeightLb']*units(x) for x in p['contents']))<1e-8 for p in c['packs']))
    check('Explorer source mass is 59 pounds',packs['pack.explorer']['grossWeightLb']==59)
    check('Priest uses two blocks of incense',sum(x['quantity'] for x in packs['pack.priest']['contents'] if ids[x['itemId']]['name']=='Incense block')==2)
    f=json.loads((ROOT/'data/playtest/character_foundation.json').read_text(encoding='utf-8'))
    check('Every reviewed Base class has exactly one kit',{x['class'] for x in c['classKits']}=={x['class'] for x in f['classes']} and len(c['classKits'])==17)
    for x in f['classes']:check('Preserved class contract '+x['class'],sha(GAME/x['classCandidatePath'])==x['classCandidateSha256'])
    check('Class kits reference valid packs',all(k['packId'] in packs for k in c['classKits']))
    check('Fixed class mass includes source pack once',all(abs(k['fixedWeightBeforeChoicesBackgroundSizingLb']-(packs[k['packId']]['grossWeightLb']+sum(ids[x['itemId']]['unitWeightLb']*units(x) for x in k['contents'])))<1e-8 for k in c['classKits']))
    ammorefs=[x for k in c['classKits'] for x in k['contents'] if ids[x['itemId']]['category']=='Ammunition']
    check('Four kits each grant one twenty-projectile bundle, never twenty bundles',len(ammorefs)==4 and all(x['quantity']==1 and x['grantedUnits']==20 and x['grantedUnits']==x['quantity']*ids[x['itemId']]['bundleSize'] for x in ammorefs))
    filled=['Acid (vial)',"Alchemist's fire (flask)",'Holy water (flask)','Oil (flask)','Potion of healing']
    check('Printed filled consumables have inclusive gross weights',all(x['sourceWeightIncludesContents'] is True for x in c['items'] if x['name'] in filled))
    completed=['Antitoxin (vial)','Ink (1 ounce bottle)','Perfume (vial)','Poison, basic (vial)']
    check('Completed filled weights preserve source null and mark operational contents',all(x['sourceWeightLb'] is None and x['operationalWeightIncludesContents'] is True for x in c['items'] if x['name'] in completed))
    empty=['Glass vial','Crystal vial','Vial',"Alchemist's bottle",'Reinforced flask']
    check('Empty containers are not marked as filled consumables',all(not x.get('sourceWeightIncludesContents') and not x.get('operationalWeightIncludesContents') for x in c['items'] if x['name'] in empty))
    warrior=next(k for k in c['classKits'] if k['class']=='Warrior')
    check('Warrior repair preserves Martial backup eligibility',sum(x['quantity'] for x in warrior['contents'] if ids[x['itemId']]['name']=='Trident')==2 and all(ids[x['itemId']]['name']!='Handaxe' for x in warrior['contents']))
    druid=next(k for k in c['classKits'] if k['class']=='Druid')
    check('Druid actual OR choices remain separate selections',len(druid['choices'])==3 and all(x['choose']==1 and len(x['options'])>1 for x in druid['choices']))
    b=json.loads((ROOT/'data/playtest/ancestry_background_candidate.json').read_text(encoding='utf-8'))['backgrounds']
    bm={x['id']:x for x in c['backgrounds']}
    check('All twenty background source equipment fields remain verbatim',len(bm)==20 and all(bm[x['id']]['sourceEquipment']==x['equipmentSource'] for x in b))
    check('Sidearm permission has exact five identities',{x['name'] for x in c['items'] if 'sidearm' in x['tags']}=={'Dagger','Club','Light hammer','Handaxe','Crossbow, hand'})
    check('Transport stays source-reference scope','Mounts vehicles and services' in c['sourceReferenceOnlyCategories'])
    out={'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','scope':'Source/projection/inventory-reference verification, not semantic approval, numerical balance or runtime execution','checks':checks,'checkCount':len(checks),'failures':[x for x in checks if not x['passed']]}
    (AUDIT/'EQUIPMENT_CANDIDATE_VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':out['status'],'checks':len(checks),'failures':out['failures']},ensure_ascii=False))
    if out['failures']:raise SystemExit(1)

if __name__=='__main__':main()
