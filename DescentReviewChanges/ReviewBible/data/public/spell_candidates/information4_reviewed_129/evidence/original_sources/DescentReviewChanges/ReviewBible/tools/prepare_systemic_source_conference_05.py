"""Shared preservation/preflight for source conferences; never promotes a spell."""
from copy import deepcopy
from datetime import datetime,timezone
import json,zipfile
from pathlib import Path
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def prepare(*,slug,stem,title,ids,questions,findings,extra_sources,registry_entries,counterparts,caller,readme,arithmetic):
    out=R/f'data/director/spell_review/{slug}_conference_01.json';root=A/f'{slug.replace("_", "-")}-conference-01';check=A/f'{stem}_CONFERENCE_01_CHECK.json';archive=A/f'DD_{title.replace(" ", "_")}_Conference_01.zip';req=A/f'{stem}_CONFERENCE_01_REQUEST.txt';prep=A/f'{stem}_CONFERENCE_01_PREPARATION.json'
    assert all(not p.exists() for p in [out,root,check,archive,req,prep]);sources={};checks=[]
    def read(p):return json.loads(p.read_bytes())
    def bind(p):
        b=info(p);sources[b['path']]=b;return b
    def ck(label,v):
        checks.append({'check':label,'passed':bool(v)});assert v,label
    qp=R/'data/director/spell_review/remaining_work_queue_09.json';cp=R/'data/public/spell_playtests/catalog.json';ip=R/'data/public/spell_playtests/authored_review_index.json';rp=R/'data/director/spell_review/accepted_interface_registry_05.json';queue,catalog,index,reg=map(read,[qp,cp,ip,rp])
    for p in [qp,cp,ip,rp,Path(__file__),Path(caller),R/'data/public/class_playtests/wizard.json',R/'data/public/class_playtests/cleric.json',R/'data/public/expedition_candidate/complete_candidate.json']+extra_sources:bind(p)
    records=[];shared={};cases=[]
    for ident in ids:
        row=next(r for r in queue['rows'] if r['id']==ident);ck('Not already queued '+ident,row['currentGroup'] is None);prior=row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'][0];p=G/prior['source']['path'];ck('Full original source '+ident,bind(p)==prior['source']);doc=read(p);rec=at(doc,prior['recordPointer']);card=next(s for s in catalog['spells'] if s['id']==ident);entry=next(e for e in index['entries'] if e['id']==ident)
        ck('Full procedure '+ident,rec['spellId']==ident and len(rec['procedure'])>100);ck('Current source/access '+ident,rec['fullSourceAndCurrentAccessRecord']==card);ck('Pending identity '+ident,entry['authoredStatus']=='pending-authored-procedure')
        records.append({'spellId':ident,'source':info(p),'pointer':prior['recordPointer'],'completeOriginalRecordUnchanged':deepcopy(rec),'completeCurrentCatalogSourceAndAccess':deepcopy(card),'indexEntry':deepcopy(entry),'riskTier':'C','status':'Earlier full proposal; unadopted.'});shared[str(p)]={'source':info(p),'completeOriginalSharedProposalUnchanged':deepcopy(doc['sharedProposal']),'completeOriginalJointIssuesUnchanged':deepcopy(doc['explicitJointIssues'])}
        for n,t in enumerate(rec['workedCases']):cases.append({'id':t.split(':',1)[0],'spellId':ident,'originalTextUnchanged':t,'source':info(p),'pointer':prior['recordPointer']+f'/workedCases/{n}'})
        for key in ['catalog','core']:ck('Underlying '+key+' '+ident,bind(R/card['source'][key+'Path'])['sha256']==card['source'][key+'Sha256'])
    inherited=[]
    for n in registry_entries:
        e=reg['entries'][n];b=e['currentAuthoritativeSource'];a=bind(G/b['path']);ck('Accepted authority '+str(n),a['bytes']==b['bytes'] and a['sha256']==b['sha256']);inherited.append({'registryPointer':f'/entries/{n}','completeEntryUnchanged':deepcopy(e),'scopeLimit':'Exact accepted scope only; no new application by analogy.'})
    cards=[]
    for ident in counterparts:
        entry=next(e for e in index['entries'] if e['id']==ident);ck('Reviewed counterpart '+ident,entry['authoredStatus']=='reviewed-authored-operational-playtest');p=(ip.parent/entry['procedureFile']).resolve();doc=read(p);ptr=entry.get('wholeCardPointer',entry['procedurePointer']);cards.append({'spellId':ident,'source':bind(p),'pointer':ptr,'completeCurrentCard':deepcopy(at(doc,ptr)),'completeSharedRules':deepcopy(doc.get('sharedRules',{})),'indexEntry':deepcopy(entry)})
    qs=[{'id':qid,'spellIds':which,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for qid,which,src,opts,rec in questions]
    ck('Unique pending identities',len(records)==len(set(ids)));ck('Two preserved original cases each',len(cases)==len({c['id'] for c in cases})==len(ids)*2);ck('Unique questions',len(qs)==len({q['id'] for q in qs}));ck('Question identity coverage',set().union(*(set(q['spellIds']) for q in qs))==set(ids));ck('Counts unchanged',index['authoredCounts']=={'reviewed':505,'pending':343})
    for label,v in arithmetic:ck(label,v)
    root.mkdir();frozen=[]
    for b in sources.values():
        p=G/b['path'];ck('Source unchanged '+b['path'],info(p)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes());ck('Frozen byte equality '+b['path'],dst.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    result={'id':stem.replace('_','-')+'-CONFERENCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREAUTHORSHIP_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'allOriginalScenarios':cases,'completeOriginalSharedProposalsUnchanged':list(shared.values()),'sharedRouting':'Only actual source-specific rules apply. Complete old shared text remains historical evidence; current accepted source scopes and current class engine supersede obsolete baseline prose without deleting it.','currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':cards,'semanticDelta':[{'spellId':r['spellId'],'riskTier':'C','fullEarlierNewChoices':r['completeOriginalRecordUnchanged']['newChoices'],'genuineQuestionIds':[q['id'] for q in qs if r['spellId'] in q['spellIds']]} for r in records],'questions':qs,'findings':findings,'riskCounts':{'C':len(ids)},'currentVectors':[],'currentVectorScope':'Zero new complete encounters at this source-conference stage. Every original case is preserved as an obligation, including conditional/unsupplied prerequisites. After actual decisions, full source-qualified current cases and exact acceptance remain required.','sourceBindings':list(sources.values()),'countsUnchanged':{'reviewed':505,'pending':343},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'cosmologyDecisions':0,'sourceInformationDeleted':0}
    out.write_bytes(encoded(result));check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'fullProcedures':len(ids),'originalCases':len(cases),'newCurrentVectors':0,'questions':len(qs),'failures':0,'validationScope':'Exact sources/access/history/membership plus explicitly conditional arithmetic. No final semantic acceptance/runtime.'}));(root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}));(root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n in ['README.md','MANIFEST.json']:z.write(root/n,n)
        z.write(out,'CANDIDATE.json');z.write(check,'PREFLIGHT.json')
        for b in frozen:z.write(G/b['frozenCopy'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json')==out.read_bytes()
        for b in frozen:assert z.read('sources/'+b['path'])==(G/b['frozenCopy']).read_bytes()
    b=info(archive);req.write_text(f'Please conduct {title} preauthorship conference with {archive.name} ({b["bytes"]}bytes;SHA256 {b["sha256"]}). Read all{len(ids)} complete original procedures,{len(cases)} unchanged scenarios,{len(qs)} explicit questions and full sources. Zero new current encounter vectors are submitted. Resolve actual new local choices and inherited corrections before full current authorship. Preserve each original and every source-specific interface. Return downloadable complete per-spell/per-question dispositions and full source-linked proposed replacements with case-development requirements.505 reviewed/343 pending unchanged; no adoption/runtime/human/balance/cosmology/75-domain/whole-game closure.\n',encoding='utf8',newline='\n');prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'check':info(check),'request':info(req),'sourceCount':len(sources),'allArchiveSourcesVerified':True,'status':'Prepared UNSENT; actual GPT conference tracked separately.','newRuleAdoptions':0}));print(json.dumps({'archive':b,'candidate':info(out),'preparation':info(prep),'sources':len(sources),'checks':len(checks),'originalCases':len(cases),'questions':len(qs)}))
