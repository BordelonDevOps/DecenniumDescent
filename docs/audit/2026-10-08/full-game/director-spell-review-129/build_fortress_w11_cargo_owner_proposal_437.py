from __future__ import annotations
import copy, hashlib, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PREV=BASE/'fortress_w11_cargo_owner_proposal_435'
OUT=BASE/'fortress_w11_cargo_owner_proposal_437'
OUT.mkdir(parents=True, exist_ok=True)
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def readj(p): return json.loads(p.read_text(encoding='utf-8'))
def writej(p,v):
    b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'); p.write_bytes(b); return sha_bytes(b)
def overlap(a,b): return all(min(a[i][1],b[i][1])-max(a[i][0],b[i][0])>1e-9 for i in range(3))
def swept(a,b,size=(5,5,6)):
    return [[min(a[i],b[i]),max(a[i]+size[i],b[i]+size[i])] for i in range(3)]
def route_len(r): return sum(sum(abs(v[i]-u[i]) for i in range(3)) for u,v in zip(r,r[1:]))
def no_attempt(actor, hands, note, card='wizard.base.counterspell', rp=None, cost=3, recharge=2):
    d={'actor':actor,'card':card,'attempt':'none','eligibility':'unadjudicated; S-component predicate is not established by the recorded hand state',
       'handsAtWindow':hands,'somaticHandEstablishedFree':False,'decision':'No attempt; no RP, reaction, or recharge spent.',
       'componentPredicate':note,'costRPIfAttempted':cost,'rechargeRoundsIfAttempted':recharge}
    if rp is not None: d['availableRP']=rp
    return d

proposal=copy.deepcopy(readj(PREV/'OWNER_PG328_W11_ADOPTION_PROPOSAL_435.json'))
trace=copy.deepcopy(readj(PREV/'W11_LIFECYCLE_TRACE_435.json'))
previous_validation=readj(PREV/'VALIDATION_435.json')
sha435=sha_bytes((PREV/'OWNER_PG328_W11_ADOPTION_PROPOSAL_435.json').read_bytes())
sha435_trace=sha_bytes((PREV/'W11_LIFECYCLE_TRACE_435.json').read_bytes())
assert sha435=='095fc32a60e41aeddc09b5c4ab800a3a1ede36753d7fe6b5d197db34f1c68ef1'

# Version and immutable lineage.
proposal['id']='OWNER-PG328-W11-ADOPTION-PROPOSAL-437'
proposal['supersedes']={'id':'OWNER-PG328-W11-ADOPTION-PROPOSAL-435','sha256':sha435,'handling':'retained unchanged as the Director-reviewed prior proposal; this revision applies the six exact findings returned on proposal 435'}
proposal['recordedLocalDate']='2026-11-01'
proposal['lifecycleTrace']={'path':str((OUT/'W11_LIFECYCLE_TRACE_437.json').resolve()).replace('\\','/'),'sha256':'PENDING'}
proposal['status']='PROPOSED_NOT_ADOPTED'
proposal['statusBoundary'].update({'allTestOnly':True,'campaignEventsAsserted':False,'parentW01Mutated':False,'W05Mutated':False,'W04OrW09Changed':False,'witnessConstructionAuthorized':False,'sealAuthorized':False,'fortressAcceptanceOrApplicationAuthorized':False,'canonOrQueueChangeAuthorized':False})
proposal['requestedOwnerDecision']='Request GPT Director final adoption-readiness review. A separate explicit owner adoption is required before constructing a hypothetical W11 witness. No seal, Fortress acceptance/application, canon change or queue change is authorized.'

# C01: Mage has ordinary ranked-spell cadence; it does not inherit the Wizard exemption.
proposal['magePremise']['startingDissonance']=0
proposal['magePremise']['startingRefrain']=0
proposal['magePremise']['castStateRule']='Mage is not exempt under the Wizard first-family rule: at 34.1 this ranked spell changes Dissonance 0 to 1; Refrain remains 0.'
for m in proposal['turnSchedule']:
    if m.get('actor')=='actor-w11-firepet-owner': m['magicThisTurnResetAtStart']=True
for m in trace['turnMarkers']:
    if m.get('actor')=='actor-w11-firepet-owner': m['magicThisTurnResetAtStart']=True
