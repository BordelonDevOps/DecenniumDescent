"""Lossless gathering-tool source packets and unresolved cases; prepares but never sends."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as E,re
from prepare_cooking_exact_review import common,delta,merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(d):return json.dumps(d,ensure_ascii=False,separators=(',',':'))
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    status_path=AUDIT/'GATHERING_TOOL_SOURCE_PACKET_STATUS.json';assert not status_path.exists()
    e=read(AUDIT/'GATHERING_TOOL_SOURCE_PREPARATION.json');src=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    rs=[r for r in read(src)['recipes'] if r['skill'] in e['trades']]
    assert rs==e['recipes'] and len(rs)==128 and sha(src)==e['sourceSha256'] and all(c['pass'] for c in e['checks'])
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';assert sha(book)==e['bookSha256']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    assert len(e['publicBookBindings'])==82 and all(ps[p['index']]==p['text'] for b in e['publicBookBindings'] for p in b['paragraphs'])
    for b in e['reviewedBoundaryEvidence']:assert sha(GAME/b['file'])==b['sha256'] and b['exactParagraph'] in (GAME/b['file']).read_text(encoding='utf-8')
    version={k:v for k,v in e['versionAudit'].items() if k!='comparisons'}
    assert all(sha(GAME/version['sourcePaths'][k])==h for k,h in version['sourceHashes'].items())
    eqpath=ROOT/'data/playtest/equipment_acquisition_candidate.json';eq={r['id']:r for r in read(eqpath)['items']}
    ids=['adventuring-gear.pick-miner-s','adventuring-gear.hammer','adventuring-gear.hammer-sledge','adventuring-gear.shovel','new.small-knife','adventuring-gear.magnifying-glass','adventuring-gear.lantern-bullseye','adventuring-gear.lantern-hooded','tools.leatherworker-s-tools','tools.tinker-s-tools']
    equipment=[eq[id] for id in ids]
    enginepath=ROOT/'data/playtest/crafting_engine_candidate.json';engine=read(enginepath)
    trades=[r for r in engine['trades'] if r['name'] in e['trades']];assert len(trades)==3 and all(not r['artisanTool'] for r in trades)
    kits=[r for r in engine['newToolProfiles'] if r['name'] in {t['primaryTool'] for t in trades}];assert len(kits)==3
    scenarios=(AUDIT/'GATHERING_TOOL_REVIEW_SCENARIOS.md').read_text(encoding='utf-8');assert len(set(re.findall(r'GT-\d\d',scenarios)))==32
    # Preserve every occurrence via its exact source record/index, without duplicating the component body.
    occurrences={key:[{k:v for k,v in r.items() if k!='sourceComponent'} for r in e[key]] for key in ['reusableToolOccurrences','consumedToolOccurrences','catalystOccurrences']}
    by={r['id']:r for r in rs}
    for key,records in occurrences.items():
        for ref,original in zip(records,e[key]):assert by[ref['recipeId']]['components'][ref['componentIndex']]==original['sourceComponent']
    shared='''PREPARED GATHERING-TOOL SOURCE EVIDENCE — NOT SENT; NO EFFECT DECISIONS.

Four saved parts form one internal evidence set: shared interfaces plus complete Mining43, Skinning43 and Salvaging42 sources. A future actual conference needs the then-current reviewed governing guides and preceding-trade decisions. Do not send these while another request is active; this preparation itself is not a request, receipt or approval.

The current exact operational pass has262/687 reviewed and425remaining,public168/433. Tailoring source directions are pending. These counts and timing describe preparation only; verify at future dispatch. All128 gathering-tool sources and82 actual public-book bindings are preserved. The25 positive extraYield:1 omissions remain unresolved. The source includes213 reusable tool occurrences,12 consumed tool occurrences and10 real catalysts. No role label silently changes consumption or price.

Existing reviewed credentials for Mining, Skinning and Salvaging are all NON-ARTISAN. Existing ordinary dismantling is binary, while selected source effects refer to critical success; the needed operational bridge remains undecided. The finite harvest manifest and its ordinary critical benefit remain governing evidence. Source tags/family names do not decide physical outputs, donor access or cosmology.

The three source parts each contain COMMON and per-recipe overrides. Recursively merge dictionaries; arrays and scalars replace; nulls remain real. Every current, legacy, source-status, access, ingredient and guidance field is retained and reconstructed exactly against the source locally. Component occurrence references resolve to components[componentIndex] in the named full original recipe. Validation is local source evidence, not a notebook approval.
'''
    blocks=[shared,(AUDIT/'GATHERING_TOOL_SOURCE_AUDIT.md').read_text(encoding='utf-8'),'ALL32 UNRESOLVED CASES\n'+scenarios,
      'EXACT EXISTING HARVEST/DISMANTLING/PRESERVATION BOUNDARIES\n'+compact(e['reviewedBoundaryEvidence']),
      'COMPLETE CURRENT NON-ARTISAN TRADE AND KIT REFERENCES\n'+compact({'source':enginepath.relative_to(GAME).as_posix(),'sha256':sha(enginepath),'trades':trades,'kits':kits,'fullTradeGuide':(ROOT/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md').read_text(encoding='utf-8'),'scope':'Existing ordinary kit profiles, not an automatic binding for all17 magical output families.'}),
      'TEN COMPLETE EQUIPMENT REFERENCES\n'+compact({'source':eqpath.relative_to(GAME).as_posix(),'sha256':sha(eqpath),'items':equipment,'scope':'Comparative ordinary implements only. No family-to-output binding, weapon profile, proficiency grant, duplicate free kit or universal fit permission implied.','excludedWeaponNameMatches':[{'id':id,'name':eq[id]['name']} for id in ['simple-melee-weapons.light-hammer','martial-melee-weapons.war-pick','martial-melee-weapons.warhammer']]}),
      'PRESERVED COMPONENT OCCURRENCE REFERENCES\n'+compact(occurrences),
      'COMPLETE NUMERIC/PROSE OMISSIONS\n'+compact(e['extraYieldOmissions']),
      'FULL VERSION DIFFERENCES AND COMPARISON SUMMARY\n'+compact(version),
      'SOURCE AUDIT CHECKS\n'+compact(e['checks'])]
    parts={'SHARED_INTERFACES':'\n\n'.join(blocks)}
    for trade in e['trades']:
        group=[r for r in rs if r['skill']==trade];common_fields=common(group);overrides={r['id']:delta(r,common_fields) for r in group}
        assert all(merge(common_fields,overrides[r['id']])==r for r in group)
        ids={r['id'] for r in group};bindings=[b for b in e['publicBookBindings'] if b['recipeId'] in ids]
        assert len(bindings)==sum(r['visibility']=='public' for r in group)
        parts[trade.upper()]='\n\n'.join([f'PREPARED {trade.upper()} COMPLETE SOURCE PART — NOT SENT. Read with SHARED_INTERFACES and current reviewed governing guides. No effect is approved here.',
          'ALL ORIGINAL RECORDS LOSSLESSLY FACTORED\n'+compact({'sourceSha256':e['sourceSha256'],'sourceIndices':{id:i for id,i in e['sourceIndices'].items() if id in ids},'COMMON':common_fields,'recipeOverrides':overrides}),
          'EXACT PUBLIC BOOK BINDINGS\n'+compact({'bookSha256':e['bookSha256'],'bindings':bindings}),
          'COMPLETE TRADE STRUCTURAL EVIDENCE\n'+compact({'summary':e['tradeSummaries'][trade],'records':[x for x in e['structuralAudit'] if x['recipeId'] in ids]})])
    protected=read(AUDIT/'TAILORING_PART2_REVIEW_BASELINE.json')['files'];assert all(sha(GAME/p)==h for p,h in protected.items())
    status={'status':'Prepared complete four-part source evidence; not sent; no effect approval','parts':{},'sourceRecipes':128,'losslessReconstructions':128,'publicBookBindings':82,'visibility':e['counts'],'families':17,'unresolvedScenarios':32,'extraYieldOmissions':25,'reusableToolOccurrences':213,'consumedToolOccurrences':12,'catalystOccurrences':10,'completeEquipmentReferences':10,'completeReviewedKitProfiles':3,'nonArtisanTradeBindings':3,'sourceFieldComparisons':3380,'sourceAuditChecks':18,'protectedFilesUnchanged':len(protected),'recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'after successful authorized push and verified remote commit only'}
    for label,s in parts.items():
        p=AUDIT/f'CODEX_GATHERING_TOOL_{label}_PREPARED.txt';create(p,s);status['parts'][label]={'file':p.name,'characters':len(s),'sha256':sha(p),'sent':False}
    create(status_path,json.dumps(status,ensure_ascii=False,indent=2)+'\n');print(compact(status))
if __name__=='__main__':main()
