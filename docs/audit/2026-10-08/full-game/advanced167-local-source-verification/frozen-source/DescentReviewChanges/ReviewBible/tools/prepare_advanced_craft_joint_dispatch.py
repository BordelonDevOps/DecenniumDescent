"""Refresh the advanced source archive after actual gathering promotion.

Preserves the original prepared archive and packets. Includes current complete
class/feat comparisons as evidence; pending feat text is not approved authority.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 out=A/'ADVANCED_CRAFT_JOINT_DISPATCH_PREPARATION.json';assert not out.exists()
 prior=read(A/'ADVANCED_CRAFT_FILE_HANDOFF_PREPARATION.json')
 assert sha(A/prior['bundleFile'])==prior['bundleSha256']
 assert all(sha(G/p)==h for p,h in prior['currentSourceAndRuleHashes'].items())
 gm=read(R/'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json');assert all(sha(G/p)==h for p,h in gm['artifactHashes'].items())
 receipt=read(A/'GATHERING_128_EXACT_PROMOTION_RECEIPT.json');assert receipt['recipesPromoted']==128
 files={G/p for p in prior['currentSourceAndRuleHashes']}|{G/p for p in gm['artifactHashes']}
 files|={R/'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json',A/'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md',A/'GATHERING_128_EXACT_VERDICT_CAPTURE.json',A/'GATHERING_128_EXACT_PROMOTION_RECEIPT.json',A/'GATHERING_128_EXACT_COMPLETION_VALIDATION.json',Path(__file__)}
 rebase=[]
 for prefix in ['TINKER_DEVICE_INTERFACE','CRAFTING_FEAT_INTERFACE','SKILL_FEAT_SOURCE']:
  p=A/(prefix+'_PREPARATION.json');e=read(p)
  files|={p,A/(prefix+'_AUDIT.md'),A/(prefix+'_STATUS.json'),A/('CODEX_'+prefix+'_PREPARED.txt')}
  for name,h in e['protectedFiles'].items():
   q=G/name;assert q.is_file(),name;files.add(q)
   if sha(q)!=h:rebase.append({'preparation':p.name,'file':name,'historicalSha256':h,'currentSha256':sha(q),'treatment':'Historical protection snapshot retained; current full file supplied separately; do not treat old excerpt status as current authority'})
  if prefix=='TINKER_DEVICE_INTERFACE':
   for filekey,hashkey in [('classCandidateFile','classCandidateSha256'),('classGuideFile','classGuideSha256'),('classExtractFile','classExtractSha256'),('underlyingBookFile','underlyingBookSha256')]:
    q=G/e[filekey];assert sha(q)==e[hashkey];files.add(q)
   assert len(e['craftedRecipeIds'])==43 and len(e['cases'])==18
 sources=read(A/'ADVANCED_CRAFT_SOURCE_PREPARATION.json');assert len(sources['recipes'])==167 and len(sources['publicBookBindings'])==100
 catalog=read(R/'data/director/crafting_recipe_review_catalog.json');assert catalog['totals']['reviewed']==520 and catalog['totals']['unreviewed']==167
 pending={x['recipeId'] for x in catalog['recipes'] if x['status']!='reviewed-authored-playtest'}
 assert pending=={x['id'] for x in sources['recipes']}
 files|={R/'data/director/crafting_recipe_review_catalog.json',R/'data/playtest/crafting_recipe_review_catalog_public.json',R/'docs/director-only/CRAFTING_REVIEW_QUEUE.md'}
 report={'status':'READY complete advanced167 source-authoring handoff; UNSENT','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'originalPreparedBundlePreserved':prior['bundleFile'],'originalSourceRuleHashesStillExact':len(prior['currentSourceAndRuleHashes']),'gatheringPromotionVerified':True,'recipesReviewed':520,'recipesPending':167,'publicReviewed':333,'publicPending':100,'allPendingRecipeIdsExact':True,'advancedSourceObjects':167,'publicBookBindings':100,'sourceCases':50,'tinkerDeviceCases':18,'currentInterfaceFilesSupplied':True,'historicalInterfaceHashChanges':rebase,'pendingFeatEffectsApproved':False,'sourceInformationDeleted':0,'sent':False}
 rp=A/'ADVANCED_CRAFT_JOINT_REBASE_CHECK.json';dump(rp,report);files.add(rp)
 prompt="""Codex reports the gathering exact-review gate complete: your final reply af756084-996a-4143-a34a-baf1da9bcce3 is fully captured. GEX-01/GEX-02 are applied, all1,668 existing checks plus45 focused checks pass, all82 protected sources unchanged. The required Mining11/Failure and Salvaging1.25/.125lb and.25/.025lb regressions pass. All128 cards are promoted under your explicit conditional authority. Current520/687 reviewed,167 pending; public333/433. Complete authority and receipt are included; no repeat gathering conference is needed.