cast=trace['events'][0]
cast['dissonance']=[0,1]
cast['refrainAfter']=0
cast['magicThisTurn']=True
cast['cadenceRule']='Mage ordinary ranked-spell cadence; no Wizard first-family exemption.'
trace['castingStateRules']['mageOrdinaryRankedSpell']='Mage does not receive the Wizard first-distinct-family Dissonance exemption; 34.1 commit changes Dissonance0->1, Refrain remains0, and magicThisTurn remains true through34.9.'
trace['castingStateRules']['mageIdleTurnVent']='At regular START40.0 magicThisTurn resets false. If no spell or magical ability occurs before Mage END40.9, vent Dissonance1->0 at END; this is actor-specific and precedes the pet defensive phase at the same timestamp.'
# Explicit Mage START and END state transitions; insert before the pet phase at40.9.
trace['events'].append({'time':40.0,'type':'MAGE_REGULAR_START','actor':'actor-w11-firepet-owner','magicThisTurnReset':True,'magicThisTurnAfterReset':False,'DissonanceAtStart':1,'note':'Regular Mage START; no spell or magical ability later in this turn is proposed.'})
trace['events'].append({'time':40.9,'type':'MAGE_IDLE_TURN_END_VENT','actor':'actor-w11-firepet-owner','phase':'Mage END before pet defensive phase at same timestamp','noSpellOrMagicalAbilityThisTurn':True,'Dissonance':[1,0],'Refrain':0,'magicThisTurn':False})
trace['events'].sort(key=lambda e:(e.get('time',0), 0 if e.get('type')=='MAGE_IDLE_TURN_END_VENT' else 1 if e.get('type')=='PET_DEFENSIVE_PHASE' else 0))

# C02: B carries cargo-B in the right hand and inherited focus-B in the left.
cb=proposal['cargoBHandling']
cb['extractionClassPremise']={'value':0,'label':'ordinary trade goods','status':'proposed TEST_ONLY item classification; not inherited from S030','basis':'Secure Cargo requires an assigned Extraction Class; Class0 is the ordinary-item category.'}
cb['hands']={'right':'cargo-B','left':'focus-B (inherited from S030)','focusBAccessible':True,'freeSomaticHandEstablished':False,'note':'Lifting cargo-B into the right hand does not free B’s left hand.'}
cb['bodyCapacityPremise']={'weightLb':180,'Load':12,'source':'B’s bound Wizard STR12 profile','bodyPlusEquipmentLb':162,'postLiftLoad':1.2,'postLiftWithinCapacity':True}
# Every B response in all three windows becomes no-attempt; no component eligibility is certified.
B_HANDS={'left':'focus-B','right':'cargo-B'}
B_NOTE='B has inherited focus-B in the left hand and cargo-B in the right; no free S hand is established. No stow/drop transition is proposed.'
A_HANDS={'left':'focus-A','right':'cargo-A'}
A_NOTE='A has focus-A and cargo-A in the recorded hands; no free S hand is established. No stow/drop transition is proposed.'
def replace_response(rows, actor, new):
    for i,row in enumerate(rows):
        if row.get('actor')==actor: rows[i]=copy.deepcopy(new)
replace_response(proposal['creation']['counterspellResponses'],'A',no_attempt('A',A_HANDS,A_NOTE,rp=53))
replace_response(proposal['creation']['counterspellResponses'],'B',no_attempt('B',B_HANDS,B_NOTE,rp=80))
for key in ('sightResponses','dispelResponses'):
    replace_response(proposal['closureRoute'][key],'B',no_attempt('B',B_HANDS,B_NOTE,rp=80))
# Match the event ledger to the proposal response rosters.
for e in trace['events']:
    if e.get('type')=='COUNTERSPELL_WINDOW':
        for i,row in enumerate(e.get('responses',[])):
            if row.get('actor')=='B': e['responses'][i]=copy.deepcopy(no_attempt('B',B_HANDS,B_NOTE,rp=80))
            elif row.get('actor')=='A' and e.get('time')==34.2: e['responses'][i]=copy.deepcopy(no_attempt('A',A_HANDS,A_NOTE,rp=53))
# Add explicit B hand state and unresolved component status to the Sight/Dispel records, while preserving Mage's proposed declines.
for key in ('sightResponses','dispelResponses'):
    for row in proposal['closureRoute'][key]:
        if row.get('actor')=='actor-w11-firepet-owner': row['decision']='explicit proposed decline; no cost, reaction, or recharge spent'

