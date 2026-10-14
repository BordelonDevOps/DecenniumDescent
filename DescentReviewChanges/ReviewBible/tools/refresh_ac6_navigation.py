"""Preserve IN6 navigation and expose the unadopted AC6 proposals."""
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
s = once(s, 'higher-spell-index-before-in6/', 'higher-spell-index-before-ac6/')
s = once(s, "('illusion_necromancy_rank6', 'Rank-six Illusion and Necromancy')]:", "('illusion_necromancy_rank6', 'Rank-six Illusion and Necromancy'), ('abjuration_conjuration_rank6', 'Rank-six Abjuration and Conjuration')]:")
for before, after in [('151', '162'), ('237', '226'), ('302', '324'), ('80', '91')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0
s = once(s, 'Eighty new drafts', 'Ninety-one new drafts')
s = once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The fourteenth adds eleven rank-six Abjuration/Conjuration procedures and twenty-two examples, sixteen current counterparts, eight earlier proposals and eight full class envelopes. Sixteen joint issues cover the incoming rank barrier, three constituent wards, alignment predicates, seven-day anchoring, stronger cleansing, projectile defense, elemental resistance, randomized arcs, two-attack commands, accelerated forge work and many-body army limits. The Forge conversion and cross-family Seal restriction are explicitly new decisions. Three cosmology-related identities remain literal receipts. The earlier71 drafts were shared only as comparisons with the feat conference;')
n = nav.read_text('utf-8')
n = once(n, '    featured = [\n', '    featured = [\n        ("11 new rank-six Abjuration/Conjuration drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/ABJURATION_CONJURATION_RANK6.md"),\n')
n = once(n, '    pending = [\n', '    pending = [\n        ("Rank-six Abjuration/Conjuration proposals — preservation and source checks", "ABJURATION_CONJURATION_RANK6_OPERATING_PROPOSAL_CHECK.json"),\n')
n = once(n, 'Higher-spell index has151 unadopted procedures/302 examples,237 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has162 unadopted procedures/324 examples,226 remaining mechanical questions and47 post-push receipts. AC6 adds11 Abjuration/Conjuration procedures and22 examples,16 whole current counterparts,8 prior drafts and8 class envelopes while preserving3 literal post-push receipts. Its636 source-preservation/rendering checks pass, including31 plain arithmetic checks;16 explicit issues await joint review. These are authored proposals, with no semantic approval or application runtime testing claimed.')
compile(s, str(index), 'exec'); compile(n, str(nav), 'exec')
preserve('higher-spell-index-before-ac6', [index, R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md', A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-ac6-proposals', [nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_IN6.json'])
index.write_text(s, encoding='utf-8', newline='\n')
nav.write_text(n, encoding='utf-8', newline='\n')
print('Preserved eight index/navigation artifacts and updated AC6 navigation builders.')
