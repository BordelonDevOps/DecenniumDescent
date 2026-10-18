"""Rebind four conditional terrain cases to actual occupied space; all design forks remain open."""
from copy import deepcopy
from datetime import datetime, timezone
import json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_de4_fate_guard_amendment_01 import parent


def main():
    src=R/'data/director/spell_review/material_terrain_8_conference_01.json'
    out=R/'data/director/spell_review/material_terrain_8_conference_02.json'
    oldroot=A/'material-terrain8-conference-01';root=A/'material-terrain8-conference-02'
    delta=A/'MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02.json';zp=A/'DD_Material_Terrain_8_Conference_02.zip'
    prep=A/'MATERIAL_TERRAIN_8_CONFERENCE_02_PREPARATION.json';req=A/'MATERIAL_TERRAIN_8_CONFERENCE_02_REQUEST.txt'
    assert all(not p.exists() for p in [out,root,delta,zp,prep,req])
    old=json.loads(src.read_bytes());d=deepcopy(old);ops=[];checks=[]
    def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
    def edit(i,fn,why):
        before=deepcopy(d['conditionalConferenceVectors'][i]);after=deepcopy(before);fn(after)
        after['occupiedSpaceCorrection02']={'acceptedSource':info(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'),'reason':why,'actualGPTConcurrence':False}
        d['conditionalConferenceVectors'][i]=after;ops.append({'path':'/conditionalConferenceVectors/'+str(i),'before':before,'after':deepcopy(after),'reason':why})
    def swimmer(c):
        p=c['initialState']['declaredPath'];p.update({'centerFrom':[15,0,3],'centerTo':[25,0,3],'bodyHalfExtents':[2.5,2.5,3],'anatomy':'Actual Medium Wizard5x5, measured occupied height6. Swimming posture and occupied vertical clearance are explicit fixture inputs, not an automatic class height.','requiredClearWholeBodySweep':{'x':[12.5,27.5],'y':[-2.5,2.5],'z':[0,6]}})
        c['unresolvedPremises']+=' The whole-body swept corridor now needs actual fluid clearance throughx27.5. This required clearance is not a claim of1600ft3 selected water, new water creation, immunity to immersion or proved buoyancy. Bind the real selected quantity and continuous fluid/airway state under Q02 before a completed case.'
    edit(1,swimmer,'Replace a2x2 Wizard body with actual5x5 and measured height6; preserve conditional10ft forced path and real unresolved water/boat/breath inputs.')
    def magnet(c):
        s=c['initialState'];s['casterCenter']=[0,0,3];s['casterBodyHalfExtents']=[2.5,2.5,3]
        s['subjects'][0]['halfExtents']=[5,5,5]
        s['subjects'][1]['center']=[32,0,3];s['subjects'][1]['halfExtents']=[2.5,2.5,3]
        s['actualMeasuredHeights']='Large10x10 occupied footprint with measured height10; Medium5x5 with measured height6. Both start supported on floorz0. The actual proposed sphere point remains[20,0,1].'
        s['geometryConsequences02']={'largeCenterDistanceSquared':160,'mediumCenterDistanceSquared':148,'radiusSquared':400,'casterLargeHorizontalGapFt':0.5,'bothWholeBodiesIntersectSphere':True}
        c['unresolvedPremises']+=' The low sphere point makes a literal3D straight pull descend toward the ground for both subjects. Their larger whole bodies cannot penetrate that floor: a failed save alone does not prove a positive displacement. Under Q09 explicitly resolve center/arrival geometry, collision order and ground blocking without silently projecting a3D pull onto horizontal ground or granting flight. No final stop/distance is asserted here.'
    edit(6,magnet,'Correct Large10x10 and Medium5x5, caster5x5 and actual heights. Recompute membership and expose the real ground-collision consequence for the pending ordered-pull rule; keep mass/material/save profiles conditional.')
    def passwall(c):
        s=c['initialState'];s['bodyCenter']=[21.5,0,3];s['bodyHalfExtents']=[2.5,2.5,3];s['nearExteriorCandidateCenter']=[17.5,0,3]
        s['actualBodyAndSupport']='Declared Medium5x5, measured height6 on floorz0. Current bodyx[19,24] occupies the open5ft-wide/10ft-high passage and near mouth. At exterior center17.5 its entire bodyx[15,20] lies outside the wall interior; y[-2.5,2.5],z[0,6] fit the local route. Gear must fit that declared occupied envelope.'
        c['expectedIfNamedProposalAgreed']['nearCandidateCenterDistanceFt']=4
        c['expectedIfNamedProposalAgreed']['entireExteriorBodyX']=[15,20]
    edit(9,passwall,'The old exteriorcenter19 left a corrected5ft body inside the wall. The nearest whole-body exterior center is17.5,4ft from21.5; preserve both-mouth-blocked pending conflict and the distinct suppression/ending fork.')
    def rock(c):
        s=c['initialState'];s['casterCenter']=[0,0,3];s['casterBodyHalfExtents']=[2.5,2.5,3];s['recipient']['center']=[20,0,3];s['recipient']['bodyHalfExtents']=[2.5,2.5,3]
        s['actualBodiesAndSupport']='Both actual Medium Wizards occupy5x5 with measured height6 on floorz0. Target bodyz[0,6] remains below the ceilingz[10,11]; its horizontal footprint contains the converted2x2 ceiling projection. Caster body is separate. Proposed overhead-burst eligibility and actual support remain conditional.'
    edit(11,rock,'Correct real Wizard bodies and floor support without narrowing the falling-ceiling obligation or granting the proposed4d6 burst. Existing15→7→HP1 and one successful Wound save remain unchanged.')
    reverse=deepcopy(d)
    for op in reversed(ops):
        p,k=parent(reverse,op['path']);ck('Exact after '+op['path'],p[k]==op['after']);p[k]=deepcopy(op['before'])
    ck('Four case repairs reverse exactly',reverse==old)
    ck('All eight original procedures unchanged',d['records']==old['records'] and len(d['records'])==8)
    ck('All16 original texts and questions unchanged',d['all16HistoricalScenarioTexts']==old['all16HistoricalScenarioTexts'] and d['conferenceQuestions']==old['conferenceQuestions'])
    ck('All16 current IDs preserved',[c['id'] for c in d['conditionalConferenceVectors']]==[c['id'] for c in old['conditionalConferenceVectors']] and len(d['conditionalConferenceVectors'])==16)
    ck('Swimmer whole-body sweep covers endpoint',25+2.5==27.5 and 15-2.5==12.5 and 25-15==10)
    ck('Actual Large and Medium space',2*5==10 and 2*2.5==5)
    ck('Magnet both centers inside sphere',(8-20)**2+(5-1)**2==160 and (32-20)**2+(3-1)**2==148 and 160<400 and 148<400)
    ck('Caster and Large have no initial overlap',8-5-(0+2.5)==0.5)
    ck('Passwall nearest full exterior clearance',17.5+2.5==20 and 21.5-17.5==4 and 2*2.5==5 and 2*3<10)
    ck('Rock body below ceiling with exact damage/Wound arithmetic',3+3<10 and sum([4,4,4,3])==15 and 15//2==7 and 8-7==1 and 2*7>=8 and 15+2>=10)
    meta={k:d[k] for k in ['id','recordedAtUtc','status']};d['id']=d['id'].removesuffix('01')+'02';d['recordedAtUtc']=datetime.now(timezone.utc).isoformat();d['status']='UNSENT / UNADOPTED source-design conference02. All eight complete original procedures,16 original scenarios and16 questions unchanged; four conditional geometry cases repaired. No systemic rule chosen.'
    delta.write_bytes(encoded({'previousCandidate':info(src),'fullBeforeAfterChanges':ops,'actualGPTConcurrence':False,'sourceInformationDeleted':0}))
    d['occupiedSpaceReconciliation02']={'previousCandidate':info(src),'fullDelta':info(delta),'previousMetadataUnchanged':meta,'actualGPTConcurrence':False}
    manifest=json.loads((oldroot/'MANIFEST.json').read_bytes());paths={}
    for b in manifest['sources']:
        p=G/b['path'];ck('Exact full source '+b['path'],info(p)=={k:b[k] for k in ['path','bytes','sha256']});paths[p]=info(p)
    out.write_bytes(encoded(d))
    for p in [src,out,delta,R/'tools/repair_material_terrain_geometry_02.py',R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md']:paths[p]=info(p)
    root.mkdir();frozen=[]
    for p,b in sorted(paths.items(),key=lambda item:item[1]['path']):
        arc='sources/'+b['path'];dest=root/arc;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());frozen.append({**b,'archivePath':arc})
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'sources':frozen,'sourceCount':len(frozen),'originalProcedures':8,'originalCases':16,'conditionalTraces':16,'questions':16,'newRuleAdoptions':0}))
    (root/'LOCAL_PREFLIGHT.json').write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    (root/'README.md').write_text((oldroot/'README.md').read_text(encoding='utf8')+'\n\nConference02 supersedes UNSENT01 with four complete reversible body/placement repairs. Read the new candidate and MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02. Source procedures and16 design questions remain unchanged. In particular, do not infer a positive Magnetize displacement through the ground from a failed save, an undersized body in Passwall, or a new volume of selected water from a required clear path. These conditional traces expose necessary design inputs, not demonstrated runtime outcomes.\n',encoding='utf8',newline='\n')
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for b in frozen:assert z.read(b['archivePath'])==(G/b['path']).read_bytes()
    b=info(zp);req.write_text(f'Please conduct the material/terrain8 source conference using {zp.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}). Read all8 complete original procedures,16 preserved original scenarios,16 unchanged design questions and repaired conditional geometry traces. The new candidate preserves UNSENT01 and complete reversible body/placement deltas. Resolve actual finite water/current/buoyancy, permanent material/crafting/economy, terrain/ice clearance, Magnetize mass/metal/ordered whole-body collision, Passwall closure, rock/mud support/HP, building occupants and earth geometry before operative authorship. Correct Large10x10 and Medium5x5 bodies reveal ground blocking for the low Magnetize point and require exterior Passwall center17.5,4ft displacement. Do not silently fill missing profiles, stock value or physical permissions. Return complete source-linked dispositions/replacements in a downloadable archive; no adoption/runtime/balance/cosmology/domain closure.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'candidate':info(out),'archive':b,'manifest':info(root/'MANIFEST.json'),'checkReport':info(root/'LOCAL_PREFLIGHT.json'),'request':info(req),'sourceCount':len(frozen),'checkCount':len(checks),'submitted':False,'adopted':False,'allArchiveSourceHashesVerified':True}))
    print(json.dumps({'candidate':info(out),'archive':b,'sources':len(frozen),'checks':len(checks),'preparation':info(prep)}))


if __name__=='__main__':main()
