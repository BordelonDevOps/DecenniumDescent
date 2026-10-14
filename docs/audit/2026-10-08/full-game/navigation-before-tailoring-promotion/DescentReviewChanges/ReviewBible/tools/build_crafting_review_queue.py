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
      'Tailoring':('TAILORING_SOURCE_PREPARATION.json','GPT_TAILORING_SOURCE_CONFERENCE.md','TAILORING_EXACT_PART2_SUBMISSION.json'),
      'Jewelcrafting':('JEWELCRAFTING_SOURCE_PREPARATION.json','JEWELCRAFTING_SOURCE_AUDIT.md','JEWELCRAFTING_SOURCE_PACKET_STATUS.json'),
      'Fishing':('FISHING_SOURCE_PREPARATION.json','FISHING_SOURCE_AUDIT.md','FISHING_SOURCE_PACKET_STATUS.json'),
      'Mining':('GATHERING_TOOL_SOURCE_PREPARATION.json','GATHERING_TOOL_SOURCE_AUDIT.md','GATHERING_TOOL_SOURCE_PACKET_STATUS.json'),
      'Skinning':('GATHERING_TOOL_SOURCE_PREPARATION.json','GATHERING_TOOL_SOURCE_AUDIT.md','GATHERING_TOOL_SOURCE_PACKET_STATUS.json'),
      'Salvaging':('GATHERING_TOOL_SOURCE_PREPARATION.json','GATHERING_TOOL_SOURCE_AUDIT.md','GATHERING_TOOL_SOURCE_PACKET_STATUS.json'),
      'Enchanting':('ADVANCED_CRAFT_SOURCE_PREPARATION.json','ADVANCED_CRAFT_SOURCE_AUDIT.md','ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json'),
      'Rune Carving':('ADVANCED_CRAFT_SOURCE_PREPARATION.json','ADVANCED_CRAFT_SOURCE_AUDIT.md','ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json'),
      'Scribing':('ADVANCED_CRAFT_SOURCE_PREPARATION.json','ADVANCED_CRAFT_SOURCE_AUDIT.md','ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json'),
      'Tinkering':('ADVANCED_CRAFT_SOURCE_PREPARATION.json','ADVANCED_CRAFT_SOURCE_AUDIT.md','ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json')}
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
            if trade=='Tailoring':
                assert draft==43
                phase=read(AUDIT/status)['status']
                next_action='Obtain actual exact-card verdict, apply finite repairs and validate before promotion'
                links.append(link('draft public cards',ROOT/'docs/mechanics/TAILORING_PUBLIC_RECIPE_CARDS.md'))
            elif trade=='Leatherworking':
                assert draft==44
                phase='Source direction complete; 44 exact cards submitted, verdict pending'
                next_action='Retrieve actual Part B verdict; apply required edits and validate before promotion'
                links.append(link('draft public cards',ROOT/'docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md'))
            else:
                prepared_only+=n
                phase='Complete source evidence prepared; not sent' if status else 'Complete source audit; questions prepared, not sent'
                next_action='Confer with GPT using current reviewed rules, then author and review exact cards'
                if trade=='Tailoring':
                    phase=read(AUDIT/status)['status']
        else:
            phase='Catalog/source fields inventoried; individual operational pass open'
            next_action='Prepare complete trade-specific sources and interfaces for GPT'
            links=[link('catalog-wide numeric audit',AUDIT/'CRAFTING_EFFECT_FIELD_AUDIT.md')]
        rows.append({'trade':trade,'total':n,'public':sum(r['visibility']=='public' for r in group),'reviewed':reviewed,'draft':draft,'phase':phase,'nextAction':next_action,'links':links})
    assert len(checked_manifests)==6 and sum(x['total'] for x in rows)==687 and sum(x['reviewed'] for x in rows)==262 and sum(x['draft'] for x in rows)==43 and prepared_only==382
    text=['# Crafting review queue â€” internal navigation','',
      'This is the current operational-manuscript pass, not a replacement for historical source approvals. It includes counts of restricted/Director-only work and belongs in the internal review route. All original source information remains preserved.','',
      '**262 of 687 recipes reviewed; 425 remain.** All425 remaining recipes now have complete trade-specific source evidence and prepared conference material. Tailoring has43 authored drafts awaiting exact review; the other382 remaining formulas have source preparation. Public operational reviews are168 of433. Source preparation is not effect approval; each remaining trade needs joint decisions,complete operational cards and exact review.','',
      'Leatherworking exact review is complete: both finite evidence repairs passed91 checks and52 worked cases. Tailoring has completed source directions and43 exact drafts in the joint review in **Calibration Review Part 2**; its packet state below records actual dispatch/receipt status. Check the live chat before sending anything; do not infer a result from this saved page.','',
      '| Trade | Total / public | Reviewed | Drafts | Current phase | Evidence |','|---|---:|---:|---:|---|---|']
    for row in rows:text.append(f"| {row['trade']} | {row['total']} / {row['public']} | {row['reviewed']} | {row['draft']} | {row['phase']} | {'; '.join(row['links'])} |")
    text+=['','## Next work and preserved boundaries','',
      'Complete the exact review of all43 Tailoring cards and apply any finite repairs before promotion. Jewelcrafting and Fishing have complete unsent source packets. Mining/Skinning/Salvaging have a four-part source packet with32 unresolved cases,25 yield omissions and the existing finite-harvest/dismantling boundaries. All three use non-artisan credentials; the binary ordinary dismantling rule needs an explicit interface for source critical-success effects. No new decisions are inferred from preparation.','',
      'The Fishing audit preserves three historical Fishing Boat-to-Tackle names for the transport review. The gathering-tool audit preserves213 reusable tool occurrences,12 explicitly consumed tool occurrences and10 catalysts. Neither legacy names nor component role names silently replace current effects or consumption flags.','',
      'Enchanting,Rune Carving,Scribing andTinkering now have167 complete source records,100 book bindings and50 unresolved cases in five unsent parts. The source comparison preserves21 Rune tool-list andeight component-name differences against each of two older versions.22 Scribing use-count questions,18 incomplete automaton attack profiles andfive distinct custom effects remain undecided.','',
      'A separate '+link('crafting/feat interface audit',AUDIT/'CRAFTING_FEAT_INTERFACE_AUDIT.md')+' prepares24 pending feats affecting creation time,quality,repair,research,languages,trap/fortification rules andprices. These are part of the327 pending full-feat reviews,not additional recipe approvals. The eight previously reviewed feats remain unchanged.','',
      'The '+link('Tinker class/device interface audit',AUDIT/'TINKER_DEVICE_INTERFACE_AUDIT.md')+' preserves48 complete class cards,8 engine paragraphs and210 source lines against43 pending Tinkering recipes;18 interface cases remain for joint review.','',
      'Human playtesting, numerical balance, ingredient availability, runtime parity and final whole-game flow remain open. No historical source is deleted without both audit and GPT confirmation. The authorized GitHub push follows the final joint flow review; careful cosmology review follows a successful push and verification of the remote commit.','']
    OUT.write_text('\n'.join(text),encoding='utf-8',newline='\n')
    result={'status':'PASS','trades':16,'totalRecipes':687,'reviewed':262,'remaining':425,'draftAwaitingExactReview':43,'otherSourcePrepared':382,'otherTradePreparationOpen':0,'verifiedReviewedManifests':6,'rows':rows,'scope':'navigation and source accounting only; no new approval'}
    (AUDIT/'CRAFTING_REVIEW_QUEUE_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
if __name__=='__main__':main()
