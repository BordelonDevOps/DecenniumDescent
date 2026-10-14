"""Preserve all31 defensive feat sources and author full non-operative proposals."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,re,sys
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def info(b):return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=R/'data/director/general_defense_feat_operating_proposal_internal.json';doc=R/'docs/feats/GENERAL_DEFENSE_FEAT_OPERATING_PROPOSAL.md';receipt=A/'GENERAL_DEFENSE_31_OPERATING_PROPOSAL_CHECK.json'
assert all(not p.exists() for p in [out,doc,receipt])
draft=load(A/'GENERAL_DEFENSE_31_OPERATING_PROPOSALS.json');prepared=load(A/'GENERAL_DEFENSE_FEAT_SOURCE_PREPARATION.json')
registry=R/'src/data/feats.js';raw=json.JSONDecoder().raw_decode(registry.read_text('utf-8').split('export const feats = ',1)[1])[0];by={x['id']:x for x in raw}
manifest=R/'data/public/feat_playtests/manifest.json';reviewed=set(load(manifest)['operationalIds'])
assert len(raw)==335 and len(reviewed)==8
sources={x['featId']:x for x in prepared['selectedFeats']}
assert len(draft['proposals'])==31 and {x['featId'] for x in draft['proposals']}==set(sources)
checks=[]
def check(n,v):checks.append({'name':n,'pass':bool(v)});assert v,n
records=[]
for x in draft['proposals']:
 s=sources[x['featId']];q=x['questionId'];check(q+' original question identity',q==s['questionId']);check(q+' source object unchanged',s['sourceObject']==by[x['featId']]);check(q+' remains pending',x['featId'] not in reviewed)
 check(q+' authored procedure present',bool(x['procedure'].strip()));check(q+' explicit new choices present',bool(x['newChoices'].strip()));check(q+' two authored adjudications',len(x['workedCases'])==2 and all(c.strip() for c in x['workedCases']))
 records.append({**x,'sourceObject':s['sourceObject'],'sourceObjectSha256':s['sourceObjectSha256'],'originalQuestion':s['fullClauseQuestion'],'status':'unadopted-full-feat-proposal','priorReviewedComponentsCarried':x['featId'] in ['tenacity','tough','tough_as_nails','dark_fortitude'],'authoredCasesAreRuntimeTests':False})
inputs=[registry,manifest,A/'GENERAL_DEFENSE_FEAT_SOURCE_PREPARATION.json',A/'GENERAL_DEFENSE_31_OPERATING_PROPOSALS.json']
for n in ['MAXIMUM_HP_PLAYTEST.md','MAXIMUM_HP_SOURCE_BINDINGS.md','CORE_RESOLUTION_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','CLASS_PLAYTEST_RULES.md','LANGUAGE_COMMUNICATION_PLAYTEST.md','BUFFER_FEAT_PLAYTEST.md']:
 inputs.append(R/'docs/mechanics'/n)
inputs.extend([R/'tools/maximum_hp_playtest_rules.py',A/'GPT_MAXIMUM_HP_FINAL_CLOSURE.md'])
inputInfo={p.relative_to(G).as_posix():info(p.read_bytes()) for p in inputs}
result={'status':draft['status'],'createdAtUtc':datetime.now(timezone.utc).isoformat(),'sharedProposal':draft['sharedProposal'],'records':records,'sourceFiles':inputInfo,'sourceFeats':335,'reviewedFullFeatsUnchanged':8,'pendingFullFeatsUnchanged':327,'reviewedMaximumHpComponentsRetained':['tenacity','tough','tough_as_nails','dark_fortitude'],'sourceInformationDeleted':0,'runtimeImplemented':False,'cosmologyReviewed':False}
save(out,result)
lines=['# Defensive and foundation feats: complete operating proposal','',
 '**UNADOPTED — all31 full feat entries await the joint source conference and exact review.** The already reviewed maximum-HP components of Tenacity, Tough, Tough as Nails and Dark Fortitude remain controlling within their actual scope. This manuscript completes proposed acquisition and other-effect procedures; it does not reopen those settled coefficients, change the eight reviewed full feats or activate any of the327 pending entries.','',
 '[Complete structured proposal and source objects](../../data/director/general_defense_feat_operating_proposal_internal.json) · [Original defensive feat source audit](../../../../docs/audit/2026-10-08/full-game/GENERAL_DEFENSE_FEAT_SOURCE_AUDIT.md) · [Reviewed maximum-HP contract](../mechanics/MAXIMUM_HP_PLAYTEST.md) · [Local preservation/component checks](../../../../docs/audit/2026-10-08/full-game/GENERAL_DEFENSE_31_OPERATING_PROPOSAL_CHECK.json)','',
 'The62 worked examples are authored adjudications. The specifically recorded component/arithmetic checks below do not implement these full feats, prove campaign balance or represent actual play. All303 repository payloads of the live304-file expedition conference remain frozen. Dragon Blood and Elemental Body keep literal prerequisite receipts without new ancestry/plane interpretation.','',
 '## Shared proposed and retained rules','']
for h,t in draft['sharedProposal'].items():
 title=re.sub(r'(?<!^)(?=[A-Z])',' ',h).capitalize();lines.extend(['### '+title,'',t,''])
lines+=['## Complete feat entries','']
for x in records:
 f=x['sourceObject'];lines.extend(['### '+x['questionId']+' — '+f['name'],'',f"Source identity: `{f['id']}`. Original prerequisite: **{f['prerequisite']}**.",'','**Source effect, unchanged**','',f['effect'],'','**Proposed complete procedure**','',x['procedure'],'','**Explicit NEW choices:** '+x['newChoices'],'','**Worked adjudications**',''])
 for c in x['workedCases']:lines.extend(['- '+c,''])
 lines.extend(['**Dependencies:** '+'; '.join(x['dependencies'])+'.','',
  '<details><summary>Complete original record and original conference question</summary>','','```json',json.dumps(f,ensure_ascii=False,indent=2),'```','',x['originalQuestion'],'','</details>',''])
lines+=['## Joint decisions still required','',
 'Review all31 original questions against these complete procedures. Explicit new decisions include ASI/armor/save-feat repeatability; composite ability caps; Battle Ready helper timing; Berserker melee scope; literal Dragon Blood/Elemental Body eligibility; Durable and Quick Recovery healing arithmetic; Endurance deprivation clocks; Healer costs and recipient cadence; the mental-effect predicate; fear/death reroll boundaries; Cursebound silver components/floor timing; Dark Fortitude reaction ordering; and Undying Flesh’s actual living-episode deadline and damage rider. Preserve every current and legacy source alongside the selected result.','',
 'Do not call the whole feats reviewed because their maximum-HP components already passed. Do not treat a synthetic arithmetic result as a working actor/resource scheduler. Runtime integration, full spell/class/feat interactions, human teaching and numerical balance remain separate work. Final whole-game flow agreement precedes the authorized GitHub push; verified remote precedes careful cosmology review.','']
doc.parent.mkdir(parents=True,exist_ok=True);doc.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
for rel,want in inputInfo.items():check('Input preserved: '+rel,info((G/rel).read_bytes())==want)
check('Both original registries identical',registry.read_bytes()==(G/'src/data/feats.js').read_bytes())
check('31 original questions exactly once',len({x['questionId'] for x in records})==31)
check('62 authored examples',sum(len(x['workedCases']) for x in records)==62)
sys.path.insert(0,str(R/'tools'))
from maximum_hp_playtest_rules import source_amount,MaxHpRecord,effective_maximum,threshold,update_maximum
from core_playtest_rules import LifeState
component=[]
def componentCheck(n,a,e):component.append({'name':n,'actual':a,'expected':e});check(n,a==e)
componentCheck('Retained Tenacity coefficient',source_amount('feat:tenacity',character_level=7),7)
componentCheck('Retained Tough acquisition snapshot',source_amount('feat:tough',character_level=10,acquisition_level=4),8)
componentCheck('Retained Tough as Nails coefficient',source_amount('feat:tough_as_nails',character_level=6),12)
componentCheck('Retained Dark Fortitude coefficient',source_amount('feat:dark_fortitude',character_level=6),12)
mods=[MaxHpRecord('tenacity','feat:tenacity','pc','pc',6),MaxHpRecord('tough','feat:tough','pc','pc',8),MaxHpRecord('nails','feat:tough_as_nails','pc','pc',12),MaxHpRecord('dark','feat:dark_fortitude','pc','pc',12)]
componentCheck('Retained distinct HP feat bonuses add',effective_maximum(30,mods,target='pc')['effectiveMaximum'],68)
componentCheck('Retained duplicate Tough does not add',effective_maximum(30,mods+[MaxHpRecord('duplicate','feat:tough','pc','pc',8)],target='pc')['effectiveMaximum'],68)
componentCheck('Retained strict below-half odd maximum at10',threshold(10,21),True)
componentCheck('Retained strict below-half odd maximum at11',threshold(11,21),False)
life,report=update_maximum(LifeState(40,35),33,[],target='pc')
componentCheck('Retained capacity clamp is not damage',[life.hp,life.maximum_hp,report['capacityClamp'],report['actualHpDamage'],report['actualHpGained'],report['woundSaves'],report['deathFailuresAdded']],[33,33,2,0,0,0,0])
arith=[('Battle Ready with one helper',60/2/2,15),('Athlete running increase',16+3,19),('Durable positive CON floor',max(1+3,2*3,0),6),('Durable negative CON floor',max(1-1,2*-1,0),0),('Endurance future accrual',12/2,6),('Giant Strength pounds',18*15*2,540),('Giant Strength Load',18*2,36),('Healer dice and signed WIS',3+2+3,8),('Immortal Vigor natural aging',2/2,1),('Medium Armor Master formula',14+3,17),('Quick Recovery once-rest total',11+3,14),('Cursebound one own-family half',11//2,5),('Dark Fortitude remaining half',5//2,2)]
for n,a,e in arith:check(n,a==e)
for rel,want in load(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
 if rel!='README_EXPEDITION_INTEGRATED_V3.md':check('Submitted current payload unchanged: '+rel,info((G/rel).read_bytes())==want)
links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text('utf-8'))
for link in links:check('Local link: '+link,(doc.parent/link).resolve().exists() or (doc.parent/link).resolve()==receipt)
e={'status':draft['status'],'createdAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRecords':31,'originalQuestions':31,'authoredExamples':62,'checks':len(checks),'failures':0,'existingReviewedComponentQueries':len(component),'componentResults':component,'plainArithmeticChecks':len(arith),'fullFeatRuntimeCases':0,'sourceFeats':335,'operationalReviewedUnchanged':8,'pendingUnchanged':327,'submittedCurrentPayloadsUnchanged':303,'artifacts':{p.relative_to(G).as_posix():info(p.read_bytes()) for p in [out,doc]},'details':checks,'sourceInformationDeleted':0,'cosmologyReviewed':False,'pushed':False}
save(receipt,e);assert all((doc.parent/link).resolve().exists() for link in links)
print(json.dumps({k:v for k,v in e.items() if k not in ['details','componentResults']},ensure_ascii=False))
