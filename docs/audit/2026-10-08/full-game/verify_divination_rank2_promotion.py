import json, hashlib, sys
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'; D=R/'data/playtest/spell_drafts'
sys.path.insert(0,str(R/'tools'))
from build_spell_playtests import FIELDS
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
sub=read(A/'DIVINATION_RANK2_EXACT_SUBMISSION.json')
fence=chr(96)*3
submitted=json.loads((A/'CODEX_DIVINATION_RANK2_EXACT_REVIEW.md').read_text(encoding='utf-8').split(fence+'json\n',1)[1].split('\n'+fence,1)[0])
before={s['id']:s for s in submitted['spells']}
candidate=read(D/'candidate_divination_rank2.json')
cards={s['id']:s for s in candidate['spells']}
source={s['id']:s for s in read(D/'candidate_divination_rank2_sources.json')['spells']}
catalog=read(R/'data/public/spell_playtests/catalog.json')['spells']; by={s['id']:s for s in catalog}
selected=[i for v in read(D/'selected_sources.json').values() for i in v]
changed=sorted((i,f) for i in cards for f in FIELDS if before[i][f]!=cards[i][f])
expected=sorted((r['id'],r['field']) for r in sub['requiredRepairsApplied'])
approved={(r['id'],r['field']):r['after'] for r in sub['requiredRepairsApplied']}
doc=(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md').read_text(encoding='utf-8')
rendered=True
for i,s in cards.items():
    part=doc.split(f'<a id="spell-{i}"></a>',1)[1].split('<a id="spell-',1)[0]
    rendered &= all(s[f].replace('|','/') in part for f in FIELDS if isinstance(s[f],str))
low=[s for s in catalog if not s['operational'] and any(a['rank']<=3 for a in s['classAccess'].values())]
divlow=[s for s in catalog if not s['operational'] and any(a['school']=='Divination' and a['rank']<=2 for a in s['classAccess'].values())]
existing={s['id']:s['operational'] for s in catalog if s['operational'] and s['id'] not in cards}
pipeline=read(R/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json')
cov=read(R/'data/playtest/game_development_coverage.json')['aspects']
checks={
 'eight_promoted_once':len(cards)==8 and all(selected.count(i)==1 and by[i]['operational'] for i in cards),
 'only_six_reviewed_functional_fields_changed':changed==expected and len(changed)==6,
 'exact_approved_repairs_applied':all(cards[i][f]==v for (i,f),v in approved.items()),
 'candidate_batch_identical':(D/'candidate_divination_rank2.json').read_bytes()==(D/'batch_divination_rank2.json').read_bytes(),
 'source_evidence_preserved':all(cards[i]['sourcePlacements']==source[i]['sourcePlacements']==by[i]['source']['original']['placements'] and cards[i]['sourceCoreEntries']==source[i]['sourceCoreEntries']==by[i]['source']['coreEntries'] and source[i]['possibleHistoricalAliases']==by[i]['source']['possibleHistoricalAliases'] for i in cards),
 'class_access_preserved':all(cards[i]['classAccessEvidence']==source[i]['classAccess']==by[i]['classAccess'] for i in cards),
 'all_848_ids_and_936_placements':len(catalog)==len(by)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936,
 'all_functional_fields_rendered':rendered and all(all(cards[i][f]==by[i]['operational'][f] for f in FIELDS) for i in cards),
 'prior_182_operational_records_unchanged':len(existing)==182 and hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sub['previousOperationalSha256'],
 'source_hashes_unchanged':read(R/'data/playtest/spell_sources/source_hashes.json')==sub['sourceHashLedgerBefore'] and all(sha(R/x['path'])==x['sha256'] for x in sub['sourceHashLedgerBefore']),
 'frozen_class_rules_unchanged':sha(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md')==sub['classRulesSha256Before']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81',
 'pipeline_pass':pipeline['status']=='PASS' and len(pipeline['checks'])==42 and pipeline['accessBoundaryCases']==89040 and pipeline['operationalDrafts']==190 and pipeline['unfinishedSpells']==658 and not pipeline['errors'],
 'low_rank_unfinished_223':len(low)==223,
 'all_divination_rank_0_to_2_identities_authored':len(divlow)==0,
 'wider_coverage_not_closed':len(cov)==75 and sum(a['closure']=='closed' for a in cov)==1
}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'reviewedFieldChanges':changed,'operational':190,'unfinished':658,'unfinishedWithClassRank0To3':len(low),'unfinishedWithDivinationClassRank0To2':len(divlow),'limits':'Source, exact reviewed repairs, rendered manuscript, existing-card preservation and schema/access/common-cost verification. Not effect-runtime execution, source-variant closure or numerical balance.','sourceDeletion':False,'githubPushed':False}
dump(A/'DIVINATION_RANK2_PROMOTION_CHECK.json',result)
assert all(checks.values()), checks
statusp=R/'docs/mechanics/DIVINATION_RANK2_REVIEW_STATUS.json'; status=read(statusp)
status.update({'pipelineValidation':'PASS','pipelineSummary':'42 checks / 89,040 class-level access boundaries / zero issues','promotionVerification':'docs/audit/2026-10-08/full-game/DIVINATION_RANK2_PROMOTION_CHECK.json','unfinishedWithClassRank0To3':223,'unfinishedWithDivinationClassRank0To2':0})
dump(statusp,status)
sub.update({'status':'promoted and verified; 15 promotion checks plus 42 pipeline checks pass','promotionVerification':'docs/audit/2026-10-08/full-game/DIVINATION_RANK2_PROMOTION_CHECK.json'})
dump(A/'DIVINATION_RANK2_EXACT_SUBMISSION.json',sub)
print(json.dumps(result,indent=2))
