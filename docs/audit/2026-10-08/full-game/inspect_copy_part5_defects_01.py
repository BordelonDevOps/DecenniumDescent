"""One-shot local diagnostic receipt; does not modify any gameplay source."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from copy import deepcopy
import json
import sys
import zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json'
assert not OUT.exists(), 'Preserve successful diagnostic evidence'
sys.dont_write_bytecode = True
sys.path.insert(0, str(R / 'tools'))

def binding(path):
    raw = path.read_bytes()
    return {'file': str(path.relative_to(G)).replace('\\', '/'),
            'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}

archive = A / 'DD_Feat335_Copy_Classes_01.zip'
assert binding(archive)['sha256'] == '6d3e0d415576a6481fbe3072af4473ada373cb22e90cefab460c077f77ce1626'
bindings = []
with zipfile.ZipFile(archive) as z:
    for name in z.namelist():
        if name.startswith('sources/') and name.endswith('.py'):
            p = G / name.removeprefix('sources/')
            assert p.read_bytes() == z.read(name), name
            bindings.append(binding(p))

from feat335_copy_class_fixtures import ClassCopyFixtures
from feat335_copy_class_release import SharedClassWallet, ClassCopyPayloadReleases

f = ClassCopyFixtures()
cases = []

m, _ = f.class_make('Mirrorsage')
before = {'captureReactions': m.captures.reactions, 'canonicalReaction': m.pool['reaction']}
f.capture_class(m, 'strike', sid='eldritch_echo')
after_capture = {'captureReactions': m.captures.reactions, 'canonicalReaction': m.pool['reaction']}
SharedClassWallet(m.pool).pay(action='reaction')
assert after_capture == {'captureReactions': 0, 'canonicalReaction': True}
assert m.pool['reaction'] is False
cases.append({'id': 'LOCAL-COPY-REACTION-01', 'status': 'defect-reproduced',
    'premise': 'Existing paid level-12 Mirrorsage fixture; actual legal Eldritch Echo capture; one initially available ordinary Reaction.',
    'actions': ['Capture witnessed strike through Eldritch Echo.', 'Pay another Reaction through SharedClassWallet using the same owner pool.'],
    'before': before, 'afterCapture': after_capture, 'secondReactionPaymentAccepted': True,
    'finding': 'Copy capture consumes its private Reaction counter but leaves the canonical class wallet Reaction available.',
    'code': ['tools/feat335_copy_capture.py:147', 'tools/feat335_copy_class_release.py:168']})

m, s = f.class_make('Shaman', shaman=True)
f.capture_class(m, 'mend'); f.declare_class(m, 'mend')
s.actors['owner']['body']['conscious'] = False
before_hp = m.world.actors['target']['life'].hp
result = m.resolve('cast', rolls={'nativeDice': [4, 4]})
assert result['resolved'] and before_hp == 30 and m.world.actors['target']['life'].hp == 32
cases.append({'id': 'LOCAL-COPY-RESOLUTION-BODY-01', 'status': 'defect-reproduced',
    'premise': 'Actual integrated Shaman fixture with paid live totem; legal Mend capture and paid declaration, followed by canonical unconsciousness before resolution.',
    'actions': ['Declare Mend with initially conscious canonical body.', 'Set the actual Shaman body conscious=False as the intervening event.', 'Resolve with nativeDice=[4,4].'],
    'canonicalConscious': s.actors['owner']['body']['conscious'],
    'copyWorldConscious': m.world.actors['owner']['conscious'],
    'hpBefore': before_hp, 'hpAfter': m.world.actors['target']['life'].hp, 'result': result,
    'finding': 'Resolution reads a separate stale copy-world body after class commitment had validated the canonical Shaman body.',
    'code': ['tools/feat335_copy_class_release.py:49', 'tools/feat335_copy_payloads.py:217']})

m, s = f.class_make('Shaman', shaman=True)
f.capture_class(m, 'step')
selection = f.selection('step'); selection.update(destination=[-15, 0, 0], distanceFeet=15)
before = {'copyPosition': deepcopy(m.world.actors['owner']['position']),
          'classPosition': deepcopy(s.actors['owner']['position3d']),
          'auraPosition': s.actors['owner']['positionFeet'], 'aura': s._qualifying_aura('owner')}
m.declare('cast', 'capture', permission='pending', grant_id='Shaman/class-engine', frame=f.frame(m), selection=selection)
result = m.resolve('cast')
after = {'copyPosition': deepcopy(m.world.actors['owner']['position']),
         'classPosition': deepcopy(s.actors['owner']['position3d']),
         'auraPosition': s.actors['owner']['positionFeet'], 'aura': s._qualifying_aura('owner')}
assert result['resolved'] and after['copyPosition'] == [-15, 0, 0]
assert after['classPosition'] == [0, 0, 0] and after['aura'] == 'totem'
cases.append({'id': 'LOCAL-COPY-STEP-AURA-01', 'status': 'defect-reproduced',
    'premise': 'Actual integrated Shaman fixture; stationary own totem at x=5, radius=15; visible lawful personal teleport from x=0 to x=-15 with supplied physical eligibility.',
    'actions': ['Capture Step.', 'Declare the supplied lawful 15-foot destination [-15,0,0].', 'Resolve Step without RNG.'],
    'before': before, 'after': after, 'totemPosition': s.totems['totem']['positionFeet'],
    'distanceAfterActualStep': 20, 'auraRadius': 15,
    'finding': 'Copy-world movement succeeds while canonical class coordinates and the aura query retain the former position, wrongly retaining the qualifying aura.',
    'code': ['tools/feat335_copy_payloads.py:311', 'tools/di7_shaman_transactions.py:84', 'tools/di7_area_geometry.py:104']})

m, s = f.class_make('Shaman', shaman=True)
f.capture_class(m, 'mend', adapt=True)
m.pool['actions'] = 2  # Explicit upstream lawful extra Action premise, not a grant by copy.
f.declare_class(m, 'mend'); m.resolve('cast', rolls={'nativeDice': [4, 4]})
n = ClassCopyPayloadReleases(m.captures, m.owner, m.pool, m.cadence,
    m.lifecycle.ledger, m.world, action_account=m.action_account)
f.declare_class(n, 'mend', event='second', permission='adapted')
assert m.release_rounds == n.release_rounds == {1} and m.pool['actions'] == 0
cases.append({'id': 'LOCAL-COPY-DUPLICATE-ADAPTER-01', 'status': 'integration-guard-gap-reproduced',
    'premise': 'Actual integrated Shaman fixture, one independently lawful extra Action, paid unexpired adapted permission, two constructed adapters sharing the same capture/resource/action/world/concentration objects.',
    'actions': ['Commit and resolve one Mend in numbered round 1.', 'Construct a second adapter for that same owner and shared state.', 'Commit a second adapted Mend in numbered round 1.'],
    'firstAdapterRounds': sorted(m.release_rounds), 'secondAdapterRounds': sorted(n.release_rounds),
    'remainingActions': m.pool['actions'], 'secondCost': n.casts['second']['quote']['cost'],
    'finding': 'The per-owner copy limit is stored per adapter; construction permits a second instance with an empty cap ledger. Either enforced ownership/singleton registration or a shared owner ledger is required at the integration boundary.',
    'qualification': 'This intentionally exercises duplicate adapter construction. It does not claim that a production scheduler currently creates duplicates; no production scheduler was exercised.',
    'code': ['tools/feat335_copy_release.py:148', 'tools/feat335_copy_class_release.py:37']})

assert bindings == [binding(G / b['file']) for b in bindings]
report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'status': 'four-local-reference-helper-findings-reproduced',
    'sourceArchive': binding(archive), 'sourceBindings': bindings,
    'allArchivedPythonSourcesStillExact': True, 'sourcePythonFiles': len(bindings),
    'cases': cases,
    'relationshipToGPT': 'Independent local investigation prompted by the active Part 5 copied-feat review. Its final package has not yet been received; findings do not select a correction.',
    'limits': ['Conditional fixtures and reference Python helpers only.',
               'No project-engine runtime, human gameplay or balance validation.',
               'No gameplay source, canonical procedure, index or registry was edited.',
               'The owner reserved later implementation; all corrections remain unapplied.'],
    'implementationApplied': False, 'sourceInformationDeleted': 0}
with OUT.open('x', encoding='utf-8', newline='\n') as handle:
    handle.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'receipt': binding(OUT), 'confirmedFindings': len(cases), 'unchangedPythonSources': len(bindings)}))
