"""Apply four finite repairs from the actual exact Herbalism review."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def edit(p,old,new,count=1):
    s=p.read_text(encoding='utf-8');assert s.count(old)==count,(p.name,s.count(old),count)
    p.write_text(s.replace(old,new),encoding='utf-8')

def main():
    if (ROOT/'docs/mechanics/HERBALISM_REVIEW_STATUS.json').exists():raise SystemExit('Already reviewed; do not reapply draft repairs.')
    reply=(AUDIT/'GPT_HERBALISM_EXACT_REVIEW.txt').read_text(encoding='utf-8');assert 'After those four finite repairs, I approve' in reply
    paths=[ROOT/'docs/mechanics/HERBALISM_RECIPE_PLAYTEST.md',ROOT/'docs/director-only/HERBALISM_INTERNAL_PROCEDURES.md',ROOT/'docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/HERBALISM_INTERNAL_RECIPE_CARDS.md',ROOT/'data/playtest/herbalism_recipe_candidate.json',ROOT/'data/director/herbalism_recipe_candidate_internal.json']
    for p in paths:
        backup=AUDIT/('BEFORE_HERBALISM_EXACT_REPAIRS_'+p.name)
        if backup.exists():raise SystemExit('Repair backup already exists; inspect partial state before resuming.')
        backup.write_bytes(p.read_bytes())
    edit(paths[0],'Source tags remain available to rules that explicitly inspect such tags, without creating new resistance, damage or disease.',"Only the recipe's explicit current `mechanics.tag`, when present, is an operational finished-dose recipe tag. Ingredient properties, ingredient names, legacy names/effects and inferred thematic labels remain source/component metadata and are not added to the finished dose's recipe-tag set. A rule that explicitly inspects recipe tags may inspect only that current recipe tag. A recipe with no current `mechanics.tag` has no operational recipe tag. The JSON keeps original `sourceRecipeTags` separately and uses `operational.effect.recipeTags` for the active set.")
    timing='Resolution occurs at the first moment both the required regular-turn Action count and the elapsed-time minimum are satisfied; no eleventh Action, or one-hundred-first Action for Panacea, is required. If the final required Action occurs before the elapsed minimum, the application remains continuously in progress until that elapsed deadline and resolves then, provided all required hand, touch/access and recipient eligibility have remained uninterrupted.'
    edit(paths[0],'finish only when both requirements are met.','finish only when both requirements are met. '+timing)
    edit(paths[1],'Extra Actions and inserted turns do not shorten either requirement.','Extra Actions and inserted turns do not shorten either requirement. '+timing)
    old='Do not make the extra Medicine check if this same dose\'s healing already resolved an explicit removal/treatment attempt for that record, including an unsuccessful source save. Ended records cannot be selected again. A different present eligible Bleeding record may be selected if this dose has not already attempted its healing endpoint.'
    new="Do not make the extra Medicine check against a Bleeding record if this same dose's healing already resolved an explicit removal or treatment attempt for that same record, including an unsuccessful source save. An ended record cannot be selected. A different present eligible Bleeding record may be selected only if this dose's healing did not already resolve an explicit removal or treatment attempt for that different record."
    edit(paths[0],old,new)
    package='The full Masterwork-reserve amount shown above, including all required vials and any listed supplementary carrier, must be physically available and reserved before the completion check regardless of the intended quality option. Consume only the amount required by the resolved output; unused reserved packaging and carrier return to ordinary inventory under the shared procedure.'
    for p,n in [(paths[2],29),(paths[3],45)]:edit(p,'All chosen-output packaging and carrier must be present before the check.',package,n)
    source={r['id']:r for r in read(AUDIT/'HERBALISM_SOURCE_EVIDENCE.json')['recipes']}
    for p in paths[4:]:
        data=read(p)
        for c in data['cards']:
            r=source[c['recipeId']];eff=c['operational']['effect'];c['sourceRecipeTags']=r['tags']
            eff.pop('sourceTags');eff['recipeTags']=[r['mechanics']['tag']] if 'tag' in r['mechanics'] else []
            c['operational']['craft']['maximumMasterworkReserveMandatory']=True
            if c['operational']['activation']['activeMinutes']:
                c['operational']['activation'].update(resolutionTiming='first moment required regular-turn Action count and elapsed minimum both satisfied',additionalActionAfterRequiredCount=False,continuousConditionsRequiredUntilResolution=True)
        dump(p,data)
    dump(AUDIT/'HERBALISM_EXACT_REPAIRS_APPLIED.json',{'status':'four exact repairs applied','exactReviewTurnId':'45dfe30e-6f5a-4efd-adaf-5fea18fbfd6f','exactReplyId':'63005e51-58e4-4bc4-a08e-e3841d6ba105','repairs':['Operational recipe tags use only explicit current mechanics.tag; original tags preserved separately.','All cards require full maximum-Masterwork packaging/carrier reservation before the check.','Timed application resolves at first instant both time and Action count complete, without an extra Action.','Local Treatment prohibits a duplicate attempt per same actual Bleeding record.'],'clarificationsApproved':['Panacea actual-benefit entitlement with one concurrent attempt; no eligible cure does not block independent healing.','Both Actions and elapsed time required.','Open potency deadline applies to legal administration start, not completion.']})
    print('Applied all four finite exact-review repairs.')

if __name__=='__main__':main()
