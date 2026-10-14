"""Compare Tailoring source versions without treating missing old access data as public."""
from pathlib import Path
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    target=AUDIT/'TAILORING_SOURCE_VERSION_AUDIT.json';assert not target.exists(),'Existing evidence must be inspected.'
    paths={'mechanicalV4':ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json','internalV4':GAME/'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json','v2':GAME/'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json','publicRuntime':GAME/'src/data/crafting-recipes.json'}
    hashes={k:sha(p) for k,p in paths.items()};versions={}
    for k,p in paths.items():
        x=read(p);versions[k]={r['id']:r for r in (x if isinstance(x,list) else x['recipes'])}
    rs=[r for r in versions['mechanicalV4'].values() if r['skill']=='Tailoring'];assert rs==read(AUDIT/'TAILORING_SOURCE_PREPARATION.json')['recipes']
    fields=['name','effects','mechanics','quantity','components','workRequirements','craftingCheck','economy','visibility','discovery']
    comparisons=[];differences=[]
    for r in rs:
        for name,rows in versions.items():
            if name=='mechanicalV4' or r['id'] not in rows:continue
            other=rows[r['id']]
            for field in fields:
                same=(field in r)==(field in other) and r.get(field)==other.get(field)
                comparisons.append({'recipeId':r['id'],'version':name,'field':field,'equal':same})
                if not same:differences.append({'recipeId':r['id'],'version':name,'field':field,'currentFieldPresent':field in r,'currentValue':r.get(field),'otherFieldPresent':field in other,'otherValue':other.get(field)})
    expected_public={r['id'] for r in rs if r['visibility']=='public'}
    actual_public={r['id'] for r in versions['publicRuntime'].values() if r['skill']=='Tailoring'}
    checks={
      'completeCurrent43RecordsPreserved':len(rs)==43,
      'internalV4AndV2ContainAll43Identities':all(all(r['id'] in versions[k] for r in rs) for k in ('internalV4','v2')),
      'publicRuntimeContainsExactly29PublicIdentities':actual_public==expected_public and len(actual_public)==29,
      'onlyDifferencesAre43AbsentV2VisibilityFields':len(differences)==43 and all(d['version']=='v2' and d['field']=='visibility' and not d['otherFieldPresent'] for d in differences),
      'currentEffectsMechanicsComponentsAndWorkAgreeAcrossAvailableVersions':all(c['equal'] for c in comparisons if c['field']!='visibility'),
      'allFourOriginalFilesUnchanged':all(sha(paths[k])==h for k,h in hashes.items())}
    assert all(checks.values()),checks
    tools=[{'recipeId':r['id'],'componentIndex':i,'sourceComponent':c} for r in rs for i,c in enumerate(r['components']) if not c['consumed']]
    assert len(tools)==25 and all(z['sourceComponent']['role']=='tool' for z in tools)
    out={'status':'PASS — source comparison only; no Tailoring operational approval','scope':'Ten named source fields for every available Tailoring identity across three comparison variants; full mechanical originals are separately preserved in TAILORING_SOURCE_PREPARATION.json. This is not live runtime behavior verification.','sourcePaths':{k:p.relative_to(GAME).as_posix() for k,p in paths.items()},'sourceHashes':hashes,'comparisons':comparisons,'fieldComparisons':len(comparisons),'matchingFields':sum(c['equal'] for c in comparisons),'differences':differences,'differenceInterpretation':'V2 lacks visibility fields for all43 records. Missing historical access metadata does not override current V4 visibility or make restricted/Director formulas public. No compared numerical, effect, component, work, economy or discovery discrepancy was found.','nonconsumedToolOccurrences':tools,'toolPriceReferencesGp':dict(Counter(str(z['sourceComponent']['value']) for z in tools)),'checks':checks,'sourceInformationDeleted':0,'recipesApproved':0}
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PASS','fieldComparisons':len(comparisons),'matchingFields':out['matchingFields'],'explainedMissingV2VisibilityFields':len(differences),'nonconsumedToolOccurrences':len(tools),'checks':len(checks)}))
if __name__=='__main__':main()
