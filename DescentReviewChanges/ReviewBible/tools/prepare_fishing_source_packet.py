"""Prepare lossless Fishing sources and unresolved procedures; never sends."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as E
from prepare_cooking_exact_review import common,delta,merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    target=AUDIT/'CODEX_FISHING_SOURCE_EVIDENCE_PREPARED.txt';status_path=AUDIT/'FISHING_SOURCE_PACKET_STATUS.json'
    assert not target.exists() and not status_path.exists(),'Existing preparation is preserved.'
    evidence=read(AUDIT/'FISHING_SOURCE_PREPARATION.json');source_path=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    source=read(source_path);rs=[r for r in source['recipes'] if r['skill']=='Fishing']
    assert len(rs)==44 and rs==evidence['recipes'] and sha(source_path)==evidence['sourceSha256']
    shared=common(rs);overrides={r['id']:delta(r,shared) for r in rs};assert all(merge(shared,overrides[r['id']])==r for r in rs)
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';assert sha(book)==evidence['bookSha256']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    assert len(evidence['publicBookBindings'])==28 and all(ps[p['index']]==p['text'] for b in evidence['publicBookBindings'] for p in b['paragraphs'])
    eqpath=ROOT/'data/playtest/equipment_acquisition_candidate.json';eq={r['id']:r for r in read(eqpath)['items']}
    assert sha(eqpath)==evidence['equipmentSha256'] and all(eq[r['id']]==r for r in evidence['completeEquipmentReferenceRecords'])
    version={k:v for k,v in evidence['versionAudit'].items() if k!='comparisons'}
    assert all(sha(GAME/version['sourcePaths'][k])==h for k,h in version['sourceHashes'].items())
    version['comparisonRule']='Every listed field of every available identity compared against mechanicalV4. All match except the complete differences array; missing gated publicRuntime identities remain intentional.'
    boundary=[]
    for file,needle in [('docs/mechanics/CRAFTING_TRADE_REFERENCE.md','Existing equipment supplies its actual price'),('docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md','The extraction lead selects a compatible gathering trade')]:
        p=ROOT/file;paras=p.read_text(encoding='utf-8').split('\n\n');matches=[s for s in paras if s.startswith(needle)];assert len(matches)==1
        boundary.append({'file':p.relative_to(GAME).as_posix(),'sha256':sha(p),'exactParagraph':matches[0],'scope':'Existing reviewed boundary, not a newly authored Fishing catch rule.'})
    oldboats=[{'recipeId':r['id'],'currentName':r['name'],'currentFamily':r['recipeFamily'],'currentEffect':r['effects'],'legacyName':r['legacyName'],'legacyEffect':r.get('legacyEffect')} for r in rs if 'boat' in r.get('legacyName','').lower()];assert {x['recipeId'] for x in oldboats}=={'recipe-172','recipe-173','recipe-177'}
    cross=read(AUDIT/'BESTIARY_CRAFTING_CROSSLINK_AUDIT.json');links=[r for r in cross['printedRecipeReferences'] if 'recipe-173' in r.get('recipeIds',[])];assert len(links)==1
    assert sha(GAME/links[0]['sourcePath'])==links[0]['sourceSha256']
    scope='''PREPARED FISHING SOURCE EVIDENCE — NOT SENT.

This preserves44 complete current formulas,28 exact public V5 bindings,212 consumed component occurrences,nine equipment references,24 unresolved scenarios and1,160 source-field comparisons. It includes three legacy Fishing Boat-to-Tackle name transitions and the literal Sporefolk Adult reference to recipe-173; neither source relationship establishes availability, a free boat or a finished fishing/transport rule.

Existing reviewed authority: Fishing uses WIS and Fishing tackle is explicitly a non-artisan tool proficiency. It may support compatible aquatic harvesting under the shared extraction framework. None of that supplies an unwritten catching, attraction or extra-yield procedure. Full current governing guides and actual preceding trade decisions must accompany a future conference. Leatherworking's exact review is active now; this preparation is not sent and must not interrupt it.

Every original recipe is preserved losslessly as COMMON recursively merged with its complete per-ID override. Dictionary fields merge; arrays/scalars replace, and nulls stay real values. Source status, legacy/current names/effects, source access, work, exact ingredients and optional guidance remain intact. The full reconstructed originals equal the authoritative records locally; do not attribute these local checks to GPT. Missing V2 visibility cannot make current gated recipes public. No new effects, available creatures, ingredient supply, runtime behavior or cosmology are approved here.
'''
    blocks=[scope,(AUDIT/'FISHING_SOURCE_AUDIT.md').read_text(encoding='utf-8'),
      'COMPLETE ORIGINAL SOURCE RECORDS',compact({'sourceSha256':evidence['sourceSha256'],'sourceIndices':evidence['sourceIndices'],'COMMON':shared,'recipeOverrides':overrides}),
      'PUBLIC BOOK BINDINGS AND EXACT SOURCE AUDIT',compact({k:evidence[k] for k in ('bookSha256','counts','families','tags','publicBookBindings','structuralAudit','componentOccurrences','componentRoleCounts','fieldFlagCounts','checks')}),
      'EXISTING EQUIPMENT REFERENCES — NO OUTPUT BINDING IMPLIED',compact({k:evidence[k] for k in ('equipmentSha256','completeEquipmentReferenceRecords','equipmentReferenceScope','excludedNameSearchMatches')}),
      'COMPLETE SOURCE-VARIANT DIFFERENCES',compact(version),
      'EXACT REVIEWED NON-ARTISAN AND HARVEST BOUNDARIES',compact(boundary),
      'PRESERVED LEGACY BOAT TRANSITIONS AND BESTIARY REFERENCE',compact({'legacyBoatTransitions':oldboats,'literalBestiaryLink':links,'interpretation':'Current and legacy records retained; current Tackle is not silently a boat. The printed bestiary reference is not a complete availability/harvest/crafting binding.'}),
      '24 UNRESOLVED CONCRETE SCENARIOS',(AUDIT/'FISHING_REVIEW_SCENARIOS.md').read_text(encoding='utf-8')]
    packet='\n\n'.join(blocks);create(target,packet)
    protected=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files'];assert all(sha(GAME/p)==h for p,h in protected.items())
    d={'status':'Prepared only; not sent; needs reviewed-rule cover and actual preceding-trade decisions','packetFile':target.name,'packetSha256':sha(target),'characters':len(packet),'sourceRecipes':44,'losslessReconstructions':44,'publicBookBindings':28,'components':212,'equipmentReferences':9,'reviewScenarios':24,'sourceFieldComparisons':1160,'checks':17,'legacyBoatTransitions':3,'literalBestiaryLinks':1,'protectedFilesUnchanged':42,'sourceInformationDeleted':0,'recipesApproved':0,'cosmology':'After successful authorized push and verified remote commit only.'}
    create(status_path,json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(compact(d))
if __name__=='__main__':main()
