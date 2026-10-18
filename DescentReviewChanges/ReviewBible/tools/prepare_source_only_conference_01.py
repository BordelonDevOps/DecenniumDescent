"""Shared immutable source-only conference builder; does not invent prior procedures/cases."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def prepare(*,slug,stem,title,ids,questions,original_path,extra_sources,registry_entries,counterparts,caller,findings):
 root=A/f'{slug.replace("_","-")}-conference-01';out=R/f'data/director/spell_review/{slug}_conference_01.json';check=A/f'{stem}_CONFERENCE_01_CHECK.json';archive=A/f'DD_{title.replace(" ","_")}_Conference_01.zip';req=A/f'{stem}_CONFERENCE_01_REQUEST.txt';prep=A/f'{stem}_CONFERENCE_01_PREPARATION.json'
 assert not any(p.exists() for p in [root,out,check,archive,req,prep]);sources={};checks=[]
 def read(p):return json.loads(p.read_bytes())
 def bind(p):
  b=info(p);sources[b['path']]=b;return b
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 qp=R/'data/director/spell_review/remaining_work_queue_10.json';cp=R/'data/public/spell_playtests/catalog.json';ip=cp.parent/'authored_review_index.json';rp=R/'data/director/spell_review/accepted_interface_registry_05.json'
 original,queue,catalog,index,registry=map(read,[original_path,qp,cp,ip,rp])
 for p in [original_path,qp,cp,ip,rp,Path(__file__),Path(caller),R/'rulebook_output.txt']+extra_sources:bind(p)
 booklines=(R/'rulebook_output.txt').read_text(encoding='utf-16').splitlines();records=[]
 for ident in ids:
  n=next(n for n,r in enumerate(original['selectedSpells']) if r['spellId']==ident);old=original['selectedSpells'][n];row=next(r for r in queue['rows'] if r['id']==ident);card=next(s for s in catalog['spells'] if s['id']==ident);entry=next(e for e in index['entries'] if e['id']==ident)
  ck('Source-only ungrouped '+ident,row['currentGroup'] is None and row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords']==[])
  ck('Original source card still current '+ident,old['fullSourceAndCurrentAccessRecord']==card)
  ck('Pending identity '+ident,entry['authoredStatus']=='pending-authored-procedure')
  for key in ['catalog','core']:ck('Full underlying '+key+' '+ident,bind(R/card['source'][key+'Path'])['sha256']==card['source'][key+'Sha256'])
  bb=[deepcopy(b) for b in original['currentBookBindings'] if b['spellId']==ident]
  ck('All printed placements bound '+ident,len(bb)==len(card['source']['original']['placements']))
  for b in bb:ck('Exact book line '+ident+' '+str(b['currentBookRow']['line']),booklines[b['currentBookRow']['line']-1]==b['currentBookRow']['exactText'])
  records.append({'spellId':ident,'source':info(original_path),'pointer':f'/selectedSpells/{n}','completeOriginalSourceQuestionUnchanged':deepcopy(old),'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'completeCurrentBookBindings':bb,'earlierCompleteProcedures':[],'earlierWorkedCases':[],'riskTier':'C','status':'Source question only; no earlier complete procedure or current case claimed.'})
 inherited=[]
 for n in registry_entries:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path']);ck('Accepted source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']));inherited.append({'registryPointer':f'/entries/{n}','completeEntryUnchanged':deepcopy(e),'scopeLimit':'Exact accepted scope only; any new spell-specific extension must be separately chosen.'})
 cards=[]
 for ident in counterparts:
  e=next(e for e in index['entries'] if e['id']==ident);ck('Reviewed counterpart '+ident,e['authoredStatus']=='reviewed-authored-operational-playtest');p=(ip.parent/e['procedureFile']).resolve();doc=read(p);ptr=e.get('wholeCardPointer',e['procedurePointer']);cards.append({'spellId':ident,'source':bind(p),'pointer':ptr,'completeCurrentCard':deepcopy(at(doc,ptr)),'completeSharedRules':deepcopy(doc.get('sharedRules',{})),'indexEntry':deepcopy(e)})
 qs=[{'id':qid,'spellIds':which,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for qid,which,src,opts,rec in questions]
 ck('Unique source identities',len(records)==len(set(ids)));ck('Unique questions',len(qs)==len({q['id'] for q in qs}));ck('All identities have questions',set().union(*(set(q['spellIds']) for q in qs))==set(ids));ck('Live membership baseline',index['authoredCounts']=={'reviewed':505,'pending':343});ck('143 current interfaces',len(registry['entries'])==143)
 result={'id':stem.replace('_','-')+'-CONFERENCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREAUTHORSHIP_SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'completeHistoricalCommonQuestionUnchanged':original['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':original['commonQuestionException'],'historicalSourcePacket':info(original_path),'historyScope':'Full earlier packet, other identities and stale historical hashes remain unchanged. Current exact bindings govern this conference.','currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':cards,'questions':qs,'findings':findings,'semanticDelta':[{'spellId':r['spellId'],'riskTier':'C','startingPoint':'Complete original source and source question only. No complete procedure or worked case exists in the audited prior authoring map.','genuineQuestionIds':[q['id'] for q in qs if r['spellId'] in q['spellIds']]} for r in records],'riskCounts':{'C':len(ids)},'originalWorkedCases':[],'currentVectors':[],'caseDevelopmentRequirement':'After actual GPT decisions, full current actors/access/resource/timing/occupied-body/counterpart fixtures and at least two substantive scenarios per spell, plus full branch coverage. Missing native creature/profile or topology remains a declared hold; no illustrative arithmetic is promoted to a complete encounter.','countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'cosmologyDecisions':0,'sourceInformationDeleted':0}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Source unchanged '+b['path'],info(p)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes());ck('Frozen byte equality '+b['path'],dst.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 out.write_bytes(encoded(result));check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':len(ids),'placements':sum(len(r['completeCurrentBookBindings']) for r in records),'fullEarlierProcedures':0,'originalWorkedCases':0,'newCurrentVectors':0,'questions':len(qs),'failures':0,'validationScope':'Source/access/book-binding/preservation checks only; no semantic acceptance/runtime.'}));(root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 (root/'README.md').write_text(f'# {title} source conference01\n\nRead all{len(ids)} complete source records/questions and{len(qs)} explicit new questions, the full accepted comparisons and frozen source files. There are ZERO earlier complete procedures or worked cases for this cohort in the audited authoring map. Return complete source-linked proposed procedures, per-question decisions and subsequent case-development requirements. Preserve all original school placements and each actual class access. New local choices remain provisional until current full cases and exact acceptance.505 reviewed/343 pending unchanged. No source deletion, global interface expansion, runtime/human/balance/cosmology or75-domain closure.\n',encoding='utf8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in ['README.md','MANIFEST.json']:z.write(root/name,name)
  z.write(out,'CANDIDATE.json');z.write(check,'PREFLIGHT.json')
  for b in frozen:z.write(G/b['frozenCopy'],'sources/'+b['path'])
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and z.read('CANDIDATE.json')==out.read_bytes()
  for b in frozen:assert z.read('sources/'+b['path'])==(G/b['frozenCopy']).read_bytes()
 b=info(archive);req.write_text(f'Please conduct {title} source conference with {archive.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}). Read all{len(ids)} complete original source records/questions,{len(qs)} genuine decisions and all current source files. No full prior procedure or worked case is claimed. Return full source-linked proposed procedures, per-question decisions and case requirements; no source deletion, adoption, runtime/human/balance/cosmology or whole-game closure.\n',encoding='utf8',newline='\n');prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'check':info(check),'request':info(req),'sourceCount':len(sources),'allArchiveSourcesVerified':True,'status':'Prepared UNSENT; actual GPT conference tracked separately.','newRuleAdoptions':0}));print(json.dumps({'archive':b,'candidate':info(out),'preparation':info(prep),'sources':len(sources),'checks':len(checks),'originalCases':0,'questions':len(qs)}))
