"""Index existing feat work without changing any rule or review status."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, os, re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
OUT = R / 'docs/feats/FEAT_OPERATING_PROPOSAL_INDEX.md'
DATA = R / 'data/director/feat_operating_proposal_index.json'
RECEIPT = A / 'FEAT_OPERATING_PROPOSAL_INDEX_CHECK.json'

def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def rel(p): return p.relative_to(G).as_posix()
def link(p): return os.path.relpath(p,OUT.parent).replace('\\','/')
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

backup=A/'feat-index-before-heritage-mutation-proposal'
for p in [OUT,DATA,RECEIPT]:
    assert (backup/p.name).is_file() and info(backup/p.name)==info(p), 'Preserve prior index before this one-use refresh'
registry=R/'src/data/feats.js'
feats=json.JSONDecoder().raw_decode(registry.read_text('utf-8').split('export const feats = ',1)[1])[0]
by={f['id']:f for f in feats}
manifest=R/'data/public/feat_playtests/manifest.json'
approved=set(read(manifest)['operationalIds'])
assert len(feats)==len(by)==335 and len(approved)==8
cohorts=[
 ('Crafting and tools','CRAFTING_FEAT_INTERFACE_PREPARATION.json','CRAFTING_FEAT_INTERFACE_AUDIT.md',24,'crafting'),
 ('Combat techniques','COMBAT_FEAT_SOURCE_PREPARATION.json','COMBAT_FEAT_SOURCE_AUDIT.md',47,'combat'),
 ('Skills','SKILL_FEAT_SOURCE_PREPARATION.json','SKILL_FEAT_SOURCE_AUDIT.md',25,'skill'),
 ('Core magic','MAGIC_CORE_FEAT_SOURCE_PREPARATION.json','MAGIC_CORE_FEAT_SOURCE_AUDIT.md',31,'magic_core'),
 ('Extended magic','MAGIC_EXTENDED_FEAT_SOURCE_PREPARATION.json','MAGIC_EXTENDED_FEAT_SOURCE_AUDIT.md',58,None),
 ('Heritage and mutation','HERITAGE_MUTATION_FEAT_SOURCE_PREPARATION.json','HERITAGE_MUTATION_FEAT_SOURCE_AUDIT.md',22,'heritage_mutation'),
 ('Defense and foundations','GENERAL_DEFENSE_FEAT_SOURCE_PREPARATION.json','GENERAL_DEFENSE_FEAT_SOURCE_AUDIT.md',31,'general_defense'),
 ('Exploration and society','GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json','GENERAL_EXPLORATION_FEAT_SOURCE_AUDIT.md',31,'general_exploration'),
 ('General combat','GENERAL_COMBAT_FEAT_SOURCE_PREPARATION.json','GENERAL_COMBAT_FEAT_SOURCE_AUDIT.md',58,'general_combat'),
]
checks=[]
def check(name,value):
    checks.append({'name':name,'pass':bool(value)})
    assert value,name
inputs={rel(p):info(p) for p in [registry,G/'src/data/feats.js',manifest]}
records=[]; grouped=[]; proposed=set(); complete=set(); deferred=set(); examples=0
for title,prep_name,audit_name,count,stem in cohorts:
    prep=A/prep_name; audit=A/audit_name
    # The crafting cohort uses its original interface-audit title.
    if not audit.exists() and stem is None and title=='Crafting and tools':
        audit=A/'CRAFTING_FEAT_INTERFACE_SOURCE_AUDIT.md'
    check(title+' audit exists',audit.is_file())
    source=read(prep)['selectedFeats']
    check(title+' expected cohort size',len(source)==count)
    inputs[rel(prep)]=info(prep); inputs[rel(audit)]=info(audit)
    drafts={}; draft_path=None; draft_doc=None
    if stem:
        draft_path=R/f'data/director/{stem}_feat_operating_proposal_internal.json'
        draft_doc=R/f'docs/feats/{stem.upper()}_FEAT_OPERATING_PROPOSAL.md'
        drafts={x['featId']:x for x in read(draft_path)['records']}
        check(title+' proposal covers exact cohort',set(drafts)=={x['featId'] for x in source})
        inputs[rel(draft_path)]=info(draft_path);inputs[rel(draft_doc)]=info(draft_doc)
    group=[]
    for s in source:
        fid=s['featId']; check(fid+' exact source object',s['sourceObject']==by[fid])
        check(fid+' not already operational',fid not in approved)
        d=drafts.get(fid)
        if d:
            check(fid+' draft preserves source',d['sourceObject']==by[fid])
            check(fid+' nonempty operating procedure',bool(d['procedure'].strip()))
            check(fid+' no duplicate proposal',fid not in proposed)
            proposed.add(fid);examples+=len(d['workedCases'])
            (deferred if d.get('procedureScope')=='grant-interface-only-deferred-spell' else complete).add(fid)
        x={'featId':fid,'name':by[fid]['name'],'cohort':title,'questionId':s.get('questionId'),
           'originalQuestion':s.get('fullClauseQuestion',s.get('issue')),
           'sourcePreparation':rel(prep),'sourceAudit':rel(audit),
           'status':('unadopted-grant-interface-only-deferred-spell' if fid in deferred else 'unadopted-procedure-proposed') if d else 'source-question-prepared',
           'proposalData':rel(draft_path) if d else None,'proposalManuscript':rel(draft_doc) if d else None,
           'authoredExamples':len(d['workedCases']) if d else 0,'runtimeImplemented':False}
        check(fid+' source issue present',bool(x['originalQuestion']))
        records.append(x);group.append(x)
    grouped.append((title,audit,draft_doc,group))
check('All nine cohorts partition the 327 pending identities',len(records)==327 and len({x['featId'] for x in records})==327 and {x['featId'] for x in records}==set(by)-approved)
check('269 distinct source feats with unadopted treatment',len(proposed)==269)
check('267 complete proposed procedures and two deferred grant interfaces',len(complete)==267 and deferred=={'astral_projection','planar_binding'} and complete.isdisjoint(deferred))
check('544 authored examples',examples==544)
check('Two original registries identical',registry.read_bytes()==(G/'src/data/feats.js').read_bytes())
for path,expected in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
    if path!='README_EXPEDITION_INTEGRATED_V3.md':check('Active expedition payload unchanged: '+path,info(G/path)==expected)
for path,expected in inputs.items():check('Index source unchanged: '+path,info(G/path)==expected)
data={'createdAtUtc':datetime.now(timezone.utc).isoformat(),'purpose':'Navigation only; existing procedures and source questions are linked, not promoted.',
      'sourceFeats':335,'reviewedFullFeats':8,'pendingFullFeats':327,'unadoptedProposedFeats':269,'completeProposedProcedures':267,
      'deferredPayloadGrantInterfaces':2,'pendingWithSourceQuestionsOnly':58,'pendingWithoutCompleteLocalProposal':60,
      'newSupplementalFeatProposalsOutsideOriginalRegistry':1,
      'authoredExamples':544,'completeFeatRuntimeTests':0,'reviewedIds':sorted(approved),'cohorts':9,'records':records,
      'sourceFiles':inputs,'sentToGpt':False,'sourceInformationDeleted':0,'cosmologyReviewed':False,'pushed':False}
write(DATA,data)
lines=['# Feat development: one index','',
       '**335 source feats: 8 reviewed, 327 still awaiting full review.** Of the pending entries, 267 now have complete proposed operating procedures, two have grant outlines with deferred spell payloads, and 58 have source-linked questions only. The 269 entries with proposed treatment include 544 authored examples. None of these proposals has been adopted or sent to GPT; this index changes no rules or review status.','',
       'Astral Projection and Planar Binding retain their deferred cosmology dependencies. One proposed NEW Spell Focus feat would fill the missing prerequisite of Greater Spell Focus; it is separate from the 335 original source feats and has not been added to the public registry.','',
       'The nine cohorts below contain every pending feat exactly once. The older six-feat training draft is already included in the 31 exploration entries and is not six additional feats. Reviewed maximum-HP components remain controlling, but do not confer whole-feat approval on Tenacity, Tough, Tough as Nails or Dark Fortitude.','',
       f'[Reviewed operational manifest]({link(manifest)}) · [Complete machine-readable index and original questions]({link(DATA)}) · [Preservation checks]({link(RECEIPT)})','',
       '## Find the current work','',
       '| Cohort | Pending feats | Complete proposed procedures | Source discussion |','|---|---:|---|---|']
for title,audit,doc,group in grouped:
    completed=sum(x['status']=='unadopted-procedure-proposed' for x in group)
    bounded=sum(x['status']=='unadopted-grant-interface-only-deferred-spell' for x in group)
    description=f'{completed} complete proposals'+(f'; {bounded} deferred grant outlines' if bounded else '')
    proposed_label=f'[{description}]({link(doc)})' if doc else 'Not yet authored as a complete local proposal'
    lines.append(f'| {title} | {len(group)} | {proposed_label} | [Original sources and questions]({link(audit)}) |')
lines+=['','## Already reviewed full feats','',', '.join(by[fid]['name'] for fid in sorted(approved))+'.','',
        'Use their operational manifest and linked governing guides. A proposed cross-feat rule cannot silently supersede their existing contracts.','',
        '## Pending identity register','',
        '“Proposed” means authored for discussion. “Source questions” means the original record and its unresolved clauses have been assembled. Both remain pending.','']
for title,audit,doc,group in grouped:
    lines+=['### '+title,'','| Original question | Feat | Current work |','|---|---|---|']
    for x in group:
        label=x['questionId'] or 'Original interface issue'
        status=(('Grant outline only; deferred spell payload' if x['status']=='unadopted-grant-interface-only-deferred-spell' else 'Proposed')+f"; {x['authoredExamples']} examples") if x['proposalManuscript'] else 'Source questions'
        lines.append(f"| {label} | {x['name']} (`{x['featId']}`) | {status} |")
    lines.append('')
lines+=['## Next joint review','',
        'After the active expedition conference returns, reconcile its actual travel, service, rest, social and transport decisions with the proposed feats. Send the full pending-feat sources, current governing manuscripts and complete proposed procedures to Calibration Review Part 2 together. Preserve any earlier/current disagreements explicitly; a source-authoring verdict is followed by exact review of the completed candidate.','',
        'Worked examples are authored adjudications. The cohort receipts distinguish structural preservation, arithmetic and existing reviewed component queries from full feat runtime tests. No full runtime implementation or human balance approval is claimed.','',
        'Final joint whole-game flow agreement precedes the authorized GitHub push. Verification of the remote commit precedes the careful cosmology review.','']
OUT.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',OUT.read_text('utf-8')):
    p=(OUT.parent/target).resolve();check('Index link: '+target,p.exists() or p==RECEIPT)
write(RECEIPT,{'createdAtUtc':data['createdAtUtc'],'purpose':data['purpose'],'checks':len(checks),'failures':0,'sourceFeats':335,'reviewedUnchanged':8,
               'pendingUnchanged':327,'uniqueSourceFeatsWithProposedTreatment':269,'completeProposedProcedures':267,'deferredPayloadGrantInterfaces':2,
               'pendingWithSourceQuestionsOnly':58,'newSupplementalFeatProposalsOutsideOriginalRegistry':1,
               'authoredExamples':544,'fullFeatRuntimeCases':0,'submittedCurrentPayloadsUnchanged':303,
               'artifacts':{rel(p):info(p) for p in [OUT,DATA]},'details':checks})
print(json.dumps({k:v for k,v in read(RECEIPT).items() if k!='details'},ensure_ascii=False))
