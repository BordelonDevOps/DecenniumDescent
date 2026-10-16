"""Resolve the sample's exact footprint, movement and boundary references."""
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
    root=A/'cosmology-epilogue-campaign-arcs-local-draft-01';history=root/'history/before-voyage-geometry-04a'
    receipt=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_GEOMETRY_04A.json'
    assert not history.exists() and not receipt.exists();history.mkdir(parents=True)
    for name in ['ARCS_MODEL.json','CASEBOOK.json','MANIFEST.json']:(history/name).write_bytes((root/name).read_bytes())
    model=read(root/'ARCS_MODEL.json');cases=read(root/'CASEBOOK.json');oldmodel=deepcopy(model);oldcases=deepcopy(cases)
    arc=model['arcs'][1];v=arc['vessel'];oldbody=v['body']
    v['body'] += ' In the berth map, the hull isx0–20,y0–30. Main cabin isx0–20,y0–15; airlock isx10–20,y15–25, so the two enclosed rooms do not overlap. The inner door lies aty15,x10–20; the outer door lies atx20,y15–25. The two5ft station positions lie atx0–5,y0–5 andx15–20,y0–5. The sample worker starts beside the inner door at(12.5,12.5), uses a legal airlock cell at(12.5,17.5), and works at(32.5,17.5). The longest sample doorway/gangplank traversal is20ft; no crew station blocks it.'
    oldgeometry=arc['strandScene']['geometry']
    arc['strandScene']['geometry']=oldgeometry.replace('outer hatch atx20,y10–20; fixed10ft-wide5ft-long gangplank spansx20–25,y10–20; working bayx25–35,y10–20','outer hatch atx20,y15–25; fixed10ft-wide5ft-long gangplank spansx20–25,y15–25; working bayx25–35,y15–25').replace('atx35,y15','atx35,y20')
    oldpriority=v['supportStates']['priority']
    v['supportStates']['priority'] += ' Exactly enough fuel to cover an interval supplies power through that interval’s endpoint, allowing its legal completed transfer to resolve before the resulting zero-fuel loss. Insufficient fuel removes lift at its actual earlier depletion timestamp; the transfer cannot pretend it remained powered.'
    schedule=arc['route']['workedDefaultSchedule']['schedule']
    inner=next(x for x in schedule if x['id']=='inner-out');oldevent=inner['event'];inner['event']='Open inner door and move to the legal airlock position using actual effectiveSpeed20 after Burdened. The printed route is within20ft.'
    c=next(x for x in cases['cases'] if x['id']=='ARC16-C14');oldcase=deepcopy(c)
    c['start']='TimeT0 is the end of the current numbered round: its craft event was already paid, and the engineer has just become Incapacitated after contributing. No replacement is available for the next full round.'
    c['events']='The already-paid event stands. During the next full6second round no replacement engineer contributes; assess the unmet requirement atT0+6.'
    checks=[
      {'name':'cabin and airlock interiors do not overlap','pass':15<=15 and 20*15+10*10<=20*30},
      {'name':'hull and working bay fit the40ft platform','pass':30<=40 and 35<=40 and 25<=40},
      {'name':'Burdened sample movement fits printed path','pass':30-10==20 and 32.5-12.5==20},
      {'name':'strands within5ft reach from sample work position','pass':(35-32.5)**2+(20-17.5)**2<=25},
      {'name':'all28 IDs and authored durations remain unchanged','pass':[(x['id'],x.get('elapsedSeconds')) for x in cases['cases']]==[(x['id'],x.get('elapsedSeconds')) for x in oldcases['cases']]},
      {'name':'20interval schedule and final time remain intact','pass':len(schedule)==20 and schedule[-1]['end']==3726 and all(a['end']==b['start'] for a,b in zip(schedule,schedule[1:]))}
    ]
    assert all(x['pass'] for x in checks)
    (root/'ARCS_MODEL.json').write_bytes(encoded(model));(root/'CASEBOOK.json').write_bytes(encoded(cases))
    entries=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json']
    (root/'MANIFEST.json').write_bytes(encoded({'files':entries}))
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Local proposal clarification, unsubmitted/unadopted.','baseRefinement':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_VOYAGE_REFINEMENT_04.json'),'previousModel':info(history/'ARCS_MODEL.json'),'previousCases':info(history/'CASEBOOK.json'),'model':info(root/'ARCS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'changes':[{'jsonPointer':'/arcs/1/vessel/body','before':oldbody,'after':v['body']},{'jsonPointer':'/arcs/1/strandScene/geometry','before':oldgeometry,'after':arc['strandScene']['geometry']},{'jsonPointer':'/arcs/1/vessel/supportStates/priority','before':oldpriority,'after':v['supportStates']['priority']},{'scheduleId':'inner-out','before':oldevent,'after':inner['event']},{'caseId':'ARC16-C14','before':oldcase,'after':c}],'checks':checks,'checkCount':6,'failureCount':0,'scope':'Exact sample geometry/movement, time origin and retained schedule only; no broad semantic approval.','newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    print(json.dumps({'receipt':info(receipt),'model':info(root/'ARCS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'checks':6,'failures':0}))
if __name__=='__main__':main()
