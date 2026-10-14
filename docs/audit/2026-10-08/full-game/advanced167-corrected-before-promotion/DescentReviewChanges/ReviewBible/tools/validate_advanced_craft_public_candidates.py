"""Validate the actual whole player envelope, not only matching effect strings."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
from collections import Counter
import json
import re
import hashlib

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    pp=R/'data/crafting/advanced_craft_recipe_candidate_public.json';p=load(pp)
    ip=R/'data/director/advanced_craft_recipe_candidate_internal.json';d=load(ip)
    full={c['recipeId']:c for c in d['cards']};public={k:c for k,c in full.items() if c['visibility']=='public'}
    materials=load(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['materials']
    checks=[]
    def ck(n,b):checks.append({'name':n,'pass':bool(b)})
    ck('Exactly100 public source members',len(p['cards'])==100 and {c['recipeId'] for c in p['cards']}==set(public))
    ck('No exact promotion/runtime/balance',all(p[k] is False for k in ['exactRecipeApproval','runtimeImplemented','balanceApproved']))
    source_keys={'id','name','skill','skillLevel','difficulty','difficultyBand','craftingTime','rarity','quantity','tags','recipeFamily','outputType','effects','mechanics','workRequirements','craftingCheck','discovery','economy','skillProgression','tier','visibility','knowledgeStatus','publicAvailability','components'}
    mechanical_keys=['profile','useBinding','bodyModelIds','standardQuantity','maximumOrderedBodyReserve','work','creation','references','creatureOutput','sourceStandardBatchReferenceGp','sourceProcessUnitReferenceGp','bodyVariants']
    documents=[]
    for t in ['Enchanting','Rune Carving','Scribing','Tinkering']:
        path=R/f"docs/mechanics/{t.upper().replace(' ','_')}_CANDIDATE_RECIPE_CARDS.md";documents.append((path,path.read_text(encoding='utf-8')))
    docs={t:text for t,(_,text) in zip(['Enchanting','Rune Carving','Scribing','Tinkering'],documents)}
    for c in p['cards']:
        id=c['recipeId'];original=public[id];s=original['sourceRecipe'];projected=c['sourceRecipe'];o=c['operational']
        ck(id+':explicit source field envelope',set(projected)==(set(s)&source_keys) and all(projected[k]==s[k] for k in projected if k!='components'))
        ck(id+':mechanical overlay remains equal',all(o[k]==original['operational'][k] for k in mechanical_keys))
        ck(id+':complete six paragraph book binding',c['publicBookBinding']==original['publicBookBinding'] and len(c['publicBookBinding']['paragraphs'])==6)
        ck(id+':every component mention preserved',len(projected['components'])==len(s['components']) and len(o['componentOccurrences'])==len(s['components']))
        for i,sc in enumerate(s['components']):
            actual=projected['components'][i];expected={k:sc[k] for k in ['name','quantity','role','consumed']}
            matches=[m for m in materials if m['name'].casefold()==sc['name'].casefold() and all(m.get(k)==sc.get(k) for k in ['tier','value','weight'])]
            if len(matches)==1 and matches[0].get('visibility')=='public':
                m=matches[0];expected['publicMaterialProfile']={k:m[k] for k in ['name','tier','rarity','category','value','weight','properties'] if k in m}
            ck(id+f':component{i} independently reconstructed public envelope',actual==expected)
            oc=o['componentOccurrences'][i];ic=original['operational']['componentOccurrences'][i]
            keys={'index','retainedTool','consumedTool','masterworkCatalystEligible','failedRecoveryEligible','defaultFailurePrecision','precisionCondition','physicalIdentityMustRemainDistinct'}
            ck(id+f':component{i} operation without hidden source object',set(oc)==keys|{'componentMention'} and oc['componentMention']==expected and all(oc[k]==ic[k] for k in keys))
        ck(id+':actual manuscript present once',docs[s['skill']].count(c['manuscriptText'])==1)
        ck(id+':every paragraph exactly rendered',all(('**'+x['label']+'**\n\n'+x['text']+'\n') in c['manuscriptText'] for x in o['paragraphs']))
        ck(id+':all book prose rendered',all(f"Paragraph {x['index']}: {x['text']}" in c['manuscriptText'] for x in c['publicBookBinding']['paragraphs']))
        ck(id+':only internal history paragraph omitted',len(o['paragraphs'])==len(original['operational']['paragraphs'])-1 and all(x['label']!='Internal source history' for x in o['paragraphs']))
        ck(id+':player links only',o['guide']==p['guide'] and o['bodyGuide']==p['bodyGuide'] and 'director-only/' not in c['manuscriptText'])
    body_ids={bid for c in public.values() for bid in c['operational']['bodyModelIds']}
    ck('Exactly15 required public body variants',len(body_ids)==15 and set(p['bodyModels'])==body_ids)
    for bid,b in p['bodyModels'].items():
        src=d['bodyModels'][bid];raw=src['sourceAuthoringProfile']
        ck(bid+':original finite body statistics',all(b[k]==raw[k] for k in ['id','priceGp','massLb','HP','AC','dimensionsIn','material']))
        ck(bid+':correct actual model and primary',b['model']==src.get('operationalModelDescription',raw['model']) and b['primary']==src.get('operationalPrimaryRule',raw['primary']))
        ck(bid+':body prose visibly included',b['bodyText'] in p['bodyGuideText'] and b['primary'] in p['bodyGuideText'])
    ck('All50 host source profiles preserved',p['enchantingHostModels']==d['enchantingHostModels'] and len(p['enchantingHostModels'])==50)
    for key,h in p['enchantingHostModels'].items():
        ck(key+':actual host in player catalogue',key in p['bodyGuideText'] and h['sourceEquipmentRecord']['name'] in p['bodyGuideText'])
    ck('Whole operating guide exactly embedded',p['operatingGuideText']==(R/p['guide']).read_text(encoding='utf-8'))
    ck('Whole body guide exactly embedded',p['bodyGuideText']==(R/p['bodyGuide']).read_text(encoding='utf-8'))
    envelopes=[('public JSON',pp.read_text(encoding='utf-8'))]+[(path.relative_to(R).as_posix(),text) for path,text in documents]+[(p['guide'],p['operatingGuideText']),(p['bodyGuide'],p['bodyGuideText'])]
    private_ids=set(full)-set(public);private_bodies=set(d['bodyModels'])-body_ids
    # Exact source IDs/model memberships are forbidden anywhere in the complete public envelope.
    for name,text in envelopes:
        ck(name+':no private recipe membership',not (set(re.findall(r'recipe-\d+',text))&private_ids))
        ck(name+':no private body identifiers',not any(b in text for b in private_bodies))
        ck(name+':no internal path', 'director-only/' not in text and 'data/director/' not in text)
    forbidden={'sourceMonsters','dropRate','dropQuantity','legacyName','legacyEffect','matrixResearch','directorGuidance','wholeCreatureUse','sourceComponent','sourceAuthoringRegister','sourceRecipeIndex','privateOnlyBodyDependencyIds'}
    illegal=[]
    def walk(v,path='$'):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in forbidden:illegal.append(path+'.'+k)
                walk(x,path+'.'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,f'{path}[{i}]')
    walk(p);ck('Recursive envelope contains no donor/private/source-register fields',not illegal)
    # Required player operation must not disappear with private metadata.
    required=['fieldCraftable=false','Language Insight','0.01','Typed Guard','Typed Pulse','Charged Strike','06:00','Snap Rebuild','Overload Suppression','six unspent','per numbered round','two-active-work-Watch']
    for term in required:ck('Player operating dependency: '+term,term in p['operatingGuideText'])
    ck('Complete controlling spring rule is in player guide',d['controllingCorrections'][0]['rule'] in p['operatingGuideText'])
    ledger=load(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json')
    excluded=[e for e in ledger['entries'] if e.get('publicCardIncluded') is False]
    ck('Every withheld recipe has internal disposition',len(excluded)==67 and {x['recipeId'] for x in excluded}==private_ids)
    ck('Projection ledger binds current actual internal candidate',ledger['internalCandidateSha256']==sha(ip))
    protected=load(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
    ck('All138 source inputs unchanged',len(protected)==138 and all(sha(G/path)==h for path,h in protected.items()))
    report={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checkedAtUtc':datetime.now(timezone.utc).isoformat(),
            'scope':'Independent reconstruction of every public source/component occurrence; equal active mechanical fields; actual complete public manuscript/guide/body envelope and recursive withheld-field checks. Not exhaustive semantic prose, runtime, state-sequence or balance validation.',
            'checks':len(checks),'failed':[c for c in checks if not c['pass']], 'illegalKeys':illegal,
            'publicRecipes':100,'bookParagraphs':600,'publicBodies':15,'publicCandidateSha256':sha(pp),'internalCandidateSha256':sha(ip),'newApprovals':0,'results':checks}
    (A/'ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False,indent=2))
    if report['failed']:raise SystemExit(1)


if __name__=='__main__':main()
