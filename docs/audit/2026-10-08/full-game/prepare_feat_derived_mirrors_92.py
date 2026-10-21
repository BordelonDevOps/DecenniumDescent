"""Reconcile accepted FT84 wording into an isolated complete review copy.

Only this script's independent file/data operations run. No canonical file or
downloaded program is executed or modified. New renderings remain for later
parent exact review, not a promotion of335 feats or language engine changes.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json, hashlib, re, zipfile

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
P=A/'feat335-work-compositions84-part5-return-01'
ROOT=A/'feat335-ft84-derived-review-92'
OUT=A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json'
ZIP=A/'DD_Feat335_Derived_Review_Candidate_92.zip'
SAVED=A/Path(__file__).name
for p in (ROOT,OUT,ZIP,SAVED):assert not p.exists(),str(p)
def jbytes(b):return json.loads(b.decode('utf-8-sig'))
def j(p):return jbytes(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def meta(rel,b):return {'path':rel,'bytes':len(b),'sha256':sha(b)}
checks=[]
def ck(name,condition):checks.append({'check':name,'pass':bool(condition)});assert condition,name

cp=j(A/'ACTIVE_AUTHORING_CHECKPOINT_PHYSICAL_SOCIAL_RECIPES_91.json')
cp_bindings=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]
for row in cp_bindings:ck('Canonical baseline '+row['path'],info(G/row['path'])==row)
accepted=j(A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json')
ck('FT84 independent semantic acceptance449checks',accepted['passed']==449 and accepted['failed']==0 and not accepted['canonicalApplied'])
bindings=j(P/'ARTIFACT_BINDINGS.json')['files']
selected=j(P/'SELECTED_PROCEDURES.json')['procedures']
selected_by_id={r['id']:r for r in selected}
questions=j(P/'QUESTION_DISPOSITIONS.json')['questions'];q2=next(r for r in questions if r['id']=='FT84-Q02')

# Read all actual complete feat candidate artifacts and all chapter mirrors.
source_paths=set(p for directory in [R/'data/director/feat_candidates/exact_01',R/'data/public/feat_candidates/exact_01',R/'docs/feats/exact-candidate-01'] for p in directory.iterdir() if p.is_file())
source_paths.update(G/b['repositoryPath'] for b in bindings)
lang_public=R/'data/playtest/language_communication_candidate_public.json'
lang_internal=R/'data/director/language_communication_candidate_internal.json'
lang_guide=R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md'
source_paths.update([lang_public,lang_internal,lang_guide])
before={p.relative_to(G).as_posix():p.read_bytes() for p in sorted(source_paths)}
after=deepcopy(before);changes={};new_operations=[]

for row in bindings:
 rel=row['repositoryPath'];received=(P/row['after']['file']).read_bytes()
 ck('Exact whole current baseline for received successor '+row['fileKey'],len(before[rel])==row['before']['bytes'] and sha(before[rel])==row['before']['sha256'])
 ck('Received full successor binding '+row['fileKey'],len(received)==row['after']['bytes'] and sha(received)==row['after']['sha256'])
 after[rel]=received
 changes[rel]={'basis':'Exact previously independently accepted FT84 successor. Inherited51-operation proof from87/88; not rerunning supplied verifier.','origin':'received-full-artifact'}

internal_rel=(R/'data/director/feat_candidates/exact_01/candidate.json').relative_to(G).as_posix()
public_rel=(R/'data/public/feat_candidates/exact_01/candidate.json').relative_to(G).as_posix()
internal_before=jbytes(before[internal_rel]);internal_after=jbytes(after[internal_rel]);public_before=jbytes(before[public_rel]);public_after=jbytes(after[public_rel])
records_before={r['id']:r for r in internal_before['records']};records_after={r['id']:r for r in internal_after['records']}
public_records_before={r['id']:r for r in public_before['feats']};public_records_after={r['id']:r for r in public_after['feats']}
preexisting_public_differences=[rid for rid in records_before if records_before[rid]['operationalRules']!=public_records_before[rid]['operationalRules']]
ck('Exactly three preexisting copy-release public additions identified',set(preexisting_public_differences)=={'arcane_adaptation','eldritch_echo','mimicry'})
ck('327 authored identities and335 public identities remain exact',len(records_after)==327 and len(public_records_after)==335 and list(records_before)==list(records_after) and list(public_records_before)==list(public_records_after))
ck('All335 original registry entries preserved',internal_after['original335Registry']==internal_before['original335Registry'])
ck('All eight already-reviewed complete records preserved',internal_after['unchangedReviewedFeats']==internal_before['unchangedReviewedFeats'] and len(internal_after['unchangedReviewedFeats'])==8)
for rid,old in records_before.items():
 new=records_after[rid]
 ck(rid+' original complete source/question/direction preserved',all(new[k]==old[k] for k in old if k not in ('operationalRules','payloadOperational')))
 if rid in preexisting_public_differences:
  ck(rid+' preexisting public addition retained without alteration',public_records_after[rid]==public_records_before[rid] and new==old)
 else:ck(rid+' entire public procedure equals private procedure',new['operationalRules']==public_records_after[rid]['operationalRules'])
 ck(rid+' no activation/exact/runtime promotion',not new['selectionEnabled'] and not new['exactApproved'] and not new['runtimeApproved'])
 if rid in selected_by_id:
  chosen=selected_by_id[rid]
  ck(rid+' exact accepted complete before/after wording',old['operationalRules']==chosen['before'] and new['operationalRules']==chosen['after'])
 else:ck(rid+' unaffected complete row exact',old==new)

chapter_names=['COMBAT.md','CRAFTING.md','GENERAL_COMBAT.md','GENERAL_DEFENSE.md','GENERAL_EXPLORATION.md','HERITAGE_MUTATION.md','MAGIC_CORE.md','MAGIC_EXTENDED.md','SKILL.md']
chapter_rels=[(R/'docs/feats/exact-candidate-01'/name).relative_to(G).as_posix() for name in chapter_names]
def chapter_blocks(text):
 matches=list(re.finditer(r'^## [^\n]*\(`([^`]+)`\)[^\n]*$',text,re.M));result=[]
 for n,m in enumerate(matches):
  end=matches[n+1].start() if n+1<len(matches) else len(text)
  result.append((m.group(1),m.start(),end,text[m.start():end]))
 return result
def procedure_in_block(block):
 return block.split('\n\n',2)[2].split('\n### Worked examples',1)[0].strip()
original_map={}
for rel in chapter_rels:
 for rid,start,end,block in chapter_blocks(before[rel].decode('utf-8-sig')):
  ck('Unique original chapter identity '+rid,rid not in original_map)
  original_map[rid]=(rel,start,end,block)
  ck('Full original chapter procedure '+rid,procedure_in_block(block)==records_before[rid]['operationalRules'].strip())
ck('All327 original full chapter procedures covered',set(original_map)==set(records_before))
for rid,chosen in selected_by_id.items():
 rel,_,_,_=original_map[rid]
 if rel in changes:continue # CRAFTING full accepted successor already supplies its3 rows.
 text=after[rel].decode('utf-8-sig')
 matching=[x for x in chapter_blocks(text) if x[0]==rid];ck('One new mirror location '+rid,len(matching)==1)
 _,start,end,block=matching[0]
 ck('Exact new mirror before paragraph '+rid,procedure_in_block(block)==chosen['before'].strip() and block.count(chosen['before'])==1)
 replacement=block.replace(chosen['before'],chosen['after'],1)
 updated=text[:start]+replacement+text[end:]
 ck('New mirror inverse complete bytes '+rid,updated[:start]+updated[start:start+len(replacement)].replace(chosen['after'],chosen['before'],1)+updated[start+len(replacement):]==text)
 after[rel]=updated.encode()
 changes[rel]={'basis':'Exact selected full procedure inserted in the actual existing cohort chapter; unrelated paragraphs and all examples retained.','origin':'new-derived-mirror'}
 new_operations.append({'kind':'exact-text-replace','repositoryPath':rel,'withinFeatId':rid,'before':chosen['before'],'after':chosen['after']})

shared_internal_rel=(R/'data/director/feat_candidates/exact_01/shared_rules.json').relative_to(G).as_posix()
shared_public_rel=(R/'data/public/feat_candidates/exact_01/shared_rules.json').relative_to(G).as_posix()
shared_before=jbytes(before[shared_internal_rel]);shared_after=jbytes(after[shared_internal_rel])
old_rule=next(r for r in shared_before['rules'] if r['id']=='FS-14')['wording'];new_rule=next(r for r in shared_after['rules'] if r['id']=='FS-14')['wording']
public_shared_before=jbytes(before[shared_public_rel]);public_shared_after=deepcopy(public_shared_before)
ck('Public FS-14 baseline matches selected before wording',public_shared_before['rules'][13]['id']=='FS-14' and public_shared_before['rules'][13]['wording']==old_rule)
ck('Existing public shared-rule difference is only FS-08 wording',[n for n,(a,b) in enumerate(zip(shared_before['rules'],public_shared_before['rules'])) if a!=b]==[7] and len(shared_before['rules'])==len(public_shared_before['rules'])==16)
public_shared_after['rules'][13]['wording']=new_rule
reverse_shared=deepcopy(public_shared_after);reverse_shared['rules'][13]['wording']=old_rule
ck('Full unrelated public shared rules retained',reverse_shared==public_shared_before)
after[shared_public_rel]=enc(public_shared_after)
changes[shared_public_rel]={'basis':'Propagate only the exact accepted FS-14 wording into the actual full public baseline. Preserve its preexisting FS-08 copy-release addendum and every unrelated field.','origin':'new-derived-mirror'}
new_operations.append({'kind':'json-replace','repositoryPath':shared_public_rel,'pointer':'/rules/13/wording','before':old_rule,'after':new_rule})
shared_md_rel=(R/'docs/feats/exact-candidate-01/SHARED_RULES.md').relative_to(G).as_posix()
shared_md=before[shared_md_rel].decode('utf-8-sig');ck('Whole original FS-14 rendering unique',shared_md.count(old_rule)==1)
after[shared_md_rel]=shared_md.replace(old_rule,new_rule,1).encode()
ck('Full shared rendering inverse byte exact',after[shared_md_rel].decode().replace(new_rule,old_rule,1).encode()==before[shared_md_rel])
changes[shared_md_rel]={'basis':'Exact accepted FS-14 full wording propagated to its complete current public rendering.','origin':'new-derived-mirror'}
new_operations.append({'kind':'exact-text-replace','repositoryPath':shared_md_rel,'before':old_rule,'after':new_rule})

# The language public guide and embedded guideText are actual operative mirrors.
# The existing480-minute and assistant480 fields remain baseline values. Selected
# wording supplies the scoped factor/phase policy without inventing a scheduler.
lp_rel=lang_public.relative_to(G).as_posix();li_rel=lang_internal.relative_to(G).as_posix();lg_rel=lang_guide.relative_to(G).as_posix()
lp=jbytes(before[lp_rel]);li=jbytes(before[li_rel]);guide=before[lg_rel].decode('utf-8-sig')
ck('Actual language rules mirrors identical before',lp['rules']==li['rules'])
ck('Actual public language guide matches embedded text apart from existing line endings',lp['guideText'].replace('\r\n','\n')==guide.replace('\r\n','\n'))
completion={'sourceDisposition':'FT84-Q02','authority':'Independent scoped authored acceptance88; this derived file is unapplied and awaits parent exact reconciliation.','completeSelectedWording':q2['selectedWording']}
boundary={'canonicalApplied':False,'parent335Accepted':False,'runtimeImplementedByThisChange':False,'scope':'Only the exact accepted FT84-Q02 completion is added. Existing language approval flags retain their prior source scope and do not approve these newly rendered bytes or the parent335.'}
addition='\n\n## Scoped FT84 research-phase completion for parent review\n\n'+q2['selectedWording']+'\n'
file_addition=addition.replace('\n','\r\n') if '\r\n' in guide else addition
after[lg_rel]=(guide+file_addition).encode()
changes[lg_rel]={'basis':'Full exact accepted public FT84-Q02 wording appended to the actual complete current public language guide. Existing text preserved as baseline/native source.','origin':'new-derived-mirror'}
new_operations.append({'kind':'exact-text-append','repositoryPath':lg_rel,'beforePresent':False,'after':file_addition})
for rel,source_obj in [(lp_rel,lp),(li_rel,li)]:
 target=deepcopy(source_obj)
 ck('No preexisting FT84 derived property '+rel,'ft84ScopedCompletion' not in target['rules']['decipherProject'] and 'ft84DerivedReviewBoundary' not in target)
 target['rules']['decipherProject']['ft84ScopedCompletion']=deepcopy(completion)
 target['ft84DerivedReviewBoundary']=deepcopy(boundary)
 new_operations.extend([{'kind':'json-add','repositoryPath':rel,'pointer':'/rules/decipherProject/ft84ScopedCompletion','beforePresent':False,'after':completion},{'kind':'json-add','repositoryPath':rel,'pointer':'/ft84DerivedReviewBoundary','beforePresent':False,'after':boundary}])
 if rel==lp_rel:
  target['guideText']=source_obj['guideText']+addition
  new_operations.append({'kind':'json-replace','repositoryPath':rel,'pointer':'/guideText','before':source_obj['guideText'],'after':target['guideText']})
 reverse=deepcopy(target);del reverse['rules']['decipherProject']['ft84ScopedCompletion'];del reverse['ft84DerivedReviewBoundary']
 if rel==lp_rel:reverse['guideText']=source_obj['guideText']
 ck('All unrelated language fields retained '+rel,reverse==source_obj)
 after[rel]=enc(target);changes[rel]={'basis':'Explicit scoped accepted wording in the matching LA07 project plus a derived-review boundary. Whole public guide mirror updated exactly; no other native value changes.','origin':'new-derived-mirror'}
ck('Complete derived public/internal language rules identical',jbytes(after[lp_rel])['rules']==jbytes(after[li_rel])['rules'])
ck('Complete derived public language guide matches embedded text preserving native line endings',jbytes(after[lp_rel])['guideText'].replace('\r\n','\n')==after[lg_rel].decode().replace('\r\n','\n'))

final_map={}
for rel in chapter_rels:
 for rid,start,end,block in chapter_blocks(after[rel].decode('utf-8-sig')):
  ck('Unique final chapter identity '+rid,rid not in final_map);final_map[rid]=rel
  ck('Full derived chapter procedure matches complete envelope '+rid,procedure_in_block(block)==records_after[rid]['operationalRules'].strip())
  rendered_examples=block.split('### Worked examples',1)[1].strip()
  original_rendered_examples=original_map[rid][3].split('### Worked examples',1)[1].strip()
  expected_examples='\n\n'.join(records_before[rid]['workedCases']).strip()
  expected_suffix='\n\n**Unavailable payload:** retained grant wrapper only; operational payload is null.' if rid in ('astral_projection','planar_binding') else ''
  ck('Full current worked examples and null-payload notices preserved '+rid,rendered_examples==original_rendered_examples==expected_examples+expected_suffix)
ck('All nine manuscripts retain all327 identities',set(final_map)==set(records_after))

# Preserve full original and expected casebook values. This census is fidelity,
# not a claim that all660/28 cases received new semantic or runtime execution.
case_rel=(R/'data/director/feat_candidates/exact_01/example_dispositions.json').relative_to(G).as_posix()
fa_rel=(R/'data/director/feat_candidates/exact_01/additional_boundary_expectations.json').relative_to(G).as_posix()
casebook=jbytes(before[case_rel]);fa=jbytes(before[fa_rel])
ck('All660 original positions preserved byte exact',len(casebook['cases'])==660 and after[case_rel]==before[case_rel])
ck('All28 extra boundary positions preserved byte exact',len(fa['cases'])==28 and after[fa_rel]==before[fa_rel])
ck('No duplicate660 case identity',len({c['id'] for c in casebook['cases']})==660)
ck('All660 bind original authored identities',set(c['featId'] for c in casebook['cases'])==set(records_before))
ck('Full finite supplemental groups retained',after[(R/'data/director/feat_candidates/exact_01/supplements.json').relative_to(G).as_posix()]==before[(R/'data/director/feat_candidates/exact_01/supplements.json').relative_to(G).as_posix()])
for rel in before:ck('Actual source remains untouched '+rel,(G/rel).read_bytes()==before[rel])
for row in cp_bindings:ck('Final protected canonical baseline '+row['path'],info(G/row['path'])==row)

extra_paths=[P/'SELECTED_PROCEDURES.json',P/'QUESTION_DISPOSITIONS.json',P/'CASEBOOK.json',P/'HOLD_REGISTER.json',P/'JSON_POINTER_OPERATIONS.json',P/'ARTIFACT_BINDINGS.json',P/'FULL_ARTIFACT_REPLACEMENTS.json',P/'PUBLIC_SCOPED_WORDING.md',A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json',A/'DD_Feat335_Work_Compositions_84_Part5_Return_01.zip',A/'FEAT335_TIME_PROVISIONS_CASES_83.json',A/'FEAT335_WORK_COMPOSITIONS_84.json',A/'FEAT335_RESOLUTION_CASES_85.json',A/'FEAT335_HEALING_COMPOSITIONS_89.json',A/'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json',A/'FEAT335_PHYSICAL_SOCIAL_COVERAGE_QUALIFICATION_91.json',A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md']
extras={p.relative_to(G).as_posix():p.read_bytes() for p in extra_paths}
changed=sorted(rel for rel in before if before[rel]!=after[rel])
ck('Every changed file has an exact source basis',set(changed)==set(changes))
artifact_plan=[{'repositoryPath':rel,'before':meta('before/'+rel,before[rel]),'after':meta('after/'+rel,after[rel]),'changed':rel in changes,'basis':changes.get(rel,{'origin':'unchanged-current-artifact','basis':'Exact complete current bytes retained.'})} for rel in sorted(before)]
report={'id':'FEAT335-FT84-DERIVED-MIRROR-RECONCILIATION-92','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'DERIVED_REVIEW_COPY_COMPLETE_NOT_CANONICALLY_APPLIED_PARENT335_PENDING','scope':'Carry the six already accepted FT84 procedures and their exact shared/scoped wording into complete current feat/public/manuscript/language mirrors in an isolated copy. This supplies full previously unseen artifacts for later exact review, with no new mechanics or whole-parent acceptance.','inheritedAcceptance':info(A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json'),'receivedSuccessorCount':7,'newDerivedMirrorCount':len(changed)-7,'completeArtifactCount':len(before),'changedArtifactCount':len(changed),'fullArtifactPlan':artifact_plan,'newDerivedOperations':new_operations,'originalFT84Operations':info(P/'JSON_POINTER_OPERATIONS.json'),'alternativeApplicationRule':'Use the complete before/after replacement plan OR the corresponding original51 plus new mirror operations, never both for the same file. All paths here describe isolated review files; no canonical apply is authorized. Recompare complete current before-bytes before any later integration.','authoringIdentityCounts':{'internal':327,'originalRegistry':335,'public':335,'unchangedReviewed':8,'ordinaryOriginalCasePositions':660,'additionalBoundaryPositions':28,'cohortManuscripts':9,'changedFeatProcedures':6},'sourceHistory': [info(p) for p in extra_paths],'retainedHolds':j(P/'HOLD_REGISTER.json'),'remainingScope':['Full independent semantic review of all660 original expected outcomes and28 additional FA cases remains incomplete. The byte census is not that review.','The complete supplemental tables are now supplied in this isolated packet; their complete parent integration/operation review and every actual acquisition/world prerequisite remain required.','All6 proposed work selections were independently accepted88; newly rendered mirror bytes and schema annotations need parent exact reconciliation before implementation.','These source copies do not implement real acquisition, scheduler, persistence, physical world geometry, native copy/command payloads, human gameplay or balance.','Current FT84 language fields retain480-minute baseline values; the exact scoped completion controls eligible reductions/phases. This is authorship with explicit provenance, not a tested engine adapter.','Existing copied-feat preparation-only decisions and unrelated source history remain byte-exact. All prior whole-positive-case holds, remaining spell reviews and owner implementation reservation survive.'],'checks':checks,'passed':len(checks),'failed':0,'newRuleAdoptions':0,'sourceInformationDeleted':0,'canonicalImplementationApplied':False,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'humanPlaytests':0,'parent335Accepted':False,'wholeGameComplete':False,'cosmologyDecisions':0,'actuallySentToGpt':False,'acceptedButUnappliedSpellIdentities':53}
report['preexistingPublicInternalProcedureDifferences']=[{'featId':rid,'directorPointer':'/records/'+str(next(n for n,r in enumerate(internal_before['records']) if r['id']==rid))+'/operationalRules','publicPointer':'/feats/'+str(next(n for n,r in enumerate(public_before['feats']) if r['id']==rid))+'/operationalRules','status':'EXISTING_UNCHANGED_NOT_RECONCILED_BY_FT84','finding':'Public text includes the existing FEAT335-COPY-RELEASE-SOURCE-01-ADDENDUM while the director procedure and chapter retain their existing shorter procedure. Both complete versions are preserved. This packet does not supersede later copy-release or COPY-READY preparation-only successors.'} for rid in preexisting_public_differences]
report['remainingScope'].append('Three existing public/internal copy-release differences remain: arcane_adaptation, eldritch_echo and mimicry. They are preserved exactly and require the separate complete copy-release/preparation-only successor chain during parent integration; FT84 does not reconcile or approve those mirrors.')
report['preexistingPublicSharedDifference']={'ruleId':'FS-08','pointer':'/rules/7/wording','status':'EXISTING_UNCHANGED_NOT_RECONCILED_BY_FT84','finding':'Public FS-08 already has a copy-release addendum absent from the director mirror. Both complete versions are preserved; only FS-14 is changed in the public derived artifact. Separate copy-release/preparation-only successor integration remains required.'}
script=Path(__file__).read_bytes();report['independentScript']=meta(SAVED.relative_to(G).as_posix(),script)
report_bytes=enc(report) # Validate serialization before any output is created.
ROOT.mkdir()
for prefix,group in [('before',before),('after',after),('evidence',extras)]:
 for rel,raw in group.items():
  target=ROOT/prefix/rel;target.parent.mkdir(parents=True,exist_ok=True)
  with target.open('xb') as f:f.write(raw)
with SAVED.open('xb') as f:f.write(script)
with (ROOT/'RECONCILIATION.json').open('xb') as f:f.write(report_bytes)
with OUT.open('xb') as f:f.write(report_bytes)
with (ROOT/Path(__file__).name).open('xb') as f:f.write(script)
readme='''Isolated derived review copy92, not an applied repository. RECONCILIATION.json binds every complete before/after artifact and the exact six FT84 accepted procedures. All nine feat cohort chapters and all327 authored/335 public identities are present. Original660 case positions and28 extra boundaries are preserved, not newly semantically approved. Seven existing GPT successors are reused against exact live baselines; previously unseen public shared-rule, other cohort and language mirrors are newly reconciled with exact selected wording. Original source fields and every unrelated field remain preserved. All actual canonical files remain unchanged and parent335 stays unaccepted. No supplied program needs execution. Read the complete source/expected outcomes and remaining gates before any claim of completion.\n'''
with (ROOT/'README.txt').open('xb') as f:f.write(readme.encode())
files=sorted(p for p in ROOT.rglob('*') if p.is_file())
manifest={'id':'FEAT335-DERIVED92-MANIFEST','files':[meta(p.relative_to(ROOT).as_posix(),p.read_bytes()) for p in files]}
with (ROOT/'MANIFEST.json').open('xb') as f:f.write(enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 for row in manifest['files']:
  raw=z.read(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'checks':len(checks),'failures':0,'completeArtifacts':len(before),'changedArtifacts':len(changed),'newMirrors':len(changed)-7,'archiveMembers':len(manifest['files'])+1,'canonicalApplied':False},indent=2))
