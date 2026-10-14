"""Prepare exact temporal source evidence; no new temporal rule or promotion."""
from pathlib import Path
import hashlib
import json
import re

AUDIT=Path(__file__).resolve().parent;GAME=AUDIT.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
id='oracle.supplement.spiral-touched.spiral-touched-boon-v'
def walk(value):
    if isinstance(value,dict):
        yield value
        for v in value.values():yield from walk(v)
    elif isinstance(value,list):
        for v in value:yield from walk(v)

cards=json.loads((ROOT/'data/public/class_playtests/oracle.json').read_text(encoding='utf-8'))
matches=[v for v in walk(cards) if v.get('id')==id]
assert len(matches)==1
source=json.loads((ROOT/'data/playtest/class_sources/oracle.json').read_text(encoding='utf-8'))
booklines=source['bookLines']
line_matches=[]
for i,line in enumerate(booklines):
    if re.search(r'time loop',line['text'],re.I):
        line_matches.append(booklines[max(0,i-5):i+4])
supplement=json.loads((ROOT/'data/playtest/class_sources/supplements.json').read_text(encoding='utf-8'))
supplement_matches=[v for v in walk(supplement) if isinstance(v.get('description'),str)
                    and re.search(r'time loop',v['description'],re.I)]
sourcefile=ROOT/'src/data/oracle-curses.js'
lines=sourcefile.read_text(encoding='utf-8').splitlines()
source_lines=[{'line':i+1,'text':line} for i,line in enumerate(lines) if re.search(r'time loop',line,re.I)]
packet={'status':'PREPARED / UNDISCUSSED temporal world transaction',
 'scope':'Exact Time Loop source/card and previously reviewed bounded interfaces; not new copy/steal catalog authorization',
 'card':matches[0], 'cardSha256':hashlib.sha256(json.dumps(matches[0],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
 'sourceFile':str(sourcefile.relative_to(GAME)).replace('\\','/'),
 'sourceFileSha256':hashlib.sha256(sourcefile.read_bytes()).hexdigest(),
 'exactSourceLines':source_lines,'bookSourcePath':source['sourcePath'],
 'bookExtractSha256':source['sourceSha256'],'bookContext':line_matches,'supplementObjects':supplement_matches}
(AUDIT/'TEMPORAL_WORLD_EXACT_SOURCES.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
parts=['# Time Loop: full world transaction source conference — PREPARED, not yet sent\n\n'
       'The eight feats are in a separate implementation review. Do not infer their approval here. '
       'Time Loop is the remaining original form/buffer deferred class interface. '
       'Its existing selected participant contract is already reviewed, but not a runnable world transaction. '
       'Please preserve the exact original source and current reviewed participant/resource distinctions, '
       'label necessary NEW bridges, and resolve the ten questions below. '
       'No map-wide rollback, invented resource refund, created soul or duplicated equipment may be inferred silently. '
       'If a proposed rule conflicts with the original reset-entire-combat promise, identify the conflict explicitly.\n',
       (AUDIT/'TEMPORAL_WORLD_REVIEW_PREPARATION.md').read_text(encoding='utf-8'),
       '\n## Exact original/current source evidence\n```json\n'+json.dumps(packet,ensure_ascii=False,indent=2)+'\n```\n']
for filename,patterns,context in [
 ('docs/mechanics/HEALING_DEATH_PLAYTEST.md',[r'Time Loop',r'temporal',r'does not restore RP'],2),
 ('docs/mechanics/FORM_TEMP_HP_PLAYTEST.md',[r'Time Loop',r'grant identit',r'original regular'],2),
 ('docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md',[r'sponsor',r'suppress',r'meld',r'original',r'concentration',r'placement'],1),
 ('docs/mechanics/CLASS_PLAYTEST_RULES.md',[r'snapshot',r'long rest',r'per.encounter',r'turn'],0),
 ('tools/healing_playtest_rules.py',[r'TEMPORAL_PARTICIPANT_FIELDS'],20),
]:
    path=ROOT/filename;lines=path.read_text(encoding='utf-8').splitlines();indices=set()
    for i,line in enumerate(lines):
        if any(re.search(p,line,re.I) for p in patterns):
            indices.update(range(max(0,i-context),min(len(lines),i+context+1)))
    parts.append('\n## Exact interface excerpts: '+filename+'\n\n'+
                 '\n'.join(str(i+1)+': '+lines[i] for i in sorted(indices))+'\n')
parts.append('''
## Concrete acceptance scenarios for your proposed transaction

- Two eligible Oracles each use Time Loop at different iterations; every LR use stays spent and there is no automatic free Reaction refresh through a conserved spent-use reset.
- A snapshot creature later dies; its remains were used by an undead-raising source or its body became an object. Restore one actual identity without cloning consumed corpse material or leaving a second raised body.
- A nonparticipant enters a participant's old square; terrain is destroyed or a wall appears. Define atomic placement/terrain treatment or a concrete legal preflight failure, not an unexplained teleport or automatic damage.
- A snapshot form/True Polymorph record ends after the snapshot, original gear unmolds, and an item is consumed/transferred/lost. Reconstitute the allowed anatomy/buffer state without restoring forbidden inventory or sponsor slots for free.
- An originally active spell would now be past its absolute deadline. State whether deadline time rewinds, persists, or rebases, including suppressed True Polymorph stabilization and next-regular-turn shields.
- A later summon spends its shared command offense; a device is destroyed; kits and RP are spent. Explain each entity/slot/stock/resource separately, preserving the source's explicit reset RC/per-encounter categories.
- Soul Charge death rewards, Necrotic Affinity seals, Lifeleech reserve and Agony reducers cross the rewind. These eight-feat candidate interactions must eventually match the actual final review; no review status is assumed. Prevent death farming or replayed heal/excess/kill rewards.
- A target was already Dead at the snapshot; a living participant retained a source-bound Soul Bind. Preserve the reviewed participant state distinction without treating Time Loop as ordinary resurrection.
- Knowledge belongs to real allies and players; control/allegiance changes cannot force a player's later choice or erase agency.

Please provide a complete finite snapshot schema, explicit participant/world boundary, restoration versus conservation table, preflight/commit/cleanup ordering, exact timing and failure behavior. State any content-specific operation still needing an exact source rather than declaring the whole world solved by a generic boolean. This is a source conference, not a request to approve unseen code.
''')
(AUDIT/'CODEX_TEMPORAL_WORLD_CONFERENCE_PREPARED.md').write_text('\n'.join(parts),encoding='utf-8')
print(json.dumps({'card':matches[0],'bookMatches':len(line_matches),'sourceLines':len(source_lines),
                  'packetBytes':(AUDIT/'CODEX_TEMPORAL_WORLD_CONFERENCE_PREPARED.md').stat().st_size},ensure_ascii=False,indent=2))
