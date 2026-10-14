"""Pin the actual 41-card Poisoncrafting approval after its finite repairs."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TURN='f8cd1339-42dc-413b-b3cb-b071aa52b12e';REPLY='d151511f-1830-4828-8134-98c91c482444'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def backup(p,name):
    q=AUDIT/name
    assert not q.exists(), str(q)
    q.write_bytes(p.read_bytes())
def main():
    manifest=ROOT/'docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json'
    assert not manifest.exists(),'Review already recorded; inspect final state.'
    validation=read(AUDIT/'POISONCRAFTING_CANDIDATE_VALIDATION.json');assert validation['status']=='PASS' and len(validation['checks'])==50
    repairs=read(AUDIT/'POISONCRAFTING_EXACT_REPAIRS_APPLIED.json');assert len(repairs['repairs'])==5
    reply=AUDIT/'GPT_POISONCRAFTING_EXACT_REVIEW.txt';s=reply.read_text(encoding='utf-8');assert 'After applying the five items above' in s and 'all 41 cards' in s
    paths=[ROOT/'docs/mechanics/POISONCRAFTING_RECIPE_PLAYTEST.md',ROOT/'docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/POISONCRAFTING_INTERNAL_RECIPE_CARDS.md',ROOT/'data/playtest/poisoncrafting_recipe_candidate.json',ROOT/'data/director/poisoncrafting_recipe_candidate_internal.json']
    label='REVIEWED provisional authored operational PLAYTEST Poisoncrafting recipe set'
    for p in paths[:3]:
        s=p.read_text(encoding='utf-8')
        s=s.replace('**Draft awaiting exact manuscript review.** The source conference and Thief-interface follow-up approve the authoring direction. Completed cards still require exact review.','**'+label+'.** Source conference, Thief-interface follow-up and exact manuscript review are complete; all five exact corrections are applied.')
        s=s.replace('**Draft awaiting exact GPT review.**','**'+label+'.**')
        s=s.replace('This is an authored provisional ruleset, pending exact manuscript approval.','This authored provisional ruleset has completed exact manuscript review for all 41 recipes.')
        p.write_text(s,encoding='utf-8')
    for p in paths[3:]:
        x=read(p);assert x['pendingBindings']==[];x.update(status=label,exactReviewTurnId=TURN,exactReplyId=REPLY)
        for c in x['cards']:c['status']='reviewed-authored-operational-playtest'
        dump(p,x)
    replyfiles=[AUDIT/'GPT_POISONCRAFTING_SOURCE_CONFERENCE.txt',AUDIT/'GPT_POISONCRAFTING_CLASS_INTERFACE_REVIEW.txt',reply]
    dump(manifest,{'status':label,'sourceConferenceTurnId':'94caea42-6dfa-43fe-b5aa-8d1257d0b3de','sourceConferenceReplyId':'c0683977-af53-4731-ab4e-ef5f6affbc8f','classInterfaceTurnId':'767b9ae9-7d72-4d6e-a5ef-e134cefd088f','classInterfaceReplyId':'8ce8d9cd-d0a9-491a-ac04-f8b8e36c8d3e','exactReviewTurnId':TURN,'exactReplyId':REPLY,'repairsApplied':repairs['repairs'],'coverage':{'recipes':41,'public':25,'restricted':3,'directorOnly':13,'deliveryFamilies':3,'conditionFamilies':8},'validationChecks':50,'protectedSourceAndPriorRuleArtifactsUnchanged':26,'artifactHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in paths},'replyHashes':{p.name:sha(p) for p in replyfiles},'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,'aggregateReviewedRecipes':175,'remainingRecipeEffects':512,'cosmology':'Deferred until successful authorized GitHub push and verified remote commit.'})
    wrapper='# Poisoncrafting source, Thief interface and exact manuscript review\n\nActual notebook: [Calibration Review](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede). Exact turn `'+TURN+'`, reply `'+REPLY+'`. The complete [source conference](GPT_POISONCRAFTING_SOURCE_CONFERENCE.txt), [Thief/timing follow-up](GPT_POISONCRAFTING_CLASS_INTERFACE_REVIEW.txt) and [exact verdict](GPT_POISONCRAFTING_EXACT_REVIEW.txt) are preserved.\n\nGPT approved the full 41-card authored operational PLAYTEST family after five finite corrections, all applied:\n\n'+''.join('- '+r+'\n' for r in repairs['repairs'])+'\nFifty source/projection checks pass. All 41 original source records reconstruct losslessly, 25 public effects match exact V5 paragraphs, and 26 protected source/prior-rule files remain unchanged. Three restricted and thirteen Director-only formulas stay internal. The [final manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json) pins five final artifacts and all three replies.\n\nThis closes Poisoncrafting authored operational effect review only. Numerical balance, material availability, wider unfinished class/spell interactions, runtime/companion parity, human playtesting and whole-game flow remain open. No source deletion or GitHub push occurred. Cosmology remains strictly post-push.\n'
    (AUDIT/'GPT_POISONCRAFTING_EXACT_REVIEW.md').write_text(wrapper,encoding='utf-8')
    p=AUDIT/'POISONCRAFTING_EXACT_SUBMISSION.json';x=read(p)
    assert (AUDIT/'CODEX_POISONCRAFTING_EXACT_REVIEW.txt').read_text(encoding='utf-8').strip()==(AUDIT/'CODEX_POISONCRAFTING_EXACT_REVIEW_SENT.txt').read_text(encoding='utf-8').strip()
    x.update(status='completed; five exact corrections applied and validated',exactReviewTurnId=TURN,exactReplyId=REPLY,validationChecks=50,reviewStatus=str(manifest.relative_to(GAME)));dump(p,x)
    p=AUDIT/'POISONCRAFTING_SOURCE_CONFERENCE_STATUS.json';x=read(p);x.update(status='source, Thief/timing and exact manuscript reviews complete; all 41 cards reviewed after five finite corrections',recipesApproved=41,exactReviewCompleted=True,exactReviewTurnId=TURN,exactReplyId=REPLY,finalReviewManifest=str(manifest.relative_to(GAME)));dump(p,x)
    p=ROOT/'data/playtest/game_development_coverage.json';backup(p,'COVERAGE_BEFORE_POISONCRAFTING_COMPLETION.json');x=read(p)
    notes={
      'DD-18':'Poisoncrafting Stunned joins the shared source/target/encounter allowance without refresh after spending. Fixed-locus fear, source-qualified Confused/Slowed/Weakened, inherited speed modifiers and Burning ending saves are reviewed for all 41 recipes.',
      'DD-24':'Poisoncrafting distinguishes Poisoned-only cures from full poison-application removal, allows covered cures on present suppressed records, and leaves no hidden toxin that reapplies an ended sole condition. Damage already resolved is not undone.',
      'DD-28':'All 41 Poisoncrafting recipes reviewed: 26 injury, ten contact and five inhaled profiles, finite deployments, condition records, cures and physical dose accounting.',
      'DD-29':'175 of 687 recipe effects reviewed: 45 Alchemy, 45 Herbalism, 44 Cooking and 41 Poisoncrafting. The remaining 512 retain their recipe review gates.',
      'DD-30':'Poisoncrafting preserves source batch economics, separate actual supplementary vials/water, consumed process tools and ordinary spent-container value; finite markets and balance remain open.',
      'DD-54':'Poisoncrafting 25 public formulas have exact V5 bindings; three restricted and thirteen Director-only formulas remain separately gated. Public reviewed formulas now total 111 of 433.',
      'DD-63':'Poisoncrafting authored JSON now projects all 41 sources, delivery/condition/ownership clocks and the narrow Thief interface. Fifty checks pass; runtime and companion parity remain unimplemented.'}
    for z in x['aspects']:
        if z['id'] not in notes:continue
        z['status']='selected-interfaces-closed-remainder-integrating';z['closure']='open'
        for k,vals in {'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_POISONCRAFTING_EXACT_REVIEW.md'],'sourceEvidence':['docs/audit/2026-10-08/full-game/POISONCRAFTING_SOURCE_PREPARATION.json','docs/audit/2026-10-08/full-game/POISONCRAFTING_THIEF_INTERFACE_EVIDENCE.json'],'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_RECIPE_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md'],'validationEvidence':['docs/audit/2026-10-08/full-game/POISONCRAFTING_CANDIDATE_VALIDATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json']}.items():
            for v in vals:
                if v not in z.setdefault(k,[]):z[k].append(v)
        z.setdefault('completedScopes',[]).append(notes[z['id']])
    dump(p,x)
    p=GAME/'START_HERE.md';backup(p,'START_HERE_BEFORE_POISONCRAFTING.md');s=p.read_text(encoding='utf-8')
    s=s.replace('553 other recipe effects','512 other recipe effects').replace('The other 553 recipe effects remain open.','The other 512 recipe effects remain open.')
    anchor='| Ordinary spells |';assert s.count(anchor)==1;s=s.replace(anchor,'| [Poisoncrafting recipes](DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md) | All 41 formulas jointly reviewed; 25 public, 16 separately gated; 50 checks pass | Ingredient availability, wider interactions, runtime and balance |\n'+anchor)
    begin=s.index('The latest recipe work completes ');end=s.index('\n\n',begin)
    s=s[:begin]+'The latest recipe work completes [all 41 Poisoncrafting formulas](DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_RECIPE_PLAYTEST.md), including [25 public cards](DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md). GPT’s five exact corrections are applied; 50 checks pass and 26 protected source/rule files are unchanged. The [recipe index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md) records **175 of 687 recipe effects reviewed; 512 remain** (111 of 433 public formulas reviewed). The next [Blacksmithing source preparation](docs/audit/2026-10-08/full-game/BLACKSMITHING_NEXT_REVIEW_NOTES.md) preserves 43 formulas and 27 exact public-book bindings; it is not yet approved. Generated bestiary discrepancies remain recorded for correction. No deletion, GitHub push or cosmology review occurred.\n\nThe preceding [44 Cooking formulas](DescentReviewChanges/ReviewBible/docs/mechanics/COOKING_RECIPE_PLAYTEST.md), including 30 public cards, remain reviewed after five repairs and 45 checks.'+s[end:]
    s=s.replace('Alchemy, Herbalism and Cooking now account for 134 reviewed effects; the remaining 553 stay in the recipe queue.','Alchemy, Herbalism, Cooking and Poisoncrafting now account for 175 reviewed effects; the remaining 512 stay in the recipe queue.')
    p.write_text(s,encoding='utf-8')
    p=AUDIT/'REVIEW_STATUS.md';backup(p,'REVIEW_STATUS_BEFORE_POISONCRAFTING.md')
    checkpoint='All 41 Poisoncrafting recipes have completed source, Thief/timing and exact manuscript review. Five finite corrections are applied. Fifty source/projection checks pass; all 41 original records reconstruct losslessly and 26 protected files are unchanged. Visibility remains 25 public / 3 restricted / 13 Director-only. [Actual verdict](GPT_POISONCRAFTING_EXACT_REVIEW.md); [final manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json).\n\nCurrent recipe progress: **175 of 687 reviewed, 512 remaining**; public progress 111 of 433. Earlier counts are historical checkpoints. Next is [Blacksmithing](BLACKSMITHING_NEXT_REVIEW_NOTES.md): 43 preserved formulas, 27 public-book bindings and existing reviewed equipment evidence; no Blacksmithing approval yet.\n\nBroader spells, feats, expedition/Haven, generated bestiary corrections, class interactions and companion integration remain open. Human balance testing and whole-game flow remain separate gates. No source information was deleted and no GitHub push occurred. Careful cosmology review starts only after the authorized push succeeds and the remote commit is verified.\n'
    with p.open('a',encoding='utf-8') as f:f.write('\n\n## All 41 Poisoncrafting recipe effects reviewed\n\n'+checkpoint)
    (AUDIT/'POISONCRAFTING_REVIEW_CHECKPOINT.md').write_text('# Poisoncrafting completed\n\n'+checkpoint,encoding='utf-8')
    print(json.dumps({'status':label,'recipes':41,'reviewedTotal':175,'remaining':512,'checks':50}))
if __name__=='__main__':main()
