"""Author six pending training feats; preserve sources and operational manifest."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def info(b):return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
prepared=load(A/'GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json')
sources={x['featId']:x for x in prepared['selectedFeats']}
registry=R/'src/data/feats.js';raw=json.JSONDecoder().raw_decode(registry.read_text('utf-8').split('export const feats = ',1)[1])[0];by={f['id']:f for f in raw}
manifest=R/'data/public/feat_playtests/manifest.json';reviewed=set(load(manifest)['operationalIds'])
assert len(raw)==335 and len(reviewed)==8
out=R/'data/director/training_feat_operating_proposal_internal.json';doc=R/'docs/feats/TRAINING_FEAT_OPERATING_PROPOSAL.md';receipt=A/'TRAINING_FEAT_6_OPERATING_PROPOSAL_CHECK.json'
assert not out.exists() and not doc.exists() and not receipt.exists()
shared=[
 ('Acquire the actual feat', 'UNADOPTED NEW scope: these six feats are nonrepeatable and require an actual legal feat selection at the class progression\'s existing milestone. Check the printed permanent ability prerequisite at acquisition. A title, descriptive similarity or compatibility alias grants no second acquisition. The six names below remain distinct source identities.'),
 ('Snapshot each skill separately', 'NEW: immediately before applying this feat, record whether the character is already proficient in each listed skill. For a skill not yet proficient, grant proficiency. For a skill already proficient, grant twice-PB Expertise for that skill. Make this branch decision independently for every skill, before any of this feat\'s own grants. Do not let its first proficiency grant count as prior proficiency for a second reading of the same clause.'),
 ('Record and retain the selected branch', 'NEW: save the acquisition event, feat ID, skill, prior proficiency and resulting grant. A proficiency branch does not turn into Expertise merely because another source later grants the same proficiency. Resolve the later source under its own duplicate rule. Where an earned advancement permits sequential choices, process and record the actual chosen acquisition order; do not rewrite that order after observing a later result or silently treat all grants as simultaneous.'),
 ('One proficiency contribution', 'RETAIN current character foundation: a check uses its actual ability modifier plus at most one applicable proficiency contribution. Twice PB replaces normal PB. Two Expertise sources still supply twice PB, never three or four times PB. If an independently reviewed source explicitly supplies a larger proficiency multiplier, use the largest applicable single multiplier; this proposal grants none. A qualifying skill and tool do not each add PB.'),
 ('Do the real task', 'The feat grants training, not automatic success or a new permitted action. Apply task degrees, contested ties, actual senses, equipment, legal access, time, materials and advantage/disadvantage normally. A skill check may use a different ability when the actual governing task expressly calls for it; the applicable proficiency grant remains in that skill. No feat creates a movement mode, willing creature, food, information, companion or new social authority.'),
 ('Existing overlap stays distinct', 'Acrobat grants only Acrobatics training/Expertise. Acrobatic, Athletic Prodigy and Acrobatic Mastery remain separate original feats with their own prerequisites and effects. Animal Affinity does not grant Beast Whisperer or Beast Lore. Naturalist grants no Ranger class level or Ranger Training hiding permission. Shared skills do not merge source IDs or create repeatable acquisitions.'),
 ('What still needs joint approval', 'The acquisition-time branch, nonrepeatability and duplicate-branch policy are explicit new authoring choices. They need GPT agreement across all feat cohorts, including Cultural Expert, fixed training grants and any later retraining procedure. Current operational feat count remains eight of 335; these six and the separate 25 Skill-feat proposals remain pending. No source registry or public operational manifest is changed.')]
cards=[
 ('GE-01','acrobat',['Acrobatics'],
  'Gain proficiency in Acrobatics if not already proficient immediately before acquiring this feat. Otherwise use twice PB for Acrobatics checks. This does not substitute Dexterity for an Athletics check, grant a climbing Speed, improve an actual jump distance or allow a reroll. Those benefits require their own actual sources.',
  ['A DEX 16, PB +2 character without Acrobatics gains a +5 normal Dexterity (Acrobatics) modifier, not +7.',
   'A DEX 16, PB +2 character already proficient in Acrobatics now uses +7. Already having another twice-PB Acrobatics source leaves +7, not +11.',
   'Owning this feat does not satisfy a prerequisite asking for the differently named Acrobatic feat unless a future explicit identity decision says so.']),
 ('GE-04','animalAffinity',['Animal Handling'],
  'Gain proficiency in Animal Handling if not already proficient immediately before acquiring this feat. Otherwise use twice PB for Animal Handling checks. Apply it to an actual Animal Handling task allowed by the creature and situation. It provides no telepathy, creature language, automatic attitude change, trained mount, companion, domination or guaranteed cooperation. A different social or knowledge skill does not gain this proficiency merely because an animal is present.',
  ['A WIS 14, PB +3 character already trained in Animal Handling uses +8 on an eligible Wisdom (Animal Handling) check.',
   'An untrained holder gains normal proficiency, then later gains another Animal Handling grant from a separate source: this feat remains its original proficiency branch. The new grant follows its own rule.',
   'Even an excellent check does not create an absent beast or let an untrained mount use combat actions unavailable under its real control procedure.']),
 ('GE-06','athleticProdigy',['Athletics','Acrobatics'],
  'The prerequisite is Strength 15 or Dexterity 15; either permanent score suffices. Evaluate Athletics and Acrobatics separately at acquisition. Grant proficiency in each untrained skill and twice-PB Expertise in each already proficient skill. Neither skill grant changes which ability the ordinary task uses. The feat gives no Speed, movement, jumping-distance increase or automatic success. Other Expertise in one of these skills is an overlapping grant of twice PB, not another multiplier.',
  ['STR 15, DEX 12 meets the prerequisite. If Athletics is already trained but Acrobatics is not, acquire Athletics Expertise and ordinary Acrobatics proficiency.',
   'With PB +3, STR +2 and DEX +1 in that mixed case, ordinary Athletics is +8 and ordinary Acrobatics is +4. An Acrobatics roll of 12 totals 16.',
   'If both skills are already proficient, both gain twice PB independently. If both already have Expertise, neither becomes four times PB.']),
 ('GE-09','charismatic',['Persuasion','Deception'],
  'Evaluate Persuasion and Deception separately at acquisition: gain proficiency if untrained, or twice-PB Expertise if already proficient. These grants do not extend to Performance, Intimidation, Reputation or Insight. Persuasion and Deception remain distinct tasks with actual possible stakes, evidence, audience understanding and failure. The feat does not force agreement, make a lie objectively true, change standing or defeat magical truth restrictions by itself.',
  ['A CHA 16, PB +2 holder already proficient in Persuasion but not Deception has +7 Persuasion and +5 Deception after acquiring this feat.',
   'The same holder\'s Performance proficiency and modifier remain exactly what their other real sources provide; Charismatic grants neither.',
   'Two actual feats each granting Persuasion Expertise still yield +7 in this example, not +11; the overlapping grant history remains recorded.']),
 ('GE-14','diplomat',['Persuasion','Insight'],
  'Evaluate Persuasion and Insight separately at acquisition: gain proficiency if untrained, or twice-PB Expertise if already proficient. Use the actual ability for each task, normally Charisma for Persuasion and Wisdom for Insight. Diplomacy still requires an eligible request and a perceivable, understandable interaction. Insight can reveal only what the actual successful task supports; it is neither automatic mind reading nor a guarantee that a suspected statement is false. This feat grants no extra audience, faction rank or negotiated discount.',
  ['CHA 14, WIS 16 and PB +3 with existing Insight but no Persuasion produces +5 Persuasion and +9 Insight after acquisition.',
   'A legal choice order acquiring Charismatic first can leave Persuasion proficient before a later Diplomat acquisition, so Diplomat grants Expertise there. Record both events; this is sequential ownership, not free retroactive rewriting.',
   'An opposed Insight total of 16 against Deception 16 keeps the existing state under current Core ties; Expertise does not create an automatic win.']),
 ('GE-23','naturalist',['Nature','Survival'],
  'Evaluate Nature and Survival separately at acquisition: gain proficiency if untrained, or twice-PB Expertise if already proficient. Nature remains the relevant knowledge skill, normally Intelligence; Survival remains the actual navigation, tracking or resource-finding skill, normally Wisdom, when the task calls for it. The feat grants no free forage yield, hidden ecological fact, ingredient identity, wilderness immunity or new resource. It does not bypass the actual Supply, source-depletion, route, watch or creature-size procedures. No creature origin or cosmology is inferred from its name.',
  ['INT 12, WIS 16, PB +2 with Nature trained and Survival untrained gives Nature +5 and Survival +5 after acquisition; equal totals arise from different ability/proficiency contributions.',
   'Two sources of Survival Expertise use one twice-PB contribution. A tool credential that also fits the task does not add a second PB.',
   'A successful knowledge check can identify a plant from available evidence. If an area is already depleted, the feat does not make another harvest exist.'])]
records=[];checks=[]
def check(n,v):checks.append({'name':n,'pass':bool(v)});assert v,n
for q,fid,skills,procedure,cases in cards:
 s=sources[fid];check(q+' original question identity',s['questionId']==q);check(q+' complete source unchanged',s['sourceObject']==by[fid]);check(q+' still pending',fid not in reviewed)
 records.append({'questionId':q,'featId':fid,'sourceObject':s['sourceObject'],'sourceObjectSha256':s['sourceObjectSha256'],'originalQuestion':s['fullClauseQuestion'],'skills':skills,'procedure':procedure,'newChoices':'Apply the shared proposed acquisition snapshot independently to each listed skill; retain full source prerequisite/effect and no stacking of Expertise.','workedCases':cases,'status':'unadopted-authoring-proposal'})
inputs=[registry,manifest,A/'GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json',R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/BUFFER_FEAT_PLAYTEST.md']
inputInfo={p.relative_to(G).as_posix():info(p.read_bytes()) for p in inputs}
result={'status':'UNADOPTED; six complete training-feat proposals for next joint review; UNSENT','createdAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Exactly GE-01/04/06/09/14/23 from the 31-entry General exploration source cohort; the other 25 GE records remain outside this proposal.','sharedProposal':[{'heading':h,'text':t} for h,t in shared],'records':records,'inputs':inputInfo,'sourceFeats':335,'reviewedFeatsUnchanged':8,'pendingFeatsUnchanged':327,'runtimeImplemented':False,'cosmologyReviewed':False,'sourceInformationDeleted':0}
save(out,result)
lines=['# Six training feats: complete operating proposal','',
 '**UNADOPTED; awaiting joint GPT review.** This proposal completes the draft procedures for Acrobat, Animal Affinity, Athletic Prodigy, Charismatic, Diplomat and Naturalist. It preserves all six full original records and their original GE questions. The other 25 General exploration feats are outside this document. The operational feat count remains eight reviewed and 327 pending.','',
 '[Structured proposal and preserved sources](../../data/director/training_feat_operating_proposal_internal.json) · [Original General exploration source audit](../../../../docs/audit/2026-10-08/full-game/GENERAL_EXPLORATION_FEAT_SOURCE_AUDIT.md) · [Separate 25 Skill-feat proposals](SKILL_FEAT_OPERATING_PROPOSAL.md)','',
 '## Shared procedure','']
for h,t in shared:lines.extend(['### '+h,'',t,''])
for x in records:
 f=x['sourceObject'];lines.extend(['## '+x['questionId']+' — '+f['name'],'',f"Source identity: `{f['id']}`. Original prerequisite: **{f['prerequisite']}**.",'','**Source effect, unchanged**','',f['effect'],'','**Proposed procedure**','',x['procedure'],'','**Worked adjudications**',''])
 for c in x['workedCases']:lines.extend(['- '+c,''])
 lines.extend(['<details><summary>Complete original source and conference question</summary>','','```json',json.dumps(f,ensure_ascii=False,indent=2),'```','',x['originalQuestion'],'','</details>',''])
lines+=['## Evidence and boundary','',
 'The 18 examples are authored adjudications, not complete character-builder runtime tests. The local check verifies their explicit arithmetic, six exact source objects, identity/scope and unchanged reviewed manifest. No active rules, character saves, source registries or submitted expedition files are edited. Joint source agreement and exact candidate review still precede operational adoption; numerical balance and human testing remain open.','']
doc.parent.mkdir(parents=True,exist_ok=True);doc.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
arithmetic=[('Acrobat proficiency',3+2,5),('Acrobat expertise',3+2*2,7),('Animal Affinity expertise',2+2*3,8),('Athletic mixed Athletics',2+2*3,8),('Athletic mixed Acrobatics',1+3,4),('Athletic actual roll',12+1+3,16),('Charismatic Persuasion',3+2*2,7),('Charismatic Deception',3+2,5),('Diplomat Persuasion',2+3,5),('Diplomat Insight',3+2*3,9),('Naturalist Nature',1+2*2,5),('Naturalist Survival',3+2,5)]
for n,a,e in arithmetic:check(n,a==e)
check('Six complete records',len(records)==6);check('Eighteen authored adjudications',sum(len(x['workedCases']) for x in records)==18)
check('Preserved current inputs',all(info((G/rel).read_bytes())==want for rel,want in inputInfo.items()))
check('Both source registries unchanged and identical',registry.read_bytes()==(G/'src/data/feats.js').read_bytes())
for rel,want in load(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
 if rel!='README_EXPEDITION_INTEGRATED_V3.md':check('Frozen submission unchanged: '+rel,info((G/rel).read_bytes())==want)
e={'status':result['status'],'createdAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'failures':0,'sourceRecords':6,'originalQuestions':6,'authoredAdjudications':18,'plainArithmeticChecks':len(arithmetic),'runtimeCases':0,'operationalReviewedUnchanged':8,'pendingUnchanged':327,'artifacts':{p.relative_to(G).as_posix():info(p.read_bytes()) for p in [out,doc]},'details':checks,'sourceInformationDeleted':0,'cosmologyReviewed':False}
save(receipt,e);print(json.dumps({k:v for k,v in e.items() if k!='details'},ensure_ascii=False))
