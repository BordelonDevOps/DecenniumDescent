"""Consolidate all31 GE source records with full unadopted procedures."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,re,sys
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def info(b):return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=R/'data/director/general_exploration_feat_operating_proposal_internal.json';doc=R/'docs/feats/GENERAL_EXPLORATION_FEAT_OPERATING_PROPOSAL.md';receipt=A/'GENERAL_EXPLORATION_31_OPERATING_PROPOSAL_CHECK.json'
assert all(not p.exists() for p in [out,doc,receipt])
draft=load(A/'GENERAL_EXPLORATION_25_OPERATING_PROPOSALS.json')
six=load(R/'data/director/training_feat_operating_proposal_internal.json')
prepared=load(A/'GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json')
registry=R/'src/data/feats.js';raw=json.JSONDecoder().raw_decode(registry.read_text('utf-8').split('export const feats = ',1)[1])[0];by={x['id']:x for x in raw}
manifest=R/'data/public/feat_playtests/manifest.json';reviewed=set(load(manifest)['operationalIds'])
assert len(raw)==335 and len(reviewed)==8
proposed={x['featId']:x for x in draft['proposals']};existing={x['featId']:x for x in six['records']}
assert len(proposed)==25 and len(existing)==6 and not set(proposed)&set(existing)
assert set(proposed)|set(existing)=={x['featId'] for x in prepared['selectedFeats']}
checks=[]
def check(n,v):checks.append({'name':n,'pass':bool(v)});assert v,n
records=[]
for s in prepared['selectedFeats']:
 fid=s['featId'];x=proposed.get(fid,existing.get(fid));q=s['questionId']
 check(q+' exact current original source',by[fid]==s['sourceObject'])
 check(q+' original question identity',x['questionId']==q)
 check(q+' remains pending',fid not in reviewed)
 check(q+' complete procedure',len(x['procedure'])>=300)
 check(q+' explicit new choices',len(x['newChoices'])>30)
 check(q+' authored examples',len(x['workedCases'])>=2 and all(len(c)>70 for c in x['workedCases']))
 records.append({**x,'sourceObject':s['sourceObject'],'sourceObjectSha256':s['sourceObjectSha256'],'originalQuestion':s['fullClauseQuestion'],'sharedTrainingProcedureApplies':fid in existing,'status':'unadopted-proposal-not-operational','authoredCasesAreRuntimeTests':False})
inputPaths=[registry,manifest,A/'GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json',A/'GENERAL_EXPLORATION_25_OPERATING_PROPOSALS.json',R/'data/director/training_feat_operating_proposal_internal.json',R/'docs/feats/TRAINING_FEAT_OPERATING_PROPOSAL.md',R/'data/director/skill_feat_operating_proposal_internal.json']
for name in ['CORE_RESOLUTION_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','LANGUAGE_COMMUNICATION_PLAYTEST.md','SPELL_INTEGRATION_RULES.md','CLASS_PLAYTEST_RULES.md','EQUIPMENT_ITEM_PROCEDURES.md']:
 inputPaths.append(R/'docs/mechanics'/name)
inputInfo={p.relative_to(G).as_posix():info(p.read_bytes()) for p in inputPaths}
result={'status':'UNADOPTED; all31 General exploration feats have complete proposed procedures; UNSENT','createdAtUtc':datetime.now(timezone.utc).isoformat(),'sharedProposal':draft['sharedProposal'],'trainingSharedProposal':six['sharedProposal'],'records':records,'sourceFiles':inputInfo,'sourceFeats':335,'reviewedFeatsUnchanged':8,'pendingFeatsUnchanged':327,'sourceInformationDeleted':0,'runtimeImplemented':False,'cosmologyReviewed':False,'priorSixProposalPreserved':True}
save(out,result)
lines=['# General exploration feats: complete operating proposal','',
 '**UNADOPTED — all31 GE entries await the joint source conference and exact review.** This manuscript consolidates the six prior training-feat proposals with25 new exploration/social procedures. Every original record, prerequisite, effect and GE question is retained. The public operational manifest still has eight reviewed feats and327 pending; this document grants no active feat.','',
 '[Complete structured proposal](../../data/director/general_exploration_feat_operating_proposal_internal.json) · [Original source audit](../../../../docs/audit/2026-10-08/full-game/GENERAL_EXPLORATION_FEAT_SOURCE_AUDIT.md) · [Separate25 Skill-feat proposal](SKILL_FEAT_OPERATING_PROPOSAL.md) · [Preserved six-feat draft](TRAINING_FEAT_OPERATING_PROPOSAL.md) · [Local preservation/arithmetic evidence](../../../../docs/audit/2026-10-08/full-game/GENERAL_EXPLORATION_31_OPERATING_PROPOSAL_CHECK.json)','',
 'The68 examples are authored adjudications. Only the specifically recorded arithmetic/Core queries are executed checks; they do not implement these feats, certify balance or represent a campaign. The live58-question expedition packet remains frozen. Reconcile its actual final decisions before sending this proposal.','',
 '## Shared proposal','']
for h,t in draft['sharedProposal'].items():lines.extend(['### '+h[0].upper()+h[1:],'',t,''])
lines+=['## Additional shared procedure for the six training feats','',
 'This section applies only to GE-01/04/06/09/14/23. Other fixed skill grants use the explicit proposal above.','']
for x in six['sharedProposal']:lines.extend(['### '+x['heading'],'',x['text'],''])
lines+=['## Complete feat entries','']
for x in records:
 f=x['sourceObject'];lines.extend(['### '+x['questionId']+' — '+f['name'],'',f"Source identity: `{f['id']}`. Original prerequisite: **{f['prerequisite']}**.",'','**Source effect, unchanged**','',f['effect'],'','**Proposed procedure**','',x['procedure'],'','**Explicit NEW choices:** '+x['newChoices'],'','**Worked adjudications**',''])
 for c in x['workedCases']:lines.extend(['- '+c,''])
 if x.get('dependencies'):lines.extend(['**Dependencies:** '+'; '.join(x['dependencies'])+'.',''])
 lines.extend(['<details><summary>Complete original record and original conference question</summary>','','```json',json.dumps(f,ensure_ascii=False,indent=2),'```','',x['originalQuestion'],'','</details>',''])
lines+=['## Decisions that must be conferred explicitly','',
 'Appraise currently proposes identification of ordinary magical properties and otherwise discoverable curses, not merely a mundane estimate. Cartographer interprets the never-lost promise as reliable retracing of actually traversed, unchanged routes. Deceiver proposes a narrow exception to magical truth compulsion while preserving other effects. Forager retains a guaranteed seven-person yield only where actual accessible food and water stocks can supply it. Improved Athlete proposes a full-Strength standing jump and keeps the base Athlete running benefit. Tracker proposes a real but local, finite exceptional trail sense over air and water. Wilderness Walker proposes removal of terrain-only movement penalties including qualifying magical terrain. Those are concrete design choices requiring the actual source conference, not claims that all details were already canon.','',
 'The new hireling, inquiry, performance, foraging, exposure and scavenging times/numbers must be reconciled with the expedition/social/transport decision and full corresponding catalogs. Preserve creature agency, actual inventories, party limits and every remaining source effect. A broad feat label cannot approve a spell, magic item, creature, runtime or cosmology. Final whole-game flow agreement, authorized push and remote verification still precede the careful cosmology review.','']
doc.parent.mkdir(parents=True,exist_ok=True);doc.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
for rel,want in inputInfo.items():check('Current input preserved: '+rel,info((G/rel).read_bytes())==want)
check('Source registries remain identical',registry.read_bytes()==(G/'src/data/feats.js').read_bytes())
check('All31 original GE questions represented once',len(records)==31 and len({x['questionId'] for x in records})==31)
check('All68 authored examples present',sum(len(x['workedCases']) for x in records)==68)
sys.path.insert(0,str(R/'tools'));from core_playtest_rules import task_check
core=[('Improved Climber deficit4',task_check(10,4,18),{'total':14,'degree':'failure','success':False}),('Improved Climber natural1 deficit2',task_check(1,15,18),{'total':16,'degree':'critical-failure','success':False})]
for name,actual,expected in core:check(name,actual==expected)
arith=[('Acrobatic Athletics',3+2,5),('Bruiser Intimidation',4+3,7),('Entertainer actual fee less cost',20-5,15),('Gossip90minute task',90/2,45),('Improved Athlete running distance',16+3,19),('Improved Athlete approach and jump',10+19,29),('Observant passive Perception',10+3+2+5,20),('Observant passive Investigation',10+3+3+5,21),('Survivalist food',2/2,1),('Survivalist water',4/2,2),('Tracker old intermingled DC',15+5+5,25),('Wilderness Walker crawl squeeze cost',1+1+1,3)]
for n,a,e in arith:check(n,a==e)
for rel,want in load(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
 if rel!='README_EXPEDITION_INTEGRATED_V3.md':check('Live submission unchanged: '+rel,info((G/rel).read_bytes())==want)
links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text('utf-8'))
for rel in links:check('Manuscript link '+rel,(doc.parent/rel).resolve().exists() or (doc.parent/rel).resolve()==receipt)
e={'status':result['status'],'createdAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRecords':31,'originalQuestions':31,'newThisBuild':25,'priorTrainingProceduresPreserved':6,'authoredExamples':68,'checks':len(checks),'failures':0,'existingCoreQueries':len(core),'plainArithmeticChecks':len(arith),'fullFeatRuntimeCases':0,'sourceFeats':335,'operationalReviewedUnchanged':8,'pendingUnchanged':327,'submittedRepositoryPayloadsUnchanged':303,'artifacts':{p.relative_to(G).as_posix():info(p.read_bytes()) for p in [out,doc]},'details':checks,'sourceInformationDeleted':0,'cosmologyReviewed':False,'pushed':False}
save(receipt,e);assert all((doc.parent/rel).resolve().exists() for rel in links)
print(json.dumps({k:v for k,v in e.items() if k!='details'},ensure_ascii=False))
