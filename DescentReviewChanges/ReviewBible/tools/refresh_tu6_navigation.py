"""Preserve DI6 navigation and add thirteen unadopted TU6 proposals."""
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
    assert not dest.exists(), 'One-use update; preserve existing backup.'
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
s = once(s, 'higher-spell-index-before-di6/', 'higher-spell-index-before-tu6/')
s = once(s, "('divination_rank6', 'Rank-six Divination')]:", "('divination_rank6', 'Rank-six Divination'), ('transmutation_universal_rank6', 'Rank-six Transmutation and Universal')]:")
for before, after in [('167','180'), ('221','208'), ('334','360'), ('96','109')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0
s = once(s, 'Ninety-six new drafts', 'One hundred nine new drafts')
s = once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The sixteenth adds thirteen rank-six Transmutation/Universal procedures and twenty-six examples, twenty-one current counterparts, ten earlier proposals and all seventeen class envelopes. Its seventeen joint issues cover elemental defense suppression, actual matter and body movement, ability-score capacity, permanent Petrified, mist travel, decoys, allied area exclusions, paid contingent casting, physical servants and remote object recall. Gaseous Form and Glyph of Warding already have reviewed descendants; their old catalog/preparation snapshots remain preserved without being mistaken for current status. Wind Walk adds no physical resistance. The earlier71 drafts were shared only as comparisons with the feat conference;')
n = nav.read_text('utf-8')
n = once(n, '    featured = [\n', '    featured = [\n        ("13 new rank-six Transmutation and Universal drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/TRANSMUTATION_UNIVERSAL_RANK6.md"),\n')
n = once(n, '    pending = [\n', '    pending = [\n        ("Rank-six Transmutation and Universal proposals — preservation and source checks", "TRANSMUTATION_UNIVERSAL_RANK6_OPERATING_PROPOSAL_CHECK.json"),\n')
n = once(n, 'Higher-spell index has167 unadopted procedures/334 examples,221 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has180 unadopted procedures/360 examples,208 remaining mechanical questions and47 post-push receipts. TU6 adds13 Transmutation/Universal procedures and26 examples,21 current counterparts (11 reviewed/10 pending),10 earlier drafts and all17 class envelopes. Its675 source-preservation/rendering checks pass, including39 plain arithmetic checks;17 explicit issues await joint review. Reviewed Gaseous Form/Glyph descendants are correctly distinguished from stale catalog snapshots. Local checks do not establish runtime correctness, balance or joint approval.')
compile(s, str(index), 'exec'); compile(n, str(nav), 'exec')
preserve('higher-spell-index-before-tu6', [index, R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md', A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-tu6-proposals', [nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI6.json'])
index.write_text(s, encoding='utf-8', newline='\n'); nav.write_text(n, encoding='utf-8', newline='\n')
print('Preserved eight navigation artifacts and updated TU6 builders.')
