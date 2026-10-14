from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'data/playtest/class_drafts/warrior.json'
d=json.loads(p.read_text(encoding='utf-8'))
for c in d['cards']:
 if c[0]==4875 and len(c)==9:c[6:8]=['Once at the start of each regular turn']
 if c[0] in [4847,4851]:c[7]=c[7].replace('Your own resistance and DR may mitigate it once after transfer.','Transferred damage cannot be reduced again, redirected again or generate BT.').replace('may be mitigated once by your own resistance/DR,','cannot be reduced again or generate BT,')
 if c[0]==4829:c[7]=c[7].replace('generates no BT from its own damage until after it finishes resolving','cannot generate BT or Brutality Progress from its own damage')
 if c[0] in[4811,4831,4901,4912,4917]:c[4]=c[4].replace('Enemies of your choice','Up to3 enemies of your choice').replace('Enemies within','Up to3 enemies within')
 if c[0] in[4875]:c[3]='Spend healing amount from Mutation Recovery Reserve';c[7]+=' Each HP actually restored spends1 Mutation Recovery Reserve; heal only up to remaining reserve.' if 'Mutation Recovery Reserve' not in c[7] else ''
rejected=[e for e in d['extraCards'] if e.get('sourceLine')==0]
if rejected:d['excludedRegistryAlternatives']=rejected
d['extraCards']=[e for e in d['extraCards'] if e.get('sourceLine')!=0]
for e in d['extraCards']:
 if e['name'] in ['Bloodthick Node','Rapid Coagulation','Hemophage Core']:
  if 'Mutation Recovery Reserve' not in e['effect']:e['effect']+=' Each HP actually restored spends1 Mutation Recovery Reserve; heal no more than remaining reserve.'
 if e['name']=='Flesh Warden':e['effect']='Increase maximum HP by2 per Warrior level while equipped. Equipping raises maximum only, never current HP. Unequipping clamps current HP to the reduced maximum if necessary; it does not subtract another amount from current HP. Repeated swaps cannot heal.'
 if e['name']=='Transcendent':
  e['duration']='Until start of your next regular turn'
  e['frequency']='1/encounter total, regardless of trigger'
  e['effect']='At Warrior12+, the first time this encounter you cross100% Brutality Progress or reach stored BT4, activate all equipped mutations until start of your next regular turn. No serum profile or immediate healing trigger is granted. This is one total pulse, never a permanent BT4 concurrency increase. At end choose active mutations up to normal limit, with their original remaining durations; others become dormant.'
  e['prerequisite']='Warrior12;100% Brutality Progress or BT4 with raised cap; new explicit level gate'
 if e.get('kind')=='progression':e['acquisition']='automatic'
for s in d['engine']:
 pass
d['engine']=[s.replace('Source basis: \nPasted text\n','Source basis: approved Player Rulebook extract and preserved class registry.').replace('At BT 4, if you can hold it, you are also Transcendent. Crossing 100% Brutality Progress triggers one Transcendent pulse even if your stored cap remains 3.','At Warrior12+, reaching BT4 or crossing100% Brutality Progress may trigger the same once-per-encounter Transcendent pulse, even if your stored cap remains3; it is never an indefinitely active state.').replace('Registry-only Fighting Style, Second Wind, Action Surge, Extra Attack and draft level features are preserved as separately labelled extraCards rather than silently substituted for the book progression.','Registry-only Fighting Style, Second Wind, Action Surge, Extra Attack and draft level features are preserved in excludedRegistryAlternatives and original source evidence. They are not acquired or stacked onto this playtest schedule.') for s in d['engine']]
extra='Finite recovery completion: Mutation Recovery Reserve=3L+M HP after a long rest. Bloodthick Node, Rapid Coagulation, Regenerative Mutation, Hemophage Core and their healing enhancements draw from this shared reserve,1point per actual HP healed. No short-rest refill; no gauge, critical hit, free activation or form change replenishes it. Other explicitly limited-use/dose healing retains its own printed limit. This new test reserve prevents indefinite regenerative healing from free mutation activations.'
if extra not in d['engine']:d['engine'].append(extra)
d['reviewStatus']='Source completeness and editorial loop review applied; table balance unverified'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(d['cards']),'skill cards;',len(d['extraCards']),'operational supplements;',len(d.get('excludedRegistryAlternatives',[])),'preserved excluded alternatives')
