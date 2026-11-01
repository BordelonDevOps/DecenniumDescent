#!/usr/bin/env python3
"""Independent integrity and mechanics verification for PG328-W09-R1 witness 428."""
from __future__ import annotations
import copy, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=BASE/'fortress_w09_successor_witness_428'
REPLAY=OUT/'W09_REPLAY_428_TESTONLY.json'
ARCHIVE=OUT/'DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip'

def rawsha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def unesc(s): return s.replace('~1','/').replace('~0','~')
def apply_patch(doc,ops):
    doc=copy.deepcopy(doc)
    for op in ops:
        tokens=[unesc(x) for x in op['path'].split('/')[1:]]
        parent=doc
        for token in tokens[:-1]: parent=parent[int(token)] if isinstance(parent,list) else parent[token]
        key=tokens[-1]
        if op['op']=='remove':
            if isinstance(parent,list): parent.pop(int(key))
            else: del parent[key]
        elif op['op']=='replace':
            if isinstance(parent,list): parent[int(key)]=copy.deepcopy(op['value'])
            else: parent[key]=copy.deepcopy(op['value'])
        elif op['op']=='add':
            if isinstance(parent,list): parent.insert(int(key),copy.deepcopy(op['value']))
            else: parent[key]=copy.deepcopy(op['value'])
        else: raise ValueError(op['op'])
    return doc

