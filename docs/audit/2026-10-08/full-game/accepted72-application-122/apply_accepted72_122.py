"""Local, non-runtime authoring integration. Run without --apply for preflight."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
O = A / 'spell-review-resume-116'
OUT = A / 'accepted72-application-122'
INDEX = R / 'data/public/spell_playtests/authored_review_index.json'
CATALOG = R / 'data/public/spell_playtests/catalog.json'
EXPECTED_INDEX = '6f9b86e21f6a69c7ba2469aba89d5907aa08da567226a2c4bd3ced9e09409857'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def encoded(x):
    return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def binding(p, data=None):
    b = p.read_bytes() if data is None else data
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha(b)}

def verify(p, expected):
    b = p.read_bytes()
    assert sha(b) == expected['sha256'], ('hash mismatch', str(p))
    if 'bytes' in expected:
        assert len(b) == expected['bytes'], ('size mismatch', str(p))
    return b

def walk_bindings(x):
    if isinstance(x, dict):
        if 'sha256' in x and ('path' in x or 'file' in x):
            yield x
        for k,v in x.items():
            if any(t in k.lower() for t in ('before','baseline','historical','originalreturn')):
                continue
            yield from walk_bindings(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk_bindings(v)

assert sha(INDEX.read_bytes()) == EXPECTED_INDEX, 'Live index changed; recompute rather than overwrite.'
before_bytes = INDEX.read_bytes()
before = read(INDEX)
assert before['authoredCounts'] == {'reviewed': 525, 'pending': 323}
assert sha(CATALOG.read_bytes()) == before['sourceCatalogSha256']
queue = read(O / 'CURRENT_SPELL_QUEUE_121.json')
accepted_ids = set(queue['acceptedIdentities'])
assert len(accepted_ids) == 72
plan = read(A / 'part5-accepted24-integration-staging-01/INTEGRATION_PLAN.json')
now = datetime.now(timezone.utc).isoformat()
writes = {}
source_bindings = {}

def stage(dest, data):
    assert dest.resolve().is_relative_to(G.resolve())
    if dest in writes:
        assert writes[dest] == data
    elif dest.exists():
        assert dest.read_bytes() == data, ('destination conflict', str(dest))
    writes[dest] = data

def exact_copy(src, dest, expected=None):
    b = verify(src, expected) if expected else src.read_bytes()
    source_bindings[str(src)] = binding(src, b)
    stage(dest, b)

specs = []
for cohort in plan['cohorts']:
    name = cohort['id']
    copies = [c for c in plan['canonicalCopies'] if c['cohort'] == name]
    for c in copies:
        exact_copy(G / c['source']['path'], G / c['proposedCanonicalDestination']['path'], c['source'])
    model_copy = next(c for c in copies if c['source']['path'].endswith('SPELLS_MODEL.json'))
    chapter_copy = next(c for c in copies if c['source']['path'].endswith('PLAYER_CHAPTER.md'))
    specs.append(dict(name=name, source=G/model_copy['source']['path'], model=G/model_copy['proposedCanonicalDestination']['path'],
                      chapter=G/chapter_copy['proposedCanonicalDestination']['path'], authority=G/cohort['acceptance']['path'],
                      expected=cohort['acceptedArtifactBindings'], root='spells', idkey='id', textkey='procedure',
                      rules='sharedRules', cases='currentCases', sourceDir=(G/model_copy['source']['path']).parent,
                      holdFile='REGISTER.json'))
    verify(G/cohort['acceptance']['path'], cohort['acceptance'])

for name, folder, authority, root, idkey, textkey, rules, cases, model_sha in [
 ('control15-ready14', 'copy-ready-preparation-only-part5-successor-01/successor', 'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json', 'spells','id','procedure','sharedContractRouting11','currentExamples','81200770f94be0b0bde1c018529eb8fe289ec1caedf8691bfe558555dce0b62e'),
 ('rank8-damage6', 'rank8-damage6-part5-cast-history-return-03', 'RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','records','spellId','procedure','selectedSharedRules','currentVectors','07e508c7135a65db2cabc98d6c8aa97b7f5feb4bc108b499f11b697aa904e656'),
 ('rank7-identity-casting5','rank7-identity-casting5-part5-ready-deadline-recovery-01','RANK7_IDENTITY_CASTING5_PART5_EXACT_AUTHORING_ACCEPTANCE_79.json','records','spellId','proposedProcedure','selectedSharedRules','currentVectors','949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a'),
 ('rank9-resonance3','rank9-resonance-fields3-feedback-receipt-return-02','RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json','records','spellId','procedure','selectedSharedRules','currentVectors','5b02270f39fce01c392b6e8187ce9e144f06957d908140c5c18cf96f1e78952a'),
 ('rank7-mechanics16','rank7-mechanics16-final-120','spell-review-resume-116/R7M16_FINAL_LOCAL_ACCEPTANCE_120.json','procedures','id','completeProcedure','sharedRules','currentCases','08390de18c1b2da3060bd5ad3a8e3473a83fba061ee7dcb245706a0f9da9ef33'),
 ('memory-creation3','memory-creation3-corrected-121','spell-review-resume-116/MEMORY_CREATION3_FINAL_LOCAL_ACCEPTANCE_121.json','spells','id','procedure','sharedRules','currentCases','36b540cd3078cea02c80abbcfff8568d2ff4a021da795b77cac6a2bdd08a4326')]:
    srcdir = A/folder
    src = srcdir/('CONTROL15_READY_REFERENCE_SUCCESSOR14.json' if name.startswith('control') else 'MODEL.json')
    dst = R/'data/public/spell_candidates'/f'{name.replace("-", "_")}_reviewed_122.json'
    exact_copy(src,dst,{'sha256':model_sha})
    specs.append(dict(name=name,source=src,model=dst,chapter=R/'docs/spells/candidates'/f'{name.upper().replace("-", "_")}_REVIEWED_122.md',
                      authority=A/authority,root=root,idkey=idkey,textkey=textkey,rules=rules,cases=cases,sourceDir=srcdir,holdFile='HOLD_REGISTER.json'))

after = copy.deepcopy(before)
entries = {e['id']:e for e in after['entries']}
seen = set()
cohort_receipts = []
verified_artifacts = 0
for s in specs:
    name = s['name']; source_dir=s['sourceDir']; model=read(s['source'])
    rows = model[s['root']]
    ids = [r[s['idkey']] for r in rows]
    assert not seen.intersection(ids)
    seen.update(ids)
    assert all(i in accepted_ids and entries[i]['authoredStatus']=='pending-authored-procedure' for i in ids)
    authority=read(s['authority'])
    # Verify current local artifacts against their exact package binding manifests.
    for manifest_name in ['ARTIFACT_BINDINGS.json','EVIDENCE_MANIFEST.json','SOURCE_HASHES.json']:
        manifest = source_dir/manifest_name
        if manifest.exists():
            for b in walk_bindings(read(manifest)):
                rel=b.get('path', b.get('file'))
                p=source_dir/rel
                if p.is_file() and p.parent == source_dir:
                    verify(p,b); verified_artifacts+=1
    # Exact accepted packages remain the complete historical/reference roots.
    evidence_files = {p.name:binding(p) for p in source_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.json','.md'}}
    holds_src=source_dir/s['holdFile']
    if name.startswith('control'):
        holds_src=A/'control15-full-conference-part5-return-02/HOLD_REGISTER.json'
    holds_dest=R/'data/director/spell_review'/f'{name.replace("-", "_")}_retained_holds_122.json'
    exact_copy(holds_src,holds_dest)
    # Use exact authored chapters where available. Otherwise render complete operative strings verbatim.
    if s['chapter'] not in writes:
        player=source_dir/'PLAYER_CHAPTER.md'
        if player.exists():
            exact_copy(player,s['chapter'])
        else:
            parts=[f'# {name}: accepted authored procedures', '', 'Applied to the authored-review index on owner instruction. Runtime selection remains disabled. Historical proposal labels in the exact source remain history.', '']
            for row in rows:
                text=row[s['textkey']]
                assert isinstance(text,str) and len(text)>100
                parts += [f'## {row.get("name",row[s["idkey"]])}', '', text, '']
            parts += ['## Complete scoped shared rules', '', '```json', json.dumps(model[s['rules']],ensure_ascii=False,indent=2), '```', '']
            if name.startswith('control'):
                parts += ['## Complete original shared proposals (apply only through the accepted routing above)', '', '```json',json.dumps(model['completeOriginalSharedProposals'],ensure_ascii=False,indent=2),'```','']
            stage(s['chapter'],'\n'.join(parts).encode('utf-8'))
    cases_dest=R/'data/playtest/spell_candidates'/f'{name.replace("-", "_")}_cases_122.json'
    if (source_dir/'CASEBOOK.json').exists():
        exact_copy(source_dir/'CASEBOOK.json',cases_dest)
    else:
        stage(cases_dest,encoded({'id':f'{name}-CASEBOOK-122','source':binding(s['source']),'sourcePointer':'/'+s['cases'],
                                 'cases':model[s['cases']], 'retainedHolds':binding(holds_dest,writes[holds_dest]),'runtimeExecuted':False}))
    receipt_path=OUT/f'{name}_APPLICATION.json'
    receipt={'id':f'{name.upper()}-APPLICATION-122','recordedAtUtc':now,'status':'APPLIED_AUTHORED_REVIEW_WITH_RETAINED_HOLDS',
             'ownerInstruction':'look at the 251 which need acceptance, whats wrong with them? Apply the 72',
             'acceptedIds':ids,'acceptedModelSource':binding(s['source']),'canonicalModel':binding(s['model'],writes[s['model']]),
             'authority':binding(s['authority']),'exactEvidenceRoot':source_dir.relative_to(G).as_posix(),'evidenceFiles':evidence_files,
             'chapter':binding(s['chapter'],writes[s['chapter']]),'casebook':binding(cases_dest,writes[cases_dest]),
             'holds':binding(holds_dest,writes[holds_dest]),'runtimeSelectionEnabled':False,'runtimeImplemented':False,
             'historicalPendingLabelsPreserved':True,'scope':'Select exact accepted authored procedures and cases. Preserve source access, original evidence, conditional premises and content holds. No balance, runtime or cosmology approval.',
             'supersession':'Only authoring-application reservation is discharged by the current owner instruction. Content and runtime holds remain.'}
    if name.startswith('control'):
        receipt['readySuccessorAuthority']=binding(A/'copy-ready-preparation-only-part5-successor-01/REVIEW_RECEIPT.json')
        receipt['readyPolicy']=binding(A/'copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json')
        receipt['readyLimitations']=binding(A/'copy-ready-preparation-only-part5-successor-01/RETAINED_LIMITATIONS.json')
        base=read(A/'control15-full-conference-part5-return-02/successor/CONTROL15_REVIEWED_SUCCESSOR13.json')
        assert model['spells']==base['spells'] and model['currentExamples']==base['currentExamples']
        receipt['readyNote']='Uses accepted successor14 metadata/reference; no feat files changed. Fifteen procedures and thirty cases equal accepted successor13.'
    if name=='rank9-resonance3':
        receipt['supersession']+=' RF9-LOCAL-SEMANTIC-ACCEPTANCE was discharged by exact acceptance90; all other qualifications remain.'
    if name.startswith('illusion'):
        receipt['laterDependencyAcceptances']=['Control15 and Mental Prison: exact accepted Control15 ready14 selected in this application.', 'Creation: exact MemoryCreation3 return02 selected in this application. Historical dependency review labels are not new content holds; their actual retained qualifications still govern.']
    stage(receipt_path,encoded(receipt))
    receipt_binding=binding(receipt_path,writes[receipt_path])
    cohort_receipts.append(receipt_binding)
    # Provide a canonical director navigation record without relocating relative evidence dependencies.
    director=R/'docs/director-only/spells'/f'{name.upper().replace("-", "_")}_APPLICATION_122.md'
    stage(director,(f'# {name}: application122\n\nAccepted exact evidence remains at `{source_dir.relative_to(G).as_posix()}`.\n\nApplication receipt: `{receipt_path.relative_to(G).as_posix()}`.\n\nRetained hold register: `{holds_dest.relative_to(G).as_posix()}`.\n\nCasebook: `{cases_dest.relative_to(G).as_posix()}`. All original examples and conditional branches are preserved. Historical pending/application labels inside source files are not current selection status. The application receipt records the limited supersessions; no content or runtime hold is silently cleared.\n').encode('utf-8'))
    for n,row in enumerate(rows):
        i=row[s['idkey']]; e=entries[i]; pointer=f'/{s["root"]}/{n}'
        assert isinstance(row[s['textkey']],str) and len(row[s['textkey']])>100
        e.update(sourceCatalogWholeCardPointer=e['wholeCardPointer'],authoredStatus='reviewed-authored-operational-playtest',
                 procedureFile='../spell_candidates/'+s['model'].name,procedurePointer=pointer,wholeCardPointer=pointer,
                 wholeCardIdField=s['idkey'],procedureTextPointer=pointer+'/'+s['textkey'],sharedRulesPointer='/'+s['rules'],
                 manuscript='../../../docs/spells/candidates/'+s['chapter'].name,reviewId=receipt['id'],runtimeSelectionEnabled=False,
                 completeEnvelopeBinding=receipt['canonicalModel'],authoredAcceptanceReceipt=receipt['authority'],
                 authoredApplicationReceipt=receipt_binding,historicalCandidateLabelsPreserved=True,
                 casebookBinding=receipt['casebook'],retainedHoldsBinding=receipt['holds'])
        if name.startswith('control'):
            e['additionalSharedRulesPointers']=['/completeOriginalSharedProposals']
    after['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/'+s['model'].name,'binding':receipt['canonicalModel'],
        'reviewId':receipt['id'],'acceptedIds':ids,'authority':receipt['authority'],'receipt':receipt_binding})

assert seen==accepted_ids
after['authoredCounts']={'reviewed':597,'pending':251}
after['representationCounts']['completeReviewedStandaloneProcedures']=321
assert len(after['entries'])==848
assert [e for e in before['entries'] if e['id'] not in seen]==[e for e in after['entries'] if e['id'] not in seen]

# Inventory all 251 pending identities, retaining each actual question and finding, not guessing defects.
backlog=[]
for group in queue['groups']:
    if set(group['identities']).issubset(seen):
        continue
    p=G/group['candidate']['path']; verify(p,group['candidate']); candidate=read(p)
    records=candidate.get('records',candidate.get('spells',[]))
    by_id={r.get('spellId',r.get('id')):(n,r) for n,r in enumerate(records)}
    questions=candidate.get('questions',candidate.get('conferenceQuestions',[]))
    spell_records=[]
    for i in group['identities']:
        assert i in by_id, (group['group'],i)
        n,row=by_id[i]
        matched=[]
        for q in questions:
            if not isinstance(q,dict):
                matched.append(q);continue
            targets=q.get('spellIds',q.get('spells',[]))
            if not targets or i in targets:
                matched.append(q)
        spell_records.append({'id':i,'riskTier':row.get('riskTier'),'riskReason':row.get('riskReason'),
            'sourceRecordPointer':f'/{"records" if "records" in candidate else "spells"}/{n}',
            'openQuestions':matched,'status':'Awaiting authored acceptance; not a finding that this entire spell is broken.'})
    backlog.append({'group':group['group'],'currentPhase':group['currentPhase'],'candidate':group['candidate'],
        'identityCount':len(spell_records),'spells':spell_records,'allGroupQuestions':questions,
        'sourceFindings':candidate.get('sourceFindings',candidate.get('findings',[])),'riskCounts':candidate.get('riskCounts')})
assert len(backlog)==47 and sum(x['identityCount'] for x in backlog)==251
assert len({s['id'] for g in backlog for s in g['spells']})==251
report={'id':'PENDING251-REVIEW-INVENTORY-122','recordedAtUtc':now,'interpretation':'251 identities have no final authored acceptance. The source questions distinguish incomplete design, conflicting source wording, external source premises and validation work. A proposed solution is not an accepted choice.',
        'count':251,'groups':backlog,'questionCount':sum(len(g['allGroupQuestions']) for g in backlog),
        'scope':'Inventory of every current prepared conference; does not count preparation or recommendations as acceptance.'}
stage(OUT/'PENDING251_REVIEW_INVENTORY.json',encoded(report))

new_queue=copy.deepcopy(queue)
new_queue.update(id='SPELL-REVIEW-QUEUE-122',recordedAtUtc=now,previousQueue=binding(O/'CURRENT_SPELL_QUEUE_121.json'))
new_queue['currentCounts'].update(appliedReviewed=597,indexPending=251,acceptedUnapplied=0,needsAcceptance=251)
new_queue['appliedAcceptedIdentities']=new_queue.pop('acceptedIdentities')
new_queue['acceptedIdentities']=[]
for group in new_queue['groups']:
    if set(group['identities']).issubset(seen):
        group['previousPhase']=group['currentPhase'];group['currentPhase']='applied-authored-review-122-with-retained-holds'
new_queue['latestApplicationReceipts']=cohort_receipts
stage(O/'CURRENT_SPELL_QUEUE_122.json',encoded(new_queue))
stage(OUT/'authored_review_index.before.json',before_bytes)
stage(OUT/'authored_review_index.after.json',encoded(after))
stage(R/'docs/mechanics/SPELL_ACCEPTED72_APPLICATION_122_STATUS.json',encoded({'id':'SPELL-ACCEPTED72-APPLICATION-122',
    'authoredCounts':after['authoredCounts'],'representationCounts':after['representationCounts'], 'applicationReceipts':cohort_receipts,
    'appliedIds':sorted(seen),'acceptedUnapplied':0,'pendingReviewInventory':binding(OUT/'PENDING251_REVIEW_INVENTORY.json',writes[OUT/'PENDING251_REVIEW_INVENTORY.json']),
    'runtimeSelectionEnabled':False,'acceptedGlobalInterfaceCountUnchanged':173,'historicalSourcesPreserved':True}))
summary={'id':'SPELL-ACCEPTED72-APPLICATION-122','recordedAtUtc':now,'status':'APPLIED_AUTHORED_REVIEW_WITH_RETAINED_HOLDS',
    'beforeIndex':binding(INDEX,before_bytes),'afterIndex':binding(INDEX,encoded(after)),'catalogPreserved':binding(CATALOG),
    'beforeCounts':before['authoredCounts'],'afterCounts':after['authoredCounts'],'acceptedUnapplied':0,'identitiesApplied':sorted(seen),
    'cohortReceipts':cohort_receipts,'inputSources':list(source_bindings.values()),'verifiedPackageArtifactBindings':verified_artifacts,
    'unchangedIndexEntries':776,'runtimeExecuted':False,'downloadedCodeExecuted':False,'featsChanged':False,
    'outputs':[binding(p,b) for p,b in writes.items()]}
stage(OUT/'APPLICATION_RECEIPT.json',encoded(summary))
print(json.dumps({'mode':'apply' if '--apply' in sys.argv else 'preflight','newFiles':len(writes),'cohorts':len(specs),
    'identities':len(seen),'unchangedEntries':776,'packageBindingsChecked':verified_artifacts,'pendingGroups':47,
    'pendingIdentities':251,'pendingQuestions':report['questionCount'],'counts':after['authoredCounts']}))
if '--apply' not in sys.argv:
    sys.exit(0)
# Inputs and all destinations have passed before the first write. Preserve old index then atomically select the new one.
assert sha(INDEX.read_bytes())==EXPECTED_INDEX
for p,b in writes.items():
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(b)
assert sha(INDEX.read_bytes())==EXPECTED_INDEX
temp=INDEX.with_name('authored_review_index.application122.tmp')
assert not temp.exists()
temp.write_bytes(encoded(after));temp.replace(INDEX)
assert INDEX.read_bytes()==encoded(after)
for p,b in writes.items():
    assert p.read_bytes()==b,str(p)
assert sha(CATALOG.read_bytes())==before['sourceCatalogSha256']
print('APPLIED and read-back verified: 72 exact authored selections, 597 reviewed / 251 pending.')
