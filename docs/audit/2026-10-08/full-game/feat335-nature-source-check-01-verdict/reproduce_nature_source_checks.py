#!/usr/bin/env python3
"""Read-only submitted-source audit and exact descendant/reference checks.

Python standard library only. This is NOT a Nature/feat/class runtime.
Optionally write the three amended reference files to a separate directory.
The input ZIP is never modified or extracted over a repository.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import stat
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
BASE = 'DescentReviewChanges/ReviewBible/'
CARD = 'ranger.base.nature-s-whisper'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_pointer(obj: Any, pointer: str) -> Any:
    if pointer == '':
        return obj
    if not pointer.startswith('/'):
        raise ValueError('JSON pointer must be absolute')
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    return obj


def put_pointer(obj: Any, pointer: str, value: Any) -> None:
    prefix, token = pointer.rsplit('/', 1)
    parent = get_pointer(obj, prefix)
    token = token.replace('~1', '/').replace('~0', '~')
    if isinstance(parent, list):
        parent[int(token)] = value
    else:
        parent[token] = value


def task_reference(face: int, modifier: int, dc: int) -> dict[str, Any]:
    """Only the supplied Core fixed-DC degree arithmetic; no task permission."""
    if type(face) is not int or not 1 <= face <= 20:
        raise ValueError('One legal d20 face required')
    total = face + modifier
    degree = 3 if total >= dc + 10 else 2 if total >= dc else 0 if total <= dc - 10 else 1
    degree = min(3, degree + 1) if face == 20 else max(0, degree - 1) if face == 1 else degree
    return {'total': total, 'degree': ['critical-failure', 'failure', 'success', 'critical-success'][degree], 'success': degree >= 2}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive', type=Path)
    ap.add_argument('--descendants', type=Path, help='Optional new/separate output directory')
    args = ap.parse_args()
    binding = json.loads((HERE / 'SUBMISSION_BINDING.json').read_bytes())
    corrections = json.loads((HERE / 'EXACT_NATURE_CORRECTIONS.json').read_bytes())
    rows: list[dict[str, Any]] = []

    def check(label: str, ok: bool, category: str, detail: Any = None) -> None:
        row = {'id': f'NC-{len(rows)+1:03d}', 'category': category, 'check': label, 'pass': bool(ok)}
        if detail is not None:
            row['detail'] = detail
        rows.append(row)
        if not ok:
            raise ValueError(f'Failed check: {label}')

    raw = args.archive.read_bytes()
    check('exact ZIP byte count', len(raw) == binding['bytes'], 'submission integrity')
    check('exact ZIP SHA-256', digest(raw) == binding['sha256'], 'submission integrity')
    with zipfile.ZipFile(args.archive) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        check('no duplicate ZIP entries', len(names) == len(set(names)), 'submission integrity')
        check('safe regular payload paths', all(not PurePosixPath(i.filename).is_absolute()
              and '..' not in PurePosixPath(i.filename).parts
              and not stat.S_ISLNK(i.external_attr >> 16) and not i.is_dir() for i in infos), 'submission integrity')
        manifest_raw = z.read(binding['manifest'])
        check('submitted root manifest hash', digest(manifest_raw) == binding['manifestSha256'], 'submission integrity')
        manifest = json.loads(manifest_raw)
        # Root keys are the ZIP members. REQUEST/QUESTIONS inner path metadata differs deliberately.
        check('all 23 payloads and manifest, no extra members', len(manifest) == 23
              and set(names) == set(manifest) | {binding['manifest']}, 'submission integrity')
        data = {name: z.read(name) for name in manifest}
        for name, meta in manifest.items():
            check(name + ' bytes', len(data[name]) == meta['bytes'], 'payload preservation')
            check(name + ' SHA-256', digest(data[name]) == meta['sha256'], 'payload preservation')

    questions = json.loads(data['QUESTIONS.json'])
    check('four exact question IDs', [q['id'] for q in questions['questions']] == [f'NWQ-{i:02d}' for i in range(1, 5)], 'source binding')
    rp = BASE + 'data/public/class_playtests/ranger.json'
    mp = BASE + 'docs/mechanics/classes/ranger.md'
    sp = BASE + 'data/public/feat_candidates/exact_01/supplements.json'
    cp = BASE + 'data/public/feat_candidates/exact_01/candidate.json'
    apath = 'docs/audit/2026-10-08/full-game/FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    ranger = json.loads(data[rp]); card = ranger['cards'][7]
    check('exact complete Ranger source identity', card['id'] == CARD and card['sourceKind'] == 'active', 'source binding')
    check('null spell rank is present, not zero or absent', 'spellRank' in card and card['spellRank'] is None, 'source binding')
    check('no component/tag defaults supplied by source', 'components' not in card and 'tags' not in card, 'source binding')
    check('all explicit native header values retained', {k:card[k] for k in ['activation','cost','rangeAndTarget','duration','frequency']} == {
        'activation':'Action','cost':'1 RP','rangeAndTarget':'Natural terrain within 15 ft','duration':'1 minute','frequency':'Recharge 3'}, 'source binding')
    check('full historical spell wording retained', card['source']['originalText'] == "Nature's Whisper: Cast a minor nature spell that reveals hidden creatures or tracks within a small area.", 'source binding')
    candidate = json.loads(data[cp]); contracts = json.loads(data[apath])
    feat = next(c for c in candidate['feats'] if c['id'] == 'versatile_mastery')
    contract = next(c for c in contracts['records'] if c['id'] == 'versatile_mastery')
    check('complete current feat procedure mirrors agree', feat['operationalRules'] == feat['payloadOperational'] == contract['completeOperativeProcedure'], 'source binding')
    check('actual original feat matches acquisition source', feat['sourceObject'] == contract['originalObject'], 'source binding')
    check('no feat/candidate approval or selection inferred', not candidate['selectionEnabled'] and not feat['selectionEnabled'] and not feat['exactApproved'] and not feat['runtimeApproved'], 'source binding')
    supp = json.loads(data[sp]); menu = supp['groups'][8]
    check('all twelve distinct SUP09 entries retained', menu['id'] == 'SUP-09' and len(menu['value']) == len({x['sourceId'] for x in menu['value']}) == 12, 'source binding')
    check('specific borrowed Nature row source and minimum', menu['value'][5]['sourceId'] == CARD and menu['value'][5]['actualSourceClass'] == 'Ranger' and menu['value'][5]['minimumBorrowerTotalLevel'] == 1, 'source binding')
    check('technique exception in shared class rules', 'Printed class techniques pay printed costs and cause no automatic spell Dissonance' in data[BASE+'docs/mechanics/CLASS_PLAYTEST_RULES.md'].decode(), 'source binding')
    check('no rank-zero Counterspell fallback in spell rules', 'An unassigned rank is not automatically zero.' in data[BASE+'docs/mechanics/SPELL_INTEGRATION_RULES.md'].decode(), 'source binding')
    check('generic nonspell Ready pays on release', 'For ordinary nonspell actions, feature/ammunition costs are paid on release unless text charges setup.' in data[BASE+'docs/mechanics/COMBAT_ACTION_PLAYTEST.md'].decode(), 'source binding')

    amended = dict(data)
    descendant_meta = []
    check('exactly three operations on three files', len(corrections['operations']) == len({o['path'] for o in corrections['operations']}) == 3, 'exact amendments')
    for op in corrections['operations']:
        path = op['path']; old_raw = data[path]
        check(op['id']+' full-file guard', len(old_raw) == op['expectedFileBytes'] and digest(old_raw) == op['expectedFileSha256'], 'exact amendments')
        if op['op'] == 'replace_json_string':
            before = json.loads(old_raw)
            check(op['id']+' exact pointer old value', get_pointer(before, op['pointer']) == op['old'], 'exact amendments')
            guards = op.get('recordGuards', []) + ([op['recordGuard']] if 'recordGuard' in op else [])
            check(op['id']+' exact record identity guards', all(get_pointer(before, g['pointer']) == g['equals'] for g in guards), 'exact amendments')
            old_token = json.dumps(op['old'], ensure_ascii=False).encode()
            new_token = json.dumps(op['replacement'], ensure_ascii=False).encode()
        else:
            old_token = op['old'].encode(); new_token = op['replacement'].encode()
        check(op['id']+' one exact lexical occurrence', old_raw.count(old_token) == op['expectedOccurrences'] == 1, 'exact amendments')
        new_raw = old_raw.replace(old_token, new_token, 1)
        check(op['id']+' replacement byte inverse', new_raw.count(new_token) == 1 and new_raw.replace(new_token, old_token, 1) == old_raw, 'exact amendments')
        if op['op'] == 'replace_json_string':
            after = json.loads(new_raw)
            check(op['id']+' full intended value', get_pointer(after, op['pointer']) == op['replacement'], 'exact amendments')
            restored = copy.deepcopy(after); put_pointer(restored, op['pointer'], op['old'])
            check(op['id']+' no other JSON object/field change', restored == before, 'exact amendments')
        else:
            check('Ranger historical details/source preserved', card['source']['originalText'].encode() in new_raw, 'exact amendments')
        amended[path] = new_raw
        descendant_meta.append({'path':path,'sourceSha256':digest(old_raw),'bytes':len(new_raw),'sha256':digest(new_raw)})
        if args.descendants:
            dest = args.descendants / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and dest.read_bytes() != new_raw:
                raise ValueError(f'Refusing to overwrite differing existing output: {dest}')
            dest.write_bytes(new_raw)

    nc = json.loads(amended[rp])['cards'][7]
    check('native full manuscript/effect parity', nc['effect'].replace('\n','\r\n').encode() in amended[mp] if b'\r\n' in amended[mp] else nc['effect'].encode() in amended[mp], 'derived parity')
    check('full native procedure included verbatim in borrowed row', json.loads(amended[sp])['groups'][8]['value'][5]['proposedBorrowedProcedure'].endswith(nc['effect']), 'derived parity')
    for k in card:
        if k != 'effect':
            check('Ranger /cards/7/'+k+' unchanged', nc[k] == card[k], 'derived preservation')
    check('all other Ranger cards and engines/schedules unchanged',
          json.loads(amended[rp])['cards'][:7] + json.loads(amended[rp])['cards'][8:] == ranger['cards'][:7] + ranger['cards'][8:]
          and json.loads(amended[rp])['engine'] == ranger['engine'], 'derived preservation')
    check('other20 submitted payloads byte-identical', all(amended[p] == data[p] for p in data if p not in {rp,mp,sp}), 'derived preservation')
    check('all335 original/candidate and acquisition objects untouched', amended[cp] == data[cp] and amended[apath] == data[apath], 'derived preservation')
    report = json.loads(data['docs/audit/2026-10-08/full-game/FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json'])
    check('reported362/38 evidence recorded, not re-executed', report['checks'] == 362 and len(report['histories']) == 38
          and any('minor-Weave clearance' in x for x in report['limitations']), 'evidence qualification')
    present_report_bindings = [x for x in report['sourceBindings'] if x['path'] in data]
    check('all report bindings actually present match submitted bytes', all(len(data[x['path']]) == x['bytes'] and digest(data[x['path']]) == x['sha256'] for x in present_report_bindings), 'evidence qualification', {'presentBindings':len(present_report_bindings),'otherBindingsNotAvailableInThisScopedPacket':len(report['sourceBindings'])-len(present_report_bindings)})
    check('old Nature clearance premise is visibly unimplemented', "owner['actualMinorWeaveClearance']" in data[BASE+'tools/feat335_borrowed_stunts.py'].decode(), 'evidence qualification')
    missing = [name for name in ['core_playtest_rules.py','combat_playtest_rules.py','feat_exact_01_acquisition_models.py','feat335_allowance_bindings.py'] if BASE+'tools/'+name not in data]
    check('declare absent borrowed-suite helpers, no fabricated rerun', len(missing) == 4, 'evidence qualification')

    # Executed arithmetic only: these assert neither actor/world legitimacy nor the full procedure.
    bard = json.loads(data[BASE+'data/public/Decennium_Descent_Bard_Playtest_v0_1.json'])
    check('Bard4 source maximum7 and one-RP remainder6', bard['rpByClassLevel'][3] == 7 and bard['rpByClassLevel'][3] - 1 == 6, 'reference arithmetic')
    for label, face, mod, dc, total, degree in [
        ('trained own WIS1 plus PB2, selected advantage face12',12,3,15,15,'success'),
        ('untrained own WIS1, no borrowed skill PB',12,1,15,13,'failure'),
        ('natural20 Core shift retained',20,0,22,20,'success'),
        ('natural1 Core shift retained',1,9,10,10,'failure')]:
        got = task_reference(face, mod, dc)
        check(label, got['total'] == total and got['degree'] == degree, 'reference arithmetic')
    def choose_reference(faces: list[int], advantages: int, disadvantages: int) -> tuple[int, str]:
        mode = 'normal' if bool(advantages) == bool(disadvantages) else 'advantage' if advantages else 'disadvantage'
        if len(faces) != (1 if mode == 'normal' else 2):
            raise ValueError('Wrong face count after source cancellation')
        return (faces[0] if mode == 'normal' else max(faces) if mode == 'advantage' else min(faces)), mode
    check('two advantage sources cancel against one disadvantage', choose_reference([7], 2, 1) == (7, 'normal'), 'reference arithmetic')
    check('uncancelled advantage selects one higher face', choose_reference([2,12], 1, 0) == (12, 'advantage'), 'reference arithmetic')
    check('one-minute deadline begins at resolution61', 61+60 == 121 and 120<121 and not 121<121, 'reference arithmetic')
    check('Ready release5 deadline65, not setup0 deadline60', 5+60 == 65 and 5<6, 'reference arithmetic')
    check('late task outcome130 misses deadline121', not 130<121, 'reference arithmetic')
    check('fixed-area/current-range example', abs(20-5)==15 and abs(21-5)==16 and 30>15, 'reference arithmetic')
    counter = 3; trail=[]
    for _ in range(3):
        counter=max(0,counter-1);trail.append(counter)
    check('three regular recharge ticks', trail == [2,1,0] and 3*6 == 18, 'reference arithmetic')
    expectations = json.loads((HERE/'FINITE_NATURE_EXPECTATIONS.json').read_bytes())
    check('sixteen authored groups distinctly labeled unexecuted', len(expectations['groups'])==16
          and all('not executed' in x['status'] for x in expectations['groups']), 'evidence qualification')
    check('four question coverage, no whole335 gate', {q for g in expectations['groups'] for q in g['questions']} == {f'NWQ-{i:02d}' for i in range(1,5)}, 'evidence qualification')

    result = {'reviewId':'FEAT335-NATURE-SOURCE-CHECK-01','submission':binding,'checks':len(rows),'passed':sum(x['pass'] for x in rows),'failed':[],
              'categories':dict(Counter(x['category'] for x in rows)), 'results':rows,'referenceDescendants':descendant_meta,
              'limits':{'reported362SuiteRerun':False,'missingBorrowedSuiteHelpers':missing,'sixteenFollowthroughGroupsExecuted':False,
                        'worldAuthentication':False,'fullNatureRuntime':False,'fullFeatApproval':False,'cosmologyReviewed':False}}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
