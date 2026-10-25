"""Fresh read-only checks of every complete committed-cast event against current sources."""
from pathlib import Path
import json,re,sys,math
D=Path(__file__).parent;E=Path(sys.argv[1]) if len(sys.argv)>1 else D/'lifematter5_return01_received'
out=Path(sys.argv[2]) if len(sys.argv)>2 else D/'LIFEMATTER5_RETURN01_CAST_SOURCE_AUDIT_129.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
templates=read(E/'ACTOR_TEMPLATES.json');native={s['id']:s for s in read(E/'evidence/NATIVE_CATALOG.json')['spells']}
cache={};checks=[];errors=[];casts=[];attacks=[]
def check(k,ok):
 checks.append(k)
 if not ok:errors.append(k)
def ptr(file,pointer):
 if file not in cache:cache[file]=read(E/file)
 v=cache[file]
 for k in pointer.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
def walk(c):
 yield c
 for b in c['branches']:yield from walk(b)
for main in read(E/'CASEBOOK.json')['mainCases']:
 for c in walk(main):
  for e in c['timeline']:
   for ref in e['sourceReferences']:
    if ref.get('pointer') and ref['file'].endswith('.json'):
     try:ptr(ref['file'],ref['pointer']);check(e['id']+':source-pointer',True)
     except Exception as x:check(e['id']+':source-pointer:'+repr(x),False)
   o=e['observations']
   if o.get('status')!='committed':continue
   k=e['id'];casts.append(k);a=e['before']['actors'][o['caster']];b=e['after']['actors'][o['caster']];t=templates[a['template']];sid=o['spellId'];n=o['nativeAccess'];rank=n['rank']
   check(k+':actual-RP-payment',a['rp']-b['rp']==o['finalRpPaid'] and o['finalRpPaid']==o['baseRp']+o['surcharge']-o['discount'])
   check(k+':actual-Action',a['wallet']['action'] is True and b['wallet']['action'] is False)
   p=a['phase'];check(k+':own-regular-turn',p['active'] and p['lastStart']<=e['time']<=p['lastStart']+p['turnSeconds'] and (p['lastEnd'] is None or p['lastEnd']<p['lastStart']))
   check(k+':conscious-living-caster',a['life']=='living' and not any(x in a['conditions'] for x in ['Petrified','Incapacitated','Unconscious','Stunned']))
   ref=o['sourceBinding'];source=ptr(ref['file'],ref['pointer']);check(k+':actual-source-identity',source.get('id',source.get('spellId'))==sid)
   check(k+':actual-level',a['classLevel']>=n['minimumClassLevel'])
   if a['class']=='Wizard':
    mod=(a['abilities']['INT']-10)//2;limit=max(4,2+a['PB']+max(0,mod));check(k+':actual-Limit',a['limit']==limit)
    surcharge=(0 if rank==0 or a['dissonance']<limit else 1 if a['dissonance']<limit+3 else 2 if a['dissonance']<limit+6 else 3)
    check(k+':strain-block-and-price',rank==0 or a['dissonance']<limit+6);check(k+':actual-surcharge',o['surcharge']==surcharge)
    base=0 if sid not in a['familiesUsed'] or rank==0 else 1 if rank<=5 else 2
    refrain=min(3,a['refrain']+1) if a['lastSpell']==sid else 0
    check(k+':protected-base',o['baseDissonance']==base);check(k+':chronological-Refrain',o['refrainAdded']==refrain and b['refrain']==refrain and b['lastSpell']==sid)
    check(k+':exact-Dissonance',b['dissonance']==a['dissonance']+base+refrain)
    check(k+':family-history',b['familiesUsed']==a['familiesUsed']+([] if sid in a['familiesUsed'] else [sid]))
    if o['route']=='ordinary Wizard':
     check(k+':repertoire',sid in (a['knownCantrips'] if rank==0 else a['prepared']) and (rank==0 or sid in a['book']))
     access=[native[sid]['classAccess']['Wizard']]
     check(k+':actual-native-placement',any(r['rank']==rank and r['minimumClassLevel']==n['minimumClassLevel'] and r['school']==n['school'] for r in access))
    else:
     cards=[x['completeCard'] for x in t['selectedAcquisition']]+t['automaticCards']
     check(k+':actual-class-acquisition',source in cards)
     match=re.search(r'(\d+) RP',source['cost']);check(k+':printed-RP-cost',match is not None and int(match[1])==o['baseRp'])
     check(k+':class-matrix-rank',rank==source['spellRank'])
    plan=o.get('plan',{})
    if 'attackBonus' in plan:
     expected=mod+a['PB']+(t['schoolBonus'] if n['school']==t['school'] else 0)
     check(k+':source-attack-bonus',plan['attackBonus']==expected)
     for target in o['targets']:
      if target in e['before']['actors']:
       targetActor=e['before']['actors'][target]
       if 'Prone' in targetActor['conditions'] and 'Unconscious' in targetActor['conditions']:
        attacks.append({'event':k,'target':target,'source':sid,'plan':plan,'expected':'straight roll; ranged Prone disadvantage cancels Unconscious advantage'})
        check(k+':Prone-Unconscious-cancellation','advantageFaces' not in plan)
result={'id':'LIFEMATTER5-COMMITTED-CAST-SOURCE-AUDIT-129','directory':str(E),'checks':len(checks),'casts':len(casts),'errors':errors,'proneUnconsciousAttackChecks':attacks,'canonicalChanges':False,'runtimeExecuted':False,'suppliedCodeExecuted':False}
assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
sys.exit(bool(errors))
