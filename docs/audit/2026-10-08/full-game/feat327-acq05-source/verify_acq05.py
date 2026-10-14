"""Read-only ACQ-05 source, exact-patch and reference-arithmetic checks.

Usage: python -X utf8 verify_acq05.py /path/DD_FEAT327_ACQ05_Companion_Timing_Source.zip
No game runtime or actual feat/bond events are executed. Optional --report writes
only the named report; the input ZIP is never written or extracted.
"""
import argparse, copy, hashlib, json, zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    spec = json.loads((here/'ACQ05_EXACT_OPERATIONS.json').read_text(encoding='utf-8'))
    results = []
    def check(name, condition):
        results.append({'id':name, 'passed':bool(condition)})
        if not condition:
            raise AssertionError(name)
    digest = lambda value: hashlib.sha256(value).hexdigest()
    raw = args.archive.read_bytes()
    check('archive.bytes', len(raw) == spec['submission']['bytes'])
    check('archive.sha256', digest(raw) == spec['submission']['sha256'])
    with zipfile.ZipFile(args.archive) as z:
        names = [i.filename for i in z.infolist() if not i.is_dir()]
        check('zip.unique-members', len(names) == len(set(names)))
        payload = {name:z.read(name) for name in names}
    manifest = json.loads(payload['PACKAGE_MANIFEST.json'])
    check('manifest.bytes-binding', digest(payload['PACKAGE_MANIFEST.json']) == spec['submission']['manifestSha256'])
    check('manifest.exact-members', set(payload) == set(manifest) | {'PACKAGE_MANIFEST.json'})
    check('manifest.21-payloads', len(manifest) == 21)
    for name, binding in manifest.items():
        check('source.bytes/'+name, len(payload[name]) == binding['bytes'])
        check('source.hash/'+name, digest(payload[name]) == binding['sha256'])
    B='DescentReviewChanges/ReviewBible/'
    A='docs/audit/2026-10-08/full-game/'
    j = lambda name: json.loads(payload[name])
    pubpath = B+'data/public/feat_candidates/exact_01/candidate.json'
    intpath = B+'data/director/feat_candidates/exact_01/candidate.json'
    conpath = A+'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    original = {name:j(name) for name in [pubpath,intpath,conpath]}
    check('public.id', original[pubpath]['feats'][10]['id'] == 'animal_companion')
    check('internal.id', original[intpath]['records'][161]['id'] == 'animal_companion')
    check('contract.id', original[conpath]['records'][10]['id'] == 'animal_companion')
    check('prerequisite.only-actual-Handling', original[conpath]['records'][10]['requirements'] == {'kind':'actualProficiency','credential':'Animal Handling'})
    check('feat.nonrepeatable', original[conpath]['records'][10]['repeats']['policy'] == 'nonrepeatable')
    check('child.OR-preserved', original[conpath]['records'][297]['requirements'] == {'kind':'any','requirements':[{'kind':'ownedFeat','id':'animal_companion'},{'kind':'actualProficiency','credential':'Animal Handling'}]})
    rules = j(B+'data/public/feat_candidates/exact_01/shared_rules.json')['rules']
    check('FS01.id', rules[0]['id'] == 'FS-01')
    check('FS06.id', rules[5]['id'] == 'FS-06')
    check('FS06.initial-finite-allowance', 'specified full finite allowance' in rules[5]['wording'])
    check('FS06.real-rest', 'one beneficial Long Rest per 24 elapsed hours' in rules[5]['wording'])
    ranger = j(B+'data/public/class_playtests/ranger.json')
    check('Ranger.native-feature', ranger['cards'][29]['id'] == 'ranger.hero.warder.beast-companion')
    check('Ranger.native-gate', ranger['cards'][29]['minimumClassLevel'] == 16 and ranger['cards'][29]['path'] == 'Warder' and ranger['cards'][29]['acquisition'] == 'selection')
    check('Ranger.native-cost', ranger['cards'][29]['cost'] == '4 RP; 1 hour with a willing/tamed eligible beast')
    check('Ranger.native-frequency', ranger['cards'][29]['frequency'] == '1/long rest')
    foundation = j(B+'data/playtest/character_foundation.json')
    warrior = next(x for x in foundation['classes'] if x['class'] == 'Warrior')
    check('Warrior.real-4-and-8-opportunities', 4 in warrior['asiClassLevels'] and 8 in warrior['asiClassLevels'])
    templates = j(B+'data/public/feat_candidates/exact_01/supplements.json')['groups'][1]
    check('SUP02.three-bodies', templates['id'] == 'SUP-02' and [x['id'] for x in templates['value']] == ['feat-animal.ground','feat-animal.flyer','feat-animal.swimmer'])
    derived = copy.deepcopy(original)
    text_original = {}
    text_derived = {}
    def parent(obj, pointer):
        parts = [x.replace('~1','/').replace('~0','~') for x in pointer.strip('/').split('/')]
        for key in parts[:-1]:
            obj = obj[int(key)] if isinstance(obj,list) else obj[key]
        return obj, parts[-1]
    for n, op in enumerate(spec['operations'],1):
        path=op['path']
        if op['op']=='replace_json_string':
            node,key=parent(derived[path],op['pointer'])
            check(f'patch{n}.old-guard', node[key] == op['old'])
            node[key]=op['replacement']
        else:
            text_original.setdefault(path,payload[path].decode('utf-8'))
            text_derived.setdefault(path,text_original[path])
            check(f'patch{n}.single-old-guard', text_derived[path].count(op['old']) == op['expectedOccurrences'])
            text_derived[path]=text_derived[path].replace(op['old'],op['replacement'],1)
    expected = (here/'ACQ05_ANIMAL_COMPANION_OPERATIVE.txt').read_text(encoding='utf-8').removesuffix('\n')
    for path,ptr in [(pubpath,'/feats/10/operationalRules'),(pubpath,'/feats/10/payloadOperational'),(intpath,'/records/161/operationalRules'),(intpath,'/records/161/payloadOperational'),(conpath,'/records/10/completeOperativeProcedure')]:
        node,key=parent(derived[path],ptr)
        check('derived.parity/'+path+ptr,node[key]==expected)
    check('reader.complete-text', expected in text_derived[B+'docs/feats/exact-candidate-01/GENERAL_COMBAT.md'])
    check('audit.complete-current-text', expected in text_derived[B+'docs/feats/exact-candidate-01/source-audit/GENERAL_COMBAT.md'])
    check('audit.historical-submitted-text-kept', '### Preserved submitted procedure\n\n'+original[intpath]['records'][161]['sourceDirection']['submittedProcedure'] in text_derived[B+'docs/feats/exact-candidate-01/source-audit/GENERAL_COMBAT.md'])
    check('internal.sourceDirection-unchanged', derived[intpath]['records'][161]['sourceDirection']==original[intpath]['records'][161]['sourceDirection'])
    # Reverse every allowed operation. Full equality proves no other field/string changed.
    back=copy.deepcopy(derived)
    backtext=dict(text_derived)
    for op in reversed(spec['operations']):
        if op['op']=='replace_json_string':
            node,key=parent(back[op['path']],op['pointer']);node[key]=op['old']
        else:
            backtext[op['path']]=backtext[op['path']].replace(op['replacement'],op['old'],1)
    for path in original:
        check('whole-object-inverse/'+path,back[path]==original[path])
    for path in text_original:
        check('whole-text-inverse/'+path,backtext[path]==text_original[path])
    for name,curr,maxhp,expectedhp in [('groundSmall',5,10,4),('groundMedium',1,20,1),('flyer',3,7,3),('swimmer',7,10,6)]:
        newhp=max(1,(5+4)*curr//maxhp)
        check('reference.initial-HP/'+name,newhp==expectedhp)
        check('reference.growth-no-heal/'+name,min(newhp,5+8)==expectedhp)
    check('reference.release-HP',max(1,10*4//9)==4)
    check('reference.hour-seconds',60*60==3600)
    check('input-archive-unchanged',digest(args.archive.read_bytes())==spec['submission']['sha256'])
    report={
        'reviewId':'FEAT327-ACQ-05','archive':spec['submission'],
        'kind':'Executed read-only source/patch/preservation and reference-arithmetic checks only',
        'checks':len(results),'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results),'results':results,
        'operations':len(spec['operations']),'existingDerivedFiles':len(derived)+len(text_derived),
        'submitted110CheckModelRerun':False,'lifecycleCasesExecuted':False,'gameplayRuntimeExecuted':False,
        'campaignRecordsAuthenticated':0,'featOrClassPromotion':False,
        'limits':'The submitted successful-hour model/report were read, not rerun. Its imported wider prerequisite suite is not contained in this narrow ZIP. Patch rehearsal runs only on in-memory copies. The20 lifecycle groups are authored acceptance expectations, not executed gameplay/attempt/transfer tests.'}
    if args.report:
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
if __name__=='__main__':
    main()
