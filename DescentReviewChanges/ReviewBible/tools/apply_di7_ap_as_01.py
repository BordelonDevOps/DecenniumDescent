"""Apply only GPT's named AP-AS-01 interface, preserving reversible exact evidence."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

G = Path('C:/Github/DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
V = A / 'di7-joint-review-01-verdict'


def digest(b):
    return hashlib.sha256(b).hexdigest()


def info(p, b=None):
    b = p.read_bytes() if b is None else b
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': digest(b)}


def encoded(d, crlf=False):
    b = (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return b.replace(b'\n', b'\r\n') if crlf else b


def node(d, pointer):
    parts = pointer.strip('/').split('/')
    for p in parts[:-1]:
        d = d[int(p)] if isinstance(d, list) else d[p]
    return d, int(parts[-1]) if isinstance(d, list) else parts[-1]


def main():
    operations_path = A / 'DI7_AP_AS_01_DERIVED_OPERATIONS.json'
    control_path = A / 'DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json'
    preservation = A / 'source-before-di7-ap-as-01'
    assert all(not p.exists() for p in [operations_path, control_path, preservation])
    contract_path = V / 'ALIGNMENT_SUGGESTION_AP_AS_01.json'
    contract = json.loads(contract_path.read_bytes())
    primary, guide = contract['operationsOnNewDerivedCopies']
    old, new = primary['old'], primary['replacement']
    planned = []

    def json_change(rel, edits):
        p = R / rel
        before = p.read_bytes()
        original = json.loads(before)
        crlf = before == encoded(original, True)
        assert before == encoded(original, crlf), rel
        updated = deepcopy(original)
        for pointer, expected, replacement in edits:
            obj, key = node(updated, pointer)
            assert obj[key] == expected, (rel, pointer)
            obj[key] = deepcopy(replacement)
        reverse = deepcopy(updated)
        for pointer, expected, replacement in reversed(edits):
            obj, key = node(reverse, pointer)
            assert obj[key] == replacement
            obj[key] = deepcopy(expected)
        assert reverse == original and encoded(reverse, crlf) == before
        after = encoded(updated, crlf)
        assert before != after
        planned.append((p, before, after, [{'pointer': e[0], 'old': e[1], 'replacement': e[2]} for e in edits]))
        return updated, after

    catalog = R / 'data/public/spell_playtests/catalog.json'
    assert digest(catalog.read_bytes()) == primary['sourceFileSha256']
    original_catalog = json.loads(catalog.read_bytes())
    assert original_catalog['spells'][329]['id'] == primary['idGuard']
    updated_catalog, catalog_bytes = json_change('data/public/spell_playtests/catalog.json', [(primary['pointer'], old, new)])
    new_binding = info(catalog, catalog_bytes)
    for rel in ['data/playtest/spell_drafts/candidate_enchantment_rank1.json', 'data/playtest/spell_drafts/batch_enchantment_rank1.json']:
        d = json.loads((R / rel).read_bytes())
        assert d['spells'][9]['id'] == primary['idGuard']
        json_change(rel, [('/spells/9/resolution', old, new)])

    dependency_rel = 'data/public/feat_candidates/exact_01/spell_dependencies.json'
    dependencies = json.loads((R / dependency_rel).read_bytes())
    edits = [('/spells/alignment-suggestion/completeCurrentProcedureCard/operational/resolution', old, new)]
    bindings = 0
    for spell_id, entry in dependencies['spells'].items():
        binding = entry['binding']
        if binding['file'] != primary['path']:
            continue
        bindings += 1
        assert binding['sha256'] == primary['sourceFileSha256'] and binding['bytes'] == len(catalog.read_bytes())
        index = int(binding['pointer'].split('/')[-1])
        assert original_catalog['spells'][index]['id'] == spell_id
        assert entry['completeCurrentProcedureCard'] == original_catalog['spells'][index]
        for key in ['bytes', 'sha256']:
            edits.append((f'/spells/{spell_id}/binding/{key}', binding[key], new_binding[key]))
    assert bindings == 202
    new_dependencies, _ = json_change(dependency_rel, edits)
    for spell_id, entry in new_dependencies['spells'].items():
        assert entry['originalCatalogRecord'] == dependencies['spells'][spell_id]['originalCatalogRecord']
        if entry['binding']['file'] == primary['path']:
            assert entry['completeCurrentProcedureCard'] == updated_catalog['spells'][int(entry['binding']['pointer'].split('/')[-1])]

    cohort_rel = 'data/director/feat_candidates/exact_01/cohorts/general_combat.json'
    cohort_before = json.loads((R / cohort_rel).read_bytes())
    cohort, _ = json_change(cohort_rel, [('/completeCurrentSpellDependencies/alignment-suggestion/completeCurrentProcedureCard/operational/resolution', old, new)])
    assert cohort['records'] == cohort_before['records']
    assert cohort['completeCurrentSpellDependencies']['alignment-suggestion']['completeOriginalCatalogObject'] == cohort_before['completeCurrentSpellDependencies']['alignment-suggestion']['completeOriginalCatalogObject']
    assert cohort['completeCurrentSpellDependencies']['alignment-suggestion']['completeCurrentProcedureCard'] == updated_catalog['spells'][329]

    def text_change(rel, original, replacement, expected_sha=None):
        p = R / rel
        before = p.read_bytes()
        if expected_sha:
            assert digest(before) == expected_sha
        old_bytes, new_bytes = original.encode(), replacement.encode()
        assert before.count(old_bytes) == 1 and new_bytes not in before
        after = before.replace(old_bytes, new_bytes, 1)
        assert after.count(new_bytes) == 1 and after.replace(new_bytes, old_bytes, 1) == before
        planned.append((p, before, after, [{'type': 'exact-text', 'old': original, 'replacement': replacement}]))

    text_change('docs/mechanics/SPELL_INTEGRATION_RULES.md', guide['old'], guide['replacement'], guide['sourceFileSha256'])
    text_change('docs/mechanics/SPELL_PLAYTEST_STARTER.md', old, new)
    text_change('docs/feats/exact-candidate-01/SPELL_PAYLOADS.md', json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False))
    assert len(planned) == 8
    changes = []
    for p, before, after, edits in planned:
        assert p.read_bytes() == before
        preserved = preservation / p.relative_to(G)
        preserved.parent.mkdir(parents=True, exist_ok=True)
        preserved.write_bytes(before)
        assert preserved.read_bytes() == before
        changes.append({'before': {**info(p, before), 'preservedCopy': preserved.relative_to(G).as_posix()}, 'after': info(p, after), 'operations': edits, 'exactInverseBytesVerified': True})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded([c['before'] for c in changes]))
    for p, before, after, _ in planned:
        assert p.read_bytes() == before
        p.write_bytes(after)
        assert p.read_bytes() == after
    now = datetime.now(timezone.utc).isoformat()
    operations_path.write_bytes(encoded({'recordedAtUtc': now, 'id': 'DI7-AP-AS-01-active-counterparts', 'authority': info(contract_path), 'changes': changes,
        'activeFilesChanged': 8, 'wholeCatalogDependencyBindingsRefreshed': bindings, 'allUnlistedFieldsByteReversible': True,
        'historicalOriginalCatalogObjectsUnchanged': True, 'featRecordsUnchanged': True, 'ordinarySpellCount': 848,
        'ordinaryReviewedCountUnchanged': 412, 'ordinaryPendingCountUnchanged': 436, 'sourceInformationDeleted': 0, 'selectionPromotion': False}))
    control_path.write_bytes(encoded({'recordedAtUtc': now, 'id': 'AP-AS-01', 'authority': info(contract_path), 'application': info(operations_path),
        'scope': contract['scope'], 'classification': contract['classification'], 'primaryActiveReaders': [primary['path'], guide['path']],
        'activeMirrors': [info(p) for p, _, _, _ in planned],
        'historicalCopiesRetained': ['originalCatalogRecord in public exact_01 spell dependencies', 'completeOriginalCatalogObject in internal general_combat cohort',
            'original divination_rank7, abjuration_conjuration_rank4, and general_combat operating proposals and bound review-input copies'],
        'historicalCopiesAreEvidenceOnly': True, 'newDI7CandidatesMustBindUpdatedActiveCounterpart': True,
        'alignmentPurgeApprovedOrSelectable': False, 'otherSpellsOrAlignmentEffectsInheritException': False,
        'sourceInformationDeleted': 0, 'runtimeImplemented': False, 'cosmologyReviewed': False, 'pushed': False}))
    print(json.dumps({'operations': info(operations_path), 'control': info(control_path), 'files': 8, 'bindingRefreshes': bindings, 'inverseBytesVerified': True}))


if __name__ == '__main__':
    main()
