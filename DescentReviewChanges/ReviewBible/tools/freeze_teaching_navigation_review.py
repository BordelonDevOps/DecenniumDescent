"""Freeze the nine-artifact teaching review with current LRX fulfillment evidence."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,zipfile
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(raw):return sha256(raw).hexdigest()
def record(p):return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def save(p,x):p.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    target=A/'DD_Teaching_Navigation_9_Exact_Review_v1.zip'
    assert not target.exists(),'Never replace a submitted review archive'
    staging_path=A/'TEACHING_NAVIGATION_REVIEW_STAGING.json';stage=read(staging_path)
    assert len(stage['sourceFiles'])==147 and stage['draftCount']==9 and stage['reviewQuestions']==29
    navigation=read(A/'LOW_RANK_136_FULFILLMENT_NAVIGATION.json')['navigationHashes']
    prior_navigation=read(A/'navigation-before-low136-fulfillment/FILE_MANIFEST.json')
    refreshed=[]
    for rel,e in stage['sourceFiles'].items():
        current=record(G/rel)
        if current!=e:
            assert rel in navigation and current['sha256']==navigation[rel] and e['sha256']==prior_navigation[rel],rel
            refreshed.append({'path':rel,'before':e,'after':current,'reason':'Documented LRX fulfillment navigation; original bytes backed up.'})
    fulfilled=read(A/'LOW_RANK_136_EXACT_FULFILLMENT.json')
    assert fulfilled['promotedAuthoredProcedures']==136 and fulfilled['protectedOriginalsUnchanged']==342
    backup=A/'teaching-before-exact-dispatch';backup.mkdir()
    for name in ['TEACHING_NAVIGATION_REVIEW_STAGING.json','TEACHING_NAVIGATION_REVIEW_CHECKLIST.json','TEACHING_NAVIGATION_REVIEW_README.md']:(backup/name).write_bytes((A/name).read_bytes())
    save(backup/'FILE_MANIFEST.json',{p.name:record(p) for p in backup.iterdir() if p.is_file()})
    questions=read(A/'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json')
    q=next(q for q in questions['questions'] if q['id']=='TE-22')
    assert 'Pending136 spell candidates remain unavailable until their exact gate;' in q['question']
    q['question']=q['question'].replace('Pending136 spell candidates remain unavailable until their exact gate; other pending spells/feats stay pending.','The136 low-rank authored procedures now have fulfilled LRX approval; authored ordinary totals are412 reviewed/436 pending, with full standalone representation and runtime selection still disabled. Other pending spells/feats stay pending.')
    questions['status']='complete-exact-review-checklist-prepared-for-dispatch'
    save(A/'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json',questions)
    stage['status']='complete-nine-artifact-exact-review-prepared-for-dispatch'
    stage['priorStagingSnapshot']='docs/audit/2026-10-08/full-game/teaching-before-exact-dispatch/TEACHING_NAVIGATION_REVIEW_STAGING.json'
    stage['priorFrozenSpellPayloadCheck']=stage.pop('activeExactReviewDiskPayloadsUnchanged')
    stage['lowRankExactReview']='LRX-01–05 fulfilled; precise working candidate amendments and review labels now differ from the frozen submission, with full pre-label/reversal proof. All342 original sources unchanged.'
    stage['currentAuthoredOrdinaryCounts']={'reviewed':412,'pending':436}
    stage['refreshedNavigationSources']=refreshed
    stage['preparedForDispatchAtUtc']=datetime.now(timezone.utc).isoformat()
    stage['sourceFiles']={rel:record(G/rel) for rel in stage['sourceFiles']}
    save(staging_path,stage)
    readme='''# Nine teaching artifacts — exact authored presentation review v1

Read the complete nine artifacts named in TEACHING_NAVIGATION_REVIEW_CHECKLIST.json and answer all29 questions. Eight manuscripts and one five-page fillable PDF are supplied, together with all147 original supporting files and the current LRX fulfillment evidence. This is an internal review archive; source comparisons are not a public release.

The drafts are the eight-form language worksheet;48-term glossary with52 section links; first-craft, injury/aid and companion-command worked examples; full character-foundation navigation copy; all17-class resource reference; and blank character PDF with complete instructions. The original character chapter and exact five-note navigation diff are included. The PDF has364 fields; field definitions, save/reopen QA and all five blank page renders are included. Read the whole artifacts and sources, not just their reports or counts.

TE-23 is the single explicitly requested mechanical reconciliation: TC-RECYCLING-01. The older reviewed Tinker card and lifecycle exclude deliberate sacrifice/copies but explicitly do not require enemy cause; later TD-13/crafting guide added enemy destruction. The full evidence, source cards, guides, existing helper/regression, unapplied preferred paragraph and five boundaries are included. Explicitly settle that predicate and exact current-guide/erratum wording, preserving history and unrelated recipe scopes. A newer date is not evidence that the narrowing was intended. Paladin Wave's long-rest cadence is a separate already-authored amendment, not a new unresolved conflict.

LRX-01–05 are now fulfilled in the actual repository under final reply5ece3872-cb87-4e1c-b14b-915859f41fef. The complete LOW_RANK_136_EXACT_FULFILLMENT.json records source preservation, all16 exact field operations applied symmetrically, eight regenerated artifacts, local1,093 strict pre-label checks and42 focused examples. The clean archive baseline reproduces5,439 static checks and49 original checks including18,840 access/2,808 quotation trials. A separate2,533-check final audit verifies label reversal, full index pointers and preservation. These overlap and are not full spell-runtime or human trials.

All136 complete authored procedures have the explicitly authorized reviewed labels. The standalone envelope preserves full prose, modes, access and shared rules. authored_review_index.json joins those136 with276 older authored procedures:412 reviewed/436 pending. The legacy source catalog remains byte-identical at276 populated rows; a runtime adapter has not been invented and selectionEnabled stays false in the standalone envelope. Blink is an unchanged null receipt. The full final LRX package, pre-label snapshot/proof, final eight artifacts and reproduction scripts are included. The original immutable60,244,248-byte exact ZIP is nested unchanged if a full original reproduction is needed; extract it into a separate frozen tree. Scripts for the original baseline must not be run against the later amended tree or mistaken for whole-game tests.

Carry fulfilled LAX, NWX and687 internal/433 public recipe scopes forward. The earlier staging reports retain historical checks such as391 unchanged spell-packet payloads; those describe their dates, not a claim that LRX subsequently changed no candidate fields. Their source data are preserved. Current fulfillment is the later authority.

Give scoped authored-presentation acceptance or finite corrections with exact affected file/field/paragraph, complete replacement wording, and acceptance cases. State what the nine-artifact gate permits after those corrections. Distinguish existing rules from any explicitly NEW decision; do not approve unrelated pending spells, feats or remaining whole-game areas by implication. TE-23 is a bounded consequential rules question, not merely proofreading. Human teaching/accessibility/two-lookup trials, numerical balance, deployed companion behavior and actual whole-game flow remain separate and unclaimed.

The user authorized the GitHub push after actual final joint Codex/GPT whole-game-flow agreement. Verify the remote commit before careful cosmology review. Do not add a new owner-confirmation gate. No deletion, push or cosmology interpretation is performed by this packet.
'''
    save(A/'TEACHING_NAVIGATION_REVIEW_README.md',readme)
    payload={}
    def add(p):
        rel=p.relative_to(G).as_posix();raw=p.read_bytes()
        if rel in payload:assert payload[rel]==raw,rel
        payload[rel]=raw
    for rel in stage['sourceFiles']:add(G/rel)
    for rel in stage['draftFiles']:add(G/rel)
    for name in ['TEACHING_NAVIGATION_REVIEW_STAGING.json','TEACHING_NAVIGATION_REVIEW_CHECKLIST.json','TEACHING_NAVIGATION_REVIEW_README.md','LOW_RANK_136_EXACT_FULFILLMENT.json','LOW_RANK_136_EXACT_PRELABEL_FULFILLMENT.json','LOW_RANK_136_EXACT_LABEL_ONLY_PROOF.json','LOW_RANK_136_LOCAL_FINAL_FULFILLMENT_VALIDATION.json','LOW_RANK_136_LOCAL_STRICT_PRELABEL_PROOF.json','LOW_RANK_136_LOCAL_NAMED_AMENDMENTS_APPLIED.json','LOW_RANK_136_LOCAL_FOCUSED_REFERENCES.json','LOW_RANK_136_LOCAL_EXACT_BASELINE_AUDIT.json','LOW_RANK_136_LOCAL_LRX01_BASELINE_VALIDATION.json','LOW_RANK_136_LRX01_LOCAL_PREPARATION.json','LOW_RANK_136_FULFILLMENT_NAVIGATION.json','LOW_RANK_136_EXACT_FINAL_NOTEBOOK_RESPONSE.json','DD_Low_Rank_136_Exact_Review_v1.zip']:
        add(A/name)
    for rel in fulfilled['finalArtifacts']:add(G/rel)
    for path in [A/'low-rank136-exact-prelabel',A/'low-rank136-exact-reviewer-files',backup]:
        for p in sorted(path.rglob('*')):
            if p.is_file():add(p)
    for p in [R/'data/public/spell_playtests/authored_review_index.json',R/'docs/mechanics/LOW_RANK_SPELL_REVIEW_STATUS.json',G/'START_HERE.md',R/'data/playtest/game_development_coverage.json',R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md']:
        add(p)
    for name in ['fulfill_low_rank_exact_review.py','validate_low_rank_exact_fulfillment.py','manifest_loader.py','build_low_rank_136_candidates.py','validate_low_rank_136_candidates.py','prepare_low_rank_136_exact_review.py','register_low_rank_fulfillment.py','freeze_teaching_navigation_review.py']:
        add(R/'tools'/name)
    payload['README_TEACHING_EXACT_V1.md']=readme.encode('utf-8')
    manifest={k:{'bytes':len(v),'sha256':sha(v)} for k,v in sorted(payload.items())}
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for k,v in sorted(payload.items()):z.writestr(k,v)
        z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(target) as z:
        assert len(z.namelist())==len(manifest)+1
        for k,e in manifest.items():assert sha(z.read(k))==e['sha256'] and len(z.read(k))==e['bytes']
    receipt={'status':'prepared-not-submitted','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':str(target),**record(target),'payloadFiles':len(manifest),'manifest':manifest,'draftArtifacts':9,'manuscripts':8,'pdfPages':5,'pdfFields':364,'questions':29,'supportingFilesFromOriginalStage':147,'refreshedNavigationSources':refreshed,'otherOriginalStageSourcesUnchanged':True,'fulfilledLowRankAuthored':136,'authoredOrdinaryCounts':{'reviewed':412,'pending':436},'focusedMechanicConflict':'TC-RECYCLING-01','presentationApproved':False,'runtimeVerified':False,'humanUsabilityVerified':False,'pushPerformed':False,'cosmologyReviewed':False}
    save(A/'TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json',receipt)
    prompt=f'''LRX-EXACT-2026-10-11 is fulfilled in the actual repository under your final reply5ece3872-cb87-4e1c-b14b-915859f41fef. All16 exact field replacements were applied symmetrically, all eight full artifacts regenerated, and LRX-01 uses your authentic manifest loader. Local checks:5,439 frozen-baseline checks;49 original checks with18,840 access/2,808 quote trials;1,093 strict pre-label checks;42 focused fixtures;2,533 final label-reversal/source/index checks. All342 original sources remain byte-identical. The version-bound receipt, all identity/case dispositions, pre-label hashes and reversible label-only proof are attached. All136 complete authored procedures now have the authorized reviewed labels. The full-mode standalone envelope stays intact with runtime selection disabled. authored_review_index.json connects276 older procedures and136 reviewed standalone procedures:412 reviewed/436 pending. The legacy catalog remains unchanged; no lossy schema conversion, runtime or human claim. Blink remains null/unavailable. This is the concise fulfillment you authorized, not a request to reopen the unchanged136-card conference.

Next, please exact-review ALL nine teaching artifacts (eight complete manuscripts and the five-page fillable character PDF) and ALL TE-01–29 questions in DD_Teaching_Navigation_9_Exact_Review_v1.zip: {receipt['bytes']:,}bytes, SHA256 {receipt['sha256']}, {len(manifest)} complete payloads plus manifest. Start with README_TEACHING_EXACT_V1.md and the actual TEACHING_NAVIGATION_REVIEW_CHECKLIST.json. The full147 original supporting files, full17 class datasets/1223 cards, governing sources, five blank PDF page renders, field inventory/QA, current fulfilled gates and actual candidate texts are included. Please read the files, including every PDF page; do not infer acceptance from report counts.

Scope: eight-form language worksheet;48-term glossary; full craft/injury/companion worked examples; exact five-note character-foundation navigation copy; all17-class resource reference; blank character sheet and full instructions. TE-23 separately asks you to settle TC-RECYCLING-01: reviewed class/lifecycle says enemy cause NOT required for Efficient Recycling, while later TD-13/crafting guide says enemy destruction. Full conflicting texts, helpers, five boundaries and a complete UNAPPLIED proposed replacement are supplied. Please explicitly settle the one predicate and exact guide/erratum wording, preserving history and all unrelated recipe/device gates. Do not silently prefer later wording. Paladin Wave's long-rest amendment is already governed, not another unresolved conflict.

Return scoped authored-presentation acceptance or finite precise corrections with affected files/paragraphs/fields, complete replacement wording, finite acceptance cases and a clear final disposition for every TE question. Distinguish the one consequential rule reconciliation from presentation edits. Carry fulfilled LAX/NWX/LRX and687/433 recipes; other catalogs remain open. No full runtime, actual campaign premise, human teaching/two-lookup, balance or whole-game-flow approval is inferred. Actual final joint game flow precedes the already authorized GitHub push; verified remote precedes careful cosmology. No additional owner confirmation or source deletion. Please supply complete verdict/evidence files when helpful.'''
    save(A/'CODEX_TEACHING_NAVIGATION_EXACT_V1_PROMPT.txt',prompt)
    print(json.dumps({k:receipt[k] for k in ['bytes','sha256','payloadFiles','draftArtifacts','questions']},indent=2))
if __name__=='__main__':main()
