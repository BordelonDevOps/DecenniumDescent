"""Preserve full operative sources omitted from Bestiary V3; never run supplied code."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, zipfile

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
ROOT=A/'bestiary-linked-recipe-dependencies-91'
OUT=A/'BESTIARY_LINKED_RECIPE_DEPENDENCIES_91_PREPARATION.json'
ZIP=A/'DD_Bestiary_Linked_Recipe_Dependencies_91.zip'
SAVED=A/Path(__file__).name
for p in (ROOT,OUT,ZIP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
checks=[]
def ck(name,cond):checks.append({'check':name,'pass':bool(cond)});assert cond,name
source=A/'BESTIARY_CRAFTING_CROSSLINK_AUDIT.json'
audit=j(source);bible_path=R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';bible=j(bible_path)
root_recipes=bible['recipes'];rows=[];paths=[source,bible_path,R/'data/director/crafting_recipe_review_catalog.json']
paths += [R/'docs/mechanics'/n for n in ['CRAFTING_HARVEST_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','BODY_EQUIPMENT_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md']]
original_zip=A/'DD_Bestiary_Complete_Source_Prepared_v3_81.zip'
with zipfile.ZipFile(original_zip) as z:original_members=set(z.namelist())
for trade,rid in [('fishing','recipe-173'),('cooking','recipe-92')]:
 prefix=trade.upper()
 manifest_path=R/f'docs/mechanics/{prefix}_REVIEW_STATUS.json';manifest=j(manifest_path)
 candidate_path=R/f'data/playtest/{trade}_recipe_candidate.json';candidate=j(candidate_path)
 guide_path=R/f'docs/mechanics/{prefix}_RECIPE_PLAYTEST.md'
 cards_path=R/f'docs/mechanics/{prefix}_PUBLIC_RECIPE_CARDS.md'
 paths.extend([manifest_path,candidate_path,guide_path,cards_path])
 # Verify the full exact-review bindings, including private artifacts by hash only.
 for rel,digest in manifest['artifactHashes'].items():ck('Exact '+prefix+' review artifact unchanged: '+rel,sha((G/rel).read_bytes())==digest)
 ck(prefix+' whole original source binding',candidate['sourceSha256']==sha(bible_path.read_bytes()))
 selected=[x for x in candidate['cards'] if x['recipeId']==rid];ck(prefix+' one exact public card',len(selected)==1)
 card=selected[0]
 raw=[x for x in root_recipes if x['id']==rid];ck(prefix+' one exact source identity',len(raw)==1)
 linked=[x for x in audit['linkedRecipes'] if x['sourceRecipe']['id']==rid];ck(prefix+' prior complete linked source exact',len(linked)==1 and linked[0]['sourceRecipe']==raw[0])
 text=cards_path.read_text(encoding='utf-8');heading='## '+rid+' — '+card['name']
 ck(prefix+' public card heading unique',text.count(heading)==1)
 start=text.index(heading);end=text.find('\n## ',start+1)
 complete_card_text=text[start:] if end<0 else text[start:end]
 ck(prefix+' card includes complete operative output',len(complete_card_text)>1500)
 current_files=[manifest_path,candidate_path,guide_path,cards_path]
 missing=[p.relative_to(G).as_posix() for p in current_files if 'sources/'+p.relative_to(G).as_posix() not in original_members]
 existing=[p.relative_to(G).as_posix() for p in current_files if 'sources/'+p.relative_to(G).as_posix() in original_members]
 rows.append({'recipeId':rid,'trade':trade,'fullOriginalRecipe':raw[0],'fullPriorAuditLink':linked[0],'fullCurrentOperativeCard':card,'fullCurrentPublicCardText':complete_card_text,'wholeCurrentFiles':[info(p) for p in current_files],'notIncludedInOriginalV3':missing,'alreadyIncludedInOriginalV3':existing,'scope':'Complete current source provision, not a new recipe review, ingredient alias, actual harvest grant or canonical rule change.'})
ck('Both and only the two catalog-linked recipes supplemented',set(x['recipeId'] for x in rows)=={'recipe-92','recipe-173'} and len(audit['linkedRecipes'])==2)
fish=next(x for x in rows if x['recipeId']=='recipe-173')
ck('Fishing four full current public source artifacts absent from V3',len(fish['notIncludedInOriginalV3'])==4)
ck('Current Fishing recipe produces Tackle, not historical Boat name',fish['fullCurrentOperativeCard']['operational']['baseModelIds']==['fishing.tackle'] and fish['fullCurrentOperativeCard']['operational']['eligibleMethods']==['Rod'])
ck('Current Fishing extra recovery retains one evaluation including zero',fish['fullCurrentOperativeCard']['operational']['effect']['oneEvaluationIncludingZero'] is True)
# Full current local review receipts are evidence, never executed tooling.
extra_names=['FISHING_REPAIRED_COMPLETION_VALIDATION.json','FISHING_EXACT_REPAIRS_APPLIED.json','GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md','GPT_COOKING_EXACT_REVIEW.txt']
for name in extra_names:
 p=A/name
 ck('Complete review history available: '+name,p.is_file());paths.append(p)
fm=j(R/'docs/mechanics/FISHING_REVIEW_STATUS.json')
ck('Fishing local completion receipt binding',sha((A/'FISHING_REPAIRED_COMPLETION_VALIDATION.json').read_bytes())==fm['validationSha256'])
ck('Fishing exact repairs binding',sha((A/'FISHING_EXACT_REPAIRS_APPLIED.json').read_bytes())==fm['repairEvidenceSha256'])
ck('Fishing actual GPT review binding',sha((A/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md').read_bytes())==fm['replyHashes']['GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md'])
cm=j(R/'docs/mechanics/COOKING_REVIEW_STATUS.json')
ck('Cooking actual GPT review binding',sha((A/'GPT_COOKING_EXACT_REVIEW.txt').read_bytes())==cm['replyHashes']['GPT_COOKING_EXACT_REVIEW.txt'])
bindings=[info(p) for p in paths]
cp=j(A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_ACCEPTANCE_90.json')
for row in [cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]:ck('Canonical baseline unchanged: '+row['path'],info(G/row['path'])==row)
model={'id':'BESTIARY-LINKED-RECIPE-FULL-CURRENT-SOURCES-91','status':'PREPARED_UNSENT_DEPENDENCY_SUPPLEMENT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'originalBestiaryPacket':info(original_zip),'sourceBindings':bindings,'linkedRecipes':rows,
       'authorityBoundary':'Full reviewed current public candidate/card/guide files and actual exact-review receipts resolve missing-source access. Older aggregate recipe counts and source-conference pending phrases are historical. Current total687 recipes/433public is separate; this supplement does not confer new domain review.',
       'preservedQuestions':'The original40 printed recipe references,178 harvest occurrences and all name/context/material conflicts remain in the full original audit. Matching current ingredient or legacy names does not prove creature/material identity, authorize replacement, create known formulas, grant catches or yield, or reopen sealed dossiers/cosmology.',
       'operativeSourceHighlights':[
          'recipe-173 retains the complete current fishing.tackle model and Rod-only eligibility. Legacy River Fishing Boat is a retained source name, not authority for a boat body, capacity, propulsion or mount.',
          'Fishing check bonus and extra-recovery family are separately selected. Actual secure capture evaluates once per physical creature including zero; extra available disjoint real reserve units require later lawful harvesting. It creates neither immediate meat nor another creature.',
          'recipe-92 retains the actual completed/accepted feast, temporaryHP offer and separate one-hour lightning resistance, actual food/packaging and all full shared rules. A printed monster ingredient reference creates no feast, food mass or source permissions.'
       ],'newRuleAdoptions':0,'sourceInformationDeleted':0,'canonicalImplementationApplied':False,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'cosmologyDecisions':0,'actuallySent':False}
README='''Bestiary linked-recipe dependency supplement91. The live ongoing Bestiary review exposed a missing full Fishing dependency. Local inspection confirmed all four current public Fishing artifacts were absent from V3. The two directly catalog-linked recipe identities are recipe-92 and recipe-173; complete source/history/current cards are provided, with the full current guides and candidates rather than label-only summaries. Read CURRENT_LINKED_RECIPES.json and its full sources. Historical raw labels, review counts and pending phrases are not current authority. The underlying exact-review hashes all match live files. No supplied code needs execution. Do not alter monster CR/type, invent formula/ingredient aliases, infer a boat from the old recipe title, award an extra catch, or touch sealed dossier contents/cosmology. This packet is prepared while GPT's existing response is active; do not interrupt it. After that response completes and is locally preserved, use these complete sources to resolve any actual missing-dependency hold and preserve all other findings.\n'''
ROOT.mkdir()
for p in paths:
 dst=ROOT/'sources'/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True)
 with dst.open('xb') as f:f.write(p.read_bytes())
with (ROOT/'CURRENT_LINKED_RECIPES.json').open('xb') as f:f.write(enc(model))
with (ROOT/'README.txt').open('xb') as f:f.write(README.encode())
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
with (ROOT/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
files=sorted(p for p in ROOT.rglob('*') if p.is_file())
manifest={'id':'BESTIARY-RECIPE-DEPENDENCIES91-MANIFEST','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
with (ROOT/'MANIFEST.json').open('xb') as f:f.write(enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 ck('Complete supplement archive CRC',z.testzip() is None)
 for row in manifest['files']:
  raw=z.read(row['path']);ck('Archive complete member '+row['path'],len(raw)==row['bytes'] and sha(raw)==row['sha256'])
result={'id':'BESTIARY-LINKED-RECIPE-DEPENDENCIES91-PREPARATION','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT_WHILE_EXISTING_GPT_BESTIARY_GENERATION_ACTIVE','archive':info(ZIP),'model':info(ROOT/'CURRENT_LINKED_RECIPES.json'),'fullSourceFiles':len(paths),'archiveMembers':len(manifest['files'])+1,'exactRecipeIds':['recipe-92','recipe-173'],'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED),'actuallySent':False,'sourceInformationDeleted':0,'canonicalImplementationApplied':False,'cosmologyDecisions':0}
with OUT.open('xb') as f:f.write(enc(result))
print(json.dumps({'preparation':info(OUT),'archive':info(ZIP),'passed':len(checks),'failed':0,'sources':len(paths),'members':len(manifest['files'])+1,'actuallySent':False},indent=2))
