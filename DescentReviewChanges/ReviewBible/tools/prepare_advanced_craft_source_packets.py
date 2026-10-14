"""Prepare complete four-trade sources and shared questions; no dispatch or approval."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,re,zipfile,xml.etree.ElementTree as E
from prepare_cooking_exact_review import common,delta,merge
from prepare_advanced_craft_source_audit import leafdiff
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(d):return json.dumps(d,ensure_ascii=False,separators=(',',':'))
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def restore_field(current,changes):
    out=deepcopy(current)
    for c in changes:
        parts=c['path'].strip('/').split('/');cursor=out
        for key in parts[:-1]:cursor=cursor[int(key)] if isinstance(cursor,list) else cursor[key]
        key=int(parts[-1]) if isinstance(cursor,list) else parts[-1];assert cursor[key]==c['current'];cursor[key]=c['other']
    return out
def main():
    status_path=AUDIT/'ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json';assert not status_path.exists()
    e=read(AUDIT/'ADVANCED_CRAFT_SOURCE_PREPARATION.json');src=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';rs=[r for r in read(src)['recipes'] if r['skill'] in e['trades']]
    assert len(rs)==167 and rs==e['recipes'] and sha(src)==e['sourceSha256'] and all(c['pass'] for c in e['checks']);by={r['id']:r for r in rs}
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';assert sha(book)==e['bookSha256']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    assert len(e['publicBookBindings'])==100 and all(ps[p['index']]==p['text'] for b in e['publicBookBindings'] for p in b['paragraphs'])
    version=e['versionAudit'];assert all(sha(GAME/version['sourcePaths'][k])==h for k,h in version['sourceHashes'].items())
    # Losslessly encode every differing selected historical field using current records.
    encoded=[]
    for d in version['differences']:
        if not d['otherFieldPresent']:encoded.append({'recipeId':d['recipeId'],'version':d['version'],'field':d['field'],'otherFieldAbsent':True});continue
        changes=sorted(leafdiff(d['currentValue'],d['otherValue']),key=lambda c:c['path'])
        assert restore_field(by[d['recipeId']][d['field']],changes)==d['otherValue']
        encoded.append({'recipeId':d['recipeId'],'version':d['version'],'field':d['field'],'changesFromCurrentField':changes})
    assert len(encoded)==225 and sum('changesFromCurrentField' in r for r in encoded)==58
    toolbook_bindings=[b for b in e['publicBookBindings'] if b['recipeId'] in e['sourceNameCorrespondences']['uniqueAffectedRecipes']]
    assert len(toolbook_bindings)==21 and all('Resonance lens' in next(p['text'] for p in b['paragraphs'] if p['text'].startswith('Work.')) for b in toolbook_bindings)
    component_name_ids={d['recipeId'] for d in e['sourceNameCorrespondences']['leafDifferences'] if d['path'].startswith('/components')}
    assert len(component_name_ids)==8 and all('Resonance Lens' in next(p['text'] for p in b['paragraphs'] if p['text'].startswith('Components.')) for b in toolbook_bindings if b['recipeId'] in component_name_ids)
    engine_path=GAME/e['reviewedTradeBindings']['file'];assert sha(engine_path)==e['reviewedTradeBindings']['sha256'];engine=read(engine_path)
    kits=[r for r in engine['newToolProfiles'] if r['name'] in {t['primaryTool'] for t in e['reviewedTradeBindings']['trades']}];assert len(kits)==2
    eqpath=ROOT/'data/playtest/equipment_acquisition_candidate.json';eq={r['id']:r for r in read(eqpath)['items']}
    ids=['simple-melee-weapons.quarterstaff','arcane-focuses.crystal','arcane-focuses.rod','arcane-focuses.staff','arcane-focuses.wand','adventuring-gear.book','adventuring-gear.case-map-or-scroll','adventuring-gear.ink-1-ounce-bottle','adventuring-gear.ink-pen','adventuring-gear.paper-one-sheet','adventuring-gear.parchment-one-sheet','adventuring-gear.ram-portable','adventuring-gear.sealing-wax','adventuring-gear.spellbook','tools.calligrapher-s-supplies','tools.tinker-s-tools'];equipment=[eq[id] for id in ids];assert len(equipment)==16
    scenarios=(AUDIT/'ADVANCED_CRAFT_REVIEW_SCENARIOS.md').read_text(encoding='utf-8');assert len(set(re.findall(r'(?:AC|EN|RC|SC|TI)-\d\d',scenarios)))==50
    occurrences={key:[{k:v for k,v in r.items() if k!='sourceComponent'} for r in e[key]] for key in ['reusableToolOccurrences','consumedToolOccurrences','catalystOccurrences']}
    for key,rows in occurrences.items():
        for ref,original in zip(rows,e[key]):assert by[ref['recipeId']]['components'][ref['componentIndex']]==original['sourceComponent']
    cover='''PREPARED ADVANCED-CRAFT SOURCE EVIDENCE — FIVE PARTS, NOT SENT.

This internal set preserves all167 current Enchanting/RuneCarving/Scribing/Tinkering sources,100 actual public-book bindings and50 unresolved cases. Shared interfaces plus one complete part per trade must be combined with current reviewed governing rules before any future conference. Tailoring is currently in source review; do not interrupt or infer its pending decisions. Preparation is not submission or approval. Current counts262/687 reviewed,425remaining,public168/433 are a preparation checkpoint only.

Each current recipe is reconstructed exactly by recursively merging COMMON with its per-ID recipeOverrides; dictionaries merge and arrays/scalars replace, including real nulls. All current/legacy/source-status/access/component/guidance fields remain. Component occurrence references point to components[componentIndex] in that full source.

For the ten selected comparison fields, all current/historical values are equal except the complete225-field difference list. otherFieldAbsent:true preserves an actually missing older field. Otherwise start with the full current recipe[field] and replace only each changesFromCurrentField path with its other value; paths are relative to that field and numeric segments address arrays. These replacements are asserted locally to reconstruct the exact historical field. This is not a claim to reconstruct every unrelated field of each complete older variant; those full original files remain preserved separately.58 field differences are only the existing Rune Focusing/Resonance name correspondences across two older variants, plus167 missingV2 visibility fields.

The charge/use/trigger/service ambiguities,18 incomplete automaton attack profiles,five custom exceptional schemas andone null work-year must be explicitly resolved later. Literal names and target prohibitions touching cosmology remain preserved without interpretation. No source information is deleted, no effect is approved, and no GitHub push or cosmology review is performed by this preparation.
'''
    shared=[cover,(AUDIT/'ADVANCED_CRAFT_SOURCE_AUDIT.md').read_text(encoding='utf-8'),'ALL50 UNRESOLVED SCENARIOS\n'+scenarios,
      'FOUR EXISTING ARTISAN TRADE BINDINGS AND TWO NEW ORDINARY KITS\n'+compact({**e['reviewedTradeBindings'],'kits':kits,'fullTradeGuide':(ROOT/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md').read_text(encoding='utf-8')}),
      'SIXTEEN COMPLETE COMPARATIVE EQUIPMENT REFERENCES\n'+compact({'file':eqpath.relative_to(GAME).as_posix(),'sha256':sha(eqpath),'items':equipment,'scope':'Existing reference bodies only. No automatic magical-output binding,weapon/focus permission or kit duplication. Separate druidic focus and crystal-vial name matches are not proposed outputs.'}),
      'ALL SPECIAL COMPONENT OCCURRENCE REFERENCES\n'+compact(occurrences),
      'EXACT HISTORICAL NAME-CORRESPONDENCE EVIDENCE\n'+compact(e['sourceNameCorrespondences']),
      'COMPLETE SELECTED SOURCE-FIELD DIFFERENCES\n'+compact({k:v for k,v in version.items() if k not in ['comparisons','differences']}|{'encodedDifferences':encoded,'losslessHistoricalFieldReconstructions':58,'absentV2VisibilityFields':167,'publicBookToolNameBindings':21,'publicBookConsumedNameBindings':8}),
      'ALL27 SOURCE AUDIT CHECKS\n'+compact(e['checks'])]
    parts={'SHARED_INTERFACES':'\n\n'.join(shared)}
    for trade in e['trades']:
        group=[r for r in rs if r['skill']==trade];ids={r['id'] for r in group};shared_fields=common(group);overrides={r['id']:delta(r,shared_fields) for r in group};assert all(merge(shared_fields,overrides[r['id']])==r for r in group)
        parts[trade.upper().replace(' ','_')]='\n\n'.join([f'PREPARED {trade.upper()} COMPLETE SOURCE EVIDENCE — NOT SENT. Read with SHARED_INTERFACES and actual current reviewed rules. No source/interface directions or exact-card approval are granted.',
          'ALL CURRENT ORIGINAL RECORDS\n'+compact({'sourceSha256':e['sourceSha256'],'sourceIndices':{id:i for id,i in e['sourceIndices'].items() if id in ids},'COMMON':shared_fields,'recipeOverrides':overrides}),
          'EXACT PUBLIC BOOK BINDINGS\n'+compact({'bookSha256':e['bookSha256'],'bindings':[b for b in e['publicBookBindings'] if b['recipeId'] in ids]}),
          'STRUCTURAL AND NUMERIC EVIDENCE\n'+compact({'summary':e['tradeSummaries'][trade],'structuralAudit':[r for r in e['structuralAudit'] if r['recipeId'] in ids],'numericAuditRecords':[r for r in e['numericAuditReference']['records'] if r['recipeId'] in ids],'scribingUseQuestions':[r for r in e['scribingUseQuestions'] if r['recipeId'] in ids],'customSourceEffects':[r for r in e['customSourceEffects'] if r['recipeId'] in ids],'automatonMissingAttackFields':[r for r in e['automatonMissingAttackFields'] if r['recipeId'] in ids],'sourceHourNulls':[r for r in e['sourceHourNulls'] if r['recipeId'] in ids]})])
    protected=read(AUDIT/'TAILORING_PART2_REVIEW_BASELINE.json')['files'];assert all(sha(GAME/p)==h for p,h in protected.items())
    d={'status':'Prepared complete five-part source evidence; not sent; no effect approval','parts':{},'sourceRecipes':167,'losslessReconstructions':167,'publicBookBindings':100,'families':31,'unresolvedScenarios':50,'sourceAuditChecks':27,'sourceFieldComparisons':4340,'equalFields':4115,'preservedDifferences':225,'losslessHistoricalFieldReconstructions':58,'absentV2VisibilityFields':167,'publicBookToolNameBindings':21,'publicBookConsumedNameBindings':8,'componentOccurrences':758,'reusableToolRows':90,'consumedToolRows':6,'catalysts':172,'completeEquipmentReferences':16,'completeNewKitProfiles':2,'reviewedArtisanTradeBindings':4,'protectedFilesUnchanged':53,'recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'Literal source restrictions preserved; no interpretation; review strictly after successful authorized push and verified remote commit.'}
    for label,s in parts.items():
        p=AUDIT/f'CODEX_ADVANCED_CRAFT_{label}_PREPARED.txt';create(p,s);d['parts'][label]={'file':p.name,'characters':len(s),'sha256':sha(p),'sent':False}
    create(status_path,json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(compact(d))
if __name__=='__main__':main()
