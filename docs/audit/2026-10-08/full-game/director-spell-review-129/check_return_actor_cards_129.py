"""Fresh read-only current-native card and selected-level inspector; not a build/play verdict."""
from pathlib import Path
import argparse,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('report');a=p.parse_args()
D=Path(__file__).parent.resolve();E=(D/a.directory).resolve();assert E.parent==D
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
cards={};sources={}
native_files=list((R/'data/public/class_playtests').glob('*.json'))
native_files.append(R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json')
for source in native_files:
 obj=read(source)
 if not isinstance(obj,dict) or not isinstance(obj.get('cards'),list):continue
 for i,c in enumerate(obj['cards']):
  if 'id' not in c:continue
  assert c['id'] not in cards or cards[c['id']]==c
  cards[c['id']]=c;sources[c['id']]={'path':source.relative_to(G).as_posix(),'pointer':'/cards/'+str(i),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
actors=read(E/'ACTOR_TEMPLATES.json');checks=[];errors=[];unknown=[];matches=[]
def check(label,ok):
 checks.append(label)
 if not ok:errors.append(label)
def walk(v,path):
 if isinstance(v,dict):
  if isinstance(v.get('completeCard'),dict):
   c=v['completeCard'];sid=c.get('id')
   if sid in cards:
    check('current-card:'+path,c==cards[sid]);matches.append({'path':path+'/completeCard','id':sid,'nativeSource':sources[sid]})
    if isinstance(v.get('classLevel'),int):check('minimum-acquisition-level:'+path,v['classLevel']>=cards[sid]['minimumClassLevel'])
   else:unknown.append({'path':path+'/completeCard','id':sid,'reason':'Not in current class_playtests and separate Bard card map; independent source resolution required.'})
  for k,x in v.items():walk(x,path+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,path+'/'+str(i))
walk(actors,'')
for aid,t in actors.items():
 if not isinstance(t,dict):continue
 for sel in t.get('selectedAcquisition',[]):
  if isinstance(sel.get('classLevel'),int) and isinstance(t.get('classLevel'),int):check('acquisition-not-future:'+aid+':'+str(sel.get('cardIndex')),sel['classLevel']<=t['classLevel'])
  card=sel.get('completeCard',{})
  if t.get('class') and card.get('className'):check('selected-class:'+aid+':'+str(card.get('id')),t['class']==card['className'])
result={'status':'NATIVE_CARD_DATA_CHECKS_COMPLETE_NOT_FULL_ACTOR_ACCEPTANCE','checks':len(checks),'errors':errors,'matchedCompleteCardOccurrences':len(matches),'uniqueMatchedCardIds':len({v['id'] for v in matches}),'unknownCardsNeedingIndependentSource':unknown,'matches':matches,'scope':'Exact current native copied-card bytes/JSON and recorded minimum/current level gates only. Selection cadence/path/prerequisites/ability scores/HP/RP/book/prepared capacity/equipment/phase and actual event legality still require independent review. No supplied code or gameplay executed.','canonicalChanges':False,'runtimeExecuted':False}
out=(D/a.report).resolve();assert out.parent==D and not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='matches'},indent=2))
if errors:sys.exit(1)
