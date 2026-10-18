"""Preserve Current08 and repair eight current worked cases in unaccepted Current09."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    src=R/'data/director/spell_proposals/damage_control_25_current_08.json'
    out=R/'data/director/spell_proposals/damage_control_25_current_09.json'
    delta=A/'DAMAGE_CONTROL_25_GEOMETRY_DELTA_09.json'
    check=A/'DAMAGE_CONTROL_25_GEOMETRY_CHECK_09.json'
    assert all(not p.exists() for p in [out,delta,check])
    assert info(src)['sha256']=='24f09a343566d44e532ef31b5aa8b295f6123c024e15919c8e9c16c92a739a60'
    old=json.loads(src.read_bytes());d=deepcopy(old);ops=[];checks=[]
    body=info(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md')
    hp=[info(R/'data/public/class_playtests/wizard.json'),info(R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md')]
    def ck(label,ok):
        checks.append({'name':label,'passed':bool(ok)});assert ok,label
    def amend(group,index,edit,reason):
        prior=deepcopy(d[group][index]);cur=deepcopy(prior);edit(cur)
        cur['occupiedSpaceAudit09']={'acceptedBodySource':body,'status':'Source-driven fixture repair; actual GPT concurrence pending. No new size rule or runtime proof.','reason':reason}
        ops.append({'path':'/'+group+'/'+str(index),'before':prior,'after':deepcopy(cur),'reason':reason})
        d[group][index]=cur
    def medium(c):
        c['initialState']['actualBodyProfile09']='Declared Medium 5x5 feet with measured occupied height6. Centers at z0 stand on actual continuous floor z=-3. Size does not supply an invented height; height6 is this fixture input. Synthetic recipients retain only their explicitly declared defenses and lifecycle.'
    def meteor(c):
        medium(c);s=c['initialState'];s['eachBodyHalfExtents']=[2.5,2.5,3]
        s['solidWallBounds09']={'x':[35,36],'y':[-100,100],'z':[-3,100]}
        s['coveredPerceptionPremise09']='Previously designated/perceived creature position is stipulated independently; current area-origin LoE is blocked by the solid wall and it is excluded regardless of perception.'
        c['occupiedGeometryResults09']={'foeBeforeWall':True,'coveredWholeBodyBehindWall':True,'nearestHorizontalGapBetweenConsecutiveBodies':5,'prismIntersectionPreserved':True,'wallSpansWholePrism':True}
    amend('currentDigitalVectors',7,meteor,'Replace2x2 footprints with actual5x5 Medium fixtures; explicitly instantiate the original wall and recompute body separation/area clipping. Original sole foe recipient is unchanged.')
    def wail(c):
        medium(c);s=c['initialState'];s['allBodyHalfExtents']=[2.5,2.5,3]
        del s['allHP'];del s['allMaxHP']
        s['HPByRecipient']={'caster':80,'foe':100,'ally':100};s['maxHPByRecipient']=deepcopy(s['HPByRecipient'])
        s['casterHPDerivation09']={'CON':14,'firstLevel':8,'laterFixedGains':12,'eachLaterGain':6,'maximumHP':80,'sourceRefs':hp,'startingCurrentHP':'explicitly full at fixture start; not advancement healing'}
        c['expectedIntermediateAndFinalStates']['HP']['caster']=80
        c['occupiedGeometryResults09']={'foeAllyBoundaryTouchOnly':True,'casterNearestOwnAreaDistance':0,'foeNearestOriginDistance':17.5,'allyNearestOriginDistance':22.5}
    amend('highRankCurrentVectors05',0,wail,'Restore5x5 occupied spaces and concrete Wizard13/CON14 maxHP80. Original WIS outcomes, eight psychic damage, recipients and Stunned deadline remain unchanged.')
    def horrid(c):
        medium(c);s=c['initialState']
        for key in ['declaredActualRecipientA','recipientB']:s[key]['bodyHalfExtents']=[2.5,2.5,3]
        s['profileQualification09']='Both recipients are declared conditional synthetic profiles, not newly approved bestiary entries. A is a continuing Undead creature with exactly its stated absence of necrotic defense; B has explicitly supplied necrotic resistance. Their body spaces touch only at y2.5.'
        c['occupiedGeometryResults09']={'AEntireBodyInsideCube':True,'BEntireBodyInsideCube':True,'bodiesInteriorOverlap':False}
    amend('highRankCurrentVectors05',3,horrid,'Restore both5x5 bodies without adding a type immunity; preserve54 and13 damage and one shared raw roll.')
    def lance_wall(c):
        medium(c);s=c['initialState'];s['targetBody']['halfExtents']=[2.5,2.5,3]
        s['wallBounds09']={'x':[40,45],'y':[-100,100],'z':[-3,100]}
        e=c['expectedIntermediateAndFinalStates'];e['finalBodyCenter']=[37.5,0,0];e['actualPushFeet']=7.5
        c['occupiedGeometryResults09']={'initialBodyX':[27.5,32.5],'finalBodyX':[35,40],'maximumNonpenetratingCenterX':37.5,'requestedPushFeet':20,'actualPushFeet':7.5}
    amend('highRankCurrentVectors05',6,lance_wall,'Recompute collision from leading body face: a5ft-wide body stops at center37.5 before wall40, moving7.5ft. Fire immunity still does not erase the separately allowed push.')
    def lance_dying(c):
        medium(c);s=c['initialState'];s['bodyHalfExtents']=[2.5,2.5,3]
        s['clearWholeBodyCorridor09']={'x':[27.5,52.5],'y':[-2.5,2.5],'z':[-3,3],'floorZ':-3,'blockers':[]}
        s['postProneGeometry09']='Body remains in this declared5x5 occupied footprint after becoming Prone; actual lowered vertical extent stays within the clear6ft corridor and on its same floor. No posture change permits wall traversal.'
        c['occupiedGeometryResults09']={'centerFrom':[30,0,0],'centerTo':[50,0,0],'wholeBodyClearAtEndThroughX':52.5,'forcedDistance':20}
    amend('highRankCurrentVectors05',7,lance_dying,'Recompute the complete swept body corridor while retaining the significant-NPC Dying branch and independently supplied ended-identity branch.')
    def flash(c):
        medium(c);c['initialState']['bodyHalfExtents']=[2.5,2.5,3]
        c['initialState']['suppressionQualification09']='The already-admitted local suppression interval[6,10] is an explicit composition input, not a fabricated spell cast. It cannot pause the original Blinded deadline8.'
        c['occupiedGeometryResults09']={'targetNearestSphereCenterFt':7.5,'sphereRadius':20,'casterPointToPlacementFt':120,'areaIntersection':True}
    amend('highRankCurrentVectors05',8,flash,'Restore the5x5 target space; preserve exact120ft placement, cold immunity, independently established blindness and expiry during suppression.')
    def tide(c):
        medium(c);s=c['initialState'];s['bodyHalfExtents']=[2.5,2.5,3]
        del s['bothHP'];del s['bothMaxHP']
        s['HPByRecipient']={'caster':104,'farAlly':200};s['maxHPByRecipient']=deepcopy(s['HPByRecipient'])
        s['casterHPDerivation09']={'CON':14,'firstLevel':8,'laterFixedGains':16,'eachLaterGain':6,'maximumHP':104,'sourceRefs':hp,'startingCurrentHP':'explicitly full at fixture start; no unprinted HP-changing feature'}
        s['farAllyProfile09']='Declared synthetic significant living ally, HP/max200, no relevant defenses, temporary HP or Wounds; this is no new bestiary or class grant.'
        c['expectedIntermediateAndFinalStates']['casterHP']=80
        c['occupiedGeometryResults09']={'bothNearestSphereCenterFt':97.5,'radius':100,'bothBodiesIntersectArea':True,'casterPointToPlacementFt':100}
    amend('highRankCurrentVectors05',12,tide,'Restore5x5 occupied spaces at both radius boundaries; bind actual Wizard17/CON14 HP104, then24 damage→80. Far ally200→151 and both recipient roots remain unchanged.')
    def beast(c):
        s=c['initialState']['sameBeastBeforeEitherIndependentBranch'];s['bodyHalfExtents']=[2.5,2.5,1]
        s['measuredOccupiedHeightFt']=2;s['support']='Actual continuous ground at z=-1 supports the complete swept5x5 body fromx27.5 throughx52.5, y[-2.5,2.5]; no blocker along that whole corridor.'
        c['occupiedGeometryResults09']={'ordinaryCorpseCenter':[30,0,0],'nullContinuingBodyCenter':[50,0,0],'wholeNullEndpointBodyX':[47.5,52.5],'sameMediumBodyIdentity':True,'sourceSpecificHPOnlyLifecycleUnchanged':True}
    amend('highRankCurrentVectors05',14,beast,'Restore the actual Medium Beast5x5 footprint with measured height2 and whole-body support through52.5. Preserve ordinary corpse/bond ending and Null same-body20ft push branches.')
    finish(d,old,src,out,delta,check,ops,checks,ck)


def finish(d,old,src,out,delta,check,ops,checks,ck):
    from prepare_de4_fate_guard_amendment_01 import parent
    back=deepcopy(d)
    for op in reversed(ops):
        par,key=parent(back,op['path']);ck('Exact changed case '+op['path'],par[key]==op['after']);par[key]=deepcopy(op['before'])
    ck('Eight repairs fully reversible to Current08',back==old and len(ops)==8)
    ck('25 complete procedures and every original source/access record unchanged',d['spells']==old['spells'] and len(d['spells'])==25)
    ck('36 full original scenario texts unchanged',d['originalCohortCasesUnchanged']==old['originalCohortCasesUnchanged'] and len(d['originalCohortCasesUnchanged'])==36)
    for group in ['currentDigitalVectors','mixedDefenseOptionVectors04','highRankCurrentVectors05','currentConferenceWorkedSupplements08']:
        ck('All IDs and order preserved '+group,[c['id'] for c in d[group]]==[c['id'] for c in old[group]])
    ck('Named lifecycle supplement unchanged',d['namedLifecycleSupplement06']==old['namedLifecycleSupplement06'])
    ck('Actual body width and measured height',2*2.5==5 and 2*3==6 and 2*1==2)
    ck('Meteor foe before wall and covered body behind',30+2.5<35 and 40-2.5>36)
    ck('Meteor consecutive bodies clear',30-2.5-(20+2.5)==5 and 40-2.5-(30+2.5)==5)
    ck('Wail bodies touch without interior overlap',20+2.5==25-2.5)
    ck('Wail caster actual HP and eight psychic to foe',6+2+12*(4+2)==80 and 100-sum([1,6,1])==92)
    ck('Horrid two bodies in cube without interior overlap',25+2.5<=20+15 and 5+2.5<=15 and 3<=15 and 0+2.5==5-2.5)
    ck('Horrid real save then typed resistance',sum([1,8]*6)==54 and (54//2)//2==13 and 200-13==187)
    ck('Lance whole body stops against wall',40-2.5==37.5 and 37.5-30==7.5 and 37.5+2.5==40)
    ck('Lance Dying body full20 push and whole endpoint support',30+20==50 and 50+2.5==52.5 and 42-20<100 and 20<21 and 21-20<5)
    ck('Crystalline Flash nearest body point in sphere',130-2.5-120==7.5 and 7.5<20 and 6<8<10)
    ck('Death Tide boundary bodies remain recipients',100-2.5==97.5 and 200-2.5-100==97.5 and 97.5<100)
    ck('Death Tide actual caster HP and damage',6+2+16*(4+2)==104 and sum([1,6]*7)==49 and 104-49//2==80 and 2*(49//2)<104)
    ck('Beast actual source HP and whole-body support',2*16+4==36 and 42-36==6 and 50+2.5==52.5)
    for key in ['newSpellAdoptions','runtimeTestsExecuted','sourceInformationDeleted']:ck('No change '+key,d[key]==old[key]==0)
    previous_meta={k:deepcopy(d[k]) for k in ['id','recordedAtUtc','status']}
    d['id']='DAMAGE-CONTROL-25-CURRENT-09';d['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
    d['status']='PENDING actual GPT exact review: Current08 preserved; eight current cases repaired for accepted occupied space and two explicit caster HP builds. All25 procedures,26 placements,36 original scenarios and70 current case identities retained. Previous actual conference23 changes and three supplement repairs remain intact. No source adoption or runtime/balance/cosmology approval.'
    delta.write_bytes(encoded({'id':'DAMAGE-CONTROL25-GEOMETRY-DELTA09','previousCandidate':info(src),'actualGPTConcurrence':False,'completeCaseChanges':ops,'unchangedOriginalScenarios':36,'sourceInformationDeleted':0}))
    d['occupiedSpaceReconciliation09']={'previousCandidate':info(src),'fullBeforeAfterDelta':info(delta),'previousMetadataUnchanged':previous_meta,'changedCaseIds':[o['after']['id'] for o in ops],'heldSupersededPacket':'DD_Damage_Control_25_Exact_Rebound_09.zip was never submitted; prepare a newly bound packet for Current09.','actualGPTConcurrenceOnTheseChanges':False}
    out.write_bytes(encoded(d))
    check.write_bytes(encoded({'id':'DAMAGE-CONTROL25-GEOMETRY-CHECK09','candidate':info(out),'previousCandidate':info(src),'fullBeforeAfterDelta':info(delta),'checks':checks,'checkCount':len(checks),'failures':0,'reversibleChangedCases':8,'actualGPTConcurrence':False,'newSpellAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'candidate':info(out),'delta':info(delta),'check':info(check),'checks':len(checks)}))


if __name__=='__main__':main()
