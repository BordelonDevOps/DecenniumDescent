"""Fresh data-only packet assembly. Does not import or execute project code."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile, io

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
D=A/'director-spell-review-126'
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def safe(z):
    ns=z.namelist()
    assert len(ns)==len(set(ns)) and z.testzip() is None
    assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n for n in ns)
def bind(path,b): return dict(path=path,bytes=len(b),sha256=sha(b))

queue_path=A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_126.json'
queue=json.loads(queue_path.read_text(encoding='utf-8-sig'))
queue['scope']='Current navigation with exact Body8 authored acceptance recorded by receipt126. Original source queue and source archives preserved; no canonical application or runtime execution.'
queue['nextSuggestedGroups']=['time-cast5','transport6','magic-modifiers7','material-terrain8']
queue_path.write_bytes(enc(queue))
source=A/'DD_Transport6_Director_Conference_125.zip'
with zipfile.ZipFile(source) as z:
    safe(z)
    oldmanifest=json.loads(z.read('MANIFEST.json'))
    for r in oldmanifest['files']:
        assert bind(r['path'],z.read(r['path']))==r
    original={n:z.read(n) for n in z.namelist() if n!='MANIFEST.json'}

receipt_path=D/'BODY8_EXACT_ACCEPTANCE_126.json'
receipt=json.loads(receipt_path.read_text())
body_path=D/'DD_Body_Defense8_Accepted_126.zip'
body=body_path.read_bytes()
assert len(body)==23250730 and sha(body)=='a69336ec77dc3bc02d29ed725b8ff4f440d532f47edcf546b3885c735dbf14e8'
with zipfile.ZipFile(io.BytesIO(body)) as z: safe(z)
common={n:b for n,b in original.items() if n.startswith(('accepted-context/','current/','APPLICATION_'))}
common['accepted-context/DD_Body_Defense8_Accepted_126.zip']=body
common['accepted-context/BODY8_EXACT_ACCEPTANCE_126.json']=receipt_path.read_bytes()
common['CURRENT_SPELL_QUEUE_126.json']=queue_path.read_bytes()

boundary='''Current applied baseline597 reviewed/251 public-index pending/321 standalone/173 interfaces. Body/Defense8 now has exact independent authored acceptance with retained holds:8 accepted-unapplied,605 total accepted,243 still needing acceptance. BODY8_EXACT_ACCEPTANCE_126.json and its exact accepted archive supersede historical pending labels. Only four primitive crate-support documentary fields differ from the director final, fully recorded in LOCAL_ERRATUM_126.json; the director original is preserved. No Body8 canonical application or gameplay execution is claimed. Closed335feats and the72 applied spells remain closed dependencies. Time/Cast5 is currently undergoing director review and is not yet authority. Material8's missing complete return is unaccepted. Pending Eye and unsupported physical/body/cosmology producers remain unavailable. Read historical executables only as source text; do not execute them. All delivered evidence must distinguish authored cases from game execution.'''

transport=dict(common)
for n in ['original/DD_Transport_6_Conference_01.zip','TRANSPORT6_INDEPENDENT_QUESTIONS.json','SOURCE_BINDING_AUDIT.json']:
    transport[n]=original[n]
readme=original['README.md'].decode('utf-8-sig')
start=readme.index('Baseline597')
end=readme.index('Select full local procedures')
readme=readme[:start]+boundary+'\n\n'+readme[end:]
readme=readme.replace('conference125','conference126').replace('not an instruction to interrupt Body/Defense8','not an instruction to interrupt Time/Cast5')
transport['README.md']=readme.encode()

magic=dict(common)
magic_archive=A/'DD_Magic_Modifiers_7_Conference_01.zip'
magic_bytes=magic_archive.read_bytes()
assert len(magic_bytes)==4657895 and sha(magic_bytes)=='a4527b23f61140f865b5cf75409dea776a700070a01f008a2d96ef86d973649f'
with zipfile.ZipFile(io.BytesIO(magic_bytes)) as z:
    safe(z); m=json.loads(z.read('MANIFEST.json')); checks=[]
    for r in m['files']:
        b=z.read('sources/'+r['path'])
        assert len(b)==r['bytes'] and sha(b)==r['sha256']
        checks.append(dict(path=r['path'],archiveVerified=True,currentMatches=(G/r['path']).read_bytes()==b))
    assert len(z.read('CANDIDATE.json'))==m['candidate']['bytes'] and sha(z.read('CANDIDATE.json'))==m['candidate']['sha256']
magic['original/DD_Magic_Modifiers_7_Conference_01.zip']=magic_bytes
magic['MAGIC_MODIFIERS7_INDEPENDENT_QUESTIONS.json']=(A/'director-spell-review-125/MAGIC_MODIFIERS7_NEXT_CONFERENCE_NOTES_125.json').read_bytes()
magic['SOURCE_BINDING_AUDIT.json']=enc(dict(originalBindings=checks,driftExplanation='Only authored_review_index is expected to differ after accepted72 application; current exact index included.'))
magic['README.md']=('''# MagicModifiers7 director conference126 — prepared, not sent

Review Arcane Clone, Arcane Reversal, Elemental Rebind, Spell Sculptor, Spell Seal, Spell Theft and Resonance Communion. Preserve all7 complete original proposals,14 original case obligations,16 original questions and7 independent followups (23 total). This packet follows Transport6; it does not interrupt an active conference.

'''+boundary+'''

The seven independent questions are unselected requests, not adopted rules. Their earlier Body8-pending statement is historical and superseded only by the exact acceptance receipt included here. Select complete local procedures with explicit new-versus-inherited dispositions. Resolve actual combined Clone/MirrorImage selection and concentration; WaterPet's real2d6 heal without invented reserve; legal source-root and recipient defenses for heal-to-damage conversion; sourced Rebind resistance/immunity/reduction; real mixed terrain Sculptor and genuinely selective suppression limits; Seal/Anchor reciprocal exclusions as explicit new rules; Haste theft creator-self-donor backlash/concentration; Communion's exact currently accepted/class-legal acquired and unavailable IDs. No runtime repertoire permission is silently enabled.

Return full procedures, all23 question dispositions, all14 original scenario obligations with actual paid actors/rolls/clocks/geometry, adverse branches and explicit unavailable-source holds. Preserve immutable event-local observations, exact custody and class-level acquisition. Deliver complete MODEL, CASEBOOK, original-source history, full-value forward/inverse operations, hold register, manifest and actual verified downloadable ZIP. Do not silently replace failed original positive obligations with simpler passing cases. No summary-only acceptance or gameplay/balance certification.
''').encode()

for label,files,ids in [('Transport6',transport,oldmanifest['identities']),('MagicModifiers7',magic,['arcane-clone','arcane-reversal','elemental-rebind','spell-sculptor','spell-seal','spell-theft','resonance-communion'])]:
    manifest=dict(id=label.upper()+'-DIRECTOR-CONFERENCE-126',status='PREPARED_NOT_SENT',identities=ids,files=[bind(n,b) for n,b in sorted(files.items())])
    files['MANIFEST.json']=enc(manifest)
    out=A/f'DD_{label}_Director_Conference_126.zip'
    assert not out.exists()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n,b in files.items(): z.writestr(n,b)
    with zipfile.ZipFile(out) as z:
        safe(z)
        for r in manifest['files']: assert bind(r['path'],z.read(r['path']))==r
    rec=dict(id=manifest['id'],status='PREPARED_NOT_SENT',archive=bind(str(out),out.read_bytes()),members=len(files),manifestBindings=len(manifest['files']),questionCount=21 if label=='Transport6' else 23,body8AcceptanceIncluded=True,canonicalChanges=False,runtimeExecuted=False)
    (D/f'{label.upper()}_PACKET_126.json').write_bytes(enc(rec))
    (D/f'{label.upper()}_README_126.md').write_bytes(files['README.md'])
    print(json.dumps(rec))
