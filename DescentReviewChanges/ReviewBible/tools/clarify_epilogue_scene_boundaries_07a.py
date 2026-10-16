"""Clarify source wording, initiative and finite pressure in the local arc proposal."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    root=A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    hist=root/'history/before-scene-boundaries-07a'; out=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_SCENE_BOUNDARIES_07A.json'
    assert not hist.exists() and not out.exists()
    d=read(root/'ARCS_MODEL.json'); cb=read(root/'CASEBOOK.json'); before=deepcopy(d); oldcb=deepcopy(cb)
    assert cb['count']==65
    evidence=read(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARC_READING_01.json')
    source=next(x for u in evidence['units'] if u['id']=='EPI-15' for x in u['evidence'] if x['paragraphIndexZeroBased']==320)
    assert 'flickers out nightly' in source['text']
    a=d['arcs'][0]; site=a['map']['sites'][0]; k=d['arcs'][2]['knowledgeReward']; changes=[]
    def change(target,key,value,path):
        changes.append({'field':path,'before':deepcopy(target[key]),'after':deepcopy(value)}); target[key]=value
    change(a,'hook','One of the new constellations above post-epilogue Yieldheart flickers out nightly, preserving the original hook. The NEW local adaptation places three finite stray Null fragments in instruments that redirect star energy into weaponized silence. Their exact relationship to the reviewed residual-Null and relic procedures remains for joint integration.','/arcs/0/hook')
    change(site,'actors',site['actors']+' When an actor first attempts to touch or manipulate the lens assembly (including either service control), or attacks a spindle, begin ordinary initiative before resolving that hostile interaction. Venting is an actual Action on the actor’s turn; rotating the inner ring is another actual Action. No free pre-initiative vent or automatic uninterrupted pair is granted. Use actual positions, initiative, legal extra Actions and attacks; control completion powers off the extant spindles immediately. They do not attack after being powered off.','/arcs/0/map/sites/0/actors')
    change(site,'solution',site['solution']+' The visible vent and ring are both accessible within 5 ft of the lens assembly. Their labels provide the correct order, but do not suppress the stated hostility trigger. Before a player commits, describe the spindles turning toward any hand approaching those controls. Retreat through the actual south entrance remains possible; the spindles do not pursue beyond it.','/arcs/0/map/sites/0/solution')
    change(a['map']['sites'][1],'clue','Maintenance log explicitly confirms fragments moved into instruments after the constellation first began flickering out. It names no cosmic identity or Equation.','/arcs/0/map/sites/1/clue')
    profile=next(x for x in d['profiles'] if x['id']=='ARC-ENVOY')
    change(profile,'property',profile['property']+' The three reusable discussion slips are additional actual paper, 0.02 lb each. They cannot be replenished by restarting the exercise; a witnessed oral choice can substitute if the tokens are unavailable.','/profiles/2/property')
    change(k['operation'],'charge',k['operation']['charge']+' Activation requires the actual cap closed, vent closed and gauge verified at zero. An attempted activation without those prerequisites fails without consuming or resetting a cell; use ordinary Actions and the visible interlock. An intact seal raises gauge to 1. A cracked seal lets that one charge escape and the gauge reaches 0 by the failed sixty-second test. The running drive cannot refill pressure. A wrong route with an intact seal instead leaves gauge 1 with the return vane stopped. Both faults can coexist; the leaking gauge then reaches 0 and the operator must correct both before a passing test.','/arcs/2/knowledgeReward/operation/charge')
    # Preserve case IDs, replacing a false precise combat duration with its actual clock boundary.
    case=next(x for x in cb['cases'] if x['id']=='ARC15-C01'); oldcase=deepcopy(case)
    case.update(start='T=E−72h; S1 unsealed; both North Observatory spindles active. Known street pace 3 mph.',
        events='Travel 600 seconds from court to the site. Record actual siteElapsedSeconds from entry to exit, including approach, initiative, vent/ring/remove Actions, hostile turns, other abilities and any interruption. On successful recovery, return by the 600-second street; fit and close in two actual Actions (12 seconds), then stabilize for 600 uninterrupted seconds.',
        elapsedSeconds=None, elapsedFormula='1812 + actual siteElapsedSeconds, plus any independently incurred road/bench interruptions',
        end='If those actual events succeed, S1 becomes sealed and its one 50 gp claim is earned. The former fixed 1830-second total did not account for hostile initiative and is withdrawn in this proposal, preserved in history. No assumed misses, free enemy turns, extra Actions or resource refresh.')
    cb['cases'].extend([
        {'id':'ARC15-C08','start':'Worker adjacent to the labeled lens controls; both spindles active and aware of the approaching hand.','events':'Attempt to open the vent: enter actual initiative before resolving that Action. On a later legal Action the worker turns the inner ring if still able and within reach.','elapsedSeconds':None,'end':'Any spindle turns before completed power-off use their actual attacks/targets; after completed power-off they cannot attack. The posted solution succeeds mechanically but grants no immunity or guaranteed combat timing. Record actual regular markers rather than inserting an outside-initiative 12-second shortcut.'},
        {'id':'ARC17-C28','start':'One real cell activated with cap/vent closed and starting gauge 0; intact seal but reversed return route.','events':'Observe sixty seconds: gauge holds 1 but vane does not turn. Opening cap now would discharge the same stored charge. Instead close I, close E, open V (three Actions), wait sixty seconds, then open C (one Action).','elapsedSeconds':144,'end':'60-second diagnosis plus 84-second isolation. Gauge 0; one spent casing retained, no paper/ink spent and no blast. Correcting the route requires actual three Actions and a new real cell for another powered test; the still-running old drive cannot recharge it.'}
    ])
    cb['count']=len(cb['cases']); assert cb['count']==67
    d['knownProposalSeams']=[s.replace('Review EPI15 hostile-trigger/initiative assumptions and exact original flickering-constellation language before a final prose pass.','Scene clarification07A restores the exact flickering-out hook and requires real initiative at the lens; the old fixed combat sample is superseded by its explicit actual-clock formula. These corrections also need joint review.') for s in d['knownProposalSeams']]
    checks=[
        {'name':'original hook verified against preserved paragraph320','pass':source['textSha256']==hashlib.sha256(source['text'].encode()).hexdigest()},
        {'name':'all65 prior case IDs preserved and unique','pass':set(x['id'] for x in oldcb['cases'])<=set(x['id'] for x in cb['cases']) and len({x['id'] for x in cb['cases']})==67},
        {'name':'fixed offsite portion excludes actual site combat','pass':600+600+12+600==1812 and case['elapsedSeconds'] is None},
        {'name':'actual diagnosis plus safe charged isolation','pass':60+3*6+60+6==144},
        {'name':'voyage including source atmosphere unchanged','pass':d['arcs'][1]==before['arcs'][1]},
        {'name':'annual contract procedure unchanged','pass':d['arcs'][2]['contractProcedure']==before['arcs'][2]['contractProcedure']},
        {'name':'all approval gates remain false','pass':not any(d['common']['approvalGates'].values())}
    ]
    assert all(x['pass'] for x in checks)
    hist.mkdir(parents=True)
    for n in ['ARCS_MODEL.json','CASEBOOK.json','MANIFEST.json']:(hist/n).write_bytes((root/n).read_bytes())
    (root/'ARCS_MODEL.json').write_bytes(encoded(d)); (root/'CASEBOOK.json').write_bytes(encoded(cb))
    entries=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json']
    (root/'MANIFEST.json').write_bytes(encoded({'files':entries}))
    out.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Local source-fidelity and scene-boundary proposals, not jointly adopted.','sourceEvidence':source,'previousModel':info(hist/'ARCS_MODEL.json'),'previousCases':info(hist/'CASEBOOK.json'),'model':info(root/'ARCS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'changes':changes,'case01Change':{'before':oldcase,'after':case},'authoredCases':67,'newCases':2,'checks':checks,'checkCount':len(checks),'failureCount':0,'scope':'Source phrase, explicit actual initiative boundary, finite-pressure diagnostic distinction and selected arithmetic; not a combat simulation or joint semantic approval.','newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    print(json.dumps({'receipt':info(out),'model':info(root/'ARCS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'cases':67,'checks':len(checks),'failures':0}))

if __name__=='__main__':main()
