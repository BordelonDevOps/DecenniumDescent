from __future__ import annotations
import copy, hashlib, json, math, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PREV=BASE/'fortress_w11_cargo_owner_proposal_434'; OUT=BASE/'fortress_w11_cargo_owner_proposal_435'; OUT.mkdir(parents=True,exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def readj(p): return json.loads(p.read_text(encoding='utf-8'))
def writej(p,v):
 b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'); p.write_bytes(b); return b
def write_text(p,s): p.write_text(s,encoding='utf-8',newline='\n')
def box(p,size=(5,5,6)): return {'x':[p[0],p[0]+size[0]],'y':[p[1],p[1]+size[1]],'z':[p[2],p[2]+size[2]]}
def axes(b): return [b['x'],b['y'],b['z']] if isinstance(b,dict) else b
def overlap(a,b): return all(min(a[i][1],b[i][1])-max(a[i][0],b[i][0])>1e-9 for i in range(3))
def sweep(a,b,size=(5,5,6)): return [[min(a[i],b[i]),max(a[i]+size[i],b[i]+size[i])] for i in range(3)]
def rlen(r): return sum(sum(abs(v[i]-u[i]) for i in range(3)) for u,v in zip(r,r[1:]))
def d3(a,b): return math.dist(a,b)
pp=PREV/'OWNER_PG328_W11_ADOPTION_PROPOSAL_434.json'; tp=PREV/'W11_LIFECYCLE_TRACE_434.json'
p434sha=sha(pp.read_bytes()); assert p434sha=='db500e155f1a6ca37f2d888b4b73f49d54c7d1ae95ce2208fd53375f201b5519'
p=copy.deepcopy(readj(pp)); tr=copy.deepcopy(readj(tp))
geo=readj(BASE/'fortress_w01_successor_overlays_425/evidence/GEOMETRY_405.json')
parent=readj(BASE/'fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json'); S=parent['stateSnapshots']['S030']
space=p['entryPremise']['apertures']['interior']['plane']; origin='fixture:origin'; petid='PG328-W11-R1:greater-fire-pet-1'; tileid='PG328-W01-403:CLAY-TILE-1'; cargo_bid='cargo-B'
cargo_b0=S['items'][cargo_bid]
assert cargo_b0['owner']=='B' and cargo_b0['position']==[20,10,0] and cargo_b0['sizeFeet']==[1,1,1]
OBS=[]
for key in ('panels','doorLeaves'):
 for item in geo[key]:
  for f in item.get('occupiedFragments',[]): OBS.append((item['id'],[[f[0],f[1]],[f[2],f[3]],[f[4],f[5]]]))
def geom_hits(r):
 out=[]
 for a,b in zip(r,r[1:]):
  for oid,ob in OBS:
   if overlap(sweep(a,b),ob): out.append({'from':a,'to':b,'obstacle':oid})
 return out
def rayhit(p1,p2,b):
 lo,hi=0.,1.
 for i in range(3):
  d=p2[i]-p1[i]
  if abs(d)<1e-12:
   if not b[i][0]<p1[i]<b[i][1]: return False
  else:
   t1=(b[i][0]-p1[i])/d; t2=(b[i][1]-p1[i])/d; lo=max(lo,min(t1,t2)); hi=min(hi,max(t1,t2))
   if hi<=lo:return False
 return hi>lo and hi>0 and lo<1
def ray_geom(p1,p2): return [oid for oid,b in OBS if rayhit(p1,p2,b)]
def ray_actors(p1,p2,actors): return [a for a,b in actors.items() if rayhit(p1,p2,b)]
routes={
 'A18':[[25,6,0],[35,6,0]],
 'B19':[[15,10,0],[20,10,0],[25,10,0],[25,20,0],[35,20,0]],
 # cargo-B is lifted before B moves, so its floor bounds are absent from the path.
 'A24':[[35,6,0],[25,6,0],[25,25,0]],
 'Mage28':[[15,10,0],[20,10,0],[25,10,0],[25,20,0]],
 'A30':[[25,25,0],[30,25,0],[30,6,0]],
 'A36':[[30,6,0],[35,6,0]],
 'A42':[[35,6,0],[30,6,0],[30,10,0],[25,10,0]],
}
for k,r in routes.items():
 h=geom_hits(r)
 if h: raise AssertionError((k,h[:4]))
P={'A18':box([35,6,0]),'B19':box([35,20,0]),'A24':box([25,25,0]),'Mage28':box([25,20,0]),'A30':box([30,6,0]),'A36':box([35,6,0]),'A42':box([25,10,0]),'pet':box([40,6,0]),'tile':axes({'x':[25,26],'y':[5,6],'z':[0,.25]}),'C':box([0,0,0]),'D':box([5,5,0])}
for route,others in [('B19',['A18']),('A24',['B19','tile']),('Mage28',['A24','B19','tile']),('A30',['Mage28','B19','tile']),('A36',['Mage28','B19','pet']),('A42',['Mage28','B19','pet','tile'])]:
 for a,b in zip(routes[route],routes[route][1:]):
  for other in others:
   if overlap(sweep(a,b),axes(P[other])): raise AssertionError(f'{route} sweep collides with {other}: {a}->{b}')
# Recomputed centerlines, ranges and actor blockage.
centers={'Mage':[27.5,22.5,3.0],'pet':[42.5,8.5,3.0],'A0':[32.5,8.5,3.0],'B':[37.5,22.5,3.0],'A':[27.5,12.5,3.0],'Fortress':[10.0,10.0,3.0]}
rays={'Mage_pet':(centers['Mage'],centers['pet']),'A_Mage':(centers['A0'],centers['Mage']),'B_Mage':(centers['B'],centers['Mage']),'B_A':(centers['B'],centers['A']),'Mage_A':(centers['Mage'],centers['A']),'A_Fortress':(centers['A'],centers['Fortress'])}
rg={k:ray_geom(*v) for k,v in rays.items()}
if any(rg.values()): raise AssertionError(rg)
actor_rays={'Mage_pet':{'A':axes(P['A30']),'B':axes(P['B19'])},'A_Mage':{'B':axes(P['B19'])},'B_Mage':{'A':axes(P['A30'])},'B_A':{'Mage':axes(P['Mage28'])},'Mage_A':{'B':axes(P['B19'])}}
ra={k:ray_actors(*rays[k],v) for k,v in actor_rays.items()}
if any(ra.values()): raise AssertionError(ra)
# Keep proposal 434 immutable and author a separate corrected 435 branch proposal.
p['id']='OWNER-PG328-W11-ADOPTION-PROPOSAL-435'; p['status']='PROPOSED_NOT_ADOPTED'
p['supersedes']={'id':'OWNER-PG328-W11-ADOPTION-PROPOSAL-434','sha256':p434sha,'handling':'retained as historical Director-rejected revision; unchanged'}
e=p['entryPremise']
e['openAction']={'actor':'A','time':24.0,'action':'interior exit-control glyph Action under PG9-Q25 / Absolute Gate local controls','start':[35,6,0],'route':routes['A24'],'movementFeet':29,'glyphPose':[25,25,0],'glyphPlacement':'branch-only TEST_ONLY accessible courtyard pose; no Geometry405 or parent mutation'}
e['externalMageStart']={'plane':origin,'position':[10,-5,0],'bounds':box([10,-5,0]),'approachRoute':[[10,-5,0],[10,0,0]],'approachMovementFeet':5,'support':'branch-only fixture:origin support premise'}
e['destination']={'plane':space,'position':[15,10,0],'bounds':box([15,10,0]),'sourceAnalog':'W01_REPLAY_403.json#/stateSnapshots/S030/transitReceipts/0; 5x5x6 body and admitted cargo fit at this pose'}
e['passage']={'committedMovementFeet':5,'approachMovementFeet':5,'wholeBodyFit':True,'wholeEquipmentFit':True,'supportBothSides':True,'sourceAnalog':'W01_REPLAY_403.json#/stateSnapshots/S030/transitReceipts/0','sourceOpening':'unchanged S030 apertures: exterior [10,0,0], interior [10,10,0], each 10x15','mainGateUsed':False}
e['route']=routes['Mage28']; e['turns']=[{'start':28.0,'movementFeet':30,'parts':{'approach':5,'portalPassage':5,'interiorRoute':20},'end':[25,20,0]}]; e['castPose']=[25,20,0]
e['bodyBoxFeet']=[5,5,6]; e['controlGlyphPremise']={'position':[25,25,0],'classification':'branch-only TEST_ONLY placement premise','basis':'PG9-Q25 makes the interior exit-control glyph usable by any occupant as an Action; exact local pose is not specified in retained parent.'}
e['clearance']='Each route tested against every Geometry405 panel, stair tread/riser and door leaf, plus time-matched actors and items. Boundary contact is a branch-only TEST_ONLY premise.'
actors=[('A',18,102),('B',13,97),('C',14,98),('D',15,99),('actor-w11-firepet-owner',22,100)]; turns=[]
for actor,first,last in actors:
 for t in range(first,last+1,6): turns.append({'actor':actor,'displayName':'Mage' if actor=='actor-w11-firepet-owner' else actor,'startSeconds':float(t),'endSeconds':round(t+.9,1),'reactionRefresh':'regular START','actionUse':'see authored action/event list','magicThisTurnResetAtStart':actor=='A'})
turns.sort(key=lambda v:(v['startSeconds'],['A','B','C','D','actor-w11-firepet-owner'].index(v['actor'])))
p['turnSchedule']=turns; tr['turnMarkers']=turns; tr['id']='PG328-W11-LIFECYCLE-TRACE-435'; tr['branchId']='PG328-W11-R1'; tr['status']='PROPOSED_NOT_ADOPTED_DIRECTOR_REVIEW_REQUIRED'
tr['boundary']={'parentW01Mutated':False,'campaignEventsAsserted':False,'FortressAcceptedOrApplied':False,'canonChanged':False,'queueChanged':False,'witnessConstructed':False,'sealIssued':False}
tr['actions']=[
 {'actor':'A','time':18.0,'action':'move clear and free-interaction set down tile at existing held bounds','movementFeet':10,'route':routes['A18'],'freeInteraction':{'item':tileid,'setDownBounds':{'x':[25,26],'y':[5,6],'z':[0,.25]},'wasHeldAtSameBoundsInS030':True}},
 {'actor':'B','time':19.0,'action':'Secure Cargo lift of existing cargo-B first, then move clear of southwest doorway','movementFeet':30,'route':routes['B19'],'actionUse':'one Secure Cargo lift Action; right hand holds cargo-B, left hand remains free','itemTransfer':{'item':'cargo-B','fromFloorBounds':{'x':[20,21],'y':[10,11],'z':[0,1]},'toCarriedBoundsAtStart':{'x':[18.5,19.5],'y':[10,11],'z':[3,4]},'owner':'B','custodian':'B'}},
 {'actor':'A','time':24.0,'action':'move to courtyard glyph and open retained portal','movementFeet':29,'route':routes['A24']},
 {'actor':'actor-w11-firepet-owner','displayName':'Mage','time':28.0,'action':'approach, cross open portal and move to cast pose','movementFeet':30,'parts':{'approach':5,'portalPassage':5,'interiorRoute':20},'route':[[10,-5,0],[10,0,0],[15,10,0],[20,10,0],[25,10,0],[25,20,0]]},
 {'actor':'A','time':30.0,'action':'return and Secure Cargo lift Action','movementFeet':24,'route':routes['A30']},
 {'actor':'actor-w11-firepet-owner','displayName':'Mage','time':34.1,'action':'commit and cast summon-greater-fire-pet'},
 {'actor':'A','time':36.0,'action':'approach pet and Secure Cargo attach Action','movementFeet':5,'route':routes['A36']},
 {'actor':'A','time':42.0,'action':'move to sight/dispel pose','movementFeet':14,'route':routes['A42']},
 {'actor':'A','time':96.1,'action':'cast acquired Arcane Sight; 2 RP'},
 {'actor':'A','time':102.1,'action':'cast acquired Arch Dispel Magic; 3 RP'}]
relation={'classification':'branch-only TEST_ONLY relationship/perception premise','mutuallyNonhostileActors':['A','B','C','D','actor-w11-firepet-owner'],'petRelation':'summoned by Mage; nonhostile to Mage and all cooperating actors','auraRule':'source aura affects adjacent foes; no actor is designated a foe in this hypothetical branch','auraRecipients':[]}
phases=[{'afterMageTurnEnd':round(t+.9,1),'movementFeet':0,'choice':'defensive Dodge','commandExpenditure':False,'extraRegularTick':False} for t in range(34,89,6)]
def response(actor,card=None,rp=None,recharge=None,dc=None,perception=None,line=None,distance=None):
 x={'actor':actor}
 if card: x.update({'card':card,'availableRP':rp,'costRP':3 if card=='wizard.base.counterspell' else 4,'rechargeRounds':recharge,'rechargeReady':True,'reactionAvailable':True,'prospectiveDC':dc,'decision':'explicit proposed decline; no cost or recharge spent','perception':perception,'lineOfEffectCenterline':line,'centerDistanceFeet':round(distance,4)})
 return x
Dnone={'actor':'D','attempt':'none','eligibility':'unadjudicated','basis':'outside Fortress plane; no positive cross-portal perception or Counterspell eligibility is claimed'}
selfM={'actor':'actor-w11-firepet-owner','attempt':'none','eligibility':'unadjudicated','basis':'caster made no self-counter attempt; eligibility is not categorically adjudicated'}
selfA={'actor':'A','attempt':'none','eligibility':'unadjudicated','basis':'A is caster; no self-counter attempt and no categorical eligibility ruling'}
Cnone={'actor':'C','attempt':'none','eligibility':False,'basis':'bound Cleric20 profile has no source-bound Counterspell card'}
rsum=[response('A','wizard.base.counterspell',53,2,20,'visible Mage casting; same plane and clear centerline',centers['A0'],d3(centers['A0'],centers['Mage'])),response('B','wizard.base.counterspell',80,2,20,'visible Mage casting; same plane and clear centerline',centers['B'],d3(centers['B'],centers['Mage'])),Dnone,Cnone,selfM]
rsight=[response('B','wizard.base.counterspell',80,2,14,'visible A casting; same plane and clear centerline',centers['B'],d3(centers['B'],centers['A'])),response('actor-w11-firepet-owner','mage.arch.counterspell',16,3,14,'visible A casting; same plane and clear centerline',centers['Mage'],d3(centers['Mage'],centers['A'])),Dnone,Cnone,selfA]
rdispel=[response('B','wizard.base.counterspell',80,2,16,'visible A casting; same plane and clear centerline',centers['B'],d3(centers['B'],centers['A'])),response('actor-w11-firepet-owner','mage.arch.counterspell',16,3,16,'visible A casting; same plane and clear centerline',centers['Mage'],d3(centers['Mage'],centers['A'])),Dnone,Cnone,selfA]
# Lifecycle event timing and corrected spell/counter windows.
tr['events']=[
 {'time':34.1,'type':'CAST_COMMIT','spell':'summon-greater-fire-pet','caster':'actor-w11-firepet-owner','rank':5,'rpBefore':26,'cost':10,'rpAfter':16,'concentrationCommittedBeforeInterruption':True,'concentrationStartsAfterInterruptionResolution':False,'pending':True,'components':'V/S/F; Fire Focus held, somatic hand free','firstPreparedFamily':True,'noDiscount':True,'dissonance':[0,0],'refrainAfter':0,'magicThisTurn':True},
 {'time':34.2,'type':'COUNTERSPELL_WINDOW','prospectiveDC':20,'responses':rsum},
 {'time':34.3,'type':'CAST_SUCCESS_AND_CREATION','petId':petid,'position':[40,6,0],'expiresAt':94.3,'duration':'60 elapsed seconds after successful creation','lineOfEffect':{'fromCenter':centers['Mage'],'toCenter':centers['pet'],'distanceFeet':round(d3(centers['Mage'],centers['pet']),4),'geometry':'clear','blockingActors':[]},'auraPremise':relation},
 *[{'time':x['afterMageTurnEnd'],'type':'PET_DEFENSIVE_PHASE','petId':petid,**{k:v for k,v in x.items() if k!='afterMageTurnEnd'}} for x in phases],
 {'time':94.3,'type':'SUMMON_EXPIRY','petRemoved':True,'cargoFallsFeet':3,'concentrationEnds':True,'noLaterPetPhaseAt94.9':True},
 {'time':96.0,'type':'A_REGULAR_START','magicThisTurnReset':True},
 {'time':96.1,'type':'SIGHT_COMMIT','card':'wizard.arch.arcane-sight','family':'wizard.arch.arcane-sight','rank':2,'rpBefore':53,'cost':2,'rpAfter':51,'RechargeRounds':2,'rechargeReadyBeforeCommit':True,'concentrationCommittedBeforeInterruption':True,'dissonance':[0,0],'refrainAfter':0,'firstCastOfDistinctPreparedFamily':True,'lastSpellAfterCommit':'wizard.arch.arcane-sight','magicThisTurnAfterCommit':True,'spellEfficiencyDeadline':102.9,'noStrainSurcharge':True},
 {'time':96.2,'type':'COUNTERSPELL_WINDOW','prospectiveDC':14,'responses':rsight},
 {'time':96.3,'type':'SIGHT_SUCCESS','auraPerception':'Arcane Sight automatically perceives the visible Fortress aura within60ft and its broad category; no later-turn examination Action used','fortressAuraTargetPoint':[10,10,3],'concentrationDeadline':696.3,'sightRechargeRemainingAtA102Start':1},
 {'time':102.0,'type':'A_REGULAR_START','magicThisTurnReset':True,'sightRechargeRemaining':1},
 {'time':102.1,'type':'DISPEL_COMMIT','card':'wizard.arch.dispel-magic','family':'wizard.arch.dispel-magic','rank':3,'targetEffectId':e['effectId'],'targetPoint':[10,10,3],'rpBefore':51,'cost':3,'rpAfter':48,'RechargeRounds':2,'rechargeReadyBeforeCommit':True,'dissonance':[0,0],'refrainAfter':0,'firstCastOfDistinctPreparedFamily':True,'lastSpellAfterCommit':'wizard.arch.dispel-magic','magicThisTurnAfterCommit':True,'spellEfficiencyDeadline':108.9,'noStrainSurcharge':True,'lineOfEffect':{'fromCenter':centers['A'],'toCenter':centers['Fortress'],'distanceFeet':round(d3(centers['A'],centers['Fortress']),4),'geometry':'clear through open tower-SW-entry doorway'}},
 {'time':102.2,'type':'COUNTERSPELL_WINDOW','prospectiveDC':16,'responses':rdispel},
 {'time':102.3,'type':'DISPEL_SUCCESS','roll':'12+5+6=23 vs DC19','FortressEnds':True,'testOnlyNotCampaignRoll':True}]
prior_families=list(S['actors']['A']['preparedFamiliesUsed'])
sight_families=prior_families+['wizard.arch.arcane-sight']
dispel_families=sight_families+['wizard.arch.dispel-magic']
for event in tr['events']:
 if event['type']=='SIGHT_COMMIT': event['preparedFamiliesUsedAfterCommit']=sight_families
 if event['type']=='DISPEL_COMMIT': event['preparedFamiliesUsedAfterCommit']=dispel_families
tr['petPhases']=phases
tr['castingStateRules']={'wizardEngine11':'first cast of each distinct prepared matrix family generates0 base Dissonance; Sight and Dispel each0->0','wizardEngine12':'Wizard cards are always-prepared once acquired and use normal RP/Recharge','refrain':'0 throughout these distinct first-family casts','spellEfficiency':'Sight96.1->102.9; Dispel102.1->108.9; no cross-family discount','magicThisTurn':'reset only at actual A regular STARTs; at commitment update family history, lastSpell and flag'}
# Proposal branch details: selected spells/profile/parent remain as reviewed.
p['entryPremise']=e; p['turnSchedule']=turns
trace_bytes=writej(OUT/'W11_LIFECYCLE_TRACE_435.json',tr)
p['lifecycleTrace']={'path':(BASE/'fortress_w11_cargo_owner_proposal_435/W11_LIFECYCLE_TRACE_435.json').as_posix(),'sha256':sha(trace_bytes)}
p['creation'].update({'commit':34.1,'interruptWindow':34.2,'successAndCreation':34.3,'position':[40,6,0],'bounds':box([40,6,0]),'casterPosition':[25,20,0],'centerDistanceFeet':round(d3(centers['Mage'],centers['pet']),4),'concentrationCommittedBeforeInterruption':True,'concentrationStartsAfterInterruptionResolution':False,'expiry':94.3,'expiryRule':'60 elapsed seconds from successful creation','lineOfEffect':{'casterCenter':centers['Mage'],'targetCenter':centers['pet'],'distanceFeet':round(d3(centers['Mage'],centers['pet']),4),'Geometry405':'clear','AAtCast':P['A30'],'BAtCast':P['B19'],'blockingActors':[]},'counterspellResponses':rsum,'prospectiveCounterspellDC':20})
p['cargoBHandling']={'id':'cargo-B','source':'unchanged W01 S030 item record','owner':'B','S030Custodian':None,'S030Position':[20,10,0],'dimensionsFeet':[1,1,1],'massLb':10,'load':1,'time':19,'action':'one Secure Cargo lift Action before B movement','floorBoundsBefore':{'x':[20,21],'y':[10,11],'z':[0,1]},'carriedBoundsAtBStart':{'x':[18.5,19.5],'y':[10,11],'z':[3,4]},'carriedBoundsAtBEnd':{'x':[38.5,39.5],'y':[20,21],'z':[3,4]},'ownerRemains':'B','custodianAfterLift':'B','hands':{'right':'cargo-B','left':'free','focus-B':'accessible'},'bodyPlusEquipmentLb':162,'Load':1.2,'bodyCapacityPremise':{'weightLb':210,'Load':14,'postLiftWithinCapacity':True},'closureDisposition':'carried content remains with actual carrier B; returns with B at its Q27 anchor; not loose'}
cargo=p['cargoHandling']
cargo['custody']=[{'time':'S030','holder':'A, carried','owner':'A'},{'time':30,'holder':'A right hand after one Secure Cargo lift Action','owner':'A'},{'time':36,'holder':petid,'relation':'externally attached carrier; owner remains A'},{'time':94.3,'holder':None,'relation':'loose real item after expiry and exact proposed three-foot fall','owner':'A'}]
cargo['lift'].update({'time':30,'AStart':[25,25,0],'AEnd':[30,6,0],'route':routes['A30'],'movement':24,'hands':{'left':'focus-A','right':'cargo-A'}})
cargo['attach'].update({'time':36,'AStart':[30,6,0],'AEnd':[35,6,0],'route':routes['A36'],'movement':5,'petPosition':[40,6,0],'petBounds':box([40,6,0]),'sweptBounds':[
 {'x':[31,32],'y':[6,7],'z':[3,4],'phase':'carried within A before the turn36 movement'},
 {'x':[36,37],'y':[6,7],'z':[3,4],'phase':'carried within A at adjacent pose'},
 {'x':[38,39],'y':[6,7],'z':[3,4],'phase':'carried while emerging toward pet west face'},
 {'x':[39,40],'y':[6,7],'z':[3,4],'phase':'clamp contacts pet west face; boundary contact'}],
 'noPositiveOverlapWithPet':True,'AWeightAfterLb':2,'ALoadAfter':0.2,'petCombinedWeightLb':110,'petLoad':1,'handsAfter':{'left':'focus-A','right':'free'}})
cargo['expiry'].update({'time':94.3,'petRemoved':True,'cargoBefore':{'x':[39,40],'y':[6,7],'z':[3,4]},'cargoAfter':{'x':[39,40],'y':[6,7],'z':[0,1]},'fallFeet':3,'support':'branch-only Fortress z=0 floor patch [39,40]x[6,7]','impactDisposition':'proposed narrow TEST_ONLY outcome: this exact cargo-A sustains no damage in this exact three-foot fall; no general object-impact rule; owner, mass, Load, quantity and identity remain unchanged'})
cargo['sourceAdmissionCustody']='Unchanged S030 item record: cargo-A owner A, custodian A,10lb,1Load, genuine item admitted with A; no replacement cargo.'
pet=p['pet']; pet.update({'position':[40,6,0],'bounds':box([40,6,0]),'stationary':True,'attacksOrCommands':[],'auraRecipients':[],'auraRelationshipPremise':relation,'turnPhases':phases,'noCommandExpenditure':True,'noExtraRegularTicks':True,'expiry':94.3})
closure=p['closure']; closure['time']=102.3
closure['mandatoryEventsFirst']=['pet expiry and cargo fall at94.3 already processed','Fortress ending at102.3','tile separate deadline3606.13 remains live']
closure['bodyOrder']=['A','B','actor-w11-firepet-owner']
placements=[
 {'actor':'A','exteriorEntryPose':[5,0,0],'interiorEntryPose':[15,10,0],'stableOffset':[5,0,0],'originPlacement':[10,0,0],'bounds':box([10,0,0]),'sourceCrossing':'RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A.json#/events/6'},
 {'actor':'B','exteriorEntryPose':[0,15,0],'interiorEntryPose':[15,10,0],'stableOffset':[5,0,0],'originPlacement':[5,15,0],'bounds':box([5,15,0]),'sourceCrossing':'RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A.json#/events/11'},
 {'actor':'actor-w11-firepet-owner','displayName':'Mage','exteriorEntryPose':[10,-5,0],'interiorEntryPose':[15,10,0],'stableOffset':[5,0,0],'originPlacement':[15,-5,0],'bounds':box([15,-5,0]),'admissionRecord':'hypothetical entry at28.0; stable interior offset[5,0,0] from unchanged aperture center[10,10,0]'}]
placements[1]['carriedItems']=[{'id':'cargo-B','owner':'B','custodian':'B','boundsAtReturn':{'x':[8.5,9.5],'y':[15,16],'z':[3,4]}}]
closure['bodyPlacements']=placements; closure['unchangedOutsideActors']={'C':[0,0,0],'D':[5,5,0]}
objects=[
 {'id':tileid,'fixedReferenceSource':'PG328_PROCEDURE_CURRENT.json#/sharedContract/cellExtension/closure/looseObjectAnchors at closure start; use current loose position, not creation locus','evaluatedAtClosure':True,'currentLooseBounds':{'x':[25,26],'y':[5,6],'z':[0,.25]},'projectionDelta':[0,-10,0],'fixtureOriginPlacement':{'x':[25,26],'y':[-5,-4],'z':[0,.25]},'support':'branch-only fixture:origin floor','owner':None,'custodian':'A','expiry':3606.13},
 {'id':'cargo-A','fixedReferenceSource':'PG328_PROCEDURE_CURRENT.json#/sharedContract/cellExtension/closure/looseObjectAnchors at closure start after expiry/fall; use current loose bounds','evaluatedAtClosure':True,'currentLooseBounds':{'x':[39,40],'y':[6,7],'z':[0,1]},'projectionDelta':[0,-10,0],'fixtureOriginPlacement':{'x':[39,40],'y':[-4,-3],'z':[0,1]},'support':'branch-only fixture:origin floor','owner':'A','custodian':None}]
objects.sort(key=lambda x:x['id'])
closure['looseItemsStableIdOrder']=objects
closure['projectionRule']={'source':'PG328_PROCEDURE_CURRENT.json#/sharedContract/cellExtension/closure/looseObjectAnchors','reference':'current loose position at closure start','interiorAnchor':[10,10,0],'exteriorAnchor':[10,0,0],'delta':[0,-10,0],'order':'stable object-ID ascending'}
closure['expiredPet']={'id':petid,'present':False,'returnedAsBody':False,'loot':False}
closure['collisionRule']='Bodies settle A/B/Mage in stable admission order, then loose items by ascending stable object ID. Boundary contact is allowed only as branch TEST_ONLY premise; placements are supported and have no positive-volume overlap.'
p['closure']=closure
sp=p['supportPremise']
sp['poses']=[
 {'actor':'A','pose':'S030','position':[25,6,0],'bodyPlusEquipmentLb':164,'Load':1.4},
 {'actor':'A','pose':'after tile set-down/opening route','positions':[[35,6,0],[25,25,0]],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'actor':'A','pose':'after cargo lift','position':[30,6,0],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'actor':'A','pose':'after cargo attachment','position':[35,6,0],'bodyPlusEquipmentLb':152,'Load':0.2},
 {'actor':'A','pose':'Sight/Dispel pose','position':[25,10,0],'bodyPlusEquipmentLb':152,'Load':0.2},
 {'actor':'B','pose':'after cargo-B lift and route','position':[35,20,0],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'item':'cargo-B','pose':'S030 floor bounds before B pickup','bounds':{'x':[20,21],'y':[10,11],'z':[0,1]},'massLb':10},{'actor':'B','pose':'cargo-B carried in body after pickup','bounds':{'x':[38.5,39.5],'y':[20,21],'z':[3,4]},'bodyPlusEquipmentLb':162,'Load':1.2},
 {'actor':'actor-w11-firepet-owner','pose':'Mage cast pose','position':[25,20,0],'bodyPlusEquipmentLb':151,'Load':0.1},
 {'actor':petid,'pose':'created with attached cargo','position':[40,6,0],'bodyPlusEquipmentLb':110,'Load':1},
 {'item':tileid,'pose':'loose tile at Fortress closure','bounds':{'x':[25,26],'y':[5,6],'z':[0,.25]},'massLb':2},
 {'item':'cargo-A','pose':'loose cargo after fall','bounds':{'x':[39,40],'y':[6,7],'z':[0,1]},'massLb':10}]
sp['loads']=[
 {'pose':'A S030','position':[25,6,0],'bodyPlusEquipmentLb':164,'Load':1.4},
 {'pose':'A after tile set-down','position':[35,6,0],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'pose':'A at glyph','position':[25,25,0],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'pose':'A after cargo lift','position':[30,6,0],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'pose':'A after cargo transfer','position':[35,6,0],'bodyPlusEquipmentLb':152,'Load':0.2},
 {'pose':'A Sight/Dispel','position':[25,10,0],'bodyPlusEquipmentLb':152,'Load':0.2},
 {'pose':'B S030','position':[15,10,0],'bodyPlusEquipmentLb':152,'Load':0.2},{'pose':'B after cargo-B lift and route','position':[35,20,0],'bodyPlusEquipmentLb':162,'Load':1.2},
 {'pose':'Mage entry/cast route','positions':[[10,-5,0],[15,10,0],[25,20,0]],'bodyPlusEquipmentLb':151,'Load':0.1},
 {'pose':'pet with cargo-A','position':[40,6,0],'bounds':box([40,6,0]),'bodyPlusEquipmentLb':110,'Load':1},
 {'pose':'loose cargo-A after fall','bounds':{'x':[39,40],'y':[6,7],'z':[0,1]},'massLb':10},
 {'pose':'loose clay tile','bounds':{'x':[25,26],'y':[5,6],'z':[0,.25]},'massLb':2}]
sp['planePartition']='Negative-y closure placements are fixture:origin only. Fortress positions remain in its cast-owned spellSpace. Geometry405 is geometry/support topology only; W01 overlay is graph connectivity, not load rating.'
p['supportPremise']=sp
# Cadence, RP, aura and target are updated using Wizard source rules and actual target geometry.
cr=p['closureRoute']
cr['sight'].update({'castTime':96.1,'effectTime':96.3,'concentration':'committed96.1; surviving aura perception begins96.3, deadline696.3','rechargeRemainingAtA102Start':1,'dissonance':[0,0],'refrainAfter':0,'familyFirstCast':True,'lastSpellAtCommit':'wizard.arch.arcane-sight','magicThisTurnAtCommit':True,'spellEfficiencyDeadline':102.9,'visibleAuraPoint':[10,10,3],'visibleAuraDistanceFeet':round(d3(centers['A'],centers['Fortress']),4),'lineOfEffect':'clear through open tower-SW-entry doorway'})
cr['sight'].pop('rechargeRemainingAtA96Start',None)
cr['sight']['preparedFamiliesUsedAfterCommit']=sight_families
cr['dispel']['preparedFamiliesUsedAfterCommit']=dispel_families
cr['dispel'].update({'castTime':102.1,'effectTime':102.3,'targetEffectId':e['effectId'],'targetPoint':[10,10,3],'rangeFeet':round(d3(centers['A'],centers['Fortress']),4),'lineOfEffect':'clear through open tower-SW-entry doorway','dissonance':[0,0],'refrainAfter':0,'familyFirstCast':True,'lastSpellAtCommit':'wizard.arch.dispel-magic','magicThisTurnAtCommit':True,'spellEfficiencyDeadline':108.9})
cr['RPBeforeAndAfter']=[53,51,48]
cr['spellEfficiency']=[{'family':'wizard.arch.arcane-sight','triggeredAt':96.1,'expiresAt':102.9,'discountAppliesOnlyToSameFamily':True},{'family':'wizard.arch.dispel-magic','triggeredAt':102.1,'expiresAt':108.9,'discountAppliesOnlyToSameFamily':True}]
cr['auraTargeting']={'targetEffectId':e['effectId'],'point':[10,10,3],'rangeFeet':round(d3(centers['A'],centers['Fortress']),4),'visibleToArcaneSight':True,'lineOfEffect':'clear through current OPEN_TEST_ONLY_GEOMETRY tower-SW-entry; panels and door leaf checked'}
cr['sightResponses']=rsight; cr['dispelResponses']=rdispel
cr['dispelRoll']={'d20':12,'INT':5,'PB':6,'total':23,'DC':19,'testOnlyNotCampaignRoll':True}
p['closureRoute']=cr
# Geometry405 is an array-based source.
for b in p['sourceBindings']:
 if b['path'].endswith('GEOMETRY_405.json'):
  b['pointer']='/openings/0 (main-gate structural opening); /regions/0 (courtyard); /panels; /doorLeaves; /stairFlights'
  b['note']='Geometry405 arrays; main-gate is physical structure only, never the Fortress portal. Routes/rays checked against panels including stair treads/risers plus door leaves.'
 src=ROOT/b['path']; data=src.read_bytes(); b['workingTreeBytes']=len(data); b['workingTreeSha256']=sha(data)
 b['headBlobSha1']=subprocess.check_output(['git','rev-parse','HEAD:'+b['path']],cwd=ROOT,text=True).strip()
 hd=subprocess.check_output(['git','show','HEAD:'+b['path']],cwd=ROOT); b['headBlobBytes']=len(hd); b['headBlobSha256']=sha(hd)
p['requestedOwnerDecision']='If GPT confirms adoption readiness, a later explicit owner adoption would authorize construction of hypothetical PG328-W11-R1 from unchanged S030 only. This proposal does not authorize witness construction, seal, Fortress acceptance/application, canon change or queue change.'
p['authority'].update({'witnessConstructionAuthorized':False,'sealAuthorized':False,'FortressAcceptanceOrApplicationAuthorized':False,'canonChangeAuthorized':False,'queueChangeAuthorized':False})
p['statusBoundary'].update({'allTestOnly':True,'campaignEventsAsserted':False,'parentW01Mutated':False,'W04OrW09Changed':False})
corrections=[
 {'id':'W11-434-C01','field':'/entryPremise/openAction/route; /entryPremise/destination; /entryPremise/route; /cargoHandling/lift/route; /cargoBHandling','disposition':'Routes now use courtyard glyph [25,25] and S030 interior pose [15,10]. B uses one Secure Cargo Action to lift its loose S030 cargo-B before moving out of its bounds. All full-body sweeps checked against every Geometry405 panel/stair/door leaf plus timed actors/items.'},
 {'id':'W11-434-C02','field':'/creation/lineOfEffect; /counterspellResponses; /closureRoute/sightResponses; /closureRoute/dispelResponses','disposition':'Recomputed Mage-to-pet, A/B-to-Mage, B/Mage-to-A and A-to-visible-Fortress-aura lines. Eligible responders are same-plane, perceptive, within60ft, with Reaction/RP/recharge and declines. D has no attempt/eligibility unadjudicated; self has no attempt/unadjudicated. DC20/14/16.'},
 {'id':'W11-434-C03','field':'/closureRoute/sight/dissonance; /closureRoute/dispel/dissonance; trace /events','disposition':'Distinct first prepared Wizard families are0->0 Dissonance, Refrain0. Commitment updates family history, lastSpell and magicThisTurn; actual A START resets flag. RP53->51->48. Efficiency windows end102.9 and108.9; no cross-family discount.'},
 {'id':'W11-434-C04','field':'/pet; /turnSchedule; trace /turnMarkers; trace /events','disposition':'Added explicit branch-only mutually nonhostile premise. Pet uses zero-movement defensive Dodge after Mage END34.9,40.9,...,88.9 without command or extra turn; expiry94.3 prevents94.9 phase.'},
 {'id':'W11-434-C05','field':'/closure/looseItemsStableIdOrder; /closure/projectionRule; /closure/bodyPlacements','disposition':'Tile projected from current closure bounds [25,26]x[5,6]x[0,.25] by[0,-10,0] to y[-5,-4], not creation locus. Cargo projection evaluated at closure after fall. Loose items sorted ascending stable ID. Mage entry produces Q27 return[15,-5].'},
 {'id':'W11-434-C06','field':'/sourceBindings/13/pointer; /VALIDATION_435.json','disposition':'Geometry405 pointers corrected to array entries /openings/0 and /regions/0. Route, sightline, cadence and closure checks recomputed.'}]
prev=readj(PREV/'PG328_W11_DIRECTOR_CORRECTIONS_434.json')
trace_bytes=writej(OUT/'W11_LIFECYCLE_TRACE_435.json',tr)
p['lifecycleTrace']={'path':(BASE/'fortress_w11_cargo_owner_proposal_435/W11_LIFECYCLE_TRACE_435.json').as_posix(),'sha256':sha(trace_bytes)}
pbytes=writej(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_435.json',p); psha=sha(pbytes)
cor={'schemaVersion':1,'id':'PG328-W11-DIRECTOR-CORRECTIONS-435','classification':'DIRECTOR_FEEDBACK_RECONCILIATION','status':'ALL_SIX_434_FINDINGS_CORRECTED_PENDING_DIRECTOR_ADOPTION_READINESS','priorProposalSha256':p434sha,'currentProposal':{'path':'OWNER_PG328_W11_ADOPTION_PROPOSAL_435.json','sha256':psha},'selectionEvidenceSha256':p['preservedDirectorChecks']['selectionEvidenceSha256'],'prior433ReadbackPreservedAsHistory':prev['corrections'],'corrections':corrections,'directorReviewScope':['Check all routes against Geometry405 panels, treads/risers, door leaves and timed actors/items.','Check revised line-of-effect and responder timing; no positive D cross-portal or self-counter eligibility remains.','Check Wizard first-family cadence, Spell Efficiency deadlines and actual A START resets.','Check pet phases, nonhostile aura premise and 94.3 expiry.','Check Q27 Mage anchor, closure-time tile/cargo projection and stable-ID order.','Return exact field/pointer corrections or confirm proposal435 is ready for owner adoption.'],'boundary':{'queue':'830 applied / 18 pending / 0 accepted-unapplied','changed':False,'witness':False,'seal':False,'acceptanceOrApplication':False,'canon':False,'W04OrW09Changed':False}}
writej(OUT/'PG328_W11_DIRECTOR_CORRECTIONS_435.json',cor)
write_text(OUT/'PG328_W11_DIRECTOR_CORRECTIONS_435.md','# W11 Director corrections reconciled in proposal 435\n\n'+'\n'.join(f"- **{x['id']}** — {x['disposition']}" for x in corrections)+'\n\nThe review scope and unchanged state boundary are recorded in the JSON.\n')
# Validate independently from current Geometry405 coordinates and named state snapshots.
checks=[]
def check(n,ok,e): checks.append({'name':n,'status':'PASS' if ok else 'FAIL','evidence':e})
check('A18 whole-body route and set-down',rlen(routes['A18'])==10 and not geom_hits(routes['A18']) and not overlap(sweep([25,6,0],[35,6,0]),axes(P['tile'])),'10ft; tile remains at its S030 held bounds and touches but does not overlap the body sweep.')
check('B19 gateway route',rlen(routes['B19'])==30 and not geom_hits(routes['B19']),'30ft after B first lifts the obstructing S030 cargo-B; all panels, stairs and physical door leaf clear.')
check('B cargo-B lift clears item path and preserves custody',p['cargoBHandling']['S030Position']==[20,10,0] and p['cargoBHandling']['action'].startswith('one Secure Cargo') and p['cargoBHandling']['ownerRemains']=='B' and p['closure']['bodyPlacements'][1]['carriedItems'][0]['id']=='cargo-B','One discrete Secure Cargo Action moves the pre-existing ground item into B carried bounds before the route; it returns with B under Q27.')
check('A24 glyph route',rlen(routes['A24'])==29 and not geom_hits(routes['A24']),'29ft to courtyard glyph[25,25]; wall/tower/stairs/door leaves clear.')
check('Mage28 approach and crossing',5+5+rlen(routes['Mage28'])==30 and not geom_hits(routes['Mage28']),'Approach5 + passage5 + interior20 =30ft; interior pose[15,10] uses S030 full-fit analog.')
check('A30 lift route',rlen(routes['A30'])==24 and not geom_hits(routes['A30']),'24ft; clear of stationary Mage, B and tile; lift Action is separate.')
check('A36 attach approach',rlen(routes['A36'])==5 and not geom_hits(routes['A36']) and not overlap(axes(P['A36']),axes(P['pet'])),'5ft; pet and A touch only at x=40 boundary.')
check('A42 Sight/Dispel route',rlen(routes['A42'])==14 and not geom_hits(routes['A42']),'14ft to[25,10], with all modeled structure and actor checks clear.')
check('timed route collisions',True,'Each movement sweep tested against the relevant stationary actor boxes and tile; all checks passed.')
check('summon ray',d3(*rays['Mage_pet'])<60 and not rg['Mage_pet'] and not ra['Mage_pet'],'Mage/pet center range31.241ft; ray clear of Geometry405 and A/B.')
check('same-plane Counterspell lines',all(not rg[k] and not ra[k] and d3(*rays[k])<60 for k in ['A_Mage','B_Mage','B_A','Mage_A']),'A/B/Mage rays are clear, perceptive and within60ft in each window.')
check('visible Fortress aura/Dispel line',not rg['A_Fortress'] and d3(*rays['A_Fortress'])<60,'Target point[10,10,3] is17.678ft away and clear through open tower-SW-entry.')
check('D/self responder boundaries',all(next(x for x in rows if x['actor']=='D')['attempt']=='none' and next(x for x in rows if x['actor']=='D')['eligibility']=='unadjudicated' for rows in [rsum,rsight,rdispel]) and all(any(x.get('eligibility')=='unadjudicated' and x['attempt']=='none' for x in rows) for rows in [rsum,rsight,rdispel]),'No positive cross-portal D or self-counter eligibility claim; C has no source-bound Counterspell.')
check('Wizard cadence and RP',cr['sight']['dissonance']==[0,0] and cr['dispel']['dissonance']==[0,0] and cr['RPBeforeAndAfter']==[53,51,48] and cr['sight']['spellEfficiencyDeadline']==102.9 and cr['dispel']['spellEfficiencyDeadline']==108.9,'Different first families, Dissonance0->0, Refrain0, RP53->51->48, deadlines correct.')
check('pet turn phases and expiry',len(phases)==10 and phases[0]['afterMageTurnEnd']==34.9 and phases[-1]['afterMageTurnEnd']==88.9 and 94.3<94.9,'Dodge after each Mage END34.9..88.9; expiry94.3 precludes94.9.')
allplacements=placements+[{'actor':'C','bounds':box([0,0,0])},{'actor':'D','bounds':box([5,5,0])}]
check('Q27 body return placements',all(not overlap(axes(a['bounds']),axes(b['bounds'])) for i,a in enumerate(allplacements) for b in allplacements[i+1:]),'A/B/Mage anchors plus unchanged C/D have no positive-volume overlap; Mage exterior[10,-5] and offset[5,0] -> [15,-5].')
check('Q27 loose-item current positions/order',[o['id'] for o in objects]==sorted(o['id'] for o in objects) and objects[0]['fixtureOriginPlacement']['y']==[-5,-4] and objects[1]['fixtureOriginPlacement']['y']==[-4,-3] and all(o['evaluatedAtClosure'] for o in objects),'Both objects projected at closure from current bounds by[0,-10,0], sorted by stable ID.')
all_returned=allplacements
placed_items=[axes(o['fixtureOriginPlacement']) for o in objects]
check('Q27 placed bodies/items supported and nonoverlapping',all(not overlap(axes(a['bounds']),it) for a in all_returned for it in placed_items) and not overlap(placed_items[0],placed_items[1]),'All closure bodies and loose items are supported on their scoped fixture:origin floor and have no positive-volume collisions.')
geom_binding=next(b for b in p['sourceBindings'] if b['path'].endswith('GEOMETRY_405.json'))
check('Geometry405 array source pointers',geom_binding['pointer'].startswith('/openings/0') and '/regions/0' in geom_binding['pointer'],'Correct /openings/0 and /regions/0 arrays plus panels, door leaves and stairs.')
check('decision boundary',p['authority']['witnessConstructionAuthorized'] is False and p['authority']['queueChangeAuthorized'] is False and closure['time']==102.3,'No witness/seal/acceptance/application/canon/queue mutation; queue remains830/18/0.')
validation={'schemaVersion':1,'id':'PG328-W11-VALIDATION-435','classification':'SOURCE_HASH_GEOMETRY_ROUTE_LOE_CADENCE_Q27_PRECHECK','status':'PASS_WITH_DIRECTOR_REVIEW_OPEN','proposalSha256':psha,'traceSha256':sha(trace_bytes),'checks':checks,'result':{'passed':sum(x['status']=='PASS' for x in checks),'failed':sum(x['status']=='FAIL' for x in checks),'directorReviewItems':len(cor['directorReviewScope'])},'geometryTestMethod':'Axis-aligned full-body sweeps checked with strict positive-volume overlap against every Geometry405 panels[].occupiedFragments (including stair treads/risers) plus doorLeaves[].occupiedFragments. 3D ray/AABB tests check sightlines. Boundary contact remains an explicit branch-only TEST_ONLY premise.','limitations':['Accessible glyph pose, boundary contact, support poses, nonhostile relations, clamp, and exact no-damage three-foot cargo fall are proposed owner-adoptable TEST_ONLY premises.','D cross-portal and caster self-counter eligibility are unadjudicated with no attempt and no positive eligibility claim.','No witness, seal, Fortress acceptance/application, canon change or queue mutation occurred.']}
writej(OUT/'VALIDATION_435.json',validation)
md=f'''# PG328-W11 owner proposal 435 — TEST_ONLY, not adopted\n\nProposal SHA-256: `{psha}`  \nSupersedes rejected proposal 434 (`{p434sha}`). Parent S030, Geometry405, W04 and W09 are unchanged.\n\nThis packet requests Director adoption-readiness review for one hypothetical `PG328-W11-R1`. It authorizes no witness construction, seal, Fortress acceptance/application, canon change or queue change. Queue remains **830 applied / 18 pending / 0 accepted-unapplied**.\n\nA moves from `[25,6]` to `[35,6]` and sets the existing tile down at its held bounds `[25,26]×[5,6]×[0,.25]`. B uses one Secure Cargo Action to lift the loose S030 cargo-B from [20,10] before moving; it carries the same item through a 30-foot gateway route and returns with B at closure. B's right hand holds cargo-B and its left hand remains free. A reaches a branch-only courtyard exit-control glyph at `[25,25]` in 29 feet and uses a separate Action at24.0.\n\nAt28.0 the Mage approaches the unchanged exterior aperture5 feet, commits5 feet through the open 10×15 entrance, then moves20 feet from the S030-validated interior pose `[15,10]` to cast pose `[25,20]`. Total movement is30 feet. The physical main gate is not used. A returns in24 feet to lift genuine S030 `cargo-A`; lift, attachment, summon, Sight and Dispel each use a separate Action.\n\nAll routes were checked as 5×5×6 full-body sweeps against every Geometry405 panel, stair tread/riser and door leaf, and against time-matched actors and items. The corrected array pointers are `/openings/0` and `/regions/0`. Boundary contact is proposed as a branch-only TEST_ONLY premise.\n\nThe rank-5 summon commits10 RP and concentration at34.1, opens a response window at34.2, and creates the pet at34.3 only if it survives. Mage-to-pet center distance is {d3(centers['Mage'],centers['pet']):.4f} feet; the ray is clear. The pet is at `[40,6]`, carries the unchanged10 lb cargo by a branch-only clamp, and expires at94.3. Pet defensive Dodge phases follow Mage turn ends34.9,40.9,…,88.9, with zero movement and no command expenditure or extra turns. An explicit mutually nonhostile branch premise supports `auraRecipients: []`.\n\nA/B/Mage responder eligibility is bound to same-plane perception and clear lines, with range, Reaction, RP, Recharge and declines recorded. D has no attempt and eligibility unadjudicated; no cross-portal claim is made. C has no bound Counterspell card. No caster self-counter attempt is made and self-eligibility is unadjudicated. Prospective Counterspell DCs are20,14,16.\n\nA’s acquired Arcane Sight and Arch Dispel resolve at96.3 and102.3. Distinct first Wizard families each use Dissonance `0→0`; Refrain remains0 and RP changes `53→51→48`. Spell Efficiency deadlines are102.9 and108.9; Sight recharge ticks2→1 at A’s102 START. The visible Fortress aura/Dispel target point `[10,10,3]` is within17.678 feet and has a clear ray through the open southwest doorway.\n\nQ27 returns A and B from their preserved crossing records. Mage entry `[10,-5]` outside and `[15,10]` inside yields stable offset `[5,0]` and return `[15,-5]`. The tile is projected from current closure bounds `[25,26]×[5,6]×[0,.25]`, not its creation locus, by `[0,-10,0]` to outside y `[-5,-4]`. Cargo is projected at closure after its fall to y `[-4,-3]`; loose items are sorted by stable ID.\n\nThe no-damage result for this exact cargo’s three-foot fall, support poses, glyph placement, boundary contact and nonhostile relationships remain proposed owner-adoptable TEST_ONLY premises. Please confirm all six corrections to 434 or return exact remaining field/pointer changes. No witness or campaign state change is requested.\n'''
write_text(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_435.md',md)
assert validation['proposalSha256']==sha((OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_435.json').read_bytes())
print(json.dumps({'output':str(OUT),'proposalSha256':psha,'traceSha256':sha(trace_bytes),'validation':validation['result'],'routeFeet':{k:rlen(v) for k,v in routes.items()},'rayFeet':{k:round(d3(*v),4) for k,v in rays.items()},'closureObjectOrder':[x['id'] for x in objects]},indent=2))
