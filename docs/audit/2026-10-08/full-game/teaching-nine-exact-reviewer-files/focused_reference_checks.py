"""Finite reference checks, NOT a game/encounter implementation.
The full original device validator needs absent combat_playtest_rules.py.
This explicitly isolated harness executes unchanged AST-selected Wallet,
CommandLedger, Destruction, profile_stats and material/Recycling methods
against declared fixtures; it does not authenticate their campaign premises.
"""
from pathlib import Path
from dataclasses import dataclass,field,asdict
from types import SimpleNamespace,ModuleType
from fractions import Fraction
from copy import deepcopy
import argparse,ast,hashlib,json,sys

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();r=a.root/'DescentReviewChanges/ReviewBible';tools=r/'tools';sys.path.insert(0,str(tools))
 import core_playtest_rules as c
 from spell_playtest_rules import integer,SpellRuleError
 rows=[]
 def ck(name,x,y):rows.append({'id':'TF-'+str(len(rows)+1).zfill(2),'name':name,'passed':x==y,'actual':x,'expected':y})
 def reject(name,fn):
  try:fn()
  except SpellRuleError as e:ck(name,'rejected','rejected')
  else:ck(name,'accepted','rejected')
 q=c.LifeState(10,10);q,e=c.damage_event(q,6,constitution_save_modifier=2,wound_natural=6);ck('First hit HP/Wounds/Injury/save',(q.hp,len(q.wounds),list(c.active_injuries(q)),e['woundTotal']),(4,1,[],8))
 q,e=c.damage_event(q,4,constitution_save_modifier=2,wound_natural=3,injury_d6=3);ck('Second hit preexisting-Wound penalty and no dying-hit double charge',(q.hp,q.wounds,q.death_failures,e['woundTotal']),(0,(None,3),0,4))
 q=c.death_save(q,8,regular_turn_id=1);ck('Death save8 unmodified',q.death_failures,1);c.stabilize(q,2,12*3600);ck('Stable clears counters, stays0 and has14:00 deadline',(q.hp,q.stable,q.death_failures,q.stable_until_seconds),(0,True,0,14*3600))
 q=c.stable_recovery(q,14*3600-1);ck('Before stable deadline remains0',q.hp,0);q=c.stable_recovery(q,14*3600);ck('At stable deadline1HP/Wounds unchanged',(q.hp,q.wounds),(1,(None,3)))
 rr=c.task_check(10,3,12);ck('Treatment tierI successful',rr['degree'],'success');q=c.remove_wounds(q,[1]);ck('Remove W2 removes its linked Injury only',(q.hp,q.wounds,list(c.active_injuries(q))),(1,(None,),[]));ck('Treatment elapsed overlap',(20*60+30-12*60),510)
 q,e=c.damage_event(c.LifeState(10,10,temp_hp=3),6);ck('Temporary HP prevents large-normal-HP Wound trigger',(q.hp,e['woundSaves']),(7,0))
 q,e=c.damage_event(c.LifeState(10,0,death_failures=1),1,critical=True);ck('Already-dying critical adds2 reachingDead',(q.dead,q.death_failures),(True,3))
 q,e=c.damage_event(c.LifeState(10,4),14);ck('Instant death before Wounds',(q.dead,e['instantDeath'],e['woundSaves']),(True,True,0))
 q=c.death_save(c.LifeState(10,0,wounds=(None,3)),20,regular_turn_id=1);ck('Natural20 death save does not remove Wounds',(q.hp,q.wounds),(1,(None,3)))
 q=c.heal(c.LifeState(10,3,wounds=(None,None,None)),20);ck('Critical Wound healing ceiling',q.hp,9)
 q,e=c.damage_event(c.LifeState(10,10,wounds=(None,None,None)),5,constitution_save_modifier=2,wound_natural=1);ck('Fourth failed Wound save fatal rather than fourth Wound',(q.dead,len(q.wounds)),(True,3))
 ck('Core task natural1 shift differs from basic dismantling',(c.task_check(1,9,10)['success'],1+9>=10),(False,True))
 ck('Natural20 attack critical not task margin',c.attack_roll(20,0,30)['critical'],True);ck('Ordinary save natural1 can meetDC',c.saving_throw(1,9,10)['success'],True)
 def band(n,mod=2,dc=10):
  d=n+mod-dc
  return 'Mishap' if n==1 or d<=-10 else 'Masterwork' if d>=10 else 'Exceptional' if d>=5 else 'Standard' if d>=0 else 'Flawed' if d>=-4 else 'Failed'
 for n,b in [(10,'Standard'),(5,'Flawed'),(13,'Exceptional'),(20,'Masterwork'),(3,'Failed'),(1,'Mishap')]:ck('Recipe200 six-band natural '+str(n),band(n),b)
 ck('Recipe200 maximum ordered vials',5*3//2,7);ck('Recipe200 actual consumed mass',str(4*Fraction('0.5')+Fraction('0.36')),'59/25');ck('Recipe200 consumed reference GP',4*8+10,42);ck('Vials7 plus42source GP reference',42+7,49)
 ck('Standard mass includes5filled +2empty',str(5*(Fraction('.1')+Fraction('.1'))+2*Fraction('.1')),'6/5');ck('After use dose inventory and retained vial',str(4*(Fraction('.1')+Fraction('.1'))+3*Fraction('.1')),'11/10');ck('Failed recovery divisible water, indivisiblepetal',(4//4,1//4),(1,0));ck('Included first phase minutes',120-15,105)
 def bg(level,spill):return 6 if level>=9 or spill else 3
 for level,spill,maximum in [(8,False,3),(8,True,6),(9,False,6),(9,True,6),(20,True,6)]:ck('BG cap '+str((level,spill)),bg(level,spill),maximum)
 ck('Capacity change alone retains currentBG',min(2,bg(9,False)),2);ck('Shaman1/12/13cap',[1 if n<13 else 2 for n in [1,12,13]],[1,1,2])
 # Load genuine selected source nodes without pretending missing full imports exist.
 src=tools/'device_lifecycle_playtest_rules.py';dt=ast.parse(src.read_text());rt=ast.parse((tools/'redirection_playtest_rules.py').read_text());nodes=[n for n in dt.body if getattr(n,'name',None) in {'Wallet','CommandLedger','Destruction','profile_stats'}];nodes+=[n for n in rt.body if getattr(n,'name',None)=='identity'];m=ModuleType('tex_isolated_device_reference');sys.modules[m.__name__]=m;m.__dict__.update(dataclass=dataclass,field=field,integer=integer,SpellRuleError=SpellRuleError)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src)+'[isolated nodes]','exec'),m.__dict__)
 lifecycle=next(n for n in dt.body if isinstance(n,ast.ClassDef) and n.name=='Lifecycle');methods=[n for n in lifecycle.body if getattr(n,'name',None) in {'material','consume_material','recycling'}]
 def entity(self,ident):return self.entities[ident]
 cls=ast.ClassDef(name='MaterialHarness',bases=[],keywords=[],body=methods,decorator_list=[]);exec(compile(ast.fix_missing_locations(ast.Module(body=[cls],type_ignores=[])),'unchanged-material-methods','exec'),m.__dict__);m.MaterialHarness.entity=entity
 def fixture(**kw):
  d=m.Destruction('d','x',False,False,False,False,True,False,frozenset(),None,True,True)
  for k,v in kw.items():setattr(d,k,v)
  e=SimpleNamespace(state='destroyed',material_event='d',paid_deployment_rp=2);b=m.MaterialHarness();b.entities={'x':e};b.destructions={'d':d};return b,e,d
 b,e,d=fixture();w=m.Wallet(0);ck('TC friendly accidental source can refund1',b.recycling('x',w,use_key='recycle/sr1'),1);ck('TC consumes usable debris once',(w.rp,d.material_available,d.material_consumer),(1,False,'recycling'));reject('TC second material claim',lambda:b.material('x'))
 for key,val in [('deliberate_sacrifice',True),('copied_object',True),('no_own_destruction_chain',True),('flags',frozenset({'noResourceGeneration'}))]:
  b,e,d=fixture(**{key:val});w=m.Wallet(0);reject('TC excludes '+key,lambda:b.recycling('x',w,use_key='recycle/sr1'));ck('TC rejection preserves debris '+key,d.material_available,True)
 b,e,d=fixture(deliberate_sacrifice=True,enemy_caused=True);reject('TC enemy involvement does not waive sacrifice',lambda:b.recycling('x',m.Wallet(0),use_key='recycle/sr1'))
 b,e,d=fixture();e.paid_deployment_rp=0;w=m.Wallet(0);ck('TC actual0RP deployment produces0 refund',b.recycling('x',w,use_key='recycle/sr1'),0);ck('TC no mintedRP from GP',w.rp,0)
 b,e,d=fixture(incoming_damage_was_copy=True);ck('TC copied incoming damage is not copied device',b.recycling('x',m.Wallet(0),use_key='recycle/sr1'),1)
 b,e,d=fixture();w=m.Wallet(0,used={'recycle/sr1'});reject('TC same real rest-use key alreadyspent',lambda:b.recycling('x',w,use_key='recycle/sr1'));ck('TC spent-use rejection preserves debris',d.material_available,True)
 b,e,d=fixture();ck('Nonenemy does not qualify hostile-only consumers',d.hostile_qualifies(),False)
 b,e,d=fixture(enemy_caused=True,friendly_damage=False);ck('Enemy cause without hit remains distinct',(d.hostile_qualifies(),d.enemy_hit),(True,False))
 led=m.CommandLedger('Ilan');w=m.Wallet(1);res=led.activate(1,'attack',w,tinker=True);ck('Attack command spends sharedcommand andoffense',(res['commandSpent'],res['damagingActivationSpent']),(True,True));reject('Another subject sameowner round cannotcommand',lambda:led.activate(1,'attack',m.Wallet(1),tinker=True));reject('Extra turn cannot refresh Tinkercommand',lambda:led.activate(2,'attack',m.Wallet(1),tinker=True,regular=False))
 led=m.CommandLedger('Ilan');res=led.activate(1,'support',m.Wallet(1),tinker=True);ck('Support spendscommand notoffense',(res['commandSpent'],res['damagingActivationSpent']),(True,False));ck('Tinker1 actual Anacite stats',m.profile_stats('drone',1,2,intelligence=2),{'hp':8,'ac':15,'attack':4})
 hp=30
 for n,mod,damage in [(9,3,4),(8,4,3),(8,3,0),(10,3,2)]:
  if c.attack_roll(n,mod,12)['hit']:hp-=damage
 ck('Companion four-round attack numeric trace enemyHP',hp,21);ck('Field Repair6offer5missing',min(12,7+4+2),12);ck('Tinymaintenancepack GP/lb',(str(Fraction(25,10)),str(Fraction(8,100))),('5/2','2/25'));ck('Service INTtool check succeeds',c.task_check(6,4,10)['success'],True)
 out={'scope':'Core helper execution, simple source-bound arithmetic and isolated unchanged device source nodes. Not whole validator, scheduler, acquisition/authentication, range/channels, feature ownership, real rest calendars or deployed runtime.','checks':len(rows),'failed':[x for x in rows if not x['passed']],'sourceHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,tools/'core_playtest_rules.py',tools/'redirection_playtest_rules.py']},'isolatedNodes':['Wallet','CommandLedger','Destruction','profile_stats','identity','Lifecycle.material','Lifecycle.consume_material','Lifecycle.recycling'],'results':rows}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(rows),'failed':out['failed']}))
 if out['failed']: raise SystemExit(1)
if __name__=='__main__':main()
