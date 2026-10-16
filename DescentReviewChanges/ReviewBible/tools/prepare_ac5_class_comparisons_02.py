"""Record independently read class interfaces for the forthcoming full AC5 review."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    target = A / 'AC5_CLASS_INTERFACE_ADDENDUM_02.json'
    assert not target.exists()
    selections = {'wizard': [19, 22, 23], 'mage': [15, 18], 'shaman': [41],
                  'thief': [21, 23, 24, 27], 'ranger': [7, 36], 'tinker': [28, 38],
                  'oracle': [6, 8, 54, 79], 'paladin': [69, 70, 119, 122, 142],
                  'cleric': [47], 'druid': [19]}
    cards = []
    for name, indices in selections.items():
        path = R / f'data/public/class_playtests/{name}.json'
        doc = read(path)
        for i in indices:
            cards.append({'binding': info(path), 'pointer': f'/cards/{i}', 'completeCard': doc['cards'][i],
                          'readScope': 'Current operative card independently read; original source object preserved as evidence.'})
    old = read(R / 'data/director/spell_proposals/abjuration_conjuration_rank5.json')
    old_ranger = next(x['completeCurrentEnvelope'] for x in old['completeClassComparisons'] if x['path'].endswith('/ranger.json'))
    issues = [
        ('AC5-CLASS-01', 'Wizard Dispel Magic is a distinct class spell', ['wizard.arch.dispel-magic', 'wizard.hero.spellbinder.sigil-authority'], 'Wizard class Dispel is Action3RP/60ft/Recharge2/rank3, automatic through3 and INT+PB against10+rank above3. Do not replace this with the proposed Greater Dispel10+2rank procedure or ordinary same-name payload. Sigil Authority explicitly names Counterspell and Dispel Magic checks; do not silently extend its+1 to Greater Dispel solely because both end spells.'),
        ('AC5-CLASS-02', 'Nature\'s Whisper current classification', ['ranger.base.nature-s-whisper'], 'The old AC5 Ranger envelope predates accepted NWQ. Current Nature\'s Whisper is magical NONSPELL, spellRank:null, Action1RP/Recharge3, no ordinary spell components/counter window/rank cadence, and has exact suppression and Ready rules. Lesser Antimagic may interact only through a genuinely applicable magical-technique scope; Greater Dispel needs an actual nonspell dispel interface. Nexus/Dampening do not apply merely because it costs1RP.'),
        ('AC5-CLASS-03', 'Intrinsic Oracle condition protection', ['oracle.supplement.shared.oracle-s-burden', 'oracle.supplement.shared.curse-manifestation', 'oracle.supplement.curse.tongues', 'oracle.supplement.consumed.consumed-boon-i'], 'Oracle\'s Burden expressly prevents generic remove/suspend and requires a feature naming the Oracle Curse. Do not let broad magic language suppress the entire Curse. Manifestation prevents normally voluntary Curse suppression for its3rounds; Tongues and Consumed retain their own expressly named suppression permissions and limits. Decide specific effects from the actual cards, not a blanket class erasure.'),
        ('AC5-CLASS-04', 'Spell-save defenses remain distinct', ['shaman.hero.bloodcaller.spell-resistance', 'thief.hero.arcane-trickster.arcane-resistance', 'druid.hero.land.nature-s-ward'], 'Shaman Spell Resistance already grants advantage against actual spells; the ordinary rank5ward cannot stack another advantage. Thief Arcane Resistance grants+2spell saves, not damage resistance. Druid Nature\'s Ward immunity covers Charmed/Frightened from fey/elementals plus its printed poison/disease scope, not every ability of those types or every planar removal.'),
        ('AC5-CLASS-05', 'Mage price and penetration scope', ['mage.arch.arcane-bypass', 'mage.arch.spell-efficiency'], 'Arcane Bypass ignores actual printed damage-type resistance for one declared damaging Mage spell, not immunity, antimagic, walls or endpoint blockers. Spell Efficiency needs prior real Focus-eligible cast and next differently named same-current-element eligible spell, min1, with actual exclusions. Use that predicate before the new Nexus/Dampening/Influence stages; no automatic eligibility for every Conjuration spell.'),
        ('AC5-CLASS-06', 'Limited theft and suppression are not universal dispels', ['thief.hero.arcane-trickster.spell-disruptor', 'thief.hero.arcane-trickster.magebane-blade', 'thief.hero.arcane-trickster.arcane-theft', 'ranger.hero.stalker.shattershot'], 'Preserve each trigger, save, rank cap and selected payload. Arcane Theft only temporary rank1–3buffs and printed AC/Speed/one resistance; it cannot take rank5Spell Resistance, prevention pools, summons or resources. Shattershot distinguishes shield equipmentAC from one visible rank1–3magical defense. Spell Disruptor affects observed temporary magical+AC maximum2; Resonance Barrier is not+AC merely because named shield/barrier.'),
        ('AC5-CLASS-07', 'Device abilities are not antimagic by title', ['tinker.hero.artificer.overload-suppression', 'tinker.hero.warmachine.malfunction-field'], 'Overload Suppression targets construct/device and applies its next-Reaction/attack-disadvantage/Stunned failure-by5 clauses, with shared hard-control guard. Malfunction Field imposes disadvantage on the first qualifying spell attack, once/round total; it leaves save-based areas unchanged and explicitly creates no antimagic zone.'),
        ('AC5-CLASS-08', 'Paladin aura and word do not share one suppression scope', ['paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified', 'paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word'], 'The aura uses a target-start CHA save and one Director-selected temporary beneficial non-innate magical effect, never immunities/class engines/permanent traits/attunement. The Blasphemous Word uses an Action2RP, CON and damage plus one temporary beneficial spell or regeneration effect. Keep these predicates distinct in ward/summon suppression examples.'),
        ('AC5-CLASS-09', 'Release and transfer apply only their printed components', ['paladin.supplement.oath-of-chains-broken.liberating-smite', 'paladin.supplement.oath-of-chains-broken.break-bonds', 'paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree'], 'Liberating Smite/Break Bonds operate on their actual Grappled/Restrained predicates and source release permissions, not generic Planar Binding service or Banishment. Crownshatter transfers temporary+1/+2numerical AC/attack/save bonuses only; it cannot move Spell Resistance advantage, Resonance Barrier prevention, immunity, resources or a class engine.'),
        ('AC5-CLASS-10', 'Protected books and radiant conversions', ['wizard.hero.spellbinder.spell-preservation', 'cleric.hero.priest.cosmic-equilibrium'], 'Spell Preservation protects against permanent destruction/erasure but explicitly permits suppression; a field does not destroy or duplicate the book. Cosmic Equilibrium converts actual eligible excess healing/radiant damage under two once/round pools which cannot trigger each other. Fire aura damage and prevented Barrier damage do not become qualifying Cleric radiant damage or actual damage dealt.'),
    ]
    fixtures = [
        ('Wizard class and ordinary dispels', 'Use a real rank7 ongoing source. Class Dispel DC17 with INT4+PB4 and die10 totals18: success. Proposed Greater Dispel DC24 with the same modifiers and die15 totals23: failure unless its own reviewed rule changes. Record Action/RP/recharge separately and do not automatically add Sigil Authority to Greater Dispel.'),
        ('Nature\'s Whisper in a field', 'Actual Ranger with personalRP5 uses lawful Nature\'s Whisper inside Nexus plus Dampening: it remains a nonspell technique with its own1RP/recharge rules. Separately apply eligible antimagic suppression to the same technique without granting ordinary Counterspell or a guessed spell rank.'),
        ('Oracle exact protection', 'Oracle2+ with Burden and selected Tongues enters Lesser Antimagic while Curse Manifestation is active. Decide only source-permitted specific suppression; no generic removal of intrinsic Curse or its protected drawbacks.'),
        ('Different save defenses', 'A Shaman Bloodcaller with its actual passive receives ordinary Spell Resistance: one advantage only. Separately a Thief with Arcane Resistance receives the ward: apply one advantage plus its actual+2spell-save modifier under existing bonus rules; generic concentration saves do not acquire spell-save provenance.'),
        ('Theft and prevention', 'A Thief attempts Arcane Theft against rank5Spell Resistance, then Spell Disruptor against a Resonance Barrier prevention pool. Both fail the respective rank/payload predicate; neither becomes an AC bonus from a name.'),
        ('Tinker versus save area', 'A caster under a real Malfunction Field uses proposed Massive Elemental Blast, which resolves via target DEX saves. No spell attack exists for the device\'s disadvantage to affect.'),
        ('Paladin release versus service', 'A target is subject to Planar Binding service but is neither Grappled nor Restrained. Break Bonds and Liberating Smite do not automatically end that unrelated binding record. A separately sourced actual restraint uses its own release branch.'),
        ('Aura and word suppression', 'Use actual Inferno Paladin cards69and70 against a recipient with temporary Spell Resistance and a distinct intrinsic immunity. Respect each save/timing/eligibility and never suppress the immunity via the aura.'),
    ]
    data = {
        'id': 'AC5-CLASS-INTERFACE-ADDENDUM-02', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Prepared and unsent; concrete source comparisons for forthcoming AC5 conference, no new spell approvals.',
        'parentAudit': info(A / 'AC5_CURRENT_SOURCE_INTERFACE_AUDIT_01.json'),
        'independentlyReadCardCount': len(cards), 'completeCurrentCards': cards,
        'scopeWarning': '25 selected operative cards read; not exhaustive semantic review of all17 classes or approval of pending AC5 rules.',
        'rangerDrift': {'historicalBinding': next(x for x in old['completeClassComparisons'] if x['path'].endswith('/ranger.json'))['sha256'], 'pointer': '/cards/7/effect', 'historicalEffect': old_ranger['cards'][7]['effect'], 'currentCardId': 'ranger.base.nature-s-whisper', 'interpretation': 'Current NWQ nonspell classification and activation/rider procedure supersede the shorter historical comparison text.'},
        'issues': [{'id': i, 'title': title, 'cardIds': ids, 'requiredReview': text} for i, title, ids, text in issues],
        'additionalExamples': [{'id': f'AC5-K{i:02}', 'title': title, 'requiredResolution': text, 'runtimeTest': False, 'newSpellRuleAdopted': False} for i, (title, text) in enumerate(fixtures, 1)],
        'sourceInformationDeleted': 0, 'newSpellAdoptions': 0, 'runtimeTestsExecuted': 0, 'humanPlaytested': False,
    }
    assert len(cards) == 25
    target.write_bytes(encoded(data))
    print(json.dumps({'addendum': info(target), 'currentCardsRead': len(cards), 'issues': len(issues), 'additionalExamplesRequired': len(fixtures)}))


if __name__ == '__main__':
    main()
