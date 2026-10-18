"""Rebind active pending cohorts to actual DE4 adoption, preserving complete prior drafts."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
def read(p):return json.loads(p.read_bytes())
def main():
 report=A/'PENDING_COHORTS_AFTER_DE4_07_CHECK.json';assert not report.exists();checks=[];results=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 pairs=[('damage_control_25_current_06.json','damage_control_25_current_07.json'),('persistent_damage_20_current_04.json','persistent_damage_20_current_05.json'),('illusion_perception_14_current_03.json','illusion_perception_14_current_04.json')]
 P=R/'data/director/spell_proposals';regold=R/'data/director/spell_review/accepted_interface_registry_03.json';regnew=regold.with_name('accepted_interface_registry_04.json');invold=regold.with_name('ordinary_spell_inventory_02.json');invnew=invold.with_name('ordinary_spell_inventory_03.json');receipt=A/'DE4_EXACT_ACCEPTANCE_07_RECEIPT.json';model=R/'data/public/spell_candidates/divination_enchantment_rank4_reviewed_07.json';remap={regold.relative_to(G).as_posix():regnew.relative_to(G).as_posix(),invold.relative_to(G).as_posix():invnew.relative_to(G).as_posix()}
 for oldname,newname in pairs:
  oldp=P/oldname;out=P/newname;ck('New successor absent '+newname,not out.exists());old=read(oldp);d=deepcopy(old);oldself=oldp.relative_to(G).as_posix();newself=out.relative_to(G).as_posix()
  previous=deepcopy(d['sourceBindings']);changes=[];bindings={}
  for b in previous:
   path=remap.get(b['path'],b['path']);p=G/path;new=info(p);bindings[path]=new
   if new!=b:changes.append({'before':b,'after':new,'reason':'Actual exact DE4 application/current registry refresh; complete prior draft and pre-application bytes remain preserved.'})
  for p in [oldp,receipt,model,regnew,invnew,A/'DE4_EXACT_ACCEPTANCE_07_APPLICATION_CHECK.json',A/'DE4_REGISTRY_INVENTORY_REFRESH_04_CHECK.json']:bindings[info(p)['path']]=info(p)
  # Rewrite only operative references; complete original/history objects remain untouched.
  skipped={'completeSourceAndAccess','completeEarlierRecordUnchanged','originalSourceReference','historicalProposalUnchanged','originalQuestion','previousStructuredAlternative01','originalAuthoredProposalUnchanged','originalSharedProposalUnchanged','priorProposalBinding','historicalReconciliation','originalExamplesUnchanged','completeOriginalSharedProposals','creationSeparate','previousChangedCaseRecords03','previousCompleteDraft','previousDraft','sourceBindings','historicalReconciliations','originalCohortCasesUnchanged','previousCurrent01CasesUnchanged','previousChangedSpellRecords','previousChangedCaseRecords'}
  def refs(v):
   if isinstance(v,dict):
    if isinstance(v.get('path'),str):
     original=v['path'];path=newself if original==oldself else remap.get(original,original);v['path']=path
     if all(k in v for k in ['bytes','sha256']) and path!=newself and (G/path).is_file():
      if original in {b['path'] for b in previous}:v.update(info(G/path))
    for k,z in v.items():
     if k not in skipped:refs(z)
   elif isinstance(v,list):
    for z in v:refs(z)
  refs(d)
  d['sourceBindings']=list(bindings.values());d['previousCompleteDraft']=info(oldp);d['de4AdoptionReferenceRefresh']={'status':'References refreshed after actual acceptance; this pending cohort gains no approval.','receipt':info(receipt),'registry':info(regnew),'inventory':info(invnew),'previousSourceBindings':previous,'currentBindingChanges':changes,'authoredCounts':{'reviewed':480,'pending':368},'originalProceduresChangedByRefresh':0,'newAuthorshipAcceptedByRefresh':0,'scope':'DE4 three-spell lineage/RNG/disclosure and its own source procedures now have actual scoped acceptance. No ordinary case grants a sixth disclosure entry. Phantom Swarm, persistent damage, illusion channels, mount choices and all other proposed cross-source extensions still require independent conference.','historicalReferencePolicy':'Earlier full drafts and their bindings describe pre-adoption evidence. Current bindings/index/registry govern current comparisons; prior complete objects remain unchanged.'}
  d['id']=d['id'].rsplit('-',1)[0]+'-'+newname.rsplit('_',1)[1].split('.')[0];d['recordedAtUtc']=datetime.now(timezone.utc).isoformat();d['status']='UNSENT, UNADOPTED current proposal. References refreshed after verified DE4 application; procedures, scenario outcomes and original source records unchanged. '+old['status']
  ck('All complete procedures unchanged '+newname,[s['procedure'] for s in d['spells']]==[s['procedure'] for s in old['spells']]);ck('Full source access unchanged '+newname,[s['completeSourceAndAccess'] for s in d['spells']]==[s['completeSourceAndAccess'] for s in old['spells']])
  for key in ['originalExamplesUnchanged','originalCohortCasesUnchanged','previousCurrent01CasesUnchanged','completeOriginalSharedProposals']:
   if key in old:ck('Complete historical field unchanged '+newname+key,d[key]==old[key])
  for b in d['sourceBindings']:ck('Current binding exact '+newname+' '+b['path'],info(G/b['path'])==b)
  # Operative source JSON pointers must still resolve, including stable inherited registry indexes.
  def checkrefs(v):
   if isinstance(v,dict):
    if isinstance(v.get('path'),str) and isinstance(v.get('pointer'),str) and v['path'].endswith('.json'):
     p=G/v['path'];obj=d if v['path']==newself else read(p);at(obj,v['pointer']);ck('Current pointer '+newname+' '+v['path']+v['pointer'],True)
    for k,z in v.items():
     if k not in skipped and k!='de4AdoptionReferenceRefresh':checkrefs(z)
   elif isinstance(v,list):
    for z in v:checkrefs(z)
  checkrefs(d);out.write_bytes(encoded(d));results.append({'previous':info(oldp),'candidate':info(out),'currentBindingChanges':changes})
 report.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'results':results,'checks':checks,'checkCount':len(checks),'failureCount':0,'proceduresChanged':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'results':[{k:v for k,v in x.items() if k!='currentBindingChanges'} for x in results],'checks':len(checks),'report':info(report)}))
if __name__=='__main__':main()
