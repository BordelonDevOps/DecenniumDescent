"""Preserve existing navigation, then point users to the complete class drafts."""
from pathlib import Path
import json,hashlib,shutil
REVIEW=Path(__file__).resolve().parents[1];ROOT=REVIEW.parents[1]
AUDIT=ROOT/'docs/audit/2026-10-08';BACKUP=ROOT/'_preserved/2026-10-08/all-class-pass'
paths=['START_HERE.md','docs/audit/2026-10-08/READINESS.md','DescentReviewChanges/ReviewBible/RECOVERY_REVIEW_2026-10-08.md','DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCEMENT_PLAYTEST_PROPOSAL.md']
ledger=[]
for rel in paths:
 p=ROOT/rel;b=BACKUP/rel;b.parent.mkdir(parents=True,exist_ok=True)
 if not b.exists():shutil.copy2(p,b)
 ledger.append({'path':rel,'originalBackup':b.relative_to(ROOT).as_posix(),'originalSha256':hashlib.sha256(b.read_bytes()).hexdigest()})

p=ROOT/paths[0];s=p.read_text(encoding='utf-8')
s=s.replace('| Bard pilot — current design work | [Complete 50-card Bard draft](DescentReviewChanges/ReviewBible/docs/mechanics/BARD_PLAYTEST_v0_1.md), including all three Hero paths and level 1–20 choices. Provisional mechanics; ready for a focused table test. |','| Start a Base-class character | [Base class starting guide](DescentReviewChanges/ReviewBible/docs/mechanics/BASE_CLASSES_START_HERE.md) — all 17 identities, with Arch and Hero kept as later progression. |\n| Complete class playtest drafts | [All-class library](DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md): 1,223 cards, costs, timing, source wording, level 1–20 progression and legal builds. Provisional mechanics; human balance testing remains. |')
s=s.replace('The next work is to reconcile advancement and feature acquisition across the books and registries, bring reviewed gameplay procedures into one usable candidate, close the public/Director data mismatch, and run an actual table playtest.','The class playtest drafts and reviewed gameplay procedures now provide a concrete candidate for review. Remaining game-wide work includes ordinary-spell and live companion integration, character-sheet consistency, closing the public/Director data mismatch, and an actual table playtest.')
p.write_text(s,encoding='utf-8')

p=ROOT/paths[1];s=p.read_text(encoding='utf-8')
s=s.replace('| Reconcile all 17 classes and level 1–20 acquisition | In progress |','| Reconcile all 17 classes and level 1–20 acquisition | Provisional class packets complete |')
s=s.replace('| Normalize unresolved ability wording | Bard 50-card draft complete; remaining classes open |','| Normalize unresolved ability wording | All 17 class packets complete; broader spell catalog remains separate |')
s=s.replace('| Playtest materials | Open |','| Playtest materials | Class guides, legal builds and session log complete; campaign kit open |')
s=s.replace('This is direction to develop scheduled feature choices in the Bard pilot; it is not blanket numerical approval or automatic adoption by every other class.','The owner then requested “do all the classes like this” and clarified that these are Base classes, with Arch and Hero afterwards. This authorizes the all-class drafting pass, while numerical approval remains separate.')
s=s.replace('The other classes remain to be completed.','All 17 now have [class packets](../../../DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md) and an explicit [Base-class entry point](../../../DescentReviewChanges/ReviewBible/docs/mechanics/BASE_CLASSES_START_HERE.md).')
section='''

## All-class follow-up

All 17 Base class families now have the Bard-style treatment: operational cards, protected engines, original wording, costs/actions/targets/durations, level gates and worked turns. The library contains 1,223 cards including later Arch/Hero abilities, exceptional forms, Mysteries, Curse Boons, Oaths and inversions. These later branches are not additional Base classes or level-1 grants.

The structural validator passes 144 checks. It includes 3,900 sampled ordinary-class acquisitions (plus the Bard validator’s 300), 1,800 Oracle Mystery/Curse/ordered-Tier-II configurations, 70 Druid Circle/Arch-form pairs and 120 Paladin Oath/inversion/style/aura configurations. These are acquisition and written-rule checks, not complete combat simulations. All eight main Word books match the preserved source hashes.

The source supplements and notebook replies remain in the audit record. The interrupted Paladin response was preserved; its 51 complete objects were recovered and the missing nine Martyr King cards were explicitly completed and submitted for notebook review. No original files were deleted. Current navigation originals are preserved under `_preserved/2026-10-08/all-class-pass`.

This completes the requested class-drafting pass. Live character-sheet integration, the entire ordinary spell catalog, human campaign balance and publication remain separate work items.
'''
if '## All-class follow-up' not in s:s+=section
p.write_text(s,encoding='utf-8')

