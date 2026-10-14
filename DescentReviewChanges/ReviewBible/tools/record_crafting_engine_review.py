"""Record actual GPT conditional approval after all eight exact repairs."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TURN='efef736f-b8e7-4fbc-a0d4-65e3df137876'
REPLY='3f8aefb0-1fa8-4a85-9fff-ddc4552551ab'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def backup(p,name):
    q=AUDIT/name
    if not q.exists():q.write_bytes(p.read_bytes())

def main():
    status=ROOT/'docs/mechanics/CRAFTING_ENGINE_REVIEW_STATUS.json'
    if status.exists():raise SystemExit('Review already recorded; do not repeat.')
    v=read(AUDIT/'CRAFTING_ENGINE_VALIDATION.json')
    assert v['status']=='PASS'
    reply=AUDIT/'GPT_CRAFTING_ENGINE_EXACT_REVIEW.txt'
    assert 'CONDITIONALLY APPROVE with 8 finite repairs' in reply.read_text(encoding='utf-8')
    main=ROOT/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md';s=main.read_text(encoding='utf-8')
    expected=['isolated framework test','This reduced maximum is a crafting flaw','within the selected attempted allocation',
              'maximum quantity physically remaining','pause the order before further active work','Any physically capable workers',
              'stored numeric `tier`','The two-Watch ceiling limits this framework']
    assert all(x in s for x in expected)
    repairs=['Unreviewed output effects grant no gameplay benefit; isolated framework tests only.',
             'Flawed durable maximum HP persists through ordinary repair; no free craftsmanship correction.',
             'Critical harvest recovery stays inside the selected attempted allocation.',
             'Successful dismantling recovers exactly 25% of predeclared physically remaining ordinary component quantities.',
             'Illegal perishables pause work; legal replacement or abandonment, no quality roll.',
             'Mishap 5 requires finite worker-count labor that any capable workers can perform.',
             'Stored component tiers above VI retain identity but grant no generic harvest/public entitlement.',
             'Two active work Watches cap this framework only; other expedition/rest rules keep authority.']
    label='REVIEWED authored operational PLAYTEST crafting/harvesting/preservation framework'
    s=s.replace('**Status: authored candidate awaiting GPT review.**', '**Status: '+label+'.**')
    s=s.replace('**Forge Dwarf completion proposed for review:**','**Reviewed Forge Dwarf completion:**')
    s=s.replace('Exact source text, hashes and paragraph/line bindings are in', 'The [actual GPT review](../../../../docs/audit/2026-10-08/full-game/GPT_CRAFTING_ENGINE_EXACT_REVIEW.md) conditionally approved this framework; all eight required repairs are applied. Exact source text, hashes and paragraph/line bindings are in')
    main.write_text(s,encoding='utf-8')
    ref=ROOT/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md';s=ref.read_text(encoding='utf-8')
    s=s.replace('**Status: authored framework candidate awaiting GPT review.**','**Status: reviewed authored operational PLAYTEST framework reference.**')
    ref.write_text(s,encoding='utf-8')
    paths=[main,ref,ROOT/'data/playtest/crafting_engine_candidate.json',ROOT/'data/director/crafting_engine_recipe_index.json']
    for p in paths[2:]:
        c=read(p);c['status']=label;c['exactReviewTurnId']=TURN;c['approvalCondition']='All eight exact repairs applied; no additional generic framework conference required.';dump(p,c)
    text='# Crafting framework source and exact manuscript review\n\nActual notebook: [Calibration Review](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede). Turn `'+TURN+'`, reply `'+REPLY+'`. The [full actual response](GPT_CRAFTING_ENGINE_EXACT_REVIEW.txt) has SHA-256 `'+sha(reply)+'`.\n\nGPT conditionally approved the complete source/manuscript packet with eight finite repairs. All eight are applied:\n\n'+''.join('- '+x+'\n' for x in repairs)+'\nThis approves the shared operational framework, 16 trade bindings and five new mundane kits. All 687 individual recipe effects remain unreviewed, with 433 public rows separated from restricted/Director records. It does not approve runtime, balance, full expedition/Haven/economy integration or whole-game delivery. No source deletion or GitHub push occurred. Cosmology remains deferred until after successful authorized push and remote verification.\n'
    (AUDIT/'GPT_CRAFTING_ENGINE_EXACT_REVIEW.md').write_text(text,encoding='utf-8')
    manifest={'status':label,'exactReviewTurnId':TURN,'replyId':REPLY,'replySha256':sha(reply),'repairsApplied':repairs,
       'coverage':{'trades':16,'newMundaneKits':5,'recipeFrameworkRows':687,'publicRows':433,'restrictedRows':39,'directorOnlyRows':215,'recipeEffectsApproved':0},
       'validationChecks':37,'protectedMechanicsAndSourceFilesUnchanged':88,'coverageLedgerOriginalPreserved':True,
       'artifactHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in paths},
       'originalSourcesDeleted':0,'githubPushed':False,'cosmology':'post-verified-push only',
       'remaining':['All 687 output effects','Magic essence and active-core containment','Full expedition/Haven and Supply integration','Runtime and companion parity','Human balance','Full game flow and final delivery']}
    dump(status,manifest)
    sp=AUDIT/'CRAFTING_ENGINE_SUBMISSION.json';submission=read(sp)
    submission.update(status='completed; all eight repairs applied',turnId=TURN,replyId=REPLY,replyFile=reply.name,replySha256=sha(reply),reviewStatus=str(status.relative_to(GAME)));dump(sp,submission)
    coverage=ROOT/'data/playtest/game_development_coverage.json';backup(coverage,'COVERAGE_BEFORE_CRAFTING_ENGINE.json');cv=read(coverage)
    notes={
      'DD-00':'Crafting framework source/exact review preserved primary books/JSON and all source IDs. V5 2400-hour Opening supersedes stale 240-hour framework sentence; source remains intact.',
      'DD-03':'Crafting active time, Workday/Week/Month conversions, interruptible phases and no overlapping labor/rest reviewed. Two-Work-Watch ceiling is framework-scoped only.',
      'DD-06':'Trade level1-20 progression, first/repeat/failure/trivial XP, excess carry and level10 specialty reviewed independently of character level/PB.',
      'DD-15':'16 primary-tool/trade bindings, training entry, once-only PB, assistant caps, safe take10 and six-band craft results reviewed.',
      'DD-27':'Crafting batches, exact component identities, finite recovery, physical packaging and preservation mass now have bounded rules; per-output mass/packaging still open.',
      'DD-28':'Five new mundane craft kits and station rental reviewed; all687 unique recipe effects remain unreviewed.',
      'DD-29':'Crafting/harvesting/preservation framework jointly reviewed after eight repairs.687 IDs indexed;49 rank-band conflicts preserve individual requirements;19 consumed tool rows retained. Individual recipe cards still open.',
      'DD-30':'Standard batch reference vs unit ratios, finite buyer quotes, commission terms and ordinary/artifact market separation reviewed for crafting; full economy remains open.',
      'DD-38':'Finite harvest manifests, single total size-yield pool, exceptional-drop deduplication, partial selection and dismantling caps reviewed. Broader rewards remain open.',
      'DD-39':'Size-based harvesting and hurried/partial times integrate with actual Watch minutes. Full travel/route procedure remains open.',
      'DD-40':'Material preservation age, treatment intervals and spoiled-input replacement reviewed. These do not close Supply, Strain or all expedition resources.',
      'DD-41':'Crafting work cannot double-count beneficial rest; this framework does not resolve the separate rest/recovery integration.',
      'DD-43':'Ordinary workshop rental, batch workday assignment and commission boundaries reviewed; complete Haven flow still open.',
      'DD-44':'Trade training, crafting phase scheduling, formula transcription/research and finite market work reviewed; other downtime remains open.',
      'DD-54':'Framework projection keeps433 public recipes separate from39 restricted and215 Director-only; no restricted material export or cosmology review.'}
    for x in cv['aspects']:
        if x['id'] not in notes:continue
        x['status']='selected-interfaces-closed-remainder-integrating';x['closure']='open'
        for key,vals in {'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_CRAFTING_ENGINE_EXACT_REVIEW.md'],
          'sourceEvidence':['docs/audit/2026-10-08/full-game/CRAFTING_ENGINE_SOURCE_EVIDENCE.json'],
          'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_TRADE_REFERENCE.md'],
          'validationEvidence':['docs/audit/2026-10-08/full-game/CRAFTING_ENGINE_VALIDATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_ENGINE_REVIEW_STATUS.json']}.items():
            for val in vals:
                if val not in x.setdefault(key,[]):x[key].append(val)
        x.setdefault('completedScopes',[]).append(notes[x['id']])
    dump(coverage,cv)
    start=GAME/'START_HERE.md';backup(start,'START_HERE_BEFORE_CRAFTING_ENGINE.md');s=start.read_text(encoding='utf-8')
    s=s.replace('**Current position — 9 October 2026**','**Current position — 10 October 2026**',1)
    s=s.replace('| Ordinary spells |','| [Crafting and harvesting](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md) | Shared framework, 16 trades, five new kits and preservation jointly reviewed; all eight repairs applied | All 687 recipe effects, magical containment, full expedition/Haven flow, runtime and balance |\n| Ordinary spells |',1)
    s=s.replace('The latest reviewed scope is [equipment and acquisition]','The preceding reviewed scope is [equipment and acquisition]',1)
    anchor='The preceding reviewed scope is [equipment and acquisition]'
    para='The latest reviewed scope is [crafting, harvesting and preservation](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md), with [all 16 trade bindings](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_TRADE_REFERENCE.md). GPT’s eight exact repairs are applied. The framework resolves training, time, quality, finite material recovery, harvest allocation, spoilage, formula research and batch pricing. It supplies the bounded Forge Dwarf crafting-quality integration that earlier ancestry/equipment notes left open. All 687 recipe effects remain separate work: their source records are preserved, with 433 public rows kept separate from restricted/Director entries. The next recipe pass begins with 45 Alchemy formulas. No GitHub push or cosmology review has occurred.\n\n'
    s=s.replace(anchor,para+anchor,1);start.write_text(s,encoding='utf-8')
    review=AUDIT/'REVIEW_STATUS.md';backup(review,'REVIEW_STATUS_BEFORE_CRAFTING_ENGINE.md')
    with review.open('a',encoding='utf-8') as f:f.write('\n\n## Crafting, harvesting and preservation framework reviewed\n\nThe [actual source/exact review](GPT_CRAFTING_ENGINE_EXACT_REVIEW.md) conditionally approves the authored framework after eight finite repairs, all applied. The [final manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_ENGINE_REVIEW_STATUS.json) records artifact hashes and scope. The framework covers16 trades, five new kits, training, work phases, quality, ingredient recovery, finite harvesting, preservation, basic dismantling, formula research and batch pricing. All687 unique recipe effects remain unreviewed.\n\n37 source/visibility/reference checks pass;88 protected mechanics/source files are unchanged, and the original administrative coverage ledger is preserved byte-for-byte before its authorized update. The recipe queue contains25 families and56 source review flags. Next: complete Alchemy’s45 recipes, then the other families and full expedition-to-Haven flow. No original information deleted, no GitHub push and no cosmology evaluation.\n')
    (AUDIT/'CRAFTING_ENGINE_REVIEW_CHECKPOINT.md').write_text('# Crafting framework completed\n\nActual GPT turn '+TURN+' conditionally approves after eight repairs. All eight are applied and the review manifest records final hashes.37 checks pass,88 source/mechanics files are unchanged, and the prior coverage ledger is preserved. No effect approval is implied for any of687 recipes.\n\nNext: Alchemy45 formulas (27 public,5 restricted,13 Director) captured in ALCHEMY_RECIPE_SOURCE_EVIDENCE.json. Full queue:25 output families,56 review flags. Resolve recipe prose/data discrepancies, activation, targets, duration, output mass/packaging, perishable phases and quality eligibility. Preserve IDs, legacy effects and visibility. Full expedition/Haven flow and remaining spell/feat catalogs still open. Cosmology only after successful authorized GitHub push and verified remote commit.\n',encoding='utf-8')
    print(json.dumps({'status':label,'repairsApplied':8,'artifactCount':len(paths),'recipeEffectsApproved':0}))

if __name__=='__main__':main()
