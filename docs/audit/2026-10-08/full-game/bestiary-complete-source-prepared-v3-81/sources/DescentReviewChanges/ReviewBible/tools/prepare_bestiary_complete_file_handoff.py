"""Consolidate existing bestiary evidence; preserve historical/current pairs.

Preparation only: no ingestion, creature authoring, audience change, cosmology
interpretation or dispatch. Refresh dependencies before the future conference.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
AUDITS = ['BESTIARY_SOURCE_RUNTIME_AUDIT.json', 'BESTIARY_HISTORY_PROVENANCE.json',
          'BESTIARY_SOURCE_CANDIDATE_VALIDATION.json', 'BESTIARY_CRAFTING_CROSSLINK_AUDIT.json']

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.resolve().relative_to(G).as_posix()

def dump(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    receipt = A / 'BESTIARY_COMPLETE_FILE_HANDOFF_PREPARATION.json'
    archive = A / 'DD_Bestiary_Complete_Source_Prepared_v1.zip'
    assert not receipt.exists() and not archive.exists(), 'Preserve existing snapshot'
    files, original_hashes, historical_pairs = set(), {}, []
    for name in AUDITS:
        p = A / name
        data = read(p)
        files.add(p)
        for path, h in data['sourceHashes'].items():
            if path in original_hashes:
                assert original_hashes[path] == h, ('Multiple historical revisions require explicit handling', path)
            original_hashes[path] = h
            files.add(G / path)
        for path, h in data.get('artifactHashes', {}).items():
            assert sha(G / path) == h
            files.add(G / path)
    assert len(original_hashes) == 278
    for path, old_hash in original_hashes.items():
        current_hash = sha(G / path)
        if current_hash != old_hash:
            folder = 'blacksmithing-before-part2-promotion' if path.endswith('/crafting_recipe_review_catalog.json') else 'blacksmithing-before-part2-repairs'
            previous = A / folder / path
            assert previous.is_file() and sha(previous) == old_hash, ('Exact historical bytes not found', path)
            files.add(previous)
            historical_pairs.append({'file': path, 'historicalFile': rel(previous),
                                     'historicalSha256': old_hash, 'currentSha256': current_hash,
                                     'treatment': 'Both complete files supplied. Historical source checks bind the historical file; current operational metadata/rules use current file and review receipts.'})
    assert len(historical_pairs) == 6
    for prefix in ['BESTIARY_SOURCE', 'BESTIARY_HISTORY']:
        p = A / (prefix + '_CONFERENCE_STATUS.json')
        d = read(p)
        assert not d['sent'] and d['reviewVerdict'] is None
        assert sha(G / d['packet']) == d['packetSha256']
        assert sha(G / d['sourceAudit']) == d['sourceAuditSha256']
        files.update([p, G / d['packet']])
    p = A / 'BESTIARY_CRAFTING_CROSSLINK_STATUS.json'
    d = read(p)
    assert not d['sent'] and d['reviewVerdict'] is None
    files.add(p)
    for name, h in d['artifactHashes'].items():
        assert sha(G / name) == h
        files.add(G / name)
    internal = read(R / 'data/director/bestiary_source_candidate_internal.json')
    public = read(R / 'data/playtest/bestiary_public_source_candidate.json')
    by = {x['id']: x for x in internal['records']}
    assert len(by) == len(internal['records']) == 67 and len(public['records']) == 26
    for row in internal['records']:
        p = G / row['source']['path']
        assert sha(p) == row['source']['sha256']
        assert p.read_text(encoding='utf-8-sig') == row['source']['originalUtf8Text']
    assert all(row == by[row['id']] for row in public['records'])
    assert sum(row['statBlock'] is not None for row in internal['records']) == 66
    cross = read(A / 'BESTIARY_CRAFTING_CROSSLINK_AUDIT.json')
    assert len(cross['harvestRows']) == 178 and len(cross['printedRecipeReferences']) == 40
    history = read(A / 'BESTIARY_HISTORY_PROVENANCE.json')
    assert len(history['runtimeWorkbookBindings']) == 707
    source_audit = read(A / 'BESTIARY_SOURCE_RUNTIME_AUDIT.json')
    assert len(source_audit['runtimeFieldDifferences']) == 184 and len(source_audit['sealedRoutingOnly']) == 5
    files.update([A / 'BESTIARY_SOURCE_RUNTIME_AUDIT.md', A / 'BESTIARY_HISTORY_PROVENANCE.md',
                  A / 'BESTIARY_SPELL_PROFILE_DEPENDENCY_INDEX.md',
                  A / 'GPT_BLACKSMITHING_PART2_EXACT_REVIEW.md', A / 'BLACKSMITHING_PART2_REPAIRS_APPLIED.json',
                  R / 'docs/mechanics/BLACKSMITHING_REVIEW_STATUS.json', Path(__file__)])
    spell_addenda = []
    for name in ['RANK6_UNDEAD_PROFILE_SOURCE_ADDENDUM', 'RANK6_7_CREATED_COMPANION_SOURCE_ADDENDUM']:
        p = A / (name + '.json')
        data = read(p)
        files.update([p, A / (name + '.md')])
        for path, h in data['protectedFiles'].items():
            assert sha(G / path) == h
            files.add(G / path)
        spell_addenda.append({'file': rel(p), 'sha256': sha(p), 'spellIds': data['spellIds'],
                              'completeComparisonMatches': len(data['completeMatches'])})
    gather = read(R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json')
    assert all(sha(G / p) == h for p, h in gather['artifactHashes'].items())
    files.update(G / p for p in gather['artifactHashes'])
    files.update([R / 'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json',
                  A / 'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md', A / 'GATHERING_128_EXACT_PROMOTION_RECEIPT.json',
                  A / 'ADVANCED_CRAFT_SOURCE_PREPARATION.json', A / 'ADVANCED_CRAFT_REVIEW_SCENARIOS.md',
                  A / 'ADVANCED_CRAFT_JOINT_SUBMISSION.json',
                  R / 'docs/mechanics/CLASS_PLAYTEST_RULES.md', R / 'docs/mechanics/SPELL_INTEGRATION_RULES.md',
                  R / 'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md', R / 'docs/mechanics/HEALING_DEATH_PLAYTEST.md',
                  R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', R / 'docs/mechanics/CONDITIONS_PLAYTEST.md',
                  R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', R / 'data/public/spell_playtests/catalog.json'])
    assert all(p.is_file() for p in files)
    report = {'status': 'complete bestiary evidence files prepared; UNSENT; current-interface refresh required before dispatch',
              'preparedAtUtc': datetime.now(timezone.utc).isoformat(),
              'historicalSourceFiles': len(original_hashes), 'unchangedHistoricalSources': 272,
              'historicalCurrentPairs': historical_pairs, 'allHistoricalBytesAvailable': True,
              'knownDossiers': 67, 'statBlocks': 66, 'publicSourceDossiers': 26,
              'all67OriginalDossierTextsExact': True, 'all26PublicRecordsMatchInternalSourceRecords': True,
              'retainedRuntimeWorkbookBindings': 707, 'retainedRuntimeFieldDifferences': 184,
              'harvestOccurrences': 178, 'printedRecipeReferences': 40,
              'unresolvedCrosslinkCounts': cross['counts'],
              'unresolvedSourceInterfaces': read(A / 'BESTIARY_SOURCE_CANDIDATE_VALIDATION.json')['counts']['unresolvedInterfacesByKind'],
              'sealedDossiers': 5, 'sealedScope': 'routing/containment evidence only; no sealed content or cosmology review',
              'namedSpellProfileAddenda': spell_addenda,
              'sent': False, 'newApprovals': 0, 'sourceInformationDeleted': 0,
              'runtimeChangedOrBuilt': False, 'publicationRoutesChanged': False,
              'dispatchPrerequisite': 'Refresh after actual advanced-crafting and any intervening spell/profile decisions; preserve this snapshot',
              'cosmology': 'literal text retained; origins/afterlife/planes and sealed content remain outside this pre-push source conference'}
    rp = A / 'BESTIARY_COMPLETE_FILE_HANDOFF_SOURCE_CHECK.json'
    assert not rp.exists()
    dump(rp, report)
    files.add(rp)
    prompt = '''PREPARED BESTIARY SOURCE REQUEST — NOT SENT. Refresh current dependencies after intervening crafting/spell decisions before dispatch.

Read the complete source/runtime, history, structured-candidate and harvesting/crafting evidence. The archive preserves67 Known Descent dossiers,66 stat blocks,26 public source routes,707 workbook/runtime bindings,184 recorded field differences and178 printed harvest occurrences. The six historical/current dependency pairs have exact old bytes, current files and the relevant Blacksmithing/gathering receipts. Read the full source questions, not just this cover.

Give finite source-authoring decisions for the actual creature procedures, missing actions/defense mappings, named identity conflicts, missing publication routes and harvest/material/recipe interfaces. Map each ruling to the exact dossier, field and printed row; retain all original and legacy records. Address the34 literal material-name matches and144 unmatched occurrences, rate/value/time/DC context differences, and38 unresolved printed recipe links without inventing donor identities from names alone. Preserve complete creature profiles and identify genuinely missing finite mechanics with explicit NEW completions. Distinguish a source-based authoring candidate from old runtime data; no regeneration or replacement is authorized by a hash match alone.

The two spell-profile addenda retain full Ghoul/Ghast/Wight/Mummy/Wraith/Zombie/Homunculus comparisons and bounded missing-profile searches. Reconcile actual spell output needs and complete existing profiles without importing another game's stat blocks or merging same-named class companions. Interpret current mechanical eligibility only where an actual source supports it; unresolved world classification stays bounded.

Keep public, restricted and Director audiences distinct. The five sealed dossier names/build routes are containment evidence only: do not review their content or cosmology. Incidental literal lore remains preserved, not reinterpreted. No origin, soul, afterlife, planar or cosmological decisions before the verified GitHub push. No source deletion, runtime installation, public disclosure or exact operational approval in this source conference. Complete cards and manuscript require their later exact review. Final joint flow precedes the authorized GitHub push; remote verification precedes the careful cosmology review.
'''
    pp = A / 'CODEX_BESTIARY_COMPLETE_FILE_HANDOFF_PROMPT_PREPARED.txt'
    assert not pp.exists()
    pp.write_text(prompt, encoding='utf-8')
    files.add(pp)
    readme = '''# Complete bestiary evidence handoff — UNSENT

This is a frozen source-conference preparation, not approved creature rules or an installed/public dataset. Read the prepared prompt and existing audits. Source, history, structured candidate, harvesting crosslinks and named spell-output addenda are included in full, with their original questions and stated search limits.

FILE_MANIFEST.json lists every full file and its hash. BESTIARY_COMPLETE_FILE_HANDOFF_SOURCE_CHECK.json verifies67 original dossier texts,26 unchanged public source records,66 stat blocks and full membership counts. Of278 historical source files,272 remain identical; all six changed files have an exact preserved historical counterpart and a complete current file. Original validation reports retain their historical scope; current rules/counts use the included current files and actual review receipts. No historical report is silently treated as a fresh validation of changed bytes.

The five sealed dossiers occur among preserved sources only for routing/containment evidence. Their content and cosmology are outside the pre-push review. Public projection requires actual source authority; a record's presence in this internal archive is not publication permission. Full current gathering/Blacksmithing context and still-pending advanced-craft sources are included with explicit status. No advanced approval is inferred.

Before the future conference, refresh any interfaces changed by actual intervening verdicts. Keep all original archives, manuscripts, source flags and aliases. No build/import scripts were executed, no runtime data or publication filter changed, and no creature, spell, material identity or cosmology decision is made by this preparation.
'''
    manifest = {rel(p): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files, key=rel)}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW.md', readme.encode('utf-8'))
        z.writestr('FILE_MANIFEST.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        for p in sorted(files, key=rel):
            z.write(p, rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(manifest) + 2
        assert all(len(z.read(p)) == m['bytes'] and hashlib.sha256(z.read(p)).hexdigest() == m['sha256'] for p, m in manifest.items())
    assert all(sha(G / p) == m['sha256'] for p, m in manifest.items())
    report.update({'bundleFile': archive.name, 'bundleSha256': sha(archive), 'bundleBytes': archive.stat().st_size,
                   'payloadFiles': len(manifest), 'zipRoundtripVerified': True,
                   'promptFile': pp.name, 'promptSha256': sha(pp),
                   'currentFileHashes': {p: m['sha256'] for p, m in manifest.items()}})
    dump(receipt, report)
    print(json.dumps({k: report[k] for k in ['status', 'knownDossiers', 'statBlocks', 'publicSourceDossiers',
                       'historicalSourceFiles', 'unchangedHistoricalSources', 'payloadFiles', 'bundleBytes', 'bundleSha256', 'sent']}))

if __name__ == '__main__':
    main()
