from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
allrows=json.loads((HERE/'HEALING_SEMANTIC_SUPPLEMENT_CANDIDATES.json').read_text(encoding='utf-8'))['classRecords']
chosen={
 'cleric':{'consecrated-ground','radiance','renewal','echoes','aura-of-faith','sanctified-reprisal','aura-of-grace','cosmic-equilibrium','sanguine-rite','zealot-s-fervor','words-of-equilibrium'},
 'crimson-agent':{'blood-tithe','hemostasis','transfusion','veinweave-vitality-link'},
 'monk':{'stance-shift','meditative-healing','tranquil-lotus-step','balance-beyond-flesh','transcendent-meditation'},
 'oracle':{'spiral-touched-boon-iii','spiral-touched-boon-v','wound-eater-boon-iii','wound-eater-boon-iv','wound-eater-boon-v','burning-blood','false-life','false-life-boon-v','fate-bound-boon-iv','unfinished-chorus','ember-mantle','life-prophecy-trigger','life-linked','garden-of-restoration','life-prophecy','rewind-wound','the-spiral-opens'},
 'paladin':{'lay-on-hands','desecrated-ground','merciful-smite','channel-life','verdict-absolute','last-rites','throne-s-grace','crown-undying'},
 'ranger':{'living-pulse','healing-touch'},
 'shaman':{'benevolent-spirits','blood-feast','blood-curse','talon-strike'},
 'warrior':{'bloodthick-node','rapid-coagulation','bio-stabilizer','adrenal-floodgate','flesh-warden','cellular-reconstruction'},
 'tinker':{'snap-rebuild'},
 'thief':{'exsanguinate'},
 'mirrorsage':{'echo-leech'},
 'wizard':{'infernal-pact-quest-based-unlock'},
}
engines={('paladin',0),('paladin',11),('warrior',24),('shaman',1),('mirrorsage',2),('mirrorsage',5)}
rows=[r for r in allrows if (r['kind']=='class-card' and r['card']['id'].split('.')[-1] in chosen.get(r['owner'],set())) or (r['kind']=='class-engine' and (r['owner'],r['engineIndex']) in engines)]
out={'status':'UNREVIEWED_EXACT_SUPPLEMENT','scope':'Selected omitted death replacements, recovery gates, healing arithmetic/trigger/reserve examples. Not all199 additional lexical matches.',
 'counts':{'classCards':sum(r['kind']=='class-card' for r in rows),'classEngines':sum(r['kind']=='class-engine' for r in rows)},'classRecords':rows}
(HERE/'HEALING_INTERFACE_SUPPLEMENT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out['counts'])
