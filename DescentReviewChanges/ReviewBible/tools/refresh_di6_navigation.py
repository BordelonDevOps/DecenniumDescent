"""Preserve AC6 navigation and add the five unadopted DI6 proposals."""
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
s = once(s, 'higher-spell-index-before-ac6/', 'higher-spell-index-before-di6/')
s = once(s, "('abjuration_conjuration_rank6', 'Rank-six Abjuration and Conjuration')]:", "('abjuration_conjuration_rank6', 'Rank-six Abjuration and Conjuration'), ('divination_rank6', 'Rank-six Divination')]:")
for before, after in [('162','167'), ('226','221'), ('324','334'), ('91','96')]:
    s, count = re.subn(r'(?<!\d)' + before + r'(?!\d)', after, s)
    assert count > 0
s = once(s, 'Ninety-one new drafts', 'Ninety-six new drafts')
s = once(s, 'The earlier71 drafts were shared only as comparisons with the feat conference;',
    'The fifteenth adds five rank-six Divination procedures and ten examples, thirteen current counterparts, six prior proposals and complete envelopes for all seventeen classes. Thirteen joint issues cover school-specific stasis, class-feature suppression and resource conservation, shortest physical routes, thirty-day institutional scenarios and complete eligible committed-spell warnings. The prediction interface and its Instantaneous source conflict remain explicit proposals. Planar Binding Minor remains a literal CR8 receipt. The earlier71 drafts were shared only as comparisons with the feat conference;')
n = nav.read_text('utf-8')
n = once(n, '    featured = [\n', '    featured = [\n        ("5 new rank-six Divination drafts", "DescentReviewChanges/ReviewBible/docs/spells/proposals/DIVINATION_RANK6.md"),\n')
n = once(n, '    pending = [\n', '    pending = [\n        ("Rank-six Divination proposals — preservation and source checks", "DIVINATION_RANK6_OPERATING_PROPOSAL_CHECK.json"),\n')
n = once(n, 'Higher-spell index has162 unadopted procedures/324 examples,226 remaining mechanical questions and47 post-push receipts.',
    'Higher-spell index has167 unadopted procedures/334 examples,221 remaining mechanical questions and47 post-push receipts. DI6 adds5 Divination procedures and10 examples,13 current counterparts,6 prior drafts and all17 class envelopes while preserving1 literal post-push receipt. Its577 source-preservation/rendering checks pass, including22 plain arithmetic checks;13 explicit issues await joint review. Class suppression and prediction require actual GPT agreement; no semantic approval or application runtime testing is claimed.')
compile(s, str(index), 'exec'); compile(n, str(nav), 'exec')
preserve('higher-spell-index-before-di6', [index, R / 'data/director/higher_spell_operating_proposal_index.json',
    R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md', A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'])
preserve('navigation-before-di6-proposals', [nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json', A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6.json'])
index.write_text(s, encoding='utf-8', newline='\n'); nav.write_text(n, encoding='utf-8', newline='\n')
print('Preserved eight navigation artifacts and updated DI6 builders.')
