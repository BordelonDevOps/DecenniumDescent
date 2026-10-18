"""Apply the single final Followup06 wording correction to a new pending draft."""
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def main():
 oldp=R/'data/director/spell_proposals/divination_enchantment_rank4_current_06.json';newp=oldp.with_name('divination_enchantment_rank4_current_07.json');checkp=A/'DE4_CURRENT_07_CHECK.json';review=A/'de4-review-followup-06-review-final'
 assert not newp.exists() and not checkp.exists()
 old=json.loads(oldp.read_bytes());d=deepcopy(old);ops=json.loads((review/'PROPOSED_CORRECTIONS.json').read_bytes());assert info(oldp)==ops['reviewedCandidateBinding'];assert len(ops['operations'])==1
 o=ops['operations'][0];assert o['pointer']=='/currentExamples/3/initialState' and o['file']==info(oldp)['path'];node,key=parent(d,o['pointer']);assert node[key]==o['before'];assert hashlib.sha256(o['after'].encode()).hexdigest()==o['afterUtf8Sha256'];node[key]=o['after']
 d['previousCompleteDraft']=info(oldp);d['previousChangedCaseRecords07']=[deepcopy(old['currentExamples'][3])]
 oldrel=info(oldp)['path'];newrel=newp.relative_to(G).as_posix()
 for c in d['currentExamples']:
  for ref in c.get('sourceRefs',[]):
   if ref['path']==oldrel:ref['path']=newrel
 d.update(id='DE4-CURRENT-PROCEDURES-07',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='UNADOPTED exact N04 wording correction after four substantive deltas agreed by actual GPT; final rebound-file acceptance remains pending.')
 d['directorReview07']={'review':info(review/'REVIEW.json'),'corrections':info(review/'PROPOSED_CORRECTIONS.json'),'receipt':info(A/'DE4_REVIEW_FOLLOWUP_06_FINAL_RECEIPT.json'),'disposition':'Four substantive deltas AGREE. One N04 adjective corrected exactly here. No new mechanism.','remainingRequirement':'Exact final rebinding and authored-file acceptance.'}
 d['remainingJointChoices']=['Confirm the single exact N04 wording correction and final rebound artifacts; settled substantive cohort and AC6 decisions are retained.']
 for p in [oldp,review/'REVIEW.json',review/'PROPOSED_CORRECTIONS.json',A/'DE4_REVIEW_FOLLOWUP_06_FINAL_RECEIPT.json']:
  if info(p)['path'] not in {b['path'] for b in d['sourceBindings']}:d['sourceBindings'].append(info(p))
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 ck('All complete procedures identical',d['spells']==old['spells']);ck('All shared rules identical',d['sharedRules']==old['sharedRules']);ck('All30 exact original texts',d['originalExamplesUnchanged']==old['originalExamplesUnchanged']);ck('All37 ordered current cases',[c['id'] for c in d['currentExamples']]==[c['id'] for c in old['currentExamples']])
 for i,(c,p) in enumerate(zip(d['currentExamples'],old['currentExamples'])):
  v=deepcopy(c)
  for ref in v.get('sourceRefs',[]):
   if ref['path']==newrel:ref['path']=oldrel
  if i==3:v['initialState']=o['before']
  ck('Only prescribed case delta '+c['id'],v==p)
 for b in d['sourceBindings']:ck('Frozen source '+b['path'],info(G/b['path'])==b)
 for c in d['currentExamples']:
  for ref in c.get('sourceRefs',[]):
   if 'pointer' in ref:ck('Case pointer '+c['id']+ref['pointer'],at(d if ref['path']==newrel else json.loads((G/ref['path']).read_bytes()),ref['pointer']) is not None)
 newp.write_bytes(encoded(d));checkp.write_bytes(encoded({'id':'DE4-CURRENT-07-CHECK','candidate':info(newp),'checks':checks,'checkCount':len(checks),'failureCount':0,'changedRules':0,'activeFilesModified':0,'newSpellAdoptions':0,'counts':{'reviewed':465,'pending':383}}));print(json.dumps({'candidate':info(newp),'checks':len(checks)}))

if __name__=='__main__':main()
