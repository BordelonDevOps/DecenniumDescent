"""Repair frozen guide locations without changing any proposed rule or case."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
 oldp=R/'data/director/spell_proposals/illusion_perception_14_current_10.json';out=oldp.with_name('illusion_perception_14_current_11.json');report=A/'ILLUSION_PERCEPTION_14_BINDING_CHECK_11.json';assert not out.exists() and not report.exists()
 old=json.loads(oldp.read_bytes());d=deepcopy(old);reg=json.loads((R/'data/director/spell_review/accepted_interface_registry_04.json').read_bytes());changes=[];checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 for e in d['currentAcceptedInterfaceComparisons']:
  current=reg['entries'][int(e['registryPointer'].split('/')[-1])]
  if e['completeEntry']!=current:
   before=deepcopy(e['completeEntry']);ck('Unchanged exact authority '+e['registryPointer'],before['exactAuthority']==current['exactAuthority']);changes.append({'pointer':e['registryPointer'],'completePreviousEntry':before,'completeCurrentEntry':deepcopy(current),'reason':'Whole-file binding had been refreshed in Current04 but its historical frozenCopy location still pointed to the old guide. Use the complete exact Registry04 entry; no authority text changes.'});e['completeEntry']=deepcopy(current)
  source=current['currentAuthoritativeSource'];frozen=G/source['frozenCopy'];ck('Exact frozen authority bytes '+e['registryPointer'],info(frozen)['sha256']==source['sha256'] and info(frozen)['bytes']==source['bytes'])
 ck('Exactly three guide frozen locations corrected',len(changes)==3)
 d['bindingCorrection11']={'changes':changes,'scope':'Reference-only. Original Current10 and its prepared UNSENT archive remain unchanged. All rules, cases, original source/access,28original texts,3supplements and16conference questions remain identical.'};d['previousCompleteDraft']=info(oldp);d['sourceBindings'].append(info(oldp));d.update(id='ILLUSION-PERCEPTION-14-CURRENT-11',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status=old['status']+' Current11 corrects three guide frozen-copy locations only.')
 for k in ['spells','currentExamples','originalExamplesUnchanged','supplementalVectors09','conferenceDecisions10','sharedContractRouting10','creationSeparate']:ck('Complete unchanged '+k,d[k]==old[k])
 for bind in d['sourceBindings']:ck('Current source '+bind['path'],info(G/bind['path'])==bind)
 out.write_bytes(encoded(d));report.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'candidate':info(out),'checks':len(checks)}))
if __name__=='__main__':main()
