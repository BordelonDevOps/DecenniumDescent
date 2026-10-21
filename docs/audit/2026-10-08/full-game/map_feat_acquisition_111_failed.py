from pathlib import Path
import datetime, hashlib, json, zipfile

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
OUT=A/'feat335-acquisition-map-111'
assert not OUT.exists(), 'One-shot output already exists'
checks=[]; sources={}; objects={}
def ser(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def bind(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ck(n,v):
    checks.append({'name':n,'passed':bool(v)})
    assert v,n
def add(key,p,expected=None):
    p=Path(p);b=bind(p)
    if expected:ck('Exact source '+key,b['bytes']==expected['bytes'] and b['sha256']==expected['sha256'])
    sources[key]={'key':key,'file':'sources/'+key+p.suffix,'original':b}
    objects[key]=json.loads(p.read_bytes()) if p.suffix=='.json' else p.read_text(encoding='utf-8-sig')
    return objects[key]
def ref(k,p=''):return {'document':k,'pointer':p}
def ptr(o,p):
    for t in p.split('/')[1:]:
        t=t.replace('~1','/').replace('~0','~');o=o[int(t)] if isinstance(o,list) else o[t]
    return o
def result_refs(k,predicate):
    return [ref(k,'/results/'+str(i)) for i,r in enumerate(objects[k]['results']) if predicate(r['name'])]

cp=add('checkpoint109',A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_109.json')
protected=cp['canonicalHelperBaselinesUnchanged']+[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry']]
for b in protected:
    v=bind(G/b['path']);ck('Protected '+b['path'],v['bytes']==b['bytes'] and v['sha256']==b['sha256'])
contract=add('requirements107',A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json')
gate=next(x for x in contract['gates'] if x['id']=='FXC-05')
assembly=add('current_acquisition108',A/'feat335-planar-reference-108/after/acquisition_assembly.json',{'bytes':4813149,'sha256':'3b9d631dadf455fabab11679f3d33e16664e431a55abe2898a45ae4807e65a48'})
candidate=add('current_candidate108',A/'feat335-planar-reference-108/after/data/director/feat_candidates/exact_01/candidate.json',{'bytes':3697319,'sha256':'e4e106a4a3f9cc8bd40b378ccddc53bbf146070504136f8e1b0abd6ed14a6590'})
allowances=add('current_allowances106',A/'feat335-acquisition-106/allowance_descriptors.json',{'bytes':1722813,'sha256':'54ff173a090c88bbf2c671ccb0e0f807fc62f89a7ce972a3b0fbc10089681f73'})
ar=add('acquisition_report106',A/'feat335-acquisition-106/EVIDENCE_REPORT.json')
historykeys=['providers','physical_profiles','immutable_capture','numeric_prerequisites','shared_paid','shared_existing','deferred_descriptors','deferred_state','snapshot_descriptors','snapshot_state','historical_allowances','conditional_wrappers','cadence_corrections','flora_corrections','paid_history']
ck('Exactly fifteen historical files',len(ar['historicalEvidenceFiles'])==len(historykeys)==15)
for key,row in zip(historykeys,ar['historicalEvidenceFiles']):
    b=row['binding'];add(key,G/b['path'],b)
reviews=add('all_semantic_reviews106',A/'feat335-assembly-106/ALL_CASE_REVIEWS.json')
fx3=add('conflict_map107',A/'FEAT335_FXC03_EXACT_MAPPING_107.json')
magic=add('magic_review102',A/'FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json')
heritage=add('heritage_review105',A/'FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json')
resolution=add('native_resolution85',A/'FEAT335_RESOLUTION_CASES_85.json')
shared=add('current_shared106',A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/shared_rules.json')
for name in ['mage','dragoon','warrior','wizard']:
    b=next(x for x in magic['sourceBindings'] if x['path'].endswith('/class_playtests/'+name+'.json'))
    obj=add('class_'+name,G/b['path'],b)
    ck('Complete genuine class dependency '+name,obj==magic['completeClassDependencies'][name])

entries={e['id']:(i,e) for i,e in enumerate(assembly['entries'])}
records={e['id']:(i,e) for i,e in enumerate(candidate['records'])}
unchanged={e['id']:(i,e) for i,e in enumerate(candidate['unchangedReviewedFeats'])}
originals={e['id']:e for e in candidate['original335Registry']}
num=objects['numeric_prerequisites'];cov={e['id']:(i,e) for i,e in enumerate(num['coverage'])};other={e['id']:(i,e) for i,e in enumerate(num['remaining'])}
al={e['id']:(i,e) for i,e in enumerate(allowances['entries'])}
ck('All335 identities preserved',len(entries)==335 and set(entries)==set(originals)==set(records)|set(unchanged))
ck('209 numeric plus126 credential identities partition all335',len(cov)==209 and len(other)==126 and not(set(cov)&set(other)) and set(cov)|set(other)==set(entries))
ck('Complete numeric evidence retained',len(num['cases'])==1678 and len(num['actors'])==416)
ck('All177 current allowance descriptors retained',len(al)==177)
ck('All660 ordinary and28 additional full semantic reviews retained',len(reviews['ordinary'])==660 and len(reviews['additional'])==28)
semantic={fid:[] for fid in entries}
for group in ['ordinary','additional']:
    for i,r in enumerate(reviews[group]):
        fid=r['position']['featId'];semantic[fid].append({'document':'all_semantic_reviews106','pointer':'/'+group+'/'+str(i),'caseId':r['position']['id']})
indexed=[]
for fid,(i,e) in entries.items():
    c=e['currentCompleteContract'];r=(records.get(fid) or unchanged[fid])[1]
    ck('Full original equality '+fid,c['originalObject']==originals[fid]==r['sourceObject'])
    ck('Current operative procedure equality '+fid,c['completeOperativeProcedure']==r['operationalRules']==e['reviewedAcquisitionDescriptor']['completeControllingOperativeProcedure'])
    ck('Printed prerequisite exact '+fid,c['printedPrerequisitePresent']==('prerequisite' in originals[fid]) and c['printedPrerequisite']==originals[fid].get('prerequisite'))
    ck('Paid choice separate from predicate and use '+fid,c['actualClassScheduleRequired'] is True and c['candidateSelectionEnabled'] is False and c['acquisitionDoesNotGrantUseWithoutOngoingPredicates'] is True and bool(c['additionalUniversalAcquisitionGate']))
    if fid in other: ck('Other credential normalized requirement exact '+fid,c['requirements']==other[fid][1]['requirements'])
    if fid in cov:ck('Numeric printed prerequisite exact '+fid,c['printedPrerequisite']==cov[fid][1]['printedPrerequisite'])
    row={'id':fid,'completeCurrentAcquisition':ref('current_acquisition108','/entries/'+str(i)),
         'completeCurrentFeat':ref('current_candidate108',('/records/' if fid in records else '/unchangedReviewedFeats/')+str((records.get(fid) or unchanged[fid])[0])),
         'predicateEvidence':ref('numeric_prerequisites',('/coverage/' if fid in cov else '/remaining/')+str((cov.get(fid) or other[fid])[0])),
         'predicateEvidenceMeaning':'Historical numeric boundary coverage; complete acquisition explicitly false.' if fid in cov else 'Source-dependent prerequisite: actual credential/world receipt remains required; normalized AST alone does not authenticate it.',
         'completeSemanticReviews':semantic[fid], 'finiteGroups':list(e['finiteGroupEvidence']),
         'specializedCurrentEvidence':e['specializedCurrentEvidence'], 'fullActorExecuted':False}
    if fid in al:row['currentAllowance']=ref('current_allowances106','/entries/'+str(al[fid][0]))
    indexed.append(row)

areas=[]
def area(title,meaning,fids,refs):
    for fid in fids:ck(title+' current identity '+fid,fid in entries)
    for rr in refs:ptr(objects[rr['document']],rr['pointer'])
    areas.append({'requirementArea':title,'meaning':meaning,'currentAcquisitionIds':fids,'completeEvidence':refs,'scope':'SOURCE_QUALIFIED_AUTHORED_EVIDENCE_MAPPING_NOT_RUNTIME_OR_GATE_APPROVAL'})

area('All printed prerequisites','All335 exact printed predicates/current procedures are linked individually.209 numeric-only identities have1678 retained boundaries;126 require independent real credentials/context. Current full finite-group evidence is included without turning conditional receipts into campaign facts.',list(entries),[ref('numeric_prerequisites'),ref('providers'),ref('physical_profiles'),ref('conditional_wrappers')])
repeatids=[fid for fid,(_,e) in entries.items() if e['currentCompleteContract']['repeats'].get('policy')!='nonrepeatable']
area('Repeatability and one paid opportunity','Keep one earned grant identity, no double payment, no nonrepeatable reacquisition, exact different-save/weapon/armor/PureASI boundaries and curriculum family conflicts.',repeatids,result_refs('paid_history',lambda n:any(w in n for w in ['reacquire','opportunity','PureASI','Resilient','weapon Focus','weapon choices','curriculum','genericWizard','namedWizard','tier','Nonrepeatable'])))
training=['athleticProdigy','charismatic','diplomat','naturalist','acrobatic','ranger_training']
trrefs=result_refs('paid_history',lambda n:any(n.startswith(fid+' ') for fid in training) or n=='Two skill snapshots evaluated independently')
ck('Six complete fixed training groups retained',len(training)==6 and len(trrefs)==91)
area('Six fixed training branches','Snapshot actual proficiency per exact skill independently at acquisition. No retroactive branch promotion, reacquisition change, independent proficiency duplication or4PB Expertise.',training,trrefs+[ref('snapshot_state'),ref('snapshot_descriptors')])
legacy=[fid for fid,(_,e) in entries.items() if e['currentCompleteContract']['requiresLegacyOrContextReceiptWithoutCreatingIt']]
area('Actual legacy and context credentials','Full18 source-dependent rows retain literal lineage/established exposure/worship/rage/Spellcraft receipts. No silent ancestry or Arcana alias, no free deity/plane/class grant. Conditional wrapper evidence does not authorize absent source facts.',legacy,[ref('conditional_wrappers'),ref('providers'),ref('heritage_review105','/completeHeritageSourceMatches')])
ck('Eight prior reviewed identities exact',set(unchanged)=={'chef','empowered_summoning','field_medic','inspiring_leader','blood_ritual','lifeleech','necrotic_affinity','soul_cage'})
area('Eight unchanged reviewed records','Full reviewed envelopes and original identities remain exact; full acquisition still needs its real source predicates and paid opportunity.',list(unchanged),result_refs('paid_history',lambda n:n.endswith('reviewed envelope untouched'))+[ref('shared_paid'),ref('shared_existing')])
pairs=fx3['twelveWarriorCounterparts'];pids=[]
for p in pairs:
    fid=p['completePreservedPair']['featId'];pids.append(fid);c=entries[fid][1]['currentCompleteContract']
    ck('Warrior shared paid alias '+fid,c['sharedPaidIdentity']['samePaidIdentity'] is True and c['sharedPaidIdentity']['classCardId']==p['currentClassCard']['id'])
    ck('Warrior current feat equals settled conflict mapping '+fid,c['completeOperativeProcedure']==p['currentFeatProcedure'])
ck('Twelve distinct shared Warrior paid identities',len(set(pids))==12)
area('Twelve shared Warrior paid identities','The registry feat and exact class counterpart share one paid identity; similarly named unmapped cards do not alias. Current feat procedure and current class counterpart are preserved in full.',pids,[ref('conflict_map107','/twelveWarriorCounterparts')]+result_refs('paid_history',lambda n:any(n.startswith(fid+' ') for fid in pids) or n.startswith('Exactly12') or 'similarly named' in n or 'Unmapped actual' in n))
area('Equipped versus active mutation predicates','Acquisition uses actual unlocked slots/tier/equipped predicates. Activation, serum, Strain, active limits and real event gates remain use conditions. Warrior8 has2slots; Warrior13 may equip3 but3active still needs an explicit exception. No dormant-to-active inference.',pids,[ref('conflict_map107','/currentWarriorEngine'),ref('heritage_review105','/completeCurrentWarriorEngine'),ref('heritage_review105','/completeWarriorMutationCards'),ref('heritage_review105','/numericAndStateCalculations/20'),ref('heritage_review105','/additionalBoundaryReviews/2')])
area('Genuine class schedules and paid milestones','Total level is not each class level. Oracle12 does not invent ASI12; actual14 may qualify. Soldier3/Mage1 creates no class4choice. Banked actual opportunities keep their source identity.',[],result_refs('paid_history',lambda n:any(w in n for w in ['schedule','Oracle','Soldier3','earned grant','prerequisite alone','Actual choice','Rejected unmet','One opportunity']))+[ref('class_mage'),ref('class_dragoon'),ref('class_warrior'),ref('class_wizard')])
capcalc=next(i for i,x in enumerate(magic['numericAndStateCalculations']) if x['id']=='MX102-N24')
fa16=next(i for i,x in enumerate(reviews['additional']) if x['position']['id']=='FA-16')
mage=objects['class_mage']['rpByClassLevel'];dragoon=objects['class_dragoon']['rpByClassLevel'];warrior=objects['class_warrior']['rpByClassLevel']
ck('Genuine table cells Mage3=8 Dragoon8=7 Warrior7=0',mage[2]==8 and dragoon[7]==7 and warrior[6]==0)
ck('Retained bounded capacity arithmetic exact',magic['numericAndStateCalculations'][capcalc]['calculatedResult']==[mage[2],max(0,mage[2]-7),dragoon[7],warrior[6],warrior[6]>=3])
area('Mage3 / Dragoon8 / Warrior7 actual capacities','Mage3max8/current7 has only1headroom; Dragoon8max7; Warrior7has0RP and cannot pay3RP Arcane Pulse. Mage3alone does not qualify for total-level10 Arcane Recall. This is a table/capacity boundary, not a fabricated multiclass acquisition.', ['arcane_recall','arcane_pulse'],[ref('magic_review102','/numericAndStateCalculations/'+str(capcalc)),ref('all_semantic_reviews106','/additional/'+str(fa16)),ref('class_mage','/rpByClassLevel'),ref('class_dragoon','/rpByClassLevel'),ref('class_warrior','/rpByClassLevel')])
growth=next(i for i,x in enumerate(resolution['cases']) if x['id']=='FR85-27')
area('Capacity growth does not heal or refill','Tough fixes twice acquisition-level snapshot; separate HP sources keep their own live/snapshot rules. MaxHP additions are not HP gains; suppression may clamp without damage. Real Mage3->4max8->10 keeps current3. PB reserve growth does not refill.', ['tough','tough_as_nails','durable','life_drinker'],[ref('snapshot_state','/histories/34'),ref('snapshot_state','/histories/35'),ref('native_resolution85','/cases/'+str(growth))]+result_refs('paid_history',lambda n:n in ['PB-capacity growth no refill','Explicit empty reserve remains empty on acquisition']))
area('Suppression and reacquisition preserve spent history','Lucky restores the original identity and remaining uses; debt-only rest is no refill, beneficial real rest is, and replay is no second reset. Full177 current descriptors preserve source-specific cadence; copy preparation-only policy controls the three later correction rows.', ['lucky'],result_refs('paid_history',lambda n:any(w in n for w in ['Suppression','Suppressed Lucky','Reacquisition','Debt-only','beneficial rest','Same rest','Replayed rest','Restoration keeps one']))+[ref('current_allowances106'),ref('deferred_state'),ref('shared_paid')])
area('Permanent curriculum, vision and source-state branches','Named/generic curriculum conflicts remain exact. Both vision branches stay fixed through independent source changes/suppression. Snapshot, provider and initial-state histories retain actual menus and bodies without granting a new one.', ['night_hunter','dark_affinity']+training,result_refs('paid_history',lambda n:any(w in n for w in ['vision','Existing60','fallback60','stronger actual base','independent base','original branch','Base branch','curriculum','genericWizard','namedWizard']))+[ref('snapshot_state'),ref('providers'),ref('physical_profiles'),ref('deferred_state')])

report={'id':'FEAT335-FXC05-EXACT-MAPPING-111','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'completeOriginalRequirement':gate['completeOriginalRequirement'],'scope':'Complete named acquisition/capacity source and historical-evidence join for review. No historical program rerun, invented campaign receipt, source mutation or runtime execution.',
 'namedRequirementMap':areas,'all335CurrentAcquisitionIndex':indexed,
 'sourceMap':'SOURCE_MAP.json','classification':{'currentEntries':335,'numericPredicateIdentities':209,'otherCredentialDependentIdentities':126,'retainedNumericBoundaryCases':1678,'retainedSyntheticProjections':416,'fixedTrainingBranches':6,'legacyOrContextRows':len(legacy),'unchangedReviewedIds':8,'sharedWarriorPaidIdentities':12,'currentAllowanceDescriptors':177},
 'historicalQualification':'All original reports are included in full, including their remaining-scope/false-full-acquisition fields. Historical counts are not fresh executions. Current full operative procedures control over stale historical mirrors. Numeric-only boundaries do not establish independently legal complete characters.',
 'remaining':['GPT exact named FXC05 authored-evidence review remains pending; this mapping cannot approve itself.','Actual credential authentication, complete legal character construction, physical/world providers, persistence and runtime integration remain their separate gates.','FXC04 full supplement lifecycle and complete parent335 exact submission remain open.','No parent335/canonical/human/balance/whole-game/cosmology/release approval.'],
 'passed':len(checks),'failed':0,'checks':checks,'all335FullAcquisitionsExecuted':False,'historicalProgramsRerun':False,'runtimeExecuted':False,'canonicalApplied':False,'parent335Accepted':False,'actuallySentToGpt':False,'sourceInformationDeleted':False}
for rr in sources.values():write(OUT/rr['file'],Path(rr['original']['path']).read_bytes())
write(OUT/'SOURCE_MAP.json',ser(list(sources.values())))
write(OUT/'FXC05.json',ser(report))
readme='''# Feat335 acquisition/capacity evidence,111

FXC05.json maps twelve named acquisition/capacity areas to complete supplied source objects and retained histories. Every one of335 current acquisition entries has its exact printed prerequisite, current complete procedure, numeric-or-credential evidence and applicable complete semantic review links. SOURCE_MAP.json binds each supplied full file by SHA256 and length.

Current Planar108 acquisition/candidate and current ACQ106177 allowance descriptors control. Earlier reports preserve historical procedures/status without pretending those are current. Nothing in this package creates actual campaign credentials or turns source-qualified examples into full-character/runtime tests. Mage3 capacity arithmetic does not supply Arcane Recall's total-level10 prerequisite. Mutation equipment and active-state predicates are distinct.

No supplied program is required or authorized to run. Inspect the JSON/text as data. No historical successful validator was rerun. Current owner-reserved canonical files remain unchanged. Parent335 and the named gate remain unaccepted pending exact GPT review.
'''
write(OUT/'README.md',readme.encode())
archive=OUT/'DD_Feat335_Acquisition_Evidence_111.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file() and p!=archive:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
receipt={'id':'FEAT335-FXC05-RECEIPT-111','archive':bind(archive),'report':bind(OUT/'FXC05.json'),'sourceMap':bind(OUT/'SOURCE_MAP.json'),'passed':len(checks),'failed':0,'namedAreas':len(areas),'classification':report['classification'],'actuallySentToGpt':False,'parent335Accepted':False,'canonicalApplied':False,'runtimeExecuted':False}
write(A/'FEAT335_FXC05_EXACT_MAPPING_RECEIPT_111.json',ser(receipt))
write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps(receipt,ensure_ascii=False))
