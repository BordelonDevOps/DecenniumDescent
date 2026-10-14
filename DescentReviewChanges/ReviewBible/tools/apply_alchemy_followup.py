"""Apply the two agreed recipient/container clarifications without widening damage."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    guide=ROOT/'docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md';s=guide.read_text(encoding='utf-8')
    if 'an already owned spent vial requires no repurchase' in s:raise SystemExit('Followup already applied.')
    old='Empty intact containers remain actual 0.1-lb vials after an oral dose, without a refund of recipe price; a bomb consumes/breaks its container.'
    new="After oral use, the surviving empty container becomes an ordinary spent dose vial: 0.1 lb, AC 13, its actual remaining/max structural HP (normally 1, or 2 if the finished container received the approved durability improvement), and one ordinary dose of capacity. It has no remaining magical dose, ingredient-tier benefit or component properties. It may be reused as supplementary packaging if intact. Its ordinary empty-vial reference value is 1 gp, subject to an actual market quotation; an already owned spent vial requires no repurchase merely to reuse it. The original ingredient identity, tier, properties and value remain provenance only and are not recovered as usable crafting properties. The spent vial cannot satisfy a higher-tier Crystal Vial or other specialized vessel requirement except through a separately legal substitution rule. A bomb's container is destroyed by use and returns no container."
    assert s.count(old)==1;s=s.replace(old,new)
    s=s.replace('reflected damage, summoned-creature damage, independent riders','reflected damage, damage resolved by another creature, independent riders')
    anchor='or nonattack damage merely because the source operates at melee range.'
    extra="\n\nThe bonus applies only to the recipient's own qualifying melee damage roll. It does not propagate to attacks or damage resolved by another creature, including a creature summoned, created or controlled by the recipient. A summoned or created creature that is itself legally administered the dose may apply the bonus to its own qualifying melee damage rolls, subject to its existing action, command and eligibility limits. Here, qualifying retains the preceding direct rolled damage of a successful melee attack requirement, including a melee spell attack. This recipient clarification does not add a new category of nonattack damage."
    assert s.count(anchor)==1;s=s.replace(anchor,anchor+extra)
    guide.write_text(s,encoding='utf-8')
    replacements={}
    for p in [ROOT/'data/playtest/alchemy_recipe_candidate.json',ROOT/'data/director/alchemy_recipe_candidate_internal.json']:
        d=read(p)
        for c in d['cards']:
            op=c['operational'];e=op['effect']
            if c['recipeId'] in ['recipe-11','recipe-12','recipe-16']:
                e.pop('appliesToSummonedCreatureDamage',None);e.update(propagatesToRecipientsSummons=False,recipientMayBeSummonedCreature=True)
                old=op['text'];op['text']=old.replace('summoned damage','damage resolved by another creature')+" A summoned/created creature that itself legally receives the dose can benefit from its own qualifying melee attack, within its existing command/action limits."
                replacements[old]=op['text']
            op['physical']['postUseContainer']=None if e['type']=='thrown_explosive' else {
                'kind':'ordinary-spent-dose-vial','weightLb':0.1,'AC':13,'capacityDoses':1,
                'actualCurrentAndMaxHpRetained':True,'magicalUsesRemaining':0,'ingredientTierBenefit':None,
                'ingredientPropertiesRecovered':False,'originalIngredientValueRecovered':False,
                'referenceValueCp':100,'supplementaryPackagingReuseIfIntact':True,'reuseRequiresRepurchase':False,
                'originalIngredientIdentityRetainedAsProvenanceOnly':True}
        save(p,d)
    for p in [ROOT/'docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md']:
        text=p.read_text(encoding='utf-8')
        for old,new in replacements.items():
            assert old in text;text=text.replace(old,new)
        p.write_text(text,encoding='utf-8')
    print(json.dumps({'clarificationsApplied':2,'directSuccessfulMeleeAttackPredicateRetained':True,'expensiveIngredientRegenerationPrevented':True}))

if __name__=='__main__':main()
