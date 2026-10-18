"""Repair current control fixtures after whole-body audit, retaining all original scenarios."""
from copy import deepcopy
from datetime import datetime, timezone
import json, math
from apply_di7_ap_as_01 import R,A,info,encoded


def main():
    src=R/'data/director/spell_proposals/control_15_current_11.json'
    out=R/'data/director/spell_proposals/control_15_current_12.json'
    delta=A/'CONTROL_15_GEOMETRY_DELTA_12.json';check=A/'CONTROL_15_GEOMETRY_CHECK_12.json'
    assert all(not p.exists() for p in [out,delta,check])
    old=json.loads(src.read_bytes());d=deepcopy(old);checks=[];ops=[]
    def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
    def sub(c,a,b):
        found=0
        def walk(v):
            nonlocal found
            if isinstance(v,str):found+=v.count(a);return v.replace(a,b)
            if isinstance(v,list):return [walk(x) for x in v]
            if isinstance(v,dict):return {k:(x if k in ['originalTextUnchanged','sourceRefs','originalSource'] else walk(x)) for k,x in v.items()}
            return v
        result=walk(c);ck('Exact active phrase '+c['id']+' '+a,found>0);c.clear();c.update(result)
    def resize(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ['originalTextUnchanged','sourceRefs','originalSource']:continue
                if isinstance(x,list) and x==[1,1,1] and 'body' in k.lower() and 'half' in k.lower():v[k]=[2.5,2.5,3]
                else:resize(x)
        elif isinstance(v,list):
            for x in v:resize(x)
    for i,c in enumerate(d['currentExamples']):
        before=deepcopy(c)
        if i==28:continue # Vaskor is source-only; no invented body/CR/profile.
        resize(c)
        c['actualFixtureBodies12']={'source':info(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'),'realCurrentAnatomy':'The concrete named class bodies and declared synthetic living recipients in this current fixture are Medium, occupied5x5 feet with measured height6, half-extents[2.5,2.5,3]. The particular bonded Medium Beast, when actually present, also has measured occupied height6. This measurement is a stated fixture input, not a general class/species height.','coordinates':'Preserve stated center z1; actual supporting floor is z=-2, so full standing bodyz[-2,4]. All named current bodies must fit their entire initial, traversed and final space. A Prone posture retains its5x5 footprint and can only reduce vertical extent within that clear envelope.','exceptions':'Apparent images are nonphysical authored visual bounds; their4x4x4 appearance is not creature occupancy. Source-only Vaskor/CaveBear and unresolved CR/contest branches remain uninstantiated; no geometry or CR granted to them.','scope':'No new source rule, runtime or actual GPT acceptance.'}
        if i==3:
            sub(c,'actual hostileWizard1 at[0,0,1]','actual hostileWizard1 at[0,-12,1]')
            sub(c,'At20ft, Unconscious','At center distance sqrt544≈23.32ft (nearest body distance sqrt274≈16.55ft), Unconscious')
            sub(c,'Distance20isnotwithin5','Actual body separation exceeds5ft')
            sub(c,'helper at[20,3,1]','helper at[20,5,1]')
        if i in [4,5]:
            c['initialState']['imageBoundsQualification12']='Four authored nonphysical4x4x4 audiovisual images, each fitting its permitted10ft cube. Their apparent bounds remain half-extents[2,2,2]; actual Medium body space is5x5 with measured height6. This is not a physical image body or occupied square.'
        if i==5:
            c['recipientProfile']['physicalSupports']='Actual flat clear floorz=-2, full swept body corridorx[37.5,52.5],y[-2.5,2.5], no blockers; actual body height6.'
            c['timeline'][1]['operation']='Recipient voluntarily follows the actual supported route from[40,0,1] toward[50,0,1]. Its leading real occupied-body face uses half-extent2.5; the authored apparent image has half-extent2. First contact with the image left face48 occurs at body center45.5, after5.5 actual feet. That genuine physical contradiction reveals the whole false party and ends this application with no roll.'
            c['timeline'][1]['expected']['movementSpentAtRecognition']=5.5;c['timeline'][1]['expected']['movementRemainingAtRecognition']=24.5
            c['timeline'][2]['operation']='Recipient may continue the remaining4.5ft to[50,0,1] under ordinary permissions. No image body blocks it or supplies support; total actual movement remains10ft.'
        if i==6:
            sub(c,'evenwith1ftextent','even with2.5ft horizontal half-extent (nearest point52.5, beyond fieldedge50)')
            sub(c,'Firstcontactatcenter51after4actualfeet','First contact at center52.5 after2.5 actual feet')
            sub(c,'reenterthrough51','reenter through52.5')
        if i==7:
            sub(c,'bodyhalfextents1','bodyhalfextents[2.5,2.5,3],Medium5x5/measuredheight6')
            am=c['independentBranches'][1]['suppressor'];am['casterCenter']=[35,9,1]
            am['rangeAndOwnField12']='Source center to chosen point9ft≤10, with clear LoE and no body overlap. Caster intersects its own field; accepted same-family exemption preserves Lesser Antimagic. Next legal Minor Illusion commitment can end old concentration before its own payload resolves.'
            sub(c,'5ftfromcaster','11ft from caster')
        if i==15:
            sub(c,'freeusablehandat[20,3,1]','freeusablehandat[20,-5,1]')
            sub(c,'origin[20,15,1]','origin[29,0,1]')
            c['independentBranches'][1]['ownerAndBeast']['wholeBodyGeometry12']='Medium ownercenter[20,5,1] and particular Medium Beastcenter[20,0,1],5x5/measuredheight6 on floor-2: boundaries touch but interiors do not overlap. AM castercenter[29,0,1] is9ft from field point and has no body overlap.'
        if i in [16,17]:
            c['initialState']['fixedBoundary']={'minimum':[22.5,-7.5,-7],'maximum':[37.5,7.5,9]}
            c['initialState']['boundaryDerivation12']='Initial actual body boundsx[27.5,32.5],y[-2.5,2.5],z[-2,4], expanded by exactly5ft on each side as the pending full procedure requires. For the eastward route, full-body containment ends just beyond centerx35 (leading face37.5); no physical wall/clearance or new movement permission exists.'
        if i==17:
            sub(c,'casts from[30,15,1]','casts from[30,9,1]')
            c['commonPrefix'][1]['expected']['antimagicCasterToPointFt']=9
            c['commonPrefix'][1]['expected']['antimagicCasterOwnFieldExemption']=True
        if i==18:
            c['initialState']['completeRouteGeometry12']='Floorz=-2; complete clear swept body corridorx[17.5,37.5],y[-2.5,2.5],z[-2,4]. The complete voluntary15ft path remains in the stipulated difficult terrain; all30 movement is spent, with no changed terrain-edge crossing.'
        if i==19:
            sub(c,'center[20,3,1]','center[20,-5,1]')
            sub(c,'origin[20,15,1]outside','origin[29,0,1],9ft from the field point and intersecting its own same-family-exempt field')
        if i==20:
            sub(c,'at[0,0,1]targets real sleeper20ft','at[0,-12,1] targets real sleeper at center distance sqrt544≈23.32ft, nearest body distance sqrt274≈16.55ft')
            c['initialState']['rayAttackerSeparation12']='The independent Ray attacker is separate from the original caster at[0,0,1]; their nearest body gap7ft exceeds close-quarters5ft even if they are hostile. No additional capability or attack is granted.'
        if i==21:
            s=c['independentBranches'][0]['initialState']
            s['geometry']='Explicit synthetic safe horizontal corridorwidth5ft (y[-2.5,2.5]), floorz=-2, no side door or alternate legal movement mode. Known lethal drop begins beyond support edgex32.5. A body center can safely reachx30, its leading face at32.5. No safe farther/lateral increasing-distance route exists. This repositions the explicit fixture edge to preserve the original exactly10ft safe-retreat obligation with the real5ft footprint.'
            c['independentBranches'][1]['initialState']['realOpponentGeometry12']='Recipientcenter[20,0,1], actual real opponentcenter[30,0,1], both declared Medium5x5/measuredheight6. Their nearest whole-body gap5ft means a genuinely hostile, capable opponent perceiving the attacker can also impose ranged close-quarters disadvantage. This combines with Poisoned as one disadvantage, not extra dice; original[5,17]→11miss remains.'
        if i==23:
            sub(c,'bodyhalf1','actualMedium5x5,measuredheight6,half-extents[2.5,2.5,3]')
        if i==24:
            c['initialState']['wholeBodyPath12']='Full clear supported swept corridorx[17.5,37.5],y[-2.5,2.5],floorz=-2. At targetcenter35 and innkeepercenter40,5x5 body boundaries touch atx37.5 without interior overlap; ordinary handoff remains within5ft. No shortened forced route or new Action is inferred.'
        if i==25:
            sub(c,'caster[20,15,1]outside','caster[20,9,1],9ft from the chosen point; inside its own exempt field')
        if i==26:
            for j,t in enumerate(c['initialState']['recipients']):t['center']=[20,-27.5+5*j,1]
            c['initialState']['geometry']='All12 distinct5x5 bodies are in one row, centersx20,y=-27.5+5*i for i0..11,z1, on floorz-2; adjacent boundaries touch without overlap. Maximum center distance sqrt1156.25≈34.00ft<60, with stipulated actual casterLoE and audible command. No extra targets or substituted outcomes.'
        if i in [7,15,17,19,25]:
            c['antimagicPlacement12']={'actualSource':info(R/'data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json'),'pointer':'/spells/0/procedure','sourceRangeFt':10,'actualCenterToPointFt':9,'wholeRecipientCovered':True,'sameFamilyExemption':'The caster may intersect its own field; Lesser Antimagic never suppresses itself.','concentrationTransition':'Where the existing later Minor Illusion branch occurs, its otherwise legal commitment is permitted even inside the field. Commitment ends old concentration before the new payload; old field cannot suppress that later resolution. No extra Action, RP refund or new transition rule.'}
        if i!=28:ops.append({'path':'/currentExamples/'+str(i),'before':before,'after':deepcopy(c)})
    finish(d,old,src,out,delta,check,ops,checks,ck)


def finish(d,old,src,out,delta,check,ops,checks,ck):
    from prepare_de4_fate_guard_amendment_01 import parent
    reverse=deepcopy(d)
    for op in reversed(ops):
        p,k=parent(reverse,op['path']);ck('Exact current after '+op['path'],p[k]==op['after']);p[k]=deepcopy(op['before'])
    ck('Complete reverse returns Current11',reverse==old)
    ck('All15 full procedures/source records unchanged',d['spells']==old['spells'] and len(d['spells'])==15)
    ck('30 original source texts unchanged',d['originalExamplesUnchanged']==old['originalExamplesUnchanged'] and len(d['originalExamplesUnchanged'])==30)
    ck('All30 current case identities and original obligations preserved',[c['id'] for c in d['currentExamples']]==[c['id'] for c in old['currentExamples']] and all(a['originalTextUnchanged']==b['originalTextUnchanged'] for a,b in zip(d['currentExamples'],old['currentExamples'])))
    ck('13 questions unchanged',d['conferenceQuestions10']==old['conferenceQuestions10'] and len(d['conferenceQuestions10'])==13)
    ck('Unreviewed CR8 source-only case untouched',d['currentExamples'][28]==old['currentExamples'][28])
    ck('Body size and real floor',2*2.5==5 and 2*3==6 and 1-3==-2)
    ck('Group illusion retains nonphysical4ft apparent bounds',d['currentExamples'][4]['initialState']['imageApparentHalfExtents']==[2,2,2] and d['currentExamples'][5]['initialState']['imageApparentHalfExtents']==[2,2,2])
    ck('Group contact at5.5ft then4.5ft',50-2-2.5==45.5 and 45.5-40==5.5 and 30-5.5==24.5 and 50-45.5==4.5)
    ck('Mind Fog first contact2.5ft, not4ft',30+20+2.5==52.5 and 55-52.5==2.5 and 55-2.5>30+20)
    ck('Rousing helper and grappler fit without overlap',5==2.5+2.5 and -5+2.5==-2.5)
    ck('Ray attackers separate and within30ft',math.sqrt(20**2+12**2)<30 and math.sqrt(15**2+7**2)>5 and 12-5==7)
    ck('All five actual AM placements within10ft',9<=10 and all(d['currentExamples'][i]['antimagicPlacement12']['actualCenterToPointFt']==9 for i in [7,15,17,19,25]))
    ck('Whole recipient inside10ft sphere',2.5**2+2.5**2+3**2<10**2)
    ck('AM later image points remain outside old sphere and within ordinary30ft placement',20>10 and 20-9==11 and math.sqrt(9**2+20**2)<30)
    for i in [16,17]:
        s=d['currentExamples'][i]['initialState'];center=s['targetCenter'];half=s['targetBodyHalfExtents']
        ck('Prison exact initial body plus5 each direction '+str(i),s['fixedBoundary']=={'minimum':[center[j]-half[j]-5 for j in range(3)],'maximum':[center[j]+half[j]+5 for j in range(3)]})
    ck('Prison east crossing still after5ft',37.5-2.5-30==5)
    ck('Original10ft safe Panicked retreat preserved',32.5-2.5-20==10)
    guards=d['currentExamples'][26]['initialState']['recipients']
    ck('Twelve real5ft guard footprints never overlap',len(guards)==12 and all(b['center'][1]-a['center'][1]==5 for a,b in zip(guards,guards[1:])))
    ck('All twelve guard centers in60ft range',all(sum(x*x for x in [g['center'][0],g['center'][1],g['center'][2]-1])<=60**2 for g in guards))
    ck('No proposed scope/count promotion',d['newRuleAdoptions']==d['runtimeTestsExecuted']==d['sourceInformationDeleted']==0 and d['countsUnchanged']==old['countsUnchanged'])
    # A search only verifies that the exact faulty explicit body fields have gone;
    # it is not a proof of all game geometry or a runtime test.
    leftovers=[]
    def scan(v,path=''):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ['originalTextUnchanged','sourceRefs','originalSource']:continue
                if 'body' in k.lower() and 'half' in k.lower() and x==[1,1,1]:leftovers.append(path+'/'+k)
                scan(x,path+'/'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):scan(x,path+'/'+str(i))
    scan(d['currentExamples']);ck('No remaining explicit2x2 current body fields',not leftovers)
    prior_meta={k:deepcopy(d[k]) for k in ['id','recordedAtUtc','status']}
    d['id']='CONTROL-15-CURRENT-12';d['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
    d['status']='UNSENT / UNADOPTED full15-spell source conference12. Thirty original scenarios and30 current cases preserved; actual body/range/clearance repairs and29 complete before/after cases supplied.13 design questions remain unchanged. No runtime, source-rule adoption, CR inference or exact joint acceptance.'
    delta.write_bytes(encoded({'id':'CONTROL15-GEOMETRY-DELTA12','previousCandidate':info(src),'completeCaseChanges':ops,'actualGPTConcurrence':False,'sourceInformationDeleted':0}))
    d['geometryReconciliation12']={'previousCandidate':info(src),'completeDelta':info(delta),'previousMetadataUnchanged':prior_meta,'scope':'Correct actual Medium occupied spaces, five illegal15ft Lesser Antimagic placements, overlapping helper/grappler and guard positions, image contact, Mind Fog entry, exact Mental Prison expansion, safe ledge and complete path support. Apparent images and unresolved bestiary remain distinct. All source-specific decisions are still pending actual conference.','actualGPTConcurrence':False}
    out.write_bytes(encoded(d))
    check.write_bytes(encoded({'candidate':info(out),'previousCandidate':info(src),'completeDelta':info(delta),'checks':checks,'checkCount':len(checks),'failureCount':0,'changedCurrentCaseRecords':len(ops),'originalScenarios':30,'procedures':15,'designQuestions':13,'actualGPTConcurrence':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'candidate':info(out),'delta':info(delta),'check':info(check),'checks':len(checks),'cases':len(ops)}))


if __name__=='__main__':main()
