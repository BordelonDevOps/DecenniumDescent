"""Preserved-input/current-authority supplement for a new, nonidentical bestiary return."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';RF=A/'rank9-resonance-fields3-feedback-receipt-return-02';FT=A/'feat335-work-compositions84-part5-return-01'
ROOT=A/'bestiary-replacement-context-96';ZIP=A/'DD_Bestiary_Replacement_Current_Context_96.zip';OUT=A/'BESTIARY_REPLACEMENT_CONTEXT_PREPARATION_96.json';SAVED=A/Path(__file__).name
for p in (ROOT,ZIP,OUT,SAVED):assert not p.exists(),str(p)
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
external=[(A/'DD_Bestiary_Complete_Source_Prepared_v3_81.zip',42404028,'a07245c72cfbe44079d9addcf1376f3d7f9c8a7ad1b3a6cee442f2964fb1a15b'),(A/'DD_Bestiary_Current_EX58_Context_82.zip',3510131,'424be66594e6acdea09f640e3e6e64af997cd56805852beb6e451081de0aa334'),(A/'DD_Bestiary_Linked_Recipe_Dependencies_91.zip',564856,'019ef9001fa948d02c1df0bb60bf7195bcbfa83485b2e9efaa5c85a4b8c6dd58')]
for p,n,h in external:ck('Complete original/supplement source '+p.name,info(p)['bytes']==n and info(p)['sha256']==h)
paths=[A/'GPT_BESTIARY_COMPLETED_RESPONSE_96.txt',A/'GPT_BESTIARY_COMPLETED_NATIVE_96.json',A/'GPT_BESTIARY_DELIVERY_UNAVAILABLE_RESPONSE_96.txt',A/'GPT_BESTIARY_DELIVERY_UNAVAILABLE_NATIVE_96.json',A/'CODEX_BESTIARY_ACTUAL_DISPATCH_REQUEST_89.txt',A/'CODEX_BESTIARY_DELIVERY_REPAIR_REQUEST_96.txt',A/'CODEX_RESONANCE_ACCEPTANCE_FOLLOWUP_90.txt',A/'RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json',A/'RANK9_RESONANCE_FIELDS3_RECEIPT_SEMANTIC_RECONCILIATION_90.json',A/'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json',A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json',A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json',A/'BESTIARY_LINKED_RECIPE_DEPENDENCIES_91_PREPARATION.json',A/'ACTIVE_AUTHORING_CHECKPOINT_CRAFTING_CASEBOOK_95.json']
paths += [RF/n for n in ['MODEL.json','PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','HOLD_REGISTER.json','FEEDBACK_RECEIPT_CONTRACT.json','ALL_MAGIC_CATEGORY_MAP.json','SOURCE_AUTHORITY.json','SOURCE_BINDING_VERIFICATION.json','SOURCE_REFERENCES.json','IMPLEMENTATION_BOUNDARIES.json','ORIGINAL_HISTORY.json']]
paths += [FT/n for n in ['MODEL.json','SELECTED_PROCEDURES.json','QUESTION_DISPOSITIONS.json','HOLD_REGISTER.json','CASEBOOK.json','CONSTRUCTION_CATEGORY_MAP.json','SOURCE_BINDINGS.json','SOURCE_EXCERPTS.md']]
source_bytes={p.relative_to(G).as_posix():p.read_bytes() for p in paths};accept=j(A/'RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json')
ck('Full exact accepted Resonance MODEL matches acceptance',info(RF/'MODEL.json')==accept['selectedSuccessor'])
ck('FT84 full selected MODEL unchanged',info(FT/'MODEL.json')['sha256']=='758ab64c8948d1112f16a397da71082256c3d5a7c27442e453b6f737317971d2')
ck('Accepted53 not applied',accept['resultingAcceptedButUnapplied']==53 and not accept['implementationApplied'])
readme='''Bestiary replacement current context96 — read this first.

The previous proposed Bestiary Return01 has NOT been delivered or independently accepted. Its complete final response is historical evidence of proposed decisions and claimed artifacts, NOT recoverable complete MODEL/case/manuscript bytes. The later GPT delivery-repair response explicitly reports the generated archive, folder, MODEL, manifest and cases unavailable. Do not claim byte-identical recovery, reuse the lost MODEL hash as a new result, or describe its reported test counts as independent local evidence. Preserve both full responses and original user request.

Create a newly identified Return02 from the complete original V3 and EX58 archives already attached to this chat, plus the separately attached complete linked-recipe dependency91 archive and this current-authority supplement. All original files remain preserved locally at the manifest-bound paths. No previous successful program may be rerun; do not execute supplied code. New authoring/verification code must be separate and all new proposals must remain distinguishable from old response-only descriptions.

The original source request retains its full scope: all67 dossiers/66 printed profiles,162 actions,42 multiattacks,178 harvest occurrences,707 bindings,184 history differences,27 new questions and every retained source/runtime/history/crafting question and interface. Five sealed dossiers remain containment/routing only, not creature-content review or new public disclosure. All original values and sources survive; the lost response cannot substitute for missing full procedures. Current expected trait count and average observations must be measured independently from actual inputs.

The current exact Resonance Fields3 MODEL and its complete procedures/shared rules/question dispositions/holds/receipt contract are supplied with independent acceptance90 and semantic/intake evidence. Only the specifically discharged local acceptance hold changes; no canonical integration or other hold is cleared. Applied525/323/249/173 stays fixed and accepted-unapplied is53. Original archives supporting that accepted spell history remain preserved at acceptance-record paths; this supplement is not falsely presented as containing those large archives.

The full accepted FT84 MODEL, six before/after procedures, three question dispositions, casebook and hold register are supplied. Their scoped acceptance88 and derived-mirror review92 remain distinct from pending parent335 approval. Do not treat candidate integration labels or the isolated mirrors as owner-authorized canonical implementation.

Linked recipe91 supplies the actual missing full public Fishing sources and complete Cooking sources. Use recipe173's exact Rod-only Refined Verdant Tackle and recipe92's actual feast profile; historical boat name and matching material words do not create bodies, ingredients or entitlement. The later complete recipe sources resolve an input omission, not a new creature/crafting benefit. All unmatched links still need finite explicit disposition.

All canonical, runtime, human-play, numerical-balance, cosmology and release gates remain separate. Return new complete authoring artifacts with full source bindings and exact reversible references to the preserved original source model, plus adequate actual positive encounter/state cases and explicit unexercised boundaries. Verify actual final files exist and hashes immediately before delivery. A unavailable return must be reported as unavailable, not replaced by fabricated download links.
'''
ROOT.mkdir()
for rel,b in source_bytes.items():
 p=ROOT/'sources'/rel;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
with (ROOT/'README.txt').open('xb') as f:f.write(readme.encode())
with (ROOT/'EXTERNAL_COMPLETE_ARCHIVES.json').open('xb') as f:f.write(enc({'archives':[info(p) for p,_,_ in external],'delivery':'V3 and EX58 already attached and GPT confirmed accessible; linked recipe91 is supplied as a separate new attachment. These archives are not duplicated inside this context ZIP.'}))
files=sorted(p for p in ROOT.rglob('*') if p.is_file());manifest={'id':'BESTIARY-REPLACEMENT-CURRENT-CONTEXT-96','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
with (ROOT/'MANIFEST.json').open('xb') as f:f.write(enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 ck('ZIP unique members',len(z.namelist())==len(set(z.namelist())))
 ck('ZIP CRC',z.testzip() is None)
 for r in manifest['files']:ck('Archive complete bytes '+r['path'],len(z.read(r['path']))==r['bytes'] and sha(z.read(r['path']))==r['sha256'])
for rel,b in source_bytes.items():ck('Original source remains unchanged '+rel,(G/rel).read_bytes()==b)
report={'id':'BESTIARY-REPLACEMENT-CONTEXT-PREPARATION-96','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'NEW_FULL_CURRENT_CONTEXT_PREPARED_NOT_SENT','archive':info(ZIP),'sourceBindings':[info(p) for p in paths],'externalCompleteArchives':[info(p) for p,_,_ in external],'fullSourceFiles':len(paths),'archiveMembers':len(manifest['files'])+1,'lostReturnResponse':'Historical proposed response preserved, full generated artifacts reported unavailable; no receipt or independent acceptance','checks':checks,'passed':len(checks),'failed':0,'actuallySentToGpt':False,'canonicalApplied':False,'sourceInformationDeleted':0,'downloadedCodeExecuted':False}
with OUT.open('xb') as f:f.write(enc(report))
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'preparation':info(OUT),'archive':info(ZIP),'sources':len(paths),'members':report['archiveMembers'],'checks':len(checks),'failed':0},indent=2))
