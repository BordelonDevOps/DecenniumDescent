"""Build full exact pending damage/control manuscripts, model, cases and frozen sources."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
def read(p):return json.loads(p.read_bytes())
def strings(x):
 if isinstance(x,str):yield x
 elif isinstance(x,dict):
  for v in x.values():yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
def render(x,depth=3):
 if isinstance(x,str):return x+'\n\n'
 if isinstance(x,dict):return ''.join('#'*min(depth,6)+' '+str(k)+'\n\n'+render(v,depth+1) for k,v in x.items())
 if isinstance(x,list):return ''.join(render(v,depth) for v in x)
 return json.dumps(x,ensure_ascii=False)+'\n\n'
def main():
 root=A/'damage-control25-exact-rebound-08';zp=A/'DD_Damage_Control_25_Exact_Rebound_08.zip';req=A/'DAMAGE_CONTROL_25_EXACT_REBOUND_08_REQUEST.txt';prep=A/'DAMAGE_CONTROL_25_EXACT_REBOUND_08_PREPARATION.json';checkp=A/'DAMAGE_CONTROL_25_EXACT_REBOUND_08_CHECK.json'
 assert not any(p.exists() for p in [root,zp,req,prep,checkp]);curp=R/'data/director/spell_proposals/damage_control_25_current_08.json';cur=read(curp);reviewp=A/'damage-control25-conference-07-review/REVIEW.json';review=read(reviewp);receipt=A/'DAMAGE_CONTROL_25_CONFERENCE_07_RECEIPT.json';checks=[];buffers={};now=datetime.now(timezone.utc).isoformat()
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def put(name,b):assert name not in buffers;buffers[name]=b
 def planned(name):return {'name':name,'bytes':len(buffers[name]),'sha256':hashlib.sha256(buffers[name]).hexdigest()}
 ids=[s['id'] for s in cur['spells']];ck('25 source identities',len(ids)==len(set(ids))==25)
 categories=['currentDigitalVectors','highRankCurrentVectors05','currentCases','mixedDefenseOptionVectors04','currentConferenceWorkedSupplements08'];cases=[deepcopy(c) for k in categories for c in cur[k]]
 ck('70 distinct records',len(cases)==len({c['id'] for c in cases})==70);ck('36 original current identities',[x['id'] for x in cur['currentDigitalVectors']]==[x['id'] for x in cur['originalCohortCasesUnchanged']])
 catalogp=R/'data/public/spell_playtests/catalog.json';catalog=read(catalogp);byid={s['id']:s for s in catalog['spells']}
 for s in cur['spells']:ck('Exact current source/access '+s['id'],s['completeSourceAndAccess']==byid[s['id']])
 model={'schemaVersion':'1.0','moduleId':'DAMAGE-CONTROL25-EXACT08','status':'PENDING exact authored review; video game only. No runtime selection or live adoption.','scope':'25 existing spell identities/26 printed placements. Full reviewed conference proposals plus explicitly identified local supplemental example corrections, pending final joint acceptance.','authorityBoundary':'Actual source/access records remain complete and unchanged; local NEW choices remain explicit. Accepted AC6/DE4/Fate scope is not broadened. Historical labels and original alternatives remain preserved evidence.','sharedRules':deepcopy(cur['sharedRules']),'spells':deepcopy(cur['spells']),'mixedDefenseOperatingOption':deepcopy(cur['mixedDefenseConferenceOption04']),'conferenceDecisions':deepcopy(cur['conferenceDecisions']),'actualConferenceReview':info(reviewp),'actualConferenceReceipt':info(receipt),'currentCandidate':info(curp),'codexDisposition':deepcopy(cur['codexConferenceDisposition08']),'originalScenarioTextsUnchanged':deepcopy(cur['originalCohortCasesUnchanged']),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'balanceApproved':False,'cosmologyCanonModified':False,'sourceInformationDeleted':0}
 cb={'schemaVersion':'1.0','id':'DAMAGE-CONTROL25-CASEBOOK08','status':'PENDING exact authored review; these are scenario records, not70executed games.','cases':cases,'caseCategories':[{'sourceArray':k,'count':len(cur[k]),'ids':[c['id'] for c in cur[k]],'coverage':'Seven of currentCases are raw-arithmetic-only fixtures; source-qualified inputs/conditional branches remain explicitly limited. Overlapping purposes are not independent runtime trials.'} for k in categories],'historicalOriginalTexts':deepcopy(cur['originalCohortCasesUnchanged']),'historicalCurrent01Cases':deepcopy(cur['previousCurrent01CasesUnchanged']),'directorProposedWorkedSupplementsUnchanged':deepcopy(cur['directorProposedWorkedSupplementsUnchanged']),'codexSupplementCorrectionsPending':deepcopy(cur['codexConferenceSupplementCorrections08']),'existingChangedBeforeValues':deepcopy(cur['conference07ChangedBeforeValues']),'caseSourceReferenceAliases':{'SPELLS_MODEL.json':'current/SPELLS_MODEL.json','CASEBOOK.json':'current/CASEBOOK.json','REGISTER.json':'current/REGISTER.json'},'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}
 base='# Damage and control spells — proposed video game rules\n\n**Pending exact authored review.** These25 spell identities preserve their original class/school/rank access. NEW choices are explicit and apply only to their named source. Use the full shared procedures and the spell together. This is an authored candidate, not implemented or balance-certified gameplay.\n\n## Shared operating rules\n\n'+render(model['sharedRules'])+'## Complete spell procedures\n\n'
 for s in model['spells']:
  base+='## '+s['name']+' — '+s['id']+'\n\n| Actual class | School | Rank | Minimum class level | Base RP |\n|---|---|---:|---:|---:|\n'
  for cl,a in s['completeSourceAndAccess']['classAccess'].items():base+=f"| {cl} | {a['school']} | {a['rank']} | {a['minimumClassLevel']} | {a['baseRpCost']} |\n"
  base+='\n'+render(s['procedure'],3)
  base+='### Explicit new authorship\n\n'+render(s.get('newAuthorship',s.get('procedure',{}).get('new','See the explicitly NEW fields above.')),4)
 player=base+'## Scope and review status\n\nAll original sources, alternatives and scenarios remain preserved in the complete source package. Conditional dependencies grant no missing capability. Runtime, human gameplay, balance, cosmology and final release remain separate.\n'
 director=base+'## Review decisions and pending local corrections\n\n'+render(cur['codexConferenceDisposition08'])+render(cur['codexConferenceSupplementCorrections08'])+'## Full authored scenario records\n\n'
 for c in cases:director+='### '+c['id']+'\n\n```json\n'+json.dumps(c,ensure_ascii=False,indent=2)+'\n```\n\n'
 director+='## Preserved original scenario texts\n\n'+''.join('### '+c['id']+'\n\n'+c['originalText']+'\n\n' for c in cur['originalCohortCasesUnchanged'])
 for label,chapter in [('PLAYER_CHAPTER.md',player),('DIRECTOR_REVIEW.md',director)]:
  for s in model['spells']:
   for j,leaf in enumerate(strings(s['procedure'])):ck('Full procedure '+label+' '+s['id']+'/'+str(j),leaf in chapter)
  for key,rule in model['sharedRules'].items():
   for j,leaf in enumerate(strings(rule)):ck('Full shared '+label+' '+key+'/'+str(j),leaf in chapter)
 put('SPELLS_MODEL.json',encoded(model));put('CASEBOOK.json',encoded(cb));put('PLAYER_CHAPTER.md',player.encode('utf8'));put('DIRECTOR_REVIEW.md',director.encode('utf8'))
 paths={curp,catalogp,receipt,reviewp,A/'DAMAGE_CONTROL_25_REBOUND_08_CHECK.json',R/'data/public/spell_playtests/authored_review_index.json',R/'tools/prepare_damage_control25_rebound_08.py',R/'tools/package_damage_control25_exact_08.py'}
 for b in cur['sourceBindings']:
  p=G/b['path'];ck('Exact current complete source '+b['path'],info(p)==b);paths.add(p)
 def bindings(x):
  if isinstance(x,dict):
   if all(k in x for k in ['path','bytes','sha256']):yield {k:x[k] for k in ['path','bytes','sha256']}
   for v in x.values():yield from bindings(v)
  elif isinstance(x,list):
   for v in x:yield from bindings(v)
 reg=read(R/'data/director/spell_review/accepted_interface_registry_04.json')
 for e in reg['entries']:
  for b in bindings({'current':e['currentAuthoritativeSource'],'acceptance':e['acceptanceBasis']}):
   p=G/b['path'];ck('Exact registry authority '+b['path'],info(p)==b);paths.add(p)
 # Validate every actual source pointer in current case records; no renderer/cursor is treated as authority.
 pointer_checks=[]
 for c in cases:
  def walk(x,where=''):
   if isinstance(x,dict):
    if isinstance(x.get('path'),str) and isinstance(x.get('pointer'),str) and x['pointer'].startswith('/'):
     p=G/x['path']
     if p.is_file() and p.suffix.lower()=='.json':
      value=at(read(p),x['pointer']);pointer_checks.append({'caseId':c['id'],'at':where,'path':x['path'],'pointer':x['pointer'],'resolved':True});paths.add(p)
    for k,v in x.items():walk(v,where+'/'+k)
   elif isinstance(x,list):
    for j,v in enumerate(x):walk(v,where+'/'+str(j))
  walk(c)
 put('SOURCE_HASHES.json',encoded({'bindings':[info(p) for p in sorted(paths,key=lambda p:p.relative_to(G).as_posix())],'scope':'Whole raw bytes; historical input records remain exact. No supplied executable needs to run in GPT review.'}))
 register={'schemaVersion':'1.0','id':'DAMAGE-CONTROL25-EXACT08-REGISTER','status':'PENDING exact joint acceptance; no current index membership change.','spellIds':ids,'placementCount':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in cur['spells']),'originalScenarioTexts':36,'currentScenarioRecords':70,'existingCurrentRecords':64,'additionalConferenceSupplements':6,'actualConferenceReview':info(reviewp),'currentCandidate':info(curp),'sourceCount':len(paths),'caseCategories':cb['caseCategories'],'pendingCodexCorrections':['DC25-P01: Wizard11 CON14 fixedHP68→53 after15 damage.','DC25-P02: actual vertical x=3.75 cut of x[0,5] slab gives both75/25area and volume.','DC25-P04: Wizard9 CON14 fixedHP56→41→25 and actual automaticCounterspell atWizard2; Orb caster Abjuration specialization explicit.'],'applicationPlan':{'preconditions':'Actual GPT exact acceptance of this full supplied file set, followed by independent byte/preservation verification. No acceptance receipt invented now.','canonicalByteCopies':{'SPELLS_MODEL.json':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/damage_control_25_reviewed_08.json','CASEBOOK.json':'DescentReviewChanges/ReviewBible/data/playtest/spell_candidates/damage_control_25_cases_08.json','PLAYER_CHAPTER.md':'DescentReviewChanges/ReviewBible/docs/spells/candidates/DAMAGE_CONTROL_25_REVIEWED_08.md','DIRECTOR_REVIEW.md':'DescentReviewChanges/ReviewBible/docs/director-only/spells/DAMAGE_CONTROL_25_REVIEWED_08.md'},'laterMembershipOnly':'Only after real acceptance:25pending identities point to the exact standalone model; expected505reviewed/343pending/229standalone. Preserve848identityorder/sourcecatalog. No sourcecatalog rewrite or acceptedguide change is proposed. Refresh registry/discovery and any active procedural dependencies separately with actual evidence.','currentCounts':{'reviewed':480,'pending':368,'standalone':204},'runtimeSelectionEnabled':False},'scenarioCoverage':[{'originalId':o['id'],'spellId':o['spellId'],'exactOriginalText':o['originalText'],'currentCaseIndex':next(j for j,c in enumerate(cases) if c['id']==o['id'])} for o in cur['originalCohortCasesUnchanged']],'noSourceDeletion':True,'runtimeTestsExecuted':0}
 ck('26 placements',register['placementCount']==26);put('REGISTER.json',encoded(register))
 notes='''# Local exact review notes — pending

The actual final GPT conference is preserved in the230039-byte review archive and receipt. All23 complete before/after operations were independently replayed forward/reverse against exactCurrent07; Current08 preserves the full predecessor and changed before values. This package keeps all25source/access records,26placements,36originaltexts and64existingcurrentrecordidentities, including limited raw arithmetic/conditional fixtures. Six additional conference examples remain distinct.

The local current copies of three GPT supplements correct source-bound fixture details: Wizard11CON14fixedHP68→53, Wizard9CON14fixedHP56→41→25/automaticCounterspell ownership, and a specifically vertical ice cut before assigning75/25supportarea. Full original GPT versions are preserved unchanged in the casebook and Current08. Actual GPT concurrence is still required; these changes do not purport to be already accepted.

The model and both complete manuscripts carry identical current procedures/sharedrules. The Director manuscript adds all70currentrecords and36originaltexts. File/source/pointer/arithmetic verification is not gameplay. No live catalog, index, registry or source authority was changed; no acceptedAC6/DE4 reopening, global ice/mixed-defense rule or sixth Fate presentation. Separate pending cohorts and all75domain gates remain open at their actual status.
''';put('LOCAL_REVIEW_NOTES.md',notes.encode('utf8'))
 put('EVIDENCE_MANIFEST.json',encoded({'id':'DAMAGE-CONTROL25-EXACT08-MANIFEST','files':[planned(n) for n in sorted(buffers)],'selfHashConvention':'Seven companion files bound here; manifest itself is bound by outer archive/preparation.','pendingExactAcceptance':True}))
 root.mkdir()
 for n,b in buffers.items():(root/n).write_bytes(b)
 checkp.write_bytes(encoded({'candidate':info(curp),'checks':checks,'checkCount':len(checks),'failureCount':0,'resolvedCurrentCaseSourcePointers':pointer_checks,'sourcePointerCount':len(pointer_checks),'pendingLocalSupplementCorrections':3,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
 readme='''# Damage/control25 — exact rebound08

Read current/REGISTER.json, current/LOCAL_REVIEW_NOTES.md, current/SPELLS_MODEL.json, current/CASEBOOK.json and both full manuscripts. Current08 source is supplied under sources/. The actual final conference review/receipt and all exact sources/history are included; the preliminary analysis archive is not evidence.

Please retain settled scoped conference decisions and review the actual23replayed replacements plus3small source/geometry corrections to newly supplied supplements. Confirm all25procedures/sharedrules, exact manuscripts, source preservation,64retainedcurrentrecords+6supplements and application boundaries. No original36scenario was dropped. The source-qualified/conditional input distinctions remain material:70records do not mean70game executions.

If coherent, return exact bounded authored acceptance of the EIGHT current files, binding name/bytes/SHA256. Otherwise give minimal full exact before/after replacements with real file/pointers, preserving previous versions. The only subsequent planned live change is byte-identical canonical copies and separately verified25-membership discovery after acceptance; no sourcecatalog or acceptedAC6/DE4guide edits are requested here. Active dependency/registry refresh must preserve their own complete sources and cannot retroactively claim unseen byte acceptance.

Counts currently480/368/204standalone; expected505/343/229 only after actual acceptance/application. No runtime,human gameplay,balance,cosmology,75domain closure or release approval. Persistent20 is a separate active conference; illusion14/control15/Creation/memory remain outside this acceptance scope.
'''
 (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(root/'README.md','README.md');z.write(checkp,'LOCAL_ARTIFACT_CHECK.json')
  for n in sorted(buffers):z.write(root/n,'current/'+n)
  for p in sorted(paths,key=lambda p:p.relative_to(G).as_posix()):z.write(p,'sources/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for n,b in buffers.items():assert z.read('current/'+n)==b
  for p in paths:assert z.read('sources/'+p.relative_to(G).as_posix())==p.read_bytes()
 bind=info(zp);req.write_text(f'''Please review DD_Damage_Control_25_Exact_Rebound_08.zip ({bind['bytes']} bytes;SHA256 {bind['sha256']}) for bounded final authored acceptance. Your actual final conference assistant2c3a231c-f1f7-42b7-ae87-649bde455583 and230039-byte review are preserved. All23 complete proposed operations replay and reverse exactly; Current08 and these full files preserve25sourceidentities/26placements/36originaltexts/all64currentrecordIDs, plus6newconference supplements.

Read README.md and current/REGISTER.json. Three explicit local supplemental corrections need your concurrence: P01Wizard11CON14fixedHP68→53;P02vertical cut x=3.75 through the full0.75ft remaining slab, so area and volume both75/25;P04Wizard9CON14fixedHP56→41→25 and automaticCounterspellacquisitionat2,plusOrb casterAbjurationspecialization. Complete original GPT supplement objects remain unchanged in history. All23proposed rule changes remain exact; no source oracceptedAC6/DE4 was rewritten.

Please verify the EIGHT current full artifacts/model/casebook/manuscripts/sourcebindings and scoped follow-through, preserving the previously agreed source decisions. If coherent, ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_DAMAGE_CONTROL25_VIDEO_GAME_CANDIDATE, binding each actual filename/bytes/SHA256; otherwise supply minimal exact full replacements. Do not serialize unchanged files. Current480/368 and204standalone stay unchanged until actual later25-membership application. No runtime/gameplay/balance/cosmology/full75domain/release or othercohort approval.''',encoding='utf8',newline='\n')
 prep.write_bytes(encoded({'archive':bind,'candidate':info(curp),'currentFiles':[info(root/n) for n in sorted(buffers)],'sourceCount':len(paths),'artifactCheck':info(checkp),'request':info(req),'allArchiveMembersVerified':True,'status':'Prepared UNSENT; persistent20 actual review active. Await next substantive conference opportunity.','newRuleAdoptions':0,'runtimeTestsExecuted':0}));print(json.dumps({'archive':bind,'currentFiles':len(buffers),'sources':len(paths),'checks':len(checks),'sourcePointers':len(pointer_checks),'preparation':info(prep)}))
if __name__=='__main__':main()