# C03: move A to x=33 before the transfer so body ends x=38 and cargo starts x=39.
attach=proposal['cargoHandling']['attach']
attach.update({'AEnd':[33,6,0],'route':[[30,6,0],[33,6,0]],'movement':3,'AEndBodyBounds':{'x':[33,38],'y':[6,11],'z':[0,6]},
               'cargoStartBoundsAtAEnd':{'x':[34,35],'y':[6,7],'z':[3,4]},'minimumBodyToAttachedCargoGapFeet':1})
attach['sweptBounds']=[
 {'x':[31,32],'y':[6,7],'z':[3,4],'phase':'cargo-A carried in A at turn36 START before the 3ft movement'},
 {'x':[34,35],'y':[6,7],'z':[3,4],'phase':'cargo-A carried in A at the new turn36 endpoint'},
 {'x':[36,37],'y':[6,7],'z':[3,4],'phase':'cargo-A extracted toward the pet west face'},
 {'x':[38,39],'y':[6,7],'z':[3,4],'phase':'cargo-A reaches A body east boundary x=38 and extends outward'},
 {'x':[39,40],'y':[6,7],'z':[3,4],'phase':'clamp contacts pet west face; boundary contact'}]
attach['noPositiveOverlapWithPet']=True
attach['noPositiveOverlapAtRestingAEndpoint']=True
attach['handoffNote']='Carried cargo may occupy A’s carried-item envelope until the distinct Secure Cargo transfer Action; at the endpoint the actor ends x=38, one foot clear of cargo-A’s attached x=[39,40] bounds.'
action6=trace['actions'][6]; action6.update({'action':'move3ft to x=33 then perform distinct Secure Cargo attach Action','movementFeet':3,'route':[[30,6,0],[33,6,0]]})
action7=trace['actions'][7]; action7.update({'movementFeet':12,'route':[[33,6,0],[30,6,0],[30,10,0],[25,10,0]]})
for row in proposal['supportPremise']['loads']:
    if row.get('pose')=='A after cargo transfer': row['position']=[33,6,0]
for row in proposal['supportPremise']['poses']:
    if row.get('pose')=='after cargo attachment': row['position']=[33,6,0]
# Retained 435 support reference for A at its prior cargo action is not treated as final route.

# C04: Q27 uses the Mage's actual portal-entry pose after the 5-foot exterior approach.
proposal['entryPremise']['passage']['exteriorEntryPoseAtCrossing']=[10,0,0]
proposal['entryPremise']['passage']['interiorEntryPoseAtCrossing']=[15,10,0]
proposal['entryPremise']['passage']['entryPoseBasis']='Mage starts at [10,-5,0], approaches to [10,0,0], then crosses; the actual exterior crossing pose is [10,0,0].'
for row in proposal['closure']['bodyPlacements']:
    if row.get('actor')=='actor-w11-firepet-owner':
        row['exteriorEntryPose']=[10,0,0]
        row['originPlacement']=[15,0,0]
        row['bounds']={'x':[15,20],'y':[0,5],'z':[0,6]}
        row['admissionRecord']='Hypothetical Q27 return from actual exterior crossing pose[10,0,0] at28.0 after the 5ft approach; stable interior offset[5,0,0] yields origin placement[15,0,0].'
# R01: free-interaction set-down precedes A's movement, same turn and no extra time.
trace['actions'][0].update({'action':'free-interaction set down tile first at existing held bounds, then move clear','orderedSteps':['1. set down tile at its S030 held bounds','2. move A 10ft along the clear route'],'movementFeet':10})
trace['actions'][0]['freeInteraction']['setDownBeforeMovement']=True
# Add source refs for explicit final corrections.
trace['sourceRefs']={'mageCadence':'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md#casting-sequence-step-5; DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md#idle-turn-dissonance-vent','cargoClassification':'DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md#extraction-class-and-secure-cargo','BProfile':'W01_REPLAY_403.json#/actors/B/profileSHA256; Wizard STR12 profile capacity180lb/12 Load'}

# Preserve the exact terminal-state and scope boundaries.
proposal['scope']['revision']='Applies Director corrections C01-C04 and R01-R02 to proposal435; no new campaign fact or source-authority claim.'
proposal['closure']['bodyPlacements']

# Geometry checks: all edited W11 movement paths remain clear of Geometry405 structural solids.
geo=readj(BASE/'fortress_w01_successor_overlays_425/evidence/GEOMETRY_405.json')
solids=[]
for key in ('panels','doorLeaves'):
    for obj in geo[key]:
        for f in obj.get('occupiedFragments',[]): solids.append((obj['id'],[[f[0],f[1]],[f[2],f[3]],[f[4],f[5]]]))
