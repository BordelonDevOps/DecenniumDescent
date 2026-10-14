"""Apply GPT's four finite Alchemy repairs without touching the source recipes."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def finish_card_manuscripts():
    before=read(AUDIT/'BEFORE_ALCHEMY_REPAIRS_alchemy_recipe_candidate_internal.json')
    current=read(ROOT/'data/director/alchemy_recipe_candidate_internal.json')
    old_by={c['recipeId']:c for c in before['cards']};new_by={c['recipeId']:c for c in current['cards']}
    pairs={old_by[id]['operational']['text']:new_by[id]['operational']['text'] for id in ['recipe-11','recipe-12','recipe-16']}
    for p in [ROOT/'docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md']:
        text=p.read_text(encoding='utf-8')
        for old,new in pairs.items():
            if old in text:text=text.replace(old,new)
            elif new not in text:raise ValueError('Strength text missing from '+str(p))
        text=text.replace('select finite yield or physical container durability only.', 'select fully pre-reserved finite yield or Standard batch quantity with every container at maximum/current HP 2. No partial bonus yield or post-roll packaging acquisition. Masterwork catalyst retention remains independent.')
        p.write_text(text,encoding='utf-8')

def main():
    guide=ROOT/'docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md';s=guide.read_text(encoding='utf-8')
    if 'cannot pause resolution to buy' in s:
        finish_card_manuscripts()
        print(json.dumps({'repairsApplied':4,'completedPreviouslyInterruptedManuscriptSync':True}))
        return
    paths=[guide,ROOT/'docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md',ROOT/'data/playtest/alchemy_recipe_candidate.json',ROOT/'data/director/alchemy_recipe_candidate_internal.json']
    for p in paths:(AUDIT/('BEFORE_ALCHEMY_REPAIRS_'+p.name)).write_bytes(p.read_bytes())
    start=s.index('Each finished dose needs an actual container.')
    end=s.index('\n\nEach dose contains',start)
    s=s[:start]+'''Each finished dose needs an actual container. Recipe components with role `vessel` can supply that many output containers, each retaining its source component identity for accounting; all source consumed quantities remain spent according to the recipe. Before the completion check, reserve any supplementary empty Glass Vials and any declared carrier material needed for every quality option the crafter intends to keep available. Reserved supplementary packaging is consumed only when actually used; unused reserved packaging remains inventory.

After the quality result is known, the crafter cannot pause resolution to buy, borrow, manufacture or retrieve additional packaging or carrier material. If the reserved and source-supplied containers cannot package the full Exceptional/Masterwork yield, that yield option is unavailable; use the permitted durability option instead, or retain Standard quantity and the quality label if no legal improvement exists. No partial bonus yield, fractional dose or banked uncontained product is created. Additional packaging costs and mass are separately recorded rather than silently editing source component totals or the source batch recommendation. Original source vessel inputs follow their printed consumed flags even on a failed batch.'''+s[end:]
    old='This carrier has no independent magical effect; its mass counts and its ordinary acquisition costs are extra.'
    new=old+" A carrier deficit caused by a declared substitution must be calculated and its carrier reserved before the completion check. Carrier water satisfies physical finished mass only; it never substitutes for a recipe component's required tier, property, role or amount."
    assert s.count(old)==1;s=s.replace(old,new)
    old='The flat melee damage bonus applies once per actual melee damage roll, not per die or per damage type within that same hit; it is not doubled by a critical hit. No damage roll means no bonus packet. Spell/class damage qualifies only if it is actually a melee damage roll under that source.'
    new="The flat +1 applies once to the direct damage of each successful melee attack whose damage is actually rolled. A melee weapon attack or melee spell attack can qualify. Assemble that attack's direct damage dice/types normally, then add +1 total before defenses. Do not add it once per die, damage type or critical die, and do not double it on a critical hit. It does not apply to attack rolls, Strength saves, ranged attacks, periodic damage, transferred/copied damage, retaliation, reflected damage, summoned-creature damage, independent riders or nonattack damage merely because the source operates at melee range."
    assert s.count(old)==1;s=s.replace(old,new)
    old='The vial remains physically present with its actual HP after a legal oral use.'
    new=old+"\n\nWhen an Alchemy batch chooses the generic durability improvement instead of bonus yield, produce the recipe's Standard batch quantity, and every finished dose produced by that work order has container maximum structural HP 2 and begins at 2 structural HP. The magical contents are unchanged. This improvement does not create extra units and is not cumulative with the quality-yield option. Masterwork catalyst retention remains independently applicable as normal."
    assert s.count(old)==1;s=s.replace(old,new)
    old='Apply ordinary advantage/disadvantage cancellation.'
    new='Measure this range band from the user to the burst origin (the thrown destination point), once for the throw, not separately from the user to each victim. '+old
    assert s.count(old)==1;s=s.replace(old,new)
    guide.write_text(s,encoding='utf-8')
    replacements={}
    for p in paths[3:]:
        d=read(p)
        for c in d['cards']:
            id=c['recipeId'];op=c['operational'];e=op['effect'];craft=op['craft']
            craft.update(supplementaryInputsReserveTiming='before-completion-check',postRollPackagingAcquisitionAllowed=False,
                         qualityYieldRequiresFullPackaging=True,partialBonusYieldAllowed=False,
                         qualityDurabilityOption='Standard batch quantity; every finished container max/current HP2; no extra yield; Masterwork catalyst retention independent')
            if id in ['recipe-11','recipe-12','recipe-16']:
                old=op['text'];duration=c['sourceMechanics']['duration']
                op['text']=f'Gain +1 to Strength ability checks and +1 total to direct rolled damage of each successful melee attack for {duration}. Melee weapon/spell attacks qualify; no attack accuracy, saves, ranged attacks, periodic/copied/transferred/reflected damage, retaliation, summoned damage, independent riders or nonattack damage. Add once before defenses, never per die/type or doubled on a critical.'
                replacements[old]=op['text'];e.update(meleeDamagePredicate='direct rolled damage of successful melee attack',damageBonusPerAttack=1,criticalDoublesFlatBonus=False,appliesToIndependentRiders=False,appliesToSummonedCreatureDamage=False)
            if id in ['recipe-24','recipe-27','recipe-626']:e.update(telepathyRequiresPerception=True,telepathyPerceptionTiming='initial-contact-only')
            if id in ['recipe-36','recipe-38','recipe-40']:e.update(cureTiming='after-healing-attempt',cureIndependentOfPositiveHpRestoration=True,cureRequiresPresentRemovableEffect=True)
            if id in ['recipe-3','recipe-37','recipe-627']:e.update(requiresExistingRpPool=True,cappedAtActualRpMaximum=True,clearsDissonance=False,clearsRefrain=False,operation='RP-resource-recovery')
            if id=='recipe-41':e.update(followingResistanceTrigger='normal-immunity-expiry-only',earlyImmunityEndingTriggersResistance=False)
            if id in ['recipe-13','recipe-26','recipe-28','recipe-39','recipe-624']:e.update(longRangeBandMeasuredToBurstOrigin=True,chainDetonation=False)
        save(p,d)
    finish_card_manuscripts()
    print(json.dumps({'repairsApplied':4,'sourceFilesChanged':0,'publicAndInternalProjectionAligned':True}))

if __name__=='__main__':main()
