"""Independently inspect emitted source-directed envelopes and complete text.

No builder imports. This does not execute all feat mechanics or claim FXC closure.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from collections import Counter
import json
import re

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
V=A/'feat327-source-verdict';I=R/'data/director/feat_candidates/exact_01';U=R/'data/public/feat_candidates/exact_01';D=R/'docs/feats/exact-candidate-01'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def at(d,p):
    for k in p.strip('/').split('/'):d=d[int(k)] if isinstance(d,list) else d[k.replace('~1','/').replace('~0','~')]
    return d
def fields(v,names):return {k:v[k] for k in names.split()}
def expected_supplement(g):
    """Separate public shape reconstruction from source verdict, not builder."""
    sid=g['id'];v=g['completeAuthoringValue']
    if sid=='SUP-01':return fields(v,'profile nativeBody actions conversion recovery')
    if sid=='SUP-02':return [fields(x,'id name eligibleBody abilities movement attack sense limits') for x in v]
    if sid=='SUP-03':return [fields(x,'id name activation cost procedure') for x in v]
    if sid=='SUP-04':
        out={}
        for name,row in v.items():
            out[name]=fields(row,'featCastingAbility rank0Choices rank1Choices selection ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax')
            out[name]['choices']=[fields(x,'id name rank school sourceClass fullOriginalClassAccessRow') for x in row['choices']]
        return out
    if sid=='SUP-05':
        return {'newSpellFocus':fields(v['newSpellFocus'],'id name sourceRegistryEntry prerequisite effect'),
                'newLegacyInitiateCurricula':{n:fields(x,'ability notice cantrips rank1') for n,x in v['newLegacyInitiateCurricula'].items()},
                'newRitualTagOverlay':fields(v['newRitualTagOverlay'],'ids placement'),
                'newDetectThoughts':fields(v['newDetectThoughts'],'id rank school completeProcedureInFeat ordinaryClassAccess explicitComparisonOnly')}
    if sid=='SUP-06':return [fields(x,'id name rank school sourceClass fullOriginalClassAccessRow') for x in v]
    if sid=='SUP-07':
        cp=fields(v['copyProfileContract'],'capture rankAndPayment numericBound lifecycle')
        cp['profiles']=[fields(x,'id role activation range resolution') for x in v['copyProfileContract']['profiles']]
        flora=fields(v['floraBody'],'size statistics dc cadence endpoints commandChoice')
        flora['modes']=[fields(x,'id command trap burstType') for x in v['floraBody']['modes']]
        return {'copyProfileContract':cp,'eldritchBlast':fields(v['eldritchBlast'],'id name rank castingAbility castingTime components rangeFeet effect grant'),
                'pactSigils':[fields(x,'id effect') for x in v['pactSigils']], 'floraBody':flora,
                'minorBuffTransfer':fields(v['minorBuffTransfer'],'guidance resistance true-strike finalClarification'),
                'timeTagOverlay':fields(v['timeTagOverlay'],'spellIds condition'),'naturePredicate':fields(v['naturePredicate'],'castingClassRoutes exclusions')}
    if sid=='SUP-08':return [fields(x,'die id name procedure') for x in v]
    if sid=='SUP-09':return [fields(x,'sourceId name actualSourceClass minimumBorrowerTotalLevel proposedBorrowedProcedure') for x in v]
    raise ValueError(sid)

def main():
    checks=[]
    def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
    build=read(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    for n,b in build['originalSourceBindings'].items():check('Original input unchanged '+n,info(G/n)==b)
    for n,b in build['artifacts'].items():check('Exact emitted artifact '+n,info(G/n)==b)
    preservation=read(G/build['preservationManifest']['path'])
    for n,b in preservation.items():
        check('Preserved bytes '+n,info(G/b['preservedCopy'])=={k:b[k] for k in ('bytes','sha256')})
    internal=read(I/'candidate.json');public=read(U/'candidate.json')
    source=read(V/'FEAT_327_AUTHORING_REGISTER.json')['records'];sr={x['featId']:x for x in source}
    registry=json.JSONDecoder().raw_decode((R/'src/data/feats.js').read_text('utf-8').split('export const feats = ',1)[1])[0]
    orig={x['id']:x for x in registry};ir={x['id']:x for x in internal['records']};pr={x['id']:x for x in public['feats']}
    live=read(R/'data/public/feat_playtests/catalog.json')['feats'];old={x['id']:x for x in live if x['operationalStatus']=='operational-playtest'}
    check('Exact335 ID set and order',len(pr)==335 and [x['id'] for x in public['feats']]==[x['id'] for x in registry])
    check('Exact327 source question IDs',len(ir)==327 and set(ir)==set(sr) and len({x['questionId'] for x in ir.values()})==327)
    check('Original registry structure unchanged',internal['original335Registry']==registry)
    common={'schemaVersion','status','sourceVerdictId','createdAtUtc','selectionEnabled','runtimeImplemented','humanBalanceApproved','wholeGameFlowApproved','sourceInformationDeleted','cosmologyReviewed'}
    check('Public top-level explicit allowlist',set(public)==common|{'feats','originalFeats','unchangedReviewedFeats','sourceAuthoredCandidates','deferredNullWrappers','newSupplementsAreOutsideOriginalCounts'})
    for sid in orig:
        p=pr[sid];check(sid+' original object including absence/null',p['sourceObject']==orig[sid])
        if sid in old:
            check(sid+' reviewed envelope byte-structure unchanged',p['unchangedReviewedRecord']==old[sid])
            check(sid+' reviewed public allowlist',set(p)=={'id','name','reviewStatus','sourceObject','unchangedReviewedRecord'})
            continue
        s=sr[sid];i=ir[sid]
        check(sid+' candidate field allowlist',set(p)=={'id','name','cohort','sourceObject','reviewStatus','operationalRules','workedCases','payloadOperational','selectionEnabled','exactApproved','runtimeApproved','sharedRulesRef','supplementsRef'})
        check(sid+' whole public/internal/final procedure equality',p['operationalRules']==i['operationalRules']==s['completeAuthoringProcedure'])
        check(sid+' whole public/internal/final examples equality',p['workedCases']==i['workedCases']==s['workedCases'])
        check(sid+' full original question and decision',i['originalQuestion']==s['originalQuestion'] and i['sourceDirection']==s)
        check(sid+' no premature activation',p['selectionEnabled'] is False and p['exactApproved'] is False and p['runtimeApproved'] is False)
        check(sid+' payload null distinction',p['payloadOperational']==(None if sid in {'astral_projection','planar_binding'} else s['completeAuthoringProcedure']))
        for f in (D/(s['cohort'].upper()+'.md'),D/'source-audit'/(s['cohort'].upper()+'.md')):
            content=f.read_text('utf-8');check(sid+' exact complete rendered text '+str(f.relative_to(D)),s['completeAuthoringProcedure'] in content and all(x in content for x in s['workedCases']))
    check('Only two null candidate payloads',{sid for sid in sr if pr[sid]['payloadOperational'] is None}=={'astral_projection','planar_binding'})
    check('Original live manifest remains eight reviewed',read(R/'data/public/feat_playtests/manifest.json')['operationalFeats']==8)
    dirs={c:read(I/'cohorts'/(c+'.json')) for c in {s['cohort'] for s in source}}
    operations=read(V/'FEAT_EXACT_REPLACEMENTS.json')['operations']
    for op in operations:
        c=sr[op['featId']]['cohort'];saved=G/preservation[op['path']]['preservedCopy']
        check(op['id']+' preserved original pointer',info(saved)['sha256']==op['sourceFileSha256'] and at(read(saved),op['pointer'])==op['old'])
        check(op['id']+' exact derived replacement',at(dirs[c],op['pointer'])==op['replacement'])
    for x in read(V/'FEAT_SHARED_CONVENTION_DISPOSITIONS.json')['entries']:
        check(x['cohort']+x['pointer']+' complete convention replacement',at(dirs[x['cohort']],x['pointer'])==x['replacement'])
    for file in ['shared_rules.json','fex_dispositions.json','source_conflict_dispositions.json','example_dispositions.json','additional_boundary_expectations.json','convention_dispositions.json']:
        source_file={'shared_rules.json':'FEAT_SHARED_DIRECTIONS.json','fex_dispositions.json':'FEX_01_15_DISPOSITIONS.json','source_conflict_dispositions.json':'FEAT_SOURCE_CONFLICT_DISPOSITIONS.json','example_dispositions.json':'FEAT_660_EXAMPLE_DISPOSITIONS.json','additional_boundary_expectations.json':'FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json','convention_dispositions.json':'FEAT_SHARED_CONVENTION_DISPOSITIONS.json'}[file]
        check(file+' full returned source equality',read(I/file)==read(V/source_file))
    check('Complete public shared rules',read(U/'shared_rules.json')==read(V/'FEAT_SHARED_DIRECTIONS.json'))
    gs=read(V/'FEAT_SUPPLEMENT_DIRECTIONS.json')['groups'];pubgs=read(U/'supplements.json')['groups']
    check('All nine public supplement identities',len(pubgs)==9 and [g['id'] for g in gs]==[g['id'] for g in pubgs])
    for g,p in zip(gs,pubgs):
        check(g['id']+' independent public field reconstruction',p['value']==expected_supplement(g) and set(p)=={'id','cohort','status','selectionEnabled','value'} and p['selectionEnabled'] is False)
        check(g['id']+' exact complete internal value',at(dirs[g['cohort']],g['pointer'])==g['completeAuthoringValue'])
        check(g['id']+' full reader supplement text',json.dumps(p['value'],ensure_ascii=False,indent=2) in (D/'SUPPLEMENTS.md').read_text('utf-8'))
    public_supp_text=json.dumps(pubgs,ensure_ascii=False)
    check('No borrowed full comparison card copied into public supplements','completeCurrentSourceCard' not in public_supp_text)
    sp=R/'data/public/spell_playtests';index={x['id']:x for x in read(sp/'authored_review_index.json')['entries']}
    cat={x['id']:x for x in read(sp/'catalog.json')['spells']};deps=read(U/'spell_dependencies.json')['spells']
    spell_text=(D/'SPELL_PAYLOADS.md').read_text('utf-8')
    cache={}
    for sid,x in deps.items():
        e=index[sid];p=sp/e['procedureFile'];cache.setdefault(str(p),read(p));card=at(cache[str(p)],e['wholeCardPointer'])
        check(sid+' exact source public envelope',x['originalCatalogRecord']==cat[sid] and x['authoredIndexEntry']==e and x['completeCurrentProcedureCard']==card)
        check(sid+' pointer/hash binding',x['binding']=={'file':p.relative_to(G).as_posix(),**info(p),'pointer':e['wholeCardPointer']})
        check(sid+' complete payload manuscript',json.dumps(card,ensure_ascii=False,indent=2) in spell_text)
    rows=read(U/'spell_placements.json')['placements'];check('1838 curricula and seven ritual placements',len(rows)==1845)
    for x in rows:
        e=index[x['id']];current=cat[x['id']]['classAccess'][x['sourceClass']]
        check(x['route']+x.get('curriculum','Wizard')+x['id']+' exact reviewed placement',e['authoredStatus']=='reviewed-authored-operational-playtest' and current==x['fullOriginalClassAccessRow'] and current['rank']==x['rank'] and current['school']==x['school'] and x['id'] in deps)
    casebook=(D/'source-audit/CASEBOOK.md').read_text('utf-8')
    for x in read(V/'FEAT_660_EXAMPLE_DISPOSITIONS.json')['cases']+read(V/'FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json')['cases']:
        check(x['id']+' complete casebook disposition',json.dumps(x,ensure_ascii=False,indent=2) in casebook)
    for p in D.rglob('*.md'):
        # Ignore fenced source data; those literal historical strings are not navigation.
        body=re.sub(r'```.*?```','',p.read_text('utf-8'),flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',body):
            if not re.match(r'^[a-zA-Z]+:|^#',target):check('Reader link '+str(p.relative_to(D))+' '+target,(p.parent/target.split('#')[0]).resolve().is_file())
    fails=[x for x in checks if not x['pass']]
    result={'createdAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Independent emitted-file/source equality, exact public field allowlists, complete question/procedure/example rendering, full current spell modes and original preservation. No full feat runtime, balance or FXC state-boundary completion claimed.',
            'checks':len(checks),'failures':len(fails),'counts':{'originals':335,'unchangedReviewed':8,'sourceDirected':327,'fullyAuthored':325,'nullWrappers':2,'sharedRules':16,'conventions':91,'fex':15,'originalCases':660,'additionalCases':28,'curriculumPlacements':1838,'ritualPlacements':7},
            'failedChecks':fails,'details':checks,'candidateBuild':info(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json'),
            'readyForSubmission':False,'remainingAcceptanceWork':['FXC-04 complete row-by-row operative-state qualification','FXC-05 all acquisition/repeatability/training/capacity boundaries','FXC-06 actual clock/Endurance/work transitions','FXC-07 numeric/native resolution cases','FXC-08 physical/social sequences','FXC-09 spell/copy/command state','FXC-10 finite rejection variants and valid actor snapshots','FXC-12 complete evidence package and exact review request'],
            'runtimeCases':0,'catalogPromotions':0,'sourceInformationDeleted':0}
    target=A/'FEAT_EXACT_CANDIDATE_01_STRUCTURE_CHECK.json';assert not target.exists(),'Preserve previous check before replacing.'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('details',)},ensure_ascii=False,indent=2))
    raise SystemExit(1 if fails else 0)

if __name__=='__main__':main()
