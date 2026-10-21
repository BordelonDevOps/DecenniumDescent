"""Data-only FXC09 source/evidence join. No supplied code imports or historical reruns."""
from pathlib import Path
import datetime,hashlib,json,zipfile

A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
OUT=A/'feat335-spell-state-110-v3';OUT.mkdir(exist_ok=False)
P=A/'feat335-planar-reference-108/after/data/director/feat_candidates/exact_01/candidate.json'
S=A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/shared_rules.json'
U=A/'feat335-assembly-106/after/data/director/feat_candidates/exact_01/supplements.json'
D=A/'feat335-planar-reference-108/after/data/public/feat_candidates/exact_01/spell_dependencies.json'
R=A/'feat335-assembly-106/ALL_CASE_REVIEWS.json'
C=A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md'
checks=[];source_map=[];documents={}
def h(b):return hashlib.sha256(b).hexdigest()
def ser(x):return (json.dumps(x,ensure_ascii=False,indent=2)+chr(10)).encode()
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':h(b)}
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def retain(key,p,expected=None):
 b=p.read_bytes()
 if expected:ck('Exact known source '+key,h(b)==expected)
 fn='evidence/'+str(len(source_map)+1).zfill(2)+'.json'
 write(OUT/fn,b);source_map.append({'key':key,'file':fn,'original':bind(p)})
 documents[key]=json.loads(b)
 return documents[key]
def retain_member(key,folder,name):
 manifest=json.loads((A/folder/'MANIFEST.json').read_bytes());entry=next(x for x in manifest['files'] if x['path']==name)
 p=A/folder/name;ck('Bound member size '+key,p.stat().st_size==entry['bytes'])
 return retain(key,p,entry['sha256'])

candidate=json.loads(P.read_bytes());shared=json.loads(S.read_bytes());supp=json.loads(U.read_bytes());deps=json.loads(D.read_bytes());reviews=json.loads(R.read_bytes())
feat={x['id']:(i,x) for i,x in enumerate(candidate['records'])};rules={x['id']:(i,x) for i,x in enumerate(shared['rules'])}
cohort_sources={
 'magic100':('FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json','acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2'),
 'magic102':('FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json','17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b'),
 'magic103':('FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json','6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4'),
 'magic104':('FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json','d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92')}
for key,(file,sha) in cohort_sources.items():retain(key,A/file,sha)
retain('copyComponents',A/'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json','de46ed72a4f473665c972fb71d60a7af3ea83b3681c4d27c2d0656a54d651ac8')
retain('copyCapture',A/'FEAT335_COPY_CAPTURE_CHECK.json','5db4f01e6aa4d91203aae120c6cc6b6a6c3e2b21c5f8d86c2d5ed5a24260548e')
for key,file in [('readyPolicy','POLICY_SELECTION.json'),('readyCases','CASE_DISPOSITIONS.json'),('readySupersession','SUPERSESSION_REGISTER.json'),('readyOriginals','ORIGINAL_AND_REVISED_EXAMPLES.json'),('readyLimits','RETAINED_LIMITATIONS.json')]:retain_member(key,'copy-ready-preparation-only-part5-successor-01',file)
for key,file in [('copyDispositions','CASE_DISPOSITIONS.json'),('copyFindings','FINDINGS.json'),('copyProfiles','PROFILE_DISPOSITIONS.json'),('copyTestClassification','TEST_CLASSIFICATION.json')]:retain_member(key,'copied-feat-integration-part5-return-01',file)
for key,file in [('supplementCases','CASE_DISPOSITIONS.json'),('supplementFindings','FINDING_DISPOSITIONS.json'),('supplementLimits','RETAINED_LIMITATIONS.json'),('supplementTestClassification','TEST_CLASSIFICATION.json')]:retain_member(key,'copied-feat-integration-part5-supplement-02',file)
retain('readyLocalPreflight',A/'COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json','f7a4ea7a61758a969f261f932eaea7bfc594743fcd2fad0642d6258a1511f779')
retain('timeWorkMap',A/'FEAT335_FXC06_EXACT_MAPPING_108.json')
retain('dependencyComparison107',A/'feat335-spell-dependencies-107/AUDIT_REPORT.json','a2a24ecf03ef658c604d4c7cf9819e567c4a61ecc34ce86866dc4a9af23cb71a')
retain('currentPlanarReference',A/'feat335-planar-reference-108/REPORT.json','8d27e96b877ddb0f15c52587eef9007af7aedf597b4c211a83bfb723c8c4e01c')
cp=supp['groups'][6]['completeAuthoringValue']['copyProfileContract'];policy=documents['readyPolicy']
ck('Current policy exact complete text',cp['readyAllowanceDecision']['id']=='COPY-READY-ALLOWANCE-02' and cp['readyAllowanceDecision']['operativeWording']==policy['completeOperativeWording'])
ck('Current seven concentration tags',[(x['id'],x['concentrationRequired']) for x in cp['profiles']]==[('strike',False),('burst',False),('mend',False),('ward',True),('hindrance',True),('boon',True),('step',False)])
ck('Forty-two current policy cases retained',len(documents['readyCases']['completeCases'])==42)
ck('Original and selected implementation cases retained',documents['readyOriginals']['completePriorImplementationCases']['count']==documents['readyOriginals']['completeSelectedImplementationCases']['count'])
ck('Sixty-eight old complete histories have explicit dispositions',documents['copyDispositions']['historyCount']==len(documents['copyDispositions']['histories'])==68)
ck('Seven old Ready histories remain conditional history',len(documents['copyDispositions']['readyLifecycleHistories'])==7)
ck('Thirteen original source acceptance cases retained',len(documents['copyDispositions']['sourceAcceptanceExamples'])==13)
ck('Seven correction groups retained',len(documents['copyFindings']['findings'])+len(documents['supplementFindings']['findings'])==7)
ck('Five supplement complete before/after cases retained',len(documents['supplementCases']['cases'])==5)
ck('Source/capture histories preserved',len(documents['copyComponents']['histories'])==35 and len(documents['copyCapture']['histories'])==31)
ck('Current preflight751checks remains inherited evidence',documents['readyLocalPreflight']['checkCount']==751 and documents['readyLocalPreflight']['failures']==0)

