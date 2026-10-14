#!/usr/bin/env python3
"""Read-only source/patch checks and extracted EpochClaims identity trials.

Usage: python check_cadence_addendum.py INPUT.zip [OUTPUT_REPORT.json]
The input archive is never extracted or modified. No full feat procedure,
turn scheduler, BoundAllowance, rest engine or campaign authenticator runs.
"""
import ast
import copy
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import sys
import zipfile

D='docs/audit/2026-10-08/full-game/FEAT335_ALLOWANCE_DESCRIPTORS.json'
S='DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json'
B='DescentReviewChanges/ReviewBible/tools/build_feat335_allowance_descriptors.py'
E='DescentReviewChanges/ReviewBible/tools/feat335_allowance_bindings.py'
EXPECTED='5d67cc24ab7ce5274f6a055a60616143d5d605b3dfdfdb9b1c4f4e7910f1ffe9'
ACTUAL_IDS='bladedancer break_line bull_rush crippling_strike crusher piercer punishing_blow slasher tactical_flanker unstoppable_force precision_strike'.split()
RESULTS=[]
def check(name,actual,expected=True,kind='static'):
 a=copy.deepcopy(actual);e=copy.deepcopy(expected)
 RESULTS.append({'id':name,'kind':kind,'actual':a,'expected':e,'pass':a==e})
def digest(b): return hashlib.sha256(b).hexdigest()
def get(o,p):
 for k in p.strip('/').split('/'): o=o[int(k)] if isinstance(o,list) else o[k]
 return o
def setv(o,p,v):
 ks=p.strip('/').split('/');a=o
 for k in ks[:-1]:a=a[int(k)] if isinstance(a,list) else a[k]
 a[int(ks[-1]) if isinstance(a,list) else ks[-1]]=copy.deepcopy(v)
def cadence_from_builder(text):
 nodes=[]
 for n in ast.parse(text).body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CADENCE' for t in n.targets):nodes.append(n)
  elif isinstance(n,ast.FunctionDef) and n.name=='cadence':nodes.append(n)
  elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='cadence':nodes.append(n)
 ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<source CADENCE declarations>','exec'),ns)
 return ns['CADENCE']

