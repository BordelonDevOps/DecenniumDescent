"""Prepare complete Jewelcrafting evidence without interrupting the active review."""
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
    target=AUDIT/'CODEX_JEWELCRAFTING_SOURCE_EVIDENCE_PREPARED.txt';statusfile=AUDIT/'JEWELCRAFTING_SOURCE_PACKET_STATUS.json'
    assert not target.exists() and not statusfile.exists(),'Preserve existing preparation.'
    e=read(AUDIT/'JEWELCRAFTING_SOURCE_PREPARATION.json');v=read(AUDIT/'JEWELCRAFTING_SOURCE_VERSION_AUDIT.json')
    srcpath=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';source=read(srcpath);rs=[r for r in source['recipes'] if r['skill']=='Jewelcrafting']
    assert len(rs)==43 and rs==e['recipes'] and sha(srcpath)==e['sourceSha256']
    shared=common(rs);diff={r['id']:delta(r,shared) for r in rs};assert all(merge(shared,diff[r['id']])==r for r in rs)
    eqpath=ROOT/'data/playtest/equipment_acquisition_candidate.json';eq={z['id']:z for z in read(eqpath)['items']}
    assert sha(eqpath)==e['equipmentSha256'] and all(eq[z['id']]==z for z in e['completeEquipmentReferenceRecords'])
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';assert sha(book)==e['bookSha256']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    assert len(e['publicBookBindings'])==26 and all(ps[p['index']]==p['text'] for b in e['publicBookBindings'] for p in b['paragraphs'])
    assert all(sha(GAME/v['sourcePaths'][k])==h for k,h in v['sourceHashes'].items())
    version={k:z for k,z in v.items() if k!='comparisons'}
    version['comparisonRule']='Compare each listed field of each available identity against mechanicalV4. Every comparison is equal except the complete differences array; missing restricted/Director identities on the public runtime route are intentional.'
    intro='''PREPARED JEWELCRAFTING SOURCE EVIDENCE — NOT SENT.

All43 original records,26 exact V5 public bindings,10 complete equipment reference records,11 consumed catalyst occurrences,1,120 source-field comparisons and24 unresolved scenarios are preserved below. These references are not an approved jewelry-body whitelist. No charge, dawn, slot, body, quality or repair decision has been approved.

Before sending, supply actual current reviewed crafting, equipment, body, roll/control and item-bonus rules, plus actual completed Leatherworking/Tailoring decisions. Leatherworking exact review is currently active; do not interrupt it or treat an unfinished verdict as settled. This is preparation only, not a new message to GPT. Cosmology remains strictly after the successful authorized GitHub push and verification of the remote commit.

Lossless source format: recursively merge COMMON and the complete per-ID override; arrays/scalars replace. Every reconstructed original equals its saved source exactly, including nulls, legacy, status, access, optional guidance, all material occurrences and source quality labels. Those labels do not override the reviewed framework's structural-HP-only default. A replacement charge improvement needs precise separate review.
'''
    blocks=[intro,(AUDIT/'JEWELCRAFTING_SOURCE_AUDIT.md').read_text(encoding='utf-8'),
      'COMPLETE SOURCE RECORDS',compact({'sourceSha256':e['sourceSha256'],'sourceIndices':e['sourceIndices'],'COMMON':shared,'recipeOverrides':diff}),
      'EXACT SOURCE/BOOK AUDIT',compact({k:e[k] for k in ('bookSha256','counts','families','operativeTags','publicBookBindings','structuralAudit','componentOccurrences','componentRoleCounts','catalystOccurrences','checks')}),
      'COMPLETE EQUIPMENT REFERENCES — NOT A BINDING WHITELIST',compact({'equipmentSha256':e['equipmentSha256'],'scope':e['equipmentReferenceScope'],'items':e['completeEquipmentReferenceRecords'],'excludedNameSearchMatches':e['excludedNameSearchMatches']}),
      'SOURCE VERSION COMPARISON AND ALL CATALYST ROWS',compact(version),
      'UNRESOLVED24 SCENARIOS',(AUDIT/'JEWELCRAFTING_REVIEW_SCENARIOS.md').read_text(encoding='utf-8')]
    text='\n\n'.join(blocks);create(target,text)
    baseline=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json');assert all(sha(GAME/p)==h for p,h in baseline['files'].items())
    status={'status':'Prepared source evidence only; not sent; needs current reviewed-rule cover and actual preceding trade decisions','packetFile':target.name,'packetSha256':sha(target),'characters':len(text),'sourceRecipes':43,'losslessReconstructions':43,'publicBookBindings':26,'completeEquipmentReferenceRecords':10,'catalystOccurrences':11,'reviewScenarios':24,'sourceFieldComparisons':1120,'sourceAuditChecks':len(e['checks']),'versionChecks':len(v['checks']),'protectedFilesUnchanged':len(baseline['files']),'sourceInformationDeleted':0,'recipesApproved':0,'currentReviewedTotal':218,'currentAuthoredDrafts':44,'currentGPTDependency':'Leatherworking44 exact-card review in Calibration Review Part2, both parts sent; final verdict pending','cosmology':'After successful authorized GitHub push and verified remote commit only.'}
    create(statusfile,json.dumps(status,ensure_ascii=False,indent=2)+'\n');print(compact(status))
if __name__=='__main__':main()
