"""One-use TEX preparation: preserve exact inputs and assemble isolated proof trees."""
from pathlib import Path
import hashlib, json, shutil, zipfile

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
D = A / 'teaching-nine-exact-reviewer-files'
BASE = Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\teaching-tex-reproduction')
F, W, N = (BASE / x for x in ('frozen', 'working', 'nested-originals'))
def h(b): return hashlib.sha256(b).hexdigest()
def extract(z, root):
    for name in z.namelist():
        p = (root / name).resolve()
        assert p.is_relative_to(root.resolve()) and not p.exists(), name
    for name in z.namelist():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(z.read(name))

assert not BASE.exists(), 'One-use preparation already exists'
archive = A / 'DD_Teaching_Navigation_9_Exact_Review_v1.zip'
assert h(archive.read_bytes()) == 'df0390f6a17a00428e102d3de2b8195d4334f1ead80493b70ffb6dfa21b03085'
with zipfile.ZipFile(archive) as z:
    mf = json.loads(z.read('FILE_MANIFEST.json'))
    assert len(mf) == 218
    disk = []
    for rel, v in mf.items():
        b = z.read(rel)
        assert len(b) == v['bytes'] and h(b) == v['sha256'], rel
        p = G / rel
        if p.exists():
            assert p.is_file() and h(p.read_bytes()) == v['sha256'], rel
            disk.append(rel)
    assert len(disk) == 217
    extract(z, F)
shutil.copytree(F, W)
corrections = json.loads((D / 'TEX_EXACT_CORRECTIONS.json').read_text('utf-8'))
ops = corrections['operations']
with zipfile.ZipFile(F / 'docs/audit/2026-10-08/full-game/DD_Low_Rank_136_Exact_Review_v1.zip') as z:
    nested = json.loads(z.read('FILE_MANIFEST.json'))
    for rel in ['DescentReviewChanges/ReviewBible/data/director/advanced_craft_recipe_candidate_internal.json', 'DescentReviewChanges/ReviewBible/docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md']:
        b = z.read(rel)
        assert h(b) == nested[rel]['sha256'] and h((G/rel).read_bytes()) == h(b)
        for root in (N, W):
            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
for op in ops:
    assert h((G/op['path']).read_bytes()) == op['beforeFileSha256'], op['id']
out = {'scope':'Exact frozen inputs and separate amendment working copy; no live correction applied yet.', 'frozen':str(F), 'working':str(W), 'nestedOriginals':str(N), 'liveDiskPayloadsUnchanged':disk, 'payloadCount':len(mf), 'liveDiskCount':len(disk), 'operations':len(ops)}
(A/'TEACHING_TEX_LOCAL_PREPARATION.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frozenPayloads':218,'unchangedLivePayloads':217,'operativeReplacements':9,'base':str(BASE)}))
