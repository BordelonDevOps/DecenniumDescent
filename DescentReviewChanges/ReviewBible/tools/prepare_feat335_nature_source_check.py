"""One-use source packet for Nature Whisper classification and casting interfaces."""
from pathlib import Path
from datetime import datetime, timezone
import json, zipfile
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'

def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    root=A/'feat335-nature-source-check-01-input';archive=A/'DD_FEAT335_Nature_Source_Check_01.zip'
    receipt=A/'FEAT335_NATURE_SOURCE_CHECK_01_PREPARATION.json'
    assert not root.exists() and not archive.exists() and not receipt.exists();root.mkdir()
    questions=[
        {'id':'NWQ-01','question':"Classify the exact Nature's Whisper card and its SUP09 borrowed activation: ordinary ranked spell, class spell or magical nonspell technique? Current normalized spellRank is null and no spell tag/rank is present; originalText says minor nature spell, SUP09 says apply actual minorWeave/sharedcasting restrictions. Shared integration says unassigned rank is not zero and RP expenditure alone does not establish Counterspell eligibility. Give a source-bound KEEP interpretation or minimal explicit NEW completion, preserving originalText and the real1RP cost. Do not import another same-name spell or silently assign rank0/1, a Ranger repertoire or donor class engine."},
        {'id':'NWQ-02','question':'Specify required actual components/channel and physical activation predicates. Current card has Action/1RP/natural terrain within15ft/minute/Recharge3 but no V/S/F block. Does Silence, no free hand or absent focus prohibit activation, distinct from the feat donor needing to perceive the borrower signal? If not specified, make a minimal NEW complete procedure rather than claiming a historical default. The borrower uses an existing legal personal RP pool and own stats; donor pays nothing.'},
        {'id':'NWQ-03','question':'Bind Dissonance, Refrain/name history, strain surcharges, Fracture and actual class cadence hooks for this exact native/borrowed activation. The local positive fixture uses Bard4 personalRP but has only an unexecuted actualMinorWeaveClearance boolean. What actual history/resource updates and ability operand are required? Do not borrow Ranger Track Target/Hit Chain/stabilization or invent a casting provider, rank or pool. Resolve separately whether this magical activation prevents idle-turn Dissonance recovery and whether paid interruption preserves its start costs/history.'},
        {'id':'NWQ-04','question':'Give the finite declare/pay/resolve and later-one-check boundaries: actual source-permitted interruption/Counterspell scope, readiness if the existing generic rule applies, when the one-minute rider begins, and whether the natural terrain/evidence area is fixed at activation or is an owner-carried15ft check benefit. The current card gives advantage on one actual Perception/Survival check, no free check, no automatic/through-total-cover revelation. State exactly when the one check is consumed, preserve failed rolls/costs, current real evidence and deadline, and disallow fabricated knowledge. Supply only concrete missing completions and focused acceptance cases; do not reopen unrelated full335 or cosmology decisions.'}
    ]
    questions_path=root/'QUESTIONS.json';save(questions_path,{'reviewId':'FEAT335-NATURE-SOURCE-CHECK-01','questions':questions,'sourceClassificationUnresolved':True})
    request=root/'REQUEST.txt'
    request.write_text('FEAT335-NATURE-SOURCE-CHECK-01\n\nFlora FLQ01–04 is now fulfilled locally using your exact amendments:101 reproduced reviewer checks,738 guarded propagation checks,189 finite checks/54 conditional histories covering all18 groups. Original114 report and earlier186 local version remain preserved and qualified; the current V2 corrects active-Flora versus capability for Verdant. The fulfillment receipt is included only for continuity, not a repeat-review request.\n\nVersatile Mastery now has362 bounded checks/38 conditional histories retaining all12 native-card cases and adding distinct attack/task/skill declare-pay-resolve interfaces. Its Nature Whisper positive remains explicitly conditional on an unimplemented actualMinorWeaveClearance premise. Do not call that a full casting test.\n\nPlease settle the four concrete QUESTIONS.json interfaces for this exact Nature Whisper source and its SUP09 borrowed procedure. Full current Ranger card/engine/manuscript, shared class/spell/component/Counterspell rules, candidate/contracts/SUP09, exact prior feat source decision and current local model/evidence are supplied. Inspect those sources, distinguish KEEP from explicit NEW completions, and provide guarded exact amendments only if necessary, plus finite follow-through expectations. A missing rank must not default to zero. The frozen historical originalText remains preserved.\n\nThis is a narrow source question, not the final full335 exact review, new general magic redesign, runtime/balance certification or cosmology review. Preserve paid costs, source identity and other completed decisions. If a specific source needed for a decision is absent, name it precisely. No generic unchanged resubmission after exact finite fulfillment.\n',encoding='utf-8',newline='\n')
    paths=[request,questions_path,
        R/'data/public/class_playtests/ranger.json',R/'docs/mechanics/classes/ranger.md',
        R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',
        R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
        R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A/'feat327-source-verdict/cohorts/HERITAGE_MUTATION.md',A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',
        R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json',
        R/'tools/feat335_borrowed_stunts.py',R/'tools/feat335_borrowed_transactions.py',R/'tools/feat335_borrowed_skill_transactions.py',
        R/'tools/spell_playtest_rules.py',A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json',A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_SCOPE.json',
        A/'FEAT335_FLORA_SOURCE_CHECK_01_FINITE_FULFILLMENT.json',A/'FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_SCOPE.json']
    def name(p):return p.name if p.parent==root else p.relative_to(G).as_posix()
    bindings={name(p):info(p) for p in paths}
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.writestr(name(p),p.read_bytes())
        z.writestr('PACKAGE_MANIFEST.json',json.dumps(bindings,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(paths)+1
        for p in paths:assert z.read(name(p))==p.read_bytes()
    save(receipt,{'id':'FEAT335-NATURE-SOURCE-CHECK-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'prepared-not-submitted','archive':info(archive),'questions':info(questions_path),'request':info(request),
        'payloads':len(paths),'sourceBindings':list(bindings.values()),
        'scope':'Exact Nature Whisper card/SUP09 classification, components, strain/history and declare/resolve/check interfaces only.',
        'sourceInformationDeleted':0,'candidateChanged':False,'fullFeatExactApproved':False,'cosmologyReviewed':False})
    print(json.dumps({'receipt':info(receipt),'archive':info(archive),'payloads':len(paths)}))

if __name__=='__main__':main()