# These are source joins, not a new interpreter or rerun of their calculations.
areas=[
 ('Paid feat copies, secondary echoes and actual class release',['arcane_adaptation','eldritch_echo','mimicry','echo_spell','spell_reflection','spell_deflection','mirror_cast','twin_cast'],['FS-07','FS-08','FS-09'],['copyDispositions','copyProfiles','copyCapture','readyPolicy'],'Paid feat cast uses its independent canonical-source family and scoped strain. Secondary repeated/redirected payloads and actual separately acquired Mirrorsage class releases retain their own histories, budgets and exclusions.'),
 ('Actual components and interruption',['battleMage','silent_casting','still_casting','flash_cast','war_caster','mage_slayer'],['FS-05','FS-08','FS-09'],['copyDispositions','readyCases'],'Occupied hands versus actual incapacity; focus/material capability remains. Validate/pay preparation before its one interruption window. An already committed countered cast retains genuine costs.'),
 ('True rank prices and independent Silent/Still costs',['heighten_spell','efficient_caster','silent_casting','still_casting','blood_magic','forbidden_pact','arcane_transfusion','metamagicAdept'],['FS-07','FS-09'],['magic100','magic102','magic103','magic104'],'Actual route/rank price and independently due costs remain separate from charges or HP funding. Silent V and Still S are separate paid choices, not universal component freedom.'),
 ('One concentration/Ready slot and preparation-only allowance',['arcane_adaptation','eldritch_echo','mimicry','spellweave','arcane_calculus','concentrated_will'],['FS-08','FS-09'],['readyPolicy','readyCases','readyOriginals','readySupersession','copyFindings','supplementFindings'],'Forty-two current full policy cases include same/later round, genuinely available competing use, no extra Action, actual Reaction, exact original expiry, one paid hold and final profile burden. Historic two-round debits are superseded only where explicitly named.'),
 ('Bounded ritual learning and written copying',['spell_scribe','ritual_caster'],['FS-02','FS-09','FS-14'],['timeWorkMap','magic100'],'Selected FT84 written-copy/material predicate, actual texts/teacher, rank cap, complete labor/phases and preserved ordinary no-discount case; no free spell, language, book, formula or access.'),
 ('Actual ritual execution and helpers',['ritual_caster','quick_ritualist','ritual_channeler'],['FS-09','FS-14'],['timeWorkMap','magic100','magic103'],'Keep base labor and actual waiting, non-worsening added-time floor, one group25percent reduction, complete helper attendance and one physical lead distinct from assistants.'),
 ('Quickened Thought on any later actual turn',['quickened_thought'],['FS-06','FS-08','FS-10'],['magic104'],'One prepared cantrip may release between completed events during a later actual turn, including another actor turn; preserve held concentration, Ready capacity and actual next-START deadline. No interrupt or second casting transaction.'),
 ('Native spell endpoints and full standalone payloads',['illusionist_s_trick','lingering_magic','temporal_flux','shadow_touched','spellweave','telekinetic','familiar_bond','ritual_caster'],['FS-08','FS-09'],['magic100','magic102','magic103','dependencyComparison107','currentPlanarReference'],'Use complete currently accepted ordinary cards, including LRX envelopes. No new save for Haste, no revival of ended Silent Image, no permanent familiar or ignored Invisibility ending event.'),
 ('Plant body and attached command phases',['conjure_flora','verdant_bond','trapcasting'],['FS-06','FS-10','FS-15'],['magic104'],'Fixed creation source/actual body, finite lifespan and separately created second plant; actual attached phase and paid command may survive owner death where the exact source says so. No extra creature phase or body duplication.'),
 ('Trapcasting conserved shared offensive action',['trapcasting','conjure_flora'],['FS-10','FS-15'],['magic104'],'Exact first eligible trap trigger spends the same round offense even when saved; Burst consumes one real plant before payload. Existing command and source-specific automatic-trigger exception do not supply a second offense.'),
 ('No duplicate resource, production, reflection or capture chains',['echo_spell','spell_reflection','spell_deflection','twin_cast','arcane_recall','arcaneResonance','energy_sink','mana_burn','hemocraft','curse_channeling','voltyros_pact'],['FS-03','FS-07','FS-08'],['copyComponents','copyCapture','copyDispositions','copyFindings','supplementFindings','magic100','magic102','magic103','magic104'],'Preserve original paid/root identity and no-resource/no-recapture restrictions. Secondary copied/redirected damage cannot create another cast, refund, production, capture, attack or reward. Real separately paid native exceptions remain explicit.'),
 ('Source-specific exceptions and unresolved implementation edges',['arcane_adaptation','eldritch_echo','mimicry','hemocraft','forbidden_pact','wounding_magic'],['FS-07','FS-08'],['copyDispositions','supplementCases','supplementFindings','supplementLimits','readyLimits'],'Inactive next-healing records do not block Mend; active source-owned consumption remains unimplemented. Shared expiry instructions must be preserved/forwarded, but downstream condition choice is not executed by the copy helper. State sacrifice and real damage costs are distinct.'),
 ('Higher drafts remain comparisons and wrappers remain unavailable',['astral_projection','planar_binding'],['FS-01','FS-09','FS-16'],['dependencyComparison107','currentPlanarReference'],'The original contract71 comparison drafts do not become payload authority. Current ordinary sources are independently bound; wrapper nulls and disabled flags persist, including the agreed Planar reference update. No71-draft approval is claimed.')]

