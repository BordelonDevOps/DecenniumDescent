"""Prepare complete companion exact candidate with frozen historical/current authorities."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from package_damage_control25_exact_09 import render,strings

def read(p):return json.loads(p.read_bytes())
def binding(path,raw):return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
 root=A/'companion-life10-exact-05';zp=A/'DD_Companion_Life_10_Exact_05.zip';prep=A/'COMPANION_LIFE_10_EXACT_05_PREPARATION.json';checkp=A/'COMPANION_LIFE_10_EXACT_05_CHECK.json';request=A/'COMPANION_LIFE_10_EXACT_05_REQUEST.txt'
 assert not any(p.exists() for p in [root,zp,prep,checkp,request])
 source=R/'data/director/spell_proposals/companion_life_10_current_05.json';d=read(source);layer=d['current04ReviewProposedLayer'];reviewp=A/'companion-life10-current04-review/REVIEW.json';review=read(reviewp);receipt=A/'COMPANION_LIFE_10_CURRENT_04_RETURN_RECEIPT.json';replayp=A/'COMPANION_LIFE_10_CURRENT_05_REPLAY_CHECK.json';replay=read(replayp);checks=[];buffers={};sources={};historical={}
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def put(n,raw):assert n not in buffers;buffers[n]=raw
 def planned(n):return {'name':n,'bytes':len(buffers[n]),'sha256':hashlib.sha256(buffers[n]).hexdigest()}
 def include(p):
  path=p.relative_to(G).as_posix();raw=p.read_bytes()
  if path in sources:ck('Same current source '+path,sources[path]==raw)
  sources[path]=raw;return binding(path,raw)
 ck('Exact nine-operation replay candidate',info(source)==replay['candidate'] and replay['failures']==0 and replay['operations']==9 and replay['checkCount']==308)
 ck('Actual final identified',read(receipt)['actualAssistantMessageId']=='a3ef8d40-93f2-475d-b8af-9eed34023d60')
 with zipfile.ZipFile(A/'DD_Companion_Life_10_Current_04_Draft.zip') as z:
  oldmanifest=json.loads(z.read('MANIFEST.json'));ck('63 complete historical authorities',len(oldmanifest['files'])==63)
  for b in oldmanifest['files']:
   raw=z.read(b['archivePath']);ck('Original archive bytes '+b['path'],binding(b['path'],raw)=={k:b[k] for k in ['path','bytes','sha256']});historical[b['path']]=raw
 ck('All56 previous nested sources remain exact',all(binding(b['path'],historical[b['path']])==b for b in d['sourceBindings']+d['newSourceBindings']))
 for path,raw in historical.items():include(G/path)
 indexp=R/'data/public/spell_playtests/authored_review_index.json';index=read(indexp);oldindex=json.loads(historical[indexp.relative_to(G).as_posix()]);byid={s['id']:s for s in index['entries']};oldbyid={s['id']:s for s in oldindex['entries']};catp=R/'data/public/spell_playtests/catalog.json';cat={s['id']:s for s in read(catp)['spells']}
 ids=[s['spellId'] for s in d['records']];ck('Ten unique pending identities',len(ids)==len(set(ids))==10 and all('pending' in byid[i]['authoredStatus'] for i in ids))
 ck('Current525/323/249 baseline',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249)
 for s in d['records']:ck('Unchanged complete source/access '+s['spellId'],s['completeSourceAndAccess']==cat[s['spellId']] and byid[s['spellId']]==oldbyid[s['spellId']])
 changed=[i for i in byid if byid[i]!=oldbyid[i]];ctx=read(A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01.json');applications=deepcopy(ctx['acceptedApplications']);acceptedids=[]
 for app in applications:
  p=G/app['source']['path'];ck('Exact actual application receipt '+p.name,info(p)==app['source'] and read(p)==app['completeReceipt']);include(p)
  for k in ['acceptanceAuthority','actualNativeFinal','applicationCheck']:
   ref=app['completeReceipt'].get(k)
   if isinstance(ref,dict) and 'path' in ref:ck('Actual accepted evidence '+k,info(G/ref['path'])==ref);include(G/ref['path'])
 # Accepted complete current procedures are supplied without rewriting the preserved pending comparisons.
 p20p=R/'data/public/spell_candidates/persistent_damage_20_reviewed_07.json';p20=read(p20p);dc25p=R/'data/public/spell_candidates/damage_control_25_reviewed_10.json';dc25=read(dc25p)
 acceptedids=[s['id'] for m in [p20,dc25] for s in m['spells']]
 ck('Exactly45 actual accepted membership differences',len(changed)==45 and set(changed)==set(acceptedids))
 for p in [p20p,dc25p,R/'data/playtest/spell_candidates/persistent_damage_20_cases_07.json',R/'data/playtest/spell_candidates/damage_control_25_cases_10.json',R/'docs/spells/candidates/PERSISTENT_DAMAGE_20_REVIEWED_07.md',R/'docs/spells/candidates/DAMAGE_CONTROL_25_REVIEWED_10.md',R/'docs/director-only/spells/PERSISTENT_DAMAGE_20_REVIEWED_07.md',R/'docs/director-only/spells/DAMAGE_CONTROL_25_REVIEWED_10.md']:
  include(p)
 regp=R/'data/director/spell_review/accepted_interface_registry_06.json';reg=read(regp);oldreg=read(R/'data/director/spell_review/accepted_interface_registry_04.json');ck('All108 former interfaces unchanged in173 current entries',len(oldreg['entries'])==108 and len(reg['entries'])==173 and reg['entries'][:108]==oldreg['entries'])
 counterpart=[]
 for sid in ['enervation','leeching-plague']:
  n=next(n for n,s in enumerate(p20['spells']) if s['id']==sid);counterpart.append({'spellId':sid,'source':info(p20p),'pointer':'/spells/'+str(n),'completeCurrentCard':deepcopy(p20['spells'][n]),'completeSharedRules':deepcopy(p20['sharedRules']),'currentIndexEntry':deepcopy(byid[sid]),'historicalRouting':'The complete previous pending comparison remains untouched. This accepted exact07 card and its named shared rules now govern current operative use. No inherited spell-specific exception becomes a general rule.'})
 missingp=R/'data/director/spell_proposals/enchantment_illusion_rank5.json';missing=include(missingp);ck('Supplemental historical Dominate Monster pointer exists',at(read(missingp),'/records/0') is not None)
 searchp=A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_01.json';search=read(searchp)
 for b in search['frozenSources']:
  p=G/b['frozenCopy'];raw=p.read_bytes();ck('Bounded bestiary original bytes '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']);include(p)
 for p in [source,reviewp,receipt,replayp,searchp,regp,catp,indexp,R/'data/director/spell_review/ordinary_spell_inventory_05.json',A/'COMPANION_LIFE_10_CURRENT_05_PROPOSAL_APPLICATION.json',A/'COMPANION_LIFE_10_CURRENT_04_ACTUAL_GPT_FINAL.json',R/'tools/apply_companion_current04_to_draft05.py',R/'tools/package_companion10_exact_05.py',R/'tools/audit_command_undeath_target_sources_01.py']:
  include(p)
 for p in (A/'companion-life10-current04-review').iterdir():
  if p.is_file():include(p)
 drift=[{'path':p,'frozen':binding(p,b),'current':binding(p,sources[p]),'meaning':'Only actual accepted45 membership/index progress. No source/access or operative rule is replaced.'} for p,b in historical.items() if sources[p]!=b]
 ck('Only frozen index drift',len(drift)==1 and drift[0]['path']==indexp.relative_to(G).as_posix())
 convergence={'historicalArchive':info(A/'DD_Companion_Life_10_Current_04_Draft.zip'),'frozenSourceCount':63,'nestedBindingsRetained':56,'currentIndex':info(indexp),'previousCounts':oldindex['authoredCounts'],'currentCounts':index['authoredCounts'],'currentRepresentationCounts':index['representationCounts'],'completeMembershipChanges':[{'id':i,'before':oldbyid[i],'after':byid[i]} for i in changed],'actualApplications':applications,'currentRegistry':info(regp),'registryPrefixUnchanged':108,'registryEntries':173,'sourceDrift':drift,'currentAcceptedCounterparts':counterpart,'dominateMonsterHistoricalBacklink':{'originalReviewLimitationUnchanged':deepcopy(review['verificationLimitations']),'supplementalRawSource':missing,'pointer':'/records/0','scope':'Historical-only raw backlink now supplied; this does not retroactively change what Current04 reviewed. Dominate Monster remains pending, grants no operative capability and does not solve CR2.'},'boundedCR2Search':info(searchp),'searchLimitation':'Eleven preserved JSON sources, nine parseable and two already-truncated historical JSONs; zero exactCR2 Undead in the parseable subset. Not a whole repository/workbook/DOCX absence claim; no new NPC rating is assigned.'}
 selectors={s['spellId']:s['pointer'] for s in layer['currentProcedureSelection']};spells=[]
 for s in d['records']:
  rec=deepcopy(s);rec['id']=s['spellId'];rec['name']=s['completeSourceAndAccess']['name'];rec['procedure']=at(d,selectors[s['spellId']]);rec['selectedProcedureSource']={'candidate':info(source),'pointer':selectors[s['spellId']]};spells.append(rec)
 cases=deepcopy(d['currentCases']);originals=deepcopy(d['completePreservedAppliedLayer']['all20HistoricalScenarioTexts']);ck('27 main and38 branches',len(cases)==len({c['id'] for c in cases})==27 and sum(len(c.get('independentBranches',[])) for c in cases)==38);ck('20 preserved original obligations',len(originals)==len(d['originalObligationCoverage'])==20)
 limits={'wholeCaseContentHolds':deepcopy(layer['wholeCaseContentHolds']),'nextContentReviewRequirement':layer['nextContentReviewRequirement'],'conditionalAuthoredAcceptanceMeaning':'A coherent procedure may be accepted with missing concrete content explicitly held. This is not a fulfilled positive scenario, creature rating, implemented fallback, executable feature or whole-game completion. Do not silently count either held case as complete.','fullyApprovedCurrentCases':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'numericalBalanceApproved':False,'cosmologyCanonModified':False,'domainGatesDistinct':75,'sourceInformationDeleted':0}
 model={'schemaVersion':'1.0','moduleId':'COMPANION-LIFE10-EXACT05','status':'PENDING exact authored acceptance; video game only','candidate':info(source),'spells':spells,'sharedRules':deepcopy(d['sharedRules']),'newScopedRules':deepcopy(layer['newScopedRules']),'actualConferenceReview':info(reviewp),'actualConferenceReceipt':info(receipt),'actualPerSpellDispositions':deepcopy(review['perSpellDispositions']),'actualClarificationDispositions':deepcopy(review['clarificationDispositions']),'codexConcurrenceForDrafting':deepcopy(d['current04ConferenceApplication05']['codexConcurrence']),'currentSourceConvergence':convergence,'authorityRouting':'Only each spells[].procedure is the selected complete current procedure. The named six shared rules and four scoped new rules accompany it. Complete earlier procedures, statuses, pending questions and cases remain historical evidence; the selectors and actual dispositions identify the current choice. No source-only class/access object supplies absent runtime content.','contentLimits':limits,'runtimeSelectionEnabled':False,'runtimeImplemented':False,'newRuleAdoptions':0,'sourceInformationDeleted':0}
 casebook={'schemaVersion':'1.0','id':'COMPANION-LIFE10-CASEBOOK05','status':'Pending exact authored acceptance with two explicit whole-case content holds; zero executed runtime tests','cases':cases,'originalScenarioTextsUnchanged':originals,'originalObligationCoverageUnchanged':deepcopy(d['originalObligationCoverage']),'completeActualCurrent04CaseReview':read(A/'companion-life10-current04-review/CASE_REVIEW.json'),'completeReversibleApplication':deepcopy(d['current04ConferenceApplication05']),'caseCounts':deepcopy(d['caseCounts']),'contentLimits':limits,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 base='# Companion and life spells — proposed video game rules\n\n**Pending exact authored acceptance.** Ten existing spell identities retain their full source and class access. Each full procedure below is selected from Current05 after the actual GPT conference. Two Command Undeath cases need a separately reviewed exact CR 2 undead profile.\n\n## Shared procedures\n\n'+render(d['sharedRules'])+'## Four explicitly scoped conference choices\n\n'+render(layer['newScopedRules'])
 for s in spells:
  base+='## '+s['name']+'\n\n| Class | School | Rank | Minimum class level | Base RP |\n|---|---|---:|---:|---:|\n'
  for cl,x in s['completeSourceAndAccess']['classAccess'].items():base+=f"| {cl} | {x['school']} | {x['rank']} | {x['minimumClassLevel']} | {x['baseRpCost']} |\n"
  base+='\n'+s['procedure']+'\n\n'
 player=base+'## Content still required\n\nCommand Undeath requires an actual reviewed Undead creature with CR exactly 2. A lower CR, an unrated conjured profile or an assumed rating does not qualify. The two positive cases remain on hold. A separate native NPC profile and rating review is required. All other conditional fixture limits remain in the complete Director casebook.\n\nThese are proposed authored rules. Runtime implementation, human playtesting, numerical balance, cosmology and release remain separate.\n'
 director=base+'## Actual review decisions\n\n'+render(review['perSpellDispositions'])+render(review['clarificationDispositions'])+'## Current authority and source convergence\n\n'+render(convergence)+'## Case limits\n\n'+render(limits)+'## Complete current cases\n\n'
 for c in cases:director+='### '+c['id']+'\n\n```json\n'+json.dumps(c,ensure_ascii=False,indent=2)+'\n```\n\n'
 director+='## Twenty original scenarios, unchanged\n\n```json\n'+json.dumps(originals,ensure_ascii=False,indent=2)+'\n```\n'
 for n,chapter in [('PLAYER_CHAPTER.md',player),('DIRECTOR_REVIEW.md',director)]:
  for s in spells:ck('Full selected procedure '+n+' '+s['id'],s['procedure'] in chapter)
  for rules in [d['sharedRules'],layer['newScopedRules']]:
   for rid,rule in rules.items():ck('Full shared/scoped prose '+n+' '+rid,rule['completeText'] in chapter)
 pointerchecks=[]
 def walk(v,path):
  if isinstance(v,dict):
   if isinstance(v.get('path'),str) and isinstance(v.get('pointer'),str) and v['pointer'].startswith('/'):
    ref=v['path'];p=G/ref
    if p.is_file() and p.suffix.lower()=='.json':at(read(p),v['pointer']);include(p);pointerchecks.append({'object':path,'sourcePath':ref,'pointer':v['pointer']})
   for k,x in v.items():
    if k not in ['previousCurrent04Version','completeHistoricalRecordUnchanged']:walk(x,path+'/'+k)
  elif isinstance(v,list):
   for n,x in enumerate(v):walk(x,path+'/'+str(n))
 for c in cases:walk(c,'currentCases/'+c['id'])
 walk(layer['newScopedRules'],'newScopedRules')
 put('SPELLS_MODEL.json',encoded(model));put('CASEBOOK.json',encoded(casebook));put('PLAYER_CHAPTER.md',player.encode());put('DIRECTOR_REVIEW.md',director.encode())
 put('SOURCE_HASHES.json',encoded({'id':'COMPANION-LIFE10-SOURCES05','currentSources':[dict(binding(p,raw),archivePath='sources/'+p) for p,raw in sorted(sources.items())],'frozenCurrent04Sources':[dict(binding(p,raw),archivePath='historical-current04/'+p) for p,raw in sorted(historical.items())],'sourceConvergence':convergence,'scope':'Complete raw historical and current sources supplied separately; historical review limitations remain preserved. No pending counterpart is approved through inclusion.'}))
 register={'id':'COMPANION-LIFE10-EXACT05-REGISTER','status':'PENDING actual exact authored acceptance','spellIds':ids,'placementCount':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in spells),'candidate':info(source),'mainCases':27,'independentSubbranches':38,'originalScenarios':20,'sharedRules':6,'newScopedRules':4,'replayedOperations':9,'contentLimits':limits,'applicationPlan':{'preconditions':'Actual GPT acceptance bound to all eight exact current files, with explicit per-spell and content-hold disposition. Independently validate current pending membership and preserved sources before copying any accepted files.','canonicalByteCopies':{'SPELLS_MODEL.json':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/companion_life_10_reviewed_05.json','CASEBOOK.json':'DescentReviewChanges/ReviewBible/data/playtest/spell_candidates/companion_life_10_cases_05.json','PLAYER_CHAPTER.md':'DescentReviewChanges/ReviewBible/docs/spells/candidates/COMPANION_LIFE_10_REVIEWED_05.md','DIRECTOR_REVIEW.md':'DescentReviewChanges/ReviewBible/docs/director-only/spells/COMPANION_LIFE_10_REVIEWED_05.md'},'membership':'Only identities explicitly accepted by actual GPT may gain authored-review membership. A full ten-identity bounded authored acceptance at the frozen525/323/249 baseline would produce535/313/259; this does not close either held case. Recompute against the actual live index at application, with separate transparent receipt; do not preapprove unseen future index/registry bytes.','runtimeSelectionEnabled':False,'unrelatedAuthoritiesUnchanged':True},'newRuleAdoptions':0,'sourceInformationDeleted':0}
 put('REGISTER.json',encoded(register))
 notes='''# Companion exact05 review notes

The actual Current04 assistant a3ef8d40-93f2-475d-b8af-9eed34023d60 returned nine full reversible operations. Current05 replays and reverses all nine, with308 passing source/hash/replay/arithmetic checks. Codex concurs for drafting with all four explicit new choices: Soulburn intrinsic recovery under Grand Reservoir, the wraith's two ordinary handling extremities, its generated body mass0lb, and the Ghast oral15ft circular cone. The Ready correction now distinguishes paid setup at5 from field establishment at6.1, nominal expiry66.1 and actual earlier ending13. There are no additional local semantic alterations in this exact rendering.

The model selects three appended full procedures and seven unchanged ones, carries all six shared rules and four scoped choices, and retains every source/history record.27 complete cases and38 independent subbranches include20 original obligations; one newly positive Soulburn/Reservoir branch coexists with the old zero-output comparator. All replaced case objects retain previousCurrent04Version. Both Command Undeath positive cases remain whole-case content holds; exactCR2 is not <=2 and no conjured profile acquires a rating.

The supplied bounded bestiary search covers11 preserved JSON sources, nine parseable and two already-truncated historical files. No exactCR2 Undead exists in that parseable subset. This is not a whole archive absence claim. A separate full native NPC and rating review remains necessary. No NPC is invented here.

The original63-source archive remains byte-identical in historical-current04/. Current source copies are separate. Only the old480/368 authored index changed, by exactly45 actual accepted DamageControl25/Persistent20 identities, to525/323/249. All ten current pending entries are identical. All108 earlier registry entries remain unchanged in the173-entry registry06. Complete current accepted Enervation and Leeching Plague cards and their source-specific shared rules are included; the prior pending counterparts remain historical. The missing historical Dominate Monster raw backlink is now supplied separately, without changing the previous review's limitation or accepting Dominate Monster.

Review all eight current artifacts and their full rule/source flow. If coherent, return exact bounded authored acceptance with individual spell dispositions and explicit preservation of the two whole-case holds. Otherwise return minimal full before/after corrections with exact pointers. Authored acceptance must not imply runtime implementation/testing, actual gameplay, balance, cosmology, final release, future unseen payloads or closure of any of the75 independent domain gates.
'''
 put('LOCAL_REVIEW_NOTES.md',notes.encode());put('EVIDENCE_MANIFEST.json',encoded({'id':'COMPANION-LIFE10-EXACT05-MANIFEST','files':[planned(n) for n in sorted(buffers)],'selfHashConvention':'Seven companion files bound here; outer preparation binds this eighth manifest.','pendingActualExactAcceptance':True}))
 ck('Eight exact files',len(buffers)==8)
 root.mkdir()
 for n,raw in buffers.items():(root/n).write_bytes(raw)
 checkp.write_bytes(encoded({'candidate':info(source),'checks':checks,'checkCount':len(checks),'failureCount':0,'currentSourceCount':len(sources),'frozenSourceCount':len(historical),'currentSourcePointerChecks':pointerchecks,'currentSourcePointerCount':len(pointerchecks),'mainCases':27,'independentSubbranches':38,'wholeCaseContentHolds':2,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
 readme='Read current/REGISTER.json and LOCAL_REVIEW_NOTES.md, then the complete model, casebook and both chapters. Review eight exact current artifacts. Historical source bytes are under historical-current04/; complete current source bytes under sources/. Command Undeath retains two explicit whole-case holds. No pending NPC or counterpart is approved by inclusion.\n';(root/'README.md').write_text(readme,encoding='utf8',newline='\n')
 with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(root/'README.md','README.md');z.write(checkp,'LOCAL_ARTIFACT_CHECK.json')
  for n,raw in sorted(buffers.items()):z.writestr('current/'+n,raw)
  for p,raw in sorted(sources.items()):z.writestr('sources/'+p,raw)
  for p,raw in sorted(historical.items()):z.writestr('historical-current04/'+p,raw)
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for n,raw in buffers.items():assert z.read('current/'+n)==raw
  for p,raw in sources.items():assert z.read('sources/'+p)==raw
  for p,raw in historical.items():assert z.read('historical-current04/'+p)==raw
 b=info(zp);request.write_text(f'Please review {zp.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}) for exact bounded authored acceptance. Your actual Current04 nine operations replay/reverse exactly; Codex concurs with all four scoped choices and Ready correction. Ten full selected procedures, six shared/four new scoped rules,20 original scenarios,27 current main cases and38 independent branches are supplied in eight complete artifacts. No further semantic alterations. Preserve two Command Undeath exactCR2 whole-case holds; the bounded11-JSON search is not whole-archive absence and authors no NPC. Frozen63 sources plus current accepted45/index525/323/249 and registry173 context are fully supplied. Current Enervation/Leeching Plague exact07 authorities govern; original comparisons remain history. Historical Dominate Monster raw backlink is separately supplied and remains pending. If coherent return ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_COMPANION_LIFE10_VIDEO_GAME_CANDIDATE_WITH_CONTENT_HOLDS with each exact eight filename/bytes/SHA256, ten individual spell dispositions, and explicit two-case holds. Otherwise complete minimal before/after corrections with exact pointers. No unseen future integration, runtime, human playtest, balance, cosmology,75-domain closure or release approval.\n',encoding='utf8',newline='\n')
 prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Prepared UNSENT; actual Illusion14 Current12 conference active','archive':b,'candidate':info(source),'currentFiles':[info(root/n) for n in sorted(buffers)],'artifactCheck':info(checkp),'request':info(request),'currentSourceCount':len(sources),'frozenSourceCount':len(historical),'allArchiveMembersVerified':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
 print(json.dumps({'archive':b,'preparation':info(prep),'checks':len(checks),'currentSources':len(sources),'frozenSources':len(historical),'pointers':len(pointerchecks),'exactFiles':len(buffers)}))

if __name__=='__main__':main()
