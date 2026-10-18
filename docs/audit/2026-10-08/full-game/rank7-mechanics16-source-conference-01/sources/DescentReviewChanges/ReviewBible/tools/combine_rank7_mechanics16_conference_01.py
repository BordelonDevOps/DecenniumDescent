"""Risk-tiered mixed16 source conference; preserves both earlier all-C staging packets."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

TIERS={
 'lightning-grave':('B','Finite conditional mark and trigger timing; damage pipeline inherited.'),
 'pyroclasm':('B','Initial burst plus persistent ground interaction; actual geometry and condition families reused.'),
 'frost-reaver':('B','Until-healed rider definition and cure predicate; existing slow/HP rules retained.'),
 'arcbolt-singularity':('A','One instantaneous finite multi-target damage operation; new local placement/radius/save parameters only.'),
 'delayed-blast-fireball':('B','Finite delayed charge and suppression lifecycle; no new casting/Ready/Null system.'),
 'prismatic-spray':('C','Seven missing native effects and selection semantics require a complete bounded authored table.'),
 'whirlwind':('B','Source-specific pull geometry and falling; ordinary damage and body interfaces inherited.'),
 'crown-of-stars':('B','Finite discharge record, action cadence and suppression; no autonomous companion permission.'),
 'mass-confusion':('B','Enemy-only area and local binding of the already accepted behavior/control interfaces.'),
 'dominate-greater-beast':('B','Actual creature classification/CR predicate and explicit binding of existing control procedures.'),
 'mindfog-field':('B','Finite zone, actual roll modifiers and exposure/stacking histories.'),
 'lasting-control':('C','A new duration-extension exception conflicts with concentration transition and control-clock limits.'),
 'power-word-pain':('B','Paid hiddenHP eligibility plus finite authored pain components; actual controls remain inherited.'),
 'project-image':('B','Two preserved school profiles, source-qualified sensing and nonphysical image lifecycle.'),
 'reverse-gravity':('C','Altered gravity for real creatures/objects needs explicit bounded motion/support/boundary rules.'),
 'symbol-of-stunning':('B','Finite armed source, trigger snapshot and hard-control admission; existing guard not redefined.')}

def main():
 root=A/'rank7-mechanics16-source-conference-01';out=R/'data/director/spell_review/rank7_mechanics_16_source_conference_01.json';check=A/'RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_CHECK.json';prep=A/'RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_PREPARATION.json';req=A/'RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_REQUEST.txt';archive=A/'DD_Rank7_Mechanics_16_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,req,archive]);checks=[];sources={};parents=[];records=[];questions=[];inherited=[];counterparts=[]
 def read(p):return json.loads(p.read_bytes())
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def bind(p):
  b=info(p)
  if b['path'] in sources:ck('Identical duplicated source '+b['path'],sources[b['path']]==b)
  sources[b['path']]=b;return b
 for stem in ['EVOCATION_RANK7_8','ENCHANTMENT_RANK7_8']:
  pp=A/f'{stem}_CONFERENCE_01_PREPARATION.json';p=read(pp);doc=read(G/p['candidate']['path'])
  for key in ['candidate','archive','manifest','check','request']:ck('Exact parent '+stem+' '+key,info(G/p[key]['path'])==p[key])
  parents.append({'preparation':bind(pp),'candidate':bind(G/p['candidate']['path']),'archivePreservedLocallyUnchanged':p['archive'],'check':bind(G/p['check']['path']),'scope':'Unsent parent packet and original all-C staging labels remain historical. Current per-spell risk assessment below replaces only those labels, not source data or questions.'})
  for b in doc['sourceBindings']:ck('Current source exact '+b['path'],bind(G/b['path'])==b)
  for rec in doc['records']:
   r=deepcopy(rec);tier,why=TIERS[r['spellId']];r['priorRiskTierUnchangedInParent']=r['riskTier'];r['riskTier']=tier;r['riskReason']=why;records.append(r)
  for q in doc['questions']:
   if q['id'] in ['EV7-Q16','EN7-Q19']:
    inherited.append({'formerQuestionUnchanged':deepcopy(q),'currentDisposition':'INHERITED_SOURCE_ACCESS_AND_WORKFLOW_REQUIREMENT_NOT_AN_OPEN_DESIGN_FORK','reason':'Exact per-class access/pricing, current class engines, ordinary strain/cast order and full-case standards already govern. No request to reopen them. Future fixtures must actually satisfy them.'})
   else:questions.append(deepcopy(q))
  for e in doc['currentAcceptedInterfaceComparisons']:
   if e not in inherited:inherited.append(deepcopy(e))
  for c in doc['completeAcceptedCounterparts']:
   if c not in counterparts:counterparts.append(deepcopy(c))
 bind(Path(__file__));ip=R/'data/public/spell_playtests/authored_review_index.json';index=read(ip);ck('Current505/343',index['authoredCounts']=={'reviewed':505,'pending':343});bind(ip)
 ck('All16 distinct actual source identities',len(records)==len({r['spellId'] for r in records})==16 and set(TIERS)=={r['spellId'] for r in records})
 ck('18 printed placements',sum(len(r['completeCurrentBookBindings']) for r in records)==18)
 counts=dict(Counter(r['riskTier'] for r in records));ck('Actual mixed risk allocation',counts=={'B':12,'A':1,'C':3})
 ck('33 unique genuine source questions',len(questions)==len({q['id'] for q in questions})==33)
 ck('No earlier complete cases invented',all(not r['earlierCompleteProcedures'] and not r['earlierWorkedCases'] for r in records))
 result={'id':'RANK7-MECHANICS16-SOURCE-CONFERENCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREAUTHORSHIP_SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','supersedesForDispatchOnly':parents,'sourcePreservation':'Both complete parent packets and all original16-spell historical records/questions remain exact. Grouping and risk metadata are revised; no prior file is edited or deleted.','records':records,'riskCounts':counts,'reviewAllocation':'Read all16source records and all33genuine questions. Reuse exact accepted interfaces without reopening them. Arcbolt receives routine finite-parameter review; twelve interaction-heavy spells receive focused lifecycle/geometry/control review; deeper systemic conference is limited to Lasting Control, Reverse Gravity and Prismatic Spray. Mixed16 grouping avoids two repeated reviews of common current sources; no requirement for identical treatment across all16.','questions':questions,'acceptedDependenciesAndInheritedRequirements':inherited,'completeAcceptedCounterparts':counterparts,'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'why':r['riskReason'],'sourcePreserved':True,'existingInterfacesReusedUnchanged':True,'newScopedChoices':[q['id'] for q in questions if r['spellId'] in q['spellIds']],'fullSourcePromise':r['completeCurrentCatalogSourceAndAccess']['source']['original']['description']} for r in records],'conferenceRouting':'Within each question, settled current interface behavior is context and a required constraint, not a new decision. Resolve only missing local parameters, source promise conflicts and explicitly identified new systemic exceptions. Do not reconstruct ordinary pricing, casting, hard admission, damage, Null, ordinary body/falling, Fate or companion engines. A new source-specific binding is not global promotion.','caseDevelopmentRequirement':'Zero current encounters submitted. Return complete proposed procedures and source-qualified case requirements, then build actual complete vectors and obtain exact acceptance. At least two substantive scenarios per spell, every Prismatic entry and both preserved school profiles where applicable; missing real eligibility/body/source records remain explicit holds.','originalWorkedCases':[],'currentVectors':[],'sourceBindings':list(sources.values()),'countsUnchanged':index['authoredCounts'],'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'cosmologyDecisions':0,'sourceInformationDeleted':0}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Freeze current source '+b['path'],info(p)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes());ck('Full raw copy '+b['path'],dst.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 out.write_bytes(encoded(result));check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'failures':0,'sourceIdentities':16,'placements':18,'riskCounts':counts,'genuineQuestions':33,'inheritedFormerQuestions':2,'fullEarlierProcedures':0,'originalWorkedCases':0,'newCurrentVectors':0,'sourceCount':len(sources),'validationScope':'Source preservation, exact current access/book references from checked parent packets, risk allocation and archive integrity only; no semantic acceptance or engine tests.'}))
 (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'sources':frozen,'parentPacketsUnchanged':parents,'sourceCount':len(sources)}))
 (root/'README.md').write_text('''# Rank7 mechanics16 source conference01

This is a mixed16 source conference under the owner’s accelerated digital review protocol:1routine,12interaction-heavy,3systemic. Read all16exact source records/18placements and33genuine source decisions. Allocate deep review to the3systemic decisions, not every inherited rule. The original two unsent8-spell packets remain full unchanged history; their blanket all-C staging labels are superseded by this per-spell classification. Two former workflow/access questions are inherited requirements, not open design choices.

Return complete source-linked proposed procedures, exception-focused per-question dispositions, full source verification and precise current-case obligations. No earlier full procedures or worked cases exist for this cohort in the audited authoring map; zero current encounters are submitted here. No new access, external spell imports, global interface promotion, cosmology, runtime/human/balance or whole-game approval.505reviewed/343pending unchanged. This packet is UNSENT.
''',encoding='utf8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in ['README.md','MANIFEST.json']:z.write(root/n,n)
  z.write(out,'CANDIDATE.json');z.write(check,'PREFLIGHT.json')
  for b in frozen:z.write(G/b['frozenCopy'],'sources/'+b['path'])
 with zipfile.ZipFile(archive) as z:
  ck('Archive CRC',z.testzip() is None);assert z.read('CANDIDATE.json')==out.read_bytes()
  for b in frozen:assert z.read('sources/'+b['path'])==(G/b['frozenCopy']).read_bytes()
 b=info(archive);req.write_text(f'Conduct Rank7 mechanics16 source conference using {archive.name}, {b["bytes"]} bytes,SHA256 {b["sha256"]}. Read all16source identities/18placements/33genuine decisions. Risk allocation1A/12B/3C; use accepted143interfaces unchanged and do not reopen inherited requirements. Return complete source-linked proposed procedures and case obligations. Zero earlier full procedures or worked cases are claimed. All original parent packets retained; new per-spell risk classification supersedes only blanket staging labels.505/343 unchanged, no adoption/runtime/human/balance/cosmology/domain closure.\n',encoding='utf8',newline='\n')
 prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'check':info(check),'request':info(req),'sourceCount':len(sources),'allArchiveSourcesVerified':True,'riskCounts':counts,'status':'Prepared UNSENT; preferred dispatch instead of the two unchanged eight-spell parents.','newRuleAdoptions':0}));print(json.dumps({'archive':b,'candidate':info(out),'sources':len(sources),'checks':len(checks),'riskCounts':counts,'questions':33}))

if __name__=='__main__':main()
