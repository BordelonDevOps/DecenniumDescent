"""Correct evidence pointers without changing DE4 procedure or fixture behavior."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())
def main():
 oldp=R/'data/director/spell_proposals/divination_enchantment_rank4_current_04.json';newp=oldp.with_name('divination_enchantment_rank4_current_04a.json');report=A/'DE4_SOURCE_REFERENCE_CHECK_04A.json'
 assert not newp.exists() and not report.exists()
 old=read(oldp);d=deepcopy(old);oldbinding=info(oldp);checks=[]
 def ck(label,ok):checks.append({'check':label,'passed':bool(ok)});assert ok,label
 ck('Expected original04 bytes',oldbinding['sha256']=='67cfcb6804a9f674007373233373002a5d15489706208c3bc7362033ccaaac9a')
 oldrel=oldp.relative_to(G).as_posix();newrel=newp.relative_to(G).as_posix();wizard='DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json'
 for case in d['currentExamples']:
  for ref in case['sourceRefs']:
   if ref['path']==oldrel:ref['path']=newrel
 n24=next(c for c in d['currentExamples'] if c['id']=='DE4-N24');n25=next(c for c in d['currentExamples'] if c['id']=='DE4-N25')
 n24['sourceRefs'].append({'path':wizard,'pointer':'/engine/9','role':'Actual Abjuration specialization; no Enchantment specialist DC bonus'})
 wrong=[r for r in n25['sourceRefs'] if r['path']==wizard and r.get('pointer')=='/engine/7'];ck('One known wrong source pointer',len(wrong)==1)
 wrong[0].update(pointer='/engine/9',role='Actual Abjuration specialization; no Enchantment specialist DC bonus')
 n25['sourceRefs'].append({'path':wizard,'pointer':'/engine/11','role':'First distinct prepared Wizard matrix family has zero base Dissonance; no Refrain exemption'})
 w=read(G/wizard);ck('Specialization evidence content','ARCANE SCHOOL SPECIALIZATION' in w['engine'][9] and 'save DC' in w['engine'][9]);ck('Protected Dissonance evidence content','PROTECTED DISSONANCE INTERFACE' in w['engine'][11] and '0 BASE Dissonance' in w['engine'][11])
 changes=[]
 for b in d['sourceBindings']:
  current=info(G/b['path'])
  if current!=b:
   ck('Only accepted index changed since04',b['path']=='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
   preserved=A/'source-before-ac6-exact-acceptance-06'/b['path'];ck('Exact old binding preserved',all(info(preserved)[k]==b[k] for k in ['bytes','sha256']))
   changes.append({'before':deepcopy(b),'preservedCopy':preserved.relative_to(G).as_posix(),'after':current,'authority':info(A/'AC6_EXACT_ACCEPTANCE_06_RECEIPT.json'),'scope':'AC6 index membership accounting only; DE4 remains pending'});b.update(current)
 d.update(id='DE4-CURRENT-PROCEDURES-04A',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='Unadopted video-game candidate; 04A corrects source references only. All DE4 procedures and guard remain pending joint review.',previousDraft=oldbinding)
 d['sourceReferenceCorrections04A']={'ruleChanges':0,'fixtureBehaviorChanges':0,'previousWholeDraft':oldbinding,'previousSourceReferences':{c['id']:deepcopy(c['sourceRefs']) for c in old['currentExamples'] if c['id'] in ['DE4-N24','DE4-N25']},'correction':'Replace resolving-but-unrelated Wizard engine/7 citation with actual engine/9 and engine/11 evidence; add engine/9 to N24. All procedure text and three test vectors unchanged.','sourceBindingReconciliations':changes}
 ck('All15 full spell records unchanged',d['spells']==old['spells'] and len(d['spells'])==15)
 for key in ['sharedRules','originalExamplesUnchanged','originalSharedProposalUnchanged','originalIssuesUnchanged','currentIssuesForJointDisposition','guardAmendment','remainingJointChoices']:ck('Exact preserved '+key,d[key]==old[key])
 ck('All30 ordered IDs retained',[c['id'] for c in d['currentExamples']]==[c['id'] for c in old['currentExamples']] and len(d['currentExamples'])==30)
 for before,after in zip(old['currentExamples'],d['currentExamples']):
  ck('Fixture behavior unchanged '+before['id'],{k:v for k,v in before.items() if k!='sourceRefs'}=={k:v for k,v in after.items() if k!='sourceRefs'})
  for i,r in enumerate(after['sourceRefs']):
   if 'pointer' in r:ck('Resolved source '+after['id']+':'+str(i),at(d if r['path']==newrel else read(G/r['path']),r['pointer']) is not None)
   else:ck('Descriptive reference file '+after['id']+':'+str(i),(G/r['path']).is_file())
 for b in d['sourceBindings']:ck('Current source binding '+b['path'],info(G/b['path'])==b)
 ck('Prior04 whole bytes preserved',info(oldp)==oldbinding)
 newp.write_bytes(encoded(d));report.write_bytes(encoded({'id':'DE4-SOURCE-REFERENCE-CHECK-04A','draft':info(newp),'previousDraft':oldbinding,'checks':checks,'checkCount':len(checks),'failureCount':0,'sourceCount':len(d['sourceBindings']),'ruleChanges':0,'fixtureBehaviorChanges':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Pointer meaning for the named Wizard evidence, pointer resolution, source bindings and exact behavioral preservation; no new DE4 semantic acceptance.'}))
 print(json.dumps({'draft':info(newp),'checks':len(checks),'failures':0,'rulesChanged':0,'sourceCount':len(d['sourceBindings'])}))
if __name__=='__main__':main()
