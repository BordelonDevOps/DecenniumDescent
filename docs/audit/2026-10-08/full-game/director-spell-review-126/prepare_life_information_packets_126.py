"""Fresh data-only assembly from verified sources; no supplied code execution."""
from pathlib import Path, PurePosixPath
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent'); A=G/'docs/audit/2026-10-08/full-game'; D=A/'director-spell-review-126'
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def bind(n,b): return dict(path=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
with zipfile.ZipFile(A/'DD_Transport6_Director_Conference_126.zip') as z:
    manifest=json.loads(z.read('MANIFEST.json'))
    assert z.testzip() is None
    for r in manifest['files']: assert bind(r['path'],z.read(r['path']))==r
    common={n:z.read(n) for n in z.namelist() if n.startswith(('accepted-context/','current/','APPLICATION_','CURRENT_SPELL_QUEUE_126'))}
    boundary=z.read('README.md').decode().split('Current applied baseline',1)[1].split('\n\nSelect full',1)[0]
configs=[
    ('LifeMatter5','DD_Life_Matter_5_Conference_01.zip','LIFE_MATTER5_NEXT_CONFERENCE_NOTES_126.json','Review Awaken, Bone Cage, Contagion, Disintegrate and Telekinesis after MagicModifiers7. Preserve five original proposals, ten original scenarios and fourteen original questions plus six independent followups (20 total). Resolve real Beast/shrub lifecycle, full supported cage geometry and suppression, actual oral disease-cure delivery, the inherited Null override on damage-caused disintegration, and complete Telekinesis body/cargo paths, holders and hinge rotation.'),
    ('Information8','DD_Information_8_Conference_01.zip','INFORMATION8_NEXT_CONFERENCE_NOTES_126.json','Review Arcane Eye, Concordant Mindlink, Faction Prophecy, Faction Destiny, Find the Path, Legend Lore, Prophetic Frenzy and Resonance Prophecy after LifeMatter5. Preserve eight original proposals, sixteen original scenarios and eighteen original questions plus seven independent followups (25 total). Resolve actual school-qualified protection/sensing, finite sensor geometry, roster/send clocks, real institutional and route/lore premises, permitted outcome views/Reaction/lineage, and the substantial source-promise change and remote-arrival timing in Resonance Prophecy.')
]
for label,original,notes_name,intro in configs:
    notes=json.loads((D/notes_name).read_text()); files=dict(common)
    original_path=A/original; original_bytes=original_path.read_bytes()
    with zipfile.ZipFile(original_path) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in z.namelist())
    files['original/'+original]=original_bytes
    files['INDEPENDENT_QUESTIONS_126.json']=(D/notes_name).read_bytes()
    files['README.md']=(f'# {label} director conference126 — prepared, not sent\n\n'+intro+'\n\nCurrent applied baseline'+boundary+'\n\nThe independent questions are requests, not adopted rules. No pending packet is authority solely because it exists. Director-authored fixture facts must be labeled as new encounter prerequisites and retain content/world holds. Do not silently substitute a simpler positive for an unavailable original obligation. Return all question dispositions, complete selected procedures, source-qualified actors/costs/timelines/geometry, original-scenario mapping, adverse branches, complete MODEL and CASEBOOK, original-source history, full-value forward/inverse operations, retained holds and a verified downloadable archive. Execute no supplied or historical programs. No new acceptance, canonical application, game execution or numerical balance claim follows from this input packet.\n').encode()
    manifest=dict(id=label.upper()+'-DIRECTOR-CONFERENCE-126',status='PREPARED_NOT_SENT',identities=notes['identities'],files=[bind(n,b) for n,b in sorted(files.items())])
    files['MANIFEST.json']=enc(manifest); out=A/f'DD_{label}_Director_Conference_126.zip'; assert not out.exists()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n,b in files.items(): z.writestr(n,b)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for r in manifest['files']: assert bind(r['path'],z.read(r['path']))==r
    rec=dict(id=manifest['id'],status='PREPARED_NOT_SENT',archive=bind(str(out),out.read_bytes()),members=len(files),manifestBindings=len(manifest['files']),questionCount=notes['totalQuestionCount'],originalScenarioCount=notes['originalScenarioCount'],body8AcceptanceIncluded=True,canonicalChanges=False,runtimeExecuted=False)
    (D/f'{label.upper()}_PACKET_126.json').write_bytes(enc(rec)); print(json.dumps(rec))

qpath=A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_126.json'; q=json.loads(qpath.read_text())
for g in q['groups']:
    mapping={'transport6':('TRANSPORT6',None),'magic-modifiers7':('MAGICMODIFIERS7',None),'life-matter5':('LIFEMATTER5','LIFE_MATTER5_NEXT_CONFERENCE_NOTES_126.json'),'information8':('INFORMATION8','INFORMATION8_NEXT_CONFERENCE_NOTES_126.json')}
    if g['group'] in mapping:
        label,n=mapping[g['group']]; g['currentPhase']='current-director-packet-prepared-126-unsent';g['currentPacket']=str(D/f'{label}_PACKET_126.json')
        if n: g['independentPreconferenceReview']=str(D/n)
qpath.write_bytes(enc(q))
