"""Index this operational review pass without invalidating historical approvals."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';src=read(source)
    by={x['id']:x for x in src['recipes']};authored={};approved=set()
    # Register each completed trade here with its actual manuscript-review manifest.
    batches=[
        ('Alchemy','data/director/alchemy_recipe_candidate_internal.json','docs/mechanics/ALCHEMY_REVIEW_STATUS.json','docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md','docs/director-only/ALCHEMY_INTERNAL_RECIPE_CARDS.md'),
        ('Herbalism','data/director/herbalism_recipe_candidate_internal.json','docs/mechanics/HERBALISM_REVIEW_STATUS.json','docs/mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md','docs/director-only/HERBALISM_INTERNAL_RECIPE_CARDS.md'),
        ('Cooking','data/director/cooking_recipe_candidate_internal.json','docs/mechanics/COOKING_REVIEW_STATUS.json','docs/mechanics/COOKING_PUBLIC_RECIPE_CARDS.md','docs/director-only/COOKING_INTERNAL_RECIPE_CARDS.md'),
        ('Poisoncrafting','data/director/poisoncrafting_recipe_candidate_internal.json','docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json','docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md','docs/director-only/POISONCRAFTING_INTERNAL_RECIPE_CARDS.md'),
        ('Blacksmithing','data/director/blacksmithing_recipe_candidate_internal.json','docs/mechanics/BLACKSMITHING_REVIEW_STATUS.json','docs/mechanics/BLACKSMITHING_PUBLIC_RECIPE_CARDS.md','docs/director-only/BLACKSMITHING_INTERNAL_RECIPE_CARDS.md'),
        ('Leatherworking','data/director/leatherworking_recipe_candidate_internal.json','docs/mechanics/LEATHERWORKING_REVIEW_STATUS.json','docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md','docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md'),
        ('Tailoring','data/director/tailoring_recipe_candidate_internal.json','docs/mechanics/TAILORING_REVIEW_STATUS.json','docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md','docs/director-only/TAILORING_INTERNAL_RECIPE_CARDS.md'),
        ('Jewelcrafting','data/director/jewelcrafting_recipe_candidate_internal.json','docs/mechanics/JEWELCRAFTING_REVIEW_STATUS.json','docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md','docs/director-only/JEWELCRAFTING_INTERNAL_RECIPE_CARDS.md'),
        ('Fishing','data/director/fishing_recipe_candidate_internal.json','docs/mechanics/FISHING_REVIEW_STATUS.json','docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md','docs/director-only/FISHING_INTERNAL_RECIPE_CARDS.md'),
        ('Mining','data/director/gathering_tool_recipe_candidate_internal.json','docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json','docs/mechanics/MINING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/MINING_INTERNAL_RECIPE_CARDS.md'),
        ('Skinning','data/director/gathering_tool_recipe_candidate_internal.json','docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json','docs/mechanics/SKINNING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/SKINNING_INTERNAL_RECIPE_CARDS.md'),
        ('Salvaging','data/director/gathering_tool_recipe_candidate_internal.json','docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json','docs/mechanics/SALVAGING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/SALVAGING_INTERNAL_RECIPE_CARDS.md'),
        ('Enchanting','data/director/advanced_craft_recipe_candidate_internal.json','docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json','docs/mechanics/ENCHANTING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/ENCHANTING_INTERNAL_RECIPE_CARDS.md'),
        ('Rune Carving','data/director/advanced_craft_recipe_candidate_internal.json','docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json','docs/mechanics/RUNE_CARVING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/RUNE_CARVING_INTERNAL_RECIPE_CARDS.md'),
        ('Scribing','data/director/advanced_craft_recipe_candidate_internal.json','docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json','docs/mechanics/SCRIBING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/SCRIBING_INTERNAL_RECIPE_CARDS.md'),
        ('Tinkering','data/director/advanced_craft_recipe_candidate_internal.json','docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json','docs/mechanics/TINKERING_CANDIDATE_RECIPE_CARDS.md','docs/director-only/TINKERING_INTERNAL_RECIPE_CARDS.md'),
    ]
    batch_records=[]
    for name,data_path,review_path,public_path,internal_path in batches:
        dp=ROOT/data_path;rp=ROOT/review_path
        if not dp.exists():continue
        cards=read(dp)['cards'];reviewed=False
        if name in ('Mining','Skinning','Salvaging','Enchanting','Rune Carving','Scribing','Tinkering'):cards=[c for c in cards if c['sourceRecipe']['skill']==name]
        if rp.exists():
            m=read(rp)
            if not m['status'].startswith('REVIEWED'):raise ValueError('Review manifest not final: '+name)
            if not all(sha(GAME/p)==h for p,h in m['artifactHashes'].items()):raise ValueError('Reviewed artifact changed: '+name)
            if not m.get('exactReviewTurnId'):raise ValueError('Missing actual review provenance: '+name)
            reviewed=True
        for c in cards:
            id=c['recipeId']
            if id in authored or id not in by:raise ValueError('Duplicate or unknown identity: '+id)
            if c['visibility']!=by[id]['visibility']:raise ValueError('Source visibility changed: '+id)
            authored[id]={'batch':name,'status':'reviewed-authored-playtest' if reviewed else 'draft-awaiting-GPT-review',
                'cardFile':public_path if c['visibility']=='public' else internal_path,'reviewManifest':review_path if reviewed else None}
            if reviewed:approved.add(id)
        batch_records.append({'batch':name,'authored':len(cards),'reviewed':len(cards) if reviewed else 0,'publicAuthored':sum(c['visibility']=='public' for c in cards)})
    rows=[]
    for r in src['recipes']:
        rows.append({'recipeId':r['id'],'name':r['name'],'trade':r['skill'],'family':r['outputType'],'visibility':r['visibility'],'sourceStatus':r['status'],
            **authored.get(r['id'],{'batch':None,'status':'source-only-unreviewed','cardFile':None,'reviewManifest':None})})
    totals={'sourceRecipes':len(rows),'reviewed':len(approved),'unreviewed':len(rows)-len(approved),'authoredDrafts':len(authored)-len(approved),
        'publicRecipes':sum(x['visibility']=='public' for x in rows),'publicReviewed':sum(x['visibility']=='public' and x['recipeId'] in approved for x in rows)}
    meta={'schemaVersion':1,'sourceSha256':sha(source),'scope':'Current operational manuscript-review pass only, not a count of all previously authored or approved work. Historical source statuses and prior owner approvals remain preserved; they do not by themselves certify these new operational cards, numerical balance or runtime implementation.','batches':batch_records}
    dump(ROOT/'data/director/crafting_recipe_review_catalog.json',{**meta,'visibility':'director-internal','totals':totals,'recipes':rows})
    public=[x for x in rows if x['visibility']=='public']
    dump(ROOT/'data/playtest/crafting_recipe_review_catalog_public.json',{'schemaVersion':1,'sourceSha256':sha(source),'scope':meta['scope'],'visibility':'public','totals':{'sourceRecipes':len(public),'reviewed':totals['publicReviewed'],'unreviewed':len(public)-totals['publicReviewed']},'recipes':public})
    text=['# Crafting recipe review index','',
        f"The public catalog contains {len(public)} existing formulas. **{totals['publicReviewed']} have completed this operational manuscript-review pass; {len(public)-totals['publicReviewed']} remain for this pass.** These counts do not describe all prior authoring or approval. The earlier source books, records and owner-authorized release remain preserved. This pass is separate from the reviewed shared crafting framework.",'',
        'Status labels below apply only to this pass. In particular, source-only-unreviewed means an existing source formula has no completed operational-card review recorded here; it does not mean the formula was never developed or discussed. Earlier developed/developed-provisional labels do not establish approval of a newly expanded card.','',
        'Read [crafting, harvesting and preservation](CRAFTING_HARVEST_PLAYTEST.md) for the shared procedure. Each reviewed effect still requires its actual formula/trade/material access. Review does not certify human balance or live companion implementation. Director-only/restricted formulas remain in the internal catalog.','',
        '| ID | Public formula | Trade | Effect review | Card |','|---|---|---|---|---|']
    for x in public:
        link='â€”' if not x['cardFile'] else '['+('Reviewed' if x['status']=='reviewed-authored-playtest' else 'Draft')+']('+Path(x['cardFile']).name+')'
        text.append(f"| {x['recipeId']} | {x['name']} | {x['trade']} | {x['status']} | {link} |")
    (ROOT/'docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    report={'status':'PASS','totals':totals,'publicIdsExact':{x['recipeId'] for x in public}=={x['id'] for x in src['recipes'] if x['visibility']=='public'},'all687SourceIdsAccounted':len(rows)==len({x['recipeId'] for x in rows})==687,'approvedRequiresManifestAndMatchingHashes':True,'runtimeOrBalanceApprovalInferred':False}
    assert report['publicIdsExact'] and report['all687SourceIdsAccounted']
    dump(AUDIT/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json',report)
    print(json.dumps(report))

if __name__=='__main__':main()
