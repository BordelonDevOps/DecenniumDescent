"""Package final reviewer artifacts. No submitted file is modified."""
from pathlib import Path
import json,hashlib,zipfile
O=Path(__file__).resolve().parent; E=O/'evidence'; ROOT=Path('/mnt/data/low_rank_source_v3'); A=ROOT/'docs/audit/2026-10-08/full-game'; P=Path('/mnt/data/low_rank_reproduction')
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reg=load(O/'LR_137_AUTHORING_REGISTER.json'); read=load(E/'READ_ONLY_SOURCE_AUDIT.json'); val=load(E/'AUTHORING_REGISTER_AND_REFERENCE_VALIDATION.json')
assert not read['failedChecks'] and not val['failedChecks']
normative=['LR_137_SOURCE_AUTHORING_VERDICT.md','LR_137_AUTHORING_REGISTER.json','LR_SHARED_OPERATING_DIRECTIONS.json','LR_SOURCE_CONFLICT_DISPOSITIONS.json','LR_8_PROPOSAL_DISPOSITIONS.json','LR_CLASS_AND_SPELL_INTERFACE_DISPOSITIONS.json','LR_WORKED_BOUNDARIES.json','LR_EXACT_CANDIDATE_CHECKLIST.json','LR_EXACT_CANDIDATE_CHECKLIST.md']
reproduced=normative+['evidence/READ_ONLY_SOURCE_AUDIT.json','evidence/AUTHORING_REGISTER_AND_REFERENCE_VALIDATION.json']
proof={'scope':'Deterministic reproduction in a separate reviewer working directory, not gameplay runtime.','sourceArchiveSha256':reg['scope']['archiveSha256'],'files':[{'path':f,'frozenSha256':sha(O/f),'reproducedSha256':sha(P/f),'equal':sha(O/f)==sha(P/f)} for f in reproduced]}
assert all(r['equal'] for r in proof['files'])
(E/'REPRODUCTION_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n')
f=load(A/'LANGUAGE_EXACT_FULFILLMENT.json')
carry={'reviewId':'LR-SOURCE-2026-10-11','disposition':'CARRY FULFILLED AUTHORED LANGUAGE GATE; NO FINITE DISCREPANCY FOUND','actualSourcePath':str((A/'LANGUAGE_EXACT_FULFILLMENT.json').relative_to(ROOT)),'actualReceiptSha256':sha(A/'LANGUAGE_EXACT_FULFILLMENT.json'),'checkedFinalHashes':f['finalHashes'],'checkedReportHashes':f['reportHashes'],'scope':'Compared packaged final file/report hashes and scope flags. Prior 460/496/44/496 completion results are preserved receipt evidence, not mislabeled as rerun here. This conference reran only its own read-only source audit and exported reference suites.','languageOnlyApproval':f['exactLanguageApproval'],'otherPromotion':f['classSpellFeatPromotion'],'currentRecipeGate':[687,433],'nwxCarried':True,'newPromotions':0,'sourceAmendmentRequired':False,'unsentReferenceAddendumRequired':False,'runtimeCertified':False,'wholeGameFlowApproved':False,'cosmologyReviewed':False}
(E/'FULFILLED_GATE_CARRY_RECEIPT.json').write_text(json.dumps(carry,ensure_ascii=False,indent=2)+'\n')
summary={'reviewId':'LR-SOURCE-2026-10-11','state':'FINAL_SOURCE_AUTHORING_VERDICT','archiveBytes':29192630,'archiveSha256':reg['scope']['archiveSha256'],'payloads':342,'originalV2Payloads':184,'originalSourceFiles':163,'identities':137,'mechanicalDecisions':136,'receiptOnly':['blink'],'bookBindings':141,'sharedPolicies':20,'namedSharedConflicts':18,'proposals':8,'proposalBoundaries':32,'classComparisons':54,'completeCounterparts':114,'perIdentityAuthoredBoundaries':137,'jointAuthoredBoundaries':18,'totalAuthoredBoundaryRecords':187,'readOnlySourceChecks':read['checkCount'],'authoringStaticAndReferenceChecks':val['checkCount'],'executableReferenceSubset':val['executableReferenceChecks'],'failedChecks':0,'authoringRecordIds':[d['decisionId'] for d in reg['records']],'normativeFileHashes':{f:sha(O/f) for f in normative},'promotionAuthorized':False,'exactCandidatesRequired':True,'runtimeCertified':False,'humanBalanceApproved':False,'dd01Closed':False,'wholeGameFlowApproved':False,'sourceInformationDeleted':0,'pushAuthorized':False,'cosmologyReviewed':False,'finalizationNote':'These are the final exported decisions, not an intermediate live draft. The source objects and statuses in the register remain preserved historical/current evidence; only the separately labeled authoring layer is new.'}
(O/'LR_FINAL_REVIEW_RECEIPT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
# A navigation-only index; the complete wording is always in the full verdict/register.
lines=['# Low-rank source decision index','137 identities;136 mechanical directions;Blink receipt-only. No exact-card approval.','| Question | Exact spell ID | Name | Source-authoring disposition |','|---|---|---|---|']
for d in reg['records']:lines.append(f'| {d["questionId"]} | `{d["spellId"]}` | {d["name"]} | '+('Receipt-only; no operation' if d['authoring'] is None else 'Complete direction in LR-'+d['questionId'])+' |')
(O/'LR_137_DECISION_INDEX.md').write_text('\n\n'.join(lines[:2])+'\n\n'+'\n'.join(lines[2:])+'\n')
readme='''# FINAL low-rank spell source-authoring package

Review ID: **LR-SOURCE-2026-10-11**. This is the final source verdict, not a draft and not exact operational-card approval.

## Read in this order

1. `LR_137_SOURCE_AUTHORING_VERDICT.md`: full readable verdict, all20 shared policies,18 named shared conflicts, all136 complete operating directions plus Blink receipt,54 individual class-interface dispositions and18 joint worked boundaries.
2. `LR_137_AUTHORING_REGISTER.json`: every original question/spell ID, complete unchanged source and class access,141 book bindings, source mode/alias decisions, full authoring wording and numeric parameters. Original operational fields remain null; no source objects are rewritten.
3. `LR_SOURCE_CONFLICT_DISPOSITIONS.json` and `LR_8_PROPOSAL_DISPOSITIONS.json`: exact mappings and all8 full original proposals/32 authored boundaries beside their NEW source-only adoption.
4. `LR_CLASS_AND_SPELL_INTERFACE_DISPOSITIONS.json`: all54 actual class comparisons and114 full ordinary spell counterparts, with no access/engine/status merge.
5. `LR_WORKED_BOUNDARIES.json` and `LR_EXACT_CANDIDATE_CHECKLIST.md`/`.json`:137 per-identity authored boundaries (including Blink's receipt),18 joint boundaries, plus the32 proposal boundaries referenced from their own file. These187 records are authored expectations, not gameplay-runtime passes.
6. `LR_FINAL_REVIEW_RECEIPT.json`, `FILE_MANIFEST.json`, and `evidence/`: exact scope, final hashes, read-only source audit, limited reference checks, reproduction proof and fulfilled-language carry check. `LR_137_DECISION_INDEX.md` is navigation only, not a substitute for full wording.

## Actual verification

The frozen submitted ZIP is29,192,630bytes; SHA256`5acb3e4c6d9b3652b5731ffc111539a558874285c87dd0952a3398431b896640`. All342 payloads match. The184 earlier V2 files and163 original source files retain their recorded hashes.

- **3,476** read-only byte/source/access/Core/book/receipt comparisons: zero failures.
- **3,726** exported-register/manuscript/preservation/reference checks: zero failures, comprising3,654 static/source/text checks and **72 executable limited reference arithmetic/contract fixtures**.
- The nine normative files and two resulting evidence reports reproduce byte-for-byte in a separate reviewer working directory. This is deterministic reviewer-package reproduction, not a companion/gameplay runtime or campaign authentication.

The source audit parses complete catalogs for identity equality but reviews mechanics only for the selected scope. It does not approve the other pending spells. The LAX carry check compares supplied final hashes, report hashes and limited flags; earlier reported460/496/44/496 results remain their own receipt evidence and are not advertised as rerun here.

## Reproduction: Python standard library only

Keep this package separate from the submitted archive. From this package directory run:

```text
python reproduce_review.py --archive /path/to/DD_Low_Rank_Spells_137_Source_Prepared_v3.zip --output /path/to/new-review-working-copy
```

This verifies and safely extracts the submission into the new working directory, copies the three immutable selected-reference JSON files, and runs the read-only audit, final export and limited reference suite. Nothing installs or accesses a network. No submitted source is edited. Reports are written only in the supplied output directory. An existing unmodified extracted submission can instead be read using `--source-root /path/to/extracted/submission`.

The submitted ZIP is deliberately not duplicated in this package. It is required for the archive/hash and actual-source reproduction. Source evidence files here are reference extracts preserved beside the verdict, not replacement governing authority.

## Scope and next step

Carry the fulfilled687/433 recipe, NWX and LA authored-language gates. Adopt these NEW source directions for authoring **136 full mechanical cards plus Blink's complete nonoperative receipt**. Return the full137-identity candidate envelope and public projection for separate exact review. There is no further generic preliminary conference or unresolved ordinary mechanical question blocking that authorship. Ritual Anchor currently has no eligible ordinary Ritual-tagged payload; the three higher-rank alternative records remain unassigned; actual world/access prerequisites remain real use-time conditions. Blink is intentionally receipt-only.

No promotion, class/feat approval, source deletion, runtime/human-balance certification, DD01/whole-game closure or GitHub push is authorized. Preserve literal setting references without interpretation. Final owner whole-game flow confirmation precedes an authorized push; verified remote commit precedes careful cosmology review.
'''
(O/'README_FINAL_REVIEW.md').write_text(readme)
files=normative+['LR_137_DECISION_INDEX.md','LR_FINAL_REVIEW_RECEIPT.json','README_FINAL_REVIEW.md','build_verdict.py','export_verdict.py','read_only_source_audit.py','validate_authoring_register.py','reproduce_review.py','package_review.py','evidence/READ_ONLY_SOURCE_AUDIT.json','evidence/AUTHORING_REGISTER_AND_REFERENCE_VALIDATION.json','evidence/REPRODUCTION_PROOF.json','evidence/FULFILLED_GATE_CARRY_RECEIPT.json','evidence/SELECTED_137_ORIGINAL_RECORDS.json','evidence/GOVERNING_EXCERPTS.json','evidence/CLASS_COMPARISONS.json','evidence/COUNTERPARTS.json','evidence/SOURCE_CONFLICTS.json']
manifest={f:{'bytes':(O/f).stat().st_size,'sha256':sha(O/f)} for f in files}
(O/'FILE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
archive=Path('/mnt/data/DD_Low_Rank_137_Source_Verdict_and_Evidence.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(files+['FILE_MANIFEST.json']):z.write(O/f,f)
with zipfile.ZipFile(archive) as z:
 assert len(z.namelist())==len(files)+1
 for f,m in manifest.items():
  b=z.read(f);assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
print({'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'payloadFiles':len(files),'plusManifest':1,'verdictSha256':sha(O/'LR_137_SOURCE_AUTHORING_VERDICT.md'),'registerSha256':sha(O/'LR_137_AUTHORING_REGISTER.json')})
