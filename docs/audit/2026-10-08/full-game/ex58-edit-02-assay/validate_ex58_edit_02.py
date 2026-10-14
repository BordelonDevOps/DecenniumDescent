#!/usr/bin/env python3
"""Read-only archive verification plus in-memory EX58-EDIT-02/reference checks.

No repository files, submitted archives, or historical receipts are modified.
The report is new evidence only. Numerical fixtures do not authenticate campaign
facts or execute the game's assay, adjudication, custody, or settlement runtime.
"""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import zipfile


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pointer_get(value, pointer: str):
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def pointer_set(value, pointer: str, replacement):
    parts = pointer.lstrip('/').split('/')
    for part in parts[:-1]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    key = parts[-1].replace('~1', '/').replace('~0', '~')
    value[int(key) if isinstance(value, list) else key] = replacement


def apply_in_memory(raw: bytes, op: dict) -> bytes:
    if sha(raw) != op['parentFileSha256']:
        raise ValueError('Parent bytes differ; do not overwrite a changed current file.')
    if op['op'] == 'replace_json_string':
        obj = json.loads(raw)
        guard = op['recordGuard']
        if pointer_get(obj, guard['pointer']) != guard['equals']:
            raise ValueError('Wrong record identity.')
        if pointer_get(obj, op['pointer']) != op['old']:
            raise ValueError('Old JSON string differs.')
        old = json.dumps(op['old'], ensure_ascii=False).encode('utf-8')
        new = json.dumps(op['replacement'], ensure_ascii=False).encode('utf-8')
    elif op['op'] == 'replace_text':
        old, new = op['old'].encode('utf-8'), op['replacement'].encode('utf-8')
    else:
        raise ValueError('Unsupported correction operation.')
    if raw.count(old) != op['expectedOccurrences']:
        raise ValueError('Expected unique old text is missing or duplicated.')
    return raw.replace(old, new, 1)