Please now open the attached complete-file advanced-crafting handoff, its README_SOURCE_REVIEW.md and FILE_MANIFEST.json. It supplies all167 untouched advanced originals (Enchanting43, Rune Carving41, Scribing40, Tinkering43),100 exact six-paragraph public-book bindings, four original version sources, the actual book, all50 finite AC/EN/RC/SC/TI cases and current governing files. It also supplies all48 Tinker class cards, original class evidence and18 TD cases, plus complete pending crafting/Skill feat comparisons. Old pending Tailoring/gathering labels in original preparation packets are historical; the fresh rebase report and current full files control.

Give finite, usable source-authoring decisions for all four trades and their actual shared interfaces so the exact operational candidates can be built next. Resolve the50 prepared cases and relevant18 Tinker/device cases, name every affected recipe/group, supply missing body/attack/action/control/service/charge/spell-use/quality/repair details as explicitly NEW authoring choices, and give worked boundary examples. State which actual earlier rule is kept or changed. Shared names alone must not merge class devices, crafted devices, spell effects or pending feats. Include precise Rune source-name treatment, one-year/null-hour recipe623,22 Scribing use questions,18 incomplete automaton attacks and five distinct custom profiles. Preserve all source fields and absent/null distinctions.

Read complete originals before deciding. Ordinary operating procedures can be completed with finite authored defaults; do not turn already supplied sources or hypothetical campaign facts into repeated preliminary conferences. Genuine missing spell effects, acquisition and world permissions must remain explicit bounded dependencies. Pending feats are supplied for comparison and their future focused review; do not silently approve all feats in this recipe conference. No exact-card promotions are requested now. Distinguish the four artisan creation credentials from finished-item use permissions, source dawn recharge from Rune charges, and servicing from repair or rest.

Return a coherent source-authoring verdict with exact mappings and sufficient procedures for every output family. Avoid repeating large originals already in the archive; refer to their real paths/IDs. Explicitly state any finite remaining source question that truly prevents authoring rather than approving unseen material. Preserve literal Silent Ones/Heartcell/Matrix and other cosmology references without interpreting them. Final joint whole-game flow precedes the authorized GitHub push; remote verification precedes the careful cosmology review. No deletion or push here.
"""
 pp=A/'CODEX_ADVANCED_CRAFT_JOINT_SOURCE_PROMPT.txt';assert not pp.exists();pp.write_text(prompt,encoding='utf-8');files.add(pp)
 readme="""# Complete advanced crafting source conference

Current totals:520/687 recipes reviewed;167 pending. Public333/433;100 pending. Gathering GEX-01/GEX-02 are fulfilled and128 cards promoted; the actual final verdict, current guides/cards and completion receipt are supplied. The earlier prepared archive and all five text packets are unchanged historical preparation.

Read CODEX_ADVANCED_CRAFT_JOINT_SOURCE_PROMPT.txt for the conference request. ADVANCED_CRAFT_SOURCE_PREPARATION.json contains all167 exact originals,100 complete V5 public bindings, version differences, occurrence registers and missing-field evidence. ADVANCED_CRAFT_REVIEW_SCENARIOS.md contains50 finite cases. TINKER_DEVICE_INTERFACE_PREPARATION.json and its audit provide48 full class cards, original source extract and18 interactions. CRAFTING_FEAT_INTERFACE_PREPARATION.json and SKILL_FEAT_SOURCE_PREPARATION.json provide unapproved feat comparisons; their presence grants no feat approval.

Every file in FILE_MANIFEST.json is supplied in full at its actual repository-relative path. Current governing files are included for every historical protected-interface path. ADVANCED_CRAFT_JOINT_REBASE_CHECK.json reports historical hash changes explicitly; old embedded excerpts/counts/pending labels remain historical, not current rule authority. No source recipe changed. The authoring conference must decide actual finite mechanics before new exact cards are built. No software installation or network access is needed to inspect this archive.

Audience remains100 public/7 restricted/60 Director-only for these advanced recipes. Literal cosmology restrictions are preserved without interpretation. Cosmology review follows final whole-game flow, authorized GitHub push and verified remote commit. Runtime and human balance remain separately open.
"""
 manifest={rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
 zp=A/'DD_Advanced_Craft_167_Joint_Source_v2.zip';assert not zp.exists()
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.writestr('README_SOURCE_REVIEW.md',readme.encode('utf-8'));z.writestr('FILE_MANIFEST.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
  for p in sorted(files,key=rel):z.write(p,rel(p))
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None and len(z.namelist())==len(manifest)+2
  assert all(hashlib.sha256(z.read(p)).hexdigest()==m['sha256'] and len(z.read(p))==m['bytes'] for p,m in manifest.items())
 report.update({'bundleFile':zp.name,'bundleSha256':sha(zp),'bundleBytes':zp.stat().st_size,'payloadFiles':len(manifest),'zipRoundtripVerified':True,'promptFile':pp.name,'promptSha256':sha(pp),'currentFileHashes':{p:m['sha256'] for p,m in manifest.items()}});dump(out,report)
 print(json.dumps({k:report[k] for k in ['status','bundleFile','bundleBytes','payloadFiles','recipesReviewed','recipesPending','sent']}))
if __name__=='__main__':main()