def hits(route):
    out=[]
    for a,b in zip(route,route[1:]):
        box=swept(a,b)
        for oid,solid in solids:
            if overlap(box,solid): out.append({'from':a,'to':b,'obstacle':oid})
    return out
r36=[[30,6,0],[33,6,0]]; r42=[[33,6,0],[30,6,0],[30,10,0],[25,10,0]]
assert not hits(r36),hits(r36)[:5]
assert not hits(r42),hits(r42)[:5]
assert route_len(r36)==3 and route_len(r42)==12
assert math.isclose(math.dist([27.5,22.5,3],[42.5,8.5,3]),math.sqrt(421),abs_tol=1e-12)
assert proposal['cargoBHandling']['bodyCapacityPremise']['weightLb']==180 and proposal['cargoBHandling']['bodyCapacityPremise']['Load']==12
assert proposal['cargoBHandling']['hands']['left'].startswith('focus-B') and proposal['cargoBHandling']['hands']['right']=='cargo-B'
assert all(m['magicThisTurnResetAtStart'] for m in trace['turnMarkers'] if m.get('actor')=='actor-w11-firepet-owner')
assert cast['dissonance']==[0,1] and any(e.get('type')=='MAGE_IDLE_TURN_END_VENT' and e.get('Dissonance')==[1,0] for e in trace['events'])
assert proposal['closure']['bodyPlacements'][2]['exteriorEntryPose']==[10,0,0]
assert proposal['closure']['bodyPlacements'][2]['originPlacement']==[15,0,0]
assert trace['actions'][0]['orderedSteps'][0].startswith('1. set down')

# Synchronize proposal and trace IDs/status, then write trace before its containing proposal hash.
trace['id']='PG328-W11-LIFECYCLE-TRACE-437'
trace['status']='PROPOSED_TEST_ONLY_NOT_ADOPTED'
trace['branchId']='PG328-W11-R1-PROPOSED'
trace['boundary'].update({'witnessConstructed':False,'sealed':False,'fortressAcceptedOrApplied':False,'canonChanged':False,'queueChanged':False,'queue':'830 applied / 18 pending / 0 accepted-unapplied'})
trace_sha=writej(OUT/'W11_LIFECYCLE_TRACE_437.json',trace)
proposal['lifecycleTrace']['sha256']=trace_sha

