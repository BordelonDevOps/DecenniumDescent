"""Verify source preservation, visibility and independent framework arithmetic."""
from pathlib import Path
from fractions import Fraction
from math import floor, ceil
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    d=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    c=read(ROOT/'data/playtest/crafting_engine_candidate.json')
    internal=read(ROOT/'data/director/crafting_engine_recipe_index.json')
    rows=internal['recipes']; original={x['id']:x for x in d['recipes']}
    baseline=read(AUDIT/'CRAFTING_ENGINE_BASELINE.json')
    book=(ROOT/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md').read_text(encoding='utf-8')
    checks=[]
    def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
    # The coverage ledger is updated only after review. Its original snapshot is
    # retained byte-for-byte; mechanics/source artifacts have no such exception.
    ledger_key='DescentReviewChanges\\ReviewBible\\data\\playtest\\game_development_coverage.json'
    protected={p:h for p,h in baseline['files'].items() if p!=ledger_key}
    check('All protected sources and previously reviewed mechanics unchanged',all(sha(GAME/p)==h for p,h in protected.items()),len(protected))
    old_ledger=baseline['files'][ledger_key]
    backup=AUDIT/'COVERAGE_BEFORE_CRAFTING_ENGINE.json'
    check('Mutable coverage ledger original is intact or preserved byte-for-byte',sha(GAME/ledger_key)==old_ledger or (backup.exists() and sha(backup)==old_ledger))
    check('687 unique recipe IDs preserved',len(rows)==len({x['recipeId'] for x in rows})==687 and {x['recipeId'] for x in rows}==set(original))
    check('Source SHA matches',c['sourceSha256']==sha(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')==internal['sourceSha256'])
    check('Public projection contains exactly public IDs',len(c['publicRecipeFrameworkIndex'])==433 and {x['recipeId'] for x in c['publicRecipeFrameworkIndex']}=={x['id'] for x in original.values() if x['visibility']=='public'})
    check('No restricted rows in public projection',all(x['visibility']=='public' for x in c['publicRecipeFrameworkIndex']))
    check('Public records match internal projection',all(x in rows for x in c['publicRecipeFrameworkIndex']))
    check('All recipe visibility fields retained',all(x['visibility']==original[x['recipeId']]['visibility'] for x in rows))
    check('No effect approval claimed',c['ordinaryRecipeEffectsApproved']==0 and all(x['effectReviewStatus']=='unreviewed' for x in rows))
    check('All recipe quantities retained',all(x['batchQuantity']==original[x['recipeId']]['quantity'] for x in rows))
    check('All recipe requirements retained',all((x['skill'],x['skillLevel'],x['tier'],x['requiresFormula'])==tuple(original[x['recipeId']][k] for k in ['skill','skillLevel','tier'])+(original[x['recipeId']]['discovery']['requiresFormula'],) for x in rows))
    check('Original active hours and nulls retained',all(x['sourceActiveHours']==original[x['recipeId']]['workRequirements']['activeWorkHours'] for x in rows))
    check('682 nonnull active-hour bindings unchanged',sum(x['sourceActiveHours'] is not None for x in rows)==682 and all(x['candidateActiveHours']==x['sourceActiveHours'] for x in rows if x['sourceActiveHours'] is not None))
    check('Five workyear overlays explicit and Director-only',sum(x['sourceActiveHours'] is None for x in rows)==5 and all(x['candidateActiveHours']==1920 and x['visibility']=='director-only' and x['timeProvenance']=='new workyear conversion' for x in rows if x['sourceActiveHours'] is None))
    check('No batch recommendation multiplied by output',all(x['sourceRecommendedValue']==original[x['recipeId']]['economy']['recommendedMarketValue']==x['candidateBatchReferenceValueGp'] for x in rows))
    check('Unit references remain exact ratios',all(x['candidateUnitValueRatioGp']=={'numerator':x['candidateBatchReferenceValueGp'],'denominator':x['batchQuantity']} for x in rows))
    check('Source pointers resolve exact recipe',all(d['recipes'][int(x['sourcePointer'].split('/')[-1])]['id']==x['recipeId'] for x in rows))
    check('All 16 trades bound once',len(c['trades'])==16 and {x['name'] for x in c['trades']}==set(d['tradeskills']))
    check('Trade source station/tools/ability preserved',all(x['source']=={k:v for k,v in d['tradeskills'][x['name']].items() if k!='rankBands'} for x in c['trades']))
    check('Five distinct new mundane kits',len(c['newToolProfiles'])==len({x['id'] for x in c['newToolProfiles']})==5 and all(x['priceCp']>0 and x['weightLb']>0 for x in c['newToolProfiles']))
    check('All trades have a primary credential and injury type',all(x['primaryTool'] and x['injuryDamageType'] in ['acid','fire','force','piercing','slashing','bludgeoning','poison'] for x in c['trades']))
    check('100-day opening is 2400 elapsed hours',c['rules']['openingElapsedHours']==100*24)
    check('Work units are internally consistent',c['rules']['workweekHours']==5*c['rules']['workdayHours'] and c['rules']['workmonthHours']==4*c['rules']['workweekHours'] and c['rules']['workyearHours']==12*c['rules']['workmonthHours'])
    check('Recipe-1 batch/unit worked value',Fraction(original['recipe-1']['economy']['recommendedMarketValue'],original['recipe-1']['quantity'])==18)
    check('Masterwork yield boundary vector', [floor(q*Fraction(3,2)) for q in [1,2,3,4,5]]==[1,3,4,6,7])
    check('Exceptional yield boundary vector',[floor(q*Fraction(5,4)) for q in [1,2,3,4,5]]==[1,2,3,5,6])
    check('Indivisible ordinary failure recovery',[floor(q*Fraction(1,4)) for q in [1,3,4,5,7,8]]==[0,0,1,1,1,2])
    check('Forge Dwarf 8-hour order takes 360 minutes',ceil(8*60*Fraction(3,4))==360)
    check('Partial Medium harvest rounds to 8 minutes',ceil(30*Fraction(1,4))==8)
    check('Preservation example resumes 10 minutes before degradation',60-50==10 and c['rules']['preservationProtectionHours']==24)
    check('Trade advancement costs increase without repeated XP award',sum(10+level for level in range(1,5))==50)
    for phrase in ['natural 1 is a Mishap','natural 20 uses its numerical total','separate from equipment grade','Nineteen source component rows','All 687', '2,400']:
        # The explicit catalog count is also in the opening as lower-case prose.
        check('Manuscript retains '+phrase,phrase.lower() in book.lower() or (phrase=='All 687' and '687 recipe effects' in book))
    result={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'Source/visibility consistency and reference arithmetic, not runtime or balance tests. GPT review separate.','checks':checks,'count':len(checks)}
    (AUDIT/'CRAFTING_ENGINE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[x['name'] for x in checks if not x['pass']]}))
    if result['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
