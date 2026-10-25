"""Read-only compact projection of complete conference native rules/questions."""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path(r'C:\Github\DecenniumDescent\DescentReviewChanges\ReviewBible\data\director\spell_review')/sys.argv[1]
d=json.loads(p.read_text(encoding='utf-8-sig'))
out={'source':str(p),'native':[],'questions':d['questions'],'futureCaseRequirements':d['futureCaseRequirements']}
for r in d['records']:
 c=r['completeCurrentCatalogSourceAndAccess'];s=c['source']
 out['native'].append({'id':r['spellId'],'classAccess':c['classAccess'],'additionalRpCost':c['additionalRpCost'],'placements':s['original']['placements'],'coreEntries':s['coreEntries']})
if len(sys.argv)>2:
 section=sys.argv[2]
 out=out[section]
 if len(sys.argv)>3:
  start,end=map(int,sys.argv[3].split(':'));out=out[start:end]
print(json.dumps(out,ensure_ascii=False,indent=2))
