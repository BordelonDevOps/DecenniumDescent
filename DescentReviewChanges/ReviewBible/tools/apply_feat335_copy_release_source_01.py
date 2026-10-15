"""Apply only the three source-bound copying directions, preserving every original."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    decision_path = A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json'
    receipt_path = A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json'
    delta = A/'FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json'
    report = A/'FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json'
    preservation = A/'source-before-feat335-copy-release-source-01'
    assert all(not p.exists() for p in [delta, report, preservation])
    receipt = read(receipt_path); assert info(decision_path) == receipt['decision']
    decision = read(decision_path); assert decision['reviewId'] == 'FEAT335-COPY-RELEASE-SOURCE-01-ADDENDUM'
    rules = {r['id']: r for r in decision['decisions']}; assert set(rules) == {'CRS-01', 'CRS-02', 'CRS-03'}
    addition = '\n\nFEAT335-COPY-RELEASE-SOURCE-01-ADDENDUM — controlling release completion.\n' + '\n\n'.join(rules[k]['operativeWording'] for k in ['CRS-01', 'CRS-02', 'CRS-03'])
    base = R/'data/public/feat_candidates/exact_01'
    paths = [base/'shared_rules.json', base/'supplements.json', base/'candidate.json', A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json']
    submitted = read(A/'feat335-copy-release-source-01-input/PACKAGE_MANIFEST.json')
    before = {}; after = {}
    for p in paths:
        rel = p.relative_to(G).as_posix(); b = info(p); assert {'bytes': b['bytes'], 'sha256': b['sha256']} == submitted[rel], rel
        before[p] = read(p); after[p] = deepcopy(before[p])
    guide = R/'docs/mechanics/SPELL_INTEGRATION_RULES.md'; guide_before = info(guide)
    ids = {'eldritch_echo', 'mimicry', 'arcane_adaptation'}
    fs = next(r for r in after[paths[0]]['rules'] if r['id'] == 'FS-08'); fs['wording'] += addition
    sup = next(r for r in after[paths[1]]['groups'] if r['id'] == 'SUP-07')['value']['copyProfileContract']
    old_sentence = 'Strike/Burst/Mend are immediate. Ward/Hindrance/Boon/Step use their stated maximum two-interval duration;'
    new_sentence = 'Strike/Burst/Mend/Step are immediate. Ward/Hindrance/Boon use their stated maximum two-interval duration;'
    assert sup['lifecycle'].count(old_sentence) == 1
    sup['lifecycle'] = sup['lifecycle'].replace(old_sentence, new_sentence, 1)
    for key in ['castFamilyKeyContract', 'concentrationRules', 'strainEngineRef', 'strainEngineRules']: assert key not in sup
    sup.update(castFamilyKeyContract=rules['CRS-01']['operativeWording'], concentrationRules=rules['CRS-02']['operativeWording'],
        strainEngineRef='FS-09/CRS-03', strainEngineRules=rules['CRS-03']['operativeWording'])
    tags = {'strike': False, 'burst': False, 'mend': False, 'ward': True, 'hindrance': True, 'boon': True, 'step': False}
    assert {r['id'] for r in sup['profiles']} == set(tags)
    for row in sup['profiles']:
        assert 'concentrationRequired' not in row
        row['concentrationRequired'] = tags[row['id']]
    candidate = after[paths[2]]; contracts = after[paths[3]]
    for row in candidate['feats']:
        if row['id'] in ids:
            contract = next(r for r in contracts['records'] if r['id'] == row['id'])
            assert row['operationalRules'] == row['payloadOperational'] == contract['completeOperativeProcedure']
            row['operationalRules'] += addition; row['payloadOperational'] += addition
            contract['completeOperativeProcedure'] += addition
    contracts['controllingAddenda'].append(info(decision_path))
    # Independent footprint checks: no original, prerequisite, source/null, worked
    # case, unrelated feat, allowance or selection flag may change.
    checks = []
    def check(name, condition):
        assert condition, name
        checks.append(name)
    check('335 candidate identities retained', len(candidate['feats']) == len(before[paths[2]]['feats']) == 335)
    check('335 contract identities retained', len(contracts['records']) == len(before[paths[3]]['records']) == 335)
    for old, new in zip(before[paths[2]]['feats'], candidate['feats']):
        check(old['id']+' candidate identity and original unchanged', old['id'] == new['id'] and old['sourceObject'] == new['sourceObject'])
        expected = deepcopy(new)
        if old['id'] in ids:
            for k in ['operationalRules', 'payloadOperational']:
                check(old['id']+' '+k+' retains complete prior text', new[k] == old[k] + addition)
                expected[k] = old[k]
        check(old['id']+' all other candidate fields unchanged', expected == old)
    for old, new in zip(before[paths[3]]['records'], contracts['records']):
        expected = deepcopy(new)
        if old['id'] in ids:
            check(old['id']+' full current candidate/contract parity', new['completeOperativeProcedure'] == next(r for r in candidate['feats'] if r['id']==old['id'])['operationalRules'])
            expected['completeOperativeProcedure'] = old['completeOperativeProcedure']
        check(old['id']+' original and all acquisition fields unchanged', expected == old)
    shared_inverse = deepcopy(after[paths[0]])
    next(r for r in shared_inverse['rules'] if r['id']=='FS-08')['wording'] = next(r for r in before[paths[0]]['rules'] if r['id']=='FS-08')['wording']
    check('FS08 append only; FS09 and all other shared fields unchanged', shared_inverse == before[paths[0]])
    sup_inverse = deepcopy(after[paths[1]])
    inverse_contract = next(r for r in sup_inverse['groups'] if r['id']=='SUP-07')['value']['copyProfileContract']
    inverse_contract['lifecycle'] = inverse_contract['lifecycle'].replace(new_sentence, old_sentence, 1)
    for k in ['castFamilyKeyContract','concentrationRules','strainEngineRef','strainEngineRules']: del inverse_contract[k]
    for row in inverse_contract['profiles']: del row['concentrationRequired']
    check('SUP07 inverse reconstructs all prior supplement data', sup_inverse == before[paths[1]])
    check('all new profile tags explicit', {r['id']:r['concentrationRequired'] for r in sup['profiles']} == tags)
    for p, key in [(paths[2], 'feats'), (paths[3], 'records')]:
        inverse = deepcopy(after[p]); inverse[key] = before[p][key]
        if p == paths[3]: inverse['controllingAddenda'] = before[p]['controllingAddenda']
        check(p.name+' unrelated envelope unchanged', inverse == before[p])
    check('ordinary casting guide remains byte-identical', info(guide) == guide_before)
    preserved = []
    for p in paths:
        dest = preservation/p.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(p.read_bytes())
        assert dest.read_bytes() == p.read_bytes()
        preserved.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    for p in paths: p.write_bytes(encoded(after[p])); assert read(p) == after[p]
    changes = [{'before': b, 'after': info(G/b['path'])} for b in preserved]
    now = datetime.now(timezone.utc).isoformat()
    delta.write_bytes(encoded({'recordedAtUtc': now, 'authority': info(decision_path), 'changes': changes,
        'sourceInformationDeleted': 0, 'newCompletionDirections': ['CRS-01','CRS-02'], 'existingScopeClarification': ['CRS-03'],
        'targetFeatIds': sorted(ids), 'sourceOriginalsAndFlagsUnchanged': True, 'ordinaryCastingGuideUnchanged': guide_before}))
    report.write_bytes(encoded({'reviewId': decision['reviewId'], 'recordedAtUtc': now, 'status': 'source-application-verified; behavioral-acceptance-pending',
        'authority': info(decision_path), 'operations': info(delta), 'preservation': info(preservation/'PRESERVATION_MANIFEST.json'),
        'checks': len(checks), 'passed': checks, 'failures': [], 'changedFiles': len(paths), 'profileConcentration': tags,
        'acceptanceExamples': decision['acceptanceExamples'], 'behavioralExamplesExecuted': 0,
        'fullFeatCandidateApproved': False, 'runtimeImplemented': False, 'wholeGameFlowConfirmed': False, 'sourceInformationDeleted': 0}))
    assert info(guide) == guide_before
    print(json.dumps({'report': info(report), 'changedFiles': len(paths), 'sourcePreservationChecks': len(checks), 'behavioralExamplesStillRequired': len(decision['acceptanceExamples']), 'sourceInformationDeleted': 0}))

if __name__ == '__main__': main()
