"""Join existing accepted finite work evidence to FXC06; rerun no old program."""
from pathlib import Path
import hashlib,json,datetime

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
P=A/'feat335-work-compositions84-part5-return-01';F=A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/candidate.json'
OUT=A/'FEAT335_FXC06_EXACT_MAPPING_108.json'
assert not OUT.exists()
def j(p):return json.loads(p.read_bytes())
def bind(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ref(p,ptr):return {'binding':bind(p),'pointer':ptr}
checks=[]
def ck(n,v):
    checks.append({'name':n,'passed':bool(v)})
    assert v,n
gate=next(x for x in j(A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json')['gates'] if x['id']=='FXC-06')
time=A/'FEAT335_TIME_PROVISIONS_CASES_83.json';work=A/'FEAT335_WORK_COMPOSITIONS_84.json'
old={'DD_Feat335_Work_Compositions_84.zip':(work,j(work)), 'DD_Feat335_Time_Provisions_Cases_83.zip':(time,j(time))}
disps=j(P/'ORIGINAL_CASE_DISPOSITIONS.json')['cases'];new=j(P/'CASEBOOK.json')['cases'];review=j(A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json')
ck('Exact inherited scoped acceptance',review['status']=='ACCEPTED_SCOPED_AUTHORED_FOLLOWTHROUGH_UNAPPLIED_PARENT335_NOT_ACCEPTED' and review['review']['completeCasesRead']==57)
rows=[]
for i,d in enumerate(disps):
    file,doc=old[d['archive']];ix=int(d['pointer'].split('/')[-1]);c=doc['cases'][ix]
    ck('Exact original '+d['id'],c==d['completeOriginalCase'] and c['id']==d['id'])
    ck('Existing disposition retains qualified evidence '+d['id'],d['disposition'] in {'RETAIN_SUPPLIED_CONDITIONAL_SPECIFICATION_UNCHANGED','RETAIN_SOURCE_SCOPED_CONDITIONAL_EVIDENCE_UNCHANGED'} and d['historicalScriptExecutedHere'] is False)
    rows.append({'id':d['id'],'original':ref(file,d['pointer']),'existingDisposition':ref(P/'ORIGINAL_CASE_DISPOSITIONS.json','/cases/'+str(i)),'completeOriginalCase':c,'completeDisposition':d,'currentMeaning':'Retained at the exact disclosed predicate/fixture scope. Not rerun, not generalized to a newly authorized process, not a new engine result.'})
ck('All106 original positions exactly once',len(rows)==106 and len({(r['original']['binding']['path'],r['original']['pointer']) for r in rows})==106 and sum(r['original']['binding']['path']==str(work) for r in rows)==78)
current=j(F)['records'];procedures=[]
for i,r in enumerate(j(P/'SELECTED_PROCEDURES.json')['procedures']):
    ix=next(i for i,x in enumerate(current) if x['id']==r['id']);c=current[ix]
    ck('Current adopted FT84 procedure '+r['id'],c['operationalRules']==r['after'])
    procedures.append({'id':r['id'],'selection':ref(P/'SELECTED_PROCEDURES.json','/procedures/'+str(i)),'current':ref(F,'/records/'+str(ix)),'completeOriginalAndSelectedProcedure':r,'currentOperationalRules':c['operationalRules']})
groups=[
 ('Foraging and actual provisioning',['FP83-01','FP83-02','FP83-03','FP83-04','FP83-05','FP83-06','FP83-07','FP83-08','FP83-19'],[], 'Actual active Watch, completed-use cadence, finite sites, separate person/animal needs, no missing oil/sundry conversion or invented Supply.'),
 ('Endurance, rest debt and cause counters',['FP83-09','FP83-10','FP83-11','FP83-12','FP83-13','FP83-14','FP83-15','FP83-16','FP83-17','FP83-18','FP83-20'],[], 'Separate food/water and sleep credits; debt deadline/later missed Watch/safe rest; old Strain and history preserved; suppression and unavailable cause credits; no third work Watch.'),
 ('Manufacturing and actual closed construction',['WC84-01','WC84-02','WC84-03','WC84-04','WC84-05'],['FT84-03-gadget','FT84-03-kit','FT84-03-category','FT84-03-recipe'], 'Old arithmetic assumes genuinely eligible creation. FT84-Q03 now resolves which named procedures qualify; no source case required numerical replacement.'),
 ('Research time, phase and exclusions',['WC84-06','WC84-07'],['FT84-02'], 'FT84-Q02 adds only the two named process clocks and real final remainder; actual exclusions/waits and work caps remain.'),
 ('Spell copying, written ritual learning and material bills',['WC84-08','WC84-09','WC84-10','WC84-11','WC84-12'],['FT84-01'], 'FT84-Q01 selects true complete written copying versus teaching; original mixed/unclassified bill arithmetic remains conditional; current six full procedures control.'),
 ('Ritual casting composition and true helpers',['WC84-13','WC84-14','WC84-15','WC84-16'],[], 'Real casting base/floor/non-worsening rule and actual distinct participating bodies; no extra helpers or learning/copying benefit inferred.'),
 ('Other explicit time compositions',['WC84-17','WC84-18','WC84-19'],[], 'Gossip active inquiry versus calendar appointments; specific armor/helper multiplication retains its own scope.'),
 ('Whole short rest repairs and long-job tails',['WC84-20','WC84-21','WC84-22','WC84-23','WC84-24','WC84-25','WC84-26','WC84-27','WC84-28','WC84-29'],['FT84-03-rest'], 'Whole eligible20/30-minute repairs versus31/480-minute jobs; actual completion, stock, remaining HP, source qualifications and replay protection.'),
]
mapped=[];coveredold=set();coverednew=set()
for name,prefixes,newprefixes,meaning in groups:
    ori=[r for r in rows if any(r['id'].startswith(p) for p in prefixes)]
    add=[(i,c) for i,c in enumerate(new) if any(c['id'].startswith(p) for p in newprefixes)]
    coveredold.update(r['id'] for r in ori);coverednew.update(c['id'] for _,c in add)
    mapped.append({'requirementArea':name,'meaning':meaning,'originalCases':[{'id':r['id'],**r['original'],'existingDisposition':r['existingDisposition']} for r in ori],'acceptedScopedNewCases':[{'id':c['id'],**ref(P/'CASEBOOK.json','/cases/'+str(i))} for i,c in add]})
ck('Every106 original case mapped to named FXC06 area',coveredold=={r['id'] for r in rows})
ck('Every57 scoped followthrough case mapped',coverednew=={c['id'] for c in new})
report={'id':'FEAT335-FXC06-EXACT-MAPPING-108','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'FINITE_SOURCE_AND_ACCEPTED_EVIDENCE_MAP_COMPLETE_PARENT_EXACT_VERDICT_PENDING','completeOriginalRequirement':gate['completeOriginalRequirement'],'gateContract':j(A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json')['contract'],'inheritedScopedAcceptance':ref(A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json',''),'completeInheritedReview':review['review'],'namedRequirementMap':mapped,'allOriginalCaseDispositions':rows,'completeCurrentSixProcedures':procedures,'fullThreeQuestionSelections':j(P/'QUESTION_DISPOSITIONS.json'),'full57AcceptedScopedCases':new,'supersessionFinding':{'historicalOriginalCases':106,'work':78,'timeProvision':28,'oldCasesNumericallyReplaced':0,'oldCaseProgramsRerun':0,'finding':'The actual already-reviewed ORIGINAL_CASE_DISPOSITIONS retains all106 at their exact qualified inputs. The three unselected interface questions are superseded by FT84-Q01/Q02/Q03 and six full procedures;57 new cases provide concrete followthrough. No old78 case is silently rerun, relabelled engine proof, or falsely claimed numerically superseded. This corrects the overly broad supersession task wording in the107 overview.'},'passed':len(checks),'failed':0,'checks':checks,'canonicalApplied':False,'parentExactGateAccepted':False,'runtimeExecuted':False,'wholeGameComplete':False,'limits':['This is an exact source/evidence join; accepted scoped semantic/calculation work is inherited from88, not newly performed.','Actual campaign credentials, stocks, access, safe work and world interruptions remain explicit premises; no new universal classifier or scheduler is implemented.','Other FXC gates and parent review remain separate.']}
with OUT.open('xb') as f:f.write((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'output':str(OUT),'passed':len(checks),'failed':0,'old106':len(rows),'new57':len(new),'numericallySupersededOldCases':0}))
