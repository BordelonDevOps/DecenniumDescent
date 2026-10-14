# Healing source extensions — remaining class passages

**Three selected primitives reviewed; broader integrations remain open.** All131 remaining class passages have individual roles in the [source register](HEALING_REMAINING_SOURCE_BINDINGS.md), with [exact-source verification](HEALING_REMAINING_SOURCE_VALIDATION.json). The [exact extension review](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_EXTENSIONS_CLOSURE.md) closes only the three procedures below. Read the [first captured discussion](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_REMAINING_REVIEW_PARTIAL.md) together with the [complete tail and corrections](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_REMAINING_CORRECTIONS.md); the first capture alone is incomplete.

The previously reviewed [153-source interface](HEALING_DEATH_PLAYTEST.md) remains the arithmetic/life-state reference, with the narrow Paladin Wave cadence amendment below. Original sources and earlier interpretations remain preserved.

## Three corrected source procedures

### Zealot's Renewal backlash

Attempt the healing first. Its Poisoned/disease option is an independent component, so lack of actual HP gain does not prevent that option. Unless a printed Convergence/Prophecy feature suppresses the backlash, roll its separate1d4 fire packet, apply ordinary defenses, then enforce at least1 resolved backlash damage. Fire immunity alone therefore does not eliminate this particular source's minimum.

This minimum concerns damage, not the creature's surviving HP. Then temporary HP, normal HP loss, Wounds and dying/death apply normally. A creature at1HP without temporary HP can fall to0 from the backlash; a legal temporary-HP buffer can absorb it. A blocked heal still has its backlash unless expressly suppressed.

### Crown's Burn pooled healing

Use the numeric actual fire damage dealt to qualifying meaningful hostile creatures, including absorbed temporary HP and excluding overkill as defined in the reviewed interface. A positive packet that inflicts zero numeric actual damage contributes zero.

For up to3 distinct legal allied recipients, divide the total by the recipient count and round down. Use one shared `S d6 + M` healing-cap roll for the burst. If the numeric total is positive, each recipient's source base is `max(1, min(share, sharedCapRoll))`. With no recipients, skip healing; with numeric total0, generate no healing application.

Each resulting target application then receives its own ordinary healing modifiers/restrictions. The source minimum does not bypass Decay or guarantee actual HP gain. Retain the same roll identity and S healing dice for each target's per-die adjustments.

Declare and lock the allied recipients at activation, before hostile saves, damage or the shared healing-cap roll. Enhanced mastery changes the selection range only. If a declared recipient becomes ineligible before healing, skip its application without replacement or recalculating the denominator. The other recipients keep the same shares.

### Dual Echo Cast with two Mend profiles

Two otherwise eligible Mend records from different source creatures may both be used. Pay both RP costs, consume both records and spend the single combined release/action. Halve each legal profile's rolled amount independently, rounding down once. The resulting halves are copied numeric amounts with zero newly rolled healing dice; separately authorized additional dice retain their actual provenance.

The two components may heal the same legal ally. They are distinct supplied components; neither is erased just because both use Mend. Preserve ordinary copy/no-resource/no-recursion restrictions and shared-root causal limits. No extra release is created.

Echo Fusion's printed “only one may be healing” restriction belongs to Echo Fusion. It is not a Dual Echo Cast limitation.

The [21 extension checks](HEALING_EXTENSION_VALIDATION.json) test these selected boundaries, including loss of a declared recipient. Full record acquisition, RP spending, target legality and command/release lifecycle remain caller/source responsibilities; these helpers are not complete class execution.

## Paladin cadence amendment

The explicit reconciliation in `paladin.engine[13]` sets level17 Full Cleansing Wave to **once per long rest**, superseding the preserved Hero card and the earlier healing guide's once-per-short-rest wording. Retain its entire remaining pool cost, target limits, cleansing option and corresponding Oathbreaker mode. Switching Oath state does not refill the pool.

Paid Smite obeys both own-turn eligibility and the shared **one paid Smite per numbered round**, including an independently allowed Reaction Smite. An off-turn Smite can therefore consume the round's allowance before the Paladin's regular turn. The Reaction source supplies that specific permission; the general rule adds no new off-turn trigger.

## Other discussed interfaces

| Source or family | Agreed direction | Remaining work |
|---|---|---|
| Divine Invocation Renewal | Printed5 Stamina co-resolves independently of actual HP gain; base Renewal retains its actual-gain requirement | Integrate exact finite Stamina resource rules |
| Purging Flame / Zealot's Renewal | Printed cure option independent of actual HP gained | Preserve each disease's actual permitted save/cure |
| Bloodbond / Flame Prophecy / Enhanced Convergence | Healing-trigger branches require actual HP restoration; Flame's damage branch uses positive fire packet | Source provenance/cadence implementation |
| Lifewell | Action+4RP+allBG establishes it; even first pulse needs same-turn BA+1RP; without that pulse, end at turn end | Paid pulse scheduler |
| Healing Briar / Restoration Field | Activation includes first pulse; later pulses require printed maintenance | Paid pulse scheduler |
| Oracle target-start healing zones | Proposed source-owned funded windows: activation window, then1RC at each next source regular start; not per ally | Exact schedule/expiry/target cap review |
| Crown Restored / Eternal Bloom Finals | Printed finite pulses included in limited use; no generic extra RC upkeep | Final-specific clocks and pulse limits |
| Renewal / Echo Totem | Shared upkeep/concentration; same-name overlap uses stronger application; fourth pulse requires paid BA+1RP | Exact echo/parent lifecycle and schedule |
| Monk maximum-HP effects | Stat changes clamp currentHP without damage/healing/Wounds; restoring maximum does not heal | [58-source composition interface reviewed](MAXIMUM_HP_PLAYTEST.md); wider advancement/unsupplied modifiers remain open |
| Veinburst Requiem | Post-damage set-to0 is a separate state component; no second Wound save or added damage metric | Broad versus damage-only floor scope and zero-state transition |
| Devices, companions and forms | Separate organic healing, functional repair, destroyed reconstruction, initialHP and finite tempHP reserves | Individual lifecycle/source evidence |
| Copies and added dice | Copied numeric halves have zero new dice; actual added dice and shared roll identities persist | Complete roll/copy provenance interface |

## Next review packages

1. Damage sharing/redirection: [39 sources plus2 supporting device passages reviewed](DAMAGE_SHARING_PLAYTEST.md), including exact pre/post-defense sequence and inherited consequences.
2. Maximum-HP composition: [58 supplied passages reviewed](MAXIMUM_HP_PLAYTEST.md), including Monk, Flesh Warden, Exhaustion, Expedition and selected feats/thresholds.
3. [Selected sustained-zone and pulse scheduling interface](HEALING_PULSE_PLAYTEST.md):100 roles plus6 supporting passages reviewed;89 checks and301 reserve partitions.
4. [Selected device/Totem lifecycle](DEVICE_LIFECYCLE_PLAYTEST.md):74 roles plus3 shared paragraphs reviewed;132 checks and1,200 states. Broader living companions, Druid forms/Buffer Reserve and tempHP remain open.
5. Roll/copy provenance: exact numeric components, dice, per-die modifiers, eligible copied restrictions and shared causal limits.

Discussion dispositions identify the work; they do not replace those remaining implementation reviews or human playtesting.
