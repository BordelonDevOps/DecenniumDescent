"""Clarify existing Core/equipment rules while exact manuscript review is pending."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.relative_to(G).as_posix()

def main():
    receipt = A / 'ONBOARDING_WOUND_FIRST_AID_CLARIFICATIONS.json'
    backup = A / 'onboarding-before-wound-first-aid-clarification'
    assert not receipt.exists() and not backup.exists()
    prior = json.loads((A / 'ONBOARDING_STANCE_REFRAIN_CLARIFICATIONS.json').read_text(encoding='utf-8'))
    player = R / 'docs/playtest/NEWCOMER_PLAYER_GUIDE.md'
    director = R / 'docs/playtest/NEWCOMER_DIRECTOR_GUIDE.md'
    sources = [R / 'docs/mechanics' / n for n in ['CORE_RESOLUTION_PLAYTEST.md', 'HEALING_DEATH_PLAYTEST.md', 'EQUIPMENT_ITEM_PROCEDURES.md']]
    source_hashes = {rel(p): sha(p) for p in sources}
    changes = [
        (player,
         "Use an Action and a DC 10 Wisdom (Medicine) check to stabilize a living dying creature, or an Action and one healer's-kit use for automatic stabilization. A Stable creature remains at zero HP and unconscious, without death saves.",
         "To stabilize a living dying creature, use an Action and a DC 10 Wisdom (Medicine) check. Alternatively, use an Action, one available hand and one charge from an actual accessible healer's kit to automatically stabilize an adjacent living dying creature, as described in [equipment procedures](../mechanics/EQUIPMENT_ITEM_PROCEDURES.md). Stabilization clears both death-save counters. A Stable creature remains at zero HP and unconscious, without death saves."),
        (director,
         "When Instant Death does not apply, the actual positive-to-zero, half-maximum-damage or Maiming triggers require one Wound save for that damage event. Use the existing save, Injury and Critical procedures; a new Wound does not penalize its own creating save. The next failed Wound save after already having three Wounds is fatal.",
         "When Instant Death does not apply, make one Wound save for the damage event if the creature dropped from positive HP to zero, if twice the uncapped post-temporary-HP damage is at least effective maximum HP, or if the effect actually inflicts Maiming. Overlapping triggers still require only one save. Roll Constitution against **DC max(10, floor(post-temporary-HP damage / 2))**, applying the -1 penalty for each pre-event Wound. Maiming can require this save even when temporary HP absorbs all ordinary damage; zero post-temporary-HP damage uses DC 10. A new Wound cannot penalize its own creating save. Success adds no Wound; failure starting with fewer than three adds one, with a linked Injury on failure by 5 or more. Failure when already at three Wounds is fatal instead. Apply actual prevention and survival exceptions in the complete damage order.\n\nEach Wound also reduces the normal maximum Hit Dice recovered per beneficial long rest by one, to a minimum of zero; it does not reduce the HP rolled on each Hit Die. At three Wounds, Critical reduces Speed by 10 feet, minimum zero, and ordinary healing cannot raise HP above **max(1, effective maximum HP - 1)**. This ceiling neither reduces maximum HP nor removes existing HP. Wound treatment and linked Injuries use the [Core injury procedure](../mechanics/CORE_RESOLUTION_PLAYTEST.md#wounds-and-critical-state); ordinary HP healing does not remove them.")
    ]
    for p, old, new in changes:
        assert sha(p) == prior['currentManuscriptHashes'][rel(p)]
        assert p.read_text(encoding='utf-8').count(old) == 1
    before = {rel(p): sha(p) for p, _, _ in changes}
    for p, old, new in changes:
        saved = backup / rel(p)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, saved)
        p.write_text(p.read_text(encoding='utf-8').replace(old, new), encoding='utf-8')
    assert all(sha(G / n) == h for n, h in source_hashes.items())
    report = {'status': 'Source-confirmed teaching clarification; exact verdict pending',
              'appliedAtUtc': datetime.now(timezone.utc).isoformat(),
              'exactReviewTurnId': '89ebb4cd-5076-4984-af86-53549cf5f9c2',
              'priorClarifications': 'ONBOARDING_STANCE_REFRAIN_CLARIFICATIONS.json',
              'preservedPreviousHashes': before, 'backup': rel(backup),
              'currentManuscriptHashes': {rel(p): sha(p) for p, _, _ in changes},
              'unchangedGoverningSources': source_hashes,
              'changes': [{'file': rel(p), 'before': old, 'after': new} for p, old, new in changes],
              'ruleChanges': 0, 'newApprovals': 0, 'sourceInformationDeleted': 0,
              'nextAction': 'Reconcile all local clarifications with the completed exact verdict before manuscript acceptance.'}
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'changes'}, indent=2))

if __name__ == '__main__':
    main()
