"""Independent finite AABB/source verification; does not import the builder.

A collision pass is not an engineering/support pass. Expected world-bound failures
are recorded as failures of the witness predicate, never disguised as a sealed W01.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent/'fortress_w01_geometry_405'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def pointer(x,p):
    for part in p.strip('/').split('/'):
        k=part.replace('~1','/').replace('~0','~')
        x=x[int(k)] if isinstance(x,list) else x[k]
    return x
def body(p):return [p[0],p[0]+5,p[1],p[1]+5,p[2],p[2]+6]
def intersection(a,b):
    lengths=[min(a[k+1],b[k+1])-max(a[k],b[k]) for k in (0,2,4)]
    return all(x>0 for x in lengths)
def union(a,b):return [v for k in (0,2,4) for v in (min(a[k],b[k]),max(a[k+1],b[k+1]))]
def contains(a,b):return all(a[k]<=b[k] and b[k+1]<=a[k+1] for k in (0,2,4))
def contacts(a,b):
    result=[]
    for k in (0,2,4):
        if a[k+1]==b[k] or b[k+1]==a[k]:
            other=[j for j in (0,2,4) if j!=k]
            lengths=[min(a[j+1],b[j+1])-max(a[j],b[j]) for j in other]
            if min(lengths)>0:result.append(dict(axis='xyz'[k//2],areaSquareFeet=lengths[0]*lengths[1]))
    return result


def main():
    m=json.loads((ROOT/'GEOMETRY_405.json').read_bytes()); checks=[]
    def check(name,predicate):
        checks.append(dict(id=name,pass_=bool(predicate)))
        if not predicate:raise AssertionError(name)
    for s in m['sourceBindings']:
        b=(ROOT/s['member']).read_bytes();check('bytes:'+s['member'],len(b)==s['bytes'] and sha(b)==s['sha256'])
    q=json.loads((ROOT/'sources/Q23.json').read_bytes())
    check('Q23 exact source',sha((ROOT/'sources/Q23.json').read_bytes())=='149d4098591799f51afa37837ccca722eb9ae08c3ea437c640d943f33b1bb637')
    check('Q23 pointer',pointer(q,'/questions/2/id')=='PG9-Q23')
    contract=json.loads((ROOT/'sources/W01_CONTRACT.json').read_bytes())
    check('W01 contract pointer',pointer(contract,'/remainingWitnessParts/0/id')=='PG328-W01')
    parent=json.loads((ROOT/'sources/PARENT.json').read_bytes())
    space='RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1/space'
    check('inherited bounds exact',parent['final']['spaces'][space]['bounds']==m['worldBounds'])
    check('no new mechanics or application',m['mechanicalSupport']==dict(status='UNADJUDICATED',contactsAreLoadBearing=False,collapseSimulated=False) and not any(m['stateChange'][k] for k in ('parentMutated','actorMoved','castsOrDamageAdded','W02Constructed','queueChanged','applicationAuthorized')))
    ids=[p['id'] for p in m['panels']];check('unique primitive identities',len(ids)==len(set(ids)))
    check('wall/floor durability',all((p['AC'],p['HP'])==(17,60) for p in m['panels'] if 'AC' in p))
    check('door/main gate durability',all((p['AC'],p['HP'])==((17,60) if p['kind']=='main-gate' else (15,30)) for p in m['openings']))
    check('source damage panel exact',next(p['nominalBounds'] for p in m['panels'] if p['id']=='W01-SOUTH-WALL-X25-Z0')==[25,30,0,5,0,5])
    check('source ground keep flight unchanged',next(s for s in m['stairFlights'] if s['id']=='keep-flight-0')['count']==30)
    for p in m['panels']:
        check('finite geometry:'+p['id'],all(contains(m['worldBounds'],f) and all(f[k]<=f[k+1] for k in (0,2,4)) for f in p['occupiedFragments']))
    objects=m['panels']+m['doorLeaves']
    check('each opening has one leaf',sorted(x['openingId'] for x in m['doorLeaves'])==sorted(x['id'] for x in m['openings']))
    solids=[(p['id'],f) for p in objects for f in p['occupiedFragments'] if all(f[k]<f[k+1] for k in (0,2,4))]
    route_results=[]
    for ri,r in enumerate(m['navigationPaths']):
        bad=[];outside=[]
        for n,(a,b) in enumerate(zip(r['positions'],r['positions'][1:])):
            envelope=union(body(a),body(b))
            if not contains(m['worldBounds'],envelope):outside.append(dict(segment=n,pointer=f'/navigationPaths/{ri}/positions/{n+1}',sweptBounds=envelope))
            hits=[id for id,f in solids if intersection(envelope,f)]
            if hits:bad.append(dict(segment=n,pointer=f'/navigationPaths/{ri}/positions/{n+1}',solidIds=hits))
        # All bound cargo is contained in the body envelope at every pose, hence in each swept union.
        cargo=all(contains([0,5,0,5,0,6],b) for b in m['bodyAndCargo']['cargoRelativeBounds'].values())
        route_results.append(dict(id=r['id'],sourcePointer=f'/navigationPaths/{ri}',segments=len(r['positions'])-1,
            collisionPass=not bad,worldBoundsPass=not outside,cargoContainmentPass=cargo,
            collisions=bad,worldBoundFailures=outside,mechanicalSupport='UNADJUDICATED'))
    # Independently validate preserved 403 B position and A/B line of sight through SW aperture.
    bbody=body([15,10,0]);check('B retained body clear',not any(intersection(bbody,f) for _,f in solids))
    # A narrow rectangular tube contains the actual centre-to-centre line without touching a solid.
    los=[17.5,27.5,12.5,12.5,3,3]
    los_hits=[id for id,f in solids if f[0]<27.5 and f[1]>17.5 and f[2]<12.5<f[3] and f[4]<3<f[5]]
    check('403 A/B centre line clear',not los_hits)
    local=next(r for r in route_results if r['id']=='403-A-movement')
    check('403 local movement retained clear',local['collisionPass'] and local['worldBoundsPass'])
    local_path=next(r for r in m['navigationPaths'] if r['id']=='403-A-movement')['positions']
    rel=m['bodyAndCargo']['local403TileRelativeBounds']
    tile_pose=m['bodyAndCargo']['cargoRelativeBounds']['PG328-W01-403:CLAY-TILE-1']
    check('tile dimensions retained', [tile_pose[k+1]-tile_pose[k] for k in (0,2,4)]==[1,1,.25])
    for a,b in zip(local_path,local_path[1:]):
        boxes=[[rel[k]+p[k//2] for k in range(6)] for p in (a,b)]
        envelope=union(*boxes)
        check('403 original tile sweep',not any(intersection(envelope,f) for _,f in solids))
    # Face-contact inventory is deliberately not a support/dependency graph.
    graph=[]
    for i,a in enumerate(objects):
        for b in objects[i+1:]:
            face=[];joined=False
            for af in a['occupiedFragments']:
                for bf in b['occupiedFragments']:
                    face.extend(contacts(af,bf));joined=joined or intersection(af,bf)
            if face or joined:graph.append(dict(a=a['id'],b=b['id'],faceContacts=face,positiveVolumeJoin=joined,loadBearing=None))
    dump(ROOT/'GEOMETRIC_CONNECTIONS_405.json',dict(id='PG328-W01-CONTACTS-405',geometrySha256=sha((ROOT/'GEOMETRY_405.json').read_bytes()),connections=graph,mechanicalMeaning='NONE; contact and overlapping construction joints do not designate load-bearing support.'))
    failures=[r['id'] for r in route_results if not r['collisionPass']]
    expected=[f'tower-{name}-stairs-30' for name in ('SW','SE','NW','NE')]
    bounds_failed=[r['id'] for r in route_results if not r['worldBoundsPass']]
    # Exact quarter-foot subdivision only identifies path junctions. Collision tests
    # above cover full continuous swept boxes, not isolated sample points.
    adjacency={}
    for r,res in zip(m['navigationPaths'],route_results):
        if not res['collisionPass'] or not res['worldBoundsPass']:continue
        for a,b in zip(r['positions'],r['positions'][1:]):
            check('axis-aligned route:'+r['id'],sum(x!=y for x,y in zip(a,b))<=1)
            n=max(1,round(max(abs(x-y) for x,y in zip(a,b))*4))
            points=[tuple(a[k]+(b[k]-a[k])*i/n for k in range(3)) for i in range(n+1)]
            for u,v in zip(points,points[1:]):
                adjacency.setdefault(u,set()).add(v);adjacency.setdefault(v,set()).add(u)
    visited=set();todo=[(25,10,0)]
    while todo:
        u=todo.pop()
        if u in visited:continue
        visited.add(u);todo.extend(adjacency.get(u,set())-visited)
    disconnected=[]
    for r,res in zip(m['navigationPaths'],route_results):
        if res['collisionPass'] and res['worldBoundsPass'] and any(tuple(p) not in visited for p in r['positions']):disconnected.append(r['id'])
    report=dict(id='PG328-W01-INDEPENDENT-GEOMETRY-405',status='GEOMETRY_CHECKED_W01_OPEN_NO_SEAL',
        sourceAndRegistryAssertions=len(checks),primitiveCount=len(m['panels']),occupiedFragments=len(solids),
        openingCount=len(m['openings']),routeCount=len(route_results),sweptSegments=sum(r['segments'] for r in route_results),
        faceOrJointConnections=len(graph),checks=checks,routes=route_results,
        connectedClearanceNodes=len(visited),disconnectedPassingRoutes=disconnected,
        unexpectedCollisionRoutes=failures,worldBoundFailureRoutes=bounds_failed,expectedWorldBoundFailures=expected,
        towerRoofCertificate=dict(requiredStandingBody=[5,5,6],floorZ=40,minimumBodyTopZ=46,inheritedMaximumZ=40,deficitFeet=6,
            parentPointer='/final/spaces/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A~1cast1~1space/bounds',sourcePointer='sources/Q23.json#/questions/2/answer'),
        geometryOnlyCandidate=not failures and not disconnected and bounds_failed==expected,mechanicalSupportValidated=False,witnessSealed=False,acceptedIds=[],appliedIds=[],applicationAuthorized=False)
    dump(ROOT/'VERIFICATION_405.json',report)
    print(json.dumps({k:report[k] for k in ('sourceAndRegistryAssertions','primitiveCount','openingCount','routeCount','sweptSegments','faceOrJointConnections','unexpectedCollisionRoutes','worldBoundFailureRoutes','geometryOnlyCandidate')}))
    if failures or disconnected or bounds_failed!=expected:raise SystemExit('Unexpected geometry defect; inspect VERIFICATION_405.json')


if __name__=='__main__':main()
