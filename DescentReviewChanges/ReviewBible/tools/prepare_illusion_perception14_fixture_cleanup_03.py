"""Make actual class stages and the new mount lifecycle vectors explicit, preserving v2."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def main():
 oldp=R/'data/director/spell_proposals/illusion_perception_14_current_02.json';out=oldp.with_name('illusion_perception_14_current_03.json');checkp=A/'ILLUSION_PERCEPTION_14_FIXTURE_CHECK_03.json';assert not out.exists() and not checkp.exists();old=json.loads(oldp.read_bytes());d=deepcopy(old)
 d['previousChangedCaseRecords03']=deepcopy(d['currentExamples'])
 for c in d['currentExamples']:
  actor=c['sourceActor'];level=actor['classLevel'];actor['stage']='Hero' if level>=10 else 'Arch Arcanist' if level>=3 else 'Base Wizard';actor['HeroPath']='Spellbinder' if level>=10 else None
  for ref in c['sourceRefs']:
   if ref['path']==oldp.relative_to(G).as_posix():ref['path']=out.relative_to(G).as_posix()
 c=next(x for x in d['currentExamples'] if x['id']=='IN4-05-B')
 c['actionsAndResolution']=[
  'Under the separately pending end-on-suppression choice, actual creating-source suppression ends the mount at t=20 without damage or salvage. The real rider, tack and cargo remain at their actual positions.',
  'The rider enters Falling immediately but does not immediately descend. The accepted Fall Marker is the end of slot K in the following regular round. Every participant retains its normal opportunity before that marker; the fixture assumes no successful intervention.',
  'At t=26 descend 40 feet, within the ordinary 300-foot step limit, and land. Impact is min(10, floor(40/20)) = 2d6. Faces [3,4] give 7 bludgeoning damage: HP 100 to 93. Positive falling damage leaves the rider Prone. No Wound threshold or zero-HP state is reached.',
  'Independent grounded replacement branch: before any suppression, the owner on its own regular turn first spends its Bonus Action to command the old steed, then uses its available Action to cast the replacement Greater Phantom Steed. The repeated matrix costs 7 RP, leaving 10 from 17. Base Dissonance 1 plus Refrain 1 yields Dissonance 2 after commitment. Concentration displaces the old source before the counter window. The new body has HP 20 and its own deadline, but the already spent command allowance stays spent. The old pending command does not transfer, and no new Bonus Action is granted.'
 ]
 d.update(id='ILLUSION-PERCEPTION-14-CURRENT-03',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCompleteDraft=info(oldp));d['fixtureClarifications03']={'actualClassStages':'Wizard7 fixtures are Arch Arcanists with no Hero path. Wizard11 fixtures specify the actually available Spellbinder Hero path. No optional feature is invoked.','mountLifecycleText':'Spacing and explicit event descriptions only; all numeric values, pending choices and conditional branches retained.'};d['sourceBindings'].append(info(oldp))
 checks=[{'check':'All original texts and current procedures preserved','passed':d['originalExamplesUnchanged']==old['originalExamplesUnchanged'] and d['spells']==old['spells']},{'check':'Actual gated Hero paths','passed':all((c['sourceActor']['HeroPath'] is None)==(c['sourceActor']['classLevel']<10) for c in d['currentExamples'])},{'check':'Eight ordered current cases','passed':[c['id'] for c in d['currentExamples']]==[c['id'] for c in old['currentExamples']]},{'check':'All expected outcomes unchanged','passed':[c['expectedFinalState'] for c in d['currentExamples']]==[c['expectedFinalState'] for c in old['currentExamples']]}]
 assert all(x['passed'] for x in checks)
 for b in d['sourceBindings']:assert info(G/b['path'])==b
 out.write_bytes(encoded(d));checkp.write_bytes(encoded({'candidate':info(out),'checks':checks,'failureCount':0,'sourceBindings':len(d['sourceBindings']),'runtimeTestsExecuted':0,'newRuleAdoptions':0}));print(json.dumps({'candidate':info(out),'checks':len(checks),'currentCases':8,'remaining':20}))

if __name__=='__main__':main()
