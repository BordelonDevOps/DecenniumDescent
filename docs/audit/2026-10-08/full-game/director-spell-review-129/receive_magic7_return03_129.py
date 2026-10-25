"""Verify declared delivery binding and safely preserve a downloaded Return03 as data."""
from pathlib import Path
import sys,json,zipfile,hashlib,shutil
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;P=Path(sys.argv[1]);expected_size=int(sys.argv[2]);expected_sha=sys.argv[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
assert P.stat().st_size==expected_size and sha(P.read_bytes())==expected_sha
E=D/'magic7_return03_received';E.mkdir(exist_ok=True)
with zipfile.ZipFile(P) as z:
 names=z.namelist();assert z.testzip() is None and len(names)==len(set(names))
 for n in names:
  assert not n.endswith('/'),n
  target=(E/n).resolve();assert target.is_relative_to(E.resolve()),n
  b=z.read(n);target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():assert target.read_bytes()==b
  else:target.write_bytes(b)
 m=json.loads(z.read('MANIFEST.json'))
 for row in m['files']:
  b=z.read(row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256']
dest=D/P.name
if dest.exists():assert dest.read_bytes()==P.read_bytes()
else:shutil.copyfile(P,dest)
receipt={'id':'MAGIC7-RETURN03-RECEIVED-129','status':'RECEIVED_BINDINGS_VERIFIED_NOT_ACCEPTED','archive':{'path':str(dest),'bytes':P.stat().st_size,'sha256':expected_sha},'directory':str(E),'members':len(names),'bindings':len(m['files']),'manifest':{'bytes':(E/'MANIFEST.json').stat().st_size,'sha256':sha((E/'MANIFEST.json').read_bytes())},'canonicalChanges':False,'suppliedCodeExecuted':False}
(D/'MAGIC7_RETURN03_DOWNLOAD_RECEIPT_129.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))
