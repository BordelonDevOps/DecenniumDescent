"""Preserve Jewelcrafting variant differences before proposing charge rules."""
from pathlib import Path
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    target=AUDIT/'JEWELCRAFTING_SOURCE_VERSION_AUDIT.json';assert not target.exists(),'Inspect existing evidence rather than overwrite.'
    paths={'mechanicalV4':ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json','internalV4':GAME/'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json','v2':GAME/'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json','publicRuntime':GAME/'src/data/crafting-recipes.json'}
    hashes={k:sha(p) for k,p in paths.items()};versions={}
    for k,p in paths.items():
        d=read(p);versions[k]={r['id']:r for r in (d if isinstance(d,list) else d['recipes'])}
    rs=[r for r in versions['mechanicalV4'].values() if r['skill']=='Jewelcrafting'];assert rs==read(AUDIT/'JEWELCRAFTING_SOURCE_PREPARATION.json')['recipes']
    fields=['name','effects','mechanics','quantity','components','workRequirements','craftingCheck','economy','visibility','discovery'];comparisons=[];differences=[]
    for r in rs:
      for version,rows in versions.items():
        if version=='mechanicalV4' or r['id'] not in rows:continue
        other=rows[r['id']]
        for field in fields:
            same=(field in r)==(field in other) and r.get(field)==other.get(field)
            comparisons.append({'recipeId':r['id'],'version':version,'field':field,'equal':same})
            if not same:differences.append({'recipeId':r['id'],'version':version,'field':field,'currentFieldPresent':field in r,'currentValue':r.get(field),'otherFieldPresent':field in other,'otherValue':other.get(field)})
    expected={r['id'] for r in rs if r['visibility']=='public'};actual={r['id'] for r in versions['publicRuntime'].values() if r['skill']=='Jewelcrafting'}
    checks={'all43CurrentRecordsPreserved':len(rs)==43,
      'all43IdentitiesExistInBothHistoricalVariants':all(all(r['id'] in versions[v] for r in rs) for v in ('internalV4','v2')),
      'publicRuntimeExactly26PublicIdentities':actual==expected and len(actual)==26,
      '43AbsentV2VisibilityFieldsAreOnlyDifferences':len(differences)==43 and all(d['version']=='v2' and d['field']=='visibility' and not d['otherFieldPresent'] for d in differences),
      'allOtherComparedFieldsMatch':all(c['equal'] for c in comparisons if c['field']!='visibility'),
      'allFourSourceFilesUnchanged':all(sha(paths[k])==h for k,h in hashes.items())}
    catalysts=[{'recipeId':r['id'],'componentIndex':i,'component':c} for r in rs for i,c in enumerate(r['components']) if c['role']=='catalyst']
    checks['elevenActualConsumedCatalystOccurrencesPreserved']=len(catalysts)==11 and all(c['component']['consumed'] for c in catalysts)
    out={'status':'PASS' if all(checks.values()) else 'FAIL','scope':'Source-field reconciliation only; no charge, slot, physical-body, runtime or effect approval.','sourcePaths':{k:p.relative_to(GAME).as_posix() for k,p in paths.items()},'sourceHashes':hashes,'fields':fields,'comparisons':comparisons,'fieldComparisons':len(comparisons),'matchingFields':sum(c['equal'] for c in comparisons),'differences':differences,'differenceInterpretation':'The43 V2 records lack visibility metadata; absence cannot override the current access boundary. No compared effect, numerical, work, component or economic difference was found.' if all(checks.values()) else 'Inspect every retained difference; do not silently reconcile.','catalystOccurrences':catalysts,'checks':checks,'recipesApproved':0,'sourceInformationDeleted':0}
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':out['status'],'fieldComparisons':len(comparisons),'matchingFields':out['matchingFields'],'differences':len(differences),'catalystOccurrences':len(catalysts),'checks':len(checks)}))
    assert all(checks.values()),checks
if __name__=='__main__':main()
