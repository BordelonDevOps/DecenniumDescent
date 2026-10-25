from pathlib import Path
import json, hashlib, zipfile, copy
G=Path(r'C:\Github\DecenniumDescent'); A=G/'docs/audit/2026-10-08/full-game'; D=A/'director-spell-review-129'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
q=read(A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json');g=next(x for x in q['groups'] if x['group']=='rank8-ward5')
assert g['currentPhase']=='prepared-awaiting-review'
c=read(G/g['candidate']['path']);orig=G/g['archive']['path'];assert sha(orig.read_bytes())==g['archive']['sha256']
checks=[]
with zipfile.ZipFile(orig) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
 for b in c['sourceBindings']:
  v=z.read('sources/'+b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256'];checks.append({'path':b['path'],'originalExact':True,'currentExact':sha((G/b['path']).read_bytes())==b['sha256']})
extra=[
 {'id':'RW129-ADD01','spellIds':g['identities'],'exactSourceOrConflict':'Original packet predates current applied cohorts; native238? count is not inferred. Exact232 pending-source guard has all768 native class rows and268 placements, no mismatches.','request':'Use current exact Body8/Time5/Transport6, Illusion14/Control15/Memory3 and accepted alignment/interface contexts only within their applied scopes. Resolve actual living/body lineage, observer knowledge and field geometry from those complete sources. Preserve all five current rank8/21RP rows and inaccessible alternate school placements; do not invent full spell access from a native placement alone. No pending proposal becomes authority through this comparison.','decisionSelected':False},
 {'id':'RW129-ADD02','spellIds':['antimagic-field','antilife-shell','reputation-fortress'],'exactSourceOrConflict':'Independent boundary transactions need one defined ordering when a completed teleport/body growth/field restoration changes occupancy.','request':'Author explicit finite source-local admission and restoration outcomes with actual swept body/gear volume, independent carried creatures, centers/planes/edges, real origin/destination fields and original clocks. Show distinct partial local suppression versus whole source ending. Transport6 was applied128 but does not supply a universal field-bypass or forced safe-arrival search. Require actual native source for every source exception; no infinite event oscillation, repeated blocked movement, body cutting, free ejection or free recast.','decisionSelected':False},
 {'id':'RW129-ADD03','spellIds':['alignment-immunity','mind-blank','reputation-fortress'],'exactSourceOrConflict':'A source may be mechanically protected while ordinary visible facts and historical institutional records remain true.','request':'Give complete concrete information-flow and interaction cases: genuine existing record versus blocked new magical read, friendly communication versus mind reading, currently negative standing versus hostile appearance, and ongoing versus newly prevented effects. Use actual source predicates and source-qualified actors. A source-local new taxonomy must be clearly labeled and finite; no hidden exact alignment/standing/HP detector or retrospective change to established records. Private eligibility failure retains ordinary paid-failure rules.','decisionSelected':False}
]
extra[0]['exactSourceOrConflict']='Original packet predates current applied cohorts. Exact232 pending-source guard has all768 native class rows and268 placements with no mismatches.'
specs={
'alignment-immunity':['Real source-based alignment effects with24hour original endpoint, underlying versus effective/snapshot records and actual beneficial/harmful decision.','Actual protected query/ward entry and independent nonalignment barriers, preexisting effect/suppression/expiry, no hidden diagnosis or replay.'],
'antilife-shell':['Complete actual living0HP, nonliving and carried-body classification; exact selected finite shell, initial occupancy and paid concentration.','Actual body movement, forced crossing/teleport/Falling/reach/released projectile, moving support and occupied suppressed-region restoration.'],
'antimagic-field':['Both original placement records and actual accessible selected mode, source-local lifetime and local manifestations including genuine nonspell/innate exceptions.','Two true field-family sources, establishment/overlap/removal ordering, actual outside-to-outside and inside endpoint transport and finite restoration of paid prior effects.'],
'mind-blank':['Three native source descriptions and precise currently acquired mode; actual psychic packet, separate mental control and real divination query.','Existing versus new mental effects, room/witness/record evidence and voluntary communication; actual suppression/expiry with preserved hard-control history.'],
'reputation-fortress':['Full selected faction provenance, real reputation ledger−1/0/+1 and uninitialized treatment, exact finite ward and original occupation.','Actual changes including native ReputationShield, independent companions/carried bodies/attack channels/teleport, suppressed crossing/restoration without fake disclosure or ejection.']}
cases=[{'id':'RW129-'+sid.upper()+'-'+chr(65+i),'spellId':sid,'requiredEvidence':s,'status':'REQUIRED_NEW_CASE_NOT_AUTHORED'} for sid,ss in specs.items() for i,s in enumerate(ss)]
notes={'id':'RANK8WARD5-INDEPENDENT-CONFERENCE-129','status':'PREPARED_UNSENT_NOT_ACCEPTED','identities':g['identities'],'currentAppliedCounts':{'reviewed':616,'pending':232,'acceptedUnapplied':0},'completeOriginalQuestionsUnchanged':c['questions'],'focusedAdditionalQuestions':extra,'allQuestions':c['questions']+extra,'requiredNewCases':cases,'originalFutureCaseRequirementsUnchanged':c['futureCaseRequirements'],'sourceChecks':checks,'scope':'Source/data review and preparation only. No canonical adoption, program execution, runtime/human/balance/cosmology or release claim.'}
(D/'RANK8WARD5_NEXT_CONFERENCE_NOTES_129.json').write_bytes(enc(notes));files={}
with zipfile.ZipFile(A/'DD_VitalityMatter10_Director_Conference_128.zip') as z:
 for n in z.namelist():
  if n.startswith(('accepted-context/','accepted/','current/')): files[n]=z.read(n)
files['original/'+orig.name]=orig.read_bytes();files['INDEPENDENT_QUESTIONS_129.json']=enc(notes)
guard=read(D/'PENDING232_NATIVE_SOURCE_GUARD_129.json');guard['records']=[r for r in guard['records'] if r['id'] in g['identities']];guard['scope']='Exact5native row subset of full pending232 read-only audit129; source guard only.'
files['NATIVE_SOURCE_GUARD_129.json']=enc(guard)
files['README.md']=b'Rank8 Ward5 director conference129. All5pending,26questions,10main cases plus native mode and interaction branches. Baseline616applied/232pending. Preserve original full sources and current accepted comparison scopes. No supplied/historical program execution. Exact independent acceptance required before application.\n'
man={'id':'RANK8WARD5-CONFERENCE-129-MANIFEST','files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in files.items()]}; files['MANIFEST.json']=enc(man)
out=A/'DD_Rank8Ward5_Director_Conference_129.zip'; assert not out.exists()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in files.items():z.writestr(n,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for b in man['files']:v=z.read(b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256']
r={'id':'RANK8WARD5-DIRECTOR-CONFERENCE-129','status':'PREPARED_NOT_SENT','archive':{'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes())},'members':len(files),'bindings':len(man['files']),'questions':len(notes['allQuestions']),'requiredMainCases':len(cases),'sourceChecks':len(checks),'canonicalChanges':False}
(D/'RANK8WARD5_PACKET_129.json').write_bytes(enc(r));g['currentPhase']='current-director-conference-prepared-129-unsent';(A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json').write_bytes(enc(q)); print(json.dumps(r,indent=2))
