"""Build lossless Tailoring source evidence; defer sending until current review finishes."""
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as E
from prepare_cooking_exact_review import common,delta,merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    packet_path=AUDIT/'CODEX_TAILORING_SOURCE_EVIDENCE_PREPARED.txt';status_path=AUDIT/'TAILORING_SOURCE_PACKET_STATUS.json'
    assert not packet_path.exists() and not status_path.exists(),'Inspect preserved preparation rather than overwrite.'
    evidence=read(AUDIT/'TAILORING_SOURCE_PREPARATION.json');version=read(AUDIT/'TAILORING_SOURCE_VERSION_AUDIT.json')
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';src=read(source);rs=[r for r in src['recipes'] if r['skill']=='Tailoring']
    assert rs==evidence['recipes'] and len(rs)==43 and sha(source)==evidence['sourceSha256']
    base=common(rs);overrides={r['id']:delta(r,base) for r in rs};assert all(merge(base,overrides[r['id']])==r for r in rs)
    equipment=ROOT/'data/playtest/equipment_acquisition_candidate.json';eq={r['id']:r for r in read(equipment)['items']}
    assert sha(equipment)==evidence['equipmentSha256'] and all(eq[r['id']]==r for r in evidence['completeEquipmentReferenceRecords'])
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';assert sha(book)==evidence['bookSha256']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    assert all(ps[p['index']]==p['text'] for b in evidence['publicBookBindings'] for p in b['paragraphs'])
    assert all(sha(GAME/version['sourcePaths'][k])==h for k,h in version['sourceHashes'].items())
    source_version={k:v for k,v in version.items() if k!='comparisons'}
    # Full current records are present, with no source field dropped. Repeated
    # equality rows are replaced by the exact compared-field list and counts.
    source_version['comparedFields']=['name','effects','mechanics','quantity','components','workRequirements','craftingCheck','economy','visibility','discovery']
    source_version['comparisonMatrixRule']='Compare each named field of each available identity against mechanicalV4; all field comparisons are equal except the complete differences array. Missing gated publicRuntime identities are intentionally excluded from that route.'
    source_version['localEvidenceOnly']='File comparisons were executed locally by Codex; GPT has not independently accessed those files.'
    intro='PREPARED TAILORING SOURCE EVIDENCE — NOT YET SENT.\n\nThis contains all43 original Tailoring records, all29 exact public V5 paragraph bindings,20 complete existing equipment references, the actual source-version comparison and20 unresolved scenarios. No Tailoring operational card is approved. Before sending, attach the current reviewed body/carrying, crafting, equipment and Blacksmithing guides plus the actual completed Leatherworking decisions. The ongoing Leatherworking request must not be treated as a completed decision. Update the cover/status from actual evidence at send time; do not replace or erase this preserved preparation.\n\nLOSSLESS SOURCE FORMAT: expand COMMON with each recipeOverride recursively; arrays replace complete arrays. Reconstruction is exactly equal to every original recipe, including source status, needsReview, current and legacy effects, components and optional guidance. No access field or ingredient is silently omitted. Source hashes and indices identify the original authoritative records. The version-comparison evidence reports local checks; it is not another GPT approval.\n\n'
    blocks=[intro,(AUDIT/'TAILORING_SOURCE_AUDIT.md').read_text(encoding='utf-8'),
      '\nCOMPLETE ORIGINAL RECIPES — COMMON PLUS RECURSIVE OVERRIDES\n',compact({'sourceSha256':evidence['sourceSha256'],'sourceIndices':evidence['sourceIndices'],'COMMON':base,'recipeOverrides':overrides}),
      '\nEXACT PUBLIC BOOK PARAGRAPHS AND STRUCTURAL AUDIT\n',compact({k:evidence[k] for k in ('bookSha256','counts','effectTypes','families','publicBookBindings','structuralAudit','componentOccurrences','sourceComponentRoles','checks')}),
      '\nCOMPLETE EXISTING EQUIPMENT REFERENCE RECORDS\n',compact({'equipmentSha256':evidence['equipmentSha256'],'items':evidence['completeEquipmentReferenceRecords']}),
      '\nSOURCE VERSION COMPARISON AND ALL25 REUSABLE TOOL OCCURRENCES\n',compact(source_version),
      '\nUNRESOLVED CONCRETE SCENARIOS\n',(AUDIT/'TAILORING_REVIEW_SCENARIOS.md').read_text(encoding='utf-8')]
    packet='\n'.join(blocks);create(packet_path,packet)
    protected=dict(read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files'])
    assert all(sha(GAME/p)==h for p,h in protected.items())
    status={'status':'Prepared source evidence only; not sent; awaits actual Leatherworking decisions and current rule-context cover','packetFile':packet_path.name,'packetSha256':sha(packet_path),'packetCharacters':len(packet),'sourceRecipes':43,'losslessReconstructions':43,'publicBookBindings':29,'completeEquipmentRecords':20,'reviewScenarios':20,'nonconsumedToolOccurrences':25,'sourceFieldComparisons':version['fieldComparisons'],'sourceAuditChecks':len(evidence['checks']),'sourceVersionChecks':len(version['checks']),'protectedFilesUnchanged':len(protected),'sourceInformationDeleted':0,'recipesApproved':0,'currentGPTDependency':{'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','turnId':'86413ad7-8096-4e6f-baca-3cab34aa66a3','scope':'Leatherworking source/interface conference; response pending at preparation'},'cosmology':'After authorized successful GitHub push and verified remote commit only.'}
    create(status_path,json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(compact(status))
if __name__=='__main__':main()
