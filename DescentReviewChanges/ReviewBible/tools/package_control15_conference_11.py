"""Add explicit source-contract routing and freeze the full control15 conference."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
 oldp=R/'data/director/spell_proposals/control_15_current_10.json';out=oldp.with_name('control_15_current_11.json');root=A/'control-15-conference-11';zp=A/'DD_Control_15_Conference_11.zip';prep=A/'CONTROL_15_CONFERENCE_11_PREPARATION.json';req=A/'CONTROL_15_CONFERENCE_11_REQUEST.txt';checkp=A/'CONTROL_15_CONFERENCE_CHECK_11.json'
 assert not any(p.exists() for p in [out,root,zp,prep,req,checkp]);old=read(oldp);d=deepcopy(old);checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 selected={0:['casting','timing','noCosmology'],1:['casting','snapshots','clocks','control','controlCadence'],2:['casting','admissionAndAgency','compelledBudgets','safetyOfCompelledConduct','clocksAndSaves','postPushBoundary'],3:['casting','geometry','clocks'],4:['casting','geometry','clocks','damageAndControl','identity']}
 d['sharedContractRouting11']={'status':'Proposed source-contract routing for conference, not new rule adoption.','precedence':'Actual accepted current interfaces govern only their recorded scopes. Each current full spell procedure controls its explicitly stated local proposal; these named original shared keys provide their relevant common constraints. A clause about another named spell never grants its powers to this cohort. Preserved historical examples/statuses and unrelated shared keys are evidence only. No generic attached phase, virtual control cycle, extra Action, memory edit or class permission is created by routing.','routes':[]}
 for s in d['spells']:
  j=next(j for j,x in enumerate(d['completeOriginalSharedProposals']) if x['source']['path']==s['originalSourceReference']['path']);shared=d['completeOriginalSharedProposals'][j]
  for key in selected[j]:ck('Actual shared key '+s['id']+'/'+key,key in shared['completeOriginalSharedProposal'])
  d['sharedContractRouting11']['routes'].append({'spellId':s['id'],'originalSource':deepcopy(shared['source']),'completeSharedPointer':f'/completeOriginalSharedProposals/{j}/completeOriginalSharedProposal','namedRelevantKeys':selected[j],'limits':'Only clauses applicable to this exact source identity. Source-specific bridges remain proposals; accepted registry does not authorize new sources by analogy.'})
 regp=R/'data/director/spell_review/accepted_interface_registry_04.json';reg=read(regp)
 for e in d['currentAcceptedInterfaceComparisons']:
  current=reg['entries'][int(e['registryPointer'].split('/')[-1])];ck('Full current registry entry '+e['registryPointer'],e['completeEntry']==current)
 d['previousCompleteDraft']=info(oldp);d['sourceBindings'].append(info(oldp));d.update(id='CONTROL-15-CURRENT-11',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='UNSENT UNADOPTED full conference candidate:15 full procedures,30 original/current scenario records and13questions; explicit source-contract routing. Conditional source gaps remain named. No30-game-runtime or fully-instantiated-all-branches claim.')
 for k in ['spells','originalExamplesUnchanged','currentExamples','completeOriginalSharedProposals','conferenceQuestions10','memorySourcesSeparated']:ck('Full unchanged '+k,d[k]==old[k])
 paths={oldp,regp}
 for b in d['sourceBindings']:
  p=G/b['path'];ck('Full source '+b['path'],info(p)==b);paths.add(p)
 def bindings(x):
  if isinstance(x,dict):
   if all(k in x for k in ['path','bytes','sha256']):yield {k:x[k] for k in ['path','bytes','sha256']}
   for v in x.values():yield from bindings(v)
  elif isinstance(x,list):
   for v in x:yield from bindings(v)
 for e in reg['entries']:
  for b in bindings({'current':e['currentAuthoritativeSource'],'acceptance':e['acceptanceBasis']}):
   p=G/b['path'];ck('Registry full authority '+b['path'],info(p)==b);paths.add(p)
 out.write_bytes(encoded(d));paths.add(out)
 checkp.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'runtimeTestsExecuted':0,'newRuleAdoptions':0,'sourceInformationDeleted':0}));paths.add(checkp)
 for p in A.glob('CONTROL*CHECK*.json'):paths.add(p)
 for p in (R/'tools').glob('prepare_control*.py'):paths.add(p)
 paths.add(R/'tools/package_control15_conference_11.py')
 root.mkdir();readme='''# Control15 — full source conference11

Prepared UNSENT while GPT reviews persistent20. Read MANIFEST.json, then the complete Current11 under files/DescentReviewChanges/ReviewBible/data/director/spell_proposals/. Review all15 spells, their complete source/access/procedures,30 original texts/current scenario records,13 conferenceQuestions10 and sharedContractRouting11. Every earlier draft and all full original proposals remain preserved. This is not a claim that every conditional branch is a completely instantiated game.

Current11 adds explicit routing only; all15 procedures and30 current records are byte-value identical to Current10. Accepted Registry04 entries and complete original source files are supplied. Named clauses retain their actual source predicates; generic shared headings never grant a different spell's powers. Historical statuses/examples are not current approval evidence. Actual current Wizard engine11 supplies first-distinct-matrix D0 without waiving Refrain or other actual hooks.

## Consequential review points

- Dominate Monster requires real operative numericalCR, not character level. Actual Warrior8 has none. Vaskor printedCR8 and CaveBear printedCR2 are preserved FULL director-only source candidates, still NOT operationally reviewed; neither native attack reach nor Large-to-bounded-companion conversion is invented. Original native-attack/CR2attached branches stay conditional. No bestiary, Gate/lore or cosmology promotion is requested.
- Standard companion PB is printed for saves, not every ability check. Puppet’s genuine-grapple acquisition premise remains explicitly conditional pending an actual contest profile. A phase already underway when Puppet establishes cannot receive a retroactive route. The exact first future END save after suppressed START is an explicit question.
- Mental Prison retains distinct28entry and24exit events, clear fixed body+5ft bounds, finite entitlement and real Lesser Antimagic branches. Its exact entry/exit damage-root and replacement sequence need concurrence. Pending TrueSeeing is a complete source counterpart; this conference does not adopt that spell.
- Actual MassSleep/Sleep/FalseLife/ArcaneRay and Eyebite fixtures keep positive defended damage separate from HP loss. At range, Prone disadvantage cancels Unconscious advantage; Current07 preserves and corrects the earlier current-case error. Specific rousing clears only its actual spell family; independent zeroHP/life causes persist.
- Willbreaker uses actual RefinedGaleSword, RefinedTideEnchantedArmor and FieldStoneTool records. Current equipment rules permit nonproficient worn-armor casting with+1RP; the prior Wizard9Wall therefore costs11RP32→21, not10. Passive armor remains; new deliberate item use is barred. Actual Ready release is not a new cast. Uncommitted Quicken child and already-committed midcast stack remain conditional, with no invented interrupt.
- Geas and MassSuggestion keep real30day/24hour clocks, safe fixed commands, real rest/work/resource limits and establishment-time hardreservation. One-day suppression remains explicitly conditional; concrete LesserAM is60seconds. No calendar/world-time reset or fictional labor is granted.
- Dance uses actual Haste extraFullAction, earlier Command arbitration, real Ready release before attached phase, actual Grapple and Lich/HoldMonster/Globe sources. Actual Lich sleep/fear/charm/Poisoned immunities do not include Paralyzed. MindFog/MassCharm/TerrorChain/GroupIllusion exact current cases distinguish source-local saves/admission/observer effects and shared real budgets.

## Boundaries and requested output

Give substantive source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED for each15 procedure and each13 question. Keep original scenario IDs and complete old text. For necessary changes supply full exact before/after pointer replacements against Current11; identify unresolved conditional source premises honestly. Review source-specific timings/roots/geometry/hardguard independently, not through a generic parent grant. Return downloadable REVIEW.json,VERDICT.md and corrections as needed. Do not accept unseen future integration mirrors.

The two full memory records WovenThreads and HazeofForgetting remain separately preserved for their permanent-memory/provenance/recovery conference. Creation is separate economy/crafting. Current counts480reviewed/368pending; accepted AC6/DE4 stay closed; all75 domain gates remain distinct. No new RNG/Fate disclosure item, global control/companion rule, runtime/human-playtest/balance/canon or release approval. Source preservation checks are not game executions.
''';(root/'README.md').write_text(readme,encoding='utf8',newline='\n')
 paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix());manifest={'id':'CONTROL15-CONFERENCE11','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(out),'files':[info(p) for p in paths],'counts':{'identities':15,'originalScenarioTexts':30,'currentScenarioRecords':30,'questions':13,'memoryIdentitiesExcluded':2},'conditionalBranchesAreNotFullyProvedGames':True,'authoredCounts':{'reviewed':480,'pending':368},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0};(root/'MANIFEST.json').write_bytes(encoded(manifest))
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in ['README.md','MANIFEST.json']:z.write(root/n,n)
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for b in manifest['files']:
   raw=z.read('files/'+b['path']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
 bind=info(zp);req.write_text(f'''Please conduct the full control15 source conference using DD_Control_15_Conference_11.zip ({bind['bytes']} bytes; SHA256 {bind['sha256']}). Read README.md, MANIFEST.json and Current11:15 full source/access/procedure records,30 preserved original/current scenario records,13 explicit questions,source-contract routing,all full current/old sources and actual accepted interfaces.

Review each procedure/question substantively, particularly operative CR/native-profile gaps, companion ability-check limits and finite phase routing, MentalPrison entry/exit roots/replacement, specific sleep/wake/harm predicates, deliberate Willbreaker item use/current armor prices/Ready, safe long commands/rest/work caps and distinct actual hardguards. Conditional original source premises remain labeled, not erased or described as executed games. WovenThreads/HazeofForgetting, Creation and pending TrueSeeing stay separate. Do not silently supply monster attackreach,CR,companion extraAction or a generic Fate disclosure.

Return source-linked AGREE/AGREE_WITH_SCOPED_AUTHORSHIP/CHANGE_REQUIRED with downloadable REVIEW.json,VERDICT.md and exact complete pointer replacements. Preserve originals/class-school access/history. Accepted AC6/DE4 and480/368counts remain closed/unchanged; no unseen-mirror acceptance, runtime/human balance/cosmology/full75-domain/release approval.''',encoding='utf8',newline='\n')
 prep.write_bytes(encoded({'archive':bind,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'request':info(req),'checks':info(checkp),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared UNSENT; persistent20 actual conference active. Conditional source dependencies remain explicit.','newRuleAdoptions':0,'runtimeTestsExecuted':0}));print(json.dumps(read(prep)))
if __name__=='__main__':main()
