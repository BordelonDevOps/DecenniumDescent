from pathlib import Path
import json,hashlib,sys
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.path.insert(0,str(R/'tools'));from build_spell_playtests import FIELDS
sub=read(A/'EVOCATION_RANK2_EXACT_SUBMISSION.json');conference=read(A/'EVOCATION_RANK2_CONFERENCE_SUBMISSION.json')
parts=[json.loads((A/f'CODEX_EVOCATION_RANK2_EXACT_REVIEW_PART{n}.txt').read_text(encoding='utf-8').split(f'\nPART {n} OF 2\n',1)[1]) for n in range(1,3)]
before={}
for part in parts:
 for row in part['cards']:
  s={**parts[0]['defaults'],**row}
  for k,v in list(s.items()):
   if isinstance(v,dict) and 'concat' in v:s[k]=''.join(parts[0]['sharedFragments'][z['shared']] if isinstance(z,dict) else z for z in v['concat'])
  before[s['id']]=s
cards={s['id']:s for s in read(D/'candidate_evocation_rank2.json')['spells']};sources={s['id']:s for s in read(D/'candidate_evocation_rank2_sources.json')['spells']}
catalog=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in catalog}
selected=[i for v in read(D/'selected_sources.json').values() for i in v]
prior={s['id']:s['operational'] for s in catalog if s['operational'] and s['id'] not in cards}
repairs=read(A/'EVOCATION_RANK2_EXACT_REPAIR_LOG.json')['changes']
changed={(i,f) for i in cards for f in FIELDS if before[i][f]!=cards[i][f]}
expected={(x['id'],x['field']) for x in repairs}
text=(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md').read_text(encoding='utf-8');rendered=True
for i,s in cards.items():
 section=text.split(f'<a id="spell-{i}"></a>',1)[1].split('<a id="spell-',1)[0]
 rendered &= all(s[f].replace('|','/') in section for f in FIELDS if isinstance(s[f],str))
pipeline=read(R/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json');coverage=read(R/'data/playtest/game_development_coverage.json')
low=[s for s in catalog if not s['operational'] and any(x['rank']<=3 for x in s['classAccess'].values())]
evoc0=[s for s in catalog if not s['operational'] and any(x['rank']<=2 and x['school']=='Evocation' for x in s['classAccess'].values())]
checks={
 'eight_promoted_once':len(cards)==8 and all(selected.count(i)==1 and by[i]['operational'] for i in cards),
 'only_exactly_documented_review_repairs':changed==expected and all(before[x['id']][x['field']]==x['before'] and cards[x['id']][x['field']]==x['after'] for x in repairs),
 'candidate_batch_identical':(D/'candidate_evocation_rank2.json').read_bytes()==(D/'batch_evocation_rank2.json').read_bytes(),
 'eight_placements_five_exact_three_alias_blocks':sum(len(s['sourcePlacements']) for s in cards.values())==8 and sum(len(s['sourceCoreEntries']) for s in cards.values())==5 and sum(len(s['sourceHistoricalAliasEvidence']) for s in cards.values())==3,
 'exact_source_evidence_and_aliases':all(cards[i]['sourcePlacements']==sources[i]['sourcePlacements']==by[i]['source']['original']['placements'] and cards[i]['sourceCoreEntries']==sources[i]['sourceCoreEntries']==by[i]['source']['coreEntries'] and cards[i]['sourceHistoricalAliasEvidence']==sources[i]['possibleHistoricalAliases']==by[i]['source']['possibleHistoricalAliases'] for i in cards),
 'all_actual_class_access_preserved':all(cards[i]['classAccessEvidence']==sources[i]['classAccess']==by[i]['classAccess'] for i in cards),
 'all_848_ids_936_placements_retained':len(catalog)==len(by)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936,
 'all_functional_fields_rendered_exactly':rendered and all(all(cards[i][f]==by[i]['operational'][f] for f in FIELDS) for i in cards),
 'all_261_prior_operational_records_unchanged':len(prior)==261 and hashlib.sha256(compact(prior).encode()).hexdigest()==sub['previousOperationalSha256'],
 'all_frozen_source_and_class_files_unchanged':all(sha(R/k)==v for k,v in sub['frozenSourceAndClassFiles'].items()),
 'raw_source_hash_ledger_preserved':read(R/'data/playtest/spell_sources/source_hashes.json')==sub['sourceHashLedgerBefore'] and all(sha(R/x['path'])==x['sha256'] for x in sub['sourceHashLedgerBefore']),
 'frozen_class_rules_unchanged':sha(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md')==sub['classRulesSha256Before']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81',
 'complete_sent_prompt_matches_prepared':sub['dispatch']['serviceAccepted'] and sub['dispatch']['turnId']=='174b2eda-9e1c-4f1a-b342-b082f21e4586' and Path(sub['dispatch']['sentPromptPath']).read_text(encoding='utf-8').strip()==Path(sub['dispatch']['preparedCombinedPath']).read_text(encoding='utf-8').strip() and sha(Path(sub['dispatch']['sentPromptPath']))==sub['dispatch']['sentPromptSha256'],
 'original_exact_packet_preserved':sha(Path(sub['packetPath']))==sub['packetSha256'] and all(sha(Path(x['path']))==x['sha256'] for x in sub['parts']),
 'source_reviews_preserved':all(sha(G/k)==v for k,v in sub['reviewSourceHashes'].items()),
 'pipeline_42_checks_89040_boundaries':pipeline['status']=='PASS' and len(pipeline['checks'])==42 and pipeline['accessBoundaryCases']==89040 and pipeline['operationalDrafts']==269 and pipeline['unfinishedSpells']==579 and not pipeline['errors'],
 'low_rank_unfinished_144':len(low)==144,
 'no_unfinished_evocation_through_rank2_access':not evoc0,
 'previous_control_guide_preserved_as_exact_prefix':hashlib.sha256((R/'docs/mechanics/CONTROL_STATES_PLAYTEST.md').read_bytes()[:sub['controlGuidePrefixBytes']]).hexdigest()==sub['controlGuidePrefixSha256']==sha(A/'CONTROL_STATES_BEFORE_FROST_NOVA.md'),
 'wider_coverage_not_closed':len(coverage['aspects'])==75 and sum(s['closure']=='closed' for s in coverage['aspects'])==1,
 'cosmology_remains_post_push_open':next(s for s in coverage['aspects'] if s['id']=='DD-50')['workPhase']=='post-github-push' and next(s for s in coverage['aspects'] if s['id']=='DD-50')['closure']!='closed'
}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'functionalRepairFields':sorted([list(x) for x in changed]),'operational':269,'unfinished':579,'unfinishedWithClassRank0To3':len(low),'unfinishedEvocationRank0To2':len(evoc0),'limits':'Exact manuscript, source/class preservation, schema and common-price/access checks; no effect-runtime execution, human balance, source-variant closure, whole-game approval, GitHub push or cosmology review.','sourceDeletion':False,'githubPushed':False}
dump(A/'EVOCATION_RANK2_PROMOTION_CHECK.json',result);assert all(checks.values()),checks
sp=R/'docs/mechanics/EVOCATION_RANK2_REVIEW_STATUS.json';s=read(sp);s.update(pipelineValidation='PASS',pipelineSummary='42 checks /89,040 class-level access boundaries /zero issues',promotionVerification='docs/audit/2026-10-08/full-game/EVOCATION_RANK2_PROMOTION_CHECK.json',unfinishedWithClassRank0To3=144,unfinishedEvocationRank0To2=0,nextWork='Continue dependency-ordered character creation and advancement, equipment and expedition-to-Haven flow alongside larger catalog batches. Full scope and post-push-only cosmology remain unchanged.');dump(sp,s)
sub.update(status='promoted and verified;21 preservation checks and42 pipeline checks PASS',promotionVerification=s['promotionVerification']);dump(A/'EVOCATION_RANK2_EXACT_SUBMISSION.json',sub)
print(json.dumps(result,indent=2))
