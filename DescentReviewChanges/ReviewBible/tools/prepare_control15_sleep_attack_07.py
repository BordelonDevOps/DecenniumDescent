"""Repair an attack modifier in a preserved current Mass Sleep fixture."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def main():
 oldp=R/'data/director/spell_proposals/control_15_current_06.json';out=oldp.with_name('control_15_current_07.json');report=A/'CONTROL_15_SLEEP_ATTACK_CHECK_07.json'
 assert not out.exists() and not report.exists();old=json.loads(oldp.read_bytes());d=deepcopy(old);i=next(i for i,c in enumerate(d['currentExamples']) if c['id']=='EN5-02-B');c=d['currentExamples'][i]
 before='Perceived unconsciousWizard20ftaway gives attackadvantage;d20faces[8,15]select15,+6=21hitsAC12.'
 after='The actual sleeping recipient is also Prone. At20ft, Unconscious attack advantage and Prone disadvantage cancel; roll one ordinary d20face15,+6=21hitsAC12.'
 assert before in c['actionsAndResolution'][1]
 d['previousChangedCaseRecords07']=[{'source':info(oldp),'pointer':f'/currentExamples/{i}','reason':'Include actual Prone disadvantage at ranged distance; it cancels Unconscious advantage. Fixed single face15 preserves hit21 and original damage/wake result.','completePreviousCurrentCase':deepcopy(c)}]
 c['actionsAndResolution'][1]=c['actionsAndResolution'][1].replace(before,after)
 c['currentRepair07']='The original scenario text remains exact. This correction changes only the attack-roll procedure; all original and current resulting HP/temp/wake/source-history outcomes remain unchanged.'
 d['previousCompleteDraft']=info(oldp);d['sourceBindings'].append(info(oldp));d.update(id='CONTROL-15-CURRENT-07',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='UNSENT UNADOPTED assembly:15 unchanged full procedures,22 of30 current original vectors/8 remaining. Mass Sleep ranged attack uses actual opposing condition modifiers; full prior current case preserved.')
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 for k in ['spells','originalExamplesUnchanged','completeOriginalSharedProposals','memorySourcesSeparated','remainingOriginalCaseIds']:ck('Full unchanged '+k,d[k]==old[k])
 ck('Outcomes unchanged',c['expectedBranches']==old['currentExamples'][i]['expectedBranches'])
 ck('All other cases unchanged',all(x==old['currentExamples'][j] for j,x in enumerate(d['currentExamples']) if j!=i))
 ck('Correct ordinary hit',15+6==21 and 21>=12)
 for b in d['sourceBindings']:ck('Exact current full source '+b['path'],info(G/b['path'])==b)
 out.write_bytes(encoded(d));report.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'candidate':info(out),'checks':len(checks),'currentVectors':22,'remaining':8}))
if __name__=='__main__':main()
