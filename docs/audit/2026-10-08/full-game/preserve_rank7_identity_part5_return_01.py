"""Independent inbound verification; returned programs are parsed, never run."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast, copy, hashlib, io, json, stat, zipfile

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
IN = Path(r'C:\Users\cbord\Downloads\DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip')
OUT = A / IN.name
ROOT = A / 'rank7-identity-casting5-part5-conference-return-01'
REPORT = A / 'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_LOCAL_PREFLIGHT.json'
checks = []

def ck(label, value):
    checks.append({'check': label, 'passed': bool(value)})
    assert value, label

def sha(raw): return hashlib.sha256(raw).hexdigest()
def enc(obj): return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
def info(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}
def binding(raw, record, label):
    ck(label, len(raw) == record['bytes'] and sha(raw) == record['sha256'])

def safe(archive, label):
    names = archive.namelist()
    ck(label + ' unique names', len(names) == len(set(names)) == len(set(n.casefold() for n in names)))
    for item in archive.infolist():
        p = PurePosixPath(item.filename)
        ck(label + ' safe member ' + item.filename, not p.is_absolute() and '..' not in p.parts and '\\' not in item.filename and ':' not in item.filename and not stat.S_ISLNK(item.external_attr >> 16) and not item.is_dir())
    ck(label + ' bounded expanded size', sum(i.file_size for i in archive.infolist()) < 100_000_000)
    ck(label + ' CRC', archive.testzip() is None)

def parent(doc, pointer):
    parts = [x.replace('~1', '/').replace('~0', '~') for x in pointer.split('/')[1:]]
    current = doc
    for key in parts[:-1]: current = current[int(key)] if isinstance(current, list) else current[key]
    return current, parts[-1]

def main():
    ck('Fresh output locations', not any(p.exists() for p in (OUT, ROOT, REPORT)))
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_ILLUSION_REALITY_66.json'
    cp = json.loads(checkpoint.read_bytes())
    protected = [G / cp[k]['path'] for k in ['currentWorkQueue', 'currentAuthoredIndex', 'currentAcceptedInterfaceRegistry', 'decisionLedger']]
    protected += [G / b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected += [checkpoint, G / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json', G / 'DescentReviewChanges/ReviewBible/data/director/spell_review/rank7_identity_casting_5_source_conference_01.json']
    before = {p: p.read_bytes() for p in protected}
    raw = IN.read_bytes()
    binding(raw, {'bytes':14578890, 'sha256':'cdc2b871521cdb2c33bb2b23932d5fcb25dcb486e794e826c637d48d10beb5b7'}, 'Expected complete downloaded archive')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        safe(z, 'Returned archive')
        payload = {n: z.read(n) for n in z.namelist()}
    j = lambda n: json.loads(payload[n])
    manifest = j('MANIFEST.json')
    ck('51 members and 50 bound files', len(payload) == 51 and len(manifest['files']) == manifest['fileCount'] == 50)
    ck('Manifest exact membership', set(payload) == {'MANIFEST.json'} | {b['path'] for b in manifest['files']})
    for b in manifest['files']: binding(payload[b['path']], b, 'Manifest ' + b['path'])
    ib = j('INPUT_BINDINGS.json')
    original = payload[ib['archive']['path']]
    binding(original, ib['archive'], 'Original source archive binding')
    ck('Original source archive exact local bytes', original == (A / Path(ib['archive']['path']).name).read_bytes())
    authority = j('SOURCE_AUTHORITY.json')
    with zipfile.ZipFile(io.BytesIO(original)) as iz:
        safe(iz, 'Original source archive')
        ck('Original candidate exact local and returned baseline', iz.read('CANDIDATE.json') == payload['baseline/CANDIDATE.json'] == before[protected[-1]])
        sources = authority['completeOriginalSources']
        ck('68 complete source bindings retained', len(sources) == ib['expectedSources'] == 68 and sources == j('baseline/CANDIDATE.json')['sourceBindings'])
        ck('Input source checks match complete bindings', [{k:b[k] for k in ('path','bytes','sha256')} for b in ib['sourceChecks']] == sources)
        for b in sources:
            content = iz.read('sources/' + b['path'])
            binding(content, b, 'Original source ' + b['path'])
            ck('Actual authoring source unchanged ' + b['path'], (G / b['path']).read_bytes() == content)
    contexts = j('CONTEXT_BINDINGS.json')
    ck('Ten later exact contexts retained', len(contexts) == 10 and contexts == authority['laterExactContexts'])
    archives = {}
    for b in contexts:
        content = payload[b['path']]
        binding(content, b, 'Context ' + b['path'])
        anchor = b['originArchive']
        if anchor['name'] not in archives: archives[anchor['name']] = (A / anchor['name']).read_bytes()
        archived = archives[anchor['name']]
        binding(archived, anchor, 'Actual prior archive ' + anchor['name'])
        with zipfile.ZipFile(io.BytesIO(archived)) as az: member = az.read(b['member'])
        ck('Context exact prior member ' + b['path'], content == member)
    ops = j('EXACT_OPERATIONS_FROM_SOURCE.json')
    base = payload[ops['baseline']['path']]
    target = payload[ops['successor']['path']]
    binding(base, ops['baseline'], 'Replay baseline')
    binding(target, ops['successor'], 'Replay successor')
    binding(target, {'bytes':11968546, 'sha256':'2cd09a244b6f49a6aa1240ed295470bcbdaff8df038bb51092756849a47ef2f5'}, 'Expected MODEL bytes')
    ck('27 complete operations', len(ops['operations']) == ops['operationCount'] == 27)
    current = json.loads(base)
    for i, op in enumerate(ops['operations']):
        container, key = parent(current, op['pointer'])
        ck('Supported exact operation ' + str(i), isinstance(container, dict) and op['op'] in ('replace','add') and op['afterExists'])
        ck('Before presence ' + str(i), (key in container) == op['beforeExists'])
        ck('Before value ' + str(i), container.get(key) == op['before'])
        container[key] = copy.deepcopy(op['after'])
    ck('Forward reconstructs exact MODEL bytes', enc(current) == target)
    for i, op in enumerate(reversed(ops['operations'])):
        container, key = parent(current, op['pointer'])
        ck('Reverse complete after value ' + str(i), key in container and container[key] == op['after'])
        if op['beforeExists']: container[key] = copy.deepcopy(op['before'])
        else: del container[key]
    ck('Reverse reconstructs exact original candidate bytes', enc(current) == base)
    old, model = json.loads(base), json.loads(target)
    ck('Five original spell identities preserved', [x['spellId'] for x in old['records']] == [x['spellId'] for x in model['records']] and len(model['records']) == 5)
    for i, (source, successor) in enumerate(zip(old['records'], model['records'])):
        ck('Complete original spell record retained ' + str(i), all(successor[k] == v for k,v in source.items()))
        ck('Complete proposed procedure present ' + str(i), len(successor['proposedProcedure']) > 1000)
        ck('Shared-rule references resolve ' + str(i), set(successor['proposedSharedRuleIds']) <= {r['id'] for r in model['selectedSharedRules']})
    for key in old:
        if key not in {'id','recordedAtUtc','status','records','currentVectors'}: ck('Original top-level field unchanged ' + key, old[key] == model[key])
    cases = j('CASE_DISPOSITIONS.json')
    ck('Ten main and 39 independent branches', len(cases['cases']) == cases['newMainCaseCount'] == 10 and sum(len(c['independentBranches']) for c in cases['cases']) == cases['independentBranchCount'] == 39)
    ck('Complete case mirror equality', cases['cases'] == model['currentVectors'])
    ck('Eleven explicit conditional branches retained', cases['conditionalBranchCount'] == len(model['conditionalBranchRegister']) == 11)
    ck('24 original questions and selected dispositions', len(model['questions']) == len(model['selectedQuestionDispositions']) == 24)
    ck('All five identities retain tier C', old['riskCounts'] == model['riskCounts'] == {'C':5})
    ck('No application runtime testing cosmology or whole-game completion claims', not any(model[k] for k in ('newRuleAdoptions','runtimeTestsExecuted','humanPlaytests','sourceInformationDeleted','cosmologyDecisions','wholeGameComplete')) and not cases['runtimeExecuted'])
    for name, content in payload.items():
        if name.endswith('.py'):
            ast.parse(content.decode('utf-8'))
            ck('Python syntax parsed only, never executed ' + name, True)
    ROOT.mkdir()
    OUT.write_bytes(raw)
    for name, content in payload.items():
        dest = ROOT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        ck('Extracted complete bytes ' + name, dest.read_bytes() == content)
    ck('Preserved archive exact', OUT.read_bytes() == raw)
    for p, content in before.items(): ck('Protected authority unchanged ' + p.relative_to(G).as_posix(), p.read_bytes() == content)
    report = {'id':'RANK7-IDENTITY-CASTING5-PART5-RETURN-01-LOCAL-PREFLIGHT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(OUT),'model':info(ROOT/'MODEL.json'),'nativeFinal':info(A/'GPT_PART5_RANK7_IDENTITY_RETURN_01_NATIVE.json'),'nativeFinalLimit':'Native assistant text is truncated; the complete REVIEW.md, MODEL, chapters and source artifacts are preserved in the archive.','checks':checks,'checkCount':len(checks),'failures':0,'sourceFiles':68,'contextFiles':10,'forwardAndReverseOperations':27,'caseInventory':{'main':10,'branches':39,'conditionalBranches':11},'scope':'Independent source, hash, manifest, exact replay and preservation checks. Authored semantic review remains pending. Returned code parsed only; no returned code imported/executed and no game runtime tests.','acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'implementationApplied':False}
    REPORT.write_bytes(enc(report))
    print(json.dumps({'report':info(REPORT),'checks':len(checks),'failures':0,'archive':info(OUT)}))

if __name__ == '__main__': main()
