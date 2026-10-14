"""Freeze the complete next conference after fulfilled TEX, preserving original V2 bytes."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def h(b):return sha256(b).hexdigest()
def entry(b):return {'bytes':len(b),'sha256':h(b)}
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=A/'DD_Expedition_Transport_Social_58_Source_v3.zip';assert not out.exists()
plan=load(A/'EXPEDITION_INTEGRATED_CONFERENCE_PLAN.json');add=load(A/'TEACHING_TEX_ADDENDUM_FULFILLMENT.json')
assert add['status'].startswith('FULFILLED') and add['failures']==0
prior=load(A/'TEACHING_TEX_EXACT_FULFILLMENT.json')
for rel,v in {**prior['finalArtifacts'],**prior['correctedCurrentCraftArtifacts'],**add['finalArtifacts']}.items():assert h((G/rel).read_bytes())==v['sha256'],rel
paths=set(plan['sourceFilesAtPreparation'])
extras=['EXPEDITION_INTEGRATED_CONFERENCE_PLAN.json','EXPEDITION_INTEGRATED_CONFERENCE_SCOPE.md','EXPEDITION_INTEGRATED_SCOPE_PREPARATION.json','TEACHING_TEX_ADDENDUM_FULFILLMENT.json','TEACHING_TEX_ADDENDUM_LOCAL_CHECKS.json','TEACHING_TEX_ADDENDUM_STATUS_PROOF.json','TEX_CONTROLLING_ADDENDUM_2026_10_11.md','DD_TEX_Controlling_Addendum_2026_10_11.zip','DD_Teaching_9_Exact_Verdict_and_Evidence.zip','DD_Teaching_Navigation_9_Exact_Verdict_and_Evidence.zip','TEACHING_TEX_NAVIGATION_UPDATE.json','GPT_REVIEW_CONTINUATION_HANDOFF.md']
paths.update('docs/audit/2026-10-08/full-game/'+x for x in extras)
for p in (A/'teaching-tex-controlling-addendum-files').iterdir():paths.add(p.relative_to(G).as_posix())
for p in (R/'tools').glob('*playtest_rules.py'):paths.add(p.relative_to(G).as_posix())
paths.update(add['finalArtifacts'])
paths.add('DescentReviewChanges/ReviewBible/tools/freeze_integrated_expedition_conference.py')
payload={rel:(G/rel).read_bytes() for rel in sorted(paths)}
v2=load(A/'EXPEDITION_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json');oldzip=A/v2['bundleFile']
assert h(oldzip.read_bytes())==v2['bundleSha256']
payload[oldzip.relative_to(G).as_posix()]=oldzip.read_bytes()
pairs=[]
with zipfile.ZipFile(oldzip) as z:
    mf=json.loads(z.read('FILE_MANIFEST.json'))
    assert len(mf)==194
    for rel,v in mf.items():
        b=z.read(rel);assert entry(b)==v,rel
        assert rel in payload,rel
        if payload[rel]!=b:
            historic='docs/audit/2026-10-08/full-game/expedition-before-v3/'+rel
            dest=G/historic;assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);payload[historic]=b
            pairs.append({'currentPath':rel,'originalV2':entry(b),'current':entry(payload[rel]),'preservedOriginalPath':historic,'scope':'Historical/current revisions are both retained. Current TEX/TEX-ADD and earlier completed authority controls only its stated interfaces.'})
summary={'scope':'Frozen integrated source conference; no source decision or promotion performed','originalV2Payloads':194,'originalV2Archive':{'path':oldzip.relative_to(G).as_posix(),**entry(oldzip.read_bytes())},'originalV2FilesUnchangedAtCurrentPaths':194-len(pairs),'historicalCurrentPairs':pairs,'allOriginalV2BytesPreserved':True,'priorPlanIsHistoricalPreparation':True,'questionCounts':plan['questionCounts'],'questions':plan['questions'],'proposalStillUnadopted':True,'TEXAddendumFulfilled':{'path':'docs/audit/2026-10-08/full-game/TEACHING_TEX_ADDENDUM_FULFILLMENT.json',**entry((A/'TEACHING_TEX_ADDENDUM_FULFILLMENT.json').read_bytes())},'ordinaryAuthoredCounts':{'reviewed':412,'pending':436},'recipeCounts':{'internalReviewed':687,'publicReviewed':433},'newApprovals':0,'sourceInformationDeleted':0,'runtimeImplemented':False,'cosmologyReviewed':False}
summrel='docs/audit/2026-10-08/full-game/EXPEDITION_INTEGRATED_V3_SOURCE_HISTORY.json';save(G/summrel,summary);payload[summrel]=(G/summrel).read_bytes()
readme='''# Integrated expedition, transport and social source conference — v3

This is a complete-file SOURCE-AUTHORING conference, not an exact-promotion request. Read docs/audit/2026-10-08/full-game/EXPEDITION_INTEGRATED_CONFERENCE_SCOPE.md first, then all58 original questions in EXPEDITION_INTEGRATED_V3_SOURCE_HISTORY.json. They comprise26 FL,12 SO,14 TR and6 RP-A questions. Supporting full books, current complete rules, source registries, whole class datasets/guides, runtime comparisons and the unadopted social proposal are included. Preserve source values; label genuinely new decisions.

The earlier TEX cb2 teaching contract and controlling TEX-ADD are now fulfilled in the actual repository. Their complete receipts and current files are supplied. Three additional internal/recharge replacements and provenance append passed399 local structural/preservation/link checks; TA-01–03 are authored source-based adjudications, not executed runtime. Carry all accepted corrections, including Shaman/Crimson capacities, stance instructions and cb2 Tinker disposition. The duplicate alternate package is preserved evidence only; the explicit addendum determines the three adopted operations. Old receipt hashes remain historical; use this FILE_MANIFEST for current bytes. No generic teaching re-review is requested.

Carry LAX/NWX/LRX and687 internal/433 public recipes. Current ordinary authored counts412/436. Existing complete class/feat/spell/creature comparison records do not gain approval here. Keep owner-locked twelve-character expedition structure and actual actors/time/resources. The SO ±3 score recommendation,24-hour checkpoint, outside-initiative Help and all proposed social procedures remain UNADOPTED for your explicit decision.

The original unsent expedition V2 archive and every changed original/current pair are retained. Its194 payloads are all verified; the source-history file identifies exact changes. Historical preparation reports and source extracts describe their own frozen revisions. Their old pending labels do not override current review receipts or current actual files, and their hashes must not be rewritten to match descendants. The258-file plan was unfrozen preparation before this dispatch; this archive's manifest is the authoritative current payload inventory.

Return a coherent decision for all58 questions, complete retained/replaced procedures and numerical profiles where needed, source-versus-NEW distinctions, finite examples and exact-candidate acceptance criteria. Include all29 named transport records plus Core services; do not silently narrow this to starter transport. The complete scope file specifies clock,Supply,camp,Pressure,route,extraction,retreat,transport,settlement,social/standing/faction and advancement outcomes. One complete objective-to-next-descent example is required for subsequent authoring.

All archive material is an internal owner/Director review packet, not a player distribution. Keep underlying cosmology, alignment meaning, sealed interpretations and soul-linked currency origins deferred; literal scheduling/specialist receipts are not new cosmology authority. Complete later catalogs/bestiary/Director integration and actual final joint whole-game flow before the authorized GitHub push. Verify remote commit before careful cosmology review. No deletion, runtime certification, human balance claim or additional owner-confirmation gate.
'''
payload['README_EXPEDITION_INTEGRATED_V3.md']=readme.encode('utf-8')
manifest={rel:entry(b) for rel,b in sorted(payload.items())}
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for rel,b in sorted(payload.items()):z.writestr(rel,b)
    z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(out) as z:
    assert len(z.namelist())==len(manifest)+1
    for rel,v in manifest.items():assert entry(z.read(rel))==v,rel
for rel in paths:assert entry((G/rel).read_bytes())==manifest[rel],rel
receipt={'status':'FROZEN complete integrated source conference; UNSENT','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':{'path':out.relative_to(G).as_posix(),**entry(out.read_bytes())},'payloadFiles':len(manifest),'manifest':manifest,'questions':58,'questionCounts':plan['questionCounts'],'originalV2PayloadsPreserved':194,'historicalCurrentPairs':pairs,'zipRoundtripVerified':True,'allCurrentFilesStableDuringFreeze':True,'sourceInformationDeleted':0,'newApprovals':0,'submitted':False,'runtimeImplemented':False,'cosmologyInterpreted':False}
save(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k not in ['manifest','historicalCurrentPairs']}))
