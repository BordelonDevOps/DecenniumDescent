"""Freeze source questions before implementing paid feat-copy release history."""
from datetime import datetime, timezone
import json
import zipfile
from pathlib import Path
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def main():
    root = A / 'feat335-copy-release-source-01-input'
    archive = A / 'DD_Feat335_Copy_Release_Source_01.zip'
    receipt = A / 'FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json'
    assert not root.exists() and not archive.exists() and not receipt.exists()
    pub = R / 'data/public/feat_candidates/exact_01'
    paths = {pub / n for n in ['candidate.json', 'shared_rules.json', 'fex_rules.json',
                              'supplements.json', 'spell_dependencies.json']}
    paths.update(R / 'data/public/class_playtests' / n for n in
                 ['wizard.json', 'cleric.json', 'mirrorsage.json', 'shaman.json'])
    paths.update(R / 'docs/mechanics' / n for n in
                 ['SPELL_INTEGRATION_RULES.md', 'CLASS_PLAYTEST_RULES.md', 'COMBAT_ACTION_PLAYTEST.md'])
    paths.update(A / n for n in ['FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
                 'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json',
                 'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json', 'FEAT335_COPY_CAPTURE_CHECK.json'])
    paths.update(R / 'tools' / n for n in ['feat335_copy_source_components.py',
                 'feat335_copy_capture.py', 'spell_playtest_rules.py'])
    paths.add(R / 'data/director/feat_candidates/exact_01/additional_boundary_expectations.json')
    paths.add(Path(__file__))
    assert all(p.is_file() for p in paths)
    bindings = {p: info(p) for p in paths}
    shared = read(pub / 'shared_rules.json')
    supplements = read(pub / 'supplements.json')
    candidate = read(pub / 'candidate.json')
    rules = {row['id']: row for row in shared['rules']}
    copy_contract = next(x['value']['copyProfileContract'] for x in supplements['groups'] if x['id'] == 'SUP-07')
    contract_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    contracts = [x for x in read(contract_path)['records']
                 if x['id'] in {'eldritch_echo', 'mimicry', 'arcane_adaptation'}]
    assert len(contracts) == 3 and len(copy_contract['profiles']) == 7
    parity = []
    for c in contracts:
        card = candidate
        for segment in c['candidatePointer'].strip('/').split('/'):
            card = card[int(segment)] if isinstance(card, list) else card[segment]
        assert card['id'] == c['id']
        assert card['operationalRules'] == c['completeOperativeProcedure']
        assert card['payloadOperational'] == c['completeOperativeProcedure']
        parity.append({'featId': c['id'], 'pointer': c['candidatePointer'],
                       'bothCurrentOperativeFieldsMatchAcquisitionContract': True})
    question_text = '''FEAT335-COPY-RELEASE-SOURCE-01: three bounded source questions

Please finish the already submitted DI7-EXACT-REVIEW-01 before considering this separate request. This is a source clarification for the paid Eldritch Echo/Mimicry/Arcane Adaptation release integration, not a resubmission or approval request for all 335 feats. No copy-release implementation is supplied or claimed complete.

The archive contains the complete current candidate, shared FS rules, FEX rules, SUP-07, all three complete acquisition contracts, source dependencies, four complete class envelopes, governing guides, and historical capture/source-component reports. The selected candidate operationalRules and payloadOperational exactly match the three acquisition contracts. Historical reports remain their original evidence; their input bindings do not recertify changed source versions. The local source scan below is bounded to these governing sources, not a claim that no historical notebook passage could answer the questions.

CRS-01 — canonical chronological identity. FS-08 and SUP-07 require ordinary Dissonance/Refrain for a NEW temporary paid feat-copy cast; the integration guide uses consecutive same-named casts. SUP-07 records original source/event, selected profile and q, but does not explicitly name the resulting cast family. Please specify the exact stable name/key: original underlying spell, bounded profile, or another source-defined identity. Determine whether changing capture event, Echo versus Mimicry versus adapted permission, selected numeric type/q, or chosen ability route changes that identity, and whether the ordinary original spell shares the copy's history. Include two consecutive real-copy examples and an original-then-copy example. Please cite an existing governing rule if it already answers this, otherwise label the minimum completion NEW. Do not grant the original spell or new ordinary access.

CRS-02 — concentration of seven profiles. FS-08 says the new copy uses one concentration slot and SUP-07 refers to actual concentration, but the seven profile rows specify durations without explicit concentration tags. Please give a precise yes/no tag for each of Strike, Burst, Mend, Ward, Hindrance, Boon and Step. Does a lasting copy require concentration independently of whether the witnessed original did? What happens to existing concentration at commitment, to a countered copy, and to a lasting effect on lost concentration? Preserve the printed deadlines, single-grant temporary HP and strongest-family rules. Generic Ready already holds concentration at preparation; distinguish that hold from the released profile. If this is new completion, label it NEW rather than recovered source wording.

CRS-03 — actual strain engine and Limit. The chosen own route supplies ability/rank ceiling and does not teach the original spell. FS-08 calls these ordinary quote/Dissonance/Refrain while disabling ordinary class procs. FS-09 separately states for a feat-only grant without a class-engine override base 0/1/2 and Limit=max(4,2PB+casting modifier), and says being a Wizard does not make an independent feat charge a prepared matrix. SPELL_INTEGRATION_RULES uses Limit=max(4,2+PB+max(0,modifier)); quote_cast implements that ordinary formula. Please decide which explicit formula governs these temporary feat-copy casts, and whether any chosen class engine's protected base reduction/routing/vent applies. In particular, does a Wizard-qualified copy receive a prepared-matrix first-family exemption despite not being a prepared matrix? Does choosing the explicit feat-only rank-zero Eldritch Blast route change the copy engine/Limit? Keep rank0 price0 and rank-dependent base strain, the actual pre-cast surcharge/block threshold, chronological counter history and independent real costs. Do not silently correct either existing formula globally: identify the exact bounded applicability or guarded source correction and every active counterpart it needs.

Return exact operative wording, source citations/KEEP versus NEW classifications and a finite set of acceptance examples for these three questions. A downloadable JSON/text addendum with bytes and SHA256 is preferred. Preserve all source/original fields, 335 identities, legacy nulls, selection flags, prior examples and per-owner shared one-release/numbered-round cap. Do not add new copying, ordinary repertoire, RP pools, proc chains or extra concentration. No whole-game signoff, publication, cosmology or owner balance approval is requested. All unchanged feat categories remain outside this bounded source clarification.
'''
    context = {'reviewId': 'FEAT335-COPY-RELEASE-SOURCE-01',
        'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'prepared-not-sent',
        'sourceBindings': [bindings[p] for p in sorted(paths)], 'candidateContractParity': parity,
        'completeCopyProfileContract': copy_contract, 'completeSelectedContracts': contracts,
        'completeRelevantSharedRules': [rules[k] for k in ['FS-06', 'FS-08', 'FS-09']],
        'questions': ['CRS-01-canonical-copy-history-identity', 'CRS-02-profile-concentration',
                      'CRS-03-copy-strain-engine-and-limit'],
        'currentEvidence': {'sourceComponents': info(A / 'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json'),
                            'captureOnly': info(A / 'FEAT335_COPY_CAPTURE_CHECK.json')},
        'scope': 'Source clarification only; no new source ruling, paid release, current historical rerun, feat approval or runtime claimed.',
        'sendAfter': 'Actual terminal DI7-EXACT-REVIEW-01 reply; do not interrupt or duplicate the current request.',
        'ownerUsageGuard': 'Check weekly usage; stop at 50 percent used. Prepared is not sent.'}
    root.mkdir()
    (root / 'REQUEST.txt').write_text(question_text, encoding='utf-8', newline='\n')
    (root / 'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    manifest = {p.relative_to(G).as_posix(): {'bytes': bindings[p]['bytes'], 'sha256': bindings[p]['sha256']}
                for p in sorted(paths)}
    for name in ['REQUEST.txt', 'CURRENT_REVIEW_CONTEXT.json']:
        data = (root / name).read_bytes()
        manifest[name] = {'bytes': len(data), 'sha256': digest(data)}
    (root / 'PACKAGE_MANIFEST.json').write_bytes(encoded(manifest))
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(paths): z.write(p, p.relative_to(G).as_posix())
        for name in ['REQUEST.txt', 'CURRENT_REVIEW_CONTEXT.json', 'PACKAGE_MANIFEST.json']:
            z.write(root / name, name)
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(manifest) + 1
        for name, b in manifest.items():
            data = z.read(name)
            assert len(data) == b['bytes'] and digest(data) == b['sha256']
    assert bindings == {p: info(p) for p in paths}
    result = {'reviewId': context['reviewId'], 'recordedAtUtc': context['createdAtUtc'],
        'status': 'prepared-not-sent', 'archive': info(archive), 'payloadsVerified': len(manifest),
        'manifest': info(root / 'PACKAGE_MANIFEST.json'), 'request': info(root / 'REQUEST.txt'),
        'context': info(root / 'CURRENT_REVIEW_CONTEXT.json'), 'currentOperativeParity': parity,
        'sourceFilesUnchanged': True, 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0,
        'copyReleaseExecuted': False, 'selectionEnabled': False, 'exactApprovalReceived': False,
        'pushed': False, 'cosmologyReviewed': False}
    receipt.write_bytes(encoded(result))
    print(json.dumps(result))


if __name__ == '__main__':
    main()
