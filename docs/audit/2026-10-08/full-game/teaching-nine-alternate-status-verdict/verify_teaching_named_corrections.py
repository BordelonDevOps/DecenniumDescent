#!/usr/bin/env python3
"""Read-only verification of the finite TEX-01–04 pre-label amendments.

Uses Python standard library only. It does not apply corrections, modify a
repository, normalize review labels, run game procedures, or grant approvals.
Run before optional label normalization; preserve a label-only inverse proof
for the later labeled tree. The frozen archive is never written.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

EXPECTED_SHA = 'df0390f6a17a00428e102d3de2b8195d4334f1ead80493b70ffb6dfa21b03085'
B = 'DescentReviewChanges/ReviewBible/'
D = 'docs/audit/2026-10-08/full-game/'
NESTED_ZIP = D + 'DD_Low_Rank_136_Exact_Review_v1.zip'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pointer_parent(value, pointer: str):
    parts = [p.replace('~1', '/').replace('~0', '~') for p in pointer.lstrip('/').split('/')]
    parent = value
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
    return parent, key


def build_expected(archive: Path, spec: dict) -> tuple[dict, dict, list]:
    """Construct expected changed file values in memory from authentic inputs."""
    raw = archive.read_bytes()
    if digest(raw) != EXPECTED_SHA:
        raise ValueError('Unexpected submission archive SHA-256')
    originals = {}
    expected = {}
    kinds = {}
    deferred = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        nested = None

        def load(path: str) -> bytes:
            nonlocal nested
            if path in originals:
                return originals[path]
            if path in z.namelist():
                data = z.read(path)
            else:
                if nested is None:
                    nested = zipfile.ZipFile(io.BytesIO(z.read(NESTED_ZIP)))
                data = nested.read(path)
            originals[path] = data
            return data

        for correction in spec['corrections']:
            for op in correction['operations']:
                path = op['path']
                name = op['op']
                if name == 'create_text_file':
                    expected[path] = op['replacement']
                    kinds[path] = 'text'
                    continue
                if path not in expected:
                    data = load(path)
                    kinds[path] = 'json' if path.endswith('.json') else 'text'
                    expected[path] = json.loads(data) if kinds[path] == 'json' else data.decode('utf-8').replace('\r\n', '\n')
                value = expected[path]
                if name == 'replace_text':
                    if value.count(op['old']) != op['expectedOccurrences']:
                        raise ValueError(f'Wrong original occurrence count: {path}')
                    expected[path] = value.replace(op['old'], op['replacement'])
                elif name in ('replace_json_string', 'replace_text_in_json_string'):
                    parent, key = pointer_parent(value, op['pointer'])
                    if name == 'replace_json_string':
                        if parent[key] != op['old']:
                            raise ValueError(f'Wrong original JSON value: {path}{op["pointer"]}')
                        parent[key] = op['replacement']
                    else:
                        if parent[key].count(op['old']) != op['expectedOccurrences']:
                            raise ValueError(f'Wrong original embedded text: {path}{op["pointer"]}')
                        parent[key] = parent[key].replace(op['old'], op['replacement'])
                elif name == 'append_json_array':
                    parent, key = pointer_parent(value, op['pointer'])
                    parent[key].append(op['value'])
                elif name == 'set_absent_json_field':
                    parent, key = pointer_parent(value, op['pointer'])
                    if key in parent:
                        raise ValueError(f'Expected absent field: {path}{op["pointer"]}')
                    parent[key] = op['value']
                elif name == 'refresh_current_hashes':
                    deferred.append(op)
                else:
                    raise ValueError(f'Unsupported operation: {name}')
        # Also load every unchanged teaching artifact and complete comparison datasets.
        artifact_spec = json.loads(z.read(D + 'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json'))
        for p in artifact_spec['candidateFiles']:
            load(p)
        for p in z.namelist():
            if re.fullmatch(re.escape(B) + r'data/public/class_playtests/[^/]+\.json', p):
                load(p)
        for p in (
            B+'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md',
            B+'tools/device_lifecycle_playtest_rules.py',
            B+'tools/validate_device_lifecycle_playtests.py',
            B+'docs/mechanics/CLASS_PLAYTEST_RULES.md',
            B+'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
            B+'data/playtest/character_sheet_form_fields.json',
            D+'GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md',
            D+'CROSS_GUIDE_EFFICIENT_RECYCLING_CONFLICT.json',
        ):
            load(p)
    return expected, originals, deferred


def verify(root: Path, archive: Path, spec: dict) -> dict:
    rows = []

    def check(name: str, passed: bool, **details):
        rows.append({'id': f'TEX-CHECK-{len(rows)+1:03}', 'name': name, 'passed': bool(passed), **details})

    expected, originals, deferred = build_expected(archive, spec)
    check('Authentic immutable archive', True, sha256=EXPECTED_SHA)
    # Only current hash values depend on the user's harmless JSON serialization choices.
    for op in deferred:
        parent, key = pointer_parent(expected[op['path']], op['pointer'])
        for path in op['targetPaths']:
            f = root/path
            if not f.is_file():
                check('Required corrected hash target exists', False, path=path)
                continue
            parent[key][path] = digest(f.read_bytes())
    for path, value in expected.items():
        f = root/path
        if not f.is_file():
            check('Required corrected file exists', False, path=path)
            continue
        try:
            actual = json.loads(f.read_bytes()) if path.endswith('.json') else f.read_text(encoding='utf-8').replace('\r\n', '\n')
            check('Exact finite amendment, no unrelated change (pre-label)', actual == value, path=path)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            check('Corrected file parses', False, path=path, error=str(exc))
    for path, raw in originals.items():
        if path in expected:
            continue
        f = root/path
        check('Unchanged source/comparison/teaching artifact preserved', f.is_file() and f.read_bytes() == raw, path=path, expectedSha256=digest(raw))
    pub_path=B+'data/crafting/advanced_craft_recipe_candidate_public.json'
    int_path=B+'data/director/advanced_craft_recipe_candidate_internal.json'
    if (root/pub_path).exists() and (root/int_path).exists():
        pub=json.loads((root/pub_path).read_bytes())
        full=json.loads((root/int_path).read_bytes())
        old_pub=json.loads(originals[pub_path]);old_full=json.loads(originals[int_path])
        check('Whole public operating-guide parity', pub['operatingGuideText'] == (root/B/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md').read_text())
        td=full['procedureSections']['TD-13']['text']
        guide=(root/B/'docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md').read_text()
        check('Full current TD-13 paragraph in internal guide', guide.count(td)==1)
        for key in ('cards','bodyModels','enchantingHostModels'):
            check('All internal objects unchanged: '+key, full[key]==old_full[key])
            check('All public objects unchanged: '+key, pub[key]==old_pub[key])
        check('All 48 Tinker interfaces preserved',full['tinkerInterfaceRegister']==old_full['tinkerInterfaceRegister'])
        check('Historical source verdict hash is not relabeled',full['procedureSections']['TD-13']['sourceVerdictSha256']==old_full['procedureSections']['TD-13']['sourceVerdictSha256'])
    failed=[x for x in rows if not x['passed']]
    return {'reviewId':'TEX-EXACT-2026-10-11','scope':'Read-only pre-label text/object/current-hash preservation and parity checks. Not actual game procedures, human trials, or repository fulfillment authority by itself.','checks':len(rows),'passed':len(rows)-len(failed),'failed':failed,'rows':rows}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive',type=Path,required=True)
    ap.add_argument('--root',type=Path,required=True,help='Complete corrected pre-label tree')
    ap.add_argument('--spec',type=Path,default=Path(__file__).with_name('TEX_01_04_CORRECTIONS.json'))
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    result=verify(args.root,args.archive,json.loads(args.spec.read_text()))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('reviewId','checks','passed','failed')},indent=2))
    raise SystemExit(1 if result['failed'] else 0)

if __name__=='__main__':
    main()
