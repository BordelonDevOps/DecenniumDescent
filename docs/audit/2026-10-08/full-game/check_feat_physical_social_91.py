"""Independent source-bound physical/social fixture calculations; no project/downloaded imports.

These are authored diagnostic slices. Acquired feats and legal world providers are
explicit input premises, not grants or executed campaign actors. Source packets
preserve the full records needed for later parent335 exact review.
"""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib, json, zipfile

G = Path(r'C:\Github\DecenniumDescent'); R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'; I = R / 'data/director/feat_candidates/exact_01'
ROOT = A / 'feat335-physical-social-91'
OUT = A / 'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json'
ZIP = A / 'DD_Feat335_Physical_Social_Compositions_91.zip'
SAVED = A / Path(__file__).name
for p in (ROOT, OUT, ZIP, SAVED): assert not p.exists(), str(p)

def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def info(p):
    b = p.read_bytes(); return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
checks, cases = [], []
def ck(label, actual, expected=True):
    ok = actual == expected
    checks.append({'check': label, 'pass': ok, 'actual': actual, 'expected': expected})
    assert ok, label + ': ' + repr(actual) + ' != ' + repr(expected)
def case(cid, title, inputs, actual, expected, sources, qualification=None):
    ck(cid + ' ' + title, actual, expected)
    cases.append({'id': cid, 'title': title, 'inputs': deepcopy(inputs), 'computed': deepcopy(actual), 'expected': deepcopy(expected), 'sourceRefs': sources,
                  'qualification': qualification or 'Source-qualified authored diagnostic. Actual lawful acquisition, credentials, actor/body/geometry, provider access and native event eligibility are input premises; this neither grants them nor executes a campaign engine.'})