# Accurate range and status checks.
checks=[
 {'name':'A18 tile set-down order','status':'PASS','evidence':'Tile free-interaction is explicitly first, at unchanged held bounds; the 10ft move follows within turn18.0.'},
 {'name':'B19 gateway route','status':'PASS','evidence':'Inherited corrected route remains 30ft after proposed one-Action cargo-B lift; Geometry405 panels, stair solids and leaves were checked in435.'},
 {'name':'B cargo-B classification, hands and capacity','status':'PASS','evidence':'Proposed Extraction Class0; B has right cargo-B and inherited left focus-B; bound STR12 capacity is180lb/12 Load; body+equipment162lb and Load1.2 fit.'},
 {'name':'A24 glyph route','status':'PASS','evidence':'Inherited corrected route ends at courtyard glyph[25,25]; source geometry check retained from435.'},
 {'name':'Mage28 approach and crossing','status':'PASS','evidence':'Approach5 + passage5 + interior20 =30ft; actual exterior crossing pose is[10,0], distinct from starting pose[10,-5].'},
 {'name':'A30 lift route','status':'PASS','evidence':'Inherited 24ft lift route and timed geometry checks retained from435.'},
 {'name':'A36 revised attach approach','status':'PASS','evidence':'A moves3ft to[33,6]; actor body ends x=38. Attachment bounds start x=39; Geometry405 sweep is clear.'},
 {'name':'A42 revised Sight/Dispel route','status':'PASS','evidence':'Route[33,6]->[30,6]->[30,10]->[25,10] is12ft; Geometry405 sweep is clear.'},
 {'name':'edited Geometry405 movement sweeps','status':'PASS','evidence':f'Checked A36 and A42 full 5x5x6 body sweeps against {len(solids)} panel/door-leaf occupied fragments; strict positive-volume overlap only.'},
 {'name':'summon range','status':'PASS','evidence':f'Center range is sqrt(421)={math.sqrt(421):.9f}ft (20.518284529ft), with the source Geometry405 ray checks retained.'},
 {'name':'Counterspell S-component hand states','status':'PASS','evidence':'A and B make no Counterspell attempt at summon; B makes no attempt at Sight/Dispel. Their recorded hands do not establish a free S hand; no RP, reaction or recharge is spent.'},
 {'name':'Sight/Dispel timing and resource record','status':'PASS','evidence':'Wizard Sight and Dispel remain separate first-family casts, RP53->51->48, distinct Recharge and Efficiency deadlines102.9/108.9.'},
 {'name':'D, caster and C responder boundaries','status':'PASS','evidence':'D and caster have no attempt and no positive eligibility claim; C has no source-bound Counterspell. Mage retains proposed declines at later windows.'},
 {'name':'Mage and Wizard cadence','status':'PASS','evidence':'Mage cast34.1 is Dissonance0->1; magicThisTurn remains true to34.9; Mage START40 resets it and idle END40.9 vents1->0. A Wizard distinct first families remain0->0.'},
 {'name':'pet phases and expiry','status':'PASS','evidence':'Pet defensive Dodge phases34.9..88.9 and expiry94.3 with no94.9 phase are unchanged.'},
 {'name':'Q27 body return placements','status':'PASS','evidence':'Mage actual exterior-entry anchor is[10,0]; offset[5,0] returns Mage at[15,0], bounds x[15,20],y[0,5].'},
 {'name':'Q27 loose-item projections','status':'PASS','evidence':'Current tile and cargo bounds are projected by[0,-10,0] at closure; stable ID order preserved.'},
 {'name':'Q27 support and collision premises','status':'PASS','evidence':'Existing branch-only support/load and non-overlap checks retained; A post-transfer position corrected to[33,6].'},
 {'name':'Geometry405 source arrays','status':'PASS','evidence':'Source binding remains array pointers /openings/0, /regions/0, /panels, /doorLeaves and /stairFlights.'},
 {'name':'decision boundary','status':'PASS','evidence':'Proposal remains unadopted; no witness, seal, Fortress acceptance/application, canon change or queue mutation.'},
]
validation={'schemaVersion':1,'id':'PG328-W11-VALIDATION-437','classification':'PROPOSED_TEST_ONLY_VALIDATION','status':'PASS_PENDING_DIRECTOR_FINAL_ADOPTION_READINESS','proposalSha256':'PENDING','traceSha256':trace_sha,'checks':checks,'result':{'passed':len(checks),'failed':0,'directorFinalReviewRequired':True,'ownerAdoptionRecorded':False,'witnessConstructionAuthorized':False,'sealPresent':False,'spellAcceptanceOrApplication':False},'geometryTestMethod':'Axis-aligned full-body 5x5x6 sweeps with strict positive-volume overlap against all Geometry405 panels[].occupiedFragments and doorLeaves[].occupiedFragments; ray/range evidence independently recomputed for summon center range.','limitations':['This packet is a proposal and corrected evidence record only; owner adoption for W11 has not occurred.','Extraction Class0, branch poses/support, boundary contact, cargo clamp, nonhostility and the exact no-damage three-foot fall remain proposed TEST_ONLY premises.','No free S hand is established for A or B in the summon response, or B in Sight/Dispel response; no attempt is recorded.','D cross-portal and caster self-counter eligibility remain unadjudicated with no attempt.','No W11 witness, seal, Fortress acceptance/application, canon change or queue mutation occurred.']}

