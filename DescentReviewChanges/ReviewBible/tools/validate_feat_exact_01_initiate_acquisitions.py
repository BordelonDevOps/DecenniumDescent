"""Exercise paid Magic Initiate choices against all sixteen actual curricula."""
from collections import Counter
from copy import deepcopy
from datetime import datetime,timezone
from hashlib import sha256
import argparse
import json
from pathlib import Path
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
parser=argparse.ArgumentParser()
parser.add_argument('--report',type=Path,default=A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json')
parser.add_argument('--notes',type=Path,default=A/'FEAT_EXACT_01_INITIATE_ACQUISITION_NOTES.md')
args=parser.parse_args();assert not args.report.exists() and not args.notes.exists(),'Use new outputs; preserve historical checks.'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def serial(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v
checks=[]
def check(label,ok,kind='bounded-behavior',details=None):checks.append({'id':label,'kind':kind,'passed':bool(ok),'details':serial(details)})
def reject(label,obj,call):
    before=obj.snapshot()
    try:call()
    except (ValueError,KeyError,TypeError) as exc:check(label,True,'rejection',str(exc))
    else:check(label,False,'rejection','Expected rejection did not occur')
    check(label+'/atomic',before==obj.snapshot())

foundation=read(R/'data/playtest/character_foundation.json');classes={x['class']:x for x in foundation['classes']}
skills={s:a for a,items in foundation['skillAbilities'].items() for s in items}
ancestry=read(R/'data/playtest/ancestry_background_candidate.json');backgrounds={x['id']:x for x in ancestry['backgrounds']}
equipment={x['id']:x for x in read(R/'data/playtest/equipment_source_catalog.json')['records']}
contracts={x['id']:x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}
groups={x['id']:x for x in read(R/'data/public/feat_candidates/exact_01/supplements.json')['groups']}
curricula=groups['SUP-04']['value']
dependencies=read(R/'data/public/feat_candidates/exact_01/spell_dependencies.json')['spells']
placements=read(R/'data/public/feat_candidates/exact_01/spell_placements.json')['placements']
fixture=read(A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json')
actor=deepcopy(next(x['actor'] for x in fixture['cases'] if x['id']=='weaponFocus/source-training'))
actor.pop('weaponChoice');actor['classLevels']={'Warrior':1};actor['targetClassOpportunity']=None;actor['priorFeatChoices']=[]

# Authored examples, retaining actual curriculum-specific school/source-class distinctions.
CHOICES={
 'Bard':('CHA',['daze','calm-whispers'],'shield'),
 'Cleric':('WIS',['arcane-ward','dispel-minor'],'shield'),
 'Crimson Agent':('INT',['daze','calm-whispers'],'charm-person'),
 'Dragoon':('STR',['flare-spark','dust-gust'],'summon-fire-pet'),
 'Druid':('WIS',['arcane-ward','dispel-minor'],'shield'),
 'Mage':('INT',['arcane-ward','dispel-minor'],'shield'),
 'Monk':('DEX',['arcane-ward','dispel-minor'],'shield'),
 'Mirrorsage':('INT',['detect-poison','foresight-flicker'],'shield'),
 'Paladin':('CHA',['arcane-ward','dispel-minor'],'shield'),
 'Ranger':('WIS',['detect-poison','flare-spark'],'summon-fire-pet'),
 'Shaman':('WIS',['detect-poison','flare-spark'],'summon-fire-pet'),
 'Thief':('DEX',['daze','calm-whispers'],'charm-person'),
 'Tinker':('INT',['arcane-ward','dispel-minor'],'shield'),
 'Wizard':('INT',['arcane-ward','dispel-minor'],'shield'),
 'Sorcerer':('CHA',['sparkbolt','ray-of-frost'],'shield'),
 'Warlock':('CHA',['chill-touch','minor-illusion'],'cause-fear'),
}
def choice(name):return {'curriculum':name,'cantrips':deepcopy(CHOICES[name][1]),'rank1':CHOICES[name][2]}
def create():return InitiateAcquisitions(actor,classes,equipment,skills,ancestry,backgrounds,contracts,curricula,dependencies)
source_paths=[Path(__file__),R/'tools/feat_exact_01_initiate_acquisition_model.py',R/'tools/feat_exact_01_acquisition_models.py',
 R/'tools/feat_exact_01_training_prerequisite_model.py',R/'data/playtest/character_foundation.json',
 R/'data/playtest/ancestry_background_candidate.json',R/'data/playtest/equipment_source_catalog.json',
 R/'data/public/feat_candidates/exact_01/supplements.json',R/'data/public/feat_candidates/exact_01/shared_rules.json',
 R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/feat_candidates/exact_01/spell_placements.json',
 A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json',
 G/classes['Warrior']['classCandidatePath']]
bindings={p.relative_to(G).as_posix():info(p) for p in source_paths}
check('sixteen-curricula',set(CHOICES)==set(curricula) and len(curricula)==16,'source-data')
check('warrior-no-ordinary-pool',all(x==0 for x in classes['Warrior']['rpByClassLevel']),'source-data')
check('warrior-class-binding',info(G/classes['Warrior']['classCandidatePath'])['sha256']==classes['Warrior']['classCandidateSha256'],'source-integrity')
named={sid:sid.removeprefix('magic_initiate_').capitalize() for sid in contracts if sid.startswith('magic_initiate_')}
check('six-named-plus-generic',len(named)==6 and 'magicInitiate' in contracts,'source-data')
traces=[];selected_envelopes={};current_files={}
def verify_route(label,obj,route):
    check(label+'/source-ability',route['castingAbility']==CHOICES[route['curriculum']][0],'source-data')
    check(label+'/three-distinct-selected',len(route['spells'])==3 and len({x['id'] for x in route['spells']})==3)
    check(label+'/ranks-zero-zero-one',sorted(x['rank'] for x in route['spells'])==[0,0,1])
    check(label+'/no-class-or-rp',obj.actor['classLevels']=={'Warrior':4} and obj.rp=={'maximum':0,'current':0} and not obj.ordinaryClassRepertoire)
    check(label+'/initial-single-charge',route['rankOneCharge']=={'maximum':1,'current':1})
    check(label+'/no-rank-three-grant',not obj.initial_grant_matches(minimum_rank=3))
    check(label+'/paid-opportunity',obj.pay.opportunities['Warrior:4']['spent'] and len(obj.pay.grants)==1,'paid-history')
    for row in route['spells']:
        dep=dependencies[row['id']];selected_envelopes[row['id']]=dep
        expected=[x for x in placements if x.get('route')=='curriculum' and x.get('curriculum')==route['curriculum'] and x['id']==row['id'] and x['rank']==row['rank']]
        check(label+'/'+row['id']+'/placement',len(expected)==1 and expected[0]['school']==row['school'] and expected[0]['sourceClass']==row['sourceClass'],'source-data')
        bind=dep['binding'];path=G/bind['file']
        if bind['file'] not in current_files:
            measured=info(path);bindings[measured['path']]=measured
            check('spell-file/'+bind['file'],measured['bytes']==bind['bytes'] and measured['sha256']==bind['sha256'],'source-integrity')
            current_files[bind['file']]=read(path)
        card=current_files[bind['file']]
        for token in bind['pointer'].strip('/').split('/'):card=card[int(token)] if isinstance(card,list) else card[token]
        check(label+'/'+row['id']+'/whole-current-card',card==dep['completeCurrentProcedureCard'],'source-integrity')
        check(label+'/'+row['id']+'/grant-matches',obj.initial_grant_matches(spell_id=row['id'],school=row['school'],exact_rank=row['rank']))
    traces.append({'id':label,'selectedChoice':deepcopy(obj.pay.grants[-1]['choice']),'final':serial(obj.snapshot())})

for curriculum in CHOICES:
    obj=create();obj.advance(4);obj.earn(4);route=obj.acquire('magicInitiate',4,choice(curriculum));verify_route('generic/'+curriculum,obj,route)
for sid,curriculum in named.items():
    obj=create();obj.advance(4);obj.earn(4);route=obj.acquire(sid,4,choice(curriculum));verify_route('named/'+curriculum,obj,route)
    for first,second in [('magicInitiate',sid),(sid,'magicInitiate')]:
        obj=create();obj.advance(4);obj.earn(4);obj.acquire(first,4,choice(curriculum))
        # Conditional existing spent-charge state; no cast/effect is claimed executed.
        obj.routes[0]['rankOneCharge']['current']=0
        obj.advance(8);obj.earn(8)
        reject('duplicate-family/'+curriculum+'/'+first,obj,lambda:obj.acquire(second,8,choice(curriculum)))
        check('duplicate-family/'+curriculum+'/'+first+'/no-refill',obj.routes[0]['rankOneCharge']['current']==0 and not obj.pay.opportunities['Warrior:8']['spent'])
        traces.append({'id':'duplicate-family/'+curriculum+'/'+first,'conditionalPremise':'The original charge was legitimately spent earlier; that cast is not simulated here.','final':serial(obj.snapshot())})

for first,first_curr,second,second_curr in [('magic_initiate_bard','Bard','magic_initiate_wizard','Wizard'),
 ('magicInitiate','Wizard','magic_initiate_bard','Bard'),('magic_initiate_bard','Bard','magicInitiate','Wizard')]:
    obj=create();obj.advance(4);obj.earn(4);obj.acquire(first,4,choice(first_curr));obj.advance(8);obj.earn(8);obj.acquire(second,8,choice(second_curr))
    check('distinct-curricula/'+first+'/'+second,len(obj.routes)==2 and len(obj.pay.grants)==2 and all(v['spent'] for v in obj.pay.opportunities.values()),'paid-history')
    shields=[(r['curriculum'],s['school'],r['castingAbility']) for r in obj.routes for s in r['spells'] if s['id']=='shield']
    check('same-spell-distinct-placements/'+first+'/'+second,set(shields)=={('Bard','Universal','CHA'),('Wizard','Abjuration','INT')})
    traces.append({'id':'distinct-curricula/'+first+'/'+second,'final':serial(obj.snapshot())})

obj=create();obj.advance(4);obj.earn(4);obj.acquire('magicInitiate',4,choice('Wizard'));obj.advance(8);obj.earn(8)
reject('generic-identity-is-nonrepeatable',obj,lambda:obj.acquire('magicInitiate',8,choice('Bard')))
obj=create();obj.advance(4)
reject('none-prerequisite-no-free-feat',obj,lambda:obj.acquire('magicInitiate',4,choice('Wizard')))
obj.earn(4)
invalids={
 'duplicate-cantrips':{'curriculum':'Wizard','cantrips':['arcane-ward','arcane-ward'],'rank1':'shield'},
 'one-cantrip':{'curriculum':'Wizard','cantrips':['arcane-ward'],'rank1':'shield'},
 'three-cantrips':{'curriculum':'Wizard','cantrips':['arcane-ward','dispel-minor','friends'],'rank1':'shield'},
 'cantrip-in-rank-one-slot':{'curriculum':'Wizard','cantrips':['arcane-ward','dispel-minor'],'rank1':'friends'},
 'rank-one-in-cantrip-slot':{'curriculum':'Wizard','cantrips':['shield','dispel-minor'],'rank1':'shield'},
 'rank-three-not-granted':{'curriculum':'Wizard','cantrips':['arcane-ward','dispel-minor'],'rank1':'dispel-magic'},
 'invented-spell':{'curriculum':'Wizard','cantrips':['unlimited-free-fire','dispel-minor'],'rank1':'shield'},
 'no-warrior-curriculum':{'curriculum':'Warrior','cantrips':['arcane-ward','dispel-minor'],'rank1':'shield'},
 'caller-cannot-relabel-school':{**choice('Wizard'),'school':'Universal'},
}
for label,value in invalids.items():reject('selection/'+label,obj,lambda value=value:obj.acquire('magicInitiate',4,value))
reject('named-curriculum-mismatch',obj,lambda:obj.acquire('magic_initiate_bard',4,choice('Wizard')))
reject('unknown-named-identity',obj,lambda:obj.acquire('magic_initiate_warrior',4,choice('Wizard')))

# Exact current reviewed descendants control these two formerly blocked catalog records.
obj=create();obj.advance(4);obj.earn(4)
special_choice={'curriculum':'Bard','cantrips':['mage-hand','prestidigitation'],'rank1':'find-familiar'}
route=obj.acquire('magicInitiate',4,special_choice);verify_route('current-low-rank-descendants',obj,route)
for sid in ['mage-hand','prestidigitation']:
    check('reviewed-current-over-preserved-status/'+sid,dependencies[sid]['originalCatalogRecord']['status']=='blocked-pending-operational-review' and dependencies[sid]['authoredIndexEntry']['authoredStatus']=='reviewed-authored-operational-playtest','source-data')
obj=create();obj.advance(4);obj.earn(4)
route=obj.acquire('magicInitiate',4,{'curriculum':'Wizard','cantrips':['friends','arcane-ray'],'rank1':'find-familiar'});verify_route('diverse-school-selected-entitlements',obj,route)
check('selected-schools-are-not-union',obj.initial_grant_matches(school='Enchantment') and obj.initial_grant_matches(school='Evocation') and obj.initial_grant_matches(school='Universal') and not obj.initial_grant_matches(school='Abjuration'))
check('selected-familiar-not-dispel',obj.initial_grant_matches(spell_id='find-familiar') and not obj.initial_grant_matches(spell_id='dispel-magic'))
obj.routes[0]['rankOneCharge']['current']=0
reject('depleted-casting-prerequisite-not-adjudicated',obj,lambda:obj.initial_grant_matches(spell_id='find-familiar'))
check('original-335-count-unchanged',len(contracts)==335,'coverage')
check('all-source-inputs-unchanged',all(info(G/x['path'])==x for x in bindings.values()),'source-integrity')
failures=[x for x in checks if not x['passed']]
scope=('Paid selection and initial named-spell entitlements for all16 supplied curricula and all6 named Magic Initiate identities. '
       'No ordinary class/RP/repertoire grant; exact school/source placement and duplicate-family payment checks. '
       'This does not adjudicate depleted/suppressed ability-to-cast prerequisites or simulate spell components, payments, targets, effects or full class builds.')
report={
 'createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'passed-finite-initiate-acquisitions' if not failures else 'failed-finite-initiate-acquisitions',
 'scope':scope,'sourceBindings':list(bindings.values()),'completeFeatContracts':{sid:contracts[sid] for sid in ['magicInitiate',*named]},
 'selectedSpellSourceEnvelopes':selected_envelopes,'actorSourceProjection':actor,'authoredCurriculumChoices':CHOICES,
 'counts':{'curricula':16,'namedFeatIdentities':6,'genericFeatIdentities':1,'recordedHistories':len(traces),'sourceSpellIdentities':len(selected_envelopes),
 'remainingCredentialDependentIdentities':56,'newlyClosedCredentialPredicateIdentities':0},
 'checks':len(checks),'checkKinds':dict(Counter(x['kind'] for x in checks)),'failures':failures,'results':checks,'histories':traces,
 'unresolvedCastingQuestion':'Define retained acquired casting entitlement versus immediate cast executability for depleted charges/RP, temporary suppression, component absence and class preparation. Seek a narrow actual GPT clarification before treating these states as generic ability-to-cast prerequisite results.',
 'allSevenFeatsFullUsesValidated':False,'all335ActualAcquisitionBoundaryCasesExecuted':False,'candidateReadyForSubmission':False,
 'newRulesAdopted':False,'sourceInformationDeleted':False,'cosmologyReviewed':False,
}
with args.report.open('x',encoding='utf-8',newline='\n') as stream:json.dump(report,stream,ensure_ascii=False,indent=2);stream.write('\n')
notes=f'''# Magic Initiate: paid curriculum selections

All16 supplied curricula and all6 named Magic Initiate feats now have source-qualified selection histories. {len(checks)} checks pass with {len(failures)} failures. Each selection pays an earned Warrior class feat opportunity, fixes two distinct cantrip identities plus one rank-one identity, and preserves the exact school, source class, casting ability and reviewed spell text.

This covers the generic identity and six named identities already included in the earlier numeric prerequisite group. It adds no new original feat, closes no additional credential-dependent prerequisite tree, and leaves56 such identities remaining.

The cases prevent duplicate curriculum charges through generic/named aliases, prevent repetition of the generic identity for a different curriculum, and allow two separately paid different curricula where the actual feat identities permit it. A previously spent charge is supplied as a conditional state premise in the duplicate tests and stays spent after rejection. No spell-use event is claimed executed.

The same Shield identity keeps Bard's Universal/CHA placement and Wizard's Abjuration/INT placement. Dragoon's curriculum uses STR; Monk and Thief use DEX. The Sorcerer and Warlock curricula supply feat-only choices without creating either class. A Warrior acquires no RP pool, Wizard level, ordinary prepared position or rank progression. The current reviewed Mage Hand/Prestidigitation descendants remain distinct from their preserved older blocked catalog records.

The diverse Wizard example chooses Friends (rank0 Enchantment), Arcane Ray (rank0 Evocation) and Find Familiar (rank1 Universal). These are recorded entitlements, not proof of every immediate casting condition or of Dispel Magic/rank3/rank5 access. Depleted charges, suppression, missing components and preparation changes need a narrow acquisition-prerequisite interpretation before the remaining casting trees are reported covered.

The report preserves the involved seven complete feat contracts, selected whole spell source envelopes, source bindings and paid histories. Full casting/effect validation, the unfinished exact candidate, human balance, final whole-game agreement, GitHub push and cosmology review remain separate.
'''
with args.notes.open('x',encoding='utf-8',newline='\n') as stream:stream.write(notes)
print(json.dumps({'report':info(args.report),'notes':info(args.notes),'counts':report['counts'],'checks':len(checks),'failures':failures},indent=2))
raise SystemExit(bool(failures))
