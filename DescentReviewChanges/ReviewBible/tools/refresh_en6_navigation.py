"""One-use preserved EN6 navigation update; all proposals remain unadopted."""
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
preserve('higher-spell-index-before-en6', [index, R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md', A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-en6-proposals', [nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EV6.json'])
s = index.read_text('utf-8')
s = once(s, 'higher-spell-index-before-ev6/', 'higher-spell-index-before-en6/')
s = once(s, "('evocation_rank6', 'Rank-six Evocation')]:", "('evocation_rank6', 'Rank-six Evocation'), ('enchantment_rank6', 'Rank-six Enchantment')]:")
for before, after in [('131', '138'), ('257', '250'), ('262', '276'), ('60', '67')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0
s = once(s, 'Sixty new drafts', 'Sixty-seven new drafts')
s = once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The twelfth adds seven rank-six Enchantment procedures and fourteen examples while preserving Soul Cage as an untouched post-push receipt. Its fifteen current counterparts, seven prior proposals and seven class envelopes support thirteen explicit issues: independent charm, recent episodic-memory loss and recovery, movement control, spell/item-use restriction, mental prison transitions, twelve-recipient24-hour suggestion and full-Action dance. The Haze/Woven recovery bridge and Mass Suggestion duration harmonization are expressly new proposals. The earlier71 drafts were shared only as comparisons with the feat conference;')
index.write_text(s, encoding='utf-8', newline='\n')
s = nav.read_text('utf-8')
s = once(s, '    featured = [\n', '    featured = [\n        ("7 new rank-six Enchantment drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ENCHANTMENT_RANK6.md"),\n')
s = once(s, '    pending = [\n', '    pending = [\n        ("Rank-six Enchantment proposals — preservation and source checks", "ENCHANTMENT_RANK6_OPERATING_PROPOSAL_CHECK.json"),\n')
s = once(s, 'Higher-spell index has131 unadopted procedures/262 examples,257 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has138 unadopted procedures/276 examples,250 remaining mechanical questions and47 post-push receipts. EN6 adds7 Enchantment procedures and14 examples,15 full current counterparts,7 earlier drafts and7 class envelopes, preserving Soul Cage as a literal post-push receipt. Its581 preservation/rendering/source checks pass, including19 arithmetic checks;13 explicit issues await joint review. These checks are not semantic approval or application runtime tests.')
nav.write_text(s, encoding='utf-8', newline='\n')
print('Preserved eight index/navigation artifacts and updated EN6 navigation builders.')
