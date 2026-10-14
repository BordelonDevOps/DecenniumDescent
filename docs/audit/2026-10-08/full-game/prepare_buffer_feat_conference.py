"""Enrich the preserved eight-feat packet with exact already-reviewed interfaces."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
prepared=(HERE/'CODEX_BUFFER_FEAT_COMPLETION_PREPARED.md').read_text(encoding='utf-8')
text=prepared.replace('# Eight named feats — completion preparation','# Eight named feats — full-clause source conference',1)
text=text.replace('**Prepared, not submitted or adopted.**','**Prepared conference packet; submission is recorded only after visible browser confirmation. No feat is promoted by this packet.**',1)
text+='\n## Existing reviewed interfaces — preserve these while completing missing clauses\n\n'
refs=[('docs/mechanics/FORM_TEMP_HP_PLAYTEST.md',[91,93]),
      ('docs/mechanics/HEALING_DEATH_PLAYTEST.md',[28,29,31,33,74,78,80,86,96,100,102,104])]
for name,numbers in refs:
    path=ROOT/name;lines=path.read_text(encoding='utf-8').splitlines()
    text+='\n### '+name+'\n\nFile SHA256: '+hashlib.sha256(path.read_bytes()).hexdigest()+'\n\n'
    for n in numbers:text+=f'Line{n}: '+lines[n-1]+'\n\n'
text+='''
## Dependency and preservation check

All8 original feat objects and all335 registry entries remain preserved and byte-identical in the main project and review copy. Feat file SHA256842d14e868aa93d51fc6f21e39bc9dd3a1b872cdffcf467ffaa99a4cc3f779b6. Soul Cage explicitly names Lifeleech in prerequisites; Lifeleech explicitly says its charges power Soul Cage. Treat them together; do not create a second charge resource merely because they are two feats.

The new transformation conference also established immutable earliest physical origin: an object-origin creature cannot produce a soul, ordinary healing or corpse entitlement through anatomy changes. Creature-origin identity persists through object anatomy and back. No transformed object is an eligible manufactured soul farm. These remain constraints, not permission to invent a new generic soul economy.

Please answer the ten source questions with complete operational candidate objects for every clause of all eight feats, using exact source IDs, prerequisites and provenance. Identify any truly new numbers, durations, costs and anti-farm restrictions. Preserve distinctions between temporary HP, ordinary healing, stabilization, resurrection prohibition and actual soul custody. Point out new dependent sources that must be read rather than silently copying their effects. The complete objects, code and tests will return for independent implementation review before promotion.
'''
(HERE/'CODEX_BUFFER_FEAT_CONFERENCE_READY.md').write_text(text,encoding='utf-8')
print('Prepared full8-feat conference plus exact reviewed interface passages:',len(text.encode('utf-8')),'bytes; NOT submitted.')
