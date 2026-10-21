"""One-shot byte preservation and independent container checks; no supplied code imports."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, zipfile

A = Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
D = Path(r'C:\Users\cbord\Downloads')
OUT = A / 'bestiary-deliveries-104'
OUT.mkdir(exist_ok=False)
EXPECTED = {
 'DD_Bestiary_Recovery_Part01.json': (1744791, '810c3551c3b369ffe12e69e8790d12f42731d35166be6e1e580d2e4c433e1938'),
 'DD_Bestiary_Recovery_Part01.txt': (29116, '3e974ffdca03a014e656724328e17bf0eb6690f427474bf1370b7f1d7b0ff8b9'),
 'DD_Bestiary_Recovery_Part01_MANIFEST.json': (999, 'dc075a862a118c1d8cf813062b5a93809e1547d033c5b25d390ce9a49fb7bf04'),
 'DD_Bestiary_Return02.zip': (53908070, 'ae2dd8f6300546321ddceb1a305aab108df04114acad4fbb737607cb71a1875f'),
}
checks, inventories, copies = [], {}, []
def h(b): return hashlib.sha256(b).hexdigest()
def check(name, ok, detail=None):
 checks.append({'id':name,'pass':bool(ok),'detail':detail})
 if not ok: raise AssertionError(name)
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f: f.write(b)
def check_zip(z,label):
 entries=z.infolist(); names=[x.filename for x in entries]
 check(label+':unique',len(names)==len(set(names)))
 check(label+':paths',all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n for n in names))
 check(label+':no-symlinks',all(not stat.S_ISLNK(x.external_attr>>16) for x in entries))
 check(label+':crc',z.testzip() is None)
 inventories[label]=[{'path':x.filename,'bytes':x.file_size,'sha256':h(z.read(x))} for x in entries if not x.is_dir()]
for n,(length,digest) in EXPECTED.items():
 b=(D/n).read_bytes(); check(n+':download-binding',len(b)==length and h(b)==digest)
 write(OUT/n,b); check(n+':preserved', (OUT/n).read_bytes()==b)
 copies.append({'path':str(OUT/n),'bytes':len(b),'sha256':h(b)})
pmanifest=json.loads((OUT/'DD_Bestiary_Recovery_Part01_MANIFEST.json').read_bytes())
for row in pmanifest['files']:
 b=(OUT/row['file']).read_bytes();check('part01-manifest:'+row['file'],len(b)==row['bytes'] and h(b)==row['sha256'])
with zipfile.ZipFile(OUT/'DD_Bestiary_Return02.zip') as z:
 check_zip(z,'Return02')
 manifest=json.loads(z.read('MANIFEST.json'))
 check('return02-manifest-members',set(x['path'] for x in manifest['files'])==set(z.namelist())-{'MANIFEST.json'})
 for row in manifest['files']:
  b=z.read(row['path']);check('return02-manifest:'+row['path'],len(b)==row['bytes'] and h(b)==row['sha256'])
 receipt=json.loads(z.read('REVIEW_RECEIPT.json'))
 for row in receipt['inputBindings']:
  b=z.read('input/'+row['path']);check('input:'+row['path'],len(b)==row['bytes'] and h(b)==row['sha256'])
  check('input-local-unchanged:'+row['path'],(A/row['path']).read_bytes()==b)
  with zipfile.ZipFile(io.BytesIO(b)) as nested:
   check_zip(nested,row['path'])
 for n in z.namelist():
  if '/' not in n and not n.endswith('.py'):
   write(OUT/'return02'/n,z.read(n))
 for row in json.loads(z.read('ARTIFACT_BINDINGS.json'))['files']:
  b=z.read(row['path']);check('artifact-binding:'+row['path'],len(b)==row['bytes'] and h(b)==row['sha256'])
report={'id':'BESTIARY-DUAL-DELIVERY-INTAKE-104','status':'PRESERVED_AND_CONTAINER_VERIFIED_NOT_SEMANTICALLY_ACCEPTED','files':copies,'checkCount':len(checks),'failures':0,'checks':checks,'inventories':inventories,'inputMemberCount':sum(len(v) for k,v in inventories.items() if k!='Return02'),'outerMemberCount':len(inventories['Return02']),'boundaries':['Both distinct final proposals preserved; neither takes automatic precedence.','Supplied scripts retained only inside unchanged ZIP; not imported or executed.','Checks cover bytes, hashes, container paths, CRC and bindings, not authored semantic correctness or runtime.','Sealed contents were hashed as opaque archive bytes only; no dossier content rendered.','No canonical, public, index, registry, helper or Git writes.']}
write(A/'BESTIARY_DUAL_DELIVERY_INTAKE_104.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps({'output':str(OUT),'checks':len(checks),'failures':0,'outerMembers':report['outerMemberCount'],'inputMembers':report['inputMemberCount']}))