paths = [I/'candidate.json', I/'shared_rules.json', R/'data/public/feat_candidates/exact_01/candidate.json',
         R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
         R/'docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md', R/'data/playtest/equipment_acquisition_candidate.json',
         R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md', R/'docs/mechanics/CONTROL_STATES_PLAYTEST.md',
         R/'data/director/expedition_candidate/complete_candidate.json', R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',
         A/'EX58_EDIT_02_FULFILLMENT.json', A/'EX58_X01_FULFILLMENT.json',
         A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json', A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA_FULFILLMENT.json',
         A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',
         A/'feat335-work-compositions84-part5-return-01/MODEL.json', A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json']
bindings = [info(p) for p in paths]
records = {x['id']: x for x in j(paths[0])['records']}
public = {x['id']: x for x in j(paths[2])['feats']}
selected_ids = ['lock_savant','burglar','trap_sense','trapsetter','cavalry','mounted_combatant','silver_tongue','diplomat','negotiator','merchant_s_guile','appraise']
selected = {k: records[k] for k in selected_ids}
for key, record in selected.items():
    ck(key + ' public/internal procedure text matches', record['operationalRules'], public[key]['operationalRules'])
    ck(key + ' remains unpromoted', not record['selectionEnabled'] and not record['exactApproved'] and not record['runtimeApproved'])
shared = {x['id']: x for x in j(paths[1])['rules']}
equipment = {x['id']: x for x in j(paths[6])['items']}
for name, price, weight in [('adventuring-gear.caltrops-bag-of-20',100,2), ('adventuring-gear.lock',1000,1), ('tools.thieves-tools',2500,1)]:
    ck(name + ' actual price/weight', [equipment[name]['sourcePriceCp'], equipment[name]['sourceWeightLb']], [price, weight])
book = paths[10].read_text(encoding='utf-8')
for text in ['P=max(0.10×F,S)', 'P−S=max(0,0.10×F−S)', 'immediately **after** the rider', 'original scene-opening score', 'round a final sale receipt **down** once']:
    ck('Current full EX58 governing text: ' + text, text in book)

def task(face, modifier, dc):
    if face not in range(1,21): raise ValueError('Actual d20 face required')
    total = face + modifier
    degree = 3 if total >= dc+10 else 2 if total >= dc else 0 if total <= dc-10 else 1
    degree = max(0, min(3, degree + (1 if face == 20 else -1 if face == 1 else 0)))
    return {'total': total, 'degree': ['critical-failure','failure','success','critical-success'][degree], 'success': degree >= 2}

# Lock outcomes retain source time/DC and numerical margin separately from task degree.
def lock(face, dex, pb, expertise, burglar, savant, complex_lock, dc, touch_trigger=False):
    modifier = dex + pb * (2 if expertise else 1) + (2 if burglar else 0) + (2 if savant and complex_lock else 0)
    result = task(face, modifier, dc)
    failed_trigger = not result['success'] and not (savant and dc-result['total'] < 5)
    return {**result, 'modifier': modifier, 'failureOnlyTrapFires': failed_trigger, 'independentTouchTriggerFires': touch_trigger, 'actionSpent': 1}
for suffix, values, expected in [
 ('01',(8,3,2,False,True,False,False,15), {'total':15,'degree':'success','success':True,'modifier':7,'failureOnlyTrapFires':False,'independentTouchTriggerFires':False,'actionSpent':1}),
 ('02',(6,3,2,True,True,False,False,15), {'total':15,'degree':'success','success':True,'modifier':9,'failureOnlyTrapFires':False,'independentTouchTriggerFires':False,'actionSpent':1}),
 ('03',(5,3,2,False,True,True,True,18), {'total':14,'degree':'failure','success':False,'modifier':9,'failureOnlyTrapFires':False,'independentTouchTriggerFires':False,'actionSpent':1}),
 ('04',(4,3,2,False,True,True,True,18), {'total':13,'degree':'failure','success':False,'modifier':9,'failureOnlyTrapFires':True,'independentTouchTriggerFires':False,'actionSpent':1}),
 ('05',(1,5,6,False,True,True,True,18,True), {'total':16,'degree':'critical-failure','success':False,'modifier':15,'failureOnlyTrapFires':False,'independentTouchTriggerFires':True,'actionSpent':1}),
 ('06',(10,3,2,False,True,True,False,15), {'total':17,'degree':'success','success':True,'modifier':7,'failureOnlyTrapFires':False,'independentTouchTriggerFires':False,'actionSpent':1})]:
    case('FP91-L'+suffix,'Lock source, feat stacking and actual failure margin',{'orderedArguments':list(values)},lock(*values),expected,['lock_savant','burglar','FS-03','FS-05','FS-15','EQUIPMENT_ITEM_PROCEDURES#Ordinary lock'])
def retry_same_lock(prior_failed, changed_evidence, changed_speaker):
    return {'newAttemptAllowed': not prior_failed or changed_evidence, 'newSpeakerResetsFailure': False}
case('FP91-L07','Swapping picker alone does not reopen unchanged failure',{'priorFailure':True,'newSpeaker':True,'changedEvidence':False},retry_same_lock(True,False,True),{'newAttemptAllowed':False,'newSpeakerResetsFailure':False},['burglar'])
case('FP91-L08','Materially improved tools allow a new actual Action',{'priorFailure':True,'newSpeaker':False,'changedEvidence':True},retry_same_lock(True,True,False),{'newAttemptAllowed':True,'newSpeakerResetsFailure':False},['burglar'])

def detection(wis,pb,trained,dc,accessible,normal_pace,active_required=False):
    value = 10+wis+(pb if trained else 0)
    return {'passive':value,'noticesClue':accessible and normal_pace and not active_required and value>=dc,'naturalDieRolled':False,'automaticallyDisarmed':False}
for suffix, args, noticed in [('01',(2,3,True,15,True,True),True),('02',(2,3,True,15,False,True),False),('03',(2,3,True,15,True,True,True),False),('04',(2,3,True,16,True,True),False)]:
    case('FP91-P'+suffix,'Passive clue detection respects source access',{'orderedArguments':list(args)},detection(*args),{'passive':15,'noticesClue':noticed,'naturalDieRolled':False,'automaticallyDisarmed':False},['trap_sense'])
for suffix, visible, expected in [('05',True,True),('06',False,False)]:
    case('FP91-P'+suffix,'Trap save bonus requires current sight',{'face':10,'dexModifier':2,'DC':14,'visibleOperativeTrapComponent':visible}, {'total':10+2+(2 if visible else 0),'success':10+2+(2 if visible else 0)>=14}, {'total':14 if visible else 12,'success':expected},['trap_sense','FS-05'],qualification='Actual trap/native binary DEX save. A remembered component while blinded supplies no current sight; the prior perceptual event is not erased.')

# Persistent caltrop stock: every original physical piece has one location.
piece_ids = ['c'+str(i).zfill(2) for i in range(1,21)]
initial_field = {'fieldId':'field-A','setter':'S','storedDC':14,'armed':True,'physicallyCleared':False,'enhancedAllowanceOccupied':True,
                 'quickUseSpent':True,'pieces':{k:'field-A' for k in piece_ids},'entryReceipts':{},'targets':{},'collectionReceipts':{}}
def conserve(state):
    assert len(state['pieces']) == len(set(state['pieces'])) == 20
    assert set(state['pieces']) == set(piece_ids)
def entry(before,event):
    s=deepcopy(before); key=event['originalEntryId']
    if key in s['entryReceipts']: return s, {'outcome':'duplicate-entry','creditedDamage':0}
    if not event['actualEntry'] or not s['armed'] or s['physicallyCleared']:
        return s, {'outcome':'no-new-entry-or-hazard','creditedDamage':0}
    if not event['sourceQualifiedCoverage']:
        return s, {'outcome':'outside-actual-coverage','creditedDamage':0}
    if event['movingAtHalfSpeed']:
        outcome='half-speed-avoidance'; damage=0
    elif event['saveFace'] + event['saveModifier'] >= s['storedDC']:
        outcome='saved'; damage=0
    else:
        outcome='failed'; damage=1
        piece=event['actualEmbeddedPieceId']; assert s['pieces'][piece] == s['fieldId']
        s['pieces'][piece]='embedded:'+event['target']
        s['targets'][event['target']]={'hp':event['beforeHP']-1,'movementRemaining':0,'walkingReduction':10,'embeddedPieces':[piece]}
    s['entryReceipts'][key]={'target':event['target'],'outcome':outcome,'damage':damage}
    conserve(s); return s, {'outcome':outcome,'creditedDamage':damage}
def event(eid,target,face,**kwargs):
    return {'originalEntryId':eid,'target':target,'saveFace':face,'saveModifier':2,'actualEntry':True,'sourceQualifiedCoverage':True,'movingAtHalfSpeed':False,'beforeHP':10,'actualEmbeddedPieceId':'c01',**kwargs}
def field_summary(state):
    return {'fieldCount':sum(v=='field-A' for v in state['pieces'].values()),'embeddedCount':sum(v.startswith('embedded:') for v in state['pieces'].values()),'collectedCount':sum(v.startswith('container:') for v in state['pieces'].values()),'active':state['armed'],'allowanceOccupied':state['enhancedAllowanceOccupied'],'quickUseSpent':state['quickUseSpent'],'receipts':len(state['entryReceipts']),'targets':deepcopy(state['targets'])}
field_states = []
def field_case(cid,title,before,ev,expected_state,expected_result):
    after,result=entry(before,ev)
    case(cid,title,{'before':before,'event':ev},{'summary':field_summary(after),'result':result},{'summary':expected_state,'result':expected_result},['trapsetter','FS-15','EQUIPMENT_ITEM_PROCEDURES#Caltrops'],qualification='Full caltrop stock/reward state slice. Entrant identity, actual legal entry, defensive eligibility and remaining spatial coverage are explicit source-qualified physical facts. This test does not derive a new piece-count/coverage law, creature defense rule or movement provider.')
    field_states.append({'id':cid,'before':deepcopy(before),'event':deepcopy(ev),'after':deepcopy(after)})
    return after
base_summary={'fieldCount':20,'embeddedCount':0,'collectedCount':0,'active':True,'allowanceOccupied':True,'quickUseSpent':True,'receipts':1,'targets':{}}
s1=field_case('FP91-T01','Successful entry save leaves all20 pieces hazardous',initial_field,event('entry1','A',12),base_summary,{'outcome':'saved','creditedDamage':0})
summary2={**base_summary,'fieldCount':19,'embeddedCount':1,'receipts':2,'targets':{'B':{'hp':9,'movementRemaining':0,'walkingReduction':10,'embeddedPieces':['c01']}}}
s2=field_case('FP91-T02','Second entrant fails; only actual embedded piece moves',s1,event('entry2','B',11),summary2,{'outcome':'failed','creditedDamage':1})
s3=field_case('FP91-T03','Renamed delivery of same entry cannot repeat damage or consume stock',s2,event('entry2','B',11,deliveryId='new-callback'),summary2,{'outcome':'duplicate-entry','creditedDamage':0})
s4=field_case('FP91-T04','Standing still is no new entry',s3,event('standing','B',1,actualEntry=False),summary2,{'outcome':'no-new-entry-or-hazard','creditedDamage':0})
s5=field_case('FP91-T05','Real half-Speed entry avoids a save and consumes no pieces',s4,event('entry3','C',None,movingAtHalfSpeed=True),{**summary2,'receipts':3},{'outcome':'half-speed-avoidance','creditedDamage':0})
summary6={**summary2,'fieldCount':18,'embeddedCount':2,'receipts':4,'targets':{**summary2['targets'],'D':{'hp':9,'movementRemaining':0,'walkingReduction':10,'embeddedPieces':['c02']}}}
s6=field_case('FP91-T06','A later actual entry can still trigger the persistent field',s5,event('entry4','D',2,actualEmbeddedPieceId='c02'),summary6,{'outcome':'failed','creditedDamage':1})
s7=field_case('FP91-T07','JSON reload retains entry ownership and physical stock',json.loads(json.dumps(s6)),event('entry4','D',2,actualEmbeddedPieceId='c02'),summary6,{'outcome':'duplicate-entry','creditedDamage':0})
case('FP91-T08','Source same-area slows do not add to20',{'existingReduction':10,'newSameAreaReduction':10,'walkingSpeedBefore':30},{'sameAreaReduction':max(10,10),'walkingSpeed':max(0,30-max(10,10))},{'sameAreaReduction':10,'walkingSpeed':20},['trapsetter','EQUIPMENT_ITEM_PROCEDURES#Caltrops'])

def remove_piece(before,target,piece,action_available,receiver):
    s=deepcopy(before)
    if not action_available or not receiver or s['pieces'].get(piece) != 'embedded:'+target: return s,False
    s['pieces'][piece]='container:'+receiver
    s['targets'][target]['embeddedPieces'].remove(piece)
    s['targets'][target]['walkingReduction']=0
    conserve(s);return s,True
s8,removed=remove_piece(s7,'B','c01',True,'B-pouch')
case('FP91-T09','Actual Action removes one embedded piece to a real receiver',{'before':s7,'target':'B','piece':'c01','ActionAvailable':True,'receiver':'B-pouch'}, {'removed':removed,'after':field_summary(s8),'pieceLocation':s8['pieces']['c01']}, {'removed':True,'after':{**summary6,'embeddedCount':1,'collectedCount':1,'targets':{'B':{'hp':9,'movementRemaining':0,'walkingReduction':0,'embeddedPieces':[]},'D':summary6['targets']['D']}},'pieceLocation':'container:B-pouch'}, ['trapsetter','EQUIPMENT_ITEM_PROCEDURES#Caltrops'])
s9,removed2=remove_piece(s8,'B','c01',True,'second-pouch')
case('FP91-T10','Removed piece cannot be recovered twice',{'before':s8,'repeatPiece':'c01'}, {'secondRemoval':removed2,'stateUnchanged':s9==s8}, {'secondRemoval':False,'stateUnchanged':True},['trapsetter'])
def collect(before,collection_id,elapsed,accessible,unoccupied,receiver):
    s=deepcopy(before)
    if collection_id in s['collectionReceipts']:return s,0
    if elapsed<60 or not accessible or not unoccupied or not receiver:return s,0
    actual=[k for k,v in s['pieces'].items() if v==s['fieldId']]
    for key in actual:s['pieces'][key]='container:'+receiver
    s['collectionReceipts'][collection_id]=actual
    s['physicallyCleared']=True;s['armed']=False;s['enhancedAllowanceOccupied']=False
    conserve(s);return s,len(actual)
s10,count=collect(s9,'collection1',60,True,True,'S-bag')
case('FP91-T11','One real minute collects18 remaining pieces, not the embedded or already removed ones',{'before':s9,'activeSeconds':60,'actualUnoccupiedAccessibleSquare':True,'receiver':'S-bag'}, {'count':count,'after':field_summary(s10)}, {'count':18,'after':{**field_summary(s9),'fieldCount':0,'collectedCount':19,'active':False,'allowanceOccupied':False}}, ['trapsetter'],qualification='The supplied safe physical collection covers the actual remaining pieces and clears the square. Coverage is verified as a world premise; no universal nineteen-piece hazard threshold is invented. Quick-placement use remains spent until its own real Short Rest.')
for suffix,args in [('12',('collection1',60,True,True,'other-bag')),('13',('collection2',59,True,True,'S-bag'))]:
    before=s10 if suffix=='12' else s9;after,number=collect(before,*args)
    case('FP91-T'+suffix,'Collection replay/incomplete work cannot mint recovered stock',{'before':before,'arguments':args},{'count':number,'unchanged':after==before},{'count':0,'unchanged':True},['trapsetter'])
case('FP91-T14','Field clearing does not recall a piece still embedded in another creature',{'afterCollection':s10},{'Dpiece':s10['pieces']['c02'],'Dslow':s10['targets']['D']['walkingReduction'],'totalPhysicalPieces':len(s10['pieces'])},{'Dpiece':'embedded:D','Dslow':10,'totalPhysicalPieces':20},['trapsetter'])

def assembly(face,modifier,craftsman=False):
    outcome=task(face,modifier,12)
    return {'activeMinutes':15 if craftsman else 30,'workingPreparedKit':outcome['success'],'expendableConsumed':not outcome['success'],'recoverableFrameRetained':True,'task':outcome}
for suffix,args,expected in [
 ('15',(8,4),{'activeMinutes':30,'workingPreparedKit':True,'expendableConsumed':False,'recoverableFrameRetained':True,'task':{'total':12,'degree':'success','success':True}}),
 ('16',(1,11),{'activeMinutes':30,'workingPreparedKit':False,'expendableConsumed':True,'recoverableFrameRetained':True,'task':{'total':12,'degree':'failure','success':False}}),
 ('17',(20,0),{'activeMinutes':30,'workingPreparedKit':True,'expendableConsumed':False,'recoverableFrameRetained':True,'task':{'total':20,'degree':'critical-success','success':True}}),
 ('18',(8,4,True),{'activeMinutes':15,'workingPreparedKit':True,'expendableConsumed':False,'recoverableFrameRetained':True,'task':{'total':12,'degree':'success','success':True}})]:
    case('FP91-T'+suffix,'Trap assembly retains Core natural shifts and actual parts',{'arguments':args},assembly(*args),expected,['trapsetter','Core tasks','FT84/Q3'],qualification='One genuine authorized kit assembly with suitable owned components, tools and real credential. Success incorporates the parts in that same kit rather than duplicating loose stock. Craftsman applies only where actually acquired. These are source-qualified modifier slices, not claimed full actor builds.')

def snare(armed,actual_entry,save_total,dc,denial_spent,grounded=True):
    triggered=armed and actual_entry and grounded
    return {'triggered':triggered,'discharged':triggered,'stunned':triggered and save_total<dc and not denial_spent,'substituteDamage':0,'hardDenialLedgerSpent':denial_spent or (triggered and save_total<dc and not denial_spent)}
for suffix,args,expected in [('19',(True,True,13,14,False),[True,True,True,0,True]),('20',(True,True,13,14,True),[True,True,False,0,True]),('21',(True,True,14,14,False),[True,True,False,0,False]),('22',(True,True,1,14,False,False),[False,False,False,0,False])]:
    case('FP91-T'+suffix,'Snare discharge and source/target/encounter denial are separate',{'arguments':args},list(snare(*args).values()),expected,['trapsetter','FS-15'],qualification='Actual same source-character/target/encounter identity is retained across replaced trap IDs. Any granted Stunned lasts to the target original next regular end. This diagnostic does not allocate an additional denial event or substitute a damage reward when barred.')

def reaction_move(speed,terrain_cost,available,capable,perceived,distance,trigger_source=True):
    legal=available and capable and perceived and distance<=30 and trigger_source
    budget=F(speed,2) if legal else F(0)
    return {'reactionSpent':legal,'movementCostBudget':str(budget),'possibleFeetOnSuppliedPath':str(budget/terrain_cost),'immuneToTriggererOA':legal,'otherOAImmunity':False}
for suffix,args,expected in [('23',(30,2,True,True,True,20),[True,'15','15/2',True,False]),('25',(30,1,True,False,True,20),[False,'0','0',False,False]),('26',(30,1,True,True,True,31),[False,'0','0',False,False])]:
    case('FP91-T'+suffix,'Trapsetter post-effect Reaction moves only through real legal path',{'arguments':args},list(reaction_move(*args).values()),expected,['trapsetter'],qualification='Voluntary use after a real personally placed trap trigger and its immediate effects. A blocked path or lack of actual cover cannot be fixed by this arithmetic. Other creatures retain their normal opportunity conditions; no automatic attack is created.')
case('FP91-T24','Speed0 permits no displacement',{'currentApplicableSpeed':0}, {'maximumDisplacementFeet':str(F(0,2))}, {'maximumDisplacementFeet':'0'}, ['trapsetter'],qualification='Movement ceiling only. No choice is made about voluntarily spending a Reaction on a zero-distance attempt; this does not authorize motion while restrained.')

# Mounted attack scopes, costs and source ownership; no second mount phase.
def mounted_advantage(kind,target_unmounted,target_smaller,cavalry,mounted_combatant,legally_mounted,disadvantage=False):
    attack=kind in ('melee','ranged')
    sources=int(legally_mounted and attack and target_unmounted and cavalry)+int(legally_mounted and kind=='melee' and target_unmounted and target_smaller and mounted_combatant)
    return {'qualifyingSources':sources,'rollMode':'normal' if bool(sources)==disadvantage else 'advantage' if sources else 'disadvantage','dice':2 if bool(sources)!=disadvantage else 1}
for suffix,args,expect in [('01',('melee',True,True,True,True,True),[2,'advantage',2]),('02',('ranged',True,False,True,True,True),[1,'advantage',2]),('03',('melee',True,False,False,True,True),[0,'normal',1]),('04',('save',True,True,True,True,True),[0,'normal',1]),('05',('melee',True,True,True,True,True,True),[2,'normal',1])]:
    case('FP91-M'+suffix,'Mounted feats retain distinct attack scopes',{'arguments':args},list(mounted_advantage(*args).values()),expect,['cavalry','mounted_combatant','FS-10'],qualification='Actual legally mounted attack-qualification projection only. Target and mount sizes, actual saddle position, perception/range and full offensive source eligibility remain independently required; no mount or attack is granted.')
def mount_cost(speed,remaining,already_used,access=True):
    cost=max(1,speed//2) if speed>0 else None
    return {'costFeet':cost,'allowed':cost is not None and cost<=remaining and not already_used and access,'mountBudgetChanges':False}
for suffix,args,expected in [('06',(31,15,False),[15,True,False]),('07',(1,1,False),[1,True,False]),('08',(0,10,False),[None,False,False]),('09',(30,30,True),[15,False,False]),('10',(30,14,False),[15,False,False])]:
    case('FP91-M'+suffix,'Mount operation uses rider movement and original interval',{'arguments':args},list(mount_cost(*args).values()),expected,['EX58/TR-04','FS-10'],qualification='Reachable fitting seat/free legal landing, actual stable approach, usable hand and non-Prone state supplied. The already-used flag belongs to the original regular-turn interval; an extra turn does not clear it.')
def speeds(existing,derived,riders,immobile=False,burden=False):
    result={k:max(0,v+(10 if riders else 0)) for k,v in existing.items()}
    if burden:result={k:max(0,v-10) for k,v in result.items()}
    if immobile:result={k:0 for k in result}
    for child,parent in derived.items():result[child]=result[parent]
    return result
case('FP91-M11','Two Cavalry riders add one bonus, derived mode follows its parent',{'existingSpeeds':{'walk':40,'swim':20},'derivedClimbEqualsWalk':True,'riders':2,'burden':True},speeds({'walk':40,'swim':20},{'climb':'walk'},2,burden=True),{'walk':40,'swim':20,'climb':40},['cavalry','BODY_EQUIPMENT','FS-10'],qualification='Synthetic already-authorized mount speed relationship for formula ordering, not a created creature/extra locomotion mode. Actual body/capacity/load and the source granting derived climb are external fixture premises. No flying mode or vehicle pace is inferred.')
case('FP91-M12','Speed0 restriction still overrides Cavalry',{'existingWalk':40,'riders':1,'immobile':True},speeds({'walk':40},{},1,immobile=True),{'walk':0},['cavalry'])
case('FP91-M13','Controller change retains original spent slot and companion offense',{'regularRound':1,'mountAlreadyActed':True,'offensiveAllowanceSpent':True,'newController':'other'}, {'anotherRegularTurn':False,'offensiveAllowanceRestored':False,'newLinkedPhaseStartsRound':2,'riderSelfPoweredFeetFromCarriage':0}, {'anotherRegularTurn':False,'offensiveAllowanceRestored':False,'newLinkedPhaseStartsRound':2,'riderSelfPoweredFeetFromCarriage':0},['EX58/TR-03','EX58/TR-06','FS-10'],qualification='Source-adjudicated state boundary, not an executed initiative scheduler or companion native command. Future exact integration must exercise real control changes with the unchanged physical actor and actual original slot.')

# Social checks preserve concrete attainable terms; arithmetic never supplies consent or goods.
def diplomat(cha,wis,pb,persuasion_trained,insight_trained):
    return {'persuasion':cha+pb*(2 if persuasion_trained else 1),'insight':wis+pb*(2 if insight_trained else 1)}
case('FP91-S01','Diplomat snapshots each skill separately',{'CHAmodifier':2,'WISmodifier':3,'PB':3,'priorPersuasion':False,'priorInsight':True},diplomat(2,3,3,False,True),{'persuasion':5,'insight':9},['diplomat'])
case('FP91-S02','Previously trained Persuasion gives Expertise without tripling PB',{'CHAmodifier':2,'WISmodifier':3,'PB':3,'priorPersuasion':True,'priorInsight':True},diplomat(2,3,3,True,True),{'persuasion':8,'insight':9},['diplomat'])
def silver(skill,purposeful,understood):return 2 if skill=='Persuasion' and purposeful and understood else 0
for suffix,args,expected in [('03',('Persuasion',True,True),2),('04',('Deception',True,True),0),('05',('Intimidation',True,True),0),('06',('Persuasion',True,False),0)]:
    case('FP91-S'+suffix,'Silver Tongue applies only to the actual diplomatic Persuasion task',{'arguments':args},silver(*args),expected,['silver_tongue','FS-13'])
def negotiate(faces,modifier,dc,quoted_success_cp,offered_failure_cp):
    result=task(max(faces),modifier,dc)
    return {'keptFace':max(faces),'outcome':result,'agreedCp':quoted_success_cp if result['success'] else offered_failure_cp,'additionalUnprintedDiscount':0}
case('FP91-S07','Negotiator honors the announced45gp quote once',{'actualNormalQuoteCp':5000,'announcedSuccessCp':4500,'faces':[3,12],'modifier':5,'DC':15},negotiate([3,12],5,15,4500,5000),{'keptFace':12,'outcome':{'total':17,'degree':'success','success':True},'agreedCp':4500,'additionalUnprintedDiscount':0},['negotiator','FS-13'])
def merchant(quote_cp,ceiling,direction,success,eligible=True,already_used=False):
    if not eligible or already_used:return {'applicable':False,'exactCp':str(F(quote_cp)),'paidOrReceivedCp':None}
    multiplier=1+(ceiling if direction=='sale' else -ceiling) if success else F(1)
    exact=F(quote_cp)*multiplier
    rounded=exact.numerator//exact.denominator if direction=='sale' else -(-exact.numerator//exact.denominator)
    return {'applicable':True,'exactCp':str(exact),'paidOrReceivedCp':rounded}
for suffix,args,expected in [('08',(10000,F(1,10),'sale',True),[True,'11000',11000]),('09',(10000,F(3,100),'purchase',True),[True,'9700',9700]),('10',(101,F(1,10),'purchase',True),[True,'909/10',91]),('11',(101,F(1,10),'sale',True),[True,'1111/10',111]),('12',(11000,F(1,10),'sale',True,True,True),[False,'11000',None]),('13',(5000,F(1,10),'purchase',True,False),[False,'5000',None])]:
    shown=[str(x) if isinstance(x,F) else x for x in args]
    case('FP91-S'+suffix,'Merchant concession eligibility, family cap and final copper rounding',{'arguments':shown},list(merchant(*args).values()),expected,['merchant_s_guile','FS-13','EX58/FL-21'],qualification='Actual willing ordinary mundane-goods deal with fixed quoted quantity, lawful owner/provider, predeclared attainable ceiling and actual successful task supplied. Ineligible branch represents excluded fixed tariff/service/artifact; repeated branch preserves the existing110gp bill rather than minting another concession. No purchase/resale parity or willing buyer is inferred.')

def appraisal(haven,tier_dc,standalone_dc,face,modifier):
    dc=tier_dc if haven else standalone_dc; outcome=task(face,modifier,dc)
    return {'activeMinutes':30 if haven else 10,'oneCheckDC':dc,'checkCount':1,'outcome':outcome,'referenceCp':4000 if outcome['success'] else None,'actualBuyerQuoteCp':2000,'cashCreatedByKnowledge':0}
for suffix,args,expected in [('14',(False,None,15,10,5),[10,15,1,{'total':15,'degree':'success','success':True},4000,2000,0]),('15',(True,18,15,13,5),[30,18,1,{'total':18,'degree':'success','success':True},4000,2000,0]),('16',(True,18,15,10,5),[30,18,1,{'total':15,'degree':'failure','success':False},None,2000,0])]:
    case('FP91-S'+suffix,'Appraise inside Haven retains30 minutes and governing DC',{'arguments':args,'realItemReferenceCp':4000,'realBuyerQuoteCp':2000},list(appraisal(*args).values()),expected,['appraise','FS-13','EX58/FL-19'],qualification='One actual item/lot with source-set reference and buyer quote, lawful safe inspection and the stated source classification. Identification discloses only the actual complete unprotected operative properties; no missing profile, curse, formula, title or cosmology is authored by this arithmetic.')

def ceil_f(value):return -(-value.numerator//value.denominator)
def settlement(gross_cp,taxes,rq,sponsor):
    # One actual final tax bill and one sponsor payment; monetary amounts are copper.
    tax=ceil_f(F(gross_cp)*max(taxes,default=F(0)))
    base=max(0,gross_cp-tax-rq)
    share=ceil_f(F(base)*sponsor)
    return {'grossCp':gross_cp,'taxCp':tax,'mandatoryRescueQuarantineCp':rq,'sponsorBaseCp':base,'sponsorShareCp':share,'netCp':gross_cp-tax-rq-share}
case('FP91-S17','Highest levy once; actual prior rescue costs reduce sponsor base once',{'grossCp':11000,'applicableLevies':['3/100','5/100'],'actualRQAlreadyPaidCp':1000,'guildShare':'1/5'},settlement(11000,[F(3,100),F(5,100)],1000,F(1,5)),{'grossCp':11000,'taxCp':550,'mandatoryRescueQuarantineCp':1000,'sponsorBaseCp':9450,'sponsorShareCp':1890,'netCp':7560},['EX58/FL-21','EX58/FL-22','FS-13'])
def assay(face_cp,assay_cp,remint_cp,knowing,paid_cp):
    fees=F(assay_cp)+F(remint_cp)
    total=max(F(face_cp,10),fees) if knowing else fees
    fine=total-fees
    rounded=ceil_f(total)
    return {'serviceFeesExactCp':str(fees),'fineExactCp':str(fine),'totalExactCp':str(total),'totalPayableCp':rounded,'priorPaymentCreditCp':min(rounded,paid_cp),'remainingPayableCp':max(0,rounded-paid_cp),'seizurePaymentCreditCp':0}
for suffix,args,expected in [('18',(100000,1000,500,True,1500),['1500','8500','10000',10000,1500,8500,0]),('19',(100,100,0,True,50),['100','0','100',100,50,50,0]),('20',(100000,1000,500,False,0),['1500','0','1500',1500,0,1500,0]),('21',(1001,100,0,True,100),['100','1/10','1001/10',101,100,1,0])]:
    ck('FP91-S'+suffix+' actual assay1% minimum1gp',F(args[1]),max(F(100),F(args[0],100)))
    case('FP91-S'+suffix,'Assay greater-of total allocates fees once and credits actual payments',{'arguments':list(args),'actualAcceptedAssayBillFaceCp':args[0],'actualAcceptedLegitimateRemintValueCp':args[2]*50,'assayRate':'1/100 minimum100cp','remintRate':'1/50'},list(assay(*args).values()),expected,['EX58/FL-25','EX58_EDIT_02','FS-13'],qualification='Actual commissioned bill, legitimate remint service and lawful knowing-holder determination are supplied separately. The fractional example checks a single coherent liability payment and retains the1gp minimum assay fee. Seized false coin is custody evidence, never payment credit; unpayable debt remains owed without automatic borrowing.')

def standing(opening,events):
    unique={}
    for eid,cause,delta in events:
        if eid not in unique and cause not in [x[0] for x in unique.values()]:unique[eid]=(cause,delta)
    signed=sum(x[1] for x in unique.values());bounded=max(-2,min(2,signed));final=max(-3,min(3,opening+bounded))
    return {'signedSum':signed,'sceneBoundedChange':bounded,'sceneOverflow':signed-bounded,'finalStanding':final,'appliedFromOpening':final-opening,'scaleOverflow':opening+bounded-final,'recordCount':len(unique)}
for suffix,events,expected in [('22',[('e1','first',2)],[2,2,0,3,1,1,1]),('23',[('e1','first',2),('e2','second',-2)],[0,0,0,2,0,0,2]),('24',[('e1','first',2),('e1','first',2),('new-id','first',2)],[2,2,0,3,1,1,1])]:
    case('FP91-S'+suffix,'Standing recomputes from original scene score and real distinct causes',{'opening':2,'events':events},list(standing(2,events).values()),expected,['EX58/RP-A06','FS-13'],qualification='Eligible actual signed consequences for one real institution/subject/scene and current version. This isolated arithmetic does not authenticate witnesses, actual cause equivalence or establish a new reputation event. An alternate delivery ID does not make the same cause distinct.')

cp=j(A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_ACCEPTANCE_90.json')
for binding in [cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]:
    ck('Canonical baseline preserved: '+binding['path'],info(G/binding['path']),binding)
for binding in bindings:ck('Full source unchanged during diagnostic: '+binding['path'],info(G/binding['path']),binding)

report={'id':'FEAT335-PHYSICAL-SOCIAL-COMPOSITIONS-91','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'BOUNDED_SOURCE_QUALIFIED_DIAGNOSTICS_COMPLETE_PARENT335_PENDING',
        'sourceBindings':bindings,'fullSelectedFeatRecords':selected,
        'fullSelectedSharedRules':{k:shared[k] for k in ('FS-03','FS-05','FS-10','FS-13','FS-15')},
        'fullRelevantEquipmentRecords':{k:equipment[k] for k in ('adventuring-gear.caltrops-bag-of-20','adventuring-gear.lock','tools.thieves-tools')},
        'cases':cases,'caseCount':len(cases),'completeCaltropSequenceStates':field_states,
        'finalCaltropPhysicalState':s10,'checks':checks,'passed':len(checks),'failed':0,
        'coverage':['Lock source Actions/DC, Burglar PB/Expertise, distinct feat bonuses, Lock Savant numerical trap margin and independent trigger.',
                    'Trap Sense accessible clues, passive numbers without a natural die, actual sight-dependent binary saves.',
                    'Caltrop full physical piece ownership across successful/failed/replayed/new entries, actual Action removal and safe timed collection. No20-piece refill or remote clearing.',
                    'Trap kit assembly natural shifts, accepted scoped Craftsman time, snare discharge/denial ledger, post-effect Reaction movement.',
                    'Mounted feat attack scopes, actual original mount/dismount allowance, Cavalry mode derivation/order and preserved phase ownership.',
                    'Skill acquisition snapshots, purposeful understood persuasion, real announced quotes, actual Merchant ceiling and family cap.',
                    'Haven Appraise keeps full30-minute procedure/one governing check; reference value versus offer.',
                    'Single highest levy, sponsor base, greater-of assay fees/fine allocation, previous payments and standing scene recomputation.'],
        'remainingScope':['Actual independent full660-original-plus28-FA casebook review and parent335 exact submission remain open.',
                          'Complete actor acquisition snapshots, world providers, physical coverage/body defenses, locks/traps native machinery and initiative/companion scheduler are not executed here.',
                          'FP91-M13 is source-adjudicated rather than executed scheduler behavior; expected prose values are not counted as runtime verification.',
                          'Real counterpart response, actor comprehension, property/cursed-item disclosure and actual market/title/liability decisions need their full source-qualified world event.',
                          'All physical/social source relationships and original worked cases remain preserved; these diagnostics supplement rather than replace them.',
                          'Plant/copy/world commands, ranged breath/self-eligible clauses and remaining mixed native healing interactions still require their later bounded review.',
                          'Full gadget activation profiles and all prior335 holds remain.'],
        'newRuleAdoptions':0,'canonicalImplementationApplied':False,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'humanPlaytests':0,
        'balanceApproval':False,'cosmologyDecisions':0,'wholeGameComplete':False,'parent335Accepted':False,'sourceInformationDeleted':0,
        'appliedCountsUnchanged':[525,323,249,173],'acceptedButUnappliedUnchanged':53}

ROOT.mkdir()
for source in paths:
    dest=ROOT/'sources'/source.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(source.read_bytes())
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
report['independentDiagnosticScript']=info(SAVED)
payload=enc(report)
with OUT.open('xb') as f:f.write(payload)
with (ROOT/'DIAGNOSTICS.json').open('xb') as f:f.write(payload)
with (ROOT/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
readme='''FEAT335 physical/social review91. Read DIAGNOSTICS.json and complete bound sources. All11 selected feat records and original worked cases are retained. The authored case calculations are independent local standard-library diagnostics, not the production game engine. Actual acquisition/world premises remain explicit. Parent335 is unaccepted; canonical integration, balance/human/cosmology/release are not granted. No supplied code needs execution. These cases supplement every earlier original/FA case and prior evidence. The current FT84 scoped accepted work successors govern their named time compositions; old proposal labels remain historical. No deletion or publication requested.\n'''
with (ROOT/'README.txt').open('xb') as f:f.write(readme.encode())
files=sorted(p for p in ROOT.rglob('*') if p.is_file())
manifest={'id':'FEAT335-PHYSICAL-SOCIAL-91-MANIFEST','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
with (ROOT/'MANIFEST.json').open('xb') as f:f.write(enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
    for row in manifest['files']:
        raw=z.read(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'caseCount':len(cases),'passed':len(checks),'failed':0,'fullSources':len(paths),'archiveMembers':len(manifest['files'])+1},indent=2))
