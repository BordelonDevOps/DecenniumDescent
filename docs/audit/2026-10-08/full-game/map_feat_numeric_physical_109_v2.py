"""Join finite FXC07/08 requirements to complete existing evidence, with four new boundary examples."""
from pathlib import Path
import copy,datetime,hashlib,json,re,zipfile

A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
OUT=A/'feat335-numeric-physical-109-v2';OUT.mkdir(exist_ok=False)
P=A/'feat335-planar-reference-108/after/data/director/feat_candidates/exact_01/candidate.json'
S=A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/shared_rules.json'
R=A/'feat335-assembly-106/ALL_CASE_REVIEWS.json'
C=A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md'
checks=[]
def h(b):return hashlib.sha256(b).hexdigest()
def ser(v):return (json.dumps(v,ensure_ascii=False,indent=2)+chr(10)).encode()
def bind(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':h(b)}
def ck(n,v):
    checks.append({'name':n,'passed':bool(v)});assert v,n
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
candidate=json.loads(P.read_bytes());shared=json.loads(S.read_bytes());reviews=json.loads(R.read_bytes())
feat={x['id']:(i,x) for i,x in enumerate(candidate['records'])}
oldfeat={x['id']:(i,x) for i,x in enumerate(candidate['unchangedReviewedFeats'])}
rules={x['id']:(i,x) for i,x in enumerate(shared['rules'])}
contract=C.read_text(encoding='utf8')
source_info={
 'resolution85':('FEAT335_RESOLUTION_CASES_85.json','fa753b291513edd57067553907627787cb48976c9c2bedf129bfb7a9917cd906',36),
 'healing89':('FEAT335_HEALING_COMPOSITIONS_89.json','64b044d33854fe2841d3a7cbffccb9e86eff12c8888aa3acd5e7efdb140bb228',56),
 'physical91':('FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json','50439bc127b3ebc05fd1a2a1554fde87a0df6a415144cef3c9b37206cf1c8379',77)}
reports={}
for key,(name,sha,count) in source_info.items():
    p=A/name;b=p.read_bytes();d=json.loads(b)
    ck(key+' frozen report exact',h(b)==sha and len(d['cases'])==count)
    reports[key]={'binding':bind(p),'completeReport':d}
    write(OUT/'evidence'/name,b)
ck('Complete prior semantic register retained',len(reviews['ordinary'])==660 and len(reviews['additional'])==28)

def refs(key,indices):
    out=[]
    for i in indices:
        case=reports[key]['completeReport']['cases'][i]
        out.append({'report':key,'pointer':'/cases/'+str(i),'id':case['id'],'evidenceKind':'HISTORICAL_SOURCE_ADJUDICATION_NOT_SCHEDULER_EXECUTION' if case['id']=='FP91-M13' else 'HISTORICAL_BOUNDED_REFERENCE_CASE_NOT_GAME_RUNTIME'})
    return out

fresh=[]
def extra(id,title,ids,ruleids,initial,operations,expected,kind,projection=None):
    row={'id':id,'title':title,'currentFeatIds':ids,'currentRuleIds':ruleids,'premise':'A conditional authored boundary fixture. Actual lawful acquired sources, body/equipment access, event eligibility and world facts are explicit inputs, not authenticated campaign state. No new mechanical choice is adopted.','initialState':initial,'operations':operations,'expectedFinalState':expected,'evidenceKind':kind,'runtimeExecuted':False}
    if projection is not None:row['freshReferenceProjection']=projection
    fresh.append(row)

# New arithmetic fills the named fixed-Strength versus attack-ability distinction.
v={'STRmodifier':1,'DEXmodifier':4,'PB':3,'actualProficientMeleeAttackOriginallySTR':True,'WeaponFinesseAppliesToAttackOnly':True,'damageIndependentFinesseProperty':False}
numeric={'attackModifier':v['DEXmodifier']+v['PB'],'nativeDamageAbilityModifier':v['STRmodifier'],'DisarmingBlowDC':8+v['PB']+v['DEXmodifier'],'BullRushDC':8+v['PB']+v['STRmodifier'],'ShieldBashStunDC':8+v['PB']+v['STRmodifier']}
ck('New fixed-Strength arithmetic',numeric=={'attackModifier':7,'nativeDamageAbilityModifier':1,'DisarmingBlowDC':15,'BullRushDC':12,'ShieldBashStunDC':12})
extra('FN109-01','Attack substitution does not rewrite explicitly Strength-fixed damage/DCs',['weapon_finesse','disarming_blow','bull_rush','shield_bash'],['FS-05'],v,[{'kind':'Independent legal comparisons, not one granted combined action','declaration':'Use DEX on a qualifying normal STR melee attack. Evaluate each otherwise eligible rider in its own native source scope. This does not supply the approach, Attack Action, usable shield, held object, die payment, stun use or hit.'}],numeric,'NEW_BOUNDED_ARITHMETIC_PROJECTION_NOT_RUNTIME',numeric)

distinct=len({'owner-109','owner-109'})
ck('Same identity cannot form two-person pair',distinct==1)
extra('FP109-01','Ally self-eligibility retains a genuinely separate flanking participant',['coordinator','tactical_flanker'],['FS-05'],{'ownerId':'owner-109','ownerCanPayBonusAction':True,'selfInstructionPredicatesSatisfied':True,'flankingCandidateIds':['owner-109','owner-109'],'otherDistinctCreaturePresent':False},[{'kind':'Independent branches','selfCoordinator':'Pay one actual Bonus Action; create one next-attack entitlement to next original regular START. First attack consumes it even if disadvantage cancels it.','selfFlanking':'Reject using two aliases of the same physical actor as both participants; do not grant a flanking rider or spend its hit-only allowance.'}],{'coordinatorSelfEligible':True,'coordinatorBonusActionsSpent':1,'coordinatorExtraAttacksGranted':0,'distinctFlankingParticipants':1,'tacticalFlankerEligible':False,'flankerRiderDiceGranted':0,'flankerAllowanceSpent':0},'NEW_SOURCE_ADJUDICATED_STATE_BRANCHES_WITH_IDENTITY_COUNT_ONLY',{'distinctPhysicalIds':distinct})

trap_before={'trapId':'snare-109-A','type':'snare','setterId':'setter-109','armed':True,'accessibleBySetterWithSafeReach':True,'physicalAssemblyIntact':True,'parts':['cord-109','spring-109','anchor-109'],'storedDC':13,'setterActionsAvailable':1,'quickPlacementUseSpent':True,'preparedReplacementKitCreated':False,'holderId':None}
trap_disarmed=copy.deepcopy(trap_before);trap_disarmed.update(armed=False,setterActionsAvailable=0)
trap_carried=copy.deepcopy(trap_disarmed);trap_carried.update(holderId='carrier-109',physicalAssemblyIntact=False)
ck('New disarm/custody identity and expenditure invariant',trap_before['trapId']==trap_carried['trapId'] and trap_before['parts']==trap_carried['parts'] and trap_carried['quickPlacementUseSpent'] and not trap_carried['armed'] and not trap_carried['preparedReplacementKitCreated'])
extra('FP109-02','Safe own-trap disarm and actual transport preserve physical stock and spent allowance',['trapsetter'],['FS-10','FS-15'],trap_before,[{'kind':'Own safe disarm','before':trap_before,'after':trap_disarmed,'adjudication':'Actual setter spends one Action with safe reach to accessible own trap. No new roll or consumed complete kit is required by this disarm clause.'},{'kind':'Later lawful physical transport','before':trap_disarmed,'after':trap_carried,'premise':'A separately legal world operation actually collects the same parts and transports them with real custody, load, route and costs; those underlying operations are supplied premises, not granted or priced by this feat. Moving the necessary arrangement leaves it disarmed; actual rearming is still required.'}],trap_carried,'NEW_SOURCE_ADJUDICATED_STATE_SEQUENCE_NOT_NATIVE_PHYSICS_EXECUTION')

disarm={'storedDC':13,'DEXmodifier':3,'actualToolPB':2,'detected':True,'appropriateTools':True,'actualSafeReach':True,'manipulationEntersWorkingTrigger':False,'ActionAvailable':1,'armed':True,'storedQuickUseSpent':True}
branches=[]
for die,success in [(8,True),(5,False)]:
    total=die+3+2
    ck('New other-disarm task '+str(die),(total>=13)==success and die not in [1,20])
    branches.append({'d20':die,'modifier':5,'total':total,'DC':13,'coreDegree':'Success' if success else 'Failure','result':{'ActionAvailable':0,'armed':not success,'triggered':False,'storedQuickUseSpent':True,'newKitCreated':False},'qualification':'Failure does not trigger the mechanism when the actual manipulation did not enter its working trigger. This is not universal failure safety; changed physical contact can change that predicate.'})
extra('FP109-03','Other creature disarms at stored DC; failed safe manipulation does not invent a remote trigger',['trapsetter'],['FS-05','FS-15'],disarm,[{'kind':'Two independent declared task branches','branches':branches}],{'branches':branches},'NEW_BOUNDED_TASK_ARITHMETIC_AND_SOURCE_ADJUDICATION_NOT_RUNTIME',{'totals':[13,10],'successes':[True,False]})

# Each tuple names a finite requirement, complete current sources and exact existing cases.
rows07=[
 ('Native attacks, AC and natural attack results',['weapon_mastery'],['FS-05'],refs('resolution85',range(0,5)),'Native attack rules; a margin is not a critical. Expanded19 still needs an actual hit.'),
 ('Core tasks/natural shifts, opposed ties and binary saves',['resilient_mind','iron_will'],['FS-05'],refs('resolution85',range(5,10)),'Do not transfer task degrees/natural shifts into attacks or binary saves; initiator loses unchanged-state opposed ties.'),
 ('Genuine before-consequence rerolls',['lucky','elvenAccuracy','resilient_mind','slayer_s_resolve'],['FS-05'],refs('resolution85',range(10,14)),'Named die positions versus whole original save procedure, mandatory replacement and no rollback; current mental predicate is separately retained.'),
 ('Independent native percentage floors and typed distribution',['anatomy_lore','precision_strike','giant_slayer','elemental_affinity'],['FS-03','FS-04'],refs('resolution85',range(14,18)),'Independent floor from the same native eligible subtotal; independent external riders excluded; stable typed allocation and defenses follow.'),
 ('Actual damage, temporary HP, overkill, Wounds and death order',['piercer','healer','life_drinker'],['FS-07'],refs('resolution85',range(18,24))+refs('healing89',range(29,36)),'Actual lost normal HP plus absorbed temporary HP, not overkill or state assignment; instant death precedes remaining Wound processing.'),
 ('Per-die versus per-packet additions',['evocation_focus','elementalAdept','berserker','companion_training','durable','quick_recovery'],['FS-03','FS-04','FS-07'],refs('healing89',range(0,12)),'Actual distinct die identities versus flat event/roll additions; rerolls do not create extra dice; no critical doubling of ordinary flats.'),
 ('Current critical ranges and eligible dice',['weapon_mastery','exploit_weakness','piercer','disarming_blow'],['FS-03','FS-05'],refs('resolution85',[18]),'Broadest actual range rather than additive threshold steps; native20 and critical-if-hit remain distinct.'),
 ('Healing installments, Wounds, finite reserves and Critical ceilings',['healer','quick_recovery','durable','field_surgeon','herbalist','life_drinker','bioStabilizer'],['FS-06','FS-07'],refs('healing89',range(0,56))+refs('resolution85',range(24,29)),'First eligible installment, spent Hit Dice/rest epochs, blocked/direct recovery, finite source reserves and max(1,maxHP-1) Critical ceiling. Separate vectors do not simulate the combined nested dispatcher.'),
 ('Explicit Strength-fixed branches and real capacity',['weapon_finesse','disarming_blow','shield_bash','bull_rush','giant_strength','abilityScoreImprovement','tough'],['FS-02','FS-07'],refs('resolution85',[35])+refs('healing89',[53,54,55]),'New FN109-01 adds the exact attack-ability/Strength-fixed comparison. Actual carrying and resource capacity use existing body/class sources; growth does not refill.'),
 ('Source-specific no-resource flags, one paid refund and finite spending',['life_drinker','bioStabilizer','arcane_recall','arcaneResonance','arcane_transfusion'],['FS-07'],refs('resolution85',range(29,36))+refs('healing89',range(29,50)),'Preserve flags through descendants; numeric damage alone cannot erase source prohibitions. One actual payment cannot be refunded twice.')]
rows08=[
 ('Locks remain an Action at actual DC15',['lock_savant','burglar'],['FS-05'],refs('physical91',range(0,8)),'Real tools/custody/failed-lock state; changing picker alone gives no fresh attempt.'),
 ('Persistent caltrop stock, coverage and collection',['trapsetter'],['FS-15'],refs('physical91',range(14,28)),'Every physical piece is in only one location; persistent coverage is not discharged by first entry, save or alias.'),
 ('Actual preparation, trigger, safe disarm, custody and transport',['trapsetter'],['FS-05','FS-10','FS-14','FS-15'],refs('physical91',range(28,40)),'FT84-selected current assembly procedure retained; FP109-02/03 explicitly add safe disarm/custody branches. No provider, parts, transport or rearming permission is fabricated.'),
 ('Self-eligible ally clauses retain their other predicates',['battlefield_commander','target_mark','coordinator','defender','inspiring_presence','natural_leader','primal_instinct'],['FS-05'],[],'Complete source corrections and all14 corresponding original reviewed cases, plus FA07; exact paid actions, perception, range and first-event consumption remain.'),
 ('Genuine other-person and two-body requirements',['tactical_flanker','field_surgeon','leadership'],['FS-05'],[],'Full current sources and original examples; FP109-01 explicitly rejects two aliases as a flanking pair. Self-eligibility supplies no second participant, helper or observer.'),
 ('Actual ranged breath attacks and separate save branch',['slayer_s_resolve'],['FS-05'],[],'Exact CF47-E02 and FA08 distinguish ranged breath attack, non-breath ranged attack and personal breath-save reroll; no invented attack or save.'),
 ('Mount/rider phase, real displacement and shared offense',['cavalry','mounted_combatant','animal_companion','companion_training','bull_rush'],['FS-10'],refs('physical91',range(40,53)),'One real body/phase/ledger, paid mounted interval and carried versus personal movement. FP91-M13 is authored source adjudication, not an executed scheduler.'),
 ('Thirty-minute Haven work and actual subtask integration',['appraise','negotiator','merchant_s_guile'],['FS-13'],refs('physical91',range(59,74)),'Ten-minute feat work is a real nonoverlapping part of the full30-minute Haven transaction, not a duration override.'),
 ('Truthful attainable predeclared social outcomes',['bruiser','silver_tongue','diplomat','commanding_presence','leadership'],['FS-13'],refs('physical91',range(53,59)),'Legitimate channels/actual counterpart agency; no new penalty or cost substituted after a successful predeclared check.'),
 ('Standing bounds and actual history',['appraise','negotiator'],['FS-13'],refs('physical91',range(74,77)),'Standing -3 through+3, signed scene award bounded at2; retain existing earned causes/history.'),
 ('Reference/gross/net and greater-of assay allocation',['appraise','negotiator','merchant_s_guile'],['FS-13'],refs('physical91',range(59,74)),'Separate reference basis, offer/gross/net; exact final copper rounding; actual fees/levy once, greater-of assay, no invented compulsory market.')]

def build(gate,rows,reportkeys,newids,unchanged):
    named=[];selected=set();selectedrules=set()
    for title,ids,rids,case_refs,meaning in rows:
        selected.update(ids);selectedrules.update(rids)
        ordinary=[{'pointer':'/ordinary/'+str(i),'id':x['position']['id'],'featId':x['position']['featId']} for i,x in enumerate(reviews['ordinary']) if x['position']['featId'] in ids]
        additional=[{'pointer':'/additional/'+str(i),'id':x['position']['id'],'featId':x['position']['featId']} for i,x in enumerate(reviews['additional']) if x['position']['featId'] in ids]
        ck(gate+' exact named evidence '+title,bool(case_refs or ordinary or additional))
        named.append({'requirementArea':title,'meaning':meaning,'currentFeatIds':ids,'currentSharedRuleIds':rids,'historicalCaseReferences':case_refs,'completeSemanticRegisterReferences':ordinary+additional,'status':'EXACT_EVIDENCE_MAPPED_FOR_PARENT_REVIEW_NOT_GATE_APPROVAL'})
    current=[]
    for id in sorted(selected):
        idx,r=feat[id];ck(gate+' exact feat '+id,r['id']==id and isinstance(r['operationalRules'],str) and not r['selectionEnabled'] and not r['exactApproved'])
        selected_reviews=[x for x in reviews['ordinary'] if x['position']['featId']==id]
        ck(gate+' complete ordinary case join '+id,len(selected_reviews)==len(r['workedCases']))
        current.append({'binding':bind(P),'pointer':'/records/'+str(idx),'completeCurrentRecord':r,'completeOrdinaryReviews':selected_reviews,'completeAdditionalReviews':[x for x in reviews['additional'] if x['position']['featId']==id]})
    fullrules=[{'binding':bind(S),'pointer':'/rules/'+str(rules[id][0]),'completeCurrentRule':rules[id][1]} for id in sorted(selectedrules)]
    kept=[{'binding':bind(P),'pointer':'/unchangedReviewedFeats/'+str(oldfeat[id][0]),'completeUnchangedReviewedRecord':oldfeat[id][1]} for id in unchanged]
    contractlines=contract.splitlines()
    heading=next((i for i,line in enumerate(contractlines) if line.startswith('## '+gate+' ')),None)
    section=None if heading is None else contractlines[heading+2]
    ck(gate+' complete contract found',section is not None)
    return {'id':'FEAT335-'+gate+'-EXACT-MAPPING-109','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'NAMED_REQUIREMENTS_MAPPED_WITH_COMPLETE_SOURCE_AND_EVIDENCE_PARENT_VERDICT_PENDING','completeOriginalRequirement':section,'contract':bind(C),'namedRequirementMap':named,'completeCurrentFeatJoins':current,'completeCurrentSharedRules':fullrules,'completeUnchangedReviewedSupportingRecords':kept,'completeHistoricalReports':{k:reports[k] for k in reportkeys},'completeNewBoundaryExamples':[x for x in fresh if x['id'] in newids],'semanticRegisterBinding':bind(R),'qualifications':['Historical successful diagnostic programs were not rerun and their counters are not fresh checks. Historical source snapshots/remaining-scope prose are preserved, with current sources and later full case reviews supplied separately.','All660+28 stated cases have separate completed semantic reviews. This join does not repeat them or authenticate an actual character, real item/provider/body/market or world event.','Existing current FT84 and mental-predicate successors govern their exact fields. Old frozen wording is evidence, not revived authority.','Fresh numerical/identity projections are limited to FN109-01 and the numeric parts of FP109-01/03. FP109-02 is source-adjudicated authored state, not physics or custody runtime.','Combined nested healing dispatch, native actor/world scheduling, no-resource source authentication and actual acquisition remain implementation obligations. No blanket authored, engine, human, balance or whole-game approval is inferred.'],'runtimeExecuted':False,'historicalProgramsRerun':False,'canonicalApplied':False,'parentExactGateAccepted':False,'wholeGameComplete':False}

d07=build('FXC-07',rows07,['resolution85','healing89'],['FN109-01'],['field_medic','lifeleech','necrotic_affinity'])
d08=build('FXC-08',rows08,['physical91'],['FP109-01','FP109-02','FP109-03'],['inspiring_leader'])
ck('All new boundary IDs unique',len({x['id'] for x in fresh})==4)
for doc in [d07,d08]:
    ck(doc['id']+' all historical references resolve',all(reports[x['report']]['completeReport']['cases'][int(x['pointer'].split('/')[-1])]['id']==x['id'] for row in doc['namedRequirementMap'] for x in row['historicalCaseReferences']))
    doc['freshMappingChecks']={'passed':len(checks),'failed':0,'scope':'Exact data joins, selected requirement presence, cardinality and the four explicitly bounded new examples; not a rerun of old calculations or game runtime.'}
write(OUT/'FXC07.json',ser(d07));write(OUT/'FXC08.json',ser(d08));write(OUT/'NEW_BOUNDARY_EXAMPLES.json',ser(fresh))
write(OUT/'CHECKS.json',ser({'id':'FEAT335-NUMERIC-PHYSICAL-MAPPING-109-CHECKS','passed':len(checks),'failed':0,'checks':checks}))
write(OUT/'REPRODUCTION_SCRIPT.py',Path(__file__).read_bytes())
files=[{'file':p.relative_to(OUT).as_posix(),**bind(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
write(OUT/'MANIFEST.json',ser({'id':'FEAT335-NUMERIC-PHYSICAL-MAPPING-109-MANIFEST','files':files,'warning':'Reproduction script is retained as source evidence; do not rerun a successful one-shot script.'}))
archive=A/'DD_Feat335_Numeric_Physical_Evidence_109.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for r in files:assert h(z.read(r['file']))==r['sha256']
receipt={'id':'FEAT335-NUMERIC-PHYSICAL-MAPPING-109','archive':bind(archive),'FXC07':bind(OUT/'FXC07.json'),'FXC08':bind(OUT/'FXC08.json'),'newExamples':bind(OUT/'NEW_BOUNDARY_EXAMPLES.json'),'namedAreas':{'FXC07':len(rows07),'FXC08':len(rows08)},'historicalReferenceCases':169,'newBoundaryExamples':4,'passed':len(checks),'failed':0,'actuallySentToGpt':False,'canonicalApplied':False,'runtimeExecuted':False,'parentExactGateAccepted':False}
write(A/'FEAT335_NUMERIC_PHYSICAL_MAPPING_RECEIPT_109.json',ser(receipt));write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps(receipt))
