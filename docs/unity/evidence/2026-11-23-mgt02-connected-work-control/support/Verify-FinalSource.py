from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
root=Path(__file__).resolve().parents[5];packet=Path(__file__).resolve().parent.parent;run=root/sys.argv[1]
h=lambda b:hashlib.sha256(b).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
pins=read(packet/'SOURCE_BINDINGS.json');same=[];changed=[]
for p in pins['pins']:
    actual=h((root/p['path']).read_bytes());row={'path':p['path'],'role':p['role'],'actual':actual,'pinned':p['workingSha256']}
    (same if actual==p['workingSha256'] else changed).append(row)
mutable_docs={'docs/unity/IMPLEMENTATION_MAP.md','docs/unity/IMPLEMENTATION_STATUS.json'}
assert all(x['path'].startswith('engine/') or x['path'] in mutable_docs for x in changed)
old=json.loads(subprocess.check_output(['git','show',pins['baseline']+':docs/unity/IMPLEMENTATION_STATUS.json'],cwd=root))
current=read(root/'docs/unity/IMPLEMENTATION_STATUS.json')
preserved={k:current[k]==old[k] for k in ['historicalDependencyMap','workItems','completionContract']}
assert all(preserved.values()),preserved
report=read(run/'results.json');assert report['coreCompilation']=='PASS'
with zipfile.ZipFile(run/'source-snapshot.zip') as z:
    for p in report['sourceHashes']:
        name=p['path'].replace('\\','/');assert h((root/'engine'/name).read_bytes())==p['sha256']==h(z.read(name)),name
assert len(report['sourceHashes'])==486
for name,digest in {'SOURCE_API_CONTRACT.md':'d65c7bcdf6c9ade960e70b527c82d71c367e4f883d180d91f0b299c8e13d8819','MODULE_DEFINITION.md':'39bed9de15d2a7e69e20860904207482a95f5f3ded1070432cd184ae9ec478f4','SOURCE_BINDINGS.json':'fed19205ac0a008826b3118ba1d5e37df475b037b0381ef88acdd12854644012'}.items():assert h((packet/name).read_bytes())==digest
out={'status':'PASS','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'compiledSourceHashesVerified':486,'sourceArchiveSha256':h((run/'source-snapshot.zip').read_bytes()),'pins':len(pins['pins']),'unchangedPins':same,'expectedImplementedSeamAndProgressChanges':changed,'preservedDependencyAndCompletionFields':preserved,'scope':'Immutable rules/authority/decisions and accepted contract bytes unchanged; existing implementation seams and progress map updates are explicitly distinguished. All486 compiled inputs match current worktree and frozen source archive.'}
(run.parent.parent/'final-source-pins.json').write_bytes((json.dumps(out,indent=2)+'\n').encode());print('PASS486 compiled inputs, immutable source/contract pins and unchanged dependency/completion fields')
