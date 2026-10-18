"""Package complete sources for the two unadopted memory design forks."""
from datetime import datetime, timezone
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(p):
    return json.loads(p.read_bytes())


def main():
    candidatepath = R / 'data/director/spell_review/memory_2_conference_01.json'
    candidate = read(candidatepath)
    root = A / 'memory-2-conference-01'
    archive = A / 'DD_Memory_2_Conference_01.zip'
    preparation = A / 'MEMORY_2_CONFERENCE_01_PREPARATION.json'
    requestpath = A / 'MEMORY_2_CONFERENCE_01_REQUEST.txt'
    assert not root.exists() and not archive.exists() and not preparation.exists() and not requestpath.exists()
    sources = {s['path']: s for s in candidate['sourceBindings']}
    checks = []

    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name

    def add(path):
        binding = info(path)
        sources[binding['path']] = binding

    for path in [candidatepath, A / 'MEMORY_2_CONFERENCE_CHECK_01.json', R / 'tools/prepare_memory2_conference_01.py', Path(__file__)]:
        add(path)
    for counterpart in candidate['completeCurrentCounterparts']:
        data = read(G / counterpart['source']['path'])
        ck('Exact whole current counterpart ' + counterpart['spellId'], at(data, counterpart['wholeCardPointer']) == counterpart['completeCurrentCard'])
        card = counterpart['completeCurrentCard']
        op = card.get('operational', card)
        for field in ['sourceReview', 'reviewEvidence']:
            for relative in op.get(field, []):
                add(G / relative)
    wizard = read(R / 'data/public/class_playtests/wizard.json')
    actors = []
    for vector in candidate['conditionalConferenceVectors']:
        actors.extend(value for value in vector.values() if isinstance(value, dict) and value.get('class') == 'Wizard' and 'actualPreparedMatrix' in value)
    for i, actor in enumerate(actors):
        ck('Actual Wizard RP maximum ' + str(i), wizard['rpByClassLevel'][actor['level'] - 1] == actor['RPBefore'])
        ck('Actual Wizard rank ceiling ' + str(i), wizard['maxSpellRankByClassLevel'][actor['level'] - 1] >= actor['generatingRank'])
        ck('Explicit cost ledger ' + str(i), actor['RPBefore'] - actor['quotedBaseAndFinalCost'] == actor['RPAfter'])
        ck('Actual DC ' + str(i), 8 + actor['PB'] + (actor['INT'] - 10) // 2 == actor['spellDC'])
    root.mkdir()
    frozen = []
    for binding in sources.values():
        path = G / binding['path']
        ck('Source hash ' + binding['path'], info(path) == binding)
        copy = root / 'sources' / binding['path']
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        ck('Exact frozen copy ' + binding['path'], info(copy)['sha256'] == binding['sha256'])
        frozen.append({**binding, 'archivePath': 'sources/' + binding['path']})
    manifest = {'id': 'MEMORY-2-CONFERENCE-01-MANIFEST', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'candidate': info(candidatepath), 'sources': frozen, 'sourceCount': len(frozen), 'completeOriginalProcedures': 2, 'originalScenarios': 4, 'conditionalTraces': 4, 'designQuestions': 8, 'status': 'Systemic design conference only, unsent/unadopted', 'newRuleAdoptions': 0}
    (root / 'MANIFEST.json').write_bytes(encoded(manifest))
    (root / 'LOCAL_PREFLIGHT.json').write_bytes(encoded({'checks': checks, 'checkCount': len(checks), 'failureCount': 0, 'runtimeTestsExecuted': 0, 'scope': 'Exact source/copy/pointer/access and arithmetic checks, not semantic acceptance.'}))
    (root / 'README.md').write_text('''# Two memory sources: design conference

Read MANIFEST.json and every complete procedure in the bound candidate. Preserve the original Woven Threads and Haze of Forgetting procedures and all four original scenario obligations. These are unadopted prior proposals. The new four traces are explicitly conditional design comparisons, not adopted memory rules or game-runtime tests.

Resolve the eight actual design questions before new systemic authorship. Give each question an explicit disposition and explain any different choice. Return complete replacement procedure/shared-rule text where needed, not summary-only instructions. Inherit actual access, casting, task/save, source protection and antimagic interfaces without reopening them. Original shared-proposal examples are historical; prepared-Wizard Dissonance follows the actual current class source.

The packet's full sources include current Disrupt Memory, Minor Illusion, Lesser Antimagic and Greater Dispel counterparts, class foundations, the accepted interface registry and source books' extracted records. Disrupt Memory's six-second firsthand loss and express concentration ending remain its own rule. No memory discussion decides cosmology, player consent, real world history or future agency. Do not invent a generic memory-restoration ability.

Report archive/source/candidate hashes, actual files and procedures read, current pointers verified, findings with exact locations, all question dispositions and complete before/after corrections. State explicitly whether any conditional vector depends on a rejected rule. Do not count these spells reviewed or adopted merely because the design conference is finished.
''', encoding='utf-8')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(root.rglob('*')):
            if path.is_file():
                z.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(frozen) + 3
        for binding in frozen:
            raw = z.read(binding['archivePath'])
            assert len(raw) == binding['bytes'] and hashlib.sha256(raw).hexdigest() == binding['sha256']
    binding = info(archive)
    request = f'''Please confer on the two systemic memory sources Woven Threads and Haze of Forgetting using the attached DD_Memory_2_Conference_01.zip ({binding['bytes']} bytes; SHA-256 {binding['sha256']}). This is video-game-only development and a design conference BEFORE any substantial new systemic memory rule is adopted.

The packet preserves both complete earlier procedures, exact source/access records, all four original cases and four explicit conditional traces. All {len(frozen)} full source files are frozen and verified. Read the candidate's eight concrete design forks and dispose of each. Resolve persistence, finite replacement, real event-time provenance, evidence-based recovery, recoverable interval/evidence boundaries, overlapping original DCs, Haze area origin and separation from actual state/agency. If approving a new shared recovery rule, provide complete harmonized text for both sources. Do not extend it to the already reviewed Disrupt Memory.

Verify the exact source and pointer evidence and recompute the conditional cases against your chosen text. Return a downloadable review archive with source verification, question dispositions, exact before/after replacements, all case findings and bounded verdict. This is not exact acceptance, adoption, runtime testing, balance, cosmology or whole-game closure.
'''
    requestpath.write_text(request, encoding='utf-8')
    preparation.write_bytes(encoded({'archive': binding, 'candidate': info(candidatepath), 'manifest': info(root / 'MANIFEST.json'), 'localPreflight': info(root / 'LOCAL_PREFLIGHT.json'), 'request': info(requestpath), 'sourceCount': len(frozen), 'checkCount': len(checks), 'allArchiveSourceHashesVerified': True, 'submitted': False, 'adopted': False, 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0}))
    print(json.dumps({'archive': binding, 'fullSources': len(frozen), 'packageChecks': len(checks), 'originalProcedures': 2, 'originalCases': 4, 'conditionalTraces': 4, 'questions': 8}))


if __name__ == '__main__':
    from pathlib import Path
    main()
