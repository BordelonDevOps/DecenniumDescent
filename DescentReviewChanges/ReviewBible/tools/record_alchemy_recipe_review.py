"""Promote the complete Alchemy manuscript only after actual joint review."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TURN='472ee86f-89f7-4b0c-a571-87b33be6d65e'
FOLLOWUP='d28816d4-0d74-4b82-9449-2e9bb5903a20'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def backup(p,name):
    q=AUDIT/name
    if not q.exists():q.write_bytes(p.read_bytes())

def main():
    status=ROOT/'docs/mechanics/ALCHEMY_REVIEW_STATUS.json'
    if status.exists():raise SystemExit('Alchemy review already recorded.')
    v=read(AUDIT/'ALCHEMY_CANDIDATE_VALIDATION.json');assert v['status']=='PASS' and v['checkCount']==46
    reply=AUDIT/'GPT_ALCHEMY_EXACT_REVIEW.txt';follow=AUDIT/'GPT_ALCHEMY_RECIPIENT_CONTAINER_FOLLOWUP.txt'
    assert 'entire 45-card Alchemy packet may be marked' in reply.read_text(encoding='utf-8')
    assert 'complete 45-formula Alchemy set approved' in follow.read_text(encoding='utf-8')
    label='REVIEWED provisional authored operational PLAYTEST Alchemy recipe set'
    paths=[ROOT/'docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md',ROOT/'docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md',ROOT/'data/playtest/alchemy_recipe_candidate.json',ROOT/'data/director/alchemy_recipe_candidate_internal.json']
    for p in paths[:3]:
        s=p.read_text(encoding='utf-8')
        s=s.replace('**Draft awaiting joint source and manuscript review.**','**'+label+'.**')
        s=s.replace('**Draft awaiting joint review.**','**'+label+'.**')
        s=s.replace('These rules and the accompanying recipe cards are proposed completions','These rules and the accompanying recipe cards are jointly reviewed authored completions')
        s=s.replace('## Worked boundaries for joint review','## Worked boundaries')
        s=s.replace('part of this same proposed review','part of this same completed authored review')
        s=s.replace('Proposed ordinary merchant treatment','Reviewed ordinary merchant treatment')
        s=s.replace('this proposed card completes it as','this reviewed card completes it as')
        p.write_text(s,encoding='utf-8')
    for p in paths[3:]:
        d=read(p);d.update(status=label,exactReviewTurnId=TURN,followupReviewTurnId=FOLLOWUP)
        for c in d['cards']:c['status']='reviewed-authored-operational-playtest'
        dump(p,d)
    repairs=['Packaging/carrier reserved before the check; full quality yield must be physically packable, with no post-roll acquisition or partial bonus yield.',
             'Strength bonus is once per recipient direct rolled successful melee attack; no accuracy, indirect damage or other-creature propagation.',
             'Durability quality creates Standard quantity with all finished containers at maximum/current HP2; no bonus yield combined.',
             'Machine projection records initial telepathy perception, independent cure sequence, actual RP caps/nonconversion, normal immunity-expiry trigger and bomb origin-range/no-chain rules.']
    clarifications=['Summoned/created creatures may themselves be legal recipients; qualification remains the prior direct successful melee-attack damage predicate, including melee spell attacks.',
                    'Intact spent oral containers are ordinary0.1lb/1gp-reference vials reusable without repurchase; no rare component tier/properties/value regenerate. Used bomb containers return nothing.']
    manifest={'status':label,'exactReviewTurnId':TURN,'exactReplyId':'1058cd84-a133-48d2-8f2d-23a60e395dd7','followupReviewTurnId':FOLLOWUP,'followupReplyId':'6d66f006-89f1-404f-b601-5489d1f41ee5',
       'repairsApplied':repairs,'clarificationsApplied':clarifications,'coverage':{'recipes':45,'public':27,'restricted':5,'directorOnly':13,'families':6},
       'validationChecks':46,'protectedSourceAndPriorRuleArtifactsUnchanged':17,
       'approvalBasis':'Both actual replies explicitly approve the complete45-card set after the stated edits; the exact-review resistance enumeration omits recipe15, but both complete-set dispositions include it and its source/card was supplied.',
       'strengthClarificationInterpretation':'Qualifying melee damage refers to the direct successful melee attack predicate required by the first exact review; recipient followup changes propagation/origin eligibility only, not nonattack-damage scope.',
       'artifactHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in paths},
       'replyHashes':{reply.name:sha(reply),follow.name:sha(follow)},'originalSourcesDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,
       'remainingRecipeEffects':642,'cosmology':'Deferred until authorized push succeeds and remote commit is verified.',
       'remaining':['642 other recipe effects','Ingredient availability and legitimate harvesting','Numerical balance and wider economy','Runtime/companion parity','Full expedition/Haven and whole-game flow']}
    dump(status,manifest)
    wrapper='# Alchemy source and exact manuscript review\n\nActual notebook: [Calibration Review](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede). Exact turn `'+TURN+'`, response `1058cd84-a133-48d2-8f2d-23a60e395dd7`; focused followup turn `'+FOLLOWUP+'`, response `6d66f006-89f1-404f-b601-5489d1f41ee5`. Full [exact review](GPT_ALCHEMY_EXACT_REVIEW.txt) and [two-point followup](GPT_ALCHEMY_RECIPIENT_CONTAINER_FOLLOWUP.txt) are preserved.\n\nAll four exact repairs and both followup clarifications are applied:\n\n'+''.join('- '+x+'\n' for x in repairs+clarifications)+'\nBoth replies expressly approve the complete45-formula set. The first response’s final resistance-ID list accidentally omits15; that formula was included in the submitted source/manuscript and is covered by both explicit whole-set dispositions. The followup’s phrase qualifying melee damage is read with the preceding exact direct successful melee-attack predicate; it does not reopen nonattack damage.\n\nThe [final manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_REVIEW_STATUS.json) records hashes. There are27 public,5 restricted and13 Director-only entries.46 source/projection checks pass;17 protected source/prior-rule files remain byte-identical. The other642 recipe effects, availability, runtime, balance, full game flow and final delivery remain open. No deletion/push or cosmology adjudication occurred.\n'
    (AUDIT/'GPT_ALCHEMY_EXACT_REVIEW.md').write_text(wrapper,encoding='utf-8')
    f=AUDIT/'ALCHEMY_EXACT_SUBMISSION.json';s=read(f);s.update(status='completed; four repairs and two focused clarifications applied',followupTurnId=FOLLOWUP,followupReplyId=manifest['followupReplyId'],followupReplyFile=follow.name,reviewStatus=str(status.relative_to(GAME)),validationChecks=46);dump(f,s)
    coverage=ROOT/'data/playtest/game_development_coverage.json';backup(coverage,'COVERAGE_BEFORE_ALCHEMY.json');cv=read(coverage)
    notes={
      'DD-13':'Alchemy recipe3/37/627 RP1/4/6 recovery reviewed with real-pool cap, per-recipient+recipe LR entitlement and no RC/Dissonance/Refrain conversion/reset. Ordinary spells remain separate.',
      'DD-24':'Six Alchemy healing profiles and the three explicit independent poison/disease riders reviewed under existing HP/life-state rules; no generic resurrection/Wound/curse removal.',
      'DD-28':'All45 Alchemy dose effects, delivery, magic/nonspell classification, duration/stacking, bombs, quality and physical containers jointly reviewed.27 public entries;18 restricted/Director remain separate.',
      'DD-29':'45 of687 recipe effects reviewed;642 remain. Alchemy preserves all original requirements/legacy fields and adds finite packaging, first processing phase, precise quality and ordinary spent-vial handling.',
      'DD-30':'Alchemy batch-to-unit values and finite quoted merchant treatment reviewed. High-tier source price/effect disparities preserved for later balance/economy review.',
      'DD-54':'Alchemy public27 cards separated from5 restricted and13 Director-only. Internal review does not grant public access.',
      'DD-63':'Code inspection identifies concrete CraftingBuilder gaps: name-only material merging, random mass/rarity, missing batch/review fields and improvised random experiment outputs. No runtime change or parity approval.'}
    for x in cv['aspects']:
        if x['id'] not in notes:continue
        x['status']='selected-interfaces-closed-remainder-integrating';x['closure']='open'
        for key,vals in {'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_ALCHEMY_EXACT_REVIEW.md'],
          'sourceEvidence':['docs/audit/2026-10-08/full-game/ALCHEMY_RECIPE_SOURCE_EVIDENCE.json','docs/audit/2026-10-08/full-game/ALCHEMY_PUBLIC_BOOK_BINDINGS.json'],
          'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md'],
          'validationEvidence':['docs/audit/2026-10-08/full-game/ALCHEMY_CANDIDATE_VALIDATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_REVIEW_STATUS.json']}.items():
            for value in vals:
                if value not in x.setdefault(key,[]):x[key].append(value)
        x.setdefault('completedScopes',[]).append(notes[x['id']])
        if x['id']=='DD-63':x['sourceEvidence'].append('docs/audit/2026-10-08/full-game/CRAFTING_COMPANION_GAP_AUDIT.json')
    dump(coverage,cv)
    start=GAME/'START_HERE.md';backup(start,'START_HERE_BEFORE_ALCHEMY.md');s=start.read_text(encoding='utf-8')
    s=s.replace('| Ordinary spells |','| [Alchemy recipes](DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md) | All45 Alchemy formulas jointly reviewed;27 public,18 separately gated;46 checks pass |642 other recipe effects, ingredient availability, runtime and balance |\n| Ordinary spells |',1)
    s=s.replace('All 687 recipe effects, magical containment, full expedition/Haven flow, runtime and balance','642 other recipe effects, magical containment, full expedition/Haven flow, runtime and balance',1)
    s=s.replace('The latest reviewed scope is [crafting, harvesting and preservation]','The preceding reviewed framework is [crafting, harvesting and preservation]',1)
    anchor='The preceding reviewed framework is [crafting, harvesting and preservation]'
    para='The latest recipe work completes [all45 Alchemy formulas](DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md), with [27 public cards](DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md) and the [current recipe status index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md). GPT’s four exact repairs and two recipient/container clarifications are applied;46 checks pass. The other642 recipe effects remain open. Earlier framework notes stating all687 unreviewed describe that earlier checkpoint and are superseded by this recipe index. No source was deleted and no GitHub push or cosmology review occurred.\n\n'
    s=s.replace(anchor,para+anchor,1);start.write_text(s,encoding='utf-8')
    review=AUDIT/'REVIEW_STATUS.md';backup(review,'REVIEW_STATUS_BEFORE_ALCHEMY.md')
    with review.open('a',encoding='utf-8') as f:f.write('\n\n## All45 Alchemy recipe effects reviewed\n\nThe [actual exact review and focused followup](GPT_ALCHEMY_EXACT_REVIEW.md) approve all45 Alchemy formulas after four repairs and two clarifications, all applied. Visibility remains27 public/5 restricted/13 Director-only. The [review manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_REVIEW_STATUS.json) records exact hashes.46 source/projection checks pass;17 protected prior-rule/source files remain unchanged. The current recipe review catalog supersedes earlier all687-unreviewed checkpoint counts:45 reviewed,642 remaining.\n\nA separate [companion code audit](CRAFTING_COMPANION_GAP_AUDIT.json) records actual runtime integration gaps without claiming implementation. Next: other coherent recipe families, broader expedition/Haven integration and the remaining spell/feat/game areas. No source deletion, GitHub push or cosmology evaluation.\n')
    (AUDIT/'ALCHEMY_REVIEW_CHECKPOINT.md').write_text('# Alchemy completed\n\nAll45 Alchemy formulas are jointly reviewed, with four exact repairs and two focused clarifications applied.46 checks pass.27 public cards and18 separately gated cards are indexed. Original17 source/prior-rule artifacts remain byte-identical. Review manifest contains final hashes.\n\nNext: other recipe families (suggest Herbalism45 next, then Cooking44/Poisoncrafting41 and the remaining equipment/charged-item families), then full expedition-to-Haven and broader remaining game work.642 recipe effects still unreviewed; read CRAFTING_RECIPE_COMPLETION_QUEUE.json for25 source families/56 flagged questions and current recipe registry for live review status. The companion code audit names concrete remaining runtime gaps. No GitHub push; cosmology only after successful authorized push and remote verification.\n',encoding='utf-8')
    print(json.dumps({'status':label,'recipes':45,'remaining':642,'repairs':4,'clarifications':2,'checks':46}))

if __name__=='__main__':main()
