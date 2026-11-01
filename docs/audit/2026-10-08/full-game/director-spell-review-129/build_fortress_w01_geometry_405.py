"""Build a TEST_ONLY Q23 geometry certificate; never change a game state or rules.

Run with --source-cache pointing at the previously byte-verified Intake367 cache.
The separate verifier evaluates the exported primitives without importing this file.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / '.git').exists())
COMMIT = 'aaa6fff1f83ac41e24243a75b11147e4672901c6'
OUT = BASE / 'fortress_w01_geometry_405'
PREFIX = 'docs/audit/2026-10-08/full-game/director-spell-review-129/'


def encode(x):
    return (json.dumps(x, indent=2, ensure_ascii=False) + '\n').encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def overlap(a, b):
    return all(min(a[k+1], b[k+1]) > max(a[k], b[k]) for k in (0, 2, 4))


def cut(a, b):
    if not overlap(a, b):
        return [a]
    core = a[:]
    pieces = []
    for k in (0, 2, 4):
        lo, hi = max(core[k], b[k]), min(core[k+1], b[k+1])
        if core[k] < lo:
            part = core[:]; part[k+1] = lo; pieces.append(part); core[k] = lo
        if core[k+1] > hi:
            part = core[:]; part[k] = hi; pieces.append(part); core[k+1] = hi
    return pieces


def build(cache):
    OUT.mkdir(exist_ok=True)
    (OUT / 'sources').mkdir(exist_ok=True)
    (OUT / '.gitattributes').write_text('** -text !eol\nsources/** -diff -whitespace\n')
    bindings = []
    source_paths = {
        'Q23.json': 'conjure_demiplane_fortress_closure_intake_367/payload/rules/PG328_QUESTION_DISPOSITIONS.json',
        'W01_CONTRACT.json': 'conjure_demiplane_fortress_closure_intake_367/payload/authority/PG328_BLOCKER_REASSESSMENT.json',
        'AUTHORIZATION403.json': 'fortress_w01_structural_damage_witness_403_repack01/OWNER_W01_CONSTRUCTION_AUTHORIZATION_403.json',
        'GEOMETRY403.json': 'fortress_w01_structural_damage_witness_403_repack01/W01_GEOMETRY_403.json',
    }
    for name, path in source_paths.items():
        b = subprocess.check_output(['git', 'show', COMMIT + ':' + PREFIX + path], cwd=REPO)
        (OUT / 'sources' / name).write_bytes(b)
        bindings.append(dict(member='sources/' + name, repositoryPath=PREFIX+path, commit=COMMIT, bytes=len(b), sha256=sha(b)))
    parent = cache / 'held/evidence/packet328/prior/Return284_cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A.json'
    b = parent.read_bytes()
    assert sha(b) == 'b18e7c3b7acc9867d6448a8a58d98f2d45eeea629144b1a696ef0d7c76844e54'
    (OUT / 'sources/PARENT.json').write_bytes(b)
    bindings.append(dict(member='sources/PARENT.json', archivePath=PREFIX+'conjure_demiplane_fortress_closure_intake_367/payload/authority/PG328_HELD_ARCHIVE.zip', archiveSha256='47af8e23be318210229f7fd2b360be809b2b7ed5d73b08abcbeaf7a078c3f1f4', archiveMember='evidence/packet328/prior/Return284_cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A.json', bytes=len(b), sha256=sha(b)))
    panels, openings, regions, paths, stairs = [], [], [], [], []

    def opening(id, bounds, kind='door'):
        openings.append(dict(id=id, bounds=bounds, kind=kind, position='OPEN_TEST_ONLY_GEOMETRY', AC=17 if kind=='main-gate' else 15, HP=60 if kind=='main-gate' else 30))

    def primitive(id, bounds, kind, group, clips=(), durability=True):
        pieces = [bounds]
        for c in clips:
            pieces = [v for p in pieces for v in cut(p, c)]
        if pieces:
            p = dict(id=id, group=group, kind=kind, nominalBounds=bounds, occupiedFragments=pieces,
                     geometryOnly=True, loadBearingDependencies=None)
            if durability: p.update(AC=17, HP=60)
            panels.append(p)

    def wall(group, axis, start, stop, t0, t1, height, clips):
        for u in range(int(start), int(stop), 5):
            for z in range(0, height, 5):
                b = [u,u+5,t0,t1,z,z+5] if axis=='x' else [t0,t1,u,u+5,z,z+5]
                primitive(f'{group}-{u}-{z}', b, 'wall-panel', group, clips)

    def floors(group, bounds, levels, holes):
        x0,x1,y0,y1=bounds
        for z in levels:
            for i in range(round((x1-x0)/5)):
                for j in range(round((y1-y0)/5)):
                    x,y=x0+5*i,y0+5*j
                    clips=[[a,b,c,d,z-.25,z+.25] for a,b,c,d in holes(z)]
                    primitive(f'{group}-F{z}-{i}-{j}', [x,x+5,y,y+5,max(0,z-.25),z], 'floor-panel', group, clips)

    def route(id, group, poses, purpose):
        paths.append(dict(id=id, group=group, purpose=purpose, positions=poses,
                          bodyFeet=[5,5,6], expectedMechanicalSupport='UNADJUDICATED'))

    # Enclosure wall runs meet, rather than overlap, the four distinct corner towers.
    opening('main-gate', [55,65,0,5,0,15], 'main-gate')
    wall('outer-south','x',20,100,0,5,30,[openings[-1]['bounds']])
    wall('outer-north','x',20,100,115,120,30,[])
    wall('outer-west','y',20,100,0,5,30,[])
    wall('outer-east','y',20,100,115,120,30,[])
    # Main historical 403 panel retains its exact ID and bounds in the new registry.
    next(p for p in panels if p['id']=='outer-south-25-0')['id']='W01-SOUTH-WALL-X25-Z0'
    primitive('origin-ground-face',[0,120,0,120,0,0],'ground-face','enclosure',durability=False)
    regions.append(dict(id='courtyard',sourceBounds=[5,115,5,115],excludedStructures=['keep','tower-SW','tower-SE','tower-NW','tower-NE']))

    opening('keep-entry',[55,60,40,45,0,8])
    wall('keep-south','x',40,80,40,45,30,[openings[-1]['bounds']])
    wall('keep-north','x',40,80,75,80,30,[])
    wall('keep-west','y',45,75,40,45,30,[])
    wall('keep-east','y',45,75,75,80,30,[])
    floors('keep',[45,75,45,75],[0,15,30],lambda z: [] if z==0 else [[45,50,60,75]])
    for z in (0,15):
        for side,x0,x1 in [('west',45,55),('east',65,75)]:
            # Q23's room extents remain gross extents. A thin partition lies on the room side.
            px=(54.75,55) if side=='west' else (65,65.25)
            door=[px[0],px[1],47.5,52.5,z,z+8]
            opening(f'keep-{side}-room-door-{z}',door)
            for y in (45,50):
                for h in (0,5,10):
                    primitive(f'keep-room-{side}-{z}-side-{y}-{h}',[px[0],px[1],y,y+5,z+h,z+h+5],'partition-panel','keep',[door])
            for x in (x0,x0+5):
                for h in (0,5,10):
                    primitive(f'keep-room-{side}-{z}-north-{x}-{h}',[x,x+5,54.75,55,z+h,z+h+5],'partition-panel','keep')
            regions.append(dict(id=f'keep-room-{side}-{z}',sourceBounds=[x0,x1,45,55,z,z+15],grossDimensionsUnchanged=True,partitionInsideGrossFootprint=True))
        regions.extend([dict(id=f'keep-corridor-{z}',sourceBounds=[55,65,45,60,z,z+15]),dict(id=f'keep-transverse-{z}',sourceBounds=[45,75,55,60,z,z+15]),dict(id=f'keep-hall-{z}',sourceBounds=[50,75,60,75,z,z+15])])
        positions=[[45,55,z]]
        for i in range(30):
            top=z+(i+1)*.5; y=60+i*.5
            primitive(f'keep-tread-{z}-{i+1}',[45,50,y,y+.5,top-.25,top],'stair-tread','keep',durability=False)
            primitive(f'keep-riser-{z}-{i+1}',[45,50,y,y+.125,top-.5,top],'stair-riser','keep',durability=False)
            positions.extend([[45,55+i*.5,top],[45,55+(i+1)*.5,top]])
        positions.append([50,70,z+15])
        stairs.append(dict(id=f'keep-flight-{z}',count=30,treadFeet=.5,riseFeet=.5,widthFeet=5,
                           lowerLanding=[45,50,55,60,z],upperLanding=[50,55,70,75,z+15],
                           sourceGroundFlight=(z==0),roofConnectorBranchChoice=(z==15)))
        route(f'keep-flight-{z}','keep',positions,'ground-to-upper' if z==0 else 'upper-to-roof')
        route(f'keep-west-room-{z}','keep',[[55,47.5,z],[47.5,47.5,z]],'west room')
        route(f'keep-east-room-{z}','keep',[[60,47.5,z],[67.5,47.5,z]],'east room')
        route(f'keep-central-cross-{z}','keep',[[55,47.5,z],[60,47.5,z]],'connect both room entrances across central corridor')
        route(f'keep-stair-approach-{z}','keep',[[55,45,z],[55,55,z],[45,55,z]],'central and transverse corridors to stair')
        route(f'keep-hall-{z}','keep',[[55,55,z],[55,65,z],[65,65,z]],'north hall')
    route('keep-upper-return-to-stair','keep',[[50,70,15],[50,55,15],[45,55,15]],'connect both keep stair flights')
    route('keep-entry','keep',[[55,35,0],[55,45,0]],'courtyard to keep')
    route('keep-roof','keep',[[50,70,30],[65,70,30],[65,45,30],[45,45,30]],'roof access and clearance')
    route('403-A-movement','courtyard',[[25,10,0],[25,11,0],[25,6,0]],'unchanged 403 body/cargo sweep')
    route('courtyard-to-keep','courtyard',[[25,10,0],[55,10,0],[55,35,0]],'connect inherited actor pose to keep')

    # 20-square corner towers; wall thickness and 10-rise U stairs are geometry choices.
    for name,ox,oy in [('SW',0,0),('SE',100,0),('NW',0,100),('NE',100,100)]:
        g='tower-'+name; a,b=ox+2.5,oy+2.5
        east=ox==0
        # SW door accommodates the preserved B body at [15,10,0] without a wall overlap.
        entry=[ox+17.5,ox+20,oy+10,oy+15,0,8] if east else [ox,ox+2.5,oy+10,oy+15,0,8]
        opening(g+'-entry',entry)
        wall(g+'-south','x',ox,ox+20,oy,oy+2.5,40,[entry])
        wall(g+'-north','x',ox,ox+20,oy+17.5,oy+20,40,[entry])
        for side,x0,x1 in [('west',ox,ox+2.5),('east',ox+17.5,ox+20)]:
            for j in range(3):
                for z in range(0,40,5):
                    primitive(f'{g}-{side}-{j}-{z}',[x0,x1,oy+2.5+5*j,oy+7.5+5*j,z,z+5],'wall-panel',g,[entry])
        def transform_box(v):
            x0,x1,y0,y1,z0,z1=v
            return [ox+x0,ox+x1,oy+y0,oy+y1,z0,z1] if east else [ox+20-x1,ox+20-x0,oy+y0,oy+y1,z0,z1]
        def transform_pose(v):
            x,y,z=v
            return [ox+x,oy+y,z] if east else [ox+15-x,oy+y,z]
        def tower_part(id,v,kind,durability=False):
            primitive(g+'-'+id,transform_box(v),kind,g,durability=durability)
        for level in (0,10,20,30,40):
            for i in range(3):
                for j in range(3):
                    if level==0 or (i,j) in [(1,1),(2,2)]:
                        tower_part(f'floor-{level}-{i}-{j}',[2.5+5*i,7.5+5*i,2.5+5*j,7.5+5*j,max(0,level-.25),level],'floor-panel',True)
        for level in (0,10,20,30):
            # Four 5-ft-wide quarter flights around a 5x5 central floor.
            # A 1:2 rise/run ratio clears the next storey's landings for a 5x5x6 body.
            poses=[[12.5,12.5,level]]
            for leg in range(4):
                for i in range(10):
                    top=level+2.5*leg+(i+1)*.25
                    if leg==0:
                        v=[12.5-(i+1)*.5,12.5-i*.5,12.5,17.5,top-.25,top]
                        rise=[12.5-i*.5-.125,12.5-i*.5,12.5,17.5,top-.25,top]
                        pre=[12.5-i*.5,12.5,top];post=[12.5-(i+1)*.5,12.5,top]
                    elif leg==1:
                        v=[2.5,7.5,12.5-(i+1)*.5,12.5-i*.5,top-.25,top]
                        rise=[2.5,7.5,12.5-i*.5-.125,12.5-i*.5,top-.25,top]
                        pre=[2.5,12.5-i*.5,top];post=[2.5,12.5-(i+1)*.5,top]
                    elif leg==2:
                        v=[7.5+i*.5,8+i*.5,2.5,7.5,top-.25,top]
                        rise=[7.5+i*.5,7.625+i*.5,2.5,7.5,top-.25,top]
                        pre=[2.5+i*.5,2.5,top];post=[2.5+(i+1)*.5,2.5,top]
                    else:
                        v=[12.5,17.5,7.5+i*.5,8+i*.5,top-.25,top]
                        rise=[12.5,17.5,7.5+i*.5,7.625+i*.5,top-.25,top]
                        pre=[12.5,2.5+i*.5,top];post=[12.5,2.5+(i+1)*.5,top]
                    tower_part(f'tread-{level}-{leg}-{i}',v,'stair-tread')
                    tower_part(f'riser-{level}-{leg}-{i}',rise,'stair-riser')
                    poses.extend([pre,post])
                corner=[(2.5,12.5),(2.5,2.5),(12.5,2.5),(12.5,12.5)][leg]
                top=level+2.5*(leg+1)
                if leg<3:tower_part(f'landing-{level}-{leg}',[corner[0],corner[0]+5,corner[1],corner[1]+5,top-.25,top],'stair-landing')
                poses.append([*corner,top])
            route(f'{g}-stairs-{level}',g,[transform_pose(v) for v in poses],'tower ascent; z40 arrival exceeds inherited body bounds')
            stairs.append(dict(id=f'{g}-stairs-{level}',count=40,treadFeet=.5,riseFeet=.25,widthFeet=5,classification='TEST_ONLY tower geometry choice'))
            if level:
                route(f'{g}-floor-{level}',g,[transform_pose(v) for v in [[12.5,12.5,level],[12.5,7.5,level],[7.5,7.5,level]]],'central floor and landing')
        regions.append(dict(id=g,sourceBounds=[ox,ox+20,oy,oy+20,0,40],levels=[0,10,20,30,40],wallThicknessBranchFeet=2.5))
        route(g+'-entry',g,[transform_pose(v) for v in [[20,10,0],[12.5,10,0],[12.5,12.5,0]]],'courtyard entry below upper stair flight to ground landing')
    route('courtyard-loop','courtyard',[[25,10,0],[90,10,0],[90,90,0],[25,90,0],[25,10,0]],'connect all four courtyard quadrants around keep')
    route('to-SW','courtyard',[[25,10,0],[20,10,0]],'SW entry')
    route('to-SE','courtyard',[[90,10,0],[95,10,0]],'SE entry')
    route('to-NW','courtyard',[[25,90,0],[25,110,0],[20,110,0]],'NW entry')
    route('to-NE','courtyard',[[90,90,0],[90,110,0],[95,110,0]],'NE entry')
    leaves=[]
    for op in openings:
        id=op['id'];b=op['bounds'];z=b[4]
        if id=='main-gate':v=[55,65,2.25,2.5,15,30]
        elif id=='keep-entry':v=[50,55,39.75,40,0,8]
        elif 'room-door' in id:
            v=[49.75,54.75,47.375,47.5,z,z+8] if 'west' in id else [65.25,70.25,47.375,47.5,z,z+8]
        else:
            east='SW' in id or 'NW' in id
            v=[b[1],b[1]+5,b[3],b[3]+.125,z,z+8] if east else [b[0]-5,b[0],b[3],b[3]+.125,z,z+8]
        # Recesses are explicit geometry, not overlapping duplicate solid matter.
        for p in panels:p['occupiedFragments']=[piece for f in p['occupiedFragments'] for piece in cut(f,v)]
        leaves.append(dict(id=id+'-leaf',openingId=id,nominalBounds=v,occupiedFragments=[v],AC=op['AC'],HP=op['HP'],
                           pose='OPEN_TEST_ONLY_STATIC',loadBearingDependencies=None))
    model=dict(id='PG328-W01-GEOMETRY-405',classification='AUTHORIZED_TEST_ONLY_GEOMETRY_ONLY_NO_SEAL',
               sourceCommit=COMMIT,sourceBindings=bindings,worldBounds=[0,120,0,120,0,40],
               geometryChoices=dict(towerWallThicknessFeet=2.5,outerWallThicknessFeet=5,keepWallThicknessFeet=5,
                    floorAndTreadThicknessFeet=.25,roomPartitionThicknessFeet=.25,
                    towerPlacement='Four literal 20x20 corner footprints; 5-ft enclosure wall runs meet their faces.',
                    roomExtents='Printed 10x10 gross footprints retained; thin internal partition occupies the room side. No claim of 10x10 clear interior.',
                    stairs='Thirty specified ground-to-upper keep treads unchanged. Separate upper-to-roof connector in the same reserved well is a branch geometry choice. Tower treads and landings are branch geometry.',
                    stepMotion='Swept body clearance only; step-up geometry is not a new movement budget, support rule, climbing rule or permission.'),
               panels=panels,openings=openings,doorLeaves=leaves,regions=regions,stairFlights=stairs,navigationPaths=paths,
               bodyAndCargo=dict(bodyFeet=[5,5,6],positionConvention='minimum x/y and feet z',
                  cargoRelativeBounds={'focus-A':[0,.5,0,.5,3,3.5],'pack-A':[.5,1,0,.5,3,3.5],'cargo-A':[1,2,0,1,3,4],'PG328-W01-403:CLAY-TILE-1':[2,3,1,2,3,3.25]},
                  local403TileRelativeBounds=[0,1,-1,0,0,.25],
                  scope='All four 403 carried objects included. The tile keeps its exact 1x1x0.25 size; its unchanged attack/courtyard pose is checked separately. Whole-map routes use an explicit TEST_ONLY hand-carry pose inside the body envelope, without changing identity or custody. No reposition, movement, free interaction, temporal traversal or extended tile lifetime is awarded; this is a static clearance certificate.'),
               mechanicalSupport=dict(status='UNADJUDICATED',contactsAreLoadBearing=False,collapseSimulated=False),
               stateChange=dict(parentMutated=False,actorMoved=False,castsOrDamageAdded=False,W02Constructed=False,queueChanged=False,acceptedIds=[],appliedIds=[],applicationAuthorized=False))
    (OUT/'GEOMETRY_405.json').write_bytes(encode(model))
    (OUT/'SOURCE_BINDINGS_405.json').write_bytes(encode(dict(commit=COMMIT,bindings=bindings)))
    print(json.dumps(dict(panels=len(panels),openings=len(openings),routes=len(paths),path=str(OUT/'GEOMETRY_405.json'),sha256=sha(encode(model)))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-cache',type=Path,required=True)
    build(p.parse_args().source_cache)
