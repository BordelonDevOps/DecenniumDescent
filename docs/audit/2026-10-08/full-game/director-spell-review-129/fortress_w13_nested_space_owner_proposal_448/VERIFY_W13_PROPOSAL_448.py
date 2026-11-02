from __future__ import annotations
import hashlib,json,math,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[5]; BASE='cf0ea55dcbb781af4bae548513999c88daf022de'
def sha(b):return hashlib.sha256(b).hexdigest()
def j(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def git(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=REPO)
def seg(a,b,q):
 t0,t1=0.,1.
 for ax,(lo,hi) in enumerate(((q[0],q[1]),(q[2],q[3]),(q[4],q[5]))):
  d=b[ax]-a[ax]
  if abs(d)<1e-12:
   if not lo<a[ax]<hi:return False
  else:
   u,v=(lo-a[ax])/d,(hi-a[ax])/d; en,le=sorted((u,v));t0,t1=max(t0,en),min(t1,le)
   if t0>=t1:return False
 return t1>max(t0,0.) and t0<1.
def main():
 p=j('PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json'); x=p['ownerProposedInputs']; sched=x['scheduledTimeAdvance']; L=x['resourceLedger']; close=x['rootTerminalClosure']; cargo=next(z for z in close['looseItems'] if z['id']=='cargo-B'); val=j('BUILD_VALIDATION_448.json'); man=j('MANIFEST_448.json'); delivery=j('DELIVERY_448.json')
 prev=ROOT.parent/'fortress_w13_nested_space_owner_proposal_447'/'PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.json'
 checks={}
 checks['superseded proposal and director correction IDs']=sha(prev.read_bytes())=='5dc27a73ffde95b92fe278e62d8233aef85b264cf9d4ae801b0af0fa96a3c786' and [z['id'] for z in p['reviewCorrectionsApplied']]==['W447-C01','W447-C02','W447-C03','W447-C04']
 checks['17 source blobs and Model166/Secure Cargo locators']=len(p['sourceBindings'])==17 and all(sha(git(z['path']))==z['sha256'] and len(git(z['path']))==z['bytes'] for z in p['sourceBindings']) and '/spells/0/procedure/rules/geometry' in next(z for z in p['sourceBindings'] if z['path'].endswith('DEMIPLANE_MODEL_166.json'))['jsonPointers'] and 'Secure Cargo Action definition' in next(z for z in p['sourceBindings'] if z['path'].endswith('COMBAT_ACTION_PLAYTEST.md'))['textAnchors'][0]
 checks['Class0 remains an explicit unadopted test premise and Action is paid']=L['B']['cargoExtractionClassPremise']['class']==0 and 'NOT OWNER-ADOPTED' in L['B']['cargoExtractionClassPremise']['classification'] and L['B']['cargoSecureAction']['at']==19.01 and L['B']['cargoSecureAction']['cost']=='one Action' and L['B']['cargoSecureAction']['freeInteractionClaim'] is False
 checks['eligible Counterspell decline precedes cargo pickup']=x['AArcaneSight']['counterspellDispositionAt18_2']['result']=='ELIGIBLE_DECLINES' and x['AArcaneSight']['counterspellDispositionAt18_2']['reactionSpent'] is False and sched['lifecycleEvents'][6]['at']==18.2 and sched['lifecycleEvents'][8]['at']==19.01
 starts=sum(len(z['starts']) for z in sched['markersByActor'].values()); ends=sum(len(z['ends']) for z in sched['markersByActor'].values())
 checks['12 START/11 END through terminal with retimed spells']=starts==12 and ends==11 and sched['counts']=={'starts':12,'ends':11} and sched['through']==30.31 and (x['childDispel']['commitAt'],x['childDispel']['counterspellWindowAt'],x['childDispel']['resolutionAt'],x['childTerminalSettlement']['at'])==(25.1,25.2,25.3,25.31) and (x['parentDispel']['commitAt'],x['parentDispel']['counterspellWindowAt'],x['parentDispel']['resolutionAt'])==(30.1,30.2,30.3)
 pdisp=x['parentDispel']['counterspellDispositionAt30_2']
 checks['responder distance is 7ft and eligible decline']=math.dist(x['parentDispel']['casterCenter'],[pdisp['BPosition'][0]+2.5,pdisp['BPosition'][1]+2.5,3])==7 and pdisp['distanceFeet']==7 and pdisp['declaredDecision']=='ELIGIBLE; B DECLINES'
 checks['resource and deadline ledger preserved']=L['A']['terminalRP']==48 and L['B']['terminalRP']==56 and L['B']['childDoorExpiresAt']==73.1 and L['A']['concentrationAtTerminal']['deadline']==618.1 and L['A']['arcaneSightRechargeRoundsRemainingAtTerminal']==0 and L['B']['spellEfficiencyDeadlineForChildDispel']==31.9 and L['A']['spellEfficiencyDeadlineForParentDispel']==36.9
 checks['cargo projection, exterior bounds, and distinct supports']=cargo['insidePosition']==[40,15,0] and cargo['outsidePosition']==[40,5,0] and cargo['projectionOffset']==[0,-10,0] and cargo['bounds']=={'x':[40,41],'y':[5,6],'z':[0,1]} and cargo['supportPatchId']=='W13-448-CARGO-B-ORIGIN-GROUND' and any(z.get('plane')=='fixture:origin' and z['bounds']['y']==[5,6] for z in close['supportPatches']) and close['parentSupportPatches'][0]['bounds']['y']==[15,16]
 ray=x['geometryAudit']['rays']['BChildDispel']; model=git(ray['geometrySourcePath']); a=ray['from']; b=ray['to']; room=ray['roomInteriorBoundsFeet']; inroom=all(room[i]<=pt[axis]<=room[i+1] for pt in (a,b) for axis,i in ((0,0),(1,2),(2,4)))
 checks['child ray uses Model166 room/opaque boundary and actual contents']=sha(model)==ray['geometrySourceSha256'] and inroom and ray['roomInteriorBoundsFeet']==[0,30,0,30,0,15] and len(ray['actualChildContentsAt25_1'])==4 and ray['opaqueBoundary']['segmentWithinInterior'] and ray['geometrySourcePath'].endswith('DEMIPLANE_MODEL_166.json') and not seg(a,b,[5,6,15,16,0,1]) and not ray['opaqueBoundary']['boundaryIntersections']
 checks['Q27 exterior has 15 nonoverlapping pairs']=len(x['geometryAudit']['rootQ27ExteriorCollisionPairs'])==15 and all(not z['positiveVolumeOverlap'] for z in x['geometryAudit']['rootQ27ExteriorCollisionPairs'])
 checks['unadopted/unwitnessed authority boundary']=p['classification'].endswith('NOT_A_WITNESS') and p['boundaries']['ownerAdoptionRequired'] and not p['boundaries']['witnessConstructed'] and not p['boundaries']['queueChanged'] and p['queueAtProposal']['applied']==830 and p['queueAtProposal']['pending']==18 and p['queueAtProposal']['acceptedUnapplied']==0
 checks['build validation binds exact current artifacts']=val['status']=='PASS' and val['passed']==sum(z['pass'] for z in val['checks']) and val['proposalFileSha256']==sha((ROOT/'PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json').read_bytes()) and val['sourceCount']==17
 checks['manifest and delivery hashes']=delivery['ownerAdopted'] is False and delivery['witnessConstructed'] is False and delivery['proposalSha256']==sha((ROOT/'PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json').read_bytes()) and any(z['path']=='PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json' and z['sha256']==delivery['proposalSha256'] for z in man['artifacts'])
 arc=ROOT/'DD_Fortress_W13_Proposal_448_TESTONLY.zip'
 with zipfile.ZipFile(arc) as z: checks['archive CRC and payload bytes']=z.testzip() is None and all(z.read('payload/'+q.name)==q.read_bytes() for q in [ROOT/'PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json',ROOT/'PG328_W13_DIRECTOR_CORRECTIONS_448.json',ROOT/'BUILD_VALIDATION_448.json',ROOT/'MANIFEST_448.json'])
 for k,v in checks.items():print(('PASS: ' if v else 'FAIL: ')+k)
 if not all(checks.values()):raise SystemExit(1)
 print(f'PASS: {sum(checks.values())}/{len(checks)} independent checks; proposal448 remains unadopted and unwitnessed.')
if __name__=='__main__':main()
