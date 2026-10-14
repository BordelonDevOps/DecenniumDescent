"""Record the completed exact Jewelcrafting scope without closing broader areas."""
from pathlib import Path
import json,shutil
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,s):p.write_text(s,encoding='utf-8')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def main():
    paths=[GAME/'START_HERE.md',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',ROOT/'data/playtest/game_development_coverage.json',ROOT/'tools/build_crafting_review_queue.py',ROOT/'docs/director-only/CRAFTING_REVIEW_QUEUE.md',AUDIT/'CRAFTING_REVIEW_QUEUE_VALIDATION.json',ROOT/'tools/build_feat_review_queue.py']
    backup=AUDIT/'navigation-before-jewelcrafting-promotion';backup.mkdir()
    for p in paths:
        dest=backup/p.relative_to(GAME);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    p=ROOT/'tools/build_crafting_review_queue.py';s=p.read_text(encoding='utf-8')
    for old,new in [('len(checked_manifests)==7','len(checked_manifests)==8'),("sum(x['reviewed'] for x in rows)==305","sum(x['reviewed'] for x in rows)==348"),("sum(x['draft'] for x in rows)==43","sum(x['draft'] for x in rows)==0"),('**305 of 687 recipes reviewed; 382 remain.** All382','**348 of 687 recipes reviewed; 339 remain.** All339'),('Public operational reviews are197 of433','Public operational reviews are223 of433'),("'reviewed':305,'remaining':382,'draftAwaitingExactReview':43","'reviewed':348,'remaining':339,'draftAwaitingExactReview':0"),("'verifiedReviewedManifests':7","'verifiedReviewedManifests':8")]:
        assert old in s,old;s=s.replace(old,new)
    old='Jewelcrafting source decisions are complete and all43 cards are authored with98 checks,69 predicate cases,486 structural states and86 body-value combinations. Exact review is in progress; check its actual packet state before dispatching anything. Fishing is the next prepared source conference after the Jewelcrafting verdict.'
    new='Jewelcrafting exact review is complete: JC-ER01..03 fulfilled,131 checks,69 predicate cases,486 structural states and86 body-value combinations;54 protected inputs unchanged. All43 cards are operationally reviewed,26 public. Fishing is the next prepared source conference; use current reviewed dependencies and check the actual dispatch state before sending.'
    assert old in s;s=s.replace(old,new);write(p,s)
    p=ROOT/'tools/build_feat_review_queue.py';s=p.read_text(encoding='utf-8').replace('Finish the active Jewelcrafting exact-card review before dispatching another conference.','Jewelcrafting exact review is complete; Fishing is the next planned source conference. Check live dispatch state before sending any feat packet.');write(p,s)
    for p,prefix in [(GAME/'START_HERE.md','docs/audit/2026-10-08/full-game/'),(AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md','')]:
        s=p.read_text(encoding='utf-8-sig');paragraphs=s.split('\n\n')
        for i,para in enumerate(paragraphs):
            if para.startswith('The [Jewelcrafting source conference]') or para.startswith('Jewelcrafting source conference completed'):
                paragraphs[i]='The [Jewelcrafting exact verdict]('+prefix+'GPT_JEWELCRAFTING_EXACT_REVIEW.md) conditionally approved all43 cards. [JC-ER01..03 are fulfilled]('+prefix+'JEWELCRAFTING_EXACT_REPAIRS_APPLIED.json): chronological charge/dawn ordering, shared roll-event identity and source-bound Gem repair fixtures. All131 checks,69 predicate cases,486 structural states and86 values pass;54 protected inputs remain unchanged. All43 cards are promoted under that exact authorization,26 public,one restricted and16 Director-only. Complete public cards,guide andJSON reconstruct exactly. The submitted revision,full verdict and reviewer archive are preserved. Current totals348/687 reviewed,339 remaining;public223/433. Fishing44 is next; no Fishing approval, deletion, push or cosmology review.'
            elif para.startswith('The latest completed recipe review covers'):
                paragraphs[i]='The latest completed recipe review covers [all43 Jewelcrafting formulas](DescentReviewChanges/ReviewBible/docs/mechanics/JEWELCRAFTING_RECIPE_PLAYTEST.md). All three finite repairs are satisfied;131 checks pass. The [recipe index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md) records **348 of687 recipe effects reviewed;339 remain** (223 of433 public formulas reviewed). The [crafting review queue](DescentReviewChanges/ReviewBible/docs/director-only/CRAFTING_REVIEW_QUEUE.md) links all16 trades. Original sources and prior submitted revisions remain preserved. No deletion, GitHub push or cosmology review occurred.'
            elif 'Current request: exact Jewelcrafting candidate;' in para:
                paragraphs[i]=para[:para.index('Current request:')]+ 'Jewelcrafting exact review has now also completed: turn3074a6c4-b718-4241-ae05-f6b3ed1238b0/reply872837f3-e844-4e3f-9a79-068060b62213. JC-ER01..03 are fulfilled;43 cards promoted after131 checks,54 protected inputs unchanged. Fishing is the next source conference; check FISHING_PART2_SUBMISSION.json once prepared. No resubmission of unchanged Jewelcrafting cards is required.'
        s='\n\n'.join(paragraphs)
        if p.name=='START_HERE.md':
            s=s.replace('382 other recipe effects','339 other recipe effects').replace('All382 recipes remaining in the operational pass','All339 recipes remaining in the operational pass')
            marker='| Ordinary spells |';s=s.replace(marker,'| [Jewelcrafting recipes](DescentReviewChanges/ReviewBible/docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md) | All43 formulas reviewed;26 public,17 separately gated;131 checks pass | Material availability, wider interactions, runtime and balance |\n'+marker,1)
        write(p,s)
    p=ROOT/'data/playtest/game_development_coverage.json';d=read(p)
    r=next(x for x in d['aspects'] if x['id']=='DD-29')
    outdated=[x for x in r['openIssues'] if 'Jewelcrafting' in x or '305/687' in x or '382remaining' in x]
    r.setdefault('resolvedIssueHistory',[]).extend(outdated);r['openIssues']=[x for x in r['openIssues'] if x not in outdated]
    r['completedScopes'].append('Jewelcrafting43 exact operational cards promoted under conditional verdict3074a6c4/reply872837f3 after JC-ER01..03 passed.131 checks,69 predicate cases,486 structural states,86 values;54 protected inputs unchanged. Public26 cards and complete guide/JSON project exactly. Source/runtime/human gates remain separate.')
    r['openIssues'].append('Current recipe pass348/687 reviewed,339 remaining,public223/433. Complete Fishing44,Mining43,Skinning43,Salvaging42,Enchanting43,RuneCarving41,Scribing40,Tinkering43 and broader interfaces; all pending sources prepared but not approved.')
    r['jewelcraftingCurrentCheckpoint']='Exact review completed; JC-ER01..03 fulfilled and43 cards promoted. See JEWELCRAFTING_REVIEW_STATUS.json and repair receipt; submitted evidence remains historical.'
    for key,ref in [('reviewEvidence','docs/audit/2026-10-08/full-game/GPT_JEWELCRAFTING_EXACT_REVIEW.md'),('validationEvidence','docs/audit/2026-10-08/full-game/JEWELCRAFTING_EXACT_REPAIRS_APPLIED.json'),('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/JEWELCRAFTING_REVIEW_STATUS.json')]:
        if ref not in r[key]:r[key].append(ref)
    dump(p,d)
    p=AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';d=read(p);d['observedAtUtc']=datetime.now(timezone.utc).isoformat();d['threadStatus']='idle'
    d['currentRequest'].update(completedExactVerdictPresent=True,replyId='872837f3-e844-4e3f-9a79-068060b62213',observedItemTypes=['userMessage','agentMessage'],status='completed; finite conditions fulfilled;43 cards promoted')
    d['authoredProgress'].update(checks=131,currentReviewedRecipes=348,newApprovals=43,publicReviewed=223,remainingRecipes=339)
    d['currentGoalTurnClassification']='progress: exact Jewelcrafting verdict captured,three finite corrections implemented,validated and43 cards promoted; all327 pending feat sources prepared'
    d['nextAction']='Prepare current-rule Fishing source conference, send Part A once, await actual receipt, then send Part B. No push or cosmology review.';dump(p,d)
    print('Updated navigation; broader crafting coverage remains open.')
if __name__=='__main__':main()