def main():
 if len(sys.argv)<2:raise SystemExit(__doc__)
 archive=Path(sys.argv[1]);raw=archive.read_bytes();here=Path(__file__).resolve().parent
 check('archive.bytes',len(raw),243342,'integrity');check('archive.sha256',digest(raw),EXPECTED,'integrity')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();m=json.loads(z.read('PACKAGE_MANIFEST.json'))
  check('archive.uniqueNames',len(names),len(set(names)),'integrity')
  check('manifest.payloadCount',len(m),12,'integrity');check('archive.members',set(names)==set(m)|{'PACKAGE_MANIFEST.json'},True,'integrity')
  content={n:z.read(n) for n in names}
 for n,rec in m.items():
  check('bytes:'+n,len(content[n]),rec['bytes'],'integrity');check('sha256:'+n,digest(content[n]),rec['sha256'],'integrity')
 ops=json.loads((here/'EXACT_CADENCE_CORRECTIONS.json').read_text(encoding='utf-8'))
 register=json.loads((here/'CADENCE_38_REGISTER.json').read_text(encoding='utf-8'))
 check('bound.manifest',digest(content['PACKAGE_MANIFEST.json']),ops['inputManifestSha256'],'integrity')
 d=json.loads(content[D]);s=json.loads(content[S]);b=content[B].decode('utf-8')
 old_d=copy.deepcopy(d);old_s=copy.deepcopy(s)
 old_map=cadence_from_builder(b)
 selected={e['id']:e['laterEventCadences'] for e in d['entries'] if e['laterEventCadences']}
 check('all.entries',len(d['entries']),177);check('cadence.identities',len(selected),38);check('cadence.records',sum(map(len,selected.values())),40)
 check('original.completeBuilderDescriptorEquality',old_map,selected)
 for op in ops['operations']:check('operation.preflight:'+op['operationId'],digest(content[op['path']]),op['expectedSha256'],'integrity')
 for op in ops['operations']:
  if op['kind']=='append_json_string':
   check('old:'+op['operationId'],get(s,op['pointer']),op['old']);setv(s,op['pointer'],op['old']+op['append'])
  elif op['kind']=='replace_text':
   check('old:'+op['operationId'],b.count(op['old']),op['expectedOccurrences']);b=b.replace(op['old'],op['replacement'],1)
  elif op['kind']=='replace_json_value':
   check('old:'+op['operationId'],get(d,op['pointer']),op['old']);setv(d,op['pointer'],op['replacement'])
  else:raise ValueError('Unknown operation')
 new_map=cadence_from_builder(b);new_selected={e['id']:e['laterEventCadences'] for e in d['entries'] if e['laterEventCadences']}
 check('descendant.completeBuilderDescriptorEquality',new_map,new_selected)
 check('new FS06 exact append',s['rules'][5]['wording'],old_s['rules'][5]['wording']+'\n\n'+ops['newSharedParagraph'])
 reverse_s=copy.deepcopy(s);reverse_s['rules'][5]['wording']=old_s['rules'][5]['wording'];check('other shared values unchanged',reverse_s,old_s,'preservation')
 changed=[]
 for i,(old,new) in enumerate(zip(old_d['entries'],d['entries'])):
  if old['laterEventCadences']!=new['laterEventCadences']:changed.append(old['id'])
  restored=copy.deepcopy(new);restored['laterEventCadences']=old['laterEventCadences']
  check('all unrelated entry fields:'+old['id'],restored,old,'preservation')
 check('exact changed ids',sorted(changed),sorted(ACTUAL_IDS+['overrun']))
 for rec in register['rows']:
  check('register.before:'+rec['id'],rec['before'],selected[rec['id']])
  check('register.after:'+rec['id'],rec['after'],new_selected[rec['id']])
  check('register.boundSource:'+rec['id'],digest(get(old_d,rec['sourceProcedurePointer']).encode()),rec['sourceProcedureSha256'])
 # Compile ONLY the submitted EpochClaims class, without unavailable imports.
 node=next(n for n in ast.parse(content[E].decode('utf-8')).body if isinstance(n,ast.ClassDef) and n.name=='EpochClaims')
 ns={'dataclass':dataclass,'field':field,'__name__':__name__}
 exec(compile(ast.Module(body=[node],type_ignores=[]),'<submitted EpochClaims only>','exec'),ns)
 Claims=ns['EpochClaims']
 for sid in ACTUAL_IDS:
  c=Claims();out=[c.claim(sid,['A'],'enc:R:A:1'),c.claim(sid,['A'],'enc:R:A:1'),c.claim(sid,['A'],'enc:X:A:2'),c.claim(sid,['A'],'enc:R:A:1'),c.claim(sid,['A'],'enc:R:B:3')]
  check('actual-turn identity:'+sid,out,[True,False,True,False,True],'extracted-key-algebra')
 c=Claims();check('overrun owner-recipient-turn',[c.claim('overrun.challenge',['A','T1'],'R1'),c.claim('overrun.challenge',['A','T1'],'R1'),c.claim('overrun.challenge',['A','T2'],'R1'),c.claim('overrun.challenge',['A','T1'],'X1')],[True,False,True,True],'extracted-key-algebra')
 c=Claims();check('Savage linked extra carries existing regular key',[c.claim('savage_attacker',['A'],'reg-interval-1'),c.claim('savage_attacker',['A'],'reg-interval-1'),c.claim('savage_attacker',['A'],'reg-interval-2')],[True,False,True],'extracted-key-algebra')
 c=Claims();check('Eldritch both modes one embedded regular key',[c.claim('eldritch_combat.embeddedCast',['A'],'reg-interval-1'),c.claim('eldritch_combat.embeddedCast',['A'],'reg-interval-1'),c.claim('eldritch_combat.ordinaryAppend',['A'],'A-reg-1'),c.claim('eldritch_combat.ordinaryAppend',['A'],'A-reg-1')],[True,False,True,False],'extracted-key-algebra')
 c=Claims();check('freeStoredRelease shared same-round key',[c.claim('freeStoredRelease',['A'],'round-1'),c.claim('freeStoredRelease',['A'],'round-1'),c.claim('freeStoredRelease',['A'],'round-2')],[True,False,True],'extracted-key-algebra')
 c=Claims();check('Quickened firstInitiative no encounter replay',[c.claim('quickened_thought.firstInitiative',['A'],'enc-1'),c.claim('quickened_thought.firstInitiative',['A'],'enc-1'),c.claim('quickened_thought.firstInitiative',['A'],'enc-2')],[True,False,True],'extracted-key-algebra')
 c=Claims();check('Mana Burn recipient pool shared owners',[c.claim('mana_burn',['T'],'round-1'),c.claim('mana_burn',['T'],'round-1'),c.claim('mana_burn',['U'],'round-1')],[True,False,True],'extracted-key-algebra')
 c=Claims();check('Curse Weaving owner-recipient separation',[c.claim('curse_weaving',['A','T'],'round-1'),c.claim('curse_weaving',['B','T'],'round-1'),c.claim('curse_weaving',['A','T'],'round-1')],[True,True,False],'extracted-key-algebra')
 c=Claims();check('Wilderness Chef eater rest independent of cook',[c.claim('wilderness_chef.recipient',['T'],'T-LR-1'),c.claim('wilderness_chef.recipient',['T'],'T-LR-1'),c.claim('wilderness_chef.recipient',['T'],'T-LR-2')],[True,False,True],'extracted-key-algebra')
 c=Claims();check('cast lifetime does not incorporate new rest epoch',[c.claim('energy_sink.hostileCast',['A','cast-X'],'cast-X-lifetime'),c.claim('energy_sink.hostileCast',['A','cast-X'],'cast-X-lifetime')],[True,False],'extracted-key-algebra')
 c=Claims();check('Lucky original roll identity survives replacement',[c.claim('lucky.intervention',['A','roll-X'],'roll-X-lifetime'),c.claim('lucky.intervention',['A','roll-X'],'roll-X-lifetime')],[True,False],'extracted-key-algebra')
 check('source archive remains byte-identical',digest(archive.read_bytes()),EXPECTED,'preservation')
 from collections import Counter
 report={'reviewId':'FEAT335-CADENCE-CHECK-01','submissionSha256':EXPECTED,'executedChecks':len(RESULTS),'passed':sum(r['pass'] for r in RESULTS),'failed':sum(not r['pass'] for r in RESULTS),'countsByKind':dict(Counter(r['kind'] for r in RESULTS)),'executionScope':'Read-only archive/manifest; exact in-memory patch/preservation; original and amended CADENCE declaration execution; extracted submitted EpochClaims identity algebra under explicitly conditional supplied event/epoch facts. Full assemble(), BoundAllowance/FiniteFeatUse, source turn authentication, actual feat/cast/attack/Ready/rest/temporal procedures and full-candidate suites were NOT executed.','semanticExpectations':'FINITE_CADENCE_EXPECTATIONS.json is authored, not asserted as executed gameplay.','results':RESULTS}
 path=Path(sys.argv[2]) if len(sys.argv)>2 else here/'EXECUTED_CHECKS.json'
 # Equality was evaluated against deep snapshots. Compact only large successful
 # report values into reproducible canonical fingerprints; never hide a failure.
 for row in report['results']:
  if row['pass']:
   for label in ('actual','expected'):
    val=row[label]; encoded=json.dumps(val,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    if len(encoded)>1000:
     row[label]={'reportRepresentation':'canonical-json fingerprint of compared value','canonicalBytes':len(encoded),'sha256':digest(encoded)}
 path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:report[k] for k in ['executedChecks','passed','failed','countsByKind']}))
 if report['failed']:raise SystemExit(1)
if __name__=='__main__':main()
