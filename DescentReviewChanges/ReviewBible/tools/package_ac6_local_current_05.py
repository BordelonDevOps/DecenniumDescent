"""Package the complete current candidate plus its frozen source evidence for actual GPT."""
import json,hashlib,zipfile
from pathlib import Path
from datetime import datetime,timezone
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';O=A/'ac6-local-current-05';I=A/'ac6-full-current-review-03-input'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
archive=A/'DD_AC6_Local_Current_05.zip';request=A/'AC6_LOCAL_CURRENT_05_REQUEST.txt';prep=A/'AC6_LOCAL_CURRENT_05_PREPARATION.json'
assert not any(p.exists() for p in [archive,request,prep])
check=read(A/'AC6_LOCAL_CURRENT_05_CHECK.json');assert check['failureCount']==0
message='''Continue our existing Decennium Descent AC6 review with the attached complete Local Current05 candidate. This is the next review of your actual Repair04 return, not a restart or a spell adoption.

Your exact Repair04 archive is preserved. Independent checks found one omitted history record (NX-D02) and remaining Chain Arc / Falling fixture defects. Local Current05 retains all14 identities/16 placements,103 frozen sources,22 original texts and55 ordered current cases. All unchanged rules, source/access and earlier histories remain. The eight complete candidate files are under current/; the frozen manifest and full source files are under SOURCE_MANIFEST.json and sources/. Both prior returned archives and our exact check reports are included.

Please inspect the current candidate and give an explicit evidence-based AGREE or REVISE for each AC6-L05-01..04 in REGISTER.json:
1. Exact missing NX-D02 return03 history restored; exact return04 case also retained.
2. NEW source-specific Chain Arc body-volume measurement uses one same pair of points for <=30ft distance AND clear LoE, uniformly across body sizes. N17 now enumerates every local creature (including the caster), complete arrays, fair draws, six actual saves and HP results. Please independently calculate every array, especially U excluding B/C. The old universal center-to-center endpoint bound is removed because bodies have extent.
3. Explicit NEW AC6 body-intersection suppression extends only the accepted AC5 summon convention to Air Pet, Greater Ally and Army soldier. It is not a global extended-field rule.
4. N15 gives actual paid Ready, a24.5 Reaction during the24..26 regular slot, next-round fall marker32, actual continuous sphere/body intersection during descent, Healing Rite7HP, impact3 ->4HP/Prone, and independent original expiry60. The already-damaged HP and legally resolved qualifying Null packet are stated fixture inputs, not invented attack executions. Verify accepted Ready/Falling/antimagic sources.

Our939 checks pass (189 current JSON pointers,21 descriptive source sections); they prove preservation, reference resolution and the repaired arithmetic/geometry, not all55-case semantic completeness. Please also inspect the other current procedures/cases for substantive conflicts or missing source prerequisites. Report the actual scope you checked; do not replace an unreviewed case with a generic assertion of coverage.

Return DD_AC6_Local_Current_05_Review.zip with REVIEW.json and VERDICT.md. Bind the eight exact current input files by bytes/SHA-256 and record each disposition, concrete evidence and any remaining findings. If revisions are needed, provide precise file/pointer and complete replacement text or complete changed files, preserving their old current versions. If no revision is needed, explicitly say the eight supplied files can remain byte-identical; do not reserialize them just to create new hashes. No adoption, runtime execution, human playtesting, numerical balance, cosmology canon, whole-game closure or publication approval is requested or implied.'''
request.write_text(message+'\n',encoding='utf8')
members=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(O.iterdir()):z.write(p,'current/'+p.name);members.append('current/'+p.name)
 z.write(I/'SOURCE_MANIFEST.json','SOURCE_MANIFEST.json');members.append('SOURCE_MANIFEST.json')
 for b in read(I/'SOURCE_MANIFEST.json')['bindings']:
  p=I/'sources'/b['path'];data=p.read_bytes();assert len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256'];n='sources/'+b['path'];z.writestr(n,data);members.append(n)
 for n in ['DD_AC6_Repair_04_Return.zip','DD_AC6_Full_Review_03_Return.zip','AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json','AC6_LOCAL_CURRENT_05_CHECK.json','AC6_LOCAL_CURRENT_05_REQUEST.txt']:
  z.write(A/n,'evidence/'+n);members.append('evidence/'+n)
with zipfile.ZipFile(archive) as z:assert z.namelist()==members and z.testzip() is None
record={'id':'AC6-LOCAL-CURRENT-05-PREPARATION','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'request':info(request),'candidateFiles':[info(p) for p in sorted(O.iterdir())],'independentCheck':info(A/'AC6_LOCAL_CURRENT_05_CHECK.json'),'memberCount':len(members),'frozenSourceCount':103,'status':'Complete correction candidate ready for joint review; no adoption','newSpellAdoptions':0}
prep.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'archive':info(archive),'request':info(request),'members':len(members)}))
