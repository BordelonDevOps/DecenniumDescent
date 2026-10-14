"""Record exact Herbalism approval after its four finite repairs and validation."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TURN='45dfe30e-6f5a-4efd-adaf-5fea18fbfd6f'
REPLY='63005e51-58e4-4bc4-a08e-e3841d6ba105'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def backup(p,name):
    q=AUDIT/name
    if not q.exists():q.write_bytes(p.read_bytes())

def main():
    status=ROOT/'docs/mechanics/HERBALISM_REVIEW_STATUS.json'
    if status.exists():raise SystemExit('Herbalism already recorded; inspect final state instead.')
    v=read(AUDIT/'HERBALISM_CANDIDATE_VALIDATION.json');assert v['status']=='PASS' and len(v['checks'])==43
    repairs=read(AUDIT/'HERBALISM_EXACT_REPAIRS_APPLIED.json');assert len(repairs['repairs'])==4
    reply=AUDIT/'GPT_HERBALISM_EXACT_REVIEW.txt';assert 'After those four finite repairs, I approve the complete' in reply.read_text(encoding='utf-8')
    source_reply=AUDIT/'GPT_HERBALISM_SOURCE_CONFERENCE.txt'
    paths=[ROOT/'docs/mechanics/HERBALISM_RECIPE_PLAYTEST.md',ROOT/'docs/director-only/HERBALISM_INTERNAL_PROCEDURES.md',ROOT/'docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/HERBALISM_INTERNAL_RECIPE_CARDS.md',ROOT/'data/playtest/herbalism_recipe_candidate.json',ROOT/'data/director/herbalism_recipe_candidate_internal.json']
    label='REVIEWED provisional authored operational PLAYTEST Herbalism recipe set'
    for p in paths[:4]:
        s=p.read_text(encoding='utf-8')
        s=s.replace('**Draft awaiting exact manuscript review.** The source conference approved the authoring direction, not these final cards.','**'+label+'.** The source conference and exact manuscript review are complete; all four required repairs are applied.')
        s=s.replace('**Draft awaiting exact manuscript review. Director-only.**','**'+label+'. Director-only.**')
        s=s.replace('**Draft awaiting exact GPT review.**','**'+label+'.**')
        s=s.replace('For this exact-review draft, a **successful benefit resolution**','A **successful benefit resolution**')
        s=s.replace('This success boundary is explicitly submitted for exact GPT review.','This success boundary was explicitly approved in the exact GPT review.')
        s=s.replace('Exact manuscript approval, numerical balance, ingredient availability, runtime/companion integration and whole-game delivery remain separate.','Exact manuscript approval is complete for this set. Numerical balance, ingredient availability, runtime/companion integration and whole-game delivery remain separate unfinished gates.')
        p.write_text(s,encoding='utf-8')
    for p in paths[4:]:
        x=read(p);x.update(status=label,exactReviewTurnId=TURN)
        for c in x['cards']:c['status']='reviewed-authored-operational-playtest'
        dump(p,x)
    manifest={'status':label,'sourceConferenceTurnId':'c79c204e-c973-4340-a590-7aae79c1110c','sourceConferenceReplyId':'cbbb06fe-f365-4437-8b62-69f6a8768980','exactReviewTurnId':TURN,'exactReplyId':REPLY,'repairsApplied':repairs['repairs'],'clarificationsApproved':repairs['clarificationsApproved'],'coverage':{'recipes':45,'public':29,'restricted':3,'directorOnly':13,'topicalHealing':18,'hazardBuffs':22,'antidotes':4,'panacea':1},'validationChecks':43,'protectedSourceAndPriorRuleArtifactsUnchanged':19,'artifactHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in paths},'replyHashes':{source_reply.name:sha(source_reply),reply.name:sha(reply)},'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,'remainingRecipeEffects':597,'cosmology':'Deferred until authorized GitHub push succeeds and remote commit is verified.'}
    dump(status,manifest)
    wrapper='# Herbalism source and exact manuscript review\n\nActual notebook: [Calibration Review](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede). Source conference `c79c204e-c973-4340-a590-7aae79c1110c`, reply `cbbb06fe-f365-4437-8b62-69f6a8768980`; exact review `'+TURN+'`, reply `'+REPLY+'`. The full [source conference](GPT_HERBALISM_SOURCE_CONFERENCE.txt) and [exact review](GPT_HERBALISM_EXACT_REVIEW.txt) are preserved.\n\nThe exact reply approves all 45 formulas once four finite repairs are applied. All are applied:\n\n'+''.join('- '+x+'\n' for x in repairs['repairs'])+'\nThree explicit clarifications were also approved:\n\n'+''.join('- '+x+'\n' for x in repairs['clarificationsApproved'])+'\nThe active recipe-tag array is named `operational.effect.recipeTags`; original source `tags` remain separately preserved as `sourceRecipeTags` and in full source evidence. This removes the operational/source ambiguity without discarding ingredient metadata.\n\nThe final [manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_REVIEW_STATUS.json) pins all six artifacts. There are 29 public, three restricted and 13 Director-only formulas; all 29 public effects match their V5 book paragraphs. 43 source/projection checks pass and 19 protected source/prior-rule files remain byte-identical. This is authored operational review, not numerical balance, runtime execution, full-game approval or delivery. No source deletion or GitHub push; cosmology stays deferred.\n'
    (AUDIT/'GPT_HERBALISM_EXACT_REVIEW.md').write_text(wrapper,encoding='utf-8')
    f=AUDIT/'HERBALISM_EXACT_SUBMISSION.json';x=read(f);x.update(status='completed; four finite repairs applied',exactReviewTurnId=TURN,exactReplyId=REPLY,validationChecks=43,reviewStatus=str(status.relative_to(GAME)));dump(f,x)
    p=AUDIT/'HERBALISM_AUTHORING_DECISIONS.json';x=read(p);x.update(status='authoring direction and exact manuscripts reviewed; four repairs applied in final artifacts',exactReviewTurnId=TURN);dump(p,x)
    p=AUDIT/'HERBALISM_REVIEW_CASES.md';s=p.read_text(encoding='utf-8');s=s.replace('Reconcile any changed disposition into these examples before closing the batch.','The actual exact review approves these boundaries after the four recorded repairs.');s=s.replace('This clarification awaits exact review.','This clarification is approved.');s=s.replace('Submitted draft','Reviewed rule');s=s.replace('submitted draft','reviewed rule');s=s.replace('explicitly submitted for exact review','explicitly approved in the exact review');s=s.replace('once present, control which submitted interpretations have been accepted','control the accepted interpretations');p.write_text(s,encoding='utf-8')
    coverage=ROOT/'data/playtest/game_development_coverage.json';backup(coverage,'COVERAGE_BEFORE_HERBALISM.json');cv=read(coverage)
    notes={
        'DD-24':'All 18 Herbalism topical healing/treatment profiles reviewed, with actual healing endpoints and one bounded local care interaction; no automatic Wound, Burning, Injury or disease removal. Antidotes and Panacea retain precise independent source-record cures.',
        'DD-28':'All 45 Herbalism consumables have reviewed delivery, timing, hazard scopes, recipe tags, containers, expiry and quality. 29 public formulas remain separate from three restricted and 13 Director-only.',
        'DD-29':'90 of 687 recipe effects are now reviewed (45 Alchemy plus 45 Herbalism); 597 remain. Herbalism includes maximum pre-check packaging/carrier reservation, the unique recipe-201 mass deficit and returned tiered mortars.',
        'DD-30':'Herbalism preserves exact batch/unit reference values and separate real packaging/carrier acquisition. Numerical price/effect balance and wider economy remain open.',
        'DD-54':'Herbalism public 29-card set excludes the three restricted and 13 Director-only formulas. Panacea procedure and seasonal recipient history remain internal.',
        'DD-63':'Herbalism JSON projection now separates original source tags from current operational recipe tags and records recipient/timing/quality boundaries. No live companion implementation or parity claim.'}
    for a in cv['aspects']:
        if a['id'] not in notes:continue
        a['status']='selected-interfaces-closed-remainder-integrating';a['closure']='open'
        for k,vals in {'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_HERBALISM_EXACT_REVIEW.md'],'sourceEvidence':['docs/audit/2026-10-08/full-game/HERBALISM_SOURCE_EVIDENCE.json'],'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_RECIPE_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md'],'validationEvidence':['docs/audit/2026-10-08/full-game/HERBALISM_CANDIDATE_VALIDATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_REVIEW_STATUS.json']}.items():
            for value in vals:
                if value not in a.setdefault(k,[]):a[k].append(value)
        a.setdefault('completedScopes',[]).append(notes[a['id']])
    dump(coverage,cv)
    start=GAME/'START_HERE.md';backup(start,'START_HERE_BEFORE_HERBALISM.md');s=start.read_text(encoding='utf-8')
    s=s.replace('642 other recipe effects','597 other recipe effects').replace('other642 recipe effects','other597 recipe effects')
    s=s.replace('| Ordinary spells |','| [Herbalism recipes](DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md) | All 45 formulas jointly reviewed; 29 public, 16 separately gated; 43 checks pass | Ingredient availability, runtime and balance |\n| Ordinary spells |',1)
    s=s.replace('The latest recipe work completes [all45 Alchemy formulas]','The preceding recipe work completed [all45 Alchemy formulas]',1)
    anchor='The preceding recipe work completed [all45 Alchemy formulas]'
    para='The latest recipe work completes [all 45 Herbalism formulas](DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_RECIPE_PLAYTEST.md), including [29 public cards](DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md). GPT’s four exact repairs are applied; 43 checks pass and 19 prior source/rule files are unchanged. The [recipe index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md) now records **90 of 687 recipes reviewed; 597 remain**. Cooking’s 44 source recipes are prepared for the next conference. No deletion, GitHub push or cosmology review occurred.\n\n'
    assert anchor in s;s=s.replace(anchor,para+anchor,1)
    old='All 687 recipe effects remain separate work: their source records are preserved, with 433 public rows kept separate from restricted/Director entries. The next recipe pass begins with 45 Alchemy formulas.'
    new='The source catalog contains 687 effects, including 433 public rows kept separate from restricted/Director entries. Alchemy and Herbalism now account for 90 reviewed effects; the remaining 597 stay in the recipe queue.'
    assert old in s;s=s.replace(old,new,1);start.write_text(s,encoding='utf-8')
    review=AUDIT/'REVIEW_STATUS.md';backup(review,'REVIEW_STATUS_BEFORE_HERBALISM.md')
    with review.open('a',encoding='utf-8') as f:f.write('\n\n## All 45 Herbalism recipe effects reviewed\n\nThe [source and exact GPT reviews](GPT_HERBALISM_EXACT_REVIEW.md) approve the complete set after four finite repairs, all applied: recipe tags, mandatory maximum packaging reservation, final timed-application completion point and record-specific Local Treatment. Panacea’s actual-benefit entitlement, concurrent attempt lock and stable season/fallback clock are approved. Visibility remains 29 public / 3 restricted / 13 Director-only. 43 checks pass; 19 source/prior-rule artifacts are unchanged. [Final manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_REVIEW_STATUS.json).\n\nAggregate recipe progress is 90 reviewed / 597 remaining; previous counts are historical checkpoints. [Cooking preparation](COOKING_NEXT_REVIEW_NOTES.md) captures the next 44 source records and concrete meal/trait/failure questions without approving them. Runtime, availability, balance, wider game flow and final delivery remain open. No original deletion, GitHub push or cosmology work.\n')
    (AUDIT/'HERBALISM_REVIEW_CHECKPOINT.md').write_text('# Herbalism completed\n\nAll 45 formulas are jointly reviewed after the four exact repairs. 29 public cards, three restricted and 13 Director-only formulas retain their source boundaries. All six final artifacts are hashed. 43 source/projection checks pass; 19 protected sources/prior rules are byte-identical. No source information was deleted.\n\nCurrent recipe progress: 90 of 687 reviewed, 597 remaining. Next: Cooking 44 (30 public, two restricted, 12 Director-only), whose unchanged full source records are in COOKING_SOURCE_PREPARATION.json. Read COOKING_NEXT_REVIEW_NOTES.md before its source conference. Then other recipe families and the remaining whole-game ledger, including expedition/Haven, spells, feats and companion integration. No GitHub push yet; careful cosmology review only after successful authorized push and verified remote commit.\n',encoding='utf-8')
    print(json.dumps({'status':label,'recipes':45,'aggregateReviewed':90,'remaining':597,'checks':43}))

if __name__=='__main__':main()
