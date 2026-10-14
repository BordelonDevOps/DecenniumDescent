from pathlib import Path
import json,hashlib,sys
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True)
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.path.insert(0,str(R/'tools'));from build_spell_playtests import FIELDS
sub=read(A/'EVOCATION_CANTRIP_EXACT_SUBMISSION.json');conference=read(A/'EVOCATION_CANTRIP_CONFERENCE_SUBMISSION.json')
parts=[json.loads((A/f'CODEX_EVOCATION_CANTRIP_EXACT_REVIEW_PART{n}.txt').read_text(encoding='utf-8').split(f'\nPART {n} OF 4\n',1)[1]) for n in range(1,5)]
before={}
for part in parts:
 for row in part['cards']:
  s={**parts[0]['defaults'],**row}
  for k,v in list(s.items()):
   if isinstance(v,dict) and 'concat' in v:s[k]=''.join(parts[0]['sharedFragments'][z['shared']] if isinstance(z,dict) else z for z in v['concat'])
  before[s['id']]=s
cards={s['id']:s for s in read(D/'candidate_evocation_cantrips.json')['spells']};sources={s['id']:s for s in read(D/'candidate_evocation_cantrips_sources.json')['spells']}
catalog=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in catalog}
selected=[i for v in read(D/'selected_sources.json').values() for i in v]
prior={s['id']:s['operational'] for s in catalog if s['operational'] and s['id'] not in cards}
repairs=read(A/'EVOCATION_CANTRIP_EXACT_REPAIR_LOG.json')['changes']
changed={(i,f) for i in cards for f in FIELDS if before[i][f]!=cards[i][f]}
expected={(x['id'],x['field']) for x in repairs}
text=(R/'docs/mechanics/SPELL_PLAYTEST_STARTER.md').read_text(encoding='utf-8');rendered=True
for i,s in cards.items():
 section=text.split(f'<a id="spell-{i}"></a>',1)[1].split('<a id="spell-',1)[0]
 rendered &= all(s[f].replace('|','/') in section for f in FIELDS if isinstance(s[f],str))
pipeline=read(R/'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json');coverage=read(R/'data/playtest/game_development_coverage.json')
low=[s for s in catalog if not s['operational'] and any(x['rank']<=3 for x in s['classAccess'].values())]
evoc0=[s for s in catalog if not s['operational'] and any(x['rank']==0 and x['school']=='Evocation' for x in s['classAccess'].values())]
checks={
 'twelve_promoted_once':len(cards)==12 and all(selected.count(i)==1 and by[i]['operational'] for i in cards),
 'only_exactly_documented_review_repairs':changed==expected and all(before[x['id']][x['field']]==x['before'] and cards[x['id']][x['field']]==x['after'] for x in repairs),
 'candidate_batch_identical':(D/'candidate_evocation_cantrips.json').read_bytes()==(D/'batch_evocation_cantrips.json').read_bytes(),
 'fourteen_placements_and_core_blocks':sum(len(s['sourcePlacements']) for s in cards.values())==sum(len(s['sourceCoreEntries']) for s in cards.values())==14,
 'exact_source_evidence_and_aliases':all(cards[i]['sourcePlacements']==sources[i]['sourcePlacements']==by[i]['source']['original']['placements'] and cards[i]['sourceCoreEntries']==sources[i]['sourceCoreEntries']==by[i]['source']['coreEntries'] and sources[i]['possibleHistoricalAliases']==by[i]['source']['possibleHistoricalAliases'] for i in cards),
 'all_actual_class_access_preserved':all(cards[i]['classAccessEvidence']==sources[i]['classAccess']==by[i]['classAccess'] for i in cards),
 'all_848_ids_936_placements_retained':len(catalog)==len(by)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936,
 'all_functional_fields_rendered_exactly':rendered and all(all(cards[i][f]==by[i]['operational'][f] for f in FIELDS) for i in cards),
 'all_237_prior_operational_records_unchanged':len(prior)==237 and hashlib.sha256(compact(prior).encode()).hexdigest()==sub['previousOperationalSha256'],
 'all_frozen_source_and_class_files_unchanged':all(sha(R/k)==v for k,v in conference['frozenSourceAndClassFiles'].items()),
 'raw_source_hash_ledger_preserved':read(R/'data/playtest/spell_sources/source_hashes.json')==sub['sourceHashLedgerBefore'] and all(sha(R/x['path'])==x['sha256'] for x in sub['sourceHashLedgerBefore']),
 'frozen_class_rules_unchanged':sha(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md')==sub['classRulesSha256Before']=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81',
 'four_actual_delivered_parts_match_prepared':len(sub['dispatch']['attachments'])==4 and all(Path(x['path']).read_text(encoding='utf-8-sig').rstrip()==Path(sub['parts'][n]['path']).read_text(encoding='utf-8').rstrip() and sha(Path(x['path']))==x['sha256'] for n,x in enumerate(sub['dispatch']['attachments'])),
 'original_exact_packet_preserved':sha(Path(sub['packetPath']))==sub['packetSha256'] and all(sha(Path(x['path']))==x['sha256'] for x in sub['parts']),
 'source_reviews_preserved':sha(G/sub['sourceConference'])==sub['sourceConferenceSha256'] and sha(G/sub['authoringClarification'])==sub['authoringClarificationSha256'],
 'pipeline_42_checks_89040_boundaries':pipeline['status']=='PASS' and len(pipeline['checks'])==42 and pipeline['accessBoundaryCases']==89040 and pipeline['operationalDrafts']==249 and pipeline['unfinishedSpells']==599 and not pipeline['errors'],
 'low_rank_unfinished_164':len(low)==164,
 'no_unfinished_evocation_cantrip_access':not evoc0,
 'wider_coverage_not_closed':len(coverage['aspects'])==75 and sum(s['closure']=='closed' for s in coverage['aspects'])==1,
 'cosmology_remains_post_push_open':next(s for s in coverage['aspects'] if s['id']=='DD-50')['workPhase']=='post-github-push' and next(s for s in coverage['aspects'] if s['id']=='DD-50')['closure']!='closed'
}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'functionalRepairFields':sorted([list(x) for x in changed]),'operational':249,'unfinished':599,'unfinishedWithClassRank0To3':len(low),'unfinishedEvocationCantrips':len(evoc0),'limits':'Exact manuscript, source/class preservation, schema and common-price/access checks; no effect-runtime execution, human balance, source-variant closure, whole-game approval, GitHub push or cosmology review.','sourceDeletion':False,'githubPushed':False}
dump(A/'EVOCATION_CANTRIP_PROMOTION_CHECK.json',result);assert all(checks.values()),checks
sp=R/'docs/mechanics/EVOCATION_CANTRIP_REVIEW_STATUS.json';s=read(sp);s.update(pipelineValidation='PASS',pipelineSummary='42 checks /89,040 class-level access boundaries /zero issues',promotionVerification='docs/audit/2026-10-08/full-game/EVOCATION_CANTRIP_PROMOTION_CHECK.json',unfinishedWithClassRank0To3=164,unfinishedEvocationCantrips=0,nextWork='Continue twelve rank-one Evocation source identities. Broader runtime, human balance, whole-game flow and GitHub delivery remain open.');dump(sp,s)
sub.update(status='promoted and verified;20 preservation checks and42 pipeline checks PASS',promotionVerification=s['promotionVerification']);dump(A/'EVOCATION_CANTRIP_EXACT_SUBMISSION.json',sub)
print(json.dumps(result,indent=2))
