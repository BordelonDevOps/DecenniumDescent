from pathlib import Path
import json,hashlib,zipfile,re,datetime,collections
A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game');V=A/'feat335-final-verdict-115';C=A/'feat335-corrected-candidate-114'
def j(p):return json.loads(p.read_bytes())
def h(b):return hashlib.sha256(b).hexdigest()
checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)});assert v,n
d=j(V/'DECISION.json');binding=j(V/'ARTIFACT_BINDINGS.json');ops=j(V/'CORRECTIONS.json')['operations'];ident=j(V/'IDENTITY_DISPOSITIONS.json')
raw=(A/d['input']['file']).read_bytes();ck('Exact submitted archive',len(raw)==d['input']['bytes'] and h(raw)==d['input']['sha256'])
with zipfile.ZipFile(A/d['input']['file']) as z:
 for r in binding['artifacts']:
  before=z.read(r['inputMember']);after=(C/Path(r['inputMember']).relative_to('candidate')).read_bytes()
  ck(r['inputMember']+' original binding',len(before)==r['beforeBytes'] and h(before)==r['beforeSha256'])
  ck(r['inputMember']+' selected binding',len(after)==r['selectedBytes'] and h(after)==r['selectedSha256'])
 before=z.read('candidate/docs/feats/exact-candidate-01/SPELL_PAYLOADS.md')
after=(V/'successor/SPELL_PAYLOADS.md').read_bytes();work=before
for op in sorted(ops,key=lambda o:o['beforeStartByte'],reverse=True):
 start,end=op['beforeStartByte'],op['beforeEndByte'];ck(op['id']+' exact before',work[start:end]==op['before'].encode());work=work[:start]+op['after'].encode()+work[end:]
ck('Full forward reconstruction',work==after)
for op in sorted(ops,key=lambda o:o['afterStartByte'],reverse=True):
 start,end=op['afterStartByte'],op['afterEndByte'];ck(op['id']+' exact after',work[start:end]==op['after'].encode());work=work[:start]+op['before'].encode()+work[end:]
ck('Full byte reversal',work==before)
ck('Independent114 correction equals actual final',after==(C/'docs/feats/exact-candidate-01/SPELL_PAYLOADS.md').read_bytes())
dep=j(C/'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells'];blocks=[json.loads(x) for x in re.findall(r'```json\s*\n(.*?)\n```',after.decode(),re.S)];ck('284 strict JSON blocks',len(blocks)==284)
for ob in blocks:ck('Whole current card '+ob['id'],ob==(dep[ob['id']] if ob['id']=='planar-binding' else dep[ob['id']]['completeCurrentProcedureCard']))
pub=j(C/'data/public/feat_candidates/exact_01/candidate.json');pri=j(C/'data/director/feat_candidates/exact_01/candidate.json')
def ptr(o,p):
 for k in p.strip('/').split('/'):o=o[int(k)] if isinstance(o,list) else o[k]
 return o
ck('335 unique dispositions',len(ident['identities'])==len({x['id'] for x in ident['identities']})==335)
for r in ident['identities']:
 record=ptr(pub,r['publicPointer']);ck(r['id']+' identity',record['id']==r['id'])
 if r['disposition']=='ACCEPT_EXACT_PROVISIONAL_AUTHORED_PROCEDURE':
  b=record['operationalRules'].encode();ck(r['id']+' selected full procedure',len(b)==r['completeProcedureBytes'] and h(b)==r['completeProcedureSha256'])
ck('Exact325 selected procedures',sum(r['disposition']=='ACCEPT_EXACT_PROVISIONAL_AUTHORED_PROCEDURE' for r in ident['identities'])==325)
ck('Two null wrappers remain unavailable',all(next(r for r in pri['records'] if r['id']==n)['payloadOperational'] is None for n in ['astral_projection','planar_binding']))
ck('Runtime and selection remain disabled',not pub['selectionEnabled'] and not pub['runtimeImplemented'] and not pri['selectionEnabled'] and not pri['runtimeImplemented'])
report={'id':'FEAT335-FINAL-LOCAL-ACCEPTANCE-115','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':d['verdict'],'decisionFile':str(V/'DECISION.json'),'decisionSha256':h((V/'DECISION.json').read_bytes()),'acceptedCandidate':str(C),'acceptedCandidateArchive':str(A/'DD_Feat335_Corrected_Candidate_114.zip'),'candidateFiles':46,'passed':len(checks),'failed':0,'checks':checks,'parent335ExactAuthoredReviewComplete':True,'canonicalApplied':False,'runtimeExecuted':False,'historicalCaseTestsRerun':False,'retainedHoldsFile':str(V/'HOLD_REGISTER.json')}
(A/'FEAT335_FINAL_LOCAL_ACCEPTANCE_115.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
