"""Preserve current navigation before a one-use DU5 draft-index update."""
from pathlib import Path
from hashlib import sha256
import json
import re
import shutil

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'

def info(p):
    data = p.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}

def preserve(folder, paths):
    dest = A / folder
    assert not dest.exists(), 'One-use update: preserve existing backup'
    manifest = {}
    for p in paths:
        rel = p.relative_to(G).as_posix()
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        assert info(p) == info(target)
        manifest[rel] = {**info(p), 'preservedCopy': target.relative_to(G).as_posix()}
    (dest / 'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

def replace_once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after)

index = R / 'tools/build_higher_spell_operating_proposal_index.py'
nav = R / 'tools/build_review_map.py'
preserve('higher-spell-index-before-du5', [index,
    R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md',
    A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-du5-proposals', [nav, G / 'REVIEW_MAP.html',
    A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5.json'])

s = index.read_text('utf-8')
s = replace_once(s, 'higher-spell-index-before-ac5/', 'higher-spell-index-before-du5/')
s = replace_once(s, "('abjuration_conjuration_rank5', 'Rank-five Abjuration and Conjuration')]:",
    "('abjuration_conjuration_rank5', 'Rank-five Abjuration and Conjuration'), ('divination_universal_rank5', 'Rank-five Divination and Universal')]:")
for before, after in [('112', '123'), ('276', '265'), ('224', '246'), ('41', '52')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0, before
s = replace_once(s, 'Forty-one new drafts', 'Fifty-two new drafts')
s = replace_once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The tenth adds eleven rank-five Divination/Universal procedures and twenty-two examples, preserving four post-push receipts. Its twenty-four whole current counterparts, seven earlier proposals and nine class envelopes support thirteen explicit review issues: premonition outcomes, source-range conflicts, memory and agency, institutional forecasts, temporary spell access, separate cast costs, dispel protection, atomic swaps, permanent circle operation, voluntary communication and established lore. The earlier71 drafts were shared only as comparisons with the feat conference;')
index.write_text(s, encoding='utf-8', newline='\n')

s = nav.read_text('utf-8')
s = replace_once(s, '    featured = [\n',
    '    featured = [\n        ("11 new rank-five Divination and Universal drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/DIVINATION_UNIVERSAL_RANK5.md"),\n')
s = replace_once(s, '    pending = [\n',
    '    pending = [\n        ("Rank-five Divination and Universal proposals — preservation and source checks", "DIVINATION_UNIVERSAL_RANK5_OPERATING_PROPOSAL_CHECK.json"),\n')
s = replace_once(s, 'Higher-spell index has112 unadopted procedures/224 examples,276 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has123 unadopted procedures/246 examples,265 remaining mechanical questions and47 post-push receipts. DU5 adds11 Divination/Universal procedures and22 examples,24 full current counterparts,7 earlier drafts and9 class envelopes, while preserving4 literal post-push receipts. Its634 preservation/rendering/source checks pass, including18 arithmetic checks;13 explicit issues await joint review. These are authored checks, with no independent semantic approval or application runtime testing.')
nav.write_text(s, encoding='utf-8', newline='\n')
print('Preserved eight index/navigation artifacts and updated two builders for DU5.')
