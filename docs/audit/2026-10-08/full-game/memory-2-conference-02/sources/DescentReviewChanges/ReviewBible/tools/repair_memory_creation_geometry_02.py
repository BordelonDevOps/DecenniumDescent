"""Repair conditional conference body fixtures; do not choose any pending memory/material rule."""
from copy import deepcopy
from datetime import datetime, timezone
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    for name,folder,title in [('memory_2','memory-2','Memory_2'),('creation','creation','Creation')]:
        repair(name,folder,title)


def repair(name,folder,title):
    src=R/f'data/director/spell_review/{name}_conference_01.json'
    out=R/f'data/director/spell_review/{name}_conference_02.json'
    oldroot=A/f'{folder}-conference-01';root=A/f'{folder}-conference-02'
    delta=A/f'{title.upper()}_GEOMETRY_DELTA_02.json'
    zp=A/f'DD_{title}_Conference_02.zip';prep=A/f'{title.upper()}_CONFERENCE_02_PREPARATION.json'
    request=A/f'{title.upper()}_CONFERENCE_02_REQUEST.txt'
    assert all(not p.exists() for p in [out,root,delta,zp,prep,request])
    old=json.loads(src.read_bytes());d=deepcopy(old);ops=[];checks=[]
    def ck(n,v):
        checks.append({'name':n,'passed':bool(v)});assert v,n
    def edit(i,fn,why):
        before=deepcopy(d['conditionalConferenceVectors'][i]);after=deepcopy(before);fn(after)
        after['geometryRepair02']={'acceptedBodySource':info(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'),'reason':why,'actualGPTConcurrence':False,'scope':'Conditional source-conference trace; no new rule, ability, defense or runtime proof.'}
        ops.append({'path':'/conditionalConferenceVectors/'+str(i),'before':before,'after':deepcopy(after),'reason':why});d['conditionalConferenceVectors'][i]=after
    if name=='memory_2':
        def first(c):
            c['geometry'].update({'casterCenter':[0,0,3],'targetCenter':[20,0,3],'bothBodyHalfExtents':[2.5,2.5,3],'anatomy':'Both actual Medium Wizard bodies; measured occupied height6, supporting floorz0.','nearestBodyGapFt':15})
        edit(0,first,'Replace both actual Wizard2x2 cubes with5x5 bodies on the floor; target remains legally near, separate and unobstructed. Narrative/window/save/resource results unchanged.')
        def sequential(c):
            c['geometry']='At each separately admitted named cast, that source occupies center[0,0,3] and the recipient center[20,0,3]; each actual Medium anatomy occupies5x5ft with measured height6, half-extents[2.5,2.5,3], supported on floorz0. Whole-body gap15ft; actual perception where required and clear LoE. The source casts occur at different times; this conditional trace does not place all source actors simultaneously in the same space or grant them free movement. Any other area recipients retain their actual independent outcomes; only this named recipient history is followed.'
        edit(1,sequential,'Repair sequential source/recipient body declarations; preserve the genuine evidence, original-event chronology and highest-DC recovery fork without deciding it.')
        def haze(c):
            c['geometry'].update({'declaredCasePoint':[0,0,3],'casterBodyCenter':[0,0,3],'witnessBodyCenters':[[10,0,3],[0,20,3],[0,-20,3]],'allHalfExtents':[2.5,2.5,3],'actualAnatomyAndSupport':'All declared Medium5x5 bodies have measured height6 on unobstructed floorz0. WitnessC is on the same floor at y-20; no flight, unsupported elevated body, platform or new ability is assumed.','nearestPointDistancesFt':[0,7.5,17.5,17.5]})
        edit(2,haze,'Place all four ordinary bodies on real ground inside either unresolved30ft origin option. Remove the unsupported elevated synthetic witness and repair every footprint while preserving the original four saves/experience intervals.')
        edit(3,sequential,'Restore legal whole-body source/recipient geometry for each independently admitted cast; preserve exact overlapping memory intervals and independent Disrupt Memory boundary. This is not a complete simulated world/turn sequence.')
        ck('Four unchanged IDs and original texts',[c['id'] for c in d['conditionalConferenceVectors']]==[c['id'] for c in old['conditionalConferenceVectors']] and all(a['originalTextUnchanged']==b['originalTextUnchanged'] for a,b in zip(old['conditionalConferenceVectors'],d['conditionalConferenceVectors'])))
        ck('All four Haze bodies in sphere and nonoverlapping',7.5<30 and 17.5<30 and 10-5>0 and 20-5>0)
        ck('Two targeted bodies separated within30ft',20-2.5-2.5==15 and 15<30)
    else:
        def food(c):
            c['proposedCaseGeometry'].update({'casterCenter':[0,0,3],'casterBodyHalfExtents':[2.5,2.5,3],'casterAnatomy':'Actual Medium5x5, measured height6 on floorz0; output remains entirely separate.'})
        edit(0,food,'Bind actual caster body without altering the conditional14lb food composition/value or provisioning calculation.')
        def wood(c):
            c['sourceActor']['bodyGeometry02']={'center':[0,0,3],'halfExtents':[2.5,2.5,3],'floorZ':0,'anatomy':'Medium5x5, measured height6'}
            c['actualDamageSource'].update({'position':[17.5,0,3],'bodyHalfExtents':[2.5,2.5,3],'bodyGeometry02':'Actual Medium Warrior5x5, measured height6 on floorz0. Its x[15,20] only touches stockx[20,24] at the boundary; no interior overlap. The stock is within ordinary5ft melee reach with clear LoE.','nearestWholeBodyToStockFt':0})
        edit(1,wood,'A widened Warrior at oldcenter19 would intersect the wood. Move to17.5, retain legal Sunder reach and all paid attack/damage/conditional partition obligations.')
        ck('Whole Warrior body does not penetrate stock',17.5+2.5==20 and 17.5-2.5==15)
        ck('Stock damage and preserved totals',12+5>=15 and 5+3==8 and 20-8==12 and 20+60==80 and 5+15==20 and 3+9==12)
        ck('Provisioning remains conditional with no water grant',14//2==7 and 7*8==56 and d['conditionalConferenceVectors'][0]['conditionalArithmetic']==old['conditionalConferenceVectors'][0]['conditionalArithmetic'])
    from prepare_de4_fate_guard_amendment_01 import parent
    back=deepcopy(d)
    for op in reversed(ops):
        p,k=parent(back,op['path']);ck('Exact after '+op['path'],p[k]==op['after']);p[k]=deepcopy(op['before'])
    ck('Complete source candidate restored by reverse',back==old)
    ck('All design questions and complete originals unchanged',d['questions']==old['questions'] and d['originalExamplesUnchanged']==old['originalExamplesUnchanged'])
    prior_meta={k:d[k] for k in ['id','recordedAtUtc','status']}
    d['id']=d['id'].removesuffix('01')+'02';d['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
    d['status']='UNSENT / UNADOPTED source/design conference02. Complete original proposals, questions and scenarios unchanged; conditional body geometry repaired against accepted occupied space. No new systemic decision chosen.'
    delta.write_bytes(encoded({'id':title.upper()+'-GEOMETRY-DELTA02','previousCandidate':info(src),'completeCaseChanges':ops,'actualGPTConcurrence':False,'sourceInformationDeleted':0}))
    d['geometryReconciliation02']={'previousCandidate':info(src),'fullDelta':info(delta),'previousMetadataUnchanged':prior_meta,'actualGPTConcurrence':False}
    # Preserve every old full source; add new candidate and explicit correction evidence.
    manifest=json.loads((oldroot/'MANIFEST.json').read_bytes());paths={}
    for ref in manifest['sources']:
        p=G/ref['path'];ck('Exact prior full source '+ref['path'],info(p)=={k:ref[k] for k in ['path','bytes','sha256']});paths[p]=info(p)
    bodyp=R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'
    if not any(x['path']==info(bodyp)['path'] for x in d['sourceBindings']):d['sourceBindings'].append(info(bodyp))
    out.write_bytes(encoded(d))
    for p in [src,out,delta,bodyp,R/'tools/repair_memory_creation_geometry_02.py']:paths[p]=info(p)
    root.mkdir();frozen=[]
    for p,b in sorted(paths.items(),key=lambda pair:pair[1]['path']):
        arc='sources/'+b['path'];dest=root/arc;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());frozen.append({**b,'archivePath':arc})
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'sources':frozen,'sourceCount':len(frozen),'previousConference':info(oldroot/'MANIFEST.json'),'questions':len(d['questions']),'originalScenarios':len(d['originalExamplesUnchanged']),'conditionalTraces':len(d['conditionalConferenceVectors']),'newRuleAdoptions':0}))
    (root/'LOCAL_PREFLIGHT.json').write_bytes(encoded({'checks':checks,'checkCount':len(checks),'failureCount':0,'candidate':info(out),'newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    readme=(oldroot/'README.md').read_text(encoding='utf8')+'\n\nConference02 supersedes UNSENT01 solely to repair conditional occupied-space fixtures. Read the new candidate and full reversible GEOMETRY_DELTA_02 in sources. All original proposals and design questions remain unchanged. No source rule, quantity, ability or acceptance is inferred from these repaired conditional traces. Return actual question dispositions before operative authorship.\n'
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for ref in frozen:assert z.read(ref['archivePath'])==(G/ref['path']).read_bytes()
    b=info(zp)
    request.write_text(f'Please confer on {title.replace("_"," ")} using {zp.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}). This source/design conference02 supersedes unsent01 after occupied-space repair. Read all complete original procedures, {len(d["originalExamplesUnchanged"])} unchanged original scenarios, conditional traces and all {len(d["questions"])} unchanged design questions. Full frozen sources and reversible body/placement changes are supplied. Resolve every genuine new choice before operative authorship; preserve accepted interfaces and explicitly conditional missing content. Return a downloadable source-linked review with complete replacements where needed. No rule adoption, runtime, balance, cosmology or domain closure is requested.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'candidate':info(out),'archive':b,'manifest':info(root/'MANIFEST.json'),'checkReport':info(root/'LOCAL_PREFLIGHT.json'),'request':info(request),'sourceCount':len(frozen),'checkCount':len(checks),'questions':len(d['questions']),'submitted':False,'adopted':False,'allArchiveSourceHashesVerified':True}))
    print(json.dumps({'candidate':info(out),'archive':b,'sources':len(frozen),'checks':len(checks),'preparation':info(prep)}))


if __name__=='__main__':main()