def ceiling_cp(gp: Fraction) -> int:
    value = 100 * gp
    return -(-value.numerator // value.denominator)


def reference(false_face: str, assay_face: str, remint_value: str, *,
              knowing: bool = True, assay_incurred: bool = True,
              remint_incurred: bool = True, credited: str = '0') -> dict:
    f, af, rm, credit = map(Fraction, (false_face, assay_face, remint_value, credited))
    if min(f, af, rm, credit) < 0:
        raise ValueError('Negative fixture input.')
    a = max(Fraction(1), af / 100) if assay_incurred else Fraction(0)
    r = rm / 50 if remint_incurred else Fraction(0)
    s = a + r
    p = max(f / 10, s) if knowing else s
    return {'assay': str(a), 'remint': str(r), 'fees': str(s),
            'totalExact': str(p), 'fineExact': str(p - s),
            'remainingExact': str(max(Fraction(0), p - credit)),
            'combinedFinalBillCp': ceiling_cp(p)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-archive', type=Path, required=True)
    ap.add_argument('--verdict-archive', type=Path, required=True)
    ap.add_argument('--corrections', type=Path, default=Path(__file__).with_name('EX58_EDIT_02_CORRECTIONS.json'))
    ap.add_argument('--report', type=Path, default=Path(__file__).with_name('EX58_EDIT_02_CHECKS_REPRODUCED.json'))
    args = ap.parse_args()
    source_bytes = args.source_archive.read_bytes()
    parent_bytes = args.verdict_archive.read_bytes()
    c = json.loads(args.corrections.read_text(encoding='utf-8'))
    results = []
    def check(name, result, kind='source/structure'):
        results.append({'name': name, 'kind': kind, 'pass': bool(result)})
        if not result:
            raise AssertionError(name)
    check('Frozen source ZIP digest', sha(source_bytes) == c['source']['archiveSha256'])
    check('Historical verdict ZIP digest', sha(parent_bytes) == c['historicalPackage']['sha256'])
    check('Historical verdict ZIP byte count', len(parent_bytes) == c['historicalPackage']['bytes'])
    with zipfile.ZipFile(args.source_archive) as z:
        loop = z.read(c['source']['path'])
        source_entry = json.loads(z.read('FILE_MANIFEST.json'))[c['source']['path']]
    check('Loop member digest matches source manifest/addendum', sha(loop) == source_entry['sha256'] == c['source']['sha256'])
    check('Loop member byte count matches source manifest/addendum', len(loop) == source_entry['bytes'] == c['source']['bytes'])
    source_lines = loop.decode('utf-8').splitlines()
    check('Source subsection location', source_lines[612] == '### Coin assay and reminting')
    check('Greater-of sentence preserved at source line 617', c['source']['controllingQuote'] in source_lines[616])
    check('Innocent documented-holder source rule', 'An innocent holder with documented provenance pays no criminal fine.' in source_lines[616])
    check('Actual source assay/remint rates', "Assay costs 1% of the lot's face value, minimum 1 gp. Reminting costs 2% of recovered metal value." in source_lines[614])
    with zipfile.ZipFile(args.verdict_archive) as z:
        original = {n: z.read(n) for n in z.namelist()}
    manifest = json.loads(original['FILE_MANIFEST.json'])
    check('All 17 original verdict payloads inventoried', manifest['payloadCount'] == len(manifest['files']) == 17)
    for entry in manifest['files']:
        raw = original[entry['path']]
        check('Original payload: ' + entry['path'], sha(raw) == entry['sha256'] and len(raw) == entry['bytes'])
    marker = b"Knowing fraud's fine is capped"
    found = {n: b.count(marker) for n, b in original.items() if marker in b}
    check('Exact exhaustive three-file cap occurrence set', found == {op['path']: 1 for op in c['affectedRepresentations']})
    derived = dict(original)
    for op in c['affectedRepresentations']:
        before = original[op['path']]
        after = apply_in_memory(before, op)
        derived[op['path']] = after
        check(op['operationId'] + ' exact descendant bytes/hash', len(after) == op['minimalReplacementResult']['bytes'] and sha(after) == op['minimalReplacementResult']['sha256'])
        if op['op'] == 'replace_json_string':
            old_obj, new_obj = json.loads(before), json.loads(after)
            check(op['operationId'] + ' exact new field value', pointer_get(new_obj, op['pointer']) == op['replacement'])
            restored = copy.deepcopy(new_obj)
            pointer_set(restored, op['pointer'], op['old'])
            check(op['operationId'] + ' all other JSON values unchanged', restored == old_obj)
            old_pars, new_pars = op['old'].split('\n\n'), op['replacement'].split('\n\n')
            check(op['operationId'] + ' only paragraph 3 differs', len(old_pars) == len(new_pars) == 8 and [i for i,(a,b) in enumerate(zip(old_pars,new_pars)) if a!=b] == [2])
        else:
            check(op['operationId'] + ' all other manuscript bytes unchanged', after.replace(op['replacement'].encode(),op['old'].encode(),1) == before)
        try:
            apply_in_memory(after, op)
        except ValueError:
            rejected = True
        else:
            rejected = False
        check(op['operationId'] + ' repeat-application rejected', rejected, 'negative control')
    new_par = c['exactReplacementParagraph']
    reg = json.loads(derived['EX58_AUTHORING_REGISTER.json'])['directions'][24]['authoringWording']
    conflict = json.loads(derived['EX58_CONFLICT_DISPOSITIONS.json'])['conflicts'][22]['completeReplacementWording']['FL-25']
    check('Complete FL-25 register/conflict parity', reg == conflict)
    check('Exact manuscript/JSON paragraph parity', reg.split('\n\n')[2] == new_par and derived['EX58_AUTHORING_VERDICT.md'].decode().count(new_par) == 1)
    check('All non-target verdict payloads byte-identical in derived view', all(derived[n] == b for n,b in original.items() if n not in found))
    check('Cap absent from corrected operational representations', all(marker not in derived[n] for n in found))
    check('Exactly three representation operations', len(c['affectedRepresentations']) == 3)
    check('NEW allocation provenance explicit', 'NEW explicit total-payment and fee allocation:' in new_par)
    check('Seven finite acceptance expectations', len(c['acceptanceExpectations']) == 7)
    fixtures = [
        ('F1 ten-percent branch, no remint', {'false_face':'1000','assay_face':'1000','remint_value':'0','remint_incurred':False}, {'fees':'10','totalExact':'100','fineExact':'90','remainingExact':'100'}),
        ('F2 mixed bill and prepaid fees', {'false_face':'1000','assay_face':'1200','remint_value':'200','credited':'16'}, {'fees':'16','totalExact':'100','fineExact':'84','remainingExact':'84'}),
        ('F3 fees greater than comparator', {'false_face':'20','assay_face':'120','remint_value':'100'}, {'fees':'16/5','totalExact':'16/5','fineExact':'0'}),
        ('F4 equal amounts', {'false_face':'50','assay_face':'500','remint_value':'0','remint_incurred':False}, {'fees':'5','totalExact':'5','fineExact':'0'}),
        ('F5 innocent documented holder, fees only', {'false_face':'1000','assay_face':'1200','remint_value':'200','knowing':False}, {'fees':'16','totalExact':'16','fineExact':'0'}),
        ('F6 knowing not established, missing provenance not guilt', {'false_face':'1000','assay_face':'1200','remint_value':'200','knowing':False,'credited':'16'}, {'totalExact':'16','fineExact':'0','remainingExact':'0'}),
        ('F7 no incurred services, independently lawful knowing finding', {'false_face':'100','assay_face':'0','remint_value':'0','assay_incurred':False,'remint_incurred':False}, {'fees':'0','totalExact':'10','fineExact':'10'}),
        ('F8 combined final-copper boundary, no intermediate floors', {'false_face':'100.03','assay_face':'100.03','remint_value':'0','remint_incurred':False}, {'fees':'10003/10000','totalExact':'10003/1000','fineExact':'90027/10000','combinedFinalBillCp':1001}),
        ('F9 whole liability already paid', {'false_face':'1000','assay_face':'1200','remint_value':'200','credited':'100'}, {'totalExact':'100','fineExact':'84','remainingExact':'0'}),
    ]
    fixture_results = []
    for name, inputs, expected in fixtures:
        actual = reference(**inputs)
        check(name, all(actual[k] == v for k,v in expected.items()), 'executed rational reference under stated synthetic premises')
        check(name + ' fees+fine equal total', Fraction(actual['fees'])+Fraction(actual['fineExact']) == Fraction(actual['totalExact']), 'executed rational invariant')
        fixture_results.append({'name':name,'syntheticInputs':inputs,'expected':expected,'actual':actual})
    check('Source ZIP untouched after verification', args.source_archive.read_bytes() == source_bytes)
    check('Historical verdict ZIP untouched after verification', args.verdict_archive.read_bytes() == parent_bytes)
    report={'addendumId':c['addendumId'],'status':'PASS','checks':len(results),'failedChecks':[],
        'executedScope':'Two frozen archive digests, the controlling Loop member, all17 original verdict payload hashes/bytes, exhaustive cap-location scan, three in-memory amendments, parity/preservation/replay checks and nine rational arithmetic fixtures. Not the original2,316 suite, repository fulfillment, gameplay runtime, actual intent/authority/custody, market evidence or campaign authentication.',
        'source':c['source'],'historicalPackage':c['historicalPackage'],
        'measuredMinimalReplacementDescendants':{op['path']:op['minimalReplacementResult'] for op in c['affectedRepresentations']},
        'results':results,'referenceFixtures':fixture_results,
        'authoredSemanticExpectationsNotRuntimeExecuted':c['acceptanceExpectations'],
        'originalsModified':False,'repositoryModified':False,'newPromotions':0}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"PASS: {len(results)} focused checks; 0 failures. Report: {args.report}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
