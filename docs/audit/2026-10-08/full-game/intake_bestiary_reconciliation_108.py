"""Preserve the actual final GPT reconciliation; execute no supplied code."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile

A = Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
P = Path(r'C:\Users\cbord\Downloads\DD_Bestiary_Final_Reconciliation_105_01.zip')
OUT = A / 'bestiary-reconciliation-108'
OUT.mkdir(exist_ok=False)
checks = []

def h(b): return hashlib.sha256(b).hexdigest()
def check(name, ok):
    checks.append({'name': name, 'passed': bool(ok)})
    if not ok: raise AssertionError(name)
def write(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f: f.write(b)
def info(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':h(b)}

b=P.read_bytes()
check('Actual final ZIP matches visible final receipt', len(b)==634707 and h(b)=='951bdc3d80f1b803e92584139ba50c900294af62ec7e38860ae697b96873465c')
write(OUT/P.name,b)
with zipfile.ZipFile(P) as z:
    names=z.namelist()
    check('39 unique safe text/data members', len(names)==39 and len(set(names))==39 and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n and PurePosixPath(n).suffix in {'.json','.txt','.md'} for n in names))
    check('No archive symbolic links', all(not stat.S_ISLNK(i.external_attr>>16) for i in z.infolist()))
    check('All members CRC valid',z.testzip() is None)
    manifest=json.loads(z.read('MANIFEST.json'))
    check('Manifest final binding',len(z.read('MANIFEST.json'))==7141 and h(z.read('MANIFEST.json'))=='59d0411b20ee9111d0ef5f016154b7d638d0b274b97c7acda0732df4714fdb34')
    check('Manifest complete membership', {r['path'] for r in manifest['files']}==set(names)-{'MANIFEST.json'})
    for r in manifest['files']:
        x=z.read(r['path']); check('Member bound '+r['path'],len(x)==r['bytes'] and h(x)==r['sha256'])
    for n in names:
        x=z.read(n)
        if n.endswith('.json'): json.loads(x)
        else: x.decode('utf8')
        write(OUT/'delivery'/n,x)
    for r in manifest['externalCompleteHistory']:
        x=(A/'bestiary-deliveries-104'/r['file']).read_bytes()
        check('Preserved historical source '+r['file'],len(x)==r['bytes'] and h(x)==r['sha256'])
report={'id':'BESTIARY-FINAL-RECONCILIATION-INTAKE-108','status':'ACTUAL_FINAL_PRESERVED_CONTAINER_VERIFIED_SEMANTIC_REVIEW_PENDING','finalArchive':info(OUT/P.name),'manifest':info(OUT/'delivery'/'MANIFEST.json'),'passed':len(checks),'failed':0,'checks':checks,'supersedesStagedMetadataOnly':{'earlierVisibleArtifact':'DD_Bestiary_Final_Reconciliation_105.zip','earlierVisibleBytes':334113,'earlierVisibleSha256':'a941ca9203a1e4250a2629e9978bbb382bfabbb7b77b1fff881a824e39053a5f','disposition':'Interim generation evidence only; not the final delivered archive, not downloaded or accepted.'},'scope':['No supplied code executed/imported.','Both original final proposals unchanged.','Local checkpoint108 is independent of GPT artifact label105_01.','No canonical gameplay change, whole-catalog acceptance, runtime test, balance approval, cosmology change, or GitHub push.']}
write(A/'BESTIARY_FINAL_RECONCILIATION_INTAKE_108.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps({'output':str(OUT),'passed':len(checks),'failed':0,'archive':report['finalArchive']}))
