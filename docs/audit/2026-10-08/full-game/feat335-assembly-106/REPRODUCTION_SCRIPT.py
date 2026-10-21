"""One-shot, data-only assembly of preserved feat review successors.

Does not import project/downloaded code or alter canonical files. A successful
output directory is never reused. Reproduction is for inspection, not rerunning
previous successful evidence programs.
"""
from pathlib import Path
from copy import deepcopy as dc
import json, hashlib, datetime, zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
D = A / 'feat335-ft84-derived-review-92/after/DescentReviewChanges/ReviewBible'
C = A / 'copy-ready-preparation-only-part5-successor-01'
OUT = A / 'feat335-assembly-106'
assert not OUT.exists(), 'One-shot output already exists; preserve it.'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
STATUS = 'Derived complete-text assembly 106; exact parent review and integration pending.'
inputs, checks, operations = {}, [], []

def digest(b): return hashlib.sha256(b).hexdigest()
def canon(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def read(p):
    p = Path(p).resolve()
    b = p.read_bytes()
    inputs[str(p)] = b
    return b
def js(p): return json.loads(read(p).decode('utf-8-sig'))
def binding(p):
    b = read(p)
    return {'path': str(Path(p).resolve()), 'bytes': len(b), 'sha256': digest(b)}
def ck(name, result):
    checks.append({'name': name, 'passed': bool(result)})
    assert result, name
def ptr(obj, path):
    for k in path.strip('/').split('/') if path else []:
        k = k.replace('~1', '/').replace('~0', '~')
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    return obj
def escape(k): return str(k).replace('~', '~0').replace('/', '~1')
def diff(before, after, artifact, path=''):
    if before == after: return
    if isinstance(before, dict) and isinstance(after, dict):
        for k in before.keys() | after.keys():
            p = path + '/' + escape(k)
            if k not in before or k not in after:
                operations.append({'artifact': artifact, 'pointer': p, 'beforeExists': k in before,
                    'before': dc(before.get(k)), 'afterExists': k in after, 'after': dc(after.get(k))})
            else: diff(before[k], after[k], artifact, p)
    elif isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        for n, (x, y) in enumerate(zip(before, after)): diff(x, y, artifact, path + '/' + str(n))
    else:
        operations.append({'artifact': artifact, 'pointer': path, 'beforeExists': True,
            'before': dc(before), 'afterExists': True, 'after': dc(after)})
def apply_ops(obj, ops, reverse=False):
    obj = dc(obj)
    for o in reversed(ops) if reverse else ops:
        parts = o['pointer'].strip('/').split('/')
        parent = ptr(obj, '/' + '/'.join(parts[:-1])) if len(parts) > 1 else obj
        key = parts[-1].replace('~1', '/').replace('~0', '~')
        key = int(key) if isinstance(parent, list) else key
        exists = (0 <= key < len(parent)) if isinstance(parent, list) else key in parent
        old, new = ('after', 'before') if reverse else ('before', 'after')
        assert exists == o[old + 'Exists']
        if exists: assert parent[key] == o[old]
        if o[new + 'Exists']: parent[key] = dc(o[new])
        else: del parent[key]
    return obj
def allow(v, keys): return {k: dc(v[k]) for k in keys.split()}
def overlay(base, public):
    # Only fields already explicitly published in the bound candidate are read.
    if isinstance(base, dict) and isinstance(public, dict):
        result = dc(base)
        for k, v in public.items(): result[k] = overlay(result[k], v) if k in result else dc(v)
        return result
    if isinstance(base, list) and isinstance(public, list) and len(base) == len(public):
        return [overlay(x, y) for x, y in zip(base, public)]
    return dc(public)

I = 'data/director/feat_candidates/exact_01/'
U = 'data/public/feat_candidates/exact_01/'
before = {I+'candidate.json': js(D/I/'candidate.json'), U+'candidate.json': js(D/U/'candidate.json'),
    I+'shared_rules.json': js(D/I/'shared_rules.json'), U+'shared_rules.json': js(D/U/'shared_rules.json'),
    I+'supplements.json': js(D/I/'supplements.json'), U+'supplements.json': js(D/U/'supplements.json'),
    'acquisition_contracts.json': js(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'),
    'acquisition_assembly.json': js(A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json')}
after = dc(before)
internal, pubbase = after[I+'candidate.json'], before[U+'candidate.json']
copy_public = js(C/'successor/DescentReviewChanges/ReviewBible'/U/'candidate.json')
copy_shared = js(C/'successor/DescentReviewChanges/ReviewBible'/U/'shared_rules.json')
copy_sup = js(C/'successor/DescentReviewChanges/ReviewBible'/U/'supplements.json')
copy_baseline = js(C/'baseline_original/DescentReviewChanges/ReviewBible'/U/'candidate.json')
copy_ops = js(C/'ALTERNATIVE_RULE_OPERATIONS_FROM_ORIGINAL.json')
js(C/'POLICY_SELECTION.json')
js(C/'OWNER_DIRECTION_CONTEXT.json')
js(C/'REVIEW_RECEIPT.json')
js(C/'CASE_DISPOSITIONS.json')
js(C/'ORIGINAL_AND_REVISED_EXAMPLES.json')
coverage = js(A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_105.json')
defense = js(A/'FEAT335_DEFENSE_ORIGINAL_CASEBOOK_REVIEW_97.json')
mental_source = defense['fullRetainedSourceMentalPredicate']
ck('Mental source exact bytes', binding(G/mental_source['source']['path'])['sha256'] == mental_source['source']['sha256'])
mental_original = js(G/mental_source['source']['path'])
ck('Mental source complete text', ptr(mental_original, mental_source['pointer']) == mental_source['completeText'])
mental = mental_source['completeText'].split(': ', 1)[1].split('; this classification needs the full spell/class conference.')[0] + '.'
mental = 'CURRENT ADOPTED MENTAL-EFFECT PREDICATE (FS-05). ' + mental[0].upper() + mental[1:]
mental += ' This is the finite source definition already adopted for Iron Will and Resilient Mind; it supplies no new roll, immunity or concentration permission.'

copied_ids = ['arcane_adaptation', 'eldritch_echo', 'mimicry']
by_copy = {r['id']: r for r in copy_public['feats']}
by_copy_base = {r['id']: r for r in copy_baseline['feats']}
by_public_base = {r['id']: r for r in pubbase['feats']}
for row in internal['records']:
    ident = row['id']
    if ident in copied_ids:
        for key in ['operationalRules', 'payloadOperational']:
            ck(ident+' disjoint merge '+key, by_public_base[ident][key] == by_copy_base[ident][key])
            row[key] = dc(by_copy[ident][key])
    if ident in ['iron_will', 'resilient_mind']:
        row['operationalRules'] = row['operationalRules'].replace('shared proposed finite predicate', 'current adopted finite predicate in FS-05') + '\n\n' + mental
        row['payloadOperational'] = row['operationalRules']

shared = after[I+'shared_rules.json']
ck('Shared copy baseline unchanged before merge', before[U+'shared_rules.json']['rules'][7] == js(C/'baseline_original/DescentReviewChanges/ReviewBible'/U/'shared_rules.json')['rules'][7])
shared['rules'][7]['wording'] = copy_shared['rules'][7]['wording']
shared['rules'][4]['wording'] += '\n\n' + mental
after[U+'shared_rules.json'] = dc(shared)
ck('All 16 shared rules match across complete envelopes', len(shared['rules']) == 16 and shared == after[U+'shared_rules.json'])

ck('All public supplements match pre-successor source', before[U+'supplements.json'] == js(C/'baseline_original/DescentReviewChanges/ReviewBible'/U/'supplements.json'))
private_groups = after[I+'supplements.json']['groups']
for private, public in zip(private_groups, copy_sup['groups']):
    ck('Supplement identity '+private['id'], private['id'] == public['id'])
    private['completeAuthoringValue'] = overlay(private['completeAuthoringValue'], public['value'])

def public_supplement(g):
    v = g['completeAuthoringValue']; ident = g['id']
    if ident == 'SUP-01': p = allow(v, 'profile nativeBody actions conversion recovery')
    elif ident == 'SUP-02': p = [allow(x, 'id name eligibleBody abilities movement attack sense limits') for x in v]
    elif ident == 'SUP-03': p = [allow(x, 'id name activation cost procedure') for x in v]
    elif ident == 'SUP-04':
        p = {}
        for name, row in v.items():
            p[name] = allow(row, 'featCastingAbility rank0Choices rank1Choices selection ordinaryMinimumClassLevelsArePreservedButNotFeatAcquisitionTax')
            p[name]['choices'] = [allow(x, 'id name rank school sourceClass fullOriginalClassAccessRow') for x in row['choices']]
    elif ident == 'SUP-05':
        p = {'newSpellFocus': allow(v['newSpellFocus'], 'id name sourceRegistryEntry prerequisite effect castingPrerequisitePolicyRef'),
             'newLegacyInitiateCurricula': {k:allow(x, 'ability notice cantrips rank1') for k,x in v['newLegacyInitiateCurricula'].items()},
             'newRitualTagOverlay': allow(v['newRitualTagOverlay'], 'ids placement'),
             'newDetectThoughts': allow(v['newDetectThoughts'], 'id rank school completeProcedureInFeat ordinaryClassAccess explicitComparisonOnly')}
    elif ident == 'SUP-06': p = [allow(x, 'id name rank school sourceClass fullOriginalClassAccessRow') for x in v]
    elif ident == 'SUP-07':
        cp = allow(v['copyProfileContract'], 'capture rankAndPayment numericBound lifecycle castFamilyKeyContract concentrationRules strainEngineRef strainEngineRules readyAllowanceDecision')
        cp['profiles'] = [allow(x, 'id role activation range resolution concentrationRequired') for x in v['copyProfileContract']['profiles']]
        flora = allow(v['floraBody'], 'size statistics dc cadence endpoints commandChoice')
        flora['modes'] = [allow(x, 'id command trap burstType') for x in v['floraBody']['modes']]
        p = {'copyProfileContract':cp, 'eldritchBlast':allow(v['eldritchBlast'], 'id name rank castingAbility castingTime components rangeFeet effect grant'),
             'pactSigils':[allow(x, 'id effect') for x in v['pactSigils']], 'floraBody':flora,
             'minorBuffTransfer':allow(v['minorBuffTransfer'], 'guidance resistance true-strike finalClarification'),
             'timeTagOverlay':allow(v['timeTagOverlay'], 'spellIds condition'), 'naturePredicate':allow(v['naturePredicate'], 'castingClassRoutes exclusions')}
    elif ident == 'SUP-08': p = [allow(x, 'die id name procedure') for x in v]
    elif ident == 'SUP-09': p = [allow(x, 'sourceId name actualSourceClass minimumBorrowerTotalLevel proposedBorrowedProcedure') for x in v]
    else: raise AssertionError(ident)
    return {'id':ident, 'cohort':g['cohort'], 'status':next(x['status'] for x in copy_sup['groups'] if x['id']==ident), 'selectionEnabled':False, 'value':p}

public_groups = [public_supplement(x) for x in private_groups]
ck('Explicit public supplement allowlist exactly reproduces selected full public source', public_groups == copy_sup['groups'])
after[U+'supplements.json'] = {'status': copy_sup['status'], 'groups': public_groups}
source_registry = dc([x['sourceObject'] for x in pubbase['feats']])
ck('All 335 original objects equal internal registry', source_registry == internal['original335Registry'])
records = {x['id']:x for x in internal['records']}
reviewed = {x['id']:x for x in internal['unchangedReviewedFeats']}
public_rows = []
for src in source_registry:
    ident = src['id']
    if ident in reviewed:
        p = {'id':ident, 'name':src['name'], 'reviewStatus':by_public_base[ident]['reviewStatus'],
             'sourceObject':dc(src), 'unchangedReviewedRecord':dc(reviewed[ident])}
        ck('Unchanged full reviewed feat '+ident, p == by_public_base[ident])
    else:
        r = records[ident]
        p = allow(r, 'id name cohort sourceObject operationalRules workedCases payloadOperational selectionEnabled exactApproved runtimeApproved sharedRulesRef supplementsRef')
        p['reviewStatus'] = STATUS
    public_rows.append(p)
public = allow(pubbase, 'schemaVersion status sourceVerdictId createdAtUtc selectionEnabled runtimeImplemented humanBalanceApproved wholeGameFlowApproved sourceInformationDeleted cosmologyReviewed originalFeats unchangedReviewedFeats sourceAuthoredCandidates deferredNullWrappers newSupplementsAreOutsideOriginalCounts')
public['feats'] = public_rows
public['status'] = internal['status'] = STATUS
public['createdAtUtc'] = internal['createdAtUtc'] = NOW
internal['assemblyScope'] = 'Derived full-text synchronization of D92 FT84, current paid-copy/Ready sources and adopted finite mental predicate, with all original case-review references. No canonical integration or parent acceptance.'
after[U+'candidate.json'] = public

contracts = after['acquisition_contracts.json']
by_contract = {x['id']:x for x in contracts['records']}
for row in public_rows:
    if row['id'] in records: by_contract[row['id']]['completeOperativeProcedure'] = row['operationalRules']
contracts['status'] = STATUS
contracts['candidateReadyForSubmission'] = False
acq = after['acquisition_assembly.json']
for e in acq['entries']:
    row = next(x for x in public_rows if x['id'] == e['id'])
    e['currentPublic'] = dc(row)
    e['currentCompleteContract'] = dc(by_contract[e['id']])
    if e['id'] in records: e['reviewedAcquisitionDescriptor']['completeControllingOperativeProcedure'] = row['operationalRules']
    e['all335FullAcquisitionsExecuted'] = False
acq['status'] = STATUS

# Full exact original cases are paired with the complete authored review at each
# original position. This assembles evidence; it does not rerun those programs.
assembled_cases = {'id':'FEAT335-ALL-CASE-REVIEWS-106', 'ordinary':[], 'additional':[],
    'runtimeExecuted':False, 'parentAccepted':False, 'historicalProgramsRerun':False}
for group, expected in [('ordinary',660), ('additional',28)]:
    for position in coverage[group]['positions']:
        b = position['reviewEvidenceReport']; rp = G/b['path']
        raw = read(rp)
        ck('Case evidence bytes '+position['id'], len(raw)==b['bytes'] and digest(raw)==b['sha256'])
        review = dc(ptr(json.loads(raw.decode('utf-8-sig')), position['reviewEvidencePointer']))
        ck('Case evidence identity '+position['id'], review['id']==position['id'])
        assembled_cases[group].append({'position':dc(position), 'completeReview':review})
    ck('Complete unique '+group+' cases', len(assembled_cases[group])==expected and len({x['position']['id'] for x in assembled_cases[group]})==expected)
original_cases = js(G/coverage['originalCasebook']['path'])
additional_cases = js(G/coverage['additionalBoundaryCasebook']['path'])

# Preserve all D92 supporting data, including external language/crafting mirrors.
support = {}
for p in sorted(D.rglob('*')):
    if p.is_file():
        rel = p.relative_to(D).as_posix()
        support[rel] = read(p)
for name in ['example_dispositions.json','additional_boundary_expectations.json','convention_dispositions.json','fex_dispositions.json','source_conflict_dispositions.json']:
    ck('Required source artifact retained '+name, I+name in support)

protected = [R/'data/public/spell_playtests/authored_review_index.json',
    R/'data/director/spell_review/accepted_interface_registry_06.json'] + [R/'tools'/n for n in
    ['feat335_copy_capture.py','feat335_copy_release.py','feat335_copy_payloads.py','feat335_copy_class_release.py']]
protected_before = [binding(p) for p in protected]

for key in sorted(before):
    diff(before[key], after[key], key)
    ops = [o for o in operations if o['artifact']==key]
    ck('Full forward JSON reconstruction '+key, apply_ops(before[key], ops)==after[key])
    ck('Full reverse JSON reconstruction '+key, apply_ops(after[key], ops, True)==before[key])
for row in public_rows:
    ident = row['id']
    ck('Original object unchanged '+ident, row['sourceObject']==by_public_base[ident]['sourceObject'])
    if ident in records:
        r = records[ident]
        ck('Independent full public/internal equality '+ident, all(row[k]==r[k] for k in ['sourceObject','operationalRules','workedCases','payloadOperational']))
        ck('Historical complete source direction unchanged '+ident, r['sourceDirection']==next(x for x in before[I+'candidate.json']['records'] if x['id']==ident)['sourceDirection'])
        ck('Current acquisition procedure '+ident, by_contract[ident]['completeOperativeProcedure']==r['operationalRules'])
ck('327 original questions and two null payloads',len(records)==327 and sum(x['payloadOperational'] is None for x in records.values())==2)
ck('Eight reviewed originals unchanged',len(reviewed)==8 and internal['unchangedReviewedFeats']==before[I+'candidate.json']['unchangedReviewedFeats'])
ck('Concentration tags retained', {p['id'] for p in public_groups[6]['value']['copyProfileContract']['profiles'] if p['concentrationRequired']}=={'ward','hindrance','boon'})

OUT.mkdir()
def write(rel, data):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(data if isinstance(data,bytes) else data.encode('utf-8'))
def save(rel, obj): write(rel,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
for rel,b in support.items(): write('after/'+rel,b)
for key,obj in after.items():save('after/'+key,obj)
save('EXACT_OPERATIONS.json',{'id':'FEAT335-ASSEMBLY-106', 'scope':STATUS, 'operations':operations,
    'beforeBytesRetainedInSourceMap':True,'canonicalApplication':False})
save('ALL_CASE_REVIEWS.json',assembled_cases)
save('MENTAL_PREDICATE_PROVENANCE.json',{'fullSourceReceipt':mental_source,'currentCompleteWording':mental,
    'historicalConferenceSentenceRetainedOnlyInReceipt':True,'newMechanicAuthored':False})

DOC='after/docs/feats/exact-candidate-01/'
cohorts = list(dict.fromkeys(r['cohort'] for r in internal['records']))
def block(v):return ['```json',json.dumps(v,ensure_ascii=False,indent=2),'```','']
for cohort in cohorts:
    current=['# '+cohort.replace('_',' ').title()+' feats','',STATUS,'',
        '[Shared rules](SHARED_RULES.md) · [Finite supplements](SUPPLEMENTS.md) · [Spell payloads](SPELL_PAYLOADS.md)','']
    audit=['# '+cohort.replace('_',' ').title()+' — source reconciliation','',STATUS,'',
        'Original source decisions below are historical receipts. The complete current candidate procedure and linked complete case review control this derived reading.','']
    for r in internal['records']:
        if r['cohort']!=cohort:continue
        current += ['## '+r['name']+' (`'+r['id']+'`)','', '**Printed prerequisite:** '+str(r['sourceObject'].get('prerequisite','No printed prerequisite.')),'',r['operationalRules'],'','### Authored examples','']
        current += [x+'\n' for x in r['workedCases']]
        if r['payloadOperational'] is None:current += ['Unavailable: this preserved grant wrapper has a null operational payload.','']
        relevant=[{'id':x['position']['id'],'report':x['position']['reviewEvidenceReport'],'pointer':x['position']['reviewEvidencePointer']} for group in assembled_cases.values() if isinstance(group,list) for x in group if x['position']['featId']==r['id']]
        audit += ['## '+r['questionId']+' — '+r['name'],'','### Complete original object','']+block(r['sourceObject'])
        audit += ['### Original question','']+block(r['originalQuestion'])
        audit += ['### Preserved original source direction (historical)','']+block(r['sourceDirection'])
        audit += ['### Complete current candidate procedure','',r['operationalRules'],'','### Original-position authored review references','']+block(relevant)
    write(DOC+cohort.upper()+'.md','\n'.join(current))
    write(DOC+'source-audit/'+cohort.upper()+'.md','\n'.join(audit))
    for r in internal['records']:
        if r['cohort']==cohort:ck('Complete current text rendered twice '+r['id'],r['operationalRules'] in '\n'.join(current) and r['operationalRules'] in '\n'.join(audit))
lines=['# Shared feat rules','',STATUS,'']
for r in shared['rules']:lines += ['## '+r['id']+' — '+r['title'],'',r['wording'],'']
write(DOC+'SHARED_RULES.md','\n'.join(lines))
lines=['# Complete finite feat supplements','',STATUS,'','These separately identified supplements do not add original registry identities or activate deferred payloads.','']
for g in public_groups:lines+=['## '+g['id'],'']+block(g['value'])
write(DOC+'SUPPLEMENTS.md','\n'.join(lines))
lines=['# All original feat cases and complete authored reviews','',STATUS,'','660 original positions and 28 additional boundaries. Authored semantic review and bounded calculations are distinct from game-runtime tests.','']
for group in ['ordinary','additional']:
    for c in assembled_cases[group]:lines+=['## '+c['position']['id'],'']+block(c)
write(DOC+'source-audit/CASEBOOK.md','\n'.join(lines))
lines=['# Eight unchanged reviewed feats','',STATUS,'']
for r in internal['unchangedReviewedFeats']:lines+=['## '+r['name'],'']+block(r)
write(DOC+'UNCHANGED_REVIEWED.md','\n'.join(lines))
lines=['# Complete feat candidate assembly 106','',STATUS,'',
    'All 335 original identities remain: eight unchanged reviewed records, 325 authored procedures and two unavailable null wrappers. No runtime selection, canonical integration, whole-game, balance or cosmology approval is granted.','',
    '[Shared rules](SHARED_RULES.md) · [Supplements](SUPPLEMENTS.md) · [Spell payloads](SPELL_PAYLOADS.md) · [Eight unchanged records](UNCHANGED_REVIEWED.md) · [Complete case reviews](source-audit/CASEBOOK.md)','',
    '## Cohorts','']
for c in cohorts:lines+=['- ['+c.replace('_',' ').title()+']('+c.upper()+'.md) · [Complete source reconciliation](source-audit/'+c.upper()+'.md)']
lines+=['','## Review state','',
    'The complete-copy wording, preparation-only Ready allowance, six FT84 successors and adopted mental predicate are synchronized across the derived files. All 660 original cases and 28 added boundaries are linked to their complete preserved authored reviews. Historical programs were not rerun.','',
    'This mechanical assembly does not assert every FXC acceptance gate fulfilled. Current acquisition evidence, all source dependencies, deferred payloads and the exact-parent submission checklist still require final reconciliation before requesting acceptance. The four copy helpers remain unmodified and do not implement this Ready successor.','']
write(DOC+'README.md','\n'.join(lines))

# Short archived source names avoid Windows MAX_PATH while retaining exact paths.
source_map=[]
for n,(path,b) in enumerate(sorted(inputs.items()),1):
    ext=Path(path).suffix.lower() or '.bin';member='sources/'+f'{n:03d}'+ext
    write(member,b);source_map.append({'file':member,'originalPath':path,'bytes':len(b),'sha256':digest(b)})
save('SOURCE_MAP.json',source_map)
save('BASELINE_MAP.json',{key:next(x for x in source_map if x['originalPath']==str((D/key if key not in ['acquisition_contracts.json','acquisition_assembly.json'] else A/('FEAT_EXACT_01_ACQUISITION_CONTRACTS.json' if key=='acquisition_contracts.json' else 'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json')).resolve())) for key in before})
write('REPRODUCTION_SCRIPT.py',Path(__file__).read_bytes())
for p in protected:ck('Protected input unchanged '+p.name,p.read_bytes()==inputs[str(p.resolve())])
for path,b in inputs.items():ck('Source bytes unchanged '+path,Path(path).read_bytes()==b)
report={'id':'FEAT335-ASSEMBLY-106-REPORT','recordedAtUtc':NOW,'status':STATUS,
    'inputFiles':len(inputs),'originalIdentities':335,'originalQuestions':327,'unchangedReviewed':8,'authoredProcedures':325,'nullWrappers':2,
    'ordinaryCases':660,'additionalBoundaries':28,'cohortChapters':len(cohorts),'sharedRules':16,'supplementGroups':9,
    'copyIds':copied_ids,'mentalIds':['iron_will','resilient_mind'],'exactFieldOperations':len(operations),
    'scope':'Complete text/source/mirror reconstruction and evidence assembly only. Full acquisition execution, acceptance gates, runtime and gameplay are not inferred.',
    'passed':len(checks),'failed':0,'checks':checks,'protectedInputs':protected_before,
    'historicalProgramsRerun':False,'downloadedCodeExecuted':False,'canonicalApplied':False,'parentAccepted':False,
    'candidateReadyForExactSubmission':False,'runtimeImplemented':False,'humanBalanceApproved':False,'sourceInformationDeleted':False,'cosmologyReviewed':False}
save('ASSEMBLY_REPORT.json',report)
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():
        b=p.read_bytes();manifest.append({'file':p.relative_to(OUT).as_posix(),'bytes':len(b),'sha256':digest(b)})
save('MANIFEST.json',{'files':manifest,'count':len(manifest),'selfHashRecordedOutsideArchive':True})
zp=A/'DD_Feat335_Assembled_106.zip'
assert not zp.exists()
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for m in manifest:
        b=z.read(m['file']);assert len(b)==m['bytes'] and digest(b)==m['sha256']
receipt={'id':'FEAT335-ASSEMBLY-106-RECEIPT','recordedAtUtc':NOW,'directory':str(OUT),'zip':{'path':str(zp),'bytes':zp.stat().st_size,'sha256':digest(zp.read_bytes())},'report':{'path':str(OUT/'ASSEMBLY_REPORT.json'),'bytes':(OUT/'ASSEMBLY_REPORT.json').stat().st_size,'sha256':digest((OUT/'ASSEMBLY_REPORT.json').read_bytes())},'manifest':{'path':str(OUT/'MANIFEST.json'),'sha256':digest((OUT/'MANIFEST.json').read_bytes())},'passed':len(checks),'failed':0,'archiveMembers':len(manifest)+1,'canonicalApplied':False,'parentAccepted':False,'next':'Reconcile current acquisition/evidence and FXC exact-submission gates, then submit complete candidate to GPT.'}
(A/'FEAT335_ASSEMBLY_RECEIPT_106.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
