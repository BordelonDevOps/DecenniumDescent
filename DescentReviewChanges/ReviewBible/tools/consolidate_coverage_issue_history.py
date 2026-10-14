"""Preserve old coverage checkpoints while correcting their active queue stage."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
AUDIT = PROJECT / 'docs/audit/2026-10-08/full-game'
DATA = ROOT / 'data/playtest/game_development_coverage.json'
DOC = ROOT / 'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md'
RENDERER = ROOT / 'tools/build_game_coverage.py'
START = PROJECT / 'START_HERE.md'
HANDOFF = AUDIT / 'GPT_REVIEW_CONTINUATION_HANDOFF.md'
BACKUP = AUDIT / 'coverage-ledger-before-status-consolidation'
HISTORY = AUDIT / 'COVERAGE_ISSUE_HISTORY_2026-10-11.md'
RECEIPT = AUDIT / 'COVERAGE_ISSUE_HISTORY_REGISTRATION.json'
PREFIX = 'docs/audit/2026-10-08/full-game/'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return path.relative_to(PROJECT).as_posix()


def main():
    assert not BACKUP.exists() and not HISTORY.exists() and not RECEIPT.exists()
    frozen = json.loads((AUDIT / 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json').read_text(encoding='utf-8'))['currentFileHashes']
    changed_paths = [DATA, DOC, RENDERER, START, HANDOFF]
    assert all(rel(p) not in frozen for p in changed_paths)
    assert all(sha(PROJECT / p) == h for p, h in frozen.items())
    before = json.loads(DATA.read_text(encoding='utf-8'))
    packet = copy.deepcopy(before)
    now = datetime.now(timezone.utc).isoformat()
    mappings = [
        ('tinker', 'Tinker class/device interface preparation',
         'The 18 TD class/device source questions have bounded authoring decisions; all 43 Tinkering recipes completed the advanced-recipe exact review. Use TD-01–18 with the fulfilled LAX TI-04 correction for identity, ownership, commands, repair, fabrication and debris resources. Retain the individual class-card review scopes; game-wide class/device integration, runtime and human use remain open.',
         'Advanced source decisions, AEX fulfillment and the later LAX correction supersede the earlier pending-recipe/source-conference checkpoint. They do not promote all 48 class cards.',
         ['GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md', 'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json', 'LANGUAGE_EXACT_FULFILLMENT.json']),
        ('illusion', '26 remaining low-rank Illusion',
         'All 26 low-rank Illusion identities are included in the submitted 137-spell conference. Duration, range, target, variant, alias and Panicked conflicts still require finite decisions, complete candidate authoring and exact review. No new spell approval.',
         'The preserved preparation checkpoint is now part of the submitted v3 conference; its mechanical questions remain open.',
         ['LOW_RANK_SPELLS_V3_SUBMISSION.json', 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json']),
        ('universal', '23 low-rank Universal',
         'All 23 low-rank Universal identities are included in the submitted 137-spell conference. Preserve quickening, copying, delaying and redirection effects while obtaining finite action, resource, provenance and replay decisions; then author complete candidates and obtain exact review. No new spell approval.',
         'The preserved preparation checkpoint is now part of the submitted v3 conference; its mechanical questions remain open.',
         ['LOW_RANK_SPELLS_V3_SUBMISSION.json', 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json']),
        ('transmutation', '29 low-rank Transmutation',
         'All 29 low-rank Transmutation identities are included in the submitted 137-spell conference. Preserve Stone Shape variants and every material, preservation, body and movement clause; obtain source decisions, complete candidate authoring and exact review. No new spell approval.',
         'The preserved preparation checkpoint is now part of the submitted v3 conference; its mechanical questions remain open.',
         ['LOW_RANK_SPELLS_V3_SUBMISSION.json', 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json']),
        ('necromancy', 'Low-rank Necromancy30',
         'All 30 low-rank Necromancy identities are included in the submitted 137-spell conference. Soul Tap wording and corpse, armor and recovery interfaces still require explicit mechanical decisions, complete candidate authoring and exact review. Preserve incidental cosmology for its post-push review; no new spell approval.',
         'The older unsent label and partial four-cohort count are superseded by the actual v3 dispatch; no mechanical decision is inferred.',
         ['LOW_RANK_SPELLS_V3_SUBMISSION.json', 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json']),
        ('evocation', 'Eight rank-three Evocation',
         'All eight rank-three Evocation identities are included in the submitted 137-spell conference. Range, area, finite meteors, launch/falling and extinguishing questions still require source decisions, complete candidate authoring and exact review. No new spell approval.',
         'The older unsent label is superseded by the actual v3 dispatch; no mechanical decision is inferred.',
         ['LOW_RANK_SPELLS_V3_SUBMISSION.json', 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json']),
        ('spell_queue', 'Twenty-one unsent cohorts',
         'All 572 pending ordinary spell identities have complete source preparations across 44 cohorts and 627 book bindings: 524 mechanical questions and 48 post-push receipts. Six cohorts (137 identities) are submitted; 38 cohorts (435 identities, 388 questions and 47 receipts) remain unsent. Refresh their LAX and intervening interfaces before dispatch. Totals remain 276 operational drafts and 572 pending; preparation and submission grant no approval.',
         'The 279-identity checkpoint predates completion of all 572 source preparations and the first 137-identity dispatch.',
         ['PREPARED_SPELL_SOURCE_INDEX.md', 'HIGHER_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json', 'LOW_RANK_SPELLS_V3_SUBMISSION.json']),
        ('feat_authoring', 'Complete the remaining327 feat source objects;',
         'All 327 pending feat source objects are preserved in full across nine prepared, unsent cohorts; obtain source decisions, author every complete candidate and complete exact review. Only 8 of 335 feats are operationally reviewed. Keep class selections, the ordinary Soul Cage spell and Soulrender whole-soul ritual distinct, retaining deferred cosmology boundaries.',
         'Full source preparation is complete; the remaining work is actual source decisions, candidate authorship and exact review.',
         ['FEAT_COMPLETE_FILE_HANDOFF_PREPARATION.json', 'FEAT_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json']),
        ('feat_queue', 'The complete335-ID feat queue',
         'All 335 feat identities remain distinct: 8 reviewed and 327 pending with complete source preparations. Source category does not define mechanical scope; General, Magic and Skill combat interfaces remain open. Counterpart records are dependency evidence only and do not increase approval counts.',
         'The earlier 256-unprepared subtotal is superseded by the complete nine-cohort source preparation.',
         ['FEAT_COMPLETE_FILE_HANDOFF_PREPARATION.json', 'FEAT_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json']),
        ('feat_queue_followup', 'Current focused source queue supersedes prior256-other count:',
         None,
         'The later 231-unprepared subtotal is superseded by the complete nine-cohort source preparation. Its counterpart/count caveats are retained in the current feat-queue issue.',
         ['FEAT_COMPLETE_FILE_HANDOFF_PREPARATION.json', 'FEAT_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json']),
    ]
    compact = lambda text: re.sub(r'\s+', '', text)
    changes = []
    counts = {m[0]: 0 for m in mappings}
    for area in packet['aspects']:
        active = []
        for index, original in enumerate(area['openIssues']):
            matches = [m for m in mappings if compact(original).startswith(compact(m[1]))]
            assert len(matches) <= 1
            if not matches:
                active.append(original)
                continue
            key, _, replacement, reason, evidence = matches[0]
            entry = {'id': f"{area['id']}-HIST-{index:02}", 'originalIndex': index,
                     'originalText': original, 'reason': reason, 'replacement': replacement,
                     'evidence': [PREFIX + p for p in evidence], 'recordedAtUtc': now}
            assert all((PROJECT / p).is_file() for p in entry['evidence'])
            area.setdefault('historicalIssueNotes', []).append(entry)
            changes.append({'area': area['id'], 'domain': area['domain'], 'kind': key, **entry})
            counts[key] += 1
            if replacement:
                active.append(replacement)
        area['openIssues'] = active
    assert all(counts.values()), counts
    assert counts['tinker'] == 4 and counts['spell_queue'] == 1
    assert all(counts[k] == 1 for k in ('feat_authoring', 'feat_queue', 'feat_queue_followup'))
    assert len(before['aspects']) == len(packet['aspects']) == 75
    for old, new in zip(before['aspects'], packet['aspects']):
        for key in old:
            if key not in ('openIssues', 'historicalIssueNotes'):
                assert old[key] == new[key], (old['id'], key)
        retained = new['openIssues'] + [n['originalText'] for n in new.get('historicalIssueNotes', [])]
        assert all(text in retained for text in old['openIssues'])
    BACKUP.mkdir()
    backups = {}
    for path in changed_paths:
        dest = BACKUP / rel(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(path.read_bytes())
        backups[rel(path)] = {'backup': rel(dest), 'sha256': sha(path)}
        assert sha(dest) == sha(path)
    (BACKUP / 'FILE_MANIFEST.json').write_text(json.dumps(backups, indent=2) + '\n', encoding='utf-8')
    lines = ['# Preserved coverage checkpoint history', '',
             'This is an editorial correction of active queue stages. Every original issue below is retained exactly, together with the evidence and its current replacement. No game rule or acceptance gate changed; no source material was deleted.', '',
             f'{len(changes)} checkpoint occurrences updated across {len({c["area"] for c in changes})} areas. The complete pre-edit ledger, rendered guide, renderer, start page and handoff are preserved in [the backup manifest](coverage-ledger-before-status-consolidation/FILE_MANIFEST.json).', '']
    for item in changes:
        lines += [f"## {item['id']} — {item['domain']}", '', '**Original, retained verbatim:**', '',
                  '> ' + item['originalText'], '', '**Disposition:** ' + item['reason'], '',
                  '**Current active text:** ' + (item['replacement'] or 'Merged into the current complete feat-queue issue; no unresolved mechanical question removed.'), '',
                  '**Evidence:** ' + ', '.join(f'[{Path(p).name}]({Path(p).name})' for p in item['evidence']), '']
    HISTORY.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    packet.setdefault('historyReferences', []).append(rel(HISTORY))
    DATA.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    text = RENDERER.read_text(encoding='utf-8')
    anchor = "    for row in rows:\n        issue=' '.join(row['openIssues']) or 'Acceptance evidence recorded.'"
    addition = "    for path in packet.get('historyReferences', []):\n        assert (PROJECT / path).is_file(), path\n        index = lines.index('## Completion standard')\n        lines[index:index] = [f'[Preserved checkpoint history](../../../../{path}) — earlier queue stages remain available verbatim.', '']\n"
    assert text.count(anchor) == 1
    RENDERER.write_text(text.replace(anchor, addition + anchor), encoding='utf-8')
    result = subprocess.run([sys.executable, '-X', 'utf8', str(RENDERER)], capture_output=True, text=True, check=True)
    start = START.read_text(encoding='utf-8')
    note = '**Coverage ledger updated:** Earlier preparation checkpoints are retained in [the issue history](docs/audit/2026-10-08/full-game/COVERAGE_ISSUE_HISTORY_2026-10-11.md); active entries now distinguish submitted spell sources, prepared feat sources and reviewed crafting interfaces. All game acceptance gates remain unchanged.\n\n'
    assert start.startswith('# Decennium Descent — start here\n\n')
    START.write_text(start.replace('# Decennium Descent — start here\n\n', '# Decennium Descent — start here\n\n' + note, 1), encoding='utf-8')
    with HANDOFF.open('a', encoding='utf-8') as handle:
        handle.write('\n## Coverage issue-stage consolidation\n\n[Preserved issue history](COVERAGE_ISSUE_HISTORY_2026-10-11.md) retains every superseded checkpoint verbatim. Active entries now reflect the submitted 137-spell conference, complete 327-feat source preparations, and completed TD/AEX/LAX recipe-interface decisions. Every status, acceptance gate, closure and human-evidence field is unchanged. This is editorial reconciliation, not new game approval.\n')
    unchanged = all(sha(PROJECT / p) == h for p, h in frozen.items())
    assert unchanged
    receipt = {'status': 'PASS — active queue stages reconciled without losing issue history', 'atUtc': now,
               'changedOccurrences': len(changes), 'changedAreas': len({c['area'] for c in changes}),
               'countsByCheckpoint': counts, 'changes': changes, 'beforeFiles': backups,
               'allOriginalIssuesRetainedExactly': True, 'allOtherExistingAreaFieldsUnchanged': True,
               'all75AcceptanceGatesUnchanged': True, 'all75StatusesUnchanged': True,
               'all75ClosuresUnchanged': True, 'humanEvidenceUnchanged': True,
               'activeSpellPacketInputs': len(frozen), 'activeSpellPacketInputsUnchanged': unchanged,
               'renderCheck': result.stdout.strip(),
               'afterHashes': {rel(p): sha(p) for p in changed_paths + [HISTORY]},
               'sourceInformationDeleted': False, 'newMechanicalApproval': False, 'pushPerformed': False,
               'cosmologyReviewed': False}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in receipt.items() if k not in ('changes', 'beforeFiles', 'afterHashes')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
