"""Current-source dependency comparison and a non-activating review proposal."""
from pathlib import Path
from copy import deepcopy as dc
import json, hashlib, collections, datetime, zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
P=A/'feat335-assembly-106/after';O=A/'feat335-spell-dependencies-107';assert not O.exists()
sources={};checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):
    p=p.resolve();b=p.read_bytes();sources[str(p)]=b;return json.loads(b.decode('utf-8-sig'))
def binding(p):
    p=p.resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def ptr(o,s):
    for k in s.strip('/').split('/') if s else []:o=o[int(k)] if isinstance(o,list) else o[k.replace('~1','/').replace('~0','~')]
    return o
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n

deps=read(P/'data/public/feat_candidates/exact_01/spell_dependencies.json')
placements=read(P/'data/public/feat_candidates/exact_01/spell_placements.json')
public=read(P/'data/public/feat_candidates/exact_01/candidate.json')
internal=read(P/'data/director/feat_candidates/exact_01/candidate.json')
supplements=read(P/'data/public/feat_candidates/exact_01/supplements.json')
index=read(R/'data/public/spell_playtests/authored_review_index.json');by_index={x['id']:x for x in index['entries']}
catalog=read(R/'data/public/spell_playtests/catalog.json');by_catalog={x['id']:x for x in catalog['spells']}
cache={};comparisons=[];drift=[]
for ident,dep in deps['spells'].items():
    row=by_index[ident];path=(R/'data/public/spell_playtests'/row['procedureFile']).resolve()
    if str(path) not in cache:cache[str(path)]=read(path)
    card=ptr(cache[str(path)],row['wholeCardPointer'])
    ck('Current complete card identity '+ident,card['id']==ident)
    same=card==dep['completeCurrentProcedureCard'];index_same=row==dep['authoredIndexEntry']
    if not same or not index_same:drift.append(ident)
    comparisons.append({'id':ident,'completeCardMatches':same,'currentIndexMatches':index_same,
        'retainedCardSha256CanonicalJson':sha(canonical(dep['completeCurrentProcedureCard'])),
        'currentCardSha256CanonicalJson':sha(canonical(card)),
        'currentSource':binding(path),'currentPointer':row['wholeCardPointer'],
        'grantRoute':'deferred feat wrapper; no activation' if ident in ['astral-projection','planar-binding'] else 'bounded curriculum/ritual placement only'})
ck('Only discovered current dependency divergence',drift==['planar-binding'])
for n,row in enumerate(placements['placements']):
    ident=row['id'];access=by_catalog[ident]['classAccess'][row['sourceClass']]
    ck('Exact original class placement '+str(n),row['fullOriginalClassAccessRow']==access)
    ck('Exact named rank/school '+str(n),row['rank']==access['rank'] and row['school']==access['school'])
    current=by_index[ident]
    ck('Current actual selected payload '+str(n),current['authoredStatus']=='reviewed-authored-operational-playtest' and deps['spells'][ident]['authoredIndexEntry']==current)
    ck('Deferred wrapper absent from selected placements '+str(n),ident not in ['planar-binding','astral-projection'])
groups={x['id']:x['value'] for x in supplements['groups']}
expected=[]
for name,curriculum in groups['SUP-04'].items():
    for row in curriculum['choices']:expected.append(('curriculum',name,row['id'],row['rank'],row['school'],row['sourceClass']))
for row in groups['SUP-06']:expected.append(('ritual',None,row['id'],row['rank'],row['school'],row['sourceClass']))
actual=[(x['route'],x.get('curriculum'),x['id'],x['rank'],x['school'],x['sourceClass']) for x in placements['placements']]
ck('Complete curriculum and ritual multiset',collections.Counter(expected)==collections.Counter(actual))
ck('All16 curricula and7 ritual entries retained',len(groups['SUP-04'])==16 and len(groups['SUP-06'])==7)

