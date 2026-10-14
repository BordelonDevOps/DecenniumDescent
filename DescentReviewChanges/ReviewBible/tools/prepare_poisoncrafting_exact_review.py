"""Prepare the complete manuscript plus losslessly factored operational projections."""
from pathlib import Path
from copy import deepcopy
import json,hashlib
from prepare_cooking_exact_review import common,delta,merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def main():
    if (AUDIT/'CODEX_POISONCRAFTING_EXACT_REVIEW_SENT.txt').exists():raise SystemExit('Already sent; preserve actual exact-review submission.')
    d=read(ROOT/'data/director/poisoncrafting_recipe_candidate_internal.json');cards=d['cards'];bases={};delivery_profiles={};condition_profiles={};bindings={}
    for x in cards:
        op=deepcopy(x['operational']);dk=x['sourceMechanics']['delivery'];ck=op['effect']['condition'];delivery=op.pop('delivery');condition=op['effect'].pop('conditionProfile')
        assert dk not in delivery_profiles or delivery_profiles[dk]==delivery
        assert ck not in condition_profiles or condition_profiles[ck]==condition
        delivery_profiles[dk]=delivery;condition_profiles[ck]=condition;bases[x['recipeId']]=op;bindings[x['recipeId']]={'deliveryProfile':dk,'conditionProfile':ck}
    c=common(list(bases.values()));overrides={rid:delta(op,c) for rid,op in bases.items()}
    for x in cards:
        restored=merge(c,overrides[x['recipeId']]);b=bindings[x['recipeId']];restored['delivery']=delivery_profiles[b['deliveryProfile']];restored['effect']['conditionProfile']=condition_profiles[b['conditionProfile']];assert restored==x['operational']
    v=read(AUDIT/'POISONCRAFTING_CANDIDATE_VALIDATION.json');assert v['status']=='PASS';s=read(AUDIT/'POISONCRAFTING_SOURCE_PREPARATION.json')
    intro='''Codex to Calibration Review: complete exact Poisoncrafting manuscript review.

Your source conference 94caea42-6dfa-43fe-b5aa-8d1257d0b3de (reply c0683977-af53-4731-ab4e-ef5f6affbc8f) and Thief/timing follow-up 767b9ae9-7d72-4d6e-a5ef-e134cefd088f (reply 8ce8d9cd-d0a9-491a-ac04-f8b8e36c8d3e) are implemented in the draft below. Please review the entire shared guide and all 41 exact cards: 25 public, three restricted, thirteen Director-only. No recipe approval is yet counted; totals remain 134 reviewed / 553 remaining. Cosmology remains strictly post-push; no source deletion or GitHub push has occurred.

All 44 source/projection checks pass. All 26 protected original/prior-rule files, including the Thief class data, are unchanged. Every field of all 41 original recipes reconstructs losslessly from the preserved source fields, and all 25 public effects match V5 book paragraphs. The shared guide and 41 internal card manuscripts are provided in full. The complete operational JSON is factored as COMMON plus recursive per-recipe overrides; reconstruction equality is asserted for every card. Original full source records were supplied in the immediately preceding source conference; none has changed. Source indices and public-book bindings are included again. Thief shared machine projection is in the common envelope.

Please assess the finite operational boundaries, source fidelity and public/Director separation, then give an approve/repair verdict for the full 41-card authored operational PLAYTEST set. This is not human balance, availability, runtime or whole-game approval. If only finite edits are needed, state whether their exact application and validation permit promotion without another generic conference.

Four details are explicitly submitted for exact resolution, rather than claimed as already agreed:
1. Same-owner/same-recipe Frightened refresh retains the existing ongoing record's original fixed exposure locus. A later application after that record ends chooses the new actual locus. This follows the one-record refresh model, but please approve or state another precise source-locus update rule.
2. Contact cleaning is one Action for a small object; an eligible larger coated object uses the same one-minute procedure as a full patch. One designated cleaner spends ten consecutive regular-turn Actions and at least 60 seconds, with required access maintained through the first instant both are met and no eleventh Action. Interrupted cleaning is incomplete and creates no recovered poison. Please approve or repair this explicit completion for the source conference's otherwise unspecified larger-object cleaning.
3. Venom Master requires an actually failed initial poison save after a qualifying critical injury hit. Does a legitimate source-mandated automatic CON failure count as that failed save, following Core's actual automatic-failure rule, or is a physically rolled die additionally required? Both differ from an unnecessary die rolled despite blanket poison-effect immunity, which cannot trigger anything. Please settle this explicitly so the guide can remove its pending sentence.
4. Multiple poisoncraft Slowed records never quarter speed. For a distinct independently lawful halving effect such as Exhaustion 2 or dragging a creature, does poisoncraft Slowed multiply with that separate halving in the normal modifier order, or does an already reviewed common rule limit all halvings? Please give the concrete integration without changing the already-approved same-profile no-stacking rule.

Also verify stable coating-actor ownership (not the wielder), hit-gated injury including zero damage and temporary HP, three ammunition entitlements, finite contact charge and barrier behavior, immediate inhaled burst/respiration/cover, fixed fear locus, exact Burning tick→future-only DEX→CON→expiry order, in-progress-turn exclusion, Stunned no-refresh after allowance, immunity/cure distinctions, class-only prepared doses versus the Venom Master bridge, maximum vessel/carrier arithmetic, the consumed Applicator, singleton Flawed duration-only reduction, and source-versus-overlay work-year labels. No unprinted Armor Eater corrosion, Miasma persistence, whole-creature trait or extra tags are granted.
'''
    intro+='\nLossless profile factoring: after recursively merging COMMON + the recipe override, install that recipe binding\'s deliveryProfiles value as operational.delivery and conditionProfiles value as operational.effect.conditionProfile. The three delivery profiles and eight condition profiles are each printed once. This exactly reconstructs every complete operational object; no field or text was dropped.\n'
    blocks=[intro,'FULL SHARED GUIDE',(ROOT/'docs/mechanics/POISONCRAFTING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8'),'FULL INTERNAL CARDS',(ROOT/'docs/director-only/POISONCRAFTING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8'),'COMPLETE FACTORED OPERATIONAL JSON',compact({'envelope':{k:v for k,v in d.items() if k!='cards'},'common':c,'recipeOverrides':overrides,'deliveryProfiles':delivery_profiles,'conditionProfiles':condition_profiles,'profileBindings':bindings}),'IMMUTABLE SOURCE AND PUBLIC BOOK BINDINGS',compact({'sourceSha256':s['sourceSha256'],'bookSha256':s['bookSha256'],'sourceIndices':s['sourceIndices'],'publicBookBindings':s['publicBookBindings']}),'WORKED BOUNDARY TRACES',(AUDIT/'POISONCRAFTING_REVIEW_CASES.md').read_text(encoding='utf-8'),'VALIDATION REPORT',compact(v)]
    packet='\n\n'.join(blocks);target=AUDIT/'CODEX_POISONCRAFTING_EXACT_REVIEW.txt';target.write_text(packet,encoding='utf-8')
    paths=['docs/mechanics/POISONCRAFTING_RECIPE_PLAYTEST.md','docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md','docs/director-only/POISONCRAFTING_INTERNAL_RECIPE_CARDS.md','data/playtest/poisoncrafting_recipe_candidate.json','data/director/poisoncrafting_recipe_candidate_internal.json']
    record={'status':'prepared, not sent','sourceConferenceTurnId':d['sourceConferenceTurnId'],'classInterfaceTurnId':d['classInterfaceTurnId'],'packetCharacters':len(packet),'packetSha256':sha(target),'losslessOperationalReconstructions':41,'artifactHashes':{str((ROOT/p).relative_to(GAME)).replace('\\','/'):sha(ROOT/p) for p in paths}}
    (AUDIT/'POISONCRAFTING_EXACT_SUBMISSION.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'characters':len(packet),'cards':41,'checks':len(v['checks'])}))
if __name__=='__main__':main()