def main():
    checks=[]
    def check(name,ok,detail):
        checks.append({'id':name,'passed':bool(ok),'detail':detail})
        if not ok: raise AssertionError(f'{name}: {detail}')
    w=read(REPLAY); bindings=w['sourceBindings']
    for b in bindings:
        p=ROOT/Path(b['path'])
        check('source:'+b['id'],p.is_file() and p.stat().st_size==b['bytes'] and rawsha(p)==b['sha256'],b['path'])
    parent=read(BASE/'fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json')
    check('exact-parent-terminal',parent['terminalStateId']=='S030' and parent['terminalStateSha256']==w['parentBinding']['terminalStateSha256'] and digest(parent['stateSnapshots']['S030'])==parent['terminalStateSha256'],'W01-403 S030 is source-bound and copied without modification.')
    state=copy.deepcopy(w['stateSnapshots'][w['branchInitialStateId']])
    check('embedded-parent-snapshot',digest(state['inheritedParentState'])==parent['terminalStateSha256'] and state['inheritedParentState']==parent['stateSnapshots']['S030'] and state['parentSnapshotReference']['copiedWithoutBranchEdits'],'The entire S030 snapshot is embedded byte-equivalently at JSON value level and remains separately preserved.')
    check('branch-initial-hash',digest(state)==w['branchInitialStateSha256'],'Initial branch snapshot hash matches.')
    for e in w['events']:
        check('forward-before:'+e['eventId'],digest(state)==e['beforeStateSha256'],'Current replay state equals event before hash.')
        after=apply_patch(state,e['forwardPatch'])
        check('forward-after:'+e['eventId'],digest(after)==e['afterStateSha256'],'Forward patch reproduces event after hash.')
        restored=apply_patch(after,e['inversePatch'])
        check('inverse:'+e['eventId'],digest(restored)==digest(state),'Inverse patch restores exact prior canonical bytes.')
        if e['kind']=='TEST_ONLY_ORDINARY_ATTACK_SUNDER':
            held=state['tile']['heldBoundsFeet']
            bounds={'x':held['x'],'y':held['y'],'z':held['z']}
            flat=[bounds['x'][0],bounds['x'][1],bounds['y'][0],bounds['y'][1],bounds['z'][0],bounds['z'][1]]
            sim={'boundsFeet':flat}; initial=copy.deepcopy(sim)
            for sub in e['authoredInputs']['tileSwingSubmotions']:
                check('swing-from:'+e['eventId']+':'+sub['id'],sim['boundsFeet']==sub['fromBoundsFeet'],'Swing submotion starts at current tile bounds.')
                nxt=apply_patch(sim,sub['forwardPatch'])
                check('swing-to:'+e['eventId']+':'+sub['id'],nxt['boundsFeet']==sub['toBoundsFeet'],'Swing submotion reaches its recorded bounds.')
                back=apply_patch(nxt,sub['inversePatch'])
                check('swing-inverse:'+e['eventId']+':'+sub['id'],back==sim,'Submotion inverse restores its exact prior bounds.')
                sim=nxt
            check('swing-return:'+e['eventId'],sim==initial and after['tile']['heldBoundsFeet']==held,'Object returns to its held carry bounds within the same ordinary attack action.')
        state=after
    check('terminal-hash',digest(state)==w['terminalStateSha256'] and digest(state)==digest(w['stateSnapshots'][w['terminalStateId']]),'Final replay state matches the terminal snapshot.')
    events=w['events']
    starts=[e for e in events if e['kind']=='REGULAR_TURN_START']; ends=[e for e in events if e['kind']=='REGULAR_TURN_END']
    by_actor={a:{'start':sum(e['authoredInputs']['actor']==a for e in starts),'end':sum(e['authoredInputs']['actor']==a for e in ends)} for a in 'ABCD'}
    check('regular-markers',by_actor=={a:{'start':16,'end':16} for a in 'ABCD'},json.dumps(by_actor,sort_keys=True))
    check('inherited-12_9-boundary',w['initiativeMarkerCoverage']['inheritedBoundaryMarker']['time']==12.9 and w['initiativeMarkerCoverage']['inheritedBoundaryMarker']['inheritedFromExactS030Parent'],'The 12.9 A end marker remains inherited from S030.')
    moves=[e for e in events if e['kind']=='REGULAR_MOVEMENT']
    move_spends=[e['authoredInputs']['spentFeet'] for e in moves]
    endpoints=[e['authoredInputs']['routePoints'][-1] for e in moves]
    check('movement-budget-and-endpoints',move_spends==[30.0,30.0,30.0,10.0] and endpoints==[[49.0,10.0,0.0],[55.0,34.0,0.0],[46.0,55.0,0.0],[45.0,59.5,4.5]],'100-foot movement is split 30/30/30/10 and reaches the attack pose.')
    route=w['movementPlan']['routePoints']; route_feet=sum(sum(abs(float(y)-float(x)) for x,y in zip(a,b)) for a,b in zip(route,route[1:]))
    check('route-length',route_feet==100.0 and w['movementPlan']['routeTotalFeet']==100.0,'Expanded Geometry405 route is 100 feet.')
    carry=[e for e in events if e['kind']=='TEST_ONLY_FREE_OBJECT_INTERACTION']
    check('carry-transition',len(carry)==1 and carry[0]['time']==18.01 and carry[0]['authoredInputs']['correctedBoundsFeet']==[27,28,7,8,3,3.25] and carry[0]['authoredInputs']['noActionOrMovementSpent'],'Corrected tile reposition is one interaction after A starts at 18.0.')
    attacks=[e for e in events if e['kind']=='TEST_ONLY_ORDINARY_ATTACK_SUNDER']
    expected_times=[36.1+6*i for i in range(12)]
    check('attack-inputs',len(attacks)==12 and [e['time'] for e in attacks]==expected_times and all(e['authoredInputs']['roll']['total']==17 and e['authoredInputs']['damage']['total']==5 and e['authoredInputs']['actionCost']==1 and e['authoredInputs']['rpCost']==0 for e in attacks),'Twelve stipulated successful 5-damage attacks occur at the adopted times.')
    final=read(REPLAY)['stateSnapshots'][w['terminalStateId']]
    fw=final['fortressW09']
    check('collapse-scope',fw['targetPanel']['hp']==0 and fw['targetPanel']['destroyed'] and fw['destroyedParts']==fw['dependentStairPartsOnTargetRemoval'] and len(fw['destroyedParts'])==18 and fw['rootId']=='origin-ground-face','Only the named target and 18 dependent stair parts are marked destroyed in the branch ledger.')
    check('fall-result',fw['fall']['status']=='LANDED_TEST_ONLY' and fw['fall']['distanceFeet']==4.0 and fw['fall']['damage']==0 and fw['fall']['landedAt']==108.9 and final['actors']['A']['position']==[45,59.5,0.5] and final['actors']['A']['HP']==122,'The hypothetical fall lands on tread 1 after 4 feet with zero damage.')
    check('tile-preserved',final['tile']['heldBy']=='A:right' and final['tile']['expiresAtEventTime']==3606.13 and not final['tile']['consumed'],'Tile custody, expiry and non-consumption are preserved.')
    q=final['queueAuthority']
    check('queue-preserved',q['reviewedApplied']==830 and q['pending']==18 and q['acceptedUnapplied']==0 and not q['identityAcceptedOrApplied'],'Current queue remains 830/18/0 and Fortress remains pending.')
    check('no-seal-or-canon',w['scope']['campaignOccurrence'] is False and w['scope']['canonicalRulesChanged'] is False and w['scope']['fixtureMutated'] is False and w['scope']['identityAcceptedOrApplied'] is False and 'No W09 or Fortress seal is issued.' in w['nonEffects'],'No campaign event, seal, canon update, acceptance or application is claimed.')

    report={'schemaVersion':1,'id':'PG328-W09-R1-INDEPENDENT-VERIFICATION-428','classification':'INDEPENDENT_TEST_ONLY_STATIC_AND_REVERSIBLE_REPLAY_VERIFICATION',
      'status':'PASS_PENDING_GPT_DIRECTOR_REVIEW','checkedLocalDate':'2026-11-01','witnessPath':'W09_REPLAY_428_TESTONLY.json',
      'witnessSha256':rawsha(REPLAY),'checksPassed':len(checks),'checksFailed':0,'checks':checks,
      'eventCount':len(events),'turnMarkerCount':len(starts)+len(ends),'reversibleEventCount':len(events),
      'queue':{'reviewedApplied':830,'pending':18,'acceptedUnapplied':0},'witnessSealed':False,'applicationAuthorized':False}
    (OUT/'INDEPENDENT_VERIFICATION_428.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (OUT/'VERIFY_W09_REPLAY_428.py').write_text(Path(__file__).read_text(encoding='utf-8-sig'),encoding='utf-8',newline='\n')
    manifest_files=[]
    for p in sorted(x for x in OUT.rglob('*') if x.is_file() and x.name not in {'MANIFEST_428.json','DELIVERY_428.json',ARCHIVE.name}):
        manifest_files.append({'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':rawsha(p)})
    manifest={'id':'PG328-W09-R1-MANIFEST-428','artifact':ARCHIVE.name,'status':'TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW',
      'files':manifest_files,'sourceBindings':bindings}
    (OUT/'MANIFEST_428.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    archive=OUT/ARCHIVE
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in OUT.rglob('*') if x.is_file() and x.name not in {'DELIVERY_428.json',ARCHIVE.name}): z.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:
        bad=z.testzip(); names=z.namelist()
        check('archive-crc',bad is None,f'CRC result {bad!r}; members {len(names)}')
        check('archive-member-set',set(names)=={x['path'] for x in manifest_files}|{'MANIFEST_428.json'},'Archive members match the manifest plus manifest file.')
        for f in manifest_files: check('archive-member:'+f['path'],hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256'],'Member bytes match manifest.')
    # Re-emit report with archive checks included, then refresh manifest/archive/delivery once.
    report['checks']=checks; report['checksPassed']=len(checks)
    (OUT/'INDEPENDENT_VERIFICATION_428.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    manifest_files=[]
    for p in sorted(x for x in OUT.rglob('*') if x.is_file() and x.name not in {'MANIFEST_428.json','DELIVERY_428.json',ARCHIVE.name}):
        manifest_files.append({'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':rawsha(p)})
    manifest['files']=manifest_files
    (OUT/'MANIFEST_428.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in OUT.rglob('*') if x.is_file() and x.name not in {'DELIVERY_428.json',ARCHIVE.name}): z.write(p,p.relative_to(OUT).as_posix())
    delivery={'id':'PG328-W09-R1-DELIVERY-428','artifact':ARCHIVE.name,'archiveBytes':archive.stat().st_size,'archiveSha256':rawsha(archive),
      'manifestSha256':rawsha(OUT/'MANIFEST_428.json'),'witnessPath':'W09_REPLAY_428_TESTONLY.json','witnessSha256':rawsha(REPLAY),
      'memberCount':len(manifest_files)+1,'status':'TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW'}
    (OUT/'DELIVERY_428.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':report['status'],'checksPassed':report['checksPassed'],'eventCount':len(events),'archiveBytes':delivery['archiveBytes'],'archiveSha256':delivery['archiveSha256']},indent=2))
if __name__=='__main__': main()
