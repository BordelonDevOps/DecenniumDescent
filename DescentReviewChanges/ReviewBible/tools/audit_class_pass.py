"""Verify source-book preservation, navigation backups and delivered class links."""
from pathlib import Path
import json,hashlib,re
REVIEW=Path(__file__).resolve().parents[1];ROOT=REVIEW.parents[1]
AUDIT=ROOT/'docs/audit/2026-10-08';OUT=AUDIT/'classes';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=read(AUDIT/'project_inventory.json');issues=[];books=[]
for p in (ROOT/'books').rglob('*.docx'):
 rel=p.relative_to(ROOT).as_posix();expected=next(x for x in inv if x['path'].replace('\\','/')=='Descent assets/DecenniumDescent-main/'+rel)
 ok=sha(p)==expected['sha256'];books.append({'path':rel,'unchanged':ok,'sha256':sha(p)})
 if not ok:issues.append('Changed main book: '+rel)
nav=read(AUDIT/'all_class_navigation_changes.json')
for x in nav:
 if sha(ROOT/x['originalBackup'])!=x['originalSha256']:issues.append('Backup changed: '+x['path'])
 if sha(ROOT/x['path'])!=x['newSha256']:issues.append('Navigation changed since ledger: '+x['path'])
manifest=read(REVIEW/'data/public/class_playtests/manifest.json')
validation=read(REVIEW/'docs/mechanics/CLASS_PLAYTEST_VALIDATION.json')
bard=read(REVIEW/'docs/mechanics/BARD_PLAYTEST_VALIDATION.json')
if validation['status']!='PASS':issues.append('Class validator not passing')
if bard['status']!='PASS':issues.append('Bard validator not passing')
docs=list((REVIEW/'docs/mechanics/classes').glob('*.md'))+[REVIEW/'docs/mechanics'/n for n in ['CLASS_PLAYTEST_INDEX.md','BASE_CLASSES_START_HERE.md','CLASS_PLAYTEST_BUILD_EXAMPLES.md','CLASS_PLAYTEST_RULES.md','CLASS_PLAYTEST_SESSION_LOG.md','PALADIN_OATHS_AND_OATHBREAKERS.md']]+[ROOT/x['path'] for x in nav]
linkcount=0
for p in docs:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  target=target.split('#')[0];linkcount+=1
  if not (p.parent/target).resolve().exists():issues.append('Broken link '+str(p.relative_to(ROOT))+':'+target)
artifacts=[]
for folder in [REVIEW/'data/public/class_playtests',REVIEW/'data/playtest/class_drafts',REVIEW/'data/playtest/class_sources',REVIEW/'docs/mechanics/classes']:
 artifacts.extend(p for p in folder.iterdir() if p.is_file())
artifacts.extend(p for p in docs if p not in artifacts)
hashes=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(artifacts))]
(OUT/'class_artifact_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
result={'status':'PASS' if not issues else 'FAILED','classes':len(manifest['classes']),'cards':manifest['totalCards'],
 'classChecks':len(validation['checks']),'ordinaryBuildSamples':sum(v['sampleCount'] for v in validation['buildExamples'].values()),'bardBuildSamples':bard['randomLegalProgressions'],
 'oracleCombinations':1800,'druidCombinations':70,'paladinCombinations':120,'mainWordBooks':books,'navigationBackups':len(nav),'markdownLinksChecked':linkcount,
 'scope':'Class draft source/structure/acquisition and selected reference invariants. No full effect simulator, human balance result, live companion integration or approved-book promotion.', 'errors':issues}
(OUT/'CLASS_PASS_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(result['status'],result['classes'],'classes;',result['cards'],'cards;',len(books),'unchanged books;',linkcount,'links;',len(issues),'issues')
for s in issues:print(s)
