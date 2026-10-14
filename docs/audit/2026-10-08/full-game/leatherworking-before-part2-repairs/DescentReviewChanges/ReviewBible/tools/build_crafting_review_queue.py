"""One internal navigation page for reviewed, drafted and source-prepared trades."""
from pathlib import Path
from collections import Counter
import os,json,hashlib
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
OUT=ROOT/'docs/director-only/CRAFTING_REVIEW_QUEUE.md'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(label,p):return '['+label+']('+os.path.relpath(p,OUT.parent).replace('\\','/')+')'
def main():
    source=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json');rs=source['recipes']
    catalog=read(ROOT/'data/director/crafting_recipe_review_catalog.json');by={r['recipeId']:r for r in catalog['recipes']}
    preparations={
      'Leatherworking':('LEATHERWORKING_SOURCE_PREPARATION.json','LEATHERWORKING_SOURCE_DECISIONS.md','LEATHERWORKING_EXACT_PART2_SUBMISSION.json'),
      'Tailoring':('TAILORING_SOURCE_PREPARATION.json','TAILORING_SOURCE_AUDIT.md','TAILORING_SOURCE_PACKET_STATUS.json'),
      'Jewelcrafting':('JEWELCRAFTING_SOURCE_PREPARATION.json','JEWELCRAFTING_SOURCE_AUDIT.md','JEWELCRAFTING_SOURCE_PACKET_STATUS.json'),
      'Fishing':('FISHING_SOURCE_PREPARATION.json','FISHING_SOURCE_AUDIT.md','FISHING_SOURCE_PACKET_STATUS.json'),
      'Mining':('GATHERING_TOOL_SOURCE_PREPARATION.json','GATHERING_TOOL_SOURCE_AUDIT.md',None),
      'Skinning':('GATHERING_TOOL_SOURCE_PREPARATION.json','GATHERING_TOOL_SOURCE_AUDIT.md',None),
      'Salvaging':('GATHERING_TOOL_SOURCE_PREPARATION.json','GATHERING_TOOL_SOURCE_AUDIT.md',None)}
    rows=[];checked_manifests=set();prepared_only=0
    for trade in ['Alchemy','Herbalism','Cooking','Poisoncrafting','Blacksmithing','Leatherworking','Tailoring','Jewelcrafting','Fishing','Mining','Skinning','Salvaging','Enchanting','Rune Carving','Scribing','Tinkering']:
        group=[r for r in rs if r['skill']==trade];n=len(group);reviewed=sum(by[r['id']]['status']=='reviewed-authored-playtest' for r in group);draft=sum(by[r['id']]['status']=='draft-awaiting-GPT-review' for r in group)
        links=[]
        if reviewed:
            assert reviewed==n
            paths={by[r['id']]['reviewManifest'] for r in group};assert len(paths)==1
            p=ROOT/next(iter(paths));m=read(p)
            assert m['status'].startswith('REVIEWED') and m['exactReviewTurnId'] and all(sha(GAME/q)==h for q,h in m['artifactHashes'].items())
            checked_manifests.add(str(p));phase='Exact operational review complete; runtime and human balance separate';next_action='Retain dependencies for later cross-system flow review'
            links=[link('review evidence',p),link('public cards',ROOT/next(by[r['id']]['cardFile'] for r in group if r['visibility']=='public'))]
        elif trade in preparations:
            original,notes,status=preparations[trade];e=read(AUDIT/original)
            assert [r for r in e['recipes'] if r['skill']==trade]==group
            links=[link('source decisions' if trade=='Leatherworking' else 'source audit',AUDIT/notes)]
            if status:links.append(link('packet state',AUDIT/status))
            if trade=='Leatherworking':
                assert draft==44
                phase='Source direction complete; 44 exact cards submitted, verdict pending'
                next_action='Retrieve actual Part B verdict; apply required edits and validate before promotion'
                links.append(link('draft public cards',ROOT/'docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md'))
            else:
                prepared_only+=n
                phase='Complete source evidence prepared; not sent' if status else 'Complete source audit; questions prepared, not sent'
                next_action='Confer with GPT using current reviewed rules, then author and review exact cards'
        else:
            phase='Catalog/source fields inventoried; individual operational pass open'
            next_action='Prepare complete trade-specific sources and interfaces for GPT'
            links=[link('catalog-wide numeric audit',AUDIT/'CRAFTING_EFFECT_FIELD_AUDIT.md')]
        rows.append({'trade':trade,'total':n,'public':sum(r['visibility']=='public' for r in group),'reviewed':reviewed,'draft':draft,'phase':phase,'nextAction':next_action,'links':links})
    assert len(checked_manifests)==5 and sum(x['total'] for x in rows)==687 and sum(x['reviewed'] for x in rows)==218 and sum(x['draft'] for x in rows)==44 and prepared_only==258
    text=['# Crafting review queue — internal navigation','',
      'This is the current operational-manuscript pass, not a replacement for historical source approvals. It includes counts of restricted/Director-only work and belongs in the internal review route. All original source information remains preserved.','',
      '**218 of 687 recipes reviewed; 469 remain.** Of the remaining recipes,44 have authored drafts in exact review;258 more have complete trade-specific source evidence/audits prepared;167 still need that individual trade preparation. Public operational reviews remain138 of433. Source preparation is not effect approval.','',
      'The active joint request is Leatherworking exact Part B in **Calibration Review Part 2**, turn `2a3db078-0ab3-411a-a9d2-aeb19da8765e`. Both parts were sent once; Part A has a completed receipt. The latest checked live state is active with no completed Part B reply. Check the live chat before sending anything; do not infer a result from this saved page.','',
      '| Trade | Total / public | Reviewed | Drafts | Current phase | Evidence |','|---|---:|---:|---:|---|---|']
    for row in rows:text.append(f"| {row['trade']} | {row['total']} / {row['public']} | {row['reviewed']} | {row['draft']} | {row['phase']} | {'; '.join(row['links'])} |")
    text+=['','## Next work and preserved boundaries','',
      'After Leatherworking has an actual exact verdict and its required edits pass validation, prepare the Tailoring conference using the resulting rules. Jewelcrafting and Fishing have complete unsent source packets. Mining/Skinning/Salvaging share a completed source audit with25 unresolved yield omissions and the existing finite-harvest/dismantling boundaries; their complete body/quality/recovery decisions still need a conference.','',
      'The Fishing audit preserves three historical Fishing Boat-to-Tackle names for the transport review. The gathering-tool audit preserves213 reusable tool occurrences,12 explicitly consumed tool occurrences and10 catalysts. Neither legacy names nor component role names silently replace current effects or consumption flags.','',
      'Human playtesting, numerical balance, ingredient availability, runtime parity and final whole-game flow remain open. No historical source is deleted without both audit and GPT confirmation. The authorized GitHub push follows the final joint flow review; careful cosmology review follows a successful push and verification of the remote commit.','']
    OUT.write_text('\n'.join(text),encoding='utf-8',newline='\n')
    result={'status':'PASS','trades':16,'totalRecipes':687,'reviewed':218,'remaining':469,'draftAwaitingExactReview':44,'otherSourcePrepared':258,'otherTradePreparationOpen':167,'verifiedReviewedManifests':5,'rows':rows,'scope':'navigation and source accounting only; no new approval'}
    (AUDIT/'CRAFTING_REVIEW_QUEUE_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
if __name__=='__main__':main()
