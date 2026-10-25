"""Fresh data-only Wizard book/access inspector for the observed return schema.
This is not actor acceptance. Extra acquisition/preparation routes are flagged for source review.
"""
from pathlib import Path
import argparse, collections, json, sys
sys.stdout.reconfigure(encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('report');a=p.parse_args()
D=Path(__file__).parent.resolve();E=(D/a.directory).resolve();assert E.parent==D
R=Path(r'C:\Github\DecenniumDescent\DescentReviewChanges\ReviewBible')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
native={s['id']:s for s in read(R/'data/public/spell_playtests/catalog.json')['spells']}
templates=read(E/'ACTOR_TEMPLATES.json');checks=[];errors=[];manual=[];actors=[]
def check(label,ok):
 checks.append(label)
 if not ok:errors.append(label)
for aid,t in templates.items():
 if not isinstance(t,dict) or t.get('class')!='Wizard':continue
 actors.append(aid);level=t['classLevel'];book=t['spellbook'];prepared=t['prepared']
 assert isinstance(level,int) and 1<=level<=20 and isinstance(book,list) and isinstance(prepared,list)
 ids=[x['spellId'] for x in book]
 check(aid+':unique-book-identities',len(ids)==len(set(ids)))
 check(aid+':unique-prepared-identities',len(prepared)==len(set(prepared)))
 for row in book:
  sid=row['spellId'];acq=row['classLevel'];assert isinstance(acq,int)
  check(aid+':acquisition-not-future:'+sid,1<=acq<=level)
  access=native.get(sid,{}).get('classAccess',{}).get('Wizard')
  if access is None:
   manual.append({'actor':aid,'spell':sid,'issue':'No normal Wizard access; an actual independently sourced exception is required.'});continue
  check(aid+':exact-native-access:'+sid,row['completeAccess']==access)
  check(aid+':rank-legal-at-acquisition:'+sid,acq>=access['minimumClassLevel'])
 counts=collections.Counter(row['classLevel'] for row in book)
 limits={n:7 if n==1 else 2 if n<=4 else 3 if n<=8 else 4 if n<=12 else 5 if n<=16 else 6 for n in range(1,level+1)}
 for n,total in sorted(counts.items()):
  if n in limits and total>limits[n]:manual.append({'actor':aid,'level':n,'recordedAdditions':total,'normalFreeAdditions':limits[n],'issue':'Requires actual extra scribing/acquisition source and its cost/time; not automatic rejection.'})
 if counts[1]==7:
  school=t.get('school')
  if not any(row['classLevel']==1 and row['completeAccess'].get('rank')==1 and row['completeAccess'].get('school')==school for row in book):
   manual.append({'actor':aid,'issue':'Seven level1 additions contain no identified rank1 chosen-school bonus; establish an actual bonus/extra acquisition source.'})
 for sid in prepared:
  if sid not in ids:manual.append({'actor':aid,'spell':sid,'issue':'Prepared outside the ordinary recorded book; requires exact separate preparation source.'})
 intelligence=t['abilities']['INT'];base=max(1,level+(intelligence-10)//2)
 if len(prepared)>base or t.get('preparedCapacity',base)!=base:
  manual.append({'actor':aid,'preparedCount':len(prepared),'ordinaryCapacity':base,'declaredCapacity':t.get('preparedCapacity'),'issue':'Check the actual selected preparation exception, school restrictions and each extra matrix.'})
result={'status':'DATA_CHECKS_COMPLETE_PENDING_SOURCE_SEMANTICS','wizardActors':actors,'checks':len(checks),'errors':errors,'exceptionCandidates':manual,'scope':'Current ordinary Wizard access, acquisition timing, unique identities and normal free-book/preparation boundaries. Source exceptions, actual selection cadence, prerequisites, preparation history and event casts still need independent review.','canonicalChanges':False,'runtimeExecuted':False,'suppliedCodeExecuted':False}
out=(D/a.report).resolve();assert out.parent==D and not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if errors:sys.exit(1)
