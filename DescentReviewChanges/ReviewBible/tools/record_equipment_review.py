"""Record the completed exact review after its six concrete repairs are applied."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def backup(p,name):
    q=AUDIT/name
    if not q.exists():q.write_bytes(p.read_bytes())

def main():
    statusfile=ROOT/'docs/mechanics/EQUIPMENT_REVIEW_STATUS.json'
    if statusfile.exists():raise SystemExit('Equipment review already recorded; do not repeat promotion.')
    validation=json.loads((AUDIT/'EQUIPMENT_CANDIDATE_VALIDATION.json').read_text(encoding='utf-8'))
    assert validation['status']=='PASS' and validation['checkCount']==78
    reply=AUDIT/'GPT_EQUIPMENT_EXACT_REVIEW_BROWSER.txt'
    assert reply.exists() and 'After the six repairs above' in reply.read_text(encoding='utf-8')
    repairs=[
      'Four ammunition kits record one retail bundle with20 grantedUnits; prose and price-unit policy agree.',
      'Five printed filled consumables mark source gross weight; four completed filled weights mark operational contents while preserving source null; healer kit remains3lb regardless of charges.',
      'Broken worn/held gear retains physical drawbacks, slots, hands, mass and doff requirements.',
      'One oil coating per creature across users; ground fire limited once per affected creature per any turn, regardless of whose turn.',
      'Core repair service uses undamaged applicable valuation before damage/standing/sale discounts.',
      'Component pouch has ordinary pouch capacity, with original2lb/25gp and no new F access.'
    ]
    guides=['EQUIPMENT_ACQUISITION_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_STARTING_PACKAGES.md']
    for name in guides:
        p=ROOT/'docs/mechanics'/name;s=p.read_text(encoding='utf-8')
        s=s.replace('**AUTHORED PLAYTEST CANDIDATE — exact manuscript review pending.**','**REVIEWED authored operational PLAYTEST equipment/acquisition scope.**')
        s=s.replace('**AUTHORED PLAYTEST CANDIDATE — exact review pending.**','**REVIEWED authored operational PLAYTEST equipment/acquisition scope.**')
        s=s.replace('including its twelve repairs, transaction rounding and poison clarification.','including its twelve conference repairs, the [six exact-review repairs](../../../../docs/audit/2026-10-08/full-game/GPT_EQUIPMENT_EXACT_REVIEW.md), transaction rounding and poison clarification.')
        s=s.replace('New candidate quantity completion','New agreed quantity completion').replace('new candidate quantity completion','new agreed quantity completion')
        p.write_text(s,encoding='utf-8')
    cp=ROOT/'data/playtest/equipment_acquisition_candidate.json';c=json.loads(cp.read_text(encoding='utf-8'))
    c['status']='REVIEWED authored operational PLAYTEST equipment/acquisition scope'
    c['exactReviewTurnId']='dc3b5e6d-6960-46d6-bb49-7d9d77f676ed'
    c['approvalCondition']='Six required repairs applied; two local quantity completions and nonstacking oil explicitly approved.'
    for x in c['items']+c['packs']:x['status']='reviewed-authored-playtest'
    for x in c['backgrounds']:x['physicalMapping']=x['physicalMapping'].replace('New candidate quantity completion','New agreed quantity completion').replace('new candidate quantity completion','new agreed quantity completion')
    dump(cp,c)
    wrapper='# Exact equipment manuscript review\n\nActual GPT notebook: [Calibration Review](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede). Turn `dc3b5e6d-6960-46d6-bb49-7d9d77f676ed`, response `446420f4-f14b-43f8-9d5b-5276c9b03c7d`. The complete [visible response](GPT_EQUIPMENT_EXACT_REVIEW_BROWSER.txt) is preserved with SHA-256 `'+sha(reply)+'`.\n\nGPT conditionally approves the bounded equipment scope after six repairs. All six are applied:\n\n'+''.join('- '+x+'\n' for x in repairs)+'\nThe exact reviewed scope includes220 item records, seven packs,17 class kits and20 background physical mappings. Source tables preserve273 rows. The original source information remains intact. This is authored playtest review, not runtime, human-balance, whole-game or final-delivery certification. Cosmology remains post-push only.\n'
    (AUDIT/'GPT_EQUIPMENT_EXACT_REVIEW.md').write_text(wrapper,encoding='utf-8')
    paths=[ROOT/'docs/mechanics'/n for n in guides]+[ROOT/'docs/mechanics/EQUIPMENT_SOURCE_BINDINGS.md',cp,ROOT/'data/playtest/equipment_source_catalog.json']
    manifest={'status':c['status'],'sourceConferenceTurn':'2e6b4aa3-d9e7-4983-9ef3-a3ca4f3da037','exactReviewTurn':c['exactReviewTurnId'],
      'approvalCondition':c['approvalCondition'],'repairsApplied':repairs,'coverage':{'sourceTableRows':273,'sourceTables':17,'physicalSourceItems':195,'newItemProfiles':25,'itemRecords':220,'packs':7,'classKits':17,'backgrounds':20},
      'validationChecks':78,'protectedBaselineFilesUnchanged':34,'classContractsUnchanged':17,
      'originalSourcesDeleted':0,'githubPushed':False,'cosmology':'deferred until successful authorized push and verified remote commit',
      'unclosedScope':c['openScope']+['full game flow and final delivery'],
      'artifactHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in paths},'exactReplySha256':sha(reply)}
    dump(statusfile,manifest)
    sp=AUDIT/'EQUIPMENT_EXACT_SUBMISSION.json';m=json.loads(sp.read_text());m.update(status='completed; all six required repairs applied',replyFile=reply.name,replySha256=sha(reply),reviewStatus=str(statusfile.relative_to(GAME)).replace('\\','/'));dump(sp,m)
    coverage=ROOT/'data/playtest/game_development_coverage.json';backup(coverage,'COVERAGE_BEFORE_EQUIPMENT.json')
    cv=json.loads(coverage.read_text(encoding='utf-8'))
    notes={
      'DD-00':'Equipment source/projection provenance preserved:273 table rows, all source nulls, separate new procedures and exact review hashes; no original deleted.',
      'DD-04':'All17 fixed class gear alternatives and20 background physical mappings reviewed; real choices, fitted size, ammunition and carrying remain explicit. Broader character creation dependencies remain open.',
      'DD-25':'All38 source weapon options preserved, including unarmed as noninventory; repeating heavy crossbow/kama/nunchaku profiles and exact Sidearm set reviewed. Broader card/feat/recipe/runtime interactions remain open.',
      'DD-26':'Mundane armor/shield AC, strength, Dwarf exception, proficiency and casting boundaries, grade and broken-gear drawbacks reviewed. Broader magic/DR/class integration remains open.',
      'DD-27':'220 item records, seven exact packs, source/operational gross weights, actual container capacity and17 creation-kit masses reviewed. Runtime and transport remain open.',
      'DD-28':'Common medicine, alchemy, lights, traps/restraints and tools have reviewed actions/targets/charges/lifetimes.687 recipe outputs and magical equipment remain open.',
      'DD-29':'Crafting structural audit preserves687 recipes/696 global materials;433 public records match source exactly and all consumed-value/weight arithmetic matches. Equipment grade is separated from craft outcome; recipe mechanics remain unapproved.',
      'DD-30':'Ordinary currency, retail-bundle/individual-unit distinction, qualitative resale, final cp rounding and self/professional repair bases reviewed. Full market/faction/recipe economics remain open.',
      'DD-31':'Background ordinary focuses and Celestial Emissary dim-light reliquary have bounded physical rules; no magical item catalog/durability/attunement closure.'}
    for x in cv['aspects']:
        if x['id'] not in notes:continue
        x['status']='selected-interfaces-closed-remainder-integrating';x['closure']='open'
        for field,values in {
          'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_EQUIPMENT_ACQUISITION_CONFERENCE.md','docs/audit/2026-10-08/full-game/GPT_EQUIPMENT_EXACT_REVIEW.md'],
          'sourceEvidence':['docs/audit/2026-10-08/full-game/EQUIPMENT_SOURCE_EVIDENCE.json','docs/audit/2026-10-08/full-game/CRAFTING_COMPONENT_STRUCTURAL_AUDIT.json'],
          'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/'+n for n in guides],
          'validationEvidence':['docs/audit/2026-10-08/full-game/EQUIPMENT_CANDIDATE_VALIDATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_REVIEW_STATUS.json']}.items():
            for v in values:
                if v not in x.setdefault(field,[]):x[field].append(v)
        x.setdefault('completedScopes',[]).append(notes[x['id']])
    dump(coverage,cv)
    start=GAME/'START_HERE.md';backup(start,'START_HERE_BEFORE_EQUIPMENT.md');s=start.read_text(encoding='utf-8')
    anchor='| Ordinary spells |'
    row='| [Equipment and acquisition](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md) |220 item records, seven packs,17 class kits and20 background physical mappings jointly reviewed;78 checks pass | Full crafting outputs, transport, artifact/faction economy, runtime and balance |\n'
    s=s.replace(anchor,row+anchor,1)
    s=s.replace('Equipment and remaining ancestry/background dependencies; companion integration','Remaining creation choices, Supply/Reputation/Oracle dependencies and companion integration',1)
    old='The latest reviewed manuscript is [ancestry/background integration]'
    s=s.replace(old,'The previous reviewed manuscript is [ancestry/background integration]',1)
    pos=s.index('The previous reviewed manuscript is')
    para='The latest reviewed scope is [equipment and acquisition](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md), with [item procedures](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md) and [all starting packages](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_STARTING_PACKAGES.md). All six exact-review repairs are applied;78 checks pass,34 protected files and all17 class contracts are unchanged. The foundation guide’s earlier pending labels for ancestry/background and mundane gear are superseded by these linked supplements. Complete crafting, transport, the expedition-to-Haven flow and the remaining catalogs still need work. No GitHub push or cosmology review has occurred.\n\n'
    s=s[:pos]+para+s[pos:];start.write_text(s,encoding='utf-8')
    p=AUDIT/'REVIEW_STATUS.md';backup(p,'REVIEW_STATUS_BEFORE_EQUIPMENT.md')
    with p.open('a',encoding='utf-8') as f:
        f.write('\n\n## Mundane equipment and acquisition reviewed\n\nThe [source conference](GPT_EQUIPMENT_ACQUISITION_CONFERENCE.md) and [exact manuscript review](GPT_EQUIPMENT_EXACT_REVIEW.md) approve the bounded equipment scope after twelve conference repairs and six exact repairs, all applied. The [review manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_REVIEW_STATUS.json) records final hashes.273 source rows and seven packs are preserved;220 operational item records include195 source items and25 explicit additions, with17 class kits and20 background mappings.\n\nAll78 source/projection checks pass.34 protected files and17 class contracts remain unchanged. The crafting structural audit confirms all687 consumed-material totals and exact433-public-record parity; it does not approve recipe effects. Full crafting, harvesting, transport, artifact/faction economy, runtime/companion behavior, balance and remaining game areas stay open. No source deletion, GitHub push or cosmology review occurred.\n')
    (AUDIT/'EQUIPMENT_REVIEW_CHECKPOINT.md').write_text('# Equipment review completed\n\nThe source conference and exact review are complete. All twelve conference repairs and six exact repairs are applied. Read EQUIPMENT_REVIEW_STATUS.json for the exact final artifact hashes, scope and exclusions. The78 verification checks pass. Start Here and the whole-game ledger now link this bounded reviewed scope.\n\nNext work: crafting/harvesting/economy and the expedition-to-Haven flow, plus larger unfinished spell/feat catalogs and existing integrations. No original information was deleted. No GitHub push occurred. Cosmology remains deferred until after successful authorized push and verified remote commit.\n',encoding='utf-8')
    print(json.dumps({'status':manifest['status'],'files':len(paths),'checks':78,'allSixRepairsApplied':True}))

if __name__=='__main__':main()
