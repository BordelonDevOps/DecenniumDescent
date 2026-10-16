"""Read-only source/return verification; writes a new audit, never adopts spells."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'ac6-full-review-03-return'
INP = A / 'ac6-full-current-review-03-input'
checks = []

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def check(label, actual, expected=True):
    checks.append({'check': label, 'passed': actual == expected,
                   **({} if actual == expected else {'actual': actual, 'expected': expected})})

def ptr(d, pointer):
    if not pointer:
        return d
    assert pointer.startswith('/'), pointer
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        d = d[int(token)] if isinstance(d, list) else d[token]
    return d

def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)

def refs(obj, where=''):
    if isinstance(obj, dict):
        if 'path' in obj and 'pointer' in obj:
            yield where, obj
        for k, v in obj.items():
            yield from refs(v, where + '/' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from refs(v, where + '/' + str(i))

model = read(OUT / 'SPELLS_MODEL.json')
register = read(OUT / 'REGISTER.json')
casebook = read(OUT / 'CASEBOOK.json')
source_hashes = read(OUT / 'SOURCE_HASHES.json')
manifest = read(OUT / 'EVIDENCE_MANIFEST.json')
source = read(INP / 'CURRENT_REVIEW_INPUT.json')
input_bindings = read(INP / 'SOURCE_MANIFEST.json')['bindings']
archive = A / 'DD_AC6_Full_Review_03_Return.zip'
ab = archive.read_bytes()
check('returned archive length', len(ab), 252130)
check('returned archive hash', sha(ab), 'dbbef55122205be4bc3477c53c489cc150f46e832c2b78cad2b8e887573179f9')
expected_names = {'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
with zipfile.ZipFile(archive) as z:
    check('exact eight unique root members', len(z.namelist()) == 8 and set(z.namelist()) == expected_names)
    for name in sorted(expected_names):
        check('extracted exact bytes ' + name, (OUT/name).read_bytes() == z.read(name))
for entry in manifest['files']:
    b = (OUT/entry['name']).read_bytes()
    check('output length ' + entry['name'], len(b), entry['bytes'])
    check('output SHA ' + entry['name'], sha(b), entry['sha256'])
check('output manifest covers seven nonself files', {e['name'] for e in manifest['files']} == expected_names - {'EVIDENCE_MANIFEST.json'})
check('exact source binding list', source_hashes['bindings'] == input_bindings)
check('103 bindings', len(input_bindings), 103)
for e in input_bindings:
    b = (INP/'sources'/e['path']).read_bytes()
    check('source length ' + e['path'], len(b), e['bytes'])
    check('source SHA ' + e['path'], sha(b), e['sha256'])
check('input archive length', (A/'DD_AC6_Full_Current_Review_03.zip').stat().st_size, manifest['inputArchive']['bytes'])
check('input archive SHA', sha((A/'DD_AC6_Full_Current_Review_03.zip').read_bytes()), manifest['inputArchive']['sha256'])
check('14 identity order', [v['id'] for v in model['spells']], [v['spellId'] for v in source['records']])
check('14 identities unique', len({v['id'] for v in model['spells']}), 14)
check('register ID order', register['spellIds'], [v['id'] for v in model['spells']])
placements = 0
for new, old in zip(model['spells'], source['records']):
    for field in ['questionId','completeSourceAndAccess','historicalQuestionAndRecord','completePriorDraftRecord','priorDraftBinding','priorWholeRecordPointer']:
        check(new['id'] + ' preserves ' + field, new[field] == old[field])
    placements += len(old['completeSourceAndAccess']['source']['original']['placements'])
check('16 placements', placements, 16)
check('22 original texts unchanged', casebook['historicalOriginalTexts'], source['originalExamplesUnchanged'])
check('32 original example requirements unchanged', casebook['originalRequiredExamples'], source['originalRequiredExamplesUnchanged'])
check('model original example requirements unchanged', model['originalRequiredExamples'], source['originalRequiredExamplesUnchanged'])
check('51 original current IDs retain order', [v['id'] for v in casebook['cases'][:51]], [v['id'] for v in source['currentExamples']])
check('four additional cases', [v['id'] for v in casebook['cases'][51:]], ['AC6-RX01','AC6-RX02','AC6-RX03','AC6-RX04'])
check('55 cases unique', len({v['id'] for v in casebook['cases']}), 55)
for new, old in zip(casebook['cases'], source['currentExamples']):
    check('prior current case retained ' + old['id'], new.get('previousCurrentVersion') == old)
for key, input_key, embedded in [
    ('historicalIssueDispositions','historicalIssuesUnchanged','originalIssue'),
    ('currentInterfaceIssueDispositions','currentIssuesUnchanged','originalIssue'),
    ('currentReviewQuestionDispositions','currentReviewQuestions','question')]:
    check(key + ' exact ID order', [v['id'] for v in model[key]], [v['id'] for v in source[input_key]])
    check(key + ' register matches model', register[key], model[key])
    for new, old in zip(model[key], source[input_key]):
        check(key + ' preserves original ' + old['id'], new[embedded], old if embedded == 'originalIssue' else old['question'])
        check(key + ' nonempty disposition ' + old['id'], bool(new['verdict'] and new['reason']))
check('original questions ID coverage', [v['id'] for v in model['originalQuestionDispositions']], [v['questionId'] for v in source['records']])
for flag in ['runtimeTestsExecuted','humanPlaytested','balanceApproved','cosmologyCanonModified']:
    check('no unsupported approval ' + flag, model[flag], False)

# Current executable surfaces only: frozen prior versions are retained evidence,
# not current reference endorsements. Check each occurrence, including duplicates.
current_objects = [
    ('/spells/'+str(i), {k:v for k,v in s.items() if k not in ['completePriorDraftRecord','historicalQuestionAndRecord','completeSourceAndAccess']})
    for i,s in enumerate(model['spells'])]
current_objects += [('/cases/'+str(i), {k:v for k,v in c.items() if k != 'previousCurrentVersion'}) for i,c in enumerate(casebook['cases'])]
pointer_count = 0
pointer_results = []
cache = {}
for where, obj in current_objects:
    for at, ref in refs(obj, where):
        pointer_count += 1
        path = OUT/ref['path'] if ref['path'] in expected_names else INP/'sources'/ref['path']
        try:
            if path not in cache:
                cache[path] = read(path)
            value = ptr(cache[path], ref['pointer'])
            ok = value is not None
            error = None
        except Exception as exc:
            ok = False
            error = str(exc)
        check('current pointer ' + at, ok)
        pointer_results.append({'at': at, 'path':ref['path'], 'pointer':ref['pointer'], 'resolves':ok, **({'error':error} if error else {})})

# Text inclusion is a narrow check, not proof that a procedure is complete.
for chapter in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
    text = (OUT/chapter).read_text(encoding='utf-8')
    for s in model['spells']:
        for i, leaf in enumerate(strings(s['procedure'])):
            check(chapter + ' contains current procedure leaf ' + s['id'] + ':' + str(i), leaf in text)
    for key, profile in model['profiles'].items():
        check(chapter + ' identifies profile ' + key, key in text)
report = {
    'id':'AC6-FULL-REVIEW-03-INDEPENDENT-STRUCTURAL-CHECK',
    'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
    'status':'Read-only structural/preservation verification; separate substantive findings block acceptance.',
    'returnedArchive':{'path':str(archive.relative_to(G)).replace('\\','/'),'bytes':len(ab),'sha256':sha(ab)},
    'counts':{'sources':103,'identities':14,'placements':placements,'historicalExamples':22,'preservedCurrentCases':51,'currentCases':55,'currentPointerOccurrencesExamined':pointer_count},
    'checkCount':len(checks),'failureCount':sum(not c['passed'] for c in checks),
    'checks':checks,'pointerResults':pointer_results,
    'newSpellAdoptions':0,'runtimeTestsExecuted':False,'humanPlaytested':False,
    'semanticReviewComplete':False,'balanceApproved':False,'wholeGameApproved':False
}
target=A/'AC6_FULL_REVIEW_03_INDEPENDENT_STRUCTURAL_CHECK.json'
assert not target.exists(), 'Preserve existing audit; use a new revision.'
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['counts','checkCount','failureCount']}))
print(json.dumps([v for v in checks if not v['passed']],ensure_ascii=False))
