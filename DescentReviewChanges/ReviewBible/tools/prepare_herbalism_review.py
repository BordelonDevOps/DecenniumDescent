"""Capture the complete Herbalism source set before authoring any overlay."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,zipfile,xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    if (AUDIT/'HERBALISM_SOURCE_EVIDENCE.json').exists():raise SystemExit('Evidence already captured; inspect instead of replacing.')
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    data=json.loads(source.read_text(encoding='utf-8-sig'));recipes=[r for r in data['recipes'] if r['skill']=='Herbalism']
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    binding=[]
    for r in recipes:
        hits=[i for i,s in enumerate(ps) if s.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];assert ps[i-4]=='Effect. '+r['effects']
            binding.append({'recipeId':r['id'],'effectMatches':True,'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:assert not hits,(r['id'],hits)
    dump(AUDIT/'HERBALISM_SOURCE_EVIDENCE.json',{'sourcePath':str(source.relative_to(GAME)),'sourceSha256':sha(source),'bookPath':str(book.relative_to(GAME)),'bookSha256':sha(book),'sourceIndices':{r['id']:data['recipes'].index(r) for r in recipes},'recipes':recipes,'publicBookBindings':binding})
    frozen=[source,book,GAME/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json',ROOT/'src/data/crafting-recipes.json',GAME/'src/data/crafting-recipes.json']
    frozen += [ROOT/'docs/mechanics'/n for n in ['CRAFTING_HARVEST_PLAYTEST.md','CRAFTING_TRADE_REFERENCE.md','CORE_RESOLUTION_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','CONDITIONS_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','ALCHEMY_RECIPE_PLAYTEST.md','ALCHEMY_PUBLIC_RECIPE_CARDS.md','ALCHEMY_REVIEW_STATUS.json']]
    frozen += [ROOT/'data/playtest'/n for n in ['equipment_acquisition_candidate.json','crafting_engine_candidate.json','alchemy_recipe_candidate.json']]
    frozen += [ROOT/'data/director/alchemy_recipe_candidate_internal.json']
    dump(AUDIT/'HERBALISM_REVIEW_BASELINE.json',{'files':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in frozen}})
    compact=[{k:r[k] for k in ['id','name','visibility','effects','mechanics','recipeFamily','quantity','tier','rarity','skillLevel','difficulty','craftingTime','components']} for r in recipes]
    prompt='''HERBALISM SOURCE CONFERENCE — 45 formulas, before exact cards. Alchemy now has both approvals, all four repairs and both recipient/vial clarifications applied; 46 checks pass. No deletion or push. Cosmology remains strictly deferred until successful authorized push and verified remote commit.

I have captured all 45 Herbalism V4 records and exact matching V5 public passages. Their source developed labels are not approval. Please settle the following operational source ambiguities as provisional game design, not new recovered canon. Review all supplied formula effects/ingredients; identify any overlooked exception. I will then send the full candidate for exact review.

Proposals/questions:
1. All crafted Herbalism effects in this set are magical nonspell consumables, with no generic RP/RC, attunement or artifact status. Kit proficiency is manufacturing eligibility, not required for administration. Tags do not grant damage, resistance or toxic side effects. Dream-Bark Sleeping Draught has only its actual psychic hazard bonus, not sleep; Regeneration Poultice only its healing/treatment, not repeated regeneration. Keep names and legacy text preserved.
2. Antidotes: Action, one hand, drink/feed willing or Incapacitated compatible active recipient within5ft, ends present removable Poisoned condition record(s) only; does not delete underlying disease/toxin curse/intoxication emergency or prevent future reapplication. Advantage against poison for actual duration; source bonus1/3 is not an added numeric bonus because complete source prose prints advantage. Should ending Poisoned clear all currently removable applications or exactly one selected record? Propose all removable Poisoned applications while keeping their independent causes. Source-specific irremovable clauses control.
3. Balms/compresses/salves/poultice: one uninterrupted active minute (10 consecutive regular-turn Actions if initiative), touch and one available hand throughout, no concentration requirement, willing/Incapacitated compatible accessible tissue recipient; dose spent at start, no benefit until completion, interruption loses dose. Printed magical nonspell HP heal plus one selected local treatment: permit immediate ordinary Medicine attempt for one present eligible Bleed using actual source DC, with no extra kit charge because actual paid dose supplies materials; no proficiency requirement, no auto Wound/linked Injury/disease removal. Actual magical-healing Bleed endpoints already apply once, so this manual attempt must not duplicate a resolved endpoint. Alternatively the local treatment can satisfy a source's explicitly allowed topical dressing/cleaning step, not waive its full treatment project. Core actual Wound treatment remains8h+medical kit+1Supply+Medicine DC; these do not shortcut it. Please give exact finite rider that respects source 'treats one wound, burn, or infection appropriate to ingredients' without inventing a universal condition cure.
4. Buff Powder/Tonic/Tea/Remedy/Draught: all use Action oral prepared dose, no inhaled attack, coating or extra brewing/boiling step in play. Define 'saves and checks related to [tag] hazards' before roll: genuine defensive/identification/disarming/avoidance hazard tasks only, never attacks/damage/spellcasting checks or ordinary crafting/research because ingredient matches. Hazard tags require actual source descriptor or a concrete Director-declared physical cause, not species/alignment/origin inference. Poison/fire/cold/lightning/acid are direct matching hazard or source save. Earth rockfall/burial/unstable stone; water current/drowning; air wind/inhalation/air loss; psychic actual mental intrusion/psychic harm; Unholy only an explicitly labeled Unholy hazard, no cosmos/evil inference. Arcane explicit magical trap/ward/environmental hazard, not every enemy spell. Strength STR checks/saves to resist physical hazards/escape restraint, not attacks or allSTR checks. Stealth Stealth checks to avoid hazard detection or evade a pursuer, not generalDeception/Initiative. Vitality CON checks/saves against fatigue/environment/disease, not death saves/Wound saves/concentration or an automatic additional recovery. Multiple Herbalism buffs qualifying one roll use the strongest numeric bonus; an independent legal advantage can coexist. Does this bound actual source faithfully enough? Please settle concrete scope rather than blanket all checks.
5. Panacea647: ten active uninterrupted minutes, one hand touching/willing or Incapacitated compatible creature, dose+recipient entitlement committed at legal start; independent cure one selected removable disease OR poison OR external removable curse OR one legally removable Exhaustion level, then10d6+20 HP. Respect source cures, no intrinsic Oracle curse/Corruption/Wound/soul/Dead revival, no cosmology review. Recipient cap cannot be bypassed by crafter/dose ownership/death/rest. What season clock exactly? Existing source V5P11–12/P88 says one Opening100days2400hours; Gameplay Loop section20 says one Opening may contain many expeditions/contracts/stages/campaign seasons and those are not additional Openings. Thus season≠Opening automatic. Propose once per registered campaign season with actual stable seasonID set before use and recorded transition, never session/travel/long rest/self-declaration; if no campaign season calendar exists, a provisional100elapsed-day cooldown from administration start, openly labeled as fallback rather than canon. Prefer one unambiguous rule if these two paths introduce loopholes.
6. Packaging: all45 have zero source vessel components. Propose exact same supplementary1gp/.1lb Glass vial per finished dose, .1lb compound/.2lb gross, AC13HP1 (quality durabilityHP2 across Standard quantity), one slot; no ingredient replacement. Reserve full possible bonus packaging/carrier before completion check; source recipe201 consumes.46lb but Masterwork6doses requires.6lb, so supplemental clean carrierwater.14lb must be reserved beforecheck (no substitute for exact listed materials; actual availability, separate supply). Catalyst retention can increase deficit if any. Topical paste and oral solution both fit this reusable vial, returns ordinary spent container. First15active minutes included inwork legal stabilization; shelf-life sealedindefinite/open1h, no fresh-ingredient revival. Please confirm these choices or concrete correction.
7. Quality: source batch count and prices unchanged, no potencybuff/cures/charges. Q>=2Flawedfloor(Q/2); singleton fixed-durationbuff/antidote halves only duration; antidote immediatecondition removal stays? Propose yes: reduced-duration result retains instant rider, like effect tied to primary duration. Singleton instantaneoushealing/topical/Panacea or untilLRduration=>Failed, no madeup halfhealing. Exceptional/Masterwork floor1.25Q/1.5Q or allStandardcontainersHP2; selectedemptyvials reserved beforehand. No potion label imports15/30day drug dependence without an actual reviewed substanceprofile.

Return finite decisions for these seven issues and source-specific exceptions. Do not claim exact-card approval yet or expand into cosmology. Complete source records are preserved locally; below are all45 unabridged effect/ingredient/identity records, including restricted/Director entries for internal review only.
'''
    prompt+='\n'+json.dumps(compact,ensure_ascii=False,separators=(',',':'))
    (AUDIT/'CODEX_HERBALISM_SOURCE_CONFERENCE.txt').write_text(prompt+'\n',encoding='utf-8')
    print(json.dumps({'recipes':len(recipes),'visibility':dict(Counter(r['visibility'] for r in recipes)),'publicBookMatches':len(binding),'protectedArtifacts':len(frozen),'promptCharacters':len(prompt)}))

if __name__=='__main__':main()
