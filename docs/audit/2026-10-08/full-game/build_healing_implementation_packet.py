"""Author the candidate review layer and exact notebook implementation packet."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
guide='''# Healing, survival and resurrection — working candidate

**IN REVIEW: exact implementation.** Three notebook conferences classify147 class sources and propose6 individual ordinary spell objects. Those spells remain inactive until individual review. This is a bounded interface, not DD24 completion:131 additional semantic matches and healing content in other domains still need dispositions. Original cards/books are preserved.

[Exact source procedures](HEALING_DEATH_SOURCE_BINDINGS.md) · [Latest boundary decisions](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_BOUNDARIES.md) · [Supplement decisions](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_SUPPLEMENT_REVIEW.md) · [Reference checks](HEALING_PLAYTEST_VALIDATION.json) · [Source integrity](HEALING_DEATH_SOURCE_VALIDATION.json)

## Distinct life operations

| Operation | Result | Restriction interface |
|---|---|---|
| Minimum-HP prevention | Preserve positiveHP instead of crossing a floor | Not HP gain; cannot create positiveHP from0 |
| Ordinary healing | Increase a living creature's normalHP | Apply modifiers, prohibitions, reserve and Critical ceiling |
| Direct state recovery | Specifically defined dying/Stable/HP recovery | Broad cannot-regain-HP applies; ordinary healing modifiers do not |
| Would-die replacement | Replace a pending death before it becomes final | Exact source eligibility; not a generic damage floor |
| Resurrection | Actually dead willing identity returns at printedHP | Separate life transition; actual corpse/soul blockers apply |
| Companion reconstruction | Restore a device/companion through its own source | No general creature resurrection permission |
| TemporaryHP | Separate nonstacking buffer | Not healing, stabilization or resurrection |

Names never select the operation. Phoenix Rebirth heals a still-living ally at0. Cleric Resurrection returns an actual dead identity. Ritual of Undeath's Ward replaces death; ordinary Death Ward is a positive-to-zero floor. Feign death and spirit manifestations are not death or resurrection.

## Damage quantities and resolution

| Quantity | Definition and use |
|---|---|
| resolvedDamage | After defenses, before tempHP; positive damage event iff greater than0 |
| tempAbsorbed | min(tempHP, resolvedDamage) |
| postTempDamage | resolvedDamage minus tempAbsorbed, uncapped by currentHP; Core Instant Death/Wounds |
| actualHpDamage | NormalHP lost to the packet after true prevention; recovery and state-assignment loss excluded |
| actualDamageDealt | NEW anti-overkill bridge: tempAbsorbed plus actualHpDamage; numeric actual-damage drains/reflections |

Ordinary “damages,” “takes damage” and “damaging hit” predicates use a positive resolved packet. Actual-HP wording (Burning Blood/Rewind Wound) uses actualHpDamage. Numeric actual-damage wording (Sanguine Rite/Echo Leech/Merciful Smite/Wound Eater/Gravebrand) uses actualDamageDealt. Source attack/hit predicates remain distinct.

Example: HP10/temp10 takes5: numeric actual damage5, actualHP damage0, positive packet. HP1 under a floor takes5: numeric0 but positive packet. HP3 takes12: numeric3, raw post-temp12. HP0 takes1: numeric0, positive packet and normal death-failure consequences.

Divine Judgment consumes its once-this-actual-target-turn entitlement on a positive packet, then reflects min(Cleric level, max(1, floor(actualDamageDealt/2))). Thus HP1-floor/numeric0 reflects1 and consumes; fully prevented resolved0 does neither. Wrathful Brand/Balanced Scales use the positive predicate where their source says damage occurred.

Resolve a damage event in this order:

1. Snapshot pre-event HP/tempHP/Wounds; resolve defenses, temp absorption and uncapped post-temp damage.
2. Core Instant Death uses postTempDamage minus preHP greater than or equal to effective maximum when reduced to0. It precedes ordinary floors. Open a legal would-die replacement; stop that packet's death procedure. No Wound save or zero-HP failure follows this branch.
3. If not Instant Death, resolve applicable true floors. They cannot raise an already0 creature. They preserve raw damage and attached conditions; a prevented drop creates no drop-only Wound trigger, but half-max/Maiming still applies.
4. Spiral-TouchedIII alone has a specific pre-Wound recovery exception. If positive-to-zero remains, spend its use, preserve that raw crossing trigger, attempt quarter-max direct recovery and apply phase-out. Broad HP-gain prohibition blocks the recovery but not the use/phase.
5. Resolve the one Core Wound save using original post-temp damage and pre-event Wounds. Fatal Wound death opens its own legal replacement window. Actual death ends Spiral phase; a successful independent Ward prevents actual death.
6. Resolve already-zero damage failures/death and its legal replacement window. A successful replacement stops skipped same-packet death branches; never replay a Wound/failure branch merely because replacement changedHP.
7. Finalize a newly surviving0 creature's dying/Stable/knockout state. Only an explicitly triggered post-zero Reaction such as Grace Reversal can act before ordinary zeroHP Reaction loss finalizes.
8. Resolve eligible post-zero Phoenix/Unyielding-style healing only if target still lives, followed by later triggers. This healing never retroactively reduces the triggering packet's numeric damage.

The affected creature chooses among simultaneously eligible offered survival effects, then rechecks remaining triggers. A paid Reaction spends its declared cost; a limited automatic survival use spends when its actual source resolves. A true floor preventing the crossing means Spiral's use is not spent. No generic extra Reaction or return from death is created.

For Ritual Ward, sufficient body and no explicitly unpreventable death are prerequisites. It can intercept Instant Death, fatal Wounds, third death-save failure, eligible direct death and lethal tracks. Positive pre-eventHP→1 is loss prevention and works through Decay. Already0 with HP gain prohibited instead becomes living Stable0: clear counters and establish a d4-hour recovery deadline immediately.

Freeze packetHpLossBeforeReplacement after true floors but before Ward. Ward metrics are min(packetHpLossBeforeReplacement, max(0, preHP minus replacementHP)); never include loss caused solely by assigning a lowerHP state. HP20 takes10 then fatal Wound/Ward1 means actualHP damage10, not19. HP5 takes100 then Ward1 means actualHP damage4, raw100.

Direct death (e.g. Wound EaterIII) produces no damage or Wound save. Its healing requires actual death; a Ward interception prevents that trigger without refunding the paid activation. False LifeI has only its printed floor and failed-death-save replacement modes sharing1/LR; it is not an all-causes Ward.

## ZeroHP permissions and start timing

A conscious but dying creature still rolls at each regular start unless Stable. Extra turns do not advance these regular-start deadlines. Further damage and actual death retain normal consequences.

Mage Undying Spellform partially overrides only zeroHP Unconscious/Incapacitated restrictions: normal speech, voluntary half-Speed movement, normal Action, legal spellcasting with that Action, and starting/maintaining concentration. No independent BA/Reaction. Existing concentration avoids automatic loss from zeroHP, but the triggering damage still requires its concentration save. Separate Stunned/Unconscious/Expedition5 or6/Silence and other restrictions still apply. Healing above0 ends the feature. Expiry at0 destabilizes, cancels the Stable recovery deadline and adds one failure; the third kills normally and permits only an eligible would-die replacement.

Oracle False LifeIII permits exactly one choice during the allowed zeroHP turn: move up to Speed, speak, or activate one Revelation. The latter uses its printed Action/BA/trigger (trigger must occur on that turn), costs and components. It can start concentration; the feature did not preserve earlier concentration. No independent actions accompany the choice.

False LifeV quarter-max direct recovery resolves at its next regular start before the death save. Blocked recovery leaves0 without invented stability; dead creatures do not revive. Spiral phase expires at its next regular start before normal start processing. Fate-BoundIV rerolls a failed death save before committing natural1/counters; use the new result. Its generic death-effect save bonus is not an ordinary death-save modifier.

## Ordinary healing arithmetic

Determine legal source, recipients, costs, clocks and available entitlements before arithmetic. The helper receives already eligible modifiers; it does not acquire class powers or validate every source for its caller.

Pre-resolution modifiers include Words of Equilibrium's formula M, Zealot's Fervor +S, Throne's Grace +1/die capped S+M, Benevolent Spirits' eligible paid-technique +M, Life Prophecy maximizing dice, and Crane's applicable +S. Conditional add-ons include Ground, Radiance, Aura of Faith, Ember Mantle, Life Linked's rolled1d4, Ranger Healing Touch, Aura of Mercy, Garden's stored+1 and Tranquil Lotus Step.

First compute without conditional add-ons. Only if this preview actually restores at least1HP, recompute that same event once with its eligible add-ons. The preview changes no pools/uses. Base5 minus5 plus a conditional3 remains0; eligible pre-resolution Benevolent3 yields3. Multiple flat class bonuses use the strongest across both passes unless an explicit source exception allows stacking. Rolled extra dice/per-die changes are separate.

Within each permitted reduction plan: formula/bonuses; per-die adjustments; compatible exact fractional multipliers with one floor after multiplication; compatible flat reductions; floor at0; broad HP prohibition; maximum/Critical/reserve caps. Intrinsic Wound Eater and systemic Corrupted remain independent factors. Duplicate same-stat per-die penalties use the strongest. Dice remain dice when maximized/shared; flat Lay on Hands and stored numeric Echoes have zero healing dice.

Blight Totem cannot compound other local healing reducers. Compare systemic factors plus Totem-half alone against systemic factors plus all otherwise compatible local reducers; use the lower result. Compatible halves multiply, compatible distinct flat penalties add, duplicate same-profile groups use strongest. Suppressed reducers do not participate.

Every present, operative, applicable next-positive-healing reduction consumes exactly once when the final event commits if its pre-reduction HP potential was positive. This includes reducers whose arithmetic branch lost to Totem or whose actual gain was later blocked. Zero potential and suppressed records consume none. Two-pass preview never consumes twice.

Critical at3Wounds caps ordinary healing at max(1, effective maximum minus1); it is not a maximumHP reduction and healing cannot lower currentHP. Reserve spends only actualHP restored. A final heal8 with room3 spends3 reserve; blocked healing spends0, other activation costs remain paid. Revival/form changes/encounter starts do not replenish reserve.

## Recovery gates, triggers and loops

False Life curse gates another creature's healing SPELL: optional Insight vs RevelationDC; success permits; failed or declined check rolls d2,1 blocks HP and2 permits. Nonspell recovery and independent nonHP components remain distinct. Burning Blood blocks the cold-tagged HP-healing component only, not independent tempHP/stabilization/resurrection.

Actual positiveHP restoration is required for Radiance's cure, Renewal's Stamina, Sanctified Reprisal and Life Prophecy's RC trigger. Meditative Healing's laterKi and Transcendent Meditation's second-pulseKi are independent components and still resolve when healing caps/blocks. Blood Tithe uses its actual qualifying hostile Bleed-death trigger and finite use; not staged farming.

Passive regeneration includes Bloodthick Node, Rapid Coagulation, Regenerative Mutation and Bio-Stabilizer's modification; these retain Reserve. Finite paid/limited pulses such as Aura of Grace, Living Pulse, Renewal Totem, Blood Feast, Exsanguinate, Hemostasis, Transcendent Meditation, Cellular Reconstruction and Adrenal Floodgate are not passive regeneration. Their own Downed/Incapacitated gates remain. A passive-regeneration prohibition is not a universal healing prohibition.

Lay on Hands retains its5×Paladin-level finite pool and ordinary Long Rest refill. Base Action spends at most level on one target; Hero1/SR spends the entire remaining pool across at most3, each allocation at least1. No RP conversion. Verdict Absolute's explicit qualifying brand-kill refill is a source exception.

Transfusion donor spends K normalHP; recipient ordinary base is K+floor(K/2). Channel Life spends X; baseX. Donor must remain at least1, tempHP cannot pay, loss is not damage and cannot be prevented/redirected/refunded when recipient gets0. Recipient legal bonuses/reductions apply.

Secondary healing retains root ID and visited application IDs in a shared causal ledger, including across sibling branches. Each link/application can fire at most once/root. Numeric add-ons remain the same packet, creating no new root/child. Legal finite primary healing may trigger unrelated eligible effects.

Stronger source flags override generic provenance: Vitality Link's child blocks every further link; Echo Leech blocks secondary healing/resource triggers; Blood Feast blocks damage/resource triggers; Merciful Smite blocks Smite/heal-copy chains; Crown Undying blocks redirection/heal-copy chains; Echoes/Spiral copies retain their explicit exclusions. Source payment and direct/actual-gain predicates still apply before a child exists.

## Excess healing

OrdinaryMissingHP = effective maximum minus currentHP. Genuine excess is max(0, legal post-reduction healing minus OrdinaryMissingHP). Broad HP prohibition makes legal healing and excess0. Critical's ceiling does not redefine missingHP: max20/HP19/Critical/legalheal10 restores0 but has9 genuine excess; the missing1 is not excess. At HP20, legalheal10 has10 excess.

This quantity alone grants no conversion. A legal converter must satisfy its own costs/caps/cadences. One excess point can fund only one conversion. Source-internal Overflowing Light resolves before outside Cosmic Equilibrium uses remaining excess. Channel Life attaches a packet-wide prohibition on ALL excess-to-tempHP conversion, including another owner's feature. It permits an otherwise eligible Cosmic damage conversion.

**Exact-review question:** Passive Reserve-based healing can produce a computed excess quantity while restoring0 and spending0 reserve. Do those particular sources qualify for Cosmic conversion at all? No conversion is authorized by the arithmetic helper; this eligibility must be resolved before activating that combination.

## Actual resurrection and retained consequences

Require an actually dead, willing identity, legal source body/anchor, location, target limit, elapsed window, paid cost and no applicable resurrection/soul blocker. ReturnedHP is a life transition, unaffected by ordinary healing multipliers or generic living HP-gain prohibitions. Explicit corpse-local and identity/soul blockers are different scopes.

Preserve Wounds/Injuries, Corruption, intrinsic Oracle Curse, debt/legal-death/body claims and spent resources. ThreeWounds is Critical, not continuous automatic death. Clear death counters/Stable deadline but preserve used turn markers and persistent histories. No duplicate creature or resource refresh.

| Class source | Exact selected procedure |
|---|---|
| Cleric Resurrection | Touch one eligible allied body, dead≤60seconds;1HP and printed2S+M tempHP1minute;3Conviction+10RP;1/LR |
| Celestial Resurgence | Up to6 eligible allied corpses30ft, dead≤18elapsedseconds;1HP;5Conviction+10RP;1/LR |
| Divine Rebirth | One successful resurrection by your Cleric feature instead max(1,floor(effectiveMax/2))HP plus printedS+M tempHP1minute;1/LR |
| Thousand Petals | At most6total including at most2eligible corpses20ft;5Ki+5RP;1/LR. Living3S d8+M healing, dead1HP. Corpse died strictly after previous source regular end. Printed floor until next source start |
| Grace Reversal | Source Reaction on surviving positive→0;10RP;one other eligible allied corpse in Oath aura since previous source regular end; Paladin stays0 |
| Soulbound Ritual / Snap Rebuild | Companion/device reconstruction via exact token/slot/expiry restrictions; no generic creature revival |

Thousand Petals revival history is campaign-persistent per Monk-owner/target identity; another Monk/source remains independent. Grace Reversal history is per Paladin-owner/target until that Paladin's qualifying Long Rest. Death of either participant resets neither. Living healing does not spend resurrection history.

Elapsed windows are inclusive (exact60seconds qualifies); previous-end windows are strictly after that typed phase20 marker through the current event. Initiative changes do not rewrite history.

## Lethal tracks after return or replacement

Both an actual resurrection and would-die replacement retain lethal tracks. Exhaustion6 becomes protected exhaustion.lethal-collapse: alive, Unconscious, no voluntary act/travel. Its static lethal endpoint is suspended for this protected return, ending once legally below6. A qualifying Long Rest can occur unconscious with another creature's care/food/water, inactive root cause and no recovery blocker.

Expedition6 retains all six provenance-bearing points and enters its existing collapse. Only genuine24hour Haven care or explicit eligible treatment can reduce it; point removal gates persist. A later positive unprevented gain at6 reevaluates either track's lethal endpoint. A fresh independently legal finite Ward may intervene; collapse is not continuing immunity.

## Removing suppressed Bleed and fire

Cures examine present, unexpired, not-ended records, including temporary suppression/acquired immunity. Initial immunity that prevented application leaves nothing to cure. Damage arbitration and active hooks still exclude suppressed/immune records.

Medicine selects one present eligible Bleed before rolling its printed/source/fallbackDC. A legal positive-potential magical heal invokes every present applicable Bleed endpoint; each Blood Curse instead receives its printedCON save. An actualHP-gain prerequisite still controls a source that expressly requires it.

A legal extinguish Action/full immersion ends all present ordinary-extinguishable fires within its scope; protected/special prerequisite fires persist. A permitted per-record fire DEX ending save remains available while suppressed when a future tick remains; no extra save after the final consumed tick. Cured records never resume when suppression ends.

## Six ordinary spell candidates — inactive until exact review

All retain preserved Action/RP/rank/class gates, and range120ft except Ward60ft. V/S/F uses the established M/F focus alternative; no imported material cost.

| Spell | Proposed individual operation |
|---|---|
| Stitch Fate | Rank8/21RP. Living dying0, not Stable/dead. Remove one recorded failure, or direct1HP recovery/clear counters; blocked latter becomes Stable0 with immediate d4-hour deadline. Not retrospective death undo |
| Death Ward | Rank4/7RP, concentration1minute. One positive-to-zero floor at1, then ends. No Instant Death/fatalWound/thirdfailure/lethal-track protection and no already0 recovery |
| Resurrection | Rank7/17RP. One willing identity, sufficient in-range remains, death≤8elapsedhours; return1HP and retained consequences/collapse |
| Mass Resurrection Denial | Rank8/21RP. Fixed20ft-radius sphere, concentration1minute (NEW supersedes Instantaneous). Corpse-local anchor block while remains inside; movement out/conc end/eligible rank8 removal ends block. Bodyless legal formation is not automatically blocked |
| True Resurrection | Rank9/26RP. One actually dead willing known identity, death≤7elapsed days. Usable in-range body or perceived legal unoccupied formation space120ft. Return1HP; every other remains anchor loses eligibility to duplicate that identity. No true-name or guessed soul-plane knowledge requirement |
| Soul Bind | Rank9/26RP, no concentration. Living dying0 perceived targetCHA save; failed save pending60seconds. PositiveHP/Stable ends pending. Death strictly before expiry creates bound identity for24hours from death. Exact expiry wins. One family record per identity; second legal failed save refreshes pending deadline, no post-death recast. Caster death/incapacity does not end it |

Soul Bind removal targets pending creature or existing post-death remains as local anchor. With no remains, removal must expressly free the bound identity/soul; invent no physical anchor. No mind control, ownership or indefinite prison. True Resurrection still obeys actual identity/soul barriers, and an already-living identity is ineligible. Complete objects retain countering, Dissonance/Refrain, costs and source access.

## Temporal dependency and validation boundary

Spiral-TouchedV Time Loop is temporal restoration, not generic resurrection. Its discussed participant contract restores recorded position, life/death/HP/temp/counters, Wounds/linked Injuries, Core/custom conditions, RC, per-encounter uses and snapshot Soul Bind state. Post-snapshot death/body destruction is conceptually undone; already-dead-at-snapshot remains dead. Generic corpse-resurrection denial does not automatically block it.

It does not restore RP/Ki/Conviction/BG, device resources, Mutation Reserve, daily/rest uses, physical consumables or its own spent use. The helper tests that field distinction only. Full equipment/environment topology, corpse/body-part duplication and clock rebasing remain in the dedicated temporal package; Time Loop is not declared fully operational by these tests.

Current selected checks:155 healing/death plus120 unchanged Core damage states;150 control including2 new clarification cases;98 custom including14 cure-presence cases;153 exact source records. These are interface tests, not execution of147 complete class cards, numerical balance, whole-game completion or a substitute for human playtesting.
'''
(ROOT/'docs/mechanics/HEALING_DEATH_PLAYTEST.md').write_text(guide,encoding='utf-8')

intro='''# Exact healing/death implementation review

Codex → Calibration Review. User asks us to continue through every aspect. This is the next bounded exact review after your first, supplement and final-boundary decisions. Original class/book objects remain unchanged. Please inspect the actual guide, helpers, tests, source dispositions and all6 spell objects below. Give concrete contradictions/bugs before accepting this scope. Do NOT close whole DD24,131 other matches, temporal world rules or the game.

Current verification:155 selected healing checks plus120 unchanged Core damage states,150 control checks plus9,393 Speed states,98 custom tests,153 source integrity records. Six spells remain inactive outside batch_*.json. Please review each six-spell object individually for later operational promotion, retaining preserved class/rank/RP metadata from the source conferences.

Two exact questions remain: (1) Passive Reserve-bound regeneration at Critical/fullHP can compute excess while restoring0/spending0 reserve. Does Cosmic Equilibrium accept such a packet? I recommend explicit exclusion of unpaid passive regeneration from excess conversion; otherwise a source that says Reserve bounds regeneration could generate radiant damage with no Reserve spend. The current helper calculates quantity only and requires separately validated converter eligibility. (2) SpiralIII phase-out survives if its later fatal Wound is prevented by an independent Ward, because actual death never occurred. Please confirm/reject.

New strictness: healing causal applications use a shared root ledger across sibling branches, not just per-path visited copies, to enforce once/application/root. The temporal helper ONLY tests selected participant fields; topology/equipment/clock issues are explicitly deferred. Lethal track reconciliation is an explicit required post-success call, not hidden in unrelated systems.

Please also inspect death-save reroll before commit, zeroHP Ward/dead identity behavior, non-damage direct death, delayed FalseLifeV, cure-presence correction, would-die metrics and all source-specific restrictions. Request missing source evidence if needed; do not infer unavailable fields.
'''
parts=[intro,'## Candidate guide\n'+guide]
for rel in ('tools/healing_playtest_rules.py','tools/validate_healing_playtests.py','data/playtest/spell_drafts/candidate_healing_death.json'):
 parts.append('## '+rel+'\n```\n'+(ROOT/rel).read_text(encoding='utf-8')+'\n```')
control=(ROOT/'tools/control_playtest_rules.py').read_text(encoding='utf-8')
parts.append('## Control damage consumers\n```python\n'+control[control.index('@dataclass\nclass WrathfulBrand'):control.index('def physical_escape_fallback')]+'\n```')
custom=(ROOT/'tools/custom_condition_rules.py').read_text(encoding='utf-8')
parts.append('## Custom condition helper (cure correction among previously reviewed logic)\n```python\n'+custom+'\n```')
bindings=json.loads((ROOT/'data/playtest/healing_death_bindings.json').read_text(encoding='utf-8'))
parts.append('## All153 source-qualified roles/overrides (unchanged exact procedures in prior source packets)\n'+json.dumps([{'bindingId':b['bindingId'],'classification':b['classification'],'overrides':b['operationalOverrides']} for b in bindings['bindings']],ensure_ascii=False,indent=2))
(HERE/'CODEX_HEALING_IMPLEMENTATION_REVIEW.md').write_text('\n\n'.join(parts),encoding='utf-8')
print('Wrote candidate guide and exact implementation packet:',sum(len(x) for x in parts),'characters')
