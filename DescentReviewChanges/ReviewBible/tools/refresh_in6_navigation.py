"""Preserve EN6 navigation and expose complete, unadopted IN6 proposals."""
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
s = index.read_text('utf-8')
s = once(s, 'higher-spell-index-before-en6/', 'higher-spell-index-before-in6/')
s = once(s, "('enchantment_rank6', 'Rank-six Enchantment')]:", "('enchantment_rank6', 'Rank-six Enchantment'), ('illusion_necromancy_rank6', 'Rank-six Illusion and Necromancy')]:")
for before, after in [('138', '151'), ('250', '237'), ('276', '302'), ('67', '80')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0
s = once(s, 'Sixty-seven new drafts', 'Eighty new drafts')
s = once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The thirteenth adds thirteen rank-six Illusion/Necromancy procedures and twenty-six examples, with fifteen full current counterparts, eight prior proposals and seven class envelopes. Four explicitly new Ghoul/Ghast/Wight/Mummy profiles retain their unrated CR and remain separate from the current bestiary. Seventeen joint issues cover truth and illusion perception, finite detonations, real Prone, programmed triggers, incorporeal movement and lifetap, periodic fog damage, permanent binding/creation and three Eyebite modes. These are new proposals with no catalog or runtime promotion. The earlier71 drafts were shared only as comparisons with the feat conference;')
n = nav.read_text('utf-8')
n = once(n, '    featured = [\n', '    featured = [\n        ("13 new rank-six Illusion/Necromancy drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ILLUSION_NECROMANCY_RANK6.md"),\n')
n = once(n, '    pending = [\n', '    pending = [\n        ("Rank-six Illusion/Necromancy proposals — preservation and source checks", "ILLUSION_NECROMANCY_RANK6_OPERATING_PROPOSAL_CHECK.json"),\n')
n = once(n, 'Higher-spell index has138 unadopted procedures/276 examples,250 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has151 unadopted procedures/302 examples,237 remaining mechanical questions and47 post-push receipts. IN6 adds13 Illusion/Necromancy procedures and26 examples,15 full current counterparts,8 earlier drafts,7 class envelopes and4 explicitly new creature profiles. Its646 preservation/rendering/source checks pass, including29 arithmetic checks;17 explicit issues await joint review. The profiles remain unrated, sources remain intact, and no semantic approval or application runtime tests are claimed.')
preserve('higher-spell-index-before-in6', [index, R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md', A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-in6-proposals', [nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EN6.json'])
index.write_text(s, encoding='utf-8', newline='\n')
nav.write_text(n, encoding='utf-8', newline='\n')
print('Preserved eight index/navigation artifacts and updated IN6 navigation builders.')
