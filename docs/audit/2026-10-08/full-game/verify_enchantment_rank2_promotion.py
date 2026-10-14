import json, hashlib, sys
from pathlib import Path
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
sys.path.insert(0,str(R/'tools'))
from build_spell_playtests import FIELDS
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sub=read(A/'ENCHANTMENT_RANK2_EXACT_SUBMISSION.json')
p1=(A/'CODEX_ENCHANTMENT_RANK2_EXACT_REVIEW_PART1.txt').read_text(encoding='utf-8')
p2=(A/'CODEX_ENCHANTMENT_RANK2_EXACT_REVIEW_PART2.txt').read_text(encoding='utf-8')
compact1=json.loads(p1.split('\nPART 1 OF 3\n',1)[1]);compact2=json.loads(p2.split('\n',1)[1])
restored=[]
for row in compact1['cards']+compact2['cards']:
    s={**compact1['defaults'],**row}
    for key,value in list(s.items()):
        if isinstance(value,dict) and 'concat' in value:
            s[key]=''.join(compact1['sharedFragments'][p['shared']] if isinstance(p,dict) else p for p in value['concat'])
    restored.append(s)
before={s['id']:s for s in restored}
cards={s['id']:s for s in read(D/'candidate_enchantment_rank2.json')['spells']}
sources={s['id']:s for s in read(D/'candidate_enchantment_rank2_sources.json')['spells']}
catalog=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in catalog}
selected=[i for values in read(D/'selected_sources.json').values() for i in values]
changes=[(i,f) for i in cards for f in FIELDS if before[i][f]!=cards[i][f]]
doc=(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md').read_text(encoding='utf-8')
rendered=True
for i,s in cards.items():
    part=doc.split(f'<a id="spell-{i}"></a>',1)[1].split('<a id="spell-',1)[0]
    rendered &= all(s[f].replace('|','/') in part for f in FIELDS if isinstance(s[f],str))
existing={s['id']:s['operational'] for s in catalog if s['operational'] and s['id'] not in cards}
low=[s for s in catalog if not s['operational'] and any(a['rank']<=3 for a in s['classAccess'].values())]
enchlow=[s for s in catalog if not s['operational'] and any(a['school']=='Enchantment' and a['rank']<=2 for a in s['classAccess'].values())]
pipeline=read(R/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json')
cov=read(R/'data/playtest/game_development_coverage.json')
pub=read(A/'ENCHANTMENT_RANK2_SHARED_PUBLICATION_CHANGES.json')
shared=(D/'candidate_enchantment_rank2_shared_rules.md').read_text(encoding='utf-8')
reconstructed=shared
for x in pub['statusLabelReplacements']:
    assert reconstructed.count(x['before'])==1
    reconstructed=reconstructed.replace(x['before'],x['after'])
reconstructed=reconstructed.rstrip()+'\n\n'+pub['appendedBindingClarifications']+'\n'
part3=(A/'CODEX_ENCHANTMENT_RANK2_EXACT_REVIEW_PART3.txt').read_text(encoding='utf-8')
part3shared=part3.split('\n\n',1)[1].split('\n\nEXISTING CLASS COMPARISON',1)[0]
checks={
'seven_promoted_once':len(cards)==7 and all(selected.count(i)==1 and by[i]['operational'] for i in cards),
'no_functional_card_changes':not changes and sub['requiredRepairsApplied']==[],
'candidate_batch_identical':(D/'candidate_enchantment_rank2.json').read_bytes()==(D/'batch_enchantment_rank2.json').read_bytes(),
'source_evidence_and_aliases_preserved':all(cards[i]['sourcePlacements']==sources[i]['sourcePlacements']==by[i]['source']['original']['placements'] and cards[i]['sourceCoreEntries']==sources[i]['sourceCoreEntries']==by[i]['source']['coreEntries'] and sources[i]['possibleHistoricalAliases']==by[i]['source']['possibleHistoricalAliases'] for i in cards),
'eight_placements_and_core_blocks':sum(len(s['sourcePlacements']) for s in cards.values())==sum(len(s['sourceCoreEntries']) for s in cards.values())==8,
'class_access_preserved':all(cards[i]['classAccessEvidence']==sources[i]['classAccess']==by[i]['classAccess'] for i in cards),
'all_848_ids_and_936_placements':len(catalog)==len(by)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936,
'all_functional_fields_rendered':rendered and all(all(cards[i][f]==by[i]['operational'][f] for f in FIELDS) for i in cards),
'prior_222_operational_records_unchanged':len(existing)==222 and hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sub['previousOperationalSha256'],
'source_hashes_unchanged':read(R/'data/playtest/spell_sources/source_hashes.json')==sub['sourceHashLedgerBefore'] and all(sha(R/x['path'])==x['sha256'] for x in sub['sourceHashLedgerBefore']),
'five_class_comparison_sources_unchanged':all(sha(G/x['path'])==x['sha256'] for x in read(A/'ENCHANTMENT_RANK2_EMOTION_CLASS_EVIDENCE.json')['records']),
'frozen_class_rules_unchanged':sha(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md')==sub['classRulesSha256Before']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81',
'pipeline_pass':pipeline['status']=='PASS' and len(pipeline['checks'])==42 and pipeline['accessBoundaryCases']==89040 and pipeline['operationalDrafts']==229 and pipeline['unfinishedSpells']==619 and not pipeline['errors'],
'low_rank_unfinished_184':len(low)==184,
'all_enchantment_rank0_through_rank2_identities_authored':not enchlow,
'wider_coverage_not_closed':len(cov['aspects'])==75 and sum(a['closure']=='closed' for a in cov['aspects'])==1,
'actual_three_delivered_parts_match_prepared':len(sub['dispatch']['attachments'])==3 and all(Path(x['path']).read_text(encoding='utf-8-sig').rstrip()==Path(sub['parts'][n]['path']).read_text(encoding='utf-8').rstrip() and sha(Path(x['path']))==x['sha256'] for n,x in enumerate(sub['dispatch']['attachments'])),
'exact_packet_and_parts_preserved':sha(Path(sub['packetPath']))==sub['packetSha256'] and all(sha(Path(x['path']))==x['sha256'] for x in sub['parts']),
'submitted_shared_body_preserved':part3shared.rstrip()==shared.rstrip() and sha(D/'candidate_enchantment_rank2_shared_rules.md')==sub['sharedCandidateSha256BeforeReview'],
'published_shared_body_matches_reviewed_status_changes_and_clarifications':reconstructed==Path(pub['publicationPath']).read_text(encoding='utf-8') and sha(Path(pub['publicationPath']))==pub['publicationSha256'],
'shared_rule_linked_in_master_overlay':'[shared control integration](ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md)' in (R/'docs/mechanics/SPELL_INTEGRATION_RULES.md').read_text(encoding='utf-8'),
'cosmology_remains_deferred_open':next(a for a in cov['aspects'] if a['id']=='DD-50')['workPhase']=='post-github-push' and next(a for a in cov['aspects'] if a['id']=='DD-50')['closure']!='closed'
}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'reviewedFieldChanges':changes,'operational':229,'unfinished':619,'unfinishedWithClassRank0To3':len(low),'unfinishedWithEnchantmentClassRank0To2':len(enchlow),'limits':'Exact source/access and manuscript preservation, rendered text, and schema/common-cost validation. No runtime execution, human numerical balance, variant closure, whole-game approval or cosmology review.','sourceDeletion':False,'githubPushed':False}
dump(A/'ENCHANTMENT_RANK2_PROMOTION_CHECK.json',result)
assert all(checks.values()),checks
p=R/'docs/mechanics/ENCHANTMENT_RANK2_REVIEW_STATUS.json';s=read(p)
s.update(pipelineValidation='PASS',pipelineSummary='42 checks / 89,040 class-level access boundaries / zero issues',promotionVerification='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK2_PROMOTION_CHECK.json',unfinishedWithClassRank0To3=184,unfinishedWithEnchantmentClassRank0To2=0)
dump(p,s)
sub.update(status='promoted and verified; 22 preservation/promotion checks plus 42 pipeline checks pass',promotionVerification='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK2_PROMOTION_CHECK.json')
dump(A/'ENCHANTMENT_RANK2_EXACT_SUBMISSION.json',sub)
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8');t=t.replace('Source preservation and catalog integration are being verified.','Source preservation and catalog integration passed 22 targeted checks; the spell pipeline passed 42 checks and 89,040 class-access boundary cases.');p.write_text(t,encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8');t=t.replace('The catalog now targets 229 reviewed identities','The catalog now has 229 reviewed identities');p.write_text(t,encoding='utf-8')
print(json.dumps(result,indent=2))

