"""Build a non-operative full-source authoring proposal; no reviewed manifest changes."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,re
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def info(b):return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def digest(x):return sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
dataout=R/'data/director/skill_feat_operating_proposal_internal.json'
docout=R/'docs/feats/SKILL_FEAT_OPERATING_PROPOSAL.md'
receipt=A/'SKILL_FEAT_25_OPERATING_PROPOSAL_CHECK.json'
if any(p.exists() for p in (dataout,docout,receipt)):
    backup=A/'skill-feats-before-proposal-arithmetic-correction'
    assert all(p.exists() and (backup/p.name).read_bytes()==p.read_bytes() for p in (dataout,docout,receipt)), 'Existing outputs must be preserved exactly before replacement'
draft=load(A/'SKILL_FEAT_25_OPERATING_PROPOSALS.json')
prepared=load(A/'SKILL_FEAT_SOURCE_PREPARATION.json')
registry=R/'src/data/feats.js'
raw=json.JSONDecoder().raw_decode(registry.read_text('utf-8').split('export const feats = ',1)[1])[0]
by={f['id']:f for f in raw}
manifestPath=R/'data/public/feat_playtests/manifest.json';operational=load(manifestPath)
reviewed=set(operational['operationalIds'])
assert len(raw)==335 and len(reviewed)==8
assert registry.read_bytes()==(G/'src/data/feats.js').read_bytes()
assert {x['featId'] for x in draft['proposals']}=={x['featId'] for x in prepared['selectedFeats']}
sources={x['featId']:x for x in prepared['selectedFeats']}
context=[registry,manifestPath,A/'SKILL_FEAT_SOURCE_PREPARATION.json',A/'SKILL_FEAT_25_OPERATING_PROPOSALS.json',R/'data/playtest/character_foundation.json']
for name in ['CORE_RESOLUTION_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CLASS_PLAYTEST_RULES.md','COMBAT_ACTION_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','BUFFER_FEAT_PLAYTEST.md','CRAFTING_HARVEST_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','SPELL_INTEGRATION_RULES.md','classes/wizard.md']:
    context.append(R/'docs/mechanics'/name)
contextInfo={p.relative_to(G).as_posix():info(p.read_bytes()) for p in context}
records=[];checks=[]
def check(name,value):checks.append({'name':name,'pass':bool(value)});assert value,name
for x in draft['proposals']:
    s=sources[x['featId']]
    check(x['questionId']+' source object unchanged',by[x['featId']]==s['sourceObject'])
    check(x['questionId']+' original question identity',x['questionId']==s['questionId'])
    check(x['questionId']+' remains pending',x['featId'] not in reviewed)
    check(x['questionId']+' full authored procedure and explicit new choices',len(x['procedure'])>=450 and len(x['newChoices'])>=40)
    check(x['questionId']+' two authored adjudications',len(x['workedCases'])==2 and all(len(c)>90 for c in x['workedCases']))
    records.append({**x,'sourceObject':s['sourceObject'],'sourceObjectSha256':s['sourceObjectSha256'],'originalQuestion':s['fullClauseQuestion'],'status':'unadopted-proposal-not-operational','authoredCasesAreRuntimeTests':False})
result={**{k:v for k,v in draft.items() if k!='proposals'},'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'records':records,'currentSourceFiles':contextInfo,'protectedReviewedIds':sorted(reviewed),'sourceFeatCount':335,'reviewedFeatCountUnchanged':8,'pendingFeatCountUnchanged':327,'sourceInformationDeleted':0,'publicOperationalManifestChanged':False,'runtimeImplemented':False,'cosmologyInterpreted':False}
save(dataout,result)
lines=['# Skill feats: complete operating proposal','',
 '**UNADOPTED — for the next joint Codex/GPT conference.** These 25 entries retain their original full source records and original SF questions. The new procedures, prerequisite bridges and numerical choices below are proposals, not active rules. The operational manifest still contains the same eight reviewed feats; all 327 others remain pending.','',
 '[Complete structured source and proposal records](../../data/director/skill_feat_operating_proposal_internal.json) · [Original 25-question source audit](../../../../docs/audit/2026-10-08/full-game/SKILL_FEAT_SOURCE_AUDIT.md) · [Local preservation checks](../../../../docs/audit/2026-10-08/full-game/SKILL_FEAT_25_OPERATING_PROPOSAL_CHECK.json)','',
 'This document is an internal development proposal. Its 50 worked adjudications are authored expectations, not executed game-runtime tests or campaign facts. The currently submitted 58-question expedition package remains frozen; no proposal in this file changes that submission. Reconcile the eventual expedition/social/transport verdict before sending this proposal for review.','',
 '## Shared proposed procedure','']
for k,v in draft['sharedProposal'].items():lines.extend(['### '+k[0].upper()+k[1:],'',v,''])
lines+=['## The 25 feats','']
for x in records:
    f=x['sourceObject'];lines.extend([f"### {x['questionId']} — {f['name']}",'',f"Source identity: `{f['id']}`. Source category: {f['type']}. Original prerequisite: **{f['prerequisite']}**.",'',
      '**Current source effect, preserved verbatim**','',f['effect'],'',
      '**Proposed complete procedure**','',x['procedure'],'',
      '**Explicit NEW choices requiring agreement:** '+x['newChoices'],'',
      '**Worked adjudications**',''])
    for case in x['workedCases']:lines.extend(['- '+case,''])
    lines.extend(['**Dependencies:** '+ '; '.join(x['dependencies'])+'.','',
      '<details><summary>Complete original record and original conference question</summary>','','```json',json.dumps(f,ensure_ascii=False,indent=2),'```','',x['originalQuestion'],'','</details>',''])
lines+=['## Review and adoption boundary','',
 'The next joint conference must explicitly decide the shared prerequisite/stacking bridges and every SF-01–25 procedure. Particular changes needing direct source-conflict decisions include Field Surgeon’s recovery classification, Runic Scholar’s protection against a gaze trigger, Spell Scribe’s overlapping discounts, the entire missing Wilderness Chef effect list, Anatomy Lore’s proposed damage base and Beast Lore’s call/briefing limits. Nothing here is a recovered numerical rule merely because it is now precise.','',
 'Following source agreement, revise the complete candidate and submit its exact files for operational review alongside the other feat cohorts. Preserve all current/legacy source wording and the eight already reviewed feat identities. Player publication, companion integration, human teaching and numerical balance remain separate. Final whole-game flow agreement comes before the authorized GitHub push; verified remote comes before careful cosmology review.','']
docout.parent.mkdir(parents=True,exist_ok=True);docout.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
check('25 complete source/proposal records',len(records)==25)
check('50 authored expectations',sum(len(x['workedCases']) for x in records)==50)
check('Master Tracker alias unchanged',by['master_tracker']['compatibilityAliases']==['skill_feats1_master_tracker'])
check('All source/context files unchanged during authoring',all(info((G/rel).read_bytes())==want for rel,want in contextInfo.items()))
frozen=load(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'];live=0
for rel,want in frozen.items():
    p=G/rel
    if p.exists():check('Submitted payload unchanged: '+rel,info(p.read_bytes())==want);live+=1
    else:check('Only archive README is virtual',rel=='README_EXPEDITION_INTEGRATED_V3.md')
check('303 live expedition payloads unchanged',live==303)
links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',docout.read_text('utf-8'))
for link in links:
    target=(docout.parent/link).resolve()
    check('Local manuscript link: '+link,target.exists() or target==receipt)
evidence={'status':'AUTHORING PROPOSAL SAVED; UNSENT; no feat promotion','generatedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'failures':0,'details':checks,'sourceRecords':25,'authoredAdjudications':50,'executedRuntimeCases':0,'originalQuestionsPreserved':25,'sourceFeatCount':335,'operationalReviewedUnchanged':8,'pendingUnchanged':327,'submittedExpeditionPayloadsUnchanged':303,'artifacts':{p.relative_to(G).as_posix():info(p.read_bytes()) for p in (dataout,docout)},'sourceInformationDeleted':0,'cosmologyReviewed':False,'pushed':False}
save(receipt,evidence)
assert all((docout.parent/x).resolve().exists() for x in links)
print(json.dumps({k:v for k,v in evidence.items() if k not in ['details']},ensure_ascii=False))
