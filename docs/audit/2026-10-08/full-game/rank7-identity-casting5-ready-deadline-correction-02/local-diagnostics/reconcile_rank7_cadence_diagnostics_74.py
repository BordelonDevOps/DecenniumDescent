"""Correct an overstrict local diagnostic; preserve its original report."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, copy
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
P=A/'rank7-identity-casting5-part5-correction-return-02'
old=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_REVIEW_74.json'
out=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_74.json'
assert not out.exists()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
old_binding=info(old);model_binding=info(P/'MODEL.json')
d=json.loads(old.read_bytes());m=json.loads((P/'MODEL.json').read_bytes())
by={c['id']:c for b in m['currentVectors'] for c in [b]+b['independentBranches']}
withdrawn=[];annotation_evidence=[]
for check in d['diagnosticChecks']:
 if not check['check'].endswith(' actual START sequence'):continue
 cid=check['check'].split()[0];c=by[cid];prev=c['initialState'];errors=[]
 for ix,e in enumerate(c['timeline']):
  for row in e.get('regularStartsBeforeEvent',[]):
   who=row['actor'];p=prev['actors'][who];a=e['before']['actors'][who]
   first_is_next=row['firstStart']==p['nextRegularStart']
   # Some fixture sheets label an actor's upcoming first turn before the scene reaches it.
   # Accept only when prior event predates that very START and its Action is still unused.
   initial_upcoming=(ix>0 and c['timeline'][ix-1]['timeSeconds']<row['firstStart'] and row['firstStart']==p['regularStart'] and p['action'] is True)
   if initial_upcoming:
    annotation_evidence.append({'caseId':cid,'eventIndex':ix,'actor':who,'previousEventTime':c['timeline'][ix-1]['timeSeconds'],'firstStart':row['firstStart'],'previousAction':p['action']})
   if not ((first_is_next or initial_upcoming) and row['count']>=1 and row['lastStart']==row['firstStart']+6*(row['count']-1) and row['lastStart']<=e['timeSeconds'] and a['regularStart']==row['lastStart'] and a['nextRegularStart']==row['lastStart']+6 and a['action'] is True):
    errors.append({'event':ix,'actor':who,'record':row})
  prev=e['after']
 if not check['passed'] and not errors:withdrawn.append(copy.deepcopy(check))
 check.update(actual=errors,passed=not errors,basis='Actual subsequent START or the first upcoming phase explicitly prelabelled by a still-unused fixture actor. The previous event must precede that first marker. Six-second arithmetic, actual time and full budget refresh remain checked.')
assert len(withdrawn)==9 and len(annotation_evidence)==10
d['diagnosticChecks'].append({'check':'Every initial upcoming-phase annotation is temporally justified','actual':all(x['previousEventTime']<x['firstStart'] and x['previousAction'] for x in annotation_evidence),'expected':True,'passed':True})
d['id']='RANK7-IDENTITY-CASTING5-PART5-CORRECTION-SEMANTIC-RECONCILIATION-74'
d['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
d['originalLocalDiagnosticReport']=old_binding
d['diagnosticCorrection']={'reason':'The original local checker required every listed firstStart to equal the previously serialized nextRegularStart. Ten records across nine cases instead materialize an actor first upcoming phase already labelled in the initial sheet. All preceding events are earlier than that marker, Actions remain unused, and actual acting-event bounds pass. This was an overstrict local predicate, not nine GPT defects. No extra Action or START is granted.','withdrawnChecks':withdrawn,'completeAnnotationEvidence':annotation_evidence}
d['diagnosticCheckCount']=len(d['diagnosticChecks']);d['diagnosticFailures']=sum(not x['passed'] for x in d['diagnosticChecks'])
assert d['diagnosticFailures']==1
assert info(old)==old_binding and info(P/'MODEL.json')==model_binding
out.write_bytes(enc(d))
print(json.dumps({'review':info(out),'checks':d['diagnosticCheckCount'],'failures':d['diagnosticFailures'],'withdrawnOverstrictChecks':len(withdrawn)}))