ac5receipt=read(A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json')
authority_path=G/ac5receipt['acceptanceAuthority']['path'];authority=read(authority_path)
ck('Actual AC5 authority bytes',binding(authority_path)['sha256']==ac5receipt['acceptanceAuthority']['sha256'])
ck('Ordinary Planar Binding actually accepted','planar-binding' in authority['moduleIdentity']['spellIds'] and authority['verdict']=='ACCEPT_FOR_AUTHORED_CAMPAIGN_PLAYTEST_INTEGRATION')
current_index=by_index['planar-binding'];ac5path=(R/'data/public/spell_playtests'/current_index['procedureFile']).resolve()
ck('Current full AC5 envelope hash matches acceptance',binding(ac5path)['sha256']==ac5receipt['completeEnvelope']['sha256'])
ac5=cache[str(ac5path)];current_card=ptr(ac5,current_index['wholeCardPointer'])
ck('AC5 retains separate unapproved cosmology','cosmology canon' in authority['notApproved'])
feat=next(x for x in internal['records'] if x['id']=='planar_binding')
pubfeat=next(x for x in public['feats'] if x['id']=='planar_binding')
ck('Feat still explicitly null and disabled',feat['payloadOperational'] is None and pubfeat['payloadOperational'] is None and not pubfeat['selectionEnabled'])

proposed_reading=feat['operationalRules'].split('\n\n')[0].replace('defined by the eventual completed spell','defined by the accepted ordinary spell, if separately authorized for this feat grant')
proposed_reading += '\n\nCURRENT DEPENDENCY STATUS: the ordinary Planar Binding spell has an accepted authored procedure in DD-AC5-EXACT-ACCEPTANCE-05. Its complete current card and source access are retained separately. That ordinary-spell acceptance does not itself activate this separate feat grant: this candidate retains payloadOperational=null and selectionEnabled=false under its original deferred-wrapper boundary. No cast, charge debit, target eligibility or service record is produced through this feat while that boundary remains. Retain the original feat source verdict and post-push dependency as historical/authorization evidence; exact parent review must expressly resolve the feat wrapper before any later integration. This status correction authors no planar taxonomy, native or soul origin, destination, consent rule, cosmology canon or new ordinary-spell procedure.'
proposed_dependency=dc(deps['spells']['planar-binding'])
proposed_dependency['historicalDeferredDependencyRecord']=dc(deps['spells']['planar-binding'])
proposed_dependency['authoredIndexEntry']=dc(current_index)
proposed_dependency['completeCurrentProcedureCard']=dc(current_card)
proposed_dependency['binding']={'file':ac5path.relative_to(G).as_posix(),**{k:v for k,v in binding(ac5path).items() if k!='path'},'pointer':current_index['wholeCardPointer']}
proposed_dependency['featGrantBoundary']={'featId':'planar_binding','payloadOperational':None,'selectionEnabled':False,'ordinaryAcceptanceIsNotFeatAcceptance':True,'sourceReceipt':dc(ac5receipt['acceptanceAuthority'])}
proposal={'id':'FEAT335-PLANAR-DEPENDENCY-107','status':'PROPOSED_EDITORIAL_DEPENDENCY_CORRECTION_PENDING_GPT_CONFERENCE',
    'discovery':'283 of284 complete dependency cards still match current sources; only the retained Planar Binding receipt predates its ordinary AC5 acceptance. All1845 actual curriculum/ritual rows remain exact and exclude both deferred wrappers.',
    'before':{'completePrivateFeat':feat,'completePublicFeat':pubfeat,'completeDependency':deps['spells']['planar-binding']},
    'currentOrdinarySource':{'completeIndexEntry':current_index,'completeCard':current_card,'completeEnvelopeBinding':binding(ac5path),'acceptanceReceipt':binding(A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'),'acceptanceAuthority':authority},
    'proposed':{'completeReadingProcedure':proposed_reading,'completeDependency':proposed_dependency,'payloadOperational':None,'selectionEnabled':False},
    'exactQuestion':'Confirm a current-reference-only correction with both feat wrappers remaining null/unavailable, or name exact source-supported replacement wording. Do not infer that ordinary AC5 acceptance approves the separate feat grant or reopen accepted AC5 mechanics/cosmology.',
    'notClaimed':['feat activation','parent335 acceptance','ordinary AC5 re-review','runtime implementation','new cosmology','post-push canon review'],
    'canonicalApplied':False,'derived106FilesChanged':False,'newMechanicAuthored':False,'actuallySentToGpt':False}

# Retain historic source bindings and identify the two genuine later changes.
historical_bindings=[]
for path,old in internal['sourceFileBindings'].items():
    p=G/path;now=binding(p)
    historical_bindings.append({'path':path,'historical':old,'current':now,'same':old['bytes']==now['bytes'] and old['sha256']==now['sha256']})
ck('Historical source-binding drift remains exactly the two updated spell registries',sum(not x['same'] for x in historical_bindings)==2)
for path,raw in sources.items():ck('All inspected inputs unchanged '+path,Path(path).read_bytes()==raw)

O.mkdir()
def save(name,obj):
    p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('PLANAR_DEPENDENCY_PROPOSAL.json',proposal)
report={'id':'FEAT335-SPELL-DEPENDENCY-AUDIT-107','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Current-source equality and exact class/rank/school placement audit for FXC04/11; no ordinary-spell runtime rerun or null-feat activation.',
    'dependencyCount':284,'exactCurrentCardMatches':283,'dependencyDivergenceIds':drift,
    'selectedPlacements':len(actual),'curriculumPlacements':sum(x[0]=='curriculum' for x in actual),'ritualPlacements':sum(x[0]=='ritual' for x in actual),
    'comparisons':comparisons,'historicalSourceBindingComparisons':historical_bindings,
    'consequence':'Current Planar Binding source/reference status must be reconciled before exact parent submission. Ordinary AC5 acceptance and the null feat wrapper remain separately governed.',
    'passed':len(checks),'failed':0,'checks':checks,'canonicalApplied':False,'parent335Accepted':False,'allFXCGatesFulfilled':False,'runtimeExecuted':False,'newCosmology':False,'historicalValidatorsRerun':False}
save('AUDIT_REPORT.json',report)
sm=[]
for n,(path,raw) in enumerate(sorted(sources.items()),1):
    name='sources/'+f'{n:03d}'+Path(path).suffix;p=O/name;p.parent.mkdir(exist_ok=True);p.write_bytes(raw)
    sm.append({'file':name,'originalPath':path,'bytes':len(raw),'sha256':sha(raw)})
save('SOURCE_MAP.json',sm);(O/'REPRODUCTION_SCRIPT.py').write_bytes(Path(__file__).read_bytes())
manifest=[]
for p in sorted(O.rglob('*')):
    if p.is_file():manifest.append({'file':p.relative_to(O).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
save('MANIFEST.json',{'files':manifest})
zpath=A/'DD_Feat335_Spell_Dependencies_107.zip';assert not zpath.exists()
with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(O.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(O).as_posix())
with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None
    for m in manifest:
        raw=z.read(m['file']);assert len(raw)==m['bytes'] and sha(raw)==m['sha256']
receipt={'id':report['id'],'report':binding(O/'AUDIT_REPORT.json'),'proposal':binding(O/'PLANAR_DEPENDENCY_PROPOSAL.json'),'zip':binding(zpath),'passed':len(checks),'failed':0,'currentCardMatches':283,'selectedPlacements':1845,'openDependencyIds':drift,'actuallySentToGpt':False,'canonicalApplied':False}
(A/'FEAT335_SPELL_DEPENDENCIES_RECEIPT_107.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
