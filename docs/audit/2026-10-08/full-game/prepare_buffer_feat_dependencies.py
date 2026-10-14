"""Capture exact existing Soul Bind identity interface for the next feat review."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/public/spell_playtests/catalog.json'
catalog=json.loads(path.read_text(encoding='utf-8'))
spell=next(s for s in catalog['spells'] if s['id']=='soul-bind')
assert spell['status']=='operational-playtest-draft'
result={'status':'PREPARED supporting evidence; not a new rule or source merge',
        'sourcePath':str(path.relative_to(ROOT)).replace('\\','/'),
        'spellId':'soul-bind','wholeOverlay':spell,
        'wholeOverlaySha256':hashlib.sha256(json.dumps(spell,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
        'relationship':'Soul Cage/Lifeleech charge design must explicitly state how it interacts with this already-reviewed per-identity resurrection blocker. Similar names alone confer no compatibility.',
        'nonAliases':['Paladin Lifeleech Bloom Aura','Paladin Lifeleech Bloom'],
        'nonAliasReason':'Distinct preserved class-source IDs; not the Lifeleech feat and not evidence of an identical soul-charge feature.'}
(HERE/'BUFFER_FEAT_SOUL_DEPENDENCY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Captured exact reviewed Soul Bind overlay and excluded similar-name Paladin false aliases.')
