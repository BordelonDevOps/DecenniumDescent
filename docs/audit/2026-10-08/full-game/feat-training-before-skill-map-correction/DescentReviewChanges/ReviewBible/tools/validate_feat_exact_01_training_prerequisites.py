"""Validate authored training witnesses against measured current source files.

Read-only against source rules/candidates; creates a new report and reader note.
Payment checks deliberately do not claim complete feat-specific acquisition.
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import json
from pathlib import Path
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_training_prerequisite_model import materialize_training, meets_training_prerequisite

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
parser=argparse.ArgumentParser()
parser.add_argument('--report',type=Path,default=A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json')
parser.add_argument('--notes',type=Path,default=A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_NOTES.md')
args=parser.parse_args()
assert not args.report.exists() and not args.notes.exists(),'Preserve historical evidence; use new output paths for a justified rerun.'

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def info(path):
    data=path.read_bytes()
    return {'path':path.relative_to(G).as_posix(),'bytes':len(data),'sha256':sha256(data).hexdigest()}
def serial(value):
    if isinstance(value,set):return sorted(value)
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(x) for x in value]
    return value

checks=[]
def check(label,condition,kind='bounded-behavior',detail=None):
    checks.append({'id':label,'kind':kind,'passed':bool(condition),'detail':serial(detail)})
def reject(label,action,state=None):
    before=deepcopy(state.__dict__) if state is not None else None
    try:action()
    except (ValueError,KeyError,TypeError) as exc:
        check(label,True,'rejection',str(exc))
    else:check(label,False,'rejection','Expected rejection did not occur')
    if state is not None:check(label+'/atomic',state.__dict__==before,'bounded-behavior')

fixture_path=A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json'
fixture=read(fixture_path)
foundation=read(R/'data/playtest/character_foundation.json')
classes={x['class']:x for x in foundation['classes']}
equipment={x['id']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records']}
ancestry=read(R/'data/playtest/ancestry_background_candidate.json')
backgrounds={x['id']:x for x in ancestry['backgrounds']}
skill_abilities=foundation['skillAbilities']
contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
public={x['id']:x for x in read(R/'data/public/feat_candidates/exact_01/candidate.json')['feats']}
bindings=fixture['sourceBindings']+[info(fixture_path),info(Path(__file__)),info(R/'tools/feat_exact_01_training_prerequisite_model.py'),info(R/'tools/feat_exact_01_acquisition_models.py')]
for source in bindings:check('source/'+source['path'],info(G/source['path'])==source,'source-integrity')
for row in fixture['completeContracts']:
    check('contract/'+row['id'],row==contracts[row['id']],'source-integrity')
    p=public[row['id']]
    # The eight earlier reviewed envelopes retain their own nested projection.
    check('original/'+row['id'],p['sourceObject']==row['originalObject'],'source-integrity')
    if isinstance(p.get('operationalRules'),str):
        check('procedure/'+row['id'],p['operationalRules']==row['completeOperativeProcedure'],'source-integrity')
for name,row in fixture['firstClassSources'].items():
    check('class-row/'+name,row==classes[name],'source-integrity')
    check('class-descendant/'+name,info(G/row['classCandidatePath'])['sha256']==row['classCandidateSha256'],'source-integrity')

# Explicit source assertions for the finite training projection, independent of its parser.
rows={
 'Bard':('Light','Simple weapons; musical instruments used as improvised weapons','Three musical instruments'),
 'Monk':('None','Simple weapons; kama; nunchaku; staff',"One artisan's tool"),
 'Paladin':('Light; Medium; Heavy; Shields','Simple weapons; Martial weapons','None'),
 'Shaman':('Light','Clubs; spears; staves',"Alchemist's supplies; herbalism kit"),
 'Soldier':('Light; Medium; Heavy; Shields','Repeating heavy crossbows; actual equipment explicitly classified as a sidearm',"Carpenter's tools; siege engineer's kit"),
 'Thief':('Light','Daggers; shortswords; hand crossbows; actual Thrown-property weapons',"Thieves' tools; poisoner's kit"),
 'Warrior':('Medium; Heavy','Martial weapons','None'),
}
for name,expected in rows.items():check('actual-training-row/'+name,tuple(classes[name][k] for k in ['armor','weapons','tools'])==expected,'source-data')
human=next(x for x in ancestry['ancestries'] if x['id']=='human')
imperial=next(x for x in human['variants'] if x['id']=='imperial-human')
check('ancestry-bonuses-once',imperial['combinedAbilityBonuses']=={'STR':1,'DEX':1,'CON':1,'INT':1,'WIS':1,'CHA':2},'source-data')
check('human-training',next(x for x in human['traits'] if x['name']=='Versatility')['text']=='You gain proficiency in one skill of your choice.','source-data')
check('imperial-training',next(x for x in imperial['traits'] if x['name']=='Social Intuition')['text'].startswith('You have proficiency in the Persuasion skill.'),'source-data')
guide=(R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md').read_text(encoding='utf-8')
check('creation-duplicate-rule','fixed' in guide.lower() and '20' in guide and 'duplicate training' in guide,'source-data')

def training(who):return materialize_training(who,classes,equipment,skill_abilities,ancestry,backgrounds)
def predicate(sid,who,t):return meets_training_prerequisite(contracts[sid]['requirements'],who,t,equipment,skill_abilities)

def payment_history(who,label):
    first=who['firstClass'];level=who['classLevels'][first]
    prior_levels=[x['classLevel'] for x in who['priorFeatChoices']]
    check(label+'/prior-schedule',prior_levels==[n for n in classes[first]['asiClassLevels'] if n<who['targetClassOpportunity']],'paid-history')
    pay=PaidChoices({name:row['asiClassLevels'] for name,row in classes.items()}, {}, {first:1},deepcopy(who['permanentScores']),set(contracts))
    prefix=[]
    for grant in who['priorFeatChoices']:
        at=deepcopy(who);at['classLevels']={first:grant['classLevel']};at['priorFeatChoices']=deepcopy(prefix)
        before=training(at)
        actual=predicate(grant['featId'],at,before)
        # Validate the ordered choices before granting their downstream credential.
        at['priorFeatChoices'].append(grant);after=training(at)
        check(label+'/prior-'+str(grant['classLevel']),actual,'paid-history')
        pay.current_classes={first:grant['classLevel']}
        op=first+':'+str(grant['classLevel']);pay.earn_class_opportunity(op,first,grant['classLevel'])
        pay.commit(grant['featId'],op,choice=grant,prerequisites_met=actual)
        prefix.append(grant)
    pay.current_classes={first:level}
    now=training(who);pay.weapon_proficiencies=set(now['weapons'])
    return pay

traces=[];cohort=set(fixture['cohortIds'])
check('cohort-size',len(cohort)==48,'coverage')
for case in fixture['cases']:
    sid=case['featId'];who=case['actor'];label=case['id']
    t=training(who)
    # Separate arithmetic verification of the chosen four-d6 receipts and ancestry once.
    expected_scores={k:sum(sorted(d)[1:])+(2 if k=='CHA' else 1) for k,d in who['abilityRolls'].items()}
    check(label+'/scores',t['scores']==expected_scores==who['permanentScores'],'actor-source')
    check(label+'/complete-starting-skill-choice',len(who['selectedClassSkills'])==classes[who['firstClass']]['skillChoices'] and set(who['selectedClassSkills'])<=set(classes[who['firstClass']]['skillOptions']),'actor-source')
    actual=predicate(sid,who,t)
    check(label+'/predicate',actual==case['expectedPrerequisite'],detail={'expected':case['expectedPrerequisite'],'actual':actual,'reason':case['reason']})
    pay=payment_history(who,label)
    op=who['firstClass']+':'+str(who['targetClassOpportunity'])
    choice=who.get('weaponChoice')
    reject(label+'/without-earned-choice',lambda:pay.commit(sid,op,choice=choice,prerequisites_met=actual),pay)
    pay.earn_class_opportunity(op,who['firstClass'],who['targetClassOpportunity'])
    if actual:
        pay.commit(sid,op,choice=choice,prerequisites_met=actual)
        check(label+'/paid-once',pay.opportunities[op]['spent'] and pay.grants[-1]['identity']==sid,'paid-history')
        reject(label+'/spent-choice-reuse',lambda:pay.commit('alertness',op,prerequisites_met=True),pay)
    else:
        reject(label+'/failed-prerequisite',lambda:pay.commit(sid,op,choice=choice,prerequisites_met=actual),pay)
        check(label+'/choice-remains',not pay.opportunities[op]['spent'],'paid-history')
    modifiers={name:(t['scores'][skill_abilities[name]]-10)//2 + ({4:2,8:3,12:4}[t['totalLevel']])*factor for name,factor in t['skills'].items()}
    traces.append({'case':label,'featId':sid,'sourcePrintedPrerequisite':contracts[sid]['printedPrerequisite'],
                   'normalizedRequirements':contracts[sid]['requirements'],'actor':who,'derivedTraining':serial(t),
                   'permanentSkillModifiersIndependentArithmetic':modifiers,'prerequisiteMet':actual,
                   'paymentHistory':serial(pay.__dict__),'completeFeatAcquisitionValidated':False})

by_case={x['case']:x for x in traces}
def td(label):return by_case[label]['derivedTraining']
check('longbow-or-shortbow/long-only','martial-ranged-weapons.longbow' in td('bowyer/source-training')['weapons'] and 'simple-ranged-weapons.shortbow' not in td('bowyer/source-training')['weapons'])
check('longbow-or-shortbow/short-only','simple-ranged-weapons.shortbow' in td('bowyer/shortbow-only')['weapons'] and 'martial-ranged-weapons.longbow' not in td('bowyer/shortbow-only')['weapons'])
check('thief-hand-crossbow-spelling','martial-ranged-weapons.crossbow-hand' in td('lock_savant/source-training')['weapons'])
check('shaman-finite-profiles',set(td('cleaving_momentum/shaman-versatile-thrown')['weapons'])=={'simple-melee-weapons.club','simple-melee-weapons.spear','simple-melee-weapons.quarterstaff'})
check('no-soldier-martial-inference','martial-melee-weapons.whip' not in td('battlefield_tactician/source-training')['weapons'])
check('warrior-no-imported-shield-light','shields' not in td('shield_expert/wrong-source-training')['armor'] and 'light' not in td('moderately_armored/wrong-source-training')['armor'])
check('nature-bridge-without-survival','Nature' in td('anatomy_lore/source-training')['skills'] and 'Survival' not in td('anatomy_lore/source-training')['skills'])
check('survival-without-nature','Survival' in td('anatomy_lore/survival-only')['skills'] and 'Nature' not in td('anatomy_lore/survival-only')['skills'])
check('engineering-without-thieves','Engineering' in td('trapsetter/source-training')['skills'] and 'tools.thieves-tools' not in td('trapsetter/source-training')['tools'])
check('thieves-without-engineering','Engineering' not in td('trapsetter/thieves-tools-only')['skills'] and 'tools.thieves-tools' in td('trapsetter/thieves-tools-only')['tools'])

special=[]
for name,who in fixture['specialTrainingCases'].items():
    t=training(who);pay=payment_history(who,'special/'+name)
    special.append({'id':name,'actor':who,'derivedTraining':serial(t),'priorPaymentHistory':serial(pay.__dict__)})
    if name in {'expertiseNewSkill','expertiseThenNaturalist'}:
        check(name+'/nature-replaces-pb',t['skills']['Nature']==2)
        check(name+'/no-four-pb',all(n in {1,2} for n in t['skills'].values()))
        check(name+'/no-ability-increase',t['scores']==who['permanentScores'])
    if name=='expertiseThenNaturalist':check(name+'/new-survival',t['skills']['Survival']==1)
    if name=='lockAtLevelEight':check(name+'/ordinary-tool-five',(t['scores']['DEX']-10)//2+3==5 and 'tools.thieves-tools' in t['tools'])

base=deepcopy(next(x['actor'] for x in fixture['cases'] if x['id']=='field_medic/source-training'))
bad=deepcopy(base);bad['selectedClassSkills'][0]='Thievery'
reject('reject-invented-skill',lambda:training(bad))
bad_duplicate=deepcopy(base);bad_duplicate['selectedClassSkills']=[base['selectedClassSkills'][0]]*3
reject('reject-duplicate-starting-choice',lambda:training(bad_duplicate))
bad_tools=deepcopy(base);bad_tools['classToolChoices']=['tools.drum']*3
reject('reject-duplicate-instrument-choice',lambda:training(bad_tools))
bad_scores=deepcopy(base);bad_scores['permanentScores']['INT']+=1
reject('reject-unearned-ability-increase',lambda:training(bad_scores))
bad_dice=deepcopy(base);bad_dice['abilityRolls']['INT']=[7,6,6,6]
reject('reject-invalid-rolls',lambda:training(bad_dice))
bad_multiclass=deepcopy(base);bad_multiclass['classLevels']['Warrior']=1
reject('reject-unmodeled-multiclass-training',lambda:training(bad_multiclass))
bad_expertise=deepcopy(fixture['specialTrainingCases']['expertiseNewSkill']);bad_expertise['priorFeatChoices'][0]['expertiseSkill']='thieves tools'
reject('reject-skill-expertise-as-tool-expertise',lambda:training(bad_expertise))
bad_expertise2=deepcopy(fixture['specialTrainingCases']['expertiseNewSkill']);bad_expertise2['priorFeatChoices'][0]['newSkill']='Persuasion'
reject('reject-skill-expert-already-trained-new-skill',lambda:training(bad_expertise2))

# Actual repeatability rules with distinct, source-proficient profiles and earned opportunities.
who=deepcopy(next(x['actor'] for x in fixture['cases'] if x['id']=='weaponFocus/source-training'))
t=training(who);p=payment_history(who,'weapon-focus-history');p.earn_class_opportunity('Warrior:4','Warrior',4)
p.commit('weaponFocus','Warrior:4',choice='martial-melee-weapons.longsword',prerequisites_met=predicate('weaponFocus',who,t))
p.current_classes={'Warrior':8};p.earn_class_opportunity('Warrior:8','Warrior',8)
reject('weapon-focus-same-profile-repeat',lambda:p.commit('weaponFocus','Warrior:8',choice='martial-melee-weapons.longsword',prerequisites_met=True),p)
who['classLevels']={'Warrior':8};who['weaponChoice']='martial-melee-weapons.whip';t=training(who)
p.commit('weaponFocus','Warrior:8',choice=who['weaponChoice'],prerequisites_met=predicate('weaponFocus',who,t))
check('weapon-focus-distinct-profile-paid',len(p.grants)==2 and all(x['spent'] for x in p.opportunities.values()))
focus_history=serial(p.__dict__)
who=deepcopy(next(x['actor'] for x in fixture['cases'] if x['id']=='weapon_mastery/source-training'))
t=training(who);p=payment_history(who,'weapon-mastery-history');p.earn_class_opportunity('Warrior:8','Warrior',8)
p.commit('weapon_mastery','Warrior:8',choice=who['weaponChoice'],prerequisites_met=predicate('weapon_mastery',who,t))
p.current_classes={'Warrior':12};p.earn_class_opportunity('Warrior:12','Warrior',12)
reject('weapon-mastery-nonrepeatable',lambda:p.commit('weapon_mastery','Warrior:12',choice='martial-melee-weapons.whip',prerequisites_met=True),p)

def kinds(node):return {node['kind']}|set().union(*(kinds(x) for x in node.get('requirements',[])))
numeric={sid for sid,row in contracts.items() if kinds(row['requirements'])<={'all','any','permanentAbility','totalCharacterLevel','noPrintedPrerequisite'}}
warrior={sid for sid,row in contracts.items() if row.get('sharedPaidIdentity')}
remaining=[{'id':sid,'name':row['name'],'printedPrerequisite':row['printedPrerequisite'],'requirements':row['requirements']} for sid,row in contracts.items() if sid not in numeric|warrior|cohort]
check('disjoint-predicate-cohorts',len(numeric)==209 and len(warrior)==12 and len(remaining)==66 and not numeric&cohort and not warrior&cohort,'coverage')
check('every-cohort-primary-qualifies',all(by_case[sid+'/source-training']['prerequisiteMet'] for sid in cohort),'coverage')
check('every-source-still-unchanged',all(info(G/x['path'])==x for x in bindings),'source-integrity')
failures=[x for x in checks if not x['passed']]
report={
 'createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'passed-finite-training-projections' if not failures else 'failed-finite-training-projections',
 'scope':fixture['scope'],'sourceBindings':bindings,'counts':{'trainingPredicateFeats':48,'authoredCases':len(traces),'specialTrainingCases':len(special),'earlierNumericPredicateFeats':209,'earlierWarriorIdentities':12,'remainingCredentialDependentFeats':len(remaining)},
 'checks':len(checks),'checkKinds':dict(Counter(x['kind'] for x in checks)),'failures':failures,'results':checks,
 'caseTraces':traces,'specialTrainingTraces':special,'weaponFocusDistinctPaidHistory':focus_history,
 'weaponMasteryNonrepeatableHistory':serial(p.__dict__),'remaining':remaining,
 'limits':[fixture['unprofiledGrantLimit'],fixture['unmodeledLegacyBranch'],
 'Class-card training grants and complete class-card selections are not modeled. The examples prove these starting/prior-feat grants suffice, or fail within the stated projection; a negative case is not a claim that every complete build of that class fails.',
 'Half-feat ability allocation, all permanent named choices beyond tested weapon/training choices, initial resources and full use procedures are not validated by a prerequisite/payment record.',
 'Four-d6 witnesses are mathematically possible synthetic rolls, not authenticated user rolls or actual campaign feat awards.'],
 'allTrainingCohortCompleteAcquisitionsValidated':False,'all335ActualAcquisitionBoundaryCasesExecuted':False,
 'candidateReadyForSubmission':False,'noNewRulesAdopted':True,'sourceInformationDeleted':False,
}
with args.report.open('x',encoding='utf-8',newline='\n') as stream:json.dump(report,stream,ensure_ascii=False,indent=2);stream.write('\n')
notes=f'''# Feat training prerequisites: 48 finite source projections

{len(traces)} authored cases cover 48 feat prerequisite trees, with actual first-class training, complete starting skill/tool choices, Human/Imperial bonuses applied once, background grants, and earned/unspent class opportunities. Result: {len(checks)} checks, {len(failures)} failures. Full source objects and operative procedures remain in the fixture; each trace records its training and payment history.

These are partial synthetic character projections. They establish prerequisite and payment behavior, not complete feat acquisitions, complete class-card builds, human rolls, full feat effects, or readiness for publication. Negative examples use only their stated source grants; a later class-card grant could change a complete character's training.

The cases distinguish actual profile proficiency from equipment ownership, thrown melee weapons from ranged profiles, and Versatile from Two-Handed. A character holding a longsword can still qualify through its Greatsword training. Bowyer's two bow branches are tested separately. Skill thresholds use permanent ability modifiers plus PB or replacing 2PB Expertise. Skill Expert supplies no ability increase or tool Expertise; Naturalist cannot stack Expertise into 4PB. The Soldier witness uses its actual class identity without importing its broader multiclass training row.

The Nature/Survival Anatomy Lore alternatives are exercised. No legacy Knowledge receipt is fabricated. The finite equipment projection leaves Soldier-specific unprofiled equipment grants unresolved rather than treating missing profiles as evidence of no proficiency.

Predicate coverage is now 209 numeric/level/None identities, 12 Warrior mutation identities, and 48 training identities, with 66 other credential-dependent identities remaining. Those are disjoint predicate groups, not 269 fully implemented or approved feats. Full selection choices, resources, use procedures, remaining finite acceptance cases, and actual GPT exact-candidate review remain open. No rules were changed, no source information was deleted, no GitHub push occurred, and cosmology remains deferred.

Evidence: `FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json` and `FEAT_EXACT_01_TRAINING_PREREQUISITE_CHECK.json` in this folder. The validator is read-only against source data and refuses to overwrite an existing report.
'''
with args.notes.open('x',encoding='utf-8',newline='\n') as stream:stream.write(notes)
print(json.dumps({'report':info(args.report),'notes':info(args.notes),'counts':report['counts'],'checks':len(checks),'failures':failures},indent=2))
raise SystemExit(bool(failures))
