from pathlib import Path
import json,hashlib,datetime
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';P=A/'feat335-assembly-106'
OUT=A/'FEAT335_FXC03_EXACT_MAPPING_107.json';assert not OUT.exists()
sources={};checks=[]
def load(p):
    b=p.read_bytes();sources[str(p)]=b;return json.loads(b.decode('utf-8-sig'))
def bind(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ck(n,r):checks.append({'name':n,'passed':bool(r)});assert r,n
def ptr(o,p):
    for k in p.strip('/').split('/') if p else []:o=o[int(k)] if isinstance(o,list) else o[k]
    return o
private=load(P/'after/data/director/feat_candidates/exact_01/candidate.json');public=load(P/'after/data/public/feat_candidates/exact_01/candidate.json')
by_private={x['id']:x for x in private['records']};by_public={x['id']:x for x in public['feats']}
shared=load(P/'after/data/public/feat_candidates/exact_01/shared_rules.json');by_shared={x['id']:x for x in shared['rules']}
conventions=load(P/'after/data/director/feat_candidates/exact_01/convention_dispositions.json')
fex=load(P/'after/data/director/feat_candidates/exact_01/fex_dispositions.json')
conflicts=load(P/'after/data/director/feat_candidates/exact_01/source_conflict_dispositions.json');by_conflict={x['id']:x for x in conflicts['conflicts']}
mx=load(R/'data/director/magic_extended_feat_operating_proposal_internal.json')
hm=load(R/'data/director/heritage_mutation_feat_operating_proposal_internal.json')
warrior=load(R/'data/public/class_playtests/warrior.json');class_cards={x['id']:x for x in warrior['cards']}
all_cases=load(P/'ALL_CASE_REVIEWS.json');cases=all_cases['ordinary']+all_cases['additional']
acq01=A/'FEAT327_ACQ_01_GPT_ADDENDUM.md';sources[str(acq01)]=acq01.read_bytes()
mapped_conventions=[]
for n,c in enumerate(conventions['entries']):
    source=G/c['sourcePath'];obj=load(source)
    ck('Original convention field exact '+str(n),ptr(obj,c['pointer'])==c['original'])
    decisions=[]
    for ident in c['controllingDecisions']:
        if ident=='FEAT327-ACQ-01':decisions.append({'id':ident,'completeText':sources[str(acq01)].decode('utf-8-sig'),'binding':bind(acq01)})
        else:decisions.append(by_shared[ident])
    mapped_conventions.append({'originalPosition':n,'completeDisposition':c,'currentCompleteControllers':decisions,'sourceBinding':bind(source),
        'qualification':'Original convention remains historical. Current full shared contract and exact per-feat exceptions control; no old future-conference label is reopened.'})
eight=[]
for n,source in enumerate(mx['descriptionEffectConflicts']):
    ident=source['featId'];d=by_conflict['CONFLICT-'+ident];r=by_private[ident]
    ck('Full explicit conflict retained '+ident,d['original']==source)
    for key in ['description','effect','legacyEffect']:ck('Original conflicting field '+ident+' '+key,r['sourceObject'][key]==source[key])
    ck('Full current conflict procedure mirror '+ident,r['operationalRules']==by_public[ident]['operationalRules'])
    evidence=[c for c in cases if c['position']['featId']==ident]
    ck('Complete ordinary case positions '+ident,len([c for c in evidence if not c['position']['id'].startswith('FA-')])==2)
    eight.append({'sourcePointer':'/descriptionEffectConflicts/'+str(n),'completeOriginalConflict':source,'completeDisposition':d,
        'exactCurrentFeatId':ident,'currentProcedure':r['operationalRules'],'preservedSourceDecision':r['sourceDirection'],
        'completeAuthoredCaseReviews':evidence,'classification':'Original competing fields preserved; current selected procedure and exact case reviews supplied, no new mechanic.'})
pairs=[]
for n,source in enumerate(hm['originalWarriorCounterpartPairs']):
    ident=source['featId'];r=by_private[ident];card=class_cards[source['completeClassCounterpart']['id']]
    ck('Complete source feat identity '+ident,source['sourceObject']==r['sourceObject'])
    ck('Complete current Warrior card unchanged '+ident,card==source['completeClassCounterpart'])
    ck('Current Warrior/feat operating mirror '+ident,r['operationalRules']==by_public[ident]['operationalRules'])
    evidence=[c for c in cases if c['position']['featId']==ident]
    ck('Full two ordinary Warrior counterpart cases '+ident,len([c for c in evidence if not c['position']['id'].startswith('FA-')])==2)
    pairs.append({'sourcePointer':'/originalWarriorCounterpartPairs/'+str(n),'completePreservedPair':source,
        'currentClassCard':card,'currentFeatProcedure':r['operationalRules'],'preservedSourceDecision':r['sourceDirection'],
        'completeAuthoredCaseReviews':evidence,'sharedAuthority':[by_shared['FS-01'],by_shared['FS-02'],by_shared['FS-03'],by_shared['FS-04']],
        'qualification':'One paid source-row identity and each exact equipped/active predicate remain controlled by the current full rules. The original pending relationship label is historical, not permission for a duplicate grant.'})
ck('All91 conventions mapped',len(mapped_conventions)==91)
ck('All15 FEX resolutions preserved',len(fex['issues'])==15 and len({x['id'] for x in fex['issues']})==15)
ck('All8 explicit extended conflicts mapped',len(eight)==8)
ck('All12 Warrior counterpart pairs mapped',len(pairs)==12)
ck('Current Warrior ACQ02 not overwritten','ACQ' in str(warrior['engine'][17]))
for path,b in sources.items():ck('Bound source unchanged '+path,Path(path).read_bytes()==b)
report={'id':'FEAT335-FXC03-EXACT-FIELD-MAP-107','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Complete source/current-controller/case-evidence join for91 conventions,15FEX,8 explicit competing-field records and12Warrior pairs. Reuses completed semantic reviews; no historical program rerun.',
    'sourceBindings':[bind(Path(p)) for p in sources], 'completeConventions':mapped_conventions,'completeFex':fex,
    'complete159ConflictRegister':conflicts,'eightExplicitConflicts':eight,'twelveWarriorCounterparts':pairs,
    'currentWarriorEngine':warrior['engine'],'currentFlatAndPercentFamilies':[by_shared['FS-03'],by_shared['FS-04']],
    'supersedesOnly':'The missing explicit field map for FXC03 in FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json is now supplied. This does not award exact parent acceptance or close other gates.',
    'passed':len(checks),'failed':0,'checks':checks,'localFXC03EvidenceJoinComplete':True,
    'canonicalApplied':False,'parent335Accepted':False,'newMechanicsAuthored':False,'runtimeExecuted':False,'historicalValidatorsRerun':False}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'report':bind(OUT),'passed':len(checks),'failed':0,'conventions':91,'FEX':15,'explicitConflicts':8,'WarriorPairs':12}))
