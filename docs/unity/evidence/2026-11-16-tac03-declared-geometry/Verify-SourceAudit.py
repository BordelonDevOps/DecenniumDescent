"""Reproduce pinned source/API findings. No C# execution or gameplay qualification."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = 'fd422433bb83b72bed88e6e62c98fe2c901c659b'
ENGINE = '2733b9fd75e2159ad73312b9583311693b925598'
SOURCE = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
CODE = 'engine/com.decennium.foundation/'
RB = 'DescentReviewChanges/ReviewBible/docs/mechanics/'
PRIOR = 'docs/unity/evidence/2026-11-16-tac10-undead-contract/'
BISHOP = 'docs/unity/evidence/2026-11-16-chr03-bishop-runtime/'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def write(name, value):
    (PACKET / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


def main():
    assert not git('diff', ENGINE, '--', 'engine').strip(), 'Engine changed before contract review'
    cs = [p for p in git('ls-tree', '-r', '--name-only', ENGINE, '--', CODE).decode().splitlines() if p.endswith('.cs')]
    sources = {p: BASELINE for p in [
        'CANON_MANIFEST.md', 'docs/canon/CANON_MANIFEST.json', 'docs/canon/REPOSITORY_PROMOTION.md',
        'engine/AGENTS.md', 'docs/unity/DEVELOPMENT_BRIEF.md',
        'docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json',
        'docs/unity/MOVEMENT_AND_UNARMED_RULE_DECISIONS.md',
        'docs/unity/EXPLORATION_MOVEMENT_RULE_DECISIONS.md',
        'docs/unity/SHARED_WORLD_RULE_DECISIONS.md', 'docs/unity/CONNECTED_COMBAT_RULE_DECISIONS.md',
        'docs/unity/OVERWATCH_RULE_DECISIONS.md',
        PRIOR+'GPT_SOURCE_API_REVIEW.json', PRIOR+'SOURCE_API_DECISIONS.md',
        BISHOP+'GPT_FINAL_REVIEW.json', BISHOP+'final/FINAL_RECONCILIATION.json',
        BISHOP+'final/qualification-evidence.zip',
        'docs/unity/evidence/2026-11-16-exp07-post-recovery/APPROVED_CONTRACT.md',
    ]}
    for p in ['COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md']:
        sources[RB+p] = SOURCE
    patterns = {
        'fixed-walkable': r'TestOnlyPolicy\.Walkable',
        'explicit-map-bounds': r'ObservationMapWidth|ObservationMapHeight|p\[0\]\s*<\s*5|p\[1\]\s*<\s*5|x\s*<\s*5\s*&&\s*y',
        'spatial-consumers': r'ObservationGeometry\.|WorldSpatialQueries\.|PlanarCombatGeometry\.|CostPerFoot|terrain\.At\(|tactical\.At\(',
        'profile-save-gates': r'BishopEntrySchema|BishopProfile\.|ConnectedExplorationObservation\.|ContentFingerprint\.StartsWith|SelectedFingerprint\(',
    }
    texts = {p: (ROOT/p).read_text(encoding='utf-8-sig') for p in cs}
    searches = {}
    for label, pattern in patterns.items():
        rows = []
        for p in cs:
            if '/Tests/' in p:
                continue
            hits = [dict(line=i+1, text=line.strip()) for i, line in enumerate(texts[p].splitlines()) if re.search(pattern, line)]
            if hits:
                rows.append(dict(path=p, hits=hits))
                sources[p] = ENGINE
        searches[label] = dict(pattern=pattern, excludesTests=True, matchedFiles=len(rows),
                               matchedLines=sum(len(x['hits']) for x in rows), rows=rows)
    extra = [
        'Runtime/Core/Simulation.cs', 'Runtime/Core/ObservationRecords.cs',
        'Runtime/Core/WorldPositionResolver.cs', 'Runtime/Core/WorldActivityRecord.cs',
        'Runtime/Core/TacticalMovementRecords.cs', 'Runtime/Core/BishopEntryRecords.cs',
        'Runtime/Core/PostRecoveryEncounterRecords.cs', 'Runtime/Core/PostRecoveryEncounterValidation.cs',
        'Runtime/Persistence/SnapshotCodec.cs', 'Runtime/Persistence/ObservationCodec.cs',
        'Laboratory/Model/TestOnlyPolicy.cs', 'Laboratory/Model/ObservationGeometry.cs',
        'Laboratory/Model/ObservationRules.cs', 'Laboratory/Model/PlanarCombatGeometry.cs',
        'Laboratory/Model/PlaytestCombatBudgets.cs', 'Laboratory/Model/PrototypeTraversal.cs',
        'Laboratory/Model/ConnectedExpeditionSession.cs', 'Laboratory/Model/ConnectedExpeditionView.cs',
        'Laboratory/Model/SharedWorldCombatPolicy.cs',
        'Laboratory/Model/LaterDefenderController.cs',
        'Tests/EditMode/TacticalMovementCases.cs', 'Tests/EditMode/SharedWorldCases.cs',
        'Tests/EditMode/OverwatchExecutionCases.cs', 'Tests/EditMode/BishopEntryCases.cs',
    ]
    for p in extra:
        sources[CODE+p] = ENGINE
    payload = ''.join(rev+':'+p+'\n' for p, rev in sorted(sources.items())).encode()
    batch = subprocess.run(['git','cat-file','--batch'], input=payload, cwd=ROOT,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    pos, blobs, bindings = 0, {}, []
    for p, rev in sorted(sources.items()):
        end = batch.stdout.index(b'\n', pos)
        header = batch.stdout[pos:end].decode().split()
        assert len(header)==3 and header[1]=='blob', (p, header)
        size = int(header[2]); pos = end+1
        raw = batch.stdout[pos:pos+size]; pos += size+1
        local = (ROOT/p).read_bytes()
        assert raw==local or raw==local.replace(b'\r\n', b'\n'), p
        blobs[p] = raw
        bindings.append(dict(path=p, revision=rev, gitBlob=header[0], bytes=size,
            sha256=hashlib.sha256(raw).hexdigest(), checkoutRelation='exact' if raw==local else 'CRLF-only'))
    assert pos==len(batch.stdout) and not batch.stderr
    text = lambda p: blobs[p].decode('utf-8-sig')
    code = lambda p: text(CODE+p)
    checks = []
    def check(name, value):
        assert value, name
        checks.append(dict(name=name, passed=True))
    review = json.loads(text(PRIOR+'GPT_SOURCE_API_REVIEW.json'))
    check('Actual review selects separate geometry before creature runtime',
          review['responseId']=='2d01541e-6b9d-54c0-88a7-0db0f65bc6af'
          and 'separate, bounded TAC-03' in review['actualResponse'])
    mapping = json.loads(text('docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json'))
    item = lambda key: next(x for x in mapping['workItems'] if x['id']==key)
    check('Dependency edges retained', item('TAC-03')['dependencies']==['CHR-01','TAC-01']
          and item('TAC-10')['dependencies']==['TAC-03','TAC-04','TAC-05','TAC-02']
          and item('CHR-05')['dependencies']==['CHR-03','TAC-02','TAC-05','TAC-08'])
    combat = text(RB+'COMBAT_ACTION_PLAYTEST.md')
    check('Source equal five-foot orthogonal and diagonal metric', 'each orthogonal or diagonal neighboring tile is 5 ft' in combat)
    check('Source two blocked sides forbid corner cut', 'both adjacent orthogonal sides are completely blocked' in combat)
    check('Source terrain strength and additive crawl preserved', 'normal/difficult/severe terrain costs 1/2/3' in combat and 'Add +1 for crawling and +1 for squeezing' in combat)
    check('Source perception and effect separate', 'Keep **visibility**, **known location**, and **line of effect** separate' in combat)
    check('Source areas use origin and obstruction', "For areas, evaluate line/cover from the area's origin" in combat)
    check('Legacy fixed floor remains explicit', 'x >= 0 && x < 5 && y >= 0 && y < 5 && !(x == 2 && y == 1)' in code('Laboratory/Model/TestOnlyPolicy.cs'))
    check('World floor intersects fixed map', '=> TestOnlyPolicy.Walkable(x, y) &&' in code('Laboratory/Model/SharedWorldCommandQueries.cs'))
    check('Tactical floor intersects fixed map', 'TestOnlyPolicy.Walkable(px,py)' in code('Laboratory/Model/TacticalMovementPolicy.cs'))
    check('World and tactical costs already share destination terrain pattern',
          'terrain.At(edge.ToX, edge.ToY)' in code('Laboratory/Model/TestOnlySharedWorldPolicy.cs')
          and 'tactical.At(x,y)' in code('Laboratory/Model/TacticalMovementPolicy.cs'))
    check('Ordinary movement stays cardinal', 'WorldSpatialQueries.Neighbor(0, 0, dx, dy, false)' in code('Laboratory/Model/SharedWorldCommandQueries.cs'))
    check('Tactical movement has diagonal corner evaluation', 'x,y,true,true,' in code('Laboratory/Model/TacticalMovementPolicy.cs'))
    geometry = code('Laboratory/Model/ObservationGeometry.cs')
    check('Declared map bounds already limited to64', 'width > 64' in geometry and 'height > 64' in geometry)
    check('Anchor restriction uses all three channels', all('&& !Blocks(x, y, ObservationChannel.'+x+')' in geometry for x in ['Sight','Effect','Movement']))
    check('Exact sight algorithm explicitly selected by normal observation enable',
          '=> EnableObservation(fixture, ObservationAlgorithmVersion.ExactPathIntervalsV2)' in code('Laboratory/Model/SharedWorldCombatPolicy.cs'))
    layout = code('Runtime/Core/ConnectedExplorationObservation.cs')
    check('Connected validator independently hardcodes legacy map', 'state.ObservationMapWidth != 5' in layout and 'cells.Length != 1' in layout)
    validation = code('Runtime/Core/ObservationRecords.cs')
    check('Existing validator rejects unsupported blocker anchors and traversal endpoints',
          '(x.BlocksSight || x.BlocksEffect || x.BlocksMovement)' in validation and 's.WorldTraversals.Any' in validation)
    check('Shared occupancy includes destination reservations', 'state.WorldTraversals.Any(edge => edge.ActorId != actorId' in code('Laboratory/Model/SharedWorldDefinitions.cs'))
    check('Mining placement has independent literal bounds', 'p[0]<5&&p[1]<5' in code('Laboratory/Model/SharedMining.cs'))
    check('Route endpoints independently require fixed map', '!TestOnlyPolicy.Walkable(leg.FromX, leg.FromY)' in code('Laboratory/Model/SharedExpeditionRouteTravel.cs'))
    check('Camp access independently requires fixed map', '!TestOnlyPolicy.Walkable(site.RouteX, site.RouteY)' in code('Laboratory/Model/SharedExpeditionCampUse.cs'))
    check('Trap anchor independently requires fixed map', '!TestOnlyPolicy.Walkable(definition.AnchorX,definition.AnchorY)' in code('Laboratory/Model/SharedHuntingTrap.cs'))
    check('Push destination independently requires fixed map', 'TestOnlyPolicy.Walkable(toX,toY)' in code('Laboratory/Model/SharedOverwatchExecution.cs'))
    check('Controller distinguishes resident static map and seen occupancy',
          'seen.Any(actor => actor.X == x && actor.Y == y)' in code('Laboratory/Model/SharedLaterDefenderDecision.cs')
          and 'Dynamic occupancy and reservations are visible only through direct sight' in code('Laboratory/Model/SharedLaterDefenderDecision.cs'))
    check('Connected interface currently excludes ranged and Overwatch payloads',
          'command.Ranged != null || command.OverwatchRider != OverwatchRider.None' in code('Laboratory/Model/ConnectedExpeditionSession.cs'))
    check('No automatic observation plus authored route composition', 'RouteObservationIntegrationUnsupported' in code('Laboratory/Model/SharedWorldCombatPolicy.cs'))
    check('Accepted engine unchanged', not git('diff', ENGINE, '--', 'engine').strip())
    archive = BISHOP+'final/qualification-evidence.zip'
    member = 'qualification/reference/second-rest.ddsave.Player.view.json'
    with zipfile.ZipFile(ROOT/archive) as z:
        raw = z.read(member)
    view = json.loads(raw)
    check('Accepted archived view is TestOnly and actual second-rest revision218', view['TestOnly'] and view['Revision']==218)
    matching = [x['Id'] for x in view['Items'] if any(word in x['Id'].lower() for word in ['crossbow','bolt','overwatch'])]
    check('Selected archived item view contains no crossbow bolt or Overwatch identities', not matching)
    write('SOURCE_BINDINGS.json', dict(baseline=BASELINE, acceptedEngine=ENGINE, sourceRevision=SOURCE, sources=bindings))
    write('API_CONSUMERS.json', dict(searchedTrackedCsharpFiles=len(cs), searches=searches,
          limits='Lexical candidate inventory, with inspected behavior recorded in the contract. Not a semantic completeness proof. Unity host rows are inventory only; Unity qualification is deferred.'))
    write('SOURCE_EXTRACTS.json', dict(selectedRules={p:text(p) for p in sources if p.startswith(RB)},
          archivedPublicView=dict(archive=archive, member=member, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
             revision=view['Revision'], testOnly=view['TestOnly'], matchingItemIds=matching,
             limitation='Item-name absence is descriptive only. The explicit session payload restriction establishes the relevant public interface exclusion; no source-grant absence is inferred from item names.'),
          scope='Pinned source evidence only. Proposals require actual review and later runtime qualification.'))
    report = dict(status='PASS_SOURCE_API_AUDIT_RUNTIME_NOT_AUTHORIZED', baseline=BASELINE, acceptedEngine=ENGINE,
          sourceRevision=SOURCE, pinnedBlobs=len(bindings), searchedTrackedCsharpFiles=len(cs),
          searchCounts={k:dict(files=v['matchedFiles'], lines=v['matchedLines']) for k,v in searches.items()},
          checks=checks, engineUnchanged=True, newCompilation=False, newGameplay=False, runtimeAuthorized=False,
          nextGate='Actual GPT review of complete bounded TAC-03 declaration, compatibility, context and evidence allocation contract')
    write('SOURCE_AUDIT.json', report)
    print(json.dumps({k:v for k,v in report.items() if k!='checks'} | dict(checks=len(checks))))


if __name__ == '__main__':
    main()
