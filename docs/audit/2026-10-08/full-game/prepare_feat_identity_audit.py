"""Detect exact source-name/effect collisions without merging any feat identity."""
from pathlib import Path
from collections import defaultdict
import json
import re
import hashlib
AUDIT=Path(__file__).resolve().parent;GAME=AUDIT.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
path=ROOT/'src/data/feats.js'
source=json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
names=defaultdict(list);effects=defaultdict(list)
normal=lambda s:re.sub(r'\s+',' ',s).strip().casefold()
for f in source:
    names[normal(f['name'])].append(f)
    effect=normal(f.get('effect',''))
    if effect:effects[effect].append(f)
groups=lambda groups:[{'normalizedKey':key,'originalObjects':items} for key,items in groups.items() if len(items)>1]
families=[('Acrobat','Acrobatic'),('Alert','Alertness','Improved Alertness'),('Blind Fight','Blind Fighting'),
          ('Athlete','Athletic Prodigy','Improved Athlete'),('Climber','Improved Climber'),
          ('Martial Adept','Martial Adept (Advanced)'),('Weapon Focus','Weapon Master'),
          ('Skilled','Skill Expert','Prodigy','Jack of All Trades'),
          ('Tough','Tough as Nails','Durable','Hardy','Tenacity'),
          ('Inspiring Leader','Inspiring Presence','Natural Leader','Leadership','Commanding Presence')]
semantic=[{'familyNames':list(family),'reason':'Manual name-related candidate only; requires reading every source and a notebook decision before alias/stacking changes',
           'originalObjects':[f for f in source if f['name'] in family]} for family in families]
data={'status':'PREPARED / NOT a merge, deletion or shared-family rule',
      'sourceFileSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceCount':len(source),
      'exactDisplayNameCollisions':groups(names),'exactNormalizedEffectCollisions':groups(effects),
      'nameRelatedCandidates':semantic}
(AUDIT/'FEAT_IDENTITY_CANDIDATES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exactNameGroups':[[f['id'] for f in g['originalObjects']] for g in data['exactDisplayNameCollisions']],
                  'exactEffectGroups':[[f['id'] for f in g['originalObjects']] for g in data['exactNormalizedEffectCollisions']],
                  'manualNameFamilies':len(semantic)},ensure_ascii=False,indent=2))
