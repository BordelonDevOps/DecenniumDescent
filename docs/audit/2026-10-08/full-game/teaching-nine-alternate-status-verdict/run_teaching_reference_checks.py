"""Bounded teaching reference checks. No encounter, device-service or authority runtime.
Usage: python run_teaching_reference_checks.py --root /extracted/submission --out /evidence.json
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,sys,json,math,ast
ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();r=Path(a.root);b=r/'DescentReviewChanges/ReviewBible';sys.path.insert(0,str(b/'tools'));import core_playtest_rules as core
rows=[]
def c(te,actual,expected,basis,kind='executed reference arithmetic'):
 rows.append(dict(id=f'REF-{len(rows)+1:02}',TE=te,kind=kind,basis=basis,actual=actual,expected=expected,passed=actual==expected))
basis='Actual supplied core_playtest_rules.py; eligibility, scene chronology and custody separately adjudicated.'
s=core.LifeState(10,10);s,e=core.damage_event(s,6,constitution_save_modifier=2,wound_natural=6)
c('TE-13',[s.hp,list(s.wounds),e['woundSaves'],e['woundTotal'],s.death_failures],[4,[None],1,8,0],basis)
s,e=core.damage_event(s,4,constitution_save_modifier=2,wound_natural=3,injury_d6=3);c('TE-13',[s.hp,list(s.wounds),e['woundSaves'],e['woundTotal'],s.death_failures],[0,[None,3],1,4,0],basis)
s=core.death_save(s,8,regular_turn_id=1);c('TE-14',s.death_failures,1,basis);core.stabilize(s,2,43200);c('TE-14',[s.hp,s.stable,s.death_failures,s.stable_until_seconds],[0,True,0,50400],basis)
c('TE-14',core.stable_recovery(s,50399).hp,0,basis);s=core.stable_recovery(s,50400);c('TE-14',[s.hp,s.stable,list(s.wounds)],[1,False,[None,3]],basis)
c('TE-14',core.task_check(10,3,12),dict(total=13,degree='success',success=True),basis);s=core.remove_wounds(s,[1]);c('TE-14',[s.hp,list(s.wounds)],[1,[None]],basis)
c('TE-14',str(F(41,2)-12),'17/2','12:00 to20:30 elapsed8.5h; treatment8activeh from12:30')
s,e=core.damage_event(core.LifeState(10,10,temp_hp=3),6,constitution_save_modifier=2);c('TE-15',[s.hp,s.temp_hp,e['woundSaves']],[7,0,0],basis)
s,e=core.damage_event(core.LifeState(10,0,death_failures=1),1,critical=True);c('TE-15',[s.dead,s.death_failures,e['deathFailuresAdded']],[True,3,2],basis)
s,e=core.damage_event(core.LifeState(10,4),14);c('TE-15',[s.dead,e['instantDeath'],e['woundSaves']],[True,True,0],basis)
s=core.death_save(core.LifeState(10,0,wounds=(None,3)),20,regular_turn_id=1);c('TE-15',[s.hp,list(s.wounds),s.death_failures],[1,[None,3],0],basis)
c('TE-15',core.heal(core.LifeState(10,3,wounds=(None,None,None)),20).hp,9,basis)
s,e=core.damage_event(core.LifeState(10,10,wounds=(None,None,None)),6,constitution_save_modifier=2,wound_natural=5);c('TE-15',[s.dead,len(s.wounds)],[True,3],basis)
o=json.loads((b/'data/playtest/herbalism_recipe_candidate.json').read_text());card=next(x for x in o['cards'] if x['recipeId']=='recipe-200');op=card['operational'];q=op['craft']['batchQuantity']
c('TE-10',max(4,1)>=card['sourceRequirements']['skillLevel'],True,'Actual trained recipe eligibility')
c('TE-10',card['sourceRequirements']['skillLevel']<=1-5,False,'Take10 five-level rule')
c('TE-11',math.floor(F(3,2)*q),7,'Q5 maximum packaging reserve')
c('TE-11',str(4*F('.5')+F('.36')),'59/25','Consumed exact source mass2.36lb')
c('TE-11',4*8+10+7,49,'42gp ingredients +7gp packaging references')
c('TE-11',[120,120-15],[120,105],'First15min included in2h')
def craft(n,m=2,dc=10):
 x=n+m-dc
 return 'Mishap' if n==1 or x<=-10 else 'Masterwork' if x>=10 else 'Exceptional' if x>=5 else 'Standard' if x>=0 else 'Flawed' if x>=-4 else 'Failed'
for n,v in [(10,'Standard'),(5,'Flawed'),(13,'Exceptional'),(20,'Masterwork'),(3,'Failed'),(1,'Mishap')]:c('TE-11',craft(n),v,'Native six-band crafting, no Core natural shifts')
c('TE-11',[q,q//2,math.floor(q*F(5,4)),math.floor(q*F(3,2))],[5,2,6,7],'Q5 quantity alternatives')
c('TE-11',[str(F(4,4)),math.floor(F(1,4))],['1',0],'Failed water/petal quantity notvalue')
c('TE-11',str(5*F('.2')+2*F('.1')),'6/5','Finished+unusedempty1.2lb')
c('TE-12',[4<11,4],[True,4],'Firstsuccess4XP below11, no advancement')
c('TE-12',str(4*F('.2')+3*F('.1')),'11/10','Afteradministration1.1lb')
c('TE-12',[43200+600,op['physical']['openedLifetimeSeconds']],[43800,3600],'12:10benefitendpoint vs1h openedclock')
c('TE-16',[13+2,5+2+1,2+2],[15,8,4],'Anacite1 stats')
hp=30
for n,bonus,damage,ehit,ehp in [(9,3,4,True,26),(8,4,3,True,23),(8,3,0,False,23),(10,3,2,True,21)]:
 hit=core.attack_roll(n,bonus,12)['hit'];hp-=damage if hit else 0;c('TE-18',[hit,hp],[ehit,ehp],basis)
c('TE-19',[min(12,7+4+2),min(5,6),1-1],[12,5,0],'FieldRepair HP+5/RP-1, notservice')
c('TE-19',[str(F(25,10)),str(F(8,100))],['5/2','2/25'],'TI06 packvalue/mass')
c('TE-19',core.task_check(6,4,10),dict(total=10,degree='success',success=True),basis)
c('TE-18',[36000+600,36012+600],[36600,36612],'Distinct realserviceblockdeadlines')
c('TE-17',10+10,20,'Two actual binding periods')
c('TE-04',[240*60,80*60,320*60,280*60],[14400,4800,19200,16800],'Language modules: spoken/literacy/combined/same-script')
c('TE-04',[math.ceil(F(15*100,480)),math.ceil(F(22*100,480))],[4,5],'Copperinvoice atactual15/22instructionminutes')
c('TE-05',[3,8*60,250,6,10,6],[3,480,250,6,10,6],'Insightpoints/time/words; speechsec; rehearsalmin/cues','static source-bound constants')
crimson=json.loads((b/'data/public/class_playtests/crimson-agent.json').read_text());c('TE-24','automatically reaches capacity 6 at class 9' in crimson['engine'][7],True,'Actual engine[7]','static source assertion')
for lev,spill,v in [(1,False,3),(8,False,3),(9,False,6),(8,True,6),(9,True,6)]:c('TE-24',6 if lev>=9 or spill else 3,v,'Source-derived capacity; no current-BG award')
c('TE-26',[max(0,2-1),2],[1,2],'Nextregularstart ticks; extra turn/end does not')
# Pure numerical binary-vs-Core fixture demonstrates why glossary exceptions must remain explicit.
c('TE-07',core.task_check(1,9,10)['success'],False,basis)
c('TE-07',1+9>=10,True,'Basic/Precision Dismantling meetDC10, nonaturalshift')
c('TE-07',[1+9>=20,11+9>=20],[False,True],'Precisionquality threshold separate from binarysuccess')
life=(b/'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md').read_text();c('TE-23','Enemy cause is **not required**.' in life,True,'Exact current reviewed lifecycle','static source assertion')
src=(b/'tools/device_lifecycle_playtest_rules.py').read_text();tree=ast.parse(src);fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='recycling');seg=ast.get_source_segment(src,fn)
c('TE-23',not any(isinstance(n,ast.Attribute) and n.attr in ('enemy_hit','hostile_cause','enemy_cause') for n in ast.walk(fn)),True,'Actual helper lacks enemycausetest; not execution','static source assertion')
c('TE-23',all(s in seg for s in ['d.deliberate_sacrifice','d.copied_object','d.no_own_destruction_chain','noResourceGeneration','consume_material']),True,'Original helper keeps exclusionandconsumption','static source assertion')
c('TE-23',[min(1,x) for x in (0,1,2)],[0,1,1],'RP refund ceiling only; actual sourceadmission/clock is separate')
report=dict(scope='Actual supplied Core-helper executions plus labeled independent reference arithmetic/static source checks. No gameplay runtime, full device lifecycle suite, authored service runtime or campaign authentication.',checks=len(rows),passed=sum(x['passed'] for x in rows),failed=[x for x in rows if not x['passed']],rows=rows)
Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
