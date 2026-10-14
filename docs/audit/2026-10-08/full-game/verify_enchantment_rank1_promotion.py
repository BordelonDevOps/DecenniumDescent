import json,hashlib,sys
from pathlib import Path
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
sys.path.insert(0,str(R/'tools'))
from build_spell_playtests import FIELDS
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sub=read(A/'ENCHANTMENT_RANK1_EXACT_SUBMISSION.json');fence=chr(96)*3
submitted=json.loads((A/'CODEX_ENCHANTMENT_RANK1_EXACT_REVIEW.md').read_text(encoding='utf-8').split(fence+'json\n',1)[1].split('\n'+fence,1)[0])
before={s['id']:s for s in submitted['spells']}
cards={s['id']:s for s in read(D/'candidate_enchantment_rank1.json')['spells']}
source={s['id']:s for s in read(D/'candidate_enchantment_rank1_sources.json')['spells']}
catalog=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in catalog}
selected=[i for v in read(D/'selected_sources.json').values() for i in v]
changed=[(i,f) for i in cards for f in FIELDS if before[i][f]!=cards[i][f]]
doc=(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md').read_text(encoding='utf-8')
rendered=True
for i,s in cards.items():
 part=doc.split(f'<a id="spell-{i}"></a>',1)[1].split('<a id="spell-',1)[0]
 rendered &= all(s[f].replace('|','/') in part for f in FIELDS if isinstance(s[f],str))
low=[s for s in catalog if not s['operational'] and any(a['rank']<=3 for a in s['classAccess'].values())]
enchlow=[s for s in catalog if not s['operational'] and any(a['school']=='Enchantment' and a['rank']<=1 for a in s['classAccess'].values())]
existing={s['id']:s['operational'] for s in catalog if s['operational'] and s['id'] not in cards}
pipeline=read(R/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json')
cov=read(R/'data/playtest/game_development_coverage.json')['aspects']
compact=(A/'CODEX_ENCHANTMENT_RANK1_EXACT_REVIEW_COMPACT.md').read_text(encoding='utf-8')
shared=json.loads(compact.split('Shared fields: ',1)[1].split('\n\n',1)[0])
hard=compact.split('HARD_GUARD: ',1)[1].split('\n\n',1)[0]
suffix=compact.split('LIMITATIONS_SUFFIX: ',1)[1].split('\n\n',1)[0]
crows=json.loads(compact.split('## Exact per-card fields\n\n',1)[1].split('\n\n## Explicit questions',1)[0])
restored=[]
for c in crows:
 s={**shared,**c};s['limitations']=s['limitations'].replace('{HARD_GUARD}',hard)+suffix;restored.append(s)
delivered=''.join(Path(x['path']).read_text(encoding='utf-8-sig').split('\n',1)[1] for x in sub['dispatch']['attachments'])
checks={
'twelve_promoted_once':len(cards)==12 and all(selected.count(i)==1 and by[i]['operational'] for i in cards),
'no_functional_card_fields_changed':not changed and sub['requiredRepairsApplied']==[],
'candidate_batch_identical':(D/'candidate_enchantment_rank1.json').read_bytes()==(D/'batch_enchantment_rank1.json').read_bytes(),
'source_evidence_preserved':all(cards[i]['sourcePlacements']==source[i]['sourcePlacements']==by[i]['source']['original']['placements'] and cards[i]['sourceCoreEntries']==source[i]['sourceCoreEntries']==by[i]['source']['coreEntries'] and source[i]['possibleHistoricalAliases']==by[i]['source']['possibleHistoricalAliases'] for i in cards),
'thirteen_placements_and_core_blocks':sum(len(s['sourcePlacements']) for s in cards.values())==sum(len(s['sourceCoreEntries']) for s in cards.values())==13,
'class_access_preserved':all(cards[i]['classAccessEvidence']==source[i]['classAccess']==by[i]['classAccess'] for i in cards),
'all_848_ids_and_936_placements':len(catalog)==len(by)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936,
'all_functional_fields_rendered':rendered and all(all(cards[i][f]==by[i]['operational'][f] for f in FIELDS) for i in cards),
'prior_210_operational_records_unchanged':len(existing)==210 and hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sub['previousOperationalSha256'],
'source_hashes_unchanged':read(R/'data/playtest/spell_sources/source_hashes.json')==sub['sourceHashLedgerBefore'] and all(sha(R/x['path'])==x['sha256'] for x in sub['sourceHashLedgerBefore']),
'class_price_evidence_unchanged':all(sha(G/x['path'])==x['sha256'] for x in read(A/'ENCHANTMENT_RANK1_RP_DISCOUNT_EVIDENCE.json')['records']),
'frozen_class_rules_unchanged':sha(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md')==sub['classRulesSha256Before']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81',
'pipeline_pass':pipeline['status']=='PASS' and len(pipeline['checks'])==42 and pipeline['accessBoundaryCases']==89040 and pipeline['operationalDrafts']==222 and pipeline['unfinishedSpells']==626 and not pipeline['errors'],
'low_rank_unfinished_191':len(low)==191,
'all_enchantment_rank0_and_rank1_identities_authored':not enchlow,
'wider_coverage_not_closed':len(cov)==75 and sum(a['closure']=='closed' for a in cov)==1,
'compact_submission_losslessly_reconstructs_candidate':restored==submitted['spells'],
'actual_four_delivered_parts_match_packet':len(sub['dispatch']['attachments'])==4 and delivered.rstrip()==compact.rstrip() and all(sha(Path(x['path']))==x['sha256'] for x in sub['dispatch']['attachments']),
'original_exact_packet_preserved':sha(A/'CODEX_ENCHANTMENT_RANK1_EXACT_REVIEW.md')==sub['packetSha256']
}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'reviewedFieldChanges':changed,'operational':222,'unfinished':626,'unfinishedWithClassRank0To3':len(low),'unfinishedWithEnchantmentClassRank0Or1':len(enchlow),'limits':'Exact submitted-card text, source/access preservation, rendered manuscript and schema/common-cost verification. Not effect runtime execution, numerical balance, variant closure or whole-game approval.','sourceDeletion':False,'githubPushed':False}
dump(A/'ENCHANTMENT_RANK1_PROMOTION_CHECK.json',result)
assert all(checks.values()),checks
p=R/'docs/mechanics/ENCHANTMENT_RANK1_REVIEW_STATUS.json';s=read(p)
s.update(pipelineValidation='PASS',pipelineSummary='42 checks / 89,040 class-level access boundaries / zero issues',promotionVerification='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK1_PROMOTION_CHECK.json',unfinishedWithClassRank0To3=191,unfinishedWithEnchantmentClassRank0Or1=0)
dump(p,s)
sub.update(status='promoted and verified; 19 preservation/promotion checks plus 42 pipeline checks pass',promotionVerification='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK1_PROMOTION_CHECK.json')
dump(A/'ENCHANTMENT_RANK1_EXACT_SUBMISSION.json',sub)
print(json.dumps(result,indent=2))

