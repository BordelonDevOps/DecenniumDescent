import json,hashlib,sys
from pathlib import Path
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
sys.path.insert(0,str(R/'tools'));from build_spell_playtests import FIELDS
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sub=read(A/'ENCHANTMENT_RANK3_EXACT_SUBMISSION.json')
p1=(A/'CODEX_ENCHANTMENT_RANK3_EXACT_REVIEW_PART1.txt').read_text(encoding='utf-8')
base=json.loads(p1.split('\nPART 1 OF 4\n',1)[1]);rows=list(base['cards'])
for n in [2,3]:rows.extend(json.loads((A/f'CODEX_ENCHANTMENT_RANK3_EXACT_REVIEW_PART{n}.txt').read_text(encoding='utf-8').split('\n',1)[1])['cards'])
before={}
for row in rows:
    s={**base['defaults'],**row}
    for k,v in list(s.items()):
        if isinstance(v,dict) and 'concat' in v:s[k]=''.join(base['sharedFragments'][z['shared']] if isinstance(z,dict) else z for z in v['concat'])
    before[s['id']]=s
cards={s['id']:s for s in read(D/'candidate_enchantment_rank3.json')['spells']}
sources={s['id']:s for s in read(D/'candidate_enchantment_rank3_sources.json')['spells']}
catalog=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in catalog}
selected=[i for vals in read(D/'selected_sources.json').values() for i in vals]
changed={(i,f) for i in cards for f in FIELDS if before[i][f]!=cards[i][f]}
edits=read(A/'ENCHANTMENT_RANK3_EDITORIAL_STATUS_CHANGES.json')['changes']
expected={(x['id'],x['field']) for x in edits}
editorial_exact=changed==expected and len(expected)==3 and all(before[x['id']][x['field']]==x['before'] and cards[x['id']][x['field']]==x['after'] and x['before'].replace(x['removedStatusText'],x['replacementStatusText'])==x['after'] for x in edits)
doc=(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md').read_text(encoding='utf-8')
rendered=True
for i,s in cards.items():
    part=doc.split(f'<a id="spell-{i}"></a>',1)[1].split('<a id="spell-',1)[0]
    rendered &= all(s[f].replace('|','/') in part for f in FIELDS if isinstance(s[f],str))
existing={s['id']:s['operational'] for s in catalog if s['operational'] and s['id'] not in cards}
low=[s for s in catalog if not s['operational'] and any(a['rank']<=3 for a in s['classAccess'].values())]
enchlow=[s for s in catalog if not s['operational'] and any(a['school']=='Enchantment' and a['rank']<=3 for a in s['classAccess'].values())]
pipeline=read(R/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json')
coverage=read(R/'data/playtest/game_development_coverage.json')
pub=read(A/'ENCHANTMENT_RANK3_SHARED_PUBLICATION_CHANGES.json')
shared=(D/'candidate_enchantment_rank3_shared_rules.md').read_text(encoding='utf-8')
reconstructed=shared
for x in pub['statusLabelReplacements']:
    assert reconstructed.count(x['before'])==1
    reconstructed=reconstructed.replace(x['before'],x['after'])
reconstructed=reconstructed.rstrip()+'\n\n'+pub['appendedBindingClarification']+'\n'
part4=(A/'CODEX_ENCHANTMENT_RANK3_EXACT_REVIEW_PART4.txt').read_text(encoding='utf-8')
part4shared=part4.split('\n\n',1)[1].split('\n\nUNCHANGED REVIEWED COMPANION SOURCE',1)[0]
companion=Path(pub['companionPath']);baseline=Path(pub['companionBaselinePath'])
checks={
'eight_promoted_once':len(cards)==8 and all(selected.count(i)==1 and by[i]['operational'] for i in cards),
'only_three_documented_status_label_edits':editorial_exact and sub['requiredRepairsApplied']==[],
'candidate_batch_identical':(D/'candidate_enchantment_rank3.json').read_bytes()==(D/'batch_enchantment_rank3.json').read_bytes(),
'exact_source_evidence_and_aliases':all(cards[i]['sourcePlacements']==sources[i]['sourcePlacements']==by[i]['source']['original']['placements'] and cards[i]['sourceCoreEntries']==sources[i]['sourceCoreEntries']==by[i]['source']['coreEntries'] and sources[i]['possibleHistoricalAliases']==by[i]['source']['possibleHistoricalAliases'] for i in cards),
'eleven_placements_and_core_blocks':sum(len(s['sourcePlacements']) for s in cards.values())==sum(len(s['sourceCoreEntries']) for s in cards.values())==11,
'exact_class_access_preserved':all(cards[i]['classAccessEvidence']==sources[i]['classAccess']==by[i]['classAccess'] for i in cards),
'all_848_ids_936_placements_preserved':len(catalog)==len(by)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936,
'all_functional_fields_rendered':rendered and all(all(cards[i][f]==by[i]['operational'][f] for f in FIELDS) for i in cards),
'prior_229_operational_records_unchanged':len(existing)==229 and hashlib.sha256(json.dumps(existing,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==sub['previousOperationalSha256'],
'raw_source_hashes_unchanged':read(R/'data/playtest/spell_sources/source_hashes.json')==sub['sourceHashLedgerBefore'] and all(sha(R/x['path'])==x['sha256'] for x in sub['sourceHashLedgerBefore']),
'frozen_class_rules_unchanged':sha(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md')==sub['classRulesSha256Before']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81',
'prior_shared_rule_bodies_preserved':all(sha(baseline if Path(x['path'])==companion else Path(x['path']))==x['sha256'] for x in sub['sharedBaseHashesBefore']),
'companion_guide_only_appended_discovery_link':companion.read_bytes()==baseline.read_bytes()+pub['companionAppendedLink'].encode('utf-8') and sha(baseline)==pub['companionBaselineSha256'],
'pipeline_pass_42_89040':pipeline['status']=='PASS' and len(pipeline['checks'])==42 and pipeline['accessBoundaryCases']==89040 and pipeline['operationalDrafts']==237 and pipeline['unfinishedSpells']==611 and not pipeline['errors'],
'low_rank_unfinished_176':len(low)==176,
'no_unfinished_enchantment_class_rank0_to3':not enchlow,
'wider_coverage_not_closed':len(coverage['aspects'])==75 and sum(a['closure']=='closed' for a in coverage['aspects'])==1,
'four_actual_delivered_parts_match_prepared':len(sub['dispatch']['attachments'])==4 and all(Path(x['path']).read_text(encoding='utf-8-sig').rstrip()==Path(sub['parts'][n]['path']).read_text(encoding='utf-8').rstrip() and sha(Path(x['path']))==x['sha256'] for n,x in enumerate(sub['dispatch']['attachments'])),
'original_packet_and_parts_preserved':sha(Path(sub['packetPath']))==sub['packetSha256'] and all(sha(Path(x['path']))==x['sha256'] for x in sub['parts']),
'submitted_shared_body_preserved':part4shared.rstrip()==shared.rstrip() and sha(D/'candidate_enchantment_rank3_shared_rules.md')==sub['sharedCandidateSha256BeforeReview'],
'published_shared_body_matches_approved_status_changes_and_interpretation':reconstructed==Path(pub['publicationPath']).read_text(encoding='utf-8') and sha(Path(pub['publicationPath']))==pub['publicationSha256'],
'shared_supplement_linked_in_master':'[rank-three integration supplement](ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md)' in (R/'docs/mechanics/SPELL_INTEGRATION_RULES.md').read_text(encoding='utf-8'),
'cosmology_remains_post_push_open':next(a for a in coverage['aspects'] if a['id']=='DD-50')['workPhase']=='post-github-push' and next(a for a in coverage['aspects'] if a['id']=='DD-50')['closure']!='closed'
}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'documentedEditorialStatusFields':sorted([list(x) for x in changed]),'functionalRepairs':[],'operational':237,'unfinished':611,'unfinishedWithClassRank0To3':len(low),'unfinishedWithEnchantmentClassRank0To3':len(enchlow),'limits':'Exact manuscript/source/access preservation and schema/common-cost validation. No spell/companion effect-runtime execution, human numerical balance, variant closure, whole-game approval, GitHub push or cosmology review.','sourceDeletion':False,'githubPushed':False}
dump(A/'ENCHANTMENT_RANK3_PROMOTION_CHECK.json',result)
assert all(checks.values()),checks
p=R/'docs/mechanics/ENCHANTMENT_RANK3_REVIEW_STATUS.json';s=read(p);s.update(pipelineValidation='PASS',pipelineSummary='42 checks /89,040 class-level access boundaries /zero issues',promotionVerification='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK3_PROMOTION_CHECK.json',unfinishedWithClassRank0To3=176,unfinishedWithEnchantmentClassRank0To3=0,nextWork='Continue Evocation cantrip source conference using the preserved twelve-identity packet. All broader runtime/balance/whole-game gates remain open.');dump(p,s)
sub.update(status='promoted and verified;23 preservation/promotion checks plus42 pipeline checks PASS',promotionVerification='docs/audit/2026-10-08/full-game/ENCHANTMENT_RANK3_PROMOTION_CHECK.json');dump(A/'ENCHANTMENT_RANK3_EXACT_SUBMISSION.json',sub)
p=G/'START_HERE.md';t=p.read_text(encoding='utf-8').replace('Source preservation and catalog integration are being verified.','Source preservation and catalog integration passed 23 targeted checks; the spell pipeline passed 42 checks and 89,040 class-access boundary cases.');p.write_text(t,encoding='utf-8')
p=A/'REVIEW_STATUS.md';t=p.read_text(encoding='utf-8').replace('The catalog now targets 237 reviewed identities','The catalog now has 237 reviewed identities');p.write_text(t,encoding='utf-8')
print(json.dumps(result,indent=2))

