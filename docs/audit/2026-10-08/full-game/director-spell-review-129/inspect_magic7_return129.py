from pathlib import Path
import json,zipfile,hashlib,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game\director-spell-review-129')
P=Path(r'C:\Users\cbord\Downloads\DD_Magic7_Corrected_Return02_129.zip')
sha=lambda b:hashlib.sha256(b).hexdigest()
assert P.stat().st_size==65044749 and sha(P.read_bytes())=='6ae12be53766b4bbb9a1ebb9bd00ecb5779b8c0d108664d9253322c8a95ea18c'
Z=zipfile.ZipFile(P);assert Z.testzip() is None and len(Z.namelist())==len(set(Z.namelist()))==79
M=json.loads(Z.read('MANIFEST.json'));assert sha(Z.read('MANIFEST.json'))=='2d39ab8988be6c0221b356886af1abea19b849d254cf3b3a96c24bb81d59610e'
print('MANIFEST_KEYS',list(M))
E=D/'magic7_return02_received';E.mkdir(exist_ok=True)
for n in Z.namelist():
 p=(E/n).resolve();assert p.is_relative_to(E.resolve())
 p.parent.mkdir(parents=True,exist_ok=True);b=Z.read(n)
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
dest=D/P.name
if dest.exists():assert dest.read_bytes()==P.read_bytes()
else:shutil.copyfile(P,dest)
for n in ['MANIFEST.json','MODEL.json','PROCEDURES.json','CASEBOOK.json','ACTOR_TEMPLATES.json','VALIDATION_REPORT.json','EVENT_REVERSIBLE_OPERATIONS.json','EXACT_PROCEDURE_OPERATIONS.json','NATIVE_AND_ACCESS_RECORDS.json']:
 d=json.loads(Z.read(n));print(n, list(d) if isinstance(d,dict) else ['list',len(d)], {k:len(v) for k,v in d.items() if isinstance(v,(list,dict))} if isinstance(d,dict) else '')
