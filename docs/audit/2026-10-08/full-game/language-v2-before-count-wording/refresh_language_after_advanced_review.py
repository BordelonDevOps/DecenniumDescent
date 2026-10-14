"""Add completed Scribing/command authority to the unchanged language source set."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 out=A/'LANGUAGE_COMMUNICATION_V2_PREPARATION.json';zp=A/'DD_Language_Communication_Source_Prepared_v2.zip';assert not out.exists() and not zp.exists()
 old=read(A/'LANGUAGE_COMMUNICATION_SOURCE_STATUS.json');assert sha(A/old['bundleFile'])==old['bundleSha256']
 changes={n:{'prior':h,'current':sha(G/n)} for n,h in old['currentFileHashes'].items() if sha(G/n)!=h}
 joint='docs/audit/2026-10-08/full-game/ADVANCED_CRAFT_JOINT_SUBMISSION.json';assert set(changes)=={joint}
 with zipfile.ZipFile(A/old['bundleFile']) as z:prior=json.loads(z.read(joint))
 current=read(G/joint)
 allowed={'status','sourceVerdictPending','actualVerdictReplyId','reviewerDecisionPackage','reviewerDecisionPackageSha256','verdictFile','verdictSha256','verdictCaptureFile'}
 assert all(prior.get(k)==current.get(k) for k in prior.keys()|current.keys() if k not in allowed)
 manifest=read(R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json');assert manifest['status'].startswith('REVIEWED') and all(sha(G/n)==h for n,h in manifest['artifactHashes'].items())
 internal=read(R/'data/director/advanced_craft_recipe_candidate_internal.json');original=read(A/'LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json')
 selected=[c for c in internal['cards'] if c['sourceRecipe']['skill']=='Scribing']
 sections={k:deepcopy(v) for k,v in internal['procedureSections'].items() if k.startswith('SC-') or k in ['AC-07','RC-01','RC-02','RC-07','TI-04','TI-05','TI-08','TD-01','TD-08']}
 addendum=A/'LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json'
 dump(addendum,{'status':'Reviewed recipe authority supplied for the pending ordinary language conference; no new language/feat/spell approval','exactReviewManifest':rel(R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json'),'exactReviewManifestSha256':sha(R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json'),'completeScribingCards':selected,'completeApplicableProcedureSections':sections,'currentInternalCandidateSha256':sha(R/'data/director/advanced_craft_recipe_candidate_internal.json'),'currentPublicCandidateSha256':sha(R/'data/crafting/advanced_craft_recipe_candidate_public.json'),'interpretationBoundary':'SC-08 permits its specific supported literal-passage translation only. Ordinary fluency/learning, language identities and pending feat/spell decisions remain LA scopes. Private dossier fields and special-tongue lore remain private/deferred.'})
 notes=A/'LANGUAGE_COMMUNICATION_V2_REVIEW_SCOPE.md'
 notes.write_text('''# Languages, literacy and communication — refreshed source scope

The original16 LA-01–16 cases and complete source records are preserved. All136 original payloads except the advanced-submission metadata are byte-identical; that record differs only by completed source-verdict provenance. The original v1 archive remains preserved. This v2 adds the completed advanced recipe authority and actual source-linked Scribing/control paragraphs. No language,spell,feat,class or runtime data has changed.

Read LANGUAGE_COMMUNICATION_SOURCE_AUDIT.md and its full preparation JSON, then LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json. The older instruction to wait for advanced167 is fulfilled: all167 recipes/public100 completed exact authored-operational review under AEX-01–07, bringing totals687/687 and433/433. The current manifest/receipt and full internal/public recipe guides and data are supplied. Older pending labels are historical snapshots.

LA-14 now has binding evidence. SC-03's loaded script temporarily supplies repertoire only for an otherwise qualified real caster; it does not create comprehension or bypass actual spell eligibility. SC-05/AEX-07 require relevant content, genuine lead consultation and exclude self-production. SC-07 preserves languages:0 on476/486/672 and one Insight on498/500 only with useful actual parallel text. SC-08 records points per researcher/target language,cap6; one actual study hour; evidence once per reader across copies. Its finite spend is3points plus8activehours for one supported preregistered passage of at most250words. It grants no fluency,separate cipher solution,new meaning or spell learning. Its private674 scope remains internal; don't export private membership through an ordinary public language guide.

Keep those completed recipe procedures. Resolve how a separately authorized ordinary fluency course, known-language literacy, deciphering and communication coexist without double-counting the same work or granting a general Insight-to-language exchange. Preserve actual fixed source meanings,translation evidence and scopes. TI-04's visible/audible control communication is an actual channel requirement,not a new spoken-language proficiency. Its command/action/range and controller gates remain unchanged; telepathy cannot silently substitute for an unspecified hardware protocol.

Retain the other15 bounded LA cases: exact starting/variant/background grants,aliases and script identities,duplicates/choice eligibility,literacy,ordinary learning,translation/task outcomes,turn communication,Silenced/Deafened/components,reviewed and pending spell/class/feat interfaces,record fields,and precise post-push receipts. Pending spells and feats stay routed to their existing dedicated questions. This conference should author only the finite missing ordinary language procedure and resolve genuine source conflicts,then permit complete exact candidate authoring for later review. It cannot promote pending catalog entries.

No cosmology,deep-language origins or hidden meanings are reviewed here. LA-16 preserves literal restrictions and names only; interpretation waits for the owner-required final whole-game flow,GitHub push and verified remote commit. No original source may be deleted from this preparation.

The currently active notebook request is the six-manuscript onboarding/charter exact review. This archive is prepared and UNSENT. Before dispatch, capture that verdict and check whether any relevant teaching/source dependency changed; do not duplicate or interrupt the active request.
''',encoding='utf-8')
 files={G/n for n in old['currentFileHashes']}
 files.update([addendum,notes,Path(__file__).resolve(),R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json',A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json',A/'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json',R/'data/director/advanced_craft_recipe_candidate_internal.json',R/'data/crafting/advanced_craft_recipe_candidate_public.json',R/internal['sharedGuide'],R/internal['bodyGuide'],R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md',R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md',R/'data/public/class_playtests/tinker.json',R/'data/playtest/class_sources/tinker.json',R/'docs/mechanics/classes/tinker.md'])
 payload={rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.writestr('README_LANGUAGE_V2.md','Read docs/audit/2026-10-08/full-game/LANGUAGE_COMMUNICATION_V2_REVIEW_SCOPE.md first. Complete original language evidence and completed advanced-crafting interfaces are included. Prepared,UNSENT; no new approvals. Preserve sources and defer cosmology.\n')
  z.writestr('FILE_MANIFEST.json',json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
  for p in sorted(files,key=rel):z.write(p,rel(p))
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None and len(z.namelist())==len(payload)+2==len(set(z.namelist()))
  assert all(hashlib.sha256(z.read(n)).hexdigest()==m['sha256'] for n,m in payload.items())
 result={'status':'PASS refreshed complete source package; UNSENT','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'originalBundle':old['bundleFile'],'originalBundleSha256':old['bundleSha256'],'originalPayloadFiles':old['payloadFiles'],'unchangedOriginalPayloadFiles':old['payloadFiles']-len(changes),'changedMetadataOnly':changes,'originalDecisionCasesPreserved':len(original['decisionCases']),'completeCurrentScribingCards':len(selected),'currentProcedureSections':len(sections),'currentRecipeReviewAuthority':rel(R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json'),'bundleFile':zp.name,'bundleBytes':zp.stat().st_size,'bundleSha256':sha(zp),'payloadFiles':len(payload),'currentFileHashes':{n:m['sha256'] for n,m in payload.items()},'sent':False,'newApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,'cosmologyReviewed':False,'nextAction':'After onboarding/charter exact verdict, check intervening dependencies and submit finite LA-01–16 source conference.'}
 dump(out,result);print(json.dumps({k:v for k,v in result.items() if k not in ['currentFileHashes','changedMetadataOnly']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
