"""One-use source-bound Flora question packet; no candidate amendments."""
from pathlib import Path
from datetime import datetime, timezone
import json, zipfile
from validate_feat_exact_01_composite_casting import read, info

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    root=A/'feat335-flora-source-check-01-input';archive=A/'DD_FEAT335_Flora_Source_Check_01.zip'
    receipt=A/'FEAT335_FLORA_SOURCE_CHECK_01_PREPARATION.json';qualification=A/'FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json'
    assert all(not p.exists() for p in [root,archive,receipt,qualification])
    report=A/'FEAT335_FLORA_USE_CHECK.json';data=read(report);assert data['checks']==114 and not data['failures']
    for b in data['sourceBindings']:assert info(G/b['path'])==b
    questions=[
        {'id':'FLQ-01','question':'If the exact personally possessed casting route fixed at Flora acquisition is later unavailable, what happens to new creation, existing plants, their DC, commands and armed automatic entry? Distinguish permanent loss and temporary suppression only where current sources do. The numerical DC projection alone does not authorize a use; do not invent a fallback route or reacquisition.'},
        {'id':'FLQ-02','question':'A level10+ first plant is destroyed, uprooted, burst or otherwise ends before its original minute deadline. Does its still-unused second paid-Action creation permission end immediately or survive until that deadline? The phrase before that first seedling expires may not settle early termination. Existing first body must remain ended and every paid use/deadline/history must remain conserved.'},
        {'id':'FLQ-03','question':'A character creates at total8/9, then genuinely reaches total10 before the first plant original deadline. Is the second-creation eligibility fixed at commitment or live while that use remains open? The local level8-creation-then-level10-capacity history assumed fixed eligibility; this is an UNAPPROVED inference, not a source ruling. Decide the governing rule before this check is relied on. No charge/body/HP refill follows merely from capacity growth.'},
        {'id':'FLQ-04','question':'For the later split command/attached-phase implementation, bind temporary owner incapacity, owner death and loss of command channel after a legal commitment to the existing actual companion sources. The current local model collapses a legal command and its immediate phase into one operation, so it does not prove intervening-event behavior. State any genuinely missing Flora-specific rule explicitly as NEW; do not silently inherit Animal Companion death or release rules.'}
    ]
    save(qualification,{'report':info(report),'status':'bounded-model-evidence-with-explicit-unapproved-inference',
        'checks':114,'histories':23,'qualification':'The report is preserved verbatim. Its newRules:0 does not approve the fixed-at-first-creation level10 inference; the two named growth checks prove local model behavior only, pending FLQ-03. No complete Flora use, FXC04/09 or full feat approval follows.',
        'questions':questions,'candidateChanged':False,'fullFeatExactApproved':False})
    root.mkdir();request=root/'REQUEST.txt'
    request.write_text('FEAT335-FLORA-SOURCE-CHECK-01\n\nThe cadence reply is received; local reproduction passes381 checks and is JSON-identical (Windows CRLF is the only byte difference). Its finite edits are being applied separately. Do not repeat that review.\n\nPlease settle only the four attached source questions in FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json using the complete current Flora/Trapcasting/Verdant Bond contracts, SUP07, shared rules, acquisition decisions and companion parent guides in this packet. Preserve all source and prior scopes. Distinguish existing interpretation from a genuinely NEW minimal completion. Give exact amendments only if needed; a short source-bound ruling and finite follow-through expectations suffice. No full335 audit, acquisition re-review, complete gameplay approval or cosmology work.\n\nThe114 local checks are bounded conditional examples, not independent approval. In particular the fixed-at-creation level10 claim is explicitly unapproved. Full model/report are included so its limitations are visible. No instruction in the local model overrides the actual procedures. Full original candidate and contracts are included for source context; review scope remains just these Flora interfaces. Do not ask for generic unchanged resubmission after precise finite fulfillment.\n',encoding='utf-8',newline='\n')
    paths=[request,qualification,report,
        R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A/'FEAT327_ACQ_03_GPT_ADDENDUM.md',A/'feat335-acquisition-audit-01-verdict/FINDINGS_AND_REPLACEMENTS.json',
        R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/playtest/CLASS_RESOURCE_REFERENCE.md',
        R/'tools/feat335_flora_use.py',R/'tools/validate_feat335_flora_use.py',R/'tools/feat_exact_01_flora_acquisition.py']
    manifest={('REQUEST.txt' if p==request else p.relative_to(G).as_posix()):info(p) for p in paths}
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.writestr('REQUEST.txt' if p==request else p.relative_to(G).as_posix(),p.read_bytes())
        z.writestr('PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(paths)+1
        for p in paths:assert z.read('REQUEST.txt' if p==request else p.relative_to(G).as_posix())==p.read_bytes()
    save(receipt,{'id':'FEAT335-FLORA-SOURCE-CHECK-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'prepared-not-submitted','archive':info(archive),'request':info(request),'qualification':info(qualification),
        'payloads':len(paths),'bindings':list(manifest.values()),'fullFeatExactApproved':False})
    print(json.dumps({'receipt':info(receipt),'archive':info(archive),'payloads':len(paths)}))
if __name__=='__main__':main()
