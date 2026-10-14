"""Build a lossless complete-file handoff for the 128-card exact review.

Includes actual candidate files and protected sources, not representative samples.
This does not send, approve or promote anything. The ZIP roundtrip is verified.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 target=A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json';assert not target.exists(),'Preserve/version any prepared or submitted bundle.'
 statusp=A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json';status=read(statusp)
 idx=R/'docs/director-only/GATHERING_TOOL_INTERNAL_DRAFT_INDEX.md';guide=R/'docs/director-only/GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md'
 archive=A/'gathering-before-exact-bundle-preparation';assert not archive.exists();archive.mkdir()
 prior=[statusp,idx,guide,A/'GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json',A/'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json']
 manifest=[]
 for p in prior:
  dst=archive/p.name;shutil.copy2(p,dst);manifest.append({'original':rel(p),'savedAs':dst.name,'sha256':sha(dst)})
 dump(archive/'MANIFEST.json',manifest)
 s=idx.read_text(encoding='utf-8');s=s.replace('Next: finish all finite physical/qualification sequences and the eight combined seams, then submit every complete card and guide for exact GPT review.','The [physical sequence casebook](GATHERING_TOOL_PHYSICAL_SEQUENCE_CASEBOOK.md) now states all27 source examples,14 additional adjudication risks,17 body boundaries and eight joint seams. Its qualitative outcomes are authored expectations awaiting reviewer assessment. Sixty-seven source/numeric/coverage checks pass; they do not constitute an implemented gathering runtime. Next: submit every complete card, guide, source and accurately scoped evidence for exact GPT review.')
 idx.write_text(s,encoding='utf-8')
 s=guide.read_text(encoding='utf-8');s+='\n\n## Exact-review physical casebook\n\nThe [complete physical sequence casebook](GATHERING_TOOL_PHYSICAL_SEQUENCE_CASEBOOK.md) supplies27 source worked examples,14 additional adjudication risks,17 body boundaries and eight joint seams. The companion evidence separates67 computed source/numeric/coverage checks from qualitative expected dispositions awaiting exact review. Structural transition and quotation calculators are bounded arithmetic, not completed work or actual-world authentication.\n';guide.write_text(s,encoding='utf-8')
 casebook=R/'docs/director-only/GATHERING_TOOL_PHYSICAL_SEQUENCE_CASEBOOK.md'
 for p in [idx,guide,casebook]:status['outputs'][rel(p)]=sha(p)
 status.update(physicalSequenceCasebook=rel(casebook),workedCaseValidation='GATHERING_TOOL_WORKED_CASE_VALIDATION.json',qualitativeSequenceReviewPending=True,exactReviewPrepared=True,exactReviewSubmitted=False,openWork=['Separate exact GPT review of all128 cards, complete guides/public envelopes and physical-case dispositions'],updatedAtUtc=datetime.now(timezone.utc).isoformat())
 dump(statusp,status)
 # The changed guide/index hashes bind fresh projection evidence; source cards
 # are unchanged. Re-run only the validator affected by that manifest change.
 subprocess.run([sys.executable,'-X','utf8',str(R/'tools/validate_gathering_tool_guides_projection.py')],check=True)
 checks={name:read(A/name) for name in ['GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json','GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json','GATHERING_TOOL_WORKED_CASE_VALIDATION.json']}
 assert all(not v['failedChecks'] for v in checks.values())
 protected=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')['protectedFiles'];assert all(sha(G/p)==h for p,h in protected.items())
 files={G/p for p in protected}|{G/p for p in status['outputs']}
 names=['GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json','GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json','GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json','GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json','GATHERING_TOOL_WORKED_CASE_VALIDATION.json','GATHERING_TOOL_PUBLIC_PROJECTION_LEDGER.json','GATHERING_TOOL_PART2_SUBMISSION.json','GATHERING_JOINT_SOURCE_RECONCILIATION_INTEGRATION.json','GATHERING_JOINT_SOURCE_RECONCILIATION_REPLY_CAPTURE.json','GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md','GPT_SKINNING_SOURCE_TALLY_ERRATUM.md']
 for tr in ['MINING','SKINNING','SALVAGING']:names += [f'GPT_{tr}_SOURCE_CONFERENCE.md',f'{tr}_SOURCE_CONFERENCE_CAPTURE.json',f'{tr}_SOURCE_VERDICT_RECONCILIATION.json']
 files|={A/n for n in names}
 tools=['build_gathering_tool_internal_draft.py','gathering_tool_models.py','build_gathering_tool_guides_projection.py','validate_gathering_tool_internal_draft.py','validate_gathering_tool_guides_projection.py','validate_gathering_worked_cases.py','prepare_gathering_exact_bundle.py','core_playtest_rules.py','fishing_reference.py']
 # Include local Python import dependencies without reading or sending unrelated
 # filesystem content. All discovered modules stay inside the known tools dir.
 queue=[R/'tools'/n for n in tools];seen=set()
 while queue:
  p=queue.pop()
  if p in seen:continue
  assert p.is_file();seen.add(p);files.add(p)
  tree=ast.parse(p.read_text(encoding='utf-8'))
  for node in ast.walk(tree):
   modules=([node.module] if isinstance(node,ast.ImportFrom) and node.module else [n.name for n in node.names] if isinstance(node,ast.Import) else [])
   for module in modules:
    possible=R/'tools'/(module.split('.')[0]+'.py')
    if possible.is_file():queue.append(possible)
 readiness={'status':'COMPLETE FILE CANDIDATE PREPARED FOR EXACT REVIEW; NOT APPROVED','internalCards':128,'publicCards':82,'visibility':[82,6,40],'internalBodyModels':17,'publicBodyModels':15,'auxiliaryModels':3,'retainedPublicBookParagraphs':492,'sourceRegisterManuscriptChecks':checks['GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json']['checkCount'],'guideProjectionArithmeticChecks':checks['GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json']['checkCount'],'workedExampleNumericCoverageChecks':checks['GATHERING_TOOL_WORKED_CASE_VALIDATION.json']['checkCount'],'manufacturingRows':1536,'positiveStructuralInputs':442,'structuralInputsIncludingZero':544,'structuralCalculatorTransitions':3264,'restorationQuotationRows':256,'sourceWorkedCases':27,'additionalAdjudicationRisks':14,'bodyBoundaryCases':17,'jointSeamsMapped':8,'qualitativeExpectedDispositionsAwaitExactReview':True,'sourceDirectionsComplete':True,'appliedDocumentationCorrections':['Skinning192/109 tally','GI-11-C1 residue accounting','GI-12-C1 structural count'],'protectedInputsUnchanged':82,'recipesApproved':0,'reviewedRecipes':392,'remainingRecipes':295,'publicReviewed':251,'runtimeImplemented':False,'balanceApproved':False,'wholeGameFlowApproved':False,'sourceInformationDeleted':0,'cosmology':'after authorized push and verified remote commit','artifactHashes':status['outputs']}
 rp=A/'GATHERING_128_EXACT_CANDIDATE_READINESS.json';dump(rp,readiness);files.add(rp)
 root_readme='''# Decennium Descent — complete 128-card gathering exact-review handoff

This archive contains actual complete files, not summaries or representative cards. It is internal reviewer material for Calibration Review Part 2. It is not the player publication package. All paths beneath this root retain their repository-relative structure. FILE_MANIFEST.json supplies byte sizes and SHA-256 for every payload file. Extract normally; no installation, shell setup, network call or package execution is needed to inspect it.

## Current authority and scope

Your GI-01–12 joint source verdict is in docs/audit/2026-10-08/full-game/GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md. Its GI-11-C1 loss/residue correction and GI-12-C1 Skinning structural-count correction are applied beside preserved originals. The earlier Skinning192/109 ingredient tally correction also remains explicit. All three full source verdicts and captures are included. Historical source-preparation reports may say unsent/pending; those describe their original stage, not this current candidate. GATHERING_128_EXACT_CANDIDATE_READINESS.json is the current scope statement.

## Read the actual candidate

The working root is DescentReviewChanges/ReviewBible/.

1. docs/director-only/GATHERING_TOOL_INTERNAL_DRAFT_INDEX.md and GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md.
2. docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md and MINING_CANDIDATE_GUIDE.md, SKINNING_CANDIDATE_GUIDE.md, SALVAGING_CANDIDATE_GUIDE.md.
3. data/director/gathering_tool_recipe_candidate_internal.json: all128 lossless original recipes, operational objects, full book bindings,17 output bodies and three auxiliary models. Read all43 Mining,43 Skinning and42 Salvaging cards. Compare the three complete internal recipe manuscripts and the internal body catalogue.
4. data/crafting/gathering_tool_recipe_candidate_public.json: all82 public records and15 output bodies. Compare all three complete public recipe manuscripts, the public body catalogue and full guide envelopes. All492 source book paragraphs remain exact and separate from operational additions.
5. docs/director-only/GATHERING_TOOL_PHYSICAL_SEQUENCE_CASEBOOK.md: all27 source worked examples,14 additional adjudication risks,17 body boundaries and eight joint seams. These qualitative outcomes are stated expectations to review, not claimed runtime passes.

## Validation is evidence with stated limits

The audit directory contains777 source/register/manuscript checks,824 guide/projection/arithmetic checks and67 worked-example numeric/coverage checks. The full1,536 manufacturing rows,544 structural inputs,3,264 reference transitions and256 quotations are supplied. Common structural and repair calculators are separately evaluated against those expectations. Declared missing-primary quotation rejections do not authenticate a real body's history or prove completed repair work.

The complete relevant authoring and validation code is included for inspection. There is no implemented gathering gameplay runtime. Numeric checks cannot establish actual world stock, anatomy, legal access, safe containment, Director authority, real receiving or human balance. The code does not purport to do so. Actual campaign records and independently governed procedures remain the prerequisites described in the cards/guides. Review the complete prose, operational objects and case dispositions rather than treating aggregate PASS as your verdict.

## Public metadata question for exact disposition

The player projection retains every printed ingredient occurrence and the public formula's required quantity/consumption/role. A supplemental material profile is included only when its name/tier/unit value/unit mass match one independently public source material. This publishes82 supplemental profiles. The other203 occurrences keep their recipe requirements, with extra metadata withheld and the exact original retained internally. This includes two printed mentions with restricted material dossiers. No donor list, drop chance, acquisition permission or private recipe membership is published. Please assess this complete envelope, including whether any withheld recipe-critical requirement needs a different explicit audience treatment; do not infer that a printed mention authorizes its dossier.

## Requested exact verdict

Review every card and give exact authored-operational approval or a finite, concrete correction list identifying affected records and replacement rules. If conditional, state whether completing the named repairs and appropriate checks permits promotion without another generic source conference. No preliminary source directions are missing. Do not reopen unchanged prior trades without a concrete newly identified conflict. Prior protected trade files are included as governing comparison evidence, not a request to reapprove them.

This review does not approve actual material availability, companion runtime, human balance, publication, final whole-game flow, push or cosmology. Counts remain392/687 reviewed,295 pending, public251/433 until an actual scoped verdict and its conditions are satisfied. The owner's order stays complete authored candidate plus final joint whole-game flow confirmation, authorized GitHub push, verified remote commit, then careful cosmology review. No deletion or push has occurred.
'''
 entries={rel(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files,key=rel)}
 assert len(entries)==len(files) and all(not p.startswith('/') and '..' not in Path(p).parts for p in entries)
 bundle=A/'DD_Gathering_128_Exact_Review_v1.zip';assert not bundle.exists()
 with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.writestr('README_EXACT_REVIEW.md',root_readme.encode('utf-8'))
  z.writestr('FILE_MANIFEST.json',(json.dumps(entries,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
  for p in sorted(files,key=rel):z.write(p,rel(p))
 with zipfile.ZipFile(bundle) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(entries)+2
  assert z.read('README_EXACT_REVIEW.md').decode('utf-8')==root_readme
  assert all(hashlib.sha256(z.read(p)).hexdigest()==v['sha256'] and len(z.read(p))==v['bytes'] for p,v in entries.items())
 currentstatus=read(statusp);assert all(sha(G/p)==h for p,h in currentstatus['outputs'].items())
 prompt='''Codex exact gathering review: the attached DD_Gathering_128_Exact_Review_v1.zip contains ALL128 actual complete Mining/Skinning/Salvaging cards, full internal/public JSON and manuscripts, all17 bodies, complete guides, preserved original sources,82 book bindings, the25 omission overlays and version-bound evidence. This is the complete-file handoff requested in your GI-01–12 verdict, not another source conference. Please open README_EXACT_REVIEW.md and FILE_MANIFEST.json, then inspect every card and full public envelope. Use the files directly; no installation or network access is required.

GI-11-C1 and GI-12-C1 are applied separately; original verdicts and the Skinning192/109 tally erratum remain preserved. Local evidence is777 source/register/manuscript checks,824 guide/projection/arithmetic checks and67 source-bound worked-example numeric/coverage checks. All1,536 manufacturing rows,544 structural inputs,3,264 reference transitions and256 quotes are included. The physical casebook supplies27 source worked examples,14 additional risks,17 body boundaries and the eight joint seams. Its qualitative outcomes are authored expectations for your assessment, NOT automated runtime passes. No gathering runtime, real-world authentication or human balance is claimed.

Please explicitly assess the fail-closed public component envelope described in the README: printed occurrences/assembly consumption retained,82 supplemental profiles independently public,203 supplemental profiles withheld but internally preserved. Identify any recipe-critical audience correction concretely without publishing a private dossier merely from its ingredient mention.

Return one exact authored-operational verdict covering all128 cards, with a finite named correction list if needed and the conditions for promotion. If the named corrections plus appropriate checks permit promotion without another generic conference, state that explicitly. Source directions are already settled; preserve genuine actual-source dependencies without expanding them into hypothetical new preliminary conferences. Include actual affected recipe IDs and replacement wording for any change. If you cannot open the attachment or cannot inspect some files, report the exact limitation rather than approving unseen material.

Counts remain392/687 reviewed,295 pending, public251/433; zero gathering approvals have been inferred. No deletion, push or cosmology review. The owner's final joint whole-game flow confirmation precedes the authorized push; remote verification precedes careful cosmology review.'''
 pp=A/'CODEX_GATHERING_128_EXACT_REVIEW_UPLOAD_PROMPT.txt';pp.write_text(prompt,encoding='utf-8')
 state={'status':'prepared-not-sent','threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','bundleFile':bundle.name,'bundleSha256':sha(bundle),'bundleBytes':bundle.stat().st_size,'payloadFiles':len(entries),'payloadUncompressedBytes':sum(x['bytes'] for x in entries.values()),'zipRoundtripVerified':True,'promptFile':pp.name,'promptSha256':sha(pp),'promptCharacters':len(prompt),'artifactHashes':status['outputs'],'protectedFiles':protected,'readinessFile':rp.name,'recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'post-verified-push only'}
 dump(target,state)
 print(json.dumps({k:state[k] for k in ['status','bundleFile','bundleSha256','bundleBytes','payloadFiles','payloadUncompressedBytes','promptCharacters','recipesApproved']}))

if __name__=='__main__':main()
