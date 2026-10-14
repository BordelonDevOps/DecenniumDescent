"""Prepare the complete Blacksmithing source conference without approving recipes."""
from pathlib import Path
import json,hashlib
from prepare_cooking_exact_review import common,delta,merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def main():
    target=AUDIT/'CODEX_BLACKSMITHING_SOURCE_CONFERENCE.txt';assert not target.exists()
    source=read(AUDIT/'BLACKSMITHING_SOURCE_PREPARATION.json');rs=source['recipes'];base=common(rs);overrides={r['id']:delta(r,base) for r in rs}
    assert all(merge(base,overrides[r['id']])==r for r in rs)
    actual=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json');assert rs==[r for r in actual['recipes'] if r['skill']=='Blacksmithing']
    assert len(rs)==43 and len(source['publicBookBindings'])==27 and all(b['effectMatches'] for b in source['publicBookBindings'])
    equipment=read(AUDIT/'BLACKSMITHING_EQUIPMENT_REFERENCE.json')
    blocks=['Codex to Calibration Review: full Blacksmithing source conference.\n', (AUDIT/'BLACKSMITHING_SOURCE_QUESTIONS.md').read_text(encoding='utf-8'),
      '\nCOMPLETE SOURCE RECORDS: reconstruct each by recursive merge of COMMON and its per-recipe override; all 43 equal the original full records exactly. Array values replace whole arrays. No field or component occurrence has been dropped.\n',compact({'sourceSha256':source['sourceSha256'],'bookSha256':source['bookSha256'],'sourceIndices':source['sourceIndices'],'COMMON':base,'recipeOverrides':overrides}),
      '\nEXACT PUBLIC V5 BINDINGS AND STRUCTURAL AUDIT\n',compact({k:source[k] for k in ['counts','effectTypes','publicBookBindings','structuralAudit']}),
      '\nEXISTING REVIEWED EQUIPMENT CATALOG: 57 relevant complete item records; original authority hash and missing standalone profiles.\n',compact({k:v for k,v in equipment.items() if k!='sourcePassages'}),
      '\nFULL REVIEWED CRAFTING FRAMEWORK\n',(ROOT/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md').read_text(encoding='utf-8'),
      '\nFULL REVIEWED EQUIPMENT ACQUISITION, QUALITY, DURABILITY AND REPAIR GUIDE\n',(ROOT/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md').read_text(encoding='utf-8')]
    for filename,lo,hi in [('CLASS_PLAYTEST_RULES.md',1,44),('COMBAT_ACTION_PLAYTEST.md',25,67),('CRAFTING_TRADE_REFERENCE.md',1,26)]:
        lines=(ROOT/'docs/mechanics'/filename).read_text(encoding='utf-8').splitlines();blocks.extend(['\nEXACT EXISTING '+filename+'\n','\n'.join(f'L{i+1}: {lines[i]}' for i in range(lo-1,min(hi,len(lines))))])
    packet='\n'.join(blocks);target.write_text(packet,encoding='utf-8')
    prior=read(AUDIT/'POISONCRAFTING_REVIEW_BASELINE.json')['files'];files=dict(prior)
    poison=read(ROOT/'docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json');files.update(poison['artifactHashes'])
    p=ROOT/'docs/mechanics/POISONCRAFTING_REVIEW_STATUS.json';files[str(p.relative_to(GAME)).replace('\\','/')]=sha(p)
    assert all(sha(GAME/p)==h for p,h in files.items())
    dump(AUDIT/'BLACKSMITHING_REVIEW_BASELINE.json',{'scope':'Original sources and prior reviewed rules, protected before Blacksmithing authoring.','files':files})
    dump(AUDIT/'BLACKSMITHING_SOURCE_CONFERENCE_STATUS.json',{'status':'prepared-not-sent','recipes':43,'publicBookMatches':27,'sourceReconstructions':43,'packetCharacters':len(packet),'packetSha256':sha(target),'protectedFiles':len(files),'recipesApproved':0,'currentReviewedRecipes':175,'currentRemainingRecipes':512,'cosmology':'post-push only'})
    print(json.dumps({'status':'prepared','characters':len(packet),'losslessSourceReconstructions':43,'publicBindings':27,'protectedFiles':len(files)}))
if __name__=='__main__':main()
