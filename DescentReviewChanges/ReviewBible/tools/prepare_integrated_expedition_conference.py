"""Plan the next source conference without freezing or sending stale current files."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def hashfile(p):return {'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()}
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=A/'EXPEDITION_INTEGRATED_CONFERENCE_PLAN.json';assert not out.exists()
v2=load(A/'EXPEDITION_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json')
flow=load(A/'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json')
social=load(A/'SOCIAL_FACTION_SOURCE_PREPARATION.json')
transport=load(A/'TRANSPORT_SOURCE_PREPARATION.json')
reputation=load(A/'REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json')
paths=set(v2['currentFileHashes'])
paths.update(flow['protectedFiles'])
for src in (social,transport,reputation):paths.update(src['fullSourceFiles'])
for p in (R/'docs/mechanics/classes').glob('*.md'):paths.add(p.relative_to(G).as_posix())
paths.add('DescentReviewChanges/ReviewBible/docs/mechanics/BARD_PLAYTEST_v0_1.md')
notes=['EXPEDITION_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json','EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json','EXPEDITION_HAVEN_FLOW_SOURCE_AUDIT.md','SOCIAL_FACTION_SOURCE_PREPARATION.json','SOCIAL_FACTION_SOURCE_AUDIT.md','SOCIAL_FACTION_SOURCE_LINK_MAP.json','SOCIAL_FACTION_OPERATING_PROPOSAL.md','SOCIAL_FACTION_PROPOSAL_PREPARATION.json','REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json','REPUTATION_PRESERVATION_SOURCE_ADDENDUM.md','REPUTATION_PRESERVATION_RUNTIME_PROBES.json','TRANSPORT_SOURCE_PREPARATION.json','TRANSPORT_SOURCE_AUDIT.md','DIRECTOR_TABLECRAFT_SOURCE_PREPARATION.json','DIRECTOR_TABLECRAFT_SOURCE_AUDIT.md','LANGUAGE_EXACT_FULFILLMENT.json','ONBOARDING_CHARTER_EXACT_FULFILLMENT.json','LOW_RANK_136_EXACT_FULFILLMENT.json','TEACHING_TEX_EXACT_FULFILLMENT.json','TEACHING_TEX_PRELABEL_FULFILLMENT.json','TEACHING_TEX_LABEL_ONLY_AND_SCOPE_PROOF.json','TEACHING_TEX_ADMIN_APPEND_PROOF.json','TC_RECYCLING_01_CONTROLLING_ERRATUM.md']
paths.update('docs/audit/2026-10-08/full-game/'+p for p in notes)
for filename,field in [('LANGUAGE_EXACT_FULFILLMENT.json','finalHashes'),('ONBOARDING_CHARTER_EXACT_FULFILLMENT.json','finalManuscriptHashes'),('LOW_RANK_136_EXACT_FULFILLMENT.json','finalArtifacts'),('TEACHING_TEX_EXACT_FULFILLMENT.json','finalArtifacts')]:
    paths.update(load(A/filename)[field])
paths.update(['DescentReviewChanges/ReviewBible/docs/playtest/TEACHING_REVIEW_STATUS.json','DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json','DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_REVIEW_STATUS.json','DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','docs/canon/CANON_MANIFEST.json','START_HERE.md'])
assert all((G/p).is_file() for p in paths),[p for p in paths if not (G/p).is_file()]
questions=[]
for family,source,key in [('FL',flow,'decisionCases'),('SO',social,'questions'),('TR',transport,'questions'),('RP',reputation,'questions')]:
    for q in source[key]:questions.append({'family':family,'originalQuestion':q})
assert len(questions)==58 and len({q['originalQuestion']['id'] for q in questions})==58
current={p:hashfile(G/p) for p in sorted(paths)}
changed=[]
for p,old in v2['currentFileHashes'].items():
    oldhash=old if isinstance(old,str) else old['sha256']
    if oldhash!=current[p]['sha256']:changed.append({'path':p,'originalV2Sha256':oldhash,'currentSha256':current[p]['sha256']})
plan={'status':'Complete source membership plan; UNFROZEN and UNSENT pending the focused TEX current-text addendum','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'All26 original FL cases,12 SO questions,14 TR refinements and6 RP-A subquestions; source-authoring conference only, not exact promotion','questionCounts':{'FL':26,'SO':12,'TR':14,'RP-A':6,'total':58},'questions':questions,'sourceFilesAtPreparation':current,'sourceFileCount':len(current),'totalSourceBytes':sum(x['bytes'] for x in current.values()),'originalV2Archive':{'path':str(A/v2['bundleFile']),**hashfile(A/v2['bundleFile'])},'changedSinceOriginalV2':changed,'unchangedSourceRecords':{'transportRecords':29,'factionDefinitions':44,'backgroundMaps':20,'classFamilies':17,'classCards':1223},'unadoptedProposal':{'path':'docs/audit/2026-10-08/full-game/SOCIAL_FACTION_OPERATING_PROPOSAL.md',**hashfile(A/'SOCIAL_FACTION_OPERATING_PROPOSAL.md'),'authoredCases':24,'mechanicallyApproved':False},'dispatchRequirements':['Await only the bounded TEX current-text addendum; no other generic teaching conference.','Apply and validate its exact added changes while preserving both reviewer packages and earlier fulfillment.','At actual dispatch, regenerate current file hashes and include full current files, the original V2 archive and preserved old/current pairs for every changed source. Do not copy this provisional plan into a frozen integrity claim.','Include the final TEX addendum, applied-current receipts, governing full guides, runtime source comparisons and completed LAX/NWX/LRX contexts.','Explain that historical preparation source hashes bind their original revisions; current descendants use the new dispatch manifest.','Request explicit decisions and complete authoring directions for all58 questions, preserving owner-locked twelve-character expedition structure and all stated source limits.','Do not adopt the proposed reputation scale, faction checkpoint or new transport profiles merely because a draft names them.','Keep underlying cosmology, sealed material and deeper meanings deferred until after verified GitHub push.','After decisions, author complete playable procedures, instances/profiles, worked examples and exact review candidate; do not report the source conference as exact completion.'],'newRuleApprovals':0,'sourceInformationDeleted':0,'realSavesReadOrChanged':False,'runtimeImplemented':False,'submitted':False,'cosmologyInterpreted':False}
save(out,plan)
print(json.dumps({'sourceFiles':len(current),'sourceBytes':plan['totalSourceBytes'],'originalQuestions':58,'changedFromV2':len(changed),'frozen':False,'submitted':False}))
print('Current changes from V2:',json.dumps(changed,indent=2))
