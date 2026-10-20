"""One-shot independent reproduction of inactive Mend reducers and expiry loss."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from datetime import datetime, timezone
import json, sys, zipfile

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
OUT=A/'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json'
assert not OUT.exists(), 'Preserve completed evidence'
sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'tools'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
archive=A/'DD_Feat335_Copy_Classes_01.zip';bindings=[]
assert info(archive)['sha256']=='6d3e0d415576a6481fbe3072af4473ada373cb22e90cefab460c077f77ce1626'
with zipfile.ZipFile(archive) as z:
    for n in z.namelist():
        if n.startswith('sources/') and n.endswith('.py'):
            p=G/n.removeprefix('sources/');assert p.read_bytes()==z.read(n);bindings.append(info(p))
from feat335_copy_payload_fixtures import CopyPayloadFixtures
from healing_playtest_rules import HealingReduction, healing_packet
from form_temphp_playtest_rules import BufferGrant
from control_playtest_rules import ClockMarker
f=CopyPayloadFixtures();cases=[]
for present,suppressed in [(False,False),(True,True)]:
    m=f.make();f.start(m);f.capture(m,'mend');f.declare(m,'mend')
    reducer=HealingReduction('old','actual-reducer','flat',1,present=present,suppressed=suppressed,next_healing=True)
    actor=m.world.actors['target'];actor['healingReductions']=[reducer]
    expected=healing_packet(actor['life'],2,dice_count=2,reductions=[reducer])
    assert expected['state'].hp==32 and expected['nextHealingCandidates']==[]
    before=m.snapshot()
    try:m.resolve('cast',rolls={'nativeDice':[4,4]})
    except ValueError as e:error=str(e)
    else:raise AssertionError('Inactive reducer defect was not reproduced')
    assert m.snapshot()==before and actor['life'].hp==30
    cases.append({'id':'LOCAL-COPY-INACTIVE-MEND-'+('ABSENT' if not present else 'SUPPRESSED'),
        'status':'defect-reproduced','premise':'Existing paid Wizard Mend fixture with an explicitly absent or suppressed prior next-healing reducer; valid pending paid declaration and nativeDice [4,4].',
        'reducer':{'application_id':'old','group':'actual-reducer','kind':'flat','value':1,'present':present,'suppressed':suppressed,'next_healing':True},
        'expectedByExistingHealingHelper':{'hp':32,'nextHealingCandidates':[]},
        'actual':{'hp':actor['life'].hp,'error':error,'failureAtomic':True},
        'finding':'The copy adapter rejects every next_healing record without filtering present/suppressed state. Existing healing arithmetic correctly ignores the inactive record. Active next-healing consumption remains a separate explicitly unimplemented adapter.'})
m=f.make();f.start(m)
grant=BufferGrant('actual-prior-overflow','oracle.supplement.life.overflowing-light','prior-owner','target',5,
    expiry=ClockMarker(12),riders={'overflowing-cleanse'})
m.world.buffers.offer(grant,m.world.now);m.world.projection()
preview=deepcopy(m.world.buffers);expected=preview.expire(ClockMarker(12))
assert len(expected)==1 and expected[0]['chooseUpTo']==1
returned=m.world.advance(ClockMarker(12),[m])
second=m.world.buffers.expire(ClockMarker(12))
assert returned is None and second==[] and m.world.buffers.grants[grant.grant_id].state=='natural-expiry'
cases.append({'id':'LOCAL-COPY-SHARED-BUFFER-EXPIRY-01','status':'defect-reproduced',
    'premise':'A conditionally already legally established Oracle Overflowing Light buffer shares the canonical BufferLedger with the copy world:5 temporary HP, remaining at its supplied actual deadline12, with its actual source-specific overflowing-cleanse rider. This fixture does not implement Oracle acquisition or grant a new cleanse.',
    'expectedNaturalExpiryInstructions':expected,'actualAdvanceReturn':returned,'secondExpiryInstructions':second,
    'finalGrantState':m.world.buffers.grants[grant.grant_id].state,'finalTempHp':m.world.actors['target']['life'].temp_hp,
    'finding':'CopyPayloadWorld.advance discards the existing BufferLedger.expire return value after it irreversibly ends the shared buffer. The real expiry benefit cannot be recovered by a later expiry call.',
    'qualification':'The proper downstream receiver must still choose/apply an actually eligible condition removal. This diagnosis proves instruction loss, not a missing free automatic cleanse.'})
assert bindings==[info(G/b['path']) for b in bindings]
report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'two-additional-defect-groups-reproduced-in-three-cases',
    'previousIndependentDiagnostics':info(A/'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json'),
    'script':info(Path(__file__)),'sourceArchive':info(archive),'sourceBindings':bindings,'unchangedArchivedPythonFiles':len(bindings),
    'cases':cases,'additionalDefectGroups':2,'totalLocallyReproducedDefectGroupsAcrossReceipts':6,
    'relationshipToGPT':'Prompted by the active Part5 interim report. Exact final fixes and its claimed47 adversarial tests have not been received or independently verified.',
    'limits':['Conditional local reference-helper tests only. No project-engine runtime or human gameplay test.',
              'No correction or new rule selected; no canonical/index/registry edits.',
              'Owner-reserved later implementation remains in force.'],
    'implementationApplied':False,'sourceInformationDeleted':0}
with OUT.open('xb') as handle:handle.write((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps({'receipt':info(OUT),'additionalDefectGroups':2,'cases':3,'unchangedPythonSources':38}))