p=ROOT/paths[2];s=p.read_text(encoding='utf-8')
s=s.replace('**Status: assembled procedure candidate with a complete Bard performance draft; other class mechanics incomplete.**','**Status: assembled procedure candidate with provisional packets for all 17 Base class families and their later Arch/Hero progression.**')
s=s.replace('The owner supports developing that Bard direction.','The owner requested extending the Bard treatment to every Base class, preserving later Arch/Hero stages.')
line='- [Start with a Base class](docs/mechanics/BASE_CLASSES_START_HERE.md), then use the [complete class library](docs/mechanics/CLASS_PLAYTEST_INDEX.md), [legal builds](docs/mechanics/CLASS_PLAYTEST_BUILD_EXAMPLES.md) and [shared session log](docs/mechanics/CLASS_PLAYTEST_SESSION_LOG.md).\n'
if line not in s:s=s.replace('## Ready to review\n\n','## Ready to review\n\n'+line)
s+='\n## All-class validation\n\nRun `python tools/build_class_playtests.py`, `python tools/validate_class_playtests.py`, then `python tools/build_class_examples.py` from this ReviewBible. The [validation report](docs/mechanics/CLASS_PLAYTEST_VALIDATION.json) records 144 checks and their exact scope. Card data are review/reference artifacts, not a complete live effect engine. See the [all-class audit](../../docs/audit/2026-10-08/classes/CLASS_PASS_REPORT.md) for collaboration, source-preservation and remaining limitations.\n' if '## All-class validation' not in s else ''
p.write_text(s,encoding='utf-8')

p=ROOT/paths[3];s=p.read_text(encoding='utf-8')
s=s.replace('Scheduled feature selections are therefore the working direction for the Bard pilot.','The owner subsequently requested this treatment for all Base classes, with Arch and Hero afterwards. Scheduled choices are the working direction for ordinary class families.')
s=s.replace('numerical balance and adoption by other classes remain provisional.','the [all-class library](CLASS_PLAYTEST_INDEX.md) now implements explicit class-specific schedules. Numerical balance remains provisional.')
s=s.replace('Each class still needs its source-specific table reconciled.','The linked class packets contain the reconciled test tables and take precedence over this generic schedule when an explicit exception differs. Cleric, Mage and Warrior permit broader Base/Arch choices at certain levels; Mage chooses its level-20 feature; Wizard Elementalist counts its automatic Affinity as one of its two level-10 acquisitions. See the guide rather than silently granting both alternatives.')
s=s.replace('Complete the remaining class milestones from its own sources. Resolve the d6/d8 discrepancy explicitly before freezing a character sheet.','The Oracle packet completes those milestones, chooses the detailed-book d6 chassis, and preserves the conflicting registry d8 alternative.')
s=s.replace('Entries with no recoverable acquisition level must be mapped individually.','The Paladin packet supplies all ten Oaths and inversions with explicit gates, and separately labels its new shared Forbidden spells.')
p.write_text(s,encoding='utf-8')
for row in ledger:
 p=ROOT/row['path'];s=p.read_text(encoding='utf-8').replace('144 checks','151 checks');p.write_text(s,encoding='utf-8')
 row['newSha256']=hashlib.sha256(p.read_bytes()).hexdigest()
(AUDIT/'all_class_navigation_changes.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
print('Updated four navigation documents with preserved pre-edit copies.')