selected=set();selectedrules=set();named=[]
for title,ids,rids,keys,meaning in areas:
 selected.update(ids);selectedrules.update(rids)
 ordinary=[{'id':x['position']['id'],'featId':x['position']['featId'],'pointer':'/ordinary/'+str(i)} for i,x in enumerate(reviews['ordinary']) if x['position']['featId'] in ids]
 additional=[{'id':x['position']['id'],'featId':x['position']['featId'],'pointer':'/additional/'+str(i)} for i,x in enumerate(reviews['additional']) if x['position']['featId'] in ids]
 calculations=[]
 for key in cohort_sources:
  for i,x in enumerate(documents[key]['numericAndStateCalculations']):
   caseids={r['id'] for r in ordinary+additional}
   if set(x['originalCaseIds']) & caseids:calculations.append({'document':key,'pointer':'/numericAndStateCalculations/'+str(i),'id':x['id'],'classification':'HISTORICAL_BOUNDED_REFERENCE_CALCULATION_NOT_RERUN'})
 ck('Named area has exact source/case evidence '+title,bool(ordinary or additional) and all(k in documents for k in keys))
 named.append({'requirementArea':title,'meaning':meaning,'currentFeatIds':ids,'currentSharedRuleIds':rids,'semanticCaseRefs':ordinary+additional,'historicalCalculationRefs':calculations,'completeEvidenceKeys':keys,'status':'EXACT_SOURCE_AND_CASE_EVIDENCE_MAPPED_PARENT_REVIEW_PENDING'})
joins=[]
for id in sorted(selected):
 index,record=feat[id];caseviews=[x for x in reviews['ordinary'] if x['position']['featId']==id]
 ck('Complete current record and case join '+id,len(caseviews)==len(record['workedCases']) and not record['selectionEnabled'] and not record['exactApproved'])
 joins.append({'binding':bind(P),'pointer':'/records/'+str(index),'completeCurrentRecord':record,'completeOrdinaryReviews':caseviews,'completeAdditionalReviews':[x for x in reviews['additional'] if x['position']['featId']==id]})
