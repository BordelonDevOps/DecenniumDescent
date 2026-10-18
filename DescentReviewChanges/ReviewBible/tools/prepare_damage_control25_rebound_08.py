"""Apply verified GPT proposals only to a new pending candidate; retain all before bytes."""
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def read(p):return json.loads(p.read_bytes())
def main():
 oldp=R/'data/director/spell_proposals/damage_control_25_current_07.json';out=oldp.with_name('damage_control_25_current_08.json')
 reviewdir=A/'damage-control25-conference-07-review';zipfile=A/'DD_Damage_Control_25_Conference_07_Review.zip';native=A/'DAMAGE_CONTROL_25_CONFERENCE_07_ACTUAL_GPT_FINAL.json';receipt=A/'DAMAGE_CONTROL_25_CONFERENCE_07_RECEIPT.json';checkp=A/'DAMAGE_CONTROL_25_REBOUND_08_CHECK.json'
 assert not any(p.exists() for p in [out,receipt,checkp]);checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 ck('Actual final review archive',info(zipfile)['bytes']==230039 and info(zipfile)['sha256']=='7becf73c3e85b9cfc064201e0234f63970d510096b03f581d0333b410722c0ba')
 manifest=read(reviewdir/'EVIDENCE_MANIFEST.json');review=read(reviewdir/'REVIEW.json');patch=read(reviewdir/'PROPOSED_CORRECTIONS.json');old=read(oldp)
 ck('Current candidate reviewed exact',info(oldp)==manifest['reviewedCandidate'])
 for f in manifest['outputFiles']:
  b=info(reviewdir/f['name']);ck('Actual final companion '+f['name'],b['bytes']==f['bytes'] and b['sha256']==f['sha256'])
 n=read(native);messages=[item for turn in n['turns'] for item in turn['items'] if item['type']=='agentMessage'];actual=next(x for x in messages if x['id']=='2c3a231c-f1f7-42b7-ae87-649bde455583')
 ck('Actual final assistant binds archive','7becf73c3e85b9cfc064201e0234f63970d510096b03f581d0333b410722c0ba' in actual['text'])
 ck('Full review scope',len(review['perSpellDispositions'])==25 and len(review['conferenceDecisionDispositions'])==9 and len(patch['operations'])==23)
 d=deepcopy(old);oprecords=[]
 for o in patch['operations']:
  ck('Only explicit replacement '+o['id'],o['op']=='replace' and o['targetFile']==oldp.relative_to(G).as_posix())
  ck('Whole before precondition '+o['id'],at(d,o['pointer'])==o['before']);par,key=parent(d,o['pointer']);par[key]=deepcopy(o['after']);oprecords.append({'id':o['id'],'pointer':o['pointer'],'classification':o['classification'],'reason':o['reason'],'completePreviousValue':deepcopy(o['before']),'completeProposedValue':deepcopy(o['after'])})
 reverse=deepcopy(d)
 for o in reversed(patch['operations']):
  ck('Whole reverse after precondition '+o['id'],at(reverse,o['pointer'])==o['after']);par,key=parent(reverse,o['pointer']);par[key]=deepcopy(o['before'])
 ck('Full reverse replay equals Current07',reverse==old)
 for j,s in enumerate(d['spells']):
  for key in ['id','name','completeSourceAndAccess','sourcePointer','originalAuthoredProposalUnchanged','originalSharedProposalUnchanged','previousStructuredAlternative01','priorProposalBinding','historicalReconciliation']:
   if key in old['spells'][j]:ck('Preserved complete source/history '+s['id']+' '+key,s[key]==old['spells'][j][key])
 for key in ['identities','placements','originalCohortCasesUnchanged','historicalReconciliations','currentDigitalVectors','currentCases','mixedDefenseOptionVectors04']:ck('Complete unchanged '+key,d[key]==old[key])
 ck('Highrank IDs/order unchanged',[x['id'] for x in d['highRankCurrentVectors05']]==[x['id'] for x in old['highRankCurrentVectors05']])
 ck('Only HR04-B existing highrank vector changed',[j for j,(x,y) in enumerate(zip(d['highRankCurrentVectors05'],old['highRankCurrentVectors05'])) if x!=y]==[7])
 d['conference07ChangedBeforeValues']=oprecords
 d['directorProposedWorkedSupplementsUnchanged']=deepcopy(review['newConferenceWorkedSupplements']);d['currentConferenceWorkedSupplements08']=deepcopy(review['newConferenceWorkedSupplements']);fixes=[]
 def textfix(cid,fields):
  c=next(x for x in d['currentConferenceWorkedSupplements08'] if x['id']==cid);before=deepcopy(c)
  for pointer,prior,new in fields:
   value=at(c,pointer);ck('Supplement exact before '+cid+pointer,value==prior);par,key=parent(c,pointer);par[key]=deepcopy(new)
  c['codexAmendmentStatus08']='PROPOSED local correction pending actual GPT concurrence; original complete Director example preserved unchanged.'
  fixes.append({'id':cid,'completePreviousDirectorExample':before,'completeProposedCurrentExample':deepcopy(c)})
 s1=next(x for x in d['currentConferenceWorkedSupplements08'] if x['id']=='DC25-P01')
 textfix('DC25-P01',[
  ('/initialState/caster',s1['initialState']['caster'],s1['initialState']['caster'].replace('HP70/max70, CON+2','HP68/max68 using actual d6 first-level6+CON2 and10 later fixed4+CON2, CON+2')),
  ('/orderedAdjudication/1',s1['orderedAdjudication'][1],s1['orderedAdjudication'][1].replace('70->55','68->53')),
  ('/expectedState/casterHP',55,53)])
 s2=next(x for x in d['currentConferenceWorkedSupplements08'] if x['id']=='DC25-P02')
 textfix('DC25-P02',[
  ('/initialState/section',s2['initialState']['section'],s2['initialState']['section'].replace('z[-1,0]','x[0,5],y[0,5],z[-1,0]')),
  ('/initialState/splitInput',s2['initialState']['splitInput'],'Later independently legal real VERTICAL cut at x=3.75 partitions the entire remaining slab height, so both horizontal areas and volumes are75%/25% with unchanged0.75ft thickness. Its actual tool/cost permission remains a conditional supplied input; no cut is granted by Freezing Sphere.')])
 s4=next(x for x in d['currentConferenceWorkedSupplements08'] if x['id']=='DC25-P04')
 textfix('DC25-P04',[
  ('/initialState/T',s4['initialState']['T'],s4['initialState']['T'].replace('actual class Counterspell selected/available','actual automatic class Counterspell acquired at Wizard2 and currently available').replace('HP60/max60','CON14, HP56/max56 from first6+2 and8 later4+2')),
  ('/initialState/C',s4['initialState']['C'],s4['initialState']['C'].replace('Wizard7 INT18/PB3','Wizard7 INT18/PB3 Abjuration specialization')),
  ('/orderedAdjudication/0',s4['orderedAdjudication'][0],s4['orderedAdjudication'][0].replace('HP60->45','HP56->41')),
  ('/orderedAdjudication/3',s4['orderedAdjudication'][3],s4['orderedAdjudication'][3].replace('45->29','41->25')),
  ('/expectedState/T_HP',29,25)])
 foundation=R/'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md';wizard=read(R/'data/public/class_playtests/wizard.json')
 ck('Wizard printed HD/fixed table','| [Wizard](classes/wizard.md) | d6 / 4 |' in foundation.read_text(encoding='utf8'))
 ck('Actual Counterspell automatic acquisition',any(c['name']=='Counterspell' and c['minimumClassLevel']==2 and c['acquisition']=='automatic' for c in wizard['cards']))
 ck('Wizard11/9 lawful fixed HP',6+2+10*(4+2)==68 and 68-15==53 and 6+2+8*(4+2)==56 and 56-15-16==25)
 ck('Vertical cut actual areas and mass',Fraction(15,4)*5/Fraction(25)==Fraction(3,4) and Fraction(750)*Fraction(3,4)==Fraction(1125,2))
 def allocation(amounts,reduction):
  a={k:v for k,v in amounts.items() if v>0};total=sum(a.values());b=min(reduction,total)
  if not total:return {k:0 for k in amounts}
  exact={k:Fraction(b*v,total) for k,v in a.items()};shares={k:x.numerator//x.denominator for k,x in exact.items()};left=b-sum(shares.values())
  for k in sorted(exact,key=lambda k:(-(exact[k]-shares[k]),k))[:left]:shares[k]+=1
  return {k:v-shares.get(k,0) for k,v in amounts.items()}
 ordinary=allocation({'fire':14,'bludgeoning':5},3);spinal=allocation({'fire':7,'bludgeoning':5},2);tie=allocation({'fire':5,'bludgeoning':5},1)
 ck('Independent Meteor fractions',ordinary=={'fire':12,'bludgeoning':4} and ordinary['fire']//2+ordinary['bludgeoning']==10 and spinal=={'fire':6,'bludgeoning':4} and tie=={'fire':5,'bludgeoning':4})
 ck('Independent ice split allocation',allocation({'first':15,'second':0},0)=={'first':15,'second':0} and Fraction(15)*Fraction(3,4)==Fraction(45,4) and 11+4==15 and Fraction(1125,2)+Fraction(375,2)+250==1000)
 d['codexConferenceSupplementCorrections08']={'status':'PENDING actual Director concurrence; three complete before/after examples, no original36case replaced.','source':info(foundation),'corrections':fixes,'reason':'Use actual fixed WizardHP/automaticCounterspell ownership and specify a vertical ice cut before claiming matching plan-area and volume support fractions.'}
 d['codexConferenceDisposition08']={'actualFinalAssistantId':actual['id'],'actualFinalReviewArchive':info(zipfile),'fullReview':info(reviewdir/'REVIEW.json'),'exactPatchEvidence':info(reviewdir/'PROPOSED_CORRECTIONS.json'),'decision':'Agree with23 proposed source/scoped-authorship corrections as a new pending rebound, subject to the three explicitly identified supplemental example corrections and later exact-file review. No live adoption.','preservedOriginalCandidate':info(oldp),'closedModules':'AC6 and DE4 remain unchanged; no new Fate whitelist item, global ice physics or cross-spell mixed-defense grant.','countsRemain':{'reviewed':480,'pending':368},'remainingWork':['Actual GPT concurrence on three supplemental example corrections.','Full exact operational model/casebook/player/director mirrors and all affected active dependency bindings.','Dedicated exact-file acceptance before live ordinary spell/index membership changes.']}
 d['previousCompleteDraft']=info(oldp)
 for p in [oldp,zipfile,native,foundation,*[reviewdir/f['name'] for f in manifest['outputFiles']],reviewdir/'EVIDENCE_MANIFEST.json']:
  if not any(x['path']==p.relative_to(G).as_posix() for x in d['sourceBindings']):d['sourceBindings'].append(info(p))
 for b in d['sourceBindings']:ck('Full exact source '+b['path'],info(G/b['path'])==b)
 d.update(id='DAMAGE-CONTROL-25-CURRENT-08',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='PENDING exact rebound review:23 actual GPT conference corrections applied to new authored candidate only; six complete new supplements retained, three current supplemental examples locally corrected pending concurrence.25sourceidentities/26placements/36originaltexts preserved. No live adoption, runtime or balance approval.')
 ck('No unintended adoption flags',d['newSpellAdoptions']==0 and d['runtimeTestsExecuted']==0 and d['sourceInformationDeleted']==0)
 out.write_bytes(encoded(d));receipt.write_bytes(encoded({'id':'DAMAGE-CONTROL25-CONFERENCE07-ACTUAL-RECEIPT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualAssistantId':actual['id'],'actualUserTurnId':'5ba509eb-89b8-43e6-b1eb-e4bdf7dc6bf3','nativeFinal':info(native),'actualReviewArchive':info(zipfile),'reviewedCandidate':info(oldp),'verdict':review['verdict'],'outputManifest':info(reviewdir/'EVIDENCE_MANIFEST.json'),'localPendingRebound':info(out),'liveFilesApplied':0,'countChange':0,'scope':'Actual final review only. Analysis/preliminary archives are not substituted for this230039-byte six-file final package.'}));checkp.write_bytes(encoded({'candidate':info(out),'receipt':info(receipt),'checks':checks,'checkCount':len(checks),'failureCount':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps({'candidate':info(out),'receipt':info(receipt),'checks':len(checks),'GPTCorrections':23,'newSupplements':6,'supplementsWithPendingCodexCorrections':3}))
if __name__=='__main__':main()
