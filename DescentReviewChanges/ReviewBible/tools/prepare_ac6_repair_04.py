"""Preserve return03 and prepare a bounded joint repair request; no rule adoption."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
I=A/'ac6-full-current-review-03-input'
O=A/'ac6-full-review-03-return'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(b): return hashlib.sha256(b).hexdigest()
def binding(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':digest(b)}
def save(p,obj):
    assert not p.exists(), str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
src=read(I/'CURRENT_REVIEW_INPUT.json')
model=read(O/'SPELLS_MODEL.json')
cases=read(O/'CASEBOOK.json')
old_cases={c['id']:c for c in src['currentExamples']}
new_cases={c['id']:c for c in cases['cases']}
nexus=next(v for v in src['records'] if v['spellId']=='alignment-nexus')
issues=[
 {'id':'AC6-L04-01','severity':'blocking-completeness','title':'Nexus mode procedures exist only in retained history',
  'evidence':{'returnedCurrentProcedure':model['spells'][13]['procedure'],
              'completeSubmittedModes':nexus['completePriorDraftRecord']['modes']},
  'finding':'The returned current procedure supplies access/alignment/family/readout and short currentIntegration notes, but no complete operative Divination6/Conjuration8 modes. The original submission also put these full modes outside its short procedure in completePriorDraftRecord.modes; this packaging gap needs explicit repair, not a false assertion that all current procedure leaves being printed proves completeness. Formation geometry, durations, destination knowledge, receiving placement, transit failures, physical attack route, suppression/closure and removal remain historical-only.',
  'proposedRepair':'Promote both complete mode procedures into the current spell record with current corrections, and reproduce them in both chapters. Keep the original full modes unchanged in history. Validate that current references target the promoted modes, never rely on an old proposal as implicit operative authority.'},
 {'id':'AC6-L04-02','severity':'blocking-contradiction','title':'Faction Army profile disagrees with its current procedure',
  'evidence':{'returnedProfile':model['profiles']['AC6-FACTION-SOLDIER-PROFILE-01'],
              'returnedProcedure':model['spells'][12]['procedure']},
  'finding':'The top-level profile gives AC16 and fixed attack +8; the current procedure specifies AC14 and original source-owner current spell attack, with six abilities, mass160lb, PB saves and hand/load limits missing from that top-level profile. These are two incompatible operative stat blocks, not merely preserved historical metadata.',
  'proposedRepair':'Retain the submitted AC14 and source-owner current spell attack unless you explicitly argue for a new numerical change. Make one complete authoritative profile and all procedure/chapter/case copies agree. A Wizard11 INT18/PB4 fixture can legitimately use +8, but the universal profile cannot hard-code that fixture value. Preserve the incorrect return03 profile as history.'},
 {'id':'AC6-L04-03','severity':'blocking-clock','title':'Portal examples silently use 60 seconds instead of the proposed 600',
  'evidence':{'submittedConjurationOpeningRule':nexus['completePriorDraftRecord']['modes']['Conjuration8']['openings'],
              'returnedClockLedgers':{k:new_cases[k]['clockLedger'] for k in ['NX-D01','NX-D05','NX-D06','NX-D07','NX-D08','NX-D09','NX-D10','NX-D11','AC6-RX02']}},
  'finding':'Divination6 has a proposed 60-second concentration lifetime; Conjuration8 has a proposed 600-second concentration lifetime. Multiple returned Conjuration8 cases say deadline60 and NX-D01 says eachMaxSeconds60, without a disposition intentionally shortening the portal.',
  'proposedRepair':'Restore Divination6=60 and Conjuration8=600 in current modes, every applicable case and both chapters. Use actual formation-relative absolute deadlines in finite examples. If a shorter portal is deliberately proposed instead, identify it as a consequential new change for joint review rather than treating it as preserved source.'},
 {'id':'AC6-L04-04','severity':'blocking-current-text','title':'Current procedures retain superseded rules and lose some lifecycle clauses',
  'evidencePointers':['SPELLS_MODEL.json#/spells/6/procedure','SPELLS_MODEL.json#/spells/12/procedure','SPELLS_MODEL.json#/spells/4/procedure/suppressionAndEnding','SPELLS_MODEL.json#/spells/4/procedure/currentPanelPrecision','SPELLS_MODEL.json#/spells/10/procedure/healingNullAndEnding'],
  'finding':'Air Pet and Army current procedures still tell readers full suppression ends bodies, then append the chosen same-body pause override; they also still call already accepted AC5 pending. Planar Barrier says intersected panels inactive and occupied panels pending, then adds exact clipped-portion rules at the same operative level. Greater Ally replacement healingNullAndEnding dropped the earlier explicit caster regular-turn no-Action dismissal permission and independent legal relocation keeps source/clock clause while still invoking dismissal.',
  'proposedRepair':'Write one clean current rule for each affected topic and copy it into both chapters. Preserve all superseded exact text in history, already present in completePriorDraftRecord/previousCurrentVersion. Explicitly distinguish qualification-change whole-panel pending from local-suppression clipped-portion pending if retaining that difference. Restore or explicitly disposition substantive removed lifecycle clauses; do not silently omit them.'},
 {'id':'AC6-L04-05','severity':'blocking-scenario-coverage','title':'Several preserved case IDs now describe different or weaker scenarios',
  'evidence':{k:{'submitted':old_cases[k],'returnedCurrent':{f:v for f,v in new_cases[k].items() if f!='previousCurrentVersion'}} for k in ['NX-D03','NX-D04','NX-D09','PB-D03','GA-D01']},
  'finding':'NX-D03 no longer tests hostile match/unknown axis. NX-D04 replaces the two-source +7→+9 no-stacking/original-reroll-modifier example with a generic coin statement. NX-D09 replaces alias/hidden destination failures with Paladin travel restrictions (already separately covered by RX02). PB-D03 loses its concrete panel/body arithmetic instead of correcting it for spherical clipping. GA-D01 loses actual attack/damage arithmetic. Retaining old IDs and history is preservation, not fulfillment of each current scenario.',
  'proposedRepair':'Restore each named scenario as a complete current finite example, retaining useful newer examples separately if needed. Review all 51 prior current cases against their original required scenario, and retain actual numbers/outcomes where supplied. For revised PB-D03 provide an actual suppressing sphere, fixed panels, body and exact clipped occupancy calculation. For known versus hidden invalid destinations, distinguish free preflight rejection from paid intervening/hidden failure. Report scenario-by-scenario coverage without claiming these authored examples are runtime tests.'},
 {'id':'AC6-L04-06','severity':'requires-explicit-new-choice','title':'Suppressed airborne Pet has unresolved Hover/support behavior',
  'evidence':{'suppressionRule':model['sharedRules']['AC6-SUMMON-SUPPRESS-01'],
              'case':{k:v for k,v in new_cases['AC6-N15'].items() if k!='previousCurrentVersion'}},
  'finding':'AC6-N15 places Air Pet hovering20ft, then fully suppresses it and resumes the same state. The shared suppression rule suppresses intrinsic traits and says same legal position/state; ordinary NullDisabled retains Hover, but full antimagic is a different predicate. Neither current text nor worked case resolves whether Hover survives this suppression or actual Falling begins.',
  'proposedRepair':'Confer explicitly: either give this Air Pet a narrow NEW retained passive Hover exception during same-body suppression, or apply actual Falling when its intrinsic Hover is suppressed. Do not silently freeze falling or infer ground support. State and work the chosen physical lifecycle with actual clock/position; keep it scoped to this summon, without planar/soul/biology claims.'}
]
report={
 'id':'AC6-LOCAL-SUBSTANTIVE-REPAIR-04', 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'Six concrete independent findings; return03 remains an unadopted replacement candidate. This is not a claim that all remaining semantics are verified.',
 'returnArchive':binding(A/'DD_AC6_Full_Review_03_Return.zip'),
 'structuralCheck':binding(A/'AC6_FULL_REVIEW_03_INDEPENDENT_STRUCTURAL_CHECK.json'),
 'structuralResult':{'checks':725,'failures':0,'sources':103,'identities':14,'placements':16,'currentCases':55,'currentPointerOccurrencesChecked':169,'pointerScope':'Current spell and case surfaces; GPT reported319 for its broader/different traversal. Counts are not represented as the same traversal.'},
 'positiveFindings':['Original source/access records and full prior spell/case versions are intact.','Wizard Dispel remains the actual rank3 spell; the negative antimagic/Seal operation conclusion is consistent with accepted AC5.','The new interruption uses actual Soldier/cards/34 Net Bolt (Action; one cartridge; one encounter use), a source-qualified readied damage route.','The actual Forge recipe42/628 work and protected later cycle principal remain present.'],
 'issues':issues,
 'remainingReviewNotes':['Chain Arc N17 needs explicit actual distance/occupied-body convention and complete geometry before its candidate arrays can be treated as independently verified. Do not omit an eligible hidden/ally body or manufacture an unsupported immediate-removal source.'],
 'requiredReturn':'DD_AC6_Repair_04_Return.zip with REGISTER.json, SPELLS_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_REVIEW.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json; complete replacement, all six findings explicitly dispositioned, no automatic adoption.',
 'currentOrdinaryCounts':{'reviewed':451,'pending':397},'newSpellAdoptions':0,
 'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyCanonModified':False,'wholeGameApproved':False,'publicationApproved':False
}
rp=A/'AC6_LOCAL_SUBSTANTIVE_REPAIR_04.json'; save(rp,report)
target=A/'DD_AC6_Repair_04.zip'; assert not target.exists()
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in ['CURRENT_REVIEW_INPUT.json','SOURCE_MANIFEST.json']:
        z.write(I/name,name)
    for e in read(I/'SOURCE_MANIFEST.json')['bindings']:
        z.write(I/'sources'/e['path'],'sources/'+e['path'])
    for p in sorted(O.iterdir()):
        if p.is_file(): z.write(p,'return03/'+p.name)
    z.write(rp,rp.name)
    z.write(A/'AC6_FULL_REVIEW_03_INDEPENDENT_STRUCTURAL_CHECK.json','AC6_FULL_REVIEW_03_INDEPENDENT_STRUCTURAL_CHECK.json')
archive=binding(target)
request=(
 f"I independently checked your AC6 return03: 725 structural/preservation checks passed, including all103 frozen source hashes,14 source/access identities,16 placements,22 original texts and all51 prior case histories. No AC6 adoption yet.\n\n"
 f"Please review attached DD_AC6_Repair_04.zip ({archive['bytes']} bytes; SHA256 {archive['sha256']}). It contains the exact103 sources, original current input, your eight unchanged return03 files, independent structural audit, and AC6_LOCAL_SUBSTANTIVE_REPAIR_04.json with six concrete findings and evidence.\n\n"
 "Resolve AC6-L04-01..06 explicitly: promote BOTH complete Nexus modes from completePriorDraftRecord.modes into current operative text (our prior input also hid this detail outside its short procedure); reconcile Army profile AC16/fixed+8 with procedure AC14/owner spell attack; restore Nexus Conjuration8 600-second versus Divination6 60-second clocks; remove superseded destruction/pending-AC5 text from current rules while preserving exact history and lifecycle permissions; restore the actual scenarios/numeric outcomes under NX-D03/D04/D09, PB-D03, GA-D01 and verify all prior51 scenario obligations; decide Air Pet Hover versus actual Falling under full suppression explicitly. Also verify Chain Arc N17 actual range/body geometry rather than only list fair dice.\n\n"
 "We agree the actual Net Bolt source is Action/cartridge/encounter-use and can supply the Ready interruption; keep its real restrictions. Keep the legal Bittersap example, negative Seal removal conclusion, actual Forge recipes and protected conversion cost. Use complete clean current procedures, both Nexus modes and complete consistent profiles in BOTH chapters. Keep all source/access/history exact; keep all55 current IDs in order and preserve return03 versions where revised. Do not substitute unrelated examples for named scenarios.\n\n"
 "Return DD_AC6_Repair_04_Return.zip with the same eight root files and explicit six-issue dispositions, finite revised examples, actual source/pointer checks and exact output hashes. No scripts need execution. This remains an unadopted authored candidate, not runtime/human/numerical balance/cosmology-canon/whole-game/publication approval. Confer on substantive choices rather than silently accepting my proposal."
)
req=A/'AC6_REPAIR_04_REQUEST.txt'; assert not req.exists(); req.write_text(request+'\n',encoding='utf-8')
receipt={'id':'AC6-REPAIR-04-PREPARATION','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Prepared locally, not yet submitted','archive':archive,'request':binding(req),'issues':binding(rp),'newSpellAdoptions':0}
save(A/'AC6_REPAIR_04_PREPARATION.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
