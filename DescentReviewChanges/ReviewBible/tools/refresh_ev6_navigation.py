"""One-use preserved EV6 navigation update, without rule promotion."""
from pathlib import Path
from hashlib import sha256
import json
import re
import shutil

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'

def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}

def preserve(folder, paths):
    dest = A / folder
    assert not dest.exists(), 'One-use update: preserve prior backup'
    manifest = {}
    for p in paths:
        rel = p.relative_to(G).as_posix(); target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        assert info(target) == info(p)
        manifest[rel] = {**info(p), 'preservedCopy': target.relative_to(G).as_posix()}
    (dest / 'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

def once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after)

index = R / 'tools/build_higher_spell_operating_proposal_index.py'
nav = R / 'tools/build_review_map.py'
preserve('higher-spell-index-before-ev6', [index, R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md', A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-ev6-proposals', [nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DU5.json'])
s = index.read_text('utf-8')
s = once(s, 'higher-spell-index-before-du5/', 'higher-spell-index-before-ev6/')
s = once(s, "('divination_universal_rank5', 'Rank-five Divination and Universal')]:",
    "('divination_universal_rank5', 'Rank-five Divination and Universal'), ('evocation_rank6', 'Rank-six Evocation')]:")
for before, after in [('123', '131'), ('265', '257'), ('246', '262'), ('52', '60')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0
s = once(s, 'Fifty-two new drafts', 'Sixty new drafts')
s = once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The eleventh adds eight rank-six Evocation procedures and sixteen examples, with fifteen complete current counterparts, six earlier proposals and seven class envelopes. Its twelve joint issues cover visual blindness, actual time suspension, three-shot cannon operation, structural collapse, lightning arcs, disintegration and real ice. These remain proposed rules, with no temporal/device runtime integration approval. The earlier71 drafts were shared only as comparisons with the feat conference;')
index.write_text(s, encoding='utf-8', newline='\n')
s = nav.read_text('utf-8')
s = once(s, '    featured = [\n', '    featured = [\n        ("8 new rank-six Evocation drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/EVOCATION_RANK6.md"),\n')
s = once(s, '    pending = [\n', '    pending = [\n        ("Rank-six Evocation proposals — preservation and source checks", "EVOCATION_RANK6_OPERATING_PROPOSAL_CHECK.json"),\n        ("Feat review access-limitation report — no verdict", "GPT_FEAT_V3_TERMINAL_ACCESS_LIMITATION.md"),\n        ("Requested continuation of the existing full feat review", "CODEX_FEAT_V3_RECOVERY_CONTINUATION_REQUEST.txt"),\n')
s = once(s, 'Higher-spell index has123 unadopted procedures/246 examples,265 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has131 unadopted procedures/262 examples,257 remaining mechanical questions and47 post-push receipts. EV6 adds8 Evocation procedures and16 examples,15 full current counterparts,6 earlier drafts and7 class envelopes. Its587 preservation/rendering/source checks pass, including23 arithmetic checks;12 explicit issues await joint review. No independent semantic approval or application runtime testing is claimed.')
s = once(s, 'Verdict pending; no feat promotion.',
    'The original feat request ended in access-limitation reply6cea42e9-4628-41a0-8619-6257ec16f577, not a final verdict. GPT reported its earlier707-payload verification but unavailable readable file-tool results. The exact report is preserved and continuation of the same packet/retained findings has been requested; no feat promotion.')
nav.write_text(s, encoding='utf-8', newline='\n')
print('Preserved eight index/navigation artifacts and updated EV6 navigation builders.')
