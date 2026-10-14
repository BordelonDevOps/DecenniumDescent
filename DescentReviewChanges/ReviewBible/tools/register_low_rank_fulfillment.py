"""Register the fulfilled authored spell scope without closing wider game gates."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from hashlib import sha256
import json,re,subprocess,sys
from manifest_loader import load_protected_manifest
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    output=A/'LOW_RANK_136_FULFILLMENT_NAVIGATION.json'
    assert not output.exists()
    validation=read(A/'LOW_RANK_136_LOCAL_FINAL_FULFILLMENT_VALIDATION.json')
    assert validation['checkCount']==2533 and not validation['failedChecks']
    protected=load_protected_manifest(G)
    data=R/'data/playtest/game_development_coverage.json'
    nav=[G/'START_HERE.md',A/'PREPARED_SPELL_SOURCE_INDEX.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',data,R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md']
    backup=A/'navigation-before-low136-fulfillment';backup.mkdir()
    for p in nav:(backup/p.name).write_bytes(p.read_bytes())
    save(backup/'FILE_MANIFEST.json',{p.relative_to(G).as_posix():sha(p) for p in nav})
    d=read(data);before=deepcopy(d);now=datetime.now(timezone.utc).isoformat()
    d['activeLowRankSpellReview'].update(phase='LRX-01–05-fulfilled;136-reviewed-authored-operational',exactReviewId='LRX-EXACT-2026-10-11',exactReplyId='5ece3872-cb87-4e1c-b14b-915859f41fef',exactApproval=True,ordinaryOperational=412,ordinaryPending=436,countScope='authored review across complete standalone and preserved legacy representations',legacyCatalogOperational=276,legacyCatalogPending=572,fulfillmentReceipt='docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_FULFILLMENT.json',runtimeVerified=False)
    changed=[]
    for row in d['aspects']:
        for i,old in enumerate(row['openIssues']):
            new=old
            if old.startswith('All136 full low-rank mechanical'):
                new='LRX-EXACT-2026-10-11 is fulfilled:136 complete authored procedures are reviewed, with20 shared rules,141 bindings and187 authored examples. All342 source files remain unchanged. Authored ordinary coverage is412 reviewed/436 pending; Blink stays receipt-only. Complete the remaining435 higher-rank identities and wider runtime/class/integration gates.'
            elif old.startswith('276 of848'):
                new='412 of848 ordinary identities now have reviewed complete authored procedures;436 remain pending (435 higher-rank identities and Blink). The legacy catalog remains byte-identical at276 populated procedures, with136 reviewed standalone procedures linked in authored_review_index.json. Ten ancestry-grant-only spells stay separate. Complete pending variants, aliases, rituals, individual effects and runtime interfaces.'
            elif old.startswith('All572 pending ordinary identities'):
                new='The original572-identity source preparation remains preserved across44 cohorts and627 book bindings. The first six cohorts have136 fulfilled authored procedures plus Blink receipt-only. The other38 cohorts/435 identities remain unsent with388 mechanical questions and47 post-push receipts. Refresh LAX/LRX and other current interfaces at actual dispatch. Current authored coverage is412 reviewed/436 pending.'
            elif old.startswith('276 ordinary spell drafts are operational;572'):
                new='412 ordinary identities have reviewed complete authored procedures, including the136 fulfilled LRX cards;436 remain pending. Full modes, costs, shared rules and access remain preserved. Remaining aliases, rituals, class-specific repertoire interfaces and complete runtime implementation remain open; authored acceptance alone does not implement an adapter.'
            elif 'Complete candidates with actual access, costs, clocks and boundaries are authored and submitted in the full 136-card exact-review packet; await the final exact verdict and fulfill its bounded corrections.' in old:
                new=old.replace('Complete candidates with actual access, costs, clocks and boundaries are authored and submitted in the full 136-card exact-review packet; await the final exact verdict and fulfill its bounded corrections.','The complete136-card authored gate is now fulfilled under LRX-01–05, with exact preservation, amended-case and label-only proofs. Remaining broader interfaces and runtime/human gates stay open.')
            if new!=old:
                row.setdefault('historicalIssueNotes',[]).append({'id':f"{row['id']}-LRX-FULFILLED-{i}",'originalText':old,'replacement':new,'reason':'Actual finite fulfillment and authorized authored-review promotion; no wider game closure.','recordedAtUtc':now,'evidence':['docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_FULFILLMENT.json']})
                row['openIssues'][i]=new;changed.append({'id':row['id'],'issue':i})
        if any(x['id']==row['id'] for x in changed):
            for key,path in [('reviewEvidence',A/'LOW_RANK_136_EXACT_FULFILLMENT.json'),('validationEvidence',A/'LOW_RANK_136_LOCAL_FINAL_FULFILLMENT_VALIDATION.json'),('draftEvidence',R/'data/public/spell_playtests/authored_review_index.json')]:
                rel=path.relative_to(G).as_posix()
                if rel not in row[key]:row[key].append(rel)
    for old,new in zip(before['aspects'],d['aspects']):
        for key in ['acceptanceGate','status','closure','humanEvidence','completedScopes','completionClass']:assert old.get(key)==new.get(key),(old['id'],key)
    save(data,d)
    start=(G/'START_HERE.md').read_text(encoding='utf-8')
    line='**Current joint review:** The [136 complete low-rank spell procedures](DescentReviewChanges/ReviewBible/docs/playtest/LOW_RANK_136_CANDIDATE.md) have completed exact authored review in Calibration Review Part 2. [LRX-01–05 are fulfilled](docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_FULFILLMENT.json); all342 source files are preserved. The [authored spell index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json) records **412 reviewed /436 pending**. Blink stays receipt-only; complete runtime and human balance remain open. The next bounded review covers nine teaching artifacts and the Efficient Recycling conflict. Fulfilled language, onboarding and crafting gates carry forward.'
    start=re.sub(r'^\*\*Current joint review:\*\*.*$',lambda _:line,start,flags=re.M)
    start=re.sub(r'^\| Ordinary spells \|.*$', '| Ordinary spells | **412 reviewed authored procedures;436 pending.** All848 identities and936 placements preserved;136 procedures use a complete standalone representation | Remaining435 higher-rank identities plus Blink;48 total post-push receipts; runtime and class integration; ten ancestry-only spells remain separate |',start,flags=re.M)
    start=re.sub(r'^\| Spells \|.*$', '| Spells | [All44 original source cohorts](docs/audit/2026-10-08/full-game/PREPARED_SPELL_SOURCE_INDEX.md) remain preserved. The first six now have136 reviewed authored procedures under [fulfilled LRX](docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_FULFILLMENT.json), plus Blink receipt-only. The other38 cohorts/435 identities remain unsent; refresh current interfaces before dispatch. Current authored totals:412 reviewed/436 pending. |',start,flags=re.M)
    save(G/'START_HERE.md',start)
    index=A/'PREPARED_SPELL_SOURCE_INDEX.md';old=index.read_text(encoding='utf-8')
    first='**Current status:412 reviewed authored ordinary-spell procedures and436 pending.** The first six of44 prepared source cohorts now have136 complete reviewed procedures under [fulfilled LRX-01–05](LOW_RANK_136_EXACT_FULFILLMENT.json), plus the unavailable Blink receipt. The remaining38 cohorts/435 identities are unsent (388 mechanical questions,47 post-push receipts). [The complete authored index](../../../../DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json) retains both full representations without altering original source bytes.\n\nThe original preparation paragraphs below are preserved as submission history; their prior pending counts and live-review statements are superseded by this checkpoint.\n\n'
    title,rest=old.split('\n',1);save(index,title+'\n\n'+first+rest.lstrip('\n'))
    handoff=A/'GPT_REVIEW_CONTINUATION_HANDOFF.md';old=handoff.read_text(encoding='utf-8')
    checkpoint='**CURRENT PHASE — low-rank exact review fulfilled:** GPT final `5ece3872-cb87-4e1c-b14b-915859f41fef`, LRX-EXACT-2026-10-11, authorized the136 authored promotions after finite corrections. [Actual fulfillment](LOW_RANK_136_EXACT_FULFILLMENT.json) records all16 field operations (32 symmetric writes), eight regenerated artifacts, LRX-01 portability,1,093 strict pre-label checks,42 focused fixtures, baseline5,439 plus49 checks (18,840 access/2,808 quote trials), and2,533 final label/source/index checks. [Reversible label proof](LOW_RANK_136_EXACT_LABEL_ONLY_PROOF.json) preserves full source/mode/access/prose; all342 originals remain unchanged. Authored totals are412 reviewed/436 pending via authored_review_index.json; the unchanged legacy representation still has276 populated procedures. Blink is null and unavailable. Runtime/human/full-game flow remain open.\n\n**Next: dispatch the complete teaching review** (nine artifacts,29 questions), including the existing TE-23 recycling conflict and current LRX fulfillment. Preserve all prior LAX/NWX/687-internal/433-public recipe scopes. Final actual joint whole-game flow still precedes the authorized push; verified remote precedes cosmology.\n\n**Historical checkpoints below are preserved; earlier live-review labels and pending counts are superseded by the checkpoint above.**\n\n'
    save(handoff,checkpoint+old)
    subprocess.run([sys.executable,str(R/'tools/build_game_coverage.py')],check=True)
    assert load_protected_manifest(G)==protected
    save(output,{'status':'fulfilled-authored-scope-registered','changedIssueNotes':changed,'all75AcceptanceStatusClosureHumanScopesUnchanged':True,'protectedOriginalsUnchanged':342,'navigationHashes':{p.relative_to(G).as_posix():sha(p) for p in nav},'historicalNavigationPreserved':str(backup)})
    print(json.dumps({'updatedIssueNotes':len(changed),'authoredReviewed':412,'authoredPending':436,'widerClosuresChanged':0}))
if __name__=='__main__':main()
