"""Stage complete advanced-trade source files while gathering exact review runs.

This is unsent preparation. Dispatch must recheck current reviewed interfaces;
pending gathering candidates are not promoted into source authority by this file.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,re,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 target=A/'ADVANCED_CRAFT_FILE_HANDOFF_PREPARATION.json';assert not target.exists()
 e=read(A/'ADVANCED_CRAFT_SOURCE_PREPARATION.json');parts=read(A/'ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json');source=R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';book=G/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
 raw=read(source);recipes=[r for r in raw['recipes'] if r['skill'] in e['trades']]
 checks=[]
 def check(n,v):checks.append({'name':n,'pass':bool(v)})
 check('All167 exact current original records and source indices',recipes==e['recipes'] and len(recipes)==167 and all(raw['recipes'][e['sourceIndices'][r['id']]]==r for r in recipes))
 check('Original mechanical V4 and public book bytes unchanged',sha(source)==e['sourceSha256'] and sha(book)==e['bookSha256'])
 check('All4 selected version sources retain original bytes',all(sha(G/e['versionAudit']['sourcePaths'][k])==h for k,h in e['versionAudit']['sourceHashes'].items()))
 check('All5 original prepared packets retain exact bytes',len(parts['parts'])==5 and all(sha(A/p['file'])==p['sha256'] for p in parts['parts'].values()))
 check('Four actual trade counts',dict(Counter(r['skill'] for r in recipes))=={'Enchanting':43,'Rune Carving':41,'Scribing':40,'Tinkering':43})
 check('Visibility100/7/60',dict(Counter(r['visibility'] for r in recipes))=={'public':100,'restricted':7,'director-only':60})
 with zipfile.ZipFile(book) as z:xml=E.fromstring(z.read('word/document.xml'))
 w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in xml.iter(w+'p')]
 check('All100 complete V5 bindings/600 paragraph texts still exact',len(e['publicBookBindings'])==100 and sum(len(b['paragraphs']) for b in e['publicBookBindings'])==600 and all(ps[p['index']]==p['text'] for b in e['publicBookBindings'] for p in b['paragraphs']))
 scenario=A/'ADVANCED_CRAFT_REVIEW_SCENARIOS.md';scenario_text=scenario.read_text(encoding='utf-8')
 check('All50 finite source scenarios retained',len(set(re.findall(r'(?:AC|EN|RC|SC|TI)-\d\d',scenario_text)))==50)
 check('758 occurrences/90 reusable/6 consumed tools/172 catalysts',sum(len(r['components']) for r in recipes)==758 and len(e['reusableToolOccurrences'])==90 and len(e['consumedToolOccurrences'])==6 and len(e['catalystOccurrences'])==172)
 check('Current reviewed trade binding and original numeric audit unchanged',sha(G/e['reviewedTradeBindings']['file'])==e['reviewedTradeBindings']['sha256'] and sha(G/e['numericAuditReference']['file'])==e['numericAuditReference']['sha256'])
 check('All167 INT/false field restrictions retained',all(r['workRequirements']['fieldCraftable'] is False and r['craftingCheck']['abilityOptions']==['Intelligence'] for r in recipes))
 check('One null work-hour record and18 automaton gaps retained',len(e['sourceHourNulls'])==1 and len(e['automatonMissingAttackFields'])==18)
 assert all(c['pass'] for c in checks),[c['name'] for c in checks if not c['pass']]
 files={source,book,scenario,A/'ADVANCED_CRAFT_SOURCE_PREPARATION.json',A/'ADVANCED_CRAFT_SOURCE_AUDIT.md',A/'ADVANCED_CRAFT_SOURCE_PACKET_STATUS.json',G/e['reviewedTradeBindings']['file'],G/e['numericAuditReference']['file']}
 files|={A/p['file'] for p in parts['parts'].values()}|{G/p for p in e['versionAudit']['sourcePaths'].values()}
 guides=['CRAFTING_HARVEST_PLAYTEST.md','CRAFTING_TRADE_REFERENCE.md','CORE_RESOLUTION_PLAYTEST.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','GAMEPLAY_LOOP_CANON.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','ALCHEMY_RECIPE_PLAYTEST.md','HERBALISM_RECIPE_PLAYTEST.md','COOKING_RECIPE_PLAYTEST.md','POISONCRAFTING_RECIPE_PLAYTEST.md','BLACKSMITHING_RECIPE_PLAYTEST.md','LEATHERWORKING_RECIPE_PLAYTEST.md','TAILORING_RECIPE_PLAYTEST.md','JEWELCRAFTING_RECIPE_PLAYTEST.md','FISHING_RECIPE_PLAYTEST.md']
 files|={R/'docs/mechanics'/n for n in guides}
 files|={R/'data/playtest/equipment_acquisition_candidate.json',R/'tools/prepare_advanced_craft_source_audit.py',R/'tools/prepare_advanced_craft_source_packets.py',Path(__file__).resolve()}
 for p in files:assert p.is_file(),p
 baseline={rel(p):sha(p) for p in files}
 report={'status':'PASS complete-source file handoff preparation; UNSENT; review-interface refresh required before dispatch','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':checks,'checkCount':len(checks),'sourceRecipes':167,'publicBookBindings':100,'publicParagraphs':600,'sourceScenarios':50,'tradeCounts':dict(Counter(r['skill'] for r in recipes)),'componentOccurrences':758,'sourceNullsPreserved':True,'originalFivePartFilesPreserved':True,'currentSourceAndRuleHashes':baseline,'gatheringExactReviewPending':True,'gatheringCandidatesTreatedAsApprovedAuthority':False,'dispatchRequirement':'First inspect the actual gathering exact verdict, apply its required changes and refresh any affected current reviewed interfaces. Verify these source/rule hashes before upload. Do not dispatch automatically while that review is active.','recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'literal restrictions retained, no interpretation; post-verified-push review only'}
 evidence=A/'ADVANCED_CRAFT_FILE_HANDOFF_REBASE_CHECK.json';dump(evidence,report);files.add(evidence)
 readme='''# Advanced crafting — complete source handoff, prepared but not sent

This is a source-authoring packet for the final167 crafting formulas:43 Enchanting,41 Rune Carving,40 Scribing and43 Tinkering. It does not approve effects. The original five prepared text packets remain unchanged and are included, but their old reviewed totals and references to a pending Tailoring conference are historical. The fresh rebase check records the current sources/rules and is controlling for this preparation stage.

The audit folder docs/audit/2026-10-08/full-game/ contains ADVANCED_CRAFT_SOURCE_PREPARATION.json with all167 complete source objects,100 exact six-paragraph V5 bindings, all758 component occurrences, selected historical field differences,18 automaton attack-profile gaps,22 Scribing use questions, five distinct custom profiles and the one null work-hour source. The50 finite questions are in ADVANCED_CRAFT_REVIEW_SCENARIOS.md. All original source variants, the actual V5 DOCX and relevant current governing guides are included beneath their real repository-relative paths. FILE_MANIFEST.json gives byte hashes and sizes.

No new operational choice is made here. Enchanting dawn recharge is not imported into Rune Carving; Scribing use counts are not silently collapsed to one; automaton attacks/speeds are not invented from their names; the one-year/null-hour recipe is not normalized; consumed tools and172 catalyst occurrences remain literal. The four credentials are artisan trades, but that does not grant a finished object's use permissions. Actual magical base compatibility, stacking, triggers, recharge ownership, control/service, origin, material handling and special effects need the named source decisions before exact cards are authored.

Literal references and prohibitions involving cosmology are preserved as source text. This is not permission to interpret cosmology or alter Silent Ones/Heartcell/Matrix lore. The user's careful cosmology review remains after the authorized GitHub push and remote verification. Missing actual acquisition, anatomy or special handling is not supplied by a name or price.

Before dispatch: inspect and integrate the separate pending gathering exact verdict, refresh affected reviewed interfaces and validate the recorded hashes. Gathering candidates are not included as approved authority here. Do not interrupt that active review or infer a result from this prepared archive. The review request itself remains to be finalized against that actual state. No source deletion, recipe promotion or push is performed by this preparation.
'''
 zip_path=A/'DD_Advanced_Craft_167_Source_Prepared_v1.zip';assert not zip_path.exists()
 manifest={rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
 with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.writestr('README_SOURCE_REVIEW.md',readme.encode('utf-8'));z.writestr('FILE_MANIFEST.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
  for p in sorted(files,key=rel):z.write(p,rel(p))
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None and len(z.namelist())==len(manifest)+2==len(set(z.namelist()))
  assert all(hashlib.sha256(z.read(p)).hexdigest()==v['sha256'] for p,v in manifest.items())
 result={**report,'bundleFile':zip_path.name,'bundleSha256':sha(zip_path),'bundleBytes':zip_path.stat().st_size,'payloadFiles':len(manifest),'zipRoundtripVerified':True,'sent':False};dump(target,result)
 print(json.dumps({k:result[k] for k in ['status','checkCount','sourceRecipes','publicBookBindings','bundleFile','bundleBytes','payloadFiles','sent','recipesApproved']}))

if __name__=='__main__':main()