for id in ['astral_projection','planar_binding']:
 record=feat[id][1];ck('Unavailable null wrapper '+id,record['payloadOperational'] is None and not record['selectionEnabled'] and not record['exactApproved'] and not record['runtimeApproved'])
for id in ['arcane_adaptation','eldritch_echo','mimicry']:
 ck('Current selected policy in whole copy procedure '+id,policy['completeOperativeWording'] in feat[id][1]['operationalRules'])
native=[]
for id in ['silent-image','haste','invisibility','mage-hand','true-strike','find-familiar','arcane-ray','burning-hands','lifedraw','false-life','slow','shield','mist-step']:
 card=deps['spells'][id];ck('Full current native endpoint '+id,card['id']==id and bool(card['completeCurrentProcedureCard']) and card['grantsNoAccessByItself'])
 native.append({'binding':bind(D),'pointer':'/spells/'+id,'completeCurrentDependency':card})
contract=C.read_text(encoding='utf8').splitlines();heading=next(i for i,x in enumerate(contract) if x.startswith('## FXC-09 '));requirement=contract[heading+2]
record={'id':'FEAT335-FXC09-EXACT-MAPPING-110','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CURRENT_COMPLETE_RULE_CASE_AND_HISTORY_MAPPING_PARENT_VERDICT_PENDING','completeOriginalRequirement':requirement,'contract':bind(C),'namedRequirementMap':named,'currentFeatJoins':joins,'currentSharedRules':[{'binding':bind(S),'pointer':'/rules/'+str(rules[id][0]),'completeCurrentRule':rules[id][1]} for id in sorted(selectedrules)],'currentSupplement07':{'binding':bind(U),'pointer':'/groups/6','completeCurrentGroup':supp['groups'][6]},'completeCurrentNativeEndpoints':native,'semanticRegister':bind(R),'completeEvidenceFiles':source_map,'historicalStatusQualification':'All historical source snapshots, checks, findings and limits remain complete and unmodified. Supersession is solely the supplied exact later policy/corrections. Historical counts, unsent status and incomplete cohort frontiers are dated evidence, not current project status. No downloaded/project code or prior successful program executed.','currentEvidenceCounts':{'namedAreas':len(named),'currentFeatRecords':len(joins),'currentNativeEndpoints':len(native),'readyCases':42,'ordinaryCopyHistories':68,'originalReadyHistories':7,'originalSourceAcceptanceExamples':13,'originalComponentHistories':35,'originalCaptureHistories':31,'supplementCases':5,'scopedCopyFindings':7,'fullCohortCalculations':sum(len(documents[k]['numericAndStateCalculations']) for k in cohort_sources)},'retainedImplementationGaps':documents['readyLimits']['unimplemented'],'limits':['Actual acquisition, source completion, perception, meaningful hostility, body/geometry, materials/providers and real competing Action opportunities remain explicit source-qualified premises.','Current reference helper changes remain unapplied under owner reservation. Data/history matching cannot certify the native game, Ready persistence or full class Echo engine.','Inherited examples and semantic reviews distinguish described state from executed bounded calculations. This map performs source/data joins only.','The full335 exact verdict, other content/system catalogs, human gameplay, balance, publication, cosmology and final whole-game flow remain separate.'],'passed':len(checks),'failed':0,'checks':checks,'runtimeExecuted':False,'historicalProgramsRerun':False,'canonicalApplied':False,'parentExactGateAccepted':False,'wholeGameComplete':False}
write(OUT/'FXC09.json',ser(record));write(OUT/'SOURCE_MAP.json',ser(source_map));write(OUT/'REPRODUCTION_SCRIPT.py',Path(__file__).read_bytes())
manifest=[{'file':p.relative_to(OUT).as_posix(),**bind(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
write(OUT/'MANIFEST.json',ser({'id':'FEAT335-SPELL-STATE-110-MANIFEST','files':manifest,'warning':'Retained reproduction source is evidence only; do not rerun this successful one-shot script.'}))
archive=A/'DD_Feat335_Spell_State_Evidence_110.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for row in manifest:assert h(z.read(row['file']))==row['sha256']
receipt={'id':record['id'],'archive':bind(archive),'report':bind(OUT/'FXC09.json'),'counts':record['currentEvidenceCounts'],'passed':len(checks),'failed':0,'actuallySentToGpt':False,'canonicalApplied':False,'runtimeExecuted':False,'parentExactGateAccepted':False}
write(A/'FEAT335_FXC09_EXACT_MAPPING_RECEIPT_110.json',ser(receipt));write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps(receipt))