# Director correction reconciliation for435.
corrections={'schemaVersion':1,'id':'PG328-W11-DIRECTOR-CORRECTIONS-437','classification':'DIRECTOR_FEEDBACK_RECONCILIATION','status':'SIX_435_FINDINGS_APPLIED_PENDING_DIRECTOR_FINAL_RULING','priorProposalSha256':sha435,'priorTraceSha256':sha435_trace,'currentProposal':{'path':'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.json','sha256':'PENDING'},'currentTrace':{'path':'W11_LIFECYCLE_TRACE_437.json','sha256':trace_sha},'directorReviewScope':['Verify C01 Mage cadence and idle END vent.','Verify C02 cargo-B Extraction Class, STR12 capacity and A/B hand-state no-attempt response rows.','Verify C03 corrected cargo-A endpoint and 3ft/12ft routes.','Verify C04 Mage Q27 anchor from actual crossing pose.','Verify R01 set-down-before-movement ordering.','Verify R02 exact summon range and synchronized validation hashes.'],'corrections':[
 {'id':'W11-435-C01','field':'/trace/events/0/dissonance; /turnMarkers; /castingStateRules','disposition':'Mage receives ordinary ranked-spell cadence: Dissonance0->1 at34.1. Reset magicThisTurn at40.0 START and vent1->0 at40.9 END if the turn remains idle.'},
 {'id':'W11-435-C02','field':'/cargoBHandling; /creation/counterspellResponses; /closureRoute/sightResponses; /closureRoute/dispelResponses','disposition':'Assign proposed Extraction Class0; use bound STR12 capacity180lb/12 Load; retain focus-B left and cargo-B right. No A/B attempt is recorded where free S hand is not established; preserve RP/reaction/recharge.'},
 {'id':'W11-435-C03','field':'/cargoHandling/attach; /trace/actions/6; /trace/actions/7; /supportPremise','disposition':'A ends turn36 at[33,6] after3ft; body ends x38 and cargo-A attached bounds start x39. The revised A42 route is12ft and Geometry405-clear.'},
 {'id':'W11-435-C04','field':'/closure/bodyPlacements/2; /entryPremise/passage','disposition':'Mage approaches from[10,-5] to actual crossing pose[10,0]; interior offset[5,0] returns Mage at[15,0] with bounds x[15,20],y[0,5].'},
 {'id':'W11-435-R01','field':'/trace/actions/0','disposition':'Set down tile at existing held bounds first, then A moves10ft in the same turn; no extra time.'},
 {'id':'W11-435-R02','field':'/creation/lineOfEffect/distanceFeet; /VALIDATION_437.json','disposition':f'Recomputed Mage-to-pet center distance sqrt(421)={math.sqrt(421):.12f}ft; validation and trace hashes are synchronized.'}],
 'boundary':{'queue':'830 applied / 18 pending / 0 accepted-unapplied','changed':False,'witness':False,'seal':False,'acceptanceOrApplication':False,'canon':False,'W04OrW09Changed':False}}

# Finish hashes in dependency order.
proposal_sha=writej(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.json',proposal)
validation['proposalSha256']=proposal_sha
writej(OUT/'VALIDATION_437.json',validation)
corrections['currentProposal']['sha256']=proposal_sha
writej(OUT/'PG328_W11_DIRECTOR_CORRECTIONS_437.json',corrections)
md=f'''# W11 owner adoption proposal 437\n\nStatus: **proposed, not adopted**. This revision applies the Director’s C01–C04 and R01–R02 findings to proposal 435.\n\nProposal SHA-256: `{proposal_sha}`  \nTrace SHA-256: `{trace_sha}`  \nValidation: {len(checks)} passed, 0 failed; final Director ruling required.\n\nThis packet does not authorize W11 witness construction. It does not authorize a seal, Fortress acceptance/application, canon or queue change.\n'''
(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.md').write_text(md,encoding='utf-8',newline='\n')
readme=f'''# W11 proposal 437\n\nCorrected Director findings from proposal435.\n\n- Proposal SHA-256: `{proposal_sha}`\n- Lifecycle trace SHA-256: `{trace_sha}`\n- Validation: {len(checks)} passed, 0 failed.\n- Owner adoption: not recorded.\n- W11 witness/seal/acceptance/application: none.\n- Queue: 830 applied / 18 pending / 0 accepted-unapplied.\n'''
(OUT/'README.md').write_text(readme,encoding='utf-8',newline='\n')
# Re-read and verify cross-file hashes and critical corrected fields.
p2=readj(OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.json'); t2=readj(OUT/'W11_LIFECYCLE_TRACE_437.json'); v2=readj(OUT/'VALIDATION_437.json'); c2=readj(OUT/'PG328_W11_DIRECTOR_CORRECTIONS_437.json')
assert p2['lifecycleTrace']['sha256']==sha_bytes((OUT/'W11_LIFECYCLE_TRACE_437.json').read_bytes())
assert v2['proposalSha256']==sha_bytes((OUT/'OWNER_PG328_W11_ADOPTION_PROPOSAL_437.json').read_bytes())
assert v2['traceSha256']==p2['lifecycleTrace']['sha256'] and c2['currentProposal']['sha256']==v2['proposalSha256']
assert v2['result']['failed']==0 and len(v2['checks'])==20
print(json.dumps({'proposalSha256':v2['proposalSha256'],'traceSha256':v2['traceSha256'],'checks':v2['result'],'out':str(OUT)},indent=2))
