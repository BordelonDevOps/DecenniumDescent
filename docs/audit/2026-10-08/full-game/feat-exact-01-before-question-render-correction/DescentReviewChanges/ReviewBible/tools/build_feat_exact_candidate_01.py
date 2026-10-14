"""Assemble complete source-directed feat text without promoting live catalogs.

This is a one-use authoring builder. The separate acceptance validator/case work
and actual GPT exact-candidate review remain required before submission/adoption.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from copy import deepcopy
from collections import Counter
import json
import os
import re
import shutil

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
V=A/'feat327-source-verdict'
I=R/'data/director/feat_candidates/exact_01'
U=R/'data/public/feat_candidates/exact_01'
D=R/'docs/feats/exact-candidate-01'
STATUS='Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.'
COHORTS=['skill','general_exploration','general_defense','crafting','combat','general_combat','magic_core','magic_extended','heritage_mutation']

def read(p):return json.loads(p.read_text('utf-8-sig'))
def dump(d):return json.dumps(d,ensure_ascii=False,indent=2)+'\n'
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(dump(d),encoding='utf-8',newline='\n')
def text(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def digest(x):return sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pointer(obj,p):
    for k in p.strip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj
def set_pointer(obj,p,value):
    parts=p.strip('/').split('/');parent=obj
    for k in parts[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
    key=int(parts[-1]) if isinstance(parent,list) else parts[-1];parent[key]=deepcopy(value)
def link(p,base):return Path(os.path.relpath(p,base.parent)).as_posix()
def allowed(obj,keys):
    assert set(keys)<=set(obj),(keys,list(obj))
    return {k:deepcopy(obj[k]) for k in keys}

def public_supplements(groups):
    """Explicit per-shape allowlist. Never copy comparison class cards to readers."""
    result=[]
    for group in groups:
        sid=group['id'];v=group['completeAuthoringValue']
        if sid=='SUP-01':value=allowed(v,['profile','nativeBody','actions','conversion','recovery'])
        elif sid=='SUP-02':value=[allowed(x,['id','name','eligibleBody','abilities','movement','attack','sense','limits']) for x in v]
        elif sid=='SUP-03':value=[allowed(x,['id','name','activation','cost','procedure']) for x in v]
        elif sid=='SUP-04':
            value={}
            for name,c in v.items():
                value[name]=allowed(c,['featCastingAbility','rank0Choices','rank1Choices','selection','ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax'])
                value[name]['choices']=[allowed(x,['id','name','rank','school','sourceClass','fullOriginalClassAccessRow']) for x in c['choices']]
        elif sid=='SUP-05':
            value={'newSpellFocus':allowed(v['newSpellFocus'],['id','name','sourceRegistryEntry','prerequisite','effect']),
                   'newLegacyInitiateCurricula':{name:allowed(x,['ability','notice','cantrips','rank1']) for name,x in v['newLegacyInitiateCurricula'].items()},
                   'newRitualTagOverlay':allowed(v['newRitualTagOverlay'],['ids','placement']),
                   'newDetectThoughts':allowed(v['newDetectThoughts'],['id','rank','school','completeProcedureInFeat','ordinaryClassAccess','explicitComparisonOnly'])}
        elif sid=='SUP-06':value=[allowed(x,['id','name','rank','school','sourceClass','fullOriginalClassAccessRow']) for x in v]
        elif sid=='SUP-07':
            copy=allowed(v['copyProfileContract'],['capture','rankAndPayment','numericBound','lifecycle'])
            copy['profiles']=[allowed(x,['id','role','activation','range','resolution']) for x in v['copyProfileContract']['profiles']]
            flora=allowed(v['floraBody'],['size','statistics','dc','cadence','endpoints','commandChoice'])
            flora['modes']=[allowed(x,['id','command','trap','burstType']) for x in v['floraBody']['modes']]
            value={'copyProfileContract':copy,'eldritchBlast':allowed(v['eldritchBlast'],['id','name','rank','castingAbility','castingTime','components','rangeFeet','effect','grant']),
                   'pactSigils':[allowed(x,['id','effect']) for x in v['pactSigils']],
                   'floraBody':flora,'minorBuffTransfer':allowed(v['minorBuffTransfer'],['guidance','resistance','true-strike','finalClarification']),
                   'timeTagOverlay':allowed(v['timeTagOverlay'],['spellIds','condition']),
                   'naturePredicate':allowed(v['naturePredicate'],['castingClassRoutes','exclusions'])}
        elif sid=='SUP-08':value=[allowed(x,['die','id','name','procedure']) for x in v]
        elif sid=='SUP-09':value=[allowed(x,['sourceId','name','actualSourceClass','minimumBorrowerTotalLevel','proposedBorrowedProcedure']) for x in v]
        else:raise AssertionError(sid)
        result.append({'id':sid,'cohort':group['cohort'],'status':'NEW supplement; source directions settled, exact review pending; not an original catalog identity.',
                       'selectionEnabled':False,'value':value})
    return result

def main():
    assert not any(p.exists() for p in [I,U,D,A/'FEAT_EXACT_CANDIDATE_01_BUILD.json',A/'feat-exact-01-source-preservation']), 'One-use authoring; preserve existing outputs.'
    checks=[]
    def ck(label,ok):
        checks.append({'name':label,'pass':bool(ok)});assert ok,label
    returned=read(V/'PACKAGE_MANIFEST.json')
    for name,binding in returned['files'].items():ck('Returned verdict payload '+name,info(V/name)==binding)
    reg=read(V/'FEAT_327_AUTHORING_REGISTER.json')['records']
    ops=read(V/'FEAT_EXACT_REPLACEMENTS.json')['operations']
    conv=read(V/'FEAT_SHARED_CONVENTION_DISPOSITIONS.json')['entries']
    groups=read(V/'FEAT_SUPPLEMENT_DIRECTIONS.json')['groups']
    shared=read(V/'FEAT_SHARED_DIRECTIONS.json')
    fex=read(V/'FEX_01_15_DISPOSITIONS.json')
    examples=read(V/'FEAT_660_EXAMPLE_DISPOSITIONS.json')
    extra=read(V/'FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json')
    source_paths=sorted({r['sourcePath'] for r in reg})
    source={p:read(G/p) for p in source_paths}
    original=deepcopy(source);derived=deepcopy(source)
    registry_path=R/'src/data/feats.js'
    registry=json.JSONDecoder().raw_decode(registry_path.read_text('utf-8').split('export const feats = ',1)[1])[0]
    registry_by={x['id']:x for x in registry}
    live_path=R/'data/public/feat_playtests/catalog.json';live=read(live_path)
    reviewed=[x for x in live['feats'] if x['operationalStatus']=='operational-playtest']
    reviewed_ids={x['id'] for x in reviewed}
    ck('All335 original IDs /327 source-directed /eight unchanged reviewed',len(registry)==len(registry_by)==335 and len(reg)==327 and len(reviewed)==8 and set(registry_by)=={x['featId'] for x in reg}|reviewed_ids)
    ck('Eight exact reviewed identities',reviewed_ids==set(read(V/'GOVERNING_SOURCE_BINDINGS.json')['unchangedReviewedFeatIds']))
    ck('Both original335 source files identical',registry_path.read_bytes()==(G/'src/data/feats.js').read_bytes())
    ck('Two deferred wrappers only',{r['featId'] for r in reg if r['payloadOperational'] is None}=={'astral_projection','planar_binding'})
    inputs={registry_path,G/'src/data/feats.js',live_path,R/'data/public/feat_playtests/manifest.json',Path(__file__).resolve()}
    inputs.update(G/p for p in source_paths);inputs.update(V/n for n in returned['files']);inputs.add(V/'PACKAGE_MANIFEST.json')
    for r in reg:
        p=r['sourcePath'];old=pointer(source[p],r['sourcePointer'])
        ck(r['featId']+' exact source file',info(G/p)['sha256']==r['sourceFileSha256'])
        ck(r['featId']+' immutable original object',old['sourceObject']==r['originalSourceObject']==registry_by[r['featId']])
        ck(r['featId']+' complete submitted procedure/cases',old['procedure']==r['submittedProcedure'] and old['workedCases']==r['submittedWorkedCases'])
    operation_log=[]
    for op in ops:
        p=op['path'];ck(op['id']+' exact full field binding',info(G/p)['sha256']==op['sourceFileSha256'] and pointer(derived[p],op['pointer'])==op['old'] and op['preserveOriginal'] is True)
        set_pointer(derived[p],op['pointer'],op['replacement'])
        operation_log.append({**op,'applicationStatus':'Applied to separate exact candidate only; original unchanged.'})
    for x in conv:
        ck(x['cohort']+x['pointer']+' original convention',pointer(source[x['sourcePath']],x['pointer'])==x['original'])
        set_pointer(derived[x['sourcePath']],x['pointer'],x['replacement'])
    for x in groups:
        ck(x['id']+' original supplement value',pointer(source[x['sourcePath']],x['pointer'])==x['original'])
        set_pointer(derived[x['sourcePath']],x['pointer'],x['completeAuthoringValue'])
    for r in reg:
        v=pointer(derived[r['sourcePath']],r['sourcePointer'])
        ck(r['featId']+' complete final procedure and case arrays',v['procedure']==r['completeAuthoringProcedure'] and v['workedCases']==r['workedCases'])
        v.update({'exactCandidateStatus':STATUS,'sourceVerdictDecision':r['decision'],'sourceVerdictId':returned['reviewId'],
                  'payloadOperational':None if r['payloadOperational'] is None else r['completeAuthoringProcedure'],
                  'selectionEnabled':False,'exactApproved':False,'runtimeApproved':False})

    # Resolve every actual spell dependency from the current authored index.
    sp=R/'data/public/spell_playtests';catalog_path=sp/'catalog.json';index_path=sp/'authored_review_index.json'
    catalog={x['id']:x for x in read(catalog_path)['spells']};idx={x['id']:x for x in read(index_path)['entries']}
    inputs.update([catalog_path,index_path])
    spell_ids=set()
    for obj in source.values():spell_ids.update(obj.get('completeCurrentSpellDependencies',{}))
    curricula=next(x['completeAuthoringValue'] for x in groups if x['id']=='SUP-04')
    rituals=next(x['completeAuthoringValue'] for x in groups if x['id']=='SUP-06')
    placement_rows=[]
    for name,c in curricula.items():
        ck(name+' exact rank0/rank1 choice counts',sum(x['rank']==0 for x in c['choices'])==c['rank0Choices'] and sum(x['rank']==1 for x in c['choices'])==c['rank1Choices'])
        for x in c['choices']:placement_rows.append({'route':'curriculum','curriculum':name,**x});spell_ids.add(x['id'])
    for x in rituals:placement_rows.append({'route':'ritual',**x});spell_ids.add(x['id'])
    dependencies={}
    for sid in sorted(spell_ids):
        e=idx[sid];p=sp/e['procedureFile'];inputs.add(p);card=pointer(read(p),e['wholeCardPointer'])
        ck(sid+' current whole spell identity',card.get('id',card.get('spellId'))==sid)
        op=card.get('operational',card.get('operationalCandidate'))
        if sid in {'astral-projection','planar-binding'}:
            ck(sid+' literal deferred receipt only',e['authoredStatus']=='pending-authored-procedure' and op is None)
        else:
            ck(sid+' reviewed full payload',e['authoredStatus']=='reviewed-authored-operational-playtest' and isinstance(op,dict))
        dependencies[sid]={'id':sid,'originalCatalogRecord':catalog[sid],'authoredIndexEntry':e,'completeCurrentProcedureCard':card,
                           'binding':{'file':p.relative_to(G).as_posix(),**info(p),'pointer':e['wholeCardPointer']},'grantsNoAccessByItself':True}
    for x in placement_rows:
        row=catalog[x['id']]['classAccess'][x['sourceClass']]
        ck(x['route']+':'+x.get('curriculum','Wizard')+':'+x['id']+' exact class/rank/school placement',row==x['fullOriginalClassAccessRow'] and row['rank']==x['rank'] and row['school']==x['school'])
        ck(x['id']+' current placement pointer',x['currentProcedureFile']==idx[x['id']]['procedureFile'] and x['currentWholeCardPointer']==idx[x['id']]['wholeCardPointer'])
        ck(x['id']+' selectable placement has reviewed payload',idx[x['id']]['authoredStatus']=='reviewed-authored-operational-playtest')
    ck('Sixteen curricula and seven ritual placements',len(curricula)==16 and len(rituals)==7)
    ck('All660 original example positions and28 additional cases',len(examples['cases'])==660 and len(extra['cases'])==28)
    ck('All16 rules /91 conventions /15 interfaces /67 operations /9 supplement groups',len(shared['rules'])==16 and len(conv)==91 and len(fex['issues'])==15 and len(ops)==67 and len(groups)==9)

    # Preserve current original bytes before creating any separately named output.
    preserve_inputs=set(inputs)-{Path(__file__).resolve(),catalog_path,index_path}
    preserve_inputs.update(R/'docs/feats'/f'{c.upper()}_FEAT_OPERATING_PROPOSAL.md' for c in COHORTS)
    preservation={};folder=A/'feat-exact-01-source-preservation'
    for p in sorted(preserve_inputs):
        inputs.add(p);rel=p.relative_to(G).as_posix();q=folder/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
        ck('Preserved original '+rel,info(p)==info(q));preservation[rel]={**info(p),'preservedCopy':q.relative_to(G).as_posix()}
    save(folder/'PRESERVATION_MANIFEST.json',preservation)
    input_bindings={p.relative_to(G).as_posix():info(p) for p in sorted(inputs)}
    now=datetime.now(timezone.utc).isoformat()
    common={'schemaVersion':'feat-exact-candidate-01','status':STATUS,'sourceVerdictId':returned['reviewId'],'createdAtUtc':now,
            'selectionEnabled':False,'runtimeImplemented':False,'humanBalanceApproved':False,'wholeGameFlowApproved':False,'sourceInformationDeleted':0,'cosmologyReviewed':False}
    internal_records=[]
    for r in reg:
        internal_records.append({'id':r['featId'],'name':r['name'],'cohort':r['cohort'],'sourceObject':r['originalSourceObject'],
            'originalQuestion':r['originalQuestion'],'questionId':r['questionId'],'sourceDirection':r,
            'operationalRules':r['completeAuthoringProcedure'],'workedCases':r['workedCases'],
            'payloadOperational':None if r['payloadOperational'] is None else r['completeAuthoringProcedure'],
            'selectionEnabled':False,'exactApproved':False,'runtimeApproved':False,
            'sourceAuthored':True,'sharedRulesRef':'shared_rules.json','supplementsRef':'supplements.json'})
    internal={**common,'records':internal_records,'unchangedReviewedFeats':reviewed,'original335Registry':registry,
              'originalQuestionCount':327,'sourceFileBindings':input_bindings,'preservationManifest':(folder/'PRESERVATION_MANIFEST.json').relative_to(G).as_posix(),
              'assemblyScope':'Complete text/envelope assembly only. FXC state-boundary validation and actual exact review remain outstanding.'}
    save(I/'candidate.json',internal)
    save(I/'shared_rules.json',shared);save(I/'supplements.json',{'reviewId':returned['reviewId'],'groups':groups})
    save(I/'applied_operations.json',{'scope':'Exact source-authoring operations on separate derived files; no live catalog update.','operations':operation_log})
    save(I/'convention_dispositions.json',read(V/'FEAT_SHARED_CONVENTION_DISPOSITIONS.json'))
    save(I/'fex_dispositions.json',fex);save(I/'source_conflict_dispositions.json',read(V/'FEAT_SOURCE_CONFLICT_DISPOSITIONS.json'))
    save(I/'example_dispositions.json',examples);save(I/'additional_boundary_expectations.json',extra)
    for c in COHORTS:
        path=next(p for p in source_paths if Path(p).name==c+'_feat_operating_proposal_internal.json')
        derived[path]['status']=STATUS;derived[path]['createdAtUtc']=now
        derived[path]['currentSourceDirectionContract']={'verdictId':returned['reviewId'],'sharedRules':'../shared_rules.json','supplements':'../supplements.json','exactApproved':False}
        save(I/'cohorts'/f'{c}.json',derived[path])

    # Public reconstruction is from verified original public registry + final
    # per-ID source directions, not a serialization of private candidate objects.
    by_reg={r['featId']:r for r in reg};by_reviewed={x['id']:x for x in reviewed}
    public_rows=[]
    for original_source in registry:
        sid=original_source['id']
        if sid in by_reviewed:
            public_rows.append({'id':sid,'name':original_source['name'],'reviewStatus':'Previously reviewed; unchanged original full operational record.',
                                'sourceObject':original_source,'unchangedReviewedRecord':deepcopy(by_reviewed[sid])})
        else:
            r=by_reg[sid]
            public_rows.append({'id':sid,'name':r['name'],'cohort':r['cohort'],'sourceObject':deepcopy(original_source),
                'reviewStatus':'Source-authored; exact candidate review pending.','operationalRules':r['completeAuthoringProcedure'],
                'workedCases':deepcopy(r['workedCases']),'payloadOperational':None if r['payloadOperational'] is None else r['completeAuthoringProcedure'],
                'selectionEnabled':False,'exactApproved':False,'runtimeApproved':False,'sharedRulesRef':'shared_rules.json','supplementsRef':'supplements.json'})
    public={**common,'feats':public_rows,'originalFeats':335,'unchangedReviewedFeats':8,'sourceAuthoredCandidates':325,'deferredNullWrappers':2,
            'newSupplementsAreOutsideOriginalCounts':True}
    save(U/'candidate.json',public);save(U/'shared_rules.json',shared)
    pub_sup=public_supplements(groups);save(U/'supplements.json',{'status':STATUS,'groups':pub_sup})
    # These complete envelopes are already public sources, retained exactly.
    save(U/'spell_dependencies.json',{'status':'Exact current public payloads and two literal deferred receipts. Linked placements grant only their specific feat permission; deferred receipts supply no operational payload.','spells':dependencies})
    save(U/'spell_placements.json',{'status':STATUS,'placements':placement_rows})
    save(U/'fex_rules.json',{'rules':[allowed(x,['id','completeResolution']) for x in fex['issues']]})

    # Full reader text and source-audit chapters, not title-only stubs.
    for c in COHORTS:
        rows=[r for r in internal_records if r['cohort']==c]
        pubdoc=D/f'{c.upper()}.md';auditdoc=D/'source-audit'/f'{c.upper()}.md'
        head=['# '+c.replace('_',' ').title()+' feats','', '**'+STATUS+'**','',
              '[Complete shared rules](SHARED_RULES.md) · [Finite supplements](SUPPLEMENTS.md) · [Spell payloads](SPELL_PAYLOADS.md)','',
              'Read every procedure with the complete shared rules. NEW identifies authored completions; old source alternatives remain preserved. The two deferred payloads are unavailable.','']
        pub=list(head);audit=['# '+c.replace('_',' ').title()+' — complete source/question reconciliation','',STATUS,'']
        for r in rows:
            src=r['sourceObject'];pub += ['## '+r['name']+' (`'+r['id']+'`)','',
                '**Prerequisite:** '+str(src.get('prerequisite','No printed prerequisite.')),'',r['operationalRules'],'','### Worked examples','',*[x+'\n' for x in r['workedCases']]]
            if r['payloadOperational'] is None:pub += ['**Unavailable payload:** retained grant wrapper only; operational payload is null.','']
            audit += ['## '+r['questionId']+' — '+r['name'],'','### Original complete object','','```json',json.dumps(src,ensure_ascii=False,indent=2),'```','',
                '### Original question','',r['originalQuestion'],'','### Final source decision','',r['sourceDirection']['decision'],'',
                '### Complete candidate procedure','',r['operationalRules'],'','### Final authored examples','',*[x+'\n' for x in r['workedCases']],
                '### Preserved submitted procedure','',r['sourceDirection']['submittedProcedure'],'','### Preserved submitted examples','',*[x+'\n' for x in r['sourceDirection']['submittedWorkedCases']]]
        text(pubdoc,'\n'.join(pub));text(auditdoc,'\n'.join(audit))
    lines=['# Shared feat rules','',STATUS,'']
    for rule in shared['rules']:lines+=['## '+rule['id']+' — '+rule['title'],'',rule['wording'],'']
    text(D/'SHARED_RULES.md','\n'.join(lines))
    lines=['# Complete finite feat supplements','',STATUS,'',
           'All entries here are NEW bounded supplements. Their source directions are settled; the assembled candidate still awaits exact review. They do not add original registry IDs or promote comparison class/spell cards.','']
    for group in pub_sup:
        lines+=['## '+group['id']+' — '+group['cohort'].replace('_',' ').title(),'','```json',json.dumps(group['value'],ensure_ascii=False,indent=2),'```','']
    text(D/'SUPPLEMENTS.md','\n'.join(lines))
    lines=['# Current spell payloads and deferred source receipts for feats','',
           'Each complete public record below is retained without flattening a standalone operationalCandidate into a legacy adapter. The curriculum/ritual table fixes the actual class, rank and school; other class placements in an original record are not additional feat grants.','']
    for sid,dep in dependencies.items():
        if sid in {'astral-projection','planar-binding'}:lines+=['**The following is a literal deferred receipt. Its operational payload remains null and unavailable; no cosmology interpretation is supplied.**','']
        lines+=['## '+catalog[sid]['name']+' (`'+sid+'`)','','```json',json.dumps(dep['completeCurrentProcedureCard'],ensure_ascii=False,indent=2),'```','']
    text(D/'SPELL_PAYLOADS.md','\n'.join(lines))
    lines=['# Feat candidate casebook','',STATUS,'',
           'The following are complete authored expectations, not executed full feat-runtime tests. Original examples and their final outcomes are retained at every original position.','']
    for case in examples['cases']:lines+=['## '+case['id'],'','```json',json.dumps(case,ensure_ascii=False,indent=2),'```','']
    for case in extra['cases']:lines+=['## '+case['id'],'','```json',json.dumps(case,ensure_ascii=False,indent=2),'```','']
    text(D/'source-audit/CASEBOOK.md','\n'.join(lines))
    lines=['# Complete feat candidate 01','', '**'+STATUS+'**','',
           'The complete 335-entry original registry is preserved: eight reviewed feats unchanged, 325 newly authored procedures, and two deferred grant wrappers with null payloads. All 327 original questions, 660 original example positions, 28 additional authored cases, 16 shared rules, 91 convention dispositions and 15 FEX decisions are retained.','',
           '[Shared rules](SHARED_RULES.md) · [Complete supplements](SUPPLEMENTS.md) · [Exact current spell payloads](SPELL_PAYLOADS.md) · [Full casebook](source-audit/CASEBOOK.md)','',
           '[Public envelope]('+link(U/'candidate.json',D/'README.md')+') · [Internal/source envelope]('+link(I/'candidate.json',D/'README.md')+') · [Exact-review contract]('+link(V/'FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',D/'README.md')+')','',
           '## Complete cohort chapters','']
    for c in COHORTS:lines+=['- ['+c.replace('_',' ').title()+']('+c.upper()+'.md) · [Original questions and decisions](source-audit/'+c.upper()+'.md)']
    lines+=['','## Outstanding before submission','',
            'The complete text and source envelopes are assembled. Finite FXC acquisition, capacity, clock, body, command, copy and settlement acceptance cases still need their independent validation. These authored cases are not a complete application runtime or human playtest. The exact candidate has not been submitted or approved.','']
    text(D/'README.md','\n'.join(lines))

    for r in internal_records:
        q=next(x for x in public_rows if x['id']==r['id'])
        ck(r['id']+' full independent public/internal procedure',q['operationalRules']==r['operationalRules'] and q['workedCases']==r['workedCases'])
        for doc in [D/f"{r['cohort'].upper()}.md",D/'source-audit'/f"{r['cohort'].upper()}.md"]:
            rendered=doc.read_text('utf-8');ck(r['id']+' full manuscript '+doc.parent.name,r['operationalRules'] in rendered and all(x in rendered for x in r['workedCases']))
    for row in public_rows:
        ck(row['id']+' unchanged public original',row['sourceObject']==registry_by[row['id']])
        if row['id'] in reviewed_ids:ck(row['id']+' unchanged full reviewed envelope',row['unchangedReviewedRecord']==by_reviewed[row['id']])
    for name,binding in input_bindings.items():ck('Input unchanged '+name,info(G/name)==binding)
    outputs={p.relative_to(G).as_posix():info(p) for folder in [I,U,D] for p in sorted(folder.rglob('*')) if p.is_file()}
    result={'createdAtUtc':now,'status':STATUS,'previousGoalTurnClassification':'progress: TU6 authored and actual GPT source verdict verified.',
            'scope':'Full text/envelope/source assembly checks only; the separate FXC state-boundary validator, actual exact review and runtime/human checks are not claimed.',
            'originalRegistryEntries':335,'unchangedReviewedFeats':8,'candidateIdentities':327,'completeCandidateProcedures':325,'deferredNullWrappers':2,
            'exactFieldOperationsApplied':len(ops),'originalExamplePositions':660,'additionalAuthoredCases':28,'sharedRules':16,'conventionDispositions':91,'fexDecisions':15,
            'curricula':16,'curriculumPlacements':sum(len(x['choices']) for x in curricula.values()),'ritualPlacements':7,'completeReviewedSpellDependencies':len(dependencies)-2,'literalDeferredSpellReceipts':2,
            'publicManuscripts':9,'sourceAuditManuscripts':9,'checks':len(checks),'failures':0,'checksDetails':checks,
            'originalSourceBindings':input_bindings,'artifacts':outputs,'preservationManifest':{'path':(folder/'PRESERVATION_MANIFEST.json').relative_to(G).as_posix(),**info(folder/'PRESERVATION_MANIFEST.json')},
            'readyForSubmission':False,'exactApproved':False,'catalogPromoted':False,'runtimeImplemented':False,'sourceInformationDeleted':0,'pushed':False,'cosmologyReviewed':False}
    save(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('checksDetails','originalSourceBindings','artifacts')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
