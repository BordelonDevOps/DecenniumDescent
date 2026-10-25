"""Fresh local archive receiver. Reads supplied files as bytes/JSON only; never runs them."""
from pathlib import Path,PurePosixPath
import argparse,zipfile,hashlib,json,stat,datetime,shutil
p=argparse.ArgumentParser();p.add_argument('download');p.add_argument('expected_bytes',type=int);p.add_argument('expected_sha256');p.add_argument('archive_name');p.add_argument('output_directory');p.add_argument('receipt_name');p.add_argument('--external-output-root',help='Optional short absolute extraction path to avoid Windows path-length limits');args=p.parse_args()
D=Path(__file__).parent.resolve();source=Path(args.download).resolve()
def local(name):
 out=(D/name).resolve();assert out.parent==D and name not in ['', '.', '..'];return out
dest=local(args.archive_name);out=Path(args.external_output_root).resolve() if args.external_output_root else local(args.output_directory);receipt=local(args.receipt_name)
sha=lambda b:hashlib.sha256(b).hexdigest();raw=source.read_bytes();assert len(raw)==args.expected_bytes and sha(raw)==args.expected_sha256.lower()
assert not out.exists() and not receipt.exists()
if dest.exists():assert dest.read_bytes()==raw
else:dest.write_bytes(raw)
with zipfile.ZipFile(dest) as z:
 entries=[x for x in z.infolist() if not x.is_dir()];names=[x.filename for x in entries]
 assert len(names)==len(set(names)) and len(names)==len({n.casefold() for n in names})
 for info in entries:
  n=info.filename;parts=PurePosixPath(n).parts
  assert not n.startswith('/') and '\\' not in n and ':' not in n and '..' not in parts and not stat.S_ISLNK(info.external_attr>>16),n
  assert (out/n).resolve().is_relative_to(out)
 assert z.testzip() is None
 assert 'MANIFEST.json' in names,'Missing top-level MANIFEST.json: inspect separately before extraction.'
 manifest=json.loads(z.read('MANIFEST.json').decode('utf-8-sig'))
 if 'files' in manifest:bindings=manifest['files']
 elif 'members' in manifest:
  if 'memberCountIncludingSelf' in manifest:
   assert manifest['excludedSelf']=='MANIFEST.json' and manifest['memberCountIncludingSelf']==len(names)
  else:
   assert manifest['excludedSelf']=='MANIFEST.json exact ZIP/delivery binds self' and manifest['membersIncludingSelf']==len(names)
  bindings=manifest['members'];artifact=json.loads(z.read('ARTIFACT_BINDINGS.json').decode('utf-8-sig'))
  assert artifact['bindings']==[b for b in bindings if b['path']!='ARTIFACT_BINDINGS.json']
 else:
  assert set(manifest['selfExclusions'])=={'MANIFEST.json','ARTIFACT_BINDINGS.json'}
  payload=manifest['payload'];artifact=json.loads(z.read('ARTIFACT_BINDINGS.json').decode('utf-8-sig'))
  assert artifact['bindings']==payload and manifest['payloadCount']==len(payload)
  assert manifest['memberCount']==len(names) and manifest['bindingFile']['path']=='ARTIFACT_BINDINGS.json'
  bindings=payload+[manifest['bindingFile']]
 assert len(bindings)==len({b['path'] for b in bindings}) and {b['path'] for b in bindings}==set(names)-{'MANIFEST.json'}
 for b in bindings:
  v=z.read(b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256'],b['path']
 out.mkdir()
 for n in names:
  target=out/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(n))
result={'status':'RECEIVED_BINDINGS_VERIFIED_NOT_ACCEPTED','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':{'path':str(dest),'bytes':len(raw),'sha256':sha(raw)},'directory':str(out),'members':len(names),'bindings':len(bindings),'manifest':{'bytes':(out/'MANIFEST.json').stat().st_size,'sha256':sha((out/'MANIFEST.json').read_bytes())},'canonicalChanges':False,'suppliedCodeExecuted':False}
receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
