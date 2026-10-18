#!/usr/bin/env python3
"""Read-only Exact13 preservation/integration verifier. Standard library only.

This verifies bytes, complete JSON values, source precedence evidence and rendered
content. It does not run game rules, apply repository changes or determine balance.
Optional original archives independently anchor the frozen source and prior-return
copies. No input archive code is imported or executed, and no archive is extracted.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile
from collections import Counter
from typing import Any

EXPECTED = {
    'exact13': (16084409, '8d0b39b8d110896ef99c4a5c8021cbdb3798ed686b82c15b973d6816b48fdc5b'),
    'prior_return': (228141, '018b3f0e5e932ae427d7a55b1e19ba5bd5b4500d100b4f05c73f15ab4a386590'),
    'conference12': (6026932, '625b1be66eafe2dce1ce43d5d53900de98bfe66d0aa96a679276edc2554276ab'),
    'acceptance_context': (1818434, 'b6c44900551f63abbee02d29256aade0477f9990e547a50c53447ef272de14ca'),
}
ARTIFACTS = ['CASEBOOK.json','DIRECTOR_REVIEW.md','EVIDENCE_MANIFEST.json',
             'LOCAL_REVIEW_NOTES.md','PLAYER_CHAPTER.md','REGISTER.json',
             'SOURCE_HASHES.json','SPELLS_MODEL.json']
BIBLE = 'DescentReviewChanges/ReviewBible/'
AUDIT = 'docs/audit/2026-10-08/full-game/'
RETURN = AUDIT+'illusion-perception14-part5-return-01/'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(raw: bytes) -> dict[str, Any]:
    return {'bytes':len(raw),'sha256':sha(raw)}


def exact_binding(raw: bytes, ref: dict[str,Any]) -> bool:
    return binding(raw) == {k:ref[k] for k in ('bytes','sha256')}


def at(value: Any, pointer: str) -> Any:
    if pointer == '': return value
    if not pointer.startswith('/'): raise ValueError('Not an absolute JSON pointer: '+pointer)
    for token in pointer[1:].split('/'):
        token = token.replace('~1','/').replace('~0','~')
        value = value[int(token)] if isinstance(value,list) else value[token]
    return value


def replace(value: Any, pointer: str, before: Any, after: Any) -> None:
    parent, token = pointer.rsplit('/',1)
    obj=at(value,parent); token=token.replace('~1','/').replace('~0','~')
    key = int(token) if isinstance(obj,list) else token
    if obj[key] != before: raise ValueError('Before-value mismatch at '+pointer)
    obj[key] = copy.deepcopy(after)


def differences(a: Any,b: Any,path: str='') -> list[str]:
    if type(a) is not type(b): return [path]
    if isinstance(a,dict):
        out=[]
        for key in sorted(set(a)|set(b)):
            p=path+'/'+str(key).replace('~','~0').replace('/','~1')
            out.extend([p] if key not in a or key not in b else differences(a[key],b[key],p))
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [path]
        return [p for i,(x,y) in enumerate(zip(a,b)) for p in differences(x,y,path+'/'+str(i))]
    return [] if a==b else [path]


def encode(value: Any) -> bytes:
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def section(text: str,title: str,level: int=2) -> str:
    mark='#'*level+' '+title+'\n'
    starts=[m.end() for m in re.finditer('^'+re.escape(mark),text,re.M)]
    if len(starts)!=1: raise ValueError(f'Expected one heading {mark.strip()}; got {len(starts)}')
    tail=text[starts[0]:]
    match=re.search(r'^#{1,'+str(level)+r'} ',tail,re.M)
    return (tail[:match.start()] if match else tail).strip('\n')


def scalar(value: Any) -> str:
    if isinstance(value,str): return value
    return json.dumps(value,ensure_ascii=False)


def rendered(value: Any,level: int=3) -> str:
    """Independent data-to-outline expectation; no supplied renderer is executed."""
    if isinstance(value,dict):
        return ''.join('#'*min(level,6)+' '+str(k)+'\n\n'+rendered(v,level+1) for k,v in value.items())
    if isinstance(value,list): return ''.join(rendered(v,level) for v in value)
    return scalar(value)+'\n\n'


def parse_json_section(text: str,title: str) -> Any:
    s=section(text,title)
    match=re.fullmatch(r'```json\n(.*)\n```',s,re.S)
    if not match: raise ValueError('Expected complete JSON fence under '+title)
    return json.loads(match.group(1))


def verify(args: argparse.Namespace) -> dict[str,Any]:
    checks: list[dict[str,Any]]=[]
    facts: dict[str,Any]={}
    def ck(category: str,name: str,passed: Any,evidence: Any=None) -> None:
        row={'category':category,'check':name,'passed':bool(passed)}
        if evidence is not None: row['evidence']=evidence
        checks.append(row)
    raw=Path(args.exact13).read_bytes()
    ck('archive_integrity','Exact13 supplied byte count and SHA256',
       (len(raw),sha(raw))==EXPECTED['exact13'],binding(raw))
    with zipfile.ZipFile(args.exact13) as z:
        names=z.namelist()
        ck('archive_integrity','238 unique members',len(names)==238 and len(names)==len(set(names)))
        unsafe=[]
        for item in z.infolist():
            p=PurePosixPath(item.filename)
            if (p.is_absolute() or '..' in p.parts or '\\' in item.filename or ':' in item.filename
                or stat.S_ISLNK(item.external_attr>>16) or item.filename.endswith('/')
                or str(p)!=item.filename): unsafe.append(item.filename)
        ck('archive_integrity','Canonical relative safe file names; no symbolic links',not unsafe,unsafe)
        bad=z.testzip(); ck('archive_integrity','Every ZIP CRC',bad is None,bad)
        cache: dict[str,Any]={}
        def load(path: str) -> Any:
            if path not in cache: cache[path]=json.loads(z.read(path).decode('utf-8'))
            return cache[path]
        def src(path: str) -> Any: return load('sources/'+path)
        def bck(name: str,ref: dict[str,Any]) -> None:
            p='sources/'+ref['path']
            ck('source_structure',name, p in names and exact_binding(z.read(p),ref),ref)
        ck('source_structure','Exactly eight current artifact names',
           sorted(n[8:] for n in names if n.startswith('current/'))==ARTIFACTS)
        bindings=[]
        for fn in ARTIFACTS:
            data=z.read('current/'+fn); data.decode('utf-8')
            if fn.endswith('.json'): load('current/'+fn)
            bindings.append({'name':fn,'inputArchivePath':'current/'+fn,**binding(data)})
        facts['artifactBindings']=bindings
        manifest=load('current/EVIDENCE_MANIFEST.json')
        ck('source_structure','Inner manifest binds seven companions and omits self',
           sorted(e['name'] for e in manifest['files'])==[x for x in ARTIFACTS if x!='EVIDENCE_MANIFEST.json'])
        for e in manifest['files']:
            ck('source_structure','Exact current companion '+e['name'],exact_binding(z.read('current/'+e['name']),e),e)
        sh=load('current/SOURCE_HASHES.json')
        expected_members={'README.md','LOCAL_ARTIFACT_CHECK.json'}|{'current/'+x for x in ARTIFACTS}
        for key,count,prefix in [('currentSources',122,'sources/'),('frozenConferenceSources',72,'historical-conference12/'),('acceptedContextSources',34,'accepted-context01/')]:
            es=sh[key]
            ck('source_structure',key+' cardinality and unique paths',len(es)==count and len({e['path'] for e in es})==count)
            for e in es:
                path=e['archivePath']; expected_members.add(path)
                ck('source_structure',key+': '+e['path'],
                   path==prefix+e['path'] and path in names and exact_binding(z.read(path),e),
                   {'archivePath':path,**binding(z.read(path))})
        ck('source_structure','Manifest partitions all 238 input members without extras',expected_members==set(names))
        m=load('current/SPELLS_MODEL.json'); cb=load('current/CASEBOOK.json'); reg=load('current/REGISTER.json')
        r13=src(m['candidate']['path']); app=m['actualReversibleApplication']
        r12=src(app['previousCandidate']['path']); repaired=src(app['actualRepairedPayload']['path'])
        operations=src(app['actualOperations']['path']); old_review=src(app['actualReview']['path'])
        qd=src(app['actualQuestionDispositions']['path']); cd=src(app['actualCaseDispositions']['path'])
        for k in ['actualReturnReceipt','actualOperations','actualRepairedPayload','actualReview','actualQuestionDispositions','actualCaseDispositions','previousCandidate']:
            bck('Reversible application binding '+k,app[k])
        for k in ['candidate','actualSemanticReview','actualSemanticReturn']: bck('Model binding '+k,m[k])
        ck('replay_selection','Actual accepted repaired-payload verdict preserved',
           old_review['verdict']['repairedPayload']=='SEMANTICALLY_ACCEPTED_FOR_INTEGRATION' and old_review['verdict']['acceptedIdentities']==14)
        ck('replay_selection','Exactly the two authorized replace operations',
           len(operations['operations'])==2 and [x['jsonPointer'] for x in operations['operations']]==['/spells/4/procedure','/spells/11/procedure'] and all(x['op']=='replace' for x in operations['operations']))
        replay=copy.deepcopy(r12)
        for op in operations['operations']:
            ck('replay_selection','Full before/after values '+op['jsonPointer'],
               at(r12,op['jsonPointer'])==op['before'] and at(repaired,op['jsonPointer'])==op['after'])
            replace(replay,op['jsonPointer'],op['before'],op['after'])
        ck('replay_selection','Forward replay equals entire returned repaired JSON',replay==repaired)
        ck('replay_selection','Forward replay encoding equals exact returned payload bytes',encode(replay)==z.read('sources/'+app['actualRepairedPayload']['path']))
        for op in reversed(operations['operations']):replace(replay,op['jsonPointer'],op['after'],op['before'])
        ck('replay_selection','Reverse replay equals entire original Current12 JSON',replay==r12)
        ck('replay_selection','Reverse replay encoding equals original Current12 bytes',encode(replay)==z.read('sources/'+app['previousCandidate']['path']))
        delta=differences(r12,repaired)
        ck('replay_selection','Only two procedure values changed from Current12',set(delta)=={'/spells/4/procedure','/spells/11/procedure'},delta)
        metadata_delta=differences(repaired,r13)
        ck('replay_selection','Current13 adds only successor metadata',
           set(metadata_delta)=={'/id','/recordedAtUtc','/status','/part5SemanticApplication13'},metadata_delta)
        restored=copy.deepcopy(r13);del restored['part5SemanticApplication13']
        for key in ['id','recordedAtUtc','status']:restored[key]=repaired[key]
        ck('replay_selection','Removing recorded successor metadata restores entire repaired payload',restored==repaired)
        ck('replay_selection','Model/register use exact Current13 application metadata',m['actualReversibleApplication']==r13['part5SemanticApplication13'] and reg['candidate']==m['candidate'])
        ck('replay_selection','Previous metadata preserved as actual historical values',app['previousMetadataUnchanged']=={k:r12[k] for k in ['id','recordedAtUtc','status']})
        facts['replay']={'authorizedProcedurePointers':delta,'successorMetadataPointers':metadata_delta,
                         'original':app['previousCandidate'],'repairedPayload':app['actualRepairedPayload'],'current13':m['candidate']}
        # Entire return-member comparison, anchored to its published original ZIP when supplied.
        oldmanifest=src(RETURN+'MANIFEST.json')
        for e in oldmanifest['files']:ck('source_structure','Prior return member '+e['path'],exact_binding(z.read('sources/'+RETURN+e['path']),e))
        facts['optionalExternalAnchors']={}
        for arg,key,prefix,original_prefix,manifest_key in [
            ('prior_return','prior_return','sources/'+RETURN,'',None),
            ('conference12','conference12','historical-conference12/','files/','files'),
            ('acceptance_context','acceptance_context','accepted-context01/','sources/','sources')]:
            external=getattr(args,arg)
            if not external:
                facts['optionalExternalAnchors'][key]={'checked':False,'reason':'Optional original archive not supplied'};continue
            eraw=Path(external).read_bytes();exb=binding(eraw)
            ck('external_original_anchors','Original '+key+' exact published binding',(len(eraw),sha(eraw))==EXPECTED[key],exb)
            with zipfile.ZipFile(external) as oldz:
                ck('external_original_anchors','Original '+key+' CRC',oldz.testzip() is None)
                if manifest_key:
                    es=json.loads(oldz.read('MANIFEST.json'))[manifest_key]
                    paths=[e['path'] for e in es]
                else:paths=oldz.namelist()
                for path in paths:
                    ck('external_original_anchors','Full original bytes '+key+': '+path,
                       z.read(prefix+path)==oldz.read(original_prefix+path))
            facts['optionalExternalAnchors'][key]={'checked':True,**exb,'fullMembersCompared':len(paths)}
        # Original native catalog, core and complete operational/source envelope.
        catalog=src(BIBLE+'data/public/spell_playtests/catalog.json')
        cat={s['id']:s for s in catalog['spells']}
        js=z.read('sources/'+BIBLE+'src/data/spells.js').decode('utf-8')
        native=json.JSONDecoder().raw_decode(js.split('export const SPELLS = ',1)[1])[0]
        core=src(BIBLE+'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
        ids=[s['id'] for s in m['spells']]
        declaration=src(RETURN+'SUCCESSOR_DECLARATION.json')
        ck('replay_selection','Exactly the accepted 14 identities in original order',
           len(ids)==len(set(ids))==14 and ids==[s['id'] for s in repaired['spells']]==reg['spellIds']==declaration['acceptedSpellIds'])
        ck('replay_selection','Creation not selected', 'creation' not in ids)
        routes={r['spellId']:r for r in repaired['sharedContractRouting10']}
        native_access_count=0;expected_shared={};player=z.read('current/PLAYER_CHAPTER.md').decode('utf-8');director=z.read('current/DIRECTOR_REVIEW.md').decode('utf-8')
        proc_facts=[]
        for i,s in enumerate(m['spells']):
            sid=s['id']; prev=repaired['spells'][i]
            selected=['id','completeSourceAndAccess','completeEarlierRecordUnchanged','originalSourceReference','procedure']
            ck('replay_selection','Whole selected rule/source/history '+sid,
               {k:s[k] for k in selected}=={k:prev[k] for k in selected})
            ck('source_structure','Whole native catalog/access envelope '+sid,s['completeSourceAndAccess']==cat[sid])
            original=s['completeSourceAndAccess']['source']['original']
            ck('source_structure','Native literal JavaScript object '+sid,native[sid]==original)
            ref=s['originalSourceReference']
            ck('source_structure','Complete original proposal record '+sid,at(src(ref['path']),ref['pointer'])==s['completeEarlierRecordUnchanged'])
            sb=s['completeSourceAndAccess']['source']
            ck('source_structure','Native catalog and Core source SHA bindings '+sid,
               sha(z.read('sources/'+BIBLE+'src/data/spells.js'))==sb['catalogSha256'] and sha(z.read('sources/'+BIBLE+sb['corePath']))==sb['coreSha256'])
            ck('source_structure','Whole preserved Core placement objects '+sid,
               all(core['spells'][e['index']]==e['original'] for e in sb['coreEntries']))
            access=s['completeSourceAndAccess']['classAccess'];native_access_count+=len(access)
            ck('source_structure','Actual class/rank/level/school/RP '+sid,
               set(access)==set(original['classRanks']) and all(
                 x['rank']==original['classRanks'][cl] and x['minimumClassLevel']==original['classLearnLevels'][cl]
                 and x['school']==original['classSchools'][cl] and x['baseRpCost']==core['resonance_costs'][str(x['rank'])] for cl,x in access.items()))
            ck('replay_selection','Selected exact candidate pointer '+sid,
               s['selectedProcedureSource']=={'candidate':m['candidate'],'pointer':f'/spells/{i}/procedure'})
            ck('replay_selection','Actual full question dispositions '+sid,
               s['actualDispositions']==[q for q in qd['dispositions'] if sid in q['spells']])
            r=routes[sid];group=int(r['currentSharedContextPointer'].split('/')[2])+1
            expected_rids=[f'IP14-SOURCE{group}-{k}' for k in r['applicableKeys']]
            ck('routed_shared_clauses','Exact per-spell shared selector '+sid,s['sharedRuleIds']==expected_rids)
            for key,rid in zip(r['applicableKeys'],expected_rids):
                if rid not in expected_shared: expected_shared[rid]={'spellIds':[],'pointer':r['currentSharedContextPointer']+'/'+key,'source':r['fullOriginalSource']}
                expected_shared[rid]['spellIds'].append(sid)
            # Full sections, not substring/case-ID presence alone.
            access_table='| Class | School | Rank | Minimum class level | Base RP |\n|---|---|---:|---:|---:|\n'
            for cl,x in access.items():access_table+=f"| {cl} | {x['school']} | {x['rank']} | {x['minimumClassLevel']} | {x['baseRpCost']} |\n"
            expected=access_table+'\n'+prev['procedure']
            ck('chapter_flow','Complete player spell section '+sid,section(player,s['name'])==expected)
            dexp=expected+'\n\nApplicable shared clauses: '+', '.join(s['sharedRuleIds'])+'.'
            ck('chapter_flow','Complete director spell section '+sid,section(director,s['name'])==dexp)
            proc_facts.append({'id':sid,'modelPointer':f'/spells/{i}/procedure','procedureUtf8':binding(s['procedure'].encode()),'sharedRuleIds':s['sharedRuleIds']})
        facts['selectedProcedures']=proc_facts;facts['nativeClassAccessRows']=native_access_count
        ck('routed_shared_clauses','Exactly 19 previously routed clauses; no unselected clauses',
           len(m['sharedRules'])==19 and list(m['sharedRules'])==list(expected_shared))
        common_prefix='The following clauses apply only to their listed spells. Each spell’s complete procedure controls its expressly stated local exception. Clauses about other named spells supply no additional ability.'
        common_sections=common_prefix+'\n\n'
        for rid,expected in expected_shared.items():
            item=m['sharedRules'][rid]; txt=at(repaired,expected['pointer'])
            ck('routed_shared_clauses','Complete unchanged text/source/pointer/scope '+rid,
               item['id']==rid and item['completeText']==txt and item['candidatePointer']==expected['pointer']
               and item['source']==expected['source'] and item['applicableSpellIds']==expected['spellIds'])
            common_sections+='### '+rid+'\n\nApplies to: '+', '.join(expected['spellIds'])+'.\n\n'+txt+'\n\n'
        for fn,text in [('PLAYER_CHAPTER.md',player),('DIRECTOR_REVIEW.md',director)]:
            ck('chapter_flow','Complete shared appendix '+fn,
               section(text,'Shared procedures by source and applicable spell')==common_sections.strip('\n'))
        for i,g in enumerate(repaired['completeOriginalSharedProposals']):
            ck('source_structure','Full original shared proposal group '+str(i+1),
               g['completeOriginalSharedProposal']==src(g['source']['path'])['sharedProposal'])
        ck('chapter_flow','Director exact authority routing',section(director,'Authority routing')==m['authorityRouting'])
        # The entire rendered metadata outline is checked, including nested source refs.
        for title,value in [('Actual question dispositions',qd),('Source convergence',m['currentSourceConvergence']),('Remaining gates and conditions',m['contentLimits'])]:
            actual=section(director,title);expect=rendered(value).strip('\n')
            ck('chapter_flow','Complete rendered data outline '+title,actual==expect,
               {'actualUtf8':binding(actual.encode()),'expectedUtf8':binding(expect.encode())})
        ck('replay_selection','Entire actual 16-question record preserved',m['actualQuestionDispositions']==qd and len(qd['dispositions'])==16)
        for key,oldkey,count in [('cases','currentExamples',28),('supplementalCases','supplementalVectors09',3),('originalScenarioTextsUnchanged','originalExamplesUnchanged',28)]:
            ck('complete_cases','Entire '+key+' array equals accepted payload',len(cb[key])==count and cb[key]==repaired[oldkey])
            for i,(a,b) in enumerate(zip(cb[key],repaired[oldkey])):
                ck('complete_cases',f'Full {key}/{i} {a["id"]}',a==b)
        ck('complete_cases','Entire actual case-review object preserved',cb['completeActualCaseReview']==cd)
        for title,value in [('Complete current cases',cb['cases']),('Complete supplemental cases',cb['supplementalCases']),('Original scenario texts, unchanged',cb['originalScenarioTextsUnchanged']),('Actual complete case review',cd)]:
            ck('complete_cases','Complete director JSON block '+title,parse_json_section(director,title)==value)
        byorig={x['id']:x['exactOriginalText'] for x in repaired['originalExamplesUnchanged']}
        ck('complete_cases','All 28 original-text fields remain exact',all(x['originalTextUnchanged']==byorig[x['id']] for x in cb['cases']))
        # Frozen-vs-current progression: verify supplied current index, not remote HEAD.
        ip=BIBLE+'data/public/spell_playtests/authored_review_index.json'
        idx=src(ip); old=load('historical-conference12/'+ip); iby={x['id']:x for x in idx['entries']};oby={x['id']:x for x in old['entries']}
        ck('source_precedence','848 identity population unchanged',len(iby)==848 and set(iby)==set(oby))
        # A receipt-only cosmology entry is still blocked and not reviewed. Do not
        # count an entry as accepted merely because its label lacks 'pending'.
        statuses=Counter(x['authoredStatus'] for x in idx['entries'])
        counts={'reviewed':statuses['reviewed-authored-operational-playtest'],
                'pending':statuses['pending-authored-procedure']+statuses['receipt-only-post-push-cosmology']}
        known_states={'reviewed-authored-operational-playtest','pending-authored-procedure','receipt-only-post-push-cosmology'}
        receipt_only=[x for x in idx['entries'] if x['authoredStatus']=='receipt-only-post-push-cosmology']
        ck('source_precedence','Current index independently counts 525/323',
           set(statuses)<=known_states and counts==idx['authoredCounts']=={'reviewed':525,'pending':323}
           and all(x['procedurePointer'] is None and x['sourceStatus']=='blocked-pending-operational-review' for x in receipt_only),
           {'literalAuthoredStatusCounts':dict(statuses),'receiptOnlyNotAccepted':[x['id'] for x in receipt_only]})
        ck('source_precedence','249 complete standalone plus 276 preserved legacy records',idx['representationCounts']=={'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':249})
        for sid in ids:ck('source_precedence','Selected identity still pending and unchanged '+sid,iby[sid]==oby[sid] and 'pending' in iby[sid]['authoredStatus'])
        accepted=[]
        for fn,n in [('damage_control_25_reviewed_10.json',25),('persistent_damage_20_reviewed_07.json',20)]:
            mod=src(BIBLE+'data/public/spell_candidates/'+fn)
            mids=[s['id'] for s in mod['spells']];accepted+=mids
            ck('source_precedence','Exact separate accepted cohort population '+fn,len(mids)==len(set(mids))==n)
        changes=[{'id':sid,'before':oby[sid],'after':iby[sid]} for sid in iby if iby[sid]!=oby[sid]]
        cv=m['currentSourceConvergence']
        ck('source_precedence','Exactly the 45 documented full membership changes',len(changes)==45 and {c['id'] for c in changes}==set(accepted) and changes==cv['completeMembershipChanges'])
        ck('source_precedence','Full source convergence identical across model and hash record',cv==sh['sourceConvergence'])
        ck('source_precedence','Both exact accepted application receipts preserved',all(src(x['source']['path'])==x['completeReceipt'] for x in cv['actualAcceptedApplications']))
        frozen_drift=[];context_drift=[]
        for key,prefix,actual in [('frozenConferenceSources','historical-conference12/',frozen_drift),('acceptedContextSources','accepted-context01/',context_drift)]:
            for e in sh[key]:
                if z.read(prefix+e['path'])!=z.read('sources/'+e['path']):actual.append(e['path'])
        ck('source_precedence','Frozen conference drift is index/navigation only',set(frozen_drift)=={ip,BIBLE+'docs/DEVELOPMENT_DIRECTION.md'} and set(frozen_drift)=={x['path'] for x in cv['sourceDrift']})
        ck('source_precedence','Accepted context drift is navigation only',context_drift==[BIBLE+'docs/DEVELOPMENT_DIRECTION.md'] and context_drift==[x['path'] for x in cv['acceptedContextNavigationDrift']])
        registry=src(BIBLE+'data/director/spell_review/accepted_interface_registry_06.json')
        ck('source_precedence','173 scoped accepted interface entries preserved',len(registry['entries'])==173)
        # Important hold/control records remain structurally identical and in explanatory text.
        ck('holds','All nine original exact holds preserved',len(old_review['holds'])==9 and m['contentLimits']['holds']==old_review['holds']==app['holds'])
        ck('holds','Whole content limits identical across model/casebook/register',m['contentLimits']==cb['contentLimits']==reg['contentLimits'])
        ck('holds','No future application or runtime selection enabled',m['runtimeSelectionEnabled'] is False and reg['applicationPlan']['runtimeSelectionEnabled'] is False and app['canonicalApplicationComplete'] is False and app['futureUnseenArtifactAcceptanceClaimed'] is False)
        ck('holds','No runtime tests, human playtest, balance, canon, world/release gate approval',
           all(m['contentLimits'][k] is False for k in ['runtimeImplemented','humanPlaytested','numericalBalanceApproved','cosmologyCanonModified','wholeGameComplete','releaseApproved']) and m['contentLimits']['runtimeTestsExecuted']==cb['runtimeTestsExecuted']==0 and m['contentLimits']['domainGatesDistinct']==75)
        ck('holds','No local new rule adoption or source deletion claims',m['newRuleAdoptions']==m['sourceInformationDeleted']==reg['newRuleAdoptions']==reg['sourceInformationDeleted']==0)
        ck('holds','Player conditional Mental Prison and mid-resolution Ready boundaries',
           'does not approve Mental Prison' in section(player,'Conditional interactions') and 'after the attack finishes' in section(player,'Conditional interactions') and 'genuine interrupt source' in section(player,'Conditional interactions'))
        ck('holds','Creation full historical record unchanged and not selected',r13['creationSeparate']==repaired['creationSeparate'] and qd['dispositions'][-1]['id']=='IP14-Q16' and qd['dispositions'][-1]['disposition']=='HOLD_SEPARATE')
        ck('holds','Exact conditional N29 full case and disposition unchanged',cb['supplementalCases'][0]==repaired['supplementalVectors09'][0] and cd['supplementalCases'][0]['disposition']=='PASS_CONDITIONAL_COMPOSITION_ONLY')
        ck('holds','Corrected Shadow Step grapple record wholly unchanged',
           next(x for x in cb['cases'] if x['id']=='IN4-06-A')==next(x for x in repaired['currentExamples'] if x['id']=='IN4-06-A'))
        ck('holds','Both scoped repairs present in both complete chapters',all(tag in player and tag in director for tag in ['IP14-STEED-SUPPRESS-13','IP14-SPECTRAL-HIDDEN-TARGET-13']))
        facts['sourcePrecedence']={'authoritativeSuppliedIndex':{'reviewed':525,'pending':323,'completeReviewedStandaloneProcedures':249},'scopedInterfaceCount':len(registry['entries']),'actualMembershipChangeCount':len(changes),'frozenConferenceDrift':frozen_drift,'acceptedContextDrift':context_drift,'remoteRepositoryReverified':False}
        facts['holds']=old_review['holds']
        # Supplied reports are checked as reports, never relabelled as our engine runs.
        supplied=[('LOCAL_ARTIFACT_CHECK.json',309),('sources/'+AUDIT+'ILLUSION_PERCEPTION_14_CURRENT_13_REPLAY_CHECK.json',339)]
        facts['suppliedReportCrossChecks']=[]
        for path,n in supplied:
            report=load(path)
            ck('supplied_report_consistency','Supplied report '+path,report['checkCount']==len(report['checks'])==n and report['failures']==0 and all(c['passed'] for c in report['checks']))
            facts['suppliedReportCrossChecks'].append({'archivePath':path,'reportedChecks':n,'reportedFailures':report['failures'],'suppliedOriginalScriptExecutedHere':False})
    categories={cat:{'checks':sum(x['category']==cat for x in checks),'failures':sum(x['category']==cat and not x['passed'] for x in checks)} for cat in sorted({x['category'] for x in checks})}
    return {'id':'DD-IP14-EXACT13-INDEPENDENT-INTEGRATION-VERIFICATION-01',
            'inputArchive':{'filename':Path(args.exact13).name,**binding(raw)},
            'checkCount':len(checks),'failures':sum(not x['passed'] for x in checks),
            'categories':categories,'facts':facts,'checks':checks,
            'scope':'Read-only byte/source/complete-value/replay/rendering/hold verification. Not independent gameplay, runtime or numerical-balance evidence.',
            'engineExecutions':0,'newGameplayArithmeticTests':0,'repositoryWrites':0}


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('exact13',type=Path)
    p.add_argument('--prior-return',type=Path)
    p.add_argument('--conference12',type=Path)
    p.add_argument('--acceptance-context',type=Path)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    try:
        input_paths=[x for x in [a.exact13,a.prior_return,a.conference12,a.acceptance_context] if x is not None]
        if any(a.out.resolve()==x.resolve() for x in input_paths):
            raise ValueError('Report output must not overwrite an input archive')
        report=verify(a)
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_bytes(encode(report))
    except (OSError,ValueError,KeyError,IndexError,TypeError,zipfile.BadZipFile) as exc:
        print(f'Verification could not finish: {type(exc).__name__}: {exc}',file=sys.stderr)
        return 2
    print(json.dumps({'checks':report['checkCount'],'failures':report['failures'],'categories':report['categories']},indent=2))
    if report['failures']:
        for c in report['checks']:
            if not c['passed']:print('FAILED:',c['check'])
    return 1 if report['failures'] else 0

if __name__=='__main__':raise SystemExit(main())
